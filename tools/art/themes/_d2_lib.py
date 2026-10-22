"""Agent D2 helpers (cirebon-kasepuhan, belitung-granit, khatam-kayu, masjid-terapung): builds on _c3_lib (which brings
_b2_lib/_j1_lib/_p1_lib: bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, rect/poly/flat, bricks, wood,
light_mask, plaster, wet_sky, emboss_l) and adds glazed porcelain plates, rounded rock masses, water reflection with
ripples, and khatam micro-mosaic tiles. Previews -> /tmp/pen/nb-D2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib, _j1_lib, _b2_lib, _c3_lib
from _c3_lib import *  # noqa
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-D2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _b2_lib.PREV = _c3_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def ring_m(W, H, cx, cy, r0, r1):
    return np.clip(circles(W, H, [(cx, cy, r1)]) - circles(W, H, [(cx, cy, r0)]), 0, 1)


def glaze_gloss(W, H, cx, cy, r, seed=1, strength=0.55):
    """Soft window-reflection highlight on a glazed round surface (upper left)."""
    m = ellipses(W, H, [(cx - r * 0.38, cy - r * 0.42, r * 0.22, r * 0.09, -38)])
    m = gaussian_filter(m, r * 0.04 + 1)
    m2 = ellipses(W, H, [(cx + r * 0.45, cy + r * 0.5, r * 0.12, r * 0.04, -38)])
    m2 = gaussian_filter(m2, r * 0.03 + 1)
    return flat(np.clip(m + m2 * 0.6, 0, 1), "#ffffff", strength)


def brush_dabs(W, H, items):
    """items: (x, y, length, width, angle) -> mask of tapered comma strokes (porcelain brushwork)."""
    out = []
    for x, y, L, wd, a in items:
        out.append(([(x + math.cos(a) * L * t, y + math.sin(a) * L * t + math.sin(t * math.pi) * wd * 0.3) for t in np.linspace(0, 1, 8)], wd, (0.1, 0.7)))
    return strokes(W, H, out)


def flower_m(W, H, cx, cy, r, n=6, rot=0.0, cup=0.2):
    return shapes(W, H, [petal_pts(cx, cy, r, r * 0.55, rot + k * math.tau / n, n=12, cup=cup) for k in range(n)])


def plate(art, W, H, cx, cy, r, style, nx, rng):
    """A glazed porcelain plate seen face-on. style: 'blue' (Chinese blue-and-white), 'poly' (polychrome famille
    enamels), 'delf' (European blue rim with geometric border)."""
    body = circles(W, H, [(cx, cy, r)])
    white = "#f7f4ec" if style != "poly" else "#f6f1e2"
    art = GP(art, body, white, "#e9e4d8", seed=nx(), rough=0.6, streak=0.3)
    # body shadow toward lower right (dish curvature)
    sh = body * np.clip(1 - light_mask(H, W, cx - r * 0.3, cy - r * 0.35, r * 1.9) * 1.4, 0, 1)
    art = over(art, flat(sh, "#8f8a80", 0.22))
    well = ring_m(W, H, cx, cy, r * 0.6, r * 0.635)
    art = over(art, flat(gaussian_filter(well, 1.2), "#a9a396", 0.35))
    BL, BL2 = "#23439a", "#3a63b8"
    if style in ("blue", "delf"):
        # rim band + lines
        art = G(art, ring_m(W, H, cx, cy, r * 0.95, r * 0.985), BL, BL2, seed=nx(), density=0.9, edge=0.4, rough=1.0, feather=0.6, pad=8)
        art = G(art, ring_m(W, H, cx, cy, r * 0.64, r * 0.665), BL, seed=nx(), density=0.75, edge=0.3, rough=0.8, feather=0.6, pad=8)
        if style == "blue":
            # rim: alternating flower heads and cloud-scroll commas, painted in two tones of cobalt
            # kraak-style rim: alternating washed panels separated by double radial lines
            n = 10
            pan = []
            for k in range(0, n, 2):
                a0, a1 = (k + 0.5) * math.tau / n, (k + 1.5) * math.tau / n
                pan.append([(cx + math.cos(a) * r * 0.67, cy + math.sin(a) * r * 0.67) for a in np.linspace(a0, a1, 12)] +
                           [(cx + math.cos(a) * r * 0.94, cy + math.sin(a) * r * 0.94) for a in np.linspace(a1, a0, 12)])
            art = G(art, shapes(W, H, pan, smooth=False), "#5b80c8", "#7f9fd6", seed=nx(), density=0.38, edge=0.7, bloom=0.5, rough=1.0, feather=0.7, pad=8)
            rad = []
            for k in range(n):
                a = (k + 0.5) * math.tau / n
                for o in (-0.018, 0.018):
                    rad.append(([(cx + math.cos(a + o) * r * 0.67, cy + math.sin(a + o) * r * 0.67), (cx + math.cos(a + o) * r * 0.94, cy + math.sin(a + o) * r * 0.94)], r * 0.012, None))
            art = G(art, strokes(W, H, rad), BL, seed=nx(), density=0.8, edge=0.2, rough=0.4, feather=0.4, pad=6)
            dabs, heads = [], []
            for k in range(n):
                a = k * math.tau / n + rng.uniform(-0.03, 0.03)
                rr = r * 0.8
                hx, hy = cx + math.cos(a) * rr, cy + math.sin(a) * rr
                heads.append((hx, hy, r * 0.1))
                for s in (-1, 1):
                    b = a + s * math.pi / n * 0.95
                    lx, ly = cx + math.cos(b) * rr, cy + math.sin(b) * rr
                    dabs.append((lx - math.cos(b + s * 1.4) * r * 0.06, ly - math.sin(b + s * 1.4) * r * 0.06, r * 0.13, r * 0.035, b + s * 1.6))
            art = G(art, brush_dabs(W, H, dabs), BL2, seed=nx(), density=0.6, edge=0.6, rough=0.8, feather=0.6, pad=8)
            fh = np.maximum.reduce([flower_m(W, H, x, y, rr, 6, rng.uniform(0, 1), 0.35) for x, y, rr in heads])
            art = G(art, fh, BL, BL2, seed=nx(), density=0.8, edge=0.7, rough=0.8, feather=0.6, pad=8)
            art = over(art, flat(circles(W, H, [(x, y, rr * 0.28) for x, y, rr in heads]), "#f7f4ec", 0.9))
            # centre: lotus pond medallion (flower, leaves, curling stems), wash + darker outline strokes
            leaves = []
            for k in range(8):
                a = k * math.tau / 8 + 0.39
                leaves.append(petal_pts(cx, cy, r * 0.46, r * 0.17, a, n=14, cup=0.25))
            lm = shapes(W, H, leaves)
            art = G(art, lm, BL2, "#5b80c8", seed=nx(), density=0.45, edge=0.8, bloom=0.4, rough=1.2, feather=0.8, pad=8)
            veins = [([(cx + math.cos(a) * r * 0.2, cy + math.sin(a) * r * 0.2), (cx + math.cos(a) * r * 0.4, cy + math.sin(a) * r * 0.4)], r * 0.012, None) for a in [k * math.tau / 8 + 0.39 for k in range(8)]]
            art = G(art, strokes(W, H, veins), BL, seed=nx(), density=0.8, edge=0.2, rough=0.5, feather=0.4, pad=6)
            stems = []
            for k in range(8):
                a = k * math.tau / 8
                pts = [(cx + math.cos(a + t * 0.5) * r * (0.47 + 0.08 * math.sin(t * 3)), cy + math.sin(a + t * 0.5) * r * (0.47 + 0.08 * math.sin(t * 3))) for t in np.linspace(0, 1, 10)]
                stems.append((pts, r * 0.016, (0.1, 0.6)))
            art = G(art, strokes(W, H, stems), BL, seed=nx(), density=0.7, edge=0.3, rough=0.5, feather=0.4, pad=6)
            fl = flower_m(W, H, cx, cy, r * 0.2, 8, 0.2)
            art = G(art, fl, BL, BL2, seed=nx(), density=0.85, edge=0.8, rough=0.8, feather=0.6, pad=8)
            fl2 = flower_m(W, H, cx, cy, r * 0.11, 8, 0.6)
            art = G(art, fl2, "#16306f", seed=nx(), density=0.6, edge=0.6, rough=0.5, feather=0.5, pad=8)
            art = over(art, flat(circles(W, H, [(cx, cy, r * 0.035)]), "#f7f4ec", 0.9))
        else:
            # European blue: scalloped lambrequin border + a central compass star of lozenges
            lam = []
            n = 16
            for k in range(n):
                a = k * math.tau / n
                pts = []
                for t in np.linspace(-1, 1, 9):
                    b = a + t * math.pi / n
                    rr = r * (0.95 - 0.16 * (1 - t * t))
                    pts.append((cx + math.cos(b) * rr, cy + math.sin(b) * rr))
                pts += [(cx + math.cos(a + math.pi / n) * r * 0.95, cy + math.sin(a + math.pi / n) * r * 0.95), (cx + math.cos(a - math.pi / n) * r * 0.95, cy + math.sin(a - math.pi / n) * r * 0.95)]
                lam.append(pts)
            art = G(art, shapes(W, H, lam), BL2, "#5577c0", seed=nx(), density=0.7, edge=0.7, rough=0.8, feather=0.6, pad=8)
            dots = circles(W, H, [(cx + math.cos(k * math.tau / n) * r * 0.73, cy + math.sin(k * math.tau / n) * r * 0.73, r * 0.025) for k in range(n)])
            art = G(art, dots, BL, seed=nx(), density=0.9, rough=0.4, feather=0.4, pad=6)
            loz = []
            for k in range(8):
                a = k * math.tau / 8
                L = r * (0.5 if k % 2 == 0 else 0.34)
                loz.append([(cx, cy), (cx + math.cos(a - 0.18) * L * 0.5, cy + math.sin(a - 0.18) * L * 0.5), (cx + math.cos(a) * L, cy + math.sin(a) * L), (cx + math.cos(a + 0.18) * L * 0.5, cy + math.sin(a + 0.18) * L * 0.5)])
            art = G(art, shapes(W, H, loz, smooth=False), BL, BL2, seed=nx(), density=0.8, edge=0.7, rough=0.7, feather=0.6, pad=8)
            art = G(art, ring_m(W, H, cx, cy, r * 0.12, r * 0.16), BL, seed=nx(), density=0.8, rough=0.5, feather=0.5, pad=6)
    else:
        # polychrome enamels: green leaf scrolls, rose and yellow blossoms, iron-red rim, blue inner line
        art = G(art, ring_m(W, H, cx, cy, r * 0.93, r * 0.99), "#b2452f", "#c9603e", seed=nx(), density=0.85, edge=0.4, rough=1.0, feather=0.6, pad=8)
        art = G(art, ring_m(W, H, cx, cy, r * 0.64, r * 0.665), BL2, seed=nx(), density=0.7, rough=0.7, feather=0.5, pad=8)
        # rim: lattice of green diamonds with tiny pink dots
        n = 14
        dia = []
        for k in range(n):
            a = k * math.tau / n
            rr = r * 0.8
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            s = r * 0.1
            dia.append([(x + math.cos(a) * s, y + math.sin(a) * s), (x + math.cos(a + 1.57) * s * 0.6, y + math.sin(a + 1.57) * s * 0.6), (x - math.cos(a) * s, y - math.sin(a) * s), (x - math.cos(a + 1.57) * s * 0.6, y - math.sin(a + 1.57) * s * 0.6)])
        art = G(art, shapes(W, H, dia, smooth=False), "#3f8a5e", "#5aa271", seed=nx(), density=0.75, edge=0.6, rough=0.8, feather=0.6, pad=8)
        art = G(art, circles(W, H, [(cx + math.cos((k + .5) * math.tau / n) * r * 0.8, cy + math.sin((k + .5) * math.tau / n) * r * 0.8, r * 0.04) for k in range(n)]), "#d9627a", seed=nx(), density=0.85, rough=0.5, feather=0.5, pad=6)
        # centre: peony spray
        lv = []
        for a in [-2.7, -1.9, -0.4, 0.5, 1.6, 2.5]:
            lv.append(petal_pts(cx + math.cos(a) * r * 0.16, cy + math.sin(a) * r * 0.16, r * 0.26, r * 0.11, a, n=12, cup=0.3))
        art = G(art, shapes(W, H, lv), "#3f8a5e", "#7fae5a", seed=nx(), density=0.75, edge=0.7, bloom=0.3, rough=1.0, feather=0.7, pad=8)
        for (fx, fy, fr, c1, c2) in [(cx - r * 0.08, cy - r * 0.05, r * 0.2, "#d9627a", "#f19aa8"), (cx + r * 0.27, cy + r * 0.2, r * 0.11, "#e8b33c", "#f3d27a"), (cx - r * 0.3, cy + r * 0.24, r * 0.09, "#6a7fc8", "#9aaee0")]:
            art = G(art, flower_m(W, H, fx, fy, fr, 7, rng.uniform(0, 1), 0.3), c1, c2, seed=nx(), density=0.8, edge=0.8, bloom=0.3, rough=0.8, feather=0.6, pad=8)
            art = G(art, flower_m(W, H, fx, fy, fr * 0.5, 5, rng.uniform(0, 1)), c1, seed=nx(), density=0.6, edge=0.7, rough=0.5, feather=0.5, pad=6)
            art = over(art, flat(circles(W, H, [(fx, fy, fr * 0.16)]), "#e8b33c", 0.9))
    # crackle + glaze gloss
    cr = hatch(W, H, 0.7, r * 0.18, 0.03, nx(), 8.0) * body
    art = over(art, flat(cr, "#7c7668", 0.08))
    art = over(art, glaze_gloss(W, H, cx, cy, r, nx(), 0.6))
    rim_shadow = ring_m(W, H, cx, cy, r * 0.97, r * 1.0)
    art = over(art, flat(gaussian_filter(rim_shadow, 0.8), "#5c564c", 0.35))
    return art


def rock_mass(W, H, blobs, seed):
    """Union of rounded boulder blobs [(cx, cy, rx, ry, rot)] with a slightly lumpy outline."""
    m = ellipses(W, H, blobs)
    return displace(m, seed, 4.0, 60)


def reflect(scene, horizon, seed=1, amp=6.0, wl=7.0, fade=0.75, tint="#000000", tint_a=0.0, blur=1.2):
    """Mirror everything above `horizon` into the water below it, broken by horizontal ripple displacement.
    Returns an RGBA layer covering the water area only."""
    H, W = scene.shape[:2]
    out = np.zeros_like(scene)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(yy - horizon, 0, None)
    n = fbm(W, H, seed, 30, 3) - 0.5
    rip = np.sin(d / (wl * (0.6 + d / H)) + n * 6) * amp * (0.3 + d / max(1, H - horizon))
    sy = horizon - d * 1.0 + n * 2
    sx = xx + rip
    for c in range(4):
        out[..., c] = map_coordinates(scene[..., c], [np.clip(sy, 0, H - 1), np.clip(sx, 0, W - 1)], order=1)
    out[..., :3] = gaussian_filter(out[..., :3], (blur, blur * 2.5, 0))
    below = (yy > horizon).astype(np.float32)
    k = np.clip(1 - d / max(1, (H - horizon)) * fade, 0, 1)
    out[..., 3] *= below * k
    if tint_a:
        out[..., :3] = out[..., :3] * (1 - tint_a) + col_arr(tint) * tint_a
    return out


def ripple_lines(W, H, y0, y1, seed, density=0.5, lmin=10, lmax=60):
    """Mask of short horizontal glints/ripple strokes, longer and wider toward the viewer (y1)."""
    rng = np.random.default_rng(seed)
    items = []
    n = int((y1 - y0) * W / 900 * density)
    for _ in range(n):
        t = rng.random() ** 0.8
        y = y0 + (y1 - y0) * t
        x = rng.uniform(-20, W + 20)
        L = rng.uniform(lmin, lmax) * (0.4 + t)
        wd = 0.6 + 2.2 * t
        items.append(([(x, y), (x + L * 0.5, y + rng.uniform(-0.6, 0.6)), (x + L, y)], wd, (0.4, 0.4)))
    return strokes(W, H, items)


def tri_lattice(W, H, s, ox=0.0, oy=0.0):
    """Indices for an equilateral triangle lattice of side s: returns (i, j, up) arrays per pixel."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    h = s * math.sqrt(3) / 2
    row = np.floor((yy - oy) / h)
    fy = ((yy - oy) / h) - row
    xs = (xx - ox) / s - ((yy - oy) / h) * 0.5
    col = np.floor(xs)
    fx = xs - col
    up = (fx + fy < 1.0)
    return row.astype(np.int32), col.astype(np.int32), up, fx, fy


KH_BONE, KH_BRASS, KH_WAL, KH_EBO, KH_WAL_L = "#efe4cc", "#c9a253", "#6b4226", "#2a1a10", "#8a5a34"


def khatam(W, H, s, ox=0.0, oy=0.0, seed=1, palette=None, spacing=3):
    """Khatam-kari micro-mosaic field (RGBA, opaque): an equilateral-triangle lattice of tiny inlaid pieces (bone,
    brass, walnut, ebony) forming six-pointed stars with brass points and bone cores, each piece outlined by dark
    glue lines, brass points carrying a smaller bone inlay, slight per-piece tone variation."""
    pal = palette or {}
    bone = col_arr(pal.get("bone", KH_BONE)); brass = col_arr(pal.get("brass", KH_BRASS))
    wal = col_arr(pal.get("wal", KH_WAL)); ebo = col_arr(pal.get("ebo", KH_EBO)); wl = col_arr(pal.get("wal_l", KH_WAL_L))
    row, col, up, fx, fy = tri_lattice(W, H, s, ox, oy)
    h = s * math.sqrt(3) / 2
    # centroid in lattice (axial) coordinates
    cq = np.where(up, col + 1 / 3, col + 2 / 3).astype(np.float32)
    cr = np.where(up, row + 1 / 3, row + 2 / 3).astype(np.float32)
    # nearest star centre on the spacing-sublattice (search the 4 surrounding candidates)
    best = np.full((H, W), 1e9, np.float32); bq = np.zeros((H, W), np.float32); br = np.zeros((H, W), np.float32)
    q0 = np.floor(cq / spacing) * spacing; r0 = np.floor(cr / spacing) * spacing
    for dq in (0, spacing):
        for dr in (0, spacing):
            qq, rr = q0 + dq, r0 + dr
            ddq, ddr = cq - qq, cr - rr
            d2 = ddq * ddq + ddr * ddr + ddq * ddr  # axial metric (in units of s^2)
            sel = d2 < best
            best = np.where(sel, d2, best); bq = np.where(sel, qq, bq); br = np.where(sel, rr, br)
    d = np.sqrt(best)
    core = d < 0.7
    point = (d > 0.9) & (d < 1.3)
    # barycentric inset & glue lines
    a = np.where(up, fx, 1 - fx); b = np.where(up, fy, 1 - fy); c = np.where(up, 1 - fx - fy, fx + fy - 1)
    mn = np.minimum(np.minimum(a, b), c)
    inner = mn > 0.24
    rng = np.random.default_rng(seed)
    tid = (row * 7919 + col * 104729 + up.astype(np.int32) * 31337)
    var = ((np.sin(tid * 0.12345) * 43758.5453) % 1.0).astype(np.float32)
    rgb = np.where(up[..., None], wal, ebo) * (0.9 + 0.2 * var[..., None])
    rgb = np.where((d > 1.3)[..., None] & (d < 1.75)[..., None] & up[..., None], wl * (0.92 + 0.15 * var[..., None]), rgb)
    rgb = np.where(point[..., None], bone * (0.93 + 0.1 * var[..., None]), rgb)
    rgb = np.where((point & inner)[..., None], bone * 1.04, rgb)
    rgb = np.where(core[..., None], brass * (0.88 + 0.2 * var[..., None]), rgb)
    glue = np.clip((0.06 - mn) / 0.04, 0, 1).astype(np.float32)
    rgb = rgb * (1 - glue[..., None] * 0.7)
    # wear: tiny grain, polish
    g = gaussian_filter(rng.random((H, W)).astype(np.float32), 0.6)
    rgb = rgb * (0.96 + 0.08 * g[..., None])
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def clip_to(layer, mask):
    out = layer.copy()
    out[..., 3] = out[..., 3] * mask
    return out
