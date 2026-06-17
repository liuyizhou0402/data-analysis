# -*- coding: utf-8 -*-
"""通过 Gmail SMTP 发送邮件（HTML + 纯文本双版本，提升送达率）。

复用仓库里已有的邮箱密钥（GitHub Secrets）：
  XHS_EMAIL_USER      —— 发件 Gmail 地址
  XHS_EMAIL_PASSWORD  —— Gmail 应用专用密码（App Password）
收件人默认 config.DEFAULT_RECIPIENT（可多个，逗号分隔），可用环境变量 JOB_ALERT_TO 覆盖。
"""
from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from . import config


def _recipients() -> list[str]:
    raw = os.environ.get("JOB_ALERT_TO") or config.DEFAULT_RECIPIENT
    return [a.strip() for a in raw.split(",") if a.strip()]


def send(subject: str, html_body: str, text_body: str = "") -> bool:
    # 去掉前后空格；应用专用密码常被复制成 "abcd efgh ijkl mnop"，中间空格也一并去掉
    user = (os.environ.get("XHS_EMAIL_USER") or "").strip()
    pwd = (os.environ.get("XHS_EMAIL_PASSWORD") or "").replace(" ", "").strip()
    to_list = _recipients()

    if not user or not pwd:
        print("⚠ 未配置 XHS_EMAIL_USER / XHS_EMAIL_PASSWORD，跳过发信（仅本地预览模式）。")
        return False

    # 把发件人自己也加进收件人（发给自己几乎必进收件箱，作为送达保底）
    if user not in to_list:
        to_list.append(user)

    # 安全诊断（不泄露密钥本身）：发件账号的域名 + 密码长度。
    domain = user.split("@")[-1] if "@" in user else "(无@，可能填错)"
    print(f"📧 发件 @{domain} · 应用密码长度 {len(pwd)}（Gmail 应为 16）· 收件: {', '.join(to_list)}")

    # multipart/alternative：先放纯文本、再放 HTML（规范顺序，能显著降低被判垃圾的概率）
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"岗位雷达 <{user}>"
    msg["To"] = ", ".join(to_list)
    msg["Reply-To"] = user
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=domain if "." in domain else "gmail.com")
    if not text_body:
        text_body = "今日岗位推荐（请用支持 HTML 的客户端查看完整排版）。"
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(user, pwd)
            server.sendmail(user, to_list, msg.as_string())
        print(f"✅ 邮件已发送至 {', '.join(to_list)}")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"❌ 发信失败: {e}")
        return False
