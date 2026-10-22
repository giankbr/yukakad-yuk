"""Tunangan Modern — minimal engagement in warm white, charcoal fine-line ink + one terracotta accent: two interlocked
rings drawn with a pen over a soft terracotta wash disc, a single painted ranunculus stem, a short budding sprig, and
a pen-line divider that loops into a ring. Run: python3 -I tunangan-modern.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f6_lib import *

OUT = outdir("tunangan-modern")
PARTS = sys.argv[1:] or ["rings", "stem", "sprig", "loop"]
INK = "#23211e"
ACC, ACC_D, ACC_L = "#b9562f", "#8a3a1d", "#e8a587"
STEM, STEM_D = "#7c8a5e", "#4f5c39"
PAPER = "#f5f3ef"


def ell(cx, cy, rx, ry, rot, n=220):
    return [(cx + math.cos(t) * rx * math.cos(rot) - math.sin(t) * ry * math.sin(rot),
             cy + math.cos(t) * rx * math.sin(rot) + math.sin(t) * ry * math.cos(rot)) for t in [i / n * math.tau for i in range(n + 1)]]


def runs(pts, keep):
    """Split a polyline into runs of consecutive points where keep(p) is True."""
    out, cur = [], []
    for p in pts:
        if keep(p):
            cur.append(p)
        elif cur:
            if len(cur) > 2:
                out.append(cur)
            cur = []
    if len(cur) > 2:
        out.append(cur)
    return out


def bloom(art, W, H, cx, cy, r, rng, nx):
    """Ranunculus/peony-cup bloom: a fan of rounded cupped petals around a tight centre, one terracotta, loose pen."""
    bx, by = cx, cy + r * 0.55
    petals = []
    for k, a in enumerate([-2.75, -0.39, -2.35, -0.8, -1.95, -1.2, -1.57]):
        L = r * (1.05 if k < 2 else 0.98 - 0.04 * k) * rng.uniform(.95, 1.05)
        wd = r * (0.42 if k < 4 else 0.36)
        pts = deform(petal_pts(bx, by, L, wd, a + rng.uniform(-.06, .06), n=16, cup=-0.2), rng, 2, 0.04)
        petals.append(pts)
    for k, pts in enumerate(petals):
        m = shapes(W, H, [pts])
        art = G(art, m, mix(ACC_L, ACC, 0.15 + k * 0.08), mix(ACC, ACC_D, k * 0.08), seed=nx(), density=0.5 + k * 0.03, edge=0.75, bloom=0.4, rough=2.5)
        if k in (0, 3, 6):
            art = ink(art, inkline(W, H, [(x + 4, y - 3) for x, y in pts[3:14]], 1.2, rng), INK, nx, 0.7)
    ball = shapes(W, H, [deform(ellipse_pts(cx, cy - r * 0.05, r * 0.42, r * 0.34, 14), rng, 2, 0.05)])
    art = G(art, ball, ACC, ACC_D, seed=nx(), density=0.65, edge=0.7, bloom=0.3, rough=2)
    for k in range(4):
        rr = r * (0.36 - k * 0.07)
        arc = arc_pts(cx + rng.gauss(0, 2), cy - r * 0.02 - k * r * 0.05, rr, math.pi * (0.1 + 0.1 * k), math.pi * (0.95 - 0.05 * k), 20, 0.6)
        art = G(art, strokes(W, H, [(arc, r * 0.07, (0.3, 0.3))]), ACC_D, seed=nx(), density=0.55, edge=0.4, bloom=0, rough=1.2)
    return art


if "rings" in PARTS:
    W, H = 640, 480
    nx = Seq(71100); rng = random.Random(3)
    art = blank(W, H)
    disc = shapes(W, H, [deform(ellipse_pts(372, 250, 168, 162, 20), rng, 2, 0.03)])
    art = G(art, disc, ACC_L, "#f0c2a8", seed=nx(), density=0.42, edge=0.5, bloom=0.55, rough=6, mottle=0.7)
    A = dict(cx=262, cy=262, rx=150, ry=112, rot=-0.18)
    B = dict(cx=392, cy=226, rx=136, ry=100, rot=0.32)
    def band(d, w):
        o = shapes(W, H, [ell(d["cx"], d["cy"], d["rx"] + w, d["ry"] + w, d["rot"], 80)])
        i = shapes(W, H, [ell(d["cx"], d["cy"], d["rx"] - w, d["ry"] - w, d["rot"], 80)])
        return np.clip(o - i, 0, 1)
    bandA, bandB = band(A, 13), band(B, 12)
    inA = lambda p: bandA[min(H - 1, max(0, int(p[1]))), min(W - 1, max(0, int(p[0])))] > 0.3
    inB = lambda p: bandB[min(H - 1, max(0, int(p[1]))), min(W - 1, max(0, int(p[0])))] > 0.3
    midy = 244
    lines = []
    for d, other, under in ((A, inB, lambda p: p[1] < midy), (B, inA, lambda p: p[1] >= midy)):
        for off in (-11, 11, -3):
            pts = ell(d["cx"], d["cy"], d["rx"] + off, d["ry"] + off, d["rot"])
            w_ = 2.2 if off != -3 else 1.0
            for run in runs(pts, lambda p: not (other(p) and under(p))):
                lines.append((wobble(run, rng, 0.25), w_, (0.04, 0.04)))
    m = strokes(W, H, lines)
    art = ink(art, m, INK, nx, 0.92)
    # solitaire on ring A: crown + pavilion facets, pen only, one terracotta glint
    sx, sy = ell(A["cx"], A["cy"], A["rx"] + 11, A["ry"] + 11, A["rot"], 40)[30]
    sx += 6
    g = [(sx - 30, sy - 26), (sx - 18, sy - 40), (sx + 18, sy - 40), (sx + 30, sy - 26), (sx, sy + 6), (sx - 30, sy - 26), (sx + 30, sy - 26)]
    facets = [[(sx - 18, sy - 40), (sx - 8, sy - 26), (sx, sy + 6)], [(sx + 18, sy - 40), (sx + 8, sy - 26), (sx, sy + 6)], [(sx - 8, sy - 26), (sx, sy - 40), (sx + 8, sy - 26)]]
    gm = np.maximum(strokes(W, H, [(g, 2.0, None)]), strokes(W, H, [(f, 1.1, None) for f in facets]))
    prong = strokes(W, H, [([(sx - 22, sy - 10), (sx - 14, sy + 2)], 2.0, None), ([(sx + 22, sy - 10), (sx + 14, sy + 2)], 2.0, None)])
    art = G(art, shapes(W, H, [[(sx - 18, sy - 40), (sx, sy - 40), (sx - 8, sy - 26)]], smooth=False), ACC, seed=nx(), density=0.55, edge=0.4, bloom=0, rough=1)
    art = ink(art, np.maximum(gm, prong), INK, nx, 0.92)
    sparks = strokes(W, H, [([(sx + 46, sy - 58), (sx + 58, sy - 70)], 1.4, None), ([(sx + 52, sy - 44), (sx + 68, sy - 46)], 1.4, None), ([(sx + 36, sy - 66), (sx + 38, sy - 82)], 1.4, None)])
    art = ink(art, sparks, ACC_D, nx, 0.8)
    preview(art, "tm-rings", tone=PAPER)
    save(art, f"{OUT}/rings.webp", max_w=420, quality=84)
    clear()

if "stem" in PARTS:
    W, H = 420, 1200
    nx = Seq(71300); rng = random.Random(5)
    art = blank(W, H)
    stem = curve([(170, 1190), (196, 900), (232, 560), (226, 330), (214, 210)], 120)
    sm = strokes(W, H, [(stem, 7.5, (0.02, 0.05))])
    art = G(art, sm, STEM, STEM_D, seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.5)
    for (i, L, a, wd) in ((70, 300, -2.05, 34), (46, 250, -0.95, 28)):
        bx, by = stem[i]
        p = curve([(bx, by), (bx + math.cos(a) * L * .45, by + math.sin(a) * L * .45 - 10), (bx + math.cos(a + (0.25 if a > -1.5 else -0.25)) * L, by + math.sin(a) * L * 0.92)], 30)
        lm = shapes(W, H, [jw.blade(W, H, p, wd)])
        art = G(art, lm, "#93a173", STEM_D, seed=nx(), density=0.72, edge=0.6, bloom=0.35, rough=2.5)
        art = ink(art, inkline(W, H, [(x + 3, y + 2) for x, y in p[2:-3]], 1.1, rng), INK, nx, 0.5)
    art = ink(art, inkline(W, H, [(x + 6, y) for x, y in stem[30:110]], 1.2, rng), INK, nx, 0.55)
    # sepals under the flower
    for a in (-0.5, 0.4, 1.3, 2.6):
        art = G(art, shapes(W, H, [petal_pts(214, 214, 40, 12, math.pi / 2 + a * 0.5 + 0.6, n=10)]), "#93a173", STEM_D, seed=nx(), density=0.75, edge=0.5, rough=1.2)
    art = bloom(art, W, H, 214, 150, 104, rng, nx)
    preview(art, "tm-stem", tone=PAPER)
    save(art, f"{OUT}/stem.webp", max_w=240, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 360, 420
    nx = Seq(71500); rng = random.Random(7)
    art = blank(W, H)
    stem = curve([(150, 410), (170, 300), (196, 160), (204, 96)], 60)
    art = G(art, strokes(W, H, [(stem, 5, (0.02, 0.05))]), STEM, STEM_D, seed=nx(), density=0.8, edge=0.5, rough=1.2)
    lm = shapes(W, H, [jw.blade(W, H, curve([(174, 280), (110, 230), (66, 170)], 24), 20)])
    art = G(art, lm, "#93a173", STEM_D, seed=nx(), density=0.72, edge=0.6, bloom=0.3, rough=2)
    bud = shapes(W, H, [deform(petal_pts(204, 100, 76, 34, -math.pi / 2 + 0.08, n=14), rng, 2, 0.05)])
    art = G(art, bud, ACC_L, ACC, seed=nx(), density=0.75, edge=0.65, bloom=0.4, rough=2.5)
    art = G(art, shapes(W, H, [petal_pts(210, 96, 64, 14, -math.pi / 2 + 0.2, n=10)]), ACC_D, seed=nx(), density=0.45, edge=0.4, rough=1.5)
    for a in (-0.7, 0.7):
        art = G(art, shapes(W, H, [petal_pts(204, 104, 34, 9, -math.pi / 2 + a, n=10)]), "#93a173", STEM_D, seed=nx(), density=0.8, edge=0.5, rough=1)
    art = ink(art, inkline(W, H, [(x + 5, y - 3) for x, y in petal_pts(204, 100, 76, 34, -math.pi / 2 + 0.08, n=30)[4:26]], 1.2, rng), INK, nx, 0.7)
    preview(art, "tm-sprig", tone=PAPER)
    save(art, f"{OUT}/sprig.webp", max_w=160, quality=84)
    clear()

if "loop" in PARTS:
    W, H = 760, 120
    nx = Seq(71700); rng = random.Random(9)
    art = blank(W, H)
    cx, cy = 380, 60
    loop = [(cx + math.sin(t) * 26 - (t - math.pi) * 3, cy - (1 - math.cos(t)) * 24) for t in [i / 60 * math.tau for i in range(61)]]
    pts = curve([(20, 62), (200, 60), (cx - 30, 61)], 40) + loop + curve([(cx + 30, 61), (560, 60), (740, 62)], 40)
    m = inkline(W, H, pts, 2.0, rng, wob=0.5, taper=(0.12, 0.12))
    art = ink(art, m, INK, nx, 0.9)
    art = G(art, circles(W, H, [(cx + 2, 12, 6.5)]), ACC, seed=nx(), density=0.85, edge=0.6, rough=1)
    preview(art, "tm-loop", tone=PAPER)
    save(art, f"{OUT}/loop.webp", max_w=380, quality=84)
    clear()
