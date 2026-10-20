"""Agent P3 helpers on top of art.py (shared by boarding-pass, tiket-kereta, kursi-kereta, paket-liburan,
rencana-perjalanan): rubber stamps / postmarks, gouache travel objects (plane, train, suitcase), clouds, ink
outlines, seamless paper tiles. Never edits art.py."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter, binary_dilation

OUT_ROOT = "/root/w/frontend/public/themes/art"
PREV = "/tmp/pen/nt3-P3"
FONTS = "/tmp/pen/art/themes/_p3_fonts"
FONT_FILES = {
    "bebas": f"{FONTS}/bebas-neue-latin-400-normal.ttf",
    "barlow": f"{FONTS}/barlow-latin-800-normal.ttf",
    "elite": f"{FONTS}/special-elite-latin-400-normal.ttf",
    "mono": f"{FONTS}/jetbrains-mono-latin-800-normal.ttf",
    "caveat": f"{FONTS}/caveat-latin-700-normal.ttf",
}
_tf = {}


def typeface(name):
    if name not in _tf:
        _tf[name] = skia.Typeface.MakeFromFile(FONT_FILES[name])
    return _tf[name]


def outdir(theme):
    d = os.path.join(OUT_ROOT, theme)
    os.makedirs(d, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    return d


class Seeds:
    def __init__(self, s=100):
        self.s = s

    def __call__(self):
        self.s += 17
        return self.s


def preview(arr, path, bg="#f6efe6"):
    h, w = arr.shape[:2]
    base = np.asarray(paper(w, h, bg, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(path)


def save(arr, path, max_w=None, q=82, trim=True):
    if trim:
        size = save_asset(arr, path, max_w=max_w, quality=q)
    else:
        im = to_image(arr)
        if max_w and im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(path, "WEBP", quality=q, method=6); size = im.size
    kb = os.path.getsize(path) / 1024
    print(f"{os.path.basename(path)} {size} {kb:.0f}KB")
    return size


def shade(layer, mask, light=(-0.7, -0.7), k=0.5, blur=6.0, hi="#ffffff", lo="#000000"):
    """Directional form shading inside an object."""
    m = gaussian_filter(mask, blur)
    gy, gx = np.gradient(m)
    d = -(gx * light[0] + gy * light[1])
    d = d / (np.abs(d).max() + 1e-6)
    out = layer.copy()
    hc = np.array(hex_rgb(hi), np.float32); lc = np.array(hex_rgb(lo), np.float32)
    pos = np.clip(d, 0, 1)[..., None] * k; neg = np.clip(-d, 0, 1)[..., None] * k
    out[..., :3] = out[..., :3] * (1 - pos) + hc * pos
    out[..., :3] = out[..., :3] * (1 - neg) + lc * neg
    return out


def tint(layer, mask, col, amt):
    out = layer.copy()
    c = np.array(hex_rgb(col), np.float32)
    m = (np.clip(mask, 0, 1) * amt)[..., None]
    out[..., :3] = out[..., :3] * (1 - m) + c * m
    return out


def darken(layer, mask, amt):
    out = layer.copy()
    out[..., :3] *= (1 - np.clip(mask, 0, 1) * amt)[..., None]
    return out


def clipped(layer, mask):
    out = layer.copy()
    out[..., 3] *= np.clip(mask, 0, 1)
    return out


# ---------- masks ----------
def path_mask(w, h, build, stroke=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
            p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(build(), p)
    return mask_from(w, h, draw)


def ring_mask(w, h, cx, cy, r, width, rng=None, wob=0.0, n=120):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width)
        pts = [(cx + math.cos(t) * (r + (rng.gauss(0, wob) if rng else 0)), cy + math.sin(t) * (r + (rng.gauss(0, wob) if rng else 0)))
               for t in [i / n * math.tau for i in range(n)]]
        cv.c.drawPath(smooth_path(pts), p)
    return mask_from(w, h, draw)


def rrect_mask(w, h, x, y, rw, rh, r, rot=0.0, stroke=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        cv.c.save(); cv.c.translate(x + rw / 2, y + rh / 2); cv.c.rotate(math.degrees(rot))
        cv.c.drawRoundRect(skia.Rect.MakeXYWH(-rw / 2, -rh / 2, rw, rh), r, r, p)
        cv.c.restore()
    return mask_from(w, h, draw)


def dots_mask(w, h, pts):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in pts:
            cv.c.drawCircle(x, y, r, p)
    return mask_from(w, h, draw)


def text_mask(w, h, txt, x, y, size, font="bebas", spacing=0.0, align="center", rot=0.0):
    def draw(cv):
        f = skia.Font(typeface(font), size)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        widths = [f.measureText(ch) + spacing for ch in txt]
        total = sum(widths) - spacing
        cv.c.save(); cv.c.translate(x, y); cv.c.rotate(math.degrees(rot))
        cx = -total / 2 if align == "center" else (0 if align == "left" else -total)
        for ch, wd in zip(txt, widths):
            cv.c.drawString(ch, cx, 0, f, p)
            cx += wd
        cv.c.restore()
    return mask_from(w, h, draw)


def arc_text_mask(w, h, txt, cx, cy, r, a_center, size, font="bebas", spacing=2.0, inside=False):
    """Characters along a circle: a_center is the angle (radians) of the text's middle; inside=True flips for bottom text."""
    def draw(cv):
        f = skia.Font(typeface(font), size)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        widths = [f.measureText(ch) + spacing for ch in txt]
        total = sum(widths) - spacing
        dirn = -1 if inside else 1
        a = a_center - dirn * (total / 2) / r
        for ch, wd in zip(txt, widths):
            am = a + dirn * (wd - spacing) / 2 / r
            x, y = cx + math.cos(am) * r, cy + math.sin(am) * r
            cv.c.save(); cv.c.translate(x, y)
            cv.c.rotate(math.degrees(am + (math.pi / 2 if not inside else -math.pi / 2)))
            cv.c.drawString(ch, -(wd - spacing) / 2, 0, f, p)
            cv.c.restore()
            a += dirn * wd / r
    return mask_from(w, h, draw)


def cloud_mask(w, h, cx, cy, rx, ry, rng, lobes=5, flat=0.55):
    """Puffy cumulus: a flat-ish base ellipse with lobes on top."""
    m = shape_mask(w, h, deform(ellipse_pts(cx, cy + ry * 0.2, rx, ry * flat, 14), rng, 2, 0.05))
    for i in range(lobes):
        t = (i + 0.5) / lobes
        lx = cx - rx + t * rx * 2
        lr = rng.uniform(0.32, 0.55) * ry * (1.3 - abs(t - 0.5) * 1.2)
        ly = cy + ry * 0.2 - lr * 0.55 - ry * 0.25 * (1 - abs(t - 0.5) * 2) * rng.uniform(0.5, 1.2)
        m = np.maximum(m, shape_mask(w, h, deform(ellipse_pts(lx, ly, lr * rng.uniform(1.0, 1.35), lr, 12), rng, 2, 0.06)))
    return np.clip(m, 0, 1)


# ---------- media ----------
def rubber_stamp(mask, col, seed=1, wear=0.45, edge=0.45, rough=1.4, blur=0.5):
    """Worn rubber-stamp ink: uneven coverage (dry patches), heavier pigment at stroke edges, slight squash blur."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 14)
    m = np.clip(gaussian_filter(m, blur) * 1.25, 0, 1)
    inner = gaussian_filter(m, 1.6)
    rim = np.clip(m - inner, 0, 1)
    patchy = fbm(w, h, seed + 5, 9, 3)
    wearmap = 1 - wear * np.clip((patchy - 0.45) * 2.6, 0, 1)
    big = fbm(w, h, seed + 9, 70, 2)
    wearmap *= 0.75 + 0.25 * big
    a = m * (0.68 + edge * rim * 3) * wearmap
    tone = 0.9 + 0.1 * fbm(w, h, seed + 2, 24, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def ink(mask, col, seed, density=0.9, rough=1.4):
    return pigment(mask, col, mix(col, "#000000", .15), seed=seed, density=density, edge=0.35, bloom=0.0, gran=0.25,
                   feather=0.55, rough=rough, mottle=0.25)


def ink_outline(mask, col, seed, width=2.2, rough=1.2, density=0.8, breaks=0.0):
    """Hand-inked contour around a filled mask (gouache + line illustration style)."""
    h, w = mask.shape
    m = np.clip(mask, 0, 1)
    line = (np.abs(gaussian_filter(m, width * 0.6) - 0.5) < 0.22).astype(np.float32)
    line = gaussian_filter(line, 0.5)
    if breaks:
        b = fbm(w, h, seed + 3, 8, 2)
        line *= 1 - np.clip((b - (1 - breaks)) * 6, 0, 1)
    return pigment(line, col, mix(col, "#000000", .2), seed=seed, density=density, edge=0.2, bloom=0.0, gran=0.15,
                   feather=0.45, rough=rough, mottle=0.2)


def gouache_obj(mask, col, col2=None, seed=1, rough=2.5, streak=0.5, light=(-0.6, -0.8), k=0.3, blur=8, hi="#ffffff", lo="#000000"):
    art = gouache_paint(mask, col, col2, seed=seed, rough=rough, streak=streak)
    if k:
        art = shade(art, mask, light=light, k=k, blur=blur, hi=hi, lo=lo)
    return art


def wrap_noise(w, h, rng, sigma):
    n = gaussian_filter(rng.random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def grain_overlay(size, col="#5a3c1e", seed=3, base=0.05, k=2.6, cap=0.22, laid=0.0, fiber=1.0, mottle=1.0, fine=1.0):
    """Seamless transparent paper-grain overlay tile (RGBA)."""
    rng = np.random.default_rng(seed)
    v = wrap_noise(size, size, rng, 30) * 0.018 * mottle + wrap_noise(size, size, rng, 6) * 0.01 * mottle \
        + wrap_noise(size, size, rng, 0.6) * 0.016 * fine + wrap_noise(size, size, rng, (0.5, 7)) * 0.012 * fiber
    a = np.clip(base + v * k, 0, cap)
    if laid:
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
        a += (np.sin(yy / size * math.tau * (size // 4)) * 0.5 + 0.5) * laid
    rgb = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)


def speckles(w, h, rng, n, col, seed, rmin=0.8, rmax=2.4, region=None):
    pts = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        if region is not None and region[min(h - 1, int(y)), min(w - 1, int(x))] < 0.5:
            continue
        pts.append((x, y, rng.uniform(rmin, rmax)))
    return pigment(dots_mask(w, h, pts), col, seed=seed, density=0.7, edge=0.3, bloom=0, rough=0.5, feather=0.4)


# ---------- travel objects (masks in object-local coords; returns dict of part masks) ----------
def airliner_parts(w, h, cx, cy, L, rng, bank=0.0):
    """Side-view airliner flying to the right, nose slightly up. L = fuselage length."""
    s = L / 100.0

    def tf(pts):
        c, sn = math.cos(bank), math.sin(bank)
        return [(cx + (x * s) * c - (y * s) * sn, cy + (x * s) * sn + (y * s) * c) for x, y in pts]
    fus = [(-50, -2), (-46, -7), (-30, -9), (0, -9.5), (30, -9), (44, -6), (50, 0), (44, 6), (26, 9), (-10, 9), (-40, 7), (-50, 3)]
    fus = deform(tf(fus), rng, 2, 0.015)
    fin = [(-48, -5), (-42, -26), (-30, -26), (-22, -7)]
    tailplane = [(-45, 2), (-40, 11), (-30, 11), (-30, 4)]
    wing = [(-5, 4), (-22, 34), (-14, 36), (20, 6), (22, 0)]
    wing2 = [(0, -4), (-16, -16), (-10, -17), (18, -6)]  # far wing behind fuselage
    engine = [(-16, 20), (-6, 17), (6, 17), (8, 21), (2, 26), (-14, 26)]
    cockpit = [(36, -7), (44, -5), (46, -2), (38, -1)]
    windows = [(x, -3.5, 1.6 * s) for x in range(-34, 30, 7)]
    out = {"fus": fus, "fin": deform(tf(fin), rng, 2, 0.02), "tail": deform(tf(tailplane), rng, 1, 0.02),
           "wing": deform(tf(wing), rng, 2, 0.015), "wing2": deform(tf(wing2), rng, 2, 0.02),
           "engine": deform(tf(engine), rng, 2, 0.02), "cockpit": tf(cockpit)}
    out["windows"] = [(tf([(x, y)])[0][0], tf([(x, y)])[0][1], r) for x, y, r in windows]
    return out


def paint_airliner(w, h, parts, rng, nxt, body="#f3efe6", body2="#e2dccf", navy="#1f3556", accent="#f0a53a", ink_col="#24324a"):
    art = blank(w, h)
    m_wing2 = shape_mask(w, h, parts["wing2"])
    art = over(art, gouache_obj(m_wing2, mix(body, "#000000", .35), seed=nxt(), k=0.0))
    m_fin = shape_mask(w, h, parts["fin"])
    art = over(art, gouache_obj(m_fin, accent, mix(accent, "#c4702a", .5), seed=nxt(), light=(-0.3, -0.9), k=0.25))
    m_tail = shape_mask(w, h, parts["tail"])
    art = over(art, gouache_obj(m_tail, body2, seed=nxt(), k=0.2))
    m_fus = shape_mask(w, h, parts["fus"])
    art = over(art, gouache_obj(m_fus, body, body2, seed=nxt(), light=(-0.2, -1.0), k=0.32, blur=6, lo="#6d7a8a"))
    # belly stripe in navy
    belly = clipped(gouache_paint(np.clip(m_fus - gaussian_filter(m_fus, 0) * 0, 0, 1), navy, seed=nxt(), rough=1.5), m_fus)
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32)
    cyl = np.array([p[1] for p in parts["fus"]]).mean()
    band = np.clip((yy - (cyl + 4.5 * (parts["fus"][6][0] - parts["fus"][0][0]) / 100)) / 2.0, 0, 1)
    art = over(art, clipped(belly, band))
    # windows + cockpit
    win = dots_mask(w, h, parts["windows"])
    art = over(art, gouache_paint(win, ink_col, seed=nxt(), rough=0.8, streak=0))
    cp = shape_mask(w, h, parts["cockpit"])
    art = over(art, gouache_paint(cp, ink_col, seed=nxt(), rough=0.8, streak=0))
    m_wing = shape_mask(w, h, parts["wing"])
    art = over(art, gouache_obj(m_wing, body2, mix(body2, "#8e97a3", .4), seed=nxt(), light=(0.2, -1.0), k=0.3))
    m_eng = shape_mask(w, h, parts["engine"])
    art = over(art, gouache_obj(m_eng, mix(body, "#9aa3ad", .3), seed=nxt(), k=0.35))
    # accent cheat-line on the wing root
    whole = np.clip(m_fus + m_wing + m_fin + m_tail + m_eng + m_wing2, 0, 1)
    art = over(art, ink_outline(whole, ink_col, nxt(), width=1.9, density=0.55, breaks=0.15))
    art = over(art, ink_outline(np.clip(m_wing + m_eng, 0, 1), ink_col, nxt(), width=1.5, density=0.4, breaks=0.25))
    return art, whole


def paint_suitcase(w, h, cx, cy, W, rng, nxt, col="#c0663b", col2="#9e4f2b", trim="#f0d9a6", ink_col="#3a2a20", stickers=True):
    """Vintage suitcase, front view, slightly tilted; returns (art, mask)."""
    H = W * 0.72
    rot = rng.uniform(-0.06, 0.06)
    body = rrect_mask(w, h, cx - W / 2, cy - H / 2, W, H, W * 0.07, rot)
    body = np.clip(displace(body, nxt(), 2.0, 30), 0, 1)
    art = blank(w, h)
    art = over(art, gouache_obj(body, col, col2, seed=nxt(), light=(-0.5, -0.9), k=0.28, blur=W * 0.06, lo="#4a2414"))
    # straps
    for sx in (-0.26, 0.26):
        strap = rrect_mask(w, h, cx + sx * W - W * 0.04, cy - H / 2, W * 0.08, H, 2, rot)
        art = over(art, clipped(gouache_obj(strap, trim, mix(trim, "#b89860", .5), seed=nxt(), k=0.2), body))
        buckle = rrect_mask(w, h, cx + sx * W - W * 0.05, cy - H * 0.05, W * 0.1, H * 0.11, 2, rot)
        art = over(art, gouache_paint(buckle, "#8c7a4a", seed=nxt(), rough=1.0))
    # lid seam
    seam = rrect_mask(w, h, cx - W / 2, cy - H * 0.12, W, 2.2, 1, rot)
    art = over(art, clipped(gouache_paint(seam, col2, seed=nxt(), rough=0.6), body))
    # corner caps
    for ex in (-1, 1):
        for ey in (-1, 1):
            cap = shape_mask(w, h, deform(ellipse_pts(cx + ex * W * 0.46, cy + ey * H * 0.44, W * 0.07, W * 0.07, 10), rng, 1, 0.03))
            art = over(art, clipped(gouache_obj(cap, "#5a3c22", seed=nxt(), k=0.25), body))
    # handle
    handle = rrect_mask(w, h, cx - W * 0.16, cy - H / 2 - W * 0.09, W * 0.32, W * 0.12, W * 0.05, rot, stroke=W * 0.035)
    handle *= 1 - gaussian_filter(body, 0.5)
    art = over(art, gouache_obj(handle, "#4e3421", seed=nxt(), k=0.2))
    whole = np.clip(body + handle, 0, 1)
    if stickers:
        # travel stickers: circle, lozenge, small rect
        st1 = shape_mask(w, h, deform(ellipse_pts(cx - W * 0.08, cy + H * 0.12, W * 0.1, W * 0.1, 12), rng, 1, 0.03))
        art = over(art, gouache_paint(st1, "#f2e8cf", seed=nxt(), rough=1.0))
        art = over(art, rubber_stamp(ring_mask(w, h, cx - W * 0.08, cy + H * 0.12, W * 0.072, W * 0.014), "#2f5f9e", nxt(), wear=0.3))
        st2 = rrect_mask(w, h, cx + W * 0.04, cy - H * 0.02, W * 0.18, W * 0.1, 2, rot - 0.25)
        art = over(art, gouache_paint(st2, "#e9c45a", seed=nxt(), rough=1.0))
        art = over(art, clipped(rubber_stamp(text_mask(w, h, "BALI", cx + W * 0.13, cy + H * 0.08 - 0, W * 0.07, "bebas", 1, rot=rot - 0.25), "#3a2a20", nxt(), wear=0.35), st2))
        st3 = shape_mask(w, h, deform(ellipse_pts(cx + W * 0.3, cy + H * 0.2, W * 0.07, W * 0.07, 10), rng, 1, 0.03))
        art = over(art, gouache_paint(st3, "#d94f3d", seed=nxt(), rough=1.0))
    art = over(art, ink_outline(whole, ink_col, nxt(), width=2.4, density=0.75, breaks=0.1))
    return art, whole


def paint_locomotive(w, h, cx, cy, L, rng, nxt, col="#243a6e", col2="#1b2c55", accent="#f26a21", ink_col="#1d2238", cream="#f2e9d6"):
    """Side-view streamlined electric loco (Indonesian KA style), nose to the right. L = length. Returns (art, mask)."""
    s = L / 100.0
    H = 34 * s
    def P(pts): return [(cx + x * s, cy + y * s) for x, y in pts]
    body = [(-50, -14), (-50, 10), (-44, 14), (44, 14), (50, 8), (50, 0), (44, -10), (34, -16), (24, -17), (-46, -17)]
    m_body = shape_mask(w, h, deform(P(body), rng, 2, 0.01), smooth=False)
    m_body = np.clip(displace(m_body, nxt(), 1.6, 26), 0, 1)
    art = blank(w, h)
    art = over(art, gouache_obj(m_body, col, col2, seed=nxt(), light=(-0.3, -0.95), k=0.28, blur=L * 0.05, lo="#0d1530"))
    # cream band + accent stripe
    band = rrect_mask(w, h, cx - 50 * s, cy - 6 * s, 100 * s, 9 * s, 1)
    art = over(art, clipped(gouache_paint(band, cream, seed=nxt(), rough=1.2), m_body))
    stripe = rrect_mask(w, h, cx - 50 * s, cy + 3.5 * s, 100 * s, 3 * s, 1)
    art = over(art, clipped(gouache_paint(stripe, accent, seed=nxt(), rough=1.0), m_body))
    # windows
    wins = np.zeros((h, w), np.float32)
    for x in range(-44, 20, 10):
        wins = np.maximum(wins, rrect_mask(w, h, cx + x * s, cy - 14 * s, 6.5 * s, 6 * s, 1.2 * s))
    wins = np.maximum(wins, shape_mask(w, h, P([(26, -15), (36, -14), (44, -8), (44, -5), (26, -6)]), smooth=False))
    art = over(art, clipped(gouache_paint(wins, "#9fc0d8", "#6f93b4", seed=nxt(), rough=0.8), m_body))
    # pantograph + roof gear
    pant = stroke_mask(w, h, [(cx - 20 * s, cy - 17 * s), (cx - 8 * s, cy - 27 * s), (cx + 4 * s, cy - 17 * s)], 2.2 * s, (0.05, 0.05))
    pant = np.maximum(pant, stroke_mask(w, h, [(cx - 16 * s, cy - 28 * s), (cx + 0 * s, cy - 28 * s)], 1.8 * s, (0.05, 0.05)))
    art = over(art, gouache_paint(pant, ink_col, seed=nxt(), rough=0.6, streak=0))
    # bogies + wheels
    bog = np.zeros((h, w), np.float32)
    for bx in (-30, 24):
        bog = np.maximum(bog, rrect_mask(w, h, cx + (bx - 12) * s, cy + 13 * s, 24 * s, 5 * s, 1.5 * s))
    art = over(art, gouache_paint(bog, "#2a2a30", seed=nxt(), rough=1.0))
    wheels = dots_mask(w, h, [(cx + x * s, cy + 18 * s, 4.2 * s) for x in (-37, -24, 17, 30)])
    art = over(art, gouache_obj(wheels, "#33363f", "#1c1e26", seed=nxt(), k=0.2, blur=3))
    hubs = dots_mask(w, h, [(cx + x * s, cy + 18 * s, 1.4 * s) for x in (-37, -24, 17, 30)])
    art = over(art, gouache_paint(hubs, cream, seed=nxt(), rough=0.4, streak=0))
    # headlight
    lamp = dots_mask(w, h, [(cx + 47 * s, cy + 1 * s, 2.4 * s)])
    art = over(art, gouache_paint(lamp, "#ffe9a8", seed=nxt(), rough=0.5, streak=0))
    whole = np.clip(m_body + bog + wheels + pant, 0, 1)
    art = over(art, ink_outline(np.clip(m_body + bog, 0, 1), ink_col, nxt(), width=2.4, density=0.75, breaks=0.1))
    return art, whole


def paint_coach(w, h, cx, cy, L, rng, nxt, col="#243a6e", col2="#1b2c55", accent="#f26a21", ink_col="#1d2238", cream="#f2e9d6"):
    s = L / 100.0
    m_body = rrect_mask(w, h, cx - 50 * s, cy - 16 * s, 100 * s, 30 * s, 5 * s)
    m_body = np.clip(displace(m_body, nxt(), 1.6, 26), 0, 1)
    art = blank(w, h)
    art = over(art, gouache_obj(m_body, col, col2, seed=nxt(), light=(-0.3, -0.95), k=0.28, blur=L * 0.05, lo="#0d1530"))
    band = rrect_mask(w, h, cx - 50 * s, cy - 6 * s, 100 * s, 9 * s, 1)
    art = over(art, clipped(gouache_paint(band, cream, seed=nxt(), rough=1.2), m_body))
    stripe = rrect_mask(w, h, cx - 50 * s, cy + 3.5 * s, 100 * s, 3 * s, 1)
    art = over(art, clipped(gouache_paint(stripe, accent, seed=nxt(), rough=1.0), m_body))
    wins = np.zeros((h, w), np.float32)
    for x in range(-44, 46, 11):
        wins = np.maximum(wins, rrect_mask(w, h, cx + x * s, cy - 13.5 * s, 7.5 * s, 6 * s, 1.2 * s))
    art = over(art, clipped(gouache_paint(wins, "#9fc0d8", "#6f93b4", seed=nxt(), rough=0.8), m_body))
    bog = np.zeros((h, w), np.float32)
    for bx in (-30, 30):
        bog = np.maximum(bog, rrect_mask(w, h, cx + (bx - 12) * s, cy + 13 * s, 24 * s, 5 * s, 1.5 * s))
    art = over(art, gouache_paint(bog, "#2a2a30", seed=nxt(), rough=1.0))
    wheels = dots_mask(w, h, [(cx + x * s, cy + 18 * s, 4.2 * s) for x in (-37, -24, 24, 37)])
    art = over(art, gouache_obj(wheels, "#33363f", "#1c1e26", seed=nxt(), k=0.2, blur=3))
    hubs = dots_mask(w, h, [(cx + x * s, cy + 18 * s, 1.4 * s) for x in (-37, -24, 24, 37)])
    art = over(art, gouache_paint(hubs, cream, seed=nxt(), rough=0.4, streak=0))
    whole = np.clip(m_body + bog + wheels, 0, 1)
    art = over(art, ink_outline(np.clip(m_body + bog, 0, 1), ink_col, nxt(), width=2.4, density=0.75, breaks=0.1))
    return art, whole


def postmark(w, h, cx, cy, r, top, bottom, center, rng, nxt, col="#b23a2c", font="bebas", wear=0.45, rot=-0.2, center_font="bebas", center_size=None, date=None):
    """Round worn rubber postmark with arc text top/bottom and centre lines."""
    m = ring_mask(w, h, cx, cy, r, r * 0.06, rng, r * 0.006)
    m = np.maximum(m, ring_mask(w, h, cx, cy, r * 0.9, r * 0.025, rng, r * 0.006))
    m = np.maximum(m, ring_mask(w, h, cx, cy, r * 0.64, r * 0.03, rng, r * 0.006))
    size = r * 0.19
    m = np.maximum(m, arc_text_mask(w, h, top, cx, cy, r * 0.76, -math.pi / 2 + rot, size, font, spacing=size * 0.18))
    if bottom:
        m = np.maximum(m, arc_text_mask(w, h, bottom, cx, cy, r * 0.76, math.pi / 2 + rot, size, font, spacing=size * 0.18, inside=True))
    # stars between arcs
    for a in (0 + rot, math.pi + rot):
        m = np.maximum(m, dots_mask(w, h, [(cx + math.cos(a) * r * 0.76, cy + math.sin(a) * r * 0.76, r * 0.04)]))
    cs = center_size or r * 0.28
    m = np.maximum(m, text_mask(w, h, center, cx, cy + cs * 0.35 - (r * 0.12 if date else 0), cs, center_font, spacing=cs * 0.05, rot=rot))
    if date:
        m = np.maximum(m, text_mask(w, h, date, cx, cy + r * 0.3, r * 0.13, "mono", spacing=0, rot=rot))
    return rubber_stamp(m, col, nxt(), wear=wear)
