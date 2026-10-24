"""Gradasi Senja — minimal sunset: a hand-painted gradient sky (peach -> coral -> violet) with brush streaks, a watercolour
sun disc with a wet rim, a small sun-on-horizon mark for dividers, and a film-grain tile. No landscape detail.
Run: python3 -I gradasi-senja.py [part ...]  parts: sky sun mark grain"""
import sys, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _q3_lib import *

OUT = outdir("gradasi-senja")
PARTS = sys.argv[1:] or ["sky", "sun", "mark", "grain"]

if "sky" in PARTS:
    W, H = 520, 900
    sky = painted_sky(W, H, [(0.0, "#fde7d4"), (0.22, "#fcd6bd"), (0.42, "#f9b79c"), (0.6, "#f19583"), (0.78, "#d97a86"), (1.0, "#a86a92")], seed=31, streak=0.45, grain=0.5)
    # a couple of long, low-contrast cloud-free brush passes so it reads as painted, not a CSS gradient
    for k, (y, col, a) in enumerate([(0.3, "#ffe9d6", 0.08), (0.52, "#f6a990", 0.07), (0.7, "#e4868a", 0.06)]):
        m = strokes(W, H, [(curve([(-40, H * y), (W * 0.4, H * (y - 0.012)), (W + 40, H * (y + 0.01))], 30), 60 + k * 12, (0.3, 0.3))])
        sky = G(sky, gaussian_filter(m, 10) * a * 4, col, seed=40 + k, density=0.5, edge=0.05, bloom=0.2, rough=6, feather=8, pad=0)
    sky[..., 3] = 1
    save_rgb(sky, f"{OUT}/sky.webp", quality=80)
    Image.fromarray((np.clip(sky[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/gs-sky.png")
    clear()

if "sun" in PARTS:
    W = H = 440; c = 220
    nx = Seq(6100)
    rng = random.Random(4)
    art = blank(W, H)
    disc = shape_mask(W, H, deform(ellipse_pts(c, c, 190, 190, 40), rng, 2, 0.015))
    art = G(art, disc, "#ffb184", "#ffa27e", seed=nx(), density=0.95, edge=0.35, bloom=0.04, gran=0.12, rough=2, feather=1.2, mottle=0.08)
    core = shape_mask(W, H, deform(ellipse_pts(c - 12, c - 16, 132, 128, 30), rng, 2, 0.03))
    core = gaussian_filter(shape_mask(W, H, ellipse_pts(c - 10, c - 14, 150, 150, 30)), 26) * disc
    k = (np.clip(core * 1.3, 0, 1) * (0.85 + 0.15 * fbm(W, H, nx(), 40, 3)))[..., None]
    art[..., :3] = art[..., :3] * (1 - k * 0.9) + np.array(hex_rgb("#ffe9b4"), np.float32) * k * 0.9
    art = G(art, gaussian_filter(np.clip(disc - gaussian_filter(disc, 30) * 1.25, 0, 1), 6) * disc, "#f0806a", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=3, feather=3)
    save(art, f"{OUT}/sun.webp", max_w=360, quality=84)
    preview(art, "gs-sun", bg="#f6a88e")
    clear()

if "mark" in PARTS:
    # small half sun resting on a dry-brush horizon stroke
    W, H = 300, 120
    nx = Seq(6200)
    rng = random.Random(9)
    art = blank(W, H)
    half = shape_mask(W, H, deform(arc_pts(150, 92, 52, math.pi, math.tau, 30), rng, 2, 0.02) + [(202, 92), (98, 92)])
    art = G(art, half, "#f5946f", "#ef7f6a", seed=nx(), density=0.88, edge=0.55, bloom=0.2, rough=2.5, feather=1.0)
    art = G(art, gaussian_filter(shape_mask(W, H, ellipse_pts(142, 80, 26, 16, 16)), 6) * half, "#ffd29a", seed=nx(), density=0.6, edge=0, bloom=0.2, rough=3, feather=3)
    line = strokes(W, H, [(curve([(10, 95), (150, 93), (290, 96)], 40), 3.2, (0.1, 0.15))])
    art = G(art, line, "#5b3a6e", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1.2, feather=0.5)
    save(art, f"{OUT}/mark.webp", max_w=180, quality=84)
    preview(art, "gs-mark", "#fde7d4")
    clear()

if "grain" in PARTS:
    S = 128
    rng = np.random.default_rng(12)
    n = gaussian_filter(rng.random((S, S)).astype(np.float32), 0.55, mode="wrap")
    n = (n - n.mean()) / (n.std() + 1e-6)
    a = np.clip(np.abs(n) * 0.045, 0, 0.13)
    rgb = np.where(n[..., None] > 0, np.array([1.0, 0.97, 0.93], np.float32), np.array([0.2, 0.1, 0.2], np.float32)) * np.ones((S, S, 3), np.float32)
    art = np.concatenate([rgb, a[..., None]], -1)
    save_texture(art, f"{OUT}/grain.webp", quality=60)
    print("grain", os.path.getsize(f"{OUT}/grain.webp") // 1024, "KB")
