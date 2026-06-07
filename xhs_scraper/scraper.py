"""
XHS (Xiaohongshu) scraper.

Two modes:
  USE_MOCK_DATA=True  — returns realistic synthetic data for end-to-end testing.
  USE_MOCK_DATA=False — makes real HTTPS requests using the cookie provided in
                        config.XHS_COOKIE.  Requires a valid login session.
"""

from __future__ import annotations

import json
import logging
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------
UserDict = dict[str, Any]

# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

_MOCK_NICKNAMES_POOL = [
    "小明的留学日记", "Emily在英国", "悉尼打工人", "曼彻斯特求学记",
    "Chloe备考雅思", "墨尔本留学生", "牛津梦想家", "澳洲小留学生",
    "伦敦求职日记", "布里斯班生活录", "A-level奋斗史", "IB备考小分队",
    "托福满分攻略", "留学申请老手", "英澳双申请人", "悉尼大学在读",
    "伯明翰大学日常", "海外升学规划师", "国际课程小白鼠", "雅思7分不是梦",
    "Anna的留学故事", "Jack备考托福", "留学顾问小助手", "英国读研日记",
    "澳洲技术移民路", "曼城学生党", "墨大研究生", "皇家墨尔本日常",
    "南安普顿留学生", "爱丁堡大学Emily", "悉尼科技大David", "英国公立高中生",
    "华威大学商科生", "莫纳什大学Lily", "留学小白入门", "出国读书指南",
    "雅思6.5求经验", "英国本科录取帖", "澳洲读书省钱攻略", "IB38分上岸",
    "A-level备考tips", "国际学校家长群", "英澳直升班经验", "一年制硕士体验",
    "英国语言班日记", "布里斯班中学生", "珀斯生活指南", "阿德莱德求学录",
    "英国G5申请心得", "澳洲八大录取日",
]

_MOCK_BIO_SNIPPETS = [
    "正在备考雅思，目标7分，希望申请曼彻斯特大学",
    "A-level在读，计划申请英国TOP10大学",
    "澳洲留学两年，分享真实生活经验",
    "正在找留学顾问，求推荐靠谱机构",
    "IB课程最后一年，目标澳洲八大",
    "托福备考中，求学习搭子",
    "已拿到UCL offer，等待入学",
    "悉尼大学在读，欢迎留学咨询",
    "国际学校高一，开始规划留学",
    "英国本科+澳洲硕士双申中",
]

_MOCK_TITLES_POOL = [
    "分享我的英国留学申请经历",
    "雅思7分备考全攻略【干货】",
    "澳洲留学费用详细清单2024",
    "A-level选课指南，避开这些坑",
    "IB备考经验分享，从35到42",
    "英国大学排名解析，选校必看",
    "托福备考计划表，三个月提分",
    "留学顾问真的值得花钱吗？",
    "墨尔本生活成本大揭秘",
    "英国语言班性价比排行榜",
    "澳洲技术移民+留学双规划",
    "国际学校选择指南，家长必看",
    "英澳留学中介避坑指南",
    "留学申请文书怎么写？",
    "悉尼vs墨尔本，你选哪个？",
]


def _random_xhs_id() -> str:
    """Generate a fake but plausible XHS user/note ID (24 hex chars)."""
    return uuid.uuid4().hex[:24]


def _random_publish_time(within_days: int = 30) -> str:
    delta = random.randint(0, within_days * 24 * 3600)
    dt = datetime.now() - timedelta(seconds=delta)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _generate_mock_users(keyword: str, count: int = 10) -> list[UserDict]:
    """Return `count` synthetic user records for a given keyword."""
    users: list[UserDict] = []
    for _ in range(count):
        uid = _random_xhs_id()
        nickname = random.choice(_MOCK_NICKNAMES_POOL)
        users.append(
            {
                "user_id": uid,
                "nickname": nickname,
                "profile_url": f"{config.XHS_PROFILE_BASE}/{uid}",
                "bio": random.choice(_MOCK_BIO_SNIPPETS),
                "source_keyword": keyword,
                "match_reason": f'发布了与「{keyword}」相关的笔记',
                "discovered_date": datetime.now().strftime("%Y-%m-%d"),
                # Extra context fields (used by keyword_matcher)
                "recent_posts": [
                    {
                        "title": random.choice(_MOCK_TITLES_POOL),
                        "likes": random.randint(5, 3000),
                        "comments": random.randint(0, 500),
                        "publish_time": _random_publish_time(),
                    }
                    for _ in range(random.randint(1, 3))
                ],
            }
        )
    return users


# ---------------------------------------------------------------------------
# Real scraper helpers
# ---------------------------------------------------------------------------

def _build_session() -> requests.Session:
    """Create a requests.Session with retry logic and XHS headers."""
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update(config.DEFAULT_HEADERS)

    if config.XHS_COOKIE:
        session.headers["Cookie"] = config.XHS_COOKIE

    return session


def _parse_note(raw: dict[str, Any], keyword: str) -> UserDict | None:
    """Extract a user record from a raw note dict returned by the search API."""
    try:
        note_card = raw.get("note_card", raw)
        author = note_card.get("user", {})
        interact = note_card.get("interact_info", {})

        user_id = author.get("user_id") or author.get("userid", "")
        if not user_id:
            return None

        nickname = author.get("nickname", "未知用户")
        profile_url = f"{config.XHS_PROFILE_BASE}/{user_id}"

        likes = int(interact.get("liked_count", 0) or 0)
        comments = int(interact.get("comment_count", 0) or 0)

        note_id = raw.get("id") or note_card.get("note_id", "")
        title = note_card.get("title", "")
        desc = note_card.get("desc", "")
        publish_time = note_card.get("time", "") or note_card.get("publish_time", "")

        return {
            "user_id": user_id,
            "nickname": nickname,
            "profile_url": profile_url,
            "bio": "",
            "source_keyword": keyword,
            "match_reason": f'搜索关键词"{keyword}"命中笔记标题/内容',
            "discovered_date": datetime.now().strftime("%Y-%m-%d"),
            "recent_posts": [
                {
                    "title": title or desc[:50],
                    "likes": likes,
                    "comments": comments,
                    "publish_time": str(publish_time),
                    "note_id": note_id,
                }
            ],
        }
    except Exception as exc:
        logger.debug("Failed to parse note: %s — %s", raw, exc)
        return None


def _search_keyword(
    session: requests.Session,
    keyword: str,
    page: int = 1,
) -> list[dict[str, Any]]:
    """
    Call the XHS search API for a single keyword/page combination.
    Returns raw note dicts on success, empty list on failure.
    """
    params = {
        "keyword": keyword,
        "page": page,
        "page_size": 20,
        "sort": "general",
        "note_type": 0,
    }
    try:
        resp = session.get(
            config.XHS_SEARCH_API,
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        # XHS wraps results under data.items or data.notes depending on endpoint version
        items = (
            data.get("data", {}).get("items")
            or data.get("data", {}).get("notes")
            or []
        )
        logger.debug(
            "Keyword '%s' page %d: %d raw items", keyword, page, len(items)
        )
        return items
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        logger.warning(
            "HTTP %s on keyword '%s' page %d — may need fresh cookies",
            status, keyword, page,
        )
    except Exception as exc:
        logger.warning("Error searching keyword '%s': %s", keyword, exc)
    return []


def _fetch_comment_users(
    session: requests.Session,
    note_id: str,
    keyword: str,
) -> list[UserDict]:
    """
    Fetch first page of comments for a note and return commenters as user dicts.
    Commenters show active interest in the topic.
    """
    users: list[UserDict] = []
    try:
        params = {"note_id": note_id, "cursor": ""}
        resp = session.get(
            config.XHS_NOTE_COMMENTS_API,
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        comments = data.get("data", {}).get("comments", [])
        for c in comments:
            author = c.get("user_info", {})
            uid = author.get("user_id", "")
            if not uid:
                continue
            users.append(
                {
                    "user_id": uid,
                    "nickname": author.get("nickname", "未知用户"),
                    "profile_url": f"{config.XHS_PROFILE_BASE}/{uid}",
                    "bio": "",
                    "source_keyword": keyword,
                    "match_reason": f'评论了"{keyword}"相关笔记（主动互动，意向较强）',
                    "discovered_date": datetime.now().strftime("%Y-%m-%d"),
                    "recent_posts": [],
                }
            )
    except Exception as exc:
        logger.debug("Could not fetch comments for note %s: %s", note_id, exc)
    return users


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def scrape_users() -> list[UserDict]:
    """
    Main entry point.  Returns a list of user dicts across all keywords.
    Deduplication within a single run is handled here (by user_id); full
    historical deduplication is done by deduplicator.py.
    """
    if config.USE_MOCK_DATA:
        logger.info("USE_MOCK_DATA=True — generating synthetic data")
        return _scrape_mock()
    else:
        logger.info("USE_MOCK_DATA=False — using live XHS scraping")
        return _scrape_live()


def _scrape_mock() -> list[UserDict]:
    all_users: list[UserDict] = []
    seen_ids: set[str] = set()

    for keyword in config.SEARCH_KEYWORDS:
        batch = _generate_mock_users(keyword, count=random.randint(6, 12))
        for user in batch:
            if user["user_id"] not in seen_ids:
                seen_ids.add(user["user_id"])
                all_users.append(user)
        logger.debug("Mock: keyword '%s' → %d users", keyword, len(batch))

    logger.info("Mock scrape complete — %d unique users", len(all_users))
    return all_users


def _parse_cookies_string(cookie_str: str) -> list[dict]:
    """Convert a raw Cookie header string into a list of dicts for Playwright."""
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


def _scrape_live_playwright() -> list[UserDict]:
    """
    Use a headless Chromium browser (via Playwright) to search XHS.
    Injects the user's cookies so the page is fully authenticated and
    the JavaScript-generated security signatures are handled automatically.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("playwright not installed. Run: pip install playwright && playwright install chromium")
        return []

    if not config.XHS_COOKIE:
        logger.error("XHS_COOKIE is not set. Falling back to empty result.")
        return []

    all_users: list[UserDict] = []
    seen_ids: set[str] = set()
    cookies = _parse_cookies_string(config.XHS_COOKIE)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(
            user_agent=config.DEFAULT_HEADERS["User-Agent"],
            locale="zh-CN",
            viewport={"width": 1280, "height": 800},
        )
        # Inject cookies so we appear logged in
        context.add_cookies(cookies)
        page = context.new_page()

        # Intercept API responses to extract note/user data
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
                search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes"
                page.goto(search_url, timeout=30000, wait_until="networkidle")
                time.sleep(2)  # let JS finish rendering

                # Scroll to trigger more results
                for _ in range(2):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.5)

            except PWTimeout:
                logger.warning("Timeout loading search page for '%s'", keyword)
            except Exception as exc:
                logger.warning("Error navigating to '%s': %s", keyword, exc)

            # Parse captured API responses
            for item in captured:
                user = _parse_note(item, keyword)
                if user and user["user_id"] not in seen_ids:
                    seen_ids.add(user["user_id"])
                    keyword_users.append(user)

            # Fallback: parse visible note cards from the DOM
            if not keyword_users:
                try:
                    cards = page.query_selector_all("section.note-item, div[data-v-note-item]")
                    for card in cards[:20]:
                        try:
                            link = card.query_selector("a[href*='/user/profile/']")
                            if not link:
                                continue
                            href = link.get_attribute("href") or ""
                            uid = href.split("/user/profile/")[-1].split("?")[0].strip()
                            if not uid or uid in seen_ids:
                                continue
                            seen_ids.add(uid)
                            nickname_el = card.query_selector(".author-wrapper .name, .nickname, span.name")
                            nickname = nickname_el.inner_text().strip() if nickname_el else "未知用户"
                            title_el = card.query_selector(".title, .note-title, a.title")
                            title = title_el.inner_text().strip() if title_el else ""
                            keyword_users.append({
                                "user_id": uid,
                                "nickname": nickname,
                                "profile_url": f"{config.XHS_PROFILE_BASE}/{uid}",
                                "bio": "",
                                "source_keyword": keyword,
                                "match_reason": f'搜索关键词「{keyword}」发现笔记作者',
                                "discovered_date": datetime.now().strftime("%Y-%m-%d"),
                                "recent_posts": [{"title": title, "likes": 0, "comments": 0, "publish_time": ""}],
                            })
                        except Exception:
                            continue
                except Exception as exc:
                    logger.debug("DOM fallback failed for '%s': %s", keyword, exc)

            all_users.extend(keyword_users)
            logger.info("Live: keyword '%s' → %d new users (total: %d)", keyword, len(keyword_users), len(all_users))
            time.sleep(config.REQUEST_DELAY_SECONDS)

            if len(all_users) >= config.TARGET_USER_COUNT * 3:
                logger.info("Reached early-stop threshold; skipping remaining keywords")
                break

        browser.close()

    logger.info("Playwright scrape complete — %d unique users", len(all_users))
    return all_users


def _scrape_live() -> list[UserDict]:
    if not config.XHS_COOKIE:
        logger.error(
            "XHS_COOKIE is not set. Set it via the XHS_COOKIE env var or "
            "config.XHS_COOKIE.  Falling back to empty result."
        )
        return []

    return _scrape_live_playwright()
            break

    logger.info("Live scrape complete — %d unique users", len(all_users))
    return all_users
