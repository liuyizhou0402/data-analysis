# -*- coding: utf-8 -*-
"""跨天去重：记住已经推送过的岗位指纹，避免每天重复轰炸同一个岗位。"""
from __future__ import annotations

import json
import os
from datetime import datetime

from .sources.base import JobPosting

SEEN_PATH = os.path.join(os.path.dirname(__file__), "data", "seen_jobs.json")


def _load() -> dict:
    if os.path.exists(SEEN_PATH):
        try:
            with open(SEEN_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            return {}
    return {}


def filter_new(jobs: list[JobPosting]) -> list[JobPosting]:
    """返回未推送过的岗位；同时把它们登记为已见。"""
    seen = _load()
    fresh: list[JobPosting] = []
    today = datetime.now().strftime("%Y-%m-%d")
    for j in jobs:
        fp = j.fingerprint()
        if fp not in seen:
            seen[fp] = today
            fresh.append(j)
    _save(seen)
    return fresh


def _save(seen: dict) -> None:
    os.makedirs(os.path.dirname(SEEN_PATH), exist_ok=True)
    # 只保留最近 60 天的记录，避免文件无限膨胀
    cutoff = (datetime.now()).toordinal() - 60
    pruned = {
        k: v for k, v in seen.items()
        if _ordinal(v) is None or _ordinal(v) >= cutoff
    }
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(pruned, f, ensure_ascii=False, indent=0)


def _ordinal(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").toordinal()
    except Exception:  # noqa: BLE001
        return None
