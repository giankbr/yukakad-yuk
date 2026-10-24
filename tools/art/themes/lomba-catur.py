"""Lomba Catur — chess tournament, gouache on cream: a wooden board in perspective (maple/walnut squares with grain and a
walnut frame), carved boxwood and ebony pieces (king, knight, pawn; original designs), and an analogue chess clock.
Run: python3 -I lomba-catur.py [part ...]  parts: board pieces clock"""
import sys, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _q3_lib import *

OUT = outdir("lomba-catur")
PARTS = sys.argv[1:] or ["board", "pieces", "clock"]
MAPLE, MAPLE_D = "#e7c48c", "#d2a868"
WALNUT, WALNUT_D = "#6b4226", "#4a2c18"
EBONY, EBONY_L = "#2a1d16", "#4c382a"
BOX, BOX_D = "#e6c591", "#b98a52"
CREAM = "#f4ead8"
INK = "#1d1a17"


def wood(art, mask, col, col2, grain_col, seed, angle=0.0, spacing=5.0, dens=0.3):
    art = GP(art, mask, col, col2, seed=seed, rough=0.8, streak=1.2)
    H, W = mask.shape
    g = jw.hatch(W, H, angle, spacing, 0.12, seed + 1, wob=5) * mask
    return G(art, g, grain_col, seed=seed + 2, density=dens, edge=0, bloom=0, rough=0.5, feather=0.6, pad=4)


def edge_ink(art, seed, col=INK, dens=0.55):
    a = gaussian_filter(art[..., 3], 0.8)
    gy, gx = np.gradient(a)
    return G(art, np.clip(np.hypot(gx, gy) * 3, 0, 1), col, seed=seed, density=dens, edge=0, bloom=0, rough=0.5, feather=0.5, pad=4)


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


if "board" in PARTS:
    W, H = 820, 470
    nx = Seq(7100)
    TL, TR, BL, BR = (170, 40), (650, 40), (20, 400), (800, 400)
    # perspective rows: compress toward the top
    def P(u, v):
        vv = v ** 1.18
        top = lerp(TL, TR, u); bot = lerp(BL, BR, u)
        return lerp(top, bot, vv)
    frame = poly(W, H, [(150, 22), (670, 22), (818, 418), (2, 418)])
    side = poly(W, H, [(2, 418), (818, 418), (818, 452), (2, 452)])
    art = blank(W, H)
    art = wood(art, side, WALNUT_D, "#3a2214", "#24140a", nx(), 0.0, 6, 0.35)
    art = wood(art, frame, WALNUT, WALNUT_D, "#2e1a0c", nx(), 0.02, 7, 0.3)
    light, dark = [], []
    for i in range(8):
        for j in range(8):
            q = [P(i / 8, j / 8), P((i + 1) / 8, j / 8), P((i + 1) / 8, (j + 1) / 8), P(i / 8, (j + 1) / 8)]
            (light if (i + j) % 2 == 0 else dark).append(q)
    lm = shapes(W, H, light, smooth=False); dm = shapes(W, H, dark, smooth=False)
    art = wood(art, lm, MAPLE, MAPLE_D, "#a77a42", nx(), 0.0, 6, 0.28)
    art = wood(art, dm, "#7a4a2a", "#5e3820", "#2e1a0c", nx(), 0.0, 6, 0.3)
    # varnish sheen from the upper left + soft vignette at the far edge
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = np.clip(1 - np.hypot((xx - 260) / 360, (yy - 120) / 160), 0, 1) * (lm + dm)
    art = G(art, sheen * 0.8, "#fff4dc", seed=nx(), density=0.3, edge=0, bloom=0, rough=3, feather=4, pad=0)
    lines = strokes(W, H, [([P(0, 0), P(1, 0)], 2.2, None), ([P(1, 0), P(1, 1)], 2.2, None), ([P(1, 1), P(0, 1)], 2.2, None), ([P(0, 1), P(0, 0)], 2.2, None)])
    art = G(art, lines, "#e3b866", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    art = edge_ink(art, nx(), "#2a170b", 0.35)
    preview(art, "lc-board", CREAM)
    save(art, f"{OUT}/board.webp", max_w=780, quality=82)
    clear()


def turned(W, H, prof):
    """mirror a right-hand profile [(dx, y)] around the centre line into a closed outline."""
    c = W / 2
    right = [(c + dx, y) for dx, y in prof]
    left = [(c - dx, y) for dx, y in prof[::-1]]
    return right + left


def piece(kind, dark):
    nx = Seq(7200 + (50 if dark else 0) + {"king": 0, "knight": 10, "pawn": 20, "queen": 30}[kind])
    W, H = 240, 360
    c = W / 2
    base = [(80, 342), (82, 324), (70, 314), (58, 308), (54, 296), (62, 288), (56, 280), (42, 274)]
    if kind == "pawn":
        prof = base + [(36, 250), (30, 214), (26, 186), (40, 178), (42, 168), (26, 160), (0, 160)]
        body = np.maximum(smooth(W, H, turned(W, H, prof)), circles(W, H, [(c, 128, 40)]))
        y_top = 88
    elif kind == "king":
        prof = base + [(38, 240), (32, 190), (28, 150), (40, 142), (44, 132), (30, 126), (34, 112), (44, 96), (40, 88), (0, 88)]
        body = smooth(W, H, turned(W, H, prof))
        cross = np.maximum(rect(W, H, c - 7, 34, c + 7, 90, 3), rect(W, H, c - 22, 48, c + 22, 62, 3))
        body = np.maximum(body, cross)
        body = np.maximum(body, ellipses(W, H, [(c, 90, 42, 9, 0)]))
        y_top = 34
    else:  # knight, facing left
        pts = [(64, 342), (176, 342), (178, 324), (166, 314), (156, 306), (162, 296), (156, 288), (162, 270), (170, 236), (172, 196), (168, 158),
               (156, 122), (142, 94), (128, 74), (124, 52), (114, 64), (100, 60), (82, 70), (66, 88), (50, 110), (34, 132), (28, 148), (36, 158),
               (54, 158), (72, 150), (88, 156), (90, 176), (80, 204), (72, 236), (72, 262), (80, 288), (74, 296), (84, 306), (74, 314), (62, 324)]
        body = smooth(W, H, pts)
        y_top = 52
    art = blank(W, H)
    col, col2, grain, hi = (EBONY, EBONY_L, "#0e0a08", "#8a6a54") if dark else (BOX, BOX_D, "#9a6a36", "#fff3d8")
    art = wood(art, body, col, col2, grain, nx(), 1.5 if kind != "knight" else 1.2, 6, 0.32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # turned-wood shading: light from the left, a bright rim, darker right side
    shade = np.clip((xx - c + 10) / 70, 0, 1) * body
    art = G(art, shade, "#1a0e06" if not dark else "#000000", seed=nx(), density=0.45 if not dark else 0.4, edge=0, bloom=0.2, rough=2, feather=2.5)
    rim = np.clip(gaussian_filter(body, 2.5) - gaussian_filter(np.roll(body, 6, 1), 2.5), 0, 1) * body
    art = G(art, rim * 1.4, hi, seed=nx(), density=0.6 if dark else 0.45, edge=0, bloom=0, rough=1, feather=1.5)
    # incised rings
    rings = []
    for y in ([300, 282] if kind != "knight" else [300, 286]):
        rings.append(([(c - 60, y), (c + 60, y)], 1.6, None))
    if kind == "king":
        rings += [([(c - 40, 136), (c + 40, 136)], 1.6, None), ([(c - 44, 100), (c + 44, 100)], 1.4, None)]
    if kind == "pawn":
        rings += [([(c - 44, 172), (c + 44, 172)], 1.6, None)]
    art = G(art, strokes(W, H, rings) * body, "#000000" if dark else "#6a4420", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.6)
    if kind == "knight":
        mane = strokes(W, H, [(curve([(126, 70), (150, 104), (164, 150), (168, 210), (166, 260)], 30), 10, (0.1, 0.3))])
        notches = strokes(W, H, [([(150 + k * 2, 100 + k * 26), (162 + k * 2, 96 + k * 26)], 2.0, None) for k in range(6)])
        art = G(art, mane * body, "#000000" if dark else "#7a4e24", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1, feather=1.2)
        art = G(art, notches * body, "#000000" if dark else "#5a3414", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.5)
        eye = ellipses(W, H, [(88, 92, 6, 4, -20)])
        art = GP(art, eye, "#120c08" if not dark else "#d8b88e", seed=nx(), rough=0.3)
        mouth = strokes(W, H, [(curve([(30, 146), (48, 146), (60, 140)], 8), 2, (0.2, 0.2)), (curve([(40, 120), (46, 126)], 4), 2.4, None)])
        art = G(art, mouth, "#000000" if dark else "#4a2a10", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = edge_ink(art, nx(), "#120c08", 0.5)
    shadow = gaussian_filter(ellipses(W, H, [(c + 12, 344, 92, 12, 0)]), 4)
    sh = np.concatenate([np.zeros((H, W, 3), np.float32), (shadow * 0.35)[..., None]], -1)
    art = over(sh, art)
    clear()
    return art


if "pieces" in PARTS:
    for kind, dark, name in [("king", False, "king"), ("knight", True, "knight"), ("pawn", False, "pawn"), ("pawn", True, "pawn-d"), ("knight", False, "knight-l"), ("king", True, "king-d")]:
        a = piece(kind, dark)
        preview(a, f"lc-{name}", CREAM)
        save(a, f"{OUT}/{name}.webp", max_w=170, quality=84)

if "clock" in PARTS:
    W, H = 400, 300
    nx = Seq(7400)
    art = blank(W, H)
    top = poly(W, H, [(70, 70), (330, 70), (356, 104), (44, 104)])
    front = rect(W, H, 40, 100, 360, 272, 16)
    art = wood(art, front, WALNUT, WALNUT_D, "#2e1a0c", nx(), 0.0, 6, 0.3)
    art = wood(art, top, "#8a5634", WALNUT, "#3a2010", nx(), 0.0, 6, 0.25)
    # buttons (left pressed down)
    for x, y, h in [(125, 64, 10), (275, 48, 26)]:
        stem = rect(W, H, x - 9, y, x + 9, 74, 3)
        art = FO(art, stem, "#b88a3e", seed=nx(), emboss=0.4)
        cap = ellipses(W, H, [(x, y, 20, 8, 0)])
        art = GP(art, cap, "#c4432f" if x < 200 else "#2a1d16", seed=nx(), rough=0.4)
    for cx in (125, 275):
        ring = circles(W, H, [(cx, 186, 66)])
        art = FO(art, ring, "#c9a14a", seed=nx(), emboss=0.8, sparkle=0.05)
        face = circles(W, H, [(cx, 186, 56)])
        art = GP(art, face, "#f7efdc", "#ebe0c6", seed=nx(), rough=0.4)
        ticks = []
        for k in range(12):
            a = k * math.tau / 12
            r0 = 44 if k % 3 else 40
            ticks.append(([(cx + math.cos(a) * r0, 186 + math.sin(a) * r0), (cx + math.cos(a) * 51, 186 + math.sin(a) * 51)], 2.6 if k % 3 == 0 else 1.6, None))
        art = ink(art, strokes(W, H, ticks), INK, nx(), 0.9)
        # hands: left clock near the flag, right clock relaxed
        hm, hh = (-1.75, -2.35) if cx < 200 else (0.6, -0.9)
        hands = strokes(W, H, [([(cx, 186), (cx + math.cos(hm) * 44, 186 + math.sin(hm) * 44)], 3.2, (0.0, 0.5)), ([(cx, 186), (cx + math.cos(hh) * 30, 186 + math.sin(hh) * 30)], 4.6, (0.0, 0.4))])
        art = ink(art, hands, INK, nx(), 0.95)
        flag = poly(W, H, [(cx + 6, 136), (cx + 22, 132), (cx + 18, 148)] if cx < 200 else [(cx - 2, 132), (cx + 14, 136), (cx + 4, 146)])
        art = GP(art, flag, "#c4432f", seed=nx(), rough=0.3)
        art = GP(art, circles(W, H, [(cx, 186, 5)]), "#c9a14a", seed=nx(), rough=0.2)
        gl = smooth(W, H, ellipse_pts(cx - 18, 160, 24, 12, 12, -0.6))
        art = G(art, gl, "#ffffff", seed=nx(), density=0.35, edge=0, bloom=0, rough=2, feather=3)
    plate = rect(W, H, 170, 240, 230, 258, 4)
    art = FO(art, plate, "#c9a14a", seed=nx())
    art = edge_ink(art, nx(), "#1a0e06", 0.4)
    preview(art, "lc-clock", CREAM)
    save(art, f"{OUT}/clock.webp", max_w=300, quality=84)
    clear()
