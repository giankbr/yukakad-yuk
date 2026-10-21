"""Sweet Seventeen — pink & pearl night glam: a big puffy satin-balloon "17", a satin bow with painted sheen and long
tails, pearl swags, a pearl-and-bow divider, hand-painted night sparkles and a painted plum night sky.
Run: python3 -I sweet-seventeen.py [part ...]  parts: seventeen bow pearls divider sparkle sky
Assets -> public/themes/art/sweet-seventeen/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *
from scipy.ndimage import distance_transform_edt

OUT = outdir("sweet-seventeen")
PARTS = sys.argv[1:] or ["seventeen", "bow", "pearls", "divider", "sparkle", "sky"]
PINK, PINK_L, PINK_D, ROSE = "#f2a9c4", "#fbd6e3", "#c9638c", "#9e3f68"
NIGHT = "#2a1236"


def puffy(art, m, nx, base, light, dark, deep, hi="#fff3f8", ldir=(-0.6, -0.8)):
    """Inflated foil/satin balloon shading from the distance field: dark rim, soft body, glossy streak toward the light."""
    art = GP(art, m, base, mix(base, light, 0.2), seed=nx(), rough=0.8, streak=0.12)
    b = bbox(m, 4)
    y0, y1, x0, x1 = b
    mm = m[y0:y1, x0:x1] > 0.5
    d = distance_transform_edt(mm).astype(np.float32)
    d = gaussian_filter(d, 2.0)
    dn = d / (d.max() + 1e-6)
    full = np.zeros_like(m); full[y0:y1, x0:x1] = dn
    rimf = np.clip(1 - full / 0.35, 0, 1) * m
    art = tint(art, rimf ** 1.1, dark, 0.85, seed=nx())
    art = tint(art, np.clip(1 - full / 0.12, 0, 1) * m, deep, 0.6, seed=nx())
    # light-side gloss: shift the distance field toward the light
    sh = np.roll(np.roll(full, int(ldir[1] * 10), 0), int(ldir[0] * 10), 1)
    gloss = np.clip((sh - 0.45) * 2.4, 0, 1) * m
    art = tint(art, gloss, light, 0.9, seed=nx())
    spec = np.clip((np.roll(np.roll(full, int(ldir[1] * 22), 0), int(ldir[0] * 22), 1) - 0.78) * 7, 0, 1) * m
    art = tint(art, gaussian_filter(spec, 1.0), hi, 1.0, seed=nx(), streak=0.2)
    # foil crinkle: faint diagonal light bands
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]].astype(np.float32)
    band = 0.5 + 0.5 * np.sin((xx * 0.6 - yy) / 26 + fbm(m.shape[1], m.shape[0], nx(), 60, 2) * 2)
    art = tint(art, np.clip((band - 0.8) * 4, 0, 1) * m * full, hi, 0.35, seed=nx())
    # shadow side
    sd = np.roll(np.roll(full, int(-ldir[1] * 12), 0), int(-ldir[0] * 12), 1)
    art = tint(art, np.clip(full - sd, 0, 1) * 2.5 * m, deep, 0.35, seed=nx())
    return art


if "seventeen" in PARTS:
    W, H = 640, 640
    nx = Seq(50100); rng = random.Random(3)
    one = strokes(W, H, [([(196, 120), (196, 470)], 92, None), ([(196, 124), (126, 186)], 70, None)])
    seven = strokes(W, H, [([(292, 122), (500, 122)], 88, None), ([(500, 126), (352, 476)], 92, None)])
    art = blank(W, H)
    # strings with curls (behind)
    for (x, y) in [(196, 512), (352, 518)]:
        pts = [(x + 10 * math.sin(t * 1.3) + t * 4, y + t * 11) for t in range(0, 11)]
        art = G(art, strokes(W, H, [(pts, 2.6, (0.05, 0.4))]), "#f3d7e3", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    for m, sd in ((one, 0), (seven, 1)):
        sh = np.roll(np.roll(gaussian_filter(m, 12), 18, 0), 14, 1)
        art = OV(art, sh, lambda mm: col_arr(mm, "#14061c", mm * 0.45), pad=40)
        art = puffy(art, m, nx, "#ec96b7", "#ffdce8", "#b14a78", "#7e2a55", hi="#ffffff")
        # foil seam (centre pinch line) — lighter crease
        art = tint(art, inner_edge(m, 3.5) * 0.6, "#e58aac", 0.6, seed=nx())
    # painted catchlights: tapered strokes on the lit side
    hl = strokes(W, H, [(curve(p_, 30), w_, t_) for p_, w_, t_ in [([(170, 190), (168, 300), (170, 430)], 16, (0.25, 0.4)), ([(142, 166), (158, 152), (172, 140)], 10, (0.3, 0.3)),
                        ([(312, 100), (400, 98), (470, 100)], 14, (0.2, 0.5)), ([(462, 160), (420, 260), (356, 420)], 14, (0.25, 0.4))]])
    hlb = gaussian_filter(hl, 3.0) * np.clip(one + seven, 0, 1)
    art = over(art, col_arr(hlb, "#fff4f8", hlb * 0.62))
    dots_ = circles(W, H, [(180, 452, 5), (360, 452, 5), (488, 138, 4)])
    art = tint(art, gaussian_filter(dots_, 1.0), "#ffffff", 0.7, seed=nx(), streak=0.1)
    # knots
    for (x, y) in [(196, 506), (352, 512)]:
        k = shapes(W, H, [[(x - 9, y - 8), (x + 9, y - 8), (x + 5, y + 6), (x - 5, y + 6)]])
        art = GP(art, k, PINK_D, ROSE, seed=nx(), rough=0.5, pad=6)
    preview(art, "s17-seventeen", bg=NIGHT)
    save(art, f"{OUT}/seventeen.webp", max_w=440, quality=84)
    clear()

if "bow" in PARTS:
    W, H = 560, 520
    nx = Seq(50200); rng = random.Random(5)
    cx, cy = 280, 170
    loopL = shapes(W, H, [petal_pts(cx - 6, cy, 210, 92, math.pi + 0.18, n=24, cup=0.25)])
    loopR = shapes(W, H, [petal_pts(cx + 6, cy, 210, 92, -0.18, n=24, cup=-0.25)])
    tailL = shapes(W, H, [[(cx - 14, cy + 6), (cx + 10, cy + 20), (cx - 74, cy + 330), (cx - 104, cy + 300), (cx - 142, cy + 318)]], smooth=False)
    tailR = shapes(W, H, [[(cx + 14, cy + 6), (cx - 10, cy + 20), (cx + 62, cy + 312), (cx + 100, cy + 286), (cx + 130, cy + 306)]], smooth=False)
    knot = shapes(W, H, [deform(ellipse_pts(cx, cy + 4, 38, 46, 14), rng, 1, 0.03)])
    art = blank(W, H)
    for m, fld, sd in [(tailL, lambda x, y: (x * 0.9 + y * 0.35) / 22, 1), (tailR, lambda x, y: (-x * 0.9 + y * 0.3) / 22, 2),
                       (loopL, lambda x, y: np.hypot(x - cx, (y - cy) * 1.8) / 26, 3), (loopR, lambda x, y: np.hypot(x - cx, (y - cy) * 1.8) / 26 + 1, 4)]:
        art = GP(art, m, "#eea2bd", "#e892b2", seed=nx(), rough=1.0, streak=0.5)
        art = tint(art, side_light(m, 0, -12, 8), PINK_D, 0.55, seed=nx())
        art = sheen(art, m, fld, "#fff0f6", "#b8507c", amt=0.75, seed=nx(), freq=1.0)
    # inner loop holes (darker inside of the fold)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    near = np.clip(1 - np.hypot(xx - cx, (yy - cy) * 1.4) / 120, 0, 1) ** 1.5
    art = tint(art, near * np.clip(loopL + loopR, 0, 1), "#8e2f5a", 0.7, seed=nx())
    for s_ in (-1, 1):
        fold = strokes(W, H, [(curve([(cx + s_ * 30, cy - 8), (cx + s_ * 100, cy - 4), (cx + s_ * 170, cy + 10)], 20), 10, (0.2, 0.6))])
        art = tint(art, gaussian_filter(fold, 3), "#9a3a64", 0.45, seed=nx())
    art = GP(art, knot, "#e892b2", "#dd7fa3", seed=nx(), rough=0.8, streak=0.5)
    art = sheen(art, knot, lambda x, y: x / 9, "#fff0f6", "#b0476f", amt=0.7, seed=nx())
    art = tint(art, inner_edge(knot, 4), ROSE, 0.5, seed=nx())
    preview(art, "s17-bow", bg=NIGHT)
    save(art, f"{OUT}/bow.webp", max_w=300, quality=82)
    clear()

if "pearls" in PARTS:
    # two-strand swag across the top of the cover
    W, H = 820, 300
    art = blank(W, H)
    rng = random.Random(7)
    for (sag, r, y0, sd) in [(150, 10.5, 18, 1), (215, 8.0, 10, 2)]:
        pts = [(x, y0 + sag * (1 - ((x - W / 2) / (W / 2)) ** 2)) for x in range(-10, W + 11, 4)]
        k = 0
        for (x, y, a) in along(pts, r * 2.08):
            art = pearl(art, x, y, r * rng.uniform(0.93, 1.05), seed=sd * 1000 + k)
            k += 1
    # drop pearl at the centre
    art = pearl(art, W / 2, 196, 17, seed=99)
    preview(art, "s17-pearls", bg=NIGHT)
    save_full(art, f"{OUT}/pearls.webp", size=(410, 150), quality=84)
    clear()

if "divider" in PARTS:
    W, H = 440, 90
    nx = Seq(50300)
    art = blank(W, H)
    pts = [(x, 40 + 14 * math.sin((x - 20) / 400 * math.pi)) for x in range(20, 421, 3)]
    k = 0
    for (x, y, a) in along(pts, 13.5):
        if abs(x - 220) > 30:
            art = pearl(art, x, y, 6.2, seed=500 + k)
        k += 1
    # tiny bow centre
    cx, cy = 220, 52
    for s_ in (-1, 1):
        lp = shapes(W, H, [petal_pts(cx, cy, 34, 15, (math.pi if s_ < 0 else 0) + s_ * 0.2, n=16)])
        art = GP(art, lp, "#eea2bd", seed=nx(), rough=0.6, pad=6)
        art = sheen(art, lp, lambda x, y: np.hypot(x - cx, y - cy) / 5, "#fff0f6", "#b8507c", amt=0.6, seed=nx())
    art = GP(art, circles(W, H, [(cx, cy, 8)]), "#e07fa3", seed=nx(), rough=0.4, pad=6)
    preview(art, "s17-divider", bg="#fbeef3")
    save(art, f"{OUT}/divider.webp", max_w=220, quality=84)
    clear()

if "sparkle" in PARTS:
    W, H = 780, 780
    rng = random.Random(11)
    art = blank(W, H)
    for _ in range(7):
        art = spark(art, rng.uniform(30, W - 30), rng.uniform(30, H - 30), rng.uniform(9, 20), "#fff6fa", amt=rng.uniform(0.7, 0.95), rot=rng.uniform(-0.2, 0.2), glow_col="#f7b6cf")
    dots_ = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.2, 3.0)) for _ in range(70)])
    art = OV(art, dots_, lambda mm: col_arr(mm, "#ffe9f2", mm * 0.75), pad=4)
    save_full(art, f"{OUT}/sparkle.webp", size=(390, 390), quality=80)
    preview(art, "s17-sparkle", bg=NIGHT)
    clear()

if "sky" in PARTS:
    W, H = 600, 1000
    art = painted_sky(W, H, [(0, "#1a0b26"), (0.45, "#2e1240"), (0.8, "#4a1c4f"), (1, "#6a2a5c")], seed=13, streak=0.8, grain=0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip(1 - np.sqrt(((xx - W * 0.5) / (W * 0.6)) ** 2 + ((yy - H * 0.42) / (H * 0.3)) ** 2), 0, 1) ** 1.5
    art = over(art, col_arr(g, "#c25a8c", g * 0.22))
    save_rgb(art, f"{OUT}/sky.webp", size=(390, 650), quality=74)
