# -*- coding: utf-8 -*-
"""把打好分、排好序的岗位渲染成一封好看的 HTML 邮件。"""
from __future__ import annotations

import html
from datetime import datetime

from .sources.base import JobPosting


def _tier(score: int) -> tuple[str, str]:
    if score >= 70:
        return "强烈推荐", "#00A651"
    if score >= 55:
        return "高匹配", "#0891B2"
    if score >= 42:
        return "可关注", "#6B3FA0"
    return "补充", "#64748B"


def _card(job: JobPosting, rank: int) -> str:
    label, color = _tier(job.score)
    reasons = "".join(
        f'<span style="display:inline-block;font-size:11px;color:#4A5568;'
        f'background:#EDF2F7;border-radius:6px;padding:2px 8px;margin:2px 4px 2px 0;">'
        f"{html.escape(r)}</span>"
        for r in job.reasons[:5]
    )
    salary = (
        f'<span style="color:#007A3B;font-weight:600;">{html.escape(job.salary)}</span> · '
        if job.salary else ""
    )
    posted = f" · {html.escape(job.posted)}" if job.posted else ""
    return f"""
    <div style="background:#fff;border:1px solid #E2E8F0;border-left:4px solid {color};
                border-radius:10px;padding:14px 16px;margin-bottom:10px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div style="font-size:15px;font-weight:700;color:#0C1F35;">
          {rank}. {html.escape(job.title)}
        </div>
        <div style="white-space:nowrap;font-size:13px;font-weight:700;color:{color};">
          {job.score} 分 · {label}
        </div>
      </div>
      <div style="font-size:13px;color:#4A5568;margin:4px 0 8px;">
        {html.escape(job.company or '—')} · {html.escape(job.location)} ·
        <span style="color:#8B9BB0;">{html.escape(job.source)}</span>{posted}
      </div>
      <div style="margin-bottom:8px;">{salary}{reasons}</div>
      <a href="{html.escape(job.url)}" target="_blank"
         style="display:inline-block;font-size:13px;font-weight:600;color:#fff;
                background:{color};text-decoration:none;border-radius:7px;padding:7px 16px;">
        查看 / 投递 →
      </a>
    </div>
    """


def build_text(jobs: list[JobPosting], stats: dict) -> str:
    """纯文本版（邮件 fallback + 提升送达率）。"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"每日健康数据岗位雷达 · {today} · Sydney", ""]
    if not jobs:
        lines.append("今天没有达到匹配阈值的新岗位，明天会自动再试。")
    else:
        for i, j in enumerate(jobs, 1):
            label, _ = _tier(j.score)
            sal = f" · {j.salary}" if j.salary else ""
            lines.append(f"{i}. [{j.score}分/{label}] {j.title} — {j.company or '—'} "
                         f"({j.location}) [{j.source}]{sal}")
            lines.append(f"   {j.url}")
    lines.append("")
    lines.append("打分基于 USYD MDHDS 健康数据画像。改 job_alerts/config.py 可调权重。")
    return "\n".join(lines)


def build_email(jobs: list[JobPosting], stats: dict) -> tuple[str, str]:
    """返回 (subject, html_body)。"""
    today = datetime.now().strftime("%Y-%m-%d")
    n = len(jobs)
    top = jobs[0].score if jobs else 0
    subject = f"【每日岗位雷达】{today} · {n} 个新匹配（最高 {top} 分）"

    if not jobs:
        body_cards = (
            '<div style="background:#FFF7E6;border:1px solid #F59E0B;border-radius:10px;'
            'padding:16px;color:#92400E;">今天没有抓到达到匹配阈值的新岗位。可能是各招聘站'
            '当天没有新发健康数据岗，或部分数据源被反爬拦截——明天会自动再试。</div>'
        )
    else:
        body_cards = "".join(_card(j, i + 1) for i, j in enumerate(jobs))

    src_line = " · ".join(f"{k}:{v}" for k, v in stats.get("by_source", {}).items()) or "无"

    return subject, f"""
    <div style="max-width:680px;margin:0 auto;font-family:-apple-system,Segoe UI,'PingFang SC',sans-serif;
                background:#F4F7FA;padding:20px;">
      <div style="background:#0C1F35;border-radius:14px;padding:22px 24px;margin-bottom:16px;">
        <div style="color:#fff;font-size:20px;font-weight:700;">🎯 每日健康数据岗位雷达</div>
        <div style="color:#7AAEC8;font-size:13px;margin-top:4px;">
          {today} · Sydney · 按匹配度从高到低排序 · 已自动跨天去重
        </div>
      </div>
      <div style="font-size:13px;color:#4A5568;margin-bottom:14px;">
        本次共抓取 <b>{stats.get('raw', 0)}</b> 条，去重+过滤后命中
        <b>{n}</b> 条新匹配（≥{stats.get('min_score', 0)}分）。
        来源：{html.escape(src_line)}
      </div>
      {body_cards}
      <div style="font-size:11px;color:#8B9BB0;margin-top:18px;line-height:1.7;text-align:center;">
        打分维度：标题相关 / 健康行业 / 技能重合(R·Python·ML·BI) / 目标雇主 / 资历适配 /
        悉尼地点 / PR友好 / 新鲜度。<br>
        画像基于 USYD MDHDS · 健康数据方向 · 2027年7月毕业 · PR。改 job_alerts/config.py 可调权重。
      </div>
    </div>
    """
