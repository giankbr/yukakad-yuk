"""Ultah Panda — kids' birthday in a bamboo forest: original cute pandas (sitting with a bamboo stalk, peeking over a
ledge, a little face badge), a bamboo-wrapped birthday cake with candles, bamboo stalks and leaf sprigs.
Opaque gouache, picture-book style, soft greens + black/white.
Run: python3 -I ultah-panda.py [part ...]  parts: panda peek face cake grove sprig
Assets -> public/themes/art/ultah-panda/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n2_lib import *

OUT = outdir("ultah-panda")
PARTS = sys.argv[1:] or ["panda", "peek", "face", "cake", "grove", "sprig"]

INK, INK2 = "#25262a", "#34363b"
FUR, FUR_S = "#fbfaf4", "#d9dccf"
PINK = "#f3a7a4"
BAM, BAM_L, BAM_D, BAM_N = "#7fbf5a", "#a6d77a", "#4f9142", "#3d7a36"
LEAF, LEAF_L, LEAF_D = "#5faa4c", "#86c563", "#3b7f38"
CREAM, BERRY = "#fff5dc", "#e8585a"


def paint(art, m, c1, c2=None, nx=None, rough=1.4, streak=0.7):
    return GP(art, m, c1, c2 or c1, seed=nx(), rough=rough, streak=streak)


def shade(art, m, col, nx, k=0.35):
    return G(art, m, col, seed=nx(), density=k, edge=0.2, bloom=0.2, rough=2, feather=2.5)


def grid(W, H):
    return np.mgrid[0:H, 0:W].astype(np.float32)


def bamboo_stalk(art, W, H, x0, y0, x1, y1, wd, nx, rng, nodes=None, col=(BAM, BAM_L)):
    """A bamboo culm from (x0,y0) to (x1,y1): green body, lit stripe, node rings, little shadow under each node."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux
    body = shapes(W, H, [[(x0 + px * wd / 2, y0 + py * wd / 2), (x1 + px * wd / 2 * .9, y1 + py * wd / 2 * .9), (x1 - px * wd / 2 * .9, y1 - py * wd / 2 * .9), (x0 - px * wd / 2, y0 - py * wd / 2)]], smooth=False)
    art = paint(art, body, col[0], col[1], nx=nx, rough=1.2)
    yy, xx = grid(W, H)
    # across coordinate
    v = ((xx - x0) * px + (yy - y0) * py) / (wd / 2)
    art = shade(art, body * np.clip(v, 0, 1), BAM_D, nx, 0.55)
    hl = body * np.clip(1 - np.abs(v + 0.45) / 0.18, 0, 1)
    art = OV(art, hl, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#d8f0b4"), gaussian_filter(m, 1.2) * 0.7))
    n = nodes or max(2, int(L / (wd * 3.2)))
    items, sh = [], []
    for k in range(1, n + 1):
        t = k / (n + 0.6) + rng.uniform(-0.02, 0.02)
        cx, cy = x0 + ux * L * t, y0 + uy * L * t
        items.append(([(cx + px * wd * .56, cy + py * wd * .56), (cx - px * wd * .56, cy - py * wd * .56)], max(2.5, wd * 0.12), None))
        sh.append(([(cx + ux * wd * .16 + px * wd * .5, cy + uy * wd * .16 + py * wd * .5), (cx + ux * wd * .16 - px * wd * .5, cy + uy * wd * .16 - py * wd * .5)], max(2, wd * 0.12), None))
    art = shade(art, strokes(W, H, sh) * body, BAM_N, nx, 0.5)
    art = paint(art, strokes(W, H, items), BAM_N, BAM_D, nx=nx, rough=0.7)
    return art, [(x0 + ux * L * (k / (n + 0.6)), y0 + uy * L * (k / (n + 0.6))) for k in range(1, n + 1)]


def bleaf(art, W, H, x, y, L, ang, nx, rng, col=None):
    """Lance-shaped bamboo leaf with a midrib."""
    c1, c2 = col or (LEAF, LEAF_L)
    m = shapes(W, H, [deform(petal_pts(x, y, L, L * 0.2, ang, n=14, cup=rng.uniform(-0.15, 0.15)), rng, 1, 0.03)])
    art = paint(art, m, c1, c2, nx=nx, rough=1.0)
    half = shapes(W, H, [petal_pts(x, y, L * 0.96, L * 0.1, ang + 0.05, n=12)])
    art = shade(art, half * m, LEAF_D, nx, 0.4)
    rib = strokes(W, H, [([(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in np.linspace(0.05, 0.85, 8)], max(1.0, L * 0.02), (0.0, 0.6))])
    return G(art, rib * m, LEAF_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.5)


def leaf_fan(art, W, H, x, y, ang, n, L, nx, rng, spread=1.1):
    for k in range(n):
        a = ang + (k - (n - 1) / 2) / max(1, n - 1) * spread + rng.gauss(0, 0.06)
        art = bleaf(art, W, H, x, y, L * rng.uniform(0.8, 1.1), a, nx, rng, col=(LEAF, LEAF_L) if k % 2 else (BAM, LEAF_L))
    return art


def eyes(art, W, H, cx, cy, s, nx, look=(0, 0), closed=False):
    """Black slanted eye patches + shiny eyes."""
    for side in (-1, 1):
        patch = shapes(W, H, [ellipse_pts(cx + side * s * 0.36, cy + s * 0.02, s * 0.22, s * 0.3, 16, side * -0.55)])
        art = paint(art, patch, INK, INK2, nx=nx, rough=0.8)
    if closed:
        arcs = strokes(W, H, [(arc_pts(cx + side * s * 0.34, cy + s * 0.0, s * 0.1, math.pi + 0.3, math.tau - 0.3, 10), max(2, s * 0.04), (0.1, 0.1)) for side in (-1, 1)])
        return paint(art, arcs, FUR, nx=nx, rough=0.3)
    wh = circles(W, H, [(cx + side * s * 0.34 + look[0] * s * .04, cy + s * 0.0 + look[1] * s * .04, s * 0.1) for side in (-1, 1)])
    art = paint(art, wh, FUR, nx=nx, rough=0.3, streak=0.1)
    pu = circles(W, H, [(cx + side * s * 0.34 + look[0] * s * .07, cy + s * 0.015 + look[1] * s * .07, s * 0.065) for side in (-1, 1)])
    art = paint(art, pu, "#121215", nx=nx, rough=0.3, streak=0.1)
    gl = circles(W, H, [(cx + side * s * 0.34 - s * 0.03, cy - s * 0.03, s * 0.026) for side in (-1, 1)])
    return OV(art, gl, lambda m: rgba(np.ones(m.shape + (3,), np.float32), m))


def panda_head(art, W, H, cx, cy, s, nx, rng, look=(0, 0), closed=False, tilt=0.0):
    """Round panda head with ears, eye patches, nose, smile and cheeks. s = head radius."""
    ears = circles(W, H, [(cx - s * 0.74, cy - s * 0.68, s * 0.32), (cx + s * 0.74, cy - s * 0.68, s * 0.32)])
    art = paint(art, ears, INK, INK2, nx=nx, rough=1.0)
    head = shapes(W, H, [deform(ellipse_pts(cx, cy, s * 1.04, s * 0.92, 24, tilt), rng, 1, 0.015)])
    art = paint(art, head, FUR, "#ffffff", nx=nx, rough=1.2)
    yy, xx = grid(W, H)
    art = shade(art, head * np.clip((yy - cy - s * 0.2) / (s * 0.7), 0, 1), FUR_S, nx, 0.55)
    art = shade(art, head * np.clip((xx - cx - s * 0.4) / (s * 0.6), 0, 1), FUR_S, nx, 0.4)
    art = eyes(art, W, H, cx, cy, s, nx, look, closed)
    muzzle = shapes(W, H, [ellipse_pts(cx, cy + s * 0.36, s * 0.3, s * 0.2, 16)])
    art = shade(art, muzzle, "#efe9da", nx, 0.5)
    nose = shapes(W, H, [ellipse_pts(cx, cy + s * 0.27, s * 0.1, s * 0.065, 12)])
    art = paint(art, nose, INK, nx=nx, rough=0.4)
    mouth = strokes(W, H, [(arc_pts(cx - s * 0.07, cy + s * 0.36, s * 0.07, 0.2, math.pi - 0.3, 10), max(1.6, s * 0.03), (0.2, 0.2)),
                           (arc_pts(cx + s * 0.07, cy + s * 0.36, s * 0.07, 0.3, math.pi - 0.2, 10), max(1.6, s * 0.03), (0.2, 0.2))])
    art = paint(art, mouth, INK, nx=nx, rough=0.3)
    ch = circles(W, H, [(cx - s * 0.58, cy + s * 0.32, s * 0.12), (cx + s * 0.58, cy + s * 0.32, s * 0.12)])
    art = G(art, ch, PINK, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=2)
    return art


def panda():
    """Cover panda: sitting, hugging a bamboo stalk, a leaf sprig in one paw."""
    W, H = 520, 600
    nx = Seq(100)
    rng = random.Random(7)
    art = blank(W, H)
    # bamboo stalk behind the panda (it hugs it)
    art, nodes = bamboo_stalk(art, W, H, 336, 590, 372, 20, 44, nx, rng, nodes=5)
    art = leaf_fan(art, W, H, 370, 60, -2.4, 3, 96, nx, rng, spread=0.9)
    art = leaf_fan(art, W, H, nodes[2][0] + 18, nodes[2][1], -0.4, 3, 84, nx, rng, spread=0.8)
    # body
    body = shapes(W, H, [deform(ellipse_pts(240, 420, 170, 150, 24), rng, 1, 0.015)])
    art = paint(art, body, FUR, "#ffffff", nx=nx)
    yy, xx = grid(W, H)
    art = shade(art, body * np.clip((yy - 430) / 120, 0, 1), FUR_S, nx, 0.55)
    # black shoulder band + arms (one arm round the stalk)
    band = shapes(W, H, [[(90, 360), (150, 300), (330, 300), (392, 352), (380, 400), (310, 360), (170, 360), (100, 410)]])
    art = paint(art, band, INK, INK2, nx=nx, rough=1.0)
    arm_r = shapes(W, H, [[(320, 330), (382, 330), (406, 372), (390, 420), (352, 424), (330, 392)]])
    art = paint(art, arm_r, INK, INK2, nx=nx, rough=1.0)
    arm_l = shapes(W, H, [[(100, 370), (150, 360), (186, 420), (176, 468), (136, 476), (104, 440)]])
    art = paint(art, arm_l, INK, INK2, nx=nx, rough=1.0)
    # legs
    legs = shapes(W, H, [ellipse_pts(150, 540, 74, 52, 20, -0.25), ellipse_pts(330, 540, 74, 52, 20, 0.25)])
    art = paint(art, legs, INK, INK2, nx=nx, rough=1.0)
    pads = shapes(W, H, [ellipse_pts(126, 548, 30, 24, 14, -0.3), ellipse_pts(354, 548, 30, 24, 14, 0.3)])
    art = paint(art, pads, "#4a4b50", nx=nx, rough=0.6)
    toes = circles(W, H, [(x + dx, y + dy, 7) for x, y in ((126, 548), (354, 548)) for dx, dy in ((-18, -26), (0, -32), (18, -26))])
    art = paint(art, toes, "#4a4b50", nx=nx, rough=0.4)
    beans = circles(W, H, [(126, 552, 12), (354, 552, 12)])
    art = paint(art, beans, PINK, nx=nx, rough=0.4)
    # a little leaf sprig held in the left paw
    art = bleaf(art, W, H, 160, 452, 78, -2.5, nx, rng)
    art = bleaf(art, W, H, 160, 452, 66, -1.9, nx, rng, col=(BAM, LEAF_L))
    paw = shapes(W, H, [ellipse_pts(158, 456, 30, 24, 14)])
    art = paint(art, paw, INK, INK2, nx=nx, rough=0.6)
    # head
    art = panda_head(art, W, H, 236, 210, 132, nx, rng, look=(0.3, -0.2), tilt=-0.06)
    preview(art, "up-panda", bg="#dff0d0")
    save(art, f"{OUT}/panda.webp", max_w=360, quality=84)


def peek():
    """Panda head and paws peeking over a ledge (sits on top of cards/frames)."""
    W, H = 400, 250
    nx = Seq(200)
    rng = random.Random(3)
    art = blank(W, H)
    art = panda_head(art, W, H, 200, 140, 100, nx, rng, look=(-0.2, 0.3))
    yy, xx = grid(W, H)
    art[..., 3] *= (yy < 214)
    paws = shapes(W, H, [ellipse_pts(110, 214, 46, 30, 16), ellipse_pts(290, 214, 46, 30, 16)])
    art = paint(art, paws, INK, INK2, nx=nx, rough=0.8)
    toes = strokes(W, H, [([(x + dx, 196), (x + dx, 214)], 2.2, None) for x in (110, 290) for dx in (-14, 0, 14)])
    art = G(art, toes * paws, "#5a5b60", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.4, feather=0.5)
    preview(art, "up-peek", bg="#dff0d0")
    save(art, f"{OUT}/peek.webp", max_w=220, quality=84)


def face():
    W, H = 260, 240
    nx = Seq(300)
    rng = random.Random(11)
    art = blank(W, H)
    art = panda_head(art, W, H, 130, 136, 86, nx, rng, closed=True)
    preview(art, "up-face", bg="#dff0d0")
    save(art, f"{OUT}/face.webp", max_w=120, quality=86)


def cake():
    """Two-tier cake wrapped like bamboo culms, cream frosting drips, candles, leaf topper and berries."""
    W, H = 460, 520
    nx = Seq(400)
    rng = random.Random(5)
    art = blank(W, H)
    yy, xx = grid(W, H)
    plate = shapes(W, H, [ellipse_pts(230, 486, 200, 24, 24)])
    art = paint(art, plate, "#f4efe2", nx=nx)
    art = shade(art, plate * (yy > 486), "#c9c6b4", nx, 0.6)

    def tier(art, cx, top, bot, rw, ry):
        # a row of vertical bamboo slats wraps the tier
        side = shapes(W, H, [[(cx - rw, top), (cx + rw, top), (cx + rw, bot)] + arc_pts(cx, bot, rw, 0, math.pi, 30, ry / rw) + [(cx - rw, top)]], smooth=False)
        art = paint(art, side, BAM, BAM_L, nx=nx)
        n = 9
        for k in range(n):
            t = (k + 0.5) / n
            a = math.pi * (1 - t)
            x = cx + math.cos(a) * rw
            wslat = rw * 2 / n * math.sin(a) * 0.98 + 2
            v = math.cos(a)
            slat = shapes(W, H, [[(x - wslat / 2, top), (x + wslat / 2, top), (x + wslat / 2, bot + math.sin(a) * ry), (x - wslat / 2, bot + math.sin(a) * ry)]], smooth=False) * side
            art = G(art, slat, BAM_D if v > 0 else BAM_L, seed=nx(), density=0.15 + 0.25 * abs(v), edge=0.6, bloom=0, rough=0.8, feather=0.6)
            ny = top + (bot - top) * 0.55
            node = strokes(W, H, [([(x - wslat / 2, ny + math.sin(a) * ry * .5), (x + wslat / 2, ny + math.sin(a) * ry * .5)], 3, None)]) * side
            art = paint(art, node, BAM_N, nx=nx, rough=0.4)
        art = shade(art, side * np.clip((xx - cx) / rw, 0, 1), BAM_D, nx, 0.4)
        # frosting top + drips
        topm = shapes(W, H, [ellipse_pts(cx, top, rw + 4, ry, 30)])
        drips = []
        for k in range(10):
            a = math.pi * (k + 0.5) / 10
            dx = cx + math.cos(a) * (rw + 2)
            dy = top + math.sin(a) * ry
            L = rng.uniform(10, 34) * math.sin(a)
            drips.append(([(dx, dy - 4), (dx, dy + L)], rng.uniform(10, 16), (0.0, 0.0)))
        frost = np.maximum(topm, strokes(W, H, drips))
        art = paint(art, frost, CREAM, "#ffffff", nx=nx, rough=0.8)
        art = shade(art, frost * np.clip((yy - top) / 30, 0, 1) * np.clip((xx - cx) / rw + 0.4, 0, 1), "#e7d8b4", nx, 0.4)
        return art

    art = tier(art, 230, 330, 470, 170, 26)
    art = tier(art, 230, 200, 318, 118, 20)
    # candles
    for x, h in ((186, 74), (230, 92), (274, 74)):
        c = shapes(W, H, [[(x - 8, 196 - h), (x + 8, 196 - h), (x + 8, 200), (x - 8, 200)]], smooth=False)
        art = paint(art, c, "#ffffff", nx=nx, rough=0.5)
        stripes = c * (np.abs(((yy - xx * 0.6) / 14) % 1 - 0.5) < 0.18)
        art = paint(art, stripes, BAM if x != 230 else BERRY, nx=nx, rough=0.4)
        fl = shapes(W, H, [petal_pts(x, 190 - h, 26, 12, -math.pi / 2, n=14)])
        art = over(art, glow(fl, "#ffd26a", radius=10, strength=0.5))
        art = paint(art, fl, "#ffb43a", "#ffd56a", nx=nx, rough=0.4)
        inner = shapes(W, H, [petal_pts(x, 191 - h, 13, 6, -math.pi / 2, n=12)])
        art = paint(art, inner, "#fff2b8", nx=nx, rough=0.3)
    # leaf topper + berries on the frosting
    art = leaf_fan(art, W, H, 150, 206, -2.6, 3, 52, nx, rng, spread=0.8)
    art = leaf_fan(art, W, H, 318, 210, -0.5, 3, 52, nx, rng, spread=0.8)
    ber = circles(W, H, [(150, 212, 12), (166, 222, 10), (316, 216, 12), (300, 226, 10), (100, 344, 11), (360, 346, 11), (230, 352, 12)])
    art = paint(art, ber, BERRY, "#f07070", nx=nx, rough=0.5)
    gl = circles(W, H, [(x - 4, y - 4, 3) for x, y, _ in [(150, 212, 0), (166, 222, 0), (316, 216, 0), (300, 226, 0), (100, 344, 0), (360, 346, 0), (230, 352, 0)]])
    art = OV(art, gl, lambda m: rgba(np.ones(m.shape + (3,), np.float32), m * 0.8))
    preview(art, "up-cake", bg="#dff0d0")
    save(art, f"{OUT}/cake.webp", max_w=300, quality=84)


def grove():
    """Seamless vertical tile of three bamboo culms with leaf fans (cover side frames, repeat-y; mirrored on the right).
    Painted three tiles tall, then the middle third is cut out so the culms run straight through the seams."""
    W, T = 300, 900
    H = T * 3
    nx = Seq(500)
    rng = random.Random(9)
    art = blank(W, H)
    for (x0, wd, col) in [(222, 30, ("#9bcf74", "#b9e092")), (56, 46, (BAM, BAM_L)), (124, 38, ("#6fb251", BAM_L))]:
        art, nodes = bamboo_stalk(art, W, H, x0, H + 20, x0 + 0.01, -20, wd, nx, rng, nodes=int(H / 150))
        for i, (nx_, ny_) in enumerate(nodes):
            if not (T + 120 < ny_ < 2 * T - 120) or i % 2:
                continue
            side = 1 if (i // 2 + int(x0)) % 2 else -1
            art = leaf_fan(art, W, H, nx_ + side * wd * 0.4, ny_, (0.2 if side > 0 else math.pi - 0.2) + rng.uniform(-.2, .3), 3, rng.uniform(70, 96), nx, rng, spread=0.9)
        clear()
    tile = art[T:2 * T].copy()
    preview(tile, "up-grove", bg="#e7f4dc")
    save_full(tile, f"{OUT}/grove.webp", size=(200, 600), quality=80)


def sprig():
    W, H = 520, 110
    nx = Seq(600)
    rng = random.Random(13)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(60, 70), (200, 58), (330, 60), (460, 52)], 30), 5, (0.05, 0.4))])
    art = paint(art, stem, BAM_D, BAM, nx=nx, rough=0.6)
    for (x, y, a, L) in [(120, 66, -2.7, 70), (120, 66, 2.7, 64), (250, 60, -0.5, 80), (250, 60, 0.45, 72), (250, 60, -0.05, 90), (380, 57, -2.6, 64), (380, 57, 2.75, 60), (456, 52, -0.25, 54)]:
        art = bleaf(art, W, H, x, y, L, a, nx, rng, col=(LEAF, LEAF_L) if L > 66 else (BAM, LEAF_L))
    preview(art, "up-sprig", bg="#fff8e6")
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
kb_total(OUT)
