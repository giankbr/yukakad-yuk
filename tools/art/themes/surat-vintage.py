"""Surat Vintage — painted assets: wax seal, dried rose (stamp), pressed-flower sprig, ink flourish, laid-paper tile.
Run: python3 -I /tmp/pen/art/themes/surat-vintage.py
Medium: sepia watercolour + iron-gall ink; the seal is opaque wax (gouache base + form shading)."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b_common import *  # noqa

T = "surat-vintage"
D = outdir(T)
nxt = Seeds(300)
rng = random.Random(11)

WAX, WAX_D, WAX_L = "#8f2b22", "#5a1510", "#c0503f"


# ---------- 1. wax seal (blank: initials are live text on top) ----------
def seal():
    W = H = 460
    cx = cy = 230
    r = 170
    # blob with a few drip lobes
    pts = []
    n = 44
    for i in range(n):
        t = i / n * math.tau
        rr = r * (1 + 0.035 * math.sin(t * 5 + 1.3) + 0.02 * math.sin(t * 11))
        pts.append((cx + math.cos(t) * rr, cy + math.sin(t) * rr))
    pts = deform(pts, rng, 2, 0.05)
    m = shape_mask(W, H, pts)
    for ang, dist, rad in [(0.6, 168, 34), (2.4, 172, 26), (4.1, 165, 30), (5.3, 170, 22)]:
        m = np.maximum(m, shape_mask(W, H, deform(ellipse_pts(cx + math.cos(ang) * dist, cy + math.sin(ang) * dist, rad, rad * .8, 9, ang), rng, 2, .08)))
    m = gaussian_filter(m, 1.2); m = np.clip((m - .3) * 2.5, 0, 1)
    art = gouache_paint(m, WAX, "#7d221b", seed=nxt(), rough=2.5, streak=0.2)
    art = shade(art, m, light=(-0.6, -0.8), k=0.75, blur=14, hi="#e07c66", lo="#3a0b08")
    art = shade(art, m, light=(-0.6, -0.8), k=0.4, blur=4, hi="#e8907a", lo="#3a0b08")
    # pressed recess: inner disk, inverted light (rim catches light bottom-right)
    disk = shape_mask(W, H, deform(ellipse_pts(cx, cy, 118, 118, 30), rng, 1, .01))
    rimband = np.clip(gaussian_filter(disk, 3) - gaussian_filter(disk, 9), -1, 1)
    gy, gx = np.gradient(gaussian_filter(disk, 4))
    lit = (gx * 0.6 + gy * 0.8)
    lit = lit / (np.abs(lit).max() + 1e-6)
    hi = np.clip(lit, 0, 1); lo = np.clip(-lit, 0, 1)
    art = tint(art, hi, "#e08670", 0.55)
    art = tint(art, lo, "#2a0705", 0.65)
    # inner pressed ring of the stamp die
    ring = ring_mask(W, H, cx, cy, 100, 4.5, rng, 0.5)
    gy, gx = np.gradient(gaussian_filter(ring, 1.6))
    lit = gx * 0.6 + gy * 0.8; lit = lit / (np.abs(lit).max() + 1e-6)
    art = tint(art, np.clip(lit, 0, 1), "#e48a73", 0.5)
    art = tint(art, np.clip(-lit, 0, 1), "#2a0705", 0.55)
    # slightly darker recessed field
    art = tint(art, gaussian_filter(disk, 6), "#6b1912", 0.25)
    # two leaf sprigs pressed into the bottom of the field
    for side in (-1, 1):
        stem = curve([(cx + side * 12, cy + 82), (cx + side * 52, cy + 66), (cx + side * 80, cy + 34)], 30)
        sm = stroke_mask(W, H, stem, 3.2)
        for k, t in enumerate([0.25, 0.5, 0.75]):
            px, py = stem[int(t * (len(stem) - 1))]
            a = math.atan2(-1, side * 1.1) + side * 0.3 if side > 0 else math.atan2(-1, -1.1) - 0.3
            sm = np.maximum(sm, shape_mask(W, H, petal_pts(px, py, 20 - k * 2, 6, a + (0.6 * side), 10)))
            sm = np.maximum(sm, shape_mask(W, H, petal_pts(px, py, 18 - k * 2, 5.5, a - (0.9 * side) + math.pi * (side < 0) * 0, 10)))
        gy, gx = np.gradient(gaussian_filter(sm, 1.4))
        lit = gx * 0.6 + gy * 0.8; lit = lit / (np.abs(lit).max() + 1e-6)
        art = tint(art, np.clip(lit, 0, 1), "#e48a73", 0.45)
        art = tint(art, np.clip(-lit, 0, 1), "#2a0705", 0.5)
    # soft wax sheen, two low highlights (not glossy plastic)
    sheen = gaussian_filter(shape_mask(W, H, deform(ellipse_pts(cx - 70, cy - 92, 46, 16, 12, -0.6), rng, 2, .1)), 9)
    art = tint(art, sheen * m, "#f2b2a0", 0.35)
    sheen2 = gaussian_filter(shape_mask(W, H, deform(ellipse_pts(cx + 104, cy + 70, 22, 8, 10, -0.9), rng, 2, .1)), 5)
    art = tint(art, sheen2 * m, "#f2b2a0", 0.22)
    # fine wax texture
    g = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), 1.0)
    art[..., :3] *= (0.96 + 0.08 * g)[..., None]
    preview(art, f"{PREV}/sv-seal.png", "#e9d8b3")
    save(art, f"{D}/seal.webp", max_w=220, q=84, trim=False)


# ---------- 2. dried rose (stamp face) ----------
def rose_head(art, W, H, cx, cy, r, light, mid, deep):
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * 0.86, 10), rng, 2, 0.12))
    art = glaze(art, pigment(base, light, mid, seed=nxt(), density=0.55, edge=0.45, bloom=0.4, rough=max(2, r * .05), holes=0.05))
    for k in range(8):
        rr = r * (0.92 - k * 0.1)
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .04), cy + rng.gauss(0, r * .04), rr, a0, a0 + rng.uniform(1.5, 2.6), 22, 0.84)
        sm = stroke_mask(W, H, pts, r * rng.uniform(0.1, 0.18))
        col = mix(mid, deep, k / 8)
        art = glaze(art, pigment(sm, col, mix(col, light, .3), seed=nxt(), density=0.45 + k * 0.04, edge=0.6, bloom=0.15, rough=max(1.5, r * .02), feather=1.0))
    heart = shape_mask(W, H, ellipse_pts(cx, cy, r * .16, r * .12, 8))
    art = glaze(art, pigment(heart, deep, seed=nxt(), density=0.75, edge=0.7, bloom=0, rough=2))
    return art, base


def leaf(art, W, H, x, y, L, a, ca, cb, wdt=0.32):
    m = shape_mask(W, H, petal_pts(x, y, L, L * wdt, a, n=10))
    art = glaze(art, pigment(m, ca, cb, seed=nxt(), density=0.7, edge=0.55, bloom=0.35, rough=max(2, L * .03), holes=0.04))
    half = shape_mask(W, H, petal_pts(x, y, L * 0.95, L * wdt * .45, a + 0.07, n=10))
    art = glaze(art, pigment(half, cb, seed=nxt(), density=0.3, edge=0.3, bloom=0.2, rough=2))
    return art


def stem(art, W, H, pts, wdt, col):
    return glaze(art, pigment(stroke_mask(W, H, pts, wdt, (0.05, 0.3)), col, mix(col, "#2a2416", .3), seed=nxt(), density=0.75, edge=0.4, bloom=0, rough=1.5, feather=0.8))


def stamp_rose():
    W, H = 300, 360
    art = blank(W, H)
    art = stem(art, W, H, curve([(150, 345), (146, 260), (152, 180), (150, 140)], 40), 7, "#5c6340")
    art = leaf(art, W, H, 148, 262, 92, math.pi + 0.55, "#8a9161", "#5e6a3f")
    art = leaf(art, W, H, 152, 224, 84, -0.45, "#959a68", "#646e43")
    head = shape_mask(W, H, ellipse_pts(150, 112, 74, 64, 16))
    art = knockout(art, head, amount=1.0, grow=2)
    art, _ = rose_head(art, W, H, 150, 112, 78, "#d98a77", "#b4503f", "#6e1f18")
    preview(art, f"{PREV}/sv-rose.png", "#e4d3ae")
    save(art, f"{D}/rose.webp", max_w=120, q=84)


# ---------- 3. pressed-flower sprig (cover + closing) ----------
def sprig():
    W, H = 900, 560
    rng.seed(21)
    olive, olive_d = "#7b8352", "#4f5833"
    sage, sage_d = "#8f9468", "#5d6442"
    stems_l = blank(W, H)
    leaves_l = blank(W, H)
    heads = blank(W, H)
    head_area = np.zeros((H, W), np.float32)
    origin = (150, 470)
    spec = [  # end point, width, kind
        ((560, 150), 4.6, "rose"), ((690, 270), 4.0, "rose2"), ((470, 95), 3.4, "bud"),
        ((770, 360), 3.0, "breath"), ((780, 190), 3.0, "lav"), ((640, 420), 2.8, "breath"), ((380, 120), 3.0, "leafy")]
    ends = []
    for (ex, ey), w, kind in spec:
        mx = origin[0] + (ex - origin[0]) * .5 + rng.uniform(-18, 18)
        my = origin[1] + (ey - origin[1]) * .5 + rng.uniform(14, 36)
        pts = curve([origin, (mx, my), (ex, ey)], 60)
        stems_l = stem(stems_l, W, H, pts, w, olive_d)
        ends.append((pts, kind))
        # leaves attached along the stem
        n_leaf = 3 if kind in ("rose", "rose2", "leafy") else 1
        for j in range(n_leaf):
            t = 0.3 + j * 0.18 + rng.uniform(-.04, .04)
            i = int(t * (len(pts) - 1))
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            tang = math.atan2(y1 - y0, x1 - x0)
            side = 1 if j % 2 else -1
            L = rng.uniform(62, 90) * (1.15 if kind == "leafy" else 1)
            ca, cb = (olive, olive_d) if j % 2 else (sage, sage_d)
            leaves_l = leaf(leaves_l, W, H, x0, y0, L, tang + side * rng.uniform(0.5, 0.8), ca, cb, 0.3)
    for pts, kind in ends:
        ex, ey = pts[-1]
        if kind == "rose":
            heads, a = rose_head(heads, W, H, ex, ey, 66, "#e2ad98", "#b8644f", "#6e2219"); head_area = np.maximum(head_area, a)
        elif kind == "rose2":
            heads, a = rose_head(heads, W, H, ex, ey, 50, "#e8c0a8", "#c48467", "#7a3324"); head_area = np.maximum(head_area, a)
        elif kind == "bud":
            m = shape_mask(W, H, deform(ellipse_pts(ex, ey, 20, 28, 9, -0.7), rng, 2, .1))
            heads = glaze(heads, pigment(m, "#c97a64", "#8e3a2c", seed=nxt(), density=0.7, edge=0.6, rough=3)); head_area = np.maximum(head_area, m)
            sep = np.maximum(shape_mask(W, H, petal_pts(ex - 6, ey + 20, 26, 6, 2.2, 9)), shape_mask(W, H, petal_pts(ex + 4, ey + 22, 24, 6, 0.9, 9)))
            heads = glaze(heads, pigment(sep, olive, olive_d, seed=nxt(), density=0.75, edge=0.5, rough=2))
        elif kind == "breath":
            d = [(ex + rng.gauss(0, 30), ey + rng.gauss(0, 24), rng.uniform(3.5, 7.5)) for _ in range(30)]
            for (x, y, r) in d[::3]:
                stems_l = stem(stems_l, W, H, [(ex - 20, ey + 16), (x, y)], 1.6, olive_d)
            heads = glaze(heads, pigment(dots_mask(W, H, d), "#efe3c6", "#d8c29a", seed=nxt(), density=0.9, edge=0.7, bloom=0, rough=1.5, feather=0.6))
            heads = glaze(heads, pigment(dots_mask(W, H, [(x + 1, y + 1, r * .4) for (x, y, r) in d[::2]]), "#b48c62", seed=nxt(), density=0.55, edge=0.3, bloom=0, rough=1, feather=0.5))
        elif kind == "lav":
            bm = np.zeros((H, W), np.float32)
            seg = pts[int(len(pts) * .55):]
            for i, (x, y) in enumerate(seg[::2]):
                tang = math.atan2(pts[-1][1] - pts[0][1], pts[-1][0] - pts[0][0])
                bm = np.maximum(bm, shape_mask(W, H, petal_pts(x, y, 28, 9, tang + (0.6 if i % 2 else -0.6), 9)))
            heads = glaze(heads, pigment(bm, "#9b8590", "#715c6a", seed=nxt(), density=0.78, edge=0.55, bloom=0.2, rough=2))
    leaves_l = knockout(leaves_l, head_area, amount=0.9, grow=3)
    stems_l = knockout(stems_l, head_area, amount=1.0, grow=3)
    art = glaze(glaze(stems_l, leaves_l), heads)
    # twine bow around the bundle
    tw = stroke_mask(W, H, curve([(200, 405), (222, 428), (236, 452)], 24), 5)
    tw = np.maximum(tw, stroke_mask(W, H, curve([(214, 440), (190, 470), (150, 482), (128, 470)], 30), 4))
    tw = np.maximum(tw, stroke_mask(W, H, curve([(214, 440), (236, 480), (226, 520), (240, 545)], 30), 3.6))
    tw = np.maximum(tw, stroke_mask(W, H, curve([(214, 440), (182, 500), (170, 535)], 30), 3.6))
    art = glaze(art, pigment(tw, "#b28a5a", "#8d6a42", seed=nxt(), density=0.88, edge=0.5, bloom=0, rough=1.5, feather=0.7))
    preview(art, f"{PREV}/sv-sprig.png", "#f2e7cd")
    save(art, f"{D}/sprig.webp", max_w=460, q=82)


# ---------- 4. ink flourish divider ----------
def flourish():
    W, H = 640, 90
    cy = 46
    pts_l = curve([(16, cy + 2), (120, cy + 1), (220, cy - 2), (262, cy - 16), (288, cy - 20), (300, cy - 8), (286, cy + 4), (270, cy - 6), (282, cy - 18)], 120)
    m = stroke_mask(W, H, pts_l, 4.2, (0.5, 0.15))
    pts_r = [(W - x, y + rng.uniform(-0.3, 0.3)) for x, y in pts_l]
    m = np.maximum(m, stroke_mask(W, H, pts_r, 4.0, (0.5, 0.15)))
    # centre lozenge
    m = np.maximum(m, shape_mask(W, H, deform([(320, cy - 15), (331, cy), (320, cy + 15), (309, cy)], rng, 1, .04), smooth=False))
    art = ink(m, "#7a2a1f", nxt(), 0.92, 1.4)
    preview(art, f"{PREV}/sv-flourish.png", "#f2e7cd")
    save(art, f"{D}/flourish.webp", max_w=320, q=84)


# ---------- 5. laid-paper grain overlay (replaces the SVG feTurbulence noise) ----------
def paper_tex():
    S = 256
    t = grain_overlay(S, "#4a3018", seed=7, base=0.008, k=1.3, cap=0.09, laid=0.004, fox=4, fox_col="#a77a45", fiber=0.35, mottle=0.6)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["seal", "rose", "sprig", "flourish", "paper"]
    for w in which:
        {"seal": seal, "rose": stamp_rose, "sprig": sprig, "flourish": flourish, "paper": paper_tex}[w]()
