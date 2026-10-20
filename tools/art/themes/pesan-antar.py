"""Pesan-Antar — gouache delivery scene (painted sky, hills, road) + courier on a scooter with a heart gift box
(separate layer so it rides), gouache product thumbnails (bedcover set, pot set, table lamp), receipt paper tile.
Run: python3 -I /tmp/pen/art/themes/pesan-antar.py [scene|courier|products|paper]"""
import sys, importlib
sys.path.insert(0, "/tmp/pen/art/themes")
from _p4_lib import *  # noqa
ho = importlib.import_module("hijau-ojek")

T = "pesan-antar"
D = outdir(T)
nxt = Seeds(700)
rng = random.Random(21)
INK = "#1f2a24"


def gp(mask, c1, c2=None, rough=2.0, streak=0.5, density=0.97):
    return gouache_paint(mask, c1, c2, seed=nxt(), rough=rough, streak=streak, density=density)


def scene():
    W, H = 640, 780
    rng.seed(4)
    art = painted_sky(W, H, [(0, "#1fa65a"), (0.35, "#34b86a"), (0.62, "#5fcf86"), (1, "#8fdfa6")], seed=nxt(), streak=1.0, grain=0.6)
    # sun glow top-right
    sun = shape_mask(W, H, ellipse_pts(W * .82, H * .14, 54, 54, 24))
    art = over(art, glow(sun, "#eaffbf", radius=40, strength=0.35))
    art = over(art, gp(sun, "#fff5c2", "#ffe99a", rough=2.0))
    # clouds: stacked gouache lumps
    def cloud(cx, cy, sc):
        m = np.zeros((H, W), np.float32)
        for (dx, dy, r) in [(-1.2, 0.1, 0.7), (-0.5, -0.3, 0.9), (0.3, -0.4, 1.0), (1.0, -0.1, 0.8), (1.6, 0.2, 0.55)]:
            m = np.maximum(m, shape_mask(W, H, deform(ellipse_pts(cx + dx * sc, cy + dy * sc, r * sc, r * sc * .85, 14), rng, 2, .06)))
        m = np.maximum(m, shape_mask(W, H, [(cx - 1.8 * sc, cy + 0.2 * sc), (cx + 2.1 * sc, cy + 0.2 * sc), (cx + 2.1 * sc, cy + 0.75 * sc), (cx - 1.8 * sc, cy + 0.75 * sc)]))
        return m
    for (cx, cy, sc, d) in [(120, 120, 34, 0.95), (430, 90, 26, 0.9), (560, 230, 20, 0.85), (40, 250, 18, 0.8), (300, 200, 16, 0.7)]:
        m = cloud(cx, cy, sc)
        art = over(art, gp(m, "#ffffff", "#eef9f0", rough=2.5, density=d))
        art = over(art, shade(gp(m, "#ffffff", "#eef9f0", rough=2.5, density=d * 0.9), m, light=(-0.3, -0.9), k=0.14, blur=8, hi="#ffffff", lo="#9fd9b4"))
    # hills (three ridges, lighter to darker)
    for k, (by, amp, c1, c2) in enumerate([(0.46, 44, "#8ee3ab", "#9deab7"), (0.52, 30, "#4fc77e", "#5dd38c"), (0.58, 22, "#239f52", "#2aab5b")]):
        m = shape_mask(W, H, ridge_pts(W, H, by, amp, rng, n=7))
        layer = gp(m, c1, c2, rough=3, streak=0.8)
        rim = np.clip(m - np.roll(gaussian_filter(m, 2.0), 5, axis=0), 0, 1)
        layer = tint(layer, gaussian_filter(rim, 1.5), "#d6ffd9", 0.35 - k * 0.1)
        art = over(art, layer)
    # trees on the middle ridge: round gouache canopies + trunks
    tr = np.zeros((H, W), np.float32); trunk = np.zeros((H, W), np.float32)
    for tx in [0.07, 0.16, 0.23, 0.72, 0.8, 0.9, 0.97, 0.44, 0.52]:
        x = W * tx + rng.uniform(-8, 8)
        y = H * 0.53 - 6 + rng.uniform(-8, 8)
        r = rng.uniform(16, 26)
        tr = np.maximum(tr, shape_mask(W, H, deform(ellipse_pts(x, y - r * .6, r, r * 1.1, 12), rng, 2, .1)))
        trunk = np.maximum(trunk, stroke_mask(W, H, [(x, y), (x, y + 18)], 5, (0.05, 0.2)))
    art = over(art, gp(trunk, "#6b4a2e", "#5a3d26", rough=0.8))
    art = over(art, gp(tr, "#1d8f47", "#167a3c", rough=2.5))
    art = over(art, shade(gp(tr, "#1d8f47", "#167a3c", rough=2.5), tr, light=(-0.5, -0.8), k=0.25, blur=6, hi="#7fe39b", lo="#0d5a2a"))
    # road: grey band with perspective and a dashed centre line, soft ink edges
    road = shape_mask(W, H, deform([(-20, H * .64), (W + 20, H * .62), (W + 20, H * .83), (-20, H * .85)], rng, 2, .008), smooth=False)
    art = over(art, gp(road, "#5f6670", "#6c737c", rough=2.5, streak=1.2))
    kerb = outline(road, 4.0)
    art = over(art, pigment(kerb, "#f2f5ef", seed=nxt(), density=0.6, edge=0, bloom=0, feather=0.8, rough=1.2, holes=0.15))
    dash = np.zeros((H, W), np.float32)
    for i in range(10):
        x0 = -10 + i * 70
        dash = np.maximum(dash, stroke_mask(W, H, [(x0, H * .745 + 2 - i * 0.6), (x0 + 38, H * .745 - i * 0.6)], 6, (0.05, 0.05)))
    art = over(art, gp(dash * road, "#f3ecc8", "#e8dfb0", rough=0.8, density=0.9))
    # grass verge above the road + below
    verge = shape_mask(W, H, deform([(-20, H * .60), (W + 20, H * .59), (W + 20, H * .635), (-20, H * .645)], rng, 2, .01), smooth=False)
    art = over(art, gp(verge, "#6cd38f", "#58c47c", rough=2.5))
    below = shape_mask(W, H, [(-20, H * .83), (W + 20, H * .82), (W + 20, H + 20), (-20, H + 20)], smooth=False)
    art = over(art, gp(below, "#3fb76c", "#2fa85d", rough=2.5))
    art[..., 3] = 1
    save_rgb(art, f"{D}/scene.webp", q=80)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/pa-scene.png")


def courier():
    ho.rng.seed(9)
    art = ho.rider_art(gift=True, jacket=("#00b14f", "#009643"), helm=("#1aa868", "#118a55"), scooter=("#f0b03a", "#d9962a"))
    preview(art, f"{PREV}/pa-courier.png", "#49c47c")
    save(art, f"{D}/courier.webp", max_w=500, q=82)


def products():
    S = 220
    rng.seed(27)
    out = {}
    # bed with bedcover + pillows
    art = blank(S, S)
    headb = shape_mask(S, S, wobble_rect(40, 56, 140, 46, rng, 2.0))
    mattress = shape_mask(S, S, deform([(28, 100), (192, 100), (196, 150), (24, 150)], rng, 2, .015))
    cover = shape_mask(S, S, deform([(28, 112), (192, 112), (196, 150), (24, 150)], rng, 2, .015))
    pil = union(shape_mask(S, S, wobble_rect(50, 92, 50, 22, rng, 2.0)), shape_mask(S, S, wobble_rect(118, 92, 50, 22, rng, 2.0)))
    legs = union(shape_mask(S, S, [(34, 150), (46, 150), (44, 166), (36, 166)]), shape_mask(S, S, [(174, 150), (186, 150), (184, 166), (176, 166)]))
    stripes = np.zeros((S, S), np.float32)
    for y in (124, 136):
        stripes = np.maximum(stripes, stroke_mask(S, S, [(30, y), (190, y)], 3, (0.02, 0.02)))
    art = over(art, gp(legs, "#6b4a2e", rough=0.8))
    art = over(art, gp(headb, "#8a5a3a", "#7a4e32", rough=1.5))
    art = over(art, gp(mattress, "#f3efe4", "#e8e2d4", rough=1.2))
    art = over(art, gp(pil, "#fbfaf4", "#eeeadf", rough=1.5))
    art = over(art, gp(cover, "#2fa66a", "#27925c", rough=1.5))
    art = over(art, gp(stripes * cover, "#bfe9d0", rough=0.6, density=0.8))
    ink_m = union(outline(union(headb, mattress), 2.8), outline(pil, 2.0), outline(cover, 2.0))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    out["bed"] = art
    # pot set: big pot with lid + small pan
    art = blank(S, S)
    pot = shape_mask(S, S, deform([(44, 92), (156, 92), (150, 158), (50, 158)], rng, 2, .012))
    lid = shape_mask(S, S, deform(ellipse_pts(100, 90, 62, 12, 20), rng, 1, .02))
    knob = shape_mask(S, S, ellipse_pts(100, 76, 9, 7, 12))
    hndl = union(shape_mask(S, S, [(28, 104), (46, 104), (46, 114), (28, 114)]), shape_mask(S, S, [(154, 104), (172, 104), (172, 114), (154, 114)]))
    band = stroke_mask(S, S, [(48, 124), (152, 124)], 7, (0.02, 0.02)) * pot
    pan = shape_mask(S, S, deform([(118, 150), (196, 150), (192, 176), (122, 176)], rng, 1, .02))
    pan_h = stroke_mask(S, S, [(194, 156), (214, 150)], 6, (0.05, 0.3))
    art = over(art, gp(hndl, "#3a3f44", rough=0.8))
    art = over(art, gp(pot, "#d8d9d6", "#c3c5c2", rough=1.5))
    art = over(art, shade(gp(pot, "#d8d9d6", "#c3c5c2", rough=1.5), pot, light=(-0.7, -0.4), k=0.22, blur=8, hi="#ffffff", lo="#6a6c6a"))
    art = over(art, gp(band, "#00b14f", "#009643", rough=0.6, density=0.9))
    art = over(art, gp(lid, "#b9bcbb", "#a6a9a8", rough=1.0))
    art = over(art, gp(knob, "#3a3f44", rough=0.6))
    art = over(art, gp(pan, "#2f3337", "#3a3f44", rough=1.2))
    art = over(art, gp(pan_h, "#2f3337", rough=0.6))
    ink_m = union(outline(pot, 2.8), outline(lid, 2.0), outline(pan, 2.2), outline(hndl, 1.6))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    out["pot"] = art
    # table lamp
    art = blank(S, S)
    shade_m = shape_mask(S, S, deform([(66, 56), (154, 56), (176, 118), (44, 118)], rng, 2, .012))
    stem = stroke_mask(S, S, [(110, 118), (110, 160)], 8, (0.02, 0.02))
    foot = shape_mask(S, S, deform(ellipse_pts(110, 164, 40, 10, 16), rng, 1, .02))
    glow_m = gaussian_filter(shape_mask(S, S, ellipse_pts(110, 128, 60, 24, 16)), 6)
    art = over(art, glow(glow_m, "#ffe8a3", radius=10, strength=0.35))
    art = over(art, gp(foot, "#5a4634", "#4a3a2b", rough=1.0))
    art = over(art, gp(stem, "#b08a5a", "#9a7649", rough=0.8))
    art = over(art, gp(shade_m, "#f6d98c", "#f0c766", rough=1.8))
    art = over(art, shade(gp(shade_m, "#f6d98c", "#f0c766", rough=1.8), shade_m, light=(-0.8, -0.3), k=0.2, blur=8, hi="#fff6d4", lo="#b98a2e"))
    pleats = np.zeros((S, S), np.float32)
    for i in range(1, 7):
        x = 66 + 88 * i / 7
        pleats = np.maximum(pleats, stroke_mask(S, S, [(x, 60), (44 + 132 * i / 7, 116)], 1.5, (0.05, 0.05)))
    art = over(art, pigment(pleats * shade_m, "#c99a3a", seed=nxt(), density=0.4, edge=0, bloom=0, feather=0.5, rough=0.6))
    ink_m = union(outline(shade_m, 2.8), outline(foot, 2.0), outline(stem, 1.6))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    out["lamp"] = art
    sheet = Image.new("RGB", (S * 3, S), "#f2fbf6")
    for i, (k, a) in enumerate(out.items()):
        save(a, f"{D}/p-{k}.webp", max_w=150, q=84, trim=False)
        sheet.paste(to_image(a), (i * S, 0), to_image(a))
    sheet.save(f"{PREV}/pa-products.png")


def paper_():
    S = 256
    t = paper_tile(S, "#fdfcf8", seed=9, mottle=1.4, fiber=1.6, fine=1.4)
    save_rgb(np.concatenate([t, np.ones((S, S, 1), np.float32)], -1), f"{D}/paper.webp", q=70)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["scene", "courier", "products", "paper"]:
        {"scene": scene, "courier": courier, "products": products, "paper": paper_}[w]()
