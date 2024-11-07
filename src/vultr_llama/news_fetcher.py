import requests
import pandas as pd
from typing import *

def get_news(company_name: str, api_key: str) -> Optional[Tuple[pd.DataFrame, List]]:
    """
    Fetches news headlines for the given company using the News API.

    Args:
        company_name (str): The name of the company to fetch news for.
        api_key (str): The API key for accessing the News API.

    Returns:
        Optional[Tuple[pd.DataFrame, List]]: A tuple containing:
            - A pandas DataFrame with news headlines, URLs, and image links.
            - Returns None if the API request fails.
    """
    url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&pageSize=50'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        return None

    articles = response.json().get('articles', [])
    valid_articles = []
    for article in articles:
        if article['title'] and article['url'] and 'removed' not in article['url']:
            valid_articles.append({
                'title': article['title'],
                'url': article['url'],
                'urlToImg': article.get('urlToImage', ''),
                'publishedAt': article['publishedAt']
            })

    # Sort by published date and limit to the top 30 articles
    valid_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
    limited_headlines = valid_articles[:30]

    # Return as DataFrame and list of valid articles
    return pd.DataFrame(limited_headlines)