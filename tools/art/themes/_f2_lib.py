"""Agent F2 helpers (bromo-tengger, sentani-kayu, zanzibar-pintu, suzani-bukhara).
Builds on _j1_lib (bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, hatch), _d1_lib (thread-level loom: ikat)
and _jw_lib (along, spiral_pts). Adds:
  chain_stitch()   thread-level embroidered chain stitch along polylines (suzani)
  chain_fill()     fill a mask with rows of chain stitch that follow its contour (iso-distance rows)
  bark_cloth()     beaten-bark (kombouw / tapa) fibrous texture, tileable
  coral_stone()    lime-washed coral-rag wall texture, tileable
Previews -> /tmp/pen/nb-F2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib, _j1_lib
import _d1_lib
from _d1_lib import ikat  # noqa
from _j1_lib import *  # noqa
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt

PREV = "/tmp/pen/nb-F2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _d1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def col_arr(h):
    return np.array(hex_rgb(h), np.float32)


def mix_hex(a, b, t):
    c = col_arr(a) * (1 - t) + col_arr(b) * t
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in np.clip(c, 0, 1))


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * col_arr(col)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def xgrad(W, H, x0, x1):
    return np.clip((np.arange(W, dtype=np.float32)[None, :] - x0) / (x1 - x0), 0, 1) * np.ones((H, 1), np.float32)


def ygrad(W, H, y0, y1):
    return np.clip((np.arange(H, dtype=np.float32)[:, None] - y0) / (y1 - y0), 0, 1) * np.ones((1, W), np.float32)


def radial(W, H, cx, cy, r, sy=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.clip(1 - np.hypot(xx - cx, (yy - cy) / sy) / r, 0, 1)


def comp_rgb(bg_rgb, layer):
    a = layer[..., 3:4]
    return bg_rgb * (1 - a) + layer[..., :3] * a


def prev_rgb(rgb, name):
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def rgb_save(rgb, path, quality=80, size=None):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im


def kb_report(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)); tot += s
        print(f"  {f:24s} {s // 1024:4d} KB")
    print("  total", tot // 1024, "KB")


def wnoise(w, h, seed, sigma):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def resample(pts, step):
    """Polyline -> points every `step` px, with direction angle: [(x, y, ang)]."""
    out = []; acc = step / 2
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out


def spiral(cx, cy, r0, r1, turns, a0=0.0, n=120, direction=1):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + direction * t * turns * math.tau
        r = r0 + (r1 - r0) * t
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


# ---------------------------------------------------------------- embroidery: chain stitch
class Embroidery:
    """RGBA canvas for thread work: every chain-stitch loop is drawn as twisted thread with its own shading,
    so the result reads at thread level (loops, gaps, sheen), not as a fill."""

    def __init__(self, W, H, seed=1):
        self.W, self.H = W, H
        self.surface = skia.Surface(W, H)
        self.c = self.surface.getCanvas()
        self.c.clear(skia.ColorTRANSPARENT)
        self.rng = random.Random(seed)

    def _paint(self, col, a=1.0, width=None, stroke=False, blur=0):
        r, g, b = hex_rgb(col)
        p = skia.Paint(AntiAlias=True, Color4f=skia.Color4f(r, g, b, a))
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(width or 1)
            p.setStrokeCap(skia.Paint.kRound_Cap)
        if blur:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        return p

    def loop(self, x, y, ang, L, Wd, col, dark, light):
        """One chain loop centred at (x, y), pointing along ang: teardrop of thread around a dark eye."""
        rng = self.rng
        L *= rng.uniform(0.92, 1.08); Wd *= rng.uniform(0.9, 1.1); ang += rng.gauss(0, 0.06)
        c = self.c
        c.save(); c.translate(x, y); c.rotate(math.degrees(ang))
        # shadow under the loop
        sh = skia.Path(); sh.addOval(skia.Rect(-L * 0.55, -Wd * 0.55 + 0.6, L * 0.6, Wd * 0.55 + 1.0))
        c.drawPath(sh, self._paint("#2a1a10", 0.22, blur=0.8))
        # thread body: teardrop (round head forward, tail back where the next loop anchors)
        body = skia.Path()
        body.moveTo(-L * 0.55, 0)
        body.cubicTo(-L * 0.25, -Wd * 0.62, L * 0.45, -Wd * 0.62, L * 0.52, 0)
        body.cubicTo(L * 0.45, Wd * 0.62, -L * 0.25, Wd * 0.62, -L * 0.55, 0)
        c.drawPath(body, self._paint(col, 1.0))
        # dark eye (fabric showing through the loop) + inner shade
        eye = skia.Path(); eye.addOval(skia.Rect(-L * 0.12, -Wd * 0.13, L * 0.28, Wd * 0.13))
        c.drawPath(eye, self._paint(dark, 0.75, blur=0.35))
        # sheen on the upper thread and twist lines
        hi = skia.Path(); hi.moveTo(-L * 0.35, -Wd * 0.18); hi.cubicTo(-L * 0.1, -Wd * 0.48, L * 0.3, -Wd * 0.45, L * 0.42, -Wd * 0.12)
        c.drawPath(hi, self._paint(light, 0.65, width=max(0.6, Wd * 0.16), stroke=True))
        lo = skia.Path(); lo.moveTo(-L * 0.3, Wd * 0.25); lo.cubicTo(-L * 0.05, Wd * 0.5, L * 0.3, Wd * 0.45, L * 0.45, Wd * 0.15)
        c.drawPath(lo, self._paint(dark, 0.4, width=max(0.5, Wd * 0.12), stroke=True))
        for k in range(3):
            u = -0.3 + k * 0.28
            c.drawLine(L * u, -Wd * 0.46, L * (u + 0.06), -Wd * 0.3, self._paint(dark, 0.22, width=0.5, stroke=True))
        c.restore()

    def chain(self, pts, col, step=5.0, width=3.4, dark=None, light=None, jitter=0.25):
        dark = dark or mix_hex(col, "#140a06", 0.55)
        light = light or mix_hex(col, "#fff4dc", 0.45)
        for x, y, a in resample(pts, step):
            self.loop(x + self.rng.gauss(0, jitter), y + self.rng.gauss(0, jitter), a, step * 1.32, width, col, dark, light)

    def satin_dot(self, x, y, r, col):
        light = mix_hex(col, "#fff4dc", 0.45); dark = mix_hex(col, "#140a06", 0.5)
        c = self.c
        n = max(4, int(r * 1.3))
        a0 = self.rng.uniform(0, math.pi)
        for k in range(n):
            t = (k + 0.5) / n * 2 - 1
            hw = math.sqrt(max(0, 1 - t * t)) * r
            ca, sa = math.cos(a0), math.sin(a0)
            ox, oy = -sa * t * r, ca * t * r
            p0 = (x + ox - ca * hw, y + oy - sa * hw); p1 = (x + ox + ca * hw, y + oy + sa * hw)
            c.drawLine(*p0, *p1, self._paint(col, 1.0, width=r * 2 / n * 1.25, stroke=True))
            c.drawLine(*p0, *p1, self._paint(light if t < 0 else dark, 0.25, width=0.6, stroke=True))

    def array(self):
        img = self.surface.makeImageSnapshot()
        return img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType).astype(np.float32) / 255.0


def contour_rows(mask, spacing, min_len=6, start=None):
    """Iso-distance rows inside a mask (outline-following fill rows), as polylines [(x, y)...]."""
    from skimage import measure
    d = distance_transform_edt(mask > 0.5)
    rows = []
    lv = spacing * 0.55 if start is None else start
    k = 0
    while lv < d.max():
        for cnt in measure.find_contours(d, lv):
            if len(cnt) >= min_len:
                rows.append((k, [(float(p[1]), float(p[0])) for p in cnt]))
        lv += spacing
        k += 1
    return rows


def chain_fill(emb, mask, col, spacing=4.0, step=4.4, width=3.0, cols=None, dark=None, light=None):
    """Fill a shape with concentric chain-stitch rows (suzani fill). cols: optional per-row colour cycle."""
    for i, row in contour_rows(mask, spacing):
        c = cols[i % len(cols)] if cols else col
        emb.chain(row, c, step=step, width=width, dark=dark, light=light)


def cotton(W, H, tone="#efe6d2", seed=1, p=3, tile=True):
    """Hand-woven cotton (karbos / ivory ground) at thread level, RGB float."""
    Ty, Tx = H // p, W // p
    D = np.zeros((Ty, Tx), np.int32)
    pal = [tone, mix_hex(tone, "#e2d5bc", 0.35)]
    rng = np.random.default_rng(seed)
    D[:, rng.random(Tx) > 0.86] = 1
    D[rng.random(Ty) > 0.9, :] = 1
    return ikat(D, pal, p=p, mode="double", amp=0.0, coh=1, along=4, seed=seed, bleed=0.2, slub=0.5, fibre=0.1,
                thread_var=0.03, tile=tile)


# ---------------------------------------------------------------- bark cloth (kombouw)
def bark_cloth(W, H, base="#8a5a34", seed=1, tile=True):
    """Beaten tree-bark cloth: long fibres running vertically, cross-hatched beater marks, darker felted patches."""
    rng = np.random.default_rng(seed)
    md = "wrap" if tile else "nearest"
    f1 = gaussian_filter(rng.random((H, W)).astype(np.float32), (9, 0.6), mode=md)
    f2 = gaussian_filter(rng.random((H, W)).astype(np.float32), (30, 1.4), mode=md)
    f1 = (f1 - f1.mean()) / (f1.std() + 1e-6); f2 = (f2 - f2.mean()) / (f2.std() + 1e-6)
    blot = gaussian_filter(rng.random((H, W)).astype(np.float32), W / 14, mode=md)
    blot = (blot - blot.mean()) / (blot.std() + 1e-6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    beat = np.sin(yy / H * math.tau * (H / 7.0) + f2 * 0.8)  # beater grooves (horizontal ridges)
    beat = np.clip(beat, 0, 1) ** 3
    holes = gaussian_filter((rng.random((H, W)) > 0.9993).astype(np.float32), (4, 1.2), mode=md)
    holes = np.clip(holes * 60, 0, 1)
    v = 1 + f1 * 0.07 + f2 * 0.05 + blot * 0.07 - beat * 0.035 - holes * 0.35
    rgb = np.ones((H, W, 3), np.float32) * col_arr(base) * v[..., None]
    warm = np.clip(blot, 0, None)[..., None] * 0.05 * (col_arr("#b0753f") - col_arr(base))
    return np.clip(rgb + warm, 0, 1)


# ---------------------------------------------------------------- coral-rag lime wall
def coral_stone(W, H, tone="#e8dcc4", seed=1, tile=True):
    """Lime-plastered coral-rag wall: worn wash with porous pits, embedded coral stones showing through, stains."""
    rng = np.random.default_rng(seed)
    md = "wrap" if tile else "nearest"
    def nz(sig):
        n = gaussian_filter(rng.random((H, W)).astype(np.float32), sig, mode=md)
        return (n - n.mean()) / (n.std() + 1e-6)
    big, mid, fine = nz(W / 9), nz(6), nz(0.8)
    stones = np.clip((nz(W / 22) - 0.9) * 1.6, 0, 1)
    pits = np.clip((nz(1.3) - 2.0) * 1.5, 0, 1)
    v = 1 + big * 0.03 + mid * 0.02 + fine * 0.025 - pits * 0.22
    rgb = np.ones((H, W, 3), np.float32) * col_arr(tone) * v[..., None]
    rgb = rgb * (1 - stones[..., None] * 0.1) + stones[..., None] * 0.1 * col_arr("#b9a585")
    stain = np.clip(nz(W / 6) * 0.5 + ygrad(W, H, H * 0.2, H)[..., None][..., 0] * 0.0, 0, 1)
    rgb = rgb * (1 - stain[..., None] * 0.04)
    return np.clip(rgb, 0, 1)
