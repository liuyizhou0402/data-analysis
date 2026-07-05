"""
多平台爬虫：Gumtree / Seek / 今日澳洲
用 requests + BS4 直接爬（比 Playwright 更难被屏蔽）。
"""
from __future__ import annotations

import logging
import random
import re
import time
from datetime import datetime
from typing import Any

import config

logger = logging.getLogger(__name__)

# ── 请求头（模拟真实浏览器）─────────────────────────────────────────────────
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

# ── Mock 数据 ─────────────────────────────────────────────────────────────────
MOCK_POSTS = [
    {
        "id": "gumtree_001",
        "source": "Gumtree",
        "title": "Wanted: HSC Maths Tutor - $80-100/hr - North Shore",
        "content": "Looking for experienced HSC maths tutor for Year 12 student. North Shore area. Budget $80-100/hr. Must have own HSC experience or teaching degree. Selective school student targeting 99+ ATAR.",
        "url": "https://www.gumtree.com.au/s-ad/xxx",
        "location": "North Shore, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$80-100/hr",
        "score": 95,
    },
    {
        "id": "gumtree_002",
        "source": "Gumtree",
        "title": "IB Tutor Needed - Chemistry & Maths HL - $90/hr",
        "content": "Seeking IB tutor for Chemistry and Maths HL. Student currently in Year 12 IB programme. Eastern Suburbs. $90/hr negotiable for right candidate.",
        "url": "https://www.gumtree.com.au/s-ad/yyy",
        "location": "Eastern Suburbs, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$90/hr",
        "score": 92,
    },
    {
        "id": "seek_003",
        "source": "Seek",
        "title": "Private Tutor - HSC English & History - $75-85/hr",
        "content": "Tutoring company seeking experienced HSC English and History tutors. $75-85/hr. Must have university degree and strong HSC results.",
        "url": "https://www.seek.com.au/job/xxx",
        "location": "Sydney CBD",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Apply via Seek",
        "price_signal": "$75-85/hr",
        "score": 88,
    },
    {
        "id": "gumtree_004",
        "source": "Gumtree",
        "title": "Scholarship Exam Tutor - Year 6 - $75/hr - Mosman",
        "content": "Looking for tutor to prepare Year 6 daughter for scholarship exams (AAS/ACER). Mosman area. $75/hr, 2 sessions per week. Must have scholarship exam experience.",
        "url": "https://www.gumtree.com.au/s-ad/bbb",
        "location": "Mosman, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$75/hr",
        "score": 85,
    },
    {
        "id": "seek_005",
        "source": "Seek",
        "title": "University Level Maths Tutor - UNSW/USyd - $70/hr",
        "content": "Seeking experienced university maths tutor. UNSW or USyd campus. $70/hr. Flexible hours. Strong mathematics background required.",
        "url": "https://www.seek.com.au/job/yyy",
        "location": "Sydney Universities",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Apply via Seek",
        "price_signal": "$70/hr",
        "score": 82,
    },
    {
        "id": "gumtree_006",
        "source": "Gumtree",
        "title": "Selective School Prep Tutor Wanted - $65/hr - Chatswood",
        "content": "Year 5 child needs selective school preparation. Maths and English. Chatswood area. $65/hr, 2x per week. Please reply with your qualifications.",
        "url": "https://www.gumtree.com.au/s-ad/ccc",
        "location": "Chatswood, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$65/hr",
        "score": 80,
    },
    {
        "id": "seek_007",
        "source": "Seek",
        "title": "Senior HSC Tutor - Multiple Subjects - $60-90/hr",
        "content": "Growing tutoring centre seeking senior HSC tutors across multiple subjects. $60-90/hr depending on experience. Must have strong ATAR and tutoring background.",
        "url": "https://www.seek.com.au/job/zzz",
        "location": "North Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Apply via Seek",
        "price_signal": "$60-90/hr",
        "score": 83,
    },
    {
        "id": "gumtree_008",
        "source": "Gumtree",
        "title": "Piano + Academic Tutor Wanted - $70/hr - CBD",
        "content": "Seeking versatile tutor for piano and primary school academics. CBD location. $70/hr. Private school student.",
        "url": "https://www.gumtree.com.au/s-ad/ddd",
        "location": "CBD, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$70/hr",
        "score": 78,
    },
]


# ── requests 爬虫 ─────────────────────────────────────────────────────────────

def _get(url: str, session, timeout: int = 20) -> "requests.Response | None":
    try:
        resp = session.get(url, headers=_HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return resp
        logger.warning("HTTP %d: %s", resp.status_code, url)
    except Exception as e:
        logger.warning("请求失败 (%s): %s", url, e)
    return None


def _scrape_gumtree_requests(session) -> list[dict]:
    """用 requests 爬 Gumtree 家教分类（悉尼）"""
    from bs4 import BeautifulSoup
    posts = []
    urls = [
        "https://www.gumtree.com.au/s-tutoring-lessons/sydney/k0c18320l3004532?sort=date",
        "https://www.gumtree.com.au/s-tutoring-lessons/new-south-wales/k0c18320?sort=date",
    ]
    for url in urls:
        resp = _get(url, session)
        if not resp:
            continue
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            # Gumtree 列表项
            items = (
                soup.select("article.user-ad-row") or
                soup.select("li.user-ad-row") or
                soup.select("[data-q='search-result']") or
                soup.select(".listing-results article")
            )
            for item in items[:25]:
                try:
                    title_el = (
                        item.select_one("a[data-q='listing-title']") or
                        item.select_one(".user-ad-row-new-design__title-span") or
                        item.select_one("h2 a") or
                        item.select_one("a.user-ad-row__title")
                    )
                    link_el = item.select_one("a[href*='/s-ad/']") or item.select_one("a[href]")
                    price_el = (
                        item.select_one("[data-q='listing-price']") or
                        item.select_one(".user-ad-row-new-design__price") or
                        item.select_one(".listing-price")
                    )
                    desc_el = (
                        item.select_one("[data-q='listing-description']") or
                        item.select_one(".user-ad-row-new-design__description")
                    )
                    loc_el = (
                        item.select_one("[data-q='listing-location']") or
                        item.select_one(".user-ad-row-new-design__location")
                    )

                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title:
                        continue
                    href = (link_el.get("href") or "") if link_el else ""
                    full_url = f"https://www.gumtree.com.au{href}" if href.startswith("/") else href
                    price = price_el.get_text(strip=True) if price_el else ""
                    desc = desc_el.get_text(strip=True) if desc_el else ""
                    location = loc_el.get_text(strip=True) if loc_el else "Sydney"

                    posts.append({
                        "id": f"gumtree_{abs(hash(href or title))}",
                        "source": "Gumtree",
                        "title": title[:150],
                        "content": desc[:400],
                        "url": full_url,
                        "location": location,
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在 Gumtree 上回复帖子",
                        "price_signal": price,
                        "score": 0,
                    })
                except Exception:
                    continue

            if posts:
                break
        except Exception as e:
            logger.warning("Gumtree 解析失败: %s", e)

    logger.info("Gumtree: %d 条", len(posts))
    return posts


def _scrape_seek_requests(session) -> list[dict]:
    """用 requests 爬 Seek 家教职位（悉尼）"""
    from bs4 import BeautifulSoup
    posts = []
    urls = [
        "https://www.seek.com.au/tutoring-jobs/in-Sydney-NSW",
        "https://www.seek.com.au/tutor-jobs/in-Sydney-NSW-2000",
    ]
    for url in urls:
        resp = _get(url, session)
        if not resp:
            continue
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            items = (
                soup.select("article[data-automation='normalJob']") or
                soup.select("article") or
                soup.select("[data-automation='job-card']")
            )
            for item in items[:20]:
                try:
                    title_el = (
                        item.select_one("[data-automation='jobTitle']") or
                        item.select_one("h3 a") or
                        item.select_one("h2 a")
                    )
                    link_el = item.select_one("a[href*='/job/']") or item.select_one("a[href]")
                    salary_el = (
                        item.select_one("[data-automation='jobSalary']") or
                        item.select_one(".jobSalary")
                    )
                    loc_el = item.select_one("[data-automation='jobLocation']")
                    desc_el = item.select_one("[data-automation='jobShortDescription']")

                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title:
                        continue
                    href = (link_el.get("href") or "") if link_el else ""
                    full_url = f"https://www.seek.com.au{href}" if href.startswith("/") else href
                    salary = salary_el.get_text(strip=True) if salary_el else ""
                    location = loc_el.get_text(strip=True) if loc_el else "Sydney"
                    desc = desc_el.get_text(strip=True) if desc_el else ""

                    posts.append({
                        "id": f"seek_{abs(hash(href or title))}",
                        "source": "Seek",
                        "title": title[:150],
                        "content": desc[:400],
                        "url": full_url,
                        "location": location,
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在 Seek 上直接申请",
                        "price_signal": salary,
                        "score": 0,
                    })
                except Exception:
                    continue

            if posts:
                break
        except Exception as e:
            logger.warning("Seek 解析失败: %s", e)

    logger.info("Seek: %d 条", len(posts))
    return posts


def _scrape_jraus_requests(session) -> list[dict]:
    """用 requests 爬今日澳洲论坛（家教相关）"""
    from bs4 import BeautifulSoup
    posts = []
    search_queries = ["家教", "补习 tutor", "辅导 悉尼"]
    for q in search_queries:
        import urllib.parse
        url = f"https://www.jraus.com/search?q={urllib.parse.quote(q)}&expanded=true"
        resp = _get(url, session)
        if not resp:
            continue
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            # Discourse 论坛格式
            items = (
                soup.select(".search-result-topic") or
                soup.select(".fps-topic") or
                soup.select("article.topic-list-item") or
                soup.select(".topic-list-item")
            )
            for item in items[:15]:
                try:
                    title_el = item.select_one("a.search-link") or item.select_one("a[href*='/t/']") or item.select_one("a")
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    href = title_el.get("href", "")
                    full_url = f"https://www.jraus.com{href}" if href.startswith("/") else href
                    if not title or len(title) < 3:
                        continue

                    posts.append({
                        "id": f"jraus_{abs(hash(href or title))}",
                        "source": "今日澳洲",
                        "title": title[:150],
                        "content": "",
                        "url": full_url,
                        "location": "悉尼",
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在今日澳洲论坛回复帖子",
                        "price_signal": "",
                        "score": 0,
                    })
                except Exception:
                    continue
        except Exception as e:
            logger.warning("今日澳洲解析失败 (%s): %s", q, e)
        time.sleep(1)

    logger.info("今日澳洲: %d 条", len(posts))
    return posts


# ── 入口 ──────────────────────────────────────────────────────────────────────

def scrape_posts() -> list[dict]:
    if config.USE_MOCK_DATA:
        logger.info("USE_MOCK_DATA=True — 生成测试数据")
        mock = MOCK_POSTS.copy()
        random.shuffle(mock)
        logger.info("Mock 爬取完成 — %d 条帖子", len(mock))
        return mock

    import requests as req_lib

    session = req_lib.Session()
    session.headers.update(_HEADERS)

    all_posts: list[dict] = []

    logger.info("爬取 Gumtree...")
    all_posts.extend(_scrape_gumtree_requests(session))
    time.sleep(2)

    logger.info("爬取 Seek...")
    all_posts.extend(_scrape_seek_requests(session))
    time.sleep(2)

    logger.info("爬取今日澳洲...")
    all_posts.extend(_scrape_jraus_requests(session))

    # 去重
    seen_ids: set = set()
    unique: list[dict] = []
    for p in all_posts:
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique.append(p)

    logger.info("爬取完成 — 合计 %d 条（去内部重复后）", len(unique))
    return unique
