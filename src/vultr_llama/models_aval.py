import pathlib

import requests
import json
from dotenv import load_dotenv
import os
# Replace with your actual Vultr API key
load_dotenv(pathlib.Path.cwd() / '.env')

api_key = os.getenv('VULTR_API')

def fetch_model():
    # Set the headers for authorization
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Make the GET request to the Vultr API
    response = requests.get("https://api.vultrinference.com/v1/chat/models", headers=headers)

    # Check if the request was successful and print the response
    if response.status_code == 200:
        print("Available models:")

        data = response.json()
        # return data[0]

        print([model['model'] for model in data['models']])

    else:
        print(f"Failed to retrieve models: {response.status_code}")


if __name__ == "__main__":
    fetch_model()