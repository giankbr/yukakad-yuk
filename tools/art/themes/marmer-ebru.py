"""Marmer Ebru — Turkish-style paper marbling (ebru) painted by simulation: pigment drops floated on the bath, pulled
with a stylus and raked with combs (battal -> gel-git -> tarakli), blush / teal / ochre on ivory with threads of gold
ink, laid onto cold-press paper (original design). Run: python3 -I marmer-ebru.py [part ...]
parts: sheet bath ribbon hatip yuva paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c4_lib import *

OUT = outdir("marmer-ebru")
PARTS = sys.argv[1:] or ["sheet", "bath", "ribbon", "hatip", "yuva", "paper"]
IVORY = "#f4ece0"
BLUSH, BLUSH_D, BLUSH_L = "#e3a79c", "#c97c72", "#f2cfc6"
TEAL, TEAL_D, TEAL_L = "#3f8582", "#1f5a5a", "#8fbdb5"
OCHRE, OCHRE_L = "#c9973f", "#e2bf78"
GOLD = "#fff0b0"  # sentinel colour for gold-ink drops (replaced by foil)
GOLD_SET = {GOLD}


class GMarble(Marble):
    """Faster marble render: walks only the still-undecided pixels back through the operations and records which
    drop each pixel came from, so colour and the gold-ink mask come from one pass."""

    def render_idx(self, ss=1):
        W, H = self.W * ss, self.H * ss
        yy, xx = np.mgrid[0:H, 0:W]
        x = (xx.ravel() / ss).astype(np.float32); y = (yy.ravel() / ss).astype(np.float32)
        live = np.arange(W * H)
        idx = np.full(W * H, -1, np.int32)
        for k in range(len(self.ops) - 1, -1, -1):
            op = self.ops[k]
            kind = op[0]
            if kind == "drop":
                _, cx, cy, r, c = op
                dx, dy = x - cx, y - cy
                d2 = dx * dx + dy * dy
                ins = d2 < r * r
                if ins.any():
                    idx[live[ins]] = k
                    keep = ~ins
                    live, dx, dy, d2 = live[keep], dx[keep], dy[keep], d2[keep]
                kk = np.sqrt(np.clip(1 - r * r / np.maximum(d2, 1e-6), 0, None))
                x = cx + dx * kk; y = cy + dy * kk
            elif kind == "tine":
                _, px, py, ang, amp, lam, sharp = op
                ux, uy = math.cos(ang), math.sin(ang)
                d = np.abs((x - px) * (-uy) + (y - py) * ux)
                sh = amp * lam / (d + lam)
                x = x - ux * sh; y = y - uy * sh
            elif kind == "wave":
                _, ang, amp, period, phase = op
                ux, uy = math.cos(ang), math.sin(ang)
                sh = amp * np.sin((x * (-uy) + y * ux) / period * math.tau + phase)
                x = x - ux * sh; y = y - uy * sh
            elif kind == "swirl":
                _, cx, cy, st, rad = op
                dx, dy = x - cx, y - cy
                th = -st * np.exp(-(dx * dx + dy * dy) / (rad * rad))
                c_, s_ = np.cos(th), np.sin(th)
                x = cx + dx * c_ - dy * s_; y = cy + dx * s_ + dy * c_
        return idx.reshape(H, W)

    def lay_arrays(self, ss=2):
        idx = self.render_idx(ss)
        pal = np.array([o[4] if o[0] == "drop" else self.ground for o in self.ops] + [self.ground], np.float32)
        isg = np.array([o[0] == "drop" and np.allclose(o[4], col_arr(GOLD)) for o in self.ops] + [False], np.float32)
        img = pal[idx]; gold = isg[idx]; al = (idx >= 0).astype(np.float32)
        if ss > 1:
            img = img.reshape(self.H, ss, self.W, ss, 3).mean((1, 3)); gold = gold.reshape(self.H, ss, self.W, ss).mean((1, 3))
            al = al.reshape(self.H, ss, self.W, ss).mean((1, 3))
        self.alpha = al.astype(np.float32)
        return img.astype(np.float32), gold.astype(np.float32)


def finish(img, gold, seed, seam=0.10, foil_base="#c9a14a"):
    """Seams, paper grain and gold foil threads."""
    h, w = img.shape[:2]
    e = Marble.edges(gaussian_filter(img, (0.6, 0.6, 0)), 0.05)
    img = img * (1 - seam * gaussian_filter(e, 0.7)[..., None])
    img = paper_finish(img, seed=seed, grain=0.06, mottle=0.07, absorb=0.15)
    out = rgba(img)
    if gold is not None and gold.max() > 0:
        gm = np.clip(gaussian_filter(gold, 0.5) * 1.4, 0, 1)
        out = over(out, foil(gm, foil_base, seed=seed + 5, emboss=0.15, sparkle=0.15))
    return out


def battal(m, rng, n, cols, rmin, rmax, gold_every=0, box=None):
    W, H = m.W, m.H
    x0, y0, x1, y1 = box or (-40, -40, W + 40, H + 40)
    for i in range(n):
        c = cols[rng.integers(len(cols))]
        if gold_every and i % gold_every == gold_every - 1:
            c = GOLD
        m.drop(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(rmin, rmax) * (0.42 if c == GOLD else 1), c)


def torn_edge(W, H, y, seed, amp=7, rough=2.5, top=False):
    """Hand-torn deckled edge: 1 above (or below) a ragged line with fibre wisps."""
    rng = np.random.default_rng(seed)
    xs = np.arange(W)
    n1 = gaussian_filter(rng.standard_normal(W), 18) * amp * 5
    n2 = gaussian_filter(rng.standard_normal(W), 2.2) * rough * 2.2
    line = y + n1 + n2
    yy = np.arange(H)[:, None].astype(np.float32)
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (2.5, 0.6))
    d = (line[None, :] - yy) if not top else (yy - line[None, :])
    return np.clip((d + (fib - 0.5) * 6) / 1.6, 0, 1).astype(np.float32)


def rings_at(m, rng, cx, cy, n, cols, r0, r1, gold_p=0.18):
    """Concentric drops at one spot (the classic bullseye start): each new drop pushes the previous ones out into
    rings. Occasionally a thin gold-ink drop between colours."""
    for i in range(n):
        if rng.random() < gold_p:
            m.drop(cx, cy, rng.uniform(r0 * 0.42, r0 * 0.6), GOLD)
        m.drop(cx, cy, rng.uniform(r0, r1), cols[rng.integers(len(cols))])


def pushed(p, drops):
    """Where a point ends up after later drops push it outward (forward drop map), so a stylus can find it."""
    x, y = p
    for cx, cy, r in drops:
        dx, dy = x - cx, y - cy
        d2 = max(dx * dx + dy * dy, 1e-6)
        k = math.sqrt(1 + r * r / d2)
        x, y = cx + dx * k, cy + dy * k
    return x, y


def lay(m, W, H, ss, seed, seam=0.10, foil_base="#c9a14a", cut=False):
    """cut=True: only the floated pigment is kept (transparent bath), for motifs."""
    img, gold = m.lay_arrays(ss)
    out = finish(img, gold, seed, seam=seam, foil_base=foil_base)
    if cut:
        out[..., 3] = np.maximum(out[..., 3] * m.alpha, 0)
    return out


if "sheet" in PARTS:
    # cover sheet: battal stones raked into gel-git, a soft wave and two gentle stylus turns
    W, H = 780, 760
    rng = np.random.default_rng(5101)
    m = GMarble(W, H, ground=IVORY)
    cols = [TEAL, TEAL_D, BLUSH, BLUSH_D, BLUSH_L, BLUSH_L, IVORY, TEAL_L, IVORY, IVORY, OCHRE_L]
    for cx, cy in ((150, 140), (520, 90), (330, 380), (690, 420), (110, 560), (470, 700), (760, 760), (30, 300)):
        rings_at(m, rng, cx + rng.uniform(-20, 20), cy + rng.uniform(-20, 20), 22, cols, 34, 62, gold_p=0.26)
    m.comb(math.pi / 2, 110, 120, lam=55, alt=True)
    m.wave(0.0, 60, 380, 0.4)
    m.comb(0.0, 150, 70, lam=60, alt=True)
    m.swirl(250, 260, 1.2, 190); m.swirl(560, 520, -1.0, 200)
    art = lay(m, W, H, 2, 5102)
    art[..., 3] *= torn_edge(W, H, H - 26, 5103, amp=4)
    preview(art, "me-sheet", tone="#f6f0e6")
    save(art, f"{OUT}/sheet.webp", max_w=780, quality=80)
    clear()

if "bath" in PARTS:
    # countdown / closing ground: deep teal bath, pigment rings raked into a feathered (tarakli) pattern
    W, H = 780, 640
    rng = np.random.default_rng(5201)
    m = GMarble(W, H, ground="#1f4f4f")
    cols = ["#2a6664", "#367c79", "#215756", "#b07a72", "#d29c92", "#367c79", "#4a918c", "#efe3d2"]
    for cx, cy in ((120, 110), (420, 60), (700, 180), (260, 340), (600, 430), (90, 560), (400, 650), (760, 640)):
        rings_at(m, rng, cx, cy, 20, cols, 30, 56, gold_p=0.2)
    m.comb(0.0, 70, 90, lam=40, alt=True)
    m.comb(math.pi / 2, 26, 22, lam=9, alt=False)
    m.wave(0.0, 26, 420, 1.3)
    art = lay(m, W, H, 2, 5202, seam=0.18, foil_base="#b88f3e")
    art[..., :3] *= 0.9
    preview(art, "me-bath", tone="#163d3e")
    save(art, f"{OUT}/bath.webp", max_w=780, quality=76)
    clear()

if "ribbon" in PARTS:
    # divider: a slip of gel-git marbled paper (rings raked one way then back), torn at both ends
    W, H = 440, 60
    rng = np.random.default_rng(5301)
    m = GMarble(W, H, ground=IVORY)
    cols = [TEAL, BLUSH, TEAL_D, BLUSH_L, IVORY, BLUSH_D, TEAL_L]
    for x in range(-30, W + 60, 64):
        rings_at(m, rng, x + rng.uniform(-6, 6), H / 2 + rng.uniform(-4, 4), 8, cols, 10, 16, gold_p=0.22)
    m.tine(0, H / 2 - 9, 0.0, 70, lam=10)
    m.tine(0, H / 2 + 9, math.pi, 70, lam=10)
    m.comb(math.pi / 2, 18, 9, lam=6, alt=True)
    art = lay(m, W, H, 3, 5302, seam=0.10)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng2 = np.random.default_rng(5303)
    ragL = 14 + gaussian_filter(rng2.standard_normal(H), 2) * 5
    ragR = W - 14 + gaussian_filter(rng2.standard_normal(H), 2) * 5
    taper = np.clip((xx - ragL[:, None]) / 2, 0, 1) * np.clip((ragR[:, None] - xx) / 2, 0, 1)
    art[..., 3] *= taper * torn_edge(W, H, H - 14, 5304, amp=0.8, rough=1.0) * torn_edge(W, H, 14, 5305, amp=0.8, rough=1.0, top=True)
    preview(art, "me-ribbon")
    save(art, f"{OUT}/ribbon.webp", max_w=360, quality=84)
    clear()

if "hatip" in PARTS:
    # ebru flower: concentric blush drops pulled by one stylus stroke into a heart-shaped bloom, a teal calyx and
    # two teal leaves raked from drops (hatip-style)
    W, H = 360, 360
    rng = np.random.default_rng(5401)
    m = GMarble(W, H, ground=IVORY)
    cx, cy = 180, 150
    # leaves first (pushed by the bloom drops later)
    for lx, ly in ((110, 250), (250, 250)):
        for r, c in ((28, TEAL_D), (20, TEAL), (10, TEAL_L)):
            m.drop(lx, ly, r, c)
    m.drop(cx, cy + 70, 10, TEAL_D)
    bloom = ((60, BLUSH_D), (50, BLUSH), (40, "#f6ddd5"), (32, GOLD), (28, BLUSH_D), (18, BLUSH), (10, "#fbeee8"))
    for r, c in bloom:
        m.drop(cx, cy, r, c)
    m.tine(cx, cy - 120, math.pi / 2, 70, lam=10)          # downward pull through the bloom: heart
    for lx, d in ((110, -1), (250, 1)):
        px, py = pushed((lx, 250), [(cx, cy, r) for r, _ in bloom])
        m.tine(px, py, math.atan2(-60, d * 40), 40, lam=6)  # leaves pulled up and out to a point
    art = lay(m, W, H, 3, 5402, seam=0.14, cut=True)
    preview(art, "me-hatip")
    save(art, f"{OUT}/hatip.webp", max_w=200, quality=84)
    clear()

if "yuva" in PARTS:
    # bulbul yuvasi (nightingale's nest): concentric drops turned by the stylus into a spiral medallion
    W, H = 420, 420
    rng = np.random.default_rng(5501)
    m = GMarble(W, H, ground=IVORY)
    cx = cy = 210
    seq = [TEAL_D, BLUSH, "#f3d2c9", TEAL, GOLD, BLUSH_D, "#fbeee8", TEAL_L, BLUSH, GOLD, TEAL_D, "#f3d2c9", BLUSH_D, BLUSH_L]
    for i, c in enumerate(seq):
        m.drop(cx, cy, (34 if c != GOLD else 22) + 4 * (i % 3), c)
    for k, x in enumerate(range(cx - 120, cx + 121, 30)):
        m.tine(x, cy, math.pi / 2, 26 if k % 2 else -26, lam=7)
    m.swirl(cx, cy, 5.5, 105)
    art = lay(m, W, H, 3, 5502, seam=0.14, cut=True)
    preview(art, "me-yuva")
    save(art, f"{OUT}/yuva.webp", max_w=240, quality=84)
    clear()

if "paper" in PARTS:
    from art import paper as _paper
    im = _paper(400, 400, IVORY, seed=5601, fiber=0.6, mottle=0.6)
    arr = np.asarray(im).astype(np.float32) / 255
    # make it tile: mirror-blend edges
    a = arr; b = np.roll(np.roll(a, 200, 0), 200, 1)
    yy, xx = np.mgrid[0:400, 0:400].astype(np.float32)
    w = np.minimum(np.minimum(xx, 399 - xx), np.minimum(yy, 399 - yy)) / 200
    w = np.clip(w * 1.6, 0, 1)[..., None]
    arr = a * w + b * (1 - w)
    Image.fromarray((arr * 255).astype(np.uint8)).save(f"{OUT}/paper.webp", "WEBP", quality=70, method=6)
    print("paper.webp", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")

kb_total(OUT)
