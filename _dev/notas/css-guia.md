# Guía de CSS — Diforza

Guía práctica para tocar el CSS del sitio sin romper el sistema. El plan completo y las decisiones están en `_dev/prompts/refactor-css.md`; esto es el "cómo se hace" del día a día.

---

## 1. Cómo está armado

- **Un solo archivo de entrada:** `src/assets/css/main.css`. Solo tiene `@import`. Lightning CSS lo compila a un único `main.css` minificado que usan todas las páginas.
- **Capas (`@layer`)**, de menor a mayor prioridad:

  | Capa | Carpeta | Qué va |
  |---|---|---|
  | `tokens` | `settings/tokens.css` | Variables: colores, tipografía, radios, capas, layout |
  | `base` | `base/global.css` | Reset y estilos de etiquetas (`body`, `img`, `a`…) |
  | `components` | `components/` | Piezas reutilizables: botón, badge, formulario, tarjeta de producto, reseña… |
  | `layout` | `layout/` | Header y footer (van después de components porque ajustan botones adentro) |
  | `sections` | `sections/` | Secciones de página. Compartidas en la raíz (`hero`, `solve`, `benefits`, `faq`), propias en `home/` y `landing/` |
  | `utilities` | `utilities.css` | Lista cerrada (hoy solo `.hp-field`, el campo trampa anti-spam del formulario) |

  Una capa posterior gana siempre, sin importar la especificidad. Por eso casi nunca hace falta subir especificidad ni usar `!important`.
- **Breakpoints con nombre** en `settings/media.css`. Mobile-first: la regla sin media query es la de mobile; se sube con `min-width`.

  | Nombre | Desde | Para |
  |---|---|---|
  | `--sm` | 480px | phones grandes (ajustes menores) |
  | `--md` | 768px | tablet: arrancan layouts de 2+ columnas |
  | `--lg` | 1024px | notebook 13–14" |
  | `--xl` | 1280px | notebook 15–16" / desktop chico |
  | `--2xl` | 1440px | desktop: el shell llega a su máximo |
  | `--3xl` | 1700px | desktop grande: solo escala tipográfica |

  Excepciones (usar solo para lo que dice el comentario de cada una): `--xs-only`, `--below-sm`, `--below-md`, `--below-lg`, `--lg-only`, `--lg-to-2xl`, `--short-screen`. Nunca escribir `@media (min-width: 900px)` a mano.

---

## 2. Tokens: qué usar

Todo valor de diseño sale de `settings/tokens.css`. **El linter da error** si escribís un color HEX/`rgb()` literal, un `font-size` en px o un `z-index` numérico fuera de ese archivo.

**Colores — en componentes nuevos, usar los semánticos:**

| Token | Uso |
|---|---|
| `--color-primary` | Fondo del CTA principal (naranja accesible `#C2561A`, blanco encima 4,5:1) |
| `--color-on-primary` | Texto sobre el CTA principal (blanco) |
| `--color-accent` | Naranja de marca `#FF7E34`: bordes, íconos, líneas, subrayados. **No para texto sobre blanco ni de fondo con texto blanco** (no llega al contraste mínimo) |
| `--color-text` | Texto principal (azul `#003568`) |
| `--color-whatsapp` | Verde de WhatsApp |
| `--color-error` / `--color-success` | Estados del formulario |

Los primitivos (`--slate-50…900`, `--orange-*`, `--navy-950`, `--neutral-*`, `--green-*`) existen con los valores exactos del diseño. Usarlos solo si ningún semántico describe el caso.

**Transparencias:** canales `--rgb-*` → `rgb(var(--rgb-navy) / 12%)`, `rgb(var(--rgb-white) / 80%)`.

**Tipografía:**
- Familias: `--font-display` (Poppins, títulos), `--font-display-alt`, `--font-body` (Montserrat).
- Pesos: `--fw-light` (300) · `--fw-regular` (400) · `--fw-medium` (500) · `--fw-semibold` (600) · `--fw-bold` (700) · `--fw-black` (800).
- Tamaños: `--fs-<px>` (`--fs-13`, `--fs-12-5`…). Es la escala exacta en uso, congelada. Antes de crear uno nuevo, usar el más cercano existente.

**Forma y capas:**
- Radios: `--radius-2/4/10/12/14/16/18/24`, `--radius-pill`, `--radius-round`.
- z-index: `--z-below`, `--z-base`, `--z-layer-1…5` (capas locales dentro de una sección), `--z-header`, `--z-over-header`, `--z-float` (WhatsApp), `--z-dev`.

**Layout:** `--shell` (ancho máximo 1440), `--gutter`, `--pad`, `--nav-h`. Ver `_dev/notas/resumen_sesion_breakpoints_v2.md` antes de tocarlos.

**Qué NO está tokenizado (a propósito):** espaciados (`padding`, `margin`, `gap`), tamaños de caja, `line-height` y sombras quedan en px en cada componente. Son valores propios de cada pieza; tokenizarlos tendría sentido recién en un rediseño que consolide la escala.

---

## 3. Nombres (BEM en inglés)

- `.block`, `.block__element`, `.block--modifier`. Nunca `.block__a__b`.
- Bloques por **función**, no por página ni versión (nada de `-v2`, `-l2`).
- Estados con prefijo: `is-open`, `is-active`, `is-stuck`, `is-invalid`, `is-placeholder`.
- **JS engancha por `data-js="…"`** o por `id`, nunca por una clase de estilo. Excepciones aceptadas: `.reveal` y `.field`.
- Comentarios en español; clases y tokens en inglés.

---

## 4. Recetas

### Cambiar un color de marca
Cambiar el valor del token en `tokens.css`. Ejemplo: el CTA principal es una sola línea (`--color-primary`). No buscar y reemplazar HEX en los componentes.

### Crear un componente nuevo
1. Archivo en `components/<nombre>.css` con encabezado (qué es, dónde se usa, si lo usa el JS).
2. Importarlo en `main.css` dentro del bloque `components` con `layer(components)`.
3. Escribir mobile primero; sumar `@media (--md)`, `(--lg)`… al final del bloque, en orden ascendente.
4. Solo tokens para color, tipografía, radios y z-index.
5. `npm run lint:css` sin errores.

### Crear una sección nueva
Igual que un componente, en `sections/` (o `sections/home/`, `sections/landing/` si es propia de un tipo de página) con `layer(sections)`. Si la sección se usa en las landings, su HTML va como parcial en `src/_includes/sections/landing/` y el contenido en el JSON de cada landing.

### Crear una landing nueva
No requiere CSS. Ver el README (sección Reglas): un JSON en `src/_data/landings/`, un `index.njk` con `landingKey` y las fotos. Lo único que puede necesitar es un modificador de hero (`hero--<slug>`) si la foto pide otro encuadre.

### Variante de un componente
Modificador (`.btn--outline`, `.trust--grouped`). No duplicar el componente ni pisarlo desde la sección con selectores largos.

---

## 5. Antes de hacer commit

```bash
npm run lint:css              # 0 errores
npm run test:visual           # sin "✗" (los "≈" son ruido de fuentes y no bloquean)
```

- **Cambio que no debería verse** (refactor, limpieza): el test visual tiene que dar todo idéntico.
- **Cambio visual buscado:** revisar las capturas en `tests/visual/output/diff/`, confirmar que solo cambió lo esperado y regenerar la referencia con `npm run test:visual:baseline`.

---

## 6. Accesibilidad: reglas mínimas

- Texto normal ≥ 4,5:1 contra su fondo; texto grande (≥ 24px, o ≥ 18,7px en negrita) ≥ 3:1.
- El naranja `#FF7E34` no cumple sobre blanco ni con blanco encima: para fondos de botón usar `--color-primary`.
- Áreas clicables de al menos 24×24px (ideal 44×44px en mobile).
- No sacar el foco visible (`outline: none`) sin dar un reemplazo.

Hallazgos pendientes de decisión: ver "Informe de accesibilidad" en el registro de la fase D (`_dev/prompts/refactor-css.md`).
