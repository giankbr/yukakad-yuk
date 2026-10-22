"""Kaca Patri — art nouveau stained glass: hand-rolled cathedral glass panes (variable tint, streaks, seed bubbles,
thicker darker rims) held by dark lead came with soft highlights; whiplash lily stems, leaves and a rising sun disc
(original design). Run: python3 -I kaca-patri.py [part ...]
parts: window lunette rondel border jewel stone. Assets -> public/themes/art/kaca-patri/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b4_lib import *

OUT = outdir("kaca-patri")
PARTS = sys.argv[1:] or ["window", "lunette", "rondel", "border", "jewel", "stone"]
NIGHT = "#1b1f2e"
GLASS = {
    "ruby": [("#a81f38", "#d9485e"), ("#c22f4b", "#e86d7f")],
    "rose": [("#d4577a", "#f0a0b4"), ("#c24a6c", "#ea8aa3")],
    "amber": [("#d8962a", "#f5c95e"), ("#e3a93e", "#f8dc86")],
    "gold": [("#e6b84a", "#fbe7a2")],
    "cobalt": [("#1d4a9e", "#3d74c9"), ("#253f8f", "#4b6fc0")],
    "emerald": [("#2a7d55", "#5fb37a"), ("#3d8f4a", "#86c36b")],
    "olive": [("#6b9636", "#a8c85a"), ("#5c8a3c", "#94bb62")],
    "sky": [("#9fc8de", "#d6e9f0"), ("#b2d3e4", "#e4f0f1"), ("#8fbcd8", "#cbe2ee")],
    "opal": [("#f0dfae", "#fbf1d6"), ("#ead6b4", "#f8eedc")],
    "lilac": [("#a998cf", "#d8cdee"), ("#b6a6d6", "#e2d9f1")],
    "aqua": [("#6fb2b6", "#b2dad2"), ("#82bfb5", "#c2e2d6")],
    "violet": [("#5a3f8f", "#8a6cc0")],
}


def band(spine, w0, w1=None):
    """Closed polygon of a tapering strip along a spine (stems)."""
    pts = resample(spine, 3.0)
    w1 = w0 if w1 is None else w1
    L, R = [], []
    for i, (x, y, a) in enumerate(pts):
        t = i / max(1, len(pts) - 1)
        w = w0 + (w1 - w0) * t
        L.append((x - math.sin(a) * w, y + math.cos(a) * w)); R.append((x + math.sin(a) * w, y - math.cos(a) * w))
    return L + R[::-1]


def leaf_poly(base, tip, bulge, curl=0.0, n=30):
    bx, by = base; tx, ty = tip
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy); nxv, nyv = -dy / L, dx / L
    c = curl * L
    a = bez(base, (bx + dx * 0.3 + nxv * bulge, by + dy * 0.3 + nyv * bulge), (bx + dx * 0.75 + nxv * (bulge * 0.6 + c), by + dy * 0.75 + nyv * (bulge * 0.6 + c)), tip, n)
    b = bez(tip, (bx + dx * 0.7 - nxv * (bulge * 0.35 - c), by + dy * 0.7 - nyv * (bulge * 0.35 - c)), (bx + dx * 0.25 - nxv * bulge * 0.5, by + dy * 0.25 - nyv * bulge * 0.5), base, n)
    mid = bez(base, (bx + dx * 0.3 + nxv * bulge * 0.3, by + dy * 0.3 + nyv * bulge * 0.3), (bx + dx * 0.7 + nxv * (bulge * 0.15 + c * 0.6), by + dy * 0.7 + nyv * (bulge * 0.15 + c * 0.6)), tip, n)
    return a + b[1:], mid


def petal(cx, cy, L, wd, ang, curl=0.25, n=26):
    """Lily petal: long, pointed, the tip flicking back (whiplash)."""
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for i in range(n + 1):
        t = i / n * math.tau
        u = (math.cos(t) * 0.5 + 0.5)
        v = math.sin(t) * wd * (math.sin(math.pi * u) ** 0.7)
        bend = curl * L * u ** 3
        x, y = u * L, v + bend
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return out


class Panel:
    """Collects lead lines + category regions, then renders glass + came."""
    def __init__(self, W, H, lead_w=7.0):
        self.W, self.H, self.lw = W, H, lead_w
        self.lines = []          # (pts, width)
        self.bglines = []        # background came, clipped where motifs sit
        self.cats = {}           # name -> list of polys
        self.order = []

    def region(self, cat, poly, outline=True):
        self.cats.setdefault(cat, []).append(poly)
        if cat not in self.order:
            self.order.append(cat)
        if outline:
            self.lines.append((poly + [poly[0]], self.lw))

    def line(self, pts, w=None):
        self.lines.append((pts, w or self.lw))

    def bg(self, pts, w=None):
        self.bglines.append((pts, w or self.lw))

    def render(self, inside, seed, pick, lead_col="#26221f", field=None):
        W, H = self.W, self.H
        lead = strokes(W, H, [(p, w, None) for p, w in self.lines])
        if self.bglines:
            motif = shapes(W, H, [p for c in self.order if c not in ("cobalt", "bg") for p in self.cats[c]], smooth=False)
            clip = (field if field is not None else inside) * (1 - motif)
            lead = np.maximum(lead, strokes(W, H, [(p, w, None) for p, w in self.bglines]) * clip)
        edge = np.clip(inside - ndimage.binary_erosion(inside > 0.5, iterations=int(self.lw * 1.4)).astype(np.float32), 0, 1)
        lead = np.maximum(lead, edge)
        lead = np.maximum(lead, 1 - inside)
        masks = [(c, shapes(W, H, self.cats[c], smooth=False)) for c in self.order]
        rng = random.Random(seed)

        def colour_of(cx, cy, area, sl, reg):
            if inside[sl][reg].mean() < 0.5:
                return None
            cat = "bg"
            for c, m in masks[::-1]:
                if (m[sl][reg] > 0.5).mean() > 0.55:
                    cat = c
                    break
            return pick(cat, cx, cy, rng)
        rgb, a = glass_panes(lead, colour_of, seed, W, H, bubbles=0.0009)
        glass = np.concatenate([rgb, (a * inside)[..., None]], -1)
        came = lead_render(np.clip(lead * gaussian_filter(inside, 2) * 1.4 + edge, 0, 1) * (gaussian_filter(inside, 1.5) > 0.05), seed + 3, col=lead_col)
        out = over(glass, came)
        return out


def pick_default(cat, cx, cy, rng, H=1000):
    if cat == "bg":
        t = cy / H
        fam = "opal" if t < 0.3 and rng.random() < 0.6 else ("sky" if t < 0.55 else ("aqua" if rng.random() < 0.65 else "sky"))
        if rng.random() < 0.14:
            fam = "lilac"
    else:
        fam = cat
    return rng.choice(GLASS[fam])


def arch_poly(x0, x1, y_top, y_bot, n=60):
    r = (x1 - x0) / 2; cx = (x0 + x1) / 2
    top = [(cx + math.cos(math.pi + t * math.pi) * r, y_top + r + math.sin(math.pi + t * math.pi) * r) for t in np.linspace(0, 1, n)]
    return [(x0, y_bot)] + top + [(x1, y_bot)]


if "window" in PARTS:
    W, H = 640, 1060
    P = Panel(W, H, 7.0)
    rng = random.Random(61)
    x0, x1, yt, yb = 24, W - 24, 20, H - 22
    outer = arch_poly(x0, x1, yt, yb)
    inside = shapes(W, H, [outer], smooth=False)
    # border band
    bw = 34
    inner = arch_poly(x0 + bw, x1 - bw, yt + bw, yb - bw)
    P.line(inner + [inner[0]], 7)
    r_in = (x1 - x0) / 2 - bw; cx = W / 2; cyc = yt + (x1 - x0) / 2
    for k in range(1, 12):
        a = math.pi + k * math.pi / 12
        P.line([(cx + math.cos(a) * (r_in - 2), cyc + math.sin(a) * (r_in - 2)), (cx + math.cos(a) * (r_in + bw + 4), cyc + math.sin(a) * (r_in + bw + 4))], 6)
    for y in np.arange(cyc + 40, yb - bw, 58):
        P.line([(x0 - 4, y), (x0 + bw + 2, y)], 6); P.line([(x1 + 4, y), (x1 - bw - 2, y)], 6)
    jewels = [(cx + math.cos(math.pi + (k + 0.5) * math.pi / 12) * (r_in + bw / 2), cyc + math.sin(math.pi + (k + 0.5) * math.pi / 12) * (r_in + bw / 2)) for k in range(0, 12, 2)]
    for (jx, jy) in jewels:
        P.region("amber", ellipse_pts(jx, jy, 9, 9, 14))
    band_reg = np.clip(inside - shapes(W, H, [inner], smooth=False), 0, 1)
    # sun disc with rays at the crown, held in a ring
    sx, sy, sr = cx, cyc - 6, 74
    P.region("gold", ellipse_pts(sx, sy, sr * 0.52, sr * 0.52, 40))
    P.region("amber", ellipse_pts(sx, sy, sr, sr, 48))
    for k in range(16):
        a = k * math.tau / 16
        P.line([(sx + math.cos(a) * sr * 0.52, sy + math.sin(a) * sr * 0.52), (sx + math.cos(a) * sr, sy + math.sin(a) * sr)], 5)
    ring = ellipse_pts(sx, sy, sr + 46, sr + 46, 70)
    P.line(ring + [ring[0]], 6)
    for k in range(12):
        a = k * math.tau / 12 + 0.13
        P.line([(sx + math.cos(a) * sr, sy + math.sin(a) * sr), (sx + math.cos(a) * (sr + 46), sy + math.sin(a) * (sr + 46))], 5)
    # whiplash stems from the base
    by = yb - bw
    stemA = bez((cx - 30, by + 4), (cx - 190, 820), (cx + 160, 650), (cx - 10, 455), 70)
    stemB = bez((cx + 40, by + 4), (cx + 200, 860), (cx - 120, 760), (cx + 130, 600), 70)
    stemC = bez((cx - 60, 760), (cx - 150, 720), (cx - 200, 680), (cx - 150, 630), 40)
    for st, w0, w1 in ((stemA, 10, 6), (stemB, 9, 5), (stemC, 6, 4)):
        P.region("emerald", band(st, w0, w1))
    # leaves from the base and along the stems (each split by a midrib came)
    for base, tip, bulge, curl in [((cx - 34, by - 4), (x0 + bw + 10, 760), 66, 0.16), ((cx - 20, by - 8), (cx - 130, 880), -34, -0.1),
                                   ((cx + 46, by - 4), (x1 - bw - 8, 720), -70, -0.18), ((cx + 38, by - 10), (cx + 150, 900), 36, 0.1),
                                   ((cx + 6, 640), (x1 - bw - 30, 520), 36, -0.1), ((cx + 40, 700), (x0 + bw + 40, 640), 30, 0.12)]:
        poly, mid = leaf_poly(base, tip, bulge, curl)
        P.region("olive" if rng.random() < 0.5 else "emerald", poly)
        P.line(mid, 5)
    # lilies at the stem tips + a closed bud on the side shoot
    for (fx, fy, s_, rot) in [(cx - 10, 455, 1.0, -math.pi / 2 - 0.05), (cx + 130, 600, 0.72, -math.pi / 2 + 0.4)]:
        for k, da in enumerate([-1.1, -0.55, 0.0, 0.55, 1.1]):
            ang = rot + da
            Lp = 118 * s_ * (1.0 if k in (1, 2, 3) else 0.82)
            P.region("ruby" if k % 2 == 0 else "rose", petal(fx, fy, Lp, 25 * s_, ang, curl=0.2 * (1 if da >= 0 else -1)))
        P.region("amber", ellipse_pts(fx, fy, 15 * s_, 15 * s_, 16))
    P.region("rose", petal(cx - 150, 634, 70, 20, -math.pi / 2 - 0.5, curl=0.1))
    # background came: whiplash curves running frame to frame (clipped behind the motif)
    xa, xb = x0 + bw - 8, x1 - bw + 8
    for y0, y1, amp in [(300, 360, 50), (560, 500, 60), (700, 780, -50), (880, 860, 40), (430, 470, -40)]:
        P.bg(bez((xa, y0), (xa + 180, y0 - amp), (xb - 180, y1 + amp), (xb, y1), 60), 6)
    for spec in [((xa, 220), (150, 300), (90, 420), (xa + 40, 560)), ((xb, 200), (W - 150, 300), (W - 90, 420), (xb - 40, 560)),
                 ((xa, 860), (120, 820), (200, 760), (190, 700)), ((xb, 950), (W - 120, 900), (W - 180, 840), (W - 190, 780))]:
        P.bg(bez(*spec, n=50), 6)
    field = shapes(W, H, [inner], smooth=False)
    P.cats.setdefault("cobalt", []).append(outer)   # border band colour via mask priority (inner region overrides below)
    P.order.insert(0, "cobalt")
    P.cats.setdefault("bg", []).append(inner)
    P.order.insert(1, "bg")

    def pick(cat, cx_, cy_, r):
        if cat == "cobalt":
            return r.choice(GLASS["cobalt"] + GLASS["violet"])
        return pick_default(cat, cx_, cy_, r, H)
    art = P.render(inside, 6101, pick, field=field)
    preview(art, "kp-window", bg=NIGHT)
    save(art, f"{OUT}/window.webp", max_w=500, quality=80)
    clear()

if "lunette" in PARTS:
    # semicircular fanlight: radiating panes, a rising sun and two whiplash leaves
    W, H = 720, 380
    P = Panel(W, H, 6.0)
    rng = random.Random(62)
    cx, cy, R = W / 2, H - 14, 340
    outer = [(cx - R, cy)] + [(cx + math.cos(math.pi + t * math.pi) * R, cy + math.sin(math.pi + t * math.pi) * R) for t in np.linspace(0, 1, 80)] + [(cx + R, cy)]
    inside = shapes(W, H, [outer], smooth=False)
    ring_in = [(cx + math.cos(math.pi + t * math.pi) * (R - 30), cy + math.sin(math.pi + t * math.pi) * (R - 30)) for t in np.linspace(0, 1, 80)]
    P.line(ring_in, 6)
    for k in range(1, 14):
        a = math.pi + k * math.pi / 14
        P.line([(cx + math.cos(a) * 96, cy + math.sin(a) * 96), (cx + math.cos(a) * (R + 4), cy + math.sin(a) * (R + 4))], 6)
    P.region("gold", [(cx - 60, cy)] + [(cx + math.cos(math.pi + t * math.pi) * 60, cy + math.sin(math.pi + t * math.pi) * 60) for t in np.linspace(0, 1, 30)] + [(cx + 60, cy)])
    P.region("amber", [(cx - 96, cy)] + [(cx + math.cos(math.pi + t * math.pi) * 96, cy + math.sin(math.pi + t * math.pi) * 96) for t in np.linspace(0, 1, 40)] + [(cx + 96, cy)])
    for side in (-1, 1):
        poly, mid = leaf_poly((cx + side * 100, cy - 8), (cx + side * 270, cy - 170), side * 40, side * 0.2)
        P.region("emerald", poly); P.line(mid, 4)
        poly, mid = leaf_poly((cx + side * 110, cy - 6), (cx + side * 300, cy - 40), -side * 26, -side * 0.15)
        P.region("olive", poly); P.line(mid, 4)
        P.region("ruby", ellipse_pts(cx + side * 190, cy - 230, 22, 22, 18))
    band_ring = [(cx - R, cy)] + [(cx + math.cos(math.pi + t * math.pi) * R, cy + math.sin(math.pi + t * math.pi) * R) for t in np.linspace(0, 1, 80)] + [(cx + R, cy)]
    P.cats["cobalt"] = [band_ring]; P.order.insert(0, "cobalt")
    P.cats["bg"] = [[(cx - R + 30, cy)] + ring_in + [(cx + R - 30, cy)]]; P.order.insert(1, "bg")

    def pick(cat, cx_, cy_, r):
        if cat == "bg":
            return r.choice(GLASS["sky"] + GLASS["lilac"][:1] + GLASS["aqua"][:1])
        return r.choice(GLASS[cat] if cat != "cobalt" else GLASS["cobalt"] + GLASS["violet"])
    art = P.render(inside, 6201, pick)
    preview(art, "kp-lunette", bg=NIGHT)
    save(art, f"{OUT}/lunette.webp", max_w=420, quality=80)
    clear()

if "rondel" in PARTS:
    W = H = 380
    P = Panel(W, H, 6.0)
    cx = cy = W / 2; R = 176
    inside = circles(W, H, [(cx, cy, R)])
    P.line(ellipse_pts(cx, cy, R - 28, R - 28, 80) + [ellipse_pts(cx, cy, R - 28, R - 28, 80)[0]], 6)
    for k in range(16):
        a = k * math.tau / 16
        P.line([(cx + math.cos(a) * (R - 30), cy + math.sin(a) * (R - 30)), (cx + math.cos(a) * (R + 4), cy + math.sin(a) * (R + 4))], 5)
    for k in range(4):
        a = k * math.pi / 2 - math.pi / 2
        P.region("ruby" if k % 2 == 0 else "rose", petal(cx, cy, 120, 34, a, curl=0.12))
        poly, mid = leaf_poly((cx, cy), (cx + math.cos(a + math.pi / 4) * 128, cy + math.sin(a + math.pi / 4) * 128), 22, 0.12)
        P.region("emerald", poly); P.line(mid, 4)
    P.region("amber", ellipse_pts(cx, cy, 22, 22, 20))
    P.cats["cobalt"] = [ellipse_pts(cx, cy, R, R, 90)]; P.order.insert(0, "cobalt")
    P.cats["bg"] = [ellipse_pts(cx, cy, R - 28, R - 28, 90)]; P.order.insert(1, "bg")
    seq = iter(range(100))

    def pick(cat, cx_, cy_, r):
        if cat == "cobalt":
            return GLASS["amber"][0] if next(seq) % 2 else GLASS["cobalt"][0]
        if cat == "bg":
            return r.choice(GLASS["sky"] + GLASS["aqua"])
        return r.choice(GLASS[cat])
    art = P.render(inside, 6301, pick)
    preview(art, "kp-rondel", bg=NIGHT)
    save(art, f"{OUT}/rondel.webp", max_w=220, quality=82)
    clear()

if "border" in PARTS:
    # divider: a leaded strip — central jewel, whiplash leaves sweeping out, small panes at the ends
    W, H = 760, 120
    P = Panel(W, H, 4.2)
    rng = random.Random(64)
    cx, cy = W / 2, H / 2
    inside = np.zeros((H, W), np.float32)
    polys = []
    P.region("amber", ellipse_pts(cx, cy, 20, 20, 24)); polys.append(ellipse_pts(cx, cy, 26, 26, 24))
    for side in (-1, 1):
        for (tip, bulge, cat) in [((cx + side * 250, cy - 30), side * -40, "emerald"), ((cx + side * 205, cy + 32), side * 34, "olive")]:
            poly, mid = leaf_poly((cx + side * 22, cy), tip, bulge, side * 0.1)
            P.region(cat, poly); P.line(mid, 3.5); polys.append(poly)
        P.region("ruby", ellipse_pts(cx + side * 290, cy - 6, 13, 13, 18)); polys.append(ellipse_pts(cx + side * 290, cy - 6, 13, 13, 18))
        P.region("cobalt", ellipse_pts(cx + side * 330, cy + 4, 8, 8, 16)); polys.append(ellipse_pts(cx + side * 330, cy + 4, 8, 8, 16))
    inside = np.clip(gaussian_filter(shapes(W, H, polys), 0.5) * 1.2, 0, 1)

    def pick(cat, cx_, cy_, r):
        return r.choice(GLASS.get(cat, GLASS["sky"]))
    art = P.render(inside, 6401, pick)
    preview(art, "kp-border", bg=NIGHT)
    save(art, f"{OUT}/border.webp", max_w=380, quality=84)

if "jewel" in PARTS:
    W = H = 120
    P = Panel(W, H, 5.0)
    cx = cy = 60
    inside = circles(W, H, [(cx, cy, 52)])
    for k in range(8):
        a = k * math.tau / 8
        P.line([(cx, cy), (cx + math.cos(a) * 56, cy + math.sin(a) * 56)], 3.5)
    P.line(ellipse_pts(cx, cy, 24, 24, 30) + [ellipse_pts(cx, cy, 24, 24, 30)[0]], 3.5)
    seq = iter(range(100))

    def pick(cat, cx_, cy_, r):
        return GLASS["amber"][0] if next(seq) % 2 else GLASS["amber"][1]
    art = P.render(inside, 6501, pick)
    preview(art, "kp-jewel", bg=NIGHT)
    save(art, f"{OUT}/jewel.webp", max_w=56, quality=86)

if "stone" in PARTS:
    # deep night-blue plaster for the dark bands (seamless)
    n = 360
    base = rgb_arr(n, n, NIGHT) * (0.9 + 0.2 * wrap_noise(n, n, 21, 26))[..., None]
    base *= (1 + (wrap_noise(n, n, 22, 0.7) - 0.5) * 0.08)[..., None]
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/stone.webp", quality=72)
    n = 400
    base = rgb_arr(n, n, "#f1ece2") * (0.975 + 0.05 * wrap_noise(n, n, 23, 40))[..., None] * (1 + (wrap_noise(n, n, 24, 0.6) - 0.5) * 0.05)[..., None]
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/vellum.webp", quality=70)
