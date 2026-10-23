"""Batik Syari — soft modern batik in watercolour on cream cloth: a seamless parang selendang strip (diagonal
lereng blades with mlinjon dots between bands, sage / dusty blue / sand), its horizontal twin, a kawung medallion
(nested four-petal kawung ring), a faint seamless kawung lattice, a kawung-dot divider and a single kawung node.
No figures. Run: python3 -I batik-syari.py [part ...]   parts: parang kawung tile divider node
Assets -> public/themes/art/batik-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k5_lib import *  # noqa

OUT = outdir("batik-syari")
PARTS = sys.argv[1:] or ["parang", "kawung", "tile", "divider", "node"]
CREAM, SAND, SAND_D = "#f4eee2", "#d9c9a8", "#b49d72"
SAGE, SAGE_D = "#9db4a0", "#6c8a74"
BLUE, BLUE_D = "#94abc0", "#5c7690"
SLATE = "#46596a"
nx = Seq(300)
S2 = math.sqrt(2)


def cloth(W, H, seed):
    """Cream cotton (primissima) ground: soft weave + mottling."""
    base = solid(W, H, CREAM)
    wv = wrap_noise(W, H, seed, (0.4, 2.5)) * 0.5 + wrap_noise(W, H, seed + 1, (2.5, 0.4)) * 0.5
    base[..., :3] *= (0.975 + 0.05 * wv)[..., None]
    mot = fbm(W, H, seed + 2, 90, 3)
    base[..., :3] *= (0.985 + 0.03 * mot)[..., None]
    return base


def parang():
    """Vertical tile 220 x 400 (period 400). Bands at 45 deg, spacing 100 px in x (70.7 across)."""
    W, H, O = 220, 400, 120
    HH = H + O
    sp = 100 / S2            # across-band spacing
    L = (H / S2) / 3          # blade length along band (3 per vertical period)
    hb = sp / 2
    f = rot_frame(math.pi / 4)  # u along (1,1), v along (-1,1)
    big, small, dots, edge = [], [], [], []
    bw = 0.70  # blade half-height as a fraction of hb
    for k in range(-8, 12):
        v0 = k * sp
        for n in range(-6, 14):
            u0 = n * L
            def P(a, b):
                return f(u0 + a * L, v0 + b * hb)
            # lereng blade: region between two sideways-S curves, its upper end rounded into a hooked head
            vs = np.linspace(-bw, bw, 12)
            s = lambda t: 0.42 * math.sin(t / bw * math.pi / 2)
            left = [P(s(t) - 0.02, t) for t in vs]
            right = [P(s(t) + 0.70 - 0.10 * (t / bw), t) for t in vs[::-1]]
            big.append(left + [P(s(bw) + 0.30, bw * 1.04)] + right + [P(s(-bw) + 0.34, -bw * 1.05)])
            # inner sand stripe that curls at the head
            vs2 = np.linspace(-bw * 0.62, bw * 0.78, 10)
            l2 = [P(s(t) + 0.22, t) for t in vs2]
            r2 = [P(s(t) + 0.40, t) for t in vs2[::-1]]
            small.append(l2 + [P(s(bw * 0.78) + 0.36, bw * 0.92)] + r2)
            # mlinjon: a diamond + small dot on the rail between bands
            cx, cy = f(u0 + 0.45 * L, v0 + hb)
            r = 5.2
            dots.append(("d", cx, cy, r))
            cx, cy = f(u0 + 0.95 * L, v0 + hb)
            dots.append(("c", cx, cy, 1.9))
        for vv_ in (bw * 1.12, 2 - bw * 1.12):
            edge.append([f(-2000, v0 + hb * vv_), f(2000, v0 + hb * vv_)])
    art = cloth(W, HH, 11)
    mb = polys(W, HH, big)
    ms = polys(W, HH, small)
    md = np.maximum(circles(W, HH, [(x, y, r) for t, x, y, r in dots if t == "c"]),
                    polys(W, HH, [[f2 for f2 in ((x, y - r * 1.5), (x + r, y), (x, y + r * 1.5), (x - r, y))]
                                  for t, x, y, r in dots if t == "d"], smooth=False))
    me = lines_mask(W, HH, edge, 1.3)
    # alternate band colours: sage / dusty blue
    yy, xx = np.mgrid[0:HH, 0:W].astype(np.float32)
    vv = (-xx + yy) / S2
    band = (np.floor(vv / sp + 0.5).astype(int) % 2 == 0).astype(np.float32)
    band = gaussian_filter(band, 0.6)
    art = G(art, mb * band, SAGE, "#a9bfa6", seed=nx(), density=0.82, edge=0.6, bloom=0.25, gran=0.35, rough=2.2, feather=0.8, pad=0)
    art = G(art, mb * (1 - band), BLUE, "#a3b6c8", seed=nx(), density=0.8, edge=0.6, bloom=0.25, gran=0.35, rough=2.2, feather=0.8, pad=0)
    art = G(art, ms, SAND, "#e6d8bd", seed=nx(), density=0.75, edge=0.5, bloom=0.2, gran=0.3, rough=1.4, feather=0.6, pad=0)
    # isen-isen: fine slate outline (canting line) on the blades
    outline = np.clip(mb - gaussian_filter(np.clip(mb * 1.0, 0, 1), 1.0) * 1.0, 0, 1)
    ring = np.clip(gaussian_filter(mb, 1.1) - mb * 0.0, 0, 1) * (1 - mb) * 2.0
    art = G(art, np.clip(ring, 0, 1), SLATE, seed=nx(), density=0.5, edge=0.2, bloom=0, gran=0.2, rough=0.8, feather=0.4, pad=0)
    art = G(art, me, SAND_D, seed=nx(), density=0.55, edge=0.2, bloom=0, gran=0.3, rough=0.8, feather=0.4, pad=0)
    art = G(art, md, SLATE, BLUE_D, seed=nx(), density=0.7, edge=0.3, bloom=0, gran=0.2, rough=0.6, feather=0.4, pad=0)
    del outline
    tile = seam_y(art, H, O)
    tile = add_grain(tile, 5, 0.025)
    save_full(tile, f"{OUT}/parang.webp", quality=80, rgb=True)
    save_full(np.transpose(tile, (1, 0, 2))[::-1].copy(), f"{OUT}/parang-h.webp", quality=80, rgb=True)
    prev(np.concatenate([tile, tile], 0), "bs-parang")


def kawung_petal(cx, cy, ang, L, R):
    """Kawung petal: a plump oval pointing away from the centre."""
    pts = ellipse_pts(0, 0, L / 2, R / 2, n=28)
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def kawung_flower(cx, cy, r, rot=math.pi / 4):
    pet, eyes = [], []
    for k in range(4):
        a = rot + k * math.pi / 2
        px, py = cx + math.cos(a) * r * 0.52, cy + math.sin(a) * r * 0.52
        pet.append(kawung_petal(px, py, a, r * 0.98, r * 0.62))
        eyes.append((cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62, r * 0.07))
    return pet, eyes


def kawung():
    W = H = 560
    c = W / 2
    art = blank(W, H)
    # outer wash: a soft sage disc like a dyed roundel
    disc_m = disc(W, H, c, c, 262)
    art = G(art, disc_m, "#dfe7dc", "#e6ece3", seed=nx(), density=0.55, edge=0.45, bloom=0.5, gran=0.25, rough=5, feather=2)
    # ring of 8 blue kawung flowers
    petals, eyes = [], []
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        p, e = kawung_flower(c + math.cos(a) * 178, c + math.sin(a) * 178, 54, rot=a + math.pi / 4)
        petals += p; eyes += e
    mp = polys(W, H, petals)
    art = G(art, mp, BLUE, "#a7b9ca", seed=nx(), density=0.85, edge=0.6, bloom=0.3, gran=0.35, rough=2.5, feather=0.8)
    art = G(art, circles(W, H, eyes), SLATE, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    # centre: large sage kawung with sand inner petals
    p, e = kawung_flower(c, c, 118)
    art = G(art, polys(W, H, p), SAGE, "#b0c4ab", seed=nx(), density=0.88, edge=0.65, bloom=0.3, gran=0.35, rough=3, feather=1)
    p2, _ = kawung_flower(c, c, 66)
    art = G(art, polys(W, H, p2), SAND, "#eadcc0", seed=nx(), density=0.8, edge=0.5, bloom=0.2, gran=0.3, rough=2, feather=0.8)
    art = G(art, circles(W, H, e + [(c, c, 9)]), SLATE, BLUE_D, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    # canting outline around centre petals
    pm = polys(W, H, p)
    ring = np.clip(gaussian_filter(pm, 1.4) * 2 - pm * 2, 0, 1)
    art = G(art, ring, SAGE_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=0.4)
    # outer dotted rings (titik-titik isen)
    dots = [(c + math.cos(t) * 246, c + math.sin(t) * 246, 3.2) for t in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
    dots += [(c + math.cos(t) * 112, c + math.sin(t) * 112, 2.2) for t in np.linspace(0, 2 * math.pi, 40, endpoint=False) + 0.04]
    art = G(art, circles(W, H, dots), SAND_D, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    art = G(art, ring_mask(W, H, c, c, 254, 256.5), SAGE_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1.5, feather=0.6)
    save(art, f"{OUT}/kawung.webp", max_w=520, quality=80)
    prev(art, "bs-kawung", bg=CREAM)


def tile():
    """Seamless faint kawung lattice 240 x 240 (transparent) for band backgrounds and the cover watermark."""
    n, cell = 240, 120
    m = kawung_tile(n, cell, fat=0.36)
    m = tile_wrap(m)
    a = col_arr(m, "#ffffff", m * 0.9)
    # slight hand drift in density
    a[..., 3] *= 0.75 + 0.25 * wrap_noise(n, n, 4, 18)
    save_full(a, f"{OUT}/tile.webp", quality=80)
    prev(a, "bs-tile", bg=SAGE_D)


def divider():
    W, H = 400, 48
    c = W / 2
    art = blank(W, H)
    p, e = kawung_flower(c, H / 2, 20)
    art = G(art, polys(W, H, p), SAGE, "#adc1a9", seed=nx(), density=0.88, edge=0.6, bloom=0.2, rough=1.4, feather=0.6, pad=8)
    art = G(art, circles(W, H, e + [(c, H / 2, 2.6)]), SLATE, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.5, feather=0.3, pad=6)
    for s in (-1, 1):
        ln = stroke_mask(W, H, [(c + s * 30, H / 2), (c + s * 175, H / 2)], 2.2, taper=(0.02, 0.6))
        art = G(art, ln, BLUE_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.4, pad=6)
        dts = [(c + s * x, H / 2, r) for x, r in ((44, 3.0), (54, 2.2), (186, 2.4))]
        art = G(art, circles(W, H, dts), SAND_D, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.5, feather=0.3, pad=6)
        q, _ = kawung_flower(c + s * 120, H / 2, 8)
        art = G(art, polys(W, H, q), BLUE, seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.6, feather=0.4, pad=6)
    save(art, f"{OUT}/divider.webp", max_w=400)
    prev(art, "bs-divider", bg=CREAM)


def node():
    W = H = 110
    art = blank(W, H)
    p, e = kawung_flower(W / 2, H / 2, 46)
    art = G(art, polys(W, H, p), BLUE, "#a6b9ca", seed=nx(), density=0.88, edge=0.6, bloom=0.2, rough=1.6, feather=0.6, pad=8)
    p2, _ = kawung_flower(W / 2, H / 2, 24)
    art = G(art, polys(W, H, p2), SAND, seed=nx(), density=0.8, edge=0.4, bloom=0.1, rough=1, feather=0.5, pad=8)
    art = G(art, circles(W, H, e + [(W / 2, H / 2, 3.5)]), SLATE, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.5, feather=0.3, pad=6)
    save(art, f"{OUT}/node.webp", max_w=110)
    prev(art, "bs-node", bg=CREAM)


for part in PARTS:
    globals()[part]()
    clear()
