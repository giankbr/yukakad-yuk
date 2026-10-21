"""Kawung Biru — indigo/slate toile: misty engraved trees & palms, engraved joglo, wayang silhouettes with openwork,
kawung lattice, blue lilies + white orchids. Run: python3 -I kawung-biru.py [part ...]
parts: scene joglo wayang lily kawung divider. Assets -> public/themes/art/kawung-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *
import _jw_lib as jw

OUT = outdir("kawung-biru")
PARTS = sys.argv[1:] or ["scene", "joglo", "wayang", "lily", "kawung", "divider"]
BG = "#e9eef3"
SLATE, SLATE_D, SLATE_L, INDIGO = "#6f7f96", "#3c4a63", "#b8c3d2", "#2c3a5a"
jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = "#9fb0b8", "#61798a", "#3c5166"


def engraved(W, H, mask, tone_dark, nx, spacing=3.6, angle=0.5, light=None, seed=1, density=0.75):
    """Toile engraving: wash + hatch lines whose weight follows a light-from-top-left tone field."""
    a = blank(W, H)
    a = G(a, mask, light or SLATE_L, light or SLATE_L, seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=3)
    sh = np.clip(gaussian_filter(mask, 6) - np.roll(np.roll(gaussian_filter(mask, 6), -8, 0), -6, 1) + 0.35, 0, 1)
    tone = np.clip(sh * 1.2 * (0.6 + 0.6 * fbm(W, H, seed, 40, 2)), 0, 1)
    lines = jw.engrave(mask, tone, angle, spacing, seed, cross=0.62)
    return G(a, lines, tone_dark, seed=nx(), density=density, edge=0.1, bloom=0, rough=0.8, feather=0.45)


def tree(W, H, cx, by, h, rng):
    """Toile canopy: cluster of lumpy blobs on a thin trunk."""
    polys = []
    for k in range(9):
        r = h * rng.uniform(0.13, 0.2)
        x = cx + rng.gauss(0, h * 0.17); y = by - h * 0.62 + rng.gauss(0, h * 0.14)
        polys.append(deform(ellipse_pts(x, y, r, r * 0.8, 12), rng, 2, 0.16))
    canopy = shapes(W, H, polys)
    trunk = strokes(W, H, [(curve([(cx, by), (cx + h * 0.02, by - h * 0.3), (cx - h * 0.01, by - h * 0.55)], 12), h * 0.035, (0.0, 0.6))])
    return canopy, trunk


if "scene" in PARTS:
    W, H = 780, 1100
    nx = Seq(7100); rng = random.Random(71)
    art = blank(W, H)
    # far hills + misty tree line (pale), then nearer trees/palms at the sides (darker), all on transparent
    art = G(art, jw.hills(W, H, 560, 40, 4, 1.2), "#d5dde7", "#c4cfdc", seed=nx(), density=0.45, edge=0.35, bloom=0.5, rough=8)
    for i, (x, h) in enumerate([(60, 420), (190, 360), (330, 300), (470, 320), (610, 380), (730, 430), (120, 520), (680, 540)]):
        c, t = tree(W, H, x, 700 + (i % 3) * 30, h, rng)
        tone = 0.35 + 0.2 * (h > 400)
        art = glaze(art, engraved(W, H, c, mix(SLATE, "#ffffff", 0.3 - tone * 0.3), nx, spacing=4.2, seed=nx(), density=0.45 + tone * 0.3, light="#cfd8e3"))
        art = G(art, t, SLATE, seed=nx(), density=0.4, edge=0.3, rough=1.5)
    for (x, h, ln) in [(250, 330, -0.1), (540, 360, 0.12), (40, 300, 0.05), (750, 320, -0.08)]:
        art = G(art, jw.palm(W, H, x, 760, h, rng, ln), SLATE, SLATE_L, seed=nx(), density=0.5, edge=0.35, bloom=0.2, rough=2, feather=0.7)
    # soft mist band
    mist = np.clip(1 - np.abs(np.linspace(-1, 1, H)[:, None] * 5 - 1.2), 0, 1) * np.ones((1, W))
    art[..., 3] *= 1 - 0.45 * mist.astype(np.float32)
    preview(art, "kb-scene", BG)
    save_full(art, f"{OUT}/scene.webp", size=(520, 733), quality=74)

if "joglo" in PARTS:
    W, H = 760, 560
    nx = Seq(7200)
    m = jw.joglo_masks(W, H, 380, 515, 540)
    art = blank(W, H)
    roof = np.maximum.reduce([m["emper"], m["pen"], m["bru"]])
    art = glaze(art, engraved(W, H, roof, INDIGO, nx, spacing=3.2, angle=0.05, seed=11, density=0.85))
    art = G(art, m["tiles"] * roof, SLATE_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    art = G(art, m["shadow"], INDIGO, seed=nx(), density=0.85, edge=0.2, rough=1)
    art = G(art, np.maximum.reduce([m["posts"], m["umpak"], m["lintel"]]), SLATE_D, INDIGO, seed=nx(), density=0.85, edge=0.4, rough=1.2)
    art = glaze(art, engraved(W, H, m["gebyok"], SLATE_D, nx, spacing=2.8, angle=1.57, seed=12, density=0.6))
    art = glaze(art, engraved(W, H, m["platform"], SLATE_D, nx, spacing=3.4, angle=0.0, seed=13, density=0.6))
    art = G(art, m["ridge"], INDIGO, seed=nx(), density=0.9, edge=0.2, rough=0.8, feather=0.5)
    preview(art, "kb-joglo", BG)
    save(art, f"{OUT}/joglo.webp", max_w=620, quality=80)

if "wayang" in PARTS:
    W, H = 260, 640
    nx = Seq(7300)
    m = jw.wayang_masks(W, H, 20, 24, 2.2, "putra", 1)
    solid = np.clip(m["body"] - m["holes"], 0, 1)
    art = blank(W, H)
    art = G(art, m["sticks"], SLATE_D, seed=nx(), density=0.8, edge=0.2, rough=0.6, feather=0.5)
    art = OV(art, solid, lambda q: linocut(q, SLATE_D, seed=31, wear=0.25, rough=1.2))
    art = glaze(art, engraved(W, H, m["kain"] * solid, INDIGO, nx, spacing=2.6, angle=0.9, seed=14, density=0.7, light=SLATE))
    art = G(art, m["face"], INDIGO, seed=nx(), density=0.95, edge=0.2, rough=0.6)
    art = G(art, np.maximum(m["trim"], m["crown"] * solid * 0.6), "#e9eef3", seed=nx(), density=0.6, edge=0.2, rough=0.6, feather=0.5)
    preview(art, "kb-wayang", BG)
    save(art, f"{OUT}/wayang.webp", max_w=230, quality=82)


def lily(art, W, H, cx, cy, r, rot, rng, nx, light="#c9d6ee", mid="#7f96c9", deep="#3f548f"):
    """Blue lily: six recurved tepals, darker throat, curved stamens."""
    tep = []
    for k in range(6):
        a = rot + k * math.tau / 6 + rng.uniform(-0.12, 0.12)
        tep.append(deform(petal_pts(cx, cy, r * rng.uniform(0.9, 1.08), r * 0.38, a, n=14, cup=0.25), rng, 1, 0.05))
    for k, t in enumerate(tep):
        m = shape_mask(W, H, t)
        art = G(art, m, light, mid, seed=nx(), density=0.55, edge=0.65, bloom=0.4, rough=3)
        a = rot + k * math.tau / 6
        mid_line = [(cx + math.cos(a) * r * u, cy + math.sin(a) * r * u) for u in [0.1, 0.35, 0.6, 0.85]]
        art = G(art, stroke_mask(W, H, curve(mid_line, 12), r * 0.08), deep, seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1.2, feather=0.8)
    throat = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * 0.3, r * 0.3, 10), rng, 1, 0.1))
    art = G(art, throat, deep, mid, seed=nx(), density=0.6, edge=0.4, bloom=0.2, rough=2)
    st = []
    for k in range(6):
        a = rot + 0.5 + k * math.tau / 6
        st.append((curve([(cx, cy), (cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.45 - r * 0.05), (cx + math.cos(a) * r * 0.7, cy + math.sin(a) * r * 0.7)], 10), 1.4, (0.1, 0.1)))
    art = G(art, strokes(W, H, st), "#5b6d55", seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    tips = []
    for k in range(6):
        a = rot + 0.5 + k * math.tau / 6
        tips.append((cx + math.cos(a) * r * 0.7, cy + math.sin(a) * r * 0.7, r * 0.07, r * 0.03, math.degrees(a)))
    return G(art, ellipses(W, H, tips), "#8a5a3a", seed=nx(), density=0.85, edge=0.3, rough=0.6)


if "lily" in PARTS:
    W, H = 560, 460
    nx = Seq(7400); rng = random.Random(74)
    art = blank(W, H)
    # leaves fanning from the top-left corner (asset is used in corners; flipped by CSS)
    for (a, L) in [(0.15, 330), (0.45, 360), (0.75, 330), (1.05, 280), (1.35, 220), (-0.1, 240)]:
        p = curve([(10, 10), (10 + math.cos(a) * L * 0.5, 10 + math.sin(a) * L * 0.5 + 12), (10 + math.cos(a + 0.18) * L, 10 + math.sin(a + 0.18) * L + 30)], 24)
        art = G(art, shapes(W, H, [jw.blade(W, H, p, 20)]), "#a9bac4", "#5f7789", seed=nx(), density=0.55, edge=0.5, bloom=0.35, rough=3)
        art = G(art, strokes(W, H, [(p[2:-3], 1.3, (0.1, 0.4))]), "#3c5166", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.8, feather=0.5)
    for (x, y, r, rot) in [(150, 120, 74, 0.3), (300, 230, 62, 1.1), (90, 270, 54, 0.7)]:
        art = lily(art, W, H, x, y, r, rot, rng, nx)
    for (x, y, r) in [(250, 90, 30), (400, 150, 26), (200, 330, 24)]:
        art = jw.orchid(art, W, H, x, y, r, rng, nx, rot=rng.uniform(-0.3, 0.3))
    for (x, y, sz, a) in [(440, 260, 16, 0.6), (320, 350, 14, 1.2), (470, 110, 13, 0.1)]:
        art = jw.bud(art, W, H, x, y, sz, a, rng, nx, "#a7b8dc", "#4b5f99")
    art = jw.dots(art, W, H, rng, nx, 280, 220, 140, 110, 18, "#7f96c9")
    preview(art, "kb-lily", BG)
    save(art, f"{OUT}/lily.webp", max_w=480, quality=80)

if "kawung" in PARTS:
    n = 240
    nx = Seq(7500)
    k = jw.kawung_tile(n, 60)
    marks = jw.kawung_tile(n, 60, fat=0.07)
    art = blank(n, n)
    art = G(art, k, SLATE, SLATE_L, seed=nx(), density=0.5, edge=0.6, bloom=0.3, rough=1.5)
    art = G(art, marks, SLATE_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.6)
    art = G(art, circles(n, n, [(x, y, 3.2) for x in range(30, n + 30, 60) for y in range(30, n + 30, 60)]), SLATE_D, seed=nx(), density=0.6, edge=0.2, rough=0.6)
    save_full(art, f"{OUT}/kawung.webp", quality=78)
    preview(art, "kb-kawung", BG)

if "divider" in PARTS:
    W, H = 360, 64
    nx = Seq(7600)
    art = blank(W, H)
    art = G(art, strokes(W, H, [([(20, 32), (140, 32)], 1.6, (0.4, 0.0)), ([(220, 32), (340, 32)], 1.6, (0.0, 0.4))]), SLATE, seed=nx(), density=0.7, edge=0.2, rough=0.6, feather=0.5)
    petals = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        petals.append(deform(ellipse_pts(180 + math.cos(a) * 12, 32 + math.sin(a) * 12, 13, 7, 12, a), random.Random(k), 1, 0.05))
    pm = shapes(W, H, petals)
    art = G(art, pm, "#8fa0c6", "#4b5f99", seed=nx(), density=0.75, edge=0.6, rough=1.2)
    art = G(art, circles(W, H, [(180, 32, 3), (150, 32, 2.4), (210, 32, 2.4), (122, 32, 1.8), (238, 32, 1.8)]), INDIGO, seed=nx(), density=0.8, edge=0.2, rough=0.5)
    preview(art, "kb-divider", BG)
    save(art, f"{OUT}/divider.webp", quality=84)
