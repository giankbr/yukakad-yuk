// UI-only smoke test. API fixtures run only in an isolated Chrome profile.
import { spawn } from 'node:child_process';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';
const dir = await mkdtemp(join(tmpdir(), 'yukakad-workspace-'));
const browser = spawn(process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--remote-debugging-port=0', `--user-data-dir=${dir}`, 'about:blank'], { stdio: 'ignore' });
let socket;
try {
  let port;
  for (let i=0; i<100; i++) { try { port=(await readFile(join(dir,'DevToolsActivePort'),'utf8')).split('\n')[0]; break; } catch { await new Promise(r=>setTimeout(r,100)); } }
  assert(port);
  const targets=await (await fetch(`http://localhost:${port}/json`)).json();
  socket=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise(r=>socket.addEventListener('open',r,{once:true}));
  let id=0; const pending=new Map();
  socket.addEventListener('message',({data})=>{const m=JSON.parse(data); const p=pending.get(m.id); if(p){pending.delete(m.id); if(m.error)p.reject(m.error);else p.resolve(m.result);}});
  const call=(method,params={})=>new Promise((resolve,reject)=>{pending.set(++id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});assert(!r.exceptionDetails,JSON.stringify(r.exceptionDetails));return r.result.value;};
  await call('Page.enable');
  await call('Emulation.setFocusEmulationEnabled', { enabled: true });
  await call('Page.addScriptToEvaluateOnNewDocument',{source:`
    localStorage.setItem('yukakad_token','ui-test-only');
    localStorage.setItem('yukakad_name','Alya');
    const originalFetch=window.fetch.bind(window);
    window.fetch=(url,options)=>{
      if(String(url).includes('/api/auth/')) return Promise.resolve(new Response(JSON.stringify({error:'Contoh error untuk pengujian tampilan.'}),{status:400,headers:{'Content-Type':'application/json'}}));
      if(String(url).includes('/api/invitations')) return Promise.resolve(new Response(JSON.stringify({items:[{id:'test',title:'Alya & Rizky',slug:'alya-rizky',published:true,created_at:'2026-09-22'}]}),{headers:{'Content-Type':'application/json'}}));
      return originalFetch(url,options);
    };
  `});
  for(const route of ['/auth/register','/auth/login','/dashboard','/dashboard/invitations/create']) {
    for(const width of [1440,390]) {
      await call('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<700});
      await call('Page.navigate',{url:`${process.env.PREVIEW_ORIGIN||'http://localhost:3001'}${route}`});
      let ready=false;
      for(let i=0;i<100;i++){ready=await evaluate(`location.pathname===${JSON.stringify(route)} && document.readyState==='complete' && !!document.querySelector('h1')`);if(ready)break;await new Promise(r=>setTimeout(r,100));}
      assert(ready,`${route} did not load`);
      await evaluate(`document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,500)))`);
      assert(await evaluate(`document.documentElement.scrollWidth<=innerWidth`),`${route} ${width}: overflow`);
      assert(await evaluate(`getComputedStyle(document.querySelector('h1')).fontFamily.includes('Be Vietnam Pro')`),`${route}: wrong font`);
      if(route.startsWith('/auth')) {
        assert(await evaluate(`[...document.querySelectorAll('input')].every(i=>i.labels.length>0)`),'Unlabelled input');
        await evaluate(`document.querySelector('input').focus()`);
        assert(await evaluate(`getComputedStyle(document.activeElement).outlineStyle!=='none'`),'Missing focus');
      } else {
        assert(await evaluate(`getComputedStyle(document.querySelector('.dashboard-rail')).backgroundColor==='rgb(8, 8, 10)'`),'Wrong sidebar theme');
        assert(await evaluate(`document.querySelector('.db-nav-section').getBoundingClientRect().height>0`),'Hidden navigation');
      }
      const shot=await call('Page.captureScreenshot',{format:'png'});
      await writeFile(join(dir,`${route.replaceAll('/','-')}-${width}.png`),Buffer.from(shot.data,'base64'));
      console.log(`PASS ${route} ${width}px`);
    }
  }
  console.log(`Screenshots: ${dir}`);
} finally { socket?.close();browser.kill(); }
