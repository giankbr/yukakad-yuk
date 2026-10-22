"""Khatam Kayu — original design inspired by Persian khatam-kari: carved walnut doors whose panels are inlaid with a
micro-mosaic of tiny triangles of wood, bone and brass forming six-pointed stars, brass rings and studs, ivory
borders. Geometry only, no figures. Run: python3 -I khatam-kayu.py [part ...]
parts: test door band star frame walnut divider   Assets -> public/themes/art/khatam-kayu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d2_lib import *

OUT = outdir("khatam-kayu")
PARTS = sys.argv[1:] or ["door", "band", "star", "frame", "walnut", "divider"]
WAL, WAL_D, WAL_L, BONE, BRASS = "#5c3620", "#2e1b0f", "#74472a", "#efe4cc", "#c9a253"

if "test" in PARTS:
    W, H = 300, 200
    k = khatam(W, H, 10.0, seed=3)
    preview(k, "ktest", bg="#000000")
    Image.open(f"{PREV}/ktest.png").resize((900, 600), Image.NEAREST).save(f"{PREV}/ktest2.png")


def arch_pts(x0, x1, y_spring, rise=None, n=24, f=0.72):
    """Two-centred pointed (Persian) arch from (x0, y_spring) to (x1, y_spring); f = radius / span."""
    span = x1 - x0
    R = f * span
    cx = (x0 + x1) / 2
    ccx = x0 + R  # centre of the left arc
    ay = y_spring - math.sqrt(max(1.0, R * R - (cx - ccx) ** 2))
    a_end = math.atan2(ay - y_spring, cx - ccx)
    left = [(ccx + math.cos(a) * R, y_spring + math.sin(a) * R) for a in np.linspace(math.pi, math.tau + a_end if a_end < 0 else a_end, n)]
    right = [(2 * cx - x, y) for (x, y) in reversed(left[:-1])]
    return left + right


def walnut_paint(mask, seed, col=WAL, col2=WAL_D, angle=1.5708):
    return wood(mask, col, col2, seed=seed, angle=angle, grain=5.0)


def inlay(art, mask, s, seed, ox=0.0, oy=0.0, bevel=True):
    H, W = mask.shape
    k = khatam(W, H, s, ox, oy, seed=seed)
    art = over(art, clip_to(k, np.clip(mask, 0, 1)))
    if bevel:
        # recessed panel: shadow along top/left inner edge, light along bottom/right
        hi, lo = emboss_l(mask, 1.4, 2.0)
        art = over(art, flat(lo * mask, "#1a0e06", 0.6))
        art = over(art, flat(hi * mask, "#f5e3b8", 0.25))
    return art


def bone_line(art, mask, px, seed):
    return GP(art, np.clip(outline(mask, px), 0, 1), BONE, "#e2d4b6", seed=seed, rough=0.3, streak=0.2, pad=6)


if "door" in PARTS:
    W, H = 560, 960
    nx = Seq(500)
    art = blank(W, H)
    cx = W / 2
    SP = 380  # spring line of the arch
    outer = shapes(W, H, [[(16, H - 8)] + arch_pts(16, W - 16, SP, 250) + [(W - 16, H - 8)]], smooth=False)
    art = OV(art, outer, lambda m: walnut_paint(m, nx()))
    hi, lo = emboss_l(outer, 1.0, 3)
    art = over(art, flat(lo, "#140a04", 0.5)); art = over(art, flat(hi, "#c08a5a", 0.3))
    # khatam border band following the arch and jambs
    band_o = shapes(W, H, [[(40, H - 20)] + arch_pts(40, W - 40, SP, 226) + [(W - 40, H - 20)]], smooth=False)
    band_i = shapes(W, H, [[(64, H - 20)] + arch_pts(64, W - 64, SP, 202) + [(W - 64, H - 20)]], smooth=False)
    band = np.clip(band_o - band_i, 0, 1)
    art = inlay(art, band, 4.6, nx(), bevel=False)
    art = bone_line(art, band_o, 2.5, nx()); art = bone_line(art, band_i, 2.5, nx())
    art = FO(art, np.clip(outline(band_o, 1.2), 0, 1) * (1 - outline(band_o, 0.4)), BRASS, seed=nx(), emboss=0.6)
    # the two door leaves inside
    leaves = band_i * rect(W, H, 0, 0, W, H - 20)
    art = OV(art, leaves, lambda m: walnut_paint(m, nx(), WAL_L, WAL))
    seam = rect(W, H, cx - 2.5, 60, cx + 2.5, H - 20)
    art = over(art, flat(seam * leaves, "#140a04", 0.9))
    art = over(art, flat(rect(W, H, cx + 2.5, 60, cx + 6, H - 20) * leaves, "#c08a5a", 0.25))
    for side in (-1, 1):
        lx0, lx1 = (84, cx - 18) if side < 0 else (cx + 18, W - 84)
        # top: half of the pointed arch panel
        top_full = shapes(W, H, [[(84, SP + 40)] + arch_pts(84, W - 84, SP + 40, 190) + [(W - 84, SP + 40)]], smooth=False)
        top = top_full * rect(W, H, lx0, 0, lx1, H)
        art = inlay(art, top, 4.2, nx(), ox=3.0)
        art = bone_line(art, top, 2.2, nx())
        # middle: square panel with a six-pointed star medallion of khatam in a brass outline
        my0, my1 = SP + 70, SP + 70 + (lx1 - lx0)
        mid = rect(W, H, lx0, my0, lx1, my1)
        mcx, mcy, mr = (lx0 + lx1) / 2, (my0 + my1) / 2, (lx1 - lx0) * 0.44
        star = shapes(W, H, [star_pts(mcx, mcy, mr, 8, 0.72, -math.pi / 2)], smooth=False)
        hexa = shapes(W, H, [poly_pts(mcx, mcy, mr * 0.5, 8, math.pi / 8)], smooth=False)
        art = over(art, flat(mid, "#efe4cc", 0.0))
        art = inlay(art, mid * (1 - star), 4.2, nx() + 1)
        art = OV(art, star, lambda m: walnut_paint(m, nx(), WAL_D, "#22140a"))
        art = inlay(art, star * (1 - hexa), 3.4, nx(), bevel=False)
        art = GP(art, hexa, BONE, "#e5d7ba", seed=nx(), rough=0.4)
        art = inlay(art, shapes(W, H, [star_pts(mcx, mcy, mr * 0.4, 8, 0.7, -math.pi / 2)], smooth=False), 3.0, nx(), bevel=False)
        art = FO(art, np.clip(outline(star, 2.2), 0, 1), BRASS, seed=nx(), emboss=0.8)
        art = FO(art, np.clip(outline(hexa, 1.6), 0, 1), BRASS, seed=nx(), emboss=0.8)
        art = bone_line(art, mid, 2.2, nx())
        # bottom: long rectangular khatam panel
        bot = rect(W, H, lx0, my1 + 30, lx1, H - 46)
        hi_, lo_ = emboss_l(bot, 1.4, 2.0)
        art = over(art, flat(lo_ * bot, "#1a0e06", 0.6)); art = over(art, flat(hi_ * bot, "#f5e3b8", 0.2))
        art = bone_line(art, bot, 2.2, nx())
        bcx, bcy = (lx0 + lx1) / 2, (my1 + 30 + H - 46) / 2
        bw_, bh_ = (lx1 - lx0) * 0.38, (H - 76 - my1) * 0.42
        loz = shapes(W, H, [[(bcx, bcy - bh_), (bcx + bw_, bcy), (bcx, bcy + bh_), (bcx - bw_, bcy)]], smooth=False)
        art = inlay(art, loz, 4.0, nx() + 2, bevel=False)
        art = bone_line(art, loz, 2.4, nx())
        art = FO(art, np.clip(outline(loz, 1.0), 0, 1), BRASS, seed=nx(), emboss=0.8)
        corners = []
        for (qx, qy) in [(lx0 + 14, my1 + 44), (lx1 - 14, my1 + 44), (lx0 + 14, H - 60), (lx1 - 14, H - 60)]:
            corners.append([(qx, qy - 9), (qx + 9, qy), (qx, qy + 9), (qx - 9, qy)])
        art = inlay(art, shapes(W, H, corners, smooth=False), 3.0, nx(), bevel=False)
        # brass studs along the rails
        studs = circles(W, H, [(x, y, 3.4) for x in (lx0 + 8, lx1 - 8) for y in (SP + 55, my1 + 15, H - 32)] + [((lx0 + lx1) / 2, y, 3.4) for y in (SP + 55, my1 + 15, H - 32)])
        art = FO(art, studs, BRASS, seed=nx(), emboss=1.2, sparkle=0.2)
    # door rings on the seam
    for sx in (cx - 22, cx + 22):
        plate_ = circles(W, H, [(sx, my0 + 20, 9)])
        art = FO(art, plate_, BRASS, seed=nx(), emboss=1.2)
        ring_ = ellipses(W, H, [(sx, my0 + 44, 15, 19, 0)]) - ellipses(W, H, [(sx, my0 + 44, 11, 15, 0)])
        art = over(art, soft_shadow(np.clip(ring_, 0, 1), "#000000", 2, 0.5, 2, 3))
        art = FO(art, np.clip(ring_, 0, 1), BRASS, seed=nx(), emboss=1.2, sparkle=0.3)
    # threshold step
    art = OV(art, rect(W, H, 0, H - 20, W, H), lambda m: walnut_paint(m, nx(), WAL_D, "#22140a", 0.0))
    art = over(art, flat(outer * light_mask(H, W, 120, 200, 700), "#ffd9a0", 0.12))
    preview(art, "kdoor", bg="#2a1a10")
    save(art, f"{OUT}/door.webp", max_w=480, quality=76)
    clear()

if "band" in PARTS:
    S = 5.0
    W, H = 360, 52  # 24 star periods (3 * S each)
    k = khatam(W, 40, S, 0.0, 2.0, seed=7)
    art = np.zeros((H, W, 4), np.float32)
    art[6:46] = k
    bonec = col_arr(BONE); brassc = col_arr(BRASS)
    for (y0, y1, c) in [(0, 2, brassc * 0.8), (2, 6, bonec), (46, 50, bonec), (50, 52, brassc * 0.8)]:
        art[y0:y1, :, :3] = c * (0.95 + 0.05 * wrap_noise(W, y1 - y0, y0 + 3, 1.0)[..., None]); art[y0:y1, :, 3] = 1
    save_full(art, f"{OUT}/band.webp", quality=84)

if "star" in PARTS:
    W = H = 300
    nx = Seq(3300)
    art = blank(W, H)
    c = 150
    disc = circles(W, H, [(c, c, 140)])
    art = OV(art, disc, lambda m: walnut_paint(m, nx(), WAL, WAL_D, 0.0))
    art = bone_line(art, disc, 3, nx())
    ring_ = np.clip(circles(W, H, [(c, c, 128)]) - circles(W, H, [(c, c, 112)]), 0, 1)
    art = inlay(art, ring_, 3.6, nx(), bevel=False)
    art = bone_line(art, circles(W, H, [(c, c, 128)]), 2, nx()); art = bone_line(art, circles(W, H, [(c, c, 112)]), 2, nx())
    st = shapes(W, H, [star_pts(c, c, 100, 8, 0.7, -math.pi / 2)], smooth=False)
    art = inlay(art, st, 3.6, nx() + 1)
    art = FO(art, np.clip(outline(st, 2.4), 0, 1), BRASS, seed=nx(), emboss=0.9)
    oc = shapes(W, H, [poly_pts(c, c, 40, 8, math.pi / 8)], smooth=False)
    art = GP(art, oc, BONE, "#e2d4b6", seed=nx(), rough=0.4)
    art = inlay(art, shapes(W, H, [star_pts(c, c, 30, 8, 0.66, -math.pi / 2)], smooth=False), 3.0, nx(), bevel=False)
    art = FO(art, circles(W, H, [(c, c, 5)]), BRASS, seed=nx(), emboss=1.2)
    art = FO(art, np.clip(outline(oc, 1.5), 0, 1), BRASS, seed=nx(), emboss=0.8)
    art = over(art, flat(disc * light_mask(H, W, 80, 70, 260), "#ffe2b0", 0.12))
    preview(art, "kstar", bg="#efe4cc")
    save(art, f"{OUT}/star.webp", max_w=200, quality=82)
    clear()

if "frame" in PARTS:
    W, H = 620, 840
    nx = Seq(3700)
    art = blank(W, H)
    SP = 400
    outer = rect(W, H, 0, 0, W, H)
    b_o = shapes(W, H, [[(30, H - 30)] + arch_pts(30, W - 30, SP, f=0.6) + [(W - 30, H - 30)]], smooth=False)
    b_i = shapes(W, H, [[(60, H - 30)] + arch_pts(60, W - 60, SP, f=0.6) + [(W - 60, H - 30)]], smooth=False)
    hole = shapes(W, H, [[(82, H - 52)] + arch_pts(82, W - 82, SP, f=0.6) + [(W - 82, H - 52)]], smooth=False)
    wood_m = np.clip(outer - hole, 0, 1)
    art = OV(art, wood_m, lambda m: walnut_paint(m, nx()))
    art = inlay(art, np.clip(b_o - b_i, 0, 1), 4.6, nx(), bevel=False)
    art = bone_line(art, b_o, 2.5, nx()); art = bone_line(art, b_i, 2.5, nx()); art = bone_line(art, hole, 3, nx())
    art = FO(art, np.clip(outline(hole, 1.2), 0, 1) * 0 + np.clip(outline(outer, 2.0), 0, 1), BRASS, seed=nx(), emboss=0.7)
    hi, lo = emboss_l(wood_m, 1.0, 3)
    art = over(art, flat(lo * wood_m, "#140a04", 0.4)); art = over(art, flat(hi * wood_m, "#c08a5a", 0.25))
    # cast shadow of the frame onto the photo
    sh = np.clip(gaussian_filter(1 - hole, 7) * hole, 0, 1)
    art = over(art, flat(sh, "#140a04", 0.7))
    art = bone_line(art, rect(W, H, 8, 8, W - 8, H - 8), 2.5, nx())
    for (sx, sy) in [(70, 80), (W - 70, 80)]:
        st = shapes(W, H, [star_pts(sx, sy, 34, 8, 0.7, -math.pi / 2)], smooth=False)
        art = inlay(art, st, 3.0, nx(), bevel=False)
        art = FO(art, np.clip(outline(st, 1.6), 0, 1), BRASS, seed=nx(), emboss=0.9)
    preview(art, "kframe", bg="#efe4cc")
    save_full(art, f"{OUT}/frame.webp", size=(434, 588), quality=80)
    clear()

if "walnut" in PARTS:
    W = H = 256
    n1 = wrap_noise(W, H, 11, (40, 1.5)) if False else None
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    warp = wrap_noise(W, H, 12, 14) * 8
    stripes = 0.5 + 0.5 * np.sin((xx / W) * math.tau * 9 + warp)
    fine = wrap_noise(W, H, 13, 0.8)
    base = col_arr("#3a2414")[None, None] * (0.85 + 0.16 * stripes[..., None] + 0.06 * (fine[..., None] - 0.5))
    img = np.concatenate([np.clip(base, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/walnut.webp", quality=80)

if "divider" in PARTS:
    W, H = 460, 70
    nx = Seq(4100)
    art = blank(W, H)
    for (x0, x1) in [(20, 196), (264, 440)]:
        strip = rect(W, H, x0, 29, x1, 41)
        art = inlay(art, strip, 3.6, nx(), bevel=False)
        art = bone_line(art, strip, 1.8, nx())
    for x in (16, 444):
        art = FO(art, shapes(W, H, [[(x, 27), (x + 8, 35), (x, 43), (x - 8, 35)]], smooth=False), BRASS, seed=nx(), emboss=1.0)
    st = shapes(W, H, [star_pts(230, 35, 30, 8, 0.68, -math.pi / 2)], smooth=False)
    art = inlay(art, st, 3.0, nx(), bevel=False)
    art = FO(art, np.clip(outline(st, 1.8), 0, 1), BRASS, seed=nx(), emboss=0.9)
    art = GP(art, shapes(W, H, [poly_pts(230, 35, 10, 8, math.pi / 8)], smooth=False), BONE, seed=nx(), rough=0.3)
    preview(art, "kdiv", bg="#efe4cc")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
    clear()
