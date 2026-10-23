"""Ukir Jepara — deep-relief Jepara teak carving (floral only): a carved panel with lung-lungan vines, acanthus-like
serrated leaves, layered blossoms and a smooth polished cartouche for the names, lit by a raking light from the upper
left; pierced carved corner spray, a vine divider, a carved blossom, and a seamless teak grain tile.
Run: python3 -I ukir-jepara.py [part ...]   parts: panel ukel garis kembang kayu. Assets -> public/themes/art/ukir-jepara/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h2_lib import *

OUT = outdir("ukir-jepara")
PARTS = sys.argv[1:] or ["panel", "ukel", "garis", "kembang", "kayu"]
BG = "#1a0d06"
WARM = [(0, "#2a1104"), (0.3, "#5e2e0e"), (0.55, "#9c5722"), (0.76, "#cf8a46"), (0.9, "#efb46c"), (1.0, "#ffdc9e")]


class Relief:
    """Accumulates a carving: stems (round), leaves (domed with vein groove), petals (cupped)."""
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.stems, self.leaves, self.veins, self.petals, self.cores = [], [], [], [], []

    def stem(self, pts, width, taper=(0.05, 0.35)):
        self.stems.append((pts, width, taper))

    def leaf(self, x, y, L, Wd, ang, curl=0.0, lobes=4):
        lobes = max(lobes, 3)
        self.leaves.append(serrated_leaf(x, y, L, Wd, ang, lobes=lobes, depth=0.42, curl=curl))
        self.veins.append((leaf_vein(x, y, L, ang, curl), max(1.2, Wd * 0.11), (0.0, 0.6)))
        ca, sa = math.cos(ang), math.sin(ang)
        for i in range(1, lobes):
            t = i / lobes
            u0 = t * L * 0.86; v0 = curl * L * (t * 0.86) ** 2
            base = math.sin(math.pi * t ** 0.8) * Wd * (1 - 0.15 * t)
            for side in (1, -1):
                u1 = (t + 0.12) * L; v1 = side * base * 0.78 + curl * L * (t + 0.12) ** 2
                p0 = (x + u0 * ca - v0 * sa, y + u0 * sa + v0 * ca); p1 = (x + u1 * ca - v1 * sa, y + u1 * sa + v1 * ca)
                self.veins.append(([p0, p1], max(1.0, Wd * 0.07), (0.0, 0.7)))

    def flower(self, x, y, r, petals=6, rot=0.0, layers=2):
        r *= 1.18
        for ly in range(layers):
            rr = r * (1 - ly * 0.42)
            for k in range(petals):
                a = rot + (k + ly * 0.5) / petals * math.tau
                self.petals.append((ly, serrated_leaf(x + math.cos(a) * rr * 0.12, y + math.sin(a) * rr * 0.12, rr, rr * 0.42, a, lobes=2, depth=0.18)))
        self.cores.append((x, y, r * 0.2))

    def tendril(self, x, y, r, a0, d=1, width=3.0):
        self.stems.append((coil(x, y, r, 1.4, a0, d=d), width, (0.0, 0.8)))

    def scroll(self, x, y, s, ang, flip=1):
        it, lv = lung(x, y, s, ang, flip)
        for pts, wdt, tp in it:
            self.stems.append((pts, wdt * 1.25, tp))
        for poly in lv:
            self.leaves.append(poly)

    def height(self):
        W, H = self.W, self.H
        stems = strokes(W, H, self.stems) if self.stems else np.zeros((H, W), np.float32)
        leaves = shapes(W, H, self.leaves) if self.leaves else np.zeros((H, W), np.float32)
        veins = strokes(W, H, self.veins) if self.veins else np.zeros((H, W), np.float32)
        h = gaussian_filter(stems, 2.6) * 1.15
        hl = gaussian_filter(leaves, 3.2) * 0.95 - gaussian_filter(veins, 1.0) * 0.35
        h = np.maximum(h, hl)
        for ly in (0, 1):
            ps = [p for l, p in self.petals if l == ly]
            if ps:
                pm = shapes(W, H, ps)
                cup = gaussian_filter(pm, 6.0)
                h = np.maximum(h, gaussian_filter(pm, 2.2) * (0.85 + ly * 0.4) - np.clip(cup - 0.55, 0, 1) * 0.5)
        if self.cores:
            cm = circles(W, H, self.cores)
            h = np.maximum(h, gaussian_filter(cm, 2.0) * 1.5)
        mask = np.clip(np.maximum.reduce([stems, leaves, circles(W, H, self.cores) if self.cores else stems * 0, shapes(W, H, [p for _, p in self.petals]) if self.petals else stems * 0]), 0, 1)
        return h, mask


def half_vine(R, W, H, flip_x):
    """Left half of the panel's symmetric vine; flip_x mirrors coordinates (with its own small variations)."""
    X = (lambda x: x) if not flip_x else (lambda x: W - x)
    F = 1 if not flip_x else -1
    rng = random.Random(3 if not flip_x else 4)
    j = lambda v=4: rng.uniform(-v, v)
    A = lambda a: a if not flip_x else math.pi - a  # mirror an angle
    for top in (False, True):
        Y = (lambda y: y) if not top else (lambda y: H - y)
        V = 1 if not top else -1
        Aa = (lambda a: A(a)) if not top else (lambda a: A(-a))
        stem = curve([(X(W / 2 - 6), Y(H - 52)), (X(W / 2 - 90), Y(H - 92)), (X(168), Y(H - 150)), (X(92), Y(H - 250)), (X(84), Y(H - 360)), (X(124), Y(H - 420)), (X(160 + j()), Y(H - 404))], 90)
        R.stem(stem, 20, (0.03, 0.25))
        for k, (x, y, a) in enumerate(along(stem, 36)):
            if k < 1:
                continue
            off = 1 if k % 2 else -1
            L = 120 - k * 6 + j(10)
            Wd = 40 - k * 1.6
            la = a + off * (1.0 + rng.uniform(-0.2, 0.2))
            # leaves only on the outer side once the stem runs up the narrow side column
            if k > 7 and ((x - W / 2) * (-1 if not flip_x else 1) < 0) is False and off < 0:
                continue
            R.leaf(x, y, max(46, L * (0.6 if k > 7 else 1.0)), max(16, Wd * (0.65 if k > 7 else 1.0)), la, curl=off * 0.32, lobes=4)
        # secondary branch from the lower sweep into the bottom band, ending in a bud and scroll
        br = curve([(X(214), Y(H - 128)), (X(250), Y(H - 190)), (X(232), Y(H - 238)), (X(196), Y(H - 232))], 40)
        R.stem(br, 12, (0.05, 0.5))
        R.tendril(X(196), Y(H - 232), 14, Aa(math.pi), d=-F * V, width=5)
        for k, (x, y, a) in enumerate(along(br, 34)):
            off = 1 if k % 2 else -1
            R.leaf(x, y, 70 - k * 6, 24, a + off * 1.1, curl=off * 0.3, lobes=3)
        R.flower(X(176), Y(H - 156), 64, 6, 0.3 + j(0.2) * 0.1)
        R.flower(X(278), Y(H - 238), 32, 5, 0.1)
        # outer corner scroll
        R.scroll(X(84), Y(H - 92), 46, Aa(-0.7), F * V)
        R.leaf(X(60), Y(H - 160), 70, 22, Aa(-1.9), curl=0.3, lobes=3)
    # side blossom halfway, with leaves above and below
    R.flower(X(86), H / 2, 44, 6, 0.2)
    R.leaf(X(110), H / 2 - 52, 80, 26, A(-1.25), curl=0.3, lobes=3)
    R.leaf(X(110), H / 2 + 52, 80, 26, A(1.25), curl=-0.3, lobes=3)
    R.leaf(X(140), H / 2, 54, 18, A(0.0), curl=0.2, lobes=2)


if "panel" in PARTS:
    W, H = 640, 880
    cx, cy = W / 2, H / 2
    R = Relief(W, H)
    half_vine(R, W, H, False)
    half_vine(R, W, H, True)
    # central top and bottom blossoms on the axis
    R.flower(cx, 96, 58, 8, -math.pi / 2)
    R.flower(cx, H - 96, 58, 8, math.pi / 2)
    for sy in (1, -1):
        y0 = 96 if sy > 0 else H - 96
        for sx in (-1, 1):
            R.leaf(cx + sx * 50, y0 + sy * 46, 92, 30, (math.pi / 2 - sx * 0.9) * sy if sy > 0 else -(math.pi / 2 - sx * 0.9), curl=sx * 0.3, lobes=3)
            R.leaf(cx + sx * 60, y0 - sy * 8, 84, 26, (0 if sx > 0 else math.pi) - sx * sy * 0.35, curl=-sx * sy * 0.25, lobes=3)
    hv, vmask = R.height()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # frame: outer moulding (stepped bevel) + inner bead
    fw = 34
    frame_out = np.ones((H, W), np.float32)
    inner = ((xx > fw) & (xx < W - fw) & (yy > fw) & (yy < H - fw)).astype(np.float32)
    dist = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy])
    mould = np.clip(1 - inner, 0, 1) * (0.75 + 0.35 * np.sin(np.clip(dist / fw, 0, 1) * math.pi) - 0.2 * ((dist > 12) & (dist < 16)))
    bead = np.clip(1 - np.abs(dist - (fw + 7)) / 4, 0, 1) * 0.7
    # cartouche: smooth raised oval with a bevelled rim
    rx, ry = 176, 150
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    cart = np.clip((1 - d) * 18, 0, 1)
    rim = np.clip(1 - np.abs(d - 1.0) * 22, 0, 1)
    cart_h = cart * (0.62 + 0.05 * (1 - d)) + rim * 0.38
    # ground: chisel-textured recess, vine relief cut back near the cartouche
    ground = (fbm(W, H, 5, 6, 3) - 0.5) * 0.06 + (fbm(W, H, 9, 30, 2) - 0.5) * 0.05 + np.sin((xx * 0.8 + yy * 0.6) * 0.9 + fbm(W, H, 13, 20, 2) * 6) * 0.012 - 0.15
    hv = hv * np.clip((d - 1.06) * 8, 0, 1)
    h = np.maximum.reduce([ground, gaussian_filter(mould, 1.2) * 1.1, bead, hv * 0.95, gaussian_filter(cart_h, 1.0)])
    h = gaussian_filter(h, 0.7)
    stops = [(0, "#120602"), (0.25, "#3d1a07"), (0.5, "#8a4a1c"), (0.72, "#c47c3c"), (0.88, "#e9a964"), (1.0, "#ffd89a")]
    art = relief_rgba(h, np.ones((H, W), np.float32), 11, stops, strength=6.5, cast=(6, 8), cast_amt=0.6, spot=(W * 0.34, H * 0.28, W * 1.05, 0.7))
    # polished cartouche: lighter, with visible flame grain and a soft sheen
    g = wood_grain(W, H, 21, 1.5708, 1.4)
    pol = cart * (1 - rim)
    rgbp = ramp(0.55 + 0.25 * (g - 0.5) + 0.25 * (1 - d) - 0.18 * np.clip((xx - cx) / rx + (yy - cy) / ry, -1, 1), [(0, "#7a3e16"), (0.45, "#bf7838"), (0.75, "#e0a660"), (1.0, "#f6cf90")])
    art[..., :3] = art[..., :3] * (1 - pol[..., None] * 0.85) + rgbp * pol[..., None] * 0.85
    art = add_grain(art, 3, 0.03)
    Image.fromarray((art[..., :3] * 255).astype(np.uint8)).save(f"{PREV}/uj-panel.png")
    save_rgb(art, f"{OUT}/panel.webp", size=(560, 770), quality=78)
    clear()

if "ukel" in PARTS:
    # pierced (krawangan) corner spray: vine along two edges with leaves and a blossom in the corner
    W, H = 380, 380
    R = Relief(W, H)
    for horiz in (True, False):
        pts = curve([(62, 62), (136, 50), (232, 74), (330, 56)], 60) if horiz else curve([(62, 62), (50, 136), (74, 232), (56, 330)], 60)
        R.stem(pts, 14, (0.0, 0.5))
        for k, (x, y, a) in enumerate(along(pts, 46)):
            if k == 0:
                continue
            off = 1 if k % 2 else -1
            R.leaf(x, y, 78 - k * 6, 26 - k * 1.5, a + off * 1.0, curl=off * 0.3, lobes=3)
        ex, ey = pts[-1]
        R.tendril(ex, ey, 12, 0 if horiz else math.pi / 2, d=1 if horiz else -1, width=5)
    R.flower(62, 62, 44, 6, math.pi / 4)
    h, m = R.height()
    alpha = np.clip(gaussian_filter(m, 0.8) * 1.4, 0, 1)
    art = relief_rgba(h, alpha, 31, WARM, strength=6.0, cast_amt=0.4)
    art = over(soft_shadow(alpha, "#120804", 3, 0.55, 4, 6), art)
    preview(art, "uj-ukel", bg="#f2e4cc")
    save(art, f"{OUT}/ukel.webp", max_w=300, quality=82)
    clear()

if "garis" in PARTS:
    W, H = 780, 170
    cx, cy = W / 2, H / 2
    R = Relief(W, H)
    for sgn in (-1, 1):
        pts = curve([(cx + sgn * 40, cy), (cx + sgn * 150, cy - 18), (cx + sgn * 260, cy + 14), (cx + sgn * 350, cy - 6)], 60)
        R.stem(pts, 9, (0.0, 0.5))
        for k, (x, y, a) in enumerate(along(pts, 46)):
            off = 1 if k % 2 else -1
            aa = a if sgn > 0 else a
            R.leaf(x, y, 56 - k * 3, 19 - k * 0.8, aa + off * 1.05, curl=off * 0.3, lobes=3)
        R.tendril(cx + sgn * 356, cy - 6, 10, 0 if sgn > 0 else math.pi, d=sgn, width=4)
    R.flower(cx, cy, 40, 6, 0)
    h, m = R.height()
    alpha = np.clip(gaussian_filter(m, 0.8) * 1.4, 0, 1)
    art = relief_rgba(h, alpha, 41, WARM, strength=6.0, cast_amt=0.4)
    art = over(soft_shadow(alpha, "#120804", 2.5, 0.5, 3, 4), art)
    preview(art, "uj-garis", bg="#f2e4cc")
    save(art, f"{OUT}/garis.webp", max_w=420, quality=82)
    clear()

if "kembang" in PARTS:
    W, H = 280, 280
    R = Relief(W, H)
    R.flower(W / 2, H / 2, 98, 8, -math.pi / 2, layers=2)
    for k in range(8):
        a = -math.pi / 2 + (k + 0.5) / 8 * math.tau
        R.leaf(W / 2 + math.cos(a) * 60, H / 2 + math.sin(a) * 60, 64, 15, a, curl=0.12, lobes=2)
    h, m = R.height()
    alpha = np.clip(gaussian_filter(m, 0.8) * 1.4, 0, 1)
    art = relief_rgba(h, alpha, 51, WARM, strength=6.0, cast_amt=0.45)
    art = over(soft_shadow(alpha, "#120804", 3, 0.5, 3, 5), art)
    preview(art, "uj-kembang", bg="#f2e4cc")
    save(art, f"{OUT}/kembang.webp", max_w=220, quality=84)
    clear()

if "kayu" in PARTS:
    W, H = 512, 512
    g = wrap_grain(W, H, 61, rings=16, warp=0.9)
    rgb = ramp(0.35 + 0.45 * g, [(0, "#3a1d0c"), (0.4, "#6a3818"), (0.7, "#8e5126"), (1.0, "#b06b35")])
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/kayu.webp", quality=72)
    Image.fromarray((np.tile(rgb, (1, 2, 1)) * 255).astype(np.uint8)).save(f"{PREV}/uj-kayu.png")
    clear()
