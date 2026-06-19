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
        # 优先找具体岗位链接（路径深度 ≥ 3，如 /employers/google/ai-intern/）
        # 而非雇主概览页（/employers/google/ 只有 2 段路径）
        candidate_link = None
        if card.name == "a":
            candidate_link = card
        else:
            best_depth = 0
            for a in card.select("a[href]"):
                href_a = a.get("href", "")
                full = href_a if href_a.startswith("http") else BASE + href_a
                depth = full.rstrip("/").count("/")
                if depth > best_depth:
                    best_depth = depth
                    candidate_link = a
            # 如果只找到雇主概览页（深度 < 5 即 https://au.gradconnection.com/employers/x/），跳过
            if candidate_link and best_depth < 5:
                candidate_link = None

        if not candidate_link or not candidate_link.get("href"):
            continue
        href = candidate_link["href"]
        if href in seen:
            continue
        seen.add(href)
        title = candidate_link.get_text(strip=True) or card.select_one(
            ".box-header-title, h2, h3"
        ) and card.select_one(".box-header-title, h2, h3").get_text(strip=True) or ""
        emp = card.select_one(".employer-name, .box-employer") if card.name != "a" else None
        if not title:
            continue
        full_url = href if href.startswith("http") else BASE + href
        jobs.append(JobPosting(
            title=title,
            company=(emp.get_text(strip=True) if emp else "GradConnection"),
            location="Sydney",
            url=full_url,
            source="GradConnection",
        ))
        if len(jobs) >= limit:
            break
    return jobs
