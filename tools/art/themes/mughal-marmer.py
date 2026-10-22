"""Mughal Marmer — white Makrana-like marble with pietra-dura inlay (carnelian, coral, lapis with pyrite flecks, jade,
malachite, onyx fillets) cut and set flush, polished; a cusped (multifoil) Mughal arch, a pierced jali screen,
an inlaid flowering plant, a vine border. Ivory + soft gold.
Run: python3 -I mughal-marmer.py [part ...]   parts: marble arch jali spray border flower
Assets -> public/themes/art/mughal-marmer/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b3_lib import *

OUT = outdir("mughal-marmer")
PARTS = sys.argv[1:] or ["marble", "arch", "jali", "spray", "border", "flower"]
IVORY = "#f6f1e6"
SEQ = Seq(300)


def tileable_rgb(arr):
    """Seamless 4-way cross-fade with the half-rolled copies."""
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = (np.sin(math.pi * xx / w) ** 2)[..., None]; wy = (np.sin(math.pi * yy / h) ** 2)[..., None]
    ax = np.roll(arr, w // 2, 1); ay = np.roll(arr, h // 2, 0); axy = np.roll(ax, h // 2, 0)
    return arr * wx * wy + ax * (1 - wx) * wy + ay * wx * (1 - wy) + axy * (1 - wx) * (1 - wy)


# ---------- inlay vocabulary (each petal / leaf half is its own cut stone) ----------
def put(art, W, H, pts, kind, smooth=True):
    m = shape_mask(W, H, pts, smooth=smooth)
    return ST(art, m, kind, SEQ())


def leaf2(art, W, H, x, y, L, wd, ang, kinds=("jade", "malachite"), cup=0.15):
    """Leaf cut as two stones along the midrib (light half / dark half), the pietra-dura way of shading."""
    pts = petal_pts(x, y, L, wd, ang, n=16, cup=cup)
    m = shape_mask(W, H, pts)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = ((xx - x) * math.sin(ang) - (yy - y) * math.cos(ang)) > 0
    a = m * side; b = m * (~side)
    # thin joint between halves
    seam = gaussian_filter(np.abs(np.diff(side.astype(np.float32), axis=1, prepend=0)) + np.abs(np.diff(side.astype(np.float32), axis=0, prepend=0)), 0.5)
    art = ST(art, np.clip(a - seam * 2, 0, 1), kinds[0], SEQ())
    art = ST(art, np.clip(b - seam * 2, 0, 1), kinds[1], SEQ())
    return art


def stem(art, W, H, pts, width, kind="malachite"):
    return ST(art, strokes(W, H, [(pts, width, (0.05, 0.35))]), kind, SEQ())


def rosette(art, W, H, cx, cy, r, n=8, rot=0.0, petal="carnelian", petal2="coral", centre="lapis", ring_kind="amber"):
    """Inlaid rosette: n outer petals (alternating two stones), a ring, a centre disc."""
    for k in range(n):
        a = rot + k * 2 * math.pi / n
        pts = petal_pts(cx + math.cos(a) * r * 0.28, cy + math.sin(a) * r * 0.28, r * 0.78, r * 0.42, a, n=14)
        art = put(art, W, H, pts, petal if k % 2 == 0 else petal2)
    art = ST(art, circle_mask(W, H, cx, cy, r * 0.36), ring_kind, SEQ())
    art = ST(art, circle_mask(W, H, cx, cy, r * 0.22), centre, SEQ())
    return art


def tulip(art, W, H, x, y, s, ang, kinds=("carnelian", "coral", "carnelian")):
    """Three-petal tulip/poppy seen from the side, pointing along ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    art = put(art, W, H, petal_pts(x - px * s * 0.28, y - py * s * 0.28, s * 1.0, s * 0.42, ang - 0.32, n=14, cup=0.2), kinds[1])
    art = put(art, W, H, petal_pts(x + px * s * 0.28, y + py * s * 0.28, s * 1.0, s * 0.42, ang + 0.32, n=14, cup=0.2), kinds[2])
    art = put(art, W, H, petal_pts(x, y, s * 1.12, s * 0.46, ang, n=16, cup=0.1), kinds[0])
    # calyx
    art = put(art, W, H, ellipse_pts(x - ca * s * 0.05, y - sa * s * 0.05, s * 0.2, s * 0.13, 12, ang), "jade")
    return art


def bell(art, W, H, x, y, s, ang, kind="lapis", kind2="turquoise"):
    """Small bell flower: two flared petals + middle."""
    ca, sa = math.cos(ang), math.sin(ang)
    art = put(art, W, H, petal_pts(x, y, s, s * 0.36, ang - 0.5, n=12), kind)
    art = put(art, W, H, petal_pts(x, y, s, s * 0.36, ang + 0.5, n=12), kind)
    art = put(art, W, H, petal_pts(x, y, s * 0.9, s * 0.3, ang, n=12), kind2)
    return art


if "marble" in PARTS:
    # seamless tile: every noise is wrap-filtered and the vein phase advances by whole periods across the tile
    S = 720
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    nw = lambda sd, sg: noise(S, S, sd, sg, wrap=True)
    n1 = nw(1, 60) * 0.6 + nw(2, 24) * 0.3 + nw(3, 8) * 0.1
    n2 = nw(4, 20) * 0.7 + nw(5, 6) * 0.3
    n3 = nw(6, 110)
    ph = 2 * xx / S + 1 * yy / S + n1 * 2.6 + n2 * 0.4
    ridge = 1 - np.abs(np.sin(ph * math.pi))
    ph2 = 3 * xx / S - 2 * yy / S + n2 * 2.2 + n1 * 1.2
    ridge2 = 1 - np.abs(np.sin(ph2 * math.pi))
    strength = np.clip((nw(7, 45) - 0.3) * 1.8, 0, 1)
    vein = np.clip((ridge ** 70 * 0.8 + ridge ** 10 * 0.25) * strength + ridge2 ** 110 * np.clip((n3 - 0.45) * 3, 0, 1) * 0.5, 0, 1)
    rgb = lerp3(C("#f7f3ea"), C("#ece2d0"), np.clip(0.4 + (n3 - 0.5) * 0.9, 0, 1) * 0.55)
    rgb = lerp3(rgb, C("#8f8a84"), gaussian_filter(vein, 0.6, mode="wrap") * 0.62)
    g = noise(S, S, 9, 0.6, wrap=True)
    rgb = rgb * (0.99 + 0.02 * g[..., None])
    arr = rgba(rgb, np.ones((S, S), np.float32))
    rgb_save(arr, f"{OUT}/marble.webp", quality=74, size=(600, 600))
    to_image(arr).convert("RGB").save(f"{PREV}/mm-marble.png")
    clear()

if "arch" in PARTS:
    W, H = 640, 820
    cx = W / 2
    a = 205; e = a * 0.36; R = a + e; spring = 404
    # base pointed-arch curve (left spring -> apex -> right spring)
    th_apex = math.acos(e / R)
    left = [(cx + e + R * math.cos(math.pi - t * (math.pi - th_apex)), spring - R * math.sin(math.pi - t * (math.pi - th_apex))) for t in np.linspace(0, 1, 80)]
    right = [(2 * cx - x, y) for x, y in left[::-1]]
    base = left + right[1:]
    seglen = [math.hypot(base[i + 1][0] - base[i][0], base[i + 1][1] - base[i][1]) for i in range(len(base) - 1)]
    L = sum(seglen); cum = np.concatenate([[0], np.cumsum(seglen)])
    N = 11
    r = L / N / 2 * 1.08
    lobes = []
    for i in range(N):
        sp = (i + 0.5) * L / N
        j = int(np.searchsorted(cum, sp)) - 1; j = max(0, min(len(base) - 2, j))
        t = (sp - cum[j]) / seglen[j]
        bx_, by_ = base[j][0] + (base[j + 1][0] - base[j][0]) * t, base[j][1] + (base[j + 1][1] - base[j][1]) * t
        vx_, vy_ = cx - bx_, (spring + 60) - by_
        nn_ = math.hypot(vx_, vy_)
        lobes.append((bx_ + vx_ / nn_ * r * 0.5, by_ + vy_ / nn_ * r * 0.5))
    oy1 = H + 20
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        path = skia.Path(); path.moveTo(cx - a, oy1)
        for x, y in base:
            path.lineTo(x, y)
        path.lineTo(cx + a, oy1); path.close()
        cv.c.drawPath(path, p)
        for x, y in lobes:
            cv.c.drawCircle(x, y, r, p)
        cv.c.drawRect(skia.Rect(cx - a - r * 0.0, spring, cx + a, oy1), p)
    opening = mask_from(W, H, draw)
    # small lobes at the springs (the cusps end in a little curl into the jamb)
    dist_out = ndi.distance_transform_edt(opening < 0.5).astype(np.float32)
    # marble panel with a chamfered edge around the opening
    art = marble(W, H, seed=12, base="#f7f3ea", vein="#928c85", warm="#ebe0cc", scale=0.9, angle=0.9, veins=1.1)
    hg = np.clip(dist_out / 10, 0, 1) * 8
    sh = shade(gaussian_filter(hg, 1.2), (-0.5, -0.85), 1.4)
    art[..., :3] *= (0.86 + 0.28 * sh)[..., None] * 0.97 + 0.03
    # inlay band around the opening: onyx fillet, amber fillet, a run of stone buds between, onyx fillet
    def ringd(d0, d1):
        return np.clip((dist_out - d0) * 1.2, 0, 1) * np.clip((d1 - dist_out) * 1.2, 0, 1) * (dist_out < 200)
    art = ST(art, ringd(10, 13.5), "onyx", SEQ())
    art = ST(art, ringd(36, 39.5), "onyx", SEQ())
    art = ST(art, ringd(16, 18), "amber", SEQ())
    art = ST(art, ringd(31.5, 33.5), "amber", SEQ())
    # buds along the band: use the lobe centres pushed outward along the curve normal
    for i, (x, y) in enumerate(lobes):
        # outward direction = away from the arch's interior reference point
        vx, vy = x - cx, y - (spring + 80)
        nn = math.hypot(vx, vy); vx, vy = vx / nn, vy / nn
        bx, by = x + vx * (r + 25.5), y + vy * (r + 25.5)
        art = ST(art, circle_mask(W, H, bx, by, 5.2), "lapis" if i % 2 == 0 else "carnelian", SEQ())
        for k in (-1, 1):
            lx, ly = bx + (-vy) * k * 12, by + vx * k * 12
            art = put(art, W, H, petal_pts(bx + (-vy) * k * 5, by + vx * k * 5, 13, 5, math.atan2(vx * k, -vy * k), n=10), "jade")
    for side in (-1, 1):
        x = cx + side * (a + 25)
        for y in range(spring + 40, H - 30, 54):
            art = ST(art, circle_mask(W, H, x, y, 5.2), "lapis" if (y // 54) % 2 == 0 else "carnelian", SEQ())
            for k in (-1, 1):
                art = put(art, W, H, petal_pts(x, y + k * 5, 13, 5, math.pi / 2 * k, n=10), "jade")
    # outer frame: onyx + amber fillets near the edges
    def rectline(ins, wd):
        m = np.zeros((H, W), np.float32)
        m[ins:H - ins, ins:W - ins] = 1
        m2 = np.zeros((H, W), np.float32); m2[ins + wd:H - ins - wd, ins + wd:W - ins - wd] = 1
        return gaussian_filter(m - m2, 0.5)
    art = ST(art, rectline(16, 4), "onyx", SEQ())
    art = ST(art, rectline(26, 2), "amber", SEQ())
    # spandrels: a rosette with scrolling stems & leaves in each upper corner
    for side, sd in ((-1, 0), (1, 1)):
        fx = cx + side * 222
        fy = 150
        def S(px):  # geometry is drawn for the left spandrel and mirrored for the right
            return [((2 * cx - x) if side > 0 else x, y) for x, y in px]
        st1 = S(bez((92, 126), (120, 96), (150, 74), (194, 62), 30))
        st2 = S(bez((92, 126), (70, 170), (64, 214), (56, 262), 30))
        st3 = S(bez((92, 126), (118, 150), (124, 168), (122, 196), 24))
        for pp in (st1, st2, st3):
            art = stem(art, W, H, pp, 4.2)
        tip1 = st1[-1]; tip2 = st2[-1]; tip3 = st3[-1]
        art = tulip(art, W, H, tip1[0], tip1[1], 22, -0.35 if side < 0 else math.pi + 0.35)
        art = bell(art, W, H, tip2[0], tip2[1], 20, math.pi / 2 + (0.25 if side < 0 else -0.25))
        art = put(art, W, H, ellipse_pts(tip3[0], tip3[1], 8, 10, 10), "amber")
        for (pp, t, sgn) in ((st1, 0.45, 1), (st2, 0.5, -1), (st3, 0.55, 1), (st1, 0.75, -1)):
            q = pp[int(len(pp) * t)]
            q2 = pp[int(len(pp) * t) + 1]
            ang = math.atan2(q2[1] - q[1], q2[0] - q[0]) + sgn * 0.9
            art = leaf2(art, W, H, q[0], q[1], 30, 12, ang)
        rx = 92 if side < 0 else W - 92
        art = rosette(art, W, H, rx, 126, 30, 8, 0.2 * side)
    art[..., 3] *= 1 - opening
    # soft gold line hugging the opening (gilded edge)
    gl = np.clip((dist_out - 1.0) * 1.5, 0, 1) * np.clip((4.0 - dist_out) * 1.5, 0, 1)
    art = FO(art, gl, "#c9a35e", seed=3)
    art = add_grain(art, 2, 0.012)
    preview(art, "mm-arch", bg="#3a5a7a")
    save_full(art, f"{OUT}/arch.webp", size=(560, 718), quality=82)
    clear()

if "jali" in PARTS:
    # Pierced marble screen: interlocking hexagram stars on a triangular lattice, chamfered marble bars.
    W, H = 420, 560
    holes_cv = Canvas(W, H); p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    d = 52
    rows = int(H / (d * 0.866)) + 3
    for j in range(-1, rows):
        for i in range(-1, int(W / d) + 2):
            x = i * d + (d / 2 if j % 2 else 0); y = j * d * 0.866
            star = star_pts(x, y, d * 0.42, d * 0.42 * 0.62, 6, math.pi / 6)
            holes_cv.c.drawPath(poly_path(star), p)
            # small triangles in the gaps
            for k, (tx, ty) in enumerate(((x + d / 2, y + d * 0.866 / 3), (x, y + d * 0.866 * 2 / 3))):
                rot = -math.pi / 2 if k == 0 else math.pi / 2
                tri = [(tx + math.cos(rot + q * 2 * math.pi / 3) * d * 0.1, ty + math.sin(rot + q * 2 * math.pi / 3) * d * 0.1) for q in range(3)]
                holes_cv.c.drawPath(poly_path(tri), p)
    holes = holes_cv.array()[..., 3]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fr = 26
    panel = ((yy > 190) | (((xx - W / 2) / (W / 2)) ** 2 + ((yy - 190) / 190) ** 2 < 1)).astype(np.float32)
    inner = ((yy > 190) | (((xx - W / 2) / (W / 2 - fr)) ** 2 + ((yy - 190) / (190 - fr)) ** 2 < 1)).astype(np.float32)
    inner[:, :fr] = 0; inner[:, W - fr:] = 0; inner[H - fr:, :] = 0
    solid = np.clip(panel - inner * holes, 0, 1)
    solid = gaussian_filter(solid, 0.6)
    art = marble(W, H, seed=21, base="#f7f3ea", vein="#aaa49c", warm="#ebe0cc", scale=0.9, angle=1.1, veins=0.5)
    hg = height_of(solid, 6, "round") + (1 - inner) * 3
    sh = shade(hg, (-0.5, -0.85), 1.6)
    art[..., :3] *= (0.72 + 0.4 * sh)[..., None]
    art[..., 3] = solid
    edge2 = np.clip(gaussian_filter((ndi.binary_erosion(panel > 0.5, iterations=11)).astype(np.float32), 0.5) - gaussian_filter((ndi.binary_erosion(panel > 0.5, iterations=13)).astype(np.float32), 0.5), 0, 1)
    art = FO(art, edge2, "#c9a35e", seed=5)
    art = add_grain(art, 4, 0.012)
    preview(art, "mm-jali", bg="#8e3b2a")
    save(art, f"{OUT}/jali.webp", max_w=320, quality=80)
    clear()

if "spray" in PARTS:
    # Inlaid flowering plant (dado-panel style): tulip crown, bell flowers, buds, paired split leaves, leafy mound.
    W, H = 460, 620
    art = blank(W, H)
    cx = W / 2
    main = bez((cx, 600), (cx - 6, 470), (cx + 10, 300), (cx, 150), 50)
    lft = bez((cx, 430), (cx - 40, 380), (cx - 110, 360), (cx - 120, 262), 34)
    rgt = bez((cx + 2, 400), (cx + 50, 360), (cx + 116, 340), (cx + 126, 250), 34)
    lft2 = bez((cx, 520), (cx - 60, 500), (cx - 120, 500), (cx - 150, 448), 24)
    rgt2 = bez((cx, 510), (cx + 60, 492), (cx + 124, 488), (cx + 156, 440), 24)
    for pp, wd in ((main, 6.5), (lft, 4.6), (rgt, 4.6), (lft2, 3.8), (rgt2, 3.8)):
        art = stem(art, W, H, pp, wd)
    # leaves along the main stem
    for t, sgn, Ll in ((0.22, 1, 70), (0.22, -1, 66), (0.48, 1, 58), (0.5, -1, 62), (0.72, 1, 44), (0.72, -1, 44)):
        q = main[int(len(main) * t)]
        ang = -math.pi / 2 + sgn * 0.95
        art = leaf2(art, W, H, q[0], q[1], Ll, Ll * 0.34, ang)
    for pp in (lft, rgt):
        q = pp[int(len(pp) * 0.5)]
        q2 = pp[int(len(pp) * 0.5) + 1]
        ang = math.atan2(q2[1] - q[1], q2[0] - q[0])
        art = leaf2(art, W, H, q[0], q[1], 40, 14, ang + 1.0)
        art = leaf2(art, W, H, q[0], q[1], 36, 13, ang - 1.1)
    # mound of small leaves at the base
    for k in range(9):
        ang = -math.pi / 2 + (k - 4) * 0.36
        art = leaf2(art, W, H, cx + (k - 4) * 6, 598, 40 + (4 - abs(k - 4)) * 8, 13, ang, cup=0.25)
    # flowers
    art = tulip(art, W, H, main[-1][0], main[-1][1] + 6, 62, -math.pi / 2)
    art = bell(art, W, H, lft[-1][0], lft[-1][1], 40, -math.pi / 2 - 0.25)
    art = bell(art, W, H, rgt[-1][0], rgt[-1][1], 40, -math.pi / 2 + 0.25)
    art = rosette(art, W, H, lft2[-1][0], lft2[-1][1], 20, 6, 0.3, petal="amber", petal2="coral", centre="carnelian", ring_kind="jade")
    art = rosette(art, W, H, rgt2[-1][0], rgt2[-1][1], 20, 6, 0.0, petal="amber", petal2="coral", centre="carnelian", ring_kind="jade")
    preview(art, "mm-spray", bg=IVORY)
    save(art, f"{OUT}/spray.webp", max_w=360, quality=84)
    clear()

if "border" in PARTS:
    # Divider: inlaid vine running out from a central rosette, buds and split leaves, onyx hairline below.
    W, H = 640, 96
    art = blank(W, H)
    cx, cy = W / 2, 48
    for side in (-1, 1):
        pts = [(cx + side * x, cy + math.sin(x / 34) * 9 * (1 - x / 300)) for x in np.linspace(30, 290, 60)]
        art = stem(art, W, H, pts, 3.4)
        for i, x in enumerate((70, 130, 190, 246)):
            k = int((x - 30) / 260 * 59)
            q = pts[k]
            up = 1 if i % 2 == 0 else -1
            art = leaf2(art, W, H, q[0], q[1], 24 - i * 2.5, 9 - i * 0.6, (-math.pi / 2) * up + side * 0.7)
            if i < 3:
                bx, by = q[0] + side * 14, q[1] - up * -14
                art = ST(art, circle_mask(W, H, q[0] + side * 22, q[1] + up * 12, 4.6 - i * 0.6), "carnelian" if i % 2 else "lapis", SEQ())
        art = ST(art, circle_mask(W, H, cx + side * 296, pts[-1][1], 3), "amber", SEQ())
    art = rosette(art, W, H, cx, cy, 26, 8, 0.0)
    preview(art, "mm-border", bg=IVORY)
    save(art, f"{OUT}/border.webp", max_w=460, quality=84)
    clear()

if "flower" in PARTS:
    S = 200
    art = blank(S, S)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        art = leaf2(art, S, S, S / 2 + math.cos(a) * 30, S / 2 + math.sin(a) * 30, 56, 20, a)
    art = rosette(art, S, S, S / 2, S / 2, 56, 8, math.pi / 8)
    preview(art, "mm-flower", bg=IVORY)
    save(art, f"{OUT}/flower.webp", max_w=160, quality=84)
    clear()

report(OUT)
