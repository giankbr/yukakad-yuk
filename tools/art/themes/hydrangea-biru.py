"""Hydrangea Biru — lush blue-violet mophead hydrangeas built from hundreds of four-petal watercolour florets, sage
serrated leaves, and a dusty-blue silk ribbon with a painted sheen. Run: python3 -I hydrangea-biru.py [part ...]
parts: spray posy bloom sprig ribbon bow paper. Assets -> public/themes/art/hydrangea-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b4_lib import *

OUT = outdir("hydrangea-biru")
PARTS = sys.argv[1:] or ["spray", "posy", "bloom", "sprig", "ribbon", "bow", "paper"]
BG = "#f4f6fa"
# rim (deep) .. centre (pale): cobalt, periwinkle, violet, lilac, mist
BLUE = ["#dfe6f6", "#b3c3ea", "#93a8e0", "#7b8fd2", "#6170c0", "#4a57a3"]
VIOLET = ["#ddd3ef", "#c4b3e4", "#a994d4", "#9180c6", "#7564b0", "#5c4f98"]
MIXED = ["#e4e3f5", "#c3c4ec", "#a7a3dc", "#8c96d6", "#7a6fc0", "#56609f"]
LEAF = ("#8aa59a", "#5f817c", "#40615d")
RIB = dict(col="#a9bbdc", deep="#6b7fae", light="#f4f7fd")


def cl(art, W, H, nx, rng, x, y, R, pal, tilt=0.82):
    art = hydrangea(art, W, H, x, y, R, rng, nx, pal, tilt=tilt, fr=R * 0.16)
    clear()
    return art


def leaves(art, W, H, nx, rng, specs):
    for (x, y, L, a) in specs:
        art = serrated_leaf(art, W, H, x, y, L, a, rng, nx, ca=LEAF[0], cb=LEAF[1], vein=LEAF[2])
    return art


if "spray" in PARTS:
    # top-left corner arrangement spilling over the photo
    W, H = 760, 640
    nx = Seq(40100); rng = random.Random(41)
    art = blank(W, H)
    art = leaves(art, W, H, nx, rng, [(250, 230, 250, 0.35), (210, 260, 220, 1.35), (330, 200, 200, -0.25), (150, 170, 190, 2.4), (420, 330, 170, 0.75)])
    art = cl(art, W, H, nx, rng, 200, 190, 165, BLUE)
    art = cl(art, W, H, nx, rng, 420, 150, 110, VIOLET)
    art = cl(art, W, H, nx, rng, 120, 400, 105, MIXED)
    art = leaves(art, W, H, nx, rng, [(470, 230, 150, 0.55), (300, 330, 140, 1.1)])
    preview(art, "hb-spray", tone=BG)
    save(art, f"{OUT}/spray.webp", max_w=420, quality=80)
    clear()

if "posy" in PARTS:
    # bottom posy with a ribbon trailing to the left
    W, H = 760, 560
    nx = Seq(40200); rng = random.Random(42)
    art = blank(W, H)
    spine = curve([(560, 360), (430, 420), (300, 380), (190, 470), (60, 440)], 120)
    m, sh, sd = ribbon_band(W, H, spine, 20, twist_freq=1.6, phase=0.4)
    art = silk(art, m, sh, sd, nx, **RIB)
    spine2 = curve([(560, 380), (500, 470), (420, 520), (330, 540)], 90)
    m, sh, sd = ribbon_band(W, H, spine2, 17, twist_freq=1.1, phase=1.2)
    art = silk(art, m, sh, sd, nx, **RIB)
    clear()
    art = leaves(art, W, H, nx, rng, [(560, 330, 210, -2.6), (590, 330, 200, -1.6), (520, 320, 170, 2.9), (610, 300, 160, -0.6)])
    art = cl(art, W, H, nx, rng, 570, 240, 150, VIOLET)
    art = cl(art, W, H, nx, rng, 410, 290, 95, BLUE)
    art = cl(art, W, H, nx, rng, 690, 330, 70, MIXED)
    preview(art, "hb-posy", tone=BG)
    save(art, f"{OUT}/posy.webp", max_w=400, quality=80)
    clear()

if "bloom" in PARTS:
    W, H = 460, 420
    nx = Seq(40300); rng = random.Random(43)
    art = blank(W, H)
    art = leaves(art, W, H, nx, rng, [(215, 240, 205, 2.6), (245, 240, 195, 0.45), (232, 262, 140, 1.8)])
    art = cl(art, W, H, nx, rng, 230, 190, 150, MIXED)
    preview(art, "hb-bloom", tone=BG)
    save(art, f"{OUT}/bloom.webp", max_w=260, quality=82)
    clear()

if "sprig" in PARTS:
    # small single cluster for timeline nodes / portrait corners
    W, H = 220, 220
    nx = Seq(40400); rng = random.Random(44)
    art = blank(W, H)
    art = leaves(art, W, H, nx, rng, [(110, 120, 72, 0.45), (110, 120, 64, 2.7)])
    art = cl(art, W, H, nx, rng, 110, 100, 70, BLUE)
    preview(art, "hb-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=110, quality=84)

if "ribbon" in PARTS:
    # divider: silk ribbon flowing through a single floret knot
    W, H = 720, 150
    nx = Seq(40500); rng = random.Random(45)
    art = blank(W, H)
    for side in (-1, 1):
        spine = curve([(W / 2, 74), (W / 2 + side * 90, 50), (W / 2 + side * 180, 98), (W / 2 + side * 270, 62), (W / 2 + side * 340, 80)], 120)
        m, sh, sd = ribbon_band(W, H, spine, 11, twist_freq=1.5, phase=0.6 if side > 0 else 2.0)
        art = silk(art, m, sh, sd, nx, **RIB)
    clear()
    art = cl(art, W, H, nx, rng, W / 2, 72, 40, BLUE, tilt=0.9)
    preview(art, "hb-ribbon", tone=BG)
    save(art, f"{OUT}/ribbon.webp", max_w=360, quality=82)

if "bow" in PARTS:
    W, H = 420, 300
    nx = Seq(40600); rng = random.Random(46)
    art = blank(W, H)
    cx, cy = W / 2, 110
    loops = [curve([(cx, cy), (cx - 70, cy - 70), (cx - 150, cy - 40), (cx - 120, cy + 20), (cx, cy)], 100),
             curve([(cx, cy), (cx + 75, cy - 65), (cx + 150, cy - 30), (cx + 115, cy + 25), (cx, cy)], 100)]
    tails = [curve([(cx, cy), (cx - 30, cy + 70), (cx - 80, cy + 120), (cx - 110, cy + 175)], 80),
             curve([(cx, cy), (cx + 25, cy + 80), (cx + 70, cy + 130), (cx + 90, cy + 180)], 80)]
    for i, sp in enumerate(tails + loops):
        m, sh, sd = ribbon_band(W, H, sp, 15 if i < 2 else 18, twist_freq=0.8 + 0.3 * i, phase=0.3 * i)
        art = silk(art, m, sh, sd, nx, **RIB)
    knot = ellipses(W, H, [(cx, cy, 17, 14, 15)])
    art = silk(art, knot, gaussian_filter(ellipses(W, H, [(cx - 4, cy - 4, 7, 5, 15)]), 2), np.zeros_like(knot), nx, **RIB)
    preview(art, "hb-bow", tone=BG)
    save(art, f"{OUT}/bow.webp", max_w=200, quality=84)

if "paper" in PARTS:
    n = 420
    base = rgb_arr(n, n, BG) * (0.975 + 0.05 * wrap_noise(n, n, 5, 46))[..., None] * (1 + (wrap_noise(n, n, 6, 0.6) - 0.5) * 0.05)[..., None]
    tint = wrap_noise(n, n, 7, 70)[..., None]
    base = base * (1 - tint * 0.025) + np.array(hex_rgb("#dfe5f4"), np.float32) * tint * 0.025
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/paper.webp", quality=70)
