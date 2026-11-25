#!/usr/bin/env python3
"""Render the news-image-20261125 front page: 1024x1024, deterministic PIL.
Data: NEWS-RESEARCH.md (48 stories researched; 47 drawn, #25 Anthropic dropped
as unverified). Output: entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
GOLD = (176, 141, 60)
RULE = (26, 26, 26)
LIGHT_LINE = (180, 170, 150)
GREY = (90, 90, 90)
MAP_OCEAN = (214, 228, 240)
MAP_LAND = (239, 230, 207)
MAP_OUTLINE = (190, 175, 140)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_line(draw, text, fnt, max_w, min_size=9.5):
    """Return (text, font) shrunk until it fits one line; truncate with ellipsis."""
    f = fnt
    while draw.textlength(text, font=f) > max_w and f.size > min_size:
        f = font(f.path, f.size - 0.5)
    if draw.textlength(text, font=f) > max_w:
        while text and draw.textlength(text + "\u2026", font=f) > max_w:
            text = text[:-1]
        text = text + "\u2026"
    return text, f


# ---------------------------------------------------------------- data
STATS = [
    ("11", "wounded in Riyadh tower strike"),
    ("10 of 12", "Huawei counts guilty"),
    ("$100m", "Shein to pay in FTC settlement"),
    ("9,700 lbs", "lead azide to be detonated in Iowa"),
    ("00:18 UTC", "Shenzhou-24 lifts off, first Pakistani in orbit"),
]

HEROES = [
    dict(num=1, tag="RIYADH  \u00b7  WAR", art="riyadh",
         headline="Houthis hit Riyadh's tallest tower, 11 wounded",
         body="A Houthi drone hit the 385 m, 80-storey PIF Tower, wounding 11 \u2014 the second strike on Riyadh's tallest tower in five days.",
         src="REUTERS  \u00b7  AFP", cert="REPORTED"),
    dict(num=2, tag="NEW YORK  \u00b7  JUSTICE", art="huawei",
         headline="Huawei found guilty in US trial over Iran business",
         body="A Brooklyn jury found Huawei guilty on 10 of 12 counts \u2014 fraud, sanctions and trade-secret theft \u2014 but acquitted it of racketeering.",
         src="REUTERS  \u00b7  AP  \u00b7  BBC", cert="REPORTED"),
    dict(num=3, tag="JIUQUAN  \u00b7  SPACE", art="shenzhou",
         headline="Shenzhou-24 carries first Pakistani into orbit",
         body="Muhammad Zeeshan Ali, 40, is the first Pakistani ever in orbit and the first foreign astronaut aboard China's Tiangong station.",
         src="REUTERS  \u00b7  CMSA", cert="CONFIRMED"),
]

MEDIUM = [
    (4, "MIDDLETOWN, IOWA", "SAFETY", "Army to blow up its bomb-chemical stockpile",
     "US Army to detonate 9,700 lbs of lead azide.", "warn"),
    (5, "SHANGHAI", "POLITICS", "Shanghai pledges loyalty as purge reaches Politburo",
     "Chen Jining, 62, probed \u2014 fourth since 2025.", "flag"),
    (6, "WASHINGTON", "SECURITY", "CIA says its unclassified system was breached",
     "Open-source network hit; classified systems safe.", "shield"),
    (7, "PARIS", "JUSTICE", "Sarkozy and wife ordered to stand trial",
     "Trial over the Libyan funding case; hearing 1 Apr 2027.", "court"),
    (8, "CARTAGENA", "CRIME", "Gunmen seize 30 hostages in supermarket",
     "Failed cash robbery; 10 released, ~20 still held.", "shield"),
    (9, "MADRID", "SPORT", "Bellingham wonder goal as Real Madrid rout PSV 5\u20131",
     "Madrid's fifth straight UCL win; Mbapp\u00e9 scores twice.", "ball"),
    (10, "WASHINGTON", "BUSINESS", "Shein to pay $100m to settle FTC claims",
     "Broken shipping promises and suppressed reviews.", "chart"),
    (11, "KYIV", "WAR", "Zelenskiy confirms Ukraine hit Russian ship Sparta II",
     "Kyiv owns Saturday's drone strike in the Gulf of Finland.", "ship"),
    (12, "GAZA", "WAR", "Israeli strike kills Hamas security chief",
     "Airstrike kills Naeem Abu Nahel in Gaza City.", "burst"),
    (13, "WASHINGTON", "TRADE", "Trump set to unveil new tariffs",
     "Higher tariffs planned on China, the EU and 14 others.", "arrows"),
    (14, "NEW YORK", "MARKETS", "AI trade slides again",
     "Nasdaq falls 1.5%, Nvidia ~6%, Micron 11%.", "chart"),
    (15, "FORT HOOD", "JUSTICE", "Fort Hood gunman seeks stay of execution",
     "Nidal Hasan, who killed 13 in 2009, seeks a stay.", "court"),
]

LIST = [
    "16  Stockholm: Speaker sets 30 Nov vote on Kristersson.",
    "17  Jerusalem: Eisenkot clinches first coalition deal.",
    "18  Washington: US envoy unsure Israel aid ends this year.",
    "19  Washington: Trump pardons turkeys Freedom & Feathers.",
    "20  USA: Record Thanksgiving travel; storms in Southeast.",
    "21  Aden: Houthis 60 km away; army says Aden holds.",
    "22  Hodeida / Lahj: Saudi strikes kill 17, then 26 more.",
    "23  Ras Al Khaimah: Crash toll rises to 13; 14 injured.",
    "24  Chicago: Radar fault delays flights into O\u2019Hare.",
    "26  USA: Dell lifts outlook on AI-server boom.",
    "27  New York: Nvidia slides ~7%; lawmakers demand answers.",
    "28  Washington: AG dodges Nvidia investigation questions.",
    "29  Kabul: RFE/RL returns to shortwave for Afghan girls.",
    "30  Baghdad: Iraq cracks down on oil smuggling.",
    "31  Jeddah: Houthis threaten Saudi Red Sea ports.",
    "32  Kuala Lumpur: Malaysia to return 6,500+ Rohingya.",
    "33  Geneva: AIDS deaths fall to 570,000, lowest in 20+ years.",
    "34  Seoul: Russian jets enter air defence zone.",
    "35  Tehran: Iran braces for winter gas shortages.",
    "36  Caracas: Venezuela reports debt of $237.5bn.",
    "37  Dhaka: Hasina plans return home on 16 December.",
    "38  Sydney: CBD locked down by gas leak.",
    "39  Ohio: Bus crash kills two drivers; nine injured.",
    "40  Germany: Lufthansa mediation fails.",
    "41  Denver: Broncos suspend Dobbins one game.",
    "42  New Delhi: India launches Nayi Chetna 5.0 campaign.",
    "43  London: PM orders panel on nuclear test veterans.",
    "44  London: Ministers consult on age of consent.",
    "45  Berlin: Ifo points to recovery; VW Zwickau in crisis.",
    "46  Brussels: Budget battles, Ukraine aid, EV caps.",
    "47  Kinshasa: Army hunts missing plane; rebels claim hit.",
    "48  Baghdad: Iraq PM aims to wrest power from Kurdistan.",
]

DATE_CHECK = ("Left out because they were not this day\u2019s news: GTA 6 release (19 Nov)  \u00b7  "
    "Russia\u2019s 400-drone barrage (19\u201320 Nov)  \u00b7  Peru quake (20 Nov)  \u00b7  Sparta II hit (21 Nov)  \u00b7  "
    "El Chapo Isidro arrest (21 Nov)  \u00b7  NWSL final (21 Nov)  \u00b7  700,000 Russian soldiers figure (23 Nov analysis)  \u00b7  "
    "NATO AWACS decision (23 Nov)  \u00b7  COP31 final text (23 Nov)  \u00b7  Nepal quake (24 Nov, 07:17)  \u00b7  "
    "Giuliani Medal of Freedom (24 Nov)  \u00b7  Hormuz tankers hit mines (24 Nov)  \u00b7  BJP\u2013Akali alliance (24 Nov).")


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, x, y, s, col):
    import math
    if kind == "warn":
        d.polygon([(x + s / 2, y + 2), (x + s - 2, y + s - 2), (x + 2, y + s - 2)], fill=col)
        d.rectangle([x + s / 2 - 1, y + s * 0.35, x + s / 2 + 1, y + s * 0.62], fill=(255, 255, 255))
        d.ellipse([x + s / 2 - 1.5, y + s * 0.68, x + s / 2 + 1.5, y + s * 0.68 + 3], fill=(255, 255, 255))
    elif kind == "flag":
        d.rectangle([x + 4, y + 3, x + 6, y + s - 3], fill=col)
        d.polygon([(x + 6, y + 3), (x + s - 3, y + 7), (x + 6, y + 12)], fill=col)
    elif kind == "shield":
        d.polygon([(x + 3, y + 3), (x + s - 3, y + 3), (x + s - 3, y + s * 0.55),
                   (x + s / 2, y + s - 3), (x + 3, y + s * 0.55)], fill=col)
        d.rectangle([x + s / 2 - 1, y + 8, x + s / 2 + 1, y + s - 8], fill=(255, 255, 255))
    elif kind == "court":
        d.polygon([(x + 2, y + 3), (x + s - 2, y + 3), (x + s / 2, y + 9)], fill=col)
        for cx in (x + 5, x + s / 2 - 1, x + s - 7):
            d.rectangle([cx, y + 11, cx + 2, y + s - 5], fill=col)
        d.rectangle([x + 3, y + s - 4, x + s - 3, y + s - 2], fill=col)
    elif kind == "ball":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=col, width=2)
        d.polygon([(x + s / 2 - 3, y + s / 2 - 3), (x + s / 2 + 3, y + s / 2 - 2),
                   (x + s / 2 + 2, y + s / 2 + 4), (x + s / 2 - 4, y + s / 2 + 3)], fill=col)
    elif kind == "chart":
        for i, hh in enumerate((0.35, 0.6, 0.85)):
            bx = x + 4 + i * (s - 8) / 3
            d.rectangle([bx, y + s - 4 - (s - 8) * hh, bx + (s - 8) / 3 - 2, y + s - 4], fill=col)
    elif kind == "ship":
        d.polygon([(x + 4, y + s * 0.55), (x + s - 4, y + s * 0.55), (x + s - 8, y + s - 4), (x + 8, y + s - 4)], fill=col)
        d.rectangle([x + s / 2 - 1, y + 4, x + s / 2 + 1, y + s * 0.55], fill=col)
        d.polygon([(x + s / 2 + 1, y + 5), (x + s - 6, y + s * 0.5), (x + s / 2 + 1, y + s * 0.5)], fill=col)
    elif kind == "burst":
        cx, cy, r = x + s / 2, y + s / 2, s / 2 - 2
        pts = []
        for i in range(12):
            ang = i * math.pi / 6
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    elif kind == "arrows":
        d.rectangle([x + 3, y + s * 0.3, x + s - 8, y + s * 0.3 + 3], fill=col)
        d.polygon([(x + s - 8, y + s * 0.3 - 3), (x + s - 2, y + s * 0.3 + 1.5), (x + s - 8, y + s * 0.3 + 6)], fill=col)
        d.rectangle([x + 8, y + s * 0.62, x + s - 3, y + s * 0.62 + 3], fill=col)
        d.polygon([(x + 8, y + s * 0.62 - 3), (x + 2, y + s * 0.62 + 1.5), (x + 8, y + s * 0.62 + 6)], fill=col)
    else:
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=col, width=2)
        d.ellipse([x + s / 2 - 4, y + 2, x + s / 2 + 4, y + s - 2], outline=col, width=1)
        d.line([x + 2, y + s / 2, x + s - 2, y + s / 2], fill=col, width=1)


# ---------------------------------------------------------------- hero art (all drawing kept INSIDE the box)
def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 84))
    for sx, sy in [(20, 12), (60, 30), (120, 10), (180, 26), (240, 14), (300, 32)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    for bx, bw, bh in [(0, 42, 52), (46, 34, 70), (84, 46, 44), (250, 40, 58), (294, 36, 66)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 32, 60))
        for wy in range(y + h - bh + 8, y + h - 6, 10):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 120))
    tx, tw = x + 140, 52
    d.polygon([(tx, y + h), (tx + 8, y + 12), (tx + tw - 8, y + 12), (tx + tw, y + h)], fill=(38, 68, 110))
    for wy in range(y + 22, y + h - 8, 11):
        for wx in range(tx + 12, tx + tw - 12, 11):
            d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 214, 120))
    d.ellipse([x + w - 78, y + 8, x + w - 38, y + 48], fill=(255, 140, 40))
    d.ellipse([x + w - 70, y + 16, x + w - 46, y + 40], fill=(255, 210, 90))


def art_huawei(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 48, 74))
    # courthouse: small pediment, gold columns, big scales centred
    cx0, cx1 = x + 96, x + w - 96
    d.polygon([(cx0, y + 22), (cx1, y + 22), (x + w / 2, y + 6)], fill=(232, 222, 200))
    for ccx in (cx0 + 8, x + w / 2 - 7, cx1 - 22):
        d.rectangle([ccx, y + 26, ccx + 14, y + h - 12], fill=(232, 222, 200))
    d.rectangle([cx0 - 6, y + h - 12, cx1 + 6, y + h - 6], fill=(232, 222, 200))
    sx, sy = x + w / 2, y + 34
    d.rectangle([sx - 1, sy, sx + 1, sy + 30], fill=GOLD)
    d.line([sx - 30, sy + 3, sx + 30, sy + 3], fill=GOLD, width=2)
    for sgn in (-1, 1):
        d.line([sx + sgn * 30, sy + 3, sx + sgn * 20, sy + 18], fill=GOLD, width=1)
        d.arc([sx + sgn * 26 - 7, sy + 16, sx + sgn * 26 + 7, sy + 30], 0, 180, fill=GOLD, width=2)
    d.ellipse([sx - 4, sy - 6, sx + 4, sy + 2], fill=GOLD)


def art_shenzhou(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for sx, sy in [(16, 14), (52, 40), (110, 10), (170, 34), (230, 12), (290, 44), (310, 16), (90, 60)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x + w - 62, y + 10, x + w - 22, y + 50], fill=(235, 230, 210))
    d.ellipse([x + w - 56, y + 16, x + w - 34, y + 38], fill=(210, 204, 184))
    rx = x + w / 2
    d.polygon([(rx - 13, y + 30), (rx, y + 6), (rx + 13, y + 30)], fill=(178, 34, 34))
    d.rectangle([rx - 13, y + 30, rx + 13, y + 66], fill=(245, 245, 245))
    d.rectangle([rx - 13, y + 46, rx + 13, y + 52], fill=(178, 34, 34))
    d.polygon([(rx - 24, y + 66), (rx - 13, y + 50), (rx - 13, y + 66)], fill=(178, 34, 34))
    d.polygon([(rx + 24, y + 66), (rx + 13, y + 50), (rx + 13, y + 66)], fill=(178, 34, 34))
    d.polygon([(rx - 7, y + 66), (rx, y + 88), (rx + 7, y + 66)], fill=(255, 170, 40))
    d.polygon([(rx - 3, y + 66), (rx, y + 82), (rx + 3, y + 66)], fill=(255, 220, 120))
    # earth curve, clipped to the box
    d.ellipse([x - 40, y + h - 16, x + w + 40, y + h + 2], fill=(46, 90, 140))
    d.ellipse([x + 40, y + h - 10, x + 130, y + h + 2], fill=(70, 130, 90))


ART = {"riyadh": art_riyadh, "huawei": art_huawei, "shenzhou": art_shenzhou}


# ---------------------------------------------------------------- map
def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_OCEAN)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=1)
    polys = [
        [(30, 18), (85, 6), (135, 14), (150, 32), (125, 52), (95, 58), (60, 52), (32, 38)],
        [(150, 4), (168, 2), (172, 12), (155, 16)],
        [(95, 95), (125, 88), (140, 108), (120, 150), (100, 128)],
        [(175, 28), (200, 16), (218, 26), (208, 44), (188, 46), (172, 38)],
        [(178, 58), (215, 52), (232, 68), (222, 105), (200, 112), (182, 88)],
        [(222, 18), (300, 8), (318, 26), (308, 58), (272, 64), (242, 48), (224, 32)],
        [(285, 72), (300, 70), (302, 82), (288, 86)],
        [(288, 108), (318, 102), (324, 122), (296, 128)],
    ]
    for p in polys:
        pts = [(x0 + px * w / 330, y0 + py * h / 160) for px, py in p]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_OUTLINE)
    pins = [(1, 242, 60), (2, 88, 34), (3, 292, 36), (4, 70, 44), (5, 305, 48),
            (6, 98, 46), (7, 185, 32), (8, 78, 78), (9, 172, 42), (11, 215, 28), (12, 232, 58)]
    f_pin = font(F_SANS_BOLD, 10)
    for num, px, py in pins:
        cx, cy = x0 + px * w / 330, y0 + py * h / 160
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=f_pin)
        d.text((cx - tw / 2, cy - 7), t, font=f_pin, fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # kicker bar
    f_kick = font(F_SANS_BOLD, 13)
    d.text((8, 4), "THE WORLD ON ONE PAGE", font=f_kick, fill=INK)
    t = "DAY 329 OF 2026"
    d.text(((W - d.textlength(t, font=f_kick)) / 2, 4), t, font=f_kick, fill=RED)
    t = "47 STORIES  \u00b7  THE DAY'S NEWS"
    d.text((W - 8 - d.textlength(t, font=f_kick), 4), t, font=f_kick, fill=INK)
    d.line([8, 22, W - 8, 22], fill=RULE, width=2)

    # masthead
    f_mast = font(F_SERIF_BLACK, 54)
    t = "Wednesday 25 November 2026"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 24), t, font=f_mast, fill=INK)
    d.line([8, 86, W - 8, 86], fill=RULE, width=1)
    f_sub = font(F_SANS_BOLD, 12)
    t = "47 STORIES  \u00b7  EUROPE 9  \u00b7  MIDDLE EAST 10  \u00b7  ASIA 7  \u00b7  AFRICA 1  \u00b7  AMERICAS 18  \u00b7  OCEANIA 1  \u00b7  GLOBAL 1"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, 90), t, font=f_sub, fill=INK)
    f_tease = font(F_SERIF_IT, 14)
    t = "Shenzhou-24 carries first Pakistani into orbit    \u00b7    Houthis hit Riyadh tower again    \u00b7    Huawei guilty on 10 counts"
    d.text(((W - d.textlength(t, font=f_tease)) / 2, 108), t, font=f_tease, fill=RED)
    d.line([8, 126, W - 8, 126], fill=RULE, width=1)

    # stat strip
    f_stat_n = font(F_SERIF_BLACK, 30)
    f_stat_c = font(F_SANS, 11)
    col_w = (W - 16) / 5
    for i, (num, cap) in enumerate(STATS):
        cx = 8 + col_w * i
        nw = d.textlength(num, font=f_stat_n)
        d.text((cx + (col_w - nw) / 2, 132), num, font=f_stat_n, fill=RED)
        lines = wrap(d, cap, f_stat_c, col_w - 12)
        ly = 166
        for ln in lines[:2]:
            lw = d.textlength(ln, font=f_stat_c)
            d.text((cx + (col_w - lw) / 2, ly), ln, font=f_stat_c, fill=INK)
            ly += 13
        if i < 4:
            d.line([cx + col_w, 132, cx + col_w, 188], fill=LIGHT_LINE, width=1)
    d.line([8, 194, W - 8, 194], fill=RULE, width=1)

    # heroes
    hero_y, hero_h, art_h = 200, 220, 92
    hero_w = (W - 16 - 12) // 3
    f_tag = font(F_SANS_BOLD, 11)
    f_head = font(F_SERIF_BOLD, 17)
    f_body = font(F_SERIF, 12.5)
    f_src = font(F_SANS, 10)
    for i, hero in enumerate(HEROES):
        hx = 8 + i * (hero_w + 6)
        ART[hero["art"]](d, hx, hero_y, hero_w, art_h)
        d.rectangle([hx, hero_y, hx + hero_w, hero_y + hero_h], outline=INK, width=1)
        ty = hero_y + art_h + 6
        d.text((hx + 8, ty), hero["tag"], font=f_tag, fill=NAVY)
        tn = str(hero["num"])
        d.text((hx + hero_w - 8 - d.textlength(tn, font=f_tag), ty), tn, font=f_tag, fill=RED)
        ty += 15
        ty = draw_wrapped(d, hx + 8, ty, hero["headline"], f_head, hero_w - 16, leading=20, max_lines=2)
        ty += 2
        draw_wrapped(d, hx + 8, ty, hero["body"], f_body, hero_w - 16, leading=15, max_lines=3)
        sy = hero_y + hero_h - 16
        d.text((hx + 8, sy), hero["src"], font=f_src, fill=GREY)
        cw = d.textlength(hero["cert"], font=f_src)
        d.text((hx + hero_w - 8 - cw, sy), hero["cert"], font=f_src, fill=RED)

    # medium grid: 3 cols x 4 rows, card 58 tall
    grid_y, card_h = 426, 58
    card_w = (W - 16 - 12) // 3
    f_mtag = font(F_SANS_BOLD, 9)
    f_mhead = font(F_SERIF_BOLD, 13.5)
    f_mbody = font(F_SERIF, 11)
    for i, (num, place, cat, head, body, icon) in enumerate(MEDIUM):
        r, c = divmod(i, 3)
        cx = 8 + c * (card_w + 6)
        cy = grid_y + r * (card_h + 4)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], outline=LIGHT_LINE, width=1)
        d.rectangle([cx + 6, cy + 6, cx + 36, cy + 36], fill=NAVY)
        draw_icon(d, icon, cx + 8, cy + 8, 26, (255, 255, 255))
        tx = cx + 42
        d.text((tx, cy + 4), f"{place}  \u00b7  {cat}", font=f_mtag, fill=NAVY)
        d.text((cx + card_w - 8 - d.textlength(str(num), font=f_mtag), cy + 4), str(num), font=f_mtag, fill=RED)
        draw_wrapped(d, tx, cy + 16, head, f_mhead, card_w - 50, leading=15, max_lines=2)
        btxt, bfnt = fit_line(d, body, f_mbody, card_w - 50)
        d.text((tx, cy + 45), btxt, font=bfnt, fill=INK)

    # bottom: map left, list right
    bot_y = 668
    map_w, map_h = 320, 150
    f_sect = font(F_SANS_BOLD, 12)
    d.text((8, bot_y), "WHERE IT HAPPENED", font=f_sect, fill=INK)
    t = "pins carry the story numbers"
    d.text((8 + d.textlength("WHERE IT HAPPENED", font=f_sect) + 8, bot_y + 1), t, font=font(F_SANS, 10), fill=GREY)
    draw_map(d, 8, bot_y + 18, map_w, map_h)
    d.text((8, bot_y + 18 + map_h + 4), "Stylised map \u2014 positions approximate.",
           font=font(F_SANS, 9), fill=GREY)

    list_x = 344
    d.text((list_x, bot_y), "ALSO ON WEDNESDAY 25 NOV", font=f_sect, fill=INK)
    d.line([list_x, bot_y + 16, W - 8, bot_y + 16], fill=RULE, width=1)
    f_list = font(F_SERIF, 11)
    col_w2 = (W - 8 - list_x - 10) / 2
    per_col = 16
    for ci in range(2):
        lx = list_x + ci * (col_w2 + 10)
        yy = bot_y + 22
        for item in LIST[ci * per_col:(ci + 1) * per_col]:
            itxt, ifnt = fit_line(d, item, f_list, col_w2)
            d.text((lx, yy), itxt, font=ifnt, fill=INK)
            yy += 14

    # DATE CHECK box
    dc_y = 914
    d.rectangle([8, dc_y, W - 8, dc_y + 64], outline=RED, width=2)
    d.rectangle([8, dc_y, W - 8, dc_y + 18], fill=RED)
    d.text((14, dc_y + 2), "DATE CHECK", font=font(F_SANS_BOLD, 12), fill=(255, 255, 255))
    f_dc = font(F_SERIF, 11)
    draw_wrapped(d, 14, dc_y + 22, DATE_CHECK, f_dc, W - 28, leading=14, max_lines=3)

    # footer
    f_foot = font(F_SANS, 10)
    t1 = "The day\u2019s news, Wednesday 25 November 2026 \u2014 including Tuesday-evening wires that led Wednesday\u2019s editions. Earlier stories are named in DATE CHECK, left out."
    d.text((8, 984), t1, font=f_foot, fill=GREY)
    t2 = "Sources: Reuters  \u00b7  AP  \u00b7  BBC  \u00b7  NYT  \u00b7  AFP  \u00b7  Xinhua  \u00b7  FTC  \u00b7  CMSA  \u00b7  UNAIDS      Drawings are original vector art."
    d.text((8, 998), t2, font=f_foot, fill=GREY)
    t3 = "THE WORLD IN ONE DAY  \u2014  WEDNESDAY 25 NOVEMBER 2026  \u00b7  ONE PAGE"
    d.text((W - 8 - d.textlength(t3, font=f_foot), 998), t3, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
