"""Agent N1 helpers (rumah-limas, sidomukti-solo, mint-syari, ultah-ninja). Builds on _jw_lib (G/GP/LC/FO/OV, strokes,
shapes, circles, ellipses, flora, carve, lung, along ...). Previews -> /tmp/pen/nb-N1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-N1/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, a=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask * a)


def dilate(mask, r):
    return np.clip(gaussian_filter(mask, r) * 3.0, 0, 1) if r > 0 else mask


def erode(mask, r):
    return np.clip((gaussian_filter(mask, r) - 0.66) * 3.0, 0, 1)


def edge_ring(mask, r=1.2):
    return np.clip((mask - gaussian_filter(mask, r)) * 3, 0, 1)


def rot(pts, cx, cy, a):
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def poly(*pts):
    return list(pts)


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def relief(art, W, H, m, light, base, dark, nx, gold=None, gold_amt=0.0, wear_seed=3, depth=2):
    """Raised carved relief on an existing ground: gouache body, top-left highlight, bottom-right shadow, worn gold."""
    art = GP(art, m, light, base, seed=nx(), rough=1.0, streak=0.6, pad=10)
    lo = np.clip(m - np.roll(np.roll(m, -depth, 0), -depth, 1), 0, 1)
    hi = np.clip(m - np.roll(np.roll(m, depth, 0), depth, 1), 0, 1)
    art = G(art, lo, dark, seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    sh = np.clip(np.roll(np.roll(m, depth + 1, 0), depth + 1, 1) - m, 0, 1)
    art = G(art, sh, dark, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6, feather=0.8)
    art = OV(art, hi, lambda q: flat(q, mix(light, "#fff4da", 0.55), 0.5))
    if gold:
        wear = fbm(W, H, wear_seed, 12, 3)
        gm = m * np.clip((wear - (1 - gold_amt)) * 4, 0, 1)
        art = FO(art, gm, gold, seed=nx(), emboss=0.5, sparkle=0.15)
    return art


def tile_items(items, W, H):
    out = []
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            for it in items:
                out.append(([(x + dx, y + dy) for x, y in it[0]],) + tuple(it[1:]))
    return out


def tile_polys(polys, W, H):
    return [[(x + dx, y + dy) for x, y in p] for dx in (-W, 0, W) for dy in (-H, 0, H) for p in polys]


# ---------------------------------------------------------------- dense gilded carving (Palembang lakuer style)
def vine(path, s, rng, every=1.0, curl=True, flower_every=0):
    """Leafy carved vine along a polyline: alternating cupped leaves with veins, curled tendrils, optional flowers.
    Returns dict(stem=[items], leaves=[(poly, vein)], curls=[items], flowers=[(x, y, r)])."""
    out = dict(stem=[(path, s * 0.16, (0.08, 0.08))], leaves=[], curls=[], flowers=[])
    pts = along(path, s * 0.55 * every)
    for k, (x, y, a) in enumerate(pts):
        side = 1 if k % 2 else -1
        L = s * rng.uniform(0.7, 1.0)
        la = a + side * rng.uniform(0.7, 1.1)
        poly_ = petal_pts(x, y, L, L * 0.36, la, n=12, cup=side * 0.25)
        vein = [(x + math.cos(la) * L * t, y + math.sin(la) * L * t) for t in (0.1, 0.35, 0.6, 0.8)]
        out["leaves"].append((poly_, vein))
        if curl and k % 3 == 1:
            ca = a - side * 0.9
            sx, sy = x + math.cos(ca) * s * 0.2, y + math.sin(ca) * s * 0.2
            sp = spiral_pts(sx + math.cos(ca) * s * 0.3, sy + math.sin(ca) * s * 0.3, s * 0.3, s * 0.05, ca + math.pi, 0.9, 20, side)
            out["curls"].append(([(x, y)] + sp, s * 0.08, (0.0, 0.6)))
        if flower_every and k % flower_every == flower_every // 2:
            out["flowers"].append((x + math.cos(a - side * 1.4) * s * 0.4, y + math.sin(a - side * 1.4) * s * 0.4, s * 0.38))
    return out


def lotus_polys(cx, cy, r, n=8, rot0=0.0):
    """Layered carved rosette: outer petals, offset inner petals, heart. Returns list of (polys, kind)."""
    outer = [petal_pts(cx, cy, r, r * 0.5, rot0 + k * math.tau / n, n=12) for k in range(n)]
    inner = [petal_pts(cx, cy, r * 0.62, r * 0.36, rot0 + (k + 0.5) * math.tau / n, n=10) for k in range(n)]
    return outer, inner


def gild(art, W, H, parts, nx, ground=None, gold=None, gold2=None, cut="#2a120c", shadow="#1a0a06", glaze_col=None, scale=1.0):
    """Paint carved gilded relief from parts=dict(stem, leaves, curls, flowers) (lists can be merged from several
    vines). Leaves are painted in two passes so overlaps read; every piece gets a cast shadow, foil body, dark cut edge
    and an engraved vein; optional red lacquer glaze in the hollows."""
    gold = gold or "#d4a343"; gold2 = gold2 or "#c4893a"
    ground = np.ones((H, W), np.float32) if ground is None else ground
    lw = max(0.8, 1.1 * scale)
    stems = strokes(W, H, parts.get("stem", []) + parts.get("curls", [])) * ground if (parts.get("stem") or parts.get("curls")) else np.zeros((H, W), np.float32)
    leaves = parts.get("leaves", [])
    groups = [leaves[0::2], leaves[1::2]]
    fl_outer, fl_inner, hearts = [], [], []
    for (x, y, r) in parts.get("flowers", []):
        o, i = lotus_polys(x, y, r, 8, (x * 0.13) % 1)
        fl_outer += o; fl_inner += i; hearts.append((x, y, r * 0.24))
    allm = stems.copy()
    masks = [("stem", stems)]
    for gi, grp in enumerate(groups):
        if grp:
            m = shapes(W, H, [p for p, _ in grp]) * ground
            masks.append((f"leaf{gi}", m)); allm = np.maximum(allm, m)
    if fl_outer:
        mo = shapes(W, H, fl_outer) * ground; mi = shapes(W, H, fl_inner) * ground; mh = circles(W, H, hearts) * ground
        masks += [("fo", mo), ("fi", mi), ("fh", mh)]; allm = np.maximum(allm, mo)
    sh = np.clip(np.roll(np.roll(dilate(allm, 0.9 * scale), int(3 * scale), 0), int(2 * scale), 1) - allm * 0.7, 0, 1)
    art = G(art, sh, shadow, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.8, feather=1.0)
    for name, m in masks:
        if m.max() < 0.01:
            continue
        base = gold2 if name in ("leaf1", "fi") else gold
        art = FO(art, m, base, seed=nx(), emboss=0.9, sparkle=0.15)
        art = G(art, edge_ring(m, 1.0 * scale), cut, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.4, feather=0.4)
        if name.startswith("leaf"):
            grp = groups[int(name[-1])]
            vm = strokes(W, H, [(v, lw, (0.1, 0.6)) for _, v in grp]) * m
            art = G(art, vm, cut, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3, feather=0.3)
        if name == "fh":
            art = G(art, m, "#7a1a14", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.4)
    if glaze_col:
        hol = np.clip(gaussian_filter(allm, 2.5 * scale) - allm, 0, 1) * 1.5
        art = G(art, np.clip(hol, 0, 1) * ground, glaze_col, seed=nx(), density=0.4, edge=0, bloom=0.2, rough=1)
    return art, allm


def merge(*ps):
    out = dict(stem=[], leaves=[], curls=[], flowers=[])
    for p in ps:
        for k in out:
            out[k] += p.get(k, [])
    return out
