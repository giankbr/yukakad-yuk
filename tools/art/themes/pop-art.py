"""Pop Art — original comic-print pieces: speech + thought bubbles, a starburst, a Ben-Day heart, two rings with
action lines, and Ben-Day dot tiles. Printed look: flat process colours slightly off-register under a hand-inked
black line, dot gain and ink wear on newsprint. Run: python3 -I pop-art.py [part ...]
parts: dots bubble thought burst heart rings -> public/themes/art/pop-art/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i5_lib import *

OUT = outdir("pop-art")
PARTS = sys.argv[1:] or ["dots", "bubble", "thought", "burst", "heart", "rings"]
SEQ = Seq(700)
INK = "#15121a"
RED, RED_D = "#e5322a", "#b31d1d"
YEL, YEL_D = "#ffd21f", "#f2a516"
BLUE, CYAN = "#1d5fc4", "#2aa6df"
PAPER = "#fbf5e4"
WHITE = "#fffdf6"


def flat(mask, col, seed, wear=0.12):
    """Process-colour fill: soft-crisp edge with slight ink wear (paper white stays clean)."""
    out = linocut(mask, col, seed=seed, wear=wear, rough=1.0)
    if col == WHITE:
        out[..., :3] = np.array(hex_rgb(WHITE), np.float32)
    return out


def inked(lay, mask, width, seed, offset=(0, 0)):
    """Black comic outline around a filled mask (outline drawn over the fill, fill shifted = off-register)."""
    line = outline(mask, width=width, seed=seed, wob=1.4)
    line = np.clip(line + edge_line(mask, width * 0.5, seed + 1) * 0.6, 0, 1)
    return OV(lay, line, lambda m: ink(m, INK, seed=seed + 2, wear=0.08), pad=8)


def dots_layer(mask, tone, col, spacing=10.0, angle=math.pi / 4, seed=1):
    h, w = mask.shape
    d = halftone(w, h, tone, spacing, angle, seed=seed, jitter=0.6) * mask
    return flat(d, col, seed, wear=0.18)


def p_dots():
    """Seamless Ben-Day tiles (192 px): red dots and blue dots on transparent."""
    S = 192
    for name, col in (("dots-red", RED), ("dots-blue", CYAN)):
        tone = np.full((S, S), 0.2, np.float32)
        sp = S / 16 / math.sqrt(2)
        d = halftone(S, S, tone, sp, math.pi / 4, jitter=0)
        wear = wrap_noise(S, S, 5, 1.2)
        d = d * (1 - np.clip((wear - 0.7) * 3, 0, 1) * 0.5)
        save_full(rgba(col, d), f"{OUT}/{name}.webp", quality=80)


def p_bubble():
    W, H = 820, 600
    rng = random.Random(3)
    body = ellipse_pts(420, 255, 360, 215, 16, -0.03)
    body = deform(body, rng, 1, 0.01)
    tail = [(250, 410), (150, 585), (360, 440)]
    m = np.clip(shape_mask(W, H, body) + shapes(W, H, [tail], smooth=False), 0, 1)
    lay = blank(W, H)
    # hard comic drop shadow (solid ink offset)
    lay = OV(lay, shift(m, 14, 14), lambda mm: flat(mm, INK, SEQ(), 0.05))
    lay = OV(lay, m, lambda mm: flat(mm, WHITE, SEQ(), 0.0))
    lay = inked(lay, m, 11, SEQ())
    preview(lay, "pop-bubble", bg="#ffd21f")
    save(lay, f"{OUT}/bubble.webp", max_w=420)


def p_thought():
    W, H = 780, 620
    rng = random.Random(9)
    lobes = []
    for i in range(13):
        a = i / 13 * math.tau
        lobes.append((390 + math.cos(a) * 285, 245 + math.sin(a) * 170, rng.uniform(70, 92)))
    lobes.append((390, 245, 260))
    m = np.clip(ellipses(W, H, [(390, 245, 300, 180, 0)]) + circles(W, H, lobes[:-1]), 0, 1)
    small = circles(W, H, [(170, 480, 34), (110, 548, 22), (68, 592, 13)])
    lay = blank(W, H)
    allm = np.clip(m + small, 0, 1)
    lay = OV(lay, shift(allm, 12, 12), lambda mm: flat(mm, INK, SEQ(), 0.05))
    lay = OV(lay, allm, lambda mm: flat(mm, WHITE, SEQ(), 0.0))
    # inner scallop lines for the cloud
    lay = inked(lay, m, 10, SEQ())
    lay = inked(lay, small, 8, SEQ())
    preview(lay, "pop-thought", bg="#2aa6df")
    save(lay, f"{OUT}/thought.webp", max_w=400)


def p_burst():
    W = H = 760
    rng = random.Random(21)
    cx = cy = 380
    outer = shape_mask(W, H, burst_pts(cx, cy, 360, 240, 14, rng, 0.14, 0.1), smooth=False)
    inner = shape_mask(W, H, burst_pts(cx, cy, 270, 190, 12, rng, 0.16, 0.35), smooth=False)
    lay = blank(W, H)
    lay = OV(lay, shift(outer, 14, 14), lambda mm: flat(mm, INK, SEQ(), 0.05))
    lay = OV(lay, shift(outer, 4, 3), lambda mm: flat(mm, RED, SEQ()))
    # red dots growing toward the spikes
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.hypot(xx - cx, yy - cy) / 360
    lay = over(lay, dots_layer(outer, np.full(outer.shape, 0.22, np.float32), RED_D, 13, seed=SEQ()))
    lay = inked(lay, outer, 12, SEQ())
    lay = OV(lay, shift(inner, 3, 2), lambda mm: flat(mm, YEL, SEQ()))
    tone = np.clip((rr - 0.35) * 1.6, 0, 0.7)
    lay = over(lay, dots_layer(inner, tone, YEL_D, 12, seed=SEQ()))
    lay = inked(lay, inner, 9, SEQ())
    preview(lay, "pop-burst", bg=PAPER)
    save(lay, f"{OUT}/burst.webp", max_w=380)


def heart_pts(cx, cy, s, n=80):
    pts = []
    for i in range(n):
        t = i / n * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s, cy + y * s))
    return pts


def p_heart():
    W, H = 420, 400
    m = shape_mask(W, H, heart_pts(205, 185, 11.5), smooth=False)
    lay = blank(W, H)
    lay = OV(lay, shift(m, 10, 10), lambda mm: flat(mm, INK, SEQ(), 0.05))
    lay = OV(lay, shift(m, 4, 3), lambda mm: flat(mm, RED, SEQ()))
    sh = shade_field(m, (-0.7, -0.7), 18, 26)
    lay = over(lay, dots_layer(m, np.clip(sh * 1.3 - 0.15, 0, 0.75), RED_D, 11, seed=SEQ()))
    shine = shapes(W, H, [deform(ellipse_pts(130, 110, 40, 20, 10, -0.7), random.Random(2), 1, .03)])
    shine2 = circles(W, H, [(176, 84, 10)])
    lay = OV(lay, np.clip(shine + shine2, 0, 1), lambda mm: flat(mm, WHITE, SEQ(), 0.0))
    lay = inked(lay, m, 9, SEQ())
    preview(lay, "pop-heart", bg=PAPER)
    save(lay, f"{OUT}/heart.webp", max_w=200)


def p_rings():
    W, H = 640, 470
    rng = random.Random(4)
    r1 = np.clip(ellipses(W, H, [(250, 260, 140, 150, 0)]) - ellipses(W, H, [(250, 260, 108, 118, 0)]), 0, 1)
    r2 = np.clip(ellipses(W, H, [(395, 255, 140, 150, 0)]) - ellipses(W, H, [(395, 255, 108, 118, 0)]), 0, 1)
    gem = shapes(W, H, [[(395, 70), (430, 98), (395, 140), (360, 98)]], smooth=False)
    lay = blank(W, H)
    # action / emanata lines around
    em = []
    for a in np.linspace(-2.7, -0.4, 7):
        x0, y0 = 322 + math.cos(a) * 235, 255 + math.sin(a) * 215
        x1, y1 = 322 + math.cos(a) * 300, 255 + math.sin(a) * 265
        em.append(([(x0, y0), (x1, y1)], 9, (0.1, 0.6)))
    lay = OV(lay, strokes(W, H, em), lambda mm: ink(mm, INK, SEQ()))
    for ring, col in ((r1, YEL), (r2, YEL)):
        lay = OV(lay, shift(ring, 8, 8), lambda mm: flat(mm, INK, SEQ(), 0.05))
    # ring 1 behind ring 2 at one crossing, in front at the other (interlocked)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    front2 = r2 * (yy > 255).astype(np.float32)
    for ring in (r1,):
        lay = OV(lay, shift(ring, 3, 2), lambda mm: flat(mm, YEL, SEQ()))
        lay = over(lay, dots_layer(ring, np.clip(shade_field(ring, (-0.7, -0.7), 8, 10) * 1.2, 0, 0.7), YEL_D, 9, seed=SEQ()))
        lay = inked(lay, ring, 7, SEQ())
    lay = OV(lay, shift(r2, 3, 2), lambda mm: flat(mm, YEL, SEQ()))
    lay = over(lay, dots_layer(r2, np.clip(shade_field(r2, (-0.7, -0.7), 8, 10) * 1.2, 0, 0.7), YEL_D, 9, seed=SEQ()))
    lay = inked(lay, r2, 7, SEQ())
    # bring ring 1 back on top where it crosses in the upper half
    top1 = r1 * (yy < 255).astype(np.float32) * (xx > 300)
    lay = OV(lay, shift(top1, 3, 2), lambda mm: flat(mm, YEL, SEQ()))
    lay = over(lay, dots_layer(top1, np.full(top1.shape, 0.3, np.float32), YEL_D, 9, seed=SEQ()))
    lay = inked(lay, r1 * (yy < 255) * (xx > 290), 7, SEQ())
    lay = OV(lay, shift(gem, 3, 2), lambda mm: flat(mm, CYAN, SEQ()))
    gl = shapes(W, H, [[(395, 70), (430, 98), (395, 98)]], smooth=False)
    lay = OV(lay, gl, lambda mm: flat(mm, WHITE, SEQ(), 0.0))
    lay = inked(lay, gem, 6, SEQ())
    del front2
    # shine glints
    gl2 = np.clip(strokes(W, H, [([(165, 210), (180, 170)], 9, (0.2, 0.2)), ([(470, 205), (480, 180)], 7, (0.2, 0.2))]), 0, 1)
    lay = OV(lay, gl2, lambda mm: flat(mm, WHITE, SEQ(), 0.0))
    preview(lay, "pop-rings", bg="#e5322a")
    save(lay, f"{OUT}/rings.webp", max_w=320)


for p in PARTS:
    {"dots": p_dots, "bubble": p_bubble, "thought": p_thought, "burst": p_burst, "heart": p_heart, "rings": p_rings}[p]()
    flush()
kb(OUT)
