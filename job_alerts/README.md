# 每日健康数据岗位雷达 · 综合投递平台

一个自动化求职助手：每天定时**抓取多个招聘平台**的悉尼健康数据岗位 →
按你的个人画像**打分** → **从高到低排序** → **去重** → **发到你的邮箱**。

> 画像基于：USYD Master of Digital Health & Data Science · 健康数据方向 ·
> 2027 年 7 月毕业 · PR（无需 sponsor）· 悉尼。

## 覆盖的招聘平台

| 平台 | 方式 | 稳定性 | 对应清单里的入口 |
|---|---|---|---|
| **Adzuna**（聚合 Seek/Indeed 等）| 官方 API | ⭐⭐⭐ 最稳 | 需免费 key，见下 |
| **LinkedIn** | 免登录 guest 接口 | ⭐⭐ | LinkedIn Jobs |
| **Seek** | Playwright + 内部 JSON 接口 | ⭐ best-effort | Seek |
| **GradConnection** | Playwright | ⭐ best-effort | 毕业生/实习总站 |
| **Prosple** | Playwright | ⭐ best-effort | 毕业生项目 |
| **Indeed** | Playwright | ⚠ 反爬最凶 | Indeed |

> Seek / Indeed / LinkedIn 对数据中心 IP 有强反爬，单个源被拦不影响其它源——
> pipeline 对每个源都做了容错。**强烈建议配置 Adzuna**（它已聚合 Seek/Indeed），
> 这是让每天邮件"有货"的关键。USYD CareerHub 需要学校 SSO 登录，无法无人值守抓取，
> 已留作手动入口。

## 一次性配置（让它每天自动发信）

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 添加：

| Secret | 必填 | 说明 |
|---|---|---|
| `XHS_EMAIL_USER` | ✅ | 发件 Gmail 地址（你仓库里其它爬虫已在用，复用即可）|
| `XHS_EMAIL_PASSWORD` | ✅ | Gmail **应用专用密码**（App Password，不是登录密码）|
| `JOB_ALERT_TO` | 可选 | 收件邮箱，默认 `yizhouliu612@gmail.com` |
| `ADZUNA_APP_ID` | 建议 | 免费注册 https://developer.adzuna.com/ 获取 |
| `ADZUNA_APP_KEY` | 建议 | 同上 |

定时任务在 `.github/workflows/job_alerts.yml`：每天悉尼早上 8 点左右发一封。
也可在 **Actions** 页面点 **Run workflow** 手动触发测试。

> ⚠ GitHub 的 schedule 只在**默认分支**上才会自动触发。要让它每天自动跑，
> 需把本分支合并到 `main`（或把该 workflow 放到默认分支）。`workflow_dispatch`
> 手动触发不受此限制，可随时测试。

## 本地测试 / 调参

```bash
pip install -r job_alerts/requirements.txt
python -m job_alerts.main --sample    # 用样例数据预览邮件排版（不联网、不发信）
python -m job_alerts.main --preview    # 尝试真实抓取，抓不到则回退样例，写 HTML 不发信
python -m job_alerts.main --now        # 正式：抓取 + 发邮件（需配好邮箱密钥）
```

## 怎么改匹配逻辑

全部集中在 [`config.py`](config.py)：
- `SEARCH_KEYWORDS` —— 搜什么岗位
- `SKILLS` / `TARGET_EMPLOYERS` —— 你的技能 & 目标雇主（命中加分）
- `WEIGHTS` —— 各打分维度权重
- `MIN_SCORE` —— 低于多少分不进邮件
- `SOURCES_ENABLED` —— 关掉某个长期被封的源

## 打分维度

标题相关 (30) · 健康行业 (22) · 技能重合 R/Python/ML/BI (18) · 目标雇主 (14) ·
资历适配 (8) · 悉尼地点 (6) · PR 友好 (6) · 新鲜度 (4)。每条岗位邮件里都会显示
**命中了哪些维度**，方便你判断要不要投。
