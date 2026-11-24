#!/usr/bin/env python3
"""THE WORLD TODAY -- front page summing up Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with Pillow (stdlib + Pillow only),
deterministically, with no network access and no timestamps in the output.
Writes entry.png next to this script and, when writable, to /output/entry.png.

Stories (see NEWS.md): Nvidia reinstates Jensen Huang; Indonesia factory
fire, 24 dead; Trump hush-money case revived in federal court; FIFA names
2031/2035 Women's World Cup hosts; COP31 ends with no deal; Gukesh vs
Sindarov chess title match begins; Denmark backs 'ghetto law'; India-Nepal
$1.63bn package; Sensex slides.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (247, 241, 227)   # cream newsprint
INK = (25, 23, 19)
RED = (158, 27, 27)
NAVY = (30, 58, 95)
GREEN = (30, 107, 58)
GREY = (90, 84, 72)
LIGHT = (233, 224, 203)
GOLD = (201, 162, 39)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font; fall back to Pillow's built-in bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)         # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_para(draw, x, y, text, fnt, width, fill=INK, leading=1.28):
    """Draw wrapped text; return the y just below the last line."""
    size = fnt.size if hasattr(fnt, "size") else 16
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED, size=17):
    f = SANS_B(size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 6


def story(draw, x, y, w, kick, head, body, head_size=27, body_size=16):
    """One grid story: red kicker, serif headline, sans body. Returns bottom y."""
    y = kicker(draw, x, y, kick)
    y = draw_para(draw, x, y, head, SERIF_B(head_size), w, leading=1.12)
    y += 2
    y = draw_para(draw, x, y, body, SANS(body_size), w, fill=(52, 48, 40),
                  leading=1.3)
    return y


def draw_hero_art(draw, x, y, w, h):
    """Vector illustration: a chip (NVDA) and a rising market arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # chip
    cx, cy, cw, ch = x + 22, y + 26, 132, 132
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                           fill=(16, 32, 56), outline=GOLD, width=3)
    for i in range(5):  # pins left/right
        py = cy + 16 + i * 25
        draw.line([(cx - 11, py), (cx, py)], fill=GOLD, width=4)
        draw.line([(cx + cw, py), (cx + cw + 11, py)], fill=GOLD, width=4)
    for i in range(5):  # pins top/bottom
        px = cx + 16 + i * 25
        draw.line([(px, cy - 11), (px, cy)], fill=GOLD, width=4)
        draw.line([(px, cy + ch), (px, cy + ch + 11)], fill=GOLD, width=4)
    draw.rounded_rectangle([cx + 33, cy + 33, cx + cw - 33, cy + ch - 33],
                           radius=6, fill=GOLD)
    draw.text((cx + cw // 2, cy + ch // 2 - 12), "NVDA",
              font=SANS_B(19), fill=NAVY, anchor="mm")
    draw.text((cx + cw // 2, cy + ch // 2 + 14), "AI CHIP",
              font=SANS_B(12), fill=NAVY, anchor="mm")
    # rising arrow chart
    ax, ay = x + 180, y + 30
    pts = [(ax, ay + 108), (ax + 30, ay + 88), (ax + 60, ay + 94),
           (ax + 90, ay + 56), (ax + 120, ay + 64), (ax + 138, ay + 14)]
    draw.line(pts, fill=(120, 220, 150), width=5, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx - 4, hy + 14), (hx + 18, hy + 2), (hx - 2, hy - 10)],
                 fill=(120, 220, 150))
    draw.text((ax, ay + 124), "+33% IN ONE DAY",
              font=SANS_B(16), fill=(255, 255, 255))
    draw.text((ax, ay + 152), "Shares surge on his return",
              font=SANS(14), fill=(200, 210, 225))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- Masthead -------------------------------------------------------
    d.text((W // 2, 18), "THE WORLD TODAY", font=SERIF_B(84), fill=INK,
           anchor="ma")
    rule(d, x0, x1, 118, width=3)
    d.text((x0, 128), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(19), fill=INK)
    d.text((x1, 128), "ONE DAY  •  ONE PAGE  •  THE WORLD",
           font=SANS_B(19), fill=INK, anchor="ra")
    rule(d, x0, x1, 158, width=1)

    # ---- Hero -----------------------------------------------------------
    hy = 172
    hy = kicker(d, x0, hy, "Technology  •  Markets", size=18)
    hero_head = "HUANG IS BACK\nAT NVIDIA"
    y = hy
    for line in hero_head.split("\n"):
        d.text((x0, y), line, font=SERIF_B(56), fill=INK)
        y += 60
    y += 4
    y = draw_para(d, x0, y,
                  "Eleven days after he quit, Jensen Huang is chief "
                  "executive again — reinstated by a unanimous board "
                  "vote that found no national security risk in his "
                  "return.",
                  SANS(18), 560, leading=1.35)
    y += 6
    d.text((x0, y), "Shares jumped a third; ~$1tn of value returned.",
           font=SANS_B(18), fill=GREEN)

    # hero art, right column
    draw_hero_art(d, 612, 172, x1 - 612, 236)
    rule(d, x0, x1, 428, width=2)

    # ---- Grid: 2 columns x 3 rows ---------------------------------------
    col_w = (x1 - x0 - 28) // 2
    col_x = [x0, x0 + col_w + 28]
    row_y = [446, 606, 766]
    stories = [
        ("Disaster  •  Indonesia",
         "24 dead in factory fire",
         "A blaze tore through a candy factory in Cikande, Banten. "
         "Rescuers still search the wreckage for about 30 missing workers."),
        ("Politics  •  United States",
         "Trump's hush-money case gets new life",
         "A federal appeals court revived his bid to move the case to a "
         "federal court, where he could seek dismissal on immunity grounds."),
        ("Sport  •  Football",
         "Women's World Cups awarded",
         "FIFA named the USA, Mexico, Costa Rica and Jamaica as 2031 hosts; "
         "England, N. Ireland, Scotland and Wales will stage 2035."),
        ("Climate  •  Antalya",
         "COP31 ends with no deal",
         "UN climate talks collapsed without an agreement after a row over "
         "fossil fuels. The EU refused a text that never named them."),
        ("Sport  •  Chess",
         "Chess crown on the line in Geneva",
         "Gukesh defends his world title against Sindarov, 20, in a 14-game "
         "match. Game 1 today; Sindarov has White."),
        ("Europe  •  Denmark",
         "Top court backs 'ghetto law'",
         "Denmark's Supreme Court ruled evictions under the 2018 housing "
         "law were not ethnic discrimination."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        story(d, col_x[i % 2], row_y[i // 2], col_w, kick, head, body)
    rule(d, x0, x1, 926, width=1)

    # ---- Footer briefs --------------------------------------------------
    fy = 940
    d.text((x0, fy), "ALSO TODAY", font=SANS_B(16), fill=RED)
    d.text((x0 + 130, fy),
           "India pledges a $1.63bn package for Nepal; eight deals signed.",
           font=SANS(16), fill=INK)
    d.text((x0, fy + 26),
           "MARKETS",
           font=SANS_B(16), fill=RED)
    d.text((x0 + 130, fy + 26),
           "Sensex slides 1,484 points to 82,435; Nifty down 451.",
           font=SANS(16), fill=INK)
    d.text((x1, fy + 52), "Sources: Reuters  •  AP  •  FIFA  •  TechCrunch  •  Chess.com",
           font=SANS(13), fill=GREY, anchor="ra")

    out_here = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    img.save(out_here, "PNG")
    try:
        os.makedirs("/output", exist_ok=True)
        img.save("/output/entry.png", "PNG")
    except OSError:
        pass
    print("wrote", out_here)


if __name__ == "__main__":
    main()
