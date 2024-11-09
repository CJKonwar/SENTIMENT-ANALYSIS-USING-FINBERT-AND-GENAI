import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('VULTR_API')
#Function to see no of models available at vultr api
def fetch_model():
    # Set the headers 
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Make the GET request to the Vultr API
    response = requests.get("https://api.vultrinference.com/v1/chat/models", headers=headers)

    # Check if the request was successful and print the response
    if response.status_code == 200:
        print("Available models:")

        data = response.json()

        print([model['model'] for model in data['models']])

    else:
        print(f"Failed to retrieve models: {response.status_code}")


if __name__ == "__main__":
    fetch_model()
