"""
Entry point for the XHS Study-Abroad Customer Scraper.

Usage
-----
  python main.py                  — start the daily scheduler
  python main.py --now            — run the full pipeline once immediately
  python main.py --mock           — run once with mock data (ignores USE_MOCK_DATA env var)
  python main.py --test-email     — send a test email and exit
  python main.py --now --mock     — run once with forced mock data
"""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Bootstrap: ensure the package root is on sys.path so sub-modules resolve
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import config  # noqa: E402 — must come after sys.path patch


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def _configure_logging(level: int = logging.INFO) -> None:
    """Set up rotating file handler + stderr stream handler."""
    root = logging.getLogger()
    root.setLevel(level)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file — keep 7 days × ~5 MB per file
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=7,
            encoding="utf-8",
        )
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)
    except OSError as exc:
        print(f"[WARNING] Could not open log file {config.LOG_FILE}: {exc}", file=sys.stderr)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(fmt)
    root.addHandler(stream_handler)


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Report persistence
# ---------------------------------------------------------------------------

def _save_report(users: list[dict[str, Any]], report_date: str) -> Path:
    """Save the user list as a JSON report and return the file path."""
    filename = f"report_{report_date}.json"
    report_path = config.REPORTS_DIR / filename
    try:
        with report_path.open("w", encoding="utf-8") as fh:
            json.dump(
                {
                    "report_date": report_date,
                    "total_users": len(users),
                    "generated_at": datetime.now().isoformat(),
                    "users": users,
                },
                fh,
                ensure_ascii=False,
                indent=2,
            )
        logger.info("Report saved to %s", report_path)
    except OSError as exc:
        logger.error("Could not save report: %s", exc)
    return report_path


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def run_pipeline(force_mock: bool | None = None) -> dict[str, Any]:
    """
    Execute the full scrape → match → deduplicate → report → email pipeline.

    Parameters
    ----------
    force_mock : bool | None
        If True, override config.USE_MOCK_DATA to True for this run.
        If None, use whatever config.USE_MOCK_DATA is set to.

    Returns a summary dict with keys: report_date, total_scraped, total_new,
    report_path, email_sent.
    """
    report_date = datetime.now().strftime("%Y-%m-%d")
    logger.info("=" * 60)
    logger.info("Pipeline start — %s", report_date)
    logger.info("=" * 60)

    # Optionally override mock flag
    if force_mock is True:
        config.USE_MOCK_DATA = True
        logger.info("Mock mode forced by caller")

    # 1. Scrape
    import scraper
    raw_users = scraper.scrape_users()
    logger.info("Step 1/4 — Scrape: %d raw user records", len(raw_users))

    # 2. Score & filter
    import keyword_matcher
    scored_users = keyword_matcher.filter_and_score(raw_users)
    logger.info("Step 2/4 — Match: %d users passed scoring threshold", len(scored_users))

    # 3. Deduplicate
    import deduplicator
    new_users = deduplicator.filter_new_users(scored_users)
    logger.info(
        "Step 3/4 — Deduplicate: %d new users (historical store: %d total)",
        len(new_users),
        deduplicator.get_seen_count(),
    )

    # Warn if we're below the daily target
    if len(new_users) < config.TARGET_USER_COUNT:
        logger.warning(
            "Found %d new users — below daily target of %d.  "
            "Consider adjusting keywords or scraping more pages.",
            len(new_users),
            config.TARGET_USER_COUNT,
        )
    else:
        logger.info(
            "Target met: %d new users (target: %d)",
            len(new_users),
            config.TARGET_USER_COUNT,
        )

    # 4a. Persist report
    report_path = _save_report(new_users, report_date)

    # 4b. Mark users as seen BEFORE sending email so a crash doesn't re-send
    deduplicator.mark_seen(new_users)

    # 4c. Send email
    import email_sender
    email_sent = False
    if new_users:
        email_sent = email_sender.send_report(new_users, report_date)
        if not email_sent:
            logger.error("Step 4/4 — Email: FAILED (check credentials / network)")
        else:
            logger.info("Step 4/4 — Email: sent successfully")
    else:
        logger.warning("Step 4/4 — Email: skipped (no new users to report)")

    summary = {
        "report_date": report_date,
        "total_scraped": len(raw_users),
        "total_scored": len(scored_users),
        "total_new": len(new_users),
        "report_path": str(report_path),
        "email_sent": email_sent,
    }
    logger.info("Pipeline complete: %s", summary)
    logger.info("=" * 60)
    return summary


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="XHS Study-Abroad Customer Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--now",
        action="store_true",
        help="Run the full pipeline once immediately and exit",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force mock data for this run (overrides USE_MOCK_DATA env var)",
    )
    parser.add_argument(
        "--test-email",
        action="store_true",
        dest="test_email",
        help="Send a test email and exit (to verify SMTP credentials)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable DEBUG-level logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    _configure_logging(logging.DEBUG if args.verbose else logging.INFO)

    if args.test_email:
        import email_sender
        success = email_sender.send_test_email()
        sys.exit(0 if success else 1)

    if args.now or args.mock:
        summary = run_pipeline(force_mock=True if args.mock else None)
        total_new = summary["total_new"]
        print(
            f"\nPipeline finished — {total_new} new users found.  "
            f"Report: {summary['report_path']}",
            flush=True,
        )
        sys.exit(0)

    # Default: start scheduler
    import scheduler
    scheduler.start_scheduler()


if __name__ == "__main__":
    main()
