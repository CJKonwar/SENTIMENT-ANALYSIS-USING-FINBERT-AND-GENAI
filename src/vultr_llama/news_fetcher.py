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
    url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&pageSize=50'  # Fetch extra articles
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get('articles', [])

        # Filter out articles that are missing 'title' or 'url' or contain "removed" in the URL
        valid_articles = [
            {'Headline': article['title'], 'URL': article['url']}
            for article in articles
            if article['title'] and article['url'] and 'removed' not in article['url']
        ]

        # Limit to 30 headlines if available
        limited_headlines = valid_articles[:30]

        return pd.DataFrame(limited_headlines)
    else:
        print(f"Error fetching news: {response.status_code}")
        return None
