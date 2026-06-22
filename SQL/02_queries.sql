-- =============================================================
--  TikTok GBS 实战项目 · 三大核心面试必考 SQL 题
--  适用：DB Fiddle 右侧窗口（运行前先在左侧跑 01_setup.sql）
--  对应岗位职责：多维度归因分析 / 寻找高潜力代理商 / 政策监控
-- =============================================================


-- =============================================================
--  第一题：多维度消耗总览  [JOIN + GROUP BY]
--  业务痛点：销售总监想知道 2026 年 6 月，澳大利亚市场
--           各个行业的总广告消耗是多少？
-- =============================================================
SELECT
    a.country,
    s.industry,
    SUM(s.ad_spend_aud) AS total_spend_june
FROM tfn_ad_spend_daily s
JOIN tfn_tiktok_agents  a ON s.agent_id = a.agent_id
WHERE a.country = 'Australia'
  AND s.log_date BETWEEN '2026-06-01' AND '2026-06-30'
GROUP BY a.country, s.industry
ORDER BY total_spend_june DESC;


-- =============================================================
--  第二题：环比增长归因分析  [窗口函数 LAG()]
--  业务痛点：找出“高潜力代理商”。计算每个代理商 6 月相比
--           5 月的消耗增长率，帮销售锁定黑马。
--  ⚠️ 月份格式化是唯一的方言差异，下面给出两种写法二选一。
-- =============================================================
WITH monthly_spend AS (
    SELECT
        agent_id,
        -- MySQL 8.0 写法：
        DATE_FORMAT(log_date, '%Y-%m')  AS months,
        -- PostgreSQL 15 写法（用上面这行则注释掉本行，反之亦然）：
        -- TO_CHAR(log_date, 'YYYY-MM') AS months,
        SUM(ad_spend_aud) AS total_spend
    FROM tfn_ad_spend_daily
    GROUP BY agent_id, months
),
growth_calc AS (
    SELECT
        agent_id,
        months,
        total_spend,
        LAG(total_spend, 1) OVER (PARTITION BY agent_id ORDER BY months) AS prev_month_spend
    FROM monthly_spend
)
SELECT
    g.agent_id,
    a.agent_name,
    g.months          AS current_month,
    g.total_spend     AS june_spend,
    g.prev_month_spend AS may_spend,
    (g.total_spend - g.prev_month_spend) AS absolute_growth,
    ROUND(((g.total_spend - g.prev_month_spend) / g.prev_month_spend) * 100, 2) AS growth_rate_percent
FROM growth_calc g
JOIN tfn_tiktok_agents a ON g.agent_id = a.agent_id
WHERE g.prev_month_spend IS NOT NULL;
-- 💡 运行后可见：Agent 104 (Apex Marketing) 增长率高达 200%，即业务上的高潜力黑马。


-- =============================================================
--  第三题：大促政策达标监控  [条件聚合 CASE WHEN]
--  业务痛点：跟踪佣金激励政策执行进度。6 月总消耗 >= $10,000 AUD
--           的代理商可拿“返点金”，否则“不达标”。
-- =============================================================
SELECT
    s.agent_id,
    a.agent_name,
    SUM(s.ad_spend_aud) AS total_june_spend,
    CASE
        WHEN SUM(s.ad_spend_aud) >= 10000 THEN 'Rebate Eligible (10% Commission)'
        ELSE 'Below Target (0% Rebate)'
    END AS policy_status
FROM tfn_ad_spend_daily s
JOIN tfn_tiktok_agents  a ON s.agent_id = a.agent_id
WHERE s.log_date BETWEEN '2026-06-01' AND '2026-06-30'
GROUP BY s.agent_id, a.agent_name;
