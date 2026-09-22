// Run with the dev server active: node scripts/check-wedding-templates.mjs
// Set CHROME_BIN on non-macOS machines. UPDATE_PREVIEWS=1 refreshes catalog images.
import { spawn } from 'node:child_process';
import { mkdtemp, readFile, writeFile, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';

const directory = await mkdtemp(join(tmpdir(), 'yukakad-template-check-'));
const browser = spawn(process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--remote-debugging-port=0', `--user-data-dir=${directory}`, 'about:blank'], { stdio: 'ignore' });
let socket;
try {
  let port;
  for (let i = 0; i < 100; i++) {
    try { port = (await readFile(join(directory, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; break; } catch { await new Promise(r => setTimeout(r, 100)); }
  }
  assert(port, 'Chrome did not start');
  const targets = await (await fetch(`http://localhost:${port}/json`)).json();
  socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(r => socket.addEventListener('open', r, { once: true }));
  let id = 0;
  const pending = new Map();
  socket.addEventListener('message', ({ data }) => {
    const message = JSON.parse(data);
    if (pending.has(message.id)) { const { resolve, reject } = pending.get(message.id); pending.delete(message.id); if (message.error) reject(message.error); else resolve(message.result); }
  });
  const call = (method, params = {}) => new Promise((resolve, reject) => { pending.set(++id, { resolve, reject }); socket.send(JSON.stringify({ id, method, params })); });
  const evaluate = async expression => {
    const result = await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  await call('Page.enable');
  for (const variant of ['alyra', 'weddings', 'veloria']) {
    for (const width of [1440, 390]) {
      await call('Emulation.setDeviceMetricsOverride', { width, height: 1000, deviceScaleFactor: 1, mobile: width < 700 });
      await call('Page.navigate', { url: `${process.env.PREVIEW_ORIGIN || 'http://localhost:3001'}/invitation/demo?template=${variant}` });
      for (let i = 0; i < 100; i++) {
        if (await evaluate(`document.readyState === 'complete' && !!document.querySelector('#rsvp form') && document.querySelector('aside')?.textContent.includes('${variant}')`)) break;
        await new Promise(r => setTimeout(r, 150));
      }
      await evaluate(`[...document.images].forEach(img => img.loading = 'eager'); document.fonts.ready.then(() => Promise.all([...document.images].map(img => img.complete ? null : new Promise(r => { img.onload = r; img.onerror = r; setTimeout(r, 8000); }))))`);
      await evaluate(`new Promise(r => setTimeout(r, 800))`);
      const result = await evaluate(`({heading:document.querySelector('h1')?.textContent, width:innerWidth, scroll:document.documentElement.scrollWidth, broken:[...document.images].filter(i=>i.complete && !i.naturalWidth).map(i=>i.src)})`);
      assert(result.heading?.includes('Alya'), `${variant}: missing heading`);
      assert(result.scroll <= result.width, `${variant}: horizontal overflow at ${width}: ${result.scroll}`);
      assert.equal(result.broken.length, 0, `${variant}: broken images ${result.broken}`);
      const shot = await call('Page.captureScreenshot', { format: 'png' });
      await writeFile(join(directory, `${variant}-${width}.png`), Buffer.from(shot.data, 'base64'));
      const metrics = await call('Page.getLayoutMetrics');
      const full = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width, height: metrics.cssContentSize.height, scale: 1 } });
      await writeFile(join(directory, `${variant}-${width}-full.png`), Buffer.from(full.data, 'base64'));
      if (width === 1440 && process.env.UPDATE_PREVIEWS === '1') {
        await mkdir('public/templates', { recursive: true });
        await writeFile(`public/templates/${variant}-preview.png`, Buffer.from(shot.data, 'base64'));
      }
      await evaluate(`document.querySelector('#rsvp input[name=name]').value='Preview Guest'; document.querySelector('#rsvp form').requestSubmit();`);
      await evaluate(`new Promise(r => setTimeout(r, 200))`);
      assert(await evaluate(`document.querySelector('#rsvp [role=status]')?.textContent.includes('tidak dikirim')`), `${variant}: demo RSVP failed`);
      console.log(`PASS ${variant} ${width}px: heading, images, overflow, demo RSVP`);
    }
  }
  console.log(`Screenshots: ${directory}`);
} finally { socket?.close(); browser.kill(); }
