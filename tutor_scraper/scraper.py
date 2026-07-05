"""
多平台爬虫：今日澳洲 / Gumtree / 澳洲论坛 / 微博
"""
from __future__ import annotations

import json
import logging
import random
import re
import time
from datetime import datetime, timedelta
from typing import Any

import config

logger = logging.getLogger(__name__)

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
        "id": "jraus_002",
        "source": "今日澳洲",
        "title": "诚招数学/物理家教，悉尼北区，时薪面议",
        "content": "孩子读Year 11，就读私立学校，准备HSC，需要数学和物理一对一辅导，每周2次，每次2小时。时薪面议，有经验者优先，要求有相关专业背景。",
        "url": "https://www.jraus.com/xxx",
        "location": "悉尼北区",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "站内信联系",
        "price_signal": "时薪面议（私立学校Year 11）",
        "score": 90,
    },
    {
        "id": "gumtree_003",
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
        "id": "jraus_004",
        "source": "今日澳洲",
        "title": "找悉尼家教老师，精英学校备考，数学英语",
        "content": "小孩现在Year 5，准备考精英学校（Selective School），需要数学和英语辅导。每周两次，地点在Chatswood附近，愿意提供有竞争力的报酬。",
        "url": "https://www.jraus.com/zzz",
        "location": "Chatswood, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "站内信联系",
        "price_signal": "有竞争力的报酬（精英学校备考）",
        "score": 88,
    },
    {
        "id": "gumtree_005",
        "source": "Gumtree",
        "title": "University Chemistry Tutor Needed - UNSW - $70/hr",
        "content": "1st year UNSW chemistry student looking for tutor. Struggling with organic chemistry. $70/hr, flexible schedule, can meet on campus or online.",
        "url": "https://www.gumtree.com.au/s-ad/aaa",
        "location": "Kensington (UNSW), Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "Reply via Gumtree",
        "price_signal": "$70/hr",
        "score": 82,
    },
    {
        "id": "aussiezone_006",
        "source": "澳洲论坛",
        "title": "求HSC中文继承语家教，悉尼西北区",
        "content": "孩子读Year 12，需要中文继承语（Chinese in Context）家教，目前成绩中等，希望冲刺90分以上。悉尼西北区，时薪$60-80，有经验者优先。",
        "url": "https://www.aussiezone.com/xxx",
        "location": "西北区, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "帖子内回复",
        "price_signal": "$60-80/hr",
        "score": 80,
    },
    {
        "id": "gumtree_007",
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
        "id": "jraus_008",
        "source": "今日澳洲",
        "title": "悉尼CBD附近找钢琴老师兼文化课辅导",
        "content": "孩子就读本地私立小学，寻找能提供钢琴+数学双辅导的全能家教。时薪$70起，有经验优先，地点在CBD附近，可以上门。",
        "url": "https://www.jraus.com/piano",
        "location": "CBD, Sydney",
        "posted_at": datetime.now().strftime("%Y-%m-%d"),
        "contact_hint": "站内信联系",
        "price_signal": "$70起/hr",
        "score": 78,
    },
]


# ── 真实爬虫 ──────────────────────────────────────────────────────────────────

def _scrape_gumtree(page, keyword: str) -> list[dict]:
    """爬取 Gumtree 家教需求帖"""
    posts = []
    try:
        url = f"https://www.gumtree.com.au/s-tutoring-lessons/sydney/{keyword.replace(' ', '-').lower()}/k0c18320l3004532"
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        results = page.query_selector_all("article.user-ad-row, .listing-results article, [data-q='search-result']")
        for item in results[:10]:
            try:
                title_el = item.query_selector("a.user-ad-row-new-design__title-span, .listing-title, h2 a, [data-q='listing-title']")
                price_el = item.query_selector(".user-ad-row-new-design__price, .listing-price, [data-q='listing-price']")
                location_el = item.query_selector(".user-ad-row-new-design__location, .listing-location")
                desc_el = item.query_selector(".user-ad-row-new-design__description, .listing-description")
                link_el = item.query_selector("a[href*='/s-ad/']")

                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                price = price_el.inner_text().strip() if price_el else ""
                location = location_el.inner_text().strip() if location_el else "Sydney"
                desc = desc_el.inner_text().strip() if desc_el else ""
                href = link_el.get_attribute("href") if link_el else ""
                full_url = f"https://www.gumtree.com.au{href}" if href and href.startswith("/") else href

                post_id = f"gumtree_{abs(hash(title))}"
                posts.append({
                    "id": post_id,
                    "source": "Gumtree",
                    "title": title,
                    "content": desc,
                    "url": full_url,
                    "location": location,
                    "posted_at": datetime.now().strftime("%Y-%m-%d"),
                    "contact_hint": "在 Gumtree 上回复帖子",
                    "price_signal": price,
                    "score": 0,
                })
            except Exception:
                continue
    except Exception as e:
        logger.warning("Gumtree 爬取失败 (%s): %s", keyword, e)
    return posts


def _scrape_jraus(page) -> list[dict]:
    """爬取今日澳洲论坛家教相关帖子"""
    posts = []
    search_terms = ["家教", "补习", "辅导", "tutor"]
    for term in search_terms:
        try:
            url = f"https://www.jraus.com/search?q={term}&section=posts&sortby=newest"
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            items = page.query_selector_all(".search-result, .post-list-item, article, .thread-item")
            for item in items[:8]:
                try:
                    title_el = item.query_selector("h2, h3, .title, a.title")
                    link_el = item.query_selector("a[href]")
                    desc_el = item.query_selector(".description, .excerpt, p")

                    if not title_el:
                        continue
                    title = title_el.inner_text().strip()
                    href = link_el.get_attribute("href") if link_el else ""
                    desc = desc_el.inner_text().strip() if desc_el else ""
                    full_url = f"https://www.jraus.com{href}" if href and href.startswith("/") else href

                    posts.append({
                        "id": f"jraus_{abs(hash(title))}",
                        "source": "今日澳洲",
                        "title": title,
                        "content": desc,
                        "url": full_url,
                        "location": "悉尼",
                        "posted_at": datetime.now().strftime("%Y-%m-%d"),
                        "contact_hint": "在今日澳洲论坛站内回复",
                        "price_signal": "",
                        "score": 0,
                    })
                except Exception:
                    continue
        except Exception as e:
            logger.warning("今日澳洲爬取失败 (%s): %s", term, e)
    return posts


def _scrape_gumtree_listing_page(page) -> list[dict]:
    """直接爬 Gumtree Tutoring 分类页，用更宽松的选择器"""
    posts = []
    urls_to_try = [
        "https://www.gumtree.com.au/s-tutoring-lessons/sydney/k0c18320l3004532?sort=date",
        "https://www.gumtree.com.au/s-tutoring-lessons/k0c18320?q=tutor+wanted+sydney&sort=date",
    ]
    for url in urls_to_try:
        try:
            page.goto(url, timeout=40000, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 提取所有帖子链接（最通用方式）
            links = page.query_selector_all("a[href*='/s-ad/']")
            seen_hrefs: set = set()
            for link in links[:30]:
                try:
                    href = link.get_attribute("href") or ""
                    if not href or href in seen_hrefs:
                        continue
                    seen_hrefs.add(href)

                    title = link.inner_text().strip()
                    if not title or len(title) < 5:
                        # 尝试从父元素找标题
                        parent = link.query_selector("xpath=..")
                        title = parent.inner_text().strip()[:120] if parent else ""
                    if not title:
                        continue

                    full_url = f"https://www.gumtree.com.au{href}" if href.startswith("/") else href

                    # 从父容器提取价格和地点
                    container = link
                    for _ in range(4):
                        container = container.query_selector("xpath=..")
                        if not container:
                            break
                        text = container.inner_text()
                        if len(text) > 30:
                            break

                    container_text = container.inner_text() if container else title
                    price = ""
                    import re as _re
                    m = _re.search(r"\$[\d,]+(?:\s*/\s*(?:hr|hour|h\b))?", container_text)
                    if m:
                        price = m.group(0)

                    posts.append({
                        "id": f"gumtree_{abs(hash(href))}",
                        "source": "Gumtree",
                        "title": title[:120],
                        "content": container_text[:400],
                        "url": full_url,
                        "location": "Sydney",
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
            logger.warning("Gumtree 爬取失败 (%s): %s", url, e)

    logger.info("Gumtree 原始结果: %d 条", len(posts))
    return posts


def _scrape_seek(page) -> list[dict]:
    """爬 Seek.com.au 悉尼家教职位（英文高端帖）"""
    posts = []
    try:
        url = "https://www.seek.com.au/tutor-jobs/in-Sydney-NSW-2000"
        page.goto(url, timeout=40000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        links = page.query_selector_all("article a[href*='/job/'], a[data-automation='jobTitle']")
        seen: set = set()
        for link in links[:15]:
            try:
                href = link.get_attribute("href") or ""
                if href in seen:
                    continue
                seen.add(href)
                title = link.inner_text().strip()
                if not title:
                    continue
                full_url = f"https://www.seek.com.au{href}" if href.startswith("/") else href

                # 父容器找公司/地点
                parent = link
                for _ in range(5):
                    parent = parent.query_selector("xpath=..")
                    if not parent:
                        break
                    t = parent.inner_text()
                    if len(t) > 50:
                        break
                container_text = parent.inner_text()[:400] if parent else title

                posts.append({
                    "id": f"seek_{abs(hash(href))}",
                    "source": "Seek",
                    "title": title,
                    "content": container_text,
                    "url": full_url,
                    "location": "Sydney",
                    "posted_at": datetime.now().strftime("%Y-%m-%d"),
                    "contact_hint": "在 Seek 上直接申请",
                    "price_signal": "",
                    "score": 0,
                })
            except Exception:
                continue
    except Exception as e:
        logger.warning("Seek 爬取失败: %s", e)
    logger.info("Seek: %d 条", len(posts))
    return posts


def _scrape_facebook_groups_via_search(page) -> list[dict]:
    """尝试通过公开搜索找悉尼华人家教帖（Facebook 无需登录的公开帖）"""
    # Facebook 公开帖非常有限，跳过避免登录墙
    return []


def scrape_posts() -> list[dict]:
    if config.USE_MOCK_DATA:
        logger.info("USE_MOCK_DATA=True — 生成测试数据")
        mock = MOCK_POSTS.copy()
        random.shuffle(mock)
        logger.info("Mock 爬取完成 — %d 条帖子", len(mock))
        return mock

    from playwright.sync_api import sync_playwright

    all_posts: list[dict] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-AU",
            timezone_id="Australia/Sydney",
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.new_page()

        # 1. Gumtree 分类页
        logger.info("爬取 Gumtree...")
        gumtree_posts = _scrape_gumtree_listing_page(page)
        all_posts.extend(gumtree_posts)
        time.sleep(2)

        # 2. Seek
        logger.info("爬取 Seek...")
        seek_posts = _scrape_seek(page)
        all_posts.extend(seek_posts)
        time.sleep(2)

        # 3. 今日澳洲
        logger.info("爬取今日澳洲...")
        jraus_posts = _scrape_jraus(page)
        all_posts.extend(jraus_posts)
        logger.info("今日澳洲: %d 条", len(jraus_posts))
        time.sleep(2)

        browser.close()

    # 去重（同一 id）
    seen_ids: set = set()
    unique: list[dict] = []
    for p in all_posts:
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique.append(p)

    logger.info("爬取完成 — 合计 %d 条（去内部重复后）", len(unique))
    return unique
