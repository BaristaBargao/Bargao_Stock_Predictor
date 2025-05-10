import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train_model(symbol):
    df = yf.download(symbol, period="5y")
    df.dropna(inplace=True)

    df['Target_Close'] = df['Close'].shift(-1)
    df['Target_High'] = df['High'].shift(-1)
    df['Target_Low'] = df['Low'].shift(-1)
    df.dropna(inplace=True)

    features = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    target_close = df['Target_Close']
    target_high = df['Target_High']
    target_low = df['Target_Low']

    X_train, X_test, y_train_close, y_test_close = train_test_split(features, target_close, shuffle=False)
    _, _, y_train_high, _ = train_test_split(features, target_high, shuffle=False)
    _, _, y_train_low, _ = train_test_split(features, target_low, shuffle=False)

    model_close = RandomForestRegressor().fit(X_train, y_train_close)
    model_high = LinearRegression().fit(X_train, y_train_high)
    model_low = LinearRegression().fit(X_train, y_train_low)

    return model_close, model_high, model_low, (features.iloc[[-1]], df)
