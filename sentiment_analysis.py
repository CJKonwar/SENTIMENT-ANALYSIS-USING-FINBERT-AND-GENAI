from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import pandas as pd
import torch

def load_finbert_model():
    """
    Load the FinBERT model and tokenizer for sentiment analysis.
    
    Returns:
    - sentiment-analysis pipeline
    """
    model_name = "yiyanghkust/finbert-tone"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    
    # Load the sentiment analysis pipeline
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp

def analyze_sentiment(headlines_df, sentiment_pipeline):
    """
    Analyze sentiment of headlines using the sentiment pipeline.
    
    Args:
    - headlines_df (pandas.DataFrame): DataFrame containing news headlines.
    - sentiment_pipeline: Pre-loaded sentiment analysis pipeline.
    
    Returns:
    - pandas.DataFrame: DataFrame with added sentiment and confidence columns.
    """
    sentiments = []
    for headline in headlines_df['Headline']:
        sentiment = sentiment_pipeline(headline)[0]  # FinBERT returns a dictionary with label and score
        sentiments.append(sentiment)

    # Add sentiment information to the DataFrame
    headlines_df['Sentiment'] = [sentiment['label'] for sentiment in sentiments]
    headlines_df['Confidence'] = [sentiment['score'] for sentiment in sentiments]
    
    return headlines_df
