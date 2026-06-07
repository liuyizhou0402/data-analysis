"""
悉尼大学新生获客清单邮件发送。
每行含：昵称、主页、匹配原因、相关度、**个性化开场白草稿**。
你打开邮件，点开主页，复制草稿手动私信——合规、真诚、高转化。
"""

from __future__ import annotations

import logging
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import config

logger = logging.getLogger(__name__)

_STYLE = """
<style>
  body { font-family: "Microsoft YaHei", Arial, sans-serif; color: #333; }
  h2 { color: #e8772e; }
  .summary { background: #fff7f0; padding: 12px 16px; border-left: 4px solid #e8772e; margin-bottom: 16px; }
  .tip { background: #f0f7ff; padding: 10px 14px; border-left: 4px solid #2980b9; margin-bottom: 20px; font-size: 13px; }
  .card { border: 1px solid #e8e8e8; border-radius: 8px; padding: 14px 16px; margin-bottom: 14px; }
  .card-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .nick { font-weight: bold; font-size: 15px; color: #222; }
  .score { background: #e8772e; color: #fff; border-radius: 12px; padding: 2px 10px; font-size: 12px; }
  .score-mid { background: #f0a04b; }
  .reason { font-size: 12px; color: #888; margin-bottom: 8px; }
  .draft { background: #fafafa; border-radius: 6px; padding: 10px 12px; font-size: 13px; color: #444; white-space: pre-wrap; border: 1px dashed #ddd; }
  .draft-label { font-size: 11px; color: #e8772e; font-weight: bold; margin-bottom: 4px; }
  a.btn { display: inline-block; background: #2980b9; color: #fff; text-decoration: none; padding: 4px 12px; border-radius: 4px; font-size: 12px; }
  .footer { margin-top: 20px; font-size: 12px; color: #aaa; }
</style>
"""


def _score_cls(s: int) -> str:
    return "score" if s >= 70 else "score score-mid"


def _build_html(users: list[dict[str, Any]], date: str) -> str:
    cards = ""
    for idx, u in enumerate(users, 1):
        score = u.get("relevance_score", 0)
        reasons = "；".join(u.get("match_reasons", [])[:4])
        url = u.get("profile_url", "#")
        nick = u.get("nickname", "未知")
        draft = u.get("opener_draft", "")
        cards += f"""
        <div class="card">
          <div class="card-head">
            <span class="nick">{idx}. {nick}</span>
            <span class="{_score_cls(score)}">相关度 {score}</span>
          </div>
          <div class="reason">{reasons}</div>
          <a class="btn" href="{url}" target="_blank">打开 ta 的主页 →</a>
          <div style="margin-top:10px;">
            <div class="draft-label">💬 开场白草稿（手动复制去私信）</div>
            <div class="draft">{draft}</div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">{_STYLE}</head><body>
<h2>🎓 悉尼大学新生获客清单</h2>
<div class="summary">
  <strong>日期：</strong>{date} &nbsp;|&nbsp;
  <strong>目标：</strong>2026/2027 入学悉大新生 &nbsp;|&nbsp;
  <strong>今日新发现：</strong>{len(users)} 位（已按回复可能性排序）
</div>
<div class="tip">
  ✅ <strong>合规使用说明：</strong>本清单帮你「找到人 + 备好话术」。请你<strong>手动</strong>点开主页、
  先给 ta 的笔记点个赞或留个真诚评论，再复制下方草稿私信。切勿批量群发——真诚互动转化率更高，也不会触发风控。
</div>
{cards}
<div class="footer">由悉大新生获客系统自动生成 · 仅发送至你本人邮箱 · 发送动作由你手动完成</div>
</body></html>"""


def _build_plain(users: list[dict[str, Any]], date: str) -> str:
    lines = [f"悉尼大学新生获客清单 — {date}", f"今日新发现 {len(users)} 位（按回复可能性排序）", "=" * 50]
    for idx, u in enumerate(users, 1):
        lines.append(f"\n{idx}. {u.get('nickname','未知')}  [相关度 {u.get('relevance_score',0)}]")
        lines.append(f"   主页: {u.get('profile_url','N/A')}")
        lines.append(f"   原因: {'；'.join(u.get('match_reasons', [])[:3])}")
        lines.append(f"   话术草稿: {u.get('opener_draft','')}")
    lines.append("\n" + "=" * 50)
    lines.append("请手动点开主页、真诚互动后再私信。切勿群发。")
    return "\n".join(lines)


def send_report(users: list[dict[str, Any]], date: str | None = None) -> bool:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    sender, pwd, to = config.EMAIL_SENDER, config.EMAIL_PASSWORD, config.EMAIL_RECIPIENT
    if not sender or not pwd:
        logger.error("邮件凭据未配置（XHS_EMAIL_USER / XHS_EMAIL_PASSWORD）")
        return False

    subject = f"悉尼大学新生获客清单 - {date}（{len(users)}位新发现）"
    msg = MIMEMultipart("alternative")
    msg["Subject"], msg["From"], msg["To"] = subject, sender, to
    msg.attach(MIMEText(_build_plain(users, date), "plain", "utf-8"))
    msg.attach(MIMEText(_build_html(users, date), "html", "utf-8"))

    try:
        if config.SMTP_USE_SSL:
            with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT_SSL, context=ssl.create_default_context()) as s:
                s.login(sender, pwd)
                s.sendmail(sender, [to], msg.as_string())
        else:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT_STARTTLS) as s:
                s.ehlo(); s.starttls(context=ssl.create_default_context()); s.ehlo()
                s.login(sender, pwd)
                s.sendmail(sender, [to], msg.as_string())
        logger.info("清单邮件已发送至 %s", to)
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP 认证失败，检查 QQ 邮箱授权码")
    except Exception as exc:
        logger.error("发送邮件出错: %s", exc)
    return False


def send_test_email() -> bool:
    fake = [{
        "user_id": "test001",
        "nickname": "悉大26fall新生",
        "profile_url": "https://www.xiaohongshu.com/user/profile/test001",
        "relevance_score": 90,
        "match_reasons": ["悉大身份：悉尼大学", "入学年份信号：26fall", "新生信号：offer", "互动意愿强：扩列"],
        "opener_draft": f"嗨悉大26fall新生～恭喜拿到悉大offer呀🎉 我也是26fall入学的，想拉个悉大留子扩列一起交流～方便的话加个微信呀：{config.YOUR_WECHAT}，一起抱团不迷路😄",
    }]
    return send_report(fake, datetime.now().strftime("%Y-%m-%d") + "（测试）")
