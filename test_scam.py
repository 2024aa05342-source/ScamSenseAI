from modules.risk_engine import analyze_scam

msg = """
URGENT: Your bank account will be suspended today.
Click https://fake-bank-login.com immediately and provide your OTP to verify your identity.
"""

result = analyze_scam(msg)

print(result)
