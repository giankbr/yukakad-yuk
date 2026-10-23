"""Konser Amal — a screen-printed gig poster in gouache: a night stage with lamp truss, string lights, drum kit,
keyboard, guitar on a stand, amp and a mic stand; spotlight beams and a crowd of raised hands (separate, animated);
plus a vintage microphone, a donation jar with coins, a music-note sticker, a painted sound-wave divider and a
poster-paper tile. Original, no brands, no text in the art.
Run: python3 -I konser-amal.py [part ...]   parts: stage beam crowd mic jar note wave paper
Assets -> public/themes/art/konser-amal/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k4_lib import *

OUT = outdir("konser-amal")
PARTS = sys.argv[1:] or ["stage", "beam", "crowd", "mic", "jar", "note", "wave", "paper"]
INDIGO, INDIGO2, NIGHT = "#2a2160", "#3a2f7a", "#16113a"
PLUM = "#3b1f4f"
AMBER, AMBER2 = "#ffc94a", "#ffe08a"
CORAL, CORAL2 = "#ff6b4a", "#ff8f6b"
TEAL, TEAL2 = "#2ec4b6", "#7ee0d4"
CREAM = "#f6efe2"
INK = "#1b1433"


def halftone(W, H, tone, cell=6.0, ang=0.4):
    """Screen-print halftone dots: tone (0..1) -> dot coverage."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx * math.cos(ang) + yy * math.sin(ang)) / cell
    v = (-xx * math.sin(ang) + yy * math.cos(ang)) / cell
    d = np.hypot((u % 1) - 0.5, (v % 1) - 0.5)
    r = np.sqrt(np.clip(tone, 0, 1)) * 0.62
    return np.clip((r - d) * cell * 1.2 + 0.5, 0, 1)


def paint(art, mask, c1, c2=None, seed=1, rough=1.6, streak=0.8):
    return GP(art, mask, c1, c2 or c1, seed=seed, rough=rough, streak=streak, pad=10)


def rr(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


if "stage" in PARTS:
    W, H = 780, 600
    nx = Seq(500)
    rng = random.Random(7)
    sky = painted_sky(W, H, [(0, "#120d30"), (0.45, "#261d5c"), (0.8, "#3b2a72"), (1, "#4a2f6e")], seed=3, streak=0.9)
    art = sky
    # halftone glow behind the band
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip(1 - np.hypot((xx - W / 2) / 360, (yy - 330) / 260), 0, 1) ** 1.4
    art = over(art, flat(halftone(W, H, g * 0.75, 7, 0.5), "#7a4fb0", 0.55))
    # backdrop drape folds (plum)
    folds = []
    for i in range(0, W + 40, 52):
        folds.append(rr(i, 70, i + 26, 470))
    art = over(art, flat(gaussian_filter(shapes(W, H, folds, smooth=False), 6), "#000000", 0.18))
    # string lights
    for k, (y0, sag) in enumerate(((112, 34), (132, 22))):
        pts = [(x, y0 + sag * math.sin(math.pi * x / W)) for x in np.linspace(-10, W + 10, 60)]
        art = paint(art, strokes(W, H, [(pts, 2.2, None)]), "#0c0920", seed=nx(), rough=0.6)
        bulbs = [(x, y0 + sag * math.sin(math.pi * x / W) + 7, 5.2) for x in np.linspace(20 + k * 18, W - 20, 17)]
        bm = circles(W, H, bulbs)
        art = over(art, glow(bm, AMBER2, 9, 0.5))
        art = paint(art, bm, AMBER2, "#fff4c8", seed=nx(), rough=0.8)
    # lamp truss at the top
    truss = shapes(W, H, [rr(0, 22, W, 34), rr(0, 58, W, 66)], smooth=False)
    diag = strokes(W, H, [([(x, 30), (x + 22, 62)], 3, None) for x in range(0, W, 22)] + [([(x + 22, 30), (x, 62)], 3, None) for x in range(0, W, 44)])
    art = paint(art, np.maximum(truss, diag), "#4b4466", "#2e2848", seed=nx(), rough=0.8)
    cans = []
    for k, x in enumerate((110, 250, 390, 530, 670)):
        a = (k - 2) * 0.22
        c = [(x - 16, 62), (x + 16, 62), (x + 22 + a * 30, 100), (x - 22 + a * 30, 100)]
        cans.append(c)
    cm = shapes(W, H, cans, smooth=False)
    art = paint(art, cm, "#1d1838", "#3a3360", seed=nx(), rough=0.8)
    lens = ellipses(W, H, [(x + (k - 2) * 0.22 * 30, 100, 18, 6, 0) for k, x in enumerate((110, 250, 390, 530, 670))])
    art = over(art, glow(lens, AMBER, 12, 0.7))
    art = paint(art, lens, "#fff2c0", seed=nx(), rough=0.5)
    # stage platform
    floor = shapes(W, H, [[(0, 470), (W, 470), (W, H), (0, H)]], smooth=False)
    art = paint(art, floor, "#1c1438", "#2a1e4c", seed=nx(), rough=1.0, streak=1.2)
    lip = shapes(W, H, [rr(0, 466, W, 480)], smooth=False)
    art = paint(art, lip, CORAL, "#e85537", seed=nx(), rough=0.8)
    planks = strokes(W, H, [([(x, 482), (x + (x - W / 2) * 0.3, H)], 2, None) for x in range(20, W, 60)])
    art = over(art, flat(planks, "#000000", 0.25))
    # risers + drum kit (centre back)
    riser = shapes(W, H, [rr(300, 410, 480, 470)], smooth=False)
    art = paint(art, riser, "#2d2252", "#3a2d66", seed=nx(), rough=1.0)
    kick = circles(W, H, [(390, 392, 46)])
    art = paint(art, kick, "#f6efe2", "#e6dccb", seed=nx(), rough=1.0)
    art = paint(art, np.clip(kick - circles(W, H, [(390, 392, 38)]), 0, 1), CORAL, seed=nx(), rough=0.8)
    art = over(art, flat(circles(W, H, [(390, 392, 16)]), TEAL, 0.9))
    toms = ellipses(W, H, [(352, 336, 22, 13, -12), (428, 336, 22, 13, 12)])
    toms_body = shapes(W, H, [rr(330, 336, 374, 360), rr(406, 336, 450, 360)], smooth=False)
    art = paint(art, np.maximum(toms, toms_body), "#d84a35", "#ff6b4a", seed=nx(), rough=0.8)
    art = paint(art, toms, "#f6efe2", seed=nx(), rough=0.6)
    cym = ellipses(W, H, [(304, 300, 34, 7, -10), (480, 292, 38, 7, 12), (290, 380, 22, 6, 0)])
    stands = strokes(W, H, [([(304, 300), (300, 410)], 3, None), ([(480, 292), (486, 410)], 3, None), ([(290, 380), (292, 470)], 3, None)])
    art = paint(art, stands, "#a9a2c4", seed=nx(), rough=0.5)
    art = paint(art, cym, AMBER, "#e0a52c", seed=nx(), rough=0.6)
    # keyboard (left)
    kb_st = strokes(W, H, [([(120, 404), (96, 470)], 4, None), ([(120, 404), (150, 470)], 4, None), ([(220, 404), (196, 470)], 4, None), ([(220, 404), (250, 470)], 4, None)])
    art = paint(art, kb_st, "#9b93b8", seed=nx(), rough=0.5)
    kb = shapes(W, H, [[(84, 384), (256, 384), (262, 404), (80, 404)]], smooth=False)
    art = paint(art, kb, "#14102c", seed=nx(), rough=0.6)
    keys = shapes(W, H, [rr(92 + i * 8, 388, 98 + i * 8, 400) for i in range(20)], smooth=False)
    art = paint(art, keys, CREAM, seed=nx(), rough=0.3)
    # amp + guitar on a stand (right)
    amp = shapes(W, H, [rr(560, 392, 650, 470)], smooth=False)
    art = paint(art, amp, "#1a1530", "#272046", seed=nx(), rough=0.8)
    grill = shapes(W, H, [rr(568, 404, 642, 460)], smooth=False)
    art = over(art, flat(grill * halftone(W, H, np.ones((H, W)) * 0.5, 4, 0.0), "#5a5280", 0.9))
    gbody = shapes(W, H, [deform(ellipse_pts(690, 424, 30, 26, 16), rng, 1, 0.04), deform(ellipse_pts(690, 392, 22, 20, 14), rng, 1, 0.04)])
    neck = shapes(W, H, [[(686, 380), (694, 380), (700, 284), (690, 284)]], smooth=False)
    head = shapes(W, H, [[(688, 290), (702, 290), (704, 262), (690, 264)]], smooth=False)
    art = paint(art, strokes(W, H, [([(690, 452), (672, 470)], 3, None), ([(690, 452), (708, 470)], 3, None)]), "#9b93b8", seed=nx(), rough=0.4)
    art = paint(art, gbody, TEAL, "#25a99c", seed=nx(), rough=0.8)
    art = paint(art, np.maximum(neck, head), "#6b4428", "#8a5a34", seed=nx(), rough=0.5)
    art = over(art, flat(circles(W, H, [(690, 404, 8)]), INK, 0.95))
    # mic stand front centre
    ms = strokes(W, H, [([(390, 470), (390, 352)], 4, None), ([(390, 470), (366, 482)], 3, None), ([(390, 470), (414, 482)], 3, None), ([(390, 360), (414, 340)], 3, None)])
    art = paint(art, ms, "#cfc8e6", seed=nx(), rough=0.4)
    art = paint(art, ellipses(W, H, [(418, 336, 8, 12, 40)]), "#2b2440", seed=nx(), rough=0.3)
    # warm pool of light on the floor
    pool = ellipses(W, H, [(390, 500, 200, 34, 0)])
    art = over(art, glow(pool, AMBER2, 22, 0.35))
    # print grain + slight misregistration feel
    art = add_grain(art, 9, 0.05)
    show(art, "ka-stage")
    save_rgb(art, f"{OUT}/stage.webp", quality=78)
    clear()

if "beam" in PARTS:
    W, H = 240, 640
    cone = shapes(W, H, [[(110, 0), (130, 0), (W - 6, H), (6, H)]], smooth=False)
    yy = np.linspace(1, 0.15, H, dtype=np.float32)[:, None]
    m = gaussian_filter(cone, 10) * yy
    streaks = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (40, 3))
    streaks = (streaks - streaks.min()) / (streaks.max() - streaks.min())
    m = m * (0.75 + 0.5 * streaks)
    art = flat(np.clip(m * 0.85, 0, 1), "#ffe6a0")
    show(art, "ka-beam", bg=NIGHT)
    save_full(art, f"{OUT}/beam.webp", size=(160, 427), quality=80)

if "crowd" in PARTS:
    W, H = 780, 230
    rng = random.Random(17)
    nx = Seq(900)
    heads, bodies, arms = [], [], []
    x = -10
    while x < W + 20:
        hy = rng.uniform(96, 130)
        r = rng.uniform(17, 23)
        heads.append(deform(ellipse_pts(x, hy, r, r * 1.08, 14), rng, 1, 0.04))
        bodies.append([(x - r * 1.9, H + 5), (x - r * 1.5, hy + r * 1.3), (x, hy + r * 0.9), (x + r * 1.5, hy + r * 1.3), (x + r * 1.9, H + 5)])
        if rng.random() < 0.55:
            side = rng.choice([-1, 1])
            ax = x + side * r * 1.2
            top = (ax + side * rng.uniform(4, 20), hy - rng.uniform(40, 70))
            arms.append((curve([(ax, hy + r * 1.4), (ax + side * 6, hy - 10), top], 18), 11, (0.0, 0.0)))
            fist = top
            heads.append(deform(ellipse_pts(fist[0], fist[1] - 4, 8, 9, 10), rng, 1, 0.05))
            if rng.random() < 0.25:  # phone light / light stick
                bodies.append(rr(fist[0] - 3, fist[1] - 26, fist[0] + 3, fist[1] - 6))
        x += rng.uniform(34, 50)
    sil = np.maximum.reduce([shapes(W, H, heads), shapes(W, H, bodies, smooth=False), strokes(W, H, arms)])
    art = blank(W, H)
    art = paint(art, sil, "#120c2a", "#1f1640", seed=nx(), rough=1.2)
    # rim light from the stage on the top edges
    rim = np.clip(sil - np.roll(sil, 4, 0), 0, 1)
    art = over(art, flat(gaussian_filter(rim, 1.0), "#ff9a6b", 0.7))
    show(art, "ka-crowd", bg="#3b2a72")
    save(art, f"{OUT}/crowd.webp", max_w=780, quality=80)

if "mic" in PARTS:
    W, H = 220, 340
    nx = Seq(1300)
    art = blank(W, H)
    head = shapes(W, H, [deform(ellipse_pts(110, 96, 62, 78, 20), random.Random(2), 1, 0.03)])
    art = over(art, drop_shadow(head, INK, 6, 5, 7, 0.35))
    art = paint(art, head, "#d9d2ea", "#b7aed2", seed=nx(), rough=1.0)
    grille = head * halftone(W, H, np.ones((H, W)) * 0.45, 7, 0.78)
    art = over(art, flat(grille, "#4a4170", 0.85))
    band = shapes(W, H, [rr(44, 92, 176, 108)], smooth=False) * head
    art = paint(art, band, CORAL, "#e85537", seed=nx(), rough=0.6)
    hl = gaussian_filter(ellipses(W, H, [(84, 66, 14, 26, -20)]), 4)
    art = over(art, flat(hl * head, "#ffffff", 0.55))
    neck = shapes(W, H, [[(96, 170), (124, 170), (118, 220), (102, 220)]], smooth=False)
    yoke = strokes(W, H, [(arc_pts(110, 150, 74, 0.1, math.pi - 0.1, 24), 8, None)])
    pole = shapes(W, H, [rr(104, 220, 116, 330)], smooth=False)
    art = paint(art, np.maximum.reduce([neck, yoke, pole]), "#3a3360", "#4b4466", seed=nx(), rough=0.6)
    show(art, "ka-mic", bg=CREAM)
    save(art, f"{OUT}/mic.webp", max_w=130, quality=84)

if "jar" in PARTS:
    W, H = 260, 300
    nx = Seq(1500)
    rng = random.Random(5)
    art = blank(W, H)
    jar = shapes(W, H, [[(60, 80), (200, 80), (214, 110), (218, 250), (200, 282), (60, 282), (42, 250), (46, 110)]])
    art = over(art, drop_shadow(jar, INK, 6, 4, 7, 0.3))
    # coins inside
    coins = [(rng.uniform(70, 190), rng.uniform(190, 270), rng.uniform(15, 20)) for _ in range(16)]
    cm = ellipses(W, H, [(x, y, r, r * 0.42, rng.uniform(-20, 20)) for x, y, r in coins]) * jar
    art = paint(art, cm, AMBER, "#e5a92e", seed=nx(), rough=0.7)
    art = over(art, flat(np.clip(cm - np.roll(cm, -3, 0), 0, 1), "#a8721a", 0.7))
    glass = flat(jar, "#bfe9ec", 0.32)
    art = over(art, glass)
    edge = np.clip((gaussian_filter(jar, 1.5) > 0.05).astype(np.float32) - (gaussian_filter(jar, 1.5) > 0.95).astype(np.float32), 0, 1)
    art = paint(art, edge, "#2b6e74", seed=nx(), rough=0.5)
    hl = strokes(W, H, [(curve([(70, 120), (64, 180), (70, 240)], 12), 7, (0.2, 0.3))])
    art = over(art, flat(hl, "#ffffff", 0.75))
    lid = shapes(W, H, [rr(54, 58, 206, 84)], smooth=False)
    art = paint(art, lid, CORAL, "#e85537", seed=nx(), rough=0.8)
    slot = shapes(W, H, [rr(104, 66, 156, 74)], smooth=False)
    art = paint(art, slot, INK, seed=nx(), rough=0.3)
    # heart label
    hp = []
    for t in np.linspace(0, math.tau, 40):
        hx = 16 * math.sin(t) ** 3; hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        hp.append((130 + hx * 2.1, 150 + hy * 2.1))
    heart = shapes(W, H, [hp])
    art = paint(art, heart, CORAL, CORAL2, seed=nx(), rough=0.8)
    # a coin dropping in
    drop = ellipses(W, H, [(130, 36, 16, 16, 0)])
    art = paint(art, drop, AMBER, AMBER2, seed=nx(), rough=0.6)
    art = over(art, flat(ellipses(W, H, [(130, 36, 9, 9, 0)]) - ellipses(W, H, [(130, 36, 7, 7, 0)]), "#a8721a", 0.8))
    show(art, "ka-jar", bg=CREAM)
    save(art, f"{OUT}/jar.webp", max_w=130, quality=84)

if "note" in PARTS:
    W, H = 200, 200
    nx = Seq(1700)
    heads = ellipses(W, H, [(62, 150, 26, 19, -22), (146, 130, 26, 19, -22)])
    stems = shapes(W, H, [rr(80, 52, 92, 150), rr(164, 34, 176, 130)], smooth=False)
    beam = shapes(W, H, [[(80, 52), (176, 34), (176, 62), (80, 80)]], smooth=False)
    note = np.maximum.reduce([heads, stems, beam])
    sticker = np.clip(gaussian_filter(note, 6) * 3, 0, 1)
    art = blank(W, H)
    art = over(art, drop_shadow(sticker, INK, 4, 3, 4, 0.35))
    art = paint(art, sticker, "#fffaf0", seed=nx(), rough=1.2)
    art = paint(art, note, CORAL, "#ff7f5a", seed=nx(), rough=1.0)
    show(art, "ka-note", bg="#d8cdb8")
    save(art, f"{OUT}/note.webp", max_w=90, quality=86)

if "wave" in PARTS:
    W, H = 720, 70
    nx = Seq(1900)
    pts = []
    for x in np.linspace(20, W - 20, 240):
        t = (x - 20) / (W - 40)
        env = math.sin(math.pi * t) ** 0.8
        pts.append((x, 35 + math.sin(x / 9.0) * 22 * env * (0.6 + 0.4 * math.sin(x / 41.0))))
    m = strokes(W, H, [(pts, 5, (0.05, 0.05))])
    art = paint(blank(W, H), m, CORAL, "#ff8f6b", seed=nx(), rough=1.0)
    dots = circles(W, H, [(14, 35, 6), (W - 14, 35, 6)])
    art = paint(art, dots, TEAL, seed=nx(), rough=0.6)
    show(art, "ka-wave", bg=CREAM)
    save(art, f"{OUT}/wave.webp", max_w=360, quality=84)

if "paper" in PARTS:
    W = H = 320
    a = wrap_noise(W, H, 3, 30); b = wrap_noise(W, H, 4, 0.7); c = wrap_noise(W, H, 5, 1.2)
    t = np.clip(0.5 + (a - 0.5) * 0.5 + (b - 0.5) * 0.35, 0, 1)
    rgb = ramp(t, [(0, "#e9dfcc"), (0.5, "#f3ebdc"), (1, "#faf5ea")])
    fleck = (c > 0.88).astype(np.float32) * 0.08
    rgb = rgb * (1 - fleck[..., None])
    p = rgba(rgb, np.ones((H, W), np.float32))
    show(p, "ka-paper")
    save_rgb(p, f"{OUT}/paper.webp", quality=70)
