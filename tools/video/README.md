# Rawuh demo video ("Video Ucapan 3D")

`demo_video.py` renders the example invitation video shown on `/produk/video-ucapan-3d`.
Everything is drawn from code (numpy + Pillow): paper textures, envelope, wax seal, card,
rose petals, sparkles and bokeh. No footage, stock or AI images.

"3D" is faked with a pinhole camera: each flat layer is a planar quad posed in 3D, projected,
and warped with a perspective homography (premultiplied RGBa, mip-mapped so text stays crisp),
plus parallax bokeh, depth-of-field blur, Lambert shading, a moving sheen and soft drop shadows.

    python3 tools/video/demo_video.py              # render 600 frames + encode (~20 s on 10 cores)
    python3 tools/video/demo_video.py --still 8 12 # debug stills -> $RAWUH_TMP (default /private/tmp/claude-502)

Requires numpy, Pillow >= 10, ffmpeg (libx264 + aac). Fonts are macOS system fonts
(Snell Roundhand, Didot, Avenir Next). Output is deterministic (fixed seeds).
Temp PNG frames go to `$RAWUH_TMP` and are deleted after encoding.

Outputs:
- `frontend/public/rawuh/video-ucapan-demo.mp4` — 720x1280, 30 fps, 20 s, H.264 yuv420p + AAC 96k, faststart
- `frontend/public/rawuh/video-ucapan-demo-poster.webp` — frame at 8 s (names reveal)

Audio is `frontend/public/music/demo/romantis.mp3` (synthesized, see `tools/audio`), trimmed with
0.5 s fade-in / 1.5 s fade-out.

Timeline: 0–5 s envelope turns in, flap opens, card slides out · 5–11 s push-in on the card
(names with gold shine sweep, petals, sparkles) · 11–16 s card flips to the back (date, venue,
guest area) · 16–20 s closing line + "Dibuat dengan Rawuh · rawuh.id", fade to the opening background.
