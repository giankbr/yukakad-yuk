"""Tatreez Merah — Palestinian-style tatreez cross-stitch, rendered stitch by stitch (two thread legs per cell, floss
twist, drop shadow into the linen) in deep red with black/green accents on ivory even-weave linen. Geometry and flora
only: eight-point stars, cypress trees, sawtooth borders, carnation rosettes. Run: python3 -I tatreez-merah.py [part ...]
parts: linen band panel star cypress rose. Assets -> public/themes/art/tatreez-merah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m2_lib import *

OUT = outdir("tatreez-merah")
PARTS = sys.argv[1:] or ["linen", "band", "panel", "star", "cypress", "rose"]
LINEN = "#eee4cf"
PAL = {"R": "#9b1c24", "D": "#5c0e15", "K": "#221c1b", "G": "#2c5a3e", "O": "#b9822e", "P": "#c8414a"}
CELL = 10


class Grid:
    def __init__(self, cols, rows):
        self.g = [["." for _ in range(cols)] for _ in range(rows)]
        self.cols, self.rows = cols, rows

    def put(self, c, r, ch):
        if 0 <= c < self.cols and 0 <= r < self.rows:
            self.g[r][c] = ch

    def stamp(self, rows, c0, r0):
        for r, line in enumerate(rows):
            for c, ch in enumerate(line):
                if ch != ".":
                    self.put(c0 + c, r0 + r, ch)

    def lines(self):
        return ["".join(r) for r in self.g]


def _in_star(x, y, R, ri, pts=8, rot=0.0):
    ang = math.atan2(y, x) - rot
    r = math.hypot(x, y)
    seg = 2 * math.pi / pts
    t = (ang % seg) / seg  # 0..1 across one point
    k = abs(t - 0.5) * 2   # 1 at tips (t=0/1), 0 between
    lim = ri + (R - ri) * (k ** 1.0)
    # straight edges between tip and valley
    return r <= lim


def star_rows(n, fill="R", edge="D", core="K", centre="O"):
    """Eight-point star as a stitched polygon (tips on axes and diagonals), outlined, with an inner star ring and a
    centre lozenge."""
    s = 2 * n + 1
    R, ri = n + 0.45, n * 0.56
    ins = lambda c, r: _in_star(c - n, r - n, R, ri)
    inner = lambda c, r: _in_star(c - n, r - n, R * 0.5, ri * 0.5)
    rows = []
    for r in range(s):
        line = ""
        for c in range(s):
            if not ins(c, r):
                line += "."; continue
            if any(not ins(c + ex, r + ey) for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                line += edge
            elif abs(c - n) + abs(r - n) <= 1:
                line += centre
            elif inner(c, r):
                line += core if any(not inner(c + ex, r + ey) for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1))) else ("O" if abs(c - n) + abs(r - n) <= 2 else ".")
            else:
                line += fill
        rows.append(line)
    return rows


def cypress_rows(h, tiers=None):
    """Slender cypress (saru): black stem, red branch chevrons rising from it, green tips, small pot."""
    hw = max(3, h // 6)
    w = 2 * hw + 1
    cx = hw
    rows = []
    body = h - 4
    for r in range(h):
        line = ["."] * w
        if r < body:
            half = int(round(hw * min(1, (r + 2) / body)))
            for dx in range(-half, half + 1):
                ax = abs(dx)
                if ax == 0:
                    continue
                if ax == half:
                    line[cx + dx] = "G" if (r % 2 == 0) else "D"
                else:
                    line[cx + dx] = "D" if (r - ax) % 3 == 0 else "R"
            line[cx] = "K"
            if r == 0:
                line[cx] = "D"
        elif r < h - 2:
            line[cx] = "K"
        else:
            for dx in range(-2 - (r - h + 2), 3 + (r - h + 2)):
                if 0 <= cx + dx < w:
                    line[cx + dx] = "D" if r == h - 1 else "R"
        rows.append("".join(line))
    return rows


def rose_rows(n=7):
    """Carnation rosette: four petals on the axes, four leaves on the diagonals, ring core."""
    s = 2 * n + 1
    rows = []
    for r in range(s):
        line = ""
        for c in range(s):
            dx, dy = c - n, r - n
            ax, ay = abs(dx), abs(dy)
            ch = "."
            if ax + ay <= 2:
                ch = "O" if ax + ay == 0 else "K"
            elif (ax <= 1 and 2 < ay <= n) or (ay <= 1 and 2 < ax <= n):
                ch = "R" if max(ax, ay) < n else "D"
                if max(ax, ay) in (n - 1, n) and min(ax, ay) == 1:
                    ch = "D"
            elif ax == ay and 2 <= ax <= n - 2:
                ch = "G"
            elif abs(ax - ay) == 1 and 3 <= max(ax, ay) <= n - 2:
                ch = "G" if (ax + ay) % 3 else "."
            line += ch
        rows.append(line)
    return rows


def render(lines, name, pad=1, preview_bg=LINEN, seed=1, cell=CELL):
    cols = max(len(l) for l in lines); rows = len(lines)
    W, H = (cols + 2 * pad) * cell, (rows + 2 * pad) * cell
    cells = parse_grid(lines, PAL)
    art = stitch_layer(W, H, cells, cell, pad * cell, pad * cell, seed=seed)
    prev(opaque(art, preview_bg) if preview_bg else art, name, bg=preview_bg or "#eee4cf")
    return art


if "linen" in PARTS:
    W = H = 240
    rgb = linen(W, H, LINEN, seed=3, pitch=2.4)
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    prev(arr, "tz-linen", bg="#000000")
    save_full(arr, f"{OUT}/linen.webp", quality=74)

if "band" in PARTS:
    # seamless horizontal border, period 16 cells: sawtooth edges, chain of small stars, running diamond in black
    per, reps = 16, 3
    cols, rows = per * reps, 15
    g = Grid(cols, rows)
    for c in range(cols):
        k = c % 4
        g.put(c, 0, "D")
        tooth = [0, 1, 2, 1][k]
        for r in range(1, 2 + tooth):
            g.put(c, r, "R")
        g.put(c, rows - 1, "D")
        for r in range(rows - 2 - tooth, rows - 1):
            g.put(c, r, "R")
    sm = star_rows(4, fill="R", edge="D", core="K", centre="O")
    for i in range(reps):
        g.stamp(sm, i * per + 4, 3)
        # black running diamond between stars
        cx = i * per + 0
        for d in range(4):
            for (x, y) in ((cx - d, 7 - (3 - d)), (cx + d, 7 - (3 - d)), (cx - d, 7 + (3 - d)), (cx + d, 7 + (3 - d))):
                g.put(x % cols, y, "K")
        g.put(cx % cols, 7, "G")
    lines = g.lines()
    W, H = cols * CELL, rows * CELL
    art = stitch_layer(W + 2 * CELL, H + 2 * CELL, parse_grid(lines, PAL), CELL, CELL, CELL, seed=11)
    # make it tile: crop exactly the period (stitch shadows spill a little; keep one cell margin vertically)
    tile = art[:, CELL:CELL + W]
    tile = np.concatenate([tile[:, : per * CELL], ], 1)
    prev(opaque(tile, LINEN), "tz-band", bg=LINEN)
    save_full(tile, f"{OUT}/band.webp", size=(per * CELL // 2, (rows + 2) * CELL // 2), quality=84)

if "panel" in PARTS:
    # cover centrepiece (qabbeh-style chest panel): two cypress trees flanking a big star medallion, rosettes,
    # inside a sawtooth frame with black running stitch
    cols, rows = 61, 49
    g = Grid(cols, rows)
    for c in range(cols):
        g.put(c, 0, "D"); g.put(c, rows - 1, "D")
        if c % 2 == 0:
            g.put(c, 1, "R"); g.put(c, rows - 2, "R")
    for r in range(rows):
        g.put(0, r, "D"); g.put(cols - 1, r, "D")
        if r % 2 == 0:
            g.put(1, r, "R"); g.put(cols - 2, r, "R")
    for c in range(3, cols - 3):
        if c % 3 != 2:
            g.put(c, 3, "K"); g.put(c, rows - 4, "K")
    for r in range(3, rows - 3):
        if r % 3 != 2:
            g.put(3, r, "K"); g.put(cols - 4, r, "K")
    big = star_rows(13, fill="R", edge="D", core="K", centre="O")
    g.stamp(big, cols // 2 - 13, 6)
    cy = cypress_rows(28)
    g.stamp(cy, 6, 6)
    g.stamp(cy, cols - 7 - len(cy[0]), 6)
    ro = rose_rows(5)
    for (c0, r0) in ((cols // 2 - 5, 34),):
        g.stamp(ro, c0, r0)
    for (c0, r0) in ((6, 36), (cols - 6 - 11, 36)):
        g.stamp(star_rows(4, "P", "D", "K", "O"), c0 + 1, r0)
    art = render(g.lines(), "tz-panel", seed=21)
    save(art, f"{OUT}/panel.webp", max_w=620, quality=82)

if "star" in PARTS:
    art = render(star_rows(9, "R", "D", "K", "O"), "tz-star", seed=31, cell=12)
    save(art, f"{OUT}/star.webp", max_w=120, quality=86)

if "cypress" in PARTS:
    art = render(cypress_rows(27, tiers=4), "tz-cypress", seed=41, cell=10)
    save(art, f"{OUT}/cypress.webp", max_w=110, quality=86)

if "rose" in PARTS:
    art = render(rose_rows(7), "tz-rose", seed=51, cell=11)
    save(art, f"{OUT}/rose.webp", max_w=100, quality=86)
