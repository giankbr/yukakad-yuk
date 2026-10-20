"""Boarding Pass — painted assets: dusk sky hero with gouache cloud banks, gouache airliner (separate, floats),
worn rubber postmark, night cloud strip, gouache suitcase, inked flight-path divider, paper grain tile.
Run: python3 -I /tmp/pen/art/themes/boarding-pass.py
Medium: gouache + ink line on painted sky; stamps are worn rubber-stamp ink."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p3_common import *  # noqa

T = "boarding-pass"
D = outdir(T)
nxt = Seeds(400)
rng = random.Random(41)

NAVY, AMBER = "#0b2545", "#f4a000"


def sky():
    W, H = 780, 1200
    art = painted_sky(W, H, [(0, "#0b2545"), (0.2, "#163a66"), (0.42, "#3f6f9c"), (0.6, "#9fb0bd"), (0.7, "#e7b98e"), (0.78, "#c98a6c"), (0.9, "#0b2545"), (1.0, "#0b2545")], seed=nxt(), streak=0.9, grain=0.7)
    # soft watercolour haze bands near the horizon
    for i, (y, col, dens) in enumerate([(700, "#d9b89a", 0.35), (790, "#f0cfae", 0.4), (880, "#b77a63", 0.3)]):
        m = shape_mask(W, H, deform(ellipse_pts(rng.uniform(300, 480), y, 520, 46, 16), rng, 3, 0.1))
        art = over(art, pigment(m, col, mix(col, "#ffffff", .3), seed=nxt(), density=dens, edge=0.25, bloom=0.5, rough=12, feather=6, gran=0.1))
    # low sun glow
    art = over(art, glow(dots_mask(W, H, [(600, 965, 44)]), "#ffd9a0", radius=70, strength=0.5))
    art = over(art, glow(dots_mask(W, H, [(600, 965, 24)]), "#fff1cf", radius=10, strength=0.9))
    # far clouds: watercolour, soft
    for cx, cy, rx, ry, col in [(120, 760, 170, 36, "#e9c4a4"), (650, 720, 150, 30, "#d8b5a0"), (380, 830, 220, 28, "#f2d2b4"), (200, 900, 260, 30, "#9c6a5c")]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.5)
        art = over(art, pigment(m, col, mix(col, "#9a7a74", .3), seed=nxt(), density=0.6, edge=0.4, bloom=0.4, rough=6, feather=2.5))
    # near cloud banks: gouache, lit from the right-bottom (sun)
    banks = [(-40, 330, 260, 110), (760, 270, 230, 100), (110, 150, 150, 60), (700, 70, 120, 48), (420, 420, 180, 70), (-20, 560, 200, 80), (800, 520, 220, 90)]
    for cx, cy, rx, ry in banks:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.55)
        c = gouache_obj(m, "#f6efe4", "#e4d9cf", seed=nxt(), rough=3.0, streak=0.5, light=(0.5, 0.9), k=0.35, blur=14, hi="#fff4df", lo="#7b7f9c")
        c[..., 3] *= 0.96
        art = over(art, c)
        # pigment shadow underside
        sh = np.clip(gaussian_filter(m, 6) - np.roll(gaussian_filter(m, 6), -8, 0), 0, 1)
        art = over(art, clipped(pigment(m, "#8b8aa6", seed=nxt(), density=0.35, edge=0, bloom=0.3, rough=4, feather=3), sh * 2))
    # fade the bottom into navy (CSS also fades, keep the blend soft)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    f = np.clip((yy - 960) / 200, 0, 1) ** 1.4
    art = tint(art, f, NAVY, 1.0)
    preview(art, f"{PREV}/bp-sky.png", NAVY)
    save(art, f"{D}/sky.webp", q=80, trim=False)


def plane():
    W, H = 420, 260
    art = blank(W, H)
    parts = airliner_parts(W, H, 215, 118, 320, rng, bank=-0.16)
    a, m = paint_airliner(W, H, parts, rng, nxt, body="#f6f1e8", body2="#e3dccd", navy="#1b3a66", accent=AMBER)
    # soft contrail behind
    trail = stroke_mask(W, H, curve([(10, 150), (60, 148), (100, 146)], 20), 10, (0.4, 0.05))
    art = over(art, pigment(trail, "#ffffff", seed=nxt(), density=0.35, edge=0.1, bloom=0.3, rough=4, feather=3))
    art = over(art, a)
    preview(art, f"{PREV}/bp-plane.png", "#3f6f9c")
    save(art, f"{D}/plane.webp", max_w=340, q=84)


def stamp():
    W = H = 300
    art = postmark(W, H, 150, 150, 132, "RAWUH AIR", "FIRST LOVE CLASS", "BOARDED", rng, nxt, col="#c63a2a", wear=0.5, rot=-0.22, date="GATE CINTA 1")
    preview(art, f"{PREV}/bp-stamp.png", "#ffffff")
    save(art, f"{D}/stamp.webp", max_w=260, q=82)


def clouds():
    """Night cloud strip for the bottom of the cover (dim, bluish)."""
    W, H = 780, 240
    art = blank(W, H)
    for cx, cy, rx, ry in [(90, 190, 220, 90), (420, 210, 260, 100), (720, 180, 200, 80), (250, 230, 160, 60), (600, 240, 180, 60)]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.5)
        c = gouache_obj(m, "#2b4a78", "#1c3760", seed=nxt(), rough=3.5, light=(0.2, -1.0), k=0.4, blur=14, hi="#5f82b4", lo="#0a1e3c")
        art = over(art, c)
    preview(art, f"{PREV}/bp-clouds.png", NAVY)
    save(art, f"{D}/clouds.webp", q=78)


def luggage():
    W, H = 300, 260
    a, _ = paint_suitcase(W, H, 150, 142, 210, rng, nxt, col="#1f3d6b", col2="#15305a", trim="#e8c070", ink_col="#0b1f3d", stickers=True)
    preview(a, f"{PREV}/bp-luggage.png", "#f4f7fb")
    save(a, f"{D}/luggage.webp", max_w=220, q=84)


def divider():
    W, H = 720, 80
    pts = curve([(20, 56), (180, 48), (360, 40), (540, 30), (690, 22)], 90)
    m = np.zeros((H, W), np.float32)
    for i in range(0, len(pts) - 6, 9):
        m = np.maximum(m, stroke_mask(W, H, pts[i:i + 5], 3.2, (0.2, 0.2)))
    art = ink(m, "#5e748a", nxt(), 0.8, 1.0)
    parts = airliner_parts(W, H, 672, 24, 70, rng, bank=-0.1)
    whole = np.zeros((H, W), np.float32)
    for k in ("fus", "fin", "tail", "wing", "wing2"):
        whole = np.maximum(whole, shape_mask(W, H, parts[k]))
    art = over(art, ink(whole, "#13293d", nxt(), 0.9, 1.0))
    # heart at the start
    hm = shape_mask(W, H, deform([(20, 50), (27, 42), (35, 44), (34, 52), (24, 64), (14, 52), (13, 44), (20, 42)], rng, 2, 0.04))
    art = over(art, ink(hm, "#f4a000", nxt(), 0.9, 1.0))
    preview(art, f"{PREV}/bp-divider.png", "#f4f7fb")
    save(art, f"{D}/divider.webp", max_w=360, q=82)


def paper_tex():
    t = grain_overlay(256, "#2e4668", seed=9, base=0.006, k=1.0, cap=0.055, fiber=0.5, mottle=0.7)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["sky", "plane", "stamp", "clouds", "luggage", "divider", "paper"]
    for w in which:
        {"sky": sky, "plane": plane, "stamp": stamp, "clouds": clouds, "luggage": luggage, "divider": divider, "paper": paper_tex}[w]()
