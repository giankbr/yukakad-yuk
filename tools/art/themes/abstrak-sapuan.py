"""Abstrak Sapuan — contemporary abstract painting: big confident flat-brush sweeps + palette-knife blocks in soft blush,
sage, ochre and charcoal on gessoed canvas.
Run: python3 -I abstrak-sapuan.py [part ...]   parts: painting band sweep ochre blocks gesso
Assets -> public/themes/art/abstrak-sapuan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f4_lib import *

OUT = outdir("abstrak-sapuan")
PARTS = sys.argv[1:] or ["painting", "band", "sweep", "ochre", "blocks", "gesso"]

GESSO = "#f1ece3"
BLUSH, BLUSH_L, BLUSH_D = "#e4ac9c", "#f2d3c6", "#c98473"
SAGE, SAGE_L = "#a3b398", "#ccd5bf"
OCHRE, OCHRE_L = "#cf973f", "#ecc57c"
CHAR, CHAR_L = "#2d2b2a", "#5d5753"


def arc(x0, y0, mx, my, x1, y1, n=80):
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
            for t in np.linspace(0, 1, n)]


def wobble_pts(pts, seed, amt=2.0):
    rng = random.Random(seed)
    out = []; o = 0
    for x, y in pts:
        o = o * 0.85 + rng.gauss(0, amt) * 0.4
        out.append((x + o, y + o * 0.6))
    return out


def gesso_ground(P, W, H, seed=1, tone=GESSO):
    """Opaque gesso: flat base + broad near-white brush passes (visible only in the relief)."""
    rng = random.Random(seed)
    p = skia.Paint(AntiAlias=True, Color4f=skia.Color4f(*hex_rgb(tone), 1))
    P.col.c.drawRect(skia.Rect(0, 0, W, H), p)
    p.setColor4f(skia.Color4f(.35, .35, .35, 1))
    P.hgt.c.drawRect(skia.Rect(0, 0, W, H), p)
    for k in range(int(W * H / 14000)):
        x, y = rng.uniform(-40, W + 40), rng.uniform(-40, H + 40)
        a = rng.uniform(-0.5, 0.5) + (math.pi / 2 if rng.random() < 0.4 else 0)
        L = rng.uniform(120, 260)
        pts = arc(x - math.cos(a) * L / 2, y - math.sin(a) * L / 2, x + rng.uniform(-20, 20), y + rng.uniform(-20, 20), x + math.cos(a) * L / 2, y + math.sin(a) * L / 2, 30)
        c = mix(tone, rng.choice(["#ffffff", "#d9cfc0", "#f7f1e8"] if tone == GESSO else ["#4a4542", "#1f1d1c", "#3a3633"]), rng.uniform(0.2, 0.6))
        sweep(P, pts, rng.uniform(50, 90), c, seed=rng.randint(0, 99999), dry=0.6, hv=0.4, streak=0.015, alpha=0.45, hvar=0.06)


if "painting" in PARTS:
    W, H = 760, 980
    P = Impasto(W, H, 3)
    gesso_ground(P, W, H, 3)
    # palette-knife planes (under the sweeps)
    knife(P, [(392, 70), (724, 104), (702, 418), (362, 394)], BLUSH, seed=11, drag=0.12, col2=BLUSH_L, hv=0.62)
    knife(P, [(470, 300), (640, 288), (652, 470), (480, 486)], BLUSH_D, seed=12, drag=1.45, col2=BLUSH, hv=0.66, alpha=0.9)
    knife(P, [(34, 500), (386, 470), (412, 808), (58, 836)], SAGE, seed=13, drag=-0.08, col2=SAGE_L, hv=0.6)
    knife(P, [(560, 760), (742, 742), (746, 900), (572, 930)], SAGE_L, seed=14, drag=0.05, col2="#e9ecdf", hv=0.58)
    knife(P, [(96, 150), (250, 128), (262, 246), (110, 262)], OCHRE_L, seed=15, drag=1.5, col2=OCHRE, hv=0.6, alpha=0.95)
    # thin blush sweep, upper left
    sweep(P, wobble_pts(arc(20, 132, 170, 40, 352, 80), 1), 50, BLUSH, seed=21, col2=BLUSH_L, dry=0.5, hv=0.62)
    # the big charcoal gesture
    sweep(P, wobble_pts(arc(48, 300, 420, 260, 690, 650, 120), 2, 1.6), 112, CHAR, seed=22, col2=CHAR_L, dry=0.55, hv=0.72, streak=0.16)
    # ochre counter-sweep low
    sweep(P, wobble_pts(arc(110, 905, 420, 790, 748, 790, 110), 3), 92, OCHRE, seed=23, col2=OCHRE_L, dry=0.5, hv=0.7)
    # blush second pass dragged through the ochre (wet-in-wet)
    sweep(P, wobble_pts(arc(300, 940, 520, 880, 700, 900, 70), 4), 34, BLUSH_L, seed=24, col2=OCHRE_L, dry=0.6, hv=0.75, alpha=0.85)
    # charcoal knife sliver + small ochre square
    knife(P, [(612, 520), (720, 512), (722, 548), (614, 556)], CHAR, seed=31, drag=0.0, col2=CHAR_L, hv=0.7)
    knife(P, [(150, 600), (214, 596), (216, 660), (152, 664)], OCHRE, seed=32, drag=0.3, hv=0.72)
    # loose rigger-brush line: one charcoal loop and a blush drawn line
    sc = [(476 + 160 * t + 34 * math.sin(t * 9), 190 + 130 * t + 40 * math.cos(t * 7.5)) for t in np.linspace(0, 1, 160)]
    sweep(P, sc, 7, CHAR, seed=42, col2=CHAR_L, dry=0.35, hv=0.7, taper0=0.1, swell=0.6, rough=0.3)
    sweep(P, [(56 + t * 240, 716 + 9 * math.sin(t * 7)) for t in np.linspace(0, 1, 120)], 6, BLUSH_D, seed=43, dry=0.5, hv=0.7, taper0=0.15, swell=0.4, rough=0.3)
    art = P.finish(relief=1.5, gloss=0.12, ambient=0.86, canvas_tex=0.8)
    preview(art, "as-painting", bg="#ffffff")
    save_rgb(art, f"{OUT}/painting.webp", size=(570, 735), quality=78)
    del P; clear()

if "band" in PARTS:
    # dark abstract strip for countdown / closing (charcoal ground, blush + ochre sweeps)
    W, H = 780, 520
    P = Impasto(W, H, 5)
    gesso_ground(P, W, H, 5, tone="#2f2c2b")
    knife(P, [(-20, 40), (300, 20), (320, 260), (-10, 280)], "#3d3936", seed=51, drag=0.1, col2="#4a4541", hv=0.6)
    knife(P, [(520, 300), (800, 280), (800, 540), (540, 540)], "#3a3a33", seed=52, drag=1.5, col2="#4a4d40", hv=0.6)
    sweep(P, wobble_pts(arc(-20, 420, 330, 330, 800, 410, 110), 6), 96, "#7a5a4e", seed=53, col2=BLUSH_D, dry=0.55, hv=0.7, alpha=0.95)
    sweep(P, wobble_pts(arc(420, 70, 600, 150, 800, 90, 70), 7), 70, OCHRE, seed=54, col2="#a87532", dry=0.5, hv=0.7, alpha=0.9)
    sweep(P, wobble_pts(arc(40, 160, 200, 120, 380, 190, 60), 8), 30, SAGE, seed=55, col2="#6f7d68", dry=0.6, hv=0.7, alpha=0.85)
    art = P.finish(relief=1.5, gloss=0.12, ambient=0.86, canvas_tex=0.5)
    preview(art, "as-band", bg="#000000")
    save_rgb(art, f"{OUT}/band.webp", size=(600, 400), quality=72)
    del P; clear()

if "sweep" in PARTS:
    # divider: one loaded flat-brush sweep, charcoal dragging into blush
    W, H = 460, 90
    P = Impasto(W, H, 61)
    sweep(P, wobble_pts(arc(16, 52, 220, 30, 444, 44, 90), 61, 1.0), 34, CHAR, seed=61, col2=BLUSH_D, dry=0.6, hv=0.7, streak=0.14)
    art = P.finish(relief=1.6, gloss=0.14, canvas_tex=0)
    preview(art, "as-sweep")
    save(art, f"{OUT}/sweep.webp", max_w=360, quality=84)
    del P; clear()

if "ochre" in PARTS:
    # big transparent ochre + blush swoosh to sit behind photos
    W, H = 640, 420
    P = Impasto(W, H, 71)
    sweep(P, wobble_pts(arc(20, 330, 260, 90, 620, 120, 110), 71, 1.4), 120, OCHRE, seed=71, col2=OCHRE_L, dry=0.5, hv=0.7)
    sweep(P, wobble_pts(arc(80, 380, 320, 300, 600, 330, 80), 72), 44, BLUSH, seed=72, col2=BLUSH_L, dry=0.55, hv=0.72, alpha=0.95)
    art = P.finish(relief=1.6, gloss=0.14, canvas_tex=0)
    preview(art, "as-ochre")
    save(art, f"{OUT}/ochre.webp", max_w=480, quality=82)
    del P; clear()

if "blocks" in PARTS:
    # stacked knife blocks: small emblem (nodes, amp, closing, sent)
    W, H = 260, 260
    P = Impasto(W, H, 81)
    knife(P, [(30, 40), (170, 30), (178, 150), (36, 160)], BLUSH, seed=81, drag=0.08, col2=BLUSH_L, hv=0.62)
    knife(P, [(100, 110), (230, 118), (222, 232), (96, 226)], SAGE, seed=82, drag=1.5, col2=SAGE_L, hv=0.64)
    knife(P, [(60, 170), (120, 166), (124, 214), (62, 220)], OCHRE, seed=83, drag=0.3, hv=0.7)
    sweep(P, wobble_pts(arc(24, 120, 120, 70, 236, 80, 50), 84), 16, CHAR, seed=84, dry=0.6, hv=0.75)
    art = P.finish(relief=1.6, gloss=0.14, canvas_tex=0)
    preview(art, "as-blocks")
    save(art, f"{OUT}/blocks.webp", max_w=180, quality=84)
    del P; clear()

if "gesso" in PARTS:
    # seamless gessoed-canvas tile
    S = 384
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    k = 2 * math.pi / S * 128
    weave = np.where(((xx * 128 / S).astype(int) + (yy * 128 / S).astype(int)) % 2 == 0, np.sin(xx * k) * .5 + .5, np.sin(yy * k) * .5 + .5)
    n = wrap_noise(S, S, 3, 1.0); n2 = wrap_noise(S, S, 4, 30)
    br = gaussian_filter(np.random.default_rng(9).random((S, S)).astype(np.float32), (1.0, 14), mode="wrap")
    br = (br - br.mean()) / (br.std() + 1e-6)
    v = 0.972 + 0.014 * weave + 0.016 * (n - .5) + 0.03 * (n2 - .5) + 0.006 * br
    rgbv = np.clip(np.array(hex_rgb(GESSO), np.float32) * v[..., None], 0, 1)
    save_rgb(np.concatenate([rgbv, np.ones((S, S, 1), np.float32)], -1), f"{OUT}/gesso.webp", quality=70)

kb(OUT)
