---
name: resumen-sesion-mobile-v2
description: Sesión 17/09/2026 — feedback del cliente sobre diforza-v2, ajustes mobile del hero/solve/productos/destacado, H1 de 3 líneas en desktop, carrusel de logos y espaciado FAQ→footer.
type: project
---

# Sesión 17/09/2026 — Ajustes de feedback en diforza-v2

Archivo único de trabajo: `diforza-v2/index.html`. Todo se edita ahí (CSS inline en el `<style>`).

## Dónde vive cada cosa

- **Un solo bloque `@media(max-width:767px)` al final del `<style>`** concentra TODO el mobile
  (hero, solve, productos, destacado). Va al final a propósito, para ganarle a las reglas
  base y a los overrides de notebooks (`min-width:1024px and max-height:820px`).
- Los overrides de notebooks siguen más arriba y no chocan (son `min-width`).

## Cambios de esta sesión

### Copy
- "+20 años" → **"+15 años"** en los tres lugares: hero, sector diferenciales, sector fábrica.

### Hero
- Desktop: H1 en **3 líneas** (`Indumentaria y / seguridad para los / que hacen industria`),
  todo del mismo cuerpo, con el naranja arrancando a mitad del segundo renglón.
- Mobile: H1 en **4 líneas**, con "Indumentaria y seguridad" a `1.15em`.
- Navbar mobile: logo 46px, `.btn--nav` 9.5px sin flecha.
- Operario visible en mobile (`width:84vw; right:-22vw; bottom:0`), con `pointer-events:none`.
- Columna de texto al 66%; CTAs apilados a 11px/padding 11-20 con `z-index:5`.
- `.hero-v2__tags` oculto en mobile.
- `.hero-v2__copy` en ≥1440: `max-width: min(48%, 690px)`.

### Solve
- `.solve-v2__copy`: `width:90%; max-width:510px`.
- Mobile: H2 36px, bajada 71%, CTAs igual que el hero.

### Productos destacados
- Mobile: eyebrow 10px, H2 40px (dos líneas), bajada 75%, imagen de producto 150px.
- Carrusel: las 5 fotos ahora son `cat-audi`, `cat-craneana`, `cat-calzado2`, `cat-ocu`, `cat-resp`.
  La tarjeta que era el segundo producto ocular pasó a **Casco de seguridad / Protección craneana**.

### Destacado "Impermeables" (mobile)
- `min-height:400px`, `object-position:77% center`, velo reforzado a la izquierda,
  `padding:28px var(--pad)`, párrafo 26ch.

### Carrusel de marcas
- Logos renombrados a `logo-<marca>.webp` (libus, ziao, agio, ombu, worksafe, conwork).
  **Pendiente: falta `logo-diforza.webp`** — sigue usando `brand-diforza.webp` (174×70, otra proporción).
- Altura única para todos: 44 / 50 / **56px**. Ombú y Conwork -20% vía `.is-sm` (35/40/45px).
- Sin leyenda bajo El Ombú.
- Separadores: `.brands-v2__group::before` centrado en `var(--brands-gap)`. Una línea por
  límite de grupo, ninguna entre logos, y el patrón cierra solo en el loop.

### Otros
- `.pcard-v2`: `flex-direction:row-reverse` + `space-between` → ícono a la derecha.
- `.dif-v2__problem`: `gap:2.2em`. `.protect-v2__copy h2`: 31/40 + margin 18px.
  `.factory-v2__copy h2`: 34/40, sin `max-width:14ch`. (Ojo: valores de la regla base;
  los overrides de ≥768 y ≥1280 siguen vigentes.)
- `.faq`: `padding-top:0` y el doble espacio pasado abajo (96 / 144 / 140px), porque
  se sumaba con el `padding-bottom` de `.factory-v2` (las dos secciones son blancas).

## Trampas encontradas (no repetirlas)

1. **`.hero-v2__worker--over`** (z-index 40, la copia que cruza el navbar) tapaba los CTAs en
   mobile. Va con `display:none` y **después** de la regla de `.hero-v2__worker` —
   misma especificidad, gana la última. Hoy está como `.hero-v2 .hero-v2__worker--over`.
2. **`<br>` sin espacios** (`equipamiento<br>de`): al ocultarlos en mobile las palabras se
   pegan ("equipamientode"). Siempre ` <br> `.
3. **`.products-v2__heading p`** también matchea la eyebrow (es un `<p>`). La eyebrow necesita
   `.products-v2__heading .products-v2__eyebrow` y la bajada `p:not(.products-v2__eyebrow)`.
   En desktop la eyebrow sigue heredando los 14px de esa regla — **pendiente si se quiere corregir**.
4. **`</br>`** mal cerrados partían "Stock permanente garantizado" en tres líneas. Corregido.

## Cómo verificar

Playwright headless con `executablePath:'/opt/pw-browsers/chromium'` y **`reducedMotion:'reduce'`**
— sin eso las animaciones `hero-anim` quedan a medio camino y el screenshot engaña.
Anchos de control: 375 / 430 / 768 / 1024 / 1366 / 1440 / 1536 / 1920.
