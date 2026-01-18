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


    