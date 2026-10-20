"""Boho Terakota — opaque gouache folk paint: pampas plumes (two variants, animated separately), rainbow arch,
sun (mustard + blush), and a light linen grain overlay.
Run: python3 -I /tmp/pen/art/themes/boho-terakota.py [pampas|rainbow|sun|grain]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b_common import *  # noqa

T = "boho-terakota"
D = outdir(T)
nxt = Seeds(1300)
rng = random.Random(7)
TERRA, MUSTARD, BLUSH, SAGE, CREAM = "#c0643f", "#d39a4a", "#e8b4a0", "#8f9a76", "#fff6ec"


# ---------- 1. pampas plume ----------
def plume(name, seed, lean, length=1.0):
    W, H = 300, 600
    r = random.Random(seed)
    base = (150, 590)
    top = (150 + lean * 130, 34)
    ctrl = (150 - lean * 20, 300)
    def at(t):
        return tuple((1 - t) ** 2 * base[k] + 2 * (1 - t) * t * ctrl[k] + t * t * top[k] for k in (0, 1))
    stem = [at(t) for t in np.linspace(0, 1, 60)]
    art = blank(W, H)
    sm = stroke_mask(W, H, stem, 4.2, (0.02, 0.4))
    art = over(art, gouache_paint(sm, "#a9875f", "#8f6f4c", seed=seed + 1, rough=1.2, streak=0.4))
    # feathery fronds: many thin tapered strokes curving up and out from the upper 65% of the stem
    fr_light = np.zeros((H, W), np.float32)
    fr_dark = np.zeros((H, W), np.float32)
    for i in range(280):
        t = 0.36 + 0.64 * (i / 280) + r.uniform(-0.01, 0.01)
        x0, y0 = at(t)
        (xa, ya), (xb, yb) = at(max(0, t - 0.01)), at(min(1, t + 0.01))
        tang = math.atan2(yb - ya, xb - xa)
        side = 1 if i % 2 else -1
        envelope = math.sin(math.pi * min(1, (t - 0.33) / 0.67)) ** 0.7  # plume is widest in the middle
        L = (30 + 92 * envelope) * r.uniform(0.7, 1.15)
        ang = tang + side * r.uniform(0.3, 0.85)
        bend = side * r.uniform(-0.25, -0.05)
        pts = []
        for k in range(10):
            u = k / 9
            a = ang + bend * u
            pts.append((x0 + math.cos(a) * L * u, y0 + math.sin(a) * L * u))
        m = stroke_mask(W, H, pts, r.uniform(1.8, 3.2), (0.1, 0.7))
        if r.random() < 0.7:
            fr_light = np.maximum(fr_light, m)
        else:
            fr_dark = np.maximum(fr_dark, m)
    fluff = gaussian_filter(np.maximum(fr_light, fr_dark), 5) * 1.4
    art = over(art, pigment(np.clip(fluff, 0, 1), "#e6cfa8", "#d8bd94", seed=seed + 4, density=0.45, edge=0.1, bloom=0.5, gran=0.4, feather=3, rough=8))
    art = over(art, gouache_paint(fr_dark, "#c9a77e", "#b89468", seed=seed + 2, rough=1.4, streak=0.6, dry=0.25, density=0.9))
    art = over(art, gouache_paint(fr_light, "#ead6b5", "#dcc4a0", seed=seed + 3, rough=1.4, streak=0.6, dry=0.3, density=0.92))
    art = shade(art, np.maximum(fr_light, fr_dark), light=(-0.7, -0.4), k=0.12, blur=10, hi="#fff3df", lo="#9b7a55")
    preview(art, f"{PREV}/bt-{name}.png", "#f3e4d3")
    save(art, f"{D}/{name}.webp", max_w=150, q=80, trim=False)


def pampas():
    plume("pampas-a", 41, 0.35)
    plume("pampas-b", 77, -0.2)


# ---------- 2. rainbow ----------
def rainbow():
    W, H = 600, 316
    cx, cy = 300, 306
    art = blank(W, H)
    bands = [(TERRA, "#a9532f", 264), (MUSTARD, "#c28838", 210), (BLUSH, "#dca08a", 156), (SAGE, "#7d8865", 102)]
    for col, col2, r in bands:
        pts = arc_pts(cx, cy, r, math.pi, math.tau, 60)
        pts = [(x + rng.gauss(0, 0.6), y + rng.gauss(0, 0.6)) for x, y in pts]
        m = stroke_mask(W, H, pts, 42, (0.001, 0.001))
        # flatten the stroke ends to sit on the baseline
        m[cy - 2:, :] = 0
        layer = gouache_paint(m, col, col2, seed=nxt(), rough=2.6, streak=0.75)
        layer = shade(layer, m, light=(-0.5, -0.8), k=0.08, blur=8, hi="#fff2e2", lo="#5c2e1c")
        art = over(art, layer)
    preview(art, f"{PREV}/bt-rainbow.png", "#f3e4d3")
    save(art, f"{D}/rainbow.webp", max_w=400, q=82)


# ---------- 3. sun ----------
def sun(name, col, col2):
    W = H = 240
    c = 120
    rng.seed(13)
    rays = np.zeros((H, W), np.float32)
    for i in range(12):
        a = i * math.tau / 12 + rng.gauss(0, 0.03)
        r0, r1 = 74 + rng.uniform(-3, 3), 104 + rng.uniform(-5, 5)
        rays = np.maximum(rays, stroke_mask(W, H, [(c + math.cos(a) * (r0 + (r1 - r0) * u), c + math.sin(a) * (r0 + (r1 - r0) * u)) for u in np.linspace(0, 1, 8)], 9, (0.15, 0.4)))
    disc = shape_mask(W, H, deform(ellipse_pts(c, c, 54, 54, 24), rng, 2, .02))
    art = blank(W, H)
    art = over(art, gouache_paint(rays, col, col2, seed=nxt(), rough=1.6, streak=0.9))
    d = gouache_paint(disc, col, col2, seed=nxt(), rough=2.0, streak=1.0)
    d = shade(d, disc, light=(-0.6, -0.6), k=0.1, blur=8, hi="#fff2e2", lo="#6b3a1e")
    art = over(art, d)
    preview(art, f"{PREV}/bt-{name}.png", "#c0643f" if name == "sun-blush" else "#f3e4d3")
    save(art, f"{D}/{name}.webp", max_w=180, q=84, trim=False)


def suns():
    sun("sun", MUSTARD, "#c48a3a")
    sun("sun-blush", BLUSH, "#efc5b4")


# ---------- 4. linen grain overlay ----------
def grain():
    t = grain_overlay(256, "#6a3a22", seed=5, base=0.008, k=1.1, cap=0.07, fiber=0.5, mottle=0.4)
    # faint linen weave
    yy, xx = np.mgrid[0:256, 0:256].astype(np.float32)
    weave = (np.sin(xx / 256 * math.tau * 64) * np.sin(yy / 256 * math.tau * 64)) * 0.012
    t[..., 3] = np.clip(t[..., 3] + np.abs(weave), 0, 0.1)
    save(t, f"{D}/grain.webp", q=60, trim=False)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["pampas", "rainbow", "sun", "grain"]:
        {"pampas": pampas, "rainbow": rainbow, "sun": suns, "grain": grain}[w]()
