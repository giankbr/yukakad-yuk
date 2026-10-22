"""Kebun Anggrek — tropical orchid glasshouse in gouache: moth orchids (Phalaenopsis), dendrobium sprays, a tessellated
blue vanda; white-painted iron glasshouse frame with morning condensation; humid green light.
Run: python3 -I kebun-anggrek.py [part ...]  parts: jungle glass phal dendro vanda sprig leaf
Assets -> public/themes/art/kebun-anggrek/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *

OUT = outdir("kebun-anggrek")
PARTS = sys.argv[1:] or ["jungle", "glass", "phal", "dendro", "vanda", "sprig", "leaf"]
LEAF, LEAF_D, LEAF_L = "#3f6b45", "#1f3d2b", "#7fa06a"
STEM = "#6b7040"


def phal(art, W, H, x, y, r, rng, nx, rot=0.0, base="#fbf7f4", base2="#f1e4ea", blush="#d76a9a", lip="#b8285f", vein=True):
    """Moth orchid face-on: dorsal + two lateral sepals, two broad round petals, three-lobed magenta lip."""
    ca, sa = math.cos(rot), math.sin(rot)
    P = lambda dx, dy: (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    sep = [deform(petal_pts(*P(0, 0), r * 1.0, r * 0.4, -math.pi / 2 + rot, n=14), rng, 1, 0.02),
           deform(petal_pts(*P(0, 0), r * 0.95, r * 0.36, math.pi / 2 + 0.62 + rot, n=14), rng, 1, 0.02),
           deform(petal_pts(*P(0, 0), r * 0.95, r * 0.36, math.pi / 2 - 0.62 + rot, n=14), rng, 1, 0.02)]
    pet = [deform(ellipse_pts(*P(-r * 0.56, -r * 0.05), r * 0.6, r * 0.52, 16, -0.25 + rot), rng, 1, 0.025),
           deform(ellipse_pts(*P(r * 0.56, -r * 0.05), r * 0.6, r * 0.52, 16, 0.25 + rot), rng, 1, 0.025)]
    ms = shapes(W, H, sep); mp = shapes(W, H, pet)
    m = np.maximum(ms, mp)
    # soft cast shadow, then opaque gouache body
    art = G(art, np.roll(np.roll(m, 4, 0), 3, 1), "#1a2e22", seed=nx(), density=0.28, edge=0.1, bloom=0, rough=2, feather=3, pad=10)
    art = GP(art, ms, base2, base, seed=nx(), rough=1.2, streak=0.2, pad=8)
    art = GP(art, mp, base, base2, seed=nx(), rough=1.2, streak=0.2, pad=8)
    # blush toward the centre + crease shading
    cen = circles(W, H, [(*P(0, r * 0.02), r * 0.5)]) * m
    art = G(art, soft(cen, r * 0.18) * m, blush, seed=nx(), density=0.38, edge=0.05, bloom=0.2, rough=1.5, pad=8)
    sh = np.clip(soft(mp, 3) - np.roll(soft(mp, 3), int(r * 0.12), 0), 0, 1) * mp
    art = G(art, sh * 1.5, "#a99aa8", seed=nx(), density=0.3, edge=0, bloom=0, rough=1, pad=6)
    if vein:
        vs = []
        for side in (-1, 1):
            for k in range(5):
                a = (math.pi if side < 0 else 0) + (k - 2) * 0.28 - side * 0.1
                vs.append((curve([P(side * r * 0.1, 0), P(side * r * 0.1 + math.cos(a) * r * 0.55 * side * side, math.sin(a) * r * 0.45)], 8), 1.0, (0.0, 0.6)))
        art = G(art, strokes(W, H, vs) * mp, blush, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, feather=0.5, pad=6)
    # rim line where petals overlap sepals
    rim = np.clip((mp - soft(mp, 1.0)) * 4, 0, 1)
    art = G(art, rim, "#b7a6b2", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    # lip: side lobes, mid lobe with tendrils, yellow callus, column
    lipm = shapes(W, H, [deform(ellipse_pts(*P(0, r * 0.36), r * 0.2, r * 0.22, 12), rng, 1, 0.04),
                         ellipse_pts(*P(-r * 0.16, r * 0.16), r * 0.14, r * 0.2, 10, 0.5 + rot), ellipse_pts(*P(r * 0.16, r * 0.16), r * 0.14, r * 0.2, 10, -0.5 + rot)])
    art = GP(art, lipm, lip, mix(lip, "#6e1236", 0.4), seed=nx(), rough=0.8, streak=0.5, pad=6)
    cal = circles(W, H, [(*P(0, r * 0.14), r * 0.08)])
    art = GP(art, cal, "#f4c84a", "#e59a2c", seed=nx(), rough=0.5, pad=6)
    dots = circles(W, H, [(*P(rng.uniform(-r * .12, r * .12), rng.uniform(r * .08, r * .22)), r * 0.018) for _ in range(9)])
    art = GP(art, dots, "#9a1d40", seed=nx(), rough=0.3, pad=4)
    col = shapes(W, H, [deform(ellipse_pts(*P(0, -r * 0.04), r * 0.07, r * 0.12, 10), rng, 0, 0)])
    art = GP(art, col, "#fffaf2", "#efe6da", seed=nx(), rough=0.4, pad=4)
    return art, m


def bud(art, W, H, x, y, s, ang, nx, col="#e9efd2", col2="#c9d79c"):
    m = shapes(W, H, [petal_pts(x, y, s * 1.5, s * 0.62, ang, n=12)])
    art = GP(art, m, col, col2, seed=nx(), rough=0.8, streak=0.4, pad=6)
    hi = np.clip(soft(m, 2) - np.roll(np.roll(soft(m, 2), 3, 0), 3, 1), 0, 1) * m * 2
    art = G(art, hi, "#ffffff", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, pad=4)
    return art


def stem(art, W, H, pts, wd, nx):
    m = strokes(W, H, [(pts, wd, (0.0, 0.4))])
    art = GP(art, m, STEM, "#4a5230", seed=nx(), rough=0.6, streak=0.6, pad=6)
    return art


def broad_leaf(art, W, H, x, y, L, Wd, ang, rng, nx, cup=0.0):
    m = shape_mask(W, H, deform(petal_pts(x, y, L, Wd, ang, n=16, cup=cup), rng, 2, 0.02))
    art = G(art, np.roll(np.roll(m, 6, 0), 4, 1), "#0f2318", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=2, feather=4)
    art = GP(art, m, LEAF, LEAF_D, seed=nx(), rough=1.5, streak=1.0)
    # glossy highlight band along the upper half + midrib
    half = shape_mask(W, H, petal_pts(x, y, L * 0.92, Wd * 0.45, ang - 0.05, n=14)) * m
    art = G(art, soft(half, 4) * m, LEAF_L, seed=nx(), density=0.45, edge=0.05, bloom=0.3, rough=2)
    rib = strokes(W, H, [([(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in np.linspace(0.04, 0.9, 12)], 2.4, (0.05, 0.5))]) * m
    art = G(art, rib, LEAF_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    sheen = strokes(W, H, [([(x + math.cos(ang + 0.08) * L * t, y + math.sin(ang + 0.08) * L * t) for t in np.linspace(0.15, 0.6, 8)], Wd * 0.18, (0.3, 0.5))]) * m
    art = GP(art, sheen, "#cfe3bf", seed=nx(), rough=1, streak=0.3, density=0.55)
    return art


def root(art, W, H, pts, wd, nx):
    m = strokes(W, H, [(pts, wd, (0.0, 0.1))])
    art = GP(art, m, "#c9cdbd", "#9fa893", seed=nx(), rough=0.8, streak=0.5, pad=6)
    tip = strokes(W, H, [(pts[-6:], wd * 0.9, (0.0, 0.5))])
    return GP(art, tip, "#7fa860", seed=nx(), rough=0.5, pad=6)


def dendro_flower(art, W, H, x, y, r, rng, nx, rot, tip="#f6eef6", base="#a64d9c", lipc="#6d1f63"):
    polys = [petal_pts(x, y, r, r * (0.3 if k % 2 == 0 else 0.36), rot + k * math.tau / 5 - math.pi / 2, n=12) for k in range(5)]
    m = shapes(W, H, polys)
    art = G(art, np.roll(np.roll(m, 3, 0), 2, 1), "#1a2e22", seed=nx(), density=0.25, edge=0.1, bloom=0, rough=1, feather=2, pad=8)
    art = GP(art, m, tip, mix(tip, base, 0.25), seed=nx(), rough=0.8, streak=0.5, pad=6)
    tips = m * np.clip(1 - soft(circles(W, H, [(x, y, r * 0.62)]), r * 0.15) * 1.3, 0, 1)
    art = G(art, tips, base, seed=nx(), density=0.7, edge=0.2, bloom=0.2, rough=1.2, pad=6)
    lipm = shapes(W, H, [deform(ellipse_pts(x + math.cos(rot + math.pi / 2) * r * 0.25, y + math.sin(rot + math.pi / 2) * r * 0.25, r * 0.22, r * 0.3, 10, rot), rng, 1, 0.05)])
    art = GP(art, lipm, lipc, "#4a0f45", seed=nx(), rough=0.5, pad=4)
    art = GP(art, circles(W, H, [(x, y, r * 0.08)]), "#f7e7a0", seed=nx(), rough=0.3, pad=4)
    return art


def vanda_flower(art, W, H, x, y, r, rng, nx, rot=0.0, col="#7c7fd6", net="#3b3a9a"):
    """Vanda: five broad rounded petals, each painted separately (lighter rim, darker heart) with a fine tessellated net."""
    order = [0, 2, 4, 1, 3]
    allm = np.zeros((H, W), np.float32)
    for k in order:
        a = rot + k * math.tau / 5 - math.pi / 2
        px, py = x + math.cos(a) * r * 0.56, y + math.sin(a) * r * 0.56
        pm = shapes(W, H, [deform(ellipse_pts(px, py, r * 0.5, r * 0.4, 14, a), rng, 1, 0.03)])
        art = G(art, np.roll(np.roll(pm, 3, 0), 2, 1), "#1a2e22", seed=nx(), density=0.22, edge=0.1, bloom=0, rough=1, feather=2.5, pad=8)
        c = mix(col, "#ffffff", rng.uniform(0.2, 0.4))
        art = GP(art, pm, c, mix(col, "#ffffff", 0.55), seed=nx(), rough=1, streak=0.2, pad=6)
        b = bbox(pm, 4)
        y0, y1, x0, x1 = b
        hh, ww = y1 - y0, x1 - x0
        cell = r * 0.1
        pts = [(rng.uniform(0, ww), rng.uniform(0, hh)) for _ in range(int(ww * hh / cell ** 2))]
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        d1 = np.full((hh, ww), 1e9, np.float32); d2 = np.full((hh, ww), 1e9, np.float32)
        for qx, qy in pts:
            d = (xx - qx) ** 2 + (yy - qy) ** 2
            d2 = np.where(d < d1, d1, np.minimum(d2, d)); d1 = np.minimum(d1, d)
        edge = np.clip(1 - (np.sqrt(d2) - np.sqrt(d1)) / 1.6, 0, 1)
        netm = np.zeros((H, W), np.float32); netm[y0:y1, x0:x1] = edge
        heart = np.clip(1 - np.hypot(np.arange(W)[None, :] - x, np.arange(H)[:, None] - y) / (r * 1.05), 0, 1)
        art = G(art, netm * pm * (0.35 + 0.65 * heart), net, seed=nx(), density=0.5, edge=0, bloom=0.1, rough=0.4, feather=0.4, pad=6)
        art = G(art, pm * heart ** 1.5, net, seed=nx(), density=0.3, edge=0, bloom=0.2, rough=1, pad=6)
        rim = np.clip((pm - soft(pm, 1.2)) * 4, 0, 1)
        art = G(art, rim, net, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.4, pad=6)
        np.maximum(allm, pm, out=allm)
    lipm = shapes(W, H, [deform(ellipse_pts(x, y + r * 0.16, r * 0.09, r * 0.15, 10), rng, 1, 0.05)])
    art = GP(art, lipm, "#5a4aa8", "#3b2f86", seed=nx(), rough=0.4, pad=4)
    art = GP(art, circles(W, H, [(x, y - r * 0.02, r * 0.07)]), "#f4f0ff", seed=nx(), rough=0.3, pad=4)
    return art


if "jungle" in PARTS:
    # humid green light behind the glass: out-of-focus foliage, light shafts, mist
    W, H = 480, 800
    rng = random.Random(3); nx = Seq(300)
    art = painted_sky(W, H, [(0, "#cfe3c6"), (0.25, "#9cc39a"), (0.6, "#4f8a5e"), (1, "#24513c")], seed=5, streak=0.4)
    for k in range(26):
        x = rng.uniform(-60, W + 60); y = rng.uniform(80, H + 40); L = rng.uniform(120, 260)
        a = rng.uniform(-math.pi, 0)
        m = shape_mask(W, H, deform(petal_pts(x, y, L, L * rng.uniform(0.32, 0.48), a, n=16, cup=rng.uniform(-0.3, 0.3)), rng, 2, 0.03))
        col = rng.choice(["#2f6a48", "#3f7d52", "#5f9a62", "#1f4a34", "#7fb07a"])
        art = G(art, soft(m, rng.uniform(7, 16)), col, mix(col, "#1a3a2a", 0.3), seed=nx(), density=0.6, edge=0.05, bloom=0.3, rough=4)
    bok = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(6, 18)) for _ in range(22)])
    art = G(art, soft(bok, 2.5), "#f6fbe2", seed=nx(), density=0.4, edge=0.3, bloom=0, rough=1)
    shafts = strokes(W, H, [([(x, -20), (x - 140, H)], rng.uniform(30, 60), None) for x in (140, 270, 400, 520)])
    art = G(art, soft(shafts, 22) * 0.9, "#f4fbe4", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=4)
    mist = np.clip(1 - np.linspace(0, 1, H)[:, None] * 1.3, 0, 1) * np.ones((1, W))
    art = G(art, (mist * fbm(W, H, 33, 90, 3)).astype(np.float32), "#eef6e8", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=3)
    art[..., 3] = 1
    preview(art, "ka-jungle", bg="#ffffff")
    save_rgb(art, f"{OUT}/jungle.webp", quality=70)
    clear()

if "glass" in PARTS:
    # Victorian glasshouse window: arched iron frame painted cream-white, condensation on the panes
    W, H = 600, 1000
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    cx, top, rad = 300, 40, 280
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    inside = ((((xx - cx) ** 2 + (yy - (top + rad)) ** 2) < rad ** 2) | ((yy >= top + rad) & (np.abs(xx - cx) < rad))).astype(np.float32)
    # fog on the panes: denser low and near the edges, cleared streaks where droplets ran
    fog = fbm(W, H, 71, 60, 4) * 0.6 + np.clip((yy / H - 0.35) * 1.2, 0, 1) * 0.5
    runs = np.zeros((H, W), np.float32)
    drips = []
    for k in range(70):
        x = rng.uniform(30, W - 30); y0 = rng.uniform(60, 700); L = rng.uniform(40, 220)
        drips.append((curve([(x, y0), (x + rng.uniform(-3, 3), y0 + L * 0.5), (x + rng.uniform(-4, 4), y0 + L)], 14), rng.uniform(2.5, 5), (0.0, 0.0)))
    runs = strokes(W, H, drips)
    fogm = np.clip(fog - 0.25, 0, 1) * inside * (1 - runs * 0.9)
    fogl = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f2f7ef"), np.float32), (fogm * 0.55)[..., None]], -1)
    art = over(art, fogl)
    # droplets: tiny lenses (dark rim below, bright spec top-left), more in the fog
    drops = []
    for k in range(1100):
        x = rng.uniform(0, W); y = rng.uniform(0, H)
        if inside[int(y), int(x)] < 0.5:
            continue
        if fog[int(y), int(x)] < 0.42 and rng.random() < 0.6:
            continue
        drops.append((x, y, rng.choice([1.2, 1.6, 2.0, 2.6, 3.2, 4.2]) if rng.random() < 0.9 else rng.uniform(5, 7)))
    dm = circles(W, H, drops)
    dk = circles(W, H, [(x + r * 0.15, y + r * 0.3, r * 0.85) for x, y, r in drops]) * dm
    hi = circles(W, H, [(x - r * 0.35, y - r * 0.35, max(0.6, r * 0.3)) for x, y, r in drops])
    art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#ffffff"), np.float32), (dm * 0.35)[..., None]], -1))
    art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#264a36"), np.float32), (np.clip(dm - dk * 0.6, 0, 1) * 0.0 + dk * 0.32)[..., None]], -1))
    art = over(art, np.concatenate([np.ones((H, W, 3), np.float32), (hi * 0.95)[..., None]], -1))
    clear()
    # iron frame
    bars = []
    for x in (cx - rad, cx + rad):
        bars.append(([(x, top + rad), (x, H)], 26, None))
    for x in (cx - rad * 0.5, cx, cx + rad * 0.5):
        bars.append(([(x, top + rad * (1 - math.sqrt(1 - ((x - cx) / rad) ** 2)) + 6), (x, H)], 12, None))
    for y in (top + rad + 150, top + rad + 420):
        bars.append(([(cx - rad, y), (cx + rad, y)], 12, None))
    arc = arc_pts(cx, top + rad, rad, math.pi, math.tau, 60)
    bars.append((arc, 26, None))
    arc2 = arc_pts(cx, top + rad, rad * 0.42, math.pi, math.tau, 40)
    bars.append((arc2, 10, None))
    for k in range(1, 8):
        a = math.pi + k * math.pi / 8
        bars.append(([(cx + math.cos(a) * rad * 0.42, top + rad + math.sin(a) * rad * 0.42), (cx + math.cos(a) * rad, top + rad + math.sin(a) * rad)], 8, None))
    bars.append(([(cx - rad, top + rad), (cx + rad, top + rad)], 12, None))
    frame = strokes(W, H, bars, cap=False)
    # decorative scrolls in the arch spandrels and a rosette hub
    scr = []
    for side in (-1, 1):
        scr.append((spiral_pts(cx + side * rad * 0.7, top + rad - 30, 26, 4, math.pi / 2, 1.3, 40, side), 5, (0.0, 0.6)))
    hub = ring_m(W, H, cx, top + rad, 40, 9)
    frame = np.maximum.reduce([frame, strokes(W, H, scr), hub])
    art = G(art, np.roll(np.roll(frame, 7, 0), 5, 1), "#10251a", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=2, feather=4)
    art = GP(art, frame, "#eef1e6", "#d8dfcf", seed=nx(), rough=1.2, streak=0.8)
    shade = np.clip(frame - np.roll(np.roll(frame, -3, 0), -3, 1), 0, 1)
    art = G(art, soft(shade, 1.2) * frame, "#8f9c8c", seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    chips = frame * np.clip((fbm(W, H, 77, 7, 2) - 0.72) * 5, 0, 1)
    art = G(art, chips, "#7d6a4c", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    rivets = circles(W, H, [(x, y, 3) for x in (cx - rad, cx - rad * 0.5, cx, cx + rad * 0.5, cx + rad) for y in (top + rad + 150, top + rad + 420)])
    art = GP(art, rivets, "#c8cfc0", seed=nx(), rough=0.3)
    preview(art, "ka-glass", bg="#4f8a5e")
    save_full(art, f"{OUT}/glass.webp", size=(480, 800), quality=70)
    clear()

if "phal" in PARTS:
    # hanging moth-orchid spray: two leaves, aerial roots, an arching stem with five blooms and two buds
    W, H = 640, 620
    rng = random.Random(17); nx = Seq(1700)
    art = blank(W, H)
    art = root(art, W, H, curve([(70, 120), (50, 200), (80, 280), (60, 360)], 30), 7, nx)
    art = root(art, W, H, curve([(110, 120), (140, 190), (120, 260)], 24), 6, nx)
    art = broad_leaf(art, W, H, 90, 110, 230, 66, -0.2, rng, nx, cup=0.15)
    art = broad_leaf(art, W, H, 80, 130, 190, 56, 0.55, rng, nx, cup=-0.1)
    sp = curve([(120, 100), (250, 40), (390, 70), (500, 170), (560, 300), (580, 420)], 80)
    art = stem(art, W, H, sp, 6, nx)
    marks = [(0.3, 70), (0.45, 74), (0.6, 70), (0.73, 62), (0.84, 52)]
    for t, r in marks:
        x, y = sp[int(t * (len(sp) - 1))]
        art, _ = phal(art, W, H, x - 10, y + r * 0.55, r, rng, nx, rot=rng.uniform(-0.25, 0.25))
        clear()
    for t, s in [(0.93, 18), (0.99, 13)]:
        x, y = sp[int(t * (len(sp) - 1))]
        art = bud(art, W, H, x, y, s, math.pi / 2 + 0.2, nx)
    preview(art, "ka-phal", bg="#4f8a5e")
    save(art, f"{OUT}/phal.webp", max_w=480, quality=80)
    clear()

if "dendro" in PARTS:
    # dendrobium spray hanging down from the right: cane with strap leaves and many small purple-tipped flowers
    W, H = 420, 640
    rng = random.Random(23); nx = Seq(2300)
    art = blank(W, H)
    cane = curve([(380, 0), (360, 120), (300, 260), (260, 420), (250, 600)], 60)
    art = stem(art, W, H, cane, 7, nx)
    for (x, y, L, a) in [(370, 60, 150, 2.6), (350, 140, 130, 0.5), (320, 210, 120, 2.8)]:
        art = broad_leaf(art, W, H, x, y, L, 26, a, rng, nx)
    for i in range(16):
        t = 0.28 + i / 16 * 0.7
        x, y = cane[int(t * (len(cane) - 1))]
        side = -1 if i % 2 else 1
        ped = curve([(x, y), (x + side * 26, y + 8), (x + side * 44, y + 20)], 8)
        art = G(art, strokes(W, H, [(ped, 2.2, None)]), "#6b7040", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5, feather=0.5)
        art = dendro_flower(art, W, H, ped[-1][0] + rng.uniform(-6, 6), ped[-1][1] + rng.uniform(-4, 4), rng.uniform(24, 36) * (1.05 - t * 0.3), rng, nx, rng.uniform(-1.0, 1.0))
        if i % 4 == 0:
            clear()
    preview(art, "ka-dendro", bg="#4f8a5e")
    save(art, f"{OUT}/dendro.webp", max_w=320, quality=80)
    clear()

if "vanda" in PARTS:
    W, H = 520, 380
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    for (x, y, L, a) in [(260, 360, 230, -2.6), (260, 360, 220, -0.5), (260, 360, 170, -1.9), (260, 360, 160, -1.2)]:
        art = broad_leaf(art, W, H, x, y, L, 22, a, rng, nx)
    for (x, y, r, rot) in [(180, 170, 84, -0.2), (330, 150, 92, 0.15), (260, 270, 70, 0.05)]:
        art = vanda_flower(art, W, H, x, y, r, rng, nx, rot)
        clear()
    preview(art, "ka-vanda", bg="#f2efe6")
    save(art, f"{OUT}/vanda.webp", max_w=380, quality=82)
    clear()

if "sprig" in PARTS:
    # small single moth orchid with a bud: divider centre / node / sent art
    W, H = 300, 200
    rng = random.Random(41); nx = Seq(4100)
    art = blank(W, H)
    sp = curve([(20, 120), (90, 70), (180, 80), (270, 130)], 40)
    art = stem(art, W, H, sp, 4, nx)
    art = bud(art, W, H, 262, 132, 12, 0.6, nx)
    art = bud(art, W, H, 40, 110, 10, 3.6, nx)
    art, _ = phal(art, W, H, 150, 96, 62, rng, nx, rot=0.05)
    preview(art, "ka-sprig", bg="#f2efe6")
    save(art, f"{OUT}/sprig.webp", max_w=200, quality=84)
    clear()

if "leaf" in PARTS:
    # monstera-ish shadow leaf for the bands (soft, low contrast)
    W, H = 420, 420
    rng = random.Random(51); nx = Seq(5100)
    art = blank(W, H)
    m = shape_mask(W, H, deform(ellipse_pts(210, 210, 180, 160, 14), rng, 2, 0.04))
    cuts = strokes(W, H, [([(210 + math.cos(a) * 60, 210 + math.sin(a) * 55), (210 + math.cos(a) * 200, 210 + math.sin(a) * 180)], 12, (0.4, 0.0)) for a in np.linspace(-2.6, 2.6, 11) if abs(a) > 0.3])
    holes = circles(W, H, [(210 + math.cos(a) * 110, 210 + math.sin(a) * 100, 9) for a in np.linspace(-2.3, 2.3, 7)])
    m = np.clip(m - cuts - holes - strokes(W, H, [([(210, 210), (420, 210)], 8, None)]), 0, 1)
    art = GP(art, m, "#1f4a34", "#2f6a48", seed=nx(), rough=2, streak=0.6)
    art = G(art, strokes(W, H, [([(30, 215), (390, 205)], 5, (0.1, 0.4))]) * m, "#163626", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    preview(art, "ka-leaf", bg="#f2efe6")
    save(art, f"{OUT}/leaf.webp", max_w=260, quality=80)

kb(OUT)
