"""
过滤 + 评分：只保留高端家教需求帖，排除低价、排除老师推广帖。
"""
from __future__ import annotations

import logging
import re
from typing import Any

import config

logger = logging.getLogger(__name__)


def _extract_hourly_rate(text: str) -> float | None:
    """从文本提取时薪数字，返回 AUD/hr，找不到返回 None"""
    patterns = [
        r"\$(\d+)\s*(?:/hr|per hour|/hour|an hour|/h\b)",
        r"(\d+)\s*(?:dollars?|aud)\s*(?:/hr|per hour)",
        r"时薪\s*\$?(\d+)",
        r"\$(\d+)\s*[-–]\s*\$?(\d+)\s*/hr",  # range: take lower
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def _is_teacher_ad(text: str) -> bool:
    """判断是否是老师自我推广帖（而非找老师的需求帖）"""
    lower = text.lower()
    for kw in config.EXCLUDE_KEYWORDS:
        if kw.lower() in lower:
            return True
    return False


def _score(post: dict) -> int:
    text = (post.get("title", "") + " " + post.get("content", "") + " " + post.get("price_signal", "")).lower()
    score = 50  # 基础分

    # 高端信号加分
    for kw in config.PREMIUM_SIGNALS:
        if kw.lower() in text:
            score += 8

    # 明确价格加分
    rate = _extract_hourly_rate(text)
    if rate:
        if rate >= 80:
            score += 30
        elif rate >= 60:
            score += 20
        elif rate >= 50:
            score += 10
        elif rate < config.MIN_HOURLY:
            score -= 50  # 低价减分

    # 有 URL 加分
    if post.get("url"):
        score += 5

    # 今日以内发帖加分
    if post.get("posted_at") and "today" in post.get("posted_at", "").lower():
        score += 10

    return min(score, 100)


def filter_and_score(posts: list[dict]) -> list[dict]:
    result = []
    skipped_cheap = 0
    skipped_teacher = 0

    for post in posts:
        text = (post.get("title", "") + " " + post.get("content", "") + " " + post.get("price_signal", "")).lower()

        # 排除老师推广帖
        if _is_teacher_ad(text):
            skipped_teacher += 1
            continue

        # 排除明确低价帖
        skip = False
        for kw in config.PRICE_SKIP_KEYWORDS:
            if kw.lower() in text:
                skip = True
                break
        if skip:
            skipped_cheap += 1
            continue

        # 排除明确低于最低时薪的帖
        rate = _extract_hourly_rate(text)
        if rate is not None and rate < config.MIN_HOURLY:
            skipped_cheap += 1
            continue

        post["score"] = _score(post)
        result.append(post)

    result.sort(key=lambda x: x["score"], reverse=True)
    logger.info(
        "筛选完成：%d/%d 通过（过滤低价 %d，过滤推广 %d）",
        len(result), len(posts), skipped_cheap, skipped_teacher,
    )
    return result
