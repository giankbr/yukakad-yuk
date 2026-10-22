"""Bromo Tengger — watercolour landscape at dawn: the Tengger caldera with its sand sea, the ribbed Batok cone, the smoking
Bromo crater, Semeru far behind, layered mist; the green corrugated Bukit Teletubbies ridges; Javanese edelweiss (the
Tengger 'tana layu' flower); a woven Tengger sarung check.
Run: python3 -I bromo-tengger.py [part ...]   parts: scene ridge mist edelweiss divider sarung
Assets -> public/themes/art/bromo-tengger/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f2_lib import *  # noqa

OUT = outdir("bromo-tengger")
PARTS = sys.argv[1:] or ["scene", "ridge", "mist", "edelweiss", "divider", "sarung"]


def sky_rgb(W, H, stops, seed):
    return painted_sky(W, H, stops, seed=seed, streak=0.25, grain=0.15)[..., :3]


def mist_layer(W, H, bands, nx, rng, col="#fbf3ee"):
    """Soft horizontal mist banks: [(y, thickness, x0, x1, density)]."""
    art = blank(W, H)
    for y, th, x0, x1, dens in bands:
        blobs = []
        x = x0
        while x < x1:
            r = th * rng.uniform(1.6, 3.2)
            blobs.append((x, y + rng.uniform(-0.3, 0.3) * th, r, th * rng.uniform(0.45, 0.8), rng.uniform(-3, 3)))
            x += r * 0.9
        m = displace(ellipses(W, H, blobs), nx(), th * 0.4, max(12, th))
        art = G(art, m, col, mix_hex(col, "#e9dde6", 0.5), seed=nx(), density=dens, edge=0.05, bloom=0.45, rough=th * 0.3,
                feather=th * 0.35, gran=0.02, pad=int(th * 2))
    return art


def flutes(W, H, ax, ay, n, seed, warp=0.35):
    """Radial fluting field around an apex: 0..1 where 1 = gully floor. n = number of gullies across 180 deg."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    th = np.arctan2(xx - ax, np.maximum(yy - ay, 1.0))
    nz = fbm(W, H, seed, 30, 3) - 0.5
    f = 0.5 + 0.5 * np.sin(th * n + nz * math.tau * warp + np.sin(th * n * 0.37) * 1.2)
    return f.astype(np.float32), th


def vflutes(W, H, period, seed, warp=0.5):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nz = fbm(W, H, seed, 40, 3) - 0.5
    return (0.5 + 0.5 * np.sin(xx / period * math.tau + nz * math.tau * warp + yy / period * 0.15)).astype(np.float32)


def cone_ribs(cx, apex_y, base_y, half, n, rng, crater=0.0):
    """Radial gully lines of a volcanic cone, from just under the summit down to the base."""
    items = []
    for k in range(n):
        t = (k + rng.uniform(0.2, 0.8)) / n
        bx = cx - half + 2 * half * t
        top_x = cx + (bx - cx) * (0.08 + crater)
        ty = apex_y + (base_y - apex_y) * rng.uniform(0.04, 0.12)
        mid = ((top_x + bx) / 2 + rng.uniform(-4, 4), (ty + base_y) / 2 - abs(bx - cx) * 0.05)
        items.append(([(top_x, ty), mid, (bx, base_y + rng.uniform(-4, 6))], rng.uniform(1.6, 3.6), (0.1, 0.3)))
    return items


def part_scene():
    W, H = 780, 1500
    rng = random.Random(21); nx = Seq(400)
    rgb = sky_rgb(W, H, [(0, "#34356a"), (0.16, "#5f5590"), (0.31, "#b9809e"), (0.41, "#f0a98f"), (0.48, "#fbd3a2"), (0.56, "#f2cfb3"), (1, "#c9b3a4")], nx())
    sun = radial(W, H, 170, 650, 360, sy=0.55)
    rgb = comp_rgb(rgb, flat(sun ** 1.5, "#fff1d2", 0.9))
    # soft dawn cloud banks: long flat lenses, lit apricot on the underside
    cl = blank(W, H)
    lens = []
    for _ in range(14):
        y = rng.uniform(170, 560); x = rng.uniform(-100, W)
        L = rng.uniform(140, 380)
        lens.append((x, y, L / 2, rng.uniform(12, 24), rng.uniform(-2, 1)))
    cm = displace(ellipses(W, H, lens), nx(), 10, 30)
    cl = G(cl, cm, "#8a6b9c", "#a77a9f", seed=nx(), density=0.62, edge=0.3, bloom=0.5, rough=10, feather=6)
    lit = cm * ygrad(W, H, 300, 600) * np.clip(1 - xgrad(W, H, 100, 700) * 0.6, 0, 1)
    cl = G(cl, lit, "#f7b79c", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=6, feather=5)
    rgb = comp_rgb(rgb, cl)
    clear()
    # Semeru: far, pale violet, ash puff drifting
    far = blank(W, H)
    sem = poly(W, H, [(470, 830), (610, 680), (690, 610), (722, 594), (752, 598), (800, 640), (940, 780), (940, 830)], smooth=True)
    sem = displace(sem, nx(), 3, 20)
    far = G(far, sem, "#a497b8", "#b2a1bd", seed=nx(), density=0.85, edge=0.3, bloom=0.3, rough=2, feather=1.5)
    fl, _ = flutes(W, H, 736, 594, 40, nx())
    far = G(far, sem * np.clip((fl - 0.75) * 4, 0, 1) * ygrad(W, H, 600, 720), "#8a7fa4", seed=nx(), density=0.35, edge=0.1, rough=1, feather=1)
    far = G(far, sem * np.clip(1 - xgrad(W, H, 600, 740), 0, 1) * 0.7, "#efbfb2", seed=nx(), density=0.45, edge=0.1, rough=2, feather=2)
    puff = ellipses(W, H, [(742, 576, 18, 10, -10), (760, 560, 24, 13, -15), (784, 544, 30, 14, -15)])
    far = G(far, displace(puff, nx(), 5, 14), "#efe2e6", "#cbbbd4", seed=nx(), density=0.6, edge=0.2, bloom=0.5, rough=4, feather=3)
    rgb = comp_rgb(rgb, far)
    clear()
    # caldera wall: jagged, fluted rim
    wall = blank(W, H)
    pts = [(-20, 900)]
    x = -20
    while x < W + 40:
        pts.append((x, 768 + 24 * math.sin(x / 90) + rng.uniform(-9, 9) - 34 * math.exp(-((x - 40) / 130) ** 2)))
        x += rng.uniform(16, 34)
    pts += [(W + 40, 900)]
    wm = displace(poly(W, H, pts, smooth=True), nx(), 2, 16)
    wall = G(wall, wm, "#8b7c9c", "#97829e", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=2, feather=1)
    vf = vflutes(W, H, 17, nx())
    wall = G(wall, wm * np.clip((vf - 0.72) * 4, 0, 1) * (1 - ygrad(W, H, 780, 840)) * fbm(W, H, nx(), 50, 2), "#675a7e", seed=nx(), density=0.45, edge=0.15, rough=1, feather=1)
    wall = G(wall, wm * np.clip((0.25 - vf) * 4, 0, 1) * (1 - ygrad(W, H, 780, 830)) * np.clip(1 - xgrad(W, H, 0, 500), 0, 1), "#e1b2a4", seed=nx(), density=0.4, edge=0.1, rough=1, feather=1)
    rgb = comp_rgb(rgb, wall)
    clear()
    rgb = comp_rgb(rgb, mist_layer(W, H, [(826, 22, -40, W + 40, 0.75), (800, 12, 300, W + 40, 0.5)], nx, rng))
    clear()
    # Bromo crater: broad truncated grey-brown cone, deeply gullied ash flanks
    br = blank(W, H)
    bpts = [(320, 935), (410, 850), (470, 800), (500, 780), (535, 788), (575, 774), (612, 782), (645, 794), (705, 850), (830, 935)]
    bm = displace(poly(W, H, bpts, smooth=True), nx(), 2, 14)
    br = G(br, bm, "#a39085", "#857770", seed=nx(), density=0.95, edge=0.45, bloom=0.2, rough=1.5, feather=1)
    fl, th = flutes(W, H, 560, 700, 26, nx())
    gully = bm * np.clip((fl - 0.62) * 3.2, 0, 1) * ygrad(W, H, 780, 820) * (0.4 + 0.6 * fbm(W, H, nx(), 24, 2))
    br = G(br, gully, "#4c4352", "#5a4c50", seed=nx(), density=0.65, edge=0.35, rough=1, feather=0.8)
    spur = bm * np.clip((0.22 - fl) * 4, 0, 1) * np.clip(1.1 - xgrad(W, H, 380, 640), 0, 1)
    br = G(br, spur, "#f0bc9a", seed=nx(), density=0.55, edge=0.15, rough=1, feather=0.8)
    br = G(br, bm * xgrad(W, H, 570, 800) * 0.8, "#5d5266", seed=nx(), density=0.45, edge=0.2, rough=2, feather=2)
    rim = np.clip(bm - np.roll(bm, 5, 0), 0, 1) * ygrad(W, H, 760, 800) * (1 - ygrad(W, H, 800, 830))
    br = G(br, rim, "#3d3442", seed=nx(), density=0.5, edge=0.2, rough=1, feather=0.6)
    rgb = comp_rgb(rgb, br)
    clear()
    # sulphur plume
    pl = blank(W, H)
    blobs = []
    for k in range(20):
        t = k / 19
        cx = 562 - t * 120 + math.sin(t * 5) * 22
        cy = 782 - t * 280
        r = 18 + t * 52
        blobs.append((cx + rng.uniform(-10, 10), cy, r * rng.uniform(0.9, 1.15), r * rng.uniform(0.7, 0.9), rng.uniform(-20, 20)))
    pm = displace(ellipses(W, H, blobs), nx(), 12, 26)
    pl = G(pl, pm, "#fbf2ea", "#f1e1dc", seed=nx(), density=0.85, edge=0.15, bloom=0.5, rough=8, feather=5, gran=0.03)
    pshade = pm * np.clip(xgrad(W, H, 420, 640) * 0.7 + ygrad(W, H, 520, 800) * 0.4 - 0.15, 0, 1)
    pl = G(pl, pshade, "#a594ad", "#b5a0ae", seed=nx(), density=0.5, edge=0.4, bloom=0.5, rough=6, feather=4)
    plit = pm * np.clip(1 - xgrad(W, H, 380, 520), 0, 1)
    pl = G(pl, plit, "#ffd2b0", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=6, feather=4)
    rgb = comp_rgb(rgb, pl)
    clear()
    # Batok: the ribbed cone, olive-sage, sunlit left, deep fluted gullies
    bt = blank(W, H)
    apex = (285, 740)
    tpts = [(70, 965), (145, 908), (212, 822), (260, 758), (278, 744), (296, 743), (314, 756), (360, 822), (425, 908), (510, 965)]
    tm = displace(poly(W, H, tpts, smooth=True), nx(), 1.5, 12)
    bt = G(bt, tm, "#8a9468", "#6f7a58", seed=nx(), density=0.97, edge=0.45, bloom=0.2, rough=1.2, feather=0.9)
    fl, th = flutes(W, H, apex[0], apex[1] - 6, 34, nx(), warp=0.25)
    amp = 0.35 + 0.65 * fbm(W, H, nx(), 18, 2)
    flank = ygrad(W, H, 748, 790)
    gul = tm * np.clip((fl - 0.6) * 3.0, 0, 1) * flank * amp
    bt = G(bt, gul, "#323b2c", "#3d3b30", seed=nx(), density=0.8, edge=0.4, rough=0.8, feather=0.7)
    left = np.clip(1.15 - xgrad(W, H, 140, 330), 0, 1)
    spur = tm * np.clip((0.28 - fl) * 4, 0, 1) * flank * left
    bt = G(bt, spur, "#f2cf90", "#e8b884", seed=nx(), density=0.75, edge=0.2, rough=0.8, feather=0.6)
    bt = G(bt, tm * np.clip(xgrad(W, H, 290, 480) * 0.9, 0, 1), "#3a4642", seed=nx(), density=0.55, edge=0.25, rough=1.5, feather=1.5)
    foot = tm * ygrad(W, H, 880, 965)
    bt = G(bt, foot, "#9a8b7c", seed=nx(), density=0.6, edge=0.1, rough=3, feather=3)
    rgb = comp_rgb(rgb, bt)
    clear()
    # the sand sea: dark volcanic grey-brown, wind ripples, jeep tracks curving towards the cones
    sea = blank(W, H)
    sm = displace(poly(W, H, [(-20, 958), (200, 938), (500, 944), (W + 20, 930), (W + 20, H + 20), (-20, H + 20)], smooth=True), nx(), 4, 30)
    sea = G(sea, sm, "#b5a093", "#9f8a80", seed=nx(), density=0.95, edge=0.2, bloom=0.4, rough=3, feather=1.2, gran=0.45)
    sea = G(sea, sm * ygrad(W, H, 960, H), "#7c6a64", "#6a5b5a", seed=nx(), density=0.6, edge=0.25, bloom=0.6, rough=8, feather=6, gran=0.5)
    sea = G(sea, sm * radial(W, H, 230, 970, 420, sy=0.3), "#f6cfa3", seed=nx(), density=0.6, edge=0.05, bloom=0.3, rough=6, feather=8)
    patches = []
    for _ in range(18):
        y = rng.uniform(1000, H); t = (y - 960) / (H - 960)
        patches.append((rng.uniform(0, W), y, rng.uniform(40, 140) * (0.5 + t), rng.uniform(6, 20) * (0.5 + t), rng.uniform(-4, 4)))
    sea = G(sea, displace(ellipses(W, H, patches), nx(), 8, 20) * sm, "#5d4f52", seed=nx(), density=0.18, edge=0.45, bloom=0.5, rough=6, feather=3)
    rip = []
    for _ in range(260):
        t = rng.random() ** 1.4
        y = 950 + (H - 950) * t
        x = rng.uniform(-60, W)
        L = (24 + 150 * t) * rng.uniform(0.6, 1.3)
        cur = rng.uniform(-1, 1) * (2 + 6 * t)
        rip.append(([(x, y), (x + L * 0.5, y + cur), (x + L, y + rng.uniform(-2, 2))], 0.7 + 2.2 * t, (0.4, 0.4)))
    ripm = strokes(W, H, rip) * sm
    sea = G(sea, ripm, "#5b4c4c", seed=nx(), density=0.35, edge=0.1, rough=1, feather=0.6)
    hl = strokes(W, H, [([(x + 1, y + 2 + it[1]) for x, y in it[0]], it[1] * 0.6, it[2]) for it in rip[::2]]) * sm
    sea = G(sea, hl, "#f3dcc4", seed=nx(), density=0.4, edge=0.1, rough=1, feather=0.6)
    tracks = []
    for off in (0, 9, 26, 33):
        tracks.append((curve([(80 + off, H + 20), (180 + off * 0.8, 1300), (300 + off * 0.5, 1120), (380 + off * 0.3, 1010), (430, 962)], 60), 2.6 - off * 0.03, (0.0, 0.6)))
    sea = G(sea, strokes(W, H, tracks) * sm, "#4f4246", seed=nx(), density=0.4, edge=0.2, rough=1.5, feather=0.8)
    rgb = comp_rgb(rgb, sea)
    clear()
    rgb = comp_rgb(rgb, mist_layer(W, H, [(940, 26, -40, 430, 0.85), (966, 18, 380, W + 40, 0.7), (1020, 12, 60, 560, 0.4)], nx, rng))
    clear()
    # foreground: corrugated savanna ridges along the bottom
    fg = ridge_art(W, H, nx, rng, [(1330, 90, 1.3, 2.4, "#8fa45e", "#5d7a44"), (1440, 70, 1.8, 0.6, "#728f4c", "#46663a")])
    rgb = comp_rgb(rgb, fg)
    clear()
    paperk = np.asarray(paper(W, H, "#ffffff", 7), np.float32) / 255
    rgb = rgb * (0.96 + 0.04 * paperk)
    prev_rgb(rgb, "bt-scene")
    rgb_save(rgb, f"{OUT}/scene.webp", quality=76)
    clear()


def ridge_art(W, H, nx, rng, layers, art=None, bottom=None):
    """Corrugated green hills (Bukit Teletubbies): rounded ridges whose flanks are fluted by radiating gullies that
    fan out from the crests, grass lit gold along the tops."""
    art = blank(W, H) if art is None else art
    bottom = H if bottom is None else bottom
    for k, (base, amp, freq, phase, c_l, c_d) in enumerate(layers):
        xs = np.arange(-8, W + 16, 4)
        ys = np.array([base - amp * (0.55 + 0.45 * math.sin(x / W * math.tau * freq + phase)) - amp * 0.22 * math.sin(x / W * math.tau * freq * 2.7 + phase * 2) for x in xs])
        pts = [(-10, bottom + 10)] + list(zip(xs.tolist(), ys.tolist())) + [(W + 10, bottom + 10)]
        m = displace(poly(W, H, pts, smooth=True), nx(), 1.5, 18)
        art = G(art, m, c_l, c_d, seed=nx(), density=0.97, edge=0.5, bloom=0.3, rough=2, feather=1)
        art = G(art, m * ygrad(W, H, base - amp, base + 60), c_d, seed=nx(), density=0.45, edge=0.1, rough=3, feather=3)
        slope = np.gradient(ys) / 4
        folds, lits = [], []
        i = 0
        while i < len(xs):
            x, y = xs[i], ys[i]
            dx = float(np.clip(slope[i] * 0.8, -0.9, 0.9))
            L = (bottom - y) * rng.uniform(0.5, 1.1)
            y0 = y + rng.uniform(2, 8)
            path = [(x, y0), (x + dx * L * 0.35, y0 + L * 0.4), (x + dx * L * 0.8 + rng.uniform(-6, 6), y0 + L)]
            folds.append((curve(path, 12), rng.uniform(2.5, 6.5), (0.05, 0.5)))
            lits.append(([(px + 3, py) for px, py in curve(path, 12)], rng.uniform(1.0, 2.2), (0.05, 0.6)))
            i += rng.randint(3, 6)
        fm = gaussian_filter(strokes(W, H, folds), 1.2) * m
        art = G(art, fm, mix_hex(c_d, "#1d3020", 0.55), seed=nx(), density=0.5, edge=0.35, rough=1.5, feather=1.2)
        lm = strokes(W, H, lits) * m * np.clip(1 - ygrad(W, H, base - amp, base + 40) * 0.8, 0, 1)
        art = G(art, lm, mix_hex(c_l, "#efe6a8", 0.5), seed=nx(), density=0.45, edge=0.1, rough=1.0, feather=0.7)
        topline = np.interp(np.arange(W), xs, ys)
        top = m * np.clip(1 - (np.arange(H)[:, None] - topline[None, :]) / 22, 0, 1)
        art = G(art, top, "#e6dd98", seed=nx(), density=0.55, edge=0.1, rough=2, feather=1.5)
        clear()
    return art


def part_ridge():
    W, H = 1200, 300
    rng = random.Random(9); nx = Seq(1100)
    art = ridge_art(W, H, nx, rng, [
        (150, 70, 2.2, 0.4, "#a7b878", "#7f9a5e"),
        (215, 70, 3.1, 2.0, "#86a35c", "#5f8247"),
        (275, 52, 4.0, 1.0, "#6c8f48", "#46693a"),
    ])
    preview(art, "bt-ridge", tone="#f2e6dc")
    save_full(art, f"{OUT}/ridge.webp", size=(900, 225), quality=80)
    clear()


def part_mist():
    W, H = 1000, 220
    rng = random.Random(5); nx = Seq(1400)
    art = mist_layer(W, H, [(110, 34, -60, W + 60, 0.8), (80, 18, 150, 700, 0.5), (140, 20, 500, W + 60, 0.55)], nx, rng, col="#ffffff")
    fade = np.clip(xgrad(W, H, 0, 120) * (1 - xgrad(W, H, W - 120, W)), 0, 1)
    art[..., 3] *= fade
    preview(art, "bt-mist", bg="#9a88a4")
    save_full(art, f"{OUT}/mist.webp", size=(700, 154), quality=78)
    clear()


def edelweiss(art, W, H, cx, cy, r, nx, rng, rot=0.0):
    """Javanese edelweiss: ~10 woolly white bracts (felted, grey-green at the base) around a cluster of tiny yellow heads."""
    pets = []
    n = rng.randint(9, 11)
    for k in range(n):
        a = rot + k / n * math.tau + rng.uniform(-0.1, 0.1)
        pets.append(petal_pts(cx + math.cos(a) * r * 0.18, cy + math.sin(a) * r * 0.18, r * rng.uniform(0.78, 0.95), r * 0.36, a, n=16))
    pm = shapes(W, H, pets)
    art = knockout(art, pm, amount=1.0, grow=1.0)
    for grp in (pets[0::2], pets[1::2]):
        gm = shapes(W, H, grp)
        art = G(art, gm, "#fbf8f0", "#eef0e4", seed=nx(), density=0.9, edge=0.9, bloom=0.3, rough=0.8, feather=0.6, gran=0.5)
        art = G(art, gm * np.clip(1 - radial(W, H, cx, cy, r * 1.0) * 1.8, 0, 1), "#c3ccb0", seed=nx(), density=0.45, edge=0.3, rough=0.8, feather=0.8)
    base = pm * radial(W, H, cx, cy, r * 0.45)
    art = G(art, base, "#b9c3a8", seed=nx(), density=0.4, edge=0.1, rough=1, feather=1)
    veins = strokes(W, H, [([(cx + math.cos(rot + k / n * math.tau) * r * 0.25, cy + math.sin(rot + k / n * math.tau) * r * 0.25),
                              (cx + math.cos(rot + k / n * math.tau) * r * 0.8, cy + math.sin(rot + k / n * math.tau) * r * 0.8)], max(0.7, r * 0.03), (0.1, 0.5)) for k in range(n)])
    art = G(art, veins * pm, "#9aa491", seed=nx(), density=0.35, edge=0, rough=0.5, feather=0.5)
    heads = [(cx + rng.gauss(0, r * 0.09), cy + rng.gauss(0, r * 0.09), r * rng.uniform(0.035, 0.06)) for _ in range(26)]
    hm = circles(W, H, heads)
    art = G(art, hm, "#d4a84a", "#9a7432", seed=nx(), density=0.95, edge=0.6, rough=0.6, feather=0.5)
    dots = circles(W, H, [(x - rr * 0.3, y - rr * 0.3, rr * 0.35) for x, y, rr in heads])
    art = G(art, dots, "#fff2b8", seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    return art


def part_edelweiss():
    W, H = 260, 260
    rng = random.Random(3); nx = Seq(1600)
    art = edelweiss(blank(W, H), W, H, 130, 130, 100, nx, rng, rot=0.2)
    preview(art, "bt-edelweiss", tone="#e8d8c6")
    save(art, f"{OUT}/edelweiss.webp", max_w=120, quality=84)
    clear()


def part_divider():
    W, H = 720, 150
    rng = random.Random(4); nx = Seq(1800)
    art = blank(W, H)
    stem = curve([(60, 92), (220, 80), (360, 74), (500, 82), (660, 98)], 80)
    st = strokes(W, H, [(stem, 4.0, (0.1, 0.1))])
    art = G(art, st, "#7d8a68", "#6a7a5e", seed=nx(), density=0.9, edge=0.4, rough=1, feather=0.6)
    lv = []
    for x0, side in [(120, -1), (170, 1), (230, -1), (470, 1), (530, -1), (590, 1)]:
        y0 = 80 + (x0 - 360) ** 2 / 9000
        a = (-0.9 if side < 0 else 0.9) + (0.0 if x0 < 360 else math.pi)
        lv.append(petal_pts(x0, y0, rng.uniform(46, 60), 8, -math.pi / 2 * side * 0.5 + (math.pi if x0 > 360 else 0) + side * 0.6, n=12))
    art = G(art, shapes(W, H, lv), "#a7b39a", "#8c9a86", seed=nx(), density=0.9, edge=0.5, rough=1, feather=0.6, gran=0.3)
    art = edelweiss(art, W, H, 360, 74, 52, nx, rng, rot=0.4)
    art = edelweiss(art, W, H, 278, 92, 30, nx, rng, rot=1.0)
    art = edelweiss(art, W, H, 446, 96, 26, nx, rng, rot=0.1)
    preview(art, "bt-divider", tone="#f2e9df")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
    clear()


def part_sarung():
    """Tengger sarung (worn as a shoulder cloak against the cold): a woven check of maroon, ochre and moss with cream lines."""
    N = 168
    bands = [(0, 30, 1), (30, 34, 3), (34, 40, 2), (40, 44, 3), (44, 82, 1), (82, 84, 4), (84, 112, 2), (112, 114, 4), (114, 140, 1),
             (140, 146, 5), (146, 150, 3), (150, 168, 2)]
    D = check_design(N, bands, 0)
    pal = ["#7e2f2a", "#7e2f2a", "#3f4a2f", "#d8b56a", "#efe2c4", "#2c2a3c"]
    rgb = ikat(D, pal, p=3, mode="double", amp=0.6, coh=2, along=10, seed=11, bleed=0.4, slub=0.35, fibre=0.08, tile=True)
    prev_rgb(rgb, "bt-sarung")
    rgb_save(rgb, f"{OUT}/sarung.webp", quality=74)


def check_design(N, bands, base):
    D = np.full((N, N), base, np.int32)
    for (a, b, k) in bands:
        D[:, a:b] = k
    for (a, b, k) in bands:
        if k in (3, 4, 5):
            D[a:b, :] = np.where(D[a:b, :] <= 2, k, D[a:b, :])
        else:
            D[a:b, :] = np.where((D[a:b, :] <= 2) & (D[a:b, :] != k), np.where((np.arange(N)[None, :] % 2) == 0, k, D[a:b, :]), D[a:b, :])
    return D


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
