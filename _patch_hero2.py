# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# 1) Header: padding lateral propio (el --pad global de 1280+ es 320px y aplasta el nav)
s = s.replace(""".header{
  background:transparent;
  padding:16px var(--pad);""", """.header{
  background:transparent;
  padding:16px 24px;""", 1)
s = s.replace(""".header.is-stuck{background:var(--navy);box-shadow:0 4px 20px rgba(0,26,52,.25);}""",
"""@media(min-width:768px){ .header{padding:18px 40px;} }
@media(min-width:1280px){ .header{padding:20px 64px;} }
@media(min-width:1600px){ .header{padding:20px 96px;} }
.header.is-stuck{background:var(--navy);box-shadow:0 4px 20px rgba(0,26,52,.25);}""", 1)

# CTA del header: oculto en mobile (la regla .header .btn--nav le ganaba a .header__cta)
s = s.replace(""".header .btn--nav{
  background:var(--orange);""", """.header .btn--nav{
  background:var(--orange);
  display:none;""", 1)
s = s.replace("""@media(min-width:1024px){ .header__cta{display:inline-flex;} }""",
"""@media(min-width:1024px){ .header .btn--nav{display:inline-flex;} }""", 1)
s = s.replace(""".header__cta{display:none;}\n""", "", 1)

# Nav mobile desplegable: que arranque debajo del header fijo, con fondo solido
s = s.replace(""".nav.is-open{
  display:flex;position:absolute;top:100%;left:0;right:0;
  background:var(--navy);padding:20px var(--pad) 28px;box-shadow:0 12px 24px rgba(0,26,52,.25);
}""", """.nav.is-open{
  display:flex;position:absolute;top:100%;left:0;right:0;
  background:var(--navy);padding:20px 24px 28px;box-shadow:0 12px 24px rgba(0,26,52,.25);
}""", 1)

# 2) Hero: padding lateral propio + alineacion superior (el contenido desbordaba al centrarse)
s = s.replace(""".hero-v2__inner{
  position:relative;z-index:2;width:100%;
  display:flex;align-items:center;
  padding:120px var(--pad) 56px;
}
@media(min-width:1024px){ .hero-v2__inner{padding:140px var(--pad) 64px;} }
@media(min-width:1280px){ .hero-v2__inner{padding-top:150px;} }

.hero-v2__copy{display:flex;flex-direction:column;width:100%;max-width:620px;}
@media(min-width:1024px){ .hero-v2__copy{max-width:52%;} }""",
""".hero-v2__inner{
  position:relative;z-index:2;width:100%;
  display:flex;align-items:center;
  padding:104px 24px 48px;
}
@media(min-width:768px){ .hero-v2__inner{padding:120px 40px 48px;} }
@media(min-width:1024px){ .hero-v2__inner{padding:128px 56px 52px;} }
@media(min-width:1280px){ .hero-v2__inner{padding:132px 64px 56px;} }
@media(min-width:1600px){ .hero-v2__inner{padding:140px 96px 60px;} }

.hero-v2__copy{display:flex;flex-direction:column;width:100%;max-width:600px;}
@media(min-width:1024px){ .hero-v2__copy{max-width:min(50%,560px);} }
@media(min-width:1440px){ .hero-v2__copy{max-width:min(48%,620px);} }""", 1)

# 3) H1 un punto mas contenido para no romper en 5 lineas
s = s.replace("""@media(min-width:1280px){ .hero-v2__copy h1{font-size:58px;margin-bottom:22px;} }
@media(min-width:1600px){ .hero-v2__copy h1{font-size:64px;} }""",
"""@media(min-width:1024px){ .hero-v2__copy h1{font-size:44px;} }
@media(min-width:1280px){ .hero-v2__copy h1{font-size:50px;margin-bottom:20px;} }
@media(min-width:1600px){ .hero-v2__copy h1{font-size:58px;} }""", 1)

# 4) Operario: mas chico y pegado a la derecha, para que no invada la columna de texto
s = s.replace("""@media(min-width:768px){ .hero-v2__worker{display:block;right:2%;height:82%;} }
@media(min-width:1024px){ .hero-v2__worker{right:8%;height:92%;} }
@media(min-width:1440px){ .hero-v2__worker{right:14%;height:95%;} }""",
"""@media(min-width:768px){ .hero-v2__worker{display:block;right:-4%;height:74%;} }
@media(min-width:1024px){ .hero-v2__worker{right:2%;height:86%;} }
@media(min-width:1280px){ .hero-v2__worker{right:6%;height:90%;} }
@media(min-width:1600px){ .hero-v2__worker{right:12%;height:94%;} }""", 1)

# 5) Beneficios: mas aire, que no se corten en columnas angostas
s = s.replace(""".hero-v2__benefits li{flex:1;padding:0 18px;border-left:1px solid rgba(0,53,104,.16);}""",
""".hero-v2__benefits li{flex:1;min-width:0;padding:0 14px;border-left:1px solid rgba(0,53,104,.16);}""", 1)
s = s.replace(""".hero-v2__benefits svg{flex:none;width:30px;height:30px;""",
""".hero-v2__benefits svg{flex:none;width:26px;height:26px;""", 1)
s = s.replace("""  font-weight:400;font-size:13px;line-height:1.35;color:var(--navy);
}""", """  font-weight:400;font-size:12.5px;line-height:1.4;color:var(--navy);
}""", 1)

# 6) Bloques verticales derechos: apoyados en el borde real, no tapados por el operario
s = s.replace(""".hero-v2__claim{
  position:absolute;z-index:3;right:22px;top:34%;""",
""".hero-v2__claim{
  position:absolute;z-index:3;right:22px;top:32%;""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK2")
