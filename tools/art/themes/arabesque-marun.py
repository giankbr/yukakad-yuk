"""Arabesque Marun — pressed gold-foil arabesque with wine-red enamel inlay: corner scrolls, lobed medallion,
divider scroll, multifoil portrait frame, inked damask tile and a fabric grain. Run: python3 -I /tmp/pen/art/themes/arabesque-marun.py"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentD_lib import *  # noqa

T = "arabesque-marun"
OUT = outdir(T)
GOLD = "#d2aa60"
WINE, WINE2 = "#8e2a3f", "#a8455a"
CREAM = "#f3dfbf"
rng = random.Random(31)
_s = [700]
def nxt():
    _s[0] += 23
    return _s[0]

def foilize(mask, seed, rough=0.8, thr=0.2):
    m = np.clip((gaussian_filter(displace(mask, seed, rough, 20), 0.5) - thr) * 1.6, 0, 1)
    return foil(m, GOLD, seed=seed, emboss=0.6, sparkle=0.16)

def enamel(mask, seed):
    """Opaque wine-red inlay with brush streaks (gouache), sits inside foil cells."""
    return gouache_paint(mask, WINE, WINE2, seed=seed, rough=1.0, streak=1.0, density=0.92)

MIRROR = (0, -1, -1, 0, 100, 100)   # reflect across the corner diagonal

# ---------------- 1. corner arabesque ----------------
CW = 264; ck = CW / 100 * 0.92; ct = CW * 0.04
HALF = ["M6 94C8 60 26 32 62 14", "M22 56C10 50 10 34 22 30C32 27 38 38 30 43C26 45 22 42 24 38",
        "M44 26C40 14 50 6 58 9C65 12 63 21 57 21", "M14 76C24 72 30 64 30 54"]
LEAVES = ["M62 14c4-6 12-8 18-5-5 1-9 4-11 9-2-3-4-4-7-4z", "M30 54c-6-2-8-8-6-13 2 4 5 6 9 6-2 2-3 4-3 7z",
          "M14 76c-6 0-10-4-10-9 3 3 6 4 10 3-1 2-1 4 0 6z"]
# extra palmette buds (wine inlay framed by foil) at the scroll ends
BUDS = ["M57 21c3 3 3 8 0 11-3-3-3-8 0-11z", "M24 38c-4 1-7 5-6 9 4-1 7-5 6-9z"]
lines = np.clip(svg_mask(CW, CW, HALF, scale=ck, tx=ct, ty=ct, fill=False, stroke=2.4)
                + svg_mask(CW, CW, HALF, scale=ck, tx=ct, ty=ct, fill=False, stroke=2.4, matrix=MIRROR), 0, 1)
leaves = np.clip(svg_mask(CW, CW, LEAVES, scale=ck, tx=ct, ty=ct) + svg_mask(CW, CW, LEAVES, scale=ck, tx=ct, ty=ct, matrix=MIRROR), 0, 1)
buds = np.clip(svg_mask(CW, CW, BUDS, scale=ck, tx=ct, ty=ct) + svg_mask(CW, CW, BUDS, scale=ck, tx=ct, ty=ct, matrix=MIRROR), 0, 1)
bud_rim = np.clip(svg_mask(CW, CW, BUDS, scale=ck, tx=ct, ty=ct, fill=False, stroke=2.0)
                  + svg_mask(CW, CW, BUDS, scale=ck, tx=ct, ty=ct, fill=False, stroke=2.0, matrix=MIRROR), 0, 1)
knot = circle_mask(CW, CW, [(ct + 6 * ck, ct + 94 * ck, 3.4 * ck)])
co = enamel(buds, nxt())
# leaf vein knocked out of the foil leaves gives them a carved split-palmette look
co = over(co, foilize(np.clip(lines + leaves + bud_rim + knot, 0, 1), nxt()))
save_plain(co, f"{OUT}/corner.webp", quality=84)
preview(co, "#5a1424", f"{PREV}/am-corner.png")

# ---------------- 2. lobed medallion ----------------
MS = 300; mk = MS / 100 * 0.96; mc = MS / 2
lobe = "M0-20C6-26 6-36 0-44C-6-36-6-26 0-20Z"
tendril = ["M0-30C10-30 16-38 14-46", "M0-30C-10-30-16-38-14-46"]
def rot(deg):
    a = math.radians(deg); return (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0, 0)
lobes_f = np.zeros((MS, MS), np.float32); lobes_o = np.zeros((MS, MS), np.float32); tend = np.zeros((MS, MS), np.float32)
for i in range(8):
    lobes_f = np.maximum(lobes_f, svg_mask(MS, MS, lobe, scale=mk, tx=mc, ty=mc, matrix=rot(i * 45)))
    lobes_o = np.maximum(lobes_o, svg_mask(MS, MS, lobe, scale=mk, tx=mc, ty=mc, matrix=rot(i * 45), fill=False, stroke=2.2))
    tend = np.maximum(tend, svg_mask(MS, MS, tendril, scale=mk, tx=mc, ty=mc, matrix=rot(i * 45), fill=False, stroke=2.0))
ringm = circle_mask(MS, MS, [(mc, mc, 20 * mk)], stroke=2.4)
inner_disc = circle_mask(MS, MS, [(mc, mc, 20 * mk - 2)])
centre = shape_mask(MS, MS, star_pts(mc, mc, 12 * mk, 3.6 * mk, n=4, rot=-math.pi / 2), smooth=False)
dots = circle_mask(MS, MS, [(mc + math.cos(a) * 47 * mk, mc + math.sin(a) * 47 * mk, 1.5) for a in np.linspace(0, math.tau, 64, endpoint=False)])
tdots = circle_mask(MS, MS, [(mc + math.cos(a) * 46.5 * mk, mc + math.sin(a) * 46.5 * mk, 2.6) for a in [i * math.pi / 4 - math.pi / 2 + math.radians(-17) for i in range(8)]]
                    + [(mc + math.cos(a) * 46.5 * mk, mc + math.sin(a) * 46.5 * mk, 2.6) for a in [i * math.pi / 4 - math.pi / 2 + math.radians(17) for i in range(8)]])
md = enamel(np.clip(lobes_f - gaussian_filter(lobes_o, .6) * 1.5, 0, 1), nxt())
md = over(md, gouache_paint(inner_disc, "#4a0f1c", "#5e1626", seed=nxt(), rough=0.8, streak=1.0))
md = over(md, foilize(np.clip(lobes_o + tend + ringm + centre + tdots, 0, 1), nxt(), rough=0.6))
md = over(md, foil(dots, GOLD, seed=nxt(), emboss=0.3, sparkle=0))
print("medallion", save_asset(md, f"{OUT}/medallion.webp", max_w=260, quality=84))
preview(md, "#5a1424", f"{PREV}/am-medallion.png")

# ---------------- 3. divider scroll ----------------
DW, DH = 420, 72; dk = 3.0
side = ["M58 12C46 12 40 4 30 4S14 12 22 16C28 19 32 12 27 10", "M58 12C50 18 42 20 34 19", "M30 4C20 4 8 8 2 12"]
FLIP = (-1, 0, 0, 1, 140, 0)
sl = np.clip(svg_mask(DW, DH, side, scale=dk, ty=0, fill=False, stroke=2.4) + svg_mask(DW, DH, side, scale=dk, matrix=FLIP, fill=False, stroke=2.4), 0, 1)
palm = svg_mask(DW, DH, "M70 3c5 4 6 10 0 18-6-8-5-14 0-18z", scale=dk)
palm_in = svg_mask(DW, DH, "M70 7c3 3 3.6 7 0 11-3.6-4-3-8 0-11z", scale=dk)
sd = circle_mask(DW, DH, [(61 * dk, 12 * dk, 1.8 * dk), (79 * dk, 12 * dk, 1.8 * dk)])
sc = over(blank(DW, DH), foilize(np.clip(sl + palm + sd, 0, 1), nxt(), rough=0.6))
sc = over(sc, enamel(palm_in, nxt()))
print("scroll", save_asset(sc, f"{OUT}/scroll.webp", max_w=320, quality=84))
preview(sc, "#5a1424", f"{PREV}/am-scroll.png")

# ---------------- 4. multifoil portrait frame (234x304 css @2x) ----------------
FW, FH = 468, 608
FOIL = "M0 280V106A30 30 0 0 1 30 62A35 35 0 0 1 68 27A40 40 0 0 1 105 0A40 40 0 0 1 142 27A35 35 0 0 1 180 62A30 30 0 0 1 210 106V280Z"
# viewBox -12 -12 234 304 → px = (x + 12) * 2 ; outlines as in the SVG: translate(-6 -6) scale(1.057 1.043) and (-11 -11) (1.105 1.079)
def frame_mask(tx, ty, sx_, sy_, stroke):
    def draw(cv):
        cv.c.save(); cv.c.scale(2, 2); cv.c.translate(12, 12); cv.c.translate(tx, ty); cv.c.scale(sx_, sy_)
        cv.c.drawPath(parse_svg_path(FOIL), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=stroke / 2 / sx_, Style=skia.Paint.kStroke_Style, StrokeJoin=skia.Paint.kRound_Join))
        cv.c.restore()
    return mask_from(FW, FH, draw)
o1 = frame_mask(-6, -6, 1.057, 1.043, 3.0)
o2 = frame_mask(-11, -11, 1.105, 1.079, 1.8)
# cusp knots where the lobes meet (outer outline), plus base knots
cusps = [(30, 62), (68, 27), (105, 0), (142, 27), (180, 62)]
kn = circle_mask(FW, FH, [((-6 + x * 1.057 + 12) * 2, (-6 + y * 1.043 + 12) * 2, 4.2 if x != 105 else 0) for x, y in cusps])
apex = shape_mask(FW, FH, star_pts((-6 + 105 * 1.057 + 12) * 2, (-6 + 0 * 1.043 + 12) * 2 - 4, 13, 5, n=4), smooth=False)
# band of wine enamel between the two outlines along the arch (top only, fading at the sides)
band = np.clip(frame_mask(-8.5, -8.5, 1.081, 1.061, 9.0), 0, 1)
yy = np.mgrid[0:FH, 0:FW][0].astype(np.float32)
band *= np.clip(1 - (yy - 230) / 120, 0, 1)
fr = over(blank(FW, FH), gouache_paint(band, WINE, WINE2, seed=nxt(), rough=0.8, streak=1.0, density=0.75))
fr = over(fr, foilize(np.clip(o1 + o2 + kn, 0, 1), nxt(), rough=0.6))
fr = over(fr, foilize(apex, nxt(), rough=0.4))
save_plain(fr, f"{OUT}/frame.webp", quality=84)
preview(fr, "#5a1424", f"{PREV}/am-frame.png")

# ---------------- 5. damask tile (transparent, seamless: 2x2 cells of 80 css px @2x) ----------------
TL = 320; u = 2
DAM = ["M40 8C52 20 52 32 40 40C28 32 28 20 40 8Z", "M40 72C52 60 52 48 40 40C28 48 28 60 40 72Z", "M40 40C30 46 18 44 14 36C11 30 18 26 22 30",
       "M40 40C50 34 62 36 66 44C69 50 62 54 58 50", "M0 0C8 4 12 10 10 18", "M80 80C72 76 68 70 70 62", "M80 0C72 4 68 10 70 18", "M0 80C8 76 12 70 10 62"]
def dam(cv):
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=1.7, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
    for i in range(2):
        for j in range(2):
            cv.c.save(); cv.c.translate(i * 80 * u, j * 80 * u); cv.c.scale(u, u)
            p.setStrokeWidth(1.7 / u)
            for d in DAM:
                cv.c.drawPath(parse_svg_path(d), p)
            cv.c.restore()
tm = np.tile(wrap_draw(TL, TL, dam), (3, 3))
dt = pigment(tm, "#d6b06a", "#e8cc90", seed=nxt(), density=0.9, edge=0.3, bloom=0.3, gran=0.45, rough=0.8, feather=0.5, mottle=0.8)[TL:2 * TL, TL:2 * TL]
save_plain(dt, f"{OUT}/damask.webp", quality=78)

# ---------------- 6. velvet/fabric grain (multiply) ----------------
fb = seamless_paper(512, 512, "#f6f2ee", seed=51, mottle=0.9, fiber=1.4, fine=0.8)
save_plain(fb, f"{OUT}/grain.webp", quality=78)

tot = 0
for f in sorted(os.listdir(OUT)):
    tot += kb(f"{OUT}/{f}"); print(f, kb(f"{OUT}/{f}"), "KB", Image.open(f"{OUT}/{f}").size)
print("total", round(tot, 1), "KB")
