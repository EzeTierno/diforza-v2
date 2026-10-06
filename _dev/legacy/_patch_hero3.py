# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# 1) Beneficios: las columnas se ajustan al ancho de su texto en vez de repartir
#    el espacio en partes iguales (el primero, mas corto, quedaba con un hueco).
s = s.replace("""@media(min-width:768px){ .hero-v2__benefits{flex-direction:row;gap:0;margin-bottom:36px;} }""",
"""@media(min-width:768px){ .hero-v2__benefits{flex-direction:row;align-items:flex-start;gap:22px;margin-bottom:36px;} }
@media(min-width:1280px){ .hero-v2__benefits{gap:26px;} }""", 1)

s = s.replace("""@media(min-width:768px){
  .hero-v2__benefits li{flex:1;min-width:0;padding:0 14px;border-left:1px solid rgba(0,53,104,.16);}
  .hero-v2__benefits li:first-child{padding-left:0;border-left:none;}
}""",
"""@media(min-width:768px){
  .hero-v2__benefits li{flex:0 1 auto;min-width:0;padding-left:22px;border-left:1px solid rgba(0,53,104,.16);}
  .hero-v2__benefits li:first-child{padding-left:0;border-left:none;}
}""", 1)

# 2) Linea sobre el span de atributos: corta (ancho fijo), no del ancho del contenedor.
s = s.replace(""".hero-v2__tags{
  display:flex;align-items:center;flex-wrap:wrap;gap:10px;
  padding-top:20px;border-top:1px solid rgba(0,53,104,.18);
  font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6b7c;
}""",
""".hero-v2__tags{
  position:relative;
  display:flex;align-items:center;flex-wrap:wrap;gap:10px;
  padding-top:22px;
  font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6b7c;
}
.hero-v2__tags::before{
  content:"";position:absolute;top:0;left:0;
  width:96px;height:1px;background:rgba(0,53,104,.28);
}
@media(min-width:1280px){ .hero-v2__tags::before{width:110px;} }""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK3")
