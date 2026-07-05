"""
悉尼高端家教需求获取 — 入口

用法:
  python main.py --now        立即跑一次
  python main.py --mock       强制用测试数据
  python main.py --test-email 发测试邮件
"""
from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import config


def _log(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)
    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    try:
        fh = logging.handlers.RotatingFileHandler(config.LOG_FILE, maxBytes=5*1024*1024, backupCount=7, encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)
    except OSError:
        pass
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    root.addHandler(sh)


logger = logging.getLogger(__name__)


def _save_report(posts: list[dict[str, Any]], date: str) -> Path:
    path = config.REPORTS_DIR / f"report_{date}.json"
    try:
        with path.open("w", encoding="utf-8") as fh:
            json.dump({"date": date, "count": len(posts), "generated_at": datetime.now().isoformat(), "posts": posts},
                      fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        logger.error("保存报告失败: %s", exc)
    return path


def run_pipeline(force_mock: bool | None = None) -> dict[str, Any]:
    date = datetime.now().strftime("%Y-%m-%d")
    logger.info("=" * 60)
    logger.info("悉尼家教需求 Pipeline 启动 — %s", date)
    if force_mock:
        config.USE_MOCK_DATA = True

    import scraper
    raw = scraper.scrape_posts()
    logger.info("步骤 1/4 — 爬取: %d 条原始帖子", len(raw))

    import matcher
    scored = matcher.filter_and_score(raw)
    logger.info("步骤 2/4 — 筛选高端需求: %d 条通过", len(scored))

    import deduplicator
    new = deduplicator.filter_new_posts(scored)
    logger.info("步骤 3/4 — 去重: %d 条新帖（历史库 %d）", len(new), deduplicator.get_seen_count())

    new = new[:config.TARGET_COUNT]
    if len(new) < config.TARGET_COUNT:
        logger.warning("仅找到 %d 条，低于目标 %d", len(new), config.TARGET_COUNT)

    _save_report(new, date)
    deduplicator.mark_seen(new)

    import email_sender
    sent = False
    if new:
        sent = email_sender.send_report(new, date)
    else:
        logger.warning("步骤 4/4 — 无新帖，跳过邮件")

    summary = {"date": date, "scraped": len(raw), "scored": len(scored), "new": len(new), "email_sent": sent}
    logger.info("Pipeline 完成: %s", summary)
    logger.info("=" * 60)
    return summary


def main(argv=None):
    p = argparse.ArgumentParser(description="悉尼高端家教需求获取")
    p.add_argument("--now", action="store_true")
    p.add_argument("--mock", action="store_true")
    p.add_argument("--test-email", action="store_true", dest="test_email")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args(argv)

    _log(logging.DEBUG if args.verbose else logging.INFO)

    if args.test_email:
        import email_sender
        sys.exit(0 if email_sender.send_test_email() else 1)

    if args.now or args.mock:
        s = run_pipeline(force_mock=True if args.mock else None)
        print(f"\n完成 — 今日 {s['new']} 条高端家教需求，邮件已发送: {s['email_sent']}")
        sys.exit(0)

    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    sched = BlockingScheduler(timezone=config.SCHEDULER_TIMEZONE)
    sched.add_job(run_pipeline, CronTrigger(hour=config.SCHEDULE_HOUR, minute=config.SCHEDULE_MINUTE,
                                            timezone=config.SCHEDULER_TIMEZONE),
                  id="tutor_daily", name="Tutor Daily")
    logger.info("定时器启动 — 每天 %02d:%02d %s", config.SCHEDULE_HOUR, config.SCHEDULE_MINUTE, config.SCHEDULER_TIMEZONE)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
