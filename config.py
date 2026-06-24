# Configuration file for stock filter program
import os
from datetime import time

# ==================== Basic Settings ====================
# Data source
DATA_SOURCE = "Google Finance"
GOOGLE_FINANCE_URL = "https://www.google.com/finance/beta/"

# Taiwan electronics stock codes
ELECTRONICS_STOCKS = [
    "2330", "2454", "2412", "2357", "3008", "3034", "2303", "2308",
    "2382", "3711", "2409", "3036", "2379", "2344", "2388", "2395",
    "2353", "6669", "2360", "2364", "2368", "3014", "3231", "2367",
    "2397", "6605", "2436", "2337", "2348", "2342", "2347", "2417",
]

# ==================== Technical Indicator Settings ====================
# Bollinger Bands parameters
BOLLINGER_PERIOD = 20  # 20-day moving average
BOLLINGER_STD_DEV = 1.23  # 1.23x standard deviation
EMA_PERIOD = 8  # 8-day EMA

# ==================== Filter Conditions ====================
# Volume limit (unit: shares/1000)
MIN_VOLUME_SHARES = 1000

# Major holder threshold (unit: shares/1000)
MAJOR_HOLDER_THRESHOLD = 1000

# ==================== Time Settings ====================
# Taiwan stock market close time
MARKET_CLOSE_TIME = time(13, 30)  # 1:30 PM

# Daily execution time (after market close)
EXECUTION_TIME = time(14, 0)  # 2:00 PM

# ==================== Output Settings ====================
# Report output directory
REPORT_DIR = "reports"
OUTPUT_FORMAT = "xlsx"  # Support xlsx, csv

# Report columns
REPORT_COLUMNS = [
    "Stock Code",
    "Stock Name",
    "Close Price",
    "Bollinger Upper",
    "Bollinger Middle",
    "Bollinger Lower",
    "8-day EMA",
    "Volume (shares)",
    "Major Holder Increase (shares)",
    "Yesterday Volume",
    "Price Change (%)",
    "Matching Conditions",
]

# ==================== Logging Settings ====================
LOG_DIR = "logs"
LOG_LEVEL = "INFO"
