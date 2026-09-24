"""Shared layout toolkit for the portfolio PDFs.

Keeps the two build scripts declarative: they describe content, this module
owns every visual decision so both documents come out looking like one set.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

# ---------------------------------------------------------------- palette --
INK        = colors.HexColor("#15202B")   # body text
MUTED      = colors.HexColor("#5B6B7B")   # captions, secondary
HAIRLINE   = colors.HexColor("#D8E0E8")   # rules, table grid
PAPER      = colors.HexColor("#FFFFFF")
WASH       = colors.HexColor("#F4F7FA")   # table zebra / callout ground
ACCENT     = colors.HexColor("#0F6F8C")   # headings, links
ACCENT_DK  = colors.HexColor("#0A4E63")
FLAG       = colors.HexColor("#B4341F")   # the number that matters

PAGE_W, PAGE_H = A4
MARGIN_X = 20 * mm
MARGIN_T = 18 * mm
MARGIN_B = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

# ----------------------------------------------------------------- styles --
def _p(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK,
                spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "title":     _p("title", fontName="Helvetica-Bold", fontSize=25, leading=30,
                    textColor=INK, spaceAfter=3),
    "subtitle":  _p("subtitle", fontSize=12.5, leading=17, textColor=ACCENT,
                    spaceAfter=14),
    "byline":    _p("byline", fontSize=10, leading=15, textColor=MUTED),
    "h1":        _p("h1", fontName="Helvetica-Bold", fontSize=15, leading=19,
                    textColor=ACCENT_DK, spaceBefore=16, spaceAfter=7,
                    keepWithNext=True),
    "h2":        _p("h2", fontName="Helvetica-Bold", fontSize=11, leading=15,
                    textColor=INK, spaceBefore=11, spaceAfter=4,
                    keepWithNext=True),
    "body":      _p("body", spaceAfter=7),
    "lead":      _p("lead", fontSize=10.5, leading=16, spaceAfter=9),
    "caption":   _p("caption", fontSize=8, leading=11, textColor=MUTED,
                    spaceBefore=3, spaceAfter=11, alignment=TA_CENTER),
    "cell":      _p("cell", fontSize=8.5, leading=11.5),
    "cellb":     _p("cellb", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5),
    "cellc":     _p("cellc", fontSize=8.5, leading=11.5, alignment=TA_CENTER),
    "head":      _p("head", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5,
                    textColor=PAPER),
    "headc":     _p("headc", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5,
                    textColor=PAPER, alignment=TA_CENTER),
    "note":      _p("note", fontSize=8, leading=12, textColor=MUTED, spaceAfter=6),
    "callout":   _p("callout", fontSize=9.5, leading=14.5),
}


def para(text, style="body"):
    return Paragraph(text, S[style])


def h1(text):
    return Paragraph(text, S["h1"])


def h2(text):
    return Paragraph(text, S["h2"])


def rule(space_before=2, space_after=8, color=HAIRLINE):
    t = Table([[""]], colWidths=[CONTENT_W], rowHeights=[0.1])
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.6, color)]))
    return [Spacer(1, space_before), t, Spacer(1, space_after)]


def bullets(items, style="body"):
    """Hanging-indent list — reportlab's bulletText loses the hang on wrap."""
    rows = [[Paragraph("&bull;", S[style]), Paragraph(t, S[style])] for t in items]
    t = Table(rows, colWidths=[5 * mm, CONTENT_W - 5 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def figure(path, caption=None, max_w_mm=None, max_h_mm=105):
    """Scale to fit the column, capped in height so a figure + its text stay
    on one page."""
    iw, ih = ImageReader(path).getSize()
    max_w = (max_w_mm * mm) if max_w_mm else CONTENT_W
    scale = min(max_w / iw, (max_h_mm * mm) / ih)
    img = Image(path, iw * scale, ih * scale)
    img.hAlign = "CENTER"
    if caption:
        return KeepTogether([img, Paragraph(caption, S["caption"])])
    return KeepTogether([img, Spacer(1, 9)])


def table(rows, widths=None, align_center_from=1, head=True, flag_cells=()):
    """rows[0] is the header. `flag_cells` are (row, col) 1-indexed data cells
    to print in the accent-red that marks the number the reader should catch."""
    n = len(rows[0])
    widths = widths or [CONTENT_W / n] * n
    data = []
    for r_i, row in enumerate(rows):
        out = []
        for c_i, cell in enumerate(row):
            txt = str(cell)
            if head and r_i == 0:
                st = "headc" if c_i >= align_center_from else "head"
            else:
                st = "cellc" if c_i >= align_center_from else "cell"
                if (r_i, c_i) in flag_cells:
                    txt = f'<font color="#B4341F"><b>{txt}</b></font>'
            out.append(Paragraph(txt, S[st]))
        data.append(out)

    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, HAIRLINE),
        ("BOX", (0, 0), (-1, -1), 0.5, HAIRLINE),
    ]
    if head:
        style += [("BACKGROUND", (0, 0), (-1, 0), ACCENT_DK)]
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), WASH))
    t.setStyle(TableStyle(style))
    return t


def callout(text, label=None, tint=WASH, bar=ACCENT):
    """Left-barred block for the 'so what' line after a finding."""
    inner = []
    if label:
        inner.append(Paragraph(
            f'<font color="#0A4E63"><b>{label}</b></font>', S["callout"]))
    inner.append(Paragraph(text, S["callout"]))
    body = Table([[i] for i in inner], colWidths=[CONTENT_W - 8 * mm])
    body.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    t = Table([[body]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 7 * mm - 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([t, Spacer(1, 9)])


def metric_row(items):
    """Top-line KPI strip: list of (value, label, flagged?)."""
    cells = []
    for value, label, *rest in items:
        flagged = rest[0] if rest else False
        col = FLAG if flagged else ACCENT_DK
        cells.append([
            Paragraph(f'<font color="#{col.hexval()[2:]}" size="17"><b>{value}</b></font>',
                      _p("v", alignment=TA_CENTER, leading=21)),
            Paragraph(label, _p("l", fontSize=7.6, leading=10,
                                textColor=MUTED, alignment=TA_CENTER)),
        ])
    w = CONTENT_W / len(cells)
    t = Table([[Table([[c[0]], [c[1]]], colWidths=[w - 4]) for c in cells]],
              colWidths=[w] * len(cells))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WASH),
        ("BOX", (0, 0), (-1, -1), 0.5, HAIRLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return KeepTogether([t, Spacer(1, 11)])


# ------------------------------------------------------------- document ----
class Doc(BaseDocTemplate):
    def __init__(self, path, footer_left, **kw):
        super().__init__(path, pagesize=A4,
                         leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                         topMargin=MARGIN_T, bottomMargin=MARGIN_B, **kw)
        self.footer_left = footer_left
        frame = Frame(MARGIN_X, MARGIN_B, CONTENT_W,
                      PAGE_H - MARGIN_T - MARGIN_B, id="main",
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame]),
            PageTemplate(id="body", frames=[frame], onPage=self._chrome),
        ])

    def _chrome(self, canvas, doc):
        canvas.saveState()
        y = MARGIN_B - 6 * mm
        canvas.setStrokeColor(HAIRLINE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_X, y + 4 * mm, PAGE_W - MARGIN_X, y + 4 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_X, y, self.footer_left)
        canvas.drawRightString(PAGE_W - MARGIN_X, y, str(canvas.getPageNumber()))
        canvas.restoreState()


def cover(title, subtitle, author, stack, repo, blurb, metrics=None):
    """Full-bleed-ish cover: rule, title, stack chips, one-paragraph pitch."""
    el = [Spacer(1, 26 * mm)]
    bar = Table([[""]], colWidths=[34 * mm], rowHeights=[2.4])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    bar.hAlign = "LEFT"
    el += [bar, Spacer(1, 7 * mm)]
    el += [Paragraph(title, S["title"]), Paragraph(subtitle, S["subtitle"])]
    el += rule(0, 7)
    el += [Paragraph(author, S["byline"]),
           Paragraph(f'<font color="#5B6B7B">{stack}</font>', S["byline"]),
           Paragraph(f'<font color="#0F6F8C">{repo}</font>', S["byline"]),
           Spacer(1, 10 * mm)]
    if metrics:
        el.append(metric_row(metrics))
        el.append(Spacer(1, 3 * mm))
    el.append(Paragraph(blurb, S["lead"]))
    return el


def bind_headings(story):
    """reportlab's `keepWithNext` does not see through a KeepTogether wrapper,
    so a heading followed by a figure can still be orphaned at a page foot.
    Merge each heading into the KeepTogether that follows it."""
    out = []
    i = 0
    while i < len(story):
        cur = story[i]
        nxt = story[i + 1] if i + 1 < len(story) else None
        is_head = (isinstance(cur, Paragraph)
                   and getattr(cur.style, "keepWithNext", False))
        if is_head and isinstance(nxt, KeepTogether):
            out.append(KeepTogether([cur] + list(nxt._content)))
            i += 2
            continue
        out.append(cur)
        i += 1
    return out
