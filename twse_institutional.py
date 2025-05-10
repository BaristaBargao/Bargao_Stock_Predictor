import pandas as pd
import requests
from io import StringIO
from datetime import datetime

def get_stock_data(stock_symbol: str) -> pd.DataFrame:
    """
    擷取指定股票的歷史股價資料。
    stock_symbol: 台股代號（如 '2330'）
    回傳 DataFrame 含 Date, Open, High, Low, Close 欄位
    """
    dfs = []
    current_year = datetime.now().year
    current_month = datetime.now().month

    for year in range(2019, current_year + 1):
        for month in range(1, 13):
            if year == current_year and month > current_month:
                break  # 不抓未來月份

            url = f'https://www.twse.com.tw/fund/BFI82U?response=csv&month={year:04d}{month:02d}&selectType=ALL'
            try:
                res = requests.get(url, timeout=10)
                data = res.text
                lines = [line for line in data.split('\n') if len(line.split(",")) >= 10 and '證券代號' not in line]
                data_cleaned = "\n".join(lines)

                df = pd.read_csv(StringIO(data_cleaned))
                df.columns = df.columns.str.strip()
                df = df[df['證券代號'].astype(str) == stock_symbol]

                if df.empty:
                    continue

                df = df.rename(columns={
                    '日期': 'Date',
                    '開盤價': 'Open',
                    '最高價': 'High',
                    '最低價': 'Low',
                    '收盤價': 'Close'
                })

                df['Date'] = pd.to_datetime(df['Date'].str.replace('/', '-'))
                df['Open'] = pd.to_numeric(df['Open'].astype(str).str.replace(',', ''), errors='coerce')
                df['High'] = pd.to_numeric(df['High'].astype(str).str.replace(',', ''), errors='coerce')
                df['Low'] = pd.to_numeric(df['Low'].astype(str).str.replace(',', ''), errors='coerce')
                df['Close'] = pd.to_numeric(df['Close'].astype(str).str.replace(',', ''), errors='coerce')

                dfs.append(df[['Date', 'Open', 'High', 'Low', 'Close']])
            except Exception as e:
                print(f"無法取得 {year}-{month:02d} 的資料：{e}")

    if dfs:
        return pd.concat(dfs).dropna().sort_values('Date').reset_index(drop=True)
    else:
        return pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close'])
