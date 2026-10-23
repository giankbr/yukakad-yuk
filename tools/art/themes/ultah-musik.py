"""Ultah Musik — ulang tahun anak bertema musik: drum mainan merah, gitar kecil oranye, xilofon pelangi, terompet
kuning, not balok menari, dan lampu panggung; gouache tebal yang ceria. Run: python3 -I ultah-musik.py [part ...]
parts: band not1 not2 not3 lampu paranada     Assets -> public/themes/art/ultah-musik/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m5_lib import *

OUT = outdir("ultah-musik")
PARTS = sys.argv[1:] or ["band", "not1", "not2", "not3", "lampu", "paranada"]
RED, RED_D = "#ee4152", "#c22a3d"
ORANGE, ORANGE_D = "#ff9a3c", "#e2701f"
YEL, YEL_D = "#ffd23f", "#f0a81e"
TEAL, TEAL_D = "#2ec4b6", "#16968b"
BLUE, BLUE_D = "#4d7cf3", "#2f57c8"
PINK, PINK_D = "#ff7eb6", "#e4508f"
PURP, PURP_D = "#8f5be8", "#6a3dc4"
WOOD, WOOD_D = "#b7743f", "#8a5129"
CREAM = "#fff3dc"
PLUM = "#3b1d5e"


def paint(art, mask, c1, c2, seed, edge=None, hi=True):
    art = GP(art, mask, c1, c2, seed=seed, rough=2.2, streak=0.9)
    if edge:
        art = OV(art, outline_of(mask, 2.0), lambda m: rgba(flat(*m.shape, edge), np.clip(gaussian_filter(m, 0.6) * 0.75, 0, 1)), pad=6)
    if hi:
        gy, gx = np.gradient(gaussian_filter(mask, 3.0))
        lit = np.clip(-(gx * 0.8 + gy) * 3.0, 0, 1) * mask
        art = OV(art, lit, lambda m: rgba(flat(*m.shape, "#ffffff"), np.clip(m * 0.35, 0, 1)), pad=6)
    return art


def ell(W, H, cx, cy, rx, ry, rot=0.0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def drum(art, W, H, cx, cy, R, h, nx):
    top, bot = cy - h / 2, cy + h / 2
    body = shapes(W, H, [[(cx - R, top), (cx + R, top), (cx + R, bot), (cx - R, bot)]], smooth=False)
    body = np.clip(body + ell(W, H, cx, bot, R, R * 0.27), 0, 1)
    art = paint(art, body, RED, RED_D, nx(), edge=RED_D)
    # zigzag band (yellow triangles) around the shell
    tri = []
    n = 9
    for k in range(n):
        x0 = cx - R + k * 2 * R / n
        tri.append([(x0 + 4, top + h * 0.3), (x0 + R / n, bot - h * 0.12), (x0 + 2 * R / n - 4, top + h * 0.3)])
    tm = shapes(W, H, tri, smooth=False) * body
    art = paint(art, tm, YEL, YEL_D, nx(), hi=False)
    # rims
    rimb = np.clip(ell(W, H, cx, bot, R + 6, R * 0.27 + 8) - ell(W, H, cx, bot - 6, R, R * 0.27), 0, 1)
    rimb = np.clip(rimb * (1 - ell(W, H, cx, bot - 30, R + 10, R * 0.27)) + 0, 0, 1)
    art = paint(art, np.clip(ell(W, H, cx, bot, R + 6, R * 0.27 + 7) - shapes(W, H, [[(0, 0), (W, 0), (W, bot - 2), (0, bot - 2)]], smooth=False), 0, 1), "#fdfdfd", "#e7e2f2", nx(), edge="#c9c2d9", hi=False)
    head = ell(W, H, cx, top, R, R * 0.27)
    art = paint(art, ell(W, H, cx, top, R + 8, R * 0.27 + 7), "#fdfdfd", "#e7e2f2", nx(), edge="#b8b0cc", hi=False)
    art = paint(art, head, CREAM, "#f4e2c0", nx(), hi=False)
    # lugs
    lug = shapes(W, H, [[(cx + R * math.sin(a) - 6, top + 10), (cx + R * math.sin(a) + 6, top + 10), (cx + R * math.sin(a) + 6, top + 40), (cx + R * math.sin(a) - 6, top + 40)] for a in np.linspace(-1.2, 1.2, 5)], smooth=False)
    art = paint(art, lug, "#dfe3ea", "#aeb6c4", nx(), edge="#8a93a3")
    # sticks
    for (x0, y0, x1, y1) in ((cx - R * 0.9, top - 120, cx + R * 0.3, top - 6), (cx + R * 0.9, top - 120, cx - R * 0.3, top - 6)):
        st = strokes(W, H, [([(x0, y0), (x1, y1)], 12, (0.0, 0.1))])
        art = paint(art, st, "#e9b377", WOOD, nx(), edge=WOOD_D)
        art = paint(art, circles(W, H, [(x0, y0, 13)]), PINK, PINK_D, nx(), edge=PINK_D)
    return art


def guitar(art, W, H, cx, cy, s, ang, nx):
    def P(x, y):
        return rotp([(cx + x * s, cy + y * s)], cx, cy, ang)[0]
    big = ellipse_pts(*P(0, 40), 70 * s, 64 * s, 30, ang)
    small = ellipse_pts(*P(0, -40), 52 * s, 46 * s, 30, ang)
    body = shapes(W, H, [big, small, rotp([(cx - 40 * s, cy - 40 * s), (cx + 40 * s, cy - 40 * s), (cx + 50 * s, cy + 40 * s), (cx - 50 * s, cy + 40 * s)], cx, cy, ang)])
    neck = shapes(W, H, [rotp([(cx - 11 * s, cy - 80 * s), (cx + 11 * s, cy - 80 * s), (cx + 11 * s, cy - 250 * s), (cx - 11 * s, cy - 250 * s)], cx, cy, ang)], smooth=False)
    headm = shapes(W, H, [rotp([(cx - 17 * s, cy - 250 * s), (cx + 17 * s, cy - 250 * s), (cx + 14 * s, cy - 300 * s), (cx - 14 * s, cy - 300 * s)], cx, cy, ang)])
    art = paint(art, neck, WOOD, WOOD_D, nx(), edge=WOOD_D)
    art = paint(art, headm, TEAL, TEAL_D, nx(), edge=TEAL_D)
    art = paint(art, body, ORANGE, ORANGE_D, nx(), edge=ORANGE_D)
    # flower decal + sound hole + bridge
    hole = circles(W, H, [(*P(0, -14), 22 * s)])
    ringm = ring(W, H, *P(0, -14), 30 * s, 5 * s)
    art = paint(art, ringm, YEL, YEL_D, nx(), hi=False)
    art = paint(art, hole, "#4a2a18", "#2e180c", nx(), hi=False)
    petals = [ellipse_pts(*P(36 + math.cos(a) * 12, 66 + math.sin(a) * 12), 9 * s, 6 * s, 10, a) for a in np.linspace(0, math.tau, 5, endpoint=False)]
    art = paint(art, shapes(W, H, petals), PINK, PINK_D, nx(), hi=False)
    art = paint(art, circles(W, H, [(*P(36, 66), 6 * s)]), YEL, YEL_D, nx(), hi=False)
    br = shapes(W, H, [rotp([(cx - 24 * s, cy + 52 * s), (cx + 24 * s, cy + 52 * s), (cx + 24 * s, cy + 62 * s), (cx - 24 * s, cy + 62 * s)], cx, cy, ang)], smooth=False)
    art = paint(art, br, "#5a3420", "#3d2214", nx(), hi=False)
    strs = [[P(x, 57), P(x * 0.9, -290)] for x in (-9, -3, 3, 9)]
    art = OV(art, lines(W, H, strs, 1.4, closed=False, smooth=False), lambda m: rgba(flat(*m.shape, "#fff6e0"), m * 0.9), pad=4)
    pegs = circles(W, H, [P(x, y) + (5 * s,) for x in (-20, 20) for y in (-265, -285)])
    art = paint(art, pegs, YEL, YEL_D, nx(), hi=False)
    return art


def xylophone(art, W, H, cx, cy, s, nx):
    cols = [(RED, RED_D), (ORANGE, ORANGE_D), (YEL, YEL_D), ("#7bd35a", "#4fa83a"), (TEAL, TEAL_D), (BLUE, BLUE_D), (PURP, PURP_D)]
    n = len(cols); gap = 6 * s; bw = 26 * s
    x0 = cx - (n * bw + (n - 1) * gap) / 2
    rails = strokes(W, H, [([(x0 - 14 * s, cy - 50 * s), (x0 + n * (bw + gap) + 8 * s, cy - 18 * s)], 12 * s, None),
                            ([(x0 - 14 * s, cy + 66 * s), (x0 + n * (bw + gap) + 8 * s, cy + 40 * s)], 12 * s, None)])
    art = paint(art, rails, WOOD, WOOD_D, nx(), edge=WOOD_D)
    for k, (c1, c2) in enumerate(cols):
        x = x0 + k * (bw + gap)
        L = (150 - k * 12) * s
        mid = cy + 8 * s - k * 2.4 * s
        bar = shapes(W, H, [[(x, mid - L / 2), (x + bw, mid - L / 2), (x + bw, mid + L / 2), (x, mid + L / 2)]], smooth=True)
        art = paint(art, bar, c1, c2, nx(), edge=c2)
        art = OV(art, circles(W, H, [(x + bw / 2, mid - L / 2 + 14 * s, 3.4 * s), (x + bw / 2, mid + L / 2 - 14 * s, 3.4 * s)]), lambda m: rgba(flat(*m.shape, "#f6f1ff"), m), pad=4)
    for (xa, ya, xb, yb, col) in ((cx - 40 * s, cy - 120 * s, cx + 60 * s, cy - 30 * s, PINK), (cx + 120 * s, cy - 110 * s, cx + 40 * s, cy - 10 * s, TEAL)):
        st = strokes(W, H, [([(xa, ya), (xb, yb)], 7 * s, None)])
        art = paint(art, st, "#e9b377", WOOD, nx(), edge=WOOD_D)
        art = paint(art, circles(W, H, [(xb, yb, 13 * s)]), col, mix(col, "#000000", .2), nx(), edge=mix(col, "#000000", .25))
    return art


def trumpet(art, W, H, cx, cy, s, ang, nx):
    def T(pts):
        return rotp([(cx + x * s, cy + y * s) for x, y in pts], cx, cy, ang)
    tube = strokes(W, H, [(T([(-140, 0), (60, 0)]), 16 * s, None), (T([(-60, 0), (-60, 34), (40, 34), (40, 0)]), 13 * s, None)])
    bell = shapes(W, H, [T([(50, -9), (110, -22), (150, -54), (156, 0), (150, 54), (110, 22), (50, 9)])])
    mouth = shapes(W, H, [T([(-150, -10), (-138, -6), (-138, 6), (-150, 10)])], smooth=False)
    valves = shapes(W, H, [T([(x - 7, -6), (x + 7, -6), (x + 7, -40), (x - 7, -40)]) for x in (-30, -6, 18)], smooth=False)
    caps = shapes(W, H, [ellipse_pts(*T([(x, -44)])[0], 11 * s, 6 * s, 14, ang) for x in (-30, -6, 18)])
    for m_ in (tube, valves, bell, mouth):
        art = paint(art, m_, YEL, YEL_D, nx(), edge="#c98512")
    art = paint(art, caps, "#fff1b8", YEL, nx(), edge="#c98512")
    # bell mouth opening (darker gold ellipse)
    bo = shapes(W, H, [ellipse_pts(*T([(152, 0)])[0], 10 * s, 50 * s, 18, ang)])
    art = paint(art, bo, YEL_D, "#d88a14", nx(), hi=False)
    # ribbon tassel
    rib = strokes(W, H, [(T([(-10, 34), (-22, 70), (-6, 104)]), 18 * s, (0.05, 0.5)), (T([(-10, 34), (4, 66), (16, 96)]), 16 * s, (0.05, 0.5))])
    art = paint(art, rib, RED, RED_D, nx(), hi=False)
    return art


if "band" in PARTS:
    clear()
    W, H = 1000, 640
    art = blank(W, H)
    nx = Seq(1000)
    # soft floor shadow
    sh = ell(W, H, 500, 590, 420, 26)
    art = OV(art, sh, lambda m: rgba(flat(*m.shape, "#1a0d2e"), np.clip(gaussian_filter(m, 10) * 0.35, 0, 1)), pad=30)
    art = guitar(art, W, H, 210, 420, 1.0, -0.38, nx)
    art = trumpet(art, W, H, 760, 150, 1.0, -0.32, nx)
    art = xylophone(art, W, H, 770, 470, 1.05, nx)
    art = drum(art, W, H, 470, 470, 150, 150, nx)
    art = add_grain(art, 4, 0.03)
    preview(art, "um-band", bg=PLUM)
    save(art, f"{OUT}/band.webp", max_w=720, quality=82)


def note_masks(W, H, kind, cx, cy, s):
    if kind == "eighth":
        head = ellipses(W, H, [(cx - 22 * s, cy + 60 * s, 26 * s, 19 * s, -24)])
        stem = shapes(W, H, [[(cx - 2 * s, cy + 58 * s), (cx + 6 * s, cy + 58 * s), (cx + 6 * s, cy - 80 * s), (cx - 2 * s, cy - 80 * s)]], smooth=False)
        flag = shapes(W, H, [[(cx + 2 * s, cy - 82 * s), (cx + 40 * s, cy - 50 * s), (cx + 52 * s, cy - 10 * s), (cx + 34 * s, cy + 12 * s), (cx + 38 * s, cy - 20 * s), (cx + 22 * s, cy - 44 * s), (cx + 4 * s, cy - 52 * s)]])
        return np.clip(head + stem + flag, 0, 1)
    if kind == "beam":
        heads = ellipses(W, H, [(cx - 52 * s, cy + 66 * s, 24 * s, 18 * s, -24), (cx + 40 * s, cy + 50 * s, 24 * s, 18 * s, -24)])
        stems = shapes(W, H, [[(cx - 33 * s, cy + 64 * s), (cx - 25 * s, cy + 64 * s), (cx - 25 * s, cy - 60 * s), (cx - 33 * s, cy - 60 * s)],
                              [(cx + 58 * s, cy + 48 * s), (cx + 66 * s, cy + 48 * s), (cx + 66 * s, cy - 80 * s), (cx + 58 * s, cy - 80 * s)]], smooth=False)
        beam = shapes(W, H, [[(cx - 33 * s, cy - 76 * s), (cx + 66 * s, cy - 96 * s), (cx + 66 * s, cy - 72 * s), (cx - 33 * s, cy - 52 * s)]], smooth=False)
        return np.clip(heads + stems + beam, 0, 1)
    head = ellipses(W, H, [(cx - 20 * s, cy + 60 * s, 26 * s, 19 * s, -24)])
    stem = shapes(W, H, [[(cx, cy + 58 * s), (cx + 8 * s, cy + 58 * s), (cx + 8 * s, cy - 80 * s), (cx, cy - 80 * s)]], smooth=False)
    return np.clip(head + stem, 0, 1)


for name, kind, c1, c2 in (("not1", "eighth", PINK, PINK_D), ("not2", "beam", TEAL, TEAL_D), ("not3", "quarter", YEL, YEL_D)):
    if name in PARTS:
        clear()
        W, H = 240, 260
        art = blank(W, H)
        m = note_masks(W, H, kind, 120, 120, 1.0)
        art = paint(art, m, c1, c2, 40 + len(name) + ord(name[-1]), edge=c2)
        # tiny face on the note head (playful, simple)
        preview(art, f"um-{name}", bg=PLUM)
        save(art, f"{OUT}/{name}.webp", max_w=90, quality=84)

if "lampu" in PARTS:
    # stage can light (par lamp) on a little bracket, lens glowing
    clear()
    W, H = 300, 300
    art = blank(W, H)
    nx = Seq(1300)
    yoke = strokes(W, H, [([(90, 60), (90, 140), (210, 140), (210, 60)], 12, None)])
    can = shapes(W, H, [rotp([(110, 70), (190, 70), (205, 200), (95, 200)], 150, 130, 0.0)], smooth=False)
    rimm = ell(W, H, 150, 205, 60, 18)
    lens = ell(W, H, 150, 205, 50, 13)
    art = paint(art, yoke, "#4b4f5c", "#30333d", nx(), edge="#22242b")
    art = paint(art, can, "#3a3d48", "#25272f", nx(), edge="#1b1c22")
    art = paint(art, rimm, "#5c6070", "#3a3d48", nx(), hi=False)
    art = over(art, glow(lens, "#fff1b0", radius=14, strength=0.7))
    art = paint(art, lens, "#fff6cf", "#ffe27a", nx(), hi=False)
    art = OV(art, ring(W, H, 150, 60, 10, 4), lambda m: rgba(flat(*m.shape, "#4b4f5c"), m))
    preview(art, "um-lampu", bg=PLUM)
    save(art, f"{OUT}/lampu.webp", max_w=110, quality=84)

if "paranada" in PARTS:
    # divider: a wavy five-line staff with three little notes bouncing on it
    clear()
    W, H = 560, 150
    art = blank(W, H)
    nx = Seq(1400)
    staff = []
    for k in range(5):
        staff.append(([(x, 52 + k * 11 + math.sin(x / 70) * 10) for x in np.linspace(20, 540, 60)], 2.6, (0.06, 0.06)))
    sm = strokes(W, H, staff)
    art = paint(art, sm, PURP, PURP_D, nx(), hi=False)
    for (x, kind, c1, c2, sc) in ((150, "eighth", PINK, PINK_D, 0.42), (280, "quarter", ORANGE, ORANGE_D, 0.42), (410, "beam", TEAL, TEAL_D, 0.38)):
        m = note_masks(W, H, kind, x, 52 + math.sin(x / 70) * 10, sc)
        art = paint(art, m, c1, c2, nx(), edge=c2)
    preview(art, "um-paranada", tone="#fff6e6")
    save(art, f"{OUT}/paranada.webp", max_w=280, quality=84)

kb(OUT)
