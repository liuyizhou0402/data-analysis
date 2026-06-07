"""
悉尼大学新生获客清单 — 配置中心
合规版：只爬取识别 + 生成话术草稿，发送由用户手动完成。
凭据从环境变量读取，绝不硬编码。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env
load_dotenv(Path(__file__).parent.parent / ".env")

# ---------------------------------------------------------------------------
# 目录布局
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
SEEN_USERS_FILE = DATA_DIR / "seen_users.json"
LOG_FILE = DATA_DIR / "scraper.log"

DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 爬取行为
# ---------------------------------------------------------------------------
USE_MOCK_DATA: bool = os.getenv("USYD_USE_MOCK", "true").lower() in ("1", "true", "yes")
XHS_COOKIE: str = os.getenv("XHS_COOKIE", "")

# 每日目标新生数量
TARGET_USER_COUNT: int = 20

REQUEST_DELAY_SECONDS: float = float(os.getenv("USYD_REQUEST_DELAY", "2.0"))
MAX_PAGES_PER_KEYWORD: int = int(os.getenv("USYD_MAX_PAGES", "3"))

# ---------------------------------------------------------------------------
# 搜索关键词（悉尼大学新生导向）
# ---------------------------------------------------------------------------
SEARCH_KEYWORDS: list[str] = [
    "悉尼大学新生",
    "悉大新生",
    "USYD新生",
    "悉尼大学offer",
    "悉大offer",
    "USYD offer",
    "悉尼大学26fall",
    "悉尼大学27fall",
    "悉大留学",
    "悉尼大学研究生",
    "悉尼大学本科",
    "USYD留学",
    "悉尼大学入学",
    "悉尼大学准新生",
    "悉大扩列",
]

# ---------------------------------------------------------------------------
# 新生识别信号（用于判断是否 2026/2027 入学）
# ---------------------------------------------------------------------------
# 入学年份信号
ENROLLMENT_YEAR_SIGNALS: list[str] = [
    "2026", "2027", "26fall", "27fall", "26 fall", "27 fall",
    "26春", "26秋", "27春", "27秋", "s1 2026", "s2 2026", "s1 2027", "s2 2027",
    "2026入学", "2027入学", "26入学", "27入学",
]

# 新生身份信号
FRESHMAN_SIGNALS: list[str] = [
    "新生", "准新生", "offer", "录取", "拿到offer", "上岸",
    "入学", "报到", "开学", "求扩列", "扩列", "找搭子",
    "蹲", "求组织", "新生群", "萌新", "小白",
]

# 悉大身份信号
USYD_SIGNALS: list[str] = [
    "悉尼大学", "悉大", "usyd", "university of sydney", "sydney uni",
    "悉尼", "sydney",
]

# ---------------------------------------------------------------------------
# 邮件配置
# ---------------------------------------------------------------------------
EMAIL_SENDER: str = os.getenv("XHS_EMAIL_USER", "")
EMAIL_PASSWORD: str = os.getenv("XHS_EMAIL_PASSWORD", "")
EMAIL_RECIPIENT: str = os.getenv("USYD_EMAIL_RECIPIENT", "1225265377@qq.com")

SMTP_HOST: str = "smtp.qq.com"
SMTP_PORT_SSL: int = 465
SMTP_PORT_STARTTLS: int = 587
SMTP_USE_SSL: bool = False  # 使用 STARTTLS 587 端口

# ---------------------------------------------------------------------------
# 你的微信号（用于生成话术草稿，仅出现在发给你自己的邮件里）
# ---------------------------------------------------------------------------
YOUR_WECHAT: str = os.getenv("USYD_WECHAT", "你的微信号")

# ---------------------------------------------------------------------------
# HTTP 头
# ---------------------------------------------------------------------------
DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.xiaohongshu.com/explore",
    "Origin": "https://www.xiaohongshu.com",
}

XHS_SEARCH_API: str = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
XHS_PROFILE_BASE: str = "https://www.xiaohongshu.com/user/profile"

# ---------------------------------------------------------------------------
# 调度配置
# ---------------------------------------------------------------------------
SCHEDULER_TIMEZONE: str = "Asia/Shanghai"
SCHEDULE_HOUR: int = int(os.getenv("USYD_SCHEDULE_HOUR", "9"))
SCHEDULE_MINUTE: int = int(os.getenv("USYD_SCHEDULE_MINUTE", "0"))
