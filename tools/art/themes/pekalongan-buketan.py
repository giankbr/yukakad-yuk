"""Pekalongan Buketan — batik pesisir Pekalongan: buket bunga gaya Eropa (mawar, krisan, lili, bunga biru kecil) dengan
kupu-kupu dan burung kecil, digambar canting (garis tipis ungu-tua + cecek) dan diwarnai pastel cerah di atas mori krem.
Run: python3 -I pekalongan-buketan.py [part ...]   parts: buket kupu burung pinggir sprig mori
Assets -> public/themes/art/pekalongan-buketan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m5_lib import *

OUT = outdir("pekalongan-buketan")
PARTS = sys.argv[1:] or ["buket", "kupu", "burung", "pinggir", "sprig", "mori"]
LINE = "#3b2640"
PINK, PINK_D, ROSE_D = "#f4a6bb", "#e97c9c", "#cf4f78"
LILAC, LILAC_D = "#b7a2e2", "#8a72c6"
SKY, SKY_D = "#86c6e6", "#4f9ccb"
YEL, YEL_D = "#f7d06a", "#eda042"
CORAL, CORAL_D = "#f6a585", "#e9775a"
MINT, MINT_D, LEAF_D = "#93cfa8", "#5aa784", "#3e8467"
MORI = "#f8f0e1"


def crackle_on(art, seed, amt=0.22):
    """Fine wax-crackle (remukan) veins only where dye sits."""
    h, w = art.shape[:2]
    n = fbm(w, h, seed, 26, 3)
    c = np.clip(1 - np.abs(n - 0.5) / 0.006, 0, 1) * art[..., 3] * amt
    out = art.copy()
    out[..., :3] = out[..., :3] * (1 - c[..., None]) + np.array(hex_rgb(LINE), np.float32) * c[..., None]
    return out


class Painter:
    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.art = blank(W, H)
        self.rng = random.Random(seed)
        self.nx = Seq(seed * 10)

    def fill(self, polys, col, col2=None, smooth=True, density=0.92, **k):
        m = shapes(self.W, self.H, polys, smooth)
        self.art = D(self.art, m, col, col2, seed=self.nx(), density=density, **k)
        return m

    def outline(self, polys, width=2.2, closed=True, smooth=True, alpha=0.92):
        m = lines(self.W, self.H, polys, width, closed, smooth)
        self.art = K(self.art, m, LINE, seed=self.nx(), alpha=alpha)

    def dots(self, items, col=LINE, alpha=0.9):
        if not items:
            return
        m = circles(self.W, self.H, items)
        self.art = K(self.art, m, col, seed=self.nx(), alpha=alpha)

    def reserve(self, polys, width, closed=False):
        """White wax-reserve lines inside a dyed area (isen)."""
        m = lines(self.W, self.H, polys, width, closed)
        self.art = OV(self.art, m, lambda mm: rgba(flat(*mm.shape, "#fffaf0"), np.clip(gaussian_filter(mm, 0.5) * 0.95, 0, 1)))

    # ---------------------------------------------------------------- motifs
    def leaf(self, x, y, L, ang, Wd=0.36, col=MINT, col2=MINT_D):
        r = self.rng
        poly = wob(petal_pts(x, y, L, L * Wd, ang, n=16, cup=0.0), r, 1.0)
        self.fill([poly], col, col2)
        ex, ey = x + math.cos(ang) * L * 0.92, y + math.sin(ang) * L * 0.92
        vein = curve([(x, y), (x + math.cos(ang + 0.05) * L * 0.5, y + math.sin(ang + 0.05) * L * 0.5), (ex, ey)], 12)
        side = []
        for k in range(1, 7):
            t = k / 7.5
            px, py = x + math.cos(ang) * L * t, y + math.sin(ang) * L * t
            ln = L * Wd * 0.62 * math.sin(math.pi * min(1, t * 1.1))
            for sgn in (1, -1):
                a = ang + sgn * 0.85
                side.append([(px, py), (px + math.cos(a) * ln, py + math.sin(a) * ln)])
        self.outline([poly], 2.0)
        self.outline([vein], 1.6, closed=False)
        self.outline(side, 1.1, closed=False, alpha=0.75)

    def rose(self, cx, cy, R, col=PINK, col2=PINK_D, deep=ROSE_D, rot=0.0):
        """Batik rose: concentric scalloped rings, each a deeper dye, cecek along the inner rims, spiral heart."""
        r = self.rng

        def scallop(rad, n, ph, sq=0.92):
            pts = []
            for k in range(n * 10):
                t = k / (n * 10) * math.tau
                rr = rad * (0.8 + 0.2 * abs(math.sin(n * (t - ph) / 2)) ** 0.6) * (1 + r.uniform(-.012, .012))
                pts.append((cx + math.cos(t + rot) * rr, cy + math.sin(t + rot) * rr * sq))
            return pts
        rings = [(scallop(R, 8, 0.0), col, col2), (scallop(R * 0.74, 7, 0.3), col2, deep), (scallop(R * 0.5, 6, 0.1), deep, mix(deep, LINE, .2))]
        masks = []
        for pts, c1, c2 in rings:
            masks.append(self.fill([pts], c1, c2))
        for m in masks:
            self.art = K(self.art, outline_of(m, 1.9), LINE, seed=self.nx())
        # petal grooves: short strokes from each scallop cusp inward
        gro = []
        for (pts, _, _), n in zip(rings[:2], (8, 7)):
            for k in range(n):
                i = int((k + 0.5) / n * len(pts)) % len(pts)
                if rings[0][0] is pts:
                    i = int((k) / n * len(pts)) % len(pts)
                x, y = pts[i]
                gro.append([(x, y), (x + (cx - x) * 0.22, y + (cy - y) * 0.22)])
        self.outline(gro, 1.5, closed=False, alpha=0.8)
        spir = spiral_pts(cx, cy, R * 0.04, R * 0.36, rot, 2.4, 70, 1)
        self.outline([spir], 1.9, closed=False)
        dd = []
        for (pts, _, _), d in zip(rings, (R * 0.09, R * 0.08, R * 0.07)):
            dd += dots_along(offset_poly(pts, d), max(7, R * 0.075), max(1.3, R * 0.012), rng=r)
        self.dots(dd, "#fff6ea", alpha=0.85)
        self.reserve([arc_pts(cx, cy, R * 0.6, rot + a, rot + a + 0.55, 8, 0.92) for a in np.linspace(0.3, math.tau + .3, 5, endpoint=False)], max(1.6, R * 0.016))

    def krisan(self, cx, cy, R, col=LILAC, col2=LILAC_D, rot=0.0, n=22):
        r = self.rng
        p1 = [wob(petal_pts(cx, cy, R * r.uniform(0.92, 1.04), R * 0.2, rot + k * math.tau / n, n=10), r, 0.6) for k in range(n)]
        self.fill(p1, col, col2)
        p2 = [wob(petal_pts(cx, cy, R * 0.66, R * 0.2, rot + (k + .5) * math.tau / n, n=10), r, 0.6) for k in range(n)]
        self.fill(p2, col2, "#7058b0")
        disc = ellipse_pts(cx, cy, R * 0.24, R * 0.24, 14)
        self.fill([disc], YEL, YEL_D)
        self.outline(p1 + p2, 1.6)
        self.outline([disc], 2.0)
        self.dots([(cx + math.cos(a) * rr, cy + math.sin(a) * rr, 1.7) for rr in (R * .08, R * .15) for a in np.linspace(0, math.tau, int(rr / 3), endpoint=False)])

    def lili(self, cx, cy, R, ang=-math.pi / 2, col=YEL, col2=YEL_D):
        r = self.rng
        petals = [wob(petal_pts(cx, cy, R * (1 if k % 2 == 0 else 0.86), R * 0.36, ang + (k - 2) * 0.48, n=14, cup=-0.1), r, 0.9) for k in range(5)]
        self.fill(petals, col, col2)
        self.outline(petals, 2.0)
        stripes = [[(cx + math.cos(ang + (k - 2) * 0.48) * R * 0.2, cy + math.sin(ang + (k - 2) * 0.48) * R * 0.2),
                    (cx + math.cos(ang + (k - 2) * 0.48) * R * 0.72, cy + math.sin(ang + (k - 2) * 0.48) * R * 0.72)] for k in range(5)]
        self.outline(stripes, 1.3, closed=False, alpha=0.7)
        st = []; tips = []
        for k in range(5):
            a = ang + (k - 2) * 0.2
            tx, ty = cx + math.cos(a) * R * 1.1, cy + math.sin(a) * R * 1.1
            st.append([(cx, cy), (cx + math.cos(a) * R * .6, cy + math.sin(a) * R * .6 - 4), (tx, ty)])
            tips.append(wob(ellipse_pts(tx, ty, 6, 3.5, 8, a), r, 0.4))
        self.outline(st, 1.4, closed=False)
        self.fill(tips, CORAL_D, ROSE_D)

    def kecil(self, cx, cy, R, col=SKY, col2=SKY_D, rot=0.0):
        r = self.rng
        pet = [wob(ellipse_pts(cx + math.cos(rot + k * math.tau / 5) * R * 0.55, cy + math.sin(rot + k * math.tau / 5) * R * 0.55, R * 0.5, R * 0.42, 10, rot + k * math.tau / 5), r, 0.6) for k in range(5)]
        self.fill(pet, col, col2)
        c = ellipse_pts(cx, cy, R * 0.22, R * 0.22, 8)
        self.fill([c], YEL, YEL_D)
        self.outline(pet + [c], 1.6)

    def bud(self, x, y, s, ang, col=PINK, col2=ROSE_D):
        r = self.rng
        b = wob(petal_pts(x, y, s * 1.5, s * 0.8, ang, n=12), r, 0.6)
        self.fill([b], col, col2)
        sep = [wob(petal_pts(x, y, s * 0.9, s * 0.35, ang + d, n=8), r, 0.4) for d in (-0.5, 0.5)]
        self.fill(sep, MINT, LEAF_D)
        self.outline([b] + sep, 1.6)

    def stem(self, pts, width=5.0):
        m = strokes(self.W, self.H, [(curve(pts, 30), width, (0.0, 0.2))])
        self.art = D(self.art, m, MINT_D, LEAF_D, seed=self.nx())
        self.art = K(self.art, outline_of(m, 1.4), LINE, seed=self.nx(), alpha=0.8)


def butterfly(P, cx, cy, s, ang=0.0, cols=(SKY, SKY_D, CORAL)):
    r = P.rng
    up = [rotp([(cx + dx * s, cy + dy * s) for dx, dy in pts], cx, cy, ang) for pts in (
        [(0, 0), (-0.3, -0.6), (-0.85, -0.95), (-1.05, -0.55), (-0.8, -0.05)],
        [(0, 0), (0.3, -0.6), (0.85, -0.95), (1.05, -0.55), (0.8, -0.05)])]
    lo = [rotp([(cx + dx * s, cy + dy * s) for dx, dy in pts], cx, cy, ang) for pts in (
        [(0, 0.05), (-0.7, 0.12), (-0.8, 0.55), (-0.45, 0.8), (-0.1, 0.45)],
        [(0, 0.05), (0.7, 0.12), (0.8, 0.55), (0.45, 0.8), (0.1, 0.45)])]
    P.fill([wob(p, r, 0.8) for p in up], cols[0], cols[1])
    P.fill([wob(p, r, 0.8) for p in lo], cols[2], CORAL_D)
    eyes = [rotp([(cx + dx * s, cy + dy * s)], cx, cy, ang)[0] for dx, dy in ((-0.68, -0.55), (0.68, -0.55), (-0.45, 0.45), (0.45, 0.45))]
    P.fill([ellipse_pts(x, y, s * 0.13, s * 0.13, 10) for x, y in eyes], YEL, YEL_D)
    body = rotp([(cx, cy - 0.45 * s), (cx + 0.07 * s, cy), (cx, cy + 0.7 * s), (cx - 0.07 * s, cy)], cx, cy, ang)
    P.fill([body], LINE, "#5a3a5e")
    P.outline(up + lo, 1.8)
    P.outline([ellipse_pts(x, y, s * 0.13, s * 0.13, 10) for x, y in eyes], 1.3)
    ant = [rotp([(cx, cy - 0.42 * s), (cx + d * 0.18 * s, cy - 0.8 * s), (cx + d * 0.3 * s, cy - 0.95 * s)], cx, cy, ang) for d in (-1, 1)]
    P.outline(ant, 1.3, closed=False)
    dd = []
    for p in up + lo:
        dd += dots_along(offset_poly(p, s * 0.1), 8, 1.3)
    P.dots(dd, alpha=0.7)


if "buket" in PARTS:
    clear()
    W, H = 900, 1060
    P = Painter(W, H, 11)
    r = P.rng
    tie = (452, 880)
    C = (450, 430)
    # stem bundle under the cluster
    for k in range(9):
        x0 = 380 + k * 17
        P.stem([(x0 + r.uniform(-4, 4), 600), ((x0 + tie[0]) / 2, 760), (tie[0] - 36 + k * 9, tie[1] + 120 + r.uniform(-10, 10))], 5.5)
    # buds on arching stems
    for (x, y, a, c1, c2) in ((150, 250, -2.5, PINK, ROSE_D), (760, 240, -0.6, LILAC, LILAC_D), (120, 520, 2.9, CORAL, CORAL_D), (790, 500, 0.2, PINK, ROSE_D)):
        P.stem([(C[0] + (x - C[0]) * 0.4, C[1] + (y - C[1]) * 0.4 + 40), ((C[0] + x) / 2 + (0 if x < C[0] else 0), (C[1] + y) / 2 - 30), (x, y)], 4)
        P.bud(x, y, 24, a, c1, c2)
    # big leaves radiating behind the cluster
    for k in range(16):
        a = -math.pi * 1.02 + k * (math.pi * 1.5 / 15) + r.uniform(-.05, .05)
        rad = 170 + (k % 3) * 25
        x, y = C[0] + math.cos(a) * rad * 0.6, C[1] + math.sin(a) * rad * 0.55
        dark = k % 2 == 0
        P.leaf(x, y, 150 + (k % 3) * 18, a + r.uniform(-.15, .15), 0.36, MINT_D if dark else MINT, LEAF_D if dark else MINT_D)
    for a in (math.pi * 0.62, math.pi * 0.38, math.pi * 0.8, math.pi * 0.2):
        P.leaf(C[0] + math.cos(a) * 120, C[1] + 130 + math.sin(a) * 40, 140, a, 0.34, MINT, MINT_D)
    # hydrangea-like clusters of small blue/lilac flowers between the big heads
    for (x, y, c1, c2, n) in ((320, 560, SKY, SKY_D, 5), (600, 575, LILAC, LILAC_D, 5), (318, 186, SKY, SKY_D, 4), (606, 188, PINK, PINK_D, 4), (160, 400, YEL, YEL_D, 3), (748, 410, SKY, SKY_D, 3)):
        for j in range(n):
            a = j * math.tau / n + r.uniform(0, 1)
            P.kecil(x + math.cos(a) * 30 * (j > 0), y + math.sin(a) * 26 * (j > 0), 26, c1, c2, rot=r.uniform(0, 1))
    P.lili(455, 200, 104)
    P.krisan(262, 340, 104, rot=0.1)
    P.rose(655, 345, 98, CORAL, CORAL_D, "#d0574a", rot=0.6)
    P.rose(450, 450, 150)
    # ribbon bow at the tie
    tx, ty = tie
    loops = [wob([(tx, ty), (tx - 40, ty - 50), (tx - 110, ty - 40), (tx - 95, ty + 10), (tx - 30, ty + 12)], r, 1.0),
             wob([(tx, ty), (tx + 40, ty - 50), (tx + 110, ty - 40), (tx + 95, ty + 10), (tx + 30, ty + 12)], r, 1.0)]
    tails = [wob([(tx - 8, ty + 6), (tx - 50, ty + 90), (tx - 82, ty + 160), (tx - 52, ty + 150), (tx - 30, ty + 170), (tx + 4, ty + 20)], r, 1.0),
             wob([(tx + 8, ty + 6), (tx + 46, ty + 80), (tx + 92, ty + 140), (tx + 60, ty + 140), (tx + 46, ty + 162), (tx - 4, ty + 20)], r, 1.0)]
    P.fill(loops + tails, SKY, SKY_D, smooth=False, density=1.15, mottle=0.12)
    knot = wob(ellipse_pts(tx, ty + 4, 20, 16, 10), r, 0.6)
    P.fill([knot], SKY_D, "#3f86b8")
    P.outline(loops + tails + [knot], 2.0, smooth=False)
    P.reserve([[(tx - 30, ty - 6), (tx - 80, ty - 20)], [(tx + 30, ty - 6), (tx + 80, ty - 20)], [(tx - 30, ty + 60), (tx - 50, ty + 120)], [(tx + 30, ty + 56), (tx + 60, ty + 110)]], 2.0)
    P.dots(dots_along([(tx - 100, ty - 30), (tx - 40, ty - 40)], 9, 1.4, closed=False) + dots_along([(tx + 40, ty - 40), (tx + 100, ty - 30)], 9, 1.4, closed=False))
    # scattered cecek around the bouquet (isen tanahan)
    sc = []
    for _ in range(90):
        a = r.uniform(0, math.tau); d = r.uniform(380, 470)
        x, y = 450 + math.cos(a) * d * 0.95, 450 + math.sin(a) * d * 0.9
        if 10 < x < W - 10 and 10 < y < 820:
            sc.append((x, y, r.uniform(1.6, 2.6)))
    P.dots(sc, ROSE_D, alpha=0.55)
    art = crackle_on(P.art, 77)
    preview(art, "pb-buket", MORI)
    save(art, f"{OUT}/buket.webp", max_w=640, quality=80)

if "kupu" in PARTS:
    clear()
    P = Painter(260, 220, 21)
    butterfly(P, 130, 104, 100, -0.15)
    preview(P.art, "pb-kupu", MORI)
    save(P.art, f"{OUT}/kupu.webp", max_w=130, quality=82)

if "burung" in PARTS:
    clear()
    W, H = 520, 300
    P = Painter(W, H, 31)
    r = P.rng
    # small pesisir bird in flight, long ribboned tail (batik "burung hong kecil" softened into a swallow)
    body = wob([(330, 120), (380, 98), (420, 104), (436, 116), (414, 130), (370, 150), (320, 156), (290, 148)], r, 0.8)
    head = wob(ellipse_pts(420, 110, 22, 19, 12), r, 0.5)
    beak = [(438, 104), (462, 110), (438, 118)]
    wing1 = wob([(360, 118), (330, 60), (300, 22), (318, 70), (290, 40), (300, 90), (270, 70), (300, 122)], r, 0.8)
    wing2 = wob([(372, 112), (370, 60), (382, 14), (388, 58), (402, 30), (398, 82), (414, 64), (396, 118)], r, 0.8)
    tails = []
    for k, (dx, dy, c) in enumerate([(-200, -30, SKY), (-220, 30, PINK), (-180, 70, LILAC)]):
        tails.append((wob(petal_pts(300, 148, abs(dx), 26, math.atan2(dy, dx), n=18, cup=0.3), r, 0.8), c))
    for pts, c in tails:
        P.fill([pts], c, mix(c, LINE, 0.25))
    P.fill([wing2], LILAC, LILAC_D)
    P.fill([body], PINK, PINK_D)
    P.fill([wing1], SKY, SKY_D)
    P.fill([head], CORAL, CORAL_D)
    P.fill([beak], YEL_D, smooth=False)
    P.outline([t[0] for t in tails] + [wing2, body, wing1, head], 1.9)
    P.outline([beak], 1.5, smooth=False)
    P.dots([(428, 106, 3.2)], alpha=1)
    feathers = [arc_pts(310 + k * 9, 50 + k * 12, 14, 0.4, 2.6, 8) for k in range(5)]
    P.outline(feathers, 1.2, closed=False, alpha=0.7)
    dd = []
    for pts, _ in tails:
        dd += dots_along(offset_poly(pts, 7)[2:16], 9, 1.4, closed=False)
    P.dots(dd, alpha=0.7)
    art = crackle_on(P.art, 31)
    preview(art, "pb-burung", MORI)
    save(art, f"{OUT}/burung.webp", max_w=240, quality=82)

if "pinggir" in PARTS:
    # horizontally tileable border band (pinggiran): two rules, untu walang teeth, blossoms on a wavy vine
    clear()
    W, H = 720, 110
    P = Painter(W, H, 41)
    r = P.rng
    per = 180
    P.fill([[(0, 8), (W, 8), (W, 20), (0, 20)], [(0, 92), (W, 92), (W, 104), (0, 104)]], SKY_D, "#3f86b8", smooth=False)
    teeth = []
    for k in range(W // 20):
        x = k * 20
        teeth.append([(x, 92), (x + 10, 78), (x + 20, 92)])
    P.fill(teeth, PINK_D, ROSE_D, smooth=False)
    vine = [(x, 54 + math.sin(x / per * math.tau) * 14) for x in np.linspace(-4, W + 4, 120)]
    m = strokes(W, H, [(vine, 3.2, None)])
    P.art = D(P.art, m, LEAF_D, seed=P.nx())
    for k in range(W // per):
        x0 = k * per
        P.kecil(x0 + 45, 54 + 14, 15, [SKY, LILAC, CORAL, SKY][k % 4], [SKY_D, LILAC_D, CORAL_D, SKY_D][k % 4], rot=k)
        P.kecil(x0 + 135, 54 - 14, 15, [PINK, YEL, PINK, LILAC][k % 4], [PINK_D, YEL_D, PINK_D, LILAC_D][k % 4], rot=k + 1)
        for lx, ly, a in ((x0 + 90, 50, -1.0), (x0 + 90, 58, 2.2), (x0 + 0, 58, 1.0), (x0 + 180 - .01, 50, -2.1)):
            pass
        for lx, ly, a in ((x0 + 88, 52, -0.9), (x0 + 92, 56, 2.25)):
            poly = wob(petal_pts(lx, ly, 26, 9, a, n=12), r, 0.5)
            P.fill([poly], MINT, MINT_D)
            P.outline([poly], 1.3)
    P.outline([[(0, 8), (W, 8)], [(0, 20), (W, 20)], [(0, 92), (W, 92)], [(0, 104), (W, 104)]], 1.4, closed=False, smooth=False)
    P.dots([(x, 30, 1.6) for x in range(6, W, 12)] + [(x, 84 - 0, 0) for x in []], alpha=0.6)
    art = P.art
    bg = rgba(flat(H, W, MORI), np.ones((H, W), np.float32))
    bg = over(bg, art)
    preview(bg, "pb-pinggir", MORI)
    save_full(bg, f"{OUT}/pinggir.webp", size=(540, 83), quality=80)

if "sprig" in PARTS:
    clear()
    W, H = 520, 170
    P = Painter(W, H, 51)
    for x, y, L, a in ((250, 86, 110, math.pi + 0.15), (270, 86, 110, -0.15), (190, 80, 70, math.pi - 0.5), (330, 80, 70, -2.64),
                       (215, 96, 60, math.pi + 0.7), (305, 96, 60, -0.7)):
        P.leaf(x, y, L, a, 0.3, MINT if a > 0 else MINT_D, MINT_D if a > 0 else LEAF_D)
    P.kecil(120, 92, 20, SKY, SKY_D); P.kecil(400, 92, 20, LILAC, LILAC_D, .5)
    P.rose(260, 84, 46, PINK, PINK_D, ROSE_D, 0.3)
    art = crackle_on(P.art, 51)
    preview(art, "pb-sprig", MORI)
    save(art, f"{OUT}/sprig.webp", max_w=260, quality=82)

if "mori" in PARTS:
    # seamless mori (cotton) ground with faint scattered cecek-pitu blossoms
    clear()
    S = 512
    base = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(MORI), np.float32)
    wv = tile_noise(S, S, 3, (0.35, 2.5)) * 0.5 + tile_noise(S, S, 4, (2.5, 0.35)) * 0.5
    low = tile_noise(S, S, 5, 40)
    base *= (0.975 + 0.035 * wv + 0.02 * (low - 0.5))[..., None]
    rr = random.Random(9)
    cv = Canvas(S, S)
    pnt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for _ in range(34):
        x, y = rr.uniform(0, S), rr.uniform(0, S)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                for k in range(7):
                    a = k * math.tau / 6
                    dx, dy = (0, 0) if k == 6 else (math.cos(a) * 4.2, math.sin(a) * 4.2)
                    cv.c.drawCircle(x + ox + dx, y + oy + dy, 1.25, pnt)
    m = cv.array()[..., 3]
    col = np.array(hex_rgb("#c9a9b8"), np.float32)
    a = gaussian_filter(m, 0.4)[..., None] * 0.55
    base = base * (1 - a) + col * a
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8), "RGB")
    img.save(f"{OUT}/mori.webp", "WEBP", quality=72, method=6)
    print("mori", os.path.getsize(f"{OUT}/mori.webp") // 1024, "KB")

kb(OUT)
