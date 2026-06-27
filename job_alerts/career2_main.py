# -*- coding: utf-8 -*-
"""
悉尼名企实习雷达 · 第二封
  ① 悉尼/澳洲 全球互联网大厂实习（可线下，最高优先）
  ② USYD 对口健康数据岗（按 HTML 雇主清单全网筛选）
  ③ 国内大厂线上/远程实习（必须线上，否则剔除）

流程：AU多源×AU关键词 + 国内源×远程关键词 → 跨平台去重 → 分类打分 →
      跨天去重（独立库）→ 保底补足 → 三段式渲染 → 发邮件

用法：
  python -m job_alerts.career2_main --now       # 正式跑+发邮件
  python -m job_alerts.career2_main --preview   # 预览，不发信
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from datetime import datetime

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from job_alerts import career2_config as cfg
    from job_alerts import career2_scorer as scorer
    from job_alerts import career2_report as report
    from job_alerts import career2_dedupe as dedupe
    from job_alerts import emailer
    from job_alerts.sources import REGISTRY, china_intern
    from job_alerts.sources.base import JobPosting, is_valid_job_url
else:
    from . import career2_config as cfg
    from . import career2_scorer as scorer
    from . import career2_report as report
    from . import career2_dedupe as dedupe
    from . import emailer
    from .sources import REGISTRY, china_intern
    from .sources.base import JobPosting, is_valid_job_url


def _ingest(found, seen_fp, jobs, by_source, name) -> int:
    added = 0
    for j in found:
        fp = j.fingerprint()
        if fp in seen_fp or not j.title or not is_valid_job_url(j.url):
            continue
        seen_fp.add(fp)
        jobs.append(j)
        by_source[name] += 1
        added += 1
    return added


def collect_live() -> tuple[list[JobPosting], Counter]:
    seen_fp: set[str] = set()
    jobs: list[JobPosting] = []
    by_source: Counter = Counter()

    # —— AU 源：服务①悉尼大厂实习 + ②健康对口岗 ——
    for name, enabled in cfg.SOURCES_ENABLED.items():
        if not enabled or name not in REGISTRY:
            continue
        fetch = REGISTRY[name]
        print(f"\n=== [AU] 数据源: {name} ===")
        consec_empty = consec_no_new = 0
        for kw in cfg.SEARCH_KEYWORDS:
            try:
                found = fetch(kw, cfg.SEARCH_LOCATION, cfg.PER_SOURCE_LIMIT)
            except Exception as e:  # noqa: BLE001
                print(f"  [{name}] 关键词「{kw}」抓取异常: {e}")
                found = []
            added = _ingest(found, seen_fp, jobs, by_source, name)
            print(f"  「{kw}」-> {len(found)} 条，新增 {added}")
            consec_empty = consec_empty + 1 if not found else 0
            consec_no_new = consec_no_new + 1 if added == 0 else 0
            if consec_empty >= 2:
                print(f"  [{name}] 连续空结果，跳过剩余关键词。")
                break
            if consec_no_new >= 3:
                print(f"  [{name}] 连续无新增，提前结束该源。")
                break

    # —— 国内源：服务③大厂线上实习（必须线上）——
    if cfg.CHINA_SOURCE_ENABLED:
        print(f"\n=== [国内] 数据源: china_intern（仅线上/远程）===")
        for kw in cfg.CHINA_KEYWORDS:
            try:
                found = china_intern.fetch(kw, "China", cfg.PER_SOURCE_LIMIT)
            except Exception as e:  # noqa: BLE001
                print(f"  [china_intern] 关键词「{kw}」抓取异常: {e}")
                found = []
            added = _ingest(found, seen_fp, jobs, by_source, "国内线上")
            print(f"  「{kw}」-> {len(found)} 条，新增 {added}")

    return jobs, by_source


def run(mode: str) -> int:
    print(f"▶ 名企实习雷达·第二封 启动 [{mode}] @ {datetime.now():%Y-%m-%d %H:%M}")
    print("  目标：悉尼全球大厂实习 + USYD健康对口岗 + 国内大厂线上实习")

    raw_jobs, by_source = collect_live()
    print(f"\n抓取合计: {len(raw_jobs)} 条（跨平台去重后）")

    scored = scorer.score_all(raw_jobs)
    print(f"分类打分+过滤后候选池: {len(scored)} 条（≥{cfg.MIN_SCORE}分，仅三大方向）")

    no_dedupe = os.environ.get("CAREER2_NO_DEDUPE", "").lower() == "true"
    if mode == "now" and not no_dedupe:
        new_jobs = dedupe.filter_new(scored)
        print(f"跨天去重后新增: {len(new_jobs)} 条")
        if len(new_jobs) < cfg.MIN_DAILY_RESULTS:
            new_fps = {j.fingerprint() for j in new_jobs}
            backfill = [j for j in scored if j.fingerprint() not in new_fps]
            need = cfg.MIN_DAILY_RESULTS - len(new_jobs)
            for j in backfill[:need]:
                j.is_backfill = True
            final = new_jobs + backfill[:need]
            print(f"今日新增不足 {cfg.MIN_DAILY_RESULTS}，补充 {min(need, len(backfill))} 条往期高分。")
        else:
            final = new_jobs
        # 重新按类别优先级+分数排序（补足项混入后保持分段顺序）
        final.sort(key=lambda j: (cfg.CAT_PRIORITY.get(j.category, 9), j.is_backfill, -j.score))
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

    reports_dir = os.path.join(os.path.dirname(__file__), "data", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    out = os.path.join(reports_dir, f"career2_{datetime.now():%Y%m%d}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"📄 报告已写入 {out}")

    print("\n分类计数：")
    for c in ("bigtech_syd", "health", "china_online"):
        print(f"  {c}: {sum(1 for j in scored if j.category == c)} 条")
    print("Top 10：")
    for j in scored[:10]:
        print(f"  {j.score:>3}分 [{j.category:12}] {j.title[:42]:42} [{j.source}]")

    if mode == "now":
        ok = emailer.send(subject, body, text_body)
        if not ok:
            print("❌ 邮件未发出——请检查 XHS_EMAIL_USER / XHS_EMAIL_PASSWORD 密钥。")
            return 1
    else:
        print(f"\n（{mode} 模式不发信）主题预览: {subject}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="悉尼名企实习雷达·第二封")
    ap.add_argument("--now", action="store_true", help="正式跑并发邮件")
    ap.add_argument("--preview", action="store_true", help="预览，不发信")
    ap.parse_args()
    mode = "now" if "--now" in sys.argv else "preview"
    sys.exit(run(mode))


if __name__ == "__main__":
    main()
