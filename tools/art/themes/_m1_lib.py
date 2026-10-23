"""Agent M1 helpers (manik-kenyah, tuban-gedog, terakota-syari, ultah-serangga): bead-by-bead renderer, coarse
handspun weave, frayed cloth edges, clay/plaster texture, small motif geometry. Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses ...). Previews -> /tmp/pen/nb-M1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-M1/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col):
    """Plain colour layer from a mask (for building blocks that get textured later)."""
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask)


def mirror_mask(m):
    return np.maximum(m, m[:, ::-1])


# ---------------------------------------------------------------- beads
def bead_grid(W, H, px, py, stagger=True, margin=0):
    """Bead centres on a netted grid (every other row offset by half a bead). Returns list of (x, y, row, col)."""
    out = []
    rows = int((H - 2 * margin) // py)
    for r in range(rows):
        y = margin + py / 2 + r * py
        off = (px / 2 if (stagger and r % 2) else 0)
        cols = int((W - 2 * margin - off) // px)
        for c in range(cols):
            out.append((margin + off + px / 2 + c * px, y, r, c))
    return out


def sample(mask, x, y):
    h, w = mask.shape
    xi, yi = int(round(x)), int(round(y))
    if 0 <= xi < w and 0 <= yi < h:
        return float(mask[yi, xi])
    return 0.0


def render_beads(W, H, beads, seed=1, thread="#17110d", ground=True, gloss=0.55, size=(0.94, 0.84), wob=0.7):
    """beads: list of (x, y, hex) -> RGBA canvas with every bead painted: body, ring shading, glass highlight,
    hole shadow, slight size/colour/position jitter; dark thread shows in the gaps."""
    rng = random.Random(seed)
    cv = Canvas(W, H, seed)
    c = cv.c
    if ground:
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=color(thread, 1.0)))
    for (x, y, bw, bh, hx) in beads:
        x += rng.gauss(0, wob); y += rng.gauss(0, wob * 0.6)
        sw = bw * size[0] * rng.uniform(0.9, 1.06); sh = bh * size[1] * rng.uniform(0.92, 1.05)
        base = jitter_hex(hx, rng, 0.035)
        r, g, b = hex_rgb(base)
        lite = skia.Color4f(min(1, r * 1.18 + 0.12), min(1, g * 1.18 + 0.12), min(1, b * 1.18 + 0.12), 1)
        dark = skia.Color4f(r * 0.52, g * 0.5, b * 0.5, 1)
        rect = skia.Rect(x - sw / 2, y - sh / 2, x + sw / 2, y + sh / 2)
        # soft contact shadow
        c.drawRRect(skia.RRect.MakeRectXY(rect.makeOffset(0.6, 1.0), sw * 0.42, sh * 0.46),
                    skia.Paint(AntiAlias=True, Color4f=skia.Color4f(0, 0, 0, 0.45), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.9)))
        sh_ = skia.GradientShader.MakeRadial(skia.Point(x - sw * 0.16, y - sh * 0.2), max(sw, sh) * 0.72,
                                             [lite, skia.Color4f(r, g, b, 1), dark], [0.0, 0.55, 1.0])
        c.drawRRect(skia.RRect.MakeRectXY(rect, sw * 0.42, sh * 0.46), skia.Paint(AntiAlias=True, Shader=sh_))
        # hole seen end-on is hidden; a faint thread groove runs horizontally through the bead middle
        c.drawLine(x - sw * 0.5, y + sh * 0.06, x + sw * 0.5, y + sh * 0.06,
                   skia.Paint(AntiAlias=True, Color4f=skia.Color4f(r * 0.45, g * 0.45, b * 0.45, 0.25), StrokeWidth=max(0.6, sh * 0.08)))
        # glass glint
        if gloss:
            gx, gy = x - sw * 0.2 + rng.gauss(0, 0.4), y - sh * 0.24
            c.drawOval(skia.Rect(gx - sw * 0.17, gy - sh * 0.1, gx + sw * 0.17, gy + sh * 0.1),
                       skia.Paint(AntiAlias=True, Color4f=skia.Color4f(1, 1, 1, gloss * rng.uniform(0.6, 1.0)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.5)))
    a = cv.array()
    return a


def bead_pattern(W, H, px, py, layers, bg, seed=1, stagger=True, margin=0, keep=None):
    """layers: list of (mask, hex) highest priority first; bg hex (None = no bead). keep: optional mask of where beads
    exist at all (outside = transparent). Returns RGBA."""
    beads = []
    for (x, y, r, c) in bead_grid(W, H, px, py, stagger, margin):
        if keep is not None and sample(keep, x, y) < 0.5:
            continue
        hx = bg
        for m, col in layers:
            if sample(m, x, y) > 0.5:
                hx = col
                break
        if hx:
            beads.append((x, y, px, py, hx))
    return render_beads(W, H, beads, seed=seed, ground=False)


def dilate(mask, r):
    return np.clip(gaussian_filter(mask, r) * 3.0, 0, 1) if r > 0 else mask


def outline(mask, r):
    """Ring around a mask (mask grown by r minus the mask)."""
    g = (gaussian_filter((mask > 0.5).astype(np.float32), r) > 0.08).astype(np.float32)
    return np.clip(g - (mask > 0.5), 0, 1)


# ---------------------------------------------------------------- cloth
def handspun(w, h, seed, tone="#e6dcc4", warp=3.2, weft=3.0, slub=0.9, dark="#8d7b5f"):
    """Coarse handspun cotton plain weave (tenun gedog): uneven thread thickness, slubs, tone drift; seamless."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # per-thread thickness / tone (wrap-around so the tile repeats)
    nw = int(round(w / warp)); nf = int(round(h / weft))
    tw = rng.normal(0, 1, nw); tf = rng.normal(0, 1, nf)
    cw = np.floor(xx / w * nw).astype(int) % nw; cf = np.floor(yy / h * nf).astype(int) % nf
    phx = (xx / w * nw) % 1.0; phy = (yy / h * nf) % 1.0
    over_ = ((cw + cf) % 2 == 0)
    ridge_w = np.clip(np.cos((phx - 0.5) * math.pi), 0, 1) ** 1.2
    ridge_f = np.clip(np.cos((phy - 0.5) * math.pi), 0, 1) ** 1.2
    ridge = np.where(over_, ridge_w * (0.75 + 0.25 * ridge_f), ridge_f * (0.75 + 0.25 * ridge_w))
    tone_t = np.where(over_, tw[cw], tf[cf]) * 0.05
    s = wrap_noise(w, h, seed + 3, (0.8, 6)) - 0.5
    s2 = wrap_noise(w, h, seed + 4, (6, 0.8)) - 0.5
    big = wrap_noise(w, h, seed + 5, 30) - 0.5
    v = 0.80 + 0.26 * ridge + tone_t + (s + s2) * 0.18 * slub + big * 0.08
    gap = (1 - ridge_w * ridge_f) ** 6
    base = col3(tone)[None, None, :] * v[..., None]
    base = base * (1 - gap[..., None] * 0.35) + col3(dark) * gap[..., None] * 0.35
    # stray fibre flecks
    fl = (rng.random((h, w)) > 0.9975).astype(np.float32)
    fl = gaussian_filter(fl, (0.4, 1.4)) * 2.5
    base = base * (1 - np.clip(fl, 0, 0.35)[..., None])
    return np.clip(base, 0, 1).astype(np.float32)


def weave_shade(h, w, seed, warp=3.2, weft=3.0, amt=1.0):
    """Multiplicative thread relief (same structure as handspun, neutral) to texture dyed cloth."""
    t = handspun(w, h, seed, "#ffffff", warp, weft, dark="#777777")
    lum = t.mean(-1)
    return (1 + (lum / lum.mean() - 1) * amt).astype(np.float32)


def fray(mask, seed, amount=5.0, fibres=0.6):
    """Frayed cloth edge: ragged threshold + loose thread hairs sticking out."""
    h, w = mask.shape
    n = fbm(w, h, seed, 6, 2)
    soft = gaussian_filter(mask, amount * 0.6)
    m = np.clip((soft - 0.35 - (n - 0.5) * 0.5) * 6, 0, 1)
    rng = random.Random(seed)
    edge = np.argwhere((soft > 0.2) & (soft < 0.5))
    items = []
    for _ in range(int(len(edge) * 0.004 * fibres)):
        y, x = edge[rng.randrange(len(edge))]
        a = rng.uniform(0, math.tau); L = rng.uniform(4, 12)
        items.append(([(x, y), (x + math.cos(a) * L * 0.5 + rng.gauss(0, 1), y + math.sin(a) * L * 0.5 + rng.gauss(0, 1)), (x + math.cos(a) * L, y + math.sin(a) * L)], 0.9, (0.0, 0.6)))
    if items:
        m = np.maximum(m, strokes(w, h, items) * 0.85)
    return m


# ---------------------------------------------------------------- plaster / clay
def plaster(w, h, tone, seed, amt=1.0, wrap=True):
    """Lime plaster / clay wall: trowel swirls, pores, mottle. Opaque RGB float, seamless when wrap."""
    nz = (lambda s, sg: wrap_noise(w, h, s, sg)) if wrap else (lambda s, sg: (lambda a: (a - a.min()) / (a.max() - a.min() + 1e-6))(gaussian_filter(np.random.default_rng(s).random((h, w)).astype(np.float32), sg)))
    big = nz(seed, 46) - 0.5
    mid = nz(seed + 1, 9) - 0.5
    fine = nz(seed + 2, 0.8) - 0.5
    trowel = nz(seed + 3, (2.5, 16)) - 0.5
    pores = (nz(seed + 4, 0.7) > 0.86).astype(np.float32) * 0.5
    v = 1 + (big * 0.10 + mid * 0.06 + fine * 0.05 + trowel * 0.05 - pores * 0.06) * amt
    return np.clip(col3(tone)[None, None] * v[..., None], 0, 1).astype(np.float32)


def clay_shade(mask, base, light, dark, seed, lx=-0.6, ly=-0.8, depth=6.0):
    """Gouache terracotta volume: base clay with a directional light from the mask's gradient + speckle."""
    h, w = mask.shape
    m = gaussian_filter(mask, depth)
    gy, gx = np.gradient(m)
    l = np.clip(0.5 - (gx * lx + gy * ly) * depth * 6, 0, 1)
    rgb = col3(base) * (1 - np.abs(l - 0.5)[..., None] * 0)
    rgb = np.where(l[..., None] > 0.5, rgb * (2 - 2 * l[..., None]) + col3(light) * (2 * l[..., None] - 1), rgb * (2 * l[..., None]) + col3(dark) * (1 - 2 * l[..., None]))
    sp = fbm(w, h, seed, 3, 2)
    rgb = rgb * (0.94 + 0.12 * sp[..., None])
    return rgb


def diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
