# 技術分析模組
import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple
import config

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """技術指標計算"""
    
    @staticmethod
    def calculate_bollinger_bands(
        df: pd.DataFrame,
        period: int = config.BOLLINGER_PERIOD,
        std_dev: float = config.BOLLINGER_STD_DEV
    ) -> Tuple[float, float, float]:
        """
        計算布林通道
        
        Args:
            df: 股票數據 DataFrame
            period: 均線週期
            std_dev: 標準差倍數
            
        Returns:
            (上軌, 中線, 下軌)
        """
        try:
            if len(df) < period:
                logger.warning(f"數據不足，無法計算布林通道（需要{period}筆）")
                return None, None, None
            
            # 計算 SMA（20日均線）
            sma = df['close'].rolling(window=period).mean().iloc[-1]
            
            # 計算標準差
            std = df['close'].rolling(window=period).std().iloc[-1]
            
            # 計算布林通道
            upper_band = sma + (std_dev * std)  # 上軌
            middle_band = sma  # 中線（20均線）
            lower_band = sma - (std_dev * std)  # 下軌
            
            logger.debug(f"布林通道 - 上軌: {upper_band:.2f}, 中線: {middle_band:.2f}, 下軌: {lower_band:.2f}")
            
            return upper_band, middle_band, lower_band
            
        except Exception as e:
            logger.error(f"計算布林通道時出錯: {str(e)}")
            return None, None, None
    
    @staticmethod
    def calculate_ema(df: pd.DataFrame, period: int = config.EMA_PERIOD) -> float:
        """
        計算指數移動平均線（EMA）
        
        Args:
            df: 股票數據 DataFrame
            period: EMA 週期
            
        Returns:
            今日 EMA 值
        """
        try:
            if len(df) < period:
                logger.warning(f"數據不足，無法計算 EMA（需要{period}筆）")
                return None
            
            ema = df['close'].ewm(span=period, adjust=False).mean()
            today_ema = ema.iloc[-1]
            yesterday_ema = ema.iloc[-2] if len(ema) > 1 else today_ema
            
            logger.debug(f"今日EMA: {today_ema:.2f}, 昨日EMA: {yesterday_ema:.2f}")
            
            return {
                'today': today_ema,
                'yesterday': yesterday_ema,
            }
            
        except Exception as e:
            logger.error(f"計算 EMA 時出錯: {str(e)}")
            return None
    
    @staticmethod
    def is_ema_trending_up(ema_dict: Dict) -> bool:
        """
        判斷 EMA 是否向上
        
        Args:
            ema_dict: 包含 today 和 yesterday 的 EMA 字典
            
        Returns:
            是否向上
        """
        if ema_dict is None:
            return False
        
        is_up = ema_dict['today'] > ema_dict['yesterday']
        logger.debug(f"EMA 向上: {is_up}")
        return is_up
    
    @staticmethod
    def calculate_price_change(close_today: float, close_yesterday: float) -> float:
        """
        計算漲跌幅百分比
        
        Args:
            close_today: 今日收盤價
            close_yesterday: 昨日收盤價
            
        Returns:
            漲跌幅百分比
        """
        try:
            if close_yesterday == 0:
                return 0
            
            change_percent = ((close_today - close_yesterday) / close_yesterday) * 100
            return round(change_percent, 2)
            
        except Exception as e:
            logger.error(f"計算漲跌幅時出錯: {str(e)}")
            return 0


class FilterConditions:
    """股票過濾條件"""
    
    @staticmethod
    def check_all_conditions(
        stock_code: str,
        close_price: float,
        upper_band: float,
        ema_up: bool,
        volume: float,
        major_holder_increase: float
    ) -> Tuple[bool, int, list]:
        """
        檢查所有過濾條件
        
        Args:
            stock_code: 股票代碼
            close_price: 收盤價
            upper_band: 布林上軌
            ema_up: 8均線是否向上
            volume: 成交量（張）
            major_holder_increase: 大戶持倉增加（張）
            
        Returns:
            (是否符合所有條件, 符合條件數, 條件詳情列表)
        """
        conditions = []
        met_count = 0
        
        # 條件1: 成交量 > 1000張
        volume_ok = volume > config.MIN_VOLUME_SHARES
        conditions.append(f"成交量({volume:.0f}張) > 1000張: {volume_ok}")
        if volume_ok:
            met_count += 1
        
        # 條件2: 收盤價 > 布林上軌
        price_above_upper = close_price > upper_band
        conditions.append(f"收盤價({close_price:.2f}) > 上軌({upper_band:.2f}): {price_above_upper}")
        if price_above_upper:
            met_count += 1
        
        # 條件3: 8均線向上
        ema_trend_ok = ema_up
        conditions.append(f"8均線向上: {ema_trend_ok}")
        if ema_trend_ok:
            met_count += 1
        
        # 條件4: 大戶持倉增加 > 1000張
        major_holder_ok = major_holder_increase > config.MAJOR_HOLDER_THRESHOLD
        conditions.append(f"大戶持倉增加({major_holder_increase:.0f}張) > 1000張: {major_holder_ok}")
        if major_holder_ok:
            met_count += 1
        
        # 所有條件都需滿足
        all_conditions_met = all([volume_ok, price_above_upper, ema_trend_ok, major_holder_ok])
        
        logger.info(f"股票 {stock_code} - 符合 {met_count}/4 個條件")
        for cond in conditions:
            logger.debug(f"  {cond}")
        
        return all_conditions_met, met_count, conditions
