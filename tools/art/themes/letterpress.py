"""Letterpress — printing-shop pieces with real impression: a steel composing stick holding a line of lead sorts
(mirrored faces, a little oxblood ink left on them), a loose ampersand sort, an oxblood hedera fleuron and an ornament
rule printed into the paper (ink squash rim + deboss shading), a blind-debossed laurel wreath (no ink, light and shadow
only) and a thick cotton-paper tile.  Run: python3 -I letterpress.py [part ...]
parts: stick sort fleuron rule wreath cotton   Assets -> public/themes/art/letterpress/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l6_lib import *

OUT = outdir("letterpress")
PARTS = sys.argv[1:] or ["stick", "sort", "fleuron", "rule", "wreath", "cotton"]
OX, OX_D, PAPER = "#6e1a24", "#4f1018", "#f3eee4"
BODONI = skia.Typeface.MakeFromFile("/tmp/node_modules/@fontsource/bodoni-moda/files/bodoni-moda-latin-700-normal.woff")


def text_mask(W, H, txt, x, y, size, mirror=False, tf=BODONI, center=True):
    def draw(cv):
        f = skia.Font(tf, size)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        w = f.measureText(txt)
        cv.c.save()
        if mirror:
            cv.c.translate(x, 0); cv.c.scale(-1, 1); cv.c.translate(-x, 0)
        cv.c.drawString(txt, x - (w / 2 if center else 0), y, f, p)
        cv.c.restore()
    return mask_from(W, H, draw)


def deboss(mask, depth=1.0, blur=1.8, k=5.0, floor=0.06):
    """Impression shading layers for a pressed-in shape: shadow on the upper-left inner wall, light on the lower-right."""
    e = emboss_light(mask, blur, k)
    sh = flat(np.clip(-e, 0, 1) * depth, "#3a2a20", 0.55)
    hi = flat(np.clip(e, 0, 1) * depth, "#ffffff", 0.85)
    fl = flat(gaussian_filter(mask, 0.8), "#6b5a48", floor * depth)
    return over(over(fl, sh), hi)


def ink(mask, col=OX, seed=1, wear=0.14):
    """Letterpress ink: even coverage, slightly darker squash rim, fine speckle where the paper fibre stayed bare."""
    lay = linocut(mask, col, seed=seed, wear=wear, rough=0.8)
    rim = np.clip(mask - gaussian_filter(mask, 1.6), 0, 1)
    lay[..., :3] *= (1 - np.clip(rim * 1.4, 0, 0.35))[..., None]
    return lay


def printed(art, mask, col=OX, seed=1, depth=1.0):
    art = over(art, deboss(mask, depth))
    return over(art, ink(mask, col, seed))


def metal(mask, base, seed=1, sheen=0.35, light=True):
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = fbm(w, h, seed, 30, 3)
    brushed = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.4, 9))
    brushed = (brushed - brushed.mean()) / (brushed.std() + 1e-6)
    lum = 1 + sheen * np.sin(yy / max(8, h * 0.08) + n * 2) * 0.25 + brushed * 0.03 + (emboss_light(mask, 1.2, 4) if light else 0)
    grime = fbm(w, h, seed + 4, 14, 3)
    lum = lum * (1 - 0.18 * np.clip((grime - 0.45) * 2.5, 0, 1))
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(base), np.float32) * lum[..., None]
    rgb = rgb * np.array([1.0, 0.985, 0.96], np.float32)
    return rgba(rgb, np.clip(gaussian_filter(mask, 0.5), 0, 1))


def hedera(W, H, cx, cy, s, ang=0.0):
    """Aldine leaf: heart-shaped leaf + curled stem, pointing right at ang=0."""
    pts = []
    for i in range(60):
        t = i / 60 * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        # rotate the heart so its tip points along +x
        X, Y = -y, x
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + (X * ca - Y * sa) * s, cy + (X * sa + Y * ca) * s))
    leaf = shapes(W, H, [pts])
    vein = strokes(W, H, [([(cx - 6 * s * math.cos(ang), cy - 6 * s * math.sin(ang)), (cx + 12 * s * math.cos(ang), cy + 12 * s * math.sin(ang))], 1.6 * s, (0.1, 0.6))])
    base = (cx - 9 * s * math.cos(ang), cy - 9 * s * math.sin(ang))
    ca, sa = math.cos(ang), math.sin(ang)
    loc = lambda u, v: (base[0] + u * ca - v * sa, base[1] + u * sa + v * ca)
    curl = [loc(-4 * s - math.sin(a) * 5 * s * (1 - k / 20), -5 * s + math.cos(a) * 5 * s * (1 - k / 20)) for k, a in enumerate(np.linspace(0, 4.6, 20))]
    st = strokes(W, H, [([base] + curl, 2.0 * s, (0.0, 0.7))])
    return leaf, st


if "fleuron" in PARTS:
    W, H = 200, 160
    art = blank(W, H)
    leaf, st = hedera(W, H, 110, 80, 3.4, 0.0)
    art = printed(art, np.clip(leaf + st, 0, 1), OX, 3)
    show(art, "lp-fleuron", tone=PAPER)
    save(art, f"{OUT}/fleuron.webp", max_w=120, quality=86)
    clear()

if "rule" in PARTS:
    W, H = 520, 60
    art = blank(W, H)
    m = np.zeros((H, W), np.float32)
    m += shapes(W, H, [rr(20, 29, 196, 31.5), rr(324, 29, 500, 31.5)], smooth=False)
    m += circles(W, H, [(208, 30, 3), (312, 30, 3)])
    l1, s1 = hedera(W, H, 238, 30, 1.45, math.pi)
    l2, s2 = hedera(W, H, 282, 30, 1.45, 0.0)
    m = np.clip(m + l1 + s1 + l2 + s2 + circles(W, H, [(260, 30, 3.6)]), 0, 1)
    art = printed(art, m, OX, 5, 0.8)
    show(art, "lp-rule", tone=PAPER)
    save(art, f"{OUT}/rule.webp", max_w=340, quality=86)
    clear()

if "wreath" in PARTS:
    W, H = 560, 560
    rng = random.Random(4)
    cx, cy, R = 280, 290, 220
    leaves = []
    items = []
    for side in (-1, 1):
        stem = [(cx + side * math.sin(t) * R, cy + math.cos(t) * R) for t in np.linspace(0.18, 2.75, 40)]
        items.append((stem, 5.0, (0.05, 0.4)))
        for i, t in enumerate(np.linspace(0.32, 2.6, 10)):
            px, py = cx + side * math.sin(t) * R, cy + math.cos(t) * R
            tang = math.atan2(-math.sin(t), side * math.cos(t))
            for off in (0.55, -0.55):
                a = tang + off * side
                L = 36 - i * 1.4
                leaves.append(petal_pts(px, py, L * 1.35, L * 0.3, a, n=18))
    m = np.clip(strokes(W, H, items) + shapes(W, H, leaves), 0, 1)
    # tie at the bottom
    m = np.clip(m + strokes(W, H, [(curve([(cx - 30, cy + R + 4), (cx, cy + R - 6), (cx + 30, cy + R + 4)], 12), 4, None)]), 0, 1)
    art = deboss(m, 1.2, 1.6, 6.0, 0.2)
    show(art, "lp-wreath", tone=PAPER)
    save(art, f"{OUT}/wreath.webp", max_w=420, quality=84)
    clear()

if "stick" in PARTS:
    W, H = 820, 230
    art = blank(W, H)
    # stick: long steel tray (back wall + floor) with a knee clamp on the right
    floor = rrect(W, H, [(30, 120, 790, 190, 8)])
    back = rrect(W, H, [(30, 96, 790, 132, 6)])
    art = over(art, soft_shadow(np.clip(floor + back, 0, 1), "#2a2018", 10, 0.35, 6, 10))
    art = over(art, metal(floor, "#9aa0a6", 3))
    art = over(art, metal(back, "#b7bcc1", 4))
    knee = rrect(W, H, [(640, 62, 690, 190, 8)])
    art = over(art, metal(knee, "#868c93", 5))
    screw = circles(W, H, [(665, 84, 13)])
    art = over(art, metal(screw, "#c9cdd1", 6))
    art = over(art, flat(strokes(W, H, [([(656, 84), (674, 84)], 3, None)]), "#4a4e53", 0.9))
    # graduation ticks on the back wall
    ticks = strokes(W, H, [([(x, 98), (x, 104 if (x - 40) % 50 else 112)], 1.2, None) for x in range(40, 630, 10)])
    art = over(art, flat(ticks, "#3d4146", 0.8))
    # the line of sorts (lead), faces up with mirrored glyphs; a few ink-stained
    line = "Cinta & Restu"
    x = 610
    f = skia.Font(BODONI, 46)
    rng = random.Random(7)
    for ch in line:
        w = max(18, f.measureText(ch) + 8)
        x0 = x - w
        block = shapes(W, H, [rr(x0 + 1, 116, x - 1, 178)], smooth=False)
        art = over(art, metal(block, "#7d7f84" if ch != " " else "#6a6c70", rng.randint(1, 999), 0.2))
        top = shapes(W, H, [rr(x0 + 2, 116, x - 2, 122)], smooth=False)
        art = over(art, flat(top, "#c4c6c9", 0.6))
        if ch != " ":
            g = text_mask(W, H, ch, x0 + w / 2, 164, 46, mirror=True)
            art = over(art, flat(gaussian_filter(np.roll(g, 2, 0), 1.2), "#202124", 0.55))
            stained = rng.random() < 0.55
            art = over(art, metal(g, "#5d6066", rng.randint(1, 999), 0.2))
            if stained:
                art = over(art, flat(g * (fbm(W, H, 77, 6, 2) > 0.45), OX, 0.75))
        x = x0
        if x < 50:
            break
    # quad spacer at the left end
    art = over(art, metal(shapes(W, H, [rr(40, 118, x - 2, 172)], smooth=False), "#6d7075", 9, 0.2))
    show(art, "lp-stick", tone=PAPER)
    save(art, f"{OUT}/stick.webp", max_w=720, quality=84)
    clear()

if "sort" in PARTS:
    W, H = 220, 300
    art = blank(W, H)
    body = shapes(W, H, [[(60, 60), (160, 60), (176, 76), (176, 270), (76, 270), (60, 254)]], smooth=False)
    front = shapes(W, H, [rr(60, 76, 160, 270)], smooth=False)
    art = over(art, soft_shadow(body, "#2a2018", 10, 0.35, 8, 10))
    art = over(art, metal(body, "#6c6f74", 3))
    art = over(art, metal(front, "#888b90", 4))
    nick = shapes(W, H, [rr(60, 226, 160, 234)], smooth=False)
    art = over(art, flat(nick, "#4a4d52", 0.9))
    topface = shapes(W, H, [[(60, 60), (160, 60), (176, 76), (76, 76)]], smooth=False)
    art = over(art, flat(topface, "#b8babd", 0.9))
    g = text_mask(W, H, "&", 110, 190, 120)
    art = over(art, flat(gaussian_filter(g, 1.0), OX_D, 0.25))
    art = over(art, flat(g * 0.0 + np.clip(g, 0, 1), OX, 0.0))
    # the '&' engraved on the front as an ink-stained relief (unmirrored here: it's the printed reference)
    art = over(art, ink(g, OX, 9, 0.45))
    show(art, "lp-sort", tone=PAPER)
    save(art, f"{OUT}/sort.webp", max_w=130, quality=84)
    clear()

if "cotton" in PARTS:
    W = H = 420
    big = wrap_noise(W, H, 21, 40) - 0.5
    fine = wrap_noise(W, H, 22, 0.7) - 0.5
    fibr = gaussian_filter(np.random.default_rng(23).random((H, W)).astype(np.float32), (0.5, 6), mode="wrap")
    fibr = (fibr - fibr.mean()) / (fibr.std() + 1e-6)
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(PAPER), np.float32) * (1 + big * 0.028 + fine * 0.045 + fibr * 0.012)[..., None]
    rng = np.random.default_rng(5)
    felt = gaussian_filter(rng.random((H, W)).astype(np.float32), 2.2, mode="wrap")
    felt = (felt - felt.mean()) / (felt.std() + 1e-6)
    fib = np.zeros((H, W), np.float32)
    r2 = random.Random(3)
    items = []
    for _ in range(90):
        x, y = r2.uniform(0, W), r2.uniform(0, H)
        a = r2.uniform(0, math.pi); L = r2.uniform(6, 18)
        items.append(([(x, y), (x + math.cos(a) * L * .5 + r2.uniform(-2, 2), y + math.sin(a) * L * .5), (x + math.cos(a) * L, y + math.sin(a) * L)], 0.7, None))
    fib = strokes(W, H, items)
    rgb = base * (1 + felt[..., None] * 0.012) * (1 - fib[..., None] * 0.05)
    save_rgb(np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/cotton.webp", quality=74)
