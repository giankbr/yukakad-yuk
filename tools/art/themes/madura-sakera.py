"""Madura Sakera — bold red/black/white: batik tulis Madura tile (red & yellow florals on near-black, canting wax lines,
remukan crackle), Sakera red-white stripe cloth, rumah tanean lanjang row with langgar at dusk (gouache), a single
batik flower emblem and a brush divider. Run: python3 -I madura-sakera.py [part ...]
parts: batik stripes tanean flower divider. Assets -> public/themes/art/madura-sakera/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a1_lib import *

OUT = outdir("madura-sakera")
PARTS = sys.argv[1:] or ["batik", "stripes", "tanean", "flower", "divider"]
INK = "#160d0b"
RED, RED_D, RED_L = "#c3262c", "#7d1418", "#e04a3c"
YEL, YEL_D = "#e9b42c", "#b07a12"
GRN, GRN_D = "#3f7a3a", "#244a24"
CREAM = "#f3e6cc"


def flower_polys(cx, cy, r, n, rot, rng):
    petals = []
    for k in range(n):
        a = rot + k * math.tau / n
        petals.append(deform(petal_pts(cx + math.cos(a) * r * 0.16, cy + math.sin(a) * r * 0.16, r * 0.92, r * 0.34, a, n=18), rng, 1, 0.025))
    return petals


def inner_polys(cx, cy, r, n, rot, rng):
    out = []
    for k in range(n):
        a = rot + k * math.tau / n
        out.append(petal_pts(cx + math.cos(a) * r * 0.3, cy + math.sin(a) * r * 0.3, r * 0.5, r * 0.17, a, n=14))
    return out


def batik_motifs(T, rng):
    """Motif placement for one tile: (kind, cx, cy, r, rot)."""
    return [("big", 132, 140, 74, 0.3), ("big", 372, 352, 82, 1.1), ("mid", 380, 104, 40, 0.5), ("mid", 104, 392, 44, 0.9),
            ("bud", 250, 240, 22, -0.6), ("bud", 250, 30, 20, 1.8), ("bud", 20, 250, 20, 0.2)]


def wrap_offsets(T):
    return [(dx, dy) for dx in (-T, 0, T) for dy in (-T, 0, T)]


if "batik" in PARTS:
    T = 480
    nx = Seq(30100); rng = random.Random(4)
    motifs = batik_motifs(T, rng)
    petals, hearts, leaves, stems, buds, dots_in, inners = [], [], [], [], [], [], []
    for (kind, cx, cy, r, rot) in motifs:
        for dx, dy in wrap_offsets(T):
            x, y = cx + dx, cy + dy
            if kind in ("big", "mid"):
                petals += flower_polys(x, y, r, 6 if kind == "big" else 5, rot, random.Random(int(cx + cy)))
                hearts.append((x, y, r * 0.32))
                inners.extend(inner_polys(x, y, r, 6 if kind == "big" else 5, rot, rng))
                for k in range(6 if kind == "big" else 5):
                    a = rot + k * math.tau / (6 if kind == "big" else 5)
                    for t in (0.45, 0.62, 0.78):
                        dots_in.append((x + math.cos(a) * r * t, y + math.sin(a) * r * t))
            else:
                buds.append(deform(petal_pts(x, y, r * 2.2, r * 0.8, rot, n=14), random.Random(int(cx)), 1, 0.03))
    # leaves and curling stems between flowers
    leaf_specs = [(20, 110, 50, -1.0), (450, 450, 48, 2.0), (300, 470, 44, 0.6), (140, 250, 46, 2.4), (430, 20, 40, -2.6), (180, 470, 40, -0.7), (200, 60, 70, 0.4), (60, 200, 66, 1.9), (300, 250, 76, -0.9), (230, 420, 70, 2.6), (440, 220, 64, 1.3), (180, 300, 56, -2.2), (300, 160, 54, 0.2)]
    stem_specs = [[(132, 140), (190, 200), (250, 240), (310, 290), (372, 352)], [(380, 104), (330, 80), (280, 40), (250, 30)],
                  [(104, 392), (80, 330), (40, 280), (20, 250)], [(250, 240), (230, 180), (200, 60)]]
    for dx, dy in wrap_offsets(T):
        for (x, y, L, a) in leaf_specs:
            leaves.append(deform(petal_pts(x + dx, y + dy, L, L * 0.34, a, n=16, cup=0.25), random.Random(int(x)), 1, 0.03))
        for sp in stem_specs:
            stems.append([(px + dx, py + dy) for px, py in curve(sp, 40)])
    W = H = T
    clip = lambda m: m
    pet = shapes(W, H, petals)
    hrt = circles(W, H, hearts)
    lvs = shapes(W, H, leaves)
    bds = shapes(W, H, buds)
    stm = polyline_mask(W, H, stems, 5.0)
    # cloth ground: near black-brown mori with dye mottling
    art = cloth_base(W, H, INK, seed=nx(), cell=2.0, var=0.18)
    art = over(art, flat(fbm(W, H, nx(), 60, 3) * 0.25, "#3a1a12"))
    # colour fields (dyed: small bleed), leaves under flowers
    art = over(art, tie_dye(np.clip(lvs - pet, 0, 1), GRN, seed=nx(), bleed=1.2, density=0.95))
    art = over(art, tie_dye(stm, YEL_D, seed=nx(), bleed=0.8, density=0.9))
    art = over(art, tie_dye(np.maximum(pet, bds), RED, seed=nx(), bleed=1.2, density=0.97))
    art = over(art, tie_dye(hrt, YEL, seed=nx(), bleed=1.0, density=0.97))
    # inner petal shading (second dye bath)
    inner = np.clip(pet - gaussian_filter(pet, 4) * 0.0, 0, 1) * np.clip(1 - gaussian_filter(hrt, 10) * 2, 0, 1)
    art = over(art, flat(inner * np.clip((fbm(W, H, nx(), 20, 3) - 0.45) * 2, 0, 1), RED_D, 0.5))
    inn = shapes(W, H, inners)
    art = over(art, tie_dye(np.clip(inn - hrt, 0, 1), RED_D, seed=nx(), bleed=0.8, density=0.9))
    art = over(art, flat(outline(inn, 1.4) * (1 - hrt), YEL, 0.9))
    saw = lvs * hatch(W, H, 2.2, 5.0, 0.16, nx(), 0.8)
    art = over(art, flat(saw * np.clip(1 - gaussian_filter(pet, 2) * 3, 0, 1), CREAM, 0.6))
    # canting outlines in cream wax, isen-isen dots, leaf veins
    ol = np.maximum.reduce([outline(pet, 2.2), outline(lvs, 2.0), outline(hrt, 2.0), outline(bds, 2.0)])
    ol *= np.clip((fbm(W, H, nx(), 7, 2) - 0.1) * 6, 0, 1)
    art = over(art, flat(ol, CREAM, 0.95))
    veins = []
    for dx, dy in wrap_offsets(T):
        for (x, y, L, a) in leaf_specs:
            veins.append([(x + dx + math.cos(a) * L * t, y + dy + math.sin(a) * L * t + 0) for t in (0.05, 0.5, 0.92)])
    art = over(art, flat(wax_line(W, H, veins, 1.6, nx()), YEL, 0.95))
    dm = circles(W, H, [(x, y, 2.4) for x, y in dots_in])
    art = over(art, flat(dm, YEL, 0.95))
    # cecek dots scattered on the ground
    rr = random.Random(9); gd = []
    for _ in range(420):
        x, y = rr.uniform(0, T), rr.uniform(0, T)
        gd += [(x + dx, y + dy, rr.uniform(1.0, 1.8)) for dx, dy in wrap_offsets(T)]
    gdm = circles(W, H, gd) * np.clip(1 - gaussian_filter(np.maximum.reduce([pet, lvs, hrt, bds]), 3) * 3, 0, 1)
    art = over(art, flat(gdm, CREAM, 0.55))
    # remukan crackle: thin dark veins where the wax cracked
    cr = fbm(W, H, nx(), 22, 3)
    crack = np.clip(1 - np.abs(cr - 0.5) * 30, 0, 1) * np.maximum(pet, lvs)
    art = over(art, flat(crack, "#2a0c0a", 0.6))
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/batik.webp", quality=74)
    clear()

if "stripes" in PARTS:
    # Sakera shirt: crisp red-white horizontal stripes on cotton, periodic wobble so the tile repeats both ways
    W, H = 240, 120
    nx = Seq(30200)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wob = 1.6 * np.sin(xx / W * math.tau * 2 + 0.4) + 0.8 * np.sin(xx / W * math.tau * 5 + 1.3)
    period = H / 4
    f = ((yy + wob) % period) / period
    red = np.clip((np.abs(f - 0.5) - 0.24) * 8, 0, 1)   # red band ~ half
    cloth = cloth_base(W, H, "#f6efe2", seed=nx(), cell=2.0, var=0.05)
    dye = flat(red, RED)
    dye[..., :3] *= (0.92 + 0.12 * wrap_noise(W, H, 3, 6))[..., None]
    art = cloth.copy()
    art[..., :3] = cloth[..., :3] * (1 - red[..., None]) + dye[..., :3] * cloth[..., :3] * 1.06 * red[..., None]
    save_rgb(np.clip(art, 0, 1), f"{OUT}/stripes.webp", quality=78)
    clear()

if "tanean" in PARTS:
    # rumah tanean lanjang: a row of family houses facing a long yard, langgar (small prayer house on stilts) at the
    # west end, siwalan palms; gouache silhouettes in black/maroon over a hint of dusk wash.
    W, H = 1000, 360
    nx = Seq(30300); rng = random.Random(7)
    art = blank(W, H)
    ground = shapes(W, H, [[(-20, 318), (W + 20, 312), (W + 20, H + 10), (-20, H + 10)]], smooth=False)
    yard = shapes(W, H, [[(-20, 330), (W + 20, 326), (W + 20, H + 10), (-20, H + 10)]], smooth=False)
    # dusk glow behind
    sun = circles(W, H, [(700, 210, 70)])
    art = G(art, sun, "#e8833a", "#d6492f", seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=6, feather=3)
    houses = []
    roofs = []
    def house(x, w, h, roof_h, kind):
        base_y = 318
        body = [(x, base_y), (x, base_y - h), (x + w, base_y - h), (x + w, base_y)]
        houses.append(body)
        if kind == "pacenan":   # tall hipped roof with flared eaves
            roofs.append([(x - 18, base_y - h + 4), (x + w * 0.22, base_y - h - roof_h), (x + w * 0.78, base_y - h - roof_h), (x + w + 18, base_y - h + 4)])
        elif kind == "trompesan":  # two-tier roof
            roofs.append([(x - 16, base_y - h + 4), (x + w * 0.12, base_y - h - roof_h * 0.45), (x + w * 0.3, base_y - h - roof_h * 0.5), (x + w * 0.38, base_y - h - roof_h), (x + w * 0.62, base_y - h - roof_h), (x + w * 0.7, base_y - h - roof_h * 0.5), (x + w * 0.88, base_y - h - roof_h * 0.45), (x + w + 16, base_y - h + 4)])
        else:  # bangsal gable
            roofs.append([(x - 14, base_y - h + 4), (x + w / 2, base_y - h - roof_h), (x + w + 14, base_y - h + 4)])
    # langgar on stilts (west end)
    lx = 70
    stilts = polyline_mask(W, H, [[(lx + 6, 318), (lx + 6, 262)], [(lx + 74, 318), (lx + 74, 262)], [(lx + 40, 318), (lx + 40, 262)]], 5)
    houses.append([(lx - 4, 262), (lx - 4, 214), (lx + 84, 214), (lx + 84, 262)])
    roofs.append([(lx - 22, 218), (lx + 40, 160), (lx + 102, 218)])
    house(230, 150, 70, 64, "pacenan")
    house(420, 140, 66, 70, "trompesan")
    house(600, 150, 72, 62, "pacenan")
    house(790, 130, 62, 56, "bangsal")
    body = shapes(W, H, houses, smooth=False)
    roof = shapes(W, H, roofs, smooth=False)
    # palms (siwalan / lontar fan palms)
    import _jw_lib as jw
    def lontar(px, ph, lean):
        top = (px + lean * ph, 318 - ph)
        trunk = [(px, 318), (px + lean * ph * 0.4, 318 - ph * 0.5), top]
        items = [(curve(trunk, 20), 7, (0.0, 0.3))]
        rr = random.Random(int(px))
        for k in range(26):
            a = -math.pi + k / 25 * math.pi + rr.gauss(0, 0.05)
            L = rr.uniform(34, 44)
            items.append(([top, (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.9)], 4.2, (0.0, 0.7)))
        for k in range(6):
            a = 0.3 + k * 0.48
            items.append(([top, (top[0] + math.cos(a) * 30, top[1] + math.sin(a) * 26)], 3, (0.0, 0.7)))
        return strokes(W, H, items)
    pm = np.maximum.reduce([lontar(px, ph, lean) for (px, ph, lean) in [(176, 196, -0.05), (580, 236, 0.04), (950, 206, -0.07)]])
    porch = polyline_mask(W, H, [[(x, 318), (x, 300)] for (x0, w) in [(230, 150), (420, 140), (600, 150), (790, 130)] for x in (x0 - 8, x0 + w + 8)], 3)
    ridge = polyline_mask(W, H, [[(x - 6, y), (x + 6, y - 12)] for (x, y) in [(263, 184), (347, 184), (473, 180), (507, 180), (633, 184), (717, 184)]], 3)
    stilts = np.maximum.reduce([stilts, porch, ridge])
    sil = np.clip(np.maximum.reduce([body, roof, stilts, pm * 0.98, ground]), 0, 1)
    art = GP(art, sil, "#2a1210", INK, seed=nx(), rough=1.6, streak=0.9, pad=12)
    # roof tiles warm red catching the dusk light on the upper edge
    lit = np.clip(roof - np.roll(gaussian_filter(roof, 3), 6, 0), 0, 1) * roof
    art = G(art, np.clip(lit * 1.6, 0, 1), RED_L, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=1.5)
    tiles = roof * hatch(W, H, 0.0, 6, 0.2, nx(), 0.6)
    art = G(art, tiles, "#5a1a16", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    # lit doors/windows (warm lamp)
    wins = []
    for (x, w) in [(230, 150), (420, 140), (600, 150), (790, 130)]:
        wins.append([(x + w * 0.42, 318), (x + w * 0.42, 280), (x + w * 0.58, 280), (x + w * 0.58, 318)])
        wins.append([(x + w * 0.14, 300), (x + w * 0.14, 284), (x + w * 0.28, 284), (x + w * 0.28, 300)])
        wins.append([(x + w * 0.72, 300), (x + w * 0.72, 284), (x + w * 0.86, 284), (x + w * 0.86, 300)])
    wm = shapes(W, H, wins, smooth=False)
    art = GP(art, wm, YEL, "#f2cd6a", seed=nx(), rough=0.8, pad=6)
    art = OV(art, wm, lambda m: glow(m, "#f5b74a", radius=6, strength=0.5))
    # red-white striped door curtains (a Sakera nod) on the langgar
    lw = shapes(W, H, [[(lx + 28, 258), (lx + 28, 226), (lx + 52, 226), (lx + 52, 258)]], smooth=False)
    art = GP(art, lw, YEL, seed=nx(), rough=0.6, pad=6)
    # long yard (tanean): pale dusty strip
    art = GP(art, yard, "#3a1a14", "#26100c", seed=nx(), rough=1.4, pad=10)
    preview(art, "ms-tanean", bg="#7d1418")
    save(art, f"{OUT}/tanean.webp", max_w=780, quality=80)
    clear()

if "flower" in PARTS:
    # one batik flower emblem, opaque dyed on a cut piece of dark cloth? no: transparent, colours as dyed fields + wax lines
    W, H = 440, 440
    nx = Seq(30400); rng = random.Random(3)
    cx, cy, r = 220, 210, 120
    pet = shapes(W, H, flower_polys(cx, cy, r, 6, 0.26, rng))
    hrt = circles(W, H, [(cx, cy, r * 0.33)])
    lv = shapes(W, H, [deform(petal_pts(cx, cy + 40, 200, 56, math.pi * 0.78, n=16, cup=-0.3), rng, 1, 0.03),
                       deform(petal_pts(cx, cy + 40, 200, 56, math.pi * 0.22, n=16, cup=0.3), rng, 1, 0.03)])
    ground = circles(W, H, [(cx, cy + 6, 196)]) * 0
    art = blank(W, H)
    art = GP(art, np.clip(lv - pet, 0, 1), GRN, GRN_D, seed=nx(), rough=1.4, streak=0.8)
    art = GP(art, pet, RED, RED_D, seed=nx(), rough=1.4, streak=0.8)
    shade = pet * np.clip(1 - gaussian_filter(hrt, 18) * 3, 0, 1) * np.clip((fbm(W, H, nx(), 24, 3) - 0.4) * 2, 0, 1)
    art = G(art, shade, RED_D, seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=2)
    art = GP(art, hrt, YEL, YEL_D, seed=nx(), rough=1.0)
    art = GP(art, circles(W, H, [(cx, cy, r * 0.14)]), RED_D, seed=nx(), rough=0.6, pad=6)
    ol = np.maximum.reduce([outline(pet, 3.2), outline(np.clip(lv - pet, 0, 1), 3), outline(hrt, 2.6)])
    ol *= np.clip((fbm(W, H, nx(), 8, 2) - 0.08) * 6, 0, 1)
    art = over(art, flat(ol, CREAM, 0.95))
    dts = []
    for k in range(6):
        a = 0.26 + k * math.tau / 6
        for t in (0.5, 0.66, 0.82):
            dts.append((cx + math.cos(a) * r * t, cy + math.sin(a) * r * t, 3.4))
    for k in range(14):
        a = k * math.tau / 14
        dts.append((cx + math.cos(a) * r * 0.24, cy + math.sin(a) * r * 0.24, 2.2))
    art = GP(art, circles(W, H, dts), CREAM, seed=nx(), rough=0.4, pad=6)
    veins = [[(cx + math.cos(a) * L * t, cy + 40 + math.sin(a) * L * t) for t in (0.3, 0.6, 0.95)] for a, L in ((math.pi * 0.78, 200), (math.pi * 0.22, 200))]
    art = over(art, flat(wax_line(W, H, veins, 2.4, nx()), YEL, 0.95))
    preview(art, "ms-flower", bg=INK)
    save(art, f"{OUT}/flower.webp", max_w=260, quality=82)
    clear()

if "divider" in PARTS:
    # heavy brush bar in black with a red-white striped band and a small batik bud at its centre
    W, H = 620, 90
    nx = Seq(30500)
    bar = strokes(W, H, [(curve([(16, 48), (200, 44), (420, 47), (604, 44)], 40), 14, (0.08, 0.1))])
    art = GP(blank(W, H), bar, INK, "#2a1210", seed=nx(), rough=1.6, streak=1.0, dry=0.2)
    band = strokes(W, H, [(curve([(60, 46), (300, 44), (560, 46)], 30), 5, (0.1, 0.1))])
    art = GP(art, band, RED, seed=nx(), rough=0.8, pad=6)
    cx = 310
    pet = shapes(W, H, flower_polys(cx, 45, 34, 6, 0.0, random.Random(5)))
    art = GP(art, circles(W, H, [(cx, 45, 40)]), INK, seed=nx(), rough=0.8, pad=6)
    art = GP(art, pet, RED, RED_D, seed=nx(), rough=0.8, pad=6)
    art = GP(art, circles(W, H, [(cx, 45, 11)]), YEL, seed=nx(), rough=0.5, pad=6)
    art = over(art, flat(outline(pet, 1.8), CREAM, 0.95))
    preview(art, "ms-divider", "#f3e6cc")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
