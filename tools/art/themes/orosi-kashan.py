"""Orosi Kashan — Persian orosi sash windows of a Kashan courtyard house: walnut lattice with ruby, cobalt, amber and
emerald glass, a sunburst fanlight, the ochre courtyard with its shallow pool. Architecture only (no figures, no
calligraphy). Run: python3 -I orosi-kashan.py [part ...]  parts: orosi pane courtyard divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q4_lib import *
from scipy.ndimage import label as nd_label

OUT = outdir("orosi-kashan")
PARTS = sys.argv[1:] or ["orosi", "pane", "courtyard", "divider"]
WOOD, WOOD_D, WOOD_L = "#4a2a18", "#24120a", "#7a4a2a"
RUBY, COBALT, AMBER, EMER, TURQ = "#b8233a", "#2a4fa8", "#e8a52a", "#2c8a5c", "#3fa3a8"


def star_lattice(x0, y0, x1, y1, s):
    """Segments of a khatam-style lattice: cell borders + an 8-point star (two squares) per cell."""
    segs = []
    nxc = max(1, round((x1 - x0) / s)); nyc = max(1, round((y1 - y0) / s))
    sx = (x1 - x0) / nxc; sy = (y1 - y0) / nyc
    for i in range(nxc + 1):
        segs.append(((x0 + i * sx, y0), (x0 + i * sx, y1)))
    for j in range(nyc + 1):
        segs.append(((x0, y0 + j * sy), (x1, y0 + j * sy)))
    centres = []
    for i in range(nxc):
        for j in range(nyc):
            cx, cy = x0 + (i + 0.5) * sx, y0 + (j + 0.5) * sy
            centres.append((cx, cy, i, j))
            r = min(sx, sy) * 0.34
            for rot in (0, math.pi / 4):
                pts = [(cx + math.cos(rot + k * math.pi / 2) * r * 1.414 / 1.414, cy + math.sin(rot + k * math.pi / 2) * r) for k in range(4)]
                pts = [(cx + math.cos(rot + math.pi / 4 + k * math.pi / 2) * r * 1.414, cy + math.sin(rot + math.pi / 4 + k * math.pi / 2) * r * 1.414) for k in range(4)] if rot == 0 else [(cx + math.cos(k * math.pi / 2) * r * 1.414, cy + math.sin(k * math.pi / 2) * r * 1.414) for k in range(4)]
                for k in range(4):
                    segs.append((pts[k], pts[(k + 1) % 4]))
            # little spokes from the star tips to the cell corners make the classic orosi web
            for k in range(4):
                a = math.pi / 4 + k * math.pi / 2
                segs.append(((cx + math.cos(a) * r * 1.414, cy + math.sin(a) * r * 1.414), (cx + math.cos(a) * sx * 0.707, cy + math.sin(a) * sy * 0.707)))
    return segs, centres, (sx, sy)


def glass_fill(W, H, panel, mullions, colour_of, seed):
    """Label the glass cells (panel minus mullions) and paint each with a translucent coloured glass."""
    free = (panel > 0.5) & (mullions < 0.25)
    lab, n = nd_label(free)
    rgb = np.zeros((H, W, 3), np.float32)
    ys, xs = np.mgrid[0:H, 0:W]
    from scipy.ndimage import center_of_mass
    cms = center_of_mass(free, lab, range(1, n + 1))
    lut = np.zeros((n + 1, 3), np.float32)
    for k, (cy, cx) in enumerate(cms, start=1):
        lut[k] = hex_rgb(colour_of(cx, cy))
    rgb = lut[lab]
    a = (lab > 0).astype(np.float32)
    # glass: mottled density, seeds/bubbles, streaky pour, light from upper-left
    mot = fbm(W, H, seed, 30, 3)
    st = streaks(H, W, seed + 4, 0.8, 9) * 0.3
    lit = np.clip(1.15 - (ys / H) * 0.35 - (xs / W) * 0.15, 0.7, 1.2)
    rgb = rgb * (0.78 + 0.34 * mot[..., None]) * (1 + st[..., None] * 0.04) * lit[..., None]
    rgb = rgb + (1 - rgb) * (np.clip(mot - 0.7, 0, 1)[..., None] * 0.9)
    alpha = a * (0.82 + 0.12 * mot)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(gaussian_filter(alpha, 0.6), 0, 1)[..., None]], -1)


def wood(art, mask, nx, light=True):
    art = GP(art, mask, WOOD, WOOD_D, seed=nx(), rough=0.7, streak=1.3, pad=6)
    if light:
        hi = np.clip(mask - np.roll(np.roll(mask, 2, 0), 2, 1), 0, 1)
        art = T(art, hi, "#c08a58", 0.45)
    return art


if "orosi" in PARTS:
    W, H = 640, 1000
    nx = Seq(30100)
    art = blank(W, H)
    outer = np.maximum(rect(W, H, 18, 318, 622, 984, 4), circles(W, H, [(320, 318, 302)]) * (np.mgrid[0:H, 0:W][0] <= 318))
    art = shadow(art, outer, "#3a2410", blur=12, strength=0.45, dx=8, dy=12)
    # glass zones
    fan = circles(W, H, [(320, 318, 272)]) * (np.mgrid[0:H, 0:W][0] <= 318).astype(np.float32)
    panes = [(44, 356, 206, 640), (230, 356, 410, 640), (434, 356, 596, 640),
             (44, 666, 206, 954), (230, 666, 410, 954), (434, 666, 596, 954)]
    panel = fan.copy()
    for (a0, b0, a1, b1) in panes:
        panel = np.maximum(panel, rect(W, H, a0, b0, a1, b1))
    # mullions: fan spokes + arcs; pane lattices
    segs = []
    for k in range(13):
        a = math.pi + k * math.pi / 12
        segs.append(((320, 318), (320 + math.cos(a) * 280, 318 + math.sin(a) * 280)))
    centres = []
    for (a0, b0, a1, b1) in panes:
        sg, cs, (csx, csy) = star_lattice(a0, b0, a1, b1, 80)
        segs += sg; centres += [(c[0], c[1], c[2] + c[3], min(csx, csy)) for c in cs]
    mull = lines(W, H, segs, 3.6)
    arcs = np.maximum.reduce([ring(W, H, 320, 318, rr, 5) for rr in (96, 176, 274)]) * (np.mgrid[0:H, 0:W][0] <= 320)
    mull = np.maximum(mull, arcs)
    mull = np.maximum(mull, circles(W, H, [(320, 318, 40)]) * 0)  # hub stays glass

    def colour_of(cx, cy):
        if cy <= 320 and math.hypot(cx - 320, cy - 318) < 280:
            r = math.hypot(cx - 320, cy - 318); ang = math.atan2(cy - 318, cx - 320)
            spoke = int((ang - math.pi) % (2 * math.pi) / (math.pi / 12))
            if r < 96:
                return AMBER
            if r < 176:
                return RUBY if spoke % 2 else "#d0602a"
            return COBALT if spoke % 2 else TURQ
        best = min(centres, key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
        d = math.hypot(best[0] - cx, best[1] - cy) / best[3]
        odd = best[2] % 2
        if d < 0.2:
            return RUBY if odd else AMBER
        if d < 0.36:
            return TURQ if odd else "#d0602a"
        return COBALT if odd else EMER
    glass = glass_fill(W, H, panel, mull, colour_of, 33)
    art = over(art, glass)
    # light glints across the glass
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    band = np.clip(1 - np.abs((xx * 0.7 + yy * 0.5) - 560) / 60, 0, 1) * panel
    art = over(art, tint(gaussian_filter(band, 6), "#fff6e0", 0.22))
    clear()
    # walnut frame + mullions
    frame = np.clip(outer - panel, 0, 1)
    art = wood(art, np.maximum(frame, mull * panel), nx)
    # carved frame moulding: a darker inner line and a highlight line
    inner = outline(panel, 6) * outer
    art = T(art, inner, WOOD_D, 0.7)
    rails = np.maximum(rect(W, H, 18, 640, 622, 666), rect(W, H, 18, 318, 622, 356))
    art = T(art, outline(rails, 3) * outer, "#c08a58", 0.35)
    # brass hub of the fan
    art = SH(art, circles(W, H, [(320, 318, 22)]), "#b88a3a", "#f6dc9a", "#5a3a12", 320, 318, 22, 22, nx(), spec=0.6, rough=0.5)
    clear()
    preview(art, "ok-orosi", tone="#e9d5b0")
    save(art, f"{OUT}/orosi.webp", max_w=460, quality=74)

if "pane" in PARTS:
    W, H = 300, 300
    nx = Seq(30500)
    art = blank(W, H)
    box = rect(W, H, 12, 12, 288, 288, 6)
    pan = rect(W, H, 30, 30, 270, 270)
    sg, cs, _ = star_lattice(30, 30, 270, 270, 80)
    mull = lines(W, H, sg, 4)
    cents = [(c[0], c[1], c[2] + c[3]) for c in cs]

    def col2(cx, cy):
        best = min(cents, key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
        d = math.hypot(best[0] - cx, best[1] - cy)
        return AMBER if d < 12 else RUBY if d < 26 else (EMER if best[2] % 2 else COBALT)
    art = over(art, glass_fill(W, H, pan, mull, col2, 51))
    art = wood(art, np.maximum(np.clip(box - pan, 0, 1), mull * pan), nx)
    preview(art, "ok-pane", tone="#e9d5b0")
    save(art, f"{OUT}/pane.webp", max_w=180, quality=84)

if "divider" in PARTS:
    W, H = 640, 60
    nx = Seq(30700)
    art = blank(W, H)
    bar = rect(W, H, 40, 22, 600, 38, 3)
    cells = [rect(W, H, x, 25, x + 24, 35, 1) for x in range(150, 490, 34)]
    art = wood(art, bar, nx)
    cols = [COBALT, RUBY, AMBER, EMER, TURQ, AMBER, RUBY, COBALT, EMER, RUBY]
    for k, c in enumerate(cells):
        art = over(art, tint(c, cols[k % len(cols)], 0.9))
    diamond = shapes(W, H, [[(320, 6), (344, 30), (320, 54), (296, 30)]], smooth=False)
    art = wood(art, diamond, nx)
    art = over(art, tint(shapes(W, H, [[(320, 16), (334, 30), (320, 44), (306, 30)]], smooth=False), AMBER, 0.95))
    for x in (40, 600):
        art = SH(art, circles(W, H, [(x, 30, 7)]), "#b88a3a", "#f6dc9a", "#5a3a12", x, 30, 7, 7, nx(), spec=0.5, rough=0.4)
    preview(art, "ok-divider", tone="#efe0c4")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=86)

if "courtyard" in PARTS:
    # Kashan courtyard house: ochre adobe facade, central iwan with an orosi, side arcades, shallow pool + reflection
    W, H = 900, 640
    nx = Seq(31100)
    art = painted_sky(W, H, [(0, "#9cc4cf"), (0.35, "#d8e2d6"), (0.36, "#e2c79a"), (1, "#d9b989")], seed=11, streak=0.8, grain=0.3)
    ADO, ADO_D, ADO_L = "#cfa676", "#9a7048", "#ecd2a6"
    # facade block
    fac = rect(W, H, 0, 120, W, 470)
    art = GP(art, fac, ADO, "#c09a6a", seed=nx(), rough=1.2, streak=0.8)
    # parapet line + top band
    art = G(art, rect(W, H, 0, 120, W, 132), ADO_D, seed=nx(), density=0.5, edge=0.2, bloom=0.1, rough=1)
    # central iwan (tall pointed arch), recessed
    def pointed(cx, base, w, h, spring):
        """Two-centred Persian arch: straight jambs to `spring`, then two arcs meeting in a point (h unused)."""
        e = w * 0.22; R = w / 2 + e
        a_end = math.acos(-e / R)
        L = [(cx - w / 2, base), (cx - w / 2, spring)]
        for i in range(1, 21):
            a = math.pi - (math.pi - a_end) * i / 20
            L.append((cx + e + math.cos(a) * R, spring - math.sin(a) * R))
        Rr = [(2 * cx - x, y) for x, y in L[::-1]]
        return L + Rr[1:]
    iwan = shapes(W, H, [pointed(450, 470, 250, 310, 260)], smooth=False)
    art = GP(art, iwan, "#a87a4c", "#8a5e36", seed=nx(), rough=1, streak=0.8)
    art = G(art, iwan * np.clip((np.mgrid[0:H, 0:W][0] - 160) / 300, 0, 1), "#6a4428", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=1)
    # orosi window inside the iwan (simplified: frame + coloured cells)
    wx0, wx1, wy0, wy1 = 372, 528, 250, 450
    win = rect(W, H, wx0, wy0, wx1, wy1)
    sg, cs, _ = star_lattice(wx0 + 6, wy0 + 6, wx1 - 6, wy1 - 6, 26)
    mull = lines(W, H, sg, 2.2)
    cents = [(c[0], c[1], c[2] + c[3]) for c in cs]

    def col3(cx, cy):
        best = min(cents, key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
        d = math.hypot(best[0] - cx, best[1] - cy)
        return AMBER if d < 4 else RUBY if d < 8 else (EMER if best[2] % 2 else COBALT)
    art = over(art, glass_fill(W, H, rect(W, H, wx0 + 6, wy0 + 6, wx1 - 6, wy1 - 6), mull, col3, 61))
    art = GP(art, np.maximum(np.clip(win - rect(W, H, wx0 + 6, wy0 + 6, wx1 - 6, wy1 - 6), 0, 1), mull * win), WOOD, WOOD_D, seed=nx(), rough=0.5)
    fanw = circles(W, H, [(450, 250, 78)]) * (np.mgrid[0:H, 0:W][0] <= 250)
    spk = lines(W, H, [((450, 250), (450 + math.cos(math.pi + k * math.pi / 8) * 80, 250 + math.sin(math.pi + k * math.pi / 8) * 80)) for k in range(9)], 2.2)
    art = over(art, glass_fill(W, H, fanw, spk, lambda cx, cy: AMBER if math.hypot(cx - 450, cy - 250) < 30 else (RUBY if int(cx) % 2 else COBALT), 63))
    art = GP(art, np.maximum(spk * fanw, ring(W, H, 450, 250, 80, 5) * (np.mgrid[0:H, 0:W][0] <= 252)), WOOD, WOOD_D, seed=nx(), rough=0.5)
    # side arcades: rows of pointed niches
    for row, (y, h) in enumerate([(300, 120), (452, 120)]):
        pass
    for cx in (90, 200, 700, 810):
        nic = shapes(W, H, [pointed(cx, 450, 78, 170, 330)], smooth=False)
        art = GP(art, nic, "#9a6c40", "#7a5030", seed=nx(), rough=1, streak=0.8)
        dw = rect(W, H, cx - 26, 360, cx + 26, 450, 2)
        art = GP(art, dw, "#3e5a6a", "#2a3e4a", seed=nx(), rough=0.6)
        art = G(art, rect(W, H, cx - 26, 360, cx + 26, 372), AMBER, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6)
        for cy_ in (180,):
            win2 = shapes(W, H, [pointed(cx, 290, 50, 92, 230)], smooth=False)
            art = GP(art, win2, "#8a5e36", "#6a4428", seed=nx(), rough=0.8)
    # brick pattern hint on facade
    br = hatch(W, H, 0.0, 11, 0.08, 7) * fac * 0.6
    art = G(art, br, ADO_D, seed=nx(), density=0.25, edge=0, bloom=0, rough=0.5, feather=0.5)
    clear()
    # courtyard floor + pool
    floor = rect(W, H, 0, 470, W, H)
    art = GP(art, floor, "#cdb08a", "#b8966c", seed=nx(), rough=1, streak=0.8)
    pool = rect(W, H, 150, 500, 750, 610, 4)
    art = GP(art, rect(W, H, 140, 492, 760, 618, 6), "#e6d4b4", "#cdb894", seed=nx(), rough=0.8)
    art = GP(art, pool, "#2f7f86", "#1f5f6a", seed=nx(), rough=0.6, streak=1.5)
    # reflection of the iwan + coloured glass in the water
    refl = np.flip(art[470 - 110:470, 150:750], 0)
    refl_a = np.zeros((H, W), np.float32); patch = np.zeros((H, W, 4), np.float32)
    patch[500:610, 150:750, :3] = refl[:110, :, :3] * 0.85 + np.array(hex_rgb("#2f7f86"), np.float32) * 0.15
    patch[500:610, 150:750, 3] = 0.42
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wave = (np.sin(yy * 0.9 + np.sin(xx * 0.05) * 2) > 0.2).astype(np.float32)
    patch[..., 3] *= pool * (0.6 + 0.4 * wave)
    art = over(art, patch)
    ripples = lines(W, H, [((x, y), (x + 40 + (x * 7) % 30, y)) for x, y in [(200, 520), (330, 548), (520, 530), (610, 580), (260, 590), (450, 572)]], 1.6)
    art = T(art, ripples * pool, "#e6f4f0", 0.5)
    # two citrus trees in planters
    for tx in (80, 820):
        trunk = strokes(W, H, [(curve([(tx, 600), (tx + 4, 540), (tx - 2, 500)], 12), 7, None)])
        art = GP(art, trunk, "#5a3a22", seed=nx(), rough=0.6)
        crown = shapes(W, H, [deform(ellipse_pts(tx, 470, 62, 52, 14), random.Random(tx), 2, 0.12)])
        art = G(art, crown, "#5f8a4a", "#2f5a32", seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=6)
        fruit = circles(W, H, [(tx + random.Random(tx + k).uniform(-40, 40), 470 + random.Random(tx + k * 3).uniform(-30, 30), 4.5) for k in range(9)])
        art = T(art, fruit, "#e8962a", 0.9)
        pot = shapes(W, H, [[(tx - 30, 600), (tx + 30, 600), (tx + 22, 636), (tx - 22, 636)]], smooth=False)
        art = GP(art, pot, "#2a6a8a", "#1c4a62", seed=nx(), rough=0.6)
    art = vignette(art, 0.18)
    clear()
    on = to_image(art).convert("RGB"); on.save(f"{PREV}/ok-courtyard.png")
    save_opaque(art, f"{OUT}/courtyard.webp", size=(720, 512), quality=72)
