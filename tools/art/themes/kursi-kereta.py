"""Kursi Kereta — painted assets: violet-dusk sky header with gouache clouds and hill line, painted KA train
(separate, glides), worn postmark, gouache suitcase, subtle screen-paper tile.
Run: python3 -I /tmp/pen/art/themes/kursi-kereta.py
Medium: gouache + watercolour sky; stamps are worn rubber-stamp ink. The app UI itself stays crisp."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p3_common import *  # noqa

T = "kursi-kereta"
D = outdir(T)
nxt = Seeds(900)
rng = random.Random(19)

BLUE, ORANGE = "#3d5be9", "#f7941e"


def hero():
    W, H = 780, 460
    art = painted_sky(W, H, [(0, "#2a44c4"), (0.3, "#4a4fde"), (0.6, "#7a46e0"), (0.82, "#a86ad8"), (1.0, "#e9a37a")], seed=nxt(), streak=0.8, grain=0.6)
    # watercolour cloud wisps (translucent, lighter)
    for cx, cy, rx, ry, col in [(130, 120, 190, 36, "#9ab0ff"), (640, 90, 170, 30, "#b7a9ff"), (420, 200, 230, 34, "#c9b2ff"), (120, 300, 220, 40, "#e0b9f0"), (700, 290, 200, 38, "#f0bfd8")]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=6, flat=0.5)
        art = over(art, pigment(m, col, mix(col, "#ffffff", .4), seed=nxt(), density=0.42, edge=0.3, bloom=0.5, rough=8, feather=3, gran=0.15))
    # gouache cloud puffs, lit from below-right by the warm horizon
    for cx, cy, rx, ry in [(80, 220, 130, 56), (720, 200, 120, 50), (380, 110, 90, 38)]:
        m = cloud_mask(W, H, cx, cy, rx, ry, rng, lobes=5, flat=0.55)
        c = gouache_obj(m, "#f3effc", "#dcd4f3", seed=nxt(), rough=3.0, light=(0.4, 0.9), k=0.35, blur=12, hi="#fff6ea", lo="#8d7fc9")
        c[..., 3] *= 0.92
        art = over(art, c)
    # soft hill line at the bottom + a low sun
    art = over(art, glow(dots_mask(W, H, [(560, 400, 36)]), "#ffd9a6", radius=50, strength=0.55))
    hill = shape_mask(W, H, deform([(-40, 420), (160, 392), (360, 404), (560, 388), (820, 410), (820, 560), (-40, 560)], rng, 3, 0.03), smooth=False)
    art = over(art, gouache_obj(hill, "#4b3f9c", "#3a2f82", seed=nxt(), rough=3, light=(0.2, -1.0), k=0.25, blur=10, hi="#8b6fd0", lo="#221a5c"))
    # rail on the hill crest (the painted train rides here)
    rail = stroke_mask(W, H, curve([(-40, 414), (200, 404), (420, 410), (640, 400), (820, 410)], 60), 2.2, (0, 0))
    art = over(art, gouache_paint(rail, "#2b2550", seed=nxt(), rough=0.5, streak=0))
    art = art[:430]
    preview(art, f"{PREV}/kk-hero.png", "#3d5be9")
    save(art, f"{D}/hero.webp", q=80, trim=False)


def train():
    W, H = 560, 130
    art = blank(W, H)
    a, _ = paint_coach(W, H, 110, 76, 200, rng, nxt, col="#3a52d6", col2="#2c40b4", accent=ORANGE, ink_col="#1c2457", cream="#f6f1e6")
    art = over(art, a)
    a, _ = paint_locomotive(W, H, 340, 76, 220, rng, nxt, col="#3a52d6", col2="#2c40b4", accent=ORANGE, ink_col="#1c2457", cream="#f6f1e6")
    art = over(art, a)
    cp = rrect_mask(W, H, 208, 74, 24, 6, 2)
    art = over(art, gouache_paint(cp, "#1c2457", seed=nxt(), rough=0.5, streak=0))
    preview(art, f"{PREV}/kk-train.png", "#7a46e0")
    save(art, f"{D}/train.webp", max_w=480, q=84)


def stamp():
    W = H = 300
    art = postmark(W, H, 150, 150, 132, "KA CINTA ABADI", "GERBONG CINTA 1", "KURSI", rng, nxt, col="#2f46c9", wear=0.5, rot=-0.2, center_size=46, date="DIKUNCI")
    preview(art, f"{PREV}/kk-stamp.png", "#ffffff")
    save(art, f"{D}/stamp.webp", max_w=260, q=82)


def luggage():
    W, H = 300, 260
    a, _ = paint_suitcase(W, H, 150, 142, 210, rng, nxt, col="#e38a2e", col2="#c26f1c", trim="#f4e2b6", ink_col="#5a3410", stickers=True)
    preview(a, f"{PREV}/kk-luggage.png", "#ffffff")
    save(a, f"{D}/luggage.webp", max_w=220, q=84)


def paper_tex():
    t = grain_overlay(256, "#2f3a7a", seed=11, base=0.004, k=0.8, cap=0.04, fiber=0.3, mottle=0.8)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["hero", "train", "stamp", "luggage", "paper"]
    for w in which:
        {"hero": hero, "train": train, "stamp": stamp, "luggage": luggage, "paper": paper_tex}[w]()
