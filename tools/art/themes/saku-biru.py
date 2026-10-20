"""Saku Biru — the theme is a pure app UI mimic (no illustrations); only painted backdrops are added:
a brushed navy cover backdrop and a blue header backdrop, both with paper tooth and soft brushed light.
Run: python3 -I /tmp/pen/art/themes/saku-biru.py
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p8_lib import *  # noqa

OUT = outdir("saku-biru")
# cover: 390×844 css → 780×1400
bg = backdrop(780, 1400, [(0, "#0a4a74"), (0.45, "#063f63"), (1.0, "#03243a")],
              [(200, 120, 520, "#1c8fe0", 0.42), (720, 520, 420, "#0f6aa6", 0.3), (120, 1250, 460, "#021a2c", 0.55)], seed=21, streak=0.3, grain=0.45)
print("cover-bg", save_opaque(bg, f"{OUT}/cover-bg.webp", 74), round(kb(f"{OUT}/cover-bg.webp")), "KB")
# header: 390×~110 css → 780×240
hb = backdrop(780, 240, [(0, "#1c8fe0"), (1, "#0a4f7e")], [(680, 30, 420, "#5fb8f2", 0.45), (60, 230, 380, "#063f63", 0.5)], seed=23, streak=0.3, grain=0.4)
print("header-bg", save_opaque(hb, f"{OUT}/header-bg.webp", 74), round(kb(f"{OUT}/header-bg.webp")), "KB")
sheet = Image.new("RGB", (780, 700), "#042a42")
sheet.paste(Image.fromarray((bg[:560, ..., :3] * 255).astype(np.uint8)), (0, 0))
sheet.paste(Image.fromarray((hb[..., :3] * 255).astype(np.uint8)).resize((390, 120)), (20, 570))
sheet.save(f"{PREV}/sb-sheet.png")
print("total KB", round(sum(kb(f"{OUT}/{f}") for f in os.listdir(OUT))))
