"""Sumba Hinggi — adat Sumba Timur: hinggi ikat bands (horse, rooster, deer, shrimp stylised as on the cloth, with
feathered resist-dye edges) on kombu red, a stepped-lozenge band, tassel fringe, and a gouache savanna with tall-peaked
uma mbatangu houses and grazing sandalwood horses.
Run: python3 -I sumba-hinggi.py [part ...]  parts: figs geo fringe kuda sabana
Assets -> public/themes/art/sumba-hinggi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g2_lib import *

OUT = outdir("sumba-hinggi")
PARTS = sys.argv[1:] or ["figs", "geo", "fringe", "kuda", "sabana"]
KOMBU, KOMBU_D, KOMBU_L = "#7d2f1e", "#5e2114", "#9a4428"
CREAM, CREAM_D = "#ecdcbc", "#d9c39c"
INDIGO, INDIGO_L = "#28324d", "#3e4b6c"
KUNING = "#c99a3e"


def cloth(W, H, base, seed, wrap=True):
    """Woven cotton ground: warp/weft thread texture + slow dye unevenness (tileable when wrap)."""
    warp = lin_field(W, H, seed, (0, 1), 40, 0.45, wrap)
    weft = lin_field(W, H, seed + 1, (1, 0), 40, 0.45, wrap)
    xx = np.arange(W)[None, :].astype(np.float32); yy = np.arange(H)[:, None].astype(np.float32)
    rib = (0.5 + 0.5 * np.sin(xx * math.pi / 1.6)) * 0.5 + (0.5 + 0.5 * np.sin(yy * math.pi / 1.8)) * 0.5
    dye = wrapn(W, H, seed + 2, 30) if wrap else fbm(W, H, seed + 2, 80, 3)
    rgb = rgb_of(base)[None, None, :] * (1 + warp[..., None] * 0.035 + weft[..., None] * 0.03 + (rib[..., None] - 0.5) * 0.07 + (dye[..., None] - 0.5) * 0.12)
    return opaque(rgb)


def horse(ox, oy, s=1.0, face=1):
    """Hinggi horse: long box body, arched neck, small wedge head, stiff legs, flowing tail. Returns (body polys, leg strokes)."""
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    body = [P(-42, -6), P(-30, -14), P(18, -14), P(30, -10), P(34, 4), P(26, 14), P(-30, 14), P(-44, 6)]
    neck = [P(18, -12), P(28, -26), P(36, -36), P(46, -38), P(48, -28), P(38, -16), P(34, -4)]
    head = [P(38, -40), P(52, -38), P(64, -28), P(62, -20), P(52, -22), P(44, -28)]
    ear = [P(40, -38), P(42, -48), P(47, -39)]
    mane = [P(20, -14), P(24, -26), P(32, -38), P(36, -36), P(28, -24), P(24, -10)]
    tail = [P(-42, -8), P(-54, -2), P(-60, 16), P(-56, 30), P(-50, 14), P(-46, 2)]
    legs = [[P(-34, 12), P(-38, 30), P(-36, 44)], [P(-22, 12), P(-20, 30), P(-24, 44)], [P(16, 12), P(14, 30), P(18, 44)], [P(26, 12), P(30, 30), P(28, 44)]]
    return [body, neck, head, ear, tail, mane], legs


def rooster(ox, oy, s=1.0, face=1):
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    body = [P(-22, -6), P(-4, -18), P(16, -16), P(24, -4), P(16, 12), P(-10, 14), P(-24, 6)]
    neck = [P(10, -16), P(18, -34), P(28, -40), P(32, -32), P(24, -14)]
    comb = [P(20, -40), P(22, -48), P(26, -42), P(28, -50), P(31, -42), P(34, -46), P(33, -36)]
    beak = [P(31, -36), P(40, -33), P(31, -31)]
    tail = [P(-18, -6), P(-30, -36), P(-40, -48), P(-50, -46), P(-44, -34), P(-38, -14), P(-26, 8)]
    legs = [[P(-4, 12), P(-6, 30), P(-12, 34)], [P(6, 12), P(8, 30), P(14, 34)]]
    return [body, neck, comb, beak, tail], legs


def deer(ox, oy, s=1.0, face=1):
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    body = [P(-34, -6), P(-24, -12), P(20, -12), P(28, -4), P(24, 10), P(-26, 10), P(-36, 2)]
    neck = [P(16, -10), P(26, -28), P(32, -36), P(38, -30), P(28, -8)]
    head = [P(30, -38), P(48, -32), P(46, -26), P(32, -28)]
    tail = [P(-34, -4), P(-42, -10), P(-40, 0)]
    legs = [[P(-26, 8), P(-28, 26), P(-28, 40)], [P(-16, 8), P(-14, 26), P(-16, 40)], [P(12, 8), P(12, 26), P(14, 40)], [P(20, 8), P(24, 26), P(22, 40)]]
    antl = [[P(32, -38), P(28, -54), P(20, -64)], [P(29, -50), P(36, -60)], [P(25, -58), P(22, -70)], [P(34, -38), P(40, -52), P(48, -58)], [P(40, -50), P(46, -46)]]
    return [body, neck, head, tail], legs + antl


def shrimp(ox, oy, s=1.0, face=1):
    """Curled shrimp (udang): a C-shaped segmented body (drawn as a thick tapering stroke), fan tail, antennae, legs."""
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    spine = [P(math.cos(a) * 26, -math.sin(a) * 22 + 6) for a in [math.pi * (1.05 - 0.9 * t / 14) for t in range(15)]]
    body = [(spine, 18 * s, (0.0, 0.55))]
    head = [P(-34, -2), P(-24, -14), P(-14, -8), P(-16, 6), P(-30, 8)]
    tailfan = [P(22, 22), P(34, 26), P(30, 40), P(22, 34), P(16, 40), P(14, 28)]
    lines = [[P(-32, -6), P(-48, -26), P(-44, -46), P(-28, -54)], [P(-30, -2), P(-54, -10), P(-60, -28)],
             [P(-14, 10), P(-18, 24)], [P(-6, 14), P(-6, 28)], [P(2, 16), P(6, 28)], [P(10, 16), P(16, 26)]]
    return [head, tailfan], lines, body


def paint_fig(art, W, H, polys, lines, nx, s=1.0, fill=CREAM, detail=INDIGO, accent=KUNING, rng=None, extra=None):
    m = np.maximum(shapes(W, H, polys, smooth=False), strokes(W, H, [(l, 5.5 * s, None) for l in lines]))
    if extra:
        m = np.maximum(m, strokes(W, H, extra))
    art = IK(art, m, fill, seed=nx(), bleed=3.2 * s)
    # inner pattern: indigo zigzag/bars through the body, ochre dots
    inner = np.clip(m - (gaussian_filter(m, 3 * s) < 0.9), 0, 1)
    b = bbox(m, 0)
    if b is not None:
        y0, y1, x0, x1 = b
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        zig = (np.abs(((xx - x0) / (7 * s)) % 2 - 1) * 6 * s + (yy - y0)) % (12 * s) < 4.2 * s
        det = zig.astype(np.float32) * inner * (gaussian_filter(m, 4 * s) > 0.98)
        art = IK(art, det, detail, seed=nx(), bleed=2.0 * s)
        dts = (((xx - x0) % (11 * s)) < 3.2 * s) & (((yy - y0) % (11 * s)) < 3.2 * s)
        art = IK(art, dts.astype(np.float32) * (gaussian_filter(m, 5 * s) > 0.99) * (1 - det), accent, seed=nx(), bleed=1.5 * s)
    return art


if "figs" in PARTS:
    # one repeat of the figure band: horse, rooster, deer, shrimp (seamless along x)
    P_, Hh = 720, 170
    nx = Seq(40100)
    art = cloth(P_, Hh, KOMBU, 7)
    # border lines (indigo + cream threads) top and bottom
    for y, c, wd in ((8, INDIGO, 5), (16, CREAM, 2.4), (Hh - 9, INDIGO, 5), (Hh - 17, CREAM, 2.4)):
        art = IK(art, strokes(P_, Hh, [([(-20, y), (P_ + 20, y)], wd, None)]), c, seed=nx(), bleed=1.2, pad=4)
    cy = 92
    for k, (fn, x, face) in enumerate([(horse, 92, 1), (rooster, 270, 1), (deer, 448, -1), (shrimp, 620, 1)]):
        r = fn(x, cy, 1.15, face)
        art = paint_fig(art, P_, Hh, r[0], r[1], nx, 1.15, extra=r[2] if len(r) > 2 else None)
        clear()
    # small cross-stars between figures
    stars = []
    for x in (180, 362, 540, 0, P_):
        for dy in (-18, 18):
            stars.append(([(x - 6, cy + dy), (x + 6, cy + dy)], 3, None)); stars.append(([(x, cy + dy - 6), (x, cy + dy + 6)], 3, None))
    art = IK(art, strokes(P_, Hh, stars), KUNING, seed=nx(), bleed=1.4, pad=4)
    to_image(np.tile(art, (1, 2, 1))).convert("RGB").save(f"{PREV}/figs-2x.png")
    save_rgb(art, f"{OUT}/figs.webp", quality=76)
    clear()

if "geo" in PARTS:
    # stepped lozenge (kaliuda-style) band, seamless along x
    P_, Hh = 360, 64
    nx = Seq(40200)
    art = cloth(P_, Hh, INDIGO, 11)
    loz, inner, core = [], [], []
    for k in range(6):
        cx = 30 + k * 60
        for sc, lst in ((26, loz), (16, inner), (6, core)):
            pts = []
            for a in range(4):
                ang = a * math.pi / 2
                # stepped diamond: corners with two steps
                pts.append((cx + math.cos(ang) * sc, 32 + math.sin(ang) * sc * 0.95))
            lst.append(pts)
    art = IK(art, shapes(P_, Hh, loz, smooth=False), KOMBU_L, seed=nx(), bleed=2.2, pad=4)
    art = IK(art, shapes(P_, Hh, inner, smooth=False), CREAM, seed=nx(), bleed=2.0, pad=4)
    art = IK(art, shapes(P_, Hh, core, smooth=False), KUNING, seed=nx(), bleed=1.4, pad=4)
    hooks = []
    for k in range(7):
        x = k * 60
        hooks += [([(x - 10, 14), (x, 4), (x + 10, 14)], 3, None), ([(x - 10, 50), (x, 60), (x + 10, 50)], 3, None)]
    art = IK(art, strokes(P_, Hh, hooks), CREAM, seed=nx(), bleed=1.4, pad=4)
    to_image(np.tile(art, (1, 2, 1))).convert("RGB").save(f"{PREV}/geo-2x.png")
    save_rgb(art, f"{OUT}/geo.webp", quality=78)
    clear()

if "fringe" in PARTS:
    # twisted warp-end fringe with knotted tassels (repeat-x)
    P_, Hh = 240, 90
    nx = Seq(40300); rng = random.Random(3)
    art = blank(P_, Hh)
    art = over(art, cloth(P_, 12, KOMBU_D, 13) if False else art)
    head = shapes(P_, Hh, [[(-4, 0), (P_ + 4, 0), (P_ + 4, 10), (-4, 10)]], smooth=False)
    art = OV(art, head, lambda m: np.concatenate([cloth(m.shape[1], m.shape[0], KOMBU_D, 13)[..., :3], m[..., None]], -1), pad=0)
    for k in range(30):
        x = 4 + k * 8
        L = 66 + rng.uniform(-6, 6)
        sw = rng.uniform(-3, 3)
        cord = strokes(P_, Hh, [(curve([(x, 8), (x + sw * 0.5, 30), (x + sw, 8 + L)], 16), 6.4, (0.0, 0.35))])
        c = [CREAM, CREAM_D, KOMBU_L, CREAM, CREAM_D, INDIGO_L][k % 6]
        art = GP(art, cord, c, mix(c, "#000000", 0.15), seed=nx(), rough=0.4, streak=1.2, pad=4)
        tw = strokes(P_, Hh, [([(x - 2, 10 + j * 6), (x + 2, 14 + j * 6)], 0.9, None) for j in range(10)]) * cord
        art = OV(art, tw, lambda m: col_arr(m, "#3a1a10", m * 0.35), pad=3)
        art = GP(art, ellipses(P_, Hh, [(x + sw * 0.3, 26, 4.6, 4.0, 0)]), mix(c, "#000000", 0.25), seed=nx(), rough=0.3, pad=4)
    to_image(np.tile(art, (1, 2, 1))).save(f"{PREV}/fringe-2x.png")
    im = to_image(art); im.save(f"{OUT}/fringe.webp", "WEBP", quality=80, method=6)
    print("fringe", im.size, os.path.getsize(f"{OUT}/fringe.webp") // 1024, "KB")
    clear()

if "kuda" in PARTS:
    # one large ikat horse on a small kombu patch with feathered edges (emblem)
    W, H = 400, 340
    nx = Seq(40400)
    patch = shapes(W, H, [deform([(30, 30), (370, 26), (376, 310), (24, 314)], random.Random(4), 2, 0.01)], smooth=False)
    art = blank(W, H)
    base = cloth(W, H, KOMBU, 17, wrap=False)
    pm = ikat(patch, KOMBU, seed=nx(), bleed=6)
    pm[..., :3] = base[..., :3] * 0.6 + pm[..., :3] * 0.4
    art = over(art, pm)
    for y, c, wd in ((48, INDIGO, 5), (58, CREAM, 2.4), (296, INDIGO, 5), (286, CREAM, 2.4)):
        art = IK(art, strokes(W, H, [([(36, y), (364, y)], wd, None)]), c, seed=nx(), bleed=1.4, pad=4)
    polys, lines = horse(200, 178, 2.3, 1)
    art = paint_fig(art, W, H, polys, lines, nx, 2.3)
    preview(art, "kuda", tone="#f1e3c6")
    save(art, f"{OUT}/kuda.webp", max_w=300, quality=82)
    clear()


def uma(art, W, H, cx, by, s, nx, rng, dark=False):
    """Uma mbatangu: stilted house, broad hipped thatch roof with a tall steep central tower (menara)."""
    def P(x, y):
        return (cx + x * s, by + y * s)
    stilts = strokes(W, H, [([P(x, 0), P(x, -22)], 3.2 * s, None) for x in (-30, -14, 2, 18, 32)])
    art = GP(art, stilts, "#4a2e1c", seed=nx(), rough=0.4, pad=6)
    deck = shapes(W, H, [[P(-40, -20), P(40, -20), P(40, -26), P(-40, -26)]], smooth=False)
    art = GP(art, deck, "#6b4a2c", seed=nx(), rough=0.5, pad=6)
    wall = shapes(W, H, [[P(-34, -26), P(34, -26), P(34, -40), P(-34, -40)]], smooth=False)
    art = GP(art, wall, "#8a6a44", "#7a5a38", seed=nx(), rough=0.6, pad=6)
    art = crayon(art, strokes(W, H, [([P(-34 + k * 7, -40), P(-34 + k * 7, -26)], 1.0, None) for k in range(11)]) * wall, "#5a3e24", seed=nx(), amt=0.5)
    low = [P(-60, -34), P(-38, -58), P(-14, -64), P(14, -64), P(38, -58), P(60, -34), P(40, -38), P(-40, -38)]
    tower = [P(-16, -62), P(-11, -96), P(-6, -128), P(-3, -148), P(3, -148), P(6, -128), P(11, -96), P(16, -62)]
    th = "#9a8250" if not dark else "#7f6a42"
    roof = np.maximum(shapes(W, H, [low], smooth=False), shapes(W, H, [tower], smooth=False))
    art = GP(art, roof, th, mix(th, "#5a4428", 0.3), seed=nx(), rough=1.4, streak=1.6)
    art = tint(art, side_light(roof, -8 * s, 0, 4), "#cdb57a", 0.5, seed=nx())
    art = tint(art, side_light(roof, 6 * s, 0, 4), "#4a3a22", 0.4, seed=nx())
    # thatch lines
    ln = []
    for k in range(16):
        t = k / 15
        ln.append(([P(-58 + 116 * t, -35), P(-12 + 24 * t, -63)], 0.9, None))
    for k in range(9):
        y = -66 - k * 9
        w2 = 15 - k * 1.4
        ln.append(([P(-w2, y), P(w2, y)], 0.9, None))
    art = crayon(art, strokes(W, H, ln) * roof, "#5e4a2a", seed=nx(), amt=0.45, tooth=0.4)
    art = crayon(art, inner_edge(roof, 1.6), "#4a3a22", seed=nx(), amt=0.55, tooth=0.4)
    # ridge finials: two thin crossed sticks on the tower top
    art = GP(art, strokes(W, H, [([P(-2, -146), P(-7, -160)], 2.0 * s, None), ([P(2, -146), P(7, -160)], 2.0 * s, None)]), "#3a2a18", seed=nx(), rough=0.3, pad=6)
    return art


def sandel(art, W, H, ox, oy, s, face, nx, col, col2, grazing=True):
    """Sandalwood pony in gouache: slim body, arched neck lowered to graze (or raised), dark mane & tail."""
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    body = shapes(W, H, [[P(-30, -36), P(-12, -42), P(16, -42), P(28, -36), P(30, -24), P(22, -16), P(-24, -16), P(-32, -24)]])
    if grazing:
        neck = shapes(W, H, [[P(18, -40), P(32, -38), P(44, -20), P(50, -4), P(44, -2), P(34, -18), P(22, -24)]])
        head = shapes(W, H, [[P(42, -8), P(54, -6), P(58, 2), P(50, 4), P(42, 0)]])
        mane = strokes(W, H, [([P(20, -42), P(32, -40), P(44, -22)], 4 * s, (0.1, 0.4))])
    else:
        neck = shapes(W, H, [[P(14, -40), P(24, -54), P(32, -60), P(40, -56), P(34, -40), P(28, -26)]])
        head = shapes(W, H, [[P(30, -62), P(40, -60), P(52, -48), P(48, -42), P(38, -46), P(32, -52)]])
        mane = strokes(W, H, [([P(16, -42), P(24, -54), P(30, -60)], 4.5 * s, (0.1, 0.4))])
    legs = strokes(W, H, [([P(x, -22), P(x + d, -6), P(x + d * 0.5, 8)], 6.5 * s, (0.0, 0.3)) for x, d in ((-24, -2), (-16, 2), (14, -1), (22, 3))])
    tail = strokes(W, H, [(curve([P(-30, -36), P(-40, -28), P(-42, -8)], 12), 6 * s, (0.1, 0.8))])
    full = np.clip(body + neck + head + legs, 0, 1)
    art = G(art, shapes(W, H, [ellipse_pts(ox, oy + 9 * s, 46 * s, 5 * s, 16)]), "#5a4420", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=4)
    art = GP(art, full, col, col2, seed=nx(), rough=0.9, streak=1.2)
    art = tint(art, side_light(full, -3, -4, 3), mix(col, "#ffffff", 0.3), 0.45, seed=nx())
    art = tint(art, side_light(full, 3, 4, 3), mix(col, "#000000", 0.35), 0.5, seed=nx())
    art = GP(art, np.clip(mane + tail, 0, 1), "#2a1a10", seed=nx(), rough=0.6, streak=1.4)
    return art


if "sabana" in PARTS:
    W, H = 840, 600
    nx = Seq(40500); rng = random.Random(23)
    art = blank(W, H)
    far = hills(W, H, 250, 30, 3, 0.9)
    art = G(art, far, "#c9a77a", "#d6b88c", seed=nx(), density=0.55, edge=0.35, bloom=0.35, rough=6, feather=3)
    mid = hills(W, H, 300, 36, 8, 0.6)
    art = G(art, mid, "#bf9a4f", "#cfa95c", seed=nx(), density=0.75, edge=0.45, bloom=0.3, rough=6, feather=2)
    # dark green valley patches + lone trees
    patches = []
    for k in range(9):
        x = rng.uniform(0, W); y = rng.uniform(300, 360)
        patches.append(deform(ellipse_pts(x, y, rng.uniform(26, 60), rng.uniform(7, 12), 12), rng, 1, 0.15))
    art = G(art, shapes(W, H, patches) * mid, "#6e7a3c", seed=nx(), density=0.45, edge=0.4, bloom=0.3, rough=5, feather=3)
    near = hills(W, H, 400, 30, 14, 1.1)
    art = GP(art, near, "#d7b263", "#c99f4c", seed=nx(), rough=2.4, streak=1.6)
    art = tint(art, side_light(near, 0, -18, 10), "#a8803a", 0.45, seed=nx())
    art = G(art, near * (fbm(W, H, 555, 70, 3) > 0.52), "#b08a3e", seed=nx(), density=0.25, edge=0.2, bloom=0.3, rough=8, feather=5)
    # kampung on the mid ridge: three uma
    for cx, by, sc, dk in ((560, 336, 0.62, True), (640, 330, 0.8, False), (730, 340, 0.68, True)):
        art = uma(art, W, H, cx, by, sc, nx, rng, dk)
        clear()
    trees = []
    for x, y, r in ((120, 322, 20), (150, 330, 14), (420, 318, 16)):
        trees.append(deform(ellipse_pts(x, y - r, r * 1.2, r, 12), rng, 2, 0.12))
    tm = shapes(W, H, trees)
    art = GP(art, strokes(W, H, [([(x, y), (x, y - r * 0.6)], 3, None) for x, y, r in ((120, 322, 20), (150, 330, 14), (420, 318, 16))]), "#4a3420", seed=nx(), rough=0.4, pad=6)
    art = G(art, tm, "#55622e", "#6a7a3a", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=3, feather=1.2)
    # grazing horses in the foreground
    art = sandel(art, W, H, 230, 486, 1.55, 1, nx, "#8a5a30", "#7a4c28", True)
    art = sandel(art, W, H, 430, 460, 1.2, -1, nx, "#c9a274", "#b88e60", False)
    # grass tufts
    tufts = []
    for _ in range(900):
        x = rng.uniform(-10, W + 10); y = rng.uniform(405, H + 5)
        L = 3 + (y - 400) / 200 * 12
        for d in (-0.25, 0.08):
            a = -math.pi / 2 + d + rng.uniform(-.25, .25)
            tufts.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], 0.8 + (y - 400) / 200 * 0.9, (0.0, 0.85)))
    tmk = strokes(W, H, tufts) * near
    art = GP(art, tmk * (fbm(W, H, nx(), 20, 2) > 0.45), "#a8803a", seed=nx(), rough=0.3, pad=4, density=0.7)
    art = GP(art, np.roll(tmk, -2, 0) * (fbm(W, H, nx(), 20, 2) > 0.55), "#ecd08a", seed=nx(), rough=0.3, pad=4, density=0.7)
    preview(art, "sabana", tone="#f4dcb0")
    save(art, f"{OUT}/sabana.webp", max_w=780, quality=78)
    clear()
