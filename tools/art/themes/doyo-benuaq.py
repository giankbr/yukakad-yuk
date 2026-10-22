"""Doyo Benuaq — ulap doyo (Curculigo leaf-fibre) warp ikat at thread level: coarse hand-spun fibre, natural ground
with black + red hook/lozenge motifs; long lamin house on stilts by the Mahakam with rainforest; woven band; leaves.
Run: python3 -I doyo-benuaq.py [part ...]   parts: doyo pita kait lamin daun"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d1_lib import *

OUT = outdir("doyo-benuaq")
PARTS = sys.argv[1:] or ["doyo", "pita", "kait", "lamin", "daun"]
PAL = ["#c4a97c", "#2a1d15", "#8b2b1d", "#6c4c30", "#d9c49c"]
NAT, BLK, RED, BRN, PALE = range(5)


def hook_lozenge(c, p, cx, cy, r, w, hooks=True):
    """Lozenge outline (stroke w) with spiral hooks (kait) on its four sides."""
    sp = stroke_paint(w)
    c.drawPath(path_of([(cx, cy - r), (cx + r * 0.7, cy), (cx, cy + r), (cx - r * 0.7, cy)]), sp)
    if hooks:
        for sx in (-1, 1):
            for sy in (-1, 1):
                mx, my = cx + sx * r * 0.35, cy + sy * r * 0.5
                ex, ey = mx + sx * r * 0.32, my + sy * r * 0.26
                pa = path_of([(mx, my), (ex, ey), (ex + sx * r * 0.12, ey - sy * r * 0.12), (ex - sx * r * 0.02, ey - sy * r * 0.2)], closed=False)
                c.drawPath(pa, sp)


def design(N=96):
    lay = lambda f: wrap_draw(N, N, f)
    layers = []
    # warp stripes (bands of plain colour run the full length of the warp)
    def stripes(xs, col):
        layers.append((lay(lambda c, p: [c.drawRect(skia.Rect(x0, -N, x1, 2 * N), p) for x0, x1 in xs]), col))
    stripes([(0, 3), (93, 96), (44, 47)], BLK)
    stripes([(3, 5), (91, 93), (47, 49), (42, 44)], RED)
    # column A: hooked lozenges stacked along the warp (x 6..41)
    cxA = 23.5
    layers.append((lay(lambda c, p: [c.drawPath(path_of([(cxA, y - 20), (cxA + 14, y), (cxA, y + 20), (cxA - 14, y)]), p) for y in (24, 72)]), RED))
    layers.append((lay(lambda c, p: [hook_lozenge(c, p, cxA, y, 24, 3.2) for y in (24, 72)]), BLK))
    layers.append((lay(lambda c, p: [c.drawPath(path_of([(cxA, y - 7), (cxA + 5, y), (cxA, y + 7), (cxA - 5, y)]), p) for y in (24, 72)]), NAT))
    layers.append((lay(lambda c, p: [c.drawRect(skia.Rect(cxA - 1.5, y - 1.5, cxA + 1.5, y + 1.5), p) for y in (24, 72)]), BLK))
    # little ladder (tangga) rungs between lozenges
    layers.append((lay(lambda c, p: [c.drawRect(skia.Rect(cxA - 8, y, cxA + 8, y + 1.6), p) for y in (45, 48.5, 93, 96.5)]), BLK))
    # column B: zigzag with spiral hooks (x 49..90)
    cxB = 70
    def zig(c, p, w):
        sp = stroke_paint(w)
        pts = [(cxB + (11 if k % 2 else -11), k * 12) for k in range(-1, 10)]
        c.drawPath(path_of(pts, closed=False), sp)
    layers.append((lay(lambda c, p: zig(c, p, 7)), BLK))
    layers.append((lay(lambda c, p: zig(c, p, 2.2)), RED))
    def curls(c, p):
        sp = stroke_paint(2.4)
        for k in range(8):
            y = k * 12 + 6
            sx = 1 if k % 2 else -1
            x = cxB - sx * 3
            pts = [(x, y), (x - sx * 9, y), (x - sx * 12, y - 4), (x - sx * 9, y - 7), (x - sx * 6, y - 4)]
            c.drawPath(path_of(pts, closed=False), sp)
    layers.append((lay(curls), BLK))
    layers.append((lay(lambda c, p: [c.drawRect(skia.Rect(cxB + (13 if k % 2 == 0 else -15), k * 12 + 4, cxB + (15 if k % 2 == 0 else -13), k * 12 + 8), p) for k in range(8)]), RED))
    return layer_index(NAT, layers)


def loom(D, p=6, seed=11, tile=True):
    return ikat(D, PAL, p=p, mode="warp", ground="#8f7752", face=0.78, amp=1.6, coh=1.6, along=8, seed=seed, bleed=0.7,
                slub=0.6, fibre=0.13, thread_var=0.08, coarse=0.12, tile=tile)


if "doyo" in PARTS:
    D = design(96)
    cloth = loom(D, 6, 11)
    prev_rgb(tile_to(cloth, 1152, 700), "doyo-rep")
    save_rgb_arr(cloth, f"{OUT}/doyo.webp", quality=78)
    clear()

if "pita" in PARTS:
    D = design(96)
    cloth = loom(D, 4, 21)
    band = np.rot90(cloth[:, :49 * 4]).copy()      # lozenge column turned sideways: a woven strip
    band = band[::-1].copy()
    prev_rgb(np.concatenate([band, band], 1), "pita")
    save_rgb_arr(band, f"{OUT}/pita.webp", quality=80)
    clear()

if "kait" in PARTS:
    N = 64
    lays = []
    pd = lambda f: plain_draw(N, N, f)
    c0 = N / 2
    lays.append((pd(lambda c, p: c.drawPath(path_of([(c0, 2), (c0 + 30, c0), (c0, N - 2), (c0 - 30, c0)]), p)), BLK))
    lays.append((pd(lambda c, p: c.drawPath(path_of([(c0, 6), (c0 + 25, c0), (c0, N - 6), (c0 - 25, c0)]), p)), PALE))
    lays.append((pd(lambda c, p: c.drawPath(path_of([(c0, 12), (c0 + 17, c0), (c0, N - 12), (c0 - 17, c0)]), p)), RED))
    def hooks(c, p):
        sp = stroke_paint(2.6)
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts = [(c0 + sx * 3, c0 + sy * 3), (c0 + sx * 11, c0 + sy * 11), (c0 + sx * 7, c0 + sy * 15), (c0 + sx * 4, c0 + sy * 11)]
                c.drawPath(path_of(pts, closed=False), sp)
    lays.append((pd(hooks), BLK))
    lays.append((pd(lambda c, p: c.drawRect(skia.Rect(c0 - 2, c0 - 2, c0 + 2, c0 + 2), p)), PALE))
    D = layer_index(9, lays)
    A = (D != 9).astype(np.int32); D[D == 9] = NAT
    med = woven_cut(D, A, PAL, 5, 41, mode="warp", ground="#8f7752", face=0.78, amp=1.2, coh=1.5, along=8, slub=0.5, fibre=0.12, coarse=0.1)
    preview(med, "kait")
    save(med, f"{OUT}/kait.webp", max_w=200, quality=82)
    clear()


def gable_house(W, H, x0, x1, wall_top, floor, roof_top, overhang=26):
    roof = [(x0 - overhang, wall_top + 6), (x0 + 30, roof_top), (x1 - 30, roof_top), (x1 + overhang, wall_top + 6)]
    wall = [(x0, wall_top), (x1, wall_top), (x1, floor), (x0, floor)]
    return roof, wall


if "lamin" in PARTS:
    W, H = 920, 560
    nx = Seq(90100); rng = random.Random(9)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    # misty rainforest wall behind
    for k, (y, amp, cA, cB, dens) in enumerate([(150, 50, "#9fb3a3", "#b9c2ad", 0.45), (200, 44, "#6f8f78", "#7f9a7b", 0.55), (250, 30, "#3f644f", "#4f7356", 0.7)]):
        crowns = [(x, y + rng.uniform(-amp, amp * 0.4), rng.uniform(0.9, 1.6)) for x in range(-20, W + 40, 46)]
        cm = blobs(W, H, crowns, rng, (18, 34), 4)
        fill = poly(W, H, [(0, y), (W, y), (W, 430), (0, 430)], smooth=False)
        m = np.maximum(cm, fill) * np.clip((440 - yy) / 40, 0, 1)
        art = G(art, m, cA, cB, seed=nx(), density=dens, edge=0.45, bloom=0.4, rough=5, gran=0.3)
    # tall emergent trees (meranti) with pale trunks
    for tx, top in [(70, 40), (840, 30), (600, 90)]:
        tr = strokes(W, H, [(curve([(tx, 420), (tx + 6, (top + 420) / 2), (tx - 4, top + 40)], 20), 18, None), (curve([(tx - 2, top + 70), (tx - 30, top + 30)], 8), 6, (0.0, 0.5)), (curve([(tx + 2, top + 80), (tx + 34, top + 36)], 8), 6, (0.0, 0.5))])
        art = GP(art, tr, "#b8ab92", "#8d806a", seed=nx(), rough=1, streak=1)
        cr = blobs(W, H, [(tx + rng.uniform(-40, 40), top + rng.uniform(0, 40), 1.4) for _ in range(5)], rng, (18, 30), 4)
        art = G(art, cr, "#3b5f45", "#567a50", seed=nx(), density=0.75, edge=0.5, bloom=0.35, rough=4)
        art = G(art, blobs(W, H, [(tx - 20, top + 6, 0.8), (tx + 14, top - 4, 0.7)], rng, (10, 16), 3) * cr, "#8aa465", seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=3)
    # the long lamin on ironwood stilts
    x0, x1 = 150, 780
    wall_top, floor, roof_top = 262, 330, 196
    roof, wall = gable_house(W, H, x0, x1, wall_top, floor, roof_top)
    stilts = shapes(W, H, [[(x - 5, floor), (x + 5, floor), (x + 6, 440), (x - 6, 440)] for x in range(x0 + 8, x1, 42)], smooth=False)
    art = GP(art, stilts, "#3a2a1f", "#4d3829", seed=nx(), rough=0.9, streak=1.2)
    beam = poly(W, H, [(x0 - 10, floor), (x1 + 10, floor), (x1 + 10, floor + 12), (x0 - 10, floor + 12)], smooth=False)
    art = GP(art, beam, "#4a3526", seed=nx(), rough=0.8)
    wm = poly(W, H, wall, smooth=False)
    art = GP(art, wm, "#8b6a48", "#a07b52", seed=nx(), rough=1.2, streak=1.2)
    planks = strokes(W, H, [([(x, wall_top + 2), (x, floor - 1)], 1.2, None) for x in range(x0 + 6, x1, 9)])
    art = G(art, planks * wm, "#4c3826", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5, feather=0.5)
    # verandah rail with doyo cloths hung out to air
    rail = strokes(W, H, [([(x0 - 10, floor - 26), (x1 + 10, floor - 26)], 3, None)] + [([(x, floor - 26), (x, floor)], 2.2, None) for x in range(x0, x1 + 1, 18)])
    # doors / windows (dark openings)
    doors = shapes(W, H, [[(x - 12, wall_top + 12), (x + 12, wall_top + 12), (x + 12, floor - 2), (x - 12, floor - 2)] for x in range(x0 + 50, x1 - 20, 92)], smooth=False)
    art = GP(art, doors, "#2a1d15", "#3a2a1f", seed=nx(), rough=0.8)
    art = G(art, wm * np.clip((yy - wall_top) / 14, 0, 1) * (yy < wall_top + 20), "#2a1d15", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    kd = design(96)
    kc = loom(kd, 2, 61, tile=True)
    hang = np.zeros((H, W, 3), np.float32); hm = np.zeros((H, W), np.float32)
    for (hx, hw) in [(260, 54), (470, 60), (650, 48)]:
        hy = floor - 28
        patch = kc[0:44, 0:hw]
        hang[hy:hy + 44, hx:hx + hw] = patch
        hm[hy:hy + 44, hx:hx + hw] = 1
    hm = displace(hm, 7, 1.0, 10)
    art = over(art, rgba(hang * 0.92, hm))
    art = GP(art, rail, "#5a4230", seed=nx(), rough=0.6)
    # long gable roof of ironwood shingles (sirap)
    rm = poly(W, H, roof, smooth=False)
    art = GP(art, rm, "#5b4634", "#3f3025", seed=nx(), rough=1.4, streak=1.0)
    rows = strokes(W, H, [([(x0 - 26 + (y - roof_top) * 0, y), (x1 + 26, y)], 1.4, None) for y in range(roof_top + 8, wall_top + 6, 8)])
    art = G(art, rows * rm, "#2a2019", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5)
    shingle = strokes(W, H, [([(x, y), (x, y + 7)], 1.0, None) for y in range(roof_top + 8, wall_top, 8) for x in range(x0 - 20 + (y // 8 % 2) * 6, x1 + 20, 12)])
    art = G(art, shingle * rm, "#2a2019", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = G(art, rm * np.clip((roof_top + 26 - yy) / 26, 0, 1), "#9a8468", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    # carved finials at the ridge ends (stylised upturned hornbill-tail curls, no figures)
    fins = strokes(W, H, [(curve([(x0 + 30, roof_top), (x0 + 8, roof_top - 30), (x0 + 18, roof_top - 54), (x0 + 38, roof_top - 44)], 18), 7, (0.05, 0.5)),
                          (curve([(x1 - 30, roof_top), (x1 - 8, roof_top - 30), (x1 - 18, roof_top - 54), (x1 - 38, roof_top - 44)], 18), 7, (0.05, 0.5))])
    art = GP(art, fins, "#2a1d15", seed=nx(), rough=0.6)
    art = G(art, strokes(W, H, [(curve([(x0 + 16, roof_top - 46), (x0 + 30, roof_top - 44)], 6), 2.4, None), (curve([(x1 - 16, roof_top - 46), (x1 - 30, roof_top - 44)], 6), 2.4, None)]), "#a8321f", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4)
    # notched log ladder (tangga) from the river bank to the verandah
    lad = poly(W, H, [(372, floor + 2), (384, floor + 2), (414, 452), (400, 452)], smooth=False)
    art = GP(art, lad, "#6a4c32", "#4d3826", seed=nx(), rough=0.8)
    art = G(art, strokes(W, H, [([(378 + t * 30 - 6, floor + 10 + t * 112), (378 + t * 30 + 8, floor + 10 + t * 112)], 2, None) for t in np.linspace(0.05, 0.95, 7)]) * lad, "#2a1d15", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    # river bank + Mahakam water with the house reflected
    bank = poly(W, H, [(0, 432), (W, 426), (W, 456), (0, 462)])
    art = G(art, bank, "#7d6a4a", "#5f6b44", seed=nx(), density=0.7, edge=0.35, bloom=0.3, rough=4)
    water = poly(W, H, [(0, 452), (W, 448), (W, H), (0, H)], smooth=False)
    art = G(art, water, "#6e8a7e", "#8a8a6a", seed=nx(), density=0.7, edge=0.2, bloom=0.4, rough=5)
    refl = np.flipud(art[:, :, 3] * (yy < 440))[(H - 2 * 452):, :] if False else None
    rm2 = np.zeros((H, W), np.float32)
    src = np.maximum.reduce([rm, wm, stilts])
    for y in range(452, H):
        sy = 2 * 452 - y - 20
        if 0 <= sy < H:
            rm2[y] = src[sy]
    rm2 = displace(gaussian_filter(rm2, (1.5, 3)), 21, 4, 12) * np.clip((H - yy) / 80, 0, 1)
    art = G(art, rm2 * water, "#3d3a2c", seed=nx(), density=0.4, edge=0, bloom=0.3, rough=2)
    rip = strokes(W, H, [([(x, y), (x + rng.uniform(20, 60), y)], rng.uniform(1, 2), (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(462, H - 10)) for _ in range(60)]])
    art = G(art, rip * water, "#d6dccb", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=0.6)
    # a long boat (ces) moored at the ladder
    boat = poly(W, H, [(300, 470), (520, 468), (500, 480), (322, 482)])
    art = GP(art, boat, "#6a4a30", "#4a3424", seed=nx(), rough=0.8)
    art = G(art, strokes(W, H, [(curve([(304, 470), (410, 466), (518, 468)], 20), 2.4, (0.1, 0.1))]), "#b89a6e", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    # ferns at the bank
    ferns = []
    for fx in list(range(0, 160, 22)) + list(range(780, W, 22)):
        for k in range(5):
            a = -math.pi / 2 + rng.uniform(-1.1, 1.1); L = rng.uniform(26, 60)
            ferns.append((curve([(fx, 452), (fx + math.cos(a) * L * 0.6, 452 + math.sin(a) * L * 0.7), (fx + math.cos(a) * L, 452 + math.sin(a) * L + 14)], 12), rng.uniform(3, 6), (0.05, 0.6)))
    art = G(art, strokes(W, H, ferns), "#3e5e3c", "#5d7c45", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=1.5)
    art[..., 3] *= vignette_mask(W, H, 15, inset=8, rough=22, fade=26)
    preview(art, "lamin", tone="#efe5cf")
    save(art, f"{OUT}/lamin.webp", max_w=820, quality=80)
    clear()

if "daun" in PARTS:
    import _jw_lib as jw
    jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = "#5f7f4f", "#36573a", "#22392a"
    W, H = 440, 420
    nx = Seq(95100); rng = random.Random(3)
    art = blank(W, H)
    # rattan tendril + long forest leaves hanging from the upper left
    art = G(art, strokes(W, H, [(curve([(0, 30), (120, 60), (230, 40), (330, 90), (400, 70)], 40), 3.2, (0.0, 0.4))]), "#7a6440", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.8)
    spec = [(10, 24, 200, 1.15), (40, 34, 180, 0.7), (110, 50, 170, 1.35), (180, 46, 150, 0.95), (250, 66, 130, 1.45), (320, 84, 100, 1.1), (70, 36, 160, 1.7), (150, 54, 120, 0.45), (370, 76, 80, 1.6)]
    for i, (x, y, L, a) in enumerate(spec):
        pts = curve([(x, y), (x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5 - 8), (x + math.cos(a + 0.3) * L, y + math.sin(a + 0.3) * L)], 18)
        if i % 3 == 2:
            jw.LEAF_A, jw.LEAF_B = "#7f9c5e", "#4d6f40"
        else:
            jw.LEAF_A, jw.LEAF_B = "#4f7346", "#2f5034"
        art = jw.banana(art, W, H, pts, L * 0.2, rng, nx, tear=i % 2 == 0)
    for (x, y, L, a) in [(240, 64, 70, 1.9), (300, 84, 60, 0.4), (150, 60, 66, 2.2), (390, 78, 54, 1.6), (60, 40, 70, 2.4)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx, c=("#86a262", "#4f7042"))
    preview(art, "daun")
    save(art, f"{OUT}/daun.webp", max_w=360, quality=80)
    clear()
