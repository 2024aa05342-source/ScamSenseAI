from datetime import datetime


def get_risk_level(score):

    if score >= 81:
        return "CONFIRMED SCAM"

    elif score >= 51:
        return "LIKELY SCAM"

    elif score >= 21:
        return "SUSPICIOUS"

    return "SAFE"


def generate_report(
    input_type,
    analysis_result
):

    return {

        "case_id":
            f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}",

        "timestamp":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "input_type":
            input_type,

        "risk_score":
            analysis_result.get("risk_score", 0),

        "risk_level":
            get_risk_level(
                analysis_result.get("risk_score", 0)
            ),

        "scam_type":
            analysis_result.get("scam_type", "Unknown"),

        "red_flags":
            analysis_result.get("red_flags", []),

        "evidence":
            analysis_result.get("evidence", []),

        "recommendation":
            analysis_result.get("recommendation", "")
    }