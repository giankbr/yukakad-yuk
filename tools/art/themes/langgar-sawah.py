"""Langgar Sawah — a small wooden langgar on stilts at the edge of green rice paddies on a warm afternoon, in watercolour:
gold-to-pale sky, a blue volcano and tree line, terraced paddies with pematang paths and flooded plots mirroring the sky,
coconut palms, a fish pond under the langgar with a bamboo plank bridge, woven bamboo (gedek) walls, ijuk-thatched gable
roof, a bedug on the porch. No figures, no calligraphy.
Run: python3 -I langgar-sawah.py [part ...]   parts: sawah gedek padi bedug kelapa"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f3_lib import *

OUT = outdir("langgar-sawah")
PARTS = sys.argv[1:] or ["sawah", "gedek", "padi", "bedug", "kelapa"]
WOOD, WOOD_D, WOOD_L = "#8a5a34", "#4e301a", "#b07a48"
IJUK, IJUK_L = "#3a2e28", "#6a5446"
GREEN, GREEN_D, GREEN_L = "#7fae46", "#4a7a2e", "#c4d870"


def palm_paint(art, W, H, x, by, h, rng, nx, lean=0.1, far=0.0):
    return paint_palm(art, W, H, x, by, h, rng, nx, lean, far)


def langgar(art, W, H, cx, base, s, rng, nx):
    """Wooden langgar on stilts: gedek walls, ijuk gable roof, porch with bedug, plank bridge. base = ground/water line."""
    fw, fh = 1.0 * s, 0.42 * s  # front (gable) face width, wall height
    sw = 0.55 * s               # side face (receding to the right)
    floor = base - 0.36 * s
    # stilts
    st = []
    for px in np.linspace(cx - fw / 2 + 6, cx + fw / 2 - 6, 4):
        st.append(([(px, floor), (px, base + 6)], s * 0.035, None))
    for px in np.linspace(cx + fw / 2 + sw * 0.3, cx + fw / 2 + sw - 6, 2):
        st.append(([(px, floor - s * 0.06), (px, base + 2)], s * 0.03, None))
    sm = strokes(W, H, st, cap=False)
    art = GP(art, sm, WOOD_D, "#2e1c10", seed=nx(), rough=0.4)
    # side wall (receding, in shade)
    side = shapes(W, H, [[(cx + fw / 2, floor), (cx + fw / 2 + sw, floor - s * 0.08), (cx + fw / 2 + sw, floor - s * 0.08 - fh * 0.92), (cx + fw / 2, floor - fh)]], smooth=False)
    gtex = gedek(W, H, nx(), cell=max(4, int(s * 0.035)), light="#c9a368", dark="#94733e")
    gtex[..., 3] = side
    gtex[..., :3] *= 0.72
    art = over(art, gtex)
    # front wall (sunlit)
    front = rect(W, H, cx - fw / 2, floor - fh, cx + fw / 2, floor)
    gtex = gedek(W, H, nx(), cell=max(4, int(s * 0.035)), light="#e2c486", dark="#b08a50")
    gtex[..., 3] = front
    art = over(art, gtex)
    # door + windows (dark openings with wooden frames)
    door = rect(W, H, cx - s * 0.08, floor - fh * 0.82, cx + s * 0.08, floor)
    wins = np.maximum(rect(W, H, cx - fw / 2 + s * 0.08, floor - fh * 0.75, cx - fw / 2 + s * 0.22, floor - fh * 0.42), rect(W, H, cx + fw / 2 - s * 0.22, floor - fh * 0.75, cx + fw / 2 - s * 0.08, floor - fh * 0.42))
    art = GP(art, np.maximum(door, wins), "#2a1a12", "#3a2418", seed=nx(), rough=0.3)
    art = over(art, flat(outline(np.maximum(door, wins), 2.5), WOOD, 0.95))
    art = over(art, flat(wins * hatch(W, H, 1.5708, s * 0.035, 0.3, nx(), 0.2), WOOD_L, 0.9))
    # floor beam + porch
    beam = rect(W, H, cx - fw / 2 - 4, floor, cx + fw / 2 + 4, floor + s * 0.04)
    art = over(art, wood(beam, WOOD, WOOD_D, seed=nx(), angle=0.0, grain=3))
    # roof: front gable triangle + side slope in ijuk thatch
    apex = (cx, floor - fh - s * 0.48)
    eave = s * 0.1
    gable = shapes(W, H, [[(cx - fw / 2 - eave, floor - fh + 4), apex, (cx + fw / 2 + eave, floor - fh + 4)]], smooth=False)
    slope = shapes(W, H, [[apex, (apex[0] + sw + 6, apex[1] - s * 0.08), (cx + fw / 2 + sw + eave, floor - fh - s * 0.02), (cx + fw / 2 + eave, floor - fh + 4)]], smooth=False)
    # gable face: a wooden board triangle inside the thatch rim
    rim = np.clip(gable - shapes(W, H, [[(cx - fw / 2 + 4, floor - fh), (cx, apex[1] + s * 0.1), (cx + fw / 2 - 4, floor - fh)]], smooth=False), 0, 1)
    board = np.clip(gable - rim, 0, 1)
    art = over(art, wood(board, WOOD_L, WOOD, seed=nx(), angle=1.5708, grain=s * 0.03))
    vent = board * (np.abs(np.arange(W)[None, :] - cx) < s * 0.07) * (np.arange(H)[:, None] > apex[1] + s * 0.18) * (np.arange(H)[:, None] < apex[1] + s * 0.33)
    art = over(art, flat(vent * hatch(W, H, 1.5708, 4, 0.4, nx(), 0.2), "#2a1a12", 0.8))
    thatch = np.clip(rim + slope, 0, 1)
    art = GP(art, thatch, IJUK, "#2a201c", seed=nx(), rough=0.8, streak=1.2)
    fib = thatch * hatch(W, H, 1.2, 3.0, 0.25, nx(), 2.5)
    art = over(art, flat(fib, IJUK_L, 0.5))
    art = over(art, flat(slope * light_mask(H, W, apex[0], apex[1], s * 0.7), "#c89a62", 0.25))
    # ragged thatch eave fringe
    fr = []
    for x_ in np.arange(cx + fw / 2 + eave, cx + fw / 2 + sw + eave, 3):
        t = (x_ - cx - fw / 2 - eave) / (sw)
        y_ = floor - fh + 4 - t * s * 0.06
        fr.append(([(x_, y_ - 2), (x_ + rng.uniform(-1, 1), y_ + rng.uniform(4, 9))], 1.4, None))
    art = over(art, flat(strokes(W, H, fr), IJUK, 0.9))
    # mustaka (small finial) on the apex
    art = GP(art, shapes(W, H, [[(apex[0] - 4, apex[1] + 2), (apex[0], apex[1] - s * 0.1), (apex[0] + 4, apex[1] + 2)]], smooth=False), "#b88a3a", "#7a5a22", seed=nx(), rough=0.3)
    return art


if "sawah" in PARTS:
    W, H = 780, 1150
    nx = Seq(8100); rng = random.Random(81)
    HZ = 690
    art = painted_sky(W, H, [(0, "#b9d3df"), (0.22, "#e3e6d6"), (0.45, "#f6e2b2"), (0.6, "#f4cf8e"), (1, "#f4cf8e")], seed=nx())
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # sun glow low-left
    art = over(art, flat(light_mask(H, W, 150, 560, 380), "#fff3cc", 0.6))
    art = over(art, flat(circles(W, H, [(150, 560, 34)]), "#fff8e2", 0.85))
    clouds = np.clip(cloud_mask(W, H, 560, 420, 300, 70, rng) + cloud_mask(W, H, 250, 330, 220, 46, rng) + cloud_mask(W, H, 640, 250, 180, 40, rng), 0, 1)
    art = G(art, clouds, "#fff6e6", "#f3dcc0", seed=nx(), density=0.55, edge=0.15, bloom=0.5, rough=8)
    art = G(art, clouds * np.clip((yy - 380) / 80, 0, 1) * 0.8, "#d9a98a", seed=nx(), density=0.3, edge=0.1, bloom=0.3, rough=6)
    clear()
    # volcano + far hills
    vol = shapes(W, H, [[(-20, HZ), (210, 600), (360, 498), (410, 494), (470, 520), (640, 610), (800, 650), (800, HZ + 10), (-20, HZ + 10)]])
    art = G(art, vol, "#9db0c2", "#8597ad", seed=nx(), density=0.85, edge=0.4, bloom=0.4, rough=5)
    art = G(art, vol * light_mask(H, W, 260, 520, 260), "#f3d6a8", seed=nx(), density=0.3, edge=0, bloom=0.3, rough=4)
    hl = hills(W, H, 668, 16, nx(), 0.4)
    art = G(art, hl, "#7f9a82", "#6a8670", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=4)
    clear()
    # tree line + far palms
    trees = shapes(W, H, [deform(ellipse_pts(x_, 690 + rng.uniform(-4, 4), rng.uniform(26, 48), rng.uniform(14, 26), 12), rng, 2, 0.15) for x_ in range(-10, 800, 34)])
    art = G(art, np.clip(trees + rect(W, H, 0, 690, W, 706), 0, 1), "#5d7d4a", "#46663a", seed=nx(), density=0.9, edge=0.4, bloom=0.3, rough=3)
    for px, ph_ in ((70, 120), (110, 96), (590, 110), (700, 130), (740, 100)):
        art = palm_paint(art, W, H, px, 700, ph_, rng, nx, lean=rng.uniform(-0.1, 0.12), far=0.55)
    clear()
    # paddies: horizontal bands in perspective, alternating flooded (sky reflection) and green rows
    bands = []
    y = 704
    k = 0
    while y < H + 20:
        hgt = 10 + (y - 704) * 0.17
        bands.append((y, y + hgt, k)); y += hgt; k += 1
    for (y0, y1, k) in bands:
        wob = lambda x_, ph: math.sin(x_ / 140 + ph) * (y1 - y0) * 0.12
        ph = rng.uniform(0, 6)
        pts = [(x_, y0 + wob(x_, ph)) for x_ in range(-20, W + 21, 20)] + [(x_, y1 + wob(x_, ph + 0.5)) for x_ in range(W + 20, -21, -20)]
        m = shapes(W, H, [pts], smooth=False)
        if k % 3 == 1:  # flooded, freshly planted plot: mirrors the warm sky
            art = G(art, m, "#f1dcae", "#e7c98c", seed=nx(), density=0.9, edge=0.3, bloom=0.4, rough=2)
            rows = m * hatch(W, H, 0.0 + (rng.random() - 0.5) * 0.05, max(3, (y1 - y0) / 4), 0.22, nx(), 0.6)
            art = G(art, rows * np.clip((xx * 0 + 1) * (hatch(W, H, 1.5708, max(3, (y1 - y0) * 0.4), 0.3, nx(), 0.8)), 0, 1), "#8fb050", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.6, feather=0.5)
        else:
            c1, c2 = (GREEN, GREEN_D) if k % 3 == 0 else (GREEN_L, GREEN)
            art = G(art, m, c1, c2, seed=nx(), density=0.92, edge=0.4, bloom=0.3, rough=2, gran=0.25)
            tuft = m * np.clip((fbm(W, H, nx(), max(3, (y1 - y0) / 6), 2) - 0.55) * 3, 0, 1)
            art = G(art, tuft, GREEN_D, "#3a6226", seed=nx(), density=0.5, edge=0.2, bloom=0.1, rough=1, feather=0.6)
        # pematang (bund) along the band's top edge
        bund = strokes(W, H, [([(x_, y0 + wob(x_, ph)) for x_ in range(-20, W + 21, 10)], max(1.6, (y1 - y0) * 0.12), None)])
        art = G(art, bund, "#9a8858", "#7a6a40", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=1, feather=0.6)
        if k % 2 == 0:
            clear()
    divs = []
    for k in range(-7, 9):
        x_end = 390 + k * 150 + rng.uniform(-30, 30)
        divs.append(([(390 + k * 6, 706), (x_end, H + 10)], 1.0, None))
    dm = strokes(W, H, divs, cap=False)
    dm = np.clip(dm * (1.0 + (yy - 706) / 300), 0, 1) * (yy > 706)
    art = G(art, gaussian_filter(dm, 0.6), "#8a7a4a", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=1, feather=0.6)
    # a diagonal pematang path leading from front-left toward the langgar
    path = strokes(W, H, [(curve([(80, H + 10), (200, 1000), (300, 900), (350, 852)], 40), 34, (0.0, 0.8))])
    art = GP(art, path, "#c4ab74", "#a08a58", seed=nx(), rough=2.0, streak=0.8)
    art = G(art, np.clip(outline(path, 3), 0, 1), "#6f9e3a", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=0.8)
    art = G(art, path * light_mask(H, W, 200, 1000, 300), "#f2d9a0", seed=nx(), density=0.3, edge=0, bloom=0.2, rough=2)
    clear()
    # fish pond under the langgar
    pond = shapes(W, H, [deform(ellipse_pts(540, 812, 200, 38, 18), rng, 2, 0.06)])
    art = G(art, pond, "#e9d4a2", "#a9bfb6", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=2)
    art = langgar(art, W, H, 500, 812, 220, rng, nx)
    # reflection: flip the langgar region into the pond, darkened, rippled
    ref = art[612:812][::-1].copy()
    rh = min(ref.shape[0], H - 812)
    rip = (np.sin(np.arange(rh)[:, None] * 0.9) * 2).astype(np.int32)
    sub = ref[:rh]
    shifted = np.stack([np.roll(sub[i], int(rip[i, 0]), 0) for i in range(rh)])
    pm = pond[812:812 + rh][..., None]
    blend = shifted[..., :3] * 0.7 + np.array(hex_rgb("#6a7a70"), np.float32) * 0.3
    art[812:812 + rh, :, :3] = art[812:812 + rh, :, :3] * (1 - pm * 0.55) + blend * pm * 0.55
    # bamboo plank bridge from the path to the porch
    bridge = strokes(W, H, [([(392, 826), (346, 852)], 7, None)])
    art = GP(art, bridge, "#c9a46a", "#8a6a3a", seed=nx(), rough=0.4)
    clear()
    # near palms framing the right
    art = palm_paint(art, W, H, 800, 1040, 600, rng, nx, lean=-0.05)
    art = palm_paint(art, W, H, 300, 880, 390, rng, nx, lean=-0.08)
    clear()
    # near rice stalks in the foreground corners
    st = []
    for k in range(70):
        x_ = rng.uniform(-10, 230) if k < 40 else rng.uniform(560, 790)
        y_ = H + 5
        hh = rng.uniform(60, 140)
        bend = rng.uniform(-0.4, 0.4)
        st.append((curve([(x_, y_), (x_ + bend * hh * 0.3, y_ - hh * 0.6), (x_ + bend * hh, y_ - hh)], 12), rng.uniform(2.0, 3.6), (0.0, 0.8)))
    sm = strokes(W, H, st)
    art = G(art, sm, "#6f9e3a", "#3e6a24", seed=nx(), density=0.95, edge=0.4, bloom=0.2, rough=0.8, feather=0.6)
    art = G(art, sm * light_mask(H, W, 0, 1000, 300), "#e8d070", seed=nx(), density=0.35, edge=0, bloom=0.1, rough=1)
    # warm afternoon glaze from the left
    art = over(art, flat(light_mask(H, W, 120, 620, 700), "#ffd98a", 0.18))
    art = add_grain(art, nx(), 0.025)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/sawah.png")
    save_rgb(art, f"{OUT}/sawah.webp", quality=76)

if "gedek" in PARTS:
    t = gedek(288, 288, seed=5, cell=18)
    t[..., :3] *= (0.94 + 0.08 * wrap_noise(288, 288, 6, 30))[..., None]
    Image.fromarray((np.clip(t[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/gedek.png")
    save_rgb(t, f"{OUT}/gedek.webp", quality=74)

if "padi" in PARTS:
    W, H = 560, 140
    nx = Seq(8300); rng = random.Random(83)
    art = blank(W, H)
    stalks, grains = [], []
    for sg in (-1, 1):
        for k in range(5):
            x0 = W / 2 + sg * rng.uniform(4, 14)
            L = rng.uniform(170, 240)
            pts = curve([(x0, H - 14), (x0 + sg * L * 0.5, H - 60 - k * 6), (x0 + sg * L, H - 40 + k * 8)], 30)
            stalks.append((pts, 2.2, (0.0, 0.6)))
            for j in range(14, 30):
                px, py = pts[j]
                for side in (-1, 1):
                    grains.append(petal_pts(px, py, 9, 3.2, math.pi / 2 + side * 0.6 + sg * 0.3, n=10))
    leaves = []
    for sg in (-1, 1):
        for k in range(3):
            x0 = W / 2
            L = rng.uniform(120, 200)
            leaves.append((curve([(x0, H - 12), (x0 + sg * L * 0.4, H - 50 - k * 10), (x0 + sg * L, H - 70 - k * 20)], 20), 4.5, (0.0, 0.85)))
    art = G(art, strokes(W, H, leaves), "#8fb050", "#4f7a2e", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=1, feather=0.6)
    art = G(art, strokes(W, H, stalks), "#a49a4a", "#6a6a2a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6, feather=0.5)
    gm = shapes(W, H, grains)
    art = G(art, gm, "#e2b84a", "#b88a2a", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=0.6, feather=0.5)
    art = G(art, gm * light_mask(H, W, W / 2, 0, 300), "#fff0b0", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.5)
    knot = circles(W, H, [(W / 2, H - 14, 7)])
    art = GP(art, knot, "#c0643a", "#8a3e22", seed=nx(), rough=0.4)
    prev(art, "padi", tone="#f6eedb")
    save(art, f"{OUT}/padi.webp", max_w=340, quality=84)

if "bedug" in PARTS:
    W, H = 360, 300
    nx = Seq(8500); rng = random.Random(85)
    art = blank(W, H)
    # stand: two posts and a cross beam, drum hung horizontally by rope
    posts = np.maximum.reduce([rect(W, H, 40, 60, 54, 280), rect(W, H, 306, 60, 320, 280), rect(W, H, 26, 50, 334, 66)])
    art = over(art, soft_shadow(posts, "#2a1a10", blur=5, strength=0.3, dx=4, dy=5))
    art = over(art, wood(posts, WOOD, WOOD_D, seed=nx(), angle=1.5708, grain=5))
    art = over(art, flat(rect(W, H, 26, 50, 334, 54), WOOD_L, 0.6))
    ropes = strokes(W, H, [([(110, 66), (118, 118)], 2.2, None), ([(250, 66), (242, 118)], 2.2, None)])
    art = over(art, flat(ropes, "#c8b07a", 0.95))
    body = shapes(W, H, [[(80, 128), (280, 128), (296, 176), (280, 226), (80, 226), (64, 176)]])
    art = GP(art, body, "#9a4428", "#5e2614", seed=nx(), rough=0.4, streak=1.0)
    staves = body * hatch(W, H, 0.0, 9, 0.12, nx(), 0.8)
    art = over(art, flat(staves, "#3e1a0c", 0.35))
    art = over(art, flat(body * light_mask(H, W, 150, 130, 140), "#ffd9a0", 0.3))
    # drum head (cowhide-coloured) on the left end with pegs
    head = shapes(W, H, [ellipse_pts(78, 177, 20, 50, 20)])
    art = GP(art, head, "#e6d2a2", "#c8ae7a", seed=nx(), rough=0.3)
    pegs = circles(W, H, [(78 + math.cos(a) * 22, 177 + math.sin(a) * 54, 2.5) for a in np.linspace(0, math.tau, 18, endpoint=False)])
    art = over(art, flat(pegs, "#3a2412", 0.9))
    bands = np.maximum(rect(W, H, 120, 128, 126, 226), rect(W, H, 234, 128, 240, 226))
    art = over(art, flat(bands * body, "#d4a84a", 0.8))
    # kentongan: slit bamboo log hanging on the right post
    ken = shapes(W, H, [[(330, 96), (346, 96), (348, 214), (328, 214)]], smooth=False)
    art = GP(art, ken, "#c9a45a", "#8a6a2a", seed=nx(), rough=0.3, streak=1.2)
    art = over(art, flat(rect(W, H, 336, 120, 340, 196), "#3a2412", 0.85))
    art = over(art, flat(strokes(W, H, [([(338, 66), (338, 96)], 1.8, None)]), "#c8b07a", 0.9))
    # mallet leaning on the post
    art = GP(art, strokes(W, H, [([(20, 280), (58, 200)], 5, None)]), WOOD_L, WOOD, seed=nx(), rough=0.3)
    art = GP(art, circles(W, H, [(60, 196, 9)]), "#e6d2a2", "#b89a6a", seed=nx(), rough=0.3)
    art = G(art, shapes(W, H, [ellipse_pts(180, 284, 170, 10, 14)]), "#6a5444", seed=nx(), density=0.35, edge=0.1, bloom=0.1, rough=2)
    prev(art, "bedug", tone="#f6eedb")
    save(art, f"{OUT}/bedug.webp", max_w=240, quality=84)

if "kelapa" in PARTS:
    W, H = 360, 820
    nx = Seq(8700); rng = random.Random(87)
    art = blank(W, H)
    art = palm_paint(art, W, H, 210, 810, 640, rng, nx, lean=-0.12)
    prev(art, "kelapa", tone="#f6eedb")
    save(art, f"{OUT}/kelapa.webp", max_w=200, quality=82)
