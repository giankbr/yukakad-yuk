"""Agent R1 helpers: re-exports _p1_lib with previews in /tmp/pen/nt3-R1/art."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nt3-R1/art"
import os
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _p1_lib import *  # noqa
PREV = _p1_lib.PREV


def brick_field(w, h, seed, row=7.0, brick=19.0, joint=1.1):
    """Staggered brick joints + per-brick tone (both slightly wobbly)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx_ = (fbm(w, h, seed, 30, 2) - 0.5) * 2.2
    ny_ = (fbm(w, h, seed + 1, 30, 2) - 0.5) * 1.6
    y = yy + ny_; x = xx + nx_
    r = np.floor(y / row)
    xo = x + (r % 2) * brick * 0.5 + r * 3.1
    c = np.floor(xo / brick)
    hj = np.clip(1 - np.abs((y % row) - 0.0) / joint, 0, 1) + np.clip(1 - np.abs((y % row) - row) / joint, 0, 1)
    vj = np.clip(1 - np.abs((xo % brick)) / joint, 0, 1) + np.clip(1 - np.abs((xo % brick) - brick) / joint, 0, 1)
    joints = np.clip(hj + vj, 0, 1)
    rnd = np.random.default_rng(seed + 2).random(4096).astype(np.float32)
    tone = rnd[((r * 131 + c * 17).astype(np.int64)) % 4096]
    return joints, tone


# keep memory bounded: art.fbm caches every (size, seed) field forever
import art as _art
_over, _glaze = over, glaze


def _trim():
    if len(_art._fbm_cache) > 12:
        _art._fbm_cache.clear()


def over(dst, src):  # noqa: F811
    _trim()
    return _over(dst, src)


def glaze(dst, src):  # noqa: F811
    _trim()
    return _glaze(dst, src)
