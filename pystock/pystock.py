import datetime as dt
import pandas as pd
import math
from scipy.optimize import fsolve
import yfinance as yahooFinance
from pandas_datareader import data as pdr


def fetch_stock_data(ticker: str, length: int) -> pd.DataFrame:
    """fetches pandas dataframe of stock prices for a given ticker

    Args:
        ticker (str): stock ticker
        length (int): number of days of data to fetch

    Raises:
        TypeError: incorrect/inavlid type given to function
        ConnectionError: invalid ticker given to function

    Returns:
        pd.DataFrame: dataframe containing stock data
    """
    if not isinstance(ticker, str) or not isinstance(length, int) or length < 2:
        raise TypeError()

    end = dt.datetime.now()
    start = end - dt.timedelta(days=length)

    yahooFinance.pdr_override()

    df = pdr.get_data_yahoo(ticker, start, end)

    if df.empty:
        raise ConnectionError("Invalid Ticker")

    return df


def calculate_sigma(dataframe: pd.DataFrame) -> float:
    dataframe["Mean"] = (dataframe["High"] + dataframe["Low"]) / 2
    mean = dataframe["Mean"].mean()
    variance = dataframe["Mean"].var()
    print(mean, variance)

    def generate_black_scholes_system_of_equations(vars):
        return [
            math.exp(2 * math.log(mean))
            + vars[0] ** 2 * math.exp(vars[0])
            - math.exp(2 * math.log(mean) - vars[0] ** 2)
            - vars[0] ** 2
            - variance,
        ]

    sigma = fsolve(generate_black_scholes_system_of_equations, [0.1])

    return sigma
