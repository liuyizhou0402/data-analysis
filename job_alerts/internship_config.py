# -*- coding: utf-8 -*-
"""
悉尼实习机会雷达配置
目标岗位：AI / 具身智能 / Digital Health Data Science 方向实习
优先策略：离悉尼大学（Camperdown）近的岗位分数更高
每日目标：推送 ≥20 条
"""

# ============ 收件人（与健康数据雷达共用邮箱）============
DEFAULT_RECIPIENT = "1225265377@qq.com, yizhouliu612@gmail.com"

# ============ 个人画像 ============
PROFILE = {
    "name": "Yizhou Liu",
    "degree": "USYD Master of Digital Health & Data Science (MDHDS)",
    "grad_date": "2027-07",
    "visa": "PR",
    "base": "University of Sydney, Camperdown",
    "target_role": "AI / ML / Digital Health Intern",
    "open_to": ["internship", "intern", "student", "research assistant", "part-time", "casual"],
}

# ============ 搜索关键词 ============
SEARCH_KEYWORDS = [
    # AI/ML 实习核心词
    "machine learning intern",
    "data science intern",
    "AI intern",
    "artificial intelligence intern",
    "software engineer intern",
    "data engineer intern",
    # 专项 AI 技术
    "computer vision intern",
    "NLP intern",
    "deep learning intern",
    # 具身智能 / 机器人
    "robotics intern",
    "embodied AI",
    "autonomous systems intern",
    # Digital Health
    "digital health data",
    "health technology intern",
    "health data intern",
    # 广搜兜底（保量用）
    "technology intern",
    "analytics intern",
    "research intern AI",
]

SEARCH_LOCATION = "Sydney NSW"
SEARCH_LOCATION_ALT = ["Sydney", "New South Wales", "NSW", "Remote", "Hybrid"]

# ============ 离悉尼大学（Camperdown 主校区）距离分层 ============
# 步行/自行车可达（<2km）
USYD_VERY_CLOSE = [
    "camperdown", "darlington", "glebe", "newtown", "chippendale",
    "broadway", "ultimo", "forest lodge", "abbey hill",
]
# 公交15分钟内（2~5km）
USYD_CLOSE = [
    "pyrmont", "surry hills", "redfern", "haymarket", "central",
    "cbd", "city", "the rocks", "barangaroo", "millers point",
    "inner sydney", "sydney cbd", "sydney city", "eveleigh",
]
# 公交30分钟内（5~10km）
USYD_MEDIUM = [
    "balmain", "leichhardt", "stanmore", "annandale", "waterloo",
    "zetland", "alexandria", "marrickville", "erskineville",
    "st peters", "rozelle", "lilyfield", "ashfield",
    "north sydney", "st leonards", "crows nest", "chatswood",
    "macquarie park", "ryde", "meadowbank",
]

# ============ 打分关键词 ============
TITLE_CORE = [
    "intern", "internship", "student placement", "vacation",
    "machine learning", "artificial intelligence", "data science",
    "ai ", " ai", "ml ", "computer vision", "nlp",
    "deep learning", "research assistant", "robotics", "embodied",
    "digital health", "data analyst", "analytics",
]

DOMAIN_AI = [
    "machine learning", "artificial intelligence", "deep learning",
    "neural network", "computer vision", "nlp", "natural language",
    "reinforcement learning", "generative", "llm", "large language model",
    "foundation model", "pytorch", "tensorflow", "transformers",
    "data science", "predictive model", "classification", "clustering",
    "time series", "anomaly detection", "recommendation system",
]

DOMAIN_EMBODIED = [
    "robotics", "autonomous", "embodied", "robot", "manipulation",
    "perception", "slam", "ros", "motion planning", "simulation",
    "gazebo", "control systems", "mechatronics", "lidar", "sensor fusion",
    "embedded systems", "real-time", "edge ai", "tinyml",
]

DOMAIN_HEALTH = [
    "digital health", "health tech", "healthtech", "medtech", "ehealth",
    "clinical", "healthcare", "medical ai", "health data", "patient",
    "bioinformatics", "clinical nlp", "telehealth", "nsw health",
    "aged care", "hospital", "pharma", "biotech", "life science",
]

SKILLS = [
    "python", "pytorch", "tensorflow", "keras", "scikit-learn",
    "sql", " r,", " r ", "julia",
    "machine learning", "deep learning", "computer vision", "nlp",
    "reinforcement learning", "ros", "cuda", "gpu",
    "docker", "kubernetes", "aws", "gcp", "azure", "cloud",
    "git", "linux", "spark", "databricks",
    "statistics", "mathematical", "numpy", "pandas",
    "huggingface", "langchain", "openai api",
]

TARGET_EMPLOYERS = [
    # 大型科技（悉尼有办公室）
    "google", "microsoft", "amazon", "aws", "meta", "apple", "nvidia",
    "salesforce", "oracle", "ibm", "sap",
    # 澳洲独角兽/大厂
    "atlassian", "canva", "afterpay", "block", "safetyCulture",
    "wisetech", "xero", "zip", "tyro", "buildkite",
    # AI 公司
    "openai", "anthropic", "hugging face", "scale ai", "cohere",
    # Digital Health
    "resmed", "cochlear", "annalise", "harrison ai", "eucalyptus",
    "telstra health", "ehealth", "nsw health", "digital health agency",
    "adha", "roam analytics", "alcidion", "fred it",
    # 研究机构
    "csiro", "data61", "university of sydney", "usyd", "unsw", "uts",
    "macquarie university", "garvan", "the george institute",
    # 金融科技/AI
    "macquarie", "commonwealth bank", "cba", "westpac", "nab", "anz",
    "quantium", "mci solutions",
    # 机器人/制造
    "abb", "kuka", "boston dynamics", "clearpath",
]

SENIORITY_GOOD = [
    "intern", "internship", "student", "graduate", "entry", "junior",
    "trainee", "research assistant", "part-time", "casual",
    "vacation", "placement", "co-op", "early career",
]
SENIORITY_BAD = [
    "senior", "lead", "principal", "manager", "head of", "director",
    "5+ years", "7+ years", "10+ years", "expert", "specialist",
]

VISA_GOOD = [
    "permanent resident", "pr accepted", "no sponsorship",
    "full working rights", "valid working rights", "working rights",
    "australian citizen or pr", "must have full working",
]
VISA_BAD = [
    "must be an australian citizen", "citizenship is required",
    "security clearance", "baseline clearance", "nv1", "nv2",
    "australian citizens only",
]

# ============ 打分权重（总计约 104 满分，压缩到 0~100）============
WEIGHTS = {
    "title_intern":    30,   # 标题含 intern/internship 等实习词
    "domain_ai":       18,   # AI/ML 领域关键词
    "domain_embodied":  8,   # 具身智能/机器人领域
    "domain_health":    8,   # Digital Health 领域
    "skills":          12,   # 技能命中
    "employer":        10,   # 目标雇主
    "seniority":        8,   # 资历匹配（intern/junior 加分）
    "location_usyd":   12,   # 离悉尼大学距离（越近越高）
    "recency":          4,   # 新鲜度（最近发布优先）
    "visa":             4,   # PR/Working Rights 友好
}

MIN_SCORE = 25       # 较低阈值，保证每日 ≥20 条推送
MAX_RESULTS = 60     # 最多推送条数

# ============ 数据源开关 ============
SOURCES_ENABLED = {
    "linkedin":       True,
    "adzuna":         True,
    "seek":           True,
    "gradconnection": True,
    "prosple":        True,
    "indeed":         True,
    "jora":           True,   # 新增：SEEK 旗下聚合平台，中小企业覆盖好
}

PER_SOURCE_LIMIT = 30
