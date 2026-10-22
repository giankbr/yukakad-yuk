"""Agent D3 helpers (kilim-anatolia, pualam-hitam, sulam-zamrud, mutiara-damaskus).
Builds on _c2_lib (satin / couch / silk / lame textile media, local crops) and adds:
  kilim()      weft-faced slit-tapestry weave rendered from a cell design grid (pips, slits, abrash, wool fuzz)
  marble()     tileable Nero Marquina: black calcite ground, crisp white veins, fine web cracks, polish
  brass()      polished brass/gold inlay strips (bevel, groove seam, hairline scratches)
  walnut()     tileable walnut grain (rays, pores, figure, satin varnish)
  pearl()      mother-of-pearl pieces: iridescent thin-film hue drift, growth lines, per-piece orientation
Previews -> /tmp/pen/nb-D3/art."""
import sys, os, math
sys.path.insert(0, "/tmp/pen/art/themes")
from _c2_lib import *  # noqa
import _c2_lib, _p1_lib, _j1_lib
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates, binary_dilation, label

PREV = "/tmp/pen/nb-D3/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_c2_lib.PREV = PREV


# ------------------------------------------------------------------ embroidery (straighter satin threads)
def satin2(mask, col, col2=None, angle=0.0, spacing=3.0, seed=1, stitch=16.0, sheen=0.55, light=-0.8, radial=None,
          raise_=0.6, fuzz=0.6, wob=0.22, wsig=14):
    """Satin / long-and-short stitch fill. angle: thread direction (rad). radial=(cx, cy) makes threads radiate
    from a point (petals, fans). Returns RGBA."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1 = (wnoise(w, h, seed, wsig) - 0.5) * wob * 6 + (wnoise(w, h, seed + 1, 2) - 0.5) * wob
    if radial is not None:
        cx, cy = radial
        rr = np.hypot(xx - cx, yy - cy) + 1e-3
        ph = np.arctan2(yy - cy, xx - cx)
        v = ph * max(20.0, float(np.percentile(rr[mask > 0.5], 60)) if (mask > 0.5).any() else 40) / spacing + n1
        u = rr / stitch
        ang = ph
    else:
        ca, sa = math.cos(angle), math.sin(angle)
        v = (-xx * sa + yy * ca) / spacing + n1
        u = (xx * ca + yy * sa) / stitch
        ang = np.full((h, w), angle, np.float32)
    row = np.floor(v)
    prof = np.sin(np.pi * (v - row))  # thread cylinder 0..1
    rnd = np.random.default_rng(seed)
    off = rnd.random(4096).astype(np.float32)
    ri = (row.astype(np.int64) % 4096)
    brk = (u + off[ri] * 1.0) % 1.0  # long-and-short: each thread row breaks at its own phase
    gap = np.clip(1 - np.minimum(brk, 1 - brk) / 0.05, 0, 1)
    ca_ = C(col); cb_ = C(col2 or col)
    t = (fbm(w, h, seed + 3, 60, 2) * 0.7 + off[(ri + 7) % 4096] * 0.3)[..., None]
    base = ca_ * (1 - t) + cb_ * t
    dirk = np.abs(np.cos(ang - light))  # threads facing the light shine
    lum = 0.62 + 0.38 * prof ** 0.7
    lum = lum * (1 - 0.35 * gap)
    # raised padding: lighter in the middle of the shape, darker at the rim
    if raise_:
        dist = gaussian_filter(mask, 3.0)
        lum = lum * (0.82 + 0.25 * raise_ * np.clip(dist * 1.3, 0, 1))
    rgb = base * lum[..., None]
    hl = (prof ** 5) * dirk * sheen * (1 - gap)
    rgb = rgb + (1 - rgb) * hl[..., None] * 0.75
    a = mask
    if fuzz:
        a = np.clip(displace(mask, seed + 9, fuzz, 3.0) * 1.15, 0, 1)
    return rgba(rgb, a)



def SAT(dst, mask, col, col2=None, pad=6, mode="over", **k):
    """satin() computed inside the mask bbox only (radial centre is shifted into the crop)."""
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    if k.get("radial") is not None:
        k = dict(k); k["radial"] = (k["radial"][0] - x0, k["radial"][1] - y0)
    src = satin2(np.ascontiguousarray(mask[y0:y1, x0:x1]), col, col2, **k)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    return out



# ------------------------------------------------------------------ kilim
def kilim(D, pal, cw=6, rh=4, seed=1, abrash=0.07, slit=0.8, fuzz=0.5, tile=True, alpha=None):
    """Weft-faced kilim. D: int grid [rows, warps] of palette indices (-1 = transparent). pal: list of hex.
    Each cell = one weft pass over one warp; pips alternate by half a warp per row (over/under).
    Vertical colour boundaries become slits (dark gaps). Returns RGBA of size (rows*rh, warps*cw)."""
    D = np.asarray(D)
    gh, gw = D.shape
    H, W = gh * rh, gw * cw
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # gentle weft wobble (beaten-in rows are never quite straight)
    wob = (wnoise(W, H, seed + 1, 18) - 0.5) * rh * 0.8 if tile else (fbm(W, H, seed + 1, 60, 2) - 0.5) * rh * 0.8
    yv = yy + wob
    row = np.floor(yv / rh).astype(int)
    v = yv / rh - row
    row = row % gh if tile else np.clip(row, 0, gh - 1)
    shift = (row % 2) * 0.5
    xu = xx / cw + shift
    col = np.floor(xu).astype(int)
    u = xu - col
    col = col % gw if tile else np.clip(col, 0, gw - 1)
    idx = D[row, col]
    # pip: rounded bump of weft over a warp
    du = (u - 0.5) * 2; dv = (v - 0.5) * 2
    pip = np.clip(1 - (np.abs(du) ** 2.2 + np.abs(dv) ** 1.6), 0, 1)
    lum = 0.7 + 0.34 * pip ** 0.55
    lum *= 0.95 + 0.07 * np.cos((xx / cw) * math.tau)  # warp ridges under the weft
    # per-pip variation + per-row abrash (dye lot drift along rows for each colour)
    pv = rng.random((gh, gw)).astype(np.float32)
    lum *= 0.93 + 0.12 * pv[row, col]
    rowdrift = gaussian_filter(rng.random(gh).astype(np.float32), 3, mode="wrap")
    rowdrift = (rowdrift - rowdrift.mean()) / (rowdrift.std() + 1e-6)
    P = np.array([hex_rgb(c) for c in pal], np.float32)
    rgb = P[np.clip(idx, 0, len(pal) - 1)]
    ab = (1 + abrash * rowdrift[row] * (0.5 + pv[row, col] * 0.5))[..., None]
    rgb = rgb * ab
    # slits: vertical boundary between differently coloured neighbours in the same row
    right = D[row, (col + 1) % gw] if tile else D[row, np.clip(col + 1, 0, gw - 1)]
    left = D[row, (col - 1) % gw] if tile else D[row, np.clip(col - 1, 0, gw - 1)]
    sl = np.where(right != idx, np.clip(1 - (1 - u) / 0.16, 0, 1), 0) + np.where(left != idx, np.clip(1 - u / 0.16, 0, 1), 0)
    lum *= 1 - slit * np.clip(sl, 0, 1) * 0.75
    # wool fuzz + fibre hairs along weft
    hair = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.4, 2.2), mode="wrap")
    hair = (hair - hair.mean()) / (hair.std() + 1e-6)
    lum *= 1 + hair * 0.035 * fuzz
    rgb = rgb * lum[..., None]
    a = np.ones((H, W), np.float32) if alpha is None else alpha
    if (D < 0).any():
        a = a * (idx >= 0)
        a = np.clip(gaussian_filter(a, 0.5) * 1.3, 0, 1) * (idx >= 0)
    return rgba(rgb, a)


def stepped_diamond(D, cy, cx, r, val, ry=None, hollow=None):
    """Write a stepped (pixel) diamond |x|/r + |y|/ry <= 1 into grid D (rows are ~ ry, warps r)."""
    ry = ry or r
    gh, gw = D.shape
    for i in range(gh):
        for j in range(gw):
            d = abs(j - cx) / r + abs(i - cy) / ry
            if d <= 1 and (hollow is None or d > hollow):
                D[i, j] = val


def fringe(W, H, pitch=7, seed=1, col="#efe3c8", knot_every=4, length=0.8):
    """Warp fringe: bundles of cotton warp ends knotted every few warps, hanging down. RGBA."""
    rng = np.random.default_rng(seed)
    items = []
    knots = []
    n = int(W / pitch)
    for k in range(n // knot_every + 1):
        kx = (k + 0.5) * pitch * knot_every
        ky = H * 0.22 + rng.uniform(-1, 1)
        knots.append((kx, ky))
        for j in range(knot_every):
            x0 = (k * knot_every + j + 0.5) * pitch
            items.append(([(x0, 0), (x0 + (kx - x0) * 0.7, ky - 2), (kx + (kx - x0) * 0.1, ky + 3)], 2.4, None))
            L = H * length * rng.uniform(0.82, 1.0)
            sway = rng.uniform(-3, 3)
            pts = [(kx + (j - knot_every / 2) * 1.1 + sway * t * t, ky + t * (L - ky)) for t in np.linspace(0, 1, 12)]
            items.append((pts, 2.2, (0.0, 0.3)))
    m = strokes(W, H, items)
    km = circles(W, H, [(x, y, pitch * 0.55) for x, y in knots])
    m = np.maximum(m, km)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    tw = 0.5 + 0.5 * np.sin((xx * 1.6 + yy * 0.9) / 2.2)
    lum = 0.78 + 0.22 * tw
    lum = lum * (1 - 0.25 * (yy / H))
    rgb = np.ones((H, W, 3), np.float32) * C(col) * lum[..., None]
    sh = np.clip(gaussian_filter(km, 1.5) - km, 0, 1)
    rgb *= (1 - sh * 0.4)[..., None]
    return rgba(rgb, np.clip(m * 1.1, 0, 1))


# ------------------------------------------------------------------ marble
def ridge(n, sharp=40.0):
    """Ridged line field from noise: 1 on the 0.5 iso-line, falling off fast."""
    return np.exp(-((n - 0.5) * sharp) ** 2)


def marble(W, H, seed=1, ground="#0d0d0f", ground2="#1c1b1f", vein="#dcd7cc", tile=True, veins=1.0, web=1.0):
    """Nero Marquina: tileable when tile=True (wrap noise)."""
    nz = (lambda s, sg: wnoise(W, H, s, sg)) if tile else (lambda s, sg: fbm(W, H, s, sg * 4, 3))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cloud = nz(seed, 60) * 0.6 + nz(seed + 1, 20) * 0.4
    rgb = C(ground) * (1 - cloud[..., None]) + C(ground2) * cloud[..., None]
    # main veins: long flowing diagonal veins (low-frequency domain warp), brightness broken along their length
    warp = (nz(seed + 2, 90) - 0.5) * 0.75 + (nz(seed + 3, 22) - 0.5) * 0.14 + (nz(seed + 12, 5) - 0.5) * 0.05 + (nz(seed + 15, 2) - 0.5) * 0.02
    base = (xx / W + yy / H)
    f1 = (base * 2 + warp) % 1.0
    v1 = (ridge(f1, 80) + 0.12 * ridge(f1, 26)) * np.clip(0.2 + 1.2 * nz(seed + 4, 40), 0, 1)
    f2 = (base * 3 - warp * 1.3 + (nz(seed + 5, 50) - 0.5) * 0.5) % 1.0
    v2 = ridge(f2, 130) * np.clip((nz(seed + 6, 45) - 0.3) * 2.2, 0, 1)
    f2b = (base * 5 + warp * 0.8 + (nz(seed + 13, 30) - 0.5) * 0.4) % 1.0
    v2b = ridge(f2b, 160) * np.clip((nz(seed + 14, 30) - 0.5) * 2.5, 0, 1) * 0.6
    # web: fine fracture net, only near the big veins
    near = np.clip(gaussian_filter(v1 + v2, 14, mode="wrap" if tile else "nearest") * 4, 0, 1)
    g = nz(seed + 7, 7)
    v3 = ridge(g, 80) * near * np.clip((nz(seed + 9, 20) - 0.45) * 2.5, 0, 1) * 0.3
    v4 = ridge(nz(seed + 10, 3.5), 70) * near * np.clip((nz(seed + 11, 16) - 0.55) * 3, 0, 1) * 0.2
    v1 = v1 + v2b
    vv = np.clip(v1 * veins + v2 * veins * 0.8 + (v3 + v4) * web, 0, 1)
    halo = gaussian_filter(vv, 5, mode="wrap" if tile else "nearest") * 0.22
    rgb = rgb * (1 - halo[..., None]) + C("#6b6760") * halo[..., None]
    rgb = rgb * (1 - vv[..., None]) + C(vein) * vv[..., None]
    # polish: soft broad reflection + micro grain
    gr = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.6, mode="wrap")
    rgb = rgb * (1 + (gr - 0.5)[..., None] * 0.06)
    return rgba(rgb, np.ones((H, W), np.float32))


def brass(mask, base="#c9a24e", seed=1, groove=0.8, scratch=0.5, light=(-0.7, -0.7), tile=False, polish=0.6):
    """Polished brass inlay: bevelled strip (light from top-left), dark groove where it meets the stone,
    hairline scratches, broad specular streak. Returns RGBA (alpha = mask + groove)."""
    h, w = mask.shape
    m = np.clip(mask, 0, 1)
    sm = gaussian_filter(m, 1.2)
    gy, gx = np.gradient(sm)
    bevel = np.clip(0.5 - (gx * light[0] + gy * light[1]) * 7, 0, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nz = wnoise(w, h, seed, 30) if tile else fbm(w, h, seed, 90, 2)
    streak = 0.5 + 0.5 * np.sin((xx * 0.7 - yy * 0.7) / max(24, w * 0.08) + nz * 4)
    sc = gaussian_filter(np.random.default_rng(seed + 2).random((h, w)).astype(np.float32), (0.3, 6), mode="wrap")
    sc = (sc - sc.mean()) / (sc.std() + 1e-6)
    lum = 0.62 + 0.3 * streak * polish + (bevel - 0.5) * 0.9 + sc * 0.03 * scratch
    r, g, b = hex_rgb(base)
    rgb = np.stack([r * lum * 1.15, g * lum * 1.1, b * lum * 0.95], -1)
    rgb = rgb + np.clip(lum - 1.0, 0, 1)[..., None] * 0.8
    out = rgba(rgb, m)
    if groove:
        gm = np.clip(gaussian_filter(m, 1.3) * 2.4, 0, 1)
        grv = rgba(np.zeros((h, w, 3), np.float32) + 0.02, np.clip(gm - m, 0, 1) * groove)
        out = over(grv, out)
    return out


# ------------------------------------------------------------------ wood + shell
def walnut(W, H, seed=1, light="#6b4429", dark="#2e1a10", tile=True, figure=0.6):
    """Tileable walnut: dense fine grain lines with irregular spacing, broad colour drift, pore streaks, satin varnish."""
    nz = (lambda s, sg: wnoise(W, H, s, sg)) if tile else (lambda s, sg: fbm(W, H, s, sg * 4, 3))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.default_rng(seed + 9)
    def streak(sy, sx, sd):
        n = gaussian_filter(np.random.default_rng(sd).random((H, W)).astype(np.float32), (sy, sx), mode="wrap")
        return (n - n.min()) / (n.max() - n.min() + 1e-6)
    warp = (nz(seed, 70) - 0.5) * 10
    sh = np.round(warp).astype(int)
    def bend(a):
        return a[(np.arange(H)[:, None] + sh) % H, np.arange(W)[None, :]]
    broad = bend(streak(6, 90, seed + 2))
    mid = bend(streak(1.6, 40, seed + 3))
    fine = bend(streak(0.6, 25, seed + 4))
    t = np.clip(0.42 + (broad - 0.5) * 1.6 + (mid - 0.5) * 0.9 + (fine - 0.5) * 0.5 + (nz(seed + 5, 80) - 0.5) * 0.4, 0, 1)
    rgb = C(light) * (1 - t[..., None]) + C(dark) * t[..., None]
    pores = gaussian_filter(np.random.default_rng(seed + 4).random((H, W)).astype(np.float32), (0.4, 9), mode="wrap")
    pores = np.clip((pores - 0.53) * 9, 0, 1)
    rgb *= (1 - pores * 0.18)[..., None]
    fig = 0.5 + 0.5 * np.sin(xx / W * math.tau * 5 + nz(seed + 5, 20) * 5)
    rgb *= (1 + (fig - 0.5) * 0.08 * figure)[..., None]
    sheen = nz(seed + 6, 80)
    rgb = rgb * (0.93 + 0.14 * sheen[..., None])
    return rgba(rgb, np.ones((H, W), np.float32))


def pearl(mask, seed=1, pieces=None, base="#f4eee6", irid=0.42, lines=0.5, tile=False):
    """Mother-of-pearl inlay. pieces: optional int label map (each piece gets its own growth-line angle and
    iridescence phase). Thin-film colour drifts pink -> green -> blue across the shell."""
    h, w = mask.shape
    nz = (lambda s, sg: wnoise(w, h, s, sg)) if tile else (lambda s, sg: fbm(w, h, s, sg * 4, 3))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rng = np.random.default_rng(seed)
    if pieces is None:
        pieces, n = label(mask > 0.5)
    n = int(pieces.max()) + 1
    ang = rng.uniform(0, math.pi, n).astype(np.float32)[pieces]
    ph = rng.uniform(0, math.tau, n).astype(np.float32)[pieces]
    bri = rng.uniform(0.9, 1.06, n).astype(np.float32)[pieces]
    u = xx * np.cos(ang) + yy * np.sin(ang)
    gl = 0.5 + 0.5 * np.sin(u / 2.2 + nz(seed + 1, 6) * 5)
    film = ph + u / 26 + nz(seed + 2, 14) * 5
    # thin-film palette (soft): rose, celadon, sky, champagne
    hue = np.stack([0.5 + 0.5 * np.cos(film), 0.5 + 0.5 * np.cos(film - 2.1), 0.5 + 0.5 * np.cos(film - 4.2)], -1)
    rgb = C(base) * (1 - irid * 0.32) + hue * irid * 0.32
    rgb = rgb * (bri * (0.9 + 0.1 * gl * lines + 0.06 * (1 - lines)))[..., None]
    milk = nz(seed + 3, 10)
    rgb = rgb * (1 - 0.12 * np.clip(milk - 0.6, 0, 1))[..., None] + 0.08 * np.clip(milk - 0.7, 0, 1)[..., None]
    # bevel of each piece + glue line
    sm = gaussian_filter(mask, 0.9)
    gy, gx = np.gradient(sm)
    rgb = rgb * (1 + np.clip(-(gx + gy) * 3, -0.25, 0.25))[..., None]
    return rgba(rgb, np.clip(mask, 0, 1))


def ngon(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + k * math.tau / n), cy + r * math.sin(rot + k * math.tau / n)) for k in range(n)]


def star8(cx, cy, r, inner=0.414, rot=0.0):
    """8-point star made of two squares (khatam)."""
    pts = []
    ri = r * math.cos(math.pi / 4) / math.cos(math.pi / 8) * 0.0 + r * inner * 1.0
    for k in range(16):
        rr = r if k % 2 == 0 else r * 0.7654
        pts.append((cx + rr * math.cos(rot + k * math.pi / 8), cy + rr * math.sin(rot + k * math.pi / 8)))
    return pts


def starn(cx, cy, r, ri, n, rot=0.0):
    pts = []
    for k in range(2 * n):
        rr = r if k % 2 == 0 else ri
        pts.append((cx + rr * math.cos(rot + k * math.pi / n), cy + rr * math.sin(rot + k * math.pi / n)))
    return pts


def outline(W, H, polys, width, closed=True, cap=False):
    """Stroked polygons (sharp joins) into one mask."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                   StrokeJoin=skia.Paint.kMiter_Join, StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
    p.setStrokeMiter(8)
    for pts in polys:
        path = skia.Path(); path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        if closed:
            path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def fills(W, H, polys):
    return shapes(W, H, polys, smooth=False)


def kb(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", d.split("/")[-1], t // 1024, "KB")
