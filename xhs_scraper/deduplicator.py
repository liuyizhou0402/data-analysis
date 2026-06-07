"""
Persistent deduplication layer.

Keeps a rolling JSON file at config.SEEN_USERS_FILE that maps
user_id → first_seen_date.  Any user already in this file is
filtered out before the report is generated.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_seen() -> dict[str, str]:
    """
    Load the seen-users store from disk.
    Returns a dict mapping user_id (str) → first_seen_date (str, ISO-8601 date).
    """
    path: Path = config.SEEN_USERS_FILE
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
        # Legacy format: list of IDs
        if isinstance(data, list):
            logger.info("Migrating legacy seen_users.json list format → dict format")
            return {uid: "unknown" for uid in data}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read %s: %s — starting fresh", path, exc)
    return {}


def _save_seen(seen: dict[str, str]) -> None:
    """Persist the seen-users store to disk atomically."""
    path: Path = config.SEEN_USERS_FILE
    tmp = path.with_suffix(".json.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(seen, fh, ensure_ascii=False, indent=2)
        tmp.replace(path)
        logger.debug("Saved %d seen users to %s", len(seen), path)
    except OSError as exc:
        logger.error("Failed to save seen users: %s", exc)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def filter_new_users(users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Return only users whose user_id has NOT been seen before.
    Does NOT update the seen-users store — call ``mark_seen`` for that.
    """
    seen = _load_seen()
    new_users = [u for u in users if u.get("user_id", "") not in seen]
    logger.info(
        "Deduplication: %d total → %d new (filtered %d duplicates)",
        len(users),
        len(new_users),
        len(users) - len(new_users),
    )
    return new_users


def mark_seen(users: list[dict[str, Any]]) -> None:
    """
    Add the given users to the seen-users store and persist to disk.
    Existing entries are never overwritten (first-seen date is preserved).
    """
    if not users:
        return
    seen = _load_seen()
    today = datetime.now().strftime("%Y-%m-%d")
    added = 0
    for user in users:
        uid = user.get("user_id", "")
        if uid and uid not in seen:
            seen[uid] = today
            added += 1
    _save_seen(seen)
    logger.info("Marked %d new users as seen (store total: %d)", added, len(seen))


def get_seen_count() -> int:
    """Return the total number of historically seen user IDs."""
    return len(_load_seen())
