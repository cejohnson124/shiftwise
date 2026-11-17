// Usage:
//   node render.js stills            -> stills/*.png (one per scene)
//   node render.js video             -> shiftwise-ad.mp4 (1080x1080, 60fps, H.264 + AAC)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const ffmpeg = require('ffmpeg-static');
const fs = require('fs');
const path = require('path');

const FPS = 60, DUR = 30;
const HERE = __dirname;
const URL = 'file:///' + path.join(HERE, 'shiftwise-ad.html').replace(/\\/g, '/') + '?render';

function chromePath() {
  if (process.env.PW_CHROME) return process.env.PW_CHROME;
  const root = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright');
  if (!fs.existsSync(root)) return undefined;
  const dirs = fs.readdirSync(root).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse();
  for (const d of dirs) {
    const exe = path.join(root, d, 'chrome-headless-shell-win64', 'chrome-headless-shell.exe');
    if (fs.existsSync(exe)) return exe;
  }
  return undefined;
}

const STILLS = [
  ['1-manager-struggling', 4.2],
  ['2-marcus-asks', 7.4],
  ['3-zoom-schedule', 8.95],
  ['4-wedding-door', 12.0],
  ['5-employee-submits', 18.6],
  ['6-manager-generates', 22.6],
  ['7-board-falls', 24.2],
  ['8-dance', 26.2],
  ['9-logo', 29.5],
];

(async () => {
  const mode = process.argv[2] || 'stills';
  const browser = await chromium.launch({ executablePath: chromePath() });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(URL);
  await page.waitForFunction('window.__ready === true', null, { timeout: 30000 });
  const shot = () => page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1080, height: 1080 } });

  if (mode === 'stills') {
    fs.mkdirSync(path.join(HERE, 'stills'), { recursive: true });
    for (const [name, t] of STILLS) {
      await page.evaluate(t => window.seek(window.toReal(t)), t);
      fs.writeFileSync(path.join(HERE, 'stills', name + '.png'), await shot());
      console.log('still', name, t);
    }
  } else {
    const out = path.join(HERE, 'shiftwise-ad.mp4');
    const ff = spawn(ffmpeg, ['-y', '-hide_banner', '-loglevel', 'error',
      '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-i', path.join(HERE, 'music.wav'),
      '-map', '0:v', '-map', '1:a',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(FPS),
      '-c:a', 'aac', '-b:a', '192k', '-t', String(DUR), '-movflags', '+faststart', out],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const total = FPS * DUR;
    for (let i = 0; i < total; i++) {
      await page.evaluate(t => window.seek(t), i / FPS);
      const buf = await shot();
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 300 === 0) console.log(`frame ${i}/${total}`);
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
    console.log('wrote', out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
