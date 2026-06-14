# -*- coding: utf-8 -*-
"""匹配度打分引擎：把每个岗位打成 0~100 分，并记录命中原因（写进邮件）。"""
from __future__ import annotations

from . import config
from .sources.base import JobPosting


def _hit_any(text: str, words: list[str]) -> list[str]:
    return [w.strip() for w in words if w.strip() and w.strip() in text]


def score_job(job: JobPosting) -> JobPosting:
    title = job.title.lower()
    blob = job.text_blob()
    company = job.company.lower()
    w = config.WEIGHTS
    pts = 0.0
    reasons: list[str] = []

    # 1) 标题强相关
    th = _hit_any(title, config.TITLE_CORE)
    if th:
        pts += w["title_core"]
        reasons.append(f"标题命中「{', '.join(th[:2])}」")

    # 2) 健康/医疗领域
    dh = _hit_any(blob, config.DOMAIN_HEALTH)
    if dh:
        pts += w["domain_health"]
        reasons.append("健康/医疗行业")

    # 3) 技能重合（按命中数累计，封顶 weight）
    sk = _hit_any(blob, config.SKILLS)
    if sk:
        ratio = min(len(sk) / 4.0, 1.0)
        pts += w["skills"] * ratio
        reasons.append("技能匹配: " + ", ".join(sorted(set(s.strip() for s in sk))[:4]))

    # 4) 目标雇主
    emp = _hit_any(company + " " + blob, config.TARGET_EMPLOYERS)
    if emp:
        pts += w["employer"]
        reasons.append(f"⭐ 目标雇主: {emp[0]}")

    # 5) 资历匹配
    good = _hit_any(blob, config.SENIORITY_GOOD)
    bad = _hit_any(blob, config.SENIORITY_BAD)
    if good and not bad:
        pts += w["seniority"]
        reasons.append(f"适配级别: {good[0]}")
    elif bad and not good:
        pts -= w["seniority"]
        reasons.append(f"⚠ 偏资深({bad[0]})")

    # 6) 地点
    loc = job.location.lower()
    if any(c.lower() in loc for c in ([config.SEARCH_LOCATION] + config.SEARCH_LOCATION_ALT)):
        pts += w["location"]
    else:
        reasons.append("⚠ 地点存疑")

    # 7) PR/签证信号
    if _hit_any(blob, config.VISA_GOOD):
        pts += w["visa"]
        reasons.append("PR/工作权利友好")
    if _hit_any(blob, config.VISA_BAD):
        pts -= w["visa"]
        reasons.append("⚠ 可能要求公民/clearance")

    # 8) 新鲜度
    if job.posted_days_ago is not None:
        if job.posted_days_ago <= 1:
            pts += w["recency"]
            reasons.append("今天/昨天新发")
        elif job.posted_days_ago <= 3:
            pts += w["recency"] * 0.6

    job.score = max(0, min(100, round(pts)))
    job.reasons = reasons
    return job


def score_all(jobs: list[JobPosting]) -> list[JobPosting]:
    scored = [score_job(j) for j in jobs]
    scored = [j for j in scored if j.score >= config.MIN_SCORE]
    scored.sort(key=lambda j: j.score, reverse=True)
    return scored[: config.MAX_RESULTS]
