"""Batak Ulos — linocut gorga + woven ulos textures.
Assets: rumah-bolon (linocut Rumah Bolon), lozenge (linocut gorga diamond frame), spiral-red / spiral-bone (gorga
simeol-meol pair), gorga-band (seamless repeat-x linocut band), ulos (seamless woven cloth band), rambu (fringe),
ulos-side (seamless repeat-y woven edge for event cards).
Run: python3 -I /tmp/pen/art/themes/batak-ulos.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentF_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/batak-ulos"
PRE = "/tmp/pen/nt2-F/art"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(21)
seed = [700]
def nxt():
    seed[0] += 11
    return seed[0]

BLACK = "#15100e"; COAL = "#221a17"; RED = "#b3261e"; MAROON = "#7a1616"; BONE = "#f4efe6"


def lino(m, col, wear=.3, rough=1.4):
    return linocut(m, col, seed=nxt(), wear=wear, rough=rough)


def gouges(W, H, region, n, length, angle_fn, width=1.4, col=BONE, alpha=.35):
    """Short tapered knife marks inside a region (the carved texture of a woodblock)."""
    def draw(cv):
        for _ in range(n):
            for _try in range(20):
                x, y = rng.uniform(0, W), rng.uniform(0, H)
                if region[int(min(H - 1, y)), int(min(W - 1, x))] > .5:
                    break
            a = angle_fn(x, y) + rng.gauss(0, .08)
            L = length * rng.uniform(.5, 1.2)
            pts = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0, 1, 8)]
            for i in range(7):
                k = math.sin(math.pi * (i + .5) / 7)
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=max(.5, width * k), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(*pts[i], *pts[i + 1], p)
    m = mask_from(W, H, draw) * region
    return fade(lino(m, col, .4, .8), alpha)


# ---------------- Rumah Bolon ----------------
def rumah_bolon():
    S = 2.2; W, H = int(226 * S), int(166 * S); ox, oy = 3 * S, 3 * S
    P = lambda d: svg_path(d, S, ox, oy)
    art = blank(W, H)
    roof_d = "M4 10c44 30 76 42 106 42S172 40 216 10l-22 80c-40 9-128 9-168 0Z"
    roof = displace(path_mask(W, H, P(roof_d)), nxt(), 2, 26)
    art = over(art, lino(roof, COAL, .15))
    # thatch: knife marks following the roof's sweep
    art = over(art, gouges(W, H, roof, 260, 26 * S, lambda x, y: math.pi / 2 + (x / W - .5) * -.45, 1.2 * S, BONE, .28))
    art = over(art, lino(path_mask(W, H, P(roof_d), stroke=1.8 * S), BONE, .25))
    # ridge line accent
    art = over(art, lino(path_mask(W, H, P("M8 13c44 30 74 41 102 41s58-11 102-41"), stroke=1.0 * S), RED, .3))
    gable_d = "M58 90 110 56l52 34Z"
    gable = displace(path_mask(W, H, P(gable_d)), nxt(), 1.2, 20)
    art = over(art, lino(gable, RED, .22))
    art = over(art, lino(path_mask(W, H, P(gable_d), stroke=1.6 * S), BONE, .2))
    for d in ["M110 86c-12 0-16-8-12-13s11-3 11 2-6 5-6 1", "M110 86c12 0 16-8 12-13s-11-3-11 2 6 5 6 1", "M84 86c-4-6 0-12 6-11", "M136 86c4-6 0-12-6-11"]:
        art = over(art, lino(path_mask(W, H, P(d), stroke=1.9 * S), BONE, .25, 1))
    art = over(art, lino(circles_mask(W, H, [(ox + 110 * S, oy + 68 * S, 3.2 * S)]), BONE, .1))
    body = displace(path_mask(W, H, P("M42 90h136v30H42Z")), nxt(), 1.2, 20)
    art = over(art, lino(body, RED, .25))
    art = over(art, lino(path_mask(W, H, P("M42 90h136v30H42Z"), stroke=1.6 * S), BONE, .2))
    for d in ["M42 96h136", "M42 114h136"]:
        art = over(art, lino(path_mask(W, H, P(d), stroke=2.2 * S, cap="butt"), BLACK, .2))
    zz = "M42 105" + "".join(f"L{42 + 8 * (i + 1)} {99 if i % 2 == 0 else 105}" for i in range(17))
    art = over(art, lino(path_mask(W, H, P(zz), stroke=1.5 * S), BONE, .3, 1))
    art = over(art, lino(circles_mask(W, H, [(ox + x * S, oy + 109 * S, 1.5 * S) for x in range(50, 170, 16)]), BONE, .2))
    for x in [52, 84, 136, 168]:
        art = over(art, lino(path_mask(W, H, P(f"M{x} 121v33"), stroke=3.4 * S), BONE, .35))
    for d in ["M98 120l-6 34", "M122 120l6 34", "M95 132h30", "M93 144h34"]:
        art = over(art, lino(path_mask(W, H, P(d), stroke=1.7 * S), BONE, .3))
    ground = [(ox + x * S, oy + (154 + math.sin(x * .2) * .4) * S) for x in np.linspace(-2, 222, 40)]
    art = over(art, fade(lino(stroke_mask(W, H, ground, 1.6 * S, (.2, .2)), BONE, .5), .7))
    size = save_asset(art, f"{OUT}/rumah-bolon.webp", max_w=440, quality=82)
    preview(art, f"{PRE}/bt_house.png", BLACK)
    return size


def lozenge():
    S = 2.1; W = H = int(204 * S); o = 2 * S
    P = lambda d: svg_path(d, S, o, o)
    art = blank(W, H)
    outer = displace(path_mask(W, H, P("M100 4 196 100 100 196 4 100Z")), nxt(), 1.5, 30)
    art = over(art, lino(outer, BLACK, .05))
    art = over(art, gouges(W, H, outer, 160, 10 * S, lambda x, y: math.atan2(y - H / 2, x - W / 2) + math.pi / 2, .9 * S, COAL, .9))
    art = over(art, lino(path_mask(W, H, P("M100 4 196 100 100 196 4 100Z"), stroke=3.2 * S), RED, .2))
    art = over(art, lino(path_mask(W, H, P("M100 20 180 100 100 180 20 100Z"), stroke=1.3 * S), BONE, .3))
    for d in ["M100 20 108 28 100 36 92 28Z", "M100 180 108 172 100 164 92 172Z", "M20 100 28 92 36 100 28 108Z", "M180 100 172 92 164 100 172 108Z"]:
        art = over(art, lino(path_mask(W, H, P(d)), RED, .15))
    for d in ["M60 60c-8-8-2-18 6-14s2 12-3 8", "M140 60c8-8 2-18-6-14s-2 12 3 8", "M60 140c-8 8-2 18 6 14s2-12-3-8", "M140 140c8 8 2 18-6 14s-2-12 3-8"]:
        art = over(art, lino(path_mask(W, H, P(d), stroke=1.8 * S), BONE, .3, 1))
    size = save_asset(art, f"{OUT}/lozenge.webp", max_w=420, quality=82)
    preview(art, f"{PRE}/bt_lozenge.png", "#fbf8f2")
    return size


def spiral(name, col):
    S = 3.0; W = H = int(42 * S); o = 1 * S
    P = lambda d: svg_path(d, S, o, o)
    m = np.zeros((H, W), np.float32)
    for d in ["M4 20c0-9 8-14 15-11s7 11 1 12-6-6-2-6", "M36 20c0 9-8 14-15 11s-7-11-1-12 6 6 2 6"]:
        m = np.maximum(m, path_mask(W, H, P(d), stroke=2.8 * S))
    art = lino(displace(m, nxt(), 1.2, 12), col, .3, .8)
    size = save_asset(art, f"{OUT}/{name}.webp", max_w=88, quality=84)
    preview(art, f"{PRE}/bt_{name}.png", BLACK if col == BONE else "#fbf8f2")
    return size


def seamless_x(render, P, n=8):
    """render(width) → RGBA of (n+1) periods; crossfade the extra period over the first so the strip tiles."""
    a = render(P * (n + 1))
    out = a[:, :P * n].copy()
    t = np.linspace(0, 1, P, dtype=np.float32)[None, :, None]
    out[:, :P] = a[:, P * n:] * (1 - t) + a[:, :P] * t
    return out


def gorga_band():
    S = 2; P = 48 * S; H = 36 * S
    def render(W):
        n = W // P
        bg = np.ones((H, W, 4), np.float32); bg[..., :3] = np.array(hex_rgb(BLACK), np.float32)
        art = bg
        teeth_top = poly_mask(W, H, [(0, 0)] + [(i * 6 * S, (6 * S if i % 2 else 0)) for i in range(n * 8 + 1)] + [(W, 0)])
        teeth_bot = poly_mask(W, H, [(0, H)] + [(i * 6 * S, (H - 6 * S if i % 2 else H)) for i in range(n * 8 + 1)] + [(W, H)])
        art = over(art, lino(displace(np.maximum(teeth_top, teeth_bot), nxt(), 1, 10), RED, .25, .8))
        m = np.zeros((H, W), np.float32)
        dots = []
        for k in range(n):
            ox = k * P
            for d in ["M0 18c12 0 12-9 22-9 8 0 8 8 2 8-4 0-4-4-1-4", "M48 18c-12 0-12 9-22 9-8 0-8-8-2-8 4 0 4 4 1 4"]:
                m = np.maximum(m, path_mask(W, H, svg_path(d, S, ox, 0), stroke=2.0 * S))
            dots += [(ox + 9 * S, 24 * S, 1.7 * S), (ox + 39 * S, 12 * S, 1.7 * S)]
        art = over(art, lino(displace(m, nxt(), .8, 10), BONE, .32, .7))
        art = over(art, lino(circles_mask(W, H, dots), RED, .1, .5))
        return art
    tile = seamless_x(render, P, 8)
    im = to_image(tile).convert("RGB")
    im.save(f"{OUT}/gorga-band.webp", "WEBP", quality=80, method=6)
    im.save(f"{PRE}/bt_gorga.png")
    return im.size


# ---------------- woven ulos ----------------
def wrap_noise(h, w, seed_, sigma):
    n = gaussian_filter(np.random.default_rng(seed_).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def weave(H, W, stripes, t=2, weft="#3a0d0b", seed_=1):
    """Warp-faced cloth, warp running horizontally. stripes: list of (rows_px, hex) top→bottom.
    Returns RGB float array, periodic in x (W multiple of 2t)."""
    rgb = np.zeros((H, W, 3), np.float32)
    y = 0
    for hpx, col in stripes:
        rgb[y:y + hpx] = np.array(hex_rgb(col), np.float32); y += hpx
    rgb[y:] = rgb[y - 1] if y else 0
    yy, xx = np.mgrid[0:H, 0:W]
    over_ = ((yy // t + xx // t) % 2 == 0)
    wc = np.array(hex_rgb(weft), np.float32)
    rgb = np.where(over_[..., None], rgb, rgb * .72 + wc * .28)
    # thread roundness: brighter in the middle of each warp row
    fy = (yy % t + .5) / t
    rgb *= (0.88 + 0.16 * np.sin(math.pi * fy))[..., None]
    # per-thread tension + slubs (periodic noise)
    rowv = np.random.default_rng(seed_).normal(0, 1, (H // t + 1, 1)).astype(np.float32)
    rgb *= (1 + 0.035 * np.repeat(rowv, t, 0)[:H])[..., None]
    slub = wrap_noise(H, W, seed_ + 3, (0.6, 9))
    rgb *= (1 + 0.04 * slub)[..., None]
    big = wrap_noise(H, W, seed_ + 5, 30)
    rgb *= (1 + 0.03 * big)[..., None]
    return np.clip(rgb, 0, 1)


def ragi_row(H, W, cy, cell_w, cell_h, t=2, col=BONE):
    """Supplementary-weft diamonds (ragi), quantised to the thread grid so they read as woven floats."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gx = (xx // t) * t + t / 2; gy = (yy // t) * t + t / 2
    lx = (gx % cell_w) - cell_w / 2; ly = gy - cy
    d = np.abs(lx) / (cell_w * .44) + np.abs(ly) / (cell_h * .44)
    ring = (d > .62) & (d < 1.0)
    dot = d < .22
    m = (ring | dot).astype(np.float32)
    # floats: only on every other row slightly broken → hand-woven irregularity
    jitter = wrap_noise(H, W, nxt(), (0.5, 4)) > 2.4
    m *= ~jitter
    shade = 0.86 + 0.14 * np.sin(math.pi * ((yy % t + .5) / t))
    return m, np.array(hex_rgb(col), np.float32)[None, None] * shade[..., None]


def ulos():
    t = 2; H = 116; P = 32; W = P * 24  # 768px wide, repeats every 384 CSS px
    stripes = [(8, MAROON), (4, RED), (6, MAROON), (2, BONE), (8, MAROON), (4, BLACK), (4, MAROON), (2, RED),
               (40, MAROON), (2, RED), (4, MAROON), (4, BLACK), (8, MAROON), (2, BONE), (6, MAROON), (4, RED), (8, MAROON)]
    rgb = weave(H, W, stripes, t, seed_=nxt())
    # warm the central ragi field
    rgb[50:66] = rgb[50:66] * .9 + np.array(hex_rgb("#5e1210"), np.float32) * .1
    m, col = ragi_row(H, W, 58, P, 24, t)
    rgb = rgb * (1 - m[..., None]) + col * m[..., None]
    # tiny bone pick dots between stripes
    im = Image.fromarray((rgb * 255).astype(np.uint8), "RGB")
    im.save(f"{OUT}/ulos.webp", "WEBP", quality=82, method=6)
    im.save(f"{PRE}/bt_ulos.png")
    return im.size


def rambu():
    """Fringe: twisted bone/red thread tassels hanging from the ulos edge (repeat-x, periodic)."""
    H = 36; W = 768
    art = blank(W, H)
    def draw(cv):
        r = random.Random(5)
        x = 0.0
        while x < W - 2:
            L = r.uniform(.7, 1) * (H - 4)
            sway = r.uniform(-2, 2)
            for i in range(10):
                tt0, tt1 = i / 10, (i + 1) / 10
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=2.2 * (1 - tt0 * .45), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(x + sway * tt0 ** 2, L * tt0, x + sway * tt1 ** 2, L * tt1, p)
            x += 6
    m = mask_from(W, H, draw)
    tw = (np.sin(np.mgrid[0:H, 0:W][0] * 1.6) * .5 + .5)
    art = np.zeros((H, W, 4), np.float32)
    art[..., :3] = np.array(hex_rgb(BONE), np.float32) * (.82 + .18 * tw)[..., None]
    art[..., 3] = m * np.clip(1.15 - np.linspace(0, 1, H)[:, None] * .5, 0, 1)
    # every 4th tassel red
    cols = (np.arange(W) // 6) % 4 == 2
    art[:, cols, :3] = np.array(hex_rgb("#c0392b"), np.float32) * (.82 + .18 * tw[:, cols])[..., None]
    im = to_image(art)
    im.save(f"{OUT}/rambu.webp", "WEBP", quality=84, method=6)
    preview(art, f"{PRE}/bt_rambu.png", BLACK)
    return im.size


def ulos_side():
    """Vertical woven edge for event cards (warp runs vertically): 36px wide (18 CSS px), repeat-y."""
    t = 2; W = 36; H = 384
    stripes = [(6, MAROON), (2, BONE), (6, RED), (8, MAROON), (6, RED), (2, BONE), (6, MAROON)]
    rgb = weave(W, H, stripes, t, seed_=nxt())  # (W rows, H cols) then transpose
    m, col = ragi_row(W, H, 18, 24, 18, t)
    rgb = rgb * (1 - m[..., None]) + col * m[..., None]
    rgb = np.transpose(rgb, (1, 0, 2))
    im = Image.fromarray((rgb * 255).astype(np.uint8), "RGB")
    im.save(f"{OUT}/ulos-side.webp", "WEBP", quality=82, method=6)
    im.save(f"{PRE}/bt_side.png")
    return im.size


if __name__ == "__main__":
    print("rumah-bolon", rumah_bolon())
    print("lozenge", lozenge())
    print("spiral-red", spiral("spiral-red", RED))
    print("spiral-bone", spiral("spiral-bone", BONE))
    print("gorga-band", gorga_band())
    print("ulos", ulos())
    print("rambu", rambu())
    print("ulos-side", ulos_side())
    tot = 0
    for f in sorted(os.listdir(OUT)):
        tot += kb(f"{OUT}/{f}"); print(f, kb(f"{OUT}/{f}"), "KB")
    print("total", round(tot, 1))
