# -*- coding: utf-8 -*-
"""数据源公共部分：JobPosting 数据模型 + HTTP/浏览器抓取工具。"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import requests

# 仿真浏览器请求头，尽量降低被反爬拦截的概率
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9,zh-CN;q=0.8",
}


@dataclass
class JobPosting:
    """跨平台统一的岗位数据结构。"""
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str = ""
    salary: str = ""
    posted: str = ""               # 原始发布时间文本，如 "2 days ago"
    posted_days_ago: Optional[int] = None
    # 打分阶段填充
    score: int = 0
    reasons: list = field(default_factory=list)

    def fingerprint(self) -> str:
        """用于跨平台去重的指纹：公司+标题（归一化）。"""
        key = f"{_norm(self.company)}|{_norm(self.title)}"
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def text_blob(self) -> str:
        """用于打分的全文（小写）。"""
        return " ".join([
            self.title, self.company, self.location, self.description, self.salary
        ]).lower()


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def http_get(url: str, params: dict | None = None, headers: dict | None = None,
             timeout: int = 20) -> Optional[requests.Response]:
    """带浏览器头的 GET，失败返回 None（不抛异常，保证单源失败不影响整体）。"""
    h = dict(BROWSER_HEADERS)
    if headers:
        h.update(headers)
    try:
        r = requests.get(url, params=params, headers=h, timeout=timeout)
        if r.status_code == 200:
            return r
        print(f"    [http] {url} -> HTTP {r.status_code}")
        return None
    except Exception as e:  # noqa: BLE001
        print(f"    [http] {url} -> 异常 {e}")
        return None


def parse_relative_date(text: str) -> Optional[int]:
    """把 '3 days ago' / 'today' / '1 week ago' 解析成"几天前"。"""
    if not text:
        return None
    t = text.lower()
    if "today" in t or "just" in t or "hour" in t or "minute" in t:
        return 0
    m = re.search(r"(\d+)\s*(day|week|month)", t)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2)
    return n if unit == "day" else n * 7 if unit == "week" else n * 30
