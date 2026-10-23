"""Ultah Putri Duyung — kids' birthday under a pastel sea, gouache: Nila, an original little mermaid (brown skin, black
curly hair in two puffs with a coral starfish clip, peach scallop top, mint-to-lilac tail) holding up a pearl; a coral
castle with shell roofs; shells & pearls; pastel wave band; swaying seaweed.
Run: python3 -I ultah-putri-duyung.py [part ...]  parts: nila castle shells wave weed pearl bubble
Assets -> public/themes/art/ultah-putri-duyung/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l2_lib import *

OUT = outdir("ultah-putri-duyung")
PARTS = sys.argv[1:] or ["nila", "castle", "shells", "wave", "weed", "pearl"]
SKIN, SKIN_D, SKIN_L = "#b97a52", "#8f5a3a", "#d29a70"
HAIR, HAIR_L = "#2a1a1c", "#4a3034"
PEACH, PEACH_D, PEACH_L = "#f6a68f", "#e07f6c", "#ffc9b5"
MINT, MINT_D = "#86d6c6", "#4fae9f"
LILAC, LILAC_D, LILAC_L = "#b9a3ea", "#8a74c8", "#ddd0fa"
CORAL, CORAL_D = "#f58a8a", "#d4626c"
PEARL = "#fbf5ef"
ROCK, ROCK_D = "#a9a3c4", "#7d76a0"
INK = "#3b2a40"


def tube(cl, widths):
    """Closed polygon around a centre line with per-point widths."""
    L, R = [], []
    n = len(cl)
    if len(widths) != n:
        widths = list(np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(widths)), widths))
    for i in range(n):
        x0, y0 = cl[max(0, i - 1)]; x1, y1 = cl[min(n - 1, i + 1)]
        a = math.atan2(y1 - y0, x1 - x0)
        w = widths[i] / 2
        L.append((cl[i][0] + math.cos(a - math.pi / 2) * w, cl[i][1] + math.sin(a - math.pi / 2) * w))
        R.append((cl[i][0] + math.cos(a + math.pi / 2) * w, cl[i][1] + math.sin(a + math.pi / 2) * w))
    return L + R[::-1]


def rim(mask, px=1.6):
    """Thin outline just inside the shape edge (illustrator's line)."""
    return np.clip(mask - np.clip((gaussian_filter(mask, px) - 0.5) * 3 + 0.5, 0, 1), 0, 1) * 2.2


def side_shade(W, H, mask, cx, k=1.0, side=1):
    xx = np.arange(W, dtype=np.float32)[None, :]
    return mask * np.clip((xx - cx) * side / (k * 60), 0, 1)


def paint(art, m, c1, c2, nx, shade_col=None, shade=None, hi=None, line=None, rough=0.9):
    art = GP(art, m, c1, c2, seed=nx(), rough=rough, streak=0.9, pad=6)
    if shade is not None:
        art = G(art, np.clip(shade, 0, 1), shade_col, seed=nx(), density=0.55, edge=0.15, bloom=0.2, rough=2, feather=2)
    if hi is not None:
        art = G(art, np.clip(hi, 0, 1), "#ffffff", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=2, feather=2.5)
    if line:
        art = G(art, np.clip(rim(m), 0, 1), line, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4)
    return art


if "nila" in PARTS:
    W, H = 560, 640
    nx = Seq(41000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # rock
    rock = shapes(W, H, [deform([(80, 640), (90, 540), (150, 480), (250, 456), (360, 470), (440, 520), (470, 640)], random.Random(2), 2, 0.03)])
    art = paint(art, rock, ROCK, "#b8b1d4", nx, ROCK_D, side_shade(W, H, rock, 300, 2.0) + rock * np.clip((yy - 560) / 80, 0, 1), rock * np.clip((480 - yy) / 40 + 0.4, 0, 1) * np.clip((260 - xx) / 120, 0, 1), INK)
    spots = circles(W, H, [(150, 560, 10), (178, 590, 6), (390, 560, 9), (420, 600, 12), (300, 610, 7)])
    art = G(art, spots * rock, ROCK_D, seed=nx(), density=0.5, edge=0.4, bloom=0.1, rough=2)
    coral = strokes(W, H, [(curve([(110, 520), (100, 470), (84, 440)], 12), 9, (0.0, 0.5)), (curve([(102, 482), (124, 456), (130, 430)], 10), 7, (0.0, 0.5)),
                           (curve([(96, 470), (70, 452)], 6), 6, (0.0, 0.5))])
    art = paint(art, coral, CORAL, "#f7a0a0", nx, CORAL_D, side_shade(W, H, coral, 100, 0.3), None, CORAL_D)
    # tail: from the hips sweeping right over the rock, curling up to the fin
    cl = curve([(262, 392), (280, 450), (330, 492), (400, 500), (452, 470), (470, 428)], 60)
    wid = [96 * (1 - t) ** 0.9 + 22 * t for t in np.linspace(0, 1, len(cl))]
    tail = shapes(W, H, [tube(cl, wid)])
    tcol = np.clip((xx - 260) / 220, 0, 1)
    art = GP(art, tail, MINT, MINT_D, seed=nx(), rough=0.9, streak=0.9, pad=6)
    lil = gouache_paint(tail, LILAC, LILAC_L, seed=nx(), rough=0.9)
    lil[..., 3] *= tcol ** 1.2
    art = over(art, lil)
    # scales: rows of little arcs following the tail
    sc = []
    for i in range(4, len(cl) - 6, 3):
        x, y = cl[i]
        x0, y0 = cl[i - 1]
        a = math.atan2(y - y0, x - x0)
        w = wid[i] * 0.42
        for o in np.linspace(-w, w, max(2, int(w / 11))):
            px, py = x + math.cos(a + math.pi / 2) * o, y + math.sin(a + math.pi / 2) * o
            sc.append((arc_pts(px, py, 7, a + math.pi * 0.35, a + math.pi * 1.65, 8), 2.0, None))
    scm = strokes(W, H, sc) * tail
    art = G(art, scm, "#ffffff", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = G(art, np.clip(side_shade(W, H, tail, 300, 3) * np.clip((yy - 470) / 40, 0, 1), 0, 1), LILAC_D, seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=2, feather=2)
    art = G(art, np.clip(rim(tail), 0, 1), "#5a5290", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    # fin: two fans
    fin = shapes(W, H, [petal_pts(470, 430, 92, 30, -math.pi / 2 - 0.55, n=16), petal_pts(470, 430, 86, 28, -0.35, n=16)])
    art = paint(art, fin, LILAC_L, LILAC, nx, LILAC_D, fin * np.clip((xx - 470) / 60, 0, 1) * 0.6, None, "#5a5290")
    ribs = strokes(W, H, [([(470, 430), (470 + math.cos(a) * 80, 430 + math.sin(a) * 80)], 1.8, (0.1, 0.4)) for a in list(np.linspace(-math.pi / 2 - 0.9, -math.pi / 2 - 0.2, 4)) + list(np.linspace(-0.7, 0.0, 4))])
    art = G(art, ribs * fin, LILAC_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
    # hip frill where tail meets top
    frill = shapes(W, H, [ellipse_pts(262 + dx, 392, 15, 9, 10) for dx in range(-42, 50, 18)])
    art = paint(art, frill, MINT, "#a6e6d8", nx, MINT_D, frill * np.clip((yy - 392) / 8, 0, 1), None, "#3f8f84")
    # left arm resting on the rock (behind torso)
    arml = shapes(W, H, [tube(curve([(222, 300), (204, 350), (206, 398), (220, 432)], 30), [26, 24, 22, 20] * 0 + [26 - 6 * t for t in np.linspace(0, 1, 30)])])
    hand_l = shapes(W, H, [ellipse_pts(222, 438, 14, 11, 12, 0.5)])
    am = np.maximum(arml, hand_l)
    art = paint(art, am, SKIN, SKIN_L, nx, SKIN_D, side_shade(W, H, am, 212, 0.3), None, "#6a3e28")
    # torso + scallop top
    torso = shapes(W, H, [[(222, 300), (300, 300), (306, 340), (300, 396), (224, 396), (216, 340)]])
    art = paint(art, torso, SKIN, SKIN_L, nx, SKIN_D, side_shade(W, H, torso, 270, 0.6), None, "#6a3e28")
    top = shapes(W, H, [[(218, 304), (262, 296), (304, 304), (308, 336), (300, 372), (224, 372), (214, 336)]])
    scal = shapes(W, H, [ellipse_pts(x, 372, 11, 9, 12) for x in range(228, 300, 14)])
    topm = np.clip(np.maximum(top, scal), 0, 1)
    art = paint(art, topm, PEACH, PEACH_L, nx, PEACH_D, side_shade(W, H, topm, 266, 0.7), topm * np.clip((250 - xx) / 30, 0, 1), "#b95a4c")
    ridges = strokes(W, H, [([(262, 302), (228 + k * 14, 370)], 1.6, (0.2, 0.2)) for k in range(6)])
    art = G(art, ridges * topm, PEACH_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
    # pearl necklace
    necklace = [(262 + math.cos(a) * 30, 288 + math.sin(a) * 16) for a in np.linspace(0.35, math.pi - 0.35, 9)]
    pm = circles(W, H, [(x, y, 4.2) for x, y in necklace])
    art = paint(art, pm, PEARL, "#efe6ff", nx, "#c9bde0", pm * np.clip((yy % 1000 - 0) * 0, 0, 1), None, "#9a8cb8", rough=0.3)
    # neck
    neck = shapes(W, H, [[(248, 262), (276, 262), (278, 300), (246, 300)]], smooth=False)
    art = paint(art, neck, SKIN, SKIN_L, nx, SKIN_D, neck * np.clip((280 - yy) / 18, 0, 1), None, None)
    # right arm raised holding a pearl
    armr_cl = curve([(298, 306), (334, 286), (352, 248), (352, 214)], 30)
    armr = shapes(W, H, [tube(armr_cl, [26 - 7 * t for t in np.linspace(0, 1, 30)])])
    hand_r = shapes(W, H, [ellipse_pts(352, 206, 13, 14, 12)])
    ar = np.maximum(armr, hand_r)
    # hair puffs behind the head
    rng = random.Random(9)
    puffs = shapes(W, H, [deform(ellipse_pts(196, 140, 46, 42, 16), rng, 2, 0.06), deform(ellipse_pts(326, 140, 46, 42, 16), rng, 2, 0.06)])
    curls = circles(W, H, [(196 + math.cos(a) * 40, 140 + math.sin(a) * 36, 9) for a in np.linspace(0, math.tau, 14, endpoint=False)] + [(326 + math.cos(a) * 40, 140 + math.sin(a) * 36, 9) for a in np.linspace(0, math.tau, 14, endpoint=False)])
    pf = np.maximum(puffs, curls)
    art = paint(art, pf, HAIR, HAIR_L, nx, "#140c0e", None, None, None)
    curl_lines = strokes(W, H, [(spiral_pts(x, y, 7, 1.5, rng.uniform(0, 6), 1.1, 16, 1), 1.8, (0.0, 0.5)) for x, y in [(196 + rng.uniform(-30, 30), 140 + rng.uniform(-28, 28)) for _ in range(12)] + [(326 + rng.uniform(-30, 30), 140 + rng.uniform(-28, 28)) for _ in range(12)]])
    art = G(art, curl_lines * pf, "#6a4a50", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.3)
    # head
    head = shapes(W, H, [ellipse_pts(262, 212, 60, 58, 24)])
    ears = shapes(W, H, [ellipse_pts(203, 222, 10, 13, 10), ellipse_pts(321, 222, 10, 13, 10)])
    art = paint(art, ears, SKIN, SKIN_L, nx, SKIN_D, ears * 0.4, None, "#6a3e28")
    art = paint(art, head, SKIN, SKIN_L, nx, SKIN_D, side_shade(W, H, head, 282, 0.7), head * np.clip((236 - xx) / 40, 0, 1) * np.clip((214 - yy) / 40, 0, 1), "#6a3e28")
    # hair cap with curly fringe
    cap = shapes(W, H, [ellipse_pts(262, 196, 66, 52, 24)])
    face_cut = shapes(W, H, [ellipse_pts(262, 236, 56, 50, 24)])
    fringe = circles(W, H, [(222 + k * 13, 182 + 5 * math.sin(k * 1.3), 11) for k in range(7)])
    capm = np.clip(np.maximum(cap - face_cut, fringe * (yy < 200)) , 0, 1) * np.clip(head + cap, 0, 1)
    art = paint(art, capm, HAIR, HAIR_L, nx, "#140c0e", None, capm * np.clip((240 - xx) / 40, 0, 1) * np.clip((180 - yy) / 30, 0, 1) * 0.5, None)
    # starfish clip on the right puff
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 22 if k % 2 == 0 else 9
        star.append((342 + math.cos(a) * r, 112 + math.sin(a) * r))
    stm = shapes(W, H, [star])
    art = paint(art, stm, CORAL, "#ffb0a8", nx, CORAL_D, side_shade(W, H, stm, 342, 0.2), None, "#b5485a", rough=0.5)
    sdots = circles(W, H, [(342 + math.cos(-math.pi / 2 + k * 2 * math.pi / 5) * 11, 112 + math.sin(-math.pi / 2 + k * 2 * math.pi / 5) * 11, 2.2) for k in range(5)])
    art = GP(art, sdots, "#ffe0d6", seed=nx(), rough=0.2, pad=4)
    # face: eyes, brows, cheeks, smile, nose
    eyes = shapes(W, H, [ellipse_pts(240, 224, 7.5, 9.5, 14), ellipse_pts(284, 224, 7.5, 9.5, 14)])
    art = GP(art, eyes, INK, "#1f1426", seed=nx(), rough=0.3, pad=4)
    glint = circles(W, H, [(242.5, 220, 2.8), (286.5, 220, 2.8), (238, 228, 1.3), (282, 228, 1.3)])
    art = GP(art, glint, "#ffffff", seed=nx(), rough=0.1, pad=4)
    lash = strokes(W, H, [(arc_pts(240, 226, 11, math.pi * 1.12, math.pi * 1.62, 8), 2.0, (0.2, 0.2)), (arc_pts(284, 226, 11, math.pi * 1.38, math.pi * 1.88, 8), 2.0, (0.2, 0.2))])
    art = G(art, lash, INK, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3, feather=0.3)
    brows = strokes(W, H, [(arc_pts(240, 214, 14, math.pi * 1.25, math.pi * 1.7, 8), 2.6, (0.3, 0.3)), (arc_pts(284, 214, 14, math.pi * 1.3, math.pi * 1.75, 8), 2.6, (0.3, 0.3))])
    art = G(art, brows * (yy < 206), "#2a1a1c", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3, feather=0.3)
    cheeks = shapes(W, H, [ellipse_pts(226, 244, 11, 7, 12), ellipse_pts(298, 244, 11, 7, 12)])
    art = G(art, cheeks, "#f07a7a", seed=nx(), density=0.55, edge=0, bloom=0.2, rough=2, feather=3)
    smile = strokes(W, H, [(arc_pts(262, 238, 13, math.pi * 0.2, math.pi * 0.8, 12), 3.0, (0.25, 0.25))])
    art = G(art, smile, "#7a3a3a", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.3, feather=0.3)
    nose = shapes(W, H, [ellipse_pts(262, 236, 3.2, 2.2, 10)])
    art = G(art, nose, SKIN_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.2, feather=0.6)
    # raised arm (in front) + pearl with a glow
    art = paint(art, ar, SKIN, SKIN_L, nx, SKIN_D, side_shade(W, H, ar, 350, 0.25), None, "#6a3e28")
    pearl = circles(W, H, [(354, 186, 19)])
    art = over(art, glow(pearl, "#fff6e8", radius=16, strength=0.55))
    art = paint(art, pearl, PEARL, "#efe4ff", nx, "#c7b8e6", pearl * np.clip((xx - 350) / 18, 0, 1) * np.clip((yy - 182) / 18, 0, 1), None, "#a596c6", rough=0.3)
    art = GP(art, circles(W, H, [(348, 179, 5.5)]), "#ffffff", seed=nx(), rough=0.2, pad=4)
    fingers = strokes(W, H, [(arc_pts(352, 204, 15, math.pi * 1.05, math.pi * 1.5, 8), 5, (0.2, 0.3)), (arc_pts(354, 204, 15, math.pi * 1.55, math.pi * 1.95, 8), 5, (0.2, 0.3))])
    art = paint(art, fingers, SKIN, SKIN_L, nx, SKIN_D, None, None, "#6a3e28", rough=0.4)
    preview(art, "pd-nila", bg="#cfeef0")
    save(art, f"{OUT}/nila.webp", max_w=380, quality=84)
    clear()


def scallop_shell(W, H, cx, cy, r, ang=0.0, n=9):
    """Fan (scallop) shell polygon + rib strokes."""
    pts = []
    for i in range(n * 8 + 1):
        t = i / (n * 8)
        a = math.pi * (1.08 + 0.84 * t) + ang
        bump = 1 + 0.06 * abs(math.sin(t * n * math.pi))
        pts.append((cx + math.cos(a) * r * bump, cy + math.sin(a) * r * bump))
    pts += [(cx + math.cos(ang + math.pi * 0.25) * r * 0.22, cy + math.sin(ang + math.pi * 0.25) * r * 0.22 + r * 0.12),
            (cx + math.cos(ang + math.pi * 0.75) * r * 0.22, cy + math.sin(ang + math.pi * 0.75) * r * 0.22 + r * 0.12)]
    ribs = []
    for k in range(n + 1):
        a = math.pi * (1.1 + 0.8 * k / n) + ang
        ribs.append(([(cx, cy + r * 0.06), (cx + math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95)], 1.6, (0.1, 0.5)))
    return shapes(W, H, [pts]), strokes(W, H, ribs)


if "castle" in PARTS:
    W, H = 520, 560
    nx = Seq(42000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = random.Random(5)
    # sand mound
    sand = shapes(W, H, [deform([(0, 560), (10, 500), (120, 470), (260, 462), (400, 472), (510, 500), (520, 560)], rng, 2, 0.02)])
    art = paint(art, sand, "#f4dcb8", "#fbe9cf", nx, "#d9b88e", sand * np.clip((yy - 500) / 60, 0, 1), None, None)
    # towers: three coral-pink towers with shell (cone) roofs
    towers = [(150, 470, 70, 250), (260, 470, 92, 330), (372, 470, 70, 230)]
    for i, (cx, by, w, h) in enumerate(towers):
        body = shapes(W, H, [deform([(cx - w / 2, by), (cx - w / 2 + 4, by - h), (cx + w / 2 - 4, by - h), (cx + w / 2, by)], rng, 1, 0.02)])
        art = paint(art, body, "#f9b4ae", "#ffd2cb", nx, CORAL_D, side_shade(W, H, body, cx + w * 0.1, 0.4), body * np.clip((cx - w * 0.15 - xx) / 20, 0, 1) * 0.6, "#c45a66")
        # crenels band + windows
        band = shapes(W, H, [[(cx - w / 2 - 6, by - h + 4), (cx + w / 2 + 6, by - h + 4), (cx + w / 2 + 6, by - h + 22), (cx - w / 2 - 6, by - h + 22)]])
        art = paint(art, band, "#f58a8a", "#f9a8a0", nx, CORAL_D, None, None, "#c45a66")
        win = shapes(W, H, [[(cx - 11, by - h * 0.45), (cx - 11, by - h * 0.62), (cx, by - h * 0.7), (cx + 11, by - h * 0.62), (cx + 11, by - h * 0.45)]])
        art = paint(art, win, "#6fa9c9", "#8fc4de", nx, "#3f6f94", None, None, "#3f6f94", rough=0.4)
        art = G(art, circles(W, H, [(cx + 4, by - h * 0.62, 2.5)]), "#ffffff", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.2, feather=0.4)
        # roof: a tall conch-like cone with a spiral stripe
        top = by - h + 4
        roof = shapes(W, H, [[(cx - w / 2 - 10, top), (cx, top - w * 1.05), (cx + w / 2 + 10, top)]])
        art = paint(art, roof, LILAC, LILAC_L, nx, LILAC_D, side_shade(W, H, roof, cx, 0.3), None, "#5a5290")
        sp = []
        for k in range(4):
            y0 = top - k * w * 0.24
            hw = (w / 2 + 10) * (1 - k * 0.24)
            sp.append(([(cx - hw, y0), (cx + hw * 0.9, y0 - w * 0.16)], 3.0, (0.1, 0.3)))
        art = G(art, strokes(W, H, sp) * roof, "#ffffff", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.6)
        art = GP(art, circles(W, H, [(cx, top - w * 1.05 - 6, 7)]), PEARL, "#efe4ff", seed=nx(), rough=0.2, pad=4)
    # door
    door = shapes(W, H, [[(236, 470), (236, 410), (260, 388), (284, 410), (284, 470)]])
    art = paint(art, door, "#8a74c8", "#a58ee0", nx, "#5a5290", None, None, "#3b2a40", rough=0.4)
    # pearls strung along the middle tower + starfish on sand
    art = GP(art, circles(W, H, [(214 + k * 11.5, 300 + 6 * math.sin(k / 8 * math.pi), 4.2) for k in range(9)]), PEARL, "#f3eaff", seed=nx(), rough=0.2, pad=4)
    sh, ribs = scallop_shell(W, H, 92, 520, 30, 0.2)
    art = paint(art, sh, PEACH, PEACH_L, nx, PEACH_D, None, None, "#c4665a", rough=0.5)
    art = G(art, ribs * sh, PEACH_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.4)
    preview(art, "pd-castle", bg="#cfeef0")
    save(art, f"{OUT}/castle.webp", max_w=360, quality=84)
    clear()

if "shells" in PARTS:
    # a small cluster: scallop + pearl in an open clam — used as divider / node / emblem
    W, H = 300, 170
    nx = Seq(43000)
    art = blank(W, H)
    sh, ribs = scallop_shell(W, H, 92, 130, 62, 0.0, 10)
    art = paint(art, sh, PEACH, PEACH_L, nx, PEACH_D, sh * np.clip((np.mgrid[0:H, 0:W][1] - 92) / 60, 0, 1) * 0.6, None, "#c4665a", rough=0.5)
    art = G(art, ribs * sh, PEACH_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.3, feather=0.4)
    sh2, ribs2 = scallop_shell(W, H, 214, 138, 48, 0.25, 9)
    art = paint(art, sh2, LILAC_L, "#efe6ff", nx, LILAC, None, None, "#7a68b8", rough=0.5)
    art = G(art, ribs2 * sh2, LILAC, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.3, feather=0.4)
    pearls = circles(W, H, [(150, 148, 13), (172, 156, 8), (130, 158, 7)])
    art = over(art, glow(pearls, "#fff6e8", radius=10, strength=0.4))
    art = GP(art, pearls, PEARL, "#eee4ff", seed=nx(), rough=0.2, pad=4)
    art = GP(art, circles(W, H, [(146, 143, 3.5), (170, 153, 2.2)]), "#ffffff", seed=nx(), rough=0.1, pad=3)
    preview(art, "pd-shells", bg="#cfeef0")
    save(art, f"{OUT}/shells.webp", max_w=300, quality=84)
    clear()

if "pearl" in PARTS:
    W, H = 120, 120
    nx = Seq(44000)
    art = blank(W, H)
    p = circles(W, H, [(60, 60, 40)])
    art = over(art, glow(p, "#fff6e8", radius=14, strength=0.45))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = paint(art, p, PEARL, "#f1e8ff", nx, "#c7b8e6", p * np.clip((xx - 58) / 40, 0, 1) * np.clip((yy - 56) / 40, 0, 1), None, "#a596c6", rough=0.3)
    art = G(art, p * np.clip((50 - xx) / 30, 0, 1) * np.clip((yy - 40) / 40, 0, 1), "#ffd6e0", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=2, feather=3)
    art = GP(art, circles(W, H, [(46, 44, 10)]), "#ffffff", seed=nx(), rough=0.2, pad=4)
    preview(art, "pd-pearl", bg="#cfeef0")
    save(art, f"{OUT}/pearl.webp", max_w=120, quality=84)
    clear()

if "weed" in PARTS:
    W, H = 160, 420
    nx = Seq(45000)
    art = blank(W, H)
    rng = random.Random(9)
    blades = []
    for k, (x0, h, c) in enumerate([(50, 400, 0), (86, 330, 1), (116, 380, 0), (30, 250, 1)]):
        pts = [(x0 + 18 * math.sin(t * 5 + k) * t, 420 - t * h) for t in np.linspace(0, 1, 26)]
        blades.append((pts, 22 - k * 2, (0.9, 0.1), c))
    for pts, w, taper, c in blades:
        m = strokes(W, H, [(pts, w, taper)])
        art = paint(art, m, MINT if c == 0 else "#9be0b8", "#b8f0dd", nx, MINT_D, None, None, "#3e8f7f", rough=0.8)
    art = GP(art, circles(W, H, [(70, 200, 5), (104, 150, 4), (40, 120, 3.5)]), "#ffffff", seed=nx(), rough=0.2, pad=3)
    preview(art, "pd-weed", bg="#cfeef0")
    save(art, f"{OUT}/weed.webp", max_w=160, quality=84)
    clear()

if "wave" in PARTS:
    # seamless horizontal pastel wave band (tile 480 wide)
    W, H = 480, 120
    nx = Seq(46000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    layers = [("#bfe9ec", "#d8f4f4", 40, 14), ("#a9dcd8", "#c8eeea", 64, 12), ("#c7b6ef", "#ddd0fa", 88, 10)]
    for k, (c1, c2, base, amp) in enumerate(layers):
        top = base + amp * np.sin(xx / W * 2 * math.pi * 3 + k * 1.3)
        m = (yy >= top).astype(np.float32)
        art = GP(art, m, c1, c2, seed=nx(), rough=0.7, streak=0.9, pad=0)
        crest = np.clip(1 - np.abs(yy - top - 3) / 3, 0, 1)
        art = G(art, crest, "#ffffff", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5, feather=0.6)
    preview(art, "pd-wave", bg="#ffffff")
    save(art, f"{OUT}/wave.webp", max_w=480, quality=82)
    clear()
