from modules.llm_engine import generate_response
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
        
        parsed = json.loads(content)

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