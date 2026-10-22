"""Lengkung Putih — airy modern-syar'i: a corridor of ivory arches receding to a soft light, thin gold inlay lines on
every arch face, gentle taupe shadows in the reveals and arch-shaped light on the stone floor (watercolour glazes on
warm paper + pressed-gold lines). Run: python3 -I lengkung-putih.py [part ...]
parts: lorong arkade lengkung bintang"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g5_lib import *

OUT = outdir("lengkung-putih")
PARTS = sys.argv[1:] or ["lorong", "arkade", "lengkung", "bintang"]
PAPER = "#f7f1e6"
SHADE, SHADE_D = "#d8c9b2", "#bba88c"
WARM = "#e9dcc6"
GOLD = "#c4a062"


def proj(cx, cy, Z, X, Y):
    return cx + X / Z, cy + Y / Z


if "lorong" in PARTS:
    W, H = 780, 1500
    CX, CY = 390, 600
    A, F, HS = 300, 880, 1060          # half width, floor (below eye), jamb height (world units at Z=1)
    D = 0.22                            # slab thickness
    Zs = [1.0, 1.42, 2.0, 2.8, 3.9, 5.4, 7.6, 10.6]
    nx = Seq(51000); rng = random.Random(51)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = np.asarray(paper(W, H, PAPER, seed=5), np.float32) / 255
    art = np.concatenate([art, np.ones((H, W, 1), np.float32)], -1)

    def opening(Z, grow=0.0):
        s = 1 / Z
        return arch_pts(CX, CY + F * s, (A + grow) * s, HS * s, n=36)

    # far light: the end of the corridor glows (paper kept, a warm whisper around it)
    end = poly_fill(W, H, [opening(Zs[-1] + D)])
    art = G(art, gaussian_filter(end, 40) * (1 - end), "#efe2c9", seed=nx(), density=0.3, edge=0.05, bloom=0.5, rough=6, feather=6)
    # floor plane (stone), below the horizon at every depth: we paint it once and let slabs cover it
    floor_m = (yy > CY + F / (Zs[-1] + D)).astype(np.float32)
    depth = np.clip((yy - CY) / (H - CY), 0, 1)
    art = G(art, floor_m * (0.35 + 0.65 * depth), "#e4d6bf", "#dccdb4", seed=nx(), density=0.55, edge=0.05, bloom=0.45, rough=5, feather=2)
    # stone joints converging to the vanishing point
    joints = []
    for k in range(-7, 8):
        x0 = CX + k * 150
        joints.append(([(CX + (x0 - CX) * 0.08, CY + F / 11.5), (x0, H + 20)], 1.2, None))
    for Z in [1.15, 1.7, 2.4, 3.4, 4.6, 6.4, 9.0]:
        y = CY + F / Z
        joints.append(([(CX - 700 / Z, y), (CX + 700 / Z, y)], max(0.6, 1.6 / Z), None))
    jm = strokes(W, H, joints) * floor_m
    art = G(art, jm, "#b9a688", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=1.2, feather=0.5)

    for i in range(len(Zs) - 1, -1, -1):
        Z = Zs[i]
        front = poly_fill(W, H, [opening(Z)])
        back = poly_fill(W, H, [opening(Z + D)])
        floor_y = CY + F / Z
        above = (yy < floor_y + 1).astype(np.float32)
        far = i / (len(Zs) - 1)               # 0 near .. 1 far
        # reveal (inner thickness): left reveal in shade, right reveal catches the light
        rev = np.clip(front - back, 0, 1) * (yy < CY + F / (Z + D) + 1)
        wl = np.clip((CX - xx) / (A / Z * 0.5) + 0.5, 0, 1)
        left = rev * wl
        right = rev * (1 - wl)
        crown = rev * (yy < CY + (F - HS) / Z)
        art = G(art, left, SHADE, SHADE_D, seed=nx(), density=0.75 - far * 0.35, edge=0.45, bloom=0.3, rough=2.0, feather=1.0)
        art = G(art, right, WARM, seed=nx(), density=0.45 - far * 0.2, edge=0.35, bloom=0.4, rough=2.0, feather=1.0)
        art = G(art, crown, SHADE, seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=2, feather=1.2)
        # front face: everything outside the front opening, above this floor line. Paint it as "paper + soft wash",
        # covering what is behind (opaque base first so farther slabs are hidden outside the opening)
        face = (1 - front) * above
        if i < len(Zs) - 1:
            base = np.asarray(paper(W, H, PAPER, seed=7 + i), np.float32) / 255
            fa = np.clip(face, 0, 1)[..., None]
            art[..., :3] = art[..., :3] * (1 - fa) + base * fa
        # near faces sit in gentle shadow, far ones are lit
        tone = gaussian_filter(front, 60 / Z)  # lighter close to the opening (light spills out)
        fwash = face * (0.55 - far * 0.45) * (1 - 0.6 * np.clip(tone * 1.6, 0, 1))
        art = G(art, fwash, "#e6d9c4", "#dfd0b8", seed=nx(), density=0.6, edge=0.15, bloom=0.5, rough=4, feather=2)
        # soft cast shadow of this slab on the floor in front of it (light comes from the far end)
        sh_y0 = floor_y
        sh = np.clip(1 - (yy - sh_y0) / (90 / Z), 0, 1) * (yy > sh_y0) * (np.abs(xx - CX) < (A + 120) / Z) * (1 - poly_fill(W, H, [arch_pts(CX, floor_y + 200 / Z, A / Z * 0.92, HS / Z * 0.0 + 1, 24)]) * 0)
        lightpool = poly_fill(W, H, [[(CX - A / Z * 0.9, floor_y + 2), (CX + A / Z * 0.9, floor_y + 2), (CX + A / Z * 1.25, floor_y + 180 / Z), (CX - A / Z * 1.25, floor_y + 180 / Z)]])
        art = G(art, sh * (1 - lightpool * 0.7) * 0.8, SHADE, seed=nx(), density=0.4, edge=0.05, bloom=0.3, rough=4, feather=3)
        # thin gold inlay: an arch line on the face, a little outside the opening, and a fine inner bead
        g1 = poly_stroke(W, H, [opening(Z, grow=26)], max(1.0, 3.6 / Z)) * above
        g2 = poly_stroke(W, H, [opening(Z, grow=40)], max(0.6, 1.4 / Z)) * above
        art = FO(art, g1, GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
        art = G(art, g2, "#b89458", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.3)
        # crisp edge where face meets reveal (slight darker line, like a pencil under-drawing)
        edge = np.clip(gaussian_filter(front, 0.8) - front * 0.0, 0, 1)
        edge = np.clip(edge * (1 - gaussian_filter(front, 0.8) > 0.5) + 0, 0, 1) * 0
        clear()
    # light from the end: lift the centre a little (bloom of light down the corridor)
    halo = gaussian_filter(poly_fill(W, H, [opening(4.0)]), 50)
    art = lighten(art, halo, "#fffaf0", 0.35)
    art[..., :3] = np.clip(art[..., :3], 0, 1)
    art = add_grain(art, 5, 0.02)
    preview(art, "lp-lorong", bg="#ffffff")
    save_rgb(art, f"{OUT}/lorong.webp", size=(600, 1154), quality=76)
    clear()

if "arkade" in PARTS:
    # frontal arcade elevation: five slender round arches on columns, ivory with taupe shadow inside, gold inlay lines
    W, H = 900, 380
    nx = Seq(52000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    wall = poly_fill(W, H, [[(10, 40), (W - 10, 40), (W - 10, H - 20), (10, H - 20)]])
    ops = [arch_pts(110 + k * 170, H - 20, 62, 170, 30) for k in range(5)]
    om = poly_fill(W, H, ops)
    # wall: very pale ivory wash that fades out at the top (dissolves into the page)
    fade = np.clip((yy - 30) / 120, 0, 1)
    art = G(art, wall * (1 - om) * fade, "#f2ead9", "#efe4cf", seed=nx(), density=0.85, edge=0.25, bloom=0.4, rough=3, feather=1.2)
    # openings: shadow deepest at the crown/left, lighter toward the floor (light from the right, beyond)
    for k, pts in enumerate(ops):
        m = poly_fill(W, H, [pts])
        cx = 110 + k * 170
        g = np.clip(1 - (yy - 60) / 300, 0.25, 1) * (0.7 + 0.3 * np.clip((cx - xx) / 60 + 0.5, 0, 1))
        art = G(art, m * g, "#d9c8ad", "#cdb999", seed=nx(), density=0.7, edge=0.5, bloom=0.4, rough=2.2, feather=1.0)
        # inner reveal on the left jamb
        rev = poly_fill(W, H, [arch_pts(cx, H - 20, 62, 170, 30)]) - poly_fill(W, H, [arch_pts(cx + 10, H - 20, 54, 166, 30)])
        art = G(art, np.clip(rev, 0, 1), "#bfa985", seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=1.5, feather=0.8)
    lines = poly_stroke(W, H, [arch_pts(110 + k * 170, H - 20, 76, 170, 30) for k in range(5)], 3.0)
    lines2 = poly_stroke(W, H, [arch_pts(110 + k * 170, H - 20, 84, 170, 30) for k in range(5)], 1.2)
    cornice = poly_stroke(W, H, [[(10, 44), (W - 10, 44)], [(10, 54), (W - 10, 54)]], 1.6)
    art = FO(art, lines * (yy > 40), GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
    art = G(art, np.maximum(lines2, cornice * 0.8) * (yy > 40), "#b38f55", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.3)
    # floor line
    art = G(art, poly_fill(W, H, [[(0, H - 22), (W, H - 22), (W, H - 6), (0, H - 6)]]), "#e1d3bb", seed=nx(), density=0.6, edge=0.3, bloom=0.3, rough=2)
    preview(art, "lp-arkade")
    save(art, f"{OUT}/arkade.webp", max_w=640, quality=82)
    clear()

if "lengkung" in PARTS:
    # divider: a small double gold arch over a hairline, a tiny rosette at the crown
    W, H = 520, 150
    nx = Seq(53000)
    art = blank(W, H)
    a1 = poly_stroke(W, H, [arch_pts(260, 128, 54, 30, 36)], 3.0)
    a2 = poly_stroke(W, H, [arch_pts(260, 128, 42, 24, 36)], 1.4)
    base = poly_stroke(W, H, [[(40, 128), (480, 128)]], 1.6)
    dots = circles(W, H, [(30, 128, 3.2), (490, 128, 3.2), (160, 128, 2.2), (360, 128, 2.2)])
    ros = []
    for k in range(8):
        a = k * math.pi / 4
        ros.append(petal_pts(260 + math.cos(a) * 2, 30 + math.sin(a) * 2, 13, 6, a, n=10))
    rm = shapes(W, H, ros)
    art = FO(art, np.maximum(np.maximum(a1, rm), dots), GOLD, seed=nx(), emboss=0.5, sparkle=0.15)
    art = G(art, np.maximum(a2, base), "#b38f55", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.4, feather=0.3)
    preview(art, "lp-lengkung")
    save(art, f"{OUT}/lengkung.webp", max_w=260, quality=86)
    clear()

if "bintang" in PARTS:
    # eight-point star rosette (two squares) in pressed gold with an ivory centre, for nodes and emblems
    W = H = 240
    nx = Seq(54000)
    art = blank(W, H)
    def sq(r, rot):
        return [(120 + math.cos(rot + k * math.pi / 2) * r, 120 + math.sin(rot + k * math.pi / 2) * r) for k in range(4)]
    star = poly_fill(W, H, [sq(96, 0), sq(96, math.pi / 4)])
    inner = poly_fill(W, H, [sq(80, 0), sq(80, math.pi / 4)])
    art = FO(art, np.clip(star - inner, 0, 1), GOLD, seed=nx(), emboss=0.6, sparkle=0.15)
    art = G(art, inner, "#f3ead8", "#ead9bd", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=1.5, feather=0.6)
    petals = shapes(W, H, [petal_pts(120, 120, 46, 15, k * math.pi / 4, n=12) for k in range(8)])
    art = FO(art, np.clip(petals - circles(W, H, [(120, 120, 10)]), 0, 1) * 0.0 + poly_stroke(W, H, [petal_pts(120, 120, 46, 15, k * math.pi / 4, n=12) + [petal_pts(120, 120, 46, 15, k * math.pi / 4, n=12)[0]] for k in range(8)], 2.0), GOLD, seed=nx(), emboss=0.4)
    art = FO(art, circles(W, H, [(120, 120, 8)]), GOLD, seed=nx())
    preview(art, "lp-bintang")
    save(art, f"{OUT}/bintang.webp", max_w=120, quality=86)
    clear()
