"""
STAT3888 Statistical Machine Learning — slide-deck framework.
Builds self-contained HTML lecture decks (open in any browser, print to PDF).

A deck is a list of "slide" HTML strings produced by the helper functions
below. Figures are generated with matplotlib into ./figures and referenced
by relative path so the decks stay small and the repo stays clean.

Author: teaching materials for USYD STAT3888.
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------- palette
INK       = "#1b2430"
MUTED     = "#5b6a7d"
ACCENT    = "#E64626"   # USYD ochre-red
BLUE      = "#2A6F97"
TEAL      = "#2A9D8F"
GOLD      = "#E9AF4B"
PURPLE    = "#8E7DBE"
GREY      = "#8a97a6"
PANEL     = "#f4f6f9"
CAT = [BLUE, ACCENT, TEAL, GOLD, PURPLE, GREY]

# ---------------------------------------------------------------- matplotlib defaults
def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 130,
        "savefig.dpi": 130,
        "font.size": 13,
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#c7d0da",
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "grid.color": "#e6ebf1",
        "grid.linewidth": 1.0,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "legend.frameon": False,
    })
    return plt

def savefig(fig, name):
    path = os.path.join(FIGDIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return f"figures/{name}"

# ---------------------------------------------------------------- slide builders
def title_slide(number, title, subtitle, unit="STAT3888 · Statistical Machine Learning"):
    return f"""
    <section class="slide title">
      <div class="badge">Lecture {number:02d}</div>
      <h1>{html.escape(title)}</h1>
      <p class="sub">{subtitle}</p>
      <div class="tfoot">
        <span>{unit}</span>
        <span>The University of Sydney · School of Mathematics &amp; Statistics</span>
      </div>
    </section>"""

def objectives_slide(items):
    lis = "\n".join(f"<li>{x}</li>" for x in items)
    return f"""
    <section class="slide">
      <h2><span class="kicker">Learning objectives</span>By the end of this lecture you can…</h2>
      <ul class="obj">{lis}</ul>
    </section>"""

def content_slide(title, body, kicker=None):
    k = f'<span class="kicker">{kicker}</span>' if kicker else ""
    return f"""
    <section class="slide">
      <h2>{k}{html.escape(title)}</h2>
      {body}
    </section>"""

def figure_slide(title, figpath, caption="", kicker=None, side=None):
    k = f'<span class="kicker">{kicker}</span>' if kicker else ""
    cap = f'<p class="cap">{caption}</p>' if caption else ""
    if side:
        return f"""
    <section class="slide">
      <h2>{k}{html.escape(title)}</h2>
      <div class="split">
        <div class="fig"><img src="{figpath}" alt="{html.escape(title)}">{cap}</div>
        <div class="side">{side}</div>
      </div>
    </section>"""
    return f"""
    <section class="slide">
      <h2>{k}{html.escape(title)}</h2>
      <div class="fig center"><img src="{figpath}" alt="{html.escape(title)}">{cap}</div>
    </section>"""

def exercise_slide(title, prompt, hint=None):
    h = f'<div class="hint"><b>Hint.</b> {hint}</div>' if hint else ""
    return f"""
    <section class="slide exercise">
      <h2><span class="kicker">In-class exercise</span>{html.escape(title)}</h2>
      <div class="exbody">{prompt}</div>
      {h}
    </section>"""

def summary_slide(points, nextup=None):
    lis = "\n".join(f"<li>{x}</li>" for x in points)
    nx = f'<div class="next"><b>Next lecture →</b> {nextup}</div>' if nextup else ""
    return f"""
    <section class="slide">
      <h2><span class="kicker">Summary</span>Key takeaways</h2>
      <ul class="take">{lis}</ul>
      {nx}
    </section>"""

# small inline helpers -----------------------------------------------------
def cols(*blocks):
    inner = "".join(f'<div class="col">{b}</div>' for b in blocks)
    return f'<div class="cols">{inner}</div>'

def card(title, body, tone="blue"):
    return f'<div class="card {tone}"><h4>{title}</h4>{body}</div>'

def code(src, lang="r"):
    return f'<pre class="code"><code>{html.escape(src)}</code></pre>'

def formula(tex_like):
    return f'<div class="formula">{tex_like}</div>'

def callout(body, tone="tip"):
    return f'<div class="callout {tone}">{body}</div>'

# ---------------------------------------------------------------- page assembly
CSS = """
:root{--ink:#1b2430;--muted:#5b6a7d;--accent:#E64626;--blue:#2A6F97;
--teal:#2A9D8F;--gold:#E9AF4B;--panel:#f4f6f9;--line:#dce3ec;}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif;
color:var(--ink);background:#404a57;}
.deck{max-width:1120px;margin:0 auto;}
.slide{position:relative;background:#fff;min-height:640px;margin:26px auto;
padding:54px 62px 66px;border-radius:14px;box-shadow:0 10px 34px rgba(0,0,0,.25);
display:flex;flex-direction:column;}
.slide::after{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;
background:linear-gradient(#E64626,#b8331b);border-radius:14px 0 0 14px;}
h1{font-size:44px;line-height:1.1;margin:.2em 0 .3em;letter-spacing:-.5px}
h2{font-size:30px;margin:0 0 22px;line-height:1.15;letter-spacing:-.3px}
h2 .kicker,.kicker{display:block;font-size:13px;font-weight:700;letter-spacing:.14em;
text-transform:uppercase;color:var(--accent);margin-bottom:6px}
h4{margin:0 0 8px;font-size:17px}
p,li{font-size:19px;line-height:1.5;color:#26303c}
.sub{font-size:22px;color:var(--muted);max-width:44ch}
.title{justify-content:center}
.badge{display:inline-block;align-self:flex-start;background:var(--accent);color:#fff;
font-weight:700;font-size:14px;letter-spacing:.1em;padding:7px 14px;border-radius:30px}
.tfoot{position:absolute;left:62px;right:62px;bottom:30px;display:flex;
justify-content:space-between;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:12px}
ul.obj li{margin:12px 0;padding-left:6px}
ul.obj{padding-left:22px}
ul.take li{margin:12px 0}
.cols{display:flex;gap:22px;margin-top:6px}
.col{flex:1}
.split{display:flex;gap:30px;align-items:flex-start}
.split .fig{flex:1.15}.split .side{flex:.85}
.fig img{max-width:100%;border-radius:10px;border:1px solid var(--line)}
.fig.center{text-align:center}
.cap{color:var(--muted);font-size:15px;margin-top:10px}
.card{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:10px 0;background:var(--panel)}
.card h4{color:var(--blue)}
.card.red h4{color:var(--accent)} .card.teal h4{color:var(--teal)}
.card.gold h4{color:#b98416}
.card p,.card li{font-size:17px}
.formula{background:#0f1720;color:#eaf2fb;border-radius:10px;padding:16px 20px;margin:14px 0;
font-family:'Cambria Math','Georgia',serif;font-size:22px;text-align:center;letter-spacing:.3px}
.formula .v{color:#ffd08a;font-style:italic}
pre.code{background:#0f1720;color:#e6edf3;border-radius:10px;padding:16px 18px;overflow:auto;
font-family:'JetBrains Mono','Consolas',monospace;font-size:15px;line-height:1.5}
pre.code code{color:#e6edf3}
.callout{border-radius:10px;padding:14px 18px;margin:12px 0;font-size:17px;border-left:5px solid}
.callout.tip{background:#eef6f4;border-color:var(--teal)}
.callout.warn{background:#fdf0ec;border-color:var(--accent)}
.callout.key{background:#eef3f9;border-color:var(--blue)}
.exercise{background:linear-gradient(180deg,#fff,#fbf3f0)}
.exbody{font-size:20px}
.exbody ol{padding-left:22px}.exbody li{margin:9px 0}
.hint{margin-top:16px;background:#fff6ee;border:1px dashed var(--gold);border-radius:10px;padding:12px 16px;font-size:17px}
.next{margin-top:20px;background:var(--panel);border-radius:10px;padding:12px 16px;font-size:17px;color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:17px}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left}
th{background:var(--panel);color:var(--ink)}
.pill{display:inline-block;background:var(--blue);color:#fff;border-radius:20px;padding:3px 12px;font-size:14px;font-weight:600;margin:2px}
.nav{position:fixed;right:16px;bottom:16px;background:#1b2430cc;color:#fff;border-radius:30px;
padding:8px 16px;font-size:13px;backdrop-filter:blur(4px);z-index:9}
@media print{
  body{background:#fff}
  .slide{box-shadow:none;margin:0;border-radius:0;page-break-after:always;min-height:96vh}
  .nav{display:none}
}
"""

JS = """
<script>
const s=[...document.querySelectorAll('.slide')];let i=0;
const nav=document.querySelector('.nav .n');
function go(n){i=Math.max(0,Math.min(s.length-1,n));s[i].scrollIntoView({behavior:'smooth'});nav.textContent=(i+1)+' / '+s.length;}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();go(i+1)}if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(i-1)}});
const io=new IntersectionObserver(es=>{es.forEach(x=>{if(x.isIntersecting){i=s.indexOf(x.target);nav.textContent=(i+1)+' / '+s.length;}})},{threshold:.5});
s.forEach(x=>io.observe(x));
</script>
"""

def build(slides, out_path, page_title):
    body = "\n".join(slides)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)}</title><style>{CSS}</style></head>
<body><div class="deck">{body}</div>
<div class="nav"><span class="n">1 / {len(slides)}</span> · ← → to navigate</div>
{JS}</body></html>"""
    with open(out_path, "w") as f:
        f.write(doc)
    return out_path
