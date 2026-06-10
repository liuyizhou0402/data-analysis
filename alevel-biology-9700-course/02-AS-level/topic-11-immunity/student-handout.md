# Topic 11 — 免疫 / Immunity｜学生讲义

## 本主题你要拿下 / What you'll master
- ✅ 描述吞噬作用（phagocytosis）的完整过程
- ✅ 区分**体液免疫**与**细胞免疫**，并描述各自的 B/T 细胞激活机制
- ✅ 解释**克隆选择与克隆扩增**，以及记忆细胞的作用
- ✅ 对比**主动免疫与被动免疫**（来源、持续时间、保护时机）
- ✅ 描述**单克隆抗体**的制备步骤及主要应用

> 🎯 **A\* 提示**：高频丢分 ①浆细胞 vs 记忆细胞的区别；②主动与被动免疫的持续时间原因；③单克隆抗体制备步骤顺序混乱。

---

## 1. 非特异性免疫 / Non-specific Immunity

### 1.1 第一道防线（物理/化学屏障）
- **皮肤**：死角质细胞层，病原体无法穿透
- **黏液 + 纤毛**：黏液截留病原体，纤毛扫向咽喉
- **胃酸（HCl）**：低 pH 杀死随食物进入的病原体

### 1.2 吞噬作用（Phagocytosis）

当病原体突破第一道防线后，**吞噬细胞（phagocytes）**启动：

```
步骤 1：吞噬细胞被化学物质（趋化因子 chemokines）吸引到感染部位
步骤 2：识别病原体表面抗原（模式识别，非特异）
步骤 3：伸出伪足（pseudopodia）包围病原体 → 形成吞噬体（phagosome）
步骤 4：溶酶体（lysosome）与吞噬体融合 → 溶酶体酶水解病原体
步骤 5：消化产生的抗原片段呈递到细胞表面（与 MHC II 结合）
        → 该细胞成为抗原呈递细胞（APC，antigen presenting cell）
```

主要吞噬细胞类型：
- **中性粒细胞（neutrophils）**：血液中，快速应答，寿命短
- **巨噬细胞（macrophages）**：组织中，寿命长，也是 APC

---

## 2. 特异性免疫：体液免疫 / Humoral Immunity

**针对**：胞外病原体（细菌、毒素、病毒颗粒）

**关键细胞**：B 淋巴细胞（B lymphocytes，成熟于骨髓 bone marrow）

### 2.1 B 细胞激活流程

```
抗原进入体内
    ↓
APC 呈递抗原片段给 T helper 细胞
    ↓
T helper 细胞释放细胞因子（cytokines / lymphokines）
    ↓
特异性 B 细胞被抗原选中（克隆选择 clonal selection）
    ↓
B 细胞快速有丝分裂（克隆扩增 clonal expansion）
    ↓
    ├→ 浆细胞（plasma cells）：分泌大量抗体（~5000 个/s/cell）
    └→ 记忆 B 细胞（memory B cells）：长期存活，再次感染时快速应答
```

### 2.2 抗体结构

```
     抗原结合位点（可变区 variable region）
          ↑    ↑
         |      |
         |      |        ← 两条轻链（light chains）
         |      |
          ------
          |    |
          |    |          ← 两条重链（heavy chains）
          ------
           恒定区（constant region）
        （激活补体/促进吞噬）
```

**关键特征**：
- Y 形**糖蛋白**，两条重链 + 两条轻链
- **两个**抗原结合位点，均与同一抗原互补
- 可变区的氨基酸序列决定特异性

### 2.3 抗体的功能
| 功能 | 机制 |
|---|---|
| **中和（Neutralisation）** | 封闭病毒/毒素的结合位点 |
| **凝集（Agglutination）** | 同时结合多个病原体，使其团聚 |
| **调理（Opsonisation）** | 包被病原体，促进吞噬细胞识别与吞噬 |
| **补体激活** | 恒定区激活补体系统，裂解细菌 |

---

## 3. 特异性免疫：细胞免疫 / Cell-mediated Immunity

**针对**：胞内病原体（病毒感染的细胞）、肿瘤细胞、移植器官

**关键细胞**：T 淋巴细胞（T lymphocytes，成熟于胸腺 thymus）

### 3.1 T 细胞激活流程

```
APC（巨噬细胞）呈递抗原片段（MHC II）
    ↓
特异性 T helper 细胞（CD4⁺）被激活 → 释放细胞因子
    ↓（激活其他免疫细胞）
特异性细胞毒性 T 细胞（Tc, cytotoxic T cells, CD8⁺）被激活
    ↓
Tc 识别靶细胞（MHC I + 病毒抗原）
    ↓
释放穿孔素（perforin）→ 打穿靶细胞膜 → 靶细胞凋亡（apoptosis）
```

### 3.2 T 细胞类型
| 细胞类型 | 功能 |
|---|---|
| **T helper (Th, CD4⁺)** | 激活 B 细胞和 Tc 细胞（免疫"司令"）|
| **Cytotoxic T (Tc, CD8⁺)** | 直接杀伤靶细胞（穿孔素机制）|
| **Memory T cells** | 长期存活，再次感染时快速应答 |

> ⚠️ HIV 摧毁 **T helper 细胞** → 体液免疫（B 细胞无法被充分激活）和细胞免疫均受损。

---

## 4. 免疫记忆与疫苗 / Immune Memory & Vaccines

### 4.1 初次 vs 二次免疫应答

| | 初次应答（Primary） | 二次应答（Secondary） |
|---|---|---|
| 潜伏期 | 长（7–14 天）| 短（1–3 天）|
| 抗体峰值 | 低 | **高**（数倍）|
| 抗体持续时间 | 短 | 长 |
| 原因 | 克隆扩增需时间 | **记忆细胞**迅速应答 |

### 4.2 主动免疫 vs 被动免疫

| | 主动免疫（Active）| 被动免疫（Passive）|
|---|---|---|
| 抗体来源 | **自身** B 细胞产生 | **外部**提供（注射抗体/母乳）|
| 记忆细胞 | **有** | **无** |
| 保护持续时间 | **长期**（可终身）| **短期**（周/月，抗体降解）|
| 保护建立速度 | 慢（需数天~周）| **立即** |
| 举例 | 疫苗接种、感染后恢复 | 抗毒素注射、母乳（IgA）、胎盘 IgG |

> 🎯 口诀：被动免疫 = 借来的枪（快但不长久）；主动免疫 = 自己的武器（慢但终身持有）。

---

## 5. 单克隆抗体 / Monoclonal Antibodies (mAbs)

**原理**：单一 B 细胞克隆产生的**一种特异性抗体**，批量生产。

### 5.1 制备步骤

```
① 向小鼠注射目标抗原 → 小鼠免疫，脾脏中 B 细胞产生特异性抗体

② 取出小鼠**脾细胞（B 淋巴细胞）**

③ 与**骨髓瘤细胞（myeloma cell）**融合（细胞融合 / 聚乙二醇处理）

④ 形成**杂交瘤细胞（hybridoma cell）**：
   = B 细胞（特异性抗体）× 骨髓瘤（无限增殖能力）

⑤ 在 HAT 选择培养基中培养：未融合的骨髓瘤细胞死亡，未融合 B 细胞死亡，只有杂交瘤存活

⑥ **克隆化**：分离单个杂交瘤 → 检测所产抗体的特异性

⑦ 扩大培养目标克隆 → 大量收获单克隆抗体
```

### 5.2 主要应用

| 应用 | 原理 |
|---|---|
| **妊娠检测（pregnancy test）** | 检测尿液中 hCG（人绒毛膜促性腺激素）|
| **癌症靶向治疗** | 如曲妥珠单抗（Herceptin）靶向 HER2+ 乳腺癌细胞 |
| **侧流检测（COVID-19 rapid test）** | 两条 mAb 检测线，阳性/阴性判读 |
| **科研（免疫荧光）** | 标记特定蛋白，用于定位与检测 |

---

## 必背定义 / Must-know Definitions

| 概念 | 英文定义 | 中文 |
|---|---|---|
| Antigen | *A molecule (usually a protein/glycoprotein) on the surface of a cell or pathogen that stimulates an immune response.* | 抗原 |
| Antibody | *A specific glycoprotein (immunoglobulin) produced by plasma cells that binds to a specific antigen.* | 抗体 |
| Clonal selection | *The process by which a lymphocyte with a complementary antigen receptor to a specific antigen is selected and activated.* | 克隆选择 |
| Active immunity | *Immunity resulting from the production of antibodies by the individual's own immune system, following exposure to an antigen.* | 主动免疫 |
| Passive immunity | *Immunity resulting from the transfer of antibodies produced by another organism.* | 被动免疫 |

---

## A* 拓展 / Stretch to A*
- **Topic 6 连接**：抗体是**蛋白质**，由浆细胞核糖体合成，经 RER → 高尔基 → 分泌（Topic 1 分泌途径）。
- **Topic 10 连接**：HIV 破坏 T helper 细胞 → 理解为什么 AIDS 患者对多种感染都无抵抗力。
- **Topic 16 连接**：不同个体对疫苗应答强度不同，部分是遗传决定（MHC 分子多态性）。
- **Tolerance（免疫耐受）**：正常情况下，T 细胞在胸腺中被筛选，识别自身抗原的 T 细胞被删除（阴性选择）——自身免疫病（如 MS、RA）是耐受失败的结果。

---

## 自测清单 / Self-check
- [ ] 我能画出吞噬过程的 5 步流程图
- [ ] 我能区分浆细胞（分泌抗体）和记忆 B 细胞（长期存活）
- [ ] 我能对比体液免疫与细胞免疫的靶标和机制
- [ ] 我能用主动/被动、来源/时长/速度三个维度对比免疫类型
- [ ] 我能按正确顺序描述单克隆抗体制备的 7 步
