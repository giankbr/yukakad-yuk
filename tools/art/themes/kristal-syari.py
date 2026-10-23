"""Kristal Syari — clear faceted crystals and a prism throwing soft rainbow light on ivory; silver-grey watercolour,
spectral fringes, a faceted monogram ring and tiny glints. Run: python3 -I kristal-syari.py [part ...]
parts: cluster prism spill ring glint. Assets -> public/themes/art/kristal-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l3_lib import *

OUT = outdir("kristal-syari")
PARTS = sys.argv[1:] or ["cluster", "prism", "spill", "ring", "glint"]
GLASS, GLASS_D, SILVER, LINE = "#c4cfd9", "#8f9eae", "#a9b4bf", "#7b8794"
SPECTRUM = ["#f2a3ad", "#f5c59a", "#f0e29a", "#acdcb9", "#9fcbec", "#c3abe6"]


def rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def crystal(art, W, H, cx, cy, w, h, tip, ang, nx, fringe=True):
    """Hexagonal crystal point (three visible faces + pyramidal tip), lit from the upper left."""
    xs = [-w / 2, -w * 0.16, w * 0.24, w / 2]
    top = [-h, -h - w * 0.06, -h - w * 0.02, -h + w * 0.05]
    apex = (w * 0.05, -h - tip)
    base = [w * 0.03, w * 0.09, w * 0.06, 0]
    faces = []
    for i in range(3):
        faces.append(([(xs[i], base[i]), (xs[i], top[i]), (xs[i + 1], top[i + 1]), (xs[i + 1], base[i + 1])], [0.32, 0.1, 0.5][i]))
        faces.append(([(xs[i], top[i]), apex, (xs[i + 1], top[i + 1])], [0.22, 0.04, 0.42][i]))
    allm = np.zeros((H, W), np.float32)
    for k, (f, v) in enumerate(faces):
        m = shapes(W, H, [rot(f, cx, cy, ang)], smooth=False)
        allm = np.maximum(allm, m)
        art = G(art, m, GLASS, GLASS_D if v > 0.3 else GLASS, seed=nx(), density=0.12 + v * 1.25, edge=0.65, bloom=0.45, gran=0.15, rough=1.2, feather=0.8, pad=10)
        # inner refraction streak in the wider faces
        if k in (2, 4):
            a0, b0 = f[0], f[2]
            st = strokes(W, H, [(rot([(a0[0] * 0.6 + b0[0] * 0.4, (a0[1] + f[1][1]) * 0.5), (a0[0] * 0.3 + b0[0] * 0.7, f[1][1] * 0.8)], cx, cy, ang), w * 0.05, (0.3, 0.3))])
            art = soft(art, st * m, "#ffffff", alpha=0.85, blur=0.8, pad=6)
        if k in (0, 3):
            # light caught inside the crystal: a faint spectral patch
            c = np.mean(np.array(rot(f, cx, cy, ang)), 0)
            for j, col in enumerate(SPECTRUM[1:5]):
                sp = ellipses(W, H, [(c[0] + (j - 1.5) * w * 0.08, c[1] + h * 0.12, w * 0.07, h * 0.12, math.degrees(ang))])
                art = G(art, sp * m, col, seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=2, feather=3, pad=10)
    # edges: fine silver line work with a white catch-light on the lit edges
    edges = []
    for i in range(4):
        edges.append(rot([(xs[i], base[i]), (xs[i], top[i])], cx, cy, ang))
        edges.append(rot([(xs[i], top[i]), apex], cx, cy, ang))
    for i in range(3):
        edges.append(rot([(xs[i], top[i]), (xs[i + 1], top[i + 1])], cx, cy, ang))
    em = strokes(W, H, [(e, 1.5, (0.1, 0.1)) for e in edges])
    art = ink(art, em, LINE, alpha=0.75, rough=0.6, seed=nx())
    hi = strokes(W, H, [(rot([(xs[1] + 2, base[1] - 6), (xs[1] + 2, top[1] + 4)], cx, cy, ang), 1.6, (0.3, 0.3)), (rot([(xs[1] + 3, top[1] - 2), (apex[0] - 2, apex[1] + 8)], cx, cy, ang), 1.4, (0.2, 0.4))])
    art = soft(art, hi, "#ffffff", alpha=0.95, pad=4)
    if fringe:
        # spectral fringe along the shaded right edge
        for j, col in enumerate(SPECTRUM):
            off = xs[3] + 3 + j * 2.4
            fr = strokes(W, H, [(rot([(off, base[3] - h * 0.1), (off, top[3] + h * 0.2)], cx, cy, ang), 2.6, (0.4, 0.4))])
            art = G(art, fr, col, seed=nx(), density=0.85, edge=0.1, bloom=0, rough=1.2, feather=1.2, pad=6)
    return art, allm


if "cluster" in PARTS:
    W, H = 640, 720
    nx = Seq(51000)
    art = blank(W, H)
    # soft spectral pool under the cluster
    pool = ellipses(W, H, [(330, 650, 250, 40, -4)])
    for j, col in enumerate(SPECTRUM):
        band = ellipses(W, H, [(250 + j * 34, 650 + (j - 3) * 2, 56, 26, -4)])
        art = G(art, band, col, seed=nx(), density=0.35, edge=0.15, bloom=0.4, rough=6, feather=6)
    art = G(art, pool, "#b9c2cc", seed=nx(), density=0.2, edge=0.1, bloom=0.3, rough=6, feather=8)
    clear()
    specs = [(205, 646, 92, 300, 90, -0.4), (462, 652, 80, 230, 70, 0.42), (330, 664, 118, 430, 120, 0.05)]
    for (cx, cy, w, h, tip, ang) in specs:
        art, m = crystal(art, W, H, cx, cy, w, h, tip, ang, nx)
        clear()
    prev(art, "ks-cluster", bg=None)
    save(art, f"{OUT}/cluster.webp", max_w=440, quality=84)

if "prism" in PARTS:
    # divider: a small cut gem (crown + pavilion facets) between two tapering silver lines, spectrum on one side
    W, H = 640, 120
    nx = Seq(52000)
    art = blank(W, H)
    cx, cy = 320, 54
    ln = strokes(W, H, [([(40, cy + 4), (270, cy + 4)], 2.0, (0.9, 0.0)), ([(370, cy + 4), (600, cy + 4)], 2.0, (0.0, 0.9))])
    art = ink(art, ln, SILVER, alpha=0.8, rough=0.4, seed=nx())
    for j, col in enumerate(SPECTRUM):
        sp = strokes(W, H, [([(372, cy + 10 + j * 2.2), (520 - j * 8, cy + 10 + j * 2.2)], 2.4, (0.0, 0.9))])
        art = G(art, sp, col, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=1.2)
    crown = [(cx - 44, cy - 6), (cx - 26, cy - 26), (cx + 26, cy - 26), (cx + 44, cy - 6)]
    pav = (cx, cy + 50)
    faces = [([crown[0], crown[1], (cx - 10, cy - 6)], 0.2), ([crown[1], crown[2], (cx + 10, cy - 6), (cx - 10, cy - 6)], 0.05), ([crown[2], crown[3], (cx + 10, cy - 6)], 0.45),
             ([crown[0], (cx - 10, cy - 6), pav], 0.3), ([(cx - 10, cy - 6), (cx + 10, cy - 6), pav], 0.12), ([(cx + 10, cy - 6), crown[3], pav], 0.6)]
    for f, v in faces:
        art = G(art, shapes(W, H, [f], smooth=False), GLASS, GLASS_D if v > 0.3 else GLASS, seed=nx(), density=0.15 + v * 1.2, edge=0.6, bloom=0.3, rough=0.8, feather=0.6, pad=6)
    art = ink(art, strokes(W, H, [([crown[0], crown[1], crown[2], crown[3], pav, crown[0]], 1.3, None), ([crown[0], crown[3]], 1.0, None),
                                  ([crown[1], (cx - 10, cy - 6), pav], 0.9, None), ([crown[2], (cx + 10, cy - 6), pav], 0.9, None)]), LINE, alpha=0.75, rough=0.4, seed=nx())
    art = soft(art, strokes(W, H, [([(cx - 30, cy - 18), (cx - 14, cy - 22)], 1.6, (0.3, 0.3)), ([(cx - 20, cy + 2), (cx - 6, cy + 30)], 1.3, (0.3, 0.3))]), "#ffffff", alpha=0.95, pad=4)
    prev(art, "ks-prism", bg=None)
    save(art, f"{OUT}/prism.webp", max_w=320, quality=84)

if "spill" in PARTS:
    # rainbow light spill: diagonal pastel bands, very soft, for cover/section backgrounds
    W, H = 800, 520
    nx = Seq(53000)
    art = blank(W, H)
    for j, col in enumerate(SPECTRUM):
        y0 = 120 + j * 34
        band = shapes(W, H, [[(-40, y0 + 160), (840, y0 - 160), (840, y0 - 120), (-40, y0 + 200)]], smooth=False)
        art = G(art, band, col, seed=nx(), density=0.42, edge=0.12, bloom=0.5, rough=10, feather=10, gran=0.1, pad=30)
        clear()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(1 - np.abs(xx - 420) / 420, 0, 1) ** 0.8
    art[..., 3] *= fade
    prev(art, "ks-spill", bg="#f7f4ee")
    save_full(art, f"{OUT}/spill.webp", size=(560, 364), quality=80)

if "ring" in PARTS:
    # faceted crystal ring (octagon of cut facets) for monograms
    W = H = 460
    nx = Seq(54000)
    cx = cy = 230
    art = blank(W, H)
    R1, R2 = 220, 176
    n = 6
    for i in range(n):
        a0 = (i - 0.5) * math.tau / n - math.pi / 2
        a1 = (i + 0.5) * math.tau / n - math.pi / 2
        p0o, p1o = (cx + R1 * math.cos(a0), cy + R1 * math.sin(a0)), (cx + R1 * math.cos(a1), cy + R1 * math.sin(a1))
        p0i, p1i = (cx + R2 * math.cos(a0), cy + R2 * math.sin(a0)), (cx + R2 * math.cos(a1), cy + R2 * math.sin(a1))
        mo = ((cx + (R1 + R2) / 2 * math.cos((a0 + a1) / 2)), (cy + (R1 + R2) / 2 * math.sin((a0 + a1) / 2)))
        lightness = 0.5 + 0.5 * math.cos((a0 + a1) / 2 + math.pi * 0.75)
        outer_f = shapes(W, H, [[p0o, p1o, mo]], smooth=False)
        inner_f = shapes(W, H, [[p0i, p1i, mo]], smooth=False)
        side_a = shapes(W, H, [[p0o, mo, p0i]], smooth=False)
        side_b = shapes(W, H, [[p1o, mo, p1i]], smooth=False)
        for m, v in ((outer_f, 0.15 + 0.4 * (1 - lightness)), (inner_f, 0.35 + 0.3 * lightness), (side_a, 0.25), (side_b, 0.45)):
            art = G(art, m, GLASS, GLASS_D, seed=nx(), density=0.2 + v * 0.8, edge=0.5, bloom=0.4, gran=0.12, rough=1, feather=0.7, pad=8)
        art = ink(art, strokes(W, H, [([p0o, p1o, p1i, p0i, p0o], 1.4, None), ([p0o, mo, p1i], 1.0, None), ([p1o, mo, p0i], 1.0, None)]), LINE, alpha=0.6, rough=0.5, seed=nx())
        clear()
    # rainbow fringe on the lower-right outer edge
    for j, col in enumerate(SPECTRUM):
        arc = arc_pts(cx, cy, R1 + 5 + j * 2.6, 0.1, 1.3, 20)
        art = G(art, strokes(W, H, [(arc, 2.6, (0.4, 0.4))]), col, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1, feather=1)
    hi = strokes(W, H, [(arc_pts(cx, cy, R1 - 8, math.pi * 1.1, math.pi * 1.45, 12), 2, (0.3, 0.3))])
    art = soft(art, hi, "#ffffff", alpha=0.95, pad=4)
    prev(art, "ks-ring", bg="#f7f4ee")
    save(art, f"{OUT}/ring.webp", max_w=300, quality=84)

if "glint" in PARTS:
    # a tiny refracted glint: soft four-point star with a faint spectral halo
    W = H = 128
    nx = Seq(55000)
    art = blank(W, H)
    halo = circles(W, H, [(64, 64, 26)])
    art = soft(art, halo, "#cfe2f4", alpha=0.35, blur=10, pad=10)
    star = shapes(W, H, [[(64, 8), (69, 59), (120, 64), (69, 69), (64, 120), (59, 69), (8, 64), (59, 59)]], smooth=False)
    art = soft(art, star, "#ffffff", alpha=1.0, blur=1.2, pad=6)
    art = soft(art, circles(W, H, [(64, 64, 6)]), "#ffffff", alpha=1, blur=2, pad=6)
    prev(art, "ks-glint", bg="#9aa6b2")
    save_full(art, f"{OUT}/glint.webp", size=(64, 64), quality=84)
