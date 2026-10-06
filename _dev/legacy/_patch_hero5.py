# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# 1) Fondo limpio (sin los reflejos quemados)
s = s.replace('<img src="img/hero-bg.webp" alt="" aria-hidden="true">',
              '<img src="img/hero-bg-2.webp" alt="" aria-hidden="true">', 1)
s = s.replace("""   Fondo full-bleed (hero-bg.webp: mitad clara a la izquierda + obra
   desenfocada con los reflejos en diagonal ya quemados en la imagen).""",
"""   Fondo full-bleed (hero-bg-2.webp: mitad clara a la izquierda + obra
   desenfocada, limpia — los reflejos en diagonal se dibujan y animan
   por codigo en la capa .hero-v2__shine).""", 1)

# 2) El corte del loop: la banda todavia se veia al reiniciar el recorrido.
#    Ahora entra y sale con fade dentro del propio keyframe, y el recorrido
#    empieza/termina fuera de cuadro, asi el reinicio cae en opacidad 0.
old = """@keyframes hero-shine-sweep{
  0%{transform:skewX(-18deg) translateX(-40%);}
  100%{transform:skewX(-18deg) translateX(120%);}
}"""
new = """@keyframes hero-shine-sweep{
  0%  {transform:skewX(-18deg) translateX(-140%);opacity:0;}
  18% {opacity:1;}
  82% {opacity:1;}
  100%{transform:skewX(-18deg) translateX(220%);opacity:0;}
}"""
assert old in s
s = s.replace(old, new, 1)

# La opacidad base de cada banda ahora la maneja el keyframe: el contenedor
# sube a 1 y el peso de cada reflejo se define en el gradiente.
s = s.replace(""".hero-v2__shine{
  position:absolute;inset:-20% -30%;z-index:1;pointer-events:none;
  overflow:hidden;mix-blend-mode:screen;opacity:.55;
}""",
""".hero-v2__shine{
  position:absolute;inset:-20% -40%;z-index:1;pointer-events:none;
  overflow:hidden;mix-blend-mode:screen;opacity:.85;
}""", 1)
s = s.replace("""@keyframes hero-shine-in{from{opacity:0;}to{opacity:.55;}}""",
              """@keyframes hero-shine-in{from{opacity:0;}to{opacity:.85;}}""", 1)
s = s.replace(""".hero-v2.no-js .hero-v2__shine{opacity:.5;}""",
              """.hero-v2.no-js .hero-v2__shine{opacity:.85;}""", 1)
s = s.replace("""  .hero-v2__shine{opacity:.5;}""", """  .hero-v2__shine{opacity:.85;}""", 1)

# Los dos reflejos parten desde el mismo borde (el desfase lo dan duracion y
# delay); antes el segundo arrancaba ya dentro de cuadro y eso marcaba el corte.
s = s.replace(""".hero-v2__shine span:nth-child(1){left:38%;width:26%;}
.hero-v2__shine span:nth-child(2){left:66%;width:14%;opacity:.7;}""",
""".hero-v2__shine span:nth-child(1){left:0;width:26%;}
.hero-v2__shine span:nth-child(2){left:0;width:13%;
  background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.2) 50%, rgba(255,255,255,0) 100%);}""", 1)

# Recorridos mas largos y en proporcion no entera, para que las dos bandas
# tarden mucho en volver a coincidir (el patron no se lee repetitivo).
s = s.replace("""    animation:hero-shine-sweep 14s linear infinite;""",
"""    animation:hero-shine-sweep 17s ease-in-out infinite;""", 1)
s = s.replace(""".hero-v2.is-ready .hero-v2__shine span:nth-child(2){animation-duration:19s;animation-delay:-7s;}""",
""".hero-v2.is-ready .hero-v2__shine span:nth-child(2){animation-duration:26s;animation-delay:-11s;}""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK5")
