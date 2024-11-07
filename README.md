SentifyAI: A Functional Platform for Financial News Classification and Sentiment Analysis
SentifyAI is a comprehensive platform that classifies financial news articles, performs sentiment analysis, and provides real-time investment insights. The platform integrates machine learning models with a user-friendly interface, providing essential financial data, sentiment classifications, and visual market trends for investors and financial analysts.

Key Features
User-Friendly Interface: Enter a company name, and SentifyAI fetches the corresponding stock symbol and provides:

Investment insights, including major and institutional holders
Analysts' target prices and recent news headlines with sentiment classifications
An embedded TradingView chart for stock performance visualization
Classification Engine: Utilizes FinBert, a financial-specific NLP model, to classify news sentiment (positive, negative, or neutral) for targeted and accurate analysis.

Sentiment Analysis Module: Powered by the Llama2 13B model, deployed on Vultr’s serverless inference infrastructure, this module summarizes news articles and provides in-depth market insights.

Real-Time Processing: News articles and financial data are processed in real-time, keeping insights current and reliable.

Data Visualization: Sentiment trends, classification results, and TradingView charts are displayed through dynamic dashboards for enhanced user experience.

Technical Overview
System Architecture
The platform architecture is designed for efficiency and scalability, integrating a real-time backend and an intuitive frontend.

Frontend (Svelte): A dynamic, responsive interface that allows users to search by company name and view organized financial insights.
Backend (Flask and Socket.IO): Handles data processing, API requests, and real-time data updates using Socket.IO to provide users with up-to-date insights.
Company Symbol Database: Maps company names to stock symbols via a pre-integrated database on Vultr, making searches fast and user-friendly.
News and Financial Data Retrieval:
NewsAPI: Fetches relevant news articles for sentiment analysis.
yFinance: Provides fundamental stock data, including information on holders and financial ratios.
Sentiment Analysis and Summarization:
FinBert: Classifies news sentiment as positive, negative, or neutral.
Llama2 13B Model: Deployed on Vultr, provides summaries and investment insights from news and financial data.
Deployment and Infrastructure
SentifyAI is hosted on Vultr Cloud Compute, optimized for scalability, security, and performance:

DNS Management and Firewall: Vultr DNS and firewall configurations ensure secure, reliable data access and content delivery.
Load Balancer: Distributes traffic across servers, maintaining platform stability during peak loads.
Pull and Push Zones:
Pull Zone: Caches content for faster access.
Push Zone: Ensures fresh data distribution for real-time updates.
Key Modules
yFinance: Retrieves advanced stock data, providing insights into financial performance and ratios.
FinBert: Customizes sentiment classification for financial news, providing relevant sentiment data to users.
Llama2 13B Model: Processes news to generate summaries and market insights through Vultr’s serverless infrastructure.
API Documentation
NewsAPI Integration
SentifyAI uses NewsAPI to pull real-time financial news from a range of reputable sources. The "Top Headlines" endpoint allows for targeted searches by company name, keyword, and other filters, providing timely news content for sentiment analysis. For detailed usage and authentication guidelines, refer to the NewsAPI documentation.
