from tw_corporate_data import get_corporate_trading_single

df = get_corporate_trading_single("2024-05-09")  # 你可以改成今天或昨天
if df is not None:
    print("✅ 抓到的欄位：")
    print(df.columns.tolist())
else:
    print("❌ 沒有抓到資料")
