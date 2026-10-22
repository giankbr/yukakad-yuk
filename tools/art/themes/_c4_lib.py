"""Agent C4 helpers (zaitun-tuscan, santorini-putih, neon-malam, marmer-ebru): builds on _j1_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds olive sprigs, painted neon tubes on brick, and a marbling
(ebru) simulator: ink drops, tine combing and swirls computed by exact inverse mapping of the paint surface.
Previews -> /tmp/pen/nb-C4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_PV = "/tmp/pen/nb-C4/art"
os.makedirs(_PV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = _PV
_j1_lib.PREV = _PV
import art as _art
from scipy import ndimage
from scipy.ndimage import gaussian_filter, map_coordinates
PREV = _PV


def preview(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.PREV = _PV
    _p1_lib.preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def col_arr(h):
    return np.array(hex_rgb(h), np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * col_arr(col)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def pl(W, H, lines, width, cap=True):
    return strokes(W, H, [(pts, width, None) for pts in lines], cap=cap)


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def poly(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def light_mask(h, w, cx, cy, r):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    return np.clip(1 - d, 0, 1) ** 1.5


def ridge(W, H, y, amp, seed, wl=0.5, step=16):
    """Hill silhouette mask (filled below a wavy ridge line)."""
    rng = random.Random(seed)
    pts = [(-20, H + 20)]
    ph = rng.uniform(0, 6); ph2 = rng.uniform(0, 6)
    for i in range(0, W + 41, step):
        pts.append((i - 20, y - amp * (0.6 * math.sin(i / (W * wl) * math.pi * 2 + ph) + 0.4 * math.sin(i / (W * wl * 0.37) + ph2))))
    pts.append((W + 20, H + 20))
    return shapes(W, H, [pts], smooth=True)


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1); u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def resample(pts, step):
    """Polyline -> [(x, y, angle)] at fixed arc length."""
    out = []; acc = 0.0
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out


def soft_edge(W, H, seed, inset=0.08, power=2.2, amount=10.0):
    """Organic painted vignette (1 inside, falls off to 0 near the canvas edge with a ragged, wet border)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = np.abs(xx / W - 0.5) * 2; dy = np.abs(yy / H - 0.5) * 2
    d = (dx ** power + dy ** power) ** (1 / power)
    n = (fbm(W, H, seed, 60, 3) - 0.5) * 0.18
    m = np.clip((1 - inset - d + n) / 0.08, 0, 1)
    return m


# ------------------------------------------------------------------ olive branch (watercolour)
OLV_TOP = ("#5d6b45", "#7f8b5d")
OLV_UNDER = ("#a7b199", "#d0d6c4")
OLV_FRUIT = [("#6f7d32", "#9aa646"), ("#4a3a4a", "#6c5163"), ("#2f2532", "#4d3a48"), ("#7c7a34", "#a79a4a")]


def olive_leaf_poly(x, y, L, ang, wid=0.15, curl=0.0, n=16):
    pts = []
    ca, sa = math.cos(ang), math.sin(ang)
    for i in range(n + 1):
        t = i / n
        w = L * wid * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t)
        bend = curl * L * t * t
        pts.append((t * L, w + bend))
    for i in range(n, -1, -1):
        t = i / n
        w = L * wid * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t)
        bend = curl * L * t * t
        pts.append((t * L, -w * 0.8 + bend))
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]


def olive_branch(W, H, spine, rng, nx, art=None, leaf_len=(46, 70), spacing=15, fruit=0.35, scale=1.0,
                 stem=("#6d5b46", "#4a3c2e"), stem_w=4.0, twigs=True):
    """Paint an olive branch along a spine polyline: woody stem, paired lanceolate leaves (mix of grey-green tops and
    silvery undersides), clusters of olives in green-to-aubergine. Returns RGBA."""
    art = blank(W, H) if art is None else art
    pts = resample(spine, spacing * scale)
    n = len(pts)
    leaves_top, leaves_under, ribs, fruits = [], [], [], []
    twig_lines = []
    for i, (x, y, a) in enumerate(pts[1:], 1):
        t = i / max(1, n - 1)
        for side in (-1, 1):
            if rng.random() < 0.12:
                continue
            L = rng.uniform(*leaf_len) * scale * (1.0 - 0.45 * t)
            la = a + side * rng.uniform(0.45, 0.95) + rng.uniform(-0.12, 0.12)
            ox, oy = x + math.cos(la) * 2, y + math.sin(la) * 2
            poly_ = olive_leaf_poly(ox, oy, L, la, wid=rng.uniform(0.12, 0.17), curl=side * rng.uniform(-0.06, 0.14))
            (leaves_under if rng.random() < 0.42 else leaves_top).append(poly_)
            ribs.append([(ox, oy), (ox + math.cos(la) * L * 0.8, oy + math.sin(la) * L * 0.8)])
        if fruit and rng.random() < fruit and 0.15 < t < 0.9:
            side = rng.choice((-1, 1))
            fa = a + side * rng.uniform(0.9, 1.5)
            k = rng.randint(1, 3)
            for j in range(k):
                fl = (10 + j * 8 + rng.uniform(0, 6)) * scale
                ex, ey = x + math.cos(fa + j * 0.35 * side) * fl, y + math.sin(fa + j * 0.35 * side) * fl
                twig_lines.append([(x, y), (ex, ey)])
                fruits.append((ex + math.cos(fa) * 8 * scale, ey + math.sin(fa) * 8 * scale, 6.5 * scale * rng.uniform(0.9, 1.15), 9.5 * scale * rng.uniform(0.9, 1.1), math.degrees(fa) + 90))
    stem_m = strokes(W, H, [(spine, stem_w * scale, (0.02, 0.6))])
    tw = strokes(W, H, [(l, 1.6 * scale, None) for l in twig_lines]) if twig_lines else np.zeros((H, W), np.float32)
    art = G(art, np.maximum(stem_m, tw), stem[0], stem[1], seed=nx(), density=0.9, edge=0.4, bloom=0.1, rough=1.2, feather=0.6, pad=8)
    if leaves_under:
        mu = shapes(W, H, leaves_under)
        art = G(art, mu, OLV_UNDER[0], OLV_UNDER[1], seed=nx(), density=0.8, edge=0.65, bloom=0.3, rough=1.6, feather=0.8, gran=0.3)
    if leaves_top:
        mt = shapes(W, H, leaves_top)
        art = G(art, mt, OLV_TOP[0], OLV_TOP[1], seed=nx(), density=0.86, edge=0.7, bloom=0.35, rough=1.6, feather=0.8, gran=0.3)
        # second glaze on part of the top leaves for depth
        sel = [p for p in leaves_top if rng.random() < 0.4]
        if sel:
            art = G(art, shapes(W, H, sel), "#45523a", seed=nx(), density=0.35, edge=0.5, bloom=0.4, rough=1.4, feather=1.0)
    rib = strokes(W, H, [(r, 1.1 * scale, (0.1, 0.5)) for r in ribs])
    art = over(art, flat(rib * (art[..., 3] > 0.3), "#e3e6d6", 0.5))
    if fruits:
        for k, f in enumerate(fruits):
            ca, cb = rng.choice(OLV_FRUIT)
            m = ellipses(W, H, [f])
            art = G(art, m, ca, cb, seed=nx(), density=0.95, edge=0.6, bloom=0.15, rough=0.8, feather=0.5, pad=6)
            hx, hy = f[0] - f[2] * 0.35, f[1] - f[3] * 0.35
            art = over(art, flat(gaussian_filter(circles(W, H, [(hx, hy, f[2] * 0.28)]), 0.8), "#fff6e6", 0.55))
    return art


# ------------------------------------------------------------------ neon tubes
def neon(W, H, lines, col, core="#fff7fb", width=6.0, glow_r=(6, 18, 40), glow_a=(0.9, 0.6, 0.35), seed=1,
         flicker=0.0, clips=True, lit=True):
    """Painted neon tube: a coloured glass tube (darker edges, hot pale core, glints), with mounting clips and a soft
    multi-radius glow halo. lines: list of polylines. Returns RGBA (glow has partial alpha, works on dark brick)."""
    m = strokes(W, H, [(l, width, None) for l in lines])
    core_m = strokes(W, H, [(l, width * 0.36, None) for l in lines])
    rgb_c = col_arr(col)
    out = blank(W, H)
    if lit:
        for r, a in zip(glow_r, glow_a):
            g = np.clip(gaussian_filter(m, r) * 2.2, 0, 1) * a
            out = over(out, np.concatenate([np.ones((H, W, 3), np.float32) * rgb_c, g[..., None]], -1))
    # tube body: coloured glass, uneven brightness along its length
    var = 0.85 + 0.3 * fbm(W, H, seed, 30, 2)
    if flicker:
        var *= 1 - flicker * np.clip((fbm(W, H, seed + 4, 70, 2) - 0.6) * 4, 0, 1)
    body_rgb = np.clip(rgb_c * (1.05 if lit else 0.55) * var[..., None] + (0.12 if lit else 0), 0, 1)
    tube = np.concatenate([body_rgb, gaussian_filter(m, 0.6)[..., None]], -1)
    out = over(out, tube)
    if lit:
        crgb = col_arr(core) * np.ones((H, W, 3), np.float32)
        out = over(out, np.concatenate([crgb, (gaussian_filter(core_m, 0.9) * 0.95 * var.clip(0, 1))[..., None]], -1))
    else:
        hi = strokes(W, H, [([(x + 0.0, y - width * 0.22) for x, y in l], width * 0.18, None) for l in lines])
        out = over(out, flat(hi * m, "#ffffff", 0.35))
    if clips:
        rng = random.Random(seed)
        cl = []
        for l in lines:
            rs = resample(l, 70)
            for x, y, a in rs[1::2]:
                if rng.random() < 0.8:
                    cl.append((x, y, a))
        if cl:
            cm = strokes(W, H, [([(x - math.sin(a) * width * 1.1, y + math.cos(a) * width * 1.1), (x + math.sin(a) * width * 1.1, y - math.cos(a) * width * 1.1)], 3.0, None) for x, y, a in cl], cap=False)
            out = over(out, flat(cm, "#2b2a2e", 0.85))
            out = over(out, flat(strokes(W, H, [([(x - math.sin(a) * width * 1.1 - 0.8, y + math.cos(a) * width * 1.1 - 0.8), (x + math.sin(a) * width * 1.1 - 0.8, y - math.cos(a) * width * 1.1 - 0.8)], 0.9, None) for x, y, a in cl], cap=False), "#9c9aa3", 0.7))
    return out


# ------------------------------------------------------------------ marbling (ebru)
class Marble:
    """Ebru surface. Operations are recorded and rendered by inverse mapping: each pixel walks back through the
    operations to the point it came from; drops colour the pixels that land inside them. Exact for drops (the
    classic area-preserving drop map), tines (shift along a line by a function of the distance to it) and
    swirls (rotation by a function of radius)."""

    def __init__(self, W, H, ground="#f2e7d8"):
        self.W, self.H = W, H
        self.ops = []
        self.ground = col_arr(ground)

    def drop(self, cx, cy, r, col):
        self.ops.append(("drop", cx, cy, r, col_arr(col)))

    def tine(self, px, py, ang, amp, lam=12.0, sharp=1.0):
        """Comb stroke through point (px, py) in direction ang; displacement amp * lam / (d + lam)."""
        self.ops.append(("tine", px, py, ang, amp, lam, sharp))

    def comb(self, ang, spacing, amp, lam=8.0, offset=0.0, alt=False):
        """Parallel tines across the whole surface (alt: alternate direction = 'gel-git')."""
        nxv, nyv = -math.sin(ang), math.cos(ang)
        diag = math.hypot(self.W, self.H)
        k = 0
        for d in np.arange(-diag, diag, spacing):
            cx = self.W / 2 + nxv * (d + offset); cy = self.H / 2 + nyv * (d + offset)
            if -spacing < (cx * nxv + cy * nyv) - (self.W / 2 * nxv + self.H / 2 * nyv) - d - offset < spacing:
                pass
            s = -1 if (alt and k % 2) else 1
            self.ops.append(("tine", cx, cy, ang, amp * s, lam, 1.0))
            k += 1

    def wave(self, ang, amp, period, phase=0.0):
        """Sinusoidal shift along ang as a function of position across it (wavy comb)."""
        self.ops.append(("wave", ang, amp, period, phase))

    def swirl(self, cx, cy, strength, radius):
        self.ops.append(("swirl", cx, cy, strength, radius))

    def render(self, ss=1, edge_ink=0.0, seed=1):
        W, H = self.W * ss, self.H * ss
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
        x = xx / ss; y = yy / ss
        rgb = np.zeros((H, W, 3), np.float32)
        done = np.zeros((H, W), bool)
        depth = np.zeros((H, W), np.float32)  # distance-ish to boundary for veins
        for op in reversed(self.ops):
            kind = op[0]
            if kind == "drop":
                _, cx, cy, r, c = op
                dx, dy = x - cx, y - cy
                d2 = dx * dx + dy * dy
                inside = (d2 < r * r) & ~done
                rgb[inside] = c
                done |= inside
                k = np.sqrt(np.clip(1 - r * r / np.maximum(d2, 1e-9), 0, None))
                o = ~done
                x = np.where(o, cx + dx * k, x); y = np.where(o, cy + dy * k, y)
            elif kind == "tine":
                _, px, py, ang, amp, lam, sharp = op
                ux, uy = math.cos(ang), math.sin(ang)
                d = np.abs((x - px) * (-uy) + (y - py) * ux)
                s = amp * lam / (d + lam)
                x = x - ux * s; y = y - uy * s
            elif kind == "wave":
                _, ang, amp, period, phase = op
                ux, uy = math.cos(ang), math.sin(ang)
                d = (x * (-uy) + y * ux)
                s = amp * np.sin(d / period * math.tau + phase)
                x = x - ux * s; y = y - uy * s
            elif kind == "swirl":
                _, cx, cy, st, rad = op
                dx, dy = x - cx, y - cy
                r = np.sqrt(dx * dx + dy * dy)
                th = -st * np.exp(-(r / rad) ** 2)
                c_, s_ = np.cos(th), np.sin(th)
                x = np.where(done, x, cx + dx * c_ - dy * s_); y = np.where(done, y, cy + dx * s_ + dy * c_)
        rgb[~done] = self.ground
        img = rgb
        if ss > 1:
            img = img.reshape(self.H, ss, self.W, ss, 3).mean((1, 3))
        return img

    @staticmethod
    def edges(img, thr=0.04):
        """Colour boundaries (where gold veins / dark ink lines can sit)."""
        g = np.zeros(img.shape[:2], np.float32)
        for c in range(3):
            gy, gx = np.gradient(img[..., c])
            g += np.sqrt(gx * gx + gy * gy)
        return np.clip(g / thr, 0, 1)


def paper_finish(rgb, seed=1, grain=0.05, mottle=0.06, absorb=0.0):
    """Make a flat-rendered colour field read as pigment on paper: fibre grain, light mottling, slight softening."""
    h, w = rgb.shape[:2]
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    m = fbm(w, h, seed + 2, 50, 3) - 0.5
    out = rgb * (1 + g[..., None] * grain * 0.5 + m[..., None] * mottle)
    if absorb:
        out = out * (1 - absorb) + gaussian_filter(out, (absorb * 3, absorb * 3, 0)) * absorb
    return np.clip(out, 0, 1)


def rgba(rgb, a=None):
    h, w = rgb.shape[:2]
    a = np.ones((h, w), np.float32) if a is None else a
    return np.concatenate([rgb.astype(np.float32), a[..., None].astype(np.float32)], -1)


def kb_total(d):
    tot = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d))
    print("TOTAL", d, tot // 1024, "KB")
