import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stock_prices")

@mcp.tool()
async def get_stock_price(ticker: str) -> str:
    """
    Get the current stock price for a given ticker symbol.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
    
    Returns:
        str: The current stock price.
    """
    print(f"Fetching price for {ticker}")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not current_price:
            return f"Could not retrieve price for {ticker}"
        return f"${current_price:.2f}"
    except Exception as e: 
        return f"Error fetching data for {ticker}: {str(e)}"
    


@mcp.tool()
async def get_stock_price_for_period(ticker: str, start: str, end: str) -> str:
    """
    Get the stock price for a given ticker symbol over a specified period.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
        start (str): Start date in 'YYYY-MM-DD' format.
        end (str): End date in 'YYYY-MM-DD'
    
    Returns:
        str: The stock price for the specified period.
    """
    print(f"Fetching price for {ticker}")
    try:
        # Fetch the stock data for the specified period
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            return f"No data found for {ticker} in the given period."
        
        return data
    except Exception as e: 
        return f"Error fetching data for {ticker}: {str(e)}"
        
if __name__ == "__main__":
    mcp.run()