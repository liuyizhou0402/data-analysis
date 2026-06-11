# -*- coding: utf-8 -*-
"""抓取各 RSS 源的最新留学资讯，并按热度打分排序。

热度分 = 关键词命中加权分 + 新鲜度分（48 小时内的新闻加分）。
RSS 没有点赞/评论数，这里用「关键词相关性 + 时效性」作为热度代理指标；
如果某条新闻被多个源同时报道（标题相似），会额外加分（多源报道 ≈ 高热度）。
"""

import calendar
import difflib
import logging
import time

import feedparser

from config import RSS_FEEDS, HOT_KEYWORDS

log = logging.getLogger(__name__)


def _score_text(text: str) -> int:
    text_l = text.lower()
    score = 0
    for weight, words in HOT_KEYWORDS.items():
        for w in words:
            if w.lower() in text_l:
                score += weight
    return score


def _freshness_score(published_ts: float) -> int:
    age_hours = (time.time() - published_ts) / 3600
    if age_hours < 24:
        return 20
    if age_hours < 48:
        return 10
    if age_hours < 72:
        return 5
    return 0


def fetch_all(max_age_days: int = 4) -> list[dict]:
    """返回按热度降序排列的资讯列表。"""
    items = []
    cutoff = time.time() - max_age_days * 86400

    for source, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            log.warning("抓取 %s 失败: %s", source, e)
            continue
        for entry in feed.entries[:30]:
            ts = None
            for key in ("published_parsed", "updated_parsed"):
                if entry.get(key):
                    ts = calendar.timegm(entry[key])
                    break
            if ts is None or ts < cutoff:
                continue
            title = entry.get("title", "").strip()
            summary = entry.get("summary", "")[:500]
            if not title:
                continue
            items.append({
                "source": source,
                "title": title,
                "summary": summary,
                "link": entry.get("link", ""),
                "published_ts": ts,
                "score": _score_text(title + " " + summary) + _freshness_score(ts),
            })
        log.info("%s: 抓到 %d 条", source, len(feed.entries) if feed else 0)

    # 多源报道加分 + 去重（保留分高的那条）
    deduped: list[dict] = []
    for item in sorted(items, key=lambda x: -x["score"]):
        dup = next((d for d in deduped
                    if difflib.SequenceMatcher(None, d["title"].lower(), item["title"].lower()).ratio() > 0.75),
                   None)
        if dup:
            dup["score"] += 8  # 多源报道，热度加分
        else:
            deduped.append(item)

    deduped.sort(key=lambda x: -x["score"])
    return deduped


def filter_by_region(items: list[dict], keywords: list[str], limit: int) -> list[dict]:
    """按地区关键词过滤；keywords 为空则返回综合热榜。"""
    if not keywords:
        return items[:limit]
    matched = [it for it in items
               if any(k.lower() in (it["title"] + it["summary"]).lower() for k in keywords)]
    # 不够就用综合热榜补齐
    for it in items:
        if len(matched) >= limit:
            break
        if it not in matched:
            matched.append(it)
    return matched[:limit]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for it in fetch_all()[:20]:
        print(f"[{it['score']:>3}] {it['source']} | {it['title']}")
