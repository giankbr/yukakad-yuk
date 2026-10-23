"""Zaitun Syari — silvery-green olive branches with dark olives, watercolour on linen paper.
Run: python3 -I zaitun-syari.py [part ...]  parts: branch sprig pair wreath linen
Assets -> public/themes/art/zaitun-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l5_lib import *

OUT = outdir("zaitun-syari")
PARTS = sys.argv[1:] or ["branch", "sprig", "pair", "wreath", "linen"]
TOP, UNDER, TWIG = "#5d6d4f", "#a8b4a0", "#6e5e48"

if "branch" in PARTS:
    # long diagonal branch for the cover: enters top-right, droops towards the left
    W, H = 1100, 760
    rng = random.Random(41); nx = Seq(4100)
    art = blank(W, H)
    art = olive_branch(art, W, H, [(1090, 40), (900, 120), (700, 230), (480, 330), (250, 400), (60, 430)], rng, nx,
                       leaf_len=(96, 138), every=3, fruit_every=3, fruit_r=17, twig=TWIG, stem_w=(9, 2), top=TOP, under=UNDER)
    clear()
    art = olive_branch(art, W, H, [(760, 196), (720, 300), (640, 420), (560, 520), (520, 620)], rng, nx,
                       leaf_len=(80, 112), every=4, fruit_every=2, fruit_r=16, twig=TWIG, stem_w=(5, 1.4), top=TOP, under=UNDER)
    clear()
    art = olive_branch(art, W, H, [(330, 385), (280, 300), (200, 240), (110, 220)], rng, nx,
                       leaf_len=(70, 96), every=4, fruit_every=3, fruit_r=12, twig=TWIG, stem_w=(4, 1.2), top=TOP, under=UNDER, fruit=False)
    clear()
    preview(art, "zaitun-branch", tone="#efe9dc")
    save(art, f"{OUT}/branch.webp", max_w=820)

if "sprig" in PARTS:
    # horizontal divider sprig
    W, H = 560, 150
    rng = random.Random(7); nx = Seq(4500)
    art = blank(W, H)
    art = olive_branch(art, W, H, [(30, 80), (180, 70), (340, 76), (520, 66)], rng, nx, leaf_len=(40, 56), every=6, fruit_every=3,
                       fruit_r=9, twig=TWIG, stem_w=(3.5, 1), top=TOP, under=UNDER)
    clear()
    preview(art, "zaitun-sprig", tone="#efe9dc")
    save(art, f"{OUT}/sprig.webp", max_w=340)

if "pair" in PARTS:
    # two olives + two leaves (timeline node / amp)
    W, H = 220, 220
    rng = random.Random(3); nx = Seq(4700)
    art = blank(W, H)
    st = stroke_mask(W, H, curve([(40, 40), (90, 80), (120, 110)], 12), 4, (0.0, 0.3))
    art = G(art, st, TWIG, seed=nx(), density=0.85, edge=0.4, rough=0.8)
    art, _ = olive_leaf(art, W, H, 90, 80, 90, -0.2, rng, nx, top=TOP, under=UNDER, show_under=False, bend=0.3)
    art, _ = olive_leaf(art, W, H, 80, 72, 84, 1.9, rng, nx, top=TOP, under=UNDER, show_under=True, bend=-0.3)
    art, _ = olive_fruit(art, W, H, 118, 140, 20, 1.3, rng, nx)
    art, _ = olive_fruit(art, W, H, 152, 122, 18, 1.1, rng, nx, ripe=False)
    preview(art, "zaitun-pair", tone="#efe9dc")
    save(art, f"{OUT}/pair.webp", max_w=120)

if "wreath" in PARTS:
    # open oval wreath: two branches curving up from the bottom, gap at top
    W, H = 640, 820
    rng = random.Random(12); nx = Seq(4900)
    art = blank(W, H)
    cx, cy, rx, ry = 320, 380, 250, 320
    for side in (-1, 1):
        spine = [(cx - side * 46, cy + ry + 26)] + [(cx + side * rx * math.sin(t), cy + ry * math.cos(t)) for t in [0.25, 0.9, 1.6, 2.3, 2.8]]
        art = olive_branch(art, W, H, spine, rng, nx, leaf_len=(64, 86), every=3, fruit_every=4, fruit_r=12, twig=TWIG,
                           stem_w=(5, 1.4), top=TOP, under=UNDER)
        clear()
    preview(art, "zaitun-wreath", tone="#efe9dc")
    save(art, f"{OUT}/wreath.webp", max_w=420)

if "linen" in PARTS:
    t = linen_tile(512, "#ece6d8", seed=8, warp=0.03, weft=0.025)
    save_texture(t, f"{OUT}/linen.webp", quality=72)
    print("linen", os.path.getsize(f"{OUT}/linen.webp") // 1024, "KB")

kb_total(OUT)
