#!/usr/bin/env python3
"""Render entry.png: one image summing up world news of Sunday 22 Nov 2026.

Build tool only (needs Pillow + Liberation fonts locally). The graded entry
is main.py, which copies the finished entry.png to the output directory;
this script is kept in the repo so anyone can see exactly how the image
was drawn, and rebuild it with:  python3 render.py
News facts were checked against AP / Reuters / BBC / Dow Jones / ESA
reporting dated 22 November 2026 (see TEST_REPORT.md for sources).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 233)
INK = (20, 32, 46)
NAVY = (16, 35, 58)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 90, 82)
GREY = (90, 96, 104)
CARD = (255, 255, 255)
RULE = (200, 192, 172)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star(d, cx, cy, r_out, r_in, fill, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def burst(d, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(24):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(i * 15)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def flame(d, x, y, s, c1=(232, 116, 0), c2=(245, 196, 0)):
    """Simple flame: outer teardrop + inner teardrop, base at (x, y)."""
    d.polygon([(x, y - 1.5 * s), (x + 0.55 * s, y - 0.4 * s),
               (x + 0.45 * s, y), (x - 0.45 * s, y),
               (x - 0.55 * s, y - 0.4 * s)], fill=c1)
    d.polygon([(x, y - 0.9 * s), (x + 0.32 * s, y - 0.2 * s),
               (x + 0.26 * s, y), (x - 0.26 * s, y),
               (x - 0.32 * s, y - 0.2 * s)], fill=c2)


def draw_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=(38, 132, 120))
    d.ellipse([x, y, x + s, y + s], outline=(16, 35, 58), width=3)
    d.arc([x + s * 0.18, y + s * 0.08, x + s * 0.82, y + s * 0.92],
          270, 90, fill=(247, 243, 233), width=3)
    d.arc([x + s * 0.18, y + s * 0.08, x + s * 0.82, y + s * 0.92],
          90, 270, fill=(247, 243, 233), width=3)
    d.line([x + 4, y + s * 0.5, x + s - 4, y + s * 0.5],
           fill=(247, 243, 233), width=3)
    d.line([(x + s * 0.42, y + s * 0.12), (x + s * 0.55, y + s * 0.38),
            (x + s * 0.40, y + s * 0.55), (x + s * 0.58, y + s * 0.78),
            (x + s * 0.48, y + s * 0.95)], fill=(178, 34, 34), width=4)


def draw_tanker(d, x, y, s):
    d.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
               (x + s * 0.88, y + s * 0.82), (x + s * 0.12, y + s * 0.82)],
              fill=(40, 60, 84))
    for i, c in enumerate([(178, 34, 34), (201, 162, 39), (38, 132, 120)]):
        d.rectangle([x + s * (0.10 + i * 0.28), y + s * 0.34,
                     x + s * (0.34 + i * 0.28), y + s * 0.55], fill=c)
    d.rectangle([x + s * 0.78, y + s * 0.22, x + s * 0.94, y + s * 0.55],
                fill=(247, 243, 233))
    flame(d, x + s * 0.22, y + s * 0.34, s * 0.20)
    for i in range(3):
        d.arc([x + s * i * 0.33, y + s * 0.82, x + s * (i * 0.33 + 0.38),
               y + s * 1.06], 180, 360, fill=(38, 132, 120), width=3)


def draw_city(d, x, y, s):
    for bx, bw, bh in [(0.05, 0.26, 0.55), (0.36, 0.30, 0.72), (0.70, 0.24, 0.48)]:
        d.rectangle([x + s * bx, y + s * (0.95 - bh), x + s * (bx + bw),
                     y + s * 0.95], fill=(40, 60, 84))
        for wy in (0.30, 0.55):
            for wx in (0.25, 0.60):
                d.rectangle([x + s * (bx + bw * wx), y + s * (0.95 - bh + wy * bh * 0.55),
                             x + s * (bx + bw * wx + 0.07), y + s * (0.95 - bh + wy * bh * 0.55 + 0.08)],
                            fill=(247, 243, 233))
    burst(d, x + s * 0.51, y + s * 0.16, s * 0.26, s * 0.13, (245, 196, 0))
    burst(d, x + s * 0.51, y + s * 0.16, s * 0.15, s * 0.07, (232, 116, 0))


def draw_badge(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=(16, 35, 58))
    star(d, x + s * 0.5, y + s * 0.48, s * 0.34, s * 0.14, (201, 162, 39))
    d.ellipse([x + s * 0.44, y + s * 0.42, x + s * 0.56, y + s * 0.54],
              fill=(16, 35, 58))


def draw_chart(d, x, y, s):
    d.rectangle([x + s * 0.08, y + s * 0.55, x + s * 0.24, y + s * 0.92],
                fill=(150, 160, 172))
    d.rectangle([x + s * 0.32, y + s * 0.68, x + s * 0.48, y + s * 0.92],
                fill=(150, 160, 172))
    d.rectangle([x + s * 0.56, y + s * 0.40, x + s * 0.72, y + s * 0.92],
                fill=(150, 160, 172))
    d.line([(x + s * 0.06, y + s * 0.30), (x + s * 0.38, y + s * 0.48),
            (x + s * 0.62, y + s * 0.34), (x + s * 0.92, y + s * 0.72)],
           fill=(178, 34, 34), width=6)
    d.polygon([(x + s * 0.92, y + s * 0.72), (x + s * 0.76, y + s * 0.62),
               (x + s * 0.78, y + s * 0.78)], fill=(178, 34, 34))


def draw_factory(d, x, y, s):
    d.polygon([(x, y + s * 0.95), (x, y + s * 0.55), (x + s * 0.25, y + s * 0.38),
               (x + s * 0.50, y + s * 0.55), (x + s * 0.75, y + s * 0.38),
               (x + s, y + s * 0.55), (x + s, y + s * 0.95)],
              fill=(40, 60, 84))
    d.rectangle([x + s * 0.78, y + s * 0.12, x + s * 0.90, y + s * 0.55],
                fill=(90, 96, 104))
    flame(d, x + s * 0.30, y + s * 0.52, s * 0.20)
    d.ellipse([x + s * 0.80, y + s * 0.02, x + s * 0.94, y + s * 0.14],
              fill=(150, 160, 172))
    d.ellipse([x + s * 0.68, y - s * 0.04, x + s * 0.80, y + s * 0.06],
              fill=(180, 186, 192))


def draw_mercury(d, x, y, s):
    d.ellipse([x + s * 0.05, y + s * 0.05, x + s * 0.98, y + s * 0.98],
              outline=(201, 162, 39), width=3)
    d.ellipse([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
              fill=(176, 141, 109))
    for cx, cy, r in [(0.40, 0.40, 0.09), (0.58, 0.55, 0.07),
                      (0.45, 0.62, 0.05), (0.62, 0.36, 0.05)]:
        d.ellipse([x + s * (cx - r), y + s * (cy - r),
                   x + s * (cx + r), y + s * (cy + r)], fill=(140, 108, 82))
    d.rectangle([x + s * 0.80, y + s * 0.10, x + s * 0.88, y + s * 0.18],
                fill=(16, 35, 58))
    d.rectangle([x + s * 0.72, y + s * 0.13, x + s * 0.80, y + s * 0.15],
                fill=(16, 35, 58))
    d.rectangle([x + s * 0.88, y + s * 0.13, x + s * 0.96, y + s * 0.15],
                fill=(16, 35, 58))


ICONS = {"globe": draw_globe, "tanker": draw_tanker, "city": draw_city,
         "badge": draw_badge, "chart": draw_chart, "factory": draw_factory,
         "mercury": draw_mercury}

# tag, tag colour, icon, chip colour, headline, body
STORIES = [
    ("STRAIT OF HORMUZ", RED, "tanker", (232, 238, 240),
     "Iran hits three tankers near Hormuz",
     "Strikes deepen the US-Iran blockade stand-off over the vital oil strait."),
    ("UKRAINE", RED, "city", (238, 228, 224),
     "Missile kills boy, 7, in Kryvyi Rih",
     "Russian strike on Zelenskyy's home city kills two and wounds 60."),
    ("MEXICO", (14, 90, 82), "badge", (232, 236, 228),
     "Cartel boss \u2018El Chapo Isidro\u2019 captured",
     "Troops seize Fausto Isidro Meza Flores in Sinaloa; 11 die in the raid."),
    ("MARKETS", RED, "chart", (238, 228, 224),
     "Stocks slide as AI sell-off spreads",
     "S&P 500 falls 3.7% on Friday; Nasdaq drops 5.3%, Nikkei 5.1%."),
    ("INDONESIA", RED, "factory", (238, 228, 224),
     "Factory fire kills 3; 36 missing",
     "Blaze at a candy factory in Cikande, Banten; rescuers search the ruins."),
    ("SPACE", (14, 90, 82), "mercury", (232, 236, 228),
     "BepiColombo reaches Mercury",
     "After an 8-year voyage the probe enters orbit; ESA reports a thruster glitch."),
]

BRIEFS = [
    "EU and Indonesia sign a landmark trade deal after almost 10 years of talks",
    "Suspected drone blast hits a Russian ship at Benghazi; a second ship is hit in the Baltic",
    "Settlers torch vehicles in West Bank villages; Israel opens an inquiry",
    "Boat capsizes in Nigeria, at least 24 dead  \u2022  Tentative deal averts a strike at the busiest US ports",
    "Verstappen wins the Las Vegas Grand Prix",
]

# Body copy is kept to two wrapped lines per card at the grid width below;
# the Mercury body was shortened from three lines for exactly that reason.


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    # The date is auto-fitted: the widest size that stays inside 940 px,
    # so it can never clip at the edges (56 pt was too wide).
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.text((W // 2, 24), "THE WORLD IN ONE DAY", font=font(SANS_B, 26),
           fill=GOLD, anchor="ma")
    date_size = 56
    while (d.textlength("SUNDAY 22 NOVEMBER 2026", font=font(SERIF, date_size))
           > 940 and date_size > 36):
        date_size -= 2
    # Anchor "mm" (true middle): with "ma" the 56 pt box ran to y=137,
    # below the gold rule at y=124, and the date was clipped.
    d.text((W // 2, 82), "SUNDAY 22 NOVEMBER 2026",
           font=font(SERIF, date_size), fill=(255, 255, 255), anchor="mm")
    d.rectangle([0, 124, W, 129], fill=GOLD)

    # ---- Lead story: COP31 ----------------------------------------------
    ly, lh = 140, 190
    d.rounded_rectangle([16, ly, W - 16, ly + lh], radius=10, fill=CARD,
                        outline=RULE, width=2)
    d.rounded_rectangle([30, ly + 18, 30 + 160, ly + 178], radius=10,
                        fill=(222, 238, 234))
    draw_globe(d, 30 + 22, ly + 40, 116)
    tx = 216
    d.text((tx, ly + 20), "CLIMATE  \u00b7  ANTALYA, TURKEY",
           font=font(SANS_B, 20), fill=TEAL)
    d.text((tx, ly + 48), "COP31 ENDS WITH NO DEAL",
           font=font(SERIF, 52), fill=INK)
    lead = ("The EU and its allies reject a draft that never mentions fossil "
            "fuels; two days overdue, the UN climate summit closes empty-handed.")
    y = ly + 112
    for line in wrap(d, lead, font(SANS, 23), W - 32 - tx):
        d.text((tx, y), line, font=font(SANS, 23), fill=(52, 62, 74))
        y += 30

    # ---- Story grid ------------------------------------------------------
    # Cards are 156 tall: tag + two headline lines + two body lines fit
    # with room to spare; anything longer would spill past the card edge.
    gx, gy = 16, 342
    cw, ch, gap = 488, 156, 10
    tag_f = font(SANS_B, 18)
    head_f = font(SERIF, 26)
    body_f = font(SANS, 19)
    for i, (tag, tcol, icon, chip, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10, fill=CARD,
                            outline=RULE, width=2)
        d.rounded_rectangle([x + 12, y + 12, x + 122, y + 122], radius=10,
                            fill=chip)
        ICONS[icon](d, x + 22, y + 22, 90)
        tx = x + 136
        d.text((tx, y + 12), tag, font=tag_f, fill=tcol)
        hy = y + 38
        for line in wrap(d, head, head_f, cw - 150)[:2]:
            d.text((tx, hy), line, font=head_f, fill=INK)
            hy += 31
        by = hy + 2
        for line in wrap(d, body, body_f, cw - 150)[:2]:
            d.text((tx, by), line, font=body_f, fill=(52, 62, 74))
            by += 23

    # ---- In brief --------------------------------------------------------
    by = gy + 3 * ch + 2 * gap + 12
    d.text((16, by), "IN BRIEF", font=font(SANS_B, 20), fill=RED)
    d.line([120, by + 13, W - 16, by + 13], fill=RULE, width=2)
    brief_f = font(SANS, 18)
    y = by + 30
    for item in BRIEFS:
        d.text((16, y), "\u2022  " + item, font=brief_f, fill=INK)
        y += 24

    # ---- Footer ----------------------------------------------------------
    d.line([16, H - 24, W - 16, H - 24], fill=RULE, width=2)
    d.text((W // 2, H - 18),
           "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Dow Jones \u00b7 ESA  —  reported 22 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
