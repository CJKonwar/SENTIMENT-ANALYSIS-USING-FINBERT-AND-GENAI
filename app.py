import streamlit as st
import news_fetcher
import sentiment_analysis
import llama2_analysis  # Make sure this import is valid
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
        
        # Display the fetched news headlines
        st.dataframe(headlines_df)

        # Load FinBERT model
        sentiment_pipeline = sentiment_analysis.load_finbert_model()
        
        # Analyze sentiment
        st.write("Analyzing sentiment...")
        headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

        # Display the sentiment data
        st.write(headlines_with_sentiment)

        # Load Llama 2 model for summarization and insights
        st.write("Loading Llama 2 model for generating summary and insights...")
        llama_model, llama_tokenizer = llama2_analysis.load_llama2_model()
        
        # Generate summary and insights
        st.write("Generating summary and insights...")
        summary_and_insights = llama2_analysis.generate_summary_and_insights(headlines_df, llama_model, llama_tokenizer)

        # Display the summary and insights
        st.subheader("Summary and Investment Insights:")
        st.write(summary_and_insights)

    else:
        st.error("No news found or an error occurred while fetching the news.")
