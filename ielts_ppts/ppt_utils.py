from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import copy

# Brand colors
C_DARK   = RGBColor(0x1B, 0x3A, 0x6B)  # deep navy
C_ACCENT = RGBColor(0xE8, 0x8C, 0x00)  # gold
C_LIGHT  = RGBColor(0xF0, 0xF4, 0xFF)  # pale blue bg
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY   = RGBColor(0x55, 0x65, 0x80)
C_RED    = RGBColor(0xD0, 0x2B, 0x2B)
C_GREEN  = RGBColor(0x1A, 0x7A, 0x3C)

W, H = Inches(13.33), Inches(7.5)  # widescreen 16:9


def new_prs():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs


def blank_slide(prs):
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)


def fill_shape(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    fill_shape(shape, color)
    shape.line.fill.background()
    return shape


def set_tf(tf, text, size, bold=False, color=C_WHITE, align=PP_ALIGN.LEFT, italic=False):
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = align
    run = para.runs[0] if para.runs else para.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def add_textbox(slide, text, l, t, w, h, size=18, bold=False,
                color=C_DARK, align=PP_ALIGN.LEFT, italic=False):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = align
    run = para.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_para(tf, text, size=16, bold=False, color=C_DARK,
             align=PP_ALIGN.LEFT, italic=False, space_before=6):
    para = tf.add_paragraph()
    para.alignment = align
    para.space_before = Pt(space_before)
    run = para.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return para


# ── Slide templates ──────────────────────────────────────────────────────────

def make_cover(prs, title, subtitle, tag):
    """Full-bleed cover slide."""
    slide = blank_slide(prs)
    # BG
    add_rect(slide, 0, 0, 13.33, 7.5, C_DARK)
    # accent bar left
    add_rect(slide, 0, 0, 0.35, 7.5, C_ACCENT)
    # title
    add_textbox(slide, title, 0.7, 1.8, 11.5, 2.2, size=44, bold=True,
                color=C_WHITE, align=PP_ALIGN.LEFT)
    # subtitle
    add_textbox(slide, subtitle, 0.7, 4.0, 10.5, 1.2, size=22,
                color=RGBColor(0xCC, 0xDD, 0xFF), align=PP_ALIGN.LEFT)
    # tag chip
    chip = slide.shapes.add_shape(1, Inches(0.7), Inches(5.4), Inches(3.5), Inches(0.55))
    fill_shape(chip, C_ACCENT)
    chip.line.fill.background()
    add_textbox(slide, tag, 0.85, 5.43, 3.3, 0.5, size=14, bold=True,
                color=C_WHITE, align=PP_ALIGN.LEFT)
    # bottom note
    add_textbox(slide, "专为深圳雅思学员设计 | 40课时完整提分体系",
                0.7, 6.7, 11.5, 0.6, size=13, color=C_ACCENT)
    return slide


def make_lesson_title(prs, lesson_no, lesson_title, objectives):
    """Lesson opener: big number + objectives."""
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_LIGHT)
    add_rect(slide, 0, 0, 4.5, 7.5, C_DARK)
    # big lesson number
    add_textbox(slide, f"L{lesson_no:02d}", 0.3, 0.5, 3.8, 2.5,
                size=96, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
    # lesson title on dark panel
    add_textbox(slide, lesson_title, 0.3, 3.2, 3.9, 2.5,
                size=20, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    # objectives box
    add_textbox(slide, "本课目标 Learning Objectives", 5.0, 0.5, 7.8, 0.6,
                size=16, bold=True, color=C_DARK)
    txb = slide.shapes.add_textbox(Inches(5.0), Inches(1.3), Inches(7.8), Inches(5.5))
    tf  = txb.text_frame
    tf.word_wrap = True
    first = True
    for obj in objectives:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(10)
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = f"✦  {obj}"
        r.font.size = Pt(17)
        r.font.color.rgb = C_DARK
    return slide


def make_content(prs, title, points, note=None, accent_bar=True):
    """Standard content slide with bullet points."""
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_WHITE)
    if accent_bar:
        add_rect(slide, 0, 0, 13.33, 0.9, C_DARK)
        add_rect(slide, 0, 0.9, 13.33, 0.07, C_ACCENT)
        add_textbox(slide, title, 0.4, 0.1, 12.5, 0.72,
                    size=22, bold=True, color=C_WHITE)
    top = 1.2
    txb = slide.shapes.add_textbox(Inches(0.5), Inches(top),
                                   Inches(12.3), Inches(7.5 - top - 0.4))
    tf  = txb.text_frame
    tf.word_wrap = True
    first = True
    for pt in points:
        if isinstance(pt, tuple):
            head, body = pt
            if first:
                p = tf.paragraphs[0]; first = False
            else:
                p = tf.add_paragraph()
                p.space_before = Pt(8)
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = f"▶  {head}"
            r.font.size = Pt(19)
            r.font.bold = True
            r.font.color.rgb = C_DARK
            p2 = tf.add_paragraph()
            p2.space_before = Pt(2)
            p2.alignment = PP_ALIGN.LEFT
            r2 = p2.add_run()
            r2.text = f"    {body}"
            r2.font.size = Pt(16)
            r2.font.color.rgb = C_GRAY
        else:
            if first:
                p = tf.paragraphs[0]; first = False
            else:
                p = tf.add_paragraph()
                p.space_before = Pt(8)
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = f"◆  {pt}"
            r.font.size = Pt(18)
            r.font.color.rgb = C_DARK
    if note:
        add_rect(slide, 0.4, 6.8, 12.5, 0.55, C_LIGHT)
        add_textbox(slide, f"⚠  深圳学生注意：{note}", 0.55, 6.82, 12.2, 0.5,
                    size=13, color=C_RED, italic=True)
    return slide


def make_two_col(prs, title, left_title, left_items, right_title, right_items):
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_WHITE)
    add_rect(slide, 0, 0, 13.33, 0.9, C_DARK)
    add_rect(slide, 0, 0.9, 13.33, 0.07, C_ACCENT)
    add_textbox(slide, title, 0.4, 0.1, 12.5, 0.72, size=22, bold=True, color=C_WHITE)
    # divider
    add_rect(slide, 6.6, 1.1, 0.05, 6.2, C_LIGHT)
    for col, (ct, items) in enumerate([(left_title, left_items), (right_title, right_items)]):
        lx = 0.4 if col == 0 else 6.8
        add_textbox(slide, ct, lx, 1.1, 6.0, 0.5, size=17, bold=True,
                    color=C_ACCENT)
        txb = slide.shapes.add_textbox(Inches(lx), Inches(1.75), Inches(6.0), Inches(5.4))
        tf  = txb.text_frame; tf.word_wrap = True
        first = True
        for item in items:
            if first:
                p = tf.paragraphs[0]; first = False
            else:
                p = tf.add_paragraph(); p.space_before = Pt(7)
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = f"• {item}"
            r.font.size = Pt(16)
            r.font.color.rgb = C_DARK
    return slide


def make_example(prs, title, question, answer=None, tips=None):
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_WHITE)
    add_rect(slide, 0, 0, 13.33, 0.9, C_DARK)
    add_rect(slide, 0, 0.9, 13.33, 0.07, C_ACCENT)
    add_textbox(slide, title, 0.4, 0.1, 12.5, 0.72, size=22, bold=True, color=C_WHITE)
    # Question box
    add_rect(slide, 0.4, 1.1, 12.5, 0.35, C_ACCENT)
    add_textbox(slide, "【题目示例 / Example】", 0.55, 1.12, 5.0, 0.32,
                size=13, bold=True, color=C_WHITE)
    qbox = slide.shapes.add_textbox(Inches(0.4), Inches(1.5), Inches(12.5), Inches(2.5))
    tf = qbox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run()
    r.text = question; r.font.size = Pt(17); r.font.color.rgb = C_DARK
    if answer:
        add_rect(slide, 0.4, 4.1, 12.5, 0.35, C_GREEN)
        add_textbox(slide, "【参考答案 / Answer】", 0.55, 4.12, 5.0, 0.32,
                    size=13, bold=True, color=C_WHITE)
        abox = slide.shapes.add_textbox(Inches(0.4), Inches(4.5), Inches(12.5), Inches(1.3))
        tf2 = abox.text_frame; tf2.word_wrap = True
        p2 = tf2.paragraphs[0]; r2 = p2.add_run()
        r2.text = answer; r2.font.size = Pt(16); r2.font.color.rgb = C_GREEN
    if tips:
        y = 5.9 if answer else 4.1
        add_rect(slide, 0.4, y, 12.5, 0.35, C_LIGHT)
        add_textbox(slide, "💡 解题技巧", 0.55, y+0.02, 3.0, 0.32,
                    size=13, bold=True, color=C_DARK)
        tbox = slide.shapes.add_textbox(Inches(0.4), Inches(y+0.4), Inches(12.5), Inches(1.2))
        tf3 = tbox.text_frame; tf3.word_wrap = True
        p3 = tf3.paragraphs[0]; r3 = p3.add_run()
        r3.text = tips; r3.font.size = Pt(15); r3.font.color.rgb = C_GRAY
    return slide


def make_summary(prs, lesson_no, key_points, homework):
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_DARK)
    add_rect(slide, 0, 0, 0.35, 7.5, C_ACCENT)
    add_textbox(slide, f"L{lesson_no:02d} 课堂小结 Summary", 0.7, 0.3, 12.0, 0.8,
                size=26, bold=True, color=C_WHITE)
    add_textbox(slide, "📌 本课核心要点", 0.7, 1.3, 6.0, 0.5,
                size=16, bold=True, color=C_ACCENT)
    txb = slide.shapes.add_textbox(Inches(0.7), Inches(1.9), Inches(5.8), Inches(4.5))
    tf  = txb.text_frame; tf.word_wrap = True
    first = True
    for kp in key_points:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph(); p.space_before = Pt(8)
        r = p.add_run(); r.text = f"✓  {kp}"
        r.font.size = Pt(16); r.font.color.rgb = C_WHITE
    add_rect(slide, 7.0, 1.3, 5.9, 5.0, RGBColor(0x0D, 0x24, 0x4A))
    add_textbox(slide, "📝 课后作业 Homework", 7.2, 1.4, 5.5, 0.5,
                size=16, bold=True, color=C_ACCENT)
    txb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.0), Inches(5.5), Inches(4.0))
    tf2  = txb2.text_frame; tf2.word_wrap = True
    first = True
    for hw in homework:
        if first:
            p = tf2.paragraphs[0]; first = False
        else:
            p = tf2.add_paragraph(); p.space_before = Pt(8)
        r = p.add_run(); r.text = f"→  {hw}"
        r.font.size = Pt(15); r.font.color.rgb = C_WHITE


def make_pain_point(prs, title, problems, solutions):
    """Shenzhen-specific pain point slide."""
    slide = blank_slide(prs)
    add_rect(slide, 0, 0, 13.33, 7.5, C_WHITE)
    add_rect(slide, 0, 0, 13.33, 0.9, RGBColor(0x8B, 0x00, 0x00))
    add_rect(slide, 0, 0.9, 13.33, 0.07, C_ACCENT)
    add_textbox(slide, f"🎯 深圳学生高频痛点  {title}", 0.4, 0.1, 12.5, 0.72,
                size=20, bold=True, color=C_WHITE)
    add_textbox(slide, "❌ 常见误区", 0.4, 1.1, 6.0, 0.5,
                size=16, bold=True, color=C_RED)
    txb = slide.shapes.add_textbox(Inches(0.4), Inches(1.65), Inches(6.0), Inches(5.4))
    tf  = txb.text_frame; tf.word_wrap = True
    first = True
    for p_item in problems:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph(); p.space_before = Pt(8)
        r = p.add_run(); r.text = f"✗  {p_item}"
        r.font.size = Pt(16); r.font.color.rgb = C_RED
    add_rect(slide, 6.7, 1.1, 0.05, 6.1, C_LIGHT)
    add_textbox(slide, "✅ 正确方法", 6.9, 1.1, 6.0, 0.5,
                size=16, bold=True, color=C_GREEN)
    txb2 = slide.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(6.0), Inches(5.4))
    tf2  = txb2.text_frame; tf2.word_wrap = True
    first = True
    for s_item in solutions:
        if first:
            p = tf2.paragraphs[0]; first = False
        else:
            p = tf2.add_paragraph(); p.space_before = Pt(8)
        r = p.add_run(); r.text = f"✓  {s_item}"
        r.font.size = Pt(16); r.font.color.rgb = C_GREEN
    return slide
