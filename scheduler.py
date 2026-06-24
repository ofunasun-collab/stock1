# 定時執行器 - 每日收盤後自動執行
import logging
import time
from datetime import datetime, time as dt_time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import config
from stock_filter import StockFilterSystem

logger = logging.getLogger(__name__)

class StockFilterScheduler:
    """定時執行台灣股票過濾系統"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def start(self):
        """啟動定時排程"""
        try:
            # 設置每個交易日下午2:00執行
            # 星期一到星期五，14:00執行
            self.scheduler.add_job(
                self._run_filter,
                CronTrigger(day_of_week='0-4', hour=14, minute=0),
                id='stock_filter_job',
                name='台灣電子股過濾',
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            
            logger.info("✓ 定時排程已啟動")
            logger.info("  執行時間: 每個交易日 下午 2:00")
            logger.info("  工作名稱: 台灣電子股過濾")
            
        except Exception as e:
            logger.error(f"啟動定時排程失敗: {str(e)}")
    
    def stop(self):
        """停止定時排程"""
        try:
            if self.is_running:
                self.scheduler.shutdown()
                self.is_running = False
                logger.info("✓ 定時排程已停止")
        except Exception as e:
            logger.error(f"停止定時排程失敗: {str(e)}")
    
    def _run_filter(self):
        """執行過濾程式"""
        logger.info("="*80)
        logger.info(f"定時執行: 台灣股票過濾系統 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*80)
        
        try:
            system = StockFilterSystem()
            success = system.run()
            
            if success:
                logger.info("✓ 定時執行成功")
            else:
                logger.error("✗ 定時執行失敗")
                
        except Exception as e:
            logger.error(f"執行過程中發生錯誤: {str(e)}", exc_info=True)
    
    def run_once(self):
        """立即執行一次（用於測試）"""
        logger.info("手動執行過濾程式...")
        self._run_filter()
    
    def keep_alive(self):
        """保持程式運行"""
        try:
            logger.info("定時排程已啟動，按 Ctrl+C 退出")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n收到中斷信號")
            self.stop()


def main():
    """主函數"""
    scheduler = StockFilterScheduler()
    scheduler.start()
    scheduler.keep_alive()


if __name__ == "__main__":
    main()
