"""Agent M2 (batch 12) helpers: pamona-poso, tatreez-merah, venesia-kanal, ultah-pesulap.
Builds on _jw_lib (G/GP/LC/FO/OV crop painting, strokes/shapes/circles, hatch). Previews -> /tmp/pen/nb-M2/art.
Adds a stitch-by-stitch cross-stitch renderer and woven linen texture (tatreez)."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import art as _art

MPREV = "/tmp/pen/nb-M2/art"
os.makedirs(MPREV, exist_ok=True)


def prev(arr, name, bg="#f6efe2"):
    h, w = arr.shape[:2]
    if bg is None:
        on_paper(arr, "#f6efe2").save(f"{MPREV}/{name}.png")
        return
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{MPREV}/{name}.png")


def clear():
    _art._fbm_cache.clear()


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def soft(dst, mask, col, alpha=1.0, blur=0.0, pad=20):
    def fn(m):
        mm = gaussian_filter(m, blur) if blur else m
        return flat(mm, col, alpha)
    return OV(dst, mask, fn, pad=pad + int(blur * 3))


def ink(dst, mask, col, alpha=0.9, rough=1.0, seed=1):
    def fn(m):
        mm = displace(m, seed, rough, 14)
        h, w = mm.shape
        a = np.clip(mm * 1.25, 0, 1) * (0.8 + 0.2 * fbm(w, h, seed + 2, 20, 2)) * alpha
        return np.concatenate([flat(mm, col)[..., :3], a[..., None]], -1)
    return OV(dst, mask, fn, pad=8)


def opaque(arr, bg):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    return np.concatenate([rgb, np.ones((h, w, 1), np.float32)], -1)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def rects(W, H, items):
    """items: (x, y, w, h)"""
    return shapes(W, H, [[(x, y), (x + w, y), (x + w, y + h), (x, y + h)] for x, y, w, h in items], smooth=False)


def yy_xx(W, H):
    return np.mgrid[0:H, 0:W].astype(np.float32)


# ------------------------------------------------------------------ cross-stitch (tatreez)
def linen(W, H, tone="#efe6d2", seed=1, pitch=3.0, wrap=True):
    """Even-weave linen: warp/weft threads with slubs, opaque RGB float (H,W,3)."""
    rng = np.random.default_rng(seed)
    yy, xx = yy_xx(W, H)
    mode = "wrap" if wrap else "reflect"
    # thread brightness per column/row (slubs)
    col_v = gaussian_filter(rng.normal(0, 1, W).astype(np.float32), 0.8, mode=mode)
    row_v = gaussian_filter(rng.normal(0, 1, H).astype(np.float32), 0.8, mode=mode)
    warp = 0.5 + 0.5 * np.cos(xx / pitch * 2 * math.pi)
    weft = 0.5 + 0.5 * np.cos(yy / pitch * 2 * math.pi)
    over_ = ((np.floor(xx / pitch) + np.floor(yy / pitch)) % 2).astype(np.float32)
    tex = (warp * over_ + weft * (1 - over_)) * 0.6 + 0.4
    v = tex * (1 + 0.05 * col_v[None, :] * over_ + 0.05 * row_v[:, None] * (1 - over_))
    holes = (1 - warp) * (1 - weft)
    v = v - holes * 0.35
    mott = gaussian_filter(rng.random((H, W)).astype(np.float32), 40, mode=mode)
    mott = (mott - mott.min()) / (mott.max() - mott.min() + 1e-6)
    base = np.array(hex_rgb(tone), np.float32)
    rgb = base[None, None, :] * (0.86 + 0.16 * v[..., None]) * (0.97 + 0.05 * mott[..., None])
    return np.clip(rgb, 0, 1)


def parse_grid(rows, legend):
    """rows: list of strings; legend: char -> hex. Returns list of (col, row, hex)."""
    cells = []
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch in legend:
                cells.append((c, r, legend[ch]))
    return cells


def stitch_layer(W, H, cells, cell, ox=0.0, oy=0.0, seed=1, thick=0.42, shadow=True):
    """Render cross stitches: each cell gets two diagonal thread strokes (bottom leg / then top leg),
    each a little offset, with a twisted-floss sheen, a soft drop shadow into the linen. RGBA float."""
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    by_col = {}
    for c, r, col in cells:
        by_col.setdefault(col, []).append((c, r))
    out = blank(W, H)
    sh_all = np.zeros((H, W), np.float32)
    lw = cell * thick
    for col, cl in by_col.items():
        cv1 = Canvas(W, H)  # bottom legs  /
        cv2 = Canvas(W, H)  # top legs     \
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        for c, r in cl:
            x0 = ox + c * cell; y0 = oy + r * cell
            j = lambda: rng.uniform(-0.07, 0.07) * cell
            ins = cell * 0.16
            p.setStrokeWidth(lw * rng.uniform(0.85, 1.1))
            cv1.c.drawLine(x0 + ins + j(), y0 + cell - ins + j(), x0 + cell - ins + j(), y0 + ins + j(), p)
            p.setStrokeWidth(lw * rng.uniform(0.85, 1.1))
            cv2.c.drawLine(x0 + ins + j(), y0 + ins + j(), x0 + cell - ins + j(), y0 + cell - ins + j(), p)
        m1 = cv1.array()[..., 3]; m2 = cv2.array()[..., 3]
        base = np.array(hex_rgb(col), np.float32)
        yy, xx = yy_xx(W, H)
        for k, m in enumerate((m1, m2)):
            if not m.any():
                continue
            # floss twist: fine diagonal ridges along the stroke direction
            ang = (xx + yy) if k == 0 else (xx - yy)
            twist = 0.5 + 0.5 * np.sin(ang / max(1.6, cell * 0.16) * 2.2 + fbm(W, H, seed + k, 12, 2) * 2)
            # rounded thread: lighter centre, darker flanks
            core = gaussian_filter(m, max(0.6, lw * 0.22))
            shade = 0.62 + 0.38 * np.clip(core * 1.25, 0, 1) + 0.12 * (twist - 0.5)
            tone = 0.92 + 0.12 * gaussian_filter(nrng.random((H, W)).astype(np.float32), cell * 0.6)
            rgb = base[None, None, :] * (shade * tone)[..., None]
            hl = np.clip((core - 0.75) * 3, 0, 1) * twist * 0.22
            rgb = rgb + hl[..., None] * (1 - base[None, None, :]) * 0.8
            layer = np.concatenate([np.clip(rgb, 0, 1), np.clip(m * 1.05, 0, 1)[..., None]], -1)
            out = over(out, layer)
            sh_all = np.maximum(sh_all, m)
    if shadow:
        sh = np.roll(np.roll(gaussian_filter(sh_all, 1.4), 1, 0), 1, 1) * 0.35
        sh_layer = flat(sh * (1 - out[..., 3]), "#2a1a10")
        out = over(sh_layer, out)
    return out


def mirror_rows(rows):
    """Mirror each row horizontally around its last column (rows are left halves incl. centre)."""
    return [r + r[-2::-1] for r in rows]


def mirror_cols(rows):
    return rows + rows[-2::-1]


def star8(n):
    """Eight-point star (two overlapping squares, one rotated 45) on a (2n+1) grid; returns list of strings with 'R' fill,
    'D' outline-ish centre ring, 'G' centre."""
    size = 2 * n + 1
    out = []
    for r in range(size):
        row = ""
        for c in range(size):
            dx, dy = abs(c - n), abs(r - n)
            sq = max(dx, dy) <= int(n * 0.66)
            dia = dx + dy <= n
            if dx + dy <= 1:
                row += "G"
            elif (sq or dia) and max(dx, dy) <= int(n * 0.66) and dx + dy <= int(n * 0.66) + 1 and dx + dy >= int(n * 0.66) - 0:
                row += "K"
            elif sq or dia:
                row += "R"
            else:
                row += "."
        out.append(row)
    return out
