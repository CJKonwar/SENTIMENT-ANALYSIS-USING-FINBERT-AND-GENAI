from transformers import BertTokenizer, BertForSequenceClassification, pipeline

def load_finbert_model():
    # Load pre-trained FinBERT model and tokenizer
    model_name = "yiyanghkust/finbert-tone"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    # Load the sentiment analysis pipeline
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    return nlp

def analyze_sentiment(headlines_df, sentiment_pipeline):
    sentiments = []
    for headline in headlines_df['Headline']:
        sentiment = sentiment_pipeline(headline)[0]  # FinBERT returns a dictionary with label and score
        sentiments.append(sentiment)

    # Add sentiment information to the DataFrame
    headlines_df['Sentiment'] = [sentiment['label'] for sentiment in sentiments]
    headlines_df['Confidence'] = [sentiment['score'] for sentiment in sentiments]
    
    return headlines_df
