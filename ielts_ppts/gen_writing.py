# -*- coding: utf-8 -*-
"""
雅思写作 10 节课课件生成器
import ppt_utils（v2 API），每节课生成一个独立 .pptx 到 writing/，每个 >= 60 页。
深圳提分专属版 · 9分名师授课用。
"""
import os
import ppt_utils as U

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "writing")
os.makedirs(OUT, exist_ok=True)

# ── 写作主题配色（紫金）──────────────────────────────────────────
U.set_theme(
    U.RGBColor(0x47, 0x24, 0x73),  # primary 深紫
    U.RGBColor(0xF2, 0xA0, 0x1D),  # accent 金
    U.RGBColor(0xF1, 0xEC, 0xF7),  # light 浅紫
    U.RGBColor(0x2C, 0x11, 0x4B),  # softdark 更深紫
    "写作", "IELTS Writing",
)


# ════════════════════════════════════════════════════════════════
#  L01 评分标准与写作诊断
# ════════════════════════════════════════════════════════════════
def build_l01(p):
    U.cover(p, "写作", 1, "评分标准与写作诊断",
            "Assessment Criteria & Writing Diagnosis", total=10)

    U.agenda(p, [
        "雅思写作考试全貌与两大任务",
        "Task 1 vs Task 2 核心规则",
        "四维评分标准深度拆解",
        "考官评分逻辑与分数下限/提分区",
        "中式英语诊断与五大痛点",
        "6/7/8 分对照与提分路线",
        "课堂练习：自我写作诊断",
        "避坑指南与课后作业",
    ])

    # L01 是首课，review 位置用课程总览（content）
    U.content(p, "课程总览  10 节课你将学到什么", [
        ("L01 评分标准与写作诊断", "看懂评分表、诊断自己的问题、建立正确方法论"),
        ("L02-L03 Task 1 图表全攻略", "折线/柱状/饼图/表格/流程图/地图，重点是 Overview"),
        ("L04-L07 Task 2 议论文全类型", "5 种题型识别 + 观点/讨论/利弊/问题解决型精讲"),
        ("L08 连贯衔接与词汇资源", "连接词不滥用、词汇替换、CC 与 LR 提分"),
        ("L09 语法准确性与句型多样化", "5 类必备句型 + 7 大高频错误，GRA 6→7"),
        ("L10 全真模考与系统复盘", "60 分钟流程、考前冲刺、提分路线图"),
    ], kicker="COURSE MAP")

    U.objectives(p, [
        "说清 Task 1 与 Task 2 在字数、时间、分值上的全部差异",
        "复述 TR / CC / LR / GRA 四个维度各自的考查重点",
        "判断自己的写作问题落在哪个维度，并设定提分优先级",
        "识别并改写 5 类典型中式英语表达",
        "理解 6 分、7 分、8 分作文的本质区别",
    ])

    U.pain_point(p, "导入：你为什么停在 6 分？", [
        ("立场模糊", "开头绕 3 句还没表态，考官读不到清晰 thesis"),
        ("中式英语", "With the development of society / In my humble opinion 满篇"),
        ("连接词滥用", "几乎每句开头都是 Furthermore / Moreover"),
        ("Task 1 漏 Overview", "只堆数字，没有总体趋势句——直接卡 6 分"),
        ("词汇句型单调", "important / people / society 反复，80% 简单句"),
    ], [
        ("立场前置", "引言最后一句给出明确 thesis statement"),
        ("学术替换", "There has been growing debate about… 替代中式开头"),
        ("精准衔接", "连接词只连真正有逻辑关系的句子"),
        ("先写 Overview", "Task 1 第二段必写 Overall, …"),
        ("替换+升级", "每个高频词备 2 个替换；复合句占比过半"),
    ])

    # ── PART 01 考试全貌 ──────────────────────────────────────────
    U.section(p, 1, "雅思写作考试全貌", "The Big Picture of IELTS Writing")
    U.concept(p, "写作考试的基本盘", "60 分钟，两个任务，一张评分表，决定你的 Writing 分数。", [
        ("考试时长", "总计 60 分钟，建议 Task 1 用 20 分钟、Task 2 用 40 分钟"),
        ("两个任务", "Task 1 图表/信件描述；Task 2 议论文——两者题型与要求完全不同"),
        ("评分构成", "Task 1 占总分 1/3，Task 2 占 2/3，加权得出 Writing 总分"),
        ("评分方式", "两个任务分别按 TR/CC/LR/GRA 四维 0-9 打分，再加权"),
        ("学术 vs 培训", "A 类 Task 1 写图表；G 类 Task 1 写信件——本课程聚焦 A 类"),
        ("机考 vs 纸笔", "机考有字数统计与撤销，评分标准完全一致"),
    ], note="先记住一句话：Task 2 决定你的分数地板，Task 1 决定你能不能锦上添花。")

    U.content(p, "Task 1 vs Task 2 核心规则对照", [
        ("字数下限", "Task 1 ≥150 词；Task 2 ≥250 词。低于下限直接扣 TR 分"),
        ("时间分配", "Task 1 ≈20 分钟；Task 2 ≈40 分钟，且建议先写 Task 2"),
        ("分值权重", "Task 2 权重是 Task 1 的两倍——精力要向 Task 2 倾斜"),
        ("内容性质", "Task 1 客观描述数据/流程，不写个人观点；Task 2 表达有论证的观点"),
        ("人称使用", "Task 1 不用 I；Task 2 观点题可用 I 表明立场"),
        ("常见误判", "把 Task 1 当成议论文写评论，是 A 类考生的高频失误"),
    ], note="深圳学生最大误区：花 35 分钟雕 Task 1，只剩 25 分钟写 Task 2，导致 Task 2 词数不足、论证仓促。")

    U.content(p, "为什么一定要先写 Task 2", [
        ("分值导向", "40 分的活儿优先做，把最清醒的大脑留给权重最高的任务"),
        ("状态管理", "Task 2 需要构思与论证，趁精力充沛完成质量更高"),
        ("时间兜底", "若超时，宁可压缩 Task 1，也别牺牲 Task 2 的字数与论证"),
        ("心理稳定", "先攻下大头，写 Task 1 时心态更稳、手感更顺"),
        ("阅卷现实", "Task 2 字数不足、结论缺失，是压分最狠的硬伤"),
        ("执行口诀", "先 T2 后 T1；40+20；T2 不达 250 词不收手"),
    ])

    U.content(p, "字数、时间与卷面的硬规则", [
        ("字数统计", "标点不计词，连字符词组按其规则计；机考看字数栏，纸笔靠估算"),
        ("字数估算", "纸笔考写前数好每行平均词数，按行数快速估算总词数"),
        ("超字数", "多写不直接扣分，但浪费时间、易出错——控制在 270-290 词最优"),
        ("卷面要求", "段落之间空行或缩进，分段清晰，字迹可辨认"),
        ("跑题判定", "完全偏离题目要求，TR 可能被压到 4-5 分，无法靠词汇语法挽回"),
        ("照抄题目", "原句照搬题目不计入有效字数，且暴露改写能力不足"),
    ], note="深圳考生常见：纸笔考因为不会估字数，写超了 350 词，Task 2 反而没检查时间。")

    U.example(p, "Task 1 与 Task 2 题目长什么样",
              "Task 1（图表）: The line graph below shows the consumption of three types of "
              "fast food in the UK from 2000 to 2020. Summarise the information by selecting "
              "and reporting the main features, and make comparisons where relevant.\n\n"
              "Task 2（议论文）: Some people believe that university education should be free "
              "for all students. Others think students should pay for their own studies. "
              "Discuss both views and give your own opinion.",
              answer="Task 1 关键词：summarise / main features / comparisons —— 要选重点、做比较、写 Overview。\n"
                     "Task 2 关键词：Discuss both views and give your own opinion —— 两方都要写，且必须给个人立场。",
              tip="拿到题先圈指令词：Task 1 看 summarise/compare；Task 2 看 discuss/agree/causes/outweigh，指令决定结构。")

    U.example(p, "同一话题：Task 1 思维 vs Task 2 思维",
              "假设话题都与“在线学习”相关。\n"
              "Task 1 给你一张折线图：2015-2023 年某国在线课程注册人数。\n"
              "Task 2 给你一个观点题：Online learning will eventually replace traditional "
              "classroom teaching. To what extent do you agree or disagree?",
              answer="Task 1 该做：描述注册人数的总体趋势 + 关键数据 + 比较，绝不评价“在线学习好不好”。\n"
                     "Task 2 该做：表明立场（多大程度同意），用论证链支撑，绝不只罗列数据。",
              tip="一句话区分：Task 1 回答 What happened（发生了什么）；Task 2 回答 What do you think（你怎么看、为什么）。")

    # ── PART 02 四维评分标准 ──────────────────────────────────────
    U.section(p, 2, "四维评分标准拆解", "The Four Assessment Criteria")
    U.concept(p, "四个维度，各占 25%", "考官手里是一张 band descriptor 表，逐维度打分再平均。", [
        ("TR 任务回应", "Task Response：是否完整、准确、充分地回应题目要求"),
        ("CC 连贯与衔接", "Coherence & Cohesion：信息组织、段落逻辑、衔接手段是否自然"),
        ("LR 词汇资源", "Lexical Resource：用词范围、精准度、搭配与拼写"),
        ("GRA 语法范围与准确性", "Grammatical Range & Accuracy：句型多样性与语法正确率"),
        ("权重相等", "四维各占 25%，任何一维过低都会拉低整体"),
        ("木桶效应", "总分≈四维的平均，短板维度决定你的天花板"),
    ], note="别只盯着背高级词（LR）。如果 TR 跑题、GRA 满篇错误，词汇再花也救不回总分。")

    U.content(p, "TR 任务回应：分数的地板", [
        ("Task 1 的 TR", "覆盖所有图表要素 + 写出 Overview + 数据准确 + 做必要比较"),
        ("Task 2 的 TR", "立场清晰且贯穿全文 + 充分论证 + 紧扣题目所有部分"),
        ("最常见扣分", "Task 2 漏答题目一半（如只 discuss 一方）；Task 1 漏 Overview"),
        ("字数与 TR", "不足字数=要点必然不全，TR 先扣一档"),
        ("跑题代价", "TR 一旦判跑题，封顶 5 分，其余三维再高也无用"),
        ("提分钥匙", "审题→确保每个指令都被回应→立场/Overview 显性化"),
    ], note="深圳学生 Discussion 题最常见：只写自己赞成的一方，另一方一笔带过——直接判 TR 不完整。")

    U.content(p, "CC 连贯与衔接：逻辑的骨架", [
        ("段落划分", "引言/主体/结论清晰，一段一个中心思想"),
        ("Topic Sentence", "每个主体段首句点明本段论点，承上启下"),
        ("逻辑连接", "连接词准确表达因果/转折/递进，不堆砌"),
        ("指代衔接", "用 this / these / such 指代前文，避免名词重复"),
        ("同义替换", "关键词换不同表达，保持衔接又不重复"),
        ("常见误区", "把 CC 理解成“多用连接词”，结果每句 Furthermore"),
    ], note="考官看到每句都有连接词，第一反应不是逻辑强，而是考生不懂逻辑关系——CC 反而扣分。")

    U.content(p, "LR 词汇资源：精准优于花哨", [
        ("用词范围", "能用一定量的不常见词与话题词，但要用对"),
        ("搭配 collocation", "have a profound impact on / pose a threat to —— 搭配比单词重要"),
        ("语域 register", "学术写作用正式词：commence / obtain / demonstrate"),
        ("拼写", "拼写错误直接扣 LR；高频学术词必须背准"),
        ("避免重复", "people / important / society 反复出现是低分信号"),
        ("用词原则", "宁可准确用中级词，也不要错误堆砌高级词"),
    ], note="深圳考生爱背难词，却把 phenomenon 拼成 phenominon、用错搭配——花哨反成扣分点。")

    U.content(p, "GRA 语法范围与准确性：稳定的根基", [
        ("句型范围", "简单句+并列句+复合句混用，7 分要求复合句占比可观"),
        ("准确性", "主谓一致、时态、冠词、单复数等基础错误要少"),
        ("标点", "逗号、句号正确，避免逗号粘连（comma splice）"),
        ("复杂句", "定语从句/状语从句/条件句/被动等用得自然"),
        ("错误密度", "7 分允许少量错误但不影响理解；6 分错误较多"),
        ("常见短板", "80% 简单句 → 句型范围不足，GRA 难破 6 分"),
    ], note="句型单调是深圳学生 GRA 卡 6 的头号原因：会写复合句，但考场上图省事全写简单句。")

    U.example(p, "用四维给一段作文打分",
              "学生原句（Task 2 主体段开头）:\n"
              "“Nowadays, with the development of society, technology is very important for people. "
              "Furthermore, it can help people in many ways. Furthermore, people use it every day.”",
              answer="TR: 论点空泛、未具体回应题目；CC: Furthermore 连用、逻辑混乱；"
                     "LR: important/people/help 重复、中式开头；GRA: 全简单句、句型单调。综合约 5 分。",
              tip="逐维度自检是最快的诊断法：写完一段，分别问自己 TR/CC/LR/GRA 各能拿几分。")

    U.example(p, "把上面的 5 分段落升到 7 分",
              "请把上页 5 分段落改写为 7 分水平（话题：technology 对生活的影响）。",
              answer="“One of the most significant benefits of modern technology lies in healthcare. "
                     "Advanced diagnostic tools, such as AI-assisted imaging, allow doctors to detect "
                     "diseases far earlier than before. Consequently, survival rates for conditions "
                     "like cancer have risen markedly over the past two decades.”",
              tip="升级公式：删中式开头→给具体论点→加真实例子→说明影响→精准衔接(Consequently)。")

    # ── PART 03 考官评分逻辑 ──────────────────────────────────────
    U.section(p, 3, "考官评分逻辑解析", "How Examiners Actually Grade")
    U.concept(p, "考官是怎么读你的作文的", "了解阅卷视角，才知道把力气花在哪。", [
        ("通读两遍", "第一遍抓整体印象（TR/CC），第二遍核对语言（LR/GRA）"),
        ("先看立场与结构", "立场是否清晰、分段是否合理，几秒内形成第一印象"),
        ("Topic Sentence", "考官靠每段首句判断你是否在回应题目"),
        ("看论证而非堆砌", "有论证链 vs 罗列观点，差出一个档位"),
        ("错误是否妨碍理解", "影响理解的错误最致命，小错容忍度更高"),
        ("整体印象定档", "先定大档（6/7/8），再微调，所以第一印象极重要"),
    ], note="引言写得清晰、第一段 Topic Sentence 有力，考官的初始印象分就稳了一半。")

    U.content(p, "分数的下限与提分区", [
        ("TR 决定下限", "立场清晰、回应完整，分数地板才稳在 6 以上"),
        ("CC 锁定基本盘", "结构清晰、衔接自然，配合 TR 稳住 6-6.5"),
        ("LR+GRA 是提分区", "词汇精准、句型多样，是 6→7→8 的主战场"),
        ("先补短板", "哪一维最低先补哪个，边际收益最高"),
        ("不要偏科", "只刷词汇不练结构，TR/CC 拖后腿，总分上不去"),
        ("现实路径", "多数 6 分考生：TR/CC 尚可，卡在 LR/GRA 的多样性"),
    ])

    U.content(p, "考官眼中的“危险信号”", [
        ("模板痕迹", "套话开头 + 万能模板段，考官一眼识破，TR/CC 双扣"),
        ("背诵段落", "与题目关联弱的背诵句，判定为未真实回应题目"),
        ("连接词轰炸", "Firstly/Furthermore/Moreover/Last but not least 连珠"),
        ("立场反复", "前段同意后段反对，结论又骑墙——TR 重扣"),
        ("字数注水", "重复啰嗦凑字数，LR/CC 暴露问题"),
        ("跑偏举例", "举例与论点无关，只是“讲故事”，论证无效"),
    ], note="“背一篇万能模板套所有题”在深圳很流行，但这是 TR 与 CC 同时扣分的高危做法。")

    U.content(p, "考官最想看到的“加分信号”", [
        ("清晰立场", "引言末句一句话亮明态度，全文一以贯之"),
        ("有效论证", "观点→解释→例子→影响，逻辑闭环"),
        ("精准衔接", "用对逻辑关系的少量连接词 + 指代 + 同义替换"),
        ("地道搭配", "自然的 collocation，而非生硬堆难词"),
        ("句型多样", "长短句交错，复合句服务于表达而非炫技"),
        ("紧扣题目", "每段都能回链到题目关键词"),
    ])

    U.example(p, "对比两种引言给考官的第一印象",
              "题目：Many people think that governments should invest more in public health "
              "than in other areas. To what extent do you agree or disagree?",
              answer="✗ 模糊：“Nowadays, health is a very important topic. There are many opinions "
                     "about it. In this essay, I will discuss this question.”（没有立场，全是废话）\n"
                     "✓ 清晰：“While other sectors clearly merit funding, I firmly believe that "
                     "prioritising public health spending yields the greatest long-term benefits "
                     "for society.”（一句话亮明立场）",
              tip="引言最后一句=thesis statement，必须让考官在第一印象阶段就读到你的立场。")

    U.example(p, "三秒判断：这段在回应题目吗",
              "题目要求：Discuss both views and give your own opinion（关于是否该禁止私家车进城）。\n"
              "学生只写了：私家车的种种坏处（污染、拥堵、停车难），全文都在批评私家车。",
              answer="未完整回应。Discussion 题必须公正呈现两方（支持/反对禁车），再给个人立场；"
                     "只写一方=TR 不完整，封顶约 6 分。",
              tip="Discussion 题自检：我有没有为“对立观点”单独写一段、并给到合理篇幅？")

    # ── PART 04 中式英语诊断 ──────────────────────────────────────
    U.section(p, 4, "中式英语诊断与改写", "Diagnosing Chinglish")
    U.concept(p, "什么是“中式英语”", "语法没错，但母语者不会这么写——这正是 LR/CC 的隐性扣分项。", [
        ("直译思维", "把中文逐词译成英文：人民群众→people masses"),
        ("陈腐套语", "With the development of society / As is known to all"),
        ("过度谦辞", "In my humble opinion / As far as I am concerned"),
        ("连接词依赖", "Last but not least / What's more 当万能过渡"),
        ("空话开头", "Nowadays, … is a hot topic discussed by many people"),
        ("结果", "考官识别为模板化、非地道表达，LR 与 CC 同步受影响"),
    ], note="中式英语不是“语法错误”，而是“不地道”——它让你的作文显得套路化，是 6 分天花板的隐形推手。")

    U.content(p, "五大类中式英语清单（要戒掉）", [
        ("空洞开头类", "Nowadays / With the development of society / In recent years…"),
        ("过度谦辞类", "In my humble opinion / As far as I am concerned"),
        ("陈腐过渡类", "Last but not least / What's more / On the one hand…(机械)"),
        ("绝对化类", "All people know / Everyone agrees / It is known to all"),
        ("口语化类", "a lot of / kids / things / get / good——语域偏低"),
        ("逐字直译类", "give you some color see see 式直译（含搭配错误）"),
    ], note="深圳模考里出现频率最高的三句：With the development of society / In my humble opinion / Last but not least——三连必扣印象分。")

    U.content(p, "地道替换：从中式到学术", [
        ("替 Nowadays", "In contemporary society / Over the past few decades"),
        ("替 very important", "play a pivotal/crucial role in / be of great significance"),
        ("替 In my opinion", "I would argue that / It seems to me that / I am convinced that"),
        ("替 a lot of people", "a significant proportion of individuals / many"),
        ("替 Last but not least", "Equally important / A further consideration is that"),
        ("替 good/bad", "beneficial / detrimental / advantageous / counterproductive"),
    ])

    U.content(p, "改写中式英语的三步法", [
        ("第一步 识别", "读自己的句子，标出套话、谦辞、口语词、绝对化表达"),
        ("第二步 删减", "能删的废话直接删——空洞开头往往可整句删掉"),
        ("第三步 升级", "用学术搭配/精准动词替换，并检查语域是否统一"),
        ("自检问题", "母语者会这么开头吗？这个词在学术文章里出现吗？"),
        ("替换有度", "替换是为了精准，不是为了炫难词——用错更糟"),
        ("建立词库", "把自己的高频中式表达整理成“黑名单 → 替换表”"),
    ], note="先做减法再做加法：很多深圳学生的中式开头其实整句删掉，文章反而更紧凑、TR 更高。")

    U.example(p, "中式英语整段改写实战",
              "学生原文（Task 2 引言）:\n"
              "“Nowadays, with the development of society, education is becoming more and more "
              "important. As is known to all, many people think online education is good. "
              "In my humble opinion, I think it has both advantages and disadvantages.”",
              answer="改写（学术、立场清晰）:\n"
                     "“The rapid expansion of digital technology has transformed how education is "
                     "delivered, and online learning in particular has sparked considerable debate. "
                     "While it offers undeniable flexibility, I would argue that it cannot fully "
                     "replace the interactive benefits of traditional classrooms.”",
              tip="改写要点：删 Nowadays/As is known to all/humble opinion；给具体背景；末句亮明立场。")

    U.example(p, "句子级中式英语门诊",
              "诊断并改写下列句子：\n"
              "1) Last but not least, money is very important for people.\n"
              "2) As far as I am concerned, I think the government should do something.\n"
              "3) There are more and more people use the internet nowadays.",
              answer="1) A further crucial factor is the role of financial resources.\n"
                     "2) I would argue that governments must take decisive action.\n"
                     "3) An increasing number of people now rely on the internet.（改 there be + 动词的硬伤）",
              tip="第 3 句还有语法硬伤：there are…people use 是双谓语，必须改成定语从句或换句式。")

    # ── PART 05 词汇与句型 ────────────────────────────────────────
    U.section(p, 5, "诊断期词汇与句型", "Vocabulary & Sentence Patterns")
    U.vocab(p, "评分相关术语英文表达", [
        ("Task Response (TR)", "任务回应：是否完整准确回应题目"),
        ("Coherence & Cohesion (CC)", "连贯与衔接：逻辑组织与衔接手段"),
        ("Lexical Resource (LR)", "词汇资源：用词范围、精准、搭配、拼写"),
        ("Grammatical Range & Accuracy (GRA)", "语法范围与准确性"),
        ("band descriptor", "评分细则表（每个分数段的描述）"),
        ("paraphrase", "改写（题目/句子换词换句式）"),
        ("thesis statement", "立场句（引言末句表明观点）"),
        ("Overview", "总体概述（Task 1 必写段）"),
        ("collocation", "词语搭配（高分关键）"),
    ])

    U.vocab(p, "立场表达句型库（Task 2）", [
        ("I firmly believe that …", "我坚定认为……（强立场）"),
        ("I would argue that …", "我认为……（学术常用，比 I think 高级）"),
        ("It seems to me that …", "在我看来……"),
        ("I am convinced that …", "我深信……"),
        ("In my view, … should be …", "在我看来，……应该……"),
        ("There is no doubt that …", "毫无疑问……（慎用，需有理据）"),
        ("While …, I maintain that …", "尽管……，我仍坚持……（让步立场）"),
        ("On balance, I believe …", "总的来说，我认为……（利弊权衡后）"),
        ("I partially agree that …", "我部分赞同……（to what extent 题用）"),
    ])

    U.vocab(p, "学术高级词替换高频词", [
        ("important → crucial / pivotal", "至关重要的"),
        ("good → beneficial / advantageous", "有益的"),
        ("bad → detrimental / adverse", "有害的"),
        ("a lot of → a significant number of", "大量的"),
        ("show → demonstrate / reveal", "表明、揭示"),
        ("get → obtain / acquire", "获得"),
        ("important to → essential for", "对……必不可少"),
        ("think → maintain / contend / argue", "认为、主张"),
        ("big → substantial / considerable", "可观的"),
    ])

    U.two_col(p, "正式 vs 口语：写作语域对照", "口语/低分用词", [
        ("kids", "儿童口语词"),
        ("a lot of / lots of", "口语量词"),
        ("things / stuff", "含义空泛"),
        ("get / got", "万能动词"),
        ("good / bad", "评价含糊"),
        ("nowadays / these days", "中式开头"),
        ("big problem", "搭配偏口语"),
    ], "学术/高分用词", [
        ("children / the young", "中性正式"),
        ("a considerable amount of", "正式量化"),
        ("factors / aspects / issues", "指代精准"),
        ("obtain / acquire / gain", "精准动词"),
        ("beneficial / detrimental", "评价精准"),
        ("in recent decades", "时间状语得体"),
        ("a pressing issue", "学术搭配"),
    ])

    U.two_col(p, "万能黑名单 vs 学术开头句", "✗ 中式万能开头", [
        ("With the development of society…", "信息为零的套话"),
        ("Nowadays, … is a hot topic.", "空洞开头"),
        ("As is known to all…", "绝对化断言"),
        ("Every coin has two sides.", "陈腐谚语"),
        ("In my humble opinion…", "过度谦辞"),
        ("People's opinions vary.", "正确的废话"),
    ], "✓ 学术切入句", [
        ("Over the past few decades, …", "时间状语自然切入"),
        ("… has sparked considerable debate.", "点出争议性"),
        ("It is often argued that …", "引出常见观点"),
        ("While … , it is worth considering …", "让步式开头"),
        ("I would argue that …", "学术表态"),
        ("Opinion on this issue is divided.", "客观陈述分歧"),
    ])

    # ── PART 06 方法与范例 ────────────────────────────────────────
    U.section(p, 6, "诊断方法与高分范例", "Diagnosis Method & Models")
    U.steps(p, "写作自我诊断五步法", [
        ("第一步：核对 TR", "立场清晰吗？题目每个部分都回应了吗？字数够吗？"),
        ("第二步：检查 CC", "分段合理吗？每段首句点题吗？连接词用对逻辑吗？"),
        ("第三步：审视 LR", "有重复词吗？搭配对吗？有中式表达和拼写错误吗？"),
        ("第四步：排查 GRA", "句型单调吗？有主谓/时态/冠词错误吗？"),
        ("第五步：定优先级", "找出最低维度，作为下一篇的专项突破点"),
    ])

    U.steps(p, "把作文交给老师前的自查流程", [
        ("通读一遍", "假装自己是考官，能否一眼读到立场与结构"),
        ("圈出重复词", "用笔圈出现 3 次以上的词，准备替换"),
        ("标连接词", "数一数连接词，超过每段 2-3 个就删"),
        ("查时态", "Task 1 看图表时间；Task 2 一般现在时为主"),
        ("数字数", "确认 Task 1≥150、Task 2≥250"),
        ("记录问题", "把发现的问题写进个人错题本，按四维归类"),
    ])

    U.model_answer(p, "高分引言范文 + 批注",
                   "Some people think that university education should be free for all. "
                   "Others believe students should pay. Discuss both views and give your opinion.",
                   "The question of whether higher education should be funded by the state or by "
                   "students themselves has become increasingly contentious. Advocates of free "
                   "tuition argue that it widens access and promotes social mobility, whereas "
                   "opponents contend that those who benefit financially from a degree should "
                   "bear its cost. This essay will examine both positions before arguing that a "
                   "means-tested system offers the most equitable solution.",
                   ["开头不用 Nowadays，用话题改写自然切入",
                    "increasingly contentious 精准点出“有争议”",
                    "两方各用 argue / contend 公正呈现，CC 强",
                    "末句 thesis 给出第三条路（means-tested），立场清晰",
                    "This essay will examine… 预告结构，衔接自然",
                    "全段无中式套语，语域统一，LR 到位"])

    U.model_answer(p, "高分主体段范文 + 批注",
                   "（同上题，支持“免费教育拓宽入学机会”一方）",
                   "Those in favour of free university education emphasise its role in levelling "
                   "the playing field. When tuition fees are removed, talented students from "
                   "low-income backgrounds are no longer deterred by financial barriers. In "
                   "Germany, for instance, the abolition of fees has been accompanied by a marked "
                   "rise in enrolment among first-generation university students. Such inclusivity "
                   "not only benefits individuals but also strengthens the wider economy by "
                   "expanding the pool of skilled graduates.",
                   ["首句=Topic Sentence，点明本段论点（公平）",
                    "When… 条件状语解释机制，逻辑清晰",
                    "Germany, for instance 真实国家例证，论证有效",
                    "Such inclusivity… 用 such 指代，衔接自然(CC)",
                    "not only… but also… 句型升级(GRA)",
                    "结尾升华到经济影响(Impact)，论证链完整"])

    U.compare(p, "低分 vs 高分：引言写法", "✗ 低分引言（约 5 分）", [
        ("Nowadays education is very important", "空洞开头无信息"),
        ("Many people have different opinions", "正确的废话"),
        ("Some people think A, some think B", "原句照搬题目"),
        ("In this essay I will discuss it", "无立场预告"),
        ("用词 important/people/think 重复", "LR 单薄"),
    ], "✓ 高分引言（约 7 分）", [
        ("用话题改写自然切入", "信息密度高"),
        ("精准点出争议性", "increasingly contentious"),
        ("两方各用不同动词公正呈现", "argue / contend"),
        ("末句给出明确 thesis", "立场清晰"),
        ("搭配地道、语域统一", "LR/CC 双高"),
    ])

    U.compare(p, "低分 vs 高分：主体段写法", "✗ 低分主体段（约 5.5）", [
        ("Technology is good for people.", "论点空泛"),
        ("For example, we use phones.", "例子无展开"),
        ("It helps us communicate.", "无影响分析"),
        ("So technology is good.", "结论=重复论点"),
        ("全简单句、用词重复", "GRA/LR 双弱"),
    ], "✓ 高分主体段（约 7）", [
        ("Topic Sentence 点明具体论点", "如医疗进步"),
        ("Explanation 解释机制", "为何能更早诊断"),
        ("Example 真实例证", "AI 影像/MRI"),
        ("Impact 升华影响", "生存率显著提升"),
        ("长短句+精准搭配", "GRA/LR 双高"),
    ])

    # ── PART 07 课堂练习 ──────────────────────────────────────────
    U.section(p, 7, "课堂练习", "In-Class Practice")
    U.drill(p, "练习一：识别题型与指令", "读下列题目，写出题型与必须回应的部分。", [
        "To what extent do you agree or disagree that AI will replace human workers?",
        "Discuss both views and give your own opinion (on remote work).",
        "What are the causes of traffic congestion and what solutions can be offered?",
        "Do the advantages of studying abroad outweigh the disadvantages?",
        "Some say museums should be free; others disagree. Discuss + your opinion.",
    ])

    U.drill(p, "练习二：四维找茬", "判断下面句子主要扣哪个维度（TR/CC/LR/GRA），并说明理由。", [
        "Furthermore, technology is good. Furthermore, it helps people.",
        "The number of cars are increasing every year in big city.",
        "Nowadays, with the development of society, this is a hot topic.",
        "I think both sides have their reasons, so it is hard to say.",
        "Internet has changed people life and make them more happy.",
    ])

    U.drill(p, "练习三：中式英语改写", "把下列中式表达改写为学术表达。", [
        "In my humble opinion, this problem is very serious.",
        "Last but not least, the government should do something.",
        "As is known to all, money is very important for everyone.",
        "There are more and more people study abroad nowadays.",
        "With the development of society, our life is better and better.",
    ])

    U.drill(p, "练习四：写一个 thesis statement", "为下列题目各写一句清晰的立场句。", [
        "Should children learn a second language at primary school? (agree/disagree)",
        "Are city life advantages greater than its disadvantages? (outweigh)",
        "Public transport vs building more roads — discuss both + opinion.",
        "Causes & solutions of obesity. (说明你将讨论原因与方案)",
        "To what extent should governments fund the arts? (partial agreement)",
    ])

    # ── PART 08 避坑指南 ──────────────────────────────────────────
    U.section(p, 8, "避坑指南", "Pitfalls to Avoid")
    U.pain_point(p, "诊断阶段最易踩的坑", [
        ("只补词汇不看结构", "背了一堆难词，TR/CC 拖后腿，总分纹丝不动"),
        ("迷信万能模板", "一套模板套所有题，TR 判跑题/CC 判机械"),
        ("立场骑墙", "怕写错不敢表态，结果 TR 严重扣分"),
        ("忽视字数", "Task 2 不到 250 词还浑然不觉"),
        ("不分维度复盘", "批改后只看总分，不知道哪一维拖后腿"),
    ], [
        ("四维同抓", "短板优先，结构与立场先立住"),
        ("拒绝模板", "用结构框架而非固定句子套话"),
        ("敢于表态", "宁可立场鲜明，也不要骑墙模糊"),
        ("控字数", "考前练就估字数能力，270-290 词最佳"),
        ("按维度归档", "错题本按 TR/CC/LR/GRA 分类，逐项攻破"),
    ])

    U.content(p, "常见错误清单（Task 通用）", [
        ("照抄题目", "引言原句照搬，不计有效字数且暴露改写弱"),
        ("立场不一致", "前后段观点矛盾，结论又骑墙"),
        ("段落失衡", "一段五句、一段两句，CC 受损"),
        ("结论加新信息", "结论里突然冒出新论点，结构失控"),
        ("数字/事实错误", "Task 1 数据读错；Task 2 编造离谱事实"),
        ("拼写与大小写", "高频词拼错、句首不大写，LR 直接扣"),
    ], note="结论里加新论点是深圳学生常见失控点：时间不够就把没写完的想法塞进结论，结构反而崩了。")

    U.content(p, "常见错误清单（语言层面）", [
        ("主谓不一致", "The number of cars are… → is"),
        ("冠词缺失", "Internet has changed… → The Internet"),
        ("时态混乱", "Task 1 过去图表用现在时"),
        ("逗号粘连", "两个完整句用逗号连接，应改句号或连词"),
        ("搭配错误", "make a big effect → have a significant effect"),
        ("语域混杂", "学术文里夹 kids / a lot of / stuff"),
    ])

    U.tip_card(p, "诊断阶段四张速记卡", [
        ("TR 卡", "立场清晰 + 回应完整 + 字数达标，分数地板才稳"),
        ("CC 卡", "分段清晰 + 首句点题 + 连接词用对逻辑"),
        ("LR 卡", "搭配优先 + 替换高频词 + 拼写零错"),
        ("GRA 卡", "复合句过半 + 主谓/时态/冠词零基础错"),
    ])

    U.tip_card(p, "提分优先级四张行动卡", [
        ("先定短板", "用四维自评找出最低维度，作为本周专项"),
        ("立场先行", "每篇先写好 thesis，再展开论证"),
        ("替换清单", "随身带高频词替换表，写作时即查即换"),
        ("范文拆解", "每周拆 2 篇 Band 7 范文的结构与搭配"),
    ])

    # ── 收尾 ─────────────────────────────────────────────────────
    U.checklist(p, "本课自检清单", [
        "我能说出 Task 1 与 Task 2 在字数/时间/分值上的全部差异",
        "我能复述 TR/CC/LR/GRA 各自的考查重点",
        "我知道为什么要先写 Task 2",
        "我能识别并改写 5 类中式英语",
        "我理解 Overview 缺失为何卡 6 分",
        "我能用四维给一段作文打分",
        "我建立了个人写作问题的四维清单",
    ])

    U.summary(p, 1, [
        "Task 2 决定分数地板，先写 T2；T1 占 1/3、T2 占 2/3",
        "四维各 25%：TR 是地板，LR+GRA 是 6→7→8 的提分区",
        "中式英语三连（development of society / humble opinion / last but not least）必戒",
        "Overview 缺失、立场骑墙、连接词滥用是深圳三大硬伤",
    ], takeaway="先把结构与立场立住，再雕词汇语法——短板维度决定你的总分天花板。")

    U.homework(p, 1, [
        "不限时写 1 篇 Task 2，请老师按四维各打分，记下最低维度",
        "精读 5 篇 Band 7+ 范文，标注每篇的 thesis 句与论证结构",
        "整理个人“中式英语黑名单 → 学术替换表”，至少 10 组",
        "统计自己最近一篇作文里出现 3 次以上的词，各找 2 个替换",
    ], est_time="90 分钟")

    U.preview(p, 2, "Task 1 折线图与柱状图", [
        "四段式框架：Paraphrase / Overview / Detail A / Detail B",
        "Overview 是评分重点，必写且只写总体趋势",
        "趋势词 + 幅度词 + 数据 = 完整描述句",
        "动词句 vs 名词句、数字与时态处理",
    ])


# ════════════════════════════════════════════════════════════════
#  L02 Task 1 折线图与柱状图
# ════════════════════════════════════════════════════════════════
def build_l02(p):
    U.cover(p, "写作", 2, "Task 1 折线图与柱状图",
            "Line Graphs & Bar Charts", total=10)

    U.agenda(p, [
        "Task 1 动态图四段式框架",
        "Overview 段：评分的重中之重",
        "趋势描述词汇系统（上升/下降/平稳/波动）",
        "幅度词与精确数据表达",
        "动词句 vs 名词句的句型变换",
        "时态、数字与比较的处理",
        "课堂练习：折线图与柱状图实战",
        "避坑指南与课后作业",
    ])

    U.review(p, [
        "Task 1 占 1/3、Task 2 占 2/3，建议先写 Task 2",
        "四维评分 TR/CC/LR/GRA 各 25%，TR 是分数地板",
        "Task 1 的 TR 关键：覆盖要素 + 写 Overview + 数据准确",
        "戒中式英语：Nowadays / development of society / humble opinion",
        "本课目标：用四段式 + 趋势词把动态图写到 Band 7",
    ])

    U.objectives(p, [
        "用四段式框架完整组织一篇折线图/柱状图作文",
        "写出不含具体数字、只概括总体趋势的 Overview 段",
        "熟练运用上升/下降/平稳/波动四类趋势词 + 幅度词",
        "在动词句与名词句之间自由切换，增加句型多样性",
        "正确处理时态、数字与比较，达到 Task 1 Band 7",
    ])

    U.pain_point(p, "导入：折线图为什么写不到 7", [
        ("只堆数字", "In 1990 it was 200, in 2000 it was 350…像报数"),
        ("漏写 Overview", "没有总体趋势句，TR 直接卡 6"),
        ("数据全写", "每个点都描述，没有“选重点”"),
        ("时态用错", "过去的图用现在时"),
        ("句型单调", "全是 X increased to Y，一种句式到底"),
    ], [
        ("数字配趋势", "rose sharply from 200 to 480，趋势+数据结合"),
        ("先写 Overview", "Overall, …，只写总体趋势不写数字"),
        ("选择性描述", "只写最高/最低/转折点，忽略平稳细节"),
        ("时态对齐", "图表时间是过去→全文过去时"),
        ("句型轮换", "动词句/名词句/比较句交替使用"),
    ])

    # PART 01 四段式框架
    U.section(p, 1, "动态图四段式框架", "The Four-Paragraph Structure")
    U.concept(p, "动态图的黄金结构", "一篇高分 Task 1 = 改写 + 概述 + 两段细节，结构永远先行。", [
        ("第 1 段 Paraphrase", "改写题目：图表类型 + 主题 + 时间范围，1-2 句，禁照抄"),
        ("第 2 段 Overview", "最重要！总体趋势 + 最高/最低/最显著特征，不含具体数字"),
        ("第 3 段 Detail A", "描述主要趋势/组别的具体数据变化，3-4 句，含关键数字"),
        ("第 4 段 Detail B", "描述次要趋势/对比组别的具体数据，3-4 句，含关键数字"),
        ("字数分配", "P1≈25 / P2≈45 / P3≈45 / P4≈45 ≈ 160 词"),
        ("结构口诀", "改写—概述—细节A—细节B，四段缺一不可"),
    ], note="Overview 段是考官评分的重中之重——没有 Overview，几乎不可能过 6 分。")

    U.content(p, "第 1 段 Paraphrase 怎么写", [
        ("换图表名词", "line graph → line chart / graph；bar chart → bar graph"),
        ("换动词", "shows → illustrates / depicts / presents / gives information about"),
        ("换主题表达", "the number of → the figures for / the quantity of"),
        ("保留信息", "图表类型、主题、时间/地点范围必须保留，不能改变事实"),
        ("禁照抄", "原句照搬不计有效字数，且暴露改写能力不足"),
        ("时间状语", "between 1990 and 2020 / over a 30-year period / from… to…"),
    ], note="深圳学生常把题目原句抄成第一段——这是 TR 与 LR 的双重失分，务必改写。")

    U.content(p, "第 2 段 Overview 怎么写（核心）", [
        ("只写总体", "概括最显著的总体规律，不写任何具体数字"),
        ("找对比/极值", "两条线的相反走势、最高/最低组别、整体升降"),
        ("开头词", "Overall, … / In general, … / It is clear that …"),
        ("写 1-2 句", "通常 2 句：一句总趋势，一句最高/最低或对比"),
        ("不分析原因", "Task 1 不解释为什么，只描述是什么"),
        ("自检", "把 Overview 单独读出来，能否概括整张图"),
    ], note="判断 Overview 合格的标准：只读这两句话，听者就能想象整张图的大致样子。")

    U.content(p, "第 3、4 段 Detail 怎么写", [
        ("分组逻辑", "按数据相似性分组：相近趋势归一段，对比趋势分两段"),
        ("Detail A 写主线", "最显著/最大的趋势或组别先写，含起点、变化、终点"),
        ("Detail B 写对比", "次要趋势或对比组别，与 A 形成呼应"),
        ("数据点选择", "写起点、终点、最高点、最低点、转折点，省略平稳段"),
        ("做比较", "用 compared with / whereas / while 横向比较组别"),
        ("数字精确", "数据要准确，约数用 approximately / just over / nearly"),
    ], note="不要把每个数据都写进去——选择性描述是高分标志，列全所有点反而像报数。")

    U.example(p, "折线图四段式完整范文",
              "图表信息：折线图显示 1990-2020 年英国咖啡与茶的年消费量（百万升）。"
              "咖啡：1990=200，持续上升到 2020=600；茶：1990=500，持续下降到 2020=250。",
              answer="P1: The line graph illustrates changes in the annual consumption of coffee "
                     "and tea in the UK between 1990 and 2020, measured in millions of litres.\n"
                     "P2 (Overview): Overall, the two beverages followed opposite trends, with coffee "
                     "rising substantially while tea declined steadily over the period.\n"
                     "P3: Coffee consumption began at 200 million litres in 1990 and climbed "
                     "consistently, reaching 600 million litres by 2020 — a threefold increase.",
              tip="P1 改写、P2 只写总体相反趋势、P3 给主线数据。注意 Overview 不出现任何数字。")

    U.example(p, "柱状图四段式完整范文",
              "图表信息：柱状图显示 2020 年四个城市（A/B/C/D）人均年用水量（升）。"
              "A=320，B=210，C=180，D=95。",
              answer="P1: The bar chart compares the average annual water consumption per person in "
                     "four cities in 2020, measured in litres.\n"
                     "P2 (Overview): Overall, City A consumed by far the most water per capita, "
                     "whereas City D used the least, with a substantial gap between the two extremes.\n"
                     "P3: At 320 litres, City A's per-capita consumption was over three times that of "
                     "City D, which stood at just 95 litres. City B followed with 210 litres.",
              tip="静态柱状图无时间变化，Overview 找最大/最小组别与差距，用 by far / whereas 做比较。")

    # PART 02 Overview 专项
    U.section(p, 2, "Overview 段专项突破", "Mastering the Overview")
    U.concept(p, "为什么 Overview 决定成败", "它是考官判断你“会不会概括”的唯一窗口。", [
        ("评分权重", "TR 明确要求 select and report the main features"),
        ("没有就封顶", "缺 Overview，TR 几乎封顶在 5-6 分"),
        ("位置", "通常放第 2 段，也可放结尾，但第 2 段最稳"),
        ("内容", "总体趋势 + 极值/对比，绝不含具体数字"),
        ("长度", "1-2 句即可，贵在精准不在长"),
        ("信号词", "Overall / In general / It is evident that…"),
    ], note="把 Overview 写在第二段、用 Overall 开头，是最稳的拿分方式——别藏在结尾让考官找。")

    U.content(p, "动态图 Overview 找点公式", [
        ("找总方向", "整体是升、是降、还是有升有降"),
        ("找对比", "多条线之间是否相反走势/差距悬殊"),
        ("找极值", "哪条线最高、哪条最低、何时达到峰值"),
        ("找转折", "是否有明显的拐点（先升后降等）"),
        ("组合成句", "Overall, A 升 while B 降；A 始终高于 B"),
        ("禁数字", "公式里绝不出现具体数值"),
    ])

    U.content(p, "静态图 Overview 找点公式", [
        ("找最大组", "哪一类占比/数值最高（the largest / the highest）"),
        ("找最小组", "哪一类最低（the smallest / the least）"),
        ("找差距", "极值之间差距是否悬殊（a marked gap）"),
        ("找分层", "是否能分成高/中/低几档"),
        ("组合成句", "Overall, X 最高 whereas Y 最低，差距明显"),
        ("禁数字", "同样不写具体数值"),
    ])

    U.content(p, "Overview 常用句型模板", [
        ("总趋势", "Overall, there was a general upward/downward trend in …"),
        ("相反走势", "While … rose steadily, … showed the opposite pattern"),
        ("极值（动态）", "… reached its peak in …, whereas … hit its lowest point"),
        ("极值（静态）", "… accounted for the largest proportion, while … the smallest"),
        ("差距", "A striking feature is the considerable gap between … and …"),
        ("整体稳定", "Overall, figures for … remained relatively stable throughout"),
    ], note="把这几个句型背熟并能套用——Overview 是最值得“模板化”的一段，因为它结构固定。")

    U.example(p, "只练 Overview：多条折线图",
              "折线图：2000-2020 年三国（X/Y/Z）手机普及率（%）。"
              "X 持续上升至最高；Y 先升后稳；Z 全程最低、缓慢上升。",
              answer="Overview: Overall, mobile phone penetration increased in all three countries "
                     "over the period, with Country X experiencing the most dramatic growth to become "
                     "the highest, while Country Z consistently remained the lowest despite a gradual rise.",
              tip="多条线 Overview：先说共同趋势（都上升），再点出最高与最低，不写任何百分比。")

    U.example(p, "只练 Overview：分组柱状图",
              "柱状图：男性与女性在五种休闲活动上的参与率（%）。"
              "男性在体育类最高；女性在阅读类最高；总体女性参与率略高。",
              answer="Overview: Overall, women tended to participate slightly more than men across "
                     "most activities, with reading being the most popular pastime among women and "
                     "sport ranking highest for men.",
              tip="分组柱状图 Overview：先给整体对比（女性略高），再点出各组的最高项，避免逐项罗列。")

    # PART 03 趋势词汇系统
    U.section(p, 3, "趋势描述词汇系统", "Trend Vocabulary System")
    U.concept(p, "趋势词是 Task 1 的核心 LR", "上升/下降/平稳/波动各备一套，再配幅度词，描述才精准。", [
        ("四类趋势", "上升 / 下降 / 平稳 / 波动——每类备 4-5 个词"),
        ("词性双形", "动词形 rise 与名词形 a rise，便于句型变换"),
        ("配幅度词", "趋势词 + slightly/sharply 表示变化大小"),
        ("配速度词", "gradually / rapidly / steadily 表示变化快慢"),
        ("避免重复", "increase 用多了换 rise / climb / grow"),
        ("精准优先", "soar/plummet 表急剧，用错幅度反而扣分"),
    ], note="深圳学生爱用 increase/decrease 走天下——同义替换才是 Task 1 拉开 LR 的关键。")

    U.content(p, "上升与下降词（按幅度排序）", [
        ("上升（小→大）", "edge up < rise / increase / climb < grow < surge / soar / rocket"),
        ("下降（小→大）", "dip < fall / decrease / decline < drop < plunge / plummet"),
        ("到达峰值", "peak at / reach a peak / hit a high of / culminate in"),
        ("到达谷底", "bottom out / reach a low / hit a trough"),
        ("名词形", "a rise / an increase / a surge / a decline / a slump"),
        ("起点表达", "stood at / started at / began the period at"),
    ], note="soar/plummet 只用于急剧大幅变化；缓慢小幅却用 soar，是“幅度用词不当”的常见扣分。")

    U.content(p, "平稳与波动词", [
        ("保持平稳", "remained stable / steady / constant / unchanged"),
        ("趋于平稳", "levelled off / plateaued / flattened out"),
        ("小幅波动", "fluctuated / varied / oscillated"),
        ("波动范围", "fluctuated between X and Y / hovered around X"),
        ("名词形", "a plateau / fluctuations / stability"),
        ("无变化", "showed no significant change / saw little movement"),
    ])

    U.content(p, "幅度词与速度词", [
        ("幅度小", "slightly / marginally / modestly（约 5% 以内）"),
        ("幅度中", "moderately / noticeably / considerably"),
        ("幅度大", "significantly / substantially / dramatically / sharply"),
        ("速度快", "rapidly / swiftly / abruptly"),
        ("速度慢", "gradually / steadily / slowly / progressively"),
        ("放句中", "rose sharply / a gradual decline / increased significantly"),
    ], note="幅度词放在动词后（rose sharply）或名词前（a sharp rise）都行——这正是动词句/名词句切换的入口。")

    U.example(p, "趋势词填空实战",
              "看数据描述趋势：A 线从 100 缓慢升到 130；B 线从 400 急剧跌到 120；"
              "C 线全程在 250 上下小幅波动。用合适趋势词+幅度词各写一句。",
              answer="A: Line A rose gradually from 100 to 130.\n"
                     "B: Line B plummeted sharply from 400 to 120.\n"
                     "C: Line C fluctuated slightly, hovering around 250 throughout the period.",
              tip="缓慢小幅→gradually/slightly；急剧大幅→plummeted/sharply；上下小动→fluctuated/hovered around。")

    U.example(p, "趋势词同义替换升级",
              "原句重复严重：“Sales increased in 2010. Sales increased in 2015. "
              "Sales increased in 2020.”请用不同趋势词+句型改写为一句。",
              answer="Sales climbed steadily throughout the period, rising from their 2010 level "
                     "and continuing to grow until 2020.\n"
                     "（或名词句）There was a steady upward trend in sales across the entire period.",
              tip="把三句重复合并为一句趋势概述，用 climbed/rising/upward trend 替换重复的 increased。")

    # PART 04 句型、时态与数字
    U.section(p, 4, "句型、时态与数字", "Patterns, Tenses & Figures")
    U.concept(p, "动词句与名词句", "同一信息两种说法，交替使用是 GRA 与 LR 的双重加分。", [
        ("动词句", "主语 + 趋势动词 + 幅度词：Sales rose sharply to 500"),
        ("名词句", "There be + 幅度形容词 + 趋势名词：There was a sharp rise in sales to 500"),
        ("名词句变体", "主语 + saw/experienced + a rise：Sales saw a sharp rise"),
        ("好处", "两种交替，避免句式单调，提升 GRA 多样性"),
        ("幅度对应", "动词句用副词(sharply)，名词句用形容词(sharp)"),
        ("自然为先", "不为变换而变换，读起来通顺最重要"),
    ], note="句型单调是 Task 1 GRA 卡 6 的主因——刻意练习动词句↔名词句互换，能立竿见影提分。")

    U.content(p, "动词句 ↔ 名词句互换公式", [
        ("公式 1", "X increased significantly. ↔ There was a significant increase in X."),
        ("公式 2", "X fell sharply. ↔ X experienced a sharp fall."),
        ("公式 3", "X rose to 500. ↔ X saw a rise to 500."),
        ("副词→形容词", "sharply→sharp / gradually→gradual / steadily→steady"),
        ("加主语 saw", "X saw / experienced / underwent + a + 形容词 + 名词"),
        ("练习建议", "每句趋势都写两种版本，强制句型多样"),
    ])

    U.content(p, "时态的判断与统一", [
        ("过去图表", "时间是过去（如 1990-2020）→ 全文一般过去时"),
        ("现在/通用", "无具体时间或通用流程 → 一般现在时"),
        ("未来预测", "含 predicted/will/by 2050 → will / be expected to"),
        ("混合时间", "既有历史又有预测 → 分别用过去时与将来时"),
        ("常见错误", "过去图表用现在时，是 GRA 高频扣分"),
        ("自检", "确认图表时间轴，全文时态保持一致"),
    ], note="先看图的时间轴再动笔：是过去就一律过去时，别一会儿 rose 一会儿 rises。")

    U.content(p, "数字与比较的精确表达", [
        ("约数", "approximately / around / roughly / just over / just under"),
        ("整数倍", "doubled / tripled / a twofold/threefold increase"),
        ("分数比例", "accounted for one third / made up half of"),
        ("百分比变化", "rose by 20% (变化量) vs rose to 20% (终值)——别混"),
        ("比较句", "twice as high as / three times more than / compared with"),
        ("差距", "a gap of … / X exceeded Y by …"),
    ], note="rose by 与 rose to 一字之差含义完全不同：by 是“增加了多少”，to 是“增加到多少”，写错=数据错。")

    U.example(p, "动词句改名词句专练",
              "把下列动词句改写为名词句（用 there be 或 saw/experienced）：\n"
              "1) Unemployment fell steadily from 2010 to 2015.\n"
              "2) The price of oil rose dramatically in 2008.\n"
              "3) Tourist numbers increased gradually over the decade.",
              answer="1) There was a steady fall in unemployment from 2010 to 2015.\n"
                     "2) The price of oil saw a dramatic rise in 2008. / There was a dramatic rise…\n"
                     "3) Tourist numbers experienced a gradual increase over the decade.",
              tip="副词变形容词（steadily→steady），动词变名词（fell→fall），加 there was / saw / experienced。")

    U.example(p, "数据描述综合句",
              "数据：某产品销量 2015 年 100 万件，2020 年 300 万件。"
              "请分别用“变化量 by”“终值 to”“倍数”三种方式各写一句。",
              answer="By: Sales rose by two million units between 2015 and 2020.\n"
                     "To: Sales climbed to three million units by 2020.\n"
                     "Times: Sales tripled over the five-year period, reaching three million units.",
              tip="by=增加量(2 million)；to=终值(3 million)；倍数=tripled。三种说法轮换，句型更丰富。")

    # PART 05 词汇与句型
    U.section(p, 5, "Task 1 词汇与句型库", "Vocabulary & Patterns Bank")
    U.vocab(p, "改写题目动词替换", [
        ("show → illustrate", "展示、说明"),
        ("show → depict / portray", "描绘"),
        ("show → present / give information about", "呈现、提供信息"),
        ("compare → make a comparison between", "比较"),
        ("the number of → the figures for", "……的数量/数据"),
        ("change → variation / fluctuation", "变化/波动"),
        ("from X to Y → between X and Y", "时间范围"),
        ("over → throughout / across the period", "在整个时期"),
        ("measured in → expressed in", "以……为单位"),
    ])

    U.vocab(p, "趋势动词速查表", [
        ("rise / increase / climb", "上升（中性）"),
        ("surge / soar / rocket", "急剧上升"),
        ("fall / decrease / decline", "下降（中性）"),
        ("plunge / plummet / slump", "急剧下降"),
        ("remain stable / level off", "保持平稳/趋稳"),
        ("fluctuate / oscillate", "波动"),
        ("peak at / reach a peak", "达到峰值"),
        ("bottom out / hit a low", "触底"),
        ("stand at / stood at", "处于（某值）"),
    ])

    U.vocab(p, "幅度与比较词速查表", [
        ("slightly / marginally", "略微"),
        ("gradually / steadily", "逐渐/稳定地"),
        ("significantly / substantially", "显著地"),
        ("dramatically / sharply", "急剧地"),
        ("approximately / roughly", "大约"),
        ("twice / three times as much as", "……的两/三倍"),
        ("compared with / in contrast to", "与……相比"),
        ("whereas / while", "然而（对比）"),
        ("by far the highest", "遥遥领先最高"),
    ])

    U.two_col(p, "动词句 vs 名词句对照", "动词句（Verb-based）", [
        ("Sales rose sharply.", "主语+趋势动词+副词"),
        ("Prices fell gradually.", "副词表幅度/速度"),
        ("Numbers increased to 500.", "to 接终值"),
        ("It peaked in 2010.", "动词 peak"),
        ("Figures doubled.", "倍数动词"),
        ("Demand fluctuated.", "波动动词"),
        ("优点：简洁直接", "适合主线描述"),
    ], "名词句（Noun-based）", [
        ("There was a sharp rise in sales.", "there be+形容词+名词"),
        ("There was a gradual fall in prices.", "形容词表幅度"),
        ("Numbers saw a rise to 500.", "saw+a+名词"),
        ("2010 saw a peak.", "时间作主语"),
        ("There was a twofold increase.", "倍数名词"),
        ("Demand experienced fluctuations.", "experienced+名词"),
        ("优点：句型多样", "提升 GRA 分"),
    ])

    U.two_col(p, "by vs to · 倍数表达对照", "rose BY（变化量）", [
        ("rose by 20%", "增加了 20%（增量）"),
        ("an increase of 50 units", "增加了 50（增量）"),
        ("fell by half", "下降了一半"),
        ("a drop of 30 million", "减少了 3000 万"),
        ("grew by a factor of 3", "增长为原来 3 倍"),
        ("用于：强调变化幅度", "by + 增减量"),
    ], "rose TO（终点值）", [
        ("rose to 20%", "上升到 20%（终值）"),
        ("reached 50 units", "达到 50"),
        ("fell to half its level", "降到原来的一半"),
        ("dropped to 30 million", "降到 3000 万"),
        ("tripled / doubled", "翻三倍/两倍"),
        ("用于：强调最终数值", "to + 终值"),
    ])

    # PART 06 方法与范例
    U.section(p, 6, "写作方法与高分范例", "Method & Model Answers")
    U.steps(p, "Task 1 动态图写作六步法", [
        ("第一步 读图 1 分钟", "看清图表类型、坐标轴、单位、时间范围"),
        ("第二步 找 Overview", "确定 1-2 个总体趋势/极值/对比，标在草稿"),
        ("第三步 数据分组", "把相似趋势归 Detail A，对比趋势归 Detail B"),
        ("第四步 写改写句", "改写题目作 P1，换词换句式"),
        ("第五步 写两段细节", "选关键数据点，趋势词+数字+比较"),
        ("第六步 检查", "时态统一、数据准确、字数≥150"),
    ])

    U.steps(p, "20 分钟时间分配", [
        ("0-2 分钟", "读图 + 圈出 Overview 要点"),
        ("2-3 分钟", "草稿分组（哪些进 Detail A/B）"),
        ("3-6 分钟", "写 P1 Paraphrase + P2 Overview"),
        ("6-16 分钟", "写 P3 Detail A + P4 Detail B"),
        ("16-19 分钟", "补充比较句、替换重复词"),
        ("19-20 分钟", "检查时态/拼写/字数"),
    ])

    U.model_answer(p, "折线图高分全文范文 + 批注",
                   "The line graph shows the number of visitors (in millions) to three types of "
                   "attractions — museums, theme parks and historic sites — in one country from "
                   "2000 to 2020.",
                   "The line graph illustrates how many people, in millions, visited museums, theme "
                   "parks and historic sites in a particular country between 2000 and 2020.\n\n"
                   "Overall, visitor numbers rose for all three attractions over the two decades, "
                   "with theme parks attracting by far the most visitors by the end of the period, "
                   "while historic sites remained the least popular throughout.\n\n"
                   "Theme parks began the period at around 5 million visitors and climbed steadily, "
                   "overtaking museums in 2010 before reaching a peak of 18 million in 2020. Museums, "
                   "starting slightly higher at 7 million, grew more modestly to 12 million.",
                   ["P1 改写题目：show→illustrate，换句式",
                    "Overview 用 Overall 开头，只写总趋势+极值",
                    "by far the most / the least 做整体比较",
                    "Detail 选起点、超越点、峰值等关键点",
                    "climbed/grew 替换 increased，避免重复(LR)",
                    "始终用过去时，时态统一(GRA)"])

    U.model_answer(p, "柱状图高分全文范文 + 批注",
                   "The bar chart shows the average daily time (in hours) spent on three "
                   "activities — work, leisure and sleep — by people in four age groups.",
                   "The bar chart compares the average number of hours per day that four age "
                   "groups devoted to work, leisure and sleep.\n\n"
                   "Overall, time spent working rose with age until middle age and then fell, "
                   "whereas leisure time was greatest among the youngest and oldest groups; "
                   "sleep declined steadily as people grew older.\n\n"
                   "The youngest group enjoyed the most leisure, at roughly six hours a day, far "
                   "more than the two and a half hours recorded for the middle-aged. Conversely, "
                   "working hours peaked among the middle-aged before dropping sharply for the "
                   "oldest group.",
                   ["P1 用 compare 改写，符合静态图特征",
                    "Overview 概括三活动随年龄的总体规律",
                    "whereas / Conversely 做组间对比(CC)",
                    "roughly / far more than 约数与比较",
                    "peaked / dropping sharply 趋势词到位(LR)",
                    "无具体到小数的堆砌，选关键对比点"])

    U.compare(p, "低分 vs 高分：Detail 段写法", "✗ 低分（像报数，约 5.5）", [
        ("In 2000 it was 5.", "只有数字无趋势"),
        ("In 2005 it was 9.", "逐点罗列"),
        ("In 2010 it was 12.", "无比较"),
        ("In 2015 it was 15.", "句式完全相同"),
        ("用词 it was 重复", "LR 单薄"),
    ], "✓ 高分（趋势+数据+比较，约 7）", [
        ("climbed steadily from 5", "趋势动词起手"),
        ("overtaking museums in 2010", "点出超越/转折"),
        ("reaching a peak of 18 million", "突出峰值"),
        ("by far the most popular", "做整体比较"),
        ("climbed/grew/reached 轮换", "LR 多样"),
    ])

    U.compare(p, "低分 vs 高分：Overview 写法", "✗ 低分 Overview", [
        ("In 1990 coffee was 200.", "写了具体数字"),
        ("Coffee went up.", "只说一条线"),
        ("（无对比、无极值）", "信息不全"),
        ("（漏写茶的趋势）", "TR 不完整"),
        ("放在结尾被忽略", "位置不佳"),
    ], "✓ 高分 Overview", [
        ("Overall, the two followed opposite trends", "总体相反走势"),
        ("coffee rose while tea declined", "两条线都覆盖"),
        ("点出最高/最低或对比", "极值清晰"),
        ("不含任何具体数字", "符合 Overview 要求"),
        ("放第 2 段、Overall 开头", "位置最稳"),
    ])

    # PART 07 课堂练习
    U.section(p, 7, "课堂练习", "In-Class Practice")
    U.drill(p, "练习一：写 Paraphrase", "为下列题目各写一句改写句（换词换句式，禁照抄）。", [
        "The bar chart shows the percentage of households with internet access in five countries.",
        "The line graph shows changes in average temperature in two cities over 12 months.",
        "The chart below gives information about the number of cars sold in three regions.",
        "The graph shows electricity production from four sources between 1990 and 2020.",
        "The bar chart compares the spending on leisure activities by different age groups.",
    ])

    U.drill(p, "练习二：写 Overview", "为下列图表信息各写一句 Overview（只写总体，不写数字）。", [
        "三条线全部上升，A 始终最高，C 始终最低。",
        "出口先升后降，2010 年达到峰值。",
        "四个城市中，城市 X 用水量远高于其余三市。",
        "男性在两项活动参与率高，女性在三项活动参与率高，总体相近。",
        "某指标 20 年间基本保持平稳，只有小幅波动。",
    ])

    U.drill(p, "练习三：趋势句改写", "用趋势词+幅度词改写下列“报数”句，并各写一个名词句版本。", [
        "In 1990 sales were 100. In 2000 sales were 250.",
        "The figure was 500 in 2005 and 200 in 2015.",
        "It was 30% in 2010 and 32% in 2020.",
        "Production was 80 in 2000, 80 in 2010, 80 in 2020.",
        "The number went up and down between 40 and 60 over the years.",
    ])

    U.drill(p, "练习四：完整 Task 1", "任选一道折线/柱状图真题，20 分钟内完成四段式全文。", [
        "确保四段齐全：Paraphrase / Overview / Detail A / Detail B",
        "Overview 不写具体数字，只写总体趋势与极值/对比",
        "至少使用 3 个不同趋势词 + 2 个幅度词",
        "至少写 1 个名词句、1 个比较句",
        "写完检查：时态统一、数据准确、字数≥150",
    ])

    # PART 08 避坑指南
    U.section(p, 8, "避坑指南", "Pitfalls to Avoid")
    U.pain_point(p, "Task 1 动态图高频失分", [
        ("只写数字", "In 1990 it was 200… 逐点报数，无趋势"),
        ("漏/错 Overview", "没写或只写一条线，没有比较/极值"),
        ("数据全写", "每个点都描述，不会选重点"),
        ("时态错误", "过去图表用现在时"),
        ("照抄题目", "P1 原句照搬，TA/LR 双扣"),
    ], [
        ("数字配趋势", "rose sharply from 200 to 480"),
        ("Overview 找总规律", "总趋势+最高/最低或对比"),
        ("选择性描述", "只写极值与转折点"),
        ("时态对齐图", "过去图→全文过去时"),
        ("改写题目", "换词换句式作 P1"),
    ])

    U.content(p, "常见错误清单（数据与语言）", [
        ("by/to 混用", "rose by 20% 与 rose to 20% 含义不同"),
        ("幅度词不当", "缓慢小幅却用 soar/plummet"),
        ("单复数", "data 复数；the number of + 复数 + is"),
        ("介词搭配", "an increase IN sales（不是 of）/ rise TO"),
        ("主观评价", "Task 1 不写 good/bad、不分析原因"),
        ("单位遗漏", "忘写 million/percent/litres 等单位"),
    ], note="“rose by 20%”和“rose to 20%”一字之差就是数据错误——这是深圳考生最容易忽视的硬伤。")

    U.content(p, "提升 Task 1 分数的额外技巧", [
        ("Overview 前置", "永远放第 2 段，用 Overall 开头，最稳"),
        ("句型轮换", "动词句/名词句/比较句交替，提 GRA"),
        ("精简比较", "用 whereas/while 一句话比较两组"),
        ("约数表达", "看不清精确值用 approximately/just over"),
        ("控制字数", "160-180 词足够，别为凑字数报全部数据"),
        ("结尾不评论", "Task 1 不需要结论段，写完 Detail B 即可"),
    ])

    U.tip_card(p, "Task 1 动态图四张速记卡", [
        ("结构卡", "改写—Overview—Detail A—Detail B，四段缺一不可"),
        ("Overview 卡", "只写总趋势+极值/对比，绝不出现具体数字"),
        ("趋势卡", "上升/下降/平稳/波动各备词，配幅度词"),
        ("时态卡", "过去图过去时；by/to 别混；单位别漏"),
    ])

    U.tip_card(p, "句型升级四张行动卡", [
        ("动名互换卡", "每句趋势写两版：X rose ↔ there was a rise in X"),
        ("比较句卡", "whereas / while / compared with 串联两组数据"),
        ("约数卡", "approximately / just over / nearly 处理读不准的值"),
        ("替换卡", "increase 用多了换 rise/climb/grow/surge"),
    ])

    U.checklist(p, "本课自检清单", [
        "我能用四段式框架组织一篇动态图作文",
        "我能写出不含数字、只写总体趋势的 Overview",
        "我掌握上升/下降/平稳/波动四类趋势词",
        "我能给趋势词配上合适的幅度词与速度词",
        "我能把动词句改写成名词句",
        "我能正确处理时态、by/to 与单位",
        "我能在 20 分钟内完成一篇 Task 1",
    ])

    U.summary(p, 2, [
        "四段式：Paraphrase → Overview → Detail A → Detail B",
        "Overview 是评分重点：必写，且只写总体趋势，不含数字",
        "趋势词 + 幅度词 + 数据 = 完整描述句（rose sharply from X to Y）",
        "动词句↔名词句互换提升 GRA；时态对齐图表时间轴",
    ], takeaway="先写 Overview 再写细节；用趋势词替代报数，用名词句打破单调。")

    U.homework(p, 2, [
        "找 3 道折线图真题，每道只练 Overview 段（2-3 句），反复修改",
        "背趋势词汇表：上升/下降/平稳/波动各 5 个，配套幅度词",
        "完成 1 篇完整折线图 Task 1（20 分钟计时），请老师批改",
        "把一篇“报数”式范文改写为趋势描述，并加 2 个名词句",
    ], est_time="80 分钟")

    U.preview(p, 3, "Task 1 饼图表格流程图地图", [
        "静态图 vs 动态图的不同描述策略",
        "比较句型：account for / the largest share",
        "流程图：被动语态 + 顺序词 first/then/finally",
        "地图题：变化动词 demolished/constructed + 方位",
    ])


# ════════════════════════════════════════════════════════════════
#  L03 Task 1 饼图 / 表格 / 流程图 / 地图
# ════════════════════════════════════════════════════════════════
def build_l03(p):
    U.cover(p, "写作", 3, "Task 1 饼图表格流程图地图",
            "Pie Charts, Tables, Process & Maps", total=10)

    U.agenda(p, [
        "静态图 vs 动态图的描述思路",
        "饼图与表格的比较句型",
        "流程图：被动语态 + 顺序词",
        "地图题：变化动词 + 方位描述",
        "各类图表的 Overview 写法",
        "词汇与句型库",
        "课堂练习：四类图表实战",
        "避坑指南与课后作业",
    ])

    U.review(p, [
        "动态图四段式：Paraphrase / Overview / Detail A / Detail B",
        "Overview 是评分重点，必写且只写总体趋势，不含数字",
        "趋势词 + 幅度词 + 数据 = 完整描述句",
        "动词句↔名词句互换提升 GRA；时态对齐图表时间",
        "本课把框架迁移到饼图/表格/流程图/地图四类题",
    ])

    U.objectives(p, [
        "区分静态图与动态图，选择正确的描述策略",
        "用比较句型（account for / the largest share）描述饼图与表格",
        "用被动语态 + 顺序词完整描述流程图",
        "用变化动词 + 方位词描述地图题的今昔对比",
        "为每一类图表写出合格的 Overview",
    ])

    U.pain_point(p, "导入：非折线图为什么更易丢分", [
        ("流程图用主动", "People collect the bottles…（应被动）"),
        ("饼图只读数字", "逐项报百分比，无比较、无极值"),
        ("地图无方位", "只说建了什么，不说在哪、和谁相邻"),
        ("表格全抄", "把每个格子都写进去，像抄表"),
        ("时态混乱", "流程图用过去时、地图今昔不分"),
    ], [
        ("流程图被动", "The bottles are collected…"),
        ("饼图做比较", "X accounts for the largest share, 远超 Y"),
        ("地图给方位", "in the north / adjacent to / opposite"),
        ("表格选重点", "只写最高/最低/最大差异"),
        ("时态对题", "流程图现在时；地图过去用过去时"),
    ])

    # PART 01 静态图 vs 动态图
    U.section(p, 1, "静态图与动态图思路", "Static vs Dynamic Visuals")
    U.concept(p, "先判断图的“类型”", "题型决定句型——动态看趋势，静态看比较，流程看步骤，地图看变化。", [
        ("动态图", "折线/部分柱状：有时间轴→趋势动词 + 过去时"),
        ("静态图", "饼图/表格/无时间柱状：某时点分布→比较句型"),
        ("流程图 process", "工序/自然循环→被动语态 + 顺序词 + 现在时"),
        ("地图 map", "今昔对比→变化动词 + 方位词 + 过去时"),
        ("混合题", "两张饼图比两年→静态比较 + 时间对比"),
        ("第一步永远是", "看清类型与时间轴，再决定用哪套语言"),
    ], note="深圳学生拿到非折线图常套用趋势词——先分类再下笔，用错句型整段失分。")

    U.content(p, "静态图的描述策略", [
        ("找极值", "最大/最小的类别（the largest / the smallest）"),
        ("分层", "把类别分成高/中/低几档来组织段落"),
        ("做比较", "X 是 Y 的两倍 / X 远超 Y / X 与 Z 相近"),
        ("比例语言", "account for / make up / constitute + 百分比"),
        ("时态", "无时间→现在时；标注了年份→过去时"),
        ("Overview", "最大类别 + 最小类别 + 是否差距悬殊"),
    ])

    U.content(p, "饼图描述要点", [
        ("比例词", "proportion / share / percentage / fraction / segment"),
        ("最大份额", "X accounted for the largest share, at 45%"),
        ("最小份额", "Y made up the smallest proportion, at just 5%"),
        ("两饼对比", "Compared with 2010, the share of X rose by…"),
        ("约数", "around a third / nearly half / just over a quarter"),
        ("Overview", "占比最高与最低的类别，及两年间最大变化"),
    ], note="饼图最忌逐项报百分比——要分组、比较、突出最大与最小，而不是把每块都念一遍。")

    U.content(p, "表格描述要点", [
        ("不抄全表", "只写最高、最低、最大差异，绝不逐格描述"),
        ("选维度", "按行比较还是按列比较，挑信息量大的方向"),
        ("找极值", "全表最大值/最小值在哪一行哪一列"),
        ("做比较", "用 the highest / the lowest / compared with"),
        ("分组", "把相近的数据归为一类一起说"),
        ("Overview", "整张表最突出的规律（哪个最高/最低/趋势）"),
    ])

    U.example(p, "饼图描述范文（双饼对比）",
              "两个饼图：某国 2000 年与 2020 年家庭支出构成。"
              "2000：食品 40%、住房 25%、其他 35%；2020：食品 25%、住房 40%、其他 35%。",
              answer="Overview: Overall, the most notable change was that housing replaced food as "
                     "the largest item of household expenditure between 2000 and 2020.\n"
                     "Detail: In 2000, food accounted for the largest share at 40%, but by 2020 this "
                     "had fallen to a quarter, while spending on housing rose from 25% to 40%.",
              tip="双饼对比：Overview 抓“最大类别发生互换”；Detail 用 account for/rise from…to 做比较，不逐项念。")

    U.example(p, "表格描述范文（选重点）",
              "表格：四国（A/B/C/D）三种交通方式（公交/私家车/自行车）的通勤占比（%）。"
              "A 私家车最高(70%)；D 自行车最高(45%)；公交各国相近(约 30%)。",
              answer="Overview: Overall, private cars dominated commuting in Country A, whereas "
                     "cycling was most popular in Country D; bus use was broadly similar across "
                     "all four nations.\n"
                     "Detail: At 70%, car use in Country A was the highest of any mode in any country, "
                     "while cycling accounted for nearly half of all commutes in Country D.",
              tip="表格不抄全：Overview 点出各国最突出的方式 + 一个相近项；Detail 只挑全表最高与最低对比。")

    # PART 02 比较句型
    U.section(p, 2, "比较与比例句型", "Comparison & Proportion")
    U.concept(p, "静态图的灵魂是“比较”", "没有趋势可写，就靠比较句型把数据组织起来。", [
        ("最高级", "the largest / highest / most significant"),
        ("最低级", "the smallest / lowest / least common"),
        ("倍数比较", "twice / three times as high as"),
        ("差距比较", "considerably higher than / far exceeded"),
        ("相近比较", "roughly equal to / similar to / comparable with"),
        ("比例表达", "account for / make up / represent + %"),
    ], note="静态图若只罗列数字而不比较，TR 与 CC 都会扣分——比较句型是静态图的得分骨架。")

    U.content(p, "比例与占比句型", [
        ("account for", "X accounted for 30% of the total"),
        ("make up / constitute", "X made up nearly half of all cases"),
        ("represent", "X represented the largest category"),
        ("the proportion of", "The proportion of X stood at 25%"),
        ("a + 分数", "a quarter / a third / two thirds of…"),
        ("约数修饰", "just over / just under / approximately / nearly"),
    ])

    U.content(p, "高低与差距句型", [
        ("最高/最低", "X recorded the highest/lowest figure"),
        ("远高于", "X was considerably/significantly higher than Y"),
        ("倍数", "X was twice as large as Y / three times that of Y"),
        ("超过", "X exceeded Y by 20 percentage points"),
        ("差距", "There was a marked gap between X and Y"),
        ("接近", "X was roughly equal to / on a par with Y"),
    ], note="percentage point（百分点）≠ percent（百分比）：从 20% 到 30% 是“上升 10 个百分点”，不是上升 10%。")

    U.content(p, "横向组织段落的逻辑", [
        ("由高到低", "先写最大类别，再依次往下"),
        ("分组并列", "把相近的几项合并描述，省字又清晰"),
        ("对比结构", "whereas / in contrast / on the other hand"),
        ("先总后分", "段首给本段的比较结论，再列数据支撑"),
        ("避免重复", "account for / make up / represent 轮换"),
        ("控制信息", "一段聚焦一个比较维度，不要全塞"),
    ])

    U.example(p, "比较句型综合改写",
              "把下列罗列句改写为带比较的高分句：\n"
              "City A: 70%. City B: 35%. City C: 34%. City D: 10%.（某指标占比）",
              answer="At 70%, City A recorded by far the highest figure — double that of City B "
                     "and City C, which were broadly similar at around 35%. City D, by contrast, "
                     "accounted for just 10%, the lowest of the four.",
              tip="比较三招：by far the highest（极值）+ double that of（倍数）+ by contrast（对比最低），不逐项念。")

    U.example(p, "比例语言专练",
              "数据：某调查中 50% 选 A，25% 选 B，15% 选 C，10% 选 D。"
              "用 account for / make up / a 分数 等不同表达各写一句。",
              answer="A accounted for half of all respondents. B made up a quarter of the sample. "
                     "C and D together represented just one in four, with C slightly more common "
                     "than D.",
              tip="比例表达轮换：account for / make up / represent + half / a quarter / one in four，避免重复 percent。")

    # PART 03 流程图
    U.section(p, 3, "流程图描述", "Describing Processes")
    U.concept(p, "流程图的两大语言支柱", "被动语态写工序，顺序词串步骤——这是流程图的标配。", [
        ("被动语态", "工业流程多用被动：The material is heated…"),
        ("顺序词", "First / Then / Next / Subsequently / Finally"),
        ("现在时", "通用流程用一般现在时（自然循环也是）"),
        ("目的从句", "…in order to remove impurities"),
        ("起止说明", "The process begins with… and ends with…"),
        ("Overview", "总步骤数 + 起点 + 终点，不写细节"),
    ], note="深圳学生流程图最常见错误：用主动语态 People do…——工业流程的主语通常省略，必须用被动。")

    U.content(p, "流程图顺序连接词", [
        ("开始", "First / Initially / To begin with / At the first stage"),
        ("承接", "Then / Next / After that / Subsequently / Following this"),
        ("同时", "Meanwhile / At the same time / Simultaneously"),
        ("结果", "As a result / This results in / leading to"),
        ("结束", "Finally / Lastly / In the final stage / Ultimately"),
        ("循环", "The cycle then repeats / returns to the beginning"),
    ])

    U.content(p, "流程图被动语态与句型", [
        ("基本被动", "The bottles are collected and sorted"),
        ("被动+by", "The waste is processed by machines"),
        ("被动+方式", "The mixture is heated to a high temperature"),
        ("目的", "…so that impurities can be removed"),
        ("先后", "Once X has been done, Y is then carried out"),
        ("时态", "通用流程一律现在时，不用过去时"),
    ], note="自然循环（如水循环、生命周期）也用现在时被动/主动皆可，但工业流程几乎全用被动。")

    U.content(p, "流程图 Overview 写法", [
        ("总步骤数", "The process consists of X main stages"),
        ("起点", "beginning with the collection of raw materials"),
        ("终点", "and culminating in the distribution of products"),
        ("线性 vs 循环", "判断是直线流程还是循环流程"),
        ("不写细节", "Overview 只给框架，细节留给主体段"),
        ("句型", "Overall, the process involves X stages, from… to…"),
    ])

    U.example(p, "流程图范文（工业流程）",
              "流程图：玻璃瓶回收流程。Collection → Sorting by colour → Cleaning → "
              "Crushing → Melting → Moulding → Quality check → Distribution（8 步）。",
              answer="Intro: The diagram illustrates the process by which glass bottles are "
                     "recycled, from collection to distribution.\n"
                     "Overview: Overall, the recycling process comprises eight distinct stages, "
                     "beginning with the collection of used bottles and ending with the delivery "
                     "of new glassware.\n"
                     "Body: First, used bottles are collected and sorted by colour. They are then "
                     "cleaned before being crushed into small pieces.",
              tip="流程图三件套：Intro 改写题目；Overview 给步骤数+起点+终点；Body 用被动+First/then 串联。")

    U.example(p, "流程图范文（自然循环）",
              "流程图：青蛙生命周期。Eggs → Tadpoles → Tadpoles with legs → Froglets → "
              "Adult frog（产卵后循环）。",
              answer="Overview: Overall, the life cycle of the frog consists of four main stages "
                     "and is a continuous cycle, beginning when eggs are laid and returning to "
                     "this point as adults reproduce.\n"
                     "Body: Initially, the female frog lays eggs in water. These eggs subsequently "
                     "hatch into tadpoles, which gradually develop legs over several weeks.",
              tip="循环流程要在 Overview 点明 continuous cycle / returns to the beginning，体现“循环”特征。")

    # PART 04 地图题
    U.section(p, 4, "地图题描述", "Describing Maps")
    U.concept(p, "地图题=描述“变化”", "两张地图看今昔，核心是“什么变了、在哪里”。", [
        ("变化动词", "was built / demolished / converted / extended"),
        ("方位词", "in the north / to the east of / adjacent to"),
        ("今昔时态", "过去年份→过去时；含未来规划→将来时"),
        ("对比结构", "In 1990… However, by 2020 this had been…"),
        ("未变描述", "remained unchanged / stayed in the same place"),
        ("Overview", "总体变化方向（更现代化/工业化/绿化）"),
    ], note="深圳学生地图题常只说“建了商场”，却不说在地图哪个方位——方位词缺失=空间信息不全，TR 扣分。")

    U.content(p, "地图变化动词库", [
        ("新建", "was built / constructed / erected / established"),
        ("拆除", "was demolished / removed / pulled down / cleared"),
        ("改建", "was converted into / transformed into / replaced by"),
        ("扩建", "was extended / expanded / enlarged"),
        ("保留", "remained / was retained / stayed unchanged"),
        ("迁移", "was relocated / moved to"),
    ])

    U.content(p, "地图方位与位置词", [
        ("方向", "in the north/south/east/west / in the centre"),
        ("相对位置", "to the left/right of / above / below"),
        ("相邻", "adjacent to / next to / beside / opposite"),
        ("之间", "between X and Y / surrounded by"),
        ("沿着", "along the river / on the outskirts / on the coast"),
        ("范围", "across the site / throughout the area"),
    ], note="方位词是地图题的“数据”：每描述一处变化，都要交代它在地图的哪个位置，否则读者无法定位。")

    U.content(p, "地图题 Overview 与结构", [
        ("总体判断", "整体变得更现代/工业化/商业化/绿化"),
        ("最大变化", "点出最显著的一两处改变"),
        ("对比时态", "In 1990, there was…; by 2020, it had been replaced by…"),
        ("分区描述", "按地图区域（北/南/中）分段组织"),
        ("过去完成时", "by 2020 …had been built，强调“已完成”"),
        ("未变收尾", "提一句保持不变的地标，体现全面"),
    ])

    U.example(p, "地图题范文（今昔对比）",
              "两张地图：某海滨村庄 1990 与 2020。1990：农田、几座房屋、一条小路；"
              "2020：农田变酒店、小路拓宽为公路、新增码头与停车场。",
              answer="Overview: Overall, the village was transformed from a small rural settlement "
                     "into a developed tourist destination over the three decades.\n"
                     "Detail: The farmland in the north was cleared to make way for a large hotel, "
                     "while the narrow path running through the centre was widened into a main road. "
                     "In addition, a marina was constructed on the coast to the east.",
              tip="地图题：Overview 给总体方向（乡村→旅游区）；Detail 用 was cleared/widened/constructed + 方位词。")

    U.example(p, "地图题方位句专练",
              "描述以下变化（注意方位与时态）：原本位于地图中央的学校被拆除，"
              "在原址东侧新建了一座图书馆，南部的公园保持不变。",
              answer="The school that once stood in the centre of the area was demolished, and a new "
                     "library was constructed to the east of the original site. Meanwhile, the park "
                     "in the south remained unchanged throughout the period.",
              tip="一处变化=变化动词+方位词+时态：was demolished（拆）/ to the east（方位）/ remained unchanged（未变）。")

    # PART 05 词汇与句型
    U.section(p, 5, "静态图与流程地图词汇库", "Vocabulary Bank")
    U.vocab(p, "饼图/表格比较句型", [
        ("account for", "占（比例）：X accounted for 30%"),
        ("make up / constitute", "构成、占"),
        ("the largest/smallest share", "最大/最小份额"),
        ("twice as high as", "是……的两倍"),
        ("considerably higher than", "远高于"),
        ("a marked gap between", "……之间显著差距"),
        ("roughly equal to", "大致相等"),
        ("percentage point", "百分点（≠percent）"),
        ("the proportion of", "……的比例"),
    ])

    U.vocab(p, "流程图被动与顺序词", [
        ("is collected / sorted", "被收集/分类（被动）"),
        ("is heated to", "被加热至"),
        ("First / Initially", "首先"),
        ("Then / Subsequently", "然后/随后"),
        ("Following this", "在此之后"),
        ("in order to / so that", "为了……"),
        ("Finally / Ultimately", "最后"),
        ("The process consists of", "该流程包括"),
        ("the cycle repeats", "循环重复"),
    ])

    U.vocab(p, "地图变化与方位词", [
        ("was built / constructed", "被建造"),
        ("was demolished / cleared", "被拆除/清除"),
        ("was converted into", "被改建为"),
        ("was extended / expanded", "被扩建"),
        ("remained unchanged", "保持不变"),
        ("in the north / centre", "在北部/中央"),
        ("adjacent to / opposite", "与……相邻/相对"),
        ("on the outskirts", "在郊区"),
        ("by 2020 …had been", "到 2020 已经被……"),
    ])

    U.two_col(p, "主动 vs 被动：流程图", "✗ 主动（不地道）", [
        ("People collect the bottles.", "出现人做主语"),
        ("Workers heat the metal.", "强调执行者"),
        ("They clean it then.", "代词指代不清"),
        ("Someone checks quality.", "主语模糊"),
        ("We crush the glass.", "用 we 不当"),
        ("机器 The machine does X.", "重心错位"),
    ], "✓ 被动（地道）", [
        ("The bottles are collected.", "省略执行者"),
        ("The metal is heated.", "突出工序"),
        ("It is then cleaned.", "is then 顺序清晰"),
        ("Quality is checked.", "主语=工序对象"),
        ("The glass is crushed.", "被动标准句"),
        ("X is carried out by…", "需提执行者时用 by"),
    ])

    U.two_col(p, "静态图 vs 动态图语言", "动态图（趋势）", [
        ("rose / fell / fluctuated", "趋势动词"),
        ("sharply / gradually", "幅度/速度副词"),
        ("from X to Y / by 20%", "变化量"),
        ("peaked / bottomed out", "峰谷"),
        ("过去时为主", "时态"),
        ("Overview=总趋势", "概述重点"),
    ], "静态图（比较）", [
        ("account for / make up", "比例动词"),
        ("the largest / smallest", "极值"),
        ("twice as high as", "倍数比较"),
        ("considerably higher", "差距"),
        ("现在时或过去时", "看有无时间"),
        ("Overview=最大/最小", "概述重点"),
    ])

    # PART 06 方法与范例
    U.section(p, 6, "写作方法与高分范例", "Method & Model Answers")
    U.steps(p, "四类图表通用写作五步法", [
        ("第一步 判类型", "动态/静态/流程/地图？决定用哪套语言"),
        ("第二步 找 Overview", "趋势/极值/步骤框架/总体变化"),
        ("第三步 选重点", "动态选转折，静态选极值，流程选阶段，地图选大变化"),
        ("第四步 改写题目", "P1 换词换句式"),
        ("第五步 写细节+检查", "对应句型 + 时态统一 + 字数≥150"),
    ])

    U.steps(p, "判断图表类型的决策树", [
        ("有时间轴吗", "有→很可能是动态图（趋势词）"),
        ("是工序/循环吗", "是→流程图（被动+顺序词）"),
        ("是两张地图吗", "是→地图题（变化动词+方位）"),
        ("是某时点分布吗", "是→静态图（比较句型）"),
        ("是混合吗", "两张饼比两年→静态比较+时间对比"),
        ("定了类型再", "选 Overview 模板与句型库"),
    ])

    U.model_answer(p, "流程图高分范文 + 批注",
                   "The diagram shows how instant coffee is produced.",
                   "The flow chart illustrates the various stages involved in the production of "
                   "instant coffee.\n\n"
                   "Overall, the process comprises several main steps, beginning with the harvesting "
                   "of coffee beans and ending with the packaging of the final product.\n\n"
                   "To begin with, ripe coffee beans are picked and then dried in the sun. Once "
                   "dried, the beans are roasted at high temperatures before being ground into a "
                   "fine powder. This powder is subsequently mixed with hot water, and the liquid "
                   "is then frozen and broken into granules, which are finally packaged for sale.",
                   ["P1 用 illustrate + the various stages 改写",
                    "Overview 给步骤框架+起点+终点，不写细节",
                    "全程被动：are picked / are roasted / is mixed",
                    "顺序词 To begin with / Once / subsequently / finally",
                    "Once dried 分词结构，句型升级(GRA)",
                    "现在时贯穿，时态统一"])

    U.model_answer(p, "地图题高分范文 + 批注",
                   "The maps show a town centre in 1980 and the same area today.",
                   "The two maps compare the layout of a town centre in 1980 with its current "
                   "appearance.\n\n"
                   "Overall, the town centre has become considerably more commercial and "
                   "pedestrian-friendly, with several residential buildings giving way to shops "
                   "and a new shopping centre.\n\n"
                   "The most striking change is in the centre, where a row of houses was demolished "
                   "to make way for a large shopping mall. To the north, the small car park was "
                   "extended, whereas the church on the eastern edge of the town remained unchanged "
                   "throughout the period.",
                   ["P1 compare … with 改写题目",
                    "Overview 给总体方向（更商业化/步行化）",
                    "was demolished / was extended 变化动词到位",
                    "in the centre / to the north / eastern edge 方位",
                    "remained unchanged 体现全面（提未变项）",
                    "过去时描述变化，whereas 做对比(CC)"])

    U.compare(p, "低分 vs 高分：流程图", "✗ 低分流程图（约 5.5）", [
        ("People collect bottles.", "主动语态"),
        ("Then they clean them.", "代词混乱"),
        ("After that crush.", "句子不完整"),
        ("（无 Overview）", "缺总体框架"),
        ("用过去时 collected", "时态错误"),
    ], "✓ 高分流程图（约 7）", [
        ("Bottles are collected.", "被动语态"),
        ("They are then cleaned.", "is/are then 顺序清晰"),
        ("Subsequently, they are crushed.", "顺序词得当"),
        ("Overview 给步骤数+起止", "框架清晰"),
        ("现在时贯穿", "时态正确"),
    ])

    U.compare(p, "低分 vs 高分：饼图", "✗ 低分饼图（约 5.5）", [
        ("Food is 40%.", "逐项报数"),
        ("Housing is 25%.", "无比较"),
        ("Other is 35%.", "无极值"),
        ("（无 Overview）", "缺概述"),
        ("用词 is 重复", "LR 单薄"),
    ], "✓ 高分饼图（约 7）", [
        ("Food accounted for the largest share", "极值+比例词"),
        ("at 40%, followed by other at 35%", "排序"),
        ("twice the proportion of housing", "倍数比较"),
        ("Overview 给最大/最小类别", "概述到位"),
        ("account for/make up 轮换", "LR 多样"),
    ])

    # PART 07 课堂练习
    U.section(p, 7, "课堂练习", "In-Class Practice")
    U.drill(p, "练习一：判断图表类型", "判断下列图表应使用哪套语言（趋势/比较/被动顺序/变化方位）。", [
        "一张饼图显示某公司各部门预算占比。",
        "一张流程图显示纸张的回收过程。",
        "两张地图显示一座岛屿开发前后的变化。",
        "一张表格显示五国 2020 年的识字率。",
        "一张折线图显示三国 2000-2020 年人口变化。",
    ])

    U.drill(p, "练习二：写比较句", "把下列罗列数据改写为带比较的高分句。", [
        "A=60%, B=30%, C=8%, D=2%（某类别占比）",
        "甲城 500，乙城 480，丙城 120（某指标）",
        "男性 25 小时，女性 12 小时（每周某活动时长）",
        "线上 70%，线下 30%（销售渠道占比）",
        "2010 年 40%，2020 年 60%（某比例两年对比）",
    ])

    U.drill(p, "练习三：流程图被动改写", "把下列主动句改写为被动语态。", [
        "Workers collect the waste every morning.",
        "The machine heats the mixture to 100°C.",
        "People sort the bottles by colour.",
        "They pack the products into boxes.",
        "Someone checks the quality before shipping.",
    ])

    U.drill(p, "练习四：地图变化句", "用变化动词+方位词描述下列变化。", [
        "中央的旧仓库被拆除，原址建了公园。",
        "北部新建了一座桥连接两岸。",
        "东侧的农田被改建为住宅区。",
        "南部的学校扩建了一倍。",
        "西侧的森林保持不变。",
    ])

    # PART 08 避坑指南
    U.section(p, 8, "避坑指南", "Pitfalls to Avoid")
    U.pain_point(p, "四类图表高频失分", [
        ("流程图主动语态", "People do… 不地道"),
        ("饼图逐项报数", "无比较、无极值"),
        ("地图缺方位", "只说变化不说位置"),
        ("表格抄全表", "逐格描述像抄表"),
        ("时态用错", "流程图过去时/地图今昔不分"),
    ], [
        ("被动语态", "is collected / is heated"),
        ("比较+极值", "account for the largest share"),
        ("方位词", "in the north / adjacent to"),
        ("选重点", "只写最高/最低/最大差异"),
        ("时态对题", "流程现在时；地图过去用过去时"),
    ])

    U.content(p, "常见错误清单（句型与时态）", [
        ("percent vs point", "上升 10 个百分点 ≠ 上升 10%"),
        ("流程主动", "People collect → are collected"),
        ("地图无完成时", "by 2020 had been built 强调已完成"),
        ("饼图无比较", "逐项 is X% → account for + 比较"),
        ("方位缺失", "每处变化都要交代地图位置"),
        ("混合题漏时间", "双饼对比要同时比类别与年份"),
    ], note="双饼/双表对比题最易漏掉“年份变化”——既要比类别高低，也要比两年间的升降，两个维度都要写。")

    U.content(p, "提升非折线图分数的技巧", [
        ("先分类再下笔", "30 秒判断类型，避免用错句型"),
        ("Overview 模板化", "每类各背一个 Overview 句型"),
        ("被动语态库", "流程图准备 10 个被动句型"),
        ("方位词库", "地图题准备 10 个方位表达"),
        ("比较句库", "静态图准备 8 个比较句型"),
        ("控制信息量", "选重点，不求全，避免抄表/念百分比"),
    ])

    U.tip_card(p, "四类图表速记卡", [
        ("饼图/表格卡", "比较句型 + 极值 + 不逐项报数"),
        ("流程图卡", "被动语态 + 顺序词 + 现在时"),
        ("地图卡", "变化动词 + 方位词 + 今昔时态"),
        ("通用卡", "先分类→找 Overview→选重点→改写题目"),
    ])

    U.tip_card(p, "Overview 模板四张卡", [
        ("静态图", "Overall, X 占比最高 whereas Y 最低，差距明显"),
        ("流程图", "Overall, the process comprises X stages, from…to…"),
        ("地图", "Overall, the area became more 现代化/商业化"),
        ("混合题", "Overall, 最大类别发生互换 + 总体升降方向"),
    ])

    U.checklist(p, "本课自检清单", [
        "我能区分静态图、动态图、流程图、地图并选对句型",
        "我能用 account for / the largest share 描述饼图表格",
        "我能用被动语态 + 顺序词描述流程图",
        "我能用变化动词 + 方位词描述地图题",
        "我能为每类图表写出合格的 Overview",
        "我清楚 percent 与 percentage point 的区别",
        "我能在 20 分钟内完成任意类型 Task 1",
    ])

    U.summary(p, 3, [
        "先分类：静态看比较、流程看被动顺序、地图看变化方位",
        "饼图表格：account for / the largest share + 选重点不抄全",
        "流程图：被动语态 + first/then/finally + 现在时",
        "地图题：变化动词（demolished/constructed）+ 方位词 + 今昔时态",
    ], takeaway="所有 Task 1 都必须有 Overview——这是与 6 分的核心差距，四类图表概莫能外。")

    U.homework(p, 3, [
        "每类图表各练 1 个 Overview 段（饼图/表格/流程图/地图），不计时",
        "整理流程图被动句型 10 个、地图方位词 15 个",
        "完成 1 篇饼图 + 1 篇流程图的完整 Task 1（各 20 分钟）",
        "把一段主动语态的流程描述改写为全被动版本",
    ], est_time="80 分钟")

    U.preview(p, 4, "Task 2 议论文类型全解", [
        "5 种题型识别：Opinion/Discussion/Problem-Solution/Adv-Disadv/Mixed",
        "审题 3 步法：找话题→找角度→明确立场要求",
        "各题型的段落结构与立场策略",
        "thesis statement：引言末句必写",
    ])


# ════════════════════════════════════════════════════════════════
#  L04 Task 2 议论文类型全解
# ════════════════════════════════════════════════════════════════
def build_l04(p):
    U.cover(p, "写作", 4, "Task 2 议论文类型全解",
            "Mastering the Five Essay Types", total=10)

    U.agenda(p, [
        "Task 2 五大题型识别",
        "审题 3 步法：话题/角度/立场",
        "各题型的段落结构规划",
        "立场策略与 thesis statement",
        "引言段的三段式写法",
        "词汇与句型库",
        "课堂练习：审题与立场实战",
        "避坑指南与课后作业",
    ])

    U.review(p, [
        "Task 1 四类图表：静态比较 / 流程被动 / 地图变化方位",
        "所有 Task 1 都必须有 Overview，这是过 6 分的底线",
        "从本课起进入 Task 2：占总分 2/3，先写、写够 250 词",
        "Task 2 核心是“有论证的观点”，不是罗列数据",
        "本课目标：审题不失分，识别 5 种题型并规划结构",
    ])

    U.objectives(p, [
        "准确识别 5 种 Task 2 题型并说出各自要求",
        "用审题 3 步法快速判断话题、角度与立场要求",
        "为每种题型规划正确的段落结构",
        "写出一句清晰、可贯穿全文的 thesis statement",
        "杜绝因审题失误导致的 TR 失分",
    ])

    U.pain_point(p, "导入：审题错=最贵的失分", [
        ("题型看错", "Discuss both views 写成纯 Opinion"),
        ("漏答一半", "只 discuss 一方，另一方一笔带过"),
        ("立场缺失", "通篇分析却不表态"),
        ("立场骑墙", "前段同意后段反对，结论又模糊"),
        ("跑题", "答非所问，TR 封顶 5 分"),
    ], [
        ("圈指令词", "discuss/agree/causes/outweigh 决定结构"),
        ("逐项回应", "题目每部分都要单独成段回应"),
        ("立场前置", "引言末句给 thesis"),
        ("立场一致", "全文一个立场，结论重申"),
        ("紧扣题目", "每段回链题目关键词"),
    ])

    # PART 01 五大题型
    U.section(p, 1, "Task 2 五大题型", "The Five Essay Types")
    U.concept(p, "先认题，再动笔", "题型决定结构与立场——认错题型，结构全错，TR 必扣。", [
        ("Opinion 观点题", "Do you agree or disagree? / To what extent…"),
        ("Discussion 讨论题", "Discuss both views and give your own opinion"),
        ("Problem-Solution 问题解决", "What are the causes…? What solutions…?"),
        ("Adv-Disadv 利弊题", "advantages and disadvantages? / positive or negative?"),
        ("Mixed 混合题", "Do the advantages outweigh the disadvantages?"),
        ("辨认靠指令", "看题目指令句，别看话题——话题相同题型可不同"),
    ], note="深圳学生最常见误判：把 Discuss both views 当成 agree/disagree 来写，结果只写一方，TR 严重扣分。")

    U.content(p, "题型一：Opinion 观点题", [
        ("标志", "agree or disagree / To what extent do you agree"),
        ("要求", "明确表明同意/不同意，并论证"),
        ("结构", "引言(立场)→支持段1→支持段2→让步反驳→结论"),
        ("立场", "完全同意或完全不同意更易拿高分"),
        ("to what extent", "可部分同意，但要说清同意到什么程度"),
        ("禁忌", "both sides have good points 式的骑墙"),
    ])

    U.content(p, "题型二：Discussion 讨论题", [
        ("标志", "Discuss both views and give your own opinion"),
        ("要求", "公正讨论两种观点 + 给出个人立场"),
        ("结构", "引言→观点A段→观点B段→个人立场→结论"),
        ("两方平衡", "A、B 两段篇幅相当，不能畸轻畸重"),
        ("个人立场", "必须给！可在第三段或结论段表明"),
        ("禁忌", "只讨论两方不给立场 = TR 不完整"),
    ], note="Discussion 题的 give your own opinion 不是可选项——漏掉个人立场，TR 直接扣一档。")

    U.content(p, "题型三/四：问题解决 & 利弊", [
        ("问题解决标志", "causes / problems + solutions / measures"),
        ("问题解决结构", "引言→原因段→解决方案段→结论（原因方案对应）"),
        ("利弊标志A", "advantages and disadvantages → 各写一段"),
        ("利弊标志B", "positive or negative development → 需表态"),
        ("展开原则", "深入展开 2 点，胜过浅显罗列 5 点"),
        ("对应要求", "原因↔方案、利↔弊要一一呼应"),
    ])

    U.content(p, "题型五：Mixed 混合题", [
        ("典型", "Do the advantages outweigh the disadvantages?"),
        ("本质", "利弊题 + 必须表明哪方更重（outweigh）"),
        ("结构", "引言(表态利>弊或弊>利)→利段→弊段→结论重申"),
        ("立场要求", "引言就要明确总体立场，不能模糊"),
        ("其他混合", "Why + solutions / 双问题题也算混合"),
        ("关键", "看清题目有几个任务，逐个回应"),
    ], note="outweigh 题最易丢分点：写了利也写了弊，却忘了表态“哪方更重”——必须在引言和结论各说一次。")

    U.example(p, "审题实战：识别题型",
              "题目1: Some people think governments should spend money on public transport, while "
              "others think it is better to build more roads. Discuss both views and give your own "
              "opinion.\n"
              "题目2: More young people are choosing to study abroad. Do the advantages of this "
              "trend outweigh the disadvantages?\n"
              "题目3: Obesity is a major health concern. What are the causes and what measures can "
              "be taken to address it?",
              answer="题目1: Discussion 题→两方+个人立场（引+公交段+修路段+个人立场+结论）。\n"
                     "题目2: Mixed/outweigh 题→表明利>弊或弊>利（引表态+利段+弊段+结论重申）。\n"
                     "题目3: Problem-Solution 题→原因段+方案段对应（引+原因+方案+结论）。",
              tip="审题先圈指令词：discuss both / outweigh / causes & measures——指令词不同，结构完全不同。")

    U.example(p, "同一话题，不同题型",
              "话题都是“在家办公(remote work)”。\n"
              "A: Working from home has more benefits than drawbacks. To what extent do you agree?\n"
              "B: Discuss the advantages and disadvantages of working from home.\n"
              "C: What problems does remote work cause and how can they be solved?",
              answer="A: Opinion 题→明确同意/不同意 + 论证（一边倒更稳）。\n"
                     "B: 利弊题（无 outweigh）→利段+弊段，结论给平衡评价，可不强表态。\n"
                     "C: Problem-Solution 题→问题段+解决方案段对应。",
              tip="话题相同不代表结构相同——务必看指令句，A/B/C 三种写法完全不同。")

    # PART 02 审题三步法
    U.section(p, 2, "审题三步法", "Three-Step Analysis")
    U.concept(p, "审题决定 TR 上限", "30 秒审题，省下后面 5 分钟的返工，更避免跑题。", [
        ("第一步 找话题", "题目在谈什么（education / technology / environment）"),
        ("第二步 找角度", "要你说好坏/原因/方案/同意与否"),
        ("第三步 明立场", "题目要求你表态吗？怎么表态？"),
        ("圈关键词", "话题词、限定词、指令词分别圈出"),
        ("看限定词", "all / some / young people / in cities 缩小范围"),
        ("规划结构", "审题结果直接对应段落规划"),
    ], note="深圳学生常跳过审题直接写——结果写到一半发现跑题或漏答，时间全浪费。30 秒审题最划算。")

    U.content(p, "第一步：锁定话题与范围", [
        ("话题词", "题目的核心名词：education / crime / health"),
        ("限定词", "all students / young people / developing countries"),
        ("范围陷阱", "题目说 children，你却写 all people——偏题"),
        ("正反话题", "ban / encourage / replace 暗含立场方向"),
        ("抽象 vs 具体", "把抽象话题落到具体领域举例"),
        ("勿扩大", "严格扣住题目范围，不要自行扩展话题"),
    ])

    U.content(p, "第二步：判断角度（指令词）", [
        ("agree/disagree", "→ 表明立场并论证（Opinion）"),
        ("discuss both views", "→ 两方+个人立场（Discussion）"),
        ("causes / why", "→ 分析原因"),
        ("solutions / measures", "→ 提出解决方案"),
        ("advantages/disadvantages", "→ 利弊各一段"),
        ("outweigh / positive or negative", "→ 必须表态"),
    ], note="指令词是审题的命门：discuss≠agree，outweigh 必表态——读错指令词=结构全盘皆错。")

    U.content(p, "第三步：确定立场策略", [
        ("Opinion", "完全同意/不同意（更易高分）或部分同意"),
        ("Discussion", "讨论两方后给个人立场，结论重申"),
        ("outweigh", "引言即表态利>弊或弊>利"),
        ("Problem-Solution", "无需个人观点，但要展示分析能力"),
        ("一致性", "全文一个立场，避免前后矛盾"),
        ("可辩护", "选你最有话可说、最好举例的一方"),
    ])

    U.example(p, "审题三步法实操",
              "题目: Some people believe that children should start formal education as early as "
              "possible, while others think they should not start until the age of seven. Discuss "
              "both views and give your own opinion.",
              answer="第一步 话题：儿童开始正规教育的年龄（范围=children，别写成 all people）。\n"
                     "第二步 角度：discuss both views → 讨论“尽早”与“七岁后”两种观点。\n"
                     "第三步 立场：必须给个人观点（如倾向尽早，但需有条件）。\n"
                     "结构：引言→尽早派观点段→晚学派观点段→个人立场段→结论。",
              tip="三步审题输出三件事：话题范围、要写几方、要不要表态——直接对应段落规划。")

    U.example(p, "审题陷阱辨析",
              "题目: To what extent do you think the advantages of online shopping outweigh its "
              "disadvantages for small local businesses?",
              answer="陷阱1：to what extent + outweigh 双重指令→必须表态“多大程度上利大于弊”。\n"
                     "陷阱2：限定词 for small local businesses→必须聚焦“对小本地商家”的利弊，"
                     "不能泛泛谈对消费者的影响。",
              tip="限定词最易被忽略：题目说 for small local businesses，全文就得围绕小商家展开，否则偏题。")

    # PART 03 各题型段落结构
    U.section(p, 3, "各题型段落结构", "Paragraph Structures")
    U.concept(p, "结构是 TR 与 CC 的共同载体", "每种题型有固定的段落骨架，套对骨架，分数就稳。", [
        ("通用骨架", "引言 + 2-3 个主体段 + 结论"),
        ("引言 3 句", "Hook/背景 + Paraphrase + Thesis"),
        ("主体段", "Topic Sentence + 论证 + 例子 + 影响"),
        ("结论 2 句", "重申立场 + 总结，不加新信息"),
        ("段落数", "4-5 段最常见，每段一个中心"),
        ("题型差异", "差异主要在主体段如何安排"),
    ], note="不要背“万能模板段”，要背“结构骨架”——骨架可套所有题，模板段会被判机械、TR 扣分。")

    U.content(p, "Opinion 题段落结构", [
        ("引言", "背景 + paraphrase + 明确立场(thesis)"),
        ("主体1", "支持立场的论点 A（含论证链）"),
        ("主体2", "支持立场的论点 B（含论证链）"),
        ("让步段", "Admittedly… 承认对立观点，再反驳（加分）"),
        ("结论", "重申立场 + 总结论点"),
        ("一边倒", "全文支持一方，比骑墙更易拿高分"),
    ])

    U.content(p, "Discussion 题段落结构", [
        ("引言", "背景 + 预告两方 + 个人立场预告"),
        ("观点A段", "公正呈现一方最强论点（Proponents argue…）"),
        ("观点B段", "公正呈现另一方（Critics contend…）"),
        ("个人立场段", "明确自己倾向哪方及原因（或并入结论）"),
        ("结论", "重申个人立场"),
        ("平衡", "A、B 两段篇幅相当"),
    ])

    U.content(p, "问题解决 & 利弊题结构", [
        ("问题解决-引言", "说明问题严重性 + paraphrase + 预告原因与方案"),
        ("原因段", "Topic Sentence(主因) + 展开 + 相关次因"),
        ("方案段", "对应原因的解决方案 + 如何实施 + 预期效果"),
        ("利弊-利段", "深入展开 1-2 个优点 + 影响"),
        ("利弊-弊段", "深入展开 1-2 个缺点 + 影响"),
        ("结论", "问题解决型展望；outweigh 题重申立场"),
    ], note="问题解决型的铁律：原因与方案一一对应——说了 A 原因，就要提针对 A 的方案，不能答非所问。")

    U.example(p, "结构规划演练（Opinion）",
              "题目: Some people think that the best way to reduce crime is to give longer prison "
              "sentences. To what extent do you agree or disagree?",
              answer="立场：不同意（更长刑期不是最佳方式）。\n"
                     "引言：背景(犯罪治理)+paraphrase+thesis(不同意，教育与就业更有效)。\n"
                     "主体1：长刑期对预防犯罪作用有限（论证+例子）。\n"
                     "主体2：根本方案是教育/就业/社会支持（论证+例子）。\n"
                     "让步：Admittedly 重刑对严重罪行有威慑，但不解决根源。\n"
                     "结论：重申不同意，强调治本之策。",
              tip="先定立场再排结构：每个主体段一个支持你立场的论点，让步段承认对方再反驳。")

    U.example(p, "结构规划演练（Discussion）",
              "题目: Some believe technology has made us less social, while others argue it has "
              "improved our social lives. Discuss both views and give your own opinion.",
              answer="引言：背景(科技与社交)+预告两方+个人立场预告。\n"
                     "观点A段：科技削弱社交（面对面减少、孤独感，论证+例子）。\n"
                     "观点B段：科技改善社交（跨地域联系、弱势群体发声，论证+例子）。\n"
                     "个人立场段：倾向 B，但需理性使用（论证）。\n"
                     "结论：重申个人立场。",
              tip="Discussion 题两方各一段、篇幅相当；个人立场可单独成段或并入结论，但绝不能没有。")

    # PART 04 立场与 thesis
    U.section(p, 4, "立场与 thesis statement", "Stance & Thesis")
    U.concept(p, "thesis 是全文的指挥棒", "引言末句一句话亮明立场，全文围绕它展开。", [
        ("位置", "引言最后一句"),
        ("作用", "告诉考官你的立场，统领后文"),
        ("清晰", "一眼能读出同意/不同意/哪方更重"),
        ("可论证", "选你最有话说、最好举例的立场"),
        ("一致", "全文与结论都呼应 thesis"),
        ("禁模糊", "避免 it depends / hard to say"),
    ], note="深圳学生写 thesis 最大问题是“绕”：开头铺垫三句还不表态——考官在第一印象阶段就读不到你的立场。")

    U.content(p, "各题型的 thesis 写法", [
        ("Opinion 完全同意", "I firmly believe that … is the most effective approach"),
        ("Opinion 部分同意", "While … has merit, I would argue that …"),
        ("Discussion", "This essay will examine both views before arguing that …"),
        ("outweigh", "I am convinced that the benefits far outweigh the drawbacks"),
        ("Problem-Solution", "This essay will explore the main causes and propose solutions"),
        ("通用句架", "I would argue that + 你的立场"),
    ])

    U.content(p, "立场策略：选哪一边", [
        ("一边倒最稳", "Opinion 题完全同意/不同意，论证更集中"),
        ("部分同意有度", "to what extent 可部分同意，但要界定清楚"),
        ("选好举例的一方", "哪方你能想到真实例子，就选哪方"),
        ("避免极端", "立场鲜明但论证留有余地（让步段）"),
        ("Discussion 也要表态", "讨论两方后明确倾向"),
        ("全程一致", "切忌写着写着倒戈"),
    ], note="不要因为“觉得某方更正确”就选——要选“你最能论证、最有例子”的一方，考场上论证质量比立场对错更重要。")

    U.content(p, "立场一致性的自检", [
        ("引言-结论对照", "结论的立场是否与 thesis 完全一致"),
        ("主体段方向", "每个主体段是否都服务于同一立场"),
        ("让步不倒戈", "让步段承认对方后必须拉回自己立场"),
        ("无骑墙句", "删掉 both sides are right / it depends"),
        ("关键词回链", "结论重申时回链 thesis 的关键词"),
        ("通读检查", "读完全文，立场是否一以贯之"),
    ])

    U.example(p, "thesis statement 优劣对比",
              "题目: Should governments invest more in renewable energy? (agree/disagree)",
              answer="✗ 模糊：“There are many opinions about renewable energy. In this essay I will "
                     "discuss them.”（无立场）\n"
                     "✗ 骑墙：“Both renewable and traditional energy have advantages.”（不表态）\n"
                     "✓ 清晰：“I strongly believe that governments must prioritise investment in "
                     "renewable energy, both to combat climate change and to ensure long-term "
                     "energy security.”（立场+两个论证方向）",
              tip="高分 thesis = 明确立场 + 暗示论证方向（climate change / energy security），为主体段埋好线。")

    U.example(p, "为不同题型写 thesis",
              "为下列题目各写一句 thesis：\n"
              "1) Opinion: University should be free. (agree/disagree)\n"
              "2) outweigh: Do advantages of globalisation outweigh disadvantages?\n"
              "3) Discussion: Online vs traditional classes — discuss both + opinion.",
              answer="1) I firmly believe that higher education should be publicly funded to ensure "
                     "equal access for all.\n"
                     "2) On balance, I am convinced that the advantages of globalisation clearly "
                     "outweigh its drawbacks.\n"
                     "3) This essay will discuss both modes before arguing that a blended approach "
                     "is the most effective.",
              tip="三种题型三种 thesis 句架：firmly believe（Opinion）/ on balance…outweigh / examine both…before arguing。")

    # PART 05 词汇与句型
    U.section(p, 5, "审题与立场词汇库", "Vocabulary Bank")
    U.vocab(p, "题型指令词速查", [
        ("agree or disagree", "Opinion：表明立场"),
        ("to what extent", "Opinion：可部分同意"),
        ("discuss both views", "Discussion：两方+立场"),
        ("give your own opinion", "必须表明个人观点"),
        ("causes / reasons", "分析原因"),
        ("solutions / measures", "提出方案"),
        ("advantages/disadvantages", "利弊各一段"),
        ("outweigh", "必须表态哪方更重"),
        ("positive or negative", "需表态利/弊"),
    ])

    U.vocab(p, "引言改写句型", [
        ("… has sparked considerable debate", "……引发广泛争议"),
        ("Over the past few decades, …", "过去几十年……"),
        ("It is often argued that …", "人们常认为……"),
        ("There is growing concern about …", "对……的担忧日益增加"),
        ("Opinions are divided on whether …", "对于是否……众说纷纭"),
        ("The question of whether … remains contentious", "……是否仍有争议"),
        ("This essay will examine …", "本文将探讨……"),
        ("before arguing that …", "并论证……"),
        ("This essay will explore … and propose …", "本文将探讨……并提出……"),
    ])

    U.vocab(p, "立场表达句型", [
        ("I firmly believe that …", "我坚定认为"),
        ("I would argue that …", "我认为（学术）"),
        ("I am convinced that …", "我深信"),
        ("On balance, …", "总体而言"),
        ("While …, I maintain that …", "尽管……我仍坚持"),
        ("I partially agree that …", "我部分赞同"),
        ("In my view, … should …", "在我看来"),
        ("the benefits outweigh the drawbacks", "利大于弊"),
        ("the drawbacks outweigh the benefits", "弊大于利"),
    ])

    U.two_col(p, "Discussion vs Opinion 写法", "Opinion（一边倒）", [
        ("引言明确表态", "I firmly believe…"),
        ("主体全支持一方", "两个支持论点"),
        ("让步段反驳对方", "Admittedly…However"),
        ("结论重申立场", "立场一致"),
        ("禁两方平均用力", "避免骑墙"),
        ("用 I 表态", "可用第一人称"),
    ], "Discussion（两方+立场）", [
        ("引言预告两方", "examine both views"),
        ("A、B 各一段", "公正呈现"),
        ("篇幅平衡", "A≈B"),
        ("单设立场段或并入结论", "必须表态"),
        ("两方都要写够", "不能漏一方"),
        ("Proponents/Critics", "公正措辞"),
    ])

    U.two_col(p, "问题解决 vs 利弊题写法", "问题解决型", [
        ("引言说明问题严重", "poses a threat"),
        ("原因段", "分析主因"),
        ("方案段", "对应解决方案"),
        ("原因↔方案对应", "逻辑闭环"),
        ("结论展望", "改善前景"),
        ("无需个人立场", "重分析能力"),
    ], "利弊/outweigh 题", [
        ("引言（outweigh 需表态）", "benefits outweigh"),
        ("利段", "深入 1-2 优点"),
        ("弊段", "深入 1-2 缺点"),
        ("利↔弊呼应", "对照展开"),
        ("结论重申立场", "outweigh 必表态"),
        ("深入>罗列", "勿列 5 点"),
    ])

    # PART 06 方法与范例
    U.section(p, 6, "写作方法与高分范例", "Method & Model Answers")
    U.steps(p, "Task 2 审题到落笔六步法", [
        ("第一步 读题圈词", "圈话题词、限定词、指令词"),
        ("第二步 定题型", "Opinion/Discussion/Problem/Adv-Disadv/Mixed"),
        ("第三步 定立场", "要不要表态？倾向哪方？"),
        ("第四步 列提纲", "每段 Topic Sentence + 1-2 个支撑点"),
        ("第五步 写引言", "背景+paraphrase+thesis"),
        ("第六步 写主体+结论", "论证链 + 重申立场"),
    ])

    U.steps(p, "5 分钟审题与提纲流程", [
        ("0-1 分钟", "读题，圈指令词，判断题型"),
        ("1-2 分钟", "确定立场（要不要表态/倾向哪方）"),
        ("2-4 分钟", "列出每段 Topic Sentence + 例子方向"),
        ("4-5 分钟", "检查：题目每部分都回应了吗"),
        ("提纲完成", "再动笔写引言，思路已清晰"),
        ("好处", "5 分钟提纲省下中途返工的时间"),
    ])

    U.model_answer(p, "高分引言范文（Discussion）+ 批注",
                   "Some people think that the government should spend money on public transport, "
                   "while others believe building more roads is better. Discuss both views and give "
                   "your own opinion.",
                   "As urban populations continue to swell, governments face a difficult choice "
                   "between investing in public transport networks and expanding road infrastructure. "
                   "Those who favour public transport point to its environmental and social benefits, "
                   "whereas advocates of road building emphasise convenience and economic growth. "
                   "This essay will consider both arguments before contending that prioritising "
                   "public transport offers the more sustainable long-term solution.",
                   ["背景句切入（urban populations swell），不用 Nowadays",
                    "paraphrase 题目两个选项，换词换句式",
                    "两方各用 favour / advocates 公正预告(CC)",
                    "末句 thesis 明确倾向公共交通(立场清晰)",
                    "consider both…before contending 预告结构",
                    "搭配地道：sustainable long-term solution(LR)"])

    U.model_answer(p, "高分引言范文（outweigh）+ 批注",
                   "More and more young people are choosing to study abroad. Do the advantages of "
                   "this trend outweigh the disadvantages?",
                   "In recent years, an increasing number of young people have opted to pursue their "
                   "education overseas, a trend that brings both opportunities and challenges. While "
                   "studying abroad can be costly and emotionally demanding, it offers invaluable "
                   "academic exposure, language immersion and cross-cultural skills. On balance, I am "
                   "convinced that the long-term benefits of overseas study significantly outweigh "
                   "its drawbacks.",
                   ["开头 In recent years 自然切入（替 Nowadays）",
                    "paraphrase 题目趋势（study abroad）",
                    "先点弊(costly)再点利，铺垫立场",
                    "末句 On balance…outweigh 明确表态(必须)",
                    "I am convinced that 强立场句",
                    "三个利处并列，为主体段埋线(LR)"])

    U.compare(p, "低分 vs 高分：审题落实", "✗ 低分（审题失误）", [
        ("Discuss 题只写一方", "漏答一半"),
        ("outweigh 题不表态", "缺总体立场"),
        ("忽略限定词", "写偏话题范围"),
        ("立场骑墙", "both sides are right"),
        ("引言无 thesis", "考官读不到立场"),
    ], "✓ 高分（审题到位）", [
        ("两方各一段+个人立场", "完整回应"),
        ("引言即表态利>弊", "立场明确"),
        ("紧扣限定词", "范围精准"),
        ("立场一边倒", "论证集中"),
        ("引言末句给 thesis", "第一印象稳"),
    ])

    # PART 07 课堂练习
    U.section(p, 7, "课堂练习", "In-Class Practice")
    U.drill(p, "练习一：识别题型", "判断下列题目属于哪种题型，并写出必须回应的部分。", [
        "To what extent do you agree that AI improves education?",
        "Discuss both views on free public museums and give your opinion.",
        "What causes youth unemployment and how can it be reduced?",
        "Do the advantages of remote work outweigh the disadvantages?",
        "Is the rise of fast fashion a positive or negative development?",
    ])

    U.drill(p, "练习二：审题三步法", "对下列题目完成“话题/角度/立场”三步分析。", [
        "Some think children should learn cooking at school. Do you agree or disagree?",
        "Discuss both views: city living vs countryside living, + your opinion.",
        "What are the causes of traffic congestion and what are the solutions?",
        "Do the benefits of tourism outweigh its drawbacks for local communities?",
        "Should governments fund space exploration? To what extent do you agree?",
    ])

    U.drill(p, "练习三：规划段落结构", "为下列题目列出段落骨架（每段一句 Topic Sentence）。", [
        "Longer prison sentences reduce crime. To what extent do you agree?",
        "Discuss both views on whether homework benefits children, + opinion.",
        "Causes & solutions of air pollution in big cities.",
        "Advantages and disadvantages of working from home.",
        "Do advantages of social media outweigh disadvantages?",
    ])

    U.drill(p, "练习四：写 thesis statement", "为下列题目各写一句清晰的 thesis。", [
        "University education should be free. (agree/disagree)",
        "Discuss both views on online vs classroom learning, + opinion.",
        "Do advantages of globalisation outweigh disadvantages?",
        "Causes & solutions of childhood obesity.",
        "Should the arts receive government funding? (to what extent)",
    ])

    # PART 08 避坑指南
    U.section(p, 8, "避坑指南", "Pitfalls to Avoid")
    U.pain_point(p, "审题与立场高频失分", [
        ("题型误判", "Discuss 写成 Opinion"),
        ("漏答任务", "outweigh 不表态/双问题漏一问"),
        ("忽略限定词", "题目说 children 却写 all people"),
        ("立场骑墙", "通篇不表态"),
        ("引言无 thesis", "绕三句还不亮立场"),
    ], [
        ("圈指令词", "discuss/outweigh/causes 决定结构"),
        ("逐任务回应", "题目每部分单独成段"),
        ("紧扣限定词", "范围严格对齐题目"),
        ("敢表态", "立场鲜明且一致"),
        ("thesis 前置", "引言末句给立场"),
    ])

    U.content(p, "常见错误清单（结构层面）", [
        ("题型混淆", "discuss≠agree；outweigh 必表态"),
        ("段落失衡", "Discussion 两方畸轻畸重"),
        ("立场不一致", "前段同意后段反对"),
        ("结论加新论点", "结论只重申，不引入新内容"),
        ("原因方案脱节", "问题解决型答非所问"),
        ("引言无预告", "不预告结构，CC 受损"),
    ], note="Discussion 题两方失衡是深圳高频问题：A 段写五句、B 段两句——考官看段落篇幅就判两方不平衡。")

    U.content(p, "提升 Task 2 审题的技巧", [
        ("指令词清单", "把 5 类指令词背熟，秒判题型"),
        ("限定词高亮", "审题时圈出 all/some/young/in cities"),
        ("立场口诀", "Opinion 一边倒；Discussion 两方+立场；outweigh 必表态"),
        ("提纲先行", "5 分钟提纲再动笔，避免跑题"),
        ("回链检查", "每段写完问：这段在回应题目哪部分"),
        ("范文反推", "看范文先猜题型，再核对"),
    ])

    U.tip_card(p, "五大题型速记卡", [
        ("Opinion 卡", "agree/disagree → 一边倒+让步反驳"),
        ("Discussion 卡", "discuss both → 两方平衡+个人立场"),
        ("Problem 卡", "causes+solutions → 原因方案对应"),
        ("Adv-Disadv 卡", "利弊各一段；outweigh 必表态"),
    ])

    U.tip_card(p, "审题三步速记卡", [
        ("话题卡", "锁定话题词与限定词，别扩大范围"),
        ("角度卡", "看指令词定要写什么"),
        ("立场卡", "要不要表态？倾向哪方？"),
        ("提纲卡", "三步结果直接转成段落骨架"),
    ])

    U.checklist(p, "本课自检清单", [
        "我能识别 5 种 Task 2 题型并说出各自要求",
        "我能用审题三步法判断话题/角度/立场",
        "我知道 discuss 与 agree、outweigh 的结构区别",
        "我能为每种题型规划正确的段落结构",
        "我能写出清晰、可贯穿全文的 thesis statement",
        "我会圈出并紧扣题目的限定词",
        "我能在 5 分钟内完成审题与提纲",
    ])

    U.summary(p, 4, [
        "5 种题型各有结构：审题错误是最贵的失分",
        "审题三步：找话题→找角度（指令词）→明确立场",
        "Opinion 一边倒；Discussion 两方+个人；outweigh 必表态",
        "thesis statement 放引言末句，必须清晰且全文一致",
    ], takeaway="先认题、再表态、后排结构——指令词决定一切，30 秒审题胜过 5 分钟返工。")

    U.homework(p, 4, [
        "收集 20 道 Task 2 真题，只做审题：识别题型 + 规划结构（不写全文）",
        "为其中 10 道各写一句清晰的 thesis statement",
        "判断 5 道题：立场应“完全同意”还是“部分同意”，并说明理由",
        "把一篇骑墙立场的范文改写为立场鲜明的版本",
    ], est_time="80 分钟")

    U.preview(p, 5, "Task 2 观点类作文精讲", [
        "五段式框架与引言三段式（Hook/Paraphrase/Thesis）",
        "论证链 PEEL：观点-解释-例子-影响",
        "让步反驳段的写法",
        "中国学生“举例不论证”通病的破解",
    ])
