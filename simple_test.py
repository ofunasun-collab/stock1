# Simple test - Generate mock report (standalone)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_stock_data():
    """Generate mock stock data"""
    mock_stocks = [
        {
            'stock_code': '2330',
            'stock_name': 'TSMC',
            'close_price': 892.50,
            'bb_upper': 880.25,
            'bb_middle': 850.00,
            'bb_lower': 819.75,
            'ema8': 885.30,
            'volume': 35420,
            'major_holder_increase': 2150,
            'yesterday_volume': 31200,
            'price_change': 2.45,
        },
        {
            'stock_code': '2454',
            'stock_name': 'MediaTek',
            'close_price': 1156.00,
            'bb_upper': 1140.50,
            'bb_middle': 1100.00,
            'bb_lower': 1059.50,
            'ema8': 1150.80,
            'volume': 12850,
            'major_holder_increase': 1520,
            'yesterday_volume': 10300,
            'price_change': 1.85,
        },
        {
            'stock_code': '2412',
            'stock_name': 'Chunghwa Telecom',
            'close_price': 140.50,
            'bb_upper': 138.20,
            'bb_middle': 132.00,
            'bb_lower': 125.80,
            'ema8': 139.60,
            'volume': 3450,
            'major_holder_increase': 1200,
            'yesterday_volume': 2100,
            'price_change': 3.20,
        },
        {
            'stock_code': '3008',
            'stock_name': 'Novatek',
            'close_price': 685.00,
            'bb_upper': 670.30,
            'bb_middle': 640.00,
            'bb_lower': 609.70,
            'ema8': 680.50,
            'volume': 4520,
            'major_holder_increase': 1800,
            'yesterday_volume': 2800,
            'price_change': 2.15,
        },
        {
            'stock_code': '2303',
            'stock_name': 'UMC',
            'close_price': 61.20,
            'bb_upper': 59.80,
            'bb_middle': 57.50,
            'bb_lower': 55.20,
            'ema8': 60.80,
            'volume': 42150,
            'major_holder_increase': 2300,
            'yesterday_volume': 38900,
            'price_change': 1.65,
        },
    ]
    return mock_stocks

def test_report_generation():
    """Test report generation"""
    print("\n" + "="*100)
    print("Taiwan Stock Filter - Local Test (Simplified)")
    print("="*100)
    print(f"\nExecution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Create output directory
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Generate mock data
    print("Generating mock stock data...")
    mock_stocks = generate_mock_stock_data()
    
    for stock in mock_stocks:
        print(f"  OK {stock['stock_code']} ({stock['stock_name']}) - Close {stock['close_price']}")
    
    # Convert to DataFrame
    print("\nGenerating data table...")
    df = pd.DataFrame(mock_stocks)
    print(f"  OK Generated {len(df)} rows")
    
    # Sort by close price descending
    df = df.sort_values('close_price', ascending=False)
    
    # Save Excel
    print("\nSaving Excel report...")
    execution_time = datetime.now()
    excel_filename = f"test_report_{execution_time.strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_path = os.path.join("reports", excel_filename)
    
    try:
        df.to_excel(excel_path, index=False, sheet_name='Results')
        file_size = os.path.getsize(excel_path) / 1024
        print(f"  OK Excel report saved")
        print(f"    Path: {excel_path}")
        print(f"    Size: {file_size:.1f} KB")
    except ImportError:
        print(f"  WARNING Need openpyxl: pip install openpyxl")
        excel_path = None
    except Exception as e:
        print(f"  ERROR Save Excel failed: {e}")
        excel_path = None
    
    # Save CSV
    print("\nSaving CSV report...")
    csv_filename = f"test_report_{execution_time.strftime('%Y%m%d_%H%M%S')}.csv"
    csv_path = os.path.join("reports", csv_filename)
    
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        file_size = os.path.getsize(csv_path) / 1024
        print(f"  OK CSV report saved")
        print(f"    Path: {csv_path}")
        print(f"    Size: {file_size:.1f} KB")
    except Exception as e:
        print(f"  ERROR Save CSV failed: {e}")
        csv_path = None
    
    # Display report content
    print("\n" + "="*100)
    print("Report Content")
    print("="*100)
    print(f"\nExecution Time: {execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Fetch Time: {execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scan Range: Taiwan Electronics Stocks")
    print(f"Data Source: Google Finance / Yahoo Finance")
    print(f"Matched Stocks: {len(df)} stocks\n")
    
    print("Filter Results:")
    print(df.to_string(index=False))
    
    print("\n" + "="*100)
    print("Test Complete!")
    print("="*100)
    print(f"\nReport Locations:")
    if excel_path:
        print(f"  - Excel: {os.path.abspath(excel_path)}")
    if csv_path:
        print(f"  - CSV: {os.path.abspath(csv_path)}")
    print()
    
    return True

if __name__ == "__main__":
    test_report_generation()
