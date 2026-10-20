"""Kencan — painted cover backdrop (gouache sunset-pink wash with brush streaks + soft hand-cut hearts),
gouache tier stickers (super like star, boost bolt, flame) and wishlist vignettes (espresso machine, tent).
Run: python3 -I /tmp/pen/art/themes/kencan.py
Paints: pink (#fd3a73), coral (#ff7854), cream (#fff3ee), sky (#35c9f3), violet (#b06bff), ink (#2b1f26).
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p6_lib import *

OUT = "/root/w/frontend/public/themes/art/kencan"
os.makedirs(OUT, exist_ok=True)
nxt = Seeds(1100)
INK = "#2b1f26"

def heart_pts(cx, cy, s, n=40):
    pts = []
    for i in range(n):
        t = i / (n - 1) * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    return pts

# ---------------------------------------------------------------- cover backdrop 480x1040 (css: cover)
W, H = 480, 1040
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
ang = math.radians(300 - 90)  # css 300deg → direction vector
dx, dy = math.sin(math.radians(300)), -math.cos(math.radians(300))
t = (xx * dx + yy * dy); t = (t - t.min()) / (t.max() - t.min())
t = np.clip(t + (fbm(W, H, nxt(), 160, 3) - 0.5) * 0.12, 0, 1)
ca, cb, cc = np.array(hex_rgb("#fd3a73")), np.array(hex_rgb("#ff5f63")), np.array(hex_rgb("#ff7854"))
rgb = np.where(t[..., None] < 0.5, ca * (1 - t[..., None] * 2) + cb * t[..., None] * 2, cb * (1 - (t[..., None] - 0.5) * 2) + cc * (t[..., None] - 0.5) * 2).astype(np.float32)
# brush streaks along the gradient direction + grain
s = gaussian_filter(np.random.default_rng(7).random((H, W)).astype(np.float32), (1.2, 16))
s = (s - s.mean()) / (s.std() + 1e-6)
g = gaussian_filter(np.random.default_rng(8).random((H, W)).astype(np.float32), 0.6)
g = (g - g.mean()) / (g.std() + 1e-6)
low = fbm(W, H, nxt(), 220, 3) - 0.5
rgb = np.clip(rgb * (1 + s[..., None] * 0.016 + g[..., None] * 0.018 + low[..., None] * 0.14), 0, 1)
bg = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
# soft darker wash top-left and bottom-right so the white cards pop
vign = np.clip(((xx - W * 0.5) ** 2 / (W * 0.9) ** 2 + (yy - H * 0.42) ** 2 / (H * 0.75) ** 2), 0, 1)
bg[..., :3] *= (1 - vign[..., None] * 0.14)
# hand-cut hearts (lighter and darker, low alpha), avoiding the centre where the cards sit
rng = random.Random(21)
placed = []
for i in range(26):
    for _ in range(60):
        x, y = rng.uniform(20, W - 20), rng.uniform(40, H - 120)
        if 50 < x < W - 50 and 30 < y < 175:  # "It's a Match!" title zone
            continue
        if 60 < x < W - 60 and 250 < y < 640:  # card zone
            continue
        if 60 < x < W - 60 and 600 < y < 900:  # names / kepada zone
            continue
        if all(math.hypot(x - px, y - py) > 70 for px, py in placed):
            break
    placed.append((x, y))
    sz = rng.uniform(14, 40)
    m = shape_mask(W, H, deform(heart_pts(x, y, sz), rng, 2, .03))
    rot = rng.uniform(-0.4, 0.4)
    light = rng.random() < 0.6
    col, col2 = ("#ffd2cf", "#ffb7b3") if light else ("#d9245c", "#c21d50")
    layer = gouache_paint(m, col, col2, seed=nxt(), rough=2.5, streak=0.8, density=rng.uniform(0.22, 0.4))
    bg = over(bg, layer)
# a few cream speckles (confetti)
sp = np.zeros((H, W), np.float32)
for _ in range(40):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    if 60 < x < W - 60 and 250 < y < 900:
        continue
    sp = np.maximum(sp, circ(W, H, x, y, rng.uniform(1.5, 3.5)))
bg = over(bg, tint_layer(sp, "#fff3ee", 0.55))
bg[..., 3] = 1
print("cover-bg", save_full(bg, f"{OUT}/cover-bg.webp", (W, H), 78) // 1024, "KB")
to_image(bg).convert("RGB").resize((240, 520)).save(f"{PREV}/kc-cover-bg.png")

# ---------------------------------------------------------------- tier stickers 96px (css 34px)
S = 96
def outline(m, w=3.2, wob=0.3, col=INK):
    return brush_outline(m, w, nxt(), col, mix(col, "#ffffff", .12), wobble=wob, density=0.9)
def paint(m, c, c2=None, light=None, k=0.3, rough=1.8, streak=0.8):
    g = gouache_paint(m, c, c2 or mix(c, "#000000", .12), seed=nxt(), rough=rough, streak=streak)
    if light:
        g = darken(g, m, light[0], light[1], k, radius=S * 0.9)
    return g
def sticker(layer, mask, grow=4):
    edge = np.clip(gaussian_filter(mask, grow) * 3.0, 0, 1)
    return over(gouache_paint(edge, "#fff3ee", "#f7e3dc", seed=nxt(), rough=1.4, streak=0.3), layer)

rng = random.Random(31)
# super like: five-point star
pts = [(48 + math.cos(-math.pi / 2 + i * math.pi / 5) * (36 if i % 2 == 0 else 16), 50 + math.sin(-math.pi / 2 + i * math.pi / 5) * (36 if i % 2 == 0 else 16)) for i in range(10)]
sm = gaussian_filter(shape_mask(S, S, deform(pts, rng, 1, .02), smooth=False), 0.8)
star = paint(sm, "#35c9f3", "#1aa6d6", light=(30, 25))
hi = shape_mask(S, S, deform(ellipse_pts(40, 40, 9, 6, 10, -0.6), rng, 2, .1)) * sm
star = over(star, tint_layer(gaussian_filter(hi, 1.5), "#d8f6ff", 0.6))
star = over(star, outline(sm, 3.0, 0.35))
star = sticker(star, sm)
# boost: lightning bolt
bolt_pts = [(56, 8), (30, 54), (46, 54), (38, 90), (68, 42), (52, 42)]
bm = gaussian_filter(shape_mask(S, S, deform(bolt_pts, rng, 1, .02), smooth=False), 0.8)
bolt = paint(bm, "#b06bff", "#8a46e0", light=(35, 20))
hi = stroke_mask(S, S, densify([(50, 16), (38, 46)], 2), 4, taper=(0.3, 0.3)) * bm
bolt = over(bolt, tint_layer(gaussian_filter(hi, 1.2), "#e9d8ff", 0.6))
bolt = over(bolt, outline(bm, 3.0, 0.3))
bolt = sticker(bolt, bm)
# flame
def flame_path(p):
    p.moveTo(48, 88); p.cubicTo(22, 88, 16, 60, 30, 44); p.cubicTo(34, 56, 42, 56, 42, 48)
    p.cubicTo(42, 32, 36, 24, 50, 8); p.cubicTo(52, 30, 70, 34, 72, 54); p.cubicTo(76, 72, 66, 88, 48, 88); p.close()
fm = gaussian_filter(path_mask(S, S, flame_path), 0.8)
flame = paint(fm, "#fd3a73", "#e0255e", light=(40, 70), k=0.25)
def inner_path(p):
    p.moveTo(48, 84); p.cubicTo(36, 84, 32, 70, 40, 60); p.cubicTo(42, 66, 48, 66, 48, 58)
    p.cubicTo(48, 50, 48, 48, 52, 42); p.cubicTo(56, 54, 64, 58, 62, 70); p.cubicTo(62, 78, 56, 84, 48, 84); p.close()
im_ = gaussian_filter(path_mask(S, S, inner_path), 0.8)
flame = over(flame, paint(im_, "#ffb14a", "#ff8a3c", light=(44, 80), k=0.2))
flame = over(flame, outline(fm, 3.0, 0.35))
flame = sticker(flame, fm)
for name, arr in [("superlike", star), ("boost", bolt), ("flame", flame)]:
    print(name, save_full(arr, f"{OUT}/tier-{name}.webp", (S, S), 84) // 1024, "KB")

# ---------------------------------------------------------------- wishlist vignettes 120px (css 40px)
V = 120
def vpaint(m, c, c2=None, light=None, k=0.3, rough=1.6, streak=0.8):
    g = gouache_paint(m, c, c2 or mix(c, "#000000", .12), seed=nxt(), rough=rough, streak=streak)
    if light:
        g = darken(g, m, light[0], light[1], k, radius=V * 0.9)
    return g
rng = random.Random(41)
# espresso machine
esp = blank(V, V)
body = rrect(V, V, 26, 22, 68, 70, 10)
esp = over(esp, tint_layer(np.roll(gaussian_filter(body, 5), 6, axis=0), "#7a3a4a", 0.2))
esp = over(esp, vpaint(body, "#e9e4e6", "#cfc6ca", light=(30, 20), k=0.35))
top = rrect(V, V, 22, 16, 76, 14, 5)
esp = over(esp, vpaint(top, "#3b2f36", "#241b20", light=(30, 10), k=0.3))
head = rrect(V, V, 44, 40, 32, 12, 3)
esp = over(esp, vpaint(head, "#3b2f36", "#241b20"))
spout = rrect(V, V, 56, 52, 8, 10, 2)
esp = over(esp, vpaint(spout, "#8a8086", "#6c636a"))
cupm = path_mask(V, V, lambda p: (p.moveTo(50, 66), p.lineTo(70, 66), p.lineTo(67, 84), p.lineTo(53, 84), p.close()))
esp = over(esp, vpaint(cupm, "#fff3ee", "#f1dcd4", light=(40, 60), k=0.25))
esp = over(esp, tint_layer(rrect(V, V, 53, 66, 14, 4, 1) * cupm, "#6b4a3a", 0.8))
tray = rrect(V, V, 34, 86, 52, 6, 2)
esp = over(esp, vpaint(tray, "#3b2f36", "#241b20"))
light_ = circ(V, V, 36, 50, 3.5)
esp = over(esp, glow(light_, "#fd3a73", 4, 0.8)); esp = over(esp, vpaint(light_, "#fd3a73", rough=0.5))
knob = circ(V, V, 84, 50, 5)
esp = over(esp, vpaint(knob, "#8a8086", "#6c636a"))
steam = stroke_mask(V, V, curve([(62, 62), (66, 56), (62, 50)], 12), 2, taper=(0.3, 0.3))
esp = over(esp, tint_layer(gaussian_filter(steam, 0.8), "#b9aeb4", 0.6))
for m in (body, top, head, cupm, tray):
    esp = over(esp, brush_outline(m, 2.6, nxt(), INK, wobble=0.3, density=0.85))
print("espresso", save_full(esp, f"{OUT}/wish-espresso.webp", (V, V), 84) // 1024, "KB")
# camping tent with a pine
tent = blank(V, V)
ground = shape_mask(V, V, deform(ellipse_pts(60, 96, 50, 7, 12), rng, 2, .05))
tent = over(tent, vpaint(ground, "#bfe3c6", "#a6d3b0", rough=2.5, streak=0.5))
pine = shape_mask(V, V, deform([(96, 92), (84, 92), (90, 76), (86, 76), (92, 62), (89, 62), (96, 44), (103, 62), (100, 62), (106, 76), (102, 76), (108, 92)], rng, 1, .02), smooth=False)
tent = over(tent, vpaint(pine, "#3e9c5a", "#2f7a46", light=(80, 50), k=0.3))
tent = over(tent, brush_outline(pine, 2.4, nxt(), INK, wobble=0.35, density=0.8))
tm = shape_mask(V, V, deform([(14, 94), (52, 30), (90, 94)], rng, 1, .01), smooth=False)
tent = over(tent, vpaint(tm, "#ff7854", "#e85f3c", light=(30, 40), k=0.35))
door = shape_mask(V, V, deform([(38, 94), (52, 56), (66, 94)], rng, 1, .01), smooth=False)
tent = over(tent, vpaint(door, "#fd3a73", "#d92a5f", light=(40, 50), k=0.3))
flap = stroke_mask(V, V, densify([(52, 56), (44, 94)], 2), 2.6, taper=(0.05, 0.05)) * tm
tent = over(tent, tint_layer(flap, "#fff3ee", 0.7))
pole = stroke_mask(V, V, densify([(52, 24), (52, 32)], 2), 2.4, taper=(0.05, 0.05))
tent = over(tent, vpaint(pole, INK))
tent = over(tent, brush_outline(tm, 2.6, nxt(), INK, wobble=0.3, density=0.85))
print("tenda", save_full(tent, f"{OUT}/wish-tenda.webp", (V, V), 84) // 1024, "KB")
sheet([star, bolt, flame, esp, tent], f"{PREV}/kc-stickers.png", bg="#ffffff")
