"""Repositori — painted sponsor-tier badges (enamel-pin gouache heart & sparkles, pressed gold-foil crown).
Run: python3 -I /tmp/pen/art/themes/repositori.py
Paints: pink (#db61a2), blue (#58a6ff), gold foil (#d29922), ink (#0d1117), rim (#e6edf3).
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p6_lib import *

OUT = "/root/w/frontend/public/themes/art/repositori"
os.makedirs(OUT, exist_ok=True)
nxt = Seeds(1400)
S = 96

def pin(layer, mask, col):
    """Enamel-pin edge: a thin lighter rim and a soft drop shadow under the shape."""
    rim = np.clip(gaussian_filter(mask, 2.2) * 2.6, 0, 1)
    sh = np.roll(gaussian_filter(mask, 4), 3, axis=0)
    out = tint_layer(sh, "#000000", 0.35)
    out = over(out, gouache_paint(rim, mix(col, "#ffffff", .55), mix(col, "#ffffff", .35), seed=nxt(), rough=1.0, streak=0.3))
    return over(out, layer)

def heart_pts(cx, cy, s, n=40):
    pts = []
    for i in range(n):
        t = i / (n - 1) * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    return pts

rng = random.Random(3)
# supporter: heart
hm = gaussian_filter(shape_mask(S, S, deform(heart_pts(48, 52, 34), rng, 2, .03)), 0.8)
heart = gouache_paint(hm, "#db61a2", "#b8407f", seed=nxt(), rough=1.8, streak=0.9)
heart = darken(heart, hm, 30, 30, 0.35, radius=S * 0.9)
hi = shape_mask(S, S, deform(ellipse_pts(36, 40, 8, 5, 10, -0.5), rng, 2, .1)) * hm
heart = over(heart, tint_layer(gaussian_filter(hi, 1.4), "#ffd3ea", 0.6))
heart = over(heart, brush_outline(hm, 2.4, nxt(), "#5a1b40", wobble=0.3, density=0.8))
heart = pin(heart, hm, "#db61a2")

# backer: three sparkles
def spark(cx, cy, r):
    pts = []
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.3
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts
sm = np.zeros((S, S), np.float32)
for (cx, cy, r) in [(42, 52, 32), (74, 30, 13), (72, 72, 9)]:
    sm = np.maximum(sm, shape_mask(S, S, deform(spark(cx, cy, r), rng, 1, .02), smooth=True))
sm = gaussian_filter(sm, 0.7)
sp = gouache_paint(sm, "#58a6ff", "#2f7fe0", seed=nxt(), rough=1.4, streak=0.8)
sp = darken(sp, sm, 30, 30, 0.3, radius=S * 0.9)
sp = over(sp, tint_layer(gaussian_filter(circ(S, S, 40, 48, 7) * sm, 2), "#d8ecff", 0.7))
sp = over(sp, brush_outline(sm, 2.2, nxt(), "#163a6b", wobble=0.3, density=0.8))
sp = pin(sp, sm, "#58a6ff")

# gold: crown as pressed foil
def crown_path(p):
    p.moveTo(18, 70); p.lineTo(14, 32); p.lineTo(34, 48); p.lineTo(48, 20); p.lineTo(62, 48); p.lineTo(82, 32); p.lineTo(78, 70); p.close()
cm = gaussian_filter(path_mask(S, S, crown_path), 0.6)
band = rrect(S, S, 18, 70, 60, 10, 2)
cm = np.maximum(cm, band)
cm = displace(cm, nxt(), 1.5, 20)
crown = foil(cm, "#d29922", seed=nxt(), emboss=0.8, sparkle=0.3)
# jewels
jew = blank(S, S)
for (x, y, c) in [(48, 64, "#db61a2"), (30, 62, "#58a6ff"), (66, 62, "#58a6ff")]:
    m = circ(S, S, x, y, 4)
    jew = over(jew, gouache_paint(m, c, mix(c, "#000000", .2), seed=nxt(), rough=0.6))
    jew = over(jew, tint_layer(circ(S, S, x - 1.2, y - 1.2, 1.3), "#ffffff", 0.8))
crown = over(crown, jew)
# tips
for (x, y) in [(14, 32), (48, 20), (82, 32)]:
    crown = over(crown, foil(circ(S, S, x, y, 4.5), "#e8b53a", seed=nxt(), emboss=0.8))
sh = np.roll(gaussian_filter(cm, 4), 3, axis=0)
crown = over(tint_layer(sh, "#000000", 0.4), crown)

for name, arr in [("supporter", heart), ("backer", sp), ("gold", crown)]:
    print(name, save_full(arr, f"{OUT}/tier-{name}.webp", (S, S), 84) // 1024, "KB")
sheet([heart, sp, crown], f"{PREV}/rp-tiers.png", bg="#161b22")
