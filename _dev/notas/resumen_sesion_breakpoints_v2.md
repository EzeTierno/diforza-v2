---
name: resumen-sesion-breakpoints-v2
description: Sistema de breakpoints y contenedor unificado de diforza-v2 (17/09/2026) — tokens --gutter/--shell/--pad, zona segura del hero bajo el navbar (--nav-h) y alto mínimo fijo. Leer ANTES de tocar cualquier media query.
type: project
---

# Sistema responsive de diforza-v2 (17/09/2026)

Archivo único: `diforza-v2/index.html`. Backup previo al refactor: `index.backup-prebp.html`.

## Breakpoints canónicos (usar SOLO estos)

| Rango | Uso |
|---|---|
| `<768` | mobile |
| `≥768` | tablet |
| `≥1024` | notebook 13-14" |
| `≥1280` | notebook 15-16" / desktop chico |
| `≥1440` | desktop |
| `≥1700` | desktop grande (solo escala tipográfica) |

Se eliminaron los breakpoints huérfanos: **900 → 1024** (15 reglas) y **1600 → 1440** (3 reglas).
Se conservan como excepciones justificadas: `max-height:820px` (solo compacta el header en
notebooks bajas) y `1024–1439px` (ancho de la copy del hero + compactado de CTAs para que
no invadan al operario).

## Contenedor y margen de seguridad

En `:root`:

- `--gutter` — margen lateral de seguridad: 20 / 24 (≥480) / 40 / 48 / 56 / 64px.
- `--shell: 1440px` — ancho máximo del contenido.
- `--pad: max(var(--gutter), calc((100% - var(--shell)) / 2 + var(--gutter)))`

Cualquier sector a ancho completo usa `padding: X var(--pad)` y queda alineado con todos los
demás automáticamente: por debajo de 1440 el `max()` devuelve el gutter, y por encima suma el
centrado del shell. Se usa `100%` y no `100vw` a propósito (`100vw` incluye el scrollbar y
generaba desborde horizontal en Windows).

Migrados a `var(--pad)` (antes tenían px hardcodeados por sector, que era la causa de que cada
sector arrancara en una X distinta): `.header`, `.hero-v2__inner`, `.solve-v2__inner`,
`.products-v2__top`, `.products-v2__carousel`, `.faq`. Los demás ya lo usaban.

## Hero: nunca detrás del navbar

- El JS publica el alto real del header como `--nav-h` (en `setNavH`, recalculado en `resize`,
  `load` y `document.fonts.ready`).
- `.hero-v2__inner { padding-top: calc(var(--nav-h) + var(--hero-gap)) }` → el aire bajo el
  navbar está garantizado en cualquier altura de pantalla. `--hero-gap`: 24/32/36/40px.
- `.hero-v2 { min-height: max(var(--hero-min), min(100svh, 900px)) }` — alto mínimo fijo
  (560/620/640/660px). Si la pantalla es más baja, **la página scrollea**; el hero ya no se
  comprime ni se escala.
- Se **eliminaron** los bloques `max-height:820px` / `max-height:700px` que achicaban tipografía
  del hero: ya no hacen falta y eran la fuente de las inconsistencias entre notebooks.
- `100svh` (no `100vh`) para que la barra de direcciones del navegador móvil no altere el cálculo.

## Verificación (Playwright, `reducedMotion:'reduce'`)

Anchos/alturas medidos: 375×667, 430×932, 768×1024, 1024×600, 1280×720, 1366×768, 1440×900,
1536×864, 1920×1080, 1280×500.

En todos: **overflow horizontal 0**, **gap nav→hero ≥ 24px** (nunca negativo) y el borde
izquierdo del contenido de los 8 sectores (hero, solve, productos, diferenciales, protect,
fábrica, destacado, footer) **idéntico — spread 0px**.

En 1366×768 el hero entra completo sin scroll (768px exactos).

## Ajuste posterior: mobile chico (<=374px)

Bloque `@media(max-width:374px)` al final del `<style>` — unico lugar donde:

- `.hero-v2__copy h1` baja a **32px**;
- `.hero-v2__lead` pasa a `max-width:100%` (los benefits siguen al 66%, para no cruzarse
  con el operario);
- el CTA del navbar dice **"Cotizar"** en vez de "Pedir cotizacion".

Para eso el `<a class="btn--nav header__cta">` lleva dos labels:
`<span class="btn--nav__long">` (visible por defecto) y `<span class="btn--nav__short">`
(`display:none` en la regla base, `inline` solo en <=374px). Si se cambia el copy del boton,
**hay que cambiarlo en los dos spans**.

Verificado en 320x568: sin overflow horizontal, gap nav->hero 24px, H1 32px, CTA "COTIZAR".
