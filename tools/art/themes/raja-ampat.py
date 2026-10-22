"""Raja Ampat — watercolour: limestone karst 'mushroom' islets with jungle domes and undercut notches standing in a
clear turquoise lagoon, shallow sand and coral seen through the water, a wide pale sky with drifting cumulus.
Run: python3 -I raja-ampat.py [part ...]   parts: scene isle cloud divider wave star
Assets -> public/themes/art/raja-ampat/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e2_lib import *

OUT = outdir("raja-ampat")
PARTS = sys.argv[1:] or ["scene", "isle", "cloud", "divider", "wave", "star"]
LEAF_L, LEAF_M, LEAF_D, LEAF_DD = "#a9c46a", "#5f9a4a", "#2f6b47", "#1d4a3c"
ROCK_L, ROCK_D = "#cdbf9f", "#7d7462"


def islet(art, W, H, cx, wl, w, h, nx, rng, lean=0.0, far=0.0):
    """Paint one karst mushroom islet whose notch sits on the waterline wl. far (0..1) fades toward haze blue."""
    top = wl - h
    sk = lean * h
    # jungle dome: a bumpy crown line of tree tops, draping down to ~70% of the height
    crowns = []
    nb = max(7, int(w / 14))
    for k in range(nb):
        t = k / (nb - 1)
        ang = math.pi * (1 - t)
        bx = cx + sk * 0.3 + math.cos(ang) * w * 0.47
        by = top + h * 0.42 - math.sin(ang) * h * 0.36 + rng.uniform(-0.03, 0.03) * h
        r = w * rng.uniform(0.07, 0.11)
        crowns.append((bx, by, r * rng.uniform(1.0, 1.25), r, rng.uniform(-20, 20)))
    core = [(cx - w * 0.5 + sk * 0.2, top + h * 0.62), (cx - w * 0.44 + sk * 0.2, top + h * 0.3), (cx + sk * 0.3, top + h * 0.1),
            (cx + w * 0.45 + sk * 0.3, top + h * 0.3), (cx + w * 0.5 + sk * 0.2, top + h * 0.66)]
    canopy = np.maximum(ellipses(W, H, crowns), poly(W, H, core, smooth=True))
    drape = []
    for k in range(int(w / 10)):
        x = cx + rng.uniform(-0.48, 0.48) * w
        drape.append((x, top + h * rng.uniform(0.55, 0.72), w * rng.uniform(0.03, 0.06), h * rng.uniform(0.06, 0.12), 0))
    canopy = np.maximum(canopy, ellipses(W, H, drape))
    canopy = displace(canopy, nx(), 2.0, 14)
    # limestone: from under the trees to the water, pinched into a deep undercut notch
    inset = w * rng.uniform(0.1, 0.16)
    body = [(cx - w * 0.48, top + h * 0.5), (cx + w * 0.49, top + h * 0.5), (cx + w * 0.47, wl - h * 0.2),
            (cx + w * 0.5 - inset, wl - h * 0.12), (cx + w * 0.5 - inset * 1.1, wl + 2), (cx - w * 0.5 + inset * 1.1, wl + 2),
            (cx - w * 0.5 + inset, wl - h * 0.12), (cx - w * 0.47, wl - h * 0.21)]
    bm = displace(poly(W, H, body, smooth=False), nx(), 2.0, 16)
    bm = np.clip(bm - canopy * 0.9, 0, 1)
    c = lambda col, haze="#a9bccb": mix_hex(col, haze, far)
    art = G(art, bm, c(ROCK_L), c(ROCK_D), seed=nx(), density=0.95, edge=0.35, bloom=0.15, rough=1.5, feather=0.9)
    streak = hatch(W, H, math.pi / 2 + 0.04, max(2.5, w / 60), 0.16, nx(), 2.0) * bm * ygrad(W, H, top + h * 0.45, wl)
    art = G(art, streak, c("#5f5848"), seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    notch = bm * ygrad(W, H, wl - h * 0.24, wl - h * 0.1)
    art = G(art, notch, c("#3b443f", "#7d93a6"), c("#1e2b2a", "#7d93a6"), seed=nx(), density=0.95, edge=0.5, rough=1.0, feather=0.8)
    # canopy washes: light, mid clumps, shade on the lower right, fine crown dabs, sunlit tops
    art = G(art, canopy, c(LEAF_L, "#b8c9d0"), c(LEAF_M, "#a5b9c4"), seed=nx(), density=0.95, edge=0.55, rough=1.5, feather=0.9)
    clump = canopy * np.clip((fbm(W, H, nx(), max(6, w / 10), 3) - 0.45) * 4, 0, 1)
    art = G(art, clump, c(LEAF_M, "#9fb2bf"), seed=nx(), density=0.6, edge=0.6, rough=1.0, feather=0.7)
    sh = canopy * np.clip(xgrad(W, H, cx - w * 0.3, cx + w * 0.55) * 0.6 + ygrad(W, H, top + h * 0.2, top + h * 0.7) * 0.7 - 0.25, 0, 1)
    art = G(art, sh, c(LEAF_D, "#8299ab"), seed=nx(), density=0.75, edge=0.4, rough=1.5, feather=1.0)
    crowns2 = []
    for _ in range(int(w * h / 160)):
        x = rng.uniform(cx - w * 0.5, cx + w * 0.5); y = rng.uniform(top, top + h * 0.7)
        r = w * rng.uniform(0.028, 0.05) + 1.2
        crowns2.append((x, y, r * 1.15, r, 0))
    d = max(1.2, w * 0.012)
    e0 = ellipses(W, H, crowns2)
    eo = ellipses(W, H, [(x + d, y + d * 1.2, a, b, r) for x, y, a, b, r in crowns2])
    shade = np.clip(eo - e0 * 0.85, 0, 1) * canopy
    art = G(art, shade * np.clip(sh + 0.35, 0, 1), c(LEAF_DD, "#7f99aa"), seed=nx(), density=0.55, edge=0.25, rough=0.6, feather=0.6)
    lit = np.clip(ellipses(W, H, [(x - d, y - d, a * 0.8, b * 0.7, r) for x, y, a, b, r in crowns2]) - eo * 0.9, 0, 1) * canopy * np.clip(1 - sh * 1.5, 0, 1)
    art = G(art, lit, c("#d6e48c", "#cfdbe0"), seed=nx(), density=0.5, edge=0.15, rough=0.6, feather=0.6)
    return art


def mix_hex(a, b, t):
    ca, cb = col_arr(a), col_arr(b)
    c = ca * (1 - t) + cb * t
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def sky(W, H, top_col="#9cc6dc", low_col="#eef3ec", seed=1):
    s = painted_sky(W, H, [(0, top_col), (0.5, "#bcd9e4"), (1, low_col)], seed=seed, streak=0.12, grain=0.1)
    return s[..., :3]


def clouds(W, H, items, nx, rng):
    """Cumulus: cauliflower tops on a flat base, white left free, blue-violet shade washed into the underside."""
    art = blank(W, H)
    for cx, cy, s in items:
        blobs = []
        for k in range(14):
            t = k / 13
            ang = math.pi * (1 - t)
            r = s * rng.uniform(0.13, 0.24) * (1.25 - abs(t - 0.5))
            blobs.append((cx + math.cos(ang) * s * 0.85, cy - math.sin(ang) * s * 0.32 + rng.uniform(-0.05, 0.05) * s, r, r * 0.9, 0))
        for k in range(5):
            blobs.append((cx + rng.uniform(-0.4, 0.4) * s, cy - s * rng.uniform(0.25, 0.45), s * rng.uniform(0.16, 0.26), s * rng.uniform(0.15, 0.22), 0))
        m = ellipses(W, H, blobs) * (1 - ygrad(W, H, cy + s * 0.04, cy + s * 0.1))
        m = np.maximum(m, ellipses(W, H, [(cx, cy, s * 0.9, s * 0.08, 0), (cx, cy - s * 0.14, s * 0.78, s * 0.2, 0)]))
        m = displace(m, nx(), 3, 18)
        art = G(art, m, "#ffffff", "#fdfbf5", seed=nx(), density=0.9, edge=0.0, bloom=0.3, rough=2, feather=2.2, gran=0.05)
        und = m * np.clip(ygrad(W, H, cy - s * 0.3, cy + s * 0.08) * 1.1 - 0.15, 0, 1)
        art = G(art, und, "#9fb0c8", "#b9b7cc", seed=nx(), density=0.5, edge=0.45, bloom=0.5, rough=3, feather=2)
        crev = m * np.clip((fbm(W, H, nx(), s * 0.12, 3) - 0.55) * 3, 0, 1) * ygrad(W, H, cy - s * 0.5, cy)
        art = G(art, crev, "#c2cbdb", seed=nx(), density=0.35, edge=0.5, rough=2, feather=1.2)
    return art


def lagoon(W, H, y0, nx, rng, deep="#1f7d93", mid="#2fb3b6", shallow="#9fe0cf", sand="#efe4c4"):
    """Water from the horizon (y0) to the bottom: deep blue-teal far, turquoise, clear sandy shallows near."""
    t = ygrad(W, H, y0, H)
    base = np.zeros((H, W, 3), np.float32)
    stops = [(0, col_arr("#5e9fb4")), (0.12, col_arr(deep)), (0.45, col_arr(mid)), (0.8, col_arr(shallow)), (1.0, col_arr(sand))]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        k = np.clip((t - t0) / (t1 - t0), 0, 1)[..., None]
        sel = ((t >= t0) & (t <= t1))[..., None]
        base = np.where(sel, c0 * (1 - k) + c1 * k, base)
    return base


# ------------------------------------------------------------------ parts
def part_scene():
    W, H = 780, 1500
    rng = random.Random(11); nx = Seq(300)
    wl = 780
    rgb = sky(W, H, seed=nx())
    cl = clouds(W, H, [(160, 250, 180), (620, 170, 140), (540, 420, 110), (110, 520, 80), (690, 560, 60)], nx, rng)
    lowc = clouds(W, H, [(150, 756, 110), (430, 760, 140), (690, 758, 90)], nx, rng)
    lowc[..., 3] *= 0.4
    rgb = comp_rgb(comp_rgb(rgb, cl), lowc)
    clear()
    water = lagoon(W, H, wl, nx, rng)
    below = (np.arange(H)[:, None] >= wl).astype(np.float32) * np.ones((1, W), np.float32)
    rgb = rgb * (1 - below[..., None]) + water * below[..., None]
    wash = blank(W, H)
    band = rect(W, H, -20, wl, W + 20, wl + 60)
    wash = G(wash, band, "#1d6f8a", "#2a8aa0", seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=6, feather=4)
    reef = []
    for _ in range(26):
        y = rng.uniform(wl + 220, H - 160); x = rng.uniform(-40, W + 40)
        k = 0.5 + (y - wl) / H
        reef.append((x, y, rng.uniform(30, 80) * k, rng.uniform(8, 20) * k, rng.uniform(-10, 10)))
    rm = displace(ellipses(W, H, reef), nx(), 12, 26)
    wash = G(wash, rm, "#3a9e93", "#6d9a72", seed=nx(), density=0.28, edge=0.35, bloom=0.6, rough=10, feather=5)
    sandp = displace(ellipses(W, H, [(rng.uniform(0, W), rng.uniform(wl + 380, H), rng.uniform(80, 180), rng.uniform(20, 50), 0) for _ in range(12)]), nx(), 14, 40)
    wash = G(wash, sandp * ygrad(W, H, wl + 300, H), "#f6efd8", seed=nx(), density=0.45, edge=0.15, bloom=0.5, rough=8, feather=8)
    rgb = comp_rgb(rgb, wash)
    clear()
    groups = [
        (wl, [(240, 64, 40, 0.78, 0), (318, 40, 26, 0.82, 0), (548, 84, 46, 0.72, 0), (626, 46, 30, 0.78, 0), (40, 56, 34, 0.75, 0)]),
        (wl + 30, [(420, 150, 104, 0.4, 0.04), (170, 110, 80, 0.45, -0.04)]),
        (wl + 110, [(80, 210, 170, 0.08, -0.04)]),
        (wl + 150, [(650, 330, 270, 0.0, 0.03)]),
    ]
    for gwl, items in groups:
        isl = blank(W, H)
        for cx, w, h, far, lean in items:
            isl = islet(isl, W, H, cx, gwl, w, h, nx, rng, lean=lean, far=far)
            clear()
        isl[..., 3] = np.clip(isl[..., 3] * 2.6, 0, 1)
        ref = reflect(isl, gwl, seed=nx(), amp=3 + (gwl - wl) / 30, wl=5, fade=3.0, blur=1.0)
        ref[..., :3] = ref[..., :3] * 0.65 + col_arr("#1d7890") * 0.35
        ref[..., 3] *= 0.55
        rgb = comp_rgb(rgb, ref)
        rip = ripple_lines(W, H, gwl + 2, gwl + 40 + (gwl - wl), nx(), density=0.25, lmin=6, lmax=30)
        rgb = comp_rgb(rgb, flat(rip * (ref[..., 3] > 0.05), "#e6f7f2", 0.45))
        rgb = comp_rgb(rgb, isl)
        clear()
    rip = ripple_lines(W, H, wl + 300, H - 220, nx(), density=0.18, lmin=10, lmax=50)
    rgb = comp_rgb(rgb, flat(rip, "#f2fbf6", 0.4))
    cn = fbm(W, H, nx(), 22, 3)
    caus = np.clip(1 - np.abs(np.sin(cn * 30)) * 5, 0, 1) * ygrad(W, H, wl + 420, H)
    rgb = comp_rgb(rgb, flat(gaussian_filter(caus, 0.7), "#fbfff4", 0.35))
    paperk = np.asarray(paper(W, H, "#ffffff", 5), np.float32) / 255
    rgb = rgb * (0.97 + 0.03 * paperk)
    prev_rgb(rgb, "ra-scene")
    rgb_save(rgb, f"{OUT}/scene.webp", quality=76)
    clear()


def part_isle():
    W, H = 640, 420
    rng = random.Random(5); nx = Seq(900)
    art = blank(W, H)
    wl = 250
    art = islet(art, W, H, 210, wl, 140, 110, nx, rng, far=0.45)
    clear()
    art = islet(art, W, H, 400, wl, 250, 200, nx, rng, lean=0.03)
    art[..., 3] = np.clip(art[..., 3] * 2.2, 0, 1)
    clear()
    ref = reflect(art, wl, seed=nx(), amp=4, wl=5, fade=3.2, blur=1.0)
    ref[..., :3] = ref[..., :3] * 0.7 + col_arr("#1f8796") * 0.3
    ref[..., 3] *= 0.55
    water = displace(poly(W, H, [(40, wl - 2), (W - 30, wl - 2), (W - 80, wl + 110), (90, wl + 120)], smooth=True), nx(), 20, 60)
    wash = blank(W, H)
    wash = G(wash, water, "#43b8bd", "#8fd8cc", seed=nx(), density=0.55, edge=0.6, bloom=0.5, rough=10, feather=5)
    wash = over(wash, ref)
    rip = ripple_lines(W, H, wl + 6, wl + 100, nx(), density=0.5, x0=100, x1=W - 100)
    wash = over(wash, flat(rip * water, "#f4fff9", 0.6))
    art = over(wash, art)
    preview(art, "ra-isle")
    save(art, f"{OUT}/isle.webp", max_w=520, quality=82)
    clear()


def part_cloud():
    W, H = 640, 260
    rng = random.Random(3); nx = Seq(1300)
    art = clouds(W, H, [(320, 150, 260)], nx, rng)
    preview(art, "ra-cloud", bg="#9cc6dc")
    save(art, f"{OUT}/cloud.webp", max_w=420, quality=80)
    clear()


def part_divider():
    W, H = 640, 120
    rng = random.Random(8); nx = Seq(1500)
    art = blank(W, H)
    wl = 78
    for cx, w, h, far in [(250, 46, 36, 0.4), (320, 80, 62, 0.0), (392, 40, 30, 0.35)]:
        art = islet(art, W, H, cx, wl, w, h, nx, rng, far=far)
    line = strokes(W, H, [([(70 + i * 5, wl + 4 + math.sin(i * 0.35) * 1.5) for i in range(100)], 4.0, (0.3, 0.3))])
    art = G(art, line, "#2fa3ad", "#79cfc4", seed=nx(), density=0.7, edge=0.5, rough=1.5, feather=0.8)
    line2 = strokes(W, H, [([(150 + i * 4, wl + 13 + math.sin(i * 0.4 + 1) * 1.2) for i in range(85)], 2.2, (0.4, 0.4))])
    art = G(art, line2, "#79cfc4", seed=nx(), density=0.6, edge=0.4, rough=1, feather=0.6)
    preview(art, "ra-divider")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=82)
    clear()


def part_wave():
    """Repeat-x shoreline: clear turquoise water edge with a foam lip (tops of the lagoon bands)."""
    W, H = 1200, 150
    nx = Seq(1700)
    wrap = np.concatenate
    art = blank(W, H)
    ys = [70 + 14 * math.sin(i / 1199 * math.tau * 3) + 6 * math.sin(i / 1199 * math.tau * 7) for i in range(W)]
    pts = [(-40, H + 10)] + [(i, ys[i]) for i in range(0, W, 8)] + [(W + 40, ys[-1]), (W + 40, H + 10)]
    m = poly(W, H, pts, smooth=True)
    art = G(art, m, "#7fd3c6", "#3fb2b6", seed=nx(), density=0.75, edge=0.7, bloom=0.4, rough=5, feather=2)
    foam = strokes(W, H, [([(i, ys[i] + 3) for i in range(0, W, 6)], 4.5, None)])
    art = G(art, foam, "#ffffff", seed=nx(), density=0.6, edge=0.2, rough=2)
    # make it tile: crossfade the ends
    art = over(art, flat(ygrad(W, H, H - 60, H - 8), "#4ab6b8"))
    preview(art, "ra-wave", tone="#f7f4ea")
    save_full(art, f"{OUT}/wave.webp", size=(900, 112), quality=80)
    clear()


def part_star():
    W, H = 200, 200
    rng = random.Random(4); nx = Seq(1900)
    art = blank(W, H)
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5 + rng.uniform(-0.05, 0.05)
        r = 82 if k % 2 == 0 else 30
        pts.append((100 + math.cos(a) * r, 104 + math.sin(a) * r))
    m = displace(poly(W, H, pts, smooth=True), nx(), 3, 20)
    art = G(art, m, "#e58a4e", "#d1683e", seed=nx(), density=0.9, edge=0.7, bloom=0.3, rough=2)
    dots = circles(W, H, [(100 + math.cos(-math.pi / 2 + k * math.pi / 5 * 2) * r, 104 + math.sin(-math.pi / 2 + k * math.pi / 5 * 2) * r, 3.2) for k in range(5) for r in (18, 32, 46, 60)])
    art = G(art, dots, "#fbe1b8", seed=nx(), density=0.8, edge=0.2, rough=0.6, feather=0.6)
    preview(art, "ra-star")
    save(art, f"{OUT}/star.webp", max_w=96, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
