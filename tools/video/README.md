# Rawuh demo video ("Video Ucapan 3D")

`demo_video.py` renders the example invitation video shown on `/produk/video-ucapan-3d`.
Everything is drawn from code (numpy + Pillow): paper textures, envelope, wax seal, card,
rose petals, sparkles and bokeh. No footage, stock or AI images.

"3D" is faked with a pinhole camera: each flat layer is a planar quad posed in 3D, projected,
and warped with a perspective homography (premultiplied RGBa, mip-mapped so text stays crisp),
plus parallax bokeh, depth-of-field blur, Lambert shading, a moving sheen and soft drop shadows.

    python3 tools/video/demo_video.py                         # 1080x1920, 30 s, 900 frames (~70 s on 10 cores)
    python3 tools/video/demo_video.py --still 9 22.5          # debug stills (timeline seconds) -> $RAWUH_TMP
    python3 tools/video/demo_video.py --width 720 --duration 20 --fps 30 --crf 21

Layout is authored in design px on a 720x1280 frame and scaled by width/720 (text, blur radii, shadows,
textures all scale; text is supersampled). The timeline is authored for 30 s and time-scaled for other
durations. A fixed-seed static grain (dither) is added to every frame to prevent gradient banding.

Requires numpy, Pillow >= 10, ffmpeg (libx264 + aac). Fonts are macOS system fonts
(Snell Roundhand, Didot, Avenir Next). Output is deterministic (fixed seeds).
Temp PNG frames go to `$RAWUH_TMP` and are deleted after encoding.

Outputs:
- `frontend/public/rawuh/video-ucapan-demo.mp4` — 1080x1920, 30 fps, 30 s, H.264 High yuv420p (CRF 21, aq-mode 3) + AAC 96k, faststart
- `frontend/public/rawuh/video-ucapan-demo-poster.webp` — 1080x1920, frame at 9 s (names reveal)

Audio is `frontend/public/music/demo/romantis.mp3` (synthesized, see `tools/audio`), trimmed with
0.5 s fade-in / 2 s fade-out.

Timeline (30 s): 0–6 s envelope turns in, flap opens, card slides out · 6–13 s push-in on the card
(names with gold shine sweep, petals, sparkles) · 13–19 s card flips to the back (date, venue, guest
panel) · 19–25 s countdown "Menuju hari bahagia" (Hari/Jam/Menit/Detik tiles, digits roll each second)
· 25–30 s closing line + "Dibuat dengan Rawuh · rawuh.id", fade to the opening background (seamless loop).
Near (big, blurred) petals are confined to the frame edges; all other petals sit behind the card/text.

## Gallery styles (`--style`)

`--style blush` (default) is the main demo above. Twelve more presets render 15 s, 720x1280 gallery clips
to `frontend/public/rawuh/video-contoh/<slug>.mp4` + `<slug>-poster.webp` (poster at 4.9 s, names reveal):

    python3 tools/video/demo_video.py --gallery                      # all twelve (~3 min)
    python3 tools/video/demo_video.py --styles minang-gadang,wisuda-toga  # a subset
    python3 tools/video/demo_video.py --style navy-malam --out /tmp/x.mp4
    python3 tools/video/demo_video.py --style bali-kuning --still 1.6 4.9 10.8   # debug stills

| slug | intro | card | particles | highlight | music |
|---|---|---|---|---|---|
| `jawa-keraton` | carved gebyok doors with gunungan + kawung swing open | sogan brown, kawung border | rising gold dust | countdown (dark wood tiles) | gamelan |
| `islami-zamrud` | "Bismillahirrahmanirrahim" line, hanging lanterns | emerald mihrab arch, 8-point star pattern | lantern glows | countdown (arch tiles) | religi |
| `rustic-garden` | hanging wooden sign swings in on ropes | polaroid with painted landscape / kraft back | eucalyptus leaves | countdown (kraft tags) | akustik |
| `ultah-ceria` | gift box, lid pops off | bunting + candy "Arka" | balloons + confetti | big "7" pop + confetti burst | ceria |
| `navy-malam` | card flies in under stars, crescent moon, shooting star | navy art-deco frame, fan motifs | gold glitter, twinkling stars | countdown (deco tiles) | khidmat |
| `bali-kuning` | candi bentar split gate parts, "Om Swastyastu", penjor | stepped candi-top card, kamboja, patra band | frangipani | countdown | gamelan |
| `minang-gadang` | rumah gadang (gonjong roof) rises, then sinks away | black card with gonjong top, red songket band | gold sequins | countdown | nusantara |
| `sunda-siger` | "Sampurasun" + siger crown, melati strings drape in, mega mendung clouds drift | siger-peaked card | melati blossoms | countdown | gamelan |
| `modern-minimal` | hairline frame draws itself, card snaps in | sharp off-white / charcoal card, DIN type | none (grain only) | countdown | romantis |
| `watercolor-lavender` | lavender washes bleed in with wet edges, wisteria hangs | deckle-edged paper with washes | butterflies | countdown | romantis |
| `aqiqah-bintang` | crescent-moon cradle with a sleeping star bobs, then lifts away | cloud-topped card | pastel stars + twinkles | countdown (cloud tiles) | religi |
| `wisuda-toga` | mortarboard tossed up spinning, diploma scroll unrolls | parchment diploma with laurel + medal | gold confetti | countdown | khidmat |
