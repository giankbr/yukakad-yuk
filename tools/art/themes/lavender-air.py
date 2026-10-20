"""Lavender Air — loose watercolour wisteria racemes, lavender sprigs, soft violet washes, washi tape, paper.
Run: python3 -I /tmp/pen/art/themes/lavender-air.py [asset…]
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _p2_lib import *  # noqa

D = f"{OUT}/lavender-air"
os.makedirs(D, exist_ok=True)
TONE = "#f4f0fa"
LIGHT, MID, DEEP, PLUM = "#dccdf0", "#b093d9", "#7b5ea7", "#55367f"
GREENS = [("#b7c6ad", "#7f9676"), ("#a9bda2", "#6f8a6a")]


def floret(W, H, x, y, r, a, sd, rng, k):
    """One wisteria floret: a pair of soft petals with a deeper throat; k in [0,1] = depth along the raceme."""
    lay = blank(W, H)
    base = mix(LIGHT, MID, 0.25 + 0.6 * k)
    deep = mix(MID, DEEP, 0.3 + 0.6 * k)
    for side in (-1, 1):
        pts = deform(petal_pts(x, y, r * 1.9, r * .8, a + side * rng.uniform(.35, .6), n=10), rng, 1, .08)
        lay = glaze(lay, pig(shape_mask(W, H, pts), base, mix(base, deep, .4), seed=sd(), density=0.5, edge=0.55, bloom=0.4, rough=3, feather=1.0))
    tip = shape_mask(W, H, deform(ellipse_pts(x + math.cos(a) * r * .3, y + math.sin(a) * r * .3, r * .55, r * .4, 8, a), rng, 1, .1))
    lay = glaze(lay, pig(tip, deep, PLUM, seed=sd(), density=0.55, edge=0.6, bloom=0.1, rough=2))
    return lay


def raceme(W, H, x0, y0, length, sway, sd, rng, scale=1.0):
    """A hanging wisteria cluster: stem curving down, florets loose at the top and dense toward the tip."""
    spine = [(x0, y0), (x0 + sway * .3, y0 + length * .3), (x0 + sway * .8, y0 + length * .65), (x0 + sway, y0 + length)]
    sp = curve(spine, 60)
    art, m = stem(W, H, spine, 4 * scale, "#8a9a7c", sd, density=0.4)
    flor = blank(W, H)
    n = int(64 * scale)
    order = sorted(range(n), key=lambda i: -i)        # paint the tip first, the fuller top last (overlaps read as depth)
    for i in order:
        k = (i / n) ** 0.85
        px, py = sp[min(len(sp) - 1, int(k * (len(sp) - 1)))]
        spread = ((1 - k) * 30 + 9) * scale
        fx = px + rng.gauss(0, spread); fy = py + rng.gauss(0, 9 * scale)
        r = (19 - 9 * k) * scale * rng.uniform(.8, 1.15)
        ang = math.pi / 2 + rng.gauss(0, .45) + (fx - px) * 0.012
        flor = glaze(flor, floret(W, H, fx, fy, r, ang, sd, rng, k))
    # buds at the tip
    for j in range(5):
        bx, by = sp[-1][0] + rng.gauss(0, 8 * scale), sp[-1][1] + j * 7 * scale + rng.uniform(0, 6)
        bm = shape_mask(W, H, deform(ellipse_pts(bx, by, 5 * scale, 7 * scale, 8), rng, 1, .1))
        flor = glaze(flor, pig(bm, DEEP, PLUM, seed=sd(), density=0.55, edge=0.5, rough=2))
    return glaze(art, flor)


def wisteria():
    W, H = 640, 860
    rng = random.Random(21); sd = Seeds(300)
    art = blank(W, H)
    # leaves fanning from the hanging point
    for (x, y, L, a, g) in [(300, 60, 170, 2.55, 0), (330, 50, 150, 0.55, 1), (290, 70, 120, 1.9, 1), (350, 60, 130, 1.1, 0), (260, 40, 110, 2.95, 0)]:
        lay, _ = leaf(W, H, x, y, L, a, *GREENS[g], sd, rng, width=0.26, curl=rng.uniform(-.2, .2))
        art = glaze(art, lay)
    art = glaze(art, raceme(W, H, 300, 70, 640, 70, sd, rng, scale=1.0))
    art = glaze(art, raceme(W, H, 420, 90, 430, -40, sd, rng, scale=0.78))
    art = glaze(art, raceme(W, H, 200, 100, 360, 30, sd, rng, scale=0.7))
    # a few loose drifting petals
    for (x, y, r) in [(520, 560, 9), (120, 520, 8), (560, 400, 7), (90, 300, 8)]:
        pm = shape_mask(W, H, deform(petal_pts(x, y, r * 2, r * .8, rng.uniform(0, 6.3), n=10), rng, 1, .08))
        art = glaze(art, pig(pm, MID, DEEP, seed=sd(), density=0.45, edge=0.5, rough=2))
    print("wisteria", save_asset(art, f"{D}/wisteria.webp", max_w=420, quality=80), kb(f"{D}/wisteria.webp"))
    preview(art, f"{PREV}/la-wisteria.png", TONE)


def sprig():
    """Lavender sprig: three stalks with stacked florets, used as the section ornament."""
    W, H = 360, 300
    rng = random.Random(5); sd = Seeds(900)
    art = blank(W, H)
    for (x0, lean, h, sc) in [(180, 0, 230, 1.0), (122, -0.35, 190, .85), (240, 0.32, 200, .85)]:
        top = (x0 + math.sin(lean) * h * .5, 280 - h)
        pts = [(x0, 285), (x0 + math.sin(lean) * h * .2, 285 - h * .45), top]
        lay, _ = stem(W, H, pts, 3.2, "#8a9a7c", sd, density=0.5)
        art = glaze(art, lay)
        sp = curve(pts, 40)
        for i in range(int(9 * sc)):
            k = i / (9 * sc)
            px, py = sp[int(len(sp) * (0.45 + 0.55 * k)) - 1]
            for side in (-1, 1):
                r = (8 - 3 * k) * sc
                m = shape_mask(W, H, deform(ellipse_pts(px + side * r * .9, py, r * 1.05, r * .7, 8, side * .4), rng, 1, .12))
                art = glaze(art, pig(m, mix(LIGHT, MID, .3 + .5 * k), mix(MID, DEEP, .3 + .5 * k), seed=sd(), density=0.52, edge=0.55, bloom=0.3, rough=2.5))
        tipm = shape_mask(W, H, deform(ellipse_pts(top[0], top[1] + 2, 4 * sc, 7 * sc, 8), rng, 1, .1))
        art = glaze(art, pig(tipm, DEEP, PLUM, seed=sd(), density=0.55, edge=0.5, rough=2))
    for (x, y, L, a, g) in [(178, 270, 70, 3.6, 0), (184, 268, 64, -0.45, 1)]:
        lay, _ = leaf(W, H, x, y, L, a, *GREENS[g], sd, rng, width=0.24)
        art = glaze(art, lay)
    print("sprig", save_asset(art, f"{D}/sprig.webp", max_w=200, quality=80), kb(f"{D}/sprig.webp"))
    preview(art, f"{PREV}/la-sprig.png", TONE)


def wash():
    """A loose violet wash cloud with blooms — sits behind polaroids / gallery bubbles."""
    W, H = 900, 700
    rng = random.Random(9); sd = Seeds(50)
    art = blank(W, H)
    for (x, y, rx, ry, c1, c2, d) in [(430, 360, 360, 240, "#e6dcf4", "#cdbbea", .5), (560, 300, 230, 170, "#d7c6ee", "#b79ddc", .4), (330, 420, 200, 150, "#dccdf0", "#b093d9", .35)]:
        m = shape_mask(W, H, deform(ellipse_pts(x, y, rx, ry, 12, rng.uniform(-.4, .4)), rng, 3, .18))
        art = glaze(art, pig(m, c1, c2, seed=sd(), density=d, edge=0.4, bloom=0.6, rough=14, mottle=0.7, holes=0.08))
    art = glaze(art, pig(dots(W, H, 450, 360, 300, 200, 26, 2, 6, rng), MID, seed=sd(), density=0.45, edge=0.2, bloom=0, rough=1, feather=.5))
    print("wash", save_asset(art, f"{D}/wash.webp", max_w=560, quality=76), kb(f"{D}/wash.webp"))
    preview(art, f"{PREV}/la-wash.png", TONE)


def tape():
    """Translucent washi tape strip (lilac, with torn ends and faint stripes)."""
    W, H = 260, 80
    rng = random.Random(3)
    pts = [(14, 18), (W - 12, 14), (W - 16, H - 14), (12, H - 18)]
    pts = deform(pts, rng, 3, .05)
    m = shape_mask(W, H, pts, smooth=False)
    # torn ends: nibble the short edges
    def nib(cv):
        for x in (12, W - 12):
            for _ in range(7):
                cv.c.drawCircle(x + rng.gauss(0, 3), rng.uniform(14, H - 14), rng.uniform(3, 6), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    m = np.clip(m - mask_from(W, H, nib), 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#e9dff6"), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    stripes = 0.5 + 0.5 * np.cos(xx / 9 * math.tau)
    rgb *= (1 - stripes[..., None] * 0.035)
    g = fbm(W, H, 4, 20, 3)
    a = m * (0.55 + 0.2 * g)
    art = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
    print("tape", save_asset(art, f"{D}/tape.webp", max_w=130, quality=82), kb(f"{D}/tape.webp"))


def petal():
    W, H = 100, 100
    rng = random.Random(8); sd = Seeds(70)
    m = shape_mask(W, H, deform(petal_pts(14, 52, 72, 26, -0.25, n=14, cup=0.3), rng, 2, .05))
    art = pig(m, "#cdb8ec", "#a98bd2", seed=sd(), density=0.6, edge=0.7, bloom=0.4, rough=3, pad=10)
    print("petal", save_asset(art, f"{D}/petal.webp", max_w=40, quality=80), kb(f"{D}/petal.webp"))


def texture():
    save_texture(paper_tile(512, "#fdfbff", seed=31, mottle=0.5, fine=1.0, fiber=1.0, strength=0.8), f"{D}/paper.webp", quality=70)
    print("paper", kb(f"{D}/paper.webp"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["wisteria", "sprig", "wash", "tape", "petal", "texture"]
    for w in which:
        globals()[w]()
