import streamlit as st
from src import sentiment_analysis
from src.vultr_llama import fundamental_llama_vultr
from src.vultr_llama import llama_analysis_vultr
import os
from dotenv import load_dotenv
import torch
from src.fundamental.fundamental_basic import get_all_stock_info as get_basic_info
from src.fundamental.fundamental_adv import get_all_stock_info as get_advanced_info
from src.vultr_llama import news_fetcher
#Loader for the .env file
load_dotenv(dotenv_path='.env')

# Set up the device for CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Streamlit interface
st.title("Company News, Stock Sentiment, and Fundamental Analysis")

# User inputs
company_name = st.text_input("Enter the company name:", "")
symbol = st.text_input("Enter the stock symbol:", "")

if company_name and symbol:
    st.write(f"Fetching top news for *{company_name}*...")


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
        st.write("Loading FinBERT model for sentiment analysis...")
        sentiment_pipeline = sentiment_analysis.load_finbert_model(device)

        # Analyze sentiment of the headlines
        st.write("Analyzing sentiment of news headlines...")
        headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

        # Display the sentiment data
        st.subheader("News Headlines with Sentiment Analysis:")
        st.dataframe(headlines_with_sentiment)

        # Fetch advanced stock info

        advanced_info = get_advanced_info(symbol)

        st.write("Generating summary and investment insights using Llama  (from news headlines)...")
        summary_and_insights = llama_analysis_vultr.generate_summary_and_insights(headlines_df)

        # Display summary and insights
        st.subheader("Summary and Investment Insights from News:")
        st.write(summary_and_insights)




        fundamental_summary = fundamental_llama_vultr.generate_summary_and_insights_from_fundamentals(advanced_info)

        st.subheader("Summary and Investment Insights from Fundamentals:")
        st.write(fundamental_summary)

        # Load FinBERT model for sentiment analysis at the end


    else:
        st.error("No news found or an error occurred while fetching the news.")
else:
    st.warning("Please enter both the company name and stock symbol.")