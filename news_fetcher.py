import requests
import pandas as pd

def get_news(company_name, api_key, top_n=100):
    # URL for News API
    url = f'https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&apiKey={api_key}'
    
    # Making the request
    response = requests.get(url)
    news_data = response.json()

    # Check if the request was successful
    if news_data['status'] != 'ok':
        print("Error fetching news!")
        return None
    
    # Get the top 'n' news articles
    articles = news_data['articles'][:top_n]
    
    # Create a DataFrame for better readability
    headlines = [(article['title'], article['url']) for article in articles]
    df = pd.DataFrame(headlines, columns=['Headline', 'URL'])
    
    return df
