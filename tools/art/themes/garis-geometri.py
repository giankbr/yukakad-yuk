"""Garis Geometri — 8-fold Islamic star pattern drafted by hand: faint graphite construction (the 4.8.8 octagon-square
grid and compass circles) under fine black technical-pen line work (Hankin polygons-in-contact, 67.5 deg), with a single
vermilion watercolour accent in a few stars. White paper, generous whitespace, editorial.
Run: python3 -I garis-geometri.py [part ...]  parts: rosette band divider star corner"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e3_lib import *

OUT = outdir("garis-geometri")
PARTS = sys.argv[1:] or ["rosette", "band", "divider", "star", "corner"]
INK, GRAPH, ACC, ACC_L = "#141414", "#8c8c8c", "#c4412b", "#e0745a"
TH = math.radians(67.5)  # 8-point stars in the octagons, 4-point stars in the squares


def pattern(W, H, s, ox, oy, rng):
    octs, sqs = tiling_488(-ox, -oy, W - ox, H - oy, s)
    octs = [[(x + ox, y + oy) for x, y in o] for o in octs]
    sqs = [[(x + ox, y + oy) for x, y in q] for q in sqs]
    lines, grid = [], []
    lines = pattern_488(octs, sqs, TH)
    for p in octs + sqs:
        grid += poly_segs(p)
    return octs, sqs, lines, grid


def draft(W, H, s, ox, oy, clip, rng, nx, accents=(), width=1.6, pencil=True, circles_at=()):
    octs, sqs, lines, grid = pattern(W, H, s, ox, oy, rng)
    art = blank(W, H)
    if pencil:
        g = ink_mask(W, H, grid, 0.7, rng, amp=0.3, press=0.1) * clip
        art = OV(art, g, lambda m: linocut(m, GRAPH, seed=nx(), wear=0.5, rough=0.4), pad=4)
        for (cx, cy, r) in circles_at:
            c = ring(W, H, cx, cy, r, 0.8) * (0.6 + 0.4 * fbm(W, H, nx(), 20, 2))
            art = OV(art, c, lambda m: linocut(m, GRAPH, seed=nx(), wear=0.4, rough=0.3), pad=4)
        art[..., 3] *= 0.55
    m = ink_mask(W, H, lines, width, rng, amp=0.45, press=0.35, blobs=0.08) * clip
    if accents:
        st = region_at(m, accents) * clip
        art = G(art, st, ACC, ACC_L, seed=nx(), density=0.72, edge=0.6, bloom=0.35, rough=1.4, feather=0.8, gran=0.3)
    art = IK(art, m, INK, seed=nx())
    return art, octs


if "rosette" in PARTS:
    W, H = 760, 760
    nx = Seq(8100); rng = random.Random(12)
    s = 62.0
    k = s / math.sqrt(2); step = s + 2 * k
    cx, cy = 380, 380
    clip = circles(W, H, [(cx, cy, 330)])
    # find the octagon nearest the centre so the medallion is centred on a star
    art, octs = draft(W, H, s, cx, cy, clip, rng, nx, accents=[(cx, cy)] + [(cx + math.cos(a) * step * 0.3, cy + math.sin(a) * step * 0.3) for a in [math.pi / 8 + k * math.pi / 4 for k in range(8)]], width=1.7,
                      circles_at=[(cx, cy, 330), (cx, cy, step * 0.5), (cx, cy, step * 1.5)])
    border = np.maximum(ring(W, H, cx, cy, 338, 1.8), ring(W, H, cx, cy, 346, 0.9))
    art = IK(art, border * (0.85 + 0.15 * fbm(W, H, nx(), 30, 2)), INK, seed=nx())
    preview(art, "gg-rosette", "#fbfaf7")
    save_full(art, f"{OUT}/rosette.webp", size=(600, 600), quality=80)
    clear()

if "band" in PARTS:
    W, H = 1200, 132
    nx = Seq(8200); rng = random.Random(13)
    s = 40.0
    k = s / math.sqrt(2); step = s + 2 * k
    clip = rect(W, H, 0, 10, W, H - 10)
    art, _ = draft(W, H, s, 0, H / 2, clip, rng, nx, accents=(), width=1.3, pencil=False)
    rules = np.maximum(rect(W, H, 0, 8, W, 9.6), rect(W, H, 0, H - 9.6, W, H - 8))
    art = IK(art, rules, INK, seed=nx())
    art[..., 3] = np.where(art[..., 3] > 0.02, art[..., 3], 0)
    preview(art, "gg-band", "#fbfaf7")
    save_full(art, f"{OUT}/band.webp", size=(900, 99), quality=80)
    clear()

if "divider" in PARTS:
    W, H = 640, 96
    nx = Seq(8300); rng = random.Random(14)
    cx, cy = 320, 48
    st = star_pts(cx, cy, 30, 8, 0.62, math.pi / 8)
    segs = poly_segs(st)
    sq1 = poly_pts(cx, cy, 30, 4, 0); sq2 = poly_pts(cx, cy, 30, 4, math.pi / 4)
    art = G(blank(W, H), shapes(W, H, [star_pts(cx, cy, 13, 8, 0.6, math.pi / 8)], smooth=False), ACC, ACC_L, seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1, feather=0.6)
    lines = poly_segs(sq1) + poly_segs(sq2) + [((40, cy), (cx - 42, cy)), ((cx + 42, cy), (600, cy))]
    art = IK(art, ink_mask(W, H, lines, 1.5, rng, amp=0.35, press=0.4, blobs=0.2), INK, seed=nx())
    art = IK(art, circles(W, H, [(cx - 52, cy, 2.4), (cx + 52, cy, 2.4)]), INK, seed=nx())
    preview(art, "gg-divider", "#fbfaf7")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()

if "star" in PARTS:
    W, H = 200, 200
    nx = Seq(8400); rng = random.Random(15)
    cx, cy = 100, 100
    sq1 = poly_pts(cx, cy, 80, 4, 0); sq2 = poly_pts(cx, cy, 80, 4, math.pi / 4)
    inner = star_pts(cx, cy, 40, 8, 0.66, math.pi / 8)
    art = G(blank(W, H), shapes(W, H, [inner], smooth=False), ACC, ACC_L, seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=1.2, feather=0.7, gran=0.3)
    art = IK(art, ink_mask(W, H, poly_segs(sq1) + poly_segs(sq2) + poly_segs(inner), 3.2, rng, amp=0.5, press=0.3), INK, seed=nx())
    preview(art, "gg-star", "#fbfaf7")
    save_full(art, f"{OUT}/star.webp", size=(96, 96), quality=86)
    clear()

if "corner" in PARTS:
    W, H = 520, 520
    nx = Seq(8500); rng = random.Random(16)
    s = 46.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # quarter field fading diagonally away from the corner (pattern "dissolves" into whitespace)
    d = np.sqrt(xx ** 2 + yy ** 2)
    clip = np.clip((470 - d) / 30, 0, 1)
    k = s / math.sqrt(2); step = s + 2 * k
    art, octs = draft(W, H, s, 0, 0, clip, rng, nx, accents=[(step, step), (1, 1)], width=1.4, circles_at=[(0, 0, 470)])
    preview(art, "gg-corner", "#fbfaf7")
    save_full(art, f"{OUT}/corner.webp", size=(320, 320), quality=80)
    clear()
