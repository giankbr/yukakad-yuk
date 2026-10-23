"""Pelantikan Pengurus — formal inauguration stage of a (fictional) association: burgundy velvet drapes with gold
fringe and tie-backs, a teak podium with a gold seal, two flag stands in generic association colours (no national or
real emblems), a gold satin ribbon and a pressed-foil certificate seal with ribbon tails. Gouache + foil.
Run: python3 -I pelantikan-pengurus.py [part ...]  parts: velvet curtain stage seal ribbon
Assets -> public/themes/art/pelantikan-pengurus/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n4_lib import *

OUT = outdir("pelantikan-pengurus")
PARTS = sys.argv[1:] or ["velvet", "curtain", "stage", "seal", "ribbon"]
VEL, VEL_D, VEL_L = "#5c1324", "#330812", "#8a2a3c"
GOLD, GOLD_L, GOLD_D = "#c9a24a", "#ead08a", "#8a6a26"
TEAK, TEAK_D, TEAK_L = "#6a3d22", "#3a1f10", "#94603a"
TEAL, TEAL_D = "#1f5257", "#123236"
IVORY = "#f7f1e3"


def velvet():
    """Seamless burgundy velvet: soft nap mottling with faint vertical pile direction."""
    W = H = 384
    n1 = wrap_noise(W, H, 3, 26) - 0.5
    n2 = wrap_noise(W, H, 4, (8, 1.2)) - 0.5
    n3 = wrap_noise(W, H, 5, 0.7) - 0.5
    v = 1 + n1 * 0.22 + n2 * 0.1 + n3 * 0.05
    rgb = col3(VEL)[None, None] * v[..., None]
    save_rgb(rgba(np.clip(rgb, 0, 1), np.ones((H, W), np.float32)), f"{OUT}/velvet.webp", quality=72)


def fold_shade(W, H, x0, x1, n, seed, depth=0.45):
    """Vertical fold shading field across [x0, x1]: n soft folds, values ~0.55..1.15."""
    xx = np.arange(W, dtype=np.float32)
    t = np.clip((xx - x0) / max(1, (x1 - x0)), 0, 1)
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6)
    f = np.sin(t * math.pi * n + ph + np.sin(t * 7) * 0.4)
    f = 1 + depth * 0.5 * f + depth * 0.25 * np.sign(f) * np.abs(f) ** 3
    return np.tile(f[None, :], (H, 1)).astype(np.float32)


def curtain():
    """Theatre drapes framing the top of the stage: left/right panels gathered by gold tie-backs, a swagged valance with
    gold bullion fringe. Transparent centre."""
    W, H = 760, 520
    nx = Seq(9100)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for side in (-1, 1):
        # panel outline: full width at top, pinched at the tie-back, flaring to the bottom edge
        def X(u):
            return u if side < 0 else W - u
        pts = [(X(-10), -10), (X(150), -10), (X(140), 120), (X(96), 250), (X(62), 300), (X(84), 360), (X(118), H + 10), (X(-10), H + 10)]
        m = shapes(W, H, [pts])
        fs = fold_shade(W, H, 0 if side < 0 else W - 160, 160 if side < 0 else W, 5, nx(), 0.6)
        rgb = col3(VEL)[None, None] * fs[..., None]
        # light from top centre: lighter on inner edges
        inner = np.clip(1 - np.abs(xx - (140 if side < 0 else W - 140)) / 140, 0, 1)
        rgb = rgb * (0.8 + 0.35 * inner[..., None])
        nap = fbm(W, H, nx(), 20, 3)
        rgb = rgb * (0.93 + 0.12 * nap[..., None])
        lay = rgba(np.clip(rgb, 0, 1), m)
        lay = over(lay, rgba(np.ones((H, W, 3), np.float32) * col3(VEL_D), m * np.clip((yy - 260) / 260, 0, 1) * 0.35))
        art = over(art, soft_shadow(m, "#12030a", 10, 0.5, -6 * side, 6))
        art = over(art, lay)
        # tie-back: gold rope + tassel
        tx = X(72); ty = 300
        rope = strokes(W, H, [(curve([(X(-4), 282), (X(40), 296), (tx, 302), (X(100), 296)], 20), 9, None)])
        art = FO(art, rope, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
        knot = circles(W, H, [(tx, 304, 13)])
        art = FO(art, knot, GOLD, seed=nx(), emboss=0.8)
        tas = []
        for k in range(14):
            dx = (k - 6.5) * 2.2
            tas.append(([(tx + dx * 0.4, 314), (tx + dx, 350), (tx + dx * 1.2, 372)], 2.0, None))
        tm = strokes(W, H, tas)
        cap = shapes(W, H, [[(tx - 9, 312), (tx + 9, 312), (tx + 12, 330), (tx - 12, 330)]], smooth=True)
        art = FO(art, np.clip(tm + cap, 0, 1), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    # valance with three swags
    swags = []
    for k, (a, b) in enumerate([(-20, 270), (240, 520), (490, 780)]):
        mid = (a + b) / 2
        dip = 92 if k == 1 else 104
        top = [(a, -10), (b, -10)]
        bottom = curve([(b, 18), (mid + (b - a) * 0.3, dip - 10), (mid, dip), (mid - (b - a) * 0.3, dip - 10), (a, 18)], 40)
        swags.append(top + bottom)
    sm = shapes(W, H, swags)
    rgb = col3(VEL)[None, None] * np.ones((H, W, 1), np.float32)
    # horizontal swag folds: bands following the dip
    band = np.sin((yy - 10 * np.cos((xx % 260) / 260 * math.tau)) / 13) * 0.18 + 1
    rgb = rgb * band[..., None] * (0.92 + 0.12 * fbm(W, H, nx(), 20, 3)[..., None])
    art = over(art, soft_shadow(sm, "#12030a", 8, 0.55, 0, 8))
    art = over(art, rgba(np.clip(rgb, 0, 1), sm))
    # gold braid on the swag edge + bullion fringe
    edges = []
    fr = []
    for k, (a, b) in enumerate([(-20, 270), (240, 520), (490, 780)]):
        mid = (a + b) / 2
        dip = 92 if k == 1 else 104
        e = curve([(b, 18), (mid + (b - a) * 0.3, dip - 10), (mid, dip), (mid - (b - a) * 0.3, dip - 10), (a, 18)], 60)
        edges.append((e, 6, None))
        for x, y, ang in along(e, 5):
            fr.append(([(x, y), (x + 0.6, y + 16)], 2.0, (0.0, 0.3)))
    art = FO(art, strokes(W, H, edges), GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    art = FO(art, strokes(W, H, fr), GOLD_D, seed=nx(), emboss=0.4, sparkle=0.05)
    # rosettes where swags meet
    for x in (255, 505):
        ro = circles(W, H, [(x, 22, 16)])
        art = FO(art, ro, GOLD, seed=nx(), emboss=0.9)
    art = add_grain(art, 3, 0.03)
    preview(art, "pp-curtain", bg="#2a0710")
    save(art, f"{OUT}/curtain.webp", max_w=720, quality=78)


def flag(W, H, x, y_top, h, col, col2, nx, side=1, stripe=None):
    """Indoor flag on a stand: wood pole with gold finial, fabric hanging in soft vertical folds, gold fringe."""
    art = blank(W, H)
    pole = strokes(W, H, [([(x, y_top), (x, y_top + h)], 6, None)])
    base = shapes(W, H, [[(x - 26, y_top + h), (x + 26, y_top + h), (x + 18, y_top + h - 14), (x - 18, y_top + h - 14)]], smooth=False)
    art = GP(art, pole, TEAK_L, TEAK, seed=nx(), rough=0.4)
    art = FO(art, base, GOLD, seed=nx(), emboss=0.6)
    fin = shapes(W, H, [[(x, y_top - 26), (x + 9, y_top - 8), (x, y_top + 2), (x - 9, y_top - 8)]], smooth=False)
    art = FO(art, fin, GOLD, seed=nx(), emboss=0.8)
    fw, fh = 104, 214
    x0 = x if side > 0 else x - fw
    pts = [(x0, y_top + 6), (x0 + fw, y_top + 6), (x0 + fw + 2 * side, y_top + 6 + fh * 0.5), (x0 + fw - 6 * side, y_top + 6 + fh), (x0 + 6 * side, y_top + 6 + fh * 0.98)]
    # fabric hangs from the pole and sags: draw as smooth shape
    pts = [(x, y_top + 4), (x + fw * side, y_top + 12), (x + (fw - 4) * side, y_top + fh * 0.5), (x + fw * 0.6 * side, y_top + fh * 0.9), (x + 14 * side, y_top + fh * 1.04), (x, y_top + fh * 0.96)]
    m = shapes(W, H, [pts])
    fs = fold_shade(W, H, min(x, x + fw * side), max(x, x + fw * side), 3.5, nx(), 0.55)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rgb = col3(col)[None, None] * fs[..., None]
    # diagonal drape folds
    drape = np.sin(((xx - x) * side * 0.8 + (yy - y_top) * 0.6) / 13) * 0.12 + 1
    rgb = rgb * drape[..., None]
    rgb = rgb * (0.94 + 0.1 * fbm(W, H, nx(), 18, 3)[..., None])
    art = over(art, rgba(np.clip(rgb, 0, 1), m))
    edge = strokes(W, H, [(curve([(x + (fw - 4) * side, y_top + fh * 0.5), (x + fw * 0.6 * side, y_top + fh * 0.9), (x + 14 * side, y_top + fh * 1.04)], 24), 4, None)])
    art = FO(art, edge, GOLD, seed=nx(), emboss=0.5, sparkle=0.05)
    # small abstract gold roundel (no real emblem)
    rx, ry = x + fw * 0.5 * side, y_top + fh * 0.36
    art = FO(art, np.clip(ring_mask(W, H, rx, ry, 17, 3) + circles(W, H, [(rx, ry, 6)]), 0, 1), GOLD, seed=nx(), emboss=0.6)
    return art


def stage():
    """The stage: dark backdrop wall is NOT painted (the page is), only the floor edge, a teak podium with a gold seal,
    two flag stands and low floral troughs."""
    W, H = 760, 520
    nx = Seq(9700)
    art = blank(W, H)
    cx = W / 2
    # stage floor: front edge with gold trim
    floor = shapes(W, H, [[(-10, 400), (W + 10, 400), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    planks = (np.sin(xx / 18 + np.sin(yy / 40)) * 0.04 + 1)
    frgb = col3(TEAK)[None, None] * planks[..., None] * (0.85 + 0.25 * np.clip((yy - 400) / 120, 0, 1))[..., None]
    frgb = frgb * (0.92 + 0.12 * fbm(W, H, nx(), 30, 3)[..., None])
    art = over(art, rgba(np.clip(frgb, 0, 1), floor))
    # floor reflection glow under the podium
    art = over(art, glow(ellipses(W, H, [(cx, 420, 120, 14, 0)]), "#e9c98a", 18, 0.25))
    trim = shapes(W, H, [[(-10, 396), (W + 10, 396), (W + 10, 406), (-10, 406)]], smooth=False)
    art = FO(art, trim, GOLD, seed=nx(), emboss=0.5)
    front = shapes(W, H, [[(-10, 452), (W + 10, 452), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3(VEL_D), front * 0.85))
    art = FO(art, shapes(W, H, [[(-10, 450), (W + 10, 450), (W + 10, 456), (-10, 456)]], smooth=False), GOLD_D, seed=nx(), emboss=0.4)
    # flags
    art = over(art, flag(W, H, 118, 120, 286, TEAL, GOLD, nx, 1))
    art = over(art, flag(W, H, W - 118, 120, 286, "#e6cf98", IVORY, nx, -1))
    # podium: tapered teak lectern with a slanted top
    pod = shapes(W, H, [[(cx - 90, 230), (cx + 90, 230), (cx + 74, 404), (cx - 74, 404)]], smooth=False)
    top = shapes(W, H, [[(cx - 104, 214), (cx + 104, 214), (cx + 96, 236), (cx - 96, 236)]], smooth=False)
    art = over(art, soft_shadow(pod, "#12030a", 10, 0.5, 6, 8))
    fs = fold_shade(W, H, cx - 90, cx + 90, 1.0, 3, 0.25)
    prgb = col3(TEAK)[None, None] * fs[..., None]
    grain = np.sin(yy / 3.5 + fbm(W, H, nx(), 24, 2) * 14) * 0.04 + 1
    prgb = prgb * grain[..., None] * (0.9 + 0.15 * fbm(W, H, nx(), 40, 2)[..., None])
    art = over(art, rgba(np.clip(prgb, 0, 1), pod))
    # carved panel inset
    inset = shapes(W, H, [[(cx - 66, 262), (cx + 66, 262), (cx + 56, 384), (cx - 56, 384)]], smooth=False)
    ring_in = np.clip(inset - shapes(W, H, [[(cx - 60, 268), (cx + 60, 268), (cx + 51, 378), (cx - 51, 378)]], smooth=False), 0, 1)
    art = FO(art, ring_in, GOLD_D, seed=nx(), emboss=0.4)
    art = GP(art, top, TEAK_L, TEAK, seed=nx(), rough=0.6, streak=1.0)
    art = FO(art, shapes(W, H, [[(cx - 104, 234), (cx + 104, 234), (cx + 98, 240), (cx - 98, 240)]], smooth=False), GOLD, seed=nx(), emboss=0.5)
    # gold seal on the podium front (simple rosette, no text or real emblem)
    sc = (cx, 318)
    teeth = []
    for k in range(48):
        a = k * math.tau / 48
        r = 40 if k % 2 == 0 else 34
        teeth.append((sc[0] + math.cos(a) * r, sc[1] + math.sin(a) * r))
    sm = shapes(W, H, [teeth], smooth=False)
    art = FO(art, sm, GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    art = FO(art, ring_mask(W, H, sc[0], sc[1], 25, 2.5), GOLD_D, seed=nx(), emboss=0.6)
    star = [(sc[0] + math.cos(-math.pi / 2 + k * math.pi / 5) * (14 if k % 2 == 0 else 6), sc[1] + math.sin(-math.pi / 2 + k * math.pi / 5) * (14 if k % 2 == 0 else 6)) for k in range(10)]
    art = FO(art, shapes(W, H, [star], smooth=False), GOLD_L, seed=nx(), emboss=0.9)
    # microphone on gooseneck
    mic = strokes(W, H, [(curve([(cx + 40, 214), (cx + 46, 186), (cx + 30, 160)], 20), 3, None)])
    art = GP(art, mic, "#222222", "#444444", seed=nx(), rough=0.3)
    art = GP(art, ellipses(W, H, [(cx + 28, 156, 6, 9, -30)]), "#1a1a1a", "#555555", seed=nx(), rough=0.3)
    # floral troughs at the stage front: low mounds of white and burgundy blooms with leaves
    rng = random.Random(4)
    for (x0, x1) in [(160, 300), (W - 300, W - 160)]:
        lv = []
        for _ in range(26):
            x = rng.uniform(x0, x1); y = rng.uniform(386, 402)
            a = -math.pi / 2 + rng.uniform(-1.3, 1.3)
            lv.append(petal_pts(x, y, rng.uniform(18, 28), rng.uniform(4, 6), a, n=10))
        art = GP(art, shapes(W, H, lv), "#3f5b34", "#2a3f24", seed=nx(), rough=0.8, streak=0.8)
        bl = [(rng.uniform(x0 + 6, x1 - 6), rng.uniform(372, 396), rng.uniform(6, 10)) for _ in range(22)]
        whites = circles(W, H, bl[::2]); reds = circles(W, H, bl[1::2])
        art = GP(art, whites, "#f4eee2", "#d8cfc0", seed=nx(), rough=1.2, streak=0.6)
        art = GP(art, reds, "#8a2a3c", "#5c1324", seed=nx(), rough=1.2, streak=0.6)
        art = over(art, flat(circles(W, H, [(x, y - r * 0.3, r * 0.35) for x, y, r in bl]), "#ffffff", 0.35))
        box = shapes(W, H, [[(x0 - 6, 398), (x1 + 6, 398), (x1, 420), (x0, 420)]], smooth=False)
        art = FO(art, box, GOLD_D, seed=nx(), emboss=0.4)
    art = add_grain(art, 7, 0.03)
    preview(art, "pp-stage", bg="#3a0b16")
    save(art, f"{OUT}/stage.webp", max_w=720, quality=78)


def seal():
    """Certificate seal: serrated gold foil rosette with concentric embossed rings, a star, and two burgundy ribbon
    tails with notched ends."""
    W, H = 300, 380
    nx = Seq(9900)
    art = blank(W, H)
    cx, cy = 150, 140
    for side in (-1, 1):
        tail = shapes(W, H, [[(cx + side * 10, cy + 40), (cx + side * 52, cy + 30), (cx + side * 96, cy + 220), (cx + side * 74, cy + 206), (cx + side * 62, cy + 236)]], smooth=False)
        fs = fold_shade(W, H, cx - 100, cx + 100, 2.0, nx(), 0.35)
        rgb = col3(VEL_L)[None, None] * fs[..., None] * (0.92 + 0.12 * fbm(W, H, nx(), 16, 2)[..., None])
        art = over(art, soft_shadow(tail, "#12030a", 5, 0.4, 3, 5))
        art = over(art, rgba(np.clip(rgb, 0, 1), tail))
        edge = strokes(W, H, [([(cx + side * 52, cy + 30), (cx + side * 96, cy + 220)], 2.2, None)])
        art = FO(art, edge, GOLD, seed=nx(), emboss=0.3)
    teeth = []
    for k in range(64):
        a = k * math.tau / 64
        r = 112 if k % 2 == 0 else 102
        teeth.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    sm = shapes(W, H, [teeth], smooth=False)
    art = over(art, soft_shadow(sm, "#12030a", 8, 0.45, 4, 8))
    art = FO(art, sm, GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    for r, w in [(90, 3.0), (82, 1.4), (56, 2.4)]:
        art = FO(art, ring_mask(W, H, cx, cy, r, w), GOLD_D, seed=nx(), emboss=0.9)
    # beaded ring
    beads = circles(W, H, [(cx + math.cos(a) * 70, cy + math.sin(a) * 70, 3.2) for a in np.linspace(0, math.tau, 36, endpoint=False)])
    art = FO(art, beads, GOLD_L, seed=nx(), emboss=1.0)
    star = [(cx + math.cos(-math.pi / 2 + k * math.pi / 5) * (40 if k % 2 == 0 else 17), cy + math.sin(-math.pi / 2 + k * math.pi / 5) * (40 if k % 2 == 0 else 17)) for k in range(10)]
    art = FO(art, shapes(W, H, [star], smooth=False), GOLD_L, seed=nx(), emboss=1.0, sparkle=0.2)
    preview(art, "pp-seal", bg=IVORY)
    save(art, f"{OUT}/seal.webp", max_w=220, quality=84)


def ribbon():
    """Gold satin ribbon banner with folded, notched ends (section divider)."""
    W, H = 380, 70
    nx = Seq(9950)
    art = blank(W, H)
    for side in (-1, 1):
        x = W / 2 + side * 150
        end = shapes(W, H, [[(x, 20), (x + side * 34, 24), (x + side * 26, 38), (x + side * 36, 52), (x, 48)]], smooth=False)
        art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3(GOLD_D) * 0.8, end))
        art = FO(art, end, GOLD_D, seed=nx(), emboss=0.4)
    body = shapes(W, H, [curve([(W / 2 - 160, 14), (W / 2, 22), (W / 2 + 160, 14)], 20) + curve([(W / 2 + 160, 42), (W / 2, 50), (W / 2 - 160, 42)], 20)], smooth=False)
    art = over(art, soft_shadow(body, "#12030a", 4, 0.35, 0, 4))
    art = FO(art, body, GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    lines = strokes(W, H, [(curve([(W / 2 - 150, 19), (W / 2, 27), (W / 2 + 150, 19)], 20), 1.0, None), (curve([(W / 2 - 150, 37), (W / 2, 45), (W / 2 + 150, 37)], 20), 1.0, None)])
    art = OV(art, lines, lambda q: rgba(np.ones(q.shape + (3,), np.float32) * col3(GOLD_D), q * 0.8))
    preview(art, "pp-ribbon", bg=IVORY)
    save(art, f"{OUT}/ribbon.webp", max_w=340, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
