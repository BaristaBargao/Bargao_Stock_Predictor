# twse_data.py
import yfinance as yf
import pandas as pd

def get_taiwan_stock_data(symbol, start_date="2018-01-01", end_date="2023-01-01"):
    """
    使用 yfinance 爬取台灣股票資料。
    :param symbol: 股票代碼，如 '2330.TW'
    :param start_date: 開始日期，預設 '2018-01-01'
    :param end_date: 結束日期，預設 '2023-01-01'
    :return: 台灣股市的歷史資料 DataFrame
    """
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    if stock_data.empty:
        raise ValueError(f"無法獲取 {symbol} 的資料。請確認股票代碼是否正確。")
    return stock_data
