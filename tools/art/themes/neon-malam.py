"""Neon Malam — a night bar wall: old painted brick under low light, hand-bent neon tube signs in pink, teal and amber
(glass tube with a hot core, darker glass edges, black-painted electrode ends, metal clips, soft halo) and a hanging
Edison bulb (original design). Run: python3 -I neon-malam.py [part ...]
parts: brick sign heart cheers rings star wave bulb"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c4_lib import *

OUT = outdir("neon-malam")
PARTS = sys.argv[1:] or ["brick", "sign", "heart", "cheers", "rings", "star", "wave", "bulb"]
PINK, TEAL, AMBER = "#ff4fa3", "#2fe0d0", "#ffb547"
WALL_BG = "#1d1416"


def heart_pts(cx, cy, s, n=90, gap=0.0):
    pts = []
    for i in range(n + 1):
        t = gap / 2 + (math.tau - gap) * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s, cy + y * s))
    return pts


def ends(W, H, lines, width):
    """Black-painted electrode ends where a tube bends back through the sign."""
    items = []
    for l in lines:
        for (a, b) in ((l[0], l[1]), (l[-1], l[-2])):
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            items.append(([(a[0], a[1]), (a[0] + math.cos(ang) * width * 1.6, a[1] + math.sin(ang) * width * 1.6)], width * 1.05, None))
    return strokes(W, H, items, cap=True)


def tube(W, H, lines, col, width=7.0, seed=1, glow_scale=1.0, end_caps=True, clips=True):
    art = neon(W, H, lines, col, width=width, glow_r=(5 * glow_scale, 14 * glow_scale, 34 * glow_scale), glow_a=(0.85, 0.55, 0.32), seed=seed, clips=clips)
    if end_caps:
        art = over(art, flat(ends(W, H, lines, width), "#141015", 0.95))
    return art


if "brick" in PARTS:
    # seamless night brick: running bond, per-brick tone, chipped arrises, worn limewash, soot
    W, H, bw, bh, mort = 400, 240, 100, 30, 4.0
    rng = np.random.default_rng(83000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nrow = H // bh; ncol = W // bw
    row = np.floor(yy / bh).astype(int)
    xo = (xx + (row % 2) * bw / 2) % W
    col = np.floor(xo / bw).astype(int) % ncol
    fx = xo % bw; fy = yy % bh
    tones = rng.random((nrow, ncol)).astype(np.float32)
    tone = tones[row % nrow, col]
    wn = lambda sd, sg: wrap_noise(W, H, sd, sg)
    edge_n = (wn(1, 2.0) - 0.5) * 5
    inside = np.clip(np.minimum.reduce([fx - mort / 2, bw - mort / 2 - fx, fy - mort / 2, bh - mort / 2 - fy]) + edge_n, 0, 3) / 3
    ca, cb, cc = col_arr("#5a2f28"), col_arr("#3a1f1f"), col_arr("#6e3c2c")
    rgb = ca * (1 - tone[..., None]) + cb * tone[..., None]
    rgb = np.where((tone > 0.82)[..., None], cc * np.ones_like(rgb), rgb)
    rgb *= (0.82 + 0.34 * wn(2, 6.0))[..., None]
    pits = np.clip((wn(3, 0.8) - 0.62) * 6, 0, 1)
    rgb *= (1 - 0.35 * pits)[..., None]
    lime = np.clip((wn(4, 14.0) - 0.55) * 3, 0, 1) * np.clip((wn(5, 1.2) - 0.35) * 3, 0, 1)
    rgb = rgb * (1 - lime[..., None] * 0.45) + col_arr("#9c8f86") * lime[..., None] * 0.45
    hi = np.clip(1 - fy / 5, 0, 1) * inside
    rgb = rgb * (1 + hi[..., None] * 0.12)
    mortar = col_arr("#1a1214") * (0.8 + 0.4 * wn(6, 1.5))[..., None]
    rgb = rgb * inside[..., None] + mortar * (1 - inside[..., None])
    soot = wn(7, 30.0)
    rgb *= (0.78 + 0.25 * soot)[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    preview(arr, "nm-brick", bg="#000000")
    save_rgb(arr, f"{OUT}/brick.webp", quality=72)
    clear()

if "sign" in PARTS:
    # the cover sign: a teal tube frame (rounded, with a little dip at the top for the heart), pink heart on top,
    # amber squiggle under the names, cable dropping to the floor from the lower right
    W, H = 640, 820
    rng = random.Random(4)
    x0, y0, x1, y1, r = 40, 110, W - 40, H - 70, 70
    frame = []
    def arc(cx, cy, a0, a1, rr, n=18):
        return [(cx + math.cos(a0 + (a1 - a0) * i / (n - 1)) * rr, cy + math.sin(a0 + (a1 - a0) * i / (n - 1)) * rr) for i in range(n)]
    gap = 74
    top_l = [(W / 2 - gap, y0), (x0 + r, y0)]
    frame = top_l + arc(x0 + r, y0 + r, -math.pi / 2, -math.pi, r)[1:] + [(x0, y1 - r)] + arc(x0 + r, y1 - r, math.pi, math.pi / 2, r)[1:] + [(x1 - r, y1)] + arc(x1 - r, y1 - r, math.pi / 2, 0, r)[1:] + [(x1, y0 + r)] + arc(x1 - r, y0 + r, 0, -math.pi / 2, r)[1:] + [(W / 2 + gap, y0)]
    inner = []
    d = 18
    xi0, yi0, xi1, yi1, ri = x0 + d, y0 + d, x1 - d, y1 - d, r - d
    inner = [(xi0 + ri, yi0)] + [(W / 2 - gap + 6, yi0)]
    art = blank(W, H)
    # backing: smoked acrylic panel, barely visible, with four stand-off bolts
    panel = shapes(W, H, [[(x0 - 18, y0 - 22), (x1 + 18, y0 - 22), (x1 + 18, y1 + 22), (x0 - 18, y1 + 22)]], smooth=False)
    art = over(art, flat(panel, "#0d0a10", 0.28))
    art = over(art, flat(outline(panel, 2), "#ffffff", 0.06))
    bolts = circles(W, H, [(x0 - 4, y0 - 8, 6), (x1 + 4, y0 - 8, 6), (x0 - 4, y1 + 8, 6), (x1 + 4, y1 + 8, 6)])
    art = over(art, flat(bolts, "#8d8a95", 0.9))
    art = over(art, flat(circles(W, H, [(x0 - 6, y0 - 10, 2), (x1 + 2, y0 - 10, 2), (x0 - 6, y1 + 6, 2), (x1 + 2, y1 + 6, 2)]), "#e9e6f0", 0.8))
    # cable: from the lower right corner, sagging off the bottom
    cab = bez((x1 - 30, y1 + 22), (x1 - 20, H - 10), (x1 + 40, H - 30), (W + 10, H + 20), 40)
    art = over(art, flat(strokes(W, H, [(cab, 4.0, None)]), "#0a080b", 0.95))
    art = over(art, tube(W, H, [frame], TEAL, width=8.5, seed=11))
    heart = heart_pts(W / 2, y0 - 6, 3.4, gap=0.5)
    art = over(art, tube(W, H, [heart], PINK, width=8, seed=12))
    sq = [(x, y1 - 150 + 10 * math.sin((x - 150) / 26 * math.pi)) for x in np.linspace(170, W - 170, 80)]
    art = over(art, tube(W, H, [sq], AMBER, width=6, seed=13, glow_scale=0.8))
    preview(art, "nm-sign", bg=WALL_BG)
    save(art, f"{OUT}/sign.webp", max_w=560, quality=78)
    clear()

if "heart" in PARTS:
    W, H = 360, 330
    art = blank(W, H)
    h1 = heart_pts(180, 160, 9.0, gap=0.4)
    h2 = heart_pts(180, 168, 6.0, gap=0.6)
    art = over(art, tube(W, H, [h1], PINK, width=8, seed=21))
    art = over(art, tube(W, H, [h2], "#ff8fc6", width=5, seed=22, glow_scale=0.7, clips=False))
    preview(art, "nm-heart", bg=WALL_BG)
    save(art, f"{OUT}/heart.webp", max_w=240, quality=80)
    clear()

if "cheers" in PARTS:
    W, H = 420, 360
    art = blank(W, H)

    def glass(cx, by, tilt):
        pts = [(-46, -150), (0, -82), (46, -150), (-46, -150)]
        stem = [(0, -82), (0, -18)]
        base = [(-30, -14), (30, -14)]
        ca, sa = math.cos(tilt), math.sin(tilt)
        tr = lambda p: (cx + p[0] * ca - p[1] * sa, by + p[0] * sa + p[1] * ca)
        cup = [tr(p) for p in pts]
        liquid = [tr(p) for p in [(-34, -136), (34, -136)]]
        olive_ = [tr((-10 + 14 * math.cos(t), -120 + 14 * math.sin(t))) for t in np.linspace(0, math.tau, 26)]
        return [cup, [tr(p) for p in stem], [tr(p) for p in base]], [liquid], olive_
    l1, q1, o1 = glass(150, 320, -0.26)
    l2, q2, o2 = glass(270, 320, 0.26)
    art = over(art, tube(W, H, l1 + l2, TEAL, width=6.5, seed=31, clips=False))
    art = over(art, tube(W, H, q1 + q2, "#8ff7ee", width=4, seed=32, glow_scale=0.6, end_caps=False, clips=False))
    art = over(art, tube(W, H, [o1, o2], PINK, width=4.5, seed=33, glow_scale=0.6, clips=False))
    sparks = [[(210, 98), (210, 58)], [(176, 108), (156, 76)], [(244, 108), (264, 76)]]
    art = over(art, tube(W, H, sparks, AMBER, width=5, seed=34, glow_scale=0.7, clips=False))
    preview(art, "nm-cheers", bg=WALL_BG)
    save(art, f"{OUT}/cheers.webp", max_w=280, quality=80)
    clear()

if "rings" in PARTS:
    W, H = 380, 260
    art = blank(W, H)
    rA = [(150 + 70 * math.cos(t), 140 + 70 * math.sin(t)) for t in np.linspace(0.25, math.tau + 0.05, 90)]
    rB = [(230 + 70 * math.cos(t), 140 + 70 * math.sin(t)) for t in np.linspace(math.pi + 0.25, math.pi + math.tau + 0.05, 90)]
    art = over(art, tube(W, H, [rA], AMBER, width=7.5, seed=41, clips=False))
    art = over(art, tube(W, H, [rB], PINK, width=7.5, seed=42, clips=False))
    gem = [(150 + 70 * math.cos(-1.9) + dx, 140 + 70 * math.sin(-1.9) + dy) for dx, dy in [(-14, -6), (0, -20), (14, -6), (0, 6), (-14, -6)]]
    art = over(art, tube(W, H, [gem], TEAL, width=4.5, seed=43, glow_scale=0.6, clips=False))
    preview(art, "nm-rings", bg=WALL_BG)
    save(art, f"{OUT}/rings.webp", max_w=240, quality=80)
    clear()

if "star" in PARTS:
    W, H = 150, 150
    art = blank(W, H)
    c = 75
    st = []
    for k in range(4):
        a = k * math.pi / 2
        b = a + math.pi / 2
        st.append((c + math.cos(a) * 46, c + math.sin(a) * 46))
        st.append((c + math.cos((a + b) / 2) * 12, c + math.sin((a + b) / 2) * 12))
    st.append(st[0])
    art = over(art, tube(W, H, [st], AMBER, width=5, seed=51, glow_scale=0.55, clips=False))
    preview(art, "nm-star", bg=WALL_BG)
    save(art, f"{OUT}/star.webp", max_w=80, quality=84)
    clear()

if "wave" in PARTS:
    W, H = 520, 110
    art = blank(W, H)
    sq = [(x, 55 + 13 * math.sin((x - 70) / 32 * math.pi)) for x in np.linspace(70, W - 70, 120)]
    art = over(art, tube(W, H, [sq], PINK, width=5.5, seed=61, glow_scale=0.6, clips=False))
    dots = [[(36, 55), (40, 55)], [(W - 40, 55), (W - 36, 55)]]
    art = over(art, neon(W, H, dots, TEAL, width=9, glow_r=(4, 9, 18), glow_a=(0.8, 0.5, 0.3), seed=62, clips=False))
    preview(art, "nm-wave", bg=WALL_BG)
    save(art, f"{OUT}/wave.webp", max_w=320, quality=82)
    clear()

if "bulb" in PARTS:
    # Edison filament bulb on a black fabric cord, warm glow
    W, H = 280, 680
    art = blank(W, H)
    cx = 140
    cord = [(cx, -10), (cx, 440)]
    art = over(art, flat(strokes(W, H, [(cord, 4.0, None)]), "#0d0b0c", 1.0))
    art = over(art, flat(strokes(W, H, [([(cx - 1, -10), (cx - 1, 440)], 1.0, None)]), "#4a4450", 0.6))
    sock = shapes(W, H, [[(cx - 16, 440), (cx + 16, 440), (cx + 18, 492), (cx - 18, 492)]], smooth=False)
    art = over(art, flat(sock, "#7a5a32", 1.0))
    art = over(art, flat(sock * hatch(W, H, 1.57 + 1.4, 5, 0.25, 3, 0.5), "#3b2a16", 0.6))
    art = over(art, flat(sock * np.clip((np.arange(W)[None, :] - (cx - 8)) / 4, 0, 1) * np.clip(((cx + 2) - np.arange(W)[None, :]) / 6, 0, 1), "#e0b878", 0.5))
    globe = [(cx + 44 * math.sin(t) * (0.55 + 0.45 * math.sin(t / 2)), 560 - 64 * math.cos(t)) for t in np.linspace(0, math.tau, 60)]
    g = shapes(W, H, [[(cx - 15, 492), (cx + 15, 492)] + [(cx + 44 * math.cos(a), 556 + 50 * math.sin(a)) for a in np.linspace(-1.2, math.pi + 1.2, 40)]])
    art = over(art, glow(g, "#ffb547", radius=30, strength=0.55))
    art = over(art, flat(g, "#ffd38a", 0.22))
    fil = [[(cx - 10, 500), (cx - 12, 540), (cx - 6, 560), (cx, 545), (cx + 6, 560), (cx + 12, 540), (cx + 10, 500)]]
    art = over(art, neon(W, H, fil, "#ffb547", core="#fff4d8", width=2.6, glow_r=(3, 8, 18), glow_a=(0.9, 0.6, 0.4), seed=71, clips=False))
    rim = outline(g, 2) * 0.5
    art = over(art, flat(rim, "#ffe2b0", 0.5))
    art = over(art, flat(gaussian_filter(ellipses(W, H, [(cx - 22, 540, 6, 22, 15)]), 1.5), "#ffffff", 0.45))
    preview(art, "nm-bulb", bg=WALL_BG)
    save(art, f"{OUT}/bulb.webp", max_w=110, quality=82)
    clear()

kb_total(OUT)
