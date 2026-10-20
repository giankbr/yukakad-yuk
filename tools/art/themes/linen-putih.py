"""Linen Putih — linen weave tile, one ink-and-pencil olive branch, paper grain. Restraint is the point.
Run: python3 -I /tmp/pen/art/themes/linen-putih.py [asset…]
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _p2_lib import *  # noqa

D = f"{OUT}/linen-putih"
os.makedirs(D, exist_ok=True)
TONE = "#f6f3ee"
INK = "#2b2621"


def leaf_outline(x, y, L, wdt, a, rng, n=18):
    """Open polyline around a lanceolate leaf (two strokes meeting at the tip, as a pen would draw it)."""
    pts = petal_pts(x, y, L, wdt, a, n=n)
    pts = deform(pts, rng, 1, 0.02)
    # split at the tip (index ~ n/2 is the base? petal_pts starts at the tip side x=length... index 0 is t=0 → x=L (tip))
    return [pts[: n // 2 + 1], pts[n // 2:] + [pts[0]]]


def botanical():
    W, H = 520, 760
    rng = random.Random(14)
    lines, hatch_regions = [], []
    main = [(300, 740), (280, 600), (250, 460), (235, 320), (245, 190), (270, 80)]
    sp = curve(main, 120)
    lines.append(sp)
    # secondary twig
    twig = [(248, 440), (300, 380), (360, 345), (410, 330)]
    lines.append(curve(twig, 50))
    twig2 = [(242, 250), (190, 210), (150, 160)]
    lines.append(curve(twig2, 40))
    leaves = []
    for i, t in enumerate(np.linspace(0.08, 0.95, 11)):
        px, py = sp[int(t * (len(sp) - 1))]
        side = -1 if i % 2 else 1
        tangent = math.atan2(sp[min(len(sp) - 1, int(t * (len(sp) - 1)) + 3)][1] - py, sp[min(len(sp) - 1, int(t * (len(sp) - 1)) + 3)][0] - px)
        a = tangent + side * rng.uniform(0.9, 1.35)
        L = rng.uniform(95, 130) * (1 - 0.35 * t)
        leaves.append((px, py, L, L * 0.19, a))
    for (tw, ts) in ((twig, (0.35, 0.7, 1.0)), (twig2, (0.5, 1.0))):
        c = curve(tw, 50)
        for j, t in enumerate(ts):
            px, py = c[min(len(c) - 1, int(t * (len(c) - 1)))]
            a = math.atan2(c[-1][1] - c[0][1], c[-1][0] - c[0][0]) + (1 if j % 2 else -1) * rng.uniform(0.6, 1.1)
            L = rng.uniform(70, 95)
            leaves.append((px, py, L, L * 0.2, a))
    for k, (x, y, L, wdt, a) in enumerate(leaves):
        lines += leaf_outline(x, y, L, wdt, a, rng)
        rib = [(x + math.cos(a) * L * t + rng.gauss(0, .6), y + math.sin(a) * L * t + rng.gauss(0, .6)) for t in np.linspace(0.08, 0.82, 10)]
        lines.append(rib)
        if k % 3 == 0:
            hatch_regions.append(shape_mask(W, H, petal_pts(x, y, L * 0.9, wdt * 0.5, a + 0.09, n=14)))
    # tiny olives
    for (x, y) in [(262, 505), (254, 365), (338, 352), (175, 195)]:
        o = ellipse_pts(x + rng.uniform(-6, 6), y + rng.uniform(-6, 6), 7, 9, 12, rng.uniform(-.5, .5))
        lines.append(o + [o[0]])
    m = ink_mask(W, H, lines, width=1.9, jitter=0.35, seed=7, taper=(0.06, 0.06), wobble=0.9)
    art = ink(m, INK, seed=3, dry=0.18, bleed=0.3, density=0.9)
    hm = np.zeros((H, W), np.float32)
    for r in hatch_regions:
        hm = np.maximum(hm, r)
    art = over(pencil(hatch_mask(W, H, hm, spacing=5.5, angle=-0.75, width=0.9, seed=5), "#5a534b", seed=4, grain=0.55, density=0.5), art)
    print("botanical", save_asset(art, f"{D}/botanical.webp", max_w=300, quality=82), kb(f"{D}/botanical.webp"))
    preview(art, f"{PREV}/lp-botanical.png", TONE)


def texture():
    save_texture(linen_tile(512, "#f5f2ec", seed=5, pitch=3.5, strength=1.0, slub=0.7), f"{D}/linen.webp", quality=70)
    save_texture(paper_tile(512, "#fcfaf7", seed=12, mottle=0.5, fine=0.9, fiber=1.0, strength=0.7), f"{D}/paper.webp", quality=68)
    print("linen", kb(f"{D}/linen.webp"), "paper", kb(f"{D}/paper.webp"))
    Image.open(f"{D}/linen.webp").resize((1024, 1024), Image.NEAREST).save(f"{PREV}/lp-linen.png")


if __name__ == "__main__":
    which = sys.argv[1:] or ["botanical", "texture"]
    for w in which:
        globals()[w]()
