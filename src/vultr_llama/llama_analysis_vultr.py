import torch
import requests
import os
from dotenv import load_dotenv

import src.news_fetcher as news_fetcher

# Loading the environment variable
load_dotenv()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



def send_request(prompt):
    api_url = "https://api.vultrinference.com/v1/chat/completions"  # Example URL, change as needed
    api_key = os.getenv("VULTR_API")

    # Check the api keys are loaded correctly
    if api_key is None:
        print("Error: API keys are not loaded properly.")
        return

    # Concatenate the headlines
    # "zephyr-7b-beta-Q5_K_M",
    payload = {
        "model": "llama2-13b-chat-Q5_K_M", # Load the model
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



def join_headlines(headlines_df):
    
    # Concatenate the headlines
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    return headlines_text

def bullish(headlines_df):

    headlines_text = join_headlines(headlines_df)

    prompt_bullish = (
        "Dear Financial Assistant,\n\n"
        "Please analyze the following news headlines and provide a section titled 'Bullish Insights'. "
        "In this section, highlight any positive trends, growth areas, or market confidence factors based on the headlines. "
        "Keep this section around 50 words.\n\n"
        "Here are the headlines:\n"
        f"{headlines_text}\n\n"
        "Ensure the section is concise, actionable, and uses paragraph format."
    )

    bullish_summary = send_request(prompt_bullish)

    return bullish_summary

def bearish(headlines_df):

    headlines_text = join_headlines(headlines_df)

    prompt_bearish = (
        "Dear Financial Assistant,\n\n"
        "Please analyze the following news headlines and provide a section titled 'Bearish Insights'. "
        "In this section, highlight any negative trends or potential risks based on the headlines. "
        "Focus on brief, focused points that could impact the market in the short-term. Limit this section to about 50 words.\n\n"
        "Here are the headlines:\n"
        f"{headlines_text}\n\n"
        "Ensure the section is concise, actionable, and in uses paragraph format."
    )

    # Fetch bullish and bearish insights

    bearish_summary = send_request(prompt_bearish)

    return bearish_summary


def investment_insights(headlines_df):

    headlines_text = join_headlines(headlines_df)

    # prompt_investment = (
    #     "Dear Financial Assistant,\n\n"
    #     "Please analyze the following news headlines and provide a section titled 'Investment Insights'. "
    #     "In this section, offer insights on whether it might be a suitable time to invest based on both short-term and long-term indicators in the headlines. "
    #     "Consider any potential risks and growth areas, and keep this section focused and actionable.\n\n"
    #     "Here are the headlines:\n"
    #     f"{headlines_text}\n\n"
    #     "Ensure the section is concise, balanced, and uses bullet points."
    # )
    prompt_summary = (
        "Dear Financial Assistant,\n\n"
        "Please analyze the following news headlines and provide a section titled 'Investment Insights'. "
        "In this section, offer insights on whether it might be a suitable time to invest based on both short-term and long-term indicators in the headlines. "
        "Consider any potential risks and growth areas, and keep this section focused and actionable.\n\n"
        "Here are the headlines:\n"
        f"{headlines_text}\n\n"
        "Ensure the section is concise, balanced, and uses paragraph.")


    # Fetch bullish and bearish insights

    investment_insight = send_request(prompt_summary)

    return investment_insight


if _name_ == '_main_':

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Fetch the news
    headlines_df = news_fetcher.get_news("tesla", NEWS_API_KEY)
    print("Generating : ")
    bullish_summary = bullish(headlines_df)
    print(f"{bullish_summary}")
