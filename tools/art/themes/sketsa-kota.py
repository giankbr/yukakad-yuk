"""Sketsa Kota — urban-sketcher pen line + loose watercolour wash of an original Indonesian old-town street corner:
colonial-era shophouses (a curved Dutch gable, arched shopfronts, louvred teal shutters, a rounded corner building with a
little dome), a cast-iron street lamp, overhead wires, a flame tree and a cobbled street. Lines overshoot at corners and
the washes run past them, leaving white paper, exactly like a quick sketchbook page.
Also: a skyline strip of rooftops, an arched window sketch, colour swatch blots (divider + single), a paper tile.
Run: python3 -I sketsa-kota.py [part ...]   parts: scene skyline window swatches swatch paper
Assets -> public/themes/art/sketsa-kota/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o2_lib import *  # noqa

OUT = outdir("sketsa-kota")
PARTS = sys.argv[1:] or ["scene", "skyline", "window", "swatches", "swatch", "paper"]
INKC = "#2b2a30"
OCHRE, CREAM, PINK, BLUEGREY = "#e7bf7f", "#efdcb8", "#e3a58a", "#b7c8cf"
ROOF, TEAL, SHADOW, SKY, LEAF = "#c0674a", "#4f8f8a", "#8b86a8", "#9cc3dc", "#7ea35c"


class Sketch:
    """Collect pen segments and washes, then render: washes (misregistered, glazed) under the ink."""

    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.rng = random.Random(seed)
        self.nx = Seq(seed * 10)
        self.segs = []
        self.fine = []
        self.art = blank(W, H)

    def line(self, a, b, w=None):
        self.segs.append((a, b) if w is None else (a, b, w))

    def poly(self, pts, closed=True, w=None):
        n = len(pts)
        for i in range(n if closed else n - 1):
            self.line(pts[i], pts[(i + 1) % n], w)

    def box(self, x0, y0, x1, y1, w=None):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], True, w)

    def curve(self, pts, w=1.8):
        self.fine.append((curve(pts, 40), w, (0.08, 0.12)))

    def arch(self, cx, base, r, h=None, w=None):
        h = h or r
        pts = [(cx - r, base)] + [(cx - r * math.cos(t), base - h * math.sin(t)) for t in np.linspace(0, math.pi, 14)] + [(cx + r, base)]
        self.fine.append((pts, w or 1.7, (0.06, 0.1)))

    def hatch(self, x0, y0, x1, y1, step=7, ang=0.9, w=1.0, clip=None):
        """Loose parallel pen hatching inside a box (diagonal)."""
        L = (x1 - x0) + (y1 - y0)
        k = -L
        while k < L:
            a = (x0 + k, y1); b = (x0 + k + (y1 - y0) / math.tan(ang), y0)
            # clip to box horizontally
            if b[0] > x0 and a[0] < x1:
                ax, bx = max(x0, a[0]), min(x1, b[0])
                ty = lambda x: y1 - (x - a[0]) * math.tan(ang)
                self.segs.append(((ax, ty(ax)), (bx, ty(bx)), w))
            k += step * self.rng.uniform(0.8, 1.25)

    def wash(self, pts, col, col2=None, shift=8, dens=0.75, rough=5, bloom=0.4, smooth=False, mask=None):
        dx, dy = self.rng.uniform(-shift, shift), self.rng.uniform(-shift, shift)
        m = mask if mask is not None else poly(self.W, self.H, [(x + dx, y + dy) for x, y in pts], smooth=smooth)
        m = displace(m, self.nx(), rough, 26)
        self.art = G(self.art, m, col, col2 or mix_hex(col, "#ffffff", 0.25), seed=self.nx(), density=dens, edge=0.75, bloom=bloom,
                     rough=rough * 0.6, feather=1.0, gran=0.35)

    def render(self, width=1.9, over=7, amp=0.9):
        items = pen_items(self.segs, self.rng, width=width, over=over, amp=amp) + self.fine
        m = strokes(self.W, self.H, items)
        self.art = INK(self.art, m, INKC, seed=self.nx(), alpha=0.9)
        return self.art


def scene():
    W, H = 780, 820
    S = Sketch(W, H, 7)
    r = S.rng
    G0 = 640  # ground line
    # ── washes first (loose, misregistered) ──
    S.wash([(380, 20), (780, 0), (780, 250), (640, 230), (520, 160)], SKY, "#b9d6e8", shift=14, dens=0.55, rough=12, bloom=0.6, smooth=True)
    S.wash([(0, 330), (250, 300), (250, 640), (0, 668)], OCHRE, shift=10, dens=0.7)                   # building A
    S.wash([(250, 232), (300, 210), (340, 176), (395, 160), (450, 176), (490, 210), (540, 232), (540, 640), (250, 640)], PINK, shift=10, dens=0.72)  # B
    S.wash([(540, 200), (780, 200), (780, 640), (540, 640)], CREAM, shift=10, dens=0.7)                # C
    S.wash([(610, 120), (650, 96), (690, 120), (690, 200), (610, 200)], BLUEGREY, shift=6, dens=0.7)   # dome tower
    S.wash([(-10, 640), (780, 640), (780, 820), (-10, 820)], "#bcb6ae", "#d6d0c6", shift=6, dens=0.55, rough=10, bloom=0.6)  # street
    # awnings / roofs terracotta
    S.wash([(0, 470), (250, 452), (262, 486), (0, 512)], ROOF, shift=6, dens=0.75)
    S.wash([(540, 432), (780, 432), (790, 470), (530, 470)], "#3f7f7a", "#5d9893", shift=6, dens=0.75)
    # shutters teal
    for x in (282, 370, 458):
        S.wash([(x, 290), (x + 56, 290), (x + 56, 392), (x, 392)], TEAL, shift=5, dens=0.6, rough=3)
    for x in (580, 668):
        S.wash([(x, 270), (x + 50, 270), (x + 50, 370), (x, 370)], TEAL, shift=5, dens=0.55, rough=3)
    # tree on the left (flame tree: green with red-orange blossoms)
    tm = ellipses(W, H, [(80, 220, 120, 70, -8), (170, 170, 90, 60, 10), (30, 300, 70, 50, 0), (210, 250, 60, 40, 0)])
    S.wash(None, LEAF, "#a6c06f", mask=tm, dens=0.7, rough=14, bloom=0.6)
    bl = circles(W, H, [(r.uniform(-10, 260), r.uniform(130, 300), r.uniform(5, 11)) for _ in range(40)]) * gaussian_filter(tm, 6)
    S.wash(None, "#e0573a", "#f08a3c", mask=bl, dens=0.85, rough=3, bloom=0.2)
    # shadows: glaze on right return walls, under awnings, the dark shop interiors
    S.wash([(0, 512), (262, 486), (250, 520), (0, 540)], SHADOW, shift=4, dens=0.5)
    for cx in (310, 395, 480):
        S.wash([(cx - 30, 640), (cx - 30, 520), (cx, 492), (cx + 30, 520), (cx + 30, 640)], "#5e5770", shift=4, dens=0.6, rough=3)
    S.wash([(540, 470), (780, 470), (780, 520), (540, 500)], SHADOW, shift=4, dens=0.45)
    S.wash([(560, 640), (600, 520), (640, 520), (640, 640)], "#5e5770", shift=4, dens=0.55, rough=3)
    S.wash([(-10, 640), (300, 640), (240, 690), (-10, 700)], SHADOW, shift=6, dens=0.35, rough=8)
    clear()
    # ── pen ──
    # building A (receding to the left)
    S.poly([(0, 330), (250, 300), (250, 640), (0, 668)], closed=False)
    S.line((0, 318), (256, 288)); S.line((0, 470), (250, 452)); S.line((0, 512), (262, 486)); S.line((250, 452), (262, 486))
    for x in (30, 100, 170):
        t = x / 250
        S.box(x, 360 - t * 26, x + 46, 430 - t * 22)
        S.line((x + 23, 360 - t * 26), (x + 23, 430 - t * 22), 1.2)
    for x in (20, 120):
        S.box(x, 540 - x * 0.1, x + 70, 650 - x * 0.08)
    S.hatch(0, 512, 250, 540, step=8, w=0.9)
    # building B with the curved gable
    S.curve([(250, 232), (300, 214), (336, 180), (395, 158), (454, 180), (490, 214), (540, 232)], 2.0)
    S.curve([(270, 232), (312, 214), (344, 190), (395, 174), (446, 190), (478, 214), (520, 232)], 1.2)
    S.line((250, 232), (540, 232)); S.line((246, 246), (546, 246)); S.line((250, 232), (250, 640)); S.line((540, 232), (540, 640))
    S.arch(395, 214, 14, 16, 1.4)
    S.line((250, 420), (540, 420)); S.line((244, 430), (548, 430))
    for x in (282, 370, 458):
        S.box(x, 290, x + 56, 392)
        S.line((x + 28, 290), (x + 28, 392), 1.1)
        for yy in range(300, 390, 9):
            S.line((x + 4, yy), (x + 26, yy), 0.8); S.line((x + 30, yy), (x + 52, yy), 0.8)
        S.line((x - 6, 284), (x + 62, 284), 1.4)
    # balcony rail
    S.line((262, 404), (528, 404), 1.4)
    for x in range(266, 528, 10):
        S.line((x, 404), (x, 420), 0.9)
    for cx in (310, 395, 480):
        S.arch(cx, 520, 30, 30, 1.8)
        S.line((cx - 30, 520), (cx - 30, 640)); S.line((cx + 30, 520), (cx + 30, 640))
    # building C, rounded corner + dome tower
    S.line((540, 200), (780, 200)); S.line((536, 214), (790, 214)); S.line((540, 200), (540, 640))
    S.curve([(610, 200), (610, 130), (650, 96), (690, 130), (690, 200)], 1.8)
    S.line((650, 96), (650, 70), 1.4); S.curve([(642, 78), (650, 70), (658, 78)], 1.2)
    S.box(632, 140, 668, 190)
    for x in (580, 668):
        S.box(x, 270, x + 50, 370)
        S.line((x + 25, 270), (x + 25, 370), 1.0)
        S.arch(x + 25, 270, 25, 16, 1.4)
    S.line((540, 432), (780, 432)); S.line((530, 470), (790, 470))
    for x in range(548, 780, 26):
        S.line((x, 432), (x - 4, 470), 1.0)
    S.box(560, 520, 640, 640); S.box(680, 520, 760, 600)
    S.line((720, 520), (720, 600), 1.0); S.line((680, 560), (760, 560), 1.0)
    S.hatch(540, 470, 780, 500, step=9, w=0.9)
    # street: kerb, cobbles, perspective lines
    S.line((-10, 640), (790, 640)); S.line((-10, 652), (790, 652), 1.2)
    for k in range(9):
        y = 680 + k * 16 + k * k * 1.5
        x = r.uniform(-40, 500)
        S.line((x, y), (x + r.uniform(40, 120), y + r.uniform(-1, 1)), 0.9)
    for k in range(26):
        x, y = r.uniform(20, 760), r.uniform(670, 800)
        S.curve([(x, y), (x + 5, y - 2), (x + 10, y)], 0.9)
    # overhead wires
    S.curve([(-10, 190), (200, 214), (420, 216), (602, 250)], 1.2)
    S.curve([(602, 250), (700, 236), (790, 224)], 1.2)
    S.curve([(-10, 150), (300, 180), (602, 236)], 1.0)
    # tree: loose scribble trunk + a few leaf scribbles
    S.line((150, 330), (140, 250), 2.4); S.line((140, 250), (100, 200), 1.6); S.line((142, 256), (190, 196), 1.6)
    for _ in range(26):
        x, y = r.uniform(0, 250), r.uniform(150, 300)
        S.curve([(x, y), (x + 6, y - 5), (x + 12, y), (x + 18, y - 4)], 0.9)
    # signboards (blank boards with a scribble where letters would be)
    S.box(296, 438, 494, 466, 1.6)
    S.curve([(312, 452), (322, 446), (332, 456), (344, 446), (356, 454), (370, 448), (384, 456), (398, 446), (412, 454), (426, 448), (440, 455), (456, 447), (476, 452)], 1.1)
    S.box(20, 474, 120, 498, 1.3)
    S.curve([(30, 487), (42, 482), (54, 490), (66, 482), (80, 489), (96, 483), (110, 487)], 1.0)
    # potted plants at the shop doors
    pots = ellipses(W, H, [(258, 618, 16, 22, 0), (528, 616, 18, 24, 0), (650, 610, 14, 18, 0)])
    S.wash(None, LEAF, "#5f8a45", mask=pots, dens=0.75, rough=6)
    for cx in (258, 528, 650):
        S.poly([(cx - 10, 640), (cx - 12, 626), (cx + 12, 626), (cx + 10, 640)], closed=True, w=1.4)
        S.curve([(cx - 12, 620), (cx - 6, 600), (cx, 590), (cx + 6, 602), (cx + 12, 618)], 1.0)
    art = S.render(width=1.9)
    # the lamp stands in front: knock out what is behind it, then wash + ink it
    lm = np.maximum(rect(W, H, 592, 226, 612, 794), poly(W, H, [(572, 302), (632, 302), (634, 258), (602, 232), (570, 258)]))
    lm = np.maximum(lm, rect(W, H, 584, 756, 620, 796))
    art = knockout(art, lm, amount=1.0, grow=1.2)
    art = G(art, lm * (1 - poly(W, H, [(584, 298), (620, 298), (626, 264), (578, 264)])), "#55565f", "#6c6e78", seed=S.nx(), density=0.6, edge=0.5, rough=1.5, feather=0.6)
    S.art = art; S.segs = []; S.fine = []
    # the lamp in the foreground
    S.line((598, 790), (598, 300), 2.4); S.line((606, 790), (606, 300), 1.6)
    S.box(588, 760, 616, 792, 2.0)
    S.poly([(584, 300), (620, 300), (628, 262), (576, 262)], closed=True, w=2.0)
    S.poly([(576, 262), (602, 238), (628, 262)], closed=False, w=2.0)
    S.line((602, 238), (602, 226), 1.6)
    S.curve([(606, 330), (640, 320), (660, 336)], 1.4)
    art = S.render(width=1.9)
    # lamp glass glow (a small warm wash after the ink)
    art = G(art, poly(W, H, [(586, 296), (618, 296), (624, 266), (580, 266)]), "#f6d36a", seed=S.nx(), density=0.75, edge=0.4, rough=1, feather=0.6)
    # vignette: the sketch dissolves into the page at the edges, like a sketchbook study
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx, W - xx) * 1.0, (H - yy) * 1.3) / 110.0
    v = np.clip(d + (fbm(W, H, 99, 46, 3) - 0.5) * 1.3 - 0.15, 0, 1)
    art[..., 3] *= v
    return art


def part_scene():
    art = scene()
    preview(art, "sk-scene", tone="#f5efe2")
    rgb_save(comp_rgb(np.ones(art.shape[:2] + (3,), np.float32), art), f"{OUT}/scene.webp", quality=80, size=(780, 820))  # opaque on white: shown with mix-blend-mode multiply
    clear()


def part_skyline():
    W, H = 900, 260
    S = Sketch(W, H, 21)
    r = S.rng
    x = -10
    roofs = []
    cols = [OCHRE, PINK, CREAM, BLUEGREY, "#d9b38e"]
    while x < W:
        w = r.uniform(80, 140); h = r.uniform(90, 170)
        top = H - h
        kind = r.choice(["flat", "gable", "pitch", "flat"])
        if kind == "gable":
            pts = [(x, H), (x, top + 20), (x + w * 0.25, top + 6), (x + w * 0.5, top - 14), (x + w * 0.75, top + 6), (x + w, top + 20), (x + w, H)]
        elif kind == "pitch":
            pts = [(x, H), (x, top + 26), (x + w * 0.5, top - 6), (x + w, top + 26), (x + w, H)]
        else:
            pts = [(x, H), (x, top), (x + w, top), (x + w, H)]
        roofs.append((pts, x, w, top, kind))
        S.wash(pts, r.choice(cols), shift=8, dens=0.6)
        x += w + r.uniform(-6, 4)
    clear()
    for pts, x, w, top, kind in roofs:
        S.poly(pts[1:-1], closed=False)
        S.line(pts[0], pts[1]); S.line(pts[-2], pts[-1])
        for k in range(r.randint(1, 3)):
            wx = x + 14 + k * (w - 28) / 3
            S.box(wx, top + 40, wx + 18, top + 72, 1.2)
    S.curve([(-10, 60), (300, 92), (600, 84), (910, 50)], 1.1)
    art = S.render(width=1.7)
    art[..., 3] *= np.clip(ygrad(W, H, 0, 40) + 0.0, 0, 1)
    preview(art, "sk-skyline", tone="#f5efe2")
    rgb_save(comp_rgb(np.ones(art.shape[:2] + (3,), np.float32), art), f"{OUT}/skyline.webp", quality=74, size=(600, 173))
    clear()


def part_window():
    W, H = 300, 380
    S = Sketch(W, H, 33)
    S.wash([(40, 380), (40, 140), (150, 40), (260, 140), (260, 380)], PINK, shift=8, dens=0.65)
    S.wash([(80, 360), (80, 160), (150, 96), (220, 160), (220, 360)], TEAL, shift=6, dens=0.6, rough=3)
    S.wash([(60, 380), (240, 380), (240, 360), (60, 360)], "#8b86a8", shift=4, dens=0.5)
    clear()
    S.arch(150, 160, 70, 64, 2.2)
    S.line((80, 160), (80, 362)); S.line((220, 160), (220, 362)); S.line((150, 96), (150, 362), 1.4)
    for y in range(176, 356, 12):
        S.line((86, y), (144, y), 0.9); S.line((156, y), (214, y), 0.9)
    S.line((56, 366), (244, 366), 2.0); S.line((50, 378), (250, 378), 1.4)
    S.arch(150, 160, 92, 84, 1.4)
    art = S.render(width=2.0)
    preview(art, "sk-window", tone="#f5efe2")
    save(art, f"{OUT}/window.webp", max_w=150, quality=82)
    clear()


def blot(art, W, H, cx, cy, r, col, nx, rng):
    pts = ellipse_pts(cx, cy, r * rng.uniform(0.9, 1.1), r * rng.uniform(0.75, 0.95), 12, rng.uniform(0, 3))
    m = displace(poly(W, H, pts, smooth=True), nx(), r * 0.18, r * 0.6)
    return G(art, m, col, mix_hex(col, "#ffffff", 0.3), seed=nx(), density=0.85, edge=0.9, bloom=0.5, rough=r * 0.08, feather=0.8, gran=0.4)


def part_swatches():
    W, H = 720, 140
    rng = random.Random(5); nx = Seq(2400)
    art = blank(W, H)
    S = Sketch(W, H, 41)
    S.art = art
    for i, col in enumerate([ROOF, OCHRE, TEAL, SKY]):
        S.art = blot(S.art, W, H, 246 + i * 76, 70, 32, col, nx, rng)
    S.curve([(20, 76), (120, 70), (200, 74)], 1.8)
    S.curve([(520, 72), (610, 68), (700, 74)], 1.8)
    art = S.render()
    preview(art, "sk-swatches", tone="#f5efe2")
    save(art, f"{OUT}/swatches.webp", max_w=340, quality=82)
    clear()


def part_swatch():
    W, H = 140, 140
    rng = random.Random(8); nx = Seq(2600)
    art = blot(blank(W, H), W, H, 70, 70, 48, ROOF, nx, rng)
    preview(art, "sk-swatch", tone="#f5efe2")
    save(art, f"{OUT}/swatch.webp", max_w=56, quality=82)
    clear()


def part_paper():
    im = paper(384, 384, "#f6f0e3", seed=17, fiber=0.9, mottle=0.0)
    save_texture(im, f"{OUT}/paper.webp", quality=70)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
