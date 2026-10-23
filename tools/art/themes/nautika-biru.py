"""Nautika Biru — marine gouache: a harbour morning (sailboats, a red-and-white lighthouse on the breakwater, wave
dabs, gulls), a brass compass rose, a navy anchor wrapped in rope, a string of signal flags (decorative patterns, no
message), a rope knot divider, a brass porthole ring and a hand-painted breton-stripe tile.
Palette: navy, white, signal red, brass, sea blue, rope tan. Opaque matte paint, light from the upper left.
Run: python3 -I nautika-biru.py [part ...]  parts: harbour compass anchor flags knot ring stripe"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i6_lib import *  # noqa

OUT = outdir("nautika-biru")
PARTS = sys.argv[1:] or ["harbour", "compass", "anchor", "flags", "knot", "ring", "stripe"]
NAVY, NAVY_D, NAVY_L, WHITE, RED, RED_D, BRASS, SEA, ROPE, YEL = "#1b2a4a", "#0f1930", "#35507e", "#f5f2ea", "#c23b2e", "#8e2820", "#b8893a", "#4f7fa8", "#d9c39a", "#e8b632"


def rect(W, H, x0, y0, x1, y1):
    return shape_mask(W, H, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False)


def paint(art, m, col, col2=None, seed=1, shade=0.4, dark=NAVY_D, dx=-5, dy=-5, rough=1.4):
    art = GP(art, m, col, col2 or col, seed=seed, rough=rough, streak=0.8)
    if shade:
        art = tint(art, side_light(m, dx, dy, 4) * m, dark, shade * 0.6, seed=seed + 1)
    return art


# ------------------------------------------------------------------ harbour
def boat(art, W, H, x, y, L, rng, seed, sail=WHITE, hull=NAVY, stripe=WHITE, pennant=RED):
    """Sloop: hull with stripe, mast, mainsail + jib. (x, y) = waterline centre, L = hull length."""
    h = L * 0.16
    hull_m = shape_mask(W, H, [(x - L * .5, y - h), (x + L * .55, y - h * 1.05), (x + L * .38, y + h * .25), (x - L * .38, y + h * .25)], smooth=False)
    mast_x = x - L * 0.02; top = y - L * 1.15
    # sails first (behind hull top edge)
    main = shape_mask(W, H, [(mast_x - 3, top + L * .04), (mast_x - 3, y - h * 1.2), (x - L * .46, y - h * 1.25)] , smooth=False)
    main = np.maximum(main, shape_mask(W, H, [(mast_x - 3, top + L * .04), (mast_x - L * .1, top + L * .5), (x - L * .46, y - h * 1.25), (mast_x - 3, y - h * 1.25)], smooth=True) * 0)
    jib = shape_mask(W, H, [(mast_x + 3, top + L * .14), (x + L * .5, y - h * 1.15), (mast_x + 3, y - h * 1.15)], smooth=False)
    art = paint(art, main, sail, mix(sail, "#e6dfcf", .5), seed=seed, shade=.5, dark="#a9a49a", dx=6, dy=0)
    art = paint(art, jib, sail, "#ece6d8", seed=seed + 1, shade=.35, dark="#a9a49a", dx=6, dy=0)
    seams = []
    for t in (0.3, 0.55, 0.78):
        yy = top + (y - h * 1.2 - top) * t
        seams.append(([(mast_x - 3, yy), (mast_x - 3 - (mast_x - x + L * .46) * t, yy + L * .03)], 1.4, None))
    art = OV(art, strokes(W, H, seams) * main, lambda m: col_arr(m, "#b9b2a4", m * .7), pad=4)
    mast = strokes(W, H, [([(mast_x, y - h), (mast_x, top)], max(2.5, L * .016), None)])
    art = paint(art, mast, "#6b4a2a", seed=seed + 2, shade=.3, rough=.5)
    boom = strokes(W, H, [([(mast_x, y - h * 1.3), (x - L * .5, y - h * 1.32)], max(2.2, L * .013), None)])
    art = paint(art, boom, "#6b4a2a", seed=seed + 3, shade=.2, rough=.5)
    pen = shape_mask(W, H, [(mast_x, top - 1), (mast_x + L * .16, top + L * .03), (mast_x, top + L * .06)], smooth=False)
    art = paint(art, pen, pennant, seed=seed + 4, shade=.2, rough=.6)
    art = paint(art, hull_m, hull, NAVY_L, seed=seed + 5, shade=.5, dark=NAVY_D, dx=0, dy=-6)
    band = shape_mask(W, H, [(x - L * .49, y - h * .78), (x + L * .53, y - h * .82), (x + L * .5, y - h * .62), (x - L * .47, y - h * .58)], smooth=False)
    art = paint(art, band, stripe, seed=seed + 6, shade=0, rough=.6)
    return art


def part_harbour():
    W, H = 780, 620
    rng = random.Random(4)
    art = painted_sky(W, H, [(0, "#b4cde0"), (0.38, "#e2eae8"), (0.55, "#f3eee2"), (0.56, "#7ea4c0"), (0.75, "#3e6890"), (1, "#1c2e50")], seed=3, streak=0.35, grain=0.3)
    # clouds
    cl = []
    for (cx, cy, s) in [(150, 90, 1.0), (520, 60, 0.8), (680, 150, 0.6), (330, 160, 0.5)]:
        for k in range(6):
            cl.append((cx + (k - 2.5) * 34 * s + rng.uniform(-8, 8), cy + rng.uniform(-10, 8) * s, 22 * s + rng.uniform(0, 14) * s))
    cm = circles(W, H, cl)
    cm = np.minimum(cm, (np.mgrid[0:H, 0:W][0] < np.array([c[1] for c in cl]).max() + 14).astype(np.float32))
    art = GP(art, cm, "#fbf8f1", "#eef0ec", seed=5, rough=4.0, streak=0.5)
    art = tint(art, np.clip(np.roll(cm, -8, 0) * 0 + side_light(cm, 0, -10, 6), 0, 1), "#b7c6d2", 0.5, seed=6)
    # headland on the horizon
    hz = 344
    hill = shape_mask(W, H, [(-10, hz + 2)] + [(x, hz - 28 - 22 * math.sin(x / 90) - rng.uniform(0, 6)) for x in range(0, 380, 30)] + [(400, hz + 2)], smooth=True)
    art = paint(art, hill, "#93a8b8", "#a8b8c2", seed=7, shade=.2, dark="#6f8597")
    # breakwater + lighthouse
    rocks = []
    for k in range(16):
        rocks.append((520 + k * 18 + rng.uniform(-6, 6), hz + 10 + rng.uniform(-4, 6), rng.uniform(14, 24), rng.uniform(9, 14), rng.uniform(-20, 20)))
    rk = ellipses(W, H, rocks)
    art = paint(art, rk, "#5d6670", "#7b828a", seed=8, shade=.6, dark="#2c333b")
    lx, ltop, lbot = 640, 178, hz + 2
    tower = shape_mask(W, H, [(lx - 26, lbot), (lx - 17, ltop), (lx + 17, ltop), (lx + 26, lbot)], smooth=False)
    art = paint(art, tower, WHITE, "#e8e2d6", seed=9, shade=.55, dark="#9d988c", dx=7, dy=0)
    yy = np.mgrid[0:H, 0:W][0]
    bands = tower * (((yy - ltop) // 34) % 2 == 0)
    art = paint(art, bands.astype(np.float32), RED, "#d0503f", seed=10, shade=.5, dark=RED_D, dx=7, dy=0, rough=.6)
    gal = rect(W, H, lx - 24, ltop - 6, lx + 24, ltop + 2)
    art = paint(art, gal, NAVY, seed=11, shade=.2)
    lamp = rect(W, H, lx - 12, ltop - 30, lx + 12, ltop - 6)
    art = OV(art, glow(lamp, "#fff1b8", radius=14, strength=.5), lambda m: m, pad=0) if False else art
    g = glow(lamp, "#fff3c4", radius=12, strength=.55)
    art = over(art, g)
    art = paint(art, lamp, "#f6e7a6", "#fff6d6", seed=12, shade=0, rough=.4)
    art = OV(art, strokes(W, H, [([(lx - 4, ltop - 30), (lx - 4, ltop - 6)], 2, None), ([(lx + 5, ltop - 30), (lx + 5, ltop - 6)], 2, None)]), lambda m: col_arr(m, NAVY, m * .8), pad=3)
    cap = shape_mask(W, H, [(lx - 17, ltop - 29), (lx, ltop - 48), (lx + 17, ltop - 29)], smooth=False)
    art = paint(art, cap, RED_D, seed=13, shade=.3)
    # sea dabs: light catches on the upper wave edges, dark troughs below
    hi, lo = [], []
    for k in range(420):
        y = rng.uniform(hz + 6, H - 4)
        depth = (y - hz) / (H - hz)
        x = rng.uniform(-10, W + 10)
        L = 8 + depth * 46 * rng.uniform(.5, 1.0)
        wd = 1.2 + depth * 5
        pts = [(x - L / 2, y), (x, y - wd * .5), (x + L / 2, y)]
        (hi if rng.random() < .5 else lo).append((pts, wd, (0.3, 0.4)))
    art = GP(art, strokes(W, H, lo), "#173055", "#21406a", seed=14, rough=.8, streak=.4)
    art = GP(art, strokes(W, H, hi), "#9fc0d6", "#d9e7ee", seed=15, rough=.8, streak=.4)
    # boats + reflections
    art = boat(art, W, H, 470, hz + 26, 70, rng, 40, hull=RED, stripe=WHITE, pennant=NAVY)
    art = boat(art, W, H, 90, hz + 14, 40, rng, 50, hull=NAVY_L, stripe=WHITE)
    refl = []
    for (bx, by, L, col) in [(470, hz + 26, 70, RED), (230, 520, 200, NAVY)]:
        for k in range(10):
            x = bx + rng.uniform(-L * .45, L * .45); y = by + 8 + k * L * .05
            refl.append(([(x - L * .08, y), (x + L * .08, y + 1)], 2 + L * .02, (0.3, 0.3)))
    art = GP(art, strokes(W, H, refl), "#e9e4d8", "#c7d4dc", seed=16, rough=.8, density=.45)
    art = boat(art, W, H, 230, 520, 200, rng, 60)
    # foam at the bow
    foam = strokes(W, H, [([(150, 528), (210, 524), (330, 522)], 6, (0.3, 0.3)), ([(320, 516), (350, 522), (372, 532)], 5, (0.2, 0.5))])
    art = GP(art, foam, "#f4f4ee", seed=17, rough=1.2, streak=.3)
    # gulls
    gulls = []
    for (gx, gy, s) in [(330, 120, 14), (372, 100, 10), (560, 210, 9)]:
        gulls.append(([(gx - s, gy - s * .2), (gx - s * .45, gy - s * .45), (gx, gy)], 2.2, (0.2, 0.1)))
        gulls.append(([(gx, gy), (gx + s * .45, gy - s * .45), (gx + s, gy - s * .2)], 2.2, (0.1, 0.2)))
    art = OV(art, strokes(W, H, gulls), lambda m: col_arr(m, "#2a3346", m * .9), pad=4)
    art = add_grain(art, 3, 0.03)
    preview(art, "nau-harbour")
    save_rgb(art, f"{OUT}/harbour.webp", size=(700, 556), quality=74)


# ------------------------------------------------------------------ compass
def part_compass():
    W = H = 420
    c = W / 2
    rng = random.Random(9)
    art = blank(W, H)
    art = brass(art, ring_mask(W, H, c, c, 186, 26), BRASS, seed=1)
    art = OV(art, ring_mask(W, H, c, c, 172, 2.5), lambda m: col_arr(m, "#5a3d14", m * .7), pad=4)
    face = circle_mask(W, H, c, c, 171)
    art = GP(art, face, "#f3ece0", "#e9e0cf", seed=2, rough=.6, streak=.6)
    art = tint(art, side_light(face, 8, 8, 10) * face, "#c9bca3", .35, seed=3)
    ticks = []
    for k in range(72):
        a = k / 72 * 2 * math.pi
        r0 = 158 if k % 9 == 0 else 150 if k % 3 == 0 else 162 - 4
        ticks.append(([(c + math.cos(a) * r0, c + math.sin(a) * r0), (c + math.cos(a) * 168, c + math.sin(a) * 168)], 2.6 if k % 9 == 0 else 1.5, None))
    art = OV(art, strokes(W, H, ticks), lambda m: col_arr(m, NAVY, m * .85), pad=4)
    art = OV(art, ring_mask(W, H, c, c, 128, 1.6), lambda m: col_arr(m, NAVY, m * .6), pad=4)
    # star: diagonals (short, red), cardinals (long, navy), each point split light/dark
    for (n, R, r, c1, c2, off) in [(4, 104, 20, RED, RED_D, math.pi / 4), (4, 150, 24, NAVY_L, NAVY, 0.0)]:
        for k in range(n):
            a = -math.pi / 2 + off + k * 2 * math.pi / n
            tip = (c + math.cos(a) * R, c + math.sin(a) * R)
            l = (c + math.cos(a - math.pi / 2) * r, c + math.sin(a - math.pi / 2) * r)
            rr = (c + math.cos(a + math.pi / 2) * r, c + math.sin(a + math.pi / 2) * r)
            art = GP(art, shape_mask(W, H, [(c, c), l, tip], smooth=False), c1, seed=10 + k, rough=.6, streak=.6)
            art = GP(art, shape_mask(W, H, [(c, c), tip, rr], smooth=False), c2, seed=20 + k, rough=.6, streak=.6)
    north = shape_mask(W, H, [(c - 9, 30), (c + 9, 30), (c, 12)], smooth=False)
    art = GP(art, north, RED, seed=30, rough=.5)
    art = brass(art, circle_mask(W, H, c, c, 16), BRASS, seed=31)
    art = OV(art, circle_mask(W, H, c - 4, c - 4, 4), lambda m: col_arr(m, "#fff4cf", m * .8), pad=3)
    art = over(soft_shadow(circle_mask(W, H, c, c, 199), "#0f1930", 8, .3, 4, 6), art)
    preview(art, "nau-compass", bg="#f5f2ea")
    save(art, f"{OUT}/compass.webp", max_w=360, quality=80)


# ------------------------------------------------------------------ anchor
def part_anchor():
    W, H = 320, 400
    rng = random.Random(3)
    art = blank(W, H)
    cx = 160
    shank = rect(W, H, cx - 11, 70, cx + 11, 330)
    ring = ring_mask(W, H, cx, 46, 24, 10)
    stock = shape_mask(W, H, [(cx - 82, 92), (cx + 82, 92), (cx + 86, 110), (cx - 86, 110)], smooth=False)
    stock = np.maximum(stock, circles(W, H, [(cx - 86, 101, 11), (cx + 86, 101, 11)]))
    arm = strokes(W, H, [(arc_pts(cx, 230, 104, math.radians(15), math.radians(165), 30), 20, None)])
    fl = shape_mask(W, H, [(cx + 112, 240), (cx + 128, 196), (cx + 84, 266)], smooth=False)
    fr = shape_mask(W, H, [(cx - 112, 240), (cx - 128, 196), (cx - 84, 266)], smooth=False)
    crown = shape_mask(W, H, [(cx - 22, 320), (cx + 22, 320), (cx, 352)], smooth=False)
    body = np.clip(shank + arm + fl + fr + crown, 0, 1)
    art = paint(art, body, NAVY, NAVY_L, seed=1, shade=.65)
    art = brass(art, ring, BRASS, seed=2)
    art = paint(art, stock, "#7a5532", "#966a40", seed=3, shade=.5, dark="#3c2614")
    art = brass(art, rect(W, H, cx - 16, 88, cx + 16, 114), BRASS, seed=4)
    # highlight along the lit edge
    art = tint(art, np.clip(side_light(body, 4, 4, 2), 0, 1) * body, "#6f87b2", .5, seed=5)
    # rope wrapped around the shank, trailing off
    rp = [(cx + 40 * math.sin(t * 2.2 + 0.5), 60 + t * 270) for t in np.linspace(0, 1, 60)]
    rp += [(cx + 40 * math.sin(2.2 + 0.5) + k * 6, 330 + k * 4 - k * k * .3) for k in range(1, 18)]
    art = rope(art, W, H, rp, 11, seed=6, col=ROPE)
    preview(art, "nau-anchor", bg="#f5f2ea")
    save(art, f"{OUT}/anchor.webp", max_w=240, quality=82)


# ------------------------------------------------------------------ signal flags (decorative only)
def flag_masks(W, H, x, y, w, h, design, sway):
    """Return list of (mask, colour) for one flag hanging from (x, y). Patterns are decorative, never a message."""
    sk = lambda u, v: (x + u + v * sway, y + v)  # noqa: E731
    out = []
    def quad(u0, v0, u1, v1):
        return shape_mask(W, H, [sk(u0, v0), sk(u1, v0), sk(u1, v1), sk(u0, v1)], smooth=False)
    full = quad(0, 0, w, h)
    if design == "tri":
        out = [(full, WHITE), (quad(0, 0, w, h / 3), NAVY), (quad(0, h * 2 / 3, w, h), NAVY)]
    elif design == "diag":
        out = [(full, YEL), (shape_mask(W, H, [sk(w, 0), sk(w, h), sk(0, h)], smooth=False), RED)]
    elif design == "check":
        out = [(full, WHITE), (quad(0, 0, w / 2, h / 2), NAVY), (quad(w / 2, h / 2, w, h), NAVY)]
    elif design == "border":
        out = [(full, NAVY), (quad(w * .28, h * .28, w * .72, h * .72), WHITE)]
    elif design == "vert":
        out = [(full, RED), (quad(w / 3, 0, w * 2 / 3, h), WHITE)]
    elif design == "pennant":
        full = shape_mask(W, H, [sk(0, 0), sk(w, 0), sk(w * .5, h * 1.35)], smooth=False)
        out = [(full, RED), (shape_mask(W, H, [sk(w * .25, 0), sk(w * .75, 0), sk(w * .5, h * .7)], smooth=False), WHITE)]
    elif design == "yb":
        out = [(full, YEL), (quad(0, h / 2, w, h), NAVY)]
    return full, out


def part_flags():
    W, H = 860, 190
    rng = random.Random(12)
    art = blank(W, H)
    line = [(x, 12 + 44 * math.sin(math.pi * min(max(x, 0), W) / W)) for x in np.linspace(-6, W + 6, 80)]
    designs = ["tri", "diag", "check", "pennant", "border", "vert", "yb", "pennant", "diag", "tri", "check", "vert"]
    n = len(designs)
    flags = []
    for i, d in enumerate(designs):
        x = 30 + i * (W - 60) / (n - 1) - 24
        y = 12 + 44 * math.sin(math.pi * (x + 24) / W) + 6
        flags.append((x, y, 48, 58, d, rng.uniform(-.12, .12)))
    ties = [([(x + 4, y - 7), (x + 4, y + 2)], 1.8, None) for (x, y, w, h, d, sw) in flags] + [([(x + w - 4, y - 7), (x + w - 4, y + 2)], 1.8, None) for (x, y, w, h, d, sw) in flags]
    art = OV(art, strokes(W, H, ties), lambda m: col_arr(m, "#7d6040", m * .9), pad=3)
    for k, (x, y, w, h, d, sw) in enumerate(flags):
        full, parts = flag_masks(W, H, x, y, w, h, d, sw)
        for j, (m, col) in enumerate(parts):
            art = GP(art, m, col, mix(col, "#ffffff", .12), seed=100 + k * 7 + j, rough=1.0, streak=.6)
        # cloth folds: soft vertical shade bands
        xx = np.mgrid[0:H, 0:W][1].astype(np.float32)
        fold = (0.5 + 0.5 * np.sin((xx - x) / w * math.pi * 2.2 + k)) * full
        art = tint(art, fold * full, "#0f1930", .22, seed=200 + k)
        art = tint(art, side_light(full, -3, -3, 3) * full, "#0f1930", .3, seed=300 + k)
    art = rope(art, W, H, line, 5, seed=7, col=ROPE, dark="#7d6040")
    preview(art, "nau-flags", tone="#f5f2ea")
    save(art, f"{OUT}/flags.webp", max_w=820, quality=80)


def part_knot():
    W, H = 460, 100
    art = blank(W, H)
    cx, cy = W / 2, H / 2
    cy = cy + 12
    left = [(10.0, cy)] + [(float(x), cy + 2 * math.sin(x / 30)) for x in range(40, int(cx - 36), 12)]
    R = 24; ox, oy = cx, cy - 22
    loop = [(ox + math.cos(a) * R * 1.25, oy + math.sin(a) * R) for a in np.linspace(math.pi * .62, math.pi * .62 + 2 * math.pi * .86, 50)]
    right = [(cx + 30.0, cy)] + [(float(x), cy + 2 * math.sin(x / 30)) for x in range(int(cx + 44), W - 10, 12)] + [(W - 10.0, cy)]
    art = rope(art, W, H, left + loop + right, 10, seed=3, col=ROPE)
    # crossing: the outgoing strand passes over the loop's foot
    art = rope(art, W, H, [(cx - 30.0, cy - 2), (cx, cy + 2), (cx + 34.0, cy)], 10, seed=4, col=ROPE)
    for ex in (12, W - 12):
        art = brass(art, rect(W, H, ex - 6, cy - 7, ex + 6, cy + 7), BRASS, seed=9)
    preview(art, "nau-knot", tone="#f5f2ea")
    save(art, f"{OUT}/knot.webp", max_w=420, quality=82)


def part_ring():
    W = H = 540
    c = W / 2
    art = blank(W, H)
    rng_m = ring_mask(W, H, c, c, 236, 44)
    art = brass(art, rng_m, BRASS, seed=1, amt=.65)
    art = OV(art, ring_mask(W, H, c, c, 214, 3), lambda m: col_arr(m, "#4a3210", m * .8), pad=4)
    art = OV(art, ring_mask(W, H, c, c, 258, 2), lambda m: col_arr(m, "#6a4a1c", m * .6), pad=4)
    bolts = []
    for k in range(8):
        a = k / 8 * 2 * math.pi + math.pi / 8
        bolts.append((c + math.cos(a) * 236, c + math.sin(a) * 236))
    for k, (bx, by) in enumerate(bolts):
        art = over(art, soft_shadow(circle_mask(W, H, bx, by, 9), "#3a2508", 2, .6, 2, 3))
        art = brass(art, circle_mask(W, H, bx, by, 9), "#c79a48", seed=10 + k, amt=.7)
        art = OV(art, strokes(W, H, [([(bx - 5, by), (bx + 5, by)], 2, None)]), lambda m: col_arr(m, "#4a3210", m * .7), pad=3)
    preview(art, "nau-ring", bg="#1b2a4a")
    save(art, f"{OUT}/ring.webp", max_w=480, quality=80)


def part_stripe():
    S = 256
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    wob = (wrap_noise(S, S, 3, 18) - 0.5) * 7 + (wrap_noise(S, S, 4, 4) - .5) * 1.6
    period = 64
    v = (yy + wob) % period
    m = np.clip((26 - np.abs(v - 32)) * 0.6, 0, 1)
    fab = wrap_noise(S, S, 8, 1.2)
    streak = gaussian_filter(np.random.default_rng(2).random((S, S)).astype(np.float32), (0.6, 8), mode="wrap")
    streak = (streak - streak.mean()) / (streak.std() + 1e-6)
    nav = np.array(hex_rgb("#1e2f52"), np.float32); wht = np.array(hex_rgb("#f5f2ea"), np.float32)
    rgb = wht * (1 - m[..., None]) + nav * m[..., None]
    rgb = rgb * (1 + (fab[..., None] - .5) * 0.05 + streak[..., None] * 0.018)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{OUT}/stripe.webp", "WEBP", quality=76, method=6)
    print("stripe.webp", os.path.getsize(f"{OUT}/stripe.webp") // 1024, "KB")


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
