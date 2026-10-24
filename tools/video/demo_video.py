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


# ---------------------------------------------------------------- workers
_A = None


def _init(cfg):
    global _A
    configure(*cfg)
    _A = build_assets()


def _job(args):
    i, out_dir = args
    render(i / FPS, _A).save(os.path.join(out_dir, f"f{i:04d}.png"), compress_level=2)
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=DEF_WIDTH, help="output width (height = 16:9 portrait)")
    ap.add_argument("--duration", type=float, default=DEF_DUR, help="seconds; the 30 s timeline is time-scaled")
    ap.add_argument("--fps", type=int, default=DEF_FPS)
    ap.add_argument("--crf", type=int, default=CRF)
    ap.add_argument("--still", type=float, nargs="*", help="render still(s) at timeline second(s) and exit")
    ap.add_argument("--out", default=None, help="dir for --still output")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()
    cfg = (args.width, args.duration, args.fps)
    configure(*cfg)

    if args.still:
        A = build_assets()
        od = Path(args.out or TMP_BASE)
        od.mkdir(parents=True, exist_ok=True)
        for t in args.still:
            p = od / f"still_{t:05.2f}.png"
            render(t * DUR / TL, A).save(p)
            print(p)
        return

    os.makedirs(TMP_BASE, exist_ok=True)
    free = shutil.disk_usage(TMP_BASE).free
    if free < 8 * 1024 ** 3:
        sys.exit(f"not enough free disk in {TMP_BASE}: {free / 1e9:.1f} GB")
    tmp = tempfile.mkdtemp(prefix="rawuh-video-", dir=TMP_BASE)
    t0 = time.time()
    try:
        ctx = get_context("spawn")
        with ctx.Pool(args.workers, initializer=_init, initargs=(cfg,)) as pool:
            for n, _ in enumerate(pool.imap_unordered(_job, [(i, tmp) for i in range(NF)], chunksize=4)):
                if n % 90 == 0:
                    print(f"  frame {n}/{NF}  {time.time() - t0:.0f}s", flush=True)
        used = sum(f.stat().st_size for f in Path(tmp).iterdir())
        print(f"rendered {NF} frames in {time.time() - t0:.0f}s ({used / 1e9:.2f} GB temp)")
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [FFMPEG, "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
               "-i", str(MUSIC), "-map", "0:v", "-map", "1:a", "-t", f"{DUR}",
               "-af", f"afade=t=in:st=0:d={AUDIO_FADE_IN},afade=t=out:st={DUR - AUDIO_FADE_OUT}:d={AUDIO_FADE_OUT}",
               "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-maxrate", MAXRATE, "-bufsize", "4800k",
               "-profile:v", "high", "-pix_fmt", "yuv420p", "-x264-params", "threads=8:aq-mode=3:aq-strength=0.9:deblock=-1,-1",
               "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-movflags", "+faststart", str(OUT_MP4)]
        subprocess.run(cmd, check=True)
        _init(cfg)
        render(POSTER_T * DUR / TL, _A).save(OUT_POSTER, "WEBP", quality=80, method=6)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{OUT_MP4}  {OUT_MP4.stat().st_size / 1e6:.2f} MB")
    print(f"{OUT_POSTER}  {OUT_POSTER.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
