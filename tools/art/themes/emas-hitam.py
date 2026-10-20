"""Emas Hitam — pressed gold-foil art-deco pieces on black card (fan sunburst, stepped corner, divider, card grain).
Run: python3 -I /tmp/pen/art/themes/emas-hitam.py
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from agentA_lib import *  # noqa

D = f"{OUT}/emas-hitam"
P = "/tmp/pen/nt2-A"
os.makedirs(D, exist_ok=True)
GOLD = "#c9a352"


def foil_worn(mask, seed, base=GOLD, wear=0.22, rough=0.7):
    """Gold foil with hand-pressed imperfections: slightly wavering edge, tiny bare specks where foil didn't take."""
    h, w = mask.shape
    m = np.clip((gaussian_filter(displace(mask, seed, rough, 12), 0.5) - 0.3) * 2.0, 0, 1)
    f = foil(m, base, seed=seed, emboss=0.5, sparkle=0.04)
    speck = fbm(w, h, seed + 5, 5, 2)
    f[..., 3] *= 1 - wear * np.clip((speck - 0.64) * 5, 0, 1)
    # broad tonal drift so long bars don't look uniformly lit
    drift = 0.9 + 0.2 * fbm(w, h, seed + 9, 160, 2)
    f[..., :3] = np.clip(f[..., :3] * drift[..., None], 0, 1)
    return f


def draw_mask(W, H, fn):
    return mask_from(W, H, fn)


def P_(w, cap=skia.Paint.kRound_Cap):
    return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=w, Style=skia.Paint.kStroke_Style, StrokeCap=cap)


def F_():
    return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)


def wobble_arc(path, cx, cy, r, a0, a1, rng, n=60, amp=0.25):
    for i in range(n):
        t = a0 + (a1 - a0) * i / (n - 1)
        rr = r + rng.gauss(0, amp)
        x, y = cx + math.cos(t) * rr, cy + math.sin(t) * rr
        path.moveTo(x, y) if i == 0 else path.lineTo(x, y)


def fan():
    W, H = 690, 372
    cx, cy = 345, 352
    rng = random.Random(5)

    def draw(cv):
        c = cv.c
        for r, w in [(328, 6), (284, 3.4), (244, 3.4)]:
            p = skia.Path(); wobble_arc(p, cx, cy, r, math.pi, math.tau, rng)
            c.drawPath(p, P_(w))
        # dentil diamonds between the two outer arcs
        for i in range(23):
            t = math.pi + math.pi * (i + 0.5) / 23
            x, y = cx + math.cos(t) * 306, cy + math.sin(t) * 306
            p = skia.Path(); s = 6.5
            p.moveTo(x, y - s); p.lineTo(x + s * .7, y); p.lineTo(x, y + s); p.lineTo(x - s * .7, y); p.close()
            m = skia.Matrix(); m.setRotate(math.degrees(t) + 90, x, y); p.transform(m)
            c.drawPath(p, F_())
        # wedge rays
        n = 15
        for i in range(n):
            t = math.pi + math.pi * (i + 0.5) / n
            long = i % 2 == 0
            r0, r1 = 104, (232 if long else 186)
            hw0, hw1 = (2.2, 9.5) if long else (1.8, 6.5)
            ca, sa = math.cos(t), math.sin(t)
            nx, ny = -sa, ca
            p = skia.Path()
            p.moveTo(cx + ca * r0 + nx * hw0, cy + sa * r0 + ny * hw0)
            p.lineTo(cx + ca * r1 + nx * hw1, cy + sa * r1 + ny * hw1)
            p.lineTo(cx + ca * (r1 + 12) , cy + sa * (r1 + 12))
            p.lineTo(cx + ca * r1 - nx * hw1, cy + sa * r1 - ny * hw1)
            p.lineTo(cx + ca * r0 - nx * hw0, cy + sa * r0 - ny * hw0)
            p.close(); c.drawPath(p, F_())
        # stepped half-sun
        p = skia.Path(); wobble_arc(p, cx, cy, 88, math.pi, math.tau, rng, amp=.4); c.drawPath(p, P_(3.2))
        p = skia.Path(); p.addArc(skia.Rect(cx - 66, cy - 66, cx + 66, cy + 66), 180, 180); p.close(); c.drawPath(p, F_())
        # baseline
        c.drawLine(10, cy + 2, W - 10, cy + 2, P_(4.2, skia.Paint.kButt_Cap))
    m = draw_mask(W, H, draw)
    sun = mask_from(W, H, lambda cv: cv.c.drawCircle(cx, cy, 66, F_()))
    art = foil_worn(m, 31)
    # engraved ring lines on the half-sun (lines cut through foil so it reads pressed, not vector)
    def cut(cv):
        for r in (24, 40, 54):
            cv.c.drawCircle(cx, cy, r, P_(2.0))
    cm = mask_from(W, H, cut) * sun
    art[..., 3] *= 1 - np.clip(gaussian_filter(cm, .6) * 1.2, 0, 1) * 0.85
    print("fan", save_asset(art, f"{D}/fan.webp", max_w=460, quality=84))
    preview_dark(art, f"{P}/eh-fan.png")


def corner():
    W = H = 186
    rng = random.Random(9)

    def draw(cv):
        c = cv.c
        for (o, w) in [(6, 4.2), (22, 2.4)]:
            p = skia.Path()
            k = 46 if o == 6 else 62   # stepped L: the outer line steps in at 46, the inner one at 62
            pts = [(o, H - 4), (o, k), (k, k), (k, o), (W - 4, o)]
            for i, (x, y) in enumerate(pts):
                x += rng.gauss(0, .2); y += rng.gauss(0, .2)
                p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
            c.drawPath(p, P_(w, skia.Paint.kButt_Cap))
        # short diagonal tick from the inner step, ending in a bead
        c.drawLine(62, 62, 92, 92, P_(2.0))
        c.drawCircle(96, 96, 4.5, F_())
        # diamond
        p = skia.Path(); p.moveTo(26, 14); p.lineTo(38, 26); p.lineTo(26, 38); p.lineTo(14, 26); p.close(); c.drawPath(p, F_())
    m = draw_mask(W, H, draw)
    art = foil_worn(m, 41)
    print("corner", save_asset(art, f"{D}/corner.webp", max_w=150, quality=84))
    preview_dark(art, f"{P}/eh-corner.png")


def rule():
    W, H = 620, 52
    cx, cy = 310, 26

    lines = stroke_mask(W, H, [(14 + i * (226 / 30), cy) for i in range(31)], 3.6, taper=(0.9, 0.02))
    lines = np.maximum(lines, stroke_mask(W, H, [(380 + i * (226 / 30), cy) for i in range(31)], 3.6, taper=(0.02, 0.9)))

    def deco(cv):
        c = cv.c
        for sgn in (-1, 1):
            for k, off in enumerate((40, 54)):
                x = cx + sgn * off
                p = skia.Path(); p.moveTo(x + sgn * 8, cy - 9); p.lineTo(x, cy); p.lineTo(x + sgn * 8, cy + 9)
                c.drawPath(p, P_(2.6 - k * 0.6))
        p = skia.Path(); p.moveTo(cx, cy - 22); p.lineTo(cx + 22, cy); p.lineTo(cx, cy + 22); p.lineTo(cx - 22, cy); p.close(); c.drawPath(p, F_())
    m = np.maximum(lines, mask_from(W, H, deco))
    inner = mask_from(W, H, lambda cv: cv.c.drawPath((lambda p: (p.moveTo(cx, cy - 11), p.lineTo(cx + 11, cy), p.lineTo(cx, cy + 11), p.lineTo(cx - 11, cy), p.close(), p)[-1])(skia.Path()), P_(2.0)))
    art = foil_worn(m, 51, wear=0.15)
    art[..., 3] *= 1 - np.clip(inner * 1.2, 0, 1) * 0.8
    print("rule", save_asset(art, f"{D}/rule.webp", max_w=420, quality=84))
    preview_dark(art, f"{P}/eh-rule.png")


def texture():
    """Black card stock: fine fibre + faint mottling (seamless) — used with background-blend screen/normal under the deco lattice."""
    size = 512
    r = np.random.default_rng(77)
    g = lambda s: (lambda a: (a - a.mean()) / (a.std() + 1e-6))(gaussian_filter(r.random((size, size)).astype(np.float32), s, mode="wrap"))
    v = 1 + g(40) * 0.06 + g(0.7) * 0.05 + g((0.5, 6)) * 0.04
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb("#111112"), np.float32)
    save_texture(Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB"), f"{D}/card.webp", quality=70)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["fan", "corner", "rule", "texture"]:
        globals()[w]()
