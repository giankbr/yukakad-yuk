"""Lampu Mosaik — hanging Turkish-style mosaic glass lamps (original designs): globes, onions and tall drops built
from hundreds of small glass tesserae set in dark grout, lit from inside (hot core, cooler rim), pierced brass caps
and bottom finials, brass chains, soft coloured bloom. Night background, coloured light pools. No figures.
Run: python3 -I lampu-mosaik.py [part ...]
parts: lampA lampB lampC lampD pools divider rosette night. Assets -> public/themes/art/lampu-mosaik/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c3_lib import *

OUT = outdir("lampu-mosaik")
PARTS = sys.argv[1:] or ["lampA", "lampB", "lampC", "lampD", "pools", "divider", "rosette"]
NIGHT = "#140e22"
BRASS, BRASS_D = "#c89443", "#7a5422"
GROUT = "#241a14"
PAL = {  # roles: base, contrast, motif, pale accent, dark border, second motif
    "ruby": ["#b8203a", "#f0a83a", "#2a9c8f", "#f8e08a", "#6a1028", "#e8603a"],
    "teal": ["#1d6fb8", "#43c0b0", "#f2c14e", "#fff0c0", "#123a7a", "#e05a3a"],
    "amber": ["#e08a26", "#f8d468", "#c23a2e", "#fff1c2", "#7a3a12", "#3a9a6a"],
    "violet": ["#6a34a0", "#d0508a", "#f2b04a", "#fbe6b0", "#341a5a", "#3aa3c0"],
    "emerald": ["#2f8a52", "#9ad06a", "#f2c84b", "#fff0c0", "#164a32", "#d9533a"],
}


def body_poly(cx, cy, R, kind, n=90):
    """Glass body outline from a half-width profile w(s), s = -1 (top) .. 1 (bottom); returns pts, rx, ry."""
    rx, ry = {"globe": (R, R * 0.94), "tall": (R * 0.74, R * 1.3), "onion": (R, R * 1.1), "drop": (R, R * 1.15)}[kind]

    def prof(s):
        c = math.sqrt(max(0.0, 1 - s * s))
        if kind == "onion":
            c *= 0.62 + 0.38 * ((s + 1) / 2) ** 0.6
            c *= 1 - 0.45 * max(0.0, (-s - 0.45) / 0.55) ** 1.2
        elif kind == "drop":
            c *= 1 - 0.3 * ((s + 1) / 2) ** 1.4
            c *= 1 - 0.5 * max(0.0, (s - 0.5) / 0.5) ** 1.2
        elif kind == "tall":
            c = c ** 0.8
        return c
    ss = [-math.cos(math.pi * i / (n // 2)) for i in range(n // 2 + 1)]
    right = [(cx + rx * prof(s), cy + ry * s) for s in ss]
    left = [(cx - rx * prof(s), cy + ry * s) for s in ss[::-1]]
    return right + left[1:-1], rx, ry


def lamp(W, H, cx, chain_top, chain_len, R, kind, pal, seed, cell=None, bloom=1.0):
    """Render one lamp (chain + cap + mosaic glass + bottom finial) with its glow. Returns RGBA."""
    rng = np.random.default_rng(seed)
    nx = Seq(seed * 7)
    cap_y = chain_top + chain_len
    pts, rx, ry = body_poly(cx, 0, R, kind)
    top_off = min(p[1] for p in pts)
    cy = cap_y + R * 0.16 - top_off
    pts = [(x, y + cy) for x, y in pts]
    body = shapes(W, H, [pts], smooth=True)
    body = np.clip((gaussian_filter(body, 0.8) - 0.1) * 1.3, 0, 1)
    # --- tesserae on a sphere-mapped grid (cells shrink toward the rim)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = np.clip((xx - cx) / rx, -0.999, 0.999)
    v = np.clip((yy - cy) / ry, -0.999, 0.999)
    U = np.arcsin(u) * rx * 0.86
    V = np.arcsin(v) * ry * 0.86
    cell = cell or max(5.5, R / 17)
    gpts = []
    for j, y in enumerate(np.arange(-ry * 1.5, ry * 1.5, cell * 0.86)):
        off = (j % 2) * cell / 2
        for x in np.arange(-rx * 1.5 + off, rx * 1.5, cell):
            gpts.append((x + rng.uniform(-.38, .38) * cell, y + rng.uniform(-.38, .38) * cell))
    gpts = np.array(gpts, np.float32)
    tree = cKDTree(gpts)
    sel = body > 0.01
    q = np.stack([U[sel], V[sel]], -1)
    d, lab = tree.query(q, k=2)
    lab0 = lab[:, 0]
    gap = d[:, 1] - d[:, 0]
    scale = np.sqrt(np.clip(1 - u[sel] ** 2, 0.05, 1))  # grout narrows to the rim
    grout = np.clip((1.9 * scale + 0.3 - gap) / 0.8, 0, 1)
    # --- per-tessera colour from a banded pattern (zigzag bands, diamonds, rosette field)
    gu, gv = gpts[:, 0] / rx, gpts[:, 1] / ry
    nb = 2.3 if kind != "tall" else 3.0
    band = np.floor((gv + 1.25) * nb / 2.5 * 2).astype(int)
    f = (gv + 1.25) * nb / 2.5 * 2 - band
    fi = np.clip((f - 0.1) / 0.8, 0, 1)
    pal_c = np.array([hex_rgb(c) for c in pal], np.float32)
    bt = band % 3
    tri = np.abs(((gu * 3.2 + 40) % 2) - 1)
    zz = np.where(fi > tri * 0.8 + 0.1, 0, 1)
    du = np.abs(((gu * 1.9 + 40) % 1) - 0.5) * 2
    dd = du + np.abs(fi - 0.5) * 2
    dia = np.where(dd < 0.22, 3, np.where(dd < 0.62, 2, 0))
    dc = np.hypot(((gu * 2.3 + 40) % 1) - 0.5, (fi - 0.5) * 0.75)
    cir = np.where(dc < 0.13, 3, np.where(dc < 0.3, 5, 1))
    idx = np.where(bt == 0, zz, np.where(bt == 1, dia, cir))
    border = (f < 0.1) | (f > 0.9)
    alt = (np.floor(gu * 9 + 40).astype(int) % 2)
    idx = np.where(border, np.where(alt == 0, 3, 4), idx)
    rnd = rng.random(len(gpts))
    idx = np.where(rnd < 0.025, rng.integers(0, len(pal), len(gpts)), idx)
    cols = pal_c[idx % len(pal)]
    cols *= (0.88 + 0.2 * rng.random((len(gpts), 1))).astype(np.float32)
    clear_ = rnd > 0.988
    cols[clear_] = np.array(hex_rgb("#fff2cf"), np.float32)
    rgb_t = cols[lab0]
    # inner light: hot core, sphere falloff, slight top shadow under the cap
    r2 = np.clip(u[sel] ** 2 + v[sel] ** 2, 0, 1)
    core = np.exp(-(((xx[sel] - cx) / (rx * 0.55)) ** 2 + ((yy[sel] - cy - ry * 0.1) / (ry * 0.6)) ** 2))
    lum = 0.45 + 0.62 * (1 - r2) ** 0.7 + 0.25 * core
    lum *= 1 - 0.3 * np.clip(-(v[sel]) - 0.55, 0, 1) * 2
    tex = fbm(W, H, seed + 3, 6, 2)[sel]
    lum *= 0.9 + 0.22 * tex
    glass_rgb = np.clip(rgb_t * lum[:, None] + core[:, None] * 0.1 * np.array([1, .85, .55], np.float32), 0, 1)
    gr = np.array(hex_rgb(GROUT), np.float32) * (0.8 + 0.6 * core[:, None])
    pix = glass_rgb * (1 - grout[:, None]) + gr * grout[:, None]
    glass = blank(W, H)
    glass[sel, :3] = pix
    glass[..., 3] = body
    # small specular glints on a few tesserae (glass catching the bulb)
    # --- bloom from the emissive glass
    em = glass[..., :3] * body[..., None] * (1 - np.pad(grout, 0)[None].mean())
    out = blank(W, H)
    for rad, st in ((R * 1.1, 0.5 * bloom), (R * 0.7, 0.6 * bloom), (R * 0.25, 0.5 * bloom)):
        bl = np.stack([gaussian_filter(em[..., c], rad) for c in range(3)], -1)
        a = np.clip(bl.max(-1) * st * 2.2, 0, 1)
        colr = bl / np.maximum(bl.max(-1, keepdims=True), 1e-4)
        colr = colr * 0.82 + np.array([1, .86, .6], np.float32) * 0.18
        out = over(out, np.concatenate([np.clip(colr, 0, 1), a[..., None]], -1))
    out = over(out, glass)
    # --- brass cap (dome + scalloped skirt + pierced holes leaking light) and finial
    cr = rx * (0.52 if kind in ("onion",) else 0.7)
    ctop = cap_y - R * 0.12
    skirt = []
    n_sc = 9
    for i in range(n_sc * 8 + 1):
        t = i / (n_sc * 8)
        x = cx - cr + 2 * cr * t
        sc = abs(math.sin(t * n_sc * math.pi))
        skirt.append((x, cap_y + R * 0.1 + sc * R * 0.1))
    dome = [(cx - cr, cap_y + R * 0.1)] + [(cx + math.cos(a) * cr, cap_y + R * 0.1 + math.sin(a) * (cap_y + R * 0.1 - ctop)) for a in np.linspace(math.pi, math.tau, 30)] + skirt[::-1]
    capm = shapes(W, H, [dome], smooth=False)
    capm = np.maximum(capm, circles(W, H, [(cx, ctop - R * 0.02, R * 0.07)]))
    capm = np.maximum(capm, shapes(W, H, [[(cx - R * 0.05, ctop - R * 0.06), (cx + R * 0.05, ctop - R * 0.06), (cx + R * 0.03, ctop - R * 0.16), (cx - R * 0.03, ctop - R * 0.16)]], smooth=False))
    ringm = ring(W, H, cx, ctop - R * 0.22, R * 0.075, R * 0.03)
    capm = np.maximum(capm, ringm)
    out = over(out, foil(capm, BRASS, seed=nx(), emboss=0.9, sparkle=0.15))
    # darker underside towards the glass + band line
    out = over(out, flat(capm * np.clip((yy - (cap_y - R * 0.02)) / (R * 0.12), 0, 1), BRASS_D, 0.55))
    holes = circles(W, H, [(cx + (k - 3) * cr * 0.28, cap_y + R * 0.0 - abs(k - 3) * R * 0.03, R * 0.022) for k in range(7)])
    out = over(out, flat(holes * capm, "#ffe9a8", 0.95))
    out = over(out, glow(holes * capm, "#ffd27a", radius=3, strength=0.5))
    # bottom finial: small cup, bead and drop
    by = max(p[1] for p in pts)
    cup = [(cx - R * 0.16, by - R * 0.05)] + [(cx + math.cos(a) * R * 0.16, by - R * 0.05 + math.sin(a) * R * 0.12) for a in np.linspace(0, math.pi, 20)][::-1] + [(cx + R * 0.16, by - R * 0.05)]
    fm = np.maximum.reduce([shapes(W, H, [cup], smooth=False), circles(W, H, [(cx, by + R * 0.12, R * 0.05)]),
                            shapes(W, H, [petal_pts(cx, by + R * 0.16, R * 0.2, R * 0.06, math.pi / 2, n=10)])])
    out = over(out, foil(fm, BRASS, seed=nx(), emboss=0.9, sparkle=0.1))
    # glass bead strand + tassel bead below the finial
    beads = [(cx, by + R * 0.42 + k * R * 0.09, R * 0.035) for k in range(4)]
    bm = circles(W, H, beads)
    out = over(out, flat(bm, pal[1], 0.95))
    out = over(out, glow(bm, pal[3], radius=3, strength=0.3))
    # --- chain
    ch = chain(W, H, cx, 0, ctop - R * 0.28, link=max(7.0, R * 0.09))
    out = over(out, foil(ch, BRASS, seed=nx(), emboss=1.0, sparkle=0.1))
    out = over(out, flat(ch * np.clip((yy / max(1.0, ctop)) * 0.2, 0, 1), "#000000", 0.0))
    return out


def save_lamp(name, W, H, R, kind, pal, seed, chain_len, max_w):
    art = lamp(W, H, W / 2, 0, chain_len, R, kind, PAL[pal], seed)
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]; yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    win = np.clip(np.minimum(xx, 1 - xx) / 0.16, 0, 1) ** 1.5 * np.clip((1 - yy) / 0.1, 0, 1)
    art[..., 3] *= np.maximum(win, (art[..., 3] > 0.9) * 1.0)
    # keep full chain to top: put a near-invisible pixel in top corners so trimming keeps the hang point
    art[0, 0] = [0, 0, 0, 0.02]; art[0, -1] = [0, 0, 0, 0.02]
    prev_dark(art, name)
    save(art, f"{OUT}/{name}.webp", max_w=max_w, quality=80)
    clear()


if "lampA" in PARTS:
    save_lamp("lampA", 420, 1000, 128, "globe", "ruby", 11, 560, 300)
if "lampB" in PARTS:
    save_lamp("lampB", 340, 820, 92, "onion", "teal", 23, 470, 230)
if "lampC" in PARTS:
    save_lamp("lampC", 320, 700, 80, "drop", "amber", 37, 380, 210)
if "lampD" in PARTS:
    save_lamp("lampD", 300, 900, 66, "tall", "violet", 41, 560, 190)

if "pools" in PARTS:
    # coloured light pools: dappled projections of tesserae on a floor/wall, soft and warm
    W, H = 760, 300
    rng = random.Random(5)
    art = blank(W, H)
    for (cx, cy, rx, ry, pal) in [(380, 150, 300, 110, "ruby"), (150, 170, 150, 70, "teal"), (620, 165, 150, 70, "amber")]:
        base = ellipses(W, H, [(cx, cy, rx, ry, 0)])
        base = gaussian_filter(base, 30)
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * col_arr("#ffcf86"), (base * 0.35)[..., None]], -1))
        spots = []
        for _ in range(int(rx * ry / 1400)):
            a = rng.uniform(0, math.tau); r = math.sqrt(rng.random())
            spots.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r, rng.uniform(16, 30) * (1.2 - r * 0.6), rng.uniform(9, 16) * (1.2 - r * 0.6), rng.uniform(0, 180), rng.choice(PAL[pal])))
        for colr in set(s_[5] for s_ in spots):
            m = ellipses(W, H, [s_[:5] for s_ in spots if s_[5] == colr])
            m = gaussian_filter(m, 9) * base * 2.0
            art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * col_arr(colr), np.clip(m * 0.5, 0, 1)[..., None]], -1))
    prev_dark(art, "pools")
    save(art, f"{OUT}/pools.webp", max_w=560, quality=78)
    clear()

if "divider" in PARTS:
    # a swag of brass chain with a tiny mosaic lamp at the centre
    W, H = 720, 230
    art = blank(W, H)
    sw = bez((20, 24), (200, 110), (520, 110), (700, 24), 80)
    links = []
    for i, (x, y, a) in enumerate(resample(sw, 8.0)):
        links.append((x, y, 3.0 if i % 2 else 4.4, 2.2 if i % 2 else 2.6, math.degrees(a)))
    ch = ellipses(W, H, links) - ellipses(W, H, [(x, y, rx * 0.4, ry * 0.4, r) for x, y, rx, ry, r in links[::2]]) * 0.0
    ch = np.clip(ch, 0, 1)
    art = over(art, foil(ch, BRASS, seed=3, emboss=1.0, sparkle=0.1))
    lm = lamp(W, H, 360, 88, 26, 34, "globe", PAL["ruby"], 51, cell=6.2, bloom=0.8)
    art = over(art, lm)
    for x0 in (20, 700):
        art = over(art, foil(circles(W, H, [(x0, 24, 7)]), BRASS, seed=5))
    prev_dark(art, "divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=82)
    clear()

if "rosette" in PARTS:
    # a flat round mosaic medallion: 8-fold star rosette of tesserae in a brass ring, lit from behind
    W = H = 440
    cx = cy = 220
    rng = np.random.default_rng(9)
    disc = circles(W, H, [(cx, cy, 190)])
    lab, pts, grout = tesserae(disc, 9.0, 9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = pts[:, 0] - cx, pts[:, 1] - cy
    r = np.hypot(px, py) / 190; a = np.arctan2(py, px)
    star = 0.3 + 0.3 * (0.5 + 0.5 * np.cos(8 * a)) ** 1.5
    pal = np.array([hex_rgb(c) for c in ["#c2263a", "#f2a03a", "#1f8f9a", "#2f6fc0", "#f7d36b", "#2f9a5a", "#7a3fa6"]], np.float32)
    idx = np.where(r < 0.16, 4, np.where(r < star, np.where(np.cos(16 * a) > -0.2, 0, 1),
                                         np.where(r < 0.72, np.where(np.cos(16 * a + r * 9) > 0.2, 2, 3), np.where(r < 0.84, 5 + (np.cos(24 * a) > 0), 4))))
    cols = pal[idx] * (0.82 + 0.3 * rng.random((len(pts), 1))).astype(np.float32)
    rgb = cols[lab]
    rr = np.hypot(xx - cx, yy - cy) / 190
    lum = 0.6 + 0.55 * np.exp(-rr ** 2 * 2.4) + 0.1 * fbm(W, H, 4, 6, 2)
    rgb = rgb * lum[..., None]
    gr = col_arr(GROUT)
    g = np.clip(grout, 0, 1)[..., None]
    rgb = rgb * (1 - g) + gr * g
    glass_ = np.concatenate([np.clip(rgb, 0, 1), disc[..., None]], -1)
    em = glass_[..., :3] * disc[..., None]
    bl = np.stack([gaussian_filter(em[..., c], 26) for c in range(3)], -1)
    art = np.concatenate([np.clip(bl / np.maximum(bl.max(-1, keepdims=True), 1e-4), 0, 1), np.clip(bl.max(-1) * 1.1, 0, 1)[..., None]], -1)
    art = over(art, glass_)
    art = over(art, foil(ring(W, H, cx, cy, 200, 16), BRASS, seed=7, emboss=1.0, sparkle=0.15))
    art = over(art, foil(circles(W, H, [(cx + math.cos(k * math.tau / 16) * 192, cy + math.sin(k * math.tau / 16) * 192, 6) for k in range(16)]), BRASS, seed=8))
    prev_dark(art, "rosette")
    save(art, f"{OUT}/rosette.webp", max_w=220, quality=82)
    clear()

if "night" in PARTS:
    # tileable night plaster: deep plum-indigo, soft mottling and a few faint dust motes
    W = H = 384
    n1 = wrap_noise(W, H, 3, 26); n2 = wrap_noise(W, H, 4, 6)
    base = col_arr("#150f24")[None, None] * (0.86 + 0.22 * n1[..., None] + 0.06 * n2[..., None])
    base += col_arr("#2a1838")[None, None] * 0.12 * n1[..., None]
    img = np.concatenate([np.clip(base, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/night.webp", quality=92)
