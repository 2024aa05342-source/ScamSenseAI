# test_retrieval.py

from modules.chroma_store import retrieve_context

results = retrieve_context(
    "Share OTP immediately or your account will be blocked"
)

for item in results:
    print(item)