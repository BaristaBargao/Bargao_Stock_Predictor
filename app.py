from flask import Flask, render_template, request, redirect, url_for
from stock_prediction_model import train_model
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import os

app = Flask(__name__)
HISTORY_FILE = 'prediction_history.csv'


@app.route('/')
def landing():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    error = None
    prediction = None
    plot_url = None

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            error = '請輸入正確的股票代碼，例如 2330.TW'
        else:
            try:
                model_close, model_high, model_low, (latest_features, df_full) = train_model(symbol)
                predicted_close = model_close.predict(latest_features)[0]
                predicted_high = model_high.predict(latest_features)[0]
                predicted_low = model_low.predict(latest_features)[0]

                prediction = {
                    'symbol': symbol,
                    'predicted_close': round(predicted_close, 2),
                    'predicted_high': round(predicted_high, 2),
                    'predicted_low': round(predicted_low, 2)
                }

                # 儲存紀錄
                today = pd.Timestamp.today().strftime('%Y-%m-%d')
                new_row = pd.DataFrame([{
                    'date': today,
                    'symbol': symbol,
                    'close': prediction['predicted_close'],
                    'high': prediction['predicted_high'],
                    'low': prediction['predicted_low']
                }])
                if os.path.exists(HISTORY_FILE):
                    new_row.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
                else:
                    new_row.to_csv(HISTORY_FILE, index=False)

                # 畫圖
                df_tail = df_full.tail(60)
                plt.figure(figsize=(10, 4))
                plt.plot(df_tail.index, df_tail['Close'], label='歷史收盤價')
                plt.scatter(df_tail.index[-1] + pd.Timedelta(days=1), predicted_close, color='red', label='預測收盤價')
                plt.title(f'{symbol} 收盤價與預測')
                plt.xlabel('日期')
                plt.ylabel('股價')
                plt.legend()
                plt.tight_layout()

                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
                plt.close()

            except Exception as e:
                error = f"無法取得或預測該股票：{e}"

    return render_template('predict.html', prediction=prediction, error=error, plot_url=plot_url)


@app.route('/history')
def history():
    if not os.path.exists(HISTORY_FILE):
        records = []
    else:
        df = pd.read_csv(HISTORY_FILE)
        records = df.to_dict(orient='records')

    return render_template('history.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from stock_prediction_model import train_model
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import os

app = Flask(__name__)
HISTORY_FILE = 'prediction_history.csv'


@app.route('/')
def landing():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    error = None
    prediction = None
    plot_url = None

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            error = '請輸入正確的股票代碼，例如 2330.TW'
        else:
            try:
                model_close, model_high, model_low, (latest_features, df_full) = train_model(symbol)
                predicted_close = model_close.predict(latest_features)[0]
                predicted_high = model_high.predict(latest_features)[0]
                predicted_low = model_low.predict(latest_features)[0]

                prediction = {
                    'symbol': symbol,
                    'predicted_close': round(predicted_close, 2),
                    'predicted_high': round(predicted_high, 2),
                    'predicted_low': round(predicted_low, 2)
                }

                # 儲存紀錄
                today = pd.Timestamp.today().strftime('%Y-%m-%d')
                new_row = pd.DataFrame([{
                    'date': today,
                    'symbol': symbol,
                    'close': prediction['predicted_close'],
                    'high': prediction['predicted_high'],
                    'low': prediction['predicted_low']
                }])
                if os.path.exists(HISTORY_FILE):
                    new_row.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
                else:
                    new_row.to_csv(HISTORY_FILE, index=False)

                # 畫圖
                df_tail = df_full.tail(60)
                plt.figure(figsize=(10, 4))
                plt.plot(df_tail.index, df_tail['Close'], label='歷史收盤價')
                plt.scatter(df_tail.index[-1] + pd.Timedelta(days=1), predicted_close, color='red', label='預測收盤價')
                plt.title(f'{symbol} 收盤價與預測')
                plt.xlabel('日期')
                plt.ylabel('股價')
                plt.legend()
                plt.tight_layout()

                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
                plt.close()

            except Exception as e:
                error = f"無法取得或預測該股票：{e}"

    return render_template('predict.html', prediction=prediction, error=error, plot_url=plot_url)


@app.route('/history')
def history():
    if not os.path.exists(HISTORY_FILE):
        records = []
    else:
        df = pd.read_csv(HISTORY_FILE)
        records = df.to_dict(orient='records')

    return render_template('history.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)
