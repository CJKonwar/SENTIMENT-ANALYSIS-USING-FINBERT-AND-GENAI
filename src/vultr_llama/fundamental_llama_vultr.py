import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='../../.env')


def generate_summary_and_insights_from_fundamentals(stock_info):
    api_url = "https://api.vultrinference.com/v1/chat/completions"  # Example URL, change as needed
    api_key = os.getenv("VULTR_API")

    # Check if API keys are loaded correctly
    if api_key is None:
        print("Error: API keys are not loaded properly.")
        return

    major_holders = stock_info.get('Major Holders', 'No data available')
    institutional_holders = stock_info.get('Institutional Holders', 'No data available')
    mutual_fund_holders = stock_info.get('Mutual Fund Holders', 'No data available')
    insider_transactions = stock_info.get('Insider Transactions', 'No data available')
    insider_purchases = stock_info.get('Insider Purchases', 'No data available')
    upgrades_downgrades = stock_info.get('Upgrades/Downgrades', 'No data available')
    analyst_price_targets = stock_info.get('Analyst Price Targets', 'No data available')
    earnings_estimate = stock_info.get('Earnings Estimate', 'No data available')
    revenue_estimate = stock_info.get('Revenue Estimate', 'No data available')
    earnings_history = stock_info.get('Earnings History', 'No data available')

    # Formulate a prompt based on fundamental data
    prompt = (
            "Analyze the following stock's fundamental data and provide a structured summary along with investment insights:\n\n"

            "### Major Holders\n"
            f"{major_holders}\n\n"

            "### Institutional Holders\n"
            "| Date Reported | Holder                     | pctHeld | Shares     | Value         |\n"
            "|---------------|----------------------------|---------|------------|---------------|\n"
            + "\n".join([
        f"| {row['Date Reported']} | {row['Holder']} | {row['pctHeld']} | {row['Shares']} | {row['Value']} |"
        for index, row in institutional_holders.iterrows()
    ]) + "\n\n"

         "### Mutual Fund Holders\n"
         "| Date Reported | Holder                     | pctHeld | Shares     | Value         |\n"
         "|---------------|----------------------------|---------|------------|---------------|\n"
            + "\n".join([
        f"| {row['Date Reported']} | {row['Holder']} | {row['pctHeld']} | {row['Shares']} | {row['Value']} |"
        for index, row in mutual_fund_holders.iterrows()
    ]) + "\n\n"

         "### Insider Transactions\n"
         "| Shares   | Value           | URL | Text      | Insider | Position            | Transaction Start Date | Ownership |\n"
         "|----------|------------------|-----|-----------|---------|---------------------|------------------------|-----------|\n"
            + "\n".join([
        f"| {row['Shares']} | {row['Value']} | {row['URL']} | {row['Text']} | {row['Insider']} | {row['Position']} | {row.get('Transaction Start Date', 'N/A')} | {row['Ownership']} |"
        for index, row in insider_transactions.iterrows()
    ]) + "\n\n"

         "### Insider Purchases\n"
         "| Purchases | Sales | Net Shares Purchased (Sold) | Total Insider Shares Held | % Net Shares Purchased (Sold) | % Buy Shares | % Sell Shares |\n"
         "|-----------|-------|----------------------------|---------------------------|------------------------------|--------------|---------------|\n"
            + f"| {insider_purchases.get('Purchases', 'N/A')} | {insider_purchases.get('Sales', 'N/A')} | {insider_purchases.get('Net Shares Purchased (Sold)', 'N/A')} | {insider_purchases.get('Total Insider Shares Held', 'N/A')} | {insider_purchases.get('% Net Shares Purchased (Sold)', 'N/A')} | {insider_purchases.get('% Buy Shares', 'N/A')} | {insider_purchases.get('% Sell Shares', 'N/A')} |\n\n"

              "### Analyst Price Targets\n"
              f"**Current Price Target:** ${analyst_price_targets['current']}\n"
              f"**Low Price Target:** ${analyst_price_targets['low']}\n"
              f"**High Price Target:** ${analyst_price_targets['high']}\n"
              f"**Mean Price Target:** ${analyst_price_targets['mean']}\n"
              f"**Median Price Target:** ${analyst_price_targets['median']}\n\n"

              "### Earnings Estimate\n"
              "| Period | Number of Analysts | Avg EPS | Low EPS | High EPS | Year Ago EPS | Growth  |\n"
              "|--------|-------------------|---------|---------|----------|---------------|---------|\n"
            + "\n".join([
        f"| {period} | {row['numberOfAnalysts']} | {row['avg']} | {row['low']} | {row['high']} | {row['yearAgoEps']} | {row['growth']} |"
        for period, row in earnings_estimate.iterrows()
    ]) + "\n\n"

         "### Revenue Estimate\n"
         "| Period | Number of Analysts | Avg Revenue | Low Revenue | High Revenue | Year Ago Revenue | Growth  |\n"
         "|--------|-------------------|-------------|-------------|--------------|-------------------|---------|\n"
            + "\n".join([
        f"| {period} | {row['numberOfAnalysts']} | {row['avg']} | {row['low']} | {row['high']} | {row['yearAgoRevenue']} | {row['growth']} |"
        for period, row in revenue_estimate.iterrows()
    ]) + "\n\n"

    )

    payload = {
        "model": "llama2-13b-chat-Q5_K_M",  # Replace with the model name you want to use
        "messages": [
            {
                "role": "user",  # Set to user role with the prompt content
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "seed": -1,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.9,
        "stream": False  # Set to False if streaming is not supported
    }

    # Set the headers, including the authorization header with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  # Set content type to JSON
    }

    # Make the POST request to the API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Parse and print the generated response
        response_data = response.json()

        return response_data
    else:
        return f"Error {response.status_code}: {response.text}"





