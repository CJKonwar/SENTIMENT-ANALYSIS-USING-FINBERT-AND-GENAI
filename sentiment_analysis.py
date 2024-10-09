from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import pandas as pd
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
def load_finbert_model(device):
    """
    Load the FinBERT model and tokenizer for sentiment analysis.
    If a GPU is available, it will load the model on the GPU.
    
    Returns:
    - sentiment-analysis pipeline
    """
    model_name = "yiyanghkust/finbert-tone"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    
    # Load the model to CUDA if available, otherwise fallback to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"  # 0 is for CUDA device, -1 for CPU
    model = BertForSequenceClassification.from_pretrained(model_name).to(device)
    
    # Load the sentiment analysis pipeline and specify the device
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)
    
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
