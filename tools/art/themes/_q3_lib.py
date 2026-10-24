"""Agent Q3 helpers (wayang-golek, rumi-seljuk, gradasi-senja, lomba-catur): re-exports _jw_lib (+ _j1/_p1 local
painting helpers) with previews written to /tmp/pen/nb-Q3/art, plus a few small shape utilities."""
import sys, os, math
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import _p1_lib
import art as _art
_p1_lib.PREV = PREV = "/tmp/pen/nb-Q3/art"
os.makedirs(PREV, exist_ok=True)


def clear():
    _art._fbm_cache.clear()


def poly(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def smooth(W, H, pts):
    return shapes(W, H, [pts], smooth=True)


def ink(art, mask, col="#24150c", seed=1, density=0.85):
    """thin painted line work (watercolour-ish ink, no bloom)."""
    return G(art, mask, col, seed=seed, density=density, edge=0.12, bloom=0, rough=0.5, feather=0.4, pad=8)


def rect(W, H, x0, y0, x1, y1, r=0):
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, p)
    return cv.array()[..., 3]


def preview_dark(arr, name, bg):
    preview(arr, name, bg=bg)


def rumi_leaf(x, y, L, ang, flip=1, fat=1.0):
    """Seljuk split-leaf (rumi) outline: a slender wing whose back sweeps over into a long hooked tip, with a
    shorter second tip under it. Local frame: base at (0,0), along +x, length L; flip=-1 mirrors."""
    f = fat
    back = curve([(0, 0), (0.12, -0.12 * f), (0.36, -0.27 * f), (0.66, -0.31 * f), (0.9, -0.22 * f), (1.04, -0.02), (1.02, 0.2), (0.92, 0.34)], 30)
    hook_in = curve([(0.92, 0.34), (0.94, 0.16), (0.88, 0.04), (0.76, -0.02)], 12)
    second = curve([(0.76, -0.02), (0.74, 0.1), (0.64, 0.2)], 8)
    under = curve([(0.64, 0.2), (0.56, 0.1), (0.4, 0.05), (0.18, 0.03), (0, 0)], 14)
    pts = back + hook_in[1:] + second[1:] + under[1:]
    c, s_ = math.cos(ang), math.sin(ang)
    return [(x + (px * c - py * flip * s_) * L, y + (px * s_ + py * flip * c) * L) for px, py in pts]


def star8(cx, cy, R, rot=math.pi / 8, k=0.7654):
    pts = []
    for i in range(16):
        r = R if i % 2 == 0 else R * k
        a = rot + i * math.pi / 8
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def scroll_along(line, amp, period, leaf, phase=0.0, stem_w=5.0, wrap_h=None):
    """Rumi scroll riding a centre line (list of points): a sinuous stem, and in every bay a curled tendril ending in a
    rumi leaf plus a small counter-leaf. Returns (stem_items for strokes(), leaf polygons)."""
    pts = np.array(line, np.float32)
    seg = np.diff(pts, axis=0)
    ln = np.hypot(seg[:, 0], seg[:, 1])
    s_acc = np.concatenate([[0], np.cumsum(ln)])
    total = s_acc[-1]
    def at(sv):
        sv = min(max(sv, 0), total - 1e-3)
        i = int(np.searchsorted(s_acc, sv) - 1); i = max(0, min(i, len(seg) - 1))
        t = (sv - s_acc[i]) / max(ln[i], 1e-6)
        p = pts[i] + seg[i] * t
        tx, ty = seg[i] / max(ln[i], 1e-6)
        return p, (tx, ty), (-ty, tx)
    stem = []
    n = int(total / 3)
    for k in range(n + 1):
        sv = total * k / n
        p, _, nrm = at(sv)
        off = amp * math.sin(math.tau * sv / period + phase)
        stem.append((float(p[0] + nrm[0] * off), float(p[1] + nrm[1] * off)))
    items = [(stem, stem_w, None)]
    leaves = []
    k = 0
    sv = period * 0.25 - phase / math.tau * period
    while sv < total:
        if sv > 0:
            side = 1 if (k % 2 == 0) else -1
            p, tg, nrm = at(sv)
            off = amp * math.sin(math.tau * sv / period + phase)
            base = (p[0] + nrm[0] * off, p[1] + nrm[1] * off)
            # tendril curls from the crest back into the opposite bay
            ang_t = math.atan2(tg[1], tg[0])
            c = [base]
            for j in range(1, 9):
                u = j / 8
                a = ang_t + side * (0.0 + u * 2.4)
                r = amp * (0.25 + 1.15 * u) * (1 - 0.35 * u)
                c.append((base[0] + tg[0] * period * 0.16 * u - nrm[0] * side * r * math.sin(u * 2.2), base[1] + tg[1] * period * 0.16 * u - nrm[1] * side * r * math.sin(u * 2.2)))
            items.append((c, stem_w * 0.75, (0.0, 0.6)))
            end = c[-1]
            a_end = math.atan2(end[1] - c[-3][1], end[0] - c[-3][0])
            leaves.append(rumi_leaf(end[0], end[1], leaf, a_end, side, 1.0))
            # counter leaf on the crest pointing forward
            a_f = ang_t + side * 0.5
            leaves.append(rumi_leaf(base[0], base[1], leaf * 0.7, a_f, -side, 0.9))
        sv += period / 2
        k += 1
    return items, leaves


def relief(field, motif, seed, stone=("#d9c7a6", "#c9b48e"), light="#f4ead6", dark="#6f5a3e", depth=1.0):
    """Carved limestone: flat field, recessed darker ground around a raised motif, emboss lit from upper-left."""
    H, W = field.shape
    base = gouache_paint(field, stone[0], stone[1], seed=seed, rough=0.6, streak=0.4)
    h = gaussian_filter(np.clip(motif, 0, 1), 1.6)
    gy, gx = np.gradient(h)
    lit = np.clip(-(gx + gy) * 9 * depth, -1, 1)
    ground = np.clip(field - motif, 0, 1)
    rgb = base[..., :3]
    dk = np.array(hex_rgb(dark), np.float32); lt = np.array(hex_rgb(light), np.float32)
    amb = gaussian_filter(motif, 3.5) * ground
    rgb = rgb * (1 - ground[..., None] * 0.18) * (1 - amb[..., None] * 0.35 * depth)
    rgb = np.where(lit[..., None] > 0, rgb + (lt - rgb) * lit[..., None] * 0.8, rgb + (dk - rgb) * (-lit[..., None]) * 0.8)
    grit = fbm(W, H, seed + 3, 3, 2)
    rgb = rgb * (0.94 + 0.1 * grit[..., None])
    pits = (fbm(W, H, seed + 5, 2.5, 2) > 0.83).astype(np.float32)
    rgb = rgb * (1 - pits[..., None] * 0.12)
    return np.concatenate([np.clip(rgb, 0, 1), base[..., 3:4]], -1)
