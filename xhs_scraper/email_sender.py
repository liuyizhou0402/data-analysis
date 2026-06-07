"""
HTML email sender for the daily XHS study-abroad customer report.

Sends via QQ Mail SMTP.  Credentials are read from environment variables:
  XHS_EMAIL_USER      — sender address, e.g. example@qq.com
  XHS_EMAIL_PASSWORD  — QQ Mail authorization token (not your login password)

The email contains:
  - A styled HTML table with one row per user
  - A plain-text fallback for mail clients that don't render HTML
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


# ---------------------------------------------------------------------------
# HTML template helpers
# ---------------------------------------------------------------------------

_HTML_STYLE = """
<style>
  body { font-family: "Microsoft YaHei", Arial, sans-serif; color: #333; }
  h2 { color: #c0392b; }
  .summary { background: #f8f9fa; padding: 12px 16px; border-left: 4px solid #c0392b;
             margin-bottom: 20px; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th { background: #c0392b; color: #fff; padding: 8px 10px; text-align: left; }
  td { padding: 7px 10px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
  tr:nth-child(even) td { background: #fafafa; }
  .score-high { color: #27ae60; font-weight: bold; }
  .score-mid  { color: #e67e22; font-weight: bold; }
  .score-low  { color: #95a5a6; }
  a { color: #2980b9; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .footer { margin-top: 20px; font-size: 12px; color: #999; }
</style>
"""


def _score_class(score: int) -> str:
    if score >= 70:
        return "score-high"
    if score >= 40:
        return "score-mid"
    return "score-low"


def _build_html(users: list[dict[str, Any]], report_date: str) -> str:
    rows_html = ""
    for idx, user in enumerate(users, start=1):
        score = user.get("relevance_score", 0)
        reasons = user.get("match_reasons", [])
        reason_text = "；".join(reasons[:3]) if reasons else user.get("match_reason", "—")
        profile_url = user.get("profile_url", "#")
        nickname = user.get("nickname", "未知用户")
        source_kw = user.get("source_keyword", "—")
        sc = _score_class(score)

        rows_html += f"""
        <tr>
          <td>{idx}</td>
          <td><a href="{profile_url}" target="_blank">{nickname}</a></td>
          <td><a href="{profile_url}" target="_blank">查看主页</a></td>
          <td>{source_kw}</td>
          <td>{reason_text}</td>
          <td class="{sc}">{score}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">{_HTML_STYLE}</head>
<body>
<h2>📚 小红书意向留学客户日报</h2>
<div class="summary">
  <strong>报告日期：</strong>{report_date} &nbsp;|&nbsp;
  <strong>目标市场：</strong>英国 / 澳洲留学 &nbsp;|&nbsp;
  <strong>本次共发现：</strong>{len(users)} 位新潜在客户
</div>

<table>
  <thead>
    <tr>
      <th>序号</th>
      <th>昵称</th>
      <th>用户主页</th>
      <th>匹配关键词</th>
      <th>匹配原因</th>
      <th>相关度评分</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>

<div class="footer">
  此邮件由 XHS Study-Abroad Scraper 自动发送。如有疑问请联系系统管理员。<br>
  评分说明：≥70 高意向（绿色）、40-69 中意向（橙色）、&lt;40 低意向（灰色）
</div>
</body>
</html>"""
    return html


def _build_plain(users: list[dict[str, Any]], report_date: str) -> str:
    lines = [
        f"小红书意向留学客户日报 — {report_date}",
        f"共发现 {len(users)} 位新潜在客户（英国/澳洲留学方向）",
        "=" * 60,
    ]
    for idx, user in enumerate(users, start=1):
        score = user.get("relevance_score", 0)
        nickname = user.get("nickname", "未知用户")
        profile_url = user.get("profile_url", "N/A")
        source_kw = user.get("source_keyword", "—")
        reasons = user.get("match_reasons", [])
        reason_text = "；".join(reasons[:2]) if reasons else user.get("match_reason", "—")
        lines.append(
            f"{idx:>3}. {nickname}  [{source_kw}]  评分:{score}\n"
            f"     主页: {profile_url}\n"
            f"     原因: {reason_text}"
        )
    lines.append("=" * 60)
    lines.append("此邮件由自动系统生成，请勿直接回复。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SMTP send
# ---------------------------------------------------------------------------

def send_report(users: list[dict[str, Any]], report_date: str | None = None) -> bool:
    """
    Build and send the daily HTML report email.

    Returns True on success, False on failure (errors are logged, not raised).
    """
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    sender = config.EMAIL_SENDER
    password = config.EMAIL_PASSWORD
    recipient = config.EMAIL_RECIPIENT

    if not sender or not password:
        logger.error(
            "Email credentials not configured.  "
            "Set XHS_EMAIL_USER and XHS_EMAIL_PASSWORD environment variables."
        )
        return False

    subject = f"小红书意向留学客户日报 - {report_date}（{len(users)}位新用户）"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    plain_part = MIMEText(_build_plain(users, report_date), "plain", "utf-8")
    html_part = MIMEText(_build_html(users, report_date), "html", "utf-8")
    msg.attach(plain_part)
    msg.attach(html_part)  # HTML is preferred when supported

    try:
        if config.SMTP_USE_SSL:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT_SSL, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, [recipient], msg.as_string())
        else:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT_STARTTLS) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(sender, password)
                server.sendmail(sender, [recipient], msg.as_string())

        logger.info("Report email sent to %s (subject: %s)", recipient, subject)
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error(
            "SMTP authentication failed for %s.  "
            "Check that XHS_EMAIL_USER and XHS_EMAIL_PASSWORD are correct.  "
            "For QQ Mail, use an app-specific authorization token, not your login password.",
            sender,
        )
    except smtplib.SMTPException as exc:
        logger.error("SMTP error while sending report: %s", exc)
    except OSError as exc:
        logger.error("Network error while sending report: %s", exc)

    return False


def send_test_email() -> bool:
    """Send a minimal test email to verify SMTP credentials."""
    logger.info("Sending test email to %s …", config.EMAIL_RECIPIENT)
    fake_users: list[dict[str, Any]] = [
        {
            "user_id": "test001",
            "nickname": "测试用户_留学小助手",
            "profile_url": "https://www.xiaohongshu.com/user/profile/test001",
            "source_keyword": "英国留学",
            "match_reason": "这是一封测试邮件，用于验证邮件配置是否正常。",
            "match_reasons": ["测试匹配原因一", "测试匹配原因二"],
            "relevance_score": 85,
        }
    ]
    return send_report(fake_users, report_date=datetime.now().strftime("%Y-%m-%d") + "（测试）")
