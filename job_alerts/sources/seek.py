# -*- coding: utf-8 -*-
"""Seek（澳洲第一大招聘站）。

Seek 页面是 React，数据走内部 chalice-search JSON 接口，且有 Cloudflare。
策略：用浏览器上下文先拿 cookie，再 fetch 同源 JSON 接口。
对应 HTML 里的 "Seek · health data analyst（悉尼）"。
"""
from __future__ import annotations

from urllib.parse import quote

from . import browser
from .base import JobPosting

HOME = "https://www.seek.com.au/"
API = "https://www.seek.com.au/api/chalice-search/v4/search"


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    api_url = (
        f"{API}?siteKey=AU-Main&where={quote(location)}"
        f"&keywords={quote(keyword)}&page=1&pageSize={limit}&sortmode=ListedDate"
    )
    data = browser.fetch_json(HOME, api_url)
    if not data:
        return []

    jobs: list[JobPosting] = []
    for it in (data.get("data") or [])[:limit]:
        job_id = it.get("id")
        adv = it.get("advertiser", {}) or {}
        sal = it.get("salaryLabel", "") or ""
        loc = ", ".join(
            l.get("label", "") for l in (it.get("locations") or []) if l.get("label")
        ) or location
        jobs.append(JobPosting(
            title=it.get("title", ""),
            company=adv.get("description", "") or it.get("companyName", ""),
            location=loc,
            url=f"https://www.seek.com.au/job/{job_id}" if job_id else HOME,
            source="Seek",
            description=it.get("teaser", ""),
            salary=sal,
            posted=it.get("listingDateDisplay", ""),
        ))
    return jobs
