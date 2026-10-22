"""Tolaki Kendari — gouache dusk: Teluk Kendari at sunset (orange to magenta to indigo sky, the bay with Bungkutoko
island and the hills of Nipa-Nipa, stilt houses on the shore), a raised rumah laika (tall timber posts, plank walls,
long steep sago-thatch roof, ladder) as a standalone piece; a woven band inspired by Tolaki weaving (red, black, gold:
stepped diamonds, hooked spirals, saw-tooth borders) at thread level; a gold-thread diamond emblem and divider.
Run: python3 -I tolaki-kendari.py [part ...]   parts: weave dusk laika diamond divider
Assets -> public/themes/art/tolaki-kendari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g3_lib import *

OUT = outdir("tolaki-kendari")
PARTS = sys.argv[1:] or ["weave", "dusk", "laika", "diamond", "divider"]
BLACK, RED, RED_D, GOLD, GOLD_L, CREAM = "#17110f", "#a8231f", "#6e1512", "#c9963a", "#ecc777", "#f3e6cc"
WOOD, WOOD_D, WOOD_L = "#4a2c1c", "#22140c", "#7a4e32"
THATCH, THATCH_D, THATCH_L = "#6a4a2a", "#3a2614", "#a07a48"


def weave_pattern(n_w=96, n_h=28):
    """Band repeat: black ground, red border rows with saw-tooth, gold stepped diamonds with hooks inside."""
    p = np.zeros((n_h, n_w), np.int32)  # 0 black
    yy, xx = np.mgrid[0:n_h, 0:n_w]
    p[0:2] = 1; p[-2:] = 1                    # red edges
    p[2] = 2; p[-3] = 2                       # gold rule
    # saw-tooth (red) under the gold rules
    tooth = (yy - 3) < (4 - np.abs((xx % 8) - 4))
    p[(yy >= 3) & (yy < 7) & tooth] = 1
    tooth2 = (n_h - 4 - yy) < (4 - np.abs(((xx + 4) % 8) - 4))
    p[(yy <= n_h - 4) & (yy > n_h - 8) & tooth2] = 1
    cy = n_h // 2
    for cx in range(12, n_w, 24):
        d = np.minimum(np.abs(xx - cx), n_w - np.abs(xx - cx)) + np.abs(yy - cy)
        p[(d <= 9) & (d >= 8)] = 2            # outer stepped diamond
        p[(d <= 6) & (d >= 5)] = 1            # red inner ring
        p[d <= 2] = 2                         # gold heart
        # hooks: little spirals out of the diamond tips (left/right)
        for sgn in (-1, 1):
            hx = cx + sgn * 10
            for k in range(3):
                p[cy - 1:cy + 2, (hx + sgn * k) % n_w] = 2
            p[cy - 3:cy - 1, (hx + sgn * 2) % n_w] = 2
        # small red diamonds between motifs
        mx = cx + 12
        dm = np.minimum(np.abs(xx - mx), n_w - np.abs(xx - mx)) + np.abs(yy - cy)
        p[(dm <= 3) & (p == 0)] = 1
        p[(dm <= 1)] = 2
    return p


if "weave" in PARTS:
    pat = weave_pattern()
    art = weave_cells(pat, [BLACK, RED, "#d2a24a", "#2a1c16"], cell=4, seed=21, metallic=(2,), float_len=3, fibre=0.09)
    show(art, "tk-weave")
    save_full(art, f"{OUT}/weave.webp", quality=82)
    clr()


def laika(art, W, H, cx, by, s, rng, nx, lit=0.0):
    """Rumah laika on tall posts. by = ground line, s = scale (house body width ~ 1.0*s)."""
    def P(u, v):
        return (cx + u * s, by + v * s)
    # posts: tall, a little irregular, with cross bracing
    posts = []
    for u in np.linspace(-0.46, 0.46, 6):
        u += rng.uniform(-0.01, 0.01)
        posts.append([P(u - 0.022, 0), P(u + 0.022, 0), P(u + 0.018, -0.62), P(u - 0.018, -0.62)])
    pm = shapes(W, H, posts, smooth=False)
    art = GP(art, pm, WOOD, WOOD_D, seed=nx(), rough=0.6, streak=1.0)
    brace = strokes(W, H, [([P(-0.46, -0.1), P(-0.1, -0.5)], s * 0.012, None), ([P(0.1, -0.5), P(0.46, -0.1)], s * 0.012, None),
                           ([P(-0.48, -0.32), P(0.48, -0.32)], s * 0.014, None)])
    art = GP(art, brace, WOOD_D, seed=nx(), rough=0.4)
    # floor beam + walls
    floor = shapes(W, H, [[P(-0.56, -0.6), P(0.56, -0.6), P(0.56, -0.66), P(-0.56, -0.66)]], smooth=False)
    art = GP(art, floor, WOOD_D, WOOD, seed=nx(), rough=0.5)
    wall = shapes(W, H, [[P(-0.5, -0.66), P(0.5, -0.66), P(0.5, -0.98), P(-0.5, -0.98)]], smooth=False)
    art = GP(art, wall, WOOD_L, WOOD, seed=nx(), rough=0.6, streak=1.3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seams = np.clip((np.abs(((xx - cx) / (s * 0.045)) % 1.0 - 0.5) * 2 - 0.84) * 6, 0, 1) * wall
    art = wash(art, seams, WOOD_D, 0.55, seed=nx())
    art = wash(art, wall * grad(W, H, cx - s * 0.5, 0, cx + s * 0.5, 0), "#1a0d07", 0.4, seed=nx())
    # windows with warm lamp light
    wins = [[P(u - 0.06, -0.74), P(u + 0.06, -0.74), P(u + 0.06, -0.9), P(u - 0.06, -0.9)] for u in (-0.28, 0.0, 0.28)]
    wm = shapes(W, H, wins, smooth=False)
    art = GP(art, wm, "#f2b04a", "#ffd987", seed=nx(), rough=0.4)
    if lit:
        art = over(art, glow(wm, "#ffb24a", radius=10, strength=0.35 * lit))
    art = wash(art, strokes(W, H, [([P(u, -0.74), P(u, -0.9)], s * 0.008, None) for u in (-0.28, 0.0, 0.28)]), WOOD_D, 0.8, seed=nx())
    # long steep sago-thatch roof (gable seen side-on as a big trapezoid; front gable triangle on the left end)
    roof = shapes(W, H, [[P(-0.64, -0.94), P(0.66, -0.94), P(0.44, -1.42), P(-0.42, -1.42)]], smooth=False)
    art = GP(art, roof, THATCH, THATCH_L, seed=nx(), rough=1.4, streak=1.6)
    # thatch strands: many short downward strokes
    st = []
    for _ in range(int(260 * s / 200)):
        u = rng.uniform(-0.6, 0.62); v = rng.uniform(-1.4, -0.98)
        st.append(([P(u, v), P(u + rng.uniform(-0.01, 0.01), v + rng.uniform(0.05, 0.12))], max(1.0, s * 0.006), (0.1, 0.5)))
    sm = strokes(W, H, st) * roof
    art = wash(art, sm, THATCH_D, 0.55, seed=nx())
    st2 = [(pts, w * 0.7, t) for (pts, w, t) in st[::2]]
    art = wash(art, strokes(W, H, st2) * roof * (yy < by - 1.1 * s), THATCH_L, 0.4, seed=nx())
    # thatch courses
    for v in (-1.06, -1.18, -1.30):
        art = wash(art, strokes(W, H, [([P(-0.62 + (v + 0.94) * -0.45, v), P(0.64 - (v + 0.94) * -0.45, v)], s * 0.01, (0.05, 0.05))]) * roof, THATCH_D, 0.5, seed=nx())
    art = wash(art, roof * grad(W, H, 0, by - 1.42 * s, 0, by - 0.94 * s), "#1c1008", 0.25, seed=nx())
    art = wash(art, strokes(W, H, [([P(-0.64, -0.94), P(0.66, -0.94)], s * 0.02, None)]), "#2a1a0e", 0.7, seed=nx())
    # ridge with crossed ends
    ridge = strokes(W, H, [([P(-0.46, -1.42), P(0.48, -1.42)], s * 0.02, None),
                           ([P(-0.46, -1.42), P(-0.5, -1.47)], s * 0.012, (0.0, 0.5)), ([P(0.48, -1.42), P(0.52, -1.47)], s * 0.012, (0.0, 0.5))])
    art = GP(art, ridge, WOOD_D, seed=nx(), rough=0.4)
    # ladder
    lad = strokes(W, H, [([P(-0.2, 0.02), P(-0.12, -0.6)], s * 0.012, None), ([P(-0.08, 0.02), P(0.0, -0.6)], s * 0.012, None)] +
                  [([P(-0.2 + 0.08 * t / 1, 0.02 - 0.62 * t), P(-0.08 + 0.08 * t, 0.02 - 0.62 * t)], s * 0.008, None) for t in np.linspace(0.08, 0.92, 8)])
    art = GP(art, lad, "#5a3a24", seed=nx(), rough=0.3)
    if lit:  # warm rim light from the setting sun on the left edges
        body = np.maximum.reduce([pm, wall, roof])
        art = wash(art, np.clip(body - np.roll(body, 3, 1), 0, 1), "#ffb060", 0.55 * lit, seed=nx())
    return art


if "dusk" in PARTS:
    W, H = 860, 900
    nx = Seq(2100); rng = random.Random(21)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    HZ = 470
    art = painted_sky(W, H, [(0, "#2a1f45"), (0.18, "#5a2c5c"), (0.34, "#b5475a"), (0.45, "#ec8a4a"), (0.52, "#f7c46c"), (1.0, "#f7c46c")], seed=nx())
    SX, SY = W * 0.5, HZ - 150
    art = wash(art, radial(W, H, SX, SY, 380) ** 2.2, "#ffd890", 0.75, seed=nx())
    art = wash(art, radial(W, H, SX, SY, 160) ** 1.5, "#fff0c4", 0.6, seed=nx())
    # long streaky dusk clouds
    for cy_, x0, x1, c in [(160, -40, 380, "#7a3a68"), (230, 420, 900, "#9c4260"), (300, 40, 330, "#d4685a"), (352, 560, 880, "#e27e52"), (110, 520, 820, "#4a2a58")]:
        for j in range(3):
            ox = rng.uniform(-40, 40); oy = rng.uniform(-10, 10)
            cl = shapes(W, H, [deform(ellipse_pts((x0 + x1) / 2 + ox, cy_ + oy, (x1 - x0) / 2 * rng.uniform(0.6, 1.0), rng.uniform(12, 22), 20), rng, 3, 0.08)])
            art = wash(art, gaussian_filter(cl, 3.5), c, 0.55, seed=nx())
    # far hills (Nipa-Nipa) and Bungkutoko island
    far = shapes(W, H, [[(-20, HZ + 2), (-20, HZ - 40), (80, HZ - 70), (180, HZ - 52), (260, HZ - 24), (330, HZ + 2)]])
    art = GP(art, far, "#7a4a6a", "#8a5470", seed=nx(), rough=1.6)
    isl = shapes(W, H, [[(470, HZ + 2), (540, HZ - 16), (640, HZ - 22), (720, HZ - 10), (780, HZ + 2)]])
    art = GP(art, isl, "#6a3e60", "#7a486a", seed=nx(), rough=1.2)
    far2 = shapes(W, H, [[(W + 20, HZ + 2), (W + 20, HZ - 60), (W - 60, HZ - 86), (W - 140, HZ - 60), (W - 200, HZ - 30), (W - 240, HZ + 2)]])
    art = GP(art, far2, "#5e3456", "#6e3e60", seed=nx(), rough=1.6)
    # sea
    sea = (yy >= HZ).astype(np.float32)
    art = wash(art, sea, "#c0605a", 1.0, seed=nx(), col2="#a95060")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, H), "#3a2448", 0.75, seed=nx())
    art = wash(art, sea * np.clip(1 - np.abs(xx - SX) / 110, 0, 1) * np.clip(1 - (yy - HZ) / 300, 0, 1), "#ffd68a", 0.7, seed=nx())
    art = wash(art, sun_glints(W, H, SX, HZ + 4, H - 140, 150, rng, spread=50, col="#ffe2a8") * sea, "#ffe6b0", 0.8, seed=nx())
    # stilt houses along the far shore (silhouettes) + boats
    hs = []
    x = 250
    while x < 470:
        h_ = rng.uniform(9, 17); w_ = rng.uniform(12, 26)
        hs.append([(x, HZ + 3), (x + w_, HZ + 3), (x + w_, HZ - h_ * 0.55), (x + w_ / 2, HZ - h_), (x, HZ - h_ * 0.55)])
        x += w_ + rng.uniform(2, 26)
    art = wash(art, shapes(W, H, hs, smooth=False), "#5a3050", 0.85, seed=nx())
    for bx, by_, bs in [(360, 560, 22), (610, 520, 14), (200, 610, 28)]:
        hull = shapes(W, H, [[(bx - bs, by_), (bx + bs, by_), (bx + bs * 0.75, by_ + bs * 0.25), (bx - bs * 0.75, by_ + bs * 0.25)]])
        art = GP(art, hull, "#2a1828", seed=nx(), rough=0.4)
        art = wash(art, strokes(W, H, [([(bx + bs * 0.95, by_ - 1), (bx + bs * 1.5, by_ - bs * 0.5)], 2.0, (0.1, 0.1))]), "#2a1828", 0.9, seed=nx())
    # foreground: dark shore bank with grass, palms and the laika on the right
    bank = shapes(W, H, [[(-20, H + 20), (-20, 760), (200, 730), (420, 742), (600, 716), (W + 20, 690), (W + 20, H + 20)]])
    art = GP(art, bank, "#2a1a20", "#33202a", seed=nx(), rough=2.0, streak=1.0)
    art = wash(art, grass_tufts(W, H, 700, H, 160, rng, 10, 40, 0.2, 2.2) * (yy > 680), "#1a1014", 0.85, seed=nx())
    art = wash(art, np.clip(bank - np.roll(bank, 3, 0), 0, 1), "#ff9a5a", 0.5, seed=nx())
    pre = art.copy()
    art = laika(art, W, H, 650, 730, 230, rng, nx, lit=1.0)
    house = np.clip(np.abs(art[..., :3] - pre[..., :3]).sum(-1) * 20, 0, 1)
    art = wash(art, house * (1 - np.clip(gaussian_filter(np.clip(house - np.roll(house, 4, 1), 0, 1), 1) * 3, 0, 1)), "#3a2038", 0.38, seed=nx())
    for px, h_, lean in [(80, 380, 0.2), (180, 280, -0.08)]:
        pm = palm2(W, H, px, 780, h_, rng, lean)
        art = GP(art, pm, "#22141c", "#2a1822", seed=nx(), rough=0.6)
        art = wash(art, np.clip(pm - np.roll(pm, 2, 1), 0, 1), "#ff9a5a", 0.35, seed=nx())
    art = add_grain(art, seed=nx(), amount=0.03)
    show(art, "tk-dusk")
    save_rgb(art, f"{OUT}/dusk.webp", size=(780, 816), quality=76)
    clr()

if "laika" in PARTS:
    W, H = 560, 500
    nx = Seq(2200); rng = random.Random(22)
    art = blank(W, H)
    ground = shapes(W, H, [deform(ellipse_pts(W / 2, 470, 250, 18, 20), rng, 2, 0.04)])
    art = GP(art, ground, "#3a2a20", "#4a3626", seed=nx(), rough=1.4)
    art = laika(art, W, H, W / 2, 466, 300, rng, nx, lit=0.6)
    show(art, "tk-laika", bg="#1d1513")
    save(art, f"{OUT}/laika.webp", max_w=440, quality=82)
    clr()

if "diamond" in PARTS:
    W = H = 260
    nx = Seq(2300)
    c = W / 2
    def dia(r):
        return [(c, c - r), (c + r, c), (c, c + r), (c - r, c)]
    outer = np.clip(shapes(W, H, [dia(110)], smooth=False) - shapes(W, H, [dia(96)], smooth=False), 0, 1)
    mid = np.clip(shapes(W, H, [dia(78)], smooth=False) - shapes(W, H, [dia(60)], smooth=False), 0, 1)
    core = shapes(W, H, [dia(32)], smooth=False)
    hooks = []
    for a in range(4):
        ang = a * math.pi / 2
        tx, ty = c + math.cos(ang) * 110, c + math.sin(ang) * 110
        sp = [(tx + math.cos(ang) * 6 + math.cos(ang + 1.6) * r_ * math.cos(t) , ty + math.sin(ang) * 6 + math.sin(ang + 1.6) * r_ * math.sin(t)) for t, r_ in zip(np.linspace(0, 4.2, 20), np.linspace(14, 4, 20))]
        hooks.append((sp, 5, (0.0, 0.5)))
    hm = strokes(W, H, hooks)
    art = blank(W, H)
    art = GP(art, shapes(W, H, [dia(94)], smooth=False), BLACK, "#2a1c16", seed=nx(), rough=0.8)
    art = GP(art, mid, RED, RED_D, seed=nx(), rough=0.6)
    art = FO(art, np.clip(outer + core + hm, 0, 1), GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    art = FO(art, shapes(W, H, [dia(12)], smooth=False), GOLD_L, seed=nx(), sparkle=0.2)
    show(art, "tk-diamond", bg="#1d1513")
    save(art, f"{OUT}/diamond.webp", max_w=160, quality=84)
    clr()

if "divider" in PARTS:
    W, H = 460, 70
    nx = Seq(2400)
    c = W / 2; cy = H / 2
    def dia(x, r):
        return [(x, cy - r), (x + r, cy), (x, cy + r), (x - r, cy)]
    lines = strokes(W, H, [([(20, cy), (c - 34, cy)], 3, (0.3, 0.0)), ([(c + 34, cy), (W - 20, cy)], 3, (0.0, 0.3))])
    gold = np.clip(lines + np.clip(shapes(W, H, [dia(c, 26)], smooth=False) - shapes(W, H, [dia(c, 19)], smooth=False), 0, 1)
                   + shapes(W, H, [dia(c - 52, 8), dia(c + 52, 8), dia(c - 84, 5), dia(c + 84, 5)], smooth=False), 0, 1)
    art = blank(W, H)
    art = GP(art, shapes(W, H, [dia(c, 15)], smooth=False), RED, RED_D, seed=nx(), rough=0.4)
    art = FO(art, gold, GOLD, seed=nx(), emboss=0.6, sparkle=0.1)
    show(art, "tk-divider", bg="#1d1513")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clr()
