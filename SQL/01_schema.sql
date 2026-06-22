-- =============================================================
--  SQL 项目 · 建表脚本 (Schema / DDL)
--  TikTok 代理商广告消耗分析
-- -------------------------------------------------------------
--  设计两张表：
--    1. tfn_tiktok_agents  代理商基础表（维度表 Dimension）
--    2. tfn_ad_spend_daily 广告消耗流水表（事实表 Fact）
--  运行顺序：先建表（本文件）→ 再灌数据（02_seed_data.sql）
--  方言：标准 SQL，兼容 MySQL 8 / PostgreSQL / DB Fiddle
-- =============================================================

-- 若已存在则先删除，方便重复运行（先删子表，再删父表）
DROP TABLE IF EXISTS tfn_ad_spend_daily;
DROP TABLE IF EXISTS tfn_tiktok_agents;

-- -------------------------------------------------------------
-- 1) 代理商基础表 tfn_tiktok_agents
--    记录有哪些代理商、所属国家、代理级别
-- -------------------------------------------------------------
CREATE TABLE tfn_tiktok_agents (
    agent_id     INT          PRIMARY KEY,                 -- 代理商唯一编号
    agent_name   VARCHAR(100) NOT NULL,                    -- 代理商名称
    country      VARCHAR(50)  NOT NULL,                    -- 所属国家/地区
    agent_level  VARCHAR(20)  NOT NULL,                    -- 代理级别：Diamond/Gold/Silver/Bronze
    created_at   DATE         NOT NULL                     -- 入驻日期
);

-- -------------------------------------------------------------
-- 2) 广告消耗流水表 tfn_ad_spend_daily
--    记录每天、每个代理商、每个行业/产品的广告消耗金额（澳元 AUD）
-- -------------------------------------------------------------
CREATE TABLE tfn_ad_spend_daily (
    spend_id      INT           PRIMARY KEY,               -- 流水唯一编号
    log_date      DATE          NOT NULL,                  -- 投放日期
    agent_id      INT           NOT NULL,                  -- 代理商编号（关联 tfn_tiktok_agents）
    industry      VARCHAR(50)   NOT NULL,                  -- 行业，如 E-commerce / Gaming
    product_type  VARCHAR(50)   NOT NULL,                  -- 产品类型，如 In-Feed Ads / TopView
    ad_spend_aud  DECIMAL(12,2) NOT NULL,                  -- 广告消耗金额（澳元）
    CONSTRAINT fk_spend_agent
        FOREIGN KEY (agent_id) REFERENCES tfn_tiktok_agents (agent_id)
);

-- 常用查询索引：按日期、按代理商聚合时加速
CREATE INDEX idx_spend_log_date ON tfn_ad_spend_daily (log_date);
CREATE INDEX idx_spend_agent_id ON tfn_ad_spend_daily (agent_id);
