# -*- coding: utf-8 -*-
# Restaura el bloque de layout del hero que se perdio del <style>
# (inner / copy / eyebrow / h1 / lead / benefits / ctas / tags / claim / pillars),
# ya con todos los ajustes acordados. Se inserta entre la capa de reflejos y
# el bloque de animaciones. Idempotente: si ya existe, no hace nada.
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

if ".hero-v2__copy h1{" in s:
    print("SIN CAMBIOS: el layout ya esta presente")
    raise SystemExit

anchor = "/* Estado inicial: las capas esperan ocultas antes de .is-ready */"
assert anchor in s, "no encuentro el bloque de animaciones"

layout = """/* Operario recortado: anclado abajo a la derecha, altura relativa al hero. */
.hero-v2__worker img{height:100%;width:auto;object-fit:contain;object-position:bottom right;}
@media(min-width:768px){ .hero-v2__worker{display:block;right:-4%;height:74%;} }
@media(min-width:1024px){ .hero-v2__worker{right:2%;height:86%;} }
@media(min-width:1280px){ .hero-v2__worker{right:6%;height:90%;} }
@media(min-width:1600px){ .hero-v2__worker{right:12%;height:94%;} }

.hero-v2__inner{
  position:relative;z-index:3;width:100%;
  display:flex;align-items:center;
  padding:104px 24px 48px;
}
@media(min-width:768px){ .hero-v2__inner{padding:120px 40px 48px;} }
@media(min-width:1024px){ .hero-v2__inner{padding:128px 56px 52px;} }
@media(min-width:1280px){ .hero-v2__inner{padding:132px 64px 56px;} }
@media(min-width:1600px){ .hero-v2__inner{padding:140px 96px 60px;} }

.hero-v2__copy{display:flex;flex-direction:column;width:100%;max-width:600px;}
@media(min-width:1024px){ .hero-v2__copy{max-width:min(50%,560px);} }
@media(min-width:1440px){ .hero-v2__copy{max-width:min(48%,620px);} }

.hero-v2__eyebrow{
  display:flex;align-items:center;gap:14px;
  font-family:"Montserrat",Arial,sans-serif;
  font-weight:600;font-size:12px;color:var(--navy);letter-spacing:.14em;
  text-transform:uppercase;margin:0 0 18px;
}
.hero-v2__eyebrow::before{content:"";width:36px;height:3px;background:var(--orange);flex:none;border-radius:2px;}
@media(min-width:1280px){ .hero-v2__eyebrow{font-size:13px;margin-bottom:22px;} }

.hero-v2__copy h1{
  font-family:"Poppins","Montserrat",Arial,sans-serif;font-weight:800;
  font-size:34px;line-height:1.06;margin:0 0 18px;letter-spacing:-.02em;color:var(--navy);
}
.hero-v2__copy h1 .accent{color:var(--orange);display:block;}
@media(min-width:768px){ .hero-v2__copy h1{font-size:48px;} }
@media(min-width:1024px){ .hero-v2__copy h1{font-size:44px;} }
@media(min-width:1280px){ .hero-v2__copy h1{font-size:50px;margin-bottom:20px;} }
@media(min-width:1600px){ .hero-v2__copy h1{font-size:58px;} }

.hero-v2__lead{font-weight:400;font-size:15px;line-height:1.55;color:#3c4c5c;margin:0 0 28px;max-width:34em;}
@media(min-width:1280px){ .hero-v2__lead{font-size:17px;margin-bottom:34px;} }

/* Los 3 beneficios: cada uno con su icono, en fila desde tablet. Las
   columnas se ajustan al largo real de su texto (flex-basis de contenido);
   con partes iguales, el primero quedaba con un hueco a la derecha. */
.hero-v2__benefits{
  list-style:none;margin:0 0 30px;padding:0;
  display:flex;flex-direction:column;gap:16px;
}
@media(min-width:768px){ .hero-v2__benefits{flex-direction:row;align-items:flex-start;gap:22px;margin-bottom:36px;} }
@media(min-width:1280px){ .hero-v2__benefits{gap:26px;} }
.hero-v2__benefits li{
  display:flex;align-items:flex-start;gap:12px;
  font-weight:400;font-size:12.5px;line-height:1.4;color:var(--navy);
}
@media(min-width:768px){
  .hero-v2__benefits li{flex:1 1 auto;min-width:0;padding-left:22px;border-left:1px solid rgba(0,53,104,.16);}
  .hero-v2__benefits li:first-child{padding-left:0;border-left:none;}
}
@media(min-width:1280px){ .hero-v2__benefits li{font-size:13.5px;} }
.hero-v2__benefits svg{flex:none;width:26px;height:26px;color:var(--navy);stroke-width:1.4;}

.hero-v2 .ctas{margin-bottom:34px;}
@media(min-width:1280px){ .hero-v2 .ctas{margin-bottom:44px;} }
.hero-v2 .btn{display:inline-flex;align-items:center;gap:10px;}
.hero-v2 .btn svg{width:15px;height:15px;flex:none;}
.hero-v2 .btn--outline{border:2px solid rgba(0,53,104,.35);color:var(--navy);background:rgba(255,255,255,.55);}
.hero-v2 .btn--outline:hover{border-color:var(--navy);background:#fff;}

/* Span de atributos debajo de los botones. La linea es corta (ancho fijo),
   no del ancho del contenedor. */
.hero-v2__tags{
  position:relative;
  display:flex;align-items:center;flex-wrap:wrap;gap:10px;
  padding-top:22px;
  font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6b7c;
}
.hero-v2__tags::before{
  content:"";position:absolute;top:0;left:0;
  width:96px;height:1px;background:rgba(0,53,104,.28);
}
@media(min-width:1280px){ .hero-v2__tags{font-size:12px;gap:12px;} .hero-v2__tags::before{width:110px;} }
.hero-v2__tags .sep{color:rgba(0,53,104,.28);}
.hero-v2__tags img{height:13px;width:auto;display:inline-block;}

/* Bloques verticales sobre la foto (solo desktop). */
.hero-v2__claim{
  position:absolute;z-index:4;right:22px;top:32%;
  display:none;
  font-weight:600;font-size:12px;letter-spacing:.22em;text-transform:uppercase;
  color:rgba(255,255,255,.9);line-height:1.9;text-align:right;
}
@media(min-width:1280px){ .hero-v2__claim{display:block;right:34px;} }
.hero-v2__claim::before{content:"";display:block;width:30px;height:2px;background:var(--orange);margin:0 0 12px auto;}

.hero-v2__pillars{
  position:absolute;z-index:4;right:22px;bottom:9%;
  display:none;flex-direction:column;gap:20px;margin:0;padding:0;
}
@media(min-width:1280px){ .hero-v2__pillars{display:flex;right:34px;} }
.hero-v2__pillars li{display:flex;align-items:center;justify-content:flex-end;gap:12px;list-style:none;}
.hero-v2__pillars span{
  font-weight:600;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(255,255,255,.92);line-height:1.5;text-align:right;max-width:90px;
}
.hero-v2__pillars svg{width:26px;height:26px;flex:none;color:rgba(255,255,255,.92);stroke-width:1.3;}

"""

s = s.replace(anchor, layout + anchor, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("RESTAURADO")
