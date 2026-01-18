from io import StringIO

import pandas as pd
import urllib3


def get_sp500_tickers():
    """
    Fetch the current list of S&P 500 ticker symbols from Wikipedia.

    The data is scraped from the main S&P 500 constituents table on the
    Wikipedia page. Tickers are normalized for compatibility with common
    finance APIs (e.g., Yahoo Finance uses '-' instead of '.').

    Returns
    -------
    list
        Sorted list of S&P 500 ticker symbols.
        Example: ["AAPL", "AMZN", "BRK-B", "MSFT", ...]
    """
    # Create a connection pool with a browser-like User-Agent
    http = urllib3.PoolManager(
        headers={"User-Agent": "Mozilla/5.0"}
    )

    # Perform HTTP GET request
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = http.request("GET", url)

    # Decode HTML content
    html = response.data.decode("utf-8")

    # Parse all tables from the HTML
    tables = pd.read_html(StringIO(html))

    # First table contains the S&P 500 constituents
    sp500_table = tables[0]

    # Extract ticker symbols
    tickers = sp500_table["Symbol"].tolist()

    # Normalize tickers for Yahoo Finance compatibility (e.g., BRK.B -> BRK-B)
    tickers = [ticker.replace(".", "-") for ticker in tickers]

    # Return a sorted, stable list
    return sorted(tickers)



import time
import yfinance as yf


def build_company_info(tickers, pause=0.10):
    """
    Fetch basic company metadata for a list of stock tickers using yfinance.

    For each ticker, this function retrieves the company's short name,
    sector, and industry from Yahoo Finance and stores the results in a
    dictionary keyed by ticker symbol.

    A short delay is added between requests to reduce the likelihood of
    rate limiting by Yahoo Finance.

    Parameters
    ----------
    tickers : iterable of str
        Stock ticker symbols (e.g., ["AAPL", "MSFT", "BRK-B"]).

    pause : float, optional
        Number of seconds to sleep between API calls (default is 0.10).

    Returns
    -------
    dict
        Dictionary mapping ticker symbols to company information.
        Example:
        {
            "AAPL": {
                "Name": "Apple Inc.",
                "Sector": "Technology",
                "Industry": "Consumer Electronics"
            },
            ...
        }
    """
    company_info = {}

    for ticker in tickers:
        # Create a yfinance Ticker object
        stock = yf.Ticker(ticker)

        # Fetch metadata dictionary from Yahoo Finance
        info = stock.info

        # Safely extract relevant fields (may be missing or None)
        company_info[ticker] = {
            "Name": info.get("shortName"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
        }

        # Pause to avoid triggering rate limits
        time.sleep(pause)

    return company_info


    