"""Rustic Kayu — gouache baby's breath on watercolour stems, a painted twine bow & divider, painted plank + kraft fibre textures.
Run: python3 -I /tmp/pen/art/themes/rustic-kayu.py
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from agentA_lib import *  # noqa

D = f"{OUT}/rustic-kayu"
P = "/tmp/pen/nt2-A"
os.makedirs(D, exist_ok=True)
KRAFT = "#d3b48a"
STEM = "#86956a"
TWINE = "#a9834f"


def wrapn(rng, shape, s):
    a = gaussian_filter(rng.random(shape).astype(np.float32), s, mode="wrap")
    return (a - a.mean()) / (a.std() + 1e-6)


def floret_cluster(W, H, cx, cy, n, spread, rng, rmin=4.5, rmax=8.5):
    """Mask of tiny 5-lobed florets around (cx, cy)."""
    centres = []
    def draw(cv):
        for _ in range(n):
            x, y = cx + rng.gauss(0, spread), cy + rng.gauss(0, spread * .8)
            r = rng.uniform(rmin, rmax)
            centres.append((x, y, r))
            for k in range(5):
                a = k / 5 * math.tau + rng.uniform(-.3, .3)
                cv.c.drawCircle(x + math.cos(a) * r * .45, y + math.sin(a) * r * .45, r * .52, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw), centres


def spray(seed=3):
    W, H = 440, 540
    rng = random.Random(seed); sd = Seeds(300 + seed)
    base = (222, 528)
    # main stems fanning up, each forking into short pedicels that end in floret clusters
    tips = [(96, 110), (176, 70), (262, 84), (340, 136), (136, 196), (296, 214), (222, 160), (60, 190), (372, 240)]
    stems = blank(W, H); heads = []
    for i, (tx, ty) in enumerate(tips):
        mid = ((base[0] * .55 + tx * .45) + rng.uniform(-14, 14), (base[1] * .45 + ty * .55))
        lay, _ = stem(W, H, [base, mid, (tx, ty)], 3.6 if i < 4 else 2.8, STEM, sd, density=0.62)
        stems = glaze(stems, lay)
        for j in range(rng.randint(4, 7)):
            a = rng.uniform(-2.6, -0.5)
            L = rng.uniform(22, 58)
            ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L
            lay, _ = stem(W, H, [(tx, ty), ((tx + ex) / 2 + rng.uniform(-4, 4), (ty + ey) / 2), (ex, ey)], 1.8, STEM, sd, density=0.55)
            stems = glaze(stems, lay)
            heads.append((ex, ey))
        heads.append((tx, ty - 6))
    # two small narrow leaves low on the stem
    for (x, y, a) in [(214, 430, -2.25), (230, 404, -0.8)]:
        lay, _ = leaf(W, H, x, y, 56, a, "#93a273", "#66744a", sd, rng, width=0.18, vein=False, density=0.8)
        stems = glaze(stems, lay)
    fm = np.zeros((H, W), np.float32); cs = []
    for (x, y) in heads:
        m, c = floret_cluster(W, H, x, y, rng.randint(4, 7), 9, rng, 5, 9.5)
        fm = np.maximum(fm, m); cs += c
    # soft warm shadow under the white florets, then opaque white gouache on top, tiny olive centres
    shadow = np.roll(np.roll(gaussian_filter(fm, 1.5), 3, 0), 2, 1)
    art = glaze(stems, pig(shadow, "#9c8466", seed=sd(), density=0.35, edge=0.2, bloom=0, rough=1.5, feather=1.0))
    art = over(art, gouache_paint(fm, "#fffaf0", "#f1e9d8", seed=sd(), rough=1.3, streak=0.4, density=0.97))
    cm = mask_from(W, H, lambda cv: [cv.c.drawCircle(x, y, r * .2, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)) for (x, y, r) in cs])
    art = over(art, gouache_paint(cm, "#cfc497", "#b4ad78", seed=sd(), rough=0.6, density=0.85))
    return art


def twine_tex(mask, seed, period=7.0):
    """Gouache twine: painted strand + diagonal twist stripes + fibre fuzz."""
    h, w = mask.shape
    lay = gouache_paint(mask, TWINE, "#bf9a63", seed=seed, rough=1.2, streak=0.6)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tw = 0.5 + 0.5 * np.sin((xx + yy) / period * math.tau / 2 + fbm(w, h, seed, 14, 2) * 5)
    lay[..., :3] *= (0.86 + 0.18 * tw[..., None])
    fuzz = (np.random.default_rng(seed).random((h, w)) > 0.985).astype(np.float32)
    fuzz = gaussian_filter(fuzz, (0.4, 1.4)) * gaussian_filter(mask, 3) * 3
    lay[..., 3] = np.clip(lay[..., 3] + fuzz * 0.6, 0, 1)
    return lay


def bow():
    W, H = 300, 160
    sw = 9
    loops = [
        [(150, 72), (118, 30), (64, 18), (44, 52), (70, 84), (150, 72)],
        [(150, 72), (184, 30), (238, 20), (256, 54), (228, 86), (150, 72)],
    ]
    tails = [[(146, 76), (126, 108), (100, 134), (78, 150)], [(154, 76), (176, 108), (204, 134), (226, 148)]]
    m = np.zeros((H, W), np.float32)
    for l in loops:
        m = np.maximum(m, stroke_mask(W, H, curve(l, 90), sw, taper=(0.02, 0.02)))
    for t in tails:
        m = np.maximum(m, stroke_mask(W, H, curve(t, 50), sw * .9, taper=(0.02, 0.25)))
    knot = shape_mask(W, H, ellipse_pts(150, 74, 15, 12, 10))
    art = twine_tex(m, 61)
    art = over(art, twine_tex(knot, 62, 5))
    sh = gaussian_filter(np.roll(np.maximum(m, knot), 4, 0), 3)
    art = over(pig(sh, "#5a3a20", seed=63, density=0.25, edge=0, bloom=0, rough=1), art)
    return art


def divider():
    W, H = 460, 48
    pts = [(10 + i * 11, 24 + math.sin(i / 41 * math.tau * 2) * 8) for i in range(41)]
    m = stroke_mask(W, H, curve(pts, 160), 4.2, taper=(0.06, 0.06))
    art = twine_tex(m, 71, 5)
    rng = random.Random(8)
    fm, cs = floret_cluster(W, H, 230, 22, 4, 6, rng, 5, 8)
    art = glaze(art, pig(np.roll(gaussian_filter(fm, 1.4), 2, 0), "#9c8466", seed=72, density=0.3, edge=0.2, bloom=0, rough=1))
    art = over(art, gouache_paint(fm, "#fffaf0", "#f1e9d8", seed=73, rough=1.0, density=0.97))
    return art


def wood():
    """Seamless painted planks (opaque), 400×800 tile shown at 200×400."""
    Wt, Ht = 400, 800
    rng = np.random.default_rng(5)
    yy, xx = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    seams = [0, 128, 270, 400]
    cols = ["#6e4629", "#5f3c23", "#73492b"]
    rgb = np.zeros((Ht, Wt, 3), np.float32)
    warp = wrapn(rng, (Ht, Wt), (60, 30))
    fine = wrapn(rng, (Ht, Wt), (14, 0.6))
    fib = wrapn(rng, (Ht, Wt), (6, 0.5))
    mott = wrapn(rng, (Ht, Wt), 50)
    from scipy.ndimage import map_coordinates as _mc
    def warped(a, amt):
        return _mc(a, [yy, (xx + warp * amt) % Wt], order=1, mode="wrap")
    grain = warped(wrapn(rng, (Ht, Wt), (90, 2.2)), 10)
    lines = warped(wrapn(rng, (Ht, Wt), (120, 0.9)), 12)
    for i in range(3):
        x0, x1 = seams[i], seams[i + 1]
        sel = (xx >= x0) & (xx < x1)
        base = np.array(hex_rgb(cols[i]), np.float32)
        # long streaky grain: strongly elongated noise, gently warped, plus a few darker grain lines
        sh = np.roll(grain, i * 97, axis=1); sl = np.roll(lines, i * 61, axis=1)
        tone = 1 + sh * 0.05 + np.clip(sl - 1.2, 0, None) * -0.09 + fib * 0.03 + mott * 0.035 + (i - 1) * 0.02
        rgb[sel] = (base * tone[..., None])[sel]
        # seam: dark groove + faint lit edge
        d = xx - x0
        groove = np.exp(-((d - 1.2) ** 2) / 2.5) + np.exp(-((x1 - xx - 0.8) ** 2) / 1.5) * .7
        lit = np.exp(-((d - 4.5) ** 2) / 4.0)
        f = (1 - 0.55 * groove + 0.08 * lit)
        rgb[sel] *= f[sel][..., None]
    # one soft knot per plank pair (repeats every tile, kept quiet)
    for (kx, ky, kr) in [(70, 260, 16), (330, 610, 13)]:
        d = np.hypot((xx - kx) * 1.6, yy - ky)
        rgb *= (1 - 0.14 * np.exp(-(d / kr) ** 2))[..., None]
    img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    save_texture(img, f"{D}/wood.webp", quality=72)
    img.crop((0, 0, 400, 400)).save(f"{P}/rk-wood.png")


def kraft():
    """Transparent kraft fibre/speck overlay tile (512, shown at 256) — sits over any paper colour."""
    S = 512
    rng = random.Random(9)
    nr = np.random.default_rng(9)
    dark = np.zeros((S, S), np.float32); light = np.zeros((S, S), np.float32)
    def fibres(cv, n, wmin, wmax):
        for _ in range(n):
            x, y = rng.uniform(0, S), rng.uniform(0, S)
            a = rng.uniform(0, math.pi); L = rng.uniform(6, 22)
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=rng.uniform(wmin, wmax), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
            for ox in (-S, 0, S):
                for oy in (-S, 0, S):
                    cv.c.drawLine(x + ox, y + oy, x + ox + math.cos(a) * L, y + oy + math.sin(a) * L, p)
    dark = mask_from(S, S, lambda cv: fibres(cv, 200, .6, 1.2))
    light = mask_from(S, S, lambda cv: fibres(cv, 160, .6, 1.2))
    speck = (nr.random((S, S)) > 0.9988).astype(np.float32)
    speck = gaussian_filter(speck, 0.7, mode="wrap") * 4
    mott = wrapn(nr, (S, S), 30)
    a_dark = np.clip(dark * 0.11 + speck * 0.3 + np.clip(mott, 0, None) * 0.015, 0, 1)
    a_light = np.clip(light * 0.15 + np.clip(-mott, 0, None) * 0.015, 0, 1)
    # merge into one RGBA: dark brown where dark dominates, warm white elsewhere
    a = np.maximum(a_dark, a_light)
    t = (a_dark >= a_light)[..., None].astype(np.float32)
    rgb = t * np.array(hex_rgb("#5a3a1e"), np.float32) + (1 - t) * np.array(hex_rgb("#fff6e2"), np.float32)
    arr = np.concatenate([rgb * np.ones((S, S, 3), np.float32), a[..., None]], -1)
    save_texture(arr, f"{D}/kraft.webp", quality=60)
    prev = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(KRAFT), np.float32)
    out = prev * (1 - a[..., None]) + rgb * a[..., None]
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(f"{P}/rk-kraft.png")


def main(which):
    if "spray" in which:
        art = spray()
        print("spray", save_asset(art, f"{D}/spray.webp", max_w=260, quality=82))
        preview(art, f"{P}/rk-spray.png", KRAFT)
    if "bow" in which:
        art = bow()
        print("bow", save_asset(art, f"{D}/bow.webp", max_w=170, quality=82))
        preview(art, f"{P}/rk-bow.png", KRAFT)
    if "divider" in which:
        art = divider()
        print("divider", save_asset(art, f"{D}/twine.webp", max_w=400, quality=82))
        preview(art, f"{P}/rk-twine.png", "#f6eedf")
    if "wood" in which:
        wood()
    if "kraft" in which:
        kraft()


if __name__ == "__main__":
    main(sys.argv[1:] or ["spray", "bow", "divider", "wood", "kraft"])
