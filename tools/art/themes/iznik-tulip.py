"""Iznik Tulip — 16th-c. Iznik-inspired underglaze painting on white slip: tulips, carnations, saz leaves in cobalt,
turquoise, sage and raised tomato-red bole, thin dark outlines, crackled clear glaze, slight brush pooling.
Run: python3 -I iznik-tulip.py [part ...]   parts: dish spray border flower slip
Assets -> public/themes/art/iznik-tulip/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a3_lib import *

OUT = outdir("iznik-tulip")
PARTS = sys.argv[1:] or ["dish", "spray", "border", "flower", "slip"]
COBALT, COBALT_D, TURQ, RED, SAGE, LINE, SLIP = "#1f3f9a", "#142b72", "#2a95a3", "#c43a2c", "#5d8f4e", "#24302f", "#f7f4ec"


def paint_tulip(art, W, H, x, y, s, ang, rng, side=COBALT, mid=RED, line=True):
    left, right, centre = tulip_polys(x, y, s, ang)
    sides = shapes(W, H, [wob_poly(left, rng, 0.6), wob_poly(right, rng, 0.6)])
    cm = shape_mask(W, H, wob_poly(centre, rng, 0.6))
    art = I(art, sides, side, mix(side, "#2d55b8", 0.4), seed=rng.randint(1, 9999))
    art = B(art, cm, mid, seed=rng.randint(1, 9999))
    # white reserve stripes on the red petal
    stripe = strokes(W, H, [(rotp([(x + u * s, y - s * 0.35), (x + u * 0.6 * s, y - s * 1.0)], x, y, ang), s * 0.035, (0.2, 0.3)) for u in (-0.08, 0.08)])
    art = OV(art, stripe * cm, lambda m: rgba(flat(*m.shape, SLIP), gaussian_filter(m, 0.5) * 0.9))
    if line:
        art = K(art, np.maximum(outline_of(sides, 1.3), outline_of(cm, 1.3)), LINE, seed=rng.randint(1, 9999))
    return art


def paint_carnation(art, W, H, x, y, s, ang, rng, fan=RED, calyx=COBALT):
    fp, cp = carnation_polys(x, y, s, ang)
    fm = shape_mask(W, H, wob_poly(fp, rng, 0.6), smooth=False)
    cm = shape_mask(W, H, wob_poly(cp, rng, 0.5))
    art = B(art, fm, fan, seed=rng.randint(1, 9999))
    art = I(art, cm, calyx, seed=rng.randint(1, 9999))
    # inner petal lines (white reserves)
    vein = []
    for k in range(5):
        a = math.pi * (0.2 + 0.6 * k / 4)
        vein.append((rotp([(x, y - s * 0.5), (x - math.cos(a) * s * 0.6, y - s * (0.5 + math.sin(a) * 0.55))], x, y, ang), s * 0.03, (0.1, 0.4)))
    art = OV(art, strokes(W, H, vein) * fm, lambda m: rgba(flat(*m.shape, SLIP), gaussian_filter(m, 0.5) * 0.85))
    art = K(art, np.maximum(outline_of(fm, 1.3), outline_of(cm, 1.3)), LINE, seed=rng.randint(1, 9999))
    return art


def paint_saz(art, W, H, pts, width, rng, col=SAGE, col2=TURQ, serr=0.18):
    poly = saz_leaf(pts, width, serr)
    m = shape_mask(W, H, wob_poly(poly, rng, 0.5))
    art = I(art, m, col, col2, seed=rng.randint(1, 9999), pool=0.7)
    mid = strokes(W, H, [(pts[1:-1], max(1.2, width * 0.08), (0.05, 0.4))]) * m
    art = OV(art, mid, lambda mm: rgba(flat(*mm.shape, SLIP), gaussian_filter(mm, 0.5) * 0.7))
    art = K(art, outline_of(m, 1.3), LINE, seed=rng.randint(1, 9999))
    return art


def paint_stem(art, W, H, pts, width, rng, col=SAGE):
    m = strokes(W, H, [(pts, width * 1.5, (0.0, 0.3))])
    art = I(art, m, col, seed=rng.randint(1, 9999), pool=0.4)
    return art


def paint_bud(art, W, H, x, y, r, rng, col=COBALT):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 1.2, 10), rng, 1, 0.06))
    art = I(art, m, col, seed=rng.randint(1, 9999))
    return K(art, outline_of(m, 1.2), LINE, seed=rng.randint(1, 9999))


def finish(art, seed, crack=0.07):
    """Crazing in the clear glaze over the painted area + soft sheen."""
    h, w = art.shape[:2]
    c = crackle(w, h, seed)
    art = art.copy()
    art[..., :3] = art[..., :3] * (1 - c[..., None] * crack)
    return glaze_sheen(art, seed + 1, 0.05)


if "dish" in PARTS:
    # Iznik dish seen from above: white rim with cobalt "wave" scroll band, cavetto with 8 radiating sprays,
    # transparent well for the couple photo.
    clear()
    S = 820; c = S / 2
    rng = random.Random(7)
    R_out, R_rim, R_well = 400, 352, 226
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.hypot(xx - c, yy - c)
    plate = np.clip(R_out - rr + 0.5, 0, 1)
    well = np.clip(R_well - rr + 0.5, 0, 1)
    ground = slip_ground(S, S, 3, SLIP, crack=0.0)
    # plate shading: rim slope lighter toward top-left, shadow on lower-right inside the well edge
    ang = np.arctan2(yy - c, xx - c)
    slope = np.clip(1 - np.abs(rr - (R_rim + R_out) / 2) / 26, 0, 1)
    ground[..., :3] *= (1 - 0.06 * slope * (0.5 + 0.5 * np.sin(ang + 0.8)))[..., None]
    art = rgba(ground[..., :3], plate)
    # rim band: cobalt ground with white reserved wave-scrolls
    band = np.clip(np.clip(R_rim + 30 - rr, 0, 1) - np.clip(R_rim - 2 - rr, 0, 1), 0, 1) * 0 + ((rr > R_rim) & (rr < R_out - 12)).astype(np.float32)
    art = I(art, gaussian_filter(band, 0.8), COBALT, COBALT_D, seed=11, pool=0.4, rough=1.0)
    waves = []
    n = 26
    for k in range(n):
        a0 = k * math.tau / n
        rm = (R_rim + R_out - 12) / 2
        pts = [(c + math.cos(a0 + t * 0.2) * (rm + 10 * math.sin(t * math.pi)), c + math.sin(a0 + t * 0.2) * (rm + 10 * math.sin(t * math.pi))) for t in np.linspace(0, 1, 12)]
        sp = spiral_pts(pts[-1][0], pts[-1][1], 9, 2, a0 + 0.2 + math.pi / 2, 0.8, 20, 1)
        waves.append((pts + sp[1:], 4.2, (0.1, 0.6)))
    wv = strokes(S, S, waves) * band
    art = OV(art, wv, lambda m: rgba(flat(*m.shape, SLIP), np.clip(gaussian_filter(m, 0.6) * 1.2, 0, 1)))
    ring_lines = np.clip(np.abs(rr - R_rim) < 1.6, 0, 1).astype(np.float32) + np.clip(np.abs(rr - (R_out - 12)) < 1.4, 0, 1) + np.clip(np.abs(rr - (R_well + 6)) < 1.4, 0, 1) + np.clip(np.abs(rr - (R_well + 12)) < 1.0, 0, 1)
    art = K(art, gaussian_filter(np.clip(ring_lines, 0, 1), 0.4), LINE, seed=13)
    # cavetto sprays (8 units, alternating tulip / carnation heads)
    for k in range(8):
        a = k * math.tau / 8 + 0.18 + rng.uniform(-0.04, 0.04)
        ca, sa = math.cos(a), math.sin(a)
        P = lambda r_, t_: (c + math.cos(a + t_) * r_, c + math.sin(a + t_) * r_)
        stem = curve([P(R_well + 14, 0), P(R_well + 50, 0.06), P(R_rim - 64, 0.02)], 20)
        art = paint_stem(art, S, S, stem, 3.4, rng)
        # saz leaves arcing to both sides
        for side in (1, -1):
            leafc = curve([P(R_well + 22, 0.02 * side), P(R_well + 70, 0.16 * side * (1 if side < 0 else 0.6)), P(R_well + 104, 0.26 * side * (1 if side < 0 else 0.5))], 16)
            art = paint_saz(art, S, S, leafc, 13, rng, SAGE if k % 2 else TURQ, TURQ if k % 2 else SAGE)
        head_ang = a + math.pi / 2
        hx, hy = P(R_rim - 66, 0.02)
        if k % 2 == 0:
            art = paint_tulip(art, S, S, hx, hy, 62, head_ang, rng)
        else:
            art = paint_carnation(art, S, S, hx, hy, 60, head_ang, rng)
        # side sprig: small turquoise tulip bud on a curling stem toward the next unit
        sp = curve([P(R_well + 58, 0.05), P(R_well + 86, 0.2), P(R_well + 100, 0.3)], 14)
        art = paint_stem(art, S, S, sp, 2.2, rng)
        tx, ty = sp[-1]
        art = paint_tulip(art, S, S, tx, ty, 24, a + math.pi / 2 + 0.55, rng, TURQ, RED)
        # little rosettes between units
        bx, by = P((R_well + R_rim) / 2 + 22, math.tau / 16)
        art = paint_bud(art, S, S, bx, by, 7, rng, RED if k % 2 else COBALT)
    art = finish(art, 21)
    # cut the well (photo sits below); keep a soft inner shadow
    art[..., 3] = np.clip(art[..., 3] * (1 - well), 0, 1)
    sh = np.clip((R_well + 10 - rr) / 10, 0, 1) * (1 - well) * 0.0
    preview(art, "iz-dish", bg="#8d9fb6")
    save(art, f"{OUT}/dish.webp", max_w=620, quality=80)

if "spray" in PARTS:
    # vertical spray issuing from a small tuft: tulips, carnations, saz leaves and buds — cover sides / section accent
    clear()
    W, H = 460, 760
    rng = random.Random(17)
    art = blank(W, H)
    base = (230, 740)
    art = paint_stem(art, W, H, curve([base, (226, 560), (238, 360), (230, 160)], 40), 4.5, rng)
    art = paint_stem(art, W, H, curve([(228, 520), (170, 440), (120, 330)], 30), 3.4, rng)
    art = paint_stem(art, W, H, curve([(234, 470), (300, 400), (350, 290)], 30), 3.4, rng)
    art = paint_stem(art, W, H, curve([(232, 620), (160, 590), (96, 520)], 20), 3, rng)
    art = paint_stem(art, W, H, curve([(230, 640), (300, 610), (360, 540)], 20), 3, rng)
    art = paint_saz(art, W, H, curve([(230, 720), (150, 640), (60, 640), (30, 700)], 30), 24, rng, SAGE, TURQ)
    art = paint_saz(art, W, H, curve([(232, 700), (330, 610), (420, 600), (440, 650)], 30), 22, rng, TURQ, SAGE)
    art = paint_saz(art, W, H, curve([(236, 430), (300, 340), (300, 250)], 20), 14, rng, SAGE, TURQ, serr=0.25)
    art = paint_saz(art, W, H, curve([(228, 400), (170, 300), (176, 220)], 20), 13, rng, TURQ, SAGE, serr=0.25)
    art = paint_tulip(art, W, H, 230, 168, 74, 0.0, rng)
    art = paint_carnation(art, W, H, 120, 334, 56, -0.45, rng)
    art = paint_carnation(art, W, H, 350, 294, 56, 0.45, rng, RED, COBALT)
    art = paint_tulip(art, W, H, 96, 524, 44, -0.8, rng, TURQ, RED)
    art = paint_tulip(art, W, H, 360, 544, 44, 0.75, rng, TURQ, RED)
    for (x, y, r) in [(180, 220, 7), (290, 230, 7), (60, 420, 6), (400, 430, 6)]:
        art = paint_bud(art, W, H, x, y, r, rng, COBALT)
    art = finish(art, 31)
    preview(art, "iz-spray")
    save(art, f"{OUT}/spray.webp", max_w=300, quality=82)

if "border" in PARTS:
    # border strip: cobalt fillets, repeating small tulip / carnation alternating on white slip, turquoise dots
    clear()
    W, H = 960, 140
    rng = random.Random(27)
    art = slip_ground(W, H, 5, SLIP, crack=0.0)
    f = np.zeros((H, W), np.float32); f[8:22] = 1; f[H - 22:H - 8] = 1
    art = I(art, gaussian_filter(displace(f, 3, 1.2, 20), 0.5), COBALT, COBALT_D, seed=29, pool=0.4)
    for k, x in enumerate(np.arange(60, W, 120)):
        if k % 2 == 0:
            art = paint_tulip(art, W, H, x, 112, 58, 0.0, rng)
        else:
            art = paint_carnation(art, W, H, x, 112, 60, 0.0, rng)
        for side in (-1, 1):
            art = paint_saz(art, W, H, curve([(x, 112), (x + side * 26, 98), (x + side * 48, 80)], 10), 8, rng, SAGE, TURQ, serr=0)
    for x in np.arange(0, W + 1, 120):
        art = paint_bud(art, W, H, x, 72, 7, rng, TURQ)
    art = finish(art, 33)
    preview(art, "iz-border")
    save_full(art, f"{OUT}/border.webp", size=(640, 93), quality=80)

if "flower" in PARTS:
    # single tulip with two saz leaves — node / amp / sent ornament
    clear()
    W, H = 260, 300
    rng = random.Random(37)
    art = blank(W, H)
    art = paint_stem(art, W, H, curve([(130, 290), (128, 220), (130, 150)], 16), 4, rng)
    art = paint_saz(art, W, H, curve([(130, 280), (80, 230), (40, 200)], 16), 14, rng, SAGE, TURQ, serr=0.2)
    art = paint_saz(art, W, H, curve([(130, 270), (180, 220), (222, 196)], 16), 13, rng, TURQ, SAGE, serr=0.2)
    art = paint_tulip(art, W, H, 130, 156, 92, 0.0, rng)
    art = finish(art, 41)
    preview(art, "iz-flower")
    save(art, f"{OUT}/flower.webp", max_w=140, quality=84)

if "slip" in PARTS:
    n = 360
    g = slip_ground(n, n, 9, "#f6f2e8", wrap=True, crack=0.0)
    c = crackle(n, n, 15, 1.4, wrap=True)
    g[..., :3] *= (1 - c[..., None] * 0.08)
    save_tex(g, f"{OUT}/slip.webp", quality=72)

report(OUT)
