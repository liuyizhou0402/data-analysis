"""IELTS Writing L01-L10 PPT Builder — Purple Theme"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import ppt_utils as U

OUT = os.path.join(os.path.dirname(__file__), 'writing')
os.makedirs(OUT, exist_ok=True)

def T():
    U.set_theme(U.RGBColor(0x47,0x24,0x73), U.RGBColor(0xF2,0xA0,0x1D),
                U.RGBColor(0xF3,0xE5,0xF5), U.RGBColor(0x2C,0x0D,0x47),
                '写作','IELTS Writing')

def part(p,idx,tc,te,concs,conts,exs):
    U.section(p,idx,tc,te)
    for c in concs: U.concept(p,c[0],c[1],c[2],note=c[3] if len(c)>3 else None)
    for c in conts: U.content(p,c[0],c[1],note=c[2] if len(c)>2 else None)
    for e in exs:   U.example(p,e[0],e[1],answer=e[2],tip=e[3] if len(e)>3 else None)

# ─────────────────────────────────────────────────────────────────
#  L01  写作考试全貌与评分标准
# ─────────────────────────────────────────────────────────────────
def L01():
    T(); p = U.new_prs()
    U.cover(p,'写作',1,'写作考试全貌\n& 评分标准精解','Writing Overview & Scoring Criteria')
    U.agenda(p,['考试结构与两个任务','四维评分标准详解','Task 1 vs Task 2策略差异','深圳学生常见失分模式','备考框架与提分路径','本课学习目标'])
    part(p,1,'写作考试结构总览','IELTS Writing: Test Structure',
        [('考试基本信息','Writing Test Overview',
          [('总时间','60分钟——Task 1（20分钟）+ Task 2（40分钟）'),
           ('Task 1','描述图表/流程图/地图——最少150词'),
           ('Task 2','议论文/讨论文——最少250词'),
           ('分值比例','Task 1占总写作分1/3，Task 2占2/3——Task 2更重要'),
           ('深圳学生弱点','词汇单调+句子结构单一+Task 2论证不足')]),
         ('四维评分标准','4 Assessment Criteria',
          [('TA 任务完成度','Task Achievement——是否完整回应题目要求'),
           ('CC 连贯衔接','Coherence & Cohesion——段落组织+衔接词使用'),
           ('LR 词汇资源','Lexical Resource——词汇丰富度+准确度'),
           ('GRA 语法多样性','Grammatical Range & Accuracy——语法多样+准确')])],
        [('评分标准权重理解',
          ['四项各占25%——均等权重，哪一项弱都会影响分数\n\nBand 6 vs Band 7的核心差距：\nTA（任务完成）：Band 6=回应题目但不够完整\n                Band 7=清晰完整回应，立场明确\nCC（连贯）：Band 6=有段落但衔接词不灵活\n            Band 7=有效组织，衔接词自然多样\nLR（词汇）：Band 6=词汇够用但重复/不准确\n            Band 7=词汇丰富，搭配自然\nGRA（语法）：Band 6=简单句为主，偶有错误\n             Band 7=多种复杂句型，准确率高']),
         ('Task 1 vs Task 2评分重点差异',
          ['Task 1（图表描述）评分重点：\nTA：准确描述主要趋势/特征，选择关键数据\nCC：按逻辑顺序描述，段落清晰\nLR：数据描述词汇（increase/decline/fluctuate）\nGRA：各时态准确（过去时/现在完成时）\n\nTask 2（议论文）评分重点：\nTA：清晰表明立场，论点有支撑，结论有力\nCC：段落结构清晰（引言/主体/结论）\nLR：学术词汇+意见表达词汇\nGRA：条件句/让步从句/被动语态'])],
        [('深圳学生失分诊断',
          '深圳学生最常见写作失分原因（按频率）：\n\n1. Task 2立场不明确（TA失分最大原因）\n→ 开头段没有表明自己的观点\n\n2. 词汇重复（LR失分）\n→ "important"出现5次，没有用同义词替换\n\n3. 全篇只用简单句（GRA失分）\n→ 缺乏从句/条件句/复杂句型\n\n4. 段落没有主题句（CC失分）\n→ 每段开头不知道这段讲什么\n\n5. Task 1没有概述句（TA失分）\n→ 直接写数据，没有整体趋势概述',
          '失分优先级：先解决TA（立场/概述）→再解决LR（词汇多样）→再解决GRA（句式多样）',
          '深圳学生实际情况：通常TA和GRA失分最多——这两项最影响Band分'),
         ('Band 6→7写作提分路径',
          '6.0→6.5：\n① Task 2：每篇写完整立场（开头+结尾）\n② 每段有主题句+支撑+例子\n③ 避免词汇重复：每个核心词备3个同义词\n\n6.5→7.0：\n① 复杂句型占50%以上（条件句/让步/被动）\n② Task 1：必写概述（Overview）段\n③ 衔接词自然多样（不机械使用Furthermore）\n④ 学术词汇替换日常词（significant vs big）',
          '最快提分：先提高Task 2（占2/3分值）——Task 2提0.5分等于总写作分提0.5分')]
    )
    part(p,2,'任务完成度（TA）精解','Task Achievement in Depth',
        [('Task 1的TA要求','Task Achievement for Task 1',
          [('概述','必须有Overview段——总结最主要的趋势/特征（不是细节）'),
           ('关键数据','选择最重要的数据描述——不是每个数据都写'),
           ('准确性','数据引用必须准确——不能改变原图信息'),
           ('比较','有比较时必须比较——不能忽略最高/最低/差距'),
           ('词数','至少150词——低于150词在TA项扣分')]),
         ('Task 2的TA要求','Task Achievement for Task 2',
          [('立场明确','开头段必须表明自己的立场/观点'),
           ('全面回应','题目有两个问题都要回答——不能只答一个'),
           ('论证充分','每个观点都要有解释+例子/理由支撑'),
           ('结论有力','结论段必须重申立场，不能只是总结'),
           ('词数','至少250词——低于250词在TA项扣分')])],
        [('Task 1 TA高分vs低分示范',
          ['低分Task 1（Band 5-6）TA问题：\n"The graph shows data about sales from 2010 to 2020. In 2010, sales were 100. In 2011, they were 120. In 2012, they were 150..."\n→ 问题：只列数据，没有概述整体趋势，没有选择关键数据\n\n高分Task 1（Band 7+）TA特点：\n"Overall, sales showed a consistent upward trend over the decade, with particularly dramatic growth between 2015 and 2018. The most notable feature is that sales tripled by 2020."\n→ 优点：有概述（Overall），指出主要趋势，选择了最关键特征']),
         ('Task 2 TA高分vs低分示范',
          ['低分Task 2（Band 5-6）TA问题：\n开头："Nowadays, many people think that technology has changed our lives. This essay will discuss this topic."\n→ 问题：没有立场，泛泛而谈，不知道作者赞成还是反对\n\n高分Task 2（Band 7+）TA特点：\n开头："While technology has undoubtedly transformed modern life, I firmly believe that its benefits significantly outweigh the drawbacks, particularly in terms of communication and access to information."\n→ 优点：立场明确（believe...outweigh），有具体理由预告'])],
        [('Task 1概述句写法示范',
          '图表：折线图显示英国和法国1990-2020年能源消耗\n\n低分概述："This graph shows energy consumption in the UK and France."\n（只是描述图表内容，没有趋势）\n\n中分概述："Overall, both countries showed changes in energy consumption over the period."\n（太模糊，没有具体说明变化方向）\n\n高分概述："Overall, while the UK experienced a notable decline in energy consumption over the period, France maintained relatively stable levels with only minor fluctuations."\n（清晰对比两国趋势，指出关键差异）',
          '概述写法三要素：①Overall开头 ②不写具体数据 ③概括最主要的趋势/特征/差异',
          '概述是Task 1最重要的段落——没有概述，TA项最高只能Band 5'),
         ('Task 2立场表达示范',
          '题目："Some people think that social media has a negative impact on society. To what extent do you agree or disagree?"\n\n弱立场："Social media has both positive and negative effects on society."\n→ 没有表明是否同意——不回应题目\n\n强立场："I strongly agree that social media has predominantly negative effects on society, largely due to its damaging impact on mental health and the spread of misinformation."\n→ 清晰立场（strongly agree）+预告理由（mental health/misinformation）',
          '立场表达模板：I [firmly/strongly/partially] agree/disagree because [理由预告]')]
    )
    part(p,3,'连贯衔接（CC）精解','Coherence & Cohesion in Depth',
        [('段落结构要求','Paragraph Structure Requirements',
          [('主题句','每段第一句——说明这段讲什么（不能没有）'),
           ('支撑句','解释/论证主题句——至少2-3句'),
           ('例子/证据','支撑论点——举具体例子更有说服力'),
           ('结尾句（可选）','总结本段要点或过渡到下段'),
           ('段落长度','每段约80-120词——太短太长都不好')]),
         ('衔接词使用规范','Cohesive Devices: Rules',
          [('功能要匹配','添加用Furthermore/Moreover；转折用However/Nevertheless'),
           ('不过度使用','每段用1-2个衔接词——不是每句都要衔接词'),
           ('位置正确','衔接词通常在句首或句中——不在句尾'),
           ('代词指代','It/They/This指代清晰——不能指代不明'),
           ('避免机械','不要"First, Second, Third"机械使用')])],
        [('段落CC示范对比',
          ['低分段落（CC不足）：\n"Social media is bad. It causes problems. People use it too much. This is harmful for health. There are many issues."\n→ 问题：句子间没有逻辑连接，重复简单，没有主题句支撑\n\n高分段落（CC良好）：\n"The most significant negative effect of social media is its detrimental impact on mental health. Research suggests that excessive use is associated with higher rates of anxiety and depression, particularly among young people. For instance, a 2019 study found that teenagers who spent more than three hours daily on social media were twice as likely to report symptoms of depression. This evidence clearly indicates that unrestricted social media use poses serious risks to psychological wellbeing."\n→ 优点：主题句清晰，有研究支撑，有例子，有结论句']),
         ('衔接词功能分类速查',
          ['添加递进：Furthermore / Moreover / In addition / Additionally\n\n转折对比：However / Nevertheless / Despite this / On the other hand\n\n因果关系：Therefore / Consequently / As a result / Hence\n\n举例说明：For example / For instance / Such as / Including\n\n结论总结：In conclusion / To summarise / Overall / In short\n\n条件关系：Provided that / As long as / Unless / If'])],
        [('CC结构示范：Task 2主体段',
          '论点：公共交通投资能减少城市拥堵\n\n主题句（TS）："Investing in public transportation is one of the most effective solutions to urban congestion."\n\n支撑（支撑1）："When cities expand affordable and efficient transit networks, many commuters choose to leave their cars at home, directly reducing traffic volumes on major roads."\n\n例子（Example）："For example, Singapore\'s Mass Rapid Transit system, combined with high car ownership taxes, has helped maintain one of the lowest traffic congestion rates among Asian megacities."\n\n结论（Conclusion）："This demonstrates that well-funded public transport is a proven strategy for congestion reduction."',
          'TS→支撑→例子→结论 = 高分段落四部分结构',
          '每段只讲一个论点——主题句、支撑句、例子都服务于同一个核心论点'),
         ('CC常见问题修正',
          '问题1：段落跑题（主题句和支撑不一致）\n原文TS："Public transport reduces congestion."\n支撑句："People in cities also have health problems."\n→ 修正：支撑句必须直接论证主题句\n\n问题2：衔接词使用错误\n错误："However, public transport is beneficial for cities. Furthermore, it also helps environment."\n→ 分析："However"暗示转折，但前后没有转折关系\n→ 修正：改用"Moreover"或"Additionally"\n\n问题3：过度使用相同衔接词\n问题："Firstly...Secondly...Thirdly...Fourthly..."\n→ 修正：交替使用不同衔接词',
          'CC最常见问题：每段没有主题句——先解决这个问题')]
    )
    part(p,4,'词汇与语法精解','Lexical Resource & Grammar Range',
        [('词汇资源（LR）要求','Lexical Resource Requirements',
          [('词汇丰富','同一意思用不同词表达——避免重复'),
           ('搭配准确','正确使用词语搭配（collocations）'),
           ('词形准确','正确使用词性（名/动/形/副）'),
           ('学术词汇','使用AWL词汇替换日常词'),
           ('拼写准确','拼写错误降低LR分——尤其是常用词')]),
         ('语法多样性（GRA）要求','Grammatical Range Requirements',
          [('多种句型','简单句+并列句+复合句混合使用'),
           ('从句使用','定语从句/状语从句/名词从句——高分必须有'),
           ('被动语态','学术写作常用被动——适当使用'),
           ('条件句','If/Unless句型——表达假设'),
           ('准确率','复杂句用错不如不用——宁准确不复杂')])],
        [('LR词汇替换示范',
          ['核心词汇替换示例：\n\n❌ 低分（重复词汇）：\n"Important factors include education. Education is very important. The most important thing is economic development."\n→ important出现3次，无变化\n\n✓ 高分（词汇多样）：\n"Crucial factors include education, which plays a pivotal role in development. The most significant driver of progress, however, is economic growth, which is indispensable for social advancement."\n→ important→crucial/pivotal/significant/indispensable']),
         ('GRA句型示范',
          ['简单句：Solar energy is clean and renewable.\n\n并列句：Solar energy is clean, and it is also increasingly affordable.\n\n复合句（定语从句）：Solar energy, which produces no carbon emissions, is increasingly being adopted worldwide.\n\n复合句（状语从句）：Although initial installation costs are high, solar energy saves money in the long run.\n\n条件句：If governments invest in renewable energy, carbon emissions could be significantly reduced.\n\n被动语态：Solar panels have been installed on millions of homes worldwide.\n\n高分目标：每两段至少有2种不同的复杂句型'])],
        [('LR高频词汇替换表',
          '积累以下替换词对（IELTS写作高频）：\n\nimportant→ significant/crucial/vital/pivotal/indispensable\nbig/large→ substantial/considerable/vast/enormous/extensive\nshow→ demonstrate/indicate/suggest/reveal/illustrate\nproblem→ challenge/issue/concern/drawback/obstacle\nhelp→ assist/facilitate/enable/support/contribute to\nchange→ transform/alter/modify/shift/evolve\nuse→ utilise/employ/apply/implement/adopt\nneed→ require/demand/necessitate',
          '替换词使用规则：意思完全相同才替换——不能为了替换而用错意思'),
         ('GRA复杂句练习',
          '将以下简单句改写为复杂句：\n\n原句1："Technology is useful. It helps us communicate.\"\n目标：合并为含定语从句的复杂句\n\n原句2："We should invest in education. The economy will improve."\n目标：改写为条件句\n\n原句3："The government introduced the policy. Air quality improved."\n目标：改写为因果复合句',
          '参考答案：\n1. Technology, which helps us communicate more efficiently, has become indispensable in modern life.\n2. If we invest in education, the economy will improve significantly.\n3. Following the government\'s introduction of the new policy, air quality improved considerably.',
          '改写三步：①确定两句关系（定语/条件/因果）②选对连接词③检查语法正确')]
    )
    part(p,5,'备考框架与提分路径','Study Plan & Score Improvement',
        [('写作备考核心原则','Core Study Principles',
          [('输入先于输出','先大量读Band 7-8范文——了解高分长什么样'),
           ('每天练习','写作技能必须靠练习积累——不能只背理论'),
           ('计时练习','每次练习严格计时——培养考场时间感'),
           ('反馈循环','写完后对照评分标准自评——或请人批改'),
           ('积累词汇','每天10个学术词汇+5个高频搭配')]),
         ('4周提分计划','4-Week Score Improvement Plan',
          [('第1周','读10篇Band 7+范文，分析段落结构和词汇'),
           ('第2周','每天写1个Task 2主体段（100词），重点TA+CC'),
           ('第3周','每天写1篇完整Task 2（计时40分钟），重点LR+GRA'),
           ('第4周','全真模考：Task 1+Task 2（60分钟），全面分析')])],
        [('写作提分路径图',
          ['从Band 5到Band 7的提升路径：\n\nBand 5→5.5：基础结构建立\n→ 每篇Task 2都有引言+主体2段+结论\n→ 每段有主题句\n→ 词数达到250词以上\n\nBand 5.5→6：内容质量提升\n→ 立场明确，论证有支撑\n→ Task 1有Overview段\n→ 开始使用衔接词\n\nBand 6→6.5：语言质量提升\n→ 词汇开始多样化\n→ 有复杂句型（定语从句/状语从句）\n→ 错误减少到每段1-2处\n\nBand 6.5→7：精细化提升\n→ 词汇丰富且准确（搭配正确）\n→ 复杂句型多样且准确\n→ 论证深度和例子质量提升']),
         ('深圳学生备考时间建议',
          ['如果距离考试1个月：\n每天：Task 2完整一篇（40分钟）+Task 1（20分钟）\n重点：先解决TA（立场/概述）→再提升LR/GRA\n\n如果距离考试2-3个月：\n第1个月：专项训练（段落结构+词汇积累）\n第2个月：Task 1和Task 2分别精练\n第3个月：全真模考+弱点突破\n\n如果只有1-2周：\n每天至少写1篇Task 2\n重点记住开头句模板+段落结构\n不要追求语言完美，先保证结构和内容完整'])],
        [('写作自我评分练习',
          '用4维评分标准自评以下段落（满分各1分）：\n\n"In my opinion, environmental problems are very serious today. Many countries have pollution problems. For example, China and India have air pollution. I think governments should do more. People also need to change their habits. This is very important for our future."\n\nTA（任务完成）：/1\nCC（连贯衔接）：/1\nLR（词汇资源）：/1\nGRA（语法多样）：/1',
          'TA=/0.5（有观点，但论证不充分）\nCC=/0.5（有衔接词For example，但段落结构弱）\nLR=/0.5（词汇重复：very/important/problems，学术词汇少）\nGRA=/0.5（全是简单句，没有复杂句型）\n总体约Band 5-5.5',
          '改进版：用significant/crucial替换very+important，加入定语从句，加入原因说明'),
         ('L01总结：备考起点确认',
          '本节课学完后，你应该：\n\n1.了解写作考试结构（Task 1: 150词20分钟，Task 2: 250词40分钟）\n2.知道四维评分标准（TA/CC/LR/GRA各25%）\n3.识别了自己的主要失分原因\n4.制定了4周备考计划\n5.知道Task 2比Task 1更重要（占2/3分值）\n\n下节课：Task 1图表描述精讲——折线图+柱状图+饼图',
          '立即行动：今天写一段Task 2主体段（80-100词），用4维标准自评')]
    )
    U.model_answer(p,'Band 7 Task 2引言段示范',
        '题目："Many people believe that individuals are responsible for solving environmental problems, while others think that it is the government\'s responsibility. Discuss both views and give your own opinion."',
        '高分引言段：\n"The question of who bears primary responsibility for addressing environmental challenges has generated considerable debate. While some contend that individual lifestyle choices are the key to sustainability, others argue that only governmental policies can deliver meaningful change at scale. In my view, although individual actions play a role, the responsibility lies predominantly with governments, whose unique power to legislate and fund large-scale environmental initiatives makes them the most effective agents of change."\n\n分析：\n• TA：清晰立场（predominantly with governments），预告理由\n• CC：转折对比结构（While...others），逻辑清晰\n• LR：contend/sustainability/legislate/initiatives（学术词汇丰富）\n• GRA：让步从句（although）+定语从句（whose）',
        ['引言三段式：背景介绍→两方观点概述→表明立场',
         'whose引导定语从句：高分语法标志（governments, whose power...）',
         'predominantly比absolutely更准确——避免极端词']
    )
    U.model_answer(p,'Band 7 Task 1概述段示范',
        '图表：折线图显示四个国家（美国/中国/英国/德国）1980-2020年二氧化碳排放量（百万吨）\n美国：从5000→6000→5500（峰值2005年）\n中国：从2000→5000→10000（持续增长）\n英国：从600→500→400（持续下降）\n德国：从700→600→400（持续下降）',
        '高分概述段（Band 7+）：\n"Overall, the most striking trend is the dramatic and sustained rise in China\'s CO₂ emissions, which contrasted sharply with the declining patterns seen in both the UK and Germany. The United States, while remaining the largest emitter for much of the period, showed a slight reduction from its peak in the mid-2000s."\n\n分析：\n• 没有具体数据（概述不写数字）\n• 最主要趋势都覆盖（中国上升/英德下降/美国先升后降）\n• 用了比较（contrasted sharply with）\n• 语言学术（sustained rise/declining patterns）',
        ['概述规则：①用Overall开头 ②不写具体数字 ③覆盖最主要趋势 ④指出最突出特征',
         'contrasted sharply with：比较两组数据的高分表达',
         'for much of the period：时间表达的学术替换（不写具体年份）']
    )
    U.compare(p,'Task 1 vs Task 2 核心差异',
        'Task 1（图表描述）',
        ['时间：20分钟，最少150词',
         '任务：客观描述图表数据和趋势',
         '立场：不发表个人意见',
         '必须有：Overview（概述）段',
         '评分重点：准确性+概述质量'],
        'Task 2（议论文）',
        ['时间：40分钟，最少250词',
         '任务：表明立场，论证观点',
         '立场：必须有明确个人观点',
         '必须有：清晰引言，立场明确',
         '评分重点：论证深度+词汇语法']
    )
    U.compare(p,'Band 6 vs Band 7 写作对比',
        'Band 6 特征',
        ['立场：有观点但不够清晰',
         '结构：有段落但主题句弱',
         '词汇：够用但重复较多',
         '语法：简单句为主，有错误',
         'Task 1：有数据描述但无Overview'],
        'Band 7 特征',
        ['立场：开头段立场非常清晰',
         '结构：每段主题句+支撑+例子',
         '词汇：丰富多样，搭配准确',
         '语法：复杂句型多样且准确',
         'Task 1：有Overview，选择关键数据']
    )
    U.steps(p,'写作考场60分钟标准流程',
        [('0-2分钟','读题：Task 1图表类型+Task 2题目类型和要求'),
         ('2-5分钟','Task 2审题：确认题型+立场+2-3个论点（先想再写）'),
         ('5-20分钟','写Task 1（150词）：概述+细节描述'),
         ('20-25分钟','Task 2审题+提纲：引言立场+主体2-3段论点+结论'),
         ('25-57分钟','写Task 2（250词+）：引言+主体段+结论'),
         ('57-60分钟','快速检查：词数+拼写+标点+首段立场是否清晰')]
    )
    U.drill(p,'当堂练习：四维评分快速识别',
        '判断以下写作问题属于哪个评分维度（TA/CC/LR/GRA）',
        [('写作问题识别','问题1：Task 2开头段没有表明立场 → 维度？\n问题2：全文重复使用"important"5次 → 维度？\n问题3：所有句子都是简单句（主谓宾结构）→ 维度？\n问题4：段落之间没有衔接词 → 维度？\n【答案】问题1=TA / 问题2=LR / 问题3=GRA / 问题4=CC'),
         ('自我诊断','你目前写作最弱的维度是：___\n你计划从哪个维度开始提升：___\n理由：___\n【答案】建议优先顺序：TA（最影响分数）→CC（段落结构）→LR（词汇）→GRA（语法）')])
    U.tip_card(p,'写作5大高频原则',
        [('原则1：Task 2立场第一','引言段必须清晰表明立场——不能模棱两可'),
         ('原则2：每段主题句','每个主体段第一句说明这段讲什么'),
         ('原则3：词汇不重复','每个核心词准备3个同义词，交替使用'),
         ('原则4：有复杂句型','每段至少1个从句——条件句/定语从句/让步从句'),
         ('原则5：Task 1必须Overview','Task 1概述段必写——没有最高Band 5')])
    U.tip_card(p,'写作评分标准速查卡',
        [('TA（任务完成）','Task 2立场明确+论证充分 / Task 1有Overview+准确描述'),
         ('CC（连贯衔接）','段落有主题句+衔接词自然多样+指代清晰'),
         ('LR（词汇资源）','词汇丰富不重复+搭配准确+学术词汇使用'),
         ('GRA（语法多样）','复杂句型多样+时态准确+被动/条件/让步句型')])
    U.tip_card(p,'Task 2时间分配（40分钟）',
        [('审题立场（3分钟）','仔细读题，确认题目类型，决定立场方向'),
         ('列提纲（5分钟）','引言立场+2-3个论点+例子框架+结论要点'),
         ('写作（28分钟）','引言5分钟+主体各8分钟+结论5分钟'),
         ('检查（4分钟）','检查词数+立场清晰+拼写+首句是否有主题句')])
    U.tip_card(p,'Task 1时间分配（20分钟）',
        [('审图（2分钟）','看图表类型+时间范围+单位+主要趋势'),
         ('提纲（2分钟）','确定Overview内容+要描述的关键数据'),
         ('写作（14分钟）','Overview段4分钟+细节段各5分钟'),
         ('检查（2分钟）','数据准确+词数达标+动词时态正确')])
    U.vocab(p,'写作高频词汇：趋势描述（Task 1）',
        [('increase','→ rise/grow/surge/climb/soar/escalate'),
         ('decrease','→ fall/drop/decline/plummet/shrink/reduce'),
         ('remain stable','→ plateau/stabilise/level off/maintain/stay constant'),
         ('reach highest','→ peak at/reach a peak/hit a high of'),
         ('fluctuate','→ vary/oscillate/fluctuate/experience variations'),
         ('significant','→ notable/substantial/considerable/dramatic/marked'),
         ('slightly','→ marginally/modestly/fractionally/gradually'),
         ('rapidly','→ sharply/steeply/dramatically/swiftly')])
    U.vocab(p,'写作高频词汇：观点表达（Task 2）',
        [('I think','→ I firmly believe/I would argue/In my view/I contend'),
         ('important','→ crucial/vital/significant/indispensable/pivotal'),
         ('bad','→ detrimental/harmful/adverse/negative/damaging'),
         ('good','→ beneficial/advantageous/positive/constructive/valuable'),
         ('many people','→ a significant proportion/the majority/numerous individuals'),
         ('because','→ due to/owing to/as a result of/given that/since'),
         ('so','→ therefore/consequently/hence/as a result/thus'),
         ('although','→ while/whereas/despite/even though/notwithstanding')])
    U.two_col(p,'写作备考：6.0→7.0提分路径',
        '6.0→6.5（前4周）',
        ['每天写1篇Task 2（计时40分钟）',
         '重点：每篇都有明确立场+主体段主题句',
         '积累每个核心词3个同义词（每天5组）',
         '每周写3篇Task 1，练习Overview段',
         '目标：TA和CC维度达到Band 6.5'],
        '6.5→7.0（后4周）',
        ['引入复杂句型（定语/让步/条件从句）',
         '每篇Task 2自评LR词汇多样性',
         '读5篇Band 7+范文，分析语言特点',
         'Task 1练习：多种图表类型（折线/柱状/饼图）',
         '目标：LR和GRA维度达到Band 7']
    )
    U.checklist(p,'L01学完自测：写作基础掌握度',
        ['知道Task 1（20分钟150词）和Task 2（40分钟250词）的要求',
         '理解四维评分标准（TA/CC/LR/GRA）各占25%',
        '知道Task 2立场必须在引言段明确表明',
         'Task 1知道必须写Overview（概述）段',
         '找出了自己最弱的写作维度并制定了改进计划',
         '建立了写作备考的每日练习计划'])
    U.summary(p,1,
        ['写作考试：Task 1（20分钟/150词/图表）+ Task 2（40分钟/250词/议论文）',
         '四维评分：TA任务完成 + CC连贯衔接 + LR词汇资源 + GRA语法多样——各占25%',
         'Task 2占总写作分2/3——优先提升Task 2分数',
         'Task 2必须：引言立场明确，每段主题句，论证有支撑，结论重申立场',
         'Task 1必须：有Overview概述段，不写个人意见，数据描述准确'])
    U.homework(p,1,
        ['写一篇Task 2（250词，计时40分钟），用4维标准自评每项得分',
         '读2篇Band 7 Task 2范文，标出：立场句/主题句/衔接词/复杂句型',
         '建立词汇替换本：为important/show/increase/problem各找3个同义词'],
        est_time='约2小时')
    U.two_col(p,'Task 1 vs Task 2：词汇使用策略差异',
        'Task 1（图表描述）',
        ['数据动词：increase/decline/remain/peak/fluctuate',
         '程度副词：significantly/slightly/dramatically/gradually',
         '比较表达：compared to/higher than/twice as much',
         '时间表达：between X and Y/over the period/by 2020',
         '禁止：不用个人观点词（I believe/in my opinion）'],
        'Task 2（议论文）',
        ['观点词：I firmly believe/I would argue/it is evident',
         '让步词：while/although/despite/even though',
         '因果词：consequently/therefore/as a result/hence',
         '例子词：for instance/for example/such as',
         '结论词：in conclusion/to summarise/overall']
    )
    U.two_col(p,'写作高分：深圳学生实例分析',
        '学生A（Band 5.5→6.5提升）',
        ['弱点：Task 2没有立场，论证空洞',
         '改进：每篇先写立场句（I firmly believe...）',
         '弱点：词汇重复（important用了8次）',
         '改进：建立同义词卡片，写前先确认替换词',
         '结果：6周后从5.5→6.5'],
        '学生B（Band 6.5→7.5提升）',
        ['弱点：全是简单句，GRA很低',
         '改进：每段至少写1个复杂句（从句/条件句）',
         '弱点：Task 1没有Overview段',
         '改进：每篇Task 1必须先写Overall句',
         '结果：8周后从6.5→7.5']
    )
    U.two_col(p,'写作常见误区澄清',
        '误区（许多学生相信）',
        ['误区1：字数越多分越高',
         '误区2：用华丽词汇就能高分',
         '误区3：Task 1要写个人意见',
         '误区4：段落越多越好',
         '误区5：结论段只需要重复前面说的'],
        '正确理解',
        ['正确1：250/150词基础上，质量>数量',
         '正确2：用词准确+多样>用华丽词用错',
         '正确3：Task 1客观描述，不写观点',
         '正确4：Task 2通常3-4段最合适',
         '正确5：结论段要重申立场，可加建议']
    )
    U.two_col(p,'四维评分模拟评分练习',
        '练习段落A',
        ['"People should use public transport more. It is good for the environment. Many countries have this problem. We need to solve it."\n\nTA：/1 □\nCC：/1 □\nLR：/1 □\nGRA：/1 □\n总评：Band___'],
        '参考评分',
        ['TA：0.5（有观点，但无论证无例子）',
         'CC：0.5（无主题句，无有效衔接词）',
         'LR：0.5（good/problem/solve等低级词）',
         'GRA：0.5（全是简单句，无从句）',
         '总评：约Band 5']
    )
    U.two_col(p,'写作30天入门计划（深圳初学者）',
        '第1-10天：结构建立',
        ['每天：写1段Task 2主体段（80词）',
         '重点：主题句+支撑句+例子三部分',
         '积累：每天5个核心写作词汇',
         '读：每天读1篇Band 7范文段落'],
        '第11-30天：质量提升',
        ['第11-20天：完整Task 2（250词，计时）',
         '重点：引言立场+段落质量+结论重申',
         '第21-30天：Task 1+Task 2联合练习',
         '重点：所有维度达到Band 6水平']
    )
    U.two_col(p,'写作L01→L10学习路线图',
        'L01-L05：基础技能',
        ['L01：评分标准+备考框架（本节）',
         'L02：Task 1图表描述精讲',
         'L03：Task 1 流程图/地图/表格',
         'L04：Task 2引言与结论写法',
         'L05：Task 2主体段论证技术'],
        'L06-L10：进阶强化',
        ['L06：Task 2题型专项（讨论/同意）',
         'L07：Task 2题型专项（优劣/建议）',
         'L08：词汇与语法精进',
         'L09：写作常见错误与修正',
         'L10：全真模考与冲刺提分']
    )
    U.preview(p,2,'Task 1图表描述精讲',
        ['折线图趋势描述方法','柱状图比较策略','饼图百分比表达'])
    U.save(p, f'{OUT}/L01_写作考试全貌与评分标准.pptx')
    print(f"  L01 done: {len(p.slides)} pages")
