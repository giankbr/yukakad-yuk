"""Sage Syari — no-photo walimah: silver-dollar eucalyptus + dried leaves in transparent watercolour, a poured sage
wax seal (monogram is typeset on top in the page), soft woven linen tile. No figures, no calligraphy.
Run: python3 -I sage-syari.py [part ...]   parts: ranting segel divider daun tangkai linen"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g4_lib import *

OUT = outdir("sage-syari")
PARTS = sys.argv[1:] or ["ranting", "segel", "divider", "daun", "tangkai", "linen"]
BG = "#ecebe2"
EU = ("#a3b6aa", "#71897d")
EU2 = ("#b4c2a8", "#7f9471")
DRY = ("#d4b689", "#a77c4a")
DRY2 = ("#c9a36f", "#8f6538")


def branch(art, W, H, pts, rng, nx, leaf_r=(20, 30), every=0.11, cols=EU, start=0.06, side=1):
    art, _ = stem(art, W, H, pts, 4.2, rng, nx)
    n = len(pts)
    t = start; k = 0
    while t < 0.97:
        i = min(n - 2, int(t * (n - 1)))
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        a = math.atan2(y1 - y0, x1 - x0)
        r = rng.uniform(*leaf_r) * (1 - 0.45 * t)
        for sg in (1, -1):
            if rng.random() < 0.12:
                continue
            art, _ = euca_leaf(art, W, H, x0, y0, r * rng.uniform(0.85, 1.1), a + sg * rng.uniform(0.75, 1.25), rng, nx, cols=cols)
        if k % 3 == 2:
            clear()
        t += every * rng.uniform(0.8, 1.2); k += 1
    # tip: two tiny leaves
    x, y = pts[-1]
    a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    art, _ = euca_leaf(art, W, H, x, y, leaf_r[0] * 0.45, a + 0.4, rng, nx, cols=cols)
    art, _ = euca_leaf(art, W, H, x, y, leaf_r[0] * 0.38, a - 0.5, rng, nx, cols=cols)
    return art


def pods(art, W, H, base, ang, rng, nx, n=6, L=90):
    x, y = base
    tip = (x + math.cos(ang) * L, y + math.sin(ang) * L)
    pts = bez(base, (x + math.cos(ang + 0.3) * L * 0.5, y + math.sin(ang + 0.3) * L * 0.5), tip, 20)
    art, _ = stem(art, W, H, pts, 2.4, rng, nx)
    items, twigs = [], []
    for k in range(n):
        p = pts[int(4 + k / n * 15)]
        a = ang + (0.9 if k % 2 else -0.9) + rng.uniform(-0.2, 0.2)
        q = (p[0] + math.cos(a) * 12, p[1] + math.sin(a) * 12)
        twigs.append(([p, q], 1.4, None))
        items.append((q[0], q[1], rng.uniform(4.2, 6.0)))
    art = G(art, strokes(W, H, twigs), "#6b6a4c", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    return berries(art, W, H, items, rng, nx)


if "ranting" in PARTS:
    # long diagonal flat-lay: eucalyptus stems + seeded pods + dried leaves, reads bottom-left -> top-right
    W, H = 900, 600
    nx = Seq(1100); rng = random.Random(11)
    art = blank(W, H)
    # dried leaves first (they lie under the fresh branches)
    art, _ = dried_leaf(art, W, H, 120, 520, 340, 78, -0.42, rng, nx, cols=DRY, curl=0.15)
    art, _ = dried_leaf(art, W, H, 230, 590, 270, 62, -0.98, rng, nx, cols=DRY2, curl=-0.2)
    art, _ = dried_leaf(art, W, H, 430, 380, 230, 52, -0.12, rng, nx, cols=DRY, curl=0.25)
    art, _ = dried_leaf(art, W, H, 560, 300, 200, 46, -0.85, rng, nx, cols=DRY2, curl=-0.15)
    clear()
    art = pods(art, W, H, (300, 460), -0.62, rng, nx, n=8, L=130)
    art = branch(art, W, H, curve([(20, 590), (240, 460), (520, 320), (880, 110)], 90), rng, nx, leaf_r=(34, 46), every=0.075)
    clear()
    art = branch(art, W, H, curve([(330, 420), (500, 430), (680, 370), (860, 380)], 60), rng, nx, leaf_r=(22, 30), every=0.1, cols=EU2)
    art = branch(art, W, H, curve([(150, 520), (170, 400), (250, 300), (300, 240)], 40), rng, nx, leaf_r=(20, 26), every=0.14, cols=EU2)
    art = pods(art, W, H, (640, 270), -1.2, rng, nx, n=6, L=90)
    clear()
    prev(art, "ss-ranting", tone=BG)
    save(art, f"{OUT}/ranting.webp", max_w=700, quality=80)

if "segel" in PARTS:
    W = H = 420
    nx = Seq(2100); rng = random.Random(21)
    cx = cy = 210
    # pressed ring of tiny leaves around the monogram well (relief only)
    lv = []
    for k in range(26):
        a = k / 26 * math.tau
        x, y = cx + math.cos(a) * 122, cy + math.sin(a) * 122
        sg = 1 if k % 2 else -1
        lv.append((x + math.cos(a + math.pi / 2 + sg * 0.5) * 9, y + math.sin(a + math.pi / 2 + sg * 0.5) * 9, 13, 5.2, math.degrees(a + math.pi / 2 + sg * 0.5)))
    ring_items = np.maximum(ellipses(W, H, lv), np.clip(circles(W, H, [(cx, cy, 123)]) - circles(W, H, [(cx, cy, 120.5)]), 0, 1))
    art, blob = wax_seal(W, H, cx, cy, 168, rng, base="#869a78", deep="#5d6f50", hi="#d6dfc8", ring_items=ring_items, seed=nx())
    art = G(art, blob * (fbm(W, H, 77, 30, 3) > 0.6) * 0.5, "#4f6243", seed=nx(), density=0.25, edge=0.1, bloom=0.3, rough=3, feather=4)
    # a short eucalyptus sprig tucked under the seal (painted behind)
    back = blank(W, H)
    back = branch(back, W, H, curve([(20, 400), (90, 330), (150, 300)], 30), rng, nx, leaf_r=(16, 22), every=0.2)
    back = knockout(back, blob, 1.0, 1.0)
    art = over(back, art)
    prev(art, "ss-segel", tone=BG)
    save(art, f"{OUT}/segel.webp", max_w=300, quality=84)

if "divider" in PARTS:
    W, H = 560, 130
    nx = Seq(3100); rng = random.Random(31)
    art = blank(W, H)
    art, _ = dried_leaf(art, W, H, 280, 70, 120, 26, math.pi - 0.08, rng, nx, cols=DRY, curl=0.1)
    art, _ = dried_leaf(art, W, H, 276, 72, 110, 24, -0.06, rng, nx, cols=DRY2, curl=-0.1)
    art = branch(art, W, H, curve([(110, 82), (220, 60), (330, 58), (450, 70)], 40), rng, nx, leaf_r=(12, 16), every=0.12)
    prev(art, "ss-divider", tone=BG)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)

if "daun" in PARTS:
    W, H = 200, 110
    nx = Seq(4100); rng = random.Random(41)
    art = blank(W, H)
    art, _ = dried_leaf(art, W, H, 14, 80, 170, 40, -0.3, rng, nx, cols=DRY, curl=0.2)
    prev(art, "ss-daun", tone=BG)
    save(art, f"{OUT}/daun.webp", max_w=110, quality=86)

if "tangkai" in PARTS:
    W, H = 300, 620
    nx = Seq(5100); rng = random.Random(51)
    art = blank(W, H)
    art, _ = dried_leaf(art, W, H, 150, 600, 300, 60, -1.85, rng, nx, cols=DRY2, curl=0.2)
    art = branch(art, W, H, curve([(160, 610), (130, 420), (170, 220), (140, 30)], 60), rng, nx, leaf_r=(26, 34), every=0.09)
    art = pods(art, W, H, (150, 470), -1.1, rng, nx, n=5, L=90)
    prev(art, "ss-tangkai", tone=BG)
    save(art, f"{OUT}/tangkai.webp", max_w=210, quality=82)

if "linen" in PARTS:
    N = 512
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    weft = wrap_noise(N, N, 3, (0.6, 30))  # slubs along threads
    warp = wrap_noise(N, N, 4, (30, 0.6))
    th = 128  # threads per tile
    wx = 0.5 + 0.5 * np.sin(xx / N * th * math.tau)
    wy = 0.5 + 0.5 * np.sin(yy / N * th * math.tau)
    check = ((np.floor(xx / N * th) + np.floor(yy / N * th)) % 2).astype(np.float32)
    tex = (wx * (0.5 + warp) * check + wy * (0.5 + weft) * (1 - check))
    tex = (tex - tex.mean()) / (tex.std() + 1e-6)
    mott = wrap_noise(N, N, 9, 40)
    base = np.array(hex_rgb(BG), np.float32)
    rgb = base[None, None, :] * (1 + tex[..., None] * 0.028 + (mott[..., None] - 0.5) * 0.04)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((N, N, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/linen.webp", size=(256, 256), quality=78)
    on = to_image(arr).convert("RGB"); on.save(f"{PREV}/ss-linen.png")
