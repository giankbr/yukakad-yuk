"""Kilim Anatolia — flat-woven slit-tapestry kilim (weft-faced wool): brick red / indigo / saffron / cream with dark
walnut-brown outlines. Purely geometric: stepped diamonds (gul), sawtooth rims, stepped crosses, chevron borders.
Run: python3 -I kilim-anatolia.py [part ...]   parts: field plain border fringe frame gul divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d3_lib import *  # noqa

OUT = outdir("kilim-anatolia")
PARTS = sys.argv[1:] or ["field", "plain", "border", "fringe", "frame", "gul", "divider"]
CREAM, BRICK, INDIGO, SAFF, BROWN, MADDER = "#ece0c3", "#a23a24", "#2a3263", "#d69a2c", "#3b2219", "#c8664a"
PAL = [CREAM, BRICK, INDIGO, SAFF, BROWN, MADDER]
CR, BR, IN, SA, BW, MD = range(6)


def dist(gh, gw, cy, cx, r, ry, wrap=True, h0=0.0):
    ii, jj = np.mgrid[0:gh, 0:gw].astype(np.float32)
    dx = jj - cx; dy = ii - cy
    if wrap:
        dx = (dx + gw / 2) % gw - gw / 2
        dy = (dy + gh / 2) % gh - gh / 2
    return np.abs(dx) / r + np.maximum(0, np.abs(dy) - h0) / ry, ii, jj


def gul(D, cy, cx, r, ry, wrap=True, outer=IN, ground=BR, h0=0.0):
    gh, gw = D.shape
    d, ii, jj = dist(gh, gw, cy, cx, r, ry, wrap, h0)
    teeth = (d > 1.0) & (d < 1.0 + 2.6 / r) & (((ii // 3) % 2) == 0)
    D[teeth] = outer
    D[d <= 1.0] = outer
    D[(d > 0.80) & (d <= 0.88)] = CR
    D[d <= 0.62] = ground
    D[(d > 0.44) & (d <= 0.52)] = SA
    D[(d > 0.22) & (d <= 0.30)] = CR
    D[d <= 0.18] = BW
    # stepped cross in the core
    D[(d <= 0.12) & ((np.abs(jj - cx) < 1.5) | (np.abs(ii - cy) < 2.5))] = SA
    return d


def cross(D, cy, cx, s, col, wrap=True):
    gh, gw = D.shape
    ii, jj = np.mgrid[0:gh, 0:gw]
    dx = jj - cx; dy = ii - cy
    if wrap:
        dx = (dx + gw // 2) % gw - gw // 2
        dy = (dy + gh // 2) % gh - gh // 2
    m = ((np.abs(dx) <= s) & (np.abs(dy) <= 1.5 * s / 3)) | ((np.abs(dx) <= s / 3) & (np.abs(dy) <= 1.5 * s))
    D[m] = col
    D[(np.abs(dx) <= 0) & (np.abs(dy) <= 0)] = CR


if "field" in PARTS:
    # tileable field: brick ground, indigo guls on a half-drop lattice, saffron stepped crosses between
    gw, gh = 56, 120
    D = np.full((gh, gw), BR)
    gul(D, 0, 0, 20, 34)
    gul(D, gh / 2, gw / 2, 20, 34, outer=IN, ground=MD)
    cross(D, 0, gw // 2, 4, SA)
    cross(D, gh // 2, 0, 4, CR)
    # thin brown outline wherever indigo meets brick ground (as woven kilims do with a dark contour)
    art = kilim(D, PAL, cw=6, rh=4, seed=7101)
    preview(art, "ka-field")
    save_full(art, f"{OUT}/field.webp", quality=78)
    clear()

if "plain" in PARTS:
    # plain-weave cream panel (abrash only) for cards, and an indigo panel for bands
    for name, colr, sd in [("cream", CR, 7201), ("indigo", IN, 7202)]:
        gw, gh = 40, 64
        D = np.full((gh, gw), 0)
        pal = [PAL[colr]]
        art = kilim(D, pal, cw=6, rh=4, seed=sd, abrash=0.035)
        preview(art, f"ka-{name}")
        save_full(art, f"{OUT}/{name}.webp", quality=74)
    clear()

if "border" in PARTS:
    # repeat-x border band: brown edge stripes, sawtooth triangles (brick / indigo alternating) on cream,
    # saffron stepped diamonds riding the centre line
    gw, gh = 40, 34
    D = np.full((gh, gw), CR)
    D[0:2] = BW; D[gh - 2:] = BW
    D[2:3] = SA; D[gh - 3:gh - 2] = SA
    ii, jj = np.mgrid[0:gh, 0:gw]
    mid = gh / 2
    # triangles pointing up from the bottom and down from the top, offset by half a period
    for k in range(2):
        x0 = k * 20
        col = BR if k == 0 else IN
        up = (np.abs(((jj - x0 - 10) + gw / 2) % gw - gw / 2) * 1.1 <= (gh - 3 - ii)) & (ii >= mid) & (ii < gh - 3)
        D[up] = col
        dn = (np.abs(((jj - x0) + gw / 2) % gw - gw / 2) * 1.1 <= (ii - 3)) & (ii < mid) & (ii >= 3)
        D[dn] = IN if k == 0 else BR
    # centre stepped diamonds in saffron with brown core
    for x0 in (5, 15, 25, 35):
        d, _, _ = dist(gh, gw, mid - 0.5, x0, 3.2, 4.5)
        D[d <= 1] = SA
        D[d <= 0.35] = BW
    art = kilim(D, PAL, cw=6, rh=4, seed=7301)
    preview(art, "ka-border")
    save_full(art, f"{OUT}/border.webp", quality=80)
    clear()

if "fringe" in PARTS:
    art = fringe(240, 80, pitch=6, seed=7401, col="#efe5cc", knot_every=5)
    preview(art, "ka-fringe", bg=BRICK)
    save_full(art, f"{OUT}/fringe.webp", size=(160, 53), quality=82)
    clear()

if "frame" in PARTS:
    # stepped hexagonal lozenge frame for the photo window; transparent inside and out
    gw, gh = 81, 141
    D = np.full((gh, gw), -1)
    cx, cy = 40, 70
    r, ry, h0 = 40, 40, 30
    d, ii, jj = dist(gh, gw, cy, cx, r, ry, wrap=False, h0=h0)
    teeth = (d > 1.0) & (d < 1.07) & (((ii // 3) % 2) == 0)
    D[teeth] = BR
    D[d <= 1.0] = BW
    D[d <= 0.975] = IN
    D[(d > 0.90) & (d <= 0.94) & (((ii // 3) % 3) == 0)] = SA
    D[(d > 0.84) & (d <= 0.88)] = CR
    D[(d > 0.80) & (d <= 0.84)] = BR
    D[d <= 0.80] = -1
    # finials: stepped crosses above and below the points
    for fy in (cy - h0 - 40 + 2, cy + h0 + 40 - 2):
        pass
    art = kilim(D, PAL, cw=6, rh=4, seed=7501, tile=False)
    preview(art, "ka-frame", bg="#e7d6b4")
    sz = save(art, f"{OUT}/frame.webp", max_w=480, quality=80)
    # print the photo-window clip polygon (percent of frame bbox) for CSS: inner hexagon at d = 0.84
    k = 0.815
    W_, H_ = gw * 6, gh * 4
    pts = [(cx, cy - h0 - ry * k), (cx + r * k, cy - h0), (cx + r * k, cy + h0), (cx, cy + h0 + ry * k), (cx - r * k, cy + h0), (cx - r * k, cy - h0)]
    print("clip:", ", ".join(f"{(x + 0.5) * 6 / W_ * 100:.1f}% {(y + 0.5) * 4 / H_ * 100:.1f}%" for x, y in pts))
    clear()

if "gul" in PARTS:
    # a large woven gul medallion patch (transparent outside its sawtooth rim) for hero / closing emblem
    gw, gh = 61, 95
    D = np.full((gh, gw), -1)
    cx, cy = 30, 47
    d, ii, jj = dist(gh, gw, cy, cx, 27, 42, wrap=False)
    D[d <= 1.0] = BR
    gul(D, cy, cx, 27, 42, wrap=False, outer=IN, ground=BR)
    # inner field: madder diamond ring and saffron hooks at four points
    for (py, px) in [(cy - 21, cx), (cy + 21, cx), (cy, cx - 13.5), (cy, cx + 13.5)]:
        d2, _, _ = dist(gh, gw, py, px, 3, 4.5, wrap=False)
        D[d2 <= 1] = CR
        D[d2 <= 0.4] = IN
    art = kilim(D, PAL, cw=6, rh=4, seed=7601, tile=False)
    preview(art, "ka-gul", bg="#efe3c8")
    save(art, f"{OUT}/gul.webp", max_w=366, quality=82)
    clear()

if "divider" in PARTS:
    gw, gh = 57, 19
    D = np.full((gh, gw), -1)
    cy = 9
    for cx, r, col in [(28, 8, IN), (13, 5, BR), (43, 5, BR), (3, 2.6, SA), (53, 2.6, SA)]:
        d, _, _ = dist(gh, gw, cy, cx, r, r * 1.15, wrap=False)
        D[d <= 1] = col
        if r > 4:
            D[(d > 0.45) & (d <= 0.62)] = CR
            D[d <= 0.3] = SA if col == IN else BW
    D[cy, :][D[cy, :] < 0] = BW
    D[cy - 1, :][D[cy - 1, :] < 0] = BW
    art = kilim(D, PAL, cw=6, rh=4, seed=7701, tile=False)
    preview(art, "ka-divider", bg="#efe3c8")
    save(art, f"{OUT}/divider.webp", max_w=200, quality=86)
    clear()

kb(OUT)
