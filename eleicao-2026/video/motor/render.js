// Renderiza as cenas do plano em MP4 (1080x1920, 30 fps), quadro a quadro, no Chromium do ambiente.
// Uso: node render.js <plano.json> <cidades.json> <pasta_saida> [--previa] [--cenas 0,3]
// --previa: em vez de vídeo, salva um PNG por cena no meio e no fim do tempo da cena.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');

(async () => {
  const [planoArq, dadosArq, saida] = process.argv.slice(2, 5);
  const previa = process.argv.includes('--previa');
  const iC = process.argv.indexOf('--cenas');
  const plano = JSON.parse(fs.readFileSync(planoArq, 'utf8'));
  const dados = JSON.parse(fs.readFileSync(dadosArq, 'utf8'));
  const quais = iC > 0 ? process.argv[iC + 1].split(',').map(Number) : plano.cenas.map((_, i) => i);
  fs.mkdirSync(saida, { recursive: true });
  const nav = await chromium.launch();
  const pag = await nav.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pag.goto('file://' + path.resolve(__dirname, 'telas.html'));
  await pag.evaluate(([d, p]) => { window.DADOS = d; window.PLANO = p; }, [dados, plano]);
  await pag.evaluate(() => document.fonts.ready);
  const FPS = plano.fps || 30;
  for (const i of quais) {
    const c = plano.cenas[i];
    if (previa) {
      for (const [rot, t] of [['meio', c.duracao * 0.5], ['fim', c.duracao - 0.05]]) {
        await pag.evaluate(([i, t]) => window.desenhar(i, t), [i, t]);
        await pag.screenshot({ path: path.join(saida, `cena${String(i).padStart(2, '0')}_${c.tipo}_${rot}.png`) });
      }
      continue;
    }
    const n = Math.round(c.duracao * FPS);
    const arq = path.join(saida, `cena${String(i).padStart(2, '0')}_${c.tipo}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '18', '-r', String(FPS), arq], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < n; f++) {
      await pag.evaluate(([i, t]) => window.desenhar(i, t), [i, f / FPS]);
      const buf = await pag.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('cena', i, c.tipo, n, 'quadros ->', arq);
  }
  await nav.close();
})().catch(e => { console.error(e); process.exit(1); });
