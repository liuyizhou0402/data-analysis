# -*- coding: utf-8 -*-
"""
个人求职画像 + 搜索/打分配置。
所有"我是谁、我要什么"的信息集中在这里，改这一个文件就能调整匹配逻辑。

背景来源：USYD《投递链接清单 · 健康数据方向》HTML + 研究生论文 R 代码技能。
"""

# ============ 收件人 ============
# 排名后的 job alert 发到这个邮箱（可被环境变量 JOB_ALERT_TO 覆盖）
DEFAULT_RECIPIENT = "1225265377@qq.com"

# ============ 个人画像 ============
PROFILE = {
    "name": "Yizhou Liu",
    "degree": "USYD Master of Digital Health & Data Science (MDHDS)",
    "grad_date": "2027-07",          # 一年制硕士，2027 年 7 月毕业
    "visa": "PR",                    # 永久居民，无需 sponsor，可投政府岗
    "base_city": "Sydney",
    "target_role": "Health Data Analyst",
    # 求职阶段：可接受 Graduate Program / casual / part-time / 实习 / RA
    "open_to": ["graduate", "casual", "part-time", "internship", "research assistant", "entry level"],
}

# ============ 搜索关键词（覆盖所有滚动岗位）============
# 每个关键词都会在各平台跑一遍，结果跨平台去重
SEARCH_KEYWORDS = [
    "health data analyst",
    "health data scientist",
    "clinical data analyst",
    "healthcare data analyst",
    "digital health analyst",
    "data analyst health",
    "graduate data analyst",
    "data analyst",
    "business intelligence analyst",
    "biostatistician",
]

# 地点（悉尼 + 远程）
SEARCH_LOCATION = "Sydney NSW"
SEARCH_LOCATION_ALT = ["Sydney", "New South Wales", "NSW", "Remote", "Hybrid"]

# ============ 打分维度关键词 ============
# 1) 职位标题里出现 = 强相关（核心命中）
TITLE_CORE = [
    "health data", "clinical data", "healthcare data", "digital health",
    "data analyst", "data scientist", "analytics", "business intelligence",
    "bi analyst", "biostatistic", "epidemiolog", "data engineer",
    "reporting analyst", "insights analyst",
]

# 2) 健康/医疗领域加分词（命中说明在我的目标行业）
DOMAIN_HEALTH = [
    "health", "clinical", "hospital", "medical", "patient", "ehealth",
    "nsw health", "medibank", "bupa", "ramsay", "healthcare", "care",
    "pharma", "biotech", "life science", "digital health", "telehealth",
    "epidemiolog", "public health", "wellbeing", "aged care",
]

# 3) 技能命中加分（来自论文 R 代码 + 课程 COMP5318 机器学习）
SKILLS = [
    "python", "r ", " r,", "sql", "machine learning", "ml", "comp5318",
    "power bi", "powerbi", "tableau", "statistics", "statistical",
    "regression", "survival analysis", "forecasting", "time series",
    "bioinformatics", "data visualisation", "data visualization",
    "etl", "snowflake", "databricks", "azure", "aws", "spark",
    "predictive model", "dashboard", "caret", "tidyverse", "ggplot",
]

# 4) 雇主目标清单（命中 = 我的 Top 雇主，强加分）
TARGET_EMPLOYERS = [
    "ehealth", "nsw health", "digital health agency", "adha",
    "telstra health", "oracle health", "harrison", "annalise",
    "eucalyptus", "deloitte", "kpmg", "accenture", "pwc", "ey",
    "medibank", "bupa", "nib", "ramsay", "st vincent", "csiro",
    "university of sydney", "unsw", "garvan", "westmead",
]

# 5) 资历匹配：这些是"对我友好"的级别词（加分）
SENIORITY_GOOD = [
    "graduate", "junior", "entry", "associate", "trainee", "cadet",
    "intern", "casual", "assistant", "early career", "campus",
]
# 这些是"超出我现阶段"的级别词（减分）
SENIORITY_BAD = [
    "senior", "lead", "principal", "manager", "head of", "director",
    "5+ years", "7+ years", "8+ years", "10+ years", "expert",
]

# 6) 签证/PR 信号
VISA_GOOD = [
    "permanent resident", "pr accepted", "no sponsorship", "australian citizen or permanent resident",
    "must have full working rights", "valid working rights",
]
VISA_BAD = [
    "must be an australian citizen", "citizenship is required", "baseline clearance required",
    "nv1", "nv2", "security clearance required", "australian citizens only",
]

# ============ 打分权重（总分映射到 0~100）============
WEIGHTS = {
    "title_core": 30,      # 标题强相关
    "domain_health": 22,   # 健康行业
    "skills": 18,          # 技能重合（按命中数量累计，封顶）
    "employer": 14,        # 目标雇主
    "seniority": 8,        # 资历匹配
    "location": 6,         # 地点在悉尼/远程
    "visa": 6,             # PR 友好
    "recency": 4,          # 最近发布
}

# 进入邮件的最低分（低于此分不打扰）
MIN_SCORE = 30
# 邮件里最多展示多少条
MAX_RESULTS = 45

# ============ 数据源开关 ============
# 关掉某个源就把它设成 False（例如某站长期被封时）
SOURCES_ENABLED = {
    "linkedin": True,      # 免登录 guest API（最稳）
    "adzuna": True,        # 官方聚合 API（最稳，需要免费 key，否则自动跳过）
    "seek": True,          # Playwright 抓搜索页
    "gradconnection": True,
    "prosple": True,
    "indeed": True,        # 反爬最凶，best-effort
}

# 每个关键词每个源最多取多少条（控制总量）
PER_SOURCE_LIMIT = 25
