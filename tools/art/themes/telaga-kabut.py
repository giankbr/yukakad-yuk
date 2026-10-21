"""Telaga Kabut — misty mountain lake in wet-on-wet watercolour: layered ridges dissolving into mist, pine stands, still lake
with soft reflections, a small wooden pier and boat. Cool sage / blue-grey palette.
Run: python3 -I telaga-kabut.py [part ...]   parts: telaga pinus kabut perahu"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *

OUT = outdir("telaga-kabut")
PARTS = sys.argv[1:] or ["telaga", "pinus", "kabut", "perahu"]
PAPER = "#eef0ec"
SLATE, SLATE_D = "#5d6f7a", "#33424b"
SAGE, SAGE_D = "#8fa094", "#5c6f62"
MIST = "#c9d2d2"


def mist_fade(H, W, y0, y1):
    """1 above y0 -> 0 below y1 (used to dissolve a ridge's foot into mist)."""
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    return np.clip((y1 - yy) / max(1, y1 - y0), 0, 1)


def reflect(layer, axis_y, squash=0.7, strength=0.45, seed=1):
    """Mirror everything above axis_y into the lake below it, squashed, rippled horizontally and faded."""
    h, w = layer.shape[:2]
    out = blank(w, h)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (yy - axis_y)
    src_y = axis_y - d / squash
    rip = (fbm(w, h, seed, 10, 2) - 0.5) * 10 * np.clip(d / 60, 0, 1) + np.sin(yy * 0.9) * 1.2
    from scipy.ndimage import map_coordinates
    for c in range(4):
        out[..., c] = map_coordinates(layer[..., c], [src_y, xx + rip], order=1, mode="constant")
    fade = np.clip(1 - d / (h - axis_y + 1), 0, 1) ** 0.7 * (d > 0)
    out[..., 3] *= fade * strength
    out[..., :3] = out[..., :3] * 0.85 + np.array(hex_rgb("#9fb0b4"), np.float32) * 0.15
    return out


if "telaga" in PARTS:
    PADX = 40
    W, H = 900 + 2 * PADX, 760
    LAKE = 470
    rng = random.Random(81); nx = Seq(81000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    land = blank(W, H)
    # sky: a whisper of warm-grey wash at the top, fading out
    sky = np.clip(1 - yy / 300, 0, 1) * (yy < LAKE)
    land = G(land, sky, "#d8d9d2", "#c7cfd2", seed=nx(), density=0.35, edge=0.05, bloom=0.6, rough=10, feather=8)
    # ridges back -> front: each dissolves into the mist at its foot (wet-on-wet: high feather, blooms)
    ridges = [(250, 110, 2.0, 0.7, "#b6c0c6", "#a9b5bd", 0.55, 330),
              (300, 90, 2.8, 0.8, "#9aa9b2", "#8d9ca4", 0.62, 380),
              (360, 70, 3.6, 0.85, "#7f8f98", "#71838a", 0.7, 430),
              (420, 46, 2.4, 1.0, "#6b7c78", "#5d6f66", 0.78, LAKE + 2)]
    for k, (base, amp, fr, sh, ca, cb, dens, foot) in enumerate(ridges):
        m = ridge_mask(W, H, base, amp, 10 + k, freq=fr, sharp=sh, bottom=foot) * (yy <= foot + 1)
        fade = mist_fade(H, W, base - amp * 0.2, foot) if k < 3 else 1.0
        land = G(land, m * fade, ca, cb, seed=nx(), density=dens, edge=0.35, bloom=0.55, rough=9, feather=2.4 + (3 - k))
        if k < 3:  # soft second wash along the crest only
            crest = m * np.clip((base + amp * 0.3 - yy) / (amp * 1.2), 0, 1)
            land = G(land, crest, cb, seed=nx(), density=0.3, edge=0.25, bloom=0.5, rough=7, feather=3)
    # pine stands: far (pale, on ridge 3) and near (left shore, dark)
    far_items = []
    for _ in range(46):
        x = rng.uniform(380, 900); by = 410 + rng.uniform(-10, 20); h = rng.uniform(26, 50)
        far_items += pine_polys(x, by, h, rng)
    fm = shapes(W, H, far_items, smooth=False) * (yy < 440)
    land = G(land, fm, "#5f7069", "#6e7e78", seed=nx(), density=0.6, edge=0.4, bloom=0.2, rough=2.5, feather=1.2)
    near_items = []
    for x, h in [(20, 260), (62, 210), (100, 300), (138, 190), (176, 240), (214, 150), (250, 120), (288, 90)]:
        near_items += pine_polys(x + rng.uniform(-6, 6), LAKE + 8, h * rng.uniform(.9, 1.1), rng, lean=rng.uniform(-.02, .02))
    nm = shapes(W, H, near_items, smooth=False)
    shore = shapes(W, H, [[(-20, LAKE - 6), (120, LAKE - 14), (260, LAKE - 8), (340, LAKE + 2), (-20, LAKE + 14)]])
    land = G(land, np.maximum(shore, 0), "#4b5a52", seed=nx(), density=0.8, edge=0.4, bloom=0.2, rough=3)
    land = G(land, nm, "#3e4f4a", "#2f3d3b", seed=nx(), density=0.82, edge=0.5, bloom=0.25, rough=2.5, feather=1.0)
    land = G(land, nm * mist_fade(H, W, LAKE - 200, LAKE + 10)[::-1] * 0 + nm * np.clip((yy - (LAKE - 120)) / 120, 0, 1), MIST, seed=nx(), density=0.25, edge=0, bloom=0.4, rough=4)
    # right shore with the pier
    rshore = shapes(W, H, [[(640, LAKE + 4), (760, LAKE - 8), (W + 20, LAKE - 12), (W + 20, LAKE + 16)]])
    land = G(land, rshore, "#55655c", seed=nx(), density=0.75, edge=0.4, bloom=0.2, rough=3)
    r_items = []
    for x, h in [(850, 220), (890, 170), (930, 250), (800, 120)]:
        r_items += pine_polys(x, LAKE - 4, h, rng)
    land = G(land, shapes(W, H, r_items, smooth=False), "#44544e", "#34423f", seed=nx(), density=0.8, edge=0.45, bloom=0.25, rough=2.5, feather=1.0)
    # mist bands between ridges: knock pigment back with soft horizontal clouds
    for (y, hh, amt) in [(330, 36, 0.75), (392, 30, 0.6), (452, 20, 0.5)]:
        band = np.clip(1 - np.abs(yy - y) / hh, 0, 1) ** 1.5 * (0.55 + 0.45 * fbm(W, H, int(y), 90, 3))
        land[..., 3] *= 1 - band * amt
    # lake: reflections of the land + pale water washes + horizontal light streaks
    refl = reflect(land, LAKE, squash=0.85, strength=0.55, seed=nx())
    water = (yy > LAKE).astype(np.float32)
    art = G(blank(W, H), water * np.clip(1 - (yy - LAKE) / 290, 0, 1), "#b8c6c8", "#aab9be", seed=nx(), density=0.55, edge=0.1, bloom=0.5, rough=8, feather=6)
    art = glaze(art, refl)
    streaks = []
    for _ in range(40):
        y = rng.uniform(LAKE + 10, H - 40); x0 = rng.uniform(0, W); L = rng.uniform(60, 260)
        streaks.append(([(x0, y), (x0 + L, y + rng.uniform(-1, 1))], rng.uniform(1.2, 3.0), (0.3, 0.3)))
    sm = strokes(W, H, streaks) * water
    art[..., 3] *= 1 - sm * 0.6
    art = over(art, land)
    # pier: planks on posts reaching from the right shore, posts mirrored in the water
    pier = shapes(W, H, [[(540, LAKE + 46), (790, LAKE + 4), (800, LAKE + 12), (556, LAKE + 62)]], smooth=False)
    posts_ = [([(x, LAKE + 10 + (790 - x) * 0.17), (x, LAKE + 40 + (790 - x) * 0.17)], 4.5, None) for x in (566, 630, 700, 770)]
    pm = strokes(W, H, posts_)
    art = G(art, pm, "#3e3a32", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=1.2, feather=0.6)
    art = G(art, pier, "#6d5f4e", "#57493b", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1.5, feather=0.6)
    plank = strokes(W, H, [([(544 + k * 20, LAKE + 46 - k * 3.4), (560 + k * 20, LAKE + 62 - k * 3.6)], 1.0, None) for k in range(13)])
    art = G(art, plank * pier, "#3a3026", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.4)
    pref = [([(x, LAKE + 42 + (790 - x) * 0.17), (x + 1, LAKE + 86 + (790 - x) * 0.17)], 3.5, (0.0, 0.8)) for x in (566, 630, 700, 770)]
    art = G(art, strokes(W, H, pref), "#4a4a44", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=2, feather=1.2)
    # small wooden boat tied near the pier end
    hull = shapes(W, H, [[(462, LAKE + 62), (490, LAKE + 67), (540, LAKE + 67), (566, LAKE + 61), (550, LAKE + 76), (482, LAKE + 77)]], smooth=False)
    art = G(art, hull, "#4a3f34", "#3a3028", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)
    art = G(art, strokes(W, H, [([(474, LAKE + 66), (556, LAKE + 66)], 2.0, None)]), "#a08a6a", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = G(art, strokes(W, H, [(curve([(556, LAKE + 68), (566, LAKE + 56), (574, LAKE + 40)], 10), 1.0, None)]), "#3a3a36", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.3)
    bref = shapes(W, H, [[(484, LAKE + 80), (548, LAKE + 80), (556, LAKE + 92), (478, LAKE + 92)]])
    art = G(art, bref, "#5a5a52", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3, feather=2)
    # ripple lines around the boat
    rip = strokes(W, H, [(arc_pts(515, LAKE + 84, rr, math.pi * 0.1, math.pi * 0.9, 20, 0.12), 1.0, (0.2, 0.2)) for rr in (70, 96, 124)])
    art = G(art, rip, "#6d7d82", seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=0.5)
    # bottom fade (painting dissolves into the page)
    art[..., 3] *= np.clip((H - 10 - yy) / 160, 0, 1)
    art = art[:, PADX:PADX + 900]
    preview(art, "tk-telaga", tone=PAPER)
    save_full(art, f"{OUT}/telaga.webp", size=(680, 574), quality=76)
    clear()

if "pinus" in PARTS:
    W, H = 520, 560
    rng = random.Random(82); nx = Seq(82000)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = blank(W, H)
    back = []
    for _ in range(9):
        back += pine_polys(rng.uniform(40, 480), 540, rng.uniform(220, 380), rng)
    art = G(art, shapes(W, H, back, smooth=False), "#9aa9a6", "#8b9b98", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=3, feather=1.6)
    front = []
    for x, h in [(110, 500), (200, 420), (330, 470), (420, 360)]:
        front += pine_polys(x, 548, h, rng)
    art = G(art, shapes(W, H, front, smooth=False), "#566a63", "#3f514c", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=2.5, feather=1.0)
    art[..., 3] *= np.clip((H - yy) / 120, 0, 1) * 0.6 + 0.4 * np.clip((H - 20 - yy) / 40, 0, 1)
    preview(art, "tk-pinus", tone=PAPER)
    save(art, f"{OUT}/pinus.webp", max_w=260, quality=80)
    clear()

if "kabut" in PARTS:
    # soft drifting mist band (white, very low alpha edges), tileable horizontally
    W, H = 800, 200
    rng = random.Random(83)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = wrap_noise(W, H, 5, 22) * 0.6 + wrap_noise(W, H, 6, 8) * 0.4
    prof = np.clip(1 - np.abs(yy - H / 2) / (H / 2), 0, 1) ** 1.4
    a = np.clip((n - 0.3) * 1.8, 0, 1) * prof * 0.85
    art = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f6f8f6"), np.float32), a[..., None]], -1)
    preview(art, "tk-kabut", bg="#5d6f7a")
    save_full(art, f"{OUT}/kabut.webp", size=(400, 100), quality=70)
    clear()

if "perahu" in PARTS:
    # divider: tiny boat with a rower-less oar, reflection and ripple lines on a wet brush horizon
    W, H = 600, 120
    rng = random.Random(84); nx = Seq(84000)
    art = blank(W, H)
    hor = strokes(W, H, [([(30, 66), (250, 65), (350, 66), (570, 65)], 3.0, (0.35, 0.35))])
    art = G(art, hor, "#8fa0a6", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=2, feather=1.0)
    hull = shapes(W, H, [[(254, 54), (276, 59), (328, 59), (348, 53), (334, 68), (270, 68)]], smooth=False)
    art = G(art, hull, "#4a463e", "#3a362f", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1, feather=0.5)
    art = G(art, strokes(W, H, [([(300, 58), (316, 32)], 1.6, None)]), "#3a3a36", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.3)
    sail = shapes(W, H, [[(316, 30), (318, 56), (292, 56)]], smooth=False)
    art = G(art, sail, "#c9b79a", "#b7a688", seed=nx(), density=0.7, edge=0.6, bloom=0.2, rough=1.2, feather=0.6)
    ref = shapes(W, H, [[(272, 70), (330, 70), (322, 80), (280, 80)]])
    art = G(art, ref, "#6d7a7c", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2, feather=1.6)
    rip = strokes(W, H, [([(220, 84), (380, 84)], 1.2, (0.3, 0.3)), ([(180, 94), (420, 94)], 1.0, (0.3, 0.3)), ([(250, 102), (350, 102)], 0.9, (0.3, 0.3))])
    art = G(art, rip, "#9aaab0", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=0.4)
    preview(art, "tk-perahu", tone=PAPER)
    save(art, f"{OUT}/perahu.webp", max_w=300, quality=84)
    clear()
