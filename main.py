#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Sunday 22 November 2026.

A one-page front-page infographic summing up the day's world news:
35 stories, 7 regions, every one dated Sunday 22 November 2026.
Drawn entirely in code with Pillow and Liberation TrueType fonts.
No network access, deterministic output (two runs -> identical bytes).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/liberation"

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(s):
    return _font("LiberationSerif-Bold.ttf", s)


def serif(s):
    return _font("LiberationSerif-Regular.ttf", s)


def serif_i(s):
    return _font("LiberationSerif-Italic.ttf", s)


def sans(s):
    return _font("LiberationSans-Regular.ttf", s)


def sans_b(s):
    return _font("LiberationSans-Bold.ttf", s)


def sans_i(s):
    return _font("LiberationSans-Italic.ttf", s)


# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
PAPER2 = (240, 234, 220)
INK = (22, 22, 22)
GREY = (92, 88, 80)
NAVY = (26, 42, 74)
NAVY2 = (16, 30, 58)
RED = (172, 32, 32)
RED_D = (138, 22, 22)
GOLD = (201, 162, 39)
GREEN = (31, 122, 77)
AMBER = (176, 110, 8)
PURPLE = (109, 76, 159)
TEAL = (15, 96, 96)
OCEAN = (168, 196, 214)
OCEAN_D = (140, 175, 198)
LAND = (217, 195, 154)
LAND_EDGE = (176, 152, 106)
RULE = (180, 172, 152)

REGION_COLORS = {
    "EUROPE": (36, 80, 126),
    "MIDDLE EAST": (165, 35, 42),
    "AMERICAS": (31, 122, 77),
    "ASIA": (181, 119, 8),
    "AFRICA": (109, 76, 159),
    "OCEANIA": (15, 118, 110),
    "WORLD": (85, 85, 85),
}

TAG_COLORS = {
    "CONFIRMED": (31, 122, 77),
    "OFFICIAL": (36, 80, 126),
    "REPORTED": (176, 110, 8),
    "CLAIM": (172, 32, 32),
}


# ---------------------------------------------------------------- text helpers
def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, font, fill, leading):
    """Draw wrapped lines; return y just below the last line."""
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=font, fill=fill)
    return y + len(lines) * leading


def fit_font(d, text, font_fn, start, max_w, minimum=8):
    """Largest font size (<= start) at which text fits max_w."""
    size = start
    while size > minimum:
        f = font_fn(size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font_fn(minimum)


def chip(d, x, y, text, bg, fg=(255, 255, 255), font=None, pad_x=5, h=14):
    """Small rounded label chip; returns width used."""
    font = font or sans_b(9)
    w = int(d.textlength(text, font=font)) + pad_x * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad_x, y + (h - font.size) // 2 - 1), text, font=font, fill=fg)
    return w


# ---------------------------------------------------------------- the slate
NUMBERS = [
    ("186", "drones fired at Ukraine"),
    ("161", "downed or jammed"),
    ("720/9", "India's record Test total"),
    ("856", "Hong Kong candidates"),
    ("$60,887", "Bitcoin, 13:01 UTC Sun"),
    ("24", "dead in Bayelsa boat"),
]

REGIONS = [
    ("EUROPE", 8), ("MIDDLE EAST", 5), ("AMERICAS", 5), ("ASIA", 7),
    ("AFRICA", 5), ("OCEANIA", 3), ("WORLD", 2),
]

TIMELINE = [
    ("01:42", "Saudi downs Houthi missile"),
    ("03:00", "COP31 objections close"),
    ("06:00", "Verstappen wins Las Vegas"),
    ("08:00", "COP31 collapses — no deal"),
    ("09:45", "Bitcoin tops $61,000"),
    ("15:54", "M5.6 quake off Sarangani"),
]

FEATURES = [
    {
        "n": 1,
        "kicker": "ANTALYA, TÜRKİYE — CLIMATE",
        "tag": "CONFIRMED",
        "headline": "COP31 collapses — no deal in Antalya",
        "deck": "EU, UK and Panama object: the text never names fossil fuels. "
                "Kurum: “these decisions have not been adopted.” "
                "First no-deal COP since 2009.",
        "source": "Reuters / BBC / The Times",
    },
    {
        "n": 2,
        "kicker": "KYIV REGION, UKRAINE — WAR",
        "tag": "REPORTED",
        "headline": "Russia fires 186 drones; a Kyiv-region block is destroyed",
        "deck": "161 downed or jammed; in Dymer a five-storey block is destroyed "
                "— 1 dead, up to 15 feared trapped. 30 hurt across Ukraine in a day.",
        "source": "Ukrainian Air Force / Kyiv Independent",
    },
    {
        "n": 3,
        "kicker": "MANAMA, BAHRAIN — IRAN",
        "tag": "CLAIM",
        "headline": "Iran claims two US radars hit; Bahrain denies it",
        "deck": "IRGC says strikes hit Patriot radars at Al-Riffa and Awali Sakhir. "
                "Bahrain: defences intercepted the attacks; a civilian site burned, "
                "no casualties.",
        "source": "IRIB / Al Jazeera / Reuters",
    },
]

MEDIUM = [
    {"n": 4, "chip": "F1", "headline": "Verstappen wins the Las Vegas GP",
     "deck": "From pole, beats Norris by 0.639s; 35 lead changes, 352 overtakes.",
     "source": "F1 / Reuters · CONFIRMED"},
    {"n": 5, "chip": "CRICKET", "headline": "India declare 720/9 — a record in NZ",
     "deck": "Rahul 136, Pant 128; NZ 119/2 at stumps day 4, trail 233.",
     "source": "ESPNcricinfo · CONFIRMED"},
    {"n": 6, "chip": "ELECTION", "headline": "Hong Kong elects its Election Committee",
     "deck": "856 candidates for 723 seats; turnout 93.55% by 14:00.",
     "source": "SCMP / info.gov.hk · OFFICIAL"},
    {"n": 7, "chip": "BOAT", "headline": "Bayelsa boat toll rises to 24",
     "deck": "24 bodies recovered, 24 rescued; barge capsized Fri on the Nun River.",
     "source": "Reuters / NEMA · OFFICIAL"},
    {"n": 8, "chip": "ENERGY", "headline": "Iran begins rationing electricity",
     "deck": "Rolling cuts of up to 2 hours a day; war damage to gas networks.",
     "source": "RFE/RL / Tavanir · OFFICIAL"},
    {"n": 9, "chip": "SPACE", "headline": "BepiColombo enters Mercury orbit",
     "deck": "After 8 years and 10bn km; only the 2nd mission ever to orbit Mercury.",
     "source": "ESA / AP · CONFIRMED"},
    {"n": 10, "chip": "GAZA", "headline": "Hamas seeks urgent talks after Gaza strike",
     "deck": "Strike hit a food-delivery vehicle; 3 aid workers killed.",
     "source": "Anadolu / Wafa · REPORTED"},
    {"n": 11, "chip": "CAPTURE", "headline": "“El Chapo Isidro” captured in Sinaloa",
     "deck": "FBI top-10 fugitive seized in Guasave; 11 dead in the operation.",
     "source": "Reuters / AP · CONFIRMED"},
    {"n": 12, "chip": "HEALTH", "headline": "Bolsonaro in intensive care",
     "deck": "Acute bowel obstruction; stable and conscious in Brasília hospital.",
     "source": "Reuters / hospital · OFFICIAL"},
    {"n": 13, "chip": "FIRE", "headline": "Cikande candy-factory fire: 3 dead, 36 missing",
     "deck": "Blaze at the Milkita plant in Serang; 15 survived, search ongoing.",
     "source": "Reuters / AP · REPORTED"},
]

ALSO = [
    (14, "Kryvyi Rih: Russian missile kills 2, hurts 58. (BBC)"),
    (15, "Saudi downs Houthi missile aimed at Riyadh, 01:42. (Anadolu)"),
    (16, "AI “helped prove” Riemann; Claude credited. (Guardian)"),
    (17, "Sparta II still burning off Loviisa; 16 crew safe. (Reuters)"),
    (18, "Nvidia faces an SEC accounting probe; shares fell 14%. (Reuters)"),
    (19, "Estonia to shut five Russia border crossings on 1 Dec. (Reuters)"),
    (20, "Denmark expels Russia’s defence attaché over a plot. (Reuters)"),
    (21, "Nepal PM Shah lands in Delhi on his first visit. (PTI)"),
    (22, "Philippines: M5.6 quake off Sarangani, 15:54. (PHIVOLCS)"),
    (23, "EU and Indonesia sign a trade deal after ten years. (DW)"),
    (24, "Sudan army retakes ~30 towns in Kordofan from RSF. (Reuters)"),
    (25, "Kenya discharges its last Ebola patient. (Wires)"),
    (26, "Marles rejects a US report on AUKUS subs. (ABC)"),
    (27, "Melbourne: 70 years since the 1956 Olympics opened. (ABC)"),
    (28, "Japan poll: a record 92% feel friendly to South Korea. (JNN)"),
    (29, "Somalia expels the UAE ambassador, recalls its envoy. (Reuters)"),
    (30, "ICE arrests on Seattle jet bridge; “beyond reform”. (UPI)"),
    (31, "ATP Finals final tonight: Zverev v Alcaraz, 18:00 CET. (ATP)"),
    (32, "Football: Arsenal 2–2 Newcastle; Leeds 4–1 Chelsea. (Reuters)"),
    (33, "Lebanon: Aoun demands Israel’s withdrawal. (Al Jazeera)"),
    (34, "DR Congo: Cantine attack, 40 killed. (Local officials)"),
    (35, "Bangladesh: 30 Awami League homes set on fire. (Reports)"),
]

DATE_CHECK = (
    "Left out as another day’s news: Peru quake (Fri 20 Nov, 6.7) · Russia’s "
    "400-drone barrage (19–20 Nov) — tonight’s was 186 · ICJ Myanmar ruling "
    "(Thu 19 Nov) · Shenzhen summit (Thu 19 Nov) · Kyiv bridges hit (Fri 20 Nov) · "
    "Cyclone Akvan (Fri 20 Nov) · UK–EU deal (Fri 20 Nov) · GTA VI launch "
    "(Thu 19 Nov) · Voyager 1’s light-day (18 Nov). Not confirmed when drawn: "
    "the ATP final result (18:00 CET) and any fresh COP31 text."
)

# ---------------------------------------------------------------- illustrations
def _star(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def draw_cop31(d, x, y, w, h):
    """Antalya plenary hall at dawn: globe, delegates at a table, a draft
    text stamped with a red X — the deal was NOT adopted."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 78, 84))
    d.rectangle([x, y, x + w, y + 26], fill=(32, 96, 100))
    # rising sun glow behind the hall
    d.ellipse([x + w - 78, y + 8, x + w - 30, y + 56], fill=(232, 178, 90))
    # globe on the left
    gx, gy, gr = x + 34, y + 52, 26
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 130, 160),
              outline=(220, 220, 200), width=2)
    d.ellipse([gx - 12, gy - 18, gx + 2, gy - 2], fill=(86, 160, 90))
    d.ellipse([gx - 2, gy + 6, gx + 16, gy + 20], fill=(86, 160, 90))
    d.ellipse([gx + 8, gy - 20, gx + 20, gy - 8], fill=(86, 160, 90))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=(220, 220, 200), width=1)
    # delegates at the table
    ty = y + h - 30
    d.rectangle([x + 8, ty, x + w - 8, ty + 10], fill=(120, 72, 40))
    for i, cx in enumerate(range(x + 96, x + w - 20, 34)):
        d.ellipse([cx - 8, ty - 26, cx + 8, ty - 10], fill=(232, 205, 165))
        d.polygon([(cx - 11, ty - 8), (cx + 11, ty - 8), (cx + 7, ty + 2),
                   (cx - 7, ty + 2)], fill=((58, 90, 140) if i % 2 else (140, 60, 60)))
        d.rectangle([cx - 7, ty - 4, cx + 7, ty + 1], fill=(255, 255, 255))
    # draft text with a red X on the table
    dx, dy = x + w - 92, ty - 34
    d.rectangle([dx, dy, dx + 52, dy + 30], fill=(245, 240, 225),
                outline=(120, 110, 90))
    for j in range(3):
        d.line([dx + 6, dy + 6 + j * 6, dx + 46, dy + 6 + j * 6], fill=(120, 120, 120), width=1)
    d.line([dx + 4, dy + 4, dx + 48, dy + 26], fill=RED, width=3)
    d.line([dx + 48, dy + 4, dx + 4, dy + 26], fill=RED, width=3)
    # clock showing 03:00
    cx, cy, cr = x + w - 52, y + 20, 11
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(245, 240, 225),
              outline=INK, width=1)
    d.line([cx, cy, cx, cy - cr + 3], fill=INK, width=2)
    d.line([cx, cy, cx + cr - 3, cy], fill=INK, width=2)


def draw_drones(d, x, y, w, h):
    """Night over Kyiv: skyline with lit windows, drones on attack runs,
    an explosion glow where the Dymer block was hit."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    for sx, sy in [(18, 12), (60, 22), (110, 10), (160, 26), (210, 14),
                   (260, 20), (300, 10), (40, 38), (140, 34), (230, 40)]:
        _star(d, x + sx, y + sy, 1, (255, 255, 220))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 44, 52), (48, 36, 68), (88, 52, 44), (144, 40, 74),
                       (188, 46, 56), (238, 38, 66), (280, 48, 48)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(10, 18, 36))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 7, x + bx + bw - 6, 13):
                if (wx * 7 + wy * 3) % 5:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(240, 200, 90))
    # explosion glow at the struck block
    ex, ey = x + 108, base - 44
    d.ellipse([ex - 26, ey - 26, ex + 26, ey + 26], fill=(220, 110, 30))
    d.ellipse([ex - 15, ey - 15, ex + 15, ey + 15], fill=(245, 190, 60))
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 240, 180))
    # drones with dotted trails
    for dx, dy in [(250, 22), (200, 34), (150, 18)]:
        d.line([x + dx + 26, y + dy + 4, x + dx + 62, y + dy - 8],
               fill=(240, 200, 90), width=1)
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(220, 220, 220))
        d.line([x + dx - 8, y + dy, x + dx + 8, y + dy], fill=(220, 220, 220), width=2)
        d.line([x + dx, y + dy - 5, x + dx, y + dy + 5], fill=(220, 220, 220), width=2)


def draw_radar(d, x, y, w, h):
    """Gulf dusk: two radar domes, missile arcs overhead, a shield —
    one side claims a hit, the other denies it."""
    for i in range(4):
        d.rectangle([x, y + i * h // 4, x + w, y + (i + 1) * h // 4],
                    fill=[(64, 48, 96), (96, 58, 92), (150, 80, 78), (196, 120, 80)][i])
    d.ellipse([x + w - 70, y + 6, x + w - 26, y + 50], fill=(245, 220, 160))
    # sea
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 70, 110))
    d.line([x, y + h - 16, x + w, y + h - 16], fill=(200, 220, 235), width=1)
    # radar domes (radomes on masts, with a small dish)
    for cx in (x + 62, x + 150):
        d.rectangle([cx - 3, y + h - 52, cx + 3, y + h - 16], fill=(200, 200, 200))
        d.pieslice([cx - 17, y + h - 84, cx + 17, y + h - 50], 180, 360,
                   fill=(225, 225, 225), outline=(150, 150, 150))
        d.line([cx - 17, y + h - 66, cx + 12, y + h - 80], fill=(225, 225, 225), width=3)
        d.ellipse([cx + 10, y + h - 84, cx + 16, y + h - 78], fill=(225, 225, 225))
    # missile arcs (red, claimed) and shield arc (green, denied)
    d.arc([x + 180, y - 6, x + 330, y + 70], 200, 330, fill=(230, 60, 40), width=3)
    d.arc([x + 210, y + 4, x + 310, y + 66], 200, 330, fill=(230, 60, 40), width=2)
    d.arc([x + 96, y + 30, x + 260, y + 108], 300, 360, fill=(90, 200, 120), width=3)
    d.polygon([(x + 300, y + 16), (x + 308, y + 24), (x + 300, y + 32)],
              fill=(230, 60, 40))
    # small buildings
    for bx, bw, bh in [(x + 250, 26, 26), (x + 280, 30, 18)]:
        d.rectangle([bx, y + h - 16 - bh, bx + bw, y + h - 16], fill=(40, 40, 60))
        d.rectangle([bx + 5, y + h - 12 - bh, bx + 9, y + h - 8 - bh],
                    fill=(240, 200, 90))


# ------------------------------------------------- medium-cell illustrations
def illo_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 52))
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + w - 34 + i * 8, y + 3 + j * 8,
                             x + w - 27 + i * 8, y + 10 + j * 8], fill=(255, 255, 255))
    d.rectangle([x + 14, y + h - 16, x + w - 40, y + h - 8], fill=(210, 40, 40))
    d.polygon([(x + 30, y + h - 16), (x + 44, y + h - 24), (x + 78, y + h - 24),
               (x + 84, y + h - 16)], fill=(210, 40, 40))
    d.rectangle([x + w - 44, y + h - 26, x + w - 38, y + h - 10], fill=(210, 40, 40))
    for wx in (x + 30, x + w - 52):
        d.ellipse([wx, y + h - 9, wx + 13, y + h + 2], fill=(15, 15, 15),
                  outline=(200, 200, 200), width=1)
    d.line([x + 8, y + h - 1, x + w - 8, y + h - 1], fill=(240, 200, 90), width=2)


def illo_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 62))
    d.ellipse([x + w - 52, y + 6, x + w - 12, y + h - 6], fill=(240, 220, 140))
    for sx in (x + 46, x + 56, x + 66):
        d.rectangle([sx, y + h - 22, sx + 4, y + h - 4], fill=(245, 220, 90))
    d.rectangle([x + 44, y + h - 24, x + 72, y + h - 20], fill=(245, 220, 90))
    d.polygon([(x + 92, y + 6), (x + 104, y + 4), (x + 118, y + 22),
               (x + 108, y + 30), (x + 96, y + 26)], fill=(196, 152, 90))
    d.line([x + 96, y + 26, x + 84, y + h - 8], fill=(196, 152, 90), width=4)
    d.ellipse([x + 128, y + h - 16, x + 140, y + h - 4], fill=(200, 40, 40),
              outline=(255, 255, 255), width=1)


def illo_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 78, y + 4), (x + 108, y + 4), (x + 100, y + 20),
               (x + 86, y + 20)], fill=(255, 255, 255), outline=INK)
    d.line([x + 88, y + 13, x + 92, y + 17], fill=GREEN, width=2)
    d.line([x + 92, y + 17, x + 100, y + 8], fill=GREEN, width=2)
    d.rectangle([x + 66, y + h - 22, x + w - 66, y + h - 4], fill=(36, 80, 126))
    d.rectangle([x + 84, y + h - 26, x + w - 84, y + h - 22], fill=(20, 50, 84))
    d.text((x + 72, y + h - 19), "VOTE", font=sans_b(9), fill=(255, 255, 255))
    d.ellipse([x + 148, y + 6, x + 176, y + 28], fill=(220, 90, 60))
    d.text((x + 157, y + 10), "93%", font=sans_b(10), fill=(255, 255, 255))


def illo_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 110, 150))
    for wy in (y + 12, y + 20):
        d.arc([x + 10, wy, x + 60, wy + 12], 0, 180, fill=(255, 255, 255), width=2)
        d.arc([x + 120, wy, x + 170, wy + 12], 0, 180, fill=(255, 255, 255), width=2)
    d.polygon([(x + 60, y + h - 18), (x + 140, y + h - 18), (x + 128, y + h - 6),
               (x + 72, y + h - 6)], fill=(150, 90, 50))
    d.rectangle([x + 88, y + h - 30, x + 112, y + h - 18], fill=(120, 70, 40))
    d.line([x + 100, y + h - 30, x + 100, y + h - 40], fill=(200, 200, 200), width=2)
    d.polygon([(x + 100, y + h - 40), (x + 118, y + h - 32), (x + 100, y + h - 32)],
              fill=(240, 200, 90))
    d.ellipse([x + 150, y + h - 20, x + 168, y + h - 2], fill=(255, 255, 255),
              outline=RED, width=3)


def illo_pylon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 200))
    cx = x + 52
    d.line([cx - 26, y + h - 2, cx, y + 4], fill=(60, 60, 60), width=3)
    d.line([cx + 26, y + h - 2, cx, y + 4], fill=(60, 60, 60), width=3)
    d.line([cx - 20, y + 12, cx + 20, y + 12], fill=(60, 60, 60), width=3)
    d.line([cx - 14, y + 20, cx + 14, y + 20], fill=(60, 60, 60), width=2)
    d.line([cx, y + 4, cx, y + h - 2], fill=(60, 60, 60), width=2)
    d.polygon([(x + 128, y + 4), (x + 116, y + 20), (x + 126, y + 20),
               (x + 114, y + h - 4), (x + 132, y + 16), (x + 122, y + 16)],
              fill=(240, 190, 40))
    d.line([x + 90, y + 8, cx + 20, y + 12], fill=(60, 60, 60), width=1)
    d.line([cx - 20, y + 12, x + 10, y + 8], fill=(60, 60, 60), width=1)


def illo_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 34))
    for sx, sy in [(20, 8), (70, 16), (150, 10), (180, 22), (40, 26), (110, 28)]:
        _star(d, x + sx, y + sy, 1, (255, 255, 255))
    d.ellipse([x + 20, y + 6, x + 62, y + h - 6], fill=(170, 165, 155))
    for cx, cy, r in [(34, 14, 4), (46, 26, 3), (30, 26, 2), (50, 12, 2)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(130, 125, 115))
    d.rectangle([x + 96, y + 12, x + 118, y + 24], fill=(200, 200, 200))
    d.rectangle([x + 84, y + 14, x + 96, y + 22], fill=(90, 120, 200))
    d.rectangle([x + 118, y + 14, x + 130, y + 22], fill=(90, 120, 200))
    d.line([x + 107, y + 12, x + 107, y + 4], fill=(200, 200, 200), width=2)
    d.ellipse([x + 104, y + 1, x + 110, y + 7], fill=(240, 200, 90))
    d.arc([x + 130, y + 2, x + 170, y + 30], 300, 60, fill=(240, 200, 90), width=2)


def illo_truck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.rectangle([x + 24, y + 8, x + 118, y + h - 10], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.polygon([(x + 118, y + 16), (x + 142, y + 16), (x + 152, y + h - 10),
               (x + 118, y + h - 10)], fill=(200, 60, 50))
    d.rectangle([x + 124, y + 18, x + 138, y + 26], fill=(180, 220, 240))
    for wx in (x + 44, x + 128):
        d.ellipse([wx, y + h - 11, wx + 13, y + h + 1], fill=(20, 20, 20),
                  outline=(200, 200, 200), width=1)
    d.rectangle([x + 62, y + 12, x + 80, y + 30], fill=RED)
    d.rectangle([x + 68, y + 18, x + 74, y + 24], fill=(255, 255, 255))
    d.line([x + 8, y + h - 2, x + w - 8, y + h - 2], fill=(120, 110, 90), width=2)


def illo_capture(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 42, 74))
    cx, cy = x + 52, y + h // 2
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 16 if i % 2 == 0 else 7
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(240, 190, 60))
    d.ellipse([x + 104, y + 8, x + 128, y + 26], fill=None, outline=(220, 220, 220), width=3)
    d.ellipse([x + 136, y + 14, x + 160, y + 32], fill=None, outline=(220, 220, 220), width=3)
    d.line([x + 124, y + 20, x + 140, y + 24], fill=(220, 220, 220), width=3)
    d.ellipse([x + 170, y + 10, x + 180, y + 20], fill=(240, 200, 90))


def illo_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 235))
    d.rectangle([x + 16, y + 10, x + 78, y + h - 8], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.rectangle([x + 30, y + 14, x + 64, y + 20], fill=RED)
    d.rectangle([x + 42, y + 12, x + 52, y + 30], fill=RED)
    d.rectangle([x + 96, y + h - 14, x + 176, y + h - 10], fill=(120, 120, 120))
    d.rectangle([x + 96, y + h - 20, x + 150, y + h - 14], fill=(180, 220, 240))
    d.rectangle([x + 96, y + h - 26, x + 118, y + h - 20], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.line([x + 96, y + h - 14, x + 96, y + h - 6], fill=(120, 120, 120), width=2)
    d.line([x + 176, y + h - 14, x + 176, y + h - 6], fill=(120, 120, 120), width=2)


def illo_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 40, 44))
    d.rectangle([x + 14, y + h - 20, x + 90, y + h - 4], fill=(30, 26, 28))
    d.polygon([(x + 14, y + h - 20), (x + 30, y + h - 30), (x + 46, y + h - 20),
               (x + 62, y + h - 30), (x + 78, y + h - 20), (x + 90, y + h - 20)],
              fill=(30, 26, 28))
    d.rectangle([x + 96, y + 6, x + 104, y + h - 4], fill=(30, 26, 28))
    for fx, fh in [(120, 22), (136, 30), (152, 20)]:
        d.polygon([(x + fx, y + h - 4), (x + fx + 6, y + h - fh),
                   (x + fx + 12, y + h - 4)], fill=(240, 140, 40))
        d.polygon([(x + fx + 3, y + h - 4), (x + fx + 6, y + h - fh + 8),
                   (x + fx + 9, y + h - 4)], fill=(245, 210, 60))
    d.ellipse([x + 170, y + 6, x + 182, y + 18], fill=(150, 150, 150))
    d.ellipse([x + 176, y + 12, x + 190, y + 26], fill=(130, 130, 130))


MEDIUM_ILLOS = {
    4: illo_f1, 5: illo_cricket, 6: illo_ballot, 7: illo_boat, 8: illo_pylon,
    9: illo_space, 10: illo_truck, 11: illo_capture, 12: illo_hospital,
    13: illo_factory,
}
FEATURE_ILLOS = {1: draw_cop31, 2: draw_drones, 3: draw_radar}

# ---------------------------------------------------------------- world map
# Simplified continent outlines as (lon, lat) polygons, equirectangular.
NORTH_AMERICA = [(-168, 66), (-150, 70), (-130, 71), (-115, 73), (-100, 73),
    (-90, 74), (-82, 72), (-78, 69), (-70, 62), (-64, 60), (-56, 52), (-60, 46),
    (-66, 44), (-70, 42), (-75, 38), (-76, 35), (-80, 31), (-81, 26), (-85, 29),
    (-90, 29), (-94, 29), (-97, 26), (-97, 21), (-94, 17), (-90, 14), (-86, 12),
    (-83, 9), (-79, 9), (-81, 12), (-85, 13), (-90, 15), (-94, 16), (-97, 16),
    (-102, 18), (-106, 20), (-110, 23), (-114, 28), (-117, 32), (-122, 37),
    (-124, 42), (-124, 48), (-128, 51), (-132, 56), (-140, 60), (-148, 60),
    (-155, 58), (-162, 58), (-166, 60)]
SOUTH_AMERICA = [(-79, 9), (-77, 6), (-78, 2), (-80, -3), (-81, -6), (-77, -11),
    (-73, -16), (-70, -20), (-70, -26), (-71, -30), (-73, -36), (-73, -42),
    (-70, -48), (-68, -52), (-66, -55), (-68, -50), (-65, -45), (-62, -41),
    (-58, -38), (-52, -33), (-48, -28), (-41, -23), (-38, -17), (-35, -9),
    (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 4), (-55, 6), (-60, 8),
    (-64, 10), (-70, 11), (-75, 10)]
AFRICA = [(-17, 15), (-16, 20), (-13, 27), (-10, 31), (-6, 34), (-2, 35),
    (3, 37), (8, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
    (33, 29), (34, 27), (37, 22), (39, 18), (41, 15), (43, 12), (47, 11),
    (51, 11), (50, 10), (46, 5), (42, 0), (40, -6), (40, -12), (38, -18),
    (35, -22), (33, -26), (30, -30), (27, -33), (22, -35), (18, -33), (16, -29),
    (14, -24), (13, -18), (12, -14), (10, -6), (9, 0), (9, 4), (4, 6), (-2, 5),
    (-8, 5), (-12, 8), (-15, 11)]
EUROPE = [(-10, 36), (-9, 39), (-9, 43), (-4, 44), (-2, 47), (-4, 49), (-1, 50),
    (2, 51), (4, 53), (6, 54), (8, 57), (6, 58), (5, 60), (8, 61), (12, 62),
    (16, 64), (19, 66), (22, 68), (26, 70), (30, 70), (34, 68), (38, 67),
    (42, 66), (46, 66), (50, 68), (54, 68), (58, 69), (62, 70), (66, 71),
    (70, 72), (72, 71), (68, 68), (64, 66), (60, 62), (58, 58), (55, 54),
    (52, 50), (50, 47), (46, 45), (42, 44), (38, 44), (34, 44), (30, 45),
    (28, 44), (26, 42), (23, 40), (21, 40), (19, 42), (16, 43), (14, 45),
    (12, 44), (9, 44), (7, 44), (4, 43), (2, 42), (0, 40), (-1, 38), (-4, 37),
    (-7, 37), (-9, 37)]
ASIA = [(28, 41), (30, 41), (33, 42), (36, 42), (39, 44), (42, 46), (45, 48),
    (48, 50), (51, 52), (54, 55), (57, 58), (60, 62), (63, 65), (66, 68),
    (70, 70), (74, 72), (78, 73), (82, 74), (86, 75), (90, 75), (94, 76),
    (98, 76), (102, 76), (106, 75), (110, 74), (114, 73), (118, 73), (122, 72),
    (126, 72), (130, 71), (134, 71), (138, 72), (142, 72), (146, 71), (150, 70),
    (154, 69), (158, 68), (162, 66), (166, 64), (170, 64), (174, 65), (178, 65),
    (176, 62), (170, 60), (166, 60), (162, 58), (158, 54), (156, 51), (152, 56),
    (148, 59), (144, 59), (142, 55), (141, 50), (140, 46), (138, 43), (135, 43),
    (132, 43), (130, 42), (128, 39), (127, 36), (126, 35), (124, 37), (122, 38),
    (121, 35), (121, 31), (120, 27), (118, 25), (115, 23), (112, 22), (110, 20),
    (108, 18), (106, 15), (105, 10), (103, 8), (101, 6), (99, 8), (98, 11),
    (96, 15), (94, 17), (92, 21), (90, 22), (88, 22), (86, 20), (84, 19),
    (82, 17), (80, 14), (79, 9), (77, 8), (76, 10), (74, 15), (72, 19),
    (70, 21), (68, 23), (66, 25), (64, 25), (62, 25), (60, 25), (58, 26),
    (56, 27), (54, 26), (52, 27), (51, 29), (49, 30), (48, 30), (50, 28),
    (51, 26), (53, 25), (55, 25), (57, 26), (59, 23), (58, 21), (56, 18),
    (54, 16), (52, 15), (50, 14), (48, 14), (45, 13), (43, 12), (43, 15),
    (41, 18), (39, 21), (37, 24), (36, 27), (35, 29), (34, 31), (36, 36),
    (33, 36), (30, 36), (27, 37), (26, 39)]
AUSTRALIA = [(113, -22), (114, -28), (115, -32), (115, -35), (118, -35),
    (122, -34), (124, -33), (129, -32), (132, -32), (135, -35), (137, -35),
    (140, -38), (143, -39), (146, -39), (148, -38), (150, -37), (152, -34),
    (153, -32), (153, -28), (151, -24), (149, -20), (146, -19), (143, -17),
    (142, -14), (142, -11), (141, -13), (139, -17), (136, -15), (135, -12),
    (132, -12), (130, -13), (128, -14), (126, -14), (124, -15), (122, -17),
    (120, -20), (117, -20), (114, -22)]
ISLANDS = [
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -5), (100, -1), (97, 3)],
    [(105, -6), (108, -7), (111, -7), (114, -8), (114, -9), (110, -8), (106, -7)],
    [(109, 1), (112, 3), (115, 5), (117, 3), (117, -1), (114, -3), (110, -2), (109, 0)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)],
    [(131, -1), (134, -3), (137, -4), (141, -6), (145, -7), (147, -8), (146, -7),
     (142, -8), (138, -8), (134, -4), (131, -2)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36), (141, 38),
     (141, 41), (142, 43), (144, 44), (141, 45), (140, 42), (139, 39), (137, 37),
     (135, 34), (133, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50)],
    [(173, -35), (175, -37), (177, -38), (178, -38), (176, -40), (174, -41), (173, -39)],
    [(167, -45), (169, -43), (171, -42), (173, -41), (174, -42), (172, -44),
     (169, -46), (167, -46)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25), (43, -22),
     (43, -18)],
    [(120, 22), (121, 23), (121, 25), (120, 24)],
]

CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EUROPE, ASIA, AUSTRALIA] + ISLANDS

# story number -> (lon, lat) of its pin on the map
PINS = {
    1: (30.7, 36.9), 2: (30.5, 50.5), 3: (50.6, 26.2), 4: (-115.1, 36.2),
    5: (174.8, -41.3), 6: (114.2, 22.3), 7: (6.3, 4.9), 8: (51.4, 35.7),
    10: (34.5, 31.5), 11: (-108.5, 25.6), 12: (-47.9, -15.8), 13: (106.2, -6.1),
}


def draw_map(d, x, y, w, h):
    """Beige continents on blue ocean, numbered red pins for stories 1-13."""
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    # faint graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        d.line([gx, y, gx, y + h], fill=OCEAN_D, width=1)
    for lat in range(-60, 81, 30):
        gy = y + (80 - lat) / 140 * h
        d.line([x, gy, x + w, gy], fill=OCEAN_D, width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (80 - lat) / 140 * h)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_EDGE)
    num_font = sans_b(8)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=num_font)
        d.text((px - tw / 2, py - 5), t, font=num_font, fill=(255, 255, 255))
    d.text((x + 6, y + h - 13),
           "9 · BepiColombo — in Mercury orbit, no pin on Earth.",
           font=sans_i(9), fill=(255, 255, 255))


# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 8                      # side margin
    CW = W - 2 * MX             # content width = 1008

    # --- masthead band
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((MX, 6), "THE WORLD IN ONE DAY", font=sans_b(13), fill=GOLD)
    right = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    d.text((W - MX - d.textlength(right, font=sans_b(10)), 8), right,
           font=sans_b(10), fill=(255, 255, 255))

    # --- date headline
    title = "Sunday 22 November 2026"
    tf = fit_font(d, title, serif_b, 66, CW)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 30), title, font=tf, fill=INK)
    d.rectangle([MX, 100, W - MX, 101], fill=RULE)

    # --- red italic 3-lead subhead
    sub = ("COP31 collapses with no deal  ·  186 drones over Ukraine  ·  "
           "Iran’s radar claim meets Bahrain’s denial")
    sf = fit_font(d, sub, serif_i, 17, CW)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 106), sub, font=sf, fill=RED_D)

    # --- numbers strip
    y0, y1 = 128, 168
    cell_w = CW / 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = MX + i * cell_w
        if i:
            d.line([cx, y0 + 4, cx, y1 - 4], fill=RULE, width=1)
        nf = fit_font(d, num, serif_b, 28, cell_w - 12)
        nw = d.textlength(num, font=nf)
        d.text((cx + (cell_w - nw) / 2, y0 + 1), num, font=nf, fill=RED_D)
        lf = sans(9)
        lw = d.textlength(label, font=lf)
        d.text((cx + (cell_w - lw) / 2, y0 + 31), label, font=lf, fill=GREY)
    d.rectangle([MX, y1, W - MX, y1 + 1], fill=RULE)

    # --- region bar (widths proportional to counts, total 35)
    y0 = 172
    total = sum(c for _, c in REGIONS)
    rx = MX
    for name, count in REGIONS:
        seg = CW * count / total
        d.rectangle([rx, y0, rx + seg, y0 + 18], fill=REGION_COLORS[name])
        label = f"{name} {count}"
        lf = sans_b(10)
        if d.textlength(label, font=lf) > seg - 6:
            lf = sans_b(8)
        d.text((rx + (seg - d.textlength(label, font=lf)) / 2, y0 + 4),
               label, font=lf, fill=(255, 255, 255))
        rx += seg

    # --- THE DAY IN UTC strip
    y0 = 194
    d.rectangle([MX, y0, W - MX, y0 + 18], fill=NAVY)
    lx = MX + 6
    d.text((lx, y0 + 4), "THE DAY IN UTC", font=sans_b(10), fill=GOLD)
    lx += d.textlength("THE DAY IN UTC", font=sans_b(10)) + 12
    items = "   ·   ".join(f"{t} {s}" for t, s in TIMELINE)
    itf = fit_font(d, items, sans, 10, CW - (lx - MX) - 6)
    d.text((lx, y0 + 4), items, font=itf, fill=(255, 255, 255))

    # --- 3 big features
    fw = 328
    fx0 = [MX, MX + fw + 8, MX + 2 * (fw + 8)]
    fy, fh = 216, 214
    for feat, fx in zip(FEATURES, fx0):
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255),
                    outline=RULE, width=1)
        FEATURE_ILLOS[feat["n"]](d, fx + 1, fy + 1, fw - 2, 88)
        kx = fx + 8
        ky = fy + 94
        kf = sans_b(10)
        d.text((kx, ky), f"{feat['n']} · {feat['kicker']}", font=kf,
               fill=TAG_COLORS[feat["tag"]])
        chip(d, fx + fw - 78, ky - 1, feat["tag"], TAG_COLORS[feat["tag"]],
             font=sans_b(8), h=13)
        hy = ky + 16
        hlines = wrap(d, feat["headline"], serif_b(19), fw - 16)
        block(d, kx, hy, hlines, serif_b(19), INK, 21)
        dy = hy + len(hlines) * 21 + 3
        dlines = wrap(d, feat["deck"], sans(11.5), fw - 16)
        max_deck = max(1, int((fy + fh - 16 - dy) // 14))
        block(d, kx, dy, dlines[:max_deck], sans(11.5), (50, 48, 44), 14)
        sy = fy + fh - 14
        d.text((kx, sy), feat["source"], font=sans_i(9.5), fill=GREY)

    # --- section header
    d.text((MX, 436), "THE DAY IN TEN — THE STORIES THAT MOVED THE WORLD",
           font=sans_b(11), fill=NAVY)
    d.rectangle([MX, 449, W - MX, 450], fill=NAVY)

    # --- 5x2 medium grid, every cell illustrated
    mw, mh, gap = 196, 100, 6
    gx0, gy0 = MX, 456
    for idx, story in enumerate(MEDIUM):
        col, row = idx % 5, idx // 5
        cx = gx0 + col * (mw + gap)
        cy = gy0 + row * (mh + gap)
        d.rectangle([cx, cy, cx + mw, cy + mh], fill=(255, 255, 255),
                    outline=RULE, width=1)
        MEDIUM_ILLOS[story["n"]](d, cx + 1, cy + 1, mw - 2, 32)
        chip(d, cx + 5, cy + 5, f"{story['n']} · {story['chip']}", (0, 0, 0),
             font=sans_b(8), h=12)
        tx = cx + 6
        ty = cy + 35
        hlines = wrap(d, story["headline"], serif_b(13), mw - 12)
        block(d, tx, ty, hlines[:2], serif_b(13), INK, 14)
        deck_y = ty + len(hlines[:2]) * 14 + 2
        dlines = wrap(d, story["deck"], sans(9.5), mw - 12)
        max_deck = max(1, int((cy + mh - 12 - deck_y) // 11))
        block(d, tx, deck_y, dlines[:max_deck], sans(9.5), (50, 48, 44), 11)
        d.text((tx, cy + mh - 11), story["source"], font=sans(8.5), fill=GREY)

    # --- map + ALSO list
    my = 664
    d.text((MX, my), "WHERE IT HAPPENED — PINS MATCH STORY NUMBERS",
           font=sans_b(11), fill=NAVY)
    d.text((MX + 330, my), "ALSO ON SUNDAY 22 NOVEMBER 2026 — 22 MORE STORIES",
           font=serif_b(13), fill=INK)
    map_x, map_y, map_w, map_h = MX, my + 18, 322, 196
    draw_map(d, map_x, map_y, map_w, map_h)
    ax0, ax1 = MX + 330, W - MX
    col_w = (ax1 - ax0 - 12) / 2
    ay = map_y + 2
    for i, (n, text) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        lx = ax0 + col * (col_w + 12)
        ly = ay + row * 17
        nf = sans_b(10)
        d.text((lx, ly), f"{n}", font=nf, fill=RED_D)
        nw = d.textlength(str(n), font=nf) + 4
        tf = fit_font(d, text, sans, 10, col_w - nw)
        d.text((lx + nw, ly), text, font=tf, fill=INK)

    # --- DATE CHECK box
    by0, by1 = 882, 958
    d.rectangle([MX, by0, W - MX, by1], outline=RED, width=2)
    d.rectangle([MX, by0, W - MX, by0 + 18], fill=RED)
    d.text((MX + 8, by0 + 4), "DATE CHECK — LEFT OUT AS ANOTHER DAY’S NEWS",
           font=sans_b(11), fill=(255, 255, 255))
    dlines = wrap(d, DATE_CHECK, sans(10.5), CW - 16)
    block(d, MX + 8, by0 + 22, dlines, sans(10.5), INK, 13)

    # --- footer
    fy = 964
    d.text((MX, fy),
           "HOW WE CHECKED:  CONFIRMED = 2+ outlets  ·  OFFICIAL = on the record  ·  "
           "REPORTED = one outlet  ·  CLAIM = one side’s account",
           font=sans_b(10), fill=NAVY)
    d.text((MX, fy + 14),
           "Every story here happened, or was first reported, on Sunday 22 November 2026. "
           "Officials’ counts and claims are attributed. Sources: Reuters, BBC, AP, "
           "Al Jazeera, The Guardian, SCMP, ESPNcricinfo, ESA, NEMA.",
           font=sans(9.5), fill=GREY)
    d.rectangle([0, 1004, W, H], fill=NAVY)
    d.text((MX, 1010), "THE WORLD IN ONE DAY", font=sans_b(10), fill=GOLD)
    right = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    d.text((W - MX - d.textlength(right, font=sans_b(10)), 1010), right,
           font=sans_b(10), fill=(255, 255, 255))
    return img


def main():
    img = build()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "entry.png")
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path} {img.size} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
