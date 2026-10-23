"""Tropis Gelap — dark moody tropical: monstera, banana and palm leaves in deep greens with bird-of-paradise and
anthurium, lit by one warm shaft of light from the upper right (opaque gouache on near-black).
Run: python3 -I tropis-gelap.py [part ...]  parts: jungle corner bloom leaf divider
Assets -> public/themes/art/tropis-gelap/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o4_lib import *

OUT = outdir("tropis-gelap")
PARTS = sys.argv[1:] or ["jungle", "corner", "bloom", "leaf", "divider"]
BG = "#0b100d"
G1, G2, G3, G4 = "#0f2a1e", "#18402c", "#285a3a", "#4f8a5a"   # deep -> lit
RIM = "#a9c98a"
ORANGE, ORANGE_D, BLUE = "#ef8a2c", "#c4521e", "#3d4fa8"
RED, RED_D = "#c8202a", "#7a0e18"
LIGHT = (0.75, -0.66)  # light comes from upper right


def lit_paint(art, W, H, m, nx, base=(G2, G1), lit=G4, rim=RIM, amt=0.75, rib=None, ribcol=None, depth=1.0):
    """Opaque leaf: dark gouache body, brushed light toward the upper right, dry-brush hot spots, a rim on the lit
    edge and a rib. depth 0 = far (sinks into the dark), 1 = front. Computed inside the mask bbox only."""
    b = jw.bbox(m, 6)
    if b is None:
        return art
    y0, y1, x0, x1 = b
    mm = np.ascontiguousarray(m[y0:y1, x0:x1])
    h, w = mm.shape
    fade = (1 - depth) * 0.62
    b0, b1 = mix(base[0], BG, fade), mix(base[1], BG, fade)
    sub = art[y0:y1, x0:x1].copy()
    sub = over(sub, gouache_paint(mm, b0, b1, seed=nx(), rough=1.6, streak=0.5))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    proj = (xx / max(1, w)) * LIGHT[0] + (yy / max(1, h)) * LIGHT[1]
    proj = (proj - proj.min()) / max(1e-6, np.ptp(proj))
    sheen = np.clip((proj - 0.35) * 1.6, 0, 1) * (0.55 + 0.45 * fbm(w, h, nx(), 40, 3))
    sub = over(sub, flat(mm * np.clip(fbm(w, h, nx(), 55, 3) - 0.5, 0, 1) * 1.2 * (1 - sheen), "#06140d", 0.8))
    k = amt * (0.25 + 0.75 * depth)
    sub = over(sub, brushy(mm * sheen * k * 0.9, mix(lit, BG, fade * 0.8), mix(G3, BG, fade), nx()))
    hot = mm * np.clip((proj - 0.62) * 2.6, 0, 1) * amt * depth
    if depth > 0.4:
        sub = over(sub, brushy(hot * 0.85, "#9cc47a", "#cfe0a0", nx(), dry=True))
    dx, dy = int(round(-LIGHT[0] * 3)), int(round(-LIGHT[1] * 3))
    rimm = np.clip(mm - np.roll(np.roll(mm, dy, 0), dx, 1), 0, 1) * np.clip(proj * 1.4 - 0.2, 0, 1)
    sub = over(sub, flat(rimm, rim, 0.75 * (0.2 + 0.8 * depth)))
    out = art.copy()
    out[y0:y1, x0:x1] = sub
    art = out
    if rib is not None:
        rm = strokes(W, H, [(curve(rib, 12), 3.0, (0.02, 0.7))]) * m
        art = OV(art, rm, lambda q: gouache_paint(q, mix(ribcol or "#7fa874", BG, fade), seed=nx(), rough=0.6, density=0.55 * (0.4 + 0.6 * depth)))
    return art


def brushy(q, col, col2, seed, dry=False):
    """Semi-opaque brushed colour whose alpha follows q (soft tonal modelling with streaks / dry-brush breaks)."""
    h, w = q.shape
    st = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.6, 4.0))
    st = (st - st.mean()) / (st.std() + 1e-6)
    a = q * np.clip(0.85 + st * 0.18, 0, 1)
    if dry:
        a *= np.clip((fbm(w, h, seed + 3, 9, 2) - 0.32) * 3, 0, 1)
    t = fbm(w, h, seed + 5, 60, 3)[..., None]
    rgb = col3(col) * (1 - t) + col3(col2) * t
    return rgba(rgb * (1 + st[..., None] * 0.03), a)


def monst(art, W, H, cx, cy, L, ang, rng, nx, **k):
    m, rib = monstera(W, H, cx, cy, L, ang, rng)
    art = soft(art, W, H, m, nx)
    return lit_paint(art, W, H, m, nx, rib=rib, **k)


def soft(art, W, H, m, nx, dist=10, strength=0.55):
    """cast shadow of a leaf onto what is below (down-left, away from the light)."""
    sh = np.roll(np.roll(gaussian_filter(m, 6), int(dist * 0.9), 0), -int(dist * 0.7), 1)
    return OV(art, sh * strength, lambda q: flat(q, "#030605", 1.0), pad=30)


def banana_leaf(art, W, H, pts, width, rng, nx, **k):
    poly = blade(W, H, pts, width)
    m = shape_mask(W, H, poly)
    cuts = []
    for j in range(3, len(pts) - 2, 2):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for side in (-1, 1):
            if rng.random() < 0.5:
                aa = ang + side * 1.15
                cuts.append(([(pts[j][0] + math.cos(aa) * width * .2, pts[j][1] + math.sin(aa) * width * .2),
                              (pts[j][0] + math.cos(aa) * width * 1.4, pts[j][1] + math.sin(aa) * width * 1.4)], 2.2, None))
    if cuts:
        m = np.clip(m - strokes(W, H, cuts) * 1.3, 0, 1)
    art = soft(art, W, H, m, nx)
    art = lit_paint(art, W, H, m, nx, rib=pts[1:-1], ribcol="#8fb07a", **k)
    veins = []
    for j in range(2, len(pts) - 2):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for side in (-1, 1):
            aa = ang + side * 1.15
            veins.append(([pts[j], (pts[j][0] + math.cos(aa) * width * .95, pts[j][1] + math.sin(aa) * width * .95)], 0.9, (0.1, 0.6)))
    return OV(art, strokes(W, H, veins) * m, lambda q: flat(q, G1, 0.45))


def palm_frond(art, W, H, base, tip, bend, rng, nx, depth=1.0):
    """Areca-style frond: arching rachis with many narrow leaflets."""
    mid = ((base[0] + tip[0]) / 2 + bend[0], (base[1] + tip[1]) / 2 + bend[1])
    rach = curve([base, mid, tip], 40)
    items = [(rach, 3.2, (0.02, 0.5))]
    Ltot = sum(math.dist(rach[i], rach[i + 1]) for i in range(len(rach) - 1))
    for j in range(2, len(rach) - 1):
        px, py = rach[j]
        a, b = rach[j - 1], rach[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        t = j / len(rach)
        ll = Ltot * 0.28 * math.sin(math.pi * min(1, t * 1.1 + 0.08)) + 6
        for side in (-1, 1):
            aa = ang + side * (0.55 + 0.15 * rng.random())
            e = (px + math.cos(aa) * ll, py + math.sin(aa) * ll + ll * 0.25)
            items.append((curve([(px, py), ((px + e[0]) / 2, (py + e[1]) / 2 - ll * 0.05), e], 8), 3.4 + 2 * (1 - t), (0.05, 0.7)))
    m = strokes(W, H, items)
    art = soft(art, W, H, m, nx, 8, 0.45)
    return lit_paint(art, W, H, m, nx, base=(G3, G2), amt=0.6, depth=depth)


def bird_of_paradise(art, W, H, x, y, s, ang, rng, nx):
    """Strelitzia: green-purple beak (spathe), orange sepals fanning up, blue tongue."""
    c, sn = math.cos(ang), math.sin(ang)
    def T(px, py):
        return (x + px * c - py * sn, y + px * sn + py * c)
    stem = strokes(W, H, [([T(-s * 0.2, s * 0.05), T(-s * 0.1, s * 2.6)], s * 0.09, None)])
    art = lit_paint(art, W, H, stem, nx, base=(G3, G2), amt=0.5)
    beak = shape_mask(W, H, [T(-s * 0.3, -s * 0.02), T(s * 0.4, -s * 0.12), T(s * 1.25, -s * 0.03), T(s * 0.5, s * 0.12), T(-s * 0.25, s * 0.14)])
    art = GP(art, beak, "#2f5a3e", "#3a2a40", seed=nx(), rough=1.0, streak=0.6)
    art = OV(art, np.clip(beak - np.roll(beak, 3, 0), 0, 1), lambda q: flat(q, "#c45a3a", 0.8))
    sep = []
    for k, (a, L, wd) in enumerate([(-1.25, 1.25, 0.15), (-1.0, 1.4, 0.17), (-0.72, 1.3, 0.16), (-0.45, 1.05, 0.13)]):
        a += rng.uniform(-0.05, 0.05)
        b0 = T(s * 0.15, -s * 0.08)
        tip = (b0[0] + math.cos(a + ang) * s * L, b0[1] + math.sin(a + ang) * s * L)
        sep.append(petal_pts(b0[0], b0[1], s * L, s * wd, a + ang, n=12))
    sm = shapes(W, H, sep)
    art = GP(art, sm, ORANGE, "#f6b24a", seed=nx(), rough=1.0, streak=0.6)
    art = OV(art, sm * np.clip(1 - ramp_x(H, W, x - s * 0.2, x + s * 1.2), 0, 1) * 0.0 + edge_ring(sm, 1.6) * 0.55, lambda q: flat(q, ORANGE_D, 1))
    tongue = shapes(W, H, [petal_pts(*T(s * 0.25, -s * 0.12), s * 0.95, s * 0.07, -0.65 + ang, n=10)])
    art = GP(art, tongue, BLUE, "#5a6fd0", seed=nx(), rough=0.8)
    return art


def anthurium(art, W, H, x, y, s, ang, rng, nx, stem=None):
    """Glossy heart spathe with a cream-yellow spadix; red lacquer with one bright highlight. stem = (dx, dy) end."""
    if stem:
        sm_ = strokes(W, H, [(curve([(x, y - s * 0.1), (x + stem[0] * 0.4 + s * 0.3, y + stem[1] * 0.5), (x + stem[0], y + stem[1])], 16), s * 0.07, None)])
        art = lit_paint(art, W, H, sm_, nx, base=(G3, G2), amt=0.5)
    pts = []
    for i in range(41):
        t = i / 40 * math.tau
        hx = 16 * math.sin(t) ** 3
        hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        hy = hy * 1.45 if hy > 0 else hy * 0.8   # long pointed tip downwards, shallow lobes
        pts.append((hx / 17 * s * 0.95, hy / 17 * s))
    pts = rotp([(x + px, y + py) for px, py in pts], x, y, ang)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.03))
    art = soft(art, W, H, m, nx, 8, 0.5)
    art = GP(art, m, RED, RED_D, seed=nx(), rough=1.0, streak=0.5)
    hl = shapes(W, H, [petal_pts(x + s * 0.2, y - s * 0.3, s * 0.45, s * 0.09, -0.9 + ang, n=10)])
    art = OV(art, gaussian_filter(hl, 1.5) * m, lambda q: flat(q, "#ffb7a2", 0.55))
    art = OV(art, edge_ring(m, 1.5) * 0.6, lambda q: flat(q, "#4a0610", 1))
    vein = []
    for d in (-1, 1):
        for k in range(3):
            r0 = s * (0.25 + k * 0.18)
            vein.append((rotp(curve([(x, y - s * 0.05), (x + d * r0 * 0.9, y + s * 0.15 + k * s * 0.08), (x + d * r0 * 0.3, y + s * (0.8 + k * 0.12))], 14), x, y, ang), 1.1, (0.1, 0.4)))
    art = OV(art, strokes(W, H, vein) * m, lambda q: flat(q, "#6a0a14", 0.6))
    sp = strokes(W, H, [(rotp(curve([(x, y - s * 0.38), (x + s * 0.12, y - s * 0.75), (x + s * 0.34, y - s * 1.0)], 12), x, y, ang), s * 0.13, (0.0, 0.7))])
    shade = m * np.clip(1 - ramp_x(H, W, x - s, x + s * 0.6), 0, 1) * ramp_y(H, W, y - s * 0.4, y + s * 1.3)
    art = OV(art, shade * 0.7, lambda q: flat(q, "#3a0410", 1))
    art = GP(art, sp, "#f2dc8a", "#d9b85a", seed=nx(), rough=0.6)
    return art


def jungle():
    """Opaque cover painting: a wall of tropical leaves around a dark clearing, one warm shaft of light from the
    upper right. Back leaves sink into the dark, front leaves catch the light."""
    W, H = 720, 1400
    rng = random.Random(23); nx = Seq(400)
    art = painted_sky(W, H, [(0, "#0e1712"), (0.45, "#0a110d"), (1, "#070b09")], seed=5, streak=0.4)
    beam = shapes(W, H, [[(W * 1.05, -40), (W * 1.2, 60), (W * 0.25, H * 0.82), (W * 0.02, H * 0.7)]], smooth=False)
    art = OV(art, gaussian_filter(beam, 60) * 0.24, lambda q: flat(q, "#c9b57a", 1.0), pad=0)
    # far layer: dim silhouettes all round, a few behind the clearing
    for (cx, cy, L, a) in [(-40, 160, 300, -0.2), (760, 240, 280, math.pi + 0.3), (-30, 640, 260, 0.1), (750, 760, 300, math.pi - 0.1),
                           (200, 1420, 300, -1.3), (560, 1440, 280, -1.9), (360, -40, 240, 1.4)]:
        art = monst(art, W, H, cx, cy, L, a, rng, nx, depth=0.15)
    for (b0, t, bd) in [((-30, 470), (330, 330), (20, 20)), ((750, 520), (420, 400), (0, 30)), ((-20, 1080), (300, 1000), (30, -40)), ((740, 1130), (430, 1060), (0, -40))]:
        art = palm_frond(art, W, H, b0, t, bd, rng, nx, depth=0.3)
    clear()
    # mid layer
    art = banana_leaf(art, W, H, curve([(-40, 330), (140, 250), (330, 230)], 22), 58, rng, nx, depth=0.55)
    art = banana_leaf(art, W, H, curve([(760, 140), (600, 170), (420, 110)], 22), 52, rng, nx, depth=0.6)
    art = banana_leaf(art, W, H, curve([(760, 1010), (600, 1060), (440, 1180)], 22), 56, rng, nx, depth=0.55)
    art = monst(art, W, H, -60, 930, 300, -0.25, rng, nx, depth=0.6)
    art = monst(art, W, H, 780, 420, 280, math.pi + 0.15, rng, nx, depth=0.6)
    art = palm_frond(art, W, H, (380, -20), (120, 140), (-10, 40), rng, nx, depth=0.55)
    clear()
    # front layer: lit, heavy at top-left and bottom-right corners
    art = monst(art, W, H, -70, 40, 360, 0.35, rng, nx, depth=1.0)
    art = monst(art, W, H, 790, -10, 300, math.pi - 0.6, rng, nx, depth=0.95)
    art = banana_leaf(art, W, H, curve([(-40, 1240), (180, 1140), (420, 1150)], 24), 66, rng, nx, depth=0.9)
    art = monst(art, W, H, 790, 1290, 380, math.pi + 0.45, rng, nx, depth=1.0)
    art = monst(art, W, H, -60, 1400, 330, -0.75, rng, nx, depth=0.95)
    clear()
    art = bird_of_paradise(art, W, H, 560, 1090, 92, -0.2, rng, nx)
    art = bird_of_paradise(art, W, H, 110, 210, 74, 0.35, rng, nx)
    art = anthurium(art, W, H, 600, 270, 46, -0.4, rng, nx, stem=(70, 120))
    art = anthurium(art, W, H, 175, 1180, 52, 0.3, rng, nx, stem=(-60, 150))
    art = anthurium(art, W, H, 96, 1060, 36, -0.2, rng, nx, stem=(-40, 100))
    # vignette toward the edges, keeps the clearing deep
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.5) / (H * 0.62)) ** 2, 0, 1) ** 1.6 * 0.35
    art = OV(art, v.astype(np.float32), lambda q: flat(q, "#020403", 1.0), pad=0)
    preview(art, "tg-jungle", bg=BG)
    save_rgb(art, f"{OUT}/jungle.webp", quality=80)


def corner():
    """Section corner cluster: monstera + palm + one anthurium, transparent."""
    W, H = 440, 420
    rng = random.Random(7); nx = Seq(900)
    art = blank(W, H)
    art = palm_frond(art, W, H, (-20, 30), (380, 60), (20, 60), rng, nx, depth=0.6)
    art = banana_leaf(art, W, H, curve([(-30, 250), (120, 170), (300, 150)], 20), 46, rng, nx, depth=0.8)
    art = monst(art, W, H, -40, 10, 300, 0.55, rng, nx, depth=1.0)
    art = anthurium(art, W, H, 250, 250, 40, -0.3, rng, nx, stem=(-60, 120))
    preview(art, "tg-corner", bg=BG)
    save(art, f"{OUT}/corner.webp", max_w=300, quality=80)


def bloom():
    """Small centrepiece: a strelitzia, two anthuriums and a monstera leaf (emblem / closing)."""
    W, H = 520, 460
    rng = random.Random(19); nx = Seq(1400)
    art = blank(W, H)
    art = monst(art, W, H, 250, 400, 250, -2.0, rng, nx)
    art = monst(art, W, H, 270, 410, 210, -1.0, rng, nx, amt=0.6)
    art = bird_of_paradise(art, W, H, 190, 230, 110, -0.25, rng, nx)
    art = anthurium(art, W, H, 350, 300, 52, 0.25, rng, nx)
    art = anthurium(art, W, H, 130, 330, 42, -0.4, rng, nx)
    preview(art, "tg-bloom", bg=BG)
    save(art, f"{OUT}/bloom.webp", max_w=420, quality=80)


def leaf():
    W, H = 260, 220
    rng = random.Random(3); nx = Seq(2000)
    art = blank(W, H)
    art = monst(art, W, H, 30, 190, 200, -0.75, rng, nx)
    preview(art, "tg-leaf", bg=BG)
    save(art, f"{OUT}/leaf.webp", max_w=160, quality=82)


def divider():
    """A single arching palm leaflet spray with a small anthurium bud at the centre."""
    W, H = 720, 120
    rng = random.Random(5); nx = Seq(2400)
    art = blank(W, H)
    for d in (-1, 1):
        base = (360, 70)
        tip = (360 + d * 340, 64)
        rach = curve([base, (360 + d * 170, 44), tip], 30)
        items = [(rach, 2.4, (0.02, 0.6))]
        for j in range(2, len(rach) - 1):
            px, py = rach[j]
            a, b = rach[j - 1], rach[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            ll = 34 * (1 - j / len(rach)) + 10
            for side in (-1, 1):
                aa = ang + side * 0.6
                items.append(([(px, py), (px + math.cos(aa) * ll, py + math.sin(aa) * ll + 6)], 3.0, (0.05, 0.7)))
        m = strokes(W, H, items)
        art = lit_paint(art, W, H, m, nx, base=(G3, G2), amt=0.7)
    art = anthurium(art, W, H, 360, 64, 26, 0.0, rng, nx)
    preview(art, "tg-divider", bg=BG)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
