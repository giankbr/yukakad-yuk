"""Rote Sasando — sasando (bamboo tube zither cradled in a pleated lontar-leaf resonator), the ti'i langga lontar hat,
lontar palms and the turquoise Nemberala lagoon, in watercolour with gouache accents; a plaited lontar texture tile.
Run: python3 -I rote-sasando.py [part ...]   parts: anyam sasando tiilangga palm nemberala"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e1_lib import *

OUT = outdir("rote-sasando")
PARTS = sys.argv[1:] or ["anyam", "sasando", "kipas", "tiilangga", "palm", "nemberala"]
STRAW, STRAW_D, STRAW_DD = "#e2c07a", "#b5873f", "#7d5426"
SEA_L, SEA_M, SEA_D = "#7fd6cf", "#2fb0ae", "#1d6f8a"
INK = "#173447"


def plait(N=128, band=8):
    """Diagonal 2/2 plaited lontar strips (anyaman): RGB tile."""
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    u = (xx + yy) / band; v = (xx - yy) / band
    iu = np.floor(u); iv = np.floor(v)
    fu = u - iu; fv = v - iv
    top = ((iu + iv) % 2 == 0)  # which strip is on top in this cell
    prof_u = np.sin(np.pi * fv) ** 0.6  # strip running along u has profile across v
    prof_v = np.sin(np.pi * fu) ** 0.6
    lum = np.where(top, 0.72 + 0.32 * prof_u, 0.64 + 0.32 * prof_v)
    # alternate dye: every 4th strip a bit darker (sun-bleached vs fresh leaf)
    tone = np.where(top, (np.mod(iu, 4) == 0) * 1.0, (np.mod(iv, 6) == 0) * 1.0)
    rng = np.random.default_rng(3)
    fib = gaussian_filter(rng.random((N, N)).astype(np.float32), 0.6)
    fib = (fib - fib.mean()) / fib.std()
    base = C("#efe0bd") * (1 - tone[..., None] * 0.35) + C("#d8b679") * tone[..., None] * 0.35
    gap = np.where(top, np.abs(fv - 0.5) > 0.46, np.abs(fu - 0.5) > 0.46)
    lum = lum * (1 - 0.25 * gap)
    rgb = base * (lum[..., None] * (1 + fib[..., None] * 0.03))
    rgb = gaussian_filter(rgb, (0.6, 0.6, 0), mode="wrap")
    return np.clip(rgb, 0, 1)


if "anyam" in PARTS:
    t = plait(168, 14)
    big = np.kron(t, np.ones((2, 2, 1)))
    prev_rgb(tile_to(big, 512, 400), "anyam")
    save_rgb_arr(big, f"{OUT}/anyam.webp", quality=72)
    clear()


def sasando_art(W, H, cx, by, s, seed, tube_on=True, full=False):
    """Sasando: resonator fan of pleated lontar leaf behind a bamboo tube strung lengthwise."""
    nx = Seq(seed); rng = random.Random(seed)
    art = blank(W, H)
    R = 300 * s
    py = by - 40 * s  # fan pivot
    # resonator: wide fan from the pivot, scalloped rim (the folded leaf tips)
    a0, a1 = (math.radians(-180), math.radians(0)) if full else (math.radians(-172), math.radians(-8))
    n = 40 if full else 34
    rim = []
    for k in range(n + 1):
        t = k / n
        a = a0 + (a1 - a0) * t
        L = R * (0.9 + 0.1 * math.sin(math.pi * t)) * (1.0 if k % 2 == 0 else 0.93)
        rim.append((cx + math.cos(a) * L, py + math.sin(a) * L * 0.98))
    fan = shapes(W, H, [[(cx - 10 * s, py + 40 * s)] + rim + [(cx + 10 * s, py + 40 * s)]], smooth=False)
    art = G(art, fan, STRAW, "#e8c47c", seed=nx(), density=0.95, edge=0.65, bloom=0.35, rough=3, gran=0.35)
    art = G(art, fan, "#d9a95a", seed=nx(), density=0.35, edge=0.3, bloom=0.5, rough=4)
    # inner shadow toward the pivot (the leaf is a bowl)
    yy, xx = ygrid(W, H)
    d = np.hypot(xx - cx, yy - py) / R
    art = G(art, fan * np.clip(1 - d * 1.1, 0, 1) ** 1.0, STRAW_D, seed=nx(), density=0.85, edge=0.1, bloom=0.3, rough=4)
    # folded faces: every other wedge turns away from the light
    faces = []
    for k in range(0, n, 2):
        ta, tb = k / n, (k + 1) / n
        aa, ab = a0 + (a1 - a0) * ta, a0 + (a1 - a0) * tb
        La = R * (0.9 + 0.1 * math.sin(math.pi * ta)); Lb = R * (0.9 + 0.1 * math.sin(math.pi * tb)) * 0.93
        faces.append([(cx, py), (cx + math.cos(aa) * La, py + math.sin(aa) * La * 0.98), (cx + math.cos(ab) * Lb, py + math.sin(ab) * Lb * 0.98)])
    art = G(art, shapes(W, H, faces, smooth=False) * fan, "#9a6a30", seed=nx(), density=0.32, edge=0.25, bloom=0.3, rough=1.5)
    # pleats: alternating dark valleys / light ridges radiating from the pivot
    val, rid = [], []
    for k in range(n + 1):
        t = k / n
        a = a0 + (a1 - a0) * t + rng.uniform(-0.01, 0.01)
        L = R * (0.9 + 0.1 * math.sin(math.pi * t)) * (1.0 if k % 2 == 0 else 0.93)
        pts = [(cx + math.cos(a) * L * u, py + math.sin(a) * L * u * 0.98) for u in np.linspace(0.12, 0.99, 8)]
        (val if k % 2 else rid).append((pts, (2.6 if k % 2 else 1.6) * s, (0.25, 0.05)))
    art = G(art, strokes(W, H, val), STRAW_DD, seed=nx(), density=0.75, edge=0.2, bloom=0.0, rough=1.2, gran=0.3)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#fff3d2"), strokes(W, H, rid) * 0.45))
    # fine leaf veins between pleats
    veins = []
    for k in range(n * 3):
        t = k / (n * 3)
        a = a0 + (a1 - a0) * t
        L = R * rng.uniform(0.55, 0.85)
        veins.append(([(cx + math.cos(a) * L * 0.3, py + math.sin(a) * L * 0.3), (cx + math.cos(a) * L, py + math.sin(a) * L)], 0.6 * s, (0.2, 0.2)))
    art = G(art, strokes(W, H, veins), STRAW_D, seed=nx(), density=0.3, edge=0, bloom=0, rough=0.8)
    # rim: tied with a thin rattan binding
    rim_line = strokes(W, H, [(rim, 3.0 * s, None)])
    art = G(art, rim_line, "#8a5a28", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=1)
    if not tube_on:
        return art
    # tube (bamboo): drawn over the fan, slightly taller
    tw = 34 * s; top = by - 470 * s; bot = by + 6 * s
    tube = poly(W, H, [(cx - tw, top + 8 * s), (cx - tw * 0.92, top), (cx + tw * 0.92, top), (cx + tw, top + 8 * s), (cx + tw, bot), (cx - tw, bot)], smooth=False)
    shade = np.clip((xx - (cx - tw)) / (2 * tw), 0, 1)
    art = GP(art, tube, "#cdbb72", "#b9a55a", seed=nx(), rough=1.0, streak=0.8)
    art = G(art, tube * np.clip((shade - 0.55) * 2.4, 0, 1), "#6e6a2c", seed=nx(), density=0.6, edge=0.1, bloom=0.2, rough=1.5)
    art = G(art, tube * np.clip((0.25 - shade) * 4, 0, 1), "#8a7d38", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=1.5)
    hi = tube * np.exp(-((shade - 0.36) / 0.07) ** 2)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#fff6d6"), hi * 0.55))
    # bamboo nodes
    nodes = [top + 60 * s, by - 250 * s, by - 60 * s]
    art = G(art, strokes(W, H, [([(cx - tw, y), (cx, y + 3 * s), (cx + tw, y)], 3.5 * s, None) for y in nodes]), "#6b5f26", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=1)
    # strings + staggered wooden bridges (senda)
    bridges = []
    strs = []
    for i in range(11):
        x = cx - tw * 0.86 + i * tw * 1.72 / 10
        y_a = top + 26 * s + (i % 3) * 10 * s
        y_b = bot - 18 * s - ((i + 1) % 3) * 12 * s
        strs.append(([(x, y_a), (x, y_b)], 0.9 * s, None))
        for (yb) in (y_a + 8 * s, y_b - 8 * s):
            bridges.append(poly_pts_box(x, yb, 3.4 * s, 4.2 * s))
    art = GP(art, shapes(W, H, bridges, smooth=False), "#5b3a1e", "#7a4d26", seed=nx(), rough=0.4)
    sm = strokes(W, H, strs)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#3b3a36"), sm * 0.75))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f6f2e6"), np.roll(sm, 1, 1) * 0.35))
    # tuning pegs at the top
    pegs = []
    for i in range(5):
        y = top + 18 * s + i * 7 * s
        side = -1 if i % 2 else 1
        pegs.append(([(cx + side * tw * 0.7, y), (cx + side * (tw + 14 * s), y - 2 * s)], 3.2 * s, (0.0, 0.3)))
    art = GP(art, strokes(W, H, pegs), "#5b3a1e", "#8a5a2c", seed=nx(), rough=0.5)
    # contact shadow on the ground
    sh = ellipses(W, H, [(cx, by + 12 * s, 120 * s, 12 * s, 0)])
    art = knockout(art, np.zeros_like(sh), 0)  # no-op keeps API symmetrical
    art = glaze(rgba(np.ones((H, W, 3), np.float32) * C("#8a6a48"), gaussian_filter(sh, 6 * s) * 0.35), art)
    return art


def poly_pts_box(x, y, w, h):
    return [(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)]


if "sasando" in PARTS:
    W, H = 700, 640
    art = sasando_art(W, H, 350, 600, 1.0, 5100)
    preview(art, "sasando", tone="#f6efe0")
    save(art, f"{OUT}/sasando.webp", max_w=560, quality=80)
    clear()

if "kipas" in PARTS:
    W, H = 680, 360
    art = sasando_art(W, H, 340, 380, 1.08, 5300, tube_on=False, full=True)
    preview(art, "kipas", tone="#f6efe0")
    save(art, f"{OUT}/kipas.webp", max_w=600, quality=78)
    clear()

if "tiilangga" in PARTS:
    W, H = 420, 420
    nx = Seq(6100); rng = random.Random(61)
    art = blank(W, H)
    cx = 210
    # brim: wide flat ellipse
    brim = ellipses(W, H, [(cx, 300, 190, 46, 0)])
    art = G(art, brim, STRAW, "#e9cf92", seed=nx(), density=0.92, edge=0.55, bloom=0.3, rough=2, gran=0.3)
    yy, xx = ygrid(W, H)
    # crown: tall rounded cone
    crown = poly(W, H, [(cx - 88, 300), (cx - 84, 250), (cx - 78, 222), (cx - 50, 206), (cx, 202), (cx + 50, 206), (cx + 78, 222), (cx + 84, 250), (cx + 88, 300)])
    art = knockout(art, crown, 0.4)
    art = G(art, crown, "#e6c886", STRAW, seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=2, gran=0.3)
    art = G(art, crown * np.clip((xx - cx) / 90, 0, 1), STRAW_D, seed=nx(), density=0.55, edge=0.1, bloom=0.3, rough=2)
    # plait lines on crown and brim
    pl = []
    for k in range(-12, 13):
        x0 = cx + k * 8
        pl.append(([(x0, 300), (x0 + 60, 200)], 1.1, None))
        pl.append(([(x0, 300), (x0 - 60, 200)], 1.1, None))
    plm = strokes(W, H, pl) * crown
    art = G(art, plm, STRAW_DD, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    rings = [([(cx + math.cos(a) * rx, 300 + math.sin(a) * rx * 0.24) for a in np.linspace(0, 2 * math.pi, 60)], 1.0, None) for rx in range(70, 190, 12)]
    art = G(art, strokes(W, H, rings) * brim * (1 - crown), STRAW_DD, seed=nx(), density=0.3, edge=0, bloom=0, rough=0.6)
    # dark band at the crown base
    band = poly(W, H, [(cx - 89, 300), (cx - 88, 288), (cx + 88, 288), (cx + 89, 300), (cx, 304)])
    art = G(art, band, "#8a3b2a", "#9a5a36", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1)
    # the ti'i langga horn: a curved spire of rolled leaf rising from the front of the crown
    hp = curve([(cx - 4, 262), (cx - 8, 190), (cx + 2, 110), (cx + 20, 46), (cx + 34, 18)], 40)
    horn = poly(W, H, ribbon_poly(hp, 22, 4), smooth=True)
    art = G(art, horn, "#d3ad62", STRAW, seed=nx(), density=0.95, edge=0.55, bloom=0.2, rough=1.2)
    art = G(art, horn * np.clip((xx - cx - 2) / 12, 0, 1), STRAW_DD, seed=nx(), density=0.45, edge=0.1, bloom=0.2, rough=1)
    wraps = [([(cx - 30, y + 6), (cx + 40, y - 6)], 1.1, None) for y in range(30, 262, 8)]
    art = G(art, strokes(W, H, wraps) * horn, STRAW_DD, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    art = G(art, gaussian_filter(ellipses(W, H, [(cx, 318, 180, 14, 0)]), 6) * 0.5, "#9c7c58", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    preview(art, "tiilangga", tone="#f6efe0")
    save(art, f"{OUT}/tiilangga.webp", max_w=220, quality=82)
    clear()

if "palm" in PARTS:
    W, H = 440, 760
    nx = Seq(7100); rng = random.Random(71)
    art = blank(W, H)
    art = paint_palm(art, W, H, 215, 750, 560, rng, nx, lean=0.03, crown=1.3)
    preview(art, "palm", tone="#f6efe0")
    save(art, f"{OUT}/palm.webp", max_w=260, quality=80)
    clear()

if "nemberala" in PARTS:
    W, H = 920, 640
    nx = Seq(8100); rng = random.Random(81)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    hz = 250
    sky = poly(W, H, [(0, 0), (W, 0), (W, hz + 6), (0, hz + 6)], smooth=False)
    art = G(art, sky * np.clip((hz + 10 - yy) / 260, 0, 1) ** 0.6, "#a9d6dc", "#f4d7b4", seed=nx(), density=0.8, edge=0.0, bloom=0.5, rough=10, feather=8)
    # long clouds
    for (cx, cy, rx) in [(220, 120, 160), (640, 80, 120), (770, 170, 90)]:
        cl = poly(W, H, deform(ellipse_pts(cx, cy, rx, 16, 14), rng, 2, 0.1))
        art = G(art, cl, "#dcd6e2", "#f2e4d4", seed=nx(), density=0.55, edge=0.45, bloom=0.5, rough=6)
    # far island (Ndana) on the horizon
    isl = poly(W, H, [(560, hz + 2), (600, hz - 16), (660, hz - 22), (720, hz - 12), (760, hz + 2)])
    art = G(art, isl, "#7f9c96", "#94aaa0", seed=nx(), density=0.65, edge=0.4, bloom=0.3, rough=3)
    # sea: deep at the horizon -> turquoise -> pale shallows over sand
    sea = poly(W, H, [(0, hz), (W, hz), (W, 520), (0, 560)], smooth=False)
    art = G(art, sea * np.clip((360 - yy) / 110, 0, 1), SEA_D, "#256f96", seed=nx(), density=0.9, edge=0.2, bloom=0.3, rough=4)
    art = G(art, sea * np.clip((yy - hz - 30) / 80, 0, 1) * np.clip((500 - yy) / 90, 0, 1), SEA_M, "#38bcb5", seed=nx(), density=0.85, edge=0.1, bloom=0.45, rough=5)
    art = G(art, sea * np.clip((yy - 380) / 90, 0, 1), SEA_L, "#a8e6dc", seed=nx(), density=0.75, edge=0.2, bloom=0.5, rough=5)
    rip = sea_strokes(W, H, hz + 6, 520, rng, n=260, length=(16, 80), width=(0.7, 2.2))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#effcf8"), rip * sea * 0.55))
    art = G(art, sea_strokes(W, H, hz + 4, 400, rng, n=120, length=(30, 90), width=(0.8, 1.8)) * sea, "#1b5e78", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    # surf line at the reef edge (Nemberala break)
    surf = strokes(W, H, [(curve([(-20, 318), (300, 312), (620, 320), (940, 314)], 30), 3.0, (0.1, 0.1))])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ffffff"), gaussian_filter(surf, 1.6) * 0.75 * np.clip((fbm(W, H, 9, 70, 3) - 0.3) * 3, 0, 1)))
    # sand beach + foam lace
    sand = poly(W, H, [(0, 560), (300, 530), (600, 512), (W, 498), (W, H), (0, H)])
    art = G(art, sand, "#f3e6c8", "#ead6aa", seed=nx(), density=0.9, edge=0.4, bloom=0.4, rough=4, gran=0.5)
    foam = strokes(W, H, [(curve([(0, 556), (300, 527), (600, 509), (W, 495)], 40), 4.0, (0.05, 0.05))])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ffffff"), gaussian_filter(foam, 1.2) * 0.85))
    wet = poly(W, H, [(0, 562), (300, 533), (600, 515), (W, 501), (W, 512), (600, 528), (300, 548), (0, 580)])
    art = G(art, wet, "#cdbf9c", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3)
    # small fishing boat on the lagoon
    hull = poly(W, H, [(660, 410), (720, 410), (712, 420), (668, 420)])
    art = GP(art, hull, "#f4ede0", "#d9d0c0", seed=nx(), rough=0.6)
    art = GP(art, poly(W, H, [(664, 416), (716, 416), (712, 420), (668, 420)], smooth=False), "#b4442c", seed=nx(), rough=0.3)
    art = G(art, strokes(W, H, [([(690, 410), (690, 384)], 1.4, None)]), "#4a3a2a", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
    # lontar palms on the left shore + dune grass
    for (x, by, h, ln, sd) in [(70, 600, 420, -0.02, 1), (150, 586, 330, 0.04, 2), (860, 560, 300, 0.03, 3)]:
        r2 = random.Random(sd)
        art = paint_palm(art, W, H, x, by, h, r2, nx, lean=ln, crown=1.15)
        clear()
    grass = []
    for _ in range(140):
        x = rng.uniform(0, 260) if rng.random() < 0.7 else rng.uniform(780, W)
        y = 600 - (x < 300) * rng.uniform(0, 20) + rng.uniform(0, 40)
        grass.append(([(x, y), (x + rng.uniform(-10, 10), y - rng.uniform(14, 34))], 1.6, (0.0, 0.7)))
    art = G(art, strokes(W, H, grass), "#7e9a4c", "#a7a85a", seed=nx(), density=0.75, edge=0.2, bloom=0.2, rough=1)
    art[..., 3] *= vignette_mask(W, H, 19, inset=4, rough=20, fade=40)
    art[..., 3] *= np.clip((yy - 10 + (fbm(W, H, 5, 50, 3) - 0.5) * 60) / 120, 0, 1)
    preview(art, "nemberala", tone="#f6efe0")
    save(art, f"{OUT}/nemberala.webp", max_w=700, quality=55)
    clear()
