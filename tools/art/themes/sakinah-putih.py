"""Sakinah Putih — soft sage watercolour: eight-petal glazed rosette, leafy vine divider, jasmine & olive corner
spray for the cover, and a white paper grain. Run: python3 -I /tmp/pen/art/themes/sakinah-putih.py"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentD_lib import *  # noqa

T = "sakinah-putih"
OUT = outdir(T)
SAGE, SAGE2 = "#8fb39c", "#5f8f74"
DEEP = "#2f5a43"
CELADON = "#c9dccd"
WARM = "#e8d9a8"
rng = random.Random(23)
_s = [300]
def nxt():
    _s[0] += 11
    return _s[0]

# ---------------- 1. bloom rosette ----------------
S = 280; c = S / 2; k = 2.7
art = blank(S, S)
ring = circle_mask(S, S, [(c, c, 46 * k)], stroke=2.2)
art = glaze(art, pigment(ring, SAGE, CELADON, seed=nxt(), density=0.45, edge=0.4, bloom=0.2, gran=0.3, rough=1.4, feather=0.7))
dabs = [(c + math.cos(a) * 42 * k + rng.gauss(0, .5), c + math.sin(a) * 42 * k + rng.gauss(0, .5), rng.uniform(1.6, 2.6))
        for a in np.linspace(0, math.tau, 40, endpoint=False) + 0.03]
art = glaze(art, pigment(circle_mask(S, S, dabs), SAGE2, seed=nxt(), density=0.7, edge=0.3, bloom=0, gran=0.2, rough=0.6, feather=0.5))
for i in range(8):
    a = i * math.pi / 4 - math.pi / 2 + rng.gauss(0, 0.03)
    L = 33 * k * rng.uniform(0.95, 1.04)
    pm = shape_mask(S, S, deform(petal_pts(c + math.cos(a) * 2, c + math.sin(a) * 2, L, 12.5 * k, a, n=14), rng, 1, 0.03))
    col = [SAGE, "#9fbfa8", "#86ab93"][i % 3]
    art = glaze(art, pigment(pm, col, CELADON, seed=nxt(), density=0.42, edge=0.7, bloom=0.45, gran=0.3, rough=2.2, feather=0.9))
    vein = [(c + math.cos(a) * L * t, c + math.sin(a) * L * t) for t in np.linspace(0.18, 0.7, 6)]
    art = glaze(art, pigment(stroke_mask(S, S, vein, 1.6), SAGE2, seed=nxt(), density=0.35, edge=0.1, bloom=0, rough=0.6, feather=0.4))
heart = circle_mask(S, S, [(c, c, 6 * k)])
art = glaze(art, pigment(heart, WARM, "#d7c387", seed=nxt(), density=0.75, edge=0.6, bloom=0.2, gran=0.4, rough=1.2, feather=0.6))
art = glaze(art, pigment(circle_mask(S, S, [(c, c, 2.2 * k)]), DEEP, seed=nxt(), density=0.8, edge=0.3, bloom=0, rough=0.5, feather=0.5))
print("bloom", save_asset(art, f"{OUT}/bloom.webp", max_w=240, quality=84))
preview(art, paper_tone="#fdfdfb", path=f"{PREV}/sp-bloom.png")

# ---------------- 2. vine divider ----------------
VW, VH = 480, 64; vk = 2.0
stem = curve([(6, 32), (40, 18), (80, 44), (120, 30), (160, 18), (200, 42), (240, 32), (280, 20), (320, 44), (360, 30), (400, 18), (440, 42), (474, 32)], 260)
stem = [(x, y + math.sin(x / 50) * 1.5) for x, y in stem]
vine = pigment(stroke_mask(VW, VH, stem, 2.6, taper=(0.1, 0.1)), SAGE2, SAGE, seed=nxt(), density=0.8, edge=0.3, bloom=0, gran=0.2, rough=0.8, feather=0.5)
leaf_layer = blank(VW, VH)
for i, x in enumerate(range(30, 470, 36)):
    if abs(x - 240) < 24:
        continue
    j = min(range(len(stem)), key=lambda q: abs(stem[q][0] - x))
    sx_, sy_ = stem[j]
    up = i % 2 == 0
    a = (-math.pi / 2 if up else math.pi / 2) + (0.7 if x > 240 else -0.7) * (1 if up else -1) + rng.gauss(0, .15)
    Lf = rng.uniform(22, 28)
    m = shape_mask(VW, VH, petal_pts(sx_, sy_, Lf, Lf * 0.3, a, n=16))
    col = [SAGE, "#9fbfa8", SAGE2][i % 3]
    leaf_layer = glaze(leaf_layer, pigment(m, col, CELADON, seed=nxt(), density=0.62, edge=0.6, bloom=0.3, gran=0.25, rough=0.6, feather=0.5))
vine = glaze(vine, leaf_layer)
# centre bud (pale jasmine) with sage dot
bud = shape_mask(VW, VH, deform(ellipse_pts(240, 32, 8, 8, 8), rng, 1, .06))
vine = glaze(vine, pigment(bud, WARM, "#f1e6c2", seed=nxt(), density=0.55, edge=0.8, bloom=0.2, rough=0.8, feather=0.5))
vine = glaze(vine, pigment(circle_mask(VW, VH, [(240, 32, 2.6)]), SAGE2, seed=nxt(), density=0.85, edge=0.2, bloom=0, rough=0.4, feather=0.4))
print("vine", save_asset(vine, f"{OUT}/vine.webp", max_w=360, quality=84))
preview(vine, paper_tone="#fdfdfb", path=f"{PREV}/sp-vine.png")

# ---------------- 3. cover corner spray: olive leaves + jasmine ----------------
CW, CH = 460, 460
leaves = blank(CW, CH)
flowers = blank(CW, CH)
fl_area = np.zeros((CH, CW), np.float32)
# two arching olive stems from the top-left corner
branches = [
    [(-10, 40), (80, 70), (170, 120), (250, 200), (300, 290)],
    [(30, -10), (70, 80), (120, 150), (150, 240)],
    [(-10, 150), (60, 170), (120, 210)],
]
for bi, br in enumerate(branches):
    pts = curve(br, 120)
    leaves = glaze(leaves, pigment(stroke_mask(CW, CH, pts, 3.4 - bi * 0.6, taper=(0.02, 0.4)), "#7a8f72", SAGE2, seed=nxt(), density=0.7, edge=0.3, bloom=0, rough=1.0, feather=0.6))
    for t in range(6, len(pts) - 4, 9):
        x, y = pts[t]
        dx, dy = pts[t + 1][0] - x, pts[t + 1][1] - y
        base = math.atan2(dy, dx)
        for side in (-1, 1):
            if rng.random() < 0.18:
                continue
            a = base + side * rng.uniform(0.55, 0.9)
            Lf = rng.uniform(34, 52) * (1 - t / len(pts) * 0.35)
            m = shape_mask(CW, CH, petal_pts(x, y, Lf, Lf * 0.24, a, n=12, cup=side * 0.15))
            col = rng.choice([SAGE, "#9fbfa8", "#7fa58c", "#a7c2ad"])
            leaves = glaze(leaves, pigment(m, col, mix(col, SAGE2, .5), seed=nxt(), density=0.55, edge=0.62, bloom=0.4, gran=0.3, rough=1.3, feather=0.6))
    # tip leaf
    x, y = pts[-1]; a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    leaves = glaze(leaves, pigment(shape_mask(CW, CH, petal_pts(x, y, 40, 10, a, n=12)), "#9fbfa8", SAGE2, seed=nxt(), density=0.55, edge=0.6, bloom=0.4, rough=2))

def jasmine(cx, cy, r, rot):
    global flowers, fl_area
    for p in range(5):
        a = rot + p * math.tau / 5
        m = shape_mask(CW, CH, deform(petal_pts(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12, r, r * 0.34, a, n=16), rng, 1, 0.03))
        fl_area = np.maximum(fl_area, m)
        # white petals: only a faint warm-grey wash with a sage-tinted wet edge so they read on white paper
        flowers = glaze(flowers, pigment(m, "#f4f1e6", "#e2e8dc", seed=nxt(), density=0.3, edge=1.0, bloom=0.3, gran=0.15, rough=0.7, feather=0.5))
    flowers = glaze(flowers, pigment(circle_mask(CW, CH, [(cx, cy, r * 0.2)]), WARM, "#d6bf7c", seed=nxt(), density=0.8, edge=0.5, bloom=0, rough=0.6, feather=0.5))

for (x, y, r) in [(150, 110, 30), (235, 175, 24), (95, 200, 22), (60, 75, 18)]:
    jasmine(x, y, r, rng.uniform(0, 1))
for (x, y, s_) in [(306, 262, 8), (172, 248, 7), (288, 142, 6)]:   # buds
    m = shape_mask(CW, CH, deform(ellipse_pts(x, y, s_ * 0.6, s_, 8, rng.uniform(0, 3)), rng, 1, .08))
    fl_area = np.maximum(fl_area, m)
    flowers = glaze(flowers, pigment(m, "#dfe9dc", "#c9dccd", seed=nxt(), density=0.55, edge=0.9, rough=0.6, feather=0.5))
leaves = knockout(leaves, fl_area, amount=0.85, grow=2.0)
corner = glaze(leaves, flowers)
def specks(cv):
    for _ in range(26):
        cv.c.drawCircle(150 + rng.gauss(0, 110), 150 + rng.gauss(0, 100), rng.uniform(1, 3), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
corner = glaze(corner, pigment(mask_from(CW, CH, specks), SAGE, seed=nxt(), density=0.45, edge=0.2, bloom=0, rough=0.5, feather=0.5))
save_plain(corner, f"{OUT}/corner.webp", quality=82)
preview(corner, paper_tone="#fdfdfb", path=f"{PREV}/sp-corner.png")

# ---------------- 4. white paper grain ----------------
pp = seamless_paper(512, 512, "#fefefc", seed=41, mottle=0.3, fiber=0.6, fine=0.55)
save_plain(pp, f"{OUT}/paper.webp", quality=80)

tot = 0
for f in sorted(os.listdir(OUT)):
    tot += kb(f"{OUT}/{f}"); print(f, kb(f"{OUT}/{f}"), "KB", Image.open(f"{OUT}/{f}").size)
print("total", round(tot, 1), "KB")
