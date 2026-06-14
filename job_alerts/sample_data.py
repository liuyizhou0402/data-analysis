# -*- coding: utf-8 -*-
"""样例岗位数据：用于本地预览邮件排版 + 验证打分逻辑（无需联网）。

正式运行（--now）走真实抓取，不会用到这里。
"""
from .sources.base import JobPosting

JOBS = [
    JobPosting(
        title="Graduate Health Data Analyst",
        company="eHealth NSW",
        location="Sydney, NSW",
        url="https://iworkfor.nsw.gov.au/job/health-data-analyst",
        source="Seek",
        description=("Join eHealth NSW as a graduate health data analyst. Work with "
                     "clinical datasets, build Power BI dashboards, SQL, Python. "
                     "Australian Citizen or Permanent Resident. Entry level."),
        salary="$95,000 – $110,000",
        posted="今天", posted_days_ago=0,
    ),
    JobPosting(
        title="Clinical Data Analyst (Entry Level)",
        company="Telstra Health",
        location="Sydney, NSW (Hybrid)",
        url="https://www.livehire.com/careers/telstra-health/clinical-data-analyst",
        source="LinkedIn",
        description=("Healthcare IT. Junior analyst, statistics, machine learning, "
                     "data visualisation, Tableau. Valid working rights required."),
        salary="$100,000 – $120,000",
        posted="1 day ago", posted_days_ago=1,
    ),
    JobPosting(
        title="Data Analyst - Digital Health",
        company="Australian Digital Health Agency",
        location="Sydney / Remote",
        url="https://www.digitalhealth.gov.au/careers/data-analyst",
        source="Adzuna",
        description=("Associate data analyst, SQL, Python, regression, reporting. "
                     "Graduate program pathway. Health domain."),
        salary="$90,000 – $130,000",
        posted="2026-06-12",
    ),
    JobPosting(
        title="Biostatistician / Data Scientist",
        company="Garvan Institute",
        location="Darlinghurst, Sydney",
        url="https://www.garvan.org.au/careers/biostatistician",
        source="Indeed",
        description=("Bioinformatics, R, caret, survival analysis, ggplot, "
                     "statistical modelling, clinical research. Research assistant friendly."),
        salary="$85,000 – $115,000",
        posted="3 days ago", posted_days_ago=3,
    ),
    JobPosting(
        title="Health Analytics Graduate Program 2027",
        company="Medibank",
        location="Sydney, NSW",
        url="https://careers.medibank.com.au/graduate/health-analytics",
        source="GradConnection",
        description=("Graduate program, data analytics, business intelligence, "
                     "Power BI, SQL, health insurance domain. Campus hire."),
        posted="2026-06-10",
    ),
    JobPosting(
        title="Senior Data Engineer (10+ years)",
        company="Random Bank",
        location="Melbourne, VIC",
        url="https://example.com/senior-data-engineer",
        source="Seek",
        description=("Senior, lead, principal data engineer. 10+ years. Spark, AWS. "
                     "Must be an Australian Citizen, security clearance required."),
        salary="$180,000+",
        posted="5 days ago", posted_days_ago=5,
    ),
    JobPosting(
        title="Business Intelligence Analyst",
        company="Ramsay Health Care",
        location="Sydney, NSW",
        url="https://www.ramsaycareers.com.au/bi-analyst",
        source="Prosple",
        description=("BI analyst, hospital, dashboards, SQL, Power BI, healthcare. "
                     "Early career welcome."),
        salary="$90,000 – $105,000",
        posted="2026-06-13",
    ),
    JobPosting(
        title="Marketing Coordinator",
        company="Some Retail Co",
        location="Sydney, NSW",
        url="https://example.com/marketing",
        source="Indeed",
        description="Marketing, social media, events. No data required.",
        posted="1 day ago", posted_days_ago=1,
    ),
]
