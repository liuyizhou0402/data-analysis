# -*- coding: utf-8 -*-
"""第二封邮件打分引擎：三流分类 + 优先级排序。

类别（互斥）与优先级：
  bigtech_syd  悉尼/澳洲 全球互联网大厂实习   —— 最高
  health       USYD 对口健康数据岗            —— 次之
  china_online 国内大厂线上实习（必须线上）   —— 最低
不属于以上任何一类的 AU 岗位（other）会被过滤掉，保证邮件主题聚焦。
"""
from __future__ import annotations

import re

from . import career2_config as cfg
from .sources.base import JobPosting
from .sources.china_intern import _bigtech_name, _is_remote

_INTERN_WORDS = ["intern", "internship", "vacation", "placement", "co-op",
                 "实习", "trainee"]
_AU_LOC = ["sydney", "nsw", "new south wales", "australia", "melbourne",
           "brisbane", "perth", "adelaide", "canberra", "remote", "hybrid"]


def _hit_any(text: str, words: list[str]) -> list[str]:
    return [w for w in words if w and w in text]


def _hit_any_word(text: str, words: list[str]) -> list[str]:
    """按「单词边界」匹配雇主名，避免 'ey'(Ernst&Young) 命中 'sydney'、
    'sap' 命中 'sapphire' 这类子串误判。text/words 均应为小写。"""
    return [w for w in words if w and re.search(r"\b" + re.escape(w) + r"\b", text)]


def _usyd_proximity(location: str) -> tuple[int, str]:
    loc = (location or "").lower()
    if any(s in loc for s in cfg.USYD_VERY_CLOSE):
        return cfg.WEIGHTS["location_usyd"], "步行可达USYD"
    if any(s in loc for s in cfg.USYD_CLOSE):
        return int(cfg.WEIGHTS["location_usyd"] * 0.75), "离USYD<5km"
    if any(s in loc for s in cfg.USYD_MEDIUM):
        return int(cfg.WEIGHTS["location_usyd"] * 0.45), "离USYD 5-10km"
    if any(s in loc for s in ["sydney", "nsw", "new south wales"]):
        return int(cfg.WEIGHTS["location_usyd"] * 0.25), "悉尼"
    if any(s in loc for s in ["remote", "hybrid", "wfh", "work from home"]):
        return int(cfg.WEIGHTS["location_usyd"] * 0.2), "远程/混合"
    return 0, ""


def _classify(job: JobPosting) -> str:
    """判定类别。china_online 由数据源预先标记，这里只补判 AU 岗位。"""
    if job.category == "china_online":
        return "china_online"
    blob = job.text_blob()
    company_blob = (job.company + " " + blob).lower()
    is_au = any(s in blob for s in _AU_LOC) or any(s in (job.location or "").lower() for s in _AU_LOC)

    bigtech = _hit_any_word(company_blob, cfg.SYDNEY_BIGTECH)
    if bigtech and is_au:
        return "bigtech_syd"

    health_emp = _hit_any_word(company_blob, cfg.HEALTH_TARGET_EMPLOYERS)
    health_role = _hit_any(blob, cfg.HEALTH_ROLE_HINTS) or _hit_any(blob, cfg.DOMAIN_HEALTH)
    if (health_emp or health_role) and is_au:
        return "health"
    return "other"


def score_job(job: JobPosting) -> JobPosting:
    title = job.title.lower()
    blob = job.text_blob()
    company_blob = (job.company + " " + blob).lower()
    pts = 0.0
    reasons: list[str] = []

    cat = _classify(job)
    job.category = cat

    # —— 类别主加分（互斥）+ 各类硬规则 ——
    if cat == "china_online":
        # 硬规则：必须线上 + 必须大厂，否则判 0 分（后续过滤掉）
        bt = _bigtech_name(company_blob)
        if not _is_remote(blob) or not bt:
            job.score = 0
            job.category = "other"
            return job
        pts += cfg.WEIGHTS["cat_china_online"]
        reasons.append(f"🇨🇳 国内大厂线上: {bt}")
        pts += cfg.WEIGHTS["remote_ok"]
    elif cat == "bigtech_syd":
        bigtech = _hit_any_word(company_blob, cfg.SYDNEY_BIGTECH)
        pts += cfg.WEIGHTS["cat_bigtech_syd"]
        reasons.append(f"🏢 悉尼全球大厂: {bigtech[0]}")
    elif cat == "health":
        pts += cfg.WEIGHTS["cat_health"]
        health_emp = _hit_any_word(company_blob, cfg.HEALTH_TARGET_EMPLOYERS)
        if health_emp:
            reasons.append(f"🩺 USYD对口雇主: {health_emp[0]}")
        else:
            reasons.append("🩺 USYD对口健康数据岗")
    else:
        # other：不属于三流主题 —— 直接出局
        job.score = 0
        return job

    # —— 标题实习词 ——
    if _hit_any(title, _INTERN_WORDS):
        pts += cfg.WEIGHTS["title_intern"]
        reasons.append("实习岗")
    elif _hit_any(title, ["graduate", "junior", "entry", "campus", "校招", "毕业生"]):
        pts += cfg.WEIGHTS["title_intern"] * 0.5
        reasons.append("毕业生/初级")

    # —— 命中具体目标雇主名（大厂或健康雇主）——
    star = _hit_any_word(company_blob, cfg.SYDNEY_BIGTECH + cfg.HEALTH_TARGET_EMPLOYERS)
    if star:
        pts += cfg.WEIGHTS["employer_star"]

    # —— 数据/AI 相关度 ——
    if _hit_any(blob, cfg.DOMAIN_DATA) or _hit_any(blob, cfg.DOMAIN_DATA_ANALYST):
        pts += cfg.WEIGHTS["domain_data_ai"]
        reasons.append("数据方向")
    elif _hit_any(blob, cfg.DOMAIN_AI):
        pts += cfg.WEIGHTS["domain_data_ai"] * 0.7
        reasons.append("AI/ML方向")

    # —— 资历匹配 ——
    good = _hit_any(blob, cfg.SENIORITY_GOOD)
    bad = _hit_any(blob, cfg.SENIORITY_BAD)
    if good and not bad:
        pts += cfg.WEIGHTS["seniority"]
    elif bad and not good:
        pts -= cfg.WEIGHTS["seniority"]
        reasons.append(f"⚠ 偏资深({bad[0]})")

    # —— 离 USYD 距离（仅 AU 岗）——
    if cat != "china_online":
        loc_pts, loc_label = _usyd_proximity(job.location)
        if loc_pts:
            pts += loc_pts
            if loc_label:
                reasons.append(f"📍 {loc_label}")

    # —— 新鲜度 ——
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
    """打分 + 过滤（只保留三流）+ 排序（类别优先级 → 分数）。返回完整候选池。"""
    scored = [score_job(j) for j in jobs]
    scored = [j for j in scored
              if j.score >= cfg.MIN_SCORE and j.category in cfg.CAT_PRIORITY
              and j.category != "other"]
    scored.sort(key=lambda j: (cfg.CAT_PRIORITY.get(j.category, 9), -j.score))
    return scored[:200]
