"""Lentera Terbang — a painted night over a still highland lake: indigo sky warming to an ember horizon, layered
hills, and hundreds of paper sky lanterns rising from the far shore, mirrored as soft streaks on the water.
Separate seamless lantern tile for the gentle rising animation, one close-up lantern and a small divider.
Run: python3 -I lentera-terbang.py [part ...]   parts: langit tile lentera garis"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t6_lib import *

OUT = outdir("lentera-terbang")
PARTS = sys.argv[1:] or ["langit", "tile", "lentera", "garis"]


def lantern_sprite(h, seed, warm=0.0, detail=True):
    """One sky lantern, h px tall (+ glow margin). Paper glows from a flame at the open bottom."""
    rng = random.Random(seed)
    w = h * rng.uniform(0.62, 0.72)
    pad = int(h * 0.75) + 4
    W, H = int(w + pad * 2), int(h + pad * 2)
    cx, top, bot = W / 2, pad, pad + h
    left = []
    for i in range(15):
        t = i / 14
        # widest just above the middle, gently tapering to the open bottom
        half = w * 0.5 * (0.86 + 0.14 * math.sin(min(1, t * 1.6) * math.pi * 0.9)) * (1 - 0.18 * t ** 1.5)
        left.append((cx - half, top + h * 0.06 + (h * 0.94) * t))
    dome = [(cx + math.cos(a) * w * 0.46, top + h * 0.07 - math.sin(a) * h * 0.09) for a in [math.pi - j * math.pi / 10 for j in range(11)]]
    right = [(2 * cx - x, y) for x, y in left]
    outline = left[::-1] + dome[1:-1] + right
    m = shape_mask(W, H, outline)
    yy, xx = yx(W, H)
    t = np.clip((yy - top) / h, 0, 1)
    core = np.clip(1 - np.abs(xx - cx) / (w * 0.55), 0, 1) ** 0.8
    inner = np.clip(0.35 + 0.65 * t, 0, 1) * (0.55 + 0.45 * core)
    c_hot = np.array(hex_rgb(mix("#fff1b8", "#ffd27a", warm)), np.float32)
    c_mid = np.array(hex_rgb(mix("#ffb347", "#ff9a3c", warm)), np.float32)
    c_rim = np.array(hex_rgb(mix("#d9622b", "#b8451f", warm)), np.float32)
    k = inner[..., None]
    rgb = c_rim * (1 - k) + c_mid * k
    rgb = rgb * (1 - np.clip(k - 0.75, 0, 1)[..., :1] * 3) + c_hot * np.clip(k - 0.75, 0, 1) * 3
    if detail and h > 30:
        # paper seams + wire rim at the bottom
        seams = strokes(W, H, [([(cx + d * w * 0.5, top + h * 0.02), (cx + d * w * 0.4, bot - 1)], max(0.6, h * 0.012), None) for d in (-0.45, 0.0, 0.45)])
        rgb = rgb * (1 - seams[..., None] * 0.18)
        rim = strokes(W, H, [([(cx - w * 0.42, bot), (cx + w * 0.42, bot)], max(0.8, h * 0.03), None)])
        rgb = rgb * (1 - rim[..., None] * 0.5)
        fl = soft(ell(W, H, cx, bot - h * 0.05, w * 0.045, h * 0.055), max(0.5, h * 0.01))
        rgb = rgb * (1 - fl[..., None]) + np.array(hex_rgb("#fffbe8"), np.float32) * fl[..., None]
        g = fbm(W, H, seed, max(4, h * 0.25), 2)
        rgb = rgb * (0.93 + 0.1 * g[..., None])
    m = gaussian_filter(m, max(0.4, h * 0.012))
    spr = np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)
    halo = gaussian_filter(m, h * 0.3) * 1.2 + gaussian_filter(m, h * 0.1) * 0.6
    glowl = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#ff9f45"), np.float32), np.clip(halo, 0, 1)[..., None] * 0.55], -1)
    return over(glowl, spr)


def paste(dst, spr, x, y, alpha=1.0):
    """Paste sprite centred at x,y (over)."""
    H, W = dst.shape[:2]
    h, w = spr.shape[:2]
    x0, y0 = int(round(x - w / 2)), int(round(y - h / 2))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x0 + w), min(H, y0 + h)
    if dx1 <= dx0 or dy1 <= dy0:
        return dst
    s = spr[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0)].copy()
    s[..., 3] *= alpha
    dst[dy0:dy1, dx0:dx1] = over(dst[dy0:dy1, dx0:dx1], s)
    return dst


SPR = {}


def spr(h, seed, warm):
    key = (int(h), seed % 6, round(warm, 1))
    if key not in SPR:
        SPR[key] = lantern_sprite(int(h), seed % 6 + 3, warm, detail=h > 14)
    return SPR[key]


if "langit" in PARTS:
    W, H = 860, 1720
    HZ = int(H * 0.70)
    rng = random.Random(4)
    sky = painted_sky(W, H, [(0, "#090b26"), (0.3, "#171a45"), (0.5, "#3a2a5a"), (0.62, "#7c3f5a"), (0.7, "#c9774f"), (1.0, "#c9774f")], seed=3, streak=0.8)
    # warm horizon haze
    sky = add_light(sky, radial(W, H, W * 0.55, HZ, W * 0.9, H * 0.16), "#ffb067", 0.45)
    # a few stars in the upper sky
    st = np.random.default_rng(9).random((H, W)) > 0.9985
    st = gaussian_filter(st.astype(np.float32), 0.7) * 5 * np.clip(1 - (yx(W, H)[0] / (H * 0.45)), 0, 1)
    sky = add_light(sky, st, "#fff4dc", 0.8)
    # hills: far (misty) and near
    far = ridge_mask(W, H, HZ - 46, 40, 11, freq=2.2, sharp=0.8, bottom=HZ + 4)
    sky = OV(sky, far, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#4f3358"), np.float32), m[..., None]], -1), pad=0)
    sky = add_light(sky, gaussian_filter(far, 10) * np.clip((yx(W, H)[0] - (HZ - 40)) / 40, 0, 1), "#ffa766", 0.25)
    near = ridge_mask(W, H, HZ - 10, 90, 23, freq=1.6, sharp=0.7, bottom=HZ + 6)
    near *= np.clip((np.abs(yx(W, H)[1] - W * 0.55) - W * 0.12) / 80, 0, 1)
    sky = GP(sky, near, "#2a1d3d", "#211833", seed=31, rough=2.5, streak=0.6, pad=4)
    # lanterns: many tiny far ones low, fewer larger higher (closer, drifting up)
    lay = np.zeros((H, W, 4), np.float32)
    items = []
    for k in range(340):
        d = rng.random() ** 1.7  # 0 = far
        y = HZ - 20 - rng.random() ** (1.3 + d) * (HZ - 120) * (0.35 + 0.65 * rng.random())
        hgt = 5 + d * 30 + (HZ - y) / HZ * 6 * rng.random()
        x = rng.gauss(W * 0.55, W * (0.18 + 0.25 * (HZ - y) / HZ))
        items.append((hgt, x, y, k))
    items.sort()
    for hgt, x, y, k in items:
        if hgt > 26 and y < H * 0.36:
            continue
        lay = paste(lay, spr(hgt, k, rng.uniform(0, 1)), x, y, alpha=0.75 + 0.25 * min(1, hgt / 20))
    sky = over(sky, lay)
    # lake: mirror sky above horizon, darker, rippled
    yy, xx = yx(W, H)
    d = np.maximum(0, yy - HZ)
    src_y = np.clip(HZ - d * 0.85, 0, H - 1)
    rip = (fbm(W, H, 5, 10, 2) - 0.5) * 10 * np.clip(d / 60, 0, 1) + np.sin(yy * 0.9) * 1.6 * np.clip(d / 40, 0, 1)
    refl = np.stack([map_coordinates(sky[..., c], [src_y, np.clip(xx + rip, 0, W - 1)], order=1) for c in range(3)], -1)
    # stretch highlights vertically (streaky reflections)
    refl = np.maximum(refl * 0.5, gaussian_filter(refl, (9, 1.2), axes=(0, 1)) * 0.56)
    water = refl * np.array([0.78, 0.8, 0.98], np.float32)
    sel = (yy > HZ)[..., None]
    sky[..., :3] = np.where(sel, water, sky[..., :3])
    # horizontal water strokes + shoreline
    s = gaussian_filter(np.random.default_rng(2).random((H, W)).astype(np.float32), (0.8, 30))
    s = (s - s.mean()) / (s.std() + 1e-6)
    sky[..., :3] *= 1 + (s * 0.05 * (yy > HZ))[..., None]
    shore = band(W, H, HZ - 1, HZ + 3, 2) if False else np.clip(1 - np.abs(yy - HZ - 1) / 2.5, 0, 1)
    sky = add_light(sky, shore * 0.6, "#ffb77a", 0.5)
    # dark foreground bank with reeds, bottom corners
    bank = ridge_mask(W, H, H - 60, 30, 41, freq=1.4, sharp=0.9)
    sky = GP(sky, bank, "#120d22", "#1a1430", seed=41, rough=2, streak=0.4, pad=4)
    reeds = []
    for k in range(60):
        side = -1 if k % 2 else 1
        x = (W * 0.06 if side < 0 else W * 0.94) + rng.gauss(0, W * 0.07)
        hh = rng.uniform(60, 190)
        lean = rng.uniform(-0.25, 0.25)
        reeds.append(([(x, H + 4), (x + lean * hh * 0.5, H - hh * 0.5), (x + lean * hh, H - hh)], rng.uniform(2.5, 4.5), (0.0, 0.8)))
    sky = GP(sky, strokes(W, H, reeds), "#120d22", "#1d1630", seed=43, rough=1.2, streak=0.3, pad=4)
    sky = vignette(sky, 0.25)
    prev(sky, "lentera-langit", bg="#000000")
    save_rgb(sky, f"{OUT}/langit.webp", size=(860, 1720), quality=74)
    clear()

if "tile" in PARTS:
    # seamless vertical tile of mid-size lanterns for the rising layer
    W, H = 430, 1100
    rng = random.Random(77)
    lay = np.zeros((H, W, 4), np.float32)
    pts = []
    for k in range(26):
        for _ in range(30):
            x, y = rng.uniform(16, W - 16), rng.uniform(0, H)
            if all((x - a) ** 2 + ((y - b + H / 2) % H - H / 2) ** 2 > 70 ** 2 for a, b, _h in pts):
                break
        pts.append((x, y, rng.uniform(12, 30)))
    for x, y, hh in sorted(pts, key=lambda p: p[2]):
        sp = lantern_sprite(int(hh), int(x * 7 + y) % 9 + 1, rng.uniform(0, 1))
        for dy in (-H, 0, H):
            lay = paste(lay, sp, x, y + dy, alpha=0.95)
    lay = lay[:, :, :]
    prev(lay, "lentera-tile", bg="#1b1a45")
    save_full(lay, f"{OUT}/tile.webp", quality=78)
    clear()

if "lentera" in PARTS:
    sp = lantern_sprite(240, 5, 0.3)
    prev(sp, "lentera-big", bg="#1b1a45")
    save_full(sp, f"{OUT}/lentera.webp", size=(sp.shape[1] // 2, sp.shape[0] // 2), quality=80)
    clear()

if "garis" in PARTS:
    W, H = 640, 120
    lay = np.zeros((H, W, 4), np.float32)
    rng = random.Random(3)
    line_m = np.zeros((H, W), np.float32)
    yy, xx = yx(W, H)
    line_m = np.clip(1 - np.abs(yy - (H * 0.62 + np.sin(xx / W * math.pi) * -10)) / 1.2, 0, 1) * np.clip(1 - np.abs(xx - W / 2) / (W * 0.48), 0, 1) ** 0.6
    lay = over(lay, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f3b25a"), np.float32), line_m[..., None] * 0.7], -1))
    for x, y, h in [(W / 2, H * 0.36, 40), (W / 2 - 64, H * 0.5, 22), (W / 2 + 70, H * 0.48, 26), (W / 2 - 128, H * 0.6, 13), (W / 2 + 132, H * 0.58, 12)]:
        lay = paste(lay, lantern_sprite(int(h), int(x) % 7 + 2, 0.4), x, y)
    prev(lay, "lentera-garis", bg="#1b1a45")
    save_full(lay, f"{OUT}/garis.webp", size=(320, 60), quality=82)
