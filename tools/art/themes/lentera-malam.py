"""Lentera Malam — painted night sky, gouache brass lanterns with glowing glass, crescent moon, mosque skyline.
Run: python3 -I /tmp/pen/art/themes/lentera-malam.py
Palette: indigo night (#0a1028 → #2a2f66), lantern amber (#f2b257/#ffd98a), brass (#a8742f/#d9a650), moon cream (#f6dfa0).
Light comes from the lanterns/moon (upper right), so shadows sit on the left of every brass shape.
"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *

OUT = "/root/w/frontend/public/themes/art/lentera-malam"
PREV = "/tmp/pen/nt2-E"
os.makedirs(OUT, exist_ok=True)


def disc(cv, x, y, r):
    cv.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))


def path_mask(w, h, build):
    def draw(cv):
        p = skia.Path(); build(p)
        cv.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def preview_dark(arr, path, bg="#0d1530"):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 4), np.float32); base[..., :3] = hex_rgb(bg)
    to_image(over(base, arr)).convert("RGB").save(path)


# ---------------------------------------------------------------- lantern (fanous)
def lantern(seed, variant=0):
    rng = random.Random(seed)
    W, H = 200, 460
    cx = W / 2
    art = blank(W, H)
    # proportions (variant 1 = slimmer, taller onion cap)
    capT, capB = (40, 96) if variant == 0 else (30, 100)
    bodyT, bodyB = capB + 12, 300 if variant == 0 else 312
    halfT, halfB = (46, 58) if variant == 0 else (40, 50)
    # glow halo behind
    gm = shape_mask(W, H, ellipse_pts(cx, (bodyT + bodyB) / 2, 60, 110, 16))
    art = over(art, glow(gm, "#ffb24d", radius=26, strength=0.35))
    # glass body: tapering trapezoid with rounded bottom
    def body(p):
        p.moveTo(cx - halfT, bodyT); p.lineTo(cx + halfT, bodyT)
        p.lineTo(cx + halfB, bodyB - 40)
        p.cubicTo(cx + halfB - 6, bodyB - 6, cx + 20, bodyB + 6, cx, bodyB + 6)
        p.cubicTo(cx - 20, bodyB + 6, cx - halfB + 6, bodyB - 6, cx - halfB, bodyB - 40)
        p.close()
    bm = path_mask(W, H, body)
    glass = pigment(bm, "#f7c46a", "#e8913c", seed=seed + 1, density=0.88, edge=0.45, bloom=0.25, gran=0.2, rough=2.2, feather=0.8, mottle=0.4)
    art = over(art, glass)
    # hot inner light (flame zone)
    hot = shape_mask(W, H, deform(ellipse_pts(cx + 4, (bodyT + bodyB) / 2 + 10, 26, 62, 10), rng, 2, 0.1))
    art = over(art, glow(hot, "#fff1c2", radius=12, strength=0.75))
    flame = shape_mask(W, H, petal_pts(cx + 2, (bodyT + bodyB) / 2 + 36, 46, 11, -math.pi / 2 - 0.05, n=12))
    art = over(art, gouache_paint(flame, "#fffbe9", "#ffe39a", seed=seed + 2, rough=1.0, streak=0.2))
    # window arches (brass lattice painted over the glass)
    lat = blank(W, H)
    def frame(cv):
        st = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=5.5, StrokeCap=skia.Paint.kRound_Cap)
        # outer contour
        p = skia.Path(); body(p); cv.c.drawPath(p, st)
        st.setStrokeWidth(3.6)
        mid = (bodyT + bodyB) / 2
        for k in (-1, 1):   # two side ribs bowing out
            q = skia.Path(); q.moveTo(cx + k * halfT * 0.42, bodyT + 2)
            q.quadTo(cx + k * halfB * 0.6, mid, cx + k * halfB * 0.42, bodyB - 12); cv.c.drawPath(q, st)
        # pointed arch window in the centre
        a = skia.Path(); a.moveTo(cx - 17, bodyB - 34); a.lineTo(cx - 17, mid - 20)
        a.cubicTo(cx - 17, mid - 44, cx - 4, mid - 56, cx, mid - 66)
        a.cubicTo(cx + 4, mid - 56, cx + 17, mid - 44, cx + 17, mid - 20); a.lineTo(cx + 17, bodyB - 34); cv.c.drawPath(a, st)
        st.setStrokeWidth(2.4)
        cv.c.drawLine(cx - halfB + 6, mid + 6, cx + halfB - 6, mid + 6, st)
    fm = mask_from(W, H, frame)
    lat = over(lat, gouache_paint(fm, "#6b4518", "#8e5f22", seed=seed + 3, rough=1.2, streak=0.6, density=0.9))
    art = over(art, lat)
    # cap: dome + collar, brass gouache with light on the right
    def cap(p):
        p.moveTo(cx - halfT - 8, capB); p.lineTo(cx + halfT + 8, capB)
        if variant == 0:
            p.cubicTo(cx + halfT, capT + 18, cx + 18, capT, cx, capT)
            p.cubicTo(cx - 18, capT, cx - halfT, capT + 18, cx - halfT - 8, capB)
        else:
            p.cubicTo(cx + halfT + 6, capT + 46, cx + 6, capT + 30, cx, capT)
            p.cubicTo(cx - 6, capT + 30, cx - halfT - 6, capT + 46, cx - halfT - 8, capB)
        p.close()
    cm = path_mask(W, H, cap)
    col = path_mask(W, H, lambda p: p.addRoundRect(skia.Rect(cx - halfT - 10, capB - 2, cx + halfT + 10, bodyT + 2), 5, 5))
    brass = gouache_paint(np.maximum(cm, col), "#a8742f", "#c58e3e", seed=seed + 4, rough=1.4, streak=0.9)
    art = over(art, brass)
    shade = shape_mask(W, H, deform(ellipse_pts(cx - halfT * 0.75, capB - 10, halfT * 0.55, 46, 10), rng, 2, .1))
    art = glaze(art, pigment(gaussian_filter(shade, 6) * np.maximum(cm, col), "#6b4518", seed=seed + 5, density=0.3, edge=0.05, bloom=0, rough=1.5, feather=3))
    hi = stroke_mask(W, H, curve([(cx + 8, capT + 10), (cx + 26, capT + 26), (cx + halfT - 2, capB - 8)], 20), 5)
    art = over(art, gouache_paint(hi * cm, "#f2cd7e", seed=seed + 6, rough=0.8, streak=0.3, density=0.8))
    # finial + ring
    ring = mask_from(W, H, lambda cv: cv.c.drawCircle(cx, 14, 8.5, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=4)))
    stem = stroke_mask(W, H, [(cx, 22), (cx, capT + 4)], 4.5, taper=(0.01, 0.01))
    knob = shape_mask(W, H, ellipse_pts(cx, capT - 2, 7, 6, 8))
    art = over(art, gouache_paint(np.maximum(np.maximum(ring, stem), knob), "#9a6a2a", "#c08a3c", seed=seed + 7, rough=0.8))
    # bottom: little cone, then tassel cord + bead + fringe strokes
    def cone(p):
        p.moveTo(cx - 26, bodyB - 2); p.lineTo(cx + 26, bodyB - 2); p.lineTo(cx, bodyB + 30); p.close()
    co = path_mask(W, H, cone)
    art = over(art, gouache_paint(co, "#8e5f22", "#b07a32", seed=seed + 8, rough=1.0))
    cord = stroke_mask(W, H, [(cx, bodyB + 26), (cx + 1, bodyB + 62)], 6, taper=(0.02, 0.02))
    bead = shape_mask(W, H, ellipse_pts(cx + 1, bodyB + 68, 8, 8, 10))
    art = over(art, gouache_paint(np.maximum(cord, bead), "#a3302a", "#c2463a", seed=seed + 9, rough=0.8))
    fr = blank(W, H)
    for i in range(9):
        dx = (i - 4) * 2.4
        pts = curve([(cx + 1 + dx * .4, bodyB + 74), (cx + 1 + dx, bodyB + 98), (cx + 1 + dx * 1.3 + rng.uniform(-2, 2), bodyB + 122 + rng.uniform(-6, 4))], 16)
        fr = over(fr, gouache_paint(stroke_mask(W, H, pts, 2.6, taper=(0.05, 0.5)), "#b23a2f", "#8f2723", seed=seed + 20 + i, rough=0.5, streak=0.2))
    art = over(art, fr)
    return art


for name, sd, var in (("lantern", 11, 0), ("lantern-b", 37, 1)):
    a = lantern(sd, var)
    print(name, save_asset(a, f"{OUT}/{name}.webp", max_w=120, quality=84))
    preview_dark(a, f"{PREV}/lm-{name}.png")

# ---------------------------------------------------------------- crescent moon
W, H = 320, 320
rng = random.Random(5)
outer = shape_mask(W, H, deform(ellipse_pts(160, 160, 92, 92, 18), rng, 1, 0.01))
bite = shape_mask(W, H, ellipse_pts(196, 128, 82, 82, 18))
cres = np.clip(outer - bite, 0, 1)
moon = glow(cres, "#f6d68c", radius=30, strength=0.22)
moon = over(moon, glow(cres, "#f9dc95", radius=10, strength=0.3))
moon = over(moon, gouache_paint(cres, "#f8e6b2", "#efcf86", seed=7, rough=1.6, streak=0.3))
for i, (x, y, r) in enumerate([(98, 196, 12), (122, 238, 8), (84, 150, 7), (150, 252, 6)]):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * .8, 8), rng, 2, .15)) * cres
    moon = glaze(moon, pigment(m, "#d9ad62", seed=40 + i, density=0.4, edge=0.5, bloom=0, rough=1.5, feather=0.8))
shade = stroke_mask(W, H, arc_pts(160, 160, 80, 1.75, 3.6, 30), 16) * cres
moon = glaze(moon, pigment(shade, "#d8a85a", seed=55, density=0.35, edge=0.1, bloom=0.2, rough=2, feather=3))
print("moon", save_asset(moon, f"{OUT}/moon.webp", max_w=200, quality=84))
preview_dark(moon, f"{PREV}/lm-moon.png")

# ---------------------------------------------------------------- painted sky (cover background, opaque)
W, H = 780, 1640
sky = painted_sky(W, H, [(0, "#070c22"), (0.35, "#0f1840"), (0.72, "#1b2556"), (0.9, "#2a2c62"), (1, "#3a3168")], seed=21, streak=0.9, grain=0.6)
rng = random.Random(9)
# soft painted cloud bands (lighter, low opacity)
for i, (y, x, rx, ry, c) in enumerate([(380, 200, 330, 40, "#34407a"), (520, 560, 300, 34, "#2c376e"), (1100, 300, 380, 50, "#3a3d78"), (1220, 640, 260, 36, "#46407c")]):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, rx, ry, 12), rng, 3, 0.18))
    sky = over(sky, pigment(m, c, mix(c, "#5a5a96", .4), seed=60 + i, density=0.32, edge=0.25, bloom=0.5, rough=22, feather=8, mottle=0.8))
# stars: soft hand-dabbed dots, a few with a halo
def star_dots(cv, n, rmin, rmax):
    for _ in range(n):
        disc(cv, rng.uniform(0, W), rng.uniform(0, H * 0.82) ** 1.0, rng.uniform(rmin, rmax))
small = mask_from(W, H, lambda cv: star_dots(cv, 170, 0.7, 1.6))
big = mask_from(W, H, lambda cv: star_dots(cv, 22, 1.8, 3.0))
sky = over(sky, glow(big, "#fbe6b0", radius=5, strength=0.3))
sky = over(sky, gouache_paint(small, "#e9e4d4", seed=71, rough=0.5, density=0.75))
sky = over(sky, gouache_paint(big, "#fff2cc", seed=72, rough=0.6))
save_texture(sky, f"{OUT}/sky.webp", quality=74)
to_image(sky).convert("RGB").save(f"{PREV}/lm-sky.png")
print("sky", os.path.getsize(f"{OUT}/sky.webp"))

# ---------------------------------------------------------------- star dust overlay (transparent, for sections)
W, H = 600, 600
rng = random.Random(14)
sd = blank(W, H)
small = mask_from(W, H, lambda cv: [disc(cv, rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.7, 1.5)) for _ in range(60)])
big = mask_from(W, H, lambda cv: [disc(cv, rng.uniform(20, W - 20), rng.uniform(20, H - 20), rng.uniform(1.8, 2.8)) for _ in range(9)])
sd = over(sd, glow(big, "#fbe6b0", radius=5, strength=0.3))
sd = over(sd, gouache_paint(small, "#e9e4d4", seed=81, rough=0.5, density=0.6))
sd = over(sd, gouache_paint(big, "#fff2cc", seed=82, rough=0.6, density=0.9))
save_texture(sd, f"{OUT}/stardust.webp", quality=80)
print("stardust", os.path.getsize(f"{OUT}/stardust.webp"))

# ---------------------------------------------------------------- mosque skyline (bottom of cover)
W, H = 780, 230
rng = random.Random(3)
def skyline(p):
    base = 230
    p.moveTo(0, base); p.lineTo(0, 190)
    # low roofs on the left
    p.lineTo(40, 188); p.lineTo(52, 176); p.lineTo(64, 188); p.lineTo(70, 188)
    # minaret 1
    p.lineTo(70, 120); p.lineTo(74, 112); p.lineTo(78, 92); p.lineTo(82, 112); p.lineTo(86, 120); p.lineTo(86, 188)
    # big dome
    p.lineTo(180, 188); p.lineTo(180, 168)
    p.cubicTo(180, 120, 222, 98, 260, 88); p.lineTo(264, 70); p.lineTo(268, 88)
    p.cubicTo(306, 98, 348, 120, 348, 168); p.lineTo(348, 188)
    # minaret 2 (tall)
    p.lineTo(388, 188); p.lineTo(388, 82); p.lineTo(393, 72); p.lineTo(398, 40); p.lineTo(403, 72); p.lineTo(408, 82); p.lineTo(408, 188)
    # small dome
    p.lineTo(470, 188); p.lineTo(470, 176)
    p.cubicTo(470, 148, 492, 136, 512, 130); p.lineTo(515, 116); p.lineTo(518, 130)
    p.cubicTo(538, 136, 560, 148, 560, 176); p.lineTo(560, 188)
    # houses + palm on right
    p.lineTo(640, 188); p.lineTo(640, 172); p.lineTo(676, 152); p.lineTo(712, 172); p.lineTo(712, 192)
    p.lineTo(780, 194); p.lineTo(780, base); p.close()
sm = path_mask(W, H, skyline)
far = path_mask(W, H, lambda p: (p.moveTo(0, 230), p.lineTo(0, 200), p.cubicTo(200, 176, 520, 206, 780, 182), p.lineTo(780, 230), p.close()))
sk = gouache_paint(far, "#151c42", "#1c2350", seed=31, rough=4, streak=0.6, density=0.9)
sk = over(sk, gouache_paint(sm, "#080d22", "#0c1230", seed=32, rough=1.6, streak=0.8))
# rim light from the moon on the dome tops
rim = stroke_mask(W, H, curve([(196, 140), (230, 104), (262, 90)], 20), 3) * sm
rim2 = stroke_mask(W, H, curve([(486, 146), (500, 136), (514, 131)], 12), 2.4) * sm
sk = over(sk, gouache_paint(np.maximum(rim, rim2), "#3c4680", seed=33, rough=0.6, density=0.7))
# palm tree
palm = blank(W, H)
trunk = stroke_mask(W, H, curve([(742, 196), (736, 160), (744, 122)], 20), 5, taper=(0.02, 0.4))
palm = over(palm, gouache_paint(trunk, "#080d22", seed=34, rough=0.8))
for i, a in enumerate([-2.9, -2.4, -1.9, -1.2, -0.6, -0.15]):
    L = rng.uniform(34, 46)
    pts = curve([(744, 122), (744 + math.cos(a) * L * .6, 122 + math.sin(a) * L * .6 - 6), (744 + math.cos(a) * L, 122 + math.sin(a) * L + 10)], 14)
    palm = over(palm, gouache_paint(stroke_mask(W, H, pts, 7, taper=(0.1, 0.8)), "#080d22", seed=35 + i, rough=0.8))
sk = over(sk, palm)
# lit windows
win = mask_from(W, H, lambda cv: [cv.c.drawRoundRect(skia.Rect(x, y, x + w_, y + h_), 3, 3, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
                                  for x, y, w_, h_ in [(232, 160, 9, 16), (258, 156, 9, 20), (284, 160, 9, 16), (393, 120, 6, 10), (508, 160, 7, 12), (668, 170, 8, 9), (46, 194, 6, 7)]])
sk = over(sk, glow(win, "#ffb24d", radius=6, strength=0.45))
sk = over(sk, gouache_paint(win, "#ffcf7a", "#f2a64e", seed=36, rough=0.6))
print("skyline", save_asset(sk, f"{OUT}/skyline.webp", max_w=780, quality=82))
preview_dark(sk, f"{PREV}/lm-skyline.png", "#2a2c62")
