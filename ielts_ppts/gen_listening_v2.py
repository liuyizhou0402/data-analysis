# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ppt_utils as U

OUT = os.path.join(os.path.dirname(__file__), "listening")
os.makedirs(OUT, exist_ok=True)

def theme():
    U.set_theme(U.RGBColor(0x0F,0x4C,0x5C), U.RGBColor(0x12,0xA5,0x94),
                U.RGBColor(0xE6,0xF3,0xF1), U.RGBColor(0x07,0x2B,0x34),
                '听力', 'IELTS Listening')

# ══════════════════════════════════════════════════════════════
def build_L01():
    theme(); p = U.new_prs()
    U.cover(p,'听力',1,'听力考试全貌\n& 失分诊断','Test Overview & Failure Diagnosis')
    U.agenda(p,['课程总览与学习路线','考试结构四个Section','10大题型速览',
                '分数换算与目标设定','深圳学生失分诊断','例题体验','课堂练习','小结作业'])
    U.content(p,'雅思听力课程路线图 Course Roadmap',[
        ('L01-02','考试全貌 + Section 1 日常对话满分'),
        ('L03-04','Section 2独白场景 + Section 3学术对话'),
        ('L05-06','Section 4学术讲座 + 预测与关键词定位'),
        ('L07-08','笔记速记系统 + 六大陷阱全解析'),
        ('L09-10','口音适应 + 全真模考与系统复盘'),
    ], note='每节课含真题练习，建议配合剑桥真题10-19同步使用')
    U.objectives(p,['掌握雅思听力四个Section的结构、难度与题量分布',
                    '了解10大题型的特点与解题思路',
                    '知晓6/7/8分所需正确题数及分数换算',
                    '完成个人失分原因诊断，制定提分策略'])
    U.pain_point(p,'为什么听懂了却还是做错？',
        ['听到关键词立即写答案，忽略后续转折（but/actually/however）',
         '单词拼写不确定：necessary / accommodation / February',
         'Section 3多人讲话，跟丢说话人，分不清谁的观点',
         '预读时间没利用好，题目还没看完录音已开始'],
        ['听完整句再写，特别注意转折词之后的内容',
         '建立高频拼写词表，每天5分钟听写训练',
         '做笔记标注说话人A/B/C，追踪各自立场',
         '优先预读题目关键词，预判答案信息类型'])
    # PART01
    U.section(p,1,'考试结构与Section梯度','Exam Structure & Section Difficulty')
    U.concept(p,'雅思听力四个Section概览',
        'Section难度从S1→S4递增，题型和场景各不相同',
        [('Section 1','日常对话，2人，最简单；预约/问路/租房场景，必须拿满分'),
         ('Section 2','独白，1人，社区/活动/设施介绍；地图和匹配题为主'),
         ('Section 3','学术讨论，2-4人；观点辨别是难点，最多丢分的Section'),
         ('Section 4','学术讲座，1人独白；专业词汇密集，拉开7+差距的关键'),
         ('总时长','约30分钟录音，纸笔考额外10分钟誊写；机考边听边输入，无誊写')],
        note='深圳学生Section 3平均失分率最高，因多人对话容易张冠李戴')
    U.content(p,'各Section核心参数对比',
        [('S1 题量','10题，全填空或表格，必须稳拿10/10'),
         ('S2 题量','10题，地图+匹配+MCQ组合，数字/地点是重点'),
         ('S3 题量','10题，MCQ为主（含Choose TWO），态度词是关键'),
         ('S4 题量','10题，笔记/摘要填空为主，AWL学术词汇最密集'),
         ('录音特点','只播放一次，不可倒带，必须实时答题')])
    U.content(p,'分数换算表 Band Score Conversion',
        [('Band 9','39-40题正确（误差率<3%）'),
         ('Band 8','35-37题正确（正确率87-92%）'),
         ('Band 7','30-31题正确（正确率75-77%）'),
         ('Band 6','23-25题正确（正确率57-62%）'),
         ('Band 5','15-17题正确（正确率37-42%）'),
         ('目标设定','目标7分→需稳定做对30题；每Section平均7-8题')],
        note='从6到7分需要额外做对约6题——这6题靠策略可以找到')
    U.concept(p,'纸笔考 vs 机考差异',
        '了解考试形式差异，按实际报考类型备考',
        [('纸笔考','30分钟听力+10分钟誊写；在题册上作答后誊写到答题卡'),
         ('机考','直接在屏幕上输入，无额外誊写时间；键盘打字速度影响答题'),
         ('机考优势','可修改答案、数字和字母更准确；中文输入法要提前切换'),
         ('机考注意','Backspace键才能删除，不能像纸笔考那样划掉重写'),
         ('备考建议','报名时确认考试类型；机考考生需额外练习打字速度')])
    U.example(p,'体验题：Section 1 信息表填空',
        'Questions 1-3: Complete the form. Write NO MORE THAN TWO WORDS AND/OR A NUMBER.\n\n'
        'Customer Name: __________ (Q1)\nPhone Number: __________ (Q2)\nDelivery Date: __________ (Q3)\n\n'
        'Script: "Hi, I\'d like to place an order. My name\'s Chen Wei — C-H-E-N, Wei — W-E-I.\n'
        'Best number is 07821 double 4, 369. And I\'ll need it by the 3rd of August."',
        'Q1: Chen Wei（注意：first + last name都要写，逐字母听写）\n'
        'Q2: 07821 443369（double 4 = 44，总共11位数字）\n'
        'Q3: 3 August 或 August 3（日期格式，数字+月份均可）',
        '限词"TWO WORDS AND/OR A NUMBER"：Q3写"3rd of August"超字数→0分；写"3 August"✓')
    U.example(p,'体验题：Section 4 笔记填空',
        'Complete the notes. Write NO MORE THAN TWO WORDS.\n\n'
        'Urban Microplastics Research\n'
        '• Main source: __________ from synthetic fabrics (Q31)\n'
        '• Found in: drinking water and __________ (Q32)\n\n'
        'Script: "Our study identified microfibre shedding from synthetic textiles as the primary\n'
        'source of urban microplastics. Alarmingly, these particles were detected in both tap\n'
        'water and the food supply of major cities..."',
        'Q31: microfibres / microfibre shedding（听原词，不需要改写）\n'
        'Q32: food supply（TWO WORDS，不能写"the food supply"——冠词+名词=两词但the不是关键信息）',
        'S4填空：答案几乎都是原词；听到学术长词先记首字母，誊写时再补全')
    # PART02
    U.section(p,2,'10大题型特点与策略','10 Question Types: Features & Strategies')
    U.content(p,'题型分类：填空类（最常见）',
        [('Form Completion 表格填空','日常信息：姓名/电话/地址/日期；S1为主；答案为原词'),
         ('Note Completion 笔记填空','半结构化笔记；S2/S4为主；注意词性匹配（空格前后词的词性）'),
         ('Table Completion 表格填空','行列对应信息；读题时找行列交叉点的信息类型'),
         ('Flow-chart Completion 流程填空','顺序描述；动词多见；被动语态常出现'),
         ('Summary Completion 摘要填空','连续段落摘要；注意同义替换；难度最高的填空题')],
        note='填空类占40题中的约60%，是得分基础——拼写和限词是主要失分原因')
    U.content(p,'题型分类：选择与配对类',
        [('Multiple Choice 单选','A/B/C三选一；注意转折词（but/however）后的内容才是答案'),
         ('Multiple Choice 多选','通常Choose TWO from FIVE；每项单独判断，不能凭感觉'),
         ('Matching 匹配','将选项A-H与问题配对；选项提前熟读；可能有多余选项'),
         ('Map/Plan Labelling 地图','方向词是核心；画箭头追踪路径；参照物先识别'),
         ('Sentence Completion 句子完成','答案为原词；注意前后语法搭配（冠词/词性）')])
    U.concept(p,'解题通用流程：PRCA四步法',
        '所有题型都遵循同一个解题流程，建立习惯比技巧更重要',
        [('P — Pre-read 预读','利用Section间隙预读题目，圈关键词，预判信息类型'),
         ('R — Respond 实时答题','边听边写，不等录音结束；不确定就写最可能的答案'),
         ('C — Check 即时核查','听完一道题立即看下一题，不在已过的题上纠结'),
         ('A — Amend 誊写核查','纸笔考：誊写时检查拼写、大小写、限词、复数')],
        note='PRCA是一个循环，不是线性的——P和R几乎同时进行')
    U.example(p,'预读练习：30秒能预判什么？',
        '给你30秒，预读以下题目并预判答案类型：\n\n'
        'Section 1 Q1-5 (Fitness Centre Enquiry)\n'
        '1. Member name: __________\n'
        '2. Membership type: __________ membership\n'
        '3. Monthly fee: £__________\n'
        '4. Start date: __________ (month)\n'
        '5. Special requirement: __________',
        'Q1: 人名（专有名词，注意大写，可能需要拼写）\n'
        'Q2: 形容词（annual/monthly/student/family等，修饰membership）\n'
        'Q3: 数字（价格，两位数可能性大，注意英镑符号不需要写）\n'
        'Q4: 月份名称（January-December，注意拼写）\n'
        'Q5: 名词短语（具体需求，不限定，听到什么写什么）',
        '预读时不要读完每个字——只需圈出填空位置前后的限定词，判断答案类型即可')
    # PART03
    U.section(p,3,'深圳学生失分诊断','Failure Pattern Diagnosis')
    U.content(p,'失分类型一：拼写与书写错误',
        [('高频拼错词',  'necessary(✗necesary) / accommodation(✗accomodation) / February'),
         ('字母混淆',    'm/n, u/v, e/a 在快速听写时最容易混淆'),
         ('大小写错误',  '专有名词首字母必须大写：Monday, London, Dr Smith'),
         ('数字书写',    '单词数字（fifteen）vs 阿拉伯数字（15）均可接受'),
         ('解决方案',    '建立个人拼写词表，每天5分钟听写练习；高频词100个先背')],
        note='拼写错误是最可惜的失分——你听对了却因写错而得0分')
    U.content(p,'失分类型二：陷阱识别不足',
        [('更正陷阱',  '"It was Tuesday... actually, sorry, I meant Wednesday" → 答案是Wednesday'),
         ('否定陷阱',  '"The room is NOT available on Friday" → 考生听到Friday就写，忘了NOT'),
         ('转折陷阱',  '"The price is £45... but with student discount it\'s £32" → 答案是32'),
         ('顺序陷阱',  '答案不按题目编号出现（尤其地图题）→ 要跳着找'),
         ('解决方案',  '听到but/actually/sorry/wait/I mean立即提高警觉，准备改写')],
        note='陷阱题约占总题数的30%——学会识别是从6分到7分的关键跨越')
    U.content(p,'失分类型三：时间管理失控',
        [('单题纠结',  '一道题想太久导致后面3题全部错过；单题上限1.5分钟'),
         ('预读不足',  'Section开始前没充分预读，被动听而非主动找'),
         ('Section换题慢','S1结束到S2开始有约20秒，必须用来预读S2前几题'),
         ('誊写出错',  '纸笔考最后10分钟誊写时粗心，把正确答案抄错'),
         ('解决方案',  '建立"不纠结"习惯：跟丢了立即放弃，找下一题的锚点')])
    U.example(p,'诊断练习：找出下列答案的错误类型',
        '录音："The next workshop will be on Thursday the 14th."\n'
        '考生A答案：Thursday ← 错误！（题目问的是日期NUMBER）\n\n'
        '录音："We have openings on Monday and Friday, but NOT Wednesday."\n'
        '考生B答案：Wednesday ← 错误！（否定陷阱，NOT Wednesday = 不开放）\n\n'
        '录音："Bring your student ID... actually, your passport will be fine too."\n'
        '考生C答案：student ID ← 错误！（更正陷阱，实际上passport也可以）',
        'A: 没有预读题目，不知道要填数字而非星期\n'
        'B: 没听NOT，只听到了关键词Wednesday\n'
        'C: 没听到actually表示更正，停在了第一个答案',
        '每次做题前先问：这里要填什么类型的信息？然后带着这个预期去听')
    # PART04
    U.section(p,4,'目标设定与学习计划','Goal Setting & Study Plan')
    U.content(p,'从现在的分数到目标分数：差距分析',
        [('当前6分→目标7分', '需要额外做对约6-7题；重点攻克S3多选和S4填空'),
         ('当前6.5→目标7',   '需要额外2-3题；通常是1个陷阱题+1个拼写题的差距'),
         ('当前7→目标8',     '需要额外5题；要求S1/S2基本满分+S3/S4高正确率'),
         ('真题使用建议',     '剑桥真题10-19按难度从低到高；先做15-16，再做17-19'),
         ('每周练习量',       '每周至少2套完整真题；做完必须分析错题类型')])
    U.content(p,'10节课学习计划与资源清单',
        [('必备资源',   '剑桥雅思真题集（10-19任选3本）；录音原文（text文件）'),
         ('推荐资源',   'BBC 6-Minute English（每集6分钟，英式口音，免费）'),
         ('推荐资源2',  'Australia Network（澳式口音）；VOA Everyday（美式速度适应）'),
         ('练习方式',   '精听（逐句对照原文）vs 泛听（整套计时）各占50%'),
         ('错题记录',   '建立错题本：题号/错误类型/正确答案/陷阱说明')])
    U.two_col(p,'计时模考 vs 精听分析：如何配合',
        '计时模考（每周1-2次）',
        ['严格按考试时间，不暂停，不回放',
         '做完后对答案，记录错题题号',
         '计算每个Section的正确率',
         '标注：听懂了做错的 vs 没听懂的',
         '目的：模拟真实考场压力'],
        '精听分析（每天20-30分钟）',
        ['选1-2段错题，反复听3-5遍',
         '对照原文找出每个错误的原因',
         '标注陷阱词、连读、弱读位置',
         '做影子跟读：模仿语速和语调',
         '目的：找到根本失分原因'])
    # PART05
    U.section(p,5,'高频词汇与表达','Key Vocabulary & Expressions')
    U.vocab(p,'Section 1高频场景词汇',
        [('appointment / booking','预约，预订（S1最高频单词）'),
         ('available / vacancy',  '有空/空缺（时间或座位）'),
         ('deposit / fee / charge','押金 / 费用 / 收费'),
         ('confirm / cancel / reschedule','确认 / 取消 / 改期'),
         ('membership / registration','会员资格 / 注册'),
         ('facilities / amenities', '设施（复数！不能漏s）'),
         ('enquiry / query',        '询问（英式拼法）'),
         ('receipt / invoice',      '收据 / 发票')])
    U.vocab(p,'数字类信息听力词汇',
        [('double / treble',        'double 4 = 44; treble 5 = 555'),
         ('o / zero / nought',      '零的三种读法：电话号用o，数学用zero/nought'),
         ('thirteen vs thirty',     '13: 重音在-teen；30: 重音在thir-；注意区分'),
         ('a quarter / half past',  '3:15 = a quarter past three；3:30 = half past three'),
         ('postcode format (UK)',    'SW1A 2AA：字母+数字+空格+数字+字母'),
         ('currency',               '£45.50 = "forty-five pounds fifty"（不说cents）'),
         ('percentage',             '35% = thirty-five percent（不省略percent）')])
    U.vocab(p,'Section 3/4学术场景词汇',
        [('hypothesis / thesis',    '假设 / 论点（学术写作和讨论的核心词）'),
         ('methodology / approach', '研究方法 / 方法'),
         ('data / findings / results','数据 / 发现 / 结果'),
         ('conclude / suggest',     '得出结论 / 提出建议（作者立场词）'),
         ('significant / substantial','显著的 / 相当大的（替换important）'),
         ('evaluate / assess',      '评估（常见动词，听到它后面跟目的或标准）'),
         ('implication / impact',   '含义 / 影响（结果类讨论常见词）')])
    U.two_col(p,'同义替换：题目 vs 录音',
        '题目关键词（你看到的）',
        ['start / begin → commence',
         'show / demonstrate → reveal',
         'important → crucial / pivotal',
         'problem → issue / challenge',
         'increase → rise / grow / surge',
         'location → place / venue / site'],
        '录音表达（你听到的）',
        ['approximately / around → about',
         'children → young people / kids',
         'expensive → costly / pricey',
         'often → frequently / regularly',
         'build → construct / develop',
         'use → utilise / employ / apply'])
    # PART06
    U.section(p,6,'方法精讲与真题范例','Method & Authentic Examples')
    U.steps(p,'考场听力全流程（Section间做什么）',
        [('考前准备','检查耳机/音量；翻到Section 1题目；做好心理准备'),
         ('S1开始前','利用说明时间预读Q1-5；圈关键词；预判信息类型'),
         ('S1-S2间隙','约20秒：立即翻到S2预读Q11-15（至少完成前5题）'),
         ('S2-S3间隙','预读S3题目；特别注意MCQ的选项A-E，要提前读熟'),
         ('S3-S4间隙','预读S4所有题目；S4最难，预读最关键'),
         ('全部结束后','纸笔考：用10分钟仔细誊写，边誊写边检查拼写')])
    U.steps(p,'笔记答题同步策略',
        [('Step 1','看题目→预判本题答案类型（数字/人名/地点/形容词）'),
         ('Step 2','听录音时在题目旁边快速记下听到的候选答案'),
         ('Step 3','确认后用笔在题目空格里写下最终答案'),
         ('Step 4','若跟丢：立即放弃，找下一题的位置关键词重新定位'),
         ('Step 5','每题答完不回头，视线移到下一题，保持向前')])
    U.model_answer(p,'高分笔记示范：S4讲座笔记格式',
        'Section 4: Urban Heat Island Effect',
        'Topic: Urban Heat Island (UHI) Effect\n'
        'Cause 1: impermeable surfaces (concrete/asphalt) → absorb more heat\n'
        'Cause 2: ↓ vegetation → less evapotranspiration\n'
        'Effect: urban temp ↑ 2-3°C cf. rural at night\n'
        'Impact: ↑ energy consumption (esp. air conditioning)\n'
        'Solution: green roofs + urban trees → reduce UHI',
        ['只记名词+数字+形容词，动词be和冠词全省略',
         '用符号↑↓→cf.替代文字，大幅提速',
         '括号()记补充细节，主线信息在外',
         '答案词单独圈出：impermeable / evapotranspiration'])
    U.model_answer(p,'地图题笔记示范：路径追踪法',
        'Section 2 Map Question: Museum Layout',
        'Entrance → straight ahead → past Gift Shop (L) →\n'
        'turn RIGHT at main hall → Café on LEFT (next to toilets)\n'
        'Continue straight → Children Gallery at FAR END\n'
        'NB: Temporary Exhibition = opposite entrance (NOT permanent)',
        ['在地图上用箭头→标路径，比文字更直观',
         'L/R标注，不写left/right节省时间',
         'NB标注例外情况，避免混淆',
         'FAR END/OPPOSITE等位置词用英文缩写'])
    U.compare(p,'答题策略对比：被动听 vs 主动找',
        '❌ 被动听（5-6分做法）',
        ['打开耳朵，等着答案出现',
         '没有预读，不知道下一题考什么',
         '听到感觉像答案的词就写下来',
         '跟不上就放弃，等Section结束',
         '誊写时随便抄，不检查拼写'],
        '✅ 主动找（7分做法）',
        ['提前预读题目，知道要找什么',
         '带着问题"这里需要填数字/人名？"去听',
         '听到候选词先记下，等确认后写',
         '跟丢立即用题号找下一个锚点',
         '誊写逐词检查：拼写/大小写/复数'])
    U.compare(p,'拼写习惯：随意写 vs 严格写',
        '❌ 拼写错误（直接0分）',
        ['accomodation（少一个m）',
         'Febuary（少r）',
         'enviroment（少n）',
         'independant（a应为e）',
         'occured（少r）'],
        '✅ 正确拼写（必须背会）',
        ['accommodation（双c双m）',
         'February（Feb-ru-ary）',
         'environment（environ-ment）',
         'independent（-ent结尾）',
         'occurred（双c双r）'])
    # PART07
    U.section(p,7,'课堂练习','Classroom Practice Drills')
    U.drill(p,'练习1：信息类型预判',
        '看下列填空题，预判每空需要填入的信息类型（人名/数字/月份/形容词等）',
        ['Club name: __________ FC （答：专有名词，球队名）',
         'Membership: __________ months （答：数字）',
         'Meeting day: every __________ （答：星期几）',
         'Contact: Dr __________ （答：姓名，注意Dr后面是姓）',
         'Website: www.__________.org.uk （答：单词，注意小写）'])
    U.drill(p,'练习2：数字快速听写',
        '跟着老师读出以下信息，迅速记录（模拟课堂听写）',
        ['Phone: 07734 double 6, 298 → 写出完整号码',
         'Price: forty-five pounds fifty → 写出数字格式',
         'Date: the twenty-third of March → 写出日期',
         'Time: quarter to nine in the morning → 转换为数字',
         'Postcode: GU12 3AX → 写出完整邮编'])
    U.drill(p,'练习3：更正陷阱识别',
        '以下句子各有一处更正，找出最终正确答案',
        ['"The event is on Friday the 8th... sorry, I mean Saturday the 9th."',
         '"Call us on 0800 44... wait, let me check... it\'s 0800 33, 578."',
         '"Wear something smart, like a jacket... actually, it\'s a casual event."',
         '"Bring your student card. Oh, and a passport is fine too if you prefer."',
         '更正信号词：actually / sorry / I mean / wait / let me correct that'])
    U.drill(p,'练习4：Section间隙预读计时',
        '计时30秒，看以下S3题目，你能预读完哪些内容？',
        ['Q21: What problem does Tom mention about the survey? A) too long  B) too difficult  C) low response rate',
         'Q22: What does Amy suggest as a solution? A) online format  B) shorter questions  C) reminder emails',
         'Q23-24: Choose TWO letters. What aspects did both students find useful?',
         'A) data analysis  B) interview practice  C) library resources  D) peer feedback  E) online tools'])
    U.drill(p,'练习5：听力速记符号实战',
        '用速记符号记录以下信息（尽量用→/↑↓/∴/w/等符号）',
        ['"Pollution increases as population grows." → 如何速记？',
         '"Technology leads to job losses, but also creates new opportunities." → 如何速记？',
         '"The research was conducted because of government funding." → 如何速记？',
         '"Water temperature rose significantly, especially in summer." → 如何速记？'])
    # PART08
    U.section(p,8,'避坑指南','Common Pitfalls to Avoid')
    U.pain_point(p,'Section 4崩溃场景',
        ['开头第一句话没听懂，后面整个乱，直接放弃后面9题',
         '遇到不认识的学术词（evapotranspiration），整个人卡住',
         '笔记写太多，手速跟不上，越写越乱',
         '第37题卡了3分钟，第38-40题完全没做'],
        ['跟丢了立即放弃，用题号找下一个锚点继续',
         '不认识的词：先用字母标音（evap-trans...），誊写时再补全',
         '笔记只记关键名词和数字，动词冠词全省略',
         '单题最多纠结1分钟，写下最可能的答案继续向前'])
    U.content(p,'常见错误：限词违规',
        [('违规1','写了3个词但限制是TWO WORDS → 直接0分，无论内容多正确'),
         ('违规2','写了NUMBER但限制是WORDS ONLY → 同样0分'),
         ('违规3','忽视了AND/OR：TWO WORDS AND/OR A NUMBER → 数字也算！'),
         ('检查步骤','誊写前再看一眼限词要求→数一下答案词数→确认无误再写'),
         ('安全原则','不确定时选更短的表达："twice a week"(3词)超限时写"weekly"')],
        note='限词违规是最冤枉的失分——明明知道答案却因写多了得0分')
    U.content(p,'常见错误：拼写与大小写',
        [('人名地名','必须首字母大写：Maria, London, Tuesday（不要全小写）'),
         ('普通名词','全小写：information, accommodation（不要随意大写）'),
         ('专业术语','按录音拼写；不确定时写最像的拼写，考官有一定容错'),
         ('复数问题','看空格前后：two ______ → 复数s；a ______ → 单数'),
         ('缩写',    'dept./ info. 在填空中不推荐使用，除非录音本身用了缩写')])
    U.tip_card(p,'听力四大速记卡',
        [('更正识别','听到actually/sorry/I mean/wait → 立即划掉之前的答案，等待更正后的内容'),
         ('预读优先','每段录音开始前的说明时间=最宝贵的30秒，必须全部用来预读题目'),
         ('跟丢策略','跟丢了不要慌：数一下当前到第几题，找下一题的位置词，立即跳到那里'),
         ('限词检查','写完每个答案立即核对：字数是否在限制内？拼写是否正确？')])
    U.tip_card(p,'不同Section得分心态',
        [('Section 1','最简单，必须拿满分10/10——如果错超过2题，说明预读没做好'),
         ('Section 2','目标8/10——地图题要认真练，匹配题选项提前读'),
         ('Section 3','目标6-7/10——多选题是难点，别因一道题影响全局'),
         ('Section 4','目标5-7/10——不要追求全对，确保做完全部题比全做对更重要')])
    U.checklist(p,'L01课后自检清单',
        ['我能说出四个Section的场景类型和难度顺序',
         '我知道7分需要做对约30题，8分需要35题',
         '我已经识别出自己的失分类型（拼写/陷阱/时间管理）',
         '我理解PRCA四步法并知道如何在考场中应用',
         '我已经了解纸笔考和机考的主要区别'])
    U.summary(p,1,
        ['四个Section难度梯度：S1最简单，S4最难，S3失分率最高',
         '7分=30题正确；提分关键是减少陷阱失分和拼写失分',
         'PRCA四步法：预读→实时答→即时核→誊写检'],
        takeaway='听懂了还做错=策略问题；没听懂=词汇问题——两个病因，两种药方')
    U.homework(p,1,
        ['完成剑桥真题任意一套S1+S2（不计时，练感觉）',
         '整理个人高频拼写错误词10个，制作单词卡',
         '下载BBC 6-Minute English，听1集并写出听到的3个关键信息'],
        est_time='约60分钟')
    U.preview(p,2,'Section 1 日常对话满分策略',
        ['四大高频场景详解（预约/租房/旅游/社区）',
         '数字信息精准捕捉专项训练',
         'Section 1零失分的预读模板'])
    U.save(p, f'{OUT}/L01_听力考试全貌与失分诊断.pptx')

# ══════════════════════════════════════════════════════════════
def build_L02():
    theme(); p = U.new_prs()
    U.cover(p,'听力',2,'Section 1\n日常对话满分策略','Section 1: Perfect Score Strategies')
    U.agenda(p,['上节回顾','四大高频场景分析','预读预测技术','数字信息专项',
                '字母拼读训练','例题精讲','课堂练习','小结作业'])
    U.review(p,['S1-S4难度梯度：S1最简单，必须满分10/10',
                'PRCA：预读→实时答→即时核→誊写检',
                '7分需要做对约30题；失分主要来自拼写+陷阱+时间管理'])
    U.objectives(p,['掌握Section 1四大高频场景的词汇与答题框架',
                    '能在30秒内完成S1题目预读并预判答案类型',
                    '精准捕捉数字类信息（电话/价格/时间/邮编）',
                    '实现Section 1稳定满分10/10'])
    U.pain_point(p,'S1为什么还会失分？',
        ['预读没做：录音已经开始，还在看上一道题',
         '数字听错：thirteen(13) vs thirty(30)，fourteen vs forty',
         '字母拼读跟不上：O-C-K-H-A-M，等反应过来已经过了',
         '只写了first name漏了last name（或反之）'],
        ['录音开始说明时间是黄金30秒，全部用来预读前5题',
         '13重音在-teen（后），30重音在thir-（前）——靠重音位置区分',
         '字母拼读：同步书写，O写圆圈，不等录音结束再写',
         '看到Name空格先预判：可能有两个空（first+last）'])
    # PART01
    U.section(p,1,'四大高频场景','Four Core Scene Types')
    U.concept(p,'场景一：预约类 Appointment/Booking',
        '雅思S1最高频场景，每年出现概率>60%',
        [('常见类型','牙医/诊所预约、健身房报名、图书馆预约、课程注册'),
         ('必考信息','姓名、联系方式、预约时间/日期、特殊要求/说明'),
         ('关键词信号','appointment/booking/schedule/available/slot'),
         ('答题要点','注意时间表达：9 o\'clock / half past ten / quarter to three'),
         ('典型陷阱','时间更改：先说Monday，后改成Tuesday，答案是Tuesday')],
        note='预约场景会先提供旧信息再修改——更正陷阱出现率极高')
    U.concept(p,'场景二：租房/住宿 Accommodation',
        '词汇量最大的S1场景，信息量大，类别多',
        [('常见类型','学生公寓、民宿、B&B、酒店房型选择'),
         ('必考信息','地址/邮编、租金/押金、设施、合同期限、入住日期'),
         ('关键词信号','rent/deposit/lease/utilities/furnished/available from'),
         ('数字密度高','价格/邮编/楼层/房间号——数字类信息集中出现'),
         ('典型陷阱','押金(deposit)和月租(rent)数字互换——听清"deposit"还是"monthly"')])
    U.concept(p,'场景三：旅游/设施 Tourism & Facilities',
        '信息多样，包含位置、时间、价格三类信息',
        [('常见类型','旅游景点介绍、博物馆/公园设施、活动/节目安排'),
         ('必考信息','开放时间、票价、地点/交通、特别活动日期'),
         ('关键词信号','opening hours/admission/tour/guided/closed on'),
         ('注意','"open every day EXCEPT Sunday"→这里考的是例外情况'),
         ('表格题策略','表格通常按行/列顺序介绍，先确认表头再找对应信息')])
    U.concept(p,'场景四：社区服务 Community Services',
        '信息最杂、词汇最广的S1场景',
        [('常见类型','图书馆服务、社区课程报名、投诉/建议热线、志愿者活动'),
         ('必考信息','服务内容、申请条件/资格、联系方式、截止日期'),
         ('关键词信号','membership/eligibility/register/volunteer/contact'),
         ('难点','同时出现多个相似服务，需要区分"哪个服务对应哪个条件"'),
         ('答题策略','先看题目中的分类词，再追踪对应类别的具体信息')])
    U.example(p,'预约场景实战例题',
        'Questions 1-5: Complete the form. Write NO MORE THAN ONE WORD AND/OR A NUMBER.\n\n'
        'CITY SPORTS CENTRE — Membership Application\n'
        'Member name: __________ Hargreaves (Q1)\n'
        'Type: __________ membership (Q2)\n'
        'Monthly fee: £__________ (Q3)\n'
        'Start date: 1st __________ (Q4)\n'
        'Locker number: __________ (Q5)\n\n'
        'Script: "...my first name\'s Patricia, P-A-T-R-I-C-I-A... I\'d like the family membership... '
        'that\'ll be thirty-two fifty a month... starting from the first of September... locker 47B..."',
        'Q1: Patricia（注意逐字母拼写P-A-T-R-I-C-I-A，同步书写）\n'
        'Q2: family（修饰membership的形容词）\n'
        'Q3: 32.50（thirty-two fifty，注意是月费不是年费）\n'
        'Q4: September（月份，首字母大写！）\n'
        'Q5: 47B（数字+字母，不要漏字母B）',
        'ONE WORD AND/OR A NUMBER：Q3可以写32.50（数字）或"thirty-two fifty"不能超过限制')
    U.example(p,'租房场景实战例题',
        'Questions 6-10: Complete the notes. Write NO MORE THAN TWO WORDS AND/OR A NUMBER.\n\n'
        'STUDENT ACCOMMODATION INQUIRY\n'
        'Property: 24 __________ Road (Q6)\n'
        'Monthly rent: £__________ (Q7)\n'
        'Deposit required: __________ months\' rent (Q8)\n'
        'Available from: __________ (Q9)\n'
        'Nearest station: __________ (Q10)\n\n'
        'Script: "...the address is 24 Birchwood Road—that\'s B-I-R-C-H-W-O-O-D... '
        'rent\'s £650 per month... we require two months\' deposit... available from mid-October... '
        'closest tube is Finchley Central..."',
        'Q6: Birchwood（路名，逐字母B-I-R-C-H-W-O-O-D，首字母大写）\n'
        'Q7: 650（数字，不需要写£符号）\n'
        'Q8: 2 / two（months，数字或单词均可）\n'
        'Q9: mid-October（两词，注意连字符mid-October是标准表达）\n'
        'Q10: Finchley Central（专有名词，两词，均大写）',
        'Q9两词限制：mid-October=TWO WORDS（mid+October），符合"TWO WORDS AND/OR A NUMBER"')
    # PART02
    U.section(p,2,'预读预测技术','Pre-reading & Prediction Techniques')
    U.content(p,'30秒预读的三个层次',
        [('第一层：确认题型','这道题是表格填空/选择/地图？——决定答题方式'),
         ('第二层：圈关键词','圈出题目中的名词/动词/数字——这是你要在录音中找的'),
         ('第三层：预判答案','根据上下文判断：空格要填什么类型的信息？'),
         ('时间分配',      '每题约3-4秒预读；重点在关键词，不读每个单词'),
         ('边预读边预测',  '"Monthly fee: £___" → 预测：两位数价格，如£35/£50/£65')])
    U.content(p,'预测答案类型的四个维度',
        [('词性预测','空格前后的词决定词性：a ___ centre = 形容词；the ___ of = 名词'),
         ('数值范围','fee/price → 两位数；year → 四位数；phone → 11位'),
         ('格式预测','date → 数字+月份；postcode → 字母数字混合'),
         ('语义范围','membership ___ → 可能是type/level/duration/benefit之一'),
         ('排除法',  '如果预测是月份，就能快速忽略数字，专注听month名称')])
    U.two_col(p,'30秒预读示范：你能预判什么？',
        '看题目（30秒）',
        ['Q1: Name: __________ (Mr/Mrs/Ms)',
         'Q2: Address: __________ Street',
         'Q3: Start time: __________ am',
         'Q4: Duration: __________ hours',
         'Q5: Equipment needed: __________'],
        '预测答案类型',
        ['Q1: 姓氏（专有名词，大写，可能拼读）',
         'Q2: 街道名称（专有名词，大写）',
         'Q3: 数字（如9, 10, 11, 10:30）',
         'Q4: 数字（1-4小时，可能是小数1.5）',
         'Q5: 具体物品名词（helmet/shoes/gloves等）'])
    U.example(p,'预读实战：Section间隙计时练习',
        '你有25秒（模拟S1→S2的间隙时间），请预读以下S2题目并记录你的预测：\n\n'
        'Section 2: Community Centre Facilities\n'
        'Q11: The centre was built in __________\n'
        'Q12: Opening hours on weekdays: __________ to 9pm\n'
        'Q13: The __________ has recently been renovated\n'
        'Q14: The centre is located on __________ Street\n'
        'Q15: Annual membership fee: £__________',
        'Q11: 年份（4位数字，如1985/2003）\n'
        'Q12: 时间（如7am/8am/9am）\n'
        'Q13: 具体设施名称（gym/pool/café/library等）\n'
        'Q14: 街道名（专有名词，大写）\n'
        'Q15: 数字（年费，可能是两/三位数）',
        '25秒预读5题 = 每题5秒；只圈关键词+预判类型，不读每个字')
    # PART03
    U.section(p,3,'数字信息专项训练','Number Information: Intensive Training')
    U.content(p,'电话号码听取技巧',
        [('英式格式','通常11位：07xxx xxxxxx（手机）；01xxx xxxxxx（座机）'),
         ('double/treble读法','double 4 = 44; treble 9 = 999（三连号）'),
         ('零的读法','电话中零读作"oh"；数学中读"zero"或"nought"'),
         ('听写策略','边听边写，不要等全部说完再写——前几位忘记了很难找回'),
         ('确认信号','说完后对方常说"got that?"或"is that clear?"——这是检查时机')])
    U.content(p,'价格与费用听取',
        [('整数','£45 = "forty-five pounds"（只需写45，不写£）'),
         ('小数','£32.50 = "thirty-two pounds fifty"或"thirty-two fifty"'),
         ('千位','£1,200 = "twelve hundred" 或 "one thousand two hundred"'),
         ('折扣','with 20% discount = 原价×80%；题目可能问折后价'),
         ('比较陷阱','"normal price is £60, but members pay £45"→题目若问member fee，答45')],
        note='价格题最常见的陷阱：先说原价，再说折扣价/会员价——答案是后者')
    U.vocab(p,'数字类关键表达速查表',
        [('a dozen','12（不是数字，是集合名词）'),
         ('a score','20（古英语，现仍用于某些场合）'),
         ('a quarter','1/4; a quarter past 3 = 3:15'),
         ('half past','30分：half past seven = 7:30'),
         ('to (time)','差：ten to eight = 7:50; quarter to = 差15分'),
         ("o'clock",'整点：eight o\'clock = 8:00（正式表达）'),
         ('midnight / noon','午夜12:00 / 正午12:00，注意区分')])
    U.example(p,'数字听写专项练习',
        '请听（或跟着老师读）以下信息，快速记录：\n\n'
        '1. "Our number is oh eight double oh, treble five, 69."\n'
        '2. "The fee is forty-two pounds fifty per month."\n'
        '3. "The event runs from half past six to quarter to nine."\n'
        '4. "The property is at number 14, and the postcode is BS7 4NQ."\n'
        '5. "Thirteen people signed up, not thirty — I said thirteen."',
        '1. 08005554 → 完整：0800 555 569\n'
        '2. £42.50（或42.50）\n'
        '3. 6:30 to 8:45（半past six=6:30；quarter to nine=8:45）\n'
        '4. 14; BS7 4NQ（字母大写，空格在4和N之间）\n'
        '5. 13（not 30！）——更正陷阱，听到"not thirty"说明先前信息是错的',
        '第5题：更正陷阱。"thirteen, not thirty" = 答案是13。听到not时立即改写')
    # PART04
    U.section(p,4,'字母拼读与表格填空','Spelling Dictation & Form Completion')
    U.content(p,'字母拼读接收训练',
        [('易混字母组','B/D/E/G/P/T/V/Z（发音相近，靠语境区分）'),
         ('B vs P','B(bee) vs P(pee): B尾音更低沉；P尾音更清晰'),
         ('M vs N','M(em) vs N(en): M双唇闭合；N舌尖上颚'),
         ('拼读信号','说话人通常会说"that\'s... B for Bravo"或直接拼'),
         ('同步书写','边听边写字母，不要等全部拼完再写——写了前3个再听后几个')],
        note='字母拼读是Section 1的必考技能，每年几乎100%出现')
    U.content(p,'表格填空的行列对应策略',
        [('先看表头','竖向表头=分类；横向表头=属性；先理解表格结构'),
         ('找行列交叉','每道题=某行某列的交叉点——预判这个位置应该填什么类型'),
         ('顺序规律','表格通常按从左到右、从上到下的顺序介绍'),
         ('注意单复数','表格中的名词注意前面是否有数量词决定单复数'),
         ('特殊格式','如果表头是"Price"，空格里填数字；是"Contact"，填电话/邮箱')])
    U.two_col(p,'字母NATO音标速查（最易混的字母）',
        '字母→NATO代号',
        ['A = Alpha', 'B = Bravo', 'C = Charlie', 'D = Delta',
         'E = Echo', 'F = Foxtrot', 'G = Golf', 'M = Mike'],
        '字母→NATO代号',
        ['N = November', 'P = Papa', 'Q = Quebec', 'R = Romeo',
         'S = Sierra', 'T = Tango', 'V = Victor', 'Z = Zulu'])
    U.example(p,'综合表格填空真题示范',
        'Complete the table. Write NO MORE THAN ONE WORD AND/OR A NUMBER.\n\n'
        'COMMUNITY LANGUAGE CLASSES\n'
        'Language | Day | Time | Room | Fee/month\n'
        'Spanish  | Mon | 7pm  | __(Q1)__ | £__(Q2)__\n'
        'Mandarin | __(Q3)__ | 6:30pm | 12 | £35\n'
        'French   | Wed | __(Q4)__ | 8 | £__(Q5)__\n\n'
        'Script: "Spanish is Monday evenings at 7, in room 4B, and that\'s thirty pounds a month.\n'
        'Mandarin runs on Thursdays, six-thirty, room 12, £35. French is Wednesdays at half past five,\n'
        'room 8, and the fee\'s twenty-eight fifty per month..."',
        'Q1: 4B（数字+字母，必须两者都写对）\n'
        'Q2: 30（thirty pounds，只写数字）\n'
        'Q3: Thursday（星期四，大写T）\n'
        'Q4: 5:30 / half past five（时间，数字格式最安全）\n'
        'Q5: 28.50（twenty-eight fifty）',
        '表格按行从左到右介绍；Spanish→Mandarin→French顺序不会变——利用顺序定位')
    # PART05
    U.section(p,5,'高频词汇与表达','Key Vocabulary')
    U.vocab(p,'预约场景高频词',
        [('make/book/schedule an appointment','预约（三种说法）'),
         ('cancel/reschedule/postpone',       '取消/改期/延后'),
         ('available / free / vacant',        '有空/空闲/空缺'),
         ('slot / opening / time frame',      '时间段（可以预约的）'),
         ('reminder / confirmation',          '提醒 / 确认（预约后的跟进）'),
         ('waiting list',                     '候补名单（满了但可以等）'),
         ('deposit / advance payment',        '订金 / 预付款')])
    U.vocab(p,'住宿场景高频词',
        [('fully furnished / unfurnished',    '全配家具 / 无家具'),
         ('utilities included / excluded',    '水电费包含/不包含'),
         ('landlord / tenant / agent',        '房东 / 租客 / 中介'),
         ('lease / tenancy agreement',        '租约（签订的合同）'),
         ('bond / security deposit',          '押金（退房时可退还）'),
         ('en-suite / shared bathroom',       '独立卫浴 / 共用卫浴'),
         ('ground floor / first floor',       '英式：地面层/一楼（≠美式）')])
    U.vocab(p,'数字表达精讲',
        [('£45.99',        'forty-five pounds ninety-nine'),
         ('07700 900123',  'oh-double seven-double oh-nine-double oh-one-two-three'),
         ('3:45pm',        'quarter to four in the afternoon'),
         ('SW1A 2AA',      'S-W-one-A [space] two-A-A（英式邮编格式）'),
         ('15th October',  'the fifteenth of October / October the fifteenth'),
         ('1,500',         'fifteen hundred / one thousand five hundred'),
         ('2.5 hours',     'two and a half hours / two hours thirty')])
    U.two_col(p,'S1陷阱词：听起来像但不是',
        '❌ 常见听错',
        ['thirteen → thirty（重音位置不同！）',
         'forty → fourteen',
         'sixty → sixteen',
         'deposit → discount（语境区分）',
         'Tuesday → Thursday（T开头均大写）',
         'address → Access（发音相近）'],
        '✅ 区分技巧',
        ['-teen重音在后（thir-TEEN）',
         '-ty重音在前（FOR-ty）',
         '同理：60 vs 16, 70 vs 17',
         '听前后语境：amount/pay → 钱',
         '日期题听完整句：on ___day the Xth',
         '信息类型预测帮助排除错误'])
    # PART06
    U.section(p,6,'方法精讲与范例','Methods & Models')
    U.steps(p,'Section 1 答题黄金流程',
        [('考试说明播放时','翻到Section 1，预读Q1-5的题目和关键词'),
         ('录音开始前30秒','利用题目说明继续预读Q6-10'),
         ('Q1-5录音阶段','边听边记，不确定先写候选词，确认后改写正式答案'),
         ('Q1-5结束短暂间隙','利用约10秒预读Q6-10（若之前没完成）'),
         ('Q6-10录音阶段','特别注意数字、名称、日期的精准记录'),
         ('Section结束','立即翻到S2，利用间隙预读S2前5题')])
    U.steps(p,'字母拼读同步书写法',
        [('准备','在空格旁边画格子，1个格子=1个字母'),
         ('接收','听到字母立即写入格子，不要等拼完再写'),
         ('易混','B/P/D听不清时：继续写后面的字母，回头从语境判断'),
         ('确认','通常说完会停顿，利用此时核对：逐字母与格子对照'),
         ('誊写','正式写到答题卡时核对字母顺序，注意大小写')])
    U.model_answer(p,'满分S1答题示范：预约类',
        'Fitness Centre Membership Form',
        'Q1: Catherine  [逐字母听: C-A-T-H-E-R-I-N-E，边听边写]\n'
        'Q2: annual  [年费会员，听到"yearly"=annual]\n'
        'Q3: 38  [thirty-eight pounds，只写数字]\n'
        'Q4: March  [下月1日开始，录音说"first of March"]\n'
        'Q5: Swimming pool  [TWO WORDS限制，不能写"the swimming pool"加the]',
        ['Q1：逐字母同步写入——每个字母一个格子，不等完整说完',
         'Q2：annual=yearly（同义替换）——不要只等"annual"这个词出现',
         'Q3：数字不写£符号——题目没标货币时不需要',
         'Q4：月份首字母大写，必须正确',
         'Q5：TWO WORDS限制注意冠词"the"不算在答案里'])
    U.model_answer(p,'高分vs失分：同一录音两种结果',
        'Script: "My name is Roberts — R-O-B-E-R-T-S. The fee is thirty-five pounds... '
        'actually, with the early-bird discount it\'s twenty-eight. I\'d like to start in May."',
        '失分答案：\n'
        'Name: Robert（漏了S）\n'
        'Fee: £35（没听到折扣，写了原价）\n'
        'Month: March（听到M开头就写March，忘了是May）\n\n'
        '满分答案：\n'
        'Name: Roberts（逐字母记：R-O-B-E-R-T-S）\n'
        'Fee: 28（听到"actually...discount...twenty-eight"=更正陷阱）\n'
        'Month: May（最后说的"start in May"才是答案）',
        ['Name：拼读要同步跟写每个字母，不能等说完再写',
         'Fee："actually + 数字" = 更正陷阱，后说的28才对',
         'Month：May不是March，M开头的月份有May/March/Monday——语境区分'])
    U.compare(p,'S1预读有无对比',
        '❌ 没预读（失分）',
        ['录音开始才看题目，第一题已经过了',
         '不知道Q3要填价格还是时间',
         '听到数字不知道是电话还是费用',
         '第一遍没听清，等第二遍——但没有第二遍'],
        '✅ 充分预读（满分）',
        ['说明播放期间已圈好Q1-5关键词',
         'Q3知道要填数字（价格）',
         '听到数字时已准备好写价格',
         '第一遍听到即记录，不靠第二遍'])
    # PART07
    U.section(p,7,'课堂练习','Practice Drills')
    U.drill(p,'练习1：字母拼读听写',
        '听老师拼读以下人名，快速记录（每个字母一格）',
        ['PRZYBYLSKI → 练习：P-R-Z-Y-B-Y-L-S-K-I（10个字母）',
         'MCDOUGALL → M-C-D-O-U-G-A-L-L（9个字母）',
         'FEATHERSTONE → F-E-A-T-H-E-R-S-T-O-N-E（12个字母）',
         'JOHANNSEN → J-O-H-A-N-N-S-E-N（9个字母）'])
    U.drill(p,'练习2：数字快速记录',
        '跟着老师/录音，记录以下数字信息（限时：每条5秒）',
        ['Phone: "zero seven, double eight, treble nine, four two six" → ?',
         'Price: "sixty-four pounds, seventy-five" → ?',
         'Time: "from quarter past eight to half past ten" → ?',
         'Date: "the twenty-first of November" → ?',
         'Postcode: "W-C-two, four-R-E" → ?'])
    U.drill(p,'练习3：更正陷阱识别',
        '以下每句话都有更正，写出最终正确答案',
        ['"The group meets every Tuesday... wait, it was changed to Thursday."',
         '"The fee is £40 per month... that\'s with discount, so normally it\'s £55."',
         '"Room 15... no, sorry, it\'s been moved to Room 50."',
         '"Contact Mr Johnson... actually, his colleague Ms Patel handles this."'])
    U.drill(p,'练习4：30秒预读计时',
        '计时30秒，看以下表格题，说出你的预测',
        ['Q1: Title: Mr/Mrs/Ms __________ →（空格类型？）',
         'Q2: Course duration: __________ weeks →（空格类型？）',
         'Q3: Preferred __________ →（空格类型？语境决定）',
         'Q4: Reference number: __________ →（空格类型？）',
         'Q5: Location: __________ campus →（空格类型？）'])
    U.drill(p,'练习5：表格行列定位练习',
        '老师描述以下信息，你需要找到表格中的正确位置填入',
        ['语言课表格：西班牙语，周二，晚上8点，B202教室，£28/月',
         '活动时间表：摄影课，每周三，下午2:30-4:30，限15人',
         '设施预约表：羽毛球场，周五下午，最多4人，需提前48小时预约',
         '套餐价格表：家庭套餐，含4人，月费£85，含网球+游泳'])
    # PART08
    U.section(p,8,'避坑指南','Pitfall Prevention')
    U.pain_point(p,'Section 1 满分障碍',
        ['听到double/treble没反应过来：oh-double-seven写成了0077',
         '人名只写了"James"没写"James Wilson"（漏了姓）',
         'S1结束后没有预读S2，间隙时间白白浪费',
         '表格题没看表头就开始答题，填到了错误的行'],
        ['双数字练习：double=两个相同，treble=三个相同，要立刻反应',
         'Name题：先看空格，有几个空？first/last要分别写',
         '每个Section结束立即翻页，利用间隙读下一Section前5题',
         '做题前5秒先理解表格结构：横轴是什么，纵轴是什么'])
    U.content(p,'S1高频错误：逐一击破',
        [('错误1：October vs November', '十月vs十一月——都是O/N开头，听清完整月份名称'),
         ('错误2：am vs pm',            '"nine thirty in the evening" = 9:30pm，不是am'),
         ('错误3：street vs road vs avenue','全部都是地址后缀，注意具体说的是哪个'),
         ('错误4：first floor vs ground floor','英式first floor = 美式second floor（二楼）'),
         ('错误5：£35 vs 35p',          '35 pounds ≠ 35 pence，听清"pounds"还是"pence"')],
        note='这5个错误在剑桥真题S1中反复出现，背会它们等于多拿2-3题')
    U.content(p,'誊写阶段自检清单（纸笔考）',
        [('字数检查','每个答案数一下词数，是否在限制内（ONE/TWO WORD限制）'),
         ('大小写','专有名词/月份/星期/人名→首字母大写；普通名词→小写'),
         ('复数检查','有数量词(two/several/many)→名词加s；无→单数'),
         ('拼写核对','快速默念每个字母：accomodation?→accommodation'),
         ('字迹清晰','数字1和7、4和9要写清楚；字母i和l、u和n要区分')])
    U.tip_card(p,'S1速记卡：四大必记',
        [('double/treble','double 4=44, treble 5=555；电话号码中常见；立刻反应不要犹豫'),
         ('更正信号词','actually/sorry/I mean/wait → 划掉之前写的，写新答案'),
         ('表格先看表头','读Q1之前先用5秒扫一眼整个表格的行列标题'),
         ('S1→S2间隙','Section结束音乐响起=立即翻页，开始预读S2，一秒不浪费')])
    U.tip_card(p,'数字陷阱速记卡',
        [('13 vs 30','13=thirTEEN（重音后），30=THIRty（重音前）；听重音位置'),
         ('价格更正','first price + "but/actually/discount" → 写second price（更低的）'),
         ('时间换算','quarter to 9 = 8:45；half past 5 = 5:30；养成秒转换习惯'),
         ('邮编格式','UK postcode: 字母+数字+空格+数字+字母（如SW1A 2AA）')])
    U.checklist(p,'L02 自检清单',
        ['我能区分13/14/15和30/40/50的发音规律',
         '我知道double/treble/nought在电话号码中的含义',
         '我能在30秒内预读5道S1题目并预判答案类型',
         '我已经练习了字母拼读同步书写法',
         '我知道S1满分的核心：预读+不纠结+拼写检查'])
    U.summary(p,2,
        ['S1四大场景：预约/租房/旅游/社区服务——各有核心词汇',
         '30秒预读三层次：题型→关键词→答案类型预判',
         '数字专项：13vs30靠重音；double/treble立即反应；价格更正听后说的'],
        takeaway='S1没有不应该满分的理由——失分100%来自预读不足或拼写不认真')
    U.homework(p,2,
        ['完成剑桥真题任意两套Section 1，严格计时，统计正确率',
         '字母拼读练习：从班级同学名字中选5个，互相拼读听写',
         '数字训练：每天听5个电话号码（从英美剧中找），记录并核对'],
        est_time='约45分钟')
    U.preview(p,3,'Section 2 独白场景攻略',
        ['地图/平面图题20个核心方向词',
         '匹配题选项提前读的策略',
         'Section 2独白的结构信号词'])
    U.save(p, f'{OUT}/L02_Section1日常对话满分.pptx')

# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Building L01..."); build_L01()
    print("Building L02..."); build_L02()
    print("Done. Checking...")
    from pptx import Presentation
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.pptx'):
            n = len(Presentation(os.path.join(OUT,f)).slides)
            print(f"  {n:3d} pages  {f}")
