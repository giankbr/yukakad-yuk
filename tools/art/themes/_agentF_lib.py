"""Shared helpers for agent F's theme render scripts (sunda-siger, batak-ulos, bugis-bosara, betawi-ondel).
Extends /tmp/pen/art/art.py without editing it: tiny SVG path parser (to reuse the hand-drawn geometry of the
old SVG ornaments as masks), dark-background previews, banded Mega-Mendung style clouds, misc."""
import sys, re, math, os
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from scipy.ndimage import distance_transform_edt, binary_dilation

_TOK = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?")


def svg_path(d, scale=1.0, ox=0.0, oy=0.0):
    """Parse an SVG path 'd' (M L H V C S Q Z, abs+rel) into a skia.Path, mapped by p*scale + offset."""
    toks = _TOK.findall(d)
    p = skia.Path()
    i = 0; cmd = None; x = y = 0.0; sx0 = sy0 = 0.0; lc = None
    T = lambda a, b: (a * scale + ox, b * scale + oy)
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                p.close(); x, y = sx0, sy0; lc = None; continue
        rel = cmd.islower(); c = cmd.upper()
        if c == "M":
            nx, ny = num(), num()
            if rel: nx += x; ny += y
            p.moveTo(*T(nx, ny)); x, y = nx, ny; sx0, sy0 = x, y; cmd = "l" if rel else "L"; lc = None
        elif c == "L":
            nx, ny = num(), num()
            if rel: nx += x; ny += y
            p.lineTo(*T(nx, ny)); x, y = nx, ny; lc = None
        elif c == "H":
            nx = num() + (x if rel else 0); p.lineTo(*T(nx, y)); x = nx; lc = None
        elif c == "V":
            ny = num() + (y if rel else 0); p.lineTo(*T(x, ny)); y = ny; lc = None
        elif c == "C":
            a = [num() for _ in range(6)]
            if rel: a = [a[k] + (x if k % 2 == 0 else y) for k in range(6)]
            p.cubicTo(*T(a[0], a[1]), *T(a[2], a[3]), *T(a[4], a[5])); lc = (a[2], a[3]); x, y = a[4], a[5]
        elif c == "S":
            a = [num() for _ in range(4)]
            if rel: a = [a[k] + (x if k % 2 == 0 else y) for k in range(4)]
            c1 = (2 * x - lc[0], 2 * y - lc[1]) if lc else (x, y)
            p.cubicTo(*T(*c1), *T(a[0], a[1]), *T(a[2], a[3])); lc = (a[0], a[1]); x, y = a[2], a[3]
        elif c == "Q":
            a = [num() for _ in range(4)]
            if rel: a = [a[k] + (x if k % 2 == 0 else y) for k in range(4)]
            p.quadTo(*T(a[0], a[1]), *T(a[2], a[3])); x, y = a[2], a[3]; lc = None
        else:
            raise ValueError("unsupported path cmd " + cmd)
    return p


def path_mask(w, h, path, stroke=0.0, cap="round"):
    def draw(cv):
        pt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            pt.setStyle(skia.Paint.kStroke_Style); pt.setStrokeWidth(stroke)
            pt.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
            pt.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(path, pt)
    return mask_from(w, h, draw)


def circles_mask(w, h, pts):
    def draw(cv):
        pt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for (x, y, r) in pts:
            cv.c.drawCircle(x, y, r, pt)
    return mask_from(w, h, draw)


def poly_mask(w, h, pts):
    return shape_mask(w, h, pts, smooth=False)


def preview(arr, path, bg="#f7f2e4", paper_tone=None):
    """Composite over a flat colour (or paper) to judge the art on its real page background."""
    h, w = arr.shape[:2]
    if paper_tone:
        base = np.asarray(paper(w, h, paper_tone, 5), np.float32) / 255
    else:
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(path)


def bands(mask, widths):
    """Split a mask into concentric inward bands (Mega Mendung gradation). Returns list of masks, outer → inner,
    the last one being the remaining core."""
    dist = distance_transform_edt(mask > 0.5)
    out = []; acc = 0.0
    for wd in widths:
        out.append(((dist > acc) & (dist <= acc + wd)).astype(np.float32)); acc += wd
    out.append((dist > acc).astype(np.float32))
    return [gaussian_filter(m, 0.6) for m in out]


def grow(mask, px):
    dist = distance_transform_edt(mask < 0.5)
    return gaussian_filter((dist <= px).astype(np.float32), 0.6)


def outline(mask, px):
    """Ring of width px just outside the mask edge."""
    return np.clip(grow(mask, px) - (mask > 0.5), 0, 1)


def shadow(mask, dx=4, dy=6, blur=6, alpha=0.35, col="#000000"):
    m = np.roll(np.roll(mask, dy, 0), dx, 1)
    m = gaussian_filter(m, blur) * alpha
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, m[..., None]], -1)


def tint(arr, k):
    out = arr.copy(); out[..., :3] = np.clip(out[..., :3] * k, 0, 1); return out


def fade(arr, k):
    out = arr.copy(); out[..., 3] *= k; return out


def kb(path):
    return round(os.path.getsize(path) / 1024, 1)
