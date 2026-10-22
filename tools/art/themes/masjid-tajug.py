"""Masjid Tajug — an old Nusantara mosque (original design, Demak/Kudus-inspired): three stacked tajug roofs of teak
sirap shingles with a clay mustaka, white lime walls, teak serambi pillars, a red-brick paduraksa gate, sandy
courtyard, sawo kecik trees, warm morning light from the left. No figures.
Run: python3 -I masjid-tajug.py [part ...]  parts: masjid gapura sawo sirap divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b2_lib import *

OUT = outdir("masjid-tajug")
PARTS = sys.argv[1:] or ["masjid", "gapura", "sawo", "sirap", "divider"]
SIRAP, SIRAP_D, SIRAP_L = "#6e5240", "#3e2c22", "#9a7a5e"
TEAK, TEAK_D = "#8a5630", "#5a341c"
LIME, LIME_D = "#f1e8d6", "#cdbfa4"
BRICK_L, BRICK_D, MORTAR = "#bf5f3c", "#923c24", "#d9b892"
SAND, SAND_D = "#e9d6ae", "#cdb184"
LEAF, LEAF_D = "#4f6b3a", "#2e4426"
SUN = "#ffe3b0"


def tier(W, H, x0b, x1b, yb, x0t, x1t, yt):
    return poly(W, H, [(x0b, yb), (x0t, yt), (x1t, yt), (x1b, yb)])


def shingles(dst, area, W, H, nx, light_x, bw=8, bh=9):
    """Sirap: wooden shingle rows (running bond), light falling from the left, dark lower edges."""
    bm, tone = brick_field(W, H, bw, bh, 1.2, nx())
    ca, cb = col_arr(SIRAP_L), col_arr(SIRAP_D)
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    lit = np.clip(1 - np.abs(xx - light_x) * 1.6, 0, 1)
    mid = col_arr(SIRAP)
    rgb = mid * (1 - tone[..., None] * 0.25) * (0.75 + 0.4 * lit[..., None])
    rgb = rgb * bm[..., None] + (mid * 0.55) * (1 - bm[..., None])
    st = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (2.5, 0.4))
    rgb *= (1 + (st[..., None] - 0.5) * 0.25)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    lower = ((yy % bh) / bh)
    rgb *= (1.06 - 0.16 * lower)[..., None]
    rgb *= (0.92 + 0.14 * fbm(W, H, nx(), 5, 2))[..., None]
    a = np.clip((gaussian_filter(displace(area, nx(), 0.8, 10), 0.6) - 0.3) * 2.4, 0, 1)
    return over(dst, np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1))


def mustaka(dst, W, H, cx, y, s, nx):
    """Clay mustaka: stacked bulb + petals + spire (geometric/floral only)."""
    m = np.maximum.reduce([
        shapes(W, H, [ellipse_pts(cx, y - 8 * s, 12 * s, 9 * s, 16)]),
        shapes(W, H, [[(cx - 15 * s, y), (cx + 15 * s, y), (cx + 9 * s, y - 6 * s), (cx - 9 * s, y - 6 * s)]], smooth=False),
        shapes(W, H, [ellipse_pts(cx, y - 22 * s, 7 * s, 7 * s, 14)]),
        polyline_mask(W, H, [[(cx, y - 26 * s), (cx, y - 46 * s)]], 2.6 * s),
    ])
    dst = GP(dst, m, "#a45a36", "#7a3e24", seed=nx(), rough=0.5, pad=6)
    pet = shapes(W, H, [petal_pts(cx + dx * s, y - 10 * s, 9 * s, 3 * s, -math.pi / 2 + dx * 0.05, n=8) for dx in (-9, -3, 3, 9)])
    dst = over(dst, flat(pet, "#d9894e", 0.7))
    return dst


def sawo_tree(dst, W, H, x, by, h, nx, rng, light=True):
    """Sawo kecik: short dark trunk, very dense rounded crown of small glossy leaves (clustered dabs)."""
    trunk = strokes(W, H, [(curve([(x, by), (x + rng.uniform(-6, 6), by - h * 0.25), (x + rng.uniform(-4, 4), by - h * 0.45)], 16), h * 0.07, (0.0, 0.3)),
                           (curve([(x, by - h * 0.3), (x - h * 0.1, by - h * 0.5)], 10), h * 0.03, (0.0, 0.5)),
                           (curve([(x, by - h * 0.32), (x + h * 0.1, by - h * 0.52)], 10), h * 0.03, (0.0, 0.5))])
    dst = GP(dst, trunk, "#4a3424", "#2e2016", seed=nx(), rough=0.6, pad=6)
    cy = by - h * 0.64
    blobs = [deform(ellipse_pts(x, cy, h * 0.34, h * 0.26, 18), rng, 2, 0.08)]
    blobs += [deform(ellipse_pts(x + rng.gauss(0, h * 0.13), cy + rng.gauss(0, h * 0.08), h * rng.uniform(0.12, 0.18), h * rng.uniform(0.1, 0.14), 12), rng, 2, 0.15) for _ in range(14)]
    crown = shapes(W, H, blobs)
    dst = G(dst, crown, "#46613a", LEAF_D, seed=nx(), density=0.97, edge=0.5, bloom=0.3, rough=4)
    dabs = []
    for _ in range(int(h * 1.6)):
        a = rng.uniform(0, math.tau); r = abs(rng.gauss(0, 0.5)) * h * 0.3
        px, py = x + math.cos(a) * r * 1.2, cy + math.sin(a) * r * 0.85
        ang = rng.uniform(0, math.pi)
        dabs.append(petal_pts(px, py, h * 0.035, h * 0.014, ang, n=6))
    dm = shapes(W, H, dabs) * gaussian_filter(crown, 3)
    if light:
        lit = light_mask(H, W, x - h * 0.25, cy - h * 0.2, h * 0.5)
        dst = over(dst, flat(dm * lit, "#a9b86a", 0.8))
    dst = over(dst, flat(dm * (1 - light_mask(H, W, x - h * 0.25, cy - h * 0.2, h * 0.5)), "#22361e", 0.5))
    return dst


def paduraksa(dst, W, H, cx, base, s, nx, hole_out=None):
    """Red-brick paduraksa gate: stepped plinth, jambs with recessed bands, rectangular doorway, a stepped roof of
    corbelled brick tiers and a top finial. Returns (art, door mask)."""
    hw = 92 * s
    body = rect(W, H, cx - hw, base - 300 * s, cx + hw, base)
    plinth = rect(W, H, cx - hw - 14 * s, base - 26 * s, cx + hw + 14 * s, base)
    tiers = []
    y = base - 300 * s; ww = hw + 10 * s
    for k in range(5):
        tiers.append(rect(W, H, cx - ww, y - 16 * s, cx + ww, y))
        y -= 16 * s; ww -= 13 * s
        tiers.append(rect(W, H, cx - ww + 6 * s, y - 22 * s, cx + ww - 6 * s, y))
        y -= 22 * s; ww -= 6 * s
    top = poly(W, H, [(cx - ww, y), (cx, y - 44 * s), (cx + ww, y)])
    allm = np.maximum.reduce([body, plinth, top] + tiers)
    dst = bricks(dst, allm, W, H, BRICK_L, BRICK_D, MORTAR, seed=nx(), bw=max(8, int(18 * s)), bh=max(4, int(7 * s)))
    # side shadow + morning light
    dst = over(dst, shade_lr(allm, W, "#3a160c", 0.45, side=1, width=0.45))
    dst = over(dst, flat(allm * light_mask(H, W, cx - hw, base - 340 * s, 220 * s), SUN, 0.28))
    # cornice shadows under each tier
    for t in tiers[::2]:
        b = bbox(t, 0)
        if b:
            y0, y1, x0, x1 = b
            dst = over(dst, flat(rect(W, H, x0 + 4, y1, x1 - 4, y1 + 4 * s), "#4a1c10", 0.5))
    # recessed panels on jambs
    for sx in (-1, 1):
        pnl = rect(W, H, cx + sx * hw * 0.62 - 12 * s, base - 260 * s, cx + sx * hw * 0.62 + 12 * s, base - 60 * s)
        dst = over(dst, flat(outline(pnl, 3 * s), "#5a2214", 0.55))
    door = rect(W, H, cx - 40 * s, base - 236 * s, cx + 40 * s, base)
    lintel = rect(W, H, cx - 50 * s, base - 250 * s, cx + 50 * s, base - 236 * s)
    dst = over(dst, wood(lintel, TEAK, TEAK_D, seed=nx(), angle=1.5708))
    dst = over(dst, flat(outline(door, 3 * s) * (1 - lintel), "#3a160c", 0.5))
    dst = mustaka(dst, W, H, cx, y - 40 * s, s * 0.7, nx)
    return dst, door


if "masjid" in PARTS:
    W, H = 860, 560
    nx = Seq(74100); rng = random.Random(31)
    art = blank(W, H)
    G0 = 470
    # far trees behind
    art = sawo_tree(art, W, H, 640, G0 - 10, 250, nx, rng)
    art = sawo_tree(art, W, H, 76, G0 + 6, 300, nx, rng)
    art = sawo_tree(art, W, H, 790, G0 + 10, 280, nx, rng)
    cx = 430
    # walls of the main hall
    hall = rect(W, H, 250, 320, 610, G0)
    art = GP(art, hall, LIME, LIME_D, seed=nx(), rough=0.6, streak=0.6)
    art = over(art, shade_lr(hall, W, "#8a7658", 0.35, side=1, width=0.5))
    # tier 1/2/3 with clerestory gaps (dark + teak lattice)
    t1 = tier(W, H, 170, 690, 334, 290, 570, 252)
    g1 = rect(W, H, 300, 232, 560, 254)
    t2 = tier(W, H, 286, 574, 236, 360, 500, 176)
    g2 = rect(W, H, 368, 158, 492, 178)
    t3 = tier(W, H, 356, 504, 162, cx - 2, cx + 2, 92)
    for g in (g1, g2):
        art = GP(art, g, "#2a1a10", seed=nx(), rough=0.4, pad=6)
        lat = g * hatch(W, H, 0.0, 9, 0.22, nx(), 0.3)
        art = over(art, flat(lat, TEAK, 0.9))
    for t in (t1, t2, t3):
        art = shingles(art, t, W, H, nx, 0.36)
        b = bbox(t, 0)
        y0, y1, x0, x1 = b
        eave = rect(W, H, x0 - 2, y1 - 6, x1 + 2, y1 + 1)
        art = over(art, wood(eave, TEAK, TEAK_D, seed=nx(), angle=0.0))
        art = over(art, flat(rect(W, H, x0 + 10, y1 + 1, x1 - 10, y1 + 8), "#2a1a10", 0.45))
        hip = polyline_mask(W, H, [[(x0 + 2, y1 - 3), (x0 + (x1 - x0) * 0.24, y0 + 1)], [(x1 - 2, y1 - 3), (x1 - (x1 - x0) * 0.24, y0 + 1)]], 2.2)
        art = over(art, flat(hip * t, SIRAP_D, 0.5))
    art = over(art, flat(t1 * light_mask(H, W, 260, 250, 260), SUN, 0.18))
    art = mustaka(art, W, H, cx, 96, 1.2, nx)
    # serambi: low wide limasan roof on teak pillars in front
    ser = poly(W, H, [(150, 404), (220, 372), (640, 372), (710, 404)])
    shade = rect(W, H, 170, 404, 690, G0)
    art = G(art, shade, "#3a2818", seed=nx(), density=0.75, edge=0.2, bloom=0.1, rough=2)
    doors = np.maximum.reduce([rect(W, H, x, 420, x + 26, G0) for x in (330, 417, 504)])
    art = over(art, wood(doors, TEAK_D, "#3a2010", seed=nx(), angle=1.5708))
    pil = np.maximum.reduce([rect(W, H, x - 6, 404, x + 6, G0) for x in range(186, 690, 56)])
    art = over(art, wood(pil, TEAK, TEAK_D, seed=nx(), angle=1.5708, grain=5))
    art = over(art, flat(pil * light_mask(H, W, 180, 420, 360), SUN, 0.3))
    umpak = np.maximum.reduce([rect(W, H, x - 9, G0 - 8, x + 9, G0 + 2) for x in range(186, 690, 56)])
    art = GP(art, umpak, "#8a8070", "#6a6258", seed=nx(), rough=0.5, pad=6)
    art = shingles(art, ser, W, H, nx, 0.3, bw=7, bh=7)
    art = over(art, wood(rect(W, H, 148, 400, 712, 408), TEAK, TEAK_D, seed=nx(), angle=0.0))
    # sandy courtyard
    yard = shapes(W, H, [[(-20, G0 - 2), (W + 20, G0 - 2), (W + 20, H + 10), (-20, H + 10)]], smooth=False)
    art = G(art, yard, SAND, SAND_D, seed=nx(), density=0.9, edge=0.2, bloom=0.4, rough=4, gran=0.6)
    sh = shapes(W, H, [deform(ellipse_pts(470, G0 + 10, 300, 10, 16), rng, 1, 0.05)])
    art = G(art, sh, "#9a7a52", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=4)
    grit = circles(W, H, [(rng.uniform(0, W), rng.uniform(G0 + 4, H), rng.uniform(0.6, 1.4)) for _ in range(400)])
    art = over(art, flat(grit, "#a88a5e", 0.45))
    # low brick wall (pagar) in front with the paduraksa gate on the left
    wall = rect(W, H, -10, 494, W + 10, 532)
    art = bricks(art, wall, W, H, BRICK_L, BRICK_D, MORTAR, seed=nx(), bw=16, bh=6)
    art = over(art, flat(rect(W, H, -10, 490, W + 10, 496), "#7a2e18", 0.9))
    art = over(art, flat(wall * light_mask(H, W, 0, 480, 600), SUN, 0.2))
    art, _ = paduraksa(art, W, H, 186, 540, 0.62, nx)
    # foreground sand strip
    fg = rect(W, H, -10, 532, W + 10, H + 10)
    art = G(art, fg, SAND, "#dcc394", seed=nx(), density=0.95, edge=0.15, bloom=0.3, rough=3, gran=0.6)
    preview(art, "mt-masjid", "#fbeedb")
    save(art, f"{OUT}/masjid.webp", max_w=780, quality=78)
    clear()

if "gapura" in PARTS:
    W, H = 600, 860
    nx = Seq(74200); rng = random.Random(41)
    art = blank(W, H)
    # side wings (sayap): low stepped brick walls flanking the gate
    for sx in (-1, 1):
        wing = poly(W, H, [(300 + sx * 130, 860), (300 + sx * 130, 640), (300 + sx * 196, 680), (300 + sx * 196, 720), (300 + sx * 300, 740), (300 + sx * 300, 860)])
        art = bricks(art, wing, W, H, BRICK_L, BRICK_D, MORTAR, seed=nx(), bw=24, bh=10)
        art = over(art, flat(wing * light_mask(H, W, 0, 600, 500), SUN, 0.2))
    art, door = paduraksa(art, W, H, 300, 860, 1.5, nx)
    art[..., 3] *= (1 - door)
    preview(art, "mt-gapura", "#fbeedb")
    save_full(art, f"{OUT}/gapura.webp", size=(420, 602), quality=80)
    clear()

if "sawo" in PARTS:
    W, H = 420, 440
    nx = Seq(74300); rng = random.Random(51)
    art = blank(W, H)
    gr = shapes(W, H, [deform(ellipse_pts(210, 420, 150, 14, 14), rng, 2, 0.08)])
    art = G(art, gr, SAND_D, seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=4)
    art = sawo_tree(art, W, H, 210, 420, 400, nx, rng)
    preview(art, "mt-sawo", "#fbeedb")
    save(art, f"{OUT}/sawo.webp", max_w=260, quality=80)
    clear()

if "sirap" in PARTS:
    W, H = 240, 84
    nx = Seq(74400)
    art = shingles(blank(W, H), np.ones((H, W), np.float32), W, H, nx, 0.5, bw=12, bh=7)
    art = np.ascontiguousarray(tileable(art))
    art[..., 3] = 1
    preview(art, "mt-sirap")
    save_rgb(art, f"{OUT}/sirap.webp", quality=78)
    clear()

if "divider" in PARTS:
    W, H = 600, 64
    nx = Seq(74500); cy = 34
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 2.5, 0, 1)[None, :]
    ln = np.maximum(rect(W, H, 40, cy - 1.2, 250, cy + 1.2), rect(W, H, 350, cy - 1.2, 560, cy + 1.2)) * fade
    art = over(blank(W, H), flat(ln, TEAK, 0.85))
    # three stacked tajug silhouettes (tiny) in the centre
    t = np.maximum.reduce([tier(W, H, 262, 338, cy + 14, 280, 320, cy + 2), tier(W, H, 278, 322, cy, 290, 310, cy - 9), tier(W, H, 288, 312, cy - 11, 299, 301, cy - 24)])
    art = shingles(art, t, W, H, nx, 0.4, bw=6, bh=4)
    art = mustaka(art, W, H, 300, cy - 22, 0.35, nx)
    bk = np.maximum.reduce([rect(W, H, x, cy + 3, x + 8, cy + 8) for x in list(range(200, 250, 11)) + list(range(352, 400, 11))]) * fade
    art = bricks(art, bk, W, H, BRICK_L, BRICK_D, MORTAR, seed=nx(), bw=9, bh=5)
    preview(art, "mt-divider", "#fbeedb")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()
