"""Build a theme's styles.module.css = shared base + the theme's own CSS.
Usage: python3 /tmp/pen/base/mkcss.py <theme-id>
Reads /tmp/pen/themes-src/<id>.css (first line must be the /* Theme — description */ comment)."""
import sys
tid = sys.argv[1]
base = open("/tmp/pen/base/base.css").read()
src = open(f"/tmp/pen/themes-src/{tid}.css").read().lstrip()
head, _, rest = src.partition("*/")
out = head + "*/\n" + base + "\n/* ── Theme ── */\n" + rest.lstrip("\n")
open(f"/root/w/frontend/src/components/invitation/themes/{tid}/styles.module.css", "w").write(out)
print("wrote", tid, len(out), "bytes")
