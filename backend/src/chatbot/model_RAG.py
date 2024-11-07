import requests
import os
import json
from dotenv import load_dotenv




load_dotenv()


VULTR_API_KEY = os.getenv("VULTR_API")
collection_id = "finbert"
model_name = "llama2-7b-chat-Q5_K_M"

def get_response(user_message):

    chat_completion_endpoint = "https://api.vultrinference.com/v1/chat/completions/RAG"

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
        "max_tokens": 1024,
        "seed": -1,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.9
    }


    response = requests.post(chat_completion_endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
        return result
    else:
        return response.status_code, response.text
    
    
def get_response1(prompt):

    api_url = "https://api.vultrinference.com/v1/chat/completions"  # Example URL, change as needed
    api_key = os.getenv("VULTR_API")

    # Check the api keys are loaded correctly
    if api_key is None:
        print("Error: API keys are not loaded properly.")
        return

    # Concatenate the headlines
    # "zephyr-7b-beta-Q5_K_M",
    payload = {
        "model": "llama2-13b-chat-Q5_K_M",  # Load the model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "seed": 50,
        "temperature": 2,
        "top_k": 40,
        "top_p": 0.9,
        "stream": False  # Set to False if streaming is not supported
    }

    # Set the headers, including the authorization header with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  # Set the type of content to json
    }

    # Make post request to api
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Parse and print the generated response
        response_data = response.json()
        summary = response_data['choices'][0]['message']['content']
        return summary
    else:
        return f"Error {response.status_code}: {response.text}"