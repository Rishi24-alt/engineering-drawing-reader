import os
import urllib.request
import json

api_key = os.getenv("OPENAI_API_KEY")
user_token = os.getenv("DRAFTAI_USER_TOKEN", "")

payload = json.dumps({"api_key": api_key, "user_token": user_token}).encode()

req = urllib.request.Request(
    "http://localhost:7432/set_api_key",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

urllib.request.urlopen(req)

print("API key saved!")
