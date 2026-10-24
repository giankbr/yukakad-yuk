"""Agent S1 helpers (pasar-terapung, toska-syari, danau-angsa, ultah-pilot).
Builds on _a2_lib (which pulls in _j1_lib / _p1_lib / art). Previews -> /tmp/pen/nb-S1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-S1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def yx(W, H):
    return np.mgrid[0:H, 0:W].astype(np.float32)


def band(W, H, y0, y1, soft=20.0):
    yy = yx(W, H)[0]
    return np.clip((yy - y0) / soft + .5, 0, 1) * np.clip((y1 - yy) / soft + .5, 0, 1)


def fade_y(W, H, y0, y1):
    """1 above y0 -> 0 at y1 (or reverse if y1 < y0)."""
    yy = yx(W, H)[0]
    return np.clip((y1 - yy) / (y1 - y0), 0, 1)


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def ell(W, H, cx, cy, rx, ry, rot=0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def line(W, H, pts, width, taper=(0.15, 0.25)):
    return strokes(W, H, [(pts, width, taper)])


def save_prev(arr, name, tone="#fbf6ee", bg=None):
    preview(arr, name, tone=tone, bg=bg)
