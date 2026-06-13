import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_utils import *

def build(path):
    prs = new_prs()

    # ── COVER ────────────────────────────────────────────────────────────────
    make_cover(prs,
        "雅思听力 满分冲刺",
        "IELTS Listening · 10节课系统提分 · 深圳专属版",
        "MODULE 1 · LISTENING · L01–L10")

    # ════════════════════════════════════════════════════════════════════════
    # L01 考试全貌 & 失分诊断
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 1, "考试全貌\n& 失分诊断", [
        "了解雅思听力四个Section的结构与难度梯度",
        "掌握10大题型的特点与分布",
        "诊断深圳学生最常见的3类失分原因",
        "制定10课时个人提分路线图",
    ])
    make_content(prs, "L01 · 雅思听力考试全貌", [
        ("考试时长", "约30分钟录音 + 10分钟誊写（纸笔）/ 机考无额外誊写时间"),
        ("Section 1", "日常对话（订票/问路/预约）— 最简单，必须拿满分"),
        ("Section 2", "独白讲解（社区/活动/设施介绍）— 注意数字与地点"),
        ("Section 3", "学术讨论（2-4人，大学场景）— 观点区分是难点"),
        ("Section 4", "学术讲座（独白）— 专业词汇密集，最难，影响7+关键"),
        ("总题数",    "40题，每题1分；6分≈正确率60%；7分≈75%；8分≈88%"),
    ], note="深圳学生普遍Section 3丢分最多，因多人对话容易跟丢说话人。")

    make_content(prs, "L01 · 10大题型速览", [
        ("填空题 Form/Note/Table/Flow Completion", "拼写正确率决定得分，限词要求必须遵守"),
        ("单选题 Multiple Choice",                 "选项设陷阱，听到关键词不等于答案就在那里"),
        ("地图/平面图 Map Labelling",              "方向词是核心，opposite/next to/between"),
        ("匹配题 Matching",                        "需要边听边看所有选项，不能逐一对应"),
        ("简答题 Short Answer",                    "答案通常是名词短语，注意复数与冠词"),
    ])

    make_pain_point(prs, "为什么你听懂了却做错？", [
        "每个词都听到了，但写的时候拼错（necessary/accommodation）",
        "听到选项A中的关键词就选A，忽略后续的转折otherwise/but/actually",
        "专注听内容，忘记看题目，答案已经过去了",
        "Section 4 第一句话没跟上，后面全乱了",
        "誊写时把正确答案抄错",
    ], [
        "每天5分钟听写练习，专攻高频拼写词100个",
        "听到关键词时，继续听完整句，特别是连接词之后",
        "做题前30秒预读题目，预测关键词类型（人名/数字/地点）",
        "Section 4从第一题开始立即进入状态，不要热身",
        "誊写慢一倍速度，检查复数/大写/单位",
    ])

    make_example(prs, "L01 · 题型示例：填空题陷阱",
        "题目：The conference will be held on ________ 15th.\n"
        "（录音原文：The event was originally planned for Friday the 14th, but we've moved it to Saturday the 15th.）",
        "答案：Saturday（注意：不要写 Friday！录音先提14日再纠正为15日）",
        "预读时预测此处需要填'星期几'类词，听到数字前的修饰词不要漏掉")

    make_summary(prs, 1,
        ["S1最简单必须得满分，S4是拉开7+距离的关键",
         "10大题型各有陷阱，填空拼写、选择转折是重灾区",
         "深圳学生核心问题：听到了但做错，而非完全听不懂"],
        ["下载剑桥真题10-19，完成1套S1+S2（不计时，练熟悉感）",
         "整理个人拼写错误词表（从本课示例开始）",
         "下载BBC 6-Minute English，每天听1集"])

    # ════════════════════════════════════════════════════════════════════════
    # L02  Section 1 — 日常对话满分策略
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 2, "Section 1\n日常对话满分", [
        "掌握Section 1所有题型的答题节奏",
        "练习数字、电话号码、邮编等信息的快速捕捉",
        "学会100个雅思听力高频拼写词",
        "实现Section 1稳定满分10/10",
    ])
    make_content(prs, "L02 · Section 1 场景分类与预测策略", [
        ("高频场景1：预约类", "clinic/dentist/gym/library — 预测姓名、时间、电话"),
        ("高频场景2：租房类", "address, rent price, facilities, deposit — 预测地址格式"),
        ("高频场景3：旅游类", "tour booking, hotel, transport — 预测时间、价格、地名"),
        ("高频场景4：社区服务", "course registration, complaint — 预测人名、编号"),
        ("通用技巧",          "看题目→预测信息类型→带目的去听，不要泛听"),
    ], note="Section 1语速最慢，信息重复率最高，没理由丢分——如果丢分说明预读没做好。")

    make_content(prs, "L02 · 数字类信息捕捉专项", [
        ("电话号码", "英式读法：07700 → oh seven seven double oh；注意double/treble"),
        ("邮政编码", "英式格式：SW1A 2AA — 字母+数字混合，用斜线在纸上快速记录"),
        ("价格",     "£45.50 vs $45.50 — 注意货币单位，考试不需写货币符号"),
        ("时间",     "half past three / quarter to four — 转换为数字再写 3:30 / 3:45"),
        ("日期",     "the third of March / March 3rd — 统一写 3 March 或 March 3"),
        ("特殊数字", "thirteen(13) vs thirty(30)——注意-teen结尾重音在后"),
    ])

    make_example(prs, "L02 · 实战练习：信息表填空",
        "Customer Booking Form\n"
        "Name: __________ (1)\nPhone: __________ (2)\nDate required: __________ (3)\nSpecial request: __________ (4)\n\n"
        "（录音片段）A: Can I take your name please? B: Sure, it's Joanna — J-O-A-N-N-A — Briggs. B-R-I-G-G-S.\n"
        "A: And a contact number? B: 07891 double 4, 365.\nA: When do you need the room? B: The evening of the 23rd of April.",
        "(1) Joanna Briggs  (2) 07891 443365  (3) 23 April（注意：拼写逐字母，double=44）",
        "听到字母拼读时，在纸上同步拼写；double X=XX；电话号码一定数完再写")

    make_pain_point(prs, "Section 1 失分模式", [
        "字母拼读时没跟上速度，等反应过来已经过了",
        "写了first name漏了last name（或反之）",
        "数字13和30混淆，听teen还是ty",
        "大小写错误：name写小写，地名拼错",
        "限词'NO MORE THAN ONE WORD'写了两个词",
    ], [
        "每天练5个英文姓名拼写，训练字母接收速度",
        "看到Name题，预判可能有first+last两个空",
        "录音中thirteen重音在-teen，语调上扬；thirty重音在thir-",
        "人名地名首字母大写，其余小写，不确定全小写也可",
        "誊写前再看一眼字数限制，'one word and/or a number'也算一格",
    ])

    make_summary(prs, 2,
        ["预读30秒 → 预测信息类型 → 带目的听 → 检查拼写大小写",
         "数字/字母类信息：同步书写，不要等录音结束再写",
         "Section 1语速慢、信息重复——做到满分10/10是合理目标"],
        ["完成剑桥真题Section 1各两套，统计错误类型",
         "背诵高频拼写词50个（accommodation/necessary/available等）",
         "练习快速书写数字和字母，每天2分钟"])

    # ════════════════════════════════════════════════════════════════════════
    # L03  Section 2 — 独白讲解题型攻略
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 3, "Section 2\n独白场景攻略", [
        "掌握地图/平面图题的方向词与解题步骤",
        "学会从独白中提炼关键数据与分类信息",
        "攻克Section 2匹配题的同时跟踪技巧",
        "建立社区/设施/活动场景词汇库",
    ])
    make_content(prs, "L03 · Section 2 题型分布与场景", [
        ("常见场景", "博物馆导览、社区中心、旅游景点、志愿活动、设施介绍"),
        ("核心题型", "地图标注（Map）+ 匹配题（Matching）+ 选择题（MCQ）"),
        ("独白特点", "一人讲解，语速比S1快，信息量大，逻辑性强（顺序/分类）"),
        ("地图题",   "先看地图找参照物(entrance/main building)，听方向词定位"),
        ("匹配题",   "将选项A-F提前读熟，听到关键词→匹配描述→锁定答案"),
    ], note="深圳学生做地图题时，常常把north/south/left/right搞混——地图north朝上！")

    make_content(prs, "L03 · 地图题核心方向词", [
        ("位置关系", "next to / beside / adjacent to / opposite / facing"),
        ("方向移动", "turn left/right, go straight ahead, take the first turning"),
        ("相对位置", "at the end of, in the corner of, between X and Y"),
        ("绝对方位", "in the north/south/east/west of the building"),
        ("楼层",     "on the ground/first/second floor; upstairs/downstairs"),
        ("做题步骤", "①看参照点 ②预读问题中的地点 ③听方向词 ④边听边标注路径"),
    ])

    make_example(prs, "L03 · 地图题实战示例",
        "题目：Label the map. Write the correct letter A-F.\n"
        "Questions: 11. Children's Play Area  12. Café  13. Information Centre\n\n"
        "录音：'As you enter the park through the main gate, you'll see the car park on your left. "
        "The Information Centre is directly opposite the entrance. If you follow the path to the right, "
        "you'll find the Café next to the lake. The Children's Play Area is in the far north-east corner.'",
        "11→ NE corner (F); 12→ by the lake right side (D); 13→ opposite entrance (B)",
        "边听边在地图上画箭头标路径；'directly opposite'=正对面；'far NE corner'=右上角")

    make_pain_point(prs, "Section 2 地图题连续失分", [
        "没看清地图上已有的标注（把existing label当答案写进去）",
        "left/right从谁的角度搞混：应从站在地图中人物的视角",
        "听到方向词来不及在图上定位，跟丢了",
        "匹配题选项没提前读，听到时来不及找对应选项",
    ], [
        "做题前15秒：先扫描地图，圈出entrance/N箭头/已有标注",
        "记住：地图题left/right以人物行进方向为准，not地图绝对方向",
        "用铅笔在地图上轻轻画路径箭头，帮助跟踪方向",
        "匹配选项提前读完并记住关键词，而不是边听边找",
    ])

    make_summary(prs, 3,
        ["地图题：先识别参照点，用箭头跟踪路径，掌握20个核心方向词",
         "匹配题：选项提前读完，听到描述立即匹配，不要返回重找",
         "Section 2独白语速中等，信息有逻辑顺序，利用结构预判内容"],
        ["完成3套剑桥真题Section 2，重点练地图题",
         "整理方向词词表并默写10遍",
         "听BBC/National Geographic纪录片旁白，训练独白跟踪能力"])

    # ════════════════════════════════════════════════════════════════════════
    # L04  Section 3 — 多人学术对话突破
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 4, "Section 3\n学术对话突破", [
        "识别多人对话中的说话人切换信号",
        "捕捉观点、态度和评价类信息",
        "攻克Section 3高难度MCQ的排除法",
        "建立学术讨论场景词汇（作业/报告/研究）",
    ])
    make_content(prs, "L04 · Section 3 结构与挑战", [
        ("场景特点", "2-4名大学生/导师讨论：作业、报告、实验、presentation、研究方法"),
        ("语言特点", "观点交换频繁（I think/In my view/Actually/But don't you think）"),
        ("最难题型", "多选MCQ（从5个选项选2个）——必须判断每个说话人的态度"),
        ("态度词",   "enthusiastic/skeptical/surprised/agree/disagree/neutral/impressed"),
        ("核心策略", "标注说话人A/B/C，分别追踪各自的观点立场"),
    ], note="这是深圳学生平均失分最多的Section！关键：分清谁说了什么，而不是听懂每个词。")

    make_content(prs, "L04 · 观点与态度捕捉训练", [
        ("同意信号", "Exactly / That's a good point / I couldn't agree more / You're right"),
        ("不同意",   "Actually / Well / I'm not so sure / That's not necessarily true / But"),
        ("转折关注", "听到however/although/but/on the other hand——答案常在转折后"),
        ("观点归属", "She thinks... / As far as he's concerned... / From her perspective..."),
        ("态度判断", "语调上扬=肯定/赞同；语调下沉+停顿=怀疑/否定"),
        ("多选题法", "每个选项用✓✗?标注，确认的✓，排除的✗，不确定的?"),
    ])

    make_example(prs, "L04 · 多选题解题示范（Choose TWO）",
        "题目：Which TWO problems do the students mention about their research method?\n"
        "A. too time-consuming  B. sample size too small  C. results inconsistent\n"
        "D. equipment unreliable  E. data collection incomplete\n\n"
        "录音：Tom: 'I think the biggest issue is that we only surveyed 15 people — the sample is just too small.'\n"
        "Amy: 'I know, and I'm also worried that not everyone completed all the questions.'\n"
        "Tom: 'Yeah, the data collection wasn't thorough enough.'",
        "答案：B（sample too small）+ E（data collection incomplete）\n"
        "注意：A/C/D在录音中未提及，即使你觉得'合理'也不能选",
        "多选题：答案一定在录音中明确提到，不能靠推断；每个选项单独判断对错")

    make_pain_point(prs, "Section 3 MCQ 高频错误", [
        "听到选项中的某个词就以为是答案（词汇陷阱）",
        "录音说'I was going to... but'——结果没发生的事情当作答案",
        "两个说话人观点相反，选了被否定的那个",
        "多选题只写了一个答案，忘记要选两个",
    ], [
        "听到选项关键词≠正确答案，要确认整个句子的意思和逻辑",
        "注意否定结构：not/never/didn't/hardly——这类陈述通常是干扰项",
        "追踪说话人立场：用A: B: 标注笔记，避免张冠李戴",
        "多选题答题后检查：数字是否正确（选了2个还是1个）",
    ])

    make_summary(prs, 4,
        ["Section 3核心：分辨说话人 + 捕捉态度转折 + 排除干扰选项",
         "多选题必须听完每一个选项对应的内容再判断，不能听到就选",
         "转折词(but/however/actually)后面的内容往往是答案"],
        ["找Section 3多选题真题各3套，专项练习",
         "总结Section 3常见干扰策略（同义替换/否定陷阱/话题转移）",
         "每天听1段英语辩论/讨论，练习追踪多人观点"])

    # ════════════════════════════════════════════════════════════════════════
    # L05  Section 4 — 学术讲座高分突破
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 5, "Section 4\n学术讲座冲7+", [
        "建立学术讲座的听力框架与宏观结构意识",
        "掌握笔记速记符号系统",
        "攻克学术词汇的听力识别（Academic Word List）",
        "稳定拿到Section 4的6+分（30题中10题）",
    ])
    make_content(prs, "L05 · Section 4 结构解析", [
        ("特点",     "单人讲座，无打断，语速最快，专业词汇最密集，共10题"),
        ("常见学科", "历史/地理/生物/心理/经济/建筑/环境——关键词都有规律"),
        ("结构信号", "Today I'm going to talk about... / Firstly... / Moving on to... / To summarise..."),
        ("题型",     "填空为主（note completion / summary completion），MCQ辅助"),
        ("难点",     "单词听不懂怎么办？——靠上下文推断+笔记占位+继续往前听"),
    ], note="Section 4 要有'不求全听懂'的心态——听到40%关键信息就能得7/10分。")

    make_content(prs, "L05 · 学术讲座笔记速记系统", [
        ("数量/程度", "↑ increase / ↓ decrease / ≈ approximately / > greater than / < less than"),
        ("逻辑关系", "∴ therefore / ∵ because / → leads to / ↔ relationship / ≠ different"),
        ("常用缩写", "w/ with / w/o without / esp. especially / eg. example / cf. compare"),
        ("重复用词", "用数字①②③标并列信息；'+'连接相关概念"),
        ("实战建议", "不要试图写完整句子——只记关键名词和数字"),
        ("空格占位", "听不清的地方用_____标记，继续往后听，誊写时再回想"),
    ])

    make_example(prs, "L05 · 学术讲座实战：笔记填空",
        "Note Completion: Urban Heat Island Effect\n"
        "Causes: (31)__________ surfaces absorb more heat\n"
        "         reduced vegetation leads to less (32)__________\n"
        "Effects: nighttime temperatures (33)__________ than rural areas\n"
        "         increases energy consumption for (34)__________\n\n"
        "录音：'...impermeable surfaces such as concrete and asphalt absorb significantly more solar "
        "radiation. Furthermore, the lack of greenery means there is far less evapotranspiration occurring. "
        "As a result, urban areas can be up to 3 degrees warmer at night, driving up demand for air conditioning...'",
        "31. impermeable  32. evapotranspiration  33. warmer / higher  34. air conditioning",
        "31题：impermeable是专业词，可能拼不出→先写音标/首字母，誊写时补全；32题：evapo-trans-pi-ration逐音节听")

    make_pain_point(prs, "Section 4 崩溃场景及应对", [
        "开场没跟上，后面整个乱——'破罐子破摔'心态",
        "遇到不认识的词就卡住，后面5题全部错过",
        "笔记写太多，手写速度跟不上语速",
        "填空题答案写了但拼错，全错",
    ], [
        "跟丢了立即用题号重新定位——找下一个问题的关键词",
        "不认识的词：直接用字母标音或画线，继续往前听",
        "笔记只记名词+数字+形容词，动词/冠词全省略",
        "誊写时优先检查拼写：按音节分解s-e-p-a-r-a-t-e-l-y",
    ])

    make_summary(prs, 5,
        ["Section 4：建立框架→笔记占位→不纠结单个词→誊写检查拼写",
         "学会笔记速记系统，不求每词都写，只抓关键名词和数字",
         "跟丢了不要慌：立即用题号找到下一个锚点，继续答题"],
        ["做剑桥真题Section 4各3套，统计AWL词汇不认识的",
         "建立'雅思听力学科词汇表'（生物/地理/历史各30词）",
         "每天听TED-Ed 5分钟，练习从快速讲座中提炼关键信息"])

    # ════════════════════════════════════════════════════════════════════════
    # L06  预测技能 & 关键词定位
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 6, "预测技能\n& 关键词定位", [
        "系统训练预读技能——30秒内完成有效预判",
        "学会从题目预测答案的词性、范围和格式",
        "掌握同义替换识别（paraphrasing）",
        "建立听力的'预测→验证'循环流程",
    ])
    make_content(prs, "L06 · 预读的三个层次", [
        ("第一层：信息类型", "根据空格位置/题型判断需要听什么（名词？数字？形容词？）"),
        ("第二层：词汇范围", "根据语境缩小范围——如'booking date'预测月份+数字格式"),
        ("第三层：难度预判", "如果空格前后有专业词，准备接受不认识的词，听音记形"),
        ("关键词标记",       "在试卷上圈出题目关键词，预判录音中的同义替换"),
        ("时间分配",         "每道题预读≤5秒；提前翻到下一section预读≥20秒"),
    ], note="考试中有Section间隙（约30秒），这是预读下一Section最重要的时机！")

    make_content(prs, "L06 · 同义替换 Paraphrasing 专项", [
        ("数量表达", "a large number of → many; a significant decrease → fell sharply"),
        ("时间表达", "in the morning → before noon; at the weekend → on Saturday/Sunday"),
        ("程度表达", "extremely popular → very well-liked; slightly warm → a little above average"),
        ("动作替换", "was established → was set up / was founded / came into existence"),
        ("描述替换", "affordable → not expensive / within budget / reasonably priced"),
        ("练习方法", "剑桥真题做完后，对照录音原文找出题目与录音的替换对"),
    ])

    make_example(prs, "L06 · 预测练习：你能预测出什么？",
        "题目：The library opens at __________ on Sundays. (Q.1)\n"
        "       Membership costs £__________ per year. (Q.2)\n"
        "       Books can be borrowed for __________ days. (Q.3)\n"
        "       The library is located on __________ Street. (Q.4)",
        "Q1: 时间格式（9:00 / 10am / half past nine）\n"
        "Q2: 数字（price，可能是两位数，如£25 / £45）\n"
        "Q3: 数字（duration，可能是14/21/30天）\n"
        "Q4: 专有名词（街道名，首字母大写）",
        "预测完格式和范围后，听录音时耳朵更有针对性——不是'被动听'而是'主动找'")

    make_summary(prs, 6,
        ["预读30秒 = 考试中最重要的30秒，必须高效利用",
         "每个空格预测：词性+数字格式+词汇范围",
         "录音是题目的同义替换，不会出现100%原词"],
        ["完成5套预读专项练习：只预读不做题，然后对答案验证预测准确率",
         "整理50组高频同义替换配对（题目原文 vs 录音表达）",
         "每套真题做完后：对照文本找paraphrasing，建立替换词库"])

    # ════════════════════════════════════════════════════════════════════════
    # L07  笔记技能 & 缩写系统
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 7, "笔记技能\n& 速记系统", [
        "建立个人化的听力速记符号系统",
        "练习边听边记的双任务协调能力",
        "学会用笔记框架辅助答题（特别是S3/S4）",
        "提高手写速度和准确度",
    ])
    make_content(prs, "L07 · 听力笔记的核心原则", [
        ("原则1：记关键词", "只记名词/数字/形容词，省略冠词/介词/动词be"),
        ("原则2：记结构",   "用缩进/编号/箭头表示逻辑关系，不写完整句子"),
        ("原则3：记不确定", "听不清=留空/写首字母/写音似词，誊写时再核"),
        ("原则4：向前看",   "不要纠结已经过的答案，立即准备下一题"),
        ("错误示范",        "❌ 在笔记本上写完整段落（跟不上速度，必丢后面的答案）"),
    ])

    make_two_col(prs, "L07 · 速记符号对照表",
        "逻辑与关系符号", [
            "→  leads to / causes / results in",
            "↔  is related to / connected with",
            "∴  therefore / so / thus",
            "∵  because / due to / owing to",
            "+  and / also / in addition",
            "≠  different from / contrast with",
            "≈  approximately / about / around",
            "↑↓ increase / decrease",
        ],
        "常用词缩写", [
            "gov't  government",
            "env.   environment",
            "pop.   population",
            "tech.  technology",
            "econ.  economics/economy",
            "info.  information",
            "dept.  department",
            "esp.   especially",
            "eg./ex. for example",
            "ie.    that is",
        ])

    make_summary(prs, 7,
        ["速记不是写得少——是提取关键词+用符号替代长词",
         "笔记的目的是辅助记忆和追踪结构，不是记录全文",
         "手写速度慢是深圳学生的痛点——需要每日专项训练"],
        ["设计自己的10个核心速记符号，本周内全部形成肌肉记忆",
         "每天5分钟听写练习：听一段录音，只用符号和关键词做笔记",
         "对比笔记与原文，检验信息提取准确率"])

    # ════════════════════════════════════════════════════════════════════════
    # L08  陷阱类型全解析
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 8, "陷阱类型\n全解析", [
        "识别并规避雅思听力的6大出题陷阱",
        "建立'反陷阱'的听题习惯",
        "分析真题错题，找出个人陷阱敏感区",
        "通过模式识别提高抗干扰能力",
    ])
    make_content(prs, "L08 · 六大听力陷阱详解", [
        ("陷阱1：更正/修改", "先说A再改成B——答案是B（'Actually, let me correct that...'）"),
        ("陷阱2：否定式",   "'The meeting is NOT on Monday'——考生常写Monday"),
        ("陷阱3：同音/近音", "fifteen vs fifty / desert vs dessert / affect vs effect"),
        ("陷阱4：干扰选项", "选择题中提到某个关键词但不是正确答案（语义陷阱）"),
        ("陷阱5：顺序打乱", "答案不按题目顺序出现（地图题尤其如此）"),
        ("陷阱6：限词违反", "'NO MORE THAN TWO WORDS'但写了3个词——直接0分"),
    ], note="陷阱1（更正）是最常见也最容易规避的，只要养成'等录音说完整句'的习惯就能避免。")

    make_two_col(prs, "L08 · 更正陷阱 vs 否定陷阱",
        "更正陷阱 Correction Trap", [
            "触发词：actually / sorry / I mean / let me correct that / wait, no",
            "场景：A says 8 → 'Sorry, I meant 18'",
            "正确答案：18（后说的）",
            "解法：听到更正词立即划掉之前写的",
            "练习：剑桥15真题中共有14处更正陷阱",
            "记忆口诀：先说不算，后说才算",
        ],
        "否定陷阱 Negation Trap", [
            "触发词：not / never / no / neither / without / hardly",
            "场景：'The room is not available on Tuesday'",
            "考生错答：Tuesday（漏听not）",
            "正确答案：该日不可用，题目问available date则另选",
            "解法：提前圈出题目中的否定词，预判录音中也会有",
            "记忆口诀：听到not/never，答案反转",
        ])

    make_example(prs, "L08 · 综合陷阱练习",
        "题目：The centre is open every day EXCEPT __________.\n"
        "录音：'We're open seven days a week — well, actually six, because we close on Sundays. "
        "Oh wait, I should mention we're also closed on public holidays, but those aren't every week.'\n\n"
        "陷阱分析：\n"
        "① 先说seven days（干扰）→ 更正为six\n"
        "② 'closed on Sundays' → 答案应是Sunday\n"
        "③ 'public holidays'是额外信息，题目只问'every day EXCEPT'",
        "答案：Sunday（注意：public holidays不是每周固定，不符合'except'的含义）",
        "先排除干扰，再验证答案是否完整回答了题目的问题")

    make_summary(prs, 8,
        ["六大陷阱：更正>否定>同音>干扰>顺序>限词，按频率记忆",
         "更正陷阱：听到'actually/sorry'立即划掉之前答案",
         "限词陷阱：誊写前必须再看一次字数限制"],
        ["用红笔在真题上标出所有陷阱类型，统计个人被哪类陷阱抓最多",
         "做'只找陷阱'专项练习：带着找陷阱的目的做一套S1+S2",
         "将错题分类整理，分析自己的陷阱敏感词"])

    # ════════════════════════════════════════════════════════════════════════
    # L09  口音识别 & 速度适应
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 9, "口音识别\n& 速度适应", [
        "识别英式、澳式、美式口音的主要发音差异",
        "训练对不同语速的听力适应能力",
        "掌握连读、弱读、省音等自然语流特征",
        "提高实际考试中的口音适应速度",
    ])
    make_content(prs, "L09 · 雅思主要口音特征", [
        ("英式英语 RP", "不卷舌r（car=caa）；bath/can't中a发[ɑː]；'can't'听起来像'kaant'"),
        ("澳式英语",    "day/mate中ay发近似[æɪ]；today='te-dye'；'no'近似'noy'"),
        ("常见混淆词",  "英式thirteen vs 澳式thirteen——澳式t不送气，听起来像'dirteen'"),
        ("美式英语",    "雅思偶尔出现；r强卷舌；water='wader'；butter='budder'"),
        ("核心策略",    "不要背口音特征——大量泛听各类口音，靠熟悉度适应"),
    ], note="深圳学生普遍只听过美式发音（学校教材多为美音），遇到澳式口音第一反应：'这是英语吗？'")

    make_content(prs, "L09 · 自然语流特征（连读/弱读/省音）", [
        ("连读 Linking",  "'an apple'→'a-napple'; 'come on'→'comon'; 'next to'→'nexto'"),
        ("弱读 Reduction","'and'→[ən]; 'can'→[kən]; 'of'→[ə]; 'to'→[tə] ('want to'→'wanna')"),
        ("省音 Elision",  "'last night'→'las night'; 'next day'→'nex day'; 'must be'→'musbe'"),
        ("爆破不完全",    "'good morning'→'goo morning'（d不完整发音）"),
        ("练习方法",      "听录音原文→找连读位置→跟读模仿→再听验证"),
    ])

    make_summary(prs, 9,
        ["口音适应靠量——每天接触多种口音，不靠背发音规则",
         "连读/弱读是真正让人听不懂的原因，不是词汇量问题",
         "雅思录音以英式/澳式为主，需刻意训练这两种口音的适应"],
        ["每天听20分钟澳大利亚ABC News（澳式）+ BBC Radio（英式）",
         "找3段含大量连读的录音，标注所有连读位置后跟读",
         "完成一套剑桥真题，记录因口音导致的错题"])

    # ════════════════════════════════════════════════════════════════════════
    # L10  全真模考 & 系统复盘
    # ════════════════════════════════════════════════════════════════════════
    make_lesson_title(prs, 10, "全真模考\n& 系统复盘", [
        "完成一套完整雅思听力模拟考试（严格计时）",
        "建立系统化的错题分析方法",
        "制定考前一周的冲刺计划",
        "心理建设：考场应对与节奏控制",
    ])
    make_content(prs, "L10 · 考前一周冲刺计划", [
        ("D-7",  "完成1套完整模拟卷（含S1-S4），严格计时，误差不超过30秒"),
        ("D-6",  "精析错题：每道错题标注陷阱类型，重听3遍确认失分原因"),
        ("D-5",  "专项训练弱项Section（通常是S3/S4），各做3套"),
        ("D-4",  "拼写词复习：高频词100个过一遍，拼写练习20个"),
        ("D-3",  "轻量模拟：只做S1+S2，保持状态，避免过度练习"),
        ("D-2",  "听音乐放松，准备考试物品，不做新题"),
        ("D-1",  "早睡，听30分钟轻松英语广播，不刷新题"),
    ])

    make_content(prs, "L10 · 考场策略与心理建设", [
        ("提前30分钟", "到达考场，熟悉环境，调整座位让耳机舒适"),
        ("预读优先",   "每段录音前必须利用时间预读，哪怕只有20秒"),
        ("跟丢怎么办", "立即放弃已过的题，用题号找到下一个锚点继续"),
        ("卡壳怎么办", "填写最可能的答案，不要留空——猜1/4概率也比0高"),
        ("誊写技巧",   "纸笔考：最后10分钟誊写，检查拼写大小写复数"),
        ("机考差异",   "机考边听边输入，无誊写时间；提前练习键盘输入速度"),
    ])

    make_summary(prs, 10,
        ["模考要严格计时，不允许暂停——真实考试没有暂停键",
         "错题分析比做更多题更重要——找到模式，不重复犯错",
         "考场心态：跟丢了放弃，不要恐慌——保住能拿到的分"],
        ["本周完成2套完整模拟卷，目标分数对比第1课诊断结果",
         "制作个人听力错题本（按6大陷阱分类）",
         "考前3天：每天听1小时英语，保持语感，不刷新题"])

    # save
    prs.save(path)
    print(f"[OK] Listening PPT → {path}")

if __name__ == "__main__":
    build("/home/user/data-analysis/ielts_ppts/IELTS_Listening_深圳提分版.pptx")
