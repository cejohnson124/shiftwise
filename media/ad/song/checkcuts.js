const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const root=path.join(process.env.LOCALAPPDATA,'ms-playwright'); const d=fs.readdirSync(root).filter(x=>x.startsWith('chromium_headless_shell-')).sort().reverse()[0];
(async()=>{ const b=await chromium.launch({executablePath:path.join(root,d,'chrome-headless-shell-win64','chrome-headless-shell.exe')});
 const p=await b.newPage({viewport:{width:1080,height:1080}});
 await p.goto('file:///'+path.join(__dirname,'..','shiftwise-ad.html').split(path.sep).join('/')+'?render'); await p.waitForFunction('window.__ready');
 const r=await p.evaluate(()=>{ const out=[]; let prev='';
  for(let i=0;i<1800;i++){ window.seek(i/60); const vis=['office','wed','phonesc','logo'].filter(id=>document.getElementById(id).style.display==='block').join();
    if(vis!==prev){ out.push([i,(i/60).toFixed(3),vis]); prev=vis; } } return out; });
 const beats=JSON.parse(fs.readFileSync(path.join(__dirname,'beats.json')));
 for(const [f,t,v] of r){ const nb=beats.reduce((a,x)=>Math.abs(x-t)<Math.abs(a-t)?x:a); console.log(`frame ${f} t=${t} -> ${v.padEnd(8)} nearest beat ${nb.toFixed(3)} off ${((t-nb)*1000).toFixed(0)}ms`); }
 await b.close(); })();
