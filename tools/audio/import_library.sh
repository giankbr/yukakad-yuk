#!/usr/bin/env bash
# Trims, loudness-normalises and encodes the licensed recordings in LICENSES.md into frontend/public/music/library.
# Usage: tools/audio/import_library.sh <dir with the original downloads>
# The originals aren't committed; re-download them from the source links in LICENSES.md (file names below).
set -euo pipefail

SRC=${1:?usage: import_library.sh <source dir>}
OUT="$(cd "$(dirname "$0")/../.." && pwd)/frontend/public/music/library"
mkdir -p "$OUT"

# source file | output | seconds | channels | ID3 title
TRACKS=(
  "01-chopin-nocturne-op9-2.mp3|chopin-nocturne.mp3|150|stereo|Nocturne Op. 9 No. 2 (Chopin)"
  "02-satie-gymnopedie-1.ogg|satie-gymnopedie.mp3|150|stereo|Gymnopédie No. 1 (Satie)"
  "03-bali-xylophone.ogg|gamelan-bali.mp3|150|mono|Gamelan Bali"
  "04-gender-wayang-1928.ogg|gender-wayang.mp3|150|mono|Gendér Wayang (1928)"
  "05-pachelbel-canon-usaf.mp3|canon-pachelbel.mp3|150|stereo|Canon in D (Pachelbel)"
  "06-elgar-pomp-usmb.mp3|pomp-circumstance.mp3|150|stereo|Pomp and Circumstance No. 1 (Elgar)"
  "07-rain-stream-birds.mp3|hujan-alam.mp3|120|stereo|Hujan & Kicau Burung"
  "08-vocal-mmms.mp3|senandung.mp3|150|stereo|Senandung"
  "09-morning-garden.mp3|morning-garden.mp3|150|stereo|Morning Garden"
  "10-happy-ukulele.mp3|ukulele-ceria.mp3|128|stereo|Happy Ukulele"
)

for row in "${TRACKS[@]}"; do
  IFS='|' read -r src out len layout title <<<"$row"
  fade_out=$((len - 4))
  # Downmix first, then fade in/out (the player loops the file), normalise to -16 LUFS and keep peaks under -2 dBFS.
  ffmpeg -v error -y -t "$len" -i "$SRC/$src" -map 0:a:0 -map_metadata -1 \
    -af "aformat=channel_layouts=$layout,afade=t=in:d=1.5,afade=t=out:st=$fade_out:d=4,loudnorm=I=-16:TP=-2:LRA=11,alimiter=limit=0.79:level=disabled" \
    -ar 44100 -c:a libmp3lame -b:a 96k -id3v2_version 3 -metadata title="$title" -metadata artist="Rawuh library" "$OUT/$out"
  peak=$(ffmpeg -v info -i "$OUT/$out" -af volumedetect -f null - 2>&1 | grep -oE 'max_volume: [-0-9.]+' | cut -d' ' -f2)
  printf '%-24s %4ss  %5s KB  peak %s dB\n' "$out" "$len" "$(( $(wc -c <"$OUT/$out") / 1024 ))" "$peak"
done
