import PyPDF2
import requests
import json
from dotenv import load_dotenv
import os
import json



load_dotenv()
VULTR_API_KEY = os.getenv("VULTR_API")
collection_name = "FINBERT"  # Replace with your desired collection name


VECTOR_STORE_ENDPOINT = "https://api.vultrinference.com/v1/vector_store"

# Set up the headers
headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}

# Define the payload
payload = {
    "name": collection_name  
}

# Make the POST request to create the vector store collection
response = requests.post(VECTOR_STORE_ENDPOINT, headers=headers, data=json.dumps(payload))


if response.status_code == 201:  
    print("Collection created successfully:", response.json())
else:
    print("Error creating collection:", response.status_code, response.text)





