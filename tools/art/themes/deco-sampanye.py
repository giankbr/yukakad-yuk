"""Deco Sampanye — 1920s art deco in champagne, ivory & black: pressed champagne-foil sunburst fans and stepped frames,
black letterpress lines, a painted champagne-coupe tower. Run: python3 -I deco-sampanye.py [part ...]
parts: sunburst coupe corner fan ivory noir. Assets -> public/themes/art/deco-sampanye/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a5_lib import *

OUT = outdir("deco-sampanye")
PARTS = sys.argv[1:] or ["sunburst", "coupe", "corner", "fan", "ivory", "noir"]
CHAMP = "#cdb27e"      # champagne foil (paler, pinker than gold)
CHAMP_L = "#efe0bd"
INK = "#1a1714"
IVORY = "#f5efe2"


def wedge(cx, cy, r0, r1, a, da):
    return [(cx + math.cos(a - da) * r0, cy + math.sin(a - da) * r0), (cx + math.cos(a - da * 0.35) * r1, cy + math.sin(a - da * 0.35) * r1),
            (cx + math.cos(a + da * 0.35) * r1, cy + math.sin(a + da * 0.35) * r1), (cx + math.cos(a + da) * r0, cy + math.sin(a + da) * r0)]


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def press(art, mask, seed, depth=0.6):
    """Letterpress bite: ink sits in a slight deboss (shadow on the upper-left inner edge)."""
    hi, lo = emboss_light(mask, depth, 1.2, ang=(0.7, 0.7))
    return G(art, lo * 0.9, "#6d6250", seed=seed, density=0.35, edge=0, bloom=0, rough=0.5, feather=0.5, pad=8)


if "sunburst" in PARTS:
    W, H = 760, 400
    cx, cy = W / 2, 392
    nx = Seq(20100)
    art = blank(W, H)
    rays_long, rays_short, lines = [], [], []
    N = 34
    for k in range(N + 1):
        a = math.pi + k * math.pi / N
        if k % 2 == 0:
            rays_long.append(wedge(cx, cy, 96, 366, a, 0.045))
        else:
            rays_short.append(wedge(cx, cy, 104, 262, a, 0.03))
            lines.append(([(cx + math.cos(a) * 282, cy + math.sin(a) * 282), (cx + math.cos(a) * 338, cy + math.sin(a) * 338)], 2.2, None))
    half = np.zeros((H, W), np.float32); half[: int(cy) + 1] = 1
    longm = shapes(W, H, rays_long, smooth=False) * half
    shortm = shapes(W, H, rays_short, smooth=False) * half
    # the rising sun: stepped half discs
    sun = np.clip(circles(W, H, [(cx, cy, 70)]), 0, 1) * half
    steps = np.maximum(ring(W, H, cx, cy, 86, 4), ring(W, H, cx, cy, 380, 3)) * half
    # ink: thin letterpress lines between the rays + outer dotted arc
    dots_ = circles(W, H, [(cx + math.cos(math.pi + t * math.pi / 60) * 352, cy + math.sin(math.pi + t * math.pi / 60) * 352, 2.6) for t in range(1, 60)]) * half
    inkm = np.maximum(strokes(W, H, lines), dots_)
    art = LC(art, inkm, INK, seed=nx(), wear=0.4, rough=0.8)
    art = press(art, inkm, nx())
    art = FO(art, longm, CHAMP, seed=nx(), emboss=0.8, sparkle=0.12)
    art = FO(art, shortm, mix(CHAMP, "#b98f62", 0.35), seed=nx(), emboss=0.7, sparkle=0.08)
    art = FO(art, np.maximum(sun, steps), CHAMP, seed=nx(), emboss=0.9, sparkle=0.14)
    # stepped ziggurat lines inside the sun (letterpress black)
    zig = np.maximum.reduce([ring(W, H, cx, cy, r, 2.6) for r in (24, 40, 56)]) * half
    art = LC(art, zig * sun, INK, seed=nx(), wear=0.3, rough=0.5)
    preview(art, "ds-sunburst", tone=IVORY)
    save(art, f"{OUT}/sunburst.webp", max_w=620, quality=82)
    clear()

if "coupe" in PARTS:
    W, H = 600, 560
    nx = Seq(20200); rng = random.Random(22)
    gw, bowl_d, stem_h, foot_r = 62, 30, 46, 26     # half rim width, bowl depth, stem, foot half width
    gh = bowl_d + stem_h + 8
    rows = [4, 3, 2, 1]
    glasses = []
    base_y = H - 22
    for ri, n in enumerate(rows):
        y_foot = base_y - ri * (gh - 2)
        for k in range(n):
            x = W / 2 + (k - (n - 1) / 2) * (gw * 2 + 4)
            glasses.append((x, y_foot, ri))
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(W / 2, H - 16, 300, 12, 18)])
    art = G(art, shadow, "#5b4a33", seed=nx(), density=0.25, edge=0.05, bloom=0, rough=4, feather=6)
    # cascading champagne streams (behind glasses), from upper rims to lower bowls
    streams = []
    for (x, yf, ri) in glasses:
        if ri == 0:
            continue
        rim_y = yf - gh
        for side in (-1, 1):
            x0 = x + side * (gw - 4)
            pts = curve([(x0, rim_y + 2), (x0 + side * 6, rim_y + 20), (x0 + side * 9, rim_y + gh - 8)], 20)
            streams.append((pts, 3.6, (0.05, 0.4)))
    sm = strokes(W, H, streams)
    art = G(art, sm, "#e8c97a", "#d6ad5c", seed=nx(), density=0.55, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)
    for (x, yf, ri) in sorted(glasses, key=lambda g: -g[2]):
        rim_y = yf - gh
        bowl = [(x - gw, rim_y)] + [(x + math.cos(math.pi - t * math.pi / 14) * gw, rim_y + math.sin(t * math.pi / 14) * bowl_d) for t in range(1, 14)] + [(x + gw, rim_y)]
        bowlm = shapes(W, H, [bowl], smooth=True)
        rim_ell = ellipses(W, H, [(x, rim_y, gw, 7, 0)])
        liquid = np.clip(bowlm - ellipses(W, H, [(x, rim_y - 1, gw + 2, 9, 0)]) * (np.mgrid[0:H, 0:W][0] < rim_y + 3), 0, 1)
        stem = strokes(W, H, [([(x, rim_y + bowl_d - 2), (x, yf - 6)], 5.2, None)])
        knob = ellipses(W, H, [(x, rim_y + bowl_d + 2, 6, 4, 0)])
        foot = ellipses(W, H, [(x, yf - 4, foot_r, 5, 0)])
        glass = np.clip(bowlm + rim_ell + stem + knob + foot, 0, 1)
        art = knockout(art, glass, amount=0.7, grow=1.5)
        # glass body: very pale cool wash so it reads transparent on ivory
        art = G(art, glass, "#e9e6de", "#d8d4ca", seed=nx(), density=0.38, edge=0.7, bloom=0.2, rough=1.2, feather=0.8, pad=10)
        # champagne in the bowl, deeper at the bottom
        art = G(art, liquid, "#f0d68e", "#d9b25e", seed=nx(), density=0.75, edge=0.55, bloom=0.3, gran=0.2, rough=1.5, feather=0.8, pad=10)
        low = liquid * np.clip((np.mgrid[0:H, 0:W][0] - rim_y) / bowl_d, 0, 1)
        art = G(art, low, "#c99a45", seed=nx(), density=0.45, edge=0.1, bloom=0.2, rough=1, feather=1, pad=10)
        # bubbles
        bub = circles(W, H, [(x + rng.uniform(-gw * 0.6, gw * 0.6), rim_y + rng.uniform(6, bowl_d - 6), rng.uniform(0.9, 2.0)) for _ in range(9)]) * liquid
        art = OV(art, bub, lambda m: layer(m, "#fff8e2", 0.85), pad=4)
        # glass contour lines (ink, light) + white gouache highlights
        cont = np.clip(gaussian_filter(glass, 0.8) - gaussian_filter(glass, 2.2), 0, 1) * 2.2
        art = G(art, np.clip(cont, 0, 1), "#6e675c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4, pad=8)
        hi = strokes(W, H, [(curve([(x - gw * 0.72, rim_y + 6), (x - gw * 0.5, rim_y + bowl_d * 0.72), (x - gw * 0.2, rim_y + bowl_d * 0.92)], 12), 3.2, (0.1, 0.5)),
                            ([(x - 1.5, rim_y + bowl_d + 6), (x - 1.5, yf - 10)], 1.4, None)])
        art = GP(art, hi, "#ffffff", "#fbf7ea", seed=nx(), rough=0.5, streak=0.2, pad=6, density=0.8)
        # champagne-foil rim
        rimline = np.clip(ellipses(W, H, [(x, rim_y, gw + 1, 7.5, 0)]) - ellipses(W, H, [(x, rim_y + 0.6, gw - 2.2, 5.2, 0)]), 0, 1)
        art = FO(art, rimline, CHAMP, seed=nx(), emboss=0.5, sparkle=0.2, pad=6)
        art = FO(art, np.clip(foot - ellipses(W, H, [(x, yf - 5, foot_r - 3, 3, 0)]), 0, 1), CHAMP, seed=nx(), emboss=0.4, pad=6)
    # a little foam crown + rising bubbles on the top glass
    tx, tyf, _ = glasses[-1]
    trim = tyf - gh
    foam = circles(W, H, [(tx + rng.uniform(-gw * 0.8, gw * 0.8), trim - rng.uniform(0, 7), rng.uniform(3, 7)) for _ in range(22)])
    art = G(art, foam, "#fbf2d6", "#efdba6", seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=1, feather=0.6)
    rise = circles(W, H, [(tx + rng.gauss(0, 26), trim - 14 - rng.uniform(0, 80), rng.uniform(1.4, 3.4)) for _ in range(16)])
    art = FO(art, rise, CHAMP_L, seed=nx(), emboss=0.4, sparkle=0.3, pad=4)
    preview(art, "ds-coupe", tone=IVORY)
    save(art, f"{OUT}/coupe.webp", max_w=440, quality=82)
    clear()

if "corner" in PARTS:
    W, H = 300, 300
    nx = Seq(20300)
    def stepL(o, s):
        # stepped L running down the left & along the top with two notched steps at the corner
        return [(o, H - 6), (o, o + 2 * s), (o + s, o + 2 * s), (o + s, o + s), (o + 2 * s, o + s), (o + 2 * s, o), (W - 6, o)]
    items = [(stepL(10, 26), 4.0, None), (stepL(22, 22), 1.8, None), (stepL(32, 18), 1.2, None)]
    m = strokes(W, H, items, cap=False)
    fan = []
    cx, cy = 44, 44
    for k in range(7):
        a = k * (math.pi / 2) / 6
        fan.append(wedge(cx, cy, 4, 64, a, 0.08))
    fm = shapes(W, H, fan, smooth=False)
    q = np.zeros((H, W), np.float32); q[int(cy):, int(cx):] = 1
    fm = fm * q
    dots_ = circles(W, H, [(150, 10, 3.4), (190, 10, 3.0), (10, 150, 3.4), (10, 190, 3.0)])
    art = FO(blank(W, H), np.maximum(m, dots_), CHAMP, seed=nx(), emboss=0.8, sparkle=0.12)
    art = FO(art, fm, CHAMP, seed=nx(), emboss=0.8)
    arc = np.clip(ring(W, H, cx, cy, 76, 2.2) * q, 0, 1)
    art = LC(art, arc, INK, seed=nx(), wear=0.3, rough=0.6)
    preview(art, "ds-corner", tone=IVORY)
    save(art, f"{OUT}/corner.webp", max_w=150, quality=84)

if "fan" in PARTS:
    W, H = 600, 110
    nx = Seq(20400)
    cx, cy = W / 2, 96
    rays = [wedge(cx, cy, 10, 80, math.pi + k * math.pi / 10, 0.07) for k in range(11)]
    half = np.zeros((H, W), np.float32); half[: int(cy) + 1] = 1
    fm = shapes(W, H, rays, smooth=False) * half
    lines = [([(cx - 96, cy), (60, cy)], 2.4, None), ([(cx + 96, cy), (W - 60, cy)], 2.4, None),
             ([(cx - 96, cy - 10), (150, cy - 10)], 1.2, None), ([(cx + 96, cy - 10), (W - 150, cy - 10)], 1.2, None)]
    dia = [[(x, cy - 9), (x + 9, cy), (x, cy + 9), (x - 9, cy)] for x in (42, W - 42)]
    art = FO(blank(W, H), np.maximum(fm, shapes(W, H, dia, smooth=False)), CHAMP, seed=nx(), emboss=0.8, sparkle=0.12)
    art = LC(art, strokes(W, H, lines, cap=False), INK, seed=nx(), wear=0.35, rough=0.6)
    art = LC(art, np.clip(ring(W, H, cx, cy, 92, 2.2) * half, 0, 1), INK, seed=nx(), wear=0.3, rough=0.5)
    preview(art, "ds-fan", tone=IVORY)
    save(art, f"{OUT}/fan.webp", max_w=320, quality=84)

if "ivory" in PARTS:
    # cotton letterpress stock with a blind-debossed fan-scale pattern (seamless)
    n = 360
    nx = Seq(20500)
    base = np.asarray(paper(n, n, IVORY, seed=5, fiber=0.6, mottle=0.3), np.float32) / 255
    cot = wrap_noise(n, n, 6, 1.2) - 0.5
    base *= (1 + cot * 0.03)[..., None]
    # fan scales: rows of half circles, offset every other row
    items = []
    R = 45
    for row in range(9):
        for col in range(5):
            x = col * 2 * R + (R if row % 2 else 0); y = row * R
            items.append((x, y))
    scale = np.zeros((n, n), np.float32)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    for (x, y) in items:
        for dx in (-n, 0, n):
            for dy in (-n, 0, n):
                d = np.hypot(xx - x - dx, yy - y - dy)
                ringm = np.clip(1.6 - np.abs(d - R * 0.96), 0, 1) * (yy > y + dy - 1)
                scale = np.maximum(scale, ringm)
    scale = scale[:n, :n] if scale.shape[0] > n else scale
    hi, lo = emboss_light(scale, 1.0, 0.9, ang=(0.7, 0.7))
    base = base * (1 - lo[..., None] * 0.05) + hi[..., None] * 0.028
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/ivory.webp", quality=72)

if "noir" in PARTS:
    # black lacquer card with faint champagne fan-scale lines (seamless tile)
    n = 240
    base = rgb_arr(n, n, "#191613") * (0.9 + 0.2 * wrap_noise(n, n, 9, 30))[..., None]
    base *= (1 + (wrap_noise(n, n, 10, 0.8) - 0.5) * 0.06)[..., None]
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    R = 30
    sc = np.zeros((n, n), np.float32)
    for row in range(n // R + 1):
        for col in range(n // (2 * R) + 1):
            x = col * 2 * R + (R if row % 2 else 0); y = row * R
            for dx in (-n, 0, n):
                for dy in (-n, 0, n):
                    d = np.hypot(xx - x - dx, yy - y - dy)
                    for rr in (R * 0.96, R * 0.62):
                        sc = np.maximum(sc, np.clip(1.2 - np.abs(d - rr), 0, 1) * (yy > y + dy - 1))
    gold = rgb_arr(n, n, CHAMP)
    a = sc * 0.16
    base = base * (1 - a[..., None]) + gold * a[..., None]
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/noir.webp", quality=74)
