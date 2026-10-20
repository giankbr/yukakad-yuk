"""P5 helpers: gouache + ink-line product illustrations for the app-mimic themes (Tier 2 accents).
Every object is drawn with skia paths into masks; fills become opaque gouache with brush streaks and a hand-cut
edge, outlines become a wobbly dry ink line, and a soft wash shadow grounds the object on the card.
"""
import sys, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa

_seed = [1000]
def nxt():
    _seed[0] += 13
    return _seed[0]

def rr(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p

def circ(cx, cy, r):
    p = skia.Path(); p.addCircle(cx, cy, r); return p

def oval(cx, cy, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry)); return p

def poly(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p

def wobbly(pts, rng, amt=0.04):
    return deform(pts, rng, 2, amt)

def fill_mask(w, h, path):
    return mask_from(w, h, lambda cv: cv.c.drawPath(path, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)))

def stroke_m(w, h, path, width):
    def draw(cv):
        cv.c.drawPath(path, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))
    return mask_from(w, h, draw)

def paint(mask, col, col2=None, rough=2.4, streak=0.7, density=0.97):
    return gouache_paint(mask, col, col2, seed=nxt(), rough=rough, streak=streak, density=density)

def ink(w, h, path, width=3.0, col="#2b2220", dry=0.18, wob=2.2):
    """Hand-inked outline: stroked path, wobbled, with dry-brush breaks."""
    m = stroke_m(w, h, path, width)
    m = displace(m, nxt(), wob, 16)
    s = nxt()
    d = fbm(w, h, s, 7, 2)
    m = m * (1 - np.clip((d - (1 - dry)) * 6, 0, 1))
    m = np.clip(gaussian_filter(m, 0.5) * 1.15, 0, 1)
    tone = 0.85 + 0.15 * fbm(w, h, s + 2, 30, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([rgb, (m * 0.92)[..., None]], -1)

def shadow(w, h, path, col, offset=(6, 10), blur=9, strength=0.42):
    m = fill_mask(w, h, path)
    m = np.roll(np.roll(m, offset[1], 0), offset[0], 1)
    m = gaussian_filter(m, blur) * strength
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, m[..., None]], -1)

def wash(w, h, path, col, col2=None, density=0.5):
    return pigment(fill_mask(w, h, path), col, col2, seed=nxt(), density=density, edge=0.45, bloom=0.3, rough=5, feather=1.4)

def highlight(w, h, path, strength=0.35, col="#ffffff"):
    """Soft chalky highlight stroke (top-left light)."""
    m = stroke_m(w, h, path, 5)
    m = displace(m, nxt(), 2, 14)
    m = gaussian_filter(m, 1.2) * strength
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(m, 0, 1)[..., None]], -1)

def shade(layer, w, h, path, col, strength=0.35, blur=6):
    """Darken part of an already painted object (form shadow) — multiplies rgb inside path."""
    m = gaussian_filter(fill_mask(w, h, path), blur) * strength
    out = layer.copy()
    c = np.array(hex_rgb(col), np.float32)
    out[..., :3] = out[..., :3] * (1 - m[..., None]) + out[..., :3] * c * m[..., None]
    return out

def grain(layer, seed, amt=0.05):
    """Paper/brush grain on the finished object so it never reads as flat vector."""
    h, w = layer.shape[:2]
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.8)
    g = (g - g.mean()) / (g.std() + 1e-6)
    out = layer.copy()
    out[..., :3] = np.clip(out[..., :3] * (1 + g[..., None] * amt), 0, 1)
    return out

def preview(arr, path, tone="#ffffff"):
    on_paper(arr, tone).save(path)

def kb(path):
    import os
    return os.path.getsize(path) / 1024

def ink_mask(mask, width=3.0, col="#2b2220", dry=0.18, wob=2.2):
    """Ink outline of a mask's silhouette (union of shapes) — no interior seams."""
    from scipy.ndimage import binary_dilation, binary_erosion
    h, w = mask.shape
    b = mask > 0.5
    k = max(1, int(round(width / 2)))
    edge = binary_dilation(b, iterations=k) & ~binary_erosion(b, iterations=k)
    m = gaussian_filter(edge.astype(np.float32), 0.6)
    m = displace(m, nxt(), wob, 16)
    s = nxt()
    d = fbm(w, h, s, 7, 2)
    m = m * (1 - np.clip((d - (1 - dry)) * 6, 0, 1))
    m = np.clip(m * 1.2, 0, 1)
    tone = 0.85 + 0.15 * fbm(w, h, s + 2, 30, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([rgb, (m * 0.92)[..., None]], -1)
