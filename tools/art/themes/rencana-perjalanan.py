"""Rencana Perjalanan — painted travel pieces for the itinerary-app theme: a watercolour island route map
(sea wash, island, volcano, dashed ink route, gouache pins), worn passport stamps, a gouache airliner for
the header, a watercolour sunset-coast scene used when no cover photo exists, and a faint paper grain.
Run: python3 -I /tmp/pen/art/themes/rencana-perjalanan.py [map stamps plane scene paper]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _r2_lib import *  # noqa

T = "rencana-perjalanan"
D = outdir(T)
nxt = Seeds(3100)
rng = random.Random(57)
SKY, NAVY, ORANGE = "#0194f3", "#0b55a5", "#ff5e1f"


def pin(W, H, x, y, r, col, nxt):
    pts = [(x + math.cos(a) * r, y - r * 1.25 + math.sin(a) * r) for a in np.linspace(math.pi * 0.8, math.pi * 2.2, 18)] + [(x, y)]
    m = shape_mask(W, H, pts)
    art = gouache_obj(m, col, mix(col, "#7a1d00", .3), seed=nxt(), light=(-0.6, -0.8), k=0.3, blur=3)
    art = over(art, gouache_paint(dots_mask(W, H, [(x, y - r * 1.25, r * 0.38)]), "#fff8ef", seed=nxt(), rough=0.4, streak=0))
    return over(art, ink_outline(m, "#5a2410", nxt(), width=1.4, density=0.5, breaks=0.2))


def island_map():
    W, H = 780, 280
    art = blank(W, H)
    vign = shape_mask(W, H, deform(ellipse_pts(390, 140, 380, 136, 16), rng, 3, 0.05))
    art = glaze(art, pigment(vign, "#cbeaf8", "#a9dcf3", seed=nxt(), density=0.75, edge=0.55, bloom=0.5, rough=12, feather=4, gran=0.3))
    # shallow water ring + island body
    body = [(150, 112), (200, 92), (250, 96), (330, 70), (430, 60), (530, 74), (610, 96), (652, 130), (620, 160), (560, 182), (548, 206), (566, 230), (530, 236), (500, 214), (420, 208), (350, 214), (290, 196), (240, 176), (186, 156)]
    shallow = shape_mask(W, H, deform([((x - 390) * 1.08 + 390, (y - 140) * 1.16 + 140) for x, y in body], rng, 3, 0.03))
    art = glaze(art, pigment(shallow, "#8fd6e3", "#b8ece8", seed=nxt(), density=0.55, edge=0.4, bloom=0.4, rough=8, feather=3, gran=0.2))
    isl = shape_mask(W, H, deform(body, rng, 3, 0.035))
    art = glaze(art, pigment(isl, "#f2dfae", "#ead09a", seed=nxt(), density=0.9, edge=0.4, bloom=0.2, rough=5, feather=1.4, gran=0.3))
    inner = shape_mask(W, H, deform([((x - 400) * 0.88 + 400, (y - 138) * 0.8 + 138) for x, y in body], rng, 3, 0.04))
    art = glaze(art, pigment(inner, "#9cce8a", "#6ead6a", seed=nxt(), density=0.85, edge=0.55, bloom=0.45, rough=7, feather=2, gran=0.35))
    # volcano + rice-terrace hatching
    vol = shape_mask(W, H, deform([(420, 118), (452, 92), (470, 76), (484, 76), (504, 94), (536, 120), (480, 126)], rng, 2, 0.03))
    art = glaze(art, pigment(vol, "#8c8a62", "#6d6a48", seed=nxt(), density=0.6, edge=0.6, bloom=0.3, rough=4, feather=1.5, gran=0.4))
    lit = shape_mask(W, H, deform([(470, 78), (484, 78), (512, 108), (494, 114)], rng, 2, 0.04))
    art = glaze(art, pigment(lit, "#5f5a3c", seed=nxt(), density=0.4, edge=0.4, bloom=0.2, rough=3, feather=1.5))
    for dx in (-30, -12, 8, 26):
        art = over(art, ink(stroke_mask(W, H, curve([(477, 80), (477 + dx * 0.5, 100), (477 + dx, 120)], 16), 1.0, (0.1, 0.4)), "#4a4430", nxt(), density=0.4))
    for k in range(6):
        y = 150 + k * 8
        art = over(art, ink(stroke_mask(W, H, curve([(300 + k * 6, y), (340, y - 4), (380 - k * 4, y + 1)], 20), 1.2, (0.2, 0.2)), "#4c7f45", nxt(), density=0.45))
    # little gouache palms along the south coast
    for px in (300, 560):
        a, _ = palm(W, H, px, 196 if px < 400 else 182, 34, 0.15 if px < 400 else -0.15, rng, nxt, trunk="#7a5a3c", leaf=("#3f8a5a", "#2f6e48"), fronds=6)
        art = over(art, a)
    # dashed ink route: airport (left) → venue (right)
    route = curve([(200, 150), (270, 120), (360, 176), (450, 160), (540, 132), (586, 150)], 120)
    dash = np.zeros((H, W), np.float32)
    for i in range(0, len(route) - 3, 6):
        dash = np.maximum(dash, stroke_mask(W, H, route[i:i + 4], 3.2, (0.2, 0.2)))
    art = over(art, pigment(dash, ORANGE, "#e2471a", seed=nxt(), density=0.95, edge=0.35, bloom=0, rough=1.0, feather=0.5, gran=0.2))
    art = over(art, pin(W, H, 200, 152, 14, NAVY, nxt))
    art = over(art, pin(W, H, 586, 152, 18, ORANGE, nxt))
    # compass rose (ink) top right, sailboat bottom left
    cx, cy = 690, 70
    rose = shape_mask(W, H, [(cx, cy - 26), (cx + 6, cy), (cx, cy + 26), (cx - 6, cy)], smooth=False)
    rose = np.maximum(rose, shape_mask(W, H, [(cx - 22, cy), (cx, cy - 5), (cx + 22, cy), (cx, cy + 5)], smooth=False))
    art = over(art, ink(rose, "#20486e", nxt(), density=0.7))
    art = over(art, ink(ring_mask(W, H, cx, cy, 15, 1.4, rng, 0.3), "#20486e", nxt(), density=0.5))
    art = over(art, ink(text_mask(W, H, "U", cx, cy - 32, 14, "bebas"), "#20486e", nxt(), density=0.8))
    hull = shape_mask(W, H, [(96, 196), (130, 196), (124, 203), (102, 203)], smooth=False)
    art = over(art, gouache_paint(hull, "#7a4b2c", seed=nxt(), rough=0.6))
    art = over(art, gouache_obj(shape_mask(W, H, [(114, 194), (114, 164), (132, 192)], smooth=False), "#fff8ec", seed=nxt(), k=0.2, blur=2))
    for k in range(3):
        y = 214 + k * 6
        art = over(art, ink(stroke_mask(W, H, [(80 + k * 10, y), (110, y - 2), (146 - k * 6, y)], 1.0, (0.3, 0.3)), "#3c86b8", nxt(), density=0.45))
    preview(art, f"{PREV}/rp-map.png", "#ffffff")
    save(art, f"{D}/map.webp", max_w=720, q=80)


def stamps():
    W, H = 340, 260
    art = postmark(W, H, 112, 140, 92, "DENPASAR · ARRIVAL", "VISA SEUMUR HIDUP", "DPS", rng, nxt, col=NAVY, wear=0.5, rot=-0.22, center_size=40, date="11.09.27")
    # rectangular entry stamp, overlapping
    rect = rrect_mask(W, H, 172, 70, 150, 84, 10, rot=0.2, stroke=5)
    rect = np.maximum(rect, rrect_mask(W, H, 180, 78, 134, 68, 7, rot=0.2, stroke=1.8))
    rect = np.maximum(rect, text_mask(W, H, "PELAMINAN", 247, 113, 30, "bebas", 1.5, rot=0.2))
    rect = np.maximum(rect, text_mask(W, H, "ENTRY · 1 RUTE", 241, 136, 15, "mono", 0, rot=0.2))
    art = over(art, rubber_stamp(rect, ORANGE, nxt(), wear=0.45))
    preview(art, f"{PREV}/rp-stamps.png", "#ffffff")
    save(art, f"{D}/stamps.webp", max_w=240, q=80)


def plane():
    W, H = 420, 240
    parts = airliner_parts(W, H, 210, 120, 330, rng, bank=-0.1)
    a, _ = paint_airliner(W, H, parts, rng, nxt, body="#f7f6f1", body2="#dfe5ec", navy=NAVY, accent=ORANGE, ink_col="#123a66")
    preview(a, f"{PREV}/rp-plane.png", SKY)
    save(a, f"{D}/plane.webp", max_w=220, q=84)


def scene():
    """Watercolour sunset coast with limestone cliffs — shown when the invitation has no cover photo."""
    W, H = 780, 660
    art = painted_sky(W, H, [(0, "#2a6fb8"), (0.25, "#5f8fcf"), (0.45, "#f2a77a"), (0.56, "#ffd39a"), (1, "#ffd39a")], seed=nxt(), streak=0.8, grain=0.6)
    art = over(art, glow(dots_mask(W, H, [(520, 360, 40)]), "#ffe3a8", radius=60, strength=0.6))
    art = over(art, gouache_paint(dots_mask(W, H, [(520, 362, 34)]), "#fff1cc", "#ffe0a0", seed=nxt(), rough=1.5, streak=0.3))
    for cx, cy, rx, ry, col in [(200, 170, 260, 24, "#f7c3a8"), (600, 230, 220, 18, "#ffcfae"), (300, 290, 200, 14, "#ffd8b5")]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.45)
        art = glaze(art, pigment(m, col, "#fff0e0", seed=nxt(), density=0.5, edge=0.35, bloom=0.5, rough=9, feather=3, gran=0.15))
    sea = shape_mask(W, H, [(-20, 380), (W + 20, 380), (W + 20, H + 20), (-20, H + 20)], smooth=False)
    art = over(art, gouache_paint(sea, "#2f86b5", "#3aa6c4", seed=nxt(), rough=1.0, streak=0.9))
    art = glaze(art, pigment(shape_mask(W, H, [(-20, 470), (W + 20, 440), (W + 20, H + 20), (-20, H + 20)], smooth=False), "#57c3c7", "#7fd6cf", seed=nxt(), density=0.5, edge=0.2, bloom=0.4, rough=10, feather=5))
    gl = np.zeros((H, W), np.float32)
    for _ in range(60):
        y = rng.uniform(386, 470); x = 520 + rng.gauss(0, 40 + (y - 380) * 1.2); L = rng.uniform(10, 30)
        gl = np.maximum(gl, stroke_mask(W, H, [(x - L / 2, y), (x + L / 2, y)], rng.uniform(1.4, 2.6), (0.3, 0.3)))
    art = over(art, gouache_paint(gl, "#fff2cf", seed=nxt(), rough=0.6, streak=0, density=0.75))
    # cliffs on the left, layered, with green tops
    for i, (x1, top, col, gr) in enumerate([(300, 300, "#b98b6a", "#5f9a5c"), (420, 360, "#a1765a", "#4f8a4f")]):
        pts = [(-20, top), (x1 * 0.5, top - 14), (x1 * 0.85, top + 8), (x1, top + 60), (x1 + 20, H + 20), (-20, H + 20)]
        cm = shape_mask(W, H, deform(pts, rng, 3, 0.02), smooth=False)
        art = over(art, gouache_obj(cm, col, mix(col, "#4a2f22", .35), seed=nxt(), light=(1, -0.3), k=0.35, blur=14, lo="#3a241a"))
        topm = shape_mask(W, H, deform([(-20, top - 18), (x1 * 0.5, top - 30), (x1 * 0.86, top - 4), (x1 * 0.9, top + 16), (x1 * 0.5, top + 10), (-20, top + 14)], rng, 3, 0.04))
        for k in range(7):
            sy = top + 40 + k * 34 + rng.uniform(-6, 6)
            sm = stroke_mask(W, H, curve([(-20, sy), (x1 * 0.45, sy - 6 + rng.uniform(-4, 4)), (x1 * 0.95, sy + 10)], 30), rng.uniform(1.5, 3), (0.1, 0.3)) * cm
            art = over(art, gouache_paint(sm, mix(col, "#3a241a", .45), seed=nxt(), rough=1.2, streak=0, density=0.55))
        art = over(art, gouache_obj(topm, gr, mix(gr, "#1f4a2a", .3), seed=nxt(), light=(0.5, -1), k=0.3, blur=6))
    preview(art, f"{PREV}/rp-scene.png")
    save(art, f"{D}/scene.webp", q=76, trim=False)


def paper_tex():
    t = grain_overlay(256, "#0b4a7a", seed=31, base=0.004, k=0.8, cap=0.035, fiber=0.4, mottle=0.8)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["map", "stamps", "plane", "scene", "paper"]
    for w in which:
        {"map": island_map, "stamps": stamps, "plane": plane, "scene": scene, "paper": paper_tex}[w]()
