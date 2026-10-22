"""Hadramaut Tanah — a walled town of Hadrami mud-brick tower houses at dusk (original design, inspired by the
vernacular of Wadi Hadramaut): tall tapering adobe towers with straw-flecked mud plaster and rain runs, whitewashed
lime crowns with stepped parapets, lime-framed small windows with carved teak shutters (a few lit), date palms at
the foot of the wall, a blue-hour sky fading to warm sand. No figures.
Run: python3 -I hadramaut-tanah.py [part ...]  parts: sky town window door trim adobe
Assets -> public/themes/art/hadramaut-tanah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c3_lib import *

OUT = outdir("hadramaut-tanah")
PARTS = sys.argv[1:] or ["sky", "town", "window", "door", "trim", "adobe"]
MUD, MUD_D, MUD_L = "#b27a4a", "#7e4f2c", "#d4a271"
LIME, LIME_S = "#f4ede0", "#d6c8bb"
TEAK, TEAK_D = "#5a3620", "#2f1c10"
LIT = "#ffd58a"
SKY = [(0.0, "#22365a"), (0.32, "#556a8e"), (0.6, "#b99099"), (0.8, "#e8b98a"), (1.0, "#f5dcae")]


def tower(art, W, H, x, base, w, h, nx, rng, depth=1.0, side=0.22, lit_p=0.18, crown=2):
    """One tower house: lit front face + shadowed side face, lime crown with stepped parapet, window grid."""
    taper = w * 0.1
    sw = w * side
    fx0, fx1 = x, x + w
    front = [(fx0, base), (fx0 + taper, base - h), (fx1 - taper, base - h), (fx1, base)]
    sidep = [(fx1, base), (fx1 - taper, base - h), (fx1 - taper + sw, base - h + sw * 0.2), (fx1 + sw, base)]
    fm = poly(W, H, front); sm = poly(W, H, sidep)
    mud = mix(MUD, "#c9a588", 1 - depth) if depth < 1 else MUD
    fm = displace(fm, nx(), 2.5, 30); sm = displace(sm, nx(), 2.0, 30)
    art = OV(art, fm, lambda m: plaster(m, mix(MUD_L, mud, 0.35), mud, nx(), 0.9))
    tex = fbm(W, H, nx(), 9, 3)
    art = over(art, flat(fm * np.clip((tex - 0.55) * 3, 0, 1), MUD_D, 0.22))
    art = over(art, flat(fm * np.clip((0.4 - tex) * 3, 0, 1), "#e6bb8a", 0.18))
    art = OV(art, sm, lambda m: plaster(m, mix(MUD_D, "#5d4a5e", 0.3), MUD_D, nx(), 0.4))
    # rain runs: vertical darker streaks from the parapet and the window sills
    st = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (14, 0.9))
    st = np.clip((st - 0.5) * 9, 0, 1)
    art = over(art, flat(fm * st, MUD_D, 0.25 * depth))
    # floors / windows
    floor_h = max(22.0, w * 0.27)
    crown_h = floor_h * crown * 0.6
    cy0 = base - h
    nfl = int((h - crown_h) / floor_h)
    cols = max(2, int((w - 2 * taper) / 26))
    lime_items, shut_items, lit_items, dark_items, sill_items = [], [], [], [], []
    for f in range(nfl):
        yb = base - floor_h * (f + 0.35) + rng.uniform(-2, 2)
        if yb - floor_h * 0.5 < cy0 + crown_h:
            break
        if f < 2 and rng.random() < 0.75:
            continue
        nwin = rng.choice([1, 1, 2, 2, 3]) if f > 1 else 1
        slots = sorted(rng.sample(range(cols), min(cols, nwin)))
        for c in slots:
            xc = fx0 + taper + (c + 0.5) * (w - 2 * taper) / cols + rng.uniform(-3, 3)
            big = rng.random() < 0.25
            ww, wh = (w * 0.055 + 2) * (1.3 if big else 1), floor_h * (0.5 if big else 0.36)
            lime_items.append([(xc - ww - 3, yb - wh - 3), (xc + ww + 3, yb - wh - 3), (xc + ww + 3, yb + 3), (xc - ww - 3, yb + 3)])
            win = [(xc - ww, yb - wh), (xc + ww, yb - wh), (xc + ww, yb), (xc - ww, yb)]
            r_ = rng.random()
            (lit_items if r_ < lit_p else shut_items if r_ < 0.75 else dark_items).append(win)
            if big:
                sill_items.append([(xc - ww - 5, yb + 2), (xc + ww + 5, yb + 2), (xc + ww + 5, yb + 6), (xc - ww - 5, yb + 6)])
    # whitewashed crown and lime band under it
    cm = poly(W, H, [(fx0 + taper * (crown_h / h), cy0 + crown_h), (fx0 + taper, cy0), (fx1 - taper, cy0), (fx1 - taper * (crown_h / h), cy0 + crown_h)])
    mer = []
    nm = max(3, int(w / 16))
    for k in range(nm):
        mx0 = fx0 + taper + k * (w - 2 * taper) / nm + 2
        mx1 = mx0 + (w - 2 * taper) / nm - 4
        mh = floor_h * 0.32
        mer.append([(mx0, cy0 + 1), (mx0, cy0 - mh * 0.55), ((mx0 + mx1) / 2, cy0 - mh), (mx1, cy0 - mh * 0.55), (mx1, cy0 + 1)])
    crownm = np.maximum(cm, shapes(W, H, mer, smooth=False))
    # dripping lime edge below the crown
    drip = []
    for k in range(int(w / 7)):
        dx = fx0 + taper + rng.uniform(0, w - 2 * taper)
        dl = rng.uniform(3, 12)
        drip.append([(dx - 2, cy0 + crown_h - 1), (dx + 2, cy0 + crown_h - 1), (dx + 0.5, cy0 + crown_h + dl), (dx - 0.5, cy0 + crown_h + dl)])
    crownm = np.maximum(crownm, shapes(W, H, drip))
    art = GP(art, crownm, LIME, mix(LIME, "#e6d9c4", 0.6), seed=nx(), rough=0.9, streak=0.6, density=0.98 * depth + 0.02)
    sidecrown = poly(W, H, [(fx1 - taper * (crown_h / h), cy0 + crown_h), (fx1 - taper, cy0), (fx1 - taper + sw, cy0 + sw * 0.2), (fx1 + sw * (1 - crown_h / h), cy0 + crown_h + sw * 0.1)])
    art = GP(art, sidecrown, LIME_S, "#bfb0a6", seed=nx(), rough=0.8, streak=0.5)
    # crown windows (small dark slits)
    slits = []
    for c in range(cols):
        xc = fx0 + taper + (c + 0.5) * (w - 2 * taper) / cols
        slits.append([(xc - 2.5, cy0 + crown_h * 0.35), (xc + 2.5, cy0 + crown_h * 0.35), (xc + 2.5, cy0 + crown_h * 0.7), (xc - 2.5, cy0 + crown_h * 0.7)])
    art = GP(art, shapes(W, H, slits, smooth=False), "#3a2a2a", seed=nx(), rough=0.4, pad=6)
    if lime_items:
        art = GP(art, shapes(W, H, lime_items + sill_items, smooth=False), LIME, "#e9dfcf", seed=nx(), rough=0.7, streak=0.4, pad=6)
    if shut_items:
        sm_ = shapes(W, H, shut_items, smooth=False)
        art = OV(art, sm_, lambda m: wood(m, TEAK, TEAK_D, seed=nx(), angle=1.5708, grain=3.0), pad=6)
        lat = sm_ * hatch(W, H, 0.0, 4.0, 0.25, nx(), 0.2) * hatch(W, H, 1.5708, 4.0, 0.6, nx() , 0.2)
        art = over(art, flat(lat, "#1e120a", 0.5))
    if dark_items:
        art = GP(art, shapes(W, H, dark_items, smooth=False), "#2a1d1c", "#3b2a2a", seed=nx(), rough=0.5, pad=6)
    if lit_items:
        lm = shapes(W, H, lit_items, smooth=False)
        art = over(art, glow(lm, "#ffb347", radius=5, strength=0.35))
        art = GP(art, lm, LIT, "#ffbf5e", seed=nx(), rough=0.5, pad=6)
        lat = lm * hatch(W, H, 0.0, 4.0, 0.2, nx(), 0.2)
        art = over(art, flat(lat, TEAK, 0.55))
    # dusk light: warm on the left of the front face, haze for depth
    art = over(art, flat(fm * light_mask(H, W, fx0 - w * 0.2, base - h * 0.7, h * 0.9), "#ffb27a", 0.16))
    if depth < 1:
        art = over(art, flat(np.maximum(fm, np.maximum(sm, crownm)), "#c9a9a8", (1 - depth) * 0.55))
    return art


def date_palm(art, W, H, x, by, h, lean, nx, seed):
    m = palm_m(W, H, x, by, h, lean, seed)
    art = G(art, m, "#6f8a4a", "#3b5636", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=1.5, feather=0.7)
    art = over(art, flat(m * light_mask(H, W, x - h * 0.3, by - h, h * 0.6), "#c9c27a", 0.35))
    return art


if "sky" in PARTS:
    W, H = 600, 900
    sky = wet_sky(W, H, SKY, seed=21, blooms=0.6)
    # a few soft cloud wisps catching the last light
    for (cy, x0, x1, col) in [(470, -40, 360, "#e8a98e"), (540, 240, 660, "#f0c09a"), (400, 300, 640, "#cf9aa0")]:
        m = strokes(W, H, [(curve([(x0, cy), ((x0 + x1) / 2, cy - 14), (x1, cy + 6)], 30), 16, (0.3, 0.4))])
        sky = G(sky, m, col, seed=cy, density=0.35, edge=0.25, bloom=0.4, rough=8, feather=4)
    save_rgb(sky, f"{OUT}/sky.webp", quality=74)
    clear()

if "town" in PARTS:
    W, H = 780, 760
    nx = Seq(5300); rng = random.Random(8)
    art = blank(W, H)
    G0 = 650
    # back row (hazy)
    for (x, w, h) in [(40, 94, 460), (170, 90, 560), (350, 104, 640), (470, 96, 600), (590, 100, 520)]:
        art = tower(art, W, H, x, G0 - 40, w, h, nx, rng, depth=0.55, lit_p=0.08)
        clear()
    # front row
    for (x, w, h, cr) in [(-20, 122, 360, 2), (96, 112, 470, 2), (230, 150, 610, 3), (396, 118, 520, 2), (500, 134, 420, 2), (640, 118, 500, 2), (730, 90, 300, 1)]:
        art = tower(art, W, H, x, G0, w, h, nx, rng, depth=1.0, lit_p=0.22, crown=cr)
        clear()
    # palms in front of the wall
    for (x, h, lean, sd) in [(60, 210, 0.08, 1), (118, 170, -0.1, 2), (640, 230, -0.06, 3), (720, 180, 0.1, 4), (380, 140, 0.05, 5)]:
        art = date_palm(art, W, H, x, G0 + 30, h, lean, nx, sd)
    # town wall with a lime coping and a small gate
    wall = poly(W, H, [(-10, G0 - 22), (W + 10, G0 - 28), (W + 10, H), (-10, H)])
    art = OV(art, wall, lambda m: plaster(m, MUD_L, MUD, nx(), 0.7))
    coping = strokes(W, H, [([(-10, G0 - 22), (W + 10, G0 - 28)], 8, None)])
    art = GP(art, coping, LIME, "#e6d9c4", seed=nx(), rough=1.0)
    gate = shapes(W, H, [[(350, H), (350, G0 + 30)] + [(390 + math.cos(a) * 40, G0 + 30 + math.sin(a) * 44) for a in np.linspace(math.pi, math.tau, 20)] + [(430, H)]], smooth=False)
    art = GP(art, np.clip(gaussian_filter(gate, 3) * 1.6 - gate, 0, 1), LIME, seed=nx(), rough=0.8)
    art = OV(art, gate, lambda m: wood(m, TEAK, TEAK_D, seed=nx(), angle=1.5708, grain=5.0))
    # warm wall shading toward the bottom (blends into the page plaster)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = over(art, flat(wall * np.clip((yy - 0.9) / 0.1, 0, 1), "#ecdcc2", 1.0))
    preview(art, "town", bg="#556a8e")
    save(art, f"{OUT}/town.webp", max_w=780, quality=80)
    clear()

if "window" in PARTS:
    # carved teak window in a lime frame: two shutters with geometric lattice, a lime arch above (portrait ornament)
    W, H = 300, 380
    nx = Seq(900); rng = random.Random(3)
    art = blank(W, H)
    wall = shapes(W, H, [ellipse_pts(150, 200, 140, 175, 40)])
    wall = displace(wall, 4, 10, 40)
    art = OV(art, wall, lambda m: plaster(m, MUD_L, MUD, nx(), 0.8))
    frame = rect(W, H, 70, 110, 230, 330)
    arch = shapes(W, H, [[(70, 110)] + [(150 + math.cos(a) * 80, 110 + math.sin(a) * 60) for a in np.linspace(math.pi, math.tau, 30)] + [(230, 110)]], smooth=False)
    art = GP(art, np.maximum(frame, arch), LIME, "#e9dfcf", seed=nx(), rough=1.0)
    for sx0 in (86, 152):
        sh = rect(W, H, sx0, 124, sx0 + 62, 316)
        art = OV(art, sh, lambda m: wood(m, TEAK, TEAK_D, seed=nx(), angle=1.5708, grain=4.0))
        # carved lattice: diamond grid + a small 8-point star medallion
        lat = sh * np.maximum(hatch(W, H, 0.785, 9.0, 0.22, nx(), 0.3), hatch(W, H, -0.785, 9.0, 0.22, nx(), 0.3))
        art = over(art, flat(lat * rect(W, H, sx0 + 6, 140, sx0 + 56, 300), "#1e120a", 0.7))
        st = shapes(W, H, [star_pts(sx0 + 31, 220, 15, 8, 0.6)], smooth=False)
        art = over(art, flat(st, "#2a180c", 0.9))
        art = over(art, flat(outline(sh, 2.5), "#2a180c", 0.6))
    fan = arch * (1 - rect(W, H, 0, 0, W, 110))
    fan_in = shapes(W, H, [[(84, 112)] + [(150 + math.cos(a) * 66, 112 + math.sin(a) * 48) for a in np.linspace(math.pi, math.tau, 30)] + [(216, 112)]], smooth=False)
    art = OV(art, fan_in, lambda m: wood(m, TEAK, TEAK_D, seed=nx(), angle=0.0, grain=4.0))
    rays = strokes(W, H, [([(150, 112), (150 + math.cos(a) * 64, 112 + math.sin(a) * 46)], 2.2, None) for a in np.linspace(math.pi + 0.2, math.tau - 0.2, 7)])
    art = over(art, flat(rays * fan_in, "#1e120a", 0.7))
    sill = rect(W, H, 60, 328, 240, 342)
    art = GP(art, sill, LIME, "#ddd2c0", seed=nx(), rough=0.8)
    preview(art, "window")
    save(art, f"{OUT}/window.webp", max_w=220, quality=82)
    clear()

if "door" in PARTS:
    # carved Hadrami-style double door (geometric + floral rosettes, iron studs) in a lime-washed arched surround
    W, H = 420, 600
    nx = Seq(1300)
    art = blank(W, H)
    cx = W / 2
    surround = shapes(W, H, [[(40, 590), (40, 170)] + [(cx + math.cos(a) * 170, 170 + math.sin(a) * 140) for a in np.linspace(math.pi, math.tau, 40)] + [(380, 590)]], smooth=False)
    art = OV(art, displace(surround, 3, 3, 30), lambda m: plaster(m, MUD_L, MUD, nx(), 0.6))
    lime = shapes(W, H, [[(70, 590), (70, 180)] + [(cx + math.cos(a) * 140, 180 + math.sin(a) * 120) for a in np.linspace(math.pi, math.tau, 40)] + [(350, 590)]], smooth=False)
    art = GP(art, lime, LIME, "#e9dfcf", seed=nx(), rough=1.0)
    door = shapes(W, H, [[(96, 590), (96, 196)] + [(cx + math.cos(a) * 114, 196 + math.sin(a) * 96) for a in np.linspace(math.pi, math.tau, 40)] + [(324, 590)]], smooth=False)
    art = OV(art, door, lambda m: wood(m, "#6a4024", TEAK_D, seed=nx(), angle=1.5708, grain=5.0))
    # carved panels: frames, rosettes, a central seam
    panels = []
    for sx0 in (110, 216):
        for (y0, y1) in [(250, 380), (396, 470), (486, 576)]:
            panels.append(rect(W, H, sx0, y0, sx0 + 94, y1))
    pm = np.maximum.reduce(panels)
    art = over(art, flat(outline(pm, 3), "#24150b", 0.75))
    hi, lo = emboss_l(pm)
    art = over(art, flat(hi, "#a4724a", 0.5)); art = over(art, flat(lo, "#1a0e06", 0.5))
    ros = []
    for sx in (157, 263):
        for (yc, r) in [(315, 34), (433, 22), (531, 26)]:
            for k in range(8):
                ros.append(petal_pts(sx, yc, r, r * 0.34, k * math.tau / 8, n=10))
    rm = shapes(W, H, ros)
    art = over(art, flat(outline(rm, 2.2), "#1e1008", 0.85))
    art = over(art, flat(rm, "#8a5a34", 0.35))
    art = over(art, flat(circles(W, H, [(sx, yc, 5) for sx in (157, 263) for yc in (315, 433, 531)]), "#c99a4a", 0.95))
    fanm = door * (1 - rect(W, H, 0, 236, W, H))
    art = over(art, flat(fanm * hatch(W, H, 0.0, 10.0, 0.18, nx(), 0.4), "#1e1008", 0.55))
    seam = rect(W, H, cx - 2, 236, cx + 2, 590)
    art = over(art, flat(seam, "#140a04", 0.9))
    studs = circles(W, H, [(x, y, 3.2) for x in (104, 206, 214, 316) for y in range(250, 590, 28)])
    art = FO(art, studs, "#b98a3e", seed=nx(), emboss=1.0, sparkle=0.1)
    ring_ = ring(W, H, cx - 14, 430, 10, 2.6)
    ring2 = ring(W, H, cx + 14, 430, 10, 2.6)
    art = FO(art, np.maximum(ring_, ring2), "#b98a3e", seed=nx(), emboss=1.0)
    step = rect(W, H, 50, 586, 370, 600)
    art = GP(art, step, LIME, "#d8ccb8", seed=nx(), rough=0.8)
    preview(art, "door")
    save(art, f"{OUT}/door.webp", max_w=260, quality=82)
    clear()

if "trim" in PARTS:
    # divider: a strip of mud wall with a whitewashed stepped parapet and a tiny lit window at the centre
    W, H = 720, 120
    nx = Seq(2100)
    art = blank(W, H)
    band = rect(W, H, 20, 52, 700, 96)
    art = OV(art, displace(band, 2, 3, 20), lambda m: plaster(m, MUD_L, MUD, nx(), 0.8))
    mer = []
    for k in range(17):
        x0 = 24 + k * 40
        mer.append([(x0, 54), (x0, 36), (x0 + 8, 36), (x0 + 8, 26), (x0 + 16, 18), (x0 + 24, 26), (x0 + 24, 36), (x0 + 32, 36), (x0 + 32, 54)])
    cap = np.maximum(shapes(W, H, mer, smooth=False), rect(W, H, 18, 48, 702, 58))
    art = GP(art, cap, LIME, "#e6d9c4", seed=nx(), rough=1.0)
    for x in (120, 600):
        art = GP(art, rect(W, H, x - 7, 64, x + 7, 86), "#2a1d1c", seed=nx(), rough=0.5, pad=6)
    win = rect(W, H, 348, 62, 372, 90)
    art = GP(art, np.clip(gaussian_filter(win, 2.5) * 1.8 - win, 0, 1), LIME, seed=nx(), rough=0.6)
    art = over(art, glow(win, "#ffb347", radius=6, strength=0.3))
    art = GP(art, win, LIT, "#ffbf5e", seed=nx(), rough=0.4, pad=6)
    preview(art, "trim")
    save(art, f"{OUT}/trim.webp", max_w=300, quality=82)
    clear()

if "adobe" in PARTS:
    # tileable warm lime-plaster texture for the page
    W = H = 320
    n1 = wrap_noise(W, H, 5, 18); n2 = wrap_noise(W, H, 6, 2.2); n3 = wrap_noise(W, H, 7, 60)
    base = col_arr("#ecdcc2")[None, None] * (0.94 + 0.07 * n1[..., None] + 0.035 * (n2[..., None] - 0.5) + 0.04 * n3[..., None])
    img = np.concatenate([np.clip(base, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/adobe.webp", quality=82)
