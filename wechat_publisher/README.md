# 每日留学资讯公众号自动发布

每天自动：抓取澳洲/新西兰/英国留学最新资讯 → 按热度排序 → 用 Claude 生成 **3 篇内容不同的图文公众号文章**（澳新热点 / 英国申请 / 专业申请条件，专业按星期轮换）→ 自动生成封面图 → 推送到你的公众号草稿箱并（可选）自动发布。

## 流程

```
RSS 资讯源 ──→ fetch_news.py 热度打分排序 ──→ generate.py (Claude 写 3 篇 HTML)
                                              │
                covers.py 生成 3 张封面图 ←────┘
                                              │
                wechat.py 上传封面 → 存草稿 → freepublish 自动发布
```

热度排序说明：RSS 不提供点赞/评论数，热度分 = **关键词相关性（签证/政策/学费/排名等加权）+ 时效性（48 小时内加分）+ 多源同报加分**。文章内资讯按该热度从高到低组织。

## 需要配置的 GitHub Secrets

| Secret | 必需 | 说明 |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | 生成文章用 |
| `WECHAT_APPID` | 推送公众号时必需 | 公众号后台 → 设置与开发 → 基本配置 |
| `WECHAT_APPSECRET` | 推送公众号时必需 | 同上 |

Repository Variable：`WECHAT_AUTO_PUBLISH` 设为 `true` 时存草稿后直接提交发布；默认 `false`（只存草稿，你在后台手动点发布）。建议先跑几天草稿模式，确认内容质量后再开自动发布。

## ⚠️ 微信侧的两个硬性前提

1. **公众号必须是已认证的服务号或订阅号**。草稿箱（`/draft/add`）和发布（`/freepublish/submit`）接口对个人未认证订阅号不开放——这种情况下程序仍会每天生成 3 篇文章和封面（在 Actions 的 artifact 里下载），但需要手动粘贴到公众号编辑器发布。
2. **IP 白名单**：微信要求调用 API 的服务器 IP 在公众号后台白名单内，而 GitHub Actions 的出口 IP 是动态的。解决方案任选其一：
   - 把这套代码放到你自己的固定 IP 服务器/云函数上用 cron 跑（推荐）；
   - 用固定出口 IP 的代理转发微信 API 请求；
   - 临时方案：每次失败后把日志里的 IP 加进白名单（不现实，不推荐长期用）。

## 本地试跑

```bash
pip install -r wechat_publisher/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
cd wechat_publisher && python main.py
# 不配置 WECHAT_* 时只生成文章到 data/output/<日期>/，不推送
```

## 自定义

- 资讯源 / 热度关键词 / 三篇文章主题：改 `config.py`
- 专业轮换表：`config.py` 里的 `MAJORS_BY_WEEKDAY`
- 发文时间：改 `.github/workflows/wechat_daily.yml` 的 cron（当前北京时间每天 07:00）
- 文风和排版：改 `generate.py` 里的 `SYSTEM_PROMPT`
