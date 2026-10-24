"""Sakura Syari — soft pink cherry-blossom branches in loose watercolour on pale cream (syar'i, no figures).
Run: python3 -I sakura-syari.py [part ...]  parts: branch petal sprig bloom wash spray
Assets -> public/themes/art/sakura-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q6_lib import *

OUT = outdir("sakura-syari")
PARTS = sys.argv[1:] or ["branch", "petal", "sprig", "bloom", "wash", "spray"]


def leaf_young(art, W, H, x, y, L, ang, rng, nx):
    m = shapes(W, H, [deform(petal_pts(x, y, L, L * 0.3, ang, n=14), rng, 1, 0.03)])
    art = G(art, m, "#a9a66a", "#7f8a52", seed=nx(), density=0.6, edge=0.5, bloom=0.3, rough=1.5, feather=0.9)
    art = OV(art, strokes(W, H, [([(x, y), (x + math.cos(ang) * L * 0.9, y + math.sin(ang) * L * 0.9)], 1.4, (0.0, 0.4))]) * m, lambda q: flat(q, "#6a6a3a", 0.5))
    tip = shapes(W, H, [petal_pts(x + math.cos(ang) * L * 0.45, y + math.sin(ang) * L * 0.45, L * 0.55, L * 0.3, ang, n=8)])
    art = G(art, tip * m, "#c48a6a", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=2, feather=1.4)
    return art


def cluster(art, W, H, pts, rng, nx, r=34, area=None, buds=2, tones=None):
    for i, (x, y) in enumerate(pts):
        rr = r * rng.uniform(0.8, 1.15)
        t = tones[i % len(tones)] if tones else ("#fbe3e8", "#f2b6c4", "#cf7290")
        art, a = blossom(art, W, H, x, y, rr, rng, nx, *t, tilt=rng.uniform(0.7, 1.0))
        if area is not None:
            area[:] = np.maximum(area, a)
    for k in range(buds):
        x, y = pts[k % len(pts)]
        ang = rng.uniform(-2.8, -0.4)
        art = sakura_bud(art, W, H, x + math.cos(ang) * r * 1.5, y + math.sin(ang) * r * 1.5, r * 0.5, ang, rng, nx)
    return art


TONES = [("#fce6ea", "#f4bccb", "#d07a95"), ("#fbe9ec", "#efc2cd", "#c9748e"), ("#fde2e2", "#f5b3bd", "#d36f86"), ("#fbeef0", "#f1cbd4", "#c98399")]


def branch():
    W, H = 820, 720
    rng = random.Random(11); nx = Seq(300)
    wood = blank(W, H)
    main = curve([(830, 30), (640, 70), (470, 150), (300, 250), (140, 320), (40, 350)], 40)
    wood = bark_branch(wood, W, H, main, 30, rng, nx)
    subs = [curve([(560, 100), (520, 40), (430, 18)], 16), curve([(420, 175), (380, 260), (330, 330), (300, 420)], 20),
            curve([(260, 270), (200, 220), (120, 210)], 16), curve([(640, 70), (610, 140), (630, 220)], 14),
            curve([(330, 330), (390, 400), (420, 470)], 14)]
    for sp, w in zip(subs, (12, 13, 10, 9, 8)):
        wood = bark_branch(wood, W, H, sp, w, rng, nx)
    flowers = blank(W, H)
    area = np.zeros((H, W), np.float32)
    flowers = cluster(flowers, W, H, [(470, 92), (520, 125), (575, 158), (612, 112), (540, 70), (500, 178)], rng, nx, r=44, area=area, buds=3, tones=TONES)
    flowers = cluster(flowers, W, H, [(320, 296), (368, 340), (292, 404), (342, 444), (404, 404), (262, 350)], rng, nx, r=42, area=area, buds=3, tones=TONES[1:])
    flowers = cluster(flowers, W, H, [(150, 236), (204, 296), (108, 286), (170, 190)], rng, nx, r=36, area=area, buds=2, tones=TONES[2:])
    flowers = cluster(flowers, W, H, [(420, 24), (690, 52), (640, 232), (432, 490), (740, 90)], rng, nx, r=32, area=area, buds=2, tones=TONES)
    flowers = cluster(flowers, W, H, [(60, 345), (236, 262), (760, 40)], rng, nx, r=26, area=area, buds=1, tones=TONES[1:])
    lv = blank(W, H)
    for x, y, L, a in [(650, 75, 70, -1.9), (300, 270, 66, 2.5), (226, 330, 56, 1.9)]:
        lv = leaf_young(lv, W, H, x, y, L, a, rng, nx)
    wood = knockout(wood, area, amount=0.85, grow=3)
    lv = knockout(lv, area, amount=0.9, grow=3)
    art = glaze(glaze(wood, lv), flowers)
    # loose spatter of pale pink
    sp = circles(W, H, [(rng.uniform(80, 760), rng.uniform(40, 560), rng.uniform(1.5, 4)) for _ in range(40)])
    art = G(art, sp, "#f0b4c2", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1, feather=0.6)
    preview(art, "sakura-branch", "#fbf6ef")
    save(art, f"{OUT}/branch.webp", max_w=760, quality=80)


def petal():
    W, H = 120, 120
    rng = random.Random(5); nx = Seq(40)
    art = blank(W, H)
    pts = [(x, y * 0.8) for x, y in sakura_petal_pts(18, 60, 86, 0.0, notch=0.2, wid=0.72)]
    pts = rotp(pts, 60, 60, -0.5)
    m = shapes(W, H, [pts])
    art = G(art, m, "#fbdde4", "#f0afc0", seed=nx(), density=0.65, edge=0.6, bloom=0.3, rough=2, feather=0.9)
    base = shapes(W, H, [rotp([(x, y * 0.8) for x, y in sakura_petal_pts(18, 60, 40, 0.0, wid=0.5)], 60, 60, -0.5)])
    art = G(art, base, "#e58aa4", seed=nx(), density=0.35, edge=0.2, rough=1, feather=2)
    preview(art, "sakura-petal", "#fbf6ef")
    save(art, f"{OUT}/petal.webp", max_w=56, quality=82)


def sprig():
    W, H = 760, 120
    rng = random.Random(21); nx = Seq(500)
    wood = blank(W, H)
    wood = bark_branch(wood, W, H, curve([(80, 66), (250, 58), (420, 64), (560, 58), (690, 50)], 30), 7, rng, nx)
    wood = bark_branch(wood, W, H, curve([(300, 60), (340, 36), (380, 28)], 12), 4, rng, nx)
    fl = blank(W, H); area = np.zeros((H, W), np.float32)
    fl = cluster(fl, W, H, [(380, 58), (428, 50), (334, 68)], rng, nx, r=34, area=area, buds=2, tones=TONES)
    for x, y in [(160, 62), (600, 58)]:
        fl, a = blossom(fl, W, H, x, y, 24, rng, nx, *TONES[1], tilt=0.8)
        area = np.maximum(area, a)
    fl = sakura_bud(fl, W, H, 700, 48, 14, -0.3, rng, nx)
    fl = sakura_bud(fl, W, H, 84, 66, 13, 3.0, rng, nx)
    wood = knockout(wood, area, amount=0.85, grow=2)
    art = glaze(wood, fl)
    preview(art, "sakura-sprig", "#fbf6ef")
    save(art, f"{OUT}/sprig.webp", max_w=380, quality=82)


def bloom():
    W, H = 260, 260
    rng = random.Random(33); nx = Seq(700)
    art = blank(W, H)
    art = bark_branch(art, W, H, curve([(20, 200), (90, 160), (160, 140)], 16), 7, rng, nx)
    art, _ = blossom(art, W, H, 140, 120, 78, rng, nx, *TONES[0], tilt=0.95, rot=-1.2)
    art = sakura_bud(art, W, H, 60, 175, 24, -2.4, rng, nx)
    preview(art, "sakura-bloom", "#fbf6ef")
    save(art, f"{OUT}/bloom.webp", max_w=160, quality=82)


def wash():
    """Pale pink moon wash (behind the cover names): wet-in-wet disc with a soft bloom and uneven edge."""
    W, H = 640, 640
    rng = random.Random(4); nx = Seq(900)
    art = blank(W, H)
    disc = shapes(W, H, [deform(ellipse_pts(320, 320, 270, 270, 16), rng, 2, 0.04)])
    art = G(art, disc, "#fbe3e7", "#f8d4dc", seed=nx(), density=0.55, edge=0.45, bloom=0.55, rough=10, feather=3, gran=0.15)
    inner = shapes(W, H, [deform(ellipse_pts(300, 340, 170, 150, 12), rng, 2, 0.1)])
    art = G(art, inner, "#f9dbe2", "#f6ccd6", seed=nx(), density=0.22, edge=0.15, bloom=0.4, rough=14, feather=8)
    preview(art, "sakura-wash", "#fbf6ef")
    save(art, f"{OUT}/wash.webp", max_w=400, quality=62)


def spray():
    """Small corner spray for the closing / countdown band (lower-left, rising)."""
    W, H = 520, 420
    rng = random.Random(61); nx = Seq(1100)
    wood = blank(W, H)
    wood = bark_branch(wood, W, H, curve([(-10, 410), (90, 330), (200, 260), (330, 210), (470, 190)], 30), 18, rng, nx)
    wood = bark_branch(wood, W, H, curve([(200, 262), (230, 170), (290, 110)], 16), 8, rng, nx)
    fl = blank(W, H); area = np.zeros((H, W), np.float32)
    fl = cluster(fl, W, H, [(300, 200), (340, 230), (260, 230), (470, 188), (420, 170)], rng, nx, r=40, area=area, buds=2, tones=TONES)
    fl = cluster(fl, W, H, [(286, 110), (240, 150), (120, 320)], rng, nx, r=34, area=area, buds=1, tones=TONES[2:])
    lv = blank(W, H)
    for x, y, L, a in [(380, 200, 50, -0.6), (230, 200, 44, -2.2)]:
        lv = leaf_young(lv, W, H, x, y, L, a, rng, nx)
    wood = knockout(wood, area, amount=0.85, grow=3)
    lv = knockout(lv, area, amount=0.9, grow=3)
    art = glaze(glaze(wood, lv), fl)
    preview(art, "sakura-spray", "#fbf6ef")
    save(art, f"{OUT}/spray.webp", max_w=360, quality=80)


for p in PARTS:
    globals()[p]()
    clear()
