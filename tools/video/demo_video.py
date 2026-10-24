#!/usr/bin/env python3
"""Rawuh "Video Ucapan 3D" demo video generator.

Everything is drawn from code: paper textures, envelope, wax seal, card, rose
petals, sparkles, countdown and bokeh are numpy/Pillow renders. "3D" is faked
with a pinhole camera: every flat layer is a planar quad posed in 3D, projected
and warped with a perspective homography (Pillow PERSPECTIVE transform on
premultiplied RGBa, mip-mapped for crisp text), plus parallax, depth-of-field
blur, Lambert shading and soft shadows.

All layout is authored in "design units" on a 720x1280 frame and scaled by
S = width / 720, so resolution is a flag. The timeline is authored for 30 s and
time-scaled when --duration differs.

Output (deterministic, fixed seeds):
  frontend/public/rawuh/video-ucapan-demo.mp4         1080x1920, 30 fps, 30 s, H.264 + AAC
  frontend/public/rawuh/video-ucapan-demo-poster.webp poster (names reveal)

Usage:
  python3 tools/video/demo_video.py                     # full render + encode
  python3 tools/video/demo_video.py --still 9 21.5      # debug stills (timeline seconds)
  python3 tools/video/demo_video.py --width 720 --duration 20
"""
import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from multiprocessing import get_context
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "frontend/public/rawuh"
OUT_MP4 = OUT_DIR / "video-ucapan-demo.mp4"
OUT_POSTER = OUT_DIR / "video-ucapan-demo-poster.webp"
MUSIC = ROOT / "frontend/public/music/demo/romantis.mp3"
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
TMP_BASE = os.environ.get("RAWUH_TMP", "/private/tmp/claude-502")

# ---- output config (set by configure()) ----
DEF_WIDTH, DEF_DUR, DEF_FPS = 1080, 30.0, 30
TL = 30.0  # timeline is authored in seconds of a 30 s cut
POSTER_T = 9.0  # timeline seconds
CRF, MAXRATE = 21, "2400k"
AUDIO_FADE_IN, AUDIO_FADE_OUT = 0.5, 2.0

W = H = FPS = NF = 0
DUR = S = FOC = CX = CY = 0.0


def configure(width=DEF_WIDTH, dur=DEF_DUR, fps=DEF_FPS):
    global W, H, FPS, DUR, NF, S, FOC, CX, CY
    W = int(width) // 2 * 2
    H = int(round(W * 16 / 9)) // 2 * 2
    FPS, DUR = int(fps), float(dur)
    NF = int(round(FPS * DUR))
    S = W / 720.0
    FOC = 1500.0 * S  # world units == design px at Z = 1500
    CX, CY = W / 2, H / 2


configure()

CREAM = (246, 239, 230)
BLUSH = (242, 215, 208)
ROSE = (168, 85, 106)
GOLD = (201, 162, 74)
GOLD_HI = (224, 194, 122)
INK = (58, 42, 42)
IVORY = (251, 247, 240)

SUP = "/System/Library/Fonts/Supplemental/"
SNELL = (SUP + "SnellRoundhand.ttc", 1)
DIDOT = (SUP + "Didot.ttc", 0)
DIDOT_I = (SUP + "Didot.ttc", 1)
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
AVN_DEMI = (AVENIR, 2)
AVN_MED = (AVENIR, 5)

# envelope / card geometry in world units; textures authored at 2 design px / unit
EW, EH = 600, 400
CW, CH = 540, 756
TS = 2


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def seg(t, a, b):
    return ease((t - a) / (b - a))


def lerp(a, b, u):
    return a + (b - a) * u


def R(x, k=None):
    return int(round(x * (S if k is None else k)))


_FONTS = {}


def font(spec, size):
    key = (spec, int(size))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(spec[0], int(size), index=spec[1])
    return _FONTS[key]


def ss_mask(w, h, fn, ss=3, k=None):
    """Supersampled 'L' mask of real size (w*k, h*k); fn(draw, s) draws in design coords * s."""
    k = S if k is None else k
    rw, rh = R(w, k), R(h, k)
    m = Image.new("L", (rw * ss, rh * ss), 0)
    fn(ImageDraw.Draw(m), ss * k)
    return m.resize((rw, rh), Image.BOX)


def text(d, s, cx, by, txt, spec, size, track=0.0, fill=255):
    """Centered text at baseline by (design coords * s), optional tracking."""
    f = font(spec, size * s)
    if not track:
        d.text((cx * s, by * s), txt, font=f, fill=fill, anchor="ms")
        return
    ws = [f.getlength(c) for c in txt]
    x = cx * s - (sum(ws) + track * s * (len(txt) - 1)) / 2
    for c, cw in zip(txt, ws):
        d.text((x, by * s), c, font=f, fill=fill, anchor="ls")
        x += cw + track * s


def ornament(d, s, cx, y, half, gap=16, dia=7, lw=2.0, dots=True):
    w = max(1, int(round(lw * s)))
    d.line([((cx - half) * s, y * s), ((cx - gap) * s, y * s)], fill=255, width=w)
    d.line([((cx + gap) * s, y * s), ((cx + half) * s, y * s)], fill=255, width=w)
    d.polygon([(cx * s, (y - dia) * s), ((cx + dia) * s, y * s), (cx * s, (y + dia) * s), ((cx - dia) * s, y * s)], fill=255)
    if dots:
        r = 2.6
        for x in (cx - half - 8, cx + half + 8):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=255)


def paint(canvas, mask, fill, opacity=1.0):
    """alpha-composite a fill (RGB colour tuple or RGB image) through mask onto RGBA canvas."""
    src = Image.new("RGB", canvas.size, fill) if isinstance(fill, tuple) else fill
    layer = src.convert("RGBA")
    if opacity != 1.0:
        mask = mask.point(lambda v: int(v * opacity + 0.5))
    layer.putalpha(mask)
    canvas.alpha_composite(layer)


def gradient_stops(n, stops):
    xs = np.linspace(0, 1, n)
    pos = [p for p, _ in stops]
    cols = np.array([c for _, c in stops], np.float32)
    return np.stack([np.interp(xs, pos, cols[:, i]) for i in range(3)], -1)


def gold_fill(w, h, y0, y1):
    """Metallic gold gradient (real px), bands per text line [y0, y1]."""
    stops = [(0.0, (240, 220, 156)), (0.32, (196, 154, 66)), (0.55, (226, 196, 120)), (0.78, (170, 128, 48)), (1.0, (205, 168, 86))]
    lut = gradient_stops(256, stops)
    yy = np.arange(h, dtype=np.float32)[:, None]
    xx = np.arange(w, dtype=np.float32)[None, :]
    u = np.clip((yy - y0) / max(1, (y1 - y0)) + 0.10 * np.sin(xx / w * math.pi * 2.2), 0, 1)
    return lut[(u * 255).astype(np.int32)]


def multi_gold(w, h, bands):
    out = np.zeros((h, w, 3), np.float32)
    edges = [0] + [int((bands[i][1] + bands[i + 1][0]) / 2) for i in range(len(bands) - 1)] + [h]
    for (y0, y1), a, b in zip(bands, edges[:-1], edges[1:]):
        out[a:b] = gold_fill(w, h, y0, y1)[a:b]
    return Image.fromarray(out.astype(np.uint8))


def offset_mask(m, dx, dy, size=None):
    out = Image.new("L", size or m.size, 0)
    out.paste(m, (int(round(dx)), int(round(dy))))
    return out


def mask_sub(a, b):
    return Image.fromarray(np.clip(np.asarray(a, np.int16) - np.asarray(b, np.int16), 0, 255).astype(np.uint8))


def mask_max(a, b):
    return Image.fromarray(np.maximum(np.asarray(a), np.asarray(b)))


def gold_text(im, mask, bands, k=None):
    k = S if k is None else k
    w, h = im.size
    sh = offset_mask(mask, 2 * k, 4 * k).filter(ImageFilter.GaussianBlur(2.5 * k))
    paint(im, sh, (110, 72, 40), 0.30)
    paint(im, mask, multi_gold(w, h, [(y0 * k, y1 * k) for y0, y1 in bands]))


def paper(w, h, base, seed, grain=1.0):
    """Paper texture, real px."""
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 40, (h, w))
    fine = np.asarray(Image.fromarray(np.uint8(np.clip(128 + fine, 0, 255))).filter(ImageFilter.GaussianBlur(0.7 * S)), np.float32) - 128
    cell = 40 * S
    low = Image.fromarray(rng.normal(0, 1, (int(h / cell) + 2, int(w / cell) + 2)).astype(np.float32), "F").resize((w, h), Image.BICUBIC)
    low = np.asarray(low, np.float32)
    fib = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(fib)
    for _ in range(int(w * h / (9000 * S * S))):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        a = rng.uniform(0, math.pi)
        ln = rng.uniform(6, 26) * S
        d.line([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], fill=int(rng.uniform(40, 110)), width=max(1, int(S)))
    fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(0.6 * S)), np.float32)
    v = (fine * 0.13 + low * 1.4 - fib * 0.05) * grain
    arr = np.array(base, np.float32)[None, None, :] + v[..., None] * np.array([1.0, 0.98, 0.94])
    return np.clip(arr, 0, 255)


def rgba_from(arr_rgb, alpha):
    im = Image.fromarray(np.clip(arr_rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(alpha)
    return im


def vgrad(size, scale):
    return Image.linear_gradient("L").resize(size).point(lambda v: int(v * scale))


# ---------------------------------------------------------------- textures
class Tex:
    """Mip-mapped premultiplied texture. levels: (RGBa image, content w, h)."""

    PAD = 6

    def __init__(self, img, extra=None, min_w=20):
        self.levels, self.extra = [], []
        w0, h0 = img.size
        k = 0
        while True:
            f = 2 ** (-k / 2)
            w, h = max(2, round(w0 * f)), max(2, round(h0 * f))
            im = img if k == 0 else img.resize((w, h), Image.LANCZOS)
            pad = Image.new("RGBA", (w + 2 * self.PAD, h + 2 * self.PAD), (0, 0, 0, 0))
            pad.paste(im, (self.PAD, self.PAD))
            self.levels.append((pad.convert("RGBa"), w, h))
            if extra is not None:
                e = extra if k == 0 else extra.resize((w, h), Image.LANCZOS)
                ep = Image.new("L", pad.size, 0)
                ep.paste(e, (self.PAD, self.PAD))
                self.extra.append(np.asarray(ep, np.float32) / 255.0)
            if w < min_w:
                break
            k += 1
        self.w0, self.h0 = w0, h0

    def pick(self, quad):
        q = np.asarray(quad)
        sx = max(np.hypot(*(q[1] - q[0])), np.hypot(*(q[2] - q[3]))) / self.w0
        sy = max(np.hypot(*(q[3] - q[0])), np.hypot(*(q[2] - q[1]))) / self.h0
        s = max(sx, sy, 1e-4)
        k = 0
        while k + 1 < len(self.levels) and 2 ** (-(k + 1) / 2) >= s:
            k += 1
        return k


def homography(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B.append(v)
    return np.linalg.solve(np.array(A, np.float64), np.array(B, np.float64))


def to_rgba(arr):
    return Image.frombytes("RGBa", (arr.shape[1], arr.shape[0]), np.ascontiguousarray(arr).tobytes()).convert("RGBA")


def fade_rgba(im, a):
    if a >= 0.997:
        return im
    arr = np.asarray(im.convert("RGBa"), np.float32) * a
    return to_rgba(arr.astype(np.uint8))


def draw_quad(frame, tex, quad, alpha=1.0, blur=0.0, shade=1.0, modify=None, resample=Image.BICUBIC):
    """Warp tex onto screen quad (TL, TR, BR, BL) and composite onto frame."""
    if alpha <= 0.003:
        return
    q = np.asarray(quad, np.float64)
    if not np.all(np.isfinite(q)):
        return
    blur = float(blur)
    k = tex.pick(q)
    img, w, h = tex.levels[k]
    P = Tex.PAD
    if modify is not None:
        arr = np.array(img)
        modify(arr, k, w, h)
        img = Image.frombytes("RGBa", img.size, arr.tobytes())
    m = 4 + int(math.ceil(blur * 3))
    x0, y0 = int(math.floor(q[:, 0].min())) - m, int(math.floor(q[:, 1].min())) - m
    x1, y1 = int(math.ceil(q[:, 0].max())) + m, int(math.ceil(q[:, 1].max())) + m
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    src = [(P, P), (P + w, P), (P + w, P + h), (P, P + h)]
    coef = homography(q - [x0, y0], src)
    out = img.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, tuple(coef), resample)
    if blur > 0.25:
        out = out.filter(ImageFilter.GaussianBlur(blur))
    if shade != 1.0 or alpha != 1.0:
        a = np.asarray(out, np.float32)
        a[..., :3] *= shade * alpha
        a[..., 3] *= alpha
        out = Image.frombytes("RGBa", out.size, np.clip(a, 0, 255).astype(np.uint8).tobytes())
    frame.alpha_composite(out.convert("RGBA"), dest=(x0, y0))


# ---------------------------------------------------------------- 3D
def rot(rx, ry, rz):
    a, b, c = map(math.radians, (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Ry @ Rx @ Rz


class Pose:
    def __init__(self, X=0.0, Y=0.0, Z=1500.0, rx=0.0, ry=0.0, rz=0.0):
        self.C = np.array([X, Y, Z], np.float64)
        self.R = rot(rx, ry, rz)

    def world(self, pts):
        return (self.R @ np.asarray(pts, np.float64).T).T + self.C

    def project(self, pts):
        P = self.world(pts)
        s = FOC / P[:, 2]
        return np.stack([CX + P[:, 0] * s, CY + P[:, 1] * s], -1)

    def normal(self):
        return self.R @ np.array([0, 0, -1.0])


def screen_to_world(sx, sy, Z):
    """design-px screen position (720x1280 frame) -> world X, Y at depth Z."""
    return (sx - 360) * Z / 1500, (sy - 640) * Z / 1500


LIGHT = np.array([-0.35, -0.55, -1.0]) / np.linalg.norm([-0.35, -0.55, -1.0])
_D0 = float(np.dot([0, 0, -1.0], LIGHT))


def lambert(n, back=False):
    if back:
        n = -n
    d = float(np.dot(n, LIGHT)) / _D0
    return clamp(0.80 + 0.22 * d, 0.72, 1.05)


def facing(quad):
    q = np.asarray(quad)
    area = 0.0
    for i in range(4):
        x1, y1 = q[i]
        x2, y2 = q[(i + 1) % 4]
        area += x1 * y2 - x2 * y1
    return area > 0


def rect_pts(w, h, cx=0.0, cy=0.0, z=0.0):
    return [(cx - w / 2, cy - h / 2, z), (cx + w / 2, cy - h / 2, z), (cx + w / 2, cy + h / 2, z), (cx - w / 2, cy + h / 2, z)]


# ---------------------------------------------------------------- asset builders
def build_background():
    yy = np.linspace(0, 1, H)[:, None, None]
    xx = np.linspace(-1, 1, W)[None, :, None]
    top, bot = np.array(CREAM, np.float32), np.array(BLUSH, np.float32)
    g = top * (1 - yy ** 1.3) + bot * yy ** 1.3
    r = np.sqrt(xx ** 2 * 0.8 + ((yy - 0.42) * 1.6) ** 2)
    glow = np.clip(1 - r, 0, 1) ** 2
    g = g + glow * (np.array([253, 249, 242]) - g) * 0.55
    g = g + 0 * xx
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")


def build_dither():
    # static, fixed-seed grain added to every frame: breaks gradient banding, cheap for x264
    rng = np.random.default_rng(11)
    return rng.normal(0, 1.15, (H, W, 1)).astype(np.float32)


def build_bokeh(n, rmin, rmax, amin, amax, blur, seed, margin):
    """sizes in design px; layer is (W, H) + margin on each side."""
    rmin, rmax, blur, margin = rmin * S, rmax * S, blur * S, R(margin)
    w, h = W + 2 * margin, H + 2 * margin
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w, 4), np.float32)
    cols = [(255, 250, 240), (236, 212, 154), (240, 201, 192), (231, 179, 181), (250, 236, 210)]
    for _ in range(n):
        Rr = rng.uniform(rmin, rmax)
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        col = np.array(cols[rng.integers(len(cols))], np.float32)
        al = rng.uniform(amin, amax)
        x0, x1 = int(max(cx - Rr - 3, 0)), int(min(cx + Rr + 3, w))
        y0, y1 = int(max(cy - Rr - 3, 0)), int(min(cy + Rr + 3, h))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        a = al * np.clip((Rr - d) / (2.5 * S), 0, 1) * (0.72 + 0.28 * np.clip(d / Rr, 0, 1) ** 5)
        a = a[..., None]
        acc[y0:y1, x0:x1, :3] = col * a + acc[y0:y1, x0:x1, :3] * (1 - a)
        acc[y0:y1, x0:x1, 3:] = a * 255 + acc[y0:y1, x0:x1, 3:] * (1 - a)
    im = Image.frombytes("RGBa", (w, h), np.clip(acc, 0, 255).astype(np.uint8).tobytes())
    return im.filter(ImageFilter.GaussianBlur(blur)), margin


def build_vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / (W * 0.62)) ** 2 + ((yy - CY * 0.95) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * 0.16
    v = np.zeros((H, W, 4), np.uint8)
    v[..., 0], v[..., 1], v[..., 2] = 90, 50, 50
    v[..., 3] = (a * 255).astype(np.uint8)
    return Image.frombytes("RGBA", (W, H), v.tobytes())


def liner(w, h, seed):
    """blush envelope liner with gold lattice; w, h design px."""
    rw, rh = R(w), R(h)
    im = rgba_from(paper(rw, rh, (240, 210, 203), seed, 0.8), 255)
    lw = lambda s: max(1, int(1.3 * s))
    m = ss_mask(w, h, lambda d, s: [
        d.line([((i - h) * s, 0), (i * s, h * s)], fill=255, width=lw(s)) for i in range(0, w + h, 46)
    ] + [
        d.line([(i * s, 0), ((i - h) * s, h * s)], fill=255, width=lw(s)) for i in range(0, w + h, 46)
    ], ss=2)
    paint(im, m, (214, 178, 112), 0.42)
    dm = ss_mask(w, h, lambda d, s: [
        d.ellipse([(x - 2.4) * s, (y - 2.4) * s, (x + 2.4) * s, (y + 2.4) * s], fill=255)
        for y in range(0, h + 46, 46) for x in range(23 if (y // 46) % 2 else 0, w + 46, 46)
    ], ss=2)
    paint(im, dm, (196, 150, 70), 0.6)
    return im


def build_seal(Rd=70):
    """gold wax seal; returns RGBA (real px) and its design size."""
    Sd = int(Rd * 2 + 40)
    n = R(Sd)
    c = n / 2
    Rr = Rd * S
    rng = np.random.default_rng(5)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    ang = np.arctan2(yy - c, xx - c)
    rad = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    edge = Rr * (1 + sum(rng.uniform(0.008, 0.03) * np.sin(k * ang + rng.uniform(0, 6.28)) for k in (3, 5, 7, 11, 17)))
    a = np.clip(edge - rad + 0.5, 0, 1)
    nx, ny = (xx - c) / Rr, (yy - c) / Rr
    lit = np.clip(0.75 - 0.45 * nx - 0.6 * ny, 0, 1.4)
    lut = gradient_stops(256, [(0.0, (120, 88, 30)), (0.4, (176, 136, 56)), (0.75, (222, 190, 112)), (1.0, (250, 232, 176))])
    col = lut[np.clip(lit / 1.4 * 255, 0, 255).astype(np.int32)]
    ring = np.exp(-((rad - Rr * 0.74) / (1.6 * S)) ** 2)
    ring_hi = np.exp(-((rad - Rr * 0.74 - 2.2 * S) / (1.4 * S)) ** 2)
    col = col * (1 - 0.35 * ring[..., None]) + 255 * 0.18 * ring_hi[..., None]
    alpha = Image.fromarray((a * 255).astype(np.uint8))
    seal = rgba_from(col, alpha)
    cd = Sd / 2
    mono = ss_mask(Sd, Sd, lambda d, s: (
        text(d, s, cd - 12, cd + 14, "K", DIDOT_I, 48),
        text(d, s, cd + 15, cd + 24, "A", DIDOT_I, 48),
    ))
    paint(seal, offset_mask(mono, -S, -S), (255, 240, 196), 0.75)
    paint(seal, offset_mask(mono, S, 2 * S), (96, 68, 22), 0.75)
    paint(seal, mono, (190, 150, 66), 1.0)
    seal.putalpha(alpha)
    return seal, Sd


def build_envelope():
    w, h = EW * TS, EH * TS  # design px
    rw, rh = R(w), R(h)
    back = liner(w, h, 21)
    paint(back, vgrad((rw, rh), 0.35), (120, 70, 70), 1.0)
    back.putalpha(ss_mask(w, h, lambda d, s: d.rounded_rectangle([0, 0, w * s, h * s], radius=8 * s, fill=255), ss=2))

    vy = 420
    pocket = rgba_from(paper(rw, rh, (250, 245, 236), 22), 255)
    bf = [(0, h), (w * 0.47, h * 0.52), (w * 0.53, h * 0.52), (w, h)]
    bfm = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in bf], fill=255), ss=2)
    sh = bfm.filter(ImageFilter.GaussianBlur(10 * S))
    paint(pocket, mask_sub(sh, bfm), (110, 80, 60), 0.35)
    paint(pocket, bfm, (255, 252, 246), 0.35)
    sides = ss_mask(w, h, lambda d, s: (
        d.polygon([(0, 0), (w * 0.5 * s, vy * s), (0, h * s)], fill=255),
        d.polygon([(w * s, 0), (w * 0.5 * s, vy * s), (w * s, h * s)], fill=255)), ss=2)
    paint(pocket, mask_sub(sides, bfm), (200, 180, 160), 0.10)
    gold_edges = ss_mask(w, h, lambda d, s: (
        d.rounded_rectangle([7 * s, 7 * s, (w - 7) * s, (h - 7) * s], radius=6 * s, outline=255, width=int(3 * s)),
        d.line([(10 * s, 10 * s), (w * 0.5 * s, (vy - 10) * s), ((w - 10) * s, 10 * s)], fill=255, width=int(2.4 * s), joint="curve")))
    paint(pocket, gold_edges, GOLD, 0.95)
    pm = ss_mask(w, h, lambda d, s: (
        d.rounded_rectangle([0, 0, w * s, h * s], radius=8 * s, fill=255),
        d.polygon([(-2 * s, -2 * s), ((w + 2) * s, -2 * s), (w * 0.5 * s, vy * s)], fill=0)), ss=3)
    pocket.putalpha(pm)

    # flap: rows = distance from hinge, tip at 500 design px
    fh = 300 * TS
    rfh = R(fh)
    tip = 500
    fm = ss_mask(w, fh, lambda d, s: d.polygon([(0, 0), (w * s, 0), (w * 0.5 * s, tip * s)], fill=255), ss=3)
    fm = mask_max(fm, ss_mask(w, fh, lambda d, s: d.ellipse([(w / 2 - 80) * s, (tip - 130) * s, (w / 2 + 80) * s, (tip + 2) * s], fill=255), ss=3))
    flap = rgba_from(paper(rw, rfh, (252, 248, 240), 23), 255)
    paint(flap, vgrad((rw, rfh), 0.12), (170, 140, 110), 1.0)
    fe = ss_mask(w, fh, lambda d, s: d.line([(10 * s, 8 * s), (w * 0.5 * s, (tip - 14) * s), ((w - 10) * s, 8 * s)], fill=255, width=int(3 * s), joint="curve"))
    paint(flap, fe, GOLD, 0.95)
    seal, Sd = build_seal(70)
    sa = seal.getchannel("A")
    sx, sy = R(w / 2 - Sd / 2), R(tip - 58 - Sd / 2)
    shadow_m = offset_mask(sa, sx + 3 * S, sy + 7 * S, (rw, rfh))
    paint(flap, shadow_m.filter(ImageFilter.GaussianBlur(6 * S)), (80, 50, 30), 0.45)
    flap.alpha_composite(seal, (sx, sy))
    flap.putalpha(mask_max(fm, offset_mask(sa, sx, sy, (rw, rfh))))

    flap_in = liner(w, fh, 24)
    paint(flap_in, Image.linear_gradient("L").resize((rw, rfh)).point(lambda v: int((255 - v) * 0.25)), (120, 70, 70), 1.0)
    flap_in.putalpha(fm)
    return dict(back=Tex(back), pocket=Tex(pocket), flap=Tex(flap), flap_in=Tex(flap_in))


def card_base(seed):
    w, h = CW * TS, CH * TS
    rw, rh = R(w), R(h)
    im = rgba_from(paper(rw, rh, IVORY, seed), 255)
    frame = ss_mask(w, h, lambda d, s: (
        d.rounded_rectangle([40 * s, 40 * s, (w - 40) * s, (h - 40) * s], radius=12 * s, outline=255, width=int(3.2 * s)),
        d.rounded_rectangle([54 * s, 54 * s, (w - 54) * s, (h - 54) * s], radius=6 * s, outline=255, width=max(1, int(1.4 * s))),
        [d.polygon([(x * s, (y - 11) * s), ((x + 11) * s, y * s), (x * s, (y + 11) * s), ((x - 11) * s, y * s)], fill=255)
         for x in (40, w - 40) for y in (40, h - 40)],
        [(d.line([((x + sx * 72) * s, (y + sy * 20) * s), ((x + sx * 20) * s, (y + sy * 20) * s), ((x + sx * 20) * s, (y + sy * 72) * s)],
                 fill=255, width=int(1.6 * s)),
          d.ellipse([(x + sx * 20 - 3) * s, (y + sy * 20 - 3) * s, (x + sx * 20 + 3) * s, (y + sy * 20 + 3) * s], fill=255))
         for x, sx in ((54, 1), (w - 54, -1)) for y, sy in ((54, 1), (h - 54, -1))],
    ))
    paint(im, frame, GOLD, 0.95)
    yy = np.linspace(0, 1, rh)[:, None]
    wash = (np.exp(-(yy / 0.18) ** 2) + np.exp(-((yy - 1.0) / 0.18) ** 2)) * np.ones((1, rw))
    paint(im, Image.fromarray((wash * 70).astype(np.uint8)), BLUSH, 1.0)
    return im


def build_card_front():
    w, h = CW * TS, CH * TS
    im = card_base(31)
    cx = w / 2
    paint(im, ss_mask(w, h, lambda d, s: (
        text(d, s, cx, 300, "THE WEDDING OF", AVN_DEMI, 30, track=11),
        text(d, s, cx, 1172, "15 · 05 · 2027", DIDOT, 50, track=4))), ROSE)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1240, "YOGYAKARTA", AVN_MED, 24, track=10)), INK, 0.7)
    paint(im, ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 352, 140), ornament(d, s, cx, 1080, 210, gap=18, dia=8))), GOLD)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 760, "&", DIDOT_I, 110)), ROSE, 0.95)
    names = ss_mask(w, h, lambda d, s: (
        text(d, s, cx - 6, 620, "Kirana", SNELL, 205),
        text(d, s, cx + 4, 960, "Arya", SNELL, 205),
    ))
    gold_text(im, names, [(470, 640), (810, 980)])
    return im, names


def build_card_back():
    w, h = CW * TS, CH * TS
    im = card_base(32)
    cx = w / 2
    gold_text(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 330, "Save the Date", SNELL, 128)), [(240, 350)])
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 200, "AKAD & RESEPSI", AVN_DEMI, 28, track=11)), ROSE)
    paint(im, ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 410, 150), ornament(d, s, cx, 700, 90, gap=12, dia=6, lw=1.6, dots=False))), GOLD)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 530, "Sabtu, 15 Mei 2027", DIDOT, 70)), INK)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 620, "Pendopo Ndalem, Yogyakarta", DIDOT_I, 50)), ROSE)
    bx0, by0, bx1, by1 = 130, 850, w - 130, 1300
    paint(im, ss_mask(w, h, lambda d, s: d.rounded_rectangle([bx0 * s, by0 * s, bx1 * s, by1 * s], radius=26 * s, fill=255)), BLUSH, 0.55)
    paint(im, ss_mask(w, h, lambda d, s: d.rounded_rectangle([bx0 * s, by0 * s, bx1 * s, by1 * s], radius=26 * s, outline=255, width=int(2 * s))), GOLD, 0.9)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 950, "KEPADA YTH.", AVN_DEMI, 28, track=9)), ROSE)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1050, "Bapak/Ibu/Saudara/i", DIDOT_I, 60)), INK)
    paint(im, ss_mask(w, h, lambda d, s: [d.ellipse([(x - 2.2) * s, (1150 - 2.2) * s, (x + 2.2) * s, (1150 + 2.2) * s], fill=255)
                                          for x in range(250, w - 250 + 1, 14)]), GOLD, 0.9)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1225, "di tempat", DIDOT_I, 36)), INK, 0.6)
    return im


def build_closing():
    # authored on a 1440x2560 design canvas (2x of 720x1280), rendered straight at (W, H)
    k = S / 2
    w, h = 1440, 2560
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = w / 2
    paint(im, ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 1010, 170, gap=20, dia=9, lw=2.4), ornament(d, s, cx, 1460, 120, gap=16, dia=7, lw=2.2)), k=k), GOLD)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1180, "Kami menantikan", DIDOT_I, 92), k=k), INK)
    gold_text(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1370, "kehadiranmu", SNELL, 168), k=k), [(1240, 1390)], k=k)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 1580, "KIRANA & ARYA", AVN_DEMI, 30, track=14), k=k), ROSE)
    paint(im, ss_mask(w, h, lambda d, s: text(d, s, cx, 2440, "Dibuat dengan Rawuh · rawuh.id", AVN_MED, 36, track=1.5), k=k), INK, 0.55)
    return im.convert("RGBa")


# ---- countdown (design coords on the 720x1280 frame)
CD_TILE_W, CD_TILE_H, CD_GAP, CD_TOP = 136, 156, 16, 690
CD_LABELS = ["HARI", "JAM", "MENIT", "DETIK"]
CD_WIN = (14, 18, 104)  # number window: side inset, top, bottom (tile coords)
CD_NUM_BASE = 86  # number baseline (tile coords)
CD_START = ((203 * 24 + 8) * 60 + 15) * 60 + 3  # 203 hari 08 jam 15 menit 03 detik
CD_TICK0 = 19.8  # timeline second where the countdown clock starts


def cd_tile_x(i):
    total = 4 * CD_TILE_W + 3 * CD_GAP
    return (720 - total) / 2 + i * (CD_TILE_W + CD_GAP)


def build_countdown():
    head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = 360
    paint(head, ss_mask(720, 1280, lambda d, s: ornament(d, s, cx, 492, 110, gap=14, dia=6, lw=1.4)), GOLD)
    gold_text(head, ss_mask(720, 1280, lambda d, s: text(d, s, cx, 580, "Menuju hari bahagia", SNELL, 66)), [(520, 590)])
    paint(head, ss_mask(720, 1280, lambda d, s: text(d, s, cx, 635, "SABTU, 15 MEI 2027", AVN_DEMI, 15, track=6)), ROSE)
    foot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paint(foot, ss_mask(720, 1280, lambda d, s: ornament(d, s, cx, 912, 150, gap=14, dia=6, lw=1.2)), GOLD)
    paint(foot, ss_mask(720, 1280, lambda d, s: text(d, s, cx, 972, "Kirana & Arya", DIDOT_I, 30)), ROSE)

    pad = 30
    tw, th = CD_TILE_W + 2 * pad, CD_TILE_H + 2 * pad
    tiles = []
    for i, lab in enumerate(CD_LABELS):
        t = Image.new("RGBA", (R(tw), R(th)), (0, 0, 0, 0))
        box = lambda d, s, o=0: d.rounded_rectangle([(pad) * s, (pad + o) * s, (pad + CD_TILE_W) * s, (pad + CD_TILE_H + o) * s], radius=12 * s, fill=255)
        sh = ss_mask(tw, th, lambda d, s: box(d, s, 8), ss=2).filter(ImageFilter.GaussianBlur(9 * S))
        paint(t, sh, (92, 52, 48), 0.20)
        body = ss_mask(tw, th, box)
        fill = rgba_from(paper(R(tw), R(th), IVORY, 60 + i), 255)
        paint(fill, vgrad(fill.size, 0.10), BLUSH, 1.0)
        fill.putalpha(body)
        t.alpha_composite(fill)
        paint(t, ss_mask(tw, th, lambda d, s: (
            d.rounded_rectangle([pad * s, pad * s, (pad + CD_TILE_W) * s, (pad + CD_TILE_H) * s], radius=12 * s, outline=255, width=max(1, int(1.3 * s))),
            d.rounded_rectangle([(pad + 6) * s, (pad + 6) * s, (pad + CD_TILE_W - 6) * s, (pad + CD_TILE_H - 6) * s], radius=8 * s, outline=255, width=max(1, int(0.8 * s))),
            d.line([((pad + 30) * s, (pad + 112) * s), ((pad + CD_TILE_W - 30) * s, (pad + 112) * s)], fill=255, width=max(1, int(0.9 * s))),
        )), GOLD, 0.9)
        paint(t, ss_mask(tw, th, lambda d, s: text(d, s, pad + CD_TILE_W / 2, pad + 138, lab, AVN_DEMI, 13, track=4)), ROSE)
        tiles.append(t)
    return dict(head=head.convert("RGBa"), foot=foot.convert("RGBa"), tiles=tiles, pad=pad, num_cache={})


def cd_number_mask(C, txt):
    if txt not in C["num_cache"]:
        ww = CD_TILE_W - 2 * CD_WIN[0]
        hh = CD_WIN[2] - CD_WIN[1]
        size = 64 if len(txt) <= 2 else 54
        C["num_cache"][txt] = ss_mask(ww, hh, lambda d, s: text(d, s, ww / 2, CD_NUM_BASE - CD_WIN[1], txt, DIDOT, size))
    return C["num_cache"][txt]


def cd_fields(v):
    d, r = divmod(v, 86400)
    hh, r = divmod(r, 3600)
    mm, ss = divmod(r, 60)
    return [str(d), f"{hh:02d}", f"{mm:02d}", f"{ss:02d}"]


def draw_countdown(frame, A, t):
    a_in = seg(t, 19.4, 20.5)
    a_out = 1 - seg(t, 24.1, 25.0)
    ga = a_in * a_out
    if ga <= 0.003:
        return
    C = A["countdown"]
    rise = 18 * S * (1 - a_in) - 10 * S * (1 - a_out)

    def layer(img, a, dy):
        if abs(dy) > 0.02:
            img = img.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
        frame.alpha_composite(fade_rgba(img.convert("RGBA"), a))

    layer(C["head"], ga, rise)
    el = t - CD_TICK0
    n = max(0, int(math.floor(el)))
    cur = cd_fields(CD_START - n)
    prev = cd_fields(CD_START - n + 1) if n >= 1 else cur
    p = seg(el - n, 0.0, 0.5) if n >= 1 else 1.0
    pad = C["pad"]
    wx0, wy0 = CD_WIN[0], CD_WIN[1]
    wh = CD_WIN[2] - CD_WIN[1]
    for i in range(4):
        ti = seg(t, 19.55 + 0.12 * i, 20.6 + 0.12 * i) * a_out
        if ti <= 0.003:
            continue
        tile = C["tiles"][i].copy()
        win = np.zeros((R(wh), R(CD_TILE_W - 2 * wx0)), np.float32)
        roll = wh * 0.62

        def put(txt, dy, a):
            m = np.asarray(offset_mask(cd_number_mask(C, txt), 0, dy * S), np.float32) * a
            np.maximum(win, m[: win.shape[0], : win.shape[1]], out=win)

        if prev[i] != cur[i] and p < 1:
            put(prev[i], -roll * p, 1 - p)
            put(cur[i], roll * (1 - p), p)
        else:
            put(cur[i], 0, 1)
        wm = Image.fromarray(np.clip(win, 0, 255).astype(np.uint8))
        full = Image.new("L", tile.size, 0)
        full.paste(wm, (R(pad + wx0), R(pad + wy0)))
        paint(tile, full, INK)
        tx = R(cd_tile_x(i) - pad)
        ty = R(CD_TOP - pad) + R(22 * (1 - seg(t, 19.55 + 0.12 * i, 20.6 + 0.12 * i)))
        frame.alpha_composite(fade_rgba(tile, ti), dest=(tx, ty))
    layer(C["foot"], seg(t, 20.2, 21.2) * a_out, rise)


def build_petal(seed, tint):
    w, h = 200, 240
    ss = 3
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(np.float32)
    u = (xx / (w * ss)) * 2 - 1
    v = 1 - yy / (h * ss)
    width = 0.96 * np.sin(np.pi * np.clip(v * 0.93 + 0.035, 0, 1)) ** 0.62 * (1 - 0.08 * v)
    top = 0.97 - 0.09 * np.cos(np.clip(u, -1, 1) * np.pi / 2) ** 2
    inside = (np.abs(u) < width) & (v < top) & (v > 0.02)
    m = Image.fromarray((inside * 255).astype(np.uint8)).resize((w, h), Image.BOX).filter(ImageFilter.GaussianBlur(0.5))
    v = np.linspace(1, 0, h)[:, None] * np.ones((1, w))
    u = np.ones((h, 1)) * np.linspace(-1, 1, w)[None, :]
    lut = gradient_stops(256, [(0.0, (248, 226, 226)), (0.3, (232, 168, 176)), (0.7, tint), (1.0, (150, 70, 92))])
    col = lut[np.clip(v ** 0.9 * 255, 0, 255).astype(np.int32)]
    ridge = np.exp(-(u / 0.35) ** 2) * 0.10 - np.abs(u) ** 3 * 0.12
    col = col * (1 + ridge[..., None])
    rng = np.random.default_rng(seed)
    veins = np.zeros((h, w), np.float32)
    for _ in range(9):
        a = rng.uniform(-0.7, 0.7)
        veins += np.exp(-((u - a * v) / 0.012) ** 2) * v * 0.5
    col = col * (1 - 0.06 * veins[..., None])
    return Tex(rgba_from(col, m), min_w=10)


def build_sparkle():
    n = 96
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) - (n - 1) / 2
    r = np.sqrt(xx ** 2 + yy ** 2)
    core = np.exp(-(r / 4.5) ** 2)
    glow = np.exp(-(r / 16) ** 2) * 0.35
    rays = np.exp(-(yy / 1.3) ** 2) * np.exp(-np.abs(xx) / 13) + np.exp(-(xx / 1.3) ** 2) * np.exp(-np.abs(yy) / 13)
    diag = (np.exp(-((xx - yy) / 1.8) ** 2) + np.exp(-((xx + yy) / 1.8) ** 2)) * np.exp(-r / 6) * 0.35
    a = np.clip(core + glow + rays * 0.9 + diag, 0, 1)
    col = np.array([255, 246, 220], np.float32) * (1 - glow[..., None]) + np.array(GOLD_HI, np.float32) * glow[..., None]
    arr = np.concatenate([col * a[..., None], a[..., None] * 255], -1)
    return Tex(Image.frombytes("RGBa", (n, n), np.clip(arr, 0, 255).astype(np.uint8).tobytes()).convert("RGBA"), min_w=8)


NEAR_Z = 900  # petals nearer than this are big + blurred: kept in side bands, off the text


def petal_defs():
    rng = np.random.default_rng(77)
    out = []
    n = 50
    for i in range(n):
        near = i % 6 == 2
        Z = rng.uniform(640, NEAR_Z) if near else rng.uniform(1450, 2900)  # mid/far petals stay behind the card
        if near:
            sx0 = rng.uniform(-40, 40) if (i // 6) % 2 else rng.uniform(680, 760)
            amp = rng.uniform(8, 18)
        else:
            sx0 = rng.uniform(20, 700)
            amp = rng.uniform(25, 70)
        out.append(dict(
            t0=3.4 + i * (22.0 / n) + rng.uniform(-0.25, 0.25), Z=Z, sx0=sx0,
            dur=5.2 + 4.2 * (Z - 640) / 2260 + rng.uniform(-0.4, 0.4),
            amp=amp, fr=rng.uniform(0.2, 0.45), ph=rng.uniform(0, 6.28),
            size=rng.uniform(32, 48) * (0.8 if near else 1.0), var=int(rng.integers(3)),
            a0=rng.uniform(0, 360, 3), w=rng.uniform(40, 120, 3) * rng.choice([-1, 1], 3) * np.array([1, 1, 0.4]),
        ))
    return out


def build_assets():
    A = {}
    A["bg"] = build_background()
    A["dither"] = build_dither()
    A["bokeh_far"] = build_bokeh(70, 6, 22, 0.22, 0.5, 2.2, 1, 60)
    A["bokeh_near"] = build_bokeh(16, 34, 80, 0.10, 0.22, 7, 2, 90)
    A["vignette"] = build_vignette()
    A["env"] = build_envelope()
    front, names = build_card_front()
    A["card_front"] = Tex(front, extra=names)
    A["card_back"] = Tex(build_card_back())
    A["closing"] = build_closing()
    A["countdown"] = build_countdown()
    A["petals"] = [build_petal(40 + i, t) for i, t in enumerate([(206, 110, 130), (190, 98, 120), (222, 140, 150)])]
    A["sparkle"] = build_sparkle()
    A["petal_defs"] = petal_defs()
    return A


# ---------------------------------------------------------------- timeline (30 s authored)
def env_state(t):
    e1 = seg(t, 0.0, 2.3)
    sl = seg(t, 3.75, 5.9)
    L = seg(t, 6.0, 7.9)
    Z = lerp(2900, 1650, e1)
    Z = lerp(Z, 1850, sl) + 350 * L
    ysc = lerp(lerp(740, 700, e1), 930, sl)  # design-px screen y of the centre
    Y = (ysc - 640) * Z / 1500 + 520 * seg(t, 6.0, 8.2)
    idle = math.sin(2 * math.pi * t / 4.0) * (1 - sl) * e1
    pose = dict(X=lerp(-140, 0, e1), Y=Y + 4 * idle, Z=Z,
                rx=lerp(24, 0, e1) + 1.2 * idle, ry=lerp(-42, 0, e1), rz=lerp(-9, 0, e1))
    alpha = seg(t, 0.0, 1.0) * (1 - seg(t, 6.3, 8.1))
    theta = 180 * seg(t, 2.4, 3.75)
    blur = 9 * S * seg(t, 6.0, 7.8)
    return pose, alpha, theta, blur


CARD_IN, CARD_OUT = -EH / 2 + 28 + CH / 2, -EH / 2 - 12 - CH / 2


def card_state(t, envpose):
    sl = seg(t, 3.75, 5.9)
    cy_env = lerp(CARD_IN, CARD_OUT, sl)
    attached_C = Pose(**envpose).world([(0, cy_env, 0)])[0]
    L = seg(t, 6.0, 7.9)
    push = seg(t, 7.0, 13.0)
    flip = seg(t, 13.0, 14.9)
    rec = seg(t, 18.4, 19.9)
    hero = np.array([0.0, -12.0, lerp(1370, 1290, push)])
    C = attached_C * (1 - L) + hero * L
    C[2] += 300 * math.sin(math.pi * flip) + 1800 * rec
    C[1] -= 120 * rec
    sway_w = seg(t, 7.6, 8.8) * (1 - seg(t, 11.9, 13.0))
    sway_b = seg(t, 14.7, 15.8) * (1 - seg(t, 17.4, 18.6))
    ry = 14 * math.sin(math.pi * L) + 180 * flip
    ry += 5 * math.sin(2 * math.pi * (t - 7.6) / 4.2) * sway_w + 4.5 * math.sin(2 * math.pi * (t - 14.7) / 3.9) * sway_b
    rx = -10 * math.sin(math.pi * L) + 2.5 * math.sin(2 * math.pi * (t - 7.6) / 5.4) * sway_w + 2 * math.sin(2 * math.pi * (t - 14.7) / 4.6) * sway_b
    rx += -6 * rec
    rz = -2 * math.sin(math.pi * flip)
    pose = dict(X=C[0], Y=C[1], Z=C[2], rx=rx + envpose["rx"] * (1 - L), ry=ry + envpose["ry"] * (1 - L), rz=rz + envpose["rz"] * (1 - L))
    alpha = seg(t, 0.0, 1.0) * (1 - seg(t, 18.5, 19.8))
    blur = 7 * S * rec
    clip = None if L > 0 else (EH / 2 - 4) - (cy_env - CH / 2)  # card-local y beyond which hidden
    return pose, alpha, blur, clip, L > 0


def bg_zoom(t):
    return 1 + 0.06 * (seg(t, 5.4, 8.8) - seg(t, 24.5, 28.8)) + 0.025 * seg(t, 0, 2.4) * (1 - seg(t, 5.4, 8.8))


SHINE = (8.4, 2.6)  # start, duration of the gold sweep over the names


# ---------------------------------------------------------------- rendering
def draw_layer_affine(frame, layer, margin, zoom, ox, oy):
    a = 1 / zoom
    coef = (a, 0, CX - CX * a + margin + ox, 0, a, CY - CY * a + margin + oy)
    frame.alpha_composite(layer.transform((W, H), Image.AFFINE, coef, Image.BILINEAR).convert("RGBA"))


def shadow(frame, polys, offset, radius, opacity):
    """offset, radius in design px; polys in real px."""
    if opacity <= 0.003:
        return
    q = 4
    m = Image.new("L", (W // q, H // q), 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon([((x + offset[0] * S) / q, (y + offset[1] * S) / q) for x, y in p], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(radius * S / q)).resize((W, H), Image.BILINEAR)
    paint(frame, m, (92, 52, 48), opacity)


def render(t_out, A):
    t = t_out * TL / DUR  # timeline time
    frame = A["bg"].copy()
    z = bg_zoom(t)
    ph = 2 * math.pi * t / TL
    bf, mf = A["bokeh_far"]
    bn, mn = A["bokeh_near"]
    draw_layer_affine(frame, bf, mf, 1 + (z - 1) * 0.5, 22 * S * math.sin(ph), 30 * S * math.sin(ph + 1.3))
    draw_layer_affine(frame, bn, mn, z, -40 * S * math.sin(ph + 0.6), -55 * S * math.sin(ph))

    envpose, ealpha, theta, eblur = env_state(t)
    cpose_d, calpha, cblur, clip, lifted = card_state(t, envpose)
    cpose = Pose(**cpose_d)
    zf = (cpose.C[2] if t < 18.4 else 1330.0) if lifted else envpose["Z"]

    pal = seg(t, 6.0, 6.9) * (1 - 0.45 * seg(t, 19.0, 20.5)) * (1 - seg(t, 24.4, 26.2))
    petals = []
    if pal > 0:
        for pd in A["petal_defs"]:
            tt = t - pd["t0"]
            u = tt / pd["dur"]
            if not (0 <= u <= 1):
                continue
            sy = lerp(-140, 1420, u)
            sx = pd["sx0"] + pd["amp"] * math.sin(2 * math.pi * pd["fr"] * tt + pd["ph"])
            Zp = pd["Z"]
            X, Y = screen_to_world(sx, sy, Zp)
            petals.append((Zp, Pose(X, Y, Zp, *(pd["a0"] + pd["w"] * tt)), pd))
        petals.sort(key=lambda x: -x[0])

    def draw_petal(Zp, p, pd):
        s = pd["size"]
        quad = p.project(rect_pts(s, s * 1.2))
        fr = facing(quad)
        sh = lambert(p.normal(), back=not fr) * (1.0 if fr else 0.9)
        blur = min(9.0, 8.0 * abs(1 / Zp - 1 / zf) * 1300) * S
        draw_quad(frame, A["petals"][pd["var"]], quad, alpha=pal * 0.95, blur=blur, shade=sh, resample=Image.BILINEAR)

    # petals behind this depth draw under the card / countdown / closing text; only the
    # near side-band petals pass in front of text
    card_z = cpose.C[2] if (lifted and calpha > 0.003) else NEAR_Z
    for Zp, p, pd in petals:
        if Zp > card_z:
            draw_petal(Zp, p, pd)

    # ---- envelope group (composited as one layer so the fade does not reveal the card inside)
    ep = Pose(**envpose)
    env = A["env"]
    back_q = ep.project(rect_pts(EW, EH))
    esh = lambert(ep.normal())
    th = math.radians(theta)
    flap_q = ep.project([(x, -EH / 2 + dd * math.cos(th), -dd * math.sin(th))
                         for x, dd in ((-EW / 2, 0), (EW / 2, 0), (EW / 2, 300), (-EW / 2, 300))])
    flap_tri = ep.project([(-EW / 2, -EH / 2, 0), (EW / 2, -EH / 2, 0), (0, -EH / 2 + 250 * math.cos(th), -250 * math.sin(th))])
    fnorm = ep.R @ np.array([0, math.sin(th), -math.cos(th)])
    flap_front = facing(flap_q)
    fsh = lambert(fnorm, back=not flap_front)

    if ealpha > 0.003:
        grp = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        def draw_flap():
            draw_quad(grp, env["flap"] if flap_front else env["flap_in"], flap_q, blur=eblur, shade=fsh)

        polys = [back_q] + ([flap_tri] if theta > 5 else [])
        shadow(grp, polys, (10 * (ep.C[2] / 1650), 22 * (1650 / ep.C[2])), 22, 0.26)
        if theta > 90:
            draw_flap()
        draw_quad(grp, env["back"], back_q, blur=eblur, shade=esh)
        if not lifted:
            draw_card(grp, A, cpose, 1.0, cblur, clip, t)
        draw_quad(grp, env["pocket"], back_q, blur=eblur, shade=esh)
        if theta <= 90:
            k = 1 - theta / 90
            shadow(grp, [flap_tri], (2, 5 + 10 * (1 - k)), 6 + 10 * (1 - k), 0.20 * min(1, k * 3))
            draw_flap()
        frame.alpha_composite(fade_rgba(grp, ealpha))

    if lifted and calpha > 0.003:
        L = seg(t, 6.0, 7.9)
        rec = seg(t, 18.4, 19.9)
        cq = cpose.project(rect_pts(CW, CH))
        shadow(frame, [cq], (lerp(6, 16, L), lerp(10, 30, L) * (1 - 0.6 * rec)), lerp(10, 34, L), 0.26 * calpha)
        draw_card(frame, A, cpose, calpha, cblur, None, t)

    draw_countdown(frame, A, t)

    # closing text
    ca = seg(t, 25.3, 26.7) * (1 - seg(t, 28.3, 29.7))
    if ca > 0.003:
        lay = A["closing"]
        dy = (16 * (1 - seg(t, 25.3, 26.9)) - 8 * seg(t, 28.3, 29.7)) * S
        if abs(dy) > 0.02:
            lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
        frame.alpha_composite(fade_rgba(lay.convert("RGBA"), ca))

    for Zp, p, pd in petals:
        if Zp <= card_z:
            draw_petal(Zp, p, pd)

    # sparkles anchored to the card in 3D
    spa = seg(t, 6.9, 8.0) * (1 - seg(t, 18.0, 18.9)) * abs(math.cos(math.radians(cpose_d["ry"]))) ** 3
    if spa > 0.01:
        anchors = [(-215, -170, 3.1, 0.0, 26), (205, -95, 2.6, 0.9, 20), (-185, 120, 2.9, 1.7, 22), (210, 150, 3.4, 0.4, 30),
                   (-40, -290, 2.4, 2.1, 16), (150, 300, 2.8, 1.2, 18), (-230, 300, 3.6, 2.6, 22), (240, -300, 3.0, 1.5, 24),
                   (60, 20, 3.3, 2.9, 16), (-95, -40, 2.7, 0.6, 14)]
        for ax, ay, per, phs, sz in anchors:
            tw = math.sin(2 * math.pi * (t - phs) / per)
            a = max(0.0, tw) ** 3 * spa
            if a < 0.02:
                continue
            sxy = cpose.project([(ax, ay, -12)])[0]
            half = sz * (0.6 + 0.4 * tw) * FOC / cpose.C[2] * 1.4
            quad = [(sxy[0] - half, sxy[1] - half), (sxy[0] + half, sxy[1] - half), (sxy[0] + half, sxy[1] + half), (sxy[0] - half, sxy[1] + half)]
            draw_quad(frame, A["sparkle"], quad, alpha=a, resample=Image.BILINEAR)

    frame.alpha_composite(A["vignette"])
    out = np.asarray(frame.convert("RGB"), np.float32) + A["dither"]
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))


def draw_card(frame, A, pose, alpha, blur, clip, t):
    quad = pose.project(rect_pts(CW, CH))
    front = facing(quad)
    sh = lambert(pose.normal(), back=not front)
    ry = math.radians(math.degrees(math.atan2(pose.R[0, 2], pose.R[2, 2])))
    tex = A["card_front"] if front else A["card_back"]
    if not front:  # back face: texture's left edge sits at card-local +x
        quad = pose.project([(CW / 2, -CH / 2, 0), (-CW / 2, -CH / 2, 0), (-CW / 2, CH / 2, 0), (CW / 2, CH / 2, 0)])
    shine_p = (t - SHINE[0]) / SHINE[1]
    sheen = 0.16 * abs(math.sin(ry)) ** 0.8

    def modify(arr, k, w, h):
        P = Tex.PAD
        if clip is not None:
            r = int(P + clip / CH * h)
            if r < arr.shape[0]:
                arr[max(r, 0):] = 0
        need_shine = front and -0.2 < shine_p < 1.3
        if need_shine or sheen > 0.01:
            hh, ww = arr.shape[:2]
            yy = np.arange(hh, dtype=np.float32)[:, None] / hh
            xx = np.arange(ww, dtype=np.float32)[None, :] / ww
            diag = xx * 0.8 + yy * 0.45
            a = arr.astype(np.float32)
            add = np.zeros((hh, ww), np.float32)
            if sheen > 0.01:
                c = 0.62 - 0.5 * math.sin(ry) * (1 if front else -1)
                add += sheen * np.exp(-((diag - c) / 0.16) ** 2)
            if need_shine:
                add += 0.75 * np.exp(-((diag - lerp(-0.1, 1.35, shine_p)) / 0.05) ** 2) * tex.extra[k]
            a[..., :3] += add[..., None] * (a[..., 3:4] * np.array([1.0, 0.97, 0.88]) - a[..., :3])
            arr[...] = np.clip(a, 0, 255).astype(np.uint8)

    draw_quad(frame, tex, quad, alpha=alpha, blur=blur, shade=sh, modify=modify)


# ======================================================================
# Gallery styles (--style <slug>): 15 s timeline, 720x1280 by default.
# The "blush" style is the original demo above (render / build_assets) and
# does not use any code below.
# ======================================================================
GTL = 15.0  # gallery timeline length (authored seconds)
GAL_POSTER_T = 4.9
GAL_CRF, GAL_MAXRATE = 24, "1050k"
GAL_FADE_OUT = 1.5
GAL_DIR = OUT_DIR / "video-contoh"
SPL = "/System/Library/Fonts/"

GF = dict(
    chancery=(SUP + "Apple Chancery.ttf", 0), copper=(SUP + "Copperplate.ttc", 0), tratt=(SUP + "Trattatello.ttf", 0),
    savoye=(SUP + "Savoye LET.ttc", 0), optima=(SPL + "Optima.ttc", 0), optima_i=(SPL + "Optima.ttc", 2),
    signp=(SUP + "SignPainter.ttc", 0), amtype=(SUP + "AmericanTypewriter.ttc", 0),
    marker=(SPL + "MarkerFelt.ttc", 1), rounded=(SUP + "Arial Rounded Bold.ttf", 0), chalk=(SUP + "ChalkboardSE.ttc", 2),
    futura=(SUP + "Futura.ttc", 0), bodoni=(SUP + "Bodoni 72.ttc", 0), bodoni_i=(SUP + "Bodoni 72.ttc", 1),
    herc=(SUP + "Herculanum.ttf", 0), hoefler=(SUP + "Hoefler Text.ttc", 0), hoefler_i=(SUP + "Hoefler Text.ttc", 2),
    cochin=(SUP + "Cochin.ttc", 0), cochin_i=(SUP + "Cochin.ttc", 2),
)

M_GOLD = [(0.0, (240, 220, 156)), (0.32, (196, 154, 66)), (0.55, (226, 196, 120)), (0.78, (170, 128, 48)), (1.0, (205, 168, 86))]
M_BRIGHT = [(0.0, (255, 240, 184)), (0.35, (226, 184, 96)), (0.6, (252, 224, 150)), (0.85, (196, 146, 64)), (1.0, (238, 204, 126))]
M_CHAMP = [(0.0, (250, 240, 214)), (0.35, (214, 192, 146)), (0.6, (244, 230, 196)), (0.85, (184, 158, 108)), (1.0, (226, 206, 160))]
M_CANDY = [(0.0, (255, 150, 90)), (0.45, (255, 84, 120)), (0.75, (255, 120, 150)), (1.0, (255, 176, 64))]
M_BALI = [(0.0, (250, 214, 110)), (0.35, (204, 146, 30)), (0.6, (240, 190, 70)), (0.85, (168, 112, 20)), (1.0, (222, 168, 50))]

DW_, DH_ = CW * TS, CH * TS  # card texture design size (1080 x 1512)


def ease_out_back(x):
    x = clamp(x)
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def metal_fill(w, h, y0, y1, stops):
    lut = gradient_stops(256, stops)
    yy = np.arange(h, dtype=np.float32)[:, None]
    xx = np.arange(w, dtype=np.float32)[None, :]
    u = np.clip((yy - y0) / max(1, (y1 - y0)) + 0.10 * np.sin(xx / w * math.pi * 2.2), 0, 1)
    return lut[(u * 255).astype(np.int32)]


def metal_text(im, mask, bands, stops, k=None, sh=(60, 36, 20), sop=0.30):
    k = S if k is None else k
    w, h = im.size
    if sop > 0:
        paint(im, offset_mask(mask, 2 * k, 4 * k).filter(ImageFilter.GaussianBlur(2.5 * k)), sh, sop)
    out = np.zeros((h, w, 3), np.float32)
    bands = [(y0 * k, y1 * k) for y0, y1 in bands]
    edges = [0] + [int((bands[i][1] + bands[i + 1][0]) / 2) for i in range(len(bands) - 1)] + [h]
    for (y0, y1), a, b in zip(bands, edges[:-1], edges[1:]):
        out[a:b] = metal_fill(w, h, y0, y1, stops)[a:b]
    paint(im, mask, Image.fromarray(out.astype(np.uint8)))


def T(d, s, y, txt, fk, size, track=0.0, x=None, w=None, stroke=0):
    """text on a design canvas; x defaults to centre of width w"""
    f = font(GF[fk] if isinstance(fk, str) else fk, size * s)
    cx = x if x is not None else w / 2
    if stroke:
        d.text((cx * s, y * s), txt, font=f, fill=255, anchor="ms", stroke_width=int(stroke * s), stroke_fill=255)
    elif not track:
        d.text((cx * s, y * s), txt, font=f, fill=255, anchor="ms")
    else:
        ws = [f.getlength(c) for c in txt]
        xx = cx * s - (sum(ws) + track * s * (len(txt) - 1)) / 2
        for c, cw in zip(txt, ws):
            d.text((xx, y * s), c, font=f, fill=255, anchor="ls")
            xx += cw + track * s


def lines_onto(im, w, h, specs, k=None):
    """specs: (y, text, font, size, fill, track, opacity) ; fill = RGB tuple or ('metal', stops, (y0, y1)).
    returns union mask of metal lines (for the shine sweep)."""
    k = S if k is None else k
    metal_union = None
    for sp in specs:
        y, txt, fk, size, fill = sp[:5]
        track = sp[5] if len(sp) > 5 else 0
        op = sp[6] if len(sp) > 6 else 1.0
        x = sp[7] if len(sp) > 7 else None
        m = ss_mask(w, h, lambda d, s: T(d, s, y, txt, fk, size, track, x=x, w=w), k=k)
        if isinstance(fill, tuple) and len(fill) == 3 and fill[0] == "metal":
            metal_text(im, m, [fill[2]], fill[1], k=k, sh=(40, 24, 12) if fill[1] is not M_CANDY else (150, 40, 60))
            metal_union = m if metal_union is None else mask_max(metal_union, m)
        else:
            paint(im, m, fill, op)
    return metal_union


# ---- shapes (design coords, box inset by a)
def shape_poly(kind, w, h, a):
    x0, y0, x1, y1 = a, a, w - a, h - a
    cx = (x0 + x1) / 2
    if kind == "arch":
        half = (x1 - x0) / 2
        Rr = 1.2 * half
        ya = y0 + math.sqrt(Rr ** 2 - (Rr - half) ** 2)
        left = [(x0 + half * u, ya - math.sqrt(max(0.0, Rr ** 2 - (half * u - Rr) ** 2))) for u in np.linspace(0, 1, 48)]
        right = [(x1 - half * u, ya - math.sqrt(max(0.0, Rr ** 2 - (half * u - Rr) ** 2))) for u in np.linspace(1, 0, 48)]
        return [(x0, y1), (x0, ya)] + left + right + [(x1, ya), (x1, y1)]
    if kind == "deco":
        c = 36 if w > 400 else 12
        return [(x0 + 2 * c, y0), (x1 - 2 * c, y0), (x1 - 2 * c, y0 + c), (x1 - c, y0 + c), (x1 - c, y0 + 2 * c), (x1, y0 + 2 * c),
                (x1, y1 - 2 * c), (x1 - c, y1 - 2 * c), (x1 - c, y1 - c), (x1 - 2 * c, y1 - c), (x1 - 2 * c, y1),
                (x0 + 2 * c, y1), (x0 + 2 * c, y1 - c), (x0 + c, y1 - c), (x0 + c, y1 - 2 * c), (x0, y1 - 2 * c),
                (x0, y0 + 2 * c), (x0 + c, y0 + 2 * c), (x0 + c, y0 + c), (x0 + 2 * c, y0 + c)]
    if kind == "stepped":
        tw = x1 - x0
        pts = [(x0, y1), (x0, y0 + 180), (x0 + tw * 0.11, y0 + 180), (x0 + tw * 0.11, y0 + 120), (x0 + tw * 0.22, y0 + 120),
               (x0 + tw * 0.22, y0 + 60), (x0 + tw * 0.31, y0 + 60), (x0 + tw * 0.31, y0)]
        return pts + [(x0 + x1 - x, y) for x, y in reversed(pts)]
    if kind == "tag":
        c = 0.22 * (x1 - x0)
        return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0, y1), (x0, y0 + c)]
    return None


RADIUS = dict(rect=14, round=64, polaroid=6)


def draw_shape(d, s, kind, w, h, a, fill):
    poly = shape_poly(kind, w, h, a)
    if poly:
        d.polygon([(x * s, y * s) for x, y in poly], fill=fill)
    else:
        r = max(0.0, RADIUS.get(kind, 14) - a * 0.3)
        d.rounded_rectangle([a * s, a * s, (w - a) * s, (h - a) * s], radius=r * s, fill=fill)


def ring_mask(w, h, kind, a, lw, k=None):
    return ss_mask(w, h, lambda d, s: (draw_shape(d, s, kind, w, h, a, 255), draw_shape(d, s, kind, w, h, a + lw, 0)), k=k)


def shape_mask(w, h, kind, a=0, k=None):
    return ss_mask(w, h, lambda d, s: draw_shape(d, s, kind, w, h, a, 255), k=k)


# ---- patterns (outline masks, design coords)
def _oval(cx, cy, a, b, ang, n=28):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + a * math.cos(t) * ca - b * math.sin(t) * sa, cy + a * math.cos(t) * sa + b * math.sin(t) * ca) for t in np.linspace(0, 2 * math.pi, n)]


def kawung(d, s, w, h, cell, lw):
    lwp = max(1, int(lw * s))
    for gy in range(-1, int(h / cell) + 2):
        for gx in range(-1, int(w / cell) + 2):
            cx, cy = gx * cell, gy * cell
            for k in range(4):
                ang = math.pi / 4 + k * math.pi / 2
                pts = _oval(cx + cell * 0.25 * math.cos(ang), cy + cell * 0.25 * math.sin(ang), cell * 0.23, cell * 0.12, ang)
                d.line([(x * s, y * s) for x, y in pts], fill=255, width=lwp)
            r = cell * 0.045
            d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=255)
            r2 = cell * 0.03
            ex, ey = cx + cell / 2, cy + cell / 2
            d.ellipse([(ex - r2) * s, (ey - r2) * s, (ex + r2) * s, (ey + r2) * s], fill=255)


def star8_pts(cx, cy, ro, ri):
    return [(cx + (ro if i % 2 == 0 else ri) * math.cos(i * math.pi / 8 - math.pi / 2),
             cy + (ro if i % 2 == 0 else ri) * math.sin(i * math.pi / 8 - math.pi / 2)) for i in range(16)]


def star8(d, s, w, h, cell, lw):
    lwp = max(1, int(lw * s))
    ro = cell * 0.30
    for gy in range(-1, int(h / cell) + 2):
        for gx in range(-1, int(w / cell) + 2):
            cx, cy = gx * cell, gy * cell
            pts = star8_pts(cx, cy, ro, ro * 0.66)
            d.line([(x * s, y * s) for x, y in pts + [pts[0]]], fill=255, width=lwp)
            d.line([((cx + ro) * s, cy * s), ((cx + cell - ro) * s, cy * s)], fill=255, width=lwp)
            d.line([(cx * s, (cy + ro) * s), (cx * s, (cy + cell - ro) * s)], fill=255, width=lwp)
            ex, ey, r = cx + cell / 2, cy + cell / 2, cell * 0.10
            d.line([(ex * s, (ey - r) * s), ((ex + r) * s, ey * s), (ex * s, (ey + r) * s), ((ex - r) * s, ey * s), (ex * s, (ey - r) * s)], fill=255, width=lwp)


def spiral_pts(cx, cy, r0, turns, sign=1, rot=0.0, n=60):
    out = []
    for t in np.linspace(0, turns * 2 * math.pi, n):
        r = r0 * (1 - t / (turns * 2 * math.pi + 0.8))
        out.append((cx + sign * r * math.cos(t + rot), cy + r * math.sin(t + rot)))
    return out


def patra(d, s, w, h, cell, lw):
    lwp = max(1, int(lw * s))
    for gy in range(-1, int(h / cell) + 2):
        for gx in range(-1, int(w / cell) + 2):
            cx = gx * cell + (cell / 2 if gy % 2 else 0)
            cy = gy * cell
            for sg in (1, -1):
                pts = spiral_pts(cx + sg * cell * 0.18, cy, cell * 0.17, 1.4, sg)
                d.line([(x * s, y * s) for x, y in pts], fill=255, width=lwp)
            leaf = _oval(cx, cy - cell * 0.30, cell * 0.10, cell * 0.04, -math.pi / 2, 18)
            d.line([(x * s, y * s) for x, y in leaf], fill=255, width=lwp)


def gunungan(d, s, cx, ytop, gw, gh, fill=255, carve=0):
    pts_l, pts_r = [], []
    for v in np.linspace(0, 1, 60):
        hw = gw / 2 * (math.sin(min(v / 0.74, 1.0) * math.pi / 2) ** 1.25) * (1 - 0.08 * max(0, (v - 0.86) / 0.14))
        y = ytop + gh * v
        pts_l.append((cx - hw, y))
        pts_r.append((cx + hw, y))
    poly = pts_l + list(reversed(pts_r))
    d.polygon([(x * s, y * s) for x, y in poly], fill=fill)
    lw = max(1, int(2.2 * s))
    # carved details: trunk, branches, gate at base
    d.line([(cx * s, (ytop + gh * 0.10) * s), (cx * s, (ytop + gh * 0.74) * s)], fill=carve, width=lw)
    for i, v in enumerate(np.linspace(0.18, 0.66, 6)):
        y = ytop + gh * v
        span = gw * 0.36 * math.sin(min(v / 0.74, 1) * math.pi / 2)
        for sg in (1, -1):
            pts = [(cx + sg * span * u, y - gh * 0.06 * math.sin(u * math.pi) - gh * 0.03 * u) for u in np.linspace(0, 1, 14)]
            d.line([(x * s, yy * s) for x, yy in pts], fill=carve, width=lw)
            ex, ey = pts[-1]
            r = gw * 0.018
            d.ellipse([(ex - r) * s, (ey - r) * s, (ex + r) * s, (ey + r) * s], fill=carve)
    gx0, gx1 = cx - gw * 0.16, cx + gw * 0.16
    gy0, gy1 = ytop + gh * 0.76, ytop + gh * 0.97
    d.rectangle([gx0 * s, gy0 * s, gx1 * s, gy1 * s], outline=carve, width=lw)
    d.line([(cx * s, gy0 * s), (cx * s, gy1 * s)], fill=carve, width=lw)
    d.polygon([((gx0 - gw * 0.04) * s, gy0 * s), (cx * s, (gy0 - gh * 0.07) * s), ((gx1 + gw * 0.04) * s, gy0 * s)], outline=carve, width=lw)


def flower5(d, s, cx, cy, r, fill=255, rot=0.0):
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        pts = _oval(cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a), r * 0.55, r * 0.30, a + 0.35, 24)
        d.polygon([(x * s, y * s) for x, y in pts], fill=fill)


def deco_fan(d, s, cx, cy, r, a0, a1, n, lw):
    lwp = max(1, int(lw * s))
    for a in np.linspace(math.radians(a0), math.radians(a1), n):
        d.line([((cx + r * 0.25 * math.cos(a)) * s, (cy + r * 0.25 * math.sin(a)) * s), ((cx + r * math.cos(a)) * s, (cy + r * math.sin(a)) * s)], fill=255, width=lwp)
    for rr in (r * 0.25, r * 0.62, r):
        d.arc([(cx - rr) * s, (cy - rr) * s, (cx + rr) * s, (cy + rr) * s], a0, a1, fill=255, width=lwp)


def wood(w, h, seed, base=(118, 72, 42), freq=0.05, amp=1.0):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    low = np.asarray(Image.fromarray(rng.normal(0, 1, (h // int(60 * S) + 2, 6)).astype(np.float32), "F").resize((w, h), Image.BICUBIC))
    g = np.sin((xx / S) * freq + low * 3.0 + np.sin(yy / S * 0.004) * 2) * 0.5 + 0.5
    fine = rng.normal(0, 1, (h, 1)).repeat(w, 1) * 0.0 + rng.normal(0, 1, (h, w)) * 0.3
    v = (g * 0.18 + fine * 0.05) * amp
    arr = np.array(base, np.float32)[None, None, :] * (0.88 + v[..., None])
    return np.clip(arr, 0, 255)


def card_canvas(base, seed, kind, grain=1.0, w=DW_, h=DH_):
    im = rgba_from(paper(R(w), R(h), base, seed, grain), 255)
    return im, shape_mask(w, h, kind)


def finish(im, alpha):
    im.putalpha(alpha)
    return im


def panel(im, w, h, y0, y1, fill, fill_op, line, kind="rect", x0=130, dashed=False):
    pw, ph = w - 2 * x0, y1 - y0
    m = ss_mask(w, h, lambda d, s: d.rounded_rectangle([x0 * s, y0 * s, (w - x0) * s, y1 * s], radius=26 * s, fill=255))
    if kind == "deco":
        m = ss_mask(w, h, lambda d, s: d.polygon([((x + x0) * s, (y + y0) * s) for x, y in shape_poly("deco", pw, ph, 0)], fill=255))
    paint(im, m, fill, fill_op)
    if dashed:
        lm = ss_mask(w, h, lambda d, s: [d.line([((x0 + 10 + i) * s, (y0 + 10) * s), ((x0 + 10 + i + 14) * s, (y0 + 10) * s)], fill=255, width=int(2 * s)) for i in range(0, pw - 20, 24)] +
                     [d.line([((x0 + 10 + i) * s, (y1 - 10) * s), ((x0 + 10 + i + 14) * s, (y1 - 10) * s)], fill=255, width=int(2 * s)) for i in range(0, pw - 20, 24)] +
                     [d.line([((x0 + 10) * s, (y0 + 10 + i) * s), ((x0 + 10) * s, (y0 + 10 + i + 14) * s)], fill=255, width=int(2 * s)) for i in range(0, ph - 20, 24)] +
                     [d.line([((w - x0 - 10) * s, (y0 + 10 + i) * s), ((w - x0 - 10) * s, (y0 + 10 + i + 14) * s)], fill=255, width=int(2 * s)) for i in range(0, ph - 20, 24)])
    elif kind == "deco":
        lm = ss_mask(w, h, lambda d, s: d.line([((x + x0) * s, (y + y0) * s) for x, y in shape_poly("deco", pw, ph, 0) + [shape_poly("deco", pw, ph, 0)[0]]], fill=255, width=int(2 * s)))
    else:
        lm = ss_mask(w, h, lambda d, s: d.rounded_rectangle([x0 * s, y0 * s, (w - x0) * s, y1 * s], radius=26 * s, outline=255, width=int(2 * s)))
    paint(im, lm, line, 0.9)


def dotted(im, w, h, y, col, x0=250, step=14, r=2.2):
    paint(im, ss_mask(w, h, lambda d, s: [d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=255) for x in range(x0, int(w - x0) + 1, step)]), col, 0.9)


def guest_block(im, w, h, cap_font, cap_col, name_font, name_col, dot_col, small_font, small_col, cap="KEPADA YTH.",
                name="Bapak/Ibu/Saudara/i", small="di tempat", cap_size=28, name_size=60):
    lines_onto(im, w, h, [(950, cap, cap_font, cap_size, cap_col, 9), (1050, name, name_font, name_size, name_col),
                          (1225, small, small_font, 36, small_col, 0, 0.65)])
    dotted(im, w, h, 1150, dot_col)


# ---------------------------------------------------------------- particle sprites
def glow_tex(core, halo, n=96, core_r=0.12, halo_r=0.38, halo_a=0.55):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) - (n - 1) / 2
    r = np.sqrt(xx ** 2 + yy ** 2) / n
    c = np.exp(-(r / core_r) ** 2)
    hl = np.exp(-(r / halo_r) ** 2) * halo_a
    a = np.clip(c + hl, 0, 1)
    col = (np.array(core, np.float32) * c[..., None] + np.array(halo, np.float32) * hl[..., None]) / np.maximum(c + hl, 1e-4)[..., None]
    arr = np.concatenate([col * a[..., None], a[..., None] * 255], -1)
    return Tex(Image.frombytes("RGBa", (n, n), np.clip(arr, 0, 255).astype(np.uint8).tobytes()).convert("RGBA"), min_w=8)


def leaf_tex(seed, c0, c1):
    w, h, ss = 160, 220, 3
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(np.float32)
    u = (xx / (w * ss)) * 2 - 1
    v = 1 - yy / (h * ss)
    width = 0.92 * np.sin(np.pi * np.clip(v * 0.98 + 0.01, 0, 1)) ** 0.75
    inside = (np.abs(u) < width) & (v > 0.04) & (v < 0.99)
    m = Image.fromarray((inside * 255).astype(np.uint8)).resize((w, h), Image.BOX).filter(ImageFilter.GaussianBlur(0.5))
    v = np.linspace(1, 0, h)[:, None] * np.ones((1, w))
    u = np.ones((h, 1)) * np.linspace(-1, 1, w)[None, :]
    lut = gradient_stops(256, [(0, c0), (1, c1)])
    col = lut[np.clip((0.5 + 0.5 * u * 0.6 + v * 0.3) * 255, 0, 255).astype(np.int32)]
    rib = np.exp(-(u / 0.035) ** 2) * (v > 0.04)
    col = col * (1 - 0.0 * rib[..., None]) + rib[..., None] * 30
    bloom = np.random.default_rng(seed).normal(0, 1, (h // 20 + 2, w // 20 + 2))
    bloom = np.asarray(Image.fromarray(bloom.astype(np.float32), "F").resize((w, h), Image.BICUBIC))
    col = col + bloom[..., None] * 6 + 14
    return Tex(rgba_from(col, m), min_w=10)


def balloon_tex(col):
    w, h = 140, 340
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:150, 0:w].astype(np.float32)
    nx, ny = (xx - 70) / 62, (yy - 72) / 72
    rr = nx ** 2 + ny ** 2 * (1 + 0.25 * np.clip(ny, 0, 1))
    a = np.clip((1 - rr) * 40, 0, 1)
    lit = np.clip(1.05 - 0.35 * (nx + 0.6) ** 2 - 0.3 * (ny + 0.5) ** 2, 0.55, 1.1)
    c = np.array(col, np.float32) * lit[..., None]
    hi = np.exp(-(((xx - 46) / 12) ** 2 + ((yy - 40) / 20) ** 2)) * 0.75
    c = c + (255 - c) * hi[..., None]
    body = rgba_from(c, Image.fromarray((a * 255).astype(np.uint8)))
    im.alpha_composite(body, (0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(62, 150), (78, 150), (70, 140)], fill=tuple(int(v * 0.8) for v in col) + (255,))
    pts = [(70 + 8 * math.sin(t * 0.06), 150 + t) for t in range(0, 185, 3)]
    sm = Image.new("L", (w * 3, h * 3), 0)
    ImageDraw.Draw(sm).line([(x * 3, y * 3) for x, y in pts], fill=200, width=4)
    sm = sm.resize((w, h), Image.BOX)
    paint(im, sm, (240, 240, 240), 0.9)
    return Tex(im, min_w=10)


def confetti_tex(col):
    w, h = 24, 40
    yy = np.linspace(0, 1, h)[:, None] * np.ones((1, w))
    c = np.array(col, np.float32) * (0.85 + 0.3 * yy[..., None])
    im = rgba_from(c, 255)
    return Tex(im, min_w=6)


def kamboja_tex():
    n = 200
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) - n / 2
    r = np.sqrt(xx ** 2 + yy ** 2) / (n / 2)
    lut = gradient_stops(256, [(0.0, (250, 196, 60)), (0.28, (252, 222, 120)), (0.5, (255, 248, 232)), (1.0, (255, 253, 248))])
    col = lut[np.clip(r * 255, 0, 255).astype(np.int32)]
    m = ss_mask(n, n, lambda d, s: flower5(d, s, n / 2, n / 2, n * 0.44, 255, 0.3), k=1.0)
    m = m.filter(ImageFilter.GaussianBlur(0.6))
    shade = ss_mask(n, n, lambda d, s: [d.line([(n / 2 * s, n / 2 * s), ((n / 2 + n * 0.42 * math.cos(0.3 + k * 1.2566 + 0.5)) * s, (n / 2 + n * 0.42 * math.sin(0.3 + k * 1.2566 + 0.5)) * s)], fill=255, width=int(5 * s)) for k in range(5)], k=1.0).filter(ImageFilter.GaussianBlur(4))
    body = rgba_from(col, m)
    paint(body, Image.fromarray((np.asarray(shade, np.float32) * np.asarray(m, np.float32) / 255).astype(np.uint8)), (200, 170, 120), 0.35)
    body.putalpha(m)
    im.alpha_composite(body)
    return Tex(im, min_w=10)


def gen_parts(seed, n, t_lo, t_hi, kind, dirn=1, size=(30, 46), z_far=(1450, 2900), near_every=6, dur_near=4.0, dur_far=7.0,
              tumble=1.0, amp=(25, 70), variants=1, twinkle=False):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        near = near_every > 0 and i % near_every == 2
        Z = rng.uniform(640, NEAR_Z) if near else rng.uniform(*z_far)
        if near:
            sx0 = rng.uniform(-40, 40) if (i // near_every) % 2 else rng.uniform(680, 760)
            am = rng.uniform(8, 18)
        else:
            sx0 = rng.uniform(20, 700)
            am = rng.uniform(*amp)
        f = (Z - 640) / 2260
        out.append(dict(kind=kind, dirn=dirn, t0=t_lo + i * ((t_hi - t_lo) / n) + rng.uniform(-0.25, 0.25), Z=Z, sx0=sx0,
                        dur=lerp(dur_near, dur_far, f) * rng.uniform(0.9, 1.1), amp=am, fr=rng.uniform(0.2, 0.45), ph=rng.uniform(0, 6.28),
                        size=rng.uniform(*size) * (0.8 if near else 1.0), var=int(rng.integers(variants)),
                        a0=rng.uniform(0, 360, 3) * (1 if tumble else 0), w=rng.uniform(40, 120, 3) * rng.choice([-1, 1], 3) * np.array([1, 1, 0.4]) * tumble,
                        tw=rng.uniform(1.2, 2.6) if twinkle else 0.0, tph=rng.uniform(0, 6.28)))
    return out


# ---------------------------------------------------------------- background helpers
def grad_bg(top, bot, glow, glow_a=0.5, glow_y=0.42):
    yy = np.linspace(0, 1, H)[:, None, None]
    xx = np.linspace(-1, 1, W)[None, :, None]
    g = np.array(top, np.float32) * (1 - yy ** 1.3) + np.array(bot, np.float32) * yy ** 1.3
    r = np.sqrt(xx ** 2 * 0.8 + ((yy - glow_y) * 1.6) ** 2)
    gl = np.clip(1 - r, 0, 1) ** 2
    g = g + gl * (np.array(glow, np.float32) - g) * glow_a + 0 * xx
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")


def bokeh_cols(cols, n, rmin, rmax, amin, amax, blur, seed, margin):
    rmin, rmax, blur, margin = rmin * S, rmax * S, blur * S, R(margin)
    w, h = W + 2 * margin, H + 2 * margin
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w, 4), np.float32)
    for _ in range(n):
        Rr = rng.uniform(rmin, rmax)
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        col = np.array(cols[rng.integers(len(cols))], np.float32)
        al = rng.uniform(amin, amax)
        x0, x1 = int(max(cx - Rr - 3, 0)), int(min(cx + Rr + 3, w))
        y0, y1 = int(max(cy - Rr - 3, 0)), int(min(cy + Rr + 3, h))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        a = (al * np.clip((Rr - d) / (2.5 * S), 0, 1) * (0.72 + 0.28 * np.clip(d / Rr, 0, 1) ** 5))[..., None]
        acc[y0:y1, x0:x1, :3] = col * a + acc[y0:y1, x0:x1, :3] * (1 - a)
        acc[y0:y1, x0:x1, 3:] = a * 255 + acc[y0:y1, x0:x1, 3:] * (1 - a)
    im = Image.frombytes("RGBa", (w, h), np.clip(acc, 0, 255).astype(np.uint8).tobytes())
    return im.filter(ImageFilter.GaussianBlur(blur)), margin


def vignette_col(col, strength):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / (W * 0.62)) ** 2 + ((yy - CY * 0.95) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * strength
    v = np.zeros((H, W, 4), np.uint8)
    v[..., :3] = col
    v[..., 3] = (a * 255).astype(np.uint8)
    return Image.frombytes("RGBA", (W, H), v.tobytes())


def overlay_pattern(bg, fn, col, op):
    paint(bg, ss_mask(720, 1280, fn, ss=2), col, op)


def closing_layer(specs, footer_col, footer_op=0.55):
    k = S / 2
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines_onto(im, 1440, 2560, specs + [(2440, "Dibuat dengan Rawuh · rawuh.id", AVN_MED, 36, footer_col, 1.5, footer_op)], k=k)
    return im.convert("RGBa")


def text_layer(specs, extra=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if extra:
        extra(im)
    lines_onto(im, 720, 1280, specs)
    return im.convert("RGBa")


def orn_layer(im, fn, col, op=1.0):
    paint(im, ss_mask(720, 1280, fn), col, op)


# ---------------------------------------------------------------- countdown (generic tiles)
CDG_LABELS = ["HARI", "JAM", "MENIT", "DETIK"]


def build_cd_style(cfg):
    """cfg: title specs (720 design), tile dict, start (d, h, m, s)"""
    t = cfg["tile"]
    tw_, th_ = 136, t.get("h", 160)
    pad = 30
    head = text_layer(cfg["head"], cfg.get("head_extra"))
    foot = text_layer(cfg["foot"], cfg.get("foot_extra"))
    tiles = []
    for i, lab in enumerate(CDG_LABELS):
        W2, H2 = tw_ + 2 * pad, th_ + 2 * pad
        im = Image.new("RGBA", (R(W2), R(H2)), (0, 0, 0, 0))
        body = ss_mask(W2, H2, lambda d, s: [d.polygon([((x + pad) * s, (y + pad) * s) for x, y in (shape_poly(t["shape"], tw_, th_, 0) or [])], fill=255)] if shape_poly(t["shape"], tw_, th_, 0)
                       else d.rounded_rectangle([pad * s, pad * s, (pad + tw_) * s, (pad + th_) * s], radius=RADIUS.get(t["shape"], 12) * 0.8 * s, fill=255))
        sh = offset_mask(body, 0, 8 * S).filter(ImageFilter.GaussianBlur(9 * S))
        paint(im, sh, t.get("shadow", (40, 20, 20)), t.get("shadow_op", 0.25))
        fill = rgba_from(paper(R(W2), R(H2), t["fill"], 80 + i, t.get("grain", 1.0)), 255)
        fill.putalpha(body)
        im.alpha_composite(fill)
        if t.get("border"):
            inner = ss_mask(W2, H2, lambda d, s: [d.polygon([((x + pad) * s, (y + pad) * s) for x, y in shape_poly(t["shape"], tw_, th_, 5)], fill=255)] if shape_poly(t["shape"], tw_, th_, 0)
                            else d.rounded_rectangle([(pad + 5) * s, (pad + 5) * s, (pad + tw_ - 5) * s, (pad + th_ - 5) * s], radius=RADIUS.get(t["shape"], 12) * 0.6 * s, fill=255))
            ring = mask_sub(body, ss_mask(W2, H2, lambda d, s: [d.polygon([((x + pad) * s, (y + pad) * s) for x, y in shape_poly(t["shape"], tw_, th_, 1.6)], fill=255)] if shape_poly(t["shape"], tw_, th_, 0)
                                          else d.rounded_rectangle([(pad + 1.6) * s, (pad + 1.6) * s, (pad + tw_ - 1.6) * s, (pad + th_ - 1.6) * s], radius=RADIUS.get(t["shape"], 12) * 0.8 * s, fill=255)))
            inner_ring = mask_sub(inner, ss_mask(W2, H2, lambda d, s: [d.polygon([((x + pad) * s, (y + pad) * s) for x, y in shape_poly(t["shape"], tw_, th_, 6)], fill=255)] if shape_poly(t["shape"], tw_, th_, 0)
                                                 else d.rounded_rectangle([(pad + 6) * s, (pad + 6) * s, (pad + tw_ - 6) * s, (pad + th_ - 6) * s], radius=RADIUS.get(t["shape"], 12) * 0.6 * s, fill=255)))
            paint(im, ring, t["border"], 0.95)
            paint(im, inner_ring, t["border"], 0.7)
        if t.get("hole"):
            hm = ss_mask(W2, H2, lambda d, s: d.ellipse([(pad + tw_ / 2 - 7) * s, (pad + 12) * s, (pad + tw_ / 2 + 7) * s, (pad + 26) * s], fill=255))
            paint(im, hm, (90, 60, 40), 0.85)
        ly = t.get("line_y", 116)
        paint(im, ss_mask(W2, H2, lambda d, s: d.line([((pad + 30) * s, (pad + ly) * s), ((pad + tw_ - 30) * s, (pad + ly) * s)], fill=255, width=max(1, int(0.9 * s)))), t["accent"], 0.9)
        paint(im, ss_mask(W2, H2, lambda d, s: T(d, s, pad + t.get("label_y", 142), lab, t["lab_font"], 13, 4, x=pad + tw_ / 2)), t["lab_col"])
        tiles.append(im)
    d0, h0, m0, s0 = cfg["start"]
    return dict(head=head, foot=foot, tiles=tiles, pad=pad, tw=tw_, th=th_, num_cache={}, cfg=cfg,
                start=((d0 * 24 + h0) * 60 + m0) * 60 + s0)


def draw_cd_style(frame, C, t, t_in=9.4, t_out=11.7, tick0=9.9):
    a_in = seg(t, t_in, t_in + 0.9)
    a_out = 1 - seg(t, t_out, t_out + 0.7)
    ga = a_in * a_out
    if ga <= 0.003:
        return
    tcfg = C["cfg"]["tile"]
    rise = 18 * S * (1 - a_in) - 10 * S * (1 - a_out)

    def layer(img, a, dy):
        if abs(dy) > 0.02:
            img = img.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
        frame.alpha_composite(fade_rgba(img.convert("RGBA"), a))

    layer(C["head"], ga, rise)
    el = t - tick0
    n = max(0, int(math.floor(el)))
    cur = cd_fields(C["start"] - n)
    prev = cd_fields(C["start"] - n + 1) if n >= 1 else cur
    p = seg(el - n, 0.0, 0.5) if n >= 1 else 1.0
    pad, tw_ = C["pad"], C["tw"]
    wx0 = 14
    wy0, wy1 = tcfg.get("win", (18, 104))
    wh = wy1 - wy0
    base = tcfg.get("num_base", 86)
    total = 4 * tw_ + 3 * 16
    for i in range(4):
        ti = seg(t, t_in + 0.15 + 0.12 * i, t_in + 1.1 + 0.12 * i) * a_out
        if ti <= 0.003:
            continue
        tile = C["tiles"][i].copy()
        win = np.zeros((R(wh), R(tw_ - 2 * wx0)), np.float32)
        roll = wh * 0.62

        def nm(txt):
            key = txt
            if key not in C["num_cache"]:
                ww = tw_ - 2 * wx0
                size = tcfg.get("num_size", 62) * (1.0 if len(txt) <= 2 else 0.84)
                C["num_cache"][key] = ss_mask(ww, wh, lambda d, s: T(d, s, base - wy0, txt, tcfg["num_font"], size, x=ww / 2))
            return C["num_cache"][key]

        def put(txt, dy, a):
            m = np.asarray(offset_mask(nm(txt), 0, dy * S), np.float32) * a
            np.maximum(win, m[: win.shape[0], : win.shape[1]], out=win)

        if prev[i] != cur[i] and p < 1:
            put(prev[i], -roll * p, 1 - p)
            put(cur[i], roll * (1 - p), p)
        else:
            put(cur[i], 0, 1)
        full = Image.new("L", tile.size, 0)
        full.paste(Image.fromarray(np.clip(win, 0, 255).astype(np.uint8)), (R(pad + wx0), R(pad + wy0)))
        paint(tile, full, tcfg["num_col"])
        tx = R((720 - total) / 2 + i * (tw_ + 16) - pad)
        ty = R(tcfg.get("top", 690) - pad) + R(22 * (1 - seg(t, t_in + 0.15 + 0.12 * i, t_in + 1.1 + 0.12 * i)))
        frame.alpha_composite(fade_rgba(tile, ti), dest=(tx, ty))
    layer(C["foot"], seg(t, t_in + 0.6, t_in + 1.6) * a_out, rise)


# ---------------------------------------------------------------- intro objects
def build_doors():
    """keraton gebyok: two carved teak doors with kawung panels and a gunungan across both"""
    w, h = 1320, 1800  # design (2 px / world unit): each door 330 x 900 world
    rw, rh = R(w), R(h)
    im = rgba_from(wood(rw, rh, 51, (112, 64, 34)), 255)
    gold = (214, 172, 92)
    km = ss_mask(w, h, lambda d, s: kawung(d, s, w, h, 70, 1.6), ss=2)
    for x0 in (0, 660):
        paint(im, ss_mask(w, h, lambda d, s: d.rectangle([(x0 + 2) * s, 2 * s, (x0 + 658) * s, (h - 2) * s], outline=255, width=int(26 * s))), (70, 38, 20), 0.6)
        paint(im, ss_mask(w, h, lambda d, s: (d.rectangle([(x0 + 30) * s, 30 * s, (x0 + 630) * s, (h - 30) * s], outline=255, width=int(3 * s)),
                                              d.rectangle([(x0 + 44) * s, 44 * s, (x0 + 616) * s, (h - 44) * s], outline=255, width=int(1.5 * s)))), gold, 0.9)
        for (y0, y1) in ((110, 1010), (1110, 1700)):
            pm = ss_mask(w, h, lambda d, s: d.rectangle([(x0 + 80) * s, y0 * s, (x0 + 580) * s, y1 * s], fill=255))
            paint(im, pm, (70, 40, 22), 0.45)
            paint(im, ss_mask(w, h, lambda d, s: d.rectangle([(x0 + 80) * s, y0 * s, (x0 + 580) * s, y1 * s], outline=255, width=int(2.4 * s))), gold, 0.9)
            paint(im, Image.fromarray((np.asarray(km, np.float32) * np.asarray(pm, np.float32) / 255).astype(np.uint8)), gold, 0.5)
        paint(im, ss_mask(w, h, lambda d, s: d.polygon([((x0 + 330) * s, 1040 * s), ((x0 + 352) * s, 1060 * s), ((x0 + 330) * s, 1080 * s), ((x0 + 308) * s, 1060 * s)], fill=255)), gold)
    gm = ss_mask(w, h, lambda d, s: gunungan(d, s, 660, 150, 560, 960, 255, 0))
    sh = offset_mask(gm, 6 * S, 10 * S).filter(ImageFilter.GaussianBlur(8 * S))
    paint(im, sh, (30, 14, 6), 0.5)
    metal_text(im, gm, [(150, 1110)], M_BRIGHT, sop=0)
    hm = ss_mask(w, h, lambda d, s: [d.ellipse([(cx - 26) * s, (1180 - 26) * s, (cx + 26) * s, (1180 + 26) * s], outline=255, width=int(7 * s)) for cx in (612, 708)])
    paint(im, offset_mask(hm, 3 * S, 5 * S).filter(ImageFilter.GaussianBlur(3 * S)), (30, 14, 6), 0.5)
    metal_text(im, hm, [(1150, 1210)], M_BRIGHT, sop=0)
    left, right = im.crop((0, 0, R(660), rh)), im.crop((R(660), 0, rw, rh))
    back = rgba_from(wood(R(660), rh, 52, (86, 48, 26)), 255)
    paint(back, ss_mask(660, h, lambda d, s: d.rectangle([30 * s, 30 * s, 630 * s, (h - 30) * s], outline=255, width=int(3 * s))), gold, 0.6)
    return dict(left=Tex(left), right=Tex(right), back=Tex(back))


def build_candi():
    """bali candi bentar half (left); right half is its mirror"""
    w, h = 640, 2000
    rw, rh = R(w), R(h)
    tiers = [(0, 110, 470), (110, 200, 410), (200, 310, 350), (310, 430, 290), (430, 560, 230), (560, 700, 170), (700, 1820, 110), (1820, 2000, 20)]
    poly = []
    for y0, y1, x in tiers:
        poly += [(x, y0), (x, y1)]
    poly = [(w, 0)] + poly + [(w, h)]
    sm = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in poly], fill=255))
    stone = paper(rw, rh, (238, 230, 214), 61, 1.8)
    im = rgba_from(stone, 255)
    shade = Image.linear_gradient("L").rotate(90).resize((rw, rh)).point(lambda v: int(v * 0.18))
    paint(im, shade, (120, 100, 80), 1.0)
    lines = ss_mask(w, h, lambda d, s: [d.line([(x * s, y1 * s), (w * s, y1 * s)], fill=255, width=int(5 * s)) for y0, y1, x in tiers[:-1]]
                    + [d.line([(x * s, (y0 + 14) * s), (w * s, (y0 + 14) * s)], fill=255, width=int(1.5 * s)) for y0, y1, x in tiers[:-1]])
    paint(im, lines, (196, 146, 52), 0.9)
    relief = ss_mask(w, h, lambda d, s: [d.rectangle([(x + 30) * s, (y0 + 28) * s, (w - 40) * s, (y1 - 20) * s], outline=255, width=int(2 * s)) for y0, y1, x in tiers[1:6]]
                     + [flower5(d, s, (x + w) / 2, (y0 + y1) / 2 + 4, 16, 255, 0.4) for y0, y1, x in tiers[1:6]])
    paint(im, relief, (150, 128, 100), 0.55)
    cloth = ss_mask(w, h, lambda d, s: d.rectangle([110 * s, 1080 * s, w * s, 1250 * s], fill=255))
    paint(im, cloth, (246, 200, 56), 1.0)
    folds = ss_mask(w, h, lambda d, s: [d.line([(x * s, 1084 * s), ((x + 18) * s, 1246 * s)], fill=255, width=int(2 * s)) for x in range(130, w, 46)])
    paint(im, folds, (210, 150, 30), 0.6)
    paint(im, ss_mask(w, h, lambda d, s: (d.line([(110 * s, 1080 * s), (w * s, 1080 * s)], fill=255, width=int(4 * s)), d.line([(110 * s, 1250 * s), (w * s, 1250 * s)], fill=255, width=int(4 * s)))), (190, 130, 30), 1.0)
    paint(im, ss_mask(w, h, lambda d, s: [d.rectangle([(x + 40) * s, 1360 * s, (w - 50) * s, 1760 * s], outline=255, width=int(2 * s)) for x in (110,)]), (150, 128, 100), 0.5)
    im.putalpha(sm)
    from PIL import ImageOps
    return dict(left=Tex(im), right=Tex(ImageOps.mirror(im)))


def build_box():
    pink, ribbon = (255, 126, 150), (255, 206, 72)

    def face_tex(w, h, base, vband=True, hband=False, seed=1, dots=True):
        im = rgba_from(paper(R(w), R(h), base, seed, 0.5), 255)
        if dots:
            paint(im, ss_mask(w, h, lambda d, s: [d.ellipse([(x - 13) * s, (y - 13) * s, (x + 13) * s, (y + 13) * s], fill=255)
                                                  for j, y in enumerate(range(40, h, 90)) for x in range(40 + (45 if j % 2 else 0), w, 90)]), (255, 255, 255), 0.75)
        if vband:
            paint(im, ss_mask(w, h, lambda d, s: d.rectangle([(w / 2 - 60) * s, 0, (w / 2 + 60) * s, h * s], fill=255)), ribbon)
            paint(im, ss_mask(w, h, lambda d, s: [d.line([((w / 2 + o) * s, 0), ((w / 2 + o) * s, h * s)], fill=255, width=int(3 * s)) for o in (-44, 44)]), (230, 170, 40), 0.8)
        if hband:
            paint(im, ss_mask(w, h, lambda d, s: d.rectangle([0, (h / 2 - 60) * s, w * s, (h / 2 + 60) * s], fill=255)), ribbon)
        return im

    front = face_tex(1200, 760, pink, seed=71)
    side = face_tex(600, 760, (230, 104, 128), seed=72)
    inside = rgba_from(paper(R(1200), R(600), (120, 44, 64), 73, 0.6), 255)
    paint(inside, vgrad(inside.size, 0.5), (60, 20, 30), 1.0)
    lid_front = face_tex(1260, 180, (255, 150, 170), seed=74, dots=False)
    lid_top = face_tex(1260, 632, (255, 160, 178), hband=True, seed=75)
    bw, bh = 480, 300
    bow = Image.new("RGBA", (R(bw), R(bh)), (0, 0, 0, 0))
    lm = ss_mask(bw, bh, lambda d, s: (d.ellipse([20 * s, 40 * s, 230 * s, 260 * s], fill=255), d.ellipse([250 * s, 40 * s, 460 * s, 260 * s], fill=255),
                                       d.polygon([(200 * s, 300 * s), (240 * s, 180 * s), (280 * s, 300 * s)], fill=255)))
    paint(bow, lm, ribbon)
    paint(bow, ss_mask(bw, bh, lambda d, s: (d.ellipse([70 * s, 100 * s, 200 * s, 210 * s], fill=255), d.ellipse([280 * s, 100 * s, 410 * s, 210 * s], fill=255))), (220, 150, 30), 0.8)
    paint(bow, ss_mask(bw, bh, lambda d, s: d.ellipse([200 * s, 120 * s, 280 * s, 230 * s], fill=255)), (250, 180, 40))
    return dict(front=Tex(front), side=Tex(side), inside=Tex(inside), lid_front=Tex(lid_front), lid_top=Tex(lid_top), bow=Tex(bow))


def build_sign():
    w, h = 1120, 480
    im = rgba_from(wood(R(w), R(h), 91, (150, 104, 66), 0.03), 255)
    paint(im, ss_mask(w, h, lambda d, s: d.line([(0, (h / 2) * s), (w * s, (h / 2) * s)], fill=255, width=int(4 * s))), (80, 50, 30), 0.7)
    paint(im, ss_mask(w, h, lambda d, s: [d.ellipse([(x - 8) * s, 40 * s, (x + 8) * s, 56 * s], fill=255) for x in (180, w - 180)] +
                      [d.ellipse([(x - 5) * s, (y - 5) * s, (x + 5) * s, (y + 5) * s], fill=255) for x in (40, w - 40) for y in (120, 360)]), (50, 30, 18), 0.9)
    m = ss_mask(w, h, lambda d, s: T(d, s, 230, "Kami akan", "signp", 120, w=w))
    m2 = ss_mask(w, h, lambda d, s: T(d, s, 370, "menikah!", "signp", 140, w=w))
    for mm in (m, m2):
        paint(im, offset_mask(mm, 2 * S, 3 * S).filter(ImageFilter.GaussianBlur(2 * S)), (40, 24, 12), 0.45)
        paint(im, mm, (252, 246, 232))
    paint(im, ss_mask(w, h, lambda d, s: [d.polygon([(x * s, y * s) for x, y in _oval(cx, 420, 26, 10, a)], fill=255) for cx, a in ((150, -0.4), (190, 0.3), (930, 0.4), (970, -0.3))]), (150, 176, 150), 0.95)
    msk = ss_mask(w, h, lambda d, s: d.rounded_rectangle([0, 0, w * s, h * s], radius=18 * s, fill=255))
    im.putalpha(msk)
    rw_, rh_ = 24, 600
    rope = Image.new("RGBA", (R(rw_), R(rh_)), (170, 138, 96, 255))
    paint(rope, ss_mask(rw_, rh_, lambda d, s: [d.line([(0, y * s), (rw_ * s, (y + 14) * s)], fill=255, width=int(3 * s)) for y in range(-20, rh_, 12)]), (110, 84, 54), 0.8)
    return dict(sign=Tex(im), rope=Tex(rope))


def build_lanterns():
    out = []
    for cx, chain, sc in ((74, 110, 1.0), (646, 50, 0.82)):
        w, h = 200, chain + 300
        im = Image.new("RGBA", (R(w), R(h)), (0, 0, 0, 0))
        glow = ss_mask(w, h, lambda d, s: d.ellipse([20 * s, (chain + 40) * s, 180 * s, (chain + 240) * s], fill=255), ss=1).filter(ImageFilter.GaussianBlur(26 * S))
        paint(im, glow, (255, 200, 110), 0.55)
        body_y = chain + 70
        paint(im, ss_mask(w, h, lambda d, s: d.line([(100 * s, 0), (100 * s, (chain + 10) * s)], fill=255, width=int(2 * s))), (200, 160, 80), 0.9)
        glass = ss_mask(w, h, lambda d, s: d.polygon([(70 * s, body_y * s), (130 * s, body_y * s), (142 * s, (body_y + 50) * s), (130 * s, (body_y + 120) * s), (70 * s, (body_y + 120) * s), (58 * s, (body_y + 50) * s)], fill=255))
        paint(im, glass, (255, 214, 140), 0.92)
        frame_ = ss_mask(w, h, lambda d, s: (
            d.polygon([(70 * s, body_y * s), (130 * s, body_y * s), (142 * s, (body_y + 50) * s), (130 * s, (body_y + 120) * s), (70 * s, (body_y + 120) * s), (58 * s, (body_y + 50) * s)], outline=255, width=int(3 * s)),
            d.line([(100 * s, body_y * s), (100 * s, (body_y + 120) * s)], fill=255, width=int(2 * s)),
            d.line([(58 * s, (body_y + 50) * s), (142 * s, (body_y + 50) * s)], fill=255, width=int(2 * s)),
            d.polygon([(64 * s, body_y * s), (100 * s, (chain + 14) * s), (136 * s, body_y * s)], fill=255),
            d.polygon([(70 * s, (body_y + 120) * s), (130 * s, (body_y + 120) * s), (100 * s, (body_y + 160) * s)], fill=255),
            d.ellipse([94 * s, (chain + 4) * s, 106 * s, (chain + 16) * s], outline=255, width=int(2 * s))))
        metal_text(im, frame_, [(chain, body_y + 160)], M_BRIGHT, sop=0)
        out.append(dict(img=im, x=R(cx - w / 2), pivot=(R(w / 2), 0), sc=sc))
    return out


def build_penjor():
    w, h = 300, 460
    im = Image.new("RGBA", (R(w), R(h)), (0, 0, 0, 0))
    P0, P1, P2 = (-30, 420), (40, -50), (160, 60)
    pts = [((1 - u) ** 2 * P0[0] + 2 * (1 - u) * u * P1[0] + u * u * P2[0], (1 - u) ** 2 * P0[1] + 2 * (1 - u) * u * P1[1] + u * u * P2[1]) for u in np.linspace(0, 1, 80)]
    pole = ss_mask(w, h, lambda d, s: [d.line([(pts[i][0] * s, pts[i][1] * s), (pts[i + 1][0] * s, pts[i + 1][1] * s)], fill=255, width=int((12 - 8 * i / 79) * s)) for i in range(79)])
    paint(im, offset_mask(pole, 4 * S, 6 * S).filter(ImageFilter.GaussianBlur(4 * S)), (120, 80, 20), 0.3)
    paint(im, pole, (214, 176, 96))
    hang = ss_mask(w, h, lambda d, s: [(d.line([(x * s, y * s), ((x + 2) * s, (y + 46) * s)], fill=255, width=int(2 * s)),
                                         d.polygon([((x - 9) * s, (y + 40) * s), ((x + 11) * s, (y + 40) * s), ((x + 2) * s, (y + 70) * s)], fill=255))
                                        for x, y in pts[18:78:6]])
    paint(im, hang, (247, 204, 64))
    tipx, tipy = P2
    samp = ss_mask(w, h, lambda d, s: (d.line([(tipx * s, tipy * s), (tipx * s, (tipy + 40) * s)], fill=255, width=int(3 * s)),
                                        d.ellipse([(tipx - 34) * s, (tipy + 36) * s, (tipx + 34) * s, (tipy + 96) * s], fill=255),
                                        [d.line([((tipx + o) * s, (tipy + 90) * s), ((tipx + o * 1.3) * s, (tipy + 135 - abs(o) * 0.8) * s)], fill=255, width=int(3 * s)) for o in range(-28, 29, 8)]))
    paint(im, samp, (250, 214, 90))
    paint(im, ss_mask(w, h, lambda d, s: flower5(d, s, tipx, tipy + 66, 22, 255, 0.2)), (255, 252, 244))
    paint(im, ss_mask(w, h, lambda d, s: d.ellipse([(tipx - 6) * s, (tipy + 60) * s, (tipx + 6) * s, (tipy + 72) * s], fill=255)), (240, 180, 40))
    from PIL import ImageOps
    return [dict(img=im, x=0, pivot=(0, R(420)), sc=1), dict(img=ImageOps.mirror(im), x=W - R(w), pivot=(R(w), R(420)), sc=-1)]


def draw_hangers(frame, hangers, t, amp=1.6, alpha=1.0, glow_flicker=False):
    for i, hg in enumerate(hangers):
        ang = amp * math.sin(2 * math.pi * t * (4 + i) / GTL + i) * hg.get("sc", 1)
        img = hg["img"].rotate(ang, resample=Image.BICUBIC, center=hg["pivot"])
        a = alpha * ((0.9 + 0.1 * math.sin(2 * math.pi * t * 17 / GTL + i * 2)) if glow_flicker else 1.0)
        frame.alpha_composite(fade_rgba(img, a), dest=(hg["x"], 0))


# ---------------------------------------------------------------- style definitions
def style_keraton():
    w, h = DW_, DH_
    base = (78, 46, 28)
    cream, gold_l = (244, 230, 204), (226, 188, 112)

    def frame(im):
        band = mask_sub(shape_mask(w, h, "rect", 34), shape_mask(w, h, "rect", 118))
        km = ss_mask(w, h, lambda d, s: kawung(d, s, w, h, 56, 1.5), ss=2)
        paint(im, Image.fromarray((np.asarray(km, np.float32) * np.asarray(band, np.float32) / 255).astype(np.uint8)), gold_l, 0.55)
        paint(im, ring_mask(w, h, "rect", 26, 4), gold_l)
        paint(im, ring_mask(w, h, "rect", 118, 2.2), gold_l)
        paint(im, ring_mask(w, h, "rect", 128, 1.0), gold_l, 0.7)

    front, fa = card_canvas(base, 101, "rect", 1.3)
    frame(front)
    gm = ss_mask(w, h, lambda d, s: gunungan(d, s, w / 2, 170, 150, 230, 255, 0))
    metal_text(front, gm, [(170, 400)], M_BRIGHT, sop=0.4)
    paint(front, ss_mask(w, h, lambda d, s: (ornament(d, s, w / 2, 492, 140), ornament(d, s, w / 2, 1080, 200, gap=18, dia=8))), gold_l)
    names = lines_onto(front, w, h, [(455, "UNDANGAN PERNIKAHAN", "copper", 26, gold_l, 7), (700, "Laksmi", "chancery", 168, ("metal", M_BRIGHT, (580, 710))),
                                     (820, "&", "chancery", 92, gold_l), (990, "Bayu", "chancery", 168, ("metal", M_BRIGHT, (870, 1000))),
                                     (1172, "04 · 07 · 2027", "cochin", 48, cream, 4), (1242, "SURAKARTA", "copper", 24, cream, 10, 0.75)])
    back, ba = card_canvas(base, 102, "rect", 1.3)
    frame(back)
    paint(back, ss_mask(w, h, lambda d, s: (ornament(d, s, w / 2, 330, 150), ornament(d, s, w / 2, 700, 90, gap=12, dia=6, lw=1.6, dots=False))), gold_l)
    lines_onto(back, w, h, [(290, "AKAD & RESEPSI", "copper", 26, gold_l, 9), (480, "Minggu, 4 Juli 2027", "cochin", 66, cream),
                            (570, "Pendopo Agung, Surakarta", "cochin_i", 50, gold_l)])
    panel(back, w, h, 850, 1300, (40, 22, 12), 0.55, gold_l)
    guest_block(back, w, h, "copper", gold_l, "cochin_i", cream, gold_l, "cochin_i", cream, cap_size=26)

    bg = grad_bg((70, 42, 26), (28, 16, 10), (120, 76, 44), 0.55)
    overlay_pattern(bg, lambda d, s: kawung(d, s, 720, 1280, 64, 1.0), (214, 170, 96), 0.07)
    cd = dict(head=[(560, "Menghitung hari", "chancery", 62, ("metal", M_BRIGHT, (510, 570))), (612, "MINGGU, 4 JULI 2027", "copper", 15, gold_l, 6)],
              head_extra=lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 476, 110, gap=14, dia=6, lw=1.4), gold_l),
              foot=[(972, "Laksmi & Bayu", "cochin_i", 30, gold_l)], foot_extra=lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 912, 150, gap=14, dia=6, lw=1.2), gold_l),
              tile=dict(shape="rect", fill=(66, 38, 22), grain=1.2, border=(220, 180, 104), accent=(220, 180, 104), num_font="cochin", num_col=cream,
                        lab_font="copper", lab_col=gold_l, shadow=(10, 4, 2), shadow_op=0.5),
              start=(251, 6, 42, 3))
    closing = closing_layer([(1230, "Sugeng rawuh", "chancery", 150, ("metal", M_BRIGHT, (1110, 1250))),
                             (1350, "Terima kasih atas doa restu Bapak/Ibu", "cochin_i", 46, cream),
                             (1540, "LAKSMI & BAYU", "copper", 30, gold_l, 14)], cream)
    paint_cl = closing
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, cd=cd, closing=paint_cl,
                bokeh=((255, 214, 140), (230, 180, 100), (255, 236, 190)), bokeh_a=(0.08, 0.22), vig=((10, 4, 2), 0.35),
                intro="doors", sparkle=True,
                parts=[("dust", gen_parts(201, 90, 2.4, 13.5, "dust", -1, (5, 11), near_every=0, dur_far=8.0, tumble=0, amp=(10, 30), twinkle=True)),
                       ("dust_near", gen_parts(202, 8, 2.4, 13.5, "dust", -1, (14, 20), near_every=1, dur_near=6, tumble=0, twinkle=True))],
                sprites=dict(dust=[glow_tex((255, 246, 214), (240, 190, 90))]))


def style_islami():
    w, h = DW_, DH_
    base = (16, 88, 66)
    cream, gold_l = (246, 238, 214), (222, 190, 116)

    def frame(im):
        sm = ss_mask(w, h, lambda d, s: star8(d, s, w, h, 120, 1.3), ss=2)
        paint(im, sm, gold_l, 0.10)
        paint(im, ring_mask(w, h, "arch", 22, 4.5), gold_l)
        paint(im, ring_mask(w, h, "arch", 40, 1.6), gold_l, 0.85)
        paint(im, ring_mask(w, h, "arch", 96, 1.2), gold_l, 0.45)

    front, fa = card_canvas(base, 111, "arch", 0.9)
    paint(front, vgrad(front.size, 0.35), (6, 40, 30), 1.0)
    frame(front)
    star = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in star8_pts(w / 2, 300, 48, 30)], fill=255))
    metal_text(front, star, [(250, 350)], M_BRIGHT)
    paint(front, ss_mask(w, h, lambda d, s: (ornament(d, s, w / 2, 470, 120), ornament(d, s, w / 2, 1080, 200, gap=18, dia=8))), gold_l)
    names = lines_onto(front, w, h, [(432, "WALIMATUL 'URSY", "optima", 28, gold_l, 9), (690, "Fatimah", "savoye", 240, ("metal", M_BRIGHT, (560, 710))),
                                     (800, "&", "savoye", 150, cream), (980, "Yusuf", "savoye", 240, ("metal", M_BRIGHT, (850, 1000))),
                                     (1172, "20 · 09 · 2027", "optima", 48, cream, 4), (1242, "BANDUNG", "optima", 24, cream, 10, 0.75)])
    back, ba = card_canvas(base, 112, "arch", 0.9)
    paint(back, vgrad(back.size, 0.35), (6, 40, 30), 1.0)
    frame(back)
    metal_text(back, ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in star8_pts(w / 2, 300, 40, 25)], fill=255)), [(260, 340)], M_BRIGHT)
    paint(back, ss_mask(w, h, lambda d, s: (ornament(d, s, w / 2, 470, 150), ornament(d, s, w / 2, 760, 90, gap=12, dia=6, lw=1.6, dots=False))), gold_l)
    lines_onto(back, w, h, [(430, "AKAD NIKAH & WALIMAH", "optima", 26, gold_l, 8), (610, "Senin, 20 September 2027", "optima", 58, cream),
                            (690, "Masjid Raya Al-Falah, Bandung", "optima_i", 44, gold_l)])
    panel(back, w, h, 850, 1300, (8, 52, 40), 0.6, gold_l)
    guest_block(back, w, h, "optima", gold_l, "optima_i", cream, gold_l, "optima_i", cream, cap_size=26, name_size=56)

    bg = grad_bg((18, 86, 66), (6, 40, 32), (40, 130, 100), 0.45)
    overlay_pattern(bg, lambda d, s: star8(d, s, 720, 1280, 90, 1.0), (214, 182, 110), 0.08)
    intro_txt = text_layer([(640, "Bismillahirrahmanirrahim", "savoye", 76, ("metal", M_BRIGHT, (590, 650))),
                            (700, "Dengan menyebut nama Allah Yang Maha Pengasih", "optima_i", 18, cream, 0, 0.85),
                            (726, "lagi Maha Penyayang", "optima_i", 18, cream, 0, 0.85)],
                           lambda im: metal_text(im, ss_mask(720, 1280, lambda d, s: d.polygon([(x * s, y * s) for x, y in star8_pts(360, 540, 22, 14)], fill=255)), [(518, 562)], M_BRIGHT, sop=0))
    cd = dict(head=[(565, "Menuju hari yang dinanti", "savoye", 76, ("metal", M_BRIGHT, (510, 575))), (612, "SENIN, 20 SEPTEMBER 2027", "optima", 15, gold_l, 6)],
              head_extra=lambda im: metal_text(im, ss_mask(720, 1280, lambda d, s: d.polygon([(x * s, y * s) for x, y in star8_pts(360, 470, 18, 11)], fill=255)), [(452, 488)], M_BRIGHT, sop=0),
              foot=[(985, "Fatimah & Yusuf", "optima_i", 28, gold_l)], foot_extra=lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 930, 150, gap=14, dia=6, lw=1.2), gold_l),
              tile=dict(shape="arch", h=186, fill=(14, 76, 58), grain=0.8, border=(222, 190, 116), accent=(222, 190, 116), num_font="optima", num_col=cream,
                        lab_font="optima", lab_col=gold_l, shadow=(0, 10, 6), shadow_op=0.45, win=(62, 140), num_base=124, line_y=148, label_y=170),
              start=(329, 10, 5, 3))
    closing = closing_layer([(1250, "Jazakumullahu khairan", "savoye", 190, ("metal", M_BRIGHT, (1120, 1270))),
                             (1360, "atas doa dan kehadirannya", "optima_i", 48, cream),
                             (1540, "FATIMAH & YUSUF", "optima", 30, gold_l, 14)], cream)
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, cd=cd, closing=closing, intro_txt=intro_txt,
                bokeh=((255, 214, 140), (255, 236, 190), (200, 240, 210)), bokeh_a=(0.06, 0.18), vig=((0, 16, 10), 0.35),
                intro="text", sparkle=True, hangers=build_lanterns(), hang_flicker=True,
                parts=[("lantern", gen_parts(211, 22, 2.4, 13.5, "lantern", -1, (40, 90), near_every=0, dur_far=9.0, tumble=0, amp=(10, 30), twinkle=True)),
                       ("dust", gen_parts(212, 40, 2.4, 13.5, "dust", -1, (5, 9), near_every=0, dur_far=8.0, tumble=0, amp=(10, 30), twinkle=True))],
                sprites=dict(lantern=[glow_tex((255, 236, 190), (255, 180, 90), 128, 0.10, 0.36, 0.45)], dust=[glow_tex((255, 246, 214), (240, 200, 110))]))


def paint_photo(w, h, seed):
    """abstract painted landscape for the polaroid (no people)"""
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, R(h))[:, None, None]
    sky = np.array((226, 234, 222), np.float32) * (1 - yy) + np.array((248, 226, 204), np.float32) * yy
    im = Image.fromarray(np.clip(sky + 0 * np.zeros((1, R(w), 1)), 0, 255).astype(np.uint8)).convert("RGBA")
    sun = ss_mask(w, h, lambda d, s: d.ellipse([(w * 0.62) * s, (h * 0.22) * s, (w * 0.62 + 170) * s, (h * 0.22 + 170) * s], fill=255)).filter(ImageFilter.GaussianBlur(6 * S))
    paint(im, sun, (246, 196, 160), 0.9)
    for i, (yb, col, amp) in enumerate([(0.55, (170, 190, 160), 60), (0.66, (132, 160, 132), 70), (0.78, (98, 128, 104), 50)]):
        ph = rng.uniform(0, 6)
        pts = [(x, h * yb + amp * math.sin(x / w * math.pi * (1.3 + i * 0.5) + ph) + 14 * math.sin(x / 37 + ph)) for x in np.linspace(-10, w + 10, 60)]
        m = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in pts + [(w + 10, h + 10), (-10, h + 10)]], fill=255)).filter(ImageFilter.GaussianBlur(1.5 * S))
        paint(im, m, col, 0.92)
        rows = ss_mask(w, h, lambda d, s: [d.line([(x * s, (y + 20 + k * 26) * s), ((x + 60) * s, (y + 24 + k * 26) * s)], fill=255, width=int(3 * s))
                                           for k in range(4) for x, y in pts[::4]])
        paint(im, Image.fromarray((np.asarray(rows, np.float32) * np.asarray(m, np.float32) / 255).astype(np.uint8)), tuple(int(c * 0.9) for c in col), 0.22)
    wc = rng.normal(0, 1, (int(h / 30) + 2, int(w / 30) + 2)).astype(np.float32)
    wc = np.asarray(Image.fromarray(wc, "F").resize((R(w), R(h)), Image.BICUBIC))
    arr = np.asarray(im, np.float32)
    arr[..., :3] = arr[..., :3] * (1 + wc[..., None] * 0.010)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def style_rustic():
    w, h = DW_, DH_
    ink, sage, brown = (58, 70, 54), (122, 150, 124), (92, 64, 40)
    front, fa = card_canvas((250, 248, 240), 121, "polaroid", 0.5)
    photo = paint_photo(940, 940, 7)
    pm = ss_mask(w, h, lambda d, s: d.rectangle([70 * s, 70 * s, 1010 * s, 1010 * s], fill=255))
    front.alpha_composite(photo, (R(70), R(70)))
    inner = mask_sub(pm, ss_mask(w, h, lambda d, s: d.rectangle([84 * s, 84 * s, 996 * s, 996 * s], fill=255)).filter(ImageFilter.GaussianBlur(8 * S)))
    paint(front, Image.fromarray((np.asarray(inner, np.float32) * 0.6).astype(np.uint8)), (60, 50, 40), 0.5)
    tape = ss_mask(w, h, lambda d, s: d.polygon([(400 * s, 20 * s), (700 * s, 6 * s), (706 * s, 70 * s), (406 * s, 84 * s)], fill=255))
    paint(front, tape, (200, 214, 196), 0.75)
    for cx, cy, a in ((150, 940, -0.5), (186, 900, 0.2), (126, 880, -1.0), (930, 120, 2.6), (900, 160, 3.2)):
        paint(front, ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in _oval(cx, cy, 34, 22, a)], fill=255)), (140, 170, 150), 0.9)
    names = None
    lines_onto(front, w, h, [(1196, "Nadia & Raka", "signp", 140, ink), (1290, "12 · 06 · 2027", "amtype", 38, brown, 4), (1350, "Kebun Teh Kemuning", "amtype", 24, brown, 3, 0.7)])

    back, ba = card_canvas((196, 160, 116), 122, "polaroid", 1.8)
    lines_onto(back, w, h, [(250, "SIMPAN TANGGALNYA", "amtype", 30, brown, 6), (460, "Sabtu, 12 Juni 2027", "signp", 110, ink),
                            (560, "Kebun Teh Kemuning, Karanganyar", "amtype", 34, brown)])
    twine = ss_mask(w, h, lambda d, s: [d.line([(x * s, (660 + 6 * math.sin(x / 40 + o)) * s) for x in range(0, w, 8)], fill=255, width=int(3 * s)) for o in (0, 1.6)])
    paint(back, twine, (226, 210, 180), 0.95)
    paint(back, ss_mask(w, h, lambda d, s: (d.ellipse([770 * s, 160 * s, 960 * s, 350 * s], outline=255, width=int(4 * s)),
                                            T(d, s, 278, "N & R", "amtype", 40, x=865))), (150, 60, 50), 0.55)
    panel(back, w, h, 850, 1300, (222, 196, 160), 0.6, brown, dashed=True)
    guest_block(back, w, h, "amtype", brown, "signp", ink, brown, "amtype", brown, cap="Kepada Yth.", cap_size=28, name_size=80)

    bg = grad_bg((240, 232, 216), (224, 210, 186), (250, 246, 236), 0.5)
    bgp = paper(W, H, (0, 0, 0), 131, 0.8)
    arr = np.asarray(bg, np.float32)
    arr[..., :3] += bgp
    bg = Image.frombytes("RGBA", (W, H), np.clip(arr, 0, 255).astype(np.uint8).tobytes())

    def sprig(d, s, x0, y0, ang, n, length):
        pts = [(x0 + length * u * math.cos(ang) + 12 * math.sin(u * 4), y0 + length * u * math.sin(ang)) for u in np.linspace(0, 1, 30)]
        d.line([(x * s, y * s) for x, y in pts], fill=255, width=int(3 * s))
        for i in range(1, n):
            x, y = pts[int(i * 29 / n)]
            for sg in (1, -1):
                lx, ly = x + sg * 20 * math.cos(ang + sg * 1.2), y + sg * 20 * math.sin(ang + sg * 1.2)
                d.polygon([(px * s, py * s) for px, py in _oval(lx, ly, 18 - i * 0.8, 13 - i * 0.6, ang + sg * 1.2)], fill=255)

    overlay_pattern(bg, lambda d, s: (sprig(d, s, -10, 120, 0.5, 9, 260), sprig(d, s, 40, -10, 1.2, 7, 200), sprig(d, s, 730, 1180, 3.6, 9, 280), sprig(d, s, 690, 1290, 4.3, 7, 220)), (132, 160, 138), 0.8)
    cd = dict(head=[(570, "Sebentar lagi...", "signp", 80, ink), (614, "SABTU, 12 JUNI 2027", "amtype", 15, brown, 5)],
              foot=[(975, "Nadia & Raka", "signp", 44, sage)], foot_extra=lambda im: paint(im, ss_mask(720, 1280, lambda d, s: [d.line([(x * s, (918 + 4 * math.sin(x / 20)) * s) for x in range(220, 501, 6)], fill=255, width=int(2 * s))]), (170, 140, 100), 0.9),
              tile=dict(shape="tag", h=168, fill=(206, 172, 128), grain=1.6, border=None, accent=(120, 90, 60), num_font="amtype", num_col=(62, 44, 28),
                        lab_font="amtype", lab_col=(96, 70, 44), shadow=(60, 40, 20), shadow_op=0.3, hole=True, win=(36, 116), num_base=100, line_y=126, label_y=150),
              start=(203, 14, 20, 3))
    closing = closing_layer([(1250, "Sampai jumpa di kebun!", "signp", 150, ink), (1400, "NADIA & RAKA", "amtype", 32, brown, 12)], brown, 0.6)
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, cd=cd, closing=closing,
                bokeh=((255, 255, 250), (200, 220, 200), (240, 226, 200)), bokeh_a=(0.08, 0.2), vig=((90, 70, 40), 0.18),
                intro="sign", sparkle=False,
                parts=[("leaf", gen_parts(221, 40, 2.4, 13.0, "leaf", 1, (34, 52), variants=3, dur_near=4.5, dur_far=8.0))],
                sprites=dict(leaf=[leaf_tex(1, (118, 150, 140), (168, 190, 176)), leaf_tex(2, (100, 132, 118), (150, 176, 160)), leaf_tex(3, (140, 164, 150), (190, 206, 194))]))


def style_ultah():
    w, h = DW_, DH_
    coral, teal, orange, navy = (255, 96, 110), (30, 168, 170), (255, 160, 40), (64, 64, 110)
    cols = [(255, 96, 110), (255, 196, 60), (40, 190, 190), (130, 110, 230), (90, 200, 120)]
    front, fa = card_canvas((255, 253, 246), 141, "round", 0.4)
    paint(front, ring_mask(w, h, "round", 64, 3), teal)
    dots = [(x, 36) for x in range(80, w - 60, 54)] + [(x, h - 36) for x in range(80, w - 60, 54)] + [(36, y) for y in range(90, h - 60, 54)] + [(w - 36, y) for y in range(90, h - 60, 54)]
    for i, c in enumerate(cols):
        paint(front, ss_mask(w, h, lambda d, s: [d.ellipse([(x - 9) * s, (y - 9) * s, (x + 9) * s, (y + 9) * s], fill=255) for j, (x, y) in enumerate(dots) if j % 5 == i]), c)
    for i, c in enumerate(cols):
        paint(front, ss_mask(w, h, lambda d, s: [d.polygon([(x * s, 120 * s), ((x + 90) * s, 120 * s), ((x + 45) * s, 210 * s)], fill=255) for j, x in enumerate(range(110, w - 150, 100)) if j % 5 == i]), c)
    paint(front, ss_mask(w, h, lambda d, s: d.line([(100 * s, 118 * s), ((w - 100) * s, 118 * s)], fill=255, width=int(3 * s))), navy, 0.7)
    names = lines_onto(front, w, h, [(340, "YUK DATANG KE PESTA", "chalk", 30, teal, 4), (480, "Ulang Tahun", "marker", 96, coral),
                                     (760, "Arka", "rounded", 250, ("metal", M_CANDY, (570, 770))), (890, "yang ke-7", "marker", 84, orange),
                                     (1350, "14 · 03 · 2027", "chalk", 40, navy, 3)])
    badge = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in [(w / 2 + (120 if i % 2 == 0 else 84) * math.cos(i * math.pi / 8), 1100 + (120 if i % 2 == 0 else 84) * math.sin(i * math.pi / 8)) for i in range(16)]], fill=255))
    paint(front, offset_mask(badge, 4 * S, 8 * S).filter(ImageFilter.GaussianBlur(6 * S)), (150, 100, 40), 0.35)
    paint(front, badge, (255, 205, 60))
    lines_onto(front, w, h, [(1160, "7", "rounded", 170, (255, 255, 255))])
    back, ba = card_canvas((255, 248, 222), 142, "round", 0.4)
    paint(back, ring_mask(w, h, "round", 40, 4), coral)
    for i, c in enumerate(cols):
        rng = np.random.default_rng(300 + i)
        pts = rng.uniform([80, 80], [w - 80, h - 80], (14, 2))
        paint(back, ss_mask(w, h, lambda d, s: [d.rectangle([(x - 7) * s, (y - 12) * s, (x + 7) * s, (y + 12) * s], fill=255) for x, y in pts]), c, 0.35)
    lines_onto(back, w, h, [(300, "Catat tanggalnya!", "marker", 78, coral), (470, "Minggu, 14 Maret 2027", "chalk", 58, navy),
                            (556, "Rumah Ceria, Jakarta Selatan", "chalk", 42, teal)])
    panel(back, w, h, 850, 1300, (255, 255, 255), 0.85, teal, dashed=True)
    guest_block(back, w, h, "chalk", coral, "marker", navy, teal, "chalk", navy, cap="UNTUK", name="Teman-teman tersayang", small="jangan lupa datang ya!", cap_size=28, name_size=62)

    bg = grad_bg((186, 230, 255), (255, 238, 196), (255, 255, 255), 0.45)
    cl = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(cl)
    for cx, cy, sc in ((120, 220, 1.0), (560, 140, 0.8), (620, 1120, 1.1), (90, 1040, 0.7)):
        for dx, dy, r in ((0, 0, 60), (55, 10, 46), (-50, 14, 40), (20, -30, 44)):
            d.ellipse([R(cx + (dx - r) * sc), R(cy + (dy - r) * sc), R(cx + (dx + r) * sc), R(cy + (dy + r) * sc)], fill=255)
    paint(bg, cl.filter(ImageFilter.GaussianBlur(6 * S)), (255, 255, 255), 0.75)
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    seven = ss_mask(720, 1280, lambda d, s: T(d, s, 820, "7", "rounded", 520, x=360))
    seven_o = ss_mask(720, 1280, lambda d, s: T(d, s, 820, "7", "rounded", 520, x=360, stroke=12))
    paint(hl, offset_mask(seven_o, 6 * S, 12 * S).filter(ImageFilter.GaussianBlur(8 * S)), (120, 60, 80), 0.35)
    paint(hl, seven_o, (255, 255, 255))
    metal_text(hl, seven, [(450, 830)], M_CANDY, sop=0)
    hl_txt = text_layer([(330, "Arka", "rounded", 84, teal), (950, "tahun!", "marker", 92, coral), (1010, "Yuk rayakan bersama", "chalk", 26, navy, 2)])
    closing = closing_layer([(1230, "Ayo datang", "marker", 150, coral), (1380, "& rayakan!", "marker", 150, orange), (1530, "ARKA · 7 TAHUN", "chalk", 40, teal, 8)], navy, 0.6)
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, closing=closing, hl=hl.convert("RGBa"), hl_txt=hl_txt,
                bokeh=((255, 255, 255), (255, 220, 120), (255, 170, 190), (160, 220, 255)), bokeh_a=(0.10, 0.28), vig=((40, 60, 120), 0.10),
                intro="box", sparkle=True,
                parts=[("balloon", gen_parts(241, 16, 2.0, 13.0, "balloon", -1, (80, 110), z_far=(1450, 2600), near_every=5, dur_near=4.0, dur_far=8.5, tumble=0, amp=(15, 35), variants=5)),
                       ("confetti", gen_parts(242, 60, 2.6, 13.0, "confetti", 1, (12, 18), near_every=0, dur_far=6.0, tumble=2.5, variants=5))],
                sprites=dict(balloon=[balloon_tex(c) for c in cols], confetti=[confetti_tex(c) for c in cols]))


def style_navy():
    w, h = DW_, DH_
    base = (20, 34, 74)
    champ, cream = (220, 200, 156), (238, 232, 216)
    front, fa = card_canvas(base, 151, "deco", 0.6)

    def frame(im):
        paint(im, vgrad(im.size, 0.45), (6, 12, 30), 1.0)
        paint(im, ring_mask(w, h, "deco", 26, 3.5), champ)
        paint(im, ring_mask(w, h, "deco", 46, 1.3), champ, 0.8)
        paint(im, ss_mask(w, h, lambda d, s: (deco_fan(d, s, w / 2, 46, 160, 0, 180, 13, 1.6), deco_fan(d, s, w / 2, h - 46, 120, 180, 360, 11, 1.4),
                                              [d.line([(x * s, 260 * s), (x * s, (h - 260) * s)], fill=255, width=max(1, int(1.2 * s))) for x in (78, 90, w - 78, w - 90)])), champ, 0.8)

    frame(front)
    paint(front, ss_mask(w, h, lambda d, s: [d.polygon([((w / 2 + o) * s, 1062 * s), ((w / 2 + o + 9) * s, 1071 * s), ((w / 2 + o) * s, 1080 * s), ((w / 2 + o - 9) * s, 1071 * s)], fill=255) for o in (-30, 0, 30)]
                      + [d.line([((w / 2 - 230) * s, 1071 * s), ((w / 2 - 50) * s, 1071 * s)], fill=255, width=int(1.6 * s)), d.line([((w / 2 + 50) * s, 1071 * s), ((w / 2 + 230) * s, 1071 * s)], fill=255, width=int(1.6 * s))]), champ)
    names = lines_onto(front, w, h, [(420, "PERNIKAHAN", "futura", 28, champ, 16), (670, "Sekar", "bodoni_i", 196, ("metal", M_CHAMP, (540, 690))),
                                     (790, "&", "futura", 60, champ), (960, "Damar", "bodoni_i", 196, ("metal", M_CHAMP, (830, 980))),
                                     (1170, "18 · 09 · 2027", "futura", 40, cream, 8), (1240, "JAKARTA", "futura", 22, cream, 14, 0.75)])
    back, ba = card_canvas(base, 152, "deco", 0.6)
    frame(back)
    lines_onto(back, w, h, [(320, "RESEPSI PERNIKAHAN", "futura", 24, champ, 12), (490, "Sabtu, 18 September 2027", "bodoni", 62, cream),
                            (575, "The Ballroom, Jakarta", "bodoni_i", 54, champ)])
    paint(back, ss_mask(w, h, lambda d, s: ornament(d, s, w / 2, 680, 120, gap=14, dia=7, lw=1.4)), champ)
    panel(back, w, h, 850, 1300, (10, 20, 48), 0.7, champ, kind="deco")
    guest_block(back, w, h, "futura", champ, "bodoni_i", cream, champ, "bodoni_i", cream, cap_size=24, name_size=60)

    bg = grad_bg((22, 38, 80), (6, 10, 28), (40, 60, 110), 0.35, 0.3)
    rng = np.random.default_rng(161)
    st = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(st)
    for _ in range(420):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H * 0.85), rng.uniform(0.4, 1.4) * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.uniform(90, 255)))
    paint(bg, st.filter(ImageFilter.GaussianBlur(0.4 * S)), (255, 248, 230), 0.9)
    mx, my, mr = 560, 180, 46
    halo = ss_mask(720, 1280, lambda d, s: d.ellipse([(mx - 120) * s, (my - 120) * s, (mx + 120) * s, (my + 120) * s], fill=255), ss=1).filter(ImageFilter.GaussianBlur(40 * S))
    paint(bg, halo, (240, 230, 200), 0.25)
    moon = mask_sub(ss_mask(720, 1280, lambda d, s: d.ellipse([(mx - mr) * s, (my - mr) * s, (mx + mr) * s, (my + mr) * s], fill=255)),
                    ss_mask(720, 1280, lambda d, s: d.ellipse([(mx - mr + 24) * s, (my - mr - 12) * s, (mx + mr + 24) * s, (my + mr - 12) * s], fill=255)))
    paint(bg, moon.filter(ImageFilter.GaussianBlur(6 * S)), (255, 244, 210), 0.6)
    paint(bg, moon, (250, 240, 214))
    tw = [(rng.uniform(20, 700), rng.uniform(20, 1000), rng.uniform(10, 22), rng.uniform(1.4, 3.0), rng.uniform(0, 6)) for _ in range(28)]
    cd = dict(head=[(565, "Menuju malam bahagia", "bodoni_i", 54, ("metal", M_CHAMP, (520, 575))), (612, "SABTU, 18 SEPTEMBER 2027", "futura", 14, champ, 7)],
              head_extra=lambda im: orn_layer(im, lambda d, s: deco_fan(d, s, 360, 492, 46, 180, 360, 9, 1.2), champ),
              foot=[(975, "Sekar & Damar", "bodoni_i", 32, champ)], foot_extra=lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 918, 150, gap=14, dia=6, lw=1.2), champ),
              tile=dict(shape="deco", fill=(22, 38, 82), grain=0.6, border=champ, accent=champ, num_font="futura", num_col=cream,
                        lab_font="futura", lab_col=champ, shadow=(0, 0, 10), shadow_op=0.5, num_size=58),
              start=(330, 20, 0, 3))
    closing = closing_layer([(1150, "Sampai jumpa di", "bodoni_i", 80, cream), (1300, "malam bahagia kami", "bodoni_i", 104, ("metal", M_CHAMP, (1200, 1320))),
                             (1500, "SEKAR & DAMAR", "futura", 30, champ, 18)], cream, 0.5)
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, cd=cd, closing=closing, twinkles=tw,
                bokeh=((240, 226, 190), (150, 170, 220), (255, 255, 255)), bokeh_a=(0.03, 0.10), vig=((0, 0, 8), 0.4),
                intro="fly", sparkle=True,
                parts=[("glitter", gen_parts(251, 40, 0.5, 13.0, "glitter", 1, (14, 26), near_every=0, dur_far=9.0, tumble=0, amp=(10, 30), twinkle=True))],
                sprites=dict(glitter=[glow_tex((255, 250, 236), (226, 204, 150), 64, 0.08, 0.30, 0.5)]))


def style_bali():
    w, h = DW_, DH_
    gold_d, ink, yel = (180, 124, 24), (70, 50, 30), (247, 206, 70)
    front, fa = card_canvas((255, 252, 244), 171, "stepped", 0.6)

    def frame(im):
        paint(im, ring_mask(w, h, "stepped", 22, 4.5), (214, 160, 40))
        paint(im, ring_mask(w, h, "stepped", 42, 1.6), (214, 160, 40), 0.8)
        band = ss_mask(w, h, lambda d, s: d.rectangle([60 * s, 1380 * s, (w - 60) * s, 1452 * s], fill=255))
        paint(im, band, yel, 0.9)
        pm = ss_mask(w, h, lambda d, s: patra(d, s, w, h, 70, 1.6), ss=2)
        paint(im, Image.fromarray((np.asarray(pm, np.float32) * np.asarray(band, np.float32) / 255).astype(np.uint8)), (200, 140, 20), 0.8)
        fm = ss_mask(w, h, lambda d, s: flower5(d, s, w / 2, 112, 38, 255, -0.3))
        paint(im, offset_mask(fm, 2 * S, 4 * S).filter(ImageFilter.GaussianBlur(3 * S)), (150, 110, 40), 0.3)
        paint(im, fm, (255, 255, 255))
        paint(im, ss_mask(w, h, lambda d, s: d.ellipse([(w / 2 - 12) * s, 100 * s, (w / 2 + 12) * s, 124 * s], fill=255)), (246, 190, 50))
        paint(im, ss_mask(w, h, lambda d, s: [d.polygon([(x * s, y * s) for x, y in _oval(w / 2 + sg * 70, 118, 34, 12, sg * 0.3)], fill=255) for sg in (1, -1)]), (120, 160, 90), 0.9)

    frame(front)
    paint(front, ss_mask(w, h, lambda d, s: (ornament(d, s, w / 2, 470, 140), ornament(d, s, w / 2, 1060, 200, gap=18, dia=8))), (214, 160, 40))
    names = lines_onto(front, w, h, [(430, "PAWIWAHAN", "herc", 34, gold_d, 10), (690, "Dewa", "tratt", 196, ("metal", M_BALI, (560, 700))),
                                     (800, "&", "tratt", 100, (200, 150, 40)), (960, "Ayu", "tratt", 196, ("metal", M_BALI, (840, 980))),
                                     (1160, "09 · 10 · 2027", "hoefler", 48, ink, 4), (1232, "UBUD, BALI", "herc", 26, ink, 10, 0.75)])
    back, ba = card_canvas((255, 252, 244), 172, "stepped", 0.6)
    frame(back)
    lines_onto(back, w, h, [(330, "UPACARA PAWIWAHAN", "herc", 28, gold_d, 8), (490, "Sabtu, 9 Oktober 2027", "hoefler", 62, ink),
                            (575, "Pura Taman, Ubud", "hoefler_i", 54, gold_d)])
    paint(back, ss_mask(w, h, lambda d, s: ornament(d, s, w / 2, 680, 120, gap=14, dia=7, lw=1.4)), (214, 160, 40))
    panel(back, w, h, 830, 1290, (250, 236, 190), 0.6, (214, 160, 40))
    guest_block(back, w, h, "herc", gold_d, "hoefler_i", ink, (214, 160, 40), "hoefler_i", ink, cap_size=26, name_size=58)

    bg = grad_bg((255, 251, 240), (248, 226, 160), (255, 255, 250), 0.5)
    overlay_pattern(bg, lambda d, s: patra(d, s, 720, 1280, 96, 1.2), (200, 150, 40), 0.07)
    intro_txt = text_layer([(150, "Om Swastyastu", "tratt", 50, ("metal", M_BALI, (110, 158)))],
                           lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 184, 80, gap=12, dia=5, lw=1.2), (214, 160, 40)))
    cd = dict(head=[(565, "Menuju hari suci", "tratt", 64, ("metal", M_BALI, (515, 575))), (612, "SABTU, 9 OKTOBER 2027", "herc", 16, gold_d, 5)],
              head_extra=lambda im: paint(im, ss_mask(720, 1280, lambda d, s: flower5(d, s, 360, 470, 22, 255, -0.3)), (255, 255, 255)) or paint(im, ss_mask(720, 1280, lambda d, s: d.ellipse([352 * s, 462 * s, 368 * s, 478 * s], fill=255)), (246, 190, 50)),
              foot=[(975, "Dewa & Ayu", "hoefler_i", 32, gold_d)], foot_extra=lambda im: orn_layer(im, lambda d, s: ornament(d, s, 360, 918, 150, gap=14, dia=6, lw=1.2), (214, 160, 40)),
              tile=dict(shape="rect", fill=(255, 253, 246), grain=0.6, border=(214, 160, 40), accent=(214, 160, 40), num_font="hoefler", num_col=ink,
                        lab_font="herc", lab_col=gold_d, shadow=(150, 110, 40), shadow_op=0.25),
              start=(380, 4, 30, 3))
    closing = closing_layer([(1240, "Om Santih, Santih,", "tratt", 96, ("metal", M_BALI, (1160, 1250))), (1360, "Santih, Om", "tratt", 96, ("metal", M_BALI, (1280, 1370))),
                             (1520, "DEWA & AYU", "herc", 34, gold_d, 12)], ink, 0.55)
    return dict(front=finish(front, fa), names=names, back=finish(back, ba), bg=bg, cd=cd, closing=closing, intro_txt=intro_txt,
                bokeh=((255, 255, 255), (255, 226, 130), (255, 244, 210)), bokeh_a=(0.10, 0.26), vig=((120, 90, 20), 0.12),
                intro="split", sparkle=True, hangers=build_penjor(),
                parts=[("kamboja", gen_parts(271, 26, 2.4, 13.0, "kamboja", 1, (40, 56), dur_near=5.0, dur_far=9.0, tumble=0.6))],
                sprites=dict(kamboja=[kamboja_tex()]))


STYLES = {"jawa-keraton": style_keraton, "islami-zamrud": style_islami, "rustic-garden": style_rustic,
          "ultah-ceria": style_ultah, "navy-malam": style_navy, "bali-kuning": style_bali}
STYLE_MUSIC = {"jawa-keraton": "gamelan.mp3", "islami-zamrud": "religi.mp3", "rustic-garden": "akustik.mp3",
               "ultah-ceria": "ceria.mp3", "navy-malam": "khidmat.mp3", "bali-kuning": "gamelan.mp3"}


def build_gallery_assets(slug):
    fn = STYLES[slug]
    st = fn()
    A = dict(slug=slug, st=st)
    A["bg"] = st["bg"]
    A["bokeh_far"] = bokeh_cols(st["bokeh"], 70, 6, 22, st["bokeh_a"][0] * 1.6, st["bokeh_a"][1] * 1.6, 2.2, 1, 60)
    A["bokeh_near"] = bokeh_cols(st["bokeh"], 16, 34, 80, st["bokeh_a"][0], st["bokeh_a"][1], 7, 2, 90)
    A["vignette"] = vignette_col(*st["vig"])
    A["dither"] = build_dither()
    A["card_front"] = Tex(st["front"], extra=st["names"]) if st["names"] is not None else Tex(st["front"])
    A["has_shine"] = st["names"] is not None
    A["card_back"] = Tex(st["back"])
    A["sparkle"] = build_sparkle()
    A["closing"] = st["closing"]
    if "cd" in st:
        A["cd"] = build_cd_style(st["cd"])
    intro = st["intro"]
    A["intro_assets"] = {"doors": build_doors, "split": build_candi, "box": build_box, "sign": build_sign}.get(intro, lambda: {})()
    A["parts"] = []
    for _, defs in st["parts"]:
        A["parts"] += defs
    A["sprites"] = st["sprites"]
    return A


# ---------------------------------------------------------------- gallery timeline
G_LIFT = (2.5, 3.7)
G_SHINE = (3.9, 1.8)


def g_intro_state(t, A):
    """returns dict: card start pose (dict), grouped (card drawn inside the intro group), clip, alpha"""
    kind = A["st"]["intro"]
    hero_far = dict(X=0.0, Y=0.0, Z=1800.0, rx=0.0, ry=0.0, rz=0.0)
    if kind in ("doors", "split"):
        return dict(pose=hero_far, grouped=True, clip=None, alpha=seg(t, 1.2, 2.0))
    if kind == "box":
        e = seg(t, 0.0, 1.2)
        bp = dict(X=lerp(-80, 0, e), Y=lerp(420, 250, e), Z=lerp(2600, 1700, e), rx=lerp(14, -6, e), ry=lerp(-38, -14, e), rz=lerp(-8, 0, e))
        sl = seg(t, 1.6, 2.6)
        cy = lerp(-190 + 24 + CH / 2, -190 - 24 - CH / 2, sl)
        P = Pose(**bp)
        C = P.world([(0, cy, 150)])[0]
        clip = (190 - 4) - (cy - CH / 2)
        return dict(pose=dict(X=C[0], Y=C[1], Z=C[2], rx=bp["rx"], ry=bp["ry"], rz=bp["rz"]), grouped=True, clip=clip, alpha=1.0, box=bp)
    if kind == "sign":
        e = seg(t, 1.7, 3.0)
        return dict(pose=dict(X=lerp(-60, 0, e), Y=lerp(1000, 300, e), Z=1500, rx=lerp(-30, -8, e), ry=0, rz=lerp(-14, 6, e)), grouped=False, clip=None, alpha=1.0)
    if kind == "text":
        e = seg(t, 2.1, 3.0)
        return dict(pose=dict(X=0, Y=lerp(260, 60, e), Z=lerp(4800, 2400, e), rx=lerp(35, 8, e), ry=0, rz=0), grouped=False, clip=None, alpha=seg(t, 2.1, 2.8))
    if kind == "fly":
        e = seg(t, 0.2, 2.6)
        return dict(pose=dict(X=lerp(-520, -40, e), Y=lerp(-420, 0, e), Z=lerp(5600, 2000, e), rx=lerp(28, 6, e), ry=lerp(-58, -16, e), rz=lerp(-18, -2, e)),
                    grouped=False, clip=None, alpha=seg(t, 0.2, 0.9))
    return dict(pose=hero_far, grouped=False, clip=None, alpha=1.0)


def g_card_state(t, ist):
    L = seg(t, *G_LIFT)
    sp = ist["pose"]
    push = seg(t, 3.4, 6.3)
    flip = seg(t, 6.3, 7.5)
    rec = seg(t, 9.0, 9.9)
    hero = np.array([0.0, -12.0, lerp(1370, 1300, push)])
    C = np.array([sp["X"], sp["Y"], sp["Z"]]) * (1 - L) + hero * L
    C[2] += 300 * math.sin(math.pi * flip) + 1800 * rec
    C[1] -= 120 * rec
    sway_w = seg(t, 4.0, 4.8) * (1 - seg(t, 5.6, 6.3))
    sway_b = seg(t, 7.4, 8.0) * (1 - seg(t, 8.4, 9.0))
    ry = 14 * math.sin(math.pi * L) + 180 * flip + 4.5 * math.sin(2 * math.pi * (t - 4.0) / 2.3) * sway_w + 4 * math.sin(2 * math.pi * (t - 7.4) / 1.6) * sway_b
    rx = -10 * math.sin(math.pi * L) + 2 * math.sin(2 * math.pi * (t - 4.0) / 2.3) * sway_w - 6 * rec
    rz = -2 * math.sin(math.pi * flip)
    pose = dict(X=C[0], Y=C[1], Z=C[2], rx=rx + sp["rx"] * (1 - L), ry=ry + sp["ry"] * (1 - L), rz=rz + sp["rz"] * (1 - L))
    alpha = ist["alpha"] * (1 - seg(t, 9.0, 9.8))
    clip = ist["clip"] if L <= 0 else None
    lifted = L > 0 or not ist["grouped"]
    return pose, alpha, 7 * S * rec, clip, lifted


def g_draw_card(frame, A, pose, alpha, blur, clip, t):
    quad = pose.project(rect_pts(CW, CH))
    front = facing(quad)
    sh = lambert(pose.normal(), back=not front)
    ry = math.atan2(pose.R[0, 2], pose.R[2, 2])
    tex = A["card_front"] if front else A["card_back"]
    if not front:
        quad = pose.project([(CW / 2, -CH / 2, 0), (-CW / 2, -CH / 2, 0), (-CW / 2, CH / 2, 0), (CW / 2, CH / 2, 0)])
    shine_p = (t - G_SHINE[0]) / G_SHINE[1]
    sheen = 0.16 * abs(math.sin(ry)) ** 0.8

    def modify(arr, k, w, h):
        P = Tex.PAD
        if clip is not None:
            r = int(P + clip / CH * h)
            if r < arr.shape[0]:
                arr[max(r, 0):] = 0
        need_shine = front and A["has_shine"] and -0.2 < shine_p < 1.3
        if need_shine or sheen > 0.01:
            hh, ww = arr.shape[:2]
            yy = np.arange(hh, dtype=np.float32)[:, None] / hh
            xx = np.arange(ww, dtype=np.float32)[None, :] / ww
            diag = xx * 0.8 + yy * 0.45
            a = arr.astype(np.float32)
            add = np.zeros((hh, ww), np.float32)
            if sheen > 0.01:
                add += sheen * np.exp(-((diag - (0.62 - 0.5 * math.sin(ry) * (1 if front else -1))) / 0.16) ** 2)
            if need_shine:
                add += 0.7 * np.exp(-((diag - lerp(-0.1, 1.35, shine_p)) / 0.05) ** 2) * tex.extra[k]
            a[..., :3] += add[..., None] * (a[..., 3:4] * np.array([1.0, 0.97, 0.88]) - a[..., :3])
            arr[...] = np.clip(a, 0, 255).astype(np.uint8)

    draw_quad(frame, tex, quad, alpha=alpha, blur=blur, shade=sh, modify=modify)


def g_draw_intro(frame, A, t, ist, card_cb):
    """draw the intro object (and the card inside it) into a group layer, fade group"""
    kind = A["st"]["intro"]
    IA = A["intro_assets"]
    if kind == "doors":
        ga = seg(t, 0.0, 0.8) * (1 - seg(t, 2.7, 3.5))
        if ga <= 0.003:
            if seg(t, *G_LIFT) <= 0:
                card_cb(frame)
            return
        grp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if seg(t, *G_LIFT) <= 0:
            card_cb(grp)
        e = seg(t, 0.0, 1.0)
        op = 102 * seg(t, 1.1, 2.6)
        Zd = lerp(2300, 1500, e) - 220 * seg(t, 2.0, 3.4)
        blur = 8 * S * seg(t, 2.4, 3.3)
        for side in (-1, 1):
            hx = side * 330
            pose = Pose(hx, 30, Zd, lerp(8, 0, e), (op if side < 0 else -op) + lerp(-18, 0, e), 0)
            pts = [(0, -450, 0), (330, -450, 0), (330, 450, 0), (0, 450, 0)] if side < 0 else [(-330, -450, 0), (0, -450, 0), (0, 450, 0), (-330, 450, 0)]
            q = pose.project(pts)
            fr = facing(q)
            tex = (IA["left"] if side < 0 else IA["right"]) if fr else IA["back"]
            if not fr:
                q = q[[1, 0, 3, 2]]
            shadow(grp, [q], (8, 16), 18, 0.3)
            draw_quad(grp, tex, q, blur=blur, shade=lambert(pose.normal(), back=not fr))
        frame.alpha_composite(fade_rgba(grp, ga))
        return
    if kind == "split":
        ga = seg(t, 0.0, 0.8) * (1 - seg(t, 2.6, 3.4))
        if ga <= 0.003:
            if seg(t, *G_LIFT) <= 0:
                card_cb(frame)
            return
        grp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if seg(t, *G_LIFT) <= 0:
            card_cb(grp)
        e = seg(t, 0.0, 1.0)
        o = seg(t, 1.1, 2.8)
        Zg = lerp(2200, 1500, e) - 400 * o
        blur = 7 * S * seg(t, 2.2, 3.2)
        for side in (-1, 1):
            inner = side * lerp(14, 360, o)
            cxw = inner + side * 160
            pose = Pose(cxw, 40, Zg, 0, side * lerp(0, 22, o) + lerp(-12, 0, e), 0)
            q = pose.project(rect_pts(320, 1000))
            shadow(grp, [q], (10, 18), 20, 0.25)
            draw_quad(grp, IA["left"] if side < 0 else IA["right"], q, blur=blur, shade=lambert(pose.normal()))
        frame.alpha_composite(fade_rgba(grp, ga))
        return
    if kind == "box":
        ga = seg(t, 0.0, 0.7) * (1 - seg(t, 2.9, 3.6))
        bp = ist["box"]
        if ga <= 0.003:
            if seg(t, *G_LIFT) <= 0:
                card_cb(frame)
            return
        grp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        P = Pose(**bp)
        bw, bh, bd = 300, 190, 300
        front_q = P.project([(-bw, -bh, 0), (bw, -bh, 0), (bw, bh, 0), (-bw, bh, 0)])
        top_q = P.project([(-bw, -bh, bd), (bw, -bh, bd), (bw, -bh, 0), (-bw, -bh, 0)])
        shadow(grp, [front_q, top_q], (10, 24), 22, 0.28)
        draw_quad(grp, IA["inside"], top_q, shade=0.9)
        for sx in (-1, 1):
            if sx > 0:
                sq = P.project([(bw, -bh, 0), (bw, -bh, bd), (bw, bh, bd), (bw, bh, 0)])
            else:
                sq = P.project([(-bw, -bh, bd), (-bw, -bh, 0), (-bw, bh, 0), (-bw, bh, bd)])
            if facing(sq):
                draw_quad(grp, IA["side"], sq, shade=lambert(P.R @ np.array([sx * 1.0, 0, 0])))
        if seg(t, *G_LIFT) <= 0:
            card_cb(grp)
        draw_quad(grp, IA["front"], front_q, shade=lambert(P.normal()))
        # lid
        up = seg(t, 1.0, 1.6)
        fly = seg(t, 1.6, 2.5)
        lr = math.radians(14 * up + 34 * fly)
        dx, dy = 760 * fly, -240 * up - 520 * fly
        la = 1 - fly
        if la > 0.003:
            lc = np.array([0, -205, 150])

            def L(pts):
                out = []
                for x, y, z in pts:
                    v = np.array([x, y, z]) - lc
                    v = np.array([v[0] * math.cos(lr) - v[1] * math.sin(lr), v[0] * math.sin(lr) + v[1] * math.cos(lr), v[2]]) + lc + [dx, dy, 0]
                    out.append(v)
                return P.project(out)

            lw_ = 315
            lid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_quad(lid, IA["lid_top"], L([(-lw_, -250, 308), (lw_, -250, 308), (lw_, -250, -8), (-lw_, -250, -8)]), shade=1.02)
            draw_quad(lid, IA["bow"], L([(-120, -400, 150), (120, -400, 150), (120, -250, 150), (-120, -250, 150)]))
            draw_quad(lid, IA["lid_front"], L([(-lw_, -250, -8), (lw_, -250, -8), (lw_, -160, -8), (-lw_, -160, -8)]), shade=lambert(P.normal()))
            grp.alpha_composite(fade_rgba(lid, la))
        frame.alpha_composite(fade_rgba(grp, ga))
        return
    if kind == "sign":
        drop = 1 - seg(t, 0.0, 1.2)
        up = seg(t, 1.9, 2.8)
        if up >= 1:
            return
        tau = max(0.0, t - 0.6)
        th = 9 * math.exp(-1.1 * tau) * math.cos(3.1 * tau)
        tw = 10 * math.exp(-0.9 * tau) * math.sin(2.2 * tau)
        Lr = 900
        piv = np.array([0, -960 - 900 * drop - 1300 * up, 1500])
        thr = math.radians(th)
        C = piv + np.array([Lr * math.sin(thr), Lr * math.cos(thr), 0])
        pose = Pose(C[0], C[1], C[2], 0, tw, -th)
        q = pose.project(rect_pts(560, 240))
        for x in (-190, 190):
            rq = pose.project([(x - 6, -Lr - 400, 2), (x + 6, -Lr - 400, 2), (x + 6, -96, 2), (x - 6, -96, 2)])
            draw_quad(frame, IA["rope"], rq, shade=0.95)
        shadow(frame, [q], (10, 22), 20, 0.3)
        draw_quad(frame, IA["sign"], q, shade=lambert(pose.normal()))
        return
    if kind in ("text", "fly"):
        return


def g_draw_parts(frame, A, t, parts, zf, pal):
    for Zp, p, pd, sx, sy in parts:
        kind = pd["kind"]
        texs = A["sprites"][kind]
        tex = texs[pd["var"] % len(texs)]
        a = pal
        if pd["tw"]:
            a *= 0.55 + 0.45 * math.sin(2 * math.pi * t / pd["tw"] + pd["tph"])
        blur = min(9.0, 8.0 * abs(1 / Zp - 1 / zf) * 1300) * S
        if kind in ("dust", "lantern", "glitter"):
            half = pd["size"] * FOC / Zp / 2
            cx, cy = CX + (sx - 360) * S, CY + (sy - 640) * S
            q = [(cx - half, cy - half), (cx + half, cy - half), (cx + half, cy + half), (cx - half, cy + half)]
            draw_quad(frame, tex, q, alpha=a, blur=blur * 0.5, resample=Image.BILINEAR)
            continue
        if kind == "balloon":
            s = pd["size"]
            ang = math.radians(6 * math.sin(2 * math.pi * pd["fr"] * (t - pd["t0"]) + pd["ph"]))
            pts = []
            for lx, ly in ((-s / 2, -s * 1.2), (s / 2, -s * 1.2), (s / 2, s * 1.2), (-s / 2, s * 1.2)):
                pts.append((lx * math.cos(ang) - ly * math.sin(ang), lx * math.sin(ang) + ly * math.cos(ang), 0))
            q = Pose(p.C[0], p.C[1], p.C[2]).project(pts)
            draw_quad(frame, tex, q, alpha=a, blur=blur, resample=Image.BILINEAR)
            continue
        s = pd["size"]
        asp = {"leaf": 1.35, "confetti": 1.6, "kamboja": 1.0}.get(kind, 1.2)
        quad = p.project(rect_pts(s, s * asp))
        fr = facing(quad)
        sh = lambert(p.normal(), back=not fr) * (1.0 if fr else 0.9)
        draw_quad(frame, tex, quad, alpha=a, blur=blur, shade=sh, resample=Image.BILINEAR)


def render_gallery(t_out, A):
    st = A["st"]
    t = t_out * GTL / DUR
    frame = A["bg"].copy()
    z = 1 + 0.05 * (seg(t, 2.4, 4.6) - seg(t, 12.0, 14.6))
    ph = 2 * math.pi * t / GTL
    bf, mf = A["bokeh_far"]
    bn, mn = A["bokeh_near"]
    draw_layer_affine(frame, bf, mf, 1 + (z - 1) * 0.5, 22 * S * math.sin(ph), 30 * S * math.sin(ph + 1.3))
    draw_layer_affine(frame, bn, mn, z, -40 * S * math.sin(ph + 0.6), -55 * S * math.sin(ph))

    if "twinkles" in st:  # navy: twinkling stars + shooting star
        for x, y, sz, per, phs in st["twinkles"]:
            a = max(0.0, math.sin(2 * math.pi * t * max(1, round(GTL / per)) / GTL + phs)) ** 3
            if a > 0.03:
                c = (CX + (x - 360) * S, CY + (y - 640) * S)
                hz = sz * S * (0.6 + 0.4 * a)
                draw_quad(frame, A["sparkle"], [(c[0] - hz, c[1] - hz), (c[0] + hz, c[1] - hz), (c[0] + hz, c[1] + hz), (c[0] - hz, c[1] + hz)], alpha=a * 0.9, resample=Image.BILINEAR)
        sp = (t - 0.7) / 0.8
        if 0 <= sp <= 1:
            a = math.sin(math.pi * sp)
            x0, y0 = lerp(80, 420, ease(sp)), lerp(90, 300, ease(sp))
            m = Image.new("L", (W, H), 0)
            d = ImageDraw.Draw(m)
            for k in range(24):
                f = k / 24
                d.line([(R(x0 - 120 * f), R(y0 - 63 * f)), (R(x0 - 120 * (f + 1 / 24)), R(y0 - 63 * (f + 1 / 24)))], fill=int(255 * (1 - f) ** 2), width=max(1, R(2.2 * (1 - f))))
            paint(frame, m.filter(ImageFilter.GaussianBlur(0.8 * S)), (255, 248, 228), a)

    ist = g_intro_state(t, A)
    cpd, calpha, cblur, clip, lifted = g_card_state(t, ist)
    cpose = Pose(**cpd)
    zf = cpose.C[2] if t < 9.0 else 1330.0

    pal = seg(t, 2.6, 3.4) * (1 - 0.4 * seg(t, 9.2, 10.0)) * (1 - seg(t, 12.4, 13.8))
    if st["intro"] == "fly":
        pal = seg(t, 0.4, 1.4) * (1 - 0.4 * seg(t, 9.2, 10.0)) * (1 - seg(t, 12.4, 13.8))
    parts = []
    if pal > 0:
        for pd in A["parts"]:
            tt = t - pd["t0"]
            u = tt / pd["dur"]
            if not (0 <= u <= 1):
                continue
            sy = lerp(-160, 1440, u) if pd["dirn"] > 0 else lerp(1440, -160, u)
            sx = pd["sx0"] + pd["amp"] * math.sin(2 * math.pi * pd["fr"] * tt + pd["ph"])
            X, Y = screen_to_world(sx, sy, pd["Z"])
            parts.append((pd["Z"], Pose(X, Y, pd["Z"], *(pd["a0"] + pd["w"] * tt)), pd, sx, sy))
        parts.sort(key=lambda x: -x[0])
    card_vis = calpha > 0.003 and lifted
    thresh = cpose.C[2] if card_vis else NEAR_Z
    g_draw_parts(frame, A, t, [p for p in parts if p[0] > thresh], zf, pal)

    def card_cb(target):
        g_draw_card(target, A, cpose, calpha, cblur, clip, t)

    g_draw_intro(frame, A, t, ist, card_cb)
    if lifted and calpha > 0.003:
        L = seg(t, *G_LIFT)
        rec = seg(t, 9.0, 9.9)
        cq = cpose.project(rect_pts(CW, CH))
        shadow(frame, [cq], (lerp(6, 16, L), lerp(10, 30, L) * (1 - 0.6 * rec)), lerp(10, 34, L), 0.26 * calpha)
        g_draw_card(frame, A, cpose, calpha, cblur, None, t)

    # intro text overlays
    if "intro_txt" in st:
        if st["intro"] == "text":
            ia = seg(t, 0.2, 1.1) * (1 - seg(t, 1.5, 2.2))
        else:
            ia = seg(t, 0.3, 1.1) * (1 - seg(t, 2.2, 2.9))
        if ia > 0.003:
            dy = (10 * (1 - seg(t, 0.2, 1.3)) - 14 * seg(t, 1.9, 2.9)) * S
            lay = st["intro_txt"]
            if abs(dy) > 0.02:
                lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
            frame.alpha_composite(fade_rgba(lay.convert("RGBA"), ia))

    # highlight: countdown or the big seven
    if "cd" in A:
        draw_cd_style(frame, A["cd"], t)
    if "hl" in st:
        ha = seg(t, 9.4, 9.9) * (1 - seg(t, 11.7, 12.4))
        if ha > 0.003:
            # confetti burst from behind the 7
            bt = t - 9.6
            if bt > 0:
                rng = np.random.default_rng(909)
                for i in range(70):
                    ang = rng.uniform(0, 2 * math.pi)
                    v = rng.uniform(260, 620)
                    x = 360 + math.cos(ang) * v * bt
                    y = 640 + math.sin(ang) * v * bt * 0.8 + 260 * bt * bt
                    if not (-40 < x < 760 and -40 < y < 1320):
                        continue
                    Zc = 1500
                    X, Y = screen_to_world(x, y, Zc)
                    p = Pose(X, Y, Zc, *(rng.uniform(0, 360, 3) + rng.uniform(200, 500, 3) * bt))
                    q = p.project(rect_pts(14, 22))
                    draw_quad(frame, A["sprites"]["confetti"][i % 5], q, alpha=ha * (1 - seg(bt, 1.4, 2.2)), shade=lambert(p.normal(), back=not facing(q)), resample=Image.BILINEAR)
            sc = lerp(0.3, 1.0, ease_out_back(clamp((t - 9.45) / 0.6))) * (1 + 0.02 * math.sin(2 * math.pi * (t - 10) / 1.2) * seg(t, 10.0, 10.6))
            rot = math.radians(4 * math.sin(2 * math.pi * (t - 10) / 1.6) * seg(t, 10.0, 10.8))
            a_, b_ = math.cos(rot) / sc, math.sin(rot) / sc
            cx, cy = CX, CY + 40 * S
            coef = (a_, b_, cx - a_ * cx - b_ * cy, -b_, a_, cy + b_ * cx - a_ * cy)
            lay = st["hl"].transform((W, H), Image.AFFINE, coef, Image.BICUBIC)
            frame.alpha_composite(fade_rgba(lay.convert("RGBA"), ha))
            frame.alpha_composite(fade_rgba(st["hl_txt"].convert("RGBA"), seg(t, 9.8, 10.4) * (1 - seg(t, 11.7, 12.4))))

    ca = seg(t, 12.3, 13.1) * (1 - seg(t, 14.0, 14.85))
    if ca > 0.003:
        dy = (16 * (1 - seg(t, 12.3, 13.2)) - 8 * seg(t, 14.0, 14.85)) * S
        lay = A["closing"]
        if abs(dy) > 0.02:
            lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
        frame.alpha_composite(fade_rgba(lay.convert("RGBA"), ca))

    g_draw_parts(frame, A, t, [p for p in parts if p[0] <= thresh], zf, pal)

    if st.get("sparkle"):
        spa = seg(t, 3.6, 4.4) * (1 - seg(t, 8.8, 9.4)) * abs(math.cos(math.radians(cpd["ry"]))) ** 3
        if spa > 0.01:
            for ax, ay, per, phs, sz in [(-215, -170, 2.1, 0.0, 24), (205, -95, 1.8, 0.9, 20), (-185, 120, 2.2, 1.7, 22), (210, 150, 2.4, 0.4, 28),
                                         (-40, -290, 1.9, 2.1, 16), (150, 300, 2.0, 1.2, 18), (-230, 300, 2.6, 2.6, 22), (240, -300, 2.3, 1.5, 22)]:
                tw = math.sin(2 * math.pi * (t - phs) / per)
                a = max(0.0, tw) ** 3 * spa
                if a < 0.02:
                    continue
                sxy = cpose.project([(ax, ay, -12)])[0]
                half = sz * (0.6 + 0.4 * tw) * FOC / cpose.C[2] * 1.4
                draw_quad(frame, A["sparkle"], [(sxy[0] - half, sxy[1] - half), (sxy[0] + half, sxy[1] - half), (sxy[0] + half, sxy[1] + half), (sxy[0] - half, sxy[1] + half)], alpha=a, resample=Image.BILINEAR)

    if "hangers" in st:
        draw_hangers(frame, st["hangers"], t, glow_flicker=st.get("hang_flicker", False))

    frame.alpha_composite(A["vignette"])
    out = np.asarray(frame.convert("RGB"), np.float32) + A["dither"]
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))


# ---------------------------------------------------------------- workers
_A = None
_STYLE = "blush"


def _assets(style):
    return build_assets() if style == "blush" else build_gallery_assets(style)


def _render(t, A):
    return render(t, A) if _STYLE == "blush" else render_gallery(t, A)


def _init(cfg, style="blush"):
    global _A, _STYLE
    configure(*cfg)
    _STYLE = style
    _A = _assets(style)


def _job(args):
    i, out_dir = args
    _render(i / FPS, _A).save(os.path.join(out_dir, f"f{i:04d}.png"), compress_level=2)
    return i


def encode(style, cfg, out_mp4, out_poster, crf, workers):
    global _STYLE
    configure(*cfg)
    _STYLE = style
    gallery = style != "blush"
    music = MUSIC if not gallery else ROOT / "frontend/public/music/demo" / STYLE_MUSIC[style]
    fade_out = GAL_FADE_OUT if gallery else AUDIO_FADE_OUT
    maxrate = GAL_MAXRATE if gallery else MAXRATE
    tl, poster_t = (GTL, GAL_POSTER_T) if gallery else (TL, POSTER_T)
    os.makedirs(TMP_BASE, exist_ok=True)
    free = shutil.disk_usage(TMP_BASE).free
    if free < 8 * 1024 ** 3:
        sys.exit(f"not enough free disk in {TMP_BASE}: {free / 1e9:.1f} GB")
    tmp = tempfile.mkdtemp(prefix="rawuh-video-", dir=TMP_BASE)
    t0 = time.time()
    try:
        ctx = get_context("spawn")
        with ctx.Pool(workers, initializer=_init, initargs=(cfg, style)) as pool:
            for n, _ in enumerate(pool.imap_unordered(_job, [(i, tmp) for i in range(NF)], chunksize=4)):
                if n % 90 == 0:
                    print(f"  [{style}] frame {n}/{NF}  {time.time() - t0:.0f}s", flush=True)
        used = sum(f.stat().st_size for f in Path(tmp).iterdir())
        print(f"[{style}] rendered {NF} frames in {time.time() - t0:.0f}s ({used / 1e9:.2f} GB temp)")
        Path(out_mp4).parent.mkdir(parents=True, exist_ok=True)
        cmd = [FFMPEG, "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
               "-i", str(music), "-map", "0:v", "-map", "1:a", "-t", f"{DUR}",
               "-af", f"afade=t=in:st=0:d={AUDIO_FADE_IN},afade=t=out:st={DUR - fade_out}:d={fade_out}",
               "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-maxrate", maxrate, "-bufsize", f"{int(maxrate[:-1]) * 2}k",
               "-profile:v", "high", "-pix_fmt", "yuv420p", "-x264-params", "threads=8:aq-mode=3:aq-strength=0.9:deblock=-1,-1",
               "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-movflags", "+faststart", str(out_mp4)]
        subprocess.run(cmd, check=True)
        _init(cfg, style)
        _render(poster_t * DUR / tl, _A).save(out_poster, "WEBP", quality=80, method=6)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{out_mp4}  {Path(out_mp4).stat().st_size / 1e6:.2f} MB")
    print(f"{out_poster}  {Path(out_poster).stat().st_size / 1e3:.0f} kB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="blush", choices=["blush"] + list(STYLES), help="preset; blush = the main 30 s demo")
    ap.add_argument("--gallery", action="store_true", help="render all gallery styles to frontend/public/rawuh/video-contoh/")
    ap.add_argument("--out", default=None, help="output .mp4 path (poster is written next to it as <stem>-poster.webp)")
    ap.add_argument("--width", type=int, default=None, help="output width (height = 16:9 portrait); default 1080 blush / 720 gallery")
    ap.add_argument("--duration", type=float, default=None, help="seconds; default 30 blush / 15 gallery (timeline is time-scaled)")
    ap.add_argument("--fps", type=int, default=DEF_FPS)
    ap.add_argument("--crf", type=int, default=None)
    ap.add_argument("--still", type=float, nargs="*", help="render still(s) at timeline second(s) and exit")
    ap.add_argument("--still-dir", default=None, help="dir for --still output")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()
    styles = list(STYLES) if args.gallery else [args.style]
    for style in styles:
        gallery = style != "blush"
        cfg = (args.width or (720 if gallery else DEF_WIDTH), args.duration or (GTL if gallery else DEF_DUR), args.fps)
        configure(*cfg)
        if args.still:
            global _STYLE
            _STYLE = style
            A = _assets(style)
            od = Path(args.still_dir or TMP_BASE)
            od.mkdir(parents=True, exist_ok=True)
            tl = GTL if gallery else TL
            for t in args.still:
                p = od / f"{style}_{t:05.2f}.png"
                _render(t * DUR / tl, A).save(p)
                print(p)
            continue
        if args.out and not args.gallery:
            out = Path(args.out)
        else:
            out = (GAL_DIR / f"{style}.mp4") if gallery else OUT_MP4
        poster = out.with_name(out.stem + "-poster.webp") if (gallery or args.out) else OUT_POSTER
        encode(style, cfg, out, poster, args.crf or (GAL_CRF if gallery else CRF), args.workers)


if __name__ == "__main__":
    main()
