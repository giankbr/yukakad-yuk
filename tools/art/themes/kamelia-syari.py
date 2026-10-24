"""Kamelia Syari — pink semi-double camellias with glossy dark-green leaves in opaque gouache on blush paper, a
little pressed gold in the stamens and divider dots. Flora only (no figures).
Run: python3 -I kamelia-syari.py [part ...]   parts: rangkaian setangkai bunga garis kertas"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t6_lib import *

OUT = outdir("kamelia-syari")
PARTS = sys.argv[1:] or ["rangkaian", "setangkai", "bunga", "garis", "kertas"]
BLUSH = "#f7e6e1"
PAL = ("#f7c9d3", "#e3819b", "#a5304f", "#fde6eb")
PAL2 = ("#fbd9df", "#eb98ac", "#b3445f", "#fff0f2")
LP = ("#a9cdb3", "#2d5c45", "#163426", "#a4c7ae")
TWIG = ("#4a3427", "#6d4e39")


def leaves_along(art, W, H, pts, rng, nx, n, L0, L1, every=None, pals=None, skip=()):
    cp = curve(pts, 80)
    for k in range(n):
        if k in skip:
            continue
        t = 0.12 + 0.86 * k / max(1, n - 1)
        i = min(len(cp) - 2, int(t * (len(cp) - 1)))
        (x0, y0), (x1, y1) = cp[i], cp[i + 1]
        ta = math.atan2(y1 - y0, x1 - x0)
        side = 1 if k % 2 else -1
        ang = ta + side * rng.uniform(0.55, 1.0)
        L = rng.uniform(L0, L1) * (1.05 - 0.3 * t)
        pal = (pals or [LP])[k % len(pals or [LP])]
        art = glossy_leaf(art, W, H, x0, y0, L, ang, rng, nx, pal, gloss=0.45)
        trim_cache()
    return art


def cluster(W, H, seed):
    rng = random.Random(seed); nx = Seq(seed * 10)
    art = blank(W, H)
    cx, cy = W / 2, H * 0.48
    DK = ("#8fb79b", "#24503b", "#10291d", "#93b89c")
    main = [(-10, cy + 70), (W * .25, cy + 20), (cx, cy), (W * .75, cy - 24), (W + 10, cy - 70)]
    b1 = [(W * .27, cy + 18), (W * .2, cy - 80), (W * .1, cy - 170)]
    b2 = [(W * .72, cy - 20), (W * .8, cy + 80), (W * .92, cy + 160)]
    b3 = [(cx - 40, cy + 4), (cx - 70, cy + 120), (cx - 140, cy + 210)]
    for pts, wd in ((main, 13), (b1, 8), (b2, 8), (b3, 7)):
        art = twig(art, W, H, pts, wd, nx, *TWIG)
    art = leaves_along(art, W, H, main[:2] + [(W * .4, cy + 8)], rng, nx, 5, 120, 170, pals=[DK, LP])
    art = leaves_along(art, W, H, [(W * .6, cy - 10), (W * .75, cy - 24), (W + 10, cy - 70)], rng, nx, 5, 120, 165, pals=[LP, DK])
    art = leaves_along(art, W, H, b1, rng, nx, 4, 100, 140, pals=[LP, DK])
    art = leaves_along(art, W, H, b2, rng, nx, 4, 100, 140, pals=[DK, LP])
    art = leaves_along(art, W, H, b3, rng, nx, 4, 100, 135, pals=[LP])
    art = cam_bud(art, W, H, W * .1, cy - 172, 26, -2.0, rng, nx, PAL, LP)
    art = cam_bud(art, W, H, W * .92, cy + 162, 22, 0.9, rng, nx, PAL2, LP)
    art = cam_bud(art, W, H, cx - 142, cy + 212, 20, 2.1, rng, nx, PAL, LP)
    for (x, y, r, pal, tl) in [(W * .26, cy + 16, 112, PAL2, 0.8), (W * .73, cy - 22, 104, PAL, 0.72), (cx + 4, cy - 6, 148, PAL, 0.9)]:
        art = camellia(art, W, H, x, y, r, rng, nx, pal, tilt=tl, rings=(8, 7, 5), stamens=True)
        trim_cache()
    art = glossy_leaf(art, W, H, cx + 70, cy + 70, 140, 0.9, rng, nx, LP, gloss=0.5)
    return art


def sprig(W, H, seed):
    rng = random.Random(seed); nx = Seq(seed * 10)
    art = blank(W, H)
    art = twig(art, W, H, [(30, H - 30), (W * .3, H * .7), (W * .55, H * .45), (W * .85, H * .16)], 9, nx, *TWIG)
    tw = [(30, H - 30), (W * .3, H * .7), (W * .55, H * .45), (W * .85, H * .16)]
    art = leaves_along(art, W, H, tw, rng, nx, 7, 110, 150, pals=[LP, ("#8fb79b", "#24503b", "#10291d", "#93b89c")])
    art = camellia(art, W, H, W * .44, H * .52, 112, rng, nx, PAL, tilt=0.85, rings=(8, 7, 5), stamens=True)
    art = cam_bud(art, W, H, W * .86, H * .15, 24, -0.8, rng, nx, PAL, LP)
    return art


if "rangkaian" in PARTS:
    W, H = 1100, 620
    a = cluster(W, H, 7)
    prev(a, "kamelia-rangkaian", tone=BLUSH)
    save(a, f"{OUT}/rangkaian.webp", max_w=860, quality=80)
    clear()

if "setangkai" in PARTS:
    W, H = 640, 480
    a = sprig(W, H, 21)
    prev(a, "kamelia-setangkai", tone=BLUSH)
    save(a, f"{OUT}/setangkai.webp", max_w=480, quality=80)
    clear()

if "bunga" in PARTS:
    W, H = 420, 420
    rng = random.Random(5); nx = Seq(500)
    a = blank(W, H)
    for (L, ang) in [(150, -2.5), (150, -0.5), (140, 1.9)]:
        a = glossy_leaf(a, W, H, W / 2, H / 2, L + 40, ang, rng, nx, LP, gloss=0.5)
    a = camellia(a, W, H, W / 2, H / 2, 130, rng, nx, PAL, tilt=0.95, rings=(8, 7, 5), stamens=True)
    prev(a, "kamelia-bunga", tone=BLUSH)
    save(a, f"{OUT}/bunga.webp", max_w=300, quality=82)
    clear()

if "garis" in PARTS:
    W, H = 760, 150
    rng = random.Random(9); nx = Seq(900)
    a = blank(W, H)
    cx, cy = W / 2, H / 2
    a = twig(a, W, H, [(cx - 300, cy + 6), (cx - 150, cy - 2), (cx, cy), (cx + 150, cy - 2), (cx + 300, cy + 6)], 3.5, nx, *TWIG)
    for side in (-1, 1):
        a = glossy_leaf(a, W, H, cx + side * 30, cy, 96, (math.pi if side < 0 else 0) + side * -0.22, rng, nx, LP, wd=0.4)
        a = glossy_leaf(a, W, H, cx + side * 120, cy - 2, 70, (math.pi if side < 0 else 0) + side * 0.35, rng, nx, LP, wd=0.4)
    dots = circles(W, H, [(cx + sd * d, cy + 5 + (d % 3), 6.5 - d / 80) for sd in (-1, 1) for d in (210, 250, 284, 312)])
    a = FO(a, dots, "#c99a45", seed=nx(), emboss=0.5)
    a = cam_bud(a, W, H, cx, cy + 10, 26, -math.pi / 2, rng, nx, PAL, LP)
    prev(a, "kamelia-garis", tone=BLUSH)
    save(a, f"{OUT}/garis.webp", max_w=420, quality=82)
    clear()

if "kertas" in PARTS:
    W = H = 512
    p = np.asarray(paper(W, H, BLUSH, seed=11, fiber=0.6, mottle=0.4), np.float32) / 255
    m = tile_wrap(fbm(W, H, 4, 90, 3))
    rgb = p[..., :3] * (0.985 + 0.03 * m[..., None])
    # make it seamless
    sh = np.roll(np.roll(rgb, H // 2, 0), W // 2, 1)
    yy, xx = yx(W, H)
    k = np.clip(np.minimum(np.minimum(xx, W - 1 - xx) / (W / 2), np.minimum(yy, H - 1 - yy) / (H / 2)) * 1.6, 0, 1)[..., None]
    rgb = rgb * k + sh * (1 - k)
    save_rgb(np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/kertas.webp", quality=72)
