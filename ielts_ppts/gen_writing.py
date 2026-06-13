import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_utils import *

def build(path):
    prs = new_prs()

    make_cover(prs,
        "雅思写作 7分冲刺",
        "IELTS Writing · 10节课系统突破Task1+Task2 · 深圳专属版",
        "MODULE 4 · WRITING · L01–L10")

    # ════════ L01 评分标准全解 ════════
    make_lesson_title(prs, 1, "评分标准\n& 写作诊断", [
        "深入理解Task 1和Task 2的四大评分维度",
        "诊断深圳学生写作的典型问题",
        "建立正确的写作方法论",
        "了解考官评分的心理期待",
    ])
    make_content(prs, "L01 · Task 1 vs Task 2 基本规则", [
        ("Task 1 图表描述",  "150词以上 / 20分钟 / 占总分1/3 / 描述数据或流程，不写观点"),
        ("Task 2 议论文",    "250词以上 / 40分钟 / 占总分2/3 / 针对话题表达有论证的观点"),
        ("时间分配",         "建议：T1→20min / T2→40min；先做T2（分值更高，花时间值得）"),
        ("字数要求",         "低于150/250词扣分；多写不扣分，但质量>数量"),
        ("手写 vs 机考",     "机考可用spell check，但不影响评分标准；机考速度一般更快"),
    ], note="深圳学生最大误区：花35分钟在Task 1，只剩25分钟写Task 2——导致Task 2词数不足。")

    make_content(prs, "L01 · 四大评分维度详解", [
        ("TA/TR 任务回应 25%",  "T1：回答所有图表要素；T2：清晰立场+充分论证——最基础的要求"),
        ("CC 连贯与衔接 25%",   "段落清晰、连接词恰当、代词指代清晰；忌：乱用连接词"),
        ("LR 词汇资源 25%",     "用词精准多样；有collocations；拼写正确（拼写错误直接扣LR）"),
        ("GRA 语法范围 25%",    "句型多样（简单句+复合句）；时态准确；标点符号正确"),
        ("关键认知",            "TA/TR是基础，决定分数下限；LR+GRA是提分区间，决定6→7→8"),
    ])

    make_pain_point(prs, "深圳学生写作五大痛点", [
        "Task 2立场不明确：开头段绕了3句话才说观点",
        "中式英语：'With the development of society' / 'In my humble opinion'",
        "连接词误用：every sentence用Furthermore/Moreover/In addition",
        "Task 1只描述数字，不写Overall（缺少最重要的summary）",
        "词汇重复：important/people/society 每段都用",
    ], [
        "Task 2第一段最后一句：明确立场句（thesis statement）",
        "禁用中式开头：用'There has been growing debate about...'替代",
        "连接词只用来连接真正需要连接的内容，不是每句都加",
        "Task 1 Overview段是评分重点，必须写！",
        "每个关键词准备2个替换词，交替使用",
    ])

    make_summary(prs, 1,
        ["T2比T1更重要：先做T2，确保250词+充分论证+明确立场",
         "四维评分：TA是基础，LR+GRA是提分区间",
         "深圳学生最需要解决：立场不明+连接词滥用+Task 1缺Overview"],
        ["写一篇T2作文（不限时），请老师诊断4个维度各几分",
         "阅读5篇Band 7+ T2范文，标注：立场句/论证结构/高分词汇",
         "整理个人写作中用过最多次的5个词，每个找2个替换"])

    # ════════ L02 Task 1 折线图/柱状图 ════════
    make_lesson_title(prs, 2, "Task 1\n折线图与柱状图", [
        "掌握动态图表（折线图/柱状图）的描述框架",
        "学会Overview段的写法（最关键的段落）",
        "建立数据描述词汇库（趋势/比较/幅度）",
        "达到Task 1 Band 7的描述标准",
    ])
    make_content(prs, "L02 · Task 1 动态图表四段式框架", [
        ("第1段 Paraphrase（1-2句）", "改写题目说明：图表类型+主题+时间范围。禁止原文抄写！"),
        ("第2段 Overview（2-3句）",   "最重要！总体趋势+最高/最低/最显著特征——不含具体数据"),
        ("第3段 Detail A（3-4句）",   "描述主要趋势/组别的具体数据变化（含关键数字）"),
        ("第4段 Detail B（3-4句）",   "描述次要趋势或对比组别的具体数据变化（含关键数字）"),
        ("字数分配",                  "P1: 20词 / P2: 50词 / P3: 45词 / P4: 45词 = 约160词"),
    ], note="Overview段是考官评分的重中之重！没有Overview几乎不可能过6分。")

    make_content(prs, "L02 · 趋势描述词汇系统", [
        ("上升词",   "rose / increased / climbed / surged / soared（幅度小到大）"),
        ("下降词",   "fell / decreased / dropped / declined / plummeted（幅度小到大）"),
        ("平稳词",   "remained stable / levelled off / plateaued / stayed constant"),
        ("波动词",   "fluctuated / varied / oscillated between X and Y"),
        ("幅度词",   "slightly(5%以内) / gradually / significantly / dramatically / sharply"),
        ("句型搭配", "动词句：Sales rose sharply to 500 / 名词句：There was a sharp rise in sales to 500"),
    ])

    make_example(prs, "L02 · Task 1 折线图范文段落",
        "图表信息：折线图显示1990-2020年英国咖啡和茶的年消费量（百万升）\n"
        "咖啡：1990=200，持续上升到2020=600\n"
        "茶：1990=500，持续下降到2020=250\n\n"
        "请写Overview段和Detail A段：",
        "Overview: Overall, the most striking trend was the contrasting trajectories of the two beverages. "
        "While coffee consumption experienced significant growth throughout the period, tea consumption "
        "showed a consistent decline.\n\n"
        "Detail A: In 1990, coffee consumption stood at 200 million litres. It rose steadily over the "
        "following three decades, reaching 600 million litres by 2020 — a threefold increase.",
        "Overview不写数字，只写'最大趋势'；Detail才写具体数字；两段合计约80词")

    make_pain_point(prs, "Task 1 折线图常见失分", [
        "只写数字，不写趋势：'In 1990 it was 200. In 2000 it was 350. In 2010 it was 480.'",
        "抄写题目原句作为Introduction（被识别为原词抄写，TA扣分）",
        "忘写或写错Overview（只写了某一条线的趋势，没有比较）",
        "每个数据都写进去（选择性描述是高分标志，不是全部列出）",
        "时态错误：描述过去的图用现在时",
    ], [
        "数字+趋势词结合：'rose sharply from 200 to 480' 而非只写数字",
        "Introduction：改写题目主题，换词换句式",
        "Overview：找图表中最重要的1-2个总体规律（最高最低/对比趋势）",
        "选择性描述：只写最高点/最低点/转折点，忽略平稳段细节",
        "图表为过去时间→全文用过去时；未来预测→用情态动词",
    ])

    make_summary(prs, 2,
        ["四段式框架：Paraphrase→Overview→Detail A→Detail B",
         "Overview是评分重点：必须写，且只写总体趋势，不含数字",
         "趋势词+幅度词+数字=完整描述句型（rose sharply from X to Y）"],
        ["找3道折线图真题，每道只练Overview段（2-3句），反复修改",
         "背诵趋势词汇表：上升/下降/平稳/波动各5个，带幅度词配套使用",
         "完成1篇完整折线图Task 1（20分钟计时），请老师批改"])

    # ════════ L03 Task 1 饼图/表格/流程图/地图 ════════
    make_lesson_title(prs, 3, "Task 1\n饼图表格流程地图", [
        "掌握静态图表（饼图/表格）的比较描述方法",
        "学会流程图的顺序描述语言",
        "掌握地图题的变化描述框架",
        "能在20分钟内完成所有类型的Task 1",
    ])
    make_content(prs, "L03 · 静态图 vs 动态图区别", [
        ("动态图（折线/柱状）", "表示时间变化→用趋势动词（rose/fell）+过去时"),
        ("静态图（饼图/表格）", "表示某一时间点的分布/比较→用比较句型+过去时/现在时"),
        ("静态图Overview",      "找最大值/最小值/显著差异/占比最高的类别"),
        ("比较句型",             "X accounted for the largest share at 45% / X was considerably higher than Y"),
        ("饼图描述词",           "proportion / share / percentage / fraction of / segment"),
        ("表格描述策略",         "不写所有数据，只写最高/最低/最大差异，用行or列比较"),
    ])

    make_content(prs, "L03 · 流程图描述语言", [
        ("顺序连接词",  "First / Initially / Then / Next / Subsequently / Following this / Finally"),
        ("被动语态",    "流程图通常用被动语态：The material is heated to... / Water is then filtered..."),
        ("目的从句",    "...in order to remove impurities / ...so that the product can be..."),
        ("时态",        "一般现在时（描述通用流程）；自然流程也用现在时"),
        ("Overview策略","说明流程有多少步骤+起点和终点：'The process consists of X stages, beginning with... and culminating in...'"),
    ])

    make_content(prs, "L03 · 地图题描述框架", [
        ("Overview",    "总体变化：已建成/拆除/扩建；或：两个地区的最大差异"),
        ("对比描述",    "两张地图：In [year], there was... However, by [year], this had been replaced by..."),
        ("变化动词",    "was demolished / was constructed / was extended / was converted into / remained unchanged"),
        ("位置描述",    "in the north/centre/eastern part of the area; adjacent to / opposite / to the left of"),
        ("未变描述",    "...remained in the same location / ...was unchanged throughout the period"),
    ])

    make_example(prs, "L03 · 流程图范文示例",
        "流程图：玻璃瓶回收流程\n"
        "Collection → Sorting by colour → Cleaning/removing labels → "
        "Crushing → Melting → Moulding → Quality check → Distribution\n\n"
        "请写Introduction和Overview：",
        "Introduction: The diagram illustrates the process by which glass bottles are recycled, "
        "from collection to the distribution of new products.\n\n"
        "Overview: Overall, the recycling process involves eight distinct stages, beginning with the "
        "collection of used bottles and ending with the delivery of newly manufactured glassware to consumers.",
        "流程图Introduction：paraphrase题目；Overview：总步骤数+起点+终点（不写细节）")

    make_summary(prs, 3,
        ["静态图：最高/最低/比较句型+过去时；流程图：被动语态+顺序词+现在时",
         "地图题：变化动词（demolished/constructed）+位置词+对比结构",
         "所有Task 1都必须有Overview，这是与6分的核心差距"],
        ["练习每种图表类型的Overview段（各2道），不计时，专注质量",
         "整理流程图和地图题的专用词汇各20个",
         "完成1篇饼图+1篇流程图的完整Task 1练习"])

    # ════════ L04 Task 2 议论文类型 ════════
    make_lesson_title(prs, 4, "Task 2\n议论文类型全解", [
        "识别并区分5种Task 2题目类型",
        "掌握各类型的立场策略和段落规划",
        "建立审题不失分的'题目分析3步法'",
        "杜绝审题失误导致的TA失分",
    ])
    make_content(prs, "L04 · Task 2 五大题型识别", [
        ("类型1 观点题 Opinion Essay", "'Do you agree or disagree?' / 'To what extent do you agree?'"),
        ("类型2 讨论题 Discussion Essay", "'Discuss both views and give your own opinion'"),
        ("类型3 问题解决型", "'What are the causes of X? / What solutions can be offered?'"),
        ("类型4 双问题型", "'What are the advantages/disadvantages?' / 'Is this a positive/negative development?'"),
        ("类型5 混合型", "以上类型组合，如'Do you think the advantages outweigh the disadvantages?'"),
        ("审题3步法",    "①找话题（是什么）②找角度（说好坏/原因/解决方案）③明确立场要求"),
    ], note="深圳学生常犯错误：'Discuss both views'题目写成了纯Opinion essay，TA严重扣分。")

    make_two_col(prs, "L04 · 各题型立场策略",
        "Opinion / 观点题", [
            "立场：完全同意 or 完全不同意（更易获高分）",
            "结构：引言（立场）→支持论点1→支持论点2→让步反驳→结论",
            "避免：'both sides have good points'式的模糊立场",
            "'To what extent'：可以Partially agree，但要说清楚原因",
            "Thesis statement必须明确：'I firmly believe that...'",
        ],
        "Discussion / 讨论题", [
            "立场：讨论两种观点后，给出自己的观点",
            "结构：引言→一方观点段→另一方观点段→个人立场段→结论",
            "错误：只讨论两种观点不给自己立场（TA扣分）",
            "结论段必须重申自己的立场",
            "两个观点段：各3-4句，平衡篇幅",
        ])

    make_example(prs, "L04 · 审题实战：识别题型+确立立场",
        "题目1: 'Some people think that the government should spend money on public transport, while "
        "others think it is better to build more roads for private vehicles. Discuss both views and "
        "give your own opinion.'\n\n"
        "题目2: 'Nowadays, more and more young people are choosing to study abroad. "
        "Do you think the advantages of this trend outweigh the disadvantages?'\n\n"
        "题目3: 'Rising obesity rates are a major health concern in many countries. "
        "What are the causes of this problem and what measures can be taken to address it?'",
        "题目1: 讨论题→两方+个人观点，结构：引+公共交通段+私家车段+个人立场+结论\n"
        "题目2: 利弊题→表明总体利大于弊或弊大于利，结构：引+利处段+弊处段+结论\n"
        "题目3: 原因+解决方案题→各写一段，结构：引+原因段+解决方案段+结论",
        "审题时，用不同颜色笔画出：①话题关键词 ②题目指令（discuss/agree/causes）")

    make_summary(prs, 4,
        ["5种题型各有不同的段落结构要求，审题错误是最贵的失分",
         "Opinion题：明确立场；Discussion题：两方+个人；问题解决型：各写一段",
         "Thesis statement：Introduction最后一句，必须清晰表明立场"],
        ["收集20道Task 2真题，只做审题练习：识别题型+规划段落结构（不写全文）",
         "练习写Introduction段：每道题用2-3句完成Paraphrase+Thesis",
         "找5道真题，判断：这道题的立场应该'完全同意'还是'部分同意'？"])

    # ════════ L05 Task 2 观点类作文 ════════
    make_lesson_title(prs, 5, "Task 2\n观点类作文精讲", [
        "掌握Opinion Essay的完整写作框架",
        "学会写有力的Topic Sentence和论证支撑",
        "建立论证链：观点→理由→例子→影响",
        "避免'举例不论证'的中国学生通病",
    ])
    make_content(prs, "L05 · Opinion Essay 五段式框架", [
        ("引言段（3句话）",   "Hook（背景介绍）→ Paraphrase（话题说明）→ Thesis（明确立场）"),
        ("论点1段（4-5句）",  "Topic Sentence→Explanation→Evidence/Example→Result/Impact→Link"),
        ("论点2段（4-5句）",  "同上结构，第二个支持论点"),
        ("让步反驳段（3-4句）","Admittedly.../ However...→反驳对立观点（可选但加分）"),
        ("结论段（2-3句）",   "Rephrase thesis→Summary of main points→Final thought（不加新信息）"),
    ])

    make_content(prs, "L05 · 论证链展开技巧", [
        ("Topic Sentence",   "直接表明本段核心论点——考官只看首句判断段落方向"),
        ("Explanation",      "解释为什么这个论点成立（逻辑推导）"),
        ("Example",          "具体例子支撑论点（可用国家/城市/研究/假设场景）"),
        ("Impact",           "说明这个论点对个人/社会/未来有什么影响"),
        ("深圳学生问题",     "只有Example没有Explanation：'In China, many people...' 然后停了"),
        ("正确范式",         "Explanation→Example→Impact，Example只是中间环节，不是结论"),
    ], note="很多深圳学生把例子当论据：'China is developing fast, so...' 这不是论证，是举例。")

    make_example(prs, "L05 · 论证段范文对比",
        "题目：'Technology has made people's lives better. To what extent do you agree?'\n\n"
        "❌ 低分段落（5.5）：\n"
        "'Technology is very important in our lives. For example, we use smartphones every day. "
        "We can communicate with others. So technology makes life better.'\n\n"
        "✅ 高分段落（7）：\n"
        "'One of the most significant ways technology has improved quality of life is through "
        "advancements in medical treatment. Modern diagnostic tools such as MRI scanners and AI-driven "
        "analysis enable doctors to detect diseases at far earlier stages than was previously possible. "
        "As a result, survival rates for conditions like cancer have improved dramatically in recent "
        "decades, meaning that millions of people are living longer, healthier lives than their "
        "counterparts a generation ago.'",
        "高分段落要素：Topic Sentence（医疗进步）→Explanation（如何进步）→Example（MRI/AI）→Impact（生存率提高）",
        "段落展开：每段最少4句话，有完整的论证链，不只是列举事实")

    make_summary(prs, 5,
        ["Opinion Essay：引言（立场）→论点1→论点2→让步反驳→结论",
         "论证链：TS→Explanation→Example→Impact，缺任何一环都是低分段落",
         "例子只是论证的中间步骤，不是结论——解释'为什么'比举例更重要"],
        ["完成1篇完整Opinion Essay（40分钟计时，不少于260词）",
         "练习论证段写作：给定Topic Sentence，用4句话完成论证链",
         "找5篇Band 7范文，标注每段的TS/Explanation/Example/Impact"])

    # ════════ L06 Task 2 讨论类/利弊类 ════════
    make_lesson_title(prs, 6, "Task 2\n讨论题与利弊题", [
        "掌握Discussion Essay的平衡写法",
        "学会Advantages/Disadvantages题的论证策略",
        "建立'让步+反驳'的学术写作技巧",
        "能在40分钟内完成结构完整的讨论类作文",
    ])
    make_content(prs, "L06 · Discussion Essay 写作策略", [
        ("结构",        "引言→观点A段→观点B段→个人立场段（或在结论段表明）→结论"),
        ("引言",        "不在引言表明强烈立场，只说明'存在争议'，结尾一句预告将讨论两方"),
        ("观点A段",     "公正呈现一方的最强论点（即使你不同意），用'Proponents argue that...'"),
        ("观点B段",     "同样公正呈现另一方（'On the other hand, critics contend that...'）"),
        ("个人立场",    "可在第三个主体段表明，或在结论段说明。必须给出立场！"),
        ("深圳学生问题","观点A/B段不平衡：A段写5句，B段只写2句——考官看段落篇幅"),
    ])

    make_content(prs, "L06 · Advantages/Disadvantages 写法", [
        ("题目类型A", "'What are the advantages and disadvantages?' → 各写一段，结论给平衡评价"),
        ("题目类型B", "'Do advantages outweigh disadvantages?' → 必须表明总体立场（利>弊 or 弊>利）"),
        ("展开策略",  "不要列举3个优点/3个缺点——深入展开2个比浅显列举5个好"),
        ("Outweigh题","在引言就表明立场（利大于弊/弊大于利），结论重申；不能模糊"),
        ("连接词",    "优点段：Furthermore/Moreover; 缺点段：However/On the flip side"),
    ])

    make_example(prs, "L06 · Discussion 范文引言段",
        "题目：'Some people believe that social media has had a largely negative effect on society, "
        "while others argue that its benefits outweigh its drawbacks. Discuss both views and give "
        "your own opinion.'\n\n"
        "请写引言段（3句话）：",
        "The role of social media in modern society has become a subject of considerable debate. "
        "While many argue that platforms such as Instagram and TikTok have eroded privacy, spread "
        "misinformation, and damaged mental health, others maintain that these tools have revolutionised "
        "communication, empowered marginalised communities, and democratised access to information. "
        "This essay will examine both perspectives before arguing that, on balance, the benefits of "
        "social media are outweighed by its societal harms.",
        "三句结构：背景（争议）→两方观点预告→Thesis（明确立场：弊>利）；引言约60词，不展开论点")

    make_summary(prs, 6,
        ["Discussion题：两方平衡+个人立场，缺立场等于TA严重扣分",
         "Outweigh题：Introduction就必须表明利>弊或弊>利",
         "两方段落篇幅要平衡，不能A段5句B段2句"],
        ["完成2道Discussion Essay（各40分钟），其中1道含Outweigh",
         "练习引言段写作：10道题目各写引言，不写主体段",
         "找5篇Discussion Band 7范文，分析两方段落的平衡程度"])

    # ════════ L07 Task 2 问题解决型 ════════
    make_lesson_title(prs, 7, "Task 2\n问题解决型作文", [
        "掌握原因分析段的逻辑展开方法",
        "学会提出切实可行解决方案的写法",
        "建立社会问题类话题的词汇库",
        "通过完整范文分析掌握高分结构",
    ])
    make_content(prs, "L07 · 问题解决型结构框架", [
        ("引言（3句）",     "背景说明问题严重性→Paraphrase题目→Thesis（说明将讨论原因和解决方案）"),
        ("原因段（4-5句）", "Topic Sentence（主要原因）→展开1个核心原因→另1-2个相关原因"),
        ("解决方案段（4-5句）","Topic Sentence（对应解决方案）→解释如何实施→例证→预期效果"),
        ("结论（2-3句）",   "重申问题严重性→总结解决方案→展望"),
        ("重要原则",        "原因和解决方案要对应！说了饮食问题，就要提饮食干预方案"),
    ], note="深圳学生常见问题：原因和解决方案不对应，说了A原因，提了B解决方案——逻辑断裂。")

    make_two_col(prs, "L07 · 高频社会问题词汇库",
        "问题描述词汇", [
            "rising/increasing prevalence of... 增加的普遍程度",
            "poses a serious threat to... 对...构成严重威胁",
            "has reached alarming proportions 已达到令人担忧的程度",
            "exacerbates existing inequalities 加剧了现有不平等",
            "socioeconomic disparity 社会经济差距",
            "unsustainable growth / urban sprawl 不可持续增长/城市蔓延",
        ],
        "解决方案词汇", [
            "government intervention / policy reform 政府干预/政策改革",
            "implement stricter regulations 实施更严格的法规",
            "raise public awareness campaigns 开展公众意识活动",
            "invest in infrastructure 投资基础设施",
            "corporate social responsibility 企业社会责任",
            "holistic / multi-faceted approach 整体/多方面的方法",
        ])

    make_summary(prs, 7,
        ["原因-解决方案：一一对应是逻辑高分的关键",
         "引言说明问题严重性，结论展望改善效果——有完整的论证弧线",
         "解决方案要具体：'政府应...'比'人们应该更努力'更有说服力"],
        ["完成2篇问题解决型作文（各40分钟）",
         "检查：每个原因是否有对应的解决方案？",
         "背诵社会问题类词汇30个，本周内在写作中全部使用一次"])

    # ════════ L08 连贯衔接 & 词汇资源 ════════
    make_lesson_title(prs, 8, "连贯衔接\n& 词汇资源提升", [
        "学会正确使用各类连接词（而非滥用）",
        "掌握段落内的逻辑连贯技巧",
        "提升词汇多样性和精确度",
        "CC和LR从6分到7分的具体改善方法",
    ])
    make_content(prs, "L08 · 连接词正确使用原则", [
        ("原则1：用来连接",   "连接词是用来连接两个具有逻辑关系的想法，不是装饰品"),
        ("原则2：不过度",     "一个段落中最多2-3个连接词；不要每句话都加Furthermore"),
        ("原则3：用词准确",   "Furthermore=补充相似内容；However=转折；Therefore=结果"),
        ("原则4：多样化",     "不要只用However/Furthermore，学会使用多种衔接手段"),
        ("其他衔接手段",      "代词替代（it/this/these）/ 同义词替换 / 重复关键词 / 省略"),
        ("危险词汇",          "禁止使用：Firstly在写作中过度使用/In a word/Last but not least"),
    ], note="连接词误用是CC扣分最直接的原因。考官看到every sentence有Furthermore，认为考生不懂逻辑关系。")

    make_two_col(prs, "L08 · 正确 vs 错误连接词使用",
        "❌ 滥用连接词（常见错误）", [
            "Firstly, X. Secondly, Y. Thirdly, Z. Furthermore, A. Moreover, B.",
            "（每句都有连接词，机械罗列）",
            "In conclusion, we can see that... (空洞总结)",
            "Nowadays, with the development of society... (中式开头)",
            "In my humble opinion... (正式写作不用)",
            "Last but not least... (陈腐套语)",
        ],
        "✅ 正确衔接方式", [
            "代词：'This has led to...' / 'These factors...'",
            "同义替换：people → individuals / residents / citizens",
            "论点递进：关键词重复但用不同形式",
            "逻辑词精准：As a result（结果）/ In contrast（对比）",
            "段落间不加连接词，靠Topic Sentence承上启下",
            "结论：'In conclusion, it is evident that...'（清晰不套路）",
        ])

    make_content(prs, "L08 · LR词汇资源提升策略", [
        ("搭配记忆",   "不背单词，背词组：'have a profound impact on' 而非单背'impact'"),
        ("语域准确",   "写作用正式词汇：start→commence / show→demonstrate / get→obtain"),
        ("拼写检查",   "拼写错误=LR直接扣分；必须背会高频学术词拼写"),
        ("避免重复",   "每个关键词准备2-3个同义表达，在文章中交替使用"),
        ("词汇密度",   "一篇文章中出现3+次的词：people/government/important——必须替换"),
        ("高分词使用", "不强行使用难词，宁可准确用中级词，也不错误用高级词"),
    ])

    make_summary(prs, 8,
        ["CC：连接词不是越多越好，用对逻辑关系比数量重要",
         "LR：搭配>单词；正式词汇>口语词汇；拼写正确是基础",
         "最快提分法：找到文章中重复3次以上的词，全部替换"],
        ["改写练习：将一篇充满连接词的低分作文改写，删掉多余连接词",
         "整理个人写作词汇替换表：5个关键词×3个替换词",
         "每天背5个Academic collocations（带例句），本周在写作中使用"])

    # ════════ L09 语法与时态 ════════
    make_lesson_title(prs, 9, "语法准确性\n& 句型多样化", [
        "掌握写作中必须正确使用的5类语法结构",
        "学会用从句和复合句增加句型多样性",
        "消灭深圳学生写作中的7大语法高频错误",
        "GRA从6分到7分的关键语法改善",
    ])
    make_content(prs, "L09 · 写作五大必备语法结构", [
        ("定语从句",    "The policy, which was introduced in 2010, has significantly reduced emissions."),
        ("条件句",      "If governments were to invest more in renewable energy, carbon emissions would decline."),
        ("让步从句",    "Although economic growth is essential, it should not come at the expense of the environment."),
        ("被动语态",    "It is widely believed that... / Children are increasingly exposed to..."),
        ("名词化结构",  "The rapid development of AI→AI's rapid development / AI is developing rapidly→"),
    ], note="深圳学生写作句型单调：80%简单句。GRA 7分要求复杂句占比超过50%。")

    make_content(prs, "L09 · 七大高频语法错误", [
        ("错误1：主谓不一致", "The number of people who use smartphones are increasing. → IS"),
        ("错误2：冠词遗漏",   "Internet has changed the world. → THE Internet"),
        ("错误3：时态混乱",   "Task 1描述过去图表全文用现在时（应用过去时）"),
        ("错误4：分词悬垂",   "Being a student, technology is important. → 主语不对应"),
        ("错误5：比较结构",   "More important than other issues. → More important than OTHER ISSUES ARE"),
        ("错误6：并列不平行", "Reading, writing, and to speak English. → reading, writing, and speaking"),
        ("错误7：虚拟语气",   "If I was the government... → If I WERE the government（虚拟过去式）"),
    ])

    make_example(prs, "L09 · 语法升级改写练习",
        "原文（6分语法）：\n"
        "'Many people think technology is good. It can help us in many ways. For example, we can use "
        "the internet to find information. We can also use apps to learn new things. But some people "
        "think technology is bad. They think it makes people lazy. I think technology is mostly good.'\n\n"
        "改写目标：提升句型多样性，加入至少3种不同句型结构：",
        "改写示范（7分）：\n"
        "'While opinions on technology's impact remain divided, it is undeniable that digital tools have "
        "transformed the way people access information and acquire new skills. Proponents argue that "
        "the internet, which now connects billions of people globally, has democratised knowledge in "
        "unprecedented ways. Critics, however, contend that excessive reliance on devices has eroded "
        "people's capacity for independent thought. Despite this concern, I would argue that the "
        "benefits of technology, if used judiciously, significantly outweigh its drawbacks.'",
        "改写要点：while让步从句+定语从句(which)+条件句(if used)+被动语态+formal词汇替换")

    make_summary(prs, 9,
        ["GRA 7分：50%以上复合句+主要语法错误少+句型多样",
         "5种必备结构：定语从句/条件句/让步从句/被动/名词化",
         "7大错误：主谓一致/冠词/时态是最高频——必须零容忍"],
        ["改写练习：将自己最近写的作文，把简单句改写成复合句",
         "语法专项：每天做5道主谓一致+冠词判断练习题",
         "找5篇Band 7+范文，统计每篇中复合句的使用比例"])

    # ════════ L10 模拟考试 & 复盘 ════════
    make_lesson_title(prs, 10, "全真模考\n& 系统复盘", [
        "完成一套完整写作模拟考试（T1+T2，60分钟）",
        "建立写作自我评估的四维框架",
        "制定考前一周写作冲刺计划",
        "总结个人写作提分路线图",
    ])
    make_content(prs, "L10 · 60分钟考场写作流程", [
        ("00:00-02:00", "读题+审题：Task 2题目类型？立场？主要论点？"),
        ("02:00-05:00", "Task 2 提纲：每段Topic Sentence + 2个支撑点"),
        ("05:00-40:00", "Task 2 正文写作：引言→主体1→主体2→（让步）→结论"),
        ("40:00-42:00", "Task 1 读图：图表类型？Overview的总趋势是什么？"),
        ("42:00-45:00", "Task 1 提纲：4个段落的内容分配"),
        ("45:00-60:00", "Task 1 写作+全文检查（检查拼写/时态/词数）"),
    ], note="先做Task 2的原因：Task 2占2/3分数，精力最好时写质量最高——不要被Task 1'热身'消耗精力。")

    make_content(prs, "L10 · 考前一周写作冲刺", [
        ("D-7", "完整模拟（60分钟：T1+T2），请老师按四维标准批改"),
        ("D-6", "精析批改意见：TA/CC/LR/GRA各项哪里扣分？"),
        ("D-5", "专项训练弱项：LR弱→词汇替换练习；CC弱→连接词改写"),
        ("D-4", "Task 1专项：3道不同图表类型，各写Overview段"),
        ("D-3", "Task 2专项：写2篇引言段+论证段（不写完整文章）"),
        ("D-2", "回顾个人高频错误清单，不写新文章，只看范文"),
        ("D-1", "休息放松，默诵立场句和Overview句型，不写作"),
    ])

    make_content(prs, "L10 · 个人提分路线总结", [
        ("从5.5到6分", "Task 2字数>250词 + 有明确立场 + Task 1有Overview"),
        ("从6到7分",   "论证段有TS+Explanation+Example+Impact + 词汇替换 + 50%复合句"),
        ("从7到8分",   "论证深度+词汇精准搭配+极少语法错误+段落逻辑完美衔接"),
        ("持续训练量", "考前4周：每周至少3篇作文（T1+T2各至少1篇）"),
        ("最终建议",   "写作没有捷径——每篇作文+批改+修改=最高效的提分循环"),
    ])

    make_summary(prs, 10,
        ["60分钟流程：先T2后T1，确保T2充分展开（250+词，有完整论证）",
         "四维自评：TA→CC→LR→GRA，找到最低分的维度集中突破",
         "写作提分公式：写作→批改→分析→修改→再写，持续循环"],
        ["本周：完成完整模拟考，对比第1课基准分数，计算提分幅度",
         "建立个人写作错误清单（按四维分类），考前每天复习",
         "制作考试当天时间规划卡片：00:00写T2 / 40:00写T1 / 58:00检查"])

    prs.save(path)
    print(f"[OK] Writing PPT → {path}")

if __name__ == "__main__":
    build("/home/user/data-analysis/ielts_ppts/IELTS_Writing_深圳提分版.pptx")
