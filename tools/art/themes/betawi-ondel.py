"""Betawi Ondel — gouache folk painting.
Assets: ondel-male / ondel-female (figure) + kembang-male / kembang-female (crown, same canvas, twinkles
separately), pot (kembang kelapa in a pot), burst (kembang ring for portrait medallions), rosette (rail bullet),
balang (seamless repeat-x gigi balang fascia strip).
Run: python3 -I /tmp/pen/art/themes/betawi-ondel.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentF_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/betawi-ondel"
PRE = "/tmp/pen/nt2-F/art"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(41)
seed = [1300]
def nxt():
    seed[0] += 9
    return seed[0]

RED = "#d1262f"; YELLOW = "#f4c430"; GREEN = "#157a4b"; PINK = "#f07aa0"; WHITE = "#fffaf0"; ORANGE = "#ef7d22"
INK = "#1a1412"; STICK = "#8a6a3c"
PAPER = [RED, YELLOW, GREEN, PINK, WHITE, ORANGE]


def g(m, col, col2=None, rough=1.4, streak=.6):
    return gouache_paint(m, col, col2, seed=nxt(), rough=rough, streak=streak)


def shade_side(m, W, H, k=.5, side=1.0):
    """Mask fraction toward the right (shadow side; light from upper left)."""
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    ys, xs = np.nonzero(m > .5)
    if len(xs) == 0:
        return m * 0
    x0, x1 = xs.min() / W, xs.max() / W
    t = np.clip((xx - (x0 + (x1 - x0) * .55)) / max(1e-3, (x1 - x0) * .45), 0, 1)
    return m * t * k


def kembang(W, H, S, cx, cy, radius, count, spread=150, start=-165, stick_w=1.0, tassel=1.0):
    art = blank(W, H)
    sticks = np.zeros((H, W), np.float32)
    tips = []
    for i in range(count):
        a = math.radians(start + spread * i / max(1, count - 1)) + rng.uniform(-.04, .04)
        r = radius * rng.uniform(.93, 1.04)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        bend = rng.uniform(-1.2, 1.2)
        pts = [(cx + (x - cx) * t + math.sin(t * math.pi) * bend * math.sin(a) , cy + (y - cy) * t - math.sin(t * math.pi) * bend * math.cos(a)) for t in np.linspace(0, 1, 10)]
        pts = [(px * S, py * S) for px, py in pts]
        sticks = np.maximum(sticks, stroke_mask(W, H, pts, stick_w * S, (.05, .3)))
        tips.append((x, y, a, PAPER[i % len(PAPER)]))
    art = over(art, g(sticks, STICK, "#a5824c", .6, .3))
    for (x, y, a, col) in tips:
        # paper streamer (cut triangle, slightly crinkled) + paper ball
        ca, sa = math.cos(a), math.sin(a)
        L = 7.5 * tassel; wd = 3.2 * tassel
        tri = [(x - sa * wd, y + ca * wd), (x + sa * wd, y - ca * wd), (x + ca * L, y + sa * L)]
        tri = deform([(px * S, py * S) for px, py in tri], rng, 2, .05)
        tm = shape_mask(W, H, tri, smooth=False)
        art = over(art, g(tm, col, mix(col, "#ffffff", .15), .8))
        ball = shape_mask(W, H, deform(ellipse_pts(x * S, y * S, 2.8 * tassel * S, 2.6 * tassel * S, 9, rng.uniform(0, 3)), rng, 1, .06))
        art = over(art, g(ball, col, mix(col, INK, .12), .6))
        hl = circles_mask(W, H, [((x - .9 * tassel) * S, (y - .9 * tassel) * S, .9 * tassel * S)])
        art = over(art, fade(g(hl * ball, "#ffffff", None, .3), .45))
        if col == WHITE:
            art = over(art, fade(g(outline(ball, .5 * S), "#cdb89a", None, .3), .8))
    return art


def ondel(male):
    S = 3.0; W, H = int(120 * S), int(252 * S)
    P = lambda d: svg_path(d, S, 0, 0)
    face = "#c8202b" if male else "#fbf1e2"
    face_sh = "#8d1219" if male else "#e7cdb4"
    body = "#1f2a2e" if male else "#c8202b"
    body_sh = "#121a1d" if male else "#8f1820"
    sash = RED if male else GREEN
    motif = YELLOW if male else WHITE
    fig = blank(W, H)
    # body / gown
    gown = displace(path_mask(W, H, P("M32 118c-14 10-22 40-24 128h104c-2-88-10-118-24-128-8 6-18 9-28 9s-20-3-28-9Z")), nxt(), 2, 30)
    fig = over(fig, g(gown, body, mix(body, "#ffffff", .08), 1.5, .9))
    fig = over(fig, fade(g(shade_side(gown, W, H, 1), body_sh, None, 1), .6))
    # fabric folds: a few long soft darker strokes
    for x0 in [26, 46, 72, 92]:
        pts = [((x0 + (x0 - 60) * .25 * t + rng.uniform(-1, 1)) * S, (140 + 100 * t) * S) for t in np.linspace(0, 1, 12)]
        fig = over(fig, fade(g(stroke_mask(W, H, pts, 2.6 * S, (.3, .1)) * gown, body_sh, None, .8), .35))
    for d in ["M30 170l6-8 6 8-6 8Z", "M54 186l6-8 6 8-6 8Z", "M78 170l6-8 6 8-6 8Z", "M30 210l6-8 6 8-6 8Z", "M78 210l6-8 6 8-6 8Z", "M54 222l6-8 6 8-6 8Z"]:
        fig = over(fig, fade(g(displace(path_mask(W, H, P(d)), nxt(), .8, 10) * gown, motif, None, .6), .9))
    hem = displace(path_mask(W, H, P("M8 236h104v10H8Z")), nxt(), 1, 20)
    fig = over(fig, g(hem, YELLOW, "#e2ad1c", 1))
    fig = over(fig, g(circles_mask(W, H, [(x * S, 241 * S, 1.6 * S) for x in range(16, 112, 12)]), RED, None, .5))
    sm = displace(path_mask(W, H, P("M32 120c10 22 30 34 56 36l4 10c-30-2-54-16-66-40Z")), nxt(), 1, 16)
    fig = over(fig, g(sm, sash, mix(sash, "#ffffff", .12), 1))
    fig = over(fig, fade(g(shade_side(sm, W, H, 1), mix(sash, INK, .35), None, .6), .4))
    collar = displace(path_mask(W, H, P("M36 120c8 6 16 9 24 9s16-3 24-9l3 8c-9 6-18 9-27 9s-18-3-27-9Z")), nxt(), .8, 14)
    fig = over(fig, g(collar, YELLOW, "#e2ad1c", .8))
    # hair falls
    for d in ["M30 70c-6 10-6 30 0 44", "M90 70c6 10 6 30 0 44"]:
        fig = over(fig, g(path_mask(W, H, P(d), stroke=7.5 * S), INK, "#2a211d", 1.2))
    # cap
    cap = displace(path_mask(W, H, P("M30 64c0-20 14-30 30-30s30 10 30 30Z")), nxt(), 1.2, 20)
    fig = over(fig, g(cap, INK, "#2b221e", 1))
    # face (big mask)
    fm = displace(shape_mask(W, H, ellipse_pts(60 * S, 88 * S, 27 * S, 31 * S, 16)), nxt(), 1.4, 24)
    fig = over(fig, g(fm, face, mix(face, "#ffffff", .1), 1.2, .5))
    fig = over(fig, fade(g(shade_side(fm, W, H, 1), face_sh, None, .8), .5))
    fig = over(fig, fade(g(outline(fm, 1.2 * S), face_sh, None, .6), .9))
    if male:
        for cx in (49, 71):
            fig = over(fig, g(shape_mask(W, H, ellipse_pts(cx * S, 82 * S, 7 * S, 6 * S, 12)), "#fffaf0", None, .6))
            fig = over(fig, g(circles_mask(W, H, [((cx + (1 if cx < 60 else -1)) * S, 82 * S, 3.3 * S)]), INK, None, .4))
            fig = over(fig, g(circles_mask(W, H, [((cx + (1 if cx < 60 else -1) - 1) * S, 81 * S, .9 * S)]), "#ffffff", None, .2))
        for d in ["M40 72q9-6 17 0", "M63 72q8-6 17 0"]:
            fig = over(fig, g(path_mask(W, H, P(d), stroke=3.2 * S), INK, None, .6))
        fig = over(fig, g(path_mask(W, H, P("M60 90v8"), stroke=2 * S), face_sh, None, .4))
        fig = over(fig, g(path_mask(W, H, P("M44 104c6-6 12-2 16-2s10-4 16 2c-4 0-6 3-16 3s-12-3-16-3Z")), INK, None, .8))
        fig = over(fig, g(path_mask(W, H, P("M52 110q8 5 16 0"), stroke=2 * S), "#fffaf0", None, .4))
    else:
        for d in ["M43 82q6-5 12 0", "M65 82q6-5 12 0"]:
            fig = over(fig, g(path_mask(W, H, P(d), stroke=2.5 * S), INK, None, .5))
        for d in ["M42 74q7-4 14-1", "M64 73q7-3 14 1"]:
            fig = over(fig, g(path_mask(W, H, P(d), stroke=1.7 * S), INK, None, .5))
        fig = over(fig, g(path_mask(W, H, P("M60 88v8"), stroke=1.6 * S), face_sh, None, .4))
        cheeks = circles_mask(W, H, [(44 * S, 98 * S, 5.4 * S), (76 * S, 98 * S, 5.4 * S)])
        fig = glaze(fig, pigment(cheeks, PINK, seed=nxt(), density=.5, edge=.2, bloom=.3, gran=.2, rough=2, feather=2.5))
        fig = over(fig, g(path_mask(W, H, P("M51 105q9 7 18 0q-9 3-18 0Z")), "#c8202b", None, .5))
        fig = over(fig, g(circles_mask(W, H, [(60 * S, 68 * S, 2.5 * S)]), "#c8202b", None, .4))
    # headband with gems
    band = displace(path_mask(W, H, P("M30 52h60v9H30Z")), nxt(), .8, 16)
    fig = over(fig, g(band, YELLOW, "#e2ad1c", .8))
    fig = over(fig, g(circles_mask(W, H, [(40 * S, 56.5 * S, 2 * S), (60 * S, 56.5 * S, 2.4 * S), (80 * S, 56.5 * S, 2 * S)]), RED, None, .4))
    crown = kembang(W, H, S, 60, 54, 44, 13)
    tag = "male" if male else "female"
    a = save_full(fig, f"{OUT}/ondel-{tag}.webp", 240)
    b = save_full(crown, f"{OUT}/kembang-{tag}.webp", 240)
    preview(over(fig, crown), f"{PRE}/bw_ondel_{tag}.png", "#fbefd6")
    return a, b


def save_full(arr, path, w_out, q=84):
    im = to_image(arr)
    im = im.resize((w_out, round(im.height * w_out / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


def pot():
    S = 3.0; W, H = int(120 * S), int(132 * S)
    P = lambda d: svg_path(d, S, 0, 0)
    art = blank(W, H)
    art = over(art, g(path_mask(W, H, P("M60 106V48"), stroke=2.2 * S), STICK, None, .6))
    art = over(art, kembang(W, H, S, 60, 50, 46, 17, 300, -240))
    body = displace(path_mask(W, H, P("M44 106h32l-4 22H48Z")), nxt(), 1, 14)
    art = over(art, g(body, GREEN, "#1d8e59", .8))
    art = over(art, fade(g(shade_side(body, W, H, 1), "#0d5233", None, .5), .6))
    art = over(art, g(displace(path_mask(W, H, P("M40 102h40v7H40Z")), nxt(), .8, 12), YELLOW, "#e2ad1c", .6))
    size = save_asset(art, f"{OUT}/pot.webp", max_w=230)
    preview(art, f"{PRE}/bw_pot.png", "#fbefd6")
    return size


def burst():
    S = 3.4; W = H = int(124 * S)
    art = kembang(W, H, S, 62, 62, 56, 24, 345, -90, stick_w=.9)
    size = save_asset(art, f"{OUT}/burst.webp", max_w=400, quality=82)
    preview(art, f"{PRE}/bw_burst.png", "#fffaf0")
    return size


def rosette():
    S = 5; W = H = int(26 * S)
    art = kembang(W, H, S, 13, 13, 9, 8, 315, -90, stick_w=.7, tassel=.62)
    c = circles_mask(W, H, [(13 * S, 13 * S, 3.2 * S)])
    art = over(art, g(grow(c, .8 * S), RED, None, .4))
    art = over(art, g(c, YELLOW, "#e2ad1c", .4))
    size = save_asset(art, f"{OUT}/rosette.webp", max_w=96, quality=84)
    preview(art, f"{PRE}/bw_rosette.png", "#fffaf0")
    return size


def balang():
    """Gigi balang: painted green fascia board, yellow trim, hanging carved teeth with a red wajik. 12 teeth per tile."""
    S = 2; P = 26 * S; H = 30 * S
    def render(Wd):
        n = Wd // P
        art = blank(Wd, H)
        board = np.zeros((H, Wd), np.float32); board[:9 * S] = 1
        art = over(art, g(board, GREEN, "#1d8e59", .6, 1.2))
        # wood grain streaks on the board
        grain = gaussian_filter(np.random.default_rng(nxt()).random((H, Wd)).astype(np.float32), (.4, 14))
        grain = (grain - grain.mean()) / grain.std()
        gl = np.zeros((H, Wd, 4), np.float32); gl[..., :3] = np.array(hex_rgb("#0b4d2e"), np.float32); gl[..., 3] = np.clip(grain - .8, 0, 1) * .5 * board
        art = over(art, gl)
        trim = np.zeros((H, Wd), np.float32); trim[9 * S:11 * S] = 1
        art = over(art, g(trim, YELLOW, "#e2ad1c", .3))
        teeth = np.zeros((H, Wd), np.float32); gems = np.zeros((H, Wd), np.float32); studs = []
        for k in range(n):
            ox = k * P
            teeth = np.maximum(teeth, poly_mask(Wd, H, [(ox + 1 * S, 11 * S), (ox + 25 * S, 11 * S), (ox + 13 * S, 29 * S)]))
            gems = np.maximum(gems, poly_mask(Wd, H, [(ox + 13 * S, 14 * S), (ox + 16 * S, 18 * S), (ox + 13 * S, 22 * S), (ox + 10 * S, 18 * S)]))
            studs.append((ox + 13 * S, 4.5 * S, 1.7 * S))
        art = over(art, g(displace(teeth, nxt(), .8, 10), YELLOW, "#eab52a", .5))
        # carved shadow on the right edge of each tooth
        sh = np.zeros((H, Wd), np.float32)
        for k in range(n):
            ox = k * P
            sh = np.maximum(sh, poly_mask(Wd, H, [(ox + 15 * S, 11 * S), (ox + 25 * S, 11 * S), (ox + 13 * S, 29 * S)]))
        art = over(art, fade(g(sh * teeth, "#c98f14", None, .3), .5))
        art = over(art, g(gems, RED, None, .4))
        art = over(art, g(circles_mask(Wd, H, studs), YELLOW, None, .3))
        return art
    a = render(P * 13)
    out = a[:, :P * 12].copy()
    t = np.linspace(0, 1, P, dtype=np.float32)[None, :, None]
    out[:, :P] = a[:, P * 12:] * (1 - t) + a[:, :P] * t
    im = to_image(out)
    im.save(f"{OUT}/balang.webp", "WEBP", quality=82, method=6)
    preview(out, f"{PRE}/bw_balang.png", "#fbefd6")
    return im.size


if __name__ == "__main__":
    print("ondel male", ondel(True))
    print("ondel female", ondel(False))
    print("pot", pot())
    print("burst", burst())
    print("rosette", rosette())
    print("balang", balang())
    tot = 0
    for fn in sorted(os.listdir(OUT)):
        tot += kb(f"{OUT}/{fn}"); print(fn, kb(f"{OUT}/{fn}"), "KB")
    print("total", round(tot, 1))
