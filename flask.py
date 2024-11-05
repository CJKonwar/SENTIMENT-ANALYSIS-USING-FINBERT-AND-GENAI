from src import sentiment_analysis
from src.vultr_llama import fundamental_llama_vultr
from src.vultr_llama import llama_analysis_vultr
import os
from dotenv import load_dotenv
import torch
from src.fundamental.fundamental_basic import get_all_stock_info as get_basic_info
from src.fundamental.fundamental_adv import get_all_stock_info as get_advanced_info
from src.vultr_llama import news_fetcher
from chatbot.model_RAG import chatbot_vultr
from flask import Flask, render_template, request, jsonify, send_file
from src.fundamental import fundamental_adv

from chatbot.model_RAG import get_response

load_dotenv(dotenv_path='.env')


app = Flask(__name__)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#for chatbot
@app.route('/chatbot', methods=['POST'])
def generate_response():
    user_query = request.form.get('user_query')

    if user_query:
        response = get_response(user_query)
        return jsonify({response})
    else:
        return jsonify({"Error generating response"}), 400


@app.route('/chatbot_result', methods=['POST'])
def chatbot():
    query = request.form.get('query')  # symbol to get from the user side

    if query:
        result = chatbot_vultr(query)
        return jsonify({result})
    else:
        return jsonify({"error": "Please provide a valid query."}), 400


# For getting basic stock info from fundamental basic file
@app.route('/basic_stock_info', methods=['POST'])
def basic_stock_info():
    symbol = request.form.get('symbol') # symbol to get from the user side
    
    if symbol:
        basic_info_df = get_basic_info(symbol)
        return jsonify(basic_info_df.to_dict(orient='records'))
    else:
        return jsonify({"error": "Please provide a valid stock symbol."}), 400


# For getting news from news fetcher
@app.route('/news', methods=['POST'])
def news():
    company_name = request.form.get('company_name') # name to get from the user side
    
    if company_name:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            return headlines_df.to_dict(orient='records')
        else:
            return jsonify({"error": "No news found or an error occurred while fetching the news."}), 404
    else:
        return jsonify({"error": "Please provide a valid company name."}), 400



#for sentiment analysis of news headlines using finbert
@app.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis_route():
    company_name = request.form.get('company_name')
    
    if company_name:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            sentiment_pipeline = sentiment_analysis.load_finbert_model(device)
            headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)
            return jsonify(headlines_with_sentiment.to_dict(orient='records'))
        else:
            return jsonify({"error": "No news found for sentiment analysis."}), 404
    else:
        return jsonify({"error": "Please provide a valid company name."}), 400

# for fetching fundamental stock info and generating insights
@app.route('/fundamentals_summary', methods=['POST'])
def fundamentals():
    symbol = request.form.get('symbol')
    
    if symbol:
        advanced_info = get_advanced_info(symbol)
        fundamental_summary = fundamental_llama_vultr.generate_summary_and_insights_from_fundamentals(advanced_info)
        return jsonify({fundamental_summary})
    else:
        return jsonify({"error": "Please provide a valid stock symbol."}), 400
@app.route('/bullish', methods=['POST'])
def bullish():
    company_name = request.form.get('company_name')

    if company_name:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            summary_and_insights = llama_analysis_vultr.bullish(headlines_df)
            return jsonify({summary_and_insights})
        else:
            return jsonify({"error": "No news available for generating insights."}), 404
    else:
        return jsonify({"error": "Please provide a valid company name."}), 400


@app.route('/bearish', methods=['POST'])
def bearish():
    company_name = request.form.get('company_name')

    if company_name:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            summary_and_insights = llama_analysis_vultr.bearish(headlines_df)
            return jsonify({summary_and_insights})
        else:
            return jsonify({"error": "No news available for generating insights."}), 404
    else:
        return jsonify({"error": "Please provide a valid company name."}), 400


@app.route('/investment_insight', methods=['POST'])
def insights():
    company_name = request.form.get('company_name')

    if company_name:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            summary_and_insights = llama_analysis_vultr.investment_insights(headlines_df)
            return jsonify({summary_and_insights})
        else:
            return jsonify({"error": "No news available for generating insights."}), 404
    else:
        return jsonify({"error": "Please provide a valid company name."}), 400

# Flask route to download the PDF
@app.route('/download-pdf')
def download_pdf():
    symbol = request.args.get('symbol')
    stock_info = fundamental_adv.get_all_stock_info(symbol)
    pdf_path = fundamental_adv.generate_pdf(symbol, stock_info)

    # Send the file as a download
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
