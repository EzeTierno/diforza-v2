---
name: resumen-sesion-l2-indumentaria
description: Primera versión completa de la landing L2 Indumentaria de trabajo (30/09/2026) — ubicación, estructura S1–S12, qué reusa de la home v2 y qué quedó pendiente.
type: project
---

# L2 · Indumentaria de trabajo — v1 completa (30/09/2026)

Archivo: `diforza-v2/indumentaria-de-trabajo/index.html` (slug `/indumentaria-de-trabajo/`).
Imágenes y fuentes se toman de la carpeta madre (`../img/`). La home no se tocó.

## Cómo está armada
- Base: el `<style>` y el `<script>` de la home v2 copiados tal cual (rutas reescritas a `../img/`),
  y al final del `<style>` un bloque propio con prefijo `*-l2`. Mismos breakpoints (768/1024/1280/1440/1700),
  mismos tokens `--pad`/`--gutter`/`--nav-h`.
- Copy: literal de `04_copy_02_indumentaria_general.md`. Donde L2 remite a L1 (título de diferenciales,
  testimonios, FAQ de envíos) se usó el copy aprobado de `04_copy_01_institucional.md`.
- Garantía: textos placeholder del doc 16 §5, marcada como borrador (`data-draft="true"`).

## Sectores
| # | Sector | Componente |
|---|---|---|
| S1 | Hero | `.hero-v2` + modificador `.hero-v2--l2` (H1 más chico: es más largo) |
| S2 | Franja de confianza | `.trust-l2` (Diforza destacado + Ombú) |
| S4 | Solución / línea completa | `.line-l2` navy + CTA de mitad de página |
| S5 | 8 productos destacados | `.prod-l2` — carrusel draggeable <1024, grilla 4×2 ≥1024; botón Consultar precarga el form y el WhatsApp |
| S6+S3 | Diferenciales + problema (un solo sector, fondo blanco) | `.dif-v2` de la home; el problema usa el bloque naranja `.dif-v2__problem` con el título "Equipar a 80 personas…" + CTA blanco a `#contacto`, y las 4 pain points en acordeón |
| S7 | Prueba social — dentro del MISMO sector que S6 | `.dif-v2__reviews` con `.reviews-l2__grid` (Ariel destacado + 2 `gcard`) |
| S8 | Normativa | `.solve-v2` de la home (`--l2`) |
| S9 | Cómo trabajamos | `.steps-l2` |
| S10 | Garantía (borrador) | `.guarantee-l2` |
| S11 | FAQ | `.faq` + `.faq--l2` |
| S12 | CTA + formulario (doc 05) | `.cta-l2`: form de cotización con "Cantidad de personas a equipar" + form corto de catálogo colapsable |

Extras: WhatsApp flotante <1024, marcas `.ph` de VALIDAR/PENDIENTE visibles con botón "Ocultar marcas".

## Pendientes
- Fotos: solo la campera trucker tiene foto (provisoria `cat-indu.webp`). Las otras 7 muestran silueta.
  Nombres esperados: `prod-<nombre-kebab>.webp` en azul marino. Hero: foto propia de la línea (hoy usa el de la home).
- Códigos, tela/gramaje/composición y talles por producto.
- Validar: personalización (proceso, mínimos, plazos), rango de talles, normas IRAM, ignífuga, muestra previa, plazo de respuesta, garantía.
- Endpoint del formulario / CRM y número definitivo de WhatsApp (hoy +54 9 11 5956-9713, el de la home).
- Schema FAQPage cuando las respuestas estén validadas.

## Cambios
- 30/09: el bloque "Equipar a 80 personas…" pasó a ir debajo de productos destacados y suma CTA al formulario. Orden actual: hero › franja › línea completa › productos › problema › diferenciales › reseñas › normativa › pasos › garantía › FAQ › formulario.
- 30/09: las reseñas (S7) pasaron a estar dentro del sector de diferenciales ("Por qué las empresas eligen trabajar con Diforza"), igual que en la home. Orden: … › problema › diferenciales + reseñas › normativa › …
- 30/09: el sector diferenciales + reseñas va todo sobre el gris #f2f4f6 que tenían las reseñas (`.dif-v2--l2`); el badge "Más de 15 años" pasa a fondo blanco para contrastar. Problema (blanco) queda separado con su propio aire.
- 30/09: vuelve a fondo blanco. El bloque "Equipar a 80 personas…" se eliminó como sección propia y se integró dentro de "Por qué las empresas eligen…" (caja naranja + acordeón, mismo patrón de la home), para acortar la landing. Orden: hero › franja › línea completa › productos › diferenciales + problema + reseñas › normativa › pasos › garantía › FAQ › formulario.
- 30/09: hero con fondo propio `bg-hero-indumentaria.webp` (en esta carpeta; persona con pantalón cargo azul marino). Se quitó la capa del operario recortado. Encuadre: object-position 68% bottom (desktop), 22% en 1024–1279 para que la persona no quede bajo el H1, 60% en <1024 con velo blanco horizontal más fuerte.
- 30/09: productos destacados reemplazados por la selección del usuario, con fotos reales (800×800): campera trucker (Más vendido), buzo polar 1/2 cierre, camisa clásica (beige), camisa de trabajo, chomba piqué, mameluco con reflectivos (archivo `prod-pantalon-refl`, nombre a validar), traje de lluvia, traje de bombero (norma a validar). Los originales quedan intactos en esta carpeta; la landing usa copias normalizadas en `img/` (recorte al contenido, prenda al 87,5% del cuadro, fondo #FFF puro, ~10–16 KB c/u). Ya no hay siluetas placeholder.
- 30/09: carpeta preparada para subir. Autocontenida: `index.html` + `img/` (13 webp, todos en uso, incluidas las 4 compartidas con la home copiadas: logo-blanco, brand-diforza, logo-ombu, bg-hero-3). Sin rutas `../img/`. Todo lo que no se sube está en `_no-subir/` (originales de productos y este resumen). Los links del menú a `../` apuntan a la home.
- 30/09: img/bg-hero-3.webp comprimido (WebP q80, misma resolución 1774×887): 1,44 MB → 100 KB. La carpeta img/ pasa de 2,1 MB a 748 KB. El original sigue en ../img/ de la home.
- 30/09: hero con <picture>: <600px carga img/bg-hero-indumentaria-m.webp (recorte vertical 640×768 centrado en la persona, 19 KB); resto carga la foto completa recomprimida (26 KB, antes 456 KB). Original del hero en _no-subir/originales-hero/. img/ total ≈ 320 KB.
- 30/09: ≥1440 la columna del hero usa max-width:49% (sin tope de 690px) solo en L2 → H1 en 4 renglones de 1440 a 2560 (antes 5 desde 1700).
- 05/10: (definido por el usuario) velo del hero <1024 = linear-gradient(90deg, #fff 0%, rgb(255 255 255 / 44%) 55%, transparente 100%). Solo <600px (imagen vertical): .hero-v2--l2 .hero-v2__inner{padding-bottom:40px;width:95%}.
