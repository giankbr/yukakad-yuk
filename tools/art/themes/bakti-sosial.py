"""Bakti Sosial — warm community-service gouache: two hands forming a heart around a red heart with a white cross, a
health-post tent with a striped scalloped canopy, volunteers in orange vests (stylised, faceless, one in a hijab), sembako
boxes, a blood-drop sign, a single sembako box, a blood drop, a volunteer figure, bunting and a kraft-paper tile.
Original, no logos, no text in the art.  Run: python3 -I bakti-sosial.py [part ...]
parts: hands scene box drop person bunting paper   Assets -> public/themes/art/bakti-sosial/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l6_lib import *

OUT = outdir("bakti-sosial")
PARTS = sys.argv[1:] or ["hands", "scene", "box", "drop", "person", "bunting", "paper"]
RED, RED_D, ORANGE, ORANGE_D, YEL, GREEN, GREEN_D = "#d94b3d", "#b8382c", "#f08a3c", "#d9702a", "#f6c445", "#5b8c3a", "#47702c"
INK, CREAM, KRAFT, KRAFT_D, WHITE = "#4a2219", "#fff4e4", "#c99a5e", "#a97c45", "#fffaf2"
SKINS = ["#8d5a3b", "#c98a5e", "#e3ac80", "#a86d47"]
TEAL = "#3e8f8a"


def paint(art, mask, c1, c2=None, seed=1, rough=1.8, streak=1.0):
    return GP(art, mask, c1, c2 or c1, seed=seed, rough=rough, streak=streak, pad=10)


def heart_pts(cx, cy, s, n=80):
    pts = []
    for i in range(n):
        t = i / n * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s, cy + y * s))
    return pts


def cross(W, H, cx, cy, r, t):
    return shapes(W, H, [rr(cx - r, cy - t, cx + r, cy + t), rr(cx - t, cy - r, cx + t, cy + r)], smooth=False)


def person(art, W, H, x, by, h, nx, skin, vest=ORANGE, shirt="#8fc3d6", pants="#3d4a5c", hijab=None, wave=0, carry=False, rng=None):
    """Stylised faceless volunteer, h = full height; returns art."""
    s = h / 100.0
    X = lambda dx: x + dx * s
    Y = lambda dy: by - dy * s
    legs = shapes(W, H, [rr(X(-9), Y(36), X(-2), Y(0)), rr(X(2), Y(36), X(9), Y(0))], smooth=False)
    art = paint(art, legs, pants, mix(pants, "#000000", 0.15), seed=nx(), rough=1.0)
    shoes = ellipses(W, H, [(X(-6), Y(1), 6 * s, 3 * s, 0), (X(6), Y(1), 6 * s, 3 * s, 0)])
    art = paint(art, shoes, INK, seed=nx(), rough=0.6)
    torso = rrect(W, H, [(X(-15), Y(74), X(15), Y(32), 10 * s)])
    art = paint(art, torso, shirt, mix(shirt, "#000000", 0.06), seed=nx(), rough=1.0)
    # arms
    la = [(X(-13), Y(70)), (X(-20), Y(54)), (X(-18), Y(40))]
    ra = [(X(13), Y(70)), (X(22 + wave * 4), Y(84 + wave * 6)), (X(24 + wave * 2), Y(98 + wave * 2))] if wave else [(X(13), Y(70)), (X(20), Y(54)), (X(18), Y(40))]
    if carry:
        la = [(X(-13), Y(70)), (X(-16), Y(56)), (X(-4), Y(50))]
        ra = [(X(13), Y(70)), (X(16), Y(56)), (X(4), Y(50))]
    cl, cr = curve(la, 12), curve(ra, 12)
    arms = strokes(W, H, [(cl, 6 * s, None), (cr, 6 * s, None)])
    art = paint(art, arms, skin, mix(skin, "#000000", 0.08), seed=nx(), rough=0.8)
    sleeves = strokes(W, H, [(cl[:5], 8 * s, None), (cr[:5], 8 * s, None)])
    art = paint(art, sleeves, shirt, mix(shirt, "#000000", 0.08), seed=nx(), rough=0.6)
    hands = circles(W, H, [(la[-1][0], la[-1][1], 4 * s), (ra[-1][0], ra[-1][1], 4 * s)])
    art = paint(art, hands, skin, seed=nx(), rough=0.5)
    # vest with reflective stripes
    vest_m = shapes(W, H, [[(X(-15), Y(70)), (X(-6), Y(73)), (X(-3), Y(52)), (X(3), Y(52)), (X(6), Y(73)), (X(15), Y(70)), (X(15), Y(34)), (X(-15), Y(34))]])
    art = paint(art, vest_m, vest, mix(vest, "#000000", 0.1), seed=nx(), rough=1.0)
    stripes = shapes(W, H, [rr(X(-15), Y(48), X(-4), Y(44)), rr(X(4), Y(48), X(15), Y(44)), rr(X(-15), Y(40), X(-4), Y(37)), rr(X(4), Y(40), X(15), Y(37))], smooth=False) * vest_m
    art = paint(art, stripes, "#fff3b8", "#ffe680", seed=nx(), rough=0.4)
    # neck + head
    art = paint(art, rrect(W, H, [(X(-3.5), Y(80), X(3.5), Y(72), 2 * s)]), skin, seed=nx(), rough=0.4)
    head = circles(W, H, [(X(0), Y(87), 10 * s)])
    if hijab:
        hj = np.clip(circles(W, H, [(X(0), Y(87.5), 12.5 * s)]) + shapes(W, H, [[(X(-12.5), Y(87)), (X(12.5), Y(87)), (X(15), Y(70)), (X(0), Y(64)), (X(-15), Y(70))]]), 0, 1)
        art = paint(art, hj, hijab, mix(hijab, "#000000", 0.12), seed=nx(), rough=0.8)
        face = ellipses(W, H, [(X(0), Y(85.5), 7.2 * s, 8.4 * s, 0)])
        art = paint(art, face, skin, seed=nx(), rough=0.5)
    else:
        art = paint(art, head, skin, seed=nx(), rough=0.6)
        hair = np.clip(circles(W, H, [(X(0), Y(90), 10.5 * s)]) - circles(W, H, [(X(2), Y(84), 9.5 * s)]), 0, 1) * (np.arange(H)[:, None] < Y(84))
        art = paint(art, hair, "#2a1a14", seed=nx(), rough=0.6)
    # cheek blush hint (no features)
    art = over(art, flat(gaussian_filter(circles(W, H, [(X(4), Y(84), 2.4 * s)]), 1.5), "#e0705a", 0.35))
    return art


def sembako_box(art, W, H, x0, y0, w, h, nx, items=True, rng=None):
    if items:
        # rice sack + oil bottle + noodle pack peeking out
        art = paint(art, rrect(W, H, [(x0 + w * 0.12, y0 - h * 0.42, x0 + w * 0.46, y0 + h * 0.2, w * 0.08)]), "#f4ead6", "#e6d8bd", seed=nx(), rough=0.8)
        art = paint(art, shapes(W, H, [rr(x0 + w * 0.16, y0 - h * 0.2, x0 + w * 0.42, y0 - h * 0.12)], smooth=False), RED, seed=nx(), rough=0.4)
        art = paint(art, rrect(W, H, [(x0 + w * 0.54, y0 - h * 0.5, x0 + w * 0.7, y0 + h * 0.2, w * 0.04)]), "#e8b93a", "#d9a42b", seed=nx(), rough=0.6)
        art = paint(art, rrect(W, H, [(x0 + w * 0.58, y0 - h * 0.62, x0 + w * 0.66, y0 - h * 0.48, w * 0.02)]), GREEN, seed=nx(), rough=0.4)
        art = paint(art, rrect(W, H, [(x0 + w * 0.72, y0 - h * 0.28, x0 + w * 0.9, y0 + h * 0.2, w * 0.03)]), ORANGE, seed=nx(), rough=0.6)
    body = shapes(W, H, [rr(x0, y0, x0 + w, y0 + h)], smooth=False)
    art = over(art, soft_shadow(body, INK, 6, 0.25, 4, 6))
    art = paint(art, body, KRAFT, "#d6a96d", seed=nx(), rough=1.0, streak=1.6)
    flaps = shapes(W, H, [[(x0, y0), (x0 - w * 0.12, y0 - h * 0.22), (x0 + w * 0.36, y0 - h * 0.18), (x0 + w * 0.42, y0)],
                          [(x0 + w, y0), (x0 + w * 1.12, y0 - h * 0.22), (x0 + w * 0.64, y0 - h * 0.18), (x0 + w * 0.58, y0)]], smooth=False)
    art = paint(art, flaps, KRAFT_D, KRAFT, seed=nx(), rough=0.8)
    tape = shapes(W, H, [rr(x0, y0 + h * 0.06, x0 + w, y0 + h * 0.16)], smooth=False)
    art = over(art, flat(tape, "#e9cf9b", 0.8))
    hm = shapes(W, H, [heart_pts(x0 + w / 2, y0 + h * 0.56, w * 0.012)])
    art = paint(art, hm, RED, RED_D, seed=nx(), rough=0.6)
    return art


if "hands" in PARTS:
    W, H = 640, 560
    nx = Seq(100); rng = random.Random(3)
    art = blank(W, H)
    cx, cy, sc = 320, 250, 12.5
    outline = heart_pts(cx, cy, sc, 120)
    # left hand = left half of the heart outline, right hand = right half (thick strokes), sleeves at the wrists
    left = [p for p in outline if p[0] <= cx + 2]
    right = [p for p in outline if p[0] >= cx - 2]
    # order each half from the bottom tip upward
    def half(points, sign):
        pts = sorted(points, key=lambda p: math.atan2(p[1] - cy, sign * (p[0] - cx)))
        return pts
    hl = curve([outline[i] for i in range(60, 121, 6) if i < 120] + [outline[0]], 60)
    hr = curve([outline[i] for i in range(60, -1, -6)], 60)
    art = over(art, soft_shadow(np.clip(strokes(W, H, [(hl, 64, (0.05, 0.12)), (hr, 64, (0.05, 0.12))]), 0, 1), INK, 10, 0.25, 6, 10))
    for pts, skin, sleeve, sx, idx in ((hl, SKINS[0], ORANGE, -1, 81), (hr, SKINS[2], TEAL, 1, 39)):
        jx, jy = outline[idx]
        fore = [(jx, jy), (jx + sx * 90, jy + 80), (jx + sx * 150, H + 30)]
        fm = strokes(W, H, [(curve(fore, 16), 70, None)])
        art = paint(art, fm, skin, mix(skin, "#000000", 0.14), seed=nx(), rough=1.2)
        sl = strokes(W, H, [(curve([(jx + sx * 96, jy + 92), (jx + sx * 150, H + 30)], 8), 84, None)])
        art = paint(art, sl, sleeve, mix(sleeve, "#000000", 0.12), seed=nx(), rough=1.2)
        m = strokes(W, H, [(pts, 64, (0.06, 0.14))])
        art = paint(art, m, skin, mix(skin, "#000000", 0.12), seed=nx(), rough=1.4)
        n = len(pts)
        cr_items = []
        for f in (0.8, 0.86, 0.92):
            i = int(n * f)
            (ax, ay), (bx, by_) = pts[i], pts[min(n - 1, i + 1)]
            ang = math.atan2(by_ - ay, bx - ax) + math.pi / 2
            cr_items.append(([(ax - math.cos(ang) * 22, ay - math.sin(ang) * 22), (ax + math.cos(ang) * 22, ay + math.sin(ang) * 22)], 3.2, (0.3, 0.3)))
        art = over(art, flat(strokes(W, H, cr_items) * m, mix(skin, "#000000", 0.4), 0.6))
    tip = outline[60]
    art = paint(art, ellipses(W, H, [(tip[0] - 14, tip[1] - 14, 16, 26, -30), (tip[0] + 14, tip[1] - 14, 16, 26, 30)]), SKINS[1], seed=nx(), rough=0.8)
    clear()
    # red heart with a white cross inside
    inner = shapes(W, H, [heart_pts(cx, cy + 6, sc * 0.52, 80)])
    art = paint(art, inner, RED, "#e35e4b", seed=nx(), rough=1.0, streak=1.4)
    art = paint(art, cross(W, H, cx, cy - 4, 34, 11), WHITE, seed=nx(), rough=0.6)
    hl_ = strokes(W, H, [(arc_pts(cx - 62, cy - 52, 26, math.pi * 1.1, math.pi * 1.5, 10), 8, (0.3, 0.3))])
    art = over(art, flat(hl_, "#ffffff", 0.45))
    show(art, "bs-hands")
    save(art, f"{OUT}/hands.webp", max_w=440, quality=84)
    clear()

if "scene" in PARTS:
    W, H = 800, 440
    nx = Seq(200); rng = random.Random(9)
    art = blank(W, H)
    # ground
    ground = wavy_band(W, H, 392, H + 30, 4, 3, 0.8)
    art = paint(art, ground, "#9cc26a", "#87b05a", seed=nx(), rough=1.4, streak=1.4)
    # tree left
    art = paint(art, strokes(W, H, [([(70, 400), (74, 250)], 16, (0.0, 0.3))]), "#7a4e2e", seed=nx(), rough=0.8)
    crown = ellipses(W, H, [(70, 200, 70, 62, 0), (30, 236, 44, 36, 0), (112, 236, 46, 38, 0), (70, 150, 44, 40, 0)])
    art = paint(art, crown, GREEN, "#6fa048", seed=nx(), rough=2.0)
    clear()
    # tent: poles, striped canopy, scalloped valance, blank banner
    tx0, tx1, ty = 230, 620, 150
    poles = shapes(W, H, [rr(tx0 + 6, ty, tx0 + 14, 398), rr(tx1 - 14, ty, tx1 - 6, 398)], smooth=False)
    art = paint(art, poles, "#8a8f99", seed=nx(), rough=0.4)
    canopy = shapes(W, H, [[(tx0 - 10, ty + 40), (tx0 + 60, ty - 40), (tx1 - 60, ty - 40), (tx1 + 10, ty + 40)]], smooth=False)
    art = over(art, soft_shadow(canopy, INK, 8, 0.25, 0, 10))
    art = paint(art, canopy, CREAM, seed=nx(), rough=1.0)
    stripes = np.zeros((H, W), np.float32)
    for k in range(0, 8, 2):
        a = k / 8; b = (k + 1) / 8
        top_a, top_b = tx0 + 60 + (tx1 - tx0 - 120) * a, tx0 + 60 + (tx1 - tx0 - 120) * b
        bot_a, bot_b = tx0 - 10 + (tx1 - tx0 + 20) * a, tx0 - 10 + (tx1 - tx0 + 20) * b
        stripes += shapes(W, H, [[(top_a, ty - 40), (top_b, ty - 40), (bot_b, ty + 40), (bot_a, ty + 40)]], smooth=False)
    art = paint(art, np.clip(stripes, 0, 1) * canopy, RED, "#e05a48", seed=nx(), rough=0.8)
    scal = np.zeros((H, W), np.float32)
    for i, x in enumerate(np.arange(tx0 - 10, tx1 + 10, 30)):
        scal = np.maximum(scal, circles(W, H, [(x + 15, ty + 40, 15)]) * (np.arange(H)[:, None] >= ty + 40))
    scal = np.clip(scal + shapes(W, H, [rr(tx0 - 10, ty + 34, tx1 + 10, ty + 42)], smooth=False), 0, 1)
    art = paint(art, scal, RED_D, RED, seed=nx(), rough=0.6)
    # table with cloth + a blood pressure kit and a water jug
    table = shapes(W, H, [rr(300, 318, 560, 336)], smooth=False)
    cloth = shapes(W, H, [[(296, 330), (564, 330), (570, 382), (290, 382)]], smooth=False)
    art = paint(art, cloth, WHITE, "#f1e9dd", seed=nx(), rough=0.8)
    art = paint(art, shapes(W, H, [rr(296, 352, 570, 362)], smooth=False) * cloth, RED, seed=nx(), rough=0.4)
    art = paint(art, rrect(W, H, [(320, 296, 372, 330, 6)]), "#e9eef2", "#d7dee4", seed=nx(), rough=0.5)
    art = paint(art, circles(W, H, [(346, 312, 10)]), "#3e5a7a", seed=nx(), rough=0.4)
    art = paint(art, rrect(W, H, [(500, 282, 530, 330, 8)]), "#bfe3ea", "#9ccfd8", seed=nx(), rough=0.5)
    clear()
    # blood-drop sign on a stand (right of the tent)
    art = paint(art, strokes(W, H, [([(676, 398), (676, 240)], 6, None)]), "#8a8f99", seed=nx(), rough=0.4)
    sign = circles(W, H, [(676, 220, 40)])
    art = paint(art, sign, WHITE, "#f4ece0", seed=nx(), rough=0.6)
    drop = shapes(W, H, [[(676, 192)] + [(676 + math.cos(a) * 20, 226 + math.sin(a) * 20) for a in np.linspace(-0.45, math.pi + 0.45, 18)]])
    art = paint(art, drop, RED, RED_D, seed=nx(), rough=0.5)
    art = paint(art, cross(W, H, 676, 228, 9, 3), WHITE, seed=nx(), rough=0.3)
    # sembako boxes stack (left)
    art = sembako_box(art, W, H, 140, 330, 92, 66, nx, items=False)
    art = sembako_box(art, W, H, 150, 278, 76, 52, nx, items=True)
    clear()
    # volunteers: one behind the table, one carrying a box, one waving (hijab), one beside the sign
    art = person(art, W, H, 432, 396, 150, nx, SKINS[1], hijab="#3e8f8a")
    art = paint(art, cloth, WHITE, "#f1e9dd", seed=nx(), rough=0.8)
    art = paint(art, shapes(W, H, [rr(296, 352, 570, 362)], smooth=False) * cloth, RED, seed=nx(), rough=0.4)
    art = person(art, W, H, 262, 410, 140, nx, SKINS[0], carry=True)
    art = sembako_box(art, W, H, 236, 336, 52, 38, nx, items=False)
    art = person(art, W, H, 600, 412, 146, nx, SKINS[2], hijab="#e8a0a8", wave=1, shirt="#7a5aa0")
    art = person(art, W, H, 740, 416, 132, nx, SKINS[3], vest=YEL, shirt="#3e5a7a")
    clear()
    # grass tufts + flowers
    tufts = strokes(W, H, [([(x, 400), (x + rng.uniform(-4, 4), 400 - rng.uniform(6, 16))], 2.2, (0.0, 0.8)) for x in rng.sample(range(0, W), 120)])
    art = paint(art, tufts, GREEN_D, seed=nx(), rough=0.4)
    fl = circles(W, H, [(rng.uniform(0, W), rng.uniform(404, 432), 3.2) for _ in range(30)])
    art = paint(art, fl, YEL, seed=nx(), rough=0.3)
    show(art, "bs-scene")
    save(art, f"{OUT}/scene.webp", max_w=780, quality=82)
    clear()

if "box" in PARTS:
    W, H = 240, 240
    nx = Seq(300)
    art = blank(W, H)
    art = sembako_box(art, W, H, 50, 110, 140, 100, nx, items=True)
    show(art, "bs-box")
    save(art, f"{OUT}/box.webp", max_w=130, quality=84)
    clear()

if "drop" in PARTS:
    W, H = 200, 240
    nx = Seq(400)
    art = blank(W, H)
    drop = shapes(W, H, [[(100, 20)] + [(100 + math.cos(a) * 70, 150 + math.sin(a) * 70) for a in np.linspace(-0.5, math.pi + 0.5, 30)]])
    art = over(art, soft_shadow(drop, INK, 6, 0.2, 4, 6))
    art = paint(art, drop, RED, "#e35e4b", seed=nx(), rough=1.0, streak=1.4)
    art = paint(art, cross(W, H, 100, 156, 30, 10), WHITE, seed=nx(), rough=0.5)
    art = over(art, flat(strokes(W, H, [(arc_pts(100, 150, 50, math.pi * 1.05, math.pi * 1.4, 10), 8, (0.3, 0.3))]), "#ffffff", 0.45))
    show(art, "bs-drop")
    save(art, f"{OUT}/drop.webp", max_w=100, quality=84)
    clear()

if "person" in PARTS:
    W, H = 220, 300
    nx = Seq(500)
    art = blank(W, H)
    art = person(art, W, H, 110, 292, 270, nx, SKINS[1], wave=1)
    show(art, "bs-person")
    save(art, f"{OUT}/person.webp", max_w=140, quality=84)
    clear()

if "bunting" in PARTS:
    W, H = 840, 90
    nx = Seq(600)
    art = blank(W, H)
    pts = [(x, 12 + 26 * math.sin(math.pi * x / W)) for x in np.linspace(0, W, 40)]
    art = paint(art, strokes(W, H, [(pts, 2.4, None)]), INK, seed=nx(), rough=0.4)
    cols = [RED, YEL, ORANGE, GREEN, CREAM]
    for i, x in enumerate(np.arange(20, W - 20, 48)):
        y = 12 + 26 * math.sin(math.pi * x / W)
        y2 = 12 + 26 * math.sin(math.pi * (x + 36) / W)
        flag = shapes(W, H, [[(x, y), (x + 36, y2), (x + 18, max(y, y2) + 40)]], smooth=False)
        art = paint(art, flag, cols[i % 5], mix(cols[i % 5], "#000000", 0.1), seed=nx(), rough=0.8)
    show(art, "bs-bunting")
    save(art, f"{OUT}/bunting.webp", max_w=780, quality=82)
    clear()

if "paper" in PARTS:
    W = H = 360
    big = wrap_noise(W, H, 31, 30) - 0.5
    fine = wrap_noise(W, H, 32, 0.7) - 0.5
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fbefdc"), np.float32) * (1 + big * 0.04 + fine * 0.05)[..., None]
    rng = random.Random(5)
    flecks = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.5, 1.3)) for _ in range(160)])
    base = base * (1 - flecks[..., None] * 0.12)
    save_rgb(np.concatenate([base, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/paper.webp", quality=74)
