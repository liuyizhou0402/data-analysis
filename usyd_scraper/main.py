"""
悉尼大学新生获客清单 — 入口。

用法:
  python main.py --now          立即跑一次
  python main.py --mock         强制用测试数据跑一次
  python main.py --test-email   发测试邮件
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


def _save_report(users: list[dict[str, Any]], date: str) -> Path:
    path = config.REPORTS_DIR / f"report_{date}.json"
    try:
        with path.open("w", encoding="utf-8") as fh:
            json.dump({"date": date, "count": len(users), "generated_at": datetime.now().isoformat(), "users": users},
                      fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        logger.error("保存报告失败: %s", exc)
    return path


def run_pipeline(force_mock: bool | None = None) -> dict[str, Any]:
    date = datetime.now().strftime("%Y-%m-%d")
    logger.info("=" * 60)
    logger.info("悉大新生获客 Pipeline 启动 — %s", date)
    if force_mock:
        config.USE_MOCK_DATA = True

    import scraper
    raw = scraper.scrape_users()
    logger.info("步骤 1/4 — 爬取: %d 条原始记录", len(raw))

    import matcher
    scored = matcher.filter_and_score(raw)
    logger.info("步骤 2/4 — 识别新生 + 生成话术: %d 个通过", len(scored))

    import deduplicator
    new = deduplicator.filter_new_users(scored)
    logger.info("步骤 3/4 — 去重: %d 个新用户（历史库 %d）", len(new), deduplicator.get_seen_count())

    # 只取每日目标数量（已按回复可能性排序，取最优的）
    new = new[:config.TARGET_USER_COUNT]

    if len(new) < config.TARGET_USER_COUNT:
        logger.warning("仅找到 %d 个新用户，低于目标 %d", len(new), config.TARGET_USER_COUNT)

    _save_report(new, date)
    deduplicator.mark_seen(new)

    import email_sender
    sent = False
    if new:
        sent = email_sender.send_report(new, date)
    else:
        logger.warning("步骤 4/4 — 无新用户，跳过邮件")

    summary = {"date": date, "scraped": len(raw), "scored": len(scored), "new": len(new), "email_sent": sent}
    logger.info("Pipeline 完成: %s", summary)
    logger.info("=" * 60)
    return summary


def main(argv=None):
    p = argparse.ArgumentParser(description="悉尼大学新生获客清单")
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
        print(f"\n完成 — 今日 {s['new']} 个新悉大新生，邮件已发送: {s['email_sent']}")
        sys.exit(0)

    # 默认启动定时器
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    sched = BlockingScheduler(timezone=config.SCHEDULER_TIMEZONE)
    sched.add_job(run_pipeline, CronTrigger(hour=config.SCHEDULE_HOUR, minute=config.SCHEDULE_MINUTE,
                                            timezone=config.SCHEDULER_TIMEZONE),
                  id="usyd_daily", name="USYD Daily")
    logger.info("定时器启动 — 每天 %02d:%02d %s 运行", config.SCHEDULE_HOUR, config.SCHEDULE_MINUTE, config.SCHEDULER_TIMEZONE)
    print(f"[定时器] 每天 {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d} 运行，Ctrl+C 停止")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
