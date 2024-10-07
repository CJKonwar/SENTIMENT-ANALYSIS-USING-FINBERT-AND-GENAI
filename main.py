import os
from dotenv import load_dotenv
import news_fetcher
import sentiment_analysis

# Load environment variables from .env file
load_dotenv()

# Fetch API key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def main(company_name):
    # Step 1: Fetch the top 10 headlines for the company
    print(f"Fetching top news headlines for {company_name}...")
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)
    
    if headlines_df is None or headlines_df.empty:
        print("No news found.")
        return

    # Step 2: Load FinBERT model for sentiment analysis
    print("Loading FinBERT model...")
    sentiment_pipeline = sentiment_analysis.load_finbert_model()

    # Step 3: Analyze sentiment of the headlines
    print("Analyzing sentiment of news headlines...")
    headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)
    
    # Step 4: Display results
    print("\nTop 10 News Headlines with Sentiment:")
    print(headlines_with_sentiment)

    # Optionally, save the results to a CSV file
    headlines_with_sentiment.to_csv(f'{company_name}_news_sentiment.csv', index=False)
    print(f"Results saved to {company_name}_news_sentiment.csv")

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    main(company_name)
