"""Perpustakaan Tua — an old reading room in gouache: walnut shelves packed with leather and cloth spines (raised
bands, gilt lines, paper labels), a rolling ladder on a brass rail, a green banker's lamp with a warm pool of light,
an engraved ex-libris bookplate frame, a printer's fleuron and an aged-paper tile.
Run: python3 -I perpustakaan-tua.py [part ...]   parts: shelf lamp plate spines fleuron paper
Assets -> public/themes/art/perpustakaan-tua/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g6_lib import *  # noqa

OUT = outdir("perpustakaan-tua")
PARTS = sys.argv[1:] or ["shelf", "lamp", "plate", "spines", "fleuron", "paper"]
INK = "#3a2416"
MUTED = [("#5e1c1a", "#6c2620"), ("#1f4532", "#28523c"), ("#1c2f46", "#243a52"), ("#6a4220", "#784c26"),
         ("#3e2416", "#4a2c1c"), ("#7a6038", "#866a40"), ("#33263a", "#3e2e44"), ("#8a4a2a", "#965434"),
         ("#b4a07a", "#c2ae88"), ("#521828", "#5e2030"), ("#2c3a2a", "#364432")]
BRASS, BRASS2, BRASSD, BRASSL = "#b8873e", "#c99a4c", "#4a3014", "#ffe1a0"


def brass(art, m, nx, ldir=(6, 3)):
    art = GP(art, m, BRASS, BRASS2, seed=nx(), rough=0.5, streak=0.6)
    art = tint(art, side_light(m, ldir[0], ldir[1], 4), BRASSD, 0.7, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .6, -ldir[1] * .6, 2.5), BRASSL, 0.55, seed=nx())
    return art


if "shelf" in PARTS:
    W, H = 780, 1180
    nx = Seq(61100); rng = random.Random(611)
    art = painted_sky(W, H, [(0, "#24150d"), (0.5, "#2e1b10"), (1, "#1c100a")], seed=nx(), streak=0.8)
    shelves = [(30, 218), (258, 486), (526, 754), (794, 1022), (1062, 1180)]
    for top, base in shelves:
        # back panel grain inside each bay
        bay = shapes(W, H, [rect(34, top, W - 34, base)], smooth=False)
        art = wood(art, bay, "#2a170e", "#331d12", "#150b06", nx, angle=0.0, ring=11, grain_amt=0.25)
        if base < H:
            art = book_row(art, W, H, 40, W - 40, base, (base - top) * 0.62, (base - top) * 0.92, nx, rng, palette=MUTED, gap=(0.5, 3))
            # the shelf above throws a shadow over the book tops; the back of the bay falls into darkness
            yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
            dk = bay * np.clip(1 - (yy - top) / ((base - top) * 0.8), 0, 1) ** 1.2
            art = tint(art, dk, "#0e0705", 0.85, seed=nx(), clip=False)
            # a horizontal stack in one bay, a gap in another
        clear()
        if base < H:
            art = plank(art, W, H, 0, W, base, 26, nx)
    # vertical uprights
    for x0, x1 in ((0, 36), (W - 36, W)):
        up = shapes(W, H, [rect(x0, 0, x1, H)], smooth=False)
        art = wood(art, up, "#5a3620", "#6a4128", "#24140c", nx, angle=math.pi / 2, ring=9, grain_amt=0.4)
        art = tint(art, side_light(up, 4 if x0 == 0 else -4, 0, 3), "#120a06", 0.5, seed=nx())
    clear()
    # brass rail along the top shelf and the rolling ladder leaning on it
    rail = strokes(W, H, [([(0, 236), (W, 236)], 8, None)])
    art = brass(art, rail, nx, (0, 3))
    lx0, lx1, ly0, ly1 = 470, 560, 236, 1180
    rails = []
    for off in (0, 132):
        rails.append([(lx1 + off, ly1), (lx0 + off, ly0 - 10)])
    lad = shapes(W, H, [[(a[0] - 9, a[1]), (a[0] + 9, a[1]), (b[0] + 8, b[1]), (b[0] - 8, b[1])] for a, b in rails], smooth=False)
    rungs = []
    for k in range(1, 13):
        t = k / 13
        pa = (lx1 + (lx0 - lx1) * t, ly1 + (ly0 - 10 - ly1) * t)
        rungs.append(([pa, (pa[0] + 132, pa[1])], 8, None))
    rm = strokes(W, H, rungs)
    sh = np.roll(np.roll(gaussian_filter(np.clip(lad + rm, 0, 1), 6), 14, 1), 8, 0)
    art = OV(art, sh, lambda mm: col_arr(mm, "#0c0604", mm * 0.6), pad=20)
    art = wood(art, rm, "#7a4e2c", "#8a5a34", "#2a160a", nx, angle=0.0, ring=4, grain_amt=0.35)
    art = tint(art, side_light(rm, 0, 3, 2), "#1a0d06", 0.6, seed=nx())
    art = wood(art, lad, "#7a4e2c", "#8e5e36", "#2a160a", nx, angle=math.pi / 2 - 0.1, ring=6, grain_amt=0.45)
    art = tint(art, side_light(lad, 4, 0, 3), "#1a0d06", 0.55, seed=nx())
    art = tint(art, side_light(lad, -3, 0, 2), "#c89a64", 0.4, seed=nx())
    hooks = circles(W, H, [(lx0 + 2, ly0 - 6, 9), (lx0 + 134, ly0 - 6, 9)])
    art = brass(art, hooks, nx)
    clear()
    # warm lamplight from below-left, cooler shadow top-right
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    warm = np.exp(-(((xx - 120) / 520) ** 2 + ((yy - 1180) / 620) ** 2))
    art = over(art, col_arr(warm, "#ffb766", np.clip(warm * 0.22, 0, 1)))
    mot = fbm(W, H, nx(), 60, 4)[..., None]
    art[..., :3] = np.clip(art[..., :3] * (0.9 + 0.16 * mot), 0, 1)
    art = vignette(art, 0.55, 1.8)
    art = add_grain(art, nx(), 0.045)
    preview(art, "pt-shelf", bg="#1c100a")
    save_rgb(art, f"{OUT}/shelf.webp", size=(520, 787), quality=72)
    clear()

if "lamp" in PARTS:
    W, H = 460, 520
    nx = Seq(61200); rng = random.Random(612)
    art = blank(W, H)
    # pool of light on the desk
    pool = ellipses(W, H, [(230, 470, 210, 34, 0)])
    art = OV(art, pool, lambda mm: col_arr(mm, "#ffcf7a", np.clip(gaussian_filter(mm, 20), 0, 1) * 0.55), pad=60)
    beam = shapes(W, H, [[(110, 235), (350, 235), (430, 470), (30, 470)]], smooth=False)
    art = OV(art, beam, lambda mm: col_arr(mm, "#ffe2a0", np.clip(gaussian_filter(mm, 26), 0, 1) * 0.22), pad=60)
    # base, arm, harp
    base = shapes(W, H, [[(120, 482), (340, 482), (322, 452), (138, 452)]])
    base2 = ellipses(W, H, [(230, 452, 92, 12, 0)])
    stem = shapes(W, H, [rect(220, 250, 240, 456)], smooth=False)
    knob = ellipses(W, H, [(230, 300, 18, 9, 0), (230, 410, 22, 10, 0)])
    bm = np.clip(base + base2 + stem + knob, 0, 1)
    art = brass(art, bm, nx)
    art = OV(art, strokes(W, H, [([(150, 470), (310, 470)], 2.5, None)]), lambda mm: col_arr(mm, "#fff0c8", mm * 0.5), pad=4)
    # chain
    chain = circles(W, H, [(330, 250 + k * 9, 2.6) for k in range(9)])
    art = brass(art, chain, nx)
    art = brass(art, circles(W, H, [(330, 336, 6)]), nx)
    # green glass shade: half-cylinder dome, lit rim, glass highlight
    shade = shapes(W, H, [[(90, 240), (370, 240), (360, 196), (330, 160), (230, 146), (130, 160), (100, 196)]])
    art = GP(art, shade, "#1f5a3a", "#24704a", seed=nx(), rough=0.5, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = np.clip((yy - 146) / 94, 0, 1)
    art = tint(art, shade * (1 - v) ** 1.5, "#0c2a1a", 0.6, seed=nx())
    art = tint(art, shade * np.exp(-((v - 0.72) / 0.12) ** 2), "#4fae78", 0.45, seed=nx())
    hl = strokes(W, H, [([(150, 176), (200, 160), (260, 158)], 6, (0.3, 0.4))])
    art = OV(art, hl, lambda mm: col_arr(mm, "#e8fff0", np.clip(gaussian_filter(mm, 1.5), 0, 1) * 0.6), pad=6)
    inner = ellipses(W, H, [(230, 240, 140, 9, 0)])
    art = OV(art, inner, lambda mm: col_arr(mm, "#fff0b8", np.clip(gaussian_filter(mm, 2), 0, 1) * 0.95), pad=10)
    rimb = strokes(W, H, [([(88, 241), (372, 241)], 4, None)])
    art = brass(art, rimb, nx, (0, 2))
    finial = circles(W, H, [(230, 142, 9)])
    art = brass(art, finial, nx)
    art = edge_fade(art, 30)
    preview(art, "pt-lamp", bg="#2a170e")
    save(art, f"{OUT}/lamp.webp", max_w=230, quality=84)
    clear()

if "plate" in PARTS:
    # ex-libris bookplate frame: engraved double rule, corner scrolls, open book with rays on top, laurel below
    W, H = 640, 860
    nx = Seq(61300); rng = random.Random(613)
    art = blank(W, H)
    items = []
    x0, y0, x1, y1 = 40, 150, W - 40, H - 150
    items += [([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 3.2, None)]
    items += [([(x0 + 12, y0 + 12), (x1 - 12, y0 + 12), (x1 - 12, y1 - 12), (x0 + 12, y1 - 12), (x0 + 12, y0 + 12)], 1.4, None)]
    for cx, cy, sx, sy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        sp = spiral_pts(34, 34, 3, 20, math.pi, 1.5, 40, 1)
        sp = [(cx + px * sx, cy + py * sy) for px, py in sp]
        items.append((sp, 2.4, (0.05, 0.6)))
        items.append(([(cx + sx * 20, cy + sy * 62), (cx + sx * 20, cy + sy * 118)], 1.6, (0.1, 0.9)))
        items.append(([(cx + sx * 62, cy + sy * 20), (cx + sx * 118, cy + sy * 20)], 1.6, (0.1, 0.9)))
    # side beading
    dots = [(x0 + 6, y, 2.2) for y in np.arange(y0 + 130, y1 - 120, 16)] + [(x1 - 6, y, 2.2) for y in np.arange(y0 + 130, y1 - 120, 16)]
    # open book on top with rays
    bx, by = W / 2, 112
    left = [(bx, by + 30), (bx - 96, by + 14), (bx - 100, by - 40), (bx - 4, by - 26)]
    right = [(bx, by + 30), (bx + 96, by + 14), (bx + 100, by - 40), (bx + 4, by - 26)]
    items += [(left + [left[0]], 3.0, None), (right + [right[0]], 3.0, None), ([(bx, by - 26), (bx, by + 30)], 2.2, None)]
    for k in range(5):
        t = (k + 1) / 6
        items.append(([(bx - 92 + 6 * t, by - 32 + 46 * t * 0 + k * 9 - 4), (bx - 16, by - 18 + k * 9)], 1.2, None))
        items.append(([(bx + 16, by - 18 + k * 9), (bx + 92 - 6 * t, by - 32 + k * 9 - 4)], 1.2, None))
    for k in range(13):
        a = math.pi + k * math.pi / 12
        if 0.15 < (k / 12) < 0.85 or True:
            r0, r1 = 120, 150 + (12 if k % 2 else 0)
            items.append(([(bx + math.cos(a) * r0, by - 30 + math.sin(a) * r0 * 0.6), (bx + math.cos(a) * r1, by - 30 + math.sin(a) * r1 * 0.6)], 1.6, (0.0, 0.7)))
    # banner under the book (ribbon scroll)
    items.append(([(bx - 130, by + 6), (bx - 104, by + 22)], 1.6, None))
    items.append(([(bx + 130, by + 6), (bx + 104, by + 22)], 1.6, None))
    # laurel at the bottom: two sprigs rising outward from a tied centre
    lx, ly = W / 2, H - 22
    leaves = []
    for sgn in (-1, 1):
        f = lambda t: (lx + sgn * (6 + t * 190), ly - math.sin(t * 1.6) * 52)
        stem = [f(t) for t in np.linspace(0, 1, 30)]
        items.append((stem, 2.0, (0.05, 0.7)))
        for k in range(10):
            t = 0.1 + k * 0.088
            px, py = f(t); qx, qy = f(t + 0.01)
            ang = math.atan2(qy - py, qx - px)
            for side in (-1, 1):
                L = 21 - k * 0.8
                leaves.append(petal_pts(px, py, L, L * 0.27, ang + side * 0.62, 12))
        leaves.append(petal_pts(*f(1.0), 20, 6, math.atan2(f(1.0)[1] - f(0.98)[1], f(1.0)[0] - f(0.98)[0]), 12))
    items.append(([(lx - 14, ly + 6), (lx, ly - 4), (lx + 14, ly + 6)], 2.0, None))
    m = np.clip(strokes(W, H, items) + circles(W, H, dots) + shapes(W, H, leaves), 0, 1)
    art = LC(art, m, INK, seed=nx(), wear=0.3, rough=1.2)
    # a leaf-hatched shading on the laurels (engraving feel)
    lm = shapes(W, H, leaves)
    art = tint(art, inner_edge(lm, 2.5) * 0 + (lm - gaussian_filter(lm, 1.2) * 0) * hatch(W, H, 0.9, 3.6, 0.3, nx()) * np.clip(gaussian_filter(lm, 2.0) * 1.4 - 0.4, 0, 1), "#f1e6cc", 0.55, seed=nx(), clip=True)
    preview(art, "pt-plate")
    save(art, f"{OUT}/plate.webp", max_w=320, quality=82)
    clear()

if "spines" in PARTS:
    W, H = 620, 300
    nx = Seq(61400); rng = random.Random(614)
    art = blank(W, H)
    base = 270
    x = 20
    picks = [0, 8, 2, 1, 5, 9, 3, 6, 4, 7, 0, 2]
    k = 0
    while x < W - 110:
        w = rng.uniform(30, 52); h = rng.uniform(170, 250)
        c, c2 = LEATHER[picks[k % len(picks)]]
        art, _ = book(art, W, H, x, base, w, h, c, c2, nx, rng, bands=rng.choice([2, 3, 4]), label=rng.choice([None, "#e9dcc0", "#2a1a12"]))
        x += w + 1.5; k += 1
        if k % 4 == 0:
            clear()
    # one book leaning at the end
    art, _ = book(art, W, H, x - 2, base, 34, 200, *LEATHER[1], nx, rng, lean=0.25, bands=3, label="#e9dcc0")
    sh = ellipses(W, H, [(W / 2, base + 6, W / 2, 8, 0)])
    art = over(col_arr(sh, "#120a06", gaussian_filter(sh, 5) * 0.5), art)
    preview(art, "pt-spines", bg="#efe4cc")
    save(art, f"{OUT}/spines.webp", max_w=310, quality=84)
    clear()

if "fleuron" in PARTS:
    W, H = 420, 110
    nx = Seq(61500); rng = random.Random(615)
    art = blank(W, H)
    cx, cy = W / 2, 55
    # hedera leaf (aldus leaf) centre + two scrolling vines
    heart = [(cx, cy + 26)]
    for t in np.linspace(0, 1, 18):
        a = math.pi * 1.5 + t * math.pi
        heart.append((cx + math.sin(t * math.pi) * 26 * (1.1 - t * 0.2) * 1, cy + 26 - t * 52))
    leaf = [(cx, cy + 28), (cx - 24, cy + 8), (cx - 26, cy - 14), (cx - 10, cy - 26), (cx, cy - 12), (cx + 10, cy - 26), (cx + 26, cy - 14), (cx + 24, cy + 8)]
    lm = shapes(W, H, [leaf])
    items = []
    for sgn in (-1, 1):
        vine = [(cx + sgn * (28 + t * 150), cy + math.sin(t * math.pi * 2) * 14) for t in np.linspace(0, 1, 40)]
        items.append((vine, 2.6, (0.05, 0.7)))
        sp = spiral_pts(cx + sgn * 120, cy + 8, 3, 13, 0, 1.4, 30, sgn)
        items.append((sp, 2.0, (0.1, 0.4)))
        items.append(([(cx + sgn * 186, cy), (cx + sgn * 200, cy)], 2.0, None))
    vm = strokes(W, H, items)
    dots = circles(W, H, [(cx - 206, cy, 3.2), (cx + 206, cy, 3.2)])
    art = LC(art, np.clip(lm + vm + dots, 0, 1), "#6b1f1f", seed=nx(), wear=0.25, rough=1.0)
    art = tint(art, strokes(W, H, [([(cx, cy + 22), (cx, cy - 14)], 1.5, None)]) * lm, "#f1e6cc", 0.7, seed=nx())
    preview(art, "pt-fleuron")
    save(art, f"{OUT}/fleuron.webp", max_w=210, quality=84)
    clear()

if "paper" in PARTS:
    n = 512
    nx = Seq(61600)
    base = np.array(hex_rgb("#efe4cc"), np.float32)
    mot = wrap_noise(n, n, nx(), 40)
    fib = wrap_noise(n, n, nx(), 0.8)
    rgb = base[None, None] * (1 + (mot[..., None] - 0.5) * 0.08 + (fib[..., None] - 0.5) * 0.05)
    # foxing: small rust spots
    rs = np.random.default_rng(7)
    spots = np.zeros((n, n), np.float32)
    for _ in range(9):
        x, y = rs.integers(0, n, 2)
        spots[y, x] = rs.uniform(0.5, 1)
    spots = gaussian_filter(spots, 2.6, mode="wrap") * 30
    fox = np.array(hex_rgb("#b07a44"), np.float32)
    rgb = rgb * (1 - np.clip(spots, 0, 0.35)[..., None]) + fox * np.clip(spots, 0, 0.35)[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_texture(arr, f"{OUT}/paper.webp", quality=70)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")
