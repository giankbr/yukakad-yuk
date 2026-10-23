"""Safir Malam — sapphire night, pressed-silver linework: a sparse 8-point khatam rosette, a slim crescent, small
8-point star knots, silver hairline dividers, a painted sapphire sky with very few silver specks.
Run: python3 -I safir-malam.py [part ...]   parts: sky rosette crescent star divider band
Assets -> public/themes/art/safir-malam/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h5_lib import *

OUT = outdir("safir-malam")
PARTS = sys.argv[1:] or ["sky", "rosette", "crescent", "star", "divider", "band"]
SEQ = Seq(300)
NAVY, NAVY_D, NAVY_L = "#13254a", "#0b1733", "#1f3a6e"
SILVER = "#cdd4de"


def sky():
    W, H = 600, 1300
    arr = painted_sky(W, H, [(0, "#0a1530"), (0.45, "#13254a"), (0.8, "#172d5a"), (1, "#1c3566")], seed=4, streak=0.9, grain=0.7)
    # soft watery clouds of deeper/lighter sapphire
    for k, (cy, col, d) in enumerate([(260, "#0b1838", 0.22), (720, "#21407a", 0.14), (1080, "#0f1f44", 0.18)]):
        m = shape_mask(W, H, deform(ellipse_pts(300 + (k - 1) * 90, cy, 380, 120, 12), random.Random(k), 3, 0.2))
        arr = G(arr, m, col, seed=SEQ(), density=d, edge=0.25, bloom=0.5, gran=0.35, rough=14, feather=8)
        flush()
    # a few silver specks (sparse, not a starfield)
    rng = random.Random(9)
    pts = [(rng.uniform(10, W - 10), rng.uniform(10, H * 0.75), rng.uniform(0.8, 1.8)) for _ in range(46)]
    cm = circles(W, H, pts)
    arr = over(arr, glow(cm, "#dfe7f5", radius=2.2, strength=0.6))
    arr = over(arr, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#eef2f8"), np.float32), (cm * 0.85)[..., None]], -1))
    arr[..., 3] = 1
    save_rgb(arr, f"{OUT}/sky.webp", quality=72)


def offset_poly(pts, d):
    """Offset a convex closed polygon (CCW/CW agnostic) by d along vertex bisectors."""
    cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
    out = []
    n = len(pts)
    for i in range(n):
        x, y = pts[i]
        # move along the direction away from the centre, scaled for the corner angle
        ax, ay = pts[i - 1]; bx, by = pts[(i + 1) % n]
        e1 = math.atan2(y - ay, x - ax); e2 = math.atan2(by - y, bx - x)
        half = (e2 - e1) / 2
        k = 1 / max(0.3, math.cos(half))
        vx, vy = x - cx, y - cy; L = math.hypot(vx, vy) or 1
        out.append((x + vx / L * d * k, y + vy / L * d * k))
    return out


def strap(W, H, polys, b, lw, crossings, over_first=True):
    """Interlaced double-line straps along polygons; at each crossing (x, y, top_index) the under strap is cut."""
    lines, areas = [], []
    for P in polys:
        lines.append(poly_outline(W, H, [offset_poly(P, b / 2), offset_poly(P, -b / 2)], lw))
        ring = np.clip(shapes(W, H, [offset_poly(P, b / 2 + lw * 0.6)], smooth=False) - shapes(W, H, [offset_poly(P, -b / 2 - lw * 0.6)], smooth=False), 0, 1)
        inner = np.clip(shapes(W, H, [offset_poly(P, b / 2 - lw * 0.8)], smooth=False) - shapes(W, H, [offset_poly(P, -b / 2 + lw * 0.8)], smooth=False), 0, 1)
        areas.append((ring, inner))
    out = np.zeros((H, W), np.float32)
    for i, L in enumerate(lines):
        cut = np.zeros((H, W), np.float32)
        for (x, y, top) in crossings:
            near = circles(W, H, [(x, y, b * 2.2)])
            if top != i:
                cut = np.maximum(cut, near * areas[top][0])
        out = np.maximum(out, L * (1 - cut))
    return out


def seg_cross(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if abs(d) < 1e-9:
        return None
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
    if 0 < t < 1 and 0 < u < 1:
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
    return None


def crossings_of(A, B, cx, cy):
    pts = []
    for i in range(len(A)):
        for j in range(len(B)):
            c = seg_cross(A[i], A[(i + 1) % len(A)], B[j], B[(j + 1) % len(B)])
            if c:
                pts.append(c)
    pts.sort(key=lambda q: math.atan2(q[1] - cy, q[0] - cx))
    return [(x, y, k % 2) for k, (x, y) in enumerate(pts)]


def rosette_masks(W, H, cx, cy, R):
    """Sparse khatam rosette in interlaced double-line strapwork: two squares (8-point star), an inner 8-point star,
    a fine double ring and eight small studs."""
    sq1 = [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
    sq2 = [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in [k * math.pi / 2 for k in range(4)]]
    b = R * 0.045
    m = strap(W, H, [sq1, sq2], b, 2.2, crossings_of(sq1, sq2, cx, cy))
    inner = star8_pts(cx, cy, R * 0.52, R * 0.4, rot=math.pi / 8)
    m = np.maximum(m, poly_outline(W, H, [inner, offset_poly(inner, -b)], 2.0))
    m = np.maximum(m, poly_outline(W, H, [star8_pts(cx, cy, R * 0.2, R * 0.15, rot=0)], 2.0))
    m = np.maximum(m, ring_mask(W, H, cx, cy, R * 1.1, 1.6))
    m = np.maximum(m, ring_mask(W, H, cx, cy, R * 1.13, 1.0) * 0.8)
    m = np.maximum(m, circles(W, H, [(cx + math.cos(k * math.pi / 4 + math.pi / 8) * R * 1.115, cy + math.sin(k * math.pi / 4 + math.pi / 8) * R * 1.115, 4.6) for k in range(8)] + [(cx, cy, 4)]))
    return np.clip(m, 0, 1)


def rosette():
    W = H = 820
    m = rosette_masks(W, H, 410, 410, 340)
    m = displace(m, 5, 1.2, 30)
    lay = glow(m, "#9fb2d6", radius=5, strength=0.25)
    lay = SV(lay, m, seed=SEQ())
    preview(lay, "sm-rosette", bg=NAVY)
    save(lay, f"{OUT}/rosette.webp", max_w=520, quality=80)


def crescent():
    W = H = 420
    cv = Canvas(W, H)
    p = skia.Path()
    p.addCircle(210, 210, 150)
    q = skia.Path(); q.addCircle(262, 176, 132)
    res = skia.Op(p, q, skia.PathOp.kDifference_PathOp)
    cv.c.drawPath(res, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    m = cv.array()[..., 3]
    lay = glow(m, "#b9c8e6", radius=22, strength=0.22)
    lay = SV(lay, m, seed=SEQ(), emboss=0.8, sparkle=0.1)
    # faint lunar mottling
    mot = fbm(W, H, 77, 30, 3)
    lay[..., :3] *= np.where(m[..., None] > 0.5, 0.92 + 0.12 * mot[..., None], 1)
    preview(lay, "sm-crescent", bg=NAVY)
    save(lay, f"{OUT}/crescent.webp", max_w=240, quality=82)


def star():
    W = H = 200
    polys = [star8_pts(100, 100, 86, 64, rot=0)]
    sq1 = [(100 + math.cos(a) * 86, 100 + math.sin(a) * 86) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
    sq2 = [(100 + math.cos(a) * 86, 100 + math.sin(a) * 86) for a in [k * math.pi / 2 for k in range(4)]]
    m = poly_outline(W, H, [sq1, sq2], 4.2)
    inner = shape_mask(W, H, star8_pts(100, 100, 34, 24, rot=math.pi / 8), smooth=False)
    m = np.clip(m + inner, 0, 1)
    lay = glow(m, "#b9c8e6", radius=6, strength=0.25)
    lay = SV(lay, m, seed=SEQ(), emboss=0.7, sparkle=0.0)
    preview(lay, "sm-star", bg=NAVY)
    save(lay, f"{OUT}/star.webp", max_w=96, quality=84)


def divider():
    W, H = 900, 80
    cx, cy = 450, 40
    line = strokes(W, H, [([(30, cy), (cx - 46, cy)], 2.0, (0.6, 0.0)), ([(cx + 46, cy), (W - 30, cy)], 2.0, (0.0, 0.6))])
    sq1 = [(cx + math.cos(a) * 26, cy + math.sin(a) * 26) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
    sq2 = [(cx + math.cos(a) * 26, cy + math.sin(a) * 26) for a in [k * math.pi / 2 for k in range(4)]]
    st = poly_outline(W, H, [sq1, sq2], 2.4)
    dots = circles(W, H, [(cx - 70, cy, 3.4), (cx + 70, cy, 3.4), (cx, cy, 4.0)])
    m = np.clip(line + st + dots, 0, 1)
    lay = FO(blank(W, H), m, "#6f7f9c", seed=SEQ(), emboss=0.4, sparkle=0.05)
    preview(lay, "sm-divider", "#eef1f6")
    save(lay, f"{OUT}/divider.webp", max_w=440, quality=84)


def band():
    """Sparse repeating border band: a chain of tiny 8-point stars joined by a double hairline (tileable horizontally)."""
    W, H = 480, 60
    polys, items = [], []
    for k in range(4):
        cx = 60 + k * 120
        polys.append(star8_pts(cx, 30, 20, 12, rot=0))
    items += [([(0, 24), (W, 24)], 1.4, None), ([(0, 36), (W, 36)], 1.4, None)]
    m = np.clip(poly_outline(W, H, polys, 2.0) + strokes(W, H, items), 0, 1)
    # cut lines inside stars
    inside = shapes(W, H, polys, smooth=False)
    m = np.where(inside > 0.5, poly_outline(W, H, polys, 2.0), m)
    lay = SV(blank(W, H), m, seed=SEQ(), emboss=0.4, sparkle=0.05)
    preview(lay, "sm-band", bg=NAVY)
    save_full(lay, f"{OUT}/band.webp", size=(240, 30), quality=84)


for part in PARTS:
    {"sky": sky, "rosette": rosette, "crescent": crescent, "star": star, "divider": divider, "band": band}[part]()
    flush()
kb(OUT)
