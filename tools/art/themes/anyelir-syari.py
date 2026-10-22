"""Anyelir Syari — fine-line dip-pen carnations (frilled petals, long calyx, narrow grey-green leaves) with a loose soft
mauve watercolour wash that does not quite stay in the lines, on cream paper; monogram medallions. Minimal, calm.
Run: python3 -I anyelir-syari.py [part ...]   parts: paper spray medallion sprig bloom
Assets -> public/themes/art/anyelir-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b3_lib import *

OUT = outdir("anyelir-syari")
PARTS = sys.argv[1:] or ["paper", "spray", "medallion", "sprig", "bloom"]
INK = "#4a3843"
MAUVE, MAUVE2, ROSE = "#b88aa6", "#9d7090", "#d7aebf"
SAGE, SAGE2 = "#9aab95", "#7d9179"
CREAM = "#f7f1e8"
SEQ = Seq(500)


def wob(pts, rng, amt=0.6):
    return [(x + rng.gauss(0, amt), y + rng.gauss(0, amt)) for x, y in pts]


def frill_edge(cx, cy, ang, R, spread, rng, teeth=13, depth=0.11):
    """Outer edge of a carnation petal fan: a run of uneven ruffled lobes, each finely nicked (pinked) at the rim."""
    lobes = max(5, int(teeth * 0.75))
    pts = []
    sub = 8
    widths = [rng.uniform(0.7, 1.3) for _ in range(lobes)]
    tot = sum(widths)
    th0 = ang - spread
    for li, wl in enumerate(widths):
        span = 2 * spread * wl / tot
        rl = R * rng.uniform(0.9, 1.06) * (0.92 + 0.08 * math.cos(((th0 + span / 2) - ang) / spread * math.pi / 2))
        for k in range(sub + (1 if li == lobes - 1 else 0)):
            u = k / sub
            th = th0 + span * u
            r = rl * (0.9 + 0.1 * math.sin(math.pi * u))
            if 0 < k < sub:
                r += R * depth * 0.28 * (1 if k % 2 else -1) * rng.uniform(0.4, 1.2)
            pts.append((cx + math.cos(th) * r, cy + math.sin(th) * r))
        th0 += span
    return pts


class Pen:
    """Collects ink strokes and wash shapes for one illustration, then renders: washes first, ink on top."""
    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.rng = random.Random(seed)
        self.ink = []          # (pts, width, taper)
        self.wash = {}         # colour key -> list of polys

    def line(self, pts, w=1.7, taper=(0.12, 0.25)):
        self.ink.append((wob(pts, self.rng, 0.35), w * self.rng.uniform(0.85, 1.1), taper))

    def fill(self, key, pts):
        self.wash.setdefault(key, []).append(pts)

    def render(self, art=None, washes=None, wash_shift=(3, -2)):
        W, H = self.W, self.H
        art = blank(W, H) if art is None else art
        for key, polys in self.wash.items():
            ca, cb, dens = washes[key]
            m = shapes(W, H, [[(x + wash_shift[0], y + wash_shift[1]) for x, y in p] for p in polys])
            m = np.clip(displace(m, SEQ(), 4.0, 26), 0, 1)
            art = G(art, m, ca, cb, seed=SEQ(), density=dens, edge=0.7, bloom=0.45, gran=0.3, rough=6.0, feather=1.4)
            trim_cache()
        m = strokes(W, H, self.ink)
        art = IK(art, m, INK, seed=SEQ(), alpha=0.9, dry=0.3)
        return art


def carnation_side(p, x, y, s, ang, rng, open_=1.0):
    """Side-view carnation: frilled petal fan in 3 layers over a long calyx; ang = flower axis (up = -pi/2)."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    # calyx: slim vase from (x,y) along -axis
    L = s * 0.95
    base = (x - ca * L, y - sa * L)
    wtop, wbot = s * 0.2, s * 0.11
    left = [(base[0] + px * wbot * (1 - t * 0.2) * (1 + 0.6 * t) + ca * L * t, base[1] + py * wbot * (1 + 0.6 * t) + sa * L * t) for t in np.linspace(0, 1, 8)]
    right = [(base[0] - px * wbot * (1 + 0.6 * t) + ca * L * t, base[1] - py * wbot * (1 + 0.6 * t) + sa * L * t) for t in np.linspace(0, 1, 8)]
    p.line(left, 1.5); p.line(right, 1.5)
    # calyx teeth + a vertical rib
    p.line([(base[0] + ca * L * 0.2, base[1] + sa * L * 0.2), (base[0] + ca * L * 0.95, base[1] + sa * L * 0.95)], 1.0, (0.2, 0.5))
    tip = (x + ca * s * 0.05, y + sa * s * 0.05)
    for k in (-1, 0, 1):
        p.line([(x + px * wtop * 0.55 * k, y + py * wtop * 0.55 * k), (tip[0] + px * wtop * 0.55 * k + ca * s * 0.1, tip[1] + py * wtop * 0.55 * k + sa * s * 0.1)], 1.1, (0.0, 0.8))
    # bracts at base of calyx
    for k in (-1, 1):
        p.line([(base[0] + px * wbot * k, base[1] + py * wbot * k), (base[0] + px * wbot * 2.4 * k - ca * s * 0.08, base[1] + py * wbot * 2.4 * k - sa * s * 0.08)], 1.2, (0.0, 0.7))
    p.fill("sage", left + right[::-1])
    # petal fans (back -> front)
    fans = [(s * 1.02 * open_, 1.05, 0.0), (s * 0.88 * open_, 0.85, s * 0.04), (s * 0.66 * open_, 0.62, s * 0.08)]
    for i, (R, spread, drop) in enumerate(fans):
        cx_, cy_ = x - ca * drop, y - sa * drop
        edge = frill_edge(cx_, cy_, ang, R, spread, rng, teeth=11 - i * 2)
        poly = [(cx_, cy_)] + edge
        p.fill("mauve" if i < 2 else "rose", poly)
        p.line(edge, 1.6 if i == 0 else 1.4, (0.05, 0.05))
        # side lines down to the calyx mouth (outer fan only)
        if i == 0:
            p.line([edge[0], (x + px * wtop * 0.9, y + py * wtop * 0.9)], 1.3, (0.0, 0.6))
            p.line([edge[-1], (x - px * wtop * 0.9, y - py * wtop * 0.9)], 1.3, (0.0, 0.6))
        # a couple of petal ribs
        for k in range(1 if i else 2):
            th = ang + rng.uniform(-spread * 0.6, spread * 0.6)
            rr = R * rng.uniform(0.6, 0.8)
            p.line([(cx_ + math.cos(th) * R * 0.4, cy_ + math.sin(th) * R * 0.4), (cx_ + math.cos(th) * rr, cy_ + math.sin(th) * rr)], 0.8, (0.3, 0.6))


def carnation_top(p, x, y, r, rng):
    """Carnation seen from above: frilled pompon of concentric ruffled rings."""
    for i, (rr, key) in enumerate(((r, "mauve"), (r * 0.72, "mauve"), (r * 0.44, "rose"))):
        edge = frill_edge(x, y, rng.uniform(0, 6.3), rr, math.pi, rng, teeth=16 - i * 3, depth=0.14)
        edge = [(ex, y + (ey - y) * 0.94) for ex, ey in edge]
        p.fill(key, edge)
        p.line(edge, 1.5 if i == 0 else 1.3, (0.03, 0.03))
    for k in range(7):
        th = rng.uniform(0, 2 * math.pi)
        p.line([(x + math.cos(th) * r * 0.1, y + math.sin(th) * r * 0.1), (x + math.cos(th) * r * 0.36, y + math.sin(th) * r * 0.36)], 0.9, (0.1, 0.6))


def bud(p, x, y, s, ang, rng):
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    L = s
    tip = (x + ca * L, y + sa * L)
    left = bez((x, y), (x + px * s * 0.25, y + py * s * 0.25), (tip[0] + px * s * 0.12, tip[1] + py * s * 0.12), tip, 14)
    right = bez((x, y), (x - px * s * 0.25, y - py * s * 0.25), (tip[0] - px * s * 0.12, tip[1] - py * s * 0.12), tip, 14)
    p.line(left, 1.4); p.line(right, 1.4)
    p.fill("sage", left + right[::-1])
    # a lick of mauve peeking from the tip
    t2 = (tip[0] + ca * s * 0.22, tip[1] + sa * s * 0.22)
    pk = [(tip[0] + px * s * 0.08, tip[1] + py * s * 0.08), t2, (tip[0] - px * s * 0.08, tip[1] - py * s * 0.08)]
    p.fill("rose", pk + [tip]); p.line(pk, 1.1)


def leaf(p, x, y, L, ang, rng, curl=0.25, wd=0.09):
    """Narrow grass-like carnation leaf."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    tip = (x + ca * L + px * L * curl, y + sa * L + py * L * curl)
    mid = (x + ca * L * 0.5 + px * L * curl * 0.35, y + sa * L * 0.5 + py * L * curl * 0.35)
    a = bez((x, y), (mid[0] + px * L * wd, mid[1] + py * L * wd), (tip[0] + px * L * wd * 0.3, tip[1] + py * L * wd * 0.3), tip, 18)
    b = bez((x, y), (mid[0] - px * L * wd, mid[1] - py * L * wd), (tip[0] - px * L * wd * 0.3, tip[1] - py * L * wd * 0.3), tip, 18)
    p.line(a, 1.3, (0.0, 0.5)); p.line(b, 1.1, (0.0, 0.5))
    p.fill("sage", a + b[::-1])


def stem_path(p0, p1, bow, n=40):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    return bez(p0, (mx + nx * bow * 0.6 - dx * 0.15, my + ny * bow * 0.6 - dy * 0.15), (mx + nx * bow, my + ny * bow), p1, n)


WASH = {"mauve": (MAUVE, MAUVE2, 0.5), "rose": (ROSE, MAUVE, 0.55), "sage": (SAGE, SAGE2, 0.34)}


def stalk(p, base, head, bow, rng, leaves=2, s=60, top=False, open_=1.0):
    pts = stem_path(base, head, bow)
    p.line(pts, 1.6, (0.0, 0.1))
    p.line([(x + 2.2, y) for x, y in pts[4:-6]], 0.8, (0.2, 0.3))
    for k in range(leaves):
        t = 0.3 + 0.38 * k / max(1, leaves - 1)
        i = int(t * (len(pts) - 1))
        x, y = pts[i]
        dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        a = math.atan2(dy, dx)
        side = 1 if k % 2 == 0 else -1
        leaf(p, x, y, s * rng.uniform(1.6, 2.1), a + side * 0.5, rng, curl=0.2 * side, wd=0.1)
        if rng.random() < 0.6:
            leaf(p, x, y, s * rng.uniform(1.1, 1.5), a - side * 0.6, rng, curl=-0.2 * side, wd=0.09)
        # node knot
        p.line([(x - 3, y), (x + 3, y)], 1.6, None)
    dx, dy = pts[-1][0] - pts[-3][0], pts[-1][1] - pts[-3][1]
    a = math.atan2(dy, dx)
    hx, hy = head[0] + math.cos(a) * s * 0.95, head[1] + math.sin(a) * s * 0.95
    if top:
        bud(p, head[0], head[1], s * 0.7, a, rng)
    else:
        carnation_side(p, hx, hy, s, a, rng, open_)


if "paper" in PARTS:
    img = paper(512, 512, CREAM, seed=5, fiber=0.6, mottle=0.4)
    arr = np.asarray(img, np.float32) / 255
    if arr.shape[-1] == 3:
        arr = np.concatenate([arr, np.ones(arr.shape[:2] + (1,), np.float32)], -1)
    # make it seamless with a 4-way cross-fade
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = (np.sin(math.pi * xx / w) ** 2)[..., None]; wy = (np.sin(math.pi * yy / h) ** 2)[..., None]
    a3 = arr[..., :3]; ax = np.roll(a3, w // 2, 1); ay = np.roll(a3, h // 2, 0); axy = np.roll(ax, h // 2, 0)
    arr[..., :3] = a3 * wx * wy + ax * (1 - wx) * wy + ay * wx * (1 - wy) + axy * (1 - wx) * (1 - wy)
    rgb_save(arr, f"{OUT}/paper.webp", quality=70)
    clear()

if "spray" in PARTS:
    # corner spray: two open carnations, one half-open, one bud on long crossing stems
    W, H = 600, 720
    p = Pen(W, H, 11)
    rng = p.rng
    stalk(p, (150, 712), (300, 250), -50, rng, leaves=3, s=92)
    stalk(p, (170, 712), (420, 400), -30, rng, leaves=2, s=76, open_=0.9)
    stalk(p, (130, 712), (150, 360), 30, rng, leaves=2, s=64, open_=0.75)
    stalk(p, (160, 706), (470, 590), -20, rng, leaves=1, s=44, top=True)
    art = p.render(washes=WASH)
    preview(art, "an-spray", tone=CREAM)
    save(art, f"{OUT}/spray.webp", max_w=420, quality=84)
    clear()

if "medallion" in PARTS:
    W = H = 560
    cx = cy = W / 2
    p = Pen(W, H, 21)
    rng = p.rng
    R = 196
    for rr, wd in ((R, 1.6), (R - 9, 1.0)):
        pts = [(cx + math.cos(t) * rr * (1 + rng.uniform(-0.003, 0.003)), cy + math.sin(t) * rr) for t in np.linspace(-math.pi / 2 + 0.05, 3 * math.pi / 2 + 0.03, 160)]
        p.line(pts, wd, (0.02, 0.02))
    # a loose arc of wash behind the ring (lower left -> right), like one brush pass
    arc = [(cx + math.cos(t) * (R + 4), cy + math.sin(t) * (R + 4)) for t in np.linspace(0.5, 2.6, 40)]
    arc2 = [(cx + math.cos(t) * (R - 16), cy + math.sin(t) * (R - 16)) for t in np.linspace(2.6, 0.5, 40)]
    p.fill("rose", arc + arc2)
    # two sprigs rising from the bottom and hugging the ring, a carnation where they meet
    for side in (-1, 1):
        pts = [(cx + math.cos(t) * (R + 2), cy + math.sin(t) * (R + 2)) for t in np.linspace(math.pi / 2 + side * 0.14, math.pi / 2 + side * 1.75, 30)]
        p.line(pts, 1.5, (0.0, 0.3))
        for k, t in enumerate(np.linspace(0.12, 0.95, 7)):
            i = int(t * 29)
            x, y = pts[i]
            out = math.atan2(y - cy, x - cx)
            tang = out + side * math.pi / 2
            leaf(p, x, y, 70 - k * 5, tang + (0.5 if k % 2 else -0.5) * side * 0 + (0.45 if k % 2 else -0.45), rng, curl=0.12 * side, wd=0.13)
        tx, ty = pts[-1]
        out = math.atan2(ty - cy, tx - cx)
        bud(p, tx, ty, 26, out + side * 1.1, rng)
    carnation_top(p, cx, cy + R + 4, 30, rng)
    # small bloom at the top of the ring
    carnation_side(p, cx, cy - R + 4, 44, -math.pi / 2, rng, 0.85)
    leaf(p, cx - 6, cy - R + 12, 40, math.pi - 0.35, rng, curl=-0.15)
    leaf(p, cx + 6, cy - R + 12, 40, 0.35, rng, curl=0.15)
    art = p.render(washes=WASH)
    preview(art, "an-medallion", tone=CREAM)
    save_full(art, f"{OUT}/medallion.webp", size=(400, 400), quality=84)
    clear()

if "sprig" in PARTS:
    # divider: one carnation lying along a fine stem, two leaves, a bud
    W, H = 620, 130
    p = Pen(W, H, 31)
    rng = p.rng
    pts = bez((40, 82), (180, 70), (330, 92), (420, 72), 40)
    p.line(pts, 1.5, (0.1, 0.0))
    for t, a, L in ((0.3, -0.45, 84), (0.45, 0.5, 76), (0.68, -0.4, 62)):
        x, y = pts[int(t * 39)]
        leaf(p, x, y, L, a - 0.15, rng, curl=0.12 if a > 0 else -0.12, wd=0.12)
    x, y = pts[int(0.15 * 39)]
    bud(p, x, y, 28, math.pi + 0.5, rng)
    carnation_side(p, 470, 66, 52, -0.15, rng, 0.95)
    art = p.render(washes=WASH)
    preview(art, "an-sprig", tone=CREAM)
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=84)
    clear()

if "bloom" in PARTS:
    S = 220
    p = Pen(S, S, 41)
    carnation_top(p, S / 2, S / 2, 70, p.rng)
    art = p.render(washes=WASH)
    preview(art, "an-bloom", tone=CREAM)
    save(art, f"{OUT}/bloom.webp", max_w=120, quality=84)
    clear()

report(OUT)
