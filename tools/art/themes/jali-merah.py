"""Jali Merah — painted pieces: a pierced red-sandstone jali screen under a cusped arch (gouache stone, carved bevels,
transparent piercings so the page light shines through), the light it throws (soft shafts + projected lattice on the
floor, separate so it can breathe), a cusped-arch sandstone frame with marble inlay for photos, a chhatri pavilion,
a sandstone texture tile, an inlay band tile and a small inlay-star divider. No figures, no calligraphy.
Run: python3 -I jali-merah.py [part ...]  parts: jali light frame chhatri stone band divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k3_lib import *

OUT = outdir("jali-merah")
PARTS = sys.argv[1:] or ["jali", "light", "frame", "chhatri", "stone", "band", "divider"]
RED, RED_L, RED_D = "#b4543a", "#c86a4a", "#7d321f"
MARBLE = "#f1e6d2"


def cusped_arch(x0, x1, spring, apex, n_lobes=7, lobe=10.0, n=240, bottom=None):
    """Closed polygon: rectangle up to `spring`, then a pointed arch to `apex` with inward cusps (multifoil)."""
    cx = (x0 + x1) / 2; half = (x1 - x0) / 2
    rise = spring - apex
    pts = []
    for i in range(n + 1):
        t = i / n  # 0 left spring .. 1 right spring
        ang = math.pi * (1 - t)
        x = cx + math.cos(ang) * half
        y = spring - math.sin(ang) * rise
        y = y - (rise * 0.18) * (1 - abs(math.cos(ang))) ** 3  # sharpen to a point
        off = lobe * (1 - abs(math.sin(math.pi * n_lobes * t)))
        nx_, ny_ = -math.cos(ang), math.sin(ang)
        pts.append((x + nx_ * off, y + ny_ * off))
    by = bottom if bottom is not None else spring + 1000
    return [(x0 + 0, by)] + pts + [(x1, by)]


def plain_arch(x0, x1, spring, apex, n=120, bottom=None):
    return cusped_arch(x0, x1, spring, apex, 1, 0.0, n, bottom)


def lattice_holes(W, H, s, ox=0.0, oy=0.0):
    """8-point star holes on a square grid + small diamond holes between them."""
    polys = []
    r = s * 0.43; d = s * 0.15
    for j in range(-1, int(H / s) + 2):
        for i in range(-1, int(W / s) + 2):
            cx, cy = ox + i * s, oy + j * s
            sq1 = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in [k * math.pi / 2 for k in range(4)]]
            sq2 = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
            polys.append(sq1); polys.append(sq2)
            mx, my = cx + s / 2, cy + s / 2
            polys.append([(mx, my - d), (mx + d, my), (mx, my + d), (mx - d, my)])
    return shapes(W, H, polys, smooth=False)


def carve_shade(stone, holes, k=5.0):
    """Directional bevel from the hole edges: light from upper-left."""
    gy, gx = np.gradient(gaussian_filter(holes, 1.6))
    return np.clip((gx + gy) * k, -1, 1) * stone


def stone_layer(mask, seed, col=RED, col2=RED_L):
    lay = gouache_paint(mask, col, col2, seed=seed, rough=0.8, streak=0.8)
    h, w = mask.shape
    strata = 0.5 + 0.5 * np.sin(np.mgrid[0:h, 0:w][0] / 7.0 + fbm(w, h, seed + 2, 60, 2) * 6)
    speck = fbm(w, h, seed + 4, 3, 2)
    lay[..., :3] *= (0.94 + 0.06 * strata + (speck - 0.5) * 0.12)[..., None]
    return lay


if "jali" in PARTS:
    W, H = 560, 800
    nx = Seq(71100)
    outer = shapes(W, H, [cusped_arch(10, W - 10, 300, 20, 9, 0.0, bottom=H - 6)], smooth=False)
    opening = shapes(W, H, [cusped_arch(58, W - 58, 318, 92, 9, 13.0, bottom=H - 62)], smooth=False)
    frame = np.clip(outer - opening, 0, 1)
    holes = lattice_holes(W, H, 50, ox=(W / 2) % 50, oy=330 % 50) * opening
    # keep a solid stone margin inside the opening edge
    inner_margin = np.clip(gaussian_filter(1 - opening, 4) * 4, 0, 1)
    holes = holes * (1 - (inner_margin > 0.2))
    stone = np.clip(outer - holes, 0, 1)
    art = OV(blank(W, H), stone, lambda m: stone_layer(m, nx()))
    sh = carve_shade(stone, holes + (1 - opening) * 0, 6.0)
    art[..., :3] = np.clip(art[..., :3] * (1 + sh[..., None] * 0.35), 0, 1)
    # hole side walls (thickness of the slab, in shadow)
    side = np.clip(holes - np.roll(np.roll(holes, 4, 0), 3, 1), 0, 1)
    art = OV(art, side, lambda m: gouache_paint(m, "#5a2214", "#6d2a1a", seed=nx(), rough=0.4))
    # frame: carved border + marble inlay lines following the arch
    fr_shade = carve_shade(frame, opening, 4.0)
    art[..., :3] = np.clip(art[..., :3] * (1 + fr_shade[..., None] * 0.3), 0, 1)
    inlay_a = np.clip(shapes(W, H, [cusped_arch(26, W - 26, 306, 44, 9, 0.0, bottom=H - 22)], smooth=False) - shapes(W, H, [cusped_arch(31, W - 31, 308, 50, 9, 0.0, bottom=H - 27)], smooth=False), 0, 1)
    inlay_b = np.clip(shapes(W, H, [cusped_arch(44, W - 44, 312, 70, 9, 6.0, bottom=H - 44)], smooth=False) - shapes(W, H, [cusped_arch(48, W - 48, 314, 76, 9, 7.0, bottom=H - 48)], smooth=False), 0, 1)
    art = OV(art, np.clip(inlay_a + inlay_b, 0, 1), lambda m: gouache_paint(m, MARBLE, "#e2d3b8", seed=nx(), rough=0.5, streak=0.4))
    # weathering: darker stains along the bottom and edges
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, stone * np.clip((yy - 560) / 240, 0, 1) * fbm(W, H, 77, 40, 3), "#5a2414", seed=nx(), density=0.4, edge=0, bloom=0.4, rough=3, feather=3)
    art = add_grain(art, seed=3, amount=0.04)
    preview(art, "jm-jali", bg="#f6c66e")
    save_full(art, f"{OUT}/jali.webp", size=(420, 600), quality=80)
    np.save("/tmp/pen/nb-J3/art/jm-holes.npy", holes[::2, ::2].astype(np.float16))
    clear()

if "light" in PARTS:
    W, H = 420, 760
    nx = Seq(71200)
    art = blank(W, H)
    holes = np.load("/tmp/pen/nb-J3/art/jm-holes.npy").astype(np.float32)  # 280 x 400 (jali at half scale)
    # soft shafts from the screen (upper area) slanting down-right
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shaft = np.zeros((H, W), np.float32)
    for k, (x0, wd) in enumerate([(90, 40), (150, 26), (205, 46), (270, 30), (320, 22)]):
        xc = x0 + (yy - 120) * 0.22
        shaft += np.exp(-((xx - xc) / wd) ** 2) * np.clip((yy - 80) / 120, 0, 1) * np.clip((H - yy) / 240, 0, 1) * (0.5 + 0.5 * k % 2)
    shaft = gaussian_filter(shaft, 6) * 0.5
    # projected lattice on the floor: perspective-squashed, sheared, blurred copy of the holes
    from scipy.ndimage import map_coordinates
    fy0, fy1 = 470, 740
    v = np.clip((yy - fy0) / (fy1 - fy0), 0, 1)
    src_y = 200 + v * 190  # lower part of the jali
    widen = 0.75 + v * 0.7
    src_x = 140 + (xx - W / 2 - (yy - fy0) * 0.25) / widen
    proj = map_coordinates(holes, [src_y, src_x], order=1, mode="constant") * ((yy >= fy0) & (yy <= fy1))
    valid = ((src_x > 30) & (src_x < 250) & (yy >= fy0) & (yy <= fy1)).astype(np.float32)
    proj = gaussian_filter(proj, 1.6) * gaussian_filter(valid, 16) ** 1.5 * np.clip(1 - np.abs(xx - W / 2 - (yy - fy0) * 0.25) / 190, 0, 1) * np.clip((yy - fy0) / 40, 0, 1) * np.clip((fy1 - yy) / 60, 0, 1)
    a = np.clip(shaft + proj * 0.75, 0, 1)
    art = rgba("#ffe2a3", a)
    art[..., :3] = np.clip(art[..., :3] * (0.95 + 0.1 * fbm(W, H, 5, 40, 2))[..., None], 0, 1)
    preview(art, "jm-light", bg="#7d321f")
    save_full(art, f"{OUT}/light.webp", size=(420, 760), quality=74)
    clear()

if "frame" in PARTS:
    W, H = 520, 700
    nx = Seq(71300)
    outer = shapes(W, H, [cusped_arch(6, W - 6, 260, 8, 9, 0.0, bottom=H - 4)], smooth=False)
    opening = shapes(W, H, [cusped_arch(40, W - 40, 276, 68, 9, 12.0, bottom=H - 40)], smooth=False)
    frame = np.clip(outer - opening, 0, 1)
    art = OV(blank(W, H), frame, lambda m: stone_layer(m, nx()))
    sh = carve_shade(frame, opening, 4.0)
    art[..., :3] = np.clip(art[..., :3] * (1 + sh[..., None] * 0.35), 0, 1)
    inl = np.clip(shapes(W, H, [cusped_arch(20, W - 20, 266, 34, 9, 0.0, bottom=H - 18)], smooth=False) - shapes(W, H, [cusped_arch(25, W - 25, 268, 40, 9, 0.0, bottom=H - 23)], smooth=False), 0, 1)
    art = OV(art, inl, lambda m: gouache_paint(m, MARBLE, "#e2d3b8", seed=nx(), rough=0.5))
    # inlaid chevrons on the jambs
    chev = []
    for y in range(300, H - 40, 26):
        for x in (23, W - 23):
            chev.append([(x - 7, y), (x, y - 7), (x + 7, y), (x, y + 7)])
    art = OV(art, shapes(W, H, chev, smooth=False), lambda m: gouache_paint(m, MARBLE, seed=nx(), rough=0.4))
    art = add_grain(art, seed=4, amount=0.035)
    preview(art, "jm-frame", bg="#d8b48a")
    save_full(art, f"{OUT}/frame.webp", size=(390, 525), quality=80)
    clear()

if "chhatri" in PARTS:
    W, H = 320, 380
    nx = Seq(71400); cx = 160
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    # plinth
    plinth = shapes(W, H, [[(40, 372), (40, 344), (280, 344), (280, 372)]], smooth=False)
    # four (visible: three) pillars
    pillars = shapes(W, H, [[(x - 9, 344), (x - 7, 226), (x + 7, 226), (x + 9, 344)] for x in (70, 160, 250)], smooth=False)
    # brackets + chajja (sloping eave)
    chajja = shapes(W, H, [[(22, 226), (54, 206), (266, 206), (298, 226), (290, 232), (30, 232)]], smooth=False)
    # drum + dome + finial
    drum = shapes(W, H, [[(78, 206), (78, 186), (242, 186), (242, 206)]], smooth=False)
    dome_pts = [(cx + math.cos(a) * 78, 186 - math.sin(a) * 96) for a in np.linspace(0, math.pi, 60)]
    dome_pts = [(x, y - 14 * max(0, 1 - abs(x - cx) / 40) ** 2) for x, y in dome_pts]
    dome = shapes(W, H, [dome_pts], smooth=True)
    fin = shapes(W, H, [[(cx - 3, 80), (cx - 3, 40), (cx + 3, 40), (cx + 3, 80)]], smooth=False) + circles(W, H, [(cx, 70, 8), (cx, 52, 6), (cx, 36, 4)])
    arches = shapes(W, H, [plain_arch(x0 + 6, x1 - 6, 270, 240, bottom=344) for (x0, x1) in [(79, 151), (169, 241)]], smooth=False)
    for m, c, c2 in [(plinth, RED_D, "#8f3b25"), (pillars, RED, RED_L), (drum, "#a8492f", RED), (dome, RED, "#d07a56"), (chajja, "#9c4329", RED)]:
        art = OV(art, m, lambda mm, c=c, c2=c2: stone_layer(mm, nx(), c, c2))
    # dark interior seen through the arches
    art = OV(art, arches * (1 - pillars), lambda m: gouache_paint(m, "#4a1c10", "#5e2416", seed=nx(), rough=0.5))
    # dome shading (light from upper-left) and ribs
    art = G(art, dome * np.clip((xx - cx + 20) / 80, 0, 1), "#6d2716", seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1.5, feather=2)
    art = G(art, dome * np.clip((cx - 30 - xx) / 50, 0, 1), "#f3c49c", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1.5, feather=2)
    ribs = strokes(W, H, [(curve([(cx + o * 78, 186), (cx + o * 52, 130), (cx + o * 8, 92)], 20), 1.4, None) for o in (-0.62, -0.25, 0.25, 0.62)]) * dome
    art = G(art, ribs, "#7d321f", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = OV(art, fin, lambda m: foil(m, "#c9a24e", seed=nx(), emboss=0.5, sparkle=0.1))
    # inlay frieze on the drum
    fr = shapes(W, H, [[(x, 196), (x + 6, 190), (x + 12, 196), (x + 6, 202)] for x in range(84, 236, 16)], smooth=False)
    art = OV(art, fr, lambda m: gouache_paint(m, MARBLE, seed=nx(), rough=0.4))
    art = G(art, chajja * np.clip((yy - 226) / 6, 0, 1), "#4a1c10", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=1)
    art = G(art, ellipses(W, H, [(cx + 8, 376, 140, 6, 0)]), "#3a1a10", seed=nx(), density=0.3, edge=0, bloom=0, rough=2, feather=3)
    art = add_grain(art, seed=6, amount=0.035)
    preview(art, "jm-chhatri", bg="#f4e4c8")
    save(art, f"{OUT}/chhatri.webp", max_w=200, quality=84)
    clear()

if "stone" in PARTS:
    W, H = 256, 256
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#a44a31"), np.float32)
    n1 = wrap_noise(W, H, 3, 18); n2 = wrap_noise(W, H, 5, 1.0); n3 = wrap_noise(W, H, 9, 5)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    strata = 0.5 + 0.5 * np.sin(2 * math.pi * (yy / H * 6 + n1 * 1.5))
    rgb = base * (0.95 + 0.04 * strata + 0.16 * (n2 - 0.5) + 0.07 * (n3 - 0.5))[..., None]
    save_rgb(np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1), f"{OUT}/stone.webp", quality=72)

if "band" in PARTS:
    W, H = 320, 40
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#9a4129"), np.float32)
    n = wrap_noise(W, H, 4, 1.0)
    cv = Canvas(W, H); p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    step = 40
    for i in range(0, W // step + 1):
        x = i * step + step / 2
        pts = [(x + math.cos(k * math.pi / 4) * (13 if k % 2 == 0 else 6), 20 + math.sin(k * math.pi / 4) * (13 if k % 2 == 0 else 6)) for k in range(8)]
        cv.c.drawPath(poly_path(pts), p)
        cv.c.drawRect(skia.Rect(i * step - 2, 18, i * step + 2, 22), p)
    cv.c.drawRect(skia.Rect(0, 3, W, 5), p); cv.c.drawRect(skia.Rect(0, 35, W, 37), p)
    m = periodic_blur(cv.array()[..., 3], 0.5)
    mar = np.array(hex_rgb(MARBLE), np.float32) * (0.94 + 0.08 * wrap_noise(W, H, 8, 3))[..., None]
    rgb = base * (0.92 + 0.12 * n)[..., None] * (1 - m[..., None]) + mar * m[..., None]
    # carved groove shadow under the inlay
    sh = np.roll(m, 1, 0) * (1 - m)
    rgb *= (1 - 0.3 * sh)[..., None]
    save_full(np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1), f"{OUT}/band.webp", quality=82)

if "divider" in PARTS:
    W, H = 360, 50
    nx = Seq(71500)
    art = blank(W, H)
    line = strokes(W, H, [([(20, 25), (140, 25)], 2.0, (0.6, 0.0)), ([(220, 25), (340, 25)], 2.0, (0.0, 0.6))])
    art = OV(art, line, lambda m: gouache_paint(m, RED, seed=nx(), rough=0.4))
    lozenge = shapes(W, H, [[(180, 2), (212, 25), (180, 48), (148, 25)]], smooth=False)
    art = OV(art, lozenge, lambda m: stone_layer(m, nx()))
    star = shapes(W, H, [[(180 + math.cos(k * math.pi / 8) * (14 if k % 2 == 0 else 6), 25 + math.sin(k * math.pi / 8) * (14 if k % 2 == 0 else 6)) for k in range(16)]], smooth=False)
    art = OV(art, star, lambda m: gouache_paint(m, MARBLE, seed=nx(), rough=0.3))
    for x in (132, 228):
        art = OV(art, shapes(W, H, [[(x, 19), (x + 6, 25), (x, 31), (x - 6, 25)]], smooth=False), lambda m: gouache_paint(m, RED_D, seed=nx(), rough=0.3))
    preview(art, "jm-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)

kb(OUT)
