"""
悉尼大学新生识别 + 个性化话术草稿生成。

评分逻辑：
- 悉大身份信号        (必须命中，否则丢弃)
- 入学年份 2026/2027  (强信号，+40)
- 新生身份信号        (+30)
- 互动意愿信号        (求扩列/求搭子等，+20)
- 近期活跃            (+10)

只保留 relevance_score >= 阈值的用户，并按分数排序（最可能回复的排前面）。
为每个人生成一段「个性化开场白草稿」——你手动复制去真诚互动，绝不自动群发。
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import config

logger = logging.getLogger(__name__)

MIN_SCORE_THRESHOLD: int = 40


def _hits(text: str, signals: list[str]) -> list[str]:
    t = text.lower()
    return [s for s in signals if s.lower() in t]


def _all_text(user: dict[str, Any]) -> str:
    parts = [user.get("nickname", ""), user.get("bio", "")]
    for p in user.get("recent_posts", []):
        parts.append(p.get("title", ""))
        parts.append(p.get("desc", ""))
    return " ".join(parts)


def score_user(user: dict[str, Any]) -> dict[str, Any]:
    user = dict(user)
    text = _all_text(user)
    reasons: list[str] = []
    score = 0

    # 1. 悉大身份（硬性要求）
    usyd_hits = _hits(text, config.USYD_SIGNALS)
    if not usyd_hits:
        user["relevance_score"] = 0
        user["match_reasons"] = ["未命中悉大身份信号"]
        return user
    score += 20
    reasons.append(f"悉大身份：{('、'.join(usyd_hits[:3]))}")

    # 2. 入学年份 2026/2027
    year_hits = _hits(text, config.ENROLLMENT_YEAR_SIGNALS)
    if year_hits:
        score += 40
        reasons.append(f"入学年份信号：{('、'.join(year_hits[:3]))}")

    # 3. 新生身份
    fresh_hits = _hits(text, config.FRESHMAN_SIGNALS)
    if fresh_hits:
        score += 30
        reasons.append(f"新生信号：{('、'.join(fresh_hits[:3]))}")

    # 4. 互动意愿（求扩列/搭子）
    intent = [s for s in ("扩列", "搭子", "组织", "新生群", "蹲", "求") if s in text]
    if intent:
        score += 20
        reasons.append(f"互动意愿强：{('、'.join(intent[:3]))}")

    # 5. 近期活跃
    posts = user.get("recent_posts", [])
    if posts:
        latest = posts[0].get("publish_time", "")
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(str(latest)[:19], fmt)
                age = (datetime.now() - dt).days
                if age <= 14:
                    score += 10
                    reasons.append(f"近{age}天活跃")
                break
            except ValueError:
                continue

    user["relevance_score"] = min(score, 100)
    user["match_reasons"] = reasons
    user["opener_draft"] = _generate_opener(user)
    return user


def _generate_opener(user: dict[str, Any]) -> str:
    """
    生成个性化开场白草稿。基于用户笔记内容定制，让你手动复制去真诚私信。
    不是模板群发——每条都结合对方的具体内容，体现你真的看了 ta 的笔记。
    """
    nickname = user.get("nickname", "同学")
    text = _all_text(user)
    posts = user.get("recent_posts", [])
    post_title = posts[0].get("title", "") if posts else ""

    # 根据内容线索定制开场白
    if any(s in text for s in ("扩列", "搭子", "新生群", "组织")):
        hook = "看到你也在找悉大的新生搭子"
    elif any(s in text for s in ("offer", "录取", "上岸")):
        hook = "恭喜拿到悉大offer呀🎉"
    elif "租房" in text:
        hook = "刚看到你发的悉尼租房笔记，很有用"
    elif any(s in text for s in ("选课", "报到", "入学")):
        hook = "看到你在分享悉大入学的内容"
    else:
        hook = "刷到你的悉大笔记啦"

    year = ""
    for y in ("2026", "2027", "26fall", "27fall"):
        if y.lower() in text.lower():
            year = y
            break
    year_part = f"我也是{year}入学的，" if year else "我也是悉大的，"

    draft = (
        f"嗨{nickname}～{hook}！{year_part}"
        f"想拉个悉大留子扩列一起交流～"
        f"方便的话加个微信呀：{config.YOUR_WECHAT}，一起抱团不迷路😄"
    )
    if post_title:
        draft += f"\n（你那篇「{post_title[:20]}」我也很有共鸣）"
    return draft


def filter_and_score(users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = []
    for u in users:
        e = score_user(u)
        if e["relevance_score"] >= MIN_SCORE_THRESHOLD:
            scored.append(e)
    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    logger.info("筛选完成：%d/%d 个用户通过阈值 %d（已按回复可能性排序）",
                len(scored), len(users), MIN_SCORE_THRESHOLD)
    return scored
