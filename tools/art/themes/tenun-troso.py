"""Tenun Troso — weft-ikat (tenun ikat pakan) of Troso, Jepara: madder red, ochre, indigo and natural cream with the
feathered ikat blur; a wooden ATBM handloom seen from the weaver's bench; Jepara countryside with cloths drying.
Run: python3 -I tenun-troso.py [part ...]  parts: ikat band loom desa fringe motif divider
Assets -> public/themes/art/tenun-troso/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n4_lib import *

OUT = outdir("tenun-troso")
PARTS = sys.argv[1:] or ["ikat", "band", "loom", "desa", "fringe", "motif", "divider"]
RED, RED_D = "#93291f", "#6e1c16"
OCH, OCH_L = "#c98a2e", "#e0b25a"
IND, IND_D = "#26375c", "#18233d"
CRM = "#efe2c6"
BRN = "#3b2317"
TEAK, TEAK_D, TEAK_L = "#7a4a26", "#45260f", "#a26a3a"
PAL = [RED, OCH, IND, CRM, BRN, RED_D]  # indices 0..5


def q(v, step):
    return np.floor(v / step) * step + step / 2


def diamond_tile(W, H, cx, cy, s, step=4):
    """Index map contribution for a Troso 'wajik' lattice medallion around periodic centre; returns idx (-1 = none)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    X = q(xx, step); Y = q(yy, step)
    dx = (X - cx + W / 2) % W - W / 2
    dy = (Y - cy + H / 2) % H - H / 2
    d = np.abs(dx) / s + np.abs(dy) / (s * 1.25)
    idx = np.full((H, W), -1, np.int32)
    idx[d < 1.0] = 2                     # indigo outer
    idx[d < 0.86] = 3                    # cream ring
    idx[d < 0.76] = 1                    # ochre
    idx[d < 0.52] = 0                    # red
    idx[d < 0.40] = 3                    # cream
    idx[d < 0.28] = 2                    # indigo
    idx[d < 0.12] = 1                    # ochre heart
    # hooks (kait): stepped arms along the diagonals inside the ochre ring
    arm = (np.abs(np.abs(dx) - np.abs(dy) / 1.25) < s * 0.07) & (d > 0.56) & (d < 0.74)
    idx[arm] = 4
    # tiny cream ticks on the indigo edge
    tick = (d > 0.9) & (d < 1.0) & ((np.floor((dx + dy) / (step * 2)) % 3) == 0)
    idx[tick] = 3
    return idx


def ikat_idx(W, H, s=None, step=4):
    s = s or W * 0.36
    idx = np.zeros((H, W), np.int32)  # red ground
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    X = q(xx, step); Y = q(yy, step)
    # small ochre/cream crosses between medallions (offset lattice)
    for (cx, cy) in [(0, 0), (W / 2, H / 2)]:
        d = diamond_tile(W, H, cx, cy, s, step)
        idx = np.where(d >= 0, d, idx)
    for (cx, cy) in [(W / 2, 0), (0, H / 2)]:
        dx = (X - cx + W / 2) % W - W / 2; dy = (Y - cy + H / 2) % H - H / 2
        d = np.abs(dx) / (s * 0.34) + np.abs(dy) / (s * 0.42)
        idx[d < 1] = 5
        idx[d < 0.7] = 1
        idx[d < 0.36] = 3
        bar = ((np.abs(dx) < step * 0.6) & (np.abs(dy) < s * 0.62) & (d >= 1)) | ((np.abs(dy) < step * 0.6) & (np.abs(dx) < s * 0.5) & (d >= 1))
        idx[bar] = 1
    return idx


def ikat():
    W = H = 384
    idx = ikat_idx(W, H)
    rgb = ikat_render(idx, PAL, 11, weft=3, shift=2.6, blur=1.5)
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/ikat.webp", quality=76)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{PREV}/tt-ikat.png")


def band():
    """Horizontal Troso border band (tumpal teeth + stripes), seamless repeat-x, 384x150."""
    W, H = 384, 150
    step = 4
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    X = q(xx, step); Y = q(yy, step)
    idx = np.full((H, W), 0, np.int32)
    idx[(Y < 10)] = 4
    idx[(Y >= 10) & (Y < 16)] = 3
    idx[(Y >= 16) & (Y < 26)] = 2
    idx[(Y >= 124) & (Y < 134)] = 2
    idx[(Y >= 134) & (Y < 140)] = 3
    idx[(Y >= 140)] = 4
    # tumpal teeth pointing down + up, period 64
    p = 64
    u = (X % p) - p / 2
    tooth = (Y > 28) & (Y < 120) & (np.abs(u) < (120 - Y) * 0.34)
    idx[tooth] = 1
    inner = (Y > 40) & (Y < 112) & (np.abs(u) < (112 - Y) * 0.2)
    idx[inner] = 2
    core = (Y > 52) & (Y < 104) & (np.abs(u) < (104 - Y) * 0.08)
    idx[core] = 3
    u2 = ((X + p / 2) % p) - p / 2
    small = (Y > 82) & (Y < 122) & (np.abs(u2) < (Y - 82) * 0.32)
    idx[small] = 3
    dots = (Y > 30) & (Y < 40) & (np.abs(u2) < 4)
    idx[dots] = 3
    rgb = ikat_render(idx, PAL, 21, weft=3, shift=2.2, blur=1.4)
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/band.webp", quality=78)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{PREV}/tt-band.png")


def loom():
    """ATBM handloom seen from the weaver's bench: two teak posts, top crossbar with pulleys and cords, two heddle
    frames, warp threads converging to the warp beam, the reed/beater, the woven ikat on the breast beam, a shuttle."""
    W, H = 760, 640
    nx = Seq(900)
    rng = random.Random(4)
    art = blank(W, H)
    cx = W / 2
    # perspective: far (top) width narrower
    def X(u, y):
        t = y / H
        half = (W * 0.30) + (W * 0.17) * t
        return cx + u * half
    # ---- warp threads (far beam -> reed)
    beam_y, reed_y, cloth_y, breast_y = 70, 410, 418, 560
    warp = []
    warp_cols = []
    n = 120
    for i in range(n):
        u = -1 + 2 * (i + 0.5) / n
        x0, x1 = X(u * 0.86, beam_y), X(u * 0.94, reed_y)
        warp.append(([(x0, beam_y), (x0 + (x1 - x0) * 0.5 + rng.gauss(0, 0.4), (beam_y + reed_y) / 2), (x1, reed_y)], 1.9, None))
    wm = strokes(W, H, warp)
    # Troso warp is a single dyed colour: deep madder, with lighter sheen threads
    wcol = np.ones((H, W, 3), np.float32) * col3("#8a2a1f")
    sheen = fbm(W, H, 3, 6, 2)
    wcol = wcol * (0.85 + 0.35 * sheen[..., None])
    xs = np.arange(W)[None, :]
    lift = (np.sin(xs * 0.9) > 0.6).astype(np.float32)[..., None] * 0.18
    wcol = np.clip(wcol + lift * col3("#e3b48a"), 0, 1)
    art = over(art, rgba(wcol, wm))
    # ---- woven cloth between reed and breast beam (ikat crop with perspective-ish taper)
    ch = breast_y - cloth_y + 10
    idx = ikat_idx(384, 384)
    cloth = ikat_render(idx, PAL, 31, weft=3, shift=2.6, blur=1.5)
    cl = np.asarray(Image.fromarray((cloth * 255).astype(np.uint8)).resize((int(W * 0.92), ch), Image.LANCZOS), np.float32) / 255
    cmask = shapes(W, H, [[(X(-0.95, cloth_y), cloth_y), (X(0.95, cloth_y), cloth_y), (X(0.98, breast_y + 6), breast_y + 6), (X(-0.98, breast_y + 6), breast_y + 6)]], smooth=False)
    layer = np.zeros((H, W, 4), np.float32)
    ox = int(W * 0.04)
    layer[cloth_y:cloth_y + ch, ox:ox + cl.shape[1], :3] = cl
    layer[..., 3] = cmask
    # fell shading (where new weft meets warp) and slight wave
    sh = np.clip(1 - (np.arange(H)[:, None] - cloth_y) / 26, 0, 1) * cmask * 0.35
    layer[..., :3] *= (1 - sh[..., None])
    art = over(art, layer)
    # ---- posts
    for side in (-1, 1):
        post = shapes(W, H, [[(X(side * 1.04, 0) - 14, 0), (X(side * 1.04, 0) + 14, 0), (X(side * 1.06, H) + 18, H), (X(side * 1.06, H) - 18, H)]], smooth=False)
        art = GP(art, post, TEAK, TEAK_D, seed=nx(), rough=1.5, streak=1.4)
        art = G(art, post * np.clip((np.arange(W)[None, :] - (X(side * 1.04, 300))) * side / 12, 0, 1), TEAK_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    # ---- top crossbar + pulleys + cords to heddles
    top = shapes(W, H, [[(X(-1.12, 22), 18), (X(1.12, 22), 18), (X(1.12, 22), 40), (X(-1.12, 22), 42)]], smooth=False)
    art = GP(art, top, TEAK_L, TEAK, seed=nx(), rough=1.4, streak=1.4)
    heddles = [(205, 236), (262, 292)]
    cords = []
    pul = []
    for u in (-0.55, 0.55):
        px = X(u, 46)
        pul.append((px, 56, 13))
        cords += [([(px - 10, 58), (X(u * 1.1, heddles[0][0]) - 6, heddles[0][0])], 1.6, None), ([(px + 10, 58), (X(u * 1.1, heddles[1][0]) + 6, heddles[1][0])], 1.6, None)]
    art = GP(art, strokes(W, H, cords), "#d9c39a", "#b79d70", seed=nx(), rough=0.4, streak=0.3)
    pm = circles(W, H, pul)
    art = GP(art, pm, TEAK_D, seed=nx(), rough=0.8)
    art = GP(art, circles(W, H, [(x, y, 5) for x, y, _ in pul]), "#c9a466", seed=nx(), rough=0.4)
    # ---- heddle frames: two bars each + vertical heddle strings
    for (y0, y1) in heddles:
        hs = []
        for i in range(0, n, 2):
            u = -1 + 2 * (i + 0.5) / n
            x = X(u * 0.9, (y0 + y1) / 2)
            hs.append(([(x, y0), (x, y1)], 0.9, None))
        art = OV(art, strokes(W, H, hs), lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#5b4630"), m * 0.75))
        bars = shapes(W, H, [[(X(-1.0, y0), y0 - 5), (X(1.0, y0), y0 - 5), (X(1.0, y0), y0 + 4), (X(-1.0, y0), y0 + 4)],
                             [(X(-1.0, y1), y1 - 4), (X(1.0, y1), y1 - 4), (X(1.0, y1), y1 + 5), (X(-1.0, y1), y1 + 5)]], smooth=False)
        art = GP(art, bars, TEAK_L, TEAK, seed=nx(), rough=1.0, streak=1.2)
    # ---- far warp beam
    wb = shapes(W, H, [[(X(-0.95, beam_y), beam_y - 10), (X(0.95, beam_y), beam_y - 10), (X(0.95, beam_y), beam_y + 8), (X(-0.95, beam_y), beam_y + 8)]], smooth=False)
    art = GP(art, wb, TEAK, TEAK_D, seed=nx(), rough=1.0, streak=1.2)
    wbc = shapes(W, H, [[(X(-0.86, beam_y), beam_y - 6), (X(0.86, beam_y), beam_y - 6), (X(0.86, beam_y), beam_y + 4), (X(-0.86, beam_y), beam_y + 4)]], smooth=False)
    art = GP(art, wbc, "#e9d7b0", "#d1b98a", seed=nx(), rough=0.8, streak=1.0)
    # ---- reed / beater (batten): frame with comb teeth
    ry0, ry1 = reed_y - 60, reed_y + 6
    teeth = []
    for i in range(0, 200):
        u = -0.97 + 1.94 * i / 199
        x = X(u, reed_y)
        teeth.append(([(x, ry0 + 10), (x, ry1 - 4)], 0.8, None))
    art = OV(art, strokes(W, H, teeth), lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#6d6a63"), m * 0.55))
    rb = shapes(W, H, [[(X(-1.03, ry0), ry0 - 2), (X(1.03, ry0), ry0 - 2), (X(1.03, ry0), ry0 + 12), (X(-1.03, ry0), ry0 + 12)],
                       [(X(-1.05, ry1), ry1 - 10), (X(1.05, ry1), ry1 - 10), (X(1.05, ry1), ry1 + 12), (X(-1.05, ry1), ry1 + 12)]], smooth=False)
    art = GP(art, rb, TEAK_L, TEAK, seed=nx(), rough=1.2, streak=1.4)
    art = OV(art, soft_shadow(rb, BRN, 5, 0.45, 0, 6), lambda m: m) if False else art
    # beater handle in the middle
    hd = shapes(W, H, [[(cx - 22, ry0 - 12), (cx + 22, ry0 - 12), (cx + 16, ry0 + 2), (cx - 16, ry0 + 2)]], smooth=False)
    art = GP(art, hd, TEAK_D, TEAK, seed=nx(), rough=0.8)
    # ---- breast beam (front, big)
    bb = shapes(W, H, [[(-10, breast_y), (W + 10, breast_y), (W + 10, breast_y + 44), (-10, breast_y + 48)]], smooth=False)
    shade = soft_shadow(bb, BRN, 8, 0.5, 0, -6)
    art = over(art, shade)
    art = GP(art, bb, TEAK_L, TEAK_D, seed=nx(), rough=1.6, streak=1.6)
    hi = shapes(W, H, [[(-10, breast_y + 4), (W + 10, breast_y + 4), (W + 10, breast_y + 10), (-10, breast_y + 10)]], smooth=False)
    art = OV(art, hi, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#c99a62"), m * 0.55))
    # rolled cloth peeking under the beam
    roll = shapes(W, H, [[(X(-0.98, H), breast_y + 44), (X(0.98, H), breast_y + 44), (X(0.98, H), breast_y + 72), (X(-0.98, H), breast_y + 72)]], smooth=False)
    rl = np.zeros((H, W, 4), np.float32)
    band_c = ikat_render(ikat_idx(384, 384)[:120], PAL, 41, weft=3, shift=2.4, blur=1.4, wrap=False)
    bc = np.asarray(Image.fromarray((band_c * 255).astype(np.uint8)).resize((W, 30)), np.float32) / 255
    rl[breast_y + 43:breast_y + 73, :, :3] = bc
    rl[..., 3] = roll
    rl[..., :3] *= 0.72
    art = over(art, rl)
    # ---- shuttle (teropong) resting on the cloth
    sx, sy, L = cx + 70, 470, 190
    sh_pts = [(sx - L / 2, sy + 2), (sx - L * 0.3, sy - 13), (sx + L * 0.3, sy - 13), (sx + L / 2, sy + 2), (sx + L * 0.3, sy + 13), (sx - L * 0.3, sy + 13)]
    shm = shapes(W, H, [sh_pts])
    art = over(art, soft_shadow(shm, BRN, 4, 0.55, 3, 7))
    art = GP(art, shm, "#b07a42", "#7d4f26", seed=nx(), rough=0.8, streak=1.2)
    slot = shapes(W, H, [[(sx - L * 0.2, sy - 5), (sx + L * 0.2, sy - 5), (sx + L * 0.2, sy + 5), (sx - L * 0.2, sy + 5)]])
    art = GP(art, slot, BRN, seed=nx(), rough=0.5)
    bob = shapes(W, H, [[(sx - L * 0.17, sy - 4), (sx + L * 0.17, sy - 4), (sx + L * 0.17, sy + 4), (sx - L * 0.17, sy + 4)]], smooth=False)
    art = GP(art, bob, OCH, OCH_L, seed=nx(), rough=0.4, streak=2)
    thread = strokes(W, H, [(curve([(sx - L * 0.1, sy), (sx - L * 0.6, sy + 10), (X(-0.9, cloth_y + 6), cloth_y + 6)], 30), 1.4, None)])
    art = OV(art, thread, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3(OCH_L), m))
    # tips
    art = GP(art, circles(W, H, [(sx - L / 2 + 6, sy + 2, 4), (sx + L / 2 - 6, sy + 2, 4)]), "#d8d2c4", seed=nx(), rough=0.3)
    art = add_grain(art, 5, 0.035)
    preview(art, "tt-loom", bg=CRM)
    save(art, f"{OUT}/loom.webp", max_w=640, quality=76)


def coco(W, H, x, by, h, rng, lean=0.1):
    """Coconut palm: curved ringed trunk and a crown of drooping fronds with comb-like leaflets."""
    top = (x + lean * h, by - h)
    tr = curve([(x, by), (x + lean * h * 0.25, by - h * 0.5), top], 30)
    trunk = strokes(W, H, [(tr, h * 0.035, (0.0, 0.0))])
    items = []
    for k in range(11):
        a = -math.pi / 2 + (k - 5) * 0.36 + rng.uniform(-0.12, 0.12)
        L = h * rng.uniform(0.3, 0.42)
        droop = L * (0.25 + 0.35 * abs(math.cos(a)))
        pts = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - L * 0.08),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + droop)], 22)
        items.append((pts, h * 0.012, (0.05, 0.5)))
        for j in range(2, 21):
            px, py = pts[j]; qx, qy = pts[j + 1]
            ang = math.atan2(qy - py, qx - px)
            ll = L * 0.17 * (1 - j / 26)
            for sd in (-1, 1):
                qa = ang + sd * 1.05 + 0.35
                items.append(([(px, py), (px + math.cos(qa) * ll, py + math.sin(qa) * ll + ll * 0.5)], h * 0.009, (0.0, 0.6)))
    return trunk, strokes(W, H, items)


def desa():
    """Jepara countryside: Muria in haze, paddy terraces, coconut palms, a limasan house with red tiles, and Troso
    cloths drying on a bamboo line."""
    W, H = 760, 500
    nx = Seq(1300)
    rng = random.Random(7)
    art = painted_sky(W, H, [(0, "#e9d6b4"), (0.3, "#f1e2c4"), (0.55, "#efdcb9"), (1, "#e3cfa6")], seed=3, streak=1.0)
    # Muria
    mur = shapes(W, H, [[(-20, H * 0.5), (W * 0.18, H * 0.34), (W * 0.36, H * 0.2), (W * 0.46, H * 0.17), (W * 0.58, H * 0.24), (W * 0.78, H * 0.33), (W + 20, H * 0.42), (W + 20, H * 0.6), (-20, H * 0.6)]])
    art = G(art, mur, "#a9a7a0", "#8e9592", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=6)
    hl = hills(W, H, H * 0.47, 16, 3, 0.7)
    art = G(art, hl, "#8d9b74", "#7c8a63", seed=nx(), density=0.7, edge=0.35, bloom=0.3, rough=5)
    # paddy terraces: horizontal curved bands
    for k in range(7):
        y = H * 0.55 + k * k * 4.5 + k * 10
        pts = [(-20, H + 20)] + [(x, y + 8 * math.sin(x / 90 + k)) for x in np.arange(-20, W + 40, 20)] + [(W + 20, H + 20)]
        band = shapes(W, H, [pts], smooth=False)
        c = ["#a8b562", "#c9b36a", "#9fb38a", "#86994a", "#d0b560", "#7f9446", "#97a854"][k]
        art = G(art, band, c, mix(c, "#5f7536", 0.3), seed=nx(), density=0.75, edge=0.5, bloom=0.3, rough=4)
        # bund line
        bund = strokes(W, H, [([(x, y + 8 * math.sin(x / 90 + k)) for x in np.arange(-20, W + 40, 20)], 2 + k * 0.5, None)])
        art = G(art, bund, "#6a7a3a", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1.5)
    # rows of rice tufts in the near terraces
    tufts = []
    for _ in range(420):
        x = rng.uniform(0, W); y = rng.uniform(H * 0.74, H)
        s = 2 + (y - H * 0.7) / H * 10
        for a in (-0.5, -0.15, 0.2, 0.5):
            tufts.append(([(x, y), (x + math.sin(a) * s, y - s * 1.3)], 1.0 + s * 0.12, (0.0, 0.7)))
    art = G(art, strokes(W, H, tufts), "#4e6a2a", "#6d8a36", seed=nx(), density=0.85, edge=0.15, bloom=0, rough=0.8)
    # palms
    for (x, by, h, lean) in [(W * 0.07, H * 0.64, 250, 0.14), (W * 0.17, H * 0.61, 175, -0.06), (W * 0.86, H * 0.6, 245, -0.13), (W * 0.95, H * 0.63, 165, 0.1)]:
        trunk, fr = coco(W, H, x, by, h, rng, lean)
        art = GP(art, trunk, "#7b6a4e", "#5a4a33", seed=nx(), rough=0.8, streak=1.2)
        art = G(art, fr, "#4f6e32", "#2f4a22", seed=nx(), density=0.92, edge=0.5, bloom=0.2, rough=1.2, feather=0.7)
    # limasan house
    hx, hy = W * 0.66, H * 0.56
    wall = shapes(W, H, [[(hx - 70, hy - 30), (hx + 70, hy - 30), (hx + 70, hy + 14), (hx - 70, hy + 14)]], smooth=False)
    art = GP(art, wall, "#e8dcc2", "#d7c6a2", seed=nx(), rough=1.2)
    roof = shapes(W, H, [[(hx - 92, hy - 28), (hx - 40, hy - 74), (hx + 40, hy - 74), (hx + 92, hy - 28)]], smooth=False)
    art = GP(art, roof, "#a8452c", "#7f2f1d", seed=nx(), rough=1.4, streak=1.4)
    tiles = strokes(W, H, [([(hx - 92 + k * 9, hy - 28), (hx - 40 + k * 4.4, hy - 74)], 1.2, None) for k in range(20)])
    art = G(art, tiles * roof, "#5e2214", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    door = shapes(W, H, [[(hx - 12, hy - 18), (hx + 12, hy - 18), (hx + 12, hy + 14), (hx - 12, hy + 14)]], smooth=False)
    art = GP(art, door, "#5a3a22", seed=nx(), rough=0.8)
    for wx in (hx - 46, hx + 32):
        art = GP(art, shapes(W, H, [[(wx, hy - 18), (wx + 14, hy - 18), (wx + 14, hy - 2), (wx, hy - 2)]], smooth=False), "#5a3a22", seed=nx(), rough=0.6)
    # bamboo line with drying ikat cloths
    ly = H * 0.62
    poles = strokes(W, H, [([(W * 0.24, ly + 40), (W * 0.245, ly - 34)], 5, None), ([(W * 0.54, ly + 44), (W * 0.535, ly - 30)], 5, None)])
    art = GP(art, poles, "#b99a5e", "#8d6f3c", seed=nx(), rough=0.8)
    line = curve([(W * 0.24, ly - 30), (W * 0.39, ly - 22), (W * 0.54, ly - 27)], 30)
    art = OV(art, strokes(W, H, [(line, 2.2, None)]), lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#8d6f3c"), m))
    cloth_src = ikat_render(ikat_idx(192, 192, s=70), PAL, 51, weft=2, shift=1.6, blur=1.0)
    cloth_src2 = ikat_render(ikat_idx(192, 192, s=70), [IND, CRM, RED, OCH, BRN, IND_D], 52, weft=2, shift=1.6, blur=1.0)
    for k, (x0, x1, h, tint) in enumerate([(0.255, 0.31, 58, 1.0), (0.322, 0.395, 66, 0.0), (0.405, 0.46, 54, 1.0), (0.47, 0.527, 62, 0.0)]):
        xa, xb = W * x0, W * x1
        ya = ly - 27 + 5 * math.sin((x0 - 0.24) / 0.3 * math.pi)
        poly = [(xa, ya), (xb, ya + 1), (xb + 2, ya + h), (xa + (xb - xa) * 0.5, ya + h + 4), (xa - 1, ya + h - 1)]
        cm = shapes(W, H, [poly], smooth=False)
        lay = np.zeros((H, W, 4), np.float32)
        src = cloth_src if tint else cloth_src2
        tile = np.asarray(Image.fromarray((np.clip(src, 0, 1) * 255).astype(np.uint8)).resize((int(xb - xa) + 6, h + 8)), np.float32) / 255
        y0 = int(ya); x0i = int(xa) - 2
        lay[y0:y0 + tile.shape[0], x0i:x0i + tile.shape[1], :3] = tile
        fold = (np.sin((np.arange(W)[None, :] - xa) / 6) * 0.06 + 0.97)
        lay[..., :3] *= fold[..., None]
        lay[..., 3] = cm
        art = over(art, lay)
    art = add_grain(art, 9, 0.03)
    preview(art, "tt-desa")
    save_rgb(art, f"{OUT}/desa.webp", size=(720, int(720 * H / W)), quality=80)


def fringe():
    """Cloth end with knotted warp fringe (rumbai), repeat-x 384x70 (cloth on top, tassels hanging)."""
    W, H = 384, 76
    idx = np.zeros((H, W), np.int32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    idx[(yy < 8)] = 3
    idx[(yy >= 8) & (yy < 18)] = 2
    idx[(yy >= 18) & (yy < 24)] = 1
    rgb = ikat_render(idx, PAL, 61, weft=3, shift=1.6, blur=1.2)
    cm = (yy < 24).astype(np.float32)
    rng = random.Random(3)
    items = []
    for x in np.arange(3, W, 12):
        # a knotted bundle: 4 threads gathered then spreading
        kx = x + 3
        for j in range(4):
            x0 = x + j * 2
            L = rng.uniform(44, 52)
            items.append(([(x0, 22), (kx, 34), (kx + (j - 1.5) * 1.6 + rng.gauss(0, 0.6), 34 + L * 0.5), (kx + (j - 1.5) * 2.6 + rng.gauss(0, 1), 22 + L)], 1.3, (0.0, 0.3)))
    tm = strokes(W, H, items)
    knots = circles(W, H, [(x + 3, 34, 3.2) for x in np.arange(3, W, 12)])
    tcol = np.ones((H, W, 3), np.float32) * col3(RED) * (0.9 + 0.2 * fbm(W, H, 2, 4, 2))[..., None]
    out = rgba(rgb * cm[..., None] + tcol * (1 - cm[..., None]), np.maximum(cm, np.maximum(tm, knots)))
    out[..., :3] = np.where(knots[..., None] > 0.3, col3(RED_D)[None, None], out[..., :3])
    save_full(out, f"{OUT}/fringe.webp", quality=80)
    preview(out, "tt-fringe", bg=CRM)


def motif():
    """Single Troso wajik medallion cut from the cloth with frayed edges (nodes, portrait badge, emblem)."""
    W = H = 280
    idx = np.zeros((H, W), np.int32)
    d = diamond_tile(W, H, W / 2, H / 2, W * 0.44, 4)
    idx = np.where(d >= 0, d, 0)
    rgb = ikat_render(idx, PAL, 71, weft=3, shift=2.0, blur=1.3, wrap=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dd = np.abs(xx - W / 2) / (W * 0.47) + np.abs(yy - H / 2) / (H * 0.47 * 1.0)
    m = (dd < 1).astype(np.float32)
    a = fray(m, 72, 2.5, 0.5)
    art = rgba(rgb, a)
    preview(art, "tt-motif", bg=CRM)
    save(art, f"{OUT}/motif.webp", max_w=220, quality=82)


def divider():
    """Short strip of ikat with frayed ends: three small wajik in a row."""
    W, H = 360, 48
    step = 3
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    X = q(xx, step); Y = q(yy, step)
    idx = np.zeros((H, W), np.int32)
    for k, cx in enumerate([W / 2 - 58, W / 2, W / 2 + 58]):
        d = np.abs(X - cx) / 26 + np.abs(Y - H / 2) / 20
        idx[d < 1] = 2
        idx[d < 0.72] = 1 if k != 1 else 3
        idx[d < 0.4] = 0 if k != 1 else 2
    idx[(np.abs(Y - H / 2) < 3) & (idx == 0)] = 1
    rgb = ikat_render(idx, PAL, 81, weft=3, shift=1.6, blur=1.2, wrap=False)
    m = np.zeros((H, W), np.float32); m[8:H - 8, 14:W - 14] = 1
    xm = np.clip(np.minimum(xx - 14, W - 14 - xx) / 40, 0, 1)
    a = fray(m, 82, 1.6, 0.6) * (0.25 + 0.75 * xm)
    art = rgba(rgb, a)
    preview(art, "tt-divider", bg=CRM)
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
