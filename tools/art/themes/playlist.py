"""Playlist — painted merch (vinyl player, smart speaker, acoustic guitar) in gouache + ink for the dark chips,
and a gouache colour-field backdrop for the "Wrapped" card (brush streaks instead of a CSS gradient).
Run: python3 -I /tmp/pen/art/themes/playlist.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p5_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/playlist"
PRE = "/tmp/pen/nt3-P5/playlist"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(55)
INK, GREEN, GREEN2, CREAM, CREAM2, WOOD, WOOD2, DARK, DARK2, GREY = "#101010", "#1ed760", "#169c44", "#f4efe6", "#e2dacc", "#c99467", "#9d6a3f", "#4a4648", "#2d2a2c", "#8f8a8c"

def vinyl(W, H):
    cx, cy = W / 2, H / 2 + 4
    art = blank(W, H)
    plinth = rr(cx - 84, cy - 54, 168, 108, 12)
    art = over(art, shadow(W, H, plinth, "#000000", (5, 8), 9, 0.5))
    art = over(art, paint(fill_mask(W, H, plinth), CREAM, CREAM2))
    art = shade(art, W, H, rr(cx - 84, cy + 12, 168, 42, 10), "#9a8e7c", 0.3, 10)
    art = over(art, paint(fill_mask(W, H, circ(cx - 16, cy, 46)), DARK, DARK2))
    art = over(art, paint(fill_mask(W, H, circ(cx - 16, cy, 42)), "#161416", "#262326"))
    for r in (35, 28, 21):
        art = over(art, ink(W, H, circ(cx - 16, cy, r), 1.2, "#3c383b", 0.35))
    art = over(art, paint(fill_mask(W, H, circ(cx - 16, cy, 13)), GREEN, GREEN2))
    art = over(art, paint(fill_mask(W, H, circ(cx - 16, cy, 2.5)), CREAM))
    arm = poly([(cx + 60, cy - 38), (cx + 6, cy - 4)], False)
    art = over(art, paint(fill_mask(W, H, circ(cx + 60, cy - 38, 9)), GREY, "#5f5c58"))
    art = over(art, ink(W, H, arm, 5.0, "#bdb8ba", 0.0, 1.2))
    art = over(art, ink(W, H, arm, 1.6, INK, 0.1, 1.2))
    art = over(art, paint(fill_mask(W, H, rr(cx - 2, cy - 10, 16, 10, 3)), DARK, DARK2))
    art = over(art, paint(fill_mask(W, H, circ(cx + 62, cy + 30, 7)), GREEN, GREEN2))
    art = over(art, ink(W, H, plinth, 2.6, INK, 0.2))
    art = over(art, ink(W, H, circ(cx - 16, cy, 46), 2.0, INK, 0.2))
    art = over(art, highlight(W, H, poly([(cx - 70, cy - 44), (cx + 50, cy - 46)], False), 0.5))
    return grain(art, nxt(), 0.04)

def smart_speaker(W, H):
    cx, base = W / 2, H - 14
    art = blank(W, H)
    body = rr(cx - 42, base - 128, 84, 128, 34)
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.5))
    art = over(art, paint(fill_mask(W, H, body), CREAM, CREAM2))
    art = shade(art, W, H, rr(cx + 2, base - 128, 40, 128, 26), "#9a8e7c", 0.3, 10)
    def mesh(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for j in range(9):
            for i in range(-3, 4):
                cv.c.drawCircle(cx + i * 10 + (j % 2) * 5, base - 96 + j * 10, 1.5, p)
    art = over(art, paint(mask_from(W, H, mesh), "#8f877c", "#6f685f", rough=0.8, density=0.85))
    top = oval(cx, base - 128, 42, 12)
    art = over(art, paint(fill_mask(W, H, top), DARK, DARK2))
    # glowing light ring on top
    ring = skia.Path(); ring.addOval(skia.Rect.MakeLTRB(cx - 28, base - 134, cx + 28, base - 122))
    rm = stroke_m(W, H, ring, 4)
    art = over(art, glow(rm, GREEN, 5, 0.9))
    art = over(art, paint(rm, GREEN, "#7ff0a6", rough=0.8))
    art = over(art, ink(W, H, body, 2.6, INK, 0.2))
    for k in range(2):
        pts = arc_pts(cx + 64, base - 70, 14 + k * 10, -math.pi * 0.28, math.pi * 0.28, 16)
        art = over(art, ink(W, H, poly(pts, False), 2.4, GREEN, 0.12))
    art = over(art, highlight(W, H, poly([(cx - 30, base - 110), (cx - 30, base - 40)], False), 0.5))
    return grain(art, nxt(), 0.04)

def guitar(W, H):
    cx, cy = W / 2 + 10, H / 2 + 14
    art = blank(W, H)
    # body: two lobes (figure 8), slightly tilted
    lower = oval(cx, cy + 14, 52, 46)
    upper = oval(cx, cy - 30, 40, 34)
    body = skia.Path(); body.addPath(lower); body.addPath(upper)
    bm = np.maximum(fill_mask(W, H, lower), fill_mask(W, H, upper))
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.5))
    art = over(art, paint(bm, WOOD, WOOD2))
    art = shade(art, W, H, oval(cx + 20, cy + 20, 50, 60), "#5a3a1c", 0.3, 12)
    art = over(art, paint(fill_mask(W, H, circ(cx, cy - 4, 15)), "#1b1618", "#2a2325"))
    art = over(art, ink(W, H, circ(cx, cy - 4, 18), 2.0, "#6a4a2a", 0.3))
    bridge = rr(cx - 18, cy + 22, 36, 7, 3)
    art = over(art, paint(fill_mask(W, H, bridge), "#2a2325", "#1b1618"))
    # neck + head
    neck = poly(wobbly([(cx - 8, cy - 60), (cx + 8, cy - 60), (cx + 8, cy - 150), (cx - 8, cy - 150)], rng, 0.01))
    art = over(art, paint(fill_mask(W, H, neck), "#3b2c22", "#2a1f18"))
    head = rr(cx - 11, cy - 178, 22, 34, 5)
    art = over(art, paint(fill_mask(W, H, head), WOOD2, "#7a5230"))
    for i in range(3):
        for sx in (-1, 1):
            art = over(art, paint(fill_mask(W, H, circ(cx + sx * 14, cy - 170 + i * 10, 2.6)), GREY, "#d8d4d2"))
    # frets + strings
    for i in range(7):
        y = cy - 66 - i * 12
        art = over(art, ink(W, H, poly([(cx - 8, y), (cx + 8, y)], False), 1.2, "#bdb8ba", 0.2, 0.6))
    for i in range(4):
        x = cx - 6 + i * 4
        art = over(art, ink(W, H, poly([(x, cy - 170), (x, cy + 24)], False), 0.9, "#e8e3dc", 0.15, 0.5))
    art = over(art, ink_mask(bm, 2.6, INK, 0.2))
    art = over(art, ink(W, H, neck, 2.0, INK, 0.2))
    art = over(art, ink(W, H, head, 2.0, INK, 0.2))
    art = over(art, highlight(W, H, poly(arc_pts(cx, cy + 14, 44, math.pi * 1.1, math.pi * 1.45, 10), False), 0.45))
    return grain(art, nxt(), 0.04)

def wrapped(W, H):
    """Gouache colour field: green → violet with big horizontal brush strokes and a few poster-paint blobs."""
    art = painted_sky(W, H, [(0, "#1db954"), (1, "#1db954")], seed=nxt(), streak=1.0, grain=0.8)
    # rotate the gradient idea: build horizontal blend by hand
    t = np.linspace(0, 1, W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    t = np.clip(t + (fbm(W, H, nxt(), 120, 3) - 0.5) * 0.25, 0, 1)
    stops = [(0.0, "#1db954"), (0.42, "#2fa36b"), (0.66, "#6a41d6"), (1.0, "#7c3aed")]
    rgb = np.zeros((H, W, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        k = np.clip((t - t0) / (t1 - t0), 0, 1)[..., None]
        sel = (t >= t0) & (t <= t1)
        ca = np.array(hex_rgb(c0), np.float32); cb = np.array(hex_rgb(c1), np.float32)
        rgb[sel] = (ca * (1 - k) + cb * k)[sel]
    art[..., :3] = rgb
    # brush streaks (long horizontal strokes of slightly lighter/darker paint)
    for _ in range(70):
        y = rng.uniform(0, H); x0 = rng.uniform(-50, W * 0.7); L = rng.uniform(W * 0.15, W * 0.6)
        pts = [(x0 + L * k / 8, y + rng.gauss(0, 1.5)) for k in range(9)]
        m = stroke_mask(W, H, pts, rng.uniform(3, 9), taper=(0.25, 0.35))
        col = "#ffffff" if rng.random() < 0.55 else "#000000"
        layer = gouache_paint(m, col, seed=nxt(), rough=2, streak=0.6, density=rng.uniform(0.04, 0.09))
        art = over(art, layer)
    g = gaussian_filter(np.random.default_rng(nxt()).random((H, W)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    art[..., :3] = np.clip(art[..., :3] * (1 + g[..., None] * 0.035), 0, 1)
    return art

def save(arr, name, max_w, tone="#2a2a2a", q=82):
    size = save_asset(arr, f"{OUT}/{name}.webp", max_w=max_w, quality=q)
    preview(arr, f"{PRE}/{name}.png", tone)
    print(name, size, "%.1f KB" % kb(f"{OUT}/{name}.webp"))

save(vinyl(220, 160), "merch-vinyl", 150)
save(smart_speaker(200, 190), "merch-speaker", 130)
save(guitar(190, 230), "merch-guitar", 110)
save(wrapped(880, 440), "wrapped", 880, "#1db954", 76)
