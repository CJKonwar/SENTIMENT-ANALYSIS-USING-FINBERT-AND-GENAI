import yfinance as yf
import pandas as pd

def get_all_stock_info(symbol):
    """
    Fetches a comprehensive set of stock information for the given symbol using yfinance
    and returns it in a structured DataFrame.
    
    Args:
        symbol (str): The stock symbol to fetch data for.
        
    Returns:
        pandas.DataFrame: A DataFrame containing various stock metrics.
    """
    stock = yf.Ticker(symbol)

    # Collecting various data points
    data = {
        'Metric': [
            'Name',
            'Market Cap',
            'P/E Ratio',
            'P/E Industry Ratio',
            'P/B Ratio',
            'Debt to Equity',
            'Face Value',
            'ROE',
            'Book Value',
            'Revenue',
            'Net Income',
            'Operating Cash Flow',
        ],
        'Value': [
            stock.info.get('longName', 'N/A'),  # Company Name
            stock.info.get('marketCap', 'N/A'),  # Market Capitalization
            stock.info.get('forwardPE', 'N/A'),  # Forward P/E ratio
            stock.info.get('trailingPE', 'N/A'),  # Trailing P/E ratio
            stock.info.get('priceToBook', 'N/A'),  # Price to Book ratio
            stock.info.get('debtToEquity', 'N/A'),  # Debt to Equity ratio
            stock.info.get('faceValue', 'N/A'),  # Face value of the stock
            stock.info.get('returnOnEquity', 'N/A'),  # Return on Equity
            stock.info.get('bookValue', 'N/A'),  # Book Value per share
            stock.financials.loc['Total Revenue'][0] if 'Total Revenue' in stock.financials.index else 'N/A',  # Revenue
            stock.financials.loc['Net Income'][0] if 'Net Income' in stock.financials.index else 'N/A',  # Net Income
            stock.cashflow.loc['Cash Flow From Operating Activities'][0] if 'Cash Flow From Operating Activities' in stock.cashflow.index else 'N/A',  # Operating Cash Flow
        ]
    }

    df = pd.DataFrame(data)
    return df
