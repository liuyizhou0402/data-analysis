-- =============================================================
--  SQL 项目 · 模拟数据 (Seed / Mock Data)
--  运行前请先执行 01_schema.sql 建好两张表
-- =============================================================

-- -------------------------------------------------------------
-- 1) 代理商基础表数据：8 个代理商，覆盖 4 个国家、4 个级别
-- -------------------------------------------------------------
INSERT INTO tfn_tiktok_agents (agent_id, agent_name, country, agent_level, created_at) VALUES
    (1, 'Sydney Spark Media',     'Australia',   'Diamond', '2023-01-15'),
    (2, 'Melbourne Reach Co.',    'Australia',   'Gold',    '2023-03-02'),
    (3, 'Auckland Pulse Ads',     'New Zealand', 'Silver',  '2023-05-20'),
    (4, 'Singapore Wave Digital', 'Singapore',   'Diamond', '2022-11-08'),
    (5, 'Lion City Growth',       'Singapore',   'Gold',    '2023-07-11'),
    (6, 'Tokyo Bright Agency',    'Japan',       'Gold',    '2023-02-27'),
    (7, 'Osaka Click Lab',        'Japan',       'Bronze',  '2023-09-01'),
    (8, 'Wellington Trend Hub',   'New Zealand', 'Bronze',  '2023-10-19');

-- -------------------------------------------------------------
-- 2) 广告消耗流水表数据：覆盖多天 / 多行业 / 多产品类型
-- -------------------------------------------------------------
INSERT INTO tfn_ad_spend_daily (spend_id, log_date, agent_id, industry, product_type, ad_spend_aud) VALUES
    (1001, '2024-05-01', 1, 'E-commerce',    'In-Feed Ads',  12500.50),
    (1002, '2024-05-01', 1, 'E-commerce',    'TopView',      30200.00),
    (1003, '2024-05-01', 2, 'Gaming',        'In-Feed Ads',   8400.75),
    (1004, '2024-05-01', 4, 'Beauty',        'Spark Ads',    21000.00),
    (1005, '2024-05-02', 1, 'E-commerce',    'In-Feed Ads',  13750.25),
    (1006, '2024-05-02', 3, 'Education',     'In-Feed Ads',   5600.00),
    (1007, '2024-05-02', 5, 'Finance',       'TopView',      18900.40),
    (1008, '2024-05-02', 6, 'Gaming',        'Spark Ads',    14250.00),
    (1009, '2024-05-03', 2, 'Gaming',        'TopView',      26700.00),
    (1010, '2024-05-03', 4, 'Beauty',        'In-Feed Ads',  16800.30),
    (1011, '2024-05-03', 7, 'E-commerce',    'In-Feed Ads',   3200.00),
    (1012, '2024-05-03', 8, 'Education',     'Spark Ads',     2750.90),
    (1013, '2024-05-04', 1, 'E-commerce',    'Spark Ads',    19500.00),
    (1014, '2024-05-04', 5, 'Finance',       'In-Feed Ads',  11200.60),
    (1015, '2024-05-04', 6, 'Gaming',        'TopView',      22300.00),
    (1016, '2024-05-05', 3, 'Education',     'TopView',       9800.00),
    (1017, '2024-05-05', 4, 'Beauty',        'TopView',      28500.75),
    (1018, '2024-05-05', 2, 'Gaming',        'In-Feed Ads',   7650.00),
    (1019, '2024-05-05', 7, 'E-commerce',    'Spark Ads',     4100.25),
    (1020, '2024-05-05', 8, 'Education',     'In-Feed Ads',   3950.00);
