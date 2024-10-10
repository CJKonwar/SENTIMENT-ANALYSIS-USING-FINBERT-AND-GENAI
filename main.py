import os
from dotenv import load_dotenv
import news_fetcher
import sentiment_analysis
import llama2_analysis
import torch

# Load environment variables from .env file
load_dotenv()

# Fetch API key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def main(company_name):
    # Step 1: Fetch the top headlines for the company
    print(f"Fetching top news headlines for {company_name}...")
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)
    
    if headlines_df is None or headlines_df.empty:
        print("No news found.")
        return

    # Step 2: Load FinBERT model for sentiment analysis (with CUDA if available)
    print("Loading FinBERT model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sentiment_pipeline = sentiment_analysis.load_finbert_model(device=device)

    # Step 3: Analyze sentiment of the headlines
    print("Analyzing sentiment of news headlines...")
    headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)
    
    # Step 4: Load Llama 2 model for summarization and insights (with CUDA support)
    print("Loading Llama 2 model for summarization and insights...")
    llama_model, llama_tokenizer = llama2_analysis.load_llama2_model(device)

    # Check for CUDA availability and set the appropriate device
    if torch.cuda.is_available():
        llama_model = llama_model.to("cuda")
        print("Llama 2 model is using CUDA.")
    else:
        print("CUDA not available. Llama 2 model is using CPU.")
    
    print("Generating summary and insights using Llama 2...")
    llama_summary_and_insights = llama2_analysis.generate_summary_and_insights(headlines_df, llama_model, llama_tokenizer)
    
    # Step 5: Display results
    print("\nTop 10 News Headlines with Sentiment:")
    print(headlines_with_sentiment)
    
    print("\nSummary and Insights:")
    print(llama_summary_and_insights)

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    main(company_name)
