"""Wisteria Syari — watercolour wisteria racemes in lilac/violet cascading from a weathered pergola beam over cream.
Run: python3 -I wisteria-syari.py [part ...]; parts: cascade raceme spray wreath petals.
Assets -> public/themes/art/wisteria-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l1_lib import *

OUT = outdir("wisteria-syari")
PARTS = sys.argv[1:] or ["cascade", "raceme", "spray", "wreath", "petals"]
PALE, LIL, MID, DEEP, INK = "#d9c8ee", "#b79ddd", "#8e6cc4", "#5c3f91", "#3d2a5e"
LEAF1, LEAF2, LEAFD = "#a3b48a", "#6f8a5e", "#4b6343"
WOOD, WOOD_D, WOOD_L = "#9a8670", "#5e4c3b", "#c3b29a"


def raceme(art, W, H, x, y, L, sway, rng, nx, width=None, hue=0.0):
    """One hanging wisteria raceme: soft silhouette wash, dense overlapping pea-florets (widest in the upper third,
    pale and open at the top, deeper violet buds at the tip)."""
    width = width or L * 0.17
    stalk = bezier((x, y), (x + sway * 0.2, y + L * 0.55), (x + sway, y + L), 40)
    def wt_at(t):
        return width * (1 - t) ** 0.7 * min(1.0, 0.45 + t * 5)
    # silhouette wash under the florets
    left = [(px - wt_at(i / 39) * 0.9, py) for i, (px, py) in enumerate(stalk)]
    right = [(px + wt_at(i / 39) * 0.9, py) for i, (px, py) in enumerate(stalk)]
    sil = shapes(W, H, [deform(left + right[::-1], rng, 1, 0.02)])
    art = G(art, sil, PALE, LIL, seed=nx(), density=0.32, edge=0.35, bloom=0.5, rough=5, feather=2.5, pad=14)
    art = G(art, strokes(W, H, [(stalk, max(1.0, L * 0.003), (0.0, 0.3))]), "#8a7a6a", seed=nx(), density=0.28, edge=0.2, bloom=0, rough=1, feather=0.5, pad=10)
    groups = {k: [] for k in ("pale", "lil", "mid", "deep", "bud")}
    keels = []
    n = int(L / 2.4)
    for i in range(n):
        t = (i + rng.random()) / n
        px, py = stalk[min(39, int(t * 39))]
        wt = wt_at(t)
        for _ in range(3 if t < 0.6 else 2 if t < 0.85 else 1):
            u = rng.uniform(-1.12, 1.12)
            fx = px + u * wt + rng.gauss(0, 1.0)
            fy = py + rng.gauss(0, 3.2) + abs(u) * wt * 0.28
            s = (2.6 + 8.0 * (1 - t) ** 1.1) * rng.uniform(0.65, 1.2) * (width / 80) ** 0.5
            if t > 0.84:
                groups["bud"].append((fx, fy, s * 0.6, s * 0.9, rng.uniform(-20, 20)))
                continue
            tone = rng.random() * 0.95 + t * 1.05 - 0.25 + hue
            key = "pale" if tone < 0.35 else "lil" if tone < 0.72 else "mid" if tone < 1.1 else "deep"
            rot = rng.uniform(-30, 30) + u * 35
            groups[key].append((fx, fy, s, s * 0.72, rot))
            if rng.random() < 0.55:
                keels.append((fx + rng.gauss(0, 0.8), fy + s * 0.5, s * 0.42, s * 0.3, rot))
    cols = {"pale": (PALE, "#efe6f7"), "lil": (LIL, PALE), "mid": (MID, LIL), "deep": (DEEP, MID), "bud": (DEEP, "#6f7f58")}
    for key in ("pale", "lil", "mid", "deep", "bud"):
        if groups[key]:
            m = ellipses(W, H, groups[key])
            a, b = cols[key]
            art = G(art, m, a, b, seed=nx(), density=0.55 if key != "pale" else 0.45, edge=0.65, bloom=0.3, rough=1.8, feather=0.8, gran=0.3, pad=12)
    if keels:
        art = G(art, ellipses(W, H, keels), LIL, MID, seed=nx(), density=0.38, edge=0.6, bloom=0.2, rough=1.2, feather=0.6, pad=10)
    return art


def pinnate(art, W, H, x, y, L, ang, rng, nx, leaflets=4, size=1.0):
    """Wisteria compound leaf: a midrib with paired slender leaflets."""
    rib = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t + math.sin(t * 3) * L * 0.05) for t in [j / 20 for j in range(21)]]
    art = G(art, strokes(W, H, [(rib, 1.6 * size, (0.0, 0.3))]), LEAF2, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1, feather=0.5, pad=8)
    polys = []
    for j in range(leaflets):
        t = 0.2 + 0.8 * j / max(1, leaflets - 1)
        px, py = rib[int(t * 20)]
        ll = L * 0.32 * size * (1.1 - 0.3 * t)
        for side in (-1, 1):
            if j == leaflets - 1 and side == 1:
                polys.append(petal_pts(px, py, ll, ll * 0.32, ang + rng.gauss(0, 0.1), n=10))
                break
            polys.append(petal_pts(px, py, ll, ll * 0.34, ang + side * (0.85 + rng.gauss(0, 0.12)), n=10))
    m = shapes(W, H, polys)
    art = G(art, m, LEAF1, LEAF2, seed=nx(), density=0.62, edge=0.7, bloom=0.35, rough=1.2, feather=0.7, gran=0.25, pad=10)
    veins = []
    for pts_ in polys:
        c0 = pts_[0]; c1 = pts_[len(pts_) // 2]
        veins.append(([c0, ((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2)], 0.9))
    art = G(art, strokes(W, H, veins), LEAFD, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.3, pad=8)
    return art


def tendril(W, H, pts, w):
    return strokes(W, H, [(pts, w, (0.05, 0.4))])


if "cascade" in PARTS:
    # pergola beam across the top (from the right edge, slightly tilted) with twisting vines and hanging racemes
    W, H = 760, 1160
    nx = Seq(30100); rng = random.Random(7)
    art = blank(W, H)
    beam = shapes(W, H, [[(90, 64), (W + 20, 30), (W + 20, 92), (96, 120)]], smooth=False)
    end = shapes(W, H, [[(70, 62), (100, 58), (106, 124), (74, 130)]], smooth=False)
    wood = np.maximum(beam, end)
    art = GP(art, wood, WOOD_L, WOOD, seed=nx(), rough=1.6, streak=1.0, pad=12)
    rngg = random.Random(3)
    gl = [([(100 + t * 680, y0 + (t * -34) + rngg.gauss(0, 0.6) + 2 * math.sin(t * 7 + y0)) for t in [j / 40 for j in range(41)]], rngg.uniform(0.8, 1.8), (0.1, 0.1)) for y0 in range(70, 122, 7)]
    art = G(art, strokes(W, H, gl) * wood, WOOD_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.8, feather=0.5)
    shade = np.clip(wood - lift(wood, 0, 16), 0, 1)
    art = G(art, shade, WOOD_D, seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1.5, feather=2)
    hi = np.clip(wood - lift(wood, 0, -10), 0, 1)
    art = OV(art, hi * 0.35, lambda m: tint(m, "#efe4d2"))
    ring_ = ring(W, H, 88, 94, 18, 3) * end
    art = G(art, ring_, WOOD_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    # vines wrapping the beam
    vine = []
    for k in range(2):
        pts = [(110 + t * 660, 84 + 30 * math.sin(t * 7 + k * 2.6) - t * 32) for t in [j / 80 for j in range(81)]]
        vine.append((pts, 4.0 - k * 1.2, (0.05, 0.1)))
    art = G(art, strokes(W, H, vine), "#5b4636", "#7d6650", seed=nx(), density=0.8, edge=0.45, bloom=0.1, rough=1.4, feather=0.6)
    # back racemes (paler, behind) then front racemes
    specs_back = [(205, 112, 260, 10), (420, 98, 380, -12), (650, 80, 520, 14)]
    specs_front = [(140, 118, 300, 16), (290, 108, 470, -10), (380, 102, 620, 12), (520, 92, 820, -8), (610, 86, 990, 10), (725, 76, 720, -12)]
    for (x, y, L, sw) in specs_back:
        art = raceme(art, W, H, x, y, L, sw, rng, nx, width=L * 0.08 + 22, hue=-0.35)
    # leaves hanging from the vines
    for (x, y, L, a) in [(260, 104, 140, 1.2), (590, 84, 130, 2.0), (210, 96, 100, 0.4), (650, 70, 110, 2.8)]:
        art = pinnate(art, W, H, x, y, L, a, rng, nx, leaflets=4)
    clear()
    for (x, y, L, sw) in specs_front:
        art = raceme(art, W, H, x, y, L, sw, rng, nx, width=L * 0.09 + 26, hue=rng.uniform(-0.15, 0.12))
        clear()
    # foliage in front along the beam
    for (x, y, L, a) in [(120, 122, 150, 1.9), (330, 106, 140, 2.3), (470, 98, 150, 0.9), (690, 82, 130, 1.4)]:
        art = pinnate(art, W, H, x, y, L, a, rng, nx, leaflets=4, size=1.15)
    # curling tendrils
    td = [spiral_pts(120, 140, 2, 16, 0, 1.3, 30, 1), spiral_pts(560, 120, 2, 14, 2, 1.2, 30, -1)]
    art = G(art, strokes(W, H, [(p, 1.6, (0.0, 0.5)) for p in td]), "#6b5a4a", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=0.4)
    preview(art, "ws-cascade", tone="#f7f1e6")
    save(art, f"{OUT}/cascade.webp", max_w=520, quality=72)
    clear()

if "raceme" in PARTS:
    W, H = 220, 640
    nx = Seq(31100); rng = random.Random(11)
    art = blank(W, H)
    art = pinnate(art, W, H, 110, 20, 110, 2.5, rng, nx, leaflets=3, size=0.9)
    art = raceme(art, W, H, 110, 18, 590, 14, rng, nx, width=86)
    preview(art, "ws-raceme", tone="#f7f1e6")
    save(art, f"{OUT}/raceme.webp", max_w=180, quality=80)
    clear()

if "spray" in PARTS:
    # horizontal divider: a short twig with leaves and three small hanging racemes
    W, H = 640, 260
    nx = Seq(32100); rng = random.Random(21)
    art = blank(W, H)
    twig = [(40 + t * 560, 60 - 26 * math.sin(t * math.pi) + 6 * math.sin(t * 11)) for t in [j / 60 for j in range(61)]]
    art = G(art, strokes(W, H, [(twig, 4, (0.1, 0.2))]), "#5b4636", "#7d6650", seed=nx(), density=0.75, edge=0.4, bloom=0.1, rough=1.2, feather=0.6)
    for (x, y, L, a) in [(80, 52, 120, 2.9), (200, 38, 110, -0.6), (440, 38, 120, -2.6), (560, 50, 110, 0.3)]:
        art = pinnate(art, W, H, x, y, L, a, rng, nx, leaflets=3, size=0.8)
    for (x, y, L, sw) in [(250, 40, 200, -8), (320, 36, 175, 6), (390, 38, 195, 10)]:
        art = raceme(art, W, H, x, y, L, sw, rng, nx, width=L * 0.17)
    preview(art, "ws-spray", tone="#f7f1e6")
    save(art, f"{OUT}/spray.webp", max_w=320, quality=80)
    clear()

if "wreath" in PARTS:
    # circular wisteria garland for the monogram medallion
    W, H = 620, 760
    nx = Seq(33100); rng = random.Random(31)
    art = blank(W, H)
    cx = cy = 310; R = 250
    art = G(art, strokes(W, H, [(arc_pts(cx, cy, R, -math.pi * 0.95, math.pi * 0.95, 80), 3.2, (0.05, 0.05))]), "#6b5a4a", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1.5, feather=0.5)
    for k in range(9):
        a = -math.pi * 0.85 + k * (math.pi * 1.7) / 8
        x, y = cx + math.cos(a) * R, cy + math.sin(a) * R
        art = pinnate(art, W, H, x, y, 95, a + math.pi / 2 * (1 if k % 2 else -1) * 0.6 + math.pi / 2, rng, nx, leaflets=3, size=0.95)
    clear()
    florets = {"pale": [], "lil": [], "mid": [], "deep": []}
    for k in range(900):
        c = rng.random()
        a = rng.gauss(-2.2, 0.55) if c < 0.42 else rng.gauss(0.75, 0.6) if c < 0.84 else rng.uniform(-math.pi, math.pi)
        a = (a + math.pi) % math.tau - math.pi
        if abs(abs(a) - math.pi) < 0.25:
            continue
        rr = R + rng.gauss(0, 13)
        s = rng.uniform(4.5, 10)
        key = rng.choice(["pale", "lil", "lil", "mid", "deep"] if a > 0 else ["pale", "pale", "lil", "mid"])
        florets[key].append((cx + math.cos(a) * rr, cy + math.sin(a) * rr, s, s * 0.78, rng.uniform(0, 180)))
    cols = {"pale": (PALE, LIL), "lil": (LIL, PALE), "mid": (MID, LIL), "deep": (DEEP, MID)}
    for key, items in florets.items():
        art = G(art, ellipses(W, H, items), *cols[key], seed=nx(), density=0.6, edge=0.55, bloom=0.3, rough=2, feather=0.9, gran=0.3)
    # two short racemes hanging from the bottom of the ring
    art = raceme(art, W, H, cx - 40, cy + R - 4, 150, -6, rng, nx, width=26)
    art = raceme(art, W, H, cx + 36, cy + R - 6, 110, 8, rng, nx, width=22)
    preview(art, "ws-wreath", tone="#f7f1e6")
    save(art, f"{OUT}/wreath.webp", max_w=360, quality=80)
    clear()

if "petals" in PARTS:
    # fallen florets scattered on the ground line (closing band)
    W, H = 780, 160
    nx = Seq(34100); rng = random.Random(41)
    art = blank(W, H)
    groups = {"pale": [], "lil": [], "mid": []}
    for k in range(120):
        x = rng.uniform(10, W - 10); y = H * 0.62 + rng.gauss(0, 22) * (0.5 + 0.5 * math.sin(x / 90))
        s = rng.uniform(3, 7)
        groups[rng.choice(list(groups))].append((x, y, s, s * 0.7, rng.uniform(0, 180)))
    cols = {"pale": (PALE, LIL), "lil": (LIL, PALE), "mid": (MID, LIL)}
    for key, items in groups.items():
        art = G(art, ellipses(W, H, items), *cols[key], seed=nx(), density=0.55, edge=0.55, bloom=0.3, rough=1.6, feather=0.8)
    preview(art, "ws-petals", tone="#f7f1e6")
    save(art, f"{OUT}/petals.webp", max_w=480, quality=78)
