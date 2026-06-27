# -*- coding: utf-8 -*-
"""
第二封实习邮件配置 ——「悉尼名企 + 全球大厂 + 国内大厂线上」实习雷达

三条流（按用户优先级）：
  1️⃣ 悉尼 / 澳洲的【全球互联网大厂】实习（可线下，最高优先）
  2️⃣ USYD 对口的【健康数据方向】岗位（基于用户提供的 HTML 雇主清单全网筛选）
  3️⃣ 国内【大厂线上 / 远程】实习（必须线上，否则剔除，优先级最低）

每天去重、不重复推送；与第一封邮件（AI/具身/Digital Health）完全独立。
"""
from . import internship_config as base  # 复用 USYD 分区 / 领域词 / 技能词

# ============ 收件人（与第一封一致）============
DEFAULT_RECIPIENT = base.DEFAULT_RECIPIENT

# ============ 复用：离 USYD 距离分层 ============
USYD_VERY_CLOSE = base.USYD_VERY_CLOSE
USYD_CLOSE = base.USYD_CLOSE
USYD_MEDIUM = base.USYD_MEDIUM

# 复用领域 / 技能 / 资历词
DOMAIN_DATA = base.DOMAIN_DATA
DOMAIN_DATA_ANALYST = base.DOMAIN_DATA_ANALYST
DOMAIN_AI = base.DOMAIN_AI
DOMAIN_HEALTH = base.DOMAIN_HEALTH
SKILLS = base.SKILLS
SENIORITY_GOOD = base.SENIORITY_GOOD
SENIORITY_BAD = base.SENIORITY_BAD

# ============ ① 全球互联网大厂（悉尼/澳洲有岗即可，线下OK）============
SYDNEY_BIGTECH = [
    "google", "microsoft", "amazon", "aws", "meta", "facebook", "apple",
    "nvidia", "netflix", "salesforce", "oracle", "ibm", "sap", "adobe",
    "linkedin", "tiktok", "bytedance", "uber", "ebay", "paypal",
    "afterpay", "servicenow", "snowflake", "databricks", "stripe",
    "intel", "cisco", "samsung", "dell", "vmware", "qualcomm",
    # 澳洲本土全球级科技公司
    "atlassian", "canva", "wisetech", "safetyculture", "culture amp",
    "xero", "go1", "deputy", "linktree", "octopus deploy",
]

# ============ ② USYD 对口健康数据雇主（来自用户提供的 HTML 清单）============
HEALTH_TARGET_EMPLOYERS = [
    # 政府 & 公共健康系统
    "ehealth nsw", "ehealth", "nsw health", "iworkfor", "health nsw",
    "australian digital health agency", "digital health agency", "adha",
    # 健康科技公司
    "telstra health", "oracle health", "cerner",
    "harrison.ai", "harrison ai", "annalise.ai", "annalise",
    "eucalyptus", "resmed", "cochlear", "alcidion", "fred it",
    # 咨询 / 四大
    "deloitte", "kpmg", "accenture", "pwc", "ey", "ernst",
    # 保险 / 私立医院
    "medibank", "bupa", "nib", "ramsay", "st vincent", "svha", "healthscope",
    # 学术 / 科研
    "university of sydney", "usyd", "unsw", "csiro", "data61",
    "garvan", "the george institute", "westmead",
]

# 健康岗位角色关键词（即便雇主没命中，只要是健康数据角色也算对口）
HEALTH_ROLE_HINTS = [
    "health data", "clinical data", "digital health", "health analyt",
    "healthcare analyt", "epidemiolog", "biostatist", "bioinformatic",
    "clinical analyt", "patient data", "medical data", "health informatics",
    "population health", "health economic",
]

# ============ ③ 国内大厂（线上/远程实习用，名单见 sources/china_intern.py）============
from .sources.china_intern import CHINA_BIGTECH, REMOTE_MARKERS  # noqa: E402,F401

# ============ 搜索关键词 ============
# AU 流（同时服务①悉尼大厂实习 + ②健康对口岗）
SEARCH_KEYWORDS = [
    # —— 大厂技术实习（靠雇主打分把大厂顶上来）——
    "software engineer intern",
    "data analyst intern",
    "data scientist intern",
    "machine learning intern",
    "data science intern",
    "business analyst intern",
    "technology intern",
    "product intern",
    "graduate program data",
    # —— 健康数据对口（HTML 方向）——
    "health data analyst",
    "health data intern",
    "digital health intern",
    "clinical data analyst",
    "healthcare data analyst",
    "health analytics intern",
    "data analyst graduate",
    "business intelligence intern",
]

# 国内大厂线上实习检索词（强远程语义）
CHINA_KEYWORDS = [
    "远程实习",
    "线上实习",
    "在线实习",
    "数据 远程实习",
    "算法 远程实习",
    "data remote intern",
    "research remote intern",
]

SEARCH_LOCATION = "Sydney NSW"

# ============ 打分权重 ============
# 类别为互斥主加分，天然形成：悉尼大厂 > 健康对口 > 国内线上
WEIGHTS = {
    "title_intern":        28,   # 标题含实习词
    "cat_bigtech_syd":     32,   # 1️⃣ 悉尼/澳洲 全球互联网大厂实习（用户最高优先）
    "cat_health":          20,   # 2️⃣ USYD 对口健康数据岗
    "cat_china_online":    14,   # 3️⃣ 国内大厂线上实习
    "employer_star":       12,   # 命中具体目标雇主名（大厂或健康雇主）
    "domain_data_ai":      10,   # 数据/AI 相关度
    "seniority":            8,   # intern/junior 加分、senior 减分
    "location_usyd":       12,   # 离 USYD 距离（仅 AU 岗）
    "recency":              5,   # 新鲜度
    "remote_ok":           4,   # 远程/混合友好
}

# 类别展示优先级（数字越小越靠前）
CAT_PRIORITY = {"bigtech_syd": 0, "health": 1, "china_online": 2, "other": 9}

MIN_SCORE = 30
MIN_DAILY_RESULTS = 20   # 每日保底（不足时用候选池往期高分补足）
MAX_RESULTS = 50

# ============ 数据源开关 ============
# AU 源（服务①②流）
SOURCES_ENABLED = {
    "linkedin":       True,
    "adzuna":         True,
    "seek":           True,
    "gradconnection": True,
    "prosple":        True,
    "indeed":         True,
    "jora":           True,
}
# 国内线上实习源（服务③流）
CHINA_SOURCE_ENABLED = True

PER_SOURCE_LIMIT = 25

# ============ 邮件底部：HTML 雇主官方投递入口（常青参考）============
OFFICIAL_PORTALS = [
    ("eHealth NSW 招聘", "https://www.ehealth.nsw.gov.au/careers"),
    ("I Work for NSW · eHealth", "https://iworkfor.nsw.gov.au/nsw-health-ehealth-nsw"),
    ("ADHA 数字健康署", "https://www.digitalhealth.gov.au/about-us/careers"),
    ("Telstra Health", "https://www.livehire.com/careers/telstra-health/jobs"),
    ("Harrison.ai / Annalise.ai", "https://harrison.ai/careers/"),
    ("Eucalyptus", "https://www.eucalyptus.health/careers"),
    ("Deloitte 学生/毕业生", "https://www.deloitte.com/au/en/careers/students.html"),
    ("KPMG 毕业生", "https://kpmg.com/au/en/careers/graduates.html"),
    ("Medibank 毕业生", "https://careers.medibank.com.au/"),
    ("USYD 招聘门户", "https://usyd.wd105.myworkdayjobs.com/USYD_EXTERNAL_CAREER_SITE"),
    ("USYD CareerHub", "https://careerhub.sydney.edu.au/"),
    ("Atlassian 校招", "https://www.atlassian.com/company/careers/early-career"),
    ("Canva 校招", "https://www.lifeatcanva.com/en/early-careers/"),
]
