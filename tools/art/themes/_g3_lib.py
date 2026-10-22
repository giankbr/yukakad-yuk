"""Agent G3 helpers (kaili-souraja, tolaki-kendari, mezquita-cordoba, ultah-melukis): builds on _c1_lib (bbox-cropped
painting, gouache washes, textiles) and adds a few of my own: voussoir arches, splatters, crayon strokes.
Previews -> /tmp/pen/nb-G3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _c1_lib import *  # noqa
import _c1_lib, _b1_lib, _a1_lib, _p1_lib
import art as _art

PREV = "/tmp/pen/nb-G3/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_c1_lib, _b1_lib, _a1_lib, _p1_lib):
    _m.PREV = PREV


def clr():
    _art._fbm_cache.clear()


def show(arr, name, bg=None, tone="#f4ecdf"):
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * col_arr(bg)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def ann(cx, cy, r0, r1, a0, a1, n=40):
    """Annular sector polygon (angles in radians, y down)."""
    outer = [(cx + math.cos(a0 + (a1 - a0) * i / (n - 1)) * r1, cy + math.sin(a0 + (a1 - a0) * i / (n - 1)) * r1) for i in range(n)]
    inner = [(cx + math.cos(a1 - (a1 - a0) * i / (n - 1)) * r0, cy + math.sin(a1 - (a1 - a0) * i / (n - 1)) * r0) for i in range(n)]
    return outer + inner


def splat(W, H, x, y, r, rng, drops=10, spikes=9):
    """Paint splatter blob: irregular core with spiky arms and satellite drops (list of polys + circles mask)."""
    pts = []
    n = 28
    spk = {rng.randrange(n): rng.uniform(1.3, 2.1) for _ in range(spikes)}
    for i in range(n):
        a = i / n * math.tau
        k = spk.get(i, rng.uniform(0.82, 1.08))
        pts.append((x + math.cos(a) * r * k, y + math.sin(a) * r * k))
    m = shapes(W, H, [deform(pts, rng, 2, 0.06)])
    cs = []
    for _ in range(drops):
        a = rng.uniform(0, math.tau); d = r * rng.uniform(1.3, 2.6)
        cs.append((x + math.cos(a) * d, y + math.sin(a) * d, r * rng.uniform(0.05, 0.16)))
    return np.clip(m + circles(W, H, cs), 0, 1)


def crayon(W, H, pts, width, seed=1, grain=0.55):
    """Waxy crayon stroke mask: a stroke broken up by paper tooth (fine high-frequency holes)."""
    m = strokes(W, H, [(pts, width, (0.05, 0.1))])
    tooth = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.7)
    tooth = (tooth - tooth.min()) / (np.ptp(tooth) + 1e-6)
    streak = gaussian_filter(np.random.default_rng(seed + 1).random((H, W)).astype(np.float32), (0.4, 2.5))
    streak = (streak - streak.min()) / (np.ptp(streak) + 1e-6)
    keep = np.clip((tooth * 0.6 + streak * 0.4 - grain * 0.6) * 4, 0, 1)
    return m * keep


def palm2(W, H, x, by, h, rng, lean=0.1, fronds=11):
    """Coconut palm mask with real leaflets: tapered curved trunk, arching fronds whose leaflets hang down."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.15, by - h * 0.4), (x + lean * h * 0.6, by - h * 0.8), top], 40)
    items = [(trunk, h * 0.04, (0.0, 0.9))]
    for k in range(fronds):
        a = -math.pi / 2 + (k - (fronds - 1) / 2) * (2.9 / fronds) + rng.uniform(-0.12, 0.12)
        L = h * rng.uniform(0.34, 0.48)
        droop = L * (0.25 + 0.5 * abs(math.cos(a)))
        pts = curve([top, (top[0] + math.cos(a) * L * 0.45, top[1] + math.sin(a) * L * 0.45 - h * 0.03),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + droop)], 30)
        items.append((pts, h * 0.012, (0.0, 0.6)))
        for j in range(2, len(pts) - 1):
            px, py = pts[j]; t = j / len(pts)
            dx, dy = pts[j + 1][0] - pts[j - 1][0], pts[j + 1][1] - pts[j - 1][1]
            d = math.hypot(dx, dy) or 1
            ll = L * 0.26 * (1 - t * 0.7)
            for sgn in (-1, 1):
                nxv, nyv = -dy / d * sgn, dx / d * sgn
                ex, ey = px + (nxv * 0.55 + dx / d * 0.45) * ll, py + (nyv * 0.55 + dy / d * 0.45) * ll + ll * 0.6
                items.append(([(px, py), ((px + ex) / 2, (py + ey) / 2 - ll * 0.05), (ex, ey)], h * 0.009, (0.0, 0.8)))
    # coconuts
    m = strokes(W, H, items)
    nuts = circles(W, H, [(top[0] + rng.uniform(-6, 6) * h / 300, top[1] + h * 0.03 + rng.uniform(0, 6) * h / 300, h * 0.022) for _ in range(4)])
    return np.clip(m + nuts, 0, 1)
