"""Aqiqah Bintang — nursery watercolour: sleeping crescent moon + swaddled baby (split for the rocking motion),
puffy gouache-white clouds with lilac wet shadows, painted crib-mobile pieces and a scattered painted-star tile.
Run: python3 -I /tmp/pen/art/themes/aqiqah-bintang.py
Pigments: butter (#ffe29a/#f5c25e), blush (#f6b9c6/#e88fa3), periwinkle (#aebcf0/#8796d8), mint (#bfe8d6), peach skin (#fcd9c2).
"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *

OUT = "/root/w/frontend/public/themes/art/aqiqah-bintang"
PREV = "/tmp/pen/nt2-E"
os.makedirs(OUT, exist_ok=True)
seed = [500]
def nxt():
    seed[0] += 11
    return seed[0]

def circ(W, H, x, y, r):
    return mask_from(W, H, lambda cv: cv.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)))

def save_full(arr, path, size, quality=82):
    """Save without trimming so split layers stay registered."""
    to_image(arr).resize(size, Image.LANCZOS).save(path, "WEBP", quality=quality, method=6)

def star_pts(cx, cy, r, rot=-math.pi / 2, inner=0.5):
    return [(cx + math.cos(rot + i * math.pi / 5) * (r if i % 2 == 0 else r * inner), cy + math.sin(rot + i * math.pi / 5) * (r if i % 2 == 0 else r * inner)) for i in range(10)]

def soft_star(W, H, cx, cy, r, ca, cb, rng, rot=None):
    pts = star_pts(cx, cy, r, rot if rot is not None else -math.pi / 2 + rng.uniform(-.25, .25), 0.52)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.03), smooth=False)
    m = gaussian_filter(m, max(0.6, r * 0.04))          # rounded, puffy points
    return pigment(m, ca, cb, seed=nxt(), density=0.85, edge=0.6, bloom=0.25, gran=0.2, rough=max(1.0, r * .05), feather=0.7)

# ---------------------------------------------------------------- moon + baby (registered layers)
S = 2.4
W, H = int(220 * S), int(190 * S)
rng = random.Random(12)
P = lambda x, y: (x * S, y * S)
outer = circ(W, H, *P(104, 98), 84 * S)
bite = circ(W, H, *P(138, 70), 66 * S)
cres = np.clip(outer - bite, 0, 1)
moon = blank(W, H)
moon = glaze(moon, pigment(cres, "#ffe6a6", "#fbd27a", seed=nxt(), density=0.8, edge=0.55, bloom=0.4, gran=0.25, rough=5))
inner_sh = stroke_mask(W, H, arc_pts(*P(138, 70), 70 * S, 1.2, 3.6, 40), 22 * S * 0.6) * cres
moon = glaze(moon, pigment(gaussian_filter(inner_sh, 6), "#f2b955", seed=nxt(), density=0.5, edge=0.2, bloom=0.3, rough=3, feather=3))
for (cx_, cy_, rr) in ((70, 46, 6), (52, 62, 4.5), (86, 170, 5)):
    m = circ(W, H, *P(cx_, cy_), rr * S) * cres
    moon = glaze(moon, pigment(m, "#f4c467", seed=nxt(), density=0.35, edge=0.6, bloom=0, rough=2))
# sleeping face: closed eye, cheek, smile (rigger strokes)
eye = stroke_mask(W, H, curve([P(38, 96), P(46, 102), P(54, 96)], 20), 3.0 * S * .7, taper=(0.2, 0.2))
smile = stroke_mask(W, H, curve([P(44, 126), P(52, 131), P(60, 126)], 20), 2.6 * S * .7, taper=(0.2, 0.3))
moon = glaze(moon, pigment(np.maximum(eye, smile), "#8a6431", seed=nxt(), density=0.85, edge=0.3, bloom=0, rough=1.2, feather=0.6))
cheek = shape_mask(W, H, deform(ellipse_pts(*P(40, 112), 7.5 * S, 6.5 * S, 9), rng, 2, .1))
moon = glaze(moon, pigment(cheek, "#f7a7b4", "#f28da0", seed=nxt(), density=0.55, edge=0.6, bloom=0.3, rough=2.5))

baby = blank(W, H)
def swaddle(p):
    pts = [P(78, 150), P(74, 132), P(94, 118), P(124, 116), P(152, 115), P(168, 122), P(170, 132), P(162, 146), P(140, 154), P(110, 158), P(84, 156)]
    p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
def path_mask(build):
    def draw(cv):
        p = skia.Path(); build(p); cv.c.drawPath(smooth_path([(p.getPoint(i).fX, p.getPoint(i).fY) for i in range(p.countPoints())]), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)
sw = path_mask(swaddle)
head = circ(W, H, *P(172, 118), 20 * S)
cap_pts = [P(156, 110), P(160, 100), P(172, 94), P(186, 96), P(192, 104), P(184, 102), P(174, 103), P(166, 106)]
cap = shape_mask(W, H, cap_pts, smooth=False)
cap = gaussian_filter(cap, 1.5)
under = np.clip(np.maximum(np.maximum(sw, head), cap), 0, 1)
baby = over(baby, gouache_paint(under, "#fffaf6", seed=nxt(), rough=2, streak=0.2, density=1.0))
sw = np.clip(sw - np.clip(gaussian_filter(head, 2) * 1.6, 0, 1), 0, 1)
baby = glaze(baby, pigment(sw, "#f9c7d2", "#f3aebf", seed=nxt(), density=0.82, edge=0.55, bloom=0.4, gran=0.2, rough=4))
for pts in ([P(96, 130), P(124, 125), P(154, 130)], [P(92, 142), P(122, 137), P(158, 143)]):
    fold = stroke_mask(W, H, curve(pts, 30), 3.4 * S * .8, taper=(0.3, 0.3)) * sw
    baby = glaze(baby, pigment(fold, "#e88fa3", seed=nxt(), density=0.6, edge=0.3, bloom=0, rough=1.5, feather=0.8))
shade = shape_mask(W, H, deform(ellipse_pts(*P(118, 152), 46 * S, 9 * S, 10), rng, 2, .1)) * sw
baby = glaze(baby, pigment(shade, "#e391a6", seed=nxt(), density=0.35, edge=0.2, bloom=0.2, rough=3, feather=4))
baby = glaze(baby, pigment(head, "#fde0cc", "#f9cdb2", seed=nxt(), density=0.8, edge=0.25, bloom=0.0, gran=0.1, rough=1.5))
baby = glaze(baby, pigment(cap, "#c9d4ff", "#a9b7ee", seed=nxt(), density=0.85, edge=0.6, bloom=0.3, rough=2))
baby = glaze(baby, pigment(circ(W, H, *P(191, 99), 4.4 * S), "#ffd37a", "#f5b955", seed=nxt(), density=0.9, edge=0.6, rough=1.5))
eye2 = stroke_mask(W, H, curve([P(162.5, 120), P(167, 123.5), P(171.5, 120)], 16), 2.2 * S * .7, taper=(0.25, 0.25))
baby = glaze(baby, pigment(eye2, "#5b4636", seed=nxt(), density=0.85, edge=0.2, bloom=0, rough=1, feather=0.5))
baby = glaze(baby, pigment(circ(W, H, *P(164, 128.5), 4 * S), "#f7a7b4", seed=nxt(), density=0.5, edge=0.6, bloom=0.2, rough=2))
mouth = stroke_mask(W, H, curve([P(176, 131), P(179, 133), P(182, 131)], 10), 1.8 * S * .8, taper=(0.3, 0.3))
baby = glaze(baby, pigment(mouth, "#c98a7a", seed=nxt(), density=0.8, edge=0.2, bloom=0, rough=1, feather=0.5))

save_full(moon, f"{OUT}/moon.webp", (480, int(480 * H / W)))
save_full(baby, f"{OUT}/baby.webp", (480, int(480 * H / W)))
print("moon/baby", os.path.getsize(f"{OUT}/moon.webp"), os.path.getsize(f"{OUT}/baby.webp"), (480, int(480 * H / W)))
both = glaze(moon, baby)
pv = np.asarray(paper(W, H, "#efe6f6", 3), np.float32) / 255
a = both[..., 3:4]
Image.fromarray((np.clip(pv * (1 - a) + both[..., :3] * a, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/ab-moonbaby.png")

# ---------------------------------------------------------------- clouds: gouache white body + lilac wet shadow underneath
def cloud(W, H, lobes, seedbase, flat_bottom=True):
    rng = random.Random(seedbase)
    m = np.zeros((H, W), np.float32)
    for (x, y, r) in lobes:
        m = np.maximum(m, circ(W, H, x, y, r))
    if flat_bottom:
        base_y = max(y + r * 0.55 for x, y, r in lobes)
        m[int(base_y):, :] *= 0
        m = gaussian_filter(m, 2)
    art = blank(W, H)
    art = over(art, gouache_paint(m, "#ffffff", "#fbf8ff", seed=nxt(), rough=3, streak=0.3, density=0.97))
    # lilac shadow on the underside + a few bluish wet-in-wet blooms
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    ys = np.where(m.sum(1) > 0)[0]
    lo, hi = ys.min(), ys.max()
    under = np.clip((yy - (lo + (hi - lo) * 0.55)) / ((hi - lo) * 0.45), 0, 1) * m
    art = glaze(art, pigment(under, "#d9dcf7", "#c6cdf3", seed=nxt(), density=0.7, edge=0.35, bloom=0.4, rough=4, feather=3))
    for _ in range(3):
        x, y, r = lobes[rng.randrange(len(lobes))]
        bm = shape_mask(W, H, deform(ellipse_pts(x + rng.uniform(-r, r) * .4, y + r * .3, r * .5, r * .3, 9), rng, 2, .15)) * m
        art = glaze(art, pigment(bm, "#e5e3fa", seed=nxt(), density=0.4, edge=0.5, bloom=0.4, rough=3))
    return art

W, H = 420, 230
cl = cloud(W, H, [(96, 150, 58), (176, 108, 78), (268, 118, 66), (330, 156, 48), (60, 172, 34)], 3)
print("cloud", save_asset(cl, f"{OUT}/cloud.webp", max_w=240, quality=82), os.path.getsize(f"{OUT}/cloud.webp"))
W, H = 860, 210
lobes = [(x, 150 + random.Random(int(x)).uniform(-18, 14), random.Random(int(x) + 1).uniform(52, 82)) for x in range(10, 860, 78)]
bank = cloud(W, H, lobes, 9, flat_bottom=False)
bank[150:, :, 3] = np.maximum(bank[150:, :, 3], 0)  # keep
fill = np.zeros((H, W), np.float32); fill[160:, :] = 1
bank = over(bank, gouache_paint(gaussian_filter(fill, 3), "#ffffff", "#fdfbff", seed=nxt(), rough=2, density=1.0))
print("cloud-bank", save_asset(bank, f"{OUT}/cloud-bank.webp", max_w=780, quality=80), os.path.getsize(f"{OUT}/cloud-bank.webp"))
prev = np.asarray(paper(W, H, "#dfe2fa", 4), np.float32) / 255
a = bank[..., 3:4]
Image.fromarray((np.clip(prev * (1 - a) + bank[..., :3] * a, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/ab-bank.png")

# ---------------------------------------------------------------- crib mobile pieces
W, H = 540, 96
rng = random.Random(4)
bar = blank(W, H)
arc = curve([(20, 80), (140, 34), (270, 18), (400, 34), (520, 80)], 60)
bar = glaze(bar, pigment(stroke_mask(W, H, arc, 7, taper=(0.05, 0.05)), "#b7c2ec", "#9aa8e2", seed=nxt(), density=0.85, edge=0.5, bloom=0.2, rough=1.5, feather=0.8))
bar = glaze(bar, pigment(circ(W, H, 270, 20, 11), "#ffd37a", "#f5b955", seed=nxt(), density=0.9, edge=0.6, rough=1.5))
save_full(bar, f"{OUT}/mobile-bar.webp", (520, int(520 * H / W)))
T = 120
for name, ca, cb in (("m-star", "#ffd88a", "#f5b955"), ("m-star-mint", "#c9eedd", "#97d4ba")):
    st = soft_star(T, T, 60, 62, 44, ca, cb, random.Random(len(name)))
    print(name, save_asset(st, f"{OUT}/{name}.webp", max_w=64, quality=84))
mm = np.clip(circ(T, T, 58, 62, 42) - circ(T, T, 78, 46, 36), 0, 1)
mo = pigment(mm, "#f9c9d4", "#ee9fb2", seed=nxt(), density=0.85, edge=0.6, bloom=0.3, rough=1.5, feather=0.8)
print("m-moon", save_asset(mo, f"{OUT}/m-moon.webp", max_w=64, quality=84))

# ---------------------------------------------------------------- scattered painted stars tile (transparent)
T = 840
rng = random.Random(31)
tile = blank(T, T)
cols = [("#ffd88a", "#f5b955"), ("#f6b9c6", "#e88fa3"), ("#bcc7f3", "#8f9dde")]
placed = []
for i in range(11):
    for _ in range(80):
        x, y = rng.uniform(40, T - 40), rng.uniform(40, T - 40)
        if all(math.hypot(x - a, y - b) > 170 for a, b in placed): break
    placed.append((x, y))
    ca, cb = cols[i % 3]
    tile = glaze(tile, soft_star(T, T, x, y, rng.uniform(9, 15), ca, cb, rng))
dots = mask_from(T, T, lambda cv: [cv.c.drawCircle(rng.uniform(10, T - 10), rng.uniform(10, T - 10), rng.uniform(2.4, 4.2), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)) for _ in range(18)])
tile = glaze(tile, pigment(dots, "#c3cbf2", seed=nxt(), density=0.6, edge=0.3, bloom=0, rough=0.6, feather=0.5))
save_texture(to_image(tile).resize((560, 560), Image.LANCZOS), f"{OUT}/stars.webp", quality=82)
print("stars", os.path.getsize(f"{OUT}/stars.webp"))
on_paper(tile, "#f3ecf8").save(f"{PREV}/ab-stars.png")
