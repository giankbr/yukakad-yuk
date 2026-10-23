"""Ultah Peri — kids' birthday in a twilight fairy forest: glowing toadstools, bell flowers, ferns and dark trunks
(watercolour + gouache + glow), an original little fairy (Kiki) with petal dress and dragonfly wings, a toadstool
emblem, and a vine divider with glowing bells. Run: python3 -I ultah-peri.py [part ...]
parts: hutan peri jamur sulur. Assets -> public/themes/art/ultah-peri/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h2_lib import *

OUT = outdir("ultah-peri")
PARTS = sys.argv[1:] or ["hutan", "peri", "jamur", "sulur"]
DUSK = "#2a2452"
CAP, CAP_D, CAP_L = "#e2536b", "#a8324d", "#f59aa8"
STEM, STEM_D = "#f3e6d2", "#c9b39a"
GLOW = "#ffd98a"


def toadstool(art, W, H, x, by, h, w, nx, rng, tilt=0.0, glow_amt=0.8, cap=(CAP, CAP_D, CAP_L)):
    """Fly-agaric-ish toadstool: cream stem with skirt, domed red cap with cream spots, warm glow under the cap."""
    top = by - h
    stem = shapes(W, H, [[(x - w * 0.12, by - h * 0.06), (x - w * 0.085 + tilt * h * 0.05, top + h * 0.5), (x - w * 0.07 + tilt * h * 0.2, top + h * 0.2), (x + w * 0.07 + tilt * h * 0.2, top + h * 0.2), (x + w * 0.09 + tilt * h * 0.05, top + h * 0.5), (x + w * 0.12, by - h * 0.06)],
                         deform(ellipse_pts(x, by - h * 0.05, w * 0.15, h * 0.075, 14), rng, 1, 0.05)])
    art = GP(art, stem, STEM, STEM_D, seed=nx(), rough=2, streak=0.8, pad=10)
    shade = stem * np.clip((np.mgrid[0:H, 0:W][1] - x) / (w * 0.13), 0, 1)
    art = G(art, shade, "#8f7ea8", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1.5)
    skirt = shapes(W, H, [[(x - w * 0.12, top + h * 0.42), (x + w * 0.12, top + h * 0.42), (x + w * 0.2, top + h * 0.55), (x, top + h * 0.5), (x - w * 0.2, top + h * 0.55)]])
    art = GP(art, skirt, "#fbf3e6", "#e0cdb5", seed=nx(), rough=1.5, pad=8)
    # glow under the cap
    under = shapes(W, H, [deform(ellipse_pts(x + tilt * h * 0.2, top + h * 0.2, w * 0.46, h * 0.08, 16), rng, 1, 0.05)])
    art = over(art, glow(under, GLOW, radius=w * 0.12, strength=glow_amt * 0.6))
    gills = shapes(W, H, [deform(ellipse_pts(x + tilt * h * 0.2, top + h * 0.2, w * 0.47, h * 0.06, 18), rng, 1, 0.05)])
    art = GP(art, gills, "#f7d6a8", "#e6b783", seed=nx(), rough=1.2, pad=8)
    cx = x + tilt * h * 0.25
    capp = [(cx - w * 0.5, top + h * 0.2)] + [(cx + math.cos(a) * w * 0.5, top + h * 0.2 + math.sin(a) * h * 0.42) for a in np.linspace(math.pi, math.tau, 22)] + [(cx + w * 0.5, top + h * 0.2), (cx, top + h * 0.26)]
    cm = shapes(W, H, [capp])
    art = GP(art, cm, cap[0], cap[1], seed=nx(), rough=2.5, streak=0.9, pad=10)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hl = cm * np.clip(1 - np.sqrt(((xx - cx + w * 0.16) / (w * 0.3)) ** 2 + ((yy - top - h * 0.02) / (h * 0.18)) ** 2), 0, 1)
    art = G(art, hl, cap[2], seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=3)
    rim = cm * np.clip((yy - (top + h * 0.12)) / (h * 0.1), 0, 1)
    art = G(art, rim, cap[1], seed=nx(), density=0.45, edge=0.2, bloom=0, rough=2)
    spots = []
    for (u, v) in [(-0.62, 0.22), (-0.3, 0.55), (0.05, 0.78), (0.4, 0.52), (0.7, 0.2), (-0.05, 0.32), (-0.75, 0.05), (0.78, 0.0), (0.25, 0.18)]:
        u += rng.uniform(-0.05, 0.05); v += rng.uniform(-0.04, 0.04)
        px, py = cx + u * w * 0.5, top + h * 0.2 - v * h * 0.4
        spots.append(deform(ellipse_pts(px, py, w * rng.uniform(0.035, 0.07), w * rng.uniform(0.028, 0.05), 9), rng, 1, 0.15))
    art = GP(art, shapes(W, H, spots) * cm, "#fff6ea", "#f1dcc6", seed=nx(), rough=1, pad=8)
    return art


def bell(art, W, H, x, y, r, ang, nx, rng, col="#c9b8f2", col2="#8f7ad6"):
    """Glowing bell flower hanging from a stem point."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for t in np.linspace(0, 1, 14):
        pts.append((x + (-r * 0.55 * (0.5 + t * 0.6)) * ca * 0 + (-r * (0.35 + 0.4 * t)), y + t * r * 1.2))
    left = [(x - r * (0.3 + 0.5 * t ** 1.4), y + t * r * 1.15) for t in np.linspace(0, 1, 10)]
    right = [(x + r * (0.3 + 0.5 * t ** 1.4), y + t * r * 1.15) for t in np.linspace(0, 1, 10)]
    lip = [(x + r * 0.8 - k * r * 0.4, y + r * 1.15 + (r * 0.14 if k % 2 else 0)) for k in range(5)]
    poly = left + lip[::-1][::-1] + right[::-1]
    poly = rot_pts(left + lip + right[::-1], x, y, ang)
    m = shapes(W, H, [poly])
    art = over(art, glow(m, "#efe6ff", radius=r * 0.6, strength=0.55))
    art = G(art, m, col, col2, seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=2)
    return art


if "hutan" in PARTS:
    W, H = 820, 720
    nx = Seq(6100); rng = random.Random(61)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # far trunks (dusk indigo washes), fading upward
    tr = []
    for x, wd in [(40, 46), (150, 26), (260, 34), (560, 30), (680, 50), (790, 30), (420, 20)]:
        tr.append(([(x + rng.uniform(-10, 10), 0), (x + rng.uniform(-14, 14), H * 0.5), (x + rng.uniform(-6, 6), H * 0.8)], wd, None))
    trunks = strokes(W, H, [(curve(p, 20), w_, t) for p, w_, t in tr])
    art = G(art, trunks * np.clip(yy / H * 2.2, 0, 1), "#3b3570", "#2f2a60", seed=nx(), density=0.75, edge=0.5, bloom=0.4, rough=6)
    # rolling mossy mounds
    art = G(art, hills(W, H, 520, 30, 4, 0.7), "#4d6f92", "#40607f", seed=nx(), density=0.8, edge=0.5, bloom=0.4, rough=8)
    art = G(art, hills(W, H, 590, 24, 6, 0.5), "#3b7070", "#326062", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=6)
    # ferns (curling fronds) on both sides
    fr = []
    for (x0, y0, L, a, sgn) in [(30, 640, 230, -1.2, 1), (110, 650, 180, -1.5, 1), (790, 640, 230, -1.9, -1), (700, 660, 170, -1.6, -1), (380, 680, 120, -1.7, 1)]:
        stem = curve([(x0, y0), (x0 + math.cos(a) * L * 0.5, y0 + math.sin(a) * L * 0.5), (x0 + math.cos(a + sgn * 0.5) * L, y0 + math.sin(a + sgn * 0.5) * L)], 30)
        fr.append((stem, 4, (0.0, 0.5)))
        for k, (px, py, pa) in enumerate(along(stem, 12)):
            ll = 30 * (1 - k / 22)
            for s_ in (1, -1):
                fr.append(([(px, py), (px + math.cos(pa + s_ * 1.2) * ll, py + math.sin(pa + s_ * 1.2) * ll)], 5 * (1 - k / 26), (0.1, 0.6)))
    ferns = strokes(W, H, fr)
    art = GP(art, ferns, "#4f9a84", "#3b7f70", seed=nx(), rough=1.2, streak=0.8, density=0.9)
    # toadstools
    art = toadstool(art, W, H, 300, 640, 230, 260, nx, rng, tilt=-0.08, glow_amt=1.0)
    art = toadstool(art, W, H, 520, 660, 150, 170, nx, rng, tilt=0.1, glow_amt=0.8, cap=("#f08a5d", "#c2563a", "#ffc29a"))
    art = toadstool(art, W, H, 640, 676, 86, 104, nx, rng, tilt=0.05, glow_amt=0.6)
    art = toadstool(art, W, H, 170, 676, 70, 82, nx, rng, tilt=-0.1, glow_amt=0.5, cap=("#b58ae0", "#7c58b8", "#dcc2f6"))
    # bell flower stalks
    for (x0, h, cnt) in [(90, 260, 4), (735, 300, 5), (430, 180, 3)]:
        st = curve([(x0, 690), (x0 + 10, 690 - h * 0.5), (x0 + 34, 690 - h)], 30)
        art = G(art, strokes(W, H, [(st, 3.5, (0.0, 0.4))]), "#3f6f62", seed=nx(), density=0.9, edge=0.3, rough=1)
        for k in range(cnt):
            px, py = st[int(8 + k * (20 / cnt))]
            art = bell(art, W, H, px + 10, py, 24 - k * 2, 0.3, nx, rng, col=["#c9b8f2", "#a9e4d6", "#ffd3e2"][k % 3], col2=["#8f7ad6", "#5fb5a2", "#e58bb0"][k % 3])
    # moss ground front
    art = G(art, shapes(W, H, [[(0, 690), (W, 680), (W, H), (0, H)]], smooth=False), "#24474a", "#1f3c44", seed=nx(), density=0.95, edge=0.4, bloom=0.3, rough=6)
    grass = strokes(W, H, [([(x, 700), (x + rng.uniform(-8, 8), 700 - rng.uniform(14, 34))], rng.uniform(1.5, 3), (0.0, 0.7)) for x in rng.sample(range(0, W), 160)])
    art = G(art, grass, "#3d7466", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
    art[..., 3] *= np.clip(yy / (H * 0.25), 0, 1)
    preview(art, "up-hutan", bg=DUSK)
    save(art, f"{OUT}/hutan.webp", max_w=720, quality=78)
    clear()

if "peri" in PARTS:
    # Kiki the fairy: hovering, petal dress, dragonfly wings, holding a glowing seed-light. Original character.
    W, H = 340, 420
    nx = Seq(6200); rng = random.Random(62)
    art = blank(W, H)
    cx, cy = 170, 210
    # wings (behind): four translucent lobes with veins
    wings = []
    for sgn in (-1, 1):
        wings.append(petal_pts(cx + sgn * 10, cy - 20, 130, 46, -math.pi / 2 + sgn * 1.0, n=16))
        wings.append(petal_pts(cx + sgn * 8, cy + 4, 96, 34, -math.pi / 2 + sgn * 1.75, n=16))
    wm = shapes(W, H, wings)
    art = over(art, glow(wm, "#dff7ff", radius=10, strength=0.35))
    art = G(art, wm, "#bfeef0", "#d7ccf6", seed=nx(), density=0.45, edge=0.85, bloom=0.5, rough=2)
    veins = []
    for sgn in (-1, 1):
        for a, L in [(-math.pi / 2 + sgn * 1.0, 120), (-math.pi / 2 + sgn * 1.75, 86)]:
            veins.append(([(cx + sgn * 10, cy - 14), (cx + sgn * 10 + math.cos(a) * L, cy - 14 + math.sin(a) * L)], 1.2, (0.0, 0.4)))
    art = G(art, strokes(W, H, veins), "#8ab7c9", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    # legs
    legs = strokes(W, H, [(curve([(cx - 10, cy + 70), (cx - 16, cy + 110), (cx - 26, cy + 140)], 12), 8, (0.0, 0.2)), (curve([(cx + 10, cy + 70), (cx + 18, cy + 104), (cx + 14, cy + 136)], 12), 8, (0.0, 0.2))])
    art = GP(art, legs, "#f2c6a6", "#e0a988", seed=nx(), rough=1, pad=8)
    shoes = shapes(W, H, [deform(ellipse_pts(cx - 30, cy + 142, 11, 6, 10, -0.3), rng, 1, 0.1), deform(ellipse_pts(cx + 12, cy + 140, 11, 6, 10, 0.3), rng, 1, 0.1)])
    art = GP(art, shoes, "#7a58b8", seed=nx(), rough=1, pad=6)
    # petal dress: layered petals pointing down
    dress = []
    for k in range(7):
        a = math.pi / 2 + (k - 3) * 0.32
        dress.append(petal_pts(cx, cy + 6, 78, 26, a, n=14))
    dm = shapes(W, H, dress)
    art = GP(art, dm, "#f59ab9", "#e06a98", seed=nx(), rough=1.8, streak=0.8, pad=8)
    inner = shapes(W, H, [petal_pts(cx, cy + 6, 58, 20, math.pi / 2 + (k - 2) * 0.3, n=12) for k in range(5)])
    art = GP(art, inner, "#ffc6d8", "#f59ab9", seed=nx(), rough=1.4, pad=8)
    torso = shapes(W, H, [[(cx - 20, cy - 30), (cx + 20, cy - 30), (cx + 18, cy + 14), (cx - 18, cy + 14)]])
    art = GP(art, torso, "#9ad8c4", "#6fbea7", seed=nx(), rough=1.2, pad=8)
    # arms: one raised holding the seed-light
    arms = strokes(W, H, [(curve([(cx - 18, cy - 24), (cx - 44, cy - 2), (cx - 52, cy + 22)], 12), 8, (0.0, 0.2)),
                          (curve([(cx + 18, cy - 24), (cx + 48, cy - 44), (cx + 66, cy - 78)], 12), 8, (0.0, 0.2))])
    art = GP(art, arms, "#f2c6a6", "#e0a988", seed=nx(), rough=1, pad=8)
    wand = strokes(W, H, [([(cx + 64, cy - 74), (cx + 82, cy - 130)], 3.5, (0.0, 0.0))])
    art = GP(art, wand, "#8a6a4a", seed=nx(), rough=0.6, pad=6)
    orb = circles(W, H, [(cx + 84, cy - 138, 10)])
    art = over(art, glow(orb, GLOW, radius=16, strength=0.9))
    art = GP(art, orb, "#fff4c8", "#ffe08a", seed=nx(), rough=0.8, pad=6)
    # head, hair, face
    head = shapes(W, H, [deform(ellipse_pts(cx, cy - 66, 38, 36, 16), rng, 1, 0.03)])
    art = GP(art, head, "#f6d0b2", "#eab896", seed=nx(), rough=1.2, pad=8)
    hair = shapes(W, H, [[(cx - 42, cy - 58), (cx - 44, cy - 84), (cx - 30, cy - 104), (cx, cy - 110), (cx + 30, cy - 104), (cx + 44, cy - 84), (cx + 42, cy - 56), (cx + 30, cy - 76), (cx + 6, cy - 86), (cx - 16, cy - 78), (cx - 30, cy - 70)]])
    art = GP(art, hair, "#4a2f2a", "#5e3a30", seed=nx(), rough=1.4, streak=1.0, pad=8)
    # leaf cap
    leafcap = shapes(W, H, [petal_pts(cx + 4, cy - 104, 46, 16, -math.pi / 2 + 0.5, n=12), petal_pts(cx - 4, cy - 104, 40, 14, -math.pi / 2 - 0.6, n=12)])
    art = GP(art, leafcap, "#7cc48f", "#4f9a6a", seed=nx(), rough=1.2, pad=6)
    eyes = circles(W, H, [(cx - 13, cy - 62, 3.6), (cx + 13, cy - 62, 3.6)])
    art = GP(art, eyes, "#2a1c1c", seed=nx(), rough=0.3, pad=4)
    blush = circles(W, H, [(cx - 22, cy - 50, 7), (cx + 22, cy - 50, 7)])
    art = G(art, blush, "#f08aa0", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1.5)
    smile = strokes(W, H, [(arc_pts(cx, cy - 54, 7, 0.4, math.pi - 0.4, 10), 2.0, (0.2, 0.2))])
    art = GP(art, smile, "#9a4a4a", seed=nx(), rough=0.3, pad=4)
    preview(art, "up-peri", bg=DUSK)
    save(art, f"{OUT}/peri.webp", max_w=260, quality=84)
    clear()

if "jamur" in PARTS:
    W, H = 300, 300
    nx = Seq(6300); rng = random.Random(63)
    art = blank(W, H)
    art = G(art, shapes(W, H, [deform(ellipse_pts(150, 268, 120, 20, 14), rng, 1, 0.1)]), "#4c8a7a", "#2f6a62", seed=nx(), density=0.8, edge=0.5, rough=3)
    art = toadstool(art, W, H, 150, 266, 196, 236, nx, rng, glow_amt=0.9)
    art = toadstool(art, W, H, 236, 272, 70, 76, nx, rng, tilt=0.1, glow_amt=0.4, cap=("#b58ae0", "#7c58b8", "#dcc2f6"))
    preview(art, "up-jamur", bg="#f3effa")
    save(art, f"{OUT}/jamur.webp", max_w=220, quality=84)
    clear()

if "sulur" in PARTS:
    W, H = 760, 140
    nx = Seq(6400); rng = random.Random(64)
    art = blank(W, H)
    vine = curve([(20, 70), (140, 50), (260, 84), (380, 60), (500, 86), (620, 56), (740, 72)], 120)
    art = G(art, strokes(W, H, [(vine, 5, (0.05, 0.05))]), "#4f9a7a", "#3f7f6a", seed=nx(), density=0.9, edge=0.4, rough=1)
    lv = []
    for k, (x, y, a) in enumerate(along(vine, 34)):
        off = 1 if k % 2 else -1
        lv.append(petal_pts(x, y, 36, 13, a + off * 1.0, n=10))
    art = G(art, shapes(W, H, lv), "#7cc48f", "#4f9a6a", seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=2)
    for k, x in enumerate((130, 250, 380, 510, 630)):
        y = [p for p in vine if abs(p[0] - x) < 4][0][1]
        art = bell(art, W, H, x, y + 4, 22, 0.0 + (0.2 if k % 2 else -0.2), nx, rng, col=["#c9b8f2", "#ffd3e2", "#a9e4d6"][k % 3], col2=["#8f7ad6", "#e58bb0", "#5fb5a2"][k % 3])
    preview(art, "up-sulur", bg="#f3effa")
    save(art, f"{OUT}/sulur.webp", max_w=420, quality=82)
    clear()
