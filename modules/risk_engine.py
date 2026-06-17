from modules.llm_engine import generate_response
from modules.rule_engine import calculate_rule_score
import json
import time
from modules.rag_engine import get_knowledge
from modules.chroma_store import retrieve_context
from modules.report_generator import generate_report
from modules.agents import (
    EvidenceAgent,
    KnowledgeAgent,
    RiskAgent,
    ReportAgent
)

def analyze_scam(text):

    rule_score, rule_reasons = calculate_rule_score(text)
    print("RULE SCORE:", rule_score)
    print("RULE REASONS:", rule_reasons)
    if rule_score == 0 :

        print("SAFE SHORTCUT ACTIVATED")

        report = generate_report(
            input_type="Text",
            analysis_result={
                "risk_score": 0,
                "risk_level": "SAFE",
                "scam_type": "Normal Message",
                "red_flags": [],
                "evidence": [],
                "recommendation": "No scam indicators detected."
            }
        )

        return report
        
    retrieved_items = retrieve_context(text)

    knowledge = ""

    for item in retrieved_items:

        knowledge += (
            f"Source: {item['source']}\n"
            f"Content: {item['text']}\n\n"
        )


    prompt = f"""
You are an expert cyber fraud analyst.

Reference Knowledge:

{knowledge}

Use only the provided reference knowledge.

You MUST populate the evidence field.

For every red flag identified,
include at least one supporting evidence item.

Each evidence item MUST reference the source file.

Example:

[
 "rbi_advisories.txt: Banks never ask customers to share OTPs.",
 "phishing_patterns.txt: Immediate account blocking is a common phishing tactic."
]
Analyze the message and classify the scam risk.

Risk Scoring Rules:

0-20 = Safe Message
21-50 = Suspicious Message
51-80 = Likely Scam
81-100 = Confirmed Scam

Scoring Guidance:

- OTP requests should usually score above 85.
- Requests for passwords or banking credentials should score above 90.
- Threats such as account suspension, account blocking, KYC expiry, or urgent action should increase risk significantly.
- Fake prizes, lottery winnings, investment scams, and job scams should usually score above 80.
- Legitimate service notifications with no request for action should score below 30.

IMPORTANT:

A message should NOT be classified as a scam
simply because it mentions:

- bank
- government office
- courier
- family member
- police officer

There must be at least one scam indicator:
- OTP request
- KYC demand
- Password request
- Account suspension threat
- Remote access software
- Payment request
- Suspicious link


Message To Analyze:

{text}

Return ONLY valid JSON.

Schema:

{{
    "risk_score": 0,
    "scam_type": "",
    "red_flags": [],
    "evidence": [],
    "recommendation": ""
}}
"""

    start = time.time()

    content = generate_response(prompt)
    
    end = time.time()
    
    print(f"LLM Time: {round(end-start,2)} seconds")
    
    print("RAW RESPONSE:")
    print(content)

    try:

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()
        
        decoder = json.JSONDecoder()
        
        parsed, idx = decoder.raw_decode(content)
        
        print("PARSED JSON SUCCESSFULLY")
        print("JSON ENDS AT:", idx)
        print("REMAINING CONTENT:")
        print(content[idx:])
        
     
       
        llm_score = parsed.get("risk_score", 0)
        print("LLM SCORE:", llm_score)
        
        final_score = max(llm_score, rule_score)
        print("FINAL SCORE:", final_score)
        
        parsed["risk_score"] = final_score
        if rule_reasons:

            if "red_flags" not in parsed:
                parsed["red_flags"] = []
        
            parsed["red_flags"].extend(rule_reasons)
        
        message = text.lower()
        
        score = parsed.get("risk_score", 0)
        
        if "otp" in message:
            score = max(score, 90)
        
        if "kyc" in message:
            score = max(score, 80)
        
        if (
             "account suspended" in message
              or "account will be suspended" in message
              or "suspended today" in message
          ):
            score = max(score, 85)
        
        if (
            "account blocked" in message
            or "account will be blocked" in message
            or "blocked immediately" in message
        ):
            score = max(score, 85)
        
        if "verify your account" in message:
            score = max(score, 80)
        
        if "bank" in message and "otp" in message:
            score = max(score, 95)
        if "anydesk" in message or "teamviewer" in message:
            score = max(score, 90)
        
        parsed["risk_score"] = score
        if score >= 81:
            parsed["risk_level"] = "CONFIRMED SCAM"
        elif score >= 51:
            parsed["risk_level"] = "LIKELY SCAM"
        elif score >= 21:
            parsed["risk_level"] = "SUSPICIOUS"
        else:
            parsed["risk_level"] = "SAFE"
        
        
        print("PARSED RESULT:")
        print(parsed)

        report = generate_report(
            input_type="Text",
            analysis_result=parsed
        )

        agent_findings = {

            "Evidence Agent":
                EvidenceAgent.run(parsed),

            "Knowledge Agent":
                KnowledgeAgent.run(
                    retrieved_items
                ),

            "Risk Agent":
                RiskAgent.run(report),

            "Report Agent":
                ReportAgent.run()
        }

        report["agent_findings"] = (
            agent_findings
        )

        return report

    except Exception as e:

        print("JSON Parse Error:", e)

        report = {
            "case_id": "ERROR",
            "timestamp": "",
            "input_type": "Unknown",
            "risk_score": 0,
            "risk_level": "UNKNOWN",
            "scam_type": "Unknown",
            "red_flags": [],
            "evidence": [],
            "recommendation": content
        }

        return report