"""Pantai Senja — painted sunset beach (sky/sea scene, palm silhouettes, wave bands, shell, night sky).
Run: python3 -I /tmp/pen/art/themes/pantai-senja.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentc import *  # noqa

OUT = "/root/w/frontend/public/themes/art/pantai-senja"
PRE = "/tmp/pen/nt2-C/ps"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(21)
seed = [500]
def nxt():
    seed[0] += 13
    return seed[0]

NIGHT, PLUM, ROSE, CORAL, PEACH, SUN = "#2b2148", "#57336a", "#a84a66", "#e2725b", "#f6b98a", "#ffd38a"
SEA, SEA_D, FOAM, SAND = "#3d5f8a", "#24395c", "#fdf7ef", "#f8ecdc"
SIL = "#2a1b38"


def cloud_streaks(W, y0, y1, n, cols, wmin=14, wmax=40, xspan=(0.1, 0.9), dens=0.32):
    lay = blank(W, H_)
    for i in range(n):
        y = rng.uniform(y0, y1)
        x0 = rng.uniform(-0.2, xspan[1]) * W
        L = rng.uniform(0.25, 0.7) * W
        pts = curve([(x0, y), (x0 + L * .35, y - rng.uniform(-8, 8)), (x0 + L * .7, y + rng.uniform(-10, 6)), (x0 + L, y + rng.uniform(-6, 6))], 40)
        m = stroke_mask(W, H_, pts, rng.uniform(wmin, wmax), taper=(0.35, 0.4))
        ca, cb = cols[i % len(cols)]
        lay = glaze(lay, pigment(m, ca, cb, seed=nxt(), density=dens * rng.uniform(.7, 1.2), edge=.35, bloom=.4, rough=9, gran=.15, feather=2.2))
    return lay


# ---------------- cover scene (opaque) ----------------
W, H_ = 780, 1688
HZ = int(H_ * 0.64)
sky = painted_sky(W, H_, [(0, NIGHT), (.24, PLUM), (.44, ROSE), (.56, CORAL), (.64, PEACH), (1, PEACH)], seed=nxt(), streak=.4)
# soft warm bloom around the sun
sun_c = (W * 0.5, HZ - 26)
sky = over(sky, glow(circle_mask(W, H_, *sun_c, 120), "#ffcf8f", radius=90, strength=.55))
# clouds: plum streaks high, rose/coral mid, lit peach undersides near horizon
sky = glaze(sky, cloud_streaks(W, 330, 560, 6, [("#6a3a6c", "#834470"), ("#7a3f6e", "#5b3466")], 16, 44, dens=.28))
sky = glaze(sky, cloud_streaks(W, 600, 860, 7, [("#c05868", "#d06a62"), ("#b4506a", "#c96a6a")], 12, 34, dens=.30))
lit = blank(W, H_)
for i in range(6):
    y = rng.uniform(880, 1030); x0 = rng.uniform(-.1, .7) * W; L = rng.uniform(.18, .45) * W
    pts = curve([(x0, y), (x0 + L / 2, y + rng.uniform(-4, 4)), (x0 + L, y + rng.uniform(-4, 4))], 30)
    lit = over(lit, scale_alpha(pigment(stroke_mask(W, H_, pts, rng.uniform(6, 14), taper=(.4, .4)), "#ffe0a8", "#ffc98c", seed=nxt(), density=.45, edge=.2, bloom=.2, rough=5), .8))
sky = over(sky, lit)
# sun disc (painted, slightly uneven), sinking into the horizon
disc = shape_mask(W, H_, deform(ellipse_pts(*sun_c, 70, 68, 40), rng, 1, .012))
disc[HZ:] = 0
sky = over(sky, pigment(disc, "#fff3cf", "#ffd994", seed=nxt(), density=1.0, edge=.15, bloom=.1, rough=2.5, gran=.05, mottle=.2))
sky = over(sky, scale_alpha(glow(disc, "#fff0c0", radius=10, strength=.6), .5))

# sea
sea = painted_sky(W, H_ - HZ, [(0, "#4f6d94"), (.25, SEA), (1, SEA_D)], seed=nxt(), streak=.45)
sea_full = blank(W, H_); sea_full[HZ:] = sea
# wobbly horizon edge
hz_mask = np.zeros((H_, W), np.float32); hz_mask[HZ:] = 1
hz_mask = np.clip(displace(hz_mask, nxt(), 1.5, 60), 0, 1)
sea_full[..., 3] = hz_mask
scene = over(sky, sea_full)
# light swells: horizontal brush dabs lighter/darker blue
sw = blank(W, H_)
for i in range(70):
    y = rng.uniform(HZ + 14, H_ - 10)
    depth = (y - HZ) / (H_ - HZ)
    L = rng.uniform(40, 180) * (0.5 + depth)
    x = rng.uniform(-40, W)
    pts = [(x, y), (x + L * .5, y + rng.uniform(-2, 2)), (x + L, y + rng.uniform(-2, 2))]
    col = rng.choice([("#5b7ba3", "#6a86ab"), ("#1f3252", "#28406a"), ("#8a7fa8", "#9a87a8")])
    sw = over(sw, scale_alpha(pigment(stroke_mask(W, H_, curve(pts, 12), rng.uniform(3, 8) * (0.6 + depth)), *col, seed=nxt(), density=.5, edge=.3, bloom=0, rough=2.5, feather=1), .55))
scene = over(scene, sw)
# sun glitter path: short warm dabs widening toward the viewer
gl = blank(W, H_)
for i in range(150):
    t = rng.random() ** 1.3
    y = HZ + 6 + t * (H_ - HZ) * 0.62
    spread = 30 + t * 210
    x = W / 2 + rng.gauss(0, spread * 0.45)
    L = rng.uniform(10, 40) * (0.6 + t * 1.6)
    pts = [(x - L / 2, y), (x, y + rng.uniform(-1.5, 1.5)), (x + L / 2, y)]
    col = rng.choice([("#ffe6b0", "#ffd38a"), ("#fff4d6", "#ffe0a6"), ("#f6b98a", "#f2a27c")])
    a = (1 - t) ** 1.2 * .95
    gl = over(gl, scale_alpha(pigment(stroke_mask(W, H_, curve(pts, 8), rng.uniform(2.5, 6) * (0.7 + t)), *col, seed=nxt(), density=.9, edge=.2, bloom=0, rough=1.5, feather=.7), a))
scene = over(scene, gl)
scene[..., 3] = 1
print("cover-scene", save_opaque(scene, f"{OUT}/cover-scene.webp", quality=74), round(kb(f"{OUT}/cover-scene.webp")))


# ---------------- wave tiles (tileable, 2 crests per 390 css px) ----------------
def wave_tile(h, top, amp, cols, dens, phase=0.0, lace=False, solid_alpha=1.0, fade_bottom=True):
    TW, OV = 780, 120
    w = TW + OV
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    crest = top + amp * np.sin((xx / (TW / 2)) * math.tau + phase)
    m = (yy > crest).astype(np.float32)
    m = gaussian_filter(m, .8)
    lay = pigment(m, *cols, seed=nxt(), density=dens, edge=.6, bloom=.3, rough=4, gran=.2, feather=1.2, mottle=.6)
    if lace:  # broken, frothy foam line riding on the crest
        segs = []
        x = -10.0
        while x < w:
            L = rng.uniform(14, 60)
            pts = []
            for k in range(8):
                xx_ = x + L * k / 7
                pts.append((xx_, top + amp * math.sin((xx_ / (TW / 2)) * math.tau + phase) + rng.uniform(-1.2, 1.2)))
            segs.append((pts, rng.uniform(2.5, 6.5)))
            x += L + rng.choice([rng.uniform(1, 5), rng.uniform(8, 22)])
        fm = strokes_mask(w, h, segs)
        spray = []
        for _ in range(int(w / 9)):
            xx_ = rng.uniform(0, w)
            yy_ = top + amp * math.sin((xx_ / (TW / 2)) * math.tau + phase) + rng.uniform(3, 16)
            spray.append((xx_, yy_, rng.uniform(.8, 2.4)))
        fm = np.maximum(fm, dots_mask(w, h, spray))
        lay = over(lay, pigment(fm, "#ffffff", "#fff1e0", seed=nxt(), density=.92, edge=.25, bloom=.1, rough=3.0, feather=.8, holes=.12))
    if fade_bottom:
        k = np.clip((h - yy) / (h * .45), 0, 1)
        lay[..., 3] *= k
    lay = tileable_x(lay, OV)
    lay[..., 3] *= solid_alpha
    return lay

back = wave_tile(68, 26, 14, ("#ffc4a0", "#f6b98a"), .36, 0)
print("wave-back", save_full(back, f"{OUT}/wave-back.webp", quality=80), round(kb(f"{OUT}/wave-back.webp")))
mid = wave_tile(80, 30, 14, ("#3d5f8a", "#4a6c96"), .85, 1.4, lace=True)
print("wave-mid", save_full(mid, f"{OUT}/wave-mid.webp", quality=80), round(kb(f"{OUT}/wave-mid.webp")))
front = wave_tile(108, 34, 18, ("#fdf7ef", "#f2e6da"), .42, 2.4, lace=True, fade_bottom=False)
print("wave-front", save_full(front, f"{OUT}/wave-front.webp", quality=80), round(kb(f"{OUT}/wave-front.webp")))


# ---------------- section edges (opaque sand / foam band with lacy foam rim) ----------------
def edge(col, name):
    w, h = 780, 92
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    crest = 40 + 20 * np.sin(xx / 390 * math.tau + 0.4)
    m = (yy > crest).astype(np.float32)
    lay = gouache_paint(m, col, mix(col, "#ffffff", .3), seed=nxt(), rough=3, streak=.6, density=1.0)
    # flatten towards the bottom so it meets the section colour exactly
    k = np.clip((yy - 70) / 18, 0, 1)[..., None]
    lay[..., :3] = lay[..., :3] * (1 - k) + np.array(hex_rgb(col), np.float32) * k
    lay[-6:, :, 3] = 1
    segs, spray = [], []
    x = -10.0
    while x < w:
        L = rng.uniform(14, 60)
        segs.append(([(x + L * k / 7, 40 + 20 * math.sin((x + L * k / 7) / 390 * math.tau + 0.4) + rng.uniform(-1, 1)) for k in range(8)], rng.uniform(2.5, 6)))
        x += L + rng.choice([rng.uniform(1, 5), rng.uniform(8, 20)])
    for _ in range(80):
        xx_ = rng.uniform(0, w)
        spray.append((xx_, 40 + 20 * math.sin(xx_ / 390 * math.tau + 0.4) - rng.uniform(4, 12), rng.uniform(.8, 2.2)))
    lace = np.maximum(strokes_mask(w, h, segs), dots_mask(w, h, spray))
    lay = over(lay, pigment(lace, "#ffffff", seed=nxt(), density=.92, edge=.25, bloom=.1, rough=2.5, feather=.7, holes=.1))
    print(name, save_full(lay, f"{OUT}/{name}.webp", quality=82), round(kb(f"{OUT}/{name}.webp")))
    return lay

edge(SAND, "edge-sand")
edge(FOAM, "edge-foam")


# ---------------- palm (trunk + crown, 280x520 shared canvas = 2x viewBox 140x260) ----------------
PW, PH = 360, 560  # 2x of viewBox x -20..160, y -10..270
OX, OY = 40, 20
def P(x, y):
    return (x * 2 + OX, y * 2 + OY)
trunk_c = curve([P(36, 262), P(42, 214), P(56, 150), P(70, 108), P(88, 74)], 60)
def trunk_draw(cv):
    n = len(trunk_c)
    for i in range(n - 1):
        t = i / (n - 1)
        wdt = 19 - 8 * t
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        cv.c.drawLine(*trunk_c[i], *trunk_c[i + 1], p)
tm = mask_from(PW, PH, trunk_draw)
trunk = pigment(tm, SIL, "#3a2448", seed=nxt(), density=1.0, edge=.5, bloom=.15, rough=1.8, gran=.2, feather=.8, mottle=.3)
# growth rings: darker ticks across the trunk
rings = []
for i in range(4, len(trunk_c) - 3, 3):
    (x0, y0), (x1, y1) = trunk_c[i - 1], trunk_c[i + 1]
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    t = i / len(trunk_c); hw = (19 - 8 * t) / 2
    cx, cy = trunk_c[i]
    rings.append(([(cx - nx * hw, cy - ny * hw + 1), (cx, cy + 2.5), (cx + nx * hw, cy + ny * hw + 1)], 1.6))
trunk = glaze(trunk, pigment(strokes_mask(PW, PH, rings), "#120c1a", seed=nxt(), density=.7, edge=0, bloom=0, rough=.8, feather=.5))
# warm rim light on the sun-facing side
rim_pts = [(x + 6, y) for x, y in trunk_c[8:-6]]
trunk = over(trunk, scale_alpha(pigment(stroke_mask(PW, PH, rim_pts, 2.6, taper=(.3, .3)), "#a2506a", "#c0646a", seed=nxt(), density=.8, edge=0, bloom=0, rough=1, feather=.7), .55))
print("palm-trunk", save_full(trunk, f"{OUT}/palm-trunk.webp", quality=82), round(kb(f"{OUT}/palm-trunk.webp")))

cx, cy = P(88, 72)
fronds = []
for ang, L, droop in [(196, 168, 1.1), (226, 150, .9), (258, 120, .5), (292, 132, .7), (326, 156, 1.0), (356, 150, 1.25), (150, 116, .7), (40, 112, .7), (98, 70, .2), (210, 120, 1.4)]:
    a = math.radians(ang)
    sgn = 1 if math.cos(a) >= 0 else -1
    pts = [(cx, cy)]; x, y = cx, cy; steps = 26
    for k in range(steps):
        a += droop * sgn / steps * 1.2
        x += math.cos(a) * L / steps; y += math.sin(a) * L / steps
        pts.append((x, y))
    fronds.append((pts, L))
strokes = []
for pts, L in fronds:
    strokes.append((pts, 5.5))
    n = len(pts)
    for k in range(2, n - 1):
        s_ = k / (n - 1)
        (x0, y0), (x1, y1) = pts[k - 1], pts[k + 1]
        d = math.atan2(y1 - y0, x1 - x0)
        for side in (-1, 1):
            la = d + side * rng.uniform(.75, 1.05)
            # leaflets hang: pull towards gravity
            lx, ly = math.cos(la), math.sin(la) + .55
            nn = math.hypot(lx, ly); lx, ly = lx / nn, ly / nn
            ll = L * .36 * (1 - s_ * .72) * rng.uniform(.8, 1.15)
            px, py = pts[k]
            strokes.append(([(px, py), (px + lx * ll * .55 + rng.uniform(-2, 2), py + ly * ll * .5), (px + lx * ll, py + ly * ll + ll * .12)], rng.uniform(4.2, 6.5)))
fm = strokes_mask(PW, PH, strokes)
crown = pigment(fm, SIL, "#38223f", seed=nxt(), density=1.0, edge=.5, bloom=.1, rough=1.6, gran=.2, feather=.7, mottle=.25)
nuts = dots_mask(PW, PH, [(cx - 7, cy + 14, 9), (cx + 9, cy + 16, 9), (cx + 1, cy + 26, 8)])
crown = over(crown, pigment(nuts, "#1d1328", "#2f1d3a", seed=nxt(), density=1.0, edge=.4, bloom=0, rough=1.2, feather=.6))
print("palm-crown", save_full(crown, f"{OUT}/palm-crown.webp", quality=82), round(kb(f"{OUT}/palm-crown.webp")))
palm_prev = over(trunk, crown)


# ---------------- birds (ink strokes) ----------------
BW, BH = 170, 66
bl = []
for (bx, by, s_) in [(20, 30, 1.0), (82, 14, .85), (132, 44, .9)]:
    bl.append(([(bx - 18 * s_, by + 4), (bx - 9 * s_, by - 7 * s_), (bx, by + 2)], 3.2 * s_))
    bl.append(([(bx, by + 2), (bx + 9 * s_, by - 8 * s_), (bx + 19 * s_, by + 3)], 3.2 * s_))
birds = pigment(strokes_mask(BW, BH, bl), SIL, seed=nxt(), density=.85, edge=.5, bloom=0, rough=1, feather=.6)
print("birds", save_full(birds, f"{OUT}/birds.webp", quality=82), round(kb(f"{OUT}/birds.webp")))


# ---------------- shell (watercolour scallop) ----------------
SW = 120
fan = []
for i in range(19):
    t = i / 18 * math.pi
    r = 50 + 3 * math.sin(i * 1.7)
    fan.append((60 + math.cos(math.pi + t) * r, 70 + math.sin(math.pi + t) * r * .92))
fan += [(70, 96), (60, 102), (50, 96)]
fm = shape_mask(SW, SW, deform(fan, rng, 1, .02))
shell = pigment(fm, "#f4b48e", "#eb8f72", seed=nxt(), density=.6, edge=.7, bloom=.4, rough=2.5, gran=.25, feather=.9)
ribs = [([(60, 98), (60 + math.cos(math.pi + t) * 46, 70 + math.sin(math.pi + t) * 42)], 2.4) for t in [k / 6 * math.pi for k in range(1, 6)]]
shell = glaze(shell, pigment(strokes_mask(SW, SW, ribs), "#c4553f", "#b14a3c", seed=nxt(), density=.55, edge=.3, bloom=0, rough=1.2, feather=.6))
hinge = shape_mask(SW, SW, [(46, 96), (74, 96), (68, 108), (52, 108)])
shell = glaze(shell, pigment(hinge, "#e2725b", seed=nxt(), density=.6, edge=.5, bloom=0, rough=1.2))
print("shell", save_asset(shell, f"{OUT}/shell.webp", quality=84), round(kb(f"{OUT}/shell.webp")))


# ---------------- dusk sky (countdown section) ----------------
H_ = 1100
dusk = painted_sky(W, H_, [(0, NIGHT), (.45, "#6c3a68"), (.85, "#d0625a"), (1, "#e98a63")], seed=nxt(), streak=.4)
dusk = glaze(dusk, cloud_streaks(W, 360, 640, 6, [("#7a3f6e", "#8a4672"), ("#5e3466", "#6c3a68")], 14, 36, dens=.26))
dusk = glaze(dusk, cloud_streaks(W, 760, 1000, 5, [("#c25a62", "#d06a62")], 10, 26, dens=.25))
dusk[..., 3] = 1
print("dusk-sky", save_opaque(dusk, f"{OUT}/dusk-sky.webp", quality=72), round(kb(f"{OUT}/dusk-sky.webp")))


# ---------------- night sky (closing) + stars + moon ----------------
H_ = 1400
night = painted_sky(W, H_, [(0, NIGHT), (.55, "#3c2a5a"), (1, SEA_D)], seed=nxt(), streak=.4)
night = glaze(night, cloud_streaks(W, 500, 900, 5, [("#4a3466", "#523a6c")], 16, 40, dens=.2))
night[..., 3] = 1
print("night-sky", save_opaque(night, f"{OUT}/night-sky.webp", quality=72), round(kb(f"{OUT}/night-sky.webp")))

SH = 760
stars_pts = [(rng.uniform(10, W - 10), rng.uniform(10, SH - 10) ** 1.0, rng.choice([1.2, 1.5, 1.8, 2.4, 3.0])) for _ in range(46)]
sm = dots_mask(W, SH, stars_pts)
stars = over(glow(sm, "#fff2d6", radius=4, strength=.5), pigment(sm, "#fffaf0", "#ffe9c2", seed=nxt(), density=1.0, edge=0, bloom=0, rough=.6, feather=.5))
print("stars", save_full(stars, f"{OUT}/stars.webp", quality=80), round(kb(f"{OUT}/stars.webp")))

MW = 180
outer = circle_mask(MW, MW, 90, 90, 46)
bite = circle_mask(MW, MW, 70, 80, 44)
cres = np.clip(outer - bite, 0, 1)
moon = glow(outer, "#fbe7c0", radius=16, strength=.14)
moon = over(moon, pigment(cres, "#fdf0d0", "#f7dca6", seed=nxt(), density=1.0, edge=.3, bloom=.3, rough=1.6, gran=.25, feather=.8))
print("moon", save_full(moon, f"{OUT}/moon.webp", quality=84), round(kb(f"{OUT}/moon.webp")))

# ---------------- previews ----------------
prev = scene.copy()
for img, (x, y) in [(back, (0, HZ + 70)), (mid, (0, HZ + 200)), (front, (0, 1688 - 108))]:
    h, w = img.shape[:2]
    prev[y:y + h, :w] = over(prev[y:y + h, :w], img)
ph, pw = palm_prev.shape[:2]
prev[1688 - int(1688 * .3) - ph:1688 - int(1688 * .3), -60 + 60:pw] = over(prev[1688 - int(1688 * .3) - ph:1688 - int(1688 * .3), 0:pw], palm_prev)
on_bg(prev, prev).save(f"{PRE}/cover.png")
on_color(palm_prev, "#e98a63").save(f"{PRE}/palm.png")
on_color(shell, SAND).save(f"{PRE}/shell.png")
nprev = night[:SH].copy(); nprev = over(nprev, stars); nprev[40:220, 560:740] = over(nprev[40:220, 560:740], moon)
on_bg(nprev, nprev).save(f"{PRE}/night.png")
e = np.concatenate([np.ones((92, 780, 4), np.float32) * np.array([*hex_rgb("#7a5a8a"), 1], np.float32)], 0)
on_bg(over(e, np.asarray(Image.open(f"{OUT}/edge-sand.webp").convert("RGBA"), np.float32) / 255), e).save(f"{PRE}/edge.png")
