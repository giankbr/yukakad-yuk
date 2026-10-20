"""Mawar Blush — loose watercolour roses (blush / rose / peach + sage), light from top-left.
Run: python3 -I /tmp/pen/art/themes/mawar-blush.py
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from agentA_lib import *  # noqa

D = f"{OUT}/mawar-blush"
P = "/tmp/pen/nt2-A"
os.makedirs(D, exist_ok=True)
TONE = "#f7e4e1"

BLUSH = ("#f6d3d3", "#e9a7ad", "#b85d6c")
ROSE = ("#f2bcc2", "#de8f9b", "#a5475b")
PEACH = ("#f9dfd2", "#f0b9a3", "#c7735f")
GREENS = [("#a7b99c", "#6f8b68"), ("#b5c4a5", "#7f9875"), ("#93a98a", "#5f7c5a")]


def bouquet():
    W, H = 1000, 820
    rng = random.Random(7); sd = Seeds(200)
    flowers = blank(W, H); area = np.zeros((H, W), np.float32)
    for (x, y, r, t) in [(330, 320, 172, BLUSH), (575, 215, 128, PEACH), (500, 470, 112, ROSE), (175, 520, 92, PEACH)]:
        lay, m = rose(W, H, x, y, r, *t, sd, rng)
        flowers = glaze(flowers, knockout(lay, area, .9, 3))   # later roses tuck behind earlier ones
        area = np.maximum(area, m)
    # buds on thin stems
    stems = blank(W, H)
    for (pts, w) in [([(640, 330), (730, 280), (800, 210), (850, 170)], 7), ([(250, 600), (180, 680), (120, 740)], 6), ([(620, 120), (680, 70), (720, 40)], 5)]:
        lay, _ = stem(W, H, pts, w, "#7f9672", sd)
        stems = glaze(stems, lay)
    for (x, y, s, a, t) in [(850, 172, 34, -0.9, ROSE), (118, 742, 30, 2.2, PEACH), (722, 42, 24, -1.1, BLUSH)]:
        lay, m = bud(W, H, x, y, s, a, t[1], t[2], "#8fa585", sd, rng)
        flowers = glaze(flowers, lay); area = np.maximum(area, m)
    leaves = blank(W, H)
    for i, (x, y, L, a) in enumerate([(300, 470, 250, 2.35), (470, 330, 260, -0.55), (640, 360, 230, 0.35), (250, 220, 230, -2.6),
                                      (430, 160, 190, -1.6), (690, 260, 200, -0.2), (560, 560, 200, 0.9), (90, 470, 170, 3.0),
                                      (760, 310, 150, 0.1), (360, 610, 180, 1.9), (620, 520, 150, 0.4)]):
        ca, cb = GREENS[i % 3]
        lay, _ = leaf(W, H, x, y, L, a, ca, cb, sd, rng, width=0.27, curl=rng.uniform(-.25, .25))
        leaves = glaze(leaves, lay)
    leaves = knockout(glaze(stems, leaves), area, .93, 4)
    art = glaze(leaves, flowers)
    art = glaze(art, pig(dots(W, H, 480, 400, 300, 230, 40, 2, 5.5, rng), "#e2959c", seed=sd(), density=0.5, edge=0.2, bloom=0, rough=1, feather=.5))
    print("bouquet", save_asset(art, f"{D}/bouquet.webp", max_w=520, quality=82))
    preview(art, f"{P}/mb-bouquet.png", TONE)


def sprig():
    W, H = 420, 300
    rng = random.Random(11); sd = Seeds(900)
    lay, m = rose(W, H, 210, 150, 70, *ROSE, sd, rng, petals=8)
    leaves = blank(W, H)
    for (x, y, L, a, g) in [(200, 160, 150, 0.15, 0), (220, 150, 140, 3.0, 1), (210, 140, 100, -1.1, 2), (215, 160, 90, 1.9, 1)]:
        l2, _ = leaf(W, H, x, y, L, a, *GREENS[g], sd, rng, width=0.3)
        leaves = glaze(leaves, l2)
    art = glaze(knockout(leaves, m, .93, 3), lay)
    print("sprig", save_asset(art, f"{D}/sprig.webp", max_w=220, quality=82))
    preview(art, f"{P}/mb-sprig.png", TONE)


def petal():
    W, H = 120, 120
    rng = random.Random(3); sd = Seeds(50)
    m = shape_mask(W, H, deform(petal_pts(18, 62, 86, 34, -0.3, n=14, cup=0.4), rng, 2, .05))
    art = pig(m, "#f2b8bf", "#e59ba6", seed=sd(), density=0.6, edge=0.7, bloom=0.4, rough=3, pad=10)
    print("petal", save_asset(art, f"{D}/petal.webp", max_w=48, quality=80))


def texture():
    save_texture(paper_tile(512, "#fefcfb", seed=21, mottle=0.35, fine=1.0, fiber=1.2, strength=0.8), f"{D}/paper.webp", quality=72)


if __name__ == "__main__":
    which = sys.argv[1:] or ["bouquet", "sprig", "petal", "texture"]
    for w in which:
        globals()[w]()
