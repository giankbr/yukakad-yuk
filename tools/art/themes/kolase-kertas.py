"""Kolase Kertas — cut-paper collage (original): hand-cut leaves, lobed fronds, wobbly suns and stars, squiggles,
in bold flat construction-paper colours with fibre grain, torn edges and soft drop shadows; plus a translucent paper
tape piece and a kraft paper tile. Run: python3 -I kolase-kertas.py [part ...]
parts: top bottom star leaf strip blob tape paper   Assets -> public/themes/art/kolase-kertas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e5_lib import *  # noqa

OUT = outdir("kolase-kertas")
PARTS = sys.argv[1:] or ["top", "bottom", "star", "leaf", "strip", "blob", "tape", "paper"]
RED, COBALT, MUSTARD, PINK, GREEN, TEAL, CREAM, INK = "#e4512f", "#2f4fb8", "#f2b52e", "#f3a7b4", "#2f8a57", "#1f6f6a", "#fbf3e3", "#22202a"
BG = "#f3eadb"


def squiggle(cx, cy, L, amp, ang, waves=3):
    pts = []
    for i in range(60):
        u = i / 59
        x, y = (u - .5) * L, math.sin(u * waves * math.tau) * amp
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def leaf_with_vein(art, W, H, cx, cy, L, Wd, ang, col, vein, nx, torn=0.0, bend=0.4):
    m = shapes(W, H, [leaf_cut(cx, cy, L, Wd, ang, 22, bend)])
    art = cutpaper(art, m, col, seed=nx(), torn=torn, fleck=mix(col, INK, .4))
    # cut-out vein slits (paper removed -> paper below shows, here we paint the BG colour strips)
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (cx + u * L * ca - v * sa, cy + u * L * sa + v * ca)
    items = [([P(0.1, 0), P(0.88, 0)], max(3, Wd * .1), (0.05, 0.5))]
    for k in range(1, 5):
        u = 0.18 + k * 0.15
        for sd in (1, -1):
            items.append(([P(u, 0), P(u + 0.1, sd * Wd * 0.62 * math.sin(math.pi * u) ** .8)], max(2.4, Wd * .075), (0.05, 0.7)))
    v = strokes(W, H, items) * m
    return cutpaper(art, v, vein, seed=nx(), shadow=0, edge=0.6)


if "top" in PARTS:
    W, H = 860, 620
    nx = Seq(71100); rng = random.Random(711)
    art = blank(W, H)
    # big wobbly sun disk (red) with torn rim
    art = cutpaper(art, shapes(W, H, [blob_pts(640, 210, 150, rng, 11, 0.06)]), RED, seed=nx(), torn=2.6, fleck="#a8321b")
    # cobalt lobed frond sweeping from the right edge
    art = cutpaper(art, shapes(W, H, frond_polys(850, 90, 440, 70, math.pi * 0.82, 7, curl=-0.35)), COBALT, seed=nx(), fleck="#1b2e74")
    # mustard star
    art = cutpaper(art, shapes(W, H, [deform(star_pts(470, 330, 92, 44, 5, -1.3), rng, 1, 0.01)], smooth=False), MUSTARD, seed=nx(), fleck="#b07a12")
    # pink blob
    art = cutpaper(art, shapes(W, H, [blob_pts(760, 430, 90, rng, 8, 0.22, .4)]), PINK, seed=nx(), torn=2.2)
    # green leaves with cut veins
    art = leaf_with_vein(art, W, H, 830, 520, 330, 70, math.pi * 1.12, GREEN, PINK, nx)
    art = leaf_with_vein(art, W, H, 600, 60, 220, 50, math.pi * 0.75, TEAL, MUSTARD, nx, bend=-.4)
    clear()
    # cream squiggle + dots
    art = cutpaper(art, strokes(W, H, [(squiggle(560, 470, 230, 16, -0.35, 3), 16, None)]), CREAM, seed=nx(), shadow=0.25)
    dots = [(380, 180, 18), (420, 120, 11), (330, 250, 9), (700, 560, 14)]
    art = cutpaper(art, circles(W, H, dots), INK, seed=nx(), shadow=0.2)
    art = cutpaper(art, circles(W, H, [(520, 210, 26)]), GREEN, seed=nx())
    preview(art, "kk-top", tone=BG)
    save(art, f"{OUT}/top.webp", max_w=640, quality=80)
    clear()

if "bottom" in PARTS:
    W, H = 760, 520
    nx = Seq(71200); rng = random.Random(712)
    art = blank(W, H)
    art = cutpaper(art, shapes(W, H, [blob_pts(180, 380, 170, rng, 10, 0.12, .3)]), MUSTARD, seed=nx(), torn=2.6, fleck="#b07a12")
    art = leaf_with_vein(art, W, H, 0, 520, 420, 92, -math.pi * 0.36, GREEN, CREAM, nx, bend=.5)
    art = cutpaper(art, shapes(W, H, frond_polys(-10, 330, 380, 58, -0.3, 6, curl=-0.3)), RED, seed=nx(), fleck="#a8321b")
    art = leaf_with_vein(art, W, H, 300, 520, 260, 54, -math.pi * 0.6, COBALT, PINK, nx, bend=-.3)
    clear()
    art = cutpaper(art, shapes(W, H, [deform(star_pts(520, 410, 60, 28, 5, -1.7), rng, 1, 0.012)], smooth=False), PINK, seed=nx())
    art = cutpaper(art, strokes(W, H, [(squiggle(420, 300, 200, 13, -0.6, 2.5), 13, None)]), INK, seed=nx(), shadow=0.2)
    art = cutpaper(art, circles(W, H, [(640, 470, 22), (600, 360, 10), (250, 180, 14)]), TEAL, seed=nx())
    preview(art, "kk-bottom", tone=BG)
    save(art, f"{OUT}/bottom.webp", max_w=560, quality=80)
    clear()

if "star" in PARTS:
    W, H = 200, 200
    nx = Seq(71300); rng = random.Random(713)
    art = blank(W, H)
    art = cutpaper(art, shapes(W, H, [deform(star_pts(98, 104, 80, 38, 5, -1.45), rng, 1, 0.012)], smooth=False), MUSTARD, seed=nx(), fleck="#b07a12")
    preview(art, "kk-star", tone=BG)
    save(art, f"{OUT}/star.webp", max_w=96, quality=84)
    clear()

if "leaf" in PARTS:
    W, H = 260, 420
    nx = Seq(71400)
    art = blank(W, H)
    art = leaf_with_vein(art, W, H, 130, 400, 370, 80, -math.pi / 2 - 0.08, GREEN, MUSTARD, nx, bend=.5)
    preview(art, "kk-leaf", tone=BG)
    save(art, f"{OUT}/leaf.webp", max_w=150, quality=82)
    clear()

if "strip" in PARTS:
    W, H = 720, 120
    nx = Seq(71500); rng = random.Random(715)
    art = blank(W, H)
    art = cutpaper(art, circles(W, H, [(120, 62, 26)]), RED, seed=nx(), torn=1.8)
    art = cutpaper(art, shapes(W, H, [leaf_cut(176, 70, 120, 26, -0.25, 18, .4)]), GREEN, seed=nx())
    art = cutpaper(art, shapes(W, H, [deform(star_pts(360, 60, 40, 19, 5, -1.5), rng, 1, 0.012)], smooth=False), MUSTARD, seed=nx())
    art = cutpaper(art, shapes(W, H, [leaf_cut(544, 52, 120, 26, math.pi - 0.25, 18, .4)]), COBALT, seed=nx())
    art = cutpaper(art, circles(W, H, [(600, 62, 26)]), PINK, seed=nx(), torn=1.8)
    art = cutpaper(art, circles(W, H, [(40, 60, 8), (680, 60, 8), (300, 40, 6), (420, 84, 6)]), INK, seed=nx(), shadow=0.18)
    preview(art, "kk-strip", tone=BG)
    save(art, f"{OUT}/strip.webp", max_w=360, quality=82)
    clear()

if "blob" in PARTS:
    W, H = 560, 600
    nx = Seq(71600); rng = random.Random(716)
    art = blank(W, H)
    art = cutpaper(art, shapes(W, H, [blob_pts(280, 300, 240, rng, 10, 0.1, .2)]), PINK, seed=nx(), torn=3.0)
    art = cutpaper(art, shapes(W, H, [leaf_cut(470, 560, 220, 46, -math.pi * 0.62, 18, .4)]), GREEN, seed=nx())
    art = cutpaper(art, shapes(W, H, [deform(star_pts(90, 110, 56, 26, 5, -1.3), rng, 1, 0.012)], smooth=False), MUSTARD, seed=nx())
    preview(art, "kk-blob", tone=BG)
    save(art, f"{OUT}/blob.webp", max_w=300, quality=82)
    clear()

if "tape" in PARTS:
    W, H = 260, 90
    nx = Seq(71700)
    art = blank(W, H)
    m = shapes(W, H, [[(14, 18), (246, 12), (250, 72), (10, 78)]], smooth=False)
    m = displace(m, 7, 2.6, 6)
    art = OV(art, m, lambda mm: col_arr(mm, "#f7e7b8", np.clip(mm, 0, 1) * (0.62 + 0.12 * fbm(mm.shape[1], mm.shape[0], 3, 30, 2))), pad=4)
    art = OV(art, strokes(W, H, [([(20, 30 + k * 11), (240, 26 + k * 11)], 2, None) for k in range(4)]) * m, lambda mm: col_arr(mm, "#e9c779", mm * 0.35), pad=4)
    preview(art, "kk-tape", tone=BG)
    save(art, f"{OUT}/tape.webp", max_w=130, quality=84)
    clear()

if "paper" in PARTS:
    S = 384
    base = np.asarray(paper(S, S, BG, 11, fiber=0.7, mottle=0.4), np.float32) / 255
    fl = (np.random.default_rng(5).random((S, S)) > 0.9985).astype(np.float32)
    fl = tile_wrap(gaussian_filter(fl, 0.7) * 2.5)
    base = base * (1 - np.clip(fl, 0, 1)[..., None] * 0.35)
    arr = np.concatenate([base, np.ones((S, S, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/paper.webp", quality=74)
