"""Daun Embun — fresh morning leaves with clear dew drops, botanical watercolour: calathea (feathered dark bands),
variegated heart-leaf pothos and fern fronds, with refractive dew drops (cast shadow, inverted magnified surface,
caustic + specular). No figures, no calligraphy. Run: python3 -I daun-embun.py [part ...]
parts: atas bawah medali tetes divider sprig"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f3_lib import *

OUT = outdir("daun-embun")
PARTS = sys.argv[1:] or ["atas", "bawah", "medali", "tetes", "divider", "sprig"]
BG = "#f1f5ee"


def drops(art, masks, rng, n, rmin, rmax):
    for m in masks:
        art, _ = drop_on(art, m, n, rmin, rmax, rng)
    return art


if "atas" in PARTS:
    W, H = 840, 780
    nx = Seq(1100); rng = random.Random(11)
    art = blank(W, H)
    art, _ = fern(art, W, H, 860, -10, 720, 2.3, rng, nx, bend=-0.3, pin=0.14)
    art, _ = fern(art, W, H, 860, 120, 560, 2.95, rng, nx, bend=0.25, pin=0.15, cols=("#94c873", "#3c8646"))
    art, _ = fern(art, W, H, 560, -30, 430, 1.9, rng, nx, bend=0.3, pin=0.16)
    art, m5, _ = paint_leaf(art, W, H, 850, 330, 300, 72, 2.75, rng, nx, "plain", bend=0.3, cols=("#8fc4a0", "#3f8a6a", "#1c4d3c", "#dff0d8"))
    art, m1, _ = paint_leaf(art, W, H, 850, 40, 560, 128, 2.5, rng, nx, "calathea", bend=0.3)
    art, m2, _ = paint_leaf(art, W, H, 660, -30, 320, 112, 2.0, rng, nx, "pothos", bend=-0.3)
    clear()
    art, m3, _ = paint_leaf(art, W, H, 860, 210, 400, 96, 3.0, rng, nx, "calathea", bend=-0.25, shade=0.8)
    art, m4, _ = paint_leaf(art, W, H, 830, -20, 250, 92, 1.75, rng, nx, "pothos", bend=0.25)
    for m, n_, a_, b_ in ((m1, 6, 10, 26), (m3, 4, 8, 18), (m2, 3, 8, 18), (m4, 2, 7, 15), (m5, 2, 6, 12)):
        art, _ = drop_on(art, m, n_, a_, b_, rng)
    clear()
    prev(art, "atas", tone=BG)
    save(art, f"{OUT}/atas.webp", max_w=640, quality=80)

if "bawah" in PARTS:
    W, H = 760, 560
    nx = Seq(2100); rng = random.Random(21)
    art = blank(W, H)
    art, f1 = fern(art, W, H, -30, 580, 640, -0.5, rng, nx, bend=-0.3, pin=0.14)
    art, f2 = fern(art, W, H, 120, 600, 440, -1.2, rng, nx, bend=0.35, pin=0.16, cols=("#94c873", "#3c8646"))
    art, f3 = fern(art, W, H, -20, 420, 380, -0.12, rng, nx, bend=0.2, pin=0.15)
    art, m1, _ = paint_leaf(art, W, H, -20, 520, 470, 125, -0.42, rng, nx, "calathea", bend=-0.3)
    art, m2, _ = paint_leaf(art, W, H, 60, 600, 300, 110, -1.05, rng, nx, "pothos", bend=0.25)
    clear()
    art, m3, _ = paint_leaf(art, W, H, 220, 610, 230, 80, -1.45, rng, nx, "plain", bend=0.2)
    for m, n_, a_, b_ in ((m1, 6, 8, 20), (m2, 3, 7, 16), (m3, 2, 6, 12)):
        art, _ = drop_on(art, m, n_, a_, b_, rng)
    clear()
    prev(art, "bawah", tone=BG)
    save(art, f"{OUT}/bawah.webp", max_w=560, quality=80)

if "medali" in PARTS:
    W = H = 520
    nx = Seq(3100); rng = random.Random(31)
    art = blank(W, H)
    cx, cy, R = W / 2, H / 2 + 6, 196
    # two fern fronds sweeping up the ring from the bottom
    for sg in (-1, 1):
        a0 = math.pi / 2 + sg * 0.32
        a1 = math.pi / 2 + sg * (math.pi * 0.98)
        rib = [(cx + math.cos(a0 + (a1 - a0) * t) * R, cy + math.sin(a0 + (a1 - a0) * t) * R) for t in np.linspace(0, 1, 70)]
        art, _ = fern(art, W, H, 0, 0, 0, 0, rng, nx, rib=rib, pin=0.075, cols=("#86c26a", "#2f7a3e"))
    clear()
    leaves = []
    for k, (da, L, Wd, kind) in enumerate(((-0.55, 110, 40, "pothos"), (0.55, 104, 38, "pothos"), (-0.18, 120, 34, "calathea"), (0.2, 116, 32, "calathea"))):
        bx, by = cx + (8 if da > 0 else -8), cy + R + 8
        art, m, _ = paint_leaf(art, W, H, bx, by, L, Wd, -math.pi / 2 + da * 2.2 + (math.pi if False else 0), rng, nx, kind, bend=0.2 * (1 if da > 0 else -1))
        leaves.append(m)
    clear()
    for m in leaves[:3]:
        art, _ = drop_on(art, m, 1, 5, 8, rng, keep=0.95)
    prev(art, "medali", tone=BG)
    save(art, f"{OUT}/medali.webp", max_w=440, quality=82)

if "tetes" in PARTS:
    d = lone_drop(40, seed=4)
    prev(d, "tetes", tone=BG)
    save(d, f"{OUT}/tetes.webp", max_w=72, quality=86)

if "divider" in PARTS:
    W, H = 520, 120
    nx = Seq(4100); rng = random.Random(41)
    art = blank(W, H)
    for sg in (-1, 1):
        rib = [(W / 2 + sg * (14 + t * 230), H / 2 + 6 - math.sin(t * math.pi) * 12 * 1 + t * 4) for t in np.linspace(0, 1, 50)]
        art, _ = fern(art, W, H, 0, 0, 0, 0, rng, nx, rib=rib, pin=0.09)
    art, m, _ = paint_leaf(art, W, H, W / 2, H / 2 + 14, 62, 22, -math.pi / 2 - 0.5, rng, nx, "pothos", bend=0.1)
    art, m2, _ = paint_leaf(art, W, H, W / 2, H / 2 + 14, 58, 20, -math.pi / 2 + 0.5, rng, nx, "pothos", bend=-0.1)
    art = dew(art, W / 2 - 14, H / 2 - 18, 6, rng)
    prev(art, "divider", tone=BG)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=82)

if "sprig" in PARTS:
    W, H = 300, 380
    nx = Seq(5100); rng = random.Random(51)
    art = blank(W, H)
    art, f = fern(art, W, H, 150, 370, 330, -1.62, rng, nx, bend=0.3, pin=0.17)
    art, m, _ = paint_leaf(art, W, H, 150, 372, 210, 70, -1.2, rng, nx, "calathea", bend=-0.2)
    art, _ = drop_on(art, m, 3, 6, 12, rng)
    prev(art, "sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=220, quality=82)
