"""Cahaya Lilin — candlelit dinner in warm gouache on dark: a cluster of pillar candles with melted tops and wax drips
(flames are a separate flickering sprite), two clinking wine glasses with glints, a brass taper candlestick, scattered
rose petals and a dark bokeh backdrop.
Run: python3 -I cahaya-lilin.py [part ...]   parts: candles flame glasses taper bokeh petals
Assets -> public/themes/art/cahaya-lilin/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f5_lib import *  # noqa

OUT = outdir("cahaya-lilin")
PARTS = sys.argv[1:] or ["candles", "flame", "glasses", "taper", "bokeh", "petals"]
DARK = "#24110e"
BRASS, BRASS2, BRASSD, BRASSL = "#b8873e", "#c99a4c", "#5a3a18", "#ffe1a0"
PET, PET2, PETD = "#8e1b2c", "#a8283a", "#4a0a14"


def petals(art, W, H, items, nx, rng):
    for x, y, r, a in items:
        pts = deform(petal_pts(x, y, r * 1.6, r * 0.9, a, 14, cup=0.25), rng, 1, 0.02)
        m = shapes(W, H, [pts])
        art = GP(art, m, PET, PET2, seed=nx(), rough=0.8, streak=0.5)
        art = tint(art, side_light(m, 3, 4, 4), PETD, 0.6, seed=nx())
        art = tint(art, side_light(m, -2, -3, 3), "#e0566a", 0.35, seed=nx())
    return art


def brass(art, m, nx, ldir=(8, 4)):
    art = GP(art, m, BRASS, BRASS2, seed=nx(), rough=0.5, streak=0.6)
    art = tint(art, side_light(m, ldir[0], ldir[1], 6), BRASSD, 0.75, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .6, -ldir[1] * .6, 3), BRASSL, 0.6, seed=nx())
    return art


if "candles" in PARTS:
    W, H = 640, 760
    nx = Seq(40100); rng = random.Random(401)
    art = blank(W, H)
    # warm pool of light on the table
    art = OV(art, ellipses(W, H, [(320, 700, 300, 46, 0)]), lambda mm: col_arr(mm, "#c26a2a", np.clip(gaussian_filter(mm, 22), 0, 1) * 0.55), pad=60)
    # brass tray
    tray = ellipses(W, H, [(320, 704, 270, 34, 0)])
    art = brass(art, tray, nx, (0, 6))
    art = tint(art, ellipses(W, H, [(320, 698, 250, 24, 0)]) * tray, "#7a5124", 0.5, seed=nx())
    wicks = []
    for cx, top, base, rw, nd in ((330, 250, 694, 74, 7), (170, 420, 702, 64, 5), (474, 486, 706, 60, 5)):
        art, wk = pillar_candle(art, W, H, cx, base, top, rw, nx, rng, drips=nd)
        wicks.append(wk)
        clear()
    art = petals(art, W, H, [(70, 724, 16, 0.4), (110, 740, 14, 2.2), (560, 730, 15, -0.6), (600, 716, 12, 1.8), (520, 748, 13, 3.0)], nx, rng)
    preview(art, "cl-candles", bg=DARK)
    save_full(art, f"{OUT}/candles.webp", size=(320, 380), quality=82)
    print("wicks % :", [(round(x / W * 100, 2), round(y / H * 100, 2)) for x, y in wicks])
    clear()

if "flame" in PARTS:
    W, H = 200, 320
    nx = Seq(40200)
    art = blank(W, H)
    hm = circles(W, H, [(100, 190, 30)])
    art = OV(art, hm, lambda mm: col_arr(mm, "#ffc070", np.clip(gaussian_filter(mm, 18), 0, 1) * 0.5), pad=80)
    art = candle_flame(art, W, H, 100, 220, 84, 19, nx, lean=0.04, halo=0.0)
    art = edge_fade(art, 60)
    preview(art, "cl-flame", bg=DARK)
    save_full(art, f"{OUT}/flame.webp", size=(100, 160), quality=86)
    clear()

if "glasses" in PARTS:
    W, H = 560, 640
    nx = Seq(40300); rng = random.Random(403)
    art = blank(W, H)

    def rot(pts, ox, oy, a):
        ca, sa = math.cos(a), math.sin(a)
        return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]

    for ox, ang, liquid in ((150, 0.14, 0.52), (410, -0.14, 0.46)):
        foot_y = 600
        bowl = [(ox - 60, 150), (ox - 76, 205), (ox - 80, 260), (ox - 58, 330), (ox - 16, 362), (ox, 364), (ox + 16, 362), (ox + 58, 330), (ox + 80, 260), (ox + 76, 205), (ox + 60, 150)]
        bowl_r = rot(bowl, ox, foot_y, ang)
        stem = rot([(ox - 4, 360), (ox + 4, 360), (ox + 4, 590), (ox - 4, 590)], ox, foot_y, ang)
        bm = shapes(W, H, [bowl_r]); sm = shapes(W, H, [stem], smooth=False)
        fm = ellipses(W, H, [(ox, foot_y, 70, 12, 0)])
        # wine
        cut = 150 + (364 - 150) * liquid
        wine = [p for p in bowl if p[1] >= cut]
        wine = [(ox - 80 + 4, cut)] + wine[1:-1] + [(ox + 80 - 4, cut)] if wine else []
        rimm = strokes(W, H, [(rot(arc_pts(ox, 150, 60, 0, math.tau, 40, 0.16), ox, foot_y, ang), 2.2, None)])
        art = OV(art, rimm, lambda mm: col_arr(mm, "#fff1d6", mm * 0.6), pad=4)
        cw = foot_y - (foot_y - cut) * math.cos(ang)
        rows = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
        lm = bm * np.clip(rows - cw, 0, 1)
        art = GP(art, lm, "#5e0d19", "#7a1424", seed=nx(), rough=0.4, streak=0.4)
        art = tint(art, side_light(lm, -14, 6, 12), "#c23a3c", 0.5, seed=nx())
        art = tint(art, gaussian_filter(np.exp(-((rows - cw - 3) / 4) ** 2) * bm, 1), "#d0564a", 0.6, seed=nx())
        for m_ in (bm, np.clip(sm + fm, 0, 1)):
            art = glass_glints(art, m_, nx, amt=1.2)
        art = OV(art, sm, lambda mm: col_arr(mm, "#e8cfa8", mm * 0.35), pad=4)
        # long vertical highlight on the bowl's lit side + a small catch light
        hl = strokes(W, H, [(rot([(ox - 56, 175), (ox - 62, 240), (ox - 48, 300)], ox, foot_y, ang), 7, (0.3, 0.4))])
        art = OV(art, hl, lambda mm: col_arr(mm, "#fff7e6", np.clip(gaussian_filter(mm, 1.2), 0, 1) * 0.75), pad=6)
        hl2 = strokes(W, H, [(rot([(ox + 58, 200), (ox + 62, 250)], ox, foot_y, ang), 3, (0.3, 0.4))])
        art = OV(art, hl2, lambda mm: col_arr(mm, "#ffd9a0", mm * 0.5), pad=6)
        clear()
    # clink sparkle
    art = spark(art, 280, 158, 26, col="#fff3d6", amt=0.95, glow_col="#ffcf7a")
    preview(art, "cl-glasses", bg=DARK)
    save(art, f"{OUT}/glasses.webp", max_w=280, quality=84)
    clear()

if "taper" in PARTS:
    W, H = 220, 700
    nx = Seq(40400); rng = random.Random(404)
    art = blank(W, H)
    art = candle_flame(art, W, H, 110, 128, 70, 15, nx, lean=0.02, halo=0.9)
    taper = shapes(W, H, [[(96, 130), (124, 130), (127, 470), (93, 470)]], smooth=False)
    art = GP(art, taper, "#f0e3c8", "#e7d6b4", seed=nx(), rough=0.5)
    art = tint(art, side_light(taper, 9, 0, 5), "#6a3a24", 0.75, seed=nx())
    yy = np.arange(H)[:, None] * np.ones((1, W))
    art = tint(art, taper * np.exp(-((yy - 130) / 60) ** 2), "#ffcf86", 0.5, seed=nx())
    drip = strokes(W, H, [([(100, 134), (99, 190)], 7, (0, 0)), ([(121, 134), (122, 166)], 6, (0, 0))])
    art = GP(art, np.clip(drip + circles(W, H, [(99, 192, 4.6), (122, 168, 4)]), 0, 1), "#f8ecd4", seed=nx(), rough=0.3)
    # brass candlestick: cup, knopped stem, foot
    cup = shapes(W, H, [[(70, 466), (150, 466), (138, 490), (82, 490)]])
    knops = ellipses(W, H, [(110, 510, 26, 12, 0), (110, 560, 18, 9, 0), (110, 600, 30, 13, 0)])
    stem = shapes(W, H, [[(100, 488), (120, 488), (116, 640), (104, 640)]], smooth=False)
    foot = shapes(W, H, [[(40, 680), (180, 680), (150, 648), (124, 634), (96, 634), (70, 648)]])
    bm = np.clip(cup + knops + stem + foot, 0, 1)
    art = brass(art, bm, nx)
    art = OV(art, strokes(W, H, [([(90, 470), (94, 486)], 3, None), ([(96, 505), (100, 514)], 3, None), ([(80, 664), (100, 650)], 3, None)]), lambda mm: col_arr(mm, "#fff1c8", mm * 0.8), pad=4)
    art = edge_fade(art, 24)
    preview(art, "cl-taper", bg=DARK)
    save(art, f"{OUT}/taper.webp", max_w=110, quality=84)
    clear()

if "bokeh" in PARTS:
    W, H = 780, 1000
    nx = Seq(40500); rng = random.Random(405)
    art = painted_sky(W, H, [(0, "#1a0b0b"), (0.5, "#2b1310"), (1, "#3b1b12")], seed=nx(), streak=0.5)
    items = []
    for i in range(46):
        r = rng.choice((10, 14, 18, 26, 34, 46))
        col = rng.choice(("#ffb45c", "#ffc978", "#e8843a", "#b8343e", "#ffd99a"))
        items.append((rng.uniform(-20, W + 20), rng.uniform(-20, H + 20), r, col, rng.uniform(0.12, 0.38) * (1.2 if r < 20 else 0.8)))
    art = bokeh(art, W, H, items, seed=nx())
    art = add_grain(art, nx(), 0.03)
    preview(art, "cl-bokeh", bg=DARK)
    save_rgb(art, f"{OUT}/bokeh.webp", size=(520, 667), quality=70)
    clear()

if "petals" in PARTS:
    W, H = 300, 120
    nx = Seq(40600); rng = random.Random(406)
    art = blank(W, H)
    art = petals(art, W, H, [(50, 70, 16, 0.3), (110, 50, 13, 2.0), (190, 74, 17, -0.4), (250, 46, 12, 1.4)], nx, rng)
    preview(art, "cl-petals", bg=DARK)
    save(art, f"{OUT}/petals.webp", max_w=150, quality=84)
    clear()
