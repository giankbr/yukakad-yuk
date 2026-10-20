"""Koran — relief-print (linocut/woodcut) pieces for the newspaper theme: a woodcut masthead vignette
(interlocked rings in laurel with a ribbon), an inked thick-thin printing rule, a woodcut city skyline
tailpiece (colonial hall with twin towers, domed church, trees, carved sun), a newsprint paper tile and
a halftone screen tile for the photo treatment.
Run: python3 -I /tmp/pen/art/themes/koran.py [emblem rule city paper halftone]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _r2_lib import *  # noqa

T = "koran"
D = outdir(T)
nxt = Seeds(5100)
rng = random.Random(77)
INK = "#1d1a14"


def carve(W, H, lines, width):
    return ink_mask_lines(W, H, lines, width)


def ink_mask_lines(W, H, lines, width):
    m = np.zeros((H, W), np.float32)
    for pts in lines:
        m = np.maximum(m, stroke_mask(W, H, pts, width, (0.15, 0.15)))
    return m


def leaf_m(W, H, x, y, L, a):
    return shape_mask(W, H, deform(petal_pts(x, y, L, L * 0.38, a, n=12), rng, 1, 0.05))


def emblem():
    W, H = 520, 280
    cx, cy = 260, 118
    m = np.zeros((H, W), np.float32)
    # laurel branches: arcs rising from the base on both sides, separate carved leaves
    for side in (-1, 1):
        R = 92
        stem = [(cx + side * math.cos(a) * R * 1.12, cy - math.sin(a) * R) for a in np.linspace(math.radians(-58), math.radians(62), 34)]
        stem = [(x, y) for x, y in stem]
        m = np.maximum(m, stroke_mask(W, H, stem, 3.4, (0.05, 0.5)))
        for i in range(3, 33, 3):
            x, y = stem[i]; x2, y2 = stem[i - 1]
            ang = math.atan2(y - y2, x - x2)
            L = 26 - i * 0.3
            for sgn in (-1, 1):
                lm = leaf_m(W, H, x, y, L, ang + sgn * 0.62)
                vein = stroke_mask(W, H, [(x + math.cos(ang + sgn * 0.62) * L * t, y + math.sin(ang + sgn * 0.62) * L * t) for t in (0.2, 0.55, 0.85)], 1.6, (0.2, 0.5))
                m = np.maximum(m, np.clip(lm - vein, 0, 1))
    # two interlocked rings (carved highlight on each)
    rings = np.maximum(ring_mask(W, H, cx - 26, cy, 44, 13, rng, 0.4), ring_mask(W, H, cx + 26, cy, 44, 13, rng, 0.4))
    m = np.maximum(m, rings)
    hl = np.maximum(stroke_mask(W, H, arc_pts(cx - 26, cy, 44, 3.6, 4.6, 16), 2.4, (0.3, 0.3)), stroke_mask(W, H, arc_pts(cx + 26, cy, 44, 3.6, 4.6, 16), 2.4, (0.3, 0.3)))
    m = np.clip(m - hl, 0, 1)
    # small diamond-star above
    star = shape_mask(W, H, [(cx, cy - 74), (cx + 8, cy - 62), (cx, cy - 50), (cx - 8, cy - 62)], smooth=False)
    m = np.maximum(m, star)
    # ribbon banner with carved text
    rib = [(cx - 150, 214), (cx - 60, 204), (cx + 60, 204), (cx + 150, 214), (cx + 150, 250), (cx + 60, 240), (cx - 60, 240), (cx - 150, 250)]
    rm = shape_mask(W, H, deform(rib, rng, 1, 0.01))
    for sx in (-1, 1):
        tail = [(cx + sx * 150, 214), (cx + sx * 190, 220), (cx + sx * 172, 236), (cx + sx * 190, 256), (cx + sx * 150, 250)]
        rm = np.maximum(rm, shape_mask(W, H, tail, smooth=False))
    txt = text_mask(W, H, "KABAR GEMBIRA", cx, 236, 30, "bebas", 3)
    m = np.maximum(m, np.clip(rm - txt, 0, 1))
    art = linocut(m, INK, seed=nxt(), wear=0.18, rough=1.4)
    preview(art, f"{PREV}/ko-emblem.png", "#f3eddf")
    save(art, f"{D}/emblem.webp", max_w=300, q=82)


def rule():
    W, H = 1200, 22
    m = np.zeros((H, W), np.float32)
    m = np.maximum(m, rrect_mask(W, H, 0, 3, W, 7, 0))
    m = np.maximum(m, rrect_mask(W, H, 0, 14, W, 2.2, 0))
    art = linocut(m, INK, seed=nxt(), wear=0.5, rough=1.2)
    save(art, f"{D}/rule.webp", q=80, trim=False)


def city():
    W, H = 780, 300
    m = np.zeros((H, W), np.float32)
    G = 262
    # carved sun with rays
    SX, SY = 270, 60
    sun = dots_mask(W, H, [(SX, SY, 26)])
    rays = np.zeros((H, W), np.float32)
    for k in range(14):
        a = math.pi + k * math.pi / 13
        rays = np.maximum(rays, stroke_mask(W, H, [(SX + math.cos(a) * 34, SY + math.sin(a) * 34), (SX + math.cos(a) * 58, SY + math.sin(a) * 58)], 6.5, (0.05, 0.4)))
    m = np.maximum(m, np.clip(sun - ink_mask_lines(W, H, [[(SX - 30, SY + d), (SX + 30, SY + d)] for d in (-12, -4, 4, 12)], 3.2), 0, 1))
    m = np.maximum(m, rays)
    # sky gouge lines
    for x0, y, L in [(30, 52, 120), (60, 70, 70), (440, 40, 150), (520, 60, 90), (640, 120, 110), (40, 140, 50), (600, 150, 60)]:
        m = np.maximum(m, stroke_mask(W, H, [(x0, y), (x0 + L, y + rng.uniform(-1, 1))], 3.4, (0.25, 0.35)))
    # colonial hall with twin towers (left-centre)
    hall = rrect_mask(W, H, 120, 170, 300, G - 170, 0)
    towers = np.maximum(rrect_mask(W, H, 110, 112, 54, G - 112, 0), rrect_mask(W, H, 376, 112, 54, G - 112, 0))
    roofs = np.maximum(shape_mask(W, H, [(104, 114), (137, 70), (170, 114)], smooth=False), shape_mask(W, H, [(370, 114), (403, 70), (436, 114)], smooth=False))
    pedi = shape_mask(W, H, [(200, 172), (270, 132), (340, 172)], smooth=False)
    bld = np.clip(hall + towers + roofs + pedi, 0, 1)
    # carved windows (arched) and floor lines
    win = np.zeros((H, W), np.float32)
    for x in range(140, 400, 30):
        if 160 < x < 380:
            for y in (186, 222):
                win = np.maximum(win, rrect_mask(W, H, x, y, 14, 24, 7))
    for x in (124, 148, 390, 414):
        for y in (128, 168, 208):
            win = np.maximum(win, rrect_mask(W, H, x, y, 10, 22, 5))
    win = np.maximum(win, ink_mask_lines(W, H, [[(120, 178), (420, 178)], [(120, 214), (420, 214)], [(214, 166), (326, 166)]], 2.0))
    win = np.maximum(win, rrect_mask(W, H, 254, 226, 32, 36, 16))
    m = np.maximum(m, np.clip(bld - win, 0, 1))
    # domed church on the right
    base = rrect_mask(W, H, 500, 190, 150, G - 190, 0)
    dome = shape_mask(W, H, arc_pts(575, 192, 58, math.pi, math.tau, 30) + [(633, 192), (517, 192)])
    lantern = np.maximum(rrect_mask(W, H, 566, 112, 18, 26, 2), shape_mask(W, H, [(562, 114), (575, 96), (588, 114)], smooth=False))
    ch = np.clip(base + dome + lantern, 0, 1)
    cwin = np.zeros((H, W), np.float32)
    for x in (514, 548, 588, 622):
        cwin = np.maximum(cwin, rrect_mask(W, H, x, 206, 12, 26, 6))
    cwin = np.maximum(cwin, ink_mask_lines(W, H, [arc_pts(575, 192, 44, math.pi * 1.1, math.pi * 1.9, 20), arc_pts(575, 192, 28, math.pi * 1.15, math.pi * 1.85, 16)], 2.2))
    m = np.maximum(m, np.clip(ch - cwin, 0, 1))
    # trees: round canopies with carved crescents, trunks
    for tx, r in [(60, 40), (460, 30), (700, 44), (740, 30)]:
        can = shape_mask(W, H, deform(ellipse_pts(tx, G - r * 2.0, r, r * 1.1, 12), rng, 2, 0.08))
        carv = ink_mask_lines(W, H, [arc_pts(tx - r * 0.2, G - r * 2.0, r * k, 3.4, 4.8, 10) for k in (0.4, 0.7)], 2.0)
        m = np.maximum(m, np.clip(can - carv, 0, 1))
        m = np.maximum(m, rrect_mask(W, H, tx - 4, G - r * 1.2, 8, r * 1.2, 1))
    # street + carved cobble marks
    street = rrect_mask(W, H, 0, G, W, 14, 0)
    cob = ink_mask_lines(W, H, [[(x, G + 7), (x + 14, G + 7)] for x in range(10, W, 34)], 2.0)
    m = np.maximum(m, np.clip(street - cob, 0, 1))
    art = linocut(m, INK, seed=nxt(), wear=0.2, rough=1.5)
    preview(art, f"{PREV}/ko-city.png", "#f3eddf")
    save(art, f"{D}/city.webp", max_w=720, q=80)


def paper_tex():
    """Newsprint: soft fibre + fine grain, only a sparse sprinkle of ink specks (seamless)."""
    size = 512
    r = np.random.default_rng(13)
    wn = p2._wrapnoise
    v = 1 + wn(size, r, 30) * 0.012 + wn(size, r, 0.6) * 0.018 + wn(size, r, (0.5, 4)) * 0.01
    speck = gaussian_filter((r.random((size, size)) > 0.99982).astype(np.float32), 0.6, mode="wrap") * 4
    v -= speck * 0.12
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb("#f3eddf"), np.float32)
    save_texture(Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB"), f"{D}/paper.webp", quality=70)
    print("paper", kbsize(f"{D}/paper.webp"))


def halftone():
    t = halftone_tile(48, pitch=4.0, dot=0.5, seed=4)
    save(t, f"{D}/halftone.webp", q=80, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["emblem", "rule", "city", "paper", "halftone"]
    for w in which:
        {"emblem": emblem, "rule": rule, "city": city, "paper": paper_tex, "halftone": halftone}[w]()
