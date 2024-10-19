from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd

# Load environment variables
load_dotenv()
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_flan_t5_model():
    model_name = "google/flan-t5-large"  # Using Flan-T5 large model
    hf_token = os.getenv("hf_token")  # Replace with your actual Hugging Face token

    # Load tokenizer and model with the token
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        use_auth_token=hf_token,
        device_map="auto",  # Automatically map to GPU if available
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32  # Use half precision on GPU
    )
    return model, tokenizer

def generate_summary_and_insights_from_fundamentals(stock_info, model, tokenizer):
    # Extract relevant sections of the stock information
    major_holders = stock_info.get('Major Holders', 'No data available')
    institutional_holders = stock_info.get('Institutional Holders', pd.DataFrame())
    mutual_fund_holders = stock_info.get('Mutual Fund Holders', pd.DataFrame())
    insider_transactions = stock_info.get('Insider Transactions', pd.DataFrame())
    insider_purchases = stock_info.get('Insider Purchases', {})
    upgrades_downgrades = stock_info.get('Upgrades/Downgrades', 'No data available')
    analyst_price_targets = stock_info.get('Analyst Price Targets', {})
    earnings_estimate = stock_info.get('Earnings Estimate', pd.DataFrame())
    revenue_estimate = stock_info.get('Revenue Estimate', pd.DataFrame())

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
        f"**Current Price Target:** ${analyst_price_targets.get('current', 'N/A')}\n"
        f"**Low Price Target:** ${analyst_price_targets.get('low', 'N/A')}\n"
        f"**High Price Target:** ${analyst_price_targets.get('high', 'N/A')}\n"
        f"**Mean Price Target:** ${analyst_price_targets.get('mean', 'N/A')}\n"
        f"**Median Price Target:** ${analyst_price_targets.get('median', 'N/A')}\n\n"

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

    # Create the pipeline for text2text-generation
    text_generator = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer
    )

    # Generate the summary and insights
    summary_and_insights = text_generator(
        prompt,
        max_length=1024,  # Adjust length as needed
        do_sample=True,
        truncation=True
    )[0]['generated_text']

    return summary_and_insights
