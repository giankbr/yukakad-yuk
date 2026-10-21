"""Tasbih Mutiara — no-photo syari wedding in pearl white & sage: painted pearl strands (soft specular, iridescent rim),
soft watercolour white-blush roses with sage leaves, pearl-ring monogram medallion, pearlescent paper tile.
Run: python3 -I tasbih-mutiara.py [part ...]  parts: strand medallion roses divider pearl paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a4_lib import *

OUT = outdir("tasbih-mutiara")
PARTS = sys.argv[1:] or ["strand", "medallion", "roses", "divider", "pearl", "paper"]
SAGE_A, SAGE_B, SAGE_D = "#b2c2a6", "#7d9779", "#4d6650"
jw.LEAF_D = SAGE_D
R_LIGHT, R_MID, R_DEEP = "#fbeeea", "#eec7c2", "#c58d8c"
CHAMP = "#cdb88f"


def sprig(art, W, H, pts, rng, nx, L=44, every=3, col=(SAGE_A, SAGE_B)):
    """Sage stem with paired leaves along pts."""
    art = G(art, strokes(W, H, [(pts, 2.6, (0.05, 0.4))]), SAGE_B, SAGE_D, seed=nx(), density=0.7, edge=0.3, bloom=0, rough=1, feather=0.6)
    for j in range(2, len(pts) - 1, every):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        t = j / len(pts)
        ll = L * (0.55 + 0.45 * (1 - t))
        for side in (-1, 1):
            art = leaf(art, W, H, pts[j][0], pts[j][1], ll * rng.uniform(0.85, 1.1), ang + side * rng.uniform(0.6, 0.9), rng, nx, c=col)
    tip = pts[-1]
    a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    return leaf(art, W, H, tip[0], tip[1], L * 0.6, a, rng, nx, c=col)


def white_rose(art, W, H, x, y, r, rng, nx, area=None):
    return rose(art, W, H, x, y, r, rng, nx, R_LIGHT, R_MID, R_DEEP, area)


if "strand" in PARTS:
    W, H = 780, 330
    nx = Seq(20100); rng = random.Random(3)
    art = blank(W, H)
    items = []
    items += string_pearls(catenary(-14, 6, 394, 30, 150), 8.5, seed=1)
    items += string_pearls(catenary(386, 30, 794, 6, 150), 8.5, seed=2)
    items += string_pearls(catenary(-14, 4, 300, 4, 70), 6.0, seed=3)
    items += string_pearls(catenary(480, 4, 794, 4, 70), 6.0, seed=4)
    drop = string_pearls([(390, 34), (390, 210)], 7.0, jitter=0.02, seed=5)
    # sage sprigs + rose knot at the centre
    art = sprig(art, W, H, curve([(392, 36), (340, 30), (300, 46), (262, 40)], 20), rng, nx, L=34)
    art = sprig(art, W, H, curve([(388, 36), (440, 28), (482, 44), (520, 36)], 20), rng, nx, L=34)
    art = draw_pearls(art, items, seed=10)
    art = draw_pearls(art, drop, seed=300)
    # teardrop pearl at the end of the drop
    art = pearl_shadows(art, [(390, 236, 16)])
    art = pearl(art, 390, 236, 16, seed=77)
    art = pearl(art, 390, 222, 9, seed=78)
    area = np.zeros((H, W), np.float32)
    art = white_rose(art, W, H, 390, 34, 30, rng, nx, area)
    art = white_rose(art, W, H, 350, 40, 13, rng, nx)
    art = white_rose(art, W, H, 430, 42, 13, rng, nx)
    preview(art, "tm-strand", tone="#f6f2ea")
    save_full(art, f"{OUT}/strand.webp", quality=84)
    clear()

if "medallion" in PARTS:
    W = H = 640
    cx = cy = 320
    nx = Seq(20200); rng = random.Random(5)
    art = blank(W, H)
    # faint champagne wash inside
    disc = circles(W, H, [(cx, cy, 262)])
    art = G(art, disc, "#f3ede2", "#e7eadf", seed=nx(), density=0.35, edge=0.25, bloom=0.5, rough=6)
    art = FO(art, ring_mask(W, H, cx, cy, 277, 2.0), CHAMP, seed=nx(), emboss=0.4, sparkle=0.08)
    art = FO(art, ring_mask(W, H, cx, cy, 250, 1.2), CHAMP, seed=nx(), emboss=0.3, sparkle=0.05)
    # wreath: sage sprigs hugging the lower arc, both sides meeting under a rose
    for side in (-1, 1):
        pts = [(cx + math.cos(math.pi / 2 + side * (0.22 + 1.5 * t)) * 292, cy + math.sin(math.pi / 2 + side * (0.22 + 1.5 * t)) * 292) for t in [i / 39 for i in range(40)]]
        art = sprig(art, W, H, pts, rng, nx, L=46, every=3)
    outer = [(cx + math.cos(a) * 292, cy + math.sin(a) * 292, 10.5) for a in [k * math.tau / 96 for k in range(96)]]
    inner = [(cx + math.cos(a + 0.03) * 262, cy + math.sin(a + 0.03) * 262, 4.6) for a in [k * math.tau / 160 for k in range(160)]]
    art = draw_pearls(art, inner, seed=40)
    art = draw_pearls(art, outer, seed=500)
    area = np.zeros((H, W), np.float32)
    art = white_rose(art, W, H, cx, cy + 296, 44, rng, nx, area)
    art = white_rose(art, W, H, cx - 56, cy + 284, 28, rng, nx, area)
    art = white_rose(art, W, H, cx + 54, cy + 288, 26, rng, nx, area)
    art = white_rose(art, W, H, cx - 92, cy + 268, 13, rng, nx)
    art = white_rose(art, W, H, cx + 90, cy + 270, 13, rng, nx)
    # top: a single small pearl cluster
    art = draw_pearls(art, [(cx - 16, cy - 292, 8), (cx + 16, cy - 292, 8), (cx, cy - 306, 12)], seed=900)
    preview(art, "tm-medallion", tone="#f6f2ea")
    save(art, f"{OUT}/medallion.webp", max_w=600, quality=82)
    clear()

if "roses" in PARTS:
    W, H = 720, 600
    nx = Seq(20300); rng = random.Random(11)
    flowers = blank(W, H); area = np.zeros((H, W), np.float32)
    for (x, y, r) in [(210, 420, 92), (380, 470, 70), (110, 270, 64), (300, 300, 50)]:
        flowers = white_rose(flowers, W, H, x, y, r, rng, nx, area)
    back = blank(W, H)
    for pts, L in [(curve([(200, 430), (330, 330), (470, 300), (620, 250)], 40), 50), (curve([(160, 380), (120, 240), (150, 120), (230, 40)], 40), 46),
                   (curve([(300, 480), (450, 460), (580, 500), (700, 470)], 40), 40), (curve([(150, 420), (60, 360), (20, 250)], 30), 40)]:
        back = sprig(back, W, H, pts, rng, nx, L=L, every=3)
    # round eucalyptus-ish leaves in pale sage
    for (x, y, rr) in [(470, 380, 22), (520, 410, 18), (560, 360, 16), (250, 210, 20), (210, 160, 16), (60, 470, 20)]:
        back = G(back, shapes(W, H, [deform(ellipse_pts(x, y, rr, rr * 0.86, 10), rng, 2, 0.08)]), "#c8d3bd", SAGE_A, seed=nx(), density=0.6, edge=0.55, bloom=0.4, rough=3)
    back = knockout(back, area, amount=0.95, grow=4)
    art = glaze(back, flowers)
    for (x, y, s_, a) in [(500, 300, 17, -0.6), (420, 380, 16, -0.2), (90, 170, 16, -1.9), (640, 440, 15, 0.3)]:
        art = white_rose(art, W, H, x, y, 13, rng, nx)
    # a loose pearl strand weaving through the bouquet
    art = draw_pearls(art, string_pearls(curve([(40, 540), (200, 560), (330, 520), (440, 540), (560, 590)], 80), 7, seed=8), seed=1200)
    art = dots(art, W, H, rng, nx, 300, 380, 160, 110, 18, "#d7b4a6")
    preview(art, "tm-roses", tone="#f6f2ea")
    save(art, f"{OUT}/roses.webp", max_w=560, quality=80)
    clear()

if "divider" in PARTS:
    W, H = 440, 70
    nx = Seq(20400); rng = random.Random(21)
    art = blank(W, H)
    art = sprig(art, W, H, curve([(220, 36), (180, 30), (140, 38)], 12), rng, nx, L=22, every=3)
    art = sprig(art, W, H, curve([(220, 36), (260, 30), (300, 38)], 12), rng, nx, L=22, every=3)
    l = string_pearls(catenary(16, 30, 196, 34, 8), 4.6, seed=3)
    r = string_pearls(catenary(244, 34, 424, 30, 8), 4.6, seed=4)
    art = draw_pearls(art, l + r, seed=60)
    art = pearl_shadows(art, [(220, 35, 12)])
    art = pearl(art, 220, 35, 12, seed=61)
    preview(art, "tm-divider", tone="#f6f2ea")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)

if "pearl" in PARTS:
    W = H = 96
    art = blank(W, H)
    art = pearl_shadows(art, [(46, 46, 36)])
    art = pearl(art, 46, 46, 36, seed=5)
    preview(art, "tm-pearl", tone="#f6f2ea")
    save(art, f"{OUT}/pearl.webp", max_w=64, quality=86)

if "paper" in PARTS:
    n = 512
    a = wrap_noise(n, n, 4, 40); b = wrap_noise(n, n, 7, 26); f = wrap_noise(n, n, 9, 1.2); m = wrap_noise(n, n, 12, 90)
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#f7f4ee"), np.float32)
    base *= (0.975 + 0.035 * m + 0.03 * (f - 0.5))[..., None]
    tint = lerp3("#f6e6e8", "#e6efe4", a) * 0.5 + lerp3("#e9e9f4", "#f6efdf", b) * 0.5
    rgb = base * 0.84 + tint * 0.16
    art = np.concatenate([rgb, np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/paper.webp", quality=70)

kb(OUT)
