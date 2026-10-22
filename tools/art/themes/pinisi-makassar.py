"""Pinisi Makassar — a seven-sailed pinisi schooner (two gaff mainsails, two topsails, three jibs on a long bowsprit) at
Losari sunset in watercolour, plus the ship alone as an emblem and a lipa' sabbe Makassar silk-check tile woven at
thread level with a silk sheen. Run: python3 -I pinisi-makassar.py [part ...]   parts: sabbe pinisi losari"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e1_lib import *

OUT = outdir("pinisi-makassar")
PARTS = sys.argv[1:] or ["sabbe", "pinisi", "losari"]
HULL, HULL_D = "#3e1d14", "#24100a"
SAIL, SAIL_W, SAIL_S = "#f6dcb0", "#f4b88a", "#b9727a"


def P(cx, wl, u, pts):
    return [(cx + x * u, wl + y * u) for x, y in pts]


def ship(art, W, H, cx, wl, u, nx, rng, sunset=True, sun_x=None):
    """Paint a pinisi facing left, waterline at wl, unit u px."""
    sail_a, sail_b = (SAIL, SAIL_W) if sunset else ("#f6efe0", "#efe2c8")
    # sails, back to front: mizzen + its topsail, main + topsail, then jibs inner -> outer
    sails = [
        ([(1.25, -1.15), (1.25, -3.5), (2.55, -3.72), (2.7, -1.22)], 0),
        ([(1.25, -3.6), (1.25, -4.55), (2.45, -3.8)], 1),
        ([(-0.55, -1.05), (-0.55, -3.85), (1.0, -4.15), (1.12, -1.15)], 0),
        ([(-0.55, -3.95), (-0.55, -5.15), (0.9, -4.22)], 1),
        ([(-2.85, -1.2), (-0.62, -3.55), (-1.05, -1.0)], 2),
        ([(-3.4, -1.3), (-0.62, -4.3), (-1.5, -1.06)], 2),
        ([(-3.95, -1.4), (-0.62, -4.95), (-1.95, -1.12)], 2),
    ]
    yy, xx = ygrid(W, H)
    for k, (pts, kind) in enumerate(sails):
        # gentle belly: bow the leech/foot slightly
        pp = P(cx, wl, u, pts)
        m = poly(W, H, deform(pp, rng, 1, 0.012), smooth=False)
        art = GP(art, m, sail_a, sail_b, seed=nx(), rough=1.2, streak=0.6)
        art = G(art, m, sail_b, sail_a, seed=nx(), density=0.35, edge=0.6, bloom=0.5, rough=1.5, gran=0.2)
        # shadow along the luff (mast side) and toward the foot
        x0 = min(p[0] for p in pp); x1 = max(p[0] for p in pp)
        sh = m * np.clip(1 - (xx - x0) / max(1, (x1 - x0)), 0, 1) ** 1.5
        art = G(art, sh, SAIL_S, seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=2)
        # seams (cloth panels)
        seams = []
        if kind == 0:
            for t in np.linspace(0.12, 0.92, 7):
                a = (pp[0][0] + (pp[1][0] - pp[0][0]) * t, pp[0][1] + (pp[1][1] - pp[0][1]) * t)
                b = (pp[3][0] + (pp[2][0] - pp[3][0]) * t, pp[3][1] + (pp[2][1] - pp[3][1]) * t)
                seams.append(([a, b], 0.9, None))
        else:
            for t in np.linspace(0.15, 0.85, 4):
                a = (pp[0][0] + (pp[1][0] - pp[0][0]) * t, pp[0][1] + (pp[1][1] - pp[0][1]) * t)
                b = (pp[0][0] + (pp[2][0] - pp[0][0]) * t, pp[0][1] + (pp[2][1] - pp[0][1]) * t)
                seams.append(([a, (b[0] + (pp[2][0] - b[0]) * 0.0, b[1])], 0.8, None))
        art = G(art, strokes(W, H, seams) * m, "#a6765c", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5)
        # hem
        art = G(art, strokes(W, H, [(pp + [pp[0]], 1.4, None)]), "#8e5e48", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5)
    clear()
    # masts, gaffs, bowsprit
    spars = [([(-0.55, -0.5), (-0.55, -5.4)], 0.11), ([(1.25, -0.6), (1.25, -4.75)], 0.1), ([(-2.75, -1.12), (-4.05, -1.42)], 0.09),
             ([(-0.55, -3.85), (1.05, -4.18)], 0.05), ([(1.25, -3.5), (2.6, -3.74)], 0.05), ([(-0.55, -1.08), (1.15, -1.15)], 0.05), ([(1.25, -1.15), (2.75, -1.22)], 0.05)]
    art = G(art, strokes(W, H, [(P(cx, wl, u, p), w * u, (0.0, 0.15)) for p, w in spars]), "#4a2a1a", "#6a3e24", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6)
    # rigging: stays and shrouds
    rig = [([(-0.55, -5.3), (-4.0, -1.42)], 0.018), ([(-0.55, -5.3), (1.25, -4.7)], 0.018), ([(1.25, -4.7), (2.9, -1.0)], 0.018),
           ([(-0.55, -4.0), (-0.95, -0.7)], 0.015), ([(-0.55, -4.0), (-0.15, -0.7)], 0.015), ([(1.25, -3.6), (0.95, -0.75)], 0.015), ([(1.25, -3.6), (1.6, -0.8)], 0.015)]
    art = G(art, strokes(W, H, [(P(cx, wl, u, p), max(0.8, w * u), None) for p, w in rig]), "#3a2418", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    # pennants
    for (mx, top) in ((-0.55, -5.4), (1.25, -4.75)):
        fl = poly(W, H, P(cx, wl, u, [(mx, top), (mx + 0.55, top + 0.08), (mx + 0.48, top + 0.12), (mx, top + 0.2)]), smooth=False)
        art = G(art, fl, "#c4302c", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5)
    # hull: long low sheer rising to a high bow and a higher stern with a raised poop
    hull_pts = [(-2.95, -1.18), (-2.0, -0.8), (-0.5, -0.64), (1.0, -0.68), (1.9, -0.92), (2.45, -1.32), (2.62, -1.3), (2.42, -0.4),
                (1.75, 0.1), (-1.2, 0.14), (-2.15, -0.22), (-2.7, -0.78)]
    sheer = curve([(-2.95, -1.2), (-2.0, -0.8), (-0.5, -0.64), (1.0, -0.68), (1.9, -0.92), (2.5, -1.36)], 30)
    bottom = curve([(2.42, -0.42), (1.75, 0.1), (-1.2, 0.14), (-2.15, -0.22), (-2.75, -0.86)], 30)
    hm = poly(W, H, P(cx, wl, u, sheer + [(2.62, -1.34)] + bottom), smooth=False)
    art = GP(art, hm, HULL, "#52281a", seed=nx(), rough=0.8, streak=0.8)
    art = G(art, hm * np.clip((wl - 0.3 * u - yy) / (0.5 * u), 0, 1), "#a0583a", seed=nx(), density=0.16, edge=0.3, bloom=0.4, rough=1.0, gran=0.3)
    art = G(art, hm * np.clip((yy - (wl - 0.4 * u)) / (0.5 * u), 0, 1), HULL_D, seed=nx(), density=0.6, edge=0.1, bloom=0.2, rough=1)
    # painted bands along the sheer (white + ochre) and planking lines
    band = strokes(W, H, [(P(cx, wl, u, [(-2.75, -1.0), (-1.9, -0.68), (-0.5, -0.53), (1.0, -0.57), (1.9, -0.8), (2.45, -1.15)]), 0.09 * u, None)])
    art = G(art, band * hm, "#efe3c6", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6)
    band2 = strokes(W, H, [(P(cx, wl, u, [(-2.62, -0.84), (-1.9, -0.55), (-0.5, -0.41), (1.0, -0.45), (1.9, -0.67), (2.42, -1.0)]), 0.05 * u, None)])
    art = G(art, band2 * hm, "#d8a03a", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5)
    planks = strokes(W, H, [(P(cx, wl, u, [(-2.3, -0.2 + d), (-1.0, -0.15 + d * 0.6), (1.0, -0.15 + d * 0.6), (2.3, -0.3 + d)]), 0.012 * u + 0.6, None) for d in (-0.1, 0.0, 0.1)])
    art = G(art, planks * hm, "#2a120a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4)
    art = G(art, strokes(W, H, [(P(cx, wl, u, [(-2.78, -0.9), (-2.98, -1.24), (-3.06, -1.46)]), 0.07 * u, (0.0, 0.3)), (P(cx, wl, u, [(2.6, -1.32), (2.44, -0.42)]), 0.05 * u, None)]), HULL_D, seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5)
    rail = [(P(cx, wl, u, [(-2.9, -1.3), (-2.0, -0.92), (-0.5, -0.76), (1.0, -0.8), (1.9, -1.04), (2.5, -1.44)]), 0.03 * u, None)]
    rail += [(P(cx, wl, u, [(x, y - 0.0), (x, y - 0.14)]), 0.025 * u, None) for x, y in [(-2.3, -0.86), (-1.7, -0.76), (-1.1, -0.7), (-0.2, -0.66), (0.6, -0.68), (1.4, -0.8)]]
    art = G(art, strokes(W, H, rail), "#3a1c12", seed=nx(), density=0.8, edge=0.1, bloom=0, rough=0.4)
    # deckhouse at the stern
    dh = poly(W, H, P(cx, wl, u, [(1.45, -0.72), (1.45, -1.05), (2.2, -1.1), (2.2, -0.9)]), smooth=False)
    art = G(art, dh, "#7a4a2c", "#8e5a34", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5)
    art = G(art, strokes(W, H, [(P(cx, wl, u, [(1.4, -1.07), (2.25, -1.12)]), 0.05 * u, None)]), "#efe3c6", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.4)
    if sunset and sun_x is not None:
        # warm rim light on the sun side of every sail
        rim = np.clip((xx - sun_x + 4 * u) / (8 * u), 0, 1) * 0.0
    return art, hm


def sabbe_design(N=96):
    # lipa' sabbe: bold squares of deep red/maroon framed by thin gold, green and white lines (Makassar silk check)
    MAR, RED, GOLD, GRN, WHT, BLK = 1, 2, 3, 4, 5, 6
    bands = []
    # big blocks: alternate red and maroon squares 0..48, 48..96 (handled by base + one band)
    bands.append((44, 92, RED))
    for (a, w, k) in [(0, 2, GOLD), (3, 1, WHT), (5, 1, GRN), (40, 1, GRN), (42, 2, GOLD), (92, 2, GOLD), (20, 1, GOLD), (68, 1, GOLD)]:
        bands.append((a, a + w, k))
    D = np.full((N, N), MAR, np.int32)
    red_w = np.zeros(N, bool); red_w[44:92] = True
    # check: warp red where red_w, weft red where red_w -> mixed squares
    D[:, red_w] = RED
    D[red_w, :] = np.where(D[red_w, :] == RED, MAR, RED)
    for (a, b, k) in bands[1:]:
        D[:, a:b] = k
        D[a:b, :] = k
    return D


if "sabbe" in PARTS:
    D = sabbe_design(96)
    pal = ["#000000", "#5a0f1e", "#b0202c", "#d9a83a", "#2f6a3a", "#f1e6cf", "#1a0c10"]
    cloth = ikat(D, pal, p=3, mode="double", amp=0.25, coh=1.0, along=6, seed=31, bleed=0.3, face=0.5, slub=0.12, fibre=0.06, thread_var=0.03)
    # silk sheen: soft diagonal light
    H_, W_ = cloth.shape[:2]
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    sheen = 0.5 + 0.5 * np.sin(2 * math.pi * (xx + yy) / W_)
    cloth = np.clip(cloth * (0.9 + 0.22 * sheen[..., None]), 0, 1)
    prev_rgb(tile_to(cloth, 600, 600), "sabbe")
    save_rgb_arr(cloth, f"{OUT}/sabbe.webp", quality=78)
    clear()

if "pinisi" in PARTS:
    W, H = 600, 600
    nx = Seq(11100); rng = random.Random(111)
    art = blank(W, H)
    art, hm = ship(art, W, H, 330, 510, 90, nx, rng, sunset=False)
    # a little water under the hull
    yy, xx = ygrid(W, H)
    wv = sea_strokes(W, H, 512, 560, rng, n=60, length=(20, 70), width=(1.2, 2.6))
    wv = wv * np.clip(1 - np.abs(xx - 320) / 280, 0, 1)
    art = G(art, wv, "#3f7a96", "#2a5a78", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=1)
    preview(art, "pinisi", tone="#f6eee2")
    save(art, f"{OUT}/pinisi.webp", max_w=320, quality=82)
    clear()

if "losari" in PARTS:
    W, H = 780, 1080
    nx = Seq(12100); rng = random.Random(121)
    yy, xx = ygrid(W, H)
    hz = 700
    art = painted_sky(W, H, [(0.0, "#3b2f5c"), (0.22, "#7a4a78"), (0.42, "#d0687a"), (0.56, "#f2a06a"), (0.65, "#fbd08a"), (0.66, "#e9a06e"), (1.0, "#4a3560")], seed=7, streak=0.4, grain=0.6)
    # soft watercolour cloud bands catching light
    for (cy, x0, x1, c1, c2) in [(170, -40, 520, "#8a5a8a", "#a8688a"), (300, 260, 820, "#e08a86", "#f0a88a"), (420, -40, 400, "#f2a88a", "#f7c08e"), (520, 420, 820, "#f8c890", "#fbd8a0")]:
        cl = poly(W, H, deform([(x0, cy), (x1, cy - 16), (x1 + 20, cy + 10), (x0 + 30, cy + 24)], rng, 3, 0.12))
        art = G(art, cl, c1, c2, seed=nx(), density=0.6, edge=0.45, bloom=0.5, rough=6)
    clear()
    # the sun, low on the right
    sx, sy, sr = 716, hz - 36, 40
    disc, halo = sun_disc(W, H, sx, sy, sr)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ffd890"), halo * 0.55 * (yy < hz)))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#fff1c8"), disc * (yy < hz)))
    # far coast: Losari skyline + Makassar shore, flat violet
    sk = []
    x = -10
    while x < W:
        w_ = rng.uniform(14, 40); h_ = rng.uniform(6, 34) if x > 380 else rng.uniform(4, 14)
        sk.append([(x, hz), (x, hz - h_), (x + w_, hz - h_), (x + w_, hz)])
        x += w_ + rng.uniform(0, 6)
    art = G(art, shapes(W, H, sk, smooth=False), "#5e3f66", "#6e4a6e", seed=nx(), density=0.85, edge=0.3, bloom=0.2, rough=1)
    # sea
    sea = poly(W, H, [(0, hz), (W, hz), (W, H), (0, H)], smooth=False)
    art = G(art, sea, "#6a4a7a", "#3a2c58", seed=nx(), density=0.95, edge=0.0, bloom=0.3, rough=6)
    art = G(art, sea * np.clip((yy - hz) / 260, 0, 1), "#2a2048", seed=nx(), density=0.6, edge=0.0, bloom=0.3, rough=6)
    # golden glitter path under the sun
    gl = sea_strokes(W, H, hz + 3, H, rng, n=420, length=(10, 60), width=(1.0, 3.2))
    path = np.exp(-((xx - sx) / np.maximum(36 + (yy - hz) * 0.5, 8)) ** 2)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ffd38a"), gl * path * sea * 0.95))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f7a9a0"), gl * (1 - path) * sea * 0.35))
    clear()
    # the pinisi, big, left of the sun
    cx, wl, u = 432, hz + 150, 112
    before = art.copy()
    art, hm = ship(art, W, H, cx, wl, u, nx, rng, sunset=True, sun_x=sx)
    # reflection: everything the ship painted, mirrored at the waterline, broken by ripples
    changed = np.clip(np.abs(art[..., :3] - before[..., :3]).sum(-1) * 6, 0, 1)
    changed[wl + int(0.15 * u):] = 0
    wl0 = wl + int(0.1 * u)
    src = art[: wl0 + 1][::-1]; msk = changed[: wl0 + 1][::-1]
    n_ = min(H - wl0, src.shape[0])
    rr = np.zeros_like(art); rm = np.zeros_like(changed)
    rr[wl0:wl0 + n_] = src[:n_]; rm[wl0:wl0 + n_] = msk[:n_]
    off = (fbm(W, H, 77, 14, 2) - 0.5) * 18
    from scipy.ndimage import map_coordinates
    cy_, cx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    for ch in range(3):
        rr[..., ch] = map_coordinates(rr[..., ch], [cy_, cx_ + off], order=1, mode="nearest")
    rm = map_coordinates(rm, [cy_, cx_ + off], order=1, mode="nearest")
    rm = gaussian_filter(rm, (3, 1)) * np.clip(1 - (yy - wl0) / 330, 0, 1) * 0.5
    rr[..., :3] = rr[..., :3] * 0.62 + C("#3a2c58") * 0.38
    art = over(art, rgba(rr[..., :3], rm))
    cs = ellipses(W, H, [(cx - 0.2 * u, wl + 0.16 * u, 2.6 * u, 0.12 * u, 0)])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#1c1228"), gaussian_filter(cs, 5) * 0.75))
    lips = sea_strokes(W, H, wl - 4, wl + 0.3 * u, rng, n=90, length=(20, 70), width=(1.2, 3)) * np.clip(1 - np.abs(xx - cx) / (3.2 * u), 0, 1)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f2b48a"), lips * 0.55))
    # small lepa-lepa canoe in the foreground
    cv = poly(W, H, [(80, 960), (210, 958), (220, 950), (200, 970), (92, 972), (70, 952)])
    art = G(art, cv, "#2a1a24", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6)
    art = G(art, strokes(W, H, [([(130, 958), (110, 900)], 2.0, None)]), "#2a1a24", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4)
    art = G(art, poly(W, H, [(112, 904), (152, 950), (120, 952)], smooth=False), "#e9b98a", seed=nx(), density=0.8, edge=0.4, bloom=0.2, rough=0.6)
    art = np.nan_to_num(art)
    preview(art, "losari")
    save_rgb(art, f"{OUT}/losari.webp", quality=72)
    clear()
