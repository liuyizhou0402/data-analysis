# SQL 项目 · TikTok 代理商广告消耗分析

一个从零开始、可直接运行的 SQL 练习项目。围绕「TikTok 代理商」和「每日广告消耗流水」
两张表，覆盖**建表 → 灌数据 → 查询分析**的完整链路，适合 SQL 入门与面试速记。

## 📂 项目结构

| 文件 | 作用 | 运行顺序 |
|------|------|----------|
| `01_schema.sql`    | 建表脚本（DDL）：创建两张表、外键、索引 | 1️⃣ |
| `02_seed_data.sql` | 模拟数据：8 个代理商 + 20 条消耗流水    | 2️⃣ |
| `03_queries.sql`   | 查询示例：从看全表到 JOIN 聚合分析      | 3️⃣ |

## 🗃️ 数据模型

**`tfn_tiktok_agents`（代理商基础表 / 维度表）**

| 字段 | 类型 | 说明 |
|------|------|------|
| agent_id    | INT          | 代理商编号（主键） |
| agent_name  | VARCHAR(100) | 代理商名称 |
| country     | VARCHAR(50)  | 所属国家/地区 |
| agent_level | VARCHAR(20)  | 代理级别 Diamond/Gold/Silver/Bronze |
| created_at  | DATE         | 入驻日期 |

**`tfn_ad_spend_daily`（广告消耗流水表 / 事实表）**

| 字段 | 类型 | 说明 |
|------|------|------|
| spend_id     | INT           | 流水编号（主键） |
| log_date     | DATE          | 投放日期 |
| agent_id     | INT           | 代理商编号（外键 → tfn_tiktok_agents） |
| industry     | VARCHAR(50)   | 行业 |
| product_type | VARCHAR(50)   | 产品类型 |
| ad_spend_aud | DECIMAL(12,2) | 广告消耗金额（澳元 AUD） |

两表通过 `agent_id` 关联，是经典的「事实表 + 维度表」星型结构。

## 🚀 如何运行

### 方式一：DB Fiddle（网页端，最省事）
1. 打开 https://www.db-fiddle.com/ ，左上角数据库选 **MySQL 8** 或 **PostgreSQL**。
2. 把 `01_schema.sql` + `02_seed_data.sql` 内容贴到左边 **Schema** 框。
3. 把 `03_queries.sql` 里想跑的查询贴到右边 **Query** 框，点 **Run**。

### 方式二：本地 SQLite（一行命令）
```bash
sqlite3 demo.db < SQL/01_schema.sql
sqlite3 demo.db < SQL/02_seed_data.sql
sqlite3 demo.db < SQL/03_queries.sql
```

### 方式三：MySQL / PostgreSQL
```bash
mysql -u root -p < SQL/01_schema.sql && mysql -u root -p < SQL/02_seed_data.sql
```

## 💡 核心语法速记（面试秒懂）

- `SELECT`：告诉数据库「我要查数据」。
- `*`：所有列（All Columns），无需逐个写字段名。
- `FROM`：后面接表名，告诉数据库去哪取数据。
- `;`：一条语句的结束，多条语句用它隔开。

## 🚀 面试加分点

在字节这种动辄几十亿行的流水表里，**不建议直接 `SELECT *`**，因为非常消耗算力。
更专业的写法：

```sql
-- 只取需要的列，并先预览前 10 行
SELECT log_date, ad_spend_aud
FROM tfn_ad_spend_daily
LIMIT 10;
```

`03_queries.sql` 里还演示了 `WHERE` 过滤、`ORDER BY` 排序、`GROUP BY` 聚合、
`HAVING` 二次过滤、以及多表 `JOIN`——按国家 / 行业 / 代理级别做消耗分析。

祝面试顺利，大杀四方！🎯
