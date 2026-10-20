"""Game Retro — hand-placed pixel art rendered as a *painted* sprite sheet: per-pixel pigment jitter, nearest upscale,
faint CRT scanlines + ink speckle. Cover castle scene, coin, heart, item-shop sprites (rice cooker, vacuum bot, sofa).
Run: python3 -I /tmp/pen/art/themes/game-retro.py [castle|sprites]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p4_lib import *  # noqa

T = "game-retro"
D = outdir(T)
rng = random.Random(42)


class Pix:
    def __init__(self, w, h, bg=None):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.float32)
        if bg:
            self.a[..., :3] = hex_rgb(bg); self.a[..., 3] = 1

    def put(self, x, y, col, a=1.0):
        if 0 <= x < self.w and 0 <= y < self.h:
            c = np.array(hex_rgb(col), np.float32)
            self.a[y, x, :3] = self.a[y, x, :3] * (1 - a) + c * a
            self.a[y, x, 3] = max(self.a[y, x, 3], a)

    def rect(self, x, y, w, h, col, dither=None):
        for j in range(y, y + h):
            for i in range(x, x + w):
                if dither and (i + j) % 2:
                    self.put(i, j, dither)
                else:
                    self.put(i, j, col)

    def hline(self, x0, x1, y, col):
        for i in range(x0, x1 + 1):
            self.put(i, y, col)

    def vline(self, x, y0, y1, col):
        for j in range(y0, y1 + 1):
            self.put(x, j, col)

    def disc(self, cx, cy, r, col):
        for j in range(int(cy - r - 1), int(cy + r + 2)):
            for i in range(int(cx - r - 1), int(cx + r + 2)):
                if (i - cx) ** 2 + (j - cy) ** 2 <= r * r:
                    self.put(i, j, col)

    def poly(self, pts, col):
        m = shape_mask(self.w, self.h, pts, smooth=False)
        c = np.array(hex_rgb(col), np.float32)
        sel = m > 0.5
        self.a[sel, :3] = c; self.a[sel, 3] = 1

    def painted(self, k, seed=1, jitter=0.045, crt_=True, **kw):
        """Pigment jitter per pixel, upscale, CRT finish."""
        r = np.random.default_rng(seed)
        j = 1 + (r.random((self.h, self.w, 1)).astype(np.float32) - 0.5) * 2 * jitter
        # slight hue drift blotches (like uneven gouache)
        blot = (fbm(self.w, self.h, seed + 2, 6, 2)[..., None] - 0.5) * jitter * 1.2
        out = self.a.copy()
        out[..., :3] = np.clip(out[..., :3] * j + blot, 0, 1)
        up = pix_up(out, k)
        return crt(up, seed=seed, **kw) if crt_ else up


# ---------- cover: castle on a hill by the water ----------
def castle():
    W, H = 160, 172
    p = Pix(W, H)
    # sky bands (dithered transitions)
    bands = ["#0b0622", "#120a34", "#1a1040", "#22164f", "#2a1b5c", "#33246a"]
    edges = [0, 34, 64, 90, 110, 126, 172]
    for i, c in enumerate(bands):
        y0, y1 = edges[i], edges[i + 1]
        p.rect(0, y0, W, y1 - y0, c)
        if i + 1 < len(bands):
            p.rect(0, y1 - 3, W, 3, c, dither=bands[i + 1])
    # stars
    for _ in range(70):
        x, y = rng.randrange(W), rng.randrange(0, 100)
        p.put(x, y, rng.choice(["#ffffff", "#e8e3ff", "#b9a8f0", "#fff3b0"]))
    for (x, y) in [(22, 18), (120, 12), (140, 44), (60, 30)]:
        p.put(x, y, "#ffffff"); p.put(x - 1, y, "#b9a8f0"); p.put(x + 1, y, "#b9a8f0"); p.put(x, y - 1, "#b9a8f0"); p.put(x, y + 1, "#b9a8f0")
    # moon (top-left) with craters
    p.disc(30, 44, 15, "#f6e9b0")
    p.disc(32, 42, 13, "#fff7cf")
    for (x, y, r) in [(26, 48, 3), (36, 38, 2), (34, 50, 2)]:
        p.disc(x, y, r, "#e9d990")
    # distant hills (purple)
    p.poly([(0, 118), (20, 104), (48, 110), (78, 98), (110, 106), (134, 96), (160, 104), (160, 140), (0, 140)], "#2b1e5e")
    p.poly([(0, 126), (26, 118), (56, 122), (92, 112), (124, 120), (160, 114), (160, 140), (0, 140)], "#221650")
    # the castle hill
    p.poly([(28, 140), (46, 112), (70, 100), (104, 98), (126, 108), (142, 126), (150, 140)], "#3b2a66")
    p.poly([(38, 140), (56, 118), (78, 108), (104, 106), (122, 114), (136, 132), (142, 140)], "#4a3578")
    # castle: main keep + towers (dark with lit windows)
    stone, stone_d, stone_l = "#4b3f7a", "#372c5e", "#6b5aa0"
    def tower(x, y, w, h):
        p.rect(x, y, w, h, stone)
        p.vline(x, y, y + h, stone_d)
        p.vline(x + w - 1, y, y + h, stone_l)
        for i in range(0, w, 2):   # crenels
            p.rect(x + i, y - 2, 1, 2, stone)
        p.hline(x, x + w - 1, y, stone_l)
    tower(60, 70, 10, 42); tower(104, 66, 10, 46); tower(80, 54, 14, 58)
    p.rect(66, 84, 44, 30, stone)
    p.hline(66, 109, 84, stone_l)
    for i in range(66, 110, 2):
        p.rect(i, 82, 1, 2, stone)
    # brick courses (dithered mortar) on keep + towers
    for (x0, y0, w0, h0) in [(60, 72, 10, 40), (104, 68, 10, 44), (80, 56, 14, 56), (66, 86, 44, 28)]:
        for j in range(y0 + 2, y0 + h0, 4):
            off = 0 if (j // 4) % 2 else 2
            for i in range(x0 + 1 + off, x0 + w0 - 1, 4):
                p.put(i, j, stone_d)
                if rng.random() < .35:
                    p.put(i + 1, j, "#41356c")
    # winding path from the gate
    for k, (x, y) in enumerate([(88, 114), (87, 117), (85, 120), (82, 123), (80, 126), (79, 129), (81, 132), (84, 135), (86, 138)]):
        p.hline(x - 2, x + 2, y, "#6b5590"); p.hline(x - 2, x + 2, y + 1, "#5a4682"); p.put(x - 3, y, "#3b2a66")
    # torches by the path
    for (x, y) in [(78, 118), (96, 118), (76, 130)]:
        p.vline(x, y, y + 3, "#2a1b4a"); p.put(x, y - 1, "#ffb340"); p.put(x, y - 2, "#ffe17a")
    # gate
    p.rect(84, 100, 8, 14, "#1a1040"); p.rect(85, 98, 6, 2, "#1a1040")
    p.rect(86, 104, 4, 10, "#f0a640"); p.rect(87, 106, 2, 8, "#ffd93d")
    # flags
    for (x, y) in [(86, 48), (64, 66), (108, 62)]:
        p.vline(x, y, y + 6, "#b9a8f0"); p.rect(x + 1, y, 4, 3, "#ff2e97")
    # windows
    for (x, y) in [(63, 78), (63, 90), (107, 74), (107, 86), (107, 98), (84, 62), (89, 62), (84, 72), (89, 72), (72, 92), (100, 92), (72, 102), (100, 102)]:
        p.rect(x, y, 2, 3, "#ffd93d"); p.put(x, y, "#fff6c2")
    # pine trees on the hill
    for (x, y, h) in [(44, 136, 12), (52, 134, 10), (132, 134, 11), (140, 138, 9), (34, 140, 8), (148, 140, 8)]:
        for k in range(h):
            w = max(1, (k * 5) // h + 1)
            p.hline(x - w // 2, x + w // 2, y - h + k, "#120b30" if k % 3 else "#1b1240")
        p.vline(x, y, y + 2, "#120b30")
    # water with moon-path reflection
    p.rect(0, 140, W, 32, "#141a4a", dither="#1a2258")
    for j in range(142, 172, 3):
        for i in range(0, W, rng.choice([5, 7, 9])):
            p.put(i + rng.randrange(3), j, "#2a3a7a")
    for j in range(142, 172, 2):
        x = 34 + rng.randint(-6, 6)
        p.hline(x - rng.randint(2, 6), x + rng.randint(2, 6), j, "#bfb78a" if j % 4 else "#e9dc98")
    for j in range(142, 160, 3):
        x = 88 + rng.randint(-8, 8)
        p.hline(x - 1, x + 1, j, "#9a7a3a")
    # fireflies
    for _ in range(14):
        x, y = rng.randrange(20, 150), rng.randrange(100, 150)
        p.put(x, y, "#39ff88")
    art = p.painted(4, seed=3, jitter=0.05, scan=0.12, ink=0.05, bleed=0.5, grain=0.05, period=4)
    save_rgb(art, f"{D}/castle.webp", q=82)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/gr-castle.png")


# ---------- sprites ----------
def coin():
    p = Pix(16, 16)
    p.disc(7.5, 7.5, 7, "#b8860b")
    p.disc(7.5, 7.5, 5.6, "#ffd93d")
    p.rect(5, 4, 2, 8, "#b8860b"); p.rect(7, 4, 2, 1, "#b8860b"); p.rect(7, 11, 2, 1, "#b8860b"); p.rect(8, 7, 1, 1, "#b8860b")
    p.put(4, 3, "#fff3b0"); p.put(3, 4, "#fff3b0"); p.put(5, 2, "#fff3b0")
    return p


def heart():
    p = Pix(16, 14)
    rows = ["..XXX...XXX.....", ".XXXXX.XXXXX....", "XXXXXXXXXXXXX...", "XXXXXXXXXXXXX...", "XXXXXXXXXXXXX...", ".XXXXXXXXXXX....", "..XXXXXXXXX.....", "...XXXXXXX......", "....XXXXX.......", ".....XXX........", "......X........."]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == "X":
                p.put(i, j + 1, "#ff2e97")
    for (x, y) in [(2, 2), (3, 2), (2, 3)]:
        p.put(x, y, "#ff8ac3")
    for j, r in enumerate(rows):   # dark outline bottom-right
        for i, ch in enumerate(r):
            if ch == "X" and (j + 1 < len(rows) and (i >= len(rows[j + 1]) or rows[j + 1][i] != "X")):
                p.put(i, j + 1, "#b3145f")
    return p


def rice_cooker():
    p = Pix(24, 24)
    p.rect(4, 8, 16, 12, "#e8e6f0"); p.rect(4, 8, 16, 1, "#ffffff"); p.rect(4, 19, 16, 1, "#9a97ad")
    p.rect(5, 5, 14, 3, "#c9c6d8"); p.rect(10, 3, 4, 2, "#5a4a99"); p.rect(11, 2, 2, 1, "#5a4a99")
    p.rect(6, 12, 12, 1, "#5a4a99"); p.rect(8, 15, 3, 2, "#ff2e97"); p.rect(13, 15, 3, 2, "#39ff88")
    p.rect(3, 11, 1, 4, "#9a97ad"); p.rect(20, 11, 1, 4, "#9a97ad")
    p.rect(6, 20, 3, 1, "#3a3a4a"); p.rect(15, 20, 3, 1, "#3a3a4a")
    return p


def vacuum_bot():
    p = Pix(24, 24)
    p.disc(11.5, 13.5, 9, "#4deeea"); p.disc(11.5, 13.5, 7.4, "#2fb8b5"); p.disc(11.5, 12.5, 6, "#4deeea")
    p.rect(9, 9, 5, 2, "#1a1040"); p.rect(10, 13, 3, 3, "#ffd93d"); p.put(11, 14, "#fff6c2")
    p.rect(5, 21, 13, 1, "#1a1040"); p.rect(6, 22, 11, 1, "#5a4a99")
    p.rect(2, 12, 2, 4, "#ff2e97"); p.rect(19, 12, 2, 4, "#ff2e97")
    p.put(11, 3, "#39ff88"); p.put(11, 4, "#39ff88"); p.put(10, 2, "#39ff88"); p.put(12, 2, "#39ff88")
    return p


def sofa():
    p = Pix(24, 24)
    p.rect(3, 7, 18, 8, "#ff2e97"); p.rect(3, 7, 18, 1, "#ff8ac3")
    p.rect(5, 9, 6, 5, "#ff5fae"); p.rect(13, 9, 6, 5, "#ff5fae")
    p.rect(1, 12, 3, 7, "#c81e7a"); p.rect(20, 12, 3, 7, "#c81e7a")
    p.rect(3, 15, 18, 4, "#e0238a"); p.rect(4, 16, 16, 1, "#ff5fae")
    p.rect(4, 19, 2, 2, "#5a3a1e"); p.rect(18, 19, 2, 2, "#5a3a1e")
    return p


def sprites():
    for name, fn, k in [("coin", coin, 6), ("heart", heart, 6), ("rice-cooker", rice_cooker, 6), ("vacuum-bot", vacuum_bot, 6), ("sofa", sofa, 6)]:
        p = fn()
        art = p.painted(k, seed=5, jitter=0.06, scan=0.08, ink=0.04, bleed=0.35, grain=0.04, period=3)
        save(art, f"{D}/{name}.webp", q=86, trim=False)
    # preview sheet
    sheet = Image.new("RGB", (120 * 5, 150), "#241656")
    for i, name in enumerate(["coin", "heart", "rice-cooker", "vacuum-bot", "sofa"]):
        im = Image.open(f"{D}/{name}.webp").convert("RGBA")
        sheet.paste(im, (i * 120 + 10, 10), im)
    sheet.save(f"{PREV}/gr-sprites.png")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["castle", "sprites"]:
        {"castle": castle, "sprites": sprites}[w]()
