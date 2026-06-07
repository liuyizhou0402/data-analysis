"""
Score and filter user dicts for UK / Australia study-abroad relevance.

Scoring factors
---------------
- Keyword density in posts/bios            (0-40 pts)
- Engagement level (likes + comments)      (0-20 pts)
- Recency of latest post                   (0-20 pts)
- Profile completeness                     (0-10 pts)
- Intent signals (question marks, "求推荐")  (0-10 pts)

Final score: 0-100.  Users below MIN_SCORE_THRESHOLD are dropped.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MIN_SCORE_THRESHOLD: int = 20  # users below this are not included in the report

# High-value intent keywords — strong signals that the user needs help
HIGH_INTENT_KEYWORDS: list[str] = [
    "求推荐", "求助", "怎么选", "哪家好", "中介",
    "顾问", "申请中", "备考", "规划", "咨询",
    "怎么办", "迷茫", "需要帮助", "不知道怎么",
]

# UK / Australia topic keywords
TOPIC_KEYWORDS: list[str] = [
    "英国", "澳洲", "澳大利亚", "英澳", "伦敦", "曼彻斯特", "伯明翰",
    "牛津", "剑桥", "UCL", "LSE", "KCL", "悉尼", "墨尔本", "布里斯班",
    "墨大", "悉大", "UNSW", "A-level", "IB", "IELTS", "TOEFL",
    "雅思", "托福", "留学", "出国", "国际学校", "海外", "升学",
]

# Engagement tier thresholds (total interactions = likes + comments)
_ENGAGEMENT_TIERS: list[tuple[int, int]] = [
    # (min_interactions, score_pts)
    (500, 20),
    (200, 15),
    (50,  10),
    (10,   5),
    (1,    2),
]

# Maximum age of a post to be considered "recent"
RECENCY_WINDOW_DAYS: int = 30


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _count_keyword_hits(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    """Return (hit_count, matched_keywords) for a given text."""
    text_lower = text.lower()
    matched: list[str] = []
    for kw in keywords:
        if kw.lower() in text_lower:
            matched.append(kw)
    return len(matched), matched


def _engagement_score(posts: list[dict[str, Any]]) -> tuple[int, str]:
    if not posts:
        return 0, "无互动数据"
    total_interactions = sum(
        p.get("likes", 0) + p.get("comments", 0) for p in posts
    )
    for threshold, pts in _ENGAGEMENT_TIERS:
        if total_interactions >= threshold:
            return pts, f"总互动量{total_interactions}"
    return 0, "互动量极低"


def _recency_score(posts: list[dict[str, Any]]) -> tuple[int, str]:
    """Score based on how recent the newest post is."""
    if not posts:
        return 0, "无发帖记录"

    latest_dt: datetime | None = None
    for p in posts:
        raw = p.get("publish_time", "")
        if not raw:
            continue
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
            try:
                dt = datetime.strptime(str(raw)[:19], fmt)
                if latest_dt is None or dt > latest_dt:
                    latest_dt = dt
                break
            except ValueError:
                continue

    if latest_dt is None:
        return 5, "发布时间未知（计默认分）"

    age_days = (datetime.now() - latest_dt).days
    if age_days <= 3:
        return 20, f"最近{age_days}天内活跃"
    elif age_days <= 7:
        return 15, f"最近{age_days}天内活跃"
    elif age_days <= 14:
        return 10, f"最近{age_days}天内活跃"
    elif age_days <= RECENCY_WINDOW_DAYS:
        return 5, f"最近{age_days}天内有发帖"
    else:
        return 0, f"最后发帖超过{age_days}天前"


def _profile_completeness_score(user: dict[str, Any]) -> tuple[int, str]:
    score = 0
    reasons: list[str] = []
    if user.get("nickname") and user["nickname"] != "未知用户":
        score += 4
        reasons.append("有昵称")
    if user.get("bio"):
        score += 3
        reasons.append("有个人简介")
    if user.get("profile_url"):
        score += 3
        reasons.append("有主页链接")
    detail = "、".join(reasons) if reasons else "资料不完整"
    return score, detail


def _intent_score(text: str) -> tuple[int, list[str]]:
    hits, matched = _count_keyword_hits(text, HIGH_INTENT_KEYWORDS)
    pts = min(hits * 3, 10)
    return pts, matched


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_user(user: dict[str, Any]) -> dict[str, Any]:
    """
    Add ``relevance_score`` (int 0-100) and ``match_reasons`` (list[str])
    to a user dict and return the enriched copy.
    """
    user = dict(user)  # shallow copy — do not mutate caller's dict
    reasons: list[str] = []
    total_score = 0

    posts: list[dict[str, Any]] = user.get("recent_posts", [])
    bio: str = user.get("bio", "")
    source_kw: str = user.get("source_keyword", "")

    # -- 1. Keyword density in posts + bio (0-40) --
    all_text = bio + " " + " ".join(
        (p.get("title", "") + " " + p.get("desc", "")) for p in posts
    )
    topic_hits, topic_matched = _count_keyword_hits(all_text, TOPIC_KEYWORDS)
    keyword_pts = min(topic_hits * 5, 40)
    total_score += keyword_pts
    if topic_matched:
        reasons.append(f"内容含留学相关词：{'、'.join(topic_matched[:5])}")
    elif source_kw:
        # Fallback: credit the search keyword itself
        total_score += 10
        reasons.append(f'通过关键词「{source_kw}」发现')

    # -- 2. Engagement (0-20) --
    eng_pts, eng_reason = _engagement_score(posts)
    total_score += eng_pts
    if eng_pts > 0:
        reasons.append(eng_reason)

    # -- 3. Recency (0-20) --
    rec_pts, rec_reason = _recency_score(posts)
    total_score += rec_pts
    reasons.append(rec_reason)

    # -- 4. Profile completeness (0-10) --
    prof_pts, prof_reason = _profile_completeness_score(user)
    total_score += prof_pts
    reasons.append(prof_reason)

    # -- 5. Intent signals (0-10) --
    intent_pts, intent_matched = _intent_score(all_text + " " + bio)
    total_score += intent_pts
    if intent_matched:
        reasons.append(f"包含意向词：{'、'.join(intent_matched[:3])}")

    # Also credit the pre-populated match_reason from the scraper
    if user.get("match_reason") and user["match_reason"] not in reasons:
        reasons.insert(0, user["match_reason"])

    user["relevance_score"] = min(total_score, 100)
    user["match_reasons"] = reasons
    return user


def filter_and_score(users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Score every user, drop those below MIN_SCORE_THRESHOLD, and return
    results sorted by relevance_score descending.
    """
    scored: list[dict[str, Any]] = []
    for user in users:
        enriched = score_user(user)
        if enriched["relevance_score"] >= MIN_SCORE_THRESHOLD:
            scored.append(enriched)
        else:
            logger.debug(
                "Dropped user '%s' (score=%d)",
                user.get("nickname", "?"),
                enriched["relevance_score"],
            )

    scored.sort(key=lambda u: u["relevance_score"], reverse=True)
    logger.info(
        "Scoring complete: %d/%d users passed threshold %d",
        len(scored),
        len(users),
        MIN_SCORE_THRESHOLD,
    )
    return scored
