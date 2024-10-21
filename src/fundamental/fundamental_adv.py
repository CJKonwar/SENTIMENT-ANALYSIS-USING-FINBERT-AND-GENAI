import yfinance as yf

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
