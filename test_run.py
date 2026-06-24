# 測試腳本 - 運行一次過濾並生成報表
import sys
import os

# 確保可以導入模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from datetime import datetime
from stock_filter import StockFilterSystem

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_run():
    """運行一次測試過濾"""
    logger.info("="*100)
    logger.info("台灣股票過濾程式 - 測試運行")
    logger.info(f"開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*100)
    
    try:
        # 建立並運行過濾系統
        system = StockFilterSystem()
        success = system.run()
        
        if success:
            logger.info("\n✓ 測試運行成功")
            logger.info("✓ 報表已生成在 reports/ 目錄")
            logger.info("✓ 日誌已保存在 logs/ 目錄")
            return 0
        else:
            logger.error("\n✗ 測試運行失敗")
            return 1
            
    except Exception as e:
        logger.error(f"\n✗ 測試過程中發生錯誤: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = test_run()
    sys.exit(exit_code)
