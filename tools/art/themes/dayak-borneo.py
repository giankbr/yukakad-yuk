"""Dayak Borneo — woodcut/linocut black-and-bone print + gouache accents (hornbill, sulur, talawang, manik beads).
Run: python3 -I /tmp/pen/art/themes/dayak-borneo.py
Assets → /root/w/frontend/public/themes/art/dayak-borneo/
  enggang-tail.webp / enggang-body.webp / enggang-branch.webp   hornbill, split for perch + tail sway
                      (same 528x330 canvas each, stacked with inset:0)   css 260x162
  sulur-tosca.webp / sulur-kuning.webp   vine scroll divider            css 150x40 → 330px
  talawang.webp       shield plate for monograms                        css 150x250 → 300px
  beads-v.webp / beads-h.webp   manik bead strand tiles (4 repeats)      css 14x112 → 28x224
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g_util import *

OUT = outdir("dayak-borneo")
rng = random.Random(31)
nx = Seq(900)
BLACK, RIMBA, RIMBA2, KUNING, MERAH, PUTIH, TOSCA = "#0c1412", "#10221e", "#173a32", "#efb02a", "#c4302a", "#f1ebdd", "#1f8a84"

# ---------------- enggang ----------------
S = 2.2; W, H = 528, 330
def M(d, stroke=None, wob=0.7):
    return svg_mask(W, H, d, scale=S, stroke=stroke * S if stroke else None, wob=wob, seed=nx())

# tail: bone feathers with black woodcut bands
tail = blank(W, H)
f1 = M("M80 97 C 54 104 28 114 3 133 C 30 127 56 117 82 108 Z", wob=0.9)
f2 = M("M78 104 C 54 114 34 126 15 145 C 40 135 60 123 84 110 Z", wob=0.9)
tail = over(tail, gouache_paint(np.maximum(f1, f2), PUTIH, "#ddd3bf", seed=nx(), rough=1.2, streak=1.2))
bands = np.zeros((H, W), np.float32)
for d in ["M62 105 L 50 112", "M46 111 L 34 119", "M30 117 L 20 124", "M60 116 L 50 124", "M45 124 L 36 132", "M30 131 L 24 137"]:
    bands = np.maximum(bands, M(d, stroke=3.4, wob=0.6))
outline = np.maximum(M("M80 97 C 54 104 28 114 3 133 C 30 127 56 117 82 108", stroke=0.9), M("M78 104 C 54 114 34 126 15 145 C 40 135 60 123 84 110", stroke=0.9))
tail = over(tail, linocut(np.maximum(bands, outline), BLACK, seed=nx(), wear=0.3, rough=1.2))

# body / neck / head (black woodcut) with bone carved outline, wing with gold sulur, beak + casque gouache
body = blank(W, H)
torso = M("M69 94 C 80 69 122 61 150 71 C 165 76 171 88 162 101 C 150 115 108 121 84 113 C 71 109 65 102 69 94 Z", wob=1.0)
head = M("M145 75 C 151 60 168 51 180 57 C 189 62 190 74 182 81 C 174 87 162 87 155 85 Z", wob=0.8)
blk = np.maximum(torso, head)
body = over(body, linocut(blk, BLACK, seed=nx(), wear=0.18))
# carved (white-line) outline: thin bone lines just inside the silhouette, broken like a gouge
cut = np.maximum(M("M72 94 C 82 72 122 64 149 74 C 162 79 167 89 160 99", stroke=1.1, wob=0.9),
                 M("M149 75 C 154 63 168 55 179 60", stroke=1.0, wob=0.8))
cut = np.maximum(cut, M("M90 108 C 110 114 140 110 156 100", stroke=0.9, wob=0.9))
body = over(body, linocut(cut, PUTIH, seed=nx(), wear=0.55, rough=1.0))
# feather gouges on the breast
gouge = np.zeros((H, W), np.float32)
for i in range(7):
    x = 96 + i * 8
    gouge = np.maximum(gouge, M(f"M{x} {106 + (i % 2)} q 3 3 6 0", stroke=0.9, wob=0.4))
body = over(body, linocut(gouge, "#6f7a72", seed=nx(), wear=0.5))
wing = M("M86 94 C 102 78 132 72 154 80 C 140 94 114 104 86 104 Z", wob=0.8)
body = over(body, gouache_paint(wing, RIMBA2, "#21493f", seed=nx(), rough=1.0, streak=1.2))
wl = np.maximum(M("M86 94 C 102 78 132 72 154 80 C 140 94 114 104 86 104 Z", stroke=1.2),
                M("M100 96 C 104 88 114 86 118 92 C 120 96 114 98 112 94 M124 90 C 128 82 138 82 140 88 C 141 92 136 93 135 90", stroke=1.4))
body = over(body, linocut(wl, KUNING, seed=nx(), wear=0.35, rough=0.8))
beak = M("M180 63 C 200 60 222 70 235 93 C 218 82 200 77 182 77 Z", wob=0.7)
body = over(body, gouache_paint(beak, KUNING, "#d8901c", seed=nx(), rough=1.0, streak=1.0))
body = over(body, gouache_paint(M("M200 70 C 214 74 226 82 232 90 C 220 84 208 80 196 78 Z", wob=0.5), "#f6d27a", seed=nx(), rough=0.6, density=0.7))
casque = M("M175 58 C 184 41 210 39 227 54 C 229 61 222 63 218 57 C 208 50 194 52 184 64 Z", wob=0.7)
body = over(body, gouache_paint(casque, MERAH, "#a52520", seed=nx(), rough=1.0, streak=1.0))
body = over(body, gouache_paint(M("M218 56 C 222 49 229 49 231 54", stroke=2.6), MERAH, seed=nx(), rough=0.6))
body = over(body, linocut(np.maximum(M("M180 63 C 200 60 222 70 235 93", stroke=0.8), M("M184 64 C 194 52 208 50 218 57", stroke=0.8)), BLACK, seed=nx(), wear=0.3))
body = over(body, gouache_paint(circle_mask(W, H, 174 * S, 66 * S, 3.3 * S), PUTIH, seed=nx(), rough=0.4))
body = over(body, gouache_paint(circle_mask(W, H, 174.8 * S, 66 * S, 1.7 * S), BLACK, seed=nx(), rough=0.3))
body = over(body, gouache_paint(M("M118 114 v10 M132 112 v12", stroke=2.6), KUNING, seed=nx(), rough=0.6))

branch = blank(W, H)
br = np.maximum(M("M38 126 C 90 121 160 121 216 128", stroke=3.2, wob=1.0), M("M186 127 C 196 120 204 120 210 113 M70 124 C 62 118 58 112 60 105", stroke=1.6, wob=0.8))
branch = over(branch, linocut(br, PUTIH, seed=nx(), wear=0.4, rough=1.2))
leaves = np.zeros((H, W), np.float32)
for (x, y, a, L) in [(60, 105, -2.0, 12), (210, 113, -0.9, 12), (200, 121, -0.3, 10), (48, 125, 2.9, 11)]:
    leaves = np.maximum(leaves, shape_mask(W, H, petal_pts(x * S, y * S, L * S, L * S * .36, a, n=10)))
branch = over(branch, gouache_paint(leaves, TOSCA, "#16706b", seed=nx(), rough=1.0))
for name, arr in [("tail", tail), ("body", body), ("branch", branch)]:
    save_full(arr, f"{OUT}/enggang-{name}.webp", quality=82)
bird = over(over(branch.copy(), tail), body)
preview(bird, "dy-bird", bg="#1a3a32")

# ---------------- sulur divider ----------------
W, H = 660, 176; S2 = 4.4
half = "M8 20 C 20 20 24 7 36 7 C 48 7 52 21 44 25 C 38 28 33 22 37 19 M14 21 C 25 23 29 34 41 34 C 51 34 55 27 51 23 M44 25 C 56 31 64 23 70 13 C 66 12 63 15 62 19"
for name, col, col2 in [("tosca", TOSCA, "#176e69"), ("kuning", KUNING, "#d29a1e")]:
    sl = blank(W, H)
    st = np.zeros((H, W), np.float32)
    for sx in (1, -1):
        st = np.maximum(st, svg_mask(W, H, half, scale=S2, sx=sx, tx=W / 2, ty=0, stroke=8.6, wob=1.0, seed=nx()))
    st = np.maximum(st, svg_mask(W, H, "M75 12 L82 20 L75 28 L68 20 Z", scale=S2, tx=W / 2 - 75 * S2, wob=0.7, seed=nx()))
    sl = over(sl, linocut(st, col, seed=nx(), wear=0.35, rough=1.4))
    sl = over(sl, gouache_paint(circle_mask(W, H, W / 2, 20 * S2, 2.2 * S2), MERAH, seed=nx(), rough=0.5))
    save(sl, f"{OUT}/sulur-{name}.webp", max_w=330)
    if name == "tosca":
        preview(sl, "dy-sulur", tone="#f8f2e3")

# ---------------- talawang shield ----------------
W, H = 300, 500; S3 = 2.5
def T(d, stroke=None, wob=0.8):
    return svg_mask(W, H, d, scale=S3, stroke=stroke * S3 if stroke else None, wob=wob, seed=nx())
sh = blank(W, H)
sh = over(sh, gouache_paint(T("M60 3 L117 30 V170 L60 197 L3 170 V30 Z"), KUNING, "#cf951f", seed=nx(), rough=1.2))
sh = over(sh, gouache_paint(T("M60 8 L112 33 V167 L60 192 L8 167 V33 Z"), RIMBA, RIMBA2, seed=nx(), rough=1.4, streak=1.3))
dash = np.zeros((H, W), np.float32)
for k in range(28):
    t = k / 28
    # walk the inner hexagon
    poly = [(60, 16), (106, 37), (106, 163), (60, 184), (14, 163), (14, 37), (60, 16)]
    seg = t * 6; i = int(seg); f = seg - i
    x = poly[i][0] + (poly[i + 1][0] - poly[i][0]) * f; y = poly[i][1] + (poly[i + 1][1] - poly[i][1]) * f
    dash = np.maximum(dash, circle_mask(W, H, x * S3, y * S3, 1.1 * S3))
sh = over(sh, gouache_paint(dash, PUTIH, seed=nx(), rough=0.4, density=0.85))
spir = np.zeros((H, W), np.float32)
for dir_ in (1, -1):
    for d in ["M6 -44 C 30 -44 36 -66 24 -72 C 16 -76 12 -66 18 -64", "M6 44 C 30 44 36 66 24 72 C 16 76 12 66 18 64"]:
        spir = np.maximum(spir, svg_mask(W, H, d, scale=S3, sx=dir_, tx=60 * S3, ty=100 * S3, stroke=2.6 * S3, wob=0.8, seed=nx()))
sh = over(sh, gouache_paint(spir, MERAH, "#a52520", seed=nx(), rough=1.0))
save_full(sh, f"{OUT}/talawang.webp")
preview(sh, "dy-shield", tone="#f8f2e3")

# ---------------- bead tiles ----------------
cols = [[KUNING, BLACK, KUNING], [BLACK, MERAH, BLACK], [MERAH, PUTIH, MERAH], [BLACK, TOSCA, BLACK], [TOSCA, PUTIH, TOSCA], [BLACK, MERAH, BLACK]]
TW, TH = 28, 224; reps = 4; step = 9.33
beads = blank(TW, TH)
rows = 6 * reps
for r in range(rows):
    for c in range(3):
        cx, cy = 5 + c * 9, 4.66 + r * step
        col = cols[r % 6][c]
        m = circle_mask(TW, TH, cx + rng.uniform(-.4, .4), cy + rng.uniform(-.3, .3), 4.1 + rng.uniform(-.3, .2))
        beads = over(beads, gouache_paint(m, col, mix(col, "#000000", .25), seed=nx(), rough=0.35, streak=0.3))
        hl = circle_mask(TW, TH, cx - 1.3, cy - 1.4, 1.1)
        beads = over(beads, gouache_paint(hl, "#ffffff", seed=nx(), rough=0.2, density=0.55))
save_full(beads, f"{OUT}/beads-v.webp", quality=84)
bh = np.ascontiguousarray(np.transpose(beads, (1, 0, 2)))
save_full(bh, f"{OUT}/beads-h.webp", quality=84)
preview(np.concatenate([beads] * 6, 1), "dy-beads", bg=RIMBA)
