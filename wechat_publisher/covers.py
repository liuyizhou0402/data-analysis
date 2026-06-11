# -*- coding: utf-8 -*-
"""用 Pillow 生成公众号封面图（900x383，微信推荐比例 2.35:1）。

不依赖外部图库 API，纯本地渐变底 + 标题文字，三篇文章用不同配色。
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 900, 383

PALETTES = [
    ((20, 70, 160), (90, 170, 250)),    # 蓝 — 澳新热点
    ((120, 30, 50), (220, 90, 110)),    # 红 — 英国申请
    ((20, 110, 90), (110, 200, 170)),   # 绿 — 专业解析
]

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]


def _font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _wrap(text: str, font, max_width: int, draw) -> list[str]:
    lines, line = [], ""
    for ch in text:
        if draw.textlength(line + ch, font=font) > max_width:
            lines.append(line)
            line = ch
        else:
            line += ch
    if line:
        lines.append(line)
    return lines[:3]


def make_cover(title: str, badge: str, palette_index: int, out_path: str) -> str:
    c1, c2 = PALETTES[palette_index % len(PALETTES)]
    img = Image.new("RGB", (W, H))
    # 纵向渐变
    for y in range(H):
        t = y / H
        img.paste(tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)), (0, y, W, y + 1))
    draw = ImageDraw.Draw(img)

    # 装饰圆点
    rnd = random.Random(title)
    for _ in range(20):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(2, 6)
        draw.ellipse((x, y, x + r, y + r), fill=(255, 255, 255, 60))

    # 角标
    badge_font = _font(26)
    draw.rounded_rectangle((40, 36, 40 + draw.textlength(badge, font=badge_font) + 36, 86),
                           radius=25, fill=(255, 255, 255))
    draw.text((58, 44), badge, font=badge_font, fill=c1)

    # 标题
    title_font = _font(46)
    lines = _wrap(title, title_font, W - 100, draw)
    y = H // 2 - len(lines) * 30
    for line in lines:
        draw.text((50, y), line, font=title_font, fill=(255, 255, 255))
        y += 64

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=90)
    return out_path
