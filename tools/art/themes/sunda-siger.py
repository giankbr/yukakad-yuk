"""Sunda Siger — painted assets: gold-foil siger crown, gouache Mega Mendung clouds (dark + light),
gouache roncean melati strand, melati bloom, foil divider.
Run: python3 -I /tmp/pen/art/themes/sunda-siger.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentF_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/sunda-siger"
PRE = "/tmp/pen/nt2-F/art"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(11)
seed = [300]
def nxt():
    seed[0] += 13
    return seed[0]

GOLD = "#c9a54e"; GOLD_DEEP = "#7a5a1a"; GREEN = "#1d4a33"; IVORY = "#fffaf0"


def melati_layer(W, H, cx, cy, r, rot=0.0, petals=5, col=IVORY, shade="#d8cfb2", centre="#d9bf64"):
    """Gouache jasmine: five rounded petals, a shadow glaze toward the lower right, a yellow heart."""
    art = blank(W, H)
    pm_all = np.zeros((H, W), np.float32)
    for k in range(petals):
        a = rot + k * math.tau / petals + rng.uniform(-.12, .12)
        L = r * rng.uniform(.92, 1.06)
        pc = (cx + math.cos(a) * L * .52, cy + math.sin(a) * L * .52)
        pts = deform(ellipse_pts(pc[0], pc[1], L * .52, L * .36, 12, a), rng, 1, .04)
        m = shape_mask(W, H, pts)
        pm_all = np.maximum(pm_all, m)
        art = over(art, gouache_paint(m, col, mix(col, "#efe6cf", .5), seed=nxt(), rough=max(1.0, r * .04), streak=.25))
        # petal crease / shadow side (light from upper-left)
        half = shape_mask(W, H, ellipse_pts(cx + math.cos(a + .35) * L * .45, cy + math.sin(a + .35) * L * .45, L * .32, L * .14, 10, a + .35))
        art = glaze(art, pigment(half * m, shade, seed=nxt(), density=.26, edge=.2, bloom=0, gran=.1, rough=1, feather=max(.8, r * .05)))
    heart = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * .2, r * .18, 8), rng, 1, .1))
    art = over(art, gouache_paint(heart, centre, "#b39a3e", seed=nxt(), rough=1))
    # soft cast shadow so the white bloom still reads on cream paper
    art = over(shadow(pm_all, max(1, int(r * .06)), max(1, int(r * .1)), max(1.2, r * .12), .32, "#3d4a2e"), art)
    return art, pm_all


# ---------------- siger crown ----------------
def siger():
    S = 2.6; W, H = int(210 * S), int(124 * S); ox, oy = 5 * S, 6 * S
    P = lambda d: svg_path(d, S, ox, oy)
    art = blank(W, H)
    # kembang goyang pins (behind the crown): wire stems + small gold blooms
    pins = [(100, 24, 100, 4, 7.5), (79, 31, 70, 11, 6.4), (121, 31, 130, 11, 6.4), (58, 46, 44, 28, 5.8), (142, 46, 156, 28, 5.8)]
    for (x0, y0, x1, y1, r) in pins:
        wire = [(ox + (x0 + (x1 - x0) * t) * S + math.sin(t * 3) * 1.2, oy + (y0 + (y1 - y0) * t) * S) for t in np.linspace(0, 1, 14)]
        art = over(art, linocut(stroke_mask(W, H, wire, 1.6 * S, (0.05, 0.05)), "#8d6c22", seed=nxt(), wear=.1, rough=.8))
        bm = np.zeros((H, W), np.float32)
        a0 = rng.uniform(0, 1)
        for k in range(5):
            a = a0 + k * math.tau / 5
            px, py = ox + x1 * S + math.cos(a) * r * S * .5, oy + y1 * S + math.sin(a) * r * S * .5
            bm = np.maximum(bm, shape_mask(W, H, ellipse_pts(px, py, r * S * .5, r * S * .36, 10, a)))
        art = over(art, shadow(bm, 2, 3, 3, .25, "#0b1f15"))
        art = over(art, foil(displace(bm, nxt(), 1.6, 14), GOLD, seed=nxt(), emboss=.8, sparkle=.02))
        art = over(art, gouache_paint(circles_mask(W, H, [(ox + x1 * S, oy + y1 * S, r * S * .3)]), GREEN, "#2f6b4c", seed=nxt(), rough=1))
    body_d = "M24 101C32 62 63 35 100 22c37 13 68 40 76 79-44-15-108-15-152 0Z"
    band_d = "M20 101c46-16 114-16 160 0l-2 10c-45-14-111-14-156 0Z"
    body = displace(path_mask(W, H, P(body_d)), nxt(), 2.2, 22)
    band = displace(path_mask(W, H, P(band_d)), nxt(), 2.0, 22)
    art = over(art, shadow(np.maximum(body, band), 3, 7, 7, .35, "#06140d"))
    art = over(art, foil(body, GOLD, seed=nxt(), emboss=.7, sparkle=.03))
    # a thin warm glaze so the foil reads as hand-burnished, darker at the base
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = glaze(art, pigment(body * np.clip((yy - .35) * 1.4, 0, 1), "#a07c2c", seed=nxt(), density=.35, edge=.1, bloom=.3, gran=.4, rough=2, feather=2))
    # carved concentric arches (engraved, linocut ink)
    for d, wd in [("M40 95c9-28 31-49 60-60 29 11 51 32 60 60", 1.5), ("M58 91c8-19 23-33 42-41 19 8 34 22 42 41", 1.4), ("M76 88c6-11 14-19 24-24 10 5 18 13 24 24", 1.3)]:
        m = path_mask(W, H, P(d), stroke=wd * S)
        art = over(art, linocut(m, "#6b5016", seed=nxt(), wear=.45, rough=1.2))
        hl = np.roll(m, -2, 0) * (1 - m)
        art = over(art, fade(linocut(hl, "#f6e2a4", seed=nxt(), wear=.5, rough=1), .55))
    # pearl dots
    dots = [(100, 30, 2), (66, 52, 1.8), (134, 52, 1.8), (48, 72, 1.6), (152, 72, 1.6), (84, 42, 1.6), (116, 42, 1.6)]
    art = over(art, gouache_paint(circles_mask(W, H, [(ox + x * S, oy + y * S, r * S) for x, y, r in dots]), "#fff6d8", "#efe0b0", seed=nxt(), rough=.8))
    # emerald centre leaf with gold rim
    leaf = displace(path_mask(W, H, P("M100 56c7 6 9 13 0 22-9-9-7-16 0-22Z")), nxt(), 1.2, 10)
    art = over(art, foil(grow(leaf, 1.6 * S), "#e3c66f", seed=nxt(), emboss=.5))
    art = over(art, gouache_paint(leaf, "#1d4a33", "#2f6b4c", seed=nxt(), rough=1.2))
    art = glaze(art, pigment(shape_mask(W, H, ellipse_pts(ox + 98 * S, oy + 62 * S, 2.4 * S, 4 * S, 8)), "#7fb08e", seed=nxt(), density=.5, edge=.2, bloom=0, rough=1))
    # base band
    art = over(art, foil(band, "#b8913d", seed=nxt(), emboss=.8, sparkle=.02))
    bd = [(40, 103), (60, 99), (80, 97), (100, 96.5), (120, 97), (140, 99), (160, 103)]
    art = over(art, gouache_paint(circles_mask(W, H, [(ox + x * S, oy + y * S, (2.3 if x == 100 else 1.9) * S) for x, y in bd]), GREEN, "#2f6b4c", seed=nxt(), rough=.9))
    size = save_asset(art, f"{OUT}/siger.webp", max_w=400, quality=82)
    preview(art, f"{PRE}/siger_dark.png", "#1d4a33"); preview(art, f"{PRE}/siger_light.png", "#dfe7d6")
    return size


# ---------------- Mega Mendung cloud ----------------
LOBES = [(46, 74, 17), (78, 56, 26), (118, 44, 31), (160, 52, 25), (190, 68, 18), (28, 86, 11), (210, 84, 11)]
def cloud(name, cols, gold, core_bloom):
    """Mega Mendung: lobed cloud, 5 graded gouache bands from the gold-lined rim inward, soft back-run in the core."""
    S = 2.6; W, H = int(236 * S), int(110 * S)
    def draw(cv):
        pt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for (x, y, r) in LOBES:
            cv.c.drawCircle(x * S, y * S, r * S, pt)
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(20 * S, 66 * S, 218 * S, 96 * S), 14 * S, 14 * S), pt)
    shape = displace(mask_from(W, H, draw), nxt(), 3.5, 46)
    rim = outline(shape, 1.6 * S)
    a, b, c, d, e = cols
    bl = bands(shape, [w * S for w in (4.2, 4.2, 4.2, 4.2)])
    art = blank(W, H)
    for k, col in enumerate([a, b, c, d, e]):
        m = displace(np.clip(bl[k] + (bl[k + 1] if k + 1 < len(bl) else 0) * 0, 0, 1), nxt(), 1.4, 22)
        art = over(art, gouache_paint(np.maximum(m, shape * (k == 0)), col, mix(col, b if k else a, .2), seed=nxt(), rough=1.4, streak=.25))
    art = glaze(art, pigment(bl[-1], core_bloom, seed=nxt(), density=.28, edge=.25, bloom=.6, gran=.25, rough=6, feather=3))
    art = over(art, foil(displace(rim, nxt(), 1.0, 16), gold, seed=nxt(), emboss=.35, sparkle=0))
    size = save_asset(art, f"{OUT}/{name}.webp", max_w=600, quality=80)
    preview(art, f"{PRE}/{name}.png", "#163d2a" if name == "cloud-dark" else "#f7f2e4")
    return size


# ---------------- roncean melati strand ----------------
def ronce():
    S = 3.0; W, H = int(30 * S), int(228 * S); ox = 3 * S; oy = 2 * S
    art = blank(W, H)
    thread = [(ox + 12 * S + math.sin(t * 9) * .6, oy + t * 214 * S) for t in np.linspace(0, 1, 60)]
    art = over(art, gouache_paint(stroke_mask(W, H, thread, 1.1 * S, (0.01, 0.01)), "#d9cc9e", "#bfae78", seed=nxt(), rough=.6))
    for y in range(14, 214, 14):
        cx, cy = ox + 12 * S + rng.uniform(-.6, .6) * S, oy + y * S
        if (y // 14) % 3 == 0:
            lay, _ = melati_layer(W, H, cx, cy, 6.4 * S, rot=rng.uniform(0, 1))
            art = over(art, lay)
        else:
            m = shape_mask(W, H, deform(ellipse_pts(cx, cy, 3.3 * S, 5.6 * S, 10, rng.uniform(-.15, .15)), rng, 1, .06))
            art = over(art, gouache_paint(m, IVORY, "#f3ecd8", seed=nxt(), rough=.9))
            sh = shape_mask(W, H, ellipse_pts(cx + 1.4 * S, cy + .8 * S, 2 * S, 4.6 * S, 10))
            art = glaze(art, pigment(sh * m, "#d6ccad", seed=nxt(), density=.4, edge=.2, bloom=0, rough=.8, feather=1.4))
            art = over(shadow(m, 2, 3, 2.5, .3, "#3d4a2e"), art)
            tip = shape_mask(W, H, ellipse_pts(cx, cy - 5.2 * S, 1.3 * S, 1.2 * S, 8))
            art = over(art, gouache_paint(tip, "#9cae7a", seed=nxt(), rough=.5))
    lay, _ = melati_layer(W, H, ox + 12 * S, oy + 214 * S, 7.6 * S, rot=.3)
    art = over(art, lay)
    size = save_asset(art, f"{OUT}/ronce.webp", max_w=44, quality=84)
    preview(art, f"{PRE}/ronce.png", "#163d2a")
    return size


def melati():
    W = H = 200
    lay, _ = melati_layer(W, H, 100, 100, 82, rot=-.3)
    size = save_asset(lay, f"{OUT}/melati.webp", max_w=96, quality=84)
    preview(lay, f"{PRE}/melati.png", "#1d4a33")
    return size


def divider():
    S = 2.5; W, H = int(164 * S), int(28 * S); ox, oy = 2 * S, 2 * S
    art = blank(W, H)
    for d in ["M4 12h52", "M104 12h52"]:
        m = path_mask(W, H, svg_path(d, S, ox, oy), stroke=1.3 * S)
        art = over(art, foil(displace(m, nxt(), .8, 12), GOLD, seed=nxt(), emboss=.3, sparkle=.05))
    for d in ["M56 12c6-7 12-8 18-4", "M104 12c-6-7-12-8-18-4", "M56 12c6 7 12 8 18 4", "M104 12c-6 7-12 8-18 4"]:
        pts_path = svg_path(d, S, ox, oy)
        m = path_mask(W, H, pts_path, stroke=1.6 * S)
        art = over(art, foil(displace(m, nxt(), .6, 10), GOLD, seed=nxt(), emboss=.3, sparkle=.05))
    lay, _ = melati_layer(W, H, ox + 80 * S, oy + 12 * S, 9.5 * S, rot=-.2)
    art = over(art, lay)
    size = save_asset(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    preview(art, f"{PRE}/divider.png", "#f7f2e4")
    return size


if __name__ == "__main__":
    print("siger", siger())
    print("cloud-dark", cloud("cloud-dark", ("#0e271b", "#163d2a", "#1f4e36", "#2a6145", "#2f6b4c"), "#d9bd6c", "#4c8a66"))
    print("cloud-light", cloud("cloud-light", ("#a9c19d", "#bdd0b1", "#cfddc5", "#dfe8d6", "#ecf1e6"), "#c9a54e", "#ffffff"))
    print("ronce", ronce())
    print("melati", melati())
    print("divider", divider())
    for f in sorted(os.listdir(OUT)):
        print(f, kb(f"{OUT}/{f}"), "KB")
