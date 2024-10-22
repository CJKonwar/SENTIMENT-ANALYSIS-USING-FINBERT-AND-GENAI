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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load the .env file to access sensitive information like API keys and database URLs
load_dotenv(dotenv_path='.env')

# Set up the device for CUDA if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Database connection setup using SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch company names and stock symbols from the Vultr database
def get_company_symbols():
    with engine.connect() as connection:
        result = connection.execute("SELECT company_name, stock_symbol FROM companies")
        company_symbols = result.fetchall()
    return company_symbols

# Streamlit app UI
st.title("Company News, Stock Sentiment, and Fundamental Analysis")

# Fetch all company names and stock symbols from the Vultr database
company_symbols = get_company_symbols()

# Create a dictionary to map company names to their stock symbols
company_dict = {row[0]: row[1] for row in company_symbols}
company_list = list(company_dict.keys())

# User selects the company name from a dropdown list
company_name = st.selectbox("Select the company name:", company_list)

# Autofill the stock symbol based on the selected company name
symbol = ""
if company_name:
    symbol = company_dict.get(company_name, "")
    st.text_input("Stock symbol:", value=symbol)

# Once both company name and symbol are provided, start fetching news and stock info
if company_name and symbol:
    st.write(f"Fetching top news for *{company_name}*...")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Fetch the news using the provided company name and the API key from the .env file
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

    if headlines_df is not None and not headlines_df.empty:
        st.success("News Headlines fetched successfully!")

        # Display the fetched news headlines
        st.subheader(f"Top News Headlines for {company_name}:")
        st.dataframe(headlines_df)

        # Fetch basic stock information based on the stock symbol
        st.write(f"Fetching basic stock info for *{symbol}*...")
        basic_info_df = get_basic_info(symbol)
        st.subheader("Basic Stock Information:")
        st.dataframe(basic_info_df)

        # Load the FinBERT model for sentiment analysis
        st.write("Loading FinBERT model for sentiment analysis...")
        sentiment_pipeline = sentiment_analysis.load_finbert_model(device)

        # Analyze sentiment of the fetched news headlines
        st.write("Analyzing sentiment of news headlines...")
        headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

        # Display the news headlines along with the sentiment analysis
        st.subheader("News Headlines with Sentiment Analysis:")
        st.dataframe(headlines_with_sentiment)

        # Fetch advanced stock information based on the stock symbol
        advanced_info = get_advanced_info(symbol)

        # Generate summary and investment insights based on the news headlines
        st.write("Generating summary and investment insights (from news headlines)...")
        summary_and_insights = llama_analysis_vultr.generate_summary_and_insights(headlines_df)

        # Display the summary and investment insights from news headlines
        st.subheader("Summary and Investment Insights from News:")
        st.write(summary_and_insights)

        # Generate a fundamental summary from the fundamental data
        st.write("Generating fundamental summary (from fundamental data)...")
        fundamental_summary = fundamental_llama_vultr.generate_summary_and_insights_from_fundamentals(advanced_info)

        # Display the summary and investment insights from the fundamental data
        st.subheader("Summary and Investment Insights from Fundamentals:")
        st.write(fundamental_summary)

    else:
        st.error("No news found or an error occurred while fetching the news.")
else:
    st.warning("Please enter both the company name and stock symbol.")
