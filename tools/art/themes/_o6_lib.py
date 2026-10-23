"""Agent O6 helpers (mawar-putih, tinta-kuas, sepeda-tandem, bazar-kuliner): _j1_lib local media + white garden roses,
bristle brush strokes, ink splatter, simple gouache scene blocks. Previews -> /tmp/pen/nb-O6/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-O6/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
from _jw_lib import along, hills, spiral_pts
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image

PREV = "/tmp/pen/nb-O6/art"


def clear():
    _art._fbm_cache.clear()


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
    """Flat-ish overlay (for highlights) with a little grain."""
    return OV(dst, mask, lambda m: solid_layer(m, col, alpha), pad=pad)


# ------------------------------------------------------------------ white garden rose (gouache + glaze)
def scallop(cx, cy, r, ry, n=40, k=5, amp=0.07, ph=0.0, rot=0.0):
    pts = []
    for i in range(n):
        t = i / n * math.tau
        rr = 1 + amp * abs(math.sin(k * t / 2 + ph))
        x, y = math.cos(t) * r * rr, math.sin(t) * ry * rr
        c, s_ = math.cos(rot), math.sin(rot)
        pts.append((cx + x * c - y * s_, cy + x * s_ + y * c))
    return pts


def _rim(m, px=1.3):
    return np.clip((m - gaussian_filter(m, px)) * 3.0, 0, 1)


def white_rose(art, W, H, cx, cy, r, rng, nx, tilt=0.86, rot=0.0, area=None, warm=0.5,
               white="#fdfbf5", cream="#eee7d3", shade="#a9b09a", deep="#6f7a62", heart="#9c9b74"):
    """Cupped white garden rose built back-to-front from petals: each petal gouache-white, glazed with cool
    grey-green shadow towards the cup, a soft pencil-thin edge, bright turned-back rims; light from top-left."""
    sh_col = mix(shade, "#c4b49a", warm * 0.45)
    L = (-0.62, -0.78)  # light direction (towards top-left)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + ((yy - cy) / tilt) ** 2) / r
    outline = deform(scallop(cx, cy, r, r * tilt, 44, 7, 0.08, rng.uniform(0, 3), rot), rng, 1, 0.02)
    base = shape_mask(W, H, outline)
    if area is not None:
        np.maximum(area, base, out=area)
    sh = np.clip(np.roll(np.roll(gaussian_filter(base, r * 0.1), int(r * 0.1), 0), int(r * 0.07), 1) * 1.3 - 0.12, 0, 1)
    art = G(art, sh, "#25332a", seed=nx(), density=0.35, edge=0.05, bloom=0, rough=3, feather=2)
    art = GP(art, base, mix(cream, sh_col, .2), mix(cream, sh_col, .45), seed=nx(), rough=1.6, streak=0.1, pad=10)
    ccx, ccy = cx, cy - r * (0.86 - tilt) * 0.9  # cup sits higher on a 3/4 view
    dist = np.sqrt((xx - ccx) ** 2 + ((yy - ccy) / tilt) ** 2) / r
    rings = [(0.58, 0.50, 0.36, 7, 0.0), (0.36, 0.38, 0.28, 6, 0.5), (0.18, 0.27, 0.2, 5, 1.0)]
    a0 = rng.uniform(0, math.tau)
    for ri, (dr, pa, pb, n, depth) in enumerate(rings):
        order = sorted(range(n), key=lambda k: math.sin(a0 + k / n * math.tau + ri))  # back (top) petals first
        for k in order:
            a = a0 + k / n * math.tau + ri * 0.45 + rng.uniform(-.18, .18)
            px, py = ccx + math.cos(a) * r * dr, ccy + math.sin(a) * r * dr * tilt
            sz = rng.uniform(0.85, 1.2)
            pm = shape_mask(W, H, deform(scallop(px, py, r * pa * sz, r * pb * sz, 30, 3, 0.06, rng.uniform(0, 3), a + math.pi / 2), rng, 2, 0.05)) * base
            lit = 0.5 + 0.5 * (math.cos(a) * L[0] + math.sin(a) * L[1])
            cast = np.clip(np.roll(np.roll(gaussian_filter(pm, r * 0.035), int(r * .025) + 1, 0), int(r * .02) + 1, 1) * 1.8 - pm * 1.4, 0, 1) * base
            art = G(art, cast, mix(sh_col, deep, .45), seed=nx(), density=0.55 + 0.2 * depth, edge=0.2, bloom=0, rough=1.5, feather=1.0, pad=10)
            art = GP(art, pm, mix(cream, white, 0.35 + 0.65 * lit), mix(cream, white, 0.15 + 0.5 * lit), seed=nx(), rough=1.2, streak=0.1, pad=8)
            # shadow pooling towards the cup (closer to centre = darker)
            cup = pm * np.clip(1.0 - (dist - dr * 0.4) / (pa * 1.1), 0, 1) ** 1.4
            art = G(art, cup, sh_col, mix(sh_col, deep, .3), seed=nx(), density=0.5 + 0.3 * depth + 0.3 * (1 - lit), edge=0.45, bloom=0.25, rough=2.5, feather=1.2, pad=8)
            art = G(art, _rim(pm, 1.2), mix(sh_col, deep, 0.35 + 0.3 * depth), seed=nx(), density=0.25 + 0.2 * (1 - lit), edge=0, bloom=0, rough=1.2, feather=0.6, pad=6)
            # bright rolled-back edge on the outer lip of the petal
            lip = arc_pts(px, py, r * pa * 0.88, a - 0.9, a + 0.9, 14, pb / pa)
            art = GP(art, stroke_mask(W, H, lip, r * 0.035) * pm, white, seed=nx(), rough=0.6, streak=0.1, density=0.85, pad=6)
    # the dark heart of the cup and the tight inner curls
    pit = shape_mask(W, H, deform(ellipse_pts(ccx + r * .02, ccy - r * .03, r * .2, r * .15, 10), rng, 2, .12))
    art = G(art, pit, mix(sh_col, deep, .6), deep, seed=nx(), density=0.75, edge=0.6, bloom=0.1, rough=2, pad=8)
    for k in range(4):
        rr = r * (0.14 - k * 0.025)
        a1 = rng.uniform(0, math.tau)
        pts = arc_pts(ccx + rng.gauss(0, r * .015), ccy - r * .03, rr, a1, a1 + rng.uniform(2.2, 3.4), 18, tilt)
        art = GP(art, stroke_mask(W, H, pts, r * 0.045), white, cream, seed=nx(), rough=0.6, streak=0.1, pad=6)
    art = G(art, shape_mask(W, H, ellipse_pts(ccx, ccy - r * .04, r * .05, r * .04, 8)), heart, seed=nx(), density=0.6, edge=0.4, bloom=0, rough=1, pad=6)
    # overall form shadow on the lower right
    side = base * np.clip(((xx - cx) * -L[0] + (yy - cy) * -L[1]) / (r * 1.0), 0, 1)
    art = G(art, side, sh_col, mix(sh_col, deep, .3), seed=nx(), density=0.5, edge=0.05, bloom=0.3, rough=4, pad=10)
    art = G(art, _rim(base, 1.5), deep, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.8, feather=0.4, pad=6)
    return art


def white_bud(art, W, H, x, y, s, ang, rng, nx, leaf_c=("#3f6b4c", "#1f3d2c")):
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 1.9, s * 0.8, ang, n=14), rng, 1, 0.05))
    art = G(art, np.roll(np.roll(gaussian_filter(m, 2), 3, 0), 2, 1), "#3b4a3a", seed=nx(), density=0.25, edge=0, bloom=0, rough=2, feather=1.5, pad=8)
    art = GP(art, m, "#faf6ec", "#e9e1cd", seed=nx(), rough=1.2, pad=8)
    spiral = arc_pts(x + math.cos(ang) * s * 1.0, y + math.sin(ang) * s * 1.0, s * 0.45, ang + 1.2, ang + 4.2, 16, 0.8)
    art = G(art, stroke_mask(W, H, spiral, s * 0.14) * m, "#a9ad94", seed=nx(), density=0.45, edge=0.5, bloom=0, rough=1, feather=0.7, pad=8)
    for side in (-1, 1):
        sep = shape_mask(W, H, petal_pts(x, y, s * 1.35, s * 0.22, ang + side * 0.42, n=10))
        art = G(art, sep, leaf_c[0], leaf_c[1], seed=nx(), density=0.8, edge=0.5, bloom=0, rough=1.5, pad=8)
    return art


def serr_leaf(x, y, L, wd, ang, rng, teeth=11, amp=0.022):
    """Serrated rose-leaf outline (small saw teeth along the edge)."""
    base = petal_pts(x, y, L, wd, ang, n=teeth * 4)
    n = len(base); out = []
    for i in range(n):
        a, b = base[i - 1], base[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nxn, nyn = dy / d, -dx / d
        k = L * amp * (1 if i % 2 else -0.4)
        out.append((base[i][0] + nxn * k, base[i][1] + nyn * k))
    return out


def rose_leaf(art, W, H, x, y, L, ang, rng, nx, c=("#3f6b4c", "#1c3a29"), hi="#7fa37c", area=None, dens=0.85):
    m = shape_mask(W, H, serr_leaf(x, y, L, L * 0.3, ang, rng), smooth=False)
    m = gaussian_filter(m, 0.5)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, c[0], c[1], seed=nx(), rough=1.4, streak=0.3, pad=10)
    art = G(art, m, mix(c[0], "#9fbf8f", .25), c[1], seed=nx(), density=0.5 * dens, edge=0.6, bloom=0.45, rough=2.5, pad=10)
    half = shape_mask(W, H, petal_pts(x, y, L * 0.95, L * 0.15, ang + 0.1, n=12)) * m
    art = G(art, half, c[1], seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=2, pad=10)
    lit = shape_mask(W, H, petal_pts(x, y, L * 0.9, L * 0.13, ang - 0.12, n=12)) * m
    art = G(art, lit, mix(c[0], "#a8c49a", .55), seed=nx(), density=0.35, edge=0.2, bloom=0.5, rough=3, pad=10)
    vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [j / 12 for j in range(1, 11)]]
    art = GP(art, stroke_mask(W, H, vein, max(1.2, L * 0.022)) * m, hi, seed=nx(), rough=0.6, streak=0.2, density=0.6, pad=8)
    return art


def rose_spray(art, W, H, pts, rng, nx, L=60, c=("#3f6b4c", "#1c3a29"), area=None, every=2, stem="#2c4a34"):
    """Stem with pinnate leaf sets (3 or 5 leaflets) along a curve."""
    art = G(art, strokes(W, H, [(pts, max(2.0, L * 0.06), (0.02, 0.4))]), stem, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1, feather=0.6)
    for j in range(4, len(pts) - 2, max(3, len(pts) // 5)):
        a = math.atan2(pts[j + 1][1] - pts[j - 1][1], pts[j + 1][0] - pts[j - 1][0])
        side = 1 if (j // 3) % 2 else -1
        art = rose_leaf(art, W, H, pts[j][0], pts[j][1], L * rng.uniform(0.75, 1.05), a + side * 0.75, rng, nx, c=c, area=area)
    ex, ey = pts[-1]
    a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    return rose_leaf(art, W, H, ex, ey, L * 1.1, a, rng, nx, c=c, area=area)


# ------------------------------------------------------------------ ink brush (bristles) + splatter
def bristle_mask(W, H, pts, width, rng, n=26, dry=0.35, taper=(0.12, 0.3), press=None, gap=0.5):
    """Sumi/brush-pen stroke: many parallel bristle lines; the tail breaks into dry streaks.
    press(t) -> width factor (default: quick attack, long body, lifted tail)."""
    cv = Canvas(W, H)
    N = len(pts)
    normals = []
    for i in range(N):
        a, b = pts[max(0, i - 1)], pts[min(N - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        normals.append((-dy / d, dx / d))
    if press is None:
        def press(t):
            if t < taper[0]:
                return 0.35 + 0.65 * (t / taper[0]) ** 0.6
            if t > 1 - taper[1]:
                return max(0.05, ((1 - t) / taper[1]) ** 0.8)
            return 1.0
    for b in range(n):
        off = (b / (n - 1)) * 2 - 1 if n > 1 else 0
        off += rng.gauss(0, 0.02)
        bw = width / n * rng.uniform(1.4, 2.6)
        load = rng.uniform(0.55, 1.0)          # how long this bristle keeps ink
        edge = abs(off)
        stop = 1 - dry * (1 - load) - dry * edge * rng.uniform(0.2, 0.9)
        nz = gaussian_filter(np.random.default_rng(rng.randint(0, 10**6)).random(N).astype(np.float32), max(1.0, N * 0.015))
        nz = (nz - nz.min()) / (nz.max() - nz.min() + 1e-6)
        prev = None
        for i in range(N):
            t = i / (N - 1)
            w = width * 0.5 * press(t)
            x = pts[i][0] + normals[i][0] * off * w
            y = pts[i][1] + normals[i][1] * off * w
            tail = min(1.0, max(0.0, (t - (stop - 0.35)) / 0.35))
            on = t < stop and nz[i] > tail * 0.85 * gap
            if prev and on:
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=max(0.6, bw * (1 - 0.55 * tail)), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(prev[0], prev[1], x, y, p)
            prev = (x, y)
    m = cv.array()[..., 3]
    # fill tiny gaps in the body so it reads as a loaded brush, keep streaks at the tail
    body = gaussian_filter(m, 0.9)
    return np.clip(np.maximum(m, (body - 0.35) * 2.0), 0, 1)


def ink(mask, col="#121212", seed=1, wet=0.4):
    """Sumi ink colouring: dense black with slightly lighter, wet pooled body and darker edge."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    inner = gaussian_filter(m, 6)
    rim = np.clip(m - inner, 0, 1)
    tone = 1 - wet * 0.25 * fbm(w, h, seed, 60, 3) * (1 - rim * 2)
    base = np.array(hex_rgb(col), np.float32)
    lift = np.array(hex_rgb("#3a3a3c"), np.float32)
    k = np.clip((1 - tone) * 3, 0, 1)[..., None]
    rgb = base * (1 - k) + lift * k
    a = np.clip(m * (0.9 + 0.1 * fbm(w, h, seed + 3, 8, 2)), 0, 1)
    return np.concatenate([rgb, a[..., None]], -1)


def INK(dst, mask, *a, pad=12, **k):
    return _j1_lib._apply(dst, mask, lambda m: ink(m, *a, **k), "over", pad)


def splatter(W, H, rng, cx, cy, spread, n=60, big=14, drip=True):
    """Ink splatter: a few big blots with satellite droplets flung outward, occasional elongated flecks."""
    items = []; ells = []
    for _ in range(n):
        a = rng.uniform(0, math.tau)
        d = abs(rng.gauss(0, spread))
        r = max(0.8, big * math.exp(-d / spread * 1.6) * rng.uniform(0.3, 1.0))
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.8
        if d > spread * 0.6 and rng.random() < 0.35:
            ells.append((x, y, r * 2.4, r * 0.6, math.degrees(a)))
        else:
            items.append((x, y, r))
    m = np.maximum(circles(W, H, items), ellipses(W, H, ells) if ells else 0)
    # a central blot built from overlapping blobs
    blot = shapes(W, H, [deform(ellipse_pts(cx + rng.gauss(0, big * .4), cy + rng.gauss(0, big * .4), big * rng.uniform(1.4, 2.4), big * rng.uniform(1.0, 1.8), 10, rng.uniform(0, 3)), rng, 3, 0.18) for _ in range(3)])
    return np.clip(np.maximum(m, blot), 0, 1)


# ------------------------------------------------------------------ gouache helpers for scenes
def gp_layer(art, mask, col, col2=None, seed=1, rough=2.0, streak=0.7, density=0.97, pad=12):
    return GP(art, mask, col, col2, seed=seed, rough=rough, streak=streak, density=density, pad=pad)


def soft(art, mask, col, seed, dens=0.3, pad=14):
    """Soft watercolour shading glaze."""
    return G(art, mask, col, seed=seed, density=dens, edge=0.2, bloom=0.3, rough=3, pad=pad)
