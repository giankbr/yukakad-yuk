"""Muqarnas Putih — white stucco muqarnas vault seen from directly below: tiers of pointed niche cells (32 per ring,
each tier rotated half a cell so its niches sit on the spandrels of the tier below, the classic corbelled stalactite
logic), folded spandrel facets with a central arris, fillet ledges between tiers, and an eight-pointed oculus admitting
soft pale-gold light. Rendered analytically in polar coordinates (exact geometry) and finished as hand-trowelled
plaster: wobble, mottling, grain, warm bounce light from the centre. Also a cornice frieze (one tier unrolled), a
single niche hood for portraits, a stucco star and a divider.
Run: python3 -I muqarnas-putih.py [part ...]  parts: vault frieze niche star divider
Assets -> public/themes/art/muqarnas-putih/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i2_lib import *  # noqa

OUT = outdir("muqarnas-putih")
PARTS = sys.argv[1:] or ["vault", "frieze", "niche", "star", "divider"]

# plaster palette: ivory light, warm grey shadow, pale gold bounce
LIT = carr("#fbf8f1")
MID = carr("#efe8da")
SHD = carr("#d8cbb2")
DEEP = carr("#b8a483")
GOLDL = carr("#f3dfa6")
GOLD = carr("#d9b871")


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def niche_field(t, u, p=1.75):
    """t: 0 at tier base (outer) .. 1 at apex (inner); u: -0.5..0.5 across one cell.
    Returns (inside 0..1 soft, s lateral -1..1, edge distance in cell units)."""
    half = 0.5 * (1 - np.clip(t, 0, 1) ** p)
    d = half - np.abs(u)
    s = u / np.maximum(half, 1e-4)
    return d, np.clip(s, -1, 1), half


def tri(x):
    """Triangle wave in [-1, 1], period 2*pi."""
    return 2 / math.pi * np.arcsin(np.sin(x))


def cell_shade(t, u, cellpx, kind, glob, p=1.75):
    """Luminance + gold + inside for one tier given local coords. kind: niche | lozenge."""
    t = np.clip(t, 0, 1)
    if kind == "lozenge":
        half = 0.5 * (1 - np.abs(2 * t - 1) ** 1.05)
    else:
        half = 0.5 * (1 - t ** p)
    d = half - np.abs(u)
    s = np.clip(u / np.maximum(half, 1e-4), -1, 1)
    dpx = d * cellpx
    inside = smooth(-0.9, 0.9, dpx)
    if kind == "lozenge":
        # flat facets: the upper (inner) facet catches the light, the lower one turns away; lateral fold
        upper = t > 0.5
        n_l = np.where(upper, 0.95, 0.74) + np.where(u > 0, -0.06, 0.04) * (0.6 + 0.4 * glob)
        depth = (1 - s ** 2) * 0.2
    else:
        depth = (1 - s ** 2) * (1 - t) ** 0.8
        n_l = 0.84 + 0.18 * t - 0.36 * depth - s * (0.12 + 0.06 * glob)
    n_l = n_l + np.exp(-((dpx + 0.6) / 1.3) ** 2) * 0.24 - np.exp(-((dpx - 3.2) / 2.2) ** 2) * 0.09
    q = 0.5 - np.abs(u)
    su = np.where(u > 0, 1.0, -1.0)
    fold = np.exp(-((q * cellpx) / 1.2) ** 2) * 0.16
    if kind == "lozenge":
        # triangles above and below the diamonds: upper ones lit, lower ones shaded
        sp_l = np.where(t > 0.5, 0.9, 0.8) + su * 0.05 + fold * 0.6
    else:
        sp_l = 0.88 + 0.08 * t + su * 0.08 * (0.6 + glob * 0.4) + fold * (t < 0.62)
    val = inside * n_l + (1 - inside) * sp_l
    return val, inside * depth * 0.55, inside


def shade_cells(r, th, R, bounds, tiers, seed, lightdir=-1.9, star_n=8):
    """bounds: [(radius, amp, phase)] tier boundaries (star-modulated, 8-fold); tiers: [(n, offset, kind)] between them.
    Returns (lum, gold, inner_mask) where inner_mask is the area inside the last boundary (the oculus)."""
    H, W = r.shape
    lum = np.zeros((H, W), np.float32)
    gold = np.zeros((H, W), np.float32)
    B = [R * rr * (1 + a * tri(star_n * (th + math.pi / 2) + math.pi / 2 + ph)) for rr, a, ph in bounds]
    glob = 0.5 + 0.5 * np.cos(th - lightdir)
    for k, (n, off, kind) in enumerate(tiers):
        bo, bi = B[k], B[k + 1]
        band = (r <= bo) & (r > bi)
        t = (bo - r) / np.maximum(bo - bi, 1e-3)
        cw = math.tau / n
        ph = (th - off) / cw
        u = (ph % 1.0) - 0.5
        cid = np.floor(ph) + k * 97
        jit = ((np.sin(cid * 12.9898 + seed) * 43758.5453) % 1.0 - 0.5) * 0.05
        val, g, ins = cell_shade(t, u, cw * r, kind, glob)
        lpx = bo - r
        ledge = np.exp(-((lpx - 2.4) / 1.7) ** 2) * 0.17 - np.exp(-((lpx + 0.3) / 1.0) ** 2) * 0.15
        val = val + ledge + jit
        lum = np.where(band, val, lum)
        gold = np.where(band, g, gold)
    return lum, gold, (r <= B[-1]).astype(np.float32), B


def plaster(lum, gold, seed, light_c=None):
    """Map luminance (0..1.2) to plaster colours with mottling and grain; returns RGB."""
    H, W = lum.shape
    mot = (fbm(W, H, seed, 90, 3) - 0.5) * 0.06
    fine = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.8)
    fine = (fine - fine.mean()) / (fine.std() + 1e-6) * 0.018
    trowel = gaussian_filter(np.random.default_rng(seed + 1).random((H, W)).astype(np.float32), (2.0, 9.0))
    trowel = (trowel - trowel.mean()) / (trowel.std() + 1e-6) * 0.012
    L = np.clip(lum + mot + fine + trowel, 0, 1.25)
    # piecewise palette ramp: DEEP -> SHD -> MID -> LIT
    stops = [(0.35, DEEP), (0.62, SHD), (0.84, MID), (1.0, LIT)]
    rgb = np.zeros((H, W, 3), np.float32)
    rgb[:] = DEEP
    for (a, ca), (b, cb) in zip(stops[:-1], stops[1:]):
        k = np.clip((L - a) / (b - a), 0, 1)[..., None]
        sel = (L > a)[..., None]
        rgb = np.where(sel, ca * (1 - k) + cb * k, rgb)
    rgb = np.where((L > 1.0)[..., None], LIT + (L[..., None] - 1.0) * 0.4, rgb)
    g = np.clip(gold, 0, 1)[..., None]
    rgb = rgb * (1 - g * 0.35) + GOLD * g * 0.35
    return np.clip(rgb, 0, 1)


def star_poly(cx, cy, ro, ri, n=8, rot=0.0):
    pts = []
    for i in range(n * 2):
        a = rot + i * math.pi / n
        r = ro if i % 2 == 0 else ri
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def vault():
    S = 1500
    W = H = S
    cx = cy = S / 2
    R = S * 0.49
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # hand wobble: displace the lookup slightly so cells are trowelled, not machined
    wx = (fbm(W, H, 11, 60, 3) - 0.5) * 3.2
    wy = (fbm(W, H, 12, 60, 3) - 0.5) * 3.2
    X = xx - cx + wx; Y = yy - cy + wy
    r = np.hypot(X, Y); th = np.arctan2(Y, X)
    P = math.pi
    bounds = [(1.0, 0.0, 0), (0.865, 0.012, 0), (0.745, 0.025, 0), (0.64, 0.04, 0), (0.545, 0.06, 0), (0.46, 0.08, 0),
              (0.385, 0.10, 0), (0.315, 0.13, 0), (0.25, 0.18, 0)]
    kinds = [(32, "niche"), (32, "lozenge"), (32, "niche"), (16, "niche"), (16, "lozenge"), (16, "niche"), (8, "niche"), (8, "niche")]
    # offsets from the oculus outward: the innermost cells straddle the star troughs; each outer tier is rotated
    # half of its own cell against the tier it carries
    offs = [0.0] * len(kinds)
    o = -P / 2
    for k in range(len(kinds) - 1, -1, -1):
        n = kinds[k][0]
        if k < len(kinds) - 1:
            o = o - 0.5 * math.tau / n
        offs[k] = o
    tiers = [(n, offs[k], kind) for k, (n, kind) in enumerate(kinds)]
    lum, gold, centre, B = shade_cells(r, th, R, bounds, tiers, 5)
    # oculus: the innermost (star-shaped) boundary is open to the light
    starm = gaussian_filter(centre, 0.9)
    rr = R * bounds[-1][0]
    lum = np.where(centre > 0.5, 1.0, lum)
    # light spilling from the oculus onto the innermost tiers
    spill = np.clip(gaussian_filter(centre, 40) * 1.6, 0, 1) * (1 - centre)
    lum = lum + spill * 0.12
    # outer drum ring (moulded band just outside the vault)
    band = (r > R) & (r <= R * 1.045)
    bt = (r - R) / (R * 0.045)
    lum = np.where(band, 0.88 + 0.12 * np.sin(bt * math.pi) - 0.1 * (bt > 0.82), lum)
    rgb = plaster(lum, gold, 21)
    # light from the oculus: pale gold glow falling outward, strongest at the star
    glow_f = np.clip(1 - r / (R * 0.75), 0, 1) ** 2.2
    rgb = rgb * (1 - glow_f[..., None] * 0.12) + GOLDL * glow_f[..., None] * 0.12
    lightm = starm
    lc = np.clip(1.0 - (r / rr) * 0.25, 0, 1)
    lightc = carr("#fffaf0") * lc[..., None] + GOLDL * (1 - lc[..., None])
    rgb = rgb * (1 - lightm[..., None]) + lightc * lightm[..., None]
    halo = np.clip(gaussian_filter(starm, 14) * 1.3, 0, 1) * (1 - starm)
    rgb = rgb * (1 - halo[..., None] * 0.25) + carr("#fff3cf") * halo[..., None] * 0.25
    # vignette toward the outer ring (the vault rim is darker, light falls off)
    vig = np.clip((r / R - 0.55) / 0.45, 0, 1) ** 1.6
    rgb = rgb * (1 - vig[..., None] * 0.08)
    alpha = smooth(R * 1.045 + 1.5, R * 1.045 - 1.5, r)
    arr = np.concatenate([rgb, alpha[..., None]], -1).astype(np.float32)
    preview(arr, "vault", bg="#f3ede2")
    print("vault", save(arr, f"{OUT}/vault.webp", max_w=760, quality=80))
    clear()


def frieze():
    """A cornice: three tiers of muqarnas unrolled into a straight band (cells hang down like stalactites).
    Tileable horizontally: 6 cells across."""
    W, H = 780, 150
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wx = (fbm(W, H, 31, 40, 3) - 0.5) * 2.0
    lum = np.full((H, W), 0.0, np.float32)
    gold = np.zeros((H, W), np.float32)
    alpha = np.zeros((H, W), np.float32)
    rows = [(0, 46, 6, 0.0), (46, 92, 6, 0.5), (92, 132, 12, 0.25)]  # (y_top, y_bot, cells, offset fraction)
    # straight version of the niche field: t = 0 at the TOP (where the tier springs), 1 at the hanging tip
    for k, (y0, y1, n, off) in enumerate(rows):
        bandm = (yy >= y0) & (yy < y1)
        t = (yy - y0) / (y1 - y0)
        cw = W / n
        ph = ((xx + wx) / cw - off) % 1.0
        u = ph - 0.5
        d, s, half = niche_field(t, u, p=1.6)
        dpx = d * cw
        inside = smooth(-0.9, 0.9, dpx)
        depth = (1 - s ** 2) * (1 - t) ** 0.8
        n_l = 0.84 + 0.16 * t - 0.40 * depth - s * 0.12 + np.exp(-((dpx + 0.6) / 1.2) ** 2) * 0.2 - np.exp(-((dpx - 3) / 2) ** 2) * 0.08
        q = 0.5 - np.abs(u)
        su = np.where(u > 0, 1.0, -1.0)
        sp_l = 0.9 + 0.06 * t + su * 0.07 + np.exp(-((q * cw) / 1.1) ** 2) * 0.14 * (t < 0.6)
        lp = yy - y0
        ledge = np.exp(-((lp - 2.0) / 1.5) ** 2) * 0.16 - np.exp(-((lp + 0.2) / 0.9) ** 2) * 0.12
        val = inside * n_l + (1 - inside) * sp_l + ledge
        lum = np.where(bandm, val, lum)
        gold = np.where(bandm, inside * depth * 0.5, gold)
        # the last row hangs free: only the niche hoods + their pointed tips are solid; spandrel gaps open
        if k == len(rows) - 1:
            alpha = np.where(bandm, np.clip(inside * 1.0, 0, 1), alpha)
        else:
            alpha = np.where(bandm, 1.0, alpha)
    # top moulding
    top = yy < 10
    lum = np.where(top, 0.95 - 0.08 * (yy / 10), lum)
    rgb = plaster(lum, gold, 33)
    arr = np.concatenate([rgb, alpha[..., None]], -1).astype(np.float32)
    # soft drop shadow under the hanging tips
    sh = np.roll(gaussian_filter(alpha, 3), 4, 0) * (1 - alpha)
    arr = over(np.concatenate([np.ones((H, W, 3), np.float32) * carr("#9c8b70"), (sh * 0.25)[..., None]], -1), arr)
    preview(arr, "frieze", bg="#f6f1e7")
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA").resize((390 * 2 // 2 * 1, 75), Image.LANCZOS) \
        .save(f"{OUT}/frieze.webp", "WEBP", quality=82, method=6)
    print("frieze", (390, 75))
    clear()


def niche():
    """A single pointed niche hood (mihrab-like head) filled with fanning muqarnas cells, front view: portrait top and
    closing emblem."""
    W, H = 600, 560
    cx, spring = W / 2, 372
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    Rr = 372.0
    lc_, rc_ = cx + (Rr - W * 0.5) - 6, cx - (Rr - W * 0.5) + 6
    inA = ((np.hypot(xx - lc_, yy - spring) <= Rr - 6) & (np.hypot(xx - rc_, yy - spring) <= Rr - 6) & (yy <= H)).astype(np.float32)
    inA = gaussian_filter(inA, 0.7)
    X = xx - cx + (fbm(W, H, 41, 40, 3) - 0.5) * 2
    Y = yy - spring + (fbm(W, H, 42, 40, 3) - 0.5) * 2
    r = np.hypot(X, Y); th = np.arctan2(Y, X)
    Rv = 380.0
    radii = [1.0, 0.78, 0.6, 0.46, 0.34]
    bounds = [(rr_, 0.0, 0) for rr_ in radii]
    kinds = [(28, "niche"), (28, "lozenge"), (14, "niche"), (14, "niche")]
    offs = []
    o = -math.pi / 2
    for n, _ in kinds:
        offs.append(o); o += 0.5 * math.tau / n
    lum, gold, cen, _B = shade_cells(r, th, Rv, bounds, [(n, offs[k], kd) for k, (n, kd) in enumerate(kinds)], 7, lightdir=-math.pi / 2)
    lum = np.where(cen > 0.5, 0.97 - 0.04 * (r / (Rv * 0.34)), lum)
    jamb = yy > spring
    lum = np.where(jamb, 0.9 - 0.06 * np.abs((xx - cx) / (W / 2)), lum)
    # moulded arch edge
    din = gaussian_filter(inA, 4)
    lum = lum + np.exp(-((din - 0.6) / 0.12) ** 2) * inA * 0.12 - np.exp(-((din - 0.9) / 0.05) ** 2) * inA * 0.05
    rgb = plaster(lum, gold, 43)
    alpha = inA * np.clip((spring + 150 - yy) / 150, 0, 1)
    arr = np.concatenate([rgb, alpha[..., None]], -1).astype(np.float32)
    preview(arr, "niche", bg="#f3ede2")
    print("niche", save(arr, f"{OUT}/niche.webp", max_w=300, quality=82))
    clear()


def bevel_lum(mask, depth=9.0, lx=-0.6, ly=-0.8):
    from scipy.ndimage import distance_transform_edt
    dist = distance_transform_edt(mask > 0.5).astype(np.float32)
    hgt = gaussian_filter(np.minimum(dist, depth), 1.2)
    gy, gx = np.gradient(hgt)
    return np.clip(-(gx * lx + gy * ly), -1, 1)


def star():
    """Moulded stucco eight-pointed star with a bevelled edge and a gold-leaf inner star: nodes, amp, sent."""
    W = H = 320
    cx = cy = W / 2
    a = shapes(W, H, [star_poly(cx, cy, 148, 108, 8, -math.pi / 2)], smooth=False)
    a = gaussian_filter(a, 0.6)
    sh = bevel_lum(a, 12)
    inner = shapes(W, H, [star_poly(cx, cy, 92, 66, 8, -math.pi / 2 + math.pi / 8)], smooth=False)
    sh2 = bevel_lum(inner, 7)
    lum = 0.93 + sh * 0.3 - sh2 * 0.22
    rgb = plaster(lum, np.zeros_like(a), 51)
    arr = np.concatenate([rgb, a[..., None]], -1).astype(np.float32)
    g = shapes(W, H, [star_poly(cx, cy, 40, 29, 8, -math.pi / 2)], smooth=False)
    arr = FO(arr, g, "#d4b066", seed=53, emboss=0.8, sparkle=0.08)
    preview(arr, "star", bg="#f3ede2")
    print("star", save(arr, f"{OUT}/star.webp", max_w=120, quality=84))
    clear()


def divider():
    """A slim run of five hanging muqarnas cells (one tier) with a gold bead at the centre."""
    W, H = 640, 90
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = 9
    cw = W / n
    y0, y1 = 14, 70
    t = (yy - y0) / (y1 - y0)
    u = ((xx / cw) % 1.0) - 0.5
    d, s, half = niche_field(t, u, p=1.6)
    dpx = d * cw
    inside = smooth(-0.8, 0.8, dpx) * ((yy >= y0) & (yy < y1))
    depth = (1 - s ** 2) * (1 - np.clip(t, 0, 1)) ** 0.8
    lum = 0.85 + 0.15 * t - 0.42 * depth - s * 0.12 + np.exp(-((dpx + 0.6) / 1.2) ** 2) * 0.2
    top = (yy >= 6) & (yy < 14)
    lum = np.where(top, 0.95 - 0.1 * ((yy - 6) / 8), lum)
    alpha = np.clip(inside + top, 0, 1)
    # taper the run toward both ends
    fade = np.clip(1 - np.abs(xx - W / 2) / (W / 2), 0, 1) ** 0.35
    alpha = alpha * np.clip(fade * 1.6, 0, 1)
    rgb = plaster(lum, inside * depth * 0.5, 61)
    arr = np.concatenate([rgb, alpha[..., None]], -1).astype(np.float32)
    bead = shapes(W, H, [star_poly(W / 2, 80, 9, 6.5, 8, -math.pi / 2)], smooth=False)
    arr = FO(arr, bead, "#d4b066", seed=63, emboss=0.8, sparkle=0.1)
    preview(arr, "divider", bg="#f6f1e7")
    print("divider", save(arr, f"{OUT}/divider.webp", max_w=320, quality=84))
    clear()


for p in PARTS:
    globals()[p]()
kb_report(OUT)
