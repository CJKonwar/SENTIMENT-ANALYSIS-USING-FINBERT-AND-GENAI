import requests
import os
from dotenv import load_dotenv

load_dotenv()


VULTR_API_KEY = os.getenv("VULTR_API")


VECTOR_STORE_ENDPOINT = "https://api.vultrinference.com/v1/vector_store"


headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}


response = requests.get(VECTOR_STORE_ENDPOINT, headers=headers)


if response.status_code == 200: 
    print("Collections retrieved successfully:", response.json())
else:
    print("Error retrieving collections:", response.status_code, response.text)
