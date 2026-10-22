"""Film Analog — warm 35mm keepsakes in gouache: an unbranded rangefinder camera (leatherette body, satin-chrome top
plate, glass lens with a warm reflection), an unbranded film canister with its leader tongue, painted light leaks,
a red grease-pencil circle, a strip of masking tape and a film-grain tile.
Run: python3 -I film-analog.py [part ...]   parts: camera canister leak circle tape grain
Assets -> public/themes/art/film-analog/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g6_lib import *  # noqa

OUT = outdir("film-analog")
PARTS = sys.argv[1:] or ["camera", "canister", "leak", "circle", "tape", "grain", "snip"]
CHROME, CHROME2, CHROMED, CHROMEL = "#c9c4ba", "#dcd7cc", "#5a5650", "#fbf8f0"
LEA, LEA2 = "#24201d", "#2e2925"


def chrome(art, m, nx, ldir=(5, 5), amt=0.7):
    art = GP(art, m, CHROME, CHROME2, seed=nx(), rough=0.5, streak=0.8)
    art = tint(art, side_light(m, ldir[0], ldir[1], 4), CHROMED, amt, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .6, -ldir[1] * .6, 2), CHROMEL, 0.7, seed=nx())
    return art


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -math.pi / 2), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, math.pi / 2), (x0 + r, y0 + r, math.pi)):
        for k in range(n + 1):
            a = a0 + k / n * math.pi / 2
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


if "camera" in PARTS:
    W, H = 680, 460
    nx = Seq(62100); rng = random.Random(621)
    art = blank(W, H)
    sh = ellipses(W, H, [(340, 420, 300, 26, 0)])
    art = OV(art, sh, lambda mm: col_arr(mm, "#1a120c", np.clip(gaussian_filter(mm, 14), 0, 1) * 0.45), pad=40)
    # strap lugs
    for x in (66, 614):
        art = chrome(art, shapes(W, H, [rrect(x - 12, 150, x + 12, 196, 6)], smooth=False), nx)
    # top plate + dials
    top = shapes(W, H, [rrect(80, 120, 600, 200, 26)], smooth=False)
    art = chrome(art, top, nx, (0, 6))
    for cx, w_, h_ in ((180, 70, 34), (470, 62, 30)):
        d = shapes(W, H, [rrect(cx - w_ / 2, 120 - h_, cx + w_ / 2, 126, 8)], smooth=False)
        art = chrome(art, d, nx, (4, 4))
        knurl = stripes(W, H, math.pi / 2, 1.2, 4.2, seed=nx()) * d
        art = tint(art, knurl, CHROMED, 0.45, seed=nx())
    btn = shapes(W, H, [rrect(530, 96, 556, 124, 10)], smooth=False)
    art = chrome(art, btn, nx)
    # body with leatherette
    body = shapes(W, H, [rrect(70, 180, 610, 390, 30)], smooth=False)
    art = GP(art, body, LEA, LEA2, seed=nx(), rough=0.6, streak=0.4)
    pebble = fbm(W, H, nx(), 3, 2)
    art = tint(art, np.clip((pebble - 0.55) * 3, 0, 1) * body, "#4a433c", 0.5, seed=nx())
    art = tint(art, side_light(body, 0, 8, 6), "#0a0806", 0.6, seed=nx())
    art = tint(art, side_light(body, -4, -6, 3), "#6a625a", 0.45, seed=nx())
    band = shapes(W, H, [rect(70, 196, 610, 206)], smooth=False) * body
    art = chrome(art, band, nx, (0, 2), 0.4)
    # viewfinder + rangefinder windows
    for x0, x1, col in ((420, 520, "#2c3a40"), (110, 156, "#3a3020"), (176, 220, "#2c3a40")):
        wm = shapes(W, H, [rrect(x0, 132, x1, 176, 8)], smooth=False)
        art = GP(art, wm, col, mix(col, "#000000", 0.3), seed=nx(), rough=0.3)
        art = tint(art, side_light(wm, 3, 3, 3), "#000000", 0.5, seed=nx())
        art = OV(art, strokes(W, H, [([(x0 + 8, 142), (x0 + (x1 - x0) * 0.5, 138)], 3, None)]), lambda mm: col_arr(mm, "#d8f0f4", mm * 0.55), pad=4)
    # lens: mount ring, focus ring (knurled), front ring, glass
    cx, cy = 340, 290
    for r, col, kn in ((128, CHROME, False), (112, "#2a2622", True), (92, CHROME, False), (78, "#141210", False)):
        m = circles(W, H, [(cx, cy, r)])
        if col == CHROME:
            art = chrome(art, m, nx, (5, 6), 0.75)
        else:
            art = GP(art, m, col, mix(col, "#000000", 0.2), seed=nx(), rough=0.4)
            if kn:
                yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
                ang = np.arctan2(yy - cy, xx - cx)
                kn_ = (np.cos(ang * 90) > 0.3).astype(np.float32) * np.clip(m - circles(W, H, [(cx, cy, 96)]), 0, 1)
                art = tint(art, gaussian_filter(kn_, 0.5), "#6a625a", 0.6, seed=nx())
    glass = circles(W, H, [(cx, cy, 66)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / 66
    art = over(art, col_arr(glass, "#1c2430", glass * 0.98))
    art = tint(art, glass * np.clip(1 - d, 0, 1) ** 0.6, "#3a4a66", 0.6, seed=nx())
    art = tint(art, circles(W, H, [(cx + 6, cy + 4, 30)]), "#0c0e14", 0.8, seed=nx())
    refl = strokes(W, H, [(arc_pts(cx, cy, 48, math.pi * 1.05, math.pi * 1.55, 14), 9, (0.2, 0.3))])
    art = OV(art, refl, lambda mm: col_arr(mm, "#ffb46a", np.clip(gaussian_filter(mm, 2), 0, 1) * 0.75), pad=8)
    refl2 = circles(W, H, [(cx + 26, cy + 22, 7)])
    art = OV(art, refl2, lambda mm: col_arr(mm, "#c8e2ff", np.clip(gaussian_filter(mm, 2), 0, 1) * 0.7), pad=8)
    ring_hi = strokes(W, H, [(arc_pts(cx, cy, 120, math.pi * 1.1, math.pi * 1.45, 12), 3, (0.3, 0.3))])
    art = OV(art, ring_hi, lambda mm: col_arr(mm, "#ffffff", mm * 0.7), pad=4)
    art = add_grain(art, nx(), 0.03)
    preview(art, "fa-camera", bg="#f1e8d6")
    save(art, f"{OUT}/camera.webp", max_w=340, quality=84)
    clear()

if "canister" in PARTS:
    W, H = 420, 360
    nx = Seq(62200); rng = random.Random(622)
    art = blank(W, H)
    # film leader tongue with sprocket holes
    tongue = shapes(W, H, [[(236, 196), (404, 196), (404, 232), (330, 252), (236, 252)]], smooth=False)
    art = GP(art, tongue, "#3a2416", "#4a2c18", seed=nx(), rough=0.5)
    art = tint(art, side_light(tongue, 0, 5, 4), "#0c0806", 0.5, seed=nx())
    holes = shapes(W, H, [rrect(250 + k * 22, 200, 262 + k * 22, 208, 2, 3) for k in range(7)] + [rrect(250 + k * 22, 240, 262 + k * 22, 248, 2, 3) for k in range(4)], smooth=False)
    art = knockout(art, holes, 1.0, 0.5)
    art = tint(art, strokes(W, H, [([(244, 214), (330, 214)], 2, None)]) * tongue, "#c97a3a", 0.35, seed=nx())
    # body (vertical cylinder)
    x0, x1, y0, y1 = 120, 248, 70, 300
    body = shapes(W, H, [rect(x0, y0, x1, y1)], smooth=False)
    art = GP(art, body, "#2f6b6a", "#367674", seed=nx(), rough=0.5, streak=0.5)
    # painted label: two bands, no lettering
    for yb, hb, col in ((112, 60, "#efe4cc"), (184, 10, "#e07a2a"), (200, 6, "#e07a2a")):
        art = GP(art, shapes(W, H, [rect(x0, yb, x1, yb + hb)], smooth=False), col, mix(col, "#ffffff", 0.08), seed=nx(), rough=0.4)
    shd, hi = cyl_shade(body, x0, x1, -0.4)
    art = tint(art, gaussian_filter(shd, 1.5), "#0e1c1c", 0.6, seed=nx())
    art = tint(art, gaussian_filter(hi, 2), "#fff2cc", 0.5, seed=nx())
    for yc in (y0, y1):
        cap = shapes(W, H, [rect(x0 - 6, yc - 10, x1 + 6, yc + 10)], smooth=False)
        art = chrome(art, cap, nx, (6, 0))
        rr = ellipses(W, H, [(184, yc - (10 if yc == y0 else -10), 70, 8, 0)])
        art = chrome(art, rr * (1 if yc == y0 else 0), nx) if yc == y0 else art
    spool = shapes(W, H, [rect(170, 28, 198, 62)], smooth=False)
    art = GP(art, spool, "#2a2420", "#3a322c", seed=nx(), rough=0.4)
    art = tint(art, side_light(spool, 3, 0, 2), "#000000", 0.5, seed=nx())
    sh = ellipses(W, H, [(230, 312, 170, 14, 0)])
    art = over(col_arr(sh, "#1a120c", gaussian_filter(sh, 8) * 0.4), art)
    preview(art, "fa-canister", bg="#f1e8d6")
    save(art, f"{OUT}/canister.webp", max_w=180, quality=84)
    clear()

if "leak" in PARTS:
    W, H = 560, 760
    nx = Seq(62300)
    items = [(150, 200, 170, "#ff5a1e", 0.9), (110, 380, 130, "#ff2a18", 0.7), (230, 150, 110, "#ffb030", 0.8),
             (380, 560, 120, "#ff7a20", 0.5), (300, 420, 80, "#ffd060", 0.4)]
    art = edge_fade(light_leak(W, H, items, seed=nx()), 140)
    preview(art, "fa-leak", bg="#171310")
    save_full(art, f"{OUT}/leak.webp", size=(280, 380), quality=80)
    clear()

if "circle" in PARTS:
    W, H = 300, 220
    nx = Seq(62400); rng = random.Random(624)
    pts = []
    for k in range(70):
        t = k / 69
        a = -2.2 + t * math.tau * 1.12
        r = 1 + 0.06 * math.sin(t * 9)
        pts.append((150 + math.cos(a) * 124 * r, 110 + math.sin(a) * 86 * r + t * 8))
    m = strokes(W, H, [(pts, 9, (0.05, 0.12))])
    art = crayon(blank(W, H), m, "#d4241c", seed=nx(), amt=0.95, tooth=0.5)
    art = crayon(art, strokes(W, H, [([(p[0] + 1.5, p[1] + 1) for p in pts[20:60]], 4, None)]), "#b81a14", seed=nx(), amt=0.6, tooth=0.6)
    preview(art, "fa-circle", bg="#171310")
    save(art, f"{OUT}/circle.webp", max_w=150, quality=84)
    clear()

if "tape" in PARTS:
    W, H = 320, 110
    nx = Seq(62500); rng = random.Random(625)
    pts = [(14, 30), (40, 26), (300, 22), (308, 34), (302, 46), (306, 60), (300, 76), (34, 84), (20, 74), (12, 60), (18, 46)]
    m = shapes(W, H, [pts], smooth=False)
    art = cutpaper(blank(W, H), m, "#e8d9b0", seed=nx(), shadow=0.18, torn=2.2, edge=1.0, grain=1.4, core="#f4ead0", sdx=1, sdy=2, sblur=2.5)
    art[..., 3] *= 0.9
    preview(art, "fa-tape", bg="#171310")
    save(art, f"{OUT}/tape.webp", max_w=160, quality=84)
    clear()

if "grain" in PARTS:
    n = 128
    art = film_grain_tile(n, seed=62600, amt=0.35)
    save_texture(art, f"{OUT}/grain.webp", quality=55)
    print("grain", os.path.getsize(f"{OUT}/grain.webp") // 1024, "KB")

if "snip" in PARTS:
    # a short cut piece of colour negative: orange mask base, sprocket holes, three frames with faint inverted shapes
    W, H = 420, 110
    nx = Seq(62700); rng = random.Random(627)
    pts = [(8, 18), (412, 12), (414, 96), (10, 100)]
    base = shapes(W, H, [pts], smooth=False)
    art = GP(blank(W, H), base, "#b8642e", "#c87438", seed=nx(), rough=0.6, streak=0.6, density=0.9)
    for k in range(3):
        x0 = 22 + k * 132
        fr = shapes(W, H, [rrect(x0, 30, x0 + 118, 82, 5)], smooth=False)
        art = tint(art, fr, "#6a2c14", 0.7, seed=nx())
        for j in range(3):
            b = ellipses(W, H, [(x0 + rng.uniform(20, 98), rng.uniform(42, 72), rng.uniform(10, 26), rng.uniform(8, 18), rng.uniform(0, 180))]) * fr
            art = tint(art, gaussian_filter(b, 4), rng.choice(["#2a6a7a", "#d8e4e0", "#3a8a8a"]), 0.45, seed=nx())
    holes = shapes(W, H, [rrect(14 + k * 26, 18 + (k % 1), 28 + k * 26, 26, 2, 3) for k in range(15)] + [rrect(14 + k * 26, 88, 28 + k * 26, 96, 2, 3) for k in range(15)], smooth=False)
    art = knockout(art, holes, 1.0, 0.4)
    art = tint(art, side_light(base, 0, 3, 3), "#3a1608", 0.3, seed=nx())
    preview(art, "fa-snip", bg="#f1e8d6")
    save(art, f"{OUT}/snip.webp", max_w=210, quality=84)
    clear()
