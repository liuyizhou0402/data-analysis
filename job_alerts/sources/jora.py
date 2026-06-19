# -*- coding: utf-8 -*-
"""Jora（SEEK 旗下澳洲聚合平台，中小企业覆盖较好，反爬相对温和）。

搜索 URL：https://au.jora.com/j?q={keyword}&l={location}&daterange=7
"""
from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from . import browser
from .base import JobPosting, parse_relative_date

BASE = "https://au.jora.com"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    url = f"{BASE}/j?q={quote_plus(keyword)}&l={quote_plus(location)}&daterange=7"
    html_content = browser.get_html(
        url,
        wait_selector="article.result, .lozad, [data-job-id]",
    )
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "lxml")
    jobs: list[JobPosting] = []
    seen: set[str] = set()

    for card in soup.select(
        "article.result, div[data-job-id], [class*='job-card'], li[class*='result']"
    )[: limit * 2]:
        # 优先从 data-job-id 属性构造稳定 URL
        job_id = card.get("data-job-id") or card.get("data-id")

        title_el = (
            card.select_one("a.job-title, h2 a, h3 a, [class*='title'] a")
            or card.select_one("h2, h3, [class*='title']")
        )
        # Jora 岗位链接格式：/jobs/view/xxx、/j?p=xxx 等，不一定含 /job/
        link_el = (
            card.select_one("a[href*='/jobs/view/']")
            or card.select_one("a[href*='/j?p']")
            or card.select_one("a.job-title")
            or card.select_one("a[href]")
        )
        comp_el = card.select_one("[class*='company'], [class*='employer'], [class*='advertiser']")
        loc_el = card.select_one("[class*='location'], [class*='suburb'], [class*='area']")
        date_el = card.select_one("[class*='date'], [class*='listed'], time")

        if not title_el:
            continue

        # 构造 URL：data-job-id 最可靠，其次用抓到的链接
        if job_id:
            href = f"{BASE}/jobs/view/{job_id}"
        elif link_el:
            href = link_el.get("href", "")
            if not href:
                continue
            href = href if href.startswith("http") else BASE + href
            # 过滤掉搜索页自身 URL（Jora 搜索 URL 含 ?q= 参数）
            if "?q=" in href or href.rstrip("/") == BASE:
                continue
        else:
            continue

        if href in seen:
            continue
        seen.add(href)

        posted = date_el.get_text(strip=True) if date_el else ""
        jobs.append(JobPosting(
            title=title_el.get_text(strip=True),
            company=comp_el.get_text(strip=True) if comp_el else "",
            location=loc_el.get_text(strip=True) if loc_el else location,
            url=href,
            source="Jora",
            posted=posted,
            posted_days_ago=parse_relative_date(posted),
        ))
        if len(jobs) >= limit:
            break

    return jobs
