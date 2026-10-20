"""Syari Zamrud — gold-foil Islamic geometry (8-point khatam stars) over emerald watercolour washes. No photos.
Run: python3 -I /tmp/pen/art/themes/syari-zamrud.py   (ONLY=<name> renders one asset)
Assets → /root/w/frontend/public/themes/art/syari-zamrud/
  cover.webp     opaque painted cover: emerald washes, khatam lattice, medallion, two fanous lanterns   css 390x780 → 780x1560
  lantern.webp   single hanging lantern (sways via CSS)                                                css 56 wide → 112
  pattern.webp   seamless foil lattice tile for alt sections                                           css 120 → 240
  star.webp      8-point (rub el hizb) foil star for the monogram (turns slowly)                        css 98 → 196
  divider.webp   foil rule with a small khatam star                                                    css 150x18 → 300x36
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _r1_lib import *  # noqa
import art as _art

OUT = outdir("syari-zamrud")
ONLY = os.environ.get("ONLY")
rng = random.Random(41)
nx = Seq(4100)
GOLD = "#d4af37"
EM_TOP, EM_MID, EM_BOT = "#0f3d2e", "#0d3527", "#0a2a20"


def want(n):
    return ONLY in (None, n)


def star8(cx, cy, R, rot=0.0):
    """Outline points of an 8-point star made of two overlapping squares (khatam)."""
    pts = []
    for k in range(16):
        a = rot + k * math.pi / 8
        r = R if k % 2 == 0 else R * 0.7654   # inner vertices where the two squares cross
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def poly_stroke(W, H, pts, width, closed=True):
    def draw(cv):
        p = poly_path(pts) if closed else None
        if not closed:
            p = skia.Path(); p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                           StrokeJoin=skia.Paint.kMiter_Join)
        cv.c.drawPath(p, paint)
    return mask_from(W, H, draw)


def worn(mask, seed, amt=0.35, scale=5):
    """Foil that didn't fully take: speckled gaps + slightly uneven line weight."""
    h, w = mask.shape
    sp = fbm(w, h, seed, scale, 2)
    m = displace(mask, seed + 3, 0.9, 14)
    return np.clip(m * (1 - amt * np.clip((sp - 0.6) * 4, 0, 1)), 0, 1)


def lattice_mask(W, H, s, line=2.2, ox=0.0, oy=0.0):
    """8-point star & cross lattice with period s (seamless when the canvas is a multiple of s)."""
    m = np.zeros((H, W), np.float32)
    nxs, nys = int(W / s) + 2, int(H / s) + 2
    for i in range(-int(ox / s) - 2, nxs):
        for j in range(-int(oy / s) - 2, nys):
            cx, cy = ox + i * s, oy + j * s
            m = np.maximum(m, poly_stroke(W, H, star8(cx, cy, s * 0.36), line))
            # axis bands joining neighbouring star tips
            for dx, dy in ((1, 0), (0, 1)):
                a = (cx + dx * s * 0.36, cy + dy * s * 0.36)
                b = (cx + dx * s * 0.64, cy + dy * s * 0.64)
                m = np.maximum(m, poly_stroke(W, H, [a, b], line * 0.8, closed=False))
            # diagonal bands meet in a small square rosette at the cell centre
            ccx, ccy = cx + s / 2, cy + s / 2
            q = s * 0.11
            m = np.maximum(m, poly_stroke(W, H, [(ccx - q, ccy - q), (ccx + q, ccy - q), (ccx + q, ccy + q), (ccx - q, ccy + q)], line * 0.8))
            tip = s * 0.36 * math.cos(math.pi / 4)
            for sx_, sy_ in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                a = (ccx - sx_ * (s / 2 - tip), ccy - sy_ * (s / 2 - tip))
                b = (ccx - sx_ * q, ccy - sy_ * q)
                m = np.maximum(m, poly_stroke(W, H, [a, b], line * 0.8, closed=False))
    return m


def medallion_mask(W, H, cx, cy, R):
    m = np.zeros((H, W), np.float32)
    m = np.maximum(m, ring_mask(W, H, cx, cy, R, R * 0.025))
    m = np.maximum(m, ring_mask(W, H, cx, cy, R * 0.92, R * 0.012))
    # 16 pointed petals between the rings and the big star
    for k in range(16):
        a = k * math.pi / 8 + math.pi / 16
        m = np.maximum(m, poly_stroke(W, H, petal_pts(cx + math.cos(a) * R * 0.55, cy + math.sin(a) * R * 0.55, R * 0.34, R * 0.07, a, n=14), R * 0.012))
    m = np.maximum(m, poly_stroke(W, H, star8(cx, cy, R * 0.62), R * 0.03))
    m = np.maximum(m, poly_stroke(W, H, star8(cx, cy, R * 0.5, math.pi / 8), R * 0.014))
    m = np.maximum(m, shape_mask(W, H, star8(cx, cy, R * 0.26), smooth=False))
    m = np.maximum(m, ring_mask(W, H, cx, cy, R * 0.34, R * 0.012))
    return m


def emerald_ground(W, H, seed_base):
    g = painted_sky(W, H, [(0, EM_TOP), (0.5, EM_MID), (1.0, EM_BOT)], seed=seed_base, streak=0.8, grain=0.9)
    # watercolour washes on a dark ground: lighter emerald blooms and deep pools, with granulation
    for (cx, cy, rx, ry, col, dens) in [(W * 0.3, H * 0.18, W * 0.42, H * 0.16, "#1e6b52", 0.45), (W * 0.78, H * 0.3, W * 0.36, H * 0.14, "#1a5e48", 0.4),
                                        (W * 0.5, H * 0.08, W * 0.5, H * 0.1, "#226f55", 0.35), (W * 0.2, H * 0.55, W * 0.35, H * 0.12, "#062319", 0.55),
                                        (W * 0.85, H * 0.7, W * 0.3, H * 0.14, "#05201a", 0.5)]:
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, ry, 12), rng, 2, 0.12))
        g = over(g, pigment(m, col, mix(col, "#2c7a5f", 0.3), seed=nx(), density=dens, edge=0.5, bloom=0.5, gran=0.45, rough=16, feather=4))
    return g


# ---------------- cover ----------------
if want("cover"):
    W, H = 780, 1560
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cv = emerald_ground(W, H, nx())
    # lattice field, strongest behind the medallion, fading down and toward the edges
    lat = lattice_mask(W, H, 104, 2.4, ox=W / 2, oy=330)
    fade = np.exp(-(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - 330) / 520) ** 2)) * np.clip((1000 - yy) / 500, 0, 1)
    lf = foil(worn(lat, nx(), 0.5), GOLD, seed=nx(), emboss=0.4, sparkle=0.15)
    lf[..., 3] *= fade * 0.42
    cv = over(cv, lf)
    # dark halo so the medallion reads
    halo = circle_mask(W, H, W / 2, 330, 190)
    cv = over(cv, pigment(halo, "#072a1f", seed=nx(), density=0.6, edge=0.3, bloom=0.3, rough=10, feather=8))
    med = medallion_mask(W, H, W / 2, 330, 168)
    cv = over(cv, soft_shadow(med, "#000000", blur=4, strength=0.45, dx=3, dy=5))
    cv = over(cv, foil(worn(med, nx(), 0.28), GOLD, seed=nx(), emboss=0.75, sparkle=0.3))
    # corner spandrels: quarter khatam rosettes at the top corners
    for sx in (0, W):
        sp = medallion_mask(W, H, sx, 0, 150)
        f = foil(worn(sp, nx(), 0.35), GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
        f[..., 3] *= 0.8
        cv = over(cv, f)
    # gentle vignette + the lower area calmer for the text
    calm = np.clip((yy - 760) / 500, 0, 1)
    cv[..., :3] = cv[..., :3] * (1 - calm[..., None] * 0.35) + np.array(hex_rgb(EM_BOT), np.float32) * calm[..., None] * 0.35
    cv = vignette(cv, 0.35)
    save_rgb(cv, f"{OUT}/cover.webp", quality=70)
    Image.fromarray((np.clip(cv[..., :3], 0, 1) * 255).astype(np.uint8)).resize((390, 780)).save(f"{PREV}/sz-cover.png")
    _art._fbm_cache.clear()

# ---------------- lantern (fanous) ----------------
if want("lantern"):
    W, H = 120, 420
    cx = W / 2
    lay = blank(W, H)
    chain = np.zeros((H, W), np.float32)
    for k in range(18):
        y = 4 + k * 12
        chain = np.maximum(chain, shape_mask(W, H, ellipse_pts(cx + (k % 2) * 0.6, y + 5, 2.4 if k % 2 else 1.4, 5.5, 10)))
    top = 220
    body = [(cx - 30, top + 52), (cx - 38, top + 92), (cx - 30, top + 136), (cx + 30, top + 136), (cx + 38, top + 92), (cx + 30, top + 52)]
    bm = shape_mask(W, H, body, smooth=False)
    # warm light inside the panes (gouache, opaque) + glow outside
    light = gouache_paint(bm, "#f6cf72", "#f0b649", seed=nx(), rough=0.6, streak=0.5)
    lay = over(lay, glow(bm, "#f3c661", radius=14, strength=0.35))
    lay = over(lay, light)
    frame = np.zeros((H, W), np.float32)
    frame = np.maximum(frame, poly_stroke(W, H, body, 3.4))
    for x in (cx - 12, cx + 12):
        frame = np.maximum(frame, poly_stroke(W, H, [(x * 1.0, top + 52), (x + (x - cx) * 0.4, top + 92), (x, top + 136)], 2.2, closed=False))
    frame = np.maximum(frame, poly_stroke(W, H, [(cx - 38, top + 92), (cx + 38, top + 92)], 2.0, closed=False))
    # pierced star in the middle pane
    frame = np.maximum(frame, poly_stroke(W, H, star8(cx, top + 92, 9), 1.6))
    cap = [(cx - 32, top + 52), (cx - 24, top + 36), (cx - 8, top + 24), (cx, top + 10), (cx + 8, top + 24), (cx + 24, top + 36), (cx + 32, top + 52)]
    capm = shape_mask(W, H, cap)
    base = [(cx - 32, top + 136), (cx + 32, top + 136), (cx + 18, top + 150), (cx + 4, top + 158), (cx, top + 176), (cx - 4, top + 158), (cx - 18, top + 150)]
    basem = shape_mask(W, H, base, smooth=False)
    ring = ring_mask(W, H, cx, top + 4, 6, 2.4)
    metal = np.clip(frame + capm + basem + ring + chain, 0, 1)
    lay = over(lay, foil(worn(metal, nx(), 0.25, 3), GOLD, seed=nx(), emboss=0.8, sparkle=0.25))
    # pierced dots in the cap let light through
    for k in range(5):
        lay = over(lay, gouache_paint(circle_mask(W, H, cx - 14 + k * 7, top + 42, 1.6), "#fde6a6", seed=nx(), rough=0.2))
    save(lay, f"{OUT}/lantern.webp", max_w=112, quality=82)
    preview(lay, "sz-lantern", bg=EM_TOP)

# ---------------- seamless lattice tile ----------------
if want("pattern"):
    T_ = 240
    lat = lattice_mask(T_, T_, 120, 2.2, ox=0, oy=0)
    f = foil(worn(lat, nx(), 0.45, 4), GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
    save_full(f, f"{OUT}/pattern.webp", quality=72)
    preview(f, "sz-pattern", bg="#0a2e22")

# ---------------- monogram star ----------------
if want("star"):
    S = 200
    m = poly_stroke(S, S, star8(S / 2, S / 2, S * 0.47), 2.6)
    m = np.maximum(m, poly_stroke(S, S, star8(S / 2, S / 2, S * 0.3), 1.3))
    for k in range(8):
        a = k * math.pi / 4
        m = np.maximum(m, circle_mask(S, S, S / 2 + math.cos(a) * S * 0.47, S / 2 + math.sin(a) * S * 0.47, 2.8))
    f = foil(worn(m, nx(), 0.3, 3), GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    f[..., 3] *= 0.75
    save_full(f, f"{OUT}/star.webp", quality=80)
    preview(f, "sz-star", bg="#0a2e22")

# ---------------- divider ----------------
if want("divider"):
    W, H = 300, 36
    m = np.zeros((H, W), np.float32)
    for sg in (-1, 1):
        pts = [(W / 2 + sg * 22, 18), (W / 2 + sg * 132, 18)]
        m = np.maximum(m, stroke_mask(W, H, [(pts[0][0] + (pts[1][0] - pts[0][0]) * u, 18) for u in np.linspace(0, 1, 30)], 2.2, taper=(0.02, 0.7)))
        m = np.maximum(m, poly_stroke(W, H, [(W / 2 + sg * 40, 18), (W / 2 + sg * 46, 13), (W / 2 + sg * 52, 18), (W / 2 + sg * 46, 23)], 1.4))
    m = np.maximum(m, shape_mask(W, H, star8(W / 2, 18, 12), smooth=False))
    m = np.maximum(m, ring_mask(W, H, W / 2, 18, 15.5, 1.2))
    f = foil(worn(m, nx(), 0.25, 3), GOLD, seed=nx(), emboss=0.7, sparkle=0.2)
    save_full(f, f"{OUT}/divider.webp", quality=82)
    preview(f, "sz-divider", bg="#0a2e22")

print("total KB:", sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1024)
