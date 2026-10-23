"""Mustard Syari — warm autumn watercolour: ginkgo fans in mustard and ochre, rust leaves with dark midribs, dried grasses
with seed heads and a few olive sprigs, all on cream. Pieces: a crescent garland for the cover top, a low corner cluster,
a ginkgo wreath for the monogram, a grass sprig divider, a single ginkgo leaf, a mustard wash panel with a wavy edge.
Run: python3 -I mustard-syari.py [part ...]   parts: garland corner wreath divider leaf wash
Assets -> public/themes/art/mustard-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o2_lib import *  # noqa

OUT = outdir("mustard-syari")
PARTS = sys.argv[1:] or ["garland", "corner", "wreath", "divider", "leaf", "wash"]

MUST, MUST_D, OCHRE = "#e0aa3a", "#b98318", "#cf8f2a"
RUST, RUST_D = "#b5532f", "#86381f"
GRASS, GRASS_D = "#c4a676", "#8f7347"
OLIVE = "#8f8a55"
BROWN = "#5a3a22"


def ginkgo_pts(cx, cy, L, ang, spread=1.8, notch=0.2, rng=None):
    """Ginkgo fan: petiole at (cx, cy) pointing along ang; blade is a fan with a wavy outer edge and a central notch."""
    rng = rng or random.Random(1)
    base = L * 0.34
    bx, by = cx + math.cos(ang) * base, cy + math.sin(ang) * base
    ph = rng.uniform(0, 6)
    pts = [(bx, by)]
    n = 30
    for i in range(n + 1):
        t = i / n
        a = ang - spread / 2 + spread * t
        r = (L - base) * (1 - notch * math.exp(-((t - 0.5) / 0.05) ** 2)) * (1 + 0.018 * math.sin(t * 23 + ph))
        r *= 1 - 0.14 * abs(2 * t - 1) ** 5
        pts.append((bx + math.cos(a) * r, by + math.sin(a) * r))
    return pts


def ginkgo(art, W, H, cx, cy, L, ang, nx, rng, tone=0.0):
    """Paint one ginkgo leaf + petiole. tone 0 mustard .. 1 ochre/rust-edged."""
    tip = (cx + math.cos(ang) * L * 0.34, cy + math.sin(ang) * L * 0.34)
    art = G(art, strokes(W, H, [([(cx, cy), tip], max(1.2, L * 0.035), (0.05, 0.3))]), GRASS_D, seed=nx(), density=0.85, edge=0.3, rough=0.5, feather=0.5)
    pts = ginkgo_pts(cx, cy, L, ang, rng=rng)
    m = shape_mask(W, H, pts, smooth=False)
    art = knockout(art, m, amount=1.0, grow=0.8)
    art = G(art, m, mix_hex(MUST, OCHRE, tone), mix_hex("#edc35a", MUST_D, tone), seed=nx(), density=0.95, edge=0.7, bloom=0.4, rough=0.8, feather=0.6, gran=0.3)
    outer = m * np.clip(1 - radial(W, H, cx, cy, L * 0.95) * 1.3, 0, 1)
    art = G(art, outer, mix_hex(OCHRE, RUST, tone * 0.8), seed=nx(), density=0.45, edge=0.2, rough=0.8, feather=1.2)
    veins = []
    for k in range(9):
        a = ang - 0.85 + k / 8 * 1.7
        veins.append(([tip, (tip[0] + math.cos(a) * L * 0.55, tip[1] + math.sin(a) * L * 0.55)], max(0.6, L * 0.012), (0.1, 0.4)))
    art = G(art, strokes(W, H, veins) * m, "#9c6a12", seed=nx(), density=0.6, edge=0.0, rough=0.4, feather=0.4)
    return art


def rust_leaf(art, W, H, x, y, L, ang, nx, rng, col=RUST):
    m = shape_mask(W, H, petal_pts(x, y, L, L * 0.2, ang, n=16, cup=rng.uniform(-0.3, 0.3)))
    art = knockout(art, m, amount=1.0, grow=0.8)
    art = G(art, m, col, mix_hex(col, "#d07a3e", 0.5), seed=nx(), density=0.93, edge=0.65, bloom=0.4, rough=0.8, feather=0.6, gran=0.35)
    rib = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in np.linspace(0.02, 0.85, 8)]
    art = G(art, strokes(W, H, [(rib, max(0.8, L * 0.025), (0.05, 0.6))]) * m, RUST_D, seed=nx(), density=0.6, edge=0.1, rough=0.4, feather=0.4)
    return art


def grass(art, W, H, base, ang, L, nx, rng, bend=0.25, heads=True, col=GRASS):
    """Dried grass: a thin curving stem; seed heads as small slanted dabs along the top third."""
    pts = []
    for t in np.linspace(0, 1, 14):
        a = ang + bend * t * t
        pts.append((base[0] + math.cos(ang) * L * t + math.cos(a + 1.57) * bend * L * 0.25 * t * t, base[1] + math.sin(ang) * L * t + math.sin(a + 1.57) * bend * L * 0.25 * t * t))
    art = G(art, strokes(W, H, [(pts, max(0.9, L * 0.008), (0.02, 0.4))]), GRASS_D, seed=nx(), density=0.75, edge=0.2, rough=0.5, feather=0.4)
    if heads:
        dabs = []
        for i in range(7, 14):
            px, py = pts[i]
            qx, qy = pts[i - 1]
            a = math.atan2(py - qy, px - qx)
            for side in (-1, 1):
                if rng.random() < 0.85:
                    s = L * rng.uniform(0.028, 0.045) * (1.1 - (i - 7) / 10)
                    dabs.append((px + math.cos(a + side * 0.6) * s * 0.8, py + math.sin(a + side * 0.6) * s * 0.8, s, s * 0.38, math.degrees(a + side * 0.5)))
        hm = ellipses(W, H, dabs)
        art = G(art, hm, col, mix_hex(col, "#e8d6a8", 0.4), seed=nx(), density=0.9, edge=0.5, rough=0.5, feather=0.4, gran=0.3)
    return art, pts


def olive_sprig(art, W, H, base, ang, L, nx, rng):
    pts = [(base[0] + math.cos(ang) * L * t, base[1] + math.sin(ang) * L * t + math.sin(t * 3) * L * 0.04) for t in np.linspace(0, 1, 10)]
    art = G(art, strokes(W, H, [(pts, max(1, L * 0.012), (0.05, 0.4))]), "#6f6a3e", seed=nx(), density=0.8, edge=0.2, rough=0.5, feather=0.4)
    lv = []
    for i in range(2, 10):
        px, py = pts[i]
        for side in (-1, 1):
            if rng.random() < 0.8:
                lv.append(petal_pts(px, py, L * rng.uniform(0.12, 0.18), L * 0.032, ang + side * 0.75 + rng.uniform(-0.15, 0.15), n=12))
    m = shapes(W, H, lv)
    art = G(art, m, OLIVE, "#a7a06a", seed=nx(), density=0.85, edge=0.55, rough=0.6, feather=0.5, gran=0.3)
    return art


def spray(art, W, H, items, nx, rng):
    """items in painting order (back to front): ('grass'|'olive'|'rust'|'ginkgo', x, y, L, ang, extra)"""
    for it in items:
        kind, x, y, L, a = it[:5]
        if kind == "grass":
            art, _ = grass(art, W, H, (x, y), a, L, nx, rng, bend=it[5] if len(it) > 5 else 0.25)
        elif kind == "olive":
            art = olive_sprig(art, W, H, (x, y), a, L, nx, rng)
        elif kind == "rust":
            art = rust_leaf(art, W, H, x, y, L, a, nx, rng, col=it[5] if len(it) > 5 else RUST)
        else:
            art = ginkgo(art, W, H, x, y, L, a, nx, rng, tone=it[5] if len(it) > 5 else 0.0)
        if rng.random() < 0.3:
            clear()
    return art


def part_garland():
    """A crescent garland that arcs over the top of the cover (opens downward), heavier on the right."""
    W, H = 820, 440
    rng = random.Random(5); nx = Seq(300)
    art = blank(W, H)
    cx, cy, R = 410, -300, 560
    items = []
    # grasses radiate outward from the arc
    for k in range(22):
        t = k / 21
        a = math.pi * (0.98 - 0.96 * t)
        bx, by = cx + math.cos(a) * R * 0.97, cy + math.sin(a) * R * 0.97
        out = 0.6 * a + 0.4 * math.pi / 2 + rng.uniform(-0.35, 0.35)
        items.append(("grass", bx, by, rng.uniform(150, 230), out, rng.uniform(-0.4, 0.4)))
    for k in range(7):
        t = (k + 0.5) / 7
        a = math.pi * (0.92 - 0.84 * t)
        bx, by = cx + math.cos(a) * R * 0.97, cy + math.sin(a) * R * 0.97
        items.append(("olive", bx, by, rng.uniform(90, 140), 0.6 * a + 0.4 * math.pi / 2 + rng.uniform(-0.5, 0.5)))
    leaves = []
    for k in range(48):
        t = (k + rng.uniform(0, 1)) / 48
        a = math.pi * (0.99 - 0.98 * t)
        rr = R * 0.97 + rng.uniform(-3, 3)
        bx, by = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        heavy = 1.0 + 0.45 * (1 - t)  # bigger towards the right side of the image (small t => right)
        kind = "rust" if rng.random() < 0.42 else "ginkgo"
        L = rng.uniform(58, 84) * heavy if kind == "ginkgo" else rng.uniform(70, 110) * heavy
        leaves.append((rng.random(), (kind, bx, by, L, 0.55 * a + 0.45 * math.pi / 2 + rng.uniform(-0.6, 0.6), rng.uniform(0, 1) if kind == "ginkgo" else rng.choice([RUST, "#c56a36", "#9a4428"]))))
    leaves.sort(key=lambda v: -v[0])
    twig = [(cx + math.cos(math.pi * (1.0 - t)) * R * 0.97 + rng.uniform(-2, 2), cy + math.sin(math.pi * (1.0 - t)) * R * 0.97) for t in np.linspace(0, 1, 40)]
    art = G(art, strokes(W, H, [(twig, 3.2, (0.02, 0.02)), (twig[4:18], 2.0, (0.2, 0.4))]), "#7a5a36", "#5a3a22", seed=nx(), density=0.9, edge=0.4, rough=1, feather=0.6)
    art = spray(art, W, H, items + [v[1] for v in leaves], nx, rng)
    preview(art, "ms-garland", tone="#f7efdc")
    save(art, f"{OUT}/garland.webp", max_w=780, quality=80)
    clear()


def part_corner():
    W, H = 520, 420
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    ox, oy = 30, 410
    items = []
    for k in range(9):
        items.append(("grass", ox + rng.uniform(-10, 30), oy, rng.uniform(220, 360), -math.pi / 2 + 0.15 + k * 0.1 + rng.uniform(-0.05, 0.05), rng.uniform(0.1, 0.5)))
    items += [("olive", ox + 20, oy - 10, 230, -0.9), ("olive", ox + 10, oy - 20, 180, -1.35)]
    items += [("rust", ox + 40, oy - 40, 120, -1.1), ("rust", ox + 60, oy - 20, 110, -0.5, "#c56a36"), ("ginkgo", ox + 90, oy - 70, 86, -0.85, 0.2),
              ("rust", ox + 20, oy - 70, 100, -1.6, "#9a4428"), ("ginkgo", ox + 140, oy - 26, 74, -0.25, 0.7), ("ginkgo", ox + 40, oy - 120, 70, -1.3, 0.0),
              ("rust", ox + 150, oy - 60, 90, -0.6), ("ginkgo", ox + 200, oy - 20, 60, -0.1, 0.4)]
    art = spray(art, W, H, items, nx, rng)
    preview(art, "ms-corner", tone="#f7efdc")
    save(art, f"{OUT}/corner.webp", max_w=360, quality=80)
    clear()


def part_wreath():
    W, H = 560, 560
    rng = random.Random(12); nx = Seq(1300)
    art = blank(W, H)
    cx, cy, R = 280, 280, 205
    items = []
    for k in range(30):
        a = k / 30 * math.tau + rng.uniform(-0.05, 0.05)
        bx, by = cx + math.cos(a) * R, cy + math.sin(a) * R
        tan = a + math.pi / 2
        items.append(("grass", bx, by, rng.uniform(60, 90), tan + rng.uniform(-0.5, 0.2), 0.2))
    leaves = []
    for k in range(56):
        a = k / 56 * math.tau + rng.uniform(-0.06, 0.06)
        if 1.2 < a % math.tau < 1.95:
            continue  # small gap at the bottom
        rr = R + rng.uniform(-22, 22)
        bx, by = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        tan = a + math.pi / 2 + rng.uniform(-0.6, 0.6)
        kind = "ginkgo" if k % 3 else "rust"
        L = rng.uniform(40, 56) if kind == "ginkgo" else rng.uniform(50, 70)
        leaves.append((kind, bx, by, L, tan, rng.uniform(0, 1) if kind == "ginkgo" else rng.choice([RUST, "#c56a36", "#9a4428"])))
    art = spray(art, W, H, items + leaves, nx, rng)
    preview(art, "ms-wreath", tone="#f7efdc")
    save(art, f"{OUT}/wreath.webp", max_w=400, quality=80)
    clear()


def part_divider():
    W, H = 720, 160
    rng = random.Random(4); nx = Seq(1700)
    art = blank(W, H)
    items = [("grass", 360, 110, 300, math.pi + 0.08, -0.2), ("grass", 360, 110, 300, -0.08, 0.2), ("grass", 360, 112, 220, math.pi - 0.12, -0.3), ("grass", 360, 112, 220, 0.12, 0.3),
             ("rust", 352, 108, 70, math.pi - 0.45), ("rust", 368, 108, 70, -0.45 + 0.0, "#c56a36"), ("ginkgo", 360, 116, 64, -math.pi / 2, 0.15)]
    art = spray(art, W, H, items, nx, rng)
    preview(art, "ms-divider", tone="#f7efdc")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=82)
    clear()


def part_leaf():
    W, H = 220, 220
    rng = random.Random(2); nx = Seq(1900)
    art = ginkgo(blank(W, H), W, H, 110, 190, 150, -math.pi / 2 - 0.25, nx, rng, tone=0.25)
    preview(art, "ms-leaf", tone="#f7efdc")
    save(art, f"{OUT}/leaf.webp", max_w=96, quality=84)
    clear()


def part_wash():
    """A mustard watercolour block with a soft wavy top edge (cover foot / closing)."""
    W, H = 780, 520
    rng = random.Random(3); nx = Seq(2100)
    pts = [(-20, H + 20), (-20, 70)]
    for x in range(0, W + 30, 30):
        pts.append((x, 60 + 22 * math.sin(x / 120) + 10 * math.sin(x / 37 + 1) + rng.uniform(-4, 4)))
    pts.append((W + 20, H + 20))
    m = displace(poly(W, H, pts, smooth=True), nx(), 6, 30)
    art = G(blank(W, H), m, MUST, "#e7b54c", seed=nx(), density=0.97, edge=0.6, bloom=0.12, mottle=0.25, rough=4, feather=1.2, gran=0.12)
    art = G(art, m * ygrad(W, H, 60, 400) * 0.8, OCHRE, seed=nx(), density=0.3, edge=0.1, bloom=0.2, mottle=0.3, rough=6, feather=8, gran=0.05)
    preview(art, "ms-wash", tone="#f7efdc")
    save_full(art, f"{OUT}/wash.webp", size=(468, 312), quality=70)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
