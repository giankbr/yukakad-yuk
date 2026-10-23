"""Memphis 80an — an original Memphis-style still life in screen-printed gouache: pastel solids with black ink outlines,
hard offset shadows, squiggle/dot/stripe fills; plus a black squiggle divider, a zigzag strip, confetti tile and small
sticker shapes. Run: python3 -I memphis-80an.py [part ...]  parts: totem squig zig confetti tri half ring bolt
Assets -> public/themes/art/memphis-80an/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i4_lib import *  # noqa

OUT = outdir("memphis-80an")
PARTS = sys.argv[1:] or ["totem", "squig", "zig", "confetti", "tri", "half", "ring", "bolt"]
PINK, MINT, LILAC, YEL, CORAL, COBALT, INK, WHITE = "#f7a8c4", "#8fdcc2", "#b9a5ef", "#ffd54a", "#ff7a59", "#3b5bd6", "#151515", "#fffdf8"


def outline(m, w):
    d = distance_transform_edt(m < 0.5)
    return np.clip(w + 0.5 - d, 0, 1) * (d > 0)


def shift(m, dx, dy):
    return np.roll(np.roll(m, dy, 0), dx, 1)


def dots(W, H, sp, r, ox=0, oy=0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fx = ((xx - ox) % sp) - sp / 2; fy = ((yy - oy) % sp) - sp / 2
    return np.clip(r + 0.5 - np.hypot(fx, fy), 0, 1)


def stripes(W, H, ang, sp, duty):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx * math.cos(ang) + yy * math.sin(ang)) / sp
    f = np.abs((u % 1) - 0.5) * 2
    return np.clip((duty - f) * sp / 2 + 0.5, 0, 1)


def squiggles(W, H, rng, n, L, width, box=None):
    x0, y0, x1, y1 = box or (0, 0, W, H)
    items = []
    cols = max(1, int(round(math.sqrt(n * (x1 - x0) / (y1 - y0)))))
    rows = max(1, n // cols)
    for i in range(cols * rows):
        gx, gy = i % cols, i // cols
        x = x0 + (gx + rng.uniform(0.15, 0.85)) * (x1 - x0) / cols
        y = y0 + (gy + rng.uniform(0.15, 0.85)) * (y1 - y0) / rows
        a = rng.uniform(0, math.tau); amp = rng.uniform(3, 6); k = rng.uniform(0.3, 0.5)
        pts = [(x + math.cos(a) * t - math.sin(a) * amp * math.sin(t * k), y + math.sin(a) * t + math.cos(a) * amp * math.sin(t * k)) for t in np.linspace(0, L * rng.uniform(.7, 1.2), 24)]
        items.append((pts, width, (0.2, 0.2)))
    return strokes(W, H, items)


def solid(art, m, col, col2, nx, pattern=None, pat_col=INK, sh=(9, 9), ow=3.5):
    if sh:
        art = LC(art, shift(m, *sh) * (1 - m), INK, seed=nx(), wear=0.15, rough=1.0)
    art = GP(art, m, col, col2 or col, seed=nx(), rough=1.2, streak=0.35)
    if pattern is not None:
        art = LC(art, pattern * m, pat_col, seed=nx(), wear=0.3, rough=0.8)
    art = LC(art, outline(m, ow), INK, seed=nx(), wear=0.12, rough=0.8)
    return art


if "totem" in PARTS:
    W, H = 640, 760
    nx = Seq(100); rng = random.Random(7)
    art = blank(W, H)
    # floating black squiggle (back)
    sq = [(60 + t, 120 + 22 * math.sin(t / 26)) for t in np.linspace(0, 230, 90)]
    art = LC(art, shift(strokes(W, H, [(sq, 13, (0.05, 0.05))]), 8, 8), PINK, seed=nx(), wear=0.1)
    art = LC(art, strokes(W, H, [(sq, 13, (0.05, 0.05))]), INK, seed=nx(), wear=0.12)
    # slab: checker front + lilac top
    front = shapes(W, H, [[(70, 640), (470, 640), (470, 712), (70, 712)]], smooth=False)
    top = shapes(W, H, [[(70, 640), (130, 600), (530, 600), (470, 640)]], smooth=False)
    side = shapes(W, H, [[(470, 640), (530, 600), (530, 672), (470, 712)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    chk = (((xx // 24) + (yy // 24)) % 2).astype(np.float32)
    art = LC(art, shift(np.clip(front + side, 0, 1), 10, 10) * (1 - front - side - top), INK, seed=nx(), wear=0.15)
    art = GP(art, front, WHITE, seed=nx(), rough=1, streak=0.2)
    art = LC(art, chk * front, INK, seed=nx(), wear=0.25)
    art = solid(art, top, LILAC, "#a995e6", nx, None, sh=None)
    art = solid(art, side, "#6f5bc0", None, nx, stripes(W, H, 0.6, 12, 0.3) * 0, sh=None)
    art = LC(art, outline(front, 3.5), INK, seed=nx(), wear=0.1)
    # coral cone with dots, left
    cone = shapes(W, H, [[(46, 600), (176, 600), (112, 404)]], smooth=False)
    art = solid(art, cone, CORAL, "#f26a4a", nx, dots(W, H, 13, 3.0), INK)
    # pink column with squiggle fill
    col = shapes(W, H, [[(186, 330), (316, 330), (316, 606), (186, 606)]], smooth=False)
    col = np.clip(col + ellipses(W, H, [(251, 606, 65, 16, 0)]), 0, 1)
    art = solid(art, col, PINK, "#f498b8", nx, squiggles(W, H, rng, 22, 30, 3.4, (176, 330, 316, 610)))
    ctop = ellipses(W, H, [(251, 330, 65, 16, 0)])
    art = solid(art, ctop, "#fbd0df", None, nx, None, sh=None, ow=3)
    # yellow half disc balancing on the column, tilted
    hd = []
    cx, cy, R, tl = 262, 318, 150, -0.22
    for a in np.linspace(math.pi, math.tau, 60):
        x, y = math.cos(a) * R, math.sin(a) * R
        hd.append((cx + x * math.cos(tl) - y * math.sin(tl), cy + x * math.sin(tl) + y * math.cos(tl)))
    half = shapes(W, H, [hd], smooth=False)
    art = solid(art, half, YEL, "#ffc93a", nx, stripes(W, H, tl + math.pi / 2, 18, 0.28))
    # lilac zigzag bolt springing out to the right
    zz = [(396, 196), (446, 150), (470, 210), (522, 160), (548, 226), (600, 176)]
    bolt = strokes(W, H, [(zz, 22, None)], cap=False)
    art = solid(art, bolt, LILAC, None, nx, None, ow=3)
    # mint sphere with halftone shade on the slab
    sp = disc(W, H, 420, 528, 74)
    art = solid(art, sp, MINT, "#7fd2b6", nx, None, sh=(10, 6))
    shade_f = np.clip((np.hypot(xx - 392, yy - 500) - 40) / 70, 0, 1)
    hal = dots(W, H, 9, 1) * 0
    for k, r in enumerate((1.0, 1.8, 2.6, 3.2)):
        band = (shade_f > k * 0.25) & (shade_f <= (k + 1) * 0.25 + 0.001)
        hal = np.maximum(hal, dots(W, H, 9, r) * band)
    art = LC(art, hal * sp * 0.85, "#2c7f68", seed=nx(), wear=0.2)
    art = LC(art, outline(sp, 3.5), INK, seed=nx(), wear=0.1)
    # small cobalt ring + confetti dashes around
    ring = ring_mask(W, H, 560, 420, 20, 34)
    art = solid(art, ring, COBALT, None, nx, None, sh=(6, 6), ow=3)
    for x, y, a, c in [(560, 320, 0.6, PINK), (40, 300, -0.4, MINT), (600, 560, 1.2, YEL), (60, 470, 0.9, LILAC), (330, 70, -0.8, CORAL), (460, 320, 0.2, MINT)]:
        m = strokes(W, H, [([(x - math.cos(a) * 16, y - math.sin(a) * 16), (x + math.cos(a) * 16, y + math.sin(a) * 16)], 9, None)])
        art = solid(art, m, c, None, nx, None, sh=(4, 4), ow=2.5)
    for x, y in [(520, 90), (130, 210), (590, 640), (30, 380)]:
        art = LC(art, disc(W, H, x, y, 6), INK, seed=nx(), wear=0.1)
    save(art, f"{OUT}/totem.webp", quality=84)
    prev(art, "mp-totem", "#fff6ea")
    clear()

if "squig" in PARTS:
    W, H = 400, 60
    nx = Seq(200)
    pts = [(14 + t, 30 + 13 * math.sin(t / 15)) for t in np.linspace(0, 372, 160)]
    m = strokes(W, H, [(pts, 6.5, (0.04, 0.04))])
    art = LC(blank(W, H), shift(m, 4, 4), PINK, seed=nx(), wear=0.1)
    art = LC(art, m, INK, seed=nx(), wear=0.12)
    save(art, f"{OUT}/squig.webp", quality=84)
    prev(art, "mp-squig", "#fff6ea")

if "zig" in PARTS:
    W, H = 400, 56
    nx = Seq(300)
    pts = [(10 + i * 19, 16 if i % 2 else 40) for i in range(21)]
    m = strokes(W, H, [(pts, 9, None)], cap=False)
    art = LC(blank(W, H), shift(m, 4, 4), INK, seed=nx(), wear=0.1)
    art = GP(art, m, MINT, seed=nx(), rough=0.8)
    art = LC(art, outline(m, 2.2), INK, seed=nx(), wear=0.1)
    save(art, f"{OUT}/zig.webp", quality=84)
    prev(art, "mp-zig", "#fff6ea")

if "confetti" in PARTS:
    W, H = 360, 360
    nx = Seq(400); rng = random.Random(41)
    art = blank(W, H)
    cols = [PINK, MINT, LILAC, YEL, CORAL, INK, INK]
    for i in range(34):
        x, y = rng.uniform(10, W - 10), rng.uniform(10, H - 10)
        kind = rng.choice(["dash", "dash", "tri", "dot", "ring"])
        c = rng.choice(cols)
        a = rng.uniform(0, math.tau)
        if kind == "dash":
            L = rng.uniform(8, 14)
            m = strokes(W, H, [([(x - math.cos(a) * L, y - math.sin(a) * L), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(4.5, 6.5), None)])
        elif kind == "tri":
            r = rng.uniform(7, 11)
            m = shapes(W, H, [[(x + math.cos(a + k * math.tau / 3) * r, y + math.sin(a + k * math.tau / 3) * r) for k in range(3)]], smooth=False)
        elif kind == "dot":
            m = disc(W, H, x, y, rng.uniform(3, 5))
        else:
            m = ring_mask(W, H, x, y, 4, 7.5)
        art = (LC if c == INK else GP)(art, m, c, seed=nx(), **({"wear": 0.15} if c == INK else {"rough": 0.8}))
    save_full(art, f"{OUT}/confetti.webp", quality=80)
    prev(art, "mp-confetti", "#fff6ea")
    clear()


def sticker(name, build, W=200, H=200, nxs=500):
    nx = Seq(nxs)
    art = build(blank(W, H), nx)
    save(art, f"{OUT}/{name}.webp", quality=84)
    prev(art, f"mp-{name}", "#fff6ea")


if "tri" in PARTS:
    def b(art, nx):
        m = shapes(200, 200, [[(20, 170), (172, 170), (110, 22)]], smooth=False)
        return solid(art, m, CORAL, None, nx, dots(200, 200, 12, 2.8), INK, sh=(8, 8))
    sticker("tri", b, nxs=500)

if "half" in PARTS:
    def b(art, nx):
        hd = [(100 + math.cos(a) * 84, 140 + math.sin(a) * 84) for a in np.linspace(math.pi, math.tau, 50)]
        m = shapes(200, 200, [hd], smooth=False)
        return solid(art, m, YEL, None, nx, stripes(200, 200, math.pi / 2, 16, 0.3), INK, sh=(8, 8))
    sticker("half", b, nxs=600)

if "ring" in PARTS:
    def b(art, nx):
        m = ring_mask(200, 200, 96, 96, 40, 72)
        rng = random.Random(3)
        return solid(art, m, LILAC, None, nx, squiggles(200, 200, rng, 26, 24, 3), INK, sh=(8, 8))
    sticker("ring", b, nxs=700)

if "bolt" in PARTS:
    def b(art, nx):
        zz = [(16, 120), (66, 50), (96, 128), (146, 58), (184, 120)]
        m = strokes(200, 170, [(zz, 24, None)], cap=False)
        return solid(art, m, MINT, None, nx, None, sh=(7, 7))
    sticker("bolt", b, 200, 170, nxs=800)
