import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='../../.env')

#Function to generate insights from stock info 
def generate_summary_and_insights_from_fundamentals(stock_info):
    # Load the url 
    api_url = "https://api.vultrinference.com/v1/chat/completions"  
    api_key = os.getenv("VULTR_API")

    # Check if API keys are loaded correctly
    if api_key is None:
        print("Error: API keys are not loaded properly.")
        return

    # Extracting major holders, institutional, mutual fund, insider transactions, and earnings/revenue estimates
    major_holders = stock_info.get('Major Holders', 'No data available')
    institutional_holders = stock_info.get('Institutional Holders', 'No data available')
    mutual_fund_holders = stock_info.get('Mutual Fund Holders', 'No data available')
    insider_transactions = stock_info.get('Insider Transactions', 'No data available')
    insider_purchases = stock_info.get('Insider Purchases', 'No data available')
    analyst_price_targets = stock_info.get('Analyst Price Targets', 'No data available')
    earnings_estimate = stock_info.get('Earnings Estimate', 'No data available')
    revenue_estimate = stock_info.get('Revenue Estimate', 'No data available')

    # The Prompt
    prompt = (
            "Analyze the following stock's fundamental data and provide a summary:\n\n"

            f"### Major Holders\n{major_holders}\n\n"

            f"### Institutional Holders (Top 10)\n"
            + "\n".join([
        f"- {row['Holder']}: {row['pctHeld']} of shares held."
        for index, row in institutional_holders.head(10).iterrows()
    ]) + "\n\n"

         f"### Mutual Fund Holders (Top 10)\n"
            + "\n".join([
        f"- {row['Holder']}: {row['pctHeld']} of shares held."
        for index, row in mutual_fund_holders.head(10).iterrows()
    ]) + "\n\n"

         f"### Insider Transactions\n{insider_transactions.head(3).to_string(index=False)}\n\n"

         f"### Insider Purchases\n"
         f"- Purchases: {insider_purchases.get('Purchases', 'N/A')}\n"
         f"- Sales: {insider_purchases.get('Sales', 'N/A')}\n\n"

         f"### Analyst Price Targets\n"
         f"Current Price Target: ${analyst_price_targets['current']}\n"
         f"Mean Price Target: ${analyst_price_targets['mean']}\n\n"

         f"### Earnings Estimate (Next Quarter)\n"
            + f"- Average EPS: {earnings_estimate['avg'].iloc[0]}\n"
            + f"- Growth: {earnings_estimate['growth'].iloc[0]}\n\n"

              f"### Revenue Estimate (Next Quarter)\n"
            + f"- Average Revenue: {revenue_estimate['avg'].iloc[0]}\n"
            + f"- Growth: {revenue_estimate['growth'].iloc[0]}\n"
    )

    # Load the model
    payload = {
        "model": "llama2-13b-chat-Q5_K_M",  
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "seed": -1,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.9,
        "stream": False  # Set to False if streaming is not supported
    }

    # Loading the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  
    }

    # Make the request to the API
    response = requests.post(api_url, headers=headers, json=payload)

    # Parse and print the generated response
    if response.status_code == 200:
        response_data = response.json()
        summary = response_data['choices'][0]['message']['content']
        return summary
    else:
        return f"Error {response.status_code}: {response.text}"
