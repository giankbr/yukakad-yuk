"""Pua Kumbu — Iban warp-ikat textile (engkudu red-brown, black, undyed cream) with hooked lozenges, paku ferns and
baya (crocodile) figures, a rumah betang on the Kapuas river. Run: python3 -I pua-kumbu.py [part ...]
parts: kain betang band motif weave divider. Assets -> public/themes/art/pua-kumbu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l2_lib import *

OUT = outdir("pua-kumbu")
PARTS = sys.argv[1:] or ["kain", "betang", "band", "motif", "weave", "divider"]
RED, RED_D, RED_L = "#7a2e1c", "#5e2214", "#8e3c24"
BLACK = "#1c1310"
CREAM, CREAM_D = "#eadbbd", "#d9c39a"
OCHRE = "#b9853f"


def shrink(rx, ry, d):
    k = math.hypot(rx, ry)
    return rx - d * k / ry, ry - d * k / rx


def medallion(W, H, cx, cy, rx, ry):
    """Hooked lozenge: cream rings, black bands, hooks along the contour. Returns (cream, black) masks."""
    cream = []; black = []
    rings = [(0, 9), (24, 31), (50, 56)]
    for d0, d1 in rings:
        a = shrink(rx, ry, d0); b = shrink(rx, ry, d1)
        cream.append(ring_poly(W, H, diamond(cx, cy, *a), diamond(cx, cy, *b)))
    a = shrink(rx, ry, 9); b = shrink(rx, ry, 24)
    black.append(ring_poly(W, H, diamond(cx, cy, *a), diamond(cx, cy, *b)))
    ci = shrink(rx, ry, 80)
    black.append(shapes(W, H, [diamond(cx, cy, *ci)], smooth=False))
    cream.append(shapes(W, H, [diamond(cx, cy, ci[0] * 0.42, ci[1] * 0.42)], smooth=False))
    # four tiny eyes inside the inner field
    eyes = []
    for sx, sy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        e = shrink(rx, ry, 66)
        eyes.append(diamond(cx + sx * e[0] * 0.9, cy + sy * e[1] * 0.9, 7, 9))
    cream.append(shapes(W, H, eyes, smooth=False))
    items = []
    # ram-horn hooks at the 4 vertices
    for vx, vy, ang in [(cx, cy - ry, -math.pi / 2), (cx, cy + ry, math.pi / 2), (cx - rx, cy, math.pi), (cx + rx, cy, 0)]:
        ex, ey = vx + math.cos(ang) * 22, vy + math.sin(ang) * 22
        items.append(([(vx, vy), (ex, ey)], 9, None))
        for side in (-1, 1):
            pa = ang + side * math.pi / 2
            hc = (ex + math.cos(pa) * 14, ey + math.sin(pa) * 14)
            items.append((hook(hc[0], hc[1], 14, ang + side * math.pi / 2 + math.pi, d=-side, turns=1.1), 7, (0.0, 0.5)))
    # hooks along each edge, pointing outward
    V = diamond(cx, cy, rx, ry)
    for i in range(4):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % 4]
        nxn, nyn = (y1 - y0), -(x1 - x0)
        L = math.hypot(nxn, nyn); nxn /= L; nyn /= L
        mxx, myy = (x0 + x1) / 2, (y0 + y1) / 2
        if nxn * (mxx - cx) + nyn * (myy - cy) < 0:
            nxn, nyn = -nxn, -nyn
        for t in (0.3, 0.5, 0.7):
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            qx, qy = px + nxn * 18, py + nyn * 18
            items.append(([(px, py), (qx, qy)], 7, None))
            ang = math.atan2(nyn, nxn)
            d = 1 if t < 0.5 else -1
            hc = (qx + math.cos(ang + d * math.pi / 2) * 9, qy + math.sin(ang + d * math.pi / 2) * 9)
            items.append((hook(hc[0], hc[1], 9, ang - d * math.pi / 2, d=d, turns=1.0, n=24), 5.5, (0.0, 0.5)))
    cream.append(strokes(W, H, items))
    return np.maximum.reduce(cream), np.maximum.reduce(black)


def fern(W, H, x, y0, y1, side, s=1.0):
    """Paku: wavy stem with alternating fronds ending in fiddlehead curls (one side = facing)."""
    items = []
    stem = curve([(x, y0), (x + 8 * side, (y0 * 2 + y1) / 3), (x - 6 * side, (y0 + 2 * y1) / 3), (x, y1)], 40)
    items.append((stem, 6 * s, (0.05, 0.05)))
    top = stem[0]
    items.append((hook(top[0] + 12 * side, top[1], 12, math.pi if side > 0 else 0, d=side, turns=1.2), 6 * s, (0.0, 0.5)))
    for k, (px, py, a) in enumerate(along(stem, 38)):
        if k == 0:
            continue
        d = 1 if k % 2 else -1
        ex, ey = px + d * 30 * s, py - 16 * s
        items.append((curve([(px, py), (px + d * 16 * s, py - 4 * s), (ex, ey)], 12), 5 * s, (0.0, 0.2)))
        items.append((hook(ex, ey - 8 * s, 8 * s, math.pi / 2, d=d, turns=1.0, n=22), 4.5 * s, (0.0, 0.5)))
    return strokes(W, H, items)


def baya(W, H, x, y, s, face=1):
    """Stylised crocodile (baya): long black body with cream contour, curled tail, bent legs with curled toes."""
    def P(u, v):
        return (x + u * s * face, y + v * s)
    body = [P(-1.0, 0.0), P(-0.7, -0.16), P(-0.2, -0.22), P(0.35, -0.2), P(0.7, -0.14), P(1.0, -0.04), P(1.12, 0.02),
            P(1.0, 0.08), P(0.7, 0.14), P(0.35, 0.2), P(-0.2, 0.2), P(-0.7, 0.14)]
    bm = shapes(W, H, [body])
    rim = np.clip((gaussian_filter(bm, 4.0) > 0.12).astype(np.float32) - bm, 0, 1)
    items = []
    tail = curve([P(-1.0, 0.0), P(-1.3, 0.05), P(-1.5, -0.05)], 16)
    items.append((tail, 0.12 * s, (0.0, 0.3)))
    tc = P(-1.5, -0.05)
    items.append((hook(tc[0] - 0.0, tc[1] - 0.1 * s, 0.1 * s, math.pi / 2, d=face, turns=1.3), 0.07 * s, (0.0, 0.5)))
    legs = []
    for u, up in [(-0.45, -1), (-0.45, 1), (0.5, -1), (0.5, 1)]:
        knee = P(u + 0.12, up * 0.42)
        foot = P(u - 0.06, up * 0.62)
        legs.append(([P(u, up * 0.16), knee, foot], 0.09 * s, None))
        legs.append((hook(foot[0] - 0.07 * s * face, foot[1], 0.07 * s, 0, d=up * face, turns=1.1, n=20), 0.05 * s, (0.0, 0.5)))
    items += legs
    lm = strokes(W, H, items)
    # back spines (small cream ticks along the body) and an eye
    ticks = []
    for u in np.linspace(-0.75, 0.8, 9):
        ticks.append(([P(u, -0.05), P(u + 0.04, 0.05)], 0.035 * s, None))
    tk = strokes(W, H, ticks)
    eye = circles(W, H, [(P(0.82, -0.06)[0], P(0.82, -0.06)[1], 0.035 * s)])
    cream = np.maximum.reduce([rim, lm, tk * bm, eye])
    black = np.clip(bm - tk - eye, 0, 1)
    return cream, black


def textile(W, H, top, bot, seed, field_fn):
    """Assemble the cloth rectangle [top, bot] with border bands, call field_fn for the centre. Returns cream, black."""
    cream = [blank(W, H)[..., 3]]; black = [blank(W, H)[..., 3]]
    rect = lambda x0, y0, x1, y1: shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)
    # side borders
    for flip in (False, True):
        X = (lambda v: W - v) if flip else (lambda v: v)
        xs = sorted([X(0), X(12)]); black.append(rect(xs[0], top, xs[1], bot))
        xs = sorted([X(14), X(18)]); cream.append(rect(xs[0], top, xs[1], bot))
        xs = sorted([X(40), X(44)]); cream.append(rect(xs[0], top, xs[1], bot))
        cx = X(29)
        ds = []; dots = []
        for yy in np.arange(top + 22, bot - 10, 30):
            ds.append(diamond(cx, yy, 8.5, 12))
            dots.append(diamond(cx, yy, 3, 4.5))
        cream.append(np.clip(shapes(W, H, ds, smooth=False) - shapes(W, H, dots, smooth=False), 0, 1))
    # end bands with teeth
    for end in ("top", "bot"):
        y0 = top if end == "top" else bot
        sg = 1 if end == "top" else -1
        a, b = sorted([y0, y0 + sg * 14]); black.append(rect(0, a, W, b))
        a, b = sorted([y0 + sg * 60, y0 + sg * 68]); cream.append(rect(0, a, W, b))
        teeth = []; inner = []
        for x in np.arange(46, W - 46, 26):
            teeth.append([(x, y0 + sg * 18), (x + 26, y0 + sg * 18), (x + 13, y0 + sg * 56)])
            inner.append([(x + 8, y0 + sg * 22), (x + 18, y0 + sg * 22), (x + 13, y0 + sg * 40)])
        black.append(shapes(W, H, teeth, smooth=False))
        cream.append(shapes(W, H, inner, smooth=False))
    c2, b2 = field_fn()
    halo = np.clip((gaussian_filter(c2, 3.2) > 0.1).astype(np.float32) - c2, 0, 1)
    cream.append(c2); black.append(np.maximum(b2, halo))
    c = np.clip(np.maximum.reduce(cream), 0, 1); bl = np.clip(np.maximum.reduce(black), 0, 1) * (1 - c)
    return c, bl


def dye(W, H, cream, black, seed, top, bot, fringe=0, col_w=4):
    """Colour the masks as engkudu-dyed warp-ikat with thread texture. Returns RGBA (cloth + optional fringe)."""
    c = ikat(cream, seed, col_w=col_w, shift=3.2, bleed=3.2)
    b = ikat(black, seed, col_w=col_w, shift=3.2, bleed=3.2) * (1 - c)
    tone = fbm(W, H, seed + 3, 120, 3)
    rgb = col3(RED_D) * (1 - tone[..., None]) + col3(RED_L) * tone[..., None]
    rgb = lerp_rgb(rgb, RED, 0.4 * np.ones((H, W), np.float32))
    rgb = lerp_rgb(rgb, BLACK, b * 0.96)
    ctone = fbm(W, H, seed + 5, 60, 2)[..., None]
    cream_rgb = col3(CREAM) * (1 - ctone * 0.6) + col3(CREAM_D) * ctone * 0.6
    rgb = rgb * (1 - c[..., None]) + cream_rgb * c[..., None]
    rgb *= weave_mod(H, W, seed + 7, col_w=col_w)[..., None]
    # gentle hanging folds
    xx = np.arange(W, dtype=np.float32)
    fold = 1 + 0.05 * np.sin(xx / W * math.tau * 3.2 + 0.7) + 0.025 * np.sin(xx / W * math.tau * 7.1)
    rgb *= fold[None, :, None]
    a = np.zeros((H, W), np.float32)
    edge = (fbm(W, H, seed + 9, 20, 2) - 0.5) * 3
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    a[(yy >= top + edge) & (yy <= bot + edge)] = 1
    if fringe:
        rng = np.random.default_rng(seed + 11)
        fr = blank(W, H)
        items_c, items_r = [], []
        for x in np.arange(3, W - 3, 5.0):
            L = fringe * rng.uniform(0.75, 1.0)
            pts = [(x, bot - 2), (x + rng.normal(0, 1.5), bot + L * 0.5), (x + rng.normal(0, 3), bot + L)]
            (items_c if (int(x / 5) // 3) % 2 == 0 else items_r).append((curve(pts, 10), 2.6, (0.0, 0.3)))
        mc = strokes(W, H, items_c); mr = strokes(W, H, items_r)
        frgb = lerp_rgb(lerp_rgb(np.zeros((H, W, 3), np.float32), CREAM_D, mc), RED_D, mr)
        fa = np.maximum(mc, mr)
        rgb = rgb * (1 - fa[..., None] * (1 - a[..., None])) + frgb * fa[..., None] * (1 - a[..., None])
        a = np.maximum(a, fa)
    return rgba(rgb, a)


if "kain" in PARTS:
    W, H = 760, 600
    TOP, BOT = 30, 520

    def field():
        cr, bl = [], []
        c, b = medallion(W, H, 380, 275, 132, 142)
        cr.append(c); bl.append(b)
        for y, s_ in ((178, 74), (372, 74)):
            c, b = baya(W, H, 166, y, s_ * 0.94, 1); cr.append(mirror_mask(c)); bl.append(mirror_mask(b))
        dl = [diamond(x, y, 6, 8) for x in (110, 650) for y in (275,)] + [diamond(380, 104, 9, 12), diamond(380, 446, 9, 12)]
        dl += [diamond(x, 275, 4, 6) for x in (150, 186, 574, 610)]
        cr.append(shapes(W, H, dl, smooth=False))
        return np.maximum.reduce(cr), np.maximum.reduce(bl)

    cream, black = textile(W, H, TOP, BOT, 1, field)
    art = dye(W, H, cream, black, 1301, TOP, BOT, fringe=60)
    rod = strokes(W, H, [([(-10, 22), (W + 10, 18)], 22, None)])
    art = GP(art, rod, "#4a2d18", "#26160b", seed=1311, rough=1.0, streak=1.2, pad=8)
    hi = strokes(W, H, [([(0, 15), (W, 11)], 4, None)])
    art = G(art, hi, "#9a6a3a", seed=1312, density=0.5, edge=0, bloom=0, rough=1)
    loops = strokes(W, H, [(curve([(x - 3, 10), (x + 4, 22), (x - 2, 38)], 10), 5, None) for x in range(70, W - 40, 124)])
    art = GP(art, loops, CREAM_D, "#b59f78", seed=1313, rough=0.6, pad=6)
    preview(art, "pk-kain", bg="#241612")
    save(art, f"{OUT}/kain.webp", max_w=640, quality=80)
    clear()

if "betang" in PARTS:
    # rumah betang on stilts along the Kapuas at dusk; forest behind, longboat moored, reflections in the river
    W, H = 820, 400
    nx = Seq(13400)
    WL = 296  # water line
    art = painted_sky(W, H, [(0, "#f2dcae"), (0.35, "#efc489"), (0.62, "#e39a5c"), (1, "#b8683e")], seed=nx(), streak=1.2)
    # sun low behind the forest
    sun = circles(W, H, [(762, 176, 24)])
    art = over(art, glow(sun, "#f6e0b0", radius=30, strength=0.5))
    art = GP(art, sun, "#f8cf86", "#f2b264", seed=nx(), rough=1.0, pad=8)
    # far hills + forest canopy (two layers)
    far = jw.hills(W, H, 214, 26, 5, 0.7)
    art = GP(art, far, "#9a5a3a", "#87503a", seed=nx(), rough=3, streak=0.6, pad=8)
    rng = random.Random(4)
    crowns = [(x, 248 - rng.uniform(0, 26), rng.uniform(18, 34)) for x in range(-10, W + 20, 26)]
    canopy = np.maximum(circles(W, H, crowns), shapes(W, H, [[(-20, 250), (W + 20, 250), (W + 20, WL + 4), (-20, WL + 4)]], smooth=False))
    art = GP(art, canopy, "#4a2a1c", "#33201a", seed=nx(), rough=4, streak=0.8, pad=8)
    lit_c = circles(W, H, [(x - 6, y - r * 0.4, r * 0.55) for x, y, r in crowns])
    art = G(art, lit_c * canopy, "#8a4a2c", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=3)
    # tall tapang tree left
    trunk = strokes(W, H, [(curve([(92, WL), (98, 190), (90, 92)], 20), 9, (0.0, 0.6))])
    tc = circles(W, H, [(70, 96, 30), (104, 82, 34), (132, 102, 24), (88, 120, 22), (120, 120, 20)])
    art = GP(art, np.maximum(trunk, tc), "#3a241a", "#2a1a14", seed=nx(), rough=3, streak=0.8, pad=8)
    # riverbank strip
    bank = shapes(W, H, [[(-20, 284), (W + 20, 280), (W + 20, WL + 6), (-20, WL + 8)]], smooth=False)
    art = GP(art, bank, "#5c3424", "#43281c", seed=nx(), rough=2, pad=6)
    # longhouse
    X0, X1 = 170, 700
    FL = 236  # floor level
    house = blank(W, H)
    stilts = strokes(W, H, [([(x, FL), (x + rng.uniform(-1.5, 1.5), WL + 2)], 4.2, None) for x in range(X0 + 6, X1, 19)])
    house = GP(house, stilts, "#2a1913", seed=nx(), rough=0.8, pad=6)
    floor = shapes(W, H, [[(X0 - 22, FL - 6), (X1 + 4, FL - 6), (X1 + 4, FL + 4), (X0 - 22, FL + 4)]], smooth=False)
    wall = shapes(W, H, [[(X0 + 70, 178), (X1, 178), (X1, FL - 4), (X0 + 70, FL - 4)]], smooth=False)
    house = GP(house, wall, "#a8683c", "#7e4a2a", seed=nx(), rough=1.2, streak=1.2, pad=6)
    planks = strokes(W, H, [([(x, 180), (x, FL - 6)], 1.2, None) for x in range(X0 + 74, X1, 7)])
    house = G(house, planks * wall, "#4a2a18", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    doors = shapes(W, H, [[(x, 192), (x + 12, 192), (x + 12, FL - 6), (x, FL - 6)] for x in range(X0 + 96, X1 - 10, 58)], smooth=False)
    house = GP(house, doors, "#2a1712", seed=nx(), rough=0.6, pad=6)
    # open veranda (tanju) at the left end with railing
    rail = strokes(W, H, [([(X0 - 20, FL - 22), (X0 + 70, FL - 22)], 2.6, None)] + [([(x, FL - 22), (x, FL - 5)], 2.2, None) for x in range(X0 - 18, X0 + 70, 11)])
    house = GP(house, np.maximum(floor, rail), "#3a2216", seed=nx(), rough=0.8, pad=6)
    # roof: long gable, dark ironwood shingles with eaves
    roof = shapes(W, H, [[(X0 + 52, 182), (X0 + 92, 140), (X1 - 18, 140), (X1 + 22, 182)]], smooth=False)
    house = GP(house, roof, "#3b2418", "#2a1910", seed=nx(), rough=1.2, streak=1.4, pad=6)
    shing = strokes(W, H, [([(X0 + 92 - (y - 140) * 0.95, y), (X1 - 18 + (y - 140) * 0.95, y)], 1.1, None) for y in range(147, 182, 7)])
    house = G(house, shing * roof, "#7a4c30", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4)
    lit = shapes(W, H, [[(X0 + 92, 140), (X1 - 18, 140), (X1 - 26, 146), (X0 + 96, 146)]], smooth=False)
    house = G(house, lit, "#c58552", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6)
    # crossed gable finials (carved horns) at both roof ends + small one over the veranda roof
    fin = strokes(W, H, [(curve([(X0 + 92, 142), (X0 + 80, 124), (X0 + 86, 110)], 10), 3.6, (0.0, 0.4)), (curve([(X0 + 92, 142), (X0 + 104, 122), (X0 + 100, 108)], 10), 3.6, (0.0, 0.4)),
                         (curve([(X1 - 18, 142), (X1 - 30, 124), (X1 - 24, 110)], 10), 3.6, (0.0, 0.4)), (curve([(X1 - 18, 142), (X1 - 6, 122), (X1 - 10, 108)], 10), 3.6, (0.0, 0.4))])
    house = GP(house, fin, "#2a1910", seed=nx(), rough=0.6, pad=6)
    vroof = shapes(W, H, [[(X0 - 30, FL - 30), (X0 - 10, FL - 44), (X0 + 74, FL - 44), (X0 + 74, FL - 30)]], smooth=False)
    house = GP(house, vroof, "#4a2c1c", seed=nx(), rough=1.0, pad=6)
    # warm lamplight in two doorways
    lamp = shapes(W, H, [[(x + 2, 196), (x + 10, 196), (x + 10, FL - 8), (x + 2, FL - 8)] for x in (X0 + 154, X0 + 328)], smooth=False)
    house = GP(house, lamp, "#f0c27a", "#e0a35a", seed=nx(), rough=0.4, pad=4)
    house = over(house, glow(lamp, "#f3c682", radius=8, strength=0.4))
    # notched-log ladder (tangga) down to the river
    lad = strokes(W, H, [([(X0 + 20, FL + 2), (X0 - 14, WL + 4)], 5, None)])
    notch = strokes(W, H, [([(X0 + 20 - t * 34 - 4, FL + 2 + t * (WL - FL) ), (X0 + 20 - t * 34 + 4, FL + 2 + t * (WL - FL))], 1.6, None) for t in np.linspace(0.1, 0.9, 6)])
    house = GP(house, lad, "#4a2c1c", seed=nx(), rough=0.6, pad=6)
    house = GP(house, notch, "#a06a40", seed=nx(), rough=0.3, pad=4)
    art = over(art, house)
    # river: painted water, reflection of everything above the water line, ripples
    water = shapes(W, H, [[(-20, WL + 2), (W + 20, WL), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    wat = painted_sky(W, H, [(0, "#3a2016"), (0.72, "#3a2016"), (0.76, "#c47a4a"), (0.86, "#8e4c2e"), (1, "#3c2016")], seed=nx(), streak=1.6)
    art = art * (1 - water[..., None]) + wat * water[..., None]
    refl = art[max(0, 2 * WL - H):WL][::-1].copy()
    pad = np.zeros((H - WL - refl.shape[0], W, 4), np.float32) if H - WL > refl.shape[0] else np.zeros((0, W, 4), np.float32)
    rr = np.concatenate([refl, pad], 0)[: H - WL]
    yy = np.arange(H - WL, dtype=np.float32)
    shift = (np.sin(yy * 0.55) * 2.2 + np.sin(yy * 0.13) * 3)[:, None] * np.ones((1, W), np.float32)
    gy, gx = np.mgrid[0:H - WL, 0:W].astype(np.float32)
    rr = np.stack([map_coordinates(rr[..., c], [gy, gx + shift], order=1, mode="nearest") for c in range(4)], -1)
    fade = np.clip(1 - yy / (H - WL) * 1.2, 0, 1)[:, None] * 0.62
    seg = art[WL:].copy()
    seg[..., :3] = seg[..., :3] * (1 - fade[..., None]) + rr[..., :3] * fade[..., None] * 0.9
    art[WL:] = seg
    ripple = strokes(W, H, [([(x, y), (x + rng.uniform(18, 60), y)], 1.6, (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(WL + 8, H - 6)) for _ in range(70)]])
    art = G(art, ripple, "#e3b27a", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8, feather=0.4)
    # moored longboat (perahu) with pole
    boat = shapes(W, H, [[(430, 318), (612, 318), (636, 306), (624, 324), (600, 334), (444, 334), (420, 322), (410, 306)]])
    art = GP(art, boat, "#2a1712", "#3a2216", seed=nx(), rough=1.0, pad=6)
    gun = strokes(W, H, [([(424, 319), (618, 319)], 2, None)])
    art = GP(art, gun, "#b07446", seed=nx(), rough=0.4, pad=4)
    pole = strokes(W, H, [([(650, 262), (622, 352)], 3, None)])
    art = GP(art, pole, "#2a1712", seed=nx(), rough=0.4, pad=4)
    # feather top into transparent so it melts into the dark cover
    yy = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip(yy / 70, 0, 1) * np.clip((H - yy) / 30, 0, 1)
    xx = np.arange(W, dtype=np.float32)[None, :]
    a = a * np.clip(np.minimum(xx, W - xx) / 40, 0, 1)
    art[..., 3] = a * np.ones((1, W), np.float32)
    art = add_grain(art, 3, 0.03)
    preview(art, "pk-betang", bg="#1f1410")
    save_full(art, f"{OUT}/betang.webp", size=(640, 312), quality=78)
    clear()

if "band" in PARTS:
    W, H = 624, 104
    rect = lambda x0, y0, x1, y1: shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)
    cream = [rect(0, 10, W, 14), rect(0, H - 14, W, H - 10)]
    black = [rect(0, 0, W, 8), rect(0, H - 8, W, H)]
    teeth, inner, ds, dd = [], [], [], []
    for x in np.arange(0, W + 1, 24):
        teeth += [[(x, 16), (x + 24, 16), (x + 12, 38)], [(x + 12, H - 16), (x + 36, H - 16), (x + 24, H - 38)]]
    for x in np.arange(0, W + 1, 52):
        ds.append(diamond(x + 26, H / 2, 20, 13))
        dd.append(diamond(x + 26, H / 2, 9, 5.5))
        inner.append(diamond(x + 26, H / 2, 3, 2))
    black.append(shapes(W, H, teeth, smooth=False))
    cream.append(np.clip(shapes(W, H, ds, smooth=False) - shapes(W, H, dd, smooth=False), 0, 1))
    cream.append(shapes(W, H, inner, smooth=False))
    hooks = []
    for x in np.arange(0, W + 1, 52):
        for sx in (-1, 1):
            hx = x + 26 + sx * 26
            hooks.append((hook(hx, H / 2 - 6, 6, math.pi / 2, d=sx, turns=1.0, n=18), 3.2, (0.0, 0.5)))
    cream.append(strokes(W, H, hooks))
    c = np.maximum.reduce(cream); b = np.maximum.reduce(black) * (1 - c)
    art = dye(W, H, c, b, 1501, 0, H)
    art[..., 3] = 1
    save_full(art, f"{OUT}/band.webp", size=(312, 52), quality=82)
    preview(art, "pk-band")
    clear()

if "motif" in PARTS:
    W, H = 360, 400
    c, b = medallion(W, H, 180, 200, 128, 140)
    c = ikat(c, 1601, shift=2.6, bleed=2.6); b = ikat(b, 1601, shift=2.6, bleed=2.6) * (1 - c)
    rgb = lerp_rgb(lerp_rgb(np.zeros((H, W, 3), np.float32), BLACK, b), CREAM, c)
    rgb *= weave_mod(H, W, 1607)[..., None]
    art = rgba(rgb, np.maximum(c, b))
    preview(art, "pk-motif", bg=RED)
    save(art, f"{OUT}/motif.webp", max_w=180, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 420, 70
    items = []
    for sx in (-1, 1):
        stem = [(210 + sx * 26, 35), (210 + sx * 196, 35)]
        items.append((stem, 4, (0.0, 0.3)))
        for k, x in enumerate(range(60, 190, 30)):
            d = 1 if k % 2 else -1
            px = 210 + sx * x
            items.append((curve([(px, 35), (px + sx * 10, 35 + d * 10), (px + sx * 18, 35 + d * 14)], 10), 3.2, (0.0, 0.2)))
            items.append((hook(px + sx * 18, 35 + d * 20, 6, -d * math.pi / 2, d=sx * d, turns=1.0, n=18), 3, (0.0, 0.5)))
    lines = strokes(W, H, items)
    dm = shapes(W, H, [diamond(210, 35, 18, 24)], smooth=False)
    dc = shapes(W, H, [diamond(210, 35, 7, 10)], smooth=False)
    red = ikat(np.maximum(lines, np.clip(dm - shapes(W, H, [diamond(210, 35, 12, 17)], smooth=False), 0, 1)), 1701, shift=1.8, bleed=2)
    blk = ikat(np.maximum(dc, shapes(W, H, [diamond(210 + sx * 202, 35, 5, 7) for sx in (-1, 1)], smooth=False)), 1701, shift=1.8, bleed=2)
    rgb = lerp_rgb(lerp_rgb(np.zeros((H, W, 3), np.float32), RED, red), BLACK, blk)
    art = rgba(rgb, np.maximum(red, blk))
    preview(art, "pk-divider")
    save(art, f"{OUT}/divider.webp", max_w=260, quality=86)
    clear()

if "weave" in PARTS:
    for name, base, amt in (("weave", "#21150f", 1.6), ("weave-c", "#f1e6cf", 0.32)):
        n = 192
        rng = np.random.default_rng(1801)
        xx = np.arange(n); ct = (rng.random(n // 4) - 0.5) * 0.1
        warp = ct[xx // 4][None, :] + (np.cos((xx % 4) / 4 * math.tau) * 0.035)[None, :]
        wf = (np.cos(np.arange(n) / 3 * math.tau) * 0.04)[:, None]
        slub = (wrap_noise(n, n, 1802, 1.2) - 0.5) * 0.1 + (wrap_noise(n, n, 1803, 14) - 0.5) * 0.12
        mod = 1 + (warp + wf + slub) * amt
        rgb = np.ones((n, n, 3), np.float32) * col3(base) * mod[..., None]
        save_full(rgba(rgb, np.ones((n, n), np.float32)), f"{OUT}/{name}.webp", quality=72)

if "patch" in PARTS:
    # a lozenge-shaped piece of pua: hooked medallion on the red ground, black and cream selvedge rim
    W, H = 360, 400
    c, b = medallion(W, H, 180, 200, 104, 115)
    outer = shapes(W, H, [diamond(180, 200, 176, 196)], smooth=False)
    r1 = ring_poly(W, H, diamond(180, 200, 176, 196), diamond(180, 200, 162, 181))
    r2 = ring_poly(W, H, diamond(180, 200, 158, 177), diamond(180, 200, 153, 171))
    halo = np.clip((gaussian_filter(c, 3.0) > 0.1).astype(np.float32) - c, 0, 1)
    cream = np.maximum(c, r2); black = np.maximum.reduce([b, r1, halo]) * (1 - cream)
    art = dye(W, H, cream, black, 1901, 0, H)
    art[..., 3] = ikat(outer, 1901, shift=2.0, bleed=2.0)
    preview(art, "pk-patch")
    save(art, f"{OUT}/patch.webp", max_w=220, quality=82)
    clear()
