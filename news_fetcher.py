import requests
import pandas as pd

def get_news(company_name, api_key):
    """
    Fetches news headlines for the given company using the News API.
    
    Args:
        company_name (str): The name of the company to fetch news for.
        api_key (str): The API key for accessing the News API.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the news headlines and URLs.
    """
    url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&pageSize=30'
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        headlines = [{'Headline': article['title'], 'URL': article['url']} for article in articles]
        return pd.DataFrame(headlines)
    else:
        print(f"Error fetching news: {response.status_code}")
        return None
