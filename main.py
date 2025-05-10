import tkinter as tk
from tkinter import messagebox
from stock_prediction_model import train_model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

app = tk.Tk()
app.title('台股預測 App')

tk.Label(app, text="股票代碼（如 2330.TW）").grid(row=0, column=0)
symbol_entry = tk.Entry(app)
symbol_entry.insert(0, "2330.TW")
symbol_entry.grid(row=0, column=1)

result_label = tk.Label(app, text="預測結果將顯示在這裡")
result_label.grid(row=2, column=0, columnspan=2)

canvas = None

def load_and_predict():
    global canvas
    symbol = symbol_entry.get().strip()
    if not symbol:
        messagebox.showerror("錯誤", "請輸入股票代碼")
        return
    try:
        model_close, model_high, model_low, (latest_input, df) = train_model(symbol)

        pred_close = model_close.predict(latest_input)[0]
        pred_high = model_high.predict(latest_input)[0]
        pred_low = model_low.predict(latest_input)[0]

        result_label.config(
            text=f"明日預測：\n收盤價：{pred_close:.2f}\n最高價：{pred_high:.2f}\n最低價：{pred_low:.2f}"
        )

        if canvas:
            canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)

        # 畫收盤價曲線
        ax.plot(df.index, df['Close'], label='歷史收盤價', color='black')
        ax.axhline(pred_close, color='red', linestyle='--', label=f'預測收盤：{pred_close:.2f}')
        ax.axhline(pred_high, color='green', linestyle=':', label=f'預測最高：{pred_high:.2f}')
        ax.axhline(pred_low, color='blue', linestyle=':', label=f'預測最低：{pred_low:.2f}')
        ax.set_title(f"{symbol} 收盤價與預測")
        ax.set_ylabel('價格')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

    except Exception as e:
        messagebox.showerror("錯誤", f"預測失敗：{e}")

tk.Button(app, text="預測明日股價", command=load_and_predict).grid(row=1, column=0, columnspan=2)

app.mainloop()
