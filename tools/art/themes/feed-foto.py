"""Feed Foto — gouache wishlist product vignettes (vintage lamp, ceramic vase, rattan chair) with a thin ink line.
Run: python3 -I /tmp/pen/art/themes/feed-foto.py
Paints: brass (#c99a4a), terracotta (#c9775a), sage (#9db38f), cream (#f1e6d2), rattan (#d8a86a), ink (#4a3d33).
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p6_lib import *

OUT = "/root/w/frontend/public/themes/art/feed-foto"
os.makedirs(OUT, exist_ok=True)
nxt = Seeds(500)
INK = "#4a3d33"
W, H = 228, 120  # 2x of the 114x60 product image box

def outline(m, w=3.2, wob=0.3):
    return brush_outline(m, w, nxt(), INK, "#5b4c40", wobble=wob, density=0.85)

def paint(m, c, c2=None, light=None, k=0.22, rough=2.0, streak=0.8):
    g = gouache_paint(m, c, c2 or mix(c, "#000000", .08), seed=nxt(), rough=rough, streak=streak)
    if light:
        g = darken(g, m, light[0], light[1], k, radius=max(W, H) * 0.9)
    return g

def shadow(m, dy=6, blur=5, a=0.22):
    sh = np.roll(gaussian_filter(m, blur), dy, axis=0)
    return tint_layer(sh, "#6b5a4a", a)

# ---------------------------------------------------------------- lamp (banker's / vintage desk lamp)
rng = random.Random(1)
lamp = blank(W, H)
base = shape_mask(W, H, deform(ellipse_pts(112, 104, 44, 9, 12), rng, 2, .05))
stem = path_mask(W, H, lambda p: (p.moveTo(112, 100), p.cubicTo(112, 70, 108, 60, 110, 44)), stroke=7)
arm = path_mask(W, H, lambda p: (p.moveTo(110, 46), p.cubicTo(118, 30, 134, 26, 150, 30)), stroke=6)
shade_m = poly(W, H, [(96, 28), (190, 28), (176, 62), (112, 62)], rng, .01)
shade_m = gaussian_filter(shade_m, 0.8)
lamp = over(lamp, shadow(np.maximum(base, shade_m)))
lamp = over(lamp, paint(base, "#5a4a3d", "#3f3129", light=(80, 60)))
lamp = over(lamp, paint(stem, "#c99a4a", "#a87d33", light=(80, 40), k=0.3))
lamp = over(lamp, paint(arm, "#c99a4a", "#a87d33", light=(80, 40), k=0.3))
lamp = over(lamp, outline(np.maximum(stem, arm), 2.6))
lamp = over(lamp, paint(shade_m, "#3d6b5a", "#2d5245", light=(120, 10), k=0.35))
# warm light pool under the shade + highlight band on the shade
pool = shape_mask(W, H, deform(ellipse_pts(150, 70, 36, 14, 12), rng, 2, .2))
lamp = over(lamp, tint_layer(gaussian_filter(pool, 6), "#ffd98a", 0.35))
hi = stroke_mask(W, H, densify([(108, 36), (168, 36)], 3), 5, taper=(0.2, 0.3)) * shade_m
lamp = over(lamp, tint_layer(hi, "#8fc3ad", 0.5))
rim = stroke_mask(W, H, densify([(114, 60), (175, 60)], 3), 3, taper=(0.1, 0.1))
lamp = over(lamp, paint(rim, "#c99a4a", "#a87d33"))
knob = circ(W, H, 112, 92, 5)
lamp = over(lamp, paint(knob, "#c99a4a"))
for m in (base, shade_m):
    lamp = over(lamp, outline(m))
print("lamp", save_full(lamp, f"{OUT}/lampu.webp", (W, H), 84) // 1024, "KB")

# ---------------------------------------------------------------- ceramic vase with a eucalyptus sprig
rng = random.Random(2)
vase = blank(W, H)
def vase_path(p):
    p.moveTo(84, 116); p.cubicTo(70, 104, 66, 82, 80, 66); p.cubicTo(92, 54, 92, 48, 90, 40)
    p.lineTo(134, 40); p.cubicTo(132, 48, 132, 54, 144, 66); p.cubicTo(158, 82, 154, 104, 140, 116); p.close()
vm = path_mask(W, H, vase_path)
vase = over(vase, shadow(vm))
vase = over(vase, paint(vm, "#d98a6a", "#c3704f", light=(70, 40), k=0.32))
# glaze band + speckle
band = rrect(W, H, 60, 84, 110, 14, 3) * vm
vase = over(vase, paint(band, "#f1e6d2", "#e7d9bf", light=(70, 40), k=0.2))
hi = stroke_mask(W, H, curve([(94, 56), (90, 76), (92, 102)], 20), 5, taper=(0.3, 0.3)) * vm
vase = over(vase, tint_layer(gaussian_filter(hi, 1.2), "#ffd9c5", 0.5))
speck = (np.random.default_rng(3).random((H, W)) > 0.993).astype(np.float32) * vm
vase = over(vase, tint_layer(speck, "#7a4a35", 0.5))
neck = rrect(W, H, 88, 36, 48, 8, 2)
vase = over(vase, paint(neck, "#c3704f", "#a85c3f"))
# sprig
stem = curve([(112, 40), (118, 22), (130, 6)], 20)
sprig = blank(W, H)
sm = stroke_mask(W, H, stem, 2.6, taper=(0.02, 0.2))
sprig = over(sprig, paint(sm, "#6f8a63"))
for i in range(6):
    t = 0.15 + i * 0.15
    bx, by = stem[min(19, int(t * 19))]
    side = -1 if i % 2 else 1
    lm = shape_mask(W, H, deform(ellipse_pts(bx + side * 8, by - 1, 7.5, 5.5, 10, side * 0.3), rng, 2, .08))
    sprig = over(sprig, paint(lm, "#9db38f", "#86a078", light=(60, 0), k=0.25))
    sprig = over(sprig, outline(lm, 2.4, 0.4))
vase = over(vase, sprig)
vase = over(vase, outline(vm))
print("vase", save_full(vase, f"{OUT}/vas.webp", (W, H), 84) // 1024, "KB")

# ---------------------------------------------------------------- rattan chair (peacock-ish round back)
rng = random.Random(3)
chair = blank(W, H)
back = shape_mask(W, H, deform(ellipse_pts(114, 50, 48, 40, 14), rng, 2, .04))
seat = poly(W, H, [(72, 80), (156, 80), (164, 100), (64, 100)], rng, .01)
legs = np.zeros((H, W), np.float32)
for (x0, x1) in [(72, 66), (156, 162), (96, 94), (132, 134)]:
    legs = np.maximum(legs, stroke_mask(W, H, densify([(x0, 98), (x1, 118)], 3), 4.5, taper=(0.02, 0.02)))
chair = over(chair, shadow(np.maximum(back, seat)))
chair = over(chair, paint(back, "#d8a86a", "#c2904f", light=(80, 20), k=0.3))
# weave: crosshatch lines knocked slightly darker inside the back
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
weave = ((np.sin((xx + yy) * 0.9) > 0.75) | (np.sin((xx - yy) * 0.9) > 0.75)).astype(np.float32) * back
weave = gaussian_filter(weave, 0.5)
chair = over(chair, tint_layer(weave, "#8a5f2c", 0.35))
inner = shape_mask(W, H, deform(ellipse_pts(114, 54, 32, 26, 14), rng, 2, .04))
chair = over(chair, paint(inner, "#e6c08a", "#d9ae70", light=(80, 20), k=0.25, streak=1.2))
cushion = rrect(W, H, 78, 72, 72, 16, 7)
chair = over(chair, paint(seat, "#d8a86a", "#c2904f", light=(80, 20), k=0.3))
chair = over(chair, paint(cushion, "#f1e6d2", "#e3d4b8", light=(80, 40), k=0.2))
chair = over(chair, paint(legs, "#b8853f", "#9c6d2e"))
# radial canes in the back
for k in range(7):
    a = math.pi + k * math.pi / 6
    pts = densify([(114, 78), (114 + math.cos(a) * 44, 52 + math.sin(a) * 36)], 3)
    cm = stroke_mask(W, H, pts, 2.2, taper=(0.05, 0.1)) * back
    chair = over(chair, tint_layer(cm, "#8a5f2c", 0.45))
for m in (back, seat, cushion):
    chair = over(chair, outline(m, 3.0))
chair = over(chair, outline(legs, 2.2))
print("chair", save_full(chair, f"{OUT}/kursi.webp", (W, H), 84) // 1024, "KB")

sheet([lamp, vase, chair], f"{PREV}/ff-products.png", bg="#fafafa")
