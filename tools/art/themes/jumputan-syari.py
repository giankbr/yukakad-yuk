"""Jumputan Syari — Palembang-style jumputan (tie-dye) cloths in pastel pink, lilac and teal: pale resist rings and
starbursts where the cloth was tied, soft dye bleed and pooled edges, woven texture. Cloths hang drying on a bamboo
pole (cover). No figures. Run: python3 -I jumputan-syari.py [part ...]  parts: kain tile tile2 medal divider galah
Assets -> public/themes/art/jumputan-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o4_lib import *

OUT = outdir("jumputan-syari")
PARTS = sys.argv[1:] or ["kain", "tile", "tile2", "medal", "divider", "galah"]
PINK, PINK_D = "#e9a7b6", "#d27f95"
LILAC, LILAC_D = "#b9a6d8", "#9581c0"
TEAL, TEAL_D = "#86c6c0", "#5aa7a2"
CREAM = "#fdf6ee"


def weave(H, W, seed, wrap=False):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wv = 0.5 + 0.25 * np.sin(yy * math.pi / 1.5) + 0.25 * np.sin(xx * math.pi / 1.5)
    n = wrap_noise(W, H, seed, 1.0) if wrap else gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.8)
    n = (n - n.min()) / (np.ptp(n) + 1e-6)
    return 0.94 + 0.04 * wv + 0.04 * n


def resist(H, W, ties, seed, wrap=False):
    """Resist field 0..1 from tie points. tie = (x, y, r, kind): kind 'burst' (gathered point: pale centre with crease
    rays), 'ring' (bound ring: pale band with a dyed core), 'dot' (small pale dot with a dark heart)."""
    rng = np.random.default_rng(seed)
    A = np.zeros((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for (x, y, r, kind) in ties:
        offs = [(0, 0)]
        if wrap:
            offs = [(dx, dy) for dx in (-W, 0, W) for dy in (-H, 0, H)]
        for dx, dy in offs:
            cx, cy = x + dx, y + dy
            if cx + r * 2.2 < 0 or cx - r * 2.2 > W or cy + r * 2.2 < 0 or cy - r * 2.2 > H:
                continue
            x0, x1 = int(max(0, cx - r * 2.3)), int(min(W, cx + r * 2.3))
            y0, y1 = int(max(0, cy - r * 2.3)), int(min(H, cy + r * 2.3))
            X = xx[y0:y1, x0:x1] - cx; Y = yy[y0:y1, x0:x1] - cy
            R = np.sqrt(X * X + Y * Y) + 1e-3
            T = np.arctan2(Y, X)
            nfold = int(rng.integers(7, 12))
            ph = rng.uniform(0, 6.28)
            folds = 0.5 + 0.5 * np.cos(nfold * T + ph + 0.6 * np.sin(3 * T + ph))
            wob = 1 + 0.18 * np.sin(5 * T + ph) + 0.08 * np.sin(11 * T + 2 * ph)
            if kind == "burst":
                rr = r * wob * (0.55 + 0.5 * folds)
                v = np.clip(1 - R / rr, 0, 1) ** 0.6
                rays = np.clip(1 - R / (r * 1.9), 0, 1) * folds ** 6 * 0.8
                v = np.maximum(v, rays)
                core = np.clip(1 - R / (r * 0.16), 0, 1)
                v = v * (1 - core * 0.8)
            elif kind == "ring":
                band = np.exp(-((R - r * 0.75 * wob) / (r * 0.18)) ** 2)
                band *= 0.75 + 0.25 * folds
                inner = np.clip(1 - R / (r * 0.28), 0, 1) ** 0.8 * 0.9
                v = np.maximum(band, inner)
            else:  # dot
                v = np.clip(1 - R / (r * wob), 0, 1) ** 0.5
                v = v * (1 - np.clip(1 - R / (r * 0.3), 0, 1) * 0.9)
            A[y0:y1, x0:x1] = np.maximum(A[y0:y1, x0:x1], v)
    return np.clip(A, 0, 1)


def dye(H, W, ground, ground2, ties, seed, wrap=False, pale=CREAM):
    """Opaque dyed cloth with resist marks; dye pools darker at the resist edge (tide line) and bleeds into it."""
    if wrap:
        t = wrap_noise(W, H, seed + 1, 40)
        t2 = wrap_noise(W, H, seed + 2, 14)
    else:
        t = fbm(W, H, seed + 1, 90, 3)
        t2 = fbm(W, H, seed + 2, 30, 3)
    base = col3(ground)[None, None] * (1 - t[..., None]) + col3(ground2)[None, None] * t[..., None]
    base *= (0.96 + 0.08 * t2[..., None])
    A = resist(H, W, ties, seed, wrap)
    Ab = gaussian_filter(A, 1.6, mode="wrap" if wrap else "reflect")
    tide = np.clip(gaussian_filter(Ab, 3.0, mode="wrap" if wrap else "reflect") - Ab, 0, 1) * 2.4
    rgb = base * (1 - tide[..., None] * 0.22)
    tint = col3(pale) * 0.82 + col3(ground) * 0.18
    rgb = rgb * (1 - Ab[..., None]) + (col3(pale) * (1 - 0.35 * (1 - Ab[..., None])) + tint * 0.35 * (1 - Ab[..., None])) * Ab[..., None]
    rgb *= weave(H, W, seed + 9, wrap)[..., None]
    return rgba(rgb, np.ones((H, W), np.float32))


def flower_ties(x, y, s):
    """Bunga: a centre burst ringed by six dots."""
    out = [(x, y, s * 0.55, "burst")]
    for k in range(6):
        a = k * math.tau / 6
        out.append((x + math.cos(a) * s, y + math.sin(a) * s, s * 0.22, "dot"))
    return out


def cloth(W, H, x0, w, top, length, ground, ground2, ties, seed, fold_n=5, sway=0.0):
    """A hanging cloth: dyed, folded over the pole at the top, vertical drape folds, a hem that waves, fringe."""
    rng = random.Random(seed)
    # outline
    hem = [(x0 + w * t, top + length + 10 * math.sin(t * math.pi * 2.2 + seed) + rng.uniform(-2, 2)) for t in np.linspace(1, 0, 18)]
    outline = [(x0, top), (x0 + w, top)] + [(x0 + w + sway * 0.4, top + length * 0.6)] + hem + [(x0 + sway * 0.2, top + length * 0.6)]
    m = shape_mask(W, H, outline, smooth=False)
    m = gaussian_filter(m, 0.6)
    cl = dye(H, W, ground, ground2, ties, seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - x0) / max(1, w)
    fold = np.sin(u * math.pi * fold_n + 0.7 * np.sin(yy / 90 + seed)) * np.clip((yy - top) / 120, 0.2, 1)
    shade = 1 - 0.09 * np.clip(fold, 0, 1) - 0.05 * np.clip(-fold, 0, 1) * 0
    light = 1 + 0.05 * np.clip(-fold, 0, 1)
    cl[..., :3] *= (shade * light)[..., None]
    # top fold over the pole: darker band
    band = np.clip(1 - (yy - top) / 26, 0, 1) * (yy >= top)
    cl[..., :3] *= (1 - 0.18 * band)[..., None]
    cl[..., 3] = m
    # fringe
    fr = strokes(W, H, [([(px, py), (px + rng.uniform(-1.5, 1.5), py + rng.uniform(9, 14))], 1.3, None) for px, py in [(x0 + w * t, top + length + 10 * math.sin(t * math.pi * 2.2 + seed) - 1) for t in np.linspace(0.02, 0.98, 30)]])
    cl = over(cl, flat(fr, ground2, 0.9))
    return cl


def kain():
    """Three cloths, saved separately so each can sway on its own."""
    specs = [("kain1", PINK, PINK_D, 220, 600, 31, "flower"), ("kain2", LILAC, LILAC_D, 200, 520, 47, "rings"), ("kain3", TEAL, TEAL_D, 210, 560, 63, "dots")]
    for name, g1, g2, w, L, seed, kind in specs:
        W, H = w + 30, L + 40
        rng = random.Random(seed)
        ties = []
        if kind == "flower":
            for j, y in enumerate(range(70, L, 110)):
                for x in range(40 if j % 2 else 95, w + 20, 110):
                    ties += flower_ties(x + 10, y, 30)
        elif kind == "rings":
            for j, y in enumerate(range(60, L, 92)):
                for x in range(30 if j % 2 else 76, w + 20, 92):
                    ties.append((x + 10, y, 34, "ring"))
                    ties.append((x + 56, y + 46, 9, "dot"))
        else:
            for j, y in enumerate(range(40, L, 46)):
                for x in range(20 + (j % 3) * 15, w + 20, 46):
                    ties.append((x + 10, y, 11 if (x // 46 + j) % 3 else 22, "dot" if (x // 46 + j) % 3 else "burst"))
        cl = cloth(W, H, 15, w, 8, L, g1, g2, ties, seed, fold_n=rng.choice([4, 5]))
        preview(cl, f"js-{name}")
        save(cl, f"{OUT}/{name}.webp", max_w=int(w * 0.95), quality=80)
        clear()


def tile():
    W = H = 320
    ties = []
    for (x, y) in [(80, 80), (240, 240)]:
        ties += flower_ties(x, y, 34)
    for (x, y) in [(240, 80), (80, 240)]:
        ties.append((x, y, 30, "ring"))
    for (x, y) in [(0, 0), (160, 160), (0, 160), (160, 0)]:
        ties.append((x, y, 10, "dot"))
    t = dye(H, W, "#f2c6cf", "#eab4c2", ties, 5, wrap=True)
    save_texture(t, f"{OUT}/tile.webp", quality=84)
    print("tile", os.path.getsize(f"{OUT}/tile.webp") // 1024, "KB")
    preview(np.tile(t, (2, 2, 1)), "js-tile")


def tile2():
    W = H = 320
    ties = []
    for (x, y) in [(80, 80), (240, 240), (240, 80), (80, 240)]:
        ties.append((x, y, 40, "burst" if (x + y) % 320 == 160 else "ring"))
    for (x, y) in [(0, 0), (160, 160), (0, 160), (160, 0)]:
        ties.append((x, y, 12, "dot"))
    t = dye(H, W, "#a9d6d1", "#93cbc5", ties, 8, wrap=True)
    save_texture(t, f"{OUT}/tile2.webp", quality=84)
    print("tile2", os.path.getsize(f"{OUT}/tile2.webp") // 1024, "KB")
    preview(np.tile(t, (2, 2, 1)), "js-tile2")


def medal():
    """A round dyed patch: lilac ground with a big central burst, ringed by dots (emblem / node)."""
    W = H = 300
    ties = [(150, 150, 70, "burst")] + [(150 + math.cos(a) * 112, 150 + math.sin(a) * 112, 13, "dot") for a in np.linspace(0, math.tau, 12, endpoint=False)]
    d = dye(H, W, LILAC, LILAC_D, ties, 12)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = random.Random(3)
    R = np.sqrt((xx - 150) ** 2 + (yy - 150) ** 2)
    T = np.arctan2(yy - 150, xx - 150)
    edge = 138 + 4 * np.sin(T * 7) + 2 * np.sin(T * 13 + 1)
    m = np.clip((edge - R) / 1.5, 0, 1)
    d[..., 3] = m
    preview(d, "js-medal")
    save(d, f"{OUT}/medal.webp", max_w=180, quality=82)


def divider():
    """A strip of teal-dyed cloth with a row of pale dot rings, torn soft edges."""
    W, H = 720, 70
    ties = []
    for i, x in enumerate(range(30, 720, 60)):
        ties.append((x, 35, 16 if i % 2 else 9, "ring" if i % 2 else "dot"))
    d = dye(H, W, PINK, PINK_D, ties, 21)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = fbm(W, H, 4, 10, 2)
    m = np.clip((np.minimum(yy - 10, 60 - yy) + (n - 0.5) * 6) / 1.5, 0, 1) * np.clip((np.minimum(xx - 8, 712 - xx)) / 20, 0, 1)
    d[..., 3] = m
    preview(d, "js-divider")
    save(d, f"{OUT}/divider.webp", max_w=360, quality=82)


def galah():
    """Bamboo drying pole with nodes, tied at both ends with a twist of cord."""
    W, H = 800, 60
    nx = Seq(3000)
    art = blank(W, H)
    pole = shapes(W, H, [rect(6, 22, 794, 40)], smooth=False)
    art = GP(art, pole, "#d9c08a", "#c4a66a", seed=nx(), rough=0.8, streak=1.2)
    art = OV(art, shapes(W, H, [rect(6, 22, 794, 27)], smooth=False), lambda q: flat(q, "#f3e2b4", 0.55))
    art = OV(art, shapes(W, H, [rect(6, 35, 794, 40)], smooth=False), lambda q: flat(q, "#8f7444", 0.4))
    nodes = strokes(W, H, [([(x, 21), (x, 41)], 3.0, None) for x in (70, 230, 400, 560, 720)])
    art = OV(art, nodes, lambda q: gouache_paint(q, "#9c7f48", seed=nx(), rough=0.5, density=0.9))
    cord = strokes(W, H, [([(14 + i * 4, 18), (20 + i * 4, 44)], 2.0, None) for i in range(4)] + [([(770 + i * 4, 18), (776 + i * 4, 44)], 2.0, None) for i in range(4)])
    art = OV(art, cord, lambda q: gouache_paint(q, "#b9a6d8", "#9581c0", seed=nx(), rough=0.4, density=0.95))
    preview(art, "js-galah")
    save(art, f"{OUT}/galah.webp", max_w=780, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
