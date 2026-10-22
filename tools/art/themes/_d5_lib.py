"""Agent D5 helpers (impasto-taman, kebun-anggrek, khitan-pangeran, ultah-istana).
Adds an *impasto oil* medium: directional brush dabs sampled from a colour guide, each dab leaving bristle grooves in a
height map that is lit from the top-left (paint ridges, glossy highlights). Plus small gouache/glass helpers.
Previews -> /tmp/pen/nb-D5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa  (brings _j1_lib / _p1_lib / art)
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-D5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def preview(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.PREV = PREV
    return _p1_lib.preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def rgb_hex(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)


def soft(mask, s):
    return gaussian_filter(mask.astype(np.float32), s)


def fill(guide, mask, col, col2=None, seed=1, scale=60):
    """Paint a colour (optionally drifting to col2 by noise) into an RGB guide where mask (0..1)."""
    h, w = mask.shape
    c = np.array(hex_rgb(col), np.float32)
    if col2:
        t = fbm(w, h, seed, scale, 3)[..., None]
        c = c * (1 - t) + np.array(hex_rgb(col2), np.float32) * t
    m = mask[..., None]
    guide[...] = guide * (1 - m) + c * m
    return guide


def vgrad(h, w, stops):
    t = np.linspace(0, 1, h, dtype=np.float32)
    out = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        k = np.clip((t - t0) / max(1e-6, t1 - t0), 0, 1)[:, None, None]
        sel = ((t >= t0) & (t <= t1))
        ca = np.array(hex_rgb(c0), np.float32); cb = np.array(hex_rgb(c1), np.float32)
        out[sel] = (ca * (1 - k) + cb * k)[sel]
    return out


class Impasto:
    """Oil paint canvas: colour + height surfaces drawn with skia, lit at the end."""

    def __init__(self, W, H, seed=1):
        self.W, self.H = W, H
        self.col = Canvas(W, H, seed)
        self.hgt = Canvas(W, H, seed + 1)
        self.rng = random.Random(seed)

    def _poly(self, x0, y0, mx, my, x1, y1, wd, n=12, tip=0.35):
        pts_l, pts_r = [], []
        for i in range(n + 1):
            t = i / n
            px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
            py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
            dx = 2 * (1 - t) * (mx - x0) + 2 * t * (x1 - mx); dy = 2 * (1 - t) * (my - y0) + 2 * t * (y1 - my)
            d = math.hypot(dx, dy) or 1
            prof = min(1.0, (t / 0.1) ** 0.5 if t < 0.1 else 1.0) * (1 - max(0.0, (t - (1 - tip)) / tip) ** 1.6 * (0.75 if tip < 0.5 else 0.97))
            hw = wd / 2 * prof * self.rng.uniform(0.92, 1.06)
            pts_l.append((px - dy / d * hw, py + dx / d * hw)); pts_r.append((px + dy / d * hw, py - dx / d * hw))
        return pts_l + pts_r[::-1]

    def dab(self, x, y, ang, L, wd, c, hv=None, bristle=True, curl=0.0, guide=None, tip=0.35):
        """One brush dab: tapered stroke of colour c (rgb floats) with bristle streaks (colour picked up from the
        neighbourhood in `guide`) that leave grooves in the height map; paint piles up where the brush lifts."""
        rng = self.rng
        ca, sa = math.cos(ang), math.sin(ang)
        x0, y0 = x - ca * L / 2, y - sa * L / 2
        x1, y1 = x + ca * L / 2, y + sa * L / 2
        mx, my = x - sa * curl * L, y + ca * curl * L
        hv = rng.uniform(0.5, 0.66) if hv is None else hv
        poly = self._poly(x0, y0, mx, my, x1, y1, wd, tip=tip)
        path = poly_path(poly)
        p = skia.Paint(AntiAlias=True, Color4f=skia.Color4f(c[0], c[1], c[2], 1.0))
        self.col.c.drawPath(path, p)
        p.setColor4f(skia.Color4f(hv, hv, hv, 1.0))
        self.hgt.c.drawPath(path, p)
        # paint pile at the lifting end
        g = min(1, hv + 0.12)
        e = skia.Paint(AntiAlias=True, Color4f=skia.Color4f(g, g, g, 0.8))
        e.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, max(0.8, wd * 0.12)))
        self.hgt.c.drawCircle(x0 + (x1 - x0) * 0.86, y0 + (y1 - y0) * 0.86, wd * 0.3, e)
        if not bristle:
            return
        nb = max(3, int(wd / 1.7))
        for k in range(nb):
            off = (k / (nb - 1) - 0.5) * wd * 0.8
            ox, oy = -sa * off, ca * off
            s0 = rng.uniform(0.02, 0.3); s1 = rng.uniform(0.7, 1.04)
            path = skia.Path()
            path.moveTo(x0 + ox + (x1 - x0) * s0, y0 + oy + (y1 - y0) * s0)
            path.quadTo(mx + ox, my + oy, x0 + ox + (x1 - x0) * s1, y0 + oy + (y1 - y0) * s1)
            if guide is not None and rng.random() < 0.45:
                gx = int(min(self.W - 1, max(0, x + rng.gauss(0, wd * 1.5)))); gy = int(min(self.H - 1, max(0, y + rng.gauss(0, wd * 1.5))))
                cc = [0.5 * a + 0.5 * b for a, b in zip(c, guide[gy, gx])]
            else:
                v = rng.uniform(-0.1, 0.1)
                cc = [max(0, min(1, ch * (1 + v) + v * 0.15)) for ch in c]
            bw = rng.uniform(0.8, 1.9)
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=bw, StrokeCap=skia.Paint.kButt_Cap,
                           Color4f=skia.Color4f(cc[0], cc[1], cc[2], rng.uniform(0.3, 0.75)))
            self.col.c.drawPath(path, p)
            g = max(0, min(1, hv + rng.choice([-1, 1]) * rng.uniform(0.06, 0.2)))
            p.setColor4f(skia.Color4f(g, g, g, 0.95))
            self.hgt.c.drawPath(path, p)

    def layer(self, guide, angle, step, L, wd, where=None, jitter=0.9, colvar=0.05, angvar=0.25, curl=0.12,
              thresh=0.5, seed=1, hv=None, lum=0.0, bristle=True, prob=1.0, warm=0.0):
        """Cover the canvas (or `where`) with dabs on a jittered grid. angle: HxW radians field or float."""
        rng = random.Random(seed)
        pts = [(x + rng.uniform(-jitter, jitter) * step, y + rng.uniform(-jitter, jitter) * step)
               for y in np.arange(step / 2, self.H, step) for x in np.arange(step / 2, self.W, step)]
        rng.shuffle(pts)
        for x, y in pts:
            xi, yi = int(min(self.W - 1, max(0, x))), int(min(self.H - 1, max(0, y)))
            if where is not None and where[yi, xi] < thresh:
                continue
            if prob < 1 and rng.random() > prob:
                continue
            c = guide[yi, xi]
            v = rng.gauss(0, colvar)
            c = [max(0, min(1, c[0] * (1 + v) + lum + warm * 0.6 + rng.gauss(0, colvar * 0.4))),
                 max(0, min(1, c[1] * (1 + v) + lum + warm * 0.3 + rng.gauss(0, colvar * 0.4))),
                 max(0, min(1, c[2] * (1 + v) + lum - warm * 0.2 + rng.gauss(0, colvar * 0.4)))]
            a = (angle[yi, xi] if isinstance(angle, np.ndarray) else angle) + rng.gauss(0, angvar)
            self.dab(x, y, a, L * rng.uniform(0.65, 1.3), wd * rng.uniform(0.75, 1.2), c, hv=hv, bristle=bristle,
                     curl=rng.uniform(-curl, curl), guide=guide)

    def finish(self, light=(-0.55, -0.75), relief=3.0, gloss=0.3, ambient=0.8, canvas_tex=0.6, seed=3):
        col = self.col.array()
        hm = self.hgt.array()
        a = col[..., 3]
        h = hm[..., 0] * hm[..., 3]
        h = gaussian_filter(h, 0.9)
        gy, gx = np.gradient(h)
        nx_, ny_ = -gx * relief * 6, -gy * relief * 6
        nz = np.ones_like(nx_)
        nl = np.sqrt(nx_ ** 2 + ny_ ** 2 + nz ** 2)
        nx_, ny_, nz = nx_ / nl, ny_ / nl, nz / nl
        lx, ly = light; lz = 0.75
        ll = math.sqrt(lx * lx + ly * ly + lz * lz); lx, ly, lz = lx / ll, ly / ll, lz / ll
        dif = nx_ * lx + ny_ * ly + nz * lz
        hx, hy, hz = lx, ly, lz + 1
        hl = math.sqrt(hx * hx + hy * hy + hz * hz)
        spec = np.clip(nx_ * hx / hl + ny_ * hy / hl + nz * hz / hl, 0, 1) ** 40 * gloss
        base = dif / lz  # 1.0 on flat paint
        shade = ambient + (1 - ambient) * base
        rgb = col[..., :3] * shade[..., None] + spec[..., None]
        if canvas_tex:  # canvas weave shows through thin paint at the edges
            W, H = self.W, self.H
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            weave = (np.sin(xx * 1.9) * np.sin(yy * 1.9)) * 0.5 + 0.5
            thin = np.clip(1 - h * 1.6, 0, 1)
            rgb = rgb * (1 - canvas_tex * 0.06 * weave[..., None] * thin[..., None])
        return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def dir_from(guide, sigma=6, base=None, mix_=0.6):
    """Stroke direction perpendicular to the luminance gradient (Hertzmann), smoothed; blended with a base field."""
    lum = guide @ np.array([0.3, 0.59, 0.11], np.float32)
    lum = gaussian_filter(lum, sigma)
    gy, gx = np.gradient(lum)
    # smooth the structure tensor (orientation, not sign)
    jxx = gaussian_filter(gx * gx, sigma); jyy = gaussian_filter(gy * gy, sigma); jxy = gaussian_filter(gx * gy, sigma)
    ang = 0.5 * np.arctan2(2 * jxy, jxx - jyy) + math.pi / 2
    if base is not None:
        mag = np.sqrt(jxx + jyy); mag = mag / (mag.max() + 1e-6)
        k = np.clip(mag * 6, 0, 1) * mix_
        # blend angles on the doubled circle
        c = np.cos(2 * ang) * k + np.cos(2 * base) * (1 - k)
        s = np.sin(2 * ang) * k + np.sin(2 * base) * (1 - k)
        ang = 0.5 * np.arctan2(s, c)
    return ang.astype(np.float32)


def ragged(mask, seed, amt=14, scale=30):
    """Brushy unfinished edge for a transparent impasto vignette."""
    return np.clip((displace(mask, seed, amt, scale) - 0.35) * 3, 0, 1)


# ---------------------------------------------------------------- gouache helpers
def ring_m(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def inner_shade(mask, dx, dy, blur=8):
    """Soft crescent inside a shape, offset by (dx, dy): use for form shading in gouache."""
    s = np.clip(gaussian_filter(mask, blur) - np.roll(np.roll(gaussian_filter(mask, blur), dy, 0), dx, 1), 0, 1)
    return np.clip(s * 3, 0, 1) * mask


def rect_m(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)) // 1024
        tot += s
        print(f"  {f}: {s} KB")
    print("  total", tot, "KB")
