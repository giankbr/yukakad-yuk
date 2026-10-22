"""Pualam Hitam — polished Nero Marquina black marble with inlaid brass/gold strips: 8-point khatam stars, an
interlaced octagon medallion, chamfered-octagon photo frames, a repeat-x inlay band. No figures, no calligraphy.
Run: python3 -I pualam-hitam.py [part ...]   parts: marble band medallion frame divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d3_lib import *  # noqa

OUT = outdir("pualam-hitam")
PARTS = sys.argv[1:] or ["marble", "band", "medallion", "frame", "divider"]
GOLD = "#c7a256"


def interlace(W, H, layers, width, cut=2.2):
    """layers: list of polygon lists drawn in order; each later layer gets a dark seam (cut) where it crosses the
    earlier ones so the strips read as laid over/under. Returns combined strip mask and seam mask."""
    total = np.zeros((H, W), np.float32)
    seam = np.zeros((H, W), np.float32)
    for polys in layers:
        m = outline(W, H, polys, width)
        edge = np.clip(outline(W, H, polys, width + cut * 2) - m, 0, 1)
        seam = np.maximum(seam * (1 - m), edge * total)
        total = np.maximum(total, m)
    return total, seam


if "marble" in PARTS:
    art = marble(768, 768, seed=8101, veins=0.62, web=0.5, vein="#cfc9be")
    preview(art, "ph-marble")
    save_full(art, f"{OUT}/marble.webp", quality=74)
    clear()

if "band" in PARTS:
    W, H = 320, 110
    bg = marble(W, H, seed=8201, veins=0.7, web=0.6)
    cy = H / 2
    layers = [
        [[(0, 9), (W, 9)], [(0, H - 9), (W, H - 9)]],
        [star8(x, cy, 36, rot=math.pi / 8) for x in (80, 240)],
        [ngon(x, cy, 18, 4) for x in (0, 160, 320)],
        [[(80 + 36 * math.cos(a), cy + 36 * math.sin(a)) for a in (0,)] + [(160 - 18, cy)] for _ in (0,)],
    ]
    # connectors: from star tips to the diamonds (zig-zag interlace)
    conn = []
    for x in (80, 240):
        for sg in (-1, 1):
            tip = (x + sg * 36 * math.cos(math.pi / 8), cy + 36 * math.sin(math.pi / 8))
            tip2 = (x + sg * 36 * math.cos(math.pi / 8), cy - 36 * math.sin(math.pi / 8))
            conn.append([tip, (x + sg * 62, cy + 30), (x + sg * 80, cy + 30)])
            conn.append([tip2, (x + sg * 62, cy - 30), (x + sg * 80, cy - 30)])
    m1 = outline(W, H, layers[0][0:1] + layers[0][1:], 3.2, closed=False)
    ms, seam = interlace(W, H, [layers[1], layers[2]], 4.2)
    mc = outline(W, H, conn, 3.0, closed=False)
    seam = np.maximum(seam, np.clip(outline(W, H, conn, 7.4, closed=False) - mc, 0, 1) * ms)
    gold = np.clip(np.maximum.reduce([m1, ms * (1 - np.clip(outline(W, H, conn, 7.4, closed=False) - mc, 0, 1)), mc]), 0, 1)
    # small filled stars in the star centres, inlaid white calcite? keep brass only
    cores = fills(W, H, [star8(x, cy, 12, rot=math.pi / 8) for x in (80, 240)] + [ngon(x, cy, 6, 4) for x in (0, 160, 320)])
    gold = np.maximum(gold, cores)
    art = over(bg, brass(gold, GOLD, seed=8202, tile=True))
    preview(art, "ph-band")
    save_full(art, f"{OUT}/band.webp", size=(240, 82), quality=80)
    clear()

if "medallion" in PARTS:
    W = H = 620
    cx = cy = W / 2
    R = 290
    rings = [ngon(cx, cy, R, 96), ngon(cx, cy, R - 14, 96)]
    sq = [ngon(cx, cy, 232, 4, math.pi / 4), ngon(cx, cy, 232, 4, 0)]
    oct_ = [ngon(cx, cy, 150, 8, math.pi / 8)]
    inner = [star8(cx, cy, 108, rot=0)]
    smalls = [star8(cx + 226 * math.cos(k * math.pi / 4 + math.pi / 8), cy + 226 * math.sin(k * math.pi / 4 + math.pi / 8), 17, rot=math.pi / 8) for k in range(8)]
    strips, seam = interlace(W, H, [rings, sq[0:1], sq[1:2], oct_, inner], 6.5, cut=2.6)
    sp = outline(W, H, smalls, 3.6)
    spc = fills(W, H, [star8(x, y, 6, rot=math.pi / 8) for (x, y) in [(cx + 226 * math.cos(k * math.pi / 4 + math.pi / 8), cy + 226 * math.sin(k * math.pi / 4 + math.pi / 8)) for k in range(8)]])
    gold = np.maximum.reduce([strips, sp, spc])
    core = fills(W, H, [star8(cx, cy, 46, rot=math.pi / 8)])
    core_cut = fills(W, H, [ngon(cx, cy, 16, 8, math.pi / 8)])
    gold = np.maximum(gold, core * (1 - core_cut))
    dots = circles(W, H, [(cx + 276 * math.cos(k * math.pi / 8 + math.pi / 16), cy + 276 * math.sin(k * math.pi / 8 + math.pi / 16), 3.2) for k in range(16)])
    gold = np.maximum(gold, dots)
    art = brass(gold, GOLD, seed=8301)
    # seam = dark hairline where a strip passes under the next
    art[..., :3] *= (1 - seam * 0.85)[..., None]
    preview(art, "ph-medallion", bg="#111113")
    save(art, f"{OUT}/medallion.webp", max_w=440, quality=82)
    clear()

if "frame" in PARTS:
    W, H = 480, 620
    c = 96
    def cham(i, c=c):
        return [(c + i, i), (W - c - i, i), (W - i, c + i), (W - i, H - c - i), (W - c - i, H - i), (c + i, H - i), (i, H - c - i), (i, c + i)]
    lines = outline(W, H, [cham(6), cham(18)], 4.6)
    stars = []
    for (x, y) in [(c * 0.5 + 9, c * 0.5 + 9), (W - c * 0.5 - 9, c * 0.5 + 9), (c * 0.5 + 9, H - c * 0.5 - 9), (W - c * 0.5 - 9, H - c * 0.5 - 9)]:
        stars.append(star8(x, y, 22, rot=math.pi / 8))
    st = outline(W, H, stars, 3.6)
    stc = fills(W, H, [star8(x, y, 8, rot=math.pi / 8) for (x, y) in [(c * 0.5 + 9, c * 0.5 + 9), (W - c * 0.5 - 9, c * 0.5 + 9), (c * 0.5 + 9, H - c * 0.5 - 9), (W - c * 0.5 - 9, H - c * 0.5 - 9)]])
    mids = fills(W, H, [ngon(W / 2, 12, 9, 4), ngon(W / 2, H - 12, 9, 4), ngon(12, H / 2, 9, 4), ngon(W - 12, H / 2, 9, 4)])
    gold = np.clip(np.maximum.reduce([lines, st, stc, mids]), 0, 1)
    art = brass(gold, GOLD, seed=8401)
    preview(art, "ph-frame", bg="#111113")
    save_full(art, f"{OUT}/frame.webp", size=(360, 465), quality=82)
    i = 24
    print("clip:", ", ".join(f"{x / W * 100:.1f}% {y / H * 100:.1f}%" for x, y in cham(i, c - 3)))
    clear()

if "divider" in PARTS:
    W, H = 440, 64
    cy = H / 2
    ln = outline(W, H, [[(20, cy), (176, cy)], [(264, cy), (420, cy)]], 2.6, closed=False)
    st = outline(W, H, [star8(W / 2, cy, 24, rot=math.pi / 8)], 3.4)
    core = fills(W, H, [star8(W / 2, cy, 8, rot=math.pi / 8), ngon(186, cy, 6, 4), ngon(254, cy, 6, 4), ngon(14, cy, 5, 4), ngon(426, cy, 5, 4)])
    art = brass(np.maximum.reduce([ln, st, core]), GOLD, seed=8501)
    preview(art, "ph-divider", bg="#111113")
    save(art, f"{OUT}/divider.webp", max_w=440, quality=86)
    clear()

kb(OUT)
