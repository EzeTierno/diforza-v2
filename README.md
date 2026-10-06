# Diforza — sitio y landings

Sitio estático generado con **[11ty (Eleventy)](https://www.11ty.dev/)**. El HTML final es el mismo de siempre (sin frameworks en el navegador); 11ty solo arma las páginas a partir de piezas compartidas.

## Cómo trabajar

```bash
npm install                 # una sola vez (o cuando cambie package.json)
npx playwright install chromium   # una sola vez: navegador para el test visual
npm start                   # servidor local con recarga en vivo → http://localhost:8080
npm run build               # genera _site/ (lo que se publica, CSS minificado)
npm run lint:css            # revisa las convenciones del CSS (Stylelint)
npm run format              # formatea el CSS (Prettier)
npm run test:visual:baseline  # captura el sitio actual como referencia (antes de un cambio)
npm run test:visual           # compara contra la referencia: 0 píxeles distintos = OK
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
│  ├─ css/main.css            ← punto de entrada único (Lightning CSS → un solo main.css minificado)
│  ├─ css/settings/           ← tokens (variables) y breakpoints con nombre: @media (--lg)
│  ├─ css/base/               ← reset y estilos globales
│  ├─ css/components/         ← piezas reutilizables: botón, badge, formulario, tarjeta de producto…
│  ├─ css/layout/             ← header y footer
│  ├─ css/sections/           ← secciones: compartidas (hero, solve, benefits, faq), home/ y landing/
│  ├─ css/utilities.css       ← utilidades (lista cerrada)
│  └─ js/main.js, landing.js  ← main.js en todas; landing.js en las páginas de categoría
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
- **Nueva landing:** crear `src/<slug>/index.njk` con el front matter (`layout`, `title`, `description`, `pageJs: /assets/js/landing.js`, `waText`, `catalogName`) usando las clases de las secciones de landing, y sus imágenes en `src/<slug>/img/`. Las diferencias de diseño van como modificador (ej. `hero--<slug>` para el encuadre de la foto). Sumarla al footer en `site.json`.
- Rutas de imágenes y assets siempre **absolutas** (`/img/...`, `/<slug>/img/...`, `/assets/...`).
- **CSS:** convenciones en `_dev/prompts/refactor-css.md` (BEM en inglés, tokens, capas, breakpoints con nombre). El JS engancha por `data-js="…"`, no por clases de estilo (excepciones: `.reveal`, `.field`). Regla dura: cero cambio visual (verificar con `npm run test:visual`). Breakpoints: usar los nombres de `src/assets/css/settings/media.css`.
- Lo que no va al sitio (PSD, originales, scripts, notas) va en `_dev/`.

## Publicación (Cloudflare Pages)

- Build command: `npm run build`
- Output directory: `_site`
- Versión de Node: la toma de `.nvmrc` (22).
