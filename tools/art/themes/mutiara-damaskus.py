"""Mutiara Damaskus — Damascene furniture: dark walnut inlaid with mother-of-pearl pieces (iridescent shell, each
piece cut separately with its own growth-line angle), bone strings and apricot-wood triangles; 12-point rosettes and
lozenge chains, plus soft blush damask roses (watercolour). No figures, no calligraphy.
Run: python3 -I mutiara-damaskus.py [part ...]   parts: walnut band rosette ring roses bud divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d3_lib import *  # noqa
import _j2_lib, _p1_lib
_j2_lib.PREV = PREV
_p1_lib.PREV = PREV
from _j2_lib import rose, leaf as wleaf, bud as wbud  # noqa

OUT = outdir("mutiara-damaskus")
PARTS = sys.argv[1:] or ["walnut", "band", "rosette", "ring", "roses", "bud", "divider"]
WAL, WAL_D = "#5e3a24", "#2b170d"
APR = "#b98458"
BONE = "#efe4cf"
BL, BL_M, BL_D = "#f4cfc4", "#e0a194", "#b56d64"
GR, GR_D = "#9cae8a", "#5d7357"


def inlay(base, pieces_mask, seed, apricot=None):
    """Lay labelled mother-of-pearl pieces (+ optional apricot-wood pieces) into a wood base."""
    lab, _ = label(pieces_mask > 0.5)
    art = over(base, pearl(np.clip(pieces_mask, 0, 1), seed=seed, pieces=lab))
    if apricot is not None:
        wood = walnut(*apricot.shape[::-1], seed=seed + 5, light="#c8956a", dark="#9a6a44", tile=False, figure=0.3)
        art = over(art, rgba(wood[..., :3], apricot))
    return art


def cut(m, lines):
    return np.clip(m - lines, 0, 1)


if "walnut" in PARTS:
    art = walnut(400, 400, seed=10101, light=WAL, dark=WAL_D)
    preview(art, "md-walnut")
    save_full(art, f"{OUT}/walnut.webp", quality=74)
    clear()

if "band" in PARTS:
    W, H = 240, 96
    bg = walnut(W, H, seed=10201, light=WAL, dark=WAL_D)
    cy = H / 2
    # bone strings top/bottom, dog-tooth pearl triangles, pearl lozenges alternating with apricot diamonds
    strings = fills(W, H, [[(0, 6), (W, 6), (W, 9), (0, 9)], [(0, H - 9), (W, H - 9), (W, H - 6), (0, H - 6)]])
    teeth = []
    for k in range(12):
        x = k * 20
        teeth.append([(x + 1.5, 12), (x + 18.5, 12), (x + 10, 22)])
        teeth.append([(x + 11.5, H - 12), (x + 28.5, H - 12), (x + 20, H - 22)])
        teeth.append([(x - 8.5, H - 12), (x + 8.5, H - 12), (x, H - 22)])
    loz = []
    apr = []
    for k in range(4):
        x = k * 60 + 30
        loz.append([(x - 24, cy), (x, cy - 19), (x + 24, cy), (x, cy + 19)])
        apr.append([(x - 30 + 30 - 6 - 24, cy), (x - 30 + 30 - 24 - 0, cy - 6), (x - 30 + 30 - 24 + 6, cy), (x - 24, cy + 6)])
    lozm = fills(W, H, loz)
    # each lozenge is cut into four pieces (separate shell cuts)
    sep = outline(W, H, [[(k * 60 + 30, cy - 20), (k * 60 + 30, cy + 20)] for k in range(4)] + [[(k * 60 + 5, cy), (k * 60 + 55, cy)] for k in range(4)], 1.4, closed=False)
    pm = np.maximum.reduce([cut(lozm, sep), fills(W, H, teeth)])
    am = fills(W, H, [[(k * 60 - 6, cy), (k * 60, cy - 8), (k * 60 + 6, cy), (k * 60, cy + 8)] for k in range(5)])
    art = over(bg, rgba(np.ones((H, W, 3), np.float32) * C(BONE), strings))
    art = inlay(art, pm, 10202, apricot=am)
    preview(art, "md-band")
    save_full(art, f"{OUT}/band.webp", size=(160, 64), quality=82)
    clear()

if "rosette" in PARTS:
    W = H = 560
    cx = cy = W / 2
    R = 270
    disc = fills(W, H, [ngon(cx, cy, R, 120)])
    base = rgba(walnut(W, H, seed=10301, light=WAL, dark=WAL_D, tile=False)[..., :3], disc)
    rim = np.clip(fills(W, H, [ngon(cx, cy, R - 6, 120)]) - fills(W, H, [ngon(cx, cy, R - 12, 120)]), 0, 1)
    rim2 = np.clip(fills(W, H, [ngon(cx, cy, 214, 120)]) - fills(W, H, [ngon(cx, cy, 208, 120)]), 0, 1)
    # outer ring of alternating pearl / apricot triangles between r 214 and r 258
    tri_p, tri_a = [], []
    n = 36
    for k in range(n):
        a0 = k * math.tau / n; a1 = (k + 1) * math.tau / n; am_ = (a0 + a1) / 2
        o = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
        tri_p.append([o(218, a0 + 0.01), o(218, a1 - 0.01), o(254, am_)])
        tri_a.append([o(254, a1 - 0.0), o(254, a1 + math.tau / n - 0.0), o(219, a1 + math.tau / n / 2)] if False else [o(252, am_ + 0.02), o(252, am_ + math.tau / n - 0.02), o(220, a1)])
    # 12-point star and kites
    star = starn(cx, cy, 196, 120, 12, -math.pi / 2)
    starm = fills(W, H, [star])
    inner = fills(W, H, [ngon(cx, cy, 104, 12, -math.pi / 2 + math.pi / 12)])
    lines = outline(W, H, [[(cx, cy), (cx + 196 * math.cos(-math.pi / 2 + k * math.pi / 6), cy + 196 * math.sin(-math.pi / 2 + k * math.pi / 6))] for k in range(12)] +
                    [[(cx, cy), (cx + 120 * math.cos(-math.pi / 2 + math.pi / 12 + k * math.pi / 6), cy + 120 * math.sin(-math.pi / 2 + math.pi / 12 + k * math.pi / 6))] for k in range(12)], 2.0, closed=False)
    ring_wood = np.clip(fills(W, H, [ngon(cx, cy, 110, 12, -math.pi / 2 + math.pi / 12)]) - inner, 0, 1)
    star_pieces = cut(np.clip(starm - fills(W, H, [ngon(cx, cy, 110, 12, -math.pi / 2 + math.pi / 12)]), 0, 1), lines)
    # centre: small 12-point star in pearl inside a bone ring, surrounded by apricot kites
    c_star = fills(W, H, [starn(cx, cy, 90, 56, 12, -math.pi / 2)])
    c_lines = outline(W, H, [[(cx, cy), (cx + 90 * math.cos(-math.pi / 2 + k * math.pi / 6), cy + 90 * math.sin(-math.pi / 2 + k * math.pi / 6))] for k in range(12)], 1.6, closed=False)
    core = fills(W, H, [ngon(cx, cy, 26, 12)])
    pieces = np.maximum.reduce([star_pieces, cut(c_star, c_lines) * (1 - fills(W, H, [ngon(cx, cy, 30, 12)])), core, fills(W, H, tri_p)])
    apr = np.maximum(fills(W, H, tri_a), np.clip(inner - c_star, 0, 1) * 0.0)
    art = over(base, rgba(np.ones((H, W, 3), np.float32) * C(BONE), np.maximum.reduce([rim, rim2, ring_wood])))
    art = inlay(art, pieces, 10302, apricot=fills(W, H, tri_a))
    # varnish: soft top-left light and slight shadow
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lit = 1 + 0.08 * np.clip(1 - np.hypot(xx - W * 0.35, yy - H * 0.3) / (W * 0.7), 0, 1)
    art[..., :3] *= lit[..., None]
    art = drop_shadow(art, blur=8, dy=6, strength=0.4)
    preview(art, "md-rosette", tone="#f3e8de")
    save(art, f"{OUT}/rosette.webp", max_w=400, quality=82)
    clear()

if "ring" in PARTS:
    # inlaid ring frame for round portraits: walnut annulus, bone strings, pearl segments alternating with apricot
    W = H = 560
    cx = cy = W / 2
    ro, ri = 276, 232
    ann = np.clip(fills(W, H, [ngon(cx, cy, ro, 160)]) - fills(W, H, [ngon(cx, cy, ri, 160)]), 0, 1)
    base = rgba(walnut(W, H, seed=10401, light=WAL, dark=WAL_D, tile=False)[..., :3], ann)
    strings = np.maximum(np.clip(fills(W, H, [ngon(cx, cy, ro - 5, 160)]) - fills(W, H, [ngon(cx, cy, ro - 9, 160)]), 0, 1),
                         np.clip(fills(W, H, [ngon(cx, cy, ri + 9, 160)]) - fills(W, H, [ngon(cx, cy, ri + 5, 160)]), 0, 1))
    segs, aprs = [], []
    n = 24
    o = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    for k in range(n):
        a = k * math.tau / n
        d = math.tau / n
        segs.append([o(254, a - d * 0.36), o(262, a), o(254, a + d * 0.36), o(246, a)])  # pearl lozenge along the ring
        aprs.append([o(254, a + d * 0.5 - 0.035), o(258, a + d * 0.5), o(254, a + d * 0.5 + 0.035), o(250, a + d * 0.5)])
    lozw = []
    for k in range(n):
        a = k * math.tau / n; d = math.tau / n
        lozw.append([o(254, a - d * 0.42), o(264, a), o(254, a + d * 0.42), o(244, a)])
    pm = fills(W, H, segs)
    # split each lozenge lengthwise (two shell cuts)
    sep = outline(W, H, [[o(254, k * math.tau / n - math.tau / n * 0.4), o(254, k * math.tau / n + math.tau / n * 0.4)] for k in range(n)], 1.2, closed=False)
    art = over(base, rgba(np.ones((H, W, 3), np.float32) * C(BONE), strings))
    art = inlay(art, cut(pm, sep), 10402, apricot=fills(W, H, aprs))
    art = drop_shadow(art, blur=8, dy=5, strength=0.4)
    preview(art, "md-ring", tone="#f3e8de")
    save(art, f"{OUT}/ring.webp", max_w=400, quality=82)
    clear()

if "roses" in PARTS:
    # soft damask-rose spray (watercolour, made a little denser so it holds on walnut too)
    W, H = 720, 520
    sd = Seq(10500)
    rng = random.Random(10500)
    art = blank(W, H)
    stems = [curve([(590, 205), (560, 250), (520, 290)], 20), curve([(140, 175), (170, 215), (205, 245)], 20), curve([(400, 175), (420, 230), (450, 280)], 20)]
    for st in stems:
        art = glaze(art, pigment(stroke_mask(W, H, st, 5), GR_D, seed=sd(), density=0.6, edge=0.3, bloom=0, rough=1.5, feather=0.8))
    RS = [(300, 330, 104), (470, 300, 86), (200, 250, 62)]
    for (ri_, a, L) in [(0, 2.3, 120), (0, 1.5, 110), (0, 2.9, 100), (1, 0.5, 120), (1, -0.2, 100), (1, 1.3, 96), (2, -2.6, 90), (2, 3.3, 86), (1, -1.0, 84)]:
        rx_, ry_, rr_ = RS[ri_]
        x, y = rx_ + math.cos(a) * rr_ * 0.55, ry_ + math.sin(a) * rr_ * 0.5
        lay, _ = wleaf(W, H, x, y, L, a, GR, GR_D, sd, rng, width=0.36)
        art = glaze(art, lay)
    for (x, y, r) in [(300, 330, 104), (470, 300, 86), (200, 250, 62)]:
        lay, m = rose(W, H, x, y, r, BL, BL_M, BL_D, sd, rng, petals=11)
        art = knockout(art, m, 0.95, 3)
        art = glaze(art, lay)
    for (x, y, s_, a) in [(590, 200, 22, -0.9), (140, 170, 20, -2.2), (400, 170, 18, -1.6)]:
        lay, m = wbud(W, H, x, y, s_, a, BL_M, BL_D, GR_D, sd, rng)
        art = glaze(art, lay)
    art[..., 3] = np.clip(art[..., 3] * 1.35, 0, 1)
    preview(art, "md-roses", tone="#f3e8de")
    preview(art, "md-roses-dark", bg=WAL)
    save(art, f"{OUT}/roses.webp", max_w=440, quality=80)
    clear()

if "bud" in PARTS:
    W, H = 220, 200
    sd = Seq(10600)
    rng = random.Random(10600)
    art = blank(W, H)
    for (x, y, L, a) in [(100, 110, 64, 2.5), (100, 110, 64, 0.6)]:
        lay, _ = wleaf(W, H, x, y, L, a, GR, GR_D, sd, rng, width=0.36)
        art = glaze(art, lay)
    lay, m = rose(W, H, 100, 100, 44, BL, BL_M, BL_D, sd, rng, petals=9)
    art = knockout(art, m, 0.95, 3)
    art = glaze(art, lay)
    art[..., 3] = np.clip(art[..., 3] * 1.3, 0, 1)
    preview(art, "md-bud", tone="#f3e8de")
    save(art, f"{OUT}/bud.webp", max_w=120, quality=84)
    clear()

if "divider" in PARTS:
    # small inlaid strip: long hexagon of walnut with three pearl lozenges and bone strings
    W, H = 440, 60
    cy = H / 2
    hexm = fills(W, H, [[(10, cy), (40, 8), (W - 40, 8), (W - 10, cy), (W - 40, H - 8), (40, H - 8)]])
    base = rgba(walnut(W, H, seed=10701, light=WAL, dark=WAL_D, tile=False)[..., :3], hexm)
    strings = np.clip(outline(W, H, [[(20, cy), (44, 12), (W - 44, 12), (W - 20, cy), (W - 44, H - 12), (44, H - 12)]], 1.8) * hexm, 0, 1)
    loz = [[(x - 30, cy), (x, cy - 13), (x + 30, cy), (x, cy + 13)] for x in (W / 2 - 80, W / 2, W / 2 + 80)]
    apr = [[(x - 7, cy), (x, cy - 7), (x + 7, cy), (x, cy + 7)] for x in (W / 2 - 40, W / 2 + 40, 70, W - 70)]
    sep = outline(W, H, [[(x, cy - 14), (x, cy + 14)] for x in (W / 2 - 80, W / 2, W / 2 + 80)], 1.2, closed=False)
    art = over(base, rgba(np.ones((H, W, 3), np.float32) * C(BONE), strings))
    art = inlay(art, cut(fills(W, H, loz), sep), 10702, apricot=fills(W, H, apr))
    art = drop_shadow(art, blur=3, dy=2, strength=0.35)
    preview(art, "md-divider", tone="#f3e8de")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)
    clear()

kb(OUT)
