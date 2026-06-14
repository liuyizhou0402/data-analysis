# -*- coding: utf-8 -*-
"""LinkedIn 免登录 guest 接口。

jobs-guest 接口返回一段 <li> 列表的 HTML，无需登录，相对稳定。
对应 HTML 里的 "LinkedIn Jobs · 同关键词 + 开启 Open to work"。
"""
from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from .base import JobPosting, http_get, parse_relative_date

GUEST_API = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    jobs: list[JobPosting] = []
    url = (
        f"{GUEST_API}?keywords={quote_plus(keyword)}"
        f"&location={quote_plus(location)}&f_TPR=r604800&start=0"
    )
    resp = http_get(url, headers={"Accept": "text/html"})
    if not resp:
        return jobs

    soup = BeautifulSoup(resp.text, "lxml")
    for card in soup.select("li")[:limit]:
        title_el = card.select_one(".base-search-card__title")
        company_el = card.select_one(".base-search-card__subtitle")
        loc_el = card.select_one(".job-search-card__location")
        link_el = card.select_one("a.base-card__full-link") or card.select_one("a")
        date_el = card.select_one("time")
        if not title_el or not link_el:
            continue
        posted = (date_el.get_text(strip=True) if date_el else "")
        jobs.append(JobPosting(
            title=title_el.get_text(strip=True),
            company=(company_el.get_text(strip=True) if company_el else ""),
            location=(loc_el.get_text(strip=True) if loc_el else location),
            url=link_el.get("href", "").split("?")[0],
            source="LinkedIn",
            posted=posted,
            posted_days_ago=parse_relative_date(posted),
        ))
    return jobs
