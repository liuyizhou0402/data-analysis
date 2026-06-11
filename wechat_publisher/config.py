# -*- coding: utf-8 -*-
"""全局配置：资讯源、文章主题、热度打分关键词。"""

import os

# ---------------- 资讯源（RSS，免登录免 Cookie，可自行增删） ----------------
RSS_FEEDS = [
    # 国际教育行业媒体
    ("The PIE News", "https://thepienews.com/feed/"),
    ("ICEF Monitor", "https://monitor.icef.com/feed/"),
    ("Study International", "https://studyinternational.com/feed/"),
    # 澳洲
    ("SBS 中文", "https://www.sbs.com.au/language/chinese/zh-hans/feed"),
    ("The Conversation AU", "https://theconversation.com/au/education/articles.atom"),
    # 英国
    ("Times Higher Education", "https://www.timeshighereducation.com/feed"),
    ("GOV.UK 学生签证", "https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=uk-visas-and-immigration"),
    # 新西兰
    ("Education NZ", "https://www.education.govt.nz/rss"),
    ("RNZ", "https://www.rnz.co.nz/rss/national.xml"),
]

# 热度打分关键词（命中越多分越高），按主题相关性加权
HOT_KEYWORDS = {
    10: ["visa", "签证", "policy", "政策", "tuition", "学费", "scholarship", "奖学金",
         "ranking", "排名", "PSW", "485", "graduate route"],
    6:  ["australia", "澳洲", "澳大利亚", "new zealand", "新西兰", "uk", "英国", "britain",
         "international student", "留学生", "admission", "录取", "申请"],
    3:  ["university", "大学", "ielts", "雅思", "pte", "master", "硕士", "undergraduate",
         "本科", "immigration", "移民", "offer"],
}

# 每天三篇文章的主题模板（{major} 按星期几轮换）
ARTICLE_TOPICS = [
    {
        "slug": "aus-nz-hot",
        "title_hint": "澳洲/新西兰留学今日热点资讯盘点（按热度排序）",
        "focus": "澳大利亚和新西兰留学最新政策、签证、院校动态，按热度从高到低逐条解读，给出对申请人的实际影响和建议",
        "region_filter": ["australia", "澳洲", "澳大利亚", "new zealand", "新西兰", "nz"],
    },
    {
        "slug": "uk-apply",
        "title_hint": "英国留学申请最新动态与申请攻略",
        "focus": "英国留学最新资讯解读 + 英国硕士/本科申请流程、时间线、材料清单、避坑指南",
        "region_filter": ["uk", "英国", "britain", "london", "graduate route"],
    },
    {
        "slug": "major-guide",
        "title_hint": "{major}专业申请条件深度解析（澳洲/新西兰/英国对比）",
        "focus": "围绕{major}专业，对比澳洲八大、新西兰名校、英国名校的申请条件：学术背景、均分/GPA要求、语言要求（雅思/PTE）、学费、就业与移民前景",
        "region_filter": [],
    },
]

# 周一到周日轮换的专业
MAJORS_BY_WEEKDAY = ["商科/金融", "计算机/IT", "工程", "教育", "传媒", "护理/健康科学", "建筑/设计"]

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "output")

# Claude 模型
CLAUDE_MODEL = "claude-opus-4-8"

# 每篇文章参考的资讯条数
NEWS_PER_ARTICLE = 8
