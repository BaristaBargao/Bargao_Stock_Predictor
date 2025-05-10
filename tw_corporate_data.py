import pandas as pd
import requests
from datetime import datetime, timedelta
import yfinance as yf
import io
import certifi

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.twse.com.tw/zh/trading/foreign/bfi82u.html'
}

def get_corporate_trading_single(date):
    """
    從 https://www.twse.com.tw/zh/trading/foreign/bfi82u.html 下載外資每日買賣超總表
    """
    date_str = pd.to_datetime(date).strftime("%Y%m%d")
    url = f'https://www.twse.com.tw/fund/BFI82U?response=csv&dayDate={date_str}&type=day'

    try:
        r = requests.get(url, headers=headers, timeout=10, verify=certifi.where())
        r.encoding = 'utf-8'
    except Exception as e:
        print(f"❌ 無法連線 TWSE：{e}")
        return None

    raw = r.text
    lines = [line for line in raw.split('\n') if ',' in line and '證券代號' not in line and '合計' not in line]
    if not lines:
        print("❌ 沒有可用的法人資料")
        return None

    csv_text = '\n'.join(lines)
    df = pd.read_csv(io.StringIO(csv_text), header=None)

    df.columns = ['證券代號', '證券名稱', '外資買進股數', '外資賣出股數', '外資買賣超股數', '投信買進股數', '投信賣出股數', '投信買賣超股數', '自營商買進股數', '自營商賣出股數', '自營商買賣超股數']
    df = df[['證券代號', '外資買賣超股數']]
    df = df.replace('--', '0').fillna('0')
    df['證券代號'] = df['證券代號'].astype(str).str.zfill(4)
    df['外資買賣超股數'] = df['外資買賣超股數'].astype(str).str.replace(',', '', regex=False).astype(int)

    df = df.set_index('證券代號')
    df['Date'] = pd.to_datetime(date)
    return df


def get_corporate_trading_range(days=60):
    today = datetime.today()
    result = []
    for i in range(days):
        d = today - timedelta(days=i)
        df_day = get_corporate_trading_single(d)
        if df_day is not None:
            result.append(df_day)

    if not result:
        raise ValueError("抓不到任何法人資料")

    df_all = pd.concat(result)
    df_all = df_all.reset_index().set_index(['Date', '證券代號'])
    return df_all.sort_index()


def get_merged_stock_and_corporate(symbol='2330.TW', days=60):
    df_price = yf.download(symbol, period=f"{days}d")
    df_price = df_price.dropna()
    df_price.index = pd.to_datetime(df_price.index)

    code = symbol.split('.')[0].zfill(4)
    df_corp = get_corporate_trading_range(days)
    df_corp_stock = df_corp.xs(code, level='證券代號')

    df_all = pd.merge(df_price, df_corp_stock, left_index=True, right_index=True, how='inner')
    df_all = df_all.rename(columns={'外資買賣超股數': 'Foreign'})
    return df_all
