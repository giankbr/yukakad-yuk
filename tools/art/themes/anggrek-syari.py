"""Anggrek Syari — anggrek bulan (Phalaenopsis amabilis, puspa pesona Indonesia) putih dan ungu dalam cat air di atas
kertas krem bersih: tangkai melengkung dengan kuncup bertingkat, bunga tunggal untuk monogram, ranting kecil pembatas.
Run: python3 -I anggrek-syari.py [part ...]   parts: putih ungu bloom divider     Assets -> public/themes/art/anggrek-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n5_lib import *
import random

OUT = outdir("anggrek-syari")
PARTS = sys.argv[1:] or ["putih", "ungu", "bloom", "divider", "bulan"]
CREAM = "#fbf7f0"


def counter(start):
    c = [start]

    def nx():
        c[0] += 17
        return c[0]
    return nx


def putih():
    W, H = 920, 740
    art = orchid_spray(W, H, [(-10, 250), (150, 175), (380, 160), (600, 240), (770, 390), (860, 520)],
                       [(0.15, 116, -0.32, 0.95), (0.31, 124, 0.12, -0.86), (0.47, 112, 0.06, 0.92), (0.62, 98, 0.5, -0.84), (0.75, 82, 0.38, 0.9)],
                       [(0.85, 24), (0.905, 19), (0.95, 14), (0.99, 10)], 3, "putih", stem_w=7,
                       roots=[([(20, 245), (60, 300), (50, 360), (90, 400)], 5)])
    rng = random.Random(8); nx = counter(900)
    art = knockout(art, np.zeros((H, W), np.float32))
    preview(art, "putih", tone=CREAM)
    return save(art, f"{OUT}/putih.webp", max_w=820, quality=80)


def ungu():
    W, H = 780, 600
    rng = random.Random(5); nx = counter(500)
    leaves = blank(W, H)
    leaves = leaf_broad(leaves, W, H, 770, 560, 300, 54, math.pi * 1.08, rng, nx, bend=-0.3)
    leaves = leaf_broad(leaves, W, H, 770, 575, 250, 46, math.pi * 1.2, rng, nx, cols=("#8aa468", "#56763f"), bend=0.25)
    art = orchid_spray(W, H, [(740, 540), (620, 380), (460, 270), (280, 250), (110, 300)],
                       [(0.22, 104, 0.2, 0.9), (0.4, 100, -0.18, -0.86), (0.57, 90, -0.22, 0.92), (0.71, 74, -0.55, -0.86)],
                       [(0.81, 21), (0.88, 16), (0.94, 12), (0.99, 8)], 11, "ungu", stem_w=6.5)
    art = glaze(leaves, art)
    preview(art, "ungu", tone=CREAM)
    return save(art, f"{OUT}/ungu.webp", max_w=680, quality=80)


def bloom():
    W = H = 340
    rng = random.Random(2); nx = counter(300)
    art = phal(blank(W, H), W, H, 170, 168, 150, rng, nx, kind="putih")
    preview(art, "bloom", tone=CREAM)
    return save(art, f"{OUT}/bloom.webp", max_w=260, quality=82)


def divider():
    W, H = 600, 170
    art = orchid_spray(W, H, [(30, 120), (200, 92), (330, 88), (470, 104), (580, 130)],
                       [(0.47, 52, 0.0, 0.92)],
                       [(0.2, 11), (0.3, 13), (0.66, 13), (0.76, 11), (0.86, 8)], 21, "ungu", stem_w=3.5)
    preview(art, "divider", tone=CREAM)
    return save(art, f"{OUT}/divider.webp", max_w=440, quality=82)


def bulan():
    """Pale lilac full-moon wash (anggrek bulan = moon orchid) that sits behind the names and monograms."""
    W = H = 560
    m = circles(W, H, [(280, 280, 250)])
    art = pigment(m, "#efe6f3", "#e3d6ec", seed=31, density=0.7, edge=0.45, bloom=0.5, gran=0.2, rough=9, mottle=0.6)
    art = glaze(art, pigment(circles(W, H, [(250, 250, 150)]), "#f6eff7", seed=32, density=0.35, edge=0.2, bloom=0.6, rough=12))
    preview(art, "bulan", tone=CREAM)
    return save(art, f"{OUT}/bulan.webp", max_w=440, quality=78)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
