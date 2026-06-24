# 簡化版 - 測試報表生成（獨立運行）
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_stock_data():
    """生成模擬股票數據"""
    mock_stocks = [
        {
            '股票代碼': '2330',
            '股票名稱': '台積電',
            '收盤價': 892.50,
            '布林上軌': 880.25,
            '布林中線': 850.00,
            '布林下軌': 819.75,
            '8均線': 885.30,
            '成交量(張)': 35420,
            '大戶持倉增加(張)': 2150,
            '昨日成交量': 31200,
            '漲跌幅(%)': 2.45,
        },
        {
            '股票代碼': '2454',
            '股票名稱': '聯發科',
            '收盤價': 1156.00,
            '布林上軌': 1140.50,
            '布林中線': 1100.00,
            '布林下軌': 1059.50,
            '8均線': 1150.80,
            '成交量(張)': 12850,
            '大戶持倉增加(張)': 1520,
            '昨日成交量': 10300,
            '漲跌幅(%)': 1.85,
        },
        {
            '股票代碼': '2412',
            '股票名稱': '中華電',
            '收盤價': 140.50,
            '布林上軌': 138.20,
            '布林中線': 132.00,
            '布林下軌': 125.80,
            '8均線': 139.60,
            '成交量(張)': 3450,
            '大戶持倉增加(張)': 1200,
            '昨日成交量': 2100,
            '漲跌幅(%)': 3.20,
        },
        {
            '股票代碼': '3008',
            '股票名稱': '聯詠',
            '收盤價': 685.00,
            '布林上軌': 670.30,
            '布林中線': 640.00,
            '布林下軌': 609.70,
            '8均線': 680.50,
            '成交量(張)': 4520,
            '大戶持倉增加(張)': 1800,
            '昨日成交量': 2800,
            '漲跌幅(%)': 2.15,
        },
        {
            '股票代碼': '2303',
            '股票名稱': '聯電',
            '收盤價': 61.20,
            '布林上軌': 59.80,
            '布林中線': 57.50,
            '布林下軌': 55.20,
            '8均線': 60.80,
            '成交量(張)': 42150,
            '大戶持倉增加(張)': 2300,
            '昨日成交量': 38900,
            '漲跌幅(%)': 1.65,
        },
    ]
    return mock_stocks

def test_report_generation():
    """測試報表生成"""
    print("\n" + "="*100)
    print("台灣股票過濾程式 - 本地測試（簡化版）")
    print("="*100)
    print(f"\n執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 建立輸出目錄
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # 生成模擬數據
    print("📊 生成模擬股票數據...")
    mock_stocks = generate_mock_stock_data()
    
    for stock in mock_stocks:
        print(f"  ✓ {stock['股票代碼']} ({stock['股票名稱']}) - 收盤價 {stock['收盤價']}")
    
    # 轉換為 DataFrame
    print("\n📈 生成數據表...")
    df = pd.DataFrame(mock_stocks)
    print(f"  ✓ 成功生成 {len(df)} 行數據")
    
    # 按收盤價降序排列
    df = df.sort_values('收盤價', ascending=False)
    
    # 保存 Excel
    print("\n💾 保存 Excel 報表...")
    execution_time = datetime.now()
    excel_filename = f"tests_report_{execution_time.strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_path = os.path.join("reports", excel_filename)
    
    try:
        df.to_excel(excel_path, index=False, sheet_name='過濾結果')
        file_size = os.path.getsize(excel_path) / 1024
        print(f"  ✓ Excel 報表已保存")
        print(f"    路徑: {excel_path}")
        print(f"    大小: {file_size:.1f} KB")
    except ImportError:
        print(f"  ⚠ 需要安裝 openpyxl，執行: pip install openpyxl")
        excel_path = None
    
    # 保存 CSV
    print("\n💾 保存 CSV 報表...")
    csv_filename = f"test_report_{execution_time.strftime('%Y%m%d_%H%M%S')}.csv"
    csv_path = os.path.join("reports", csv_filename)
    
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        file_size = os.path.getsize(csv_path) / 1024
        print(f"  ✓ CSV 報表已保存")
        print(f"    路徑: {csv_path}")
        print(f"    大小: {file_size:.1f} KB")
    except Exception as e:
        print(f"  ✗ 保存 CSV 失敗: {e}")
        csv_path = None
    
    # 顯示報表內容
    print("\n" + "="*100)
    print("報表內容")
    print("="*100)
    print(f"\n程式執行時間: {execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"數據撈取時間: {execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"掃描範圍: 台灣電子類股")
    print(f"數據來源: Google Finance / Yahoo Finance")
    print(f"符合條件股票數: {len(df)} 檔\n")
    
    print("過濾結果:")
    print(df.to_string(index=False))
    
    print("\n" + "="*100)
    print("✓ 測試完成！")
    print("="*100)
    print(f"\n📁 報表位置:")
    if excel_path:
        print(f"  - Excel: {os.path.abspath(excel_path)}")
    if csv_path:
        print(f"  - CSV: {os.path.abspath(csv_path)}")
    print()
    
    return True

if __name__ == "__main__":
    test_report_generation()
