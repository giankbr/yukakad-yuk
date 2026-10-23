"""Pulau Penyengat — gouache scene of the yellow-and-green royal mosque on Penyengat island seen across the strait
from Tanjungpinang, pompong boats, Malay carved woodwork (lebah bergantung eave, selembayung, awan larat).
Run: python3 -I pulau-penyengat.py [part ...]  parts: scene pompong eave selembayung divider kuntum
Assets -> public/themes/art/pulau-penyengat/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l2_lib import *

OUT = outdir("pulau-penyengat")
PARTS = sys.argv[1:] or ["scene", "pompong", "eave", "selembayung", "divider", "kuntum"]
YEL, YEL_L, YEL_D = "#e6b92e", "#f3d672", "#b98a17"
GRN, GRN_L, GRN_D = "#23603f", "#3f8a5c", "#143a27"
SEA, SEA_D, SEA_L = "#3c8f87", "#245f5c", "#8cc4b6"
CREAM = "#fbf4e0"
WHITE = "#f7f1e2"


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def onion(cx, by, w, h, n=28):
    """Dome outline: bulb with pointed tip (bottom at by)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        y = by - h * t
        r = w / 2 * (math.sin(math.pi * min(1, t * 1.05)) ** 0.75) * (1.08 - 0.5 * t)
        if t > 0.86:
            r *= (1 - t) / 0.14 * 0.6
        pts.append((cx + r, y))
    pts += [(cx - x + cx - cx, y) for x, y in []]
    left = [(2 * cx - x, y) for x, y in reversed(pts)]
    return pts + left


def dome(art, W, H, cx, by, w, h, nx, base_h=10):
    drum = rect(W, H, cx - w * 0.46, by - base_h, cx + w * 0.46, by)
    art = GP(art, drum, YEL, YEL_D, seed=nx(), rough=0.8, streak=0.8, pad=6)
    art = GP(art, strokes(W, H, [([(cx - w * 0.47, by - base_h), (cx + w * 0.47, by - base_h)], 2.2, None)]), GRN, seed=nx(), rough=0.4, pad=4)
    d = shapes(W, H, [onion(cx, by - base_h, w, h)])
    art = GP(art, d, YEL_L, YEL, seed=nx(), rough=0.8, streak=0.9, pad=6)
    # shade the right side (light from the left/morning)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sh = d * np.clip((xx - cx) / (w * 0.5), 0, 1) ** 1.4
    art = G(art, sh, YEL_D, seed=nx(), density=0.6, edge=0.1, bloom=0.1, rough=1, feather=1.2)
    ribs = strokes(W, H, [(curve([(cx + o * w * 0.42, by - base_h - 2), (cx + o * w * 0.3, by - base_h - h * 0.5), (cx, by - base_h - h * 0.92)], 14), 1.2, None) for o in (-0.5, 0, 0.5)])
    art = G(art, ribs * d, GRN, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.3)
    tip = strokes(W, H, [([(cx, by - base_h - h * 0.9), (cx, by - base_h - h - 14)], 2.4, None)])
    art = GP(art, np.maximum(tip, circles(W, H, [(cx, by - base_h - h * 0.95, 3.4)])), GRN_D, seed=nx(), rough=0.4, pad=4)
    return art


def minaret(art, W, H, cx, by, top, w, nx):
    shaft = shapes(W, H, [[(cx - w / 2, by), (cx - w * 0.42, top), (cx + w * 0.42, top), (cx + w / 2, by)]], smooth=False)
    art = GP(art, shaft, YEL, YEL_D, seed=nx(), rough=0.6, streak=1.0, pad=6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, shaft * np.clip((xx - cx) / (w * 0.5), 0, 1), YEL_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=0.8)
    # green rings + balconies
    rings = []
    for t in (0.25, 0.55, 0.8):
        y = by - (by - top) * t
        rings.append(([(cx - w * 0.62, y), (cx + w * 0.62, y)], 4.0, None))
    art = GP(art, strokes(W, H, rings), GRN, GRN_D, seed=nx(), rough=0.4, pad=4)
    wins = []
    for t in (0.4, 0.68):
        y = by - (by - top) * t
        wins.append([(cx - 2.6, y + 9), (cx - 2.6, y - 3), (cx, y - 7), (cx + 2.6, y - 3), (cx + 2.6, y + 9)])
    art = GP(art, shapes(W, H, wins, smooth=False), GRN_D, seed=nx(), rough=0.3, pad=4)
    # pencil spire
    sp = shapes(W, H, [[(cx - w * 0.55, top), (cx, top - w * 2.6), (cx + w * 0.55, top)]], smooth=False)
    art = GP(art, sp, GRN_L, GRN, seed=nx(), rough=0.5, pad=4)
    art = G(art, sp * np.clip((xx - cx) / (w * 0.4), 0, 1), GRN_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
    art = GP(art, strokes(W, H, [([(cx, top - w * 2.5), (cx, top - w * 2.5 - 12)], 1.8, None)]), GRN_D, seed=nx(), rough=0.3, pad=4)
    return art


def pompong_art(W, H, nx, hull=WHITE, stripe="#c8402e", roof=GRN, cabin="#2f6f9a", flag="#c8402e"):
    """Wooden pompong ferry, side view facing left: white hull with red & blue stripes, cabin with green roof."""
    art = blank(W, H)
    hullp = [(18, 120), (60, 150), (330, 150), (372, 118), (380, 100), (34, 104)]
    hm = shapes(W, H, [hullp])
    art = GP(art, hm, hull, "#e3dccb", seed=nx(), rough=1.0, streak=1.0, pad=6)
    st1 = hm * rect(W, H, 0, 112, W, 120)
    st2 = hm * rect(W, H, 0, 124, W, 129)
    art = GP(art, st1, stripe, seed=nx(), rough=0.5, pad=4)
    art = GP(art, st2, cabin, seed=nx(), rough=0.5, pad=4)
    keel = hm * rect(W, H, 0, 136, W, 160)
    art = G(art, keel, "#7d8a86", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1)
    gun = strokes(W, H, [([(30, 104), (378, 100)], 4, None)])
    art = GP(art, gun, "#6b4325", seed=nx(), rough=0.4, pad=4)
    # cabin with windows and posts
    cab = rect(W, H, 92, 60, 300, 104)
    art = GP(art, cab, cabin, "#24597d", seed=nx(), rough=0.8, pad=6)
    win = shapes(W, H, [[(x, 68), (x + 26, 68), (x + 26, 88), (x, 88)] for x in range(104, 290, 36)], smooth=False)
    art = GP(art, win, "#d9ecef", "#b6d6dc", seed=nx(), rough=0.4, pad=4)
    art = G(art, win * rect(W, H, 0, 80, W, 90), "#7fb0bc", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    rf = shapes(W, H, [[(78, 62), (92, 46), (306, 46), (318, 62)]], smooth=False)
    art = GP(art, rf, roof, GRN_D, seed=nx(), rough=0.6, pad=4)
    trim = strokes(W, H, [([(80, 62), (318, 62)], 2.4, None)])
    art = GP(art, trim, YEL, seed=nx(), rough=0.3, pad=4)
    # small flag on the stern pole
    pole = strokes(W, H, [([(340, 102), (340, 26)], 2.2, None)])
    art = GP(art, pole, "#5a3a20", seed=nx(), rough=0.3, pad=4)
    fl = shapes(W, H, [[(340, 26), (368, 32), (362, 38), (340, 42)]])
    art = GP(art, fl, flag, seed=nx(), rough=0.5, pad=4)
    # bow wave
    wave = strokes(W, H, [(curve([(10, 150), (36, 140), (64, 152), (120, 154)], 16), 4, (0.2, 0.6)), (curve([(300, 154), (340, 150), (390, 156)], 12), 3, (0.2, 0.6))])
    art = GP(art, wave, "#f4faf6", seed=nx(), rough=1.2, pad=6)
    return art


if "scene" in PARTS:
    W, H = 800, 620
    nx = Seq(21000)
    WL = 404
    art = painted_sky(W, H, [(0, "#fbf4e0"), (0.42, "#f4ecd6"), (0.6, "#e4ecdc"), (0.66, "#cfe1d6"), (1, "#cfe1d6")], seed=nx(), streak=0.8)
    # soft clouds
    cl = circles(W, H, [(140, 230, 24), (176, 222, 32), (214, 232, 22), (610, 200, 22), (644, 192, 30), (678, 202, 20)])
    art = G(art, cl, "#e2ebe1", seed=nx(), density=0.6, edge=0.1, bloom=0.4, rough=8, feather=4)
    # sea
    sea = painted_sky(W, H, [(0, SEA_L), (0.66, SEA_L), (0.7, SEA), (0.86, SEA), (1, SEA_D)], seed=nx(), streak=2.2)
    water = rect(W, H, -10, WL, W + 10, H + 10)
    art = art * (1 - water[..., None]) + sea * water[..., None]
    # island: low green land with trees and palms
    rng = random.Random(7)
    land = shapes(W, H, [[(-20, WL + 6), (-20, WL - 18), (120, WL - 30), (300, WL - 36), (520, WL - 36), (700, WL - 28), (W + 20, WL - 16), (W + 20, WL + 6)]])
    trees = circles(W, H, [(x, WL - 36 - rng.uniform(0, 22), rng.uniform(16, 30)) for x in list(range(-10, 210, 24)) + list(range(600, W + 20, 24))])
    art = GP(art, np.maximum(land, trees), "#4f8a52", "#3a6e44", seed=nx(), rough=3, streak=0.8, pad=8)
    lit = circles(W, H, [(x - 5, WL - 50 - rng.uniform(0, 14), rng.uniform(8, 14)) for x in list(range(-10, 210, 24)) + list(range(600, W + 20, 24))])
    art = G(art, lit * np.maximum(land, trees), "#9cc27a", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=3)
    for x, h, ln in [(70, 120, 0.12), (130, 96, -0.1), (680, 112, 0.1), (735, 130, -0.14), (590, 84, 0.08)]:
        art = GP(art, jw.palm(W, H, x, WL - 24, h, rng, ln), "#2f5a3a", "#24452e", seed=nx(), rough=1.0, pad=6)
    # mosque
    cx = 400
    BY = WL - 30   # ground of mosque
    plat = rect(W, H, 236, BY - 12, 564, BY + 4)
    art = GP(art, plat, "#e9dfc6", "#cfc3a4", seed=nx(), rough=0.8, pad=6)
    steps = strokes(W, H, [([(360, BY - 4 + k * 4), (440, BY - 4 + k * 4)], 1.4, None) for k in range(4)])
    art = G(art, steps, "#9c8f70", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
    # back row of domes (behind the roof line)
    for dx, w, h in [(-120, 40, 40), (-60, 44, 44), (60, 44, 44), (120, 40, 40)]:
        art = dome(art, W, H, cx + dx, BY - 118, w, h, nx, 8)
    body = rect(W, H, 250, BY - 108, 550, BY - 12)
    art = GP(art, body, YEL, YEL_D, seed=nx(), rough=0.8, streak=1.0, pad=6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, body * np.clip((BY - 12 - yy) / 96, 0, 1) * 0 + body * np.clip((xx - 470) / 80, 0, 1), YEL_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    # green cornice + parapet
    corn = rect(W, H, 244, BY - 116, 556, BY - 104)
    art = GP(art, corn, GRN, GRN_D, seed=nx(), rough=0.5, pad=4)
    par = shapes(W, H, [[(x, BY - 116), (x + 6, BY - 124), (x + 12, BY - 116)] for x in range(246, 552, 12)], smooth=False)
    art = GP(art, par, GRN, seed=nx(), rough=0.3, pad=4)
    # arched openings with green frames
    arches = []
    frames = []
    for x in range(268, 540, 38):
        ap = [(x, BY - 14), (x, BY - 70), (x + 4, BY - 82), (x + 12, BY - 90), (x + 20, BY - 82), (x + 24, BY - 70), (x + 24, BY - 14)]
        arches.append(ap)
        frames.append([(x - 4, BY - 12), (x - 4, BY - 72), (x + 1, BY - 86), (x + 12, BY - 96), (x + 23, BY - 86), (x + 28, BY - 72), (x + 28, BY - 12)])
    art = GP(art, shapes(W, H, frames, smooth=False), GRN, GRN_D, seed=nx(), rough=0.4, pad=4)
    am = shapes(W, H, arches, smooth=False)
    art = GP(art, am, "#4f6e55", "#365443", seed=nx(), rough=0.4, pad=4)
    art = G(art, am * rect(W, H, 0, BY - 96, W, BY - 64), "#1f3a2a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    # window grilles (light bars)
    bars = strokes(W, H, [([(x + 12, BY - 84), (x + 12, BY - 16)], 1.2, None) for x in range(268, 540, 38)] + [([(x + 2, BY - 50), (x + 22, BY - 50)], 1.2, None) for x in range(268, 540, 38)])
    art = G(art, bars * am, "#c7d6b4", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, feather=0.3)
    # cornice shadow + dry-brush wall texture
    csh = body * np.clip((yy - (BY - 104)) / 18, 0, 1) * np.clip(((BY - 84) - yy) / 18, 0, 1)
    art = G(art, csh * (1 - am), YEL_D, seed=nx(), density=0.6, edge=0, bloom=0.1, rough=1)
    dry = strokes(W, H, [([(x, y), (x + rng.uniform(20, 60), y + rng.uniform(-1, 1))], 1.6, (0.3, 0.3)) for x, y in [(rng.uniform(250, 520), rng.uniform(BY - 100, BY - 16)) for _ in range(40)]])
    art = G(art, dry * body * (1 - am), "#f6dd8a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.3)
    # front row of domes on the roof
    for dx, w, h in [(-104, 52, 52), (104, 52, 52), (-48, 60, 62), (48, 60, 62)]:
        art = dome(art, W, H, cx + dx, BY - 116, w, h, nx, 10)
    art = dome(art, W, H, cx, BY - 112, 82, 90, nx, 14)
    # minarets at the corners (two front, taller)
    for mx in (226, 574):
        art = minaret(art, W, H, mx, BY + 2, BY - 214, 25, nx)
    # reflections in the water
    seg = art[2 * WL - H:WL][::-1].copy() if 2 * WL - H > 0 else art[:WL][::-1][: H - WL].copy()
    rr = seg[: H - WL]
    yy2 = np.arange(rr.shape[0], dtype=np.float32)
    gy, gx = np.mgrid[0:rr.shape[0], 0:W].astype(np.float32)
    shift = (np.sin(gy * 0.6) * 2.4 + np.sin(gy * 0.17 + gx * 0.01) * 3.5)
    rr = np.stack([map_coordinates(rr[..., c], [gy, gx + shift], order=1, mode="nearest") for c in range(4)], -1)
    fade = (np.clip(1 - yy2 / rr.shape[0] * 1.6, 0, 1) * 0.42)[:, None]
    low = art[WL:WL + rr.shape[0]]
    low[..., :3] = low[..., :3] * (1 - fade[..., None]) + rr[..., :3] * fade[..., None]
    art[WL:WL + rr.shape[0]] = low
    ripple = strokes(W, H, [([(x, y), (x + rng.uniform(16, 70), y)], rng.uniform(1.2, 2.6), (0.3, 0.3)) for x, y in [(rng.uniform(-20, W), rng.uniform(WL + 6, H - 4)) for _ in range(110)]])
    art = G(art, ripple, "#e9f5ef", seed=nx(), density=0.5, edge=0, bloom=0, rough=1, feather=0.4)
    dark_r = strokes(W, H, [([(x, y), (x + rng.uniform(20, 80), y)], 2, (0.3, 0.3)) for x, y in [(rng.uniform(-20, W), rng.uniform(WL + 40, H)) for _ in range(60)]])
    art = G(art, dark_r, SEA_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=1, feather=0.5)
    # foreground pelantar (wooden jetty piles) bottom-left
    piles = strokes(W, H, [([(x, H - 130 + (x % 7)), (x + 2, H + 10)], 9, None) for x in (24, 74, 124)])
    deck = shapes(W, H, [[(-20, H - 140), (150, H - 132), (150, H - 122), (-20, H - 128)]], smooth=False)
    art = GP(art, np.maximum(piles, deck), "#6b4a2c", "#4a301b", seed=nx(), rough=1.0, streak=1.2, pad=6)
    # fade the top into the page cream
    yy = np.arange(H, dtype=np.float32)[:, None]
    art[..., 3] = (np.clip((yy - 40) / 150, 0, 1) * np.ones((1, W), np.float32))
    preview(art, "pp-scene", bg=CREAM)
    save_full(art, f"{OUT}/scene.webp", size=(640, 496), quality=80)
    clear()

if "pompong" in PARTS:
    W, H = 400, 170
    art = pompong_art(W, H, Seq(22000))
    preview(art, "pp-pompong", bg=SEA)
    save(art, f"{OUT}/pompong.webp", max_w=220, quality=84)
    art = pompong_art(W, H, Seq(22100), hull="#f2e6c8", stripe=GRN, roof="#c8402e", cabin="#e6b92e", flag=GRN)
    save(art, f"{OUT}/pompong2.webp", max_w=160, quality=84)
    clear()

if "eave" in PARTS:
    # lebah bergantung: carved hanging fringe under a green fascia board (seamless repeat-x, period 40)
    W, H = 640, 96
    nx = Seq(23000)
    art = blank(W, H)
    board = rect(W, H, 0, 0, W, 30)
    art = GP(art, board, GRN, GRN_D, seed=nx(), rough=0.6, streak=1.2, pad=4)
    line = np.maximum(rect(W, H, 0, 6, W, 9), rect(W, H, 0, 23, W, 27))
    art = GP(art, line, YEL, YEL_D, seed=nx(), rough=0.3, pad=4)
    dots = circles(W, H, [(x + 20, 16, 3.2) for x in range(0, W, 40)])
    art = GP(art, dots, YEL_L, seed=nx(), rough=0.3, pad=4)
    drops, holes, small = [], [], []
    for x in range(0, W, 40):
        c = x + 20
        drops.append([(c - 16, 30), (c + 16, 30), (c + 15, 44), (c + 9, 58), (c + 3, 70), (c, 82), (c - 3, 70), (c - 9, 58), (c - 15, 44)])
        holes.append([(c, 38), (c + 6, 46), (c, 58), (c - 6, 46)])
        small.append([(x - 4, 30), (x + 4, 30), (x, 46)])
    dm = shapes(W, H, drops)
    hm = shapes(W, H, holes, smooth=False)
    sm = shapes(W, H, small, smooth=False)
    m = np.clip(np.maximum(dm, sm) - hm, 0, 1)
    art = GP(art, m, YEL, YEL_D, seed=nx(), rough=0.6, streak=0.8, pad=4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sh = m * (((xx % 40) - 20) > 2)
    art = G(art, sh.astype(np.float32) * m, YEL_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
    art = GP(art, circles(W, H, [(x + 20, 86, 3)]) if False else circles(W, H, [(x + 20, 84, 3.4) for x in range(0, W, 40)]), GRN, seed=nx(), rough=0.3, pad=4)
    rolled = np.roll(art, W // 2, 1)
    xx1 = np.arange(W, dtype=np.float32)
    wgt = np.clip(1 - np.minimum(xx1, W - xx1) / 80, 0, 1)[None, :, None]
    art = art * (1 - wgt) + rolled * wgt
    preview(art, "pp-eave", bg=CREAM)
    save_full(art, f"{OUT}/eave.webp", size=(320, 48), quality=86)
    clear()

if "selembayung" in PARTS:
    # crossed carved horns of the roof ridge, curled tips, leaf scrolls on the inner edge, a lotus bud between them
    W, H = 400, 250
    nx = Seq(24000)
    items, leaves = [], []
    for sgn in (-1, 1):
        X = lambda u: 200 + sgn * u
        horn = curve([(X(-30), 240), (X(20), 182), (X(70), 128), (X(118), 92), (X(158), 82), (X(176), 96)], 60)
        for i in range(len(horn) - 1):
            t = i / (len(horn) - 2)
            items.append(([horn[i], horn[i + 1]], 22 * (1 - t) + 9 * t, None))
        cx_, cy_ = X(168), 112
        items.append((spiral_pts(cx_, cy_, 17, 3, -math.pi / 2, 1.15, 40, sgn), 8, (0.0, 0.6)))
        for k, (x, y, a_) in enumerate(along(horn[10:46], 30)):
            # inner side normal (towards the centre/up)
            nxn, nyn = math.sin(a_) * sgn, -math.cos(a_) * sgn
            if nyn > 0:
                nxn, nyn = -nxn, -nyn
            px, py = x + nxn * 14, y + nyn * 14
            items.append((spiral_pts(px, py, 10, 2, math.atan2(-nyn, -nxn), 1.0, 24, -sgn), 4.5, (0.0, 0.5)))
            leaves.append(petal_pts(x + nxn * 6, y + nyn * 6, 30, 8, math.atan2(nyn, nxn) - sgn * 0.7, n=12))
    lotus = [petal_pts(200, 190, 72, 17, -math.pi / 2, n=14)]
    sep = [petal_pts(198, 192, 54, 12, -math.pi / 2 - 0.62, n=12, cup=-0.6), petal_pts(202, 192, 54, 12, -math.pi / 2 + 0.62, n=12, cup=0.6)]
    lm = shapes(W, H, lotus)
    m = np.clip(np.maximum(strokes(W, H, items), shapes(W, H, leaves)) - gaussian_filter(np.maximum(lm, shapes(W, H, sep)), 2) * 1.5, 0, 1)
    art = blank(W, H)
    art = GP(art, m, YEL, YEL_D, seed=nx(), rough=0.8, streak=0.9, pad=6)
    lo = np.clip(m - np.roll(np.roll(m, -2, 0), -2, 1), 0, 1)
    art = G(art, lo, "#8a6512", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    hi = np.clip(m - np.roll(np.roll(m, 2, 0), 2, 1), 0, 1)
    art = G(art, hi, "#fff0b0", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    sm = shapes(W, H, sep)
    art = GP(art, lm, YEL_L, YEL, seed=nx(), rough=0.5, pad=4)
    art = GP(art, sm, GRN, GRN_L, seed=nx(), rough=0.5, pad=4)
    vein = strokes(W, H, [([(200, 184), (200, 128)], 2, None)])
    art = G(art, vein * lm, YEL_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    preview(art, "pp-selembayung", bg=CREAM)
    save(art, f"{OUT}/selembayung.webp", max_w=200, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 460, 70
    nx = Seq(25000)
    items, leaves = [], []
    for sgn in (-1, 1):
        X = lambda u: 230 + sgn * u
        vine = curve([(X(26), 35), (X(70), 24), (X(120), 44), (X(170), 26), (X(212), 38)], 60)
        items.append((vine, 3.4, (0.0, 0.3)))
        for k, (x, y, a) in enumerate(along(vine, 42)):
            d = -1 if k % 2 else 1
            cur = spiral_pts(x + sgn * 8, y + d * 10, 9, 2, (math.pi / 2) * -d, 1.0, 22, sgn * d)
            items.append((cur, 2.4, (0.0, 0.5)))
            leaves.append(petal_pts(x, y, 15, 5, (0 if sgn > 0 else math.pi) + d * 0.9, n=10))
    vm = strokes(W, H, items); lm = shapes(W, H, leaves)
    bud = shapes(W, H, [petal_pts(230, 50, 34, 11, -math.pi / 2, n=12), petal_pts(222, 40, 22, 7, -math.pi / 2 - 0.9, n=10), petal_pts(238, 40, 22, 7, -math.pi / 2 + 0.9, n=10)])
    art = blank(W, H)
    art = GP(art, np.maximum(vm, lm), GRN, GRN_L, seed=nx(), rough=0.6, pad=4)
    art = GP(art, bud, YEL, YEL_D, seed=nx(), rough=0.5, pad=4)
    preview(art, "pp-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=86)
    clear()

if "kuntum" in PARTS:
    # bunga cengkih: four-petal carved flower, yellow with green heart
    W, H = 140, 140
    nx = Seq(26000)
    pet = shapes(W, H, [petal_pts(70, 70, 60, 20, a, n=14) for a in (0, math.pi / 2, math.pi, -math.pi / 2)])
    small = shapes(W, H, [petal_pts(70, 70, 40, 10, a, n=12) for a in (math.pi / 4, 3 * math.pi / 4, -math.pi / 4, -3 * math.pi / 4)])
    art = GP(blank(W, H), small, GRN, GRN_L, seed=nx(), rough=0.4, pad=4)
    art = GP(art, pet, YEL, YEL_D, seed=nx(), rough=0.6, pad=4)
    lo = np.clip(pet - np.roll(np.roll(pet, -2, 0), -2, 1), 0, 1)
    art = G(art, lo, "#8a6512", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = GP(art, circles(W, H, [(70, 70, 11)]), GRN_D, seed=nx(), rough=0.3, pad=4)
    art = GP(art, circles(W, H, [(70, 70, 4)]), YEL_L, seed=nx(), rough=0.2, pad=4)
    preview(art, "pp-kuntum", bg=CREAM)
    save(art, f"{OUT}/kuntum.webp", max_w=70, quality=86)
    clear()
