"""Halal Bihalal — warm green & yellow Lebaran gathering: woven janur ketupat (gouache over a real over/under weave),
terracotta pelita oil lamp with a warm flame, bedug drum on its stand (corner hint), seamless janur weave band tile.
Run: python3 -I halal-bihalal.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b6_lib import *

OUT = outdir("halal-bihalal")
PARTS = sys.argv[1:] or ["ketupat", "pelita", "bedug", "janur"]
JL, JM, JD = "#f1e59a", "#cdbb55", "#7d7a2c"
GREEN, GREEN_D = "#2f6b3a", "#1d4626"


def ketupat(W, H, cx, cy, r, nx, rng, tails=True):
    art = blank(W, H)
    dia = shapes(W, H, [deform([(cx, cy - r), (cx + r * 1.02, cy), (cx, cy + r), (cx - r * 1.02, cy)], rng, 1, 0.01)], smooth=False)
    dia = np.clip(gaussian_filter(dia, 1.2) * 1.2, 0, 1)
    sh = soft_shadow(dia, "#3a3a10", blur=8, strength=0.25, dx=5, dy=8)
    art = over(art, sh)
    weave = weave_layer(dia, cx, cy - r, math.pi / 4, r * 0.29, JL, JM, JD, seed=nx())
    art = over(art, weave)
    # a light wash of green where young janur is still greener, + rim shading
    art = G(art, dia * fbm(W, H, nx(), 70, 2), "#8fae45", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=2)
    art = G(art, shade_side(dia, -10, -10, 12), "#6c6420", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    if tails:
        tl = []
        for k, (dx, ln, curl) in enumerate([(-6, 1.1, -0.5), (5, 0.95, 0.45)]):
            tl.append((curve([(cx + dx, cy - r + 6), (cx + dx * 3 + curl * 30, cy - r - ln * r * 0.45), (cx + dx * 2 + curl * 70, cy - r - ln * r * 0.8)], 20), r * 0.15, (0.0, 0.6)))
        for k, (dx, ln) in enumerate([(-4, 0.7), (6, 0.55)]):
            tl.append((curve([(cx + dx, cy + r - 6), (cx + dx * 3 - 10, cy + r + ln * r * 0.5), (cx + dx * 5 - 24, cy + r + ln * r)], 20), r * 0.14, (0.0, 0.7)))
        tm = strokes(W, H, tl)
        art = GP(art, tm, JL, JM, seed=nx(), rough=0.6, streak=1.0, pad=8)
        art = G(art, np.clip(tm - gaussian_filter(tm, 1.6) * 1.1, 0, 1) * 2, JD, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
    return art


if "ketupat" in PARTS:
    W, H = 340, 460
    nx = Seq(40100); rng = random.Random(3)
    art = ketupat(W, H, 170, 250, 118, nx, rng)
    preview(art, "hb-ketupat")
    save(art, f"{OUT}/ketupat.webp", max_w=220, quality=82)
    clear()

if "pelita" in PARTS:
    W, H = 360, 340
    nx = Seq(40300); rng = random.Random(5)
    art = blank(W, H)
    sh = shapes(W, H, [ellipse_pts(150, 316, 110, 12, 16)])
    art = G(art, sh, "#3a2412", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=3, feather=6)
    foot = shapes(W, H, [[(112, 312), (188, 312), (176, 278), (124, 278)]])
    bowl = shapes(W, H, [arc_pts(150, 232, 104, 0, math.pi, 30, 0.5) + [(46, 232)]])
    spout = shapes(W, H, [[(214, 214), (282, 196), (290, 206), (238, 240)]])
    rim = ellipses(W, H, [(150, 230, 104, 22, 0)])
    oil = ellipses(W, H, [(150, 230, 88, 15, 0)])
    body = np.maximum.reduce([foot, bowl, spout])
    art = GP(art, body, "#b8653a", "#8c4523", seed=nx(), rough=1.2, streak=0.9, pad=10)
    art = G(art, shade_side(body, -16, -6, 10), "#5e2b14", seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1.5)
    art = GP(art, rim, "#cf7d4e", "#a95a32", seed=nx(), rough=0.8, pad=8)
    art = GP(art, oil, "#3a220f", "#5a3517", seed=nx(), rough=0.6, pad=6)
    band = strokes(W, H, [(arc_pts(150, 254, 96, 0.15, math.pi - 0.15, 30, 0.42), 4, None)])
    dotsm = circles(W, H, [(150 + math.cos(a) * 92, 262 + math.sin(a) * 34, 3.2) for a in [0.4 + k * 0.29 for k in range(9)]])
    art = GP(art, np.maximum(band, dotsm), "#f1d48a", "#d9b25a", seed=nx(), rough=0.5, pad=6)
    wick = strokes(W, H, [([(262, 204), (276, 192)], 4, None)])
    art = GP(art, wick, "#2a1a0e", seed=nx(), rough=0.3, pad=4)
    art = flame(W, H, 278, 192, 70, rng, nx, art)
    preview(art, "hb-pelita", bg="#1d4626")
    save(art, f"{OUT}/pelita.webp", max_w=170, quality=84)
    clear()

if "bedug" in PARTS:
    W, H = 700, 520
    nx = Seq(40500); rng = random.Random(7)
    art = blank(W, H)
    sh = shapes(W, H, [ellipse_pts(360, 494, 300, 18, 18)])
    art = G(art, sh, "#3a2412", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=3, feather=6)
    # stand: two A-frame legs + crossbar (behind the drum)
    stand = strokes(W, H, [([(200, 480), (250, 300)], 22, None), ([(300, 480), (250, 300)], 22, None), ([(500, 480), (540, 300)], 22, None),
                           ([(590, 480), (540, 300)], 22, None), ([(190, 440), (610, 440)], 16, None)])
    art = wood(art, stand, nx, "#6f4524", "#3d2412", "#8f5e34", angle=1.2, spacing=7, seed=21)
    # barrel (side) + hide head (left, 3/4)
    barrel = shapes(W, H, [[(178, 130), (300, 98), (385, 92), (470, 98), (592, 130), (606, 250), (592, 370), (470, 402), (385, 408), (300, 402), (178, 370)]])
    art = wood(art, barrel, nx, "#a34a2e", "#5c2213", "#c4673f", angle=0.0, spacing=14, seed=23)
    art = G(art, shade_side(barrel, 0, -30, 26), "#4e1c10", seed=nx(), density=0.5, edge=0, bloom=0.2, rough=2)
    hoops = strokes(W, H, [([(x, 120 + abs(x - 385) * 0.12), (x, 380 - abs(x - 385) * 0.12)], 7, None) for x in (300, 470)])
    art = GP(art, hoops * barrel, "#3d1a0e", "#2a1209", seed=nx(), rough=0.5, pad=6)
    head = ellipses(W, H, [(178, 250, 64, 134, 0)])
    rimh = np.clip(ellipses(W, H, [(178, 250, 74, 144, 0)]) - head, 0, 1)
    art = wood(art, ellipses(W, H, [(178, 250, 74, 144, 0)]), nx, "#7d3720", "#4a1d0f", "#a34a2e", angle=1.57, spacing=8, seed=25)
    art = GP(art, head, "#efdcb3", "#d6bc8a", seed=nx(), rough=0.8, streak=0.4, pad=8)
    art = G(art, head * fbm(W, H, nx(), 30, 3), "#b9975e", seed=nx(), density=0.3, edge=0.2, bloom=0.4, rough=2)
    art = G(art, np.clip(head - gaussian_filter(head, 6) * 1.05, 0, 1) * 2, "#8c6a3a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
    pegs = circles(W, H, [(178 + math.cos(a) * 69, 250 + math.sin(a) * 139, 4.6) for a in [k * math.tau / 22 for k in range(22)]])
    art = GP(art, pegs, "#e9cf8f", "#b99554", seed=nx(), rough=0.4, pad=6)
    _ = rimh
    # beater leaning
    beat = strokes(W, H, [([(640, 470), (560, 200)], 12, None)])
    knob = circles(W, H, [(556, 192, 18)])
    art = wood(art, beat, nx, "#8b5a30", "#4a2a14", "#b07b4c", angle=1.28, spacing=6, seed=27)
    art = GP(art, knob, "#e2c99a", "#b69766", seed=nx(), rough=0.6, pad=6)
    # green & yellow cloth ribbon tied around
    rib = strokes(W, H, [(curve([(470, 124), (486, 250), (470, 378)], 30), 16, None)])
    art = GP(art, rib * barrel, "#3f8a45", GREEN_D, seed=nx(), rough=0.6, pad=6)
    tails = strokes(W, H, [(curve([(478, 380), (500, 420), (488, 460)], 16), 12, (0, 0.6)), (curve([(470, 380), (446, 418), (452, 456)], 16), 11, (0, 0.6))])
    art = GP(art, tails, "#f2c14e", "#d39a2c", seed=nx(), rough=0.6, pad=6)
    preview(art, "hb-bedug")
    save(art, f"{OUT}/bedug.webp", max_w=420, quality=80)
    clear()

if "janur" in PARTS:
    # seamless horizontal weave band: strip period divides the tile exactly
    W, H = 288, 96
    nx = Seq(40700)
    strip = 24
    m = np.ones((H, W), np.float32)
    lay = weave_layer(m, 0, 0, math.pi / 4, strip / math.sqrt(2) * 1.0, JL, JM, JD, seed=3)
    im = to_image(lay).convert("RGB")
    im.save(f"{OUT}/janur.webp", "WEBP", quality=74, method=6)
    print("janur.webp", im.size, os.path.getsize(f"{OUT}/janur.webp") // 1024, "KB")
    Image.fromarray(np.tile(np.asarray(im), (1, 3, 1))).save("/tmp/pen/nb-B6/art/hb-janur.png")

kb(OUT)
