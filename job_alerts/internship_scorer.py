# -*- coding: utf-8 -*-
"""实习岗位打分引擎（AI / 具身智能 / Digital Health 方向）。

核心差异（vs 健康数据雷达）：
  1. 标题含 intern/internship 词 → 额外 30 分大加成
  2. 离悉尼大学（Camperdown）越近分越高（最多 +12 分）
  3. 同时覆盖 AI、具身智能、Digital Health 三个领域加分维度
"""
from __future__ import annotations

from . import internship_config as cfg
from .sources.base import JobPosting


def _hit_any(text: str, words: list[str]) -> list[str]:
    return [w for w in words if w and w in text]


def _usyd_proximity(location: str) -> tuple[int, str]:
    """按地名判断离 USYD 的距离，返回 (得分, 位置标签)。"""
    loc = location.lower()
    if any(s in loc for s in cfg.USYD_VERY_CLOSE):
        return cfg.WEIGHTS["location_usyd"], "步行可达USYD"
    if any(s in loc for s in cfg.USYD_CLOSE):
        return int(cfg.WEIGHTS["location_usyd"] * 0.75), "离USYD<5km"
    if any(s in loc for s in cfg.USYD_MEDIUM):
        return int(cfg.WEIGHTS["location_usyd"] * 0.45), "离USYD 5-10km"
    if any(s in loc for s in ["sydney", "nsw", "new south wales"]):
        return int(cfg.WEIGHTS["location_usyd"] * 0.25), "悉尼"
    if any(s in loc for s in ["remote", "hybrid", "wfh", "work from home", "flexible"]):
        return int(cfg.WEIGHTS["location_usyd"] * 0.2), "远程/混合"
    return 0, ""


def score_job(job: JobPosting) -> JobPosting:
    title = job.title.lower()
    blob = job.text_blob()
    company = job.company.lower()
    pts = 0.0
    reasons: list[str] = []

    # 1) 标题是否含实习词（最高优先级，30分）
    intern_title = [w for w in ["intern", "internship", "vacation student", "placement", "co-op"]
                    if w in title]
    if intern_title:
        pts += cfg.WEIGHTS["title_intern"]
        reasons.append(f"实习岗: {intern_title[0]}")
    else:
        # 无 intern 字样但含 AI/ML 核心词 → 给 40% 加成（研究助理/项目类）
        ai_title = _hit_any(title, ["machine learning", "data science", "artificial intelligence",
                                     "computer vision", "deep learning", "robotics", "embodied",
                                     "research assistant", "nlp", "analytics"])
        if ai_title:
            pts += cfg.WEIGHTS["title_intern"] * 0.4
            reasons.append(f"AI/研究: {ai_title[0]}")

    # 2) AI/ML 领域（18分）
    ai_hits = _hit_any(blob, cfg.DOMAIN_AI)
    if ai_hits:
        pts += cfg.WEIGHTS["domain_ai"]
        reasons.append("AI/ML: " + ", ".join(ai_hits[:3]))

    # 3) 具身智能/机器人（8分）
    emb_hits = _hit_any(blob, cfg.DOMAIN_EMBODIED)
    if emb_hits:
        pts += cfg.WEIGHTS["domain_embodied"]
        reasons.append("具身/机器人: " + emb_hits[0])

    # 4) Digital Health（8分）
    health_hits = _hit_any(blob, cfg.DOMAIN_HEALTH)
    if health_hits:
        pts += cfg.WEIGHTS["domain_health"]
        reasons.append("Digital Health")

    # 5) 技能命中（最高12分，按命中数量线性累计）
    sk = _hit_any(blob, cfg.SKILLS)
    if sk:
        ratio = min(len(sk) / 4.0, 1.0)
        pts += cfg.WEIGHTS["skills"] * ratio
        reasons.append("技能: " + ", ".join(sorted({s.strip() for s in sk})[:4]))

    # 6) 目标雇主（10分）
    emp = _hit_any(company + " " + blob, cfg.TARGET_EMPLOYERS)
    if emp:
        pts += cfg.WEIGHTS["employer"]
        reasons.append(f"⭐ {emp[0]}")

    # 7) 资历匹配（±8分）
    good = _hit_any(blob, cfg.SENIORITY_GOOD)
    bad = _hit_any(blob, cfg.SENIORITY_BAD)
    if good and not bad:
        pts += cfg.WEIGHTS["seniority"]
        reasons.append("适合实习生")
    elif bad and not good:
        pts -= cfg.WEIGHTS["seniority"]
        reasons.append(f"⚠ 偏资深({bad[0]})")

    # 8) 离悉尼大学距离（最高12分）
    loc_pts, loc_label = _usyd_proximity(job.location)
    if loc_pts:
        pts += loc_pts
        if loc_label:
            reasons.append(f"📍 {loc_label}")

    # 9) PR/签证（±4分）
    if _hit_any(blob, cfg.VISA_GOOD):
        pts += cfg.WEIGHTS["visa"]
        reasons.append("PR友好")
    if _hit_any(blob, cfg.VISA_BAD):
        pts -= cfg.WEIGHTS["visa"]
        reasons.append("⚠ 需公民/clearance")

    # 10) 新鲜度（最高4分）
    if job.posted_days_ago is not None:
        if job.posted_days_ago <= 1:
            pts += cfg.WEIGHTS["recency"]
            reasons.append("今天新发")
        elif job.posted_days_ago <= 3:
            pts += cfg.WEIGHTS["recency"] * 0.6

    job.score = max(0, min(100, round(pts)))
    job.reasons = reasons
    return job


def score_all(jobs: list[JobPosting]) -> list[JobPosting]:
    scored = [score_job(j) for j in jobs]
    scored = [j for j in scored if j.score >= cfg.MIN_SCORE]
    scored.sort(key=lambda j: j.score, reverse=True)
    return scored[: cfg.MAX_RESULTS]
