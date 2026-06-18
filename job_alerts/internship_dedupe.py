# -*- coding: utf-8 -*-
"""实习机会跨天去重（独立存储，不与健康数据岗位雷达混用）。"""
from __future__ import annotations

import json
import os
from datetime import datetime

from .sources.base import JobPosting

SEEN_PATH = os.path.join(os.path.dirname(__file__), "data", "seen_internships.json")


def _load() -> dict:
    if os.path.exists(SEEN_PATH):
        try:
            with open(SEEN_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            return {}
    return {}


def filter_new(jobs: list[JobPosting]) -> list[JobPosting]:
    """返回未推送过的岗位，并登记已见指纹。"""
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
    cutoff = datetime.now().toordinal() - 60
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
