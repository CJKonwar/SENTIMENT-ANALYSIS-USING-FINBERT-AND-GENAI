import PyPDF2
import requests
import json
from dotenv import load_dotenv
import os
import json



load_dotenv()
VULTR_API_KEY = os.getenv("VULTR_API")
collection_name = "FINBERT"  


VECTOR_STORE_ENDPOINT = "https://api.vultrinference.com/v1/vector_store"

# Set up the headers
headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}


payload = {
    "name": collection_name  
}


response = requests.post(VECTOR_STORE_ENDPOINT, headers=headers, data=json.dumps(payload))


if response.status_code == 201:  
    print("Collection created successfully:", response.json())
else:
    print("Error creating collection:", response.status_code, response.text)





