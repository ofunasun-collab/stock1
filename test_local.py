# 本地測試程式 - 模擬數據和報表生成
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# 確保可以導入模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator
import config

def generate_mock_stock_data():
    """
    生成模擬股票數據
    
    Returns:
        包含模擬符合條件股票的列表
    """
    # 模擬的電子股數據
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
            '符合條件數': 4,
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
            '符合條件數': 4,
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
            '符合條件數': 4,
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
            '符合條件數': 4,
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
            '大戶持倒增加(張)': 2300,
            '昨日成交量': 38900,
            '漲跌幅(%)': 1.65,
            '符合條件數': 4,
        },
    ]
    
    return mock_stocks

def test_report_generation():
    """測試報表生成功能"""
    print("\n" + "="*100)
    print("台灣股票過濾程式 - 本地測試")
    print("="*100)
    print(f"\n測試執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 建立報表生成器
        report = ReportGenerator()
        report.set_data_fetch_time(datetime.now() - timedelta(seconds=30))
        
        # 添加模擬數據
        print("\n📊 生成模擬股票數據...")
        mock_stocks = generate_mock_stock_data()
        
        for stock in mock_stocks:
            report.add_filtered_stock(stock)
            print(f"  ✓ 添加 {stock['股票代碼']} ({stock['股票名稱']})")
        
        print(f"\n總共添加 {len(mock_stocks)} 檔符合條件的股票")
        
        # 生成 DataFrame
        print("\n📈 生成數據表...")
        df = report.generate_report_dataframe()
        print(f"  ✓ 成功生成 {len(df)} 行數據")
        
        # 保存 Excel 報表
        print("\n💾 保存 Excel 報表...")
        excel_file = report.save_excel_report("測試報表_模擬數據.xlsx")
        if excel_file:
            file_size = os.path.getsize(excel_file)
            print(f"  ✓ Excel 報表已保存")
            print(f"    路徑: {excel_file}")
            print(f"    大小: {file_size / 1024:.1f} KB")
        
        # 保存 CSV 報表
        print("\n💾 保存 CSV 報表...")
        csv_file = report.save_csv_report("測試報表_模擬數據.csv")
        if csv_file:
            file_size = os.path.getsize(csv_file)
            print(f"  ✓ CSV 報表已保存")
            print(f"    路徑: {csv_file}")
            print(f"    大小: {file_size / 1024:.1f} KB")
        
        # 在控制台顯示摘要
        print("\n" + "="*100)
        print("報表摘要")
        print("="*100)
        report.print_console_report()
        
        print("\n✓ 測試完成！報表已生成在 reports/ 目錄")
        print("\n📁 檔案位置:")
        print(f"  - Excel: {excel_file}")
        print(f"  - CSV: {csv_file}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_report_generation()
    sys.exit(0 if success else 1)
