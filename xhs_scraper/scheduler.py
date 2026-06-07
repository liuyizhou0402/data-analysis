"""
APScheduler-based daily scheduler.

Runs the full scrape-match-deduplicate-email pipeline once per day at
config.SCHEDULE_HOUR:SCHEDULE_MINUTE in Asia/Shanghai time.

Usage:
  python scheduler.py          — start the scheduler (blocking)
  python scheduler.py --now    — fire once immediately, then exit
"""

from __future__ import annotations

import logging
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import config

logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    """
    Import and run the full pipeline.  Imported here (not at module level)
    so that the scheduler module can be imported without triggering a run.
    """
    # Late import to keep the scheduler module lightweight and independently importable.
    import main as pipeline_main  # noqa: PLC0415
    pipeline_main.run_pipeline()


def start_scheduler() -> None:
    """Start the blocking APScheduler.  Does not return until interrupted."""
    scheduler = BlockingScheduler(timezone=config.SCHEDULER_TIMEZONE)

    trigger = CronTrigger(
        hour=config.SCHEDULE_HOUR,
        minute=config.SCHEDULE_MINUTE,
        timezone=config.SCHEDULER_TIMEZONE,
    )
    scheduler.add_job(run_pipeline, trigger, id="daily_xhs_scrape", name="XHS Daily Scrape")

    logger.info(
        "Scheduler started — will run daily at %02d:%02d %s",
        config.SCHEDULE_HOUR,
        config.SCHEDULE_MINUTE,
        config.SCHEDULER_TIMEZONE,
    )
    print(
        f"[Scheduler] Running daily at "
        f"{config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d} "
        f"({config.SCHEDULER_TIMEZONE}).  Press Ctrl+C to stop.",
        flush=True,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user")


if __name__ == "__main__":
    # Configure basic logging when run directly
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if "--now" in sys.argv:
        logger.info("--now flag detected — running pipeline immediately")
        run_pipeline()
    else:
        start_scheduler()
