# L3 · EPP y protección industrial — sesión 30/09/2026

## Qué es y dónde está
- Landing de categoría `/epp-proteccion-industrial/`, armada con el mismo proceso que L2.
- Carpeta autocontenida: subir SOLO `index.html` + `img/` (~200 KB). `_no-subir/` = fuente del build, originales y este resumen.
- Copy literal de `landing-1/04_copy_03_epp_proteccion_industrial.md` (testimonios extra y garantía del doc 01 / doc 16 §5). SEO: doc 06 (title "EPP Certificado para Industria | Diforza").

## Cómo editarla
- `_no-subir/fuente-build/build.py` une el `<style>`/`<script>` de la home (`diforza-v2/index.html`) + `l3.css` + `body.html` + `l3.js`.
  Uso (desde fuente-build): `python build.py ../../../index.html ../../index.html`. No editar `index.html` a mano (el build lo pisa).
- Categorías (S4), productos (S5) y chips del formulario se generan desde las listas `CATS`, `PRODS` y `CHECKS` de build.py.
- `l3.css` = copia de l2.css con prefijo `*-l3` + bloque final "Propio de L3".

## Estructura (misma que L2)
hero › franja de confianza › cobertura por riesgo (navy, 8 categorías con alcance + CTA) › productos destacados › "Por qué las empresas eligen…" (4 diferenciales + caja naranja "El riesgo no es solo el accidente…" + acordeón de 4 problemas + reseñas) › cumplimiento normativo (banner solve-v2) › cómo trabajamos › garantía (borrador) › FAQ › CTA final + formulario.

## Decisiones del usuario (30/09)
- Hero PROVISORIO con `bg-hero-2` de la home (casco, protector auditivo, cono) → `img/bg-hero-epp.webp` + recorte mobile `bg-hero-epp-m.webp`. En ≥1024 la foto ocupa la mitad derecha con máscara de fundido (a pantalla completa tapaba el H1). La foto es de 1444×558: se ve blanda en pantallas grandes → reemplazar.
- Productos: los 8 del doc 14 en su orden, con placeholder de ícono. Única foto: respirador (220 px, marcada "Foto provisoria"). Fichas con fila "Norma" obligatoria (hoy "Pendiente norma").
- Franja S2: versión conservadora ("Cada elemento se entrega con su ficha técnica y su respaldo de ensayo…").
- ZIAO: diferencial literal del copy con chip "Pendiente alcance de categorías ZIAO" (ojo: se sabe que ZIAO es mamelucos; el copy dice "línea de EPP").
- Tabla de normas por categoría (S8): OCULTA (comentada en body.html) hasta que Diforza confirme las normas IRAM.

## Detalles técnicos nuevos respecto de L2
- Campo variable del formulario: "Categorías de EPP que necesitás" como chips multi-selección obligatorios (`data-required-group`, validación en l3.js).
- "Consultar" en un producto precarga `producto_interes`, el WhatsApp y además tilda la categoría del producto.
- Footer: link cruzado a L2 (`../indumentaria-de-trabajo/`); en L2 se actualizó el link a esta landing.

## Pendientes
- Foto de hero propia y fotos 800×800 de los 8 productos (sobre todo protección auditiva: no hay ninguna).
- Normas por producto/categoría, códigos, marca del Alternative, del arnés completo (Skiway/Skyway) y del respirador 522.
- Confirmar alcance IRAM (hero "Certificación IRAM", meta description, bajada SRT), texto S8, plazo de entrega, respuestas del FAQ, garantía, "te respondemos en el día".
- Logos: Gamisol y W|S (hoy texto + chip), logos de certificación.
- Qué categorías cubre ZIAO. Endpoint del formulario/CRM y número de WhatsApp definitivo. Quitar chips `.ph` antes de publicar.

## Actualización 30/09 (tarde)
- Hero: el usuario reemplazó `bg-hero-epp.webp` por foto propia (operario con antiparras en torno, 1376×768; original en `originales-hero/`). Recorte mobile regenerado (640×768 desde x=600). En ≥1024 el fondo arranca en `left:16%` (ajuste del usuario para 1920).
- Productos: fotos del usuario para Eco-line, Quantum, Alternative, Casco Milenium, arnés a cremallera y arnés completo. Normalizadas a 800×800 fondo blanco, producto ~85% (680 px) centrado; PSD/originales en `originales-productos/`.
- Foto del Anteojo Argon sumada. Sigue faltando la foto definitiva del respirador 522. La foto del Casco Milenium es roja (la ficha dice amarillo y blanco).

## Actualización 05/10 — hero mobile (mismo criterio que L2)
- <1024: velo `linear-gradient(90deg, rgb(255 255 255) 0%, rgb(255 255 255 / 44%) 55%, rgb(255 255 255 / 0%) 100%)`.
- <600: `.hero-v2--l3 .hero-v2__inner{padding-bottom:40px;width:95%}` y se usa la misma `bg-hero-epp.webp` (object-position 72% center). Se quitó el `<source>` mobile; `bg-hero-epp-m.webp` movida a `originales-hero/`.
- 05/10: <600 object-position `57% center` (ajuste del usuario). `bg-hero-epp.webp` re-exportada a calidad 92 (74 KB) para reducir artefactos; sigue siendo 1376×768, en celulares se estira ~2,5× → pedir original de mayor resolución.
- 05/10: franja S2 sin los párrafos `trust-l3__sub`; en mobile grilla Libus | ZIAO a `1fr 1fr` y ambos logos al mismo alto (36 px; 40 px ≥768, 44 px ≥1280).
- 05/10: mobile `.trust-l3__brands` gap 14px 18px; título "Cobertura completa…" con max-width 21ch (se quitó la regla duplicada de 12ch).
