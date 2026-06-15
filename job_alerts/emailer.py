# -*- coding: utf-8 -*-
"""通过 Gmail SMTP 发送 HTML 邮件。

复用仓库里已有的邮箱密钥（GitHub Secrets）：
  XHS_EMAIL_USER      —— 发件 Gmail 地址
  XHS_EMAIL_PASSWORD  —— Gmail 应用专用密码（App Password）
收件人默认 config.DEFAULT_RECIPIENT，可用环境变量 JOB_ALERT_TO 覆盖。
"""
from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import config


def send(subject: str, html_body: str) -> bool:
    # 去掉前后空格；应用专用密码常被复制成 "abcd efgh ijkl mnop"，中间空格也一并去掉
    user = (os.environ.get("XHS_EMAIL_USER") or "").strip()
    pwd = (os.environ.get("XHS_EMAIL_PASSWORD") or "").replace(" ", "").strip()
    # 注意：未设置的 GitHub Secret 会以空字符串注入，所以要 or 兜底
    to_addr = os.environ.get("JOB_ALERT_TO") or config.DEFAULT_RECIPIENT

    if not user or not pwd:
        print("⚠ 未配置 XHS_EMAIL_USER / XHS_EMAIL_PASSWORD，跳过发信（仅本地预览模式）。")
        return False

    # 安全诊断（不泄露密钥本身）：发件账号的域名 + 密码长度。
    # Gmail 应用专用密码应为 16 位；若长度不是 16，多半是贴错（贴成了登录密码）。
    domain = user.split("@")[-1] if "@" in user else "(无@，可能填错)"
    print(f"📧 发件账号域名: @{domain} · 应用密码长度: {len(pwd)}（Gmail 应为 16）· 收件: {to_addr}")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"岗位雷达 <{user}>"
    msg["To"] = to_addr
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(user, pwd)
            server.sendmail(user, [to_addr], msg.as_string())
        print(f"✅ 邮件已发送至 {to_addr}")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"❌ 发信失败: {e}")
        return False
