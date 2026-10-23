"""Ultah Ninja — kids' birthday: two original little ninja kids (round hoods, big eyes, headband tails) in storybook
gouache, soft foam throwing stars, bamboo, a moonlit tiled rooftop, a paper scroll. Playful, nothing sharp or violent.
Run: python3 -I ultah-ninja.py [part ...]  parts: night ninjaA ninjaB star scroll bamboo divider
Assets -> public/themes/art/ultah-ninja/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n1_lib import *

OUT = outdir("ultah-ninja")
PARTS = sys.argv[1:] or ["night", "ninjaA", "ninjaB", "star", "scroll", "bamboo", "divider"]
NAVY, NAVY_D, INDIGO = "#1d2459", "#121640", "#3a3c8a"
MOON = "#fbe6a2"
SKIN, SKIN_D = "#f6c9a4", "#e0a07c"
LINE = "#1a1838"


def capsule(x0, y0, x1, y1, r, n=10):
    a = math.atan2(y1 - y0, x1 - x0)
    pts = []
    for i in range(n + 1):
        t = a + math.pi / 2 + math.pi * i / n
        pts.append((x0 + math.cos(t) * r, y0 + math.sin(t) * r))
    for i in range(n + 1):
        t = a - math.pi / 2 + math.pi * i / n
        pts.append((x1 + math.cos(t) * r, y1 + math.sin(t) * r))
    return pts


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for (cx, cy, a0) in [(x1 - r, y0 + r, -math.pi / 2), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, math.pi / 2), (x0 + r, y0 + r, math.pi)]:
        for i in range(n + 1):
            a = a0 + math.pi / 2 * i / n
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def paint_part(art, W, H, m, col, col2, nx, shade_dir=(1, 1), shade=0.32, hi=0.22, line=True):
    """Storybook gouache part: opaque body, soft core shadow on one side, a lighter rim on the other, a soft ink line."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=0.6)
    dx, dy = shade_dir
    g = gaussian_filter(m, 6)
    sh = np.clip(m - np.roll(np.roll(g, -int(10 * dy), 0), -int(10 * dx), 1) * 1.1, 0, 1) * m
    art = G(art, sh, mix(col2, LINE, 0.35), seed=nx(), density=shade, edge=0.2, bloom=0.2, rough=2)
    lt = np.clip(m - np.roll(np.roll(g, int(10 * dy), 0), int(10 * dx), 1) * 1.1, 0, 1) * m
    art = OV(art, lt, lambda q: flat(q, mix(col, "#ffffff", 0.5), hi))
    if line:
        art = G(art, edge_ring(m, 1.4), LINE, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.8, feather=0.5)
    return art


def foam_star_mask(W, H, cx, cy, r, rot=0.0):
    """Soft rounded 4-point foam star (puffy, blunt tips) with a round centre hole."""
    pts = []
    for i in range(64):
        a = rot + i / 64 * math.tau
        k = 0.55 + 0.45 * abs(math.cos(2 * (a - rot))) ** 2.2
        pts.append((cx + math.cos(a) * r * k, cy + math.sin(a) * r * k))
    m = shape_mask(W, H, pts)
    hole = circles(W, H, [(cx, cy, r * 0.16)])
    return np.clip(m - hole, 0, 1), m


def paint_star(art, W, H, cx, cy, r, rot, col, col2, nx):
    m, full = foam_star_mask(W, H, cx, cy, r, rot)
    art = paint_part(art, W, H, m, col, col2, nx, shade=0.35, hi=0.3)
    # foam pores
    rng = random.Random(int(cx * 7 + cy))
    pores = circles(W, H, [(cx + rng.gauss(0, r * 0.4), cy + rng.gauss(0, r * 0.4), rng.uniform(0.8, 1.6)) for _ in range(int(r * 1.2))]) * erode(m, 1)
    art = G(art, pores, col2, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
    # stitched seam ring
    seam = strokes(W, H, [([(cx + math.cos(a) * r * 0.34, cy + math.sin(a) * r * 0.34) for a in np.linspace(0, math.tau, 40)], 1.2, None)]) * (np.sin(np.arctan2(np.arange(H)[:, None] - cy, np.arange(W)[None, :] - cx) * 18) > 0)
    art = G(art, seam, mix(col2, LINE, 0.3), seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    return art


def ninja(W, H, cx, by, s, nx, rng, suit, suit2, band, band2, belt, pose="jump", star=("#ffd23f", "#f2a81d")):
    """Original chibi ninja kid. pose: 'jump' (arm up with a foam star) or 'sit' (sitting, waving)."""
    art = blank(W, H)
    hy = by - 150 * s if pose == "jump" else by - 118 * s   # head centre
    hr = 58 * s
    # ---- legs
    if pose == "jump":
        legs = [capsule(cx - 16 * s, hy + 92 * s, cx - 36 * s, hy + 124 * s, 13 * s), capsule(cx + 16 * s, hy + 92 * s, cx + 30 * s, hy + 132 * s, 13 * s)]
        feet = [ellipse_pts(cx - 40 * s, hy + 128 * s, 15 * s, 9 * s, 12, -0.5), ellipse_pts(cx + 34 * s, hy + 138 * s, 15 * s, 9 * s, 12, 0.3)]
    else:
        legs = [capsule(cx - 18 * s, hy + 96 * s, cx - 26 * s, hy + 112 * s, 14 * s), capsule(cx + 18 * s, hy + 96 * s, cx + 28 * s, hy + 112 * s, 14 * s)]
        feet = [ellipse_pts(cx - 30 * s, hy + 116 * s, 15 * s, 9 * s, 12, 0.0), ellipse_pts(cx + 32 * s, hy + 116 * s, 15 * s, 9 * s, 12, 0.0)]
    lm = shapes(W, H, legs)
    art = paint_part(art, W, H, lm, suit, suit2, nx)
    fm = shapes(W, H, feet)
    art = paint_part(art, W, H, fm, "#3a3550", "#24203a", nx, hi=0.15)
    # ---- body
    body = shapes(W, H, [rrect(cx - 30 * s, hy + 44 * s, cx + 30 * s, hy + 104 * s, 22 * s)])
    art = paint_part(art, W, H, body, suit, suit2, nx)
    # wrap collar (V)
    col = strokes(W, H, [([(cx - 18 * s, hy + 50 * s), (cx, hy + 72 * s), (cx + 18 * s, hy + 50 * s)], 5 * s, None)]) * body
    art = G(art, col, mix(suit2, LINE, 0.3), seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    # belt (obi) with a bow
    bm = shapes(W, H, [rrect(cx - 31 * s, hy + 78 * s, cx + 31 * s, hy + 90 * s, 4 * s)]) * dilate(body, 1)
    art = paint_part(art, W, H, bm, belt, mix(belt, LINE, 0.25), nx, hi=0.3)
    bow = shapes(W, H, [ellipse_pts(cx + 14 * s, hy + 84 * s, 8 * s, 5 * s, 10, 0.5), ellipse_pts(cx + 24 * s, hy + 84 * s, 7 * s, 4.5 * s, 10, -0.5)])
    art = paint_part(art, W, H, bow, belt, mix(belt, LINE, 0.25), nx, hi=0.3)
    # ---- arms
    if pose == "jump":
        arms = [capsule(cx - 26 * s, hy + 56 * s, cx - 58 * s, hy + 74 * s, 11 * s), capsule(cx + 26 * s, hy + 54 * s, cx + 52 * s, hy + 6 * s, 11 * s)]
        hands = [(cx - 62 * s, hy + 76 * s), (cx + 54 * s, hy + 0 * s)]
    else:
        arms = [capsule(cx - 26 * s, hy + 58 * s, cx - 30 * s, hy + 90 * s, 11 * s), capsule(cx + 26 * s, hy + 54 * s, cx + 58 * s, hy + 18 * s, 11 * s)]
        hands = [(cx - 30 * s, hy + 94 * s), (cx + 62 * s, hy + 12 * s)]
    am = shapes(W, H, arms)
    art = paint_part(art, W, H, am, suit, suit2, nx)
    hm = circles(W, H, [(x, y, 10 * s) for x, y in hands])
    art = paint_part(art, W, H, hm, SKIN, SKIN_D, nx, hi=0.25)
    # ---- head: hood, face band, eyes
    head = shapes(W, H, [deform(ellipse_pts(cx, hy, hr, hr * 0.94, 24), rng, 1, 0.01)])
    art = paint_part(art, W, H, head, suit, suit2, nx, shade=0.3)
    face = shapes(W, H, [rrect(cx - hr * 0.74, hy - hr * 0.2, cx + hr * 0.74, hy + hr * 0.34, hr * 0.26)]) * head
    art = paint_part(art, W, H, face, SKIN, SKIN_D, nx, shade=0.18, hi=0.3)
    # eyes: big shiny ovals looking slightly up/right
    ex = [cx - hr * 0.32, cx + hr * 0.32]
    eyes = ellipses(W, H, [(x, hy + hr * 0.07, hr * 0.15, hr * 0.19, 0) for x in ex])
    art = GP(art, eyes, "#1d1a33", "#2c2850", seed=nx(), rough=0.6)
    shine = circles(W, H, [(x + hr * 0.05, hy - hr * 0.02, hr * 0.06) for x in ex] + [(x - hr * 0.05, hy + hr * 0.15, hr * 0.025) for x in ex])
    art = OV(art, shine, lambda q: flat(q, "#ffffff", 0.95))
    cheeks = ellipses(W, H, [(x, hy + hr * 0.27, hr * 0.12, hr * 0.06, 0) for x in (cx - hr * 0.56, cx + hr * 0.56)]) * face
    art = G(art, cheeks, "#f08a8a", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1)
    brows = strokes(W, H, [([(x - hr * 0.12, hy - hr * 0.12), (x + hr * 0.12, hy - hr * 0.14)], 3 * s, (0.2, 0.2)) for x in ex])
    art = G(art, brows, "#5a3a2a", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    # headband across the forehead + knot and two fluttering tails at the back
    hb = shapes(W, H, [[(cx - hr * 1.02, hy - hr * 0.38), (cx + hr * 1.02, hy - hr * 0.42), (cx + hr * 1.0, hy - hr * 0.24), (cx - hr * 1.0, hy - hr * 0.2)]]) * dilate(head, 1.5)
    art = paint_part(art, W, H, hb, band, band2, nx, hi=0.35)
    plate = shapes(W, H, [rrect(cx - hr * 0.22, hy - hr * 0.42, cx + hr * 0.22, hy - hr * 0.2, hr * 0.06)])
    art = paint_part(art, W, H, plate, "#d9dde8", "#a9afc2", nx, hi=0.5)
    art = G(art, circles(W, H, [(cx, hy - hr * 0.31, hr * 0.05)]), band2, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.4)
    kx, ky = cx - hr * 0.98, hy - hr * 0.3
    tails = [blade(W, H, curve([(kx, ky), (kx - hr * 0.5, ky - hr * 0.15), (kx - hr * 0.95, ky - hr * 0.45)], 20), hr * 0.12),
             blade(W, H, curve([(kx, ky), (kx - hr * 0.55, ky + hr * 0.1), (kx - hr * 1.0, ky + hr * 0.02)], 20), hr * 0.11)]
    tm = shapes(W, H, tails)
    art = knockout(art, tm, 0, 1)
    tl = paint_part(blank(W, H), W, H, tm, band, band2, nx, hi=0.3)
    art = over(tl, art)
    knot = circles(W, H, [(kx, ky, hr * 0.12)])
    art = paint_part(art, W, H, knot, band, band2, nx, hi=0.3)
    # ---- foam star in the raised hand (jump) / waving hand lines (sit)
    if pose == "jump":
        art = paint_star(art, W, H, hands[1][0] + 10 * s, hands[1][1] - 26 * s, 26 * s, 0.4, star[0], star[1], nx)
    else:
        wv = strokes(W, H, [(arc_pts(hands[1][0], hands[1][1], r * s, -2.4, -1.2, 10), 3 * s, (0.2, 0.2)) for r in (24, 34)])
        art = G(art, wv, "#ffffff", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.5)
    return art


def ninjaA():
    W, H = 340, 380
    rng = random.Random(3); nx = Seq(100)
    art = ninja(W, H, W * 0.52, H - 14, 1.25, nx, rng, "#e8553e", "#b8392a", "#2cc1b5", "#1b8f87", "#ffd23f", pose="jump", star=("#ffd23f", "#f0a51c"))
    preview(art, "un-ninjaA", bg=NAVY)
    save(art, f"{OUT}/ninjaA.webp", max_w=260, quality=84)


def ninjaB():
    W, H = 360, 330
    rng = random.Random(5); nx = Seq(300)
    art = ninja(W, H, W * 0.46, H - 14, 1.25, nx, rng, "#3b6fd8", "#294fa4", "#ffcf3a", "#e0a21a", "#ff7aa8", pose="sit")
    preview(art, "un-ninjaB", bg=NAVY)
    save(art, f"{OUT}/ninjaB.webp", max_w=260, quality=84)


def star():
    W = H = 200
    nx = Seq(500)
    art = paint_star(blank(W, H), W, H, W / 2, H / 2, 86, 0.3, "#ffd23f", "#eea21c", nx)
    preview(art, "un-star", bg=NAVY)
    save(art, f"{OUT}/star.webp", max_w=110, quality=84)


def night():
    """Moonlit sky over a tiled rooftop: big moon with soft craters, wispy clouds, stars, bamboo silhouettes, two warm
    paper lanterns, the curved roof ridge in the foreground where the ninjas stand."""
    W, H = 760, 980
    rng = random.Random(9); nx = Seq(700)
    art = painted_sky(W, H, [(0, "#141947"), (0.35, "#232a6e"), (0.62, "#3b3f8f"), (0.78, "#5a4f9e"), (1, "#2a2560")], seed=4, streak=1.0)
    # stars
    st = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(0.8, 2.2)) for _ in range(160)])
    art = OV(art, st, lambda q: flat(q, "#fff6d8", 0.9))
    # moon
    mx, my, mr = W * 0.66, H * 0.3, 150
    moon = circles(W, H, [(mx, my, mr)])
    art = over(art, glow(moon, "#fbe6a2", 60, 0.45))
    art = GP(art, moon, MOON, "#f4d27e", seed=nx(), rough=1.5, streak=0.4)
    for (dx, dy, r) in [(-50, -40, 28), (40, 30, 36), (-20, 60, 18), (60, -60, 16), (-70, 30, 12)]:
        art = G(art, circles(W, H, [(mx + dx, my + dy, r)]), "#e8c878", seed=nx(), density=0.4, edge=0.6, bloom=0.3, rough=2)
    # clouds drifting across the moon
    for (cx, cy, rx) in [(W * 0.55, H * 0.36, 160), (W * 0.2, H * 0.2, 120), (W * 0.86, H * 0.44, 110)]:
        cl = shapes(W, H, [deform(ellipse_pts(cx + k * rx * 0.5, cy - (k % 2) * 14, rx * 0.4, rx * 0.16, 14), rng, 2, 0.12) for k in range(-1, 2)])
        art = GP(art, cl, "#6a6cb8", "#5658a2", seed=nx(), rough=3, streak=0.8)
        art = OV(art, cl * np.clip(-(np.arange(H)[:, None] - cy) / 30 + 0.6, 0, 1), lambda q: flat(q, "#a8a6e0", 0.5))
    # distant mountains
    art = G(art, hills(W, H, H * 0.66, 50, 3, 0.4), "#3a3a7e", "#33356f", seed=nx(), density=0.9, edge=0.3, bloom=0.2, rough=4)
    # bamboo silhouettes on both sides
    for side in (0, 1):
        for k in range(5):
            x = (W * 0.04 + k * 34) if side == 0 else (W * 0.96 - k * 34)
            x += rng.uniform(-8, 8)
            stalk = strokes(W, H, [([(x, H), (x + rng.uniform(-14, 14), -30)], rng.uniform(12, 18), None)])
            nodes = strokes(W, H, [([(x - 12, y), (x + 12, y)], 2.4, None) for y in np.arange(H * 0.15, H, rng.uniform(70, 90))]) * dilate(stalk, 1)
            tone = mix("#163a46", "#0f2a36", k / 4)
            art = GP(art, stalk, tone, mix(tone, "#000000", 0.2), seed=nx(), rough=1)
            art = G(art, nodes, "#08161e", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
            lv = []
            for y in np.arange(H * 0.04, H * 0.7, 110):
                for j in range(3):
                    a = (math.pi * 0.15 if side == 0 else math.pi * 0.85) + rng.uniform(-0.6, 0.6)
                    lv.append(blade(W, H, curve([(x, y), (x + math.cos(a) * 40, y + math.sin(a) * 40 + 10), (x + math.cos(a) * 80, y + math.sin(a) * 80 + 30)], 12), 9))
            art = GP(art, shapes(W, H, lv), tone, mix(tone, "#2a6a5a", 0.3), seed=nx(), rough=1.2)
            clear()
    # warm paper lanterns hanging from a string
    for (lx, ly) in [(W * 0.22, H * 0.52), (W * 0.36, H * 0.56)]:
        art = G(art, strokes(W, H, [([(lx, ly - 70), (lx, ly - 30)], 1.6, None)]), "#0d1030", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)
        lm = shapes(W, H, [ellipse_pts(lx, ly, 26, 32, 20)])
        art = over(art, glow(lm, "#ffb04a", 30, 0.7))
        art = paint_part(art, W, H, lm, "#ff8a3d", "#e0552a", nx, hi=0.45, line=False)
        ribs = strokes(W, H, [([(lx - 26 * math.cos(t), ly + 32 * math.sin(t)), (lx + 26 * math.cos(t), ly + 32 * math.sin(t))], 1.2, None) for t in np.linspace(-1.1, 1.1, 6)]) * lm
        art = G(art, ribs, "#b8401e", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
        caps = shapes(W, H, [rect(lx - 12, ly - 36, lx + 12, ly - 28), rect(lx - 12, ly + 28, lx + 12, ly + 36)], smooth=False)
        art = GP(art, caps, "#2a1a1a", seed=nx(), rough=0.4)
    # rooftop: curved ridge and tiled slope at the bottom
    ry = H * 0.8
    roof = [(-20, H)] + [(x, ry + 60 * ((x - W / 2) / (W / 2)) ** 2 * -0.0 + 26 * ((x - W / 2) / (W / 2)) ** 2) for x in np.linspace(-20, W + 20, 40)] + [(W + 20, H)]
    rm = shapes(W, H, [roof], smooth=False)
    art = GP(art, rm, "#2b2f5c", "#1e2148", seed=nx(), rough=1.4, streak=1.0)
    tiles = strokes(W, H, [([(x + 0.0, ry + 26 * ((x - W / 2) / (W / 2)) ** 2 + 8), (x + (x - W / 2) * 0.25, H)], 5, None) for x in np.arange(0, W + 1, 26)]) * rm
    art = G(art, tiles, "#14173a", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6)
    rows = strokes(W, H, [([(x, ry + 26 * ((x - W / 2) / (W / 2)) ** 2 + dy) for x in np.linspace(-20, W + 20, 40)], 2, None) for dy in (36, 70, 110, 150)]) * rm
    art = G(art, rows, "#14173a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    ridge = strokes(W, H, [([(x, ry + 26 * ((x - W / 2) / (W / 2)) ** 2) for x in np.linspace(-20, W + 20, 40)], 16, None)])
    art = GP(art, ridge, "#3c427a", "#2b2f5c", seed=nx(), rough=1)
    art = OV(art, strokes(W, H, [([(x, ry + 26 * ((x - W / 2) / (W / 2)) ** 2 - 6) for x in np.linspace(-20, W + 20, 40)], 4, None)]), lambda q: flat(q, "#9fa6e8", 0.5))
    # moonlight rim on the roof
    art = add_grain(art, 5, 0.03)
    preview(art, "un-night")
    save_rgb(art, f"{OUT}/night.webp", size=(720, int(720 * H / W)), quality=74)


def scroll():
    """Unrolled paper scroll (makimono) with wooden rods and a red cord, horizontal; text goes on top in CSS."""
    W, H = 640, 300
    nx = Seq(900); rng = random.Random(2)
    art = blank(W, H)
    paper_m = shapes(W, H, [[(56, 40), (W - 56, 34), (W - 56, H - 36), (56, H - 40)]], smooth=False)
    art = GP(art, paper_m, "#fbf1d8", "#f2e2bc", seed=nx(), rough=1.4, streak=0.25)
    art = G(art, paper_m * fbm(W, H, 4, 30, 3), "#e8d2a0", seed=nx(), density=0.35, edge=0.1, bloom=0.4, rough=3)
    art = G(art, edge_ring(paper_m, 3), "#c9a868", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    # red border bands top/bottom of the paper
    bands = shapes(W, H, [rect(56, 48, W - 56, 58), rect(56, H - 58, W - 56, H - 48)], smooth=False)
    art = paint_part(art, W, H, bands, "#e0503a", "#b83a2a", nx, hi=0.2, line=False)
    for x0 in (30, W - 30):
        rod = shapes(W, H, [rrect(x0 - 22, 14, x0 + 22, H - 14, 18)])
        art = paint_part(art, W, H, rod, "#c07a3e", "#8a4f24", nx, shade_dir=(1, 0), hi=0.35)
        caps = shapes(W, H, [rrect(x0 - 26, 4, x0 + 26, 26, 10), rrect(x0 - 26, H - 26, x0 + 26, H - 4, 10)])
        art = paint_part(art, W, H, caps, "#3a2a4a", "#22182e", nx, hi=0.3)
    cord = strokes(W, H, [(curve([(W - 50, H * 0.5), (W - 10, H * 0.62), (W - 26, H * 0.86), (W - 6, H - 2)], 30), 6, (0.0, 0.2))])
    art = paint_part(art, W, H, cord, "#e0503a", "#b83a2a", nx, hi=0.3)
    preview(art, "un-scroll", bg=NAVY)
    save(art, f"{OUT}/scroll.webp", max_w=480, quality=82)


def bamboo():
    """A bright green bamboo pair with leaves (for section sides), vertical."""
    W, H = 220, 760
    rng = random.Random(4); nx = Seq(1100)
    art = blank(W, H)
    for (x, wd, top) in [(W * 0.36, 26, 0), (W * 0.66, 20, 90)]:
        stalk = shapes(W, H, [rrect(x - wd / 2, top, x + wd / 2, H + 10, wd * 0.3)])
        art = paint_part(art, W, H, stalk, "#7cc46a", "#4f9a48", nx, shade_dir=(1, 0), hi=0.35)
        for y in np.arange(top + 70, H, 110):
            nd = shapes(W, H, [rrect(x - wd / 2 - 2, y - 4, x + wd / 2 + 2, y + 4, 3)])
            art = paint_part(art, W, H, nd, "#5fa652", "#3f7f3a", nx, hi=0.4)
        for y in np.arange(top + 60, H * 0.8, 160):
            for d in (-1, 1):
                for j in range(2):
                    a = (-0.4 if d > 0 else math.pi + 0.4) + rng.uniform(-0.3, 0.4) + j * 0.35 * d
                    lv = blade(W, H, curve([(x, y), (x + math.cos(a) * 34, y + math.sin(a) * 34 + 6), (x + math.cos(a) * 70, y + math.sin(a) * 70 + 22)], 14), 10)
                    art = paint_part(art, W, H, shapes(W, H, [lv]), "#8fd174", "#5aa64c", nx, hi=0.3)
        clear()
    preview(art, "un-bamboo", bg=NAVY)
    save(art, f"{OUT}/bamboo.webp", max_w=140, quality=82)


def divider():
    """A short bamboo stick with two leaves and a tiny foam star (heading divider)."""
    W, H = 440, 90
    nx = Seq(1300); rng = random.Random(6)
    art = blank(W, H)
    stalk = shapes(W, H, [rrect(30, 40, W - 90, 54, 6)])
    art = paint_part(art, W, H, stalk, "#7cc46a", "#4f9a48", nx, shade_dir=(0, 1), hi=0.35)
    nodes = shapes(W, H, [rrect(x - 3, 37, x + 3, 57, 2) for x in (110, 210, 300)])
    art = paint_part(art, W, H, nodes, "#5fa652", "#3f7f3a", nx, hi=0.4)
    for (x, a) in [(110, -0.7), (110, -1.2), (300, -2.2), (300, -2.6)]:
        lv = blade(W, H, curve([(x, 44), (x + math.cos(a) * 24, 44 + math.sin(a) * 24), (x + math.cos(a) * 48, 44 + math.sin(a) * 40)], 12), 7)
        art = paint_part(art, W, H, shapes(W, H, [lv]), "#8fd174", "#5aa64c", nx, hi=0.3)
    art = paint_star(art, W, H, W - 50, 46, 30, 0.2, "#ff7aa8", "#e0508a", nx)
    preview(art, "un-divider", bg="#fff8e8")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
