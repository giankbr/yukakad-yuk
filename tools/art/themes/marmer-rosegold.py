"""Marmer Rose Gold — painted Carrara marble tile + pressed rose-gold foil (cover arch frame, divider, monogram ring,
brushed foil sheet for cards/buttons).
Run: python3 -I /tmp/pen/art/themes/marmer-rosegold.py [marble|frame|rule|ring|sheet]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b_common import *  # noqa

T = "marmer-rosegold"
D = outdir(T)
nxt = Seeds(700)
rng = random.Random(5)
RG = "#c4887c"       # rose-gold foil base


def wrap_blend(big, W, H, p):
    """big: 3H x 3W render of a periodic design → seamless H x W tile (cross-fade into the neighbouring copy)."""
    ramp = np.linspace(0, 1, p, dtype=np.float32)
    ramp = ramp * ramp * (3 - 2 * ramp)
    strip = big[:, W:2 * W].copy()
    for i in range(p):
        x = W - p + i
        strip[:, x] = strip[:, x] * (1 - ramp[i]) + big[:, x] * ramp[i]
    tile = strip[H:2 * H].copy()
    for i in range(p):
        y = H - p + i
        tile[y] = tile[y] * (1 - ramp[i]) + strip[y] * ramp[i]
    return tile


# ---------- 1. marble tile (900 x 450, veins drop exactly one tile height per tile width → seamless) ----------
def marble():
    W, H = 900, 450
    BW, BH = 3 * W, 3 * H
    r = random.Random(12)
    veins = []
    for k in range(6):
        slope = [0.5, 0.5, 0.5, -0.5, 0.0, 0.5][k]
        harm = [(f, r.uniform(8, 40) / f ** 0.6, r.uniform(0, math.tau)) for f in (1, 2, 3, 5, 8)]
        thick = [(f, r.uniform(0, math.tau)) for f in (2, 3)]
        veins.append((r.uniform(0, H), slope, harm, thick, r.uniform(0.5, 1.0), k))
    def draw_set(width, which):
        def draw(cv):
            for y0, slope, harm, thick, strength, k in veins:
                if k not in which:
                    continue
                xs = np.linspace(0, BW, 360)
                for oy in range(-3, 6):
                    pts = [(x, y0 + oy * H + slope * x + sum(A * math.sin(math.tau * f * x / W + ph) for f, A, ph in harm)) for x in xs]
                    for i in range(len(pts) - 1):
                        x = pts[i][0]
                        mod = 0.5 + 0.5 * math.sin(math.tau * thick[0][0] * x / W + thick[0][1]) * math.sin(math.tau * thick[1][0] * x / W + thick[1][1])
                        wv = width * strength * (0.15 + 0.85 * mod ** 1.5)
                        if wv < 0.35:
                            continue
                        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wv, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                        cv.c.drawLine(*pts[i], *pts[i + 1], p)
        return mask_from(BW, BH, draw)
    wide = draw_set(46, {0, 1, 2, 3, 4, 5})
    thin = draw_set(2.6, {0, 1, 3, 4})
    hair = draw_set(1.3, {2, 5})
    base = paper_tile(BW, "#f7f4f0", seed=4, mottle=0.6, fiber=0.0, fine=0.5)[:BH]
    art = np.concatenate([base, np.ones((BH, BW, 1), np.float32)], -1)
    cloud = pigment(gaussian_filter(wide, 18) * 1.5, "#dfd8d2", "#e8e2dd", seed=nxt(), density=0.22, edge=0.04, bloom=0.5, gran=0.1, feather=6, rough=46, mottle=0.9)
    art = glaze(art, cloud)
    art = glaze(art, pigment(thin, "#a39a95", "#bab0a9", seed=nxt(), density=0.62, edge=0.2, bloom=0.2, gran=0.3, feather=0.9, rough=6, mottle=0.6, holes=0.12))
    art = glaze(art, pigment(hair, "#c99c8e", seed=nxt(), density=0.5, edge=0.1, bloom=0, gran=0.3, feather=0.6, rough=3, holes=0.15))
    art[..., 3] = 1
    tile = wrap_blend(art, W, H, 70)
    im = Image.fromarray((np.clip(tile[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(f"{D}/marble.webp", "WEBP", quality=74, method=6)
    big = Image.new("RGB", (W * 2, H * 2))
    for i in range(2):
        for j in range(2):
            big.paste(im, (i * W, j * H))
    big.save(f"{PREV}/mr-marble.png")
    print("marble.webp", os.path.getsize(f"{D}/marble.webp") // 1024, "KB")


# ---------- 2. cover arch frame (foil) ----------
def arch_path(x0, y0, x1, y1):
    p = skia.Path()
    r = (x1 - x0) / 2
    p.moveTo(x0, y1)
    p.lineTo(x0, y0 + r)
    p.arcTo(skia.Rect(x0, y0, x1, y0 + 2 * r), 180, 180, False)
    p.lineTo(x1, y1)
    p.close()
    return p


def sprig_mask(W, H, cx, cy, ang, L, n=5, size=13, mirror=1):
    """Tiny laurel sprig: stem + paired leaves, as one mask."""
    pts = [(cx + math.cos(ang) * L * t + math.sin(t * 3) * 4 * mirror * -math.sin(ang), cy + math.sin(ang) * L * t) for t in np.linspace(0, 1, 18)]
    m = stroke_mask(W, H, pts, 2.6, (0.05, 0.5))
    for i in range(n):
        t = 0.18 + i * (0.78 / n)
        x, y = pts[int(t * 17)]
        s_ = size * (1 - i * 0.1)
        m = np.maximum(m, shape_mask(W, H, petal_pts(x, y, s_, s_ * 0.36, ang - 0.75, 10)))
        m = np.maximum(m, shape_mask(W, H, petal_pts(x, y, s_, s_ * 0.36, ang + 0.75, 10)))
    tip = pts[-1]
    m = np.maximum(m, shape_mask(W, H, petal_pts(tip[0], tip[1], size * .8, size * .3, ang, 10)))
    return m


def frame():
    W, H = 600, 940
    outer = path_mask(W, H, lambda: arch_path(30, 40, 570, 912), stroke=4.0)
    inner = path_mask(W, H, lambda: arch_path(52, 62, 548, 890), stroke=1.8)
    m = np.maximum(outer, inner)
    # keystone ornament: diamond + laurel either side at the arch apex, and at the base
    cx = 300
    dia = shape_mask(W, H, [(cx, 22), (cx + 13, 40), (cx, 58), (cx - 13, 40)], smooth=False)
    m = np.maximum(m, dia)
    m = np.maximum(m, sprig_mask(W, H, cx + 20, 46, -0.12, 120, 5, 15))
    m = np.maximum(m, sprig_mask(W, H, cx - 20, 46, math.pi + 0.12, 120, 5, 15))
    by = 912
    m = np.maximum(m, shape_mask(W, H, [(cx, by - 14), (cx + 10, by), (cx, by + 14), (cx - 10, by)], smooth=False))
    for dx in (-1, 1):
        m = np.maximum(m, dots_mask(W, H, [(cx + dx * 26, by, 3.2), (cx + dx * 40, by, 2.2)]))
    # wear: tiny breaks where the foil didn't transfer
    wear = fbm(W, H, 77, 7, 2)
    m = m * (1 - np.clip((wear - 0.8) * 6, 0, 1) * 0.8)
    art = foil(m, RG, seed=nxt(), emboss=0.5, sparkle=0.05)
    preview(art, f"{PREV}/mr-frame.png", "#f6f3ef")
    save(art, f"{D}/frame.webp", max_w=600, q=84, trim=False)


# ---------- 3. section divider ----------
def rule():
    W, H = 420, 60
    cy = 30
    m = stroke_mask(W, H, [(14 + i * 7.5, cy) for i in range(23)], 2.6, (0.9, 0.02))
    m = np.maximum(m, stroke_mask(W, H, [(W - 14 - i * 7.5, cy) for i in range(23)], 2.6, (0.9, 0.02)))
    m = np.maximum(m, shape_mask(W, H, [(210, cy - 14), (221, cy), (210, cy + 14), (199, cy)], smooth=False))
    m = np.maximum(m, dots_mask(W, H, [(186, cy, 2.6), (234, cy, 2.6)]))
    art = foil(m, RG, seed=nxt(), emboss=0.4, sparkle=0.0)
    preview(art, f"{PREV}/mr-rule.png", "#f6f3ef")
    save(art, f"{D}/rule.webp", max_w=210, q=86)


# ---------- 4. monogram laurel ring (closing, on dark) ----------
def ring():
    W = H = 500
    c = 250
    m = ring_mask(W, H, c, c, 168, 2.4, rng, 0.2)
    m = np.maximum(m, ring_mask(W, H, c, c, 182, 1.2, rng, 0.2))
    # laurel branches on both sides, growing from the bottom up, open at the top
    for side in (-1, 1):
        stem_pts = [(c + math.cos(math.pi / 2 + side * t) * 198, c + math.sin(math.pi / 2 + side * t) * 198) for t in np.linspace(0.12, 2.5, 40)]
        m = np.maximum(m, stroke_mask(W, H, stem_pts, 2.2, (0.02, 0.4)))
        for i in range(10):
            j = 3 + i * 3
            (x0, y0), (x1, y1) = stem_pts[j], stem_pts[j + 1]
            tang = math.atan2(y1 - y0, x1 - x0)
            s_ = 34 - i * 1.6
            m = np.maximum(m, shape_mask(W, H, petal_pts(x0, y0, s_, s_ * .26, tang + 0.8, 14)))
            m = np.maximum(m, shape_mask(W, H, petal_pts(x0, y0, s_ * .9, s_ * .26, tang - 0.8, 14)))
    m = np.maximum(m, shape_mask(W, H, [(c, c + 180), (c + 9, c + 192), (c, c + 204), (c - 9, c + 192)], smooth=False))
    art = foil(m, "#d29a88", seed=nxt(), emboss=0.5, sparkle=0.05)
    preview(art, f"{PREV}/mr-ring.png", "#2a2627")
    save(art, f"{D}/ring.webp", max_w=296, q=84, trim=False)


# ---------- 5. brushed rose-gold foil sheet (cards, buttons) ----------
def sheet():
    W, H = 720, 440
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    brushed = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (0.4, 28))
    brushed = (brushed - brushed.mean()) / (brushed.std() + 1e-6)
    sheen = 0.5 + 0.5 * np.sin((xx * 0.9 - yy * 0.6) / 140 + fbm(W, H, 4, 160, 2) * 2.4)
    lum = 0.78 + 0.26 * sheen + brushed * 0.025
    a = np.array(hex_rgb("#c98a7f"), np.float32); b = np.array(hex_rgb("#f2cdbb"), np.float32)
    t = np.clip(sheen[..., None] * 0.9, 0, 1)
    rgb = (a * (1 - t) + b * t) * lum[..., None]
    rgb = np.clip(rgb, 0, 1)
    im = Image.fromarray((rgb * 255).astype(np.uint8), "RGB")
    im.save(f"{D}/foil-sheet.webp", "WEBP", quality=78, method=6)
    im.save(f"{PREV}/mr-sheet.png")
    print("foil-sheet.webp", os.path.getsize(f"{D}/foil-sheet.webp") // 1024, "KB")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["marble", "frame", "rule", "ring", "sheet"]:
        {"marble": marble, "frame": frame, "rule": rule, "ring": ring, "sheet": sheet}[w]()
