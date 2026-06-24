# 主程式 - 台灣股票過濾系統
import logging
import os
from datetime import datetime
import sys

import config
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer, FilterConditions
from report_generator import ReportGenerator


# ==================== 日誌設定 ====================
def setup_logging():
    """設置日誌"""
    if not os.path.exists(config.LOG_DIR):
        os.makedirs(config.LOG_DIR)
    
    log_file = os.path.join(
        config.LOG_DIR,
        f"stock_filter_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


logger = setup_logging()


class StockFilterSystem:
    """台灣股票過濾系統主類"""
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.report = ReportGenerator()
        self.filtered_results = []
        
    def run(self):
        """運行完整的過濾流程"""
        logger.info("="*80)
        logger.info("台灣股票過濾系統 - 開始執行")
        logger.info("="*80)
        
        try:
            # 第1步: 抓取數據
            logger.info(f"第1步: 抓取電子類股數據...")
            self._fetch_stock_data()
            
            # 第2步: 過濾股票
            logger.info(f"第2步: 進行股票過濾...")
            self._filter_stocks()
            
            # 第3步: 生成報表
            logger.info(f"第3步: 生成報表...")
            self._generate_reports()
            
            logger.info("="*80)
            logger.info("台灣股票過濾系統 - 執行完成")
            logger.info("="*80)
            
            return True
            
        except Exception as e:
            logger.error(f"執行過程中發生錯誤: {str(e)}", exc_info=True)
            return False
    
    def _fetch_stock_data(self):
        """抓取股票數據"""
        logger.info(f"開始抓取 {len(config.ELECTRONICS_STOCKS)} 檔電子股的數據...")
        
        # 抓取所有電子股的數據
        self.fetcher.fetch_multiple_stocks(config.ELECTRONICS_STOCKS)
        
        # 記錄數據抓取時間
        self.report.set_data_fetch_time(self.fetcher.get_data_fetch_time())
        
        logger.info(f"成功抓取 {len(self.fetcher.stocks_data)} 檔股票的數據")
    
    def _filter_stocks(self):
        """過濾符合條件的股票"""
        logger.info("開始進行股票過濾...")
        
        filtered_count = 0
        
        for stock_code in config.ELECTRONICS_STOCKS:
            if stock_code not in self.fetcher.stocks_data:
                logger.debug(f"跳過 {stock_code}（無數據）")
                continue
            
            try:
                # 獲取股票數據
                df = self.fetcher.stocks_data[stock_code]
                today_data = self.fetcher.get_today_data(stock_code)
                
                if not today_data:
                    continue
                
                close_price = today_data['close']
                volume_shares = today_data['volume_shares']
                
                # 計算技術指標
                upper_band, middle_band, lower_band = self.analyzer.calculate_bollinger_bands(df)
                ema_values = self.analyzer.calculate_ema(df)
                
                if upper_band is None or ema_values is None:
                    logger.debug(f"無法計算 {stock_code} 的技術指標")
                    continue
                
                # 判斷 EMA 是否向上
                ema_trending_up = self.analyzer.is_ema_trending_up(ema_values)
                
                # 計算大戶持倉增加（這裡以成交量增加作為代理）
                yesterday_volume = self.fetcher.get_yesterday_volume(stock_code)
                volume_increase = volume_shares - yesterday_volume
                
                # 計算漲跌幅
                yesterday_close = df.iloc[-2]['close'] if len(df) > 1 else close_price
                price_change = self.analyzer.calculate_price_change(close_price, yesterday_close)
                
                # 檢查所有條件
                meets_conditions, condition_count, condition_details = FilterConditions.check_all_conditions(
                    stock_code=stock_code,
                    close_price=close_price,
                    upper_band=upper_band,
                    ema_up=ema_trending_up,
                    volume=volume_shares,
                    major_holder_increase=volume_increase
                )
                
                # 如果符合所有條件，添加到報表
                if meets_conditions:
                    stock_info = {
                        '股票代碼': stock_code,
                        '股票名稱': f"股票 {stock_code}",  # 實際應該從 API 獲取名稱
                        '收盤價': round(close_price, 2),
                        '布林上軌': round(upper_band, 2),
                        '布林中線': round(middle_band, 2),
                        '布林下軌': round(lower_band, 2),
                        '8均線': round(ema_values['today'], 2),
                        '成交量(張)': round(volume_shares, 0),
                        '大戶持倉增加(張)': round(volume_increase, 0),
                        '昨日成交量': round(yesterday_volume, 0),
                        '漲跌幅(%)': price_change,
                        '符合條件數': 4,  # 所有 4 個條件都符合
                    }
                    
                    self.report.add_filtered_stock(stock_info)
                    filtered_count += 1
                    
                    logger.info(f"✓ {stock_code} 符合所有條件")
                    for detail in condition_details:
                        logger.debug(f"    {detail}")
                
            except Exception as e:
                logger.error(f"過濾 {stock_code} 時出錯: {str(e)}", exc_info=True)
                continue
        
        logger.info(f"過濾完成，找到 {filtered_count} 檔符合條件的股票")
    
    def _generate_reports(self):
        """生成報表"""
        logger.info("生成報表...")
        
        # 保存 Excel 報表
        excel_file = self.report.save_excel_report()
        if excel_file:
            logger.info(f"✓ Excel 報表已生成: {excel_file}")
        
        # 保存 CSV 報表
        csv_file = self.report.save_csv_report()
        if csv_file:
            logger.info(f"✓ CSV 報表已生成: {csv_file}")
        
        # 在控制台打印摘要
        self.report.print_console_report()


def main():
    """主函數"""
    # 創建並運行過濾系統
    system = StockFilterSystem()
    success = system.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
