import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_utils import *

def build(path):
    prs = new_prs()

    make_cover(prs,
        "雅思阅读 高分突破",
        "IELTS Reading · 10节课从6分到8分 · 深圳专属版",
        "MODULE 3 · READING · L01–L10")

    # ════════ L01 考试结构 & 失分诊断 ════════
    make_lesson_title(prs, 1, "考试结构\n& 失分诊断", [
        "了解Academic/General Training阅读的差异",
        "掌握14种题型的分布与特征",
        "诊断深圳学生阅读失分的5大原因",
        "制定个人10课时提分路线",
    ])
    make_content(prs, "L01 · 雅思阅读考试结构", [
        ("时间",        "60分钟完成3篇文章40道题，无额外时间誊写（答案直接写在答题卡）"),
        ("Academic版",  "3篇学术文章，总词数约2750词；话题多样：科学/历史/社会/技术"),
        ("General版",   "Sec A-B偏实用性文章（广告/通知）；Sec C为较难学术文章"),
        ("评分换算",    "6分≈正确23-26题；7分≈30-32题；8分≈35-37题；9分≈40题"),
        ("难度分布",    "P1最简单（单词量小）→P2适中→P3最难（学术词汇密集）"),
    ], note="深圳学生最大问题：60分钟不够用——原因是逐词精读，必须改为strategic reading。")

    make_pain_point(prs, "深圳学生阅读5大失分原因", [
        "逐词精读：一篇文章花20分钟以上，最后10分钟仓皇答第三篇",
        "看到不认识的词就卡住，不敢继续往下读",
        "T/F/NG三者逻辑区分不清，经常混淆False和Not Given",
        "答案定位：找到了段落但找不到具体句子，浪费大量时间",
        "词汇量不足以理解关键句，导致答案判断错误",
    ], [
        "建立时间规划：P1→17min / P2→20min / P3→23min（严格执行）",
        "学会带着问题读文章，不认识的词用上下文推断，继续往前",
        "T/F/NG有严格逻辑框架，必须记住判断标准（本课详解）",
        "先读题目找关键词，再定位段落，再精读那2-3句话",
        "专攻Academic Word List（AWL）词汇，考前背300核心词",
    ])

    make_content(prs, "L01 · 14大题型分类速览", [
        ("信息定位类", "T/F/NG; Y/N/NG; Matching Headings; Matching Information"),
        ("提取细节类", "Multiple Choice; Short Answer; Sentence Completion"),
        ("填空类",     "Summary/Note/Table/Flow-chart Completion"),
        ("匹配类",     "Matching Features; Matching Sentence Endings"),
        ("时间分配建议","每道题平均1.5分钟；难题标记后跳过，先做简单题"),
    ])

    make_summary(prs, 1,
        ["阅读60分钟=3篇×20分钟，严格时间分配是基础",
         "深圳学生核心问题：太慢+遇难词卡住——改变阅读策略比练词汇更紧迫",
         "带着问题读文章：先题目→找关键词→定位→精读答案句"],
        ["下载剑桥真题，完成1篇计时练习（17分钟内完成P1+12道题）",
         "背诵Academic Word List前50词（附带例句）",
         "分析最近一次阅读错题：哪些是题型不懂，哪些是词汇不够"])

    # ════════ L02 略读与扫读 ════════
    make_lesson_title(prs, 2, "略读与扫读\n核心技能", [
        "掌握Skimming（略读）获取文章主旨的方法",
        "掌握Scanning（扫读）快速定位答案的技巧",
        "学会在考试中灵活切换两种阅读模式",
        "通过限时训练将阅读速度提高30%",
    ])
    make_content(prs, "L02 · Skimming 略读策略", [
        ("目的",         "在60-90秒内获取文章主旨、结构框架和每段大意"),
        ("读什么",       "标题→首尾段全读→每段第一句（主题句）→特殊格式（粗体/斜体/数字）"),
        ("不读什么",     "具体举例的句子 / 数据细节 / 重复论证的中间句"),
        ("关键词标注",   "边读边圈出：人名/地名/数字/大写词——这些是答案定位锚点"),
        ("常见误区",     "深圳学生略读时还是在精读第一段——要强制自己跳过细节"),
        ("练习方法",     "设置计时器60秒，只读上述部分，然后能说出文章主题即成功"),
    ], note="Skimming不是粗心，而是有目的地忽略细节——考试中的文章90%内容不会考到。")

    make_content(prs, "L02 · Scanning 扫读策略", [
        ("目的",         "在已知目标关键词的情况下，快速在文章中定位答案所在句"),
        ("方法",         "眼睛只看关键词（人名/数字/专有名词），不读其他内容"),
        ("同义替换",     "题目关键词 ≠ 文章原词；要扫描的是文章中的paraphrase"),
        ("段落预判",     "根据heading或首句推断答案可能在哪段，先扫那一段"),
        ("Z形眼动",      "眼睛按Z字形扫描页面，每行只停0.5秒在关键词上"),
        ("练习方法",     "给定1个关键词，在1分钟内在一篇文章中找到它及周围句子"),
    ])

    make_example(prs, "L02 · Skimming实战：文章主旨提取",
        "以下是一篇文章的首尾段和每段首句，请在30秒内判断文章主题：\n\n"
        "Title: The Declining Bee Population and Its Consequences\n"
        "Para 1: Colony collapse disorder has decimated bee populations worldwide...\n"
        "Para 2: Bees are responsible for pollinating approximately one-third of human food supply...\n"
        "Para 3: Agricultural practices, particularly pesticide use, have been identified as key contributors...\n"
        "Para 4: Scientists are developing various strategies to reverse this trend...\n"
        "Final para: Without urgent intervention, the consequences for global food security could be catastrophic...",
        "主题：蜜蜂数量下降的原因及后果（Causes and consequences of declining bee populations）\n"
        "结构：问题→影响→原因→解决方案→结论（标准学术文章结构）",
        "Skimming完成后，你已经知道每段大意——之后做题只需回到对应段落精读2-3句")

    make_pain_point(prs, "阅读速度慢的根本原因", [
        "默读时在脑海中'读出'每个词的发音（subvocalization）",
        "遇到难词就停下来思考，打断阅读流程",
        "每读一句话就强迫自己完全理解才继续",
        "反复回读同一段（regression），缺乏信心继续往前",
    ], [
        "训练silent reading：眼睛扫过文字，不在脑中发音",
        "难词跳过继续，靠上下文推断，不查字典",
        "接受'模糊阅读'：理解60%主旨就够，细节在做题时精读",
        "强制向前：用手指或铅笔引导眼睛移动，不回读",
    ])

    make_summary(prs, 2,
        ["Skimming：90秒读出文章框架；Scanning：30秒定位答案句",
         "阅读速度慢的核心原因：subvocalization+难词卡壳——靠训练克服",
         "考试阅读流程：题目→提取关键词→Scan定位→精读答案句"],
        ["每天限时阅读练习：1篇新闻文章，10分钟内提取5个关键信息",
         "Skimming专项：每天用60秒Skim一篇英文文章，然后用中文复述主旨",
         "计时训练：P1文章+题目，目标15分钟内完成"])

    # ════════ L03 T/F/NG 判断题 ════════
    make_lesson_title(prs, 3, "T/F/NG 判断题\n精准攻克", [
        "建立True/False/Not Given的严格判断逻辑",
        "学会区分'文章没提'和'文章说了相反'",
        "掌握阅读题中最难的逻辑判断题型",
        "通过大量练习建立判断直觉",
    ])
    make_content(prs, "L03 · T/F/NG 判断标准", [
        ("TRUE",      "题目陈述与文章内容完全一致——包括同义替换后的一致"),
        ("FALSE",     "题目陈述与文章内容直接矛盾——文章明确说了相反的事"),
        ("NOT GIVEN", "文章完全没有提到题目涉及的信息——既不支持也不否定"),
        ("关键区分",  "FALSE=文章说了A，题目说了not A；NG=文章根本没说这件事"),
        ("最大误区",  "NOT GIVEN ≠ 你不知道答案！而是文章本身没有提供信息"),
    ], note="深圳学生最常犯的错误：把NG答成F（因为用常识判断，而不是用文章内容判断）。")

    make_example(prs, "L03 · T/F/NG判断练习",
        "文章原文：'The Great Wall of China was primarily built during the Ming Dynasty (1368-1644), "
        "though earlier versions were constructed by various kingdoms during the Warring States period. "
        "The wall stretches approximately 21,196 kilometres and is visible from low Earth orbit under "
        "certain atmospheric conditions.'\n\n"
        "题目判断：\n"
        "1. The Great Wall was first built during the Ming Dynasty.\n"
        "2. The Great Wall is longer than 20,000 kilometres.\n"
        "3. The Great Wall can always be seen from space.\n"
        "4. Foreign workers were used to construct the wall.",
        "1. FALSE（文章说primarily built in Ming，但earlier versions existed before）\n"
        "2. TRUE（21,196 km > 20,000 km，数字同义替换）\n"
        "3. FALSE（文章说under certain conditions，题目说always——明确矛盾）\n"
        "4. NOT GIVEN（文章完全没有提到who built it）",
        "判断NG的关键：在文章中找3-5秒，确认真的没有提到这个信息，再选NG")

    make_two_col(prs, "L03 · T/F/NG 高频考点与陷阱",
        "FALSE的触发词（文章中）", [
            "数量/程度词矛盾：all vs some / always vs often",
            "绝对词矛盾：never / only / exclusively / solely",
            "比较关系矛盾：more than / less than / similar / different",
            "因果关系矛盾：because / lead to / cause / result in",
            "时间矛盾：before / after / since / until",
        ],
        "NOT GIVEN的判断思路", [
            "找题目中的关键名词→在文章中Scan→找不到→NG",
            "找到了关键词但没有题目所问的具体信息→NG",
            "文章提到了话题，但没有对题目所述进行评价→NG",
            "不要用常识判断：'这当然是真的'不是选T的理由",
            "最后手段：用30秒仔细扫描全文确认没有提及",
        ])

    make_summary(prs, 3,
        ["T=一致 / F=矛盾 / NG=文章没提。三者逻辑清晰，不能混淆",
         "FALSE靠'矛盾'触发词识别；NG靠'确认文章完全没提'",
         "判断依据只有文章内容，禁止使用常识和个人知识"],
        ["完成剑桥真题T/F/NG题20道，按正确率分析错误模式",
         "专项练习：只做T/F/NG题，每道题说出判断依据（引用原文句子）",
         "整理个人T/F/NG判断错误案例，分析规律"])

    # ════════ L04 配对题 Matching Headings ════════
    make_lesson_title(prs, 4, "配对标题题\n& 信息配对题", [
        "掌握Matching Headings的段落主旨提取方法",
        "学会Matching Information的快速定位策略",
        "建立'主旨→标题'的配对思维",
        "通过练习消灭深圳学生配对题的失分",
    ])
    make_content(prs, "L04 · Matching Headings 解题步骤", [
        ("步骤1", "先读所有heading选项，找出每个heading的关键词（1-2个核心词）"),
        ("步骤2", "读段落：只读首句+尾句（主题句通常在段首或段尾）"),
        ("步骤3", "将段落主旨与heading选项配对——注意同义替换"),
        ("步骤4", "确定答案后划掉该选项（选项数量>段落数，有多余选项是陷阱）"),
        ("步骤5", "不确定的段落最后再处理——用排除法缩小范围"),
        ("注意",  "不能只看段落中出现了某个关键词——要匹配整段的主旨"),
    ], note="常见陷阱：某个heading中的词在段落中出现了，但那段的主旨其实是另一个意思。")

    make_content(prs, "L04 · Matching Information 解题策略", [
        ("题目类型",   "题目陈述+选项A-H（段落字母），要求找信息出现在哪段"),
        ("关键词提取", "从题目陈述中找最具体的关键词（数字/专有名词/少见词汇）"),
        ("定位策略",   "最具体的关键词最容易Scan定位；避免用常见词搜索"),
        ("同段多题",   "多道题答案可以在同一段——选项可以重复使用"),
        ("顺序规律",   "题目顺序≠文章顺序，答案可能分布在任何段落"),
        ("效率技巧",   "做Matching Info时，同步建立段落大意印象，辅助后续题型"),
    ])

    make_example(prs, "L04 · Matching Headings示范",
        "段落原文：'While solar and wind power have seen dramatic cost reductions over the past decade, "
        "one persistent challenge has been the intermittency problem. Unlike coal or gas plants that "
        "generate electricity on demand, renewable sources depend on weather conditions. Battery storage "
        "technology, though improving rapidly, remains too expensive for widespread grid deployment.'\n\n"
        "Heading选项：\n"
        "A. The environmental benefits of renewable energy\n"
        "B. Challenges in making renewable energy reliable\n"
        "C. The high cost of installing solar panels\n"
        "D. Recent improvements in energy storage",
        "答案：B（Challenges in making renewable energy reliable）\n"
        "分析：段落主旨是'间歇性问题'和'储能成本'这两个挑战，而非A的环境益处、C的安装成本或D的改进",
        "先读首句找主旨词：'persistent challenge'→匹配'challenges'；全段围绕这个主旨展开")

    make_summary(prs, 4,
        ["Matching Headings：段落首尾句提取主旨→配对heading→不靠单词，靠段落主旨",
         "Matching Information：提取具体关键词→Scan定位→答案可同段可重复",
         "两类题型都要警惕：关键词出现≠正确配对，要看语义匹配"],
        ["完成10道Matching Headings练习，每道记录判断依据",
         "练习Matching Information：给定5个关键词，30秒内在文章中全部定位",
         "分析错题：是没读懂段落主旨，还是被关键词陷阱误导"])

    # ════════ L05 多选题 & 填空题 ════════
    make_lesson_title(prs, 5, "多选题\n& 填空类题型", [
        "掌握Multiple Choice的排除法策略",
        "攻克Summary/Note Completion的定位与填写",
        "学会短答题(Short Answer)的精准答题规范",
        "消灭填空题中的词数违规失分",
    ])
    make_content(prs, "L05 · Multiple Choice 解题策略", [
        ("单选题策略",   "先定位题目在文章的位置→精读对应句→逐项排除错误选项"),
        ("常见干扰项",   "①与文章完全矛盾 ②文章未提及 ③夸大了文章的意思 ④范围不符"),
        ("排除顺序",     "先排除最明显错误的2个，再在剩余2个中精读对比"),
        ("全文选择题",   "问整篇文章的主旨/作者观点——需要Skim后再答"),
        ("多选题(选2)",  "每个选项单独判断对错，正确的✓，错误的✗，不确定的?"),
    ], note="深圳学生多选题错误率高达50%——因为只靠'感觉'选，没有系统排除法。")

    make_content(prs, "L05 · 填空题规则与技巧", [
        ("限词规定",   "'NO MORE THAN TWO WORDS AND/OR A NUMBER'——违反直接0分"),
        ("词性判断",   "根据空格上下文判断需要填名词/动词/形容词/副词"),
        ("原词 vs 改写","大多数填空答案是文章原词；少数summary completion需要同义替换"),
        ("大小写",     "专有名词大写，普通名词小写；不确定时参考空格所在句的首词"),
        ("复数/冠词",   "注意空格前后是否有冠词(a/the)或提示复数的标志"),
        ("定位技巧",   "Summary completion：先找summary中的关键词，在文章中定位相关段落"),
    ])

    make_example(prs, "L05 · 填空题实战练习",
        "Summary Completion（NO MORE THAN TWO WORDS）：\n\n"
        "The rainforest acts as a (1)__________ for the climate, absorbing large quantities of carbon dioxide. "
        "Deforestation not only destroys habitat for countless (2)__________ but also contributes significantly "
        "to (3)__________. Researchers estimate that approximately (4)__________ of global carbon emissions "
        "come from land-use change.\n\n"
        "文章原文（节选）：'Tropical rainforests serve as a crucial carbon sink, sequestering billions of tonnes "
        "of CO₂ annually. The destruction of these ecosystems eliminates habitat for millions of species and "
        "is a major driver of climate change. Studies indicate that around 10% of global emissions result "
        "from deforestation and related land-use changes.'",
        "(1) carbon sink（原词）  (2) species（原词）  (3) climate change（原词）  (4) 10%（数字）\n"
        "注意：(1)不能写'crucial carbon sink'（三个词违反限制）",
        "做填空前先看限词，再找关键词定位，复制原文词（拼写必须完全正确）")

    make_summary(prs, 5,
        ["填空题：先看限词→根据词性找答案→复制原文词→检查拼写大小写",
         "多选题：排除法+每项单独判断，不靠感觉",
         "所有题型：先定位段落，再精读2-3句，不要全文读完再答"],
        ["完成10道Summary Completion，每题标注限词并检查词数",
         "多选题专项练习：做完后说出每个错误选项被排除的理由",
         "整理填空题常见词性错误案例（填了动词应该填名词等）"])

    # ════════ L06 语境猜词 ════════
    make_lesson_title(prs, 6, "语境猜词\n& 词汇策略", [
        "学会从语境推断不认识词汇的意思",
        "掌握Academic Word List 300核心词",
        "建立雅思阅读常见词根词缀系统",
        "不靠字典完成阅读的信心建设",
    ])
    make_content(prs, "L06 · 语境猜词六大策略", [
        ("策略1：定义线索", "文章有时直接解释难词：X, which is... / X, also known as... / X, or..."),
        ("策略2：举例线索", "such as / for example / like后面的内容揭示难词含义"),
        ("策略3：反义线索", "unlike/however/in contrast+熟悉词→难词是其反义"),
        ("策略4：同义线索", "and/or并列的同义词中有你认识的→难词与之相近"),
        ("策略5：语法分析", "判断词性（主语/谓语/修饰语）→缩小含义范围"),
        ("策略6：词根词缀", "un-/dis-/in-（否定）；-tion/-ment（名词）；-ize/-fy（动词）"),
    ], note="语境猜词不是猜——是系统推断。70%的难词可以通过上下文线索推出大致意思。")

    make_two_col(prs, "L06 · AWL高频词根词缀系统",
        "前缀（改变意义）", [
            "un-/in-/im-/il-/ir- 否定",
            "re- 再次 (recycle/reform/replace)",
            "over- 过度 (overestimate/overlook)",
            "under- 不足 (undermine/underestimate)",
            "inter- 相互 (interact/international)",
            "pre- 之前 (precede/predict/prevent)",
            "post- 之后 (postpone/postmodern)",
            "multi- 多 (multinational/multitask)",
        ],
        "后缀（改变词性）", [
            "-tion/-sion 动词→名词 (education/expansion)",
            "-ment 动词→名词 (development/achievement)",
            "-ity/-ty 形容词→名词 (diversity/ability)",
            "-ous/-ious 名词→形容词 (numerous/various)",
            "-ize/-ise 名词→动词 (modernize/utilize)",
            "-ive 动词→形容词 (effective/productive)",
            "-al 名词→形容词 (national/political)",
            "-ly 形容词→副词 (significantly/considerably)",
        ])

    make_summary(prs, 6,
        ["语境猜词是考场中最实用的技能——70%难词可从上下文推断",
         "AWL核心300词覆盖学术文章40%的难词——必须掌握",
         "词根词缀系统让词汇量扩展1倍：认识一个词，推断10个派生词"],
        ["每天用语境猜词法读1篇The Economist文章，标注所有猜词过程",
         "背AWL词汇表：每天20词，带例句理解语境用法",
         "整理个人高频遇到的生词，分析可以用哪种猜词策略推断"])

    # ════════ L07 时间管理 ════════
    make_lesson_title(prs, 7, "时间管理\n& 答题节奏", [
        "建立严格的60分钟时间分配策略",
        "学会跳题和标记的高效答题流程",
        "练习在时间压力下保持准确率",
        "制定个人的时间管理方案",
    ])
    make_content(prs, "L07 · 60分钟时间分配方案", [
        ("P1（约700词）", "17分钟：3分Skim+14分做题13道题，简单快速，不纠结"),
        ("P2（约900词）", "20分钟：3分Skim+17分做题13道题，中等难度，标记难题"),
        ("P3（约1000词）","23分钟：3分Skim+20分做题14道题，最难，先做简单题"),
        ("整体原则",      "每段先Skim→做简单题→标记难题→时间剩余时回头攻难题"),
        ("时间信号",      "每15分钟检查一次：已完成多少题？是否按计划进行？"),
        ("终极原则",      "宁可空着不确定的题，先确保其他题答完——空题得0分"),
    ], note="深圳学生时间失控通常在P3：一道难题纠结5分钟，后面5题没时间做。")

    make_two_col(prs, "L07 · 题型时间分配参考表",
        "高效题型（优先做）", [
            "T/F/NG：有序，答案按段落顺序出现",
            "配对题：扫描定位快，每题约1分钟",
            "填空题（note/form）：关键词明确，定位快",
            "Short Answer：答案具体，定位较快",
            "建议：这类题先做，保证基础分",
        ],
        "耗时题型（谨慎分配）", [
            "Matching Headings：需要理解段落主旨，每段2分钟",
            "MCQ（全文主旨）：需要阅读完整文章",
            "Matching Features：选项多，逐一比对慢",
            "Summary（需推断）：需要理解文意+语言",
            "建议：标记后放到最后，时间充裕时再做",
        ])

    make_summary(prs, 7,
        ["时间分配：P1→17min / P2→20min / P3→23min，严格执行",
         "难题标记跳过：先确保简单题全对，再攻难题",
         "每15分钟检查节奏，不允许在单题上超过2分钟"],
        ["完整计时练习一套真题（60分钟），记录每篇完成时间",
         "分析时间分配问题：哪一篇超时？哪道题花了太长时间？",
         "本周每天做1篇P1计时练习，目标15分钟内完成"])

    # ════════ L08 Academic vs General ════════
    make_lesson_title(prs, 8, "Academic阅读\nvs General阅读", [
        "了解两种阅读考试的核心差异",
        "掌握General Training阅读的特殊策略",
        "针对考生实际需求选择备考重点",
        "通过对比练习强化题型理解",
    ])
    make_content(prs, "L08 · Academic vs General Training 对比", [
        ("文章类型",   "Academic：3篇学术文章；General：多篇实用文+1篇较难文章"),
        ("话题",       "Academic：科学/历史/社会；General：工作相关/生活实用/广告通知"),
        ("难度",       "Academic普遍词汇更难；General文章简单但题目量大"),
        ("Section A",  "General专有：多篇短文（广告/通知/标识），找specific info"),
        ("Section B",  "General专有：工作相关文章（合同/政策/手册）"),
        ("Section C",  "General的P3与Academic P2-3相当，不可轻视"),
    ], note="绝大多数深圳学生考Academic（用于大学申请）；若考移民签证则选General。")

    make_content(prs, "L08 · General Training 特殊策略", [
        ("Section A攻略", "多篇短文：先读题目关键词→扫描哪篇文章包含→精读那篇"),
        ("广告类文章",    "注意价格/联系方式/条件/限制——这些最常被考到"),
        ("政策类文章",    "注意must/should/may/cannot的权限区分——细节决定答案"),
        ("注意细节",      "日期/地点/联系方式/资格条件——不能只靠skimming"),
        ("时间建议",      "Section A+B约25分钟，Section C约35分钟"),
    ])

    make_summary(prs, 8,
        ["Academic：3篇学术文章，词汇难，逻辑复杂",
         "General：文章简单但数量多，注意Section A/B的实用信息",
         "深圳学生99%考Academic——但了解General有助于理解题型多样性"],
        ["Academic学生：完成1套完整Academic真题计时训练",
         "对比阅读：找一篇General Section A和一篇Academic P1，感受差异",
         "分析个人在Academic哪个段落失分最多，制定专项计划"])

    # ════════ L09 语篇分析 ════════
    make_lesson_title(prs, 9, "语篇分析\n& 文章结构", [
        "学会识别学术文章的常见组织结构",
        "通过段落功能分析提高阅读理解深度",
        "掌握作者观点与事实陈述的区分方法",
        "提高对长难句的解析能力",
    ])
    make_content(prs, "L09 · 学术文章常见结构模式", [
        ("问题-解决型", "Problem → Analysis → Solution → Evaluation（环保/科技类常见）"),
        ("原因-结果型", "Phenomenon → Causes → Effects → Implications（社会类常见）"),
        ("比较-对比型", "Theory A → Theory B → Comparison → Conclusion（历史/学科类）"),
        ("论点-支持型", "Claim → Evidence 1 → Evidence 2 → Counter-argument → Rebuttal"),
        ("时间顺序型", "Historical background → Development → Current state → Future"),
        ("应用",        "识别结构后，可以预判答案在哪个类型段落中"),
    ])

    make_content(prs, "L09 · 长难句解析方法", [
        ("第1步：找主语", "找句子的核心主语（名词或名词短语），忽略定语从句"),
        ("第2步：找谓语", "找主要动词，注意插入语（破折号/括号/逗号隔开的部分可忽略）"),
        ("第3步：找宾语", "找动作的对象，理解主谓宾基本关系"),
        ("第4步：分析从句", "分析which/that/who/where引导的从句是修饰谁的"),
        ("练习方法",      "用括号括住插入语，用下划线标主谓宾，简化句子结构"),
        ("常见结构",      "名词化结构：the development of... / increased reliance on..."),
    ])

    make_example(prs, "L09 · 长难句解析实战",
        "原句：'The extent to which technological innovation has fundamentally altered the nature of "
        "human communication — not merely in terms of the speed and reach of information dissemination, "
        "but also with regard to the depth and authenticity of interpersonal connection — remains a "
        "matter of considerable scholarly debate.'\n\n"
        "挑战：这句话的主语、谓语、宾语各是什么？",
        "主语：The extent to which technological innovation has fundamentally altered the nature of human communication\n"
        "（破折号中间是插入语，忽略）\n"
        "谓语：remains\n"
        "表语：a matter of considerable scholarly debate\n"
        "简化：'The extent to which X altered Y — [插入补充说明] — remains debated among scholars.'",
        "技巧：先找句子骨架（主谓宾），再理解修饰成分；不要从头到尾逐词理解长句")

    make_summary(prs, 9,
        ["识别文章结构：问题-解决/原因-结果/比较对比——帮助预判答案位置",
         "长难句：先找主谓宾，括号括插入语，再理解从句",
         "作者观点词：argue/suggest/claim/propose（主观）vs 事实陈述（无情态动词）"],
        ["选3篇不同结构类型的文章，标注每段的结构功能",
         "找10个学术文章中的长难句，用括号和下划线标注分析",
         "练习从长难句中快速提炼关键意思（限时：每句15秒）"])

    # ════════ L10 模拟考试 & 复盘 ════════
    make_lesson_title(prs, 10, "全真模考\n& 系统复盘", [
        "完成一套完整阅读模拟考试（严格60分钟计时）",
        "建立系统化的错题分析方法",
        "制定考前一周阅读冲刺计划",
        "总结个人阅读提分路线图",
    ])
    make_content(prs, "L10 · 考前一周阅读冲刺", [
        ("D-7",  "完整模拟1套（60分钟严格），按题型统计错误分布"),
        ("D-6",  "专攻弱项题型：精做5道T/F/NG或Matching Headings错题"),
        ("D-5",  "词汇冲刺：复习AWL前100词+个人生词本"),
        ("D-4",  "速度训练：只做P1+P2，限时30分钟，训练快速定位"),
        ("D-3",  "Skimming专项：3篇文章各60秒Skim，口述文章主题"),
        ("D-2",  "轻量复习：回顾个人错题本，不做新题"),
        ("D-1",  "保持阅读语感：读30分钟英文文章（任何有趣的），放松心态"),
    ])
    make_content(prs, "L10 · 个人提分路线总结", [
        ("从6分到7分的关键", "T/F/NG准确率提升+时间管理改善——这两项最影响分数"),
        ("从7分到8分的关键", "Matching Headings全对+长难句理解力+AWL词汇"),
        ("从8分到9分的关键", "几乎不犯拼写错误+限词违规0次+极快阅读速度"),
        ("持续练习量",       "每周至少2套完整真题，考前4周每天1篇"),
        ("最重要的一句话",   "阅读提分没有捷径——只有足够的有效练习量"),
    ])

    make_summary(prs, 10,
        ["60分钟时间管理+14种题型策略+词汇积累=阅读高分三要素",
         "每次练习后必须分析错题——找模式比做更多题更重要",
         "深圳学生最终目标：从逐词精读改变为策略性阅读"],
        ["完成本周模拟考，对比第1课基准分数，计算提分幅度",
         "建立个人阅读错题本（按题型分类），考前每天复习",
         "制定考试当天时间规划表：17+20+23分钟分配方案"])

    prs.save(path)
    print(f"[OK] Reading PPT → {path}")

if __name__ == "__main__":
    build("/home/user/data-analysis/ielts_ppts/IELTS_Reading_深圳提分版.pptx")
