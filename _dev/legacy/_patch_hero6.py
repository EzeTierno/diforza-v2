# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------------
# CSS de la capa de reflejos, reconstruido a partir de la diferencia real
# entre hero-bg.webp (con reflejos) y hero-bg-2.webp (limpio).
# ---------------------------------------------------------------------
start = s.index("/* --- Capa de reflejos diagonales")
end = s.index("/* Operario recortado:")
shine_css = """/* --- Capa de reflejos diagonales (antes quemados en hero-bg.webp) ---
   Geometria medida sobre la diferencia entre hero-bg.webp y hero-bg-2.webp:
   1) un panel OSCURO (~7% negro) de borde nitido inclinado 28deg, que
      cubria todo el sector derecho — es lo que estructuraba la foto, va fijo;
   2) una banda de LUZ de ~11% de ancho inclinada 15deg, que se desvanecia
      hacia abajo — esa es la que recorre.
   Los dos van sobre el fondo y debajo del operario. */
.hero-v2__shine{
  position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden;
}

/* 1 — Panel oscuro fijo (reemplaza el que estaba quemado en la imagen) */
.hero-v2__shine .panel{
  position:absolute;top:-15%;bottom:-15%;left:62%;right:-40%;
  transform:skewX(-28deg);transform-origin:top left;
  background:linear-gradient(90deg, rgba(0,18,38,.10) 0%, rgba(0,18,38,.055) 45%, rgba(0,18,38,.085) 100%);
}

/* 2 — Bandas de luz que recorren la diagonal */
.hero-v2__shine .beam{
  position:absolute;top:-20%;bottom:-20%;left:0;width:11%;
  transform:skewX(-15deg);
  background:linear-gradient(90deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.30) 42%,
    rgba(255,255,255,.46) 52%,
    rgba(255,255,255,.30) 62%,
    rgba(255,255,255,0) 100%);
  /* la luz pierde fuerza hacia abajo, como en el original */
  -webkit-mask-image:linear-gradient(to bottom, #000 0%, #000 38%, rgba(0,0,0,.25) 78%, transparent 100%);
  mask-image:linear-gradient(to bottom, #000 0%, #000 38%, rgba(0,0,0,.25) 78%, transparent 100%);
}
.hero-v2__shine .beam--2{
  width:5.5%;
  background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.26) 50%, rgba(255,255,255,0) 100%);
}

"""
s = s[:start] + shine_css + s[end:]

# El contenedor ya no necesita blend ni opacidad global (cada capa trae la suya)
s = s.replace("""@keyframes hero-shine-in{from{opacity:0;}to{opacity:.85;}}""",
              """@keyframes hero-shine-in{from{opacity:0;}to{opacity:1;}}""", 1)
s = s.replace(""".hero-v2.no-js .hero-v2__shine{opacity:.85;}""",
              """.hero-v2.no-js .hero-v2__shine{opacity:1;}""", 1)
s = s.replace("""  .hero-v2__shine{opacity:.85;}""", """  .hero-v2__shine{opacity:1;}""", 1)

# Recorrido: mas rapido y perceptible, con fade en los extremos para que el
# reinicio siga siendo invisible.
s = s.replace("""@keyframes hero-shine-sweep{
  0%  {transform:skewX(-18deg) translateX(-140%);opacity:0;}
  18% {opacity:1;}
  82% {opacity:1;}
  100%{transform:skewX(-18deg) translateX(220%);opacity:0;}
}""",
"""@keyframes hero-shine-sweep{
  0%  {transform:skewX(-15deg) translateX(-160%);opacity:0;}
  14% {opacity:1;}
  80% {opacity:1;}
  100%{transform:skewX(-15deg) translateX(1000%);opacity:0;}
}""", 1)

# El selector de las bandas cambia de span a .beam
s = s.replace(""".hero-v2.is-ready .hero-v2__shine span{
    animation:hero-shine-sweep 17s ease-in-out infinite;
    will-change:transform;
  }
  .hero-v2.is-ready .hero-v2__shine span:nth-child(2){animation-duration:26s;animation-delay:-11s;}""",
""".hero-v2.is-ready .hero-v2__shine .beam{
    animation:hero-shine-sweep 9s ease-in-out infinite;
    will-change:transform,opacity;
  }
  .hero-v2.is-ready .hero-v2__shine .beam--2{animation-duration:13s;animation-delay:-5.5s;}""", 1)

# Estado inicial / reduced-motion del panel (siempre visible, no anima)
s = s.replace("""@media (prefers-reduced-motion: reduce){
  .hero-v2__bg img{opacity:1;transform:scale(1);}""",
"""@media (prefers-reduced-motion: reduce){
  .hero-v2__bg img{opacity:1;transform:scale(1);}
  .hero-v2__shine .beam{opacity:.5;left:34%;}""", 1)

# ---------------------------------------------------------------------
# HTML de la capa
# ---------------------------------------------------------------------
s = s.replace("""<div class="hero-v2__shine" aria-hidden="true"><span></span><span></span></div>""",
"""<div class="hero-v2__shine" aria-hidden="true">
    <div class="panel"></div>
    <div class="beam"></div>
    <div class="beam beam--2"></div>
  </div>""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK6")
