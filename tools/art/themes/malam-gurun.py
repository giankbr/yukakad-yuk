"""Malam Gurun — desert dunes under a deep starry night with a slim crescent; moonlit sand, a distant tent and a small
oasis of date palms in silhouette. No figures, no animals, no calligraphy.
Run: python3 -I malam-gurun.py [part ...]  parts: sky dunes sand star divider dune_band
Assets -> public/themes/art/malam-gurun/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n4_lib import *
from scipy.ndimage import gaussian_filter1d

OUT = outdir("malam-gurun")
PARTS = sys.argv[1:] or ["sky", "dunes", "sand", "star", "divider", "dune_band"]
NIGHT = [(0, "#070b1f"), (0.35, "#111940"), (0.68, "#232b5a"), (0.86, "#3d3a68"), (1, "#5a4a70")]
MOON = "#f4e9c8"
GOLD = "#d9b46a"


def crescent(W, H, cx, cy, r, off=0.32, ang=-0.6):
    a = circles(W, H, [(cx, cy, r)])
    b = circles(W, H, [(cx + math.cos(ang) * r * off * 1.6, cy + math.sin(ang) * r * off * 1.6, r * 0.93)])
    return np.clip(a - b, 0, 1)


def sky():
    W, H = 720, 1100
    art = painted_sky(W, H, NIGHT, seed=4, streak=1.4, grain=0.8)
    # faint milky band (diagonal smudge)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    band = np.exp(-((yy - (H * 0.62 - xx * 0.55)) / 110) ** 2) * (0.4 + 0.6 * fbm(W, H, 9, 60, 4))
    art = over(art, flat(np.ones((H, W), np.float32), "#8d8fc0", 1.0) * 0 + rgba(np.ones((H, W, 3), np.float32) * col3("#8f90c2"), band * 0.16))
    # stars
    sm, bm, bigs = star_field(W, H, 7, n=900, ymax=0.85, big=16)
    dust = np.clip(band * 1.6, 0, 1)
    sm2, _, _ = star_field(W, H, 8, n=700, ymax=0.85, big=0)
    art = over(art, flat(sm, "#efe8d6", 0.85))
    art = over(art, flat(sm2 * dust, "#e8e4f2", 0.8))
    art = over(art, glow(bm, "#cfd6ff", 6, 0.35))
    art = over(art, flat(bm, "#fbf6e6", 0.95))
    # crescent with soft halo (light from upper right)
    cx, cy, r = W * 0.78, H * 0.12, 46
    cm = crescent(W, H, cx, cy, r, 0.17, math.pi * 0.85)
    art = over(art, glow(circles(W, H, [(cx, cy, r * 1.05)]), "#c9c5e6", 70, 0.22))
    art = over(art, glow(cm, "#fff1c9", 16, 0.5))
    art = OV(art, cm, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3(MOON) * (0.93 + 0.1 * fbm(m.shape[1], m.shape[0], 3, 8, 3))[..., None], np.clip(gaussian_filter(m, 0.8), 0, 1)))
    # thin horizon haze
    hz = np.exp(-((yy - H * 0.98) / 110) ** 2)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3("#7a6280"), hz * 0.35))
    art = add_grain(art, 3, 0.03)
    preview(art, "mg-sky")
    save_rgb(art, f"{OUT}/sky.webp", quality=74)


def dune_poly(W, H, ys, amp, ph, wl, x0=-30, x1=None, base=None):
    x1 = x1 if x1 is not None else W + 30
    base = base if base is not None else H + 20
    pts = [(x0, base)]
    for x in np.arange(x0, x1 + 1, 12):
        y = ys - amp * (0.65 * math.sin(x / wl + ph) + 0.35 * math.sin(x / (wl * 0.43) + ph * 1.7))
        pts.append((x, y))
    pts.append((x1, base))
    return pts


def crest_fn(W, ys, amp, ph, wl, ph2=1.7):
    x = np.arange(W + 1, dtype=np.float32)
    sharp = 1 - np.abs(np.cos(x / wl + ph)) ** 0.9
    return ys - amp * (0.8 * sharp + 0.2 * np.sin(x / (wl * 0.43) + ph * ph2))


def dune_layer(W, H, c, lit, shade, deep, rim, seed, lean=0.9, fall=90.0, k=4.0, rimw=1.6):
    """Pixel-shaded dune from a crest curve c(x): moon at the upper right lights the faces descending to the right;
    the slip-face boundary leans with depth; lighting fades with distance below the crest; brush streak texture."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = c[:W]
    d = yy - cx[None, :]
    m = np.clip(d + 0.5, 0, 1)
    s = np.gradient(gaussian_filter1d(c, 3))[:W]
    xi = np.clip(xx - lean * np.maximum(d, 0) ** 0.85 * 1.05, 0, W - 1).astype(int)
    sl = s[xi]
    litv = 1 / (1 + np.exp(-sl * k * 6))
    fade = np.exp(-np.maximum(d, 0) / fall)
    litv = gaussian_filter(litv, (1.5, 3.5))
    t = litv * (0.35 + 0.65 * fade)
    rgb = col3(shade)[None, None] * (1 - t[..., None]) + col3(lit)[None, None] * t[..., None]
    dk = np.clip(np.maximum(d, 0) / (H * 0.9), 0, 1) * (1 - litv * 0.6)
    rgb = rgb * (1 - dk[..., None]) + col3(deep) * dk[..., None]
    # texture: horizontal wind streaks + soft mottling
    st = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (0.7, 9))
    st = (st - st.mean()) / (st.std() + 1e-6)
    rgb = rgb * (1 + st[..., None] * 0.025 + (fbm(W, H, seed + 1, 80, 3)[..., None] - 0.5) * 0.08)
    # ripples on lit faces
    rip = (np.sin((yy * 0.9 + np.sin(xx / 37) * 6 + fbm(W, H, seed + 2, 30, 2) * 20) * 0.55) * 0.5 + 0.5) ** 6
    rgb = rgb * (1 - rip[..., None] * 0.06 * t[..., None])
    # rim light along the crest where lit
    rimm = np.exp(-np.maximum(d, 0) / rimw) * (d > -0.5) * np.clip(litv * 1.6 - 0.2, 0, 1)
    rgb = rgb * (1 - rimm[..., None] * 0.7) + col3(rim) * rimm[..., None] * 0.7
    a = displace(m, seed + 3, 1.2, 10)
    a[-8:] = m[-8:]
    a[:, :6] = np.maximum(a[:, :6], m[:, :6]); a[:, -6:] = np.maximum(a[:, -6:], m[:, -6:])
    return rgba(np.clip(rgb, 0, 1), np.clip(a, 0, 1))


def date_palm(W, H, x, by, h, rng, lean=0.05):
    top = (x + lean * h, by - h)
    tr = curve([(x, by), (x + lean * h * 0.3, by - h * 0.5), top], 20)
    items = [(tr, h * 0.05, (0.0, 0.2))]
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.1, 0.1)
        L = h * rng.uniform(0.42, 0.55)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.6, top[1] + math.sin(a) * L * 0.6 - L * 0.12), (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.4)], 14)
        items.append((pts, h * 0.035, (0.05, 0.6)))
    return strokes(W, H, items)


def dunes():
    """Layered dunes; far ridge carries a tent and a small date-palm oasis in silhouette. Transparent above."""
    W, H = 720, 600
    nx = Seq(2200)
    rng = random.Random(5)
    art = blank(W, H)
    # far ridge (flat, hazy)
    art = over(art, dune_layer(W, H, crest_fn(W, H * 0.3, 10, 1.2, 140), "#5a5482", "#2e2a52", "#26224a", "#9d94c0", nx(), lean=0.6, fall=60))
    # oasis: palms + tent on the far ridge
    ox = W * 0.24
    sil = np.zeros((H, W), np.float32)
    for (x, h, ln) in [(ox - 30, 74, -0.08), (ox - 8, 92, 0.05), (ox + 22, 66, 0.12), (ox + 52, 52, -0.05)]:
        sil = np.maximum(sil, date_palm(W, H, x, H * 0.31, h, rng, ln))
    tx, ty = W * 0.42, H * 0.305
    tent = shapes(W, H, [[(tx - 44, ty + 2), (tx - 30, ty - 16), (tx - 6, ty - 30), (tx + 2, ty - 33), (tx + 10, ty - 30), (tx + 34, ty - 16), (tx + 48, ty + 2)]], smooth=True)
    sil = np.maximum(sil, tent)
    art = GP(art, sil, "#1c1a38", "#24214a", seed=nx(), rough=0.6, streak=0.6)
    # warm glow from the tent door (lantern light, no figure)
    door = shapes(W, H, [[(tx - 5, ty + 1), (tx + 1, ty - 15), (tx + 7, ty + 1)]], smooth=False)
    art = over(art, glow(door, "#f0b765", 10, 0.6))
    art = OV(art, door, lambda q: rgba(np.ones(q.shape + (3,), np.float32) * col3("#f6c97a"), q))
    # small pool reflection at the oasis
    pool = shapes(W, H, [ellipse_pts(ox + 6, H * 0.325, 44, 4, 14)])
    art = OV(art, pool, lambda q: rgba(np.ones(q.shape + (3,), np.float32) * col3("#6f73a8"), q * 0.8))
    # mid dunes
    art = over(art, dune_layer(W, H, crest_fn(W, H * 0.47, 34, 0.4, 110), "#8a7da2", "#3b3460", "#2c2650", "#d2c4dc", nx(), lean=0.8, fall=80))
    art = over(art, dune_layer(W, H, crest_fn(W, H * 0.66, 40, 2.6, 150), "#b39ca2", "#463c62", "#2a2346", "#efdcd0", nx(), lean=1.0, fall=110))
    art = over(art, dune_layer(W, H, crest_fn(W, H * 0.87, 16, 4.1, 200), "#5e4d68", "#221c36", "#17132a", "#a8919a", nx(), lean=1.0, fall=50))
    art = add_grain(art, 6, 0.03)
    preview(art, "mg-dunes", bg="#232b5a")
    save(art, f"{OUT}/dunes.webp", max_w=720, quality=78)


def sand():
    """Seamless pale moonlit sand with wind ripples (light sections)."""
    W = H = 384
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = wrap_noise(W, H, 3, 24) - 0.5
    rip = np.sin((yy + n * 60 + np.sin(xx / W * math.tau * 2) * 8) / H * math.tau * 22)
    rip = (rip * 0.5 + 0.5) ** 3
    base = col3("#efe4d2")[None, None] * (1 + (wrap_noise(W, H, 4, 40) - 0.5) * 0.06)[..., None]
    rgb = base * (1 - rip[..., None] * 0.045) + col3("#ffffff") * (rip[..., None] * 0.02)
    gr = (wrap_noise(W, H, 5, 0.6) - 0.5)
    rgb = rgb * (1 + gr[..., None] * 0.06)
    save_rgb(rgba(np.clip(rgb, 0, 1), np.ones((H, W), np.float32)), f"{OUT}/sand.webp", quality=72)


def star():
    """Eight-point star (khatam) in pressed gold foil with an inner rosette, for nodes, amp and emblem."""
    W = H = 240
    c = W / 2
    sq = lambda r, a: [(c + math.cos(a + k * math.pi / 2) * r, c + math.sin(a + k * math.pi / 2) * r) for k in range(4)]
    s1 = shapes(W, H, [sq(104, math.pi / 4), sq(104, 0)], smooth=False)
    i1 = shapes(W, H, [sq(84, math.pi / 4), sq(84, 0)], smooth=False)
    ring = np.clip(s1 - i1, 0, 1)
    pet = shapes(W, H, [petal_pts(c, c, 70, 20, k * math.pi / 4, n=12) for k in range(8)])
    core = circles(W, H, [(c, c, 16)])
    m = np.clip(ring + pet * (1 - circles(W, H, [(c, c, 10)])) + core * 0, 0, 1)
    art = blank(W, H)
    art = OV(art, i1, lambda q: rgba(np.ones(q.shape + (3,), np.float32) * col3("#1a2150"), q * 0.92))
    art = FO(art, m, GOLD, seed=4, emboss=0.6, sparkle=0.12)
    art = FO(art, circles(W, H, [(c, c, 6)]), GOLD, seed=5)
    preview(art, "mg-star", bg="#111940")
    save(art, f"{OUT}/star.webp", max_w=160, quality=84)


def divider():
    """A row of painted stars getting smaller towards the ends with a tiny crescent in the middle."""
    W, H = 360, 44
    art = blank(W, H)
    c = W / 2
    cm = crescent(W, H, c, H / 2, 11, 0.32, math.pi * 0.85)
    dots = []
    for k in range(1, 9):
        r = max(0.9, 3.2 - k * 0.32)
        for sd in (-1, 1):
            dots.append((c + sd * (22 + k * 17), H / 2 + (1.5 if k % 2 else -1.5), r))
    dm = circles(W, H, dots)
    line = strokes(W, H, [([(c - 160, H / 2), (c - 22, H / 2)], 0.8, (0.3, 0.0)), ([(c + 22, H / 2), (c + 160, H / 2)], 0.8, (0.0, 0.3))])
    art = FO(art, np.clip(cm + dm, 0, 1), GOLD, seed=6, emboss=0.4, sparkle=0.1)
    art = OV(art, line, lambda q: rgba(np.ones(q.shape + (3,), np.float32) * col3(GOLD), q * 0.6))
    preview(art, "mg-divider", bg="#111940")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)


def dune_band():
    """Low dune silhouettes in night colours, repeat-x strip for section bottoms (dark band to light sand)."""
    W, H = 720, 120
    nx = Seq(3100)
    art = blank(W, H)
    x = np.arange(W + 1, dtype=np.float32)
    c = H * 0.42 - 16 * np.sin(x / W * math.tau * 2 + 0.4) - 7 * np.sin(x / W * math.tau * 5)
    art = dune_layer(W, H, c, "#8a7da2", "#3b3460", "#2c2650", "#d2c4dc", nx(), lean=0.6, fall=40)
    save_full(art, f"{OUT}/dune_band.webp", quality=80)
    preview(art, "mg-band", bg="#efe4d2")


for p in PARTS:
    globals()[p]()
    clear()
