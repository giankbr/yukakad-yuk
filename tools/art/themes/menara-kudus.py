"""Menara Kudus — inspired by the red-brick minaret of Kudus (architecture only): a candi-like stepped plinth with a
front stair, a tall square brick body with pilasters, recessed panels and inlaid blue-and-white ceramic plates, stepped
crown mouldings, an open timber pavilion with a bedug, and a two-tier tajug roof with a mustaka; a brick paduraksa
gate (roofed, stepped) with an open doorway; green glazed wall tiles; one inlaid plate. No figures, no calligraphy.
Run: python3 -I menara-kudus.py [part ...]   parts: menara gate plate tegel strip
Assets -> public/themes/art/menara-kudus/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g1_lib import *  # noqa

OUT = outdir("menara-kudus")
PARTS = sys.argv[1:] or ["menara", "gate", "plate", "tegel", "strip"]
BRICK, BRICK_D, BRICK_L, MORTAR = "#b5502f", "#86351f", "#d27650", "#e2b490"
COBALT, PORC = "#2f4f8f", "#eef0ea"
GREEN, GREEN_D = "#2f7a5c", "#1c5240"


def R(W, H, x0, y0, x1, y1):
    return rect(W, H, x0, y0, x1, y1)


def bricks(art, W, H, mask, nx, bw=26, bh=9, shade=None, seed=1):
    """Paint a brick mass: warm gouache base, per-brick tone drift, mortar courses, right-side shade, weathering."""
    mask = displace(mask, nx(), 1.6, 14)
    art = GP(art, mask, BRICK, BRICK_D, seed=nx(), rough=1.6, streak=0.9)
    bm, tone = brick_field(W, H, bw, bh, 1.6, seed)
    light = bm * mask * np.clip((tone - 0.55) * 2.5, 0, 1)
    dark = bm * mask * np.clip((0.35 - tone) * 2.5, 0, 1)
    art = G(art, light, BRICK_L, seed=nx(), density=0.55, edge=0.15, rough=0.6, feather=0.5)
    art = G(art, dark, "#6e2a18", seed=nx(), density=0.4, edge=0.15, rough=0.6, feather=0.5)
    mort = (1 - bm) * mask * (0.5 + 0.5 * fbm(W, H, nx(), 20, 2))
    art = G(art, mort, MORTAR, seed=nx(), density=0.45, edge=0.0, rough=0.4, feather=0.4)
    if shade is not None:
        art = G(art, mask * shade, "#4a1c10", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=2, feather=2)
    chips = bm * mask * np.clip((fbm(W, H, nx(), 5, 2) - 0.78) * 5, 0, 1)
    art = G(art, chips, "#e9b08c", seed=nx(), density=0.5, edge=0.4, rough=0.4, feather=0.4)
    stain = mask * np.clip((fbm(W, H, nx(), 60, 3) - 0.6) * 2.5, 0, 1)
    art = G(art, stain, "#5a3a2a", seed=nx(), density=0.3, edge=0.3, bloom=0.5, rough=3, feather=3)
    return art


def plate(art, W, H, cx, cy, r, nx, rng, sunk=True):
    """Inlaid porcelain plate: white glaze, cobalt rim band, a simple four-lobed floral centre and a dark recess ring."""
    if sunk:
        art = G(art, circles(W, H, [(cx + 1, cy + 1.5, r + 2.2)]), "#3a160c", seed=nx(), density=0.75, edge=0.3, rough=0.4, feather=0.6, pad=6)
    m = circles(W, H, [(cx, cy, r)])
    art = GP(art, m, PORC, "#dfe3dc", seed=nx(), rough=0.5, streak=0.3, pad=6)
    ring = np.clip(m - circles(W, H, [(cx, cy, r * 0.78)]), 0, 1)
    art = G(art, ring, COBALT, "#3c5ea0", seed=nx(), density=0.8, edge=0.5, rough=0.5, feather=0.5, pad=6)
    pet = shapes(W, H, [petal_pts(cx, cy, r * 0.5, r * 0.2, k * math.pi / 2 + rng.uniform(-0.1, 0.1), n=8) for k in range(4)])
    art = G(art, pet, COBALT, seed=nx(), density=0.75, edge=0.6, rough=0.4, feather=0.4, pad=6)
    art = G(art, circles(W, H, [(cx - r * 0.35, cy - r * 0.4, r * 0.18)]), "#ffffff", seed=nx(), density=0.55, edge=0, rough=0.3, feather=0.8, pad=6)
    return art


def moulding(art, W, H, cx, y, w, h, nx, steps=3, out=1):
    """Stack of projecting brick courses (pelipit): each a little wider, with a lit top edge and shadow under."""
    for k in range(steps):
        ww = w + (k if out > 0 else steps - 1 - k) * 10
        yy = y + k * h
        m = R(W, H, cx - ww / 2, yy, cx + ww / 2, yy + h)
        art = bricks(art, W, H, m, nx, bw=22, bh=h / 2, seed=nx())
        art = G(art, R(W, H, cx - ww / 2, yy, cx + ww / 2, yy + 1.8), "#f0a27a", seed=nx(), density=0.7, edge=0, rough=0.3, feather=0.4)
        art = G(art, R(W, H, cx - ww / 2, yy + h - 2, cx + ww / 2, yy + h + 2), "#3a140a", seed=nx(), density=0.45, edge=0, rough=0.3, feather=0.8)
    return art


def simbar(art, W, H, cx, y, w, nx, size=12):
    """Row of small antefix triangles (simbar) along a cornice."""
    n = max(2, int(w / (size * 2.2)))
    polys = []
    for k in range(n):
        x = cx - w / 2 + (k + 0.5) * w / n
        polys.append([(x - size * 0.6, y), (x - size * 0.3, y - size * 0.55), (x, y - size * 1.05), (x + size * 0.3, y - size * 0.55), (x + size * 0.6, y)])
    m = displace(shapes(W, H, polys, smooth=False), nx(), 1, 8)
    art = GP(art, m, BRICK, BRICK_D, seed=nx(), rough=1, streak=0.5, pad=6)
    art = G(art, m * xgrad(W, H, cx - w / 2, cx + w / 2), "#5a2214", seed=nx(), density=0.35, edge=0.3, rough=0.4, feather=0.6, pad=6)
    return art


def light(art, W, H, nx, x0, x1):
    """Warm afternoon light from the left, cool shade on the right, only where paint exists."""
    m = art[..., 3]
    art = G(art, m * np.clip(1 - xgrad(W, H, x0, x1), 0, 1) * 0.8, "#f7c08e", seed=nx(), density=0.55, edge=0, bloom=0.3, rough=2, feather=3)
    art = G(art, m * xgrad(W, H, x1, x1 + (x1 - x0)) * 0.8, "#3a2a48", seed=nx(), density=0.5, edge=0, bloom=0.3, rough=2, feather=3)
    return art


def tajug(art, W, H, cx, y_top, y_bot, w_top, w_bot, nx, rng, col="#4b3a36", col2="#3a2c2a"):
    m = poly(W, H, [(cx - w_top / 2, y_top), (cx + w_top / 2, y_top), (cx + w_bot / 2, y_bot), (cx - w_bot / 2, y_bot)])
    m = displace(m, nx(), 1, 10)
    art = GP(art, m, col, col2, seed=nx(), rough=1.2, streak=0.8)
    # sirap rows
    rows = []
    for k in range(1, 9):
        t = k / 9
        y = y_top + (y_bot - y_top) * t
        hw = w_top / 2 + (w_bot - w_top) / 2 * t
        rows.append(([(cx - hw, y), (cx + hw, y)], 1.2, None))
    art = G(art, strokes(W, H, rows) * m, "#211816", seed=nx(), density=0.5, edge=0, rough=0.5, feather=0.4)
    art = G(art, m * xgrad(W, H, cx - 10, cx + w_bot / 2), "#1a1210", seed=nx(), density=0.45, edge=0.1, rough=1, feather=2)
    art = G(art, m * np.clip(1 - xgrad(W, H, cx - w_bot / 2, cx - 10), 0, 1), "#8a6e60", seed=nx(), density=0.35, edge=0.1, rough=1, feather=2)
    art = G(art, R(W, H, cx - w_bot / 2 - 4, y_bot - 3, cx + w_bot / 2 + 4, y_bot + 3), "#2a1d1a", seed=nx(), density=0.85, edge=0.3, rough=0.5, feather=0.5)
    return art


def part_menara():
    W, H = 560, 1320
    rng = random.Random(3); nx = Seq(500)
    cx = W / 2
    art = blank(W, H)
    shade_r = lambda x0, x1: xgrad(W, H, x0, x1)
    # ---- plinth: three stepped tiers
    for (y0, y1, w) in [(1210, 1300, 470), (1130, 1210, 420), (1060, 1130, 372)]:
        m = R(W, H, cx - w / 2, y0, cx + w / 2, y1)
        art = bricks(art, W, H, m, nx, shade=shade_r(cx, cx + w / 2) * 0.8, seed=nx())
        art = moulding(art, W, H, cx, y0, w + 8, 7, nx, steps=1)
        art = simbar(art, W, H, cx, y0, w - 10, nx, size=11)
        # recessed panels with a plate
        for px in (cx - w * 0.33, cx + w * 0.33):
            pm = R(W, H, px - 26, y0 + 18, px + 26, y1 - 12)
            art = G(art, pm, "#5a2214", seed=nx(), density=0.45, edge=0.4, rough=0.6, feather=0.6)
            art = plate(art, W, H, px, (y0 + y1) / 2 + 3, 13, nx, rng)
        clear()
    # ---- front stair up to the door
    st = poly(W, H, [(cx - 56, 1300), (cx + 56, 1300), (cx + 42, 1010), (cx - 42, 1010)])
    art = bricks(art, W, H, st, nx, bw=20, bh=8, seed=nx())
    treads = [([(cx - 56 + (1300 - y) * 0.048, y), (cx + 56 - (1300 - y) * 0.048, y)], 1.6, None) for y in range(1020, 1300, 14)]
    art = G(art, strokes(W, H, treads), "#f0a27a", seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    rail = [([(cx - 60, 1300), (cx - 46, 1010)], 6, None), ([(cx + 60, 1300), (cx + 46, 1010)], 6, None)]
    art = G(art, strokes(W, H, rail), "#6e2a18", seed=nx(), density=0.85, edge=0.3, rough=0.6, feather=0.5)
    clear()
    # ---- body
    body = poly(W, H, [(cx - 134, 1060), (cx + 134, 1060), (cx + 126, 470), (cx - 126, 470)])
    art = bricks(art, W, H, body, nx, shade=np.clip(shade_r(cx + 30, cx + 130), 0, 1) * 0.75, seed=nx())
    # pilasters at the corners and centre: lit edge
    for x in (cx - 120, cx - 8, cx + 108):
        pm = R(W, H, x, 480, x + 16, 1050)
        art = G(art, pm, BRICK_L, seed=nx(), density=0.35, edge=0.2, rough=0.6, feather=0.6)
        art = G(art, R(W, H, x + 15, 480, x + 18, 1050), "#4a1c10", seed=nx(), density=0.5, edge=0, rough=0.4, feather=0.6)
    # bands + panels
    for yb in (640, 820, 960):
        art = moulding(art, W, H, cx, yb, 268, 7, nx, steps=2)
    door = poly(W, H, [(cx - 26, 1060), (cx + 26, 1060), (cx + 26, 990), (cx, 972), (cx - 26, 990)])
    art = G(art, door, "#2a120a", "#3a1a10", seed=nx(), density=0.95, edge=0.5, rough=0.6, feather=0.5)
    art = GP(art, R(W, H, cx - 20, 994, cx + 20, 1058), "#5a3a24", "#3e2818", seed=nx(), rough=0.6, streak=0.8)
    for (y0, y1) in [(490, 630), (668, 810), (848, 950)]:
        for px in (cx - 64, cx + 54):
            pm = R(W, H, px - 34, y0 + 6, px + 34, y1 - 6)
            art = G(art, pm, "#5a2214", seed=nx(), density=0.38, edge=0.45, rough=0.6, feather=0.6)
            n = 2 if y1 - y0 > 120 else 1
            for k in range(n):
                py = y0 + (y1 - y0) * (k + 0.5) / n
                art = plate(art, W, H, px, py, 15, nx, rng)
    # green glazed tiles in a frieze under the crown
    for k in range(8):
        x = cx - 112 + k * 30
        tm = R(W, H, x, 452, x + 24, 468)
        art = GP(art, tm, GREEN, GREEN_D, seed=nx(), rough=0.6, streak=0.6, pad=4)
        art = G(art, R(W, H, x + 3, 454, x + 12, 457), "#bfe6cf", seed=nx(), density=0.55, edge=0, rough=0.2, feather=0.5, pad=4)
    clear()
    # ---- crown mouldings stepping outwards
    art = moulding(art, W, H, cx, 410, 262, 10, nx, steps=4, out=-1)
    art = simbar(art, W, H, cx, 410, 280, nx, size=10)
    # ---- pavilion: posts, dark interior, bedug
    inner = R(W, H, cx - 120, 300, cx + 120, 410)
    art = GP(art, inner, "#2a1a12", "#3a2418", seed=nx(), rough=0.6, streak=0.8)
    bed = shapes(W, H, [ellipse_pts(cx, 368, 46, 26, n=16)])
    art = GP(art, bed, "#8a5a30", "#6a4224", seed=nx(), rough=0.6, streak=0.8)
    art = GP(art, shapes(W, H, [ellipse_pts(cx - 40, 368, 8, 24, n=12)]), "#e6d2a8", seed=nx(), rough=0.4, streak=0.4)
    art = G(art, strokes(W, H, [([(cx - 46, 352 + k * 8), (cx + 40, 352 + k * 8)], 0.8, None) for k in range(4)]) * bed, "#3a2412", seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.4)
    posts = np.clip(sum(R(W, H, x - 6, 296, x + 6, 410) for x in (cx - 112, cx - 40, cx + 40, cx + 112)), 0, 1)
    art = GP(art, posts, "#5b3a22", "#3f2818", seed=nx(), rough=0.6, streak=1.0)
    art = G(art, R(W, H, cx - 124, 404, cx + 124, 412), "#3f2818", seed=nx(), density=0.9, edge=0.2, rough=0.4, feather=0.5)
    clear()
    # ---- two-tier tajug roof + mustaka
    art = tajug(art, W, H, cx, 230, 302, 150, 330, nx, rng)
    art = G(art, R(W, H, cx - 56, 214, cx + 56, 232), "#1e140f", seed=nx(), density=0.9, edge=0.3, rough=0.4, feather=0.5)
    art = tajug(art, W, H, cx, 120, 216, 14, 200, nx, rng)
    must = shapes(W, H, [[(cx, 46), (cx + 9, 76), (cx + 14, 104), (cx + 6, 122), (cx - 6, 122), (cx - 14, 104), (cx - 9, 76)]])
    art = FO(art, must, "#b9913f", seed=nx(), emboss=0.6, sparkle=0.1)
    clear()
    art = light(art, W, H, nx, cx - 140, cx + 60)
    preview(art, "mk-menara", tone="#f1e6d4")
    save(art, f"{OUT}/menara.webp", max_w=360, quality=82)
    clear()


def part_gate():
    """Paduraksa: a roofed brick gate, wings stepping up to a central crown, a tall doorway left open (transparent)."""
    W, H = 760, 820
    rng = random.Random(9); nx = Seq(1300)
    cx = W / 2
    art = blank(W, H)
    mass = np.zeros((H, W), np.float32)
    tiers = [(560, 820, 760), (470, 560, 640), (390, 470, 520), (320, 390, 420), (260, 320, 330), (210, 260, 250), (170, 210, 170)]
    for y0, y1, w in tiers:
        mass = np.maximum(mass, R(W, H, cx - w / 2, y0, cx + w / 2, y1))
    door = poly(W, H, [(cx - 150, 822), (cx + 150, 822), (cx + 150, 470), (cx, 400), (cx - 150, 470)])
    m = np.clip(mass - door, 0, 1)
    art = bricks(art, W, H, m, nx, shade=xgrad(W, H, cx + 40, cx + 380) * 0.7, seed=nx())
    clear()
    for y0, y1, w in tiers:
        art = moulding(art, W, H, cx, y0, w + 10, 7, nx, steps=1)
        art = simbar(art, W, H, cx, y0, w - 6, nx, size=13)
        if w > 300:
            for px in (cx - w * 0.38, cx + w * 0.38):
                if abs(px - cx) > 185:
                    art = plate(art, W, H, px, (y0 + y1) / 2 + 4, 14, nx, rng)
        clear()
    # door frame: green tile jambs
    jambs = np.clip(R(W, H, cx - 166, 470, cx - 150, 822) + R(W, H, cx + 150, 470, cx + 166, 822), 0, 1)
    art = GP(art, jambs, GREEN, GREEN_D, seed=nx(), rough=0.6, streak=0.6)
    tiles = [([(cx - 166, y), (cx - 150, y)], 1.2, None) for y in range(486, 822, 18)] + [([(cx + 150, y), (cx + 166, y)], 1.2, None) for y in range(486, 822, 18)]
    art = G(art, strokes(W, H, tiles), "#e8efe6", seed=nx(), density=0.75, edge=0, rough=0.3, feather=0.4)
    arch = stroke_mask(W, H, [(cx - 158, 472), (cx, 392), (cx + 158, 472)], 16)
    art = GP(art, arch, GREEN, GREEN_D, seed=nx(), rough=0.6, streak=0.6)
    # roof cap + finial
    art = tajug(art, W, H, cx, 120, 172, 30, 190, nx, rng)
    fin = shapes(W, H, [[(cx, 72), (cx + 8, 96), (cx + 12, 118), (cx - 12, 118), (cx - 8, 96)]])
    art = FO(art, fin, "#b9913f", seed=nx(), emboss=0.6, sparkle=0.1)
    art = light(art, W, H, nx, cx - 300, cx + 40)
    art[..., 3] *= 1 - np.clip(door * 1.2, 0, 1)
    preview(art, "mk-gate", tone="#f1e6d4")
    save_full(art, f"{OUT}/gate.webp", size=(380, 410), quality=82)
    clear()


def part_plate():
    W = H = 200
    rng = random.Random(5); nx = Seq(1700)
    art = plate(blank(W, H), W, H, 100, 100, 80, nx, rng, sunk=False)
    m = circles(W, H, [(100, 100, 80)])
    for k in range(12):
        a = k / 12 * math.tau
        x, y = 100 + math.cos(a) * 70, 100 + math.sin(a) * 70
        art = G(art, shapes(W, H, [petal_pts(x, y, 9, 4, a + math.pi / 2, n=8)]) * m, "#f4f2ea", seed=nx(), density=0.7, edge=0.3, rough=0.3, feather=0.4)
    preview(art, "mk-plate", tone="#f1e6d4")
    save(art, f"{OUT}/plate.webp", max_w=100, quality=86)
    clear()


def part_tegel():
    """Green glazed tile wall (tileable 2x2): glossy pooled glaze, darker at edges, crazing, cream grout."""
    W = H = 256
    rng = random.Random(2); nx = Seq(2000)
    art = np.concatenate([np.ones((H, W, 3), np.float32) * col_arr("#e8dcc4"), np.ones((H, W, 1), np.float32)], -1)
    for i in range(2):
        for j in range(2):
            x0, y0 = i * 128 + 4, j * 128 + 4
            m = rect(W, H, x0, y0, x0 + 120, y0 + 120)
            art = GP(art, m, mix_hex(GREEN, "#3f8a6a", rng.uniform(0, 0.6)), GREEN_D, seed=nx(), rough=0.8, streak=0.4, pad=4)
            rim = np.clip(m - gaussian_filter(m, 8) * 1.1, 0, 1)
            art = G(art, rim * 2, "#163e30", seed=nx(), density=0.5, edge=0, rough=0.5, feather=1.5, pad=4)
            hl = R(W, H, x0 + 14, y0 + 12, x0 + 60, y0 + 22)
            art = G(art, gaussian_filter(hl, 4), "#d8f2e2", seed=nx(), density=0.45, edge=0, rough=0.5, feather=2, pad=8)
            # embossed four-petal flower in the centre
            fl = shapes(W, H, [petal_pts(x0 + 60, y0 + 60, 30, 12, k * math.pi / 2 + math.pi / 4, n=10) for k in range(4)])
            art = G(art, fl, "#1c5240", seed=nx(), density=0.45, edge=0.6, rough=0.4, feather=0.6, pad=4)
            art = G(art, circles(W, H, [(x0 + 60, y0 + 60, 6)]), "#cfe8d6", seed=nx(), density=0.6, edge=0.3, rough=0.3, feather=0.5, pad=4)
    crack = []
    for _ in range(26):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        pts = [(x, y)]
        for _ in range(4):
            x += rng.uniform(-14, 14); y += rng.uniform(-14, 14); pts.append((x, y))
        crack.append((pts, 0.6, None))
    art = G(art, strokes(W, H, crack), "#153a2c", seed=nx(), density=0.3, edge=0, rough=0.2, feather=0.3)
    rgb = art[..., :3]
    prev_rgb(rgb, "mk-tegel")
    rgb_save(rgb, f"{OUT}/tegel.webp", quality=76, size=(160, 160))
    clear()


def part_strip():
    """Divider: a short brick course with three inlaid plates and green tiles between."""
    W, H = 640, 80
    rng = random.Random(6); nx = Seq(2400)
    art = blank(W, H)
    m = R(W, H, 20, 22, W - 20, 58)
    art = bricks(art, W, H, m, nx, bw=24, bh=9, seed=7)
    art = moulding(art, W, H, W / 2, 16, W - 30, 6, nx, steps=1)
    art = moulding(art, W, H, W / 2, 58, W - 30, 6, nx, steps=1)
    for k, x in enumerate([W / 2 - 180, W / 2 - 90, W / 2, W / 2 + 90, W / 2 + 180]):
        if k % 2 == 0:
            art = plate(art, W, H, x, 40, 15, nx, rng)
        else:
            tm = R(W, H, x - 14, 28, x + 14, 52)
            art = GP(art, tm, GREEN, GREEN_D, seed=nx(), rough=0.5, streak=0.5, pad=4)
            art = G(art, R(W, H, x - 10, 30, x, 34), "#c8ecd8", seed=nx(), density=0.5, edge=0, rough=0.2, feather=0.5, pad=4)
    preview(art, "mk-strip", tone="#f1e6d4")
    save(art, f"{OUT}/strip.webp", max_w=320, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
