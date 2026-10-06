# -*- coding: utf-8 -*-
import io, re, sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()
orig = s

# ---------- 1) Poppins en el <head> ----------
old_font = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
new_font = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">'
assert old_font in s, "font link"
s = s.replace(old_font, new_font, 1)

# ---------- 2) Titulos globales en Poppins 800 ----------
old_body = 'body{margin:0;font-family:"Montserrat",Arial,sans-serif;color:var(--navy);overflow-x:hidden;width:100%;}'
new_body = old_body + '\nh1,h2,h3{font-family:"Poppins","Montserrat",Arial,sans-serif;font-weight:800;}'
assert old_body in s
s = s.replace(old_body, new_body, 1)

# ---------- 3) CSS header / nav ----------
start = s.index(".header{")
end = s.index("@media(min-width:1024px){ .nav-toggle{display:none;} }") + len("@media(min-width:1024px){ .nav-toggle{display:none;} }")
header_css = u"""/* ---- Header / Nav ----
   Transparente montado sobre el hero; toma fondo navy solido al scrollear
   (clase .is-stuck que agrega el JS del final). Un scrim oscuro muy leve
   sostiene la legibilidad del logo blanco sobre el area clara del fondo. */
.header{
  background:transparent;
  padding:16px var(--pad);
  display:flex;align-items:center;justify-content:space-between;
  position:fixed; top:0; left:0; right:0; z-index:30;
  transition:background-color .3s ease, padding .3s ease, box-shadow .3s ease;
}
.header::before{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(to bottom, rgba(0,20,42,.55), rgba(0,20,42,0));
  transition:opacity .3s ease;
}
.header.is-stuck{background:var(--navy);box-shadow:0 4px 20px rgba(0,26,52,.25);}
.header.is-stuck::before{opacity:0;}
@media(min-width:1280px){ .header.is-stuck{padding-top:12px;padding-bottom:12px;} }
.header__logo img{height:34px;width:auto;}
@media(min-width:768px){ .header__logo img{height:42px;} }
@media(min-width:1280px){ .header__logo img{height:52px;} }

.nav{display:none;flex-direction:column;align-items:flex-start;gap:20px;}
.nav.is-open{
  display:flex;position:absolute;top:100%;left:0;right:0;
  background:var(--navy);padding:20px var(--pad) 28px;box-shadow:0 12px 24px rgba(0,26,52,.25);
}
@media(min-width:1024px){ .nav{display:flex;flex-direction:row;align-items:center;gap:32px;position:static;background:none;padding:0;box-shadow:none;} }
.nav a{color:#fff;font-weight:500;font-size:13px;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;position:relative;padding-bottom:3px;}
@media(min-width:1280px){ .nav a{font-size:13.5px;} }
.nav a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--orange);transform:scaleX(0);transform-origin:left;transition:transform .25s ease;}
.nav a:hover::after{transform:scaleX(1);}

.header__cta{display:none;}
@media(min-width:1024px){ .header__cta{display:inline-flex;} }
.header .btn--nav{
  background:var(--orange);color:#fff;border-radius:999px;
  padding:14px 26px;font-weight:700;font-size:12.5px;letter-spacing:.06em;
  text-transform:uppercase;text-decoration:none;
  display:inline-flex;align-items:center;gap:10px;white-space:nowrap;
  transition:transform .2s ease, box-shadow .2s ease;
}
@media(min-width:1280px){ .header .btn--nav{padding:16px 32px;font-size:13px;} }
.header .btn--nav:hover{transform:translateY(-2px);box-shadow:0 10px 20px rgba(255,126,52,.35);}
.header .btn--nav svg{width:14px;height:14px;flex:none;}

.nav-toggle{
  display:inline-flex; background:none; border:none; color:#fff; font-size:26px; line-height:1; padding:0; cursor:pointer;
}
@media(min-width:1024px){ .nav-toggle{display:none;} }"""
s = s[:start] + header_css + s[end:]

# ---------- 4) CSS del hero ----------
start = s.index("/* ---- Sector 1: Hero ----")
end = s.index("/* ---- Sector 2: Marcas (carrusel) ---- */")
hero_css = u"""/* ---- Sector 1: Hero ----
   Fondo full-bleed (hero-bg.webp: mitad clara a la izquierda + obra
   desenfocada con los reflejos en diagonal ya quemados en la imagen).
   El operario (worker-bg.webp, recortado con alpha) va en una capa
   aparte para poder animarlo con parallax independiente del fondo.
   El header es fixed y transparente, asi que el hero reserva su alto
   con padding-top propio. */
.hero-v2{
  position:relative;overflow:hidden;background:#eef1f4;
  min-height:600px;display:flex;align-items:stretch;
}
@media(min-width:1024px){ .hero-v2{min-height:720px;height:calc(100vh - 40px);max-height:900px;} }

.hero-v2__bg{position:absolute;inset:0;z-index:0;}
.hero-v2__bg img{width:100%;height:100%;object-fit:cover;object-position:70% center;}
@media(max-width:1023px){
  .hero-v2__bg::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom, rgba(255,255,255,.92) 0%, rgba(255,255,255,.86) 45%, rgba(255,255,255,.6) 100%);}
}

/* Operario recortado: anclado abajo a la derecha, altura relativa al hero. */
.hero-v2__worker{
  position:absolute;z-index:1;bottom:0;right:0;height:88%;
  display:none;pointer-events:none;
  will-change:transform;
}
.hero-v2__worker img{height:100%;width:auto;object-fit:contain;object-position:bottom right;}
@media(min-width:768px){ .hero-v2__worker{display:block;right:2%;height:82%;} }
@media(min-width:1024px){ .hero-v2__worker{right:8%;height:92%;} }
@media(min-width:1440px){ .hero-v2__worker{right:14%;height:95%;} }

.hero-v2__inner{
  position:relative;z-index:2;width:100%;
  display:flex;align-items:center;
  padding:120px var(--pad) 56px;
}
@media(min-width:1024px){ .hero-v2__inner{padding:140px var(--pad) 64px;} }
@media(min-width:1280px){ .hero-v2__inner{padding-top:150px;} }

.hero-v2__copy{display:flex;flex-direction:column;width:100%;max-width:620px;}
@media(min-width:1024px){ .hero-v2__copy{max-width:52%;} }

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
@media(min-width:1280px){ .hero-v2__copy h1{font-size:58px;margin-bottom:22px;} }
@media(min-width:1600px){ .hero-v2__copy h1{font-size:64px;} }

.hero-v2__lead{font-weight:400;font-size:15px;line-height:1.55;color:#3c4c5c;margin:0 0 28px;max-width:34em;}
@media(min-width:1280px){ .hero-v2__lead{font-size:17px;margin-bottom:34px;} }

/* Los 3 beneficios: cada uno con su icono, en fila desde tablet. */
.hero-v2__benefits{
  list-style:none;margin:0 0 30px;padding:0;
  display:flex;flex-direction:column;gap:16px;
}
@media(min-width:768px){ .hero-v2__benefits{flex-direction:row;gap:0;margin-bottom:36px;} }
.hero-v2__benefits li{
  display:flex;align-items:flex-start;gap:12px;
  font-weight:400;font-size:13px;line-height:1.35;color:var(--navy);
}
@media(min-width:768px){
  .hero-v2__benefits li{flex:1;padding:0 18px;border-left:1px solid rgba(0,53,104,.16);}
  .hero-v2__benefits li:first-child{padding-left:0;border-left:none;}
}
@media(min-width:1280px){ .hero-v2__benefits li{font-size:13.5px;} }
.hero-v2__benefits svg{flex:none;width:30px;height:30px;color:var(--navy);stroke-width:1.4;}

.hero-v2 .ctas{margin-bottom:34px;}
@media(min-width:1280px){ .hero-v2 .ctas{margin-bottom:44px;} }
.hero-v2 .btn{display:inline-flex;align-items:center;gap:10px;}
.hero-v2 .btn svg{width:15px;height:15px;flex:none;}
.hero-v2 .btn--outline{border:2px solid rgba(0,53,104,.35);color:var(--navy);background:rgba(255,255,255,.55);}
.hero-v2 .btn--outline:hover{border-color:var(--navy);background:#fff;}

/* Span de atributos debajo de los botones. */
.hero-v2__tags{
  display:flex;align-items:center;flex-wrap:wrap;gap:10px;
  padding-top:20px;border-top:1px solid rgba(0,53,104,.18);
  font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6b7c;
}
@media(min-width:1280px){ .hero-v2__tags{font-size:12px;gap:12px;} }
.hero-v2__tags .sep{color:rgba(0,53,104,.28);}
.hero-v2__tags img{height:13px;width:auto;display:inline-block;}

/* Bloques verticales sobre la foto (solo desktop). */
.hero-v2__claim{
  position:absolute;z-index:3;right:22px;top:34%;
  display:none;
  font-weight:600;font-size:12px;letter-spacing:.22em;text-transform:uppercase;
  color:rgba(255,255,255,.9);line-height:1.9;text-align:right;
}
@media(min-width:1280px){ .hero-v2__claim{display:block;right:34px;} }
.hero-v2__claim::before{content:"";display:block;width:30px;height:2px;background:var(--orange);margin:0 0 12px auto;}

.hero-v2__pillars{
  position:absolute;z-index:3;right:22px;bottom:9%;
  display:none;flex-direction:column;gap:20px;
}
@media(min-width:1280px){ .hero-v2__pillars{display:flex;right:34px;} }
.hero-v2__pillars li{display:flex;align-items:center;justify-content:flex-end;gap:12px;list-style:none;}
.hero-v2__pillars{margin:0;padding:0;}
.hero-v2__pillars span{
  font-weight:600;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(255,255,255,.92);line-height:1.5;text-align:right;max-width:90px;
}
.hero-v2__pillars svg{width:26px;height:26px;flex:none;color:rgba(255,255,255,.92);stroke-width:1.3;}

"""
s = s[:start] + hero_css + s[end:]

# ---------- 5) HTML: header ----------
hs = s.index('<header class="header">')
he = s.index('</header>') + len('</header>')
header_html = u"""<header class="header" id="siteHeader">
  <a href="#" class="header__logo"><img src="img/logo-blanco.png" alt="Diforza"></a>
  <nav class="nav" id="mainNav">
    <a href="#productos">Productos</a>
    <a href="#industrias">Industrias</a>
    <a href="#empresa">La empresa</a>
    <a href="#contacto">Contacto</a>
  </nav>
  <a href="#contacto" class="btn--nav header__cta">Pedir cotización
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 10h13m0 0l-5-5m5 5l-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </a>
  <button class="nav-toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="mainNav">&#9776;</button>
</header>"""
s = s[:hs] + header_html + s[he:]

# ---------- 6) HTML: hero ----------
hs = s.index('<section class="hero-v2">')
he = s.index('<section class="brands-v2">')
hero_html = u"""<section class="hero-v2">
  <div class="hero-v2__bg">
    <img src="img/hero-bg.webp" alt="" aria-hidden="true" data-parallax="0.12">
  </div>
  <div class="hero-v2__worker hero-anim hero-anim--2" data-parallax="0.28">
    <img src="img/worker-bg.webp" alt="Operario con campera de alta visibilidad Diforza en obra">
  </div>

  <p class="hero-v2__claim hero-anim hero-anim--4">Equipamos<br>el trabajo<br>real</p>

  <ul class="hero-v2__pillars hero-anim hero-anim--5">
    <li>
      <span>Más<br>seguridad</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17h18"/><path d="M5 17a7 7 0 0 1 14 0"/><path d="M10 10.6V5.6a1.6 1.6 0 0 1 1.6-1.6h.8A1.6 1.6 0 0 1 14 5.6v5"/></svg>
    </li>
    <li>
      <span>Más<br>producción</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.8v2.6M12 18.6v2.6M21.2 12h-2.6M5.4 12H2.8M18.5 5.5l-1.8 1.8M7.3 16.7l-1.8 1.8M18.5 18.5l-1.8-1.8M7.3 7.3L5.5 5.5"/></svg>
    </li>
    <li>
      <span>Más<br>confianza</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 20.5h17"/><rect x="4.5" y="12" width="4" height="6"/><rect x="10" y="8" width="4" height="10"/><rect x="15.5" y="4.5" width="4" height="13.5"/></svg>
    </li>
  </ul>

  <div class="hero-v2__inner">
    <div class="hero-v2__copy">
      <p class="hero-v2__eyebrow hero-anim hero-anim--1">+20 años produciendo en Argentina</p>

      <h1 class="hero-anim hero-anim--2">Indumentaria y seguridad <span class="accent">para los que hacen industria</span></h1>

      <p class="hero-v2__lead hero-anim hero-anim--3">Soluciones confiables, diseño funcional y producción nacional para equipos que no se detienen.</p>

      <ul class="hero-v2__benefits hero-anim hero-anim--3">
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.9l8.2 4.3v9.6L12 21.1l-8.2-4.3V7.2z"/><path d="M3.8 7.2L12 11.5l8.2-4.3M12 11.5v9.6"/></svg>
          Stock permanente garantizado
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.8l7.4 2.9v6.1c0 4.3-3.1 7.6-7.4 9.4-4.3-1.8-7.4-5.1-7.4-9.4V5.7z"/><path d="M8.9 11.9l2.2 2.2 4-4.4"/></svg>
          Productos con certificado de fábrica, ensayo o ficha técnica
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8.4" r="3.1"/><path d="M2.9 19.4c0-3.1 2.7-5.2 6.1-5.2s6.1 2.1 6.1 5.2"/><path d="M16.3 5.6a3 3 0 0 1 0 5.7M17.6 14.6c2.1.6 3.5 2.2 3.5 4.5"/></svg>
          Todo lo que necesita tu equipo, en un solo proveedor
        </li>
      </ul>

      <div class="ctas hero-anim hero-anim--4">
        <a href="#contacto" class="btn btn--solid">Pedir cotización
          <svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 10h13m0 0l-5-5m5 5l-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
        <a href="#" class="btn btn--outline">
          <svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v9m0 0l-3.5-3.5M10 12l3.5-3.5M4 15.5h12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Descargar catálogo
        </a>
      </div>

      <p class="hero-v2__tags hero-anim hero-anim--5">
        Protección <span class="sep">/</span> Calidad <span class="sep">/</span> Compromiso <span class="sep">/</span> Industria argentina
        <svg viewBox="0 0 24 15" width="22" height="14" aria-label="Argentina" role="img"><rect width="24" height="15" fill="#74ACDF"/><rect y="5" width="24" height="5" fill="#fff"/><circle cx="12" cy="7.5" r="1.6" fill="#F6B40E"/></svg>
      </p>
    </div>
  </div>
</section>

"""
s = s[:hs] + hero_html + s[he:]

# ---------- 7) JS: navbar sticky + parallax ----------
anchor = "<script>\n(function(){\n  // Scroll-reveal"
assert anchor in s
js = u"""<script>
(function(){
  // Header: transparente sobre el hero, navy solido al scrollear.
  var header = document.getElementById('siteHeader');
  if (header){
    var onScroll = function(){
      if (window.scrollY > 40) header.classList.add('is-stuck');
      else header.classList.remove('is-stuck');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, {passive:true});
  }
})();
(function(){
  // Parallax del hero: fondo y operario se desplazan a distinta velocidad.
  // Se apaga si el usuario pidio menos movimiento o en pantallas chicas.
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var small  = window.matchMedia('(max-width: 767px)').matches;
  if (reduce || small) return;
  var layers = [].slice.call(document.querySelectorAll('.hero-v2 [data-parallax]'));
  if (!layers.length) return;
  var hero = document.querySelector('.hero-v2');
  var ticking = false;
  function update(){
    ticking = false;
    var y = window.scrollY;
    if (y > hero.offsetHeight) return;
    layers.forEach(function(el){
      var k = parseFloat(el.getAttribute('data-parallax')) || 0;
      el.style.transform = 'translate3d(0,' + (y * k).toFixed(2) + 'px,0)';
    });
  }
  window.addEventListener('scroll', function(){
    if (!ticking){ ticking = true; window.requestAnimationFrame(update); }
  }, {passive:true});
  update();
})();
(function(){
  // Scroll-reveal"""
s = s.replace(anchor, js, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK, delta bytes:", len(s) - len(orig))
