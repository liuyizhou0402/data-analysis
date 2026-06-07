"""去重层：记录已发现过的用户，保证每日不重复。"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)


def _load() -> dict[str, str]:
    path: Path = config.SEEN_USERS_FILE
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
        if isinstance(data, list):
            return {uid: "unknown" for uid in data}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("读取 %s 失败: %s — 重新开始", path, exc)
    return {}


def _save(seen: dict[str, str]) -> None:
    path: Path = config.SEEN_USERS_FILE
    tmp = path.with_suffix(".json.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(seen, fh, ensure_ascii=False, indent=2)
        tmp.replace(path)
    except OSError as exc:
        logger.error("保存失败: %s", exc)


def filter_new_users(users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = _load()
    new = [u for u in users if u.get("user_id", "") not in seen]
    logger.info("去重：%d 总 → %d 新（过滤 %d 重复）", len(users), len(new), len(users) - len(new))
    return new


def mark_seen(users: list[dict[str, Any]]) -> None:
    if not users:
        return
    seen = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    added = 0
    for u in users:
        uid = u.get("user_id", "")
        if uid and uid not in seen:
            seen[uid] = today
            added += 1
    _save(seen)
    logger.info("标记 %d 个新用户为已见（库总计：%d）", added, len(seen))


def get_seen_count() -> int:
    return len(_load())
