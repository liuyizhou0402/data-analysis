-- =============================================================
--  TikTok GBS 商业化数据分析实战项目 · 初始化脚本 (DDL + DML)
--  适用：DB Fiddle 左侧窗口，数据库选 MySQL 8.0 或 PostgreSQL 15
--  用法：整段复制运行，即可建好两张表并灌入模拟数据
-- =============================================================

-- 重复运行时先清表（先子表后父表的顺序无外键约束，可任意）
DROP TABLE IF EXISTS tfn_ad_spend_daily;
DROP TABLE IF EXISTS tfn_tiktok_agents;

-- Create Agent Table (代理商基础表)
CREATE TABLE tfn_tiktok_agents (
    agent_id   INT PRIMARY KEY,      -- 代理商唯一编号
    agent_name VARCHAR(50),          -- 代理商名称
    country    VARCHAR(50),          -- 所属国家/地区
    tier       VARCHAR(10)           -- 代理级别 Tier 1 / Tier 2
);

-- Create Ad Spend Table (广告消耗流水表)
CREATE TABLE tfn_ad_spend_daily (
    log_date     DATE,               -- 投放日期
    agent_id     INT,                -- 代理商编号（关联 tfn_tiktok_agents）
    industry     VARCHAR(50),        -- 行业
    product_type VARCHAR(50),        -- 产品类型
    ad_spend_aud DECIMAL(10, 2)      -- 广告消耗金额（澳元 AUD）
);

-- Insert Mock Data for Agents
INSERT INTO tfn_tiktok_agents VALUES
(101, 'Blue Sky Media', 'Australia',   'Tier 1'),
(102, 'Ocean Digital',  'Australia',   'Tier 2'),
(103, 'Global Reach',   'New Zealand', 'Tier 1'),
(104, 'Apex Marketing', 'Australia',   'Tier 2');

-- Insert Mock Data for Ad Spend (模拟 2026 年 5 月和 6 月数据)
INSERT INTO tfn_ad_spend_daily VALUES
('2026-05-01', 101, 'E-commerce', 'In-Feed Ads',    5000.00),
('2026-05-15', 101, 'E-commerce', 'Spark Ads',      7000.00),
('2026-06-01', 101, 'E-commerce', 'In-Feed Ads',    8500.00),
('2026-06-15', 101, 'Gaming',     'Spark Ads',      3000.00),  -- 101 拓宽了行业

('2026-05-10', 102, 'Gaming',     'In-Feed Ads',    4000.00),
('2026-06-10', 102, 'Gaming',     'In-Feed Ads',    3500.00),  -- 102 消耗下滑了

('2026-05-20', 103, 'E-commerce', 'Branded Effect', 12000.00),
('2026-06-20', 103, 'E-commerce', 'Branded Effect', 15000.00),

('2026-05-05', 104, 'Education',  'In-Feed Ads',    2000.00),
('2026-06-05', 104, 'Education',  'In-Feed Ads',    6000.00);  -- 104 爆发增长
