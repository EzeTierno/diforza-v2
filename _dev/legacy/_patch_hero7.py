# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------------
# 1) Las bandas toman el MISMO angulo que el panel (-28deg)
# ---------------------------------------------------------------------
s = s.replace("""  position:absolute;top:-20%;bottom:-20%;left:0;width:11%;
  transform:skewX(-15deg);""",
"""  position:absolute;top:-20%;bottom:-20%;left:0;width:11%;
  transform:skewX(-28deg);""", 1)

s = s.replace("""@keyframes hero-shine-sweep{
  0%  {transform:skewX(-15deg) translateX(-160%);opacity:0;}
  14% {opacity:1;}
  80% {opacity:1;}
  100%{transform:skewX(-15deg) translateX(1000%);opacity:0;}
}""",
"""@keyframes hero-shine-sweep{
  0%  {transform:skewX(-28deg) translateX(-160%);opacity:0;}
  14% {opacity:1;}
  80% {opacity:1;}
  100%{transform:skewX(-28deg) translateX(1000%);opacity:0;}
}""", 1)

# ---------------------------------------------------------------------
# 2) La segunda banda clara pasa a ser OSCURA (una de cada una, como el
#    original: un reflejo de luz y una veladura oscura).
# ---------------------------------------------------------------------
s = s.replace(""".hero-v2__shine .beam--2{
  width:5.5%;
  background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.26) 50%, rgba(255,255,255,0) 100%);
}""",
""".hero-v2__shine .beam--dark{
  width:8%;
  background:linear-gradient(90deg,
    rgba(0,18,38,0) 0%,
    rgba(0,18,38,.10) 45%,
    rgba(0,18,38,.14) 55%,
    rgba(0,18,38,0) 100%);
}""", 1)

s = s.replace(""".hero-v2.is-ready .hero-v2__shine .beam--2{animation-duration:13s;animation-delay:-5.5s;}""",
""".hero-v2.is-ready .hero-v2__shine .beam--dark{animation-duration:13s;animation-delay:-5.5s;}""", 1)

s = s.replace("""    <div class="beam"></div>
    <div class="beam beam--2"></div>""",
"""    <div class="beam"></div>
    <div class="beam beam--dark"></div>""", 1)

# ---------------------------------------------------------------------
# 3) El panel oscuro deja de estar quieto: deriva lateral muy lenta y
#    respiracion de densidad, en alternate para que nunca haya reinicio.
# ---------------------------------------------------------------------
s = s.replace("""  transform:skewX(-28deg);transform-origin:top left;""",
"""  transform:skewX(-28deg) translateX(0);transform-origin:top left;""", 1)

s = s.replace("""@keyframes hero-copy-in{""",
"""@keyframes hero-panel-drift{
  from{transform:skewX(-28deg) translateX(0);opacity:.85;}
  to  {transform:skewX(-28deg) translateX(-5%);opacity:1;}
}
@keyframes hero-copy-in{""", 1)

s = s.replace("""  .hero-v2.is-ready .hero-v2__shine .beam{""",
"""  .hero-v2.is-ready .hero-v2__shine .panel{
    animation:hero-panel-drift 22s ease-in-out infinite alternate;
    will-change:transform,opacity;
  }
  .hero-v2.is-ready .hero-v2__shine .beam{""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK7")
