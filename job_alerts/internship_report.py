# -*- coding: utf-8 -*-
"""渲染悉尼实习机会雷达邮件（AI / 具身智能 / Digital Health 方向）。"""
from __future__ import annotations

import html
from datetime import datetime

from .sources.base import JobPosting


def _tier(score: int) -> tuple[str, str]:
    if score >= 65:
        return "强推 🔥", "#C0392B"
    if score >= 50:
        return "推荐", "#0891B2"
    if score >= 38:
        return "可投", "#6B3FA0"
    return "备选", "#64748B"


def _card(job: JobPosting, rank: int) -> str:
    label, color = _tier(job.score)
    tags = "".join(
        f'<span style="display:inline-block;font-size:11px;color:#4A5568;'
        f'background:#EDF2F7;border-radius:6px;padding:2px 8px;margin:2px 4px 2px 0;">'
        f"{html.escape(r)}</span>"
        for r in job.reasons[:6]
    )
    salary = (
        f'<span style="color:#007A3B;font-weight:600;">{html.escape(job.salary)}</span> &nbsp;·&nbsp; '
        if job.salary else ""
    )
    posted = f"&nbsp;·&nbsp; {html.escape(job.posted)}" if job.posted else ""
    return f"""
    <div style="background:#fff;border:1px solid #E2E8F0;border-left:4px solid {color};
                border-radius:10px;padding:14px 16px;margin-bottom:10px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:4px;">
        <div style="font-size:15px;font-weight:700;color:#0C1F35;flex:1;">
          {rank}. {html.escape(job.title)}
        </div>
        <div style="white-space:nowrap;font-size:13px;font-weight:700;color:{color};">
          {job.score}分&nbsp;·&nbsp;{label}
        </div>
      </div>
      <div style="font-size:13px;color:#4A5568;margin:4px 0 8px;">
        {html.escape(job.company or '—')}&nbsp;·&nbsp;{html.escape(job.location)}&nbsp;·&nbsp;
        <span style="color:#8B9BB0;">{html.escape(job.source)}</span>{posted}
      </div>
      <div style="margin-bottom:10px;">{salary}{tags}</div>
      <a href="{html.escape(job.url)}" target="_blank"
         style="display:inline-block;font-size:13px;font-weight:600;color:#fff;
                background:{color};text-decoration:none;border-radius:7px;padding:7px 18px;">
        查看&nbsp;/&nbsp;投递&nbsp;→
      </a>
    </div>
    """


def build_text(jobs: list[JobPosting], stats: dict) -> str:
    """纯文本版（邮件 fallback）。"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"悉尼实习机会雷达 · {today} · AI / 具身智能 / Digital Health", ""]
    if not jobs:
        lines.append("今天没有达到匹配阈值的新实习机会，明天会自动再试。")
    else:
        for i, j in enumerate(jobs, 1):
            label, _ = _tier(j.score)
            sal = f" · {j.salary}" if j.salary else ""
            lines.append(f"{i}. [{j.score}分/{label}] {j.title} — {j.company or '—'} "
                         f"({j.location}) [{j.source}]{sal}")
            lines.append(f"   {j.url}")
    lines += [
        "",
        "打分策略：实习标题(30) · AI/ML(18) · 具身/机器人(8) · Digital Health(8)",
        "         技能匹配(12) · 离USYD距离(12) · 目标雇主(10) · 级别匹配(8) · PR友好(4)",
    ]
    return "\n".join(lines)


def build_email(jobs: list[JobPosting], stats: dict) -> tuple[str, str]:
    """返回 (subject, html_body)。"""
    today = datetime.now().strftime("%Y-%m-%d")
    n = len(jobs)
    top = jobs[0].score if jobs else 0
    subject = f"【悉尼实习雷达】{today} · {n}个新机会（最高{top}分）"

    if not jobs:
        body_cards = (
            '<div style="background:#FFF7E6;border:1px solid #F59E0B;border-radius:10px;'
            'padding:16px;color:#92400E;">今天没有抓到符合条件的新实习机会——可能是各平台当天没有新发，'
            '或部分数据源被反爬拦截。明天会自动再试。</div>'
        )
    else:
        body_cards = "".join(_card(j, i + 1) for i, j in enumerate(jobs))

    src_line = " · ".join(f"{k}:{v}" for k, v in stats.get("by_source", {}).items()) or "无"

    return subject, f"""
    <div style="max-width:680px;margin:0 auto;
                font-family:-apple-system,Segoe UI,'PingFang SC',sans-serif;
                background:#F4F7FA;padding:20px;">

      <!-- 标题栏 -->
      <div style="background:linear-gradient(135deg,#1a1f3a 0%,#2d3561 100%);
                  border-radius:14px;padding:22px 24px;margin-bottom:14px;">
        <div style="color:#fff;font-size:20px;font-weight:700;">🤖 悉尼实习机会雷达</div>
        <div style="color:#93C5FD;font-size:13px;margin-top:6px;">
          {today} &nbsp;·&nbsp; AI / 具身智能 / Digital Health Data Science
          &nbsp;·&nbsp; 优先离悉尼大学近的岗位
        </div>
      </div>

      <!-- 打分说明条 -->
      <div style="background:#EFF6FF;border-radius:8px;padding:10px 14px;
                  font-size:12px;color:#1E40AF;margin-bottom:14px;line-height:1.6;">
        📍 <b>位置优先级</b>：Camperdown/Glebe/Newtown（步行可达）&gt;
        CBD/Pyrmont/Redfern（&lt;5km）&gt; 悉尼全域 &gt; 远程/混合<br>
        🎯 <b>领域优先级</b>：实习标题 &gt; AI/ML &gt; 具身/机器人 &gt; Digital Health &gt; 技能匹配
      </div>

      <!-- 统计摘要 -->
      <div style="font-size:13px;color:#4A5568;margin-bottom:14px;">
        本次共抓取 <b>{stats.get('raw', 0)}</b> 条，去重+过滤后命中
        <b>{n}</b> 条新实习机会（≥{stats.get('min_score', 0)}分）。
        来源：{html.escape(src_line)}
      </div>

      <!-- 岗位卡片 -->
      {body_cards}

      <!-- 脚注 -->
      <div style="font-size:11px;color:#8B9BB0;margin-top:18px;line-height:1.8;text-align:center;">
        打分维度：实习标题(30) · AI/ML领域(18) · 具身/机器人(8) · Digital Health(8) ·
        技能匹配(12) · 离USYD距离(12) · 目标雇主(10) · 级别匹配(8) · PR友好(4) · 新鲜度(4)<br>
        数据来源：LinkedIn · Seek · Adzuna · GradConnection · Prosple · Indeed · Jora<br>
        改 <code>job_alerts/internship_config.py</code> 可调整关键词、权重、雇主清单。
      </div>
    </div>
    """
