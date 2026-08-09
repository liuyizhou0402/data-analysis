# AI 炒股 Skill 清单（下载存档）

对应小红书清单「AI 炒股 Skill 清单 / 6 个工具」。清单里 6 项中 **5 项是可安装的 Agent Skill**，已下载到本目录；第 2 项 **ARTi 是网页产品，不是 Skill，无法下载**。

下载日期：2026-08-09。

## 目录内容

| 清单编号 | Skill | 目录 | 来源仓库 | 许可 |
|---|---|---|---|---|
| 01 | Stock Market Pro（行情 · K线 · 基本面） | `stock-market-pro/` | [sundial-org/awesome-openclaw-skills](https://github.com/sundial-org/awesome-openclaw-skills) @ `b80cde2` | 仓库未声明 |
| 02 | ARTi（公司研究 · 证据 · 未知项） | — | 网页产品，非 Skill | — |
| 03 | Longbridge Fundamentals（三表 · 业务构成 · 同行估值） | `longbridge-fundamentals/` + `longbridge/` | [longbridge/skills](https://github.com/longbridge/skills) @ `84bff7b` | MIT |
| 04 | Earnings Analysis（财报季 · 超预期/不及预期） | `earnings-analysis/` | [anthropics/financial-services](https://github.com/anthropics/financial-services) @ `3865222` | Apache-2.0 |
| 05 | DCF Valuation（现金流 · WACC · 敏感性） | `dcf-valuation/` | [claude-office-skills/skills](https://github.com/claude-office-skills/skills) @ `9c4c7d5` | MIT |
| 06 | Diversification（相关性 · 风险贡献 · 压力测试） | `diversification/` | [JoelLewis/finance_skills](https://github.com/JoelLewis/finance_skills) @ `5c498ea` | MIT |

各上游仓库的许可证原文见 `LICENSES/`。

## 安装

这些是标准的 Agent Skill（每个目录一个 `SKILL.md`）。安装 = 把目录放到 agent 会读取的 skills 路径下：

```bash
# 当前项目可用
mkdir -p .claude/skills && cp -r skills/*/ .claude/skills/

# 或全局可用（对所有项目生效）
mkdir -p ~/.claude/skills && cp -r skills/*/ ~/.claude/skills/
```

Codex / Cursor 等其他 agent 同理，换成各自的 skills 目录即可。

也可以直接从上游安装最新版（会跳过本目录）：

```bash
npx -y skills add longbridge/skills -g
npx -y skills add anthropics/financial-services-plugins --skill earnings-analysis --agent claude-code
npx -y skills add claude-office-skills/skills --skill dcf-valuation
```

## 已知问题与依赖

- **stock-market-pro 不完整。** 它的 `SKILL.md` 调用 `uv run --script scripts/yf ...`，但上游仓库里这个目录**只有 `SKILL.md`，没有 `scripts/` 脚本**。照原样安装，取行情/画 K 线的命令会失败。要么让 agent 按 SKILL.md 的描述用 yfinance 自己实现脚本，要么换用 longbridge 系列的行情 skill。
- **longbridge-fundamentals 依赖基础 skill。** 它需要同仓库的 `longbridge` 基础 skill（提供 CLI/MCP 接入），所以两个目录都下载了，安装时请一起装。部分接口需要登录 Longbridge 账号。
- **earnings-analysis 面向机构研报格式**（8–12 页、含图表），产出依赖 xlsx/pptx 生成能力，是 Anthropic 金融服务插件里 `earnings-reviewer` 的一个组件。
- **第三方代码未经审查。** 除 Anthropic 官方仓库外，其余均为社区仓库，`SKILL.md` 里的指令和脚本会被 agent 执行，安装前建议自己看一遍内容。
- 这些工具只做数据与分析，不构成投资建议。
