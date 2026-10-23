"""Bauhaus Primer — screen-printed primary geometry on off-white stock: a cover poster (cropped red sun, blue square
overprinting it, yellow triangle, black bars and a halftone quarter), single-ink sprites (circle, triangle, square,
half-disc, ring) and a tileable newsprint paper. Flat ink with mesh texture, pull streaks, pinholes and slight
misregistration; overlaps multiply like real overprints.
Run: python3 -I bauhaus-primer.py [part ...]  parts: poster sprites paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h4_lib import *  # noqa

OUT = outdir("bauhaus-primer")
PARTS = sys.argv[1:] or ["poster", "sprites", "paper"]
RED, YEL, BLU, BLK, OFF = "#d8402b", "#f1bb1f", "#1f4fa0", "#1b1a19", "#f1ece1"


def tri(W, H, pts):
    return shape_mask(W, H, pts, smooth=False)


if "poster" in PARTS:
    W, H = 780, 860
    art = blank(W, H)
    # yellow first (lightest ink), then red, blue, black — like a real pull order
    art = SC(art, tri(W, H, [(40, 840), (330, 330), (620, 840)]), YEL, seed=1, starve=0.1)
    art = SCM(art, circles(W, H, [(560, 300, 236)]), RED, seed=2, starve=0.12)
    # halftone shading on the red sun (lower-left quarter)
    xx, yy = grid_xy(W, H)
    tone = np.clip(((xx - 560) * -0.7 + (yy - 300) * 0.7) / 240, 0, 1) ** 1.3
    ht = halftone(W, H, tone * 0.8, cell=11, angle=0.26) * circles(W, H, [(560, 300, 236)])
    art = SCM(art, ht, "#9e2618", seed=3, wear=0.1, rough=0.6)
    art = SCM(art, rect_mask(W, H, 70, 150, 390, 470), BLU, seed=4, starve=0.1)
    # black: a heavy bar, a thin rule, a small disc, a half-disc
    art = SC(art, rect_mask(W, H, 0, 520, 520, 566), BLK, seed=5, wear=0.18)
    art = SC(art, rect_mask(W, H, 452, 40, 460, 780), BLK, seed=6, wear=0.1, rough=0.8)
    art = SC(art, circles(W, H, [(232, 668, 34)]), BLK, seed=7)
    half = circles(W, H, [(690, 720, 90)]) * (yy > 720)
    art = SCM(art, half, BLU, seed=8)
    ring = np.clip(circles(W, H, [(690, 720, 90)]) - circles(W, H, [(690, 720, 82)]), 0, 1) * (yy <= 722)
    art = SC(art, ring, BLK, seed=9, rough=0.6)
    # misregistered key line: the blue square outline printed a hair off
    out = np.clip(rect_mask(W, H, 76, 156, 398, 478) - rect_mask(W, H, 80, 160, 394, 474), 0, 1)
    art = SC(art, out, BLK, seed=10, wear=0.35, rough=0.5)
    preview(art, "bh-poster", tone=OFF)
    save(art, f"{OUT}/poster.webp", max_w=780, quality=84)
    clear()

if "sprites" in PARTS:
    S = 240
    specs = {
        "circle": (lambda: circles(S, S, [(120, 120, 110)]), RED),
        "tri": (lambda: tri(S, S, [(10, 222), (120, 22), (230, 222)]), YEL),
        "square": (lambda: rect_mask(S, S, 20, 20, 220, 220), BLU),
        "half": (lambda: circles(S, S, [(120, 120, 110)]) * (np.mgrid[0:S, 0:S][0] < 120), BLK),
        "ring": (lambda: np.clip(circles(S, S, [(120, 120, 110)]) - circles(S, S, [(120, 120, 70)]), 0, 1), RED),
    }
    for k, (name, (fn, col)) in enumerate(specs.items()):
        art = SC(blank(S, S), fn(), col, seed=30 + k, starve=0.3, wear=0.25)
        if name in ("circle", "square"):
            xx, yy = grid_xy(S, S)
            tone = np.clip((xx + yy - 200) / 280, 0, 1)
            art = SCM(art, halftone(S, S, tone * 0.7, cell=9, angle=0.3) * fn(), "#7d1f14" if name == "circle" else "#0f2d63", seed=40 + k, wear=0.1, rough=0.5)
        preview(art, f"bh-{name}", tone=OFF)
        save(art, f"{OUT}/{name}.webp", max_w=160, quality=84)
    clear()

if "paper" in PARTS:
    P = 320
    base = rgb_of(OFF)
    fib = gaussian_filter(np.random.default_rng(3).random((P, P)).astype(np.float32), (0.5, 3.0), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    cl = wrapn(P, P, 4, 26)
    sp = (np.random.default_rng(5).random((P, P)) > 0.9985).astype(np.float32)
    sp = gaussian_filter(sp, 0.5, mode="wrap") * 4
    rgb = base[None, None] * (0.975 + 0.012 * fib + (cl - 0.5) * 0.05 - np.clip(sp, 0, .6) * 0.35)[..., None]
    save_rgb(opaque(rgb), f"{OUT}/paper.webp", quality=78)
