"""Kerawang Melayu — gouache on warm cengal timber: a pierced 'tebuk tembus' kerawang lintel panel of awan larat
(continuous spiralling vine scrolls with leaves and small five-petal flowers), mirrored about a central bloom, with warm
afternoon light shining through the cut-outs; the same pattern thrown as a pool of light on a pale floor; a small
pierced divider strip; a round pierced roundel lit from behind; a dark cengal wall texture.
No figures, no calligraphy.
Run: python3 -I kerawang-melayu.py [part ...]   parts: frieze lantai awan bunga kayu
Assets -> public/themes/art/kerawang-melayu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t4_lib import *  # noqa
from _jw_lib import spiral_pts, along  # noqa

OUT = outdir("kerawang-melayu")
PARTS = sys.argv[1:] or ["frieze", "lantai", "awan", "bunga", "kayu"]
CENGAL, CENGAL_L, CENGAL_D = "#7a3a18", "#9c5226", "#2e1206"
LIGHT_C, LIGHT_E = "#fff4cf", "#e88a2c"


def scroll(cx, cy, r, a0, turns, d, n=40):
    return spiral_pts(cx, cy, r, r * 0.12, a0, turns, n, d)


def flower(cx, cy, r, rot=0.0, k=5, wr=0.42):
    rr = random.Random(int(cx * 7 + cy))
    return [deform(petal_pts(cx + math.cos(rot + i / k * math.tau) * r * 0.12, cy + math.sin(rot + i / k * math.tau) * r * 0.12, r, r * wr, rot + i / k * math.tau, n=12), rr, 1, 0.04) for i in range(k)]


def leaves_along(pts, every, L, rng, start=0, ang=0.75, wr=0.3):
    out = []
    side = 1
    for k, (x, y, a) in enumerate(along(pts, every)):
        if k < start:
            continue
        aa = a + side * ang + rng.uniform(-0.12, 0.12)
        out.append(petal_pts(x, y, L * rng.uniform(0.85, 1.1), L * wr, aa, n=12, cup=0.3 * side))
        side = -side
    return out


def awan_larat(x0, x1, yc, A, P, s, rng, flip=1):
    """Dense awan larat half-band from x0 towards x1: wavy main stem; in the hollow of every wave a spiral scroll
    (branching from the stem before the wave's extreme) with a flower in its eye; leaves all along the stem and the
    scroll; small leaf sprays in the outer corners. Returns (stroke items, leaf polys, flower polys)."""
    dirn = 1 if x1 > x0 else -1
    L = abs(x1 - x0)
    items, leaves, flowers = [], [], []
    pts = [(x0 + dirn * i, yc + A * math.sin(i / P * math.pi)) for i in range(0, int(L) + 1, 3)]
    items.append((pts, s, (0.0, 0.05)))
    leaves += leaves_along(pts, A * 0.42, A * 0.36, rng, start=1)
    halves = int(L / P + 0.5)
    for h in range(halves):
        xe = x0 + dirn * (h + 0.5) * P
        if abs(xe - x0) > L - P * 0.25:
            break
        side = 1 if h % 2 == 0 else -1
        ye = yc + A * side
        r = A * 0.72
        cx, cy = xe + dirn * P * 0.05, yc + side * A * 0.05
        # branch leaves the stem a little before the extreme and enters the spiral from the outside
        bx = x0 + dirn * (h + 0.22) * P
        by = yc + A * math.sin((h + 0.22) * math.pi)
        a0 = math.atan2(ye - cy, xe - dirn * P * 0.2 - cx)
        sp = spiral_pts(cx, cy, r, r * 0.16, a0, 1.25, 50, side * dirn * -1 * flip * flip)
        branch = curve([(bx, by), ((bx + sp[0][0]) / 2, (by + sp[0][1]) / 2 + side * A * 0.06), sp[0]], 12) + sp[1:]
        items.append((branch, s * 0.8, (0.0, 0.45)))
        leaves += leaves_along(sp[:30], r * 0.5, r * 0.34, rng, start=1, ang=0.9)
        flowers += flower(cx, cy, r * 0.3, rng.uniform(0, 1), 5)
        # outer-corner spray opposite the extreme
        ox, oy = xe, yc - side * A * 1.05
        spray = curve([(ox, yc - side * A * 0.55), (ox + dirn * 6, yc - side * A * 0.8), (ox, oy)], 10)
        items.append((spray, s * 0.45, (0.05, 0.6)))
        for t in (-1, 1):
            leaves.append(petal_pts(ox, yc - side * A * 0.75, A * 0.34, A * 0.11, -side * math.pi / 2 + t * 0.8, n=10, cup=0.2 * t))
        flowers += flower(ox, oy, A * 0.13, 0.3, 5)
    return items, leaves, flowers


def thicken(m, grow=2.5, thr=0.22):
    g = gaussian_filter(m, grow)
    return np.clip(np.maximum(m, (g - thr) * 4), 0, 1)


def light_field(W, H, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    t = np.clip(d, 0, 1)
    a = np.array(hex_rgb(LIGHT_C), np.float32); b = np.array(hex_rgb(LIGHT_E), np.float32)
    rgb = a * (1 - t[..., None]) + b * t[..., None]
    return rgb


def pierced(W, H, solid_mask, interior, seed, nx, light_rgb=None, base=CENGAL, light=CENGAL_L, dark=CENGAL_D, glow_amt=0.55, motif=None):
    """Paint a pierced panel. solid_mask = wood (frame + carving). interior = area that may be cut through.
    Holes (interior - solid) show light_rgb (opaque glow) if given, else transparent."""
    wood_m = np.clip(solid_mask, 0, 1)
    holes = np.clip(interior - wood_m, 0, 1)
    art = blank(W, H)
    if light_rgb is not None:
        lay = np.concatenate([light_rgb, holes[..., None]], -1)
        art = over(art, lay)
    # wood body with grain
    art = over(art, wood(wood_m, light, dark, seed=seed, angle=0, streak=0.9, rough=0.8))
    # relief: carved members are rounded -> lighter crest, darker flanks
    soft = gaussian_filter(wood_m, 2.2)
    crest = np.clip((soft - 0.72) * 3.2, 0, 1) * wood_m
    art = tint(art, crest, mix(light, "#f3cf98", 0.45), 0.45)
    flank = np.clip(wood_m - soft * 1.05, 0, 1) * 2.2
    art = tint(art, np.clip(flank, 0, 1) * wood_m, dark, 0.55)
    if motif is not None:
        # incised outlines of the original leaves/scrolls carved into the solid wood
        gy, gx = np.gradient(gaussian_filter(motif, 0.9))
        inc = np.clip(np.hypot(gx, gy) * 2.6, 0, 1) * wood_m
        art = tint(art, inc, dark, 0.7)
        hi = np.clip(np.roll(np.roll(inc, 1, 0), 1, 1) - inc, 0, 1)
        art = tint(art, hi, "#f0c58a", 0.35)
    # cast shadow inside the cut (top-left light): the hole is darker just under/right of each member
    if light_rgb is not None:
        sh = np.clip(np.roll(np.roll(wood_m, 4, 0), 3, 1) - wood_m, 0, 1) * holes
        art = tint(art, gaussian_filter(sh, 1.2), "#8a4a1a", 0.45)
        # light bleeding over the edges of the wood (rim light)
        rim = np.clip(gaussian_filter(holes, 2.5) * 1.6, 0, 1) * wood_m
        art = tint(art, rim, "#ffcf7a", glow_amt * 0.6)
    art = add_grain(art, seed, 0.03)
    return art


def part_frieze():
    W, H = 780, 296
    rng = random.Random(5); nx = Seq(100)
    frame_o = rect(W, H, 0, 0, W, H)
    inner = rect(W, H, 30, 30, W - 30, H - 30)
    frame = np.clip(frame_o - inner, 0, 1)
    mould = np.clip(rect(W, H, 40, 40, W - 40, H - 40) - rect(W, H, 47, 47, W - 47, H - 47), 0, 1)
    cx, cy = W / 2, H / 2
    items, leaves, fls = [], [], []
    for d in (1, -1):
        it, lv, fl = awan_larat(cx + d * 70, cx + d * (W / 2 - 36), cy, 72, 122, 11, rng, flip=d)
        items += it; leaves += lv; fls += fl
    centre = flower(cx, cy, 44, 0.2, 8, 0.36)
    ring = arc_pts(cx, cy, 60, 0, math.tau, 60)
    items.append((ring, 9, None))
    for k in range(8):
        a = k / 8 * math.tau + 0.6
        leaves.append(petal_pts(cx + math.cos(a) * 64, cy + math.sin(a) * 64, 34, 12, a, n=10))
    carving = np.maximum(strokes(W, H, items), shapes(W, H, leaves + centre + fls + [ellipse_pts(cx, cy, 12, 12, 12)]))
    motif = carving * inner
    carving = thicken(motif, 5.0, 0.1)
    solid = np.clip(np.maximum(np.maximum(frame, mould), carving), 0, 1)
    lrgb = light_field(W, H, cx, cy, W * 0.62, H * 0.9)
    art = pierced(W, H, solid, inner, 11, nx, lrgb, motif=motif)
    art = tint(art, frame * ygrad(W, H, H - 28, H), CENGAL_D, 0.45)
    art = tint(art, frame * (1 - ygrad(W, H, 0, 16)), "#e2a868", 0.25)
    np.save("/tmp/pen/nb-T4/art/kerawang_holes.npy", np.clip(inner - solid, 0, 1)[::2, ::2].astype(np.float16))
    prev(art, "kerawang-frieze", bg="#2a1408")
    save(art, f"{OUT}/frieze.webp", max_w=780, quality=80)


def part_lantai():
    """Light pool on the floor: the frieze holes, projected in perspective (wide, foreshortened), soft and warm."""
    holes = np.load("/tmp/pen/nb-T4/art/kerawang_holes.npy").astype(np.float32)  # 190 x 390
    h0, w0 = holes.shape
    W, H = 780, 300
    # perspective: map floor (u,v) back to panel coordinates: far rows (top) narrower
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = yy / H
    scale = 0.55 + 0.75 * v           # nearer rows are wider
    shear = (v - 0.5) * 120           # light falls diagonally from the left
    u = (xx - W / 2 - shear) / (W * 0.5 * scale) * 0.5 + 0.5
    src_y = (1 - v) * (h0 - 1) * 0.98
    src_x = u * (w0 - 1)
    m = map_coordinates_safe(holes, src_y, src_x)
    m = gaussian_filter(m, 2.2)
    edge = (1 - np.clip(np.abs(u - 0.5) * 2 - 0.86, 0, 1) * 7) * (u > 0) * (u < 1)
    m = m * np.clip(edge, 0, 1) * (0.55 + 0.45 * v)
    lay = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#ffd889"), np.float32), np.clip(m * 0.95, 0, 1)[..., None]], -1)
    halo = gaussian_filter(m, 18) * 0.6
    art = over(flat(halo, "#f6b860"), lay)
    prev(art, "kerawang-lantai", bg="#d9c3a0")
    save(art, f"{OUT}/lantai.webp", max_w=780, quality=78)


def map_coordinates_safe(img, ys, xs):
    from scipy.ndimage import map_coordinates
    return map_coordinates(img, [ys, xs], order=1, mode="constant", cval=0.0)


def part_awan():
    W, H = 480, 96
    rng = random.Random(9); nx = Seq(300)
    cx, cy = W / 2, H / 2
    items, leaves, fls = [], [], []
    for d in (1, -1):
        it, lv, fl = awan_larat(cx + d * 26, cx + d * (W / 2 - 6), cy, 22, 46, 4.5, rng, flip=d)
        items += it; leaves += lv; fls += fl
    centre = flower(cx, cy, 20, 0.2, 6, 0.4)
    carving = thicken(np.maximum(strokes(W, H, items), shapes(W, H, leaves + centre + fls)), 1.2, 0.25)
    art = pierced(W, H, carving, carving * 0, 21, nx, None)
    prev(art, "kerawang-awan")
    save(art, f"{OUT}/awan.webp", max_w=420, quality=82)


def part_bunga():
    W, H = 360, 360
    rng = random.Random(13); nx = Seq(500)
    cx, cy = W / 2, H / 2
    disc = circles(W, H, [(cx, cy, 172)])
    inner = circles(W, H, [(cx, cy, 150)])
    frame = np.clip(disc - inner, 0, 1)
    items, leaves, fls = [], [], []
    k = 6
    for i in range(k):
        a = i / k * math.tau - math.pi / 2
        # an S-scroll arm: out from the centre, curling back on itself near the rim
        ex, ey = cx + math.cos(a + 0.42) * 104, cy + math.sin(a + 0.42) * 104
        sp = spiral_pts(ex, ey, 30, 5, a + 0.42 + math.pi * 0.95, 1.1, 34, 1)
        stem = curve([(cx + math.cos(a) * 52, cy + math.sin(a) * 52), (cx + math.cos(a - 0.12) * 90, cy + math.sin(a - 0.12) * 90), (cx + math.cos(a + 0.12) * 126, cy + math.sin(a + 0.12) * 126), sp[0]], 18)
        items.append((stem + sp, 7, (0.02, 0.5)))
        leaves += leaves_along(stem, 22, 26, rng, start=1, ang=0.85)
        fls += flower(cx + math.cos(a - 0.5) * 128, cy + math.sin(a - 0.5) * 128, 13, a, 5)
    centre = flower(cx, cy, 34, 0.0, 8, 0.38)
    ring = arc_pts(cx, cy, 46, 0, math.tau, 50)
    items.append((ring, 7, None))
    carving = np.maximum(strokes(W, H, items), shapes(W, H, leaves + centre + fls + [ellipse_pts(cx, cy, 10, 10, 12)]))
    motif = carving * inner
    carving = thicken(motif, 4.0, 0.1)
    solid = np.clip(np.maximum(frame, carving), 0, 1)
    lrgb = light_field(W, H, cx, cy, 190, 190)
    art = pierced(W, H, solid, disc, 31, nx, lrgb, motif=motif)
    art[..., 3] *= disc
    prev(art, "kerawang-bunga", bg="#2a1408")
    save(art, f"{OUT}/bunga.webp", max_w=300, quality=82)


def part_kayu():
    """Seamless dark cengal wall: vertical planks (each tile is two planks), grain wraps top to bottom."""
    W, H = 420, 420
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.default_rng(41)
    n = gaussian_filter(rng.random((H, W)).astype(np.float32), (40, 0.8), mode="wrap")
    n = (n - n.min()) / (n.max() - n.min())
    low = gaussian_filter(rng.random((H, W)).astype(np.float32), 30, mode="wrap")
    low = (low - low.min()) / (low.max() - low.min())
    rings = 0.5 + 0.5 * np.sin(xx / 6.0 + low * 10 + np.sin(yy / H * math.tau) * 1.5)
    g = 0.55 * n + 0.45 * rings
    a = np.array(hex_rgb("#5a2c12"), np.float32); d = np.array(hex_rgb("#2a1206"), np.float32)
    k = np.clip((g - 0.4) * 1.5, 0, 1)[..., None] * 0.6
    rgb = a * (1 - k) + d * k
    seam = np.zeros((H, W), np.float32); seam[:, 0:2] = 1; seam[:, 210:212] = 1
    rgb = rgb * (1 - seam[..., None] * 0.45)
    rgb[:, 2:4] *= 1.08; rgb[:, 212:214] *= 1.08
    plank = np.where(xx < 210, 1.0, 0.93)[..., None]
    art = np.concatenate([np.clip(rgb * plank, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    art = add_grain(art, 3, 0.03)
    prev(art, "kerawang-kayu")
    save_rgb(art, f"{OUT}/kayu.webp", quality=70)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
kb(OUT)
