from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import pandas as pd
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_finbert_model(device):
    model_name = "yiyanghkust/finbert-tone"
    tokenizer = BertTokenizer.from_pretrained(model_name)

    # Load the model to CUDA if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = BertForSequenceClassification.from_pretrained(model_name).to(device)

    # Load the sentiment analysis pipeline and specify the device
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

    return nlp


def analyze_sentiment(headlines_df, sentiment_pipeline):
    sentiments = []
    for headline in headlines_df['title']:
        sentiment = sentiment_pipeline(headline)[0]
        sentiments.append(sentiment)

    # Adding sentiment information to the DataFrame
    # print(sentiments)
    headlines_df['sentiment'] = [sentiment['label'] for sentiment in sentiments]
    headlines_df['confidence'] = [sentiment['score'] for sentiment in sentiments]
    return headlines_df