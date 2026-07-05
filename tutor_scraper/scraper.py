"""
多平台爬虫：Gumtree RSS / TutorFinder / Care.com.au
使用 RSS + 轻量 HTTP 请求（避开云 IP 封锁）。
"""
from __future__ import annotations

import logging
import random
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any

import config

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
}

# ── Mock 数据 ─────────────────────────────────────────────────────────────────
MOCK_POSTS = [
    {
        "id": "gumtree_001",
        "source": "Gumtree",
        "title": "Wanted: HSC Maths Tutor - $80-100/hr - North Shore",
        "content": "Looking for experienced HSC maths tutor for Year 12 student. North Shore. Budget $80-100/hr. Selective school student targeting 99+ ATAR.",
        "url": "https://www.gumtree.com.au/s-ad/001",
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
        "content": "Seeking IB tutor for Year 12 Chemistry and Maths HL. Eastern Suburbs. $90/hr negotiable.",
        "url": "https://www.gumtree.com.au/s-ad/002",
        "location": "Eastern Suburbs, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$90/hr",
        "score": 92,
    },
    {
        "id": "tutorfinder_003",
        "source": "TutorFinder",
        "title": "Private HSC English & History Tutor Needed - $75-85/hr",
        "content": "Seeking experienced HSC tutor. $75-85/hr. North Sydney area.",
        "url": "https://www.tutorfinder.com.au/job/003",
        "location": "North Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Apply via TutorFinder",
        "price_signal": "$75-85/hr",
        "score": 88,
    },
    {
        "id": "gumtree_004",
        "source": "Gumtree",
        "title": "Scholarship Exam Tutor - Year 6 - $75/hr - Mosman",
        "content": "Year 6 scholarship exam preparation (AAS/ACER). Mosman. $75/hr, 2x per week.",
        "url": "https://www.gumtree.com.au/s-ad/004",
        "location": "Mosman, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$75/hr",
        "score": 85,
    },
    {
        "id": "tutorfinder_005",
        "source": "TutorFinder",
        "title": "University Maths Tutor UNSW/USyd - $70/hr",
        "content": "1st/2nd year university maths tutor needed. UNSW or USyd campus. $70/hr.",
        "url": "https://www.tutorfinder.com.au/job/005",
        "location": "Kensington/Camperdown",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Apply via TutorFinder",
        "price_signal": "$70/hr",
        "score": 82,
    },
    {
        "id": "gumtree_006",
        "source": "Gumtree",
        "title": "Selective School Prep - $65/hr - Chatswood",
        "content": "Year 5 selective school prep. Maths and English. Chatswood. $65/hr, 2x/week.",
        "url": "https://www.gumtree.com.au/s-ad/006",
        "location": "Chatswood, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$65/hr",
        "score": 80,
    },
    {
        "id": "gumtree_007",
        "source": "Gumtree",
        "title": "Senior HSC Tutor Multiple Subjects - $60-90/hr",
        "content": "HSC tutors needed across Maths, Science, English. $60-90/hr depending on experience. North Shore.",
        "url": "https://www.gumtree.com.au/s-ad/007",
        "location": "North Shore",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$60-90/hr",
        "score": 83,
    },
    {
        "id": "gumtree_008",
        "source": "Gumtree",
        "title": "Piano + Academic Tutor - $70/hr - CBD",
        "content": "Private school student needs piano and primary academics tutor. CBD. $70/hr.",
        "url": "https://www.gumtree.com.au/s-ad/008",
        "location": "CBD, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$70/hr",
        "score": 78,
    },
]


# ── RSS 爬虫 ──────────────────────────────────────────────────────────────────

def _get(url: str, session, timeout: int = 20):
    try:
        resp = session.get(url, headers=_HEADERS, timeout=timeout)
        if resp.status_code == 200:
            return resp
        logger.warning("HTTP %d: %s", resp.status_code, url)
    except Exception as e:
        logger.warning("请求失败 (%s): %s", url, e)
    return None


def _scrape_gumtree_rss(session) -> list[dict]:
    """通过 Gumtree RSS 获取家教帖（RSS 通常不被 IP 封锁）"""
    posts = []
    # Gumtree RSS 格式
    rss_urls = [
        "https://www.gumtree.com.au/s-tutoring-lessons/sydney/k0c18320l3004532?rss=true",
        "https://www.gumtree.com.au/s-tutoring-lessons/k0c18320?rss=true",
    ]
    for url in rss_urls:
        resp = _get(url, session)
        if not resp:
            continue
        try:
            root = ET.fromstring(resp.content)
            ns = {}
            channel = root.find("channel")
            if channel is None:
                continue
            items = channel.findall("item")
            for item in items[:30]:
                try:
                    title = (item.findtext("title") or "").strip()
                    link = (item.findtext("link") or "").strip()
                    desc = (item.findtext("description") or "").strip()
                    # 清除 HTML 标签
                    desc = re.sub(r"<[^>]+>", " ", desc).strip()[:400]
                    pub_date = (item.findtext("pubDate") or "").strip()

                    if not title:
                        continue

                    # 从描述里提取价格
                    price_m = re.search(r"\$[\d,]+(?:\s*/\s*(?:hr|hour|h\b))?", desc, re.IGNORECASE)
                    price = price_m.group(0) if price_m else ""

                    posts.append({
                        "id": f"gumtree_{abs(hash(link or title))}",
                        "source": "Gumtree",
                        "title": title[:150],
                        "content": desc,
                        "url": link,
                        "location": "Sydney",
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在 Gumtree 上回复帖子",
                        "price_signal": price,
                        "score": 0,
                    })
                except Exception:
                    continue

            if posts:
                logger.info("Gumtree RSS: %d 条", len(posts))
                break
        except ET.ParseError as e:
            logger.warning("Gumtree RSS 解析失败: %s", e)
        except Exception as e:
            logger.warning("Gumtree RSS 错误: %s", e)

    if not posts:
        logger.info("Gumtree RSS: 0 条（可能被屏蔽）")
    return posts


def _scrape_tutorfinder(session) -> list[dict]:
    """爬 TutorFinder.com.au 家教需求列表"""
    from bs4 import BeautifulSoup
    posts = []
    urls = [
        "https://www.tutorfinder.com.au/find-tutor/?subject=&location=Sydney&level=",
        "https://www.tutorfinder.com.au/find-tutor/?subject=hsc&location=Sydney",
        "https://www.tutorfinder.com.au/find-tutor/?subject=maths&location=Sydney",
    ]
    for url in urls:
        resp = _get(url, session)
        if not resp:
            continue
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            # TutorFinder 个人主页列表
            items = (
                soup.select(".tutor-card") or
                soup.select(".tutor-listing") or
                soup.select(".profile-card") or
                soup.select("article") or
                soup.select(".listing-item")
            )
            for item in items[:20]:
                try:
                    title_el = item.select_one("h2, h3, .tutor-name, .name, a[href*='tutor']")
                    link_el = item.select_one("a[href*='tutor']") or item.select_one("a")
                    rate_el = item.select_one(".rate, .price, .hourly-rate, [class*='rate'], [class*='price']")
                    desc_el = item.select_one("p, .description, .bio, .summary")

                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title:
                        continue
                    href = (link_el.get("href") or "") if link_el else ""
                    full_url = f"https://www.tutorfinder.com.au{href}" if href.startswith("/") else href
                    rate = rate_el.get_text(strip=True) if rate_el else ""
                    desc = desc_el.get_text(strip=True)[:300] if desc_el else ""

                    posts.append({
                        "id": f"tutorfinder_{abs(hash(href or title))}",
                        "source": "TutorFinder",
                        "title": title[:150],
                        "content": desc,
                        "url": full_url,
                        "location": "Sydney",
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在 TutorFinder 上联系",
                        "price_signal": rate,
                        "score": 0,
                    })
                except Exception:
                    continue
            if posts:
                break
        except Exception as e:
            logger.warning("TutorFinder 解析失败: %s", e)
        time.sleep(1)

    logger.info("TutorFinder: %d 条", len(posts))
    return posts


def _scrape_care(session) -> list[dict]:
    """爬 Care.com.au 家教需求"""
    from bs4 import BeautifulSoup
    posts = []
    urls = [
        "https://www.care.com/au/en-us/tutors/sydney--nsw",
        "https://www.care.com/au/en-us/tutors/sydney--nsw?serviceType=tutor",
    ]
    for url in urls:
        resp = _get(url, session)
        if not resp:
            continue
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            items = (
                soup.select(".provider-card") or
                soup.select("[data-testid='provider-card']") or
                soup.select(".caregiver-card") or
                soup.select("article")
            )
            for item in items[:20]:
                try:
                    name_el = item.select_one("h2, h3, .name, [class*='name']")
                    link_el = item.select_one("a")
                    rate_el = item.select_one("[class*='rate'], [class*='price'], [class*='hourly']")
                    desc_el = item.select_one("p, [class*='bio'], [class*='description']")

                    if not name_el:
                        continue
                    name = name_el.get_text(strip=True)
                    if not name:
                        continue
                    href = (link_el.get("href") or "") if link_el else ""
                    full_url = f"https://www.care.com.au{href}" if href.startswith("/") else href
                    rate = rate_el.get_text(strip=True) if rate_el else ""
                    desc = desc_el.get_text(strip=True)[:300] if desc_el else ""

                    posts.append({
                        "id": f"care_{abs(hash(href or name))}",
                        "source": "Care.com.au",
                        "title": f"Tutor Available: {name}",
                        "content": desc,
                        "url": full_url,
                        "location": "Sydney",
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在 Care.com.au 上联系",
                        "price_signal": rate,
                        "score": 0,
                    })
                except Exception:
                    continue
            if posts:
                break
        except Exception as e:
            logger.warning("Care.com.au 解析失败: %s", e)

    logger.info("Care.com.au: %d 条", len(posts))
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

    logger.info("爬取 Gumtree RSS...")
    all_posts.extend(_scrape_gumtree_rss(session))
    time.sleep(2)

    logger.info("爬取 TutorFinder...")
    all_posts.extend(_scrape_tutorfinder(session))
    time.sleep(2)

    logger.info("爬取 Care.com.au...")
    all_posts.extend(_scrape_care(session))

    # 去重
    seen_ids: set = set()
    unique: list[dict] = []
    for p in all_posts:
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique.append(p)

    logger.info("爬取完成 — 合计 %d 条（去内部重复后）", len(unique))
    return unique
