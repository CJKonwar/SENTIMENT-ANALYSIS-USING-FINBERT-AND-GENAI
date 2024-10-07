import streamlit as st
import pandas as pd
import news_fetcher
import sentiment_analysis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Streamlit interface
st.title("Company News Sentiment Analyzer")

company_name = st.text_input("Enter the company name:", "")

if company_name:
    st.write(f"Fetching top news for **{company_name}**...")

    # Fetch the news
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)
    
    if headlines_df is not None and not headlines_df.empty:
        st.write("News Headlines fetched successfully!")
        
        # Load FinBERT model
        sentiment_pipeline = sentiment_analysis.load_finbert_model()
        
        # Analyze sentiment
        st.write("Analyzing sentiment...")
        headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

        # Display the sentiment data
        st.write(headlines_with_sentiment)

        # Downloadable CSV
        csv = headlines_with_sentiment.to_csv(index=False)
        st.download_button("Download Sentiment Data as CSV", csv, f"{company_name}_news_sentiment.csv")
    else:
        st.error("No news found or an error occurred while fetching the news.")
