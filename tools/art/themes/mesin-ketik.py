"""Mesin Ketik — a vintage portable typewriter (original, unbranded) in sage-green enamel, painted gouache with chrome
and ink: platen and paper bail, typebar basket, round keys, ribbon spools (separate asset so it can turn), plus a
red-black ribbon divider, a paperclip, a carbon-paper sheet, a typing-paper tile, a desk-linen tile and an ink grain
mask for stamps.
Run: python3 -I mesin-ketik.py [part ...]  parts: machine spool ribbon clip carbon paper desk grain
Assets -> public/themes/art/mesin-ketik/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n3_lib import *

OUT = outdir("mesin-ketik")
PARTS = sys.argv[1:] or ["machine", "spool", "ribbon", "clip", "carbon", "paper", "desk", "grain"]
SAGE, SAGE_L, SAGE_D, SAGE_DD = "#86ab9a", "#a9c9b9", "#5d8474", "#3c5a4f"
INK = "#1f1d20"
CHROME, CHROME_L, CHROME_D = "#b9bcb8", "#eef0ec", "#6f7370"
KEYW = "#f3eee2"
RED = "#b3261e"
PAPER = "#f7f1e3"


def chrome(art, m, nx, vertical=False):
    art = GP(art, m, CHROME, CHROME_L, seed=nx(), rough=0.6, streak=1.0)
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    band = 0.5 + 0.5 * np.sin((xx if vertical else yy) * 0.35)
    art = tint(art, m * (band > 0.8), CHROME_L, 0.5, blur=1)
    art = tint(art, edge_ring(m, 1.4), CHROME_D, 0.8)
    return art


def machine():
    W, H = 820, 600
    rng = random.Random(3); nx = Seq(100)
    art = blank(W, H)
    cx = W / 2
    # ground shadow
    art = tint(art, shapes(W, H, [ellipse_pts(cx, 560, 380, 30, 30)]), "#000000", 0.35, blur=14)
    # main body: lower trapezoid with rounded shoulders
    body = shapes(W, H, [[(cx - 330, 560), (cx - 300, 300), (cx - 270, 250), (cx + 270, 250), (cx + 300, 300), (cx + 330, 560)]])
    art = GP(art, body, SAGE, SAGE_L, seed=nx(), rough=1.0, streak=1.0)
    art = G(art, body * below(H, 430, 140), SAGE_D, seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=2, feather=3)
    art = G(art, body * (1 - right_of(W, cx - 240, 90)), SAGE_D, seed=nx(), density=0.35, edge=0.1, bloom=0.1, rough=2, feather=3)
    art = tint(art, edge_ring(body, 2.0), SAGE_DD, 0.9)
    # top deck behind the keyboard (darker recess) + typebar basket (half ring of bars)
    deck = shapes(W, H, [[(cx - 250, 262), (cx + 250, 262), (cx + 220, 372), (cx - 220, 372)]])
    art = GP(art, deck, "#2b2a2b", "#3a3839", seed=nx(), rough=0.8)
    bars = []
    for k in range(33):
        a = 0.18 + k / 32 * (math.pi - 0.36)
        bars.append(([(cx + math.cos(a) * 46, 262 + math.sin(a) * 30), (cx + math.cos(a) * 168, 262 + math.sin(a) * 104)], 3.0, (0.0, 0.25)))
    bm = strokes(W, H, bars) * deck
    art = chrome(art, bm, nx)
    seg = shapes(W, H, [[(cx - 12, 262), (cx + 12, 262), (cx + 8, 292), (cx - 8, 292)]])
    art = chrome(art, seg, nx)
    # ribbon cups (spools sit on top of these; separate asset)
    for sx in (-208, 208):
        cup = circles(W, H, [(cx + sx, 300, 34)])
        art = GP(art, cup, "#222122", seed=nx(), rough=0.5)
        art = tint(art, edge_ring(cup, 1.6), CHROME, 0.9)
    # carriage: platen roller across the top with knobs, paper slot, paper bail, return lever
    plat = rr_mask(W, H, cx - 300, 168, cx + 300, 232, 30)
    art = GP(art, plat, INK, "#2d2a2c", seed=nx(), rough=0.6, streak=0.8)
    art = tint(art, rr_mask(W, H, cx - 290, 178, cx + 290, 190, 6), "#5a575a", 0.6, blur=2)
    rail = rr_mask(W, H, cx - 320, 226, cx + 320, 246, 6)
    art = chrome(art, rail, nx)
    for kx in (-326, 326):
        knob = rr_mask(W, H, cx + kx - 26, 170, cx + kx + 26, 230, 12)
        art = GP(art, knob, "#2a2829", seed=nx(), rough=0.5)
        ridges = strokes(W, H, [([(cx + kx - 20 + j * 6, 176), (cx + kx - 20 + j * 6, 224)], 1.4, None) for j in range(7)]) * knob
        art = tint(art, ridges, "#555255", 0.8)
    bail = rr_mask(W, H, cx - 260, 196, cx + 260, 206, 5)
    art = chrome(art, bail, nx)
    for bx in (-120, 120):
        art = tint(art, circles(W, H, [(cx + bx, 201, 9)]), INK, 0.95)
    lever = strokes(W, H, [(curve([(cx - 330, 196), (cx - 372, 150), (cx - 392, 104), (cx - 384, 80)], 30), 11, (0.0, 0.0))])
    art = chrome(art, lever, nx, vertical=True)
    art = chrome(art, circles(W, H, [(cx - 384, 78, 13)]), nx)
    # blank name plate (no brand)
    plate = rr_mask(W, H, cx - 70, 392, cx + 70, 414, 8)
    art = chrome(art, plate, nx)
    # keyboard: 4 staggered rows of round keys + space bar
    keys = []
    rows = [(436, 11, 0), (470, 11, 16), (504, 10, 30), (536, 9, 46)]
    for (y, n, off) in rows:
        span = 46
        x0 = cx - (n - 1) * span / 2 + off - 20
        for i in range(n):
            keys.append((x0 + i * span + rng.uniform(-0.6, 0.6), y, 17))
    stems = strokes(W, H, [([(x, y), (x, y - 12)], 4, None) for x, y, r in keys])
    art = tint(art, stems, "#2b2a2b", 0.9)
    rims = circles(W, H, keys)
    art = chrome(art, rims, nx)
    caps = circles(W, H, [(x, y, r - 4) for x, y, r in keys])
    art = GP(art, caps, INK, "#2e2b2d", seed=nx(), rough=0.4)
    faces = circles(W, H, [(x, y, r - 7.5) for x, y, r in keys])
    art = GP(art, faces, KEYW, "#e8e1cf", seed=nx(), rough=0.3)
    glyph = []
    for (x, y, r) in keys:
        t = rng.random()
        if t < 0.33:
            glyph.append(([(x - 3, y + 3), (x, y - 4), (x + 3, y + 3)], 1.5, None))
        elif t < 0.66:
            glyph.append(([(x - 3, y - 3), (x - 3, y + 3), (x + 3, y + 3)], 1.5, None))
        else:
            glyph.append(([(x - 3, y), (x + 3, y)], 1.5, None))
            glyph.append(([(x, y - 3), (x, y + 3)], 1.5, None))
    art = tint(art, strokes(W, H, glyph) * faces, INK, 0.85)
    art = tint(art, circles(W, H, [(x - 3, y - 4, 3) for x, y, r in keys]) * faces, "#ffffff", 0.6, blur=0.8)
    space = rr_mask(W, H, cx - 150, 556, cx + 150, 572, 7)
    art = chrome(art, space, nx)
    art = add_grain(art, 5, 0.04)
    save(art, f"{OUT}/machine.webp", max_w=760, quality=82)
    preview(art, "mk-machine", "#2e3b3a")


def spool():
    W, H = 180, 180
    nx = Seq(300); rng = random.Random(2)
    art = blank(W, H)
    c = (90, 90)
    flange = circles(W, H, [(90, 90, 84)])
    art = chrome(art, flange, nx)
    wound = circles(W, H, [(90, 90, 70)])
    art = GP(art, wound * (np.mgrid[0:H, 0:W][0] < 90), INK, "#2b282a", seed=nx(), rough=0.5)
    art = GP(art, wound * (np.mgrid[0:H, 0:W][0] >= 90), RED, "#c73a2e", seed=nx(), rough=0.5)
    rings = strokes(W, H, [(arc_pts(90, 90, r, 0, math.tau, 60), 0.9, None) for r in range(30, 70, 5)]) * wound
    art = tint(art, rings, "#000000", 0.25)
    hub = circles(W, H, [(90, 90, 30)])
    art = chrome(art, hub, nx)
    holes = circles(W, H, [(90 + math.cos(a) * 18, 90 + math.sin(a) * 18, 5.5) for a in np.linspace(0, math.tau, 6, endpoint=False)] + [(90, 90, 6)])
    art = tint(art, holes, "#1a1a1a", 0.95)
    art = add_grain(art, 7, 0.04)
    save(art, f"{OUT}/spool.webp", max_w=120, quality=84)


def ribbon():
    W, H = 600, 60
    nx = Seq(400)
    art = blank(W, H)
    top = [(x, 26 + math.sin(x / 600 * math.tau * 2) * 8) for x in range(0, W + 1, 6)]
    poly_t = [(x, y - 6) for x, y in top] + [(x, y) for x, y in top[::-1]]
    poly_b = [(x, y) for x, y in top] + [(x, y + 6) for x, y in top[::-1]]
    art = GP(art, shapes(W, H, [poly_t], smooth=False), INK, seed=nx(), rough=0.6, streak=1.2)
    art = GP(art, shapes(W, H, [poly_b], smooth=False), RED, seed=nx(), rough=0.6, streak=1.2)
    m = shapes(W, H, [[(x, y - 6) for x, y in top] + [(x, y + 6) for x, y in top[::-1]]], smooth=False)
    art = tint(art, m * (fbm(W, H, 4, 8, 2) > 0.62), "#ffffff", 0.12)
    art[..., 3] *= np.clip(np.minimum(np.arange(W)[None, :], W - np.arange(W)[None, :]) / 60, 0, 1)
    save_full(art, f"{OUT}/ribbon.webp", size=(400, 40), quality=82)


def clip():
    W, H = 80, 200
    nx = Seq(500)
    pts = [(48, 186), (48, 40), (40, 22), (28, 22), (20, 40), (20, 160), (28, 176), (36, 176), (42, 160), (42, 50)]
    path = curve(pts, 80)
    m = strokes(W, H, [(path, 5.2, None)])
    art = tint(blank(W, H), np.roll(np.roll(m, 3, 0), 2, 1), "#000000", 0.25, blur=1.5)
    art = chrome(art, m, nx, vertical=True)
    save(art, f"{OUT}/clip.webp", max_w=50, quality=86)


def carbon():
    """Carbon paper sheet: blue-violet waxy coat, smudges, a curled corner."""
    W, H = 600, 420
    nx = Seq(600)
    sheet = shapes(W, H, [[(10, 14), (590, 6), (594, 330), (540, 410), (6, 406)]], smooth=False)
    art = GP(blank(W, H), sheet, "#2b2f55", "#363b68", seed=nx(), rough=0.8, streak=1.4)
    smudge = fbm(W, H, 9, 60, 3)
    art = tint(art, sheet * np.clip((smudge - 0.55) * 3, 0, 1), "#1f2348", 0.6)
    art = tint(art, sheet * np.clip((fbm(W, H, 10, 12, 2) - 0.7) * 4, 0, 1), "#7a7fa8", 0.25)
    curl = shapes(W, H, [[(594, 330), (540, 410), (556, 352)]], smooth=False)
    art = GP(art, curl, "#d9d4c6", "#bdb6a6", seed=nx(), rough=0.4)
    art = tint(art, edge_ring(curl, 1.2), "#7d7768", 0.7)
    save(art, f"{OUT}/carbon.webp", max_w=420, quality=78)


def paper():
    S = 400
    base = col3(PAPER)[None, None] * np.ones((S, S, 3), np.float32)
    v = 1 + (wrap_noise(S, S, 41, 40) - 0.5) * 0.05 + (wrap_noise(S, S, 42, 0.7) - 0.5) * 0.05 + (wrap_noise(S, S, 43, (0.5, 5)) - 0.5) * 0.03
    rgb = base * v[..., None]
    fl = (np.random.default_rng(44).random((S, S)) > 0.9994).astype(np.float32)
    rgb = rgb * (1 - gaussian_filter(fl, 0.6)[..., None] * 0.6)
    save_rgb(rgba(np.clip(rgb, 0, 1), np.ones((S, S), np.float32)), f"{OUT}/paper.webp", quality=72)


def desk():
    """Deep slate-green desk linen (bookcloth) tile."""
    S = 400
    base = col3("#2f3d3b")[None, None] * np.ones((S, S, 3), np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    weave = (np.sin(xx * math.pi / 2) * np.sin(yy * math.pi / 2)) * 0.03
    v = 1 + weave + (wrap_noise(S, S, 51, (0.6, 8)) - 0.5) * 0.10 + (wrap_noise(S, S, 52, (8, 0.6)) - 0.5) * 0.08 + (wrap_noise(S, S, 53, 50) - 0.5) * 0.10
    rgb = base * v[..., None]
    save_rgb(rgba(np.clip(rgb, 0, 1), np.ones((S, S), np.float32)), f"{OUT}/desk.webp", quality=72)


def grain():
    """Ink-coverage mask (white = ink takes): speckled wear for typed text and rubber stamps; tileable."""
    S = 256
    n1 = wrap_noise(S, S, 61, 0.8); n2 = wrap_noise(S, S, 62, 6)
    a = np.clip(1 - np.clip((n1 - 0.68) * 5, 0, 1) * 0.85 - np.clip((n2 - 0.7) * 3, 0, 1) * 0.35, 0, 1)
    im = Image.fromarray((np.stack([np.zeros_like(a)] * 3 + [a], -1) * 255).astype(np.uint8), "RGBA")
    im.save(f"{OUT}/grain.webp", "WEBP", quality=80, method=6)
    print("grain.webp", os.path.getsize(f"{OUT}/grain.webp") // 1024, "KB")


for p in PARTS:
    globals()[p]()
    clear()
