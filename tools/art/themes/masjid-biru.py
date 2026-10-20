"""Masjid Biru — painted night scene: brushed indigo sky, layered mosque skyline (watercolour haze + gouache
silhouette, lit windows), brass lantern, glowing crescent, gold star, chalky zellige tile and a gold-leaf texture.
Run: python3 -I /tmp/pen/art/themes/masjid-biru.py"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentD_lib import *  # noqa

T = "masjid-biru"
OUT = outdir(T)
SIL, SIL2 = "#060d24", "#0b1736"
HAZE, HAZE2 = "#2d4886", "#3b5897"
LIT, LIT2 = "#f2c66a", "#e09a3c"
GOLD = "#d9ad55"
rng = random.Random(7)
_s = [900]
def nxt():
    _s[0] += 19
    return _s[0]

# ---------------- 1. painted night sky (opaque, stretched to section) ----------------
SW, SH = 780, 1500
sky = painted_sky(SW, SH, [(0, "#040a1d"), (0.42, "#0b1940"), (0.78, "#173063"), (1.0, "#2a4a86")], seed=nxt(), streak=1.2, grain=0.8)
# loose horizontal cloud washes (thin, low contrast)
for (y, x0, x1, th, col) in [(0.30, -60, 520, 36, "#1b2f62"), (0.55, 260, 860, 46, "#20386f"), (0.72, -80, 420, 54, "#2a457f"), (0.86, 330, 860, 60, "#33528e")]:
    pts = [(x0, y * SH)] + [(x0 + (x1 - x0) * t, y * SH + math.sin(t * 5 + y * 9) * th * 0.35) for t in np.linspace(0.1, 1, 9)]
    m = stroke_mask(SW, SH, pts, th, taper=(0.35, 0.4))
    sky = glaze(sky, pigment(m, col, mix(col, "#0b1940", .4), seed=nxt(), density=0.32, edge=0.25, bloom=0.4, gran=0.2, rough=14, feather=6))
# warm haze at the horizon (city light)
hz = np.zeros((SH, SW), np.float32); hz[int(SH * 0.9):, :] = 1
sky = over(sky, glow(hz, "#4a5f9a", radius=60, strength=0.25))
# a few painted stars (soft dabs, varied size) — sparse, mostly upper sky
pts = [(rng.uniform(0, SW), SH * rng.uniform(0.02, 0.6) ** 1.4, rng.uniform(0.8, 2.2)) for _ in range(34)]
dabs = circle_mask(SW, SH, pts)
sky = over(sky, glow(dabs, "#dfe6ff", radius=1.2, strength=0.38))
sky[..., 3] = 1
save_plain(sky, f"{OUT}/sky.webp", quality=74)

# ---------------- 2. mosque skyline ----------------
KW, KH = 780, 320
k = 2.0; ty = KH - 150 * k
back = [
    # distant domes and minarets (viewBox 390x150)
    "M0 150V112h10l4-6 4 6h6v-8c0-10 8-14 14-22 6 8 14 12 14 22v8h20v46z",
    "M10 150V70h2l3-16 3 16h2v80z",
    "M84 150V96c0-10 10-16 16-26 6 10 16 16 16 26v54z",
    "M150 150V60h2l3-18 3 18h2v90z",
    "M228 150V60h2l3-18 3 18h2v90z",
    "M270 150V104c0-12 10-18 18-30 8 12 18 18 18 30v46z",
    "M318 150V96h40v-6c0-12 9-18 16-28 7 10 16 16 16 28v60z",
    "M370 150V66h2l3-17 3 17h2v84z",
]
front = [
    "M44 150V44h4l6-26 6 26h4v106z", "M38 66h32v5H38z", "M41 96h26v4H41z",
    "M326 150V44h4l6-26 6 26h4v106z", "M320 66h32v5h-32z", "M323 96h26v4h-26z",
    "M84 150v-50h52v50z", "M88 102c0-20 14-26 22-38 8 12 22 18 22 38z",
    "M254 150v-50h52v50z", "M258 102c0-20 14-26 22-38 8 12 22 18 22 38z",
    "M128 150V86h134v64z", "M138 88c0-40 34-52 57-74 23 22 57 34 57 74z",
    "M193.5 2h3v14h-3z", "M0 140h390v10H0z",
]
domes = ["M88 102c0-20 14-26 22-38 8 12 22 18 22 38z", "M258 102c0-20 14-26 22-38 8 12 22 18 22 38z", "M138 88c0-40 34-52 57-74 23 22 57 34 57 74z",
         "M44 44l6-26 6 26z", "M326 44l6-26 6 26z"]
win = ["M186 150v-24a9 9 0 0 1 18 0v24z", "M152 124v-12a5 5 0 0 1 10 0v12z", "M228 124v-12a5 5 0 0 1 10 0v12z",
       "M170 122v-8a3.5 3.5 0 0 1 7 0v8z", "M213 122v-8a3.5 3.5 0 0 1 7 0v8z",
       "M104 132v-12a5 5 0 0 1 10 0v12z", "M276 132v-12a5 5 0 0 1 10 0v12z",
       "M52 60h4v8h-4z", "M334 60h4v8h-4z", "M52 112h4v10h-4z", "M334 112h4v10h-4z"]
bm = svg_mask(KW, KH, back, scale=k, ty=ty)
sk = pigment(bm, HAZE, HAZE2, seed=nxt(), density=0.7, edge=0.45, bloom=0.35, gran=0.25, rough=3, feather=1.2)
# haze fades the distant layer downward into mist
yy = np.mgrid[0:KH, 0:KW][0].astype(np.float32)
sk[..., 3] *= np.clip(1.15 - (yy - ty) / (150 * k) * 0.55, 0.45, 1)
fm = svg_mask(KW, KH, front, scale=k, ty=ty)
sk = knockout(sk, fm, amount=1.0, grow=1.0)
fr = gouache_paint(fm, SIL, SIL2, seed=nxt(), rough=1.6, streak=0.9)
sk = over(sk, fr)
# moonlight rim on the right edge of domes
dm = svg_mask(KW, KH, domes, scale=k, ty=ty)
shift = np.roll(np.roll(dm, 3, axis=1), -2, axis=0)
rim = np.clip(dm - shift, 0, 1)
sk = over(sk, pigment(rim, "#3c5a92", "#5875a8", seed=nxt(), density=0.7, edge=0.2, bloom=0, gran=0.3, rough=0.8, feather=0.8))
# lit windows: warm glow + painted glass
wm = svg_mask(KW, KH, win, scale=k, ty=ty)
sk = over(sk, glow(wm, "#f0b45a", radius=7, strength=0.32))
sk = over(sk, gouache_paint(wm, LIT, LIT2, seed=nxt(), rough=0.8, streak=0.6, density=0.95))
# gold finial crescent
fin = np.clip(circle_mask(KW, KH, [(198 * k, ty + 6 * k, 5.2 * k)]) - circle_mask(KW, KH, [(196 * k, ty + 4.6 * k, 4.4 * k)]), 0, 1)
sk = over(sk, foil(fin, GOLD, seed=nxt(), emboss=0.4, sparkle=0))
save_plain(sk, f"{OUT}/skyline.webp", quality=82)
preview(sk, "#1a3366", f"{PREV}/mb-skyline.png")

# ---------------- 3. brass lantern (body only; string is CSS) ----------------
LW, LH = 128, 196
cx = LW / 2; top = 26
def L(x, y):
    return (cx + (x - 20) * 2.2, top + y * 2.2)
def poly(pts):
    return [L(*p) for p in pts]
glass = shape_mask(LW, LH, poly([(12, 15), (28, 15), (31.5, 34), (28, 52), (12, 52), (8.5, 34)]), smooth=False)
ln = glow(glass, "#ffb54d", radius=16, strength=0.55)
ln = over(ln, pigment(glass, "#ffe1a0", "#f6b555", seed=nxt(), density=0.95, edge=0.5, bloom=0.4, gran=0.15, rough=1.2, feather=0.8, mottle=0.4))
# flame-bright core
core = shape_mask(LW, LH, ellipse_pts(*L(20, 35), 7, 12, 10))
ln = over(ln, glow(core, "#fff3cf", radius=5, strength=0.5))
frame = np.clip(
    outline_mask(LW, LH, [poly([(12, 15), (28, 15), (31.5, 34), (28, 52), (12, 52), (8.5, 34)])], 3.0, rng=rng, wobble=0.25)
    + outline_mask(LW, LH, [poly([(20, 15), (20, 52)]), poly([(8.5, 34), (31.5, 34)])], 2.2, closed=False, rng=rng, wobble=0.2)
    + shape_mask(LW, LH, poly([(11, 13), (20, 4), (29, 13)]), smooth=False)
    + shape_mask(LW, LH, poly([(9, 15), (31, 15), (29, 19), (11, 19)]), smooth=False)
    + shape_mask(LW, LH, poly([(12, 52), (28, 52), (25, 58), (15, 58)]), smooth=False)
    + outline_mask(LW, LH, [poly([(20, 58), (20, 66)])], 2.6, closed=False)
    + circle_mask(LW, LH, [(*L(20, 68), 4.2)])
    + circle_mask(LW, LH, [(*L(20, 1), 5)], stroke=2.6), 0, 1)
ln = over(ln, gouache_paint(frame, "#b88a3a", "#7a5420", seed=nxt(), rough=0.7, streak=0.8))
# warm highlight on the left of the brass (light from the flame)
ln = over(ln, foil(frame * np.clip((cx + 6 - np.mgrid[0:LH, 0:LW][1]) / 30, 0, 1) * 0.5, "#e6b95c", seed=nxt(), emboss=0.4, sparkle=0))
save_plain(ln, f"{OUT}/lantern.webp", quality=84)
preview(ln, "#0c1838", f"{PREV}/mb-lantern.png")

# ---------------- 4. crescent moon ----------------
MW = 200; mc = MW / 2
moon_m = np.clip(circle_mask(MW, MW, [(mc, mc, 52)]) - circle_mask(MW, MW, [(mc + 22, mc - 14, 46)]), 0, 1)
mo = glow(moon_m, "#f6dc9c", radius=22, strength=0.28)
mo = over(mo, pigment(moon_m, "#fbe6b0", "#e8c27a", seed=nxt(), density=1.0, edge=0.4, bloom=0.45, gran=0.35, rough=1.4, feather=0.7, mottle=0.6))
save_plain(mo, f"{OUT}/moon.webp", quality=84)
preview(mo, "#0c1838", f"{PREV}/mb-moon.png")

# ---------------- 5. head star (gold gouache 8-point with halo) ----------------
S = 88; c = S / 2
sm = np.clip(shape_mask(S, S, square_pts(c, c, 15), smooth=False) + shape_mask(S, S, square_pts(c, c, 15, math.pi / 4), smooth=False), 0, 1)
st = glow(sm, "#e6b95c", radius=8, strength=0.22)
st = over(st, foil(np.clip((gaussian_filter(displace(sm, nxt(), 1.0, 8), .5) - .2) * 1.5, 0, 1), GOLD, seed=nxt(), emboss=0.7, sparkle=0.05))
save_plain(st, f"{OUT}/star.webp", quality=86)

# ---------------- 6. chalky zellige tile (transparent, seamless: 3x3 cells of 60 css px @2x) ----------------
TL = 360; u = 2
star16 = [(30, 12.4), (35.1, 17.6), (42.4, 17.6), (42.4, 24.9), (47.6, 30), (42.4, 35.1), (42.4, 42.4), (35.1, 42.4), (30, 47.6),
          (24.9, 42.4), (17.6, 42.4), (17.6, 35.1), (12.4, 30), (17.6, 24.9), (17.6, 17.6), (24.9, 17.6)]
def tile(cv):
    r = random.Random(5)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=1.8, Style=skia.Paint.kStroke_Style, StrokeJoin=skia.Paint.kRound_Join)
    for i in range(3):
        for j in range(3):
            ox, oy = i * 60 * u, j * 60 * u
            cv.c.drawPath(poly_path([(ox + x * u + r.gauss(0, .4), oy + y * u + r.gauss(0, .4)) for x, y in star16]), p)
            cv.c.drawCircle(ox + 30 * u, oy + 30 * u, 5 * u, p)
            for (a, b, c_, d) in [(0, 0, 12.4, 12.4), (60, 0, 47.6, 12.4), (0, 60, 12.4, 47.6), (60, 60, 47.6, 47.6), (30, 0, 30, 12.4), (30, 47.6, 30, 60), (0, 30, 12.4, 30), (47.6, 30, 60, 30)]:
                cv.c.drawLine(ox + a * u, oy + b * u, ox + c_ * u, oy + d * u, p)
tm = np.tile(wrap_draw(TL, TL, tile), (3, 3))
tt = pigment(tm, "#8fd6ce", "#cfe9e4", seed=nxt(), density=0.9, edge=0.2, bloom=0.3, gran=0.55, rough=0.9, feather=0.6, mottle=0.8)[TL:2 * TL, TL:2 * TL]
save_plain(tt, f"{OUT}/tile.webp", quality=78)

# ---------------- 7. gold-leaf texture (for star medallions / avatars) ----------------
GW = 400
gm = np.ones((GW, GW), np.float32)
gl = foil(gm, "#d4a64e", seed=nxt(), emboss=0, sparkle=0.25)
cr = fbm(GW, GW, nxt(), 30, 4)
gl[..., :3] *= (0.86 + 0.22 * cr)[..., None]          # crackle / leaf seams
seams = np.abs(fbm(GW, GW, nxt(), 70, 3) - 0.5) < 0.012
gl[..., :3] *= np.where(seams, 0.78, 1.0)[..., None]
save_plain(gl, f"{OUT}/gold.webp", quality=76)

tot = 0
for f in sorted(os.listdir(OUT)):
    tot += kb(f"{OUT}/{f}"); print(f, kb(f"{OUT}/{f}"), "KB", Image.open(f"{OUT}/{f}").size)
print("total", round(tot, 1), "KB")
