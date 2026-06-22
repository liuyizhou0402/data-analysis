# TikTok 广告代理商多维度消耗分析与归因看板 (2026)

一个高度还原 **TikTok 商业化引擎（GBS, Global Business Solutions）** 真实业务的 SQL 实战项目。
围绕「代理商（Agency）多地区、多行业广告消耗」数据，覆盖**数据建模 → 多维度归因 → 政策监控**
的完整分析链路，可直接复制到网页端跑通，也可写进简历作品集。

## 📂 项目结构

| 文件 | 作用 | 在 DB Fiddle 的位置 |
|------|------|----------------------|
| `01_setup.sql`   | 建表 + 灌入模拟数据（DDL + DML） | 左侧 **Schema** 窗口 |
| `02_queries.sql` | 三大核心面试必考查询             | 右侧 **Query** 窗口 |
| `README.md`      | 项目背景、运行方式、简历包装       | — |

## 💻 在哪里运行（明天面试前 30 分钟就能跑通）

不用本地装 MySQL/PostgreSQL，直接用免费网页端：

1. **DB Fiddle**（推荐，https://www.db-fiddle.com ）或 **SQL Fiddle**（http://sqlfiddle.com ）
   - 纯网页、免费、免注册。左上角数据库选 **MySQL 8.0** 或 **PostgreSQL 15**。
   - 左框贴 `01_setup.sql` → 右框贴 `02_queries.sql` 里的某道题 → 点 **Run**。
2. **LeetCode / HackerRank**（日常刷题练肌肉记忆）
   - LeetCode Database 板块，筛 Easy + Medium，重点刷 `JOIN`、`GROUP BY`、`Window Functions`。

## 🗃️ 数据模型

**`tfn_tiktok_agents`（代理商基础表 / 维度表）**

| 字段 | 类型 | 说明 |
|------|------|------|
| agent_id   | INT         | 代理商编号（主键） |
| agent_name | VARCHAR(50) | 代理商名称 |
| country    | VARCHAR(50) | 所属国家/地区 |
| tier       | VARCHAR(10) | 代理级别 Tier 1 / Tier 2 |

**`tfn_ad_spend_daily`（广告消耗流水表 / 事实表）**

| 字段 | 类型 | 说明 |
|------|------|------|
| log_date     | DATE          | 投放日期 |
| agent_id     | INT           | 代理商编号（关联维度表） |
| industry     | VARCHAR(50)   | 行业 |
| product_type | VARCHAR(50)   | 产品类型 |
| ad_spend_aud | DECIMAL(10,2) | 广告消耗金额（澳元 AUD） |

## 🧩 三大核心面试题（详见 `02_queries.sql`）

| # | 业务痛点 | 考察技能 |
|---|----------|----------|
| 1 | 2026/6 月澳洲各行业总消耗 | `JOIN` + `GROUP BY` 多维度聚合 |
| 2 | 找出高潜力黑马（6 月 vs 5 月环比增长率） | `WITH` CTE + 窗口函数 `LAG()` |
| 3 | 大促佣金返点政策达标监控 | 条件聚合 `CASE WHEN` |

**关键洞察**：第二题跑完会发现 **Agent 104 (Apex Marketing) 6 月环比增长 200%**——
这就是你为销售团队挖出来的高潜力 Tier 2 代理商，需要重点扶持。

> 方言提示：第二题里月份格式化是唯一的方言差异。MySQL 用 `DATE_FORMAT(log_date,'%Y-%m')`，
> PostgreSQL 用 `TO_CHAR(log_date,'YYYY-MM')`，文件里已写好两行，二选一即可。

## 📝 怎么写进简历（Portfolio）

**📂 项目名称：TikTok 广告代理商多维度消耗分析与归因看板 (2026)**

- **项目描述**：针对 TikTok 商业化引擎（GBS）中代理商的多地区、多行业广告消耗数据进行清洗、
  监控与深度挖掘，帮助销售团队识别高潜力客户并监控激励政策执行情况。
- **核心产出与技术栈（SQL & Python & Tableau）**：
  - **数据建模与提取**：熟练使用 SQL（高级 `JOIN`、`CASE WHEN`）对千万级代理商流水表与基础
    信息表进行关联，实现按国家、行业、产品线的多维度消耗聚合。
  - **多维度归因（Attribution Analysis）**：运用窗口函数 `LAG`/`LEAD` 编写环比增长模型，
    下钻（Drill-down）分析消耗异常波动的底层原因，成功在模拟数据中锁定月增长率达 200%
    的高潜力 Tier 2 代理商。
  - **政策监控看板**：利用条件判断逻辑对大促期间佣金激励政策达标率进行实时跟踪，为跨部门
    （Sales & Finance）项目管理提供实时数据决策支持。

## 🏁 面试前夜叮嘱

把这套标准流程甩给面试官：**数据清洗 → 窗口函数环比 → 多维度下钻归因 → 看板可视化**。
今晚把这三道题亲手敲一遍、看懂结果，那种对数据随心切片的掌控感就长在身上了。祝面试大获全胜！🎯
