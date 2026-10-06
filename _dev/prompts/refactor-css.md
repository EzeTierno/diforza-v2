# Prompt — Refactor completo del CSS · sitio Diforza (diforza-v2)

> Prompt de ejecución para un agente (Claude) o un dev. Se ejecuta por fases; cada fase termina con verificación y un commit propio en la rama de trabajo.
> Redactado el 6 oct 2026 a partir del inventario real del CSS actual. **Las decisiones marcadas con ✅ son los defaults recomendados; si alguna cambia, editar este doc antes de ejecutar.**

---

## 1. Rol y objetivo

Actuás como **front-end senior especializado en CSS de sitios estáticos de marketing**. Tu tarea es refactorizar todo el CSS del sitio Diforza (11ty, HTML estático, sin frameworks en el cliente) para que:

1. **Escale:** una landing nueva se arma reutilizando componentes, sin escribir CSS nuevo (o con un override mínimo).
2. **Sea consistente:** todo valor de diseño (color, tipografía, espaciado, radio, sombra, z-index, tiempos) sale de **tokens**.
3. **Sea mantenible por dos personas:** convenciones explícitas, un componente por archivo, linter que las haga cumplir.
4. **No rompa nada:** la apariencia actual (aprobada por el cliente) se preserva; cualquier cambio visual es intencional, se lista y se aprueba.

---

## 2. Contexto del proyecto

- Repo: `diforza-v2` (GitHub `EzeTierno/diforza-v2`). Rama de trabajo: `optimizacion-landings`. Leer primero `README.md` y `_dev/notas/resumen_sesion_breakpoints_v2.md`.
- Stack: **11ty v3**, fuente en `src/`, salida `_site/` (lo que publica Cloudflare Pages). Node 22.
- Páginas: home `/` (`src/index.njk`), L2 `/indumentaria-de-trabajo/`, L3 `/epp-proteccion-industrial/`. Vienen L4 (lluvia/intemperie) y L5 (calzado + guantes), y a futuro el catálogo completo.
- Layout: `src/_includes/layouts/base.njk` + parciales (`header`, `footer`, `wa-float`…). Datos globales en `src/_data/site.json`.
- JS: `src/assets/js/main.js` (compartido) + `l2.js` / `l3.js`. Algunos scripts seleccionan por clase (`.hero-v2`, etc.).
- Docs de referencia (carpeta `02_sitio-web/` del proyecto, fuera del repo): **doc 15** (sistema de diseño de marca), **doc 17** (convenciones de código). **Donde este prompt difiera de los docs 15/17, manda este prompt** (el sitio construido y aprobado evolucionó respecto de esos docs; ver §3).

### 2.1 Estado actual del CSS (inventario al 6 oct 2026)

| Archivo | Líneas | Peso | Carga | Contenido |
|---|---|---|---|---|
| `src/assets/css/base.css` | 951 | 52 KB | todas | variables, reset, header, botones, footer, animaciones **+ las 8 secciones de la home** + FAQ |
| `src/assets/css/l2.css` | 423 | 26 KB | L2 | landing indumentaria (clases `*-l2`) |
| `src/assets/css/l3.css` | 484 | 30 KB | L3 | landing EPP (clases `*-l3`) |

Problemas medidos:

- **Duplicación L2/L3:** normalizando sufijos, ~223 reglas idénticas (55–60 % de cada archivo). Es la misma plantilla con distinto nombre de clase.
- **Valores sueltos:** 37 colores HEX distintos, 64 variantes `rgba()`, **43 tamaños de fuente** distintos (incluye 9.5 px, 12.5 px, 13.5 px…), 37 `line-height`, 16 `letter-spacing`, 21 `box-shadow`, 10 `border-radius`, 11 `z-index`. Solo existen 3 variables de color (`--navy`, `--orange`, `--gray`). 0 usos de `clamp()`.
- **Media queries:** 330 bloques; `min-width:1280px` aparece 173 veces (una por regla, no agrupadas). Hay 6 `max-width` y rangos puntuales.
- **Nombres con versión/página:** `hero-v2`, `dif-v2`, `pcard-l2`, `trust-l3`… (el sufijo no describe función).
- **Mezcla de responsabilidades:** las landings descargan el CSS de las 8 secciones de la home.
- 6 `!important` (honeypot y un override en `trust-l3`).
- Comentarios desactualizados (referencias a `preview_html`, `/fonts`, "v1").
- **Accesibilidad:** el CTA principal `.btn--solid` es naranja `#FF7E34` con texto blanco → **contraste 2.53:1** (AA pide 4.5:1 para texto de ese tamaño).

---

## 3. Decisiones (defaults recomendados)

| # | Tema | Decisión | Motivo |
|---|---|---|---|
| D1 | Tipografías | ✅ **CONFIRMADO (6 oct):** Poppins (titulares) + Montserrat (cuerpo/UI), como está construido. Doc 15 proponía Montserrat + Source Sans 3. | Es lo que el cliente vio y aprobó. Cambiarlo es rediseño, no refactor. Queda en tokens: cambiar familia = 1 línea. |
| D2 | Contenedor | ✅ **CONFIRMADO:** **`--shell: 1440px`** con `--gutter` fluido y `--pad` (sistema actual). Doc 17 decía 1200 px. | Sistema ya probado en 10 resoluciones con alineación 0 px entre secciones. |
| D3 | Breakpoints | ✅ `480 / 768 / 1024 / 1280 / 1440 / 1700` (ver §6), con nombre. Se conservan los existentes (D4). | Son los canónicos del proyecto. |
| D4 | Paridad visual | ✅ **CONFIRMADO — REGLA DURA: las 3 páginas quedan visualmente IDÉNTICAS a las del 6 oct 2026 en TODOS los anchos y en TODAS las fases.** Única excepción aprobada: el tono del CTA naranja (D5). No se consolidan valores parecidos ni se pasa a tipografía fluida: los tokens guardan los valores exactos actuales. | Pedido explícito del usuario. La consolidación de la escala queda para un eventual rediseño. |
| D5 | Contraste del CTA | ✅ **CONFIRMADO** — Fase D: botón sólido **`--orange-700: #C2561A`** con texto blanco (4.53:1); el naranja `#FF7E34` queda como acento (bordes, íconos, líneas). Alternativa: azul `#003568` (12.3:1). Aprobado por el usuario el 6 oct. | Regla dura del doc 15 §3.2 y WCAG AA. |
| D6 | Idioma | ✅ **Clases y tokens en inglés**; comentarios en **español**. | Consistente con lo existente (`header`, `hero`, `btn`) y con el ecosistema. |
| D7 | Entrega de CSS | ✅ **Un solo bundle `main.css`** para todo el sitio (minificado, con hash en producción). CSS crítico inline: fase de performance, no ahora. | Hoy base+l2+l3 = 20 KB gzip sin minificar; unificado y sin duplicados debería quedar por debajo. Un request cacheado sirve a todas las páginas. |
| D8 | Herramienta de build | ✅ **Lightning CSS** integrado en 11ty (bundle de `@import`, `@custom-media`, nesting, prefijos, minificado). | Una sola dependencia en vez de la cadena PostCSS del doc 17; mismas capacidades. |

---

## 4. Principios no negociables

1. **No se toca contenido:** copy, imágenes, orden de secciones y comportamiento quedan igual. Este refactor es de estilos y de los nombres de clase en el HTML/JS que los acompañan.
2. **Mobile-first estricto:** la regla sin media query es mobile; se sube con `min-width`. `max-width` solo como excepción documentada (§6.3).
3. **Todo valor de diseño sale de un token.** En componentes no hay HEX, `rgba()` literal, px de tipografía ni números mágicos de z-index. Excepciones: `0`, `1px`/`2px` de bordes, `50%`, `100%`, porcentajes de layout, valores dentro de `tokens.css`.
4. **Sin `!important`**, salvo en las utilidades `.visually-hidden` y `.hp-field` (honeypot).
5. **Sin selectores por ID** ni `[style]`. **Especificidad máxima 0,2,0** salvo estados (`.block.is-open`, `.block:hover .block__el`). Anidamiento máximo 2 niveles.
6. **Comportamiento separado del estilo:** JS selecciona por `data-js="…"`, nunca por clase de estilo. Estados que pone el JS: `is-*` / `has-*`.
7. **Accesibilidad:** foco visible en todo interactivo (`:focus-visible`), área táctil ≥ 44×44 px, `prefers-reduced-motion` anula animaciones y transiciones, contraste AA.
8. **Cada fase se verifica antes de seguir** (§11) y queda en un commit separado.

---

## 5. Arquitectura de archivos y capas

```
src/assets/css/
├─ main.css                     ← único punto de entrada: declara @layer y hace @import en orden
├─ settings/
│  ├─ tokens.css                ← todas las custom properties (primitivos + semánticos + layout)
│  └─ media.css                 ← @custom-media (breakpoints con nombre)
├─ base/
│  ├─ reset.css                 ← reset moderno mínimo
│  ├─ fonts.css                 ← @font-face (hoy vacío: las fuentes van por Google Fonts; se completa en performance)
│  ├─ typography.css            ← body, h1–h6, p, a, listas, strong, small
│  └─ global.css                ← html/body, selección, scroll-behavior, imágenes responsive, :focus-visible global
├─ layout/
│  ├─ container.css             ← .container y patrón full-bleed con --pad
│  ├─ section.css               ← .section (padding vertical por token, variantes --dark, --muted)
│  ├─ header.css
│  └─ footer.css
├─ components/                  ← piezas reutilizables, un bloque BEM por archivo
│  ├─ button.css                ← .btn + --primary/--outline/--ghost/--whatsapp/--sm/--lg
│  ├─ eyebrow.css
│  ├─ section-heading.css       ← título + bajada de sección (reemplaza h2-l2/h2-l3)
│  ├─ product-card.css          ← reemplaza pcard-v2 / pcard-l2 / pcard-l3
│  ├─ carousel.css              ← carrusel con bordes difuminados / drag (home y landings)
│  ├─ marquee.css               ← carrusel infinito de logos
│  ├─ accordion.css             ← FAQ (details/summary)
│  ├─ form.css / field.css      ← formulario de cotización, campos, errores, honeypot
│  ├─ review-card.css           ← reseñas Google (gcard/greviews)
│  ├─ chip.css · check-list.css · step.css · badge.css
│  ├─ wa-float.css              ← botón flotante de WhatsApp
│  ├─ reveal.css                ← sistema de scroll-reveal y entrada del hero
│  └─ placeholder.css           ← marcas [VALIDAR]/[PENDIENTE] + botón ph-toggle (se elimina al lanzar)
├─ sections/                    ← composición propia de una sección (layout interno), usa componentes
│  ├─ hero.css                  ← compartido home + landings, variantes por modificador
│  ├─ home/  brands.css · solve.css · featured.css · benefits.css · compliance.css · factory.css
│  └─ landing/ trust.css · category-lines.css · products.css · steps.css · guarantee.css · quote.css · catalog.css
└─ utilities.css                ← SOLO: .visually-hidden, .no-scroll, .text-center, .hp-field
```

`main.css`:

```css
@layer reset, tokens, base, layout, components, sections, utilities;

@import "settings/tokens.css" layer(tokens);
@import "settings/media.css";
@import "base/reset.css" layer(reset);
@import "base/fonts.css" layer(base);
/* … resto en el orden del árbol … */
@import "utilities.css" layer(utilities);
```

**Cascade layers** resuelven el orden por capa y no por especificidad: una utilidad gana siempre a un componente sin `!important`, y una sección puede ajustar un componente sin escalar selectores.

**Regla de ubicación:** si algo se usa en 2+ secciones o páginas → `components/`. Si es el layout interno de una sola sección → `sections/`. **No existen archivos por página** (`l2.css`, `home.css`): las diferencias entre landings se expresan con modificadores (§8.3).

---

## 6. Breakpoints

### 6.1 Escala

```css
/* settings/media.css */
@custom-media --sm  (min-width: 480px);   /* phones grandes: solo gutter/ajustes menores */
@custom-media --md  (min-width: 768px);   /* tablet: arrancan layouts de 2+ columnas */
@custom-media --lg  (min-width: 1024px);  /* notebook 13–14": layout desktop */
@custom-media --xl  (min-width: 1280px);  /* notebook 15–16" / desktop chico */
@custom-media --2xl (min-width: 1440px);  /* desktop: el shell llega a su máximo */
@custom-media --3xl (min-width: 1700px);  /* desktop grande: solo escala tipográfica (se conserva por D4) */

/* Excepciones documentadas (no usar fuera de estos casos) */
@custom-media --xs-only      (max-width: 374px);                         /* mobile chico: H1 y CTA corto del navbar */
@custom-media --below-md     (max-width: 767px);                         /* solo para ocultar/mostrar piezas puntuales */
@custom-media --lg-to-2xl    (min-width: 1024px) and (max-width: 1439px);/* copy del hero vs operario */
@custom-media --short-screen (min-width: 1024px) and (max-height: 820px);/* compactar header en notebooks bajas */
```

Uso: `@media (--lg) { … }`. Lightning CSS lo compila a px.

### 6.2 Reglas

- **Media queries junto al bloque**, inmediatamente después de sus reglas base, agrupadas por breakpoint (**un solo** `@media (--xl)` por bloque, no uno por regla).
- La tipografía sigue escalando por breakpoint (D4). Los 173 `@media(min-width:1280px)` se reducen agrupándolos por bloque, no eliminándolos. **El breakpoint 1700 se conserva** (`--3xl`) mientras haya reglas que lo usen.
- Por encima de 1440 no hay layout nuevo: el contenido queda centrado en el shell y crece el margen (`--pad`).
- Sin scroll horizontal en ningún ancho; usar `100%`, no `100vw` (el scrollbar de Windows genera desborde).

### 6.3 Anchos de verificación obligatorios

`320 · 375 · 390 · 430 · 768 · 1024 · 1280 · 1366 · 1440 · 1536 · 1920`, más alturas `1024×600`, `1280×720`, `1366×768`, `1280×500` para el hero.

---

## 7. Sistema de tokens (`settings/tokens.css`)

Dos niveles: **primitivos** (la paleta; no se usan directamente en componentes) y **semánticos** (el rol; es lo que usan los componentes). Así, cambiar el color de los títulos es cambiar un semántico, no buscar un HEX.

Los valores salen del inventario actual y son **exactos** (regla D4): cada valor distinto en uso tiene su token, aunque dos se parezcan. Los nombres numéricos (`--fs-15`, `--gray-d9`…) son intencionales: describen una escala congelada. **No se agregan valores nuevos** sin necesidad; si un rediseño futuro consolida la escala, se hace ahí. Las paletas de ejemplo de abajo se reemplazan por el set exacto generado en la fase C.

### 7.1 Color

```css
:root {
  /* Primitivos — marca */
  --navy-950: #011c37;
  --navy-900: #003568;   /* azul Diforza */
  --navy-800: #002a53;   /* hover del azul (doc 15) */
  --orange-500: #ff7e34; /* acento de marca */
  --orange-700: #c2561a; /* naranja accesible (texto/botón sobre blanco, 4.53:1) */
  --orange-300: #ffb68b;
  --orange-200: #ffd3b8;
  --orange-50:  #fff4ec;

  /* Primitivos — neutros (consolidar los ~20 grises actuales en esta escala) */
  --slate-50:  #f6f8fa;  --slate-100: #eef1f4;  --slate-200: #e4e8ec;
  --slate-300: #d7e0e8;  --slate-400: #9fb2c5;  --slate-500: #8a96a3;
  --slate-600: #6b7785;  --slate-700: #5a6b7c;  --slate-800: #4a5a6a;
  --slate-900: #3c4c5c;
  --white: #fff;  --black: #000;

  /* Primitivos — funcionales */
  --green-wa: #25d366;  --green-wa-700: #25a55f;  --green-500: #35c46f;
  --red-700: #c62828;

  /* Semánticos */
  --color-bg:            var(--white);
  --color-bg-muted:      var(--slate-50);
  --color-bg-dark:       var(--navy-900);
  --color-bg-darker:     var(--navy-950);
  --color-text:          var(--navy-900);
  --color-text-muted:    var(--slate-700);
  --color-text-subtle:   var(--slate-500);
  --color-text-inverse:  var(--white);
  --color-heading:       var(--navy-900);
  --color-border:        var(--slate-300);
  --color-accent:        var(--orange-500);
  --color-primary:       var(--orange-500);   /* fase D → var(--orange-700) si se aprueba D5 */
  --color-primary-hover: var(--orange-700);
  --color-on-primary:    var(--white);
  --color-whatsapp:      var(--green-wa);
  --color-error:         var(--red-700);
  --color-success:       var(--green-500);
  --color-focus:         var(--orange-500);

  /* Transparencias: overlays/velos con nombre (no rgba sueltos) */
  --overlay-dark:  rgb(0 26 52 / 25%);
  --veil-light:    rgb(255 255 255 / 55%);
  --line-on-dark:  rgb(255 255 255 / 14%);
  --text-on-dark-muted: rgb(255 255 255 / 75%);
}
```

Las 64 variantes `rgba()` actuales se reducen a un set con nombre (velos, líneas sobre oscuro, texto atenuado sobre oscuro, sombras). Para variaciones puntuales de opacidad se permite `color-mix(in srgb, var(--token) 40%, transparent)`.

### 7.2 Tipografía — familias y pesos

```css
--font-display: "Poppins", "Montserrat", Arial, sans-serif;  /* titulares (D1) */
--font-body:    "Montserrat", Arial, sans-serif;              /* cuerpo y UI */
--fw-light: 300; --fw-regular: 400; --fw-medium: 500;
--fw-semibold: 600; --fw-bold: 700; --fw-black: 800;
```

Fase C: auditar si se usan los 6 pesos de Montserrat (300–700) y los 3 de Poppins (600–800); cada corte es una descarga. Objetivo ≤ 5 cortes.

### 7.3 Tipografía — escala

> ⚠️ **Por D4 NO se usa `clamp()` ni tipografía fluida**: cambiaría los tamaños entre breakpoints. Se mantienen los saltos por breakpoint actuales, con tokens numéricos exactos (`--fs-9-5`, `--fs-12-5`, `--fs-15`, `--fs-44`…). Lo que sigue queda como referencia para un rediseño futuro, **no se aplica**.

Texto (fijo, en rem; colapsa los 43 tamaños actuales):

```css
--fs-2xs: 0.6875rem; /* 11 — labels, badges, placeholders */
--fs-xs:  0.75rem;   /* 12 — captions, meta */
--fs-sm:  0.8125rem; /* 13 — botones mobile, notas */
--fs-md:  0.875rem;  /* 14 — texto secundario */
--fs-base: 0.9375rem;/* 15 — cuerpo actual del sitio */
--fs-lg:  1.0625rem; /* 17 — bajadas, lead */
```

Titulares (fluidos con `clamp()`, entre 375 px y 1440 px de viewport):

```css
--fs-h4:      clamp(1.125rem, 1.05rem + 0.35vw, 1.375rem);  /* 18 → 22 */
--fs-h3:      clamp(1.25rem,  1.1rem + 0.6vw,   1.625rem);  /* 20 → 26 */
--fs-h2:      clamp(1.625rem, 1.2rem + 1.8vw,   2.75rem);   /* 26 → 44 */
--fs-h1:      clamp(2rem,     1.4rem + 2.6vw,   3.25rem);   /* 32 → 52 */
--fs-display: clamp(2.125rem, 1.3rem + 3.4vw,   3.875rem);  /* 34 → 62 (H1 del hero) */
```

> Los rangos exactos de cada `clamp()` se calibran en la fase C contra los tamaños actuales por breakpoint (tabla antes/después en el informe). En las fases A y B se mantienen los px existentes.

Interlineado y tracking:

```css
--lh-tight: 1.05;  --lh-snug: 1.15;  --lh-heading: 1.25;
--lh-body: 1.5;    --lh-relaxed: 1.6;
--ls-tight: -0.02em; --ls-normal: 0; --ls-wide: 0.04em;
--ls-wider: 0.08em;  --ls-widest: 0.16em;   /* eyebrows en mayúscula */
```

### 7.4 Espaciado (base 4 px)

```css
--space-1: 0.25rem;  /* 4 */   --space-2: 0.5rem;   /* 8 */
--space-3: 0.75rem;  /* 12 */  --space-4: 1rem;     /* 16 */
--space-5: 1.25rem;  /* 20 */  --space-6: 1.5rem;   /* 24 */
--space-8: 2rem;     /* 32 */  --space-10: 2.5rem;  /* 40 */
--space-12: 3rem;    /* 48 */  --space-16: 4rem;    /* 64 */
--space-20: 5rem;    /* 80 */  --space-24: 6rem;    /* 96 */
--space-32: 8rem;    /* 128 */

/* Por D4 no hay padding de sección fluido: cada sección conserva sus valores por breakpoint,
   expresados con los tokens de espaciado exactos (se agregan --space-* para cada valor en uso). */
```

### 7.5 Layout (se conserva el sistema actual)

```css
--gutter: 20px;   /* 24 (--sm) · 40 (--md) · 48 (--lg) · 56 (--xl) · 64 (--2xl) — se redefine en media queries de :root */
--shell: 1440px;
--pad: max(var(--gutter), calc((100% - var(--shell)) / 2 + var(--gutter)));
--nav-h: 78px;    /* lo sobrescribe el JS con el alto real */
--hero-gap: 24px; --hero-min: 560px;
--measure: 68ch;  /* ancho máximo de párrafo */
```

### 7.6 Forma, profundidad, capas y movimiento

```css
--radius-xs: 2px;  --radius-sm: 4px;  --radius-md: 10px;
--radius-lg: 16px; --radius-xl: 24px; --radius-pill: 999px; --radius-round: 50%;

--shadow-1: 0 2px 8px rgb(0 53 104 / 8%);    /* reposo de tarjeta */
--shadow-2: 0 12px 28px rgb(0 53 104 / 12%); /* hover de tarjeta */
--shadow-3: 0 24px 60px rgb(0 10 25 / 35%);  /* elementos flotantes grandes */
--shadow-accent: 0 8px 16px rgb(255 126 52 / 32%); /* glow del CTA naranja */
--ring-focus: 0 0 0 3px rgb(255 126 52 / 28%);

--z-below: -1; --z-base: 1; --z-raised: 5;
--z-header: 40; --z-overlay: 55; --z-float: 60;

--dur-fast: 150ms; --dur-base: 200ms; --dur-slow: 300ms; --dur-reveal: 500ms;
--ease-out: cubic-bezier(.2, .7, .2, 1); --ease: ease;
```

(Los 21 `box-shadow` actuales se mapean a estos 4 + ring; los 10 radios, a 7.)

---

## 8. Convenciones de nombres

### 8.1 BEM

- `.block`, `.block__element`, `.block--modifier`. Un elemento nunca encadena otro elemento (`.card__body__title` ✗ → `.card__title` ✓).
- **Bloques por función, no por versión ni página:** se eliminan los sufijos `-v2`, `-l2`, `-l3`.
- Estados: `is-open`, `is-active`, `is-stuck`, `is-scrolled`, `is-error`, `is-loading`, `has-js`.
- Contexto oscuro: modificador de sección (`.section--dark`), que redefine tokens semánticos localmente (`--color-text: var(--color-text-inverse)`) en vez de reescribir cada componente (reemplaza `.on-dark`).
- Hooks de JS: `data-js="nav-toggle"`, `data-js="consultar"`, `data-js="wa"`… (reemplazar `js-wa`, `#navToggle` en JS, etc.; los `id` se mantienen solo para anclas y `aria-controls`).

### 8.2 Tabla de renombres (a completar y entregar en la fase B)

| Actual | Nuevo | Tipo |
|---|---|---|
| `hero-v2`, `hero-v2--l2`, `hero-v2--l3` | `hero`, `hero--indumentaria`, `hero--epp` | sección |
| `brands-v2` | `brands` | sección home |
| `solve-v2`, `solve-v2--l2/l3` | `solve` (+ modificadores) | sección |
| `products-v2`, `prod-l2`, `prod-l3` | `products` | sección |
| `pcard-v2`, `pcard-l2`, `pcard-l3` | `product-card` | componente |
| `destacado-v2` | `featured` | sección home |
| `dif-v2` | `benefits` | sección |
| `protect-v2` | `compliance` | sección home |
| `factory-v2` | `factory` | sección home |
| `trust-l2/l3` | `trust` | sección landing |
| `line-l2/l3` | `category-lines` | sección landing |
| `steps-l2/l3` | `steps` | sección landing |
| `guarantee-l2/l3` | `guarantee` | sección landing |
| `cta-l2/l3`, `form-l2/l3`, `quote-l2/l3`, `quoting-l2/l3` | `quote` + `form` + `field` | sección + componentes |
| `catalog-l2/l3` | `catalog` | sección landing |
| `eyebrow-l2/l3` | `eyebrow` | componente |
| `h2-l2/l3` | `section-heading` | componente |
| `gcard`, `greviews`, `reviews-l2/l3` | `review-card`, `reviews` | componente/sección |
| `chips-l3`, `chip-l3` | `chips`, `chip` | componente |
| `faq`, `faq--l2/l3`, `accordion` | `faq` + `accordion` | sección + componente |
| `on-dark` | `section--dark` | modificador |
| `ph`, `ph-toggle`, `ph-off` | `placeholder`, `placeholder-toggle`, `is-placeholders-hidden` | dev |

### 8.3 Diferencias entre landings

1. Inventariar **cada** diferencia real entre las reglas de L2 y L3 (después de normalizar sufijos).
2. Si es de **contenido** (cantidad de columnas por cantidad de ítems, foto de fondo), resolverla con tokens locales o con el HTML, no con CSS duplicado.
3. Si es de **diseño** y se justifica, modificador: `.hero--epp`, `.trust--grouped`.
4. Una landing nueva no debería necesitar más que un modificador de hero (foto/encuadre). Si necesita más, documentar por qué.

---

## 9. Convenciones de escritura

- **Formato** (Prettier): una declaración por línea, 2 espacios, comillas dobles, `;` final, minúsculas, cero inicial (`0.5`), sin unidades en cero. El minificado lo hace el build; el fuente se escribe legible.
- **Orden de propiedades** (stylelint-order): 1) posición (`position`, `inset`, `z-index`) · 2) display y layout (`display`, `flex`, `grid`, `gap`, `place-*`) · 3) caja (`width`, `height`, `margin`, `padding`, `overflow`) · 4) tipografía (`font`, `line-height`, `letter-spacing`, `text-*`, `color`) · 5) visual (`background`, `border`, `border-radius`, `box-shadow`, `opacity`) · 6) animación (`transition`, `animation`) · 7) misc.
- **Orden dentro de un archivo:** bloque → elementos → modificadores → estados → media queries del bloque (en orden ascendente).
- **Unidades:** `rem` para tipografía y espaciado; `px` para bordes, hairlines, sombras y offsets finos; `%`, `fr`, `minmax()`, `clamp()` para layout; `svh`/`dvh` para altos de viewport; `ch` para medida de lectura.
- **Propiedades lógicas** (`margin-inline`, `padding-block`, `inset-inline-start`) en código nuevo/reescrito.
- **Color moderno:** `rgb(0 53 104 / 12%)` en tokens; nunca HEX/rgba en componentes.
- **Nesting nativo** permitido solo para pseudo-clases/estados y media queries del propio bloque (`&:hover`, `&.is-open`, `@media (--lg)`), máximo 2 niveles. No anidar elementos BEM (`&__title` ✗: no es buscable).
- **Comentarios:** encabezado por archivo (qué es, dónde se usa, dependencias) y comentarios solo para el *por qué* de algo no obvio (ej.: "100% y no 100vw: el scrollbar de Windows desborda"). Formato:

```css
/* ==========================================================================
   Product card — tarjeta de producto (home, L2, L3)
   Usa: --shadow-1/2, --radius-lg. JS: data-js="consultar" en el botón.
   ========================================================================== */
```

- Eliminar comentarios obsoletos, código comentado y reglas muertas (verificadas con la cobertura de Chrome sobre las 3 páginas y todos los anchos).

---

## 10. Build (11ty + Lightning CSS)

- Dependencias: `lightningcss`, `browserslist` (y `@11ty/eleventy` ya instalado).
- `src/assets/css/main.css` se compila a `_site/assets/css/main.css`. Los parciales de CSS **no** se copian como passthrough.
- Configuración: `bundle` (resuelve `@import`), `drafts.customMedia: true`, nesting, `targets` desde `.browserslistrc` = `"> 0.5% in AR, last 2 versions, iOS >= 15, not dead"`.
- Desarrollo (`npm start`): sin minificar + sourcemap. Producción (`npm run build`): minificado y con hash en el nombre (`main.[hash].css`), referenciado desde `base.njk`.
- El layout carga **un solo** `<link rel="stylesheet" href="…/main.css">`; se eliminan `pageCss` del front matter.
- Fuentes: fuera de alcance (fase de performance). `base/fonts.css` queda preparado y el `<link>` a Google Fonts sigue en `partials/fonts.njk`.

---

## 11. Calidad y verificación

### 11.1 Regresión visual automatizada (se construye en la fase A)

- Script en el repo: `npm run test:visual` (Playwright + `pixelmatch`, carpeta `tests/visual/`).
- **Baseline:** capturas full-page del estado actual (antes de tocar nada) de las 3 páginas × anchos de §6.3, con `reducedMotion: 'reduce'`, animaciones y transiciones desactivadas, y scroll hasta el final para disparar los reveals antes de capturar.
- **Comparación:** tras cada fase: **0 píxeles distintos** en todas (tolerancia solo de antialiasing). Fase D: el único diff permitido es el del CTA naranja, verificado por zona.
- Las baselines van a `tests/visual/baseline/` (en git); los resultados, a `tests/visual/output/` (en `.gitignore`).

### 11.2 Lint

`npm run lint:css` con **Stylelint** (`stylelint-config-standard` + `stylelint-order`):

- `color-no-hex: true` y `function-disallowed-list: ["rgba", "rgb", "hsl"]` en todo menos `settings/tokens.css`.
- `declaration-property-value-disallowed-list`: px en `font-size`, `line-height`, `margin*`, `padding*`, `gap`; números literales en `z-index`.
- `declaration-no-important: true` (excepto `utilities.css`).
- `selector-max-id: 0`, `selector-max-specificity: "0,3,0"`, `max-nesting-depth: 2`, `selector-class-pattern` (BEM en minúsculas con guiones).
- `media-feature-name-no-unknown` + permitir solo los `@custom-media` de §6.
- `npm run format` con Prettier.

### 11.3 Funcional y accesibilidad (cada fase)

- 0 errores de consola; 0 recursos 404; sin scroll horizontal en ningún ancho.
- Header: transparente → sólido al scrollear; menú mobile abre/cierra; cruce del operario sobre el navbar.
- Carruseles (drag y marquee), acordeón FAQ, reveals, botón "Consultar producto" → formulario + WhatsApp con el producto precargado, botón flotante de WhatsApp.
- Foco visible al navegar con Tab; `prefers-reduced-motion` desactiva las animaciones.
- Contraste AA de texto sobre fondos (informe con los pares que fallan).

---

## 12. Fases y entregables

| Fase | Qué se hace | Cambio visual | Entregable |
|---|---|---|---|
| **A · Infraestructura** | Baseline visual + script de test · Lightning CSS en 11ty · `main.css` con `@layer` · `tokens.css` con los **valores exactos actuales** · `media.css` · Stylelint/Prettier configurados (aún en modo aviso) | Ninguno | Commit "CSS fase A" + test en verde |
| **B · Arquitectura y nombres** | Partir el CSS en el árbol de §5 · renombrar clases (tabla §8.2) en CSS, `.njk` y JS · JS a `data-js` · unificar L2/L3 en componentes/secciones compartidas · media queries agrupadas por bloque · borrar CSS muerto y comentarios obsoletos | Ninguno | Commit "CSS fase B" + tabla de renombres + test en verde |
| **C · Tokens** | Reemplazar todos los valores sueltos por tokens **exactos** (sin consolidar) · Stylelint en modo error | **Ninguno** | Commit "CSS fase C" + tabla de tokens + test en verde |
| **D · Accesibilidad** | CTA naranja → `#C2561A` (D5, aprobado) · informe de contraste, foco y áreas táctiles (lo que implique cambio visual se reporta, no se aplica sin OK) | Solo el CTA | Commit "CSS fase D" + informe |
| **E · Documentación** | `_dev/notas/css-guia.md` (cómo crear un componente / una landing, tokens disponibles, breakpoints) · actualizar `README.md` y `MEMORY.md` | — | Commit "CSS fase E" |

**Plantilla de landing (recomendado, misma pasada que la fase B):** como en la fase B se reescribe el HTML de L2/L3 con clases unificadas, extraer las secciones de landing a parciales (`src/_includes/sections/landing/*.njk`) alimentados por datos de cada página (front matter o `src/_data/landings/*.json`: productos, líneas, FAQ, textos). Resultado: L4 y L5 = un archivo de datos + fotos.

---

## 13. Fuera de alcance

Tracking (GTM/GA4/Meta), SEO, optimización de imágenes, fuentes autoalojadas y CSS crítico (fase de performance), cambios de copy y contenidos `[VALIDAR]`, rediseño visual.

---

## 14. Criterios de aceptación (checklist final)

- [ ] Un solo `main.css` en producción, minificado y con hash; ningún `pageCss`.
- [ ] Ninguna clase con `-v2`, `-l2`, `-l3`; ningún archivo CSS por página.
- [ ] `npm run lint:css` en verde en modo error (0 HEX/rgba fuera de tokens, 0 px de tipografía/espaciado, 0 `!important` fuera de utilidades, 0 IDs).
- [ ] `npm run test:visual`: 0 diff en A, B y C; en D solo el CTA naranja.
- [ ] Media queries solo con los nombres de `media.css`; tipografía idéntica a la actual.
- [ ] JS sin selectores por clase de estilo (solo `data-js` / ids de ancla).
- [ ] Sin errores de consola, sin 404, sin overflow horizontal en los 11 anchos.
- [ ] CTA naranja en `#C2561A`; informe de contraste del resto entregado.
- [ ] Guía `_dev/notas/css-guia.md` + README y MEMORY actualizados.
- [ ] Peso del bundle completo (gzip) ≤ 20 KB, que es lo que pesan hoy base + l2 + l3 juntos sin minificar (hoy cada landing descarga ~18–19 KB gzip).
