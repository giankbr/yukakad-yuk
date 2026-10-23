"""Kolam Teratai — an original impressionist morning pond in broken-colour brushwork: hanging willow, a warm wooden
arched footbridge and its broken reflection, lily pads and pink lotus, sky light shimmering on the water.
Every surface is built from thousands of short, side-by-side dabs of pure colour (no blending), on a paper ground.
Run: python3 -I kolam-teratai.py [part ...]   parts: pond lotus pads dab. Assets -> public/themes/art/kolam-teratai/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h6_lib import *

OUT = outdir("kolam-teratai")
PARTS = sys.argv[1:] or ["pond", "lotus", "pads", "dab"]

SKY = ["#d7e4ef", "#e6dcef", "#f6e3cf", "#fbf2dc", "#cddcea", "#efe0e8"]
SUN = ["#fbe9b6", "#f9dca0", "#fff3d2", "#f6d6b0"]
FAR = ["#8fae9f", "#a3b9ae", "#a69dc6", "#7f9f98", "#b6c4b0", "#9a9fc4"]
WATER_HI = ["#cfe0ea", "#dcd2ea", "#f4dcc8", "#c4d8e4", "#e8e0d0", "#b9cfe0"]
WATER_LO = ["#6f9aa6", "#5f8a8c", "#7a8fb8", "#86a6a2", "#5c7f96", "#8b8fbf"]
PAD = ["#5f8f5a", "#78a463", "#4e7a52", "#94b56c", "#6a9a72", "#3f6b4c"]
PAD_HI = ["#b9d08a", "#d4dd9a", "#a7c98f"]
WILLOW = ["#7ea35a", "#9bba63", "#5f8a4e", "#b5c86f", "#4f7747", "#c9d27e"]
WOOD = ["#9a6a3e", "#b5814b", "#7a4f2e", "#c8955a", "#8c5e38"]
WOOD_HI = ["#e9c48a", "#f2d6a2", "#dcae70"]
LOTUS = ["#f2b8c6", "#f7cfd8", "#e48fa8", "#fbe3e8", "#d97b98"]


class Painter:
    def __init__(self, W, H, seed, ground="#f4efe4"):
        self.W, self.H = W, H
        self.cv = Canvas(W, H, seed)
        self.cv.c.clear(skia.Color4f(*hex_rgb(ground), 1.0) if ground else skia.ColorTRANSPARENT)
        self.rng = random.Random(seed)

    def dab(self, x, y, L, wd, a, col, al=0.9, soft=0.45):
        ca, sa = math.cos(a), math.sin(a)
        bend = self.rng.uniform(-0.22, 0.22) * L
        p0 = (x - ca * L / 2, y - sa * L / 2); p2 = (x + ca * L / 2, y + sa * L / 2)
        path = skia.Path(); path.moveTo(*p0); path.quadTo(x - sa * bend, y + ca * bend, *p2)
        paint = skia.Paint(AntiAlias=True, Color4f=color(col, al), Style=skia.Paint.kStroke_Style, StrokeWidth=wd, StrokeCap=skia.Paint.kRound_Cap)
        if soft:
            paint.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, soft))
        self.cv.c.drawPath(path, paint)

    def fill(self, mask, cols, step=6.0, L=(8, 14), wd=(3.5, 5.5), ang=0.0, ang_j=0.35, al=(0.75, 0.95), colfn=None, thr=0.5):
        r = self.rng
        H, W = mask.shape
        y = 0.0
        while y < H:
            x = (r.random() - 0.5) * step
            while x < W:
                xx, yy = x + r.uniform(-step * 0.5, step * 0.5), y + r.uniform(-step * 0.5, step * 0.5)
                ix, iy = int(min(W - 1, max(0, xx))), int(min(H - 1, max(0, yy)))
                if mask[iy, ix] > thr:
                    c = colfn(xx, yy, r) if colfn else cols[r.randrange(len(cols))]
                    a = (ang(xx, yy) if callable(ang) else ang) + r.uniform(-ang_j, ang_j)
                    self.dab(xx, yy, r.uniform(*L), r.uniform(*wd), a, c, r.uniform(*al))
                x += step
            y += step * 0.8

    def array(self):
        return self.cv.array()


def pick(r, cols):
    return cols[r.randrange(len(cols))]


def lilypad(W, H, cx, cy, rx, ry, notch):
    pts = []
    for i in range(40):
        t = notch + 0.18 + i / 39 * (math.tau - 0.36)
        pts.append((cx + math.cos(t) * rx, cy + math.sin(t) * ry))
    pts.append((cx, cy))
    return pts


def lotus_flower(p, x, y, s, r, open_=1.0):
    """Lotus head: fan of upright cupped petals built from dabs, warm core."""
    petals = [(-1.15, 0.85), (1.15, 0.85), (-0.75, 1.0), (0.75, 1.0), (-0.35, 1.12), (0.35, 1.12), (0.0, 1.2)]
    for k, (a, L) in enumerate(petals):
        ang = -math.pi / 2 + a * open_
        Lp = L * s
        for j in range(9):
            t = j / 8
            px = x + math.cos(ang) * Lp * t * 0.85
            py = y + math.sin(ang) * Lp * t * 0.85
            wdt = s * 0.2 * math.sin(math.pi * min(1, 0.15 + t * 0.9))
            for side in (-1, 1):
                ox = -math.sin(ang) * wdt * side * 0.8; oy = math.cos(ang) * wdt * side * 0.8
                col = pick(r, LOTUS[1:4]) if k < 4 else pick(r, LOTUS)
                if t > 0.75:
                    col = pick(r, ["#e48fa8", "#d97b98", "#f2b8c6"])
                p.dab(px + ox, py + oy, s * 0.26, s * 0.15, ang + r.uniform(-0.3, 0.3), col, r.uniform(0.8, 0.95))
    for _ in range(6):
        p.dab(x + r.uniform(-s * 0.12, s * 0.12), y - s * 0.12 + r.uniform(-3, 3), s * 0.12, s * 0.08, r.uniform(0, 3), pick(r, ["#f4d27a", "#f0c35a", "#fbe7a0"]), 0.95)


if "pond" in PARTS:
    W, H = 640, 1140
    rng = random.Random(91)
    p = Painter(W, H, 91)
    horizon = int(H * 0.40)
    ones = np.ones((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # sky: pale broken colour, warm sun glow upper right
    sky = (yy < horizon + 10).astype(np.float32)
    def skycol(x, y, r):
        d = math.hypot((x - W * 0.66) / W, (y - H * 0.12) / H * 1.6)
        return pick(r, SUN) if r.random() < max(0, 0.9 - d * 2.2) else pick(r, SKY)
    p.fill(sky, SKY, step=6, L=(9, 16), wd=(4, 6), ang=0.15, ang_j=0.4, colfn=skycol)
    # far trees across the pond (blue-green, lilac)
    far = ((yy > horizon - 120 - 40 * np.sin(xx / 70) - 30 * np.sin(xx / 23 + 1)) & (yy < horizon + 14)).astype(np.float32)
    p.fill(far, FAR, step=5, L=(7, 12), wd=(3, 5), ang=-1.45, ang_j=0.5)
    # water: light sky reflection in the middle, deeper blue-green towards the bottom and edges
    water = (yy >= horizon).astype(np.float32)
    def watercol(x, y, r):
        t = (y - horizon) / (H - horizon)
        edge = abs(x - W / 2) / (W / 2)
        deep = min(1, 0.25 + t * 0.6 + edge * 0.35)
        if y < horizon + 60 and r.random() < 0.7:
            return pick(r, FAR)
        if math.hypot((x - W * 0.66) / W, (y - horizon - 40) / H * 0.9) < 0.12 and r.random() < 0.6:
            return pick(r, SUN)
        return pick(r, WATER_LO) if r.random() < deep else pick(r, WATER_HI)
    p.fill(water, WATER_HI, step=6, L=(12, 22), wd=(3.5, 5.5), ang=0.0, ang_j=0.12, colfn=watercol)
    # bridge: arched deck + rails; reflection painted first (broken horizontal dabs)
    def arch_y(x, top, base):
        u = (x - W / 2) / (W * 0.62)
        return base - (base - top) * max(0, 1 - u * u)
    deck_top, deck_base = H * 0.315, H * 0.415
    deck = ((yy > np.vectorize(lambda x: arch_y(x, deck_top, deck_base))(xx[0])[None, :]) & (yy < np.vectorize(lambda x: arch_y(x, deck_top, deck_base) + 24)(xx[0])[None, :])).astype(np.float32)
    rail_top = np.vectorize(lambda x: arch_y(x, deck_top - 46, deck_base - 46))(xx[0])
    rail = (np.abs(yy - rail_top[None, :]) < 5).astype(np.float32)
    posts = np.zeros((H, W), np.float32)
    for x in range(10, W, 46):
        y0 = arch_y(x, deck_top - 46, deck_base - 46); y1 = arch_y(x, deck_top, deck_base)
        posts[int(y0):int(y1) + 2, max(0, x - 3):x + 4] = 1
    # piers into the water
    for x in (W * 0.16, W * 0.84):
        y1 = arch_y(x, deck_top, deck_base)
        posts[int(y1):int(horizon + 30), int(x - 6):int(x + 6)] = 1
    bridge = np.clip(deck + rail + posts, 0, 1)
    # reflection: mirror the bridge mask about the waterline, stretch & break it
    refl = np.zeros_like(bridge)
    wl = horizon + 30
    for y in range(int(wl), H):
        src = int(wl - (y - wl) * 0.9)
        if 0 <= src < H:
            refl[y] = np.roll(bridge[src], int(6 * math.sin(y / 5.0) + rng.uniform(-3, 3)))
    refl = gaussian_filter(refl, (1.5, 4)) * (yy < wl + 220) * np.clip(1 - (yy - wl) / 240, 0, 1)
    refl *= (fbm(W, H, 97, 18, 2) > 0.38)
    def reflcol(x, y, r):
        return pick(r, ["#6e5640", "#7f6a58", "#5f5a6e", "#8a7460", "#6d6a82"])
    p.fill(refl, WOOD, step=5, L=(12, 22), wd=(3, 4.5), ang=0.0, ang_j=0.1, al=(0.3, 0.55), colfn=reflcol, thr=0.25)
    def woodcol(x, y, r):
        lit = x > W * 0.45 and r.random() < 0.45
        return pick(r, WOOD_HI) if lit else pick(r, WOOD)
    p.fill(deck, WOOD, step=4, L=(8, 13), wd=(3, 4.5), ang=lambda x, y: math.atan2(-(2 * (x - W / 2) / (W * 0.62) ** 2) * (deck_top - deck_base) * -1, 1) * 0 + (0.0), ang_j=0.25, colfn=woodcol)
    p.fill(np.clip(rail + posts, 0, 1), WOOD, step=3.5, L=(5, 9), wd=(2.5, 3.5), ang=-1.57, ang_j=0.3, colfn=woodcol)
    # lily pads (perspective: smaller near the horizon), some with lotus
    pads = []
    for _ in range(46):
        y = rng.uniform(horizon + 70, H - 30)
        t = (y - horizon) / (H - horizon)
        x = rng.uniform(-40, W + 40)
        rx = 16 + 70 * t ** 1.3 + rng.uniform(-6, 6)
        pads.append((x, y, rx, rx * (0.22 + 0.2 * t), rng.uniform(0, math.tau)))
    pads.sort(key=lambda q: q[1])
    flowers = []
    for (x, y, rx, ry, notch) in pads:
        m = shape_mask(W, H, lilypad(W, H, x, y, rx, ry, notch), smooth=False)
        p.fill(m, PAD, step=max(3, rx / 9), L=(rx * 0.16, rx * 0.28), wd=(rx * 0.06 + 1.5, rx * 0.09 + 2), ang=0.0, ang_j=0.6)
        for _ in range(int(rx / 6)):
            a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
            p.dab(x + math.cos(a) * rx * 0.8, y + math.sin(a) * ry * 0.75, rx * 0.2, 2.2, a + math.pi / 2, pick(rng, PAD_HI), 0.85)
        if rng.random() < 0.3 and rx > 26:
            flowers.append((x + rng.uniform(-rx * 0.3, rx * 0.3), y - ry * 0.2, rx * 0.5))
    for x, y, s in flowers:
        lotus_flower(p, x, y, s, rng)
    # foreground standing lotus on tall stems (lower corners)
    for x, y, s, lean in [(70, H - 210, 62, 0.12), (W - 90, H - 260, 70, -0.1), (150, H - 120, 46, -0.05)]:
        for j in range(26):
            t = j / 25
            p.dab(x + lean * 200 * t, y + t * 230, 10, 4, 1.5, pick(rng, ["#6a8c4e", "#58794a", "#7fa05a"]), 0.9)
        lotus_flower(p, x, y, s, rng)
    # willow hanging from the top corners
    for side in (0, 1):
        for k in range(46):
            x0 = (rng.uniform(-30, 190) if side == 0 else rng.uniform(W - 190, W + 30))
            Lw = rng.uniform(H * 0.12, H * 0.38) * (1.0 if (x0 < 120 or x0 > W - 120) else 0.6)
            y = rng.uniform(-30, 20)
            x = x0
            while y < Lw:
                x += rng.uniform(-1.5, 1.5) + (0.4 if side == 0 else -0.4)
                p.dab(x, y, rng.uniform(8, 14), rng.uniform(2.4, 3.8), 1.45 + rng.uniform(-0.25, 0.25), pick(rng, WILLOW), rng.uniform(0.8, 0.95))
                y += rng.uniform(5, 8)
    # morning light glints on the water
    for _ in range(170):
        y = rng.uniform(horizon + 20, H * 0.75)
        x = W * 0.66 + rng.gauss(0, 60 + (y - horizon) * 0.25)
        p.dab(x, y, rng.uniform(6, 14), rng.uniform(2, 3), rng.uniform(-0.1, 0.1), pick(rng, ["#fff6dc", "#fbe7b0", "#ffffff"]), rng.uniform(0.7, 0.95))
    art = p.array()
    art = bristle(art, 93, 0.12)
    art = add_grain(art, 94, 0.03)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/kt-pond.png")
    save_rgb(art, f"{OUT}/pond.webp", size=(560, 998), quality=70)
    clear()

if "lotus" in PARTS:
    W, H = 340, 240
    rng = random.Random(92)
    p = Painter(W, H, 92, ground=None)
    m = shape_mask(W, H, lilypad(W, H, 170, 176, 150, 46, 4.4), smooth=False)
    p.fill(m, PAD, step=6, L=(12, 22), wd=(4, 6), ang=0.0, ang_j=0.6)
    for _ in range(20):
        a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
        p.dab(170 + math.cos(a) * 120, 176 + math.sin(a) * 36, 22, 2.6, a + math.pi / 2, pick(rng, PAD_HI), 0.85)
    lotus_flower(p, 170, 150, 110, rng)
    art = p.array()
    preview6(art, "kt-lotus")
    save(art, f"{OUT}/lotus.webp", max_w=220, quality=82)
    clear()

if "pads" in PARTS:
    # floating cluster of pads & lotus (band edges, closing)
    W, H = 1000, 260
    rng = random.Random(95)
    p = Painter(W, H, 95, ground=None)
    pads = [(rng.uniform(20, W - 20), rng.uniform(110, 220), 0, 0, 0) for _ in range(16)]
    out = []
    for x, y, *_ in pads:
        rx = rng.uniform(40, 86); out.append((x, y, rx, rx * 0.32, rng.uniform(0, math.tau)))
    out.sort(key=lambda q: q[1])
    for x, y, rx, ry, notch in out:
        m = shape_mask(W, H, lilypad(W, H, x, y, rx, ry, notch), smooth=False)
        p.fill(m, PAD, step=5, L=(rx * 0.16, rx * 0.28), wd=(4, 6), ang=0.0, ang_j=0.6)
        for _ in range(int(rx / 5)):
            a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
            p.dab(x + math.cos(a) * rx * 0.8, y + math.sin(a) * ry * 0.75, rx * 0.2, 2.4, a + math.pi / 2, pick(rng, PAD_HI), 0.85)
    for x, y, s in [(200, 140, 70), (520, 120, 82), (820, 150, 64)]:
        lotus_flower(p, x, y, s, rng)
    art = p.array()
    preview6(art, "kt-pads")
    save(art, f"{OUT}/pads.webp", max_w=760, quality=78)
    clear()

if "dab" in PARTS:
    # divider: a short horizontal run of broken-colour dabs, densest in the middle
    W, H = 420, 70
    rng = random.Random(96)
    p = Painter(W, H, 96, ground=None)
    for i in range(170):
        x = rng.gauss(W / 2, W * 0.2)
        if not 14 < x < W - 14:
            continue
        y = H / 2 + rng.gauss(0, 7) * (1 - abs(x - W / 2) / (W / 2))
        y = H / 2 + rng.gauss(0, 9) * (1 - abs(x - W / 2) / (W / 2))
        p.dab(x, y, rng.uniform(14, 24), rng.uniform(5, 7), rng.uniform(-0.25, 0.25), pick(rng, LOTUS[:3] + SUN[:2] + ["#a69dc6", "#8fae9f", "#7a8fb8"]), 0.9)
    art = p.array()
    preview6(art, "kt-dab")
    save(art, f"{OUT}/dab.webp", max_w=240, quality=84)
    clear()
