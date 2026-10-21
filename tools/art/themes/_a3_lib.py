"""Agent A3 helpers (zellige-hijau, andalusia-terakota, iznik-tulip, taman-persia): glazed zellige mosaic, carved
stucco relief, cuerda-seca tile, Iznik underglaze on crackled slip, Persian miniature motifs. Built on _j1_lib
(bbox-cropped G/GP/LC/FO/OV). Previews -> /tmp/pen/nb-A3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-A3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
from _j1_lib import trim_cache
from _jw_lib import along, spiral_pts
_p1_lib.PREV = "/tmp/pen/nb-A3/art"
import art as _art
from scipy import ndimage as ndi

PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def smooth01(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(h, w, col):
    return np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)


def noise(w, h, seed, sigma, wrap=False):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap" if wrap else "reflect")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def star_pts(cx, cy, r_out, r_in, n=8, rot=0.0):
    pts = []
    for k in range(n * 2):
        a = rot + k * math.pi / n
        r = r_out if k % 2 == 0 else r_in
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def poly_lines(W, H, polys, width, closed=True, cap=True):
    """Polygon outlines into one mask (grout / cord lines)."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
    for pts in polys:
        path = skia.Path()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        if closed:
            path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def wob_poly(pts, rng, amt):
    return [(x + rng.gauss(0, amt), y + rng.gauss(0, amt)) for x, y in pts]


# ------------------------------------------------------------------ glazed tile mosaic (zellige & cuerda seca)
def label_regions(grout, inside=None):
    m = grout < 0.5
    if inside is not None:
        m &= inside > 0.5
    lab, n = ndi.label(m)
    return lab, n


def per_label(lab, n, values):
    """values: array (n+1, k) -> image (h, w, k)."""
    return values[lab]


def tile_glaze(lab, n, colour_of, seed=1, bevel=3.2, chip=0.5, body="#c39a74", grout_col="#d8d0c0", inside=None,
               gloss=0.55, mottle=0.12, light=(-0.6, -0.8), tilt=0.06, rim=0.18):
    """Render labelled tiles as individually glazed ceramic pieces set in grout.
    colour_of(label_index, cx, cy, rng) -> hex. Returns opaque-in-`inside` RGBA."""
    h, w = lab.shape
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    cents = ndi.center_of_mass(np.ones_like(lab), lab, range(1, n + 1)) if n else []
    cols = np.zeros((n + 1, 3), np.float32)
    tilts = np.zeros((n + 1, 3), np.float32)
    tilemask0 = lab > 0
    dist0 = ndi.distance_transform_edt(tilemask0).astype(np.float32)
    deep = ndi.maximum_position(dist0, lab, range(1, n + 1)) if n else []
    for i, (cy, cx) in enumerate(deep, 1):
        c = colour_of(i, cx, cy, rng)
        cols[i] = np.array(hex_rgb(jitter_hex(c, rng, 0.035)), np.float32)
        a = rng.uniform(0, math.tau)
        tilts[i] = (math.cos(a) * tilt, math.sin(a) * tilt, rng.uniform(-0.05, 0.05))
    tilemask = lab > 0
    dist = ndi.distance_transform_edt(tilemask).astype(np.float32)
    hgt = smooth01(dist / bevel)
    # chips: bites out of tile edges show the clay body
    if chip:
        seeds = (nrng.random((h, w)) > 1 - 0.0016 * chip) & (dist > 0) & (dist < 2.5)
        bites = gaussian_filter(seeds.astype(np.float32), 2.6) * 40
        bites = displace(np.clip(bites, 0, 1), seed + 3, 2.0, 6)
        chipm = np.clip((bites - 0.35) * 3, 0, 1) * tilemask
    else:
        chipm = np.zeros((h, w), np.float32)
    hgt = hgt * (1 - chipm * 0.7)
    gy, gx = np.gradient(gaussian_filter(hgt, 0.8))
    shade = np.clip(0.5 - (gx * light[0] + gy * light[1]) * 2.2, 0, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = cols[lab]
    tl = tilts[lab]
    cyx = np.zeros((n + 1, 2), np.float32)
    for i, (cy, cx) in enumerate(cents, 1):
        cyx[i] = (cy, cx)
    c2 = cyx[lab]
    plane = ((xx - c2[..., 1]) * tl[..., 0] + (yy - c2[..., 0]) * tl[..., 1]) / 40 + tl[..., 2]
    mot = noise(w, h, seed + 5, 5) * 0.6 + noise(w, h, seed + 6, 14) * 0.4
    pools = np.clip((noise(w, h, seed + 7, 3.5) - 0.62) * 4, 0, 1)
    lum = 1 + plane - mottle * (mot - 0.5) * 2 - pools * 0.12
    rgb = base * lum[..., None]
    # thin glaze at rounded rims -> paler, warmer
    rimk = (1 - hgt) * tilemask * rim
    rgb = rgb * (1 - rimk[..., None]) + np.array(hex_rgb("#efe6d2"), np.float32) * rimk[..., None]
    rgb = rgb * (0.82 + 0.36 * shade[..., None])
    # gloss: soft window reflections broken by the uneven surface
    if gloss:
        g = np.clip((noise(w, h, seed + 9, 9) - 0.6) * 3.5, 0, 1) * shade * hgt
        spec = np.clip((shade - 0.62) * 5, 0, 1) * 0.5 + g
        rgb = rgb + spec[..., None] * gloss * 0.35
    # clay body in chips
    bodyc = np.array(hex_rgb(body), np.float32) * (0.85 + 0.25 * noise(w, h, seed + 11, 1.2))[..., None]
    rgb = rgb * (1 - chipm[..., None]) + bodyc * chipm[..., None]
    # grout
    gr = np.array(hex_rgb(grout_col), np.float32) * (0.86 + 0.2 * noise(w, h, seed + 13, 0.8))[..., None]
    near = np.clip(gaussian_filter(tilemask.astype(np.float32), 1.2), 0, 1)
    gr = gr * (1 - 0.22 * near[..., None])
    tm = np.clip(gaussian_filter(tilemask.astype(np.float32), 0.5), 0, 1)
    out = rgb * tm[..., None] + gr * (1 - tm[..., None])
    a = np.ones((h, w), np.float32) if inside is None else np.clip(inside, 0, 1)
    return rgba(out, a)


def star_cross_polys(x0, y0, x1, y1, d, ox=0.0, oy=0.0, rng=None, wob=0.0):
    """8-point star outlines for the star-and-cross tiling covering a box (stars at d spacing, checker)."""
    out = []
    r = d / 2 * 1.0
    ri = r * 0.7654
    i0, i1 = int(math.floor((x0 - ox) / d)) - 1, int(math.ceil((x1 - ox) / d)) + 1
    j0, j1 = int(math.floor((y0 - oy) / d)) - 1, int(math.ceil((y1 - oy) / d)) + 1
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            cx, cy = ox + i * d, oy + j * d
            pts = star_pts(cx, cy, r, ri, 8, 0)
            if rng is not None and wob:
                pts = wob_poly(pts, rng, wob)
            out.append(((i, j), pts))
    return out


# ------------------------------------------------------------------ carved stucco relief (yeseria)
def stucco(height, mask, col="#eadcc2", seed=1, light=(-0.55, -0.85), depth=2.6, ao=0.5, dirt="#9b7a55", crisp=0.6):
    """height: 0..1 relief (raised=1). Returns RGBA plaster with raking light, occlusion in recesses, worn edges."""
    h, w = height.shape
    hh = gaussian_filter(height, crisp) + (noise(w, h, seed, 1.0) - 0.5) * 0.04
    gy, gx = np.gradient(hh)
    shade = np.clip(0.55 - (gx * light[0] + gy * light[1]) * depth * 4, 0, 1)
    occ = np.clip(gaussian_filter(hh, 4) - hh, 0, 1) * 4 * ao
    base = flat(h, w, col) * (0.92 + 0.12 * noise(w, h, seed + 1, 16) + 0.05 * noise(w, h, seed + 2, 1.5))[..., None]
    rgb = base * (0.62 + 0.62 * shade[..., None])
    dc = np.array(hex_rgb(dirt), np.float32)
    k = np.clip(occ + (1 - hh) * 0.15, 0, 0.75)[..., None]
    rgb = rgb * (1 - k * 0.6) + dc * k * 0.6 * (rgb.mean(-1, keepdims=True))
    return rgba(rgb, mask)


# ------------------------------------------------------------------ Iznik underglaze on white slip
def crackle(w, h, seed, scale=1.0, wrap=False):
    """Glaze crazing: Voronoi cell boundaries (polygonal network of fine, slightly wavering lines), two scales."""
    from scipy.spatial import cKDTree
    out = np.zeros((h, w), np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    jx = (noise(w, h, seed + 40, 6, wrap) - 0.5) * 3
    jy = (noise(w, h, seed + 41, 6, wrap) - 0.5) * 3
    q = np.stack([(xx + jx).ravel(), (yy + jy).ravel()], 1)
    for k, (cell, amt) in enumerate([(34 * scale, 1.0), (13 * scale, 0.55)]):
        rng = np.random.default_rng(seed + k)
        gx_, gy_ = max(1, round(w / cell)), max(1, round(h / cell))
        cw, chh = w / gx_, h / gy_
        ii, jj = np.meshgrid(np.arange(gx_), np.arange(gy_))
        pts = np.stack([(ii.ravel() + 0.5 + (rng.random(ii.size) - 0.5) * 0.8) * cw, (jj.ravel() + 0.5 + (rng.random(ii.size) - 0.5) * 0.8) * chh], 1)
        if wrap:
            pts = np.concatenate([pts + [dx * w, dy * h] for dx in (-1, 0, 1) for dy in (-1, 0, 1)])
        d, _ = cKDTree(pts).query(q, k=2)
        edge = (d[:, 1] - d[:, 0]).reshape(h, w)
        line = np.clip(1 - edge / (0.9 + 0.3 * k), 0, 1)
        if k == 1:
            line *= noise(w, h, seed + 50, 10, wrap) > 0.45
        out = np.maximum(out, line * amt)
    return np.clip(out, 0, 1)


def slip_ground(w, h, seed=1, tone="#f7f4ec", wrap=False, crack=0.08):
    rgb = flat(h, w, tone) * (0.965 + 0.05 * noise(w, h, seed, 30, wrap)[..., None] + 0.015 * noise(w, h, seed + 1, 1, wrap)[..., None])
    rgb = rgb * (1 - crackle(w, h, seed + 4, 1.0, wrap)[..., None] * crack)
    return rgba(rgb, np.ones((h, w), np.float32))


def underglaze(mask, col, col2=None, seed=1, pool=0.55, density=0.92, rough=1.6, streak=0.4):
    """Iznik pigment under clear glaze: brushed fill with pooling (darker) at the rim and brush streaks, soft fused edge."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 10)
    m = gaussian_filter(m, 0.7)
    inner = gaussian_filter(m, 2.6)
    rim = np.clip(m - inner, 0, 1) * 2.2
    st = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.6, 4.0))
    st = (st - st.mean()) / (st.std() + 1e-6)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = noise(w, h, seed + 3, 18)[..., None]
    rgb = ca * (1 - t) + cb * t
    dark = np.clip(rim * pool + np.clip((noise(w, h, seed + 5, 3) - 0.6) * 2, 0, 1) * 0.25, 0, 1)
    rgb = rgb * (1 - 0.32 * dark[..., None]) * (1 + st[..., None] * 0.04 * streak)
    a = np.clip(m * density * (0.86 + 0.14 * noise(w, h, seed + 7, 6)) + rim * 0.1, 0, 1)
    return rgba(rgb, a)


def bole(mask, col="#c8352a", seed=1):
    """Raised Armenian-bole red: thick, slightly matte, uneven, with a faint relief edge."""
    h, w = mask.shape
    m = displace(mask, seed, 1.2, 8)
    m = np.clip((gaussian_filter(m, 0.6) - 0.3) * 2.0, 0, 1)
    n = noise(w, h, seed + 2, 2.2)
    rgb = flat(h, w, col) * (0.9 + 0.18 * n[..., None])
    gy, gx = np.gradient(gaussian_filter(m, 1.2))
    rgb = rgb * (1 + np.clip(-(gx + gy) * 1.6, -0.25, 0.25))[..., None]
    a = m * (0.86 + 0.14 * noise(w, h, seed + 3, 1.4))
    return rgba(rgb, a)


def outline_of(mask, px=1.6):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.03).astype(np.float32) - (gaussian_filter(mask, 0.6) > 0.5), 0, 1)


def ink(mask, col="#1f2c2c", seed=1, alpha=0.9):
    h, w = mask.shape
    m = displace(mask, seed, 0.8, 6)
    a = np.clip(gaussian_filter(m, 0.45) * 1.3, 0, 1) * alpha * (0.75 + 0.25 * noise(w, h, seed + 1, 3))
    return rgba(flat(h, w, col), a)


def glaze_sheen(arr, seed=1, amount=0.06):
    """Clear glaze: very soft reflections + slight blur fusion of the pigments."""
    h, w = arr.shape[:2]
    out = arr.copy()
    s = np.clip((noise(w, h, seed, 40) - 0.55) * 3, 0, 1) * amount
    out[..., :3] = np.clip(out[..., :3] + s[..., None], 0, 1)
    return out


def I(dst, mask, *a, pad=10, **k):
    return OV(dst, mask, lambda m: underglaze(m, *a, **k), pad=pad)


def B(dst, mask, *a, pad=8, **k):
    return OV(dst, mask, lambda m: bole(m, *a, **k), pad=pad)


def K(dst, mask, *a, pad=6, **k):
    return OV(dst, mask, lambda m: ink(m, *a, **k), pad=pad)


# ------------------------------------------------------------------ Iznik motifs (as polygons)
def rotp(pts, cx, cy, ang):
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def tulip_polys(x, y, s, ang=0.0):
    """Ottoman tulip: three almond-pointed petals (centre + two flaring sides). Base at (x,y), pointing up (ang=0)."""
    P = lambda u, v: (x + u * s, y - v * s)
    centre = [P(0, 0), P(-0.22, 0.3), P(-0.2, 0.75), P(-0.06, 1.15), P(0, 1.35), P(0.06, 1.15), P(0.2, 0.75), P(0.22, 0.3)]
    left = [P(0, 0.02), P(-0.3, 0.12), P(-0.45, 0.45), P(-0.46, 0.85), P(-0.52, 1.25), P(-0.3, 0.95), P(-0.12, 0.55)]
    right = [(2 * x - px, py) for px, py in left]
    polys = [left, right, centre]
    return [rotp(p, x, y, ang) for p in polys]


def carnation_polys(x, y, s, ang=0.0):
    """Ottoman carnation (fan of toothed petals over a calyx), base at (x,y)."""
    P = lambda u, v: (x + u * s, y - v * s)
    fan = []
    n = 7
    for k in range(n + 1):
        a = math.pi * (0.12 + 0.76 * k / n)
        r = 0.95 if k % 2 == 0 else 0.8
        fan.append(P(math.cos(a) * r * -1, 0.42 + math.sin(a) * r * 0.75))
    fan = [P(0.36, 0.42)] + fan[::-1] + [P(-0.36, 0.42)]
    fan = [P(0.3, 0.38)] + [P(math.cos(math.pi * (0.1 + 0.8 * k / 9)) * (0.92 if k % 2 == 0 else 0.74), 0.42 + math.sin(math.pi * (0.1 + 0.8 * k / 9)) * (0.82 if k % 2 == 0 else 0.62)) for k in range(10)] + [P(-0.3, 0.38)]
    calyx = [P(-0.16, 0), P(-0.3, 0.44), P(0, 0.52), P(0.3, 0.44), P(0.16, 0)]
    return [rotp(fan, x, y, ang), rotp(calyx, x, y, ang)]


def saz_leaf(pts, width, serr=0.0, rng=None):
    """Curved saz leaf polygon around a centre curve, with optional serrated edge."""
    n = len(pts); L = []; R = []
    for i in range(n):
        t = i / (n - 1)
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nxn, nyn = -dy / d, dx / d
        wd = width * math.sin(math.pi * t) ** 0.8 * (1 - 0.35 * t)
        if serr and 0.08 < t < 0.95:
            wd *= 1 + serr * (1 if i % 3 == 0 else -0.25)
        L.append((pts[i][0] + nxn * wd, pts[i][1] + nyn * wd)); R.append((pts[i][0] - nxn * wd * 0.85, pts[i][1] - nyn * wd * 0.85))
    return L + R[::-1]


def rosette_polys(cx, cy, r, petals=8, rot=0.0, inner=0.42):
    out = [petal_pts(cx, cy, r, r * 0.42, rot + k * math.tau / petals, n=10) for k in range(petals)]
    return out


# ------------------------------------------------------------------ Persian miniature motifs
def cypress_poly(x, by, h, w, rng, lean=0.0):
    """Flame-shaped cypress silhouette with a slightly twisted tip."""
    pts = []
    n = 18
    for k in range(n + 1):
        t = k / n
        yy = by - h * t
        wd = w * (math.sin(math.pi * min(1, t * 1.05)) ** 0.55) * (1 - t) ** 0.35 * 1.05
        pts.append((x + lean * h * t * t + wd + rng.gauss(0, w * 0.03), yy))
    tip = (x + lean * h + w * 0.18, by - h * 1.04)
    left = []
    for k in range(n, -1, -1):
        t = k / n
        yy = by - h * t
        wd = w * (math.sin(math.pi * min(1, t * 1.05)) ** 0.55) * (1 - t) ** 0.35
        left.append((x + lean * h * t * t - wd + rng.gauss(0, w * 0.03), yy))
    return pts + [tip] + left


def save_tex(arr, path, quality=78):
    im = to_image(arr).convert("RGB")
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size


def report(out):
    tot = 0
    for f in sorted(os.listdir(out)):
        sz = os.path.getsize(f"{out}/{f}")
        tot += sz
    print("TOTAL", out.split('/')[-1], tot // 1024, "KB")
