"""Agent N2 helpers (sangihe-kofo, sengkang-sutra, peach-syari, ultah-panda): thread-by-thread striped/check weaves
(abaca kofo, Sengkang silk), cloth drape with folds + sheen, water reflections, ranunculus. Builds on _m1_lib
(G/GP/LC/FO/OV, strokes, shapes, circles, ellipses, handspun ...). Previews -> /tmp/pen/nb-N2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _m1_lib import *  # noqa
_p1_lib.PREV = "/tmp/pen/nb-N2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
PREV = _p1_lib.PREV
import art as _art
from scipy.ndimage import map_coordinates


def seq_cols(seq):
    """seq: list of (hex, n_threads) -> per-thread colour array (N,3)."""
    out = []
    for hx, n in seq:
        out += [col3(hx)] * n
    return np.array(out, np.float32)


def weave(w, h, warp_seq, weft_seq, seed=1, warp=3.0, weft=3.0, twill=False, slub=0.6, sheen=0.0, fibre=0.0):
    """Seamless thread-by-thread plain (or 2/2 twill) weave. Each crossing shows warp or weft colour; thread relief,
    per-thread tone drift, slubs; `sheen` adds silk-like bright highlights on floats, `fibre` adds long abaca
    fibre streaks along the warp. Returns RGB float (h, w, 3)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nw = int(round(w / warp)); nf = int(round(h / weft))
    WC = seq_cols(warp_seq); FC = seq_cols(weft_seq)
    cw = np.floor(xx / w * nw).astype(int) % nw
    cf = np.floor(yy / h * nf).astype(int) % nf
    phx = (xx / w * nw) % 1.0; phy = (yy / h * nf) % 1.0
    over_ = ((cw + cf) % 2 == 0) if not twill else (((cw + cf) // 2) % 2 == 0)
    rw = np.clip(np.cos((phx - 0.5) * math.pi), 0, 1) ** 1.1
    rf = np.clip(np.cos((phy - 0.5) * math.pi), 0, 1) ** 1.1
    ridge = np.where(over_, rw * (0.8 + 0.2 * rf), rf * (0.8 + 0.2 * rw))
    tw = rng.normal(0, 1, nw); tf = rng.normal(0, 1, nf)
    col = np.where(over_[..., None], WC[cw % len(WC)], FC[cf % len(FC)])
    s = wrap_noise(w, h, seed + 3, (0.8, 7)) - 0.5
    s2 = wrap_noise(w, h, seed + 4, (7, 0.8)) - 0.5
    big = wrap_noise(w, h, seed + 5, 34) - 0.5
    v = 0.78 + 0.28 * ridge + np.where(over_, tw[cw], tf[cf]) * 0.04 + (s + s2) * 0.16 * slub + big * 0.06
    rgb = col * v[..., None]
    gap = (1 - rw * rf) ** 7
    rgb = rgb * (1 - gap[..., None] * 0.3)
    if sheen:
        hl = np.where(over_, rw, rf) ** 6
        band = 0.55 + 0.45 * np.sin((xx + yy * 0.6) / w * math.tau * 2 + (big * 4))
        rgb = rgb + (hl * band * sheen)[..., None] * 0.35 * (0.5 + 0.5 * col)
    if fibre:
        f = wrap_noise(w, h, seed + 9, (0.5, 22)) - 0.5
        rgb = rgb * (1 + f[..., None] * fibre * 0.5)
        glints = (wrap_noise(w, h, seed + 10, (0.4, 9)) > 0.8).astype(np.float32)
        rgb = rgb + glints[..., None] * fibre * 0.06
    return np.clip(rgb, 0, 1).astype(np.float32)


def warp_img(rgb, dx, dy):
    """Sample rgb (h,w,3) at (y+dy, x+dx) (wrap)."""
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    out = np.stack([map_coordinates(rgb[..., c], [(yy + dy) % h, (xx + dx) % w], order=1, mode="wrap") for c in range(3)], -1)
    return out


def tile_to(rgb, W, H):
    h, w = rgb.shape[:2]
    return np.tile(rgb, (H // h + 1, W // w + 1, 1))[:H, :W]


def shade_rgb(rgb, shade):
    return np.clip(rgb * shade[..., None], 0, 1)


def reflect(scene_rgb, y_line, H_out, seed=1, ripple=3.0, fade=0.55, tint="#1d3a55", tint_amt=0.35):
    """Mirror the rows above y_line below it with horizontal ripple displacement + darkening; returns (H_out, W, 3)."""
    h, w = scene_rgb.shape[:2]
    yy, xx = np.mgrid[0:H_out, 0:w].astype(np.float32)
    src_y = y_line - 1 - yy
    n = fbm(w, H_out, seed, 12, 2) - 0.5
    rip = np.sin(yy * 0.55 + n * 6) * ripple * (0.4 + yy / H_out)
    out = np.stack([map_coordinates(scene_rgb[..., c], [np.clip(src_y, 0, h - 1), np.clip(xx + rip, 0, w - 1)], order=1) for c in range(3)], -1)
    k = (fade * (0.6 + 0.4 * yy / H_out))[..., None]
    return out * (1 - k * tint_amt) + col3(tint) * k * tint_amt


def ranunculus(W, H, cx, cy, r, light, mid, deep, sd, rng, tilt=0.82, rings=6, centre="#8a6a3a"):
    """Watercolour ranunculus: tight concentric rings of small cupped petals (filled washes, each with a wet edge),
    darker and smaller towards a little green-brown eye; light from top-left."""
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * tilt, 12), rng, 2, 0.08))
    lay = pigment_local(base, light, mid, sd(), density=0.5, edge=0.5, bloom=0.45, rough=6, holes=0.03)
    for ring in range(rings):
        t = ring / max(1, rings - 1)
        rr = r * (0.9 - t * 0.72)
        n = int(10 - t * 4)
        a_off = rng.uniform(0, math.tau)
        polys = []
        for k in range(n):
            a = a_off + k / n * math.tau + rng.uniform(-.12, .12)
            px, py = cx + math.cos(a) * rr * 0.62, cy - r * 0.06 * t + math.sin(a) * rr * 0.62 * tilt
            pr = rr * (0.62 - 0.1 * t)
            polys.append(deform(ellipse_pts(px, py, pr, pr * 0.62, 10, a + math.pi / 2), rng, 1, 0.08))
        for k, pts in enumerate(polys):
            pm = shape_mask(W, H, pts)
            a = a_off + k / n * math.tau
            lit = 0.5 + 0.5 * math.cos(a + 2.4)  # light from the top-left
            c = mix(mix(light, mid, 0.2 + 0.45 * t), deep, 0.12 + 0.45 * t * (1 - lit))
            lay = glaze(lay, pigment_local(pm, c, mix(c, light, .35), sd(), density=0.22 + 0.16 * t, edge=1.0, bloom=0.25, rough=1.6, feather=0.6))
            if rng.random() < 0.55:
                pr = rr * (0.62 - 0.1 * t)
                px, py = cx + math.cos(a) * rr * 0.62, cy - r * 0.06 * t + math.sin(a) * rr * 0.62 * tilt
                rim = strokes(W, H, [(arc_pts(px, py, pr * 0.92, a - 0.7, a + 0.7, 12, 0.62), max(1.0, r * 0.018), (0.3, 0.3))])
                lay = glaze(lay, pigment_local(rim, deep, None, sd(), density=0.35, edge=0.3, bloom=0, rough=1, feather=0.5))
    eye = shape_mask(W, H, deform(ellipse_pts(cx, cy - r * .07, r * .09, r * .075, 8), rng, 1, .1))
    lay = glaze(lay, pigment_local(eye, centre, None, sd(), density=0.8, edge=0.6, bloom=0, rough=1.5))
    sh = shape_mask(W, H, deform(ellipse_pts(cx + r * .22, cy + r * .48, r * .78, r * .3, 9, -.3), rng, 2, .1)) * base
    lay = glaze(lay, pigment_local(sh, deep, None, sd(), density=0.2, edge=0.2, bloom=0.4, rough=6))
    return lay, base


def pigment_local(mask, a, b, seed, pad=30, **k):
    """pigment() computed in the mask bbox only, returned full size."""
    from _j1_lib import bbox as _bb
    if len(_art._fbm_cache) > 10:
        _art._fbm_cache.clear()
    h, w = mask.shape
    out = np.zeros((h, w, 4), np.float32)
    bb = _bb(mask, pad)
    if bb is None:
        return out
    y0, y1, x0, x1 = bb
    out[y0:y1, x0:x1] = pigment(np.ascontiguousarray(mask[y0:y1, x0:x1]), a, b, seed=seed, **k)
    return out


def opaque(rgb):
    return np.concatenate([np.clip(rgb, 0, 1), np.ones(rgb.shape[:2] + (1,), np.float32)], -1).astype(np.float32)


def kb_total(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")
