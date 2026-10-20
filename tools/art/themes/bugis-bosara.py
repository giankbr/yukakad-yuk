"""Bugis Bosara — gouache + gold foil folk painting.
Assets: bosara-lid / bosara-base (same canvas so they stack; the lid floats), divider (sulapa eppa jewel),
jewel-gold / jewel-magenta / jewel-emerald (bullets), sabbe (seamless translucent woven-silk check overlay),
walasuji (seamless bamboo lattice).
Run: python3 -I /tmp/pen/art/themes/bugis-bosara.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentF_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/bugis-bosara"
PRE = "/tmp/pen/nt2-F/art"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(31)
seed = [900]
def nxt():
    seed[0] += 7
    return seed[0]

MAGENTA = "#c2185b"; PLUM = "#7d0f3d"; EMERALD = "#0f7a5c"; GOLD = "#d4a532"; GOLD_L = "#f7dc8c"; GOLD_D = "#9b7414"; IVORY = "#fff3d6"


def g(m, col, col2=None, rough=1.6, streak=.6):
    return gouache_paint(m, col, col2, seed=nxt(), rough=rough, streak=streak)


def f(m, base=GOLD, emboss=.7):
    return foil(m, base, seed=nxt(), emboss=emboss, sparkle=.02)


def save_full(arr, path, w_out):
    im = to_image(arr)
    im = im.resize((w_out, round(im.height * w_out / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=84, method=6)
    return im.size


def bosara():
    S = 3.0; W, H = int(160 * S), int(172 * S)
    P = lambda d: svg_path(d, S, 0, 0)
    # ---- base (bowl + stand)
    base = blank(W, H)
    bowl = displace(path_mask(W, H, P("M26 114c8 22 30 34 54 34s46-12 54-34Z")), nxt(), 1.6, 24)
    stand = displace(path_mask(W, H, P("M60 148h40l8 14H52Z")), nxt(), 1.2, 20)
    foot = displace(path_mask(W, H, P("M46 160h68v6H46Z")), nxt(), 1, 20)
    base = over(base, shadow(np.maximum(np.maximum(bowl, stand), foot), 3, 6, 6, .3, "#3a0a1f"))
    base = over(base, f(foot, GOLD_D))
    base = over(base, f(stand, "#c09328"))
    base = over(base, f(bowl, GOLD))
    base = over(base, linocut(path_mask(W, H, P("M40 122c10 12 24 18 40 18s30-6 40-18"), stroke=1.2 * S), "#8a6512", seed=nxt(), wear=.35))
    # painted lotus-petal band on the bowl
    for k in range(7):
        cx = 38 + k * 14
        cy = 118 + 6 * math.sin(math.pi * k / 6)
        pm = shape_mask(W, H, petal_pts(cx * S, (cy + 8) * S, 9 * S, 3.4 * S, -math.pi / 2 + (k - 3) * .08, n=12)) * bowl
        base = over(base, fade(g(pm, "#b8862a", "#a87a22", 1), .55))
    base = over(base, g(circles_mask(W, H, [(54 * S, 128 * S, 2.2 * S), (80 * S, 134 * S, 2.6 * S), (106 * S, 128 * S, 2.2 * S)]), EMERALD, "#14936f", 1))
    # ---- lid
    lid = blank(W, H)
    dome_d = "M22 104C26 58 50 30 80 20c30 10 54 38 58 84Z"
    dome = displace(path_mask(W, H, P(dome_d)), nxt(), 2, 26)
    lid = over(lid, shadow(dome, 3, 6, 7, .28, "#3a0a1f"))
    lid = over(lid, f(grow(dome, 1.4 * S), GOLD, .5))
    lid = over(lid, g(dome, MAGENTA, "#d02a6c", 2, .9))
    # shading: light from upper left → right side of dome deepens
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    lid = over(lid, fade(g(dome * np.clip((xx - .52) * 3, 0, 1), PLUM, "#8e1446", 1, .6), .55))
    hl = shape_mask(W, H, deform(petal_pts(52 * S, 86 * S, 48 * S, 7 * S, -1.25, n=14), rng, 1, .05)) * dome
    lid = over(lid, fade(g(hl, "#e2558e", None, 1, .9), .45))
    # dotted stitch line
    def stitches(cv):
        pts = curve([(36, 100), (44, 62), (80, 34), (116, 62), (124, 100)], 120)
        for i in range(0, len(pts), 4):
            cv.c.drawCircle(pts[i][0] * S, pts[i][1] * S, 1.0 * S, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    lid = over(lid, f(mask_from(W, H, stitches), GOLD_L, .3))
    for d in ["M80 44 92 58 80 72 68 58Z", "M54 74 62 83 54 92 46 83Z", "M106 74l8 9-8 9-8-9Z", "M80 80l7 8-7 8-7-8Z"]:
        lid = over(lid, f(displace(path_mask(W, H, P(d)), nxt(), .8, 10), GOLD, .9))
    lid = over(lid, g(path_mask(W, H, P("M80 52 85 58 80 64 75 58Z")), MAGENTA, None, .6))
    lid = over(lid, g(circles_mask(W, H, [(64 * S, 54 * S, 1.6 * S), (96 * S, 54 * S, 1.6 * S), (44 * S, 96 * S, 1.4 * S), (116 * S, 96 * S, 1.4 * S), (80 * S, 30 * S, 1.6 * S)]), IVORY, None, .6))
    rim = displace(path_mask(W, H, P("M18 100h124v9H18Z")), nxt(), 1, 20)
    def scal(cv):
        r = 5.17
        x = 18 + r
        while x <= 142 - r + .1:
            cv.c.drawCircle(x * S, 109 * S, r * S, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)); x += 2 * r
    sc = mask_from(W, H, scal) * (np.arange(H)[:, None] >= 109 * S)
    lid = over(lid, shadow(np.maximum(rim, sc), 2, 4, 4, .3, "#3a0a1f"))
    lid = over(lid, f(np.maximum(rim, displace(sc, nxt(), .8, 10)), GOLD, .8))
    lid = over(lid, f(circles_mask(W, H, [(80 * S, 16 * S, 6.2 * S)]), GOLD, .9))
    lid = over(lid, g(circles_mask(W, H, [(80 * S, 16 * S, 2.5 * S)]), EMERALD, None, .6))
    sz = save_full(base, f"{OUT}/bosara-base.webp", 300), save_full(lid, f"{OUT}/bosara-lid.webp", 300)
    preview(over(base, lid), f"{PRE}/bg_bosara.png", "#fff8ef")
    return sz


def divider():
    S = 2.5; W, H = int(164 * S), int(28 * S); o = 2 * S
    P = lambda d: svg_path(d, S, o, o)
    art = blank(W, H)
    for d in ["M4 12h56", "M100 12h56"]:
        art = over(art, f(displace(path_mask(W, H, P(d), stroke=1.3 * S), nxt(), .6, 12), GOLD, .3))
    big = path_mask(W, H, P("M80 1 91 12 80 23 69 12Z"))
    art = over(art, f(grow(big, 1.3 * S), GOLD, .6))
    art = over(art, g(big, MAGENTA, "#d02a6c", 1))
    art = over(art, f(path_mask(W, H, P("M80 7 85 12 80 17 75 12Z")), GOLD, .8))
    for d in ["M62 12 66 8 70 12 66 16Z", "M90 12l4-4 4 4-4 4Z"]:
        art = over(art, g(path_mask(W, H, P(d)), EMERALD, "#14936f", .7))
    size = save_asset(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    preview(art, f"{PRE}/bg_divider.png", "#fff8ef")
    return size


def jewel(name, outer):
    S = 5; W = H = int(26 * S); o = 1 * S
    P = lambda d: svg_path(d, S, o, o)
    out_m = path_mask(W, H, P("M12 1 23 12 12 23 1 12Z"))
    art = blank(W, H)
    art = over(art, f(out_m, GOLD, .9) if outer is None else g(out_m, outer, mix(outer, "#ffffff", .12), .8))
    if outer is not None:
        art = over(art, f(outline(out_m, .9 * S), GOLD, .5))
    art = over(art, f(path_mask(W, H, P("M12 6 18 12 12 18 6 12Z")), GOLD_L if outer else "#e8c25a", .8))
    art = over(art, g(path_mask(W, H, P("M12 9.5 14.5 12 12 14.5 9.5 12Z")), outer or MAGENTA, None, .5))
    size = save_asset(art, f"{OUT}/{name}.webp", max_w=56, quality=86)
    preview(art, f"{PRE}/bg_{name}.png", "#c2185b" if outer is None else "#fff8ef")
    return size


def wrapn(h, w, s_, sigma):
    n = gaussian_filter(np.random.default_rng(s_).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def sabbe():
    """Lipa' sabbe silk check overlay: translucent white/dark/gold stripe bands in both directions + fine weave.
    Tile = 4 periods of 40 CSS px (160 CSS), rendered at 2x → 320px, seamless."""
    T = 240; p = 80  # period at 2x (3 periods = 120 CSS px)
    yy, xx = np.mgrid[0:T, 0:T]
    def band(v):
        v = v % p
        w = np.zeros_like(v, dtype=np.float32); d = np.zeros_like(w); gd = np.zeros_like(w)
        w[(v < 8)] = 1; d[(v >= 36) & (v < 44)] = 1; gd[(v >= 60) & (v < 62)] = 1
        return w, d, gd
    wx, dx, gx = band(xx); wy, dy, gy = band(yy)
    # crossing threads: the warp shows on even cells, weft on odd → stripes look woven where they meet
    cell = ((xx // 2 + yy // 2) % 2).astype(np.float32)
    white = np.clip(wx * (0.6 + .4 * cell) + wy * (0.6 + .4 * (1 - cell)), 0, 1.3)
    dark = np.clip(dx * (0.6 + .4 * cell) + dy * (0.6 + .4 * (1 - cell)), 0, 1.3)
    gold = np.clip(gx * (0.5 + .5 * cell) + gy * (0.5 + .5 * (1 - cell)), 0, 1)
    slub = wrapn(T, T, 3, (0.6, 8)) * .5 + wrapn(T, T, 4, (8, 0.6)) * .5
    fine = (cell - .5) * 0.06 + slub * 0.025  # all-over silk weave
    out = np.zeros((T, T, 4), np.float32)
    # build with over()
    layers = [(np.clip(fine, 0, 1) * 1.0, "#ffffff", 1), (np.clip(-fine, 0, 1) * 1.0, "#000000", 1),
              (white * (1 + slub * .15), "#ffffff", .16), (dark * (1 + slub * .15), "#1a0010", .16), (gold, GOLD_L, .4)]
    for m, col, al in layers:
        lay = np.zeros((T, T, 4), np.float32); lay[..., :3] = np.array(hex_rgb(col), np.float32); lay[..., 3] = np.clip(m * al, 0, 1)
        out = over(out, lay)
    im = to_image(out)
    im.save(f"{OUT}/sabbe.webp", "WEBP", quality=72, method=6)
    preview(out, f"{PRE}/bg_sabbe.png", MAGENTA)
    return im.size


def walasuji():
    """Woven bamboo lattice (diagonal splints, over-under), tile 96 CSS px at 2x = 192, seamless."""
    T = 192; sp = 32; wd = 5.0
    yy, xx = np.mgrid[0:T, 0:T].astype(np.float32)
    u = (xx + yy) % sp; v = (xx - yy) % sp
    du = np.minimum(u, sp - u); dv = np.minimum(v, sp - v)
    mu = np.clip((wd / 2 - du) * 1.2, 0, 1); mv = np.clip((wd / 2 - dv) * 1.2, 0, 1)
    iu = np.floor((xx + yy + sp / 2) / sp); iv = np.floor((xx - yy + sp / 2) / sp)
    u_on_top = ((iu + iv) % 2 == 0)
    grain_u = wrapn(T, T, 7, (1.5, 1.5)) * .5
    bam = np.array(hex_rgb("#d8b46a"), np.float32); bam2 = np.array(hex_rgb("#b98f45"), np.float32)
    def strip(m, d, gr):
        shade = 1 - (d / (wd / 2)) ** 2 * .25
        col = bam[None, None] * (1 + gr[..., None] * .08) * shade[..., None]
        return col
    cu = strip(mu, du, grain_u); cv_ = strip(mv, dv, wrapn(T, T, 8, (1.5, 1.5)) * .5)
    # under-strip darkens near crossings
    out = np.zeros((T, T, 4), np.float32)
    top_u = mu * u_on_top; top_v = mv * (~u_on_top)
    under_u = mu * (~u_on_top); under_v = mv * u_on_top
    def layer(col, m):
        l = np.zeros((T, T, 4), np.float32); l[..., :3] = np.clip(col, 0, 1); l[..., 3] = np.clip(m, 0, 1); return l
    out = over(out, layer(cu * .82, under_u)); out = over(out, layer(cv_ * .82, under_v))
    out = over(out, layer(cu, top_u)); out = over(out, layer(cv_, top_v))
    im = to_image(out)
    im.save(f"{OUT}/walasuji.webp", "WEBP", quality=82, method=6)
    preview(out, f"{PRE}/bg_walasuji.png", "#fff8ef")
    return im.size


if __name__ == "__main__":
    print("bosara", bosara())
    print("divider", divider())
    print("jewel-gold", jewel("jewel-gold", None))
    print("jewel-magenta", jewel("jewel-magenta", MAGENTA))
    print("jewel-emerald", jewel("jewel-emerald", EMERALD))
    print("sabbe", sabbe())
    print("walasuji", walasuji())
    tot = 0
    for fn in sorted(os.listdir(OUT)):
        tot += kb(f"{OUT}/{fn}"); print(fn, kb(f"{OUT}/{fn}"), "KB")
    print("total", round(tot, 1))
