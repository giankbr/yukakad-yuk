"""Lomba 17-an — kampung Agustusan in opaque folk gouache: panjat pinang pole with its prize ring and a red-white flag,
stylised faceless kids (climbing, balap karung, makan kerupuk, tarik tambang), red-white bunting, a kampung row with a
painted gapura, clouds. Indonesian flag always red on top. Run: python3 -I lomba-17an.py [part ...]
parts: pinang kampung bendera karung kerupuk tambang flag awan"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g4_lib import *

OUT = outdir("lomba-17an")
PARTS = sys.argv[1:] or ["pinang", "kampung", "bendera", "karung", "kerupuk", "tambang", "flag", "awan"]
SKY = "#bfe3ee"
RED, RED_D = "#d7262e", "#a5181f"
WHITE, WHITE_D = "#fbf6ea", "#e6dcc6"
SKINS = [("#c68a5c", "#a86d44"), ("#a8714a", "#8a5634"), ("#d9a27a", "#b9805a")]
HAIR = "#2a1d17"
INK = "#2a1d17"


def paint(art, mask, col, col2=None, seed=1, rough=1.4, streak=0.7):
    return GP(art, mask, col, col2 or col, seed=seed, rough=rough, streak=streak)


def limb(W, H, pts, w):
    return strokes(W, H, [(pts, w, (0.0, 0.0))])


def kid(art, W, H, x, y, s, rng, nx, pose="stand", shirt=(RED, RED_D), shorts=("#2f4a8a", "#233a6e"), skin=None, flip=1, face=True):
    """Stylised child (dot eyes, small smile), feet at (x, y), height s. Returns art, body mask, head."""
    skin = skin or rng.choice(SKINS)
    f = flip
    X = lambda dx: x + dx * s * f
    Y = lambda dy: y - dy * s
    lw = s * 0.062
    hr = s * 0.125
    head = (X(0.0), Y(0.855), hr)
    sh_l, sh_r = (X(-0.09), Y(0.7)), (X(0.09), Y(0.7))
    hip_l, hip_r = (X(-0.055), Y(0.38)), (X(0.055), Y(0.38))
    lean = 0.0
    if pose == "climb":
        arms = [[sh_l, (X(-0.05), Y(0.9)), (X(0.06), Y(1.0))], [sh_r, (X(0.16), Y(0.86)), (X(0.1), Y(0.99))]]
        legs = [[hip_l, (X(-0.17), Y(0.24)), (X(0.04), Y(0.12))], [hip_r, (X(0.2), Y(0.28)), (X(0.1), Y(0.1))]]
    elif pose == "sack":
        arms = [[sh_l, (X(-0.17), Y(0.58)), (X(-0.15), Y(0.47))], [sh_r, (X(0.17), Y(0.58)), (X(0.15), Y(0.47))]]
        legs = []
    elif pose == "bite":
        head = (X(0.02), Y(0.87), hr)
        arms = [[sh_l, (X(-0.13), Y(0.55)), (X(-0.03), Y(0.44))], [sh_r, (X(0.13), Y(0.55)), (X(0.03), Y(0.45))]]
        legs = [[hip_l, (X(-0.08), Y(0.18)), (X(-0.09), Y(0.0))], [hip_r, (X(0.08), Y(0.18)), (X(0.1), Y(0.0))]]
    elif pose == "pull":
        lean = -0.16
        head = (X(-0.2), Y(0.82), hr)
        sh_l, sh_r = (X(-0.22), Y(0.67)), (X(-0.06), Y(0.69))
        hip_l, hip_r = (X(-0.1), Y(0.38)), (X(0.0), Y(0.39))
        arms = [[sh_l, (X(0.02), Y(0.56)), (X(0.2), Y(0.5))], [sh_r, (X(0.1), Y(0.58)), (X(0.26), Y(0.52))]]
        legs = [[hip_l, (X(0.0), Y(0.2)), (X(0.1), Y(0.0))], [hip_r, (X(0.12), Y(0.22)), (X(0.26), Y(0.02))]]
    else:
        arms = [[sh_l, (X(-0.18), Y(0.55)), (X(-0.17), Y(0.42))], [sh_r, (X(0.18), Y(0.55)), (X(0.17), Y(0.42))]]
        legs = [[hip_l, (X(-0.07), Y(0.18)), (X(-0.07), Y(0.0))], [hip_r, (X(0.07), Y(0.18)), (X(0.07), Y(0.0))]]
    neck = strokes(W, H, [([(head[0], head[1] + hr * 0.6), ((sh_l[0] + sh_r[0]) / 2, (sh_l[1] + sh_r[1]) / 2)], lw * 1.1, None)])
    torso = shapes(W, H, [[(sh_l[0] - s * 0.025 * f, sh_l[1] - s * 0.01), (sh_r[0] + s * 0.025 * f, sh_r[1] - s * 0.01),
                           (hip_r[0] + s * 0.03 * f, hip_r[1] + s * 0.02), (hip_l[0] - s * 0.03 * f, hip_l[1] + s * 0.02)]], smooth=False)
    sleeves = strokes(W, H, [([a[0], (a[0][0] + (a[1][0] - a[0][0]) * 0.35, a[0][1] + (a[1][1] - a[0][1]) * 0.35)], lw * 1.5, None) for a in arms])
    shortm = None if pose == "sack" else shapes(W, H, [[(hip_l[0] - s * 0.035 * f, hip_l[1]), (hip_r[0] + s * 0.035 * f, hip_r[1]),
                                                        (hip_r[0] + s * 0.05 * f, hip_r[1] + s * 0.11), (hip_l[0] - s * 0.05 * f, hip_l[1] + s * 0.11)]], smooth=False)
    legm = strokes(W, H, [(curve(l, 10), lw * 1.15, None) for l in legs]) if legs else None
    armm = strokes(W, H, [(curve(a, 10), lw, None) for a in arms])
    headm = circles(W, H, [head])
    hm = shapes(W, H, [[(head[0] + math.cos(a) * hr * 1.07, head[1] + math.sin(a) * hr * 1.07) for a in np.linspace(math.pi * 0.92, math.tau * 1.04, 14)]
                       + [(head[0] + hr * 0.7 * f, head[1] - hr * 0.18), (head[0] - hr * 0.1 * f, head[1] - hr * 0.42), (head[0] - hr * 0.85 * f, head[1] - hr * 0.05)]])
    if legm is not None:
        art = paint(art, legm, *skin, seed=nx())
    art = paint(art, np.maximum(armm, neck), *skin, seed=nx())
    if shortm is not None:
        art = paint(art, shortm, *shorts, seed=nx())
    art = paint(art, np.maximum(torso, sleeves), *shirt, seed=nx())
    art = paint(art, headm, *skin, seed=nx(), rough=0.8)
    art = paint(art, hm * headm, HAIR, "#3b2a20", seed=nx(), rough=0.6)
    if face and pose not in ("climb",):
        ex = hr * 0.36
        eyes = circles(W, H, [(head[0] - ex + hr * 0.12 * f, head[1] + hr * 0.12, hr * 0.085), (head[0] + ex + hr * 0.12 * f, head[1] + hr * 0.12, hr * 0.085)])
        art = OV(art, eyes, lambda q: tint(q, INK, 0.9), pad=4)
        if pose != "bite":
            smile = strokes(W, H, [(arc_pts(head[0] + hr * 0.12 * f, head[1] + hr * 0.3, hr * 0.28, 0.4, math.pi - 0.4, 8), hr * 0.07, None)])
            art = OV(art, smile, lambda q: tint(q, "#6e2f22", 0.85), pad=4)
        art = OV(art, circles(W, H, [(head[0] - hr * 0.5 + hr * 0.12 * f, head[1] + hr * 0.38, hr * 0.14), (head[0] + hr * 0.62 + hr * 0.12 * f, head[1] + hr * 0.38, hr * 0.14)]) * headm, lambda q: tint(q, "#e8907a", 0.35))
    body = np.maximum.reduce([m for m in (legm, armm, shortm, torso, headm) if m is not None])
    return art, body, head


def flag_mask(W, H, x, y, w, h, wave=0.12, phase=0.0):
    """Waving flag rectangle from pole point (x, y); returns (red_top, white_bottom) masks. Red is ALWAYS on top."""
    def edge(t, v):
        return (x + t * w, y + v * h + math.sin(t * math.pi * 1.6 + phase) * h * wave * t)
    top = [edge(t, 0) for t in np.linspace(0, 1, 16)]
    mid = [edge(t, 0.5) for t in np.linspace(0, 1, 16)]
    bot = [edge(t, 1) for t in np.linspace(0, 1, 16)]
    red = shapes(W, H, [top + list(reversed(mid))], smooth=False)
    white = shapes(W, H, [mid + list(reversed(bot))], smooth=False)
    return red, white


def flag(art, W, H, x, y, w, h, nx, wave=0.12, phase=0.0):
    red, white = flag_mask(W, H, x, y, w, h, wave, phase)
    art = paint(art, white, WHITE, WHITE_D, seed=nx(), rough=1.0)
    art = paint(art, red, RED, RED_D, seed=nx(), rough=1.0)
    # soft fold shading
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fold = (0.5 + 0.5 * np.sin((xx - x) / max(1, w) * math.pi * 1.6 + phase)) * np.maximum(red, white)
    art = OV(art, fold * 0.22, lambda q: tint(q, "#3a1a10"))
    return art


if "pinang" in PARTS:
    # pole (greased, banded), prize ring with hanging prizes, flag on top, two climbers
    W, H = 420, 1240
    nx = Seq(1100); rng = random.Random(11)
    art = blank(W, H)
    px = 210
    pole = shapes(W, H, [[(px - 12, 210), (px + 12, 210), (px + 17, H - 8), (px - 17, H - 8)]], smooth=False)
    art = paint(art, pole, "#b9865a", "#8a5c36", seed=nx(), streak=1.2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # oily sheen + mud
    art = OV(art, pole * np.clip(1 - np.abs(xx - px + 5) / 5, 0, 1) * 0.5, lambda q: tint(q, "#f3dcb8"))
    art = OV(art, pole * (yy > 760) * fbm(W, H, 3, 14, 2) * 0.5, lambda q: tint(q, "#5b3b22"))
    # flagpole tip + flag (red top)
    tip = strokes(W, H, [([(px, 214), (px, 40)], 5, (0.0, 0.0))])
    art = paint(art, tip, "#6b4a30", seed=nx())
    art = paint(art, circles(W, H, [(px, 38, 8)]), "#e3b441", "#b8892a", seed=nx())
    art = flag(art, W, H, px + 2, 48, 150, 96, nx, wave=0.14)
    # prize ring (bamboo hoop) with ropes and prizes
    ring = np.clip(shapes(W, H, [ellipse_pts(px, 240, 170, 32, 40)]) - shapes(W, H, [ellipse_pts(px, 240, 160, 24, 40)]), 0, 1)
    ropes = strokes(W, H, [([(px, 200), (px + math.cos(a) * 165, 240 + math.sin(a) * 28)], 2.2, None) for a in np.linspace(0, math.tau, 7, endpoint=False)])
    art = paint(art, ropes, "#8b6a45", seed=nx(), rough=0.6)
    art = paint(art, ring, "#d9b26a", "#b48a46", seed=nx(), rough=0.8)
    prizes = [("ember", px - 140, "#2f7fd0"), ("tas", px - 80, "#f2a93b"), ("roda", px - 15, None), ("kotak", px + 60, "#e8523a"), ("bola", px + 128, "#4fa35a")]
    for kind, x0, col in prizes:
        yt = 262 + (abs(x0 - px) < 40) * 6
        string = strokes(W, H, [([(x0, yt - 18), (x0, yt + 40)], 2.0, None)])
        art = paint(art, string, "#8b6a45", seed=nx(), rough=0.5)
        cy = yt + 70
        if kind == "ember":
            m = shapes(W, H, [[(x0 - 24, cy - 26), (x0 + 24, cy - 26), (x0 + 18, cy + 24), (x0 - 18, cy + 24)]], smooth=False)
            art = paint(art, m, col, "#1f5ea3", seed=nx())
            art = paint(art, strokes(W, H, [(arc_pts(x0, cy - 26, 22, math.pi, math.tau, 12), 2.5, None)]), "#1f3c66", seed=nx())
        elif kind == "tas":
            m = shapes(W, H, [[(x0 - 22, cy - 16), (x0 + 22, cy - 16), (x0 + 26, cy + 26), (x0 - 26, cy + 26)]], smooth=False)
            art = paint(art, m, col, "#d48a1f", seed=nx())
            art = paint(art, strokes(W, H, [(arc_pts(x0, cy - 16, 12, math.pi, math.tau, 10), 3.5, None)]), "#a8661a", seed=nx())
        elif kind == "roda":
            rim = np.clip(circles(W, H, [(x0, cy + 6, 44)]) - circles(W, H, [(x0, cy + 6, 36)]), 0, 1)
            spokes = strokes(W, H, [([(x0, cy + 6), (x0 + math.cos(a) * 38, cy + 6 + math.sin(a) * 38)], 1.4, None) for a in np.linspace(0, math.tau, 12, endpoint=False)])
            art = paint(art, spokes, "#8f9aa3", seed=nx(), rough=0.4)
            art = paint(art, rim, "#2b2b2b", "#444444", seed=nx(), rough=0.6)
            art = paint(art, circles(W, H, [(x0, cy + 6, 6)]), "#c9d1d6", seed=nx(), rough=0.4)
        elif kind == "kotak":
            m = shapes(W, H, [[(x0 - 24, cy - 22), (x0 + 24, cy - 22), (x0 + 24, cy + 22), (x0 - 24, cy + 22)]], smooth=False)
            art = paint(art, m, col, "#c33a25", seed=nx())
            rib = strokes(W, H, [([(x0, cy - 22), (x0, cy + 22)], 6, None), ([(x0 - 24, cy), (x0 + 24, cy)], 6, None)])
            art = paint(art, rib, "#f6d35b", seed=nx(), rough=0.5)
        else:
            m = circles(W, H, [(x0, cy, 24)])
            art = paint(art, m, col, "#3a7f44", seed=nx())
            art = paint(art, strokes(W, H, [(arc_pts(x0, cy, 24, -0.6, 0.9, 10), 4, None)]) * m, WHITE, seed=nx(), rough=0.4)
    clear()
    # climbers: bottom kid supports, top kid reaches
    art, _, _ = kid(art, W, H, px - 18, 640, 220, rng, nx, pose="climb", shirt=(WHITE, WHITE_D), shorts=(RED, RED_D))
    art, _, _ = kid(art, W, H, px - 14, 860, 230, rng, nx, pose="climb", shirt=(RED, RED_D), shorts=("#2f4a8a", "#233a6e"), flip=-1)
    clear()
    preview(art, "lb-pinang", tone=SKY)
    save(art, f"{OUT}/pinang.webp", max_w=260, quality=82)

if "kampung" in PARTS:
    W, H = 1000, 380
    nx = Seq(2100); rng = random.Random(21)
    art = blank(W, H)
    # back trees
    trees = shapes(W, H, [deform(ellipse_pts(x, 190 + rng.uniform(-10, 10), rng.uniform(50, 80), rng.uniform(40, 60), 14), rng, 2, 0.06) for x in range(40, W, 110)])
    art = paint(art, trees, "#5f9b4a", "#3f7a35", seed=nx(), rough=2.5)
    # houses: walls + roofs (genteng terracotta), small windows
    xs = [20, 190, 380, 600, 790]
    cols = ["#f1e3c2", "#e9c98f", "#d8e6dc", "#f3d7c4", "#e6dcb8"]
    for i, x in enumerate(xs):
        w = rng.uniform(150, 185); top = 230 + rng.uniform(-8, 8)
        wall = shapes(W, H, [[(x, top), (x + w, top), (x + w, H), (x, H)]], smooth=False)
        roof = shapes(W, H, [[(x - 16, top + 4), (x + w * 0.5, top - 74), (x + w + 16, top + 4)]], smooth=False)
        art = paint(art, wall, cols[i], seed=nx())
        art = paint(art, roof, "#c2562f", "#9c3f22", seed=nx())
        # roof tile lines
        tl = strokes(W, H, [([(x - 20, top - 6 - k * 13), (x + w + 20, top - 6 - k * 13)], 1.6, None) for k in range(6)]) * roof
        art = OV(art, tl * 0.35, lambda q: tint(q, "#6e2a15"))
        door = shapes(W, H, [[(x + w * 0.42, top + 60), (x + w * 0.58, top + 60), (x + w * 0.58, H), (x + w * 0.42, H)]], smooth=False)
        art = paint(art, door, "#6e4a2c", seed=nx())
        for wx in (x + w * 0.14, x + w * 0.7):
            win = shapes(W, H, [[(wx, top + 50), (wx + w * 0.16, top + 50), (wx + w * 0.16, top + 92), (wx, top + 92)]], smooth=False)
            art = paint(art, win, "#3b5a6e", seed=nx(), rough=0.8)
        # small flag per house (red on top)
        fx = x + w * 0.85
        art = paint(art, strokes(W, H, [([(fx, top + 10), (fx, top - 70)], 3, None)]), "#7a5a3a", seed=nx())
        art = flag(art, W, H, fx + 1, top - 68, 46, 30, nx, wave=0.12, phase=i)
        clear()
    # gapura (village gate) painted red-white, centre
    gx = 520
    for sx in (-1, 1):
        post = shapes(W, H, [[(gx + sx * 70 - 16, 170), (gx + sx * 70 + 16, 170), (gx + sx * 70 + 18, H), (gx + sx * 70 - 18, H)]], smooth=False)
        art = paint(art, post, WHITE, WHITE_D, seed=nx())
        bands = post * (((np.mgrid[0:H, 0:W][0] // 26) % 2) == 0)
        art = paint(art, bands, RED, RED_D, seed=nx())
    beam = shapes(W, H, [[(gx - 104, 150), (gx + 104, 150), (gx + 96, 182), (gx - 96, 182)]], smooth=False)
    art = paint(art, beam, RED, RED_D, seed=nx())
    art = paint(art, shapes(W, H, [[(gx - 96, 170), (gx + 96, 170), (gx + 96, 182), (gx - 96, 182)]], smooth=False), WHITE, WHITE_D, seed=nx())
    # grass foreground
    grass = shapes(W, H, [[(0, 336)] + [(x, 330 + 10 * math.sin(x / 70)) for x in range(0, W + 1, 40)] + [(W, H), (0, H)]])
    art = paint(art, grass, "#7cbc5a", "#5c9e43", seed=nx())
    blades = strokes(W, H, [([(x, 342), (x + rng.uniform(-6, 6), 324 + rng.uniform(-6, 4))], 2, (0.0, 0.6)) for x in range(6, W, 9)])
    art = paint(art, blades * 0.9, "#4f8f3a", seed=nx(), rough=0.4)
    preview(art, "lb-kampung", tone=SKY)
    save(art, f"{OUT}/kampung.webp", max_w=680, quality=80)

if "bendera" in PARTS:
    W, H = 1000, 190
    nx = Seq(3100); rng = random.Random(31)
    art = blank(W, H)
    pts = [(x, 26 + 60 * max(0.0, math.sin(x / W * math.pi)) ** 1.2) for x in np.linspace(-10, W + 10, 60)]
    art = paint(art, strokes(W, H, [(pts, 3, None)]), "#6b4a30", seed=nx(), rough=0.4)
    tri_r, tri_w = [], []
    n = 17
    for k in range(n):
        t0 = (k + 0.1) / n; t1 = (k + 0.9) / n
        i0 = int(t0 * 59); i1 = int(t1 * 59)
        a, b = pts[i0], pts[i1]
        mx = (a[0] + b[0]) / 2; my = (a[1] + b[1]) / 2
        tip = (mx + rng.uniform(-3, 3), my + 62 + rng.uniform(-4, 4))
        (tri_r if k % 2 == 0 else tri_w).append([a, b, tip])
    art = paint(art, shapes(W, H, tri_w, smooth=False), WHITE, WHITE_D, seed=nx())
    art = paint(art, shapes(W, H, tri_r, smooth=False), RED, RED_D, seed=nx())
    preview(art, "lb-bendera", tone=SKY)
    save_full(art, f"{OUT}/bendera.webp", size=(640, 122), quality=82)

if "karung" in PARTS:
    W, H = 340, 420
    nx = Seq(4100); rng = random.Random(41)
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(170, 404, 80, 9, 20)])
    art = over(art, tint(gaussian_filter(shadow, 4) * 0.35, "#2a1d17"))
    art, body, head = kid(art, W, H, 170, 360, 330, rng, nx, pose="sack", shirt=(WHITE, WHITE_D))
    sack = shapes(W, H, [[(110, 212), (230, 212), (246, 300), (238, 384), (102, 384), (94, 300)]])
    art = paint(art, sack, "#c9a46b", "#a98450", seed=nx(), streak=1.2)
    weave = sack * hatch(W, H, 0.0, 5, 0.25, 3) * 0.25 + sack * hatch(W, H, math.pi / 2, 5, 0.25, 4) * 0.25
    art = OV(art, weave, lambda q: tint(q, "#7a5a32"))
    art = paint(art, strokes(W, H, [(curve([(108, 214), (170, 206), (232, 214)], 12), 7, None)]), "#a88450", seed=nx())
    # hands gripping the rim (paint on top)
    sk = SKINS[0]
    art = paint(art, circles(W, H, [(114, 220, 11), (226, 220, 11)]), *sk, seed=nx())
    # motion dashes
    art = paint(art, strokes(W, H, [([(40, 300), (76, 300)], 4, (0.3, 0.3)), ([(30, 330), (70, 330)], 4, (0.3, 0.3)), ([(48, 360), (80, 360)], 4, (0.3, 0.3))]), "#ffffff", seed=nx(), rough=0.4)
    preview(art, "lb-karung", tone=SKY)
    save(art, f"{OUT}/karung.webp", max_w=220, quality=84)

if "kerupuk" in PARTS:
    W, H = 380, 460
    nx = Seq(5100); rng = random.Random(51)
    art = blank(W, H)
    rope = [(x, 40 + 10 * math.sin(x / W * math.pi)) for x in np.linspace(0, W, 30)]
    art = paint(art, strokes(W, H, [(rope, 3, None)]), "#6b4a30", seed=nx(), rough=0.4)
    for k, (kx, ln) in enumerate([(80, 70), (200, 92), (316, 66)]):
        art = paint(art, strokes(W, H, [([(kx, 46), (kx, 46 + ln)], 1.8, None)]), "#8b6a45", seed=nx(), rough=0.3)
        cy = 46 + ln + 34
        km = shapes(W, H, [deform(ellipse_pts(kx, cy, 38, 36, 22), rng, 2, 0.05)])
        art = paint(art, km, "#f6e2a8", "#e9c97a", seed=nx(), rough=2.2)
        # kerupuk bubbles + a pink rim
        art = OV(art, km * (fbm(W, H, 7 + k, 6, 2) > 0.62) * 0.5, lambda q: tint(q, "#d8b05e"))
        art = OV(art, np.clip(km - shapes(W, H, [ellipse_pts(kx, cy, 32, 30, 22)]), 0, 1) * 0.7, lambda q: tint(q, "#e98a8a"))
        if k == 1:
            bite = circles(W, H, [(kx + 14, cy + 30, 13), (kx - 2, cy + 34, 11)])
            art[..., 3] *= 1 - bite
    art, body, head = kid(art, W, H, 196, 448, 300, rng, nx, pose="bite", shirt=(RED, RED_D), shorts=(WHITE, WHITE_D))
    preview(art, "lb-kerupuk", tone=SKY)
    save(art, f"{OUT}/kerupuk.webp", max_w=230, quality=84)

if "tambang" in PARTS:
    W, H = 760, 110
    nx = Seq(6100); rng = random.Random(61)
    art = blank(W, H)
    rope = [(x, 56 + 3 * math.sin(x / 40)) for x in np.linspace(10, W - 10, 60)]
    rm = strokes(W, H, [(rope, 12, (0.03, 0.03))])
    art = paint(art, rm, "#caa36a", "#a8834c", seed=nx(), streak=1.0)
    twist = rm * hatch(W, H, 1.0, 9, 0.22, 3)
    art = OV(art, twist * 0.45, lambda q: tint(q, "#7a5a32"))
    # red-white marker ribbon at the centre
    cx = W / 2
    rib_r = shapes(W, H, [[(cx - 8, 46), (cx + 8, 46), (cx + 14, 88), (cx + 2, 80), (cx - 10, 90)]])
    art = paint(art, rib_r, RED, RED_D, seed=nx())
    art = paint(art, shapes(W, H, [[(cx - 8, 46), (cx + 8, 46), (cx + 8, 58), (cx - 8, 58)]], smooth=False), RED, RED_D, seed=nx())
    art = paint(art, shapes(W, H, [[(cx - 8, 58), (cx + 8, 58), (cx + 8, 66), (cx - 8, 66)]], smooth=False), WHITE, WHITE_D, seed=nx())
    preview(art, "lb-tambang", tone=SKY)
    save(art, f"{OUT}/tambang.webp", max_w=360, quality=84)

if "flag" in PARTS:
    W, H = 200, 160
    nx = Seq(7100)
    art = blank(W, H)
    art = paint(art, strokes(W, H, [([(24, 152), (24, 14)], 5, None)]), "#7a5a3a", seed=nx())
    art = paint(art, circles(W, H, [(24, 12, 6)]), "#e3b441", seed=nx())
    art = flag(art, W, H, 26, 20, 150, 96, nx, wave=0.16)
    preview(art, "lb-flag", tone=SKY)
    save(art, f"{OUT}/flag.webp", max_w=90, quality=86)

if "awan" in PARTS:
    W, H = 420, 170
    nx = Seq(8100); rng = random.Random(81)
    art = blank(W, H)
    m = circles(W, H, [(110, 110, 50), (180, 80, 64), (260, 92, 56), (320, 118, 40), (70, 128, 34)])
    m = np.maximum(m, shapes(W, H, [[(40, 150), (370, 150), (360, 120), (50, 120)]], smooth=False))
    art = paint(art, m, "#ffffff", "#eef6f8", seed=nx(), rough=2)
    art = OV(art, m * np.clip((np.mgrid[0:H, 0:W][0] - 110) / 40, 0, 1) * 0.3, lambda q: tint(q, "#a9cbd8"))
    preview(art, "lb-awan", tone=SKY)
    save(art, f"{OUT}/awan.webp", max_w=200, quality=84)
