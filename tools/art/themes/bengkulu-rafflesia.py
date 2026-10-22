"""Bengkulu Rafflesia — gouache: a giant rafflesia arnoldii seen from above (five fleshy brick-red lobes with raised
cream warts, the spotted diaphragm rim and the dark cup with its pale spiked disc), deep-green jungle leaves and fern
fronds, Pantai Panjang at sunset with casuarina trees and a rumah adat Bubungan Lima on stilts, a vine divider.
Run: python3 -I bengkulu-rafflesia.py [part ...]   parts: bloom leaves scene vine
Assets -> public/themes/art/bengkulu-rafflesia/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c1_lib import *

OUT = outdir("bengkulu-rafflesia")
PARTS = sys.argv[1:] or ["bloom", "leaves", "scene", "vine"]
RED, RED_D, RED_L, MAROON = "#b9442b", "#8a2c1f", "#d46a3e", "#4a1410"
CREAM, CREAM_D = "#f1dfc4", "#cdb394"
GREEN, GREEN_D, GREEN_L, GREEN_X = "#2f5d3c", "#1d3d29", "#77a066", "#132a1c"


def rafflesia(art, W, H, cx, cy, R, rng, nx, rot=0.0, spots=True):
    """Top view of a rafflesia bloom centred at (cx, cy), lobe radius R."""
    lobes = []
    for k in range(5):
        a = rot + k * math.tau / 5 + rng.uniform(-0.06, 0.06)
        r = R * rng.uniform(0.93, 1.04)
        pts = []
        # rounded broad lobe: polar bump between a-0.75 and a+0.75
        for i in range(29):
            t = -1 + 2 * i / 28
            ang = a + t * 0.78
            rr = r * (0.36 + 0.64 * (1 - abs(t) ** 2.2) ** 0.6) * (1 + 0.035 * math.sin(t * 9 + k * 1.7) + 0.02 * math.sin(t * 17 + k))
            pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
        pts.append((cx + math.cos(a + 0.6) * R * 0.25, cy + math.sin(a + 0.6) * R * 0.25))
        pts.append((cx + math.cos(a - 0.6) * R * 0.25, cy + math.sin(a - 0.6) * R * 0.25))
        lobes.append((a, r, deform(pts, rng, 2, 0.004)))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    # drop shadow on the forest floor
    allm = shapes(W, H, [p for _, _, p in lobes])
    sh = np.roll(np.roll(gaussian_filter(allm, R * 0.05), int(R * 0.03), 0), int(R * 0.02), 1)
    art = wash(art, sh * 0.85, "#0e1d13", 0.55, seed=nx())
    order = [0, 2, 4, 1, 3]
    for k in order:
        a, r, pts = lobes[k]
        m = shapes(W, H, [pts])
        cast = np.roll(np.roll(gaussian_filter(m, R * 0.025), int(R * 0.025), 0), int(R * 0.02), 1) * (1 - m) * art[..., 3]
        art = wash(art, cast, "#3a0d0a", 0.6, seed=nx())
        art = knockout(art, m, 1.0, 1.0)
        art = GP(art, m, RED, "#c0502f", seed=nx(), rough=2.6, streak=1.0)
        mot = np.clip((fbm(W, H, nx(), 26, 3) - 0.45) * 2.2, 0, 1)
        art = wash(art, m * mot, RED_D, 0.38, seed=nx())
        art = relief(art, m, R * 0.08, 0.55, light="#ef9a6a", dark="#4a120c", seed=nx())
        net = np.clip((0.06 - np.abs(fbm(W, H, nx(), 14, 2) - 0.5)) / 0.06, 0, 1)
        art = wash(art, m * net * np.clip((d / r - 0.35) * 2, 0, 1), "#7a2419", 0.35, seed=nx())
        art = wash(art, m * grad(W, H, cx - R, cy - R, cx + R, cy + R), "#5a1610", 0.38, seed=nx())
        art = wash(art, m * (1 - grad(W, H, cx - R, cy - R, cx + R * 0.4, cy + R * 0.4)), "#e5865a", 0.32, seed=nx())
        # fleshy rim: darker, thick edge
        rim = np.clip(m - gaussian_filter(m, R * 0.03), 0, 1) * 3
        art = wash(art, np.clip(rim, 0, 1) * m, RED_D, 0.6, seed=nx())
        # dark toward the cup, lit toward the outer edge (light from upper left)
        art = wash(art, m * np.clip(1 - (d - R * 0.3) / (R * 0.35), 0, 1), MAROON, 0.45, seed=nx())
        lit = m * np.clip((d / r - 0.55) * 2, 0, 1) * np.clip(0.5 - (math.cos(a) * 0.7 + math.sin(a) * 0.7) * 0.5, 0, 1)
        art = wash(art, lit, "#e7895a", 0.35, seed=nx())
        # overlap shadow cast by neighbours drawn later is natural via knockout; add a soft fold crease
        crease = strokes(W, H, [([(cx + math.cos(a) * r * 0.35, cy + math.sin(a) * r * 0.35), (cx + math.cos(a + 0.04) * r * 0.8, cy + math.sin(a + 0.04) * r * 0.8)], R * 0.03, (0.2, 0.6))]) * m
        art = wash(art, gaussian_filter(crease, 3), RED_D, 0.3, seed=nx())
        if spots:
            items = []
            for _ in range(int(70 * (R / 300) ** 0.3)):
                t = rng.uniform(-0.62, 0.62); rr = r * rng.uniform(0.42, 0.93) * (1 - abs(t) ** 2.4 * 0.5)
                ang = a + t * 0.78
                sx, sy = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr
                s = R * (rng.uniform(0.008, 0.022) if rng.random() < 0.6 else rng.uniform(0.022, 0.04)) * (0.6 + rr / r * 0.6)
                items.append(deform(ellipse_pts(sx, sy, s * rng.uniform(0.8, 1.3), s * rng.uniform(0.7, 1.1), 9, rng.uniform(0, 3)), rng, 1, 0.08))
            sm = shapes(W, H, items) * m
            shm = np.roll(np.roll(sm, 2, 0), 2, 1) * m
            art = wash(art, gaussian_filter(shm, 1.0), MAROON, 0.55, seed=nx())
            art = GP(art, sm, "#ecd6b8", "#e2bd9c", seed=nx(), rough=1.1, streak=0.5)
            art = wash(art, sm * np.clip(1 - gaussian_filter(sm, 2.5) * 1.3, 0, 1) * 2, "#d4937a", 0.5, seed=nx())
            art = wash(art, sm * np.roll(np.roll(gaussian_filter(sm, 1.5), -2, 0), -2, 1), "#fff6e6", 0.5, seed=nx())
            art = wash(art, np.clip(sm - np.roll(np.roll(sm, -2, 0), -2, 1), 0, 1), CREAM_D, 0.6, seed=nx())
    # diaphragm (cup rim) — a raised ring
    r_out, r_in = R * 0.42, R * 0.25
    ring_m = shapes(W, H, [deform(ellipse_pts(cx, cy, r_out, r_out * 0.97, 40), rng, 1, 0.01)])
    sh2 = np.roll(np.roll(gaussian_filter(ring_m, R * 0.03), int(R * 0.02), 0), int(R * 0.02), 1)
    art = wash(art, sh2 * (1 - ring_m), "#2a0b08", 0.6, seed=nx())
    art = GP(art, ring_m, RED, "#c2512f", seed=nx(), rough=1.6, streak=0.8)
    art = wash(art, ring_m * np.clip((fbm(W, H, nx(), 20, 3) - 0.45) * 2.2, 0, 1), RED_D, 0.35, seed=nx())
    art = wash(art, ring_m * grad(W, H, cx - r_out, cy - r_out, cx + r_out, cy + r_out), "#5a1610", 0.4, seed=nx())
    art = relief(art, ring_m, R * 0.03, 0.5, light="#f0a070", dark="#3a0d0a", seed=nx())
    lip = np.clip(ring_m - circles(W, H, [(cx + 2, cy + 2, r_out - R * 0.012)]), 0, 1)
    art = wash(art, lip, "#f0a070", 0.35, seed=nx())
    art = wash(art, ring_m * np.clip((d - r_in) / (r_out - r_in), 0, 1) * np.clip(0.5 - ((xx - cx) + (yy - cy)) / (R * 0.6), 0, 1), "#e7895a", 0.4, seed=nx())
    # the rim's pale "window" spots in a ring
    items = []
    for i in range(26):
        ang = i / 26 * math.tau + rng.uniform(-0.05, 0.05)
        rr = (r_out + r_in) / 2 + rng.uniform(-R * 0.03, R * 0.03)
        s = R * rng.uniform(0.022, 0.034)
        items.append(deform(ellipse_pts(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr, s * 1.3, s, 9, ang + 1.57), rng, 1, 0.08))
    for i in range(18):
        ang = i / 18 * math.tau + 0.17
        rr = r_out * 0.93
        s = R * 0.017
        items.append(ellipse_pts(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr, s, s * 0.8, 8, ang))
    sm = shapes(W, H, items) * ring_m
    art = GP(art, sm, CREAM, "#ead4b4", seed=nx(), rough=0.8, streak=0.4)
    # the cup opening: deep shadow
    hole = shapes(W, H, [deform(ellipse_pts(cx, cy, r_in, r_in * 0.96, 30), rng, 1, 0.012)])
    art = GP(art, hole, "#3a0f0b", "#24080a", seed=nx(), rough=1.0, streak=0.5)
    # central disc with processes (spikes), seen at the bottom of the cup
    disc_r = r_in * 0.72
    disc = shapes(W, H, [ellipse_pts(cx + R * 0.02, cy + R * 0.02, disc_r, disc_r, 30)])
    art = GP(art, disc, "#7c2a1d", "#9a3a26", seed=nx(), rough=0.8, streak=0.4)
    sp = []
    for i in range(70):
        ang = rng.uniform(0, math.tau); rr = disc_r * math.sqrt(rng.uniform(0, 0.85))
        sp.append((cx + R * 0.02 + math.cos(ang) * rr, cy + R * 0.02 + math.sin(ang) * rr, R * rng.uniform(0.007, 0.012)))
    spm = circles(W, H, sp) * disc
    art = GP(art, spm, "#e4c4a8", "#d0a588", seed=nx(), rough=0.4, streak=0.3)
    # inner wall shading of the cup on the light side
    wall = hole * (1 - disc) * np.clip(((xx - cx) + (yy - cy)) / (r_in * 1.4) + 0.5, 0, 1)
    art = wash(art, wall, "#6b2017", 0.55, seed=nx())
    inlip = np.clip(circles(W, H, [(cx, cy, r_in + R * 0.012)]) - circles(W, H, [(cx + R * 0.008, cy + R * 0.008, r_in)]), 0, 1)
    art = wash(art, inlip, "#e9a074", 0.55, seed=nx())
    return art


if "bloom" in PARTS:
    W, H = 900, 900
    nx = Seq(100)
    rng = random.Random(11)
    art = blank(W, H)
    art = rafflesia(art, W, H, 450, 452, 410, rng, nx, rot=-math.pi / 2)
    save(art, f"{OUT}/bloom.webp", max_w=620, quality=78)
    show(art, "br-bloom", tone="#1d3d29")
    clear()

if "leaves" in PARTS:
    # corner cluster of jungle leaves + fern, anchored bottom-left (mirrored in CSS for the other side)
    W, H = 640, 720
    nx = Seq(400)
    rng = random.Random(5)
    art = blank(W, H)
    art = fern_frond(art, W, H, curve([(10, 700), (150, 520), (280, 420), (400, 380)], 40), 70, rng, nx, cols=("#4c7b4e", "#355f3c"))
    specs = [(0, 720, 520, 120, -1.05, ("#244a31", "#1a3826")), (0, 640, 460, 110, -0.55, (GREEN, GREEN_D)),
             (40, 720, 430, 100, -1.45, ("#3c6c45", "#2b5236")), (0, 560, 360, 90, -0.2, ("#2a5637", "#1f412b")),
             (120, 720, 300, 80, -0.85, ("#4a7d4f", "#355f3c"))]
    for x, y, L, Wd, ang, cols in specs:
        art = jungle_leaf(art, W, H, x, y, L, Wd, ang, rng, nx, cols=cols, bend=rng.uniform(-0.12, 0.12))
    art = fern_frond(art, W, H, curve([(60, 720), (100, 560), (90, 420), (50, 300)], 40), 56, rng, nx, cols=("#5d8a58", "#3f6b45"))
    save(art, f"{OUT}/leaves.webp", max_w=420, quality=80)
    show(art, "br-leaves")
    clear()


def bubungan_lima(art, W, H, cx, by, s, rng, nx):
    """Rumah adat Bengkulu: raised timber house on stilts, a tall hipped roof with five ridges (the main ridge and four
    hips meeting it), front verandah with a stair; painted in gouache against the sunset (warm rim light)."""
    def P(u, v):
        return (cx + u * s, by + v * s)
    WOOD, WOOD_D, WOOD_L, ROOF, ROOF_D = "#6a3b24", "#3f2216", "#a5653b", "#3b2a24", "#24181a"
    # stilts
    st = strokes(W, H, [([P(u, 0), P(u, -0.42)], s * 0.035, None) for u in (-0.95, -0.55, -0.15, 0.25, 0.65, 0.95)])
    art = GP(art, st, WOOD_D, "#2e1a12", seed=nx(), rough=0.8)
    # floor beam & walls
    body = shapes(W, H, [[P(-1.05, -0.40), P(1.05, -0.40), P(1.02, -0.92), P(-1.02, -0.92)]], smooth=False)
    art = GP(art, body, WOOD, "#7a4429", seed=nx(), rough=1.0, streak=0.9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seams = np.clip(1 - np.abs(((xx - cx) / (s * 0.09)) % 1.0 - 0.5) * 2 - 0.84, 0, 1) * 6 * body
    art = wash(art, np.clip(seams, 0, 1), WOOD_D, 0.5, seed=nx())
    art = wash(art, body * grad(W, H, cx + s, 0, cx - s, 0), WOOD_L, 0.35, seed=nx())
    beam = shapes(W, H, [[P(-1.12, -0.36), P(1.12, -0.36), P(1.12, -0.44), P(-1.12, -0.44)]], smooth=False)
    art = GP(art, beam, WOOD_D, seed=nx(), rough=0.6)
    # windows with warm lamplight
    win = shapes(W, H, [[P(u - 0.1, -0.52), P(u + 0.1, -0.52), P(u + 0.1, -0.8), P(u - 0.1, -0.8)] for u in (-0.7, 0.45, 0.8)], smooth=False)
    art = GP(art, win, "#f2b45c", "#e39645", seed=nx(), rough=0.6)
    door = shapes(W, H, [[P(-0.22, -0.42), P(0.12, -0.42), P(0.12, -0.84), P(-0.22, -0.84)]], smooth=False)
    art = GP(art, door, "#2e1a12", seed=nx(), rough=0.6)
    # stair
    stair = strokes(W, H, [([P(-0.32, -0.42), P(-0.55, 0.02)], s * 0.03, None), ([P(0.02, -0.42), P(-0.2, 0.02)], s * 0.03, None)] +
                    [([P(-0.32 - 0.23 * t, -0.42 + 0.44 * t), P(0.02 - 0.23 * t, -0.42 + 0.44 * t)], s * 0.02, None) for t in (0.2, 0.4, 0.6, 0.8)])
    art = GP(art, stair, WOOD_D, seed=nx(), rough=0.5)
    # roof: big hipped roof, steep, with a short ridge (bubungan) and flared eaves
    roof = shapes(W, H, [[P(-1.35, -0.86), P(-0.32, -1.88), P(0.32, -1.88), P(1.35, -0.86), P(1.2, -0.80), P(-1.2, -0.80)]], smooth=False)
    art = GP(art, roof, ROOF, "#4a3328", seed=nx(), rough=1.2, streak=1.0)
    # thatch/shingle courses
    rows = np.clip(1 - np.abs(((yy - by) / (s * 0.07)) % 1.0 - 0.5) * 2 - 0.82, 0, 1) * 5 * roof
    art = wash(art, np.clip(rows, 0, 1), ROOF_D, 0.45, seed=nx())
    # sunset rim light on the right roof plane
    right = shapes(W, H, [[P(0.32, -1.88), P(1.35, -0.86), P(1.2, -0.80), P(0.1, -0.80)]], smooth=False) * roof
    art = wash(art, right, "#b5603a", 0.35, seed=nx())
    # the five ridges: main ridge + four hips, plus crest finials
    ridges = strokes(W, H, [([P(-0.32, -1.88), P(0.32, -1.88)], s * 0.05, None), ([P(-0.32, -1.88), P(-1.35, -0.86)], s * 0.035, (0.0, 0.3)),
                            ([P(0.32, -1.88), P(1.35, -0.86)], s * 0.035, (0.0, 0.3)), ([P(-0.32, -1.88), P(-0.7, -0.82)], s * 0.025, (0.0, 0.3)),
                            ([P(0.32, -1.88), P(0.7, -0.82)], s * 0.025, (0.0, 0.3)), ([P(-0.32, -1.88), P(-0.36, -1.98)], s * 0.03, None), ([P(0.32, -1.88), P(0.36, -1.98)], s * 0.03, None)])
    art = GP(art, ridges, "#1c1214", seed=nx(), rough=0.6)
    eave = strokes(W, H, [([P(-1.36, -0.85), P(1.36, -0.85)], s * 0.035, None)])
    art = GP(art, eave, "#2a1a16", seed=nx(), rough=0.6)
    return art


def cemara(W, H, x, by, h, rng, lean=0.0):
    """Casuarina (cemara laut) silhouette: bare lower trunk, tall ragged cone of drooping tiers."""
    trunk = [([(x, by), (x + lean * h * 0.5, by - h * 0.6), (x + lean * h, by - h)], max(2, h * 0.022), (0.0, 0.5))]
    tiers = int(6 + h / 35)
    left, right = [], []
    for i in range(tiers + 1):
        t = 0.3 + 0.7 * i / tiers
        px, py = x + lean * h * t, by - h * t
        wdt = h * 0.17 * (1 - (t - 0.3) / 0.7) ** 0.8 * rng.uniform(0.8, 1.2) + 2
        left += [(px - wdt, py + h * 0.02), (px - wdt * 0.45, py - h * 0.02)]
        right += [(px + wdt * rng.uniform(0.85, 1.15), py + h * 0.02), (px + wdt * 0.45, py - h * 0.02)]
    pts = left + [(x + lean * h, by - h * 1.03)] + right[::-1]
    crown = shapes(W, H, [deform(pts, rng, 1, 0.03)], smooth=False)
    fr = []
    for k in range(0, len(left), 2):
        for (ex, ey) in (left[k], right[k]):
            for _ in range(4):
                sx = ex + rng.uniform(-4, 4)
                fr.append(([(sx, ey - 2), (sx + rng.uniform(-1, 1), ey + h * rng.uniform(0.02, 0.05))], 1.2, (0.0, 0.8)))
    return strokes(W, H, trunk), np.clip(crown + strokes(W, H, fr), 0, 1)


if "scene" in PARTS:
    W, H = 840, 600
    nx = Seq(700)
    rng = random.Random(23)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    HZ = 330
    sky = painted_sky(W, HZ + 10, [(0, "#4b3b6b"), (0.35, "#b5577a"), (0.7, "#ec8a5a"), (1.0, "#f6c47b")], seed=nx())
    art = blank(W, H)
    art[:HZ + 10] = sky
    # sun low over the Indian Ocean, half set
    sun = circles(W, H, [(560, HZ - 6, 46)]) * (yy < HZ)
    art = wash(art, glow(sun, "#ffd89a", 40, 0.9)[..., 3], "#ffcf86", 0.55, seed=nx())
    art = GP(art, sun, "#fff0c9", "#ffd88f", seed=nx(), rough=0.8)
    # streaky clouds lit from below
    for cy_, x0, x1, c in [(120, 40, 420, "#d37a7c"), (170, 470, 820, "#e6977a"), (82, 520, 760, "#9b5a7c"), (230, 80, 360, "#f0a56f")]:
        cl = strokes(W, H, [([(x0 + rng.uniform(-20, 20), cy_ + k * 7 + rng.uniform(-3, 3)), (x1 + rng.uniform(-30, 30), cy_ + k * 7 + rng.uniform(-3, 3))], rng.uniform(3, 7), (0.3, 0.4)) for k in range(3)])
        art = wash(art, gaussian_filter(cl, 1.5), c, 0.6, seed=nx())
    # sea
    sea = (yy >= HZ).astype(np.float32) * (yy < 470)
    art = wash(art, sea, "#5b4f78", 1.0, seed=nx(), col2="#6d5a80")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, 470), "#2f3c5e", 0.6, seed=nx())
    art = wash(art, sea * np.clip(1 - np.abs(xx - 560) / 160, 0, 1) * np.clip(1 - (yy - HZ) / 140, 0, 1), "#f2a66c", 0.5, seed=nx())
    gl = sun_glints(W, H, 560, HZ + 4, 460, 120, rng, spread=50) * sea
    art = wash(art, gl, "#ffe2a8", 0.9, seed=nx())
    waves_m = strokes(W, H, [([(x, y), (x + rng.uniform(20, 60), y + rng.uniform(-1, 1))], rng.uniform(1, 2.2), (0.3, 0.3)) for x, y in [(rng.uniform(-20, W), rng.uniform(HZ + 10, 465)) for _ in range(140)]]) * sea
    art = wash(art, waves_m, "#8a6d93", 0.5, seed=nx())
    # surf line and long beach (Pantai Panjang)
    beach = shapes(W, H, [[(-20, 468), (300, 458), (860, 446), (860, 620), (-20, 620)]])
    art = GP(art, beach, "#c98a62", "#b9795a", seed=nx(), rough=2.0)
    art = wash(art, beach * grad(W, H, 0, 450, 0, 600), "#5a3a3a", 0.55, seed=nx())
    wet = strokes(W, H, [(curve([(-20, 470), (300, 461), (860, 449)], 30), 7, (0.0, 0.0))])
    art = wash(art, wet, "#f6c898", 0.6, seed=nx())
    foam = strokes(W, H, [(curve([(x, 462 - x * 0.02), (x + 60, 460 - x * 0.02)], 8), 2.2, (0.3, 0.3)) for x in range(-20, 860, 70)])
    art = wash(art, foam, "#fff2dc", 0.7, seed=nx())
    sand = beach * np.clip((fbm(W, H, nx(), 18, 3) - 0.5) * 3, 0, 1)
    art = wash(art, sand, "#dba077", 0.18, seed=nx())
    refl = beach * np.clip(1 - np.abs(xx - 560) / 90, 0, 1) * np.clip(1 - (yy - 460) / 60, 0, 1)
    art = wash(art, refl, "#f3b77e", 0.5, seed=nx())
    for bx, by_, bs in [(470, 400, 26), (660, 372, 16)]:
        hull = shapes(W, H, [[(bx - bs, by_), (bx + bs, by_), (bx + bs * 0.7, by_ + bs * 0.18), (bx - bs * 0.75, by_ + bs * 0.18)]])
        sail = shapes(W, H, [[(bx - bs * 0.1, by_ - 2), (bx - bs * 0.1, by_ - bs * 1.2), (bx + bs * 0.6, by_ - 2)]], smooth=False)
        art = GP(art, hull + sail, "#2a2233", seed=nx(), rough=0.5)
    # casuarina line on the right, house on the left
    for x, h, ln in [(690, 230, 0.04), (740, 270, -0.03), (800, 210, 0.05), (640, 150, 0.0), (240, 170, -0.04), (40, 190, 0.03)]:
        tr, tf = cemara(W, H, x, 470 - (x > 600) * 8, h, rng, ln)
        art = GP(art, tr, "#2a2233", "#3a2a3a", seed=nx(), rough=0.8, streak=0.4)
        art = GP(art, tf, "#2c2436", "#3d2c3c", seed=nx(), rough=2.0, streak=0.5)
        art = wash(art, tf * grad(W, H, x + 60, 0, x - 40, 0), "#7a4a5c", 0.3, seed=nx())
    art = bubungan_lima(art, W, H, 330, 520, 118, rng, nx)
    # foreground jungle leaves framing the bottom-left
    art = jungle_leaf(art, W, H, -10, 610, 260, 60, -0.45, rng, nx, cols=("#1d3d29", "#132a1c"), light="#4f7a4e")
    art = jungle_leaf(art, W, H, 870, 610, 240, 56, math.pi + 0.5, rng, nx, cols=("#1d3d29", "#132a1c"), light="#4f7a4e")
    art = fade_edges(art, top=60)
    save(art, f"{OUT}/scene.webp", max_w=720, quality=74)
    show(art, "br-scene")
    clear()

if "vine" in PARTS:
    W, H = 460, 90
    nx = Seq(900)
    rng = random.Random(4)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(14, 50), (110, 40), (180, 52), (230, 45)], 30), 3.2, (0.1, 0.0)), (curve([(446, 50), (350, 40), (280, 52), (230, 45)], 30), 3.2, (0.1, 0.0))])
    art = GP(art, stem, GREEN_D, seed=nx(), rough=0.6)
    for x, y, a in [(60, 46, -0.9), (120, 42, -2.3), (160, 50, 0.7), (400, 46, -2.3), (340, 42, -0.8), (300, 50, 2.4)]:
        art = jungle_leaf(art, W, H, x, y, 44, 12, a, rng, nx, cols=(GREEN, GREEN_D), light=GREEN_L)
    art = rafflesia(art, W, H, 230, 45, 38, rng, nx, rot=-math.pi / 2, spots=True)
    save(art, f"{OUT}/vine.webp", max_w=380, quality=82)
    show(art, "br-vine")
    clear()
