import requests
import os
import json
from dotenv import load_dotenv




load_dotenv()

# Set your API key and other parameters
VULTR_API_KEY = os.getenv("VULTR_API")
collection_id = "finbert"  
model_name = "llama2-7b-chat-Q5_K_M"
user_message = input()  


CHAT_COMPLETION_ENDPOINT = "https://api.vultrinference.com/v1/chat/completions/RAG"

# Set up headers
headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}


payload = {
    "collection": collection_id,
    "model": model_name,
    "messages": [
        {
            "role": "user",
            "content": user_message
        }
    ],
    "max_tokens": 512,
    "seed": -1,
    "temperature": 0.8,
    "top_k": 40,
    "top_p": 0.9
}


response = requests.post(CHAT_COMPLETION_ENDPOINT, headers=headers, data=json.dumps(payload))


if response.status_code == 200:  
    print("Response received:", response.json())
else:
    print("Error:", response.status_code, response.text)
