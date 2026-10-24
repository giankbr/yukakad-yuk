"""Agent S2 helpers (lurik-klaten, burgundy-syari, ayunan-pohon, ultah-sepeda): _j1_lib local-crop media +
gouache-with-pencil-line painting, woven-stripe cloth, dried flowers. Previews -> /tmp/pen/nb-S2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-S2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
from _jw_lib import along, hills, spiral_pts, palm  # noqa
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image

PREV = "/tmp/pen/nb-S2/art"


def clear():
    _art._fbm_cache.clear()


def rs():
    return random.randint(1, 10 ** 6)


def prev(arr, name, bg=None, tone="#f8f4ea"):
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def kb(d):
    t = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(f"{d}/{f}"); t += s
        print(f"  {f:22s} {s // 1024:4d} KB")
    print("TOTAL", t // 1024, "KB")


def solid_layer(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def tint(dst, mask, col, alpha=1.0, pad=8):
    return OV(dst, mask, lambda m: solid_layer(m, col, alpha), pad=pad)


def line(art, mask, px=1.4, dens=0.7, col="#4a3a32"):
    """Coloured-pencil outline around a painted shape."""
    rim = np.clip((mask - gaussian_filter(mask, px)) * 3.2, 0, 1)
    return G(art, rim, col, seed=rs(), density=dens, edge=0, bloom=0, rough=0.8, feather=0.35, pad=6)


def paint(art, mask, col, col2=None, ln=True, streak=0.7, px=1.4, dens=0.7, lc="#4a3a32", rough=1.6):
    art = GP(art, mask, col, col2 or mix(col, "#000000", .12), seed=rs(), rough=rough, streak=streak, pad=10)
    return line(art, mask, px, dens, lc) if ln else art


def shade(art, mask, col, d=0.35, rough=3):
    return G(art, mask, col, seed=rs(), density=d, edge=0.25, bloom=0.3, rough=rough, pad=10)


def light_side(mask, dx, dy, blur=4):
    """Part of mask facing away from offset (dx,dy): use for rim light / shadow sides."""
    sh = np.roll(np.roll(gaussian_filter(mask, blur), dy, 0), dx, 1)
    return np.clip(mask - sh, 0, 1)


def blob(W, H, cx, cy, rx, ry, rng, n=12, rot=0.0, var=0.1):
    return shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, n, rot), rng, 2, var)])


def opaque(arr):
    out = arr.copy(); out[..., 3] = 1.0
    return out


# ---------------------------------------------------------------- woven stripes (lurik)
def lurik_cloth(W, H, stripes, seed=1, weft="#e9dcc2", slub=0.35, angle=0.0):
    """Hand-loom (ATBM) striped cloth. stripes = list of (width_px, hex) repeated across x (warp stripes).
    Thread-level: each warp thread is a column with its own tone; weft picks cross it; slubs and uneven beat."""
    rng = np.random.default_rng(seed)
    # assign colour per x column from the stripe sequence
    seq = []
    for wd, col in stripes:
        seq += [col] * int(wd)
    cols = np.array([hex_rgb(c) for c in seq], np.float32)
    xs = np.arange(W)
    warp = cols[xs % len(seq)]                              # (W,3)
    thread = 1 + (rng.random(W).astype(np.float32) - 0.5) * 0.16  # per-thread tone
    warp = warp * thread[:, None]
    img = np.repeat(warp[None, :, :], H, 0)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # weft picks (rows): alternating over/under = checker at 1-px scale, softened
    pick = ((xx.astype(int) + yy.astype(int)) % 2).astype(np.float32)
    wf = np.array(hex_rgb(weft), np.float32)
    beat = 1 + (np.repeat(rng.random((H, 1)).astype(np.float32), W, 1) - 0.5) * 0.12  # uneven beating per row
    mixk = 0.22 * pick
    img = img * (1 - mixk[..., None]) + wf * mixk[..., None]
    img = img * beat[..., None]
    # thread relief: each thread is rounded (darker at the edges every 2 px)
    rel = 0.93 + 0.07 * np.cos((xx % 2) * math.pi) * np.cos((yy % 2) * math.pi)
    img = img * rel[..., None]
    # slubs: thick irregular weft bits
    sl = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.4, 6))
    sl = (sl - sl.min()) / (sl.max() - sl.min() + 1e-6)
    img = img * (1 + slub * 0.25 * np.clip((sl - 0.7) * 4, 0, 1)[..., None])
    # broad mottle (dye unevenness)
    mot = fbm(W, H, seed + 3, 90, 3)
    img = img * (0.94 + 0.1 * mot[..., None])
    return np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def tile_x(arr):
    """Make a texture horizontally seamless by cross-fading the edges."""
    h, w = arr.shape[:2]
    k = w // 8
    out = arr.copy()
    t = np.linspace(0, 1, k, dtype=np.float32)[None, :, None]
    out[:, :k] = arr[:, :k] * t + arr[:, w - k:] * (1 - t)
    return out[:, : w - k]
