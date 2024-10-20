import torch
import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='../../.env')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def generate_summary_and_insights(headlines_df):
    api_url = "https://api.vultrinference.com/v1/chat/completions"  # Example URL, change as needed
    api_key = os.getenv("VULTR_API")

    # Check if API keys are loaded correctly
    if api_key is None:
        print("Error: API keys are not loaded properly.")
        return


    # Concatenate headlines into a single string
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    prompt = (
        "Analyze the following news headlines and provide a structured summary along with investment insights:\n\n"
        f"Use the information from the following headlines:\n{headlines_text}\n\n"
        "Please include the following sections in your response:\n"
        "1. Summary: A brief summary of the news headlines.\n"
        "2. Short-Term View: An assessment of the stock's potential performance in the short term.\n"
        "3. Long-Term View: An assessment of the stock's potential performance in the long term.\n"
        "4. Investment Recommendation: Suggestions on whether it’s a good time to invest in this company based on the analysis.\n"
        "\nProvide your insights in a clear and concise manner without reiterating the headlines."
    )

    payload = {
        "model": "llama2-13b-chat-Q5_K_M",  # Replace with the model name you want to use
        "messages": [
            {
                "role": "user",  # Set to user role with the prompt content
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "seed": -1,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.9,
        "stream": False  # Set to False if streaming is not supported
    }

    # Set the headers, including the authorization header with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  # Set content type to JSON
    }

    # Make the POST request to the API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Parse and print the generated response
        response_data = response.json()
        # summary = response_data['choices'][0]['message']['content']
        #
        # # Clean up the summary if needed (optional)
        # # For instance, you can split it at the first line break if you only want the summary part
        # cleaned_summary = summary.split("\n\n", 1)[0]  # Keep only the first paragraph
        #
        # # Print the extracted summary
        # print("Extracted Summary:")
        # print(summary)
        return response_data
    else:
        return f"Error {response.status_code}: {response.text}"


if __name__ == '__main__':
    generate_summary_and_insights()
