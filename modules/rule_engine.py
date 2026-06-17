def calculate_rule_score(text):

    text = text.lower()

    score = 0
    reasons = []

    if "otp" in text:
        score += 50
        reasons.append("OTP requested")

    if "kyc" in text:
        score += 30
        reasons.append("KYC pressure")

    if "account blocked" in text:
        score += 30
        reasons.append("Account blocking threat")

    if "account suspended" in text:
        score += 30
        reasons.append("Account suspension threat")

    if "urgent" in text:
        score += 10
        reasons.append("Urgency tactic")

    if "click link" in text:
        score += 25
        reasons.append("Suspicious link")

    return min(score,100), reasons