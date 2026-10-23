#!/usr/bin/env python3
"""
Rawuh demo background-music generator.

Every sound in this file is synthesized from scratch with numpy (additive
synthesis, wavetables, Karplus-Strong plucked strings, filtered noise) - no
samples, soundfonts or downloaded audio are used, so the output is original
and royalty-free.

Run:   python3 tools/audio/demo_music.py            (all moods)
       python3 tools/audio/demo_music.py romantis   (one or more moods)

Output: frontend/public/music/demo/<mood>.mp3 + tracks.json

Design notes
- Each track is rendered into a buffer that is exactly N bars long. Every note,
  and the reverb, is added *circularly* (index modulo N), so tails that run
  past the end wrap onto the start -> seamless `loop = true` playback.
- All filtering is done in the frequency domain on the whole circular buffer
  (zero-phase, loop-safe). Any LFO is either note-local or loop-periodic.
- Loudness: ITU-R BS.1770 style K-weighted, gated integrated loudness,
  normalized to -16 LUFS, with a gentle look-ahead peak limiter (-2 dBFS
  sample peak before encoding so the decoded MP3 stays <= -1 dBFS).
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 44100
SEED = 20261024
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_DIR = os.path.join(ROOT, "frontend", "public", "music", "demo")
FFMPEG = os.environ.get("FFMPEG", "/opt/homebrew/bin/ffmpeg")
if not os.path.exists(FFMPEG):
    FFMPEG = "ffmpeg"
BITRATE = "64k"  # CBR mono; MPEG-1 L3 has no 72k step, 80k would exceed 450 KB at 48 s
TARGET_LUFS = -16.0
PEAK_CEIL_DB = -2.0
TAU = 2 * np.pi

# --------------------------------------------------------------------------
# basic helpers
# --------------------------------------------------------------------------
NOTE_IDX = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def m(name):
    """'C#4' -> midi number."""
    pc = NOTE_IDX[name[0]]
    i = 1
    if name[i] == "#":
        pc += 1
        i += 1
    elif name[i] == "b":
        pc -= 1
        i += 1
    return pc + 12 * (int(name[i:]) + 1)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def db(x):
    return 20 * np.log10(max(x, 1e-12))


class Track:
    """Circular render buffer split into named buses."""

    def __init__(self, bpm, bars, beats_per_bar=4):
        self.bpm = bpm
        self.beat = 60.0 / bpm
        self.bars = bars
        self.bpb = beats_per_bar
        self.n = int(round(bars * beats_per_bar * self.beat * SR))
        self.buses = {}

    def t(self, beat):
        return beat * self.beat

    def add(self, bus, sig, t_sec, gain=1.0):
        if bus not in self.buses:
            self.buses[bus] = np.zeros(self.n)
        buf = self.buses[bus]
        s = int(round(t_sec * SR)) % self.n
        sig = sig * gain
        L = len(sig)
        while L > 0:  # circular add (wraps tails onto the start)
            take = min(L, self.n - s)
            buf[s:s + take] += sig[:take]
            sig = sig[take:]
            L -= take
            s = 0


def fade_env(n, attack, release_at=None, release=0.05):
    """Raised-cosine attack, optional raised-cosine release starting at
    release_at seconds. Guarantees the sample array ends at exactly 0."""
    e = np.ones(n)
    a = max(int(attack * SR), 1)
    a = min(a, n)
    e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    if release_at is not None:
        rs = int(release_at * SR)
        rl = max(int(release * SR), 1)
        if rs < n:
            seg = min(rl, n - rs)
            e[rs:rs + seg] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(seg) / rl)
            e[rs + seg:] = 0
    # always end at zero (tiny 3 ms tail fade)
    k = min(int(0.003 * SR), n)
    e[n - k:] *= np.linspace(1, 0, k)
    return e


def spectral_gain(x, fn):
    """Apply a zero-phase, circular frequency-domain gain fn(freqs)->gain."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= fn(f)
    return np.fft.irfft(X, len(x))


def lp(fc, order=2):
    return lambda f: 1.0 / np.sqrt(1.0 + (f / fc) ** (2 * order))


def hp(fc, order=2):
    def g(f):
        r = np.where(f > 0, (fc / np.maximum(f, 1e-9)) ** (2 * order), np.inf)
        return 1.0 / np.sqrt(1.0 + r)
    return g


def peak_eq(fc, gain_db, q=1.0):
    """Smooth bell on a log-frequency axis."""
    def g(f):
        lf = np.log2(np.maximum(f, 1.0) / fc)
        w = 1.0 / (q * 1.2)
        return 10 ** (gain_db / 20 * np.exp(-0.5 * (lf / w) ** 2))
    return g


def low_shelf(fc, gain_db):
    return lambda f: 10 ** (gain_db / 20 / (1.0 + (f / fc) ** 2))


def chain(*fns):
    def g(f):
        out = np.ones_like(f)
        for fn in fns:
            out = out * fn(f)
        return out
    return g


def band_noise(n, lo, hi, rng):
    x = rng.standard_normal(n)
    y = spectral_gain(x, chain(hp(lo, 2), lp(hi, 2)))
    return y / (np.sqrt(np.mean(y ** 2)) + 1e-12)


# --------------------------------------------------------------------------
# instruments
# --------------------------------------------------------------------------
def modal(f0, partials, n, rng, attack=0.002, release_at=None, release=0.15,
          maxf=9000.0):
    """Sum of exponentially decaying sinusoids.
    partials: list of (ratio, amp, t60_fast, t60_slow, slow_mix, detune_hz)."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    for ratio, amp, t60a, t60b, mix, det in partials:
        f = f0 * ratio + det
        if f > maxf or f > 0.45 * SR:
            continue
        ph = rng.uniform(0, TAU)
        env = (1 - mix) * np.exp(-6.91 * t / t60a) + mix * np.exp(-6.91 * t / t60b)
        out += amp * env * np.sin(TAU * f * t + ph)
    return out * fade_env(n, attack, release_at, release)


def piano(midi, dur, vel, rng, pedal_release=0.35):
    """Soft felt piano: inharmonic partials, two-stage decay, 2 strings."""
    f0 = hz(midi)
    B = 0.00035 * (f0 / 261.6) ** 0.5  # inharmonicity
    slow = float(np.clip(5.0 * (261.6 / f0) ** 0.55, 1.2, 9.0))
    n = int((dur + pedal_release + 0.05) * SR)
    n = min(n, int((slow * 1.2 + 0.2) * SR))
    parts = []
    bright = 0.70 + 0.22 * vel
    for k in range(1, 20):
        fk = k * f0 * np.sqrt(1 + B * k * k)
        if fk > 6000:
            break
        amp = (1.0 / k ** 1.1) * bright ** (k - 1)
        amp *= 1.0 / (1.0 + (fk / 3200.0) ** 2)  # felt hammer softness
        if k == 1:
            amp *= 0.9
        ta = slow * 0.16 / (1 + 0.55 * (k - 1))
        tb = slow / (1 + 0.35 * (k - 1))
        parts.append((fk / f0, amp, ta, tb, 0.45, 0.0))
        if k <= 4:  # second string, slightly detuned -> warm beating
            parts.append((fk / f0, amp * 0.6, ta, tb, 0.45, 0.35 + 0.1 * k))
    sig = modal(f0, parts, n, rng, attack=0.004, release_at=dur,
                release=pedal_release, maxf=6000)
    return sig * vel


_tables = {}


def table(shape, nh):
    """Band-limited single-cycle wavetable."""
    key = (shape, nh)
    if key in _tables:
        return _tables[key]
    T = 4096
    x = np.arange(T) / T
    w = np.zeros(T)
    for k in range(1, nh + 1):
        if shape == "saw":
            a = 1.0 / k
        elif shape == "warm":  # rounded saw, darker
            a = 1.0 / k ** 1.6
        elif shape == "flute":
            a = {1: 1.0, 2: 0.18, 3: 0.07, 4: 0.025}.get(k, 0.0)
        else:  # soft triangle-ish (odd harmonics)
            a = (1.0 / k ** 2) if k % 2 else 0.0
        w += a * np.sin(TAU * k * x)
    w /= np.max(np.abs(w))
    _tables[key] = w
    return w


def wt_osc(tab, freq, n, phase0=0.0):
    """freq: scalar or per-sample array."""
    f = np.broadcast_to(np.asarray(freq, dtype=float), (n,))
    ph = phase0 + np.cumsum(f) / SR
    idx = (ph % 1.0) * len(tab)
    i0 = idx.astype(np.int64) % len(tab)
    frac = idx - np.floor(idx)
    i1 = (i0 + 1) % len(tab)
    return tab[i0] * (1 - frac) + tab[i1] * frac


def pad_note(midi, dur, rng, attack=1.2, release=1.8, shape="warm",
             cutoff=2200.0, voices=3, detune_cents=7.0, vib=0.0, vib_rate=5.0):
    f0 = hz(midi)
    nh = max(1, min(40, int(cutoff / f0)))
    tab = table(shape, nh)
    n = int((dur + release + 0.05) * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for v in range(voices):
        c = 0.0 if voices == 1 else detune_cents * (2 * v / (voices - 1) - 1)
        fv = f0 * 2 ** (c / 1200)
        if vib > 0:
            rate = vib_rate * rng.uniform(0.9, 1.1)
            depth = vib * np.clip(t / 0.6, 0, 1)
            fv = fv * (1 + depth * np.sin(TAU * rate * t + rng.uniform(0, TAU)))
        out += wt_osc(tab, fv, n, rng.uniform())
    out /= voices
    return out * fade_env(n, attack, dur, release)


def flute(midi, dur, rng, vel=1.0):
    """Breathy flute / suling-like lead: sine-ish tone + band-limited breath."""
    f0 = hz(midi)
    rel = 0.35
    n = int((dur + rel + 0.05) * SR)
    t = np.arange(n) / SR
    vdepth = 0.0035 * np.clip((t - 0.35) / 0.6, 0, 1)
    fv = f0 * (1 + vdepth * np.sin(TAU * 4.8 * t + rng.uniform(0, TAU)))
    tone = wt_osc(table("flute", 4), fv, n, rng.uniform())
    breath = band_noise(n, f0 * 0.85, f0 * 1.2, rng) * 0.10
    breath += band_noise(n, 300, 2200, rng) * 0.035
    # breath is stronger at the onset ("chiff")
    bre = 0.6 + 0.4 * np.exp(-t / 0.12)
    amp_swell = 0.85 + 0.15 * np.clip(t / 0.8, 0, 1)
    sig = (tone * amp_swell + breath * bre)
    return sig * fade_env(n, 0.12, dur, rel) * vel


def ks_pluck(midi, dur, rng, t60=2.5, bright=0.5, pos=0.2, release=0.12,
             max_len=4.0):
    """Karplus-Strong plucked string (vectorized block recursion),
    pitch-corrected by resampling for exact tuning."""
    f0 = hz(midi)
    P = SR / f0
    L = int(np.floor(P - 0.5))
    ratio = P / (L + 0.5)  # >= 1 : stretch factor
    n_out = int(min(dur + release + 0.05, max_len) * SR)
    M = int(n_out / ratio) + L + 4
    g = 10 ** (-3.0 / (t60 * f0))  # per-period loop gain for target T60
    g = min(g / np.cos(np.pi / (L + 0.5)), 0.99995)  # undo averaging-filter loss
    # excitation: noise, soft-lowpassed (finger/plectrum), pluck-position comb
    exc = rng.uniform(-1, 1, L)
    a = 0.15 + 0.8 * (1 - bright)  # one-pole smoothing coefficient
    for _ in range(2):
        y = np.empty(L)
        acc = 0.0
        for i in range(L):
            acc = (1 - a) * exc[i] + a * acc
            y[i] = acc
        exc = y
    exc -= exc.mean()
    d = max(1, int(pos * L))
    exc = exc - np.roll(exc, d)
    exc -= exc.mean()
    exc /= np.max(np.abs(exc)) + 1e-12
    ybuf = np.zeros(M + 1)  # ybuf[i] == y[i-1]
    y = ybuf[1:]
    y[:L] = exc
    s = L
    while s < M:
        e = min(s + L, M)
        y[s:e] = g * 0.5 * (y[s - L:e - L] + ybuf[s - L:e - L])
        s = e
    # resample to exact pitch
    pos_idx = np.arange(n_out) / ratio
    out = np.interp(pos_idx, np.arange(M), y)
    return out * fade_env(n_out, 0.0015, dur, release)


def kick(rng, amp=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 58 + 70 * np.exp(-t / 0.035)
    ph = np.cumsum(f) / SR
    body = np.sin(TAU * ph) * np.exp(-t / 0.16)
    click = band_noise(n, 800, 3000, rng) * np.exp(-t / 0.004) * 0.08
    return (body + click) * fade_env(n, 0.002) * amp


def clap(rng, amp=1.0):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    env = np.zeros(n)
    for off in (0.0, 0.009, 0.018):
        tt = np.clip(t - off, 0, None)
        env += np.where(t >= off, np.exp(-tt / 0.006), 0) * 0.6
    env += np.where(t >= 0.025, np.exp(-np.clip(t - 0.025, 0, None) / 0.07), 0)
    sig = band_noise(n, 900, 2600, rng) * env
    return sig * fade_env(n, 0.001) * amp * 0.5


def hat(rng, amp=1.0, decay=0.025):
    n = int(0.15 * SR)
    t = np.arange(n) / SR
    sig = band_noise(n, 5500, 9000, rng) * np.exp(-t / decay)
    return sig * fade_env(n, 0.001) * amp


def shaker(rng, amp=1.0):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    env = np.clip(t / 0.018, 0, 1) ** 2 * np.exp(-np.clip(t - 0.018, 0, None) / 0.035)
    sig = band_noise(n, 3000, 7000, rng) * env
    return sig * fade_env(n, 0.002) * amp


def frame_drum(rng, kind="dung", amp=1.0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    if kind == "dung":
        f = 72 + 28 * np.exp(-t / 0.05)
        body = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t / 0.22)
        skin = band_noise(n, 150, 700, rng) * np.exp(-t / 0.02) * 0.25
        sig = body + skin
    else:  # "tak": rim/skin slap
        tone = np.sin(TAU * 310 * t) * np.exp(-t / 0.045) * 0.5
        skin = band_noise(n, 700, 2200, rng) * np.exp(-t / 0.03) * 0.5
        sig = tone + skin
    return sig * fade_env(n, 0.002) * amp


# --------------------------------------------------------------------------
# reverb (circular convolution with a frequency-dependent decaying noise IR)
# --------------------------------------------------------------------------
def make_ir(rng, t60=2.4, length=3.2, predelay=0.018, dark=1.0):
    n = int(length * SR)
    t = np.arange(n) / SR
    bands = [(20, 500, 1.0, 0.55), (500, 2000, 0.9, 1.0),
             (2000, 5000, 0.6 / dark, 0.7), (5000, 12000, 0.35 / dark, 0.35)]
    ir = np.zeros(n)
    for lo, hi, tscale, g in bands:
        nb = band_noise(n, lo, hi, rng)
        ir += g * nb * np.exp(-6.91 * t / (t60 * tscale))
    # diffuse onset
    ir *= np.clip(t / 0.03, 0, 1) ** 1.5
    # a few early reflections
    for dt, a in ((0.011, 0.5), (0.019, -0.35), (0.027, 0.3), (0.041, -0.22)):
        i = int(dt * SR)
        ir[i] += a * 3.0
    ir *= fade_env(n, 0.0, length - 0.3, 0.3)
    pd = int(predelay * SR)
    ir = np.concatenate([np.zeros(pd), ir])
    ir /= np.sqrt(np.sum(ir ** 2))
    return ir


def reverb_circular(x, ir):
    n = len(x)
    h = np.zeros(n)
    h[:min(len(ir), n)] = ir[:n]
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(h), n)


# --------------------------------------------------------------------------
# loudness (BS.1770-style) + limiter
# --------------------------------------------------------------------------
def _biquad_resp(b, a, w):
    z = np.exp(-1j * w)
    return (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)


def k_weight(x):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    w = TAU * f / SR
    # stage 1: high shelf (+4 dB @ ~1.5 kHz)
    G, Q, fc = 4.0, 1 / np.sqrt(2), 1500.0
    A = 10 ** (G / 40)
    w0 = TAU * fc / SR
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    b1 = [A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al),
          -2 * A * ((A - 1) + (A + 1) * c),
          A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al)]
    a1 = [(A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al,
          2 * ((A - 1) - (A + 1) * c),
          (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al]
    # stage 2: high pass @ 38 Hz
    Q, fc = 0.5, 38.0
    w0 = TAU * fc / SR
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    b2 = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
    a2 = [1 + al, -2 * c, 1 - al]
    H = _biquad_resp(b1, a1, w) * _biquad_resp(b2, a2, w)
    return np.fft.irfft(np.fft.rfft(x) * H, len(x))


def lufs(x):
    y = k_weight(x)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    yy = np.concatenate([y, y[:blk]])  # circular (it's a loop)
    ms = np.array([np.mean(yy[i:i + blk] ** 2) for i in range(0, len(y), hop)])
    ld = -0.691 + 10 * np.log10(ms + 1e-20)
    g = ms[ld > -70]
    if len(g) == 0:
        return -120.0
    rel = -0.691 + 10 * np.log10(np.mean(g)) - 10
    g2 = ms[(ld > -70) & (ld > rel)]
    return -0.691 + 10 * np.log10(np.mean(g2))


def _running_min_circ(g, radius):
    """min over [n-radius, n+radius] (window rounded up to a power of 2)."""
    out = g.copy()
    span, k = 1, 1
    while span < 2 * radius + 1:
        out = np.minimum(out, np.roll(out, -k))
        span += k
        k *= 2
    return np.roll(out, span // 2)


def _box_circ(g, width):
    c = np.cumsum(np.concatenate([g[-width:], g]))
    return (c[width:] - c[:-width]) / width


def limit(x, ceil_db):
    thr = 10 ** (ceil_db / 20)
    req = np.minimum(1.0, thr / np.maximum(np.abs(x), 1e-12))
    if req.min() >= 1.0:
        return x
    r = int(0.02 * SR)
    gmin = _running_min_circ(req, r)
    # box average of width <= window radius keeps gain <= required at peaks
    g = _box_circ(gmin, r)
    g = np.roll(g, -(r // 2))
    return x * np.minimum(g, 1.0)


def finalize(x):
    x = x - np.mean(x)
    for _ in range(4):
        L = lufs(x)
        x = x * 10 ** ((TARGET_LUFS - L) / 20)
        x = limit(x, PEAK_CEIL_DB)
    x = np.clip(x, -0.98, 0.98)  # safety only, never expected to engage
    return x


# --------------------------------------------------------------------------
# mixing helper
# --------------------------------------------------------------------------
def mix(track, sends, rng, ir_kw=None, master=None, wet=0.3):
    """sends: {bus: (gain, reverb_send)}"""
    dry = np.zeros(track.n)
    rev = np.zeros(track.n)
    for bus, buf in track.buses.items():
        g, s = sends.get(bus, (1.0, 0.3))
        dry += buf * g
        rev += buf * g * s
    ir = make_ir(rng, **(ir_kw or {}))
    out = dry + wet * reverb_circular(rev, ir) * 3.0
    f = master or chain(hp(35, 2), lp(9000, 2))
    out = spectral_gain(out, f)
    return out


def vel_h(rng, base, spread=0.06):
    return float(np.clip(base + rng.uniform(-spread, spread), 0.05, 1.0))


def tim_h(rng, ms=6):
    return rng.uniform(-ms, ms) / 1000.0


# --------------------------------------------------------------------------
# tracks
# --------------------------------------------------------------------------
def seq(notes):
    """[(name|None, dur_beats), ...] -> [(midi|None, start, dur)]"""
    out, t = [], 0.0
    for name, d in notes:
        out.append((None if name is None else m(name), t, d))
        t += d
    return out, t


def romantis():
    rng = np.random.default_rng(SEED + 1)
    tr = Track(bpm=70, bars=12)
    chords = [  # I - V - vi - IV in C
        ("C2", ["C3", "G3", "C4", "E4", "G4", "E4", "C4", "G3"], ["C3", "G3", "E4"]),
        ("G1", ["G2", "D3", "G3", "B3", "D4", "B3", "G3", "D3"], ["B2", "D3", "G3"]),
        ("A1", ["A2", "E3", "A3", "C4", "E4", "C4", "A3", "E3"], ["A2", "E3", "C4"]),
        ("F1", ["F2", "C3", "F3", "A3", "C4", "A3", "F3", "C3"], ["A2", "C3", "F3"]),
    ]
    for bar in range(tr.bars):
        bass, arp, padv = chords[bar % 4]
        b0 = bar * 4
        bar_len = tr.t(4)
        # arpeggio (eighths), sustain-pedal: ring until end of bar
        for i, nm in enumerate(arp):
            st = tr.t(b0 + i * 0.5) + tim_h(rng, 5)
            v = vel_h(rng, 0.42 if i else 0.5)
            ring = bar_len - i * tr.t(0.5) + 0.05
            tr.add("piano", piano(m(nm), ring, v, rng), st)
        # low root on beat 1
        tr.add("piano", piano(m(bass) + 12, tr.t(4), 0.38, rng), tr.t(b0))
        for nm in padv:
            tr.add("pad", pad_note(m(nm), bar_len, rng, attack=1.0, release=1.6,
                                   cutoff=1400), tr.t(b0) - 0.25)
    mel, L = seq([
        ("G4", 1), ("C5", 1), ("E5", 2),
        ("D5", 3), ("B4", 1),
        ("E5", 1), ("D5", 1), ("C5", 2),
        ("A4", 3), ("G4", 1),
        ("G4", 1), ("C5", 1), ("E5", 1), ("G5", 1),
        ("F5", 1), ("E5", 1), ("D5", 2),
        ("C5", 1), ("E5", 1), ("D5", 1), ("C5", 1),
        ("C5", 4),
    ])
    assert L == 32
    for nt, st, d in mel:
        tr.add("melody", piano(nt, tr.t(d) + 0.15, vel_h(rng, 0.62), rng),
               tr.t(16 + st) + tim_h(rng, 8))
    out = mix(tr, {"piano": (0.7, 0.5), "melody": (1.5, 0.4),
                   "pad": (0.11, 0.6)}, rng,
              ir_kw=dict(t60=2.6), wet=0.32,
              master=chain(hp(45, 2), low_shelf(160, -5), lp(7500, 2)))
    return out, tr


SLENDRO_CENTS = {1: 0, 2: 231, 3: 474, 5: 717, 6: 955}


def slendro(deg, octave=0, base=268.0):
    return base * 2 ** ((SLENDRO_CENTS[deg] + 1200 * octave) / 1200)


def gamelan():
    rng = np.random.default_rng(SEED + 2)
    tr = Track(bpm=60, bars=12)  # 3 gongan x 16 beats = 48 s
    # balungan (deg, octave); original melodies
    A = [(3, 0), (5, 0), (3, 0), (2, 0), (3, 0), (5, 0), (3, 0), (2, 0),
         (6, 0), (5, 0), (3, 0), (2, 0), (5, 0), (3, 0), (2, 0), (1, 0)]
    B = [(6, -1), (1, 0), (6, -1), (5, -1), (3, 0), (5, 0), (6, 0), (5, 0),
         (1, 1), (6, 0), (5, 0), (3, 0), (5, 0), (6, 0), (5, 0), (3, 0)]
    C = [(2, 0), (3, 0), (2, 0), (1, 0), (2, 0), (3, 0), (2, 0), (1, 0),
         (3, 0), (5, 0), (3, 0), (2, 0), (6, -1), (1, 0), (2, 0), (6, -1)]
    gongan = [A, B, C]

    def saron(f, vel, damp=1.0):
        parts = [(1.0, 1.0, 1.2, 3.2, 0.6, 0.0), (1.0, 0.35, 1.2, 3.2, 0.6, 1.3),
                 (2.76, 0.45, 0.5, 1.4, 0.5, 0.0), (2.76, 0.12, 0.5, 1.4, 0.5, 0.9),
                 (5.40, 0.16, 0.25, 0.6, 0.4, 0.0), (8.93, 0.05, 0.12, 0.3, 0.3, 0.0)]
        n = int((damp + 0.3) * SR)
        sig = modal(f, parts, n, rng, attack=0.002, release_at=damp, release=0.25,
                    maxf=6500)
        thump = band_noise(n, 80, 600, rng) * np.exp(-np.arange(n) / SR / 0.008) * 0.06
        return (sig + thump * fade_env(n, 0.001)) * vel

    def kenong(f, vel):
        parts = [(1.0, 1.0, 1.5, 3.5, 0.7, 0.0), (1.0, 0.5, 1.5, 3.5, 0.7, 1.6),
                 (2.01, 0.25, 0.8, 2.0, 0.5, 0.0), (2.98, 0.10, 0.4, 1.0, 0.4, 0.0)]
        return modal(f, parts, int(3.8 * SR), rng, attack=0.006) * vel

    def kempul(f, vel):
        parts = [(1.0, 1.0, 2.0, 5.0, 0.7, 0.0), (1.0, 0.6, 2.0, 5.0, 0.7, 1.9),
                 (1.49, 0.25, 1.0, 2.5, 0.5, 0.0), (2.0, 0.30, 1.0, 3.0, 0.5, 0.0),
                 (2.63, 0.12, 0.5, 1.5, 0.4, 0.0)]
        return modal(f, parts, int(5.5 * SR), rng, attack=0.012) * vel

    def gong(f, vel):
        parts = [(1.0, 1.0, 4.0, 11.0, 0.8, 0.0), (1.0, 0.8, 4.0, 11.0, 0.8, 0.9),
                 (2.02, 0.55, 3.0, 8.0, 0.7, 0.0), (2.02, 0.35, 3.0, 8.0, 0.7, 1.3),
                 (2.94, 0.30, 2.0, 5.0, 0.6, 0.0), (4.10, 0.12, 1.0, 3.0, 0.5, 0.0),
                 (5.32, 0.05, 0.6, 1.5, 0.4, 0.0)]
        n = int(12 * SR)
        sig = modal(f, parts, n, rng, attack=0.045)
        t = np.arange(n) / SR
        thump = band_noise(n, 40, 250, rng) * np.exp(-t / 0.05) * 0.15
        return (sig + thump * fade_env(n, 0.003)) * vel

    gong_f = slendro(2, -2)  # ~76 Hz
    for gi, bal in enumerate(gongan):
        g0 = gi * 16
        for k, (deg, octv) in enumerate(bal):
            beat = g0 + k
            f = slendro(deg, octv)
            st = tr.t(beat) + tim_h(rng, 6)
            # demung (low saron) on the beat
            tr.add("saron", saron(f, vel_h(rng, 0.55 + (0.08 if k % 2 else 0.0))), st)
            # saron barung (octave up), anticipating on the off-beat, from gongan 2
            nxt = gongan[(gi + (k + 1) // 16) % 3][(k + 1) % 16]
            if gi >= 1:
                tr.add("peking", saron(slendro(nxt[0], nxt[1] + 1),
                                       vel_h(rng, 0.22), damp=0.45),
                       tr.t(beat + 0.5) + tim_h(rng, 8))
            pos = k + 1  # 1..16
            if pos % 4 == 0:
                tr.add("kenong", kenong(slendro(deg, octv), 0.5), st + 0.01)
            if pos in (6, 10, 14):
                tr.add("kempul", kempul(slendro(deg, octv - 1), 0.5), st + 0.01)
            if pos == 16:
                tr.add("gong", gong(gong_f, 1.0), st + 0.02)
    out = mix(tr, {"saron": (0.55, 0.45), "peking": (0.6, 0.5),
                   "kenong": (0.45, 0.5), "kempul": (0.5, 0.4),
                   "gong": (0.45, 0.25)}, rng,
              ir_kw=dict(t60=2.8, dark=1.3), wet=0.30,
              master=chain(hp(35, 2), low_shelf(120, -3), lp(7000, 2)))
    return out, tr


def nusantara():
    rng = np.random.default_rng(SEED + 3)
    tr = Track(bpm=72, bars=12)
    # 4-bar harmonic loop on G major pentatonic: G G Em D
    ost = {
        "G": ["G2", "D3", "B3", "D3", "G2", "D3", "A3", "D3"],
        "Em": ["E2", "B2", "G3", "B2", "E2", "B2", "A3", "B2"],
        "D": ["D2", "A2", "E3", "A2", "D2", "A2", "D3", "A2"],
    }
    prog = ["G", "G", "Em", "D"]
    for bar in range(tr.bars):
        pat = ost[prog[bar % 4]]
        for i, nm in enumerate(pat):
            st = tr.t(bar * 4 + i * 0.5) + tim_h(rng, 5)
            v = 0.55 if i % 4 == 0 else 0.38
            tr.add("indung", ks_pluck(m(nm), tr.t(1.0), rng, t60=2.2, bright=0.25,
                                      pos=0.18) * vel_h(rng, v), st)
        # frame drum: dung on 1 & 3, soft tak on 2& and 4
        b0 = bar * 4
        tr.add("drum", frame_drum(rng, "dung", 0.9), tr.t(b0))
        tr.add("drum", frame_drum(rng, "dung", 0.6), tr.t(b0 + 2))
        tr.add("drum", frame_drum(rng, "tak", 0.35), tr.t(b0 + 1.5) + tim_h(rng, 4))
        tr.add("drum", frame_drum(rng, "tak", 0.45), tr.t(b0 + 3) + tim_h(rng, 4))
        if bar % 2 == 1:
            tr.add("drum", frame_drum(rng, "tak", 0.25), tr.t(b0 + 3.5) + tim_h(rng, 4))
    mel, L = seq([
        ("D5", 1), ("E5", .5), ("D5", .5), ("B4", 1), ("G4", 1),
        ("A4", 1.5), ("B4", .5), ("D5", 2),
        ("E5", 1), ("G5", 1), ("E5", .5), ("D5", .5), ("B4", 1),
        ("A4", 3), (None, 1),
        ("G5", 1), ("E5", .5), ("D5", .5), ("E5", 1), ("G5", 1),
        ("A5", 1.5), ("G5", .5), ("E5", 2),
        ("D5", 1), ("E5", .5), ("D5", .5), ("B4", 1), ("A4", 1),
        ("A4", 1), ("B4", 1), ("D5", 2),
        ("D5", 1), ("E5", .5), ("D5", .5), ("B4", 1), ("D5", 1),
        ("E5", 1.5), ("D5", .5), ("B4", 2),
        ("A4", 1), ("B4", .5), ("A4", .5), ("G4", 1), ("E4", 1),
        ("G4", 4),
    ])
    assert L == 48, L
    for nt, st, d in mel:
        if nt is None:
            continue
        dur = tr.t(d) + 0.4
        tr.add("rincik", ks_pluck(nt, dur, rng, t60=3.0, bright=0.45, pos=0.13,
                                  release=0.25) * vel_h(rng, 0.7), tr.t(st) + tim_h(rng, 6))
        # sasando-like shimmer: soft octave-down sympathetic string
        tr.add("rincik", ks_pluck(nt - 12, dur, rng, t60=2.5, bright=0.3, pos=0.3,
                                  release=0.25) * 0.25, tr.t(st) + 0.012)
    out = mix(tr, {"indung": (0.55, 0.35), "rincik": (1.0, 0.45),
                   "drum": (0.3, 0.2)}, rng,
              ir_kw=dict(t60=2.2), wet=0.30,
              master=chain(hp(40, 2), lp(5800, 2), peak_eq(180, 1.5)))
    return out, tr


def religi():
    rng = np.random.default_rng(SEED + 4)
    tr = Track(bpm=60, bars=10)
    chords = [  # 2 bars each, A minor: Am F C G Esus4
        ["A2", "E3", "A3", "C4", "E4"],
        ["F2", "C3", "A3", "C4", "F4"],
        ["C3", "G3", "C4", "E4", "G4"],
        ["G2", "D3", "B3", "D4", "G4"],
        ["E2", "B2", "E3", "A3", "B3"],
    ]
    clen = tr.t(8)
    for ci, ch in enumerate(chords):
        st = tr.t(ci * 8) - 1.0
        for j, nm in enumerate(ch):
            tr.add("pad", pad_note(m(nm), clen, rng, attack=2.4, release=3.0,
                                   cutoff=1100 + 250 * j, voices=3, detune_cents=6,
                                   vib=0.0012, vib_rate=0.25) * (1.0 if j else 0.8), st)
            # gentle swell layer (soft string-ish) on upper chord tones
            if j >= 2:
                tr.add("swell", pad_note(m(nm) + 12, clen * 0.6, rng, attack=3.0,
                                         release=2.8, shape="saw", cutoff=2400,
                                         voices=2, detune_cents=4, vib=0.002),
                       st + tr.t(2))
    # low drone (A + E) as overlapping long notes, one per 2 bars
    for i in range(5):
        for nm, g in (("A2", 0.6), ("E3", 0.35)):
            tr.add("drone", pad_note(m(nm), clen, rng, attack=3.0, release=3.0,
                                     shape="tri", cutoff=500, voices=2, detune_cents=3)
                   * g, tr.t(i * 8) - 1.5)
    mel, L = seq([
        ("A4", 2), ("C5", 2), ("D5", 1.5), ("C5", .5), ("A4", 2),
        ("G4", 1), ("A4", 1), ("C5", 2), ("E5", 3), (None, 1),
        ("D5", 2), ("C5", 1), ("B4", 1), ("G4", 3), (None, 1),
        ("E5", 2), ("D5", 1), ("B4", 1), ("A4", 3), (None, 1),
    ])
    assert L == 32
    for nt, st, d in mel:
        if nt is None:
            continue
        tr.add("flute", flute(nt, tr.t(d) - 0.05, rng, vel_h(rng, 0.8, 0.05)),
               tr.t(8 + st))
    out = mix(tr, {"pad": (0.3, 0.5), "swell": (0.1, 0.7), "drone": (0.35, 0.3),
                   "flute": (0.55, 0.5)}, rng,
              ir_kw=dict(t60=3.4, dark=1.4), wet=0.36,
              master=chain(hp(40, 2), low_shelf(120, -3), lp(5500, 2)))
    return out, tr


def akustik():
    rng = np.random.default_rng(SEED + 5)
    tr = Track(bpm=84, bars=16)
    # voicing: (root bass, alt bass, s3, s2, s1, top-melody options)
    vo = {
        "G": ("G2", "D3", "G3", "B3", "D4", ["G4", "D4", "B3"]),
        "D": ("D3", "A2", "A3", "D4", "F#4", ["A4", "F#4", "E4"]),
        "Em": ("E2", "B2", "G3", "B3", "E4", ["G4", "E4", "D4"]),
        "C": ("C3", "G2", "G3", "C4", "E4", ["E4", "G4", "D4"]),
    }
    prog = ["G", "D", "Em", "C"]
    for bar in range(tr.bars):
        r, alt, s3, s2, s1, tops = vo[prog[bar % 4]]
        b0 = bar * 4
        busy = bar >= 8
        top = tops[(bar // 4) % 3] if busy else s1
        pattern = [(0, r, 0.7), (0, top, 0.45), (0.5, s3, 0.35), (1, alt, 0.6),
                   (1.5, s2, 0.4), (2, r, 0.62), (2.5, top if busy else s1, 0.42),
                   (3, alt, 0.58), (3.5, s2, 0.38)]
        if busy and bar % 2:
            pattern.append((3.75, s3, 0.3))
        for beat, nm, v in pattern:
            st = tr.t(b0 + beat) + tim_h(rng, 7)
            ring = tr.t(4 - beat) + 0.2  # let ring until chord change
            tr.add("guitar", ks_pluck(m(nm), ring, rng, t60=3.2 if nm in (r, alt) else 2.4,
                                      bright=0.3, pos=0.16 + rng.uniform(-.03, .03),
                                      release=0.15) * vel_h(rng, v), st)
        for i in range(8):  # very light shaker on eighths
            tr.add("shaker", shaker(rng, 0.5 if i % 2 else 0.28), tr.t(b0 + i * 0.5) + tim_h(rng, 5))
    body = chain(hp(60, 2), peak_eq(110, 3.0), peak_eq(230, 2.0), peak_eq(3200, -3.0, 1.5),
                 lp(5200, 2))
    tr.buses["guitar"] = spectral_gain(tr.buses["guitar"], body)
    out = mix(tr, {"guitar": (1.0, 0.35), "shaker": (0.1, 0.4)}, rng,
              ir_kw=dict(t60=1.8), wet=0.26,
              master=chain(hp(45, 2), lp(8000, 2)))
    return out, tr


def ceria():
    rng = np.random.default_rng(SEED + 6)
    tr = Track(bpm=112, bars=16)

    def marimba(midi, vel, dur=0.6):
        f = hz(midi)
        sc = (261.6 / f) ** 0.5
        parts = [(1.0, 1.0, 0.5 * sc, 1.1 * sc, 0.4, 0.0),
                 (3.93, 0.22, 0.08, 0.18, 0.3, 0.0),
                 (9.2, 0.05, 0.03, 0.06, 0.3, 0.0)]
        n = int(min(dur + 0.2, 1.6 * sc + 0.2) * SR)
        return modal(f, parts, n, rng, attack=0.0015, maxf=7000) * vel

    def glock(midi, vel):
        f = hz(midi)
        parts = [(1.0, 1.0, 0.9, 2.0, 0.5, 0.0), (2.76, 0.12, 0.3, 0.6, 0.4, 0.0),
                 (5.40, 0.03, 0.1, 0.2, 0.3, 0.0)]
        return modal(f, parts, int(1.8 * SR), rng, attack=0.0015, maxf=7000) * vel

    prog = ["C", "F", "G", "C", "C", "Am", "F", "G",
            "F", "G", "Em", "Am", "F", "G", "C", "G"]
    roots = {"C": "C3", "F": "F2", "G": "G2", "Am": "A2", "Em": "E3"}
    triad = {"C": ["E4", "G4", "C5"], "F": ["F4", "A4", "C5"], "G": ["D4", "G4", "B4"],
             "Am": ["E4", "A4", "C5"], "Em": ["E4", "G4", "B4"]}
    for bar, ch in enumerate(prog):
        b0 = bar * 4
        r = m(roots[ch])
        for beat, note, v in ((0, r, 0.75), (1.5, r + 12, 0.45), (2, r + 7, 0.6),
                              (3, r + 12, 0.5)):
            tr.add("bass", marimba(note, vel_h(rng, v), dur=0.5), tr.t(b0 + beat))
        for off in (0.5, 1.5, 2.5, 3.5):  # chord stabs on off-beats
            for nm in triad[ch]:
                tr.add("chords", marimba(m(nm), vel_h(rng, 0.22), dur=0.25),
                       tr.t(b0 + off) + tim_h(rng, 3))
        tr.add("kick", kick(rng, 0.9), tr.t(b0))
        tr.add("kick", kick(rng, 0.7), tr.t(b0 + 2))
        if bar % 2 == 1:
            tr.add("kick", kick(rng, 0.45), tr.t(b0 + 2.5))
        tr.add("clap", clap(rng, 0.8), tr.t(b0 + 1) + 0.004)
        tr.add("clap", clap(rng, 0.8), tr.t(b0 + 3) + 0.004)
        for i in range(8):
            tr.add("hat", hat(rng, 0.55 if i % 2 else 0.3), tr.t(b0 + i * 0.5) + tim_h(rng, 4))
    E = 0.5  # eighth
    mel, L = seq([
        ("E5", E), ("G5", E), ("C6", 2 * E), ("G5", E), ("E5", E), ("G5", 2 * E),
        ("A5", E), ("G5", E), ("F5", 2 * E), ("A5", E), ("C6", E), ("A5", 2 * E),
        ("G5", 2 * E), ("F5", E), ("E5", E), ("D5", 2 * E), ("B4", 2 * E),
        ("C5", 3 * E), ("E5", E), ("G5", 4 * E),
        ("E5", E), ("G5", E), ("C6", 2 * E), ("D6", E), ("C6", E), ("G5", 2 * E),
        ("A5", 2 * E), ("C6", E), ("A5", E), ("E5", 4 * E),
        ("F5", E), ("G5", E), ("A5", 2 * E), ("G5", E), ("F5", E), ("E5", 2 * E),
        ("D5", 3 * E), (None, E), ("G4", E), ("A4", E), ("B4", 2 * E),
        ("C5", 2 * E), ("A5", 2 * E), ("A5", E), ("G5", E), ("F5", 2 * E),
        ("B4", 2 * E), ("G5", 2 * E), ("G5", E), ("F5", E), ("E5", 2 * E),
        ("E5", E), ("G5", E), ("B5", 2 * E), ("A5", E), ("G5", E), ("E5", 2 * E),
        ("A5", 4 * E), ("G5", 2 * E), ("E5", 2 * E),
        ("F5", E), ("A5", E), ("C6", 2 * E), ("A5", E), ("C6", E), ("D6", 2 * E),
        ("D6", 2 * E), ("B5", 2 * E), ("G5", 2 * E), ("A5", E), ("B5", E),
        ("C6", 3 * E), ("G5", E), ("E5", 2 * E), ("G5", 2 * E),
        ("F5", E), ("E5", E), ("D5", 2 * E), ("B4", 2 * E), ("D5", 2 * E),
    ])
    assert L == 64, L
    for nt, st, d in mel:
        if nt is None:
            continue
        tr.add("melody", marimba(nt, vel_h(rng, 0.7), dur=tr.t(d)), tr.t(st) + tim_h(rng, 4))
        if st >= 32:  # glockenspiel doubling in the second half (octave up, soft)
            tr.add("glock", glock(nt + 12, vel_h(rng, 0.35)), tr.t(st) + 0.003)
    out = mix(tr, {"melody": (0.8, 0.3), "glock": (0.22, 0.4), "bass": (0.55, 0.12),
                   "chords": (0.5, 0.3), "kick": (0.4, 0.05), "clap": (0.2, 0.35),
                   "hat": (0.08, 0.15)}, rng,
              ir_kw=dict(t60=1.4), wet=0.22,
              master=chain(hp(40, 2), lp(8500, 2)))
    return out, tr


def khidmat():
    rng = np.random.default_rng(SEED + 7)
    tr = Track(bpm=76, bars=12)
    prog = [  # I - IV - vi - V in D
        ("D2", ["D3", "A3", "D4", "F#4"], ["F#3", "A3", "D4", "F#4"]),
        ("G2", ["G3", "B3", "D4", "G4"], ["G3", "B3", "D4", "G4"]),
        ("B1", ["F#3", "B3", "D4", "F#4"], ["F#3", "B3", "D4", "F#4"]),
        ("A1", ["E3", "A3", "C#4", "E4"], ["E3", "A3", "C#4", "E4"]),
    ]
    blen = tr.t(4)
    for bar in range(tr.bars):
        bass, pchord, schord = prog[bar % 4]
        b0 = bar * 4
        # piano: bass octave on 1, chord on 1 and 3 (stately half-note pulse)
        tr.add("piano", piano(m(bass) + 12, blen, 0.5, rng), tr.t(b0))
        tr.add("piano", piano(m(bass), blen, 0.35, rng), tr.t(b0))
        for half in (0, 2):
            for j, nm in enumerate(pchord):
                tr.add("piano", piano(m(nm), tr.t(2) + 0.1, vel_h(rng, 0.36 if half else 0.42),
                                      rng), tr.t(b0 + half) + 0.006 * j)
        # strings: sustained chord + cello root
        for nm in schord:
            tr.add("strings", pad_note(m(nm), blen, rng, attack=0.45, release=0.9,
                                       shape="saw", cutoff=2600, voices=4,
                                       detune_cents=8, vib=0.0028, vib_rate=5.2),
                   tr.t(b0) - 0.1)
        tr.add("cello", pad_note(m(bass) + 12, blen, rng, attack=0.35, release=0.9,
                                 shape="saw", cutoff=1600, voices=3, detune_cents=5,
                                 vib=0.0025, vib_rate=5.0), tr.t(b0) - 0.05)
    mel, L = seq([
        ("F#5", 2), ("E5", 1), ("D5", 1),
        ("D5", 3), ("B4", 1),
        ("F#5", 2), ("D5", 2),
        ("E5", 4),
        ("A5", 2), ("F#5", 1), ("D5", 1),
        ("G5", 1), ("F#5", 1), ("E5", 2),
        ("D5", 2), ("F#5", 2),
        ("E5", 3), ("C#5", 1),
    ])
    assert L == 32
    for nt, st, d in mel:
        tr.add("melody", piano(nt, tr.t(d) + 0.1, vel_h(rng, 0.6), rng), tr.t(16 + st))
        tr.add("melstr", pad_note(nt, tr.t(d), rng, attack=0.3, release=0.7, shape="saw",
                                  cutoff=3000, voices=3, detune_cents=6, vib=0.003),
               tr.t(16 + st))
    out = mix(tr, {"piano": (0.6, 0.4), "melody": (1.3, 0.4), "strings": (0.22, 0.6),
                   "cello": (0.22, 0.4), "melstr": (0.18, 0.6)}, rng,
              ir_kw=dict(t60=2.8), wet=0.32,
              master=chain(hp(40, 2), low_shelf(150, -4), lp(7500, 2)))
    return out, tr


TRACKS = {
    "romantis": ("Piano Romantis", romantis),
    "gamelan": ("Gamelan Keraton", gamelan),
    "nusantara": ("Kecapi Nusantara", nusantara),
    "religi": ("Doa & Harapan", religi),
    "akustik": ("Petikan Akustik", akustik),
    "ceria": ("Ceria", ceria),
    "khidmat": ("Khidmat", khidmat),
}


# --------------------------------------------------------------------------
# encode / verify
# --------------------------------------------------------------------------
def encode(x, path, title):
    pcm = x.astype("<f4").tobytes()
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
           "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
           "-c:a", "libmp3lame", "-b:a", BITRATE, "-ar", str(SR), "-ac", "1",
           "-id3v2_version", "3", "-metadata", f"title={title}",
           "-metadata", "artist=Rawuh", "-metadata", "album=Rawuh Demo Music",
           "-metadata", "comment=Synthesized from code; royalty-free", path]
    subprocess.run(cmd, input=pcm, check=True)


def decode(path):
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", path,
           "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").astype(float)


def quiet_rotation(x, search=(0.30, 0.01), win=0.01):
    """Pick the quietest 10 ms spot shortly before the downbeat (inside the
    previous cycle's tail) as the file's start/end point. The loop is circular
    so this changes nothing musically, but MP3 frames at the file edges code a
    quiet passage instead of a note attack -> cleaner seam after encoding."""
    w = int(win * SR)
    lo, hi = int(search[0] * SR), int(search[1] * SR)
    seg = x[len(x) - lo:len(x) - hi]
    e = np.convolve(seg ** 2, np.ones(w) / w, "same")
    return lo - int(np.argmin(e))  # samples before the downbeat


def seam_stats(x):
    """Discontinuity at the loop point vs. normal sample-to-sample motion."""
    jump = abs(x[0] - x[-1])
    typical = np.percentile(np.abs(np.diff(x)), 99)
    w = int(0.02 * SR)
    r_end = np.sqrt(np.mean(x[-w:] ** 2))
    r_start = np.sqrt(np.mean(x[:w] ** 2))
    return jump, typical, r_end, r_start


def centroid(x):
    X = np.abs(np.fft.rfft(x)) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return float(np.sum(f * X) / np.sum(X))


def main(argv):
    names = argv[1:] or list(TRACKS)
    os.makedirs(OUT_DIR, exist_ok=True)
    rows, meta = [], []
    for mood in names:
        title, fn = TRACKS[mood]
        x, tr = fn()
        x = finalize(x)
        pre = quiet_rotation(x)
        x = np.roll(x, pre)  # file starts `pre` samples before bar 1
        path = os.path.join(OUT_DIR, f"{mood}.mp3")
        encode(x, path, f"Rawuh — {title}")
        y = decode(path)
        jump, typ, r_end, r_start = seam_stats(y)
        rows.append(dict(
            file=f"{mood}.mp3", dur=len(y) / SR, src_dur=tr.n / SR,
            size=os.path.getsize(path) / 1024, peak=db(np.max(np.abs(y))),
            lufs=lufs(y), bpm=tr.bpm, bars=tr.bars, jump=jump, typ=typ,
            r_end=db(r_end), r_start=db(r_start), cent=centroid(x)))
        meta.append({"mood": mood, "title": title, "bpm": tr.bpm,
                     "file": f"/music/demo/{mood}.mp3"})
        print(f"rendered {mood}", flush=True)
    if not argv[1:]:
        with open(os.path.join(OUT_DIR, "tracks.json"), "w") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    hdr = (f"{'file':<15}{'dur s':>7}{'size KB':>9}{'peak dBFS':>10}{'LUFS':>7}"
           f"{'BPM':>5}{'bars':>5}{'seam jump':>10}{'p99 step':>9}"
           f"{'end/start dB':>14}{'centroid':>9}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['file']:<15}{r['dur']:>7.2f}{r['size']:>9.0f}{r['peak']:>10.2f}"
              f"{r['lufs']:>7.1f}{r['bpm']:>5}{r['bars']:>5}{r['jump']:>10.4f}"
              f"{r['typ']:>9.4f}{r['r_end']:>7.1f}/{r['r_start']:<6.1f}"
              f"{r['cent']:>9.0f}")


if __name__ == "__main__":
    main(sys.argv)
