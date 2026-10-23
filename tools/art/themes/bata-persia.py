"""Bata Persia — Persian banna'i brickwork: buff fired bricks laid in running bond where single glazed brick-ends
(turquoise and cobalt) draw purely geometric patterns (diamond lattices, stepped zigzags, concentric steps — no script).
A pointed brick arch (pishtaq) with voussoir ring and glazed star tiles in the spandrels, a seamless brick tile, a
banna'i panel, a zigzag border band, a small divider and a glazed star.
Run: python3 -I bata-persia.py [part ...]   parts: tile arch panel band divider star
Assets -> public/themes/art/bata-persia/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i1_lib import *

OUT = outdir("bata-persia")
PARTS = sys.argv[1:] or ["tile", "arch", "panel", "band", "divider", "star"]
BUFF = ["#d8b88a", "#d3b081", "#dcbf93", "#cfaa7a", "#d6b486"]
MORTAR = "#cdb895"
TURQ = ["#2a9893", "#33a29c", "#238c88", "#38a8a0"]
COBALT = ["#22488a", "#274c88", "#1d4080", "#2b5596"]
PLASTER = "#f3e8d6"


def paint_cells(W, H, cells, seed=1, wrap=False, mortar_mask=None, depth=0.3):
    """cells: list of (x0, y0, x1, y1, kind) with kind in 'b' (buff brick), 't' (turquoise glaze), 'c' (cobalt glaze).
    Returns RGBA float: mortar bed + slightly irregular bricks with grain, glaze sheen, chips and relief shading."""
    rng = random.Random(seed)
    col = skia.Surface(W, H)
    cv = col.getCanvas(); cv.clear(skia.ColorTRANSPARENT)
    gl = skia.Surface(W, H); gc = gl.getCanvas(); gc.clear(skia.ColorTRANSPARENT)
    sp = skia.Surface(W, H); sc = sp.getCanvas(); sc.clear(skia.ColorTRANSPARENT)
    offs = [(0, 0)] + ([(dx, dy) for dx in (-W, 0, W) for dy in (-H, 0, H) if (dx, dy) != (0, 0)] if wrap else [])
    for (x0, y0, x1, y1, k) in cells:
        pal = BUFF if k == "b" else TURQ if k == "t" else COBALT
        c = jitter_hex(rng.choice(pal), rng, 0.05 if k == "b" else 0.03)
        inset = rng.uniform(0.9, 1.4)
        rot = rng.uniform(-0.8, 0.8)
        dx_, dy_ = rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7)
        rr = rng.uniform(1.0, 2.6)
        for ox, oy in offs:
            r = skia.Rect(x0 + inset + dx_ + ox, y0 + inset + dy_ + oy, x1 - inset + dx_ + ox, y1 - inset + dy_ + oy)
            for canvas, colr in ((cv, c),) + (((gc, "#ffffff"),) if k != "b" else ()):
                canvas.save(); canvas.rotate(rot, r.centerX(), r.centerY())
                canvas.drawRoundRect(r, rr, rr, skia.Paint(AntiAlias=True, Color=color(colr)))
                canvas.restore()
            if k != "b":
                # glaze highlight: a soft streak near the upper-left of the brick face
                hw, hh = (x1 - x0), (y1 - y0)
                sc.drawOval(skia.Rect(x0 + ox + hw * 0.18, y0 + oy + hh * 0.16, x0 + ox + hw * 0.62, y0 + oy + hh * 0.42), skia.Paint(AntiAlias=True, Color=color("#ffffff", 0.75)))
    arr = np.asarray(col.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType), np.float32) / 255
    glz = np.asarray(gl.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType), np.float32)[..., 3] / 255
    spec = np.asarray(sp.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType), np.float32)[..., 3] / 255
    a = arr[..., 3]
    rgb = arr[..., :3].copy()
    mode = "wrap" if wrap else "nearest"
    # grain + mottling (fired clay) — strong on buff, faint on glaze
    g1 = wrap_noise(W, H, seed + 1, 0.7) if wrap else (lambda n: (n - n.min()) / (n.max() - n.min() + 1e-6))(gaussian_filter(np.random.default_rng(seed + 1).random((H, W)).astype(np.float32), 0.7))
    g2 = wrap_noise(W, H, seed + 2, 9) if wrap else fbm(W, H, seed + 2, 40, 3)
    tex = 1 + ((g1 - 0.5) * 0.22 + (g2 - 0.5) * 0.16) * (1 - 0.75 * glz)
    rgb = rgb * tex[..., None]
    # pits / chips on the brick edges
    pits = (g1 > 0.86) * (1 - glz)
    rgb = rgb * (1 - pits[..., None] * 0.25)
    # relief: light from the top-left
    sm = gaussian_filter(a, 1.6, mode=mode)
    gy, gx = np.gradient(sm)
    light = np.clip(-(gx + gy) * 3.2 * depth, -0.18, 0.12)
    rgb = rgb * (1 + light[..., None])
    # glaze sheen + crackle
    rgb = rgb * (1 - spec[..., None] * 0.0) + spec[..., None] * 0.28 * glz[..., None]
    crack = np.clip((np.abs(np.sin((g2 * 40))) < 0.04) * glz * 0.5, 0, 1)
    rgb = rgb * (1 - crack[..., None] * 0.18)
    # mortar bed behind the bricks, with a soft cast shadow
    if mortar_mask is None:
        mortar_mask = np.ones((H, W), np.float32)
    m_rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(MORTAR), np.float32)
    m_rgb = m_rgb * (1 + (g1[..., None] - 0.5) * 0.25)
    shadow = np.roll(np.roll(gaussian_filter(a, 1.5, mode=mode), 2, 0), 2, 1)
    m_rgb = m_rgb * (1 - 0.32 * shadow[..., None])
    out_rgb = rgb * a[..., None] + m_rgb * (1 - a[..., None])
    out_a = np.clip(np.maximum(a, mortar_mask), 0, 1)
    return np.concatenate([np.clip(out_rgb, 0, 1), out_a[..., None]], -1)


def lay(nx_, ny_, cw, ch, pat, x0=0, y0=0, keep=None, bond=True):
    """Running bond of 2-cell bricks over an nx_ x ny_ cell grid; pat(i, j) -> None | 't' | 'c' turns a cell into a
    single glazed brick-end. keep(i, j) -> bool limits the field."""
    out = []
    for j in range(ny_):
        i = -(j % 2) if bond else 0
        while i < nx_:
            cells = [c for c in (i, i + 1) if 0 <= c < nx_]
            if not cells:
                i += 2; continue
            kinds = [pat(c, j) for c in cells]
            ok = [keep(c, j) if keep else True for c in cells]
            if len(cells) == 2 and kinds[0] is None and kinds[1] is None and all(ok):
                out.append((x0 + cells[0] * cw, y0 + j * ch, x0 + (cells[1] + 1) * cw, y0 + (j + 1) * ch, "b"))
            else:
                for c, k, o in zip(cells, kinds, ok):
                    if o:
                        out.append((x0 + c * cw, y0 + j * ch, x0 + (c + 1) * cw, y0 + (j + 1) * ch, k or "b"))
            i += 2
    return out


def zig(i, j, rows, period=10, line=1):
    """Stepped zigzag across a band `rows` tall: returns 't'/'c' on the zig line and its echo."""
    p = i % period
    z = abs(p - period // 2) * (rows - 1) / (period // 2)
    zi = int(round(z))
    if j == zi:
        return "t"
    if j == rows - 1 - zi and rows > 3:
        return "c"
    return None


def lattice(i, j, P=14):
    """Stair-stepped diamond lattice on half-brick cells: turquoise diagonals, cobalt crossings and centres."""
    a, b = (i + j) % P, (i - j) % P
    if a == 0 and b == 0:
        return "c"
    if a in (0, 1) or b in (0, 1):
        return "t"
    if a == P // 2 and b == P // 2:
        return "c"
    return None


if "tile" in PARTS:
    # seamless tile: running bond (half-brick cells 18 x 16) with the stepped diamond lattice
    cw, ch = 18, 16
    W, H = 28 * cw, 28 * ch
    cells = lay(28, 28, cw, ch, lattice)
    art = paint_cells(W, H, cells, seed=7, wrap=True)
    show(art, "bp-tile")
    save_full(art, f"{OUT}/tile.webp", quality=74)

if "arch" in PARTS:
    W, H = 648, 864
    cw, ch = 18, 16
    nx_, ny_ = W // cw, H // ch
    cxA = W / 2
    spring_y, apex_y, half = 380, 130, 200

    def in_arch(x, y, grow=0.0):
        """Pointed (two-centred) arch opening: legs from spring_y down, apex at apex_y."""
        hw = half + grow
        if y >= spring_y:
            return abs(x - cxA) <= hw
        # each side is an arc centred on the opposite side's inner point
        r = hw * 1.55
        ccx = cxA - (r - hw) if x >= cxA else cxA + (r - hw)
        if y < apex_y - grow:
            return False
        return (x - ccx) ** 2 + (y - spring_y) ** 2 <= r * r and abs(x - cxA) <= hw

    def pat(i, j):
        if j < 5:
            return zig(i, j, 5, 8)
        if j == 5:
            return "c" if i % 2 == 0 else None
        return lattice(i, j - 6)

    def keep(i, j):
        x, y = (i + 0.5) * cw, (j + 0.5) * ch
        return not in_arch(x, y, 30)
    cells = lay(nx_, ny_, cw, ch, pat, keep=keep)
    art = paint_cells(W, H, cells, seed=11)
    # remove the mortar bed inside the arch zone (paint plaster there instead)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    inner = mask_from(W, H, lambda cv: None)
    opening = np.zeros((H, W), np.float32)
    ring_m = np.zeros((H, W), np.float32)
    for y in range(H):
        pass
    # vectorised arch masks
    def arch_mask(grow):
        hw = half + grow
        r = hw * 1.55
        right = (xx >= cxA)
        ccx = np.where(right, cxA - (r - hw), cxA + (r - hw))
        top = ((xx - ccx) ** 2 + (yy - spring_y) ** 2 <= r * r) & (np.abs(xx - cxA) <= hw) & (yy < spring_y)
        legs = (yy >= spring_y) & (np.abs(xx - cxA) <= hw)
        return (top | legs).astype(np.float32)
    opening = gaussian_filter(arch_mask(0), 0.8)
    outer = gaussian_filter(arch_mask(30), 0.8)
    art[..., 3] *= 1 - outer
    # plaster recess inside the opening, shadowed towards the crown
    pl = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(PLASTER), np.float32)
    n = fbm(W, H, 5, 60, 3)
    pl *= (0.96 + 0.06 * n)[..., None]
    depth = np.clip(1 - (yy - apex_y) / 260, 0, 1) * 0.16 + np.clip(1 - np.abs(xx - cxA) / half, 0, 1) * -0.03
    pl *= (1 - depth)[..., None]
    rim_shadow = gaussian_filter(1 - arch_mask(-2), 6) * opening
    pl *= (1 - 0.22 * rim_shadow)[..., None]
    plaster = np.concatenate([pl, opening[..., None]], -1)
    art = over(art, plaster)
    # voussoir ring: radial bricks between the opening and the field, every third glazed
    vou = []
    hw0, hw1 = half + 2, half + 30
    for side in (-1, 1):
        r0, r1 = hw0 * 1.55, hw1 * 1.55
        ccx0 = cxA - side * (r0 - hw0); ccx1 = cxA - side * (r1 - hw1)
        # angles from the spring line up to the apex
        a_end = math.acos(max(-1, min(1, abs(cxA - ccx0) / r0)))
        steps = 15
        for k in range(steps):
            t0, t1 = k / steps, (k + 1) / steps
            def pt(t, rr, ccx_):
                ang = (a_end) * t
                return (ccx_ + side * rr * math.cos(ang) if False else ccx_ + side * rr * math.cos(ang * 1.0 + 0), spring_y - rr * math.sin(ang))
            p00 = (ccx0 + side * r0 * math.cos(a_end * t0) * 1.0, spring_y - r0 * math.sin(a_end * t0))
            p01 = (ccx0 + side * r0 * math.cos(a_end * t1), spring_y - r0 * math.sin(a_end * t1))
            a1_end = math.acos(max(-1, min(1, abs(cxA - ccx1) / r1)))
            p10 = (ccx1 + side * r1 * math.cos(a1_end * t0), spring_y - r1 * math.sin(a1_end * t0))
            p11 = (ccx1 + side * r1 * math.cos(a1_end * t1), spring_y - r1 * math.sin(a1_end * t1))
            vou.append(([p00, p01, p11, p10], "t" if k % 3 == 1 else "b"))
        # legs: stacked bricks down the jambs
        for y in range(spring_y, H, 20):
            x_in = cxA + side * hw0; x_out = cxA + side * hw1
            vou.append(([(x_in, y), (x_out, y), (x_out, y + 20), (x_in, y + 20)], "t" if (y // 20) % 4 == 1 else "b"))
    for kind in ("b", "t"):
        polys_ = [p for p, k in vou if k == kind]
        m = polys(W, H, polys_)
        m = np.clip(m - gaussian_filter(edge_of(m, 1.2), 0.5) * 1.5, 0, 1)
        layer = paint_cells(W, H, [], seed=17)
        base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(BUFF[0] if kind == "b" else TURQ[0]), np.float32)
        base *= (0.92 + 0.14 * fbm(W, H, 23 + (kind == "t"), 14, 3))[..., None]
        gy, gx = np.gradient(gaussian_filter(m, 1.6))
        base *= (1 + np.clip(-(gx + gy) * 1.6, -0.2, 0.2))[..., None]
        art = over(art, np.concatenate([np.clip(base, 0, 1), m[..., None]], -1))
    # mortar joints between voussoirs
    joints = np.zeros((H, W), np.float32)
    # glazed 8-point stars in the spandrels
    for sx in (cxA - 236, cxA + 236):
        sy = 210
        sq1 = polys(W, H, [[(sx + 34 * math.cos(a), sy + 34 * math.sin(a)) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]])
        sq2 = polys(W, H, [[(sx + 34 * math.cos(a), sy + 34 * math.sin(a)) for a in [k * math.pi / 2 for k in range(4)]]])
        star = np.maximum(sq1, sq2)
        art = over(art, soft_shadow(star, "#3a2a18", blur=2, strength=0.5, dx=2, dy=2))
        art = GP(art, star, COBALT[0], COBALT[2], seed=31, rough=0.6, streak=0.3)
        art = GP(art, circles(W, H, [(sx, sy, 15)]), TURQ[1], TURQ[2], seed=32, rough=0.5)
        art = GP(art, circles(W, H, [(sx, sy, 5)]), "#f3e8d6", seed=33, rough=0.3)
        art = OV(art, gaussian_filter(circles(W, H, [(sx - 12, sy - 14, 8)]), 3) * star * 0.7, lambda m: tint(m, "#ffffff", 0.6))
    art = add_grain(art, 9, 0.02)
    show(art, "bp-arch", bg="#c9a978")
    save_full(art, f"{OUT}/arch.webp", size=(540, 720), quality=76)
    clear()

if "panel" in PARTS:
    # square banna'i panel: concentric stepped diamonds of turquoise and cobalt brick-ends in a buff field
    N, cw, ch = 17, 18, 18
    W = H = N * cw
    c = N // 2

    def pat(i, j):
        d = abs(i - c) + abs(j - c)
        if d % 3 == 0:
            return "c" if (d // 3) % 2 == 0 else "t"
        return None
    cells = lay(N, N, cw, ch, pat)
    art = paint_cells(W, H, cells, seed=13)
    # clip to a diamond-cornered square (an inset tile panel) with a thin cobalt frame
    frame = polys(W, H, [rect(3, 3, W - 3, H - 3)])
    art[..., 3] *= frame
    fr = np.clip(frame - polys(W, H, [rect(10, 10, W - 10, H - 10)]), 0, 1)
    art = GP(art, fr, COBALT[0], COBALT[2], seed=41, rough=0.4)
    show(art, "bp-panel", bg="#f3e8d6")
    save(art, f"{OUT}/panel.webp", max_w=220, quality=82)

if "band" in PARTS:
    cw, ch = 18, 14
    W, H = 792, 5 * ch
    cells = lay(W // cw, 5, cw, ch, lambda i, j: zig(i, j, 5, 8))
    art = paint_cells(W, H, cells, seed=19)
    show(art, "bp-band")
    save_full(art, f"{OUT}/band.webp", quality=80)

if "divider" in PARTS:
    # stepped diamonds in a row, brick-ends only (no field) — reads as a laid ornament on plaster
    cw = 14
    cells = []
    for k in range(-3, 4):
        cx = 26 * k * 1.0
        for (di, dj) in [(0, -2), (-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1), (0, 2)]:
            cells.append((260 + cx + di * cw - cw / 2, 40 + dj * cw - cw / 2, 260 + cx + di * cw + cw / 2, 40 + dj * cw + cw / 2, "t" if k % 2 else "c"))
        if k % 2 == 0:
            cells.append((260 + cx - cw / 2, 40 - cw / 2, 260 + cx + cw / 2, 40 + cw / 2, "b"))
    # keep only every other diamond's ring to avoid overlaps
    W, H = 520, 80
    sel = []
    for k in range(-3, 4):
        cx = 260 + k * 62
        for (di, dj) in [(0, -2), (-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1), (0, 2)]:
            sel.append((cx + di * cw - cw / 2, 40 + dj * cw - cw / 2, cx + di * cw + cw / 2, 40 + dj * cw + cw / 2, "c" if k == 0 else "t"))
        sel.append((cx - cw / 2, 40 - cw / 2, cx + cw / 2, 40 + cw / 2, "b" if k else "t"))
    for k in range(-3, 3):
        x = 260 + k * 62 + 31
        sel.append((x - cw / 2, 40 - cw / 2, x + cw / 2, 40 + cw / 2, "b"))
    art = paint_cells(W, H, sel, seed=23, mortar_mask=np.zeros((H, W), np.float32))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art[..., 3] *= np.clip(1.4 - np.abs(xx - W / 2) / (W / 2) * 1.2, 0, 1)
    show(art, "bp-divider", bg="#f3e8d6")
    save(art, f"{OUT}/divider.webp", max_w=280, quality=84)

if "star" in PARTS:
    W, H = 160, 160
    sx = sy = 80
    sq1 = polys(W, H, [[(sx + 70 * math.cos(a), sy + 70 * math.sin(a)) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]])
    sq2 = polys(W, H, [[(sx + 70 * math.cos(a), sy + 70 * math.sin(a)) for a in [k * math.pi / 2 for k in range(4)]]])
    star = np.maximum(sq1, sq2)
    art = over(blank(W, H), soft_shadow(star, "#3a2a18", blur=3, strength=0.4, dx=3, dy=3))
    art = GP(art, star, COBALT[0], COBALT[2], seed=51, rough=0.8, streak=0.4)
    inner = np.maximum(polys(W, H, [[(sx + 44 * math.cos(a), sy + 44 * math.sin(a)) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]]),
                       polys(W, H, [[(sx + 44 * math.cos(a), sy + 44 * math.sin(a)) for a in [k * math.pi / 2 for k in range(4)]]]))
    art = GP(art, inner, TURQ[1], TURQ[2], seed=52, rough=0.6)
    art = GP(art, circles(W, H, [(sx, sy, 14)]), "#f3e8d6", "#e3d3b8", seed=53, rough=0.4)
    art = OV(art, gaussian_filter(circles(W, H, [(sx - 22, sy - 26, 14)]), 5) * star * 0.7, lambda m: tint(m, "#ffffff", 0.55))
    show(art, "bp-star", bg="#f3e8d6")
    save(art, f"{OUT}/star.webp", max_w=96, quality=84)
