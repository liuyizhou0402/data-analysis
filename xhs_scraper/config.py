"""
Central configuration for the XHS Study Abroad Scraper.
Sensitive credentials are read from environment variables — never hardcode them here.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
SEEN_USERS_FILE = DATA_DIR / "seen_users.json"
LOG_FILE = DATA_DIR / "scraper.log"

# Ensure directories exist at import time
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Scraping behaviour
# ---------------------------------------------------------------------------

# Set to True to use the built-in mock-data generator instead of live HTTP
# requests. Useful for CI, local testing, or when you don't have valid cookies.
USE_MOCK_DATA: bool = os.getenv("XHS_USE_MOCK", "true").lower() in ("1", "true", "yes")

# Paste your full XHS cookie string here (or via env var) when USE_MOCK_DATA=False.
# Obtain it by logging in at https://www.xiaohongshu.com and copying from DevTools.
XHS_COOKIE: str = os.getenv("XHS_COOKIE", "")

# How many unique new users to collect per daily run (soft target)
TARGET_USER_COUNT: int = 50

# Seconds to wait between keyword searches to be polite to the server
REQUEST_DELAY_SECONDS: float = float(os.getenv("XHS_REQUEST_DELAY", "2.0"))

# Maximum pages to fetch per keyword (each page ≈ 20 notes)
MAX_PAGES_PER_KEYWORD: int = int(os.getenv("XHS_MAX_PAGES", "3"))

# ---------------------------------------------------------------------------
# Search keywords (Simplified Chinese)
# ---------------------------------------------------------------------------
SEARCH_KEYWORDS: list[str] = [
    "英国留学",
    "澳洲留学",
    "英澳留学",
    "国际课程",
    "A-level辅导",
    "IB辅导",
    "雅思备考",
    "托福备考",
    "留学申请",
    "海外升学",
    "英国大学",
    "澳大利亚大学",
    "国际学校",
    "留学顾问",
    "出国留学",
]

# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------
EMAIL_SENDER: str = os.getenv("XHS_EMAIL_USER", "")
EMAIL_PASSWORD: str = os.getenv("XHS_EMAIL_PASSWORD", "")
EMAIL_RECIPIENT: str = "1225265377@qq.com"

SMTP_HOST: str = "smtp.qq.com"
SMTP_PORT_SSL: int = 465       # SSL
SMTP_PORT_STARTTLS: int = 587  # STARTTLS (fallback)
SMTP_USE_SSL: bool = True      # prefer SSL; set False to try STARTTLS

# ---------------------------------------------------------------------------
# HTTP headers used for real scraping
# ---------------------------------------------------------------------------
DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.xiaohongshu.com/explore",
    "Origin": "https://www.xiaohongshu.com",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

# XHS API endpoints
XHS_EXPLORE_URL: str = "https://www.xiaohongshu.com/explore"
XHS_SEARCH_API: str = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
XHS_NOTE_COMMENTS_API: str = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/list"
XHS_PROFILE_BASE: str = "https://www.xiaohongshu.com/user/profile"

# ---------------------------------------------------------------------------
# Scheduler configuration
# ---------------------------------------------------------------------------
SCHEDULER_TIMEZONE: str = "Asia/Shanghai"
SCHEDULE_HOUR: int = int(os.getenv("SCHEDULE_HOUR", "9"))
SCHEDULE_MINUTE: int = int(os.getenv("SCHEDULE_MINUTE", "0"))
