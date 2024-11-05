from flask import Flask, send_file, request
import yfinance as yf
from fpdf import FPDF
import pandas as pd
import os


# Function to fetch stock information using yfinance
def get_all_stock_info(symbol):
    stock = yf.Ticker(symbol)

    # Collecting various data points
    stock_info = {
        'Major Holders': stock.major_holders,
        'Institutional Holders': stock.institutional_holders,
        'Mutual Fund Holders': stock.mutualfund_holders,
        'Insider Transactions': stock.insider_transactions,
        'Insider Purchases': stock.insider_purchases,
        'Upgrades/Downgrades': stock.upgrades_downgrades,
        'Analyst Price Targets': stock.analyst_price_targets,
        'Earnings Estimate': stock.earnings_estimate,
        'Revenue Estimate': stock.revenue_estimate,
        'Earnings History': stock.earnings_history,
    }
    return stock_info

# Function to generate the PDF from the fetched stock information
def generate_pdf(symbol, stock_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Advanced Stock Information for {symbol}", 0, 1, "C")
    pdf.ln(10)

    # Define a function to add wrapped text
    def add_wrapped_text(pdf, title, data, width=180):
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, title, 0, 1, "L")
        pdf.set_font("Arial", size=10)
        
        if isinstance(data, str):
            pdf.multi_cell(w=width, h=8, txt=data, border=0, align='L')
        elif isinstance(data, pd.DataFrame):
            for idx, row in data.iterrows():
                row_text = ', '.join([f"{col}: {row[col]}" for col in data.columns])
                pdf.multi_cell(w=width, h=8, txt=row_text, border=0, align='L')
        elif isinstance(data, list):
            for item in data:
                pdf.multi_cell(w=width, h=8, txt=str(item), border=0, align='L')
        else:
            pdf.multi_cell(w=width, h=8, txt="No data available", border=0, align='L')
        pdf.ln(5)

    # Add each section to the PDF
    for title, data in stock_info.items():
        add_wrapped_text(pdf, title, data)

    # Save the PDF file
    pdf_output_path = f"{symbol}_advanced_info.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path
