#!/usr/bin/env python3
"""Draw entry.png: one image summing up world news of Monday 23 November 2026.

Dense newspaper layout: masthead, 3 lead stories, UTC timeline strip,
7 region sections with 39 short sourced stories, a drawn world map and a
markets mini-chart. Run on this VM (PIL available); the sandbox entrypoint
main.ts only copies the committed entry.png to /output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 240)          # warm paper
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (25, 70, 130)
TEAL = (0, 110, 110)
GREY = (105, 105, 105)
LIGHT = (232, 227, 218)
GOLD = (160, 116, 0)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


f_title = font(FB, 42)
f_date = font(FB, 20)
f_sub = font(F, 13)
f_lead_h = font(FB, 15)
f_lead = font(F, 12)
f_sec = font(FB, 13)
f_story = font(F, 11)
f_src = font(F, 10)
f_small = font(F, 11)
f_tiny = font(F, 10)
f_map = font(FB, 10)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


LH = 13  # story line height


def story(x, y, w, text, src):
    """One short story: bullet + wrapped text, source tag appended inline
    after the last line when it fits, else on its own line. Returns new y."""
    d.ellipse([x, y + 4, x + 6, y + 10], fill=RED)
    tx = x + 11
    lines = wrap(text, f_story, w - 11)
    for ln in lines:
        d.text((tx, y), ln, font=f_story, fill=INK)
        y += LH
    last_w = d.textlength(lines[-1], font=f_story)
    tag = "  [" + src + "]"
    if last_w + d.textlength(tag, font=f_src) <= w - 11:
        d.text((tx + last_w, y - LH), tag, font=f_src, fill=GREY)
    else:
        d.text((tx, y), "[" + src + "]", font=f_src, fill=GREY)
        y += LH
    return y + 2


# ---------------- masthead ----------------
d.rectangle([0, 0, W, 80], fill=INK)
d.text((24, 8), "THE WORLD IN ONE DAY", font=f_title, fill=(250, 247, 240))
d.text((24, 54), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=(255, 196, 0))
tag = "39 STORIES  |  7 REGIONS  |  ALL DATED 23 NOV 2026"
d.text((W - 24 - d.textlength(tag, font=f_sub), 56), tag, font=f_sub, fill=(200, 200, 200))
d.rectangle([0, 80, W, 84], fill=RED)

# ---------------- lead stories ----------------
leads = [
    ("COP31 COLLAPSES — NO DEAL",
     "COP31 ends with no deal as the EU and 130+ nations reject a fossil-fuel-free draft; blame game erupts in Australia; Pacific states despair. (Reuters, CNN)",
     "CLIMATE"),
    ("ZELENSKY CLAIMS THE SINKING",
     "Kyiv says 7 Ukrainian sea drones sank the Merkury at Benghazi and hit cargo ship Angara; a Ka-27 helicopter was destroyed too. (Reuters, WSJ)",
     "WAR AT SEA"),
    ("AI ROUT DEEPENS IN ASIA",
     "KOSPI -3.3% as Asia slides again; S&P in correction after Fri -3.7%; US futures point up; $12tn wiped since Oct. (Reuters, AJ Bell)",
     "MARKETS"),
]
lx, ly, lw, lh = 16, 92, 322, 100
for i, (head, body, tag) in enumerate(leads):
    x = lx + i * (lw + 8)
    d.rectangle([x, ly, x + lw, ly + lh], outline=INK, width=2, fill=(255, 255, 255))
    d.rectangle([x, ly, x + lw, ly + 21], fill=RED if i == 0 else (BLUE if i == 1 else TEAL))
    d.text((x + 8, ly + 3), tag, font=f_small, fill=(255, 255, 255))
    d.text((x + 8, ly + 24), head, font=f_lead_h, fill=INK)
    yy = ly + 44
    for ln in wrap(body, f_lead, lw - 16):
        d.text((x + 8, yy), ln, font=f_lead, fill=INK)
        yy += 15

# ---------------- UTC timeline strip ----------------
ty = 200
d.rectangle([16, ty, W - 16, ty + 60], fill=LIGHT, outline=INK, width=1)
d.text((24, ty + 3), "THE DAY IN UTC", font=f_sec, fill=INK)
d.line([24, ty + 37, W - 24, ty + 37], fill=INK, width=2)
timeline = [
    ("00:49", "NHS AI trial"),
    ("02:40", "M6.5 Vanuatu"),
    ("03:46", "Houthis claim hit"),
    ("05:05", "India PMI 56.3"),
    ("05:23", "Dymer toll 11"),
    ("06:30", "KOSPI -3.3%"),
    ("07:00", "Korea $1tn exports"),
    ("12:00", "COP31 backlash"),
]
n = len(timeline)
for i, (t, ev) in enumerate(timeline):
    x = 40 + i * ((W - 80) // (n - 1))
    d.ellipse([x - 4, ty + 33, x + 4, ty + 41], fill=RED)
    tx = min(max(x - 16, 18), W - 18 - d.textlength(t, font=f_tiny))
    d.text((tx, ty + 19), t, font=f_tiny, fill=BLUE)
    tw = d.textlength(ev, font=f_tiny)
    ex = min(max(x - tw / 2, 18), W - 18 - tw)
    d.text((ex, ty + 43), ev, font=f_tiny, fill=INK)

# ---------------- region sections ----------------
sections_left = [
    ("AMERICAS", BLUE, [
        ("Democrats win largest House majority since 1992, flipping a North Carolina seat.", "BBC"),
        ("Father and daughter detained by ICE at Seattle airport; protests erupt.", "The Hindu"),
        ("Delta system failure delays nearly 1,000 US flights before Thanksgiving.", "SMW News"),
        ("Mexico captures 'El Chapo Isidro', FBI top-10 fugitive; 4 soldiers, 7 gunmen killed in Guasave raid.", "WSJ"),
        ("Bolsonaro in intensive care in Brasilia with a bowel obstruction; hospital says he is stable.", "Reuters"),
        ("California AG Bonta sues OpenAI over AI agents that escaped testing.", "Reuters"),
        ("Mets sign pitcher Tarik Skubal to a record 9-year, $450m deal.", "FeedCast"),
    ]),
    ("MIDDLE EAST", RED, [
        ("Houthis claim a direct hit on Saudi Arabia's Rabigh refinery; damage unconfirmed, coalition says drone intercepted.", "Reuters"),
        ("Trump warns of new US strikes on Iran next year if no deal is reached; Tehran says it is open to talks.", "CNBC"),
        ("Iranian attack hits Bahrain industrial site, injuring two.", "AFP"),
        ("Two oil tankers catch fire near the Strait of Hormuz after mine claims.", "Al Jazeera"),
        ("Iran's FM: Hormuz reopening 'pointless' until Tehran's terms are met.", "AFP"),
        ("Israeli opposition calls settler attacks 'Jewish terrorism'; 12 vehicles torched.", "Al Jazeera"),
    ]),
    ("AFRICA", TEAL, [
        ("Reuters probe: Ebola deaths in DR Congo far undercounted; Bunia excess deaths top 1,000.", "Reuters"),
        ("Funeral boat capsizes in Nigeria's Bayelsa state; at least 24 dead.", "Reuters"),
        ("24 civilians killed in attack in South Sudan's Warrap state.", "Umsicht"),
        ("RSF drones hit Khartoum homes and a UN building; 4 killed, 3 UN staff hurt; army blames Ethiopia.", "Al Jazeera"),
        ("DR Congo warns EU deportation deal with Rwanda could aid armed militia.", "Umsicht"),
    ]),
]
sections_right = [
    ("EUROPE", BLUE, [
        ("Dymer toll rises to 11 as rescuers pull bodies from rubble; Kyiv region declares a day of mourning.", "Reuters"),
        ("Russian strike on a Vyshneve supermarket kills 3 and wounds 15, including 3 children.", "AFP"),
        ("Russian cargo ship Sparta Two still burning off Finland after drone strike.", "Reuters"),
        ("Ukrainian drones hit Russian National Guard HQ in Krasnodar.", "Umsicht"),
        ("~150,000 march in France for a sixth weekend over services and living costs.", "Umsicht"),
        ("Thousands rally in Istanbul over the Sozcu TV takeover, the third media seizure in a year.", "AFP"),
        ("Lagarde to step down as ECB president in February 2027.", "Munich Eye"),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("South Korea's annual exports top $1 trillion for the first time, on AI chip demand.", "Yonhap"),
        ("Taiwan bans short-selling after Taiex's worst week since 1990; KOSPI falls 3.3% on Monday.", "Reuters"),
        ("M 6.5 earthquake strikes the Vanuatu region at 02:40 UTC, 598 km deep.", "USGS"),
        ("Indonesia confirms 24 dead in a candy-factory fire; about 30 missing, cause probed.", "Reuters"),
        ("South Korea's education minister quits over AI exam-cheating scandal.", "Reuters"),
        ("MSCI discussed avoiding an Indonesia downgrade with Prabowo; Dalio brokered.", "Bloomberg"),
    ]),
    ("SOUTH ASIA", GOLD, [
        ("Nepal PM Balen Shah begins first official visit to India; energy on agenda.", "The Hindu"),
        ("India factory PMI hits 9-month high of 56.0; composite 56.3.", "Reuters"),
        ("India v NZ, 1st Test drawn at Wellington: India 720/9 dec, NZ 239/5 as Mitchell and Phillips hold out.", "Cricinfo"),
    ]),
    ("TECH, SCIENCE & SPORT", GOLD, [
        ("Anthropic mathematician + Claude claim a proof of the Riemann Hypothesis.", "Nature"),
        ("Suspected Chinese hackers use AI framework 'Cairn' on East Asian universities.", "SimpleLife"),
        ("BepiColombo enters orbit around Mercury after an eight-year journey.", "Trending News"),
        ("NHS launches world's largest trial of AI spotting breast cancer earlier.", "BBC"),
        ("Liverpool hammer 10-man Man Utd 4-0 in Pochettino's debut; Yoro off in 8 min.", "Reuters"),
    ]),
]

COL_W = 488
col_x = [16, 520]
sy = 272


def draw_sections(x, sections, y):
    for title, color, stories in sections:
        d.rectangle([x, y, x + COL_W, y + 19], fill=color)
        d.text((x + 8, y + 2), title, font=f_sec, fill=(255, 255, 255))
        y += 22
        for text, src in stories:
            y = story(x + 4, y, COL_W - 8, text, src)
        y += 5
    return y


end_left = draw_sections(col_x[0], sections_left, sy)
end_right = draw_sections(col_x[1], sections_right, sy)
body_end = max(end_left, end_right)
print("body ends at y =", body_end)

# ---------------- bottom band: world map + markets chart ----------------
by = body_end + 4
band_h = H - by - 28
d.rectangle([16, by, W - 16, by + band_h], fill=(255, 255, 255), outline=INK, width=1)
d.text((24, by + 3), "WHERE IT HAPPENED — DRAWN MAP", font=f_sec, fill=INK)
d.text((640, by + 3), "MARKETS TODAY", font=f_sec, fill=INK)

mx0, my0, mw, mh = 24, by + 23, 600, band_h - 30
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(214, 233, 244), outline=GREY)


def pt(lon, lat):
    return (mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh)


LAND = (196, 214, 168)
d.polygon([pt(-168, 66), pt(-140, 70), pt(-110, 68), pt(-95, 69), pt(-80, 62),
           pt(-65, 60), pt(-55, 52), pt(-60, 45), pt(-75, 35), pt(-80, 25),
           pt(-90, 21), pt(-97, 26), pt(-105, 20), pt(-110, 23), pt(-117, 33),
           pt(-124, 42), pt(-124, 48), pt(-135, 58), pt(-155, 58), pt(-168, 60)],
          fill=LAND, outline=GREY)
d.polygon([pt(-77, 8), pt(-60, 5), pt(-50, 0), pt(-35, -8), pt(-40, -22),
           pt(-48, -28), pt(-58, -38), pt(-65, -50), pt(-70, -54), pt(-73, -37),
           pt(-70, -20), pt(-77, -12), pt(-80, -3), pt(-77, 5)],
          fill=LAND, outline=GREY)
d.polygon([pt(-10, 36), pt(-9, 43), pt(-5, 48), pt(0, 51), pt(3, 53), pt(8, 57),
           pt(10, 59), pt(18, 56), pt(21, 55), pt(24, 58), pt(28, 60), pt(30, 62),
           pt(32, 70), pt(40, 68), pt(45, 60), pt(40, 50), pt(35, 47), pt(30, 45),
           pt(28, 41), pt(23, 40), pt(19, 42), pt(15, 44), pt(12, 42), pt(8, 44),
           pt(3, 43), pt(-2, 37), pt(-6, 36)],
          fill=LAND, outline=GREY)
d.polygon([pt(-17, 15), pt(-10, 31), pt(0, 36), pt(10, 37), pt(20, 32), pt(32, 31),
           pt(35, 28), pt(43, 12), pt(51, 11), pt(48, 2), pt(41, -2), pt(40, -10),
           pt(35, -18), pt(32, -29), pt(28, -33), pt(19, -35), pt(17, -29),
           pt(14, -22), pt(12, -18), pt(9, -1), pt(9, 4), pt(-8, 4), pt(-13, 8),
           pt(-17, 12)],
          fill=LAND, outline=GREY)
d.polygon([pt(32, 70), pt(45, 68), pt(60, 69), pt(80, 73), pt(100, 77), pt(120, 73),
           pt(140, 72), pt(160, 70), pt(178, 65), pt(170, 60), pt(158, 52),
           pt(142, 50), pt(140, 40), pt(130, 33), pt(122, 30), pt(120, 25),
           pt(110, 20), pt(105, 10), pt(100, 8), pt(97, 16), pt(92, 22), pt(88, 22),
           pt(80, 13), pt(77, 8), pt(73, 20), pt(66, 25), pt(60, 25), pt(57, 27),
           pt(52, 26), pt(48, 30), pt(44, 29), pt(40, 36), pt(36, 36), pt(32, 42),
           pt(35, 47), pt(40, 50), pt(45, 55), pt(40, 60)],
          fill=LAND, outline=GREY)
d.polygon([pt(114, -22), pt(122, -14), pt(132, -12), pt(142, -11), pt(150, -22),
           pt(153, -27), pt(150, -37), pt(140, -38), pt(129, -32), pt(115, -33),
           pt(113, -26)],
          fill=LAND, outline=GREY)

spots = [  # (lon, lat, label, dx, dy) — offsets de-collide crowded labels
    (-100, 40, "USA", 5, -6),
    (-102, 23, "MEX", 5, 2),
    (2, 50, "FRA/UK", -30, -14),
    (28, 50, "UKR", -26, -14),
    (20, 32, "LIBYA", 6, 2),
    (45, 32, "IRAQ", 5, -14),
    (55, 27, "HORMUZ", 6, 4),
    (47, 25, "KSA", -14, 10),
    (78, 21, "INDIA", 12, 8),
    (103, 1, "SE ASIA", 5, 2),
    (127, 36, "KOREA", 8, -14),
    (121, 25, "TAIWAN", -46, -14),
    (167, -14, "VANUATU", -54, -14),
    (20, 5, "DRC", -8, 10),
    (8, 9, "NIGERIA", -50, -6),
    (32, 15, "SUDAN", -34, 4),
    (151, -25, "AUS", 5, 2),
]
for lon, lat, lab, dx, dy in spots:
    x, y = pt(lon, lat)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=(255, 255, 255))
    d.text((x + dx, y + dy), lab, font=f_map, fill=INK)

cx0, cy0, cw, ch = 648, by + 28, 352, band_h - 42
bars = [
    ("KOSPI", -3.3, RED),
    ("S&P", -3.7, RED),
    ("Nasdaq", -5.3, RED),
    ("Dow", -1.9, RED),
    ("Gold", +2.7, TEAL),
    ("Brent", -0.2, RED),
]
bw = cw // len(bars)
zero_y = cy0 + ch // 2
d.line([cx0, zero_y, cx0 + cw, zero_y], fill=INK, width=1)
for i, (name, val, col) in enumerate(bars):
    bx = cx0 + i * bw + 8
    bh = max(3, abs(val) / 5.0 * (ch // 2 - 16))
    if val >= 0:
        d.rectangle([bx, zero_y - bh, bx + bw - 16, zero_y], fill=col)
        d.text((bx, zero_y - bh - 12), f"+{val}%", font=f_tiny, fill=INK)
    else:
        d.rectangle([bx, zero_y, bx + bw - 16, zero_y + bh], fill=col)
        # value above the zero line: the space below the bar holds the name
        d.text((bx, zero_y - 12), f"{val}%", font=f_tiny, fill=INK)
    d.text((bx, cy0 + ch - 8), name, font=f_tiny, fill=INK)

# ---------------- footer ----------------
d.text((16, H - 20),
       "Sources: Reuters, BBC, AP, AFP, Al Jazeera, The Hindu, Bloomberg, USGS, CNBC, Yonhap — every story happened or was first reported 23 Nov 2026.",
       font=f_tiny, fill=GREY)
d.text((W - 16 - d.textlength("MONDAY 23 NOVEMBER 2026", font=f_tiny), H - 20),
       "MONDAY 23 NOVEMBER 2026", font=f_tiny, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
print("bytes:", os.path.getsize("entry.png"))
