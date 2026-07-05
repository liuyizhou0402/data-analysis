from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── 路径 ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
SEEN_FILE = DATA_DIR / "seen_posts.json"
LOG_FILE = DATA_DIR / "scraper.log"

for _d in (DATA_DIR, REPORTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── 邮件 ──────────────────────────────────────────────
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 587
SMTP_USE_SSL = False
EMAIL_USER = os.getenv("TUTOR_EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("TUTOR_EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("TUTOR_EMAIL_RECIPIENT", "1225265377@qq.com")

# ── 目标 ──────────────────────────────────────────────
TARGET_COUNT = 15          # 每日目标帖子数

# ── 价格过滤（低于此时薪视为低端，跳过）──────────────
MIN_HOURLY = 40            # AUD/hr，低于此的跳过
PRICE_SKIP_KEYWORDS = [
    "15/hr", "20/hr", "25/hr", "30/hr", "$15", "$20", "$25", "$30",
    "15 per hour", "20 per hour", "25 per hour", "30 per hour",
    "15元", "20元", "25元", "30元",
]

# ── 高端信号关键词（加分）────────────────────────────
PREMIUM_SIGNALS = [
    "hsc", "atar", "selective", "gifted", "scholarship",
    "ib", "international baccalaureate",
    "university", "uni", "umat", "gamsat",
    "high school", "year 11", "year 12",
    "精英", "奖学金", "竞赛", "高薪", "优厚",
    "hsc辅导", "名校", "私立", "selective school",
    "tutoring", "private tutor", "一对一", "私教",
    "$50", "$60", "$70", "$80", "$90", "$100",
    "50/hr", "60/hr", "70/hr", "80/hr", "90/hr", "100/hr",
    "50 per hour", "60 per hour", "70 per hour", "80 per hour",
]

# ── 目标关键词（搜索用）──────────────────────────────
SEARCH_KEYWORDS_ZH = [
    "悉尼 家教", "悉尼 补习", "Sydney tutor", "找家教 悉尼",
    "家教 悉尼 招聘", "补课 悉尼", "家教老师 悉尼",
    "找辅导 悉尼", "数学家教 悉尼", "英语家教 悉尼",
    "悉尼 一对一辅导",
]

SEARCH_KEYWORDS_EN = [
    "tutor wanted Sydney", "private tutor Sydney",
    "home tutor Sydney", "tutoring Sydney",
    "HSC tutor Sydney", "maths tutor Sydney",
]

# ── 排除词（广告/中介帖，不是需求帖）────────────────
EXCLUDE_KEYWORDS = [
    "我是家教", "本人提供", "offering tutoring", "i am a tutor",
    "tutor available", "hire me", "experienced tutor offering",
]

# ── 定时 ─────────────────────────────────────────────
SCHEDULE_HOUR = 9
SCHEDULE_MINUTE = 0
SCHEDULER_TIMEZONE = "Asia/Shanghai"

# ── Mock ─────────────────────────────────────────────
USE_MOCK_DATA = os.getenv("TUTOR_USE_MOCK", "true").lower() == "true"
