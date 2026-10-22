"""Chefchaouen Biru — a blue-washed medina alley climbing in steps, painted in gouache + watercolour: layered lime-wash
coats (cobalt over older sky-blue, chalky where worn), a deep-blue arched door with studs, white-washed step edges,
potted geraniums hung on the walls, afternoon light on one wall. No figures, no calligraphy.
Run: python3 -I chefchaouen-biru.py [part ...]   parts: lorong kapur pintu pot divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f3_lib import *

OUT = outdir("chefchaouen-biru")
PARTS = sys.argv[1:] or ["lorong", "kapur", "pintu", "pot", "divider"]
COB, COB_D, SKY, PALE, WHITE = "#3f74c4", "#24508f", "#7fb0e0", "#c4dcf2", "#eef3f6"
TERRA = "#c86a3e"


def wash_fill(W, H, mask, base, deep, pale, seed, light=None, wrap=False):
    tex = limewash(W, H, base, deep, pale, seed=seed, wrap=wrap)
    tex[..., 3] = np.clip((gaussian_filter(displace(mask, seed, 1.2, 14), 0.7) - 0.3) * 2.4, 0, 1)
    if light is not None:
        tex[..., :3] = np.clip(tex[..., :3] * (1 + light[..., None]), 0, 1)
    return tex


def geranium(art, W, H, x, y, s, rng, nx, pot_col="#e8b33a", flower=("#ec4a3c", "#c42c2a"), hang=True):
    """A painted pot (hung on a nail or standing) with round scalloped geranium leaves and red flower umbels."""
    # pot
    pw, ph = s * 0.55, s * 0.42
    pot = shapes(W, H, [[(x - pw / 2, y), (x + pw / 2, y), (x + pw * 0.36, y + ph), (x - pw * 0.36, y + ph)]], smooth=False)
    rim = rect(W, H, x - pw / 2 - 3, y - 4, x + pw / 2 + 3, y + 7)
    pm = np.clip(pot + rim, 0, 1)
    art = over(art, soft_shadow(pm, "#0e2448", blur=4, strength=0.4, dx=5, dy=6))
    art = GP(art, pm, pot_col, mix(pot_col, "#000000", 0.25), seed=nx(), rough=0.5, streak=0.8)
    art = over(art, shade_lr(pm, W, "#1a1208", 0.35, side=1, width=0.45))
    art = over(art, flat(rim * light_mask(H, W, x - pw * 0.3, y, pw * 0.6), "#ffffff", 0.35))
    if hang:
        art = over(art, flat(strokes(W, H, [([(x - pw * 0.3, y), (x, y - s * 0.32), (x + pw * 0.3, y)], 1.2, None)]), "#2a2a2a", 0.6))
    # leaves: round, scalloped, with a darker horseshoe zone
    leaves = []
    for k in range(rng.randint(9, 13)):
        a = rng.uniform(-math.pi, 0) if rng.random() < 0.8 else rng.uniform(0, 0.6) * rng.choice((-1, 1))
        d = s * rng.uniform(0.12, 0.42)
        lx, ly = x + math.cos(a) * d * 1.1, y - 2 + math.sin(a) * d * 0.7
        r = s * rng.uniform(0.09, 0.14)
        pts = []
        for i in range(16):
            t = i / 16 * math.tau
            rr = r * (1 + 0.08 * math.sin(t * 7))
            pts.append((lx + math.cos(t) * rr, ly + math.sin(t) * rr * 0.85))
        leaves.append((pts, lx, ly, r))
    lm = shapes(W, H, [p for p, *_ in leaves])
    art = G(art, lm, "#7aa84a", "#4c7f32", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=1.0, feather=0.8)
    zone = shapes(W, H, [ellipse_pts(lx, ly + r * 0.1, r * 0.55, r * 0.45, 12) for _, lx, ly, r in leaves]) - shapes(W, H, [ellipse_pts(lx, ly + r * 0.1, r * 0.3, r * 0.24, 12) for _, lx, ly, r in leaves])
    art = G(art, np.clip(zone, 0, 1) * lm, "#3e5f26", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=0.8, feather=1.2)
    # flower umbels on stalks
    for k in range(rng.randint(2, 4)):
        fx, fy = x + rng.uniform(-s * 0.35, s * 0.35), y - s * rng.uniform(0.38, 0.62)
        art = G(art, strokes(W, H, [([(x + rng.uniform(-6, 6), y - s * 0.1), (fx, fy)], 1.6, (0.0, 0.3))]), "#5c8a3a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5, feather=0.5)
        dots = []
        for j in range(rng.randint(9, 14)):
            a = rng.uniform(0, math.tau); d = s * 0.11 * math.sqrt(rng.random())
            dots.append((fx + math.cos(a) * d, fy + math.sin(a) * d * 0.8, s * rng.uniform(0.028, 0.042)))
        dm = circles(W, H, dots)
        art = GP(art, dm, flower[0], flower[1], seed=nx(), rough=1.0, streak=0.6)
        hi = circles(W, H, [(dx - r * 0.3, dy - r * 0.3, r * 0.45) for dx, dy, r in dots]) * dm
        art = over(art, flat(hi, "#ff8a7a", 0.45))
    return art


if "kapur" in PARTS:
    t = limewash(360, 360, "#5b8fd2", "#3a6cb8", "#b8d4f0", seed=901, wrap=True)
    Image.fromarray((t[..., :3] * 255).astype(np.uint8)).save(f"{PREV}/kapur.png")
    save_rgb(t, f"{OUT}/kapur.webp", quality=74)
    t2 = limewash(360, 360, "#e9f0f6", "#c7d9ec", "#ffffff", seed=903, wrap=True)
    save_rgb(t2, f"{OUT}/kapur-putih.webp", quality=72)

if "lorong" in PARTS:
    W, H = 640, 900
    nx = Seq(9100); rng = random.Random(91)
    # far end of the alley (where it turns), and the step geometry
    fx0, fx1, fy0, fy1 = 236, 404, 150, 452
    art = painted_sky(W, H, [(0, "#a9cdee"), (0.12, "#d6e6f2"), (0.2, "#f7ead2"), (1, "#eac9a0")], seed=nx())
    # far wall with a white arched passage
    far = rect(W, H, fx0 - 2, fy0 - 40, fx1 + 2, fy1 + 2)
    art = over(art, wash_fill(W, H, far, SKY, COB, PALE, nx()))
    arch_pts = [(282, fy1)] + [(320 + math.cos(a) * 38, 360 + math.sin(a) * 38) for a in np.linspace(math.pi, 2 * math.pi, 16)] + [(358, fy1)]
    arch = shapes(W, H, [arch_pts], smooth=False)
    art = GP(art, arch, "#f1f4f6", "#d4e2ee", seed=nx(), rough=0.6)
    inner = shapes(W, H, [[(292, fy1)] + [(320 + math.cos(a) * 28, 362 + math.sin(a) * 28) for a in np.linspace(math.pi, 2 * math.pi, 14)] + [(348, fy1)]], smooth=False)
    art = GP(art, inner, "#2a4f86", "#1c3866", seed=nx(), rough=0.4)
    art = over(art, flat(inner * light_mask(H, W, 330, 420, 40), "#f6d9a8", 0.5))
    # left wall (sunlit high, shade low) and right wall (shade)
    lw = shapes(W, H, [[(0, 0), (fx0, fy0 - 40), (fx0, fy1), (0, H)]], smooth=False)
    rw = shapes(W, H, [[(W, 0), (fx1, fy0 - 40), (fx1, fy1), (W, H)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun = np.clip(1 - (yy - (0.05 * H + xx * 1.1)) / 300, 0, 1) * 0.5  # diagonal light band
    art = over(art, wash_fill(W, H, lw, "#5d93d6", COB, PALE, nx(), light=sun * lw))
    art = over(art, wash_fill(W, H, rw, "#4a7dc6", COB_D, SKY, nx(), light=-0.12 * rw))
    # broken skyline: parapets, a small whitewashed upper storey and wall-top lime build-up
    pl = [(0, 40), (60, 58), (60, 46), (120, 74), (150, 80), (150, 64), (236, 100), (236, 112), (0, 12)]
    pr = [(W, 30), (560, 52), (560, 34), (470, 60), (470, 76), (404, 100), (404, 112), (W, 6)]
    for pts, base in ((pl, "#6a9ddc"), (pr, "#4a7dc6")):
        m = shapes(W, H, [pts], smooth=False)
        art = over(art, wash_fill(W, H, m, base, COB, PALE, nx()))
    edge = strokes(W, H, [([(0, 40), (60, 58), (60, 46), (120, 74), (150, 80), (150, 64), (236, 100)], 3.0, None), ([(W, 30), (560, 52), (560, 34), (470, 60), (470, 76), (404, 100)], 3.0, None)])
    art = GP(art, edge, "#f2f6f9", "#d7e5f0", seed=nx(), rough=0.8, dry=0.2)
    clouds = np.clip(cloud_mask(W, H, 330, 40, 160, 46, rng) + cloud_mask(W, H, 470, 14, 120, 30, rng), 0, 1)
    art = G(art, clouds * (yy < 100), "#ffffff", "#f3f6f8", seed=nx(), density=0.6, edge=0.1, bloom=0.4, rough=6)
    # darker dado band near the ground on both walls (repainted more often)
    dado_l = shapes(W, H, [[(0, H - 230), (fx0, fy1 - 46), (fx0, fy1), (0, H)]], smooth=False)
    dado_r = shapes(W, H, [[(W, H - 230), (fx1, fy1 - 46), (fx1, fy1), (W, H)]], smooth=False)
    art = G(art, np.clip(dado_l + dado_r, 0, 1), "#2c5aa8", "#1e4589", seed=nx(), density=0.65, edge=0.3, bloom=0.3, rough=3)
    clear()
    # corner shading where walls meet the far wall
    for xc in (fx0, fx1):
        art = over(art, flat(gaussian_filter(rect(W, H, xc - 3, fy0 - 40, xc + 3, fy1), 6) * 1.0, "#0e2448", 0.35))
    # stairs: treads (pale, white-washed nosing) and risers (blue) in perspective
    N = 11
    for i in range(N):
        t0 = (i / N) ** 1.35; t1 = ((i + 1) / N) ** 1.35
        ya = H - (H - fy1) * t0; yb = H - (H - fy1) * t1
        xa0 = 0 + fx0 * t0; xa1 = W - (W - fx1) * t0
        xb0 = 0 + fx0 * t1; xb1 = W - (W - fx1) * t1
        rise = (ya - yb) * 0.55
        riser = shapes(W, H, [[(xa0, ya), (xa1, ya), (xa1 - 2, ya - rise), (xa0 + 2, ya - rise)]], smooth=False)
        tread = shapes(W, H, [[(xa0 + 2, ya - rise), (xa1 - 2, ya - rise), (xb1, yb), (xb0, yb)]], smooth=False)
        art = over(art, wash_fill(W, H, riser, "#3a6cb8", COB_D, SKY, nx()))
        art = over(art, wash_fill(W, H, tread, "#a9c9ea", "#7fa8d8", "#e8f0f8", nx()))
        nose = shapes(W, H, [[(xa0 + 2, ya - rise - 1), (xa1 - 2, ya - rise - 1), (xa1 - 2, ya - rise + max(2, rise * 0.22)), (xa0 + 2, ya - rise + max(2, rise * 0.22))]], smooth=False)
        art = GP(art, nose, WHITE, "#d6e4f0", seed=nx(), rough=0.8, dry=0.15)
        if i % 3 == 0:
            clear()
    # shadow of the right wall falling across the lower steps (afternoon)
    shadow = shapes(W, H, [[(W, H), (W, 560), (fx1 + 40, fy1 + 20), (380, H)]], smooth=False)
    art = G(art, shadow, "#1f3f80", "#2a4f96", seed=nx(), density=0.38, edge=0.15, bloom=0.2, rough=4)
    # arched door on the right wall (in perspective: narrower, taller near)
    dx0, dx1 = 488, 560
    def wy(x, y_near):  # wall line height scaled by perspective
        k = (W - x) / (W - fx1)
        return y_near
    def door_poly(x0, x1, ya0, ya1, yb0, yb1, bulge):
        top = [(x0 + (x1 - x0) * t, ya0 + (ya1 - ya0) * t - bulge * math.sin(math.pi * t)) for t in np.linspace(0, 1, 18)]
        return [(x0, yb0)] + top + [(x1, yb1)]
    door_pts = door_poly(dx0, dx1, 478, 440, 652, 690, 34)
    surround = shapes(W, H, [door_poly(dx0 - 12, dx1 + 12, 474, 432, 656, 694, 50)], smooth=False)
    art = GP(art, surround, "#f1f4f6", "#d0dfee", seed=nx(), rough=0.8)
    door = shapes(W, H, [door_pts], smooth=False)
    art = GP(art, door, "#1f4fa0", "#163a7c", seed=nx(), rough=0.5, streak=1.0)
    planks = door * hatch(W, H, 1.5708, 12, 0.1, nx(), 0.5)
    art = over(art, flat(planks, "#0e2a5c", 0.5))
    studs = circles(W, H, [(x_, y_ + (x_ - dx0) * -0.4, 2.4) for y_ in range(480, 660, 26) for x_ in (dx0 + 12, dx1 - 10)]) * door
    art = over(art, flat(studs, "#e3c27a", 0.9))
    art = over(art, flat(circles(W, H, [(dx0 + 20, 560, 5)]), "#d8b56a", 0.95))
    art = over(art, flat(gaussian_filter(np.clip(door - np.roll(door, 6, 1), 0, 1), 2), "#081a3c", 0.5))
    # step at the door threshold
    art = GP(art, shapes(W, H, [[(dx0 - 14, 690), (dx1 + 14, 690), (dx1 + 14, 702), (dx0 - 14, 706)]], smooth=False), WHITE, "#cddcea", seed=nx(), rough=0.6)
    clear()
    # potted geraniums on the sunlit left wall, a row stepping up with the stairs
    for (px, py, ps, pc, fl) in ((60, 300, 92, "#e8b33a", ("#ec4a3c", "#c42c2a")), (140, 236, 74, "#3fa38f", ("#e8506a", "#b52446")),
                                 (52, 470, 104, "#f0f0ea", ("#ec4a3c", "#c42c2a")), (190, 190, 54, "#e07a3a", ("#ec4a3c", "#c42c2a")),
                                 (126, 372, 70, "#2f4f9a", ("#f07a8a", "#c2405a"))):
        art = geranium(art, W, H, px, py, ps, rng, nx, pot_col=pc, flower=fl)
        clear()
    # a big standing pot on a step, lower right, and one by the door
    art = geranium(art, W, H, 590, 760, 120, rng, nx, pot_col="#e8b33a", hang=False)
    art = geranium(art, W, H, 455, 668, 66, rng, nx, pot_col="#f0f0ea", flower=("#e8506a", "#b52446"), hang=False)
    clear()
    # warm light glaze from the top-left + gentle vignette
    art = over(art, flat(light_mask(H, W, 80, 40, 520), "#ffe7b8", 0.22))
    art = vignette(art, 0.28, 2.0)
    art = add_grain(art, nx(), 0.03)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/lorong.png")
    save_rgb(art, f"{OUT}/lorong.webp", quality=74)

if "pintu" in PARTS:
    W, H = 440, 600
    nx = Seq(9300); rng = random.Random(93)
    art = blank(W, H)
    cx = W / 2
    def arch(w, top, bottom):
        r = w / 2
        return [(cx - r, bottom)] + [(cx + math.cos(a) * r, top + r + math.sin(a) * r * 1.08) for a in np.linspace(math.pi, 2 * math.pi, 28)] + [(cx + r, bottom)]
    outer = shapes(W, H, [arch(420, 6, H - 4)], smooth=False)
    band = shapes(W, H, [arch(380, 26, H - 4)], smooth=False)
    hole = shapes(W, H, [arch(320, 56, H - 4)], smooth=False)
    art = over(art, wash_fill(W, H, outer, "#e9f0f6", "#c7d9ec", "#ffffff", nx()))
    art = over(art, wash_fill(W, H, np.clip(band - hole, 0, 1), "#2c5aa8", "#1e4589", "#5d93d6", nx()))
    # inner reveal: a thin pale edge
    rev = np.clip(shapes(W, H, [arch(336, 48, H - 4)], smooth=False) - hole, 0, 1)
    art = over(art, flat(rev, "#9fc0e6", 0.9))
    # small painted dots along the band (folk detail)
    dots = []
    for a in np.linspace(math.pi * 1.05, math.pi * 1.95, 11):
        dots.append((cx + math.cos(a) * 175, 26 + 190 + math.sin(a) * 175 * 1.08 + 12, 4))
    art = GP(art, circles(W, H, dots), "#f4f7fa", "#dbe6f0", seed=nx(), rough=0.4)
    art[..., 3] *= 1 - np.clip(hole * 1.2, 0, 1)
    art = over(art, flat(np.clip(gaussian_filter(hole, 8) - hole, 0, 1) * 2, "#0e2448", 0.4))
    prev(art, "pintu", tone="#dfe9f3")
    save(art, f"{OUT}/pintu.webp", max_w=360, quality=82)

if "pot" in PARTS:
    W, H = 240, 300
    nx = Seq(9500); rng = random.Random(95)
    art = blank(W, H)
    art = geranium(art, W, H, 120, 190, 190, rng, nx, pot_col="#e8b33a")
    prev(art, "pot", tone="#7fb0e0")
    save(art, f"{OUT}/pot.webp", max_w=150, quality=84)

if "divider" in PARTS:
    W, H = 560, 150
    nx = Seq(9700); rng = random.Random(97)
    art = blank(W, H)
    ledge = shapes(W, H, [deform([(30, 118), (530, 118), (530, 130), (30, 132)], rng, 1, 0.04)], smooth=False)
    art = GP(art, ledge, "#2c5aa8", "#1e4589", seed=nx(), rough=1.0)
    art = over(art, flat(rect(W, H, 30, 116, 530, 119), "#eef3f6", 0.9))
    for x, s_, pc, fl in ((180, 66, "#e8b33a", ("#ec4a3c", "#c42c2a")), (280, 80, "#f0f0ea", ("#e8506a", "#b52446")), (380, 64, "#3fa38f", ("#ec4a3c", "#c42c2a"))):
        art = geranium(art, W, H, x, 118 - s_ * 0.42, s_, rng, nx, pot_col=pc, flower=fl, hang=False)
    prev(art, "divider", tone="#eef3f6")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
