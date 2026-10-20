"""Paket Liburan — painted travel pieces for the booking-app theme: a gouache/watercolour tropical beach
header (sea, island, palm, sailboat), a separate gouache airliner that floats over it, a worn 'LUNAS'
rubber-stamp postmark, a gouache suitcase for the gift list, and a faint paper-grain tile.
Run: python3 -I /tmp/pen/art/themes/paket-liburan.py [hero plane stamp luggage paper]
The app UI itself stays crisp; only illustrations are painted."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _r2_lib import *  # noqa

T = "paket-liburan"
D = outdir(T)
nxt = Seeds(2400)
rng = random.Random(41)
BLUE, NAVY, YELLOW = "#0064d2", "#0045a0", "#ffc900"


def hero():
    W, H = 780, 360
    HZ = 222  # horizon
    art = painted_sky(W, H, [(0, "#0a5fcc"), (0.35, "#2a86e6"), (0.58, "#7fc1f2"), (0.64, "#cfe8f6"), (1.0, "#cfe8f6")], seed=nxt(), streak=0.7, grain=0.6)
    # low warm sun glow on the right horizon
    art = over(art, glow(dots_mask(W, H, [(560, HZ - 18, 30)]), "#fff1c4", radius=40, strength=0.5))
    art = over(art, gouache_paint(dots_mask(W, H, [(560, HZ - 16, 22)]), "#fff6da", "#ffe9a8", seed=nxt(), rough=1.5, streak=0.3))
    # clouds: a far watercolour band + gouache puffs lit from the sun side
    for cx, cy, rx, ry, col in [(300, 178, 240, 18, "#e7f3fd"), (640, 168, 180, 16, "#dcecfb")]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.5)
        art = over(art, pigment(m, col, "#ffffff", seed=nxt(), density=0.45, edge=0.3, bloom=0.5, rough=8, feather=3, gran=0.1))
    for cx, cy, rx, ry in [(470, 204, 56, 18), (640, 196, 44, 14)]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=5, flat=0.55)
        c = gouache_obj(m, "#fbfdff", "#e3eef9", seed=nxt(), rough=3.0, light=(0.6, -0.8), k=0.3, blur=10, hi="#fffbea", lo="#8fb3d9")
        c[..., 3] *= 0.95
        art = over(art, c)
    # island on the horizon (left) with tiny palms
    isl = shape_mask(W, H, deform([(40, HZ + 2), (90, HZ - 22), (150, HZ - 34), (210, HZ - 26), (270, HZ - 6), (300, HZ + 2)], rng, 2, 0.03))
    art = over(art, gouache_obj(isl, "#3f8f73", "#2e7560", seed=nxt(), light=(1, -0.6), k=0.25, blur=6, lo="#1b4c3f"))
    for px, ph, ln in [(146, 30, -0.2), (178, 25, 0.25), (226, 20, 0.1)]:
        a, _ = palm(W, H, px, HZ - 28 + (px - 150) * 0.12, ph, ln, rng, nxt, trunk="#4f6a55", leaf=("#2d6e57", "#245c49"), fronds=6)
        a[..., 3] *= 0.9
        art = over(art, a)
    # sea: turquoise watercolour glazes with sun glitter strokes
    sea = shape_mask(W, H, [(-20, HZ), (W + 20, HZ), (W + 20, H + 20), (-20, H + 20)], smooth=False)
    art = over(art, gouache_paint(sea, "#1f8fc4", "#2bb3c9", seed=nxt(), rough=1.0, streak=0.9))
    near = shape_mask(W, H, [(-20, HZ + 40), (W + 20, HZ + 30), (W + 20, H + 20), (-20, H + 20)], smooth=False)
    art = glaze(art, pigment(near, "#5fd0cf", "#8de0d6", seed=nxt(), density=0.55, edge=0.2, bloom=0.4, rough=10, feather=6, gran=0.2))
    gl = np.zeros((H, W), np.float32)
    for _ in range(46):
        y = rng.uniform(HZ + 4, HZ + 70); x = 560 + rng.gauss(0, 60 + (y - HZ) * 1.4); L = rng.uniform(8, 26)
        gl = np.maximum(gl, stroke_mask(W, H, [(x - L / 2, y), (x + L / 2, y + rng.uniform(-0.6, 0.6))], rng.uniform(1.2, 2.4), (0.3, 0.3)))
    art = over(art, gouache_paint(gl, "#fff7da", seed=nxt(), rough=0.6, streak=0, density=0.75))
    # small sailboat
    hull = shape_mask(W, H, [(330, HZ + 22), (372, HZ + 22), (364, HZ + 29), (338, HZ + 29)], smooth=False)
    sail = shape_mask(W, H, deform([(352, HZ + 20), (352, HZ - 22), (376, HZ + 18)], rng, 1, 0.02), smooth=False)
    sail2 = shape_mask(W, H, deform([(349, HZ + 20), (349, HZ - 12), (334, HZ + 18)], rng, 1, 0.02), smooth=False)
    art = over(art, gouache_paint(hull, "#7a4b2c", seed=nxt(), rough=0.8))
    art = over(art, gouache_obj(sail, "#fff8ec", "#f1e4c8", seed=nxt(), k=0.25, light=(1, -0.4), blur=3))
    art = over(art, gouache_obj(sail2, "#ffd27a", seed=nxt(), k=0.2, blur=3))
    # beach: sand with a wet shoreline and foam
    shore = [(x, 300 + 18 * math.sin(x / 120 + 0.8) + 8 * math.sin(x / 41)) for x in np.linspace(-20, W + 20, 30)]
    sand = shape_mask(W, H, shore + [(W + 20, H + 80), (-20, H + 80)])
    wet = shape_mask(W, H, [(x, y - 9) for x, y in shore] + [(W + 20, H + 80), (-20, H + 80)])
    art = over(art, gouache_paint(wet, "#e2c58d", seed=nxt(), rough=2, streak=0.6, density=0.8))
    art = over(art, gouache_obj(sand, "#f6dfae", "#efcf92", seed=nxt(), rough=2.5, light=(0.4, -1), k=0.15, blur=12))
    foam = stroke_mask(W, H, [(x, y - 9) for x, y in shore], 4.0, (0.05, 0.05))
    foam *= 0.35 + 0.65 * fbm(W, H, 77, 30, 3)
    art = over(art, pigment(foam, "#ffffff", seed=nxt(), density=0.95, edge=0.2, bloom=0.3, rough=3, feather=1.0, gran=0.2))
    art = over(art, speckles(W, H, rng, 260, "#b8925a", nxt(), 0.6, 1.4, region=sand))
    # big palm leaning in from the right edge, starfish + shell on the sand
    a, _ = palm(W, H, 770, H + 6, 290, -0.26, rng, nxt, trunk="#9a6a44", leaf=("#2f8a5c", "#21704b"), fronds=8)
    art = over(art, a)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5; r = 13 if i % 2 == 0 else 5.5
        star.append((96 + math.cos(ang) * r, 334 + math.sin(ang) * r))
    sm = shape_mask(W, H, deform(star, rng, 1, 0.04), smooth=False)
    art = over(art, gouache_obj(sm, "#f07b4f", "#d95f3a", seed=nxt(), k=0.25, blur=2))
    preview(art, f"{PREV}/pl-hero.png")
    save(art, f"{D}/hero.webp", q=78, trim=False)


def plane():
    W, H = 420, 240
    parts = airliner_parts(W, H, 210, 120, 330, rng, bank=-0.12)
    a, _ = paint_airliner(W, H, parts, rng, nxt, body="#f6f4ee", body2="#dfe3ea", navy=NAVY, accent=YELLOW, ink_col="#163566")
    preview(a, f"{PREV}/pl-plane.png", "#4aa3ee")
    save(a, f"{D}/plane.webp", max_w=260, q=84)


def stamp():
    W = Hh = 300
    art = postmark(W, Hh, 150, 150, 132, "PAKET SELAMANYA", "E-VOUCHER CINTA", "LUNAS", rng, nxt, col="#c8352e", wear=0.5, rot=-0.18, center_size=52, date="DOA+HADIR")
    preview(art, f"{PREV}/pl-stamp.png", "#fff7d6")
    save(art, f"{D}/stamp.webp", max_w=200, q=80)


def luggage():
    W, H = 300, 260
    a, _ = paint_suitcase(W, H, 150, 142, 210, rng, nxt, col="#2e7fe0", col2="#1f62b8", trim="#ffd75e", ink_col="#123a6b", stickers=True)
    preview(a, f"{PREV}/pl-luggage.png", "#ffffff")
    save(a, f"{D}/luggage.webp", max_w=200, q=84)


def paper_tex():
    t = grain_overlay(256, "#1d4f8f", seed=23, base=0.004, k=0.8, cap=0.035, fiber=0.4, mottle=0.8)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["hero", "plane", "stamp", "luggage", "paper"]
    for w in which:
        {"hero": hero, "plane": plane, "stamp": stamp, "luggage": luggage, "paper": paper_tex}[w]()
