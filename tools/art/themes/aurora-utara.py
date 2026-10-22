"""Aurora Utara — northern lights over a frozen lake: painted night sky with stars, green-violet aurora curtains with
vertical rays (separate layer, animated with screen blend), snowy ridges, snow-laden pine forest, frozen lake with
the aurora's reflection, snow banks. Gouache-on-dark with soft wet glazes.
Run: python3 -I aurora-utara.py [part ...]   parts: langit aurora hutan pinus"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g5_lib import *

OUT = outdir("aurora-utara")
PARTS = sys.argv[1:] or ["langit", "aurora", "hutan", "pinus"]
NIGHT = "#0b1626"
PINE, PINE_D = "#13283a", "#0a1824"
SNOW, SNOW_S = "#eef4f8", "#b9cbd9"


def snow_caps(m, depth=3, grow=1.2):
    """Upper edges of a silhouette mask (where snow settles)."""
    sh = np.roll(m, depth, 0)
    top = np.clip(m - sh, 0, 1)
    return np.clip(gaussian_filter(top, grow) * 2.2, 0, 1) * m


def snowy_pines(art, W, H, items, nx, body=(PINE, PINE_D), snow=(SNOW, SNOW_S), dens=0.95, snow_amt=1.0, seed=1):
    m = shapes(W, H, items, smooth=False)
    art = GP(art, m, body[0], body[1], seed=nx(), rough=1.4, streak=0.6, density=dens)
    cap = snow_caps(m, 4, 1.4) * snow_amt
    # broken snow: dabs, not a line
    brk = fbm(W, H, seed + 3, 6, 2)
    cap = cap * np.clip((brk - 0.25) * 2.2, 0, 1)
    art = GP(art, np.clip(cap * 1.6, 0, 1), snow[0], snow[1], seed=nx(), rough=1.0, streak=0.3, density=0.92)
    return art, m


if "langit" in PARTS:
    W, H = 780, 1500
    rng = random.Random(61); nx = Seq(61000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#070d1a"), (0.35, "#0b1830"), (0.62, "#10284a"), (0.8, "#173a55"), (1, "#1d4a5c")], seed=61, streak=1.0, grain=0.8)
    # faint milky band (wet wash) diagonally
    band = np.clip(1 - np.abs((yy - 0.55 * xx) - 300) / 220, 0, 1) ** 2 * np.clip(1 - yy / 1000, 0, 1)
    art = G(art, band * fbm(W, H, 5, 60, 4), "#3a4f78", "#4a4a7a", seed=nx(), density=0.35, edge=0.05, bloom=0.6, rough=10, feather=8)
    # stars: many tiny, some bigger with soft glow (painted dots, uneven)
    small = star_field(W, H, 900, rng, ymax=1150, rmin=0.5, rmax=1.3)
    big_pts = [(rng.uniform(0, W), rng.uniform(0, 900), rng.uniform(1.6, 2.6)) for _ in range(40)]
    big = circles(W, H, big_pts)
    art = over(art, rgba("#f4f1e4", np.clip(small * (0.45 + 0.55 * fbm(W, H, 8, 30, 2)), 0, 1)))
    art = over(art, glow(big, "#cfe0ff", radius=4, strength=0.35))
    art = over(art, rgba("#fffbea", big))
    art[..., 3] = 1
    preview(art, "au-langit", bg="#000000")
    save_rgb(art, f"{OUT}/langit.webp", size=(520, 1000), quality=72)
    clear()

if "aurora" in PARTS:
    W, H = 900, 900
    rng = random.Random(62); nx = Seq(62000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    acc = np.zeros((H, W, 3), np.float32); A = np.zeros((H, W), np.float32)
    # each ribbon: lower edge path through control points (a long folded S), rays rising from it
    ribbons = [
        ([(-40, 700), (160, 610), (330, 650), (520, 520), (700, 470), (960, 360)], 210, 1.0, "#5ff2a6", "#8a63d8"),
        ([(-40, 430), (180, 380), (380, 420), (560, 330), (760, 300), (960, 230)], 150, 0.62, "#58e0a2", "#b27be6"),
        ([(120, 800), (300, 760), (460, 790), (640, 690), (960, 640)], 120, 0.45, "#86f2c8", "#7a8fe6"),
    ]
    for k, (ctrl, hh, st, cb, ct) in enumerate(ribbons):
        pts = curve(ctrl, 200)
        px = np.array([p[0] for p in pts]); py = np.array([p[1] for p in pts])
        order = np.argsort(px)
        cy = np.interp(np.arange(W), px[order], py[order]).astype(np.float32)
        cy = cy + (gaussian_filter(np.random.default_rng(70 + k).random(W).astype(np.float32), 18) - 0.5) * 60
        d = cy[None, :] - yy
        body = np.where(d >= 0, np.exp(-d / hh) * np.clip(1 - d / (hh * 2.6), 0, 1), np.clip(1 + d / 8, 0, 1))
        rays = gaussian_filter(np.random.default_rng(80 + k).random((H, W)).astype(np.float32), (90, 3.5))
        rays = (rays - rays.min()) / (rays.max() - rays.min())
        rays = np.clip((rays - 0.25) * 1.9, 0, 1)
        along = gaussian_filter(np.random.default_rng(90 + k).random(W).astype(np.float32), 40)
        along = (along - along.min()) / (along.max() - along.min())
        inten = body * (0.3 + 0.7 * rays) * (0.35 + 0.65 * along[None, :]) * st
        rim = np.clip(1 - np.abs(d - 4) / 14, 0, 1) * (0.5 + 0.5 * rays) * (0.4 + 0.6 * along[None, :]) * st
        mixc = np.clip(d / (hh * 1.0), 0, 1)[..., None] ** 0.8
        col = np.array(hex_rgb(cb), np.float32) * (1 - mixc) + np.array(hex_rgb(ct), np.float32) * mixc
        acc += col * inten[..., None] + np.array(hex_rgb("#d6ffe8"), np.float32) * rim[..., None] * 0.6
        A = A + (1 - A) * np.clip(inten + rim * 0.6, 0, 1)
    A = gaussian_filter(A, 1.0) * np.clip(yy / 160, 0, 1) * np.clip((H - yy) / 60, 0, 1)
    A *= 0.88 + 0.12 * fbm(W, H, 7, 50, 3)
    rgb = np.clip(acc / np.maximum(gaussian_filter(A, 1.0)[..., None], 1e-3) * 0.9, 0, 1)
    art = np.concatenate([rgb, np.clip(A * 0.95, 0, 1)[..., None]], -1)
    preview(art, "au-aurora", bg="#0b1830")
    save_full(art, f"{OUT}/aurora.webp", size=(560, 560), quality=74)
    clear()

if "hutan" in PARTS:
    W, H = 780, 760
    rng = random.Random(63); nx = Seq(63000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    LAKE = 470
    # far snowy ridges (blue-grey, white upper slopes)
    r1 = ridge_mask(W, H, 300, 110, 31, freq=2.2, sharp=0.75, bottom=LAKE)
    art = GP(art, r1, "#2b4560", "#223a52", seed=nx(), rough=2.0, streak=0.8, density=0.98)
    gul = gaussian_filter(np.random.default_rng(33).random((H, W)).astype(np.float32), (14, 2.5)); gul = (gul - gul.min()) / (gul.max() - gul.min())
    snow1 = r1 * np.clip((380 - yy) / 130, 0, 1) * np.clip((gul - 0.35) * 3.0 + np.clip((300 - yy) / 60, 0, 1), 0, 1)
    art = GP(art, snow1, "#c9d8e6", "#9fb4c9", seed=nx(), rough=2.0, streak=0.8, density=0.85)
    art = G(art, r1 * np.clip((yy - 330) / 140, 0, 1), "#16273a", seed=nx(), density=0.5, edge=0.1, bloom=0.4, rough=5, feather=4)
    # aurora light on the snow slopes (green tint)
    art = G(art, snow1 * np.clip(1 - np.abs(xx - 420) / 380, 0, 1), "#7fe3b5", seed=nx(), density=0.35, edge=0.05, bloom=0.4, rough=4, feather=3)
    # forest rows: far (small, many) and near (big) on both banks
    far = []
    for _ in range(90):
        x = rng.uniform(-10, W + 10); h = rng.uniform(40, 80)
        far += pine_polys(x, LAKE + rng.uniform(-6, 4), h, rng)
    art, fm = snowy_pines(art, W, H, far, nx, body=("#14283c", "#102234"), snow=("#cfdde9", "#a8bdd0"), dens=0.97, snow_amt=0.8, seed=5)
    near = []
    for x, h in [(10, 330), (58, 250), (104, 300), (150, 200), (190, 150), (226, 110),
                 (610, 120), (650, 190), (700, 280), (748, 330), (790, 240)]:
        near += pine_polys(x + rng.uniform(-6, 6), LAKE + 34 + rng.uniform(-6, 6), h * rng.uniform(.92, 1.08), rng, lean=rng.uniform(-.015, .015))
    # lake first (so near banks/pines overlap it): icy pale, aurora reflection, cracks
    lake = poly_fill(W, H, [[(-10, LAKE), (W + 10, LAKE), (W + 10, H), (-10, H)]])
    art2 = GP(blank(W, H), lake, "#2c4a63", "#1f3a52", seed=nx(), rough=1.0, streak=1.2)
    refl = lake * np.clip(1 - (yy - LAKE) / 220, 0, 1) * np.clip(1 - np.abs(xx - 420) / 300, 0, 1)
    art2 = G(art2, refl, "#5fd8a2", "#7aa6d8", seed=nx(), density=0.55, edge=0.05, bloom=0.5, rough=4, feather=6)
    ice = lake * np.clip((yy - LAKE - 80) / 200, 0, 1)
    art2 = G(art2, ice, "#a9c4d8", "#cfe0ec", seed=nx(), density=0.55, edge=0.2, bloom=0.5, rough=6, feather=3)
    cracks = []
    for _ in range(18):
        x0 = rng.uniform(80, 700); y0 = rng.uniform(LAKE + 40, H - 60)
        pts = [(x0, y0)]
        for _ in range(6):
            pts.append((pts[-1][0] + rng.uniform(-40, 40), pts[-1][1] + rng.uniform(-8, 12)))
        cracks.append((pts, rng.uniform(0.8, 1.6), (0.2, 0.4)))
    art2 = G(art2, strokes(W, H, cracks) * lake, "#e8f2f8", seed=nx(), density=0.5, edge=0, bloom=0.1, rough=0.8, feather=0.4)
    # horizontal light streaks on ice
    st = [([(rng.uniform(0, W), y), (rng.uniform(0, W), y + rng.uniform(-1, 1))], rng.uniform(1, 2.6), (0.3, 0.3)) for y in [rng.uniform(LAKE + 6, LAKE + 160) for _ in range(30)]]
    art2 = G(art2, strokes(W, H, st) * lake, "#c8f0dc", seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=0.6)
    art = over(art2, art)
    # near pines (dark, heavy snow)
    art, nm = snowy_pines(art, W, H, near, nx, body=("#0f2131", "#08151f"), snow=(SNOW, SNOW_S), dens=1.0, snow_amt=1.0, seed=9)
    # snow banks foreground: soft white mounds left & right, tinted blue in shade
    bank = shapes(W, H, [[(-30, H + 20), (-30, LAKE + 70), (70, LAKE + 80), (160, LAKE + 120), (220, H - 50), (250, H + 20)],
                         [(W + 30, H + 20), (W + 30, LAKE + 90), (710, LAKE + 100), (640, LAKE + 150), (600, H - 30), (580, H + 20)]])
    art = GP(art, bank, "#dfe9f1", "#c3d4e2", seed=nx(), rough=2.4, streak=0.6)
    shade = bank * np.clip((yy - LAKE - 40) / 220, 0, 1) * (0.5 + 0.5 * fbm(W, H, 44, 40, 3))
    art = G(art, shade, "#8fa8c2", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=4, feather=4)
    rimlight = snow_caps(bank, 6, 3) * 0.8
    art = G(art, rimlight, "#9df0c6", seed=nx(), density=0.4, edge=0, bloom=0.2, rough=2, feather=1.5)
    # top fade so the sky shows through above the ridges
    art[..., 3] *= np.clip((yy - 170) / 60, 0, 1)
    preview(art, "au-hutan", bg="#10284a")
    save(art, f"{OUT}/hutan.webp", max_w=620, quality=76)
    clear()

if "pinus" in PARTS:
    # divider/node: two snowy pines on a little drift, with a tiny star above
    W, H = 360, 300
    rng = random.Random(64); nx = Seq(64000)
    art = blank(W, H)
    items = pine_polys(150, 250, 220, rng) + pine_polys(222, 256, 150, rng)
    art, m = snowy_pines(art, W, H, items, nx, body=("#1b3850", "#10263a"), snow=(SNOW, "#c7d6e3"), seed=4)
    drift = poly_fill(W, H, [[(40, 262), (120, 240), (200, 244), (300, 256), (330, 272), (30, 276)]])
    art = GP(art, drift, "#e6eef5", "#c9d7e4", seed=nx(), rough=2)
    art = G(art, drift * np.clip((np.mgrid[0:H, 0:W][0] - 255) / 20, 0, 1), "#8fa8c2", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=2)
    preview(art, "au-pinus", bg="#10284a")
    save(art, f"{OUT}/pinus.webp", max_w=160, quality=86)
    clear()
