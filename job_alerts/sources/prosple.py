# -*- coding: utf-8 -*-
"""Prosple（毕业生项目 + 申请截止日）。

对应 HTML 里的 "Prosple · 毕业生项目+申请截止日"。
"""
from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from . import browser
from .base import JobPosting

BASE = "https://au.prosple.com"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    url = f"{BASE}/search/graduate-jobs?keywords={quote_plus(keyword)}&locations=2-25"
    html = browser.get_html(url, wait_selector="article, .SearchResultCard, a[href*='/graduate-employers/']")
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    jobs: list[JobPosting] = []
    seen = set()
    for card in soup.select("article, div[class*='SearchResult'], li[class*='result']")[: limit * 3]:
        link = card.select_one("a[href]")
        title_el = card.select_one("h2, h3, [class*='title']")
        if not link or not title_el:
            continue
        href = link["href"]
        if href in seen:
            continue
        seen.add(href)
        emp = card.select_one("[class*='employer'], [class*='company']")
        jobs.append(JobPosting(
            title=title_el.get_text(strip=True),
            company=(emp.get_text(strip=True) if emp else "Prosple employer"),
            location="Sydney",
            url=href if href.startswith("http") else BASE + href,
            source="Prosple",
        ))
        if len(jobs) >= limit:
            break
    return jobs
