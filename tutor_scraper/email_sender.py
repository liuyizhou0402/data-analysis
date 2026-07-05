from __future__ import annotations

import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import config

logger = logging.getLogger(__name__)

_SOURCE_COLORS = {
    "Gumtree": "#00855a",
    "今日澳洲": "#e84118",
    "澳洲论坛": "#0097e6",
    "微博": "#e1392d",
}


def _source_badge(source: str) -> str:
    color = _SOURCE_COLORS.get(source, "#718093")
    return f'<span style="background:{color};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:bold;">{source}</span>'


def _score_bar(score: int) -> str:
    color = "#27ae60" if score >= 80 else "#f39c12" if score >= 60 else "#95a5a6"
    return f'<span style="color:{color};font-weight:bold;">{'★' * (score // 20)}{'☆' * (5 - score // 20)} {score}分</span>'


def _post_card(post: dict, idx: int) -> str:
    title = post.get("title", "（无标题）")
    content = post.get("content", "")[:300]
    url = post.get("url", "")
    source = post.get("source", "")
    location = post.get("location", "")
    price_signal = post.get("price_signal", "")
    contact_hint = post.get("contact_hint", "")
    score = post.get("score", 0)

    price_html = (
        f'<div style="background:#fff3cd;border-left:4px solid #f39c12;padding:6px 12px;margin:8px 0;font-size:14px;">'
        f'💰 <strong>价格信号：</strong>{price_signal}</div>'
    ) if price_signal else ""

    link_html = (
        f'<a href="{url}" style="display:inline-block;margin-top:8px;padding:7px 18px;'
        f'background:#2d3436;color:#fff;border-radius:6px;text-decoration:none;font-size:13px;">'
        f'查看原帖 →</a>'
    ) if url else ""

    return f"""
<div style="border:1px solid #dfe6e9;border-radius:10px;padding:18px;margin-bottom:16px;background:#fff;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <span style="background:#2d3436;color:#fff;border-radius:50%;width:26px;height:26px;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:bold;flex-shrink:0;">{idx}</span>
    {_source_badge(source)}
    {_score_bar(score)}
  </div>
  <h3 style="margin:0 0 6px 0;font-size:16px;color:#2d3436;">{title}</h3>
  <div style="color:#636e72;font-size:13px;margin-bottom:8px;">
    📍 {location} &nbsp;|&nbsp; 💬 {contact_hint}
  </div>
  {price_html}
  <p style="color:#2d3436;font-size:14px;line-height:1.6;margin:8px 0;">{content}{"..." if len(post.get("content","")) > 300 else ""}</p>
  {link_html}
</div>
"""


def _build_html(posts: list[dict], date: str) -> str:
    cards = "".join(_post_card(p, i + 1) for i, p in enumerate(posts))
    sources = ", ".join(sorted({p.get("source", "") for p in posts}))
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f6fa;margin:0;padding:0;}}
</style></head>
<body>
<div style="max-width:680px;margin:0 auto;padding:20px;">
  <div style="background:linear-gradient(135deg,#00b894,#00cec9);border-radius:12px;padding:28px;color:#fff;margin-bottom:20px;">
    <h1 style="margin:0 0 8px 0;font-size:22px;">🎓 悉尼高端家教需求清单</h1>
    <p style="margin:0;opacity:.9;font-size:14px;">{date} &nbsp;·&nbsp; 共 {len(posts)} 条 &nbsp;·&nbsp; 来源：{sources}</p>
  </div>
  <div style="background:#dfe6e9;border-radius:8px;padding:12px 16px;margin-bottom:20px;font-size:13px;color:#636e72;">
    ⚡ <strong>使用方法：</strong>点击「查看原帖」→ 在原平台回复或私信联系家长/学生，主动介绍自己的背景和经验，争取面试机会。
  </div>
  {cards}
  <div style="text-align:center;color:#b2bec3;font-size:12px;margin-top:20px;padding-top:16px;border-top:1px solid #dfe6e9;">
    每日早 9 点自动发送 · 高端家教需求自动筛选（≥$40/hr）
  </div>
</div>
</body></html>"""


def send_report(posts: list[dict], date: str) -> bool:
    if not config.EMAIL_USER or not config.EMAIL_PASSWORD:
        logger.warning("邮件未配置，跳过发送")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"【悉尼家教需求】{date} — {len(posts)} 条高端机会"
        msg["From"] = config.EMAIL_USER
        msg["To"] = config.EMAIL_RECIPIENT
        msg.attach(MIMEText(_build_html(posts, date), "html", "utf-8"))

        if config.SMTP_USE_SSL:
            with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT) as s:
                s.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
                s.sendmail(config.EMAIL_USER, config.EMAIL_RECIPIENT, msg.as_string())
        else:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as s:
                s.ehlo()
                s.starttls(context=ssl.create_default_context())
                s.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
                s.sendmail(config.EMAIL_USER, config.EMAIL_RECIPIENT, msg.as_string())

        logger.info("邮件发送成功 → %s", config.EMAIL_RECIPIENT)
        return True
    except Exception as e:
        logger.error("发送邮件出错: %s", e)
        return False


def send_test_email() -> bool:
    from datetime import datetime
    import config as cfg
    cfg.USE_MOCK_DATA = True
    import scraper
    posts = scraper.scrape_posts()[:3]
    return send_report(posts, datetime.now().strftime("%Y-%m-%d") + "（测试）")
