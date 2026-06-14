# -*- coding: utf-8 -*-
"""GradConnection（毕业生/实习项目总站）。

对应 HTML 里的 "GradConnection · 毕业生/实习项目总站"。
用 Playwright 抓搜索结果页的岗位卡片。
"""
from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from . import browser
from .base import JobPosting

BASE = "https://au.gradconnection.com"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    url = f"{BASE}/jobs/sydney/?keywords={quote_plus(keyword)}"
    html = browser.get_html(url, wait_selector=".campaign-content, .box-content-block")
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    jobs: list[JobPosting] = []
    cards = soup.select("div.campaign-box, div.box-content-block, a.box-header-title")
    seen = set()
    for card in cards[: limit * 3]:
        link = card if card.name == "a" else card.select_one("a[href*='/employers/'], a.box-header-title, a")
        if not link or not link.get("href"):
            continue
        href = link["href"]
        if href in seen:
            continue
        seen.add(href)
        title = link.get_text(strip=True)
        emp = card.select_one(".employer-name, .box-employer") if card.name != "a" else None
        if not title:
            continue
        jobs.append(JobPosting(
            title=title,
            company=(emp.get_text(strip=True) if emp else "GradConnection employer"),
            location="Sydney",
            url=href if href.startswith("http") else BASE + href,
            source="GradConnection",
        ))
        if len(jobs) >= limit:
            break
    return jobs
