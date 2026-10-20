"""Sketsa Tangan — fountain-pen botanical corners, two inked coffee cups with heart steam, coffee-ring stain,
masking tape and cream sketchbook paper.
Run: python3 -I /tmp/pen/art/themes/sketsa-tangan.py [asset…]
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _p2_lib import *  # noqa

D = f"{OUT}/sketsa-tangan"
os.makedirs(D, exist_ok=True)
TONE = "#f3eee4"
INK = "#2a2622"


def ellipse_open(cx, cy, rx, ry, a0, a1, n=24, rng=None):
    pts = [(cx + math.cos(t) * rx, cy + math.sin(t) * ry) for t in np.linspace(a0, a1, n)]
    return pts


def wavy(x0, y0, h, amp, n=30, phase=0.0, rng=None):
    return [(x0 + math.sin(phase + t * 2.6) * amp * (1 - t * 0.3), y0 - t * h) for t in np.linspace(0, 1, n)]


def cup(lines, cx, cy, w, h, rng, handle_side=1):
    """A coffee cup drawn the way a pen would: rim ellipse, two sides, foot, saucer, handle."""
    rx, ry = w / 2, w * 0.18
    rim = ellipse_open(cx, cy, rx, ry, 0, math.tau, 30)
    lines.append(rim + [rim[0]])
    # inner coffee surface (lower ellipse)
    lines.append(ellipse_open(cx, cy + ry * 0.9, rx * 0.82, ry * 0.75, 0.15, math.pi - 0.15, 18))
    bw = w * 0.36
    lines.append([(cx - rx, cy), (cx - rx * 0.92, cy + h * 0.5), (cx - bw, cy + h)])
    lines.append([(cx + rx, cy), (cx + rx * 0.92, cy + h * 0.5), (cx + bw, cy + h)])
    lines.append(ellipse_open(cx, cy + h, bw, bw * 0.3, 0.1, math.pi - 0.1, 16))
    # saucer
    lines.append(ellipse_open(cx, cy + h * 1.02, w * 0.78, w * 0.17, 0, math.tau, 32) + [(cx + w * 0.78, cy + h * 1.02)])
    lines.append(ellipse_open(cx, cy + h * 1.02 + 4, w * 0.78, w * 0.17, 0.08, math.pi - 0.08, 20))
    # handle
    hx = cx + handle_side * rx * 0.97
    outer = ellipse_open(hx + handle_side * w * 0.12, cy + h * 0.45, w * 0.22, h * 0.3, -math.pi / 2 + (0 if handle_side > 0 else math.pi), math.pi / 2 + (0 if handle_side > 0 else math.pi), 16)
    inner = ellipse_open(hx + handle_side * w * 0.12, cy + h * 0.45, w * 0.12, h * 0.18, -math.pi / 2 + (0 if handle_side > 0 else math.pi), math.pi / 2 + (0 if handle_side > 0 else math.pi), 12)
    lines.append(outer); lines.append(inner)


def heart_pts(cx, cy, s, n=40):
    out = []
    for t in np.linspace(0, math.tau, n):
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        out.append((cx + x * s, cy + y * s))
    return out


def cups():
    W, H = 760, 620
    rng = random.Random(3)
    lines = []
    cup(lines, 230, 330, 210, 170, rng, handle_side=-1)
    cup(lines, 520, 350, 190, 150, rng, handle_side=1)
    # steam: two wisps from each cup, and a heart drawn in the middle of the steam
    for (x, ph) in [(200, 0.3), (250, 1.9), (495, 1.0), (545, 2.6)]:
        lines.append(wavy(x, 300 if x < 400 else 320, rng.uniform(120, 170), rng.uniform(18, 26), phase=ph))
    hp = heart_pts(375, 150, 3.2)
    lines.append(hp[: len(hp) // 2 + 1]); lines.append(hp[len(hp) // 2:])
    # little dots / sugar cubes
    for (x, y) in [(120, 505), (138, 512)]:
        sq = [(x, y), (x + 18, y - 4), (x + 22, y + 10), (x + 4, y + 14), (x, y)]
        lines.append(sq)
    m = ink_mask(W, H, lines, width=2.4, jitter=0.45, seed=11, taper=(0.08, 0.08), wobble=1.1)
    art = ink(m, INK, seed=5, dry=0.2, bleed=0.32, density=0.92)
    # pencil shading on the shadow side of each cup and under the saucers
    sh = np.zeros((H, W), np.float32)
    for (cx, cy, w, h) in [(230, 330, 210, 170), (520, 350, 190, 150)]:
        sh = np.maximum(sh, shape_mask(W, H, [(cx + w * .2, cy + 8), (cx + w * .5, cy + 4), (cx + w * .45, cy + h * .55), (cx + w * .33, cy + h * .96), (cx + w * .1, cy + h * .9)]))
        sh = np.maximum(sh, shape_mask(W, H, ellipse_pts(cx, cy + h * 1.02 + 10, w * .9, w * .14, 14)) * (1 - shape_mask(W, H, ellipse_pts(cx, cy + h * 1.02, w * .78, w * .17, 14))))
    art = over(pencil(hatch_mask(W, H, sh, spacing=5, angle=-0.8, width=1.0, seed=9), "#5a534b", seed=4, grain=0.6, density=0.5), art)
    # a light coffee wash inside the cups
    wash = blank(W, H)
    for (cx, cy, w) in [(230, 330, 210), (520, 350, 190)]:
        im = shape_mask(W, H, deform(ellipse_pts(cx, cy + w * .16, w * .4, w * .12, 12), rng, 2, .08))
        wash = glaze(wash, pig(im, "#a9825e", "#7a5637", seed=21, density=0.5, edge=0.6, bloom=0.3, rough=3))
    art = over(art, wash)
    print("cups", save_asset(art, f"{D}/cups.webp", max_w=400, quality=82), kb(f"{D}/cups.webp"))
    preview(art, f"{PREV}/st-cups.png", TONE)


def sprig_lines(lines, x0, y0, L, a, rng, leaves=7, leaf_len=22, kind="leaf"):
    pts = curve([(x0, y0), (x0 + math.cos(a) * L * .5 + rng.gauss(0, 8), y0 + math.sin(a) * L * .5 + rng.gauss(0, 8)), (x0 + math.cos(a) * L, y0 + math.sin(a) * L)], 40)
    lines.append(pts)
    for i in range(leaves):
        t = 0.15 + 0.8 * i / leaves
        px, py = pts[int(t * (len(pts) - 1))]
        side = 1 if i % 2 else -1
        la = a + side * rng.uniform(0.7, 1.2)
        ll = leaf_len * (1 - 0.4 * t) * rng.uniform(.8, 1.2)
        if kind == "leaf":
            p = petal_pts(px, py, ll, ll * 0.3, la, n=12)
            lines.append(p + [p[0]])
        elif kind == "berry":
            e = ellipse_pts(px + math.cos(la) * ll * .5, py + math.sin(la) * ll * .5, ll * .22, ll * .22, 10)
            lines.append([(px, py), (px + math.cos(la) * ll * .35, py + math.sin(la) * ll * .35)])
            lines.append(e + [e[0]])
        else:  # grass: thin blades
            lines.append([(px, py), (px + math.cos(la) * ll * .6, py + math.sin(la) * ll * .6), (px + math.cos(la - side * .3) * ll, py + math.sin(la - side * .3) * ll)])


def flower_lines(lines, cx, cy, r, rng, petals=5):
    c = ellipse_pts(cx, cy, r * .28, r * .28, 10)
    lines.append(c + [c[0]])
    for i in range(petals):
        a = i / petals * math.tau + rng.uniform(-.2, .2)
        p = petal_pts(cx + math.cos(a) * r * .3, cy + math.sin(a) * r * .3, r * .75, r * .32, a, n=12)
        lines.append(p + [p[0]])


def corner(name, seed, variant=0):
    """Botanical corner cluster (fits the top-left of the page; mirrored in CSS for the other corners)."""
    W, H = 460, 460
    rng = random.Random(seed)
    lines = []
    ox, oy = 20, 20
    if variant:
        # grasses, a fern frond and berries — airier than corner A
        sprig_lines(lines, ox, oy, 420, 0.3, rng, leaves=11, leaf_len=40, kind="grass")
        sprig_lines(lines, ox + 6, oy, 380, 1.15, rng, leaves=12, leaf_len=38)
        sprig_lines(lines, ox + 20, oy + 10, 300, 0.7, rng, leaves=7, leaf_len=28, kind="berry")
        sprig_lines(lines, ox, oy + 60, 220, 1.45, rng, leaves=6, leaf_len=50, kind="grass")
        sprig_lines(lines, ox + 60, oy, 220, 0.02, rng, leaves=6, leaf_len=24, kind="berry")
        flower_lines(lines, 250, 140, 36, rng, petals=6)
        flower_lines(lines, 120, 300, 26, rng, petals=5)
        centres = [(250, 140, 36), (120, 300, 26)]
    else:
        centres = [(200, 160, 42), (110, 260, 32), (320, 90, 26)]
    if not variant:
     sprig_lines(lines, ox, oy, 400, 0.22, rng, leaves=9, leaf_len=52)
     sprig_lines(lines, ox, oy + 10, 390, 1.3, rng, leaves=8, leaf_len=48)
     sprig_lines(lines, ox + 10, oy, 300, 0.72, rng, leaves=6, leaf_len=26, kind="berry")
     sprig_lines(lines, ox + 30, oy + 30, 250, 0.98, rng, leaves=5, leaf_len=60, kind="grass")
     sprig_lines(lines, ox, oy + 50, 210, 1.5, rng, leaves=5, leaf_len=30, kind="leaf")
     sprig_lines(lines, ox + 50, oy, 200, 0.05, rng, leaves=5, leaf_len=30, kind="leaf")
     flower_lines(lines, 200, 160, 42, rng, petals=5)
     flower_lines(lines, 110, 260, 32, rng, petals=6)
     flower_lines(lines, 320, 90, 26, rng, petals=5)
    m = ink_mask(W, H, lines, width=1.8, jitter=0.4, seed=seed, taper=(0.08, 0.08), wobble=1.0)
    art = ink(m, INK, seed=seed + 1, dry=0.22, bleed=0.3, density=0.88)
    # a little pencil tone inside the flower centres
    sh = np.zeros((H, W), np.float32)
    for (cx, cy, r) in centres:
        sh = np.maximum(sh, shape_mask(W, H, ellipse_pts(cx, cy, r * .26, r * .26, 10)))
    art = over(pencil(hatch_mask(W, H, sh, spacing=3.5, angle=-0.6, width=0.9, seed=seed + 2), "#5a534b", seed=4, grain=0.5, density=0.6), art)
    print(name, save_asset(art, f"{D}/{name}.webp", max_w=260, quality=82), kb(f"{D}/{name}.webp"))
    preview(art, f"{PREV}/st-{name}.png", TONE)


def corner_a():
    corner("corner-a", 31)


def corner_b():
    corner("corner-b", 77, variant=1)


def coffee():
    """Coffee-ring stain: a thin dark ring where the cup sat, plus a faint spill."""
    W, H = 420, 420
    rng = random.Random(6); sd = Seeds(400)
    outer = shape_mask(W, H, deform(ellipse_pts(210, 210, 150, 142, 16), rng, 3, .05))
    inner = shape_mask(W, H, deform(ellipse_pts(212, 209, 139, 131, 16), rng, 3, .05))
    ring = np.clip(outer - inner, 0, 1)
    art = pig(ring, "#b68a62", "#8a5f3d", seed=sd(), density=0.5, edge=1.0, bloom=0.4, rough=5, feather=1.6, holes=0.3, mottle=0.8)
    spill = shape_mask(W, H, deform(ellipse_pts(300, 120, 42, 30, 10), rng, 3, .2))
    art = glaze(art, pig(spill, "#c9a37f", "#a07753", seed=sd(), density=0.35, edge=0.8, bloom=0.5, rough=6, mottle=0.7))
    art = glaze(art, pig(dots(W, H, 300, 130, 50, 40, 9, 1.5, 4, rng), "#a07753", seed=sd(), density=0.45, edge=0.3, bloom=0, rough=1, feather=.5))
    print("coffee", save_asset(art, f"{D}/coffee.webp", max_w=240, quality=78), kb(f"{D}/coffee.webp"))
    preview(art, f"{PREV}/st-coffee.png", TONE)


def tape():
    """Masking tape: translucent beige strip with crinkled edges and torn ends."""
    W, H = 280, 90
    rng = random.Random(8)
    pts = deform([(16, 20), (W - 14, 16), (W - 18, H - 16), (14, H - 20)], rng, 3, .04)
    m = shape_mask(W, H, pts, smooth=False)
    def nib(cv):
        for x in (14, W - 14):
            for _ in range(8):
                cv.c.drawCircle(x + rng.gauss(0, 3), rng.uniform(16, H - 16), rng.uniform(3, 7), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    m = np.clip(m - mask_from(W, H, nib), 0, 1)
    g = fbm(W, H, 5, 14, 3)
    crinkle = gaussian_filter(np.random.default_rng(2).random((H, W)).astype(np.float32), (0.5, 2.5))
    crinkle = (crinkle - crinkle.mean()) / (crinkle.std() + 1e-6)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#e3d7bf"), np.float32) * (1 + crinkle[..., None] * 0.04)
    a = m * (0.62 + 0.2 * g)
    art = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
    print("tape", save_asset(art, f"{D}/tape.webp", max_w=140, quality=82), kb(f"{D}/tape.webp"))


def texture():
    save_texture(paper_tile(512, "#fbf7ee", seed=41, mottle=0.6, fine=1.1, fiber=1.2, strength=0.9), f"{D}/paper.webp", quality=68)
    print("paper", kb(f"{D}/paper.webp"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["cups", "corner_a", "corner_b", "coffee", "tape", "texture"]
    for w in which:
        globals()[w]()
