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


def _is_relevant(job: JobPosting) -> bool:
    """关联门槛：必须命中至少一个目标领域（Data/DataAnalyst/AI/具身/Health），
    否则即便是实习岗也判定为「跑题」（如 Marketing/HR/Finance 实习）予以剔除。"""
    blob = job.text_blob()
    title = job.title.lower()
    if (_hit_any(blob, cfg.DOMAIN_DATA) or _hit_any(blob, cfg.DOMAIN_DATA_ANALYST)
            or _hit_any(blob, cfg.DOMAIN_AI) or _hit_any(blob, cfg.DOMAIN_EMBODIED)
            or _hit_any(blob, cfg.DOMAIN_HEALTH)):
        return True
    # 标题里直接含数据/AI/研究类词也算相关（覆盖描述抓取不全的情况）
    return bool(_hit_any(title, [
        "data", "analyt", "scientist", "machine learning", "intelligence",
        " ai", "ai ", " ml", "ml ", "robot", "health", "research",
    ]))


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
        # 无 intern 字样但标题含数据/AI 核心词 → 给 40% 加成（研究助理/项目/初级岗）
        core_title = _hit_any(title, [
            "data analyst", "data scientist", "data engineer", "data science",
            "business intelligence", "business analyst", "analytics", "data",
            "machine learning", "artificial intelligence", "computer vision",
            "deep learning", "robotics", "embodied", "research assistant", "nlp",
        ])
        if core_title:
            pts += cfg.WEIGHTS["title_intern"] * 0.4
            reasons.append(f"相关岗: {core_title[0]}")

    # 2) Data 广义数据方向（24分）—— 领域第一优先级
    data_hits = _hit_any(blob, cfg.DOMAIN_DATA)
    if data_hits:
        pts += cfg.WEIGHTS["domain_data"]
        reasons.append("Data: " + ", ".join(data_hits[:3]))

    # 3) Data Analyst 数据分析/BI（20分）—— 领域第二优先级
    da_hits = _hit_any(blob, cfg.DOMAIN_DATA_ANALYST)
    if da_hits:
        pts += cfg.WEIGHTS["domain_data_analyst"]
        reasons.append("Data Analyst: " + ", ".join(da_hits[:3]))

    # 4) AI/ML 领域（16分）
    ai_hits = _hit_any(blob, cfg.DOMAIN_AI)
    if ai_hits:
        pts += cfg.WEIGHTS["domain_ai"]
        reasons.append("AI/ML: " + ", ".join(ai_hits[:3]))

    # 5) 具身智能/机器人（10分）
    emb_hits = _hit_any(blob, cfg.DOMAIN_EMBODIED)
    if emb_hits:
        pts += cfg.WEIGHTS["domain_embodied"]
        reasons.append("具身/机器人: " + emb_hits[0])

    # 6) Digital Health（8分）
    health_hits = _hit_any(blob, cfg.DOMAIN_HEALTH)
    if health_hits:
        pts += cfg.WEIGHTS["domain_health"]
        reasons.append("Digital Health")

    # 7) 技能命中（最高6分，按命中数量线性累计，领域里优先级最低）
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
    """打分 + 过滤 + 排序。返回完整候选池（不截断），
    最终展示条数 / 保底补足由 main 决定（这样跨天去重后还能从池里补足到 30 条）。"""
    scored = [score_job(j) for j in jobs if _is_relevant(j)]
    scored = [j for j in scored if j.score >= cfg.MIN_SCORE]
    scored.sort(key=lambda j: j.score, reverse=True)
    return scored[:200]  # 200 条安全上限，足够支撑去重后补足
