from src import sentiment_analysis
from src.vultr_llama import fundamental_llama_vultr, llama_analysis_vultr, news_fetcher
from src.fundamental.fundamental_basic import get_all_stock_info as get_basic_info
from src.fundamental.fundamental_adv import get_all_stock_info as get_advanced_info, generate_pdf
from src.chatbot.model_RAG import get_response, get_response1

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import psycopg2, os, torch


app = Flask(__name__)
# frontend.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Load environment variables
load_dotenv()

# Set up device for CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Database connection details
DB_URL = os.getenv("DATABASE_URL")

# Allow CORS for all routes
CORS(app)

# Fetch all companies and their stock symbols from the database
@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Execute the query to fetch companies
        cur.execute('SELECT "company_name", "stock_symbol" FROM "COMPANY"')
        data = cur.fetchall()
        
        data = [{"company_name": row[0], "stock_symbol": row[1]} for row in data]

        # Close cursor and connection
        cur.close()
        conn.close()
        
        # Return data as JSON
        return jsonify(data)
        
    except Exception as e:
        # If an error occurs, print it and return an error message
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Failed to fetch companies"}), 500

# Chat bot route
@app.route('/api/chatbot', methods=['POST'])
def generate_response():
    user_query = request.json.get('query')

    if user_query:
        response = get_response(user_query)
        # response = get_response(user_query)
        print(response)
        return jsonify({"reply": response})
    else:
        return jsonify({"Error generating response"}), 400

# download adv fundamentals pdf
@app.route('/api/download-pdf')
def download_pdf():
    symbol = request.args.get('symbol')
    stock_info = get_advanced_info(symbol)
    pdf_path = generate_pdf(symbol, stock_info)

    # Send the file as a download
    return send_file(pdf_path, as_attachment=True)

@socketio.on('fetch_data')
def handle_fetch_data(data):
    company_name = data.get('company_name')
    symbol = data.get('symbol')

    if not company_name or not symbol:
        emit('error', {'message': 'Please provide both company name and stock symbol.'})
        return

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Fetch news headlines and perform sentiment analysis
    try:
        headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)

        if headlines_df is not None and not headlines_df.empty:
            sentiment_pipeline = sentiment_analysis.load_finbert_model(device)
            headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)
            emit('news', {'message': 'Sentiment Analysis of News Headlines', 'data': headlines_with_sentiment.to_dict(orient="records")})
        else:
            emit('error', {'message': 'No news found for the given company name.'})
            return
    except Exception as e:
        emit('error', {'message': f'Error fetching news: {str(e)}'})
        return

    # Fetch basic stock information
    try:
        basic_info_df = get_basic_info(symbol)
        emit('basic_info', {'message': 'Basic Stock Information', 'data': basic_info_df.to_dict(orient="records")})
    except Exception as e:
        emit('error', {'message': f'Error fetching basic stock info: {str(e)}'})
        return

    # Advanced stock information
    try:
        advanced_info = get_advanced_info(symbol)
    except Exception as e:
        emit('error', {'message': f'Error fetching advanced stock info: {str(e)}'})
        return

    # Bullish View
    try:
        bullishView = llama_analysis_vultr.bullish(headlines_df)
        emit('bullish', {'message': 'Bullish View', 'data': bullishView})
    except Exception as e:
        emit('error', {'message': f'Error generating bullish view: {str(e)}'})
        return
    
    # Bearish View
    try:
        bearishView = llama_analysis_vultr.bearish(headlines_df)
        emit('bearish', {'message': 'Bearish View', 'data': bearishView})
    except Exception as e:
        emit('error', {'message': f'Error generating bearish view: {str(e)}'})
        return
    
    # Generate investment insights
    try:
        summary_and_insights = llama_analysis_vultr.investment_insights(headlines_df)
        emit('investment_insights', {'message': 'Investment Insights from News', 'data': summary_and_insights})
    except Exception as e:
        emit('error', {'message': f'Error generating news insights: {str(e)}'})
        return

    # Generate fundamental insights
    try:
        fundamental_summary = fundamental_llama_vultr.generate_summary_and_insights_from_fundamentals(advanced_info)
        emit('fundamental_summary', {'message': 'Fundamental Analysis Summary', 'data': fundamental_summary})
    except Exception as e:
        emit('error', {'message': f'Error generating fundamental insights: {str(e)}'})
        return

if __name__ == '__main__':
    socketio.run(app, debug=True)
