"""Koleksi Kupu — a museum butterfly case: six invented specimens painted in gouache with ink veins, a walnut frame
tile, a linen backing tile and a brass magnifier.
Run: python3 -I koleksi-kupu.py [part ...]  parts: bugs wood linen lens
Assets -> public/themes/art/koleksi-kupu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q6_lib import *

OUT = outdir("koleksi-kupu")
PARTS = sys.argv[1:] or ["bugs", "wood", "linen", "lens"]

# invented species (proportions in units of s; colours = (light, dark) pairs)
SPECIES = {
    "aurelia": dict(fl=1.0, fw=0.5, fs=0.08, hl=0.66, hw=0.6, fore=("#26302a", "#1c221d"), hind=("#ecbf3c", "#d99a22"),
                    border="#1a1712", bw=0.06, base="#141210", pattern="band", bandc="#3fae7c", bandw=0.13, spots="#f3df8e", vein="#0e0d0b"),
    "nila": dict(fl=1.0, fw=0.66, fs=0.02, hl=0.78, hw=0.72, fore=("#3a86d0", "#2459ac"), hind=("#3f94da", "#2a64b4"),
                 glow="#8fd0f4", border="#141b2b", bw=0.1, base="#16233f", spots="#e8eef6", vein="#16233a"),
    "senja": dict(fl=0.92, fw=0.6, fs=0.0, hl=0.7, hw=0.7, fore=("#f6efd8", "#efe2bc"), hind=("#f7d969", "#efc24a"),
                  border="#24201a", bw=0.11, base="#3a3328", pattern="dots", bandc="#d4452e", spots="#f6efe0", vein="#2a241c"),
    "ekor": dict(fl=1.04, fw=0.52, fs=0.08, hl=0.72, hw=0.62, tail=0.36, fore=("#f2e3a6", "#e8d084"), hind=("#f2e3a6", "#e3c86e"),
                 border="#26211a", bw=0.1, base="#26211a", pattern="band", bandc="#2a241c", bandw=0.07, hband="#2a241c", spots="#f2e3a6", vein="#26211a"),
    "mata": dict(fl=0.95, fw=0.62, fs=0.04, hl=0.8, hw=0.76, fore=("#c08a4e", "#9a6436"), hind=("#ad7840", "#7f522a"),
                 border="#4a2e1a", bw=0.07, base="#3a2414", pattern="eye", eye=("#f0d27a", "#1d140c", "#5aa0b8"), spots="#e7cf9a", vein="#3a2414"),
    "mawar": dict(fl=0.9, fw=0.56, fs=0.05, hl=0.66, hw=0.64, fore=("#e7a7b4", "#cf7c92"), hind=("#f0c0c8", "#dc95a6"),
                  border="#4a2232", bw=0.08, base="#5a2a3a", pattern="glass", bandc="#fbeef0", spots="#fbe3ea", vein="#4a2232"),
}


def specimen(name, seed):
    sp = SPECIES[name]
    W, H = 420, 400
    rng = random.Random(seed); nx = Seq(seed * 10)
    art = blank(W, H)
    cx, cy, s = 210, 190, 175
    # cast shadow on the linen (pinned a few mm above the backing)
    tmp, wings = butterfly(blank(W, H), W, H, cx, cy, s, sp, random.Random(seed), Seq(seed * 10))
    sh = np.roll(np.roll(gaussian_filter(wings, 6), 12, 0), 9, 1)
    art = over(art, flat(sh, "#2a2014", 0.28))
    art, _ = butterfly(art, W, H, cx, cy, s, sp, rng, nx)
    art = pin(art, W, H, cx, cy - s * 0.1, 7)
    preview(art, f"kupu-{name}", "#ece3cf")
    save(art, f"{OUT}/{name}.webp", max_w=220, quality=82)


def bugs():
    for i, n in enumerate(SPECIES):
        specimen(n, 11 + i * 7)
        clear()


def wood():
    """Seamless walnut tile: long grain, gouache-ish streaks, a few dark pores."""
    W, H = 512, 512
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n1 = wrap_noise(W, H, 3, (2.0, 60))
    n2 = wrap_noise(W, H, 5, (0.8, 30))
    n3 = wrap_noise(W, H, 9, 30)
    t = np.sin((yy / H * math.tau * 16) + n3 * 2.2 + n1 * 1.6) * 0.5 + 0.5
    t = np.clip(t * 0.4 + n2 * 0.6, 0, 1)
    c0, c1 = col3("#6a4529"), col3("#3e2516")
    rgb = c0 * (1 - t[..., None]) + c1 * t[..., None]
    pores = (wrap_noise(W, H, 13, (0.6, 4)) > 0.86).astype(np.float32)
    rgb = rgb * (1 - pores[..., None] * 0.18)
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/wood.webp", size=(256, 256), quality=70)


def linen():
    W, H = 384, 384
    rng = np.random.default_rng(4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weft = (np.sin(xx * math.pi / 1.5) * 0.5 + 0.5) * wrap_noise(W, H, 2, (40, 0.6))
    warp = (np.sin(yy * math.pi / 1.5) * 0.5 + 0.5) * wrap_noise(W, H, 3, (0.6, 40))
    slub = wrap_noise(W, H, 7, (0.7, 12))
    v = 0.5 * weft + 0.5 * warp
    base = col3("#ece3cf")
    rgb = base * (0.93 + 0.07 * v[..., None]) * (0.97 + 0.05 * slub[..., None])
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/linen.webp", quality=66)


def lens():
    """Brass magnifier lying at an angle: ring with engraved bevel, glass with soft reflection, turned wooden handle."""
    W, H = 420, 420
    rng = random.Random(7); nx = Seq(77)
    art = blank(W, H)
    cx, cy, r = 160, 160, 120
    # handle (behind ring)
    hp = [(cx + r * 0.62, cy + r * 0.62), (cx + r * 1.65, cy + r * 1.65)]
    sh = strokes(W, H, [([(x + 10, y + 14) for x, y in hp], 40, None)])
    art = over(art, flat(gaussian_filter(sh, 8), "#1a120a", 0.3))
    ferr = strokes(W, H, [([hp[0], (cx + r * 0.95, cy + r * 0.95)], 30, None)])
    art = FO(art, ferr, "#b8924a", seed=nx(), sparkle=0)
    hd = strokes(W, H, [([(cx + r * 0.95, cy + r * 0.95), hp[1]], 34, (0.0, 0.08))])
    art = GP(art, hd, "#5a3420", "#3a2012", seed=nx(), rough=1.0, streak=1.2)
    hl = strokes(W, H, [([(cx + r * 1.0, cy + r * 0.93), (cx + r * 1.6, cy + r * 1.53)], 5, (0.2, 0.3))])
    art = OV(art, hl, lambda q: flat(q, "#c08a5a", 0.6))
    # ring shadow
    ring_sh = ring_mask(W, H, cx + 8, cy + 12, r, 22)
    art = over(art, flat(gaussian_filter(ring_sh, 7), "#1a120a", 0.3))
    # glass: very light tint + reflection crescent
    glass = circle_mask(W, H, cx, cy, r - 6)
    art = over(art, flat(glass, "#e8f2f0", 0.16))
    refl = shapes(W, H, [arc_pts(cx, cy, r * 0.82, 3.6, 4.8, 18) + arc_pts(cx + 10, cy + 12, r * 0.7, 4.8, 3.6, 18)])
    art = over(art, flat(gaussian_filter(refl, 2), "#ffffff", 0.5))
    art = over(art, flat(gaussian_filter(circles(W, H, [(cx + r * 0.38, cy + r * 0.42, 10)]), 3), "#ffffff", 0.35))
    ring = ring_mask(W, H, cx, cy, r, 20)
    art = FO(art, ring, "#b8924a", seed=nx(), emboss=0.8, sparkle=0)
    art = OV(art, ring_mask(W, H, cx, cy, r - 9, 1.6), lambda q: flat(q, "#6a4a1a", 0.6))
    art = OV(art, ring_mask(W, H, cx, cy, r + 9, 1.6), lambda q: flat(q, "#6a4a1a", 0.5))
    preview(art, "kupu-lens", "#ece3cf")
    save(art, f"{OUT}/lens.webp", max_w=200, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
