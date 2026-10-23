"""Peach Syari — peach and soft-coral watercolour florals (ranunculus, garden roses, buds, waxflower) with sage leaves on
cream paper. Loose transparent washes, wet edges, blooms. Florals only (no figures).
Run: python3 -I peach-syari.py [part ...]  parts: garland corner bloom divider wash
Assets -> public/themes/art/peach-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n2_lib import *
import _j2_lib as j2
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-N2/art"

OUT = outdir("peach-syari")
PARTS = sys.argv[1:] or ["garland", "corner", "bloom", "divider", "wash"]

PEACH, PEACH_L, CORAL, CORAL_D = "#f5b394", "#fbd9c3", "#e98068", "#c2584a"
APRICOT, BLUSH, CREAMP = "#f7c79a", "#f2a7a0", "#fbe8d8"
SAGE, SAGE_D, OLIVE, TEAL = "#a6b597", "#6f8763", "#8a9a6a", "#8ea79f"


class SD:
    def __init__(self, v):
        self.v = v

    def __call__(self):
        self.v += 13
        return self.v


def leaf_spray(art, W, H, x, y, ang, n, L, rng, sd, cols=(SAGE, SAGE_D)):
    """A curved stem with alternate leaves."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = ang + math.sin(t * 2.2) * 0.35
        pts.append((x + math.cos(a) * L * t, y + math.sin(a) * L * t))
    stem = strokes(W, H, [(curve(pts, 30), max(1.6, L * 0.012), (0.0, 0.5))])
    art = glaze(art, pigment_local(stem, SAGE_D, OLIVE, sd(), density=0.6, edge=0.3, bloom=0, rough=1.2, feather=0.7))
    for i in range(1, n + 1):
        px, py = pts[i]
        side = 1 if i % 2 else -1
        la = ang + side * rng.uniform(0.6, 1.0)
        ll = L * rng.uniform(0.16, 0.24) * (1.15 - i / n * 0.4)
        lay, _ = j2.leaf(W, H, px, py, ll, la, *(cols if rng.random() > 0.3 else (TEAL, SAGE_D)), sd, rng, width=0.36, density=0.55, curl=side * 0.15)
        art = glaze(art, lay)
    return art


def filler(art, W, H, pts, rng, sd, col=CREAMP, deep=PEACH):
    """Waxflower clusters: tiny five-dot blossoms with a darker eye."""
    items = []
    for (x, y) in pts:
        for k in range(5):
            a = k / 5 * math.tau + rng.uniform(-.2, .2)
            items.append((x + math.cos(a) * 5, y + math.sin(a) * 5, 4.2))
    m = circles(W, H, items)
    art = glaze(art, pigment_local(m, col, deep, sd(), density=0.55, edge=0.7, bloom=0.2, rough=1.5, feather=0.8))
    eyes = circles(W, H, [(x, y, 2.2) for x, y in pts])
    return glaze(art, pigment_local(eyes, CORAL_D, None, sd(), density=0.7, edge=0.3, bloom=0, rough=0.8, feather=0.6))


def garland():
    """Cover spray: a big asymmetric cluster rising from the bottom-left with stems trailing up and across."""
    W, H = 820, 760
    rng = random.Random(21)
    sd = SD(300)
    art = blank(W, H)
    # leaves first (behind blooms)
    for (x, y, a, n, L) in [(250, 560, -0.55, 6, 420), (230, 590, -1.35, 5, 300), (300, 560, 0.15, 5, 360), (180, 600, -2.6, 4, 220), (330, 610, -0.2, 5, 500)]:
        art = leaf_spray(art, W, H, x, y, a, n, L, rng, sd)
    for (x, y, L, a) in [(150, 500, 120, -2.2), (380, 470, 110, -0.8), (420, 600, 130, 0.25), (110, 640, 110, 2.9), (310, 690, 120, 1.2)]:
        lay, _ = j2.leaf(W, H, x, y, L, a, SAGE, SAGE_D, sd, rng, width=0.38, density=0.6)
        art = glaze(art, lay)
    # blooms
    lay, _ = ranunculus(W, H, 250, 560, 100, PEACH_L, PEACH, CORAL_D, sd, rng, rings=7)
    art = over(art, lay)
    lay, _ = j2.rose(W, H, 380, 640, 82, CREAMP, PEACH, CORAL, sd, rng, petals=10)
    art = over(art, lay)
    lay, _ = j2.rose(W, H, 130, 640, 70, BLUSH, CORAL, CORAL_D, sd, rng, petals=9)
    art = over(art, lay)
    lay, _ = ranunculus(W, H, 365, 470, 58, CREAMP, APRICOT, CORAL, sd, rng, rings=5)
    art = over(art, lay)
    lay, _ = ranunculus(W, H, 165, 470, 44, PEACH_L, BLUSH, CORAL_D, sd, rng, rings=5)
    art = over(art, lay)
    for (x, y, s, a, c, d) in [(470, 410, 18, -0.9, CORAL, CORAL_D), (540, 360, 14, -0.6, PEACH, CORAL), (96, 420, 16, -2.2, PEACH, CORAL_D), (620, 300, 12, -0.7, BLUSH, CORAL)]:
        lay, _ = j2.bud(W, H, x, y, s, a, c, d, SAGE_D, sd, rng)
        art = glaze(art, lay)
    art = filler(art, W, H, [(470, 560), (488, 540), (452, 530), (60, 560), (80, 580), (520, 470), (300, 400), (318, 380)], rng, sd)
    # scattered drops of colour
    drops = circles(W, H, [(rng.uniform(80, 700), rng.uniform(260, 700), rng.uniform(1.5, 4)) for _ in range(18)])
    art = glaze(art, pigment_local(drops, PEACH, CORAL, sd(), density=0.4, edge=0.6, bloom=0, rough=1))
    preview(art, "ps-garland")
    save(art, f"{OUT}/garland.webp", max_w=620, quality=82)


def corner():
    W, H = 520, 440
    rng = random.Random(5)
    sd = SD(700)
    art = blank(W, H)
    for (x, y, a, n, L) in [(390, 120, 2.6, 5, 340), (380, 110, 1.9, 4, 240), (400, 140, 2.2, 4, 300)]:
        art = leaf_spray(art, W, H, x, y, a, n, L, rng, sd)
    lay, _ = ranunculus(W, H, 400, 110, 72, PEACH_L, PEACH, CORAL_D, sd, rng, rings=6)
    art = over(art, lay)
    lay, _ = j2.rose(W, H, 300, 70, 50, CREAMP, APRICOT, CORAL, sd, rng, petals=8)
    art = over(art, lay)
    for (x, y, s, a) in [(230, 190, 13, 2.4), (330, 230, 12, 2.0)]:
        lay, _ = j2.bud(W, H, x, y, s, a, PEACH, CORAL_D, SAGE_D, sd, rng)
        art = glaze(art, lay)
    art = filler(art, W, H, [(250, 120), (268, 104), (470, 210), (450, 230)], rng, sd)
    preview(art, "ps-corner")
    save(art, f"{OUT}/corner.webp", max_w=300, quality=82)


def bloom():
    W, H = 300, 280
    rng = random.Random(9)
    sd = SD(900)
    art = blank(W, H)
    for (x, y, L, a) in [(150, 150, 100, 2.6), (150, 150, 96, 0.5), (150, 150, 80, 1.6)]:
        lay, _ = j2.leaf(W, H, x, y, L, a, SAGE, SAGE_D, sd, rng, width=0.36, density=0.6)
        art = glaze(art, lay)
    lay, _ = ranunculus(W, H, 150, 130, 74, PEACH_L, PEACH, CORAL_D, sd, rng, rings=6)
    art = over(art, lay)
    preview(art, "ps-bloom")
    save(art, f"{OUT}/bloom.webp", max_w=180, quality=84)


def divider():
    W, H = 620, 120
    rng = random.Random(14)
    sd = SD(1100)
    art = blank(W, H)
    for side in (-1, 1):
        pts = [(310 + side * t * 270, 62 - math.sin(t * math.pi) * 10 + t * 4) for t in np.linspace(0.06, 1, 30)]
        stem = strokes(W, H, [(pts, 2.2, (0.0, 0.6))])
        art = glaze(art, pigment_local(stem, SAGE_D, OLIVE, sd(), density=0.6, edge=0.3, bloom=0, rough=1, feather=0.7))
        for i, t in enumerate(np.linspace(0.18, 0.9, 6)):
            x, y = 310 + side * t * 270, 62 - math.sin(t * math.pi) * 10 + t * 4
            up = 1 if i % 2 else -1
            a = (0 if side > 0 else math.pi) + side * (-0.5 * up) + (0.1 * side)
            lay, _ = j2.leaf(W, H, x, y, 34 * (1.1 - t * 0.5), a - side * 0.0 + (-up * 0.4 if side > 0 else up * 0.4), SAGE, SAGE_D, sd, rng, width=0.36, density=0.55)
            art = glaze(art, lay)
    lay, _ = ranunculus(W, H, 310, 60, 26, PEACH_L, PEACH, CORAL_D, sd, rng, rings=4)
    art = over(art, lay)
    art = filler(art, W, H, [(268, 52), (352, 68)], rng, sd)
    preview(art, "ps-divider")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)


def wash():
    """Soft peach watercolour pool (backs the names on the cover and the monograms)."""
    W, H = 640, 760
    rng = random.Random(2)
    art = blank(W, H)
    m = shape_mask(W, H, deform(ellipse_pts(320, 380, 270, 330, 16), rng, 3, 0.1))
    art = glaze(art, pigment(m, "#fde3d2", "#fbd6c2", seed=41, density=0.55, edge=0.45, bloom=0.6, gran=0.15, rough=14, feather=3))
    m2 = shape_mask(W, H, deform(ellipse_pts(300, 360, 200, 250, 14), rng, 3, 0.12))
    art = glaze(art, pigment(m2, "#fde9dc", None, seed=43, density=0.3, edge=0.3, bloom=0.6, gran=0.1, rough=12, feather=3))
    preview(art, "ps-wash")
    save(art, f"{OUT}/wash.webp", max_w=420, quality=80)


for p in PARTS:
    globals()[p]()
    clear()
kb_total(OUT)
