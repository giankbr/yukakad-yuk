"""Pameran Seni — opening of a (fictional) solo show "Garis Pasang Surut": a white-cube gallery wall with track spotlights,
two framed original abstract paintings, a wooden bench on polished concrete; plus the three works themselves for the
gallery section. Run: python3 -I pameran-seni.py [part ...]   parts: karya wall. Assets -> public/themes/art/pameran-seni/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m4_lib import *

OUT = outdir("pameran-seni")
PARTS = sys.argv[1:] or ["karya", "wall"]
INDIGO, INDIGO_D, SAND, RUST, BONE, CHAR, TEAL = "#233a5e", "#16253d", "#d6b27a", "#b4532e", "#efe9dc", "#2a2a2c", "#6fa7a2"


def canvas_tex(arr, seed, amt=0.022):
    h, w = arr.shape[:2]
    out = arr.copy()
    out[..., :3] = np.clip(out[..., :3] * weave(h, w, seed, amt)[..., None], 0, 1)
    return out


def drybrush(W, H, y, x0, x1, width, rng, seed, gaps=0.45):
    """Horizontal dry-brush drag: a band of thin bristle lines that skip across the canvas tooth."""
    items = []
    for k in range(int(width / 1.6)):
        yy = y - width / 2 + k * 1.6 + rng.uniform(-0.6, 0.6)
        xa, xb = x0 + rng.uniform(0, 30), x1 - rng.uniform(0, 40)
        pts = [(x, yy + math.sin(x / 70 + k) * 1.5) for x in np.linspace(xa, xb, 30)]
        items.append((pts, rng.uniform(0.8, 1.6), (0.04, 0.15)))
    m = strokes(W, H, items)
    tooth = fbm(W, H, seed, 4, 2)
    return m * np.clip((tooth - gaps) * 4, 0, 1)


def karya1(W=560, H=700):
    """'Pasang I' — sky, sand and a deep indigo sea in heavy horizontal bands; a rust half-disc sinks into the water."""
    nx = Seq(70000)
    rng = random.Random(1)
    art = painted_sky(W, H, [(0, "#e9e0cc"), (0.4, "#e4d6bb"), (1, "#e4d6bb")], seed=nx(), streak=0.7)
    sand = shapes(W, H, [deform([(-10, 330), (W + 10, 320), (W + 10, 420), (-10, 430)], rng, 2, 0.02)], smooth=False)
    art = GP(art, sand, SAND, "#c99e62", seed=nx(), rough=3, streak=1.6)
    sun = circles(W, H, [(330, 410, 120)])
    art = GP(art, sun, RUST, "#c4643a", seed=nx(), rough=3, streak=1.4)
    sea = shapes(W, H, [deform([(-10, 410), (W + 10, 400), (W + 10, H + 10), (-10, H + 10)], rng, 2, 0.02)], smooth=False)
    art = GP(art, sea, INDIGO, "#2c4a72", seed=nx(), rough=3, streak=1.8)
    art = GP(art, shapes(W, H, [[(-10, 560), (W + 10, 548), (W + 10, H + 10), (-10, H + 10)]], smooth=False), INDIGO_D, "#1d3050", seed=nx(), rough=4, streak=1.8, density=0.85)
    for y, col, wd in ((402, "#e9dcc0", 10), (470, "#4a6890", 18), (520, "#e9dcc0", 6), (612, "#3a5a84", 24), (180, "#f3ecdc", 30), (300, "#cdb48a", 14)):
        art = OV(art, drybrush(W, H, y, -10, W + 10, wd, rng, nx()), lambda m, c=col: flat(m, c, 0.8))
    clear()
    return canvas_tex(art, nx())


def karya2(W=560, H=700):
    """'Garis Surut' — bone ground, a pale teal wash, many wavering tide lines in indigo and charcoal, one rust mark."""
    nx = Seq(71000)
    rng = random.Random(2)
    art = painted_sky(W, H, [(0, BONE), (1, "#e6dfcf")], seed=nx(), streak=0.4)
    wash = shapes(W, H, [deform(ellipse_pts(300, 300, 210, 160, 14), rng, 3, 0.1)])
    art = G(art, wash, TEAL, "#8fbab2", seed=nx(), density=0.55, edge=0.6, bloom=0.5, rough=10, feather=3)
    items = []
    for k in range(26):
        y = 120 + k * 19 + rng.uniform(-4, 4)
        x0, x1 = rng.uniform(20, 140), rng.uniform(400, 540)
        ph = rng.uniform(0, 6)
        wl, amp = rng.uniform(90, 150), rng.uniform(2, 5)
        pts = [(x, y + math.sin(x / wl * math.tau + ph) * amp + (x - 280) ** 2 * 0.00025 * (k % 3)) for x in np.linspace(x0, x1, 120)]
        items.append((pts, rng.uniform(1.4, 3.8), (0.15, 0.35)))
    lm = strokes(W, H, items)
    art = G(art, lm, INDIGO, CHAR, seed=nx(), density=0.88, edge=0.5, bloom=0.1, rough=0.6, feather=0.7)
    mark = strokes(W, H, [(curve([(360, 560), (400, 552), (452, 566)], 12), 12, (0.2, 0.4))])
    art = GP(art, mark, RUST, seed=nx(), rough=2, streak=1.4)
    clear()
    return canvas_tex(art, nx())


def karya3(W=560, H=700):
    """'Karang' — charcoal ground, stacked coral and ochre forms in granular wash, white spatter."""
    nx = Seq(72000)
    rng = random.Random(3)
    art = painted_sky(W, H, [(0, "#2e2d30"), (1, "#232226")], seed=nx(), streak=0.6)
    for k, (cx, cy, rx, ry, c1, c2) in enumerate(((280, 560, 230, 110, "#c97a5e", "#b0603e"), (250, 420, 170, 90, "#d6b27a", "#c49a5a"),
                                                  (310, 300, 150, 80, "#e0a08a", "#c97a5e"), (260, 190, 100, 64, BONE, "#d9cfbf"))):
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 14), random.Random(k + 9), 3, 0.12)])
        art = GP(art, m, c1, c2, seed=nx(), rough=5, streak=1.4)
        art = G(art, m * (np.mgrid[0:H, 0:W][0] > cy).astype(np.float32), "#5a3a30", seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=5)
        strata = strokes(W, H, [(curve([(cx - rx, cy - ry * 0.5 + j * ry * 0.3), (cx, cy - ry * 0.45 + j * ry * 0.3 + rng.uniform(-6, 6)), (cx + rx, cy - ry * 0.5 + j * ry * 0.3)], 20), rng.uniform(1.5, 3), (0.2, 0.2)) for j in range(4)])
        art = G(art, strata * m, "#6a4232", seed=nx(), density=0.45, edge=0.3, bloom=0, rough=2)
        clear()
    sp = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), rng.choice([0.7, 1.0, 1.4])) for _ in range(50)])
    art = soft(art, sp, "#f4efe4", alpha=0.6, pad=4)
    return canvas_tex(art, nx())


def framed(art, pic, x, y, w, h, frame, frame_w, seed):
    """Place a painting (RGBA array) with a float frame and a soft cast shadow (light from above)."""
    H, W = art.shape[:2]
    im = to_image(pic).convert("RGB").resize((w, h), Image.LANCZOS)
    p = np.asarray(im, np.float32) / 255
    box = shapes(W, H, [[(x - frame_w, y - frame_w), (x + w + frame_w, y - frame_w), (x + w + frame_w, y + h + frame_w), (x - frame_w, y + h + frame_w)]], smooth=False)
    art = over(art, soft_shadow(box, "#5a5045", blur=10, strength=0.45, dx=4, dy=16))
    art = GP(art, box, frame, mix(frame, "#000000", 0.15), seed=seed, rough=0.3, streak=1.2)
    gap = shapes(W, H, [[(x - 3, y - 3), (x + w + 3, y - 3), (x + w + 3, y + h + 3), (x - 3, y + h + 3)]], smooth=False)
    art = soft(art, gap, "#1e1c1a", alpha=0.9, pad=2)
    out = art.copy()
    out[y:y + h, x:x + w, :3] = p
    out[y:y + h, x:x + w, 3] = 1
    # top edge of the canvas catches the light, the bottom is in shadow
    out[y:y + 3, x:x + w, :3] = np.clip(out[y:y + 3, x:x + w, :3] * 1.12, 0, 1)
    out[y + h - 4:y + h, x:x + w, :3] *= 0.8
    return out


if "karya" in PARTS:
    for name, fn in (("karya-1", karya1), ("karya-2", karya2), ("karya-3", karya3)):
        a = fn()
        prev(a, f"ps-{name}")
        save_rgb(a, f"{OUT}/{name}.webp", size=(480, 600), quality=80)
        np.save(f"{MPREV}/{name}.npy", a)

if "wall" in PARTS:
    W, H = 720, 1300
    nx = Seq(73000)
    rng = random.Random(4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    FLOOR = 1040
    art = painted_sky(W, H, [(0, "#e4e0d9"), (0.06, "#f3f0ea"), (0.5, "#f1eee8"), (1, "#e9e5dd")], seed=nx(), streak=0.25, grain=0.3)
    fl = np.clip((yy - FLOOR) / (H - FLOOR), 0, 1)
    floor_rgb = np.array(hex_rgb("#bdb8af"), np.float32) * (1 - fl[..., None]) + np.array(hex_rgb("#a29d93"), np.float32) * fl[..., None]
    art[..., :3] = np.where((yy >= FLOOR)[..., None], floor_rgb, art[..., :3])
    art[:44, :, :3] = np.array(hex_rgb("#e0dcd5"), np.float32)
    # ceiling track + spotlight heads, warm cones of light on the wall
    art = soft(art, shapes(W, H, [[(0, 52), (W, 52), (W, 60), (0, 60)]], smooth=False), "#2b2a2a", alpha=0.9, pad=2)
    for (sx, tx, ty) in ((160, 160, 740), (470, 490, 730), (650, 640, 780)):
        cone = shapes(W, H, [[(sx - 10, 80), (sx + 10, 80), (tx + 230, ty + 260), (tx - 230, ty + 260)]], smooth=False)
        cone = gaussian_filter(cone, 30) * np.clip(1 - (yy - 80) / 900, 0, 1)
        art = soft(art, cone, "#fff6e4", alpha=0.55, blur=0, pad=0)
        art = soft(art, ellipses(W, H, [(tx, ty, 230, 290, 0)]), "#fff3dc", alpha=0.35, blur=40, pad=0)
        head = shapes(W, H, [[(sx - 11, 62), (sx + 11, 62), (sx + 16, 104), (sx - 16, 104)]], smooth=False)
        art = GP(art, strokes(W, H, [([(sx, 56), (sx, 66)], 4, None)]), "#2b2a2a", seed=nx(), rough=0.3)
        art = GP(art, head, "#2e2d2d", "#4a4848", seed=nx(), rough=0.4, streak=1.0)
        art = soft(art, ellipses(W, H, [(sx, 105, 15, 4, 0)]), "#fff3d6", alpha=0.95, blur=1.5, pad=4)
        clear()
    # the two works
    k1 = np.load(f"{MPREV}/karya-1.npy")
    k3 = np.load(f"{MPREV}/karya-3.npy")
    art = framed(art, k1, 330, 548, 336, 420, "#b08a5a", 9, nx())
    art = framed(art, k3, 70, 648, 184, 230, "#1e1d1c", 6, nx())
    # wall label beside the big work
    art = over(art, soft_shadow(shapes(W, H, [[(682, 928), (706, 928), (706, 944), (682, 944)]], smooth=False), "#5a5045", 2, 0.3, 1, 2))
    art = soft(art, shapes(W, H, [[(682, 928), (706, 928), (706, 944), (682, 944)]], smooth=False), "#fbfaf7", alpha=1, pad=2)
    art = soft(art, lines(W, H, [([(685, 933), (701, 933)], 1.2), ([(685, 938), (697, 938)], 1.0)]), "#8a857c", alpha=0.9, pad=2)
    # skirting shadow and floor reflections
    art = soft(art, shapes(W, H, [[(0, FLOOR - 4), (W, FLOOR - 4), (W, FLOOR + 6), (0, FLOOR + 6)]], smooth=False), "#6e6a63", alpha=0.6, blur=2, pad=4)
    refl = shapes(W, H, [[(330, FLOOR + 10), (666, FLOOR + 10), (666, FLOOR + 170), (330, FLOOR + 170)], [(70, FLOOR + 10), (254, FLOOR + 10), (254, FLOOR + 100), (70, FLOOR + 100)]], smooth=False)
    art = soft(art, gaussian_filter(refl, 12) * np.clip(1 - (yy - FLOOR) / 180, 0, 1), "#7a6a5a", alpha=0.25, pad=0)
    for lx in (150, 480, 620):
        art = soft(art, ellipses(W, H, [(lx, FLOOR + 40, 150, 30, 0)]) * (yy > FLOOR + 6), "#ece6da", alpha=0.35, blur=18, pad=0)
    con = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (1.0, 6.0))
    con = (con - con.mean()) / (con.std() + 1e-6)
    art[..., :3] = np.where((yy > FLOOR + 6)[..., None], np.clip(art[..., :3] * (1 + 0.012 * con[..., None]), 0, 1), art[..., :3])
    # oak bench on the floor
    bx0, bx1, by = 220, 560, 1082
    seat = shapes(W, H, [[(bx0, by), (bx1, by), (bx1 + 6, by + 22), (bx0 - 6, by + 22)]], smooth=False)
    legs = shapes(W, H, [[(bx0 + 20, by + 22), (bx0 + 50, by + 22), (bx0 + 50, by + 92), (bx0 + 20, by + 92)], [(bx1 - 50, by + 22), (bx1 - 20, by + 22), (bx1 - 20, by + 92), (bx1 - 50, by + 92)]], smooth=False)
    art = soft(art, ellipses(W, H, [((bx0 + bx1) / 2, by + 96, 200, 16, 0)]), "#3e3a34", alpha=0.45, blur=8, pad=0)
    art = GP(art, legs, "#8a6a46", "#6e5236", seed=nx(), rough=0.4, streak=1.6)
    art = GP(art, seat, "#b48a5c", "#9a7448", seed=nx(), rough=0.4, streak=2.0)
    art = soft(art, shapes(W, H, [[(bx0, by), (bx1, by), (bx1, by + 4), (bx0, by + 4)]], smooth=False), "#e0c49a", alpha=0.8, pad=2)
    grainw = lines(W, H, [([(bx0 + rng.uniform(0, 30), by + 8 + k * 3), (bx1 - rng.uniform(0, 30), by + 8 + k * 3 + rng.uniform(-1, 1))], 0.7) for k in range(5)])
    art = soft(art, grainw * seat, "#6e5236", alpha=0.4, pad=2)
    art = add_grain(art, 7, 0.02)
    clear()
    prev(art, "ps-wall", None)
    save_rgb(art, f"{OUT}/wall.webp", size=(600, 1083), quality=78)
