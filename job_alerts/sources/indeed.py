# -*- coding: utf-8 -*-
"""Indeed（health data，悉尼）。

对应 HTML 里的 "Indeed · health data（悉尼）"。
Indeed 反爬最凶（经常弹 "verify you are human"），所以是 best-effort：
抓到就加分，抓不到也不影响其它源。建议优先用 Adzuna（聚合了 Indeed）。
"""
from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from . import browser
from .base import JobPosting, parse_relative_date

BASE = "https://au.indeed.com"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    url = f"{BASE}/jobs?q={quote_plus(keyword)}&l={quote_plus(location)}&fromage=14&sort=date"
    html = browser.get_html(url, wait_selector="#mosaic-provider-jobcards, .job_seen_beacon")
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    jobs: list[JobPosting] = []
    for card in soup.select("div.job_seen_beacon, td.resultContent")[:limit]:
        title_el = card.select_one("h2.jobTitle span, a.jcs-JobTitle span, h2 a")
        link_el = card.select_one("a.jcs-JobTitle, h2.jobTitle a, a[href*='/rc/clk'], a[href*='/viewjob']")
        comp_el = card.select_one("[data-testid='company-name'], span.companyName")
        loc_el = card.select_one("[data-testid='text-location'], div.companyLocation")
        date_el = card.select_one("[data-testid='myJobsStateDate'], span.date")
        if not title_el or not link_el:
            continue
        href = link_el.get("href", "")
        posted = date_el.get_text(strip=True) if date_el else ""
        jobs.append(JobPosting(
            title=title_el.get_text(strip=True),
            company=(comp_el.get_text(strip=True) if comp_el else ""),
            location=(loc_el.get_text(strip=True) if loc_el else location),
            url=href if href.startswith("http") else BASE + href,
            source="Indeed",
            posted=posted,
            posted_days_ago=parse_relative_date(posted),
        ))
    return jobs
