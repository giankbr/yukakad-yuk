"""Cintamani — Ottoman çintamani (three spheres + paired wavy bands) as raised crimson silk velvet with couched gold
outlines on ivory silk (kemha/çatma): seamless field tile, large single motif, yastık end-panel lappet band,
narrow cloud-band border. Run: python3 -I cintamani.py [part ...]. parts: field motif lappet border.
Assets -> public/themes/art/cintamani/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s3_lib import *

OUT = outdir("cintamani")
PARTS = sys.argv[1:] or ["field", "motif", "lappet", "border"]
IVORY = "#f3e8d2"
CRIM, CRIM_D, CRIM_H = "#9e1427", "#4a0711", "#e86a72"
GOLD = "#c49a3e"


def wave_poly(cx, cy, L, amp, T, phase=math.pi, n=60, cyc=1.0):
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        x = cx - L + 2 * L * u
        y = cy + amp * math.sin(u * math.tau * cyc + phase)
        th = T * (math.sin(math.pi * u) ** 0.8) + 0.2
        # slight lip: thicker toward the leading (left) third, like a tiger-stripe brushstroke
        th *= 0.75 + 0.45 * (1 - u)
        dy = amp * math.cos(u * math.tau * cyc + phase) * math.tau * cyc / (2 * L)
        nrm = 1 / math.sqrt(1 + dy * dy)
        top.append((x + dy * th * nrm, y - th * nrm))
        bot.append((x - dy * th * nrm, y + th * nrm))
    return top + bot[::-1]


def cintamani(W, H, cx, cy, s, rng):
    """Masks: spheres, sphere inner eyes, waves. s = overall width."""
    r = s * 0.13
    balls = [(cx, cy - s * 0.34), (cx - s * 0.17, cy - s * 0.08), (cx + s * 0.17, cy - s * 0.08)]
    sph = circles(W, H, [(x + rng.gauss(0, r * .03), y + rng.gauss(0, r * .03), r) for x, y in balls])
    eye = circles(W, H, [(x - r * 0.18, y - r * 0.12, r * 0.42) for x, y in balls])
    ring = np.clip(circles(W, H, [(x, y, r + max(1.6, s * 0.012)) for x, y in balls]) - sph * 0.0, 0, 1)
    waves = shapes(W, H, [wave_poly(cx, cy + s * 0.2, s * 0.44, s * 0.065, s * 0.06),
                          wave_poly(cx, cy + s * 0.37, s * 0.44, s * 0.065, s * 0.06)])
    return sph, eye, ring, waves


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.03).astype(np.float32) - (mask > 0.5), 0, 1)


def paint_motif(art, W, H, cx, cy, s, seed, rng):
    sph, eye, ring, waves = cintamani(W, H, cx, cy, s, rng)
    shape = np.maximum(sph, waves)
    gold = np.maximum(outline(sph, max(2.4, s * 0.022)), outline(waves, max(2.4, s * 0.022)))
    sh = soft_shadow(shape, "#3a1a0a", blur=max(2, s * 0.012), strength=0.35, dx=1, dy=2)
    art = over(art, sh)
    art = CO(art, gold, seed=seed, base=GOLD)
    art = VV(art, shape, CRIM, CRIM_D, CRIM_H, seed=seed + 1, rough=0.8, nap=0.7, depth_px=max(3.0, s * 0.03))
    art = VV(art, eye, "#6e0c1a", "#3e0610", "#a8303c", seed=seed + 2, rough=0.4, nap=0.3, depth_px=max(2.0, s * 0.015))
    return art


if "field" in PARTS:
    W = H = 400
    art = silk(W, H, IVORY, seed=401, lustre=0.8)
    # faint woven diaper of small gold dots between motifs
    dots = circles(W, H, [(x, y, 2.2) for x in (0, 200, 400) for y in (0, 200, 400)] + [(x, y, 2.2) for x in (100, 300) for y in (5, 205)])
    art = OV(art, dots, lambda m: couched(m, seed=7, base="#b8903c"))
    rng = random.Random(4)
    art = paint_motif(art, W, H, 100, 112, 150, 410, rng)
    art = paint_motif(art, W, H, 300, 312, 150, 420, rng)
    preview(art, "ci-field")
    save_full(art, f"{OUT}/field.webp", quality=74)

if "motif" in PARTS:
    W, H = 460, 470
    art = blank(W, H)
    art = paint_motif(art, W, H, 230, 240, 400, 430, random.Random(9))
    preview(art, "ci-motif")
    save(art, f"{OUT}/motif.webp", max_w=300, quality=82)

if "lappet" in PARTS:
    # yastık end panel: crimson velvet ground with a row of ivory pointed arches (lappets), each holding a small
    # çintamani; couched gold outlines. Tiles horizontally (period 160 px).
    W, H, P = 480, 220, 160
    art = blank(W, H)
    ground = shapes(W, H, [[(0, 0), (W, 0), (W, H), (0, H)]], smooth=False)
    arches = []
    for k in range(-1, W // P + 2):
        x0 = k * P + 14; x1 = (k + 1) * P - 14; xm = (x0 + x1) / 2
        pts = [(x0, H - 16), (x0, 112)] + [(xm + (x0 - xm) * math.cos(t), 112 - 70 * math.sin(t) ** 0.8 - (40 * (t / (math.pi / 2)) ** 3 if t > 0 else 0)) for t in np.linspace(0, math.pi / 2, 10)][1:]
        left = pts
        right = [(2 * xm - x, y) for x, y in left[::-1]]
        arches.append(left + right)
    am = shapes(W, H, arches, smooth=False)
    base = velvet(ground, CRIM, CRIM_D, CRIM_H, seed=440, rough=0, nap=0.7, wrap=True)
    silkg = silk(W, H, IVORY, seed=441, lustre=0.7)
    am_s = gaussian_filter(am, 0.8, mode="wrap")
    art = base.copy()
    art[..., :3] = base[..., :3] * (1 - am_s[..., None]) + silkg[..., :3] * am_s[..., None]
    bands = np.zeros((H, W), np.float32)
    bands[4:9, :] = 1; bands[H - 9:H - 4, :] = 1
    gl = np.maximum(outline(am, 3.0), bands)
    gold = couched(gl, seed=443, base=GOLD)
    art = over(art, gold)
    rng = random.Random(3)
    for k in range(W // P):
        xm = k * P + P / 2
        art = paint_motif(art, W, H, xm, 150, 74, 450 + k * 5, rng)
    # pearl dots along the crimson spandrels
    pearls = circles(W, H, [(k * P, 60, 4.5) for k in range(0, W // P + 1)] + [(k * P, 96, 3.2) for k in range(0, W // P + 1)])
    art = OV(art, pearls, lambda m: couched(m, seed=9, base="#d8b45e"))
    art[..., 3] = 1
    preview(art, "ci-lappet")
    save_full(art, f"{OUT}/lappet.webp", quality=76)

if "border" in PARTS:
    # narrow border: crimson velvet strip with a couched gold double wave (cloud band) and dots. Tiles at 120 px.
    W, H, P = 480, 44, 120
    ground = np.ones((H, W), np.float32)
    art = velvet(ground, CRIM, CRIM_D, CRIM_H, seed=460, rough=0, nap=0.6, wrap=True)
    pts1 = [(x, 22 + 9 * math.sin(x / P * math.tau)) for x in range(-4, W + 5, 3)]
    pts2 = [(x, 22 - 9 * math.sin(x / P * math.tau)) for x in range(-4, W + 5, 3)]
    m = strokes(W, H, [(pts1, 3.0, None), (pts2, 3.0, None)])
    m = np.maximum(m, circles(W, H, [(P * k + P / 4, 22, 3.2) for k in range(4)] + [(P * k + 3 * P / 4, 22, 3.2) for k in range(4)]))
    m[1:3, :] = 1; m[H - 3:H - 1, :] = 1
    art = over(art, couched(m, seed=461, base=GOLD))
    art[..., 3] = 1
    preview(art, "ci-border")
    save_full(art, f"{OUT}/border.webp", quality=78)
