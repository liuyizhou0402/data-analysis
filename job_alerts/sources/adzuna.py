# -*- coding: utf-8 -*-
"""Adzuna 官方聚合 API（最稳定的"backbone"）。

Adzuna 聚合了 Seek / Indeed 等澳洲主流招聘站，返回干净 JSON（含薪资、
描述、公司、地点、跳转链接）。需要一个**免费**的 app_id / app_key：
  注册 https://developer.adzuna.com/  →  拿到 ID 和 KEY
  在 GitHub Secrets 里加 ADZUNA_APP_ID / ADZUNA_APP_KEY

没配 key 时本源自动跳过，不报错。
"""
from __future__ import annotations

import os

from .base import JobPosting, http_get

API = "https://api.adzuna.com/v1/api/jobs/au/search/1"


def available() -> bool:
    return bool(os.environ.get("ADZUNA_APP_ID") and os.environ.get("ADZUNA_APP_KEY"))


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    if not available():
        return []
    params = {
        "app_id": os.environ["ADZUNA_APP_ID"],
        "app_key": os.environ["ADZUNA_APP_KEY"],
        "what": keyword,
        "where": location,
        "results_per_page": limit,
        "max_days_old": 14,
        "sort_by": "date",
        "content-type": "application/json",
    }
    resp = http_get(API, params=params)
    if not resp:
        return []
    try:
        data = resp.json()
    except Exception:  # noqa: BLE001
        return []

    jobs: list[JobPosting] = []
    for it in data.get("results", [])[:limit]:
        sal = ""
        lo, hi = it.get("salary_min"), it.get("salary_max")
        if lo and hi:
            sal = f"${int(lo):,} – ${int(hi):,}"
        jobs.append(JobPosting(
            title=it.get("title", ""),
            company=(it.get("company", {}) or {}).get("display_name", ""),
            location=(it.get("location", {}) or {}).get("display_name", location),
            url=it.get("redirect_url", ""),
            source="Adzuna",
            description=it.get("description", ""),
            salary=sal,
            posted=(it.get("created", "") or "")[:10],
        ))
    return jobs
