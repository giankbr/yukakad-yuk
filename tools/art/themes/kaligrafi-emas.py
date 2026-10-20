"""Kaligrafi Emas — pressed gold-foil mihrab, khatam rosette (tezhip-style ochre/teal wash), crest, star,
hand-inked lattice texture and paper grain. Run: python3 -I /tmp/pen/art/themes/kaligrafi-emas.py"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentD_lib import *  # noqa

T = "kaligrafi-emas"
OUT = outdir(T)
GOLD = "#b8903e"
OCHRE, OCHRE2 = "#e2c48a", "#c99a52"
TEAL = "#3d6670"
rng = random.Random(11)
_s = [500]
def nxt():
    _s[0] += 13
    return _s[0]

def foilize(mask, seed, rough=0.8):
    """Foil with a slightly hand-cut edge (displaced), so lines are not vector-perfect."""
    m = np.clip((gaussian_filter(displace(mask, seed, rough, 22), 0.5) - 0.18) * 1.6, 0, 1)
    return foil(m, GOLD, seed=seed, emboss=0.55, sparkle=0.18)

# ---------------- 1. mihrab arch (border-image source) ----------------
W, H = 692, 760
sx = W / 300
def Y(y):
    return 14 + (y - 12) * (480 - 14) / 224 if y <= 236 else 480 + (y - 236) * 2.4
def arch_path(off):
    # outer: M12 600V236C12 138 86 86 150 12C214 86 288 138 288 236V600 ; inner offset by `off` units
    a, b = 12 + off, 288 - off
    top = 12 + off * 0.75
    return (f"M{a*sx} {H+20}V{Y(236)}C{a*sx} {Y(138+off*0.33)} {(86+off*0.45)*sx} {Y(86+off*0.55)} {150*sx} {Y(top)}"
            f"C{(214-off*0.45)*sx} {Y(86+off*0.55)} {b*sx} {Y(138+off*0.33)} {b*sx} {Y(236)}V{H+20}")
outer = svg_mask(W, H, arch_path(0), fill=False, stroke=4.2)
inner = svg_mask(W, H, arch_path(12), fill=False, stroke=2.2)
# ochre wash band between the two lines, only around the crown (fades out down the pillars)
band_shape = svg_mask(W, H, arch_path(6), fill=False, stroke=12 * sx * 0.95)
yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
band_shape *= np.clip(1 - (yy - 430) / 140, 0, 1)
art = pigment(band_shape, OCHRE, OCHRE2, seed=nxt(), density=0.62, edge=0.6, bloom=0.35, gran=0.4, rough=2.0, feather=0.9)
# small knotwork beads on the band, regularly spaced along the crown (hand placed)
beads = []
lozenges = []
for n_, t in enumerate(np.linspace(0.04, 0.96, 27)):
    # sample along the band path by evaluating the bezier halves
    import numpy as _np
    def bez(p0, p1, p2, p3, u):
        return tuple((1-u)**3*p0[i] + 3*(1-u)**2*u*p1[i] + 3*(1-u)*u*u*p2[i] + u**3*p3[i] for i in range(2))
    off = 6
    A = ((12+off)*sx, Y(236)); B = ((12+off)*sx, Y(138+off*0.33)); Cc = ((86+off*0.45)*sx, Y(86+off*0.55)); D = (150*sx, Y(12+off*0.75))
    if t < 0.5:
        x, y = bez(A, B, Cc, D, t * 2)
    else:
        A2 = (W - A[0], A[1]); B2 = (W - B[0], B[1]); C2 = (W - Cc[0], Cc[1])
        x, y = bez(A2, B2, C2, D, (1 - t) * 2)
    if abs(x - W / 2) > 26:
        if n_ % 2:
            beads.append((x + rng.gauss(0, .4), y + rng.gauss(0, .4), 3.6 + rng.uniform(-.4, .4)))
        else:
            lozenges.append(deform(ellipse_pts(x, y, 6.5, 6.5, 4, math.pi / 4 + rng.gauss(0, .05)), rng, 1, .04))
loz = np.zeros((H, W), np.float32)
for q in lozenges:
    loz = np.maximum(loz, shape_mask(W, H, q, smooth=False))
art = glaze(art, pigment(circle_mask(W, H, beads), TEAL, "#2f5560", seed=nxt(), density=0.55, edge=0.4, bloom=0, gran=0.3, rough=1.2, feather=0.6))
# springline knots + apex finial (8-point star) + bud
sp = Y(236)
knots = circle_mask(W, H, [(18 * sx, sp, 7), (W - 18 * sx, sp, 7)])
fin = shape_mask(W, H, star_pts(W / 2, 16, 15, 8), smooth=False)
gold = np.clip(outer + inner + knots + loz, 0, 1)
gold = knockout_m = np.clip(gold - gaussian_filter(fin, 2) * 2, 0, 1)
art = over(art, foilize(gold, nxt()))
art = over(art, foilize(fin, nxt(), rough=0.6))
save_plain(art, f"{OUT}/arch.webp", quality=82)
preview(art, paper_tone="#f7f0e1", path=f"{PREV}/ke-arch.png")

# ---------------- 2. khatam rosette ----------------
S = 340; c = S / 2; k = 3.2
sq = outline_mask(S, S, [square_pts(c, c, 32 * k), square_pts(c, c, 32 * k, math.pi / 4)], 2.6, rng=rng, wobble=0.5)
st_out = outline_mask(S, S, [star_pts(c, c, 46 * k, 30 * k)], 2.2, rng=rng, wobble=0.5)
st_mid_shape = shape_mask(S, S, star_pts(c, c, 30 * k, 19 * k), smooth=False)
st_mid = outline_mask(S, S, [star_pts(c, c, 30 * k, 19 * k)], 2.6, rng=rng, wobble=0.4)
ring = circle_mask(S, S, [(c, c, 12 * k)], stroke=2.6)
dots = circle_mask(S, S, [(c + math.cos(a) * 39 * k, c + math.sin(a) * 39 * k, 4.2) for a in [i * math.pi / 4 - math.pi / 2 for i in range(8)]]
                   + [(c, c, 6.5)])
dot_ring = circle_mask(S, S, [(c + math.cos(a) * 49.5 * k, c + math.sin(a) * 49.5 * k, 1.6) for a in np.linspace(0, math.tau, 72, endpoint=False)])
ros = pigment(st_mid_shape, OCHRE, OCHRE2, seed=nxt(), density=0.7, edge=0.55, bloom=0.35, gran=0.4, rough=2.5, feather=1.0)
disc = circle_mask(S, S, [(c, c, 12 * k - 2)])
ros = glaze(ros, pigment(disc, TEAL, "#4e7a80", seed=nxt(), density=0.6, edge=0.55, bloom=0.2, gran=0.45, rough=1.6, feather=0.8))
g = np.clip(sq + st_out + st_mid + ring + dots, 0, 1)
ros = over(ros, foilize(g, nxt(), rough=0.9))
ros = over(ros, foil(dot_ring, GOLD, seed=nxt(), emboss=0.3, sparkle=0))
print("rosette", save_asset(ros, f"{OUT}/rosette.webp", max_w=240, quality=84))
preview(ros, paper_tone="#f7f0e1", path=f"{PREV}/ke-rosette.png")

# ---------------- 3. small star ----------------
S2 = 96; c2 = S2 / 2
sm = np.clip(shape_mask(S2, S2, square_pts(c2, c2, 26), smooth=False) + shape_mask(S2, S2, square_pts(c2, c2, 26, math.pi / 4), smooth=False), 0, 1)
sm *= 1 - circle_mask(S2, S2, [(c2, c2, 10)])
star = foil(np.clip((gaussian_filter(displace(sm, nxt(), 1.0, 10), .5) - .2) * 1.5, 0, 1), GOLD, seed=nxt(), emboss=0.8, sparkle=0.1)
print("star", save_asset(star, f"{OUT}/star.webp", max_w=72, quality=86))

# ---------------- 4. portrait crest ----------------
CW, CH = 480, 168; kx = CW / 120
crest_l = svg_mask(CW, CH, ["M2 38C24 38 40 26 60 4C80 26 96 38 118 38"], scale=kx, ty=4, fill=False, stroke=3.0)
crest_i = svg_mask(CW, CH, ["M18 38C34 36 46 28 60 14C74 28 86 36 102 38"], scale=kx, ty=4, fill=False, stroke=1.8)
cband = svg_mask(CW, CH, ["M2 38C24 38 40 26 60 4C80 26 96 38 118 38L102 38C86 36 74 28 60 14C46 28 34 36 18 38Z"], scale=kx, ty=4)
cr = pigment(cband, OCHRE, OCHRE2, seed=nxt(), density=0.5, edge=0.5, bloom=0.3, gran=0.35, rough=2, feather=0.9)
cdots = circle_mask(CW, CH, [(60 * kx, 4 * kx + 4, 9), (2 * kx, 38 * kx + 4, 6), (118 * kx, 38 * kx + 4, 6)])
cfin = shape_mask(CW, CH, star_pts(60 * kx, 4 * kx + 4, 14, 7.5), smooth=False)
cr = over(cr, foilize(np.clip(crest_l + crest_i + cdots * 0 , 0, 1), nxt()))
cr = over(cr, foilize(np.clip(cfin + circle_mask(CW, CH, [(2 * kx + 2, 38 * kx + 4, 6), (118 * kx - 2, 38 * kx + 4, 6)]), 0, 1), nxt(), rough=0.5))
save_plain(cr, f"{OUT}/crest.webp", quality=84)
preview(cr, paper_tone="#f7f0e1", path=f"{PREV}/ke-crest.png")

# ---------------- 5. inked lattice texture (transparent, seamless, 4x4 cells of 44 css px @2x) ----------------
L = 352; u = L / 176  # 2 px per css px
def lat(cv):
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=1.7, Style=skia.Paint.kStroke_Style, StrokeJoin=skia.Paint.kRound_Join)
    r = random.Random(4)
    for i in range(4):
        for j in range(4):
            ox, oy = i * 44 * u, j * 44 * u
            jit = lambda v: v + r.gauss(0, 0.45)
            cv.c.drawPath(poly_path([(jit(ox + 13 * u), jit(oy + 13 * u)), (jit(ox + 31 * u), jit(oy + 13 * u)), (jit(ox + 31 * u), jit(oy + 31 * u)), (jit(ox + 13 * u), jit(oy + 31 * u))]), p)
            cv.c.drawPath(poly_path([(jit(ox + 22 * u), jit(oy + 9.3 * u)), (jit(ox + 34.7 * u), jit(oy + 22 * u)), (jit(ox + 22 * u), jit(oy + 34.7 * u)), (jit(ox + 9.3 * u), jit(oy + 22 * u))]), p)
            for (a, b, c_, d) in [(0, 22, 9.3, 22), (34.7, 22, 44, 22), (22, 0, 22, 9.3), (22, 34.7, 22, 44)]:
                cv.c.drawLine(ox + a * u, oy + b * u, ox + c_ * u, oy + d * u, p)
lm = wrap_draw(L, L, lat)
lm = np.tile(lm, (3, 3))
lt = pigment(lm, "#9c7630", "#b8903e", seed=nxt(), density=0.9, edge=0.3, bloom=0.25, gran=0.3, rough=0.8, feather=0.5, mottle=0.7)[L:2 * L, L:2 * L]
save_plain(lt, f"{OUT}/lattice.webp", quality=80)
preview(np.tile(lt, (2, 2, 1)), paper_tone="#f7f0e1", path=f"{PREV}/ke-lattice.png")

# ---------------- 6. neutral paper grain (multiply over theme colours) ----------------
pp = seamless_paper(512, 512, "#fdfbf7", seed=21, mottle=0.4, fiber=0.8, fine=0.8)
save_plain(pp, f"{OUT}/paper.webp", quality=80)

tot = 0
for f in sorted(os.listdir(OUT)):
    tot += kb(f"{OUT}/{f}"); print(f, kb(f"{OUT}/{f}"), "KB", Image.open(f"{OUT}/{f}").size)
print("total", round(tot, 1), "KB")
