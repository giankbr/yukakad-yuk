"""Sabu Raijua — Sabu ikat (dark indigo-brown ground, white and madder-red flower motifs), lontar (palmyra) palms and
the karst islets of the Savu Sea. Run: python3 -I sabu-raijua.py [part ...]
parts: ikat scene lontar flower. Assets -> public/themes/art/sabu-raijua/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m4_lib import *

OUT = outdir("sabu-raijua")
PARTS = sys.argv[1:] or ["ikat", "scene", "lontar", "flower"]
INDIGO, INDIGO_D, BROWN = "#1e1b2a", "#14121c", "#4a2c1e"
WHITE, RED, RED_D, OCHRE = "#efe6d2", "#b0322a", "#7c1f1a", "#c98f3c"


def loz(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


def rosette(cx, cy, r, rot=0.0):
    """Sabu flower: 8 lozenge petals (alternating long/short) -> list of polygons."""
    out = []
    for k in range(8):
        a = rot + k * math.pi / 4
        L = r if k % 2 == 0 else r * 0.72
        wd = r * (0.3 if k % 2 == 0 else 0.22)
        tip = (cx + math.cos(a) * L, cy + math.sin(a) * L)
        mid = (cx + math.cos(a) * L * 0.5, cy + math.sin(a) * L * 0.5)
        side = (math.cos(a + math.pi / 2) * wd, math.sin(a + math.pi / 2) * wd)
        base = (cx + math.cos(a) * r * 0.18, cy + math.sin(a) * r * 0.18)
        out.append([base, (mid[0] + side[0], mid[1] + side[1]), tip, (mid[0] - side[0], mid[1] - side[1])])
    return out


def wrap(polys, W, H, both=True):
    out = []
    for p in polys:
        for dx in (-W, 0, W):
            for dy in ((-H, 0, H) if both else (0,)):
                out.append([(x + dx, y + dy) for x, y in p])
    return out


def ikat_tile(W=320, H=320, seed=40000):
    nx = Seq(seed)
    white, red, och, brown = [], [], [], []
    # main band: big rosettes in lozenge cages
    for i in range(4):
        cx, cy = i * 80 + 40, 86
        white += rosette(cx, cy, 30, 0)
        red.append(loz(cx, cy, 9, 9))
        white.append(loz(cx, cy, 3.5, 3.5))
        # small red flowers between
        x2 = i * 80
        red += rosette(x2, cy, 13, math.pi / 8)
        white.append(loz(x2, cy, 3, 3))
        # cage hooks
        for sy in (-1, 1):
            och.append([(x2 - 6, cy + sy * 26), (x2, cy + sy * 20), (x2 + 6, cy + sy * 26), (x2, cy + sy * 32)])
    # second band: offset small four-petal flowers (kaliwu) and lozenge chain
    for i in range(8):
        cx, cy = i * 40 + 20, 222
        if i % 2 == 0:
            white += rosette(cx, cy, 17, math.pi / 8)
            red.append(loz(cx, cy, 5, 5))
        else:
            red.append(loz(cx, cy, 12, 17))
            white.append(loz(cx, cy, 6, 9))
            red.append(loz(cx, cy, 2.5, 3.5))
    # zigzag teeth band
    for i in range(16):
        x = i * 20
        white.append([(x, 160), (x + 10, 150), (x + 20, 160)])
        red.append([(x, 160), (x + 10, 170), (x + 20, 160)])
    stripes_w = [[(0, y), (W, y), (W, y + t), (0, y + t)] for y, t in ((44, 3), (128, 3), (180, 2), (264, 2))]
    stripes_r = [[(0, y), (W, y), (W, y + t), (0, y + t)] for y, t in ((36, 4), (136, 4), (186, 3), (256, 3))]
    brown = [[(0, 290), (W, 290), (W, 330), (0, 330)], [(0, -30), (W, -30), (W, 14), (0, 14)]]
    mb = shapes(W, H, brown, smooth=False)
    mw = np.maximum(shapes(W, H, wrap(white, W, H), smooth=False), shapes(W, H, stripes_w, smooth=False))
    mr = np.maximum(shapes(W, H, wrap(red, W, H), smooth=False), shapes(W, H, stripes_r, smooth=False))
    mo = shapes(W, H, wrap(och, W, H), smooth=False)
    thin = shapes(W, H, [[(0, y), (W, y), (W, y + 1.4), (0, y + 1.4)] for y in (296, 302, 308, 2, 8)], smooth=False)
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(INDIGO), np.float32)
    # indigo dye unevenness (vertical warp lots)
    lot = gaussian_filter(rng.random((1, W)).astype(np.float32), (0, 3), mode="wrap")
    rgb *= (0.9 + 0.25 * (lot - lot.min()) / (np.ptp(lot) + 1e-6))[..., None]
    for m, col, amt in ((mb, BROWN, 1.0), (thin, RED_D, 1.5), (mo, OCHRE, 2.5), (mr, RED, 2.8), (mw, WHITE, 2.8)):
        mm = ikat_bleed(m, nx(), amt)
        c = np.array(hex_rgb(col), np.float32)
        rgb = rgb * (1 - mm[..., None]) + c * mm[..., None]
    rgb *= weave(H, W, nx(), 0.07)[..., None]
    rgb = np.clip(rgb, 0, 1)
    return np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)


def lontar(art, W, H, x, by, h, rng, nx, lean=0.0, scale=1.0, dark=False):
    rng = random.Random(int(x * 7 + h))
    """Palmyra palm: tall straight trunk, round head of stiff pleated fan leaves, a skirt of dried fans."""
    top = (x + lean * h, by - h)
    trunk_pts = curve([(x, by), (x + lean * h * 0.45, by - h * 0.5), top], 40)
    tw = 13 * scale
    tm = strokes(W, H, [(trunk_pts, tw, (0.0, 0.0))])
    art = GP(art, tm, "#3e3128" if not dark else "#2e2620", "#5e4a3c", seed=nx(), rough=1.0, streak=1.0)
    lit = tm * (np.mgrid[0:H, 0:W][1].astype(np.float32) < (np.interp(np.arange(H), [p[1] for p in trunk_pts[::-1]], [p[0] for p in trunk_pts[::-1]])[:, None] - tw * 0.1))
    art = G(art, lit, "#8a7058", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=1)
    ringsm = strokes(W, H, [([(px - tw * 0.6, py), (px + tw * 0.6, py + 1.5)], 1.1 * scale, None) for px, py in trunk_pts[2:-2:2]])
    art = G(art, ringsm * tm, "#241a14", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8)
    cx, cy = top
    R = 70 * scale
    core = circles(W, H, [(cx, cy + R * 0.05, R * 0.36)])
    art = G(art, core, "#2a3420", "#3a3a24", seed=nx(), density=0.95, edge=0.3, bloom=0.1, rough=2)

    def fan(a, L, spread=0.5):
        b0 = (cx + math.cos(a) * L * 0.3, cy + math.sin(a) * L * 0.3 + L * 0.04)
        arc = []
        n = 15
        for j in range(n):
            t = a - spread + 2 * spread * j / (n - 1)
            rr = L * (1.0 if j % 2 == 0 else 0.62) * (0.85 + 0.15 * math.sin(math.pi * j / (n - 1)))
            arc.append((b0[0] + math.cos(t) * rr * 0.8, b0[1] + math.sin(t) * rr * 0.8 + L * 0.05 * (j / n)))
        return b0, arc

    order = []
    for k in range(6):  # dried skirt below
        a = math.pi / 2 + (k - 2.5) * 0.4 + rng.uniform(-0.1, 0.1)
        order.append(("dry", a, R * rng.uniform(0.75, 0.9)))
    n = 10
    for k in range(n):
        a = -math.pi * 1.1 + k * (math.pi * 1.2) / (n - 1) + rng.uniform(-0.08, 0.08)
        order.append(("live", a, R * rng.uniform(0.9, 1.1)))
    # paint back (upper) fans first, then side fans, so the head has depth
    order.sort(key=lambda o: (o[0] != "dry", math.sin(o[1]) if o[0] == "live" else -2))
    for kind, a, L in order:
        b0, arc = fan(a, L, 0.42 if kind == "dry" else 0.5)
        m = shapes(W, H, [[b0] + arc], smooth=False)
        stem = strokes(W, H, [([(cx, cy), b0], 2.6 * scale, None)])
        pl = strokes(W, H, [([b0, q], 0.9 * scale, (0.05, 0.5)) for q in arc[0::2]])
        if kind == "dry":
            art = G(art, m, "#9a7444", "#6e5030", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
            art = G(art, pl * m, "#4e3820", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
        else:
            sun = math.cos(a) < 0.1  # light from the left
            c1, c2 = (("#6f8a44", "#8c9a52") if sun else ("#2e4a2c", "#3e5a34")) if not dark else ("#263826", "#34482c")
            art = G(art, stem, "#3a4a28", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.8)
            art = G(art, m, c1, c2, seed=nx(), density=0.95, edge=0.6, bloom=0.25, rough=1.4, feather=0.7)
            art = G(art, pl * m, "#1a2a16", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
    fr = circles(W, H, [(cx + rng.uniform(-9, 9) * scale, cy + rng.uniform(6, 14) * scale, 4.5 * scale) for _ in range(7)])
    art = G(art, fr, "#20160f", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=1)
    clear()
    return art


if "ikat" in PARTS:
    t = ikat_tile()
    prev(np.concatenate([np.concatenate([t, t], 1)] * 2, 0), "sb-ikat")
    save_rgb(t, f"{OUT}/ikat.webp", quality=80)

if "flower" in PARTS:
    # a small woven patch: indigo lozenge with the white flower, red heart, ochre hooks — node / amp / divider emblem
    W = H = 240
    nx = Seq(41000)
    cx = cy = 120
    patch = shapes(W, H, [loz(cx, cy, 104, 104)], smooth=False)
    white = shapes(W, H, rosette(cx, cy, 64, 0) + [loz(cx, cy, 7, 7)] + [loz(cx + dx, cy + dy, 8, 8) for dx, dy in ((0, -88), (88, 0), (0, 88), (-88, 0))], smooth=False)
    red = shapes(W, H, [loz(cx, cy, 20, 20)] + rosette(cx, cy, 30, math.pi / 8), smooth=False)
    rim = np.clip(shapes(W, H, [loz(cx, cy, 104, 104)], smooth=False) - shapes(W, H, [loz(cx, cy, 94, 94)], smooth=False), 0, 1)
    def bl(m, a=2.0):
        return ikat_bleed(m, nx(), a, wrap=False)
    art = blank(W, H)
    pm = bl(patch, 2.5)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(INDIGO), np.float32) * weave(H, W, nx(), 0.08)[..., None]
    a = pm.copy()
    for m, col in ((bl(rim), RED), (bl(red), RED), (bl(white), WHITE)):
        mm = m * pm
        rgb = rgb * (1 - mm[..., None]) + np.array(hex_rgb(col), np.float32) * mm[..., None]
    art = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
    prev(art, "sb-flower", "#f1e7d4")
    save(art, f"{OUT}/flower.webp", max_w=120, quality=84)

if "scene" in PARTS:
    # the Savu Sea in the late dry season: pale hot sky, deep blue sea, turquoise reef flats, karst islets with
    # undercut feet, lontar palms on a coral-rock shore with golden grass
    W, H = 720, 720
    nx = Seq(42000)
    rng = random.Random(9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#e8c99c"), (0.25, "#f1dbb4"), (0.42, "#f7e9cf"), (0.5, "#f5e6c9"), (1, "#f5e6c9")], seed=nx(), streak=0.8)
    # sun low left, haze
    art = soft(art, circles(W, H, [(190, 250, 34)]), "#fff6e2", alpha=0.95, blur=2)
    art = soft(art, circles(W, H, [(190, 250, 140)]), "#fbe3b8", alpha=0.35, blur=40)
    # a few dry-season clouds, long and thin
    for (cx, cy, w, h) in ((470, 150, 260, 22), (560, 196, 180, 14), (120, 120, 160, 12)):
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, w / 2, h / 2, 14), rng, 2, 0.08)])
        art = G(art, m, "#fbf3e4", "#e9d3b5", seed=nx(), density=0.7, edge=0.3, bloom=0.5, rough=6, feather=3)
    clear()
    hz = 352
    sea = shapes(W, H, [[(-10, hz), (W + 10, hz), (W + 10, H), (-10, H)]], smooth=False)
    art = GP(art, sea, "#24607e", "#2d6f8c", seed=nx(), rough=0.6, streak=1.2)
    art = soft(art, sea * np.clip((yy - hz) / 160, 0, 1), "#1f5470", alpha=0.6)
    # light streaks on water, glitter path under the sun
    st = strokes(W, H, [([(x, y), (x + rng.uniform(20, 70), y)], rng.uniform(1.0, 2.2), (0.3, 0.3)) for x, y in
                        [(rng.uniform(-20, W), rng.uniform(hz + 6, 560)) for _ in range(70)]])
    art = soft(art, st * sea, "#cfe6e6", alpha=0.45, pad=4)
    gl = strokes(W, H, [([(x, y), (x + rng.uniform(10, 30), y)], 1.6, (0.3, 0.3)) for x, y in
                        [(190 + rng.gauss(0, 30 + (yy0 - hz) * 0.3), yy0) for yy0 in [rng.uniform(hz + 4, 520) for _ in range(40)]]])
    art = soft(art, gl * sea, "#fff3d8", alpha=0.7, pad=4)
    clear()
    # far island ridge on horizon (Raijua)
    far = shapes(W, H, [[(380, hz + 1), (410, hz - 14), (470, hz - 20), (540, hz - 16), (600, hz - 22), (650, hz - 10), (690, hz + 1)]])
    art = G(art, far, "#7f8f9a", "#94a0a4", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=2)
    # karst islets: limestone with vertical cliffs, scrub cap, dark notch at waterline + reflection
    for (cx, base, w, h) in ((470, 420, 120, 78), (600, 404, 62, 50), (345, 396, 40, 30)):
        L, R = cx - w / 2, cx + w / 2
        nt = 9
        tops = []
        for j in range(nt):
            t = j / (nt - 1)
            hh = h * (0.78 + 0.22 * math.sin(math.pi * t) + rng.uniform(-0.06, 0.06))
            tops.append((L + w * 0.02 + t * w * 0.96, base - hh))
        body = [(L + w * 0.1, base), (L + w * 0.03, base - h * 0.35)] + tops + [(R - w * 0.03, base - h * 0.4), (R - w * 0.09, base)]
        m = shapes(W, H, [body], smooth=False)
        m = np.clip(gaussian_filter(m, 0.8), 0, 1)
        art = GP(art, m, "#c2ae90", "#a89272", seed=nx(), rough=1.4, streak=1.2)
        face = m * np.clip((xx - cx) / (w * 0.5), 0, 1)
        art = G(art, face, "#6e5e50", seed=nx(), density=0.7, edge=0.2, bloom=0.2, rough=2)
        vs = strokes(W, H, [([(x, base - h * rng.uniform(0.45, 0.7)), (x + rng.uniform(-2, 2), base - 4)], rng.uniform(1.0, 2.4), (0.2, 0.4)) for x in np.linspace(L + 6, R - 6, int(w / 6))])
        art = G(art, vs * m, "#5e4e42", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
        notch = m * np.clip(1 - (base - yy) / 9, 0, 1) * (yy < base)
        art = soft(art, notch, "#2c2620", alpha=0.85)
        topy = np.interp(xx[0], [p[0] for p in tops], [p[1] for p in tops])[None, :]
        capm = m * np.clip(1 - (yy - topy) / (h * 0.32), 0, 1) * (yy >= topy - 2)
        art = G(art, capm, "#4c6a38", "#6c7c42", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=2.5)
        cap = circles(W, H, [(px + rng.uniform(-5, 5), py + rng.uniform(-1, 4), rng.uniform(3, 7) * max(0.6, w / 120)) for px, py in tops for _ in range(3)])
        art = G(art, cap, "#3f5c30", "#5a7038", seed=nx(), density=0.9, edge=0.45, bloom=0.3, rough=2)
        refl = shapes(W, H, [[(L + 4, base), (R - 4, base), (R - 12, base + h * 0.45), (L + 12, base + h * 0.4)]])
        art = G(art, refl * np.clip(1 - (yy - base) / (h * 0.45), 0, 1), "#1d4458", seed=nx(), density=0.55, edge=0.1, bloom=0.3, rough=4)
        clear()
    # turquoise reef flat near shore
    reef = shapes(W, H, [[(-20, 520), (120, 500), (300, 512), (460, 506), (600, 520), (740, 512), (740, 600), (-20, 600)]])
    art = G(art, reef, "#3fa6a4", "#59b8ad", seed=nx(), density=0.85, edge=0.4, bloom=0.4, rough=5)
    art = G(art, reef * np.clip((yy - 540) / 50, 0, 1), "#9fd6c4", seed=nx(), density=0.6, edge=0.2, bloom=0.4, rough=4)
    foam = strokes(W, H, [(curve([(x, y), (x + 30, y - 2), (x + 70, y + 1)], 8), 2.2, (0.3, 0.3)) for x, y in
                          [(rng.uniform(-30, W), rng.uniform(548, 580)) for _ in range(22)]])
    art = soft(art, foam, "#f4f7ee", alpha=0.8, pad=4)
    clear()
    # shore: coral rock + golden dry grass, rising to the right
    shore = shapes(W, H, [[(-20, 590), (140, 578), (300, 586), (430, 574), (560, 560), (740, 540), (740, H + 10), (-20, H + 10)]])
    art = GP(art, shore, "#c9a464", "#b38a4e", seed=nx(), rough=2.2, streak=1.4)
    art = G(art, shore * np.clip((yy - 600) / 120, 0, 1), "#8a6432", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=3)
    grass = strokes(W, H, [([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(10, 26))], 1.4, (0.0, 0.8)) for x, y in
                           [(rng.uniform(-10, W + 10), rng.uniform(580, 700)) for _ in range(900)]])
    art = G(art, grass * (yy > 548), "#e2c07a", "#9c7438", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1)
    art = soft(art, np.clip((yy - 640) / 90, 0, 1), "#6e4e26", alpha=0.35, pad=0)
    clear()
    # a Sabu house (ammu) on the shore: low stilts, long boat-hull thatched roof of lontar leaves
    hx, hy, hw = 330, 574, 104
    roof = [(hx - hw * 0.64, hy - 50), (hx - hw * 0.4, hy - 41), (hx, hy - 38), (hx + hw * 0.4, hy - 41), (hx + hw * 0.64, hy - 50), (hx + hw * 0.5, hy - 17), (hx - hw * 0.5, hy - 17)]
    walls = shapes(W, H, [[(hx - hw * 0.4, hy - 20), (hx + hw * 0.4, hy - 20), (hx + hw * 0.4, hy - 4), (hx - hw * 0.4, hy - 4)]], smooth=False)
    posts = strokes(W, H, [([(hx + d, hy - 4), (hx + d, hy + 8)], 2.4, None) for d in (-40, -20, 0, 20, 40)])
    art = GP(art, posts, "#3a2a1e", seed=nx(), rough=0.6)
    art = GP(art, walls, "#7a5a3a", "#5e4430", seed=nx(), rough=0.8, streak=1.2)
    rm = shapes(W, H, [roof], smooth=False)
    art = GP(art, rm, "#9a7848", "#7a5a34", seed=nx(), rough=1.2, streak=1.6)
    th = strokes(W, H, [([(hx + d, hy - 38 - (abs(d) / 66) ** 2 * 12), (hx + d * 0.8, hy - 17)], 1.0, (0.1, 0.3)) for d in range(-64, 65, 5)])
    art = G(art, th * rm, "#4e3820", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
    art = soft(art, rm * (yy > hy - 22), "#3a2818", alpha=0.45)
    art = soft(art, ellipses(W, H, [(hx + 10, hy + 10, hw * 0.62, 6, 0)]), "#5e4022", alpha=0.35, blur=3)
    # a small perahu with a lontar-leaf sail near the islets
    bx, byy = 250, 432
    art = GP(art, shapes(W, H, [[(bx - 22, byy - 4), (bx + 22, byy - 4), (bx + 14, byy + 3), (bx - 16, byy + 3)]]), "#3a2a20", seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(bx - 2, byy - 6), (bx + 2, byy - 40), (bx + 20, byy - 8)]], smooth=False), "#efe2c6", "#d9c49c", seed=nx(), rough=0.8)
    art = soft(art, strokes(W, H, [([(bx - 26, byy + 6), (bx + 26, byy + 6)], 1.6, (0.3, 0.3))]), "#cfe6e6", alpha=0.6, pad=4)
    # grass tufts
    tufts = []
    for _ in range(26):
        tx, ty = rng.uniform(-10, W + 10), rng.uniform(600, 715)
        for _k in range(9):
            tufts.append(([(tx + rng.uniform(-5, 5), ty), (tx + rng.uniform(-16, 16), ty - rng.uniform(14, 30))], 1.8, (0.0, 0.8)))
    art = G(art, strokes(W, H, tufts), "#7a5a2a", "#a07a3a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
    clear()
    # lontar palms: two tall on the right, one mid left, a small one far
    art = lontar(art, W, H, 92, 616, 300, rng, nx, lean=-0.05, scale=1.0)
    art = lontar(art, W, H, 560, 590, 430, rng, nx, lean=0.04, scale=1.15)
    art = lontar(art, W, H, 648, 600, 330, rng, nx, lean=0.1, scale=0.95)
    art = add_grain(art, 3, 0.03)
    prev(art, "sb-scene", None)
    save_rgb(art, f"{OUT}/scene.webp", size=(600, 600), quality=80)

if "lontar" in PARTS:
    W, H = 360, 760
    nx = Seq(43000)
    rng = random.Random(21)
    art = blank(W, H)
    art = lontar(art, W, H, 150, 740, 560, rng, nx, lean=0.06, scale=1.5)
    grass = strokes(W, H, [([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(12, 34))], 1.6, (0.0, 0.8)) for x, y in
                           [(rng.uniform(70, 240), rng.uniform(730, 752)) for _ in range(70)]])
    art = G(art, grass, "#c9a464", "#8f6a36", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1)
    prev(art, "sb-lontar", "#f1e7d4")
    save(art, f"{OUT}/lontar.webp", max_w=220, quality=82)
