"""Kaftan Ottoman — Ottoman silk brocade (catma / kemha): crimson satin ground, gold lame weft floats forming a large
ogival lattice with pomegranate-and-tulip medallions, cintamani (three dots + wavy lines) bands. No figures.
Run: python3 -I kaftan-ottoman.py [part ...]   parts: brocade medallion cintamani divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c2_lib import *

OUT = outdir("kaftan-ottoman")
PARTS = sys.argv[1:] or ["brocade", "medallion", "cintamani", "divider"]
CRIM, CRIM_D, CRIM_L = "#8e1420", "#5a0a12", "#b52a30"
GOLD, GOLD_L, GOLD_D = "#d7b35e", "#f3dc98", "#8a6424"
CREAM = "#f3e6c8"
NAVY = "#1f2c4a"


def pomegranate(path_draw, cx, cy, r):
    """Draw a stylised pomegranate (round body, crown of three tulip petals, carnation base) into a skia canvas via
    path_draw(kind, data). kind: fill | line(w) | dot."""
    body = ellipse_pts(cx, cy, r, r * 1.05, 28)
    path_draw("fill", body)
    # crown: three tulip-like petals on top
    for k, (dx, a, L) in enumerate([(0, -math.pi / 2, r * 0.75), (-r * 0.32, -math.pi / 2 - 0.5, r * 0.6), (r * 0.32, -math.pi / 2 + 0.5, r * 0.6)]):
        path_draw("fill", petal_pts(cx + dx * 0.4, cy - r * 0.92, L, L * 0.38, a, n=12))
    # base: carnation fan
    for k in range(7):
        a = math.pi / 2 + (k - 3) * 0.32
        path_draw("fill", petal_pts(cx, cy + r * 0.9, r * 0.55, r * 0.16, a, n=10))


def drawer(cv):
    pf = paint_white()
    def f(kind, data, w_=2.0):
        if kind == "fill":
            cv.c.drawPath(smooth_path(data), pf)
        elif kind == "line":
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=w_, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            cv.c.drawPath(smooth_path(data, closed=False), p)
        elif kind == "ring":
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=w_)
            cv.c.drawPath(smooth_path(data), p)
        elif kind == "dot":
            cv.c.drawCircle(data[0], data[1], data[2], pf)
    return f


def seeds_pattern(cx, cy, r, step):
    out = []
    for i in range(-6, 7):
        for j in range(-6, 7):
            x = cx + i * step + (j % 2) * step / 2; y = cy + j * step * 0.86
            if (x - cx) ** 2 + ((y - cy) / 1.05) ** 2 < (r * 0.72) ** 2:
                out.append((x, y, step * 0.26))
    return out


def saz(x, y, L, a, curl=0.35):
    """Serrated saz leaf polygon."""
    pts = []
    n = 18
    for i in range(n + 1):
        t = i / n
        w = math.sin(t * math.pi) * L * 0.16 * (1 + 0.25 * (i % 2))
        bend = curl * L * t * t
        px = x + math.cos(a) * L * t - math.sin(a) * bend
        py = y + math.sin(a) * L * t + math.cos(a) * bend
        pts.append((px - math.sin(a) * w, py + math.cos(a) * w))
    back = []
    for i in range(n, -1, -1):
        t = i / n
        w = math.sin(t * math.pi) * L * 0.12
        bend = curl * L * t * t
        px = x + math.cos(a) * L * t - math.sin(a) * bend
        py = y + math.sin(a) * L * t + math.cos(a) * bend
        back.append((px + math.sin(a) * w, py - math.cos(a) * w))
    return pts + back


if "brocade" in PARTS:
    S = 400
    nx = Seq(60100)
    ground = silk(S, S, CRIM, CRIM_D, seed=nx(), pitch=2.0, drape=0.55, bands=1)
    # ogival lattice: two mirrored sine curves per tile -> ogee cells; drawn as a double band with a vine inside
    ys = np.linspace(-S * 0.1, S * 1.1, 160)
    Lc = [(S / 4 + S / 4 * math.sin(2 * math.pi * y / S), y) for y in ys]
    Rc = [(3 * S / 4 - S / 4 * math.sin(2 * math.pi * y / S), y) for y in ys]
    def lattice(cv):
        f = drawer(cv)
        for c in (Lc, Rc):
            f("line", c, 16)
    def lattice_cut(cv):
        f = drawer(cv)
        for c in (Lc, Rc):
            f("line", c, 8)
    def lattice_vine(cv):
        f = drawer(cv)
        for c in (Lc, Rc):
            f("line", c, 2.2)
            for k in range(6, len(c) - 6, 12):
                x, y = c[k]
                a = math.atan2(c[k + 1][1] - c[k - 1][1], c[k + 1][0] - c[k - 1][0])
                for sg in (-1, 1):
                    f("fill", petal_pts(x, y, 9, 3.4, a + sg * 0.9, n=8))
    lat = np.clip(tile_mask(S, S, lattice) - tile_mask(S, S, lattice_cut), 0, 1)
    vine = tile_mask(S, S, lattice_vine)
    # medallions in cells at (S/2, 3S/4) and (0, S/4); crowns at the nodes (S/2, S/4) and (0, 3S/4)
    def med(cv):
        f = drawer(cv)
        for (mx, my) in [(S / 2, 3 * S / 4), (0, S / 4)]:
            pomegranate(f, mx, my, S * 0.14)
            for sg in (-1, 1):
                f("fill", saz(mx + sg * S * 0.05, my + S * 0.18, S * 0.22, -math.pi / 2 + sg * 1.25, curl=-0.3 * sg))
        for (mx, my) in [(S / 2, S / 4), (0, 3 * S / 4)]:
            for k, a in enumerate([-math.pi / 2, -math.pi / 2 - 0.55, -math.pi / 2 + 0.55]):
                f("fill", petal_pts(mx, my + 6, 44 if k == 0 else 34, 13, a, n=12))
            f("dot", (mx, my + 6, 7))
            for a in (math.pi / 2 - 0.5, math.pi / 2 + 0.5):
                f("fill", petal_pts(mx, my + 6, 22, 7, a, n=10))
    medm = tile_mask(S, S, med)
    # inner details cut back to crimson (so the gold reads as woven shapes with drawing inside)
    def med_cut(cv):
        f = drawer(cv)
        for (mx, my) in [(S / 2, 3 * S / 4), (0, S / 4)]:
            f("ring", ellipse_pts(mx, my, S * 0.105, S * 0.11, 28), 3)
            for d in seeds_pattern(mx, my, S * 0.14, 10):
                f("dot", d)
    medcut = tile_mask(S, S, med_cut)
    gold = np.clip(np.maximum.reduce([lat, vine, medm]) - medcut * medm, 0, 1)
    # cream silk inlay inside pomegranate seeds (two-colour lampas effect)
    def seeds(cv):
        f = drawer(cv)
        for (mx, my) in [(S / 2, 3 * S / 4), (0, S / 4)]:
            for (x, y, r) in seeds_pattern(mx, my, S * 0.14, 10):
                f("dot", (x, y, r * 0.75))
    sd = tile_mask(S, S, seeds)
    art = over(ground, lame(gold, GOLD, seed=nx(), pitch=2.6, bind=8, deep=GOLD_D))
    art = over(art, satin(sd, CREAM, "#ffffff", angle=0.0, spacing=1.6, seed=nx(), stitch=4, raise_=0, fuzz=0))
    # self-coloured damask cintamani scattered on the ground (crimson on crimson, subtle)
    def cint(cv):
        f = drawer(cv)
        for (mx, my) in [(S * 0.25, S * 0.5), (S * 0.75, S * 0.0), (S * 0.75, S * 1.0)]:
            for (dx, dy) in [(-7, 4), (7, 4), (0, -8)]:
                f("dot", (mx + dx, my + dy, 4.6))
    cm = tile_mask(S, S, cint)
    art[..., :3] *= (1 + cm * 0.22)[..., None]
    preview(art, "ko-brocade")
    save_full(art, f"{OUT}/brocade.webp", size=(260, 260), quality=80)
    clear()

if "medallion" in PARTS:
    # big ogival cartouche with a pomegranate, saz leaves and tulip crown (gold lame + cream silk), transparent
    W, H = 560, 760
    nx = Seq(60200)
    cx, cy = W / 2, H / 2 + 20
    ys = np.linspace(-1, 1, 120)
    def og(rx, ry, cx=cx, cy=cy):
        pts = []
        for t in np.linspace(0, math.tau, 160, endpoint=False):
            x = math.sin(t); y = -math.cos(t)
            # ogee: pointed top/bottom with S-shaped flanks
            px = cx + rx * x * (1 - 0.35 * abs(y) ** 3) * (1 + 0.12 * math.sin(abs(y) * math.pi))
            py = cy + ry * y * (1 + 0.06 * (1 - abs(x)))
            pts.append((px, py))
        return pts
    outer = og(250, 350); mid_ = og(232, 330); inner = og(214, 310)
    def frame(cv):
        f = drawer(cv)
        f("fill", outer)
    def frame_cut(cv):
        f = drawer(cv)
        f("fill", mid_)
    ring = np.clip(mask_from(W, H, frame) - mask_from(W, H, frame_cut), 0, 1)
    def inner_ring(cv):
        f = drawer(cv); f("ring", inner, 3.0)
    def motif(cv):
        f = drawer(cv)
        pomegranate(f, cx, cy + 20, 104)
        f("line", [(cx, cy - 90), (cx, cy - 150), (cx, cy - 196)], 7)
        f("line", [(cx, cy + 110), (cx, cy + 200), (cx, cy + 232)], 7)
        for sg in (-1, 1):
            f("fill", saz(cx + sg * 30, cy + 160, 196, -math.pi / 2 + sg * 1.2, curl=-0.25 * sg))
            # side tulips on curved stems
            st = [(cx, cy - 150), (cx + sg * 50, cy - 160), (cx + sg * 86, cy - 180), (cx + sg * 96, cy - 200)]
            f("line", st, 5)
            for k, a in enumerate([-math.pi / 2, -math.pi / 2 - 0.45, -math.pi / 2 + 0.45]):
                f("fill", petal_pts(cx + sg * 96, cy - 196, 40 if k == 0 else 30, 13, a + sg * 0.25, n=12))
            f("fill", saz(cx, cy - 120, 92, -math.pi / 2 - sg * 0.9, curl=0.3 * sg))
        for k, a in enumerate([-math.pi / 2, -math.pi / 2 - 0.5, -math.pi / 2 + 0.5]):
            f("fill", petal_pts(cx, cy - 190, 72 if k == 0 else 56, 22, a, n=12))
        for k in range(5):
            f("fill", petal_pts(cx, cy + 232, 46, 12, math.pi / 2 + (k - 2) * 0.35, n=10))
    mm = mask_from(W, H, motif)
    def cut(cv):
        f = drawer(cv)
        f("ring", ellipse_pts(cx, cy + 20, 84, 88, 40), 4)
        for d in seeds_pattern(cx, cy + 20, 104, 17):
            f("dot", d)
        for sg in (-1, 1):
            f("line", [(cx + sg * 34, cy + 156), (cx + sg * 110, cy + 110), (cx + sg * 176, cy + 70)], 2.5)
            f("line", [(cx + sg * 6, cy - 200), (cx + sg * 14, cy - 238)], 2.5)
            f("line", [(cx + sg * 94, cy - 196), (cx + sg * 102, cy - 222)], 2.0)
    cm = mask_from(W, H, cut) * mm
    gold = np.clip(np.maximum.reduce([ring, mask_from(W, H, inner_ring), mm]) - cm, 0, 1)
    # cartouche field: deep crimson silk inside the ring (so it reads on any ground)
    field = mask_from(W, H, lambda cv: drawer(cv)("fill", mid_))
    sk = silk(W, H, "#7a0f1a", CRIM_D, seed=nx(), pitch=2.0, drape=0.6, bands=1)
    art = rgba(sk[..., :3], field)
    def seeds(cv):
        f = drawer(cv)
        for (x, y, r) in seeds_pattern(cx, cy + 20, 104, 17):
            f("dot", (x, y, r * 0.7))
    sd = mask_from(W, H, seeds)
    art = over(art, lame(gold, GOLD, seed=nx(), pitch=2.8, bind=9, deep=GOLD_D, tile=False))
    art = over(art, satin(sd, CREAM, "#ffffff", angle=0.0, spacing=1.8, seed=nx(), stitch=5, raise_=0.3, fuzz=0))
    # three cintamani dots in cream silk at each side
    for sg in (-1, 1):
        for (dx, dy) in [(-12, 8), (12, 8), (0, -12)]:
            m = circles(W, H, [(cx + sg * 150 + dx, cy + 40 + dy, 10)])
            art = SAT(art, m, CREAM, "#ffffff", radial=(cx + sg * 150 + dx, cy + 40 + dy), spacing=1.6, seed=nx(), stitch=4)
    art = drop_shadow(art, blur=6, dy=5, strength=0.45)
    preview(art, "ko-medallion", bg=CRIM)
    save(art, f"{OUT}/medallion.webp", max_w=340, quality=84)
    clear()

if "cintamani" in PARTS:
    # woven band (repeat-x): cream silk band with crimson cintamani dots edged in gold and gold wavy stripes
    W, H = 360, 90
    nx = Seq(60300)
    art = silk(W, H, CREAM, "#e8d6ae", seed=nx(), pitch=2.0, drape=0.3, bands=1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    def dots(cv):
        f = drawer(cv)
        for k in range(4):
            x = k * 90 + 45
            for (dx, dy) in [(-11, 6), (11, 6), (0, -12)]:
                f("dot", (x + dx, 44 + dy, 9))
    def rings(cv):
        f = drawer(cv)
        for k in range(4):
            x = k * 90 + 45
            for (dx, dy) in [(-11, 6), (11, 6), (0, -12)]:
                f("ring", ellipse_pts(x + dx, 44 + dy, 10.5, 10.5, 24), 2.2)
    def waves(cv):
        f = drawer(cv)
        for k in range(4):
            x0 = k * 90
            for j in (0, 1):
                f("line", [(x0 + 4 + t * 18, 66 + j * 9 + 3 * math.sin(t * 2.2)) for t in np.linspace(0, 1, 12)] if False else
                  [(x0 + 70 + u * 18, 60 + j * 10 + 4 * math.sin(u * 7)) for u in np.linspace(0, 1, 14)], 2.6)
                f("line", [(x0 + 70 + u * 18, 20 + j * 10 + 4 * math.sin(u * 7)) for u in np.linspace(0, 1, 14)], 2.6)
    dm = tile_mask(W, H, dots); rm = tile_mask(W, H, rings); wm = tile_mask(W, H, waves)
    edge = ((yy < 6) | (yy > H - 7)).astype(np.float32)
    art = over(art, satin(dm, CRIM, CRIM_L, radial=None, angle=0.6, spacing=1.6, seed=nx(), stitch=6, raise_=0.4, fuzz=0))
    art = over(art, lame(np.clip(rm + wm + edge, 0, 1), GOLD, seed=nx(), pitch=2.0, bind=6, deep=GOLD_D))
    preview(art, "ko-cint")
    save_full(art, f"{OUT}/cintamani.webp", size=(180, 45), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 560, 100
    nx = Seq(60400)
    cx = W / 2
    def d(cv):
        f = drawer(cv)
        for (dx, dy) in [(-13, 8), (13, 8), (0, -14)]:
            f("dot", (cx + dx, 50 + dy, 10))
        for sg in (-1, 1):
            for j in (0, 1):
                f("line", [(cx + sg * (40 + u * 200), 44 + j * 12 + 5 * math.sin(u * 16) * (1 - u)) for u in np.linspace(0, 1, 60)], 3.0 - j * 0.6)
            f("fill", petal_pts(cx + sg * 250, 50, 22, 8, 0 if sg > 0 else math.pi, n=10))
    m = mask_from(W, H, d)
    art = lame(m, GOLD, seed=nx(), pitch=2.0, bind=6, deep=GOLD_D, tile=False)
    for (dx, dy) in [(-13, 8), (13, 8), (0, -14)]:
        art = SAT(art, circles(W, H, [(cx + dx, 50 + dy, 6.5)]), CRIM, CRIM_L, radial=(cx + dx, 50 + dy), spacing=1.4, seed=nx(), stitch=4)
    preview(art, "ko-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)
