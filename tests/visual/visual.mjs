/* ==========================================================================
   Test de regresión visual — sitio Diforza
   Compara capturas de las páginas contra una línea base (baseline), píxel a píxel.

   Uso:
     npm run test:visual:baseline   → genera la línea base con el sitio actual
     npm run test:visual            → compara el sitio actual contra la línea base

   Antes de un refactor: generar baseline. Después de cada cambio: comparar.
   Las capturas y los diffs quedan en tests/visual/output/ (fuera de git).
   La baseline debe generarse en la MISMA computadora que la comparación
   (cada sistema renderiza las fuentes distinto).
   ========================================================================== */
import { chromium } from "playwright";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";
import pixelmatch from "pixelmatch";

const ROOT = process.cwd();
const SITE_DIR = path.join(ROOT, "_site");
const OUT_DIR = path.join(ROOT, "tests", "visual", "output");
const PORT = 4173;
const MODE = process.argv[2] === "baseline" ? "baseline" : "current";

const PAGES = [
  { name: "home", url: "/" },
  { name: "indumentaria", url: "/indumentaria-de-trabajo/" },
  { name: "epp", url: "/epp-proteccion-industrial/" },
  { name: "calzado", url: "/calzado-de-seguridad/" },
];

// Página completa en estos anchos (alto de ventana 900)
const WIDTHS = [320, 375, 390, 430, 768, 1024, 1280, 1366, 1440, 1536, 1920];
// Solo la ventana visible (hero) en estas resoluciones
const SCREENS = [
  [1024, 600],
  [1280, 720],
  [1366, 768],
  [1280, 500],
];

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".webp": "image/webp",
  ".jpg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".pdf": "application/pdf",
};

function serve() {
  return http
    .createServer((req, res) => {
      let p = decodeURIComponent(req.url.split("?")[0]);
      if (p.endsWith("/")) p += "index.html";
      const file = path.join(SITE_DIR, p);
      if (!file.startsWith(SITE_DIR) || !fs.existsSync(file)) {
        res.writeHead(404);
        return res.end();
      }
      res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
      fs.createReadStream(file).pipe(res);
    })
    .listen(PORT);
}

const FREEZE_CSS = `*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}`;

async function capture(browser, page, w, h, fullPage) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: "reduce" });
  const tab = await ctx.newPage();
  await tab.goto(`http://localhost:${PORT}${page.url}`, { waitUntil: "networkidle" });
  await tab.addStyleTag({ content: FREEZE_CSS });
  // Recorre la página para disparar los scroll-reveal y la carga diferida
  await tab.evaluate(async () => {
    const step = window.innerHeight;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 60));
    }
    window.scrollTo(0, 0);
    await document.fonts.ready;
  });
  await tab.waitForTimeout(500);
  const buf = await tab.screenshot({ fullPage });
  await ctx.close();
  return buf;
}

function compare(a, b) {
  const A = PNG.sync.read(a);
  const B = PNG.sync.read(b);
  if (A.width !== B.width || A.height !== B.height) {
    return { diff: -1, size: `${A.width}x${A.height} → ${B.width}x${B.height}` };
  }
  const D = new PNG({ width: A.width, height: A.height });
  const diff = pixelmatch(A.data, B.data, D.data, A.width, A.height, { threshold: 0.1 });
  // ¿Ruido de fuentes? Pocos píxeles (<0,05%) repartidos por toda la página (muchas
  // franjas de 100px con alguna diferencia) = antialiasing del texto, no un cambio real.
  // Un cambio real suele concentrarse en una zona.
  let noise = false;
  if (diff && diff / (A.width * A.height) < 0.0005) {
    const bands = new Set();
    for (let y = 0; y < A.height; y++)
      for (let x = 0; x < A.width; x++) {
        const i = (y * A.width + x) * 4;
        if (D.data[i] === 255 && D.data[i + 1] === 0 && D.data[i + 2] === 0) { bands.add(Math.floor(y / 100)); break; }
      }
    noise = bands.size >= 12 && bands.size >= Math.ceil(A.height / 100) * 0.3;
  }
  return { diff, noise, png: diff ? PNG.sync.write(D) : null };
}

const server = serve();
// Flags para que el texto se dibuje siempre igual (sin GPU ni suavizado subpíxel):
// evita falsas alarmas por el antialiasing de las fuentes, sobre todo en Windows.
const browser = await chromium.launch({
  ...(process.env.PW_CHROMIUM_PATH ? { executablePath: process.env.PW_CHROMIUM_PATH } : {}),
  args: ["--disable-gpu", "--font-render-hinting=none", "--disable-lcd-text", "--disable-font-subpixel-positioning", "--force-color-profile=srgb"],
});
const dir = path.join(OUT_DIR, MODE);
fs.rmSync(dir, { recursive: true, force: true });
fs.mkdirSync(dir, { recursive: true });
if (MODE === "current") fs.rmSync(path.join(OUT_DIR, "diff"), { recursive: true, force: true });

const jobs = [];
for (const page of PAGES) {
  for (const w of WIDTHS) jobs.push({ page, w, h: 900, full: true, id: `${page.name}_${w}` });
  for (const [w, h] of SCREENS) jobs.push({ page, w, h, full: false, id: `${page.name}_${w}x${h}` });
}

// La carga de fuentes web y el raster pueden variar entre una captura y otra:
// si una captura difiere, se repite hasta RETRIES veces antes de darla por mala.
const RETRIES = 3;

let failed = 0;
let noisy = 0;
for (const j of jobs) {
  let buf = await capture(browser, j.page, j.w, j.h, j.full);
  if (MODE === "baseline") {
    fs.writeFileSync(path.join(dir, `${j.id}.png`), buf);
    console.log(`  baseline  ${j.id}`);
    continue;
  }
  const basePath = path.join(OUT_DIR, "baseline", `${j.id}.png`);
  if (!fs.existsSync(basePath)) {
    console.log(`  ✗ ${j.id}  (no hay baseline: correr npm run test:visual:baseline)`);
    failed++;
    continue;
  }
  const base = fs.readFileSync(basePath);
  let r = compare(base, buf);
  for (let k = 1; k < RETRIES && r.diff !== 0; k++) {
    buf = await capture(browser, j.page, j.w, j.h, j.full);
    r = compare(base, buf);
  }
  fs.writeFileSync(path.join(dir, `${j.id}.png`), buf);
  if (r.diff === 0) {
    console.log(`  ✓ ${j.id}`);
  } else if (r.noise) {
    noisy++;
    fs.mkdirSync(path.join(OUT_DIR, "diff"), { recursive: true });
    fs.writeFileSync(path.join(OUT_DIR, "diff", `${j.id}.png`), r.png);
    console.log(`  ≈ ${j.id}  ${r.diff} píxeles sueltos en toda la página (ruido de fuentes, no bloquea)`);
  } else {
    failed++;
    if (r.diff === -1) console.log(`  ✗ ${j.id}  cambió el tamaño de la página: ${r.size}`);
    else {
      fs.mkdirSync(path.join(OUT_DIR, "diff"), { recursive: true });
      fs.writeFileSync(path.join(OUT_DIR, "diff", `${j.id}.png`), r.png);
      console.log(`  ✗ ${j.id}  ${r.diff} píxeles distintos → tests/visual/output/diff/${j.id}.png`);
    }
  }
}
await browser.close();
server.close();

if (MODE === "baseline") console.log(`\nBaseline generada: ${jobs.length} capturas.`);
else {
  console.log(`\n${jobs.length - failed - noisy}/${jobs.length} capturas idénticas` + (noisy ? ` · ${noisy} con ruido de fuentes (no bloquea)` : "") + (failed ? ` · ${failed} CON CAMBIOS` : "") + ".");
  process.exit(failed ? 1 : 0);
}
