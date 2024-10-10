import yfinance as yf
import pandas as pd

def get_all_stock_info(symbol):
    """
    Fetches a comprehensive set of stock information for the given symbol using yfinance.
    
    Args:
        symbol (str): The stock symbol to fetch data for.
        
    Returns:
        dict: A dictionary containing various stock metrics.
    """
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