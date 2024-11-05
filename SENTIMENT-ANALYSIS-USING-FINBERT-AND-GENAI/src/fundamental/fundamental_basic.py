import yfinance as yf
import pandas as pd


def get_all_stock_info(symbol):

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
            stock.info.get('longName', 'N/A'),  
            stock.info.get('marketCap', 'N/A'),  
            stock.info.get('forwardPE', 'N/A'),  
            stock.info.get('trailingPE', 'N/A'),  
            stock.info.get('priceToBook', 'N/A'),  
            stock.info.get('debtToEquity', 'N/A'),  
            stock.info.get('faceValue', 'N/A'),  
            stock.info.get('returnOnEquity', 'N/A'),  
            stock.info.get('bookValue', 'N/A'),
            stock.financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in stock.financials.index else 'N/A',
            stock.financials.loc['Net Income'].iloc[0] if 'Net Income' in stock.financials.index else 'N/A',  
            stock.cashflow.loc['Cash Flow From Operating Activities'][0] if 'Cash Flow From Operating Activities' in stock.cashflow.index else 'N/A', 
        ]
    }

    df = pd.DataFrame(data)
    return df
