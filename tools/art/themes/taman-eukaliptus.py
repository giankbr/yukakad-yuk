"""Taman Eukaliptus — watercolour silver-dollar eucalyptus (glaucous blue-greens, plum-brown stems), light from top-left.
Run: python3 -I /tmp/pen/art/themes/taman-eukaliptus.py
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from agentA_lib import *  # noqa

D = f"{OUT}/taman-eukaliptus"
P = "/tmp/pen/nt2-A"
os.makedirs(D, exist_ok=True)
TONE = "#f6f7f0"
TONES = [("#a9bcae", "#7f9a8c"), ("#9db3a7", "#6f8b80"), ("#b8c8b6", "#88a091"), ("#93aa9f", "#64806f"), ("#aec0a6", "#7d9779")]
STEMC = "#8a6f62"


def bez(p, t):
    u = 1 - t
    x = u**3 * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t**3 * p[3][0]
    y = u**3 * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t**3 * p[3][1]
    dx = 3 * u * u * (p[1][0] - p[0][0]) + 6 * u * t * (p[2][0] - p[1][0]) + 3 * t * t * (p[3][0] - p[2][0])
    dy = 3 * u * u * (p[1][1] - p[0][1]) + 6 * u * t * (p[2][1] - p[1][1]) + 3 * t * t * (p[3][1] - p[2][1])
    return x, y, math.atan2(dy, dx)


def round_leaf(W, H, x, y, r, rot, tone, sd, rng):
    ca, cb = tone
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 0.88, 18, rot), rng, 2, 0.03))
    lay = pig(m, ca, cb, seed=sd(), density=0.64, edge=0.66, bloom=0.5, rough=2.6, feather=1.1, holes=0.03, pad=24)
    # shadow crescent toward lower-right (light from top-left)
    sh = shape_mask(W, H, ellipse_pts(x + r * .32, y + r * .3, r * .78, r * .62, 10, rot)) * m
    lay = glaze(lay, pig(sh, cb, seed=sd(), density=0.22, edge=0.25, bloom=0.3, rough=2.5, pad=24))
    # faint midrib
    a = rot
    v = [(x - math.cos(a) * r * .7 * (1 - t * 2), y - math.sin(a) * r * .7 * (1 - t * 2)) for t in [j / 10 for j in range(11)]]
    lay = glaze(lay, pig(stroke_mask(W, H, v, 1.6), mix(cb, "#2d3a33", .4), seed=sd(), density=0.2, edge=0.1, bloom=0, rough=1, feather=.6, pad=16))
    return lay, m


def branch(seed, ctrl, n, r0, r1, W=320, H=660, spread=0.95):
    rng = random.Random(seed); sd = Seeds(400 + seed * 31)
    stems, _ = stem(W, H, [ctrl[0], bez(ctrl, .33)[:2], bez(ctrl, .66)[:2], ctrl[3]], 4.2, STEMC, sd, density=0.6)
    leaves = blank(W, H); stack = np.zeros((H, W), np.float32)
    # paint tip → base so lower (bigger) leaves sit on top of the smaller ones above
    items = []
    for i in range(n):
        t = 0.08 + i * (0.86 / (n - 1))
        x, y, a = bez(ctrl, t)
        side = 1 if i % 2 else -1
        r = r0 + (r1 - r0) * (i / (n - 1)) + rng.uniform(-2, 2)
        off = r * spread
        lx = x + math.cos(a + side * math.pi / 2) * off + math.cos(a) * rng.uniform(-3, 3)
        ly = y + math.sin(a + side * math.pi / 2) * off
        items.append((x, y, lx, ly, r, a + side * 0.5, i))
    for (x, y, lx, ly, r, rot, i) in items[::-1]:
        lay, m = round_leaf(W, H, lx, ly, r, rot, TONES[(i * 3 + seed) % len(TONES)], sd, rng)
        pet, _ = stem(W, H, [(x, y), ((x + lx) / 2, (y + ly) / 2 + 2), (lx, ly)], 2.4, STEMC, sd, density=0.5)
        stems = glaze(stems, knockout(pet, m, 0.95, 1.5))   # petiole disappears under its own leaf
        leaves = glaze(leaves, knockout(lay, stack, 0.55, 2))   # partially behind the leaves already painted (glazes through a bit)
        stack = np.maximum(stack, m)
    return glaze(stems, leaves)


def sprig():
    W, H = 420, 150
    rng = random.Random(21); sd = Seeds(777)
    ctrl = [(14, 80), (130, 64), (280, 90), (406, 70)]
    st, _ = stem(W, H, [ctrl[0], bez(ctrl, .33)[:2], bez(ctrl, .66)[:2], ctrl[3]], 3.2, STEMC, sd, density=0.6)
    leaves = blank(W, H); stack = np.zeros((H, W), np.float32)
    pts = [(.06, 1, 17), (.15, -1, 22), (.26, 1, 25), (.38, -1, 28), (.5, 1, 29), (.62, -1, 27), (.74, 1, 24), (.85, -1, 20), (.94, 1, 15)]
    for (t, side, r) in pts:
        x, y, a = bez(ctrl, t)
        lx, ly = x + math.cos(a + side * math.pi / 2) * r * .72, y + math.sin(a + side * math.pi / 2) * r * .72
        lay, m = round_leaf(W, H, lx, ly, r, a + side * .4, TONES[int(t * 10) % 5], sd, rng)
        leaves = glaze(leaves, knockout(lay, stack, 0.5, 2)); stack = np.maximum(stack, m)
    art = glaze(st, leaves)
    print("sprig", save_asset(art, f"{D}/sprig.webp", max_w=240, quality=82))
    preview(art, f"{P}/te-sprig.png", TONE)


def branches():
    a = branch(1, [(170, 6), (250, 170), (60, 360), (150, 640)], 17, 48, 24, spread=0.78)
    print("branch-a", save_asset(a, f"{D}/branch-a.webp", max_w=240, quality=82))
    preview(a, f"{P}/te-branch-a.png", TONE)
    b = branch(2, [(150, 6), (60, 200), (250, 380), (170, 630)], 15, 44, 22, spread=0.78)
    print("branch-b", save_asset(b, f"{D}/branch-b.webp", max_w=240, quality=82))
    preview(b, f"{P}/te-branch-b.png", TONE)


def bud():
    """Timeline node: a pair of small leaves on a stub (shown ~30×22)."""
    W, H = 150, 110
    rng = random.Random(31); sd = Seeds(901)
    st, _ = stem(W, H, [(14, 60), (60, 56), (96, 52)], 3.0, STEMC, sd)
    l1, m1 = round_leaf(W, H, 60, 36, 26, -.5, TONES[1], sd, rng)
    l2, _ = round_leaf(W, H, 98, 70, 24, .4, TONES[2], sd, rng)
    art = glaze(glaze(st, knockout(l2, m1, .5, 2)), l1)
    print("bud", save_asset(art, f"{D}/bud.webp", max_w=72, quality=82))


def texture():
    save_texture(paper_tile(512, "#fdfdfa", seed=44, mottle=0.4, fiber=1.2, strength=0.8), f"{D}/paper.webp", quality=72)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["branches", "sprig", "bud", "texture"]:
        globals()[w]()
