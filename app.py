import streamlit as st
import news_fetcher
import sentiment_analysis
import llama2_analysis
import fundamental_llama  # Import the llamafundamental module
import os
from dotenv import load_dotenv
import torch
from fundamental_basic import get_all_stock_info as get_basic_info
from fundamental_adv import get_all_stock_info as get_advanced_info

# Load environment variables from .env file
load_dotenv()

# Set up the device for CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Streamlit interface
st.title("Company News, Stock Sentiment, and Fundamental Analysis")

# User inputs
company_name = st.text_input("Enter the company name:", "")
symbol = st.text_input("Enter the stock symbol:", "")

if company_name and symbol:
    st.write(f"Fetching top news for *{company_name}*...")

    # Fetch API key from .env file
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Fetch the news
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

    if headlines_df is not None and not headlines_df.empty:
        st.success("News Headlines fetched successfully!")

        # Display the fetched news headlines
        st.subheader(f"Top News Headlines for {company_name}:")
        st.dataframe(headlines_df)

        # Fetch basic stock info
        st.write(f"Fetching basic stock info for *{symbol}*...")
        basic_info_df = get_basic_info(symbol)
        st.subheader("Basic Stock Information:")
        st.dataframe(basic_info_df)

        # Fetch advanced stock info

        advanced_info = get_advanced_info(symbol)



        # Load Llama 2 model for summarization and insights
        st.write("Loading Llama 2 model for summarization and insights...")
        llama_model, llama_tokenizer = llama2_analysis.load_llama2_model(device)
        # Load Llama 2 model for summarization and insights based on stock fundamentals
        st.write("Generating summary and investment insights using Llama 2 (from fundamental stock data)...")
        fundamental_summary = fundamental_llama.generate_summary_and_insights_from_fundamentals(advanced_info,
                                                                                                llama_model,
                                                                                                llama_tokenizer)

        # Display summary and insights from fundamental data
        st.subheader("Summary and Investment Insights from Fundamentals:")
        st.write(fundamental_summary)
        # Generate summary and insights using Llama 2 based on news headlines
        st.write("Generating summary and investment insights using Llama 2 (from news headlines)...")
        summary_and_insights = llama2_analysis.generate_summary_and_insights(headlines_df, llama_model, llama_tokenizer)

        # Display summary and insights
        st.subheader("Summary and Investment Insights from News:")
        st.write(summary_and_insights)



        # Load FinBERT model for sentiment analysis at the end
        st.write("Loading FinBERT model for sentiment analysis...")
        sentiment_pipeline = sentiment_analysis.load_finbert_model(device)

        # Analyze sentiment of the headlines
        st.write("Analyzing sentiment of news headlines...")
        headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

        # Display the sentiment data
        st.subheader("News Headlines with Sentiment Analysis:")
        st.dataframe(headlines_with_sentiment)

    else:
        st.error("No news found or an error occurred while fetching the news.")
else:
    st.warning("Please enter both the company name and stock symbol.")
