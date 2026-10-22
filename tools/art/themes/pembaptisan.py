"""Pembaptisan — a gentle Christian baptism in soft watercolour on white with pale gold light (original designs): a
white dove descending with an olive sprig, a carved stone baptismal font holding still water, a separate ripple ring
(animated), soft light rays from above, white Madonna lilies with buds, an olive-branch divider and a small gold-leaf
cross.
Run: python3 -I pembaptisan.py [part ...]  parts: dove font ripple rays lilies olive cross
Assets -> public/themes/art/pembaptisan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e6_lib import *

OUT = outdir("pembaptisan")
PARTS = sys.argv[1:] or ["dove", "font", "ripple", "rays", "lilies", "olive", "cross"]
SHADOW = "#b9c3d6"
WATER, WATER2 = "#a9cfe0", "#d6ecf3"
STONE, STONE2, STONE_D = "#ece5d8", "#ddd2bf", "#a89a82"
GOLD = "#d9b467"
OLIVE_A, OLIVE_B = "#a7b48a", "#6f7f58"
PENC = "#8a8496"


def white_shape(art, m, nx, shade=(1, 1), k=10, sh=SHADOW, line=True):
    art = GP(art, m, "#fffefb", "#f6f3ee", seed=nx(), rough=1.2, streak=0.3)
    art = G(art, inner_shade(m, int(shade[0] * k), int(shade[1] * k), blur=k), sh, seed=nx(), density=0.5, edge=0.35, bloom=0.35, rough=2)
    if line:
        art = pen(art, m, nx, col=PENC, w=1.5, dens=0.45)
    return art


def olive_sprig(art, W, H, pts, nx, rng, leaf_len=34, olives=True, width=2.6):
    art = G(art, strokes(W, H, [(pts, width, (0.05, 0.4))]), "#7a6a4a", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.6)
    lv = []
    for j in range(2, len(pts) - 1, 3):
        a, b = pts[j - 1], pts[min(len(pts) - 1, j + 1)]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for side in (-1, 1):
            L = leaf_len * rng.uniform(0.75, 1.05) * (1 - j / len(pts) * 0.35)
            lv.append(petal_pts(pts[j][0], pts[j][1], L, L * 0.2, ang + side * rng.uniform(0.5, 0.8), n=10))
    lm = shapes(W, H, lv)
    art = G(art, lm, OLIVE_A, OLIVE_B, seed=nx(), density=0.75, edge=0.55, bloom=0.35, rough=2)
    art = G(art, inner_shade(lm, 3, 3, 3), "#c9d3c0", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    if olives:
        ol = []
        for j in range(4, len(pts) - 2, 6):
            ol.append((pts[j][0] + rng.uniform(-8, 8), pts[j][1] + rng.uniform(6, 12), leaf_len * 0.18, leaf_len * 0.13, rng.uniform(0, 90)))
        om = ellipses(W, H, ol)
        art = G(art, om, "#6e7a3e", "#4a5a2a", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1)
    return art


if "dove" in PARTS:
    W, H = 560, 460
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    halo = circles(W, H, [(290, 210, 150)])
    art = G(art, gaussian_filter(halo, 40), "#f6e4b0", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=4)
    # far wing (behind body), raised
    fw = shapes(W, H, [[(300, 210), (330, 120), (380, 52), (440, 18), (470, 30), (450, 70), (430, 110), (400, 160), (360, 210)]])
    art = white_shape(art, fw, nx, shade=(-1, 1), k=14, sh="#a9b4cb")
    # tail fan (lower right, dove descends to the left)
    tail = shapes(W, H, [[(380, 260), (470, 300), (520, 340), (500, 360), (470, 352), (440, 360), (410, 330), (350, 290)]])
    art = white_shape(art, tail, nx, shade=(-1, -1), k=10)
    ts = strokes(W, H, [([(390, 280), (500, 350)], 1.4, None), ([(380, 288), (470, 352)], 1.4, None), ([(400, 274), (512, 338)], 1.2, None)])
    art = G(art, ts, SHADOW, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    # body + head
    body = shapes(W, H, [[(170, 200), (220, 186), (300, 200), (370, 240), (400, 280), (340, 300), (260, 290), (200, 262), (166, 230)]])
    head = circles(W, H, [(166, 196, 36)])
    bm = np.maximum(body, head)
    art = white_shape(art, bm, nx, shade=(-1, -1), k=18)
    # near wing, sweeping up with feather tips
    nw = [(230, 230), (220, 150), (236, 80), (270, 30), (300, 14)]
    tips = []
    for i, t in enumerate(np.linspace(0, 1, 7)):
        x = 300 + t * 60; y = 14 + t * 190
        tips.append((x + 26 - i * 2, y + 8))
        tips.append((x + 10, y + 26))
    wing = shapes(W, H, [nw + tips + [(330, 250), (280, 260)]])
    art = white_shape(art, wing, nx, shade=(1, -1), k=14, sh="#aab6cc")
    fe = []
    for i in range(6):
        t = (i + 1) / 7
        x0, y0 = 250 + t * 30, 40 + t * 170
        fe.append(([(x0, y0), (x0 + 70, y0 - 10 + t * 20)], 1.3, (0.1, 0.5)))
    art = G(art, strokes(W, H, fe) * wing, SHADOW, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6)
    # eye, beak
    art = G(art, circles(W, H, [(156, 188, 4.5)]), "#3e3a4a", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.3)
    beak = shapes(W, H, [[(132, 196), (110, 206), (134, 210)]])
    art = G(art, beak, "#e2a98a", "#c98a72", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.6)
    # olive sprig in the beak
    sp = curve([(118, 206), (90, 224), (60, 250), (34, 266)], 22)
    art = olive_sprig(art, W, H, sp, nx, rng, leaf_len=30)
    preview(art, "pb-dove", tone="#fbf8f2")
    save(art, f"{OUT}/dove.webp", max_w=300, quality=82)
    clear()

if "font" in PARTS:
    W, H = 640, 620
    nx = Seq(300); rng = random.Random(3)
    art = blank(W, H)
    cx = 320
    # base + pedestal
    base = shapes(W, H, [[(170, 600), (190, 560), (450, 560), (470, 600)]], smooth=False)
    step = shapes(W, H, [[(200, 562), (220, 530), (420, 530), (440, 562)]], smooth=False)
    col = shapes(W, H, [[(258, 534), (270, 330), (370, 330), (382, 534)]], smooth=False)
    for m, k in ((base, 10), (step, 8), (col, 22)):
        art = wash(art, m, STONE, STONE2, nx=nx, dens=0.65, shade=(-1, 0), k=k, sh_col="#8a7a64")
        art = pen(art, m, nx, col="#9a8c76", w=1.4, dens=0.45)
    flutes = strokes(W, H, [([(x, 340), (x + (x - cx) * 0.06, 526)], 2.2, None) for x in (290, 310, 330, 350)]) * col
    art = G(art, flutes, STONE_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.8)
    # basin: a wide bowl with a carved band
    bowl = shapes(W, H, [[(70, 214), (570, 214), (548, 270), (500, 316), (420, 346), (320, 354), (220, 346), (140, 316), (92, 270)]])
    art = wash(art, bowl, STONE, STONE2, nx=nx, dens=0.7, shade=(-1, 0), k=30, sh_col="#8a7a64")
    band = shapes(W, H, [[(84, 246), (556, 246), (546, 274), (94, 274)]]) * bowl
    art = G(art, band, STONE2, seed=nx(), density=0.5, edge=0.3, bloom=0.2, rough=1.5)
    # carved arches along the band
    arches = []
    for x in np.linspace(120, 520, 9):
        arches.append((arc_pts(x, 270, 18, math.pi, math.tau, 10), 1.6, None))
    art = G(art, strokes(W, H, arches) * bowl, STONE_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
    art = pen(art, bowl, nx, col="#9a8c76", w=1.6, dens=0.5)
    # rim (ellipse top) and water
    rim = shapes(W, H, [ellipse_pts(cx, 214, 252, 46, 40)])
    art = wash(art, rim, "#f4efe6", STONE, nx=nx, dens=0.6)
    art = pen(art, rim, nx, col="#9a8c76", w=1.4, dens=0.45)
    water = shapes(W, H, [ellipse_pts(cx, 216, 226, 34, 40)])
    art = G(art, water, WATER, WATER2, seed=nx(), density=0.8, edge=0.55, bloom=0.5, rough=2)
    art = G(art, inner_shade(water, 0, 6, 8), "#7fb0c8", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=1)
    rings = strokes(W, H, [(ellipse_pts(cx, 216, r, r * 0.15, 40) + [ellipse_pts(cx, 216, r, r * 0.15, 40)[0]], 1.8, None) for r in (40, 86, 140)])
    art = G(art, rings * water, "#ffffff", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.6)
    # light glint on water
    gl = shapes(W, H, [ellipse_pts(cx - 60, 208, 60, 6, 16)])
    art = G(art, gl, "#fffbe8", seed=nx(), density=0.8, edge=0, bloom=0, rough=1)
    preview(art, "pb-font", tone="#fbf8f2")
    save(art, f"{OUT}/font.webp", max_w=340, quality=82)
    clear()

if "ripple" in PARTS:
    W, H = 400, 120
    nx = Seq(500)
    art = blank(W, H)
    pts = ellipse_pts(200, 60, 180, 40, 48)
    ring = strokes(W, H, [(pts + [pts[0]], 4, None)])
    art = G(art, ring, "#ffffff", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.8)
    art = G(art, strokes(W, H, [(arc_pts(200, 60, 180, math.pi * 0.1, math.pi * 0.9, 30, 40 / 180), 3, (0.3, 0.3))]), "#8fbfd6", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.8)
    preview(art, "pb-ripple", bg="#a9cfe0")
    save_full(art, f"{OUT}/ripple.webp", size=(200, 60), quality=82)

if "rays" in PARTS:
    W, H = 600, 760
    nx = Seq(700)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy + 60, xx - 300)
    fan = np.clip(1 - np.abs(ang - math.pi / 2) / 0.6, 0, 1)
    bands = 0.5 + 0.5 * np.sin(ang * 46 + fbm(W, H, 3, 80, 2) * 3)
    bands = np.clip((bands - 0.35) * 1.6, 0, 1)
    fall = np.clip(1 - (yy + 60) / (H + 60), 0, 1) ** 1.1
    a = fan * (0.25 + 0.75 * bands) * fall * 0.55
    a = gaussian_filter(a, 2)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f7dc95"), np.float32)
    art = np.concatenate([rgb, a[..., None]], -1).astype(np.float32)
    preview(art, "pb-rays", bg="#fbf8f2")
    save_full(art, f"{OUT}/rays.webp", size=(300, 380), quality=76)

if "lilies" in PARTS:
    W, H = 600, 560
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    # leaves and stems
    stems = [curve([(80, 560), (120, 420), (180, 300), (250, 200)], 30), curve([(40, 560), (60, 440), (90, 330), (110, 250)], 30), curve([(130, 560), (200, 470), (300, 400), (370, 340)], 30)]
    for st in stems:
        art = G(art, strokes(W, H, [(st, 5, (0.0, 0.3))]), OLIVE_B, "#5d7a4e", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1)
    for st in stems:
        for j in range(3, len(st) - 4, 4):
            a, b = st[j - 1], st[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            side = 1 if j % 8 < 4 else -1
            L = rng.uniform(70, 110)
            lm = shapes(W, H, [petal_pts(st[j][0], st[j][1], L, L * 0.12, ang + side * 0.45, n=10)])
            art = G(art, lm, "#9db48a", "#5d7a4e", seed=nx(), density=0.7, edge=0.55, bloom=0.3, rough=2)
        clear()

    def lily(art, x, y, s, ang):
        """Trumpet lily facing along ang: six petals flaring from the throat."""
        dx, dy = math.cos(ang), math.sin(ang)
        throat = (x - dx * s * 0.5, y - dy * s * 0.5)
        petals = []
        for k in range(6):
            off = (k - 2.5) * 0.44
            pa = ang + off
            L = s * (1.25 if k in (0, 5) else 1.45)
            petals.append(petal_pts(throat[0], throat[1], L, s * 0.24, pa, n=12, cup=-0.15))
        back = shapes(W, H, petals[::2])
        front = shapes(W, H, petals[1::2])
        art = white_shape(art, back, nx, shade=(-dy, dx), k=8, sh="#c9cbbf")
        art = white_shape(art, front, nx, shade=(dy, -dx), k=8, sh="#cfd2c6")
        throat_m = shapes(W, H, [petal_pts(throat[0], throat[1], s * 0.6, s * 0.2, ang, n=10)])
        art = G(art, throat_m, "#d9e6b8", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1)
        st = []
        an = []
        for k in range(5):
            a2 = ang + (k - 2) * 0.16
            ex, ey = throat[0] + math.cos(a2) * s * 1.2, throat[1] + math.sin(a2) * s * 1.2
            st.append(([throat, (ex, ey)], 1.4, None))
            an.append((ex, ey, s * 0.06, s * 0.03, math.degrees(a2) + 90))
        art = G(art, strokes(W, H, st), "#a8b878", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4)
        art = G(art, ellipses(W, H, an), "#d8893e", "#b8662a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5)
        return art

    art = lily(art, 270, 180, 90, -0.4)
    clear()
    art = lily(art, 390, 320, 78, 0.2)
    clear()
    art = lily(art, 118, 222, 70, -1.5)
    clear()
    for x, y, a in ((300, 120, -1.0), (420, 290, -0.4)):
        bm = shapes(W, H, [petal_pts(x, y, 60, 15, a, n=12)])
        art = white_shape(art, bm, nx, shade=(1, 0), k=6, sh="#cdd6bf")
        art = G(art, inner_shade(bm, -3, 3, 4), "#c9dcae", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    preview(art, "pb-lilies", tone="#fbf8f2")
    save(art, f"{OUT}/lilies.webp", max_w=330, quality=82)
    clear()

if "olive" in PARTS:
    W, H = 460, 110
    nx = Seq(1100); rng = random.Random(11)
    art = blank(W, H)
    left = curve([(226, 60), (170, 50), (110, 58), (40, 44), (12, 50)], 30)
    right = curve([(234, 60), (290, 50), (350, 58), (420, 44), (448, 50)], 30)
    art = olive_sprig(art, W, H, left, nx, rng, leaf_len=30)
    art = olive_sprig(art, W, H, right, nx, rng, leaf_len=30)
    ctr = circles(W, H, [(230, 60, 5)])
    art = FO(art, ctr, GOLD, seed=nx(), emboss=0.4)
    preview(art, "pb-olive", tone="#fbf8f2")
    save(art, f"{OUT}/olive.webp", max_w=230, quality=84)

if "cross" in PARTS:
    W, H = 160, 220
    nx = Seq(1300)
    art = blank(W, H)
    c = shapes(W, H, [[(70, 16), (90, 16), (92, 66), (136, 64), (136, 86), (92, 84), (96, 204), (64, 204), (68, 84), (24, 86), (24, 64), (68, 66)]], smooth=False)
    art = OV(art, c, lambda m: glow(m, "#f7dc95", 14, 0.5))
    art = FO(art, c, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    preview(art, "pb-cross", tone="#fbf8f2")
    save(art, f"{OUT}/cross.webp", max_w=64, quality=84)

kb(OUT)
