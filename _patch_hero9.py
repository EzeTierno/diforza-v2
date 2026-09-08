# -*- coding: utf-8 -*-
import io
P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------------
# 1) CSS de la copia superior
# ---------------------------------------------------------------------
anchor = """.hero-v2__inner{"""
over_css = """/* Copia superior del operario: misma imagen, misma posicion y misma
   animacion de entrada (comparte la clase .hero-v2__worker), pero por
   ENCIMA del header. Un clip-path la recorta para que solo se vea la
   porcion que sobresale sobre la franja del navbar — el resto lo sigue
   dibujando la copia de abajo, asi no hay doble opacidad en los bordes.
   La altura del recorte (--over-h) la mide el JS: es la distancia entre
   el borde superior del operario y el borde inferior del header.
   Al scrollear se desvanece mientras el navbar toma fondo solido; el ojo
   lee las dos transiciones como una sola y no percibe el cambio de capa. */
.hero-v2__worker--over{
  z-index:40;
  clip-path:inset(0 0 calc(100% - var(--over-h, 0px)) 0);
  transition:opacity .2s ease;
}
.hero-v2.is-scrolled .hero-v2__worker--over{opacity:0;}
/* Sin medida util (o header mas alto que el operario) no se dibuja nada */
.hero-v2__worker--over[data-over="0"]{display:none;}

.hero-v2__inner{"""
assert anchor in s
s = s.replace(anchor, over_css, 1)

# ---------------------------------------------------------------------
# 2) HTML: la segunda capa, justo despues de la original
# ---------------------------------------------------------------------
old_html = """  <div class="hero-v2__worker">
    <img src="img/worker-bg.webp" alt="Operario con campera de alta visibilidad Diforza en obra">
  </div>"""
new_html = """  <div class="hero-v2__worker">
    <img src="img/worker-bg.webp" alt="Operario con campera de alta visibilidad Diforza en obra">
  </div>
  <div class="hero-v2__worker hero-v2__worker--over" aria-hidden="true">
    <img src="img/worker-bg.webp" alt="">
  </div>"""
assert old_html in s
s = s.replace(old_html, new_html, 1)

# ---------------------------------------------------------------------
# 3) JS: medir el recorte + marcar el scroll
# ---------------------------------------------------------------------
old_js = """    var onScroll = function(){
      if (window.scrollY > 40) header.classList.add('is-stuck');
      else header.classList.remove('is-stuck');
    };"""
new_js = """    var hero = document.querySelector('.hero-v2');
    var onScroll = function(){
      if (window.scrollY > 40) header.classList.add('is-stuck');
      else header.classList.remove('is-stuck');
      // La copia del operario que va sobre el navbar se desvanece apenas
      // arranca el scroll, sincronizada con el navbar tomando fondo solido.
      if (hero) hero.classList.toggle('is-scrolled', window.scrollY > 8);
    };"""
assert old_js in s
s = s.replace(old_js, new_js, 1)

old_tail = """    onScroll();
    window.addEventListener('scroll', onScroll, {passive:true});
  }
})();"""
new_tail = """    onScroll();
    window.addEventListener('scroll', onScroll, {passive:true});

    // Mide cuanto del operario queda por encima del borde inferior del
    // header y se lo pasa al clip-path. Se recalcula en resize porque
    // header y operario cambian de alto por breakpoint.
    var over = hero && hero.querySelector('.hero-v2__worker--over');
    var measure = function(){
      if (!over) return;
      if (getComputedStyle(over).display === 'none'){ return; }
      var cut = header.getBoundingClientRect().bottom - over.getBoundingClientRect().top;
      if (!(cut > 4)){ over.setAttribute('data-over','0'); return; }
      over.removeAttribute('data-over');
      over.style.setProperty('--over-h', Math.round(cut) + 'px');
    };
    measure();
    window.addEventListener('resize', measure, {passive:true});
    window.addEventListener('load', measure);
  }
})();"""
assert old_tail in s
s = s.replace(old_tail, new_tail, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("OK9")
