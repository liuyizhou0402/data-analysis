# -*- coding: utf-8 -*-
"""各招聘平台数据源。每个模块暴露 fetch(keyword, location, limit) -> list[JobPosting]。"""
from . import adzuna, gradconnection, indeed, jora, linkedin, prosple, seek

# 源名 -> fetch 函数
REGISTRY = {
    "linkedin": linkedin.fetch,
    "adzuna": adzuna.fetch,
    "seek": seek.fetch,
    "gradconnection": gradconnection.fetch,
    "prosple": prosple.fetch,
    "indeed": indeed.fetch,
    "jora": jora.fetch,
}

__all__ = ["REGISTRY"]
