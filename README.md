![WhatsApp Image 2024-11-08 at 14 02 53_b5584ccb](https://github.com/user-attachments/assets/bb5e3bb0-3847-4155-8edb-9212a65c73fc)

#Website link: https://sentifyai.tech/

# SentifyAI: A Functional Platform for Financial News Classification and Sentiment Analysis

**SentifyAI** is a comprehensive platform that classifies financial news articles, performs sentiment analysis, and provides real-time investment insights. The platform integrates machine learning models with a user-friendly interface, offering essential financial data, sentiment classifications, and visual market trends for investors and financial analysts.

## Key Features

- **User-Friendly Interface**: Enter a company name, and SentifyAI fetches the corresponding stock symbol and provides:
  - Investment insights, including major and institutional holders
  - Analysts' target prices and recent news headlines with sentiment classifications
  - An embedded TradingView chart for stock performance visualization

- **Classification Engine**: Utilizes FinBert, a financial-specific NLP model, to classify news sentiment (positive, negative, or neutral) for targeted and accurate analysis.

- **Sentiment Analysis Module**: Powered by the Llama2 13B model, deployed on Vultr’s serverless inference infrastructure, this module summarizes news articles and provides in-depth market insights.

- **Real-Time Processing**: News articles and financial data are processed in real-time, keeping insights current and reliable.

- **Data Visualization**: Sentiment trends, classification results, and TradingView charts are displayed through dynamic dashboards for an enhanced user experience.

## Technical Overview

### System Architecture

The platform architecture is designed for efficiency and scalability, integrating a real-time backend and an intuitive frontend.

- **Frontend (Svelte)**: A dynamic, responsive interface that allows users to search by company name and view organized financial insights.

- **Backend (Flask and Socket.IO)**: Handles data processing, API requests, and real-time data updates using Socket.IO to provide users with up-to-date insights.

- **Company Symbol Database**: Maps company names to stock symbols via a pre-integrated database on Vultr, making searches fast and user-friendly.

- **News and Financial Data Retrieval**:
  - **NewsAPI**: Fetches relevant news articles for sentiment analysis.
  - **yFinance**: Provides fundamental stock data, including information on holders and financial ratios.

- **Sentiment Analysis and Summarization**:
  - **FinBert**: Classifies news sentiment as positive, negative, or neutral.
  - **Llama2 13B Model**: Deployed on Vultr, provides summaries and investment insights from news and financial data.

### Deployment and Infrastructure

SentifyAI is hosted on Vultr Cloud Compute, optimized for scalability, security, and performance:

- **DNS Management and Firewall**: Vultr DNS and firewall configurations ensure secure, reliable data access and content delivery.
- **Load Balancer**: Distributes traffic across servers, maintaining platform stability during peak loads.
- **Pull and Push Zones**:
  - **Pull Zone**: Caches content for faster access.
  - **Push Zone**: Ensures fresh data distribution for real-time updates.

### Key Modules

- **yFinance**: Retrieves advanced stock data, providing insights into financial performance and ratios.
- **FinBert**: Customizes sentiment classification for financial news, providing relevant sentiment data to users.
- **Llama2 13B Model**: Processes news to generate summaries and market insights through Vultr’s serverless infrastructure.

## API Documentation

### NewsAPI Integration

SentifyAI uses [NewsAPI](https://newsapi.org/) to pull real-time financial news from a range of reputable sources. The "Top Headlines" endpoint allows for targeted searches by company name, keyword, and other filters, providing timely news content for sentiment analysis. For detailed usage and authentication guidelines, refer to the [NewsAPI documentation](https://newsapi.org/docs).

---




# SentifyAI

SentifyAI is a sentiment analysis platform that provides insights into company news, stock sentiment, and fundamental analysis.

## Setup and Usage Instructions

### Prerequisites
Ensure you have the following installed:
- **Python** (3.7 or higher)
- **pip** (Python package installer)
- **Node.js** and **npm** (Node Package Manager)

### Step 1: Clone the Repository
Clone the SentifyAI GitHub repository to your local machine. Open a terminal or command prompt and run:
```bash
git clone https://github.com/CJKonwar/SentifyAI.git
```


### Step 2: Install Python Requirements
Navigate to the project folder and install the required Python dependencies:

1. Move to the SentifyAI folder:
    ```bash
    cd SentifyAI
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Set Up Environment Variables
Create a `.env` file in the `backend` folder with all the required API keys and other configurations. Refer to the repository’s documentation or README for the specific variables needed.
## Environment Variables

To set up the environment for this project, add the following variables to a `.env` file in the `backend` folder. Each variable is described below:

```env
# API key for accessing the News API to fetch financial news and data for the application.
NEWS_API_KEY=your_news_api_key_here

# Hugging Face API token for accessing NLP models or datasets from Hugging Face.
hf_token=your_hugging_face_token_here

# API key for interacting with Vultr cloud services.
VULTR_API=your_vultr_api_key_here

# PostgreSQL database connection URL, which provides access to the application’s primary database.
DATABASE_URL=your_database_url_here
```

### Step 4: Run the Backend
1. Move to the backend folder:
    ```bash
    cd backend
    ```

2. Start the backend server:
   
  For Windows:
  
  ```bash
    python app.py
  ```
  

For Mac/Unix:
  ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

  ```

### Step 5: Set Up and Run the Frontend
1. Navigate back to the main directory:
    ```bash
    cd ..
    ```

2. Move to the frontend folder:
    ```bash
    cd frontend
    ```

3. Install the necessary Node.js dependencies:
    ```bash
    npm install
    ```

4. Start the frontend development server:
    ```bash
    npm run dev
    ```

### Step 6: Set Up the PHP server for chatbot
1. Install PHP and Composer and other laravel dependencies
2. Create the chatbot folder
   ```bash
   composer create-project laravel/laravel chatbot

   ```
3. Copy the files present in chatbot-app folder into chatbot folder
4. Run the following
```bash
cd chatbot
composer require guzzlehttp/guzzle
```
5. Run the PHP server
```bash
php artisan serve
```
   
The website should now be accessible on your local server. Check the terminal output for the exact URL (typically `http://localhost:5173`).

## Usage Instructions
- **Select a Company**: Once the website is running, go to the top search bar and click on "Select Company." This will display a list of all S&P 500 companies. Choose a company to analyze.
  
- **Chatbot Assistance**: Use the chatbot located in the bottom right corner to ask any finance or stock market-related questions. The chatbot can provide insights and help with your analysis.

## Images of our website
![WhatsApp Image 2024-11-08 at 14 02 53_1607ed97](https://github.com/user-attachments/assets/fad8ef18-77fd-4ae7-a472-982efbba170c)

![WhatsApp Image 2024-11-08 at 14 02 53_01d26f0b](https://github.com/user-attachments/assets/d83756ed-aa4c-420d-958b-07cca2ed9d7b)

![WhatsApp Image 2024-11-08 at 14 02 53_dc6b9ff6](https://github.com/user-attachments/assets/c125ded0-42b3-4a0b-880e-f4f4a7f28493)

<img width="1470" alt="Screenshot 2024-11-12 at 11 22 45 PM" src="https://github.com/user-attachments/assets/5683a6a7-4b55-497d-948a-4176fe696a73">

<img width="1470" alt="Screenshot 2024-11-12 at 11 23 11 PM" src="https://github.com/user-attachments/assets/df8b2cb4-d3b2-42bd-9ee1-3f5dfe5e9a22">








