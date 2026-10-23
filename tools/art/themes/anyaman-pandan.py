"""Anyaman Pandan — woven pandan mats (tikar) of the Nusantara: a natural straw plait tile, a colourful dyed-strip
pattern band (diamonds of saga red, leaf green, soot black and turmeric on straw) with bound hems, a round rattan-coiled
tampah rim, a bundle of fresh and dried pandan blades, a small woven-diamond divider. No figures, no calligraphy.
Run: python3 -I anyaman-pandan.py [part ...]   parts: mat band tampah pandan divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o5_lib import *

OUT = outdir("anyaman-pandan")
PARTS = sys.argv[1:] or ["mat", "band", "tampah", "pandan", "divider"]
STRAW, STRAW_L, STRAW_D = "#d8bb80", "#ead39f", "#b8945a"
RED, GREEN, BLACK, TURM = "#b02a48", "#2f6b4a", "#2b2118", "#dfa227"
RATTAN, RATTAN_D, RATTAN_L = "#b07a3e", "#7a5022", "#d4a466"
LEAF, LEAF_D, LEAF_L = "#4f8a3a", "#2f5e2a", "#7fae56"


def mat():
    T = 288
    pal = [STRAW, STRAW_L, STRAW_D]
    art = weave(T, T, 6, lambda k: pal[k % 3], lambda k: pal[(k + 1) % 3], seed=4, fibre=0.8)
    art = add_grain(art, 5, 0.03)
    save_rgb(art, f"{OUT}/mat.webp", quality=74)
    preview(art, "ap-mat")


SEQ = [STRAW, STRAW, RED, RED, BLACK, TURM, TURM, BLACK, RED, RED, STRAW, GREEN]


def band():
    Wd, Hd = 480, 120
    n = 12  # strips per width: multiple of len(SEQ) keeps the pattern seamless
    art = weave(Wd, Hd, n, lambda k: SEQ[k % 12], lambda k: SEQ[(k + 6) % 12], seed=8, fibre=0.7)
    # bound hems: rolled rattan-coloured edge with a red cloth tape and stitches
    for y0, y1 in ((0, 14), (Hd - 14, Hd)):
        hem = rect(Wd, Hd, 0, y0, Wd, y1)
        art = P(art, hem, RED, "#9a2240", seed=11 + y0, rough=0.2, streak=1.5)
        st = strokes(Wd, Hd, [([(x, y0 + 3), (x + 5, y1 - 3)], 1.6, None) for x in range(4, Wd, 12)])
        art = tint(art, st, STRAW_L, 0.85)
        art = tint(art, rect(Wd, Hd, 0, y1 - 2 if y0 == 0 else y0, Wd, y1 if y0 == 0 else y0 + 2), BLACK, 0.5)
    art = add_grain(art, 6, 0.03)
    save_rgb(art, f"{OUT}/band.webp", quality=78)
    preview(art, "ap-band")


def tampah():
    S = 640
    nx = Seq(300); rng = random.Random(3)
    cx = cy = S / 2
    R0, R1 = 252, 312
    art = blank(S, S)
    ring = np.clip(circles(S, S, [(cx, cy, R1)]) - circles(S, S, [(cx, cy, R0)]), 0, 1)
    art = P(art, ring, RATTAN, RATTAN_L, seed=nx(), rough=1.2)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.hypot(xx - cx, yy - cy); th = np.arctan2(yy - cy, xx - cx)
    # coils: concentric ridges
    coil = 0.5 + 0.5 * np.cos((rr - R0) / (R1 - R0) * math.pi * 2 * 3)
    art = tint(art, ring * (coil > 0.75) * 1.0, RATTAN_D, 0.35)
    art = tint(art, ring * (coil < 0.2), RATTAN_L, 0.4)
    # diagonal wrapping stitches (split rattan binding) across each coil
    st = 0.5 + 0.5 * np.sin(th * 96 + (rr - R0) * 0.25)
    art = tint(art, ring * (st > 0.82), RATTAN_D, 0.45)
    art = tint(art, ring * (st < 0.12), "#e8c690", 0.35)
    # dyed binding accent: a red and a green coil
    for r_, col in ((R0 + 12, RED), (R1 - 12, GREEN)):
        band_ = np.clip(1 - np.abs(rr - r_) / 4.5, 0, 1) * ring
        art = P(art, band_, col, seed=nx(), rough=0.4)
        art = tint(art, band_ * (st > 0.7), BLACK, 0.3)
    # inner lip shadow + outer rim
    art = tint(art, edge_ring(ring, 2.0), RATTAN_D, 0.7)
    inner_sh = np.clip(1 - (rr - R0 + 18) / 18, 0, 1) * (rr < R0) * (rr > R0 - 18)
    art = tint(art, inner_sh.astype(np.float32), "#5a3a1a", 0.25)
    save_full(art, f"{OUT}/tampah.webp", size=(480, 480), quality=80)
    preview(art, "ap-tampah")


def pandan():
    Wd, Hd = 560, 520
    nx = Seq(500); rng = random.Random(6)
    art = blank(Wd, Hd)
    base = (120, 520)
    # dried straw strips behind (cream, curling)
    dried = []
    for k in range(5):
        a = -1.25 + k * 0.17 + rng.uniform(-0.05, 0.05)
        L = rng.uniform(330, 420)
        pts = curve([base, (base[0] + math.cos(a) * L * 0.5, base[1] + math.sin(a) * L * 0.5), (base[0] + math.cos(a + 0.35) * L, base[1] + math.sin(a + 0.35) * L)], 30)
        dried.append(shapes(Wd, Hd, [blade(Wd, Hd, pts, 7)]))
    dm = np.clip(sum(dried), 0, 1)
    art = P(art, dm, STRAW_L, STRAW, seed=nx(), rough=0.8)
    art = tint(art, edge_ring(dm, 1.2), STRAW_D, 0.7)
    # fresh pandan blades, long, keeled (fold line), fanning
    for k in range(9):
        a = -1.95 + k * 0.2 + rng.uniform(-0.06, 0.06)
        L = rng.uniform(300, 470)
        bend = rng.uniform(0.2, 0.5) * (1 if k > 4 else -1)
        pts = curve([base, (base[0] + math.cos(a) * L * 0.55, base[1] + math.sin(a) * L * 0.55), (base[0] + math.cos(a + bend) * L, base[1] + math.sin(a + bend) * L)], 32)
        poly = blade(Wd, Hd, pts, rng.uniform(14, 19))
        m = shapes(Wd, Hd, [poly])
        c1, c2 = ((LEAF, LEAF_L), (LEAF_D, LEAF), (LEAF, LEAF_D))[k % 3]
        art = P(art, m, c1, c2, seed=nx(), rough=0.9)
        half = shapes(Wd, Hd, [poly[:len(pts)] + pts[::-1]]) * m
        art = W(art, half, LEAF_D, seed=nx(), density=0.45, edge=0.2, rough=1.5)
        art = tint(art, strokes(Wd, Hd, [(pts[1:-2], 1.6, (0.05, 0.4))]), "#cfe0a0", 0.6)
        art = tint(art, edge_ring(m, 1.2), "#1f3f1c", 0.5)
    clear()
    # binding: a strip of red cloth tied round the bundle
    tie = shapes(Wd, Hd, [rot([(base[0] - 30, 470), (base[0] + 34, 470), (base[0] + 30, 488), (base[0] - 34, 488)], base[0], 480, -0.25)], smooth=False)
    art = P(art, tie, RED, "#c43a58", seed=nx(), rough=0.5)
    tail = strokes(Wd, Hd, [(curve([(base[0] + 30, 476), (base[0] + 70, 470), (base[0] + 96, 500)], 12), 7, (0.0, 0.5)), (curve([(base[0] + 30, 482), (base[0] + 60, 500), (base[0] + 64, 518)], 12), 7, (0.0, 0.5))])
    art = P(art, tail, RED, seed=nx(), rough=0.5)
    save(art, f"{OUT}/pandan.webp", max_w=360, quality=80)
    preview(art, "ap-pandan")


def divider():
    Wd, Hd = 460, 120
    nx = Seq(700)
    cx, cy = Wd / 2, Hd / 2
    full = weave(Wd, Hd, 18, lambda k: SEQ[k % 12], lambda k: SEQ[(k + 6) % 12], seed=12, fibre=0.7, wrap=False, cell=8.5)
    dia = shapes(Wd, Hd, [[(cx, cy - 46), (cx + 46, cy), (cx, cy + 46), (cx - 46, cy)]], smooth=False)
    dia = displace(dia, 3, 1.2, 12)
    art = full.copy(); art[..., 3] = dia
    art = tint(art, edge_ring(dia, 1.6), BLACK, 0.8)
    # straw strips running out to both sides, tapering
    for sgn in (-1, 1):
        for dy, L in ((-5, 170), (5, 150)):
            pts = curve([(cx + sgn * 40, cy + dy), (cx + sgn * (40 + L * 0.5), cy + dy * 1.3), (cx + sgn * (40 + L), cy + dy * 0.4)], 20)
            m = shapes(Wd, Hd, [blade(Wd, Hd, pts, 3.6)])
            art = P(art, m, STRAW, STRAW_L, seed=nx(), rough=0.4)
            art = tint(art, edge_ring(m, 1.0), STRAW_D, 0.8)
        art = P(art, circles(Wd, Hd, [(cx + sgn * 64, cy, 4.2)]), RED, seed=nx(), rough=0.3)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
    preview(art, "ap-divider")


for p in PARTS:
    globals()[p]()
    clear()
