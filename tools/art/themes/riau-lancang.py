"""Riau Lancang Kuning — Malay royal yellow boat (lancang kuning) in gouache + gold foil with a balai cabin crowned by
selembayung crossed horns, royal umbrella and long pennants (floral scroll prow, no figures); painted sea band;
gilt selembayung ornament; tenun Siak tile (gold supplementary weft on sea-teal); awan larat gilt divider.
Run: python3 -I riau-lancang.py [part ...]   parts: tenun lancang laut selembayung awan"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d1_lib import *
import _jw_lib as jw
from _jw_lib import spiral_pts

OUT = outdir("riau-lancang")
PARTS = sys.argv[1:] or ["tenun", "lancang", "laut", "selembayung", "awan"]
YEL, YEL_D, YEL_L = "#e9b724", "#c08a14", "#f7dc7a"
GRN, GRN_D = "#1f5b3a", "#123a25"
RED = "#9e2a22"
SEA, SEA_D, SEA_L = "#1b5868", "#0f3a48", "#5f9aa3"
GOLD, GOLD_L = "#cf9f3e", "#f1d58a"
CREAM = "#fbf1d4"


def outline(m, px):
    return np.clip((gaussian_filter(m, px * 0.6) > 0.03).astype(np.float32) - m, 0, 1)


# ------------------------------------------------------------------ tenun Siak
def siak_design(N=120):
    """Gold-float map at thread resolution: lattice of siku keluang zigzags framing bunga tanjung flowers."""
    lay = lambda f: wrap_draw(N, N, f)
    c0 = N / 2
    def lattice(c, p):
        # stepped diagonals (siku keluang) crossing into a lozenge lattice
        sp = stroke_paint(2.0)
        st = 6
        for off in range(-N, 2 * N, N // 2):
            for sgn in (1, -1):
                pts = []
                for i in range(0, N // st + 2):
                    x = i * st
                    y = off + sgn * x
                    pts += [(x, y), (x + st, y)]
                c.drawPath(path_of(pts, closed=False), sp)
    def flower(c, p, cx, cy, r):
        for i in range(8):
            a = i * math.pi / 4
            c.save(); c.translate(cx, cy); c.rotate(math.degrees(a))
            c.drawPath(path_of([(r * 0.25, 0), (r * 0.7, -r * 0.22), (r, 0), (r * 0.7, r * 0.22)]), p)
            c.restore()
        c.drawCircle(cx, cy, r * 0.18, p)
    def flowers(c, p):
        flower(c, p, c0, c0, 15)
        flower(c, p, 0, 0, 15)
        for (x, y) in [(c0, 0), (0, c0)]:
            for i in range(4):
                a = i * math.pi / 2
                c.drawPath(path_of([(x, y), (x + math.cos(a) * 7 - math.sin(a) * 3, y + math.sin(a) * 7 + math.cos(a) * 3), (x + math.cos(a) * 10, y + math.sin(a) * 10), (x + math.cos(a) * 7 + math.sin(a) * 3, y + math.sin(a) * 7 - math.cos(a) * 3)]), p)
    m = np.maximum(lay(lattice), lay(flowers))
    return (m > 0.5).astype(np.float32)


if "tenun" in PARTS:
    N = 120
    # ground: fine plain weave, sea-teal warp with a deeper weft (shot silk)
    D = np.zeros((N, N), np.int32)
    ground = ikat(D, [SEA], p=3, mode="warp", ground=SEA_D, face=0.5, amp=0, seed=3, bleed=0, slub=0.1, fibre=0.05, thread_var=0.04)
    gm = siak_design(N)
    cloth = songket(ground, gm, p=3, base="#e6bd5a", deep="#7a5520", seed=5, float_len=4)
    prev_rgb(tile_to(cloth, 720, 540), "tenun-rep")
    save_rgb_arr(cloth, f"{OUT}/tenun.webp", quality=80)
    clear()


def selembayung_masks(W, H, cx, by, s):
    """Crossed upswept horns rising from a little roof gable; returns (horns, gable, carving lines)."""
    horns = []
    for sg in (-1, 1):
        base = (cx - sg * s * 0.12, by)
        pts = curve([base, (cx + sg * s * 0.18, by - s * 0.45), (cx + sg * s * 0.52, by - s * 0.78), (cx + sg * s * 0.86, by - s * 0.84), (cx + sg * s * 0.98, by - s * 0.70)], 40)
        horns.append(pts)
    hm = strokes(W, H, [(p, s * 0.13, (0.0, 0.62)) for p in horns])
    curls = strokes(W, H, [(spiral_pts(cx + sg * s * 0.92, by - s * 0.76, s * 0.12, s * 0.02, (0 if sg > 0 else math.pi) + math.pi / 2, 1.1, 30, sg), s * 0.04, (0.0, 0.6)) for sg in (-1, 1)])
    gable = poly(W, H, [(cx - s * 0.5, by + s * 0.34), (cx, by - s * 0.02), (cx + s * 0.5, by + s * 0.34)], smooth=False)
    inner = strokes(W, H, [(p[4:-6], s * 0.025, None) for p in horns])
    leaves = []
    for sg in (-1, 1):
        for t, L in [(0.35, 0.22), (0.55, 0.18), (0.72, 0.14)]:
            p = horns[0 if sg < 0 else 1][int(t * 39)]
            leaves.append(petal_pts(p[0], p[1], s * L, s * L * 0.34, -math.pi / 2 - sg * 0.9, n=10))
    lm = shapes(W, H, leaves)
    return hm, np.maximum(curls, 0), gable, inner, lm


if "selembayung" in PARTS:
    W, H = 420, 300
    nx = Seq(30100)
    art = blank(W, H)
    hm, curls, gable, inner, lm = selembayung_masks(W, H, W / 2, 222, 180)
    art = GP(art, gable, GRN, GRN_D, seed=nx(), rough=1.0)
    art = FO(art, outline(gable, 5), GOLD, seed=nx(), emboss=0.6)
    tri = strokes(W, H, [([(W / 2 - 80 + k * 20, 286), (W / 2, 222)], 1.8, None) for k in range(9)]) * gable
    art = FO(art, tri, GOLD, seed=nx(), emboss=0.4)
    art = FO(art, np.maximum.reduce([hm, curls, lm]), GOLD, seed=nx(), emboss=0.8, sparkle=0.18)
    art = G(art, inner, "#7a5520", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    preview(art, "selembayung", bg=SEA_D)
    save(art, f"{OUT}/selembayung.webp", max_w=300, quality=82)
    clear()


if "lancang" in PARTS:
    W, H = 840, 600
    nx = Seq(50100); rng = random.Random(4)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    wl = 470  # waterline
    gp = lambda a, m, c1, c2=None, **k: GP(a, m, c1, c2, seed=nx(), rough=1.2, streak=0.9, **k)
    # mast + yard + furled lateen sail in pale yellow cloth
    mast = strokes(W, H, [([(560, wl - 90), (556, 60)], 7, None), ([(470, 120), (700, 86)], 4, None)])
    art = gp(art, mast, "#6a4320", "#4a2e16")
    sail = poly(W, H, [(476, 126), (590, 104), (700, 92), (688, 210), (672, 330), (586, 340), (500, 354), (490, 240)], smooth=False)
    art = gp(art, sail, CREAM, "#f1dfa4")
    seams = strokes(W, H, [([(476 + (700 - 476) * t, 126 + (92 - 126) * t), (500 + (672 - 500) * t, 354 + (330 - 354) * t)], 1.2, None) for t in np.linspace(0.12, 0.88, 7)])
    art = G(art, seams * sail, "#b89a5a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    art = G(art, sail * np.clip((xx - 560) / 120, 0, 1), "#c9a75a", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=3)
    sb = np.maximum(outline(sail, 4) * 0, strokes(W, H, [([(476, 126), (700, 92)], 8, None), ([(500, 354), (672, 330)], 8, None)]))
    art = gp(art, sb * 1.0, GRN, GRN_D)
    art = gp(art, strokes(W, H, [([(560, wl - 60), (556, 56)], 7, None)]), "#6a4320", "#4a2e16")
    # long pennants (panji) from the masthead
    for k, (col, col2, dy) in enumerate([(YEL, YEL_D, 0), (GRN, GRN_D, 14), (RED, "#7a1d18", 28)]):
        pts = [(556 + 10 * t * 0, 64 + dy) for t in [0]] + [(556 - 260 * t, 64 + dy + 26 * t + 12 * math.sin(t * 7 + k)) for t in np.linspace(0.02, 1, 30)]
        pm = shapes(W, H, [ribbon_poly(pts, 12 - k * 2, 2)])
        art = gp(art, pm, col, col2)
    # royal umbrella (payung) on the stern deck
    pole = strokes(W, H, [([(190, wl - 52), (190, 250)], 4, None)])
    art = gp(art, pole, "#6a4320")
    canopy = poly(W, H, [(126, 276)] + [(190 + math.cos(a) * 66, 276 - math.sin(a) * 42) for a in np.linspace(0, math.pi, 24)][::-1] + [(254, 276)])
    art = gp(art, canopy, YEL, YEL_D)
    art = G(art, canopy * (xx > 200), YEL_D, seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=2)
    fr = strokes(W, H, [([(x, 276), (x, 290)], 3, (0, 0.5)) for x in range(130, 252, 8)])
    art = FO(art, np.maximum(fr, outline(canopy, 4)), GOLD, seed=nx(), emboss=0.5)
    art = FO(art, circles(W, H, [(190, 230, 8)]), GOLD, seed=nx())
    # balai (cabin) with Malay pitched roof and selembayung at both ridge ends
    wall = poly(W, H, [(286, wl - 112), (520, wl - 112), (520, wl - 46), (286, wl - 46)], smooth=False)
    art = gp(art, wall, YEL_L, YEL)
    wins = shapes(W, H, [[(x - 13, wl - 52), (x - 13, wl - 86), (x, wl - 100), (x + 13, wl - 86), (x + 13, wl - 52)] for x in range(318, 500, 44)], smooth=False)
    art = gp(art, wins, "#3a2614", "#24170c")
    art = FO(art, outline(wins, 3), GOLD, seed=nx(), emboss=0.5)
    roof = poly(W, H, [(268, wl - 108), (318, wl - 170), (488, wl - 170), (538, wl - 108)], smooth=False)
    art = gp(art, roof, GRN, GRN_D)
    art = G(art, roof * (xx > 430), GRN_D, seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=2)
    art = G(art, strokes(W, H, [([(268 + k * 10, wl - 108), (318 + k * 6.6, wl - 170)], 1.0, None) for k in range(28)]) * roof, "#0c2618", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4)
    art = FO(art, np.maximum(strokes(W, H, [([(262, wl - 106), (544, wl - 106)], 6, None), ([(316, wl - 172), (490, wl - 172)], 5, None)]), outline(roof, 3)), GOLD, seed=nx(), emboss=0.6)
    for ex in (318, 488):
        hm, curls, gable, inner, lm = selembayung_masks(W, H, ex, wl - 172, 64)
        art = FO(art, np.maximum.reduce([hm, curls, lm]), GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    # hull: long crescent sweeping up to a scrolled prow and stern
    top = curve([(40, wl - 150), (90, wl - 80), (250, wl - 48), (520, wl - 46), (720, wl - 70), (800, wl - 170)], 60)
    bot = curve([(770, wl - 92), (690, wl - 6), (430, wl + 16), (170, wl + 4), (66, wl - 90)], 60)
    hull = poly(W, H, top + bot)
    art = gp(art, hull, YEL, YEL_D)
    art = G(art, hull * np.clip((yy - (wl - 30)) / 40, 0, 1), "#8a5a10", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=3)
    art = G(art, hull * np.clip(((wl - 40) - yy) / 30, 0, 1) * (xx < 700), YEL_L, seed=nx(), density=0.35, edge=0, bloom=0.3, rough=3)
    band = strokes(W, H, [(curve([(80, wl - 74), (250, wl - 38), (520, wl - 36), (730, wl - 60)], 50), 13, (0.05, 0.05))])
    art = gp(art, band, GRN, GRN_D)
    redl = strokes(W, H, [(curve([(110, wl - 52), (260, wl - 20), (520, wl - 18), (710, wl - 40)], 50), 4, (0.05, 0.05))])
    art = gp(art, redl, RED, "#7a1d18")
    # carved gold scroll along the green band + prow/stern spirals (floral, no figures)
    items, leaves = [], []
    path = curve([(110, wl - 70), (250, wl - 36), (520, wl - 34), (700, wl - 56)], 60)
    for k, (x, y, a) in enumerate(jw.along(path, 34)):
        it, lv = jw.lung(x, y, 12, a, 1 if k % 2 else -1); items += it; leaves += lv
    scroll = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    prow = strokes(W, H, [(spiral_pts(786, wl - 176, 34, 4, math.pi * 0.2, 1.4, 50, -1), 7, (0.0, 0.6)), (spiral_pts(52, wl - 158, 30, 4, math.pi * 0.8, 1.4, 50, 1), 7, (0.0, 0.6)),
                          (curve([(730, wl - 70), (770, wl - 110), (790, wl - 150)], 16), 5, None), (curve([(90, wl - 80), (60, wl - 116), (50, wl - 140)], 16), 5, None)])
    pl = shapes(W, H, [petal_pts(760, wl - 130, 36, 11, -2.1, n=10), petal_pts(780, wl - 100, 30, 9, -0.4, n=10), petal_pts(74, wl - 120, 34, 10, -1.0, n=10), petal_pts(56, wl - 96, 28, 9, -2.8, n=10)])
    art = FO(art, np.maximum.reduce([scroll, prow, pl, outline(hull, 4)]), GOLD, seed=nx(), emboss=0.75, sparkle=0.16)
    # water: shadow under the hull and broken wave strokes
    sh = poly(W, H, deform(ellipse_pts(430, wl + 18, 380, 16, 20), rng, 1, 0.03))
    art = G(art, sh, SEA_D, seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=4, feather=4)
    waves = []
    for _ in range(46):
        x = rng.uniform(20, W - 40); y = rng.uniform(wl + 6, wl + 60); L = rng.uniform(30, 90)
        waves.append((curve([(x, y), (x + L * 0.5, y - 5), (x + L, y)], 10), rng.uniform(2, 4), (0.3, 0.4)))
    art = G(art, strokes(W, H, waves), SEA, SEA_L, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=1)
    art = G(art, strokes(W, H, waves[::3]), "#e9f1ea", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.8, feather=0.6)
    preview(art, "lancang", tone="#f6eed8")
    save(art, f"{OUT}/lancang.webp", max_w=680, quality=82)
    clear()


if "laut" in PARTS:
    # seamless sea band: rolling Malay sea with curling crests (tiles along x)
    W, H = 720, 190
    nx = Seq(60100); rng = random.Random(6)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    def wave_row(y, amp, per, ph):
        return [(x, y + amp * math.sin(x / per * math.tau + ph)) for x in np.linspace(-40, W + 40, 80)]
    rows = [(40, 8, W / 4, 0.0, SEA_L, "#86b4b4", 0.55), (80, 10, W / 3, 1.0, SEA, SEA_L, 0.75), (126, 12, W / 2, 2.0, SEA_D, SEA, 0.9)]
    for (y, amp, per, ph, cA, cB, d) in rows:
        pts = wave_row(y, amp, per, ph)
        m = poly(W, H, pts + [(W + 40, H + 10), (-40, H + 10)], smooth=False)
        art = G(art, m, cA, cB, seed=nx(), density=d, edge=0.45, bloom=0.35, rough=3, gran=0.3)
        crest = strokes(W, H, [(pts, 3, None)])
        art = G(art, crest, "#eef4ec", seed=nx(), density=0.65, edge=0.1, bloom=0, rough=1, feather=0.7)
    curls = []
    for k in range(6):
        cx = (k + 0.5) * W / 6; cy = 80 + 10 * math.sin(cx / (W / 3) * math.tau + 1.0)
        curls.append((spiral_pts(cx, cy - 6, 12, 2, math.pi, 1.2, 30, 1), 2.6, (0.0, 0.5)))
    art = G(art, strokes(W, H, curls), "#eef4ec", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.8, feather=0.6)
    # make it tile horizontally: crossfade the ends
    blend = np.clip(np.minimum(xx, W - 1 - xx) / 50, 0, 1)[..., None]
    rolled = np.roll(art, W // 2, 1)
    art = art * blend + rolled * (1 - blend)
    preview(art, "laut", tone="#f6eed8")
    save_full(art, f"{OUT}/laut.webp", quality=80)
    clear()


if "awan" in PARTS:
    # awan larat: a gilt cloud-scroll divider (floral, mirrored with hand imperfection)
    W, H = 420, 80
    nx = Seq(80100)
    art = blank(W, H)
    items, leaves = [], []
    for sg in (-1, 1):
        cx = W / 2
        pts = [(cx + sg * 30, 40), (cx + sg * 80, 28), (cx + sg * 130, 46), (cx + sg * 180, 34)]
        items.append((curve(pts, 40), 3.4, (0.05, 0.3)))
        for (x, y, r, d) in [(cx + sg * 70, 30, 12, 1), (cx + sg * 140, 46, 11, -1), (cx + sg * 190, 34, 9, 1)]:
            items.append((spiral_pts(x, y, r, 1.5, -math.pi / 2 * d, 1.1, 30, sg * d), 2.6, (0.0, 0.5)))
        leaves += [petal_pts(cx + sg * 100, 32, 20, 6, -math.pi / 2 - sg * 0.6, n=10), petal_pts(cx + sg * 160, 44, 16, 5, math.pi / 2 + sg * 0.5, n=10)]
    core = shapes(W, H, [[(W / 2, 22), (W / 2 + 14, 40), (W / 2, 58), (W / 2 - 14, 40)]])
    m = np.maximum.reduce([strokes(W, H, items), shapes(W, H, leaves), core])
    art = FO(art, m, GOLD, seed=nx(), emboss=0.7, sparkle=0.18)
    art = GP(art, shapes(W, H, [[(W / 2, 31), (W / 2 + 6, 40), (W / 2, 49), (W / 2 - 6, 40)]]), GRN, seed=nx(), rough=0.4)
    preview(art, "awan", bg=CREAM)
    save(art, f"{OUT}/awan.webp", max_w=320, quality=84)
    clear()
