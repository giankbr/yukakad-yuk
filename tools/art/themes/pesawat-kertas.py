"""Pesawat Kertas — playful gouache paper planes over a blue sky: a big dart folded from airmail paper (red/blue
striped trailing edge, crisp folds, paper grain), a small plane folded from ruled notebook paper, two soft gouache
cumulus clouds and a seamless creased-paper texture for the cards.
Run: python3 -I pesawat-kertas.py [part ...]   parts: plane plane2 clouds paper
Assets -> public/themes/art/pesawat-kertas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k5_lib import *  # noqa

OUT = outdir("pesawat-kertas")
PARTS = sys.argv[1:] or ["plane", "plane2", "clouds", "paper"]
PAPER, PAPER_S, PAPER_D = "#fbfaf5", "#dfe3e8", "#b9c2cf"
RED, BLUE, NAVY = "#d9493b", "#2e64b0", "#1f3354"
nx = Seq(700)


def face(art, W, H, pts, c1, c2, shade_from, shade_to, amt, seed):
    m = polys(W, H, [pts], smooth=False)
    art = GP(art, m, c1, c2, seed=seed, rough=0.9, streak=0.35)
    g = lin_grad(W, H, *shade_from, *shade_to)
    art = G(art, m * g * amt, "#9aa8bb", "#b6c1d0", seed=seed + 1, density=0.6, edge=0.15, bloom=0.3, gran=0.4, rough=1.2, feather=1.2)
    return art, m


def crease(art, W, H, a, b, dark=0.5, light=0.7, w=1.6):
    d = lines_mask(W, H, [[a, b]], w)
    art = over(art, tint(d, "#7d8a9c", dark))
    l = lines_mask(W, H, [[(a[0], a[1] - 1.5), (b[0], b[1] - 1.5)]], 1.0)
    art = over(art, tint(l, "#ffffff", light))
    return art


def stripes_on(art, W, H, A, B, toward, mm, band=15, step=14):
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
    nxv, nyv = -uy, ux
    if (toward[0] - A[0]) * nxv + (toward[1] - A[1]) * nyv < 0:
        nxv, nyv = -nxv, -nyv
    red, blue = [], []
    for i in range(int(L // step) + 1):
        t0 = i * step
        p0 = (A[0] + ux * t0, A[1] + uy * t0)
        q = [p0, (p0[0] + ux * step * 0.55, p0[1] + uy * step * 0.55),
             (p0[0] + ux * (step * 0.55 + 7) + nxv * band, p0[1] + uy * (step * 0.55 + 7) + nyv * band),
             (p0[0] + ux * 7 + nxv * band, p0[1] + uy * 7 + nyv * band)]
        (red if i % 2 == 0 else blue).append(q)
    art = GP(art, polys(W, H, red, smooth=False) * mm, RED, "#c63e33", seed=nx(), rough=0.6, streak=0.3)
    art = GP(art, polys(W, H, blue, smooth=False) * mm, BLUE, "#295aa0", seed=nx(), rough=0.6, streak=0.3)
    return art


def dart(W, H, N, T1, C, C2, T2, stripe=True, ruled=False):
    """3/4 view from above-behind: big near wing (N, T1, C), keel sliver (N, C, C2), far wing (N, C2, T2)."""
    art = blank(W, H)
    art, mk = face(art, W, H, [N, C, C2], "#55657d", "#6b7a91", N, C2, 0.2, nx())
    art, mfar = face(art, W, H, [N, C2, T2], "#d3dbe6", "#c5cfdc", N, T2, 0.8, nx())
    art, mnear = face(art, W, H, [N, T1, C], PAPER, "#f3f0e7", N, T1, 0.28, nx())
    if ruled:
        ang = math.atan2(N[1] - T1[1], N[0] - T1[0])
        segs = []
        for k in range(-30, 30):
            ox, oy = T1[0] - math.sin(ang) * k * 12, T1[1] + math.cos(ang) * k * 12
            segs.append([(ox - math.cos(ang) * 900, oy - math.sin(ang) * 900), (ox + math.cos(ang) * 900, oy + math.sin(ang) * 900)])
        art = over(art, tint(lines_mask(W, H, segs, 1.1) * np.maximum(mnear, mfar), "#7fb0dc", 0.6))
        mx = T1[0] + (C[0] - T1[0]) * 0.2, T1[1] + (C[1] - T1[1]) * 0.2
        art = over(art, tint(lines_mask(W, H, [[mx, (mx[0] + (N[0] - T1[0]), mx[1] + (N[1] - T1[1]))]], 1.6) * mnear, RED, 0.6))
    if stripe:
        art = stripes_on(art, W, H, T1, C, N, mnear)
        art = stripes_on(art, W, H, C2, T2, N, mfar, band=12)
    # folds
    art = crease(art, W, H, N, C, 0.5, 0.0, 1.6)
    art = over(art, tint(lines_mask(W, H, [[(N[0] - 6, N[1] + 2), (T1[0] + (C[0] - T1[0]) * 0.5, T1[1] + (C[1] - T1[1]) * 0.5)]], 1.0) * mnear, "#9aa6b5", 0.45))
    alpha = art[..., 3].copy()
    g = fbm(W, H, nx(), 6, 2)
    art[..., :3] *= (0.97 + 0.05 * g)[..., None]
    edge = np.clip(gaussian_filter(alpha, 0.9) - gaussian_filter(alpha, 2.4), 0, 1) * 2.2
    edge *= 0.6 + 0.4 * (fbm(W, H, nx(), 14, 2) > 0.35)
    art = over(art, col_arr(edge, NAVY, np.clip(edge, 0, 1) * 0.6))
    return art


def plane():
    W, H = 600, 340
    art = dart(W, H, N=(588, 34), T1=(14, 150), C=(250, 196), C2=(268, 222), T2=(330, 326))
    save(art, f"{OUT}/plane.webp", max_w=520)
    prev(art, "pk-plane", bg="#bfe0f4")


def plane2():
    W, H = 320, 200
    art = dart(W, H, N=(312, 20), T1=(10, 92), C=(136, 112), C2=(146, 126), T2=(176, 190), stripe=False, ruled=True)
    save(art, f"{OUT}/plane2.webp", max_w=240)
    prev(art, "pk-plane2", bg="#bfe0f4")


def cloud(W, H, blobs, seed):
    art = blank(W, H)
    m = circles(W, H, blobs)
    # flat-ish base
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    base = max(y + r * 0.35 for x, y, r in blobs)
    m *= np.clip((base - yy) / 6, 0, 1)
    art = GP(art, m, "#ffffff", "#f7fbff", seed=seed, rough=2.6, streak=0.4)
    sh = m * np.clip((yy - (base - 70)) / 70, 0, 1)
    art = G(art, sh, "#b9cfe6", "#c9d9ec", seed=seed + 1, density=0.6, edge=0.25, bloom=0.4, gran=0.3, rough=2, feather=3)
    # inner lobes: lighter tops
    lobes = circles(W, H, [(x - r * 0.15, y - r * 0.2, r * 0.6) for x, y, r in blobs]) * m
    art = over(art, col_arr(gaussian_filter(lobes, 6), "#ffffff", gaussian_filter(lobes, 6) * 0.6))
    return art


def clouds():
    a = cloud(560, 230, [(110, 150, 70), (200, 110, 88), (300, 96, 76), (380, 130, 66), (460, 158, 50), (60, 172, 42)], nx())
    save(a, f"{OUT}/cloud-a.webp", max_w=460)
    prev(a, "pk-cloud-a", bg="#8fc3e8")
    b = cloud(340, 150, [(70, 104, 44), (140, 76, 58), (214, 88, 48), (270, 110, 34)], nx())
    save(b, f"{OUT}/cloud-b.webp", max_w=280)
    prev(b, "pk-cloud-b", bg="#8fc3e8")


def paper():
    """Seamless creased paper 400 x 400: off-white, two sets of folds (ridge light + valley shade), fibres."""
    N = 400
    base = solid(N, N, "#fbf9f3")
    wv = wrap_noise(N, N, 4, 1.2)
    mot = wrap_noise(N, N, 5, 40)
    base[..., :3] *= (0.985 + 0.02 * wv + 0.025 * mot)[..., None]
    rng = np.random.default_rng(8)
    shade = np.zeros((N, N), np.float32)
    light = np.zeros((N, N), np.float32)
    for ang, off in ((0.0, 133), (math.pi / 2, 260), (math.pi / 4, 0), (-math.pi / 4, 200)):
        segs_d, segs_l = [], []
        ca, sa = math.cos(ang), math.sin(ang)
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                cx, cy = off + ox, off * 0.7 + oy
                a = (cx - ca * 900, cy - sa * 900); b = (cx + ca * 900, cy + sa * 900)
                segs_d.append([a, b])
                segs_l.append([(a[0] - sa * 2, a[1] + ca * 2), (b[0] - sa * 2, b[1] + ca * 2)])
        shade = np.maximum(shade, gaussian_filter(lines_mask(N, N, segs_d, 1.4), 1.2, mode="wrap"))
        light = np.maximum(light, gaussian_filter(lines_mask(N, N, segs_l, 2.2), 2.0, mode="wrap"))
    base = over(base, col_arr(shade, "#9aa6b5", shade * 0.32))
    base = over(base, col_arr(light, "#ffffff", light * 0.5))
    save_full(base, f"{OUT}/paper.webp", quality=78, rgb=True)
    prev(np.concatenate([base, base], 1), "pk-paper")


for part in PARTS:
    globals()[part]()
    clear()
