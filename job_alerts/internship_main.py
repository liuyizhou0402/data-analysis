# -*- coding: utf-8 -*-
"""
悉尼实习机会雷达（AI / 具身智能 / Digital Health 方向）

流程：多平台抓取 → 跨平台去重 → 按实习相关度+离USYD距离打分 →
      排序 → 跨天去重 → 渲染 HTML → 发邮件

用法：
  python -m job_alerts.internship_main --now       # 正式跑+发邮件（GitHub Actions 用）
  python -m job_alerts.internship_main --preview   # 预览，不发信
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from datetime import datetime

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from job_alerts import internship_config as cfg
    from job_alerts import internship_scorer as scorer
    from job_alerts import internship_report as report
    from job_alerts import internship_dedupe as dedupe
    from job_alerts import emailer
    from job_alerts.sources import REGISTRY
    from job_alerts.sources.base import JobPosting, is_valid_job_url
else:
    from . import internship_config as cfg
    from . import internship_scorer as scorer
    from . import internship_report as report
    from . import internship_dedupe as dedupe
    from . import emailer
    from .sources import REGISTRY
    from .sources.base import JobPosting, is_valid_job_url


def collect_live() -> tuple[list[JobPosting], Counter]:
    """跑所有启用的数据源 × 所有关键词，返回 (去重后岗位, 各源计数)。"""
    seen_fp: set[str] = set()
    jobs: list[JobPosting] = []
    by_source: Counter = Counter()

    for name, enabled in cfg.SOURCES_ENABLED.items():
        if not enabled or name not in REGISTRY:
            continue
        fetch = REGISTRY[name]
        print(f"\n=== 数据源: {name} ===")
        consec_empty = 0
        consec_no_new = 0
        for kw in cfg.SEARCH_KEYWORDS:
            try:
                found = fetch(kw, cfg.SEARCH_LOCATION, cfg.PER_SOURCE_LIMIT)
            except Exception as e:  # noqa: BLE001
                print(f"  [{name}] 关键词「{kw}」抓取异常: {e}")
                found = []
            added = 0
            for j in found:
                fp = j.fingerprint()
                if fp in seen_fp or not j.title or not is_valid_job_url(j.url):
                    continue
                seen_fp.add(fp)
                jobs.append(j)
                by_source[name] += 1
                added += 1
            print(f"  「{kw}」-> {len(found)} 条，新增 {added}")

            consec_empty = consec_empty + 1 if not found else 0
            consec_no_new = consec_no_new + 1 if added == 0 else 0
            if consec_empty >= 2:
                print(f"  [{name}] 连续空结果（疑似反爬/无数据），跳过剩余关键词。")
                break
            if consec_no_new >= 3:
                print(f"  [{name}] 连续无新增，提前结束该源。")
                break

    return jobs, by_source


def run(mode: str) -> int:
    print(f"▶ 实习雷达启动 [{mode}] @ {datetime.now():%Y-%m-%d %H:%M}")
    print(f"  目标：AI / 具身智能 / Digital Health 实习 · 优先离USYD近")

    raw_jobs, by_source = collect_live()
    print(f"\n抓取合计: {len(raw_jobs)} 条（跨平台去重后）")

    scored = scorer.score_all(raw_jobs)            # 完整候选池（已按分排序，未截断）
    print(f"打分+过滤后候选池: {len(scored)} 条（≥{cfg.MIN_SCORE}分）")

    no_dedupe = os.environ.get("INTERNSHIP_NO_DEDUPE", "").lower() == "true"
    n_backfill = 0
    if mode == "now" and not no_dedupe:
        new_jobs = dedupe.filter_new(scored)       # 今日新增（标记为已见）
        print(f"跨天去重后新增: {len(new_jobs)} 条")
        # —— 保底 30 条：今日新增不足时，用候选池里的往期高分岗位补足 ——
        if len(new_jobs) < cfg.MIN_DAILY_RESULTS:
            new_fps = {j.fingerprint() for j in new_jobs}
            backfill = [j for j in scored if j.fingerprint() not in new_fps]
            need = cfg.MIN_DAILY_RESULTS - len(new_jobs)
            for j in backfill[:need]:
                j.is_backfill = True
            n_backfill = min(need, len(backfill))
            final = new_jobs + backfill[:need]
            print(f"今日新增不足 {cfg.MIN_DAILY_RESULTS} 条，补充 {n_backfill} 条往期高分至保底。")
        else:
            final = new_jobs
        scored = final[: cfg.MAX_RESULTS]
    else:
        if no_dedupe:
            print(f"⏭ 已跳过跨天去重，强制推送候选池前 {cfg.MAX_RESULTS} 条")
        scored = scored[: cfg.MAX_RESULTS]

    stats = {
        "raw": len(raw_jobs),
        "min_score": cfg.MIN_SCORE,
        "by_source": dict(by_source),
        "n_new": sum(1 for j in scored if not j.is_backfill),
        "n_backfill": sum(1 for j in scored if j.is_backfill),
    }
    subject, body = report.build_email(scored, stats)
    text_body = report.build_text(scored, stats)

    # 落地报告 artifact
    reports_dir = os.path.join(os.path.dirname(__file__), "data", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    out = os.path.join(reports_dir, f"internships_{datetime.now():%Y%m%d}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"📄 报告已写入 {out}")

    print("\nTop 10 推荐：")
    for j in scored[:10]:
        print(f"  {j.score:>3}分  {j.title[:45]:45}  [{j.source}]  {j.location}")

    if mode == "now":
        ok = emailer.send(subject, body, text_body)
        if not ok:
            print("❌ 邮件未发出——请检查 XHS_EMAIL_USER / XHS_EMAIL_PASSWORD 密钥。")
            return 1
    else:
        print(f"\n（{mode} 模式不发信）主题预览: {subject}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="悉尼实习机会雷达（AI/具身智能/Digital Health）")
    ap.add_argument("--now", action="store_true", help="正式跑并发邮件")
    ap.add_argument("--preview", action="store_true", help="预览，不发信")
    args = ap.parse_args()
    mode = "now" if args.now else "preview"
    sys.exit(run(mode))


if __name__ == "__main__":
    main()
