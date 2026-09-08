# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------------
# 1) Fuera las bandas que recorrian: quedan solo los dos paneles.
# ---------------------------------------------------------------------
start = s.index("/* 2 — Bandas de luz que recorren la diagonal */")
end = s.index("@keyframes hero-bg-in")
panel_css = """/* 2 — Panel claro: mismo angulo y misma construccion que el oscuro,
   ubicado a la izquierda del personaje (como en la referencia original). */
.hero-v2__shine .panel--light{
  left:34%;right:auto;width:20%;
  background:linear-gradient(90deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,.30) 30%,
    rgba(255,255,255,.42) 60%,
    rgba(255,255,255,.16) 100%);
  /* pierde fuerza hacia abajo, como el reflejo original */
  -webkit-mask-image:linear-gradient(to bottom, #000 0%, #000 42%, rgba(0,0,0,.3) 80%, transparent 100%);
  mask-image:linear-gradient(to bottom, #000 0%, #000 42%, rgba(0,0,0,.3) 80%, transparent 100%);
}

"""
s = s[:start] + panel_css + s[end:]

# El keyframe del recorrido ya no se usa
start = s.index("@keyframes hero-shine-sweep{")
end = s.index("@keyframes hero-panel-drift{")
s = s[:start] + s[end:]

# Reglas de animacion de las bandas -> fuera; el panel claro deriva en espejo
s = s.replace("""  .hero-v2.is-ready .hero-v2__shine .beam{
    animation:hero-shine-sweep 9s ease-in-out infinite;
    will-change:transform,opacity;
  }
  .hero-v2.is-ready .hero-v2__shine .beam--dark{animation-duration:13s;animation-delay:-5.5s;}""",
"""  .hero-v2.is-ready .hero-v2__shine .panel--light{
    animation:hero-panel-drift-light 26s ease-in-out infinite alternate;
    will-change:transform,opacity;
  }""", 1)

s = s.replace("""@keyframes hero-copy-in{""",
"""@keyframes hero-panel-drift-light{
  from{transform:skewX(-28deg) translateX(0);opacity:.9;}
  to  {transform:skewX(-28deg) translateX(4%);opacity:1;}
}
@keyframes hero-copy-in{""", 1)

s = s.replace("""  .hero-v2__shine .beam{opacity:.5;left:34%;}\n""", "", 1)

# ---------------------------------------------------------------------
# 2) HTML
# ---------------------------------------------------------------------
s = s.replace("""    <div class="panel"></div>
    <div class="beam"></div>
    <div class="beam beam--dark"></div>""",
"""    <div class="panel panel--light"></div>
    <div class="panel"></div>""", 1)

# El comentario de la capa, al dia
s = s.replace("""   1) un panel OSCURO (~7% negro) de borde nitido inclinado 28deg, que
      cubria todo el sector derecho — es lo que estructuraba la foto, va fijo;
   2) una banda de LUZ de ~11% de ancho inclinada 15deg, que se desvanecia
      hacia abajo — esa es la que recorre.""",
"""   1) un panel OSCURO (~7% negro) de borde nitido inclinado 28deg sobre el
      sector derecho;
   2) un panel CLARO con el mismo angulo, a la izquierda del personaje.
   Los dos derivan muy lento en alternate (sin reinicio visible).""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK8")
