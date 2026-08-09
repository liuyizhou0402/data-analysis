// TMGM Account Manager deck — institutional research styling
const PptxGenJS = require("pptxgenjs");

/* ---------------- design tokens ---------------- */
const C = {
  bg:      "0C1622",
  bgDeep:  "070E17",
  panel:   "14202E",
  panelHi: "1A2938",
  line:    "26384C",
  gold:    "C9A227",
  goldLt:  "E2C56A",
  txt:     "EEF3F8",
  muted:   "93A6BA",
  dim:     "64788D",
  red:     "E0605A",
  redBg:   "2A1A1E",
  green:   "47A883",
  blue:    "6E9CC4",
};
const F = { head: "Cambria", body: "Arial" };

const M = 0.62;                 // page margin
const W = 13.333 - M * 2;       // content width  = 12.093
const BODY_TOP = 1.86;          // first content row
const BODY_BOT = 6.70;          // content must end above this
const FOOT_Y = 6.90;

const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
pres.author = "TMGM";
pres.title = "TMGM Account Manager — 客户沟通话术与四大资产市场分析";

/* ---------------- helpers ---------------- */
const slide = (bg) => {
  const s = pres.addSlide();
  s.background = { color: bg || C.bg };
  return s;
};

// gold square marker + letterspaced eyebrow — the deck's one repeated motif
function eyebrow(s, text, y, color) {
  s.addShape(pres.ShapeType.rect, {
    x: M, y: y + 0.055, w: 0.085, h: 0.085, fill: { color: color || C.gold },
  });
  s.addText(text, {
    x: M + 0.2, y: y - 0.04, w: W - 0.2, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 10.5, bold: true, color: color || C.gold,
    charSpacing: 2.6, valign: "middle",
  });
}

function header(s, eb, title, dek, opts = {}) {
  eyebrow(s, eb, 0.52, opts.ebColor);
  s.addText(title, {
    x: M, y: 0.76, w: opts.titleW || W, h: 0.62, margin: 0,
    fontFace: F.head, fontSize: opts.titleSize || 31, bold: true,
    color: C.txt, valign: "middle",
  });
  if (dek) {
    s.addText(dek, {
      x: M, y: 1.42, w: opts.dekW || W, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 12.5, color: C.muted, valign: "middle",
    });
  }
}

function footer(s, source, page) {
  if (source) {
    s.addText(source, {
      x: M, y: FOOT_Y, w: W - 0.9, h: 0.28, margin: 0,
      fontFace: F.body, fontSize: 9, color: C.dim, valign: "middle",
    });
  }
  if (page) {
    s.addText(page, {
      x: 13.333 - M - 0.8, y: FOOT_Y, w: 0.8, h: 0.28, margin: 0,
      fontFace: F.head, fontSize: 12, color: C.dim,
      align: "right", valign: "middle",
    });
  }
}

function panel(s, x, y, w, h, opts = {}) {
  s.addShape(pres.ShapeType.rect, {
    x, y, w, h,
    fill: { color: opts.fill || C.panel },
    line: { color: opts.line || C.line, width: 1 },
  });
}

function cardTitle(s, text, x, y, w, color) {
  s.addText(text, {
    x, y, w, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 12, bold: true,
    color: color || C.goldLt, charSpacing: 0.8, valign: "middle",
  });
}

// bulleted list built from an array of strings
function bullets(s, items, x, y, w, h, opts = {}) {
  const runs = items.map((t, i) => ({
    text: t,
    options: {
      bullet: { code: "2013" },
      breakLine: i !== items.length - 1,
      paraSpaceAfter: opts.gap === undefined ? 7 : opts.gap,
    },
  }));
  s.addText(runs, {
    x, y, w, h, margin: 0,
    fontFace: F.body, fontSize: opts.size || 11.5,
    color: opts.color || C.txt, lineSpacing: opts.lineSpacing || 17,
    valign: "top",
  });
}

function para(s, text, x, y, w, h, opts = {}) {
  s.addText(text, {
    x, y, w, h, margin: 0,
    fontFace: opts.face || F.body, fontSize: opts.size || 11.5,
    color: opts.color || C.txt, italic: !!opts.italic, bold: !!opts.bold,
    lineSpacing: opts.lineSpacing || 17, valign: opts.valign || "top",
    align: opts.align || "left",
  });
}

// large metric block
function stat(s, x, y, w, h, value, label, color) {
  panel(s, x, y, w, h);
  s.addText(value, {
    x: x + 0.26, y: y + 0.18, w: w - 0.52, h: 0.62, margin: 0,
    fontFace: F.head, fontSize: 30, bold: true, color: color || C.gold,
    valign: "middle",
  });
  s.addText(label, {
    x: x + 0.26, y: y + 0.84, w: w - 0.52, h: 0.44, margin: 0,
    fontFace: F.body, fontSize: 10.5, color: C.muted,
    lineSpacing: 14, valign: "top",
  });
}

// shared chart chrome
function chartBase(extra = {}) {
  return Object.assign({
    showLegend: false,
    showTitle: false,
    chartArea: { fill: { color: C.panel } },
    plotArea: { fill: { color: C.panel } },
    catAxisLabelColor: C.muted, catAxisLabelFontSize: 10, catAxisLabelFontFace: F.body,
    valAxisLabelColor: C.dim, valAxisLabelFontSize: 9.5, valAxisLabelFontFace: F.body,
    valGridLine: { color: "1F2E3E", size: 1 },
    catGridLine: { style: "none" },
    catAxisLineShow: false,
    valAxisLineShow: false,
    dataLabelColor: C.txt, dataLabelFontSize: 10.5, dataLabelFontFace: F.body,
  }, extra);
}

/* =======================================================================
   01 — COVER
   ===================================================================== */
{
  const s = slide(C.bgDeep);
  eyebrow(s, "TMGM  ·  ACCOUNT MANAGER", 1.30);

  s.addText("客户沟通话术\n与四大资产市场分析", {
    x: M, y: 1.72, w: 8.4, h: 1.9, margin: 0,
    fontFace: F.head, fontSize: 45, bold: true, color: C.txt,
    lineSpacing: 58, valign: "middle",
  });

  s.addText("Trademax Australia Limited   ·   ASIC AFSL 436416", {
    x: M, y: 3.76, w: 8.4, h: 0.3, margin: 0,
    fontFace: F.body, fontSize: 12.5, color: C.muted, valign: "middle",
  });

  // two-part contents
  const cw = (W - 0.34) / 2;
  const parts = [
    ["I", "公司介绍话术", "新客户  ·  资深交易者  ·  代理 IB", "01 — 06"],
    ["II", "市场分析", "黄金  ·  纳指  ·  Alphabet  ·  原油", "07 — 18"],
  ];
  parts.forEach((p, i) => {
    const x = M + i * (cw + 0.34);
    panel(s, x, 4.42, cw, 1.42);
    s.addText(p[0], {
      x: x + 0.3, y: 4.62, w: 0.6, h: 0.44, margin: 0,
      fontFace: F.head, fontSize: 21, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(p[1], {
      x: x + 1.0, y: 4.62, w: cw - 1.3, h: 0.44, margin: 0,
      fontFace: F.body, fontSize: 15, bold: true, color: C.txt, valign: "middle",
    });
    s.addText(p[2], {
      x: x + 1.0, y: 5.10, w: cw - 1.3, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.muted, valign: "middle",
    });
    s.addText(p[3], {
      x: x + cw - 1.5, y: 5.10, w: 1.2, h: 0.3, margin: 0,
      fontFace: F.head, fontSize: 11, color: C.dim, align: "right", valign: "middle",
    });
  });

  s.addText("2026年8月9日   ·   内部培训材料   ·   非投资建议", {
    x: M, y: 6.24, w: W, h: 0.3, margin: 0,
    fontFace: F.body, fontSize: 10.5, color: C.dim, valign: "middle",
  });
  s.addNotes("封面。强调这是内部材料，任何对外版本必须先过合规。");
}

/* =======================================================================
   02 — COMPLIANCE
   ===================================================================== */
{
  const s = slide();
  header(s, "COMPLIANCE", "开口之前：四条红线",
    "ASIC 产品干预令已延长至 2027年5月23日  ·  违反可处民事及刑事处罚");

  const cw = (W - 0.3) / 2, ch = 0.86;
  const lines = [
    ["禁止诱导开户", "不得提供开户奖金、返现、交易信用额度或“免费礼品”"],
    ["禁止承诺收益", "不得说“稳赚”“保本”“低风险高回报”或任何形式的收益保证"],
    ["禁止规避杠杆", "不得引导澳洲零售客户转向离岸实体以获取更高杠杆"],
    ["禁止个人建议", "实习生通常未获授权 · 不得针对个人情况推荐仓位或金额"],
  ];
  lines.forEach((L, i) => {
    const x = M + (i % 2) * (cw + 0.3);
    const y = BODY_TOP + Math.floor(i / 2) * (ch + 0.2);
    panel(s, x, y, cw, ch);
    s.addText("✕", {
      x: x + 0.26, y: y + 0.26, w: 0.34, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 15, bold: true, color: C.red,
      align: "center", valign: "middle",
    });
    s.addText(L[0], {
      x: x + 0.72, y: y + 0.18, w: cw - 0.98, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 13, bold: true, color: C.red, valign: "middle",
    });
    s.addText(L[1], {
      x: x + 0.72, y: y + 0.5, w: cw - 0.98, h: 0.32, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.muted, valign: "middle",
    });
  });

  // leverage table
  const ty = BODY_TOP + 2 * (ch + 0.2) + 0.06;
  const th = BODY_BOT - ty;
  panel(s, M, ty, cw, th);
  cardTitle(s, "零售客户杠杆上限  ·  ASIC", M + 0.3, ty + 0.22, cw - 0.6);
  const rows = [
    ["主要货币对", "30:1"], ["次要货币对 / 黄金 / 主要股指", "20:1"],
    ["其他商品 / 次要股指", "10:1"], ["个股", "5:1"], ["加密货币", "2:1"],
  ];
  rows.forEach((r, i) => {
    const ry = ty + 0.68 + i * 0.38;
    if (i % 2 === 1) {
      s.addShape(pres.ShapeType.rect, {
        x: M + 0.16, y: ry, w: cw - 0.32, h: 0.38,
        fill: { color: C.panelHi }, line: { color: C.panelHi, width: 0 },
      });
    }
    s.addText(r[0], {
      x: M + 0.3, y: ry, w: cw - 1.6, h: 0.38, margin: 0,
      fontFace: F.body, fontSize: 11.5, color: C.txt, valign: "middle",
    });
    s.addText(r[1], {
      x: M + cw - 1.4, y: ry, w: 1.1, h: 0.38, margin: 0,
      fontFace: F.head, fontSize: 14, bold: true, color: C.gold,
      align: "right", valign: "middle",
    });
  });

  const x2 = M + cw + 0.3;
  panel(s, x2, ty, cw, th, { fill: C.panelHi });
  cardTitle(s, "每通电话必须说到的三件事", x2 + 0.3, ty + 0.22, cw - 0.6, C.green);
  const musts = [
    "CFD 是杠杆产品，大多数零售客户是亏钱的",
    "已提供 PDS、FSG 与目标市场认定 (TMD)",
    "以上为一般性信息，未考虑你的个人财务状况",
  ];
  musts.forEach((t, i) => {
    const ry = ty + 0.74 + i * 0.56;
    s.addText(String(i + 1).padStart(2, "0"), {
      x: x2 + 0.3, y: ry, w: 0.42, h: 0.3, margin: 0,
      fontFace: F.head, fontSize: 13, bold: true, color: C.green, valign: "middle",
    });
    s.addText(t, {
      x: x2 + 0.82, y: ry, w: cw - 1.14, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 11.5, color: C.txt, valign: "middle",
    });
  });
  para(s, "这三句必须每通电话都讲到 — 不是走流程，是你个人的法律保护。",
    x2 + 0.3, ty + 2.28, cw - 0.6, 0.3, { size: 10.5, color: C.muted, italic: true });

  footer(s, "来源：ASIC 20-254MR / 21-060MR 产品干预令；2022年4月延长五年", "02");
}

/* =======================================================================
   03 — COMPANY FACTS
   ===================================================================== */
{
  const s = slide();
  header(s, "COMPANY", "TMGM 事实档案",
    "只说能查证的事实 · 客户会去查，夸大一次就再也建立不起信任");

  const sw = (W - 0.6) / 3;
  [["AFSL 436416", "ASIC 持牌\n2013年12月获批", C.gold],
   ["12,000+", "可交易品种\n外汇 / 指数 / 股票 / 商品", C.gold],
   ["AA 评级", "客户资金独立存放\n澳洲授权存款机构", C.gold]
  ].forEach((t, i) => {
    stat(s, M + i * (sw + 0.3), BODY_TOP, sw, 1.42, t[0], t[1], t[2]);
  });

  const y2 = BODY_TOP + 1.66;
  const h2 = BODY_BOT - y2;
  const cw = (W - 0.3) / 2;

  panel(s, M, y2, cw, h2);
  cardTitle(s, "实体结构  ·  务必分清", M + 0.3, y2 + 0.22, cw - 0.6);
  const ents = [
    ["Trademax Australia Ltd", "ASIC AFSL 436416 — 澳洲客户归这里", true],
    ["Trademax Global Ltd", "瓦努阿图 VFSC 40356", false],
    ["Trademax Global Markets (SE)", "塞舌尔 FSA SD224", false],
    ["Trademax Global Markets (Intl)", "毛里求斯 FSC", false],
    ["Zero Markets (NZ) Ltd", "新西兰 FMA FSP 569807", false],
  ];
  ents.forEach((e, i) => {
    const ry = y2 + 0.7 + i * 0.5;
    s.addText(e[0], {
      x: M + 0.3, y: ry, w: cw - 0.6, h: 0.24, margin: 0,
      fontFace: F.body, fontSize: 11, bold: true,
      color: e[2] ? C.goldLt : C.txt, valign: "middle",
    });
    s.addText(e[1], {
      x: M + 0.3, y: ry + 0.23, w: cw - 0.6, h: 0.22, margin: 0,
      fontFace: F.body, fontSize: 10, color: e[2] ? C.gold : C.muted, valign: "middle",
    });
  });

  const x2 = M + cw + 0.3;
  panel(s, x2, y2, cw, h2);
  cardTitle(s, "其他可查证事实", x2 + 0.3, y2 + 0.22, cw - 0.6);
  bullets(s, [
    "总部：Level 28, One International Tower, Barangaroo, 悉尼",
    "澳洲办公室：悉尼、墨尔本、阿德莱德、堪培拉",
    "2018 年由 TradeMax 更名为 TMGM Group",
    "赞助：澳大利亚网球公开赛、AFF 三菱电机杯",
    "私人持股，未公开上市，无披露的外部风投",
    "不接受美国、加拿大、日本居民开户",
    "受 AFCA 澳洲金融投诉管理局争议机制覆盖",
  ], x2 + 0.3, y2 + 0.72, cw - 0.6, h2 - 0.95, { size: 11, gap: 8 });

  footer(s, "来源：TMGM 官网监管页面 / ASIC 注册资料", "03");
}

/* =======================================================================
   04 — SCRIPT I
   ===================================================================== */
{
  const s = slide();
  header(s, "SCRIPT I", "新客户 / 首次接触",
    "目标不是让他今天入金，而是让他明白自己在参与什么");

  const lw = W * 0.615, rw = W - lw - 0.3;
  const h1 = 2.72;
  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "开场  ·  30 秒", M + 0.3, BODY_TOP + 0.22, lw - 0.6);
  para(s,
    "“我是 TMGM 的 [姓名]。我们是 Trademax Australia，受澳洲 ASIC 监管，持牌编号 436416，自 2013 年运营，总部在悉尼 Barangaroo。\n\n" +
    "在讲任何产品之前，我得先说清楚一件事：我们做的是差价合约，这是杠杆产品，大部分零售客户在这个产品上是亏钱的。如果你听完觉得不适合，那完全没问题。\n\n" +
    "我先问你三个问题：你之前交易过杠杆产品吗？你打算投入的这笔钱，全部亏掉会不会影响你的生活？你希望解决什么问题？”",
    M + 0.3, BODY_TOP + 0.66, lw - 0.6, h1 - 0.9, { size: 11, lineSpacing: 17 });

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "为什么这样开场", x2 + 0.3, BODY_TOP + 0.22, rw - 0.6, C.green);
  const whys = [
    ["先亮牌照", "建立可查证的信任"],
    ["先讲风险", "满足合规，筛掉赔不起的人"],
    ["提问", "判断是否属于目标市场 TMD"],
    ["“不适合也没问题”", "降低防御，提高留存"],
  ];
  whys.forEach((w, i) => {
    const ry = BODY_TOP + 0.72 + i * 0.4;
    s.addText([
      { text: w[0], options: { bold: true, color: C.txt } },
      { text: "  =  ", options: { color: C.dim } },
      { text: w[1], options: { color: C.muted } },
    ], {
      x: x2 + 0.3, y: ry, w: rw - 0.6, h: 0.36, margin: 0,
      fontFace: F.body, fontSize: 11, valign: "middle",
    });
  });

  const y3 = BODY_TOP + h1 + 0.24;
  cardTitle(s, "异议应对", M, y3, 3.0);
  const objs = [
    ["“能赚多少？”", "“我没法给你任何收益预期——真给了就是违规。我能告诉你的是成本结构和风险有多大。”"],
    ["“有没有开户优惠？”", "“澳洲监管明确禁止用奖金或礼品吸引开户。任何这么说的平台，你都该多留个心眼。”"],
    ["“我朋友说能加到 500 倍”", "“那是离岸牌照。澳洲零售上限是外汇 30 倍、黄金 20 倍。杠杆低不是缺点，是保护。”"],
  ];
  objs.forEach((o, i) => {
    const ry = y3 + 0.38 + i * 0.52;
    s.addShape(pres.ShapeType.rect, {
      x: M, y: ry, w: W, h: 0.46,
      fill: { color: i % 2 ? C.panelHi : C.panel },
      line: { color: C.line, width: 1 },
    });
    s.addText(o[0], {
      x: M + 0.28, y: ry, w: 3.0, h: 0.46, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: C.goldLt, valign: "middle",
    });
    s.addText(o[1], {
      x: M + 3.4, y: ry, w: W - 3.7, h: 0.46, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.txt, valign: "middle",
    });
  });

  footer(s, "结尾必说：“以上是一般性信息，没有考虑你的个人财务状况。开户前请读完 PDS 和 TMD。”", "04");
}

/* =======================================================================
   05 — SCRIPT II
   ===================================================================== */
{
  const s = slide();
  header(s, "SCRIPT II", "资深交易者 / 换平台客户",
    "他不需要你教他交易 · 只关心成本、执行、出金 · 讲品牌故事等于浪费他时间");

  const cw = (W - 0.6) / 3, ch = 1.42;
  [["成本", "点差结构、佣金、隔夜利息、货币转换费。给具体数字，不给形容词。"],
   ["执行", "订单类型、滑点政策、服务器位置与延迟、平台 MT4/MT5、API 接入。"],
   ["资金安全", "客户资金独立存放于 AA 评级澳洲 ADI；负余额保护；AFCA 争议解决。"]
  ].forEach((t, i) => {
    const x = M + i * (cw + 0.3);
    panel(s, x, BODY_TOP, cw, ch);
    s.addText(String(i + 1).padStart(2, "0"), {
      x: x + 0.3, y: BODY_TOP + 0.2, w: 0.5, h: 0.3, margin: 0,
      fontFace: F.head, fontSize: 13, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(t[0], {
      x: x + 0.82, y: BODY_TOP + 0.2, w: cw - 1.1, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 13.5, bold: true, color: C.txt, valign: "middle",
    });
    para(s, t[1], x + 0.3, BODY_TOP + 0.66, cw - 0.6, ch - 0.9, { size: 11, color: C.muted });
  });

  const y2 = BODY_TOP + ch + 0.28;
  const h2 = 2.42;
  const lw = W * 0.615, rw = W - lw - 0.3;

  panel(s, M, y2, lw, h2);
  cardTitle(s, "开场  ·  15 秒，直接切入", M + 0.3, y2 + 0.22, lw - 0.6);
  para(s,
    "“我不占用你时间讲品牌。三个数字：我们的 [品种] 平均点差是 X，佣金 Y，隔夜利息 Z。你现在平台是多少？\n\n" +
    "如果我们没优势，我直接告诉你，不浪费你时间。如果有，我给你开个模拟账户，你用自己的策略跑两周，看执行质量再决定。”",
    M + 0.3, y2 + 0.7, lw - 0.6, h2 - 0.95, { size: 12, lineSpacing: 20 });

  const x2 = M + lw + 0.3;
  panel(s, x2, y2, rw, h2, { fill: C.panelHi });
  cardTitle(s, "绝对不要做", x2 + 0.3, y2 + 0.22, rw - 0.6, C.red);
  bullets(s, [
    "不要背诵公司历史和奖项",
    "不要给他看你的行情分析（他比你懂）",
    "不要回避不利对比 — 他一定会自己查",
    "不要暗示离岸账户能给更高杠杆",
  ], x2 + 0.3, y2 + 0.74, rw - 0.6, h2 - 1.0, { size: 11.5, gap: 11 });

  footer(s, "所有点差、佣金、隔夜利息必须来自 TMGM 官方产品明细表，注明为浮动或历史平均值，不得报成固定值", "05");
}

/* =======================================================================
   06 — SCRIPT III
   ===================================================================== */
{
  const s = slide();
  header(s, "SCRIPT III", "代理 / IB 合作伙伴",
    "代理关心可持续的分成，不是一次性冲量 · 帮他把客户留住，他才会长期给你导流");

  const lw = W * 0.5 - 0.15, rw = lw, h1 = 2.3;
  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "开场", M + 0.3, BODY_TOP + 0.22, lw - 0.6);
  para(s,
    "“你带来的客户，我们的目标不是让他一个月爆仓走人，而是让他活得够久、交易得够久。\n\n" +
    "我们受 ASIC 监管，客户资金存在 AA 评级澳洲银行，有负余额保护和 AFCA 争议渠道 —— 这些对你意味着更少的客诉，和更长的客户生命周期。”",
    M + 0.3, BODY_TOP + 0.68, lw - 0.6, h1 - 0.92, { size: 11, lineSpacing: 17 });

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "代理真正会问的四个问题", x2 + 0.3, BODY_TOP + 0.22, rw - 0.6, C.green);
  const qs = [
    "分成结构：按手数还是按点差？几时结算？",
    "后台：能不能实时看到下线客户数据？",
    "支持：有没有中文客服、本地化材料？",
    "合规：我作为代理，营销上有哪些限制？",
  ];
  qs.forEach((q, i) => {
    const ry = BODY_TOP + 0.72 + i * 0.32;
    s.addText(String(i + 1).padStart(2, "0"), {
      x: x2 + 0.3, y: ry, w: 0.4, h: 0.3, margin: 0,
      fontFace: F.head, fontSize: 11.5, bold: true, color: C.green, valign: "middle",
    });
    s.addText(q, {
      x: x2 + 0.78, y: ry, w: rw - 1.1, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.txt, valign: "middle",
    });
  });

  const y2 = BODY_TOP + h1 + 0.28;
  cardTitle(s, "代理关系里最容易出事的地方 — 你要主动讲清楚", M, y2, 8.0, C.red);
  const risks = [
    ["代理的宣传也算数", "代理在微信群、小红书发的“稳赚”截图，监管责任可能回到持牌方"],
    ["代理不得提供建议", "未持牌代理向客户推荐仓位、品种、进出场点位，属于无牌提供金融建议"],
    ["不得代客操作", "代理拿客户账号密码下单是明确违规，一旦亏损必然演变成投诉与法律纠纷"],
  ];
  const rw3 = (W - 0.6) / 3;
  const ry = y2 + 0.4;
  const rh = 1.42;
  risks.forEach((r, i) => {
    const x = M + i * (rw3 + 0.3);
    panel(s, x, ry, rw3, rh, { fill: C.redBg, line: "48282C" });
    s.addText("!", {
      x: x + 0.3, y: ry + 0.24, w: 0.3, h: 0.3, margin: 0,
      fontFace: F.head, fontSize: 17, bold: true, color: C.red,
      align: "center", valign: "middle",
    });
    s.addText(r[0], {
      x: x + 0.68, y: ry + 0.24, w: rw3 - 0.98, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 12, bold: true, color: C.txt, valign: "middle",
    });
    para(s, r[1], x + 0.3, ry + 0.72, rw3 - 0.6, rh - 0.95, { size: 11, color: C.muted });
  });

  footer(s, "任何代理协议条款、分成比例与结算方式，必须以 TMGM 法务 / 合规提供的正式文件为准，不得口头承诺", "06");
}

/* =======================================================================
   07 — PART II · MARKET BACKDROP
   ===================================================================== */
{
  const s = slide(C.bgDeep);
  header(s, "PART II  ·  MARKETS", "2026年8月9日 · 市场背景",
    "三条主线同时在推动所有资产");

  const drivers = [
    ["01", "美联储转鹰",
      "主席 Kevin Warsh 立场强硬。7月29日会议维持 350–375bp 不变；市场一度给到 35.8% 的加息概率。6月通胀 3.5%，核心 2.6%。"],
    ["02", "霍尔木兹海峡危机",
      "美伊冲突后海峡通行受限。伊朗与阿曼谈判胶着，伊方要求排除美以船只并收费。能源价格与通胀预期被牢牢绑定。"],
    ["03", "纳指年内第二次回调",
      "AI 板块高度集中，资金对巨额资本开支的耐心下降。市场从“讲故事”转向“看现金流”。"],
  ];
  const cw = (W - 0.6) / 3;
  const ch = 2.8;
  drivers.forEach((d, i) => {
    const x = M + i * (cw + 0.3);
    panel(s, x, BODY_TOP, cw, ch);
    s.addText(d[0], {
      x: x + 0.32, y: BODY_TOP + 0.26, w: 1.0, h: 0.62, margin: 0,
      fontFace: F.head, fontSize: 34, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(d[1], {
      x: x + 0.32, y: BODY_TOP + 1.0, w: cw - 0.64, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 14, bold: true, color: C.txt, valign: "middle",
    });
    para(s, d[2], x + 0.32, BODY_TOP + 1.44, cw - 0.64, ch - 1.68,
      { size: 11.5, color: C.muted, lineSpacing: 20 });
  });

  const yq = BODY_TOP + ch + 0.3;
  panel(s, M, yq, W, 1.0, { fill: C.panelHi });
  s.addText([
    { text: "给客户的一句话：", options: { bold: true, color: C.goldLt } },
    { text: "利率、地缘、AI 资本开支 — 今天几乎每个品种的波动都能追溯到这三件事之一。",
      options: { color: C.txt } },
  ], {
    x: M + 0.34, y: yq, w: W - 0.68, h: 1.0, margin: 0,
    fontFace: F.body, fontSize: 13, valign: "middle",
  });

  footer(s, null, "07");
}

/* =======================================================================
   08 — GOLD FUNDAMENTALS
   ===================================================================== */
{
  const s = slide();
  header(s, "GOLD  ·  XAU/USD", "黄金 · 基本面与政策",
    "从 1月历史高点 $5,598 回落约 28% · 目前在 $4,020–4,050 区间盘整");

  const sw = 2.28, sh = 1.56;
  stat(s, M, BODY_TOP, sw, sh, "$4,020", "现价区间 · 8月初", C.gold);
  stat(s, M + (sw + 0.3), BODY_TOP, sw, sh, "−28%", "较1月高点回撤", C.red);
  stat(s, M + 2 * (sw + 0.3), BODY_TOP, sw, sh, "20:1", "ASIC 零售杠杆上限", C.txt);

  const xt = M + 3 * (sw + 0.3);
  const tw = W - 3 * (sw + 0.3);
  panel(s, xt, BODY_TOP, tw, sh, { fill: C.panelHi });
  cardTitle(s, "机构目标价严重分歧  ·  分歧本身就是波动来源", xt + 0.3, BODY_TOP + 0.18, tw - 0.6);
  const tgts = [["摩根大通", "$6,000"], ["高盛", "$4,900"], ["汇丰", "$4,560"], ["StoneX", "$4,000"]];
  tgts.forEach((t, i) => {
    const ry = BODY_TOP + 0.54 + i * 0.25;
    s.addText(t[0], {
      x: xt + 0.3, y: ry, w: 1.6, h: 0.25, margin: 0,
      fontFace: F.body, fontSize: 10.5, color: C.muted, valign: "middle",
    });
    s.addText(t[1], {
      x: xt + tw - 1.5, y: ry, w: 1.2, h: 0.25, margin: 0,
      fontFace: F.head, fontSize: 13, bold: true, color: C.txt,
      align: "right", valign: "middle",
    });
  });

  const y2 = BODY_TOP + sh + 0.28;
  const h2 = BODY_BOT - y2;
  const cw = (W - 0.3) / 2;

  panel(s, M, y2, cw, h2);
  cardTitle(s, "支撑金价的力量", M + 0.3, y2 + 0.24, cw - 0.6, C.green);
  bullets(s, [
    "各国央行持续购金，部分抵消 ETF 的大额赎回",
    "霍尔木兹冲突未解，避险需求随时可能被点燃",
    "美国财政赤字推向 GDP 约 7%，长期利多贵金属",
    "波动率压缩到极致，通常预示一次方向性大行情",
    "若美联储措辞转鸽，看跌结构可能快速反转",
  ], M + 0.3, y2 + 0.78, cw - 0.6, h2 - 1.05, { size: 12, gap: 16 });

  const x2 = M + cw + 0.3;
  panel(s, x2, y2, cw, h2);
  cardTitle(s, "压制金价的力量", x2 + 0.3, y2 + 0.24, cw - 0.6, C.red);
  bullets(s, [
    "Warsh 领导下的美联储拒绝转向，实际利率维持高位",
    "市场仍在给加息定价 — 对无息资产是直接打击",
    "ETF 持续净赎回，投资端需求疲弱",
    "全球矿产供应上升",
    "月线级别动能指标仍指向下方",
  ], x2 + 0.3, y2 + 0.78, cw - 0.6, h2 - 1.05, { size: 12, gap: 16 });

  footer(s, "来源：CNBC、路透、摩根大通全球研究、LiteFinance（2026年7–8月） · 一般性信息，非投资建议", "08");
}

/* =======================================================================
   09 — GOLD TECHNICALS
   ===================================================================== */
{
  const s = slide();
  header(s, "GOLD  ·  TECHNICALS", "黄金 · 技术面与关键价位",
    "价格被夹在 200 日与 50 日均线之间 — 摩根大通称之为“技术上的无人区”");

  const lw = 7.5, rw = W - lw - 0.3;
  const h1 = 3.1;
  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "黄金 2026 年走势  ·  示意", M + 0.3, BODY_TOP + 0.22, lw - 0.6);
  s.addChart(pres.ChartType.line, [{
    name: "XAU/USD",
    labels: ["25年12月", "26年1月高点", "3月", "5月", "7月末", "8月初"],
    values: [4550, 5598, 4870, 4400, 4050, 4029],
  }], chartBase({
    x: M + 0.16, y: BODY_TOP + 0.6, w: lw - 0.32, h: h1 - 0.78,
    chartColors: [C.gold],
    lineSize: 3, lineSmooth: true,
    lineDataSymbol: "circle", lineDataSymbolSize: 7,
    lineDataSymbolLineColor: C.gold, lineDataSymbolSolidFill: C.panel,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "$#,##0",
    valAxisMinVal: 3600, valAxisMaxVal: 6000,
    valAxisLabelFormatCode: "$#,##0",
  }));

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "关键价位  ·  需盘前复核", x2 + 0.3, BODY_TOP + 0.22, rw - 0.6);
  const lv = [
    ["50 日均线", "$4,730", "阻力", C.red],
    ["200 日均线", "$4,340", "分水岭", C.gold],
    ["现价", "$4,029", "—", C.txt],
    ["预测下沿", "$3,580", "支撑", C.green],
  ];
  lv.forEach((l, i) => {
    const ry = BODY_TOP + 0.66 + i * 0.46;
    if (i % 2 === 1) {
      s.addShape(pres.ShapeType.rect, {
        x: x2 + 0.16, y: ry, w: rw - 0.32, h: 0.46,
        fill: { color: C.panel }, line: { color: C.panel, width: 0 },
      });
    }
    s.addText(l[0], {
      x: x2 + 0.3, y: ry, w: 1.5, h: 0.46, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.muted, valign: "middle",
    });
    s.addText(l[1], {
      x: x2 + 1.6, y: ry, w: 1.3, h: 0.46, margin: 0,
      fontFace: F.head, fontSize: 16, bold: true, color: l[3],
      align: "right", valign: "middle",
    });
    s.addText(l[2], {
      x: x2 + rw - 1.1, y: ry, w: 0.8, h: 0.46, margin: 0,
      fontFace: F.body, fontSize: 10, color: C.dim,
      align: "right", valign: "middle",
    });
  });
  para(s, "均线为 6 月摩根大通口径，可能已变动。\n务必用 TMGM 实时图表复核后再对外使用。",
    x2 + 0.3, BODY_TOP + 2.54, rw - 0.6, 0.46, { size: 10, color: C.red, italic: true, lineSpacing: 14 });

  const y3 = BODY_TOP + h1 + 0.26;
  const h3 = BODY_BOT - y3;
  panel(s, M, y3, W, h3);
  cardTitle(s, "两种情景  ·  不做单边预测", M + 0.3, y3 + 0.2, W - 0.6);
  const sc = [
    ["看涨", "守住 200 日均线并放量上破 $4,340，配合美联储措辞转鸽，有机会重新挑战 $4,730。", C.green],
    ["看跌", "跌破 $4,000 整数关口且月线动能延续，打开向 $3,845 / $3,580 的下行空间。波动率压缩意味着无论哪个方向，启动都可能很急。", C.red],
  ];
  sc.forEach((v, i) => {
    const ry = y3 + 0.6 + i * 0.44;
    s.addText(v[0], {
      x: M + 0.3, y: ry, w: 0.7, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: v[2], valign: "middle",
    });
    s.addText(v[1], {
      x: M + 1.06, y: ry, w: W - 1.36, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.txt, valign: "middle",
    });
  });

  footer(s, "图表为示意性走势，非精确 K 线数据 · 一般性信息，不构成交易建议", "09");
}

/* =======================================================================
   10 — NASDAQ FUNDAMENTALS
   ===================================================================== */
{
  const s = slide();
  header(s, "NASDAQ", "纳斯达克 · 基本面与政策",
    "2026年内第二次进入回调区间 · 问题不在 AI 故事是否成立，而在估值是否已经透支");

  const h1 = 1.5;
  panel(s, M, BODY_TOP, W, h1, { fill: C.panelHi });
  cardTitle(s, "核心矛盾", M + 0.34, BODY_TOP + 0.22, 4.0);
  para(s,
    "纳指权重高度集中在少数依赖 AI 增长叙事的巨头。只要叙事松动，指数下跌速度就会远快于标普与道指 — 7月29日标普距高点仅 4%，道指仅 3.2%，而纳指已进入回调。这个结构性差异是解释指数波动最有力的框架。",
    M + 0.34, BODY_TOP + 0.62, W - 0.68, h1 - 0.86, { size: 12, lineSpacing: 20 });

  const y2 = BODY_TOP + h1 + 0.26;
  const h2 = BODY_BOT - y2;
  const cw = (W - 0.6) / 3;
  const cols = [
    ["政策变量", C.gold, [
      "美联储主席 Warsh 鹰派，不排除加息",
      "高利率直接压制成长股估值",
      "OBBBA 财政刺激退潮，赤字升至 GDP 约 7%",
      "地缘冲突推高能源，通胀更难压下",
    ]],
    ["支撑因素", C.green, [
      "微软 Azure 收入激增曾带动纳指创 6 月来最佳单日",
      "巨头现金流与资产负债表依然稳健",
      "AI 需求是多年期趋势，非单季故事",
      "回调后部分标的估值重新具吸引力",
    ]],
    ["风险因素", C.red, [
      "半导体板块反复抛售，美光一度重挫 30%",
      "指数集中度高，单一龙头失速即拖累全局",
      "市场进入“拿出证据来”阶段",
      "20:1 杠杆下波动仍足以快速触发强平",
    ]],
  ];
  cols.forEach((col, i) => {
    const x = M + i * (cw + 0.3);
    panel(s, x, y2, cw, h2);
    cardTitle(s, col[0], x + 0.3, y2 + 0.24, cw - 0.6, col[1]);
    bullets(s, col[2], x + 0.3, y2 + 0.76, cw - 0.6, h2 - 1.02,
      { size: 11, gap: 14 });
  });

  footer(s, "来源：The Motley Fool、CNBC（2026年7–8月） · 一般性信息，非投资建议", "10");
}

/* =======================================================================
   11 — NASDAQ TECHNICALS
   ===================================================================== */
{
  const s = slide();
  header(s, "NASDAQ  ·  TECHNICALS", "纳斯达克 · 技术面与交易含义",
    "回调定义为自高点回落 10–20% · 历史上纳指回调后多在年内收复，但“多数”不等于“这次”");

  const lw = 6.4, rw = W - lw - 0.3;
  const h1 = 2.86;
  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "三大指数自高点回撤  ·  7月末（%）", M + 0.3, BODY_TOP + 0.22, lw - 0.6);
  s.addChart(pres.ChartType.bar, [{
    name: "回撤 %",
    labels: ["纳斯达克", "标普 500", "道琼斯"],
    values: [13, 4, 3.2],
  }], chartBase({
    x: M + 0.16, y: BODY_TOP + 0.6, w: lw - 0.32, h: h1 - 0.8,
    barDir: "col", barGapWidthPct: 130,
    chartColors: [C.red, "3D5266", "3D5266"],
    chartColorsOpacity: 100,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0"%"',
    dataLabelFontSize: 12,
    valAxisMinVal: 0, valAxisMaxVal: 16,
    valAxisLabelFormatCode: '0"%"',
    catAxisLabelFontSize: 11.5,
  }));

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "这张图怎么用", x2 + 0.3, BODY_TOP + 0.22, rw - 0.6);
  para(s,
    "同一段时间里，纳指跌幅是道指的四倍。这不是市场整体崩了，而是资金在从科技集中度最高的地方撤出。\n\n" +
    "对客户的实际含义：如果他做纳指 CFD，他承担的不是“美国经济风险”，而是集中的 AI 板块风险。\n\n" +
    "这个区分能帮客户理解为什么仓位波动远大于预期 — 也是你能提供的、真正有价值的信息。",
    x2 + 0.3, BODY_TOP + 0.7, rw - 0.6, h1 - 0.95, { size: 12, lineSpacing: 20 });

  const y3 = BODY_TOP + h1 + 0.26;
  const h3 = BODY_BOT - y3;
  panel(s, M, y3, W, h3);
  cardTitle(s, "风险管理提示  ·  仅作一般性教育", M + 0.3, y3 + 0.2, W - 0.6);
  const tips = [
    ["回调 ≠ 见底", "10–20% 的回撤可以延续数月，也可以演变成熊市。别把“历史上会反弹”当成时间表。"],
    ["集中度即风险", "少数权重股决定指数方向，财报季的单日跳空风险显著高于分散型指数。"],
    ["杠杆放大一切", "20:1 下，指数 5% 的逆向波动即接近本金全损。强平会先于本金耗尽触发。"],
  ];
  tips.forEach((t, i) => {
    const ry = y3 + 0.58 + i * 0.4;
    s.addText(t[0], {
      x: M + 0.3, y: ry, w: 2.1, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: C.goldLt, valign: "middle",
    });
    s.addText(t[1], {
      x: M + 2.5, y: ry, w: W - 2.8, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.txt, valign: "middle",
    });
  });

  footer(s, "回撤数据为 2026年7月29日近似值 · 一般性信息，非投资建议", "11");
}

/* =======================================================================
   12 — ALPHABET FUNDAMENTALS
   ===================================================================== */
{
  const s = slide();
  header(s, "ALPHABET  ·  GOOGL", "Alphabet · 基本面",
    "Q2 2026 财报几乎全线超预期，但股价没涨 — 因为自由现金流转负了");

  const sw = (W - 0.9) / 4, sh = 1.34;
  [["$1,198亿", "Q2 营收\n+24% YoY", C.green],
   ["+82%", "Google Cloud 增长\n至 $248 亿", C.green],
   ["−$58.6亿", "Q2 自由现金流转负", C.red],
   ["$449亿", "Q2 资本开支\n同比 +100%", C.red]
  ].forEach((t, i) => {
    stat(s, M + i * (sw + 0.3), BODY_TOP, sw, sh, t[0], t[1], t[2]);
  });

  const y2 = BODY_TOP + sh + 0.28;
  const h2 = BODY_BOT - y2;
  const lw = 6.4, rw = W - lw - 0.3;

  panel(s, M, y2, lw, h2);
  cardTitle(s, "各业务线同比增长（%）", M + 0.3, y2 + 0.2, lw - 0.6);
  s.addChart(pres.ChartType.bar, [{
    name: "同比增长 %",
    labels: ["Google Cloud", "订阅与设备", "搜索广告", "YouTube 广告", "整体营收"],
    values: [82, 15, 17, 13, 24],
  }], chartBase({
    x: M + 0.16, y: y2 + 0.56, w: lw - 0.32, h: h2 - 0.74,
    barDir: "bar", barGapWidthPct: 60,
    chartColors: [C.gold],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"',
    valAxisMinVal: 0, valAxisMaxVal: 95,
    valAxisLabelFormatCode: '0"%"',
    catAxisLabelFontSize: 11,
  }));

  const x2 = M + lw + 0.3;
  panel(s, x2, y2, rw, h2, { fill: C.panelHi });
  cardTitle(s, "多空双方各自的论据", x2 + 0.3, y2 + 0.2, rw - 0.6);
  s.addText("看多", {
    x: x2 + 0.3, y: y2 + 0.6, w: rw - 0.6, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 11.5, bold: true, color: C.green, valign: "middle",
  });
  para(s, "EPS $9.11 远超预期 $2.89；Gemini 应用月活 9.5 亿；财富 100 强企业渗透率近 90%；33 位分析师中 28 位给出买入评级。",
    x2 + 0.3, y2 + 0.9, rw - 0.6, 0.95, { size: 11, color: C.txt, lineSpacing: 17 });
  s.addText("看空", {
    x: x2 + 0.3, y: y2 + 1.76, w: rw - 0.6, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 11.5, bold: true, color: C.red, valign: "middle",
  });
  para(s, "全年资本开支指引 $1,800–1,900 亿；6 月增发股票筹资 $496 亿并发债 $203 亿；自由现金流转负；股价年内涨 11% 但 5、6、7 月连续下跌，跑输苹果与英伟达。",
    x2 + 0.3, y2 + 2.06, rw - 0.6, 1.2, { size: 11, color: C.txt, lineSpacing: 17 });

  footer(s, "来源：Alphabet Q2 2026 财报、CNBC、TheStreet、IG（2026年7月22日） · 一般性信息，非投资建议", "12");
}

/* =======================================================================
   13 — ALPHABET TECHNICALS & REGULATION
   ===================================================================== */
{
  const s = slide();
  header(s, "ALPHABET  ·  TECHNICALS", "Alphabet · 技术面与监管",
    "监管压力是这只股票区别于其他科技巨头的独立变量");

  const cw = (W - 0.3) / 2;
  const h1 = 2.08;

  panel(s, M, BODY_TOP, cw, h1);
  cardTitle(s, "技术位  ·  7月中旬口径，需复核", M + 0.3, BODY_TOP + 0.2, cw - 0.6);
  const px = [["近期收盘", "$346.77", C.txt], ["趋势线支撑", "$341.43", C.green], ["EMA 阻力带", "$357–359", C.red]];
  px.forEach((p, i) => {
    const x = M + 0.3 + i * ((cw - 0.6) / 3);
    s.addText(p[0], {
      x, y: BODY_TOP + 0.58, w: (cw - 0.6) / 3, h: 0.24, margin: 0,
      fontFace: F.body, fontSize: 10.5, color: C.muted, valign: "middle",
    });
    s.addText(p[1], {
      x, y: BODY_TOP + 0.84, w: (cw - 0.6) / 3, h: 0.36, margin: 0,
      fontFace: F.head, fontSize: 19, bold: true, color: p[2], valign: "middle",
    });
  });
  para(s, "突破条件：需放量站上 $357–359 的 EMA 密集区，才谈得上趋势反转。",
    M + 0.3, BODY_TOP + 1.26, cw - 0.6, 0.32, { size: 10.5, color: C.goldLt, italic: true });

  const x2 = M + cw + 0.3;
  panel(s, x2, BODY_TOP, cw, h1, { fill: C.panelHi });
  cardTitle(s, "监管与政策事件", x2 + 0.3, BODY_TOP + 0.2, cw - 0.6);
  const ev = [
    ["7月2日", "欧盟法院终审维持 41 亿欧元（约 $46.7 亿）Android 反垄断罚款，八年官司落幕"],
    ["7月17–18日", "欧盟依《数字市场法》DMA 发出具约束力的互操作性指令"],
    ["影响", "罚款相对可承受（单季营收即超千亿），但会为后续案件立下判例"],
  ];
  ev.forEach((e, i) => {
    const ry = BODY_TOP + 0.58 + i * 0.38;
    s.addText(e[0], {
      x: x2 + 0.3, y: ry, w: 1.15, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 10.5, bold: true, color: C.goldLt, valign: "middle",
    });
    s.addText(e[1], {
      x: x2 + 1.5, y: ry, w: cw - 1.8, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 10.5, color: C.txt, valign: "middle",
    });
  });

  const y3 = BODY_TOP + h1 + 0.3;
  cardTitle(s, "交易 GOOGL CFD 时要提醒客户的三件事", M, y3, 7.0);
  const three = [
    ["01", "个股杠杆仅 5:1", "ASIC 对个股 CFD 的杠杆上限是 5 倍，远低于外汇。客户常误以为可以高杠杆做个股。"],
    ["02", "财报与监管跳空", "财报公布与欧盟裁决都在非交易时段发生，开盘跳空可能直接跳过止损价位。"],
    ["03", "CFD 不等于持股", "客户不持有实际股份，没有投票权；股息以调整方式处理，持仓过夜产生融资费用。"],
  ];
  const tw = (W - 0.6) / 3;
  const ty = y3 + 0.4;
  const th = 1.66;
  three.forEach((t, i) => {
    const x = M + i * (tw + 0.3);
    panel(s, x, ty, tw, th);
    s.addText(t[0], {
      x: x + 0.3, y: ty + 0.24, w: 0.6, h: 0.36, margin: 0,
      fontFace: F.head, fontSize: 17, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(t[1], {
      x: x + 0.86, y: ty + 0.24, w: tw - 1.16, h: 0.36, margin: 0,
      fontFace: F.body, fontSize: 12.5, bold: true, color: C.txt, valign: "middle",
    });
    para(s, t[2], x + 0.3, ty + 0.76, tw - 0.6, th - 1.0, { size: 11, color: C.muted });
  });

  footer(s, "价位为 2026年7月中旬数据，可能已显著变动 · 使用前必须以实时行情复核 · 非投资建议", "13");
}

/* =======================================================================
   14 — CRUDE FUNDAMENTALS
   ===================================================================== */
{
  const s = slide();
  header(s, "ENERGY  ·  CRUDE / XOM", "原油与能源股 · 基本面与政策",
    "四个资产里政策驱动最纯粹的一个 — 霍尔木兹海峡的每条新闻都会直接反映在价格上");

  const sw = (W - 0.9) / 4, sh = 1.26;
  [["$78.18", "WTI 现货 · 8月7日", C.gold],
   ["$82", "布伦特原油", C.gold],
   ["+22.4%", "同比涨幅", C.green],
   ["$54.97–119.47", "52 周区间", C.txt]
  ].forEach((t, i) => {
    const x = M + i * (sw + 0.3);
    panel(s, x, BODY_TOP, sw, sh);
    s.addText(t[0], {
      x: x + 0.26, y: BODY_TOP + 0.2, w: sw - 0.52, h: 0.56, margin: 0,
      fontFace: F.head, fontSize: i === 3 ? 18 : 28, bold: true, color: t[2], valign: "middle",
    });
    s.addText(t[1], {
      x: x + 0.26, y: BODY_TOP + 0.8, w: sw - 0.52, h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 10.5, color: C.muted, valign: "top",
    });
  });

  const y2 = BODY_TOP + sh + 0.26;
  const h2 = BODY_BOT - y2;
  const lw = W * 0.5 - 0.15, rw = lw;

  panel(s, M, y2, lw, h2, { fill: C.panelHi });
  cardTitle(s, "霍尔木兹海峡  ·  当前谈判焦点", M + 0.3, y2 + 0.24, lw - 0.6);
  bullets(s, [
    "伊朗提出的伊阿协议草案要求禁止美、以船只通行",
    "并要求被其视为敌对的国家先行支付补偿",
    "违规船只可能被处以货值 20% 的罚金",
    "伊朗称海峡须待美国解除海上封锁后才完全重开",
    "美方立场相反，要求无限制通行、恢复战前状态",
    "伊朗曾对海峡内“敌对目标”实施打击",
  ], M + 0.3, y2 + 0.76, lw - 0.6, h2 - 1.0, { size: 11.5, gap: 10 });

  const x2 = M + lw + 0.3;
  panel(s, x2, y2, rw, h2);
  cardTitle(s, "能源股的基本面", x2 + 0.3, y2 + 0.24, rw - 0.6);
  s.addText("利多", {
    x: x2 + 0.3, y: y2 + 0.68, w: rw - 0.6, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 11.5, bold: true, color: C.green, valign: "middle",
  });
  para(s, "埃克森美孚、雪佛龙、Valero 上季度均交出亮眼财报 — 美伊冲突制造了巨额短期利润。炼油类 ETF 与原油波动率产品是近半年最大赢家之一。",
    x2 + 0.3, y2 + 0.98, rw - 0.6, 0.9, { size: 11, lineSpacing: 17 });
  s.addText("利空", {
    x: x2 + 0.3, y: y2 + 1.94, w: rw - 0.6, h: 0.26, margin: 0,
    fontFace: F.body, fontSize: 11.5, bold: true, color: C.red, valign: "middle",
  });
  para(s, "高盛预测 2026 年四季度布伦特仅 $60、WTI $56，并维持全年 230 万桶/日的供给过剩判断。多位机构人士警告：押注地缘政治是高风险交易，一旦停火，溢价会迅速消失。",
    x2 + 0.3, y2 + 2.24, rw - 0.6, 1.0, { size: 11, lineSpacing: 17 });

  footer(s, "来源：Trading Economics、Forbes、CNBC、Oilprice（2026年8月） · 一般性信息，非投资建议", "14");
}

/* =======================================================================
   15 — CRUDE TECHNICALS
   ===================================================================== */
{
  const s = slide();
  header(s, "CRUDE  ·  TECHNICALS", "原油 · 技术面与情景推演",
    "3月9日曾冲到 $119.47，目前 $78 — 现价距年内高点仍有约 35% 的距离");

  const lw = 7.5, rw = W - lw - 0.3;
  const h1 = 2.86;
  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "WTI 原油 2026 年走势  ·  示意", M + 0.3, BODY_TOP + 0.22, lw - 0.6);
  s.addChart(pres.ChartType.line, [{
    name: "WTI",
    labels: ["25年12月底", "26年1月", "3月9日高", "5月", "7月", "8月7日"],
    values: [55, 65, 119.47, 88, 73, 78.18],
  }], chartBase({
    x: M + 0.16, y: BODY_TOP + 0.6, w: lw - 0.32, h: h1 - 0.78,
    chartColors: ["C2703D"],
    lineSize: 3, lineSmooth: true,
    lineDataSymbol: "circle", lineDataSymbolSize: 7,
    lineDataSymbolLineColor: "C2703D", lineDataSymbolSolidFill: C.panel,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "$#,##0",
    valAxisMinVal: 40, valAxisMaxVal: 135,
    valAxisLabelFormatCode: "$#,##0",
  }));

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "波动特征", x2 + 0.3, BODY_TOP + 0.22, rw - 0.6);
  para(s,
    "52 周振幅超过 117%，是四个资产中波动最剧烈的。\n\n" +
    "价格几乎完全由新闻驱动：海峡谈判的每一次进退，都会在数小时内反映到盘面。\n\n" +
    "ASIC 对非黄金商品的零售杠杆上限为 10:1，比黄金还低。",
    x2 + 0.3, BODY_TOP + 0.7, rw - 0.6, h1 - 0.95, { size: 12, lineSpacing: 20 });

  const y3 = BODY_TOP + h1 + 0.26;
  const h3 = BODY_BOT - y3;
  panel(s, M, y3, W, h3);
  cardTitle(s, "三种情景  ·  风险框架，不是概率预测", M + 0.3, y3 + 0.2, W - 0.6);
  const sc = [
    ["停火 / 海峡重开", "地缘溢价迅速蒸发，向高盛 $56–60 目标区间靠拢", C.green],
    ["僵局延续", "在 $75–85 区间宽幅震荡，消息面反复拉锯", C.gold],
    ["冲突升级", "供应实质中断，重新测试 $100 以上，3月高点 $119 成为参考", C.red],
  ];
  sc.forEach((v, i) => {
    const ry = y3 + 0.56 + i * 0.4;
    s.addShape(pres.ShapeType.rect, {
      x: M + 0.3, y: ry + 0.1, w: 0.14, h: 0.14, fill: { color: v[2] },
    });
    s.addText(v[0], {
      x: M + 0.62, y: ry, w: 2.1, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: v[2], valign: "middle",
    });
    s.addText(v[1], {
      x: M + 2.86, y: ry, w: W - 3.16, h: 0.34, margin: 0,
      fontFace: F.body, fontSize: 11, color: C.txt, valign: "middle",
    });
  });

  footer(s, "图表为示意性走势 · 三种情景仅为风险框架说明，不是概率预测，更不是交易建议", "15");
}

/* =======================================================================
   16 — NEW: CROSS-ASSET / DIVERSIFICATION
   ===================================================================== */
{
  const s = slide();
  header(s, "CROSS-ASSET  ·  RISK", "跨资产联动 · 分散不等于对冲",
    "四个品种看起来毫不相关，但今天它们背后只有三个驱动因子");

  const h1 = 2.9;
  panel(s, M, BODY_TOP, W, h1);
  cardTitle(s, "驱动因子映射  ·  定性框架，非实测相关系数", M + 0.3, BODY_TOP + 0.2, W - 0.6);

  const colX = [M + 0.3, M + 2.9, M + 5.6, M + 8.3, M + 10.5];
  const colW = [2.5, 2.6, 2.6, 2.1, 1.4];
  const hdr = ["资产", "美联储 / 实际利率", "霍尔木兹地缘", "AI 资本开支", "杠杆上限"];
  hdr.forEach((t, i) => {
    s.addText(t, {
      x: colX[i], y: BODY_TOP + 0.6, w: colW[i], h: 0.3, margin: 0,
      fontFace: F.body, fontSize: 10.5, bold: true, color: C.dim,
      charSpacing: 0.6, valign: "middle",
    });
  });

  const grid = [
    ["黄金 XAU/USD", "强负相关", C.red, "避险买盘", C.green, "无直接关系", C.dim, "20:1"],
    ["纳指 NAS100", "强负相关", C.red, "间接（通胀）", C.gold, "核心驱动", C.green, "20:1"],
    ["Alphabet GOOGL", "负相关", C.red, "弱", C.dim, "核心驱动", C.green, "5:1"],
    ["WTI 原油", "弱", C.dim, "核心驱动", C.green, "无直接关系", C.dim, "10:1"],
  ];
  grid.forEach((r, i) => {
    const ry = BODY_TOP + 0.96 + i * 0.38;
    if (i % 2 === 1) {
      s.addShape(pres.ShapeType.rect, {
        x: M + 0.16, y: ry, w: W - 0.32, h: 0.38,
        fill: { color: C.panelHi }, line: { color: C.panelHi, width: 0 },
      });
    }
    s.addText(r[0], {
      x: colX[0], y: ry, w: colW[0], h: 0.38, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: C.txt, valign: "middle",
    });
    [[1, 2], [3, 4], [5, 6]].forEach((pair, j) => {
      s.addText(r[pair[0]], {
        x: colX[j + 1], y: ry, w: colW[j + 1], h: 0.38, margin: 0,
        fontFace: F.body, fontSize: 11, color: r[pair[1]], valign: "middle",
      });
    });
    s.addText(r[7], {
      x: colX[4], y: ry, w: colW[4], h: 0.38, margin: 0,
      fontFace: F.head, fontSize: 13, bold: true, color: C.gold, valign: "middle",
    });
  });

  para(s, "读法：同一行看这个品种被谁推动，同一列看哪些品种会一起动。三个因子同时转向时，四个品种可能同向下跌 — 这就是“分散”失效的时刻。",
    M + 0.3, BODY_TOP + 2.56, W - 0.6, 0.3,
    { size: 10.5, color: C.muted, italic: true });

  const y2 = BODY_TOP + h1 + 0.26;
  const h2 = BODY_BOT - y2;
  const cw = (W - 0.6) / 3;
  const notes = [
    ["客户最常见的误解", C.red,
      "“我买了黄金又买了纳指，所以我分散了。” — 两者都在对美联储路径下注，只是方向相反。这不是分散，是把仓位押在同一个宏观判断上。"],
    ["集中度怎么解释", C.gold,
      "纳指与 GOOGL 高度重叠：同时持有等于在 AI 资本开支这一个因子上加倍。可以问客户：“如果 AI 叙事松动，你有几个仓位会同时亏？”"],
    ["你能讲什么，不能讲什么", C.green,
      "可以讲：因子结构、波动来源、杠杆差异。不能讲：应该配多少、该买哪个、什么时候进出。前者是一般性信息，后者是个人建议。"],
  ];
  notes.forEach((n, i) => {
    const x = M + i * (cw + 0.3);
    panel(s, x, y2, cw, h2);
    cardTitle(s, n[0], x + 0.3, y2 + 0.2, cw - 0.6, n[1]);
    para(s, n[2], x + 0.3, y2 + 0.64, cw - 0.6, h2 - 0.84,
      { size: 10.5, color: C.txt, lineSpacing: 16 });
  });

  footer(s, "本表为定性框架，用于解释风险来源，不是统计相关系数，也不构成任何配置建议", "16");
}

/* =======================================================================
   17 — NEW: VALUATION & EARNINGS FRAMEWORK
   ===================================================================== */
{
  const s = slide();
  header(s, "VALUATION  ·  METHOD", "估值与财报：怎么读，怎么讲",
    "客户问“它到底贵不贵” — 你能给框架，不能给答案");

  const lw = 6.4, rw = W - lw - 0.3;
  const h1 = 2.94;

  panel(s, M, BODY_TOP, lw, h1);
  cardTitle(s, "现金流折现的三个输入  ·  DCF", M + 0.3, BODY_TOP + 0.2, lw - 0.6);
  const dcf = [
    ["01", "自由现金流", "经营现金流减去资本开支。Alphabet Q2 转负 $58.6 亿，就是因为分母端资本开支翻倍。"],
    ["02", "折现率 WACC", "无风险利率上行 → 折现率上行 → 远期现金流现值下降。这是“美联储鹰派压制成长股”的完整机制。"],
    ["03", "终值假设", "估值里最大的一块，也最主观。多数分歧不在明年，而在“十年后还剩多少增长”。"],
  ];
  dcf.forEach((d, i) => {
    const ry = BODY_TOP + 0.6 + i * 0.76;
    s.addText(d[0], {
      x: M + 0.3, y: ry, w: 0.42, h: 0.26, margin: 0,
      fontFace: F.head, fontSize: 12, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(d[1], {
      x: M + 0.78, y: ry, w: 1.7, h: 0.26, margin: 0,
      fontFace: F.body, fontSize: 11.5, bold: true, color: C.txt, valign: "middle",
    });
    para(s, d[2], M + 0.78, ry + 0.28, lw - 1.08, 0.46, { size: 10.5, color: C.muted, lineSpacing: 15 });
  });

  const x2 = M + lw + 0.3;
  panel(s, x2, BODY_TOP, rw, h1, { fill: C.panelHi });
  cardTitle(s, "财报季：超预期为什么不等于上涨", x2 + 0.3, BODY_TOP + 0.2, rw - 0.6);
  para(s,
    "股价反映的是预期差，不是绝对好坏。Alphabet Q2 EPS $9.11 对预期 $2.89 — 数字漂亮，股价却没动。",
    x2 + 0.3, BODY_TOP + 0.62, rw - 0.6, 0.6, { size: 11.5, lineSpacing: 18 });
  const chk = [
    "看指引，不只看本季 — 全年资本开支指引才是重点",
    "看现金流表，不只看利润表",
    "看融资动作：增发 $496 亿 + 发债 $203 亿说明什么",
    "看财报后的分析师目标价调整方向",
  ];
  bullets(s, chk, x2 + 0.3, BODY_TOP + 1.34, rw - 0.6, h1 - 1.56, { size: 11, gap: 14 });

  const y2 = BODY_TOP + h1 + 0.26;
  const h2 = BODY_BOT - y2;
  const cw = (W - 0.3) / 2;

  panel(s, M, y2, cw, h2, { fill: C.panelHi });
  cardTitle(s, "可以这样说", M + 0.3, y2 + 0.22, cw - 0.6, C.green);
  bullets(s, [
    "“市场现在争论的是资本开支什么时候转化成收入。”",
    "“自由现金流转负，意味着估值模型的输入变了。”",
    "“分析师目标价从 $X 到 $Y，分歧本身就是波动来源。”",
  ], M + 0.3, y2 + 0.62, cw - 0.6, h2 - 0.8, { size: 10.5, gap: 6, color: C.txt });

  const x3 = M + cw + 0.3;
  panel(s, x3, y2, cw, h2, { fill: C.redBg, line: "48282C" });
  cardTitle(s, "绝对不能这样说", x3 + 0.3, y2 + 0.22, cw - 0.6, C.red);
  bullets(s, [
    "“现在这个价位很便宜，可以进。”",
    "“我算过它值 $XXX，现在被低估了。”",
    "“财报这么好，下周肯定涨。”",
  ], x3 + 0.3, y2 + 0.62, cw - 0.6, h2 - 0.8, { size: 10.5, gap: 6, color: C.txt });

  footer(s, "估值框架为一般性教育内容 · 任何具体目标价、买卖时点或仓位建议都属于个人建议，未获授权不得提供", "17");
}

/* =======================================================================
   18 — BEFORE YOU USE THIS
   ===================================================================== */
{
  const s = slide(C.bgDeep);
  header(s, "BEFORE YOU USE THIS", "使用这份材料之前", "三件必须做的事");

  const cw = (W - 0.6) / 3;
  const ch = 2.5;
  const items = [
    ["01", "所有价位重新复核", "本材料数据截至 2026年8月8日。任何对外引用的价格、均线、点差，都必须以 TMGM 实时数据为准。"],
    ["02", "送合规部门审核", "这是内部准备材料。任何要发给客户或代理的版本，必须先经 TMGM 合规审核。"],
    ["03", "确认你的授权范围", "向任何客户讲这些分析之前，先向主管书面确认：你是否被授权提供一般性建议？这关系到你个人的法律责任。"],
  ];
  items.forEach((it, i) => {
    const x = M + i * (cw + 0.3);
    panel(s, x, BODY_TOP, cw, ch);
    s.addText(it[0], {
      x: x + 0.32, y: BODY_TOP + 0.26, w: 1.0, h: 0.56, margin: 0,
      fontFace: F.head, fontSize: 30, bold: true, color: C.gold, valign: "middle",
    });
    s.addText(it[1], {
      x: x + 0.32, y: BODY_TOP + 0.94, w: cw - 0.64, h: 0.32, margin: 0,
      fontFace: F.body, fontSize: 14, bold: true, color: C.txt, valign: "middle",
    });
    para(s, it[2], x + 0.32, BODY_TOP + 1.34, cw - 0.64, ch - 1.56,
      { size: 11, color: C.muted, lineSpacing: 18 });
  });

  const y2 = BODY_TOP + ch + 0.3;
  const h2 = 1.5;
  panel(s, M, y2, W, h2, { fill: C.redBg, line: "48282C" });
  cardTitle(s, "风险披露", M + 0.34, y2 + 0.22, 4.0, C.red);
  para(s,
    "差价合约 (CFD) 是复杂的杠杆金融产品，存在快速亏损的高风险。大多数零售投资者在交易 CFD 时亏损。本材料为一般性信息，未考虑任何个人的投资目标、财务状况或需求，不构成个人建议。交易前请阅读 PDS、FSG 与目标市场认定 (TMD)。",
    M + 0.34, y2 + 0.62, W - 0.68, h2 - 0.86, { size: 11.5, color: C.txt, lineSpacing: 19 });

  footer(s, "Trademax Australia Limited  ·  ASIC AFSL 436416", "18");
}

pres.writeFile({ fileName: "TMGM_AccountManager_v3.pptx" })
  .then(f => console.log("written:", f));
