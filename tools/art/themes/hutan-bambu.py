"""Hutan Bambu — a towering bamboo grove in gouache + watercolour: tall culms with nodes and powdery rings (green with
one golden striped culm), leaf sprays, slanting light shafts, falling leaves, a misty far grove.
Run: python3 -I hutan-bambu.py [part ...]   parts: stand canopy rays sprig leaves grove
Assets -> public/themes/art/hutan-bambu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f5_lib import *  # noqa

OUT = outdir("hutan-bambu")
PARTS = sys.argv[1:] or ["stand", "canopy", "rays", "sprig", "leaves", "grove"]
BG = "#f1f0de"
G1, G2, GD, GL, GN = "#5f8436", "#7c9c40", "#304a1f", "#c7d77c", "#26391a"
Y1, Y2, YD, YL = "#cfae46", "#dcc05a", "#8a7224", "#f5e39a"
FAR, FAR2 = "#9fb88a", "#b9c99a"
LEAVES = ["#5d8a34", "#7ba545", "#4c7530", "#93b356"]
LEAVES_PALE = ["#9dbb78", "#b3c98d", "#8aaa6e"]


def nodes_for(y0, y1, step, rng):
    out, y = [], y0 - rng.uniform(40, step)
    while y > y1:
        out.append(y)
        y -= step * rng.uniform(0.85, 1.15)
    return out


if "stand" in PARTS:
    W, H = 440, 1640
    nx = Seq(30100); rng = random.Random(301)
    art = blank(W, H)
    # far, pale culms (wash)
    for x, wd in ((330, 18), (250, 14), (60, 16)):
        art, _ = culm(art, W, H, x, x + rng.uniform(-10, 10), H + 10, -10, wd, nodes_for(H, 0, 150, rng), nx, FAR, FAR2, "#7f9a70", "#e6eccd", "#6f8a62", wash=True, alpha=0.7)
    # mid golden striped culm
    art, gm = culm(art, W, H, 190, 214, H + 10, -10, 44, nodes_for(H, 0, 170, rng), nx, Y1, Y2, YD, YL, "#6d5a1c", stripe="#5f8436")
    # near green culms
    art, m1 = culm(art, W, H, 92, 120, H + 10, -10, 62, nodes_for(H, 0, 190, rng), nx, G1, G2, GD, GL, GN, lean=-6)
    art, m2 = culm(art, W, H, 340, 318, H + 10, -10, 50, nodes_for(H, 0, 175, rng), nx, G2, G1, GD, GL, GN, lean=5)
    # branch stubs and leaf sprays at upper nodes
    for (bx, by, ang, n) in ((118, 300, -0.5, 5), (330, 420, -2.4, 4), (210, 560, -0.3, 4), (110, 740, -2.7, 3), (330, 180, -0.9, 5), (200, 90, -2.2, 4)):
        twig = strokes(W, H, [(curve([(bx, by), (bx + math.cos(ang) * 40, by + math.sin(ang) * 40 + 10), (bx + math.cos(ang) * 80, by + math.sin(ang) * 80 + 6)], 16), 3.5, (0.0, 0.4))])
        art = GP(art, twig, "#6b6a2c", "#8a7a36", seed=nx(), rough=0.5)
        tx, ty = bx + math.cos(ang) * 80, by + math.sin(ang) * 80 + 6
        art = leaf_spray(art, W, H, tx, ty, ang + 1.2 if math.cos(ang) > 0 else ang - 1.2, n, 120, 13, nx, rng, LEAVES, droop=0.6)
        clear()
    preview(art, "hb-stand", tone=BG)
    save(art, f"{OUT}/stand.webp", max_w=230, quality=80)
    clear()

if "canopy" in PARTS:
    W, H = 900, 380
    nx = Seq(30200); rng = random.Random(302)
    art = blank(W, H)
    # pale far layer then rich near sprays hanging from the top edge
    for i in range(9):
        x = rng.uniform(20, W - 20); y = rng.uniform(-10, 90)
        art = leaf_spray(art, W, H, x, y, math.pi / 2 + rng.uniform(-0.6, 0.6), rng.randint(3, 5), 130, 14, nx, rng, LEAVES_PALE, alpha=0.6)
    clear()
    for i in range(12):
        x = rng.uniform(10, W - 10); y = rng.uniform(-6, 60)
        art = leaf_spray(art, W, H, x, y, math.pi / 2 + rng.uniform(-0.8, 0.8), rng.randint(3, 6), 150, 16, nx, rng, LEAVES)
        if i % 3 == 2:
            clear()
    # a few golden sun-touched leaves
    for i in range(4):
        x = rng.uniform(60, W - 60); y = rng.uniform(40, 120)
        art = leaf_spray(art, W, H, x, y, math.pi / 2 + rng.uniform(-0.5, 0.5), 2, 110, 12, nx, rng, ["#c9b04a", "#d8c062"], alpha=0.85)
    preview(art, "hb-canopy", tone=BG)
    save(art, f"{OUT}/canopy.webp", max_w=780, quality=78)
    clear()

if "rays" in PARTS:
    W, H = 400, 640
    nx = Seq(30300); rng = random.Random(303)
    art = blank(W, H)
    for (x, wd, a) in ((60, 70, 0.5), (170, 40, 0.38), (250, 90, 0.42), (360, 50, 0.3)):
        top = [(x - wd / 2, -20), (x + wd / 2, -20), (x + wd * 1.2 - 180, H + 20), (x - wd * 1.2 - 180, H + 20)]
        m = shapes(W, H, [top], smooth=False)
        m = gaussian_filter(m, 14) * (1 - np.linspace(0, 1, H)[:, None] * 0.75)
        streak = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (24, 2))
        streak = (streak - streak.min()) / (streak.max() - streak.min())
        art = over(art, col_arr(m, "#fff3c2", np.clip(m * a * (0.7 + 0.6 * streak), 0, 1)))
    preview(art, "hb-rays", bg="#4c6a3a")
    save_full(art, f"{OUT}/rays.webp", quality=70)
    clear()

if "sprig" in PARTS:
    W, H = 340, 140
    nx = Seq(30400); rng = random.Random(304)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(30, 96), (120, 84), (220, 80), (310, 70)], 30), 4.5, (0.05, 0.5))])
    art = GP(art, stem, "#7b7a32", "#9a8c3e", seed=nx(), rough=0.4)
    art = crayon(art, strokes(W, H, [([(118, 78), (118, 92)], 2, None), ([(218, 72), (218, 88)], 2, None)]), GN, seed=nx(), amt=0.8)
    art = leaf_spray(art, W, H, 120, 84, -0.5, 3, 92, 11, nx, rng, LEAVES, droop=0)
    art = leaf_spray(art, W, H, 220, 80, 0.55, 3, 88, 10, nx, rng, LEAVES, droop=0)
    art = leaf_spray(art, W, H, 306, 70, -0.15, 2, 70, 9, nx, rng, ["#c9b04a", "#7ba545"], droop=0)
    preview(art, "hb-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=220, quality=82)
    clear()

if "leaves" in PARTS:
    for name, cols, seed in (("leaf", ["#6f9a3c", "#88ad4a"], 30500), ("leaf2", ["#c7a845", "#d9bf62"], 30600)):
        W, H = 220, 80
        nx = Seq(seed); rng = random.Random(seed)
        art = blank(W, H)
        pts = bamboo_leaf_pts(14, 44, 196, 18, -0.08, 0.06)
        m = shapes(W, H, [pts])
        art = G(art, m, cols[0], cols[1], seed=nx(), density=0.88, edge=0.6, bloom=0.25, rough=1.0, feather=0.6)
        rib = strokes(W, H, [(leaf_rib(14, 44, 196, -0.08, 0.06), 1.6, (0.1, 0.5))])
        art = OV(art, rib * m, lambda mm: col_arr(mm, "#f6f1c8", mm * 0.4), pad=4)
        preview(art, f"hb-{name}", tone=BG)
        save(art, f"{OUT}/{name}.webp", max_w=110, quality=84)
        clear()

if "grove" in PARTS:
    W, H = 780, 760
    nx = Seq(30700); rng = random.Random(307)
    art = painted_sky(W, H, [(0, "#e9eccf"), (0.45, "#cfdcae"), (1, "#7f9d62")], seed=nx(), streak=0.8)
    # three depth rows of culms, fading into mist
    rows = ((0.5, 8, 16, "#a8bf8e", "#bccca0", 22), (0.75, 7, 26, "#7f9f62", "#94b06c", 14), (1.0, 5, 40, "#55783a", "#6f8f44", 10))
    for k, (a, n, wd, c, c2, mist_amt) in enumerate(rows):
        xs = sorted(rng.uniform(0, W) for _ in range(n))
        for x in xs:
            w_ = wd * rng.uniform(0.8, 1.2)
            art, _ = culm(art, W, H, x, x + rng.uniform(-14, 14), H + 10, -10, w_, nodes_for(H, 0, 120 + k * 40, rng), nx, c, c2, mix(c, "#1d2a14", 0.4), "#eef0d2", mix(c, "#1d2a14", 0.5), wash=k < 2, alpha=a)
            clear()
        art = mist(art, W, H, [(W * 0.5, H * (0.55 + 0.12 * k), W * 0.7, 60, 0.35)], col="#eef0dc", seed=nx())
    for i in range(6):
        art = leaf_spray(art, W, H, rng.uniform(0, W), rng.uniform(-10, 60), math.pi / 2 + rng.uniform(-0.7, 0.7), 4, 120, 13, nx, rng, LEAVES, alpha=0.9)
        clear()
    art = add_grain(art, nx(), 0.03)
    preview(art, "hb-grove", tone=BG)
    save_rgb(art, f"{OUT}/grove.webp", size=(780, 760), quality=72)
    clear()
