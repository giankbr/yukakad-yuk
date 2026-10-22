"""Bali Gringsing — Tenganan double-ikat (geringsing) cloth at thread level, Bali Aga stone village of bale with
alang-alang roofs, woven medallion + border band. Original geometric/floral gringsing-inspired motifs (no wayang).
Run: python3 -I bali-gringsing.py [part ...]   parts: kain tepi bintang desa"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d1_lib import *
from _jw_lib import hills as jw_hills

OUT = outdir("bali-gringsing")
PARTS = sys.argv[1:] or ["kain", "tepi", "bintang", "desa"]
# madder red, near-black (indigo over red), ecru, rust-brown
PAL = ["#72231a", "#24130f", "#e9d8b4", "#a8432a", "#4a1a12"]
RED, BLK, CRM, RUST, DRED = range(5)


def star4(c, cx, cy, r, inner=0.38, rot=0.0):
    pts = []
    for i in range(8):
        a = rot + i * math.pi / 4
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def design(N=120):
    def lay(draw):
        return wrap_draw(N, N, draw)
    layers = []
    c0 = N / 2
    # dotted lozenge lattice (lines of ecru dots running diagonally)
    def dots(c, p):
        for k in range(0, N, 6):
            for (x, y) in [(k, k), (k, N - k)]:
                c.drawCircle(x + 0.5, y + 0.5, 1.3, p)
    layers.append((lay(dots), CRM))
    # big star (centre + corners): black outline, ecru body, red heart
    def big(c, p, r, inner):
        for (x, y) in [(c0, c0), (0, 0)]:
            c.drawPath(path_of(star4(c, x, y, r, inner)), p)
    layers.append((lay(lambda c, p: big(c, p, 40, 0.42)), BLK))
    layers.append((lay(lambda c, p: big(c, p, 34, 0.40)), CRM))
    layers.append((lay(lambda c, p: big(c, p, 25, 0.42)), RED))
    def ring(c, p, r):
        for (x, y) in [(c0, c0), (0, 0)]:
            c.drawCircle(x, y, r, p)
    layers.append((lay(lambda c, p: ring(c, p, 11)), BLK))
    # four-petal cempaka in the heart
    def petals(c, p, L, Wd, at):
        for (x, y) in at:
            for i in range(4):
                c.save(); c.translate(x, y); c.rotate(45 + 90 * i)
                c.drawOval(skia.Rect(1, -Wd, L, Wd), p); c.restore()
    layers.append((lay(lambda c, p: petals(c, p, 9, 3.2, [(c0, c0), (0, 0)])), CRM))
    layers.append((lay(lambda c, p: ring(c, p, 2.4)), RUST))
    # small flowers at the half-drop points, with a black ring of seeds
    sm = [(c0, 0), (0, c0)]
    def seedring(c, p):
        for (x, y) in sm:
            for i in range(12):
                a = i * math.tau / 12
                c.drawCircle(x + math.cos(a) * 15, y + math.sin(a) * 15, 1.6, p)
    def bigdia(c, p, r):
        for (x, y) in sm:
            c.drawPath(path_of([(x, y - r), (x + r, y), (x, y + r), (x - r, y)]), p)
    layers.append((lay(lambda c, p: bigdia(c, p, 27)), CRM))
    layers.append((lay(lambda c, p: bigdia(c, p, 24.5)), BLK))
    layers.append((lay(seedring), CRM))
    layers.append((lay(lambda c, p: [c.drawCircle(x, y, 11.5, p) for x, y in sm]), BLK))
    layers.append((lay(lambda c, p: petals(c, p, 11, 4.2, sm)), RUST))
    layers.append((lay(lambda c, p: petals(c, p, 6, 1.8, sm)), CRM))
    layers.append((lay(lambda c, p: [c.drawCircle(x, y, 1.8, p) for x, y in sm]), BLK))
    # little ecru diamonds between motifs
    def dia(c, p):
        for (x, y) in [(c0 / 2, c0 / 2), (c0 * 1.5, c0 / 2), (c0 / 2, c0 * 1.5), (c0 * 1.5, c0 * 1.5)]:
            c.drawPath(path_of([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)]), p)
    layers.append((lay(dia), BLK))
    layers.append((lay(lambda c, p: [c.drawPath(path_of([(x, y - 2.6), (x + 2.6, y), (x, y + 2.6), (x - 2.6, y)]), p) for (x, y) in [(c0 / 2, c0 / 2), (c0 * 1.5, c0 / 2), (c0 / 2, c0 * 1.5), (c0 * 1.5, c0 * 1.5)]]), CRM))
    return layer_index(RED, layers)


if "kain" in PARTS:
    D = design(120)
    cloth = ikat(D, PAL, p=4, mode="double", amp=2.1, coh=2.2, along=10, seed=11, bleed=0.6, slub=0.3, fibre=0.08)
    prev_rgb(cloth, "bg-kain")
    prev_rgb(tile_to(cloth, 960, 720), "bg-kain-rep")
    save_rgb_arr(cloth, f"{OUT}/kain.webp", quality=80)
    clear()


def band_design(N=120, Hh=26):
    """Border band: black/ecru stripes framing a row of small cempaka flowers on red (tileable along x)."""
    W, H = N, Hh
    layers = []
    def stripes(c, p):
        for y0, y1 in [(0, 2), (Hh - 2, Hh)]:
            c.drawRect(skia.Rect(-W, y0, 2 * W, y1), p)
    layers.append((wrap_draw(W, H, stripes), BLK))
    layers.append((wrap_draw(W, H, lambda c, p: [c.drawRect(skia.Rect(-W, y0, 2 * W, y1), p) for y0, y1 in [(3, 4), (Hh - 4, Hh - 3)]]), CRM))
    cy = Hh / 2
    xs = [k * 15 + 7.5 for k in range(N // 15)]
    def dias(c, p, r):
        for x in xs:
            c.drawPath(path_of([(x, cy - r), (x + r, cy), (x, cy + r), (x - r, cy)]), p)
    layers.append((wrap_draw(W, H, lambda c, p: dias(c, p, 8)), BLK))
    def pet(c, p, L, Wd):
        for x in xs:
            for i in range(4):
                c.save(); c.translate(x, cy); c.rotate(90 * i); c.drawOval(skia.Rect(0.5, -Wd, L, Wd), p); c.restore()
    layers.append((wrap_draw(W, H, lambda c, p: pet(c, p, 5.5, 2.0)), CRM))
    layers.append((wrap_draw(W, H, lambda c, p: [c.drawCircle(x, cy, 1.2, p) for x in xs]), RUST))
    layers.append((wrap_draw(W, H, lambda c, p: [c.drawCircle(x + 7.5, cy, 1.4, p) for x in xs]), CRM))
    return layer_index(RED, layers)


def fringe(W, top, L, seed, cloth, p=4):
    """Loose warp threads below the woven edge: every warp keeps its dye colour; groups twist into tassels."""
    rng = random.Random(seed)
    H = top + L + 12
    out = blank(W, H)
    out[:top, :, :3] = cloth[:top]
    out[:top, :, 3] = 1
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    per = 6
    groups = W // (p * per)
    cols = {}
    for g in range(groups):
        x0 = g * p * per + p * per / 2
        sway = rng.uniform(-5, 5)
        ln = L * rng.uniform(0.7, 1.0)
        knot = top + rng.uniform(5, 9)
        for k in range(per):
            xs = g * p * per + k * p + p / 2
            col = tuple(np.round((cloth[top // 2 + 6, int(xs)] * 0.6 + np.array(hex_rgb(PAL[0]), np.float32) * 0.4) * 16) / 16)
            pts = []
            for t in np.linspace(0, 1, 16):
                y = top - 1 + ln * t
                pull = min(1, max(0, (y - top) / max(1, knot - top)))
                x = xs + (x0 + (k - per / 2 + 0.5) * 0.9 - xs) * pull + sway * t * t + math.sin(t * 9 + k) * 0.6
                pts.append((x, y))
            cols.setdefault(col, []).append((pts, p * 0.55, (0.0, 0.25)))
        cols.setdefault(("knot",), []).append(([(x0 - 3.4, knot), (x0 + 3.4, knot)], 4.2, None))
    for col, items in cols.items():
        m = strokes(W, H, items)
        if col == ("knot",):
            c = cloth[top - 3, :].mean(0) * 0.7
            lay = rgba(np.ones((H, W, 3), np.float32) * c, m * 0.95)
        else:
            tw = 0.78 + 0.28 * np.sin(yy / 1.7 + xx * 1.3)
            lay = rgba(np.ones((H, W, 3), np.float32) * np.array(col, np.float32) * tw[..., None], m)
        out = over(out, lay)
    return out


if "tepi" in PARTS:
    D = band_design(120, 26)
    cloth = ikat(D, PAL, p=4, mode="double", amp=1.2, coh=2.0, along=10, seed=21, bleed=0.5, slub=0.3, fibre=0.08)
    # extra plain red rows above (the band sits at the cloth's lower end)
    top = cloth.shape[0]
    f = fringe(cloth.shape[1], top, 46, 5, cloth)
    preview(f, "tepi", bg="#efe4cc")
    save_full(f, f"{OUT}/tepi.webp", quality=82)
    clear()

def rosette(N=96):
    """Non-tiling medallion design: gringsing star rosette; returns (index map, alpha design)."""
    c0 = N / 2
    lays = []
    pd = lambda f: plain_draw(N, N, f)
    lays.append((pd(lambda c, p: c.drawPath(path_of(star4(None, c0, c0, 47, 0.58, -math.pi / 2)), p)), BLK))
    lays.append((pd(lambda c, p: c.drawPath(path_of(star4(None, c0, c0, 42, 0.56, -math.pi / 2)), p)), CRM))
    lays.append((pd(lambda c, p: c.drawPath(path_of(star4(None, c0, c0, 37, 0.55, -math.pi / 2)), p)), RED))
    lays.append((pd(lambda c, p: [c.drawCircle(c0 + math.cos(a) * 24, c0 + math.sin(a) * 24, 1.7, p) for a in np.linspace(0, math.tau, 17)[:-1]]), CRM))
    lays.append((pd(lambda c, p: c.drawCircle(c0, c0, 17, p)), BLK))
    def pet(c, p, L, Wd, rot):
        for i in range(4):
            c.save(); c.translate(c0, c0); c.rotate(rot + 90 * i); c.drawOval(skia.Rect(1, -Wd, L, Wd), p); c.restore()
    lays.append((pd(lambda c, p: pet(c, p, 15, 5.2, 45)), RUST))
    lays.append((pd(lambda c, p: pet(c, p, 9, 2.4, 45)), CRM))
    lays.append((pd(lambda c, p: pet(c, p, 13, 1.6, 0)), CRM))
    lays.append((pd(lambda c, p: c.drawCircle(c0, c0, 2.6, p)), BLK))
    # tips: small black diamonds with ecru eyes at the four star points
    for a in range(4):
        ang = -math.pi / 2 + a * math.pi / 2
        x, y = c0 + math.cos(ang) * 33, c0 + math.sin(ang) * 33
        lays.append((pd(lambda c, p, x=x, y=y: c.drawPath(path_of([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)]), p)), BLK))
        lays.append((pd(lambda c, p, x=x, y=y: c.drawCircle(x, y, 1.4, p)), CRM))
    D = layer_index(5, lays)
    A = (D != 5).astype(np.int32)
    D[D == 5] = RED
    return D, A


def woven_cut(D, A, p, seed, **k):
    """Render a non-tiling design + its alpha through the same loom (identical dye offsets -> feathered edge)."""
    kw = dict(mode="double", amp=1.5, coh=2.0, along=10, seed=seed, tile=False)
    kw.update(k)
    cloth = ikat(D, PAL, p=p, bleed=0.55, slub=0.3, **kw)
    am = ikat(A, ["#000000", "#ffffff"], p=p, bleed=0, slub=0, fibre=0, thread_var=0, **kw)[..., 0]
    alpha = np.clip((am - 0.2) * 3.0, 0, 1)
    return cutout(cloth, alpha, shadow=0.28)


if "bintang" in PARTS:
    D, A = rosette(96)
    med = woven_cut(D, A, 4, 31)
    preview(med, "bintang")
    save(med, f"{OUT}/bintang.webp", max_w=280, quality=82)
    clear()


def hip_roof(W, H, cx, eave_y, w, rh, top_w, thick=14):
    """Thatched hip roof: body polygon + eave band."""
    body = [(cx - w / 2, eave_y), (cx - top_w / 2, eave_y - rh), (cx + top_w / 2, eave_y - rh), (cx + w / 2, eave_y)]
    eave = [(cx - w / 2 - 4, eave_y - 3), (cx + w / 2 + 4, eave_y - 3), (cx + w / 2 + 2, eave_y + thick), (cx - w / 2 - 2, eave_y + thick)]
    return body, eave


def paint_roof(art, W, H, cx, eave_y, w, rh, top_w, nx, rng, thick=14, base="#9a7a4c", dark="#5e4529", light="#c4a26a"):
    body, eave = hip_roof(W, H, cx, eave_y, w, rh, top_w, thick)
    bm = poly(W, H, deform(body, rng, 1, 0.01), smooth=False)
    em = poly(W, H, deform(eave, rng, 1, 0.01), smooth=False)
    art = GP(art, np.maximum(bm, em), base, dark, seed=nx(), rough=1.6, streak=1.0)
    # straw strokes, light from the left
    top = lambda x: eave_y - rh + max(0, abs(x - cx) - top_w / 2) * rh / max(1, (w - top_w) / 2)
    items = thatch_strokes(cx - w / 2, cx + w / 2, top, lambda x: eave_y + thick - 4, rng, dens=1.4, ln=(8, 18), slant=0.7)
    st = strokes(W, H, items) * np.maximum(bm, em)
    yy, xx = ygrid(W, H)
    art = G(art, st * (xx > cx), dark, seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.6, feather=0.6, gran=0.4)
    art = G(art, st * (xx <= cx) * 0.7, light, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.6, gran=0.4)
    # shade the right hip + eave underside
    rside = poly(W, H, [(cx + top_w / 2, eave_y - rh), (cx + w / 2, eave_y), (cx + w / 2 - 30, eave_y), (cx + top_w / 2 - 6, eave_y - rh)], smooth=False)
    art = G(art, rside, "#3c2a18", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2)
    art = G(art, em * (yy > eave_y + thick * 0.55), "#2e2116", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=1)
    # ridge cap (ijuk, black palm fibre)
    ridge = strokes(W, H, [([(cx - top_w / 2 - 2, eave_y - rh + 1), (cx + top_w / 2 + 2, eave_y - rh + 1)], 6, None)])
    art = GP(art, ridge, "#2b211a", "#43352a", seed=nx(), rough=1.0)
    return art


def stone_wall(art, W, H, pts, box, nx, seed, cell=13, col="#9b948a", col2="#b3a58e", moss=0.35):
    """River/field stones: tonal stones with a soft bevel (light from the upper left) and thin mortar."""
    m = poly(W, H, pts, smooth=False)
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.6)
    E = edge_field(W, H, box, cell, seed)
    Eb = gaussian_filter(np.clip(E / (cell * 0.45), 0, 1), 1.2)
    gy, gx = np.gradient(Eb)
    lit = np.clip(-(gx + gy) * 9, 0, 1) * m
    dark = np.clip((gx + gy) * 9, 0, 1) * m
    tone = stone_shade(W, H, box, cell, seed)
    art = G(art, m * (tone > 0.6) * 0.8, "#7a7368", seed=nx(), density=0.3, edge=0.15, bloom=0.3, rough=1.2, gran=0.5)
    art = G(art, m * (tone < 0.3) * 0.8, "#cdbfa3", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=1.2)
    art = G(art, dark, "#3f392f", seed=nx(), density=0.5, edge=0.0, bloom=0, rough=0.8, feather=0.8, gran=0.5)
    art = G(art, lit, "#ece2c8", seed=nx(), density=0.45, edge=0.0, bloom=0, rough=0.8, feather=0.8)
    art = G(art, m * np.clip(1 - E / 1.1, 0, 1), "#4d463c", seed=nx(), density=0.55, edge=0.0, bloom=0, rough=0.6, feather=0.5, gran=0.5)
    if moss:
        mf = fbm(W, H, seed + 3, 40, 3)
        art = G(art, m * np.clip((mf - 0.58) * 4, 0, 1), "#6f7c4c", seed=nx(), density=moss, edge=0.3, bloom=0.3, rough=2)
    return art


if "desa" in PARTS:
    W, H = 900, 600
    nx = Seq(70100); rng = random.Random(7)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    # pale morning sky wash, fading into the paper
    sky = poly(W, H, [(0, 40), (W, 20), (W, 300), (0, 300)], smooth=False) * np.clip((yy - 30) / 200, 0, 1)
    art = G(art, sky, "#e9dcc0", "#dfe3d2", seed=nx(), density=0.35, edge=0.0, bloom=0.4, rough=8, feather=8)
    # hills of Tenganan
    art = G(art, jw_hills(W, H, 215, 38, 3) * np.clip((420 - yy) / 140, 0, 1), "#9aa587", "#b2ae92", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=6)
    art = G(art, jw_hills(W, H, 262, 30, 9, 0.8) * np.clip((470 - yy) / 120, 0, 1), "#6c7d5a", "#7f8a62", seed=nx(), density=0.6, edge=0.4, bloom=0.35, rough=5)
    ridge = [(x, 250 + rng.uniform(-14, 6), rng.uniform(0.5, 0.9)) for x in range(230, 900, 34)]
    art = G(art, blobs(W, H, ridge, rng, (8, 14), 3), "#4e6340", "#3d5234", seed=nx(), density=0.6, edge=0.45, bloom=0.3, rough=3)
    # upper terrace: back row of bale roofs behind the wall
    for (cx, ey, w) in [(400, 322, 150), (585, 316, 160), (770, 320, 150)]:
        art = paint_roof(art, W, H, cx, ey, w, 44, w * 0.4, nx, rng, thick=10, base="#8f7448", dark="#5a4329", light="#b29468")
    # upper terrace wall with an angkul-angkul gate
    art = stone_wall(art, W, H, [(230, 336), (900, 330), (900, 378), (230, 384)], (230, 326, 900, 386), nx, 11, cell=11)
    gx = 470
    gate = poly(W, H, [(gx - 30, 382), (gx - 30, 318), (gx + 30, 318), (gx + 30, 382)], smooth=False)
    art = GP(art, gate, "#a3846a", "#8c705a", seed=nx(), rough=1.2)
    door = poly(W, H, [(gx - 15, 382), (gx - 15, 334), (gx + 15, 334), (gx + 15, 382)], smooth=False)
    art = GP(art, door, "#2e241d", "#3d3026", seed=nx(), rough=0.8)
    art = paint_roof(art, W, H, gx, 318, 92, 34, 26, nx, rng, thick=8)
    # terrace ground: trodden earth and grass between the walls
    gr = poly(W, H, [(0, 372), (W, 366), (W, 520), (0, 530)], smooth=False) * np.clip((540 - yy) / 60, 0, 1)
    art = G(art, gr, "#a3a476", "#b9ad86", seed=nx(), density=0.6, edge=0.3, bloom=0.45, rough=6)
    art = G(art, gr * np.clip((fbm(W, H, 91, 30, 3) - 0.55) * 3, 0, 1), "#7d8c55", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=3)
    # banyan (beringin) on the left: trunk splitting into limbs, aerial roots, big layered crown
    trunk = poly(W, H, [(84, 496), (106, 400), (112, 300), (96, 210), (70, 160), (88, 150), (120, 205), (134, 150), (150, 154), (146, 214), (178, 160), (196, 170), (160, 236), (158, 330), (164, 410), (192, 498)])
    roots = strokes(W, H, [(curve([(x, rng.uniform(150, 210)), (x + rng.uniform(-6, 6), 330), (x + rng.uniform(-10, 10), 488)], 16), rng.uniform(1.2, 2.4), (0.05, 0.1)) for x in list(range(40, 90, 11)) + list(range(176, 250, 12))])
    art = GP(art, np.maximum(trunk, roots * 0.85), "#6a5a49", "#4c3f33", seed=nx(), rough=1.4, streak=1.2)
    art = G(art, trunk * (xx > 136), "#3a2f26", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=2)
    art = G(art, trunk * (xx < 104), "#a8957c", seed=nx(), density=0.3, edge=0.0, bloom=0.2, rough=2)
    crown = [(rng.uniform(-20, 290), rng.uniform(50, 190), rng.uniform(0.9, 1.5)) for _ in range(18)]
    cm = blobs(W, H, crown, rng, (16, 30), 5)
    art = G(art, cm, "#4b6a3a", "#5f7a43", seed=nx(), density=0.78, edge=0.55, bloom=0.4, rough=5, gran=0.35)
    dk = blobs(W, H, [(x + 14, y + 22, s * 0.8) for x, y, s in crown], rng, (12, 22), 4) * cm
    art = G(art, dk, "#2b4428", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=4)
    lt = blobs(W, H, [(x - 16, y - 18, s * 0.5) for x, y, s in crown[::2]], rng, (8, 14), 3) * cm
    art = G(art, lt, "#93a35e", seed=nx(), density=0.45, edge=0.3, bloom=0.4, rough=3)
    front = blobs(W, H, [(80, 168, 0.8), (140, 140, 0.9), (196, 178, 0.7), (40, 196, 0.6)], rng, (12, 20), 5)
    art = G(art, front, "#3f5c33", "#56713f", seed=nx(), density=0.8, edge=0.5, bloom=0.35, rough=4, gran=0.35)
    art = G(art, blobs(W, H, [(70, 150, 0.4), (130, 124, 0.45)], rng, (8, 12), 3) * front, "#8fa05a", seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=3)
    # main bale on its stone platform (front right)
    cx = 665
    plat = [(460, 446), (880, 440), (880, 500), (460, 506)]
    art = stone_wall(art, W, H, plat, (456, 436, 884, 506), nx, 23, cell=15, moss=0.25)
    topf = poly(W, H, [(452, 440), (888, 434), (884, 448), (456, 452)], smooth=False)
    art = GP(art, topf, "#b9ac94", "#a59782", seed=nx(), rough=1)
    # under-roof shadow + back wall
    back = poly(W, H, [(490, 446), (490, 376), (842, 372), (842, 442)], smooth=False)
    art = GP(art, back, "#4a3a2c", "#3a2e24", seed=nx(), rough=1)
    # posts
    posts = shapes(W, H, [[(x - 5, 446), (x - 4, 372), (x + 4, 372), (x + 5, 446)] for x in (498, 580, 665, 750, 834)], smooth=False)
    art = GP(art, posts, "#7a5434", "#5e3f27", seed=nx(), rough=0.8, streak=1.2)
    # a gringsing cloth hung over the rail between two posts
    clothW, clothH = 150, 62
    kd = design(120)
    kc = ikat(kd, PAL, p=2, mode="double", amp=2.0, seed=41, bleed=0.6)
    cloth = np.zeros((H, W, 3), np.float32)
    ox, oy = 588, 388
    patch = kc[:clothH + 10, :clothW]
    # sag: shift columns down along a catenary
    for i in range(clothW):
        sag = int(8 * math.sin(math.pi * i / clothW))
        cloth[oy + sag: oy + sag + clothH, ox + i] = patch[:clothH, i]
    cm_ = poly(W, H, [(ox, oy)] + [(ox + i, oy + 8 * math.sin(math.pi * i / clothW)) for i in range(0, clothW + 1, 10)] + [(ox + clothW, oy + clothH)] + [(ox + i, oy + clothH + 8 * math.sin(math.pi * i / clothW) + (3 if (i // 10) % 2 else 0)) for i in range(clothW, -1, -10)], smooth=False)
    shade = 1 - 0.25 * np.clip((yy - oy) / clothH, 0, 1)
    art = over(art, rgba(cloth * shade[..., None], cm_ * 0.97))
    rail = strokes(W, H, [([(500, 390), (832, 386)], 3.5, None)])
    art = GP(art, rail, "#6b4a2e", seed=nx(), rough=0.6)
    art = paint_roof(art, W, H, cx, 374, 430, 82, 190, nx, rng, thick=16)
    # stone lane climbing to the gate, with low steps
    lane = [(250, 600), (600, 600), (500, 384), (440, 384)]
    lm = poly(W, H, lane, smooth=False)
    art = stone_wall(art, W, H, lane, (240, 380, 610, 600), nx, 31, cell=17, col="#a9a091", col2="#c2b59b", moss=0.15)
    curb = strokes(W, H, [([(250, 600), (440, 384)], 9, None), ([(600, 600), (500, 384)], 9, None)])
    art = G(art, curb, "#5f584c", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1.5)
    steps = strokes(W, H, [([(440 - (y - 384) * 0.88 + 6, y), (500 + (y - 384) * 0.46 - 4, y)], 2.2, None) for y in (412, 446, 488, 540)])
    art = G(art, steps * lm, "#5a5248", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1)
    # low walls in front (left) and grass verges
    art = stone_wall(art, W, H, [(0, 478), (246, 470), (230, 548), (0, 556)], (0, 466, 250, 556), nx, 41, cell=14)
    grass = []
    for _ in range(260):
        x = rng.uniform(0, W); y = rng.uniform(548, 600) if x < 260 or x > 590 else rng.uniform(500, 520) if x > 860 else None
        if y is None:
            continue
        a = -math.pi / 2 + rng.uniform(-0.5, 0.5); L = rng.uniform(8, 22)
        grass.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(1.2, 2.4), (0.0, 0.6)))
    gm = strokes(W, H, grass)
    art = G(art, gm, "#5c7340", "#7f8f4c", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=1, feather=0.6)
    vg = poly(W, H, [(600, 600), (612, 520), (900, 506), (900, 600)], smooth=False)
    art = G(art, vg, "#7c8c58", "#9a9c66", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=5)
    art = G(art, poly(W, H, [(0, 556), (246, 548), (250, 600), (0, 600)], smooth=False), "#7c8c58", "#8f9660", seed=nx(), density=0.5, edge=0.3, bloom=0.4, rough=5)
    # fade the bottom edge so the scene sits on the page
    art[..., 3] *= vignette_mask(W, H, 5, inset=8, rough=22, fade=26)
    preview(art, "desa", tone="#f2e8d2")
    save(art, f"{OUT}/desa.webp", max_w=800, quality=80)
    clear()
