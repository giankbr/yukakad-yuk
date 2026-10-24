#!/usr/bin/env python3
"""Rawuh "Video Ucapan 3D" demo video generator.

Everything is drawn from code: paper textures, envelope, wax seal, card, rose
petals, sparkles and bokeh are numpy/Pillow renders. "3D" is faked with a
pinhole camera: every flat layer is a planar quad posed in 3D, projected and
warped with a perspective homography (Pillow PERSPECTIVE transform on
premultiplied RGBa, mip-mapped for crisp text), plus parallax, depth-of-field
blur, Lambert shading and soft shadows.

Output (deterministic, fixed seeds):
  frontend/public/rawuh/video-ucapan-demo.mp4         720x1280, 30 fps, H.264 + AAC
  frontend/public/rawuh/video-ucapan-demo-poster.webp poster (names reveal)

Usage:
  python3 tools/video/demo_video.py              # full render + encode
  python3 tools/video/demo_video.py --still 8.0  # one frame -> scratch PNG (debug)
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

W, H, FPS, DUR = 720, 1280, 30, 20.0
NF = int(round(FPS * DUR))
POSTER_T = 8.0
FOC = 1500.0  # focal length in px; world units == px at Z = FOC
CX, CY = W / 2, H / 2

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

# envelope / card geometry in world units (card + envelope textures are 2x)
EW, EH = 600, 400
CW, CH = 540, 756
TS = 2  # texture px per world unit


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


_FONTS = {}


def font(spec, size):
    key = (spec, int(size))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(spec[0], int(size), index=spec[1])
    return _FONTS[key]


def ss_mask(w, h, fn, ss=3):
    """Supersampled 'L' mask: fn(draw, s) draws in design coords scaled by s."""
    m = Image.new("L", (w * ss, h * ss), 0)
    fn(ImageDraw.Draw(m), ss)
    return m.resize((w, h), Image.BOX)


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
    d.polygon([((cx) * s, (y - dia) * s), ((cx + dia) * s, y * s), (cx * s, (y + dia) * s), ((cx - dia) * s, y * s)], fill=255)
    if dots:
        r = 2.6
        for x in (cx - half - 8, cx + half + 8):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=255)


def solid(size, rgb):
    return Image.new("RGB", size, rgb)


def paint(canvas, mask, fill, opacity=1.0):
    """alpha-composite a fill (RGB colour tuple or RGB image) through mask onto RGBA canvas."""
    src = solid(canvas.size, fill) if isinstance(fill, tuple) else fill
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
    """Metallic gold gradient image, bands repeat per text line [y0, y1]."""
    stops = [(0.0, (240, 220, 156)), (0.32, (196, 154, 66)), (0.55, (226, 196, 120)), (0.78, (170, 128, 48)), (1.0, (205, 168, 86))]
    lut = gradient_stops(256, stops)
    yy = np.arange(h, dtype=np.float32)[:, None]
    xx = np.arange(w, dtype=np.float32)[None, :]
    u = np.clip((yy - y0) / max(1, (y1 - y0)) + 0.10 * np.sin(xx / w * math.pi * 2.2), 0, 1)
    arr = lut[(u * 255).astype(np.int32)]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def multi_gold(w, h, bands):
    """Gold gradient whose bands follow several text lines [(y0, y1), ...]."""
    out = np.zeros((h, w, 3), np.float32)
    edges = [0] + [int((bands[i][1] + bands[i + 1][0]) / 2) for i in range(len(bands) - 1)] + [h]
    for (y0, y1), a, b in zip(bands, edges[:-1], edges[1:]):
        out[a:b] = np.asarray(gold_fill(w, h, y0, y1), np.float32)[a:b]
    return Image.fromarray(out.astype(np.uint8))


def paper(w, h, base, seed, grain=1.0):
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 40, (h, w))
    fine = np.asarray(Image.fromarray(np.uint8(np.clip(128 + fine, 0, 255))).filter(ImageFilter.GaussianBlur(0.7)), np.float32) - 128
    low = Image.fromarray(rng.normal(0, 1, (h // 40 + 2, w // 40 + 2)).astype(np.float32), "F").resize((w, h), Image.BICUBIC)
    low = np.asarray(low, np.float32)
    fib = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(fib)
    for _ in range(int(w * h / 9000)):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        a = rng.uniform(0, math.pi)
        ln = rng.uniform(6, 26)
        d.line([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], fill=int(rng.uniform(40, 110)), width=1)
    fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(0.6)), np.float32)
    v = (fine * 0.13 + low * 1.4 - fib * 0.05) * grain
    arr = np.array(base, np.float32)[None, None, :] + v[..., None] * np.array([1.0, 0.98, 0.94])
    return np.clip(arr, 0, 255)


def rgba_from(arr_rgb, alpha):
    im = Image.fromarray(np.clip(arr_rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(alpha)
    return im


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


def draw_quad(frame, tex, quad, alpha=1.0, blur=0.0, shade=1.0, modify=None, resample=Image.BICUBIC):
    """Warp tex onto screen quad (TL, TR, BR, BL) and composite onto frame."""
    if alpha <= 0.003:
        return
    q = np.asarray(quad, np.float64)
    if not np.all(np.isfinite(q)):
        return
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
    # map content corners; padding extends naturally (soft, antialiased edges)
    src = [(P, P), (P + w, P), (P + w, P + h), (P, P + h)]
    coef = homography(q - [x0, y0], src)
    out = img.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, tuple(coef), resample)
    if blur > 0.25:
        out = out.filter(ImageFilter.GaussianBlur(float(blur)))
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
    def __init__(self, X=0.0, Y=0.0, Z=FOC, rx=0.0, ry=0.0, rz=0.0):
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


LIGHT = np.array([-0.35, -0.55, -1.0]) / np.linalg.norm([-0.35, -0.55, -1.0])
_D0 = float(np.dot([0, 0, -1.0], LIGHT))


def lambert(n, back=False):
    if back:
        n = -n
    d = float(np.dot(n, LIGHT)) / _D0
    return clamp(0.80 + 0.22 * d, 0.62, 1.05)


def facing(quad):
    q = np.asarray(quad)
    area = 0.0
    for i in range(4):
        x1, y1 = q[i]
        x2, y2 = q[(i + 1) % 4]
        area += x1 * y2 - x2 * y1
    return area > 0  # TL,TR,BR,BL clockwise on screen (y down) => positive


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
    rng = np.random.default_rng(11)
    g = g + rng.normal(0, 1.1, (H, W, 1))
    return Image.fromarray(np.clip(g + 0 * xx, 0, 255).astype(np.uint8)).convert("RGBA")


def build_bokeh(n, rmin, rmax, amin, amax, blur, seed, margin):
    w, h = W + 2 * margin, H + 2 * margin
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w, 4), np.float32)  # premultiplied
    cols = [(255, 250, 240), (236, 212, 154), (240, 201, 192), (231, 179, 181), (250, 236, 210)]
    for _ in range(n):
        R = rng.uniform(rmin, rmax)
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        col = np.array(cols[rng.integers(len(cols))], np.float32)
        al = rng.uniform(amin, amax)
        x0, x1 = int(max(cx - R - 3, 0)), int(min(cx + R + 3, w))
        y0, y1 = int(max(cy - R - 3, 0)), int(min(cy + R + 3, h))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        a = al * np.clip((R - d) / 2.5, 0, 1) * (0.72 + 0.28 * np.clip(d / R, 0, 1) ** 5)
        a = a[..., None]
        acc[y0:y1, x0:x1, :3] = col * a + acc[y0:y1, x0:x1, :3] * (1 - a)
        acc[y0:y1, x0:x1, 3:] = a * 255 + acc[y0:y1, x0:x1, 3:] * (1 - a)
    im = Image.frombytes("RGBa", (w, h), np.clip(acc, 0, 255).astype(np.uint8).tobytes())
    return im.filter(ImageFilter.GaussianBlur(float(blur)))


def build_vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / (W * 0.62)) ** 2 + ((yy - CY * 0.95) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * 0.16
    v = np.zeros((H, W, 4), np.uint8)
    v[..., 0], v[..., 1], v[..., 2] = 90, 50, 50
    v[..., 3] = (a * 255).astype(np.uint8)
    return Image.frombytes("RGBA", (W, H), v.tobytes())


def liner(w, h, seed):
    base = paper(w, h, (240, 210, 203), seed, 0.8)
    m = ss_mask(w, h, lambda d, s: [
        d.line([((i - h) * s, 0), (i * s, h * s)], fill=255, width=max(1, int(1.3 * s))) for i in range(0, w + h, 46)
    ] + [
        d.line([(i * s, 0), ((i - h) * s, h * s)], fill=255, width=max(1, int(1.3 * s))) for i in range(0, w + h, 46)
    ], ss=2)
    im = rgba_from(base, 255)
    paint(im, m, (214, 178, 112), 0.42)
    # dots at lattice crossings
    dm = ss_mask(w, h, lambda d, s: [
        d.ellipse([(x - 2.4) * s, (y - 2.4) * s, (x + 2.4) * s, (y + 2.4) * s], fill=255)
        for y in range(0, h + 46, 46) for x in range(23 if (y // 46) % 2 else 0, w + 46, 46)
    ], ss=2)
    paint(im, dm, (196, 150, 70), 0.6)
    return im


def build_seal(R=58):
    S = int(R * 2 + 40)
    c = S / 2
    rng = np.random.default_rng(5)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    ang = np.arctan2(yy - c, xx - c)
    rad = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    edge = R * (1 + sum(rng.uniform(0.008, 0.03) * np.sin(k * ang + rng.uniform(0, 6.28)) for k in (3, 5, 7, 11, 17)))
    a = np.clip(edge - rad + 0.5, 0, 1)
    # dome lighting
    nx, ny = (xx - c) / R, (yy - c) / R
    lit = np.clip(0.75 - 0.45 * nx - 0.6 * ny, 0, 1.4)
    lut = gradient_stops(256, [(0.0, (120, 88, 30)), (0.4, (176, 136, 56)), (0.75, (222, 190, 112)), (1.0, (250, 232, 176))])
    col = lut[np.clip(lit / 1.4 * 255, 0, 255).astype(np.int32)]
    # inner ring groove
    ring = np.exp(-((rad - R * 0.74) / 1.6) ** 2)
    ring_hi = np.exp(-((rad - R * 0.74 - 2.2) / 1.4) ** 2)
    col = col * (1 - 0.35 * ring[..., None]) + 255 * 0.18 * ring_hi[..., None] * (ny[..., None] > -2)
    seal = rgba_from(col, Image.fromarray((a * 255).astype(np.uint8)))
    # embossed monogram
    mono = ss_mask(S, S, lambda d, s: (
        text(d, s, c - 12, c + 14, "K", DIDOT_I, 48),
        text(d, s, c + 15, c + 24, "A", DIDOT_I, 48),
    ))
    dark = ImageChopsOffset(mono, 1, 2)
    light = ImageChopsOffset(mono, -1, -1)
    paint(seal, light, (255, 240, 196), 0.75)
    paint(seal, dark, (96, 68, 22), 0.75)
    paint(seal, mono, (190, 150, 66), 1.0)
    seal.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return seal


def ImageChopsOffset(m, dx, dy):
    out = Image.new("L", m.size, 0)
    out.paste(m, (dx, dy))
    return out


def build_envelope():
    w, h = EW * TS, EH * TS
    # back panel interior (liner), darker toward bottom (inside of pocket)
    back = liner(w, h, 21)
    shade = Image.linear_gradient("L").resize((w, h)).point(lambda v: int(v * 0.35))
    paint(back, shade, (120, 70, 70), 1.0)
    back.putalpha(ss_mask(w, h, lambda d, s: d.rounded_rectangle([0, 0, w * s, h * s], radius=8 * s, fill=255), ss=2))

    # front pocket: rect minus V notch
    vy = 420
    pocket = rgba_from(paper(w, h, (250, 245, 236), 22), 255)
    # bottom flap overlapping the side flaps: soft shadow along its edges
    bf = [(0, h), (w * 0.47, h * 0.52), (w * 0.53, h * 0.52), (w, h)]
    bfm = ss_mask(w, h, lambda d, s: d.polygon([(x * s, y * s) for x, y in bf], fill=255), ss=2)
    sh = bfm.filter(ImageFilter.GaussianBlur(10))
    paint(pocket, ImageChopsSub(sh, bfm), (110, 80, 60), 0.35)
    paint(pocket, bfm, (255, 252, 246), 0.35)
    # side flaps slightly darker
    sides = ss_mask(w, h, lambda d, s: (
        d.polygon([(0, 0), (w * 0.5 * s, vy * s), (0, h * s)], fill=255),
        d.polygon([(w * s, 0), (w * 0.5 * s, vy * s), (w * s, h * s)], fill=255)), ss=2)
    paint(pocket, ImageChopsSub(sides, bfm), (200, 180, 160), 0.10)
    gold_edges = ss_mask(w, h, lambda d, s: (
        d.rounded_rectangle([7 * s, 7 * s, (w - 7) * s, (h - 7) * s], radius=6 * s, outline=255, width=int(3 * s)),
        d.line([(10 * s, 10 * s), (w * 0.5 * s, (vy - 10) * s), ((w - 10) * s, 10 * s)], fill=255, width=int(2.4 * s), joint="curve")))
    paint(pocket, gold_edges, (201, 162, 74), 0.95)
    pm = ss_mask(w, h, lambda d, s: (
        d.rounded_rectangle([0, 0, w * s, h * s], radius=8 * s, fill=255),
        d.polygon([(-2 * s, -2 * s), ((w + 2) * s, -2 * s), (w * 0.5 * s, vy * s)], fill=0)), ss=3)
    pocket.putalpha(pm)

    # flap (front + inner liner), local rows = distance from hinge, tip at 500
    fh = 300 * TS
    tip = 500
    tri = lambda d, s: d.polygon([(0, 0), (w * s, 0), (w * 0.5 * s, tip * s)], fill=255)
    fm = ss_mask(w, fh, tri, ss=3)
    fm = ImageMax(fm, ss_mask(w, fh, lambda d, s: d.ellipse([(w / 2 - 80) * s, (tip - 130) * s, (w / 2 + 80) * s, (tip + 2) * s], fill=255), ss=3))
    flap = rgba_from(paper(w, fh, (252, 248, 240), 23), 255)
    g = Image.linear_gradient("L").resize((w, fh)).point(lambda v: int(v * 0.12))
    paint(flap, g, (170, 140, 110), 1.0)
    fe = ss_mask(w, fh, lambda d, s: d.line([(10 * s, 8 * s), (w * 0.5 * s, (tip - 14) * s), ((w - 10) * s, 8 * s)], fill=255, width=int(3 * s), joint="curve"))
    paint(flap, fe, (201, 162, 74), 0.95)
    seal = build_seal(70)
    # seal shadow
    sa = seal.getchannel("A")
    shadow = Image.new("L", (w, fh), 0)
    sx, sy = int(w / 2 - seal.width / 2), int(tip - 58 - seal.height / 2)
    shadow.paste(sa, (sx + 3, sy + 7))
    paint(flap, shadow.filter(ImageFilter.GaussianBlur(6)), (80, 50, 30), 0.45)
    flap.alpha_composite(seal, (sx, sy))
    sa_full = Image.new("L", (w, fh), 0)
    sa_full.paste(sa, (sx, sy))
    flap_a = ImageMax(fm, sa_full)
    flap.putalpha(flap_a)

    flap_in = liner(w, fh, 24)
    paint(flap_in, Image.linear_gradient("L").resize((w, fh)).point(lambda v: int((255 - v) * 0.25)), (120, 70, 70), 1.0)
    flap_in.putalpha(fm)
    return dict(back=Tex(back), pocket=Tex(pocket), flap=Tex(flap), flap_in=Tex(flap_in))


def ImageChopsSub(a, b):
    return Image.fromarray(np.clip(np.asarray(a, np.int16) - np.asarray(b, np.int16), 0, 255).astype(np.uint8))


def ImageMax(a, b):
    return Image.fromarray(np.maximum(np.asarray(a), np.asarray(b)))


def card_base(seed):
    w, h = CW * TS, CH * TS
    im = rgba_from(paper(w, h, IVORY, seed), 255)
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
    # faint blush wash at top and bottom
    yy = np.linspace(0, 1, h)[:, None]
    wash = (np.exp(-((yy - 0.0) / 0.18) ** 2) + np.exp(-((yy - 1.0) / 0.18) ** 2)) * np.ones((1, w))
    paint(im, Image.fromarray((wash * 70).astype(np.uint8)), BLUSH, 1.0)
    return im


def gold_text(im, mask, bands):
    w, h = im.size
    sh = ImageChopsOffset(mask, 2, 4).filter(ImageFilter.GaussianBlur(2.5))
    paint(im, sh, (110, 72, 40), 0.30)
    paint(im, mask, multi_gold(w, h, bands))


def build_card_front():
    w, h = CW * TS, CH * TS
    im = card_base(31)
    cx = w / 2
    small = ss_mask(w, h, lambda d, s: (
        text(d, s, cx, 300, "THE WEDDING OF", AVN_DEMI, 30, track=11),
        text(d, s, cx, 1172, "15 · 05 · 2027", DIDOT, 50, track=4),
    ))
    paint(im, small, ROSE)
    sub = ss_mask(w, h, lambda d, s: text(d, s, cx, 1240, "YOGYAKARTA", AVN_MED, 24, track=10))
    paint(im, sub, INK, 0.7)
    orn = ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 352, 140), ornament(d, s, cx, 1080, 210, gap=18, dia=8)))
    paint(im, orn, GOLD)
    amp = ss_mask(w, h, lambda d, s: text(d, s, cx, 760, "&", DIDOT_I, 110))
    paint(im, amp, ROSE, 0.95)
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
    script = ss_mask(w, h, lambda d, s: text(d, s, cx, 330, "Save the Date", SNELL, 128))
    gold_text(im, script, [(240, 350)])
    cap = ss_mask(w, h, lambda d, s: text(d, s, cx, 200, "AKAD & RESEPSI", AVN_DEMI, 28, track=11))
    paint(im, cap, ROSE)
    orn = ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 410, 150), ornament(d, s, cx, 700, 90, gap=12, dia=6, lw=1.6, dots=False)))
    paint(im, orn, GOLD)
    date = ss_mask(w, h, lambda d, s: text(d, s, cx, 530, "Sabtu, 15 Mei 2027", DIDOT, 70))
    paint(im, date, INK)
    place = ss_mask(w, h, lambda d, s: text(d, s, cx, 620, "Pendopo Ndalem, Yogyakarta", DIDOT_I, 50))
    paint(im, place, ROSE)
    # guest area
    bx0, by0, bx1, by1 = 130, 850, w - 130, 1300
    box = ss_mask(w, h, lambda d, s: d.rounded_rectangle([bx0 * s, by0 * s, bx1 * s, by1 * s], radius=26 * s, fill=255))
    paint(im, box, BLUSH, 0.55)
    boxl = ss_mask(w, h, lambda d, s: d.rounded_rectangle([bx0 * s, by0 * s, bx1 * s, by1 * s], radius=26 * s, outline=255, width=int(2 * s)))
    paint(im, boxl, GOLD, 0.9)
    k = ss_mask(w, h, lambda d, s: text(d, s, cx, 950, "KEPADA YTH.", AVN_DEMI, 28, track=9))
    paint(im, k, ROSE)
    b = ss_mask(w, h, lambda d, s: text(d, s, cx, 1050, "Bapak/Ibu/Saudara/i", DIDOT_I, 60))
    paint(im, b, INK)
    dots = ss_mask(w, h, lambda d, s: [d.ellipse([(x - 2.2) * s, (1150 - 2.2) * s, (x + 2.2) * s, (1150 + 2.2) * s], fill=255)
                                       for x in range(250, w - 250 + 1, 14)])
    paint(im, dots, GOLD, 0.9)
    tmp = ss_mask(w, h, lambda d, s: text(d, s, cx, 1225, "di tempat", DIDOT_I, 36))
    paint(im, tmp, INK, 0.6)
    return im


def build_closing():
    s2 = 2
    w, h = W * s2, H * s2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx = w / 2
    orn = ss_mask(w, h, lambda d, s: (ornament(d, s, cx, 1010, 170, gap=20, dia=9, lw=2.4), ornament(d, s, cx, 1460, 120, gap=16, dia=7, lw=2.2)))
    paint(im, orn, GOLD)
    l1 = ss_mask(w, h, lambda d, s: text(d, s, cx, 1180, "Kami menantikan", DIDOT_I, 92))
    paint(im, l1, INK)
    l2 = ss_mask(w, h, lambda d, s: text(d, s, cx, 1370, "kehadiranmu", SNELL, 168))
    sh = ImageChopsOffset(l2, 2, 5).filter(ImageFilter.GaussianBlur(3))
    paint(im, sh, (110, 72, 40), 0.25)
    paint(im, l2, multi_gold(w, h, [(1240, 1390)]))
    l3 = ss_mask(w, h, lambda d, s: text(d, s, cx, 1580, "KIRANA & ARYA", AVN_DEMI, 30, track=14))
    paint(im, l3, ROSE)
    ft = ss_mask(w, h, lambda d, s: text(d, s, cx, 2440, "Dibuat dengan Rawuh · rawuh.id", AVN_MED, 36, track=1.5))
    paint(im, ft, INK, 0.55)
    return im.resize((W, H), Image.LANCZOS).convert("RGBa")


def build_petal(seed, tint):
    w, h = 200, 240
    ss = 3
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(np.float32)
    u = (xx / (w * ss)) * 2 - 1
    v = 1 - yy / (h * ss)  # 0 base (bottom), 1 top
    width = 0.96 * np.sin(np.pi * np.clip(v * 0.93 + 0.035, 0, 1)) ** 0.62 * (1 - 0.08 * v)
    top = 0.97 - 0.09 * np.cos(np.clip(u, -1, 1) * np.pi / 2) ** 2  # notch
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
    for k in range(9):
        a = rng.uniform(-0.7, 0.7)
        veins += np.exp(-((u - a * v) / 0.012) ** 2) * v * 0.5
    col = col * (1 - 0.06 * veins[..., None])
    im = rgba_from(col, m)
    return Tex(im, min_w=10)


def build_sparkle():
    S = 96
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) - (S - 1) / 2
    r = np.sqrt(xx ** 2 + yy ** 2)
    core = np.exp(-(r / 4.5) ** 2)
    glow = np.exp(-(r / 16) ** 2) * 0.35
    rays = (np.exp(-(yy / 1.3) ** 2) * np.exp(-np.abs(xx) / 13) + np.exp(-(xx / 1.3) ** 2) * np.exp(-np.abs(yy) / 13))
    diag = (np.exp(-((xx - yy) / 1.8) ** 2) + np.exp(-((xx + yy) / 1.8) ** 2)) * np.exp(-r / 6) * 0.35
    a = np.clip(core + glow + rays * 0.9 + diag, 0, 1)
    col = np.array([255, 246, 220], np.float32) * (1 - glow[..., None]) + np.array(GOLD_HI, np.float32) * glow[..., None]
    arr = np.concatenate([col * a[..., None], a[..., None] * 255], -1)
    return Image.frombytes("RGBa", (S, S), np.clip(arr, 0, 255).astype(np.uint8).tobytes())


def build_assets():
    A = {}
    A["bg"] = build_background()
    A["bokeh_far"] = build_bokeh(70, 6, 22, 0.22, 0.5, 2.2, 1, 60)
    A["bokeh_near"] = build_bokeh(16, 34, 80, 0.10, 0.22, 7, 2, 90)
    A["vignette"] = build_vignette()
    A["env"] = build_envelope()
    front, names = build_card_front()
    A["card_front"] = Tex(front, extra=names)
    A["card_back"] = Tex(build_card_back())
    A["closing"] = build_closing()
    A["petals"] = [build_petal(40 + i, t) for i, t in enumerate([(206, 110, 130), (190, 98, 120), (222, 140, 150)])]
    A["sparkle"] = Tex(build_sparkle().convert("RGBA"), min_w=8)
    A["petal_defs"] = petal_defs()
    return A


def petal_defs():
    rng = np.random.default_rng(77)
    out = []
    n = 34
    for i in range(n):
        near = i % 6 == 2
        Z = rng.uniform(640, 900) if near else rng.uniform(1150, 2900)
        if near:
            sx0 = rng.uniform(-10, 150) if i % 12 == 2 else rng.uniform(570, 730)
        else:
            sx0 = rng.uniform(20, 700)
        out.append(dict(
            t0=2.2 + i * (12.6 / n) + rng.uniform(-0.25, 0.25), Z=Z, sx0=sx0,
            dur=4.4 + 3.6 * (Z - 640) / 2260 + rng.uniform(-0.4, 0.4),
            amp=rng.uniform(25, 70), fr=rng.uniform(0.25, 0.55), ph=rng.uniform(0, 6.28),
            size=rng.uniform(32, 48) * (0.8 if near else 1.0), var=int(rng.integers(3)),
            a0=rng.uniform(0, 360, 3), w=rng.uniform(45, 140, 3) * rng.choice([-1, 1], 3) * np.array([1, 1, 0.4]),
        ))
    return out


# ---------------------------------------------------------------- timeline
def env_state(t):
    e1 = seg(t, 0.0, 1.9)
    sl = seg(t, 3.05, 4.95)
    L = seg(t, 5.0, 6.7)
    Z = lerp(2900, 1650, e1)
    Z = lerp(Z, 1850, sl) + 350 * L
    ysc = lerp(lerp(740, 700, e1), 930, sl)  # screen y of centre
    Y = (ysc - CY) * Z / FOC + 520 * seg(t, 5.0, 7.0)
    idle = math.sin(2 * math.pi * t / 4.0) * (1 - sl) * e1
    pose = dict(X=lerp(-140, 0, e1), Y=Y + 4 * idle, Z=Z,
                rx=lerp(24, 0, e1) + 1.2 * idle, ry=lerp(-42, 0, e1), rz=lerp(-9, 0, e1))
    alpha = seg(t, 0.0, 0.9) * (1 - seg(t, 5.3, 6.9))
    theta = 180 * seg(t, 1.95, 3.05)
    blur = 9 * seg(t, 5.0, 6.6)
    return pose, alpha, theta, blur


CARD_IN, CARD_OUT = -EH / 2 + 28 + CH / 2, -EH / 2 - 12 - CH / 2


def card_state(t, envpose):
    """returns (Pose, alpha, blur, clip_y or None, lifted)"""
    sl = seg(t, 3.05, 4.95)
    cy_env = lerp(CARD_IN, CARD_OUT, sl)
    ep = Pose(**envpose)
    attached_C = ep.world([(0, cy_env, 0)])[0]
    L = seg(t, 5.0, 6.7)
    push = seg(t, 6.0, 11.0)
    flip = seg(t, 11.0, 12.7)
    rec = seg(t, 15.9, 17.3)
    hero = np.array([0.0, -12.0, lerp(1370, 1290, push)])
    C = attached_C * (1 - L) + hero * L
    C[2] += 300 * math.sin(math.pi * flip) + 1800 * rec
    C[1] -= 120 * rec
    sway_w = seg(t, 6.4, 7.6) * (1 - seg(t, 10.0, 11.0))
    sway_b = seg(t, 12.5, 13.5) * (1 - seg(t, 15.2, 16.4))
    ry = 14 * math.sin(math.pi * L) + 180 * flip
    ry += 5 * math.sin(2 * math.pi * (t - 6.4) / 3.6) * sway_w + 4.5 * math.sin(2 * math.pi * (t - 12.5) / 3.7) * sway_b
    rx = -10 * math.sin(math.pi * L) + 2.5 * math.sin(2 * math.pi * (t - 6.4) / 4.6) * sway_w + 2 * math.sin(2 * math.pi * (t - 12.5) / 4.4) * sway_b
    rx += -6 * rec
    rz = -2 * math.sin(math.pi * flip)
    pose = dict(X=C[0], Y=C[1], Z=C[2], rx=rx + envpose["rx"] * (1 - L), ry=ry + envpose["ry"] * (1 - L), rz=rz + envpose["rz"] * (1 - L))
    alpha = seg(t, 0.0, 0.9) * (1 - seg(t, 16.0, 17.2))
    blur = 7 * rec
    clip = None if L > 0 else (EH / 2 - 4) - (cy_env - CH / 2)  # card-local y beyond which hidden
    return pose, alpha, blur, clip, L > 0


def bg_zoom(t):
    return 1 + 0.06 * (seg(t, 4.5, 7.5) - seg(t, 15.8, 19.0)) + 0.025 * seg(t, 0, 2) * (1 - seg(t, 4.5, 7.5))


# ---------------------------------------------------------------- rendering
def draw_layer_affine(frame, layer, margin, zoom, ox, oy):
    a = 1 / zoom
    coef = (a, 0, CX - CX * a + margin + ox, 0, a, CY - CY * a + margin + oy)
    frame.alpha_composite(layer.transform((W, H), Image.AFFINE, coef, Image.BILINEAR).convert("RGBA"))


def shadow(frame, polys, offset, radius, opacity):
    if opacity <= 0.003:
        return
    q = 4
    m = Image.new("L", (W // q, H // q), 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon([((x + offset[0]) / q, (y + offset[1]) / q) for x, y in p], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(radius / q)).resize((W, H), Image.BILINEAR)
    paint(frame, m, (92, 52, 48), opacity)


def render(t, A):
    frame = A["bg"].copy()
    z = bg_zoom(t)
    ph = 2 * math.pi * t / DUR
    draw_layer_affine(frame, A["bokeh_far"], 60, 1 + (z - 1) * 0.5, 22 * math.sin(ph), 30 * math.sin(ph + 1.3))
    draw_layer_affine(frame, A["bokeh_near"], 90, z, -40 * math.sin(ph + 0.6), -55 * math.sin(ph))

    envpose, ealpha, theta, eblur = env_state(t)
    cpose_d, calpha, cblur, clip, lifted = card_state(t, envpose)
    cpose = Pose(**cpose_d)
    zf = cpose.C[2] if lifted else envpose["Z"]

    # petals sorted far->near
    pal = seg(t, 5.0, 5.8) * (1 - seg(t, 16.0, 17.4))
    petals = []
    if pal > 0:
        for pd in A["petal_defs"]:
            tt = t - pd["t0"]
            u = tt / pd["dur"]
            if not (0 <= u <= 1):
                continue
            sy = lerp(-140, H + 140, u)
            sx = pd["sx0"] + pd["amp"] * math.sin(2 * math.pi * pd["fr"] * tt + pd["ph"])
            Zp = pd["Z"]
            ang = pd["a0"] + pd["w"] * tt
            p = Pose((sx - CX) * Zp / FOC, (sy - CY) * Zp / FOC, Zp, *ang)
            petals.append((Zp, p, pd))
        petals.sort(key=lambda x: -x[0])

    def draw_petal(Zp, p, pd):
        s = pd["size"]
        quad = p.project(rect_pts(s, s * 1.2))
        fr = facing(quad)
        sh = lambert(p.normal(), back=not fr) * (1.0 if fr else 0.9)
        blur = min(9.0, 8.0 * abs(1 / Zp - 1 / zf) * 1300)
        draw_quad(frame, A["petals"][pd["var"]], quad, alpha=pal * 0.95, blur=blur, shade=sh, resample=Image.BILINEAR)

    card_z = cpose.C[2]
    for Zp, p, pd in petals:
        if Zp > card_z:
            draw_petal(Zp, p, pd)

    # ---- envelope group
    ep = Pose(**envpose)
    eb = eblur
    env = A["env"]
    back_q = ep.project(rect_pts(EW, EH))
    n_env = ep.normal()
    esh = lambert(n_env)
    th = math.radians(theta)

    def flap_pts():
        pts = []
        for x, dd in ((-EW / 2, 0), (EW / 2, 0), (EW / 2, 300), (-EW / 2, 300)):
            pts.append((x, -EH / 2 + dd * math.cos(th), -dd * math.sin(th)))
        return pts

    flap_q = ep.project(flap_pts())
    flap_tri = ep.project([(-EW / 2, -EH / 2, 0), (EW / 2, -EH / 2, 0),
                           (0, -EH / 2 + 250 * math.cos(th), -250 * math.sin(th))])
    fnorm = ep.R @ np.array([0, math.sin(th), -math.cos(th)])
    flap_front = facing(flap_q)
    fsh = lambert(fnorm, back=not flap_front)

    grp = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # envelope group, faded as one

    def draw_flap():
        tex = env["flap"] if flap_front else env["flap_in"]
        draw_quad(grp, tex, flap_q, blur=eb, shade=fsh)

    if ealpha > 0.003:
        # soft drop shadow
        polys = [back_q] + ([flap_tri] if theta > 5 else [])
        shadow(grp, polys, (10 * (ep.C[2] / 1650), 22 * (1650 / ep.C[2])), 22, 0.26)
        if theta > 90:
            draw_flap()
        draw_quad(grp, env["back"], back_q, blur=eb, shade=esh)
        if not lifted:
            draw_card(grp, A, cpose, 1.0, cblur, clip, t)
        draw_quad(grp, env["pocket"], back_q, blur=eb, shade=esh)
        if theta <= 90:
            # flap shadow on pocket while closed / lifting
            k = 1 - theta / 90
            shadow(grp, [flap_tri], (2, 5 + 10 * (1 - k)), 6 + 10 * (1 - k), 0.20 * min(1, k * 3))
            draw_flap()
        if ealpha < 0.997:
            a = np.asarray(grp.convert("RGBa"), np.float32) * ealpha
            grp = to_rgba(a.astype(np.uint8))
        frame.alpha_composite(grp)

    if lifted:
        L = seg(t, 5.0, 6.7)
        cq = cpose.project(rect_pts(CW, CH))
        rec = seg(t, 15.9, 17.3)
        shadow(frame, [cq], (lerp(6, 16, L), lerp(10, 30, L) * (1 - 0.6 * rec)), lerp(10, 34, L), 0.26 * calpha)
        draw_card(frame, A, cpose, calpha, cblur, None, t)

    for Zp, p, pd in petals:
        if Zp <= card_z:
            draw_petal(Zp, p, pd)

    # sparkles anchored to the card in 3D
    spa = seg(t, 5.8, 6.8) * (1 - seg(t, 15.6, 16.5)) * abs(math.cos(math.radians(cpose_d["ry"]))) ** 3
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
            size = sz * (0.6 + 0.4 * tw) * FOC / cpose.C[2] * 1.4
            half = size
            quad = [(sxy[0] - half, sxy[1] - half), (sxy[0] + half, sxy[1] - half), (sxy[0] + half, sxy[1] + half), (sxy[0] - half, sxy[1] + half)]
            draw_quad(frame, A["sparkle"], quad, alpha=a, resample=Image.BILINEAR)

    # closing text
    ca = seg(t, 16.5, 17.7) * (1 - seg(t, 18.6, 19.75))
    if ca > 0.003:
        lay = A["closing"]
        dy = 16 * (1 - seg(t, 16.5, 17.9)) - 8 * seg(t, 18.6, 19.75)
        if abs(dy) > 0.02:
            lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -dy), Image.BICUBIC)
        a = np.asarray(lay, np.float32) * ca
        frame.alpha_composite(to_rgba(np.clip(a, 0, 255).astype(np.uint8)))

    frame.alpha_composite(A["vignette"])
    return frame.convert("RGB")



def draw_card(frame, A, pose, alpha, blur, clip, t):
    quad = pose.project(rect_pts(CW, CH))
    front = facing(quad)
    n = pose.normal()
    sh = lambert(n, back=not front)
    ry = math.radians(_ry_of(pose))
    tex = A["card_front"] if front else A["card_back"]
    if not front:
        # back face: texture's left edge sits at card-local +x
        quad = pose.project([(CW / 2, -CH / 2, 0), (-CW / 2, -CH / 2, 0), (-CW / 2, CH / 2, 0), (CW / 2, CH / 2, 0)])
    shine_p = (t - 7.0) / 2.2  # gold sweep across the names
    sheen = 0.16 * abs(math.sin(ry)) ** 0.8

    def modify(arr, k, w, h):
        P = Tex.PAD
        f = w / tex.w0
        if clip is not None:
            r = int(P + clip * TS * f)
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
                m = tex.extra[k]
                c2 = lerp(-0.1, 1.35, shine_p)
                add += 0.75 * np.exp(-((diag - c2) / 0.05) ** 2) * m
            a[..., :3] += add[..., None] * (a[..., 3:4] * np.array([1.0, 0.97, 0.88]) - a[..., :3])
            arr[...] = np.clip(a, 0, 255).astype(np.uint8)

    draw_quad(frame, tex, quad, alpha=alpha, blur=blur, shade=sh, modify=modify)


def _ry_of(pose):
    # recover yaw from rotation matrix (R = Ry Rx Rz): R[0,2] = sin(ry) cos(rx), R[2,2] = cos(ry) cos(rx)
    return math.degrees(math.atan2(pose.R[0, 2], pose.R[2, 2]))


# ---------------------------------------------------------------- workers
_A = None


def _init():
    global _A
    _A = build_assets()


def _job(args):
    i, out_dir = args
    t = i / FPS
    render(t, _A).save(os.path.join(out_dir, f"f{i:04d}.png"), compress_level=1)
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", type=float, nargs="*", help="render still(s) at time(s) to scratch and exit")
    ap.add_argument("--out", default=None, help="dir for --still output")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()

    if args.still:
        A = build_assets()
        od = Path(args.out or TMP_BASE)
        od.mkdir(parents=True, exist_ok=True)
        for t in args.still:
            p = od / f"still_{t:05.2f}.png"
            render(t, A).save(p)
            print(p)
        return

    usage = shutil.disk_usage(Path(TMP_BASE).parent if not Path(TMP_BASE).exists() else TMP_BASE)
    if usage.free < 4 * 1024 ** 3:
        sys.exit(f"not enough free disk: {usage.free / 1e9:.1f} GB")
    os.makedirs(TMP_BASE, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="rawuh-video-", dir=TMP_BASE)
    t0 = time.time()
    try:
        ctx = get_context("spawn")
        with ctx.Pool(args.workers, initializer=_init) as pool:
            for n, _ in enumerate(pool.imap_unordered(_job, [(i, tmp) for i in range(NF)], chunksize=4)):
                if n % 60 == 0:
                    print(f"  frame {n}/{NF}  {time.time() - t0:.0f}s", flush=True)
        print(f"rendered {NF} frames in {time.time() - t0:.0f}s")
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [FFMPEG, "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
               "-i", str(MUSIC), "-map", "0:v", "-map", "1:a", "-t", f"{DUR}",
               "-af", f"afade=t=in:st=0:d=0.5,afade=t=out:st={DUR - 1.5}:d=1.5",
               "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "1500k", "-bufsize", "3000k",
               "-profile:v", "high", "-pix_fmt", "yuv420p", "-x264-params", "threads=8",
               "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-movflags", "+faststart", str(OUT_MP4)]
        subprocess.run(cmd, check=True)
        _init()
        render(POSTER_T, _A).save(OUT_POSTER, "WEBP", quality=80, method=6)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{OUT_MP4}  {OUT_MP4.stat().st_size / 1e6:.2f} MB")
    print(f"{OUT_POSTER}  {OUT_POSTER.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
