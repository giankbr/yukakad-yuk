"""Malam Rimba — dark botanical gouache (monstera, palm, fern) with gold-leaf edges, painted firefly glows.
Run: python3 -I /tmp/pen/art/themes/malam-rimba.py   (ONLY=<name> renders one asset)
Assets → /root/w/frontend/public/themes/art/malam-rimba/
  night.webp        opaque painted night-forest backdrop (cover/opening bg)      css 390 wide → 780
  canopy.webp       top leaf frame (monstera + palm + fern, gold edges)           css 390 → 780
  undergrowth.webp  bottom corner leaves, centre kept open for text             css 390 → 780
  fireflies.webp    tileable glow layer (drifts via CSS)                          css 390x520 → 780x1040
  frond.webp        single gold-edged monstera leaf for section corners          css 150 → 300
  leaf.webp         tiny gold leaf pair for the heading divider                  css 30x14 → 60x28
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _r1_lib import *  # noqa
import art as _art

OUT = outdir("malam-rimba")
ONLY = os.environ.get("ONLY")
rng = random.Random(71)
nx = Seq(7100)
GOLD = "#c9a24b"
G_DARK, G_MID, G_LIT = "#16301f", "#21432d", "#2f5c3c"
INK_BG = "#0b0f0c"


def want(name):
    return ONLY in (None, name)


def T(pts, x0, y0, ang, s=1.0, flip=False):
    c, si = math.cos(ang), math.sin(ang)
    out = []
    for x, y in pts:
        y = -y if flip else y
        x *= s; y *= s
        out.append((x0 + x * c - y * si, y0 + x * si + y * c))
    return out


def monstera(W, H, x0, y0, ang, L, flip=False, cols=(G_DARK, G_MID, G_LIT), gold=0.8, seed_rng=None, detail=True, depth=0.0):
    """Monstera deliciosa leaf: heart outline, edge slits, a few holes. Returns (rgba layer, mask)."""
    r = seed_rng or rng
    Wd = L * 0.46
    f = lambda t: (math.sin(math.pi * min(1, t * 1.02)) ** 0.75) * (1.0 + 0.25 * (1 - t)) * 0.92
    up = [(L * t, -Wd * f(t)) for t in np.linspace(0.02, 1.0, 18)]
    lo = [(L * t, Wd * f(t)) for t in np.linspace(1.0, 0.02, 18)]
    lobe_lo = [(-L * 0.06, Wd * 0.62), (-L * 0.16, Wd * 0.36), (-L * 0.12, Wd * 0.12), (L * 0.04, 0.0)]
    lobe_up = [(-L * 0.12, -Wd * 0.12), (-L * 0.16, -Wd * 0.36), (-L * 0.06, -Wd * 0.62)]
    outline = up + lo + lobe_lo + lobe_up
    m = shape_mask(W, H, deform(T(outline, x0, y0, ang, 1, flip), r, 2, 0.012))
    cut = np.zeros((H, W), np.float32)
    ribs = []
    for k, t in enumerate(np.linspace(0.16, 0.86, 7)):
        for sg in (-1, 1):
            e = (L * (t + 0.03), sg * Wd * f(t) * 1.15)
            inner_t = t - 0.08
            i_ = (L * inner_t, sg * Wd * f(t) * (0.28 + 0.12 * r.random()))
            ribs.append(((L * (inner_t - 0.12), 0), e))
            if r.random() < 0.85:
                wdg = L * r.uniform(0.006, 0.012)
                mx_ = ((e[0] + i_[0]) / 2 + L * 0.015, (e[1] + i_[1]) / 2)
                sl = curve([i_, mx_, (e[0], e[1] * 1.08)], 14)
                cut = np.maximum(cut, stroke_mask(W, H, T(sl, x0, y0, ang, 1, flip), wdg * 2.4, taper=(0.9, 0.0)))
            if r.random() < 0.45 and 0.25 < t < 0.8:
                hx, hy = L * (t + 0.035), sg * Wd * f(t) * 0.42
                cut = np.maximum(cut, shape_mask(W, H, T(ellipse_pts(hx, hy, L * 0.022, Wd * 0.07, 8, 0.0), x0, y0, ang, 1, flip)))
    m = np.clip(m - cut * 1.2, 0, 1)
    if depth:
        cols = tuple(mix(c, "#050906", depth) for c in cols)
    lay = gouache_paint(m, cols[0], cols[1], seed=nx(), rough=1.4, streak=0.5)
    if not detail:
        return lay, m
    # tonal modelling: shadow pools toward the stem and along the far side
    yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    ca_, sa_ = math.cos(ang), math.sin(ang)
    along = np.clip(((xx_ - x0) * ca_ + (yy_ - y0) * sa_) / L, 0, 1)
    across = ((-(xx_ - x0) * sa_ + (yy_ - y0) * ca_) / Wd) * (-1 if flip else 1)
    sh = np.clip((1 - along) * 0.9 + np.clip(across, 0, 1) * 0.6, 0, 1) * m
    dark = pigment(sh, mix(cols[0], "#000000", 0.65), seed=nx(), density=0.8, edge=0.35, bloom=0.45, rough=4, feather=2)
    lay = over(lay, dark)
    # lit half (light falls from the upper centre of the scene) — a translucent lighter glaze on one side of the midrib
    half = shape_mask(W, H, T(up + [(L, 0), (0, 0)], x0, y0, ang, 1, flip))
    lit = pigment(half * m, cols[2], cols[1], seed=nx(), density=0.55, edge=0.3, bloom=0.4, rough=3, feather=1.2)
    lit[..., 3] *= 0.7
    lay = over(lay, lit)
    # dry-brush highlights between the ribs, following the leaf's direction
    hl = np.zeros((H, W), np.float32)
    for a, b in ribs[::2]:
        o = (b[0] - a[0]) * 0.08
        pts = T([(a[0] + o + (b[0] - a[0]) * u, (a[1] + (b[1] - a[1]) * u) * 0.92 + L * 0.03) for u in np.linspace(0.15, 0.85, 8)], x0, y0, ang, 1, flip)
        hl = np.maximum(hl, stroke_mask(W, H, pts, max(2, L * 0.03), taper=(0.3, 0.5)))
    dry = np.clip((fbm(W, H, nx(), 5, 2) - 0.35) * 2.5, 0, 1)
    hlp = pigment(hl * m * dry, "#5d8a5e", "#7aa36f", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=2, feather=0.8)
    lay = over(lay, hlp)
    veins = np.zeros((H, W), np.float32)
    for a, b in ribs:
        pts = T(curve([a, ((a[0] + b[0]) / 2 + L * 0.02, (a[1] + b[1]) / 2 * 0.9), b], 16), x0, y0, ang, 1, flip)
        veins = np.maximum(veins, stroke_mask(W, H, pts, max(1.2, L * 0.008), taper=(0.1, 0.6)))
    mid = T(curve([(-L * 0.02, 0), (L * 0.4, -Wd * 0.03), (L * 0.97, 0)], 30), x0, y0, ang, 1, flip)
    midm = stroke_mask(W, H, mid, max(2.0, L * 0.018), taper=(0.05, 0.7))
    lay = over(lay, gouache_paint(veins * m, "#3d6b49", "#4b7a55", seed=nx(), rough=0.6, density=0.55))
    lay = over(lay, gouache_paint(midm, "#4f7b56", "#5f8a62", seed=nx(), rough=0.6, density=0.9))
    if gold:
        edge = np.clip(m - gaussian_filter(m, max(1.2, L * 0.008)) * 1.0, 0, 1) * 4
        broken = np.clip((fbm(W, H, nx(), max(8, L * 0.08), 2) - 0.32) * 3.2, 0, 1)
        lay = over(lay, foil(np.clip(edge * broken, 0, 1) * gold, GOLD, seed=nx(), emboss=0.4, sparkle=0.2))
        lay = over(lay, foil(midm * np.clip((fbm(W, H, nx(), 20, 2) - 0.45) * 3, 0, 1) * 0.8 * gold, GOLD, seed=nx(), emboss=0.3, sparkle=0.1))
    return lay, m


def palm_frond(W, H, x0, y0, ang, L, bend=0.25, cols=(G_DARK, G_MID), gold=0.6, n=22):
    ca, sa = math.cos(ang), math.sin(ang)
    spine_local = [(L * t, L * bend * t * t) for t in np.linspace(0, 1, 30)]
    spine = [(x0 + x * ca - y * sa, y0 + x * sa + y * ca) for x, y in spine_local]
    m = np.zeros((H, W), np.float32)
    for k in range(1, n):
        t = k / n
        i = int(t * 29)
        px, py = spine[i]
        qx, qy = spine[min(29, i + 1)]
        tang = math.atan2(qy - py, qx - px)
        ll = L * 0.36 * math.sin(math.pi * (0.15 + 0.85 * t)) ** 0.6 * (1.1 - 0.4 * t)
        for sg in (-1, 1):
            la = tang + sg * (0.9 - 0.35 * t) + rng.uniform(-0.06, 0.06)
            tip = (px + math.cos(la) * ll, py + math.sin(la) * ll + ll * 0.25)
            mid = (px + math.cos(la) * ll * 0.5, py + math.sin(la) * ll * 0.5 + ll * 0.04)
            m = np.maximum(m, stroke_mask(W, H, curve([(px, py), mid, tip], 12), max(3, L * 0.035), taper=(0.08, 0.85)))
    m = np.maximum(m, stroke_mask(W, H, spine, max(2, L * 0.012), taper=(0.02, 0.7)))
    lay = gouache_paint(m, cols[0], cols[1], seed=nx(), rough=1.0, streak=1.0)
    lay = over(lay, gouache_paint(stroke_mask(W, H, spine, max(1.5, L * 0.008), taper=(0.02, 0.7)), "#4f7b56", seed=nx(), rough=0.4))
    if gold:
        edge = np.clip(m - gaussian_filter(m, 1.2), 0, 1) * 4 * np.clip((fbm(W, H, nx(), 14, 2) - 0.4) * 3, 0, 1)
        lay = over(lay, foil(np.clip(edge, 0, 1) * gold, GOLD, seed=nx(), emboss=0.3, sparkle=0.15))
    return lay, m


def fern(W, H, x0, y0, ang, L, cols=("#1a3524", "#2a4f34"), gold=0.0, bend=0.3):
    ca, sa = math.cos(ang), math.sin(ang)
    sp = [(L * t, L * bend * t * t) for t in np.linspace(0, 1, 40)]
    spine = [(x0 + x * ca - y * sa, y0 + x * sa + y * ca) for x, y in sp]
    m = stroke_mask(W, H, spine, max(1.5, L * 0.01), taper=(0.02, 0.6))
    for k in range(2, 38, 2):
        px, py = spine[k]; qx, qy = spine[k + 1]
        tang = math.atan2(qy - py, qx - px)
        t = k / 40
        ll = L * 0.14 * (1 - t) ** 0.7 + L * 0.02
        for sg in (-1, 1):
            la = tang + sg * 1.15
            pts = petal_pts(px, py, ll, ll * 0.22, la, n=10)
            m = np.maximum(m, shape_mask(W, H, pts))
    lay = gouache_paint(m, cols[0], cols[1], seed=nx(), rough=0.8, streak=0.8)
    if gold:
        edge = np.clip(m - gaussian_filter(m, 1.0), 0, 1) * 4
        lay = over(lay, foil(np.clip(edge, 0, 1) * gold, GOLD, seed=nx(), emboss=0.3, sparkle=0.1))
    return lay, m


def shade_behind(layer, mask, blur=10, strength=0.55):
    """A soft dark shadow under leaves so overlapping layers separate."""
    return over(layer, soft_shadow(mask, "#030604", blur=blur, strength=strength, dx=4, dy=8))


# ---------------- night backdrop (opaque) ----------------
if want("night"):
    W, H = 780, 1400
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sky = painted_sky(W, H, [(0, "#0a140f"), (0.35, "#11241a"), (0.6, "#0e1c15"), (1.0, INK_BG)], seed=nx(), streak=0.9, grain=0.8)
    # moonlit mist glow in the upper middle
    glowm = np.exp(-(((xx - W * 0.52) / (W * 0.42)) ** 2 + ((yy - H * 0.3) / (H * 0.22)) ** 2))
    glowm *= 0.8 + 0.2 * fbm(W, H, nx(), 90, 3)
    sky[..., :3] = sky[..., :3] * (1 - glowm[..., None] * 0.45) + np.array(hex_rgb("#2c4836"), np.float32) * glowm[..., None] * 0.45
    # distant foliage silhouettes, two depths (soft, low contrast)
    far = blank(W, H)
    rr = random.Random(5)
    for (x, y, a, L) in [(60, 520, -1.9, 300), (720, 480, -1.2, 320), (180, 760, -1.4, 260), (640, 760, -1.8, 280), (380, 900, -1.55, 240), (40, 980, -1.2, 260), (760, 1000, -2.0, 260)]:
        lay, _ = monstera(W, H, x, y, a + rr.uniform(-0.2, 0.2), L, flip=rr.random() < 0.5, cols=("#0f2016", "#12261a", "#16301f"), gold=0.0, seed_rng=rr, detail=False)
        far = over(far, lay)
    for (x, y, a, L) in [(0, 300, -0.8, 380), (W, 320, math.pi + 0.8, 360), (90, 1100, -1.1, 300), (700, 1120, -2.0, 300)]:
        lay, _ = palm_frond(W, H, x, y, a, L, bend=0.35, cols=("#11261a", "#152e20"), gold=0.0, n=18)
        far = over(far, lay)
    far[..., 3] = gaussian_filter(far[..., 3], 3.0) * 0.6   # atmospheric softness
    out = over(sky, far)
    # mist band low down
    mist = np.clip((fbm(W, H, nx(), 160, 3) - 0.35) * 1.6, 0, 1) * np.exp(-((yy - H * 0.55) / (H * 0.16)) ** 2)
    out[..., :3] = out[..., :3] * (1 - mist[..., None] * 0.25) + np.array(hex_rgb("#4a6652"), np.float32) * mist[..., None] * 0.25
    out = vignette(add_grain(out, nx(), 0.035), strength=0.55)
    save_rgb(out, f"{OUT}/night.webp", quality=72)
    Image.fromarray((np.clip(out[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/mr-night.png")
    _art._fbm_cache.clear()

# ---------------- canopy (top frame) ----------------
if want("canopy"):
    W, H = 780, 640
    lay = blank(W, H)
    l1, m1 = palm_frond(W, H, -30, 40, 0.35, 420, bend=0.3, gold=0.7)
    lay = over(lay, l1)
    l2, m2 = palm_frond(W, H, W + 30, 70, math.pi - 0.4, 400, bend=-0.32, gold=0.7)
    lay = over(lay, l2)
    l3, m3 = fern(W, H, W - 140, -20, 1.9, 330, gold=0.6, bend=-0.2)
    lay = over(lay, l3)
    allm = np.maximum(np.maximum(m1, m2), m3)
    leaves = [(170, -30, 1.15, 200, False, 0.45), (W - 70, 30, math.pi - 0.7, 240, False, 0.3), (60, 40, 0.65, 250, True, 0.15), (-40, 210, -0.25, 300, False, 0.0), (W + 30, 230, math.pi + 0.15, 310, True, 0.0)]
    for (x, y, a, L, fl, dp) in leaves:
        l, m = monstera(W, H, x, y, a, L, flip=fl, depth=dp, gold=0.9 - dp)
        lay = over(lay, soft_shadow(m, "#020403", blur=9, strength=0.6, dx=5, dy=10))
        lay = over(lay, l)
        allm = np.maximum(allm, m)
    l4, m4 = fern(W, H, 40, -10, 1.25, 260, cols=("#1e3b28", "#2c5236"), gold=0.5, bend=0.25)
    lay = over(lay, l4)
    # keep the centre-bottom open: fade the frame towards the middle
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    keep = np.clip((np.abs(xx - W / 2) / (W * 0.5)) * 1.6 + (1 - yy / H) * 1.1 - 0.55, 0, 1)
    lay[..., 3] *= keep
    save_full(lay, f"{OUT}/canopy.webp", quality=76)
    preview(lay, "mr-canopy", bg=INK_BG)
    _art._fbm_cache.clear()

# ---------------- undergrowth (bottom corners) ----------------
if want("undergrowth"):
    W, H = 780, 460
    lay = blank(W, H)
    for (x, y, a, L, fl, g) in [(-60, H + 30, -0.75, 330, False, 0.6), (W + 60, H + 40, math.pi + 0.8, 340, True, 0.6), (40, H + 60, -1.35, 260, True, 0.5), (W - 30, H + 70, -1.85, 250, False, 0.5)]:
        l, m = monstera(W, H, x, y, a, L, flip=fl, cols=("#0f2316", "#183420", "#24492f"), gold=g)
        lay = over(lay, soft_shadow(m, "#020403", blur=9, strength=0.55, dx=-3, dy=-8))
        lay = over(lay, l)
    l, m = fern(W, H, 140, H + 10, -1.0, 280, cols=("#132a1b", "#21412b"), gold=0.45, bend=-0.25)
    lay = over(lay, l)
    l, m = fern(W, H, W - 130, H + 10, math.pi + 1.0, 270, cols=("#132a1b", "#21412b"), gold=0.45, bend=0.25)
    lay = over(lay, l)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    keep = np.clip((np.abs(xx - W / 2) / (W * 0.5)) * 1.9 + (yy / H) * 0.9 - 0.75, 0, 1)
    lay[..., 3] *= keep
    save_full(lay, f"{OUT}/undergrowth.webp", quality=76)
    preview(lay, "mr-under", bg=INK_BG)
    _art._fbm_cache.clear()

# ---------------- fireflies (tileable glow layer) ----------------
if want("fireflies"):
    W, H = 780, 1040
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    core = np.zeros((H, W), np.float32); halo = np.zeros((H, W), np.float32)
    rr = np.random.default_rng(11)
    for _ in range(26):
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        r0 = rr.uniform(1.6, 3.6); hr = rr.uniform(9, 22); k = rr.uniform(0.45, 1.0)
        for ox in (-W, 0, W):
            for oy in (-H, 0, H):
                d2 = (xx - x - ox) ** 2 + (yy - y - oy) ** 2
                core = np.maximum(core, np.exp(-d2 / (2 * r0 * r0)) * k)
                halo = np.maximum(halo, np.exp(-d2 / (2 * hr * hr)) * k)
    # painted, not lens-flare: halos get a slightly mottled watercolour edge
    halo *= 0.75 + 0.25 * wrap_noise(W, H, 4, 6)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f2c45e"), np.float32)
    rgb = rgb * (1 - core[..., None]) + np.array(hex_rgb("#fff1c2"), np.float32) * core[..., None]
    a = np.clip(core * 1.0 + halo * 0.38, 0, 1)
    ff = np.concatenate([rgb, a[..., None]], -1)
    save_full(ff, f"{OUT}/fireflies.webp", quality=72)
    preview(ff, "mr-fireflies", bg=INK_BG)

# ---------------- frond (section corner) ----------------
if want("frond"):
    W, H = 320, 320
    lay = blank(W, H)
    l, m = monstera(W, H, 46, 52, 0.78, 236, flip=False)
    lay = over(lay, soft_shadow(m, "#020403", blur=6, strength=0.5, dx=3, dy=6))
    lay = over(lay, l)
    save(lay, f"{OUT}/frond.webp", max_w=300, quality=80)
    preview(lay, "mr-frond", bg=INK_BG)

# ---------------- tiny gold leaf pair for the divider ----------------
if want("leaf"):
    W, H = 64, 30
    m = np.zeros((H, W), np.float32)
    for sg in (-1, 1):
        m = np.maximum(m, shape_mask(W, H, petal_pts(W / 2 + sg * 2, 17, 26, 7.5, (math.pi if sg < 0 else 0) + sg * -0.28, n=14, cup=0.2)))
    vein = np.zeros((H, W), np.float32)
    for sg in (-1, 1):
        vein = np.maximum(vein, stroke_mask(W, H, [(W / 2 + sg * (3 + 10 * u), 17 - sg * sg * 3.2 * u) for u in np.linspace(0, 1, 6)], 1.1, taper=(0.1, 0.6)))
    lf = foil(m, GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    lf[..., :3] *= (1 - vein[..., None] * 0.45)
    save_full(lf, f"{OUT}/leaf.webp", quality=84)
    preview(lf, "mr-leaf", bg=INK_BG)

print("total KB:", sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1024)
