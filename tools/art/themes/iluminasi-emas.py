"""Iluminasi Emas — gold-and-lapis illumination in the manner of classical manuscript frames, used as decorative frames
only (no script is drawn; every word is typeset by the page): an unwan headpiece with an ogee crest, blue finials and an
empty vellum cartouche; a sarlawh band whose cartouche holds each section title; a shamsa sunburst medallion; a
marginal palmette medallion; a vertical gold-scroll margin strip. Gold leaf (foil, worn), lapis (granulated
gouache), small vermilion and white flowers. Floral scrolls and geometry only, no figures.
Run: python3 -I iluminasi-emas.py [part ...]   parts: unwan sarlawh shamsa marginal pinggir
Assets -> public/themes/art/iluminasi-emas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q1_lib import *  # noqa

OUT = outdir("iluminasi-emas")
PARTS = sys.argv[1:] or ["unwan", "sarlawh", "shamsa", "marginal", "pinggir"]
LAPIS, LAPIS_D, LAPIS_L = "#1f3d8f", "#132a66", "#3a5cb8"
GOLD = "#c9a24a"
VELLUM = "#f5ecd6"
VERM = "#c23b22"
WHITE = "#f8f3e6"
GREEN = "#3f7a5a"
INK = "#3a2a14"


def lapis(art, m, seed):
    return G(art, m, LAPIS, LAPIS_D, seed=seed, density=0.97, edge=0.25, bloom=0.08, gran=0.55, rough=1.2, feather=0.6, mottle=0.35)


def gold(art, m, seed, wear=0.12):
    h, w = m.shape
    worn = fbm(w, h, seed + 9, 7, 2)
    mm = m * (1 - wear * np.clip((worn - 0.62) * 5, 0, 1))
    return FO(art, mm, GOLD, seed=seed, emboss=0.75, sparkle=0.1, pad=6)


def inkline(art, m, seed, col=INK, a=0.85):
    return OV(art, m, lambda mm: tint(mm, col, a), pad=4)


def scroll_band(W, H, x0, x1, yc, amp, period, seed, width=2.6, leaf=7.0, flip=False):
    """Islimi vine: a sine stem with alternating spiral offshoots ending in split-palmette leaves.
    Returns (stem_mask, leaf_mask, flower_centres)."""
    rng = random.Random(seed)
    xs = np.linspace(x0, x1, 120)
    stem = [(x, yc + amp * math.sin((x - x0) / period * math.tau)) for x in xs]
    items = [(stem, width, (0.02, 0.02))]
    leaves, flowers = [], []
    k = 0
    x = x0 + period * 0.25
    while x < x1 - period * 0.2:
        s = 1 if k % 2 == 0 else -1
        y = yc + amp * math.sin((x - x0) / period * math.tau)
        r0 = amp * 0.95
        cx_, cy_ = x + period * 0.12, y + s * r0 * 0.9
        sp = spiral_scroll(cx_, cy_, r0 * 0.9, math.atan2(y - cy_, x - cx_), 0.85, d=-s, n=26, shrink=0.7)
        items.append((sp, width * 0.8, (0.0, 0.5)))
        ex, ey = sp[-1]
        # split palmette at the spiral end
        a = math.atan2(sp[-1][1] - sp[-3][1], sp[-1][0] - sp[-3][0])
        leaves.append(petal_pts(ex, ey, leaf * 1.6, leaf * 0.6, a + 0.5, n=12))
        leaves.append(petal_pts(ex, ey, leaf * 1.6, leaf * 0.6, a - 0.5, n=12))
        # small leaf on the stem
        la = math.atan2(math.cos((x - x0) / period * math.tau), 1) - s * 1.2
        leaves.append(petal_pts(x, y, leaf * 1.3, leaf * 0.45, la, n=12))
        flowers.append((cx_, cy_ - s * 0, r0 * 0.28))
        x += period / 2
        k += 1
    return strokes(W, H, items), shapes(W, H, leaves), flowers


def blossoms(art, W, H, pts, seed, cols=(VERM, WHITE)):
    """Tiny five-dot blossoms (painted, not gold)."""
    nx = Seq(seed)
    for i, col in enumerate(cols):
        sel = pts[i::len(cols)]
        if not sel:
            continue
        dots = []
        for x, y, r in sel:
            for j in range(5):
                a = j / 5 * math.tau + 0.3
                dots.append((x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.7, r * 0.55))
        art = GP(art, circles(W, H, dots), col, seed=nx(), rough=0.5)
        art = GP(art, circles(W, H, [(x, y, r * 0.38) for x, y, r in sel]), "#e8c34f", seed=nx(), rough=0.3)
    return art


def cartouche(cx, cy, hw, hh, tip, n=6):
    """Lobed cartouche: a rectangle with pointed, cusped ends."""
    pts = []
    for sgn in (-1, 1):
        ex = cx + sgn * hw
        side = []
        for i in range(n + 1):
            t = i / n
            yy = cy - hh + 2 * hh * t
            bulge = tip * (1 - abs(2 * t - 1)) ** 0.8 + tip * 0.18 * math.sin(t * math.pi * 3) ** 2
            side.append((ex + sgn * bulge, yy))
        if sgn == 1:
            pts += side
        else:
            pts += side[::-1]
    return pts


def rim_of(m, px):
    d = (gaussian_filter(m, px * 0.5) > 0.12).astype(np.float32)
    return np.clip(gaussian_filter(d, 0.6) - m, 0, 1)


def stipple(W, H, mask, seed, step=9, r=1.3):
    rng = random.Random(seed)
    pts = [(x + rng.uniform(-1.5, 1.5), y + rng.uniform(-1.5, 1.5), r) for y in np.arange(4, H, step) for x in np.arange(4 + (y // step % 2) * step / 2, W, step)]
    return circles(W, H, pts) * mask


def band_frame(art, W, H, x0, y0, x1, y1, seed, inner_lines=True):
    """Gold rulings around a rectangle: outer gold, thin vermilion and blue lines (jadwal)."""
    nx = Seq(seed)
    def rr(a, b, c, d):
        return rect(W, H, a, b, c, d)
    outer = np.clip(rr(x0, y0, x1, y1) - rr(x0 + 6, y0 + 6, x1 - 6, y1 - 6), 0, 1)
    art = gold(art, outer, nx())
    if inner_lines:
        l1 = np.clip(rr(x0 + 9, y0 + 9, x1 - 9, y1 - 9) - rr(x0 + 11, y0 + 11, x1 - 11, y1 - 11), 0, 1)
        art = inkline(art, l1, nx(), VERM, 0.9)
    return art


def part_sarlawh():
    W, H = 700, 176
    nx = Seq(100)
    art = blank(W, H)
    x0, y0, x1, y1 = 8, 12, W - 8, H - 12
    field = rect(W, H, x0 + 12, y0 + 12, x1 - 12, y1 - 12)
    art = lapis(art, field, nx())
    cpts = cartouche(W / 2, H / 2, 196, 46, 34)
    cm = poly(W, H, cpts, smooth=True)
        # gold scrolls on the lapis, left and right of the cartouche
    st, lv, fl = scroll_band(W, H, x0 + 14, x1 - 14, H / 2, 22, 120, 7, width=3.0, leaf=7)
    mask_out = field * (1 - np.clip(gaussian_filter(cm, 6) * 3, 0, 1))
    art = gold(art, np.maximum(st, lv) * mask_out, nx(), wear=0.1)
    fl = [(x, y, r) for x, y, r in fl if mask_out[int(min(H - 1, max(0, y))), int(min(W - 1, max(0, x)))] > 0.5]
    art = blossoms(art, W, H, [(x, y, 6) for x, y, r in fl], 300)
    # cartouche: gold rim, thin blue line, vellum inside
    art = gold(art, stipple(W, H, mask_out * (1 - np.clip(gaussian_filter(np.maximum(st, lv), 3) * 4, 0, 1)), 55), nx(), wear=0)
    rim = rim_of(cm, 12)
    art = gold(art, rim, nx(), wear=0.05)
    art = OV(art, cm, lambda m: flat(m, VELLUM))
    art = GP(art, cm, VELLUM, "#efe2c4", seed=nx(), rough=0.3, streak=0.3, density=0.6)
    art = inkline(art, rim_of(cm, 3), nx(), LAPIS_D, 0.85)
    art = band_frame(art, W, H, x0, y0, x1, y1, nx())
    # small blue finials (fleurons) along the top and bottom edge
    fins = []
    for x in np.linspace(x0 + 30, x1 - 30, 13):
        fins.append([(x - 6, y0), (x, y0 - 11), (x + 6, y0)])
        fins.append([(x - 6, y1), (x, y1 + 11), (x + 6, y1)])
    art = GP(art, shapes(W, H, fins), LAPIS_L, seed=nx(), rough=0.6)
    art = add_grain(art, seed=3, amount=0.025)
    preview(art, "ie-sarlawh", tone=VELLUM)
    save(art, f"{OUT}/sarlawh.webp", max_w=700, quality=82)
    clear()


def part_unwan():
    W, H = 760, 400
    nx = Seq(400); rng = random.Random(4)
    art = blank(W, H)
    # ogee crest above a rectangular band
    bx0, by0, bx1, by1 = 16, 190, W - 16, 390
    cx = W / 2
    crest = [(cx - 230, by0 + 2), (cx - 180, by0 - 40), (cx - 120, by0 - 80), (cx - 50, by0 - 110), (cx - 14, by0 - 150), (cx, by0 - 172),
             (cx + 14, by0 - 150), (cx + 50, by0 - 110), (cx + 120, by0 - 80), (cx + 180, by0 - 40), (cx + 230, by0 + 2)]
    cm = poly(W, H, crest, smooth=True)
    band = rect(W, H, bx0 + 12, by0 + 12, bx1 - 12, by1 - 12)
    # blue finial rays above the crest
    rays = []
    for i in range(23):
        t = i / 22
        p = crest[0][0] + (crest[-1][0] - crest[0][0]) * t
        # find crest y at p (approx along polyline)
        k = min(len(crest) - 2, int(t * (len(crest) - 1)))
        u = t * (len(crest) - 1) - k
        ax, ay = crest[k]; bx_, by_ = crest[k + 1]
        x, y = ax + (bx_ - ax) * u, ay + (by_ - ay) * u
        nxv, nyv = (x - cx), (y - (by0 + 40))
        L = math.hypot(nxv, nyv) or 1
        nxv, nyv = nxv / L, nyv / L
        Lr = 30 if i % 2 == 0 else 18
        rays.append(petal_pts(x - nxv * 2, y - nyv * 2, Lr, 7 if i % 2 == 0 else 5, math.atan2(nyv, nxv), n=14))
    art = GP(art, shapes(W, H, rays), LAPIS_L, LAPIS, seed=nx(), rough=0.8)
    # crest: lapis field with gold scrolls, gold rim
    cm_in = np.clip((gaussian_filter(cm, 1) - 0.5) * 3, 0, 1) * (1 - np.clip(gaussian_filter(1 - cm, 5) * 3, 0, 1))
    art = gold(art, cm, nx())
    art = lapis(art, cm_in, nx())
    sp = []
    for d in (-1, 1):
        sp.append((spiral_scroll(cx + d * 70, by0 - 40, 46, math.pi / 2 + d * 0.9, 1.2, d=d, n=40, shrink=0.75), 3.0, (0.0, 0.5)))
        sp.append((spiral_scroll(cx + d * 150, by0 - 18, 26, math.pi / 2, 1.0, d=-d, n=30, shrink=0.75), 2.6, (0.0, 0.5)))
        sp.append((curve([(cx, by0 - 6), (cx + d * 40, by0 - 30), (cx + d * 70, by0 - 40)], 20), 3.0, (0.0, 0.0)))
    lvs = []
    for d in (-1, 1):
        for x, y, a in ((cx + d * 108, by0 - 70, -1.2), (cx + d * 186, by0 - 32, -0.6), (cx + d * 30, by0 - 76, -1.4)):
            lvs.append(petal_pts(x, y, 15, 5, a if d > 0 else math.pi - a, n=12))
    # central palmette
    palm = [petal_pts(cx, by0 - 50, 70, 22, -math.pi / 2, n=16)]
    pm = shapes(W, H, palm)
    art = gold(art, (np.maximum(strokes(W, H, sp), shapes(W, H, lvs))) * cm_in, nx())
    art = gold(art, stipple(W, H, cm_in * (1 - np.clip(gaussian_filter(np.maximum(strokes(W, H, sp), shapes(W, H, lvs)), 3) * 4, 0, 1)), 66, step=10), nx(), wear=0)
    art = gold(art, pm, nx())
    art = GP(art, shapes(W, H, [petal_pts(cx, by0 - 58, 46, 12, -math.pi / 2, n=16)]), VERM, seed=nx(), rough=0.5)
    art = GP(art, shapes(W, H, [petal_pts(cx, by0 - 64, 26, 6, -math.pi / 2, n=14)]), WHITE, seed=nx(), rough=0.4)
    art = blossoms(art, W, H, [(cx - 110, by0 - 40, 6), (cx + 110, by0 - 40, 6), (cx - 40, by0 - 112, 5), (cx + 40, by0 - 112, 5), (cx - 190, by0 - 12, 5), (cx + 190, by0 - 12, 5)], 600)
    clear()
    # rectangular band with a large empty cartouche (the page sets text inside)
    art = lapis(art, band, nx())
    cpts = cartouche(cx, (by0 + by1) / 2, 236, 68, 46, n=8)
    cart = poly(W, H, cpts, smooth=True)
    mask_out = band * (1 - np.clip(gaussian_filter(cart, 7) * 3, 0, 1))
    for yc, ph in (((by0 + by1) / 2 - 42, 0), ((by0 + by1) / 2 + 42, 1)):
        st, lv, fl = scroll_band(W, H, bx0 + 14, bx1 - 14, yc, 18, 96, 30 + ph, width=2.6, leaf=6)
        art = gold(art, np.maximum(st, lv) * mask_out, nx(), wear=0.1)
        fl = [(x, y, r) for x, y, r in fl if mask_out[int(min(H - 1, max(0, y))), int(min(W - 1, max(0, x)))] > 0.5]
        art = blossoms(art, W, H, [(x, y, 5) for x, y, r in fl], 700 + ph * 10)
    art = gold(art, stipple(W, H, mask_out, 77), nx(), wear=0)
    art = gold(art, rim_of(cart, 14), nx(), wear=0.05)
    art = OV(art, cart, lambda m: flat(m, VELLUM))
    art = GP(art, cart, VELLUM, "#efe2c4", seed=nx(), rough=0.3, streak=0.3, density=0.6)
    art = inkline(art, rim_of(cart, 3), nx(), LAPIS_D, 0.85)
    art = band_frame(art, W, H, bx0, by0, bx1, by1, nx())
    # corner medallions on the band
    for x in (bx0 + 34, bx1 - 34):
        m = circles(W, H, [(x, (by0 + by1) / 2, 20)])
        art = gold(art, m, nx())
        art = GP(art, circles(W, H, [(x, (by0 + by1) / 2, 12)]), VERM, seed=nx(), rough=0.4)
        art = GP(art, circles(W, H, [(x, (by0 + by1) / 2, 5)]), WHITE, seed=nx(), rough=0.3)
    art = add_grain(art, seed=5, amount=0.025)
    preview(art, "ie-unwan", tone=VELLUM)
    save(art, f"{OUT}/unwan.webp", max_w=760, quality=80)
    clear()


def part_shamsa():
    W = H = 360
    nx = Seq(900)
    art = blank(W, H)
    c = W / 2
    # sunburst rays (alternating gold and blue)
    rays_g, rays_b = [], []
    for i in range(32):
        a = i / 32 * math.tau
        L = 170 if i % 2 == 0 else 150
        base = 108
        p = [(c + math.cos(a - 0.05) * base, c + math.sin(a - 0.05) * base), (c + math.cos(a) * L, c + math.sin(a) * L), (c + math.cos(a + 0.05) * base, c + math.sin(a + 0.05) * base)]
        (rays_g if i % 2 == 0 else rays_b).append(p)
    art = GP(art, shapes(W, H, rays_b, smooth=False), LAPIS_L, seed=nx(), rough=0.7)
    art = gold(art, shapes(W, H, rays_g, smooth=False), nx())
    # scalloped disc
    sc = []
    for i in range(16):
        a = i / 16 * math.tau
        sc.append((c + math.cos(a) * 104, c + math.sin(a) * 104, 16))
    disc = np.maximum(circles(W, H, [(c, c, 106)]), circles(W, H, sc))
    art = gold(art, disc, nx())
    inner = circles(W, H, [(c, c, 92)])
    art = lapis(art, inner, nx())
    # eight-lobed rosette of scrolls inside
    items, lvs = [], []
    for i in range(8):
        a = i / 8 * math.tau
        sp = spiral_scroll(c + math.cos(a) * 52, c + math.sin(a) * 52, 26, a + math.pi, 0.8, d=1, n=26, shrink=0.7)
        items.append((sp, 3.2, (0.0, 0.5)))
        lvs.append(petal_pts(c + math.cos(a) * 30, c + math.sin(a) * 30, 30, 9, a, n=14))
    art = gold(art, np.maximum(strokes(W, H, items), shapes(W, H, lvs)) * inner, nx())
    art = blossoms(art, W, H, [(c + math.cos(i / 8 * math.tau + 0.39) * 66, c + math.sin(i / 8 * math.tau + 0.39) * 66, 6) for i in range(8)], 950)
    hub = circles(W, H, [(c, c, 22)])
    art = gold(art, hub, nx())
    art = GP(art, circles(W, H, [(c, c, 14)]), VERM, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(c, c, 6)]), WHITE, seed=nx(), rough=0.3)
    art = add_grain(art, seed=6, amount=0.025)
    preview(art, "ie-shamsa", tone=VELLUM)
    save(art, f"{OUT}/shamsa.webp", max_w=240, quality=82)
    clear()


def part_marginal():
    """Marginal palmette medallion (vertical, tear-drop with a finial) for the margins and portraits."""
    W, H = 180, 330
    nx = Seq(1200)
    art = blank(W, H)
    c = W / 2
    outer = [(c, 18)] + [(c + 66 * math.sin(t) * (1 - 0.35 * math.cos(t)), 150 - 110 * math.cos(t) * 0.9 + 60 * (1 - math.cos(t)) * 0.9) for t in np.linspace(0.25, math.pi - 0.05, 16)]
    outer = outer + [(2 * c - x, y) for x, y in outer[::-1][:-1]]
    om = poly(W, H, outer, smooth=True)
    stem = strokes(W, H, [([(c, 300), (c, 320)], 6, (0, 0))])
    art = gold(art, np.maximum(om, stem), nx())
    inner = np.clip((gaussian_filter(om, 1) - 0.5) * 3, 0, 1) * (1 - np.clip(gaussian_filter(1 - om, 7) * 3, 0, 1))
    art = lapis(art, inner, nx())
    sp = [(spiral_scroll(c + d * 22, 150, 24, math.pi / 2 - d * 0.4, 1.0, d=d, n=26, shrink=0.72), 2.8, (0.0, 0.5)) for d in (-1, 1)]
    sp += [(curve([(c, 270), (c - 4, 210), (c, 150), (c + 2, 90)], 30), 3, (0.02, 0.2))]
    lvs = [petal_pts(c, 92, 40, 12, -math.pi / 2, n=14)] + [petal_pts(c, 230 - k * 30, 22, 7, -math.pi / 2 + d * 1.0, n=12) for k in range(3) for d in (-1, 1)]
    art = gold(art, np.maximum(strokes(W, H, sp), shapes(W, H, lvs)) * inner, nx())
    art = GP(art, shapes(W, H, [petal_pts(c, 86, 24, 6, -math.pi / 2, n=12)]), VERM, seed=nx(), rough=0.4)
    art = blossoms(art, W, H, [(c - 30, 186, 5), (c + 30, 186, 5), (c, 250, 5)], 1250)
    # tiny blue finial on the tip
    art = GP(art, shapes(W, H, [[(c - 6, 22), (c, 2), (c + 6, 22)]], smooth=False), LAPIS_L, seed=nx(), rough=0.5)
    art = add_grain(art, seed=7, amount=0.025)
    preview(art, "ie-marginal", tone=VELLUM)
    save(art, f"{OUT}/marginal.webp", max_w=90, quality=84)
    clear()


def part_pinggir():
    """Vertical margin strip (repeat-y): thin lapis channel with a gold vine between gold and vermilion rulings."""
    W, H = 44, 240
    nx = Seq(1400)
    art = blank(W, H)
    art = lapis(art, rect(W, H, 8, -10, W - 8, H + 10), nx())
    # vine: vertical sine (period == H for seamless tiling)
    pts = [(W / 2 + 7 * math.sin(y / H * math.tau * 2), y) for y in np.linspace(-20, H + 20, 80)]
    leaves = []
    for k in range(4):
        y = k * H / 4 + H / 8
        x = W / 2 + 7 * math.sin(y / H * math.tau * 2)
        s = 1 if k % 2 == 0 else -1
        leaves.append(petal_pts(x, y, 11, 4, (0 if s > 0 else math.pi) - 0.6, n=12))
    art = gold(art, np.maximum(strokes(W, H, [(pts, 2.2, None)]), shapes(W, H, leaves)) * rect(W, H, 9, -10, W - 9, H + 10), nx(), wear=0.08)
    dots = [(W / 2 - 7 * math.sin((k * H / 4) / H * math.tau * 2) * 0.2, k * H / 4, 3.2) for k in range(5)]
    art = GP(art, circles(W, H, dots), VERM, seed=nx(), rough=0.3)
    art = gold(art, rect(W, H, 4, -10, 8, H + 10), nx(), wear=0.05)
    art = gold(art, rect(W, H, W - 8, -10, W - 4, H + 10), nx(), wear=0.05)
    art = OV(art, rect(W, H, 1, -10, 2.4, H + 10), lambda m: tint(m, VERM, 0.85))
    art = OV(art, rect(W, H, W - 2.4, -10, W - 1, H + 10), lambda m: tint(m, VERM, 0.85))
    preview(art, "ie-pinggir", tone=VELLUM)
    save_full(art, f"{OUT}/pinggir.webp", quality=84)
    clear()


for p in PARTS:
    globals()[f"part_{p}"]()
kb_report(OUT)
