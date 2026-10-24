// Screenshots of Rawuh pages at phone size, through Chrome's DevTools protocol (no extra npm packages).
// Usage: node tools/screenshots/capture.mjs <out.png> <url> [width=390] [height=780] [scale=2] [waitMs=6000]
// Hides Next's dev indicator, so it works against `next dev` too.
import { spawn } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [out, url, width = "390", height = "780", scale = "2", wait = "6000"] = process.argv.slice(2);
if (!out || !url) { console.error("usage: capture.mjs <out.png> <url> [width] [height] [scale] [waitMs]"); process.exit(1); }

const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const profile = mkdtempSync(join(tmpdir(), "rawuh-shot-"));
const port = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank"], { stdio: "ignore" });
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

try {
  let target;
  for (let i = 0; i < 50 && !target; i++) {
    await sleep(200);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t => t.type === "page"); } catch { /* not up yet */ }
  }
  if (!target) throw new Error("Chrome did not start");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(resolve => ws.addEventListener("open", resolve, { once: true }));
  let id = 0;
  const pending = new Map();
  ws.addEventListener("message", event => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  });
  const send = (method, params = {}) => new Promise(resolve => { const n = ++id; pending.set(n, resolve); ws.send(JSON.stringify({ id: n, method, params })); });

  await send("Emulation.setDeviceMetricsOverride", { width: +width, height: +height, deviceScaleFactor: +scale, mobile: true });
  await send("Page.enable");
  await send("Page.navigate", { url });
  await sleep(+wait);
  await send("Runtime.evaluate", { expression: "document.querySelectorAll('nextjs-portal').forEach(n => n.remove()); window.scrollTo(0, 0); true" });
  await sleep(300);
  const shot = await send("Page.captureScreenshot", { format: "png" });
  writeFileSync(out, Buffer.from(shot.result.data, "base64"));
  ws.close();
  console.log(`saved ${out}`);
} finally {
  proc.kill();
  await sleep(300);
  rmSync(profile, { recursive: true, force: true });
}
