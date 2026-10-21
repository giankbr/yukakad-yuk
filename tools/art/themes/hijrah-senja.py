"""Hijrah Senja — Islamic wedding at dusk in the desert: painted apricot-to-plum sky with a crescent moon, layered dunes
with warm rim light, a tiny camel caravan on a far ridge, brass lanterns with glow, brass crescent divider, sand tile.
Run: python3 -I hijrah-senja.py [part ...]  parts: scene dunes lantern divider sand"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a4_lib import *

OUT = outdir("hijrah-senja")
PARTS = sys.argv[1:] or ["scene", "dunes", "lantern", "divider", "sand"]
BRASS, BRASS_L, BRASS_D = "#b9873a", "#f0cd8a", "#6e4a1c"


def crest(W, y0, amp, seed, n_peaks=2.2, sharp=1.6):
    """Dune crest polyline: asymmetric (gentle windward, steep slip face)."""
    rng = random.Random(seed)
    ph = [rng.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for x in range(-20, W + 21, 6):
        u = x / W * n_peaks * math.tau + ph[0]
        s = math.sin(u) + 0.35 * math.sin(2 * u + ph[1])
        s = (s + 1.4) / 2.8
        s = s ** sharp
        y = y0 - amp * s - amp * 0.18 * math.sin(x / W * 5.3 + ph[2])
        pts.append((x, y))
    return pts


def dune_layer(art, W, H, pts, top, bot, lit, seed, ripples=0.0, dd=0.2):
    poly = pts + [(W + 20, H + 20), (-20, H + 20)]
    m = shapes(W, H, [poly], smooth=False)
    y_crest = np.interp(np.arange(W), [p[0] for p in pts], [p[1] for p in pts]).astype(np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None]
    depth = np.clip((yy - y_crest[None, :]) / (H * dd), 0, 1)
    rgb = lerp3(top, bot, depth ** 0.7)
    # slope lighting: faces turned to the low sun (to the left) catch a warm rim below the crest
    slope = np.gradient(y_crest)
    face = np.clip(slope * 1.4, -1, 1)  # >0: descending to the right = facing right/away; <0 faces the sun
    band = np.exp(-np.clip(yy - y_crest[None, :], 0, None) / (H * 0.03))
    light = np.clip(-face, 0, 1)[None, :] * band
    shade = np.clip(face, 0, 1)[None, :] * (1 - depth) * 0.9
    rgb = rgb + (np.array(hex_rgb(lit), np.float32) - rgb) * (light[..., None] * 0.75)
    rgb = rgb * (1 - shade[..., None] * 0.28)
    if ripples:
        f = fbm(W, H, seed + 4, 60, 2)
        rp = 0.5 + 0.5 * np.sin((yy - y_crest[None, :] * 0.6 + f * 30) / 4.2)
        rgb = rgb * (1 - ripples * (rp[..., None] - 0.5) * depth[..., None])
    layer = gouache_paint(m, "#ffffff", seed=seed, rough=2.2, streak=0.8)
    layer[..., :3] = layer[..., :3] * rgb
    return over(art, layer)


def camel(W, H, x, y, s, step=0.0):
    """Tiny camel silhouette facing left; returns mask."""
    ell = [(x, y, s * 1.0, s * 0.42, 0), (x + s * 0.12, y - s * 0.42, s * 0.46, s * 0.34, 0), (x - s * 1.45, y - s * 0.82, s * 0.30, s * 0.13, -10)]
    st = [(curve([(x - s * 0.7, y - s * 0.1), (x - s * 1.1, y - s * 0.35), (x - s * 1.3, y - s * 0.8)], 8), s * 0.26, None),
          (curve([(x + s * 0.95, y - s * 0.1), (x + s * 1.15, y + s * 0.3)], 4), s * 0.07, None)]
    for lx, d in [(-0.6, -1), (-0.35, 1), (0.5, -1), (0.75, 1)]:
        st.append(([(x + s * lx, y + s * 0.2), (x + s * (lx + 0.08 * d * (1 + step)), y + s * 0.8), (x + s * (lx + 0.04 * d), y + s * 1.3)], s * 0.13, None))
    return np.maximum(ellipses(W, H, ell), strokes(W, H, st))


if "scene" in PARTS:
    W, H = 780, 1500
    nx = Seq(30100); rng = random.Random(7)
    HZ = 0.60
    art = painted_sky(W, H, [(0, "#24152f"), (0.2, "#3c2244"), (0.36, "#6b3252"), (0.47, "#b05a64"), (0.55, "#e38f6a"), (0.6, "#f6bb7f"), (0.64, "#f8d39a"), (1, "#f8d39a")], seed=nx(), streak=1.0)
    # watercolour cloud bands catching the last light
    for (y, x0, x1, th, col) in [(0.44, -40, 520, 14, "#e8907a"), (0.50, 260, 820, 10, "#f4b07c"), (0.40, 380, 820, 9, "#c46a72"), (0.53, -40, 300, 8, "#f6c08a")]:
        pts = [(x, H * y + 6 * math.sin(x / 70 + y * 9)) for x in range(x0, x1, 10)]
        art = G(art, strokes(W, H, [(pts, th, (0.3, 0.3))]), col, mix(col, "#ffffff", 0.2), seed=nx(), density=0.45, edge=0.5, bloom=0.4, rough=7, feather=3)
    # sun glow at the horizon
    sun = circles(W, H, [(300, H * 0.645, 64)])
    art = over(art, glow(sun, "#ffe2a8", radius=70, strength=0.5))
    art = GP(art, sun, "#fff0c8", "#ffe1a0", seed=nx(), rough=1.5, streak=0.3, pad=8)
    # stars, faint, upper sky only
    srng = np.random.default_rng(3)
    st = [(float(srng.uniform(10, W - 10)), float(srng.uniform(10, H * 0.3)), float(srng.uniform(0.8, 1.9))) for _ in range(70)]
    starm = circles(W, H, st) * (1 - np.linspace(0, 1, H)[:, None] * 2.4).clip(0, 1)
    art = over(art, rgba("#fff4dc", starm * 0.8))
    # crescent moon (upper right)
    mx, my, mr = 610, 250, 52
    moon = np.clip(circles(W, H, [(mx, my, mr)]) - circles(W, H, [(mx + 22, my - 12, mr * 0.9)]), 0, 1)
    art = over(art, glow(moon, "#ffe7b5", radius=30, strength=0.45))
    art = GP(art, moon, "#fff1cf", "#f2d79c", seed=nx(), rough=1.2, streak=0.4, pad=10)
    # dunes, far to near
    layers = [
        (H * 0.655, 34, 1.3, "#e7a07a", "#d48a72", "#f7c99a", 0.0),
        (H * 0.70, 70, 1.7, "#d88a64", "#b76a5c", "#f6c58c", 0.0),
        (H * 0.79, 110, 1.2, "#b0614d", "#6a3040", "#f0ad74", 0.05),
        (H * 0.92, 140, 0.9, "#7d3f44", "#38182c", "#d98d62", 0.08),
    ]
    for k, (y0, amp, npk, top, bot, lit, rip) in enumerate(layers):
        pts = crest(W, y0, amp, 50 + k, npk)
        art = dune_layer(art, W, H, pts, top, bot, lit, nx(), rip)
        if k == 1:
            # caravan walking along the second ridge
            xs = [470, 520, 566, 610, 650]
            cm = np.zeros((H, W), np.float32)
            yc = np.interp(xs, [p[0] for p in pts], [p[1] for p in pts])
            for j, (x, yv) in enumerate(zip(xs, yc)):
                cm = np.maximum(cm, camel(W, H, x, yv - 14, 9.5 - j * 0.4, step=(j % 2) * 0.8))
            rope = strokes(W, H, [([(xs[j] + 8, yc[j] - 16), (xs[j + 1] - 12, yc[j + 1] - 22)], 0.8, None) for j in range(len(xs) - 1)])
            art = LC(art, np.maximum(cm, rope), "#4a2436", seed=nx(), wear=0.1, rough=0.5)
        clear()
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "hs-scene")
    save_rgb(art, f"{OUT}/scene.webp", quality=78)

if "dunes" in PARTS:
    W, H = 780, 300
    nx = Seq(30200)
    art = blank(W, H)
    for k, (y0, amp, npk, top, bot, lit) in enumerate([(150, 60, 1.4, "#c47a58", "#93504a", "#f2b47a"), (240, 90, 1.0, "#e4b88c", "#d9a676", "#fbe0b5")]):
        art = dune_layer(art, W, H, crest(W, y0, amp, 80 + k, npk), top, bot, lit, nx(), 0.06 if k else 0)
    # fade the bottom into the sand colour of the section below
    preview(art, "hs-dunes", bg="#3b2340")
    save_full(art, f"{OUT}/dunes.webp", quality=80)
    clear()

if "lantern" in PARTS:
    W, H = 360, 560
    nx = Seq(30300); cx = 180
    art = blank(W, H)
    body = shapes(W, H, [[(cx - 46, 250), (cx - 58, 300), (cx - 50, 380), (cx - 30, 420), (cx + 30, 420), (cx + 50, 380), (cx + 58, 300), (cx + 46, 250)]], smooth=True)
    halo = circles(W, H, [(cx, 335, 56)])
    art = over(art, glow(halo, "#ffb35c", radius=30, strength=0.5))
    # chain
    links = ellipses(W, H, [(cx, 18 + k * 22, 6, 11, 0) for k in range(8)])
    links = np.clip(links - ellipses(W, H, [(cx, 18 + k * 22, 2.6, 7, 0) for k in range(8)]), 0, 1)
    art = FO(art, links, BRASS, seed=nx(), emboss=0.7, sparkle=0.1)
    # glass: glowing warm, hottest in the middle
    art = GP(art, body, "#ffd98c", "#f0a24c", seed=nx(), rough=1.0, streak=0.5, pad=10)
    hot = gaussian_filter(circles(W, H, [(cx, 330, 26)]), 14)
    art = over(art, rgba("#fff4d0", hot * 1.6 * body))
    edge = np.clip(body - gaussian_filter(body, 9) * 1.1, 0, 1) * body
    art = G(art, edge * 2, "#c25a2c", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    # brass frame: ribs, pierced arches, bands
    ribs = strokes(W, H, [(curve([(cx + dx * 46, 252), (cx + dx * 58, 300), (cx + dx * 50, 380), (cx + dx * 30, 420)], 20), 5, None) for dx in (-1, 1)] +
                   [(curve([(cx + dx * 18, 252), (cx + dx * 22, 300), (cx + dx * 19, 380), (cx + dx * 12, 420)], 20), 4, None) for dx in (-1, 1)])
    arches = []
    for k in range(-2, 3):
        x = cx + k * 20
        arches.append((curve([(x - 7, 300), (x - 7, 286), (x, 276), (x + 7, 286), (x + 7, 300)], 12), 2.6, None))
    bands = shapes(W, H, [[(cx - 50, 240), (cx + 50, 240), (cx + 48, 256), (cx - 48, 256)], [(cx - 34, 414), (cx + 34, 414), (cx + 30, 428), (cx - 30, 428)]], smooth=False)
    cap = shapes(W, H, [[(cx - 52, 242), (cx - 40, 210), (cx - 18, 192), (cx, 186), (cx + 18, 192), (cx + 40, 210), (cx + 52, 242)]])
    fin = np.maximum(shapes(W, H, [petal_pts(cx, 186, 26, 7, -math.pi / 2, n=10)]), circles(W, H, [(cx, 176, 7), (cx, 196, 4)]))
    ring = np.clip(circles(W, H, [(cx, 186 - 34, 9)]) - circles(W, H, [(cx, 186 - 34, 5)]), 0, 1)
    bottom = shapes(W, H, [[(cx - 30, 426), (cx + 30, 426), (cx + 6, 470), (cx, 490), (cx - 6, 470)]])
    drop = shapes(W, H, [petal_pts(cx, 486, 34, 7, math.pi / 2, n=10)])
    brass = np.maximum.reduce([ribs, strokes(W, H, arches), bands, cap, fin, ring, bottom, drop])
    art = FO(art, brass, BRASS, seed=nx(), emboss=0.75, sparkle=0.12)
    art = G(art, cap * np.clip(np.linspace(-0.4, 1, W)[None, :] * 1.2, 0, 1), BRASS_D, seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1)
    art = FO(art, strokes(W, H, [([(cx, 120), (cx, 152)], 3, None)]), BRASS, seed=nx())
    preview(art, "hs-lantern", bg="#3b2340")
    save(art, f"{OUT}/lantern.webp", max_w=220, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 460, 90
    nx = Seq(30400); cx, cy = 230, 45
    moon = np.clip(circles(W, H, [(cx - 4, cy, 22)]) - circles(W, H, [(cx + 6, cy - 5, 19)]), 0, 1)
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 8 if k % 2 == 0 else 3.4
        star.append((cx + 10 + math.cos(a) * r, cy - 2 + math.sin(a) * r))
    sm = shapes(W, H, [star], smooth=False)
    lines = strokes(W, H, [(curve([(cx - 34, cy), (cx - 120, cy - 2), (cx - 210, cy + 1)], 20), 2.4, (0.0, 0.9)),
                           (curve([(cx + 34, cy), (cx + 120, cy - 2), (cx + 210, cy + 1)], 20), 2.4, (0.0, 0.9))])
    dots_ = circles(W, H, [(cx - 52, cy, 3.2), (cx + 52, cy, 3.2), (cx - 66, cy, 2), (cx + 66, cy, 2)])
    art = FO(blank(W, H), np.maximum.reduce([moon, sm, lines, dots_]), BRASS, seed=nx(), emboss=0.7, sparkle=0.12)
    preview(art, "hs-divider", tone="#f3e2c9")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)

if "sand" in PARTS:
    n = 512
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    f = wrap_noise(n, n, 3, 22); g = wrap_noise(n, n, 6, 60); fine = wrap_noise(n, n, 8, 0.8)
    rip = 0.5 + 0.5 * np.sin(2 * math.pi * (yy / n * 40 + np.sin(2 * math.pi * xx / n * 2) * 0.6 + f * 2.2))
    base = lerp3("#f5e6cf", "#efd9b9", g)
    base *= (1 - 0.025 * (rip - 0.5) - 0.05 * (fine - 0.5))[..., None]
    art = np.concatenate([base, np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/sand.webp", quality=72)

kb(OUT)
