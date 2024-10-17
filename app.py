from flask import Flask, render_template, request, redirect, url_for
from src import sentiment_analysis, news_fetcher
from src.llama_analysis import fundamental_llama, llama2_analysis
import os
from dotenv import load_dotenv
import torch
from src.fundamental.fundamental_basic import get_all_stock_info as get_basic_info
from src.fundamental.fundamental_adv import get_all_stock_info as get_advanced_info

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv('.env')
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Set up the device for CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company_name']
        symbol = request.form['symbol']
        return redirect(url_for('results', company_name=company_name, symbol=symbol))
    return render_template('index.html')

@app.route('/results')
def results():
    company_name = request.args.get('company_name')
    symbol = request.args.get('symbol')
    print(device)

    # Fetch news headlines
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)
    if headlines_df is None or headlines_df.empty:
        return render_template('results.html', error="No news found for this company.")

    # Fetch basic stock info
    basic_info_df = get_basic_info(symbol)

    # Fetch advanced stock info
    advanced_info = get_advanced_info(symbol)

    # Load Llama 2 model for summarization and insights
    llama_model, llama_tokenizer = llama2_analysis.load_llama2_model(device)
    fundamental_summary = fundamental_llama.generate_summary_and_insights_from_fundamentals(
        advanced_info, llama_model, llama_tokenizer)
    summary_and_insights = llama2_analysis.generate_summary_and_insights(
        headlines_df, llama_model, llama_tokenizer)

    # Load FinBERT model for sentiment analysis
    sentiment_pipeline = sentiment_analysis.load_finbert_model(device)
    headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)
    
    # Render the results template
    return render_template('results.html',
                           company_name=company_name,
                           basic_info=basic_info_df,
                           advanced_info=advanced_info,
                           headlines=headlines_df,
                           fundamental_summary=fundamental_summary,
                           summary_and_insights=summary_and_insights,
                           headlines_with_sentiment=headlines_with_sentiment,
                           )

if __name__ == '__main__':
    app.run(debug=True)
