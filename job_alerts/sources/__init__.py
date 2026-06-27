# -*- coding: utf-8 -*-
"""各招聘平台数据源。每个模块暴露 fetch(keyword, location, limit) -> list[JobPosting]。"""
from . import (adzuna, china_intern, gradconnection, indeed, jora, linkedin,
               prosple, seek)

# 源名 -> fetch 函数
REGISTRY = {
    "linkedin": linkedin.fetch,
    "adzuna": adzuna.fetch,
    "seek": seek.fetch,
    "gradconnection": gradconnection.fetch,
    "prosple": prosple.fetch,
    "indeed": indeed.fetch,
    "jora": jora.fetch,
    "china_intern": china_intern.fetch,   # 第二封邮件专用（国内大厂线上实习）
}

__all__ = ["REGISTRY"]
