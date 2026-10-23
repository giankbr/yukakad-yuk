"""Kertas Quilling — paper quilling on cotton card: strips of coloured paper rolled into loose coils, pinched into
teardrops and marquises, husked leaves, fringed flowers and open scrolls, every strip standing on edge with a lit top
edge and a soft cast shadow (light from the top-left). Pieces: a crescent wreath (frames the monogram), a corner spray,
a scroll divider, a single bloom, and a cotton-card tile.
Run: python3 -I kertas-quilling.py [part ...]  parts: wreath corner divider bloom card"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k6_lib import *

OUT = outdir("kertas-quilling")
PARTS = sys.argv[1:] or ["wreath", "corner", "divider", "bloom", "card"]
ROSE, ROSE_L, CORAL, MUSTARD, SAGE, SAGE_D, TEAL, LAV, CREAM = "#cf6f80", "#eea7b2", "#ec916f", "#e0ac45", "#8fae8b", "#5f8a6a", "#4f8c8a", "#9a8cc4", "#f3e6c8"
nx = Seq(1300)


def flower_a(art, W, H, x, y, R, rot=0.0):
    """Rose-pink double flower: outer teardrops, inner light teardrops, mustard tight-coil centre."""
    return quill_flower(art, W, H, x, y, R, [ROSE], MUSTARD, nx, petals=7, rot=rot, shape="tear", inner=ROSE_L)


def flower_b(art, W, H, x, y, R, rot=0.0):
    """Coral flower of eye-shaped petals."""
    return quill_flower(art, W, H, x, y, R, [CORAL, "#f2a786"], CREAM, nx, petals=6, rot=rot, shape="eye")


def aster(art, W, H, x, y, R, col=LAV, centre=MUSTARD):
    art = fringe_flower(art, W, H, x, y, R, col, nx, n=int(R * 0.9))
    return quill_coil(art, W, H, x, y, R * 0.3, centre, seed=nx(), off=0.0)


def bud(art, W, H, x, y, r, ang, col=ROSE):
    art = quill_coil(art, W, H, x, y, r, col, seed=nx(), shape="tear", ang=ang, turns=r / 5.5)
    # little sepal
    return quill_coil(art, W, H, x - math.cos(ang) * r * 0.9, y - math.sin(ang) * r * 0.9, r * 0.45, SAGE, seed=nx(), shape="marquise", ang=ang + 1.57, turns=2.5)


def scroll(art, W, H, x0, y0, x1, y1, r, side=1, col=SAGE_D):
    return quill_line(art, W, H, scroll_pts(x0, y0, x1, y1, r, 1.7, side), col, seed=nx())


def wreath():
    W = H = 780; C = 390; Rr = 250
    bg = blank(W, H)
    art = bg
    # double ring strips
    for r, col in ((240, MUSTARD), (249, ROSE_L)):
        pts = arc_pts(C, C, r, 0, math.tau, 300) + [(C + r, C)]
        art = quill_line(art, W, H, pts, col, seed=nx(), width=4.4)
    rng = random.Random(nx())
    # leaves along the ring, tangential, alternating in/out
    for k, deg in enumerate(range(-74, 262, 9)):
        if any(abs(deg - f) < 13 for f in (110, 60, 165, 18, 212)):
            continue
        a = math.radians(deg)
        side = 1 if k % 2 else -1
        rr = Rr + side * 17
        x, y = C + math.cos(a) * rr, C + math.sin(a) * rr
        ang = a + math.pi / 2 + side * 0.55 + rng.uniform(-0.15, 0.15)
        L = rng.uniform(54, 68) * (0.75 if deg < -30 or deg > 230 else 1)
        art = quill_leaf(art, W, H, x, y, L, ang, SAGE if k % 3 else SAGE_D, seed=nx(), folds=4)
    # scrolls filling gaps
    for deg, side in ((-40, 1), (240, -1), (85, 1), (140, -1), (190, 1)):
        a = math.radians(deg)
        x0, y0 = C + math.cos(a) * (Rr + 4), C + math.sin(a) * (Rr + 4)
        x1, y1 = C + math.cos(a + side * 0.1) * (Rr + 44), C + math.sin(a + side * 0.1) * (Rr + 44)
        art = scroll(art, W, H, x0, y0, x1, y1, 15, side, TEAL)
    # buds at the open top
    for deg in (-62, 252):
        a = math.radians(deg)
        art = bud(art, W, H, C + math.cos(a) * (Rr + 4), C + math.sin(a) * (Rr + 4), 18, a + (math.pi / 2 if deg < 0 else -math.pi / 2) * -1)
    # flowers
    def at(deg, rr=Rr):
        a = math.radians(deg)
        return C + math.cos(a) * rr, C + math.sin(a) * rr
    art = aster(art, W, H, *at(18), 40)
    art = aster(art, W, H, *at(212), 38, TEAL, CREAM)
    art = flower_b(art, W, H, *at(165), 60, 0.3)
    art = flower_b(art, W, H, *at(60), 62, 0.1)
    art = flower_a(art, W, H, *at(110, Rr + 6), 86, 0.2)
    # dots of tight coils
    for deg in (35, 80, 135, 185, 230, -10):
        x, y = at(deg, Rr + (34 if deg % 2 else -30))
        art = quill_coil(art, W, H, x, y, 8, MUSTARD if deg % 3 else CORAL, seed=nx(), off=0.0, turns=2.2)
    prev(art, "kq-wreath", tone="#f4efe8")
    save_full(art, f"{OUT}/wreath.webp", (640, 640), quality=82)


def corner():
    W, H = 640, 640
    art = blank(W, H)
    stem = curve([(40, 620), (120, 470), (250, 330), (420, 210), (560, 120)], 80)
    art = quill_line(art, W, H, stem, SAGE_D, seed=nx(), width=4.6)
    side = curve([(150, 430), (230, 450), (330, 430), (420, 380)], 40)
    art = quill_line(art, W, H, side, SAGE_D, seed=nx(), width=4.2)
    side2 = curve([(205, 370), (180, 270), (200, 170), (250, 110)], 40)
    art = quill_line(art, W, H, side2, SAGE_D, seed=nx(), width=4.2)
    rng = random.Random(nx())
    for i in range(6, 74, 9):
        x, y = stem[i]
        x2, y2 = stem[i + 1]
        t = math.atan2(y2 - y, x2 - x)
        s = 1 if (i // 9) % 2 else -1
        art = quill_leaf(art, W, H, x + math.cos(t + s * 1.57) * 34, y + math.sin(t + s * 1.57) * 34, rng.uniform(56, 70), t + s * 0.9, SAGE if i % 2 else SAGE_D, seed=nx(), folds=4)
    for x, y, a in ((300, 450, -0.2), (370, 420, 0.4), (180, 220, -1.3), (220, 150, -0.9)):
        art = quill_leaf(art, W, H, x, y, 52, a, SAGE, seed=nx(), folds=3)
    art = scroll(art, W, H, 110, 500, 60, 440, 20, -1, TEAL)
    art = scroll(art, W, H, 470, 180, 500, 250, 18, 1, TEAL)
    art = bud(art, W, H, 430, 372, 20, -0.6, CORAL)
    art = bud(art, W, H, 255, 100, 18, -1.0, ROSE)
    art = aster(art, W, H, 330, 300, 40)
    art = flower_b(art, W, H, 190, 380, 54, 0.4)
    art = flower_a(art, W, H, 540, 115, 84, 0.1)
    for x, y in ((280, 380), (420, 280), (150, 300), (560, 210)):
        art = quill_coil(art, W, H, x, y, 8, MUSTARD, seed=nx(), off=0.0, turns=2.2)
    prev(art, "kq-corner", tone="#f4efe8")
    save(art, f"{OUT}/corner.webp", max_w=420, quality=82)


def divider():
    W, H = 840, 150; cy = 75
    art = blank(W, H)
    for sgn in (-1, 1):
        x0 = 420 + sgn * 40
        pts = curve([(x0, cy), (420 + sgn * 160, cy - 10), (420 + sgn * 300, cy + 6)], 40)
        art = quill_line(art, W, H, pts, SAGE_D, seed=nx())
        art = scroll(art, W, H, *pts[-1], 420 + sgn * 345, cy - 14, 22, sgn, TEAL)
        art = quill_leaf(art, W, H, 420 + sgn * 120, cy - 22, 50, -0.3 * sgn + (math.pi if sgn < 0 else 0) + 0.15, SAGE, seed=nx(), folds=3)
        art = quill_leaf(art, W, H, 420 + sgn * 210, cy + 18, 44, 0.35 * sgn + (math.pi if sgn < 0 else 0), SAGE, seed=nx(), folds=3)
        art = quill_coil(art, W, H, 420 + sgn * 260, cy - 18, 7, MUSTARD, seed=nx(), off=0.0, turns=2)
        art = quill_coil(art, W, H, 420 + sgn * 78, cy + 18, 11, ROSE_L, seed=nx(), shape="tear", ang=math.pi if sgn > 0 else 0, turns=2.4)
    art = flower_a(art, W, H, 420, cy, 50, 0.3)
    prev(art, "kq-divider", tone="#f4efe8")
    save(art, f"{OUT}/divider.webp", max_w=420, quality=84)


def bloom():
    W = H = 400; C = 200
    art = blank(W, H)
    for a in (2.3, 0.6, 4.0):
        art = quill_leaf(art, W, H, C + math.cos(a) * 120, C + math.sin(a) * 120, 110, a, SAGE if a > 1 else SAGE_D, seed=nx(), folds=5)
    art = quill_flower(art, W, H, C, C, 150, [ROSE], MUSTARD, nx, petals=8, rot=0.2, shape="tear", inner=ROSE_L)
    prev(art, "kq-bloom", tone="#f4efe8")
    save(art, f"{OUT}/bloom.webp", max_w=200, quality=84)


def card():
    W = H = 512
    p = np.asarray(paper(W, H, "#f6f1ea", nx(), fiber=0.9, mottle=0.4), np.float32) / 255
    arr = np.concatenate([p, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(tileable(arr), f"{OUT}/card.webp", quality=72)


for part in PARTS:
    {"wreath": wreath, "corner": corner, "divider": divider, "bloom": bloom, "card": card}[part]()
    clear()
