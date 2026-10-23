"""Ultah Balok — a kids' birthday in a toy-block town, picture-book gouache: plain painted wooden building blocks (cubes,
long bricks, triangle roofs, arches, cylinders, half-moons; generic toys, no brand studs or logos), blank letter cubes in
four colours (the child's name is set in HTML on their faces), a little block city on a wooden floor with block trees and
bunting, a stacked tower, a block-row divider.
Run: python3 -I ultah-balok.py [part ...]   parts: cubes city tower divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o5_lib import *

OUT = outdir("ultah-balok")
PARTS = sys.argv[1:] or ["cubes", "city", "tower", "divider"]
COLS = {
    "r": ("#e2412f", "#f0624a", "#b02e20"),
    "y": ("#f6b928", "#ffd04f", "#c98e12"),
    "b": ("#2f6fd0", "#4d8be6", "#1f4f9e"),
    "g": ("#3aa25a", "#56bd72", "#277a40"),
}
WOODF, WOODL, WOODD = "#f1d6a4", "#f8e6c2", "#c99a5c"
INK = "#2a2a3a"
D = 0.32  # oblique depth ratio


def faces(x, y, w, h, d):
    """Oblique box: front rect at (x,y) w*h, depth d up-right. Returns (front, top, side) point lists."""
    front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    top = [(x, y), (x + d, y - d * 0.8), (x + w + d, y - d * 0.8), (x + w, y)]
    side = [(x + w, y), (x + w + d, y - d * 0.8), (x + w + d, y + h - d * 0.8), (x + w, y + h)]
    return front, top, side


def box_on(art, Wd, Hd, x, y, w, h, key, nx, d=None, front_col=None, inset=False, grain=True):
    base, light, dark = COLS[key] if key in COLS else (key, mix(key, "#ffffff", 0.2), mix(key, "#000000", 0.25))
    d = d if d is not None else min(w, h) * D
    fr, tp, sd = faces(x, y, w, h, d)
    fm = shapes(Wd, Hd, [fr], smooth=False); tm = shapes(Wd, Hd, [tp], smooth=False); sm = shapes(Wd, Hd, [sd], smooth=False)
    art = P(art, tm, light, mix(light, "#ffffff", 0.15), seed=nx(), rough=0.7)
    art = P(art, sm, dark, base, seed=nx(), rough=0.7)
    art = P(art, fm, front_col or base, mix(front_col or base, "#ffffff", 0.12), seed=nx(), rough=0.7)
    if inset:
        b = max(4, w * 0.11)
        inner = shapes(Wd, Hd, [[(x + b, y + b), (x + w - b, y + b), (x + w - b, y + h - b), (x + b, y + h - b)]], smooth=False)
        art = P(art, inner, WOODF, WOODL, seed=nx(), rough=0.6)
        art = tint(art, np.clip(inner - np.roll(np.roll(inner, 3, 0), 3, 1), 0, 1), "#7a5a30", 0.35)
        # wood grain on the panel
        if grain:
            gl = strokes(Wd, Hd, [(curve([(x + b, y + b + k * (h - 2 * b) / 7 + 3), (x + w / 2, y + b + k * (h - 2 * b) / 7 + 6), (x + w - b, y + b + k * (h - 2 * b) / 7 + 2)], 10), 1.2, None) for k in range(1, 7)]) * inner
            art = tint(art, gl, WOODD, 0.35)
    art = tint(art, np.clip(edge_ring(fm, 1.2) + edge_ring(tm, 1.0) + edge_ring(sm, 1.0), 0, 1), mix(dark, INK, 0.4), 0.6)
    # rounded-edge highlight along the front top edge
    art = tint(art, strokes(Wd, Hd, [([(x + 3, y + 2), (x + w - 3, y + 2)], 2.2, None)]), "#ffffff", 0.35)
    return art


def roof_on(art, Wd, Hd, x, y, w, h, key, nx, d=None):
    base, light, dark = COLS[key]
    d = d if d is not None else w * D * 0.8
    front = [(x, y + h), (x + w / 2, y), (x + w, y + h)]
    side = [(x + w / 2, y), (x + w / 2 + d, y - d * 0.8), (x + w + d, y + h - d * 0.8), (x + w, y + h)]
    sm = shapes(Wd, Hd, [side], smooth=False); fm = shapes(Wd, Hd, [front], smooth=False)
    art = P(art, sm, dark, base, seed=nx(), rough=0.7)
    art = P(art, fm, base, light, seed=nx(), rough=0.7)
    art = tint(art, np.clip(edge_ring(fm, 1.2) + edge_ring(sm, 1.0), 0, 1), mix(dark, INK, 0.4), 0.6)
    return art


def cyl_on(art, Wd, Hd, x, y, w, h, key, nx):
    base, light, dark = COLS[key]
    ry = w * 0.18
    body = shapes(Wd, Hd, [[(x, y)] + [(x + w / 2 + math.cos(a) * w / 2, y + h + math.sin(a) * ry) for a in np.linspace(math.pi, 0, 20)][::-1][::-1] + [(x + w, y)]], smooth=False)
    body = np.maximum(body, shapes(Wd, Hd, [[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], smooth=False))
    body = np.maximum(body, shapes(Wd, Hd, [ellipse_pts(x + w / 2, y + h, w / 2, ry, 20)]))
    art = P(art, body, base, light, seed=nx(), rough=0.7)
    art = tint(art, body * right_of(Wd, x + w * 0.62, w * 0.3), dark, 0.55)
    art = tint(art, body * (1 - right_of(Wd, x + w * 0.22, w * 0.12)) * right_of(Wd, x + w * 0.08, 4), "#ffffff", 0.3)
    top = shapes(Wd, Hd, [ellipse_pts(x + w / 2, y, w / 2, ry, 20)])
    art = P(art, top, light, mix(light, "#ffffff", 0.2), seed=nx(), rough=0.6)
    art = tint(art, np.clip(edge_ring(body, 1.2) + edge_ring(top, 1.0), 0, 1), mix(dark, INK, 0.4), 0.6)
    return art


def arch_on(art, Wd, Hd, x, y, w, h, key, nx):
    """Bridge block: a long brick with a half-round cut-out underneath."""
    base, light, dark = COLS[key]
    d = h * D * 0.9
    r = min(w * 0.3, h * 0.72)
    fr, tp, sd = faces(x, y, w, h, d)
    cut = circles(Wd, Hd, [(x + w / 2, y + h, r)])
    fm = np.clip(shapes(Wd, Hd, [fr], smooth=False) - cut, 0, 1)
    art = P(art, shapes(Wd, Hd, [tp], smooth=False), light, seed=nx(), rough=0.7)
    art = P(art, shapes(Wd, Hd, [sd], smooth=False), dark, seed=nx(), rough=0.7)
    art = P(art, fm, base, light, seed=nx(), rough=0.7)
    inner = np.clip(circles(Wd, Hd, [(x + w / 2, y + h, r)]) - circles(Wd, Hd, [(x + w / 2 - d * 0.35, y + h + d * 0.25, r)]), 0, 1) * shapes(Wd, Hd, [fr], smooth=False)
    art = tint(art, inner, dark, 0.8)
    art = tint(art, edge_ring(fm, 1.2), mix(dark, INK, 0.4), 0.6)
    return art


def tree_on(art, Wd, Hd, x, by, s, nx):
    art = P(art, rect(Wd, Hd, x - s * 0.08, by - s * 0.5, x + s * 0.08, by), "#a8754a", seed=nx(), rough=0.4)
    ball = circles(Wd, Hd, [(x, by - s * 0.78, s * 0.36)])
    art = P(art, ball, "#3aa25a", "#56bd72", seed=nx(), rough=0.6)
    art = tint(art, ball * right_of(Wd, x + s * 0.05, s * 0.3), "#277a40", 0.5)
    art = tint(art, circles(Wd, Hd, [(x - s * 0.13, by - s * 0.92, s * 0.08)]), "#ffffff", 0.45)
    art = tint(art, edge_ring(ball, 1.2), "#1f5a30", 0.6)
    return art


def cubes():
    for k, key in enumerate("rybg"):
        S = 200
        nx = Seq(100 + k * 50)
        art = blank(S, S)
        art = box_on(art, S, S, 16, 58, 124, 124, key, nx, d=44, inset=True)
        save_full(art, f"{OUT}/cube-{key}.webp", size=(140, 140), quality=84)
        if k == 0:
            preview(art, "ub-cube")


def city():
    Wd, Hd = 820, 470
    nx = Seq(300); rng = random.Random(4)
    art = blank(Wd, Hd)
    # wooden floor (playroom), planks
    floor = rect(Wd, Hd, 0, 360, Wd, Hd)
    art = P(art, floor, "#e2b77e", "#d6a86c", seed=nx(), rough=0.4, streak=1.6)
    art = tint(art, strokes(Wd, Hd, [([(-10, y), (Wd + 10, y)], 1.8, None) for y in (392, 428, 462)]), "#b5844e", 0.6)
    art = tint(art, strokes(Wd, Hd, [([(x, y0), (x, y0 + 34)], 1.6, None) for x, y0 in ((120, 394), (420, 394), (690, 394), (260, 430), (560, 430), (40, 430), (760, 430))]), "#b5844e", 0.55)
    art = tint(art, floor * above(Hd, 376, 14), "#a8754a", 0.25)
    # bunting string across the back
    bunt = curve([(-10, 36), (200, 86), (410, 52), (620, 90), (830, 40)], 80)
    art = P(art, strokes(Wd, Hd, [(bunt, 2.2, None)]), "#7a6a5a", seed=nx(), rough=0.3)
    flags = []
    for i, (x, y, a) in enumerate(along(bunt, 46)):
        flags.append(([(x - 14, y), (x + 14, y + 2), (x + 1, y + 30)], "rybg"[i % 4]))
    for pts, key in flags:
        art = P(art, shapes(Wd, Hd, [pts], smooth=False), COLS[key][0], COLS[key][1], seed=nx(), rough=0.5)
    clear()
    # buildings, back to front (base line y=380)
    B = 380
    art = box_on(art, Wd, Hd, 40, B - 150, 90, 150, "b", nx, d=24)
    art = roof_on(art, Wd, Hd, 40, B - 222, 90, 72, "r", nx, d=24)
    # windows on blue tower
    for wy in (B - 130, B - 84):
        art = P(art, rect(Wd, Hd, 58, wy, 80, wy + 24), "#fff4d6", seed=nx(), rough=0.3)
        art = P(art, rect(Wd, Hd, 92, wy, 114, wy + 24), "#fff4d6", seed=nx(), rough=0.3)
    art = cyl_on(art, Wd, Hd, 160, B - 200, 56, 200, "y", nx)
    art = box_on(art, Wd, Hd, 150, B - 236, 76, 36, "g", nx, d=20)
    art = cyl_on(art, Wd, Hd, 176, B - 274, 26, 38, "r", nx)
    # arch bridge with a tower on top
    art = box_on(art, Wd, Hd, 250, B - 120, 60, 120, "r", nx, d=22)
    art = box_on(art, Wd, Hd, 420, B - 120, 60, 120, "r", nx, d=22)
    art = arch_on(art, Wd, Hd, 250, B - 172, 230, 52, "y", nx)
    art = box_on(art, Wd, Hd, 320, B - 262, 90, 90, "g", nx, d=26, inset=True)
    art = roof_on(art, Wd, Hd, 320, B - 330, 90, 68, "b", nx, d=26)
    # flag on top of the green tower
    art = P(art, rect(Wd, Hd, 364, B - 380, 368, B - 330), "#6a5a4a", seed=nx(), rough=0.2)
    art = P(art, shapes(Wd, Hd, [[(368, B - 380), (404, B - 370), (368, B - 360)]], smooth=False), COLS["r"][0], seed=nx(), rough=0.3)
    clear()
    # right side: stepped building + half-moon + a long brick
    art = box_on(art, Wd, Hd, 520, B - 90, 120, 90, "b", nx, d=26)
    art = box_on(art, Wd, Hd, 540, B - 170, 80, 80, "y", nx, d=22, inset=True)
    art = cyl_on(art, Wd, Hd, 556, B - 230, 48, 60, "g", nx)
    art = box_on(art, Wd, Hd, 670, B - 210, 70, 210, "r", nx, d=22)
    for wy in range(int(B - 190), int(B - 30), 44):
        art = P(art, rect(Wd, Hd, 686, wy, 724, wy + 22), "#fff4d6", seed=nx(), rough=0.3)
    art = roof_on(art, Wd, Hd, 670, B - 268, 70, 58, "y", nx, d=22)
    # trees
    for x, s in ((232, 90), (500, 80), (770, 96), (20, 70)):
        art = tree_on(art, Wd, Hd, x, B + 4, s, nx)
    clear()
    # loose blocks scattered on the floor (front)
    art = box_on(art, Wd, Hd, 90, 410, 46, 46, "y", nx, d=16)
    art = roof_on(art, Wd, Hd, 610, 412, 56, 44, "g", nx, d=16)
    art = cyl_on(art, Wd, Hd, 470, 404, 30, 46, "b", nx)
    art = box_on(art, Wd, Hd, 300, 420, 90, 32, "r", nx, d=14)
    # contact shadows
    sh = rect(Wd, Hd, 20, B - 2, Wd - 20, B + 8)
    art = over(tint(blank(Wd, Hd), sh, "#7a5232", 0.18, blur=4), art)
    art = add_grain(art, 7, 0.03)
    save(art, f"{OUT}/city.webp", max_w=780, quality=78)
    preview(art, "ub-city")


def tower():
    Wd, Hd = 260, 440
    nx = Seq(500)
    art = blank(Wd, Hd)
    art = box_on(art, Wd, Hd, 40, 340, 150, 60, "b", nx, d=30)
    art = box_on(art, Wd, Hd, 70, 250, 90, 90, "r", nx, d=26, inset=True)
    art = cyl_on(art, Wd, Hd, 86, 170, 58, 80, "y", nx)
    art = box_on(art, Wd, Hd, 66, 130, 98, 40, "g", nx, d=22)
    art = roof_on(art, Wd, Hd, 72, 60, 86, 70, "r", nx, d=22)
    save(art, f"{OUT}/tower.webp", max_w=200, quality=82)
    preview(art, "ub-tower")


def divider():
    Wd, Hd = 520, 110
    nx = Seq(600)
    art = blank(Wd, Hd)
    B = 96
    art = box_on(art, Wd, Hd, 40, B - 40, 40, 40, "r", nx, d=12)
    art = cyl_on(art, Wd, Hd, 110, B - 52, 30, 46, "y", nx)
    art = roof_on(art, Wd, Hd, 168, B - 42, 48, 42, "g", nx, d=12)
    art = box_on(art, Wd, Hd, 236, B - 48, 48, 48, "b", nx, d=14, inset=True)
    art = arch_on(art, Wd, Hd, 306, B - 34, 90, 34, "r", nx)
    art = box_on(art, Wd, Hd, 420, B - 40, 40, 40, "y", nx, d=12)
    save(art, f"{OUT}/divider.webp", max_w=330, quality=84)
    preview(art, "ub-divider")


for p in PARTS:
    globals()[p]()
    clear()
