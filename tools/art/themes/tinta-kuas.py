"""Tinta Kuas — bold black brush-ink strokes (bristle texture, dry-brush tails) and pressed-gold ink splatters on white.
Run: python3 -I tinta-kuas.py [part ...]   parts: swash sweep ring splat rule dab
Assets -> public/themes/art/tinta-kuas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o6_lib import *

OUT = outdir("tinta-kuas")
PARTS = sys.argv[1:] or ["swash", "sweep", "ring", "splat", "rule", "dab"]
BLACK = "#141414"
GOLD = "#c9a24a"


def gold_splat(W, H, rng, nx, specs, art=None):
    art = blank(W, H) if art is None else art
    m = np.zeros((H, W), np.float32)
    for (cx, cy, spread, n, big) in specs:
        m = np.maximum(m, splatter(W, H, rng, cx, cy, spread, n, big))
    m = displace(m, nx(), 1.5, 10)
    return FO(art, np.clip(m, 0, 1), GOLD, seed=nx(), emboss=0.5, sparkle=0.15)


if "swash" in PARTS:
    # one loaded horizontal stroke rising slightly, pressure swelling in the middle, the tail flicking into dry bristles
    W, H = 980, 300
    rng = random.Random(4); nx = Seq(400)
    pts = curve([(40, 190), (260, 150), (560, 140), (800, 120), (950, 86)], 160)
    press = lambda t: (0.45 + 0.55 * (t / .08) ** .5) if t < .08 else (1.0 + 0.12 * math.sin(t * 5)) * (1 if t < .7 else max(.15, (1 - t) / .3) ** .6)
    m = bristle_mask(W, H, pts, 150, rng, n=60, dry=0.55, press=press, gap=0.7)
    art = INK(blank(W, H), m, BLACK, seed=nx(), wet=0.6)
    save(art, f"{OUT}/swash.webp", max_w=820, quality=80)
    prev(art, "tk_swash", tone="#fbfaf7")

if "sweep" in PARTS:
    # a curving corner sweep (quarter turn), heavy at the start, thinning and splitting at the end
    W, H = 640, 640
    rng = random.Random(8); nx = Seq(800)
    pts = curve([(600, 40), (460, 70), (300, 170), (190, 330), (140, 470), (130, 610)], 150)
    m = bristle_mask(W, H, pts, 110, rng, n=48, dry=0.6, taper=(0.06, 0.45), gap=0.8)
    pts2 = curve([(620, 150), (520, 190), (430, 270), (380, 360)], 80)
    m = np.maximum(m, bristle_mask(W, H, pts2, 34, rng, n=18, dry=0.7, taper=(0.1, 0.5)))
    art = INK(blank(W, H), m, BLACK, seed=nx(), wet=0.5)
    art = gold_splat(W, H, rng, nx, [(250, 420, 70, 40, 9), (470, 150, 50, 24, 6)], art)
    save(art, f"{OUT}/sweep.webp", max_w=480, quality=80)
    prev(art, "tk_sweep", tone="#fbfaf7")

if "ring" in PARTS:
    # brush ring for portraits: starts heavy at the bottom-left, travels clockwise, lifts before closing
    W, H = 460, 460
    rng = random.Random(12); nx = Seq(1200)
    cx, cy, R = 230, 230, 186
    pts = [(cx + math.cos(a) * R * (1 + 0.025 * math.sin(a * 3)), cy + math.sin(a) * R) for a in np.linspace(2.4, 2.4 + math.tau * 0.9, 220)]
    m = bristle_mask(W, H, pts, 30, rng, n=26, dry=0.6, taper=(0.04, 0.3), gap=0.8)
    art = INK(blank(W, H), m, BLACK, seed=nx(), wet=0.5)
    art = gold_splat(W, H, rng, nx, [(cx + R * .78, cy - R * .62, 30, 18, 6)], art)
    save(art, f"{OUT}/ring.webp", max_w=340, quality=82)
    prev(art, "tk_ring", tone="#fbfaf7")

if "splat" in PARTS:
    W, H = 560, 420
    rng = random.Random(16); nx = Seq(1600)
    art = gold_splat(W, H, rng, nx, [(280, 210, 90, 90, 16), (120, 320, 40, 26, 7), (460, 90, 36, 22, 6)])
    save(art, f"{OUT}/splat.webp", max_w=420, quality=82)
    prev(art, "tk_splat", tone="#fbfaf7")

if "rule" in PARTS:
    # divider: a quick dry dash with a gold drop beside it
    W, H = 520, 90
    rng = random.Random(20); nx = Seq(2000)
    pts = curve([(40, 52), (200, 44), (380, 42), (470, 36)], 80)
    m = bristle_mask(W, H, pts, 16, rng, n=14, dry=0.55, taper=(0.05, 0.45), gap=0.8)
    art = INK(blank(W, H), m, BLACK, seed=nx(), wet=0.3)
    art = gold_splat(W, H, rng, nx, [(492, 40, 10, 8, 6)], art)
    save(art, f"{OUT}/rule.webp", max_w=360, quality=84)
    prev(art, "tk_rule", tone="#fbfaf7")

if "dab" in PARTS:
    # one fat dab (brush pressed and dragged a little) for numbers / nodes
    W, H = 240, 170
    rng = random.Random(24); nx = Seq(2400)
    pts = curve([(40, 100), (110, 84), (200, 74)], 60)
    m = bristle_mask(W, H, pts, 90, rng, n=34, dry=0.45, taper=(0.15, 0.4), gap=0.6)
    art = INK(blank(W, H), m, BLACK, seed=nx(), wet=0.6)
    save(art, f"{OUT}/dab.webp", max_w=160, quality=84)
    prev(art, "tk_dab", tone="#fbfaf7")

kb(OUT)
