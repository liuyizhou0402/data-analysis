# -*- coding: utf-8 -*-
"""
每日岗位雷达 —— 综合投递平台 pipeline。

流程：多平台抓取 → 跨平台去重 → 按个人画像打分 → 排序 →
       跨天去重 → 渲染 HTML → 发到邮箱。

用法：
  python -m job_alerts.main --now        # 正式跑：抓取 + 发邮件（GitHub Actions 用）
  python -m job_alerts.main --preview     # 本地预览：抓取(若可)否则用样例，写 HTML 不发信
  python -m job_alerts.main --sample       # 强制用样例数据，写 HTML 不发信
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from datetime import datetime

# 允许 `python job_alerts/main.py` 和 `python -m job_alerts.main` 两种方式
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from job_alerts import config, dedupe, emailer, report, scorer
    from job_alerts.sources import REGISTRY
    from job_alerts.sources.base import JobPosting
    from job_alerts import sample_data
else:
    from . import config, dedupe, emailer, report, scorer
    from .sources import REGISTRY
    from .sources.base import JobPosting
    from . import sample_data


def collect_live() -> tuple[list[JobPosting], Counter]:
    """跑所有启用的数据源 × 所有关键词，返回 (去重后岗位, 各源计数)。"""
    seen_fp: set[str] = set()
    jobs: list[JobPosting] = []
    by_source: Counter = Counter()

    for name, enabled in config.SOURCES_ENABLED.items():
        if not enabled or name not in REGISTRY:
            continue
        fetch = REGISTRY[name]
        print(f"\n=== 数据源: {name} ===")
        # 熔断器：被反爬的源会连续返回 0，没必要把 10 个关键词都跑一遍（每次 ~25s 超时）；
        # 不吃关键词的源（如 GradConnection 每次返回同一批）连续"新增 0"也提前收手。
        consec_empty = 0   # 连续抓到 0 条原始结果
        consec_no_new = 0  # 连续 0 条新增（去重后）
        for kw in config.SEARCH_KEYWORDS:
            try:
                found = fetch(kw, config.SEARCH_LOCATION, config.PER_SOURCE_LIMIT)
            except Exception as e:  # noqa: BLE001
                print(f"  [{name}] 关键词「{kw}」抓取异常: {e}")
                found = []
            added = 0
            for j in found:
                fp = j.fingerprint()
                if fp in seen_fp or not j.title:
                    continue
                seen_fp.add(fp)
                jobs.append(j)
                by_source[name] += 1
                added += 1
            print(f"  「{kw}」-> {len(found)} 条，新增 {added}")

            consec_empty = consec_empty + 1 if not found else 0
            consec_no_new = consec_no_new + 1 if added == 0 else 0
            if consec_empty >= 2:
                print(f"  [{name}] 连续 2 次空结果（疑似被反爬/无数据），跳过剩余关键词。")
                break
            if consec_no_new >= 3:
                print(f"  [{name}] 连续 3 次无新增，提前结束该源。")
                break
    return jobs, by_source


def run(mode: str) -> int:
    print(f"▶ 岗位雷达启动 [{mode}] @ {datetime.now():%Y-%m-%d %H:%M}")

    if mode == "sample":
        raw_jobs = sample_data.JOBS
        by_source = Counter(j.source for j in raw_jobs)
    else:
        raw_jobs, by_source = collect_live()
        if not raw_jobs and mode == "preview":
            print("\n⚠ 实时抓取为空（本机网络受限/被反爬），改用样例数据预览。")
            raw_jobs = sample_data.JOBS
            by_source = Counter(j.source for j in raw_jobs)

    print(f"\n抓取合计: {len(raw_jobs)} 条（去重后）")

    # 打分 + 排序
    scored = scorer.score_all(raw_jobs)
    print(f"过滤+排序后: {len(scored)} 条（≥{config.MIN_SCORE}分）")

    # 跨天去重（只在正式发信时启用，预览不消耗去重库）
    # 手动补发时可设 JOB_ALERT_NO_DEDUPE=true 跳过去重，强制推送完整排名
    no_dedupe = os.environ.get("JOB_ALERT_NO_DEDUPE", "").lower() == "true"
    if mode == "now" and not no_dedupe:
        scored = dedupe.filter_new(scored)
        print(f"跨天去重后新增: {len(scored)} 条")
    elif mode == "now" and no_dedupe:
        print(f"⏭ 已跳过跨天去重，强制推送完整排名 {len(scored)} 条")

    stats = {
        "raw": len(raw_jobs),
        "min_score": config.MIN_SCORE,
        "by_source": dict(by_source),
    }
    subject, body = report.build_email(scored, stats)
    text_body = report.build_text(scored, stats)

    # 落地一份报告（artifact）
    os.makedirs(os.path.join(os.path.dirname(__file__), "data", "reports"), exist_ok=True)
    out = os.path.join(os.path.dirname(__file__), "data", "reports",
                       f"jobs_{datetime.now():%Y%m%d}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"📄 报告已写入 {out}")

    for j in scored[:10]:
        print(f"   {j.score:>3}  {j.title[:48]:48}  [{j.source}]")

    if mode == "now":
        ok = emailer.send(subject, body, text_body)
        # 发信失败时让这步以非 0 退出，GitHub Actions 会标红，方便第一时间发现
        # 邮箱密钥失效（否则只在日志里一行 ❌，很容易被忽略）。
        if not ok:
            print("❌ 邮件未发出——请检查 XHS_EMAIL_USER / XHS_EMAIL_PASSWORD 密钥。")
            return 1
    else:
        print(f"\n（{mode} 模式不发信）主题预览: {subject}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="每日岗位雷达")
    ap.add_argument("--now", action="store_true", help="正式跑并发邮件")
    ap.add_argument("--preview", action="store_true", help="预览，不发信")
    ap.add_argument("--sample", action="store_true", help="样例数据，不发信")
    args = ap.parse_args()

    if args.now:
        mode = "now"
    elif args.sample:
        mode = "sample"
    else:
        mode = "preview"
    sys.exit(run(mode))


if __name__ == "__main__":
    main()
