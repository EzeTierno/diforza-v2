# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# =====================================================================
# 1) CSS: reemplaza el bloque de animaciones del hero
# =====================================================================
old_worker = """/* Operario recortado: anclado abajo a la derecha, altura relativa al hero. */
.hero-v2__worker{
  position:absolute;z-index:1;bottom:0;right:0;height:88%;
  display:none;pointer-events:none;
  will-change:transform;
}"""
new_worker = """/* --- Capa de reflejos diagonales (antes quemados en hero-bg.webp) ---
   Dos bandas de luz en gradiente, inclinadas con skewX, que recorren la
   diagonal en loop muy lento. Van por encima del fondo pero por debajo
   del operario, en modo screen para que sumen luz sin lavar la foto. */
.hero-v2__shine{
  position:absolute;inset:-20% -30%;z-index:1;pointer-events:none;
  overflow:hidden;mix-blend-mode:screen;opacity:.55;
}
.hero-v2__shine span{
  position:absolute;top:-30%;bottom:-30%;width:22%;
  transform:skewX(-18deg);
  background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.28) 45%, rgba(255,255,255,.42) 55%, rgba(255,255,255,0) 100%);
}
.hero-v2__shine span:nth-child(1){left:38%;width:26%;}
.hero-v2__shine span:nth-child(2){left:66%;width:14%;opacity:.7;}

/* Operario recortado: anclado abajo a la derecha, altura relativa al hero. */
.hero-v2__worker{
  position:absolute;z-index:2;bottom:0;right:0;height:88%;
  display:none;pointer-events:none;
}"""
assert old_worker in s
s = s.replace(old_worker, new_worker, 1)

# El inner y las capas superiores suben un nivel de z (el shine ocupa el 1)
s = s.replace(""".hero-v2__inner{
  position:relative;z-index:2;width:100%;""",
""".hero-v2__inner{
  position:relative;z-index:3;width:100%;""", 1)
s = s.replace(""".hero-v2__claim{
  position:absolute;z-index:3;right:22px;top:32%;""",
""".hero-v2__claim{
  position:absolute;z-index:4;right:22px;top:32%;""", 1)
s = s.replace(""".hero-v2__pillars{
  position:absolute;z-index:3;right:22px;bottom:9%;""",
""".hero-v2__pillars{
  position:absolute;z-index:4;right:22px;bottom:9%;""", 1)

# =====================================================================
# 2) CSS: bloque completo de animaciones del hero (entrada + loops)
# =====================================================================
anchor = "/* ---- Sector 2: Marcas (carrusel) ---- */"
anim_css = """/* ---- Animaciones del hero ----
   Entrada escalonada por capas: fondo -> operario -> copy linea por linea.
   Todo arranca solo cuando .hero-v2 recibe .is-ready (lo agrega el JS al
   cargar la imagen del operario), asi ninguna capa aparece antes de tiempo.
   Loops: ken burns del fondo y reflejos diagonales recorriendo la diagonal.
   Con prefers-reduced-motion queda todo estatico en su estado final. */

/* Estado inicial: las capas esperan ocultas antes de .is-ready */
.hero-v2__bg img{transform:scale(1.08);opacity:0;}
.hero-v2__shine{opacity:0;}
.hero-v2__worker{opacity:0;transform:translateY(40px) scale(1.04);}
.hero-v2 .hero-anim{opacity:0;}

@keyframes hero-bg-in{from{opacity:0;transform:scale(1.08);}to{opacity:1;transform:scale(1.03);}}
@keyframes hero-kenburns{from{transform:scale(1.03);}to{transform:scale(1.09);}}
@keyframes hero-worker-in{
  from{opacity:0;transform:translateY(40px) scale(1.04);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
@keyframes hero-shine-in{from{opacity:0;}to{opacity:.55;}}
@keyframes hero-shine-sweep{
  0%{transform:skewX(-18deg) translateX(-40%);}
  100%{transform:skewX(-18deg) translateX(120%);}
}
@keyframes hero-copy-in{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:translateY(0);}}

@media (prefers-reduced-motion: no-preference){
  /* Capa 1 — fondo: entra y encadena el ken burns en loop lento */
  .hero-v2.is-ready .hero-v2__bg img{
    animation:hero-bg-in 1.1s cubic-bezier(.22,.61,.36,1) forwards,
              hero-kenburns 28s ease-in-out 1.1s infinite alternate;
  }
  /* Capa 2 — reflejos: aparecen y recorren la diagonal, desfasados entre si */
  .hero-v2.is-ready .hero-v2__shine{animation:hero-shine-in 1.4s ease .5s forwards;}
  .hero-v2.is-ready .hero-v2__shine span{
    animation:hero-shine-sweep 14s linear infinite;
    will-change:transform;
  }
  .hero-v2.is-ready .hero-v2__shine span:nth-child(2){animation-duration:19s;animation-delay:-7s;}
  /* Capa 3 — operario */
  .hero-v2.is-ready .hero-v2__worker{
    animation:hero-worker-in 1.1s cubic-bezier(.22,.61,.36,1) .35s forwards;
    will-change:transform,opacity;
  }
  /* Capa 4 — copy, linea por linea sobre la entrada del operario */
  .hero-v2.is-ready .hero-anim{animation:hero-copy-in .7s cubic-bezier(.22,.61,.36,1) forwards;}
  .hero-v2.is-ready .hero-anim--1{animation-delay:.55s;}
  .hero-v2.is-ready .hero-anim--2{animation-delay:.68s;}
  .hero-v2.is-ready .hero-anim--3{animation-delay:.81s;}
  .hero-v2.is-ready .hero-anim--4{animation-delay:.94s;}
  .hero-v2.is-ready .hero-anim--5{animation-delay:1.07s;}
}

/* Sin animaciones: todo visible en su estado final */
@media (prefers-reduced-motion: reduce){
  .hero-v2__bg img{opacity:1;transform:scale(1);}
  .hero-v2__shine{opacity:.5;}
  .hero-v2__worker{opacity:1;transform:none;}
  .hero-v2 .hero-anim{opacity:1;}
}
/* Fallback si el JS no corre: a los 3s el CSS no puede decidir, asi que
   dejamos el estado final tambien cuando .is-ready nunca llega. */
.hero-v2.no-js .hero-v2__bg img,
.hero-v2.no-js .hero-v2__worker,
.hero-v2.no-js .hero-anim{opacity:1;transform:none;}
.hero-v2.no-js .hero-v2__shine{opacity:.5;}

"""
s = s.replace(anchor, anim_css + anchor, 1)

# =====================================================================
# 3) HTML: capa de reflejos + quitar los data-parallax
# =====================================================================
s = s.replace("""    <img src="img/hero-bg.webp" alt="" aria-hidden="true" data-parallax="0.12">
  </div>""",
"""    <img src="img/hero-bg.webp" alt="" aria-hidden="true">
  </div>
  <div class="hero-v2__shine" aria-hidden="true"><span></span><span></span></div>""", 1)

s = s.replace("""<div class="hero-v2__worker hero-anim hero-anim--2" data-parallax="0.28">
    <img src="img/worker-bg.webp\"""",
"""<div class="hero-v2__worker">
    <img src="img/worker-bg.webp\"""", 1)

# =====================================================================
# 4) JS: fuera el parallax, entra el disparador de la secuencia
# =====================================================================
start = s.index("""(function(){
  // Parallax del hero""")
end = s.index("""(function(){
  // Scroll-reveal""")
new_js = """(function(){
  // Dispara la secuencia de entrada del hero recien cuando la imagen del
  // operario esta decodificada, para que ninguna capa aparezca a destiempo.
  // Si algo falla, un timeout de seguridad muestra todo igual.
  var hero = document.querySelector('.hero-v2');
  if (!hero) return;
  var img = hero.querySelector('.hero-v2__worker img');
  var done = false;
  function start(){
    if (done) return;
    done = true;
    requestAnimationFrame(function(){ hero.classList.add('is-ready'); });
  }
  if (img && img.decode){ img.decode().then(start).catch(start); }
  else if (img && !img.complete){ img.addEventListener('load', start); img.addEventListener('error', start); }
  else { start(); }
  setTimeout(function(){ if (!done){ hero.classList.add('no-js'); start(); } }, 2500);
})();
"""
s = s[:start] + new_js + s[end:]

io.open(P, "w", encoding="utf-8").write(s)
print("OK4")
