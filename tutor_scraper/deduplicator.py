from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)

_seen: set[str] = set()


def _load() -> None:
    global _seen
    if config.SEEN_FILE.exists():
        try:
            data = json.loads(config.SEEN_FILE.read_text(encoding="utf-8"))
            _seen = set(data.get("ids", []))
        except Exception:
            _seen = set()
    else:
        _seen = set()


def _save() -> None:
    try:
        config.SEEN_FILE.write_text(
            json.dumps({"ids": sorted(_seen)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        logger.error("保存去重库失败: %s", e)


def get_seen_count() -> int:
    _load()
    return len(_seen)


def filter_new_posts(posts: list[dict]) -> list[dict]:
    _load()
    new = [p for p in posts if p["id"] not in _seen]
    logger.info("去重：%d 总 → %d 新（过滤 %d 重复）", len(posts), len(new), len(posts) - len(new))
    return new


def mark_seen(posts: list[dict]) -> None:
    _load()
    for p in posts:
        _seen.add(p["id"])
    _save()
    logger.info("标记 %d 条帖子为已见（库总计：%d）", len(posts), len(_seen))
