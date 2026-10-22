"""Mashrabiya Kayu — turned-wood mashrabiya lattice (spindles, beads, cube knots, oiled walnut grain), warm light
filtering through, and the lattice's cast shadow on a sunlit plaster wall. Honey / walnut / cream.
Run: python3 -I mashrabiya-kayu.py [part ...]   parts: screen wall plaster band rosette panel
Assets -> public/themes/art/mashrabiya-kayu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b3_lib import *

OUT = outdir("mashrabiya-kayu")
PARTS = sys.argv[1:] or ["screen", "wall", "plaster", "band", "rosette", "panel"]
HONEY, WALNUT, DEEP, CREAM = "#d29a4e", "#7a4a26", "#3b2414", "#f4ead8"
W_LIGHT, W_MID, W_DARK = "#9a5c2c", "#4c2812", "#150803"


def lattice_masks(W, H, x0, y0, x1, y1, p, rod=6.0, bead=(17, 15.5), knot=13.0, ring=True):
    """Turned-wood mashrabiya: vertical + horizontal spindles with mid-span beads, collars, square knots at crossings.
    Returns (horizontal_mask, vertical_mask, knot_mask)."""
    cvh, cvv, cvk = Canvas(W, H), Canvas(W, H), Canvas(W, H)
    pt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    jr = random.Random(int(p * 7 + W))
    J = lambda a=0.9: jr.uniform(-a, a)
    xs = np.arange(x0, x1 + 0.1, p); ys = np.arange(y0, y1 + 0.1, p)
    for y in ys:
        cvh.c.drawRect(skia.Rect(x0, y - rod / 2, x1, y + rod / 2), pt)
        for x in xs[:-1]:
            mx = x + p / 2 + J(); k = 1 + J(0.07)
            cvh.c.drawOval(skia.Rect(mx - bead[0] / 2 * k, y - bead[1] / 2 * k, mx + bead[0] / 2 * k, y + bead[1] / 2 * k), pt)
            if ring:
                for dx in (-bead[0] / 2 - 2.6, bead[0] / 2 + 2.6):
                    cvh.c.drawOval(skia.Rect(mx + dx - 1.6, y - rod * 0.85, mx + dx + 1.6, y + rod * 0.85), pt)
    for x in xs:
        cvv.c.drawRect(skia.Rect(x - rod / 2, y0, x + rod / 2, y1), pt)
        for y in ys[:-1]:
            my = y + p / 2 + J(); k = 1 + J(0.07)
            cvv.c.drawOval(skia.Rect(x - bead[1] / 2 * k, my - bead[0] / 2 * k, x + bead[1] / 2 * k, my + bead[0] / 2 * k), pt)
            if ring:
                for dy in (-bead[0] / 2 - 2.6, bead[0] / 2 + 2.6):
                    cvv.c.drawOval(skia.Rect(x - rod * 0.85, my + dy - 1.6, x + rod * 0.85, my + dy + 1.6), pt)
    for x in xs:
        for y in ys:
            r = skia.RRect.MakeRectXY(skia.Rect(x - knot / 2, y - knot / 2, x + knot / 2, y + knot / 2), 2.5, 2.5)
            cvk.c.drawRRect(r, pt)
    sd = int(p * 3 + H)
    return tuple(np.clip(displace(cv.array()[..., 3], sd + i, 0.7, 14), 0, 1) for i, cv in enumerate((cvh, cvv, cvk)))


def paint_lattice(base, region, hm, vm, km, seed, light=(-0.6, -0.8)):
    """Wood render of the three lattice layers clipped to region, over base."""
    hm = hm * region; vm = vm * region; km = km * region
    allm = np.clip(hm + vm + km, 0, 1)
    out = base
    for m, along, sd, rad, prof in ((vm, "y", seed, 3.6, "round"), (hm, "x", seed + 1, 3.6, "round"), (km, "x", seed + 2, 3.2, "flat")):
        b = bbox(m, 4)
        if b is None:
            continue
        y0, y1, x0, x1 = b
        mm = np.ascontiguousarray(m[y0:y1, x0:x1])
        hg = height_of(mm, rad, prof)
        aom = np.ascontiguousarray(allm[y0:y1, x0:x1]) if prof == "round" else None
        layer = wood(mm, hg, W_LIGHT, W_MID, W_DARK, seed=sd, along=along, lightdir=light, depth=2.2, gloss=0.3, ao_mask=aom)
        o = out.copy(); o[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], layer); out = o
        trim_cache()
    return out


def backlight(W, H, seed, warm="#e8963a", hot="#ffe6aa", edge="#8a4216", cx=0.35, cy=0.25):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx / W - cx) / 0.9) ** 2 + ((yy / H - cy) / 1.1) ** 2)
    n = fbm(W, H, seed, 70, 3)
    t = np.clip(d * 1.7 + (n - 0.5) * 0.6 - 0.05, 0, 1)
    rgb = np.where(t[..., None] < 0.5, lerp3(C(hot), C(warm), t * 2), lerp3(C(warm), C(edge), (t - 0.5) * 2))
    return rgba(rgb, np.ones((H, W), np.float32))


def bloom_over(arr, light_mask, col="#ffe3a8", radius=3.0, amt=0.5):
    """Backlight spilling over thin wood edges (light wraps the spindles)."""
    g = np.clip(gaussian_filter(light_mask, radius) * amt, 0, 1)
    out = arr.copy()
    out[..., :3] = out[..., :3] * (1 - g[..., None]) + C(col) * g[..., None]
    return out


def frame_masks(W, H, outer, inner_rects, t):
    """Board frame: outer rect minus inner openings (list of rects)."""
    def draw(cv):
        p = skia.Path(); p.setFillType(skia.PathFillType.kEvenOdd)
        p.addRect(skia.Rect(*outer))
        for r in inner_rects:
            p.addRect(skia.Rect(*r))
        cv.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def carved_board(mask, seed, along="x", grooves=None):
    hg = height_of(mask, 7, "flat") * 1.0
    if grooves is not None:
        hg = hg - gaussian_filter(grooves, 0.9) * 3.2
    return wood(mask, hg, "#b77a40", "#6e3f1e", "#2c150a", seed=seed, along=along, depth=1.1, gloss=0.16)


if "screen" in PARTS:
    # The cover window: carved board frame, lattice transom with an ogee-arched opening, lattice side columns and
    # apron; the photo shows through the opening (transparent), warm light glows behind the lattice.
    W, H = 720, 900
    fr = 30
    ox0, ox1, oy0, oy1 = 132, W - 132, 214, 770   # photo opening
    rng = random.Random(3)
    # opening outline: straight sides, ogee/pointed top
    cx = W / 2
    top = [(ox0, oy1), (ox0, oy0 + 40)]
    top += bez((ox0, oy0 + 40), (ox0, oy0 - 30), (cx - 60, oy0 - 26), (cx, oy0 - 96), 30)[1:]
    top += bez((cx, oy0 - 96), (cx + 60, oy0 - 26), (ox1, oy0 - 30), (ox1, oy0 + 40), 30)[1:]
    top += [(ox1, oy1)]
    opening = shape_mask(W, H, top, smooth=False)
    inner = np.zeros((H, W), np.float32); inner[fr:H - fr, fr:W - fr] = 1
    inner = gaussian_filter(inner, 0.6)
    lat_region = np.clip(inner - gaussian_filter(opening, 0.6) * 1.0, 0, 1)
    # band of carved trim around the opening
    trim = np.clip(gaussian_filter((ndi.binary_dilation(opening > 0.5, iterations=14)).astype(np.float32), 0.7) - opening, 0, 1) * inner
    lat_region = np.clip(lat_region - trim, 0, 1)
    # mid rail between transom & sides gives the structure
    art = backlight(W, H, 7)
    art[..., 3] = inner
    hm, vm, km = lattice_masks(W, H, fr - 2, fr - 2, W - fr + 2, H - fr + 2, 34)
    art = paint_lattice(art, lat_region, hm, vm, km, 11)
    lightm = (art[..., 3] > 0) * 1.0
    art = bloom_over(art, lat_region * (1 - np.clip(hm + vm + km, 0, 1)), radius=1.6, amt=0.55)
    # trim: carved half-round moulding around opening
    hg = height_of(trim, 7, "round")
    tw = wood(trim, hg, "#bf8446", "#73421f", "#2c150a", seed=21, along="y", depth=1.2, gloss=0.2)
    art = over(art, tw)
    # outer frame boards + groove line
    frame = frame_masks(W, H, (0, 0, W, H), [(fr, fr, W - fr, H - fr)], fr)
    groove = frame_masks(W, H, (8, 8, W - 8, H - 8), [(10.5, 10.5, W - 10.5, H - 10.5)], 2)
    art = over(art, carved_board(frame, 31, "y", groove))
    # small carved rosette knobs at the four corners
    for (x, y) in [(fr / 2, fr / 2), (W - fr / 2, fr / 2), (fr / 2, H - fr / 2), (W - fr / 2, H - fr / 2)]:
        k = circle_mask(W, H, x, y, 13)
        hk = height_of(k, 9, "round")
        art = over(art, wood(k, hk, "#d39a58", "#7f4b25", "#2c150a", seed=41, depth=1.6, gloss=0.3))
    # clear the photo opening fully
    art[..., 3] *= 1 - opening
    art = add_grain(art, 3, 0.015)
    preview(art, "mk-screen", bg="#e6d6bb")
    save_full(art, f"{OUT}/screen.webp", size=(640, 800), quality=80)
    clear()

if "wall" in PARTS:
    # Sunlit plaster wall: a slanted patch of warm light with the lattice's soft cast shadow inside it.
    W, H = 780, 1180
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n1 = fbm(W, H, 5, 120, 4); n2 = fbm(W, H, 6, 18, 3)
    base = lerp3(C("#e7d5b6"), C("#d3bb95"), np.clip(n1 * 0.9 + (yy / H) * 0.3, 0, 1))
    base = base * (0.97 + 0.05 * n2[..., None])
    # trowel marks: broad soft arcs
    tr = gaussian_filter(np.random.default_rng(8).random((H, W)).astype(np.float32), (3, 26))
    tr = (tr - tr.mean()) / (tr.std() + 1e-6)
    base = base * (1 + tr[..., None] * 0.012)
    # light patch: projected window (parallelogram skewed to the right/down)
    big = 1500
    hm, vm, km = lattice_masks(big, big, 0, 0, big, big, 46, rod=7, bead=(20, 14), knot=15)
    lat = np.clip(hm + vm + km, 0, 1)
    # projection: shear x by +0.45*y, stretch y by 1.18, slight rotation
    sh, sy, rot = 0.42, 1.2, -0.06
    X = xx - W * 0.05; Y = yy + 40
    u = (X - Y * sh) * math.cos(rot) - Y * math.sin(rot) + 120
    v = (Y / sy) + X * math.sin(rot) * 0.3 + 90
    shadow_sharp = map_coordinates(lat, [v, u], order=1, mode="constant")
    shadow = gaussian_filter(shadow_sharp, 1.4) * (1 - yy / H)[..., None][..., 0] + gaussian_filter(shadow_sharp, 3.4) * (yy / H)
    # patch outline in (u, v) space: window from u 40..640 v 30..860 (with ogee top)
    px0, px1, py0, py1 = 60, 690, 40, 720
    inside = ((u > px0) & (u < px1) & (v > py0) & (v < py1)).astype(np.float32)
    cxu = (px0 + px1) / 2
    arch = v < py0 + 160 - 150 * (1 - np.clip(np.abs(u - cxu) / ((px1 - px0) / 2), 0, 1)) ** 0.6
    inside = inside * (1 - arch)
    patch = gaussian_filter(inside, 6) * (0.75 + 0.25 * fbm(W, H, 9, 80, 2))
    light = patch * (1 - shadow * 0.92)
    warm = C("#ffd890")
    rgb = base + light[..., None] * (warm - base) * 0.78 + light[..., None] * 0.07
    # the shadow inside the patch is cool and slightly blue-brown (sky fill)
    sh_in = patch * shadow
    rgb = rgb * (1 - sh_in[..., None] * 0.06)
    # very faint ambient falloff to the edges + warm bounce at the bottom
    d = np.sqrt(((xx - W * 0.55) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    rgb = rgb * (1 - 0.1 * np.clip(d, 0, 1))[..., None]
    arr = rgba(rgb, np.ones((H, W), np.float32))
    arr = add_grain(arr, 11, 0.025)
    rgb_save(arr, f"{OUT}/wall.webp", quality=76, size=(624, 944))
    to_image(arr).convert("RGB").save(f"{PREV}/mk-wall.png")
    clear()

if "plaster" in PARTS:
    S = 512
    n1 = noise(S, S, 3, 40, wrap=True); n2 = noise(S, S, 4, 6, wrap=True); n3 = noise(S, S, 5, 1.2, wrap=True)
    rgb = lerp3(C("#f4ead8"), C("#eadbc1"), np.clip(n1 * 1.1 - 0.05, 0, 1))
    rgb = rgb * (0.985 + 0.02 * n2[..., None] + 0.015 * n3[..., None])
    arr = rgba(rgb, np.ones((S, S), np.float32))
    rgb_save(arr, f"{OUT}/plaster.webp", quality=72)
    clear()

if "band" in PARTS:
    # Divider: one turned spindle lying flat — beads, collars and baluster swells growing toward a carved centre knot.
    W, H = 600, 80
    cy = H / 2
    cv = Canvas(W, H); pt = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    cv.c.drawRect(skia.Rect(14, cy - 3.2, W - 14, cy + 3.2), pt)
    rngb = random.Random(4)
    for side in (-1, 1):
        x = W / 2 + side * 44
        k = 0
        while 30 < x < W - 30:
            t = abs(x - W / 2) / (W / 2)
            r = 11.5 * (1 - t * 0.6) + rngb.uniform(-0.4, 0.4)
            if k % 2 == 0:
                cv.c.drawOval(skia.Rect(x - r * 1.25, cy - r, x + r * 1.25, cy + r), pt)
                step = r * 1.25 + 4
            else:
                cv.c.drawOval(skia.Rect(x - 2.2, cy - r * 0.62, x + 2.2, cy + r * 0.62), pt)
                step = 2.2 + 4
            x += side * (step + (r * 1.25 if k % 2 == 1 else 0) + 3)
            k += 1
    for x in (16, W - 16):
        cv.c.drawCircle(x, cy, 7.5, pt)
    m = cv.array()[..., 3]
    knot = circle_mask(W, H, W / 2, cy, 30)
    m = np.clip(m - gaussian_filter((ndi.binary_dilation(knot > 0.5, iterations=3)).astype(np.float32), 0.5), 0, 1)
    art = wood(m, height_of(m, 9, "round"), W_LIGHT, W_MID, W_DARK, seed=51, along="x", depth=1.8, gloss=0.3)
    groove = poly_lines(W, H, [star_pts(W / 2, cy, 24, 24 * 0.62, 8, math.pi / 8), star_pts(W / 2, cy, 24, 24 * 0.62, 8, 0)], 1.8)
    art = over(art, wood(knot, height_of(knot, 10, "round") - gaussian_filter(groove, 0.8) * 3, "#b47640", "#5a3118", "#1e0d06", seed=57, depth=1.5, gloss=0.3))
    preview(art, "mk-band", bg="#f4ead8")
    save(art, f"{OUT}/band.webp", max_w=440, quality=84)
    clear()

if "rosette" in PARTS:
    # Carved wooden medallion: 8-point star with an interlaced ring and chip-carved petals.
    S = 300; cx = cy = S / 2
    disc = circle_mask(S, S, cx, cy, 140)
    groove = np.zeros((S, S), np.float32)
    star = star_pts(cx, cy, 112, 112 * 0.62, 8, math.pi / 8)
    star2 = star_pts(cx, cy, 112, 112 * 0.62, 8, 0)
    groove = np.maximum(groove, poly_lines(S, S, [star, star2], 4.2))
    groove = np.maximum(groove, ring_mask(S, S, cx, cy, 128, 3.2))
    groove = np.maximum(groove, ring_mask(S, S, cx, cy, 44, 3.0))
    petals = []
    for k in range(8):
        a = k * math.pi / 4
        petals.append(petal_pts(cx + math.cos(a) * 8, cy + math.sin(a) * 8, 30, 11, a))
    pm = shapes(S, S, petals)
    hg = height_of(disc, 16, "round") - gaussian_filter(groove, 1.0) * 6 - gaussian_filter(pm, 1.2) * 4.5
    art = wood(disc, hg, "#cf9455", "#7a4622", "#2c150a", seed=71, depth=1.3, gloss=0.25)
    art = add_grain(art, 5, 0.03)
    preview(art, "mk-rosette", tone="#efe2cc")
    save(art, f"{OUT}/rosette.webp", max_w=220, quality=84)
    clear()

if "panel" in PARTS:
    # Free-standing mashrabiya panel (hero + closing): framed lattice with a carved rosette boss at the centre,
    # warmly backlit.
    W, H = 460, 640
    fr = 20
    art = backlight(W, H, 17, cx=0.5, cy=0.35)
    inner = np.zeros((H, W), np.float32); inner[fr:H - fr, fr:W - fr] = 1
    # arched top: cut the panel into a rounded-top shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shape = ((yy > 150) | (((xx - W / 2) / (W / 2)) ** 2 + ((yy - 150) / 150) ** 2 < 1)).astype(np.float32)
    shape = gaussian_filter(shape, 0.6)
    inner_shape = ((yy > 150) | (((xx - W / 2) / (W / 2 - fr)) ** 2 + ((yy - 150) / (150 - fr)) ** 2 < 1)).astype(np.float32) * inner
    inner_shape = gaussian_filter(inner_shape, 0.6)
    art[..., 3] = shape
    hm, vm, km = lattice_masks(W, H, fr - 13, fr - 13, W, H, 32, rod=4.6, bead=(14, 10), knot=10)
    boss = circle_mask(W, H, W / 2, 330, 62)
    region = np.clip(inner_shape - gaussian_filter((ndi.binary_dilation(boss > 0.5, iterations=6)).astype(np.float32), 0.6), 0, 1)
    art = paint_lattice(art, region, hm, vm, km, 81)
    art = bloom_over(art, region * (1 - np.clip(hm + vm + km, 0, 1)), radius=1.6, amt=0.55)
    frame = np.clip(shape - inner_shape, 0, 1)
    art = over(art, carved_board(frame, 91, "y"))
    # boss: reuse rosette carving
    groove = poly_lines(W, H, [star_pts(W / 2, 330, 52, 52 * 0.62, 8, math.pi / 8), star_pts(W / 2, 330, 52, 52 * 0.62, 8, 0)], 3.0)
    groove = np.maximum(groove, ring_mask(W, H, W / 2, 330, 20, 2.4))
    ring = np.clip(gaussian_filter((ndi.binary_dilation(boss > 0.5, iterations=6)).astype(np.float32), 0.6) - boss, 0, 1) * region.max()
    art = over(art, wood(boss, height_of(boss, 12, "round") - gaussian_filter(groove, 1) * 4.5, "#cf9455", "#7a4622", "#2c150a", seed=95, depth=1.3, gloss=0.25))
    art = add_grain(art, 7, 0.015)
    preview(art, "mk-panel", bg="#3b2414")
    save(art, f"{OUT}/panel.webp", max_w=380, quality=80)
    clear()

report(OUT)
