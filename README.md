# Diforza — sitio y landings

Sitio estático generado con **[11ty (Eleventy)](https://www.11ty.dev/)**. El HTML final es el mismo de siempre (sin frameworks en el navegador); 11ty solo arma las páginas a partir de piezas compartidas.

## Cómo trabajar

```bash
npm install      # una sola vez (o cuando cambie package.json)
npm start        # servidor local con recarga en vivo → http://localhost:8080
npm run build    # genera _site/ (lo que se publica)
```

> No uses Live Server para este proyecto: mostraría los archivos fuente, no el sitio armado.

## Estructura

```
src/
├─ _data/site.json            ← datos globales: WhatsApp, teléfono, GTM, menú, footer, redes
├─ _includes/
│  ├─ layouts/base.njk        ← esqueleto de TODAS las páginas (<head>, header, footer, scripts)
│  └─ partials/               ← header, footer, botón flotante de WhatsApp, fuentes, íconos
├─ assets/
│  ├─ css/base.css            ← estilos compartidos (home + todas las landings)
│  ├─ css/l2.css, l3.css      ← estilos propios de cada landing
│  └─ js/main.js, l2.js, l3.js
├─ img/                       ← imágenes compartidas
├─ index.njk                  ← home  →  /
├─ indumentaria-de-trabajo/   ← L2    →  /indumentaria-de-trabajo/
│  ├─ index.njk
│  └─ img/                    ← imágenes propias de la landing
└─ epp-proteccion-industrial/ ← L3    →  /epp-proteccion-industrial/
_dev/                         ← material de trabajo (PSD, originales, notas, versiones viejas). NO se publica.
_site/                        ← salida del build. NO se edita ni se sube a git.
```

## Reglas

- **Header, footer y WhatsApp se editan en un solo lugar** (`src/_includes/partials/` y `src/_data/site.json`). Nunca copiar ese HTML dentro de una página.
- **Número de WhatsApp:** `src/_data/site.json` → `whatsapp.number`. Lo usan los links, el botón flotante y el JS de "Consultar producto".
- **Nueva landing:** crear `src/<slug>/index.njk` con el front matter (`layout`, `title`, `description`, `pageCss`, `pageJs`, `waText`), su CSS en `src/assets/css/` y sus imágenes en `src/<slug>/img/`. Sumarla al footer en `site.json`.
- Rutas de imágenes y assets siempre **absolutas** (`/img/...`, `/<slug>/img/...`, `/assets/...`).
- Breakpoints y tokens: ver `_dev/notas/resumen_sesion_breakpoints_v2.md` antes de tocar media queries.
- Lo que no va al sitio (PSD, originales, scripts, notas) va en `_dev/`.

## Publicación (Cloudflare Pages)

- Build command: `npm run build`
- Output directory: `_site`
- Versión de Node: la toma de `.nvmrc` (22).
