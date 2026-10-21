"""Wayang Mega — no-photo theme on sand/kraft: Cirebon-style mega mendung clouds (graded gouache bands + ink line),
a pair of original wayang-kulit figures in gouache on leather with gilt, tumpal batik border, monogram medallion.
Run: python3 -I wayang-mega.py [part ...]  parts: mega wayang border medallion. Assets -> public/themes/art/wayang-mega/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *
import _jw_lib as jw
from scipy.ndimage import distance_transform_edt

OUT = outdir("wayang-mega")
PARTS = sys.argv[1:] or ["mega", "wayang", "border", "medallion"]
SAND = "#e6d8b8"
TERRA, TERRA_D, SOGAN, CREAM = "#b4532f", "#6e2c17", "#7a4a26", "#f3e7cf"
GOLD = "#c9a14a"


def mega(W, H, spine, radii, tail, nx, cols, seed=1):
    """Mega mendung cloud: union of lobes along a spine + curled tail, filled with graded bands and inked outlines."""
    lobes = [(x, y, r) for (x, y), r in zip(spine, radii)]
    base = circles(W, H, lobes)
    tx, ty, tr = tail
    base = np.maximum(base, strokes(W, H, [(spiral_pts(tx, ty, tr, tr * 0.12, 0, 1.25, 50, -1), tr * 0.5, (0.0, 0.7))]))
    base = np.maximum(base, strokes(W, H, [(curve([spine[-1], ((spine[-1][0] + tx) / 2, (spine[-1][1] + ty) / 2 + 8), (tx, ty + tr)], 20), radii[-1] * 0.8, (0.0, 0.9))]))
    base = (gaussian_filter(base, 1.5) > 0.5).astype(np.float32)
    d = distance_transform_edt(base)
    step = max(radii) / 6.5
    art = blank(W, H)
    nb = len(cols)
    for i in range(nb):
        band = ((d > i * step) & (d <= (i + 1) * step) if i < nb - 1 else (d > i * step)).astype(np.float32)
        art = OV(art, gaussian_filter(band, 0.6), lambda q, c=cols[i], k=i: gouache_paint(q, c, mix(c, "#000000", 0.08), seed=seed * 10 + k, rough=1.0, streak=0.7))
    lines = np.zeros_like(d)
    for i in range(nb):
        lines = np.maximum(lines, np.clip(1 - np.abs(d - i * step) / 1.1, 0, 1))
    lines *= base
    art = G(art, lines, "#3b1a0e", seed=nx(), density=0.8, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    return art


if "mega" in PARTS:
    nx = Seq(9500)
    cols = [TERRA_D, "#8f3b1e", TERRA, "#cf7a4f", "#e6a97f", "#f1d1b0", CREAM]
    W, H = 640, 300
    sp = [(60, 190), (130, 150), (210, 130), (290, 140), (360, 170), (420, 200)]
    a = mega(W, H, sp, [62, 70, 74, 66, 56, 40], (520, 180, 46), nx, cols, 1)
    preview(a, "wm-mega-a", SAND)
    save(a, f"{OUT}/mega-a.webp", max_w=560, quality=80)
    W, H = 520, 240
    sp = [(60, 150), (120, 120), (190, 112), (250, 130), (300, 160)]
    b = mega(W, H, sp, [48, 56, 58, 48, 32], (390, 140, 36), nx, ["#5f5330", "#7c6e40", "#9e8c56", "#c4b27a", "#e4d6a8", CREAM], 2)
    preview(b, "wm-mega-b", SAND)
    save(b, f"{OUT}/mega-b.webp", max_w=420, quality=80)

if "wayang" in PARTS:
    for kind, face, name in [("putra", 1, "putra"), ("putri", -1, "putri")]:
        W, H = 260, 640
        nx = Seq(9600 if kind == "putra" else 9700)
        m = jw.wayang_masks(W, H, 20, 24, 2.2, kind, face)
        solid = np.clip(m["body"] - m["holes"], 0, 1)
        art = blank(W, H)
        art = GP(art, m["sticks"], "#5a3a22", "#3a2414", seed=nx(), rough=0.6, pad=8)
        art = GP(art, solid, "#c99a62", "#9a6a3a", seed=nx(), rough=1.4, streak=0.9, pad=12)
        kain = m["kain"] * solid
        art = GP(art, kain, "#9a3a22" if kind == "putra" else "#2f5a4a", "#6e2416" if kind == "putra" else "#1f3e33", seed=nx(), rough=1.2, pad=10)
        # painted cawi (fine line work) on the kain and torso
        cw = jw.hatch(W, H, 0.8, 5.0, 0.18, nx()) * kain
        art = G(art, cw, GOLD, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.4)
        art = GP(art, m["face"], "#1f140d", seed=nx(), rough=0.6, pad=8)
        art = FO(art, np.maximum(m["crown"] * solid, m["trim"]), GOLD, seed=nx(), sparkle=0.06)
        art = G(art, solid * fbm(W, H, 3, 30, 3), "#4a2a14", seed=nx(), density=0.22, edge=0.2, bloom=0.3, rough=2)
        preview(art, f"wm-{name}", SAND)
        save(art, f"{OUT}/{name}.webp", max_w=230, quality=82)

if "border" in PARTS:
    # tumpal: seamless strip of tall triangles filled with little lung motifs, sogan + terracotta on cream
    W, H = 240, 72
    nx = Seq(9800)
    tri, inner, dots_ = [], [], []
    for k in range(-1, 7):
        x = k * 40
        tri.append([(x, H - 6), (x + 40, H - 6), (x + 20, 6)])
        inner.append([(x + 9, H - 12), (x + 31, H - 12), (x + 20, 22)])
        dots_ += [(x + 20, H - 22, 3), (x + 20, 36, 2), (x, 12, 2.4)]
    t = shapes(W, H, tri, smooth=False); i_ = shapes(W, H, inner, smooth=False)
    art = blank(W, H)
    art = OV(art, np.clip(t - i_, 0, 1), lambda q: linocut(q, SOGAN, seed=3, wear=0.2, rough=0.6))
    art = OV(art, i_, lambda q: linocut(q, TERRA, seed=4, wear=0.25, rough=0.6))
    art = OV(art, circles(W, H, dots_), lambda q: linocut(q, CREAM if True else SOGAN, seed=5, wear=0.1, rough=0.3))
    edge = shapes(W, H, [[(0, H - 5), (W, H - 5), (W, H), (0, H)], [(0, 0), (W, 0), (W, 3), (0, 3)]], smooth=False)
    art = OV(art, edge, lambda q: linocut(q, SOGAN, seed=6, wear=0.1, rough=0.3))
    save_full(art, f"{OUT}/border.webp", quality=82)
    preview(art, "wm-border", SAND)

if "medallion" in PARTS:
    W, H = 420, 420
    nx = Seq(9900); cx = cy = 210
    ring = np.clip(circles(W, H, [(cx, cy, 196)]) - circles(W, H, [(cx, cy, 150)]), 0, 1)
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along(arc_pts(cx, cy, 173, 0, math.tau, 140), 46)):
        it, lv = jw.lung(x, y, 24, a, 1); items += it; leaves += lv
    art = jw.carve(W, H, ring, items, leaves, nx, base=SOGAN, light="#b07a48", dark="#4a2814", gold=GOLD, gold_amt=0.5, seed=4)
    inner = np.clip(circles(W, H, [(cx, cy, 146)]) - circles(W, H, [(cx, cy, 140)]), 0, 1)
    art = FO(art, inner, GOLD, seed=nx())
    preview(art, "wm-medallion", SAND)
    save(art, f"{OUT}/medallion.webp", max_w=300, quality=82)
