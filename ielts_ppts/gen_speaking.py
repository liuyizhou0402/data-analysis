import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_utils import *

def build(path):
    prs = new_prs()

    make_cover(prs,
        "雅思口语 7分冲刺",
        "IELTS Speaking · 10节课从哑巴英语到7分表达 · 深圳专属版",
        "MODULE 2 · SPEAKING · L01–L10")

    # ════════ L01 评分标准全解 ════════
    make_lesson_title(prs, 1, "评分标准\n& 现状诊断", [
        "深入理解四大评分维度（FC/LR/GRA/P）",
        "诊断深圳学生口语的典型问题",
        "建立正确的口语学习方法论",
        "了解Part 1/2/3的时间分配与评分权重",
    ])
    make_content(prs, "L01 · 四大评分维度详解", [
        ("FC 流利度与连贯性 25%", "语速自然、停顿合理、连接词丰富；最忌：背诵感强、'robot English'"),
        ("LR 词汇资源 25%",       "用词多样、地道、有搭配；忌：高频简单词堆砌（good/nice/big）"),
        ("GRA 语法范围与准确性 25%", "时态准确、句式多样；简单句全对>复杂句全错"),
        ("P 发音 25%",            "清晰易懂为主；口音不扣分，但语调单调、吞音会扣分"),
    ], note="深圳学生普遍GRA和P相对强，FC和LR是拉低分数的核心问题——中式逻辑+有限词汇。")

    make_pain_point(prs, "深圳学生口语四大痛点", [
        "背诵模板：考官一眼识别，FC直接打低分",
        "说话总想先想中文再翻译，导致停顿过多(um...er...uh...)",
        "词汇单调：good/nice/interesting/important反复用",
        "说完Part 2题卡就停下，没有自然延伸和细节",
        "Part 3回答太短：只有一两句，没有展开论证",
    ], [
        "不背模板，背语言素材（词块/搭配/句型）",
        "用filler words过渡：Well, / That's a good question / Let me think...",
        "建立替换词词库：good→remarkable/outstanding/genuinely enjoyable",
        "Part 2讲故事：5W1H框架确保2分钟内容充实",
        "Part 3用PEEL结构：观点→解释→例子→总结（最少4句话）",
    ])

    make_content(prs, "L01 · 三个Part时间分配", [
        ("Part 1 介绍与日常话题", "4-5分钟 / 10-12个问题 / 每题2-3句话 / 话题：家乡/学习/兴趣/日常"),
        ("Part 2 长篇独白",       "3-4分钟 / 准备1分钟+说1-2分钟 / 题卡上有4个提示点"),
        ("Part 3 深度讨论",       "4-5分钟 / 4-6个问题 / 每题4-6句话 / 话题扩展至社会层面"),
        ("评分时机",              "考官全程评分，Part 1的第一句话就决定了考官对你的第一印象"),
        ("开场建议",              "Part 1第一题：直接回答+细节，不要客套'Nice to meet you'"),
    ])

    make_summary(prs, 1,
        ["FC+LR是核心得分项，GRA和P是基础保障项",
         "不背模板——背词块和搭配，让语言听起来自然",
         "Part 1开场直接回答，Part 2讲故事，Part 3讲观点+例子"],
        ["录音1分钟自我介绍，听回放评估：有几个um/er/uh？",
         "列出10个你经常说的单词，每个找2个替换词",
         "每天跟读TED演讲3分钟，模仿语调和节奏"])

    # ════════ L02 Part 1 个人话题速答 ════════
    make_lesson_title(prs, 2, "Part 1\n个人话题速答", [
        "掌握Part 1的答题节奏与扩展技巧",
        "建立家乡/学习/工作/兴趣等核心话题词库",
        "练习自然的3-4句话扩展模式",
        "消除'背诵感'，让回答听起来真实自然",
    ])
    make_content(prs, "L02 · Part 1 答题公式", [
        ("基础公式",   "答案 + 原因/细节 + 例子/补充 = 2-3句自然回答"),
        ("切忌",       "只答是/否（太短）；说5句以上（太长，占用考官下题时间）"),
        ("话题分类",   "个人信息类/日常习惯类/喜好偏好类/家乡环境类/学习工作类"),
        ("连接词",     "...because... / ...and what I like most is... / ...especially when..."),
        ("举例方式",   "For instance, / Like last weekend, / I remember once..."),
    ])

    make_two_col(prs, "L02 · Part 1 高频话题词库",
        "家乡 & 居住地", [
            "be situated in the heart of / on the outskirts of",
            "vibrant/bustling metropolis — 充满活力的大城市",
            "a fast-paced lifestyle / rapid development",
            "subtropical climate / year-round warmth",
            "tech hub / innovation-driven city（适合深圳）",
            "diverse culinary scene / blend of cultures",
            "convenient public transport / extensive metro network",
        ],
        "兴趣爱好", [
            "I'm really into... / I'm passionate about...",
            "it helps me unwind / de-stress after a long day",
            "I've been doing it since I was... / for about X years",
            "it gives me a sense of accomplishment",
            "I tend to... rather than... when I have free time",
            "streaming platform / binge-watch / on-demand content",
            "hit the gym / work out / keep fit",
        ])

    make_example(prs, "L02 · Part 1 答题对比：低分 vs 高分",
        "问题：Do you enjoy cooking?\n\n"
        "❌ 低分回答（5分）：\n"
        "'Yes, I like cooking. It is interesting. I cook sometimes. It is good for health.'\n"
        "（词汇单调、句子碎片化、没有个人特色）\n\n"
        "✅ 高分回答（7分）：\n"
        "'Honestly, I'm not a huge fan of cooking — I find it quite time-consuming after a long day at school. "
        "But I do enjoy baking occasionally, especially when I'm stressed. "
        "There's something really satisfying about making something from scratch.'",
        "差异分析：高分回答有真实的观点（不太喜欢）、具体细节（压力大时烘焙）、情感色彩（satisfying）",
        "Part 1不需要正确答案，需要真实自然、有细节的回答")

    make_pain_point(prs, "Part 1 答题过短问题", [
        "'Do you like reading?' → 'Yes, I like reading.'（完全没展开）",
        "每题都以'Yes/No, I think...'开头（公式化）",
        "理由全是'because it is interesting/useful/good'",
        "答完第一句就停下，等考官追问",
    ], [
        "开头不用Yes/No，直接给细节：'Reading is something I genuinely enjoy...'",
        "用'and what I particularly like is...'自然延伸第二点",
        "理由具体化：不说'interesting'，说'it challenges my thinking every time'",
        "答完主要内容后加一句举例/个人经历，自然结束",
    ])

    make_summary(prs, 2,
        ["Part 1：答案+原因+细节=2-3句，不长不短",
         "用真实观点和具体细节替代模板和空洞词汇",
         "开头多样化：不要总是Yes/No，直接进入内容"],
        ["准备20个Part 1高频话题，每个话题写出3句自然回答",
         "每天用手机录音练习5个Part 1问题，听回放找问题",
         "替换词练习：把昨天说过的'good/nice/like'都换掉"])

    # ════════ L03 Part 2 题卡独白 ════════
    make_lesson_title(prs, 3, "Part 2\n题卡独白精讲", [
        "掌握1分钟准备时间的高效利用方法",
        "学会用5W1H框架构建2分钟流畅故事",
        "建立高分故事的情感层次和细节技巧",
        "备考30个Part 2核心话题，举一反三",
    ])
    make_content(prs, "L03 · Part 2 1分钟准备策略", [
        ("第1步（5秒）",   "快速看清题卡要求：Describe a... + 4个提示点（WHO/WHAT/WHEN/WHY）"),
        ("第2步（20秒）",  "确定1个具体的人/事/地点/物品——越具体越好（不要泛指）"),
        ("第3步（30秒）",  "在题卡空白处写5-8个关键词（不要写完整句子）"),
        ("第4步（5秒）",   "决定结尾：为什么难忘/有什么影响/有什么感受"),
        ("注意",           "准备时间内可以用中文思考，但关键词用英文写，避免翻译卡顿"),
    ])

    make_content(prs, "L03 · 2分钟独白结构框架", [
        ("开场（10秒）",   "I'd like to talk about... / The [person/place/thing] I want to describe is..."),
        ("背景（20秒）",   "When/Where + basic context（时间地点背景，1-2句）"),
        ("主体（70秒）",   "按题卡提示点展开，每个点2-3句；加入感官描述和情感"),
        ("高光细节（20秒）","一个最难忘的具体细节/场景/对话——让考官记住你"),
        ("结尾（10秒）",   "总结感受：That experience really taught me... / I'll always remember..."),
        ("计时练习",       "第一次可能1分10秒或2分30秒，目标是1分45秒-2分15秒"),
    ])

    make_example(prs, "L03 · Part 2 范例全文",
        "题卡：Describe a meal you enjoyed eating. You should say: where you ate it / what you ate / "
        "who you were with / and explain why you enjoyed it.\n\n"
        "I'd like to talk about a meal I had about six months ago at a small Cantonese restaurant tucked "
        "away in an old neighbourhood in Shenzhen — it wasn't fancy at all, but the food was absolutely incredible.\n"
        "I went there with my grandmother, who grew up in that area and knew the owner personally. "
        "We ordered steamed fish, braised pork belly, and a clay pot rice — all classic Guangdong dishes.\n"
        "What made it particularly special was watching my grandmother chat with the chef in Cantonese, "
        "sharing stories about how the neighbourhood had changed over the decades.",
        "这段回答得分点：具体地点+人物情感+感官描述+文化细节——非常authentic，不像背诵",
        "避免虚构故事：用真实经历更自然，考官能感受到genuine情感")

    make_two_col(prs, "L03 · Part 2 三十大话题举一反三",
        "人物类（Person）", [
            "a person who has influenced you → 老师/家长/朋友",
            "someone you admire → 同上，换角度",
            "a child you know → 弟弟妹妹/邻居小孩",
            "an elderly person → 爷爷奶奶，谈传统与智慧",
            "a successful person → 可以用同一个人物，换侧重点",
        ],
        "地点类（Place）", [
            "a place you like to visit → 深圳某个公园/商场/老街",
            "a city you want to visit → 谈向往，用现在时和条件句",
            "a historical place → 可讲深圳改革开放历史",
            "a place in nature → 海边/山顶/公园",
            "a restaurant/café → 细节最丰富，推荐常备",
        ])

    make_summary(prs, 3,
        ["准备时间：定人/事/物→写关键词→规划结尾感受",
         "内容结构：背景→主体（4个提示点）→高光细节→感受总结",
         "时长目标：1分45秒-2分15秒，太短被追问，太长被打断"],
        ["每天练习1个Part 2话题，录音后分析：有没有达到1分45秒？",
         "准备5个'万能人物'和5个'万能地点'，可以回答多种话题",
         "阅读高分Part 2范文，标注细节词汇和情感表达，模仿使用"])

    # ════════ L04 Part 3 深度讨论 ════════
    make_lesson_title(prs, 4, "Part 3\n深度观点表达", [
        "掌握Part 3的PEEL论证结构",
        "学会表达同意、不同意、中立观点",
        "建立社会类话题的观点词库",
        "练习从个人延伸到社会层面的思维方式",
    ])
    make_content(prs, "L04 · Part 3 PEEL答题框架", [
        ("P — Point 观点",      "直接给出明确立场：I think... / In my view... / Personally speaking..."),
        ("E — Explain 解释",    "解释原因/逻辑：This is because... / The main reason is that..."),
        ("E — Example 举例",    "具体例子/数据/场景：For instance / Take China as an example..."),
        ("L — Link 收尾",       "总结或回扣观点：So overall... / That's why I believe... / It seems to me that..."),
        ("时间目标",             "每个Part 3问题：4-6句话，25-45秒，不少于20秒"),
    ], note="Part 3最低分回答：只有P没有EEL。深圳学生普遍说完观点就停，不会论证展开。")

    make_content(prs, "L04 · 社会类话题词汇库", [
        ("科技话题", "technological advancement / digital divide / data privacy / AI-driven / connectivity"),
        ("教育话题", "academic pressure / rote learning / critical thinking / holistic development"),
        ("环境话题", "carbon footprint / sustainable development / renewable energy / ecological impact"),
        ("社会话题", "socioeconomic disparity / work-life balance / urbanisation / ageing population"),
        ("文化话题", "cultural heritage / globalisation / cultural homogenisation / intergenerational gap"),
        ("连接词",   "On the one hand... / Conversely... / Nevertheless... / It's worth noting that..."),
    ])

    make_example(prs, "L04 · Part 3 低分 vs 高分对比",
        "问题：Do you think technology has changed the way people communicate?\n\n"
        "❌ 低分（5.5分）：\n"
        "'Yes, I think technology changed communication. Now people use phone and internet. "
        "It is faster and more convenient. But sometimes people don't meet face to face.'\n\n"
        "✅ 高分（7分）：\n"
        "'Absolutely — I think technology has transformed communication in both positive and challenging ways. "
        "On one hand, platforms like WeChat and Zoom allow people to stay connected across vast distances "
        "instantly, which was unimaginable a generation ago. However, I do worry that the depth of connection "
        "has diminished — people tend to send quick messages rather than having meaningful conversations. "
        "So while connectivity has improved, the quality of communication may have actually declined.'",
        "高分要素：转折(however)、具体细节(WeChat/Zoom)、抽象概念(depth of connection)、平衡观点",
        "Part 3不需要'正确答案'，需要有立场、有逻辑、有细节的英文论证")

    make_summary(prs, 4,
        ["PEEL框架：观点→解释→例子→总结，每个Part 3问题最少4句话",
         "社会类话题词汇：科技/教育/环境/文化各备10个核心词组",
         "展示思辨能力：给出平衡观点比只说'好/坏'更能拿高分"],
        ["用PEEL框架回答20个Part 3经典问题，录音后对照7分示范",
         "每天阅读一篇英文时评（The Guardian/BBC），摘抄5个观点词组",
         "练习从Part 2个人话题自然延伸到Part 3社会问题"])

    # ════════ L05 流利度提升 ════════
    make_lesson_title(prs, 5, "流利度\n& 连贯性提升", [
        "减少无效停顿(um/er/uh)的技巧",
        "掌握自然的过渡与连接词系统",
        "学会用填充语(filler)争取思考时间",
        "建立英语思维，减少翻译依赖",
    ])
    make_content(prs, "L05 · 自然停顿 vs 无效停顿", [
        ("无效停顿（扣分）", "um... er... uh... （超过3次/分钟开始影响FC评分）"),
        ("有效停顿（不扣分）","短暂停顿+思考词：Well... / Let me think... / That's interesting..."),
        ("升级版填充语",     "That's a great question — I'd say... / It's hard to generalise, but..."),
        ("语速建议",         "不追求快！自然节奏>快速背诵；考官评的是流利，不是语速"),
        ("英语思维训练",     "每天5分钟：用英文自言自语（描述周围的事物/当天的计划）"),
    ])

    make_two_col(prs, "L05 · 连接词分类使用指南",
        "顺序与递进", [
            "First of all / To begin with（第一点）",
            "What's more / Additionally（补充）",
            "In particular / Especially（强调）",
            "Above all / Most importantly（最重要）",
            "Finally / Last but not least（收尾）",
        ],
        "转折与对比", [
            "However / Nevertheless（然而）",
            "On the other hand（另一方面）",
            "In contrast / Whereas（对比）",
            "Despite this / Even so（尽管如此）",
            "That said / Having said that（话虽如此）",
        ])

    make_summary(prs, 5,
        ["流利≠快，而是：停顿自然、节奏稳定、连接词丰富",
         "用有效填充语替代um/er：'Well...'/'Let me think...'",
         "英语思维：每天5分钟英文自言自语是最高效的FC训练"],
        ["录音5分钟自由口语，统计um/er出现次数，目标每分钟<3次",
         "整理20个个人常用连接词，本周内全部在口语中自然使用",
         "挑战：连续用英文思考一件事10分钟（不允许中文）"])

    # ════════ L06 词汇资源 ════════
    make_lesson_title(prs, 6, "词汇资源\n精准提升", [
        "建立口语词汇替换系统，消灭单调词",
        "掌握地道搭配(collocation)的使用",
        "学习口语惯用语和习语(idiom)的正确场景",
        "LR从6分到7分的核心词汇策略",
    ])
    make_content(prs, "L06 · 高频单调词替换词库", [
        ("good/great替换",   "remarkable / outstanding / genuinely enjoyable / exceptionally well-done"),
        ("interesting替换",  "thought-provoking / captivating / fascinating / eye-opening"),
        ("important替换",    "crucial / pivotal / of great significance / plays a vital role"),
        ("big/large替换",    "substantial / considerable / massive / extensive"),
        ("a lot of替换",     "a significant number of / a wide range of / countless / numerous"),
        ("make me happy替换","gives me a sense of fulfillment / brings me immense joy / I find it deeply rewarding"),
    ], note="LR 7分标准：能使用不常见词汇且用法自然准确，有意识地避开最高频词汇。")

    make_content(prs, "L06 · 地道口语搭配 Collocations", [
        ("时间搭配", "spend time on / invest time in / waste time doing / make the most of my time"),
        ("问题搭配", "tackle a problem / address an issue / overcome a challenge / deal with difficulties"),
        ("影响搭配", "have a profound impact on / exert influence over / leave a lasting impression"),
        ("学习搭配", "acquire knowledge / broaden my horizons / sharpen my skills / pursue academic goals"),
        ("感受搭配", "feel a sense of / be struck by / be overwhelmed by / find it fulfilling"),
        ("习语使用", "适量使用1-2个习语增色，不要堆砌：'hit the nail on the head / open a can of worms'"),
    ])

    make_summary(prs, 6,
        ["LR提分关键：不是背更多单词，而是准确使用不常见词汇",
         "地道搭配比单个高级词更重要——'tackle a problem'比'solve'更地道",
         "习语：了解并能自然使用2-3个，不要刻意堆砌"],
        ["整理个人口语中出现频率最高的10个词，每个找3个替换词",
         "每天背5个Collocation（带例句），在当天口语练习中使用",
         "找1篇高分Part 2范文，标出所有不常见词汇，整理到词汇本"])

    # ════════ L07 语法范围 ════════
    make_lesson_title(prs, 7, "语法范围\n& 准确性", [
        "掌握口语中必须展示的5类句型结构",
        "时态运用：过去/现在/将来/假设的准确切换",
        "学会用从句、条件句增加句子复杂度",
        "GRA从6分到7分的关键语法错误规避",
    ])
    make_content(prs, "L07 · 口语必备5类句型", [
        ("条件句 If",         "If I had the chance, I would... / If technology continues to develop, we might..."),
        ("比较句",            "...is far more... than... / compared with X, Y seems considerably more..."),
        ("让步从句",          "Although/Even though... / Despite the fact that... / While I understand that..."),
        ("强调结构",          "What really matters is... / It's the quality, not the quantity, that counts"),
        ("被动语态",          "is widely regarded as / has been significantly influenced by / was established in"),
    ])

    make_example(prs, "L07 · 语法提升：改写练习",
        "原句（5.5分语法）：\n"
        "'I think technology is good. It help people do many things. We can communicate with friends far away. "
        "Also we can find information quickly. But sometimes technology is bad for children.'\n\n"
        "改写目标（7分语法）：请注意时态准确性、句子多样性、从句使用：",
        "改写示范（7分）：\n"
        "'I genuinely believe that technology has had a transformative impact on our daily lives. "
        "It enables us to communicate with people across the globe almost instantly, which would have seemed "
        "impossible a few decades ago. That said, I do have concerns about its influence on younger generations, "
        "particularly in terms of screen time and its effect on social skills.'",
        "关键改进：has had(现在完成时)、which从句、would have seemed(虚拟语气)、particularly(副词增色)")

    make_summary(prs, 7,
        ["GRA 7分：3种以上不同句型+时态基本准确+偶有小错无伤大雅",
         "重点练：条件句/让步从句/比较句——这三类最能提升句子复杂度",
         "时态：Part 1现在时为主，Part 2过去时为主，Part 3现在/将来为主"],
        ["用5类句型分别造5个口语场景句子，录音练习",
         "找一篇自己之前的录音，用改写练习方法升级语法",
         "每天语法练习：把5句简单句改写成复合句"])

    # ════════ L08 发音与语调 ════════
    make_lesson_title(prs, 8, "发音与语调\n自然提升", [
        "识别并纠正深圳学生的高频发音错误",
        "掌握英语语调的升降调规律",
        "学会通过语调传递情感和确信度",
        "发音(P)从6分到7分的关键技巧",
    ])
    make_content(prs, "L08 · 深圳学生高频发音问题", [
        ("th发音", "think=sink(错) → 舌尖轻触上齿背，气流穿过 [θ]；this/that中[ð]有振动"),
        ("r/l区分", "rice≠lice；right≠light → r：舌尖不碰上颚，向后卷；l：舌尖轻触上颚"),
        ("词尾辅音", "desk末尾k要完整发出；band末尾d要发出；不要吞音"),
        ("重音位置", "PREsent(n.礼物) vs preSENT(v.呈现)；REcord(n.) vs reCORD(v.)"),
        ("语调单调", "陈述句结尾降调↓；一般疑问句结尾升调↑；列举用升降升降↓"),
    ], note="发音评分标准：不要求英美口音，要求清晰易懂+语调自然。广东口音本身不扣分！")

    make_content(prs, "L08 · 英语语调规律", [
        ("信息焦点词",  "句子中最重要的词要重读：I LOVE cooking（不是i love COOKING）"),
        ("情感语调",    "兴奋：音调高、语速略快；沉思：音调低沉、语速慢"),
        ("强调技巧",    "在关键词前微微停顿、拉长元音：'It was ab-so-lutely incredible'"),
        ("连接时语调",  "and/but前通常稍停、降调，然后and/but升调继续"),
        ("结尾语调",    "观点最后一句降调→表示确定；升调→表示不确定/开放态度"),
    ])

    make_summary(prs, 8,
        ["P 7分：清晰易懂+语调自然+重音正确，广东口音不扣分",
         "重点攻克：th发音、词尾辅音、句子重音",
         "语调比发音更重要：单调的语调比偶尔发音错更影响分数"],
        ["每天跟读10个含th的句子：think/through/although/worthwhile",
         "录音并播放自己说的5个句子，听是否有语调变化",
         "找一个英语youtuber或播客主持人，模仿其语调和重音习惯"])

    # ════════ L09 高频话题词汇库 ════════
    make_lesson_title(prs, 9, "高频话题\n词汇系统备考", [
        "整合30个IELTS口语高频话题的核心词汇",
        "学会话题词汇的灵活迁移",
        "建立个人口语话题资料库",
        "针对深圳学生薄弱话题重点突破",
    ])
    make_two_col(prs, "L09 · 深圳学生薄弱话题 vs 强项话题",
        "薄弱话题（需重点准备）", [
            "Nature & Environment（很少接触大自然）",
            "Historical places & Traditions（文化类话题词汇少）",
            "Rural vs Urban life（深圳学生生活单一）",
            "Art & Music（兴趣类话题缺乏细节）",
            "Helping others & Volunteering",
            "Childhood memories（回忆类不善用过去时）",
        ],
        "相对强项（可作为展示点）", [
            "Technology & Social Media（深圳科技氛围浓）",
            "Shopping & Consumer culture",
            "Study & Academic life",
            "Food & Restaurants",
            "City life & Infrastructure",
            "Career & Future plans",
        ])

    make_content(prs, "L09 · 万能话题模板素材（Nature/Environment）", [
        ("场景",     "I once visited Dameisha Beach in Shenzhen / Wutong Mountain..."),
        ("描述词",   "pristine / breathtaking scenery / lush greenery / tranquil atmosphere"),
        ("感受词",   "I felt a profound sense of peace / it was a welcome escape from the city"),
        ("环保词",   "carbon footprint / biodiversity / ecosystem / deforestation / conservation"),
        ("话题延伸", "lack of exposure to nature among urban youth / impact of rapid urbanisation"),
    ], note="准备2-3个'万能场景'：一次旅行、一段经历、一个人物——可以用于回答多种话题。")

    make_summary(prs, 9,
        ["薄弱话题不是回避，而是准备足够的素材和词汇来应对",
         "2-3个万能故事素材可以改造回答20+种不同题目",
         "深圳学生的优势话题（科技/城市）要充分展示"],
        ["为5个薄弱话题各准备一段80词的核心素材，背熟关键词",
         "整理个人话题资料库：30个话题×10个核心词汇",
         "找考友进行模拟口语考试，互相评分"])

    # ════════ L10 模拟考试 & 复盘 ════════
    make_lesson_title(prs, 10, "全真模拟\n& 系统复盘", [
        "完成一次全流程模拟口语考试（严格计时）",
        "建立考场心理建设系统",
        "学会自我评估和持续提高的方法",
        "制定考前一周口语冲刺计划",
    ])
    make_content(prs, "L10 · 考场心理建设与节奏控制", [
        ("进考场前", "深呼吸3次；提醒自己：考官不是评判者，是对话者"),
        ("开场白",   "直接进入回答，不要说'I am nervous'或过度客套"),
        ("答不上来", "用'That's an interesting question...'争取2-3秒，然后诚实作答"),
        ("说错了",   "自然纠正：'Sorry, I meant to say...'，不要停顿太久"),
        ("考官打断", "这是正常的！说明时间到了，不是回答有问题"),
        ("结束语",   "考官说'That's the end of the test'后不要继续说话"),
    ])
    make_content(prs, "L10 · 考前一周口语冲刺", [
        ("D-7至D-5", "每天完整模拟一次Part 1+2+3（约15分钟），录音留存"),
        ("D-4",      "重听录音，对照评分标准自评FC/LR/GRA/P各项"),
        ("D-3",      "重点练习薄弱项，复习个人词汇替换词表"),
        ("D-2",      "用英文聊天：任何话题说5分钟，保持口感"),
        ("D-1",      "轻松模拟1次Part 1，不练Part 2/3，保留精力"),
        ("D-Day",    "考前30分钟：用英文在脑海中给自己一次'热身'介绍"),
    ])

    make_summary(prs, 10,
        ["口语7分不是靠背模板，而是靠大量真实练习积累的自信",
         "考场最重要的是：沉着→扩展→不停顿过多",
         "录音回听是最高效的自我提升工具，坚持到考试当天"],
        ["本课后：完成一次完整模拟考（录音），发给老师批改",
         "考前维持：每天15分钟口语练习，不间断",
         "目标复盘：对比第1课录音和现在录音，看清进步"])

    prs.save(path)
    print(f"[OK] Speaking PPT → {path}")

if __name__ == "__main__":
    build("/home/user/data-analysis/ielts_ppts/IELTS_Speaking_深圳提分版.pptx")
