"""
悉尼大学新生爬虫。
复用 Playwright 真实浏览器方案，绕过小红书 JS 签名。
捕获笔记标题 + 正文摘要，用于后续新生识别和话术生成。
"""

from __future__ import annotations

import logging
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Any

import config

logger = logging.getLogger(__name__)

UserDict = dict[str, Any]

# ---------------------------------------------------------------------------
# Mock 数据（无 Cookie 时端到端测试用）
# ---------------------------------------------------------------------------

_MOCK_NICKNAMES = [
    "悉大26fall新生", "USYD准研究生", "悉尼大学上岸啦", "Emily的悉大日记",
    "悉大商科萌新", "蹲一个悉大新生群", "27fall悉尼大学", "悉大IT研究生",
    "悉尼留学小白", "USYD求扩列", "悉大新生求搭子", "拿到悉大offer啦",
    "悉尼大学传媒研究生", "悉大金融26fall", "Sydney新生报到", "悉大教育学准新生",
    "悉尼大学法学院", "悉大建筑26入学", "USYD护理新生", "悉尼大学求组织",
]

_MOCK_BIOS = [
    "悉大26fall商科研究生，求扩列求搭子！",
    "拿到USYD offer啦，2026 S1入学，蹲新生群",
    "悉尼大学27fall准新生，IT专业，求组织",
    "悉大金融研究生在读，2026入学，分享留学日常",
    "USYD传媒26fall，悉尼租房求搭子",
    "悉尼大学教育学准新生，2027春季入学",
    "悉大法学院26fall，求悉尼新生扩列",
    "刚上岸悉尼大学，护理专业，2026开学",
]

_MOCK_TITLES = [
    "悉大26fall offer分享｜商科研究生申请经验",
    "USYD租房避雷｜悉尼新生必看",
    "悉尼大学27fall｜准新生求扩列",
    "拿到悉大offer的那一刻｜留学申请记录",
    "悉大新生报到流程｜2026入学攻略",
    "悉尼大学选课指南｜26fall新生",
    "USYD宿舍vs租房｜新生怎么选",
    "悉大留学一年花费｜真实账单",
]


def _rand_id() -> str:
    return uuid.uuid4().hex[:24]


def _generate_mock(keyword: str, n: int) -> list[UserDict]:
    users = []
    for _ in range(n):
        uid = _rand_id()
        bio = random.choice(_MOCK_BIOS)
        title = random.choice(_MOCK_TITLES)
        users.append({
            "user_id": uid,
            "nickname": random.choice(_MOCK_NICKNAMES),
            "profile_url": f"{config.XHS_PROFILE_BASE}/{uid}",
            "bio": bio,
            "source_keyword": keyword,
            "discovered_date": datetime.now().strftime("%Y-%m-%d"),
            "recent_posts": [{
                "title": title,
                "desc": bio,
                "likes": random.randint(5, 800),
                "comments": random.randint(0, 120),
                "publish_time": (datetime.now() - timedelta(days=random.randint(0, 20))).strftime("%Y-%m-%d %H:%M:%S"),
            }],
        })
    return users


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

def _parse_note(raw: dict[str, Any], keyword: str) -> UserDict | None:
    try:
        note_card = raw.get("note_card", raw)
        author = note_card.get("user", {})
        interact = note_card.get("interact_info", {})

        user_id = author.get("user_id") or author.get("userid", "")
        if not user_id:
            return None

        title = note_card.get("display_title", "") or note_card.get("title", "")
        desc = note_card.get("desc", "")

        return {
            "user_id": user_id,
            "nickname": author.get("nickname", "未知用户"),
            "profile_url": f"{config.XHS_PROFILE_BASE}/{user_id}",
            "bio": desc[:100],
            "source_keyword": keyword,
            "discovered_date": datetime.now().strftime("%Y-%m-%d"),
            "recent_posts": [{
                "title": title,
                "desc": desc,
                "likes": int(interact.get("liked_count", 0) or 0),
                "comments": int(interact.get("comment_count", 0) or 0),
                "publish_time": str(note_card.get("time", "")),
            }],
        }
    except Exception as exc:
        logger.debug("解析笔记失败: %s", exc)
        return None


def _parse_cookies(cookie_str: str) -> list[dict]:
    cookies = []
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            name, _, value = part.partition("=")
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": ".xiaohongshu.com",
                "path": "/",
            })
    return cookies


# ---------------------------------------------------------------------------
# 公开入口
# ---------------------------------------------------------------------------

def scrape_users() -> list[UserDict]:
    if config.USE_MOCK_DATA:
        logger.info("USE_MOCK_DATA=True — 生成测试数据")
        return _scrape_mock()
    logger.info("USE_MOCK_DATA=False — 使用 Playwright 真实爬取")
    return _scrape_live()


def _scrape_mock() -> list[UserDict]:
    all_users, seen = [], set()
    for kw in config.SEARCH_KEYWORDS:
        for u in _generate_mock(kw, random.randint(3, 8)):
            if u["user_id"] not in seen:
                seen.add(u["user_id"])
                all_users.append(u)
    logger.info("Mock 爬取完成 — %d 个用户", len(all_users))
    return all_users


def _scrape_live() -> list[UserDict]:
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("playwright 未安装。运行: pip install playwright && playwright install chromium")
        return []

    if not config.XHS_COOKIE:
        logger.error("XHS_COOKIE 未设置，返回空结果")
        return []

    all_users: list[UserDict] = []
    seen_ids: set[str] = set()
    cookies = _parse_cookies(config.XHS_COOKIE)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(
            user_agent=config.DEFAULT_HEADERS["User-Agent"],
            locale="zh-CN",
            viewport={"width": 1280, "height": 800},
        )
        context.add_cookies(cookies)
        page = context.new_page()

        captured: list[dict] = []

        def on_response(response):
            try:
                if "search/notes" in response.url and response.status == 200:
                    data = response.json()
                    items = (
                        data.get("data", {}).get("items")
                        or data.get("data", {}).get("notes")
                        or []
                    )
                    captured.extend(items)
            except Exception:
                pass

        page.on("response", on_response)

        for keyword in config.SEARCH_KEYWORDS:
            captured.clear()
            keyword_users: list[UserDict] = []

            try:
                url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes"
                page.goto(url, timeout=30000, wait_until="networkidle")
                time.sleep(2)
                for _ in range(2):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.5)
            except PWTimeout:
                logger.warning("加载搜索页超时: '%s'", keyword)
            except Exception as exc:
                logger.warning("导航到 '%s' 出错: %s", keyword, exc)

            for item in captured:
                u = _parse_note(item, keyword)
                if u and u["user_id"] not in seen_ids:
                    seen_ids.add(u["user_id"])
                    keyword_users.append(u)

            all_users.extend(keyword_users)
            logger.info("Live: 关键词 '%s' → %d 个新用户 (累计: %d)", keyword, len(keyword_users), len(all_users))
            time.sleep(config.REQUEST_DELAY_SECONDS)

            if len(all_users) >= config.TARGET_USER_COUNT * 4:
                logger.info("达到早停阈值，跳过剩余关键词")
                break

        browser.close()

    logger.info("Playwright 爬取完成 — %d 个唯一用户", len(all_users))
    return all_users
