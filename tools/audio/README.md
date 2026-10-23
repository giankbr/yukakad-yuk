# Rawuh demo music generator

`demo_music.py` synthesizes the background-music loops used by invitation
themes. Every sound is generated from code with numpy (additive synthesis,
band-limited wavetables, Karplus-Strong plucked strings, filtered noise, a
synthetic noise-IR reverb). No samples, soundfonts or downloaded audio are
used, so the tracks are original work and royalty-free.

## Run

```bash
python3 tools/audio/demo_music.py              # all moods + tracks.json
python3 tools/audio/demo_music.py gamelan      # re-render selected moods only
```

Requirements: Python 3 + numpy (no scipy needed), and `ffmpeg` with
libmp3lame (`/opt/homebrew/bin/ffmpeg` or on `PATH`; override with
`FFMPEG=/path/to/ffmpeg`). Output is deterministic (fixed seeds).

Output goes to `frontend/public/music/demo/<mood>.mp3` plus `tracks.json`.
A summary table (duration, size, peak, loudness, BPM, loop-seam check) is
printed at the end.

## Tracks

| mood | title | BPM | bars | what it is |
|---|---|---|---|---|
| `romantis` | Piano Romantis | 70 | 12 | Soft felt piano arpeggios I–V–vi–IV in C, warm pad, melody from bar 5 |
| `gamelan` | Gamelan Keraton | 60 | 12 (3 gongan × 16 beats) | Slendro balungan on demung-like metallophone (partials 1 / 2.76 / 5.4 / 8.93), saron off-beat anticipation, kenong, kempul, deep beating gong each gongan |
| `nusantara` | Kecapi Nusantara | 72 | 12 | Karplus-Strong kecapi/sasando: low ostinato + pentatonic melody, soft frame drum |
| `religi` | Doa & Harapan | 60 | 10 | No percussion/bells. Evolving pad Am–F–C–G–Esus4, A/E drone, breathy flute lead |
| `akustik` | Petikan Akustik | 84 | 16 | Fingerpicked Karplus-Strong guitar G–D–Em–C, very light shaker |
| `ceria` | Ceria | 112 | 16 | Marimba melody (glockenspiel doubling 2nd half), marimba bass/chords, soft kick/clap/hats |
| `khidmat` | Khidmat | 76 | 12 | Piano + string ensemble + cello, I–IV–vi–V in D, hymn-like melody from bar 5 |

## How looping works

Each track is rendered into a buffer exactly N bars long. Notes and the
reverb are added circularly, so tails past the end wrap onto the start.
All EQ is applied in the frequency domain on the circular buffer. The file
starts a few ms before bar 1 (quietest point of the previous tail), so MP3
edge frames code a quiet passage. Use `loop = true`, or Web Audio
`AudioBufferSourceNode.loop` for fully sample-accurate looping.

## Mastering

K-weighted, gated loudness (BS.1770 style) normalized to −16 LUFS, a gentle
look-ahead limiter at −2 dBFS sample peak (decoded MP3 peaks stay ≤ −1 dBFS),
mono 44.1 kHz, 64 kbps CBR MP3, ID3 title "Rawuh — <Title>", artist "Rawuh".
