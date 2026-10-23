"""Malakit Hijau — polished malachite slabs (concentric botryoidal banding, book-matched) with pressed-gold inlay,
cream onyx plaques and a malachite cabochon in a beaded gold bezel.
Run: python3 -I malakit-hijau.py [part ...]   parts: slab band gold onyx gem divider
Assets -> public/themes/art/malakit-hijau/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k4_lib import *

OUT = outdir("malakit-hijau")
PARTS = sys.argv[1:] or ["slab", "band", "gold", "onyx", "gem", "divider"]
STOPS = [(0, "#020f09"), (0.2, "#062a19"), (0.42, "#0d5532"), (0.62, "#17804c"), (0.8, "#3aa86c"), (0.93, "#86d2a6"), (1, "#c4ecd3")]
GOLD = "#c9a04e"


def centres(rng, W, H, n, wmin=0.6, wmax=1.5, pad=120):
    return [(rng.uniform(-pad, W + pad), rng.uniform(-pad, H + pad), rng.uniform(wmin, wmax)) for _ in range(n)]


if "slab" in PARTS:
    # book-matched: one half rendered, mirrored about the vertical seam
    W, H = 390, 1640
    rng = random.Random(21)
    cs = [(rng.uniform(-160, W - 150), rng.uniform(-100, H + 100), rng.uniform(0.9, 1.8)) for _ in range(7)]
    half = malachite(W, H, 31, cs, period=4.4, warp=46, stops=STOPS, light_dir=0.6)
    full = np.concatenate([half, half[:, ::-1]], 1)
    full = vignette(full, 0.35, 2.0)
    show(full[:900], "mh-slab")
    save_rgb(full, f"{OUT}/slab.webp", size=(640, 1346), quality=66)
    clear()

if "band" in PARTS:
    W, H = 780, 560
    rng = random.Random(5)
    cs = centres(rng, W, H, 9, 0.7, 1.6, 200)
    m = malachite(W, H, 47, cs, period=4.2, warp=40, stops=STOPS, light_dir=0.8)
    show(m, "mh-band")
    save_rgb(m, f"{OUT}/band.webp", quality=72)
    clear()

if "gold" in PARTS:
    # seamless brushed gold leaf tile
    W = H = 256
    n1 = wrap_noise(W, H, 3, (0.6, 14))
    n2 = wrap_noise(W, H, 4, 18)
    n3 = wrap_noise(W, H, 5, 0.7)
    t = np.clip(0.5 + (n1 - 0.5) * 1.1 + (n2 - 0.5) * 0.35 + (n3 - 0.5) * 0.25, 0, 1)
    rgb = ramp(t, [(0, "#7a5520"), (0.35, "#b48a3e"), (0.6, "#d8b466"), (0.8, "#f0d896"), (1, "#fff1c4")])
    spark = (wrap_noise(W, H, 9, 0.5) > 0.93).astype(np.float32) * 0.25
    rgb = rgb + spark[..., None]
    g = rgba(rgb, np.ones((H, W), np.float32))
    show(np.tile(g, (2, 2, 1)), "mh-gold")
    save_rgb(g, f"{OUT}/gold.webp", quality=80)

if "onyx" in PARTS:
    # seamless cream onyx: soft cloudy translucency + a few honey veins
    W = H = 512
    c1 = wrap_noise(W, H, 11, 40); c2 = wrap_noise(W, H, 12, 12); c3 = wrap_noise(W, H, 13, 3)
    base = ramp(np.clip(0.55 + (c1 - 0.5) * 0.9 + (c2 - 0.5) * 0.4, 0, 1), [(0, "#e4dac6"), (0.5, "#f1eadb"), (1, "#fbf7ef")])
    warpn = wrap_noise(W, H, 14, 46)
    v = np.abs(np.sin((warpn * 16 + c2 * 0.6) * math.pi))
    vv = gaussian_filter(np.clip((0.12 - v) / 0.12, 0, 1) * 0.55, 1.2, mode="wrap")
    rgb = base * (1 - vv[..., None] * 0.35) + np.array(hex_rgb("#c3a77a"), np.float32) * vv[..., None] * 0.22
    rgb = rgb * (1 + (c3[..., None] - 0.5) * 0.03)
    o = rgba(rgb, np.ones((H, W), np.float32))
    show(o, "mh-onyx")
    save_rgb(o, f"{OUT}/onyx.webp", quality=74)

if "gem" in PARTS:
    W, H = 220, 270
    cx, cy, rx, ry = 110, 135, 74, 96
    rng = random.Random(8)
    stone = malachite(W, H, 61, [(cx + 10, cy - 20, 0.7), (cx - 30, cy + 40, 0.5), (cx + 40, cy + 60, 0.6)], period=3.4, warp=14, stops=STOPS)
    om = ellipses(W, H, [(cx, cy, rx, ry, 0)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2, 0, 1)
    dome = np.sqrt(1 - d)
    rgb = stone[..., :3] * (0.55 + 0.55 * dome[..., None])
    hl = gaussian_filter(ellipses(W, H, [(cx - 22, cy - 40, 20, 34, -20)]), 7)
    rgb = rgb + hl[..., None] * 0.5
    gem = rgba(rgb, om)
    bez_o = ellipses(W, H, [(cx, cy, rx + 9, ry + 9, 0)])
    bez = np.clip(bez_o - gaussian_filter(om, 0.8), 0, 1)
    beads = circles(W, H, [(cx + math.cos(a) * (rx + 14), cy + math.sin(a) * (ry + 14), 4.6) for a in np.linspace(0, math.tau, 45)[:-1]])
    art = blank(W, H)
    art = over(art, drop_shadow(np.maximum(bez_o, beads), "#000000", 5, 3, 5, 0.45))
    art = FO(art, np.maximum(bez, beads), GOLD, seed=3, emboss=1.0, sparkle=0.3)
    art = over(art, gem)
    show(art, "mh-gem", bg="#f1eadb")
    save(art, f"{OUT}/gem.webp", max_w=110, quality=86)

if "divider" in PARTS:
    W, H = 720, 80
    cx, cy = W / 2, H / 2
    line = strokes(W, H, [([(30, cy), (cx - 70, cy)], 3.2, (0.4, 0.0)), ([(cx + 70, cy), (W - 30, cy)], 3.2, (0.0, 0.4)),
                          ([(110, cy - 9), (cx - 60, cy - 9)], 1.4, (0.5, 0.05)), ([(cx + 60, cy - 9), (W - 110, cy - 9)], 1.4, (0.05, 0.5)),
                          ([(110, cy + 9), (cx - 60, cy + 9)], 1.4, (0.5, 0.05)), ([(cx + 60, cy + 9), (W - 110, cy + 9)], 1.4, (0.05, 0.5))])
    loz_o = shapes(W, H, [[(cx - 58, cy), (cx, cy - 30), (cx + 58, cy), (cx, cy + 30)]], smooth=False)
    loz_i = shapes(W, H, [[(cx - 46, cy), (cx, cy - 22), (cx + 46, cy), (cx, cy + 22)]], smooth=False)
    dots = circles(W, H, [(cx - 82, cy, 5), (cx + 82, cy, 5), (cx - 98, cy, 3), (cx + 98, cy, 3)])
    stone = malachite(W, H, 71, [(cx, cy, 0.5), (cx + 30, cy + 20, 0.4)], period=2.6, warp=8, stops=STOPS)
    art = blank(W, H)
    art = over(art, drop_shadow(np.maximum.reduce([line, loz_o, dots]), "#000000", 2, 1, 2, 0.35))
    art = FO(art, np.maximum.reduce([line, np.clip(loz_o - loz_i, 0, 1), dots]), GOLD, seed=5, emboss=0.9)
    art = over(art, rgba(stone[..., :3], loz_i))
    show(art, "mh-divider", bg="#f1eadb")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=86)
