"""Sulam Zamrud — emerald silk satin embroidered with gold thread: couched gold cord outlines, satin-stitch 8-point
stars (each point split into two thread directions), satin florals in ivory/blush silk, leaf sprigs, French knots.
No figures, no calligraphy. Run: python3 -I sulam-zamrud.py [part ...]
parts: silk medallion wreath spray cord divider star"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d3_lib import *  # noqa

OUT = outdir("sulam-zamrud")
PARTS = sys.argv[1:] or ["silk", "medallion", "wreath", "spray", "cord", "divider", "star"]
EM, EM_D, EM_L = "#0f5b44", "#083a2b", "#1d7356"
GOLD, GOLD_L, GOLD_D = "#d9b75e", "#f2dc9a", "#8c6a27"
IVORY, IVORY2 = "#f4ecd6", "#e5d6b2"
BLUSH, BLUSH2 = "#ebbfae", "#d69a88"
LEAF, LEAF2 = "#8fc19c", "#5f9c76"


def star_points(cx, cy, R, ri, n=8, rot=-math.pi / 2):
    out = []
    for k in range(n):
        a = rot + k * math.tau / n
        tip = (cx + R * math.cos(a), cy + R * math.sin(a))
        l = (cx + ri * math.cos(a - math.pi / n), cy + ri * math.sin(a - math.pi / n))
        r = (cx + ri * math.cos(a + math.pi / n), cy + ri * math.sin(a + math.pi / n))
        out.append((a, tip, l, r))
    return out


def sat_star(art, W, H, cx, cy, R, ri, col=GOLD, col2=GOLD_L, n=8, rot=-math.pi / 2, sp=1.5, seed=1):
    """Satin-stitch star: each point split along its spine, threads of the two halves meet in a V."""
    for k, (a, tip, l, r) in enumerate(star_points(cx, cy, R, ri, n, rot)):
        for half, side in ((0, l), (1, r)):
            m = fills(W, H, [[(cx, cy), tip, side]])
            ang = a + (math.pi / 2 - 0.55) * (1 if half else -1)
            art = SAT(art, m, col, col2, angle=ang, spacing=sp, seed=seed + k * 2 + half, stitch=28, raise_=0.5, fuzz=0.3)
    return art


def flower(art, W, H, cx, cy, r, n=5, col=IVORY, col2=IVORY2, rot=0.0, seed=1, knot=GOLD):
    for k in range(n):
        a = rot + k * math.tau / n
        m = ellipses(W, H, [(cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55, r * 0.47, r * 0.31 * (5 / n) ** 0.6, math.degrees(a))])
        art = SAT(art, m, col, col2, radial=(cx, cy), spacing=1.4, seed=seed + k, stitch=30, raise_=0.7, fuzz=0.3)
    # gold French knots in the heart
    pts = [(cx, cy, r * 0.17)] + [(cx + math.cos(t) * r * 0.2, cy + math.sin(t) * r * 0.2, r * 0.09) for t in np.linspace(0, math.tau, 7)[:-1]]
    for i, (x, y, rr) in enumerate(pts):
        art = SAT(art, circles(W, H, [(x, y, rr)]), knot, GOLD_L, radial=(x - rr * 0.3, y - rr * 0.3), spacing=1.0, seed=seed + 40 + i, stitch=4, raise_=0.9, fuzz=0)
    return art


def leaf(art, W, H, x, y, L, a, col=LEAF, col2=LEAF2, seed=1, wd=0.36):
    pts = petal_pts(x, y, L, L * wd, a, n=14)
    m = shapes(W, H, [pts])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = ((xx - x) * math.sin(a) - (yy - y) * math.cos(a)) > 0
    for half, sg in ((side, 1), (~side, -1)):
        hm = m * half
        art = SAT(art, hm, col, col2, angle=a + sg * 0.75, spacing=1.4, seed=seed + (sg > 0), stitch=22, raise_=0.5, fuzz=0.3)
    return art


def cord(W, H, paths, width=3.4, seed=1):
    return couch(W, H, [(p, width) for p in paths], base=GOLD, seed=seed, width=width, twist=4.0)


def circ(cx, cy, r, n=120, a0=0, a1=math.tau):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / (n - 1)), cy + r * math.sin(a0 + (a1 - a0) * i / (n - 1))) for i in range(n)]


def shade(art, blur=3, dy=2, strength=0.5):
    """Thread shadow cast on the silk."""
    return drop_shadow(art, blur=blur, dy=dy, strength=strength, col="#02140e")


if "silk" in PARTS:
    S = 480
    nx = Seq(9100)
    art = silk(S, S, EM, "#0c5340", seed=nx(), pitch=2.0, drape=0.28, bands=1)
    preview(art, "sz-silk")
    save_full(art, f"{OUT}/silk.webp", quality=72)
    clear()

if "medallion" in PARTS:
    W = H = 640
    cx = cy = W / 2
    nx = Seq(9200)
    art = blank(W, H)
    # outer couched scalloped ring + plain ring
    scal = [(cx + (268 + 10 * math.cos(t * 24)) * math.cos(t), cy + (268 + 10 * math.cos(t * 24)) * math.sin(t)) for t in np.linspace(0, math.tau, 480)]
    art = over(art, cord(W, H, [scal], 3.2, nx()))
    art = over(art, cord(W, H, [circ(cx, cy, 246, 200)], 4.0, nx()))
    art = over(art, cord(W, H, [circ(cx, cy, 138, 160)], 3.6, nx()))
    # ring of florals and leaf pairs between r=150 and 240
    for k in range(8):
        a = -math.pi / 2 + k * math.tau / 8
        fx, fy = cx + 196 * math.cos(a), cy + 196 * math.sin(a)
        col, col2 = (IVORY, IVORY2) if k % 2 == 0 else (BLUSH, BLUSH2)
        for sg in (-1, 1):
            b = a + sg * math.pi / 8
            lx, ly = cx + 198 * math.cos(b), cy + 198 * math.sin(b)
            art = leaf(art, W, H, lx, ly, 40, b + sg * math.pi / 2 * 0.0 + math.pi / 2 * sg, seed=nx())
        art = flower(art, W, H, fx, fy, 30, 5, col, col2, rot=a, seed=nx())
    # central star: satin gold + couched outline + ivory core
    art = sat_star(art, W, H, cx, cy, 124, 62, seed=nx())
    outline_pts = []
    for (a, tip, l, r) in star_points(cx, cy, 124, 62):
        outline_pts += [l, tip]
    outline_pts.append(outline_pts[0])
    art = over(art, cord(W, H, [outline_pts], 2.4, nx()))
    art = SAT(art, fills(W, H, [ngon(cx, cy, 40, 8, math.pi / 8)]), EM_L, EM, angle=0.5, spacing=1.3, seed=nx(), stitch=24, raise_=0.4)
    art = flower(art, W, H, cx, cy, 30, 8, IVORY, IVORY2, rot=-math.pi / 2, seed=nx())
    art = shade(art)
    preview(art, "sz-medallion", bg=EM)
    save(art, f"{OUT}/medallion.webp", max_w=480, quality=82)
    clear()

if "wreath" in PARTS:
    W = H = 460
    cx = cy = W / 2
    nx = Seq(9300)
    art = blank(W, H)
    art = over(art, cord(W, H, [circ(cx, cy, 196, 200)], 3.6, nx()))
    art = over(art, cord(W, H, [circ(cx, cy, 182, 200)], 2.2, nx()))
    # leaf sprigs climbing both sides from the bottom flower to the top star
    for sg in (-1, 1):
        for k in range(9):
            t = 0.12 + k * 0.095
            a = math.pi / 2 - sg * t * math.pi
            px, py = cx + 208 * math.cos(a), cy + 208 * math.sin(a)
            tg = a - sg * math.pi / 2
            for j, off in enumerate((-0.55, 0.55)):
                art = leaf(art, W, H, cx + 196 * math.cos(a), cy + 196 * math.sin(a), 36 - k * 1.2, tg + off * sg, seed=nx(), wd=0.38)
            if k % 3 == 1:
                art = SAT(art, circles(W, H, [(cx + 196 * math.cos(a + sg * 0.05), cy + 196 * math.sin(a + sg * 0.05), 4.2)]), GOLD, GOLD_L, radial=(px, py), spacing=1.0, seed=nx(), stitch=4, fuzz=0)
    art = flower(art, W, H, cx, cy + 200, 24, 5, BLUSH, BLUSH2, rot=-math.pi / 2, seed=nx())
    art = sat_star(art, W, H, cx, cy - 200, 24, 11, seed=nx())
    art = shade(art)
    preview(art, "sz-wreath", bg=EM)
    save(art, f"{OUT}/wreath.webp", max_w=420, quality=82)
    clear()

if "spray" in PARTS:
    W, H = 520, 440
    nx = Seq(9400)
    art = blank(W, H)
    stems = [
        curve([(30, 420), (120, 330), (230, 260), (360, 190), (480, 150)], 80),
        curve([(150, 310), (170, 220), (150, 130), (110, 70)], 60),
        curve([(260, 245), (320, 300), (410, 320), (480, 300)], 60),
        curve([(360, 192), (380, 120), (430, 70)], 40),
    ]
    art = over(art, cord(W, H, stems, 3.0, nx()))
    for (x, y, L, a) in [(80, 372, 46, -2.2), (100, 360, 44, 0.3), (196, 282, 44, -2.0), (210, 270, 40, 0.75), (300, 228, 40, -2.3), (330, 214, 38, 0.6),
                         (160, 230, 36, 3.6), (156, 180, 34, -0.5), (330, 305, 34, 1.9), (390, 318, 32, -1.6), (380, 150, 30, 3.5), (420, 170, 32, 0.9)]:
        art = leaf(art, W, H, x, y, L * 1.35, a, seed=nx())
    art = flower(art, W, H, 480, 150, 40, 5, IVORY, IVORY2, rot=0.3, seed=nx())
    art = flower(art, W, H, 110, 70, 32, 5, BLUSH, BLUSH2, rot=1.0, seed=nx())
    art = flower(art, W, H, 480, 300, 28, 5, IVORY, IVORY2, rot=-0.4, seed=nx())
    art = sat_star(art, W, H, 430, 66, 22, 10, seed=nx())
    for (x, y) in [(250, 200), (280, 330), (60, 330), (200, 120)]:
        art = SAT(art, circles(W, H, [(x, y, 4)]), GOLD, GOLD_L, radial=(x - 1, y - 1), spacing=1.0, seed=nx(), stitch=4, fuzz=0)
    art = shade(art)
    preview(art, "sz-spray", bg=EM)
    save(art, f"{OUT}/spray.webp", max_w=420, quality=82)
    clear()

if "cord" in PARTS:
    # border-image frame: double couched cord with satin star knots in the corners (slice 44px of 176)
    W = H = 176
    nx = Seq(9500)
    art = blank(W, H)
    i1, i2 = 14, 24
    rect = lambda i: [(i, i), (W - i, i), (W - i, H - i), (i, H - i), (i, i)]
    art = over(art, cord(W, H, [rect(i1)], 3.4, nx()))
    art = over(art, cord(W, H, [rect(i2)], 2.0, nx()))
    for (x, y) in [(i1, i1), (W - i1, i1), (i1, H - i1), (W - i1, H - i1)]:
        art = sat_star(art, W, H, x, y, 13, 5.5, n=8, sp=1.1, seed=nx())
    art = shade(art, blur=2, dy=1, strength=0.45)
    preview(art, "sz-cord", bg=IVORY)
    save_full(art, f"{OUT}/cord.webp", quality=86)
    clear()

if "divider" in PARTS:
    W, H = 460, 80
    nx = Seq(9600)
    cy = H / 2
    art = blank(W, H)
    for sg in (-1, 1):
        wave = [(W / 2 + sg * (34 + u * 186), cy + 5 * math.sin(u * 14) * (1 - u)) for u in np.linspace(0, 1, 90)]
        art = over(art, cord(W, H, [wave], 2.6, nx()))
        art = leaf(art, W, H, W / 2 + sg * 52, cy - 2, 20, -math.pi / 2 - sg * 0.6, seed=nx())
        art = leaf(art, W, H, W / 2 + sg * 52, cy + 2, 20, math.pi / 2 + sg * 0.6, seed=nx())
    art = sat_star(art, W, H, W / 2, cy, 26, 11, seed=nx())
    art = shade(art, blur=2, dy=1)
    preview(art, "sz-divider", bg=EM)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=86)
    clear()

if "star" in PARTS:
    W = H = 120
    nx = Seq(9700)
    art = sat_star(blank(W, H), W, H, 60, 60, 50, 22, seed=nx())
    art = flower(art, W, H, 60, 60, 12, 6, IVORY, IVORY2, seed=nx())
    art = shade(art, blur=2, dy=1)
    preview(art, "sz-star", bg=EM)
    save(art, f"{OUT}/star.webp", max_w=96, quality=86)
    clear()

kb(OUT)
