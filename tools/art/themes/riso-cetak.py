"""Riso Cetak — risograph print: two spot inks (fluorescent pink + blue) as separate plates with AM halftone dots,
misregistration offsets, soy-ink grain and roller starvation; overprints multiply to violet. Run: python3 -I riso-cetak.py
parts: bloom seal squiggle blob paper. Assets -> public/themes/art/riso-cetak/ (use with mix-blend-mode: multiply)"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b4_lib import *

OUT = outdir("riso-cetak")
PARTS = sys.argv[1:] or ["bloom", "seal", "squiggle", "blob", "paper"]
PINK = "#ff48b0"
BLUE = "#0078bf"
PAPER = "#f6f1e7"


def press(W, H, pink, blue, seed, off=(5, -3)):
    """Print the two plates (pink first, blue shifted = misregistration) and stack them as multiply."""
    pl = riso_ink(pink, PINK, seed, grain=0.32, starve=0.28)
    bl = riso_ink(shift(blue, *off), BLUE, seed + 50, grain=0.3, starve=0.22)
    return multiply_stack([pl, bl], W, H)


def daisy(W, H, cx, cy, r, n, rot=0.0, inner=0.32, fat=0.62):
    items = []
    for k in range(n):
        a = rot + k * math.tau / n
        items.append((cx + math.cos(a) * r * 0.56, cy + math.sin(a) * r * 0.56, r * 0.45, r * 0.19 * fat / 0.62, math.degrees(a)))
    return ellipses(W, H, items)


def rprev(arr, name):
    h, w = arr.shape[:2]
    base = rgb_arr(h, w, PAPER)
    a = arr[..., 3:4]
    rgb = base * (1 - a + a * arr[..., :3])
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


if "bloom" in PARTS:
    W, H = 760, 760
    rng = random.Random(51)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = 380, 380
    # pink plate: big halftone disc fading from bottom-left (solid) to top-right (fine dots) + solid daisy centre
    disc = circles(W, H, [(cx + 40, cy - 30, 300)])
    grad = np.clip(((W - xx) * 0.55 + yy * 0.45) / W * 1.25 - 0.15, 0, 1)
    pink = halftone(grad * disc, cell=11, angle=0.26, rough=0.12, seed=3) * disc
    petals = daisy(W, H, cx - 30, cy + 40, 250, 9, rot=0.2, inner=0.22, fat=0.9)
    centre = circles(W, H, [(cx - 30, cy + 40, 62)])
    # blue plate: flower outline-ish petals as flat ink with a halftone shadow, centre ring and small dots
    petal_line = np.clip(petals - shift(gaussian_filter(petals, 0.5), 0, 0) * 0, 0, 1)
    edge = np.clip(petals - ndimage.binary_erosion(petals > 0.5, iterations=7).astype(np.float32), 0, 1)
    shade = halftone(np.clip((yy - (cy - 200)) / 500, 0, 1) * 0.55 * petals, cell=7, angle=1.31, seed=5) * petals
    ring = np.clip(circles(W, H, [(cx - 30, cy + 40, 62)]) - circles(W, H, [(cx - 30, cy + 40, 44)]), 0, 1)
    seeds = circles(W, H, [(cx - 30 + math.cos(a) * d, cy + 40 + math.sin(a) * d, 4.2) for d, a in [(rng.uniform(0, 34), rng.uniform(0, math.tau)) for _ in range(22)]])
    blue = np.maximum.reduce([edge, shade, ring, seeds])
    pink = np.maximum(pink * (1 - petals * 0.7), centre)
    art = press(W, H, pink, blue, 61, off=(7, -5))
    rprev(art, "rc-bloom")
    save(art, f"{OUT}/bloom.webp", max_w=420, quality=74)
    clear()

if "seal" in PARTS:
    # scalloped stamp seal: pink solid with blue ring of halftone, misregistered
    W, H = 300, 300
    cx, cy, n = 150, 150, 14
    pts = []
    for i in range(n * 12):
        a = i / (n * 12) * math.tau
        r = 120 + 9 * math.cos(a * n)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    sealm = shapes(W, H, [pts], smooth=False)
    ring = np.clip(circles(W, H, [(cx, cy, 96)]) - circles(W, H, [(cx, cy, 90)]), 0, 1)
    tone = halftone(np.full((H, W), 0.42, np.float32), cell=6, angle=0.79, seed=7) * circles(W, H, [(cx, cy, 86)])
    art = press(W, H, sealm, np.maximum(ring, tone), 71, off=(4, 3))
    rprev(art, "rc-seal")
    save(art, f"{OUT}/seal.webp", max_w=150, quality=82)

if "squiggle" in PARTS:
    W, H = 720, 90
    p = [(x, 45 + math.sin(x / 34) * 18) for x in np.linspace(20, W - 20, 200)]
    pink = strokes(W, H, [(p, 9, (0.03, 0.03))])
    dots = circles(W, H, [(x, 45 + math.sin(x / 34 + math.pi) * 18, 3.4) for x in np.linspace(40, W - 40, 26)])
    art = press(W, H, pink, dots, 81, off=(3, -2))
    rprev(art, "rc-squiggle")
    save(art, f"{OUT}/squiggle.webp", max_w=360, quality=84)

if "blob" in PARTS:
    # organic blob in blue halftone with a pink offset outline (behind portraits)
    W, H = 560, 640
    rng = random.Random(52)
    pts = []
    for i in range(14):
        a = i / 14 * math.tau
        r = 220 * (1 + 0.12 * math.sin(a * 3 + 0.6) + rng.uniform(-0.05, 0.05))
        pts.append((280 + math.cos(a) * r * 1.0, 320 + math.sin(a) * r * 1.18))
    m = shapes(W, H, [pts])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    blue = halftone(np.clip((xx + yy) / (W + H) * 1.1, 0, 1) * 0.85 * m, cell=10, angle=0.26, rough=0.1, seed=9) * m
    edge = np.clip(m - ndimage.binary_erosion(m > 0.5, iterations=6).astype(np.float32), 0, 1)
    art = press(W, H, shift(edge, -16, 14), blue, 91, off=(0, 0))
    rprev(art, "rc-blob")
    save(art, f"{OUT}/blob.webp", max_w=280, quality=80)
    clear()

if "paper" in PARTS:
    n = 400
    base = rgb_arr(n, n, PAPER) * (0.975 + 0.05 * wrap_noise(n, n, 11, 30))[..., None]
    fib = wrap_noise(n, n, 12, 0.5)
    base *= (1 + (fib - 0.5) * 0.06)[..., None]
    # stray ink specks from the drum (both colours)
    rng = np.random.default_rng(13)
    for col, k in ((PINK, 60), (BLUE, 45)):
        sp = np.zeros((n, n), np.float32)
        ys, xs = rng.integers(0, n, k), rng.integers(0, n, k)
        sp[ys, xs] = 1
        sp = np.clip(gaussian_filter(sp, 0.7) * 5, 0, 1) * 0.35
        base = base * (1 - sp[..., None] + sp[..., None] * np.array(hex_rgb(col), np.float32))
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/paper.webp", quality=74)
