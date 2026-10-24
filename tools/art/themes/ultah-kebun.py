"""Ultah Kebun — little-gardener birthday in matte gouache: a picket-fence garden bed with smiling vegetables
(carrot, tomato, eggplant, radish), terracotta pots with daisies and seedlings, a small trowel, a tilted watering can
(animated separately), a wooden name sign, a sprout divider and a single carrot friend.
Run: python3 -I ultah-kebun.py [part ...]  parts: kebun siram papan pot tunas wortel
Assets -> public/themes/art/ultah-kebun/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q2_lib import *

OUT = outdir("ultah-kebun")
PARTS = sys.argv[1:] or ["kebun", "siram", "papan", "pot", "tunas", "wortel"]
SOIL, SOIL_D, SOIL_L = "#7a4f33", "#5a3622", "#9a6a46"
FENCE, FENCE_D = "#f6efe0", "#d8cdb6"
LEAF, LEAF_D, LEAF_L = "#6fa04a", "#4d7d33", "#9cc46a"
CARROT, CARROT_D = "#f08a2c", "#d26a1c"
TOMATO, TOMATO_D = "#e2493a", "#b9322a"
EGG, EGG_D = "#7a4a8e", "#5a3370"
RADISH, RADISH_D = "#e8678a", "#c94d70"
TERRA, TERRA_D, TERRA_L = "#d27a4f", "#b05d38", "#e49a70"
CAN, CAN_D = "#4fb3a9", "#34918a"
FACE = "#3a2620"
CHEEK = "#f29a9a"


def face(art, W, H, x, y, s, seed, look=0.0):
    """Friendly face: two dot eyes with a highlight, a small smile, rosy cheeks."""
    e = [(x - s * 0.9 + look, y, s * 0.32), (x + s * 0.9 + look, y, s * 0.32)]
    art = GP(art, ellipses(W, H, [(cx, cy, r * 0.9, r * 1.15, 0) for cx, cy, r in e]), FACE, seed=seed, rough=0.6, streak=0.1)
    art = OV(art, circles(W, H, [(cx + r * 0.35, cy - r * 0.4, r * 0.32) for cx, cy, r in e]), lambda q: flat(q, "#ffffff", 0.95))
    smile = arc_pts(x + look, y + s * 0.35, s * 0.7, 0.35, math.pi - 0.35, 14, 0.8)
    art = GP(art, strokes(W, H, [(smile, max(1.6, s * 0.2), (0.2, 0.2))]), FACE, seed=seed + 1, rough=0.5, streak=0.1)
    art = G(art, circles(W, H, [(x - s * 1.6 + look, y + s * 0.6, s * 0.42), (x + s * 1.6 + look, y + s * 0.6, s * 0.42)]), CHEEK, seed=seed + 2, density=0.55, edge=0.2, bloom=0.1, rough=1.5, feather=1.5)
    return art


def shade(art, mask, col, amt=0.35, dx=1, seed=1):
    """Side shading painted as a second, darker gouache pass on one side of a form."""
    h, w = mask.shape
    sh = np.roll(mask, int(dx), 1)
    side = np.clip(mask - sh, 0, 1)
    side = gaussian_filter(side, 4) * mask
    return GP(art, np.clip(side * 2.2, 0, 1) * amt * 2.5, col, seed=seed, rough=1.0, streak=0.6, density=0.6)


def leafy_top(art, W, H, x, y, n, L, spread, seed, col=LEAF, col2=LEAF_D):
    rng = random.Random(seed)
    lv = []
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * spread / max(1, n - 1) + rng.uniform(-0.08, 0.08)
        lv.append(petal_pts(x, y, L * rng.uniform(0.85, 1.1), L * 0.22, a, n=14))
    m = shapes(W, H, lv)
    art = GP(art, m, col, col2, seed=seed, rough=1.6, streak=0.6)
    veins = [([(x, y), (x + math.cos(-math.pi / 2 + (i - (n - 1) / 2) * spread / max(1, n - 1)) * L * 0.75, y + math.sin(-math.pi / 2 + (i - (n - 1) / 2) * spread / max(1, n - 1)) * L * 0.75)], 1.6, (0.0, 0.5)) for i in range(n)]
    art = GP(art, strokes(W, H, veins), col2, seed=seed + 1, rough=0.4, streak=0.2, density=0.7)
    return art


def carrot(art, W, H, x, y, s, seed, tilt=0.0):
    """Carrot standing in the soil, top half out."""
    art = leafy_top(art, W, H, x, y - s * 1.55, 5, s * 1.1, 1.3, seed)
    body = [(x - s * 0.62, y - s * 1.5), (x + s * 0.62, y - s * 1.5), (x + s * 0.5, y - s * 0.2), (x + s * 0.2, y + s * 0.9), (x, y + s * 1.1), (x - s * 0.2, y + s * 0.9), (x - s * 0.5, y - s * 0.2)]
    body = rot_pts(body, x, y, tilt)
    m = shape_mask(W, H, body)
    art = GP(art, m, CARROT, CARROT_D, seed=seed + 2, rough=1.4, streak=0.6)
    art = shade(art, m, CARROT_D, 0.35, s * 0.25, seed + 3)
    rings = [([(x - s * 0.45 + k * 0.05 * s, y - s * (0.9 - k * 0.35)), (x - s * 0.15, y - s * (0.85 - k * 0.35))], 1.8, (0.2, 0.3)) for k in range(3)]
    art = GP(art, strokes(W, H, rings), CARROT_D, seed=seed + 4, rough=0.4, density=0.8)
    return face(art, W, H, x + s * 0.02, y - s * 0.95, s * 0.22, seed + 5)


def tomato(art, W, H, x, y, s, seed):
    body = ellipse_pts(x, y, s, s * 0.86, 28)
    m = shape_mask(W, H, body)
    art = GP(art, m, TOMATO, TOMATO_D, seed=seed, rough=1.6, streak=0.5)
    art = shade(art, m, TOMATO_D, 0.4, s * 0.25, seed + 1)
    art = OV(art, shape_mask(W, H, ellipse_pts(x - s * 0.45, y - s * 0.4, s * 0.22, s * 0.12, 14, -0.6)), lambda q: flat(q, "#ffd2c6", 0.7))
    cal = []
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * 0.62
        cal.append(petal_pts(x, y - s * 0.78, s * 0.42, s * 0.12, a + (math.pi if abs(i - 2) == 2 else 0) * 0, n=10))
    star = [petal_pts(x, y - s * 0.8, s * 0.45, s * 0.13, a, n=10) for a in np.linspace(0, math.tau, 6)[:-1] + 0.3]
    art = GP(art, shapes(W, H, star), LEAF, LEAF_D, seed=seed + 2, rough=0.8)
    art = GP(art, strokes(W, H, [([(x, y - s * 0.82), (x + s * 0.08, y - s * 1.12)], s * 0.1, (0.0, 0.2))]), LEAF_D, seed=seed + 3, rough=0.4)
    return face(art, W, H, x, y + s * 0.05, s * 0.2, seed + 4)


def eggplant(art, W, H, x, y, s, seed, tilt=0.35):
    body = [(x + math.cos(t) * s * (0.55 + 0.45 * (math.sin(t) * 0.5 + 0.5)), y + math.sin(t) * s * 1.05) for t in np.linspace(0, math.tau, 40)[:-1]]
    body = rot_pts(body, x, y, tilt)
    m = shape_mask(W, H, body)
    art = GP(art, m, EGG, EGG_D, seed=seed, rough=1.4, streak=0.5)
    art = shade(art, m, EGG_D, 0.45, s * 0.25, seed + 1)
    tx, ty = rot_pts([(x, y - s * 0.95)], x, y, tilt)[0]
    cap = [petal_pts(tx, ty, s * 0.42, s * 0.16, tilt + math.pi / 2 + d, n=10) for d in (-0.9, -0.3, 0.3, 0.9)]
    art = GP(art, shapes(W, H, cap), LEAF, LEAF_D, seed=seed + 2, rough=0.8)
    art = GP(art, strokes(W, H, [([(tx, ty), (tx + s * 0.05, ty - s * 0.32)], s * 0.12, (0.0, 0.2))]), LEAF_D, seed=seed + 3, rough=0.4)
    fx, fy = rot_pts([(x, y + s * 0.15)], x, y, tilt)[0]
    return face(art, W, H, fx, fy, s * 0.18, seed + 4)


def radish(art, W, H, x, y, s, seed):
    art = leafy_top(art, W, H, x, y - s * 0.8, 3, s * 1.0, 0.9, seed, LEAF_L, LEAF)
    body = [(x + math.cos(t) * s * 0.8 * (1 - 0.35 * max(0, math.sin(t))), y + math.sin(t) * s * (0.8 if math.sin(t) < 0 else 1.0)) for t in np.linspace(0, math.tau, 36)[:-1]]
    m = shape_mask(W, H, body)
    art = GP(art, m, RADISH, RADISH_D, seed=seed + 1, rough=1.2)
    art = shade(art, m, RADISH_D, 0.4, s * 0.2, seed + 2)
    art = GP(art, strokes(W, H, [([(x, y + s * 0.95), (x + s * 0.1, y + s * 1.4)], 2.2, (0.0, 0.8))]), "#f6d6de", seed=seed + 3, rough=0.4)
    return face(art, W, H, x, y + s * 0.05, s * 0.18, seed + 4)


def daisy(art, W, H, x, y, r, seed, col="#ffffff", core="#f4b93a"):
    pet = [petal_pts(x, y, r, r * 0.3, a, n=10) for a in np.linspace(0, math.tau, 10)[:-1]]
    art = GP(art, shapes(W, H, pet), col, "#f1e7d6", seed=seed, rough=0.8, streak=0.3)
    return GP(art, circles(W, H, [(x, y, r * 0.32)]), core, "#e89a2a", seed=seed + 1, rough=0.6)


def pot_at(art, W, H, x, y, s, seed, plant="daisy"):
    """Terracotta pot (rim + body), its bottom at y."""
    body = [(x - s * 0.62, y - s * 1.05), (x + s * 0.62, y - s * 1.05), (x + s * 0.45, y), (x - s * 0.45, y)]
    rim = [(x - s * 0.75, y - s * 1.3), (x + s * 0.75, y - s * 1.3), (x + s * 0.72, y - s * 1.02), (x - s * 0.72, y - s * 1.02)]
    if plant == "daisy":
        stems = [([(x + d * s * 0.2, y - s * 1.2), (x + d * s * 0.45, y - s * 2.2 - abs(d) * 0.2 * s)], s * 0.08, (0.0, 0.1)) for d in (-1, 0.15, 1)]
        art = GP(art, strokes(W, H, stems), LEAF_D, seed=seed, rough=0.6)
        lv = [petal_pts(x + d * s * 0.1, y - s * 1.55, s * 0.55, s * 0.17, -math.pi / 2 + d * 1.0, n=12) for d in (-1, 1)]
        art = GP(art, shapes(W, H, lv), LEAF, LEAF_D, seed=seed + 1, rough=0.8)
        for k, d in enumerate((-1, 0.15, 1)):
            art = daisy(art, W, H, x + d * s * 0.45, y - s * 2.2 - abs(d) * 0.2 * s, s * 0.36, seed + 2 + k, col=["#ffffff", "#ffd3dc", "#ffffff"][k])
    elif plant == "sprout":
        st = [([(x, y - s * 1.2), (x + s * 0.05, y - s * 1.9)], s * 0.09, (0.0, 0.1))]
        art = GP(art, strokes(W, H, st), LEAF_D, seed=seed, rough=0.5)
        lv = [petal_pts(x + s * 0.05, y - s * 1.85, s * 0.6, s * 0.26, a, n=14, cup=0.2) for a in (-0.5, math.pi + 0.5)]
        art = GP(art, shapes(W, H, lv), LEAF_L, LEAF, seed=seed + 1, rough=0.8)
    mb = shape_mask(W, H, body, smooth=False)
    art = GP(art, mb, TERRA, TERRA_D, seed=seed + 5, rough=1.2, streak=0.6)
    art = shade(art, mb, TERRA_D, 0.4, s * 0.25, seed + 6)
    mr = shape_mask(W, H, rim, smooth=False)
    art = GP(art, mr, TERRA_L, TERRA, seed=seed + 7, rough=1.0, streak=0.5)
    art = GP(art, np.clip(mr - np.roll(mr, -int(s * 0.12), 0), 0, 1), TERRA_D, seed=seed + 8, rough=0.6, density=0.5)
    return art


def fence(art, W, H, x0, x1, y_top, y_bot, seed, pw=34, gap=14):
    pickets = []
    x = x0
    rng = random.Random(seed)
    while x < x1:
        t = y_top + rng.uniform(-4, 4)
        pickets.append([(x, y_bot), (x, t + pw * 0.45), (x + pw / 2, t), (x + pw, t + pw * 0.45), (x + pw, y_bot)])
        x += pw + gap
    rails = [rect(x0 - 10, y_top + 40, x1 + 10, y_top + 58), rect(x0 - 10, y_bot - 46, x1 + 10, y_bot - 28)]
    art = GP(art, shapes(W, H, rails, smooth=False), FENCE_D, "#c9bca2", seed=seed, rough=1.2, streak=0.8)
    m = shapes(W, H, pickets, smooth=False)
    art = GP(art, m, FENCE, FENCE_D, seed=seed + 1, rough=1.4, streak=0.9)
    art = shade(art, m, "#cbbfa5", 0.5, 7, seed + 2)
    nails = [(p[0][0] + pw / 2, y_top + 49, 2.2) for p in pickets] + [(p[0][0] + pw / 2, y_bot - 37, 2.2) for p in pickets]
    art = GP(art, circles(W, H, nails), "#9a8d78", seed=seed + 3, rough=0.3)
    return art


def soil_bed(art, W, H, y, seed):
    top = [(x, y + 6 * math.sin(x / 37) + 4 * math.sin(x / 13)) for x in range(-10, W + 11, 10)]
    m = shape_mask(W, H, top + [(W + 10, H + 10), (-10, H + 10)], smooth=False)
    art = GP(art, m, SOIL, SOIL_D, seed=seed, rough=2.0, streak=0.9)
    rng = random.Random(seed)
    clods = [(rng.uniform(0, W), rng.uniform(y + 14, H - 6), rng.uniform(3, 7), rng.uniform(2, 4), rng.uniform(0, 180)) for _ in range(70)]
    art = GP(art, ellipses(W, H, clods), SOIL_L, seed=seed + 1, rough=0.6, density=0.75)
    furrow = [([(x, yy + 3 * math.sin(x / 30)) for x in range(0, W, 12)], 3.0, (0.05, 0.05)) for yy in (y + 34, y + 62)]
    art = GP(art, strokes(W, H, furrow), SOIL_D, seed=seed + 2, rough=0.8, density=0.6)
    return art


def sprouts(art, W, H, pts, s, seed):
    st, lv = [], []
    for x, y in pts:
        st.append(([(x, y), (x + s * 0.05, y - s * 0.7)], s * 0.12, (0.0, 0.1)))
        lv += [petal_pts(x + s * 0.05, y - s * 0.68, s * 0.55, s * 0.25, a, n=12, cup=0.25) for a in (-0.45, math.pi + 0.45)]
    art = GP(art, strokes(W, H, st), LEAF_D, seed=seed, rough=0.4)
    return GP(art, shapes(W, H, lv), LEAF_L, LEAF, seed=seed + 1, rough=0.8)


def trowel(art, W, H, x, y, s, ang, seed):
    blade = [(0, -s * 0.05), (s * 0.15, -s * 0.2), (s * 0.62, -s * 0.16), (s * 0.85, 0), (s * 0.62, s * 0.16), (s * 0.15, s * 0.2), (0, s * 0.05)]
    blade = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang)) for px, py in blade]
    shaft = [([(x, y), (x - math.cos(ang) * s * 0.35, y - math.sin(ang) * s * 0.35)], s * 0.06, None)]
    hand = [([(x - math.cos(ang) * s * 0.33, y - math.sin(ang) * s * 0.33), (x - math.cos(ang) * s * 0.85, y - math.sin(ang) * s * 0.85)], s * 0.2, None)]
    art = GP(art, strokes(W, H, shaft), "#9aa3a8", seed=seed, rough=0.4)
    art = GP(art, strokes(W, H, hand), "#f2c94c", "#e0a92e", seed=seed + 1, rough=0.6)
    mb = shape_mask(W, H, blade, smooth=True)
    art = GP(art, mb, "#b9c4c9", "#8f9ba1", seed=seed + 2, rough=0.8, streak=0.8)
    return art


def kebun():
    W, H = 820, 470
    art = blank(W, H)
    rng = random.Random(3)
    art = fence(art, W, H, 10, W - 10, 120, 360, 5)
    clear()
    # vegetables growing in front of the fence, peeking above the soil
    art = soil_bed(art, W, H, 336, 9)
    art = carrot(art, W, H, 300, 352, 62, 21, -0.05)
    art = tomato_plant(art, W, H, 455, 352, 23)
    art = eggplant(art, W, H, 590, 300, 50, 31, 0.3)
    art = radish(art, W, H, 680, 352, 34, 41)
    clear()
    art = sprouts(art, W, H, [(220, 372), (372, 384), (520, 380), (720, 386)], 34, 51)
    art = pot_at(art, W, H, 92, 452, 72, 61, "daisy")
    art = pot_at(art, W, H, 178, 458, 44, 71, "sprout")
    art = trowel(art, W, H, 760, 368, 110, 1.85, 81)
    preview(art, "uk-kebun", tone="#eaf3dc")
    save(art, f"{OUT}/kebun.webp", max_w=780, quality=80)


def tomato_plant(art, W, H, x, y, seed):
    st = [([(x, y), (x - 6, y - 120), (x + 4, y - 210)], 5, (0.0, 0.1)), ([(x - 4, y - 90), (x - 46, y - 140)], 3.4, (0.0, 0.2)), ([(x + 0, y - 150), (x + 50, y - 190)], 3.2, (0.0, 0.2))]
    art = GP(art, strokes(W, H, st), LEAF_D, seed=seed, rough=0.6)
    lv = [petal_pts(x - 4, y - 60, 46, 16, math.pi + 0.5, n=12), petal_pts(x + 2, y - 110, 44, 15, -0.3, n=12), petal_pts(x + 2, y - 205, 40, 14, -1.2, n=12),
          petal_pts(x - 40, y - 138, 36, 12, -2.4, n=12)]
    art = GP(art, shapes(W, H, lv), LEAF, LEAF_D, seed=seed + 1, rough=1.0)
    stake = [([(x + 22, y + 10), (x + 22, y - 230)], 7, None)]
    art = GP(art, strokes(W, H, stake), "#b98a5a", "#9a6e44", seed=seed + 2, rough=0.6)
    art = tomato(art, W, H, x - 48, y - 118, 30, seed + 3)
    art = tomato(art, W, H, x + 50, y - 168, 24, seed + 9)
    return art


def siram():
    """Watering can, tilted to pour (spout to the lower left)."""
    W, H = 360, 280
    art = blank(W, H)
    cx, cy = 210, 150
    body = [(cx - 70, cy - 60), (cx + 70, cy - 60), (cx + 78, cy + 70), (cx - 78, cy + 70)]
    spout = [(cx - 66, cy + 20), (cx - 160, cy - 40), (cx - 168, cy - 30), (cx - 70, cy + 44)]
    rose = ellipse_pts(cx - 170, cy - 40, 16, 24, 18, -0.6)
    handle = [arc_pts(cx, cy - 66, 60, math.pi * 1.05, math.pi * 1.95, 30, 0.9)]
    art = GP(art, strokes(W, H, [(handle[0], 14, None)]), CAN_D, seed=1, rough=0.8)
    art = GP(art, shape_mask(W, H, spout, smooth=False), CAN, CAN_D, seed=2, rough=1.0)
    art = GP(art, shape_mask(W, H, rose), CAN_D, seed=3, rough=0.8)
    art = GP(art, circles(W, H, [(cx - 176 + dx, cy - 44 + dy, 2.2) for dx, dy in [(0, -8), (4, 2), (-4, 10), (-8, 0), (2, 12)]]), "#2a6e68", seed=4, rough=0.2)
    mb = shape_mask(W, H, body)
    art = GP(art, mb, CAN, CAN_D, seed=5, rough=1.2, streak=0.8)
    art = shade(art, mb, CAN_D, 0.45, 20, 6)
    band = shape_mask(W, H, [(cx - 74, cy - 10), (cx + 74, cy - 10), (cx + 75, cy + 6), (cx - 75, cy + 6)], smooth=False)
    art = GP(art, band, "#f6efe0", seed=7, rough=0.6)
    art = daisy(art, W, H, cx + 10, cy + 34, 18, 8, col="#ffd3dc")
    art = OV(art, shape_mask(W, H, ellipse_pts(cx - 44, cy - 34, 8, 20, 14, 0.1)), lambda q: flat(q, "#d9f2ee", 0.6))
    art = rotate_arr(art, 24)
    preview(art, "uk-siram", tone="#eaf3dc")
    save(art, f"{OUT}/siram.webp", max_w=300, quality=82)


def rotate_arr(arr, deg):
    im = to_image(arr).rotate(deg, resample=Image.BICUBIC, expand=True)
    return np.asarray(im, np.float32) / 255


def papan():
    """Wooden sign board (opaque planks with nails, a painted edge) — the name sits on it in HTML."""
    W, H = 660, 380
    art = blank(W, H)
    planks = [rect(20, 20 + k * 115, W - 20, 20 + (k + 1) * 115 - 6) for k in range(3)]
    cols = [("#e3b27a", "#d49d62"), ("#ddaa70", "#cc955b"), ("#e6b780", "#d6a066")]
    for k, p in enumerate(planks):
        m = shape_mask(W, H, p, smooth=False)
        art = GP(art, m, cols[k][0], cols[k][1], seed=10 + k, rough=1.6, streak=1.6)
        # wood grain strokes
        rng = random.Random(k)
        grain = []
        for g in range(7):
            y = p[0][1] + 10 + g * 14 + rng.uniform(-3, 3)
            grain.append(([(x, y + 3 * math.sin(x / rng.uniform(40, 90) + g)) for x in range(30 + rng.randint(0, 80), W - 30 - rng.randint(0, 80), 14)], 1.6, (0.1, 0.1)))
        art = GP(art, strokes(W, H, grain), "#b9824c", seed=20 + k, rough=0.4, density=0.55)
        knot = ellipse_pts(rng.uniform(80, W - 80), p[0][1] + 55, 9, 5, 14)
        art = GP(art, shape_mask(W, H, knot), "#a8723f", seed=30 + k, rough=0.4, density=0.8)
    # inner light panel (where text sits) — a soft lighter wash
    art = OV(art, shape_mask(W, H, rect(60, 52, W - 60, H - 52)), lambda q: flat(gaussian_filter(q, 14), "#f7e3c3", 0.55))
    # nails
    nails = [(44, 77, 6), (W - 44, 77, 6), (44, 192, 6), (W - 44, 192, 6), (44, 306, 6), (W - 44, 306, 6)]
    art = GP(art, circles(W, H, nails), "#8a8a86", "#6b6b68", seed=40, rough=0.3)
    art = OV(art, circles(W, H, [(x - 1.5, y - 1.5, 2) for x, y, _ in nails]), lambda q: flat(q, "#e9e9e4", 0.9))
    preview(art, "uk-papan", tone="#eaf3dc")
    save(art, f"{OUT}/papan.webp", max_w=600, quality=78)


def pot():
    W, H = 240, 300
    art = blank(W, H)
    art = pot_at(art, W, H, 120, 290, 100, 91, "sprout")
    preview(art, "uk-pot", tone="#eaf3dc")
    save(art, f"{OUT}/pot.webp", max_w=180, quality=84)


def tunas():
    W, H = 520, 110
    art = blank(W, H)
    top = [(x, 82 + 3 * math.sin(x / 20)) for x in range(70, 451, 10)]
    m = shape_mask(W, H, [(60, 96)] + top + [(460, 96), (440, 104), (80, 104)])
    art = GP(art, m, SOIL, SOIL_D, seed=3, rough=1.2, streak=0.8)
    art = sprouts(art, W, H, [(150, 84), (260, 82), (370, 84)], 54, 5)
    art = sprouts(art, W, H, [(205, 86), (315, 86)], 30, 7)
    art = OV(art, circles(W, H, [(40, 60, 4), (480, 52, 4), (30, 80, 3), (492, 76, 3)]), lambda q: flat(q, "#7cc3e6", 0.85))
    preview(art, "uk-tunas", tone="#eaf3dc")
    save(art, f"{OUT}/tunas.webp", max_w=420, quality=84)


def wortel():
    W, H = 240, 360
    art = blank(W, H)
    art = carrot(art, W, H, 120, 250, 70, 111, 0.12)
    # soil mound at the bottom
    art = GP(art, shape_mask(W, H, ellipse_pts(120, 330, 96, 26, 24)), SOIL, SOIL_D, seed=115, rough=1.2)
    preview(art, "uk-wortel", tone="#eaf3dc")
    save(art, f"{OUT}/wortel.webp", max_w=170, quality=84)


for p in PARTS:
    {"kebun": kebun, "siram": siram, "papan": papan, "pot": pot, "tunas": tunas, "wortel": wortel}[p]()
    clear()
