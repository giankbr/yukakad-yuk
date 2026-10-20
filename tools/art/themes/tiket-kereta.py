"""Tiket Kereta — painted assets: dawn volcano + rice-terrace hero (gouache), painted KA train (separate, glides),
worn navy postmark, inked rail divider, mini loco for the ticket route, cream paper tile.
Run: python3 -I /tmp/pen/art/themes/tiket-kereta.py
Medium: gouache landscape with watercolour sky, ink line details; stamps are worn rubber-stamp ink."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p3_common import *  # noqa

T = "tiket-kereta"
D = outdir(T)
nxt = Seeds(700)
rng = random.Random(77)

NAVY, ORANGE, CREAM = "#20306b", "#f26a21", "#f7f3ec"


def hero():
    W, H = 780, 820
    art = painted_sky(W, H, [(0, "#18244f"), (0.16, "#2a3d7a"), (0.3, "#5a5f95"), (0.4, "#c47a63"), (0.5, "#f0a86a"), (0.58, "#f6c88e"), (0.7, "#d9c7a0"), (1.0, "#9fb08a")], seed=nxt(), streak=0.8, grain=0.6)
    # dawn glow behind the volcano
    art = over(art, glow(dots_mask(W, H, [(430, 360, 90)]), "#ffd08a", radius=90, strength=0.55))
    # distant volcano (two peaks), watercolour, hazy
    vol = shape_mask(W, H, deform([(-40, 470), (180, 330), (330, 250), (400, 236), (470, 262), (560, 330), (700, 420), (820, 470), (820, 520), (-40, 520)], rng, 3, 0.03), smooth=False)
    art = over(art, pigment(vol, "#5a5a86", "#7a6a8e", seed=nxt(), density=0.78, edge=0.25, bloom=0.35, rough=8, feather=2.5, gran=0.2))
    # smoke plume
    for i, (x, y, r) in enumerate([(415, 222, 16), (440, 204, 22), (475, 190, 26), (520, 184, 30)]):
        m = shape_mask(W, H, deform(ellipse_pts(x, y, r * 1.3, r, 10), rng, 2, 0.1))
        art = over(art, pigment(m, "#d9cbc2", "#b9a9a6", seed=nxt(), density=0.22 - i * 0.04, edge=0.1, bloom=0.6, rough=8, feather=6))
    # mid hills in warmer green
    hill = shape_mask(W, H, deform([(-40, 520), (120, 455), (300, 440), (480, 452), (640, 430), (820, 470), (820, 600), (-40, 600)], rng, 3, 0.03), smooth=False)
    art = over(art, gouache_obj(hill, "#5c7a56", "#4a6648", seed=nxt(), rough=3, light=(0.3, -1.0), k=0.25, blur=16, hi="#9fb56f", lo="#2f4530"))
    # rice terraces: stacked bands with slightly wobbly edges
    cols = ["#8fae5f", "#a9bf69", "#7f9f55", "#b7c974", "#6f9450", "#9fb864"]
    for i in range(6):
        y0 = 520 + i * 46
        band = shape_mask(W, H, deform([(-40, y0 + rng.uniform(-6, 6)), (200, y0 - 12), (420, y0 + 8), (620, y0 - 10), (820, y0 + 4), (820, y0 + 70), (-40, y0 + 70)], rng, 3, 0.02), smooth=False)
        art = over(art, gouache_obj(band, cols[i], mix(cols[i], "#4e6b3a", .3), seed=nxt(), rough=3, light=(0.2, -1.0), k=0.2, blur=10, hi="#d5de8f", lo="#36502e"))
        # terrace lip: dark ink-ish line along the top edge
        lip = np.clip(gaussian_filter(band, 1.0) - gaussian_filter(np.roll(band, 4, 0), 1.0), 0, 1)
        art = over(art, pigment(lip, "#35502c", seed=nxt(), density=0.6, edge=0.2, bloom=0, rough=2, feather=0.8))
    # water glints in paddies only
    paddy = (np.mgrid[0:H, 0:W][0] > 560).astype(np.float32)
    art = over(art, speckles(W, H, rng, 70, "#e9f0d8", nxt(), 1.5, 4.0, region=paddy))
    # fading stars high in the dawn sky
    stars = (np.mgrid[0:H, 0:W][0] < 150).astype(np.float32)
    art = over(art, speckles(W, H, rng, 40, "#fff3d6", nxt(), 0.8, 2.0, region=stars))
    # stone viaduct: deck at y≈336-358, piers and arches down to the hills (the train rides on the deck)
    deck = rrect_mask(W, H, -10, 336, W + 20, 24, 2)
    wall = rrect_mask(W, H, -10, 356, W + 20, 120, 2)
    arches = np.zeros((H, W), np.float32)
    for i in range(6):
        cx = 40 + i * 140
        arches = np.maximum(arches, shape_mask(W, H, ellipse_pts(cx, 482, 52, 60, 24)))
        arches = np.maximum(arches, rrect_mask(W, H, cx - 52, 482, 104, 40, 1))
    wall = np.clip(wall - arches, 0, 1)
    via = np.clip(deck + wall, 0, 1)
    via = np.clip(displace(via, nxt(), 1.5, 30), 0, 1)
    art = over(art, gouache_obj(via, "#8d7b66", "#6f5e4c", seed=nxt(), rough=2, light=(-0.4, -0.9), k=0.3, blur=8, hi="#c9b69c", lo="#3a2c20"))
    # stone courses (faint ink lines) and arch shadows
    courses = np.zeros((H, W), np.float32)
    for y in range(372, 470, 14):
        courses = np.maximum(courses, stroke_mask(W, H, [(-10, y + rng.uniform(-1, 1)), (W + 10, y + rng.uniform(-1, 1))], 1.2, (0, 0)))
    art = over(art, clipped(pigment(courses, "#4a3a2c", seed=nxt(), density=0.35, edge=0, bloom=0, rough=1, feather=0.6), wall))
    inner = np.clip(gaussian_filter(arches, 6) - gaussian_filter(arches, 1), 0, 1) * 2
    art = over(art, clipped(pigment(arches, "#3a2c20", seed=nxt(), density=0.5, edge=0, bloom=0, rough=2, feather=3), inner))
    art = over(art, ink_outline(via, "#3a2c20", nxt(), width=2.0, density=0.5, breaks=0.2))
    # ballast + track on the deck
    ballast = rrect_mask(W, H, -10, 330, W + 20, 12, 1)
    art = over(art, gouache_obj(ballast, "#9a8a76", "#7f7060", seed=nxt(), rough=2, k=0.1))
    sleepers = np.zeros((H, W), np.float32)
    for x in range(-10, 800, 18):
        sleepers = np.maximum(sleepers, rrect_mask(W, H, x, 328, 9, 12, 1))
    art = over(art, gouache_paint(sleepers, "#4a3b2e", seed=nxt(), rough=0.8))
    rails = np.maximum(stroke_mask(W, H, [(-40, 331), (820, 330)], 2.4, (0, 0)), stroke_mask(W, H, [(-40, 339), (820, 338)], 2.4, (0, 0)))
    art = over(art, gouache_paint(rails, "#2a2a33", seed=nxt(), rough=0.5, streak=0))
    # a few coconut palms silhouettes on the right
    for px, ph in [(690, 70), (730, 92), (60, 60)]:
        trunk = stroke_mask(W, H, curve([(px, 520), (px + 6, 480), (px + 14, 520 - ph)], 20), 4, (0.05, 0.3))
        fronds = np.zeros((H, W), np.float32)
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.42
            fr = petal_pts(px + 14, 520 - ph, 46, 9, a, 10, cup=0.3)
            fronds = np.maximum(fronds, shape_mask(W, H, fr))
        art = over(art, gouache_obj(np.clip(trunk + fronds, 0, 1), "#2f4a2e", "#1f3522", seed=nxt(), rough=1.5, k=0.15))
    # misty haze between hills and terraces
    haze = shape_mask(W, H, deform(ellipse_pts(390, 470, 520, 30, 16), rng, 3, 0.1))
    art = over(art, pigment(haze, "#f3dcb8", seed=nxt(), density=0.3, edge=0.1, bloom=0.5, rough=10, feather=8))
    preview(art, f"{PREV}/tk-hero.png", NAVY)
    save(art, f"{D}/hero.webp", q=80, trim=False)


def train():
    W, H = 760, 150
    art = blank(W, H)
    a, _ = paint_coach(W, H, 118, 86, 220, rng, nxt, col="#243a6e", col2="#1b2c55", accent=ORANGE)
    art = over(art, a)
    a, _ = paint_coach(W, H, 350, 86, 220, rng, nxt, col="#243a6e", col2="#1b2c55", accent=ORANGE)
    art = over(art, a)
    a, _ = paint_locomotive(W, H, 600, 86, 240, rng, nxt, col="#243a6e", col2="#1b2c55", accent=ORANGE)
    art = over(art, a)
    # couplers
    cp = np.maximum(rrect_mask(W, H, 226, 84, 16, 6, 2), rrect_mask(W, H, 458, 84, 24, 6, 2))
    art = over(art, gouache_paint(cp, "#1d2238", seed=nxt(), rough=0.5, streak=0))
    preview(art, f"{PREV}/tk-train.png", "#f0a86a")
    save(art, f"{D}/train.webp", max_w=720, q=84)


def loco_mini():
    W, H = 160, 90
    a, _ = paint_locomotive(W, H, 80, 42, 120, rng, nxt, col="#243a6e", col2="#1b2c55", accent=ORANGE)
    preview(a, f"{PREV}/tk-loco.png", CREAM)
    save(a, f"{D}/loco.webp", max_w=80, q=84)


def stamp():
    W = H = 300
    art = postmark(W, H, 150, 150, 132, "KA ARGO ASMARA", "EKSEKUTIF CINTA", "SAH", rng, nxt, col="#243a6e", wear=0.5, rot=0.18, center_size=52, date="PERON 1")
    preview(art, f"{PREV}/tk-stamp.png", "#ffffff")
    save(art, f"{D}/stamp.webp", max_w=260, q=82)


def divider():
    """Hand-inked stretch of rail track, slightly curving, with a signal lamp."""
    W, H = 720, 90
    rail1 = curve([(16, 44), (200, 40), (400, 46), (600, 40), (704, 44)], 80)
    rail2 = [(x, y + 14) for x, y in rail1]
    m = np.maximum(stroke_mask(W, H, rail1, 3.0, (0.03, 0.03)), stroke_mask(W, H, rail2, 3.0, (0.03, 0.03)))
    for i in range(0, len(rail1), 4):
        (x, y) = rail1[i]
        m = np.maximum(m, stroke_mask(W, H, [(x + rng.uniform(-1, 1), y - 4), (x + rng.uniform(-1, 1), y + 18)], 4.0, (0.05, 0.05)))
    art = ink(m, "#2b2b33", nxt(), 0.85, 1.0)
    # orange signal dot at the right
    sig = np.maximum(stroke_mask(W, H, [(690, 40), (690, 12)], 3, (0, 0)), dots_mask(W, H, [(690, 10, 7)]))
    art = over(art, ink(sig, ORANGE, nxt(), 0.9, 0.8))
    preview(art, f"{PREV}/tk-divider.png", CREAM)
    save(art, f"{D}/divider.webp", max_w=360, q=82)


def paper_tex():
    t = grain_overlay(256, "#6b4f2a", seed=5, base=0.008, k=1.1, cap=0.06, fiber=0.8, mottle=0.7)
    save(t, f"{D}/paper.webp", q=60, trim=False)


if __name__ == "__main__":
    which = sys.argv[1:] or ["hero", "train", "loco", "stamp", "divider", "paper"]
    for w in which:
        {"hero": hero, "train": train, "loco": loco_mini, "stamp": stamp, "divider": divider, "paper": paper_tex}[w]()
