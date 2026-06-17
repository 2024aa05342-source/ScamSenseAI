def calculate_rule_score(text):

    text = text.lower()

    score = 0
    reasons = []

    # High confidence indicators

    if "otp" in text:
        score += 60
        reasons.append("OTP requested")

    if "anydesk" in text or "teamviewer" in text:
        score += 90
        reasons.append("Remote access software")

    if "upi pin" in text:
        score += 90
        reasons.append("UPI PIN requested")

    if "cvv" in text:
        score += 90
        reasons.append("CVV requested")

    if "password" in text:
        score += 80
        reasons.append("Password requested")

    # Medium confidence indicators

    if "kyc" in text:
        score += 30
        reasons.append("KYC pressure")

    if (
        "account suspended" in text
        or "account will be suspended" in text
        or "suspended today" in text
    ):
        score += 40
        reasons.append("Account suspension threat")

    if (
        "account blocked" in text
        or "account will be blocked" in text
        or "blocked immediately" in text
    ):
        score += 40
        reasons.append("Account blocking threat")

    if "urgent" in text:
        score += 10
        reasons.append("Urgency tactic")

    # Suspicious links

    if (
        "http://" in text
        or "https://" in text
        or "www." in text
    ):
        score += 25
        reasons.append("Suspicious link")

    return min(score, 100), reasons