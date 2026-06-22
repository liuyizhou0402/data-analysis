-- =============================================================
--  SQL 项目 · 查询示例 (Queries)
--  从“看全表”到“面试加分”的进阶查询合集
--  运行前请先执行 01_schema.sql 和 02_seed_data.sql
-- =============================================================

-- =============================================================
--  PART A · 最基础：看整张表 (SELECT *)
-- =============================================================

-- A1. 查看代理商基础表的全部内容
--     SELECT  -> 我要查数据
--     *       -> 所有列 (All Columns)
--     FROM    -> 从哪张表取
--     ;       -> 语句结束
SELECT * FROM tfn_tiktok_agents;

-- A2. 查看广告消耗流水表的全部内容
SELECT * FROM tfn_ad_spend_daily;


-- =============================================================
--  PART B · 面试加分：用具体字段 + LIMIT 预览
--  真实大数据环境里不建议直接 SELECT *，省算力、提效率
-- =============================================================

-- B1. 只取需要的列，并预览前 10 行
SELECT log_date, ad_spend_aud
FROM tfn_ad_spend_daily
LIMIT 10;

-- B2. 按条件过滤：只看澳大利亚的代理商
SELECT agent_id, agent_name, agent_level
FROM tfn_tiktok_agents
WHERE country = 'Australia';

-- B3. 排序：消耗金额从高到低，看 Top 5 笔投放
SELECT spend_id, log_date, agent_id, ad_spend_aud
FROM tfn_ad_spend_daily
ORDER BY ad_spend_aud DESC
LIMIT 5;


-- =============================================================
--  PART C · 聚合分析 (GROUP BY / 聚合函数)
-- =============================================================

-- C1. 每个行业的总消耗与笔数
SELECT
    industry,
    COUNT(*)            AS spend_count,
    SUM(ad_spend_aud)   AS total_spend_aud,
    ROUND(AVG(ad_spend_aud), 2) AS avg_spend_aud
FROM tfn_ad_spend_daily
GROUP BY industry
ORDER BY total_spend_aud DESC;

-- C2. 每天的总消耗趋势
SELECT
    log_date,
    SUM(ad_spend_aud) AS daily_total_aud
FROM tfn_ad_spend_daily
GROUP BY log_date
ORDER BY log_date;

-- C3. 只看总消耗超过 30000 的行业（HAVING：对聚合结果再过滤）
SELECT
    industry,
    SUM(ad_spend_aud) AS total_spend_aud
FROM tfn_ad_spend_daily
GROUP BY industry
HAVING SUM(ad_spend_aud) > 30000
ORDER BY total_spend_aud DESC;


-- =============================================================
--  PART D · 多表关联 (JOIN)
--  把“消耗流水”和“代理商信息”连起来分析
-- =============================================================

-- D1. 每笔消耗带上代理商名称、国家、级别
SELECT
    s.log_date,
    a.agent_name,
    a.country,
    a.agent_level,
    s.industry,
    s.product_type,
    s.ad_spend_aud
FROM tfn_ad_spend_daily AS s
JOIN tfn_tiktok_agents  AS a
    ON s.agent_id = a.agent_id
ORDER BY s.log_date, s.ad_spend_aud DESC;

-- D2. 按国家汇总总消耗
SELECT
    a.country,
    SUM(s.ad_spend_aud) AS total_spend_aud
FROM tfn_ad_spend_daily AS s
JOIN tfn_tiktok_agents  AS a
    ON s.agent_id = a.agent_id
GROUP BY a.country
ORDER BY total_spend_aud DESC;

-- D3. 按代理级别汇总，看哪个级别贡献最大
SELECT
    a.agent_level,
    COUNT(DISTINCT a.agent_id) AS agent_count,
    SUM(s.ad_spend_aud)        AS total_spend_aud
FROM tfn_ad_spend_daily AS s
JOIN tfn_tiktok_agents  AS a
    ON s.agent_id = a.agent_id
GROUP BY a.agent_level
ORDER BY total_spend_aud DESC;
