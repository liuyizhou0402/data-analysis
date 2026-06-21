# 1B — Mammalian Transport Systems · 动画/短视频创意脚本
# Animation & Short-Video Companion

> 配套 PPT：`ppt-slides/topic-1-molecules-transport-and-health/1B-mammalian-transport-systems.md`
> 规范依据：`00-course-plan/slide-deck-standard.md` §4。
> 每个创意含：🎯 难点概念（为何动画优于静态图）· 🎬 分镜（3–6 镜）· 🎙️ 中英旁白（30–90 s）· 🎨 视觉风格 + 工具。
> 受众：国际学校学生，目标 A*；术语英文、讲解中文。

---

## 动画 1 — The Cardiac Cycle: Pressure, Valves & Flow
## 心动周期：压力—瓣膜—血流的同步舞蹈

🎯 **针对难点 / Why animation beats a static figure**
学生最难的不是记住三期名称，而是把**压力曲线的交叉点 ↔ 瓣膜开闭 ↔ 血流方向**三件事**同时**对应起来。静态压力图是"冻结的一瞬"，学生看不出"谁先谁后"。动画可让**心脏剖面、三条压力曲线、瓣膜、血流箭头四者同步推进**，一眼看懂因果。直接服务于高频 data-response 压力图题。

🎬 **分镜 / Storyboard（5 镜）**
1. **Shot 1（建立镜头）**：左半屏心脏冠状剖面（四腔+四瓣膜），右半屏空白坐标轴（x=time 0–0.8 s，y=pressure）。一个游标从左到右扫过，三条曲线（atrial 蓝、ventricular 红、aortic 金）随扫描**逐渐画出**。
2. **Shot 2（Atrial systole）**：心房收缩变小、AV 瓣开（绿色高亮）、血流箭头入心室；同步在曲线上高亮"房压略高于室压"的小峰。字幕：*AV valves OPEN*。
3. **Shot 3（Ventricular systole）**：室压红线急升，**上穿蓝线**→AV 瓣"啪"地关闭(变红)并弹出音符"lub"；红线继续**上穿金线**→SL 瓣打开、血射入主动脉。交叉点用脉冲光圈强调。
4. **Shot 4（Diastole）**：室压红线下降，**下穿金线**→SL 瓣关("dub")，主动脉曲线出现 **dicrotic notch**（放大镜特写）；红线再**下穿蓝线**→AV 瓣开、血被动充盈。
5. **Shot 5（总结叠化）**：四个交叉点定格，旁注"crossing point = valve event"；心脏循环一次回到起点，loop。

🎙️ **旁白 / Narration（中英，约 75 s）**
- 中文："看好这三条压力曲线。心房收缩，房压略高于室压——房室瓣打开，血流入心室。接着心室收缩，室压飙升，一旦超过房压，房室瓣立刻关闭，这就是第一心音 'lub'。室压继续升高、超过主动脉压，半月瓣打开，血液射入主动脉。心室舒张，室压跌破主动脉压，半月瓣关闭，'dub'，主动脉曲线上留下一个小切迹——dicrotic notch。记住一句话：**曲线的交叉点，就是瓣膜开闭的时刻。**"
- English key terms layered on screen: *atrial systole · ventricular systole · diastole · AV valves · semilunar valves · dicrotic notch · "crossing point = valve event"*.

🎨 **视觉风格 + 工具 / Style & tools**
- 风格：医学插画 + 数据可视化混合；心脏用半写实剖面，曲线用扁平高饱和三色（蓝/红/金），瓣膜事件用脉冲光圈。
- 工具：**Manim**（曲线与交叉点同步动画最佳）/ **After Effects**（心脏剖面 + 音效 lub-dub）/ PPT **Morph** 可做简化版。配 lub-dub 真实心音增强记忆。

---

## 动画 2 — Tissue Fluid Formation: The Pressure Tug-of-War
## 组织液的形成：两种压力的"拔河"

🎯 **针对难点 / Why animation**
学生常把 **hydrostatic（推出）vs oncotic（拉回）** 记反，也想不通"为什么动脉端滤出、静脉端回流"。关键在于**沿毛细血管长度 hydrostatic 在下降、oncotic 基本不变**——这是一个**随空间变化**的过程，静态图很难表达"压力在沿途此消彼长"。动画用**沿管移动的视角 + 两个反向力的长度条**实时变化，把"净滤过压翻转"演活。

🎬 **分镜 / Storyboard（4 镜）**
1. **Shot 1**：一段水平毛细血管，左=arteriole end，右=venule end。管内画红细胞流动、蛋白质（大球，标 "stays in"）。镜头从左缓慢平移到右。
2. **Shot 2（动脉端）**：在管壁画两个反向箭头——向外的红箭头(hydrostatic，长)、向内的蓝箭头(oncotic，短)。净效果：水+小分子（小点）被**挤出**进入组织间隙；字幕 *hydrostatic > oncotic → net out*。
3. **Shot 3（沿途变化）**：随镜头右移，红箭头**逐渐变短**（hydrostatic 下降），蓝箭头长度不变；两箭头长度在中段相等(net≈0)。叠加一条小曲线图同步显示两压力交叉。
4. **Shot 4（静脉端）**：蓝箭头此时更长→水（带 CO₂ 小点）**渗透回流**入血管；多余的 ~10% 液体被旁边盲端 **lymphatic capillary** 吸走。字幕 *oncotic > hydrostatic → net in*；末尾闪现 *excess → lymph*。

🎙️ **旁白 / Narration（中英，约 70 s）**
- 中文："在毛细血管动脉端，血压很高——hydrostatic pressure 把水和小分子**推出**血管，形成 tissue fluid；但血浆蛋白太大，留在管内，产生 oncotic pressure 想把水**拉回**。动脉端，推力大于拉力，液体净流出。随着血液前行，hydrostatic pressure 一路下降，而 oncotic pressure 几乎不变。到了静脉端，拉力反超推力，大部分水又被**渗透回**血液，带走 CO₂ 和废物。剩下的约 10% 由淋巴系统收回——否则就会 oedema 水肿。"
- English on-screen: *hydrostatic pressure (push out) · oncotic/osmotic pressure (pull back) · net outward / inward · tissue fluid · lymph · oedema*.

🎨 **视觉风格 + 工具 / Style & tools**
- 风格：扁平信息图风；用**箭头长度**直接编码压力大小（最直观），暖色=推出、冷色=拉回。
- 工具：**After Effects**（箭头长度补间 + 镜头平移）/ **Manim**（同步小曲线图）/ 剪映可做简版讲解。建议加一个"拔河绳"隐喻图层强化记忆。

---

## 动画 3 — Atherosclerosis: 40 Years in 60 Seconds
## 动脉粥样硬化：把 40 年压缩进 60 秒

🎯 **针对难点 / Why animation**
atherosclerosis 是一个**跨越数十年的渐进、多步骤**过程（damage→inflammation→foam cells→plaque→narrowing→thrombosis），且含**positive feedback 恶性循环**。学生背步骤却没有"动态推进感"，也理解不了"为什么越来越糟"。时间压缩动画 + 血流量实时变化，能把"进行性 + 反馈回路"直观呈现，并自然引出 angina/MI 后果，衔接 1C。

🎬 **分镜 / Storyboard（6 镜）**
1. **Shot 1（健康基线）**：动脉纵剖，内皮光滑、红细胞顺畅高速流过；角落时间轴 "Age 20"。
2. **Shot 2（损伤）**：高血压脉冲/香烟烟雾粒子冲击内皮，出现一道"裂口"；字幕 *endothelial damage*；时间轴跳到 "Age 30"。
3. **Shot 3（炎症）**：macrophages（变形虫样白细胞）迁入裂口、LDL 黄色颗粒渗入内膜，被吞噬成 **foam cells**，聚成黄色 **fatty streak**；字幕 *inflammation → foam cells*。
4. **Shot 4（斑块长大 + 恶性循环）**：脂质+纤维组织堆积成凸起 plaque，管腔变窄、血流变细变慢；旁边弹出循环箭头 "narrow → ↑blood pressure → more damage"；时间轴 "Age 50"。
5. **Shot 5（血栓）**：plaque 表面纤维帽**破裂**，血小板/纤维蛋白迅速聚集成 **thrombus**，**完全堵死**管腔；血流戛然而止。
6. **Shot 6（后果分屏）**：左=冠脉堵塞→一片心肌变灰(MI)；右=栓子飞到脑动脉→stroke。末帧字幕 *→ see Lesson 1C: risk & treatment*。

🎙️ **旁白 / Narration（中英，约 85 s）**
- 中文："二十岁，你的动脉内壁光滑如新。但高血压、吸烟、高血糖会**损伤内皮**。损伤引来巨噬细胞和 LDL 胆固醇——巨噬细胞吞下脂质，变成泡沫细胞，堆成脂纹。几十年里，脂质和纤维组织不断堆积，形成坚硬的斑块，管腔越来越窄、动脉越来越硬，血压随之升高——而更高的血压又造成更多损伤，**恶性循环**。终有一天，斑块破裂，血液在此凝固成血栓，彻底堵死动脉。如果堵在冠状动脉，一片心肌缺氧坏死——这就是 myocardial infarction；如果栓子飞进脑动脉，就是 stroke。"
- English on-screen sequence: *endothelial damage → inflammation → foam cells / fatty streak → plaque → narrowing & hardening → ↑blood pressure (positive feedback) → plaque rupture → thrombosis → ischaemia → infarction*.

🎨 **视觉风格 + 工具 / Style & tools**
- 风格：半写实医学动画 + 时间轴 HUD；血流量用"红细胞密度/速度"直接编码，越堵越稀越慢；恶性循环用闪烁回路箭头。
- 工具：**After Effects + Element 3D**（血管管腔 3D 渐变堆积）/ **Blender**（斑块体积生长）/ Manim 可做循环箭头逻辑图。配低频心跳音渐弱到血栓处"停拍"。

---

## 动画 4 — Why Big Bodies Need a Pump: SA:V & Diffusion Distance
## 为什么大块头需要泵：表面积体积比与扩散距离

🎯 **针对难点 / Why animation**
SA:V 是本课的数学根基，但学生对"体积按立方、表面积按平方增长"只有公式、没有**直觉**，还常把比值方向记反。动画用**正方体逐步放大 + 内部 O₂ 扩散计时**双线呈现：一边数字实时更新 SA:V，一边演示"小体扩散秒到、大体中心缺氧"，让抽象比值变成"看得见的供氧危机"，直接服务 SA:V 计算与"为何需要 mass transport"简答。

🎬 **分镜 / Storyboard（5 镜）**
1. **Shot 1**：一个边长 1 的发光立方体，表面均匀渗入 O₂ 蓝色粒子，**瞬间填满**中心；侧栏显示 *SA=6, V=1, SA:V=6:1*。
2. **Shot 2**：立方体长大到边长 2，表面积、体积数字与 SA:V 实时更新为 *24, 8, 3:1*；O₂ 粒子向中心扩散，**中心稍慢变蓝**。
3. **Shot 3**：长大到边长 4（*96, 64, 1.5:1*）；O₂ 粒子从表面向内推进，**中心区域长时间保持"缺氧灰"**，并出现计时器显示"扩散到中心 = 太久"。
4. **Shot 4（对比定格）**：左 Amoeba（小、全蓝、✅）vs 右大细胞团（中心灰、❌）；旁注 *small = large SA:V + short distance = diffusion enough*。
5. **Shot 5（解决方案）**：在大块头内部"长出"毛细血管网，把 O₂ 直接送到深处，中心由灰转蓝；字幕 *mass transport system to the rescue*，引出心脏+血管。

🎙️ **旁白 / Narration（中英，约 60 s）**
- 中文："边长翻倍，表面积变成 4 倍，体积却变成 8 倍——所以 surface area to volume ratio **越变越小**。看这个小立方体，氧气一瞬间就扩散到中心。但当它长大，表面积相对体积太小、扩散距离又太长，中心细胞迟迟拿不到氧气。这就是为什么 *Amoeba* 靠扩散就够了，而大型活跃动物**必须**有一套 mass transport system——用心脏和血管，把氧气直接送到每一个深处的细胞。"
- English on-screen: *surface area = 6L² · volume = L³ · SA:V = 6/L · diffusion distance · mass transport system*.

🎨 **视觉风格 + 工具 / Style & tools**
- 风格：极简几何 + 数据动画；O₂ 用蓝粒子、缺氧用灰，数字面板实时刷新，强调"立方 vs 平方"的增长落差。
- 工具：**Manim**（数值同步 + 粒子扩散最契合）/ PPT **Morph + 计数动画**做课堂简版 / After Effects 做精修粒子。可加边长滑块让老师课堂上"拖动演示"。

---

## 动画 5 —（可选加餐）Four Vessels, One Journey: A Red Blood Cell's POV
## 四种血管，一段旅程：跟着一个红细胞走完全程

🎯 **针对难点 / Why animation**
学生把 artery/arteriole/capillary/vein 当成**孤立的对比表**死记，缺乏"它们是一条连续回路、结构随压力沿途变化"的整体感，也记不牢压力沿程下降、流速在毛细血管最慢。第一人称(red cell POV)旅程动画，把**结构差异、压力变化、流速变化、交换发生地**串成一条故事线，一镜到底强化系统观，并复习 double circulation。

🎬 **分镜 / Storyboard（6 镜）**
1. **Shot 1（出发·心脏）**：镜头化身一个红细胞，从**左心室**被高压射出，穿过 aortic semilunar valve；HUD 显示 *pressure: HIGH, pulsating*。
2. **Shot 2（动脉）**：在 artery 中疾行，管壁厚、弹性纤维随脉搏一胀一缩(elastic recoil)；HUD 压力条上下波动。
3. **Shot 3（小动脉·分配）**：进入 arteriole，平滑肌收缩/舒张像"阀门"调节去向；HUD 压力**陡降**，字幕 *vasoconstriction / dilation regulates flow*。
4. **Shot 4（毛细血管·交换）**：被迫单列挤过 capillary，管壁仅一层内皮；红细胞**卸下 O₂、带上 CO₂**；HUD 流速降到最慢，字幕 *thin wall + slow flow = exchange*；顺带闪现 tissue fluid 滤出。
5. **Shot 5（静脉·回流）**：进入大管腔的 vein，低压缓行，骨骼肌收缩**挤压血管**、**瓣膜**打开防倒流，把红细胞推回心脏；HUD *low pressure, valves + muscle pump*。
6. **Shot 6（回家·双循环）**：回到右心房→右心室→肺动脉去肺**重新加 O₂**，镜头拉远显示"8 字形" double circulation 全景；字幕 *one cell, two circuits*。

🎙️ **旁白 / Narration（中英，约 80 s）**
- 中文："我是一个红细胞，刚被左心室高压射进主动脉——感受到了吗，压力又高又有脉搏。动脉壁厚、有弹性，每次心跳一胀一缩，把我平稳地送往前方。进入小动脉，平滑肌像阀门决定我去哪个器官，压力在这里骤降。终于到毛细血管，管壁只有一层细胞，我必须单列慢行——正好把氧气卸给组织、带走二氧化碳。然后进入宽阔的静脉，压力很低，全靠骨骼肌挤压和瓣膜防倒流把我送回心脏。回到右心，我又要去肺里重新装满氧气——一个细胞，两段循环。"
- English on-screen waypoints: *aorta (high, pulsating) → arteriole (pressure drops, regulates flow) → capillary (thin wall, slowest flow, exchange) → vein (low pressure, valves + muscle pump) → double circulation*.

🎨 **视觉风格 + 工具 / Style & tools**
- 风格：第一人称"过山车"运镜 + 半写实血管内壁；右上角常驻 HUD（pressure 条 + velocity 表），让抽象量沿途**可视化**。
- 工具：**Blender / Unreal**（一镜到底管腔飞行最震撼）/ After Effects（HUD 数据图层）/ 简版可用 PPT 连续 Morph 串接四段。结尾拉远成 double-circulation 全景，复习 Section 1。

---

> 🎬 制作建议 / Production notes
> - 动画 1（cardiac cycle）与动画 3（atherosclerosis）优先级最高——对应考试最难、最高频的 data-response 与机制题。
> - 课堂可用顺序：动画 4（建立"为何需要循环"）→ 动画 5（系统总览）→ 动画 2（tissue fluid）→ 动画 1（cardiac cycle）→ 动画 3（atherosclerosis，收尾衔接 1C）。
> - 所有英文术语建议在屏上**与旁白同步出现**，做到"听中文懂思路、看英文记术语"。
