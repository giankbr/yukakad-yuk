"""Agent R2 helpers: _p3_common (travel painters, stamps) + a few _p2_lib tiles; previews to /tmp/pen/nt3-R2."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p3_common import *  # noqa
import _p2_lib as p2
gou, pig, lino, local, kbsize = p2.gou, p2.pig, p2.lino, p2.local, p2.kb
paper_tile, newsprint_tile, halftone_tile, dots_scatter = p2.paper_tile, p2.newsprint_tile, p2.halftone_tile, p2.dots
PREV = "/tmp/pen/nt3-R2"
os.makedirs(PREV, exist_ok=True)


def palm(W, H, x, y, h, lean, rng, nxt, trunk="#9a6a44", leaf=("#2f8a5c", "#1f6b47"), fronds=7):
    """Gouache coconut palm: curved banded trunk + drooping fronds (comma strokes). Returns (art, mask)."""
    art = blank(W, H)
    top = (x + lean * h, y - h)
    pts = curve([(x, y), (x + lean * h * 0.25, y - h * 0.45), (x + lean * h * 0.7, y - h * 0.82), top], 40)
    tm = np.zeros((H, W), np.float32)
    for i in range(len(pts) - 1):
        t = i / (len(pts) - 1)
        tm = np.maximum(tm, stroke_mask(W, H, [pts[i], pts[i + 1]], h * (0.075 - 0.03 * t), (0, 0)))
    art = over(art, gouache_obj(tm, trunk, mix(trunk, "#000000", .25), seed=nxt(), light=(-1, 0), k=0.3, blur=3))
    for i in range(1, 9):
        p = pts[int(len(pts) * i / 9)]
        band = stroke_mask(W, H, [(p[0] - h * .035, p[1]), (p[0] + h * .035, p[1] + h * .006)], 1.6, (0, 0)) * tm
        art = over(art, gouache_paint(band, mix(trunk, "#000000", .4), seed=nxt(), rough=0.4, streak=0))
    lm = np.zeros((H, W), np.float32)
    for k in range(fronds):
        a = -math.pi / 2 + (k - (fronds - 1) / 2) * (2.6 / fronds) + rng.uniform(-.15, .15)
        L = h * rng.uniform(0.42, 0.55)
        droop = 0.25 + 0.75 * abs(math.cos(a))
        fr = [(top[0] + math.cos(a) * L * t, top[1] + math.sin(a) * L * t + droop * L * t * t) for t in np.linspace(0, 1, 14)]
        m = stroke_mask(W, H, fr, h * 0.03, (0.05, 0.6))
        # leaflets: short strokes along the frond
        for j in range(2, 13):
            px, py = fr[j]; qx, qy = fr[j - 1]
            ang = math.atan2(py - qy, px - qx)
            for sgn in (-1, 1):
                ll = h * 0.12 * (1 - j / 18) * rng.uniform(0.8, 1.15)
                e = (px + math.cos(ang + sgn * 0.75) * ll, py + math.sin(ang + sgn * 0.75) * ll + ll * 0.75)
                mid = ((px + e[0]) / 2, (py + e[1]) / 2 + ll * 0.08)
                m = np.maximum(m, stroke_mask(W, H, [(px, py), mid, e], h * 0.016, (0, 0.75)))
        col = leaf[k % 2]
        art = over(art, gouache_obj(m, col, mix(col, "#0d3b26", .3), seed=nxt(), light=(-0.5, -1), k=0.25, blur=3))
        lm = np.maximum(lm, m)
    nuts = dots_mask(W, H, [(top[0] + dx, top[1] + dy, h * 0.03) for dx, dy in ((-h * .03, h * .03), (h * .02, h * .04), (0, h * .02))])
    art = over(art, gouache_obj(nuts, "#6b4a2a", seed=nxt(), k=0.3, blur=2))
    return art, np.clip(tm + lm + nuts, 0, 1)
