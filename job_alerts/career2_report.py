# -*- coding: utf-8 -*-
"""渲染第二封邮件：悉尼名企 + 全球大厂 + 国内大厂线上 实习雷达（三段式）。"""
from __future__ import annotations

import html
from datetime import datetime

from . import career2_config as cfg
from .sources.base import JobPosting

# 类别 -> (标题, 主题色, 副说明)
CAT_META = {
    "bigtech_syd": ("🏢 悉尼 / 澳洲 · 全球互联网大厂实习", "#1D4ED8", "可线下 · 用户最高优先"),
    "health":      ("🩺 USYD 对口 · 健康数据方向", "#059669", "基于你的雇主清单全网筛选"),
    "china_online": ("🇨🇳 国内大厂 · 线上 / 远程实习", "#DC2626", "仅线上，可在悉尼远程参与"),
}
CAT_ORDER = ["bigtech_syd", "health", "china_online"]


def _tier(score: int) -> tuple[str, str]:
    if score >= 75:
        return "强推 🔥", "#C0392B"
    if score >= 60:
        return "推荐", "#0891B2"
    if score >= 45:
        return "可投", "#6B3FA0"
    return "备选", "#64748B"


def _card(job: JobPosting, rank: int) -> str:
    label, color = _tier(job.score)
    backfill_badge = (
        '<span style="display:inline-block;font-size:10px;color:#92400E;'
        'background:#FEF3C7;border-radius:5px;padding:1px 6px;margin-left:6px;">往期</span>'
        if job.is_backfill else ""
    )
    tags = "".join(
        f'<span style="display:inline-block;font-size:11px;color:#4A5568;'
        f'background:#EDF2F7;border-radius:6px;padding:2px 8px;margin:2px 4px 2px 0;">'
        f"{html.escape(r)}</span>"
        for r in job.reasons[:5]
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
          {rank}. {html.escape(job.title)}{backfill_badge}
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


def _section(cat: str, jobs: list[JobPosting], start_rank: int) -> str:
    if not jobs:
        return ""
    title, color, sub = CAT_META[cat]
    head = (
        f'<div style="margin:18px 0 10px;">'
        f'<div style="font-size:16px;font-weight:800;color:{color};">{title}'
        f'<span style="font-size:12px;font-weight:600;color:#8B9BB0;">'
        f'&nbsp;·&nbsp;{len(jobs)}个</span></div>'
        f'<div style="font-size:12px;color:#8B9BB0;margin-top:2px;">{sub}</div></div>'
    )
    cards = "".join(_card(j, start_rank + i) for i, j in enumerate(jobs))
    return head + cards


def build_text(jobs: list[JobPosting], stats: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"悉尼名企实习雷达（第二封）· {today}", ""]
    if not jobs:
        lines.append("今天没有抓到符合三大方向的新机会，明天自动再试。")
    else:
        rank = 1
        for cat in CAT_ORDER:
            seg = [j for j in jobs if j.category == cat]
            if not seg:
                continue
            lines.append(f"【{CAT_META[cat][0]}】")
            for j in seg:
                sal = f" · {j.salary}" if j.salary else ""
                flag = " [往期]" if j.is_backfill else ""
                lines.append(f"  {rank}. [{j.score}分]{flag} {j.title} — {j.company or '—'} "
                             f"({j.location}) [{j.source}]{sal}")
                lines.append(f"     {j.url}")
                rank += 1
            lines.append("")
    return "\n".join(lines)


def build_email(jobs: list[JobPosting], stats: dict) -> tuple[str, str]:
    today = datetime.now().strftime("%Y-%m-%d")
    by_cat = {c: [j for j in jobs if j.category == c] for c in CAT_ORDER}
    n = len(jobs)
    a, b, c = len(by_cat["bigtech_syd"]), len(by_cat["health"]), len(by_cat["china_online"])
    subject = f"【悉尼名企实习雷达】{today} · 共{n}个（大厂{a}/健康{b}/国内线上{c}）"

    if not jobs:
        body_sections = (
            '<div style="background:#FFF7E6;border:1px solid #F59E0B;border-radius:10px;'
            'padding:16px;color:#92400E;">今天三大方向都没抓到新机会——可能是平台当天无新发或被反爬拦截，'
            '明天会自动再试。下方为常青投递入口，可手动查看。</div>'
        )
    else:
        body_sections = ""
        rank = 1
        for cat in CAT_ORDER:
            seg = by_cat[cat]
            body_sections += _section(cat, seg, rank)
            rank += len(seg)

    # 底部常青官方入口
    portals = "".join(
        f'<a href="{html.escape(u)}" target="_blank" '
        f'style="display:inline-block;font-size:12px;color:#1D4ED8;text-decoration:none;'
        f'background:#EFF6FF;border:1px solid #DBEAFE;border-radius:7px;'
        f'padding:6px 11px;margin:3px 5px 3px 0;">{html.escape(name)} →</a>'
        for name, u in cfg.OFFICIAL_PORTALS
    )
    src_line = " · ".join(f"{k}:{v}" for k, v in stats.get("by_source", {}).items()) or "无"

    return subject, f"""
    <div style="max-width:680px;margin:0 auto;
                font-family:-apple-system,Segoe UI,'PingFang SC',sans-serif;
                background:#F4F7FA;padding:20px;">

      <div style="background:linear-gradient(135deg,#0f2027 0%,#203a43 50%,#2c5364 100%);
                  border-radius:14px;padding:22px 24px;margin-bottom:14px;">
        <div style="color:#fff;font-size:20px;font-weight:700;">🎯 悉尼名企实习雷达 · 第二封</div>
        <div style="color:#93C5FD;font-size:13px;margin-top:6px;">
          {today} &nbsp;·&nbsp; 悉尼全球大厂实习 + USYD对口健康岗 + 国内大厂线上实习
        </div>
      </div>

      <div style="background:#EFF6FF;border-radius:8px;padding:10px 14px;
                  font-size:12px;color:#1E40AF;margin-bottom:8px;line-height:1.6;">
        🥇 <b>优先级</b>：悉尼/澳洲全球互联网大厂实习（可线下）&gt;
        USYD对口健康数据岗 &gt; 国内大厂线上实习（必须线上）<br>
        🔁 每天去重，重复机会不再出现；离悉尼大学越近分越高
      </div>

      <div style="font-size:13px;color:#4A5568;margin-bottom:6px;">
        本次抓取 <b>{stats.get('raw', 0)}</b> 条，过滤+去重后推送
        <b>{n}</b> 条（今日新增 <b>{stats.get('n_new', n)}</b>
        {('，往期补充 <b>' + str(stats.get('n_backfill', 0)) + '</b>') if stats.get('n_backfill', 0) else ''}）。
        来源：{html.escape(src_line)}
      </div>

      {body_sections}

      <div style="margin-top:22px;padding-top:14px;border-top:1px dashed #CBD5E1;">
        <div style="font-size:13px;font-weight:700;color:#0C1F35;margin-bottom:8px;">
          🔗 对口雇主官方投递入口（常青参考）
        </div>
        <div>{portals}</div>
      </div>

      <div style="font-size:11px;color:#8B9BB0;margin-top:18px;line-height:1.8;text-align:center;">
        优先级：悉尼全球大厂(32) · USYD健康对口(20) · 国内线上(14) · 实习标题(28) · 雇主(12) · 离USYD(12)<br>
        国内大厂实习已强制「仅线上/远程」过滤；与第一封（AI/具身/Digital Health）独立去重<br>
        数据来源：LinkedIn · Seek · Adzuna · GradConnection · Prosple · Indeed · Jora · 腾讯招聘 · 实习僧
      </div>
    </div>
    """
