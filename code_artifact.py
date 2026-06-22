import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime

# ==========================================
# 1. 定義從外部檔案讀取股票清單的函數
# ==========================================
def load_tickers_from_file(filepath):
    """
    從指定的純文字檔讀取股票代號與名稱。
    預設檔案格式例如:
    代號.TW, # 名稱
    2330.TW, # 台積電
    """
    tickers = {}
    
    if not os.path.exists(filepath):
        print(f"❌ 錯誤: 找不到檔案 '{filepath}'。請確認檔案與本程式放置於同一目錄下。")
        return tickers

    print(f"讀取清單檔案: {filepath} ...")
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # 移除行首尾的空白字元
            line = line.strip()
            
            # 略過空行或純註解行(不含代碼的行)
            if not line or line.startswith('#'):
                continue
                
            # 根據逗號分割
            parts = line.split(',')
            ticker_part = parts[0].strip()
            
            # 確保提取出的內容不是標題列，且為有效的字串
            if ticker_part and ticker_part != '代號.TW':
                # 萃取中文名稱並移除 '#' 與空白
                name_part = parts[1].replace('#', '').strip() if len(parts) > 1 else "未知名稱"
                tickers[ticker_part] = name_part
                
    print(f"✅ 成功載入 {len(tickers)} 檔股票準備進行掃描。")
    return tickers

# ==========================================
# 2. 定義篩選邏輯函數
# ==========================================
def filter_stock(ticker_symbol):
    try:
        # 獲取過去 2 個月的歷史資料 (確保有足夠的天數計算 20 日布林通道)
        # 設定 progress=False 避免 yfinance 印出過多進度條干擾畫面
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period="2mo")
        
        # 如果資料筆數不足 20 天，則無法計算完整的布林通道，直接排除
        if len(df) < 20:
            return False, None, None
            
        # 計算 8 日均線 (MA8)
        df['MA8'] = df['Close'].rolling(window=8).mean()
        
        # 計算布林通道 (通常預設為 20 日均線 +/- 2倍標準差)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD20'] = df['Close'].rolling(window=20).std()
        df['Upper_BB'] = df['MA20'] + (2 * df['STD20'])
        
        # 獲取最新一個交易日 (today) 與前一個交易日 (yesterday) 的資料
        today = df.iloc[-1]
        yesterday = df.iloc[-2]
        
        # --- 擴充：大戶籌碼資料接口 (模擬) ---
        # 由於 yfinance 不支援台股籌碼資料，此處建立資料結構供未來串接真實資料庫
        # 暫時利用成交量的零頭來產生一個固定的虛擬持股數，僅供確保程式邏輯能順利測試
        df['Large_Holder'] = df['Volume'] % 1000 
        today = df.iloc[-1]
        yesterday = df.iloc[-2]
        
        # 取得該筆資料的實際交易日期字串 (YYYY-MM-DD)
        data_date = df.index[-1].strftime('%Y-%m-%d')
        
        # --- 條件驗證與動態標註 ---
        met_conditions = []
        
        # 新規則: 大戶1000張以上比前一天增加 (籌碼面)
        # 若未來有真實資料庫，請將 'Large_Holder' 替換為實際的大戶持股欄位
        if today['Large_Holder'] > yesterday['Large_Holder']:
            met_conditions.append("大戶1000張以上比前一天增加")
        
        # 條件 2: 成交量大於 5000 張 
        # (台股 1 張 = 1000 股，yfinance 抓取的 Volume 單位為「股」)
        if today['Volume'] >= 5_000_000:
            met_conditions.append("成交量大於5000張")
        
        # 條件 3 & 5: 收盤價在上軌道之上且站上八均線
        if (today['Close'] > today['Upper_BB']) and (today['Close'] > today['MA8']):
            met_conditions.append("收盤價站上上軌道")
        
        # 條件 4: 八均線往上 (最新 MA8 大於 前一日 MA8)
        if today['MA8'] > yesterday['MA8']:
            met_conditions.append("八均線往上")
        
        # 綜合判斷 (必須「完全符合」技術與籌碼所有條件才納入清單，共 4 項)
        if len(met_conditions) == 4:
            # --- 計算連續站上高布林的天數 ---
            above_bb = df['Close'] > df['Upper_BB']
            days_above = 0
            
            # 從最新一天(today)開始往前數，遇到沒有站上就停止累加
            for is_above in above_bb.iloc[::-1]:
                if is_above:
                    days_above += 1
                else:
                    break
                    
            # 判斷型態：今天剛突破 (1天) vs 維持強勢 (>1天)
            if days_above == 1:
                pattern_type = "今天剛突破"
            else:
                pattern_type = f"維持強勢 ({days_above}天)"
            
            # 記錄符合條件的相關數據以供參考，並加入連續天數資訊
            info = {
                '代號': ticker_symbol,
                '收盤價': round(today['Close'], 2),
                '成交張數': int(today['Volume'] / 1000),
                'MA8': round(today['MA8'], 2),
                '布林上軌': round(today['Upper_BB'], 2),
                '站上天數': days_above,
                '型態': pattern_type,
                '符合項目': '、'.join(met_conditions)
            }
            return True, info, data_date
            
        return False, None, data_date

    except Exception as e:
        # 若抓取資料發生錯誤（例如下市或無資料），忽略並繼續
        return False, None, None

# ==========================================
# 3. 執行主程式
# ==========================================
def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 啟動技術面篩選器...")
    print("-" * 50)
    
    # 從 txt 檔案讀取股票名單與名稱
    file_path = '股票代碼.txt'
    stock_dict = load_tickers_from_file(file_path)
    
    if not stock_dict:
        print("未載入任何股票代號，程式結束。")
        return

    print("-" * 50)
    print("開始掃描，請耐心等候 (依據清單長短可能需要數分鐘)...")
    
    # 準備兩個陣列來分別存放兩種型態的股票
    matched_breakout = []
    matched_sustained = []
    report_date = None
    
    for ticker, name in stock_dict.items():
        is_match, stock_info, data_date = filter_stock(ticker)
        
        # 捕捉第一筆成功獲取資料的交易日期，作為報表統一的資料日期
        if data_date and not report_date:
            report_date = data_date
            
        if is_match:
            # 將名稱加入到紀錄字典中，並確保欄位順序美觀
            full_info = {'代號': ticker, '名稱': name}
            
            # 取出符合項目與型態供終端機輸出與分類使用
            met_items = stock_info.pop('符合項目', '')
            pattern = stock_info.pop('型態', '')
            days_above = stock_info.pop('站上天數', 1) # 取出天數作為內部邏輯判斷
            
            full_info.update({k: v for k, v in stock_info.items() if k != '代號'})
            # 將額外資訊放回字典最後方，讓呈現表格時能排在最後
            full_info['站上天數'] = days_above
            full_info['符合項目'] = met_items 
            
            # 依據天數分流至對應的陣列 (1天為剛突破，大於1天為維持強勢)
            if days_above == 1:
                matched_breakout.append(full_info)
            else:
                matched_sustained.append(full_info)
            
            # 更新輸出的文字內容，將型態與符合項目標註在後面
            print(f"💡 發現強勢標的 [{pattern}] [{met_items}]: {ticker} {name}")
            
    print("-" * 50)
    
    # 準備報表開頭的日期標註
    display_date = report_date if report_date else "未知"
    print(f"掃描結束。交易日(資料日期)：{display_date}")
    
    # --- 分別印出兩張報表 ---
    print("\n【分類一】今天剛突破高布林 (第1天站上)：")
    if matched_breakout:
        result_breakout_df = pd.DataFrame(matched_breakout)
        print(result_breakout_df.to_string(index=False))
    else:
        print("今日無「剛突破高布林」之股票。")
        
    print("\n【分類二】維持強勢股 (連續多日站上高布林)：")
    if matched_sustained:
        # 讓維持強勢的股票，依照「站上天數」由大到小排序，方便看出哪些最強
        result_sustained_df = pd.DataFrame(matched_sustained).sort_values(by='站上天數', ascending=False)
        print(result_sustained_df.to_string(index=False) + "\n")
    else:
        print("今日無「維持在高布林之上」之股票。\n")

if __name__ == "__main__":
    main()