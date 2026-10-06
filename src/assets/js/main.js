(function(){
  // Header: transparente sobre el hero, navy solido al scrollear.
  var header = document.getElementById('siteHeader');
  if (header){
    var hero = document.querySelector('[data-js="hero"]');
    var onScroll = function(){
      if (window.scrollY > 40) header.classList.add('is-stuck');
      else header.classList.remove('is-stuck');
      // La copia del operario que va sobre el navbar se desvanece apenas
      // arranca el scroll, sincronizada con el navbar tomando fondo solido.
      if (hero) hero.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, {passive:true});

    // Mide cuanto del operario queda por encima del borde inferior del
    // header y se lo pasa al clip-path. Se recalcula en resize porque
    // header y operario cambian de alto por breakpoint.
    // --nav-h: alto real del header publicado como variable CSS. De ahi
    // sale el padding superior del hero, asi el contenido nunca queda
    // detras del navbar en ninguna altura de pantalla.
    var setNavH = function(){
      document.documentElement.style.setProperty('--nav-h', Math.round(header.offsetHeight) + 'px');
    };
    setNavH();
    window.addEventListener('resize', setNavH, {passive:true});
    window.addEventListener('load', setNavH);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(setNavH);

    var over = hero && hero.querySelector('[data-js="hero-worker-over"]');
    var measure = function(){
      setNavH();
      if (!over) return;
      // offsetTop/offsetHeight en vez de getBoundingClientRect: no los afecta
      // el transform de la animacion de entrada, asi la medida es correcta
      // aunque se tome antes de que el operario termine de entrar.
      var cut = header.offsetHeight - over.offsetTop;
      if (!(cut > 4)){ over.setAttribute('data-over','0'); return; }
      over.removeAttribute('data-over');
      over.style.setProperty('--over-h', Math.round(cut) + 'px');
    };
    measure();
    window.addEventListener('resize', measure, {passive:true});
    window.addEventListener('load', measure);
  }
})();
(function(){
  // Dispara la secuencia de entrada del hero recien cuando la imagen del
  // operario esta decodificada, para que ninguna capa aparezca a destiempo.
  // Si algo falla, un timeout de seguridad muestra todo igual.
  var hero = document.querySelector('[data-js="hero"]');
  if (!hero) return;
  var img = hero.querySelector('[data-js="hero-worker"] img');
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
(function(){
  // Scroll-reveal: activa .is-visible la primera vez que el elemento entra en viewport
  if ('IntersectionObserver' in window){
    var revealEls = document.querySelectorAll('.reveal');
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting){
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, {threshold: 0.15, rootMargin: '0px 0px -40px 0px'});
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('is-visible'); });
  }
})();
(function(){
  // Hace "draggeable" con mouse (y touch nativo) cualquier carrusel con
  // el atributo data-js="drag-carousel" — se usa en el de categorías y en el de productos.
  // El scroll no sigue 1 a 1 al cursor: persigue un target con easing (lerp),
  // y al soltar sigue un poco por inercia (momentum) antes de frenar.
  document.querySelectorAll('[data-js="drag-carousel"]').forEach(function(carousel){
    carousel.style.scrollBehavior = 'auto'; // el easing lo maneja el rAF, no el CSS

    var isDown = false, startX = 0, startScrollLeft = 0, moved = false;
    var current = carousel.scrollLeft, target = carousel.scrollLeft;
    var lastX = 0, lastT = 0, velocity = 0, rafId = null;
    var EASE = 0.18;

    function maxScroll(){ return carousel.scrollWidth - carousel.clientWidth; }
    function clamp(v){ return Math.max(0, Math.min(maxScroll(), v)); }

    function loop(){
      current += (target - current) * EASE;
      if (Math.abs(target - current) < 0.5){ current = target; }
      carousel.scrollLeft = current;
      if (current !== target || isDown){
        rafId = requestAnimationFrame(loop);
      } else {
        rafId = null;
      }
    }
    function startLoop(){ if (!rafId) rafId = requestAnimationFrame(loop); }

    function down(x){
      isDown = true; moved = false;
      carousel.classList.add('is-dragging');
      if (rafId){ cancelAnimationFrame(rafId); rafId = null; }
      current = carousel.scrollLeft;
      target = current;
      startX = x;
      startScrollLeft = current;
      lastX = x; lastT = Date.now(); velocity = 0;
    }
    function move(x){
      if(!isDown) return;
      var walk = x - startX;
      if (Math.abs(walk) > 4) moved = true;
      target = clamp(startScrollLeft - walk);
      var now = Date.now();
      var dt = now - lastT;
      if (dt > 0){ velocity = (x - lastX) / dt; } // px por ms
      lastX = x; lastT = now;
      startLoop();
    }
    function up(){
      if(!isDown) return;
      isDown = false;
      carousel.classList.remove('is-dragging');
      // pequeño impulso de inercia proyectado a partir de la velocidad del gesto
      var momentum = -velocity * 180;
      target = clamp(target + momentum);
      startLoop();
    }

    carousel.addEventListener('mousedown', function(e){ down(e.pageX); });
    window.addEventListener('mouseup', up);
    window.addEventListener('mousemove', function(e){ if(isDown){ e.preventDefault(); move(e.pageX); } });
    carousel.addEventListener('touchstart', function(e){ down(e.touches[0].pageX); }, {passive:true});
    carousel.addEventListener('touchmove', function(e){ move(e.touches[0].pageX); }, {passive:true});
    carousel.addEventListener('touchend', up);
    // evita que un drag termine disparando el click de un link/tarjeta
    carousel.addEventListener('click', function(e){ if(moved){ e.preventDefault(); e.stopPropagation(); } }, true);
  });
})();
(function(){
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('mainNav');
  if(!toggle || !nav) return;
  toggle.addEventListener('click', function(){
    var isOpen = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.textContent = isOpen ? '✕' : '☰';
  });
})();
(function(){
  // Carrusel "spotlight" de categorías (sector 3), infinito: el ítem activo
  // queda centrado y más grande, los vecinos más chicos y difuminados.
  // Para que nunca haya un hueco en los extremos, se clonan un par de ítems
  // a cada punta (suficiente para cubrir la distancia máxima visible, 2).
  // Al cruzar hacia una punta clonada se "teletransporta" sin transición al
  // ítem real equivalente, dando la ilusión de loop infinito.
  //
  // La corrección de posición se dispara con el evento nativo
  // "transitionend" (no con un setTimeout a ciegas): así siempre reacciona
  // al final REAL de la animación, sin importar si el usuario clickeó una
  // vez o encadenó varios clicks rápido. Además, antes de aplicar cualquier
  // click nuevo, la posición se auto-corrige si ya estaba fuera de rango
  // (por ejemplo si el usuario clickeó más rápido de lo que tarda la
  // animación en asentarse) — así "pos" nunca puede alejarse más de un paso
  // de la zona segura, y nunca se sale del array de ítems.
  var root = document.getElementById('catsCarousel');
  if (!root) return;
  var track = document.getElementById('catsTrack');
  var realItems = Array.prototype.slice.call(track.children);
  var N = realItems.length;
  var CLONES = 2; // = distancia máxima visible (data-dist "2")
  var label = document.getElementById('catsLabel');
  var dotsWrap = document.getElementById('catsDots');
  var prevBtn = document.getElementById('catsPrev');
  var nextBtn = document.getElementById('catsNext');

  // arma [clones de las últimas N] + [ítems reales] + [clones de las primeras N]
  var headClones = realItems.slice(N - CLONES).map(function(el){ return el.cloneNode(true); });
  var tailClones = realItems.slice(0, CLONES).map(function(el){ return el.cloneNode(true); });
  headClones.forEach(function(el){ track.insertBefore(el, track.firstChild); });
  tailClones.forEach(function(el){ track.appendChild(el); });

  var items = Array.prototype.slice.call(track.children); // longitud N + 2*CLONES
  var pos = CLONES; // posición extendida; pos-CLONES = índice real activo

  // dots (uno por categoría real)
  var dots = realItems.map(function(item, i){
    var dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'solve__cats-dot';
    dot.setAttribute('aria-label', 'Ir a ' + item.dataset.name);
    dot.addEventListener('click', function(){ goTo(CLONES + i); });
    dotsWrap.appendChild(dot);
    return dot;
  });

  function step(){
    // offsetLeft/offsetWidth ignoran el transform:scale() de cada ítem
    // (getBoundingClientRect no, y eso rompía el centrado según qué ítem
    // estuviera en juego y su escala actual en ese momento).
    if (items.length < 2) return items[0] ? items[0].offsetWidth : 0;
    return items[1].offsetLeft - items[0].offsetLeft;
  }

  function render(){
    var s = step();
    var itemW = items[0].offsetWidth;
    var containerW = root.querySelector('.solve__cats-viewport').clientWidth;
    var offset = (containerW / 2 - itemW / 2) - (pos * s);
    track.style.transform = 'translateX(' + offset + 'px)';

    items.forEach(function(item, i){
      var dist = Math.abs(i - pos);
      item.setAttribute('data-dist', dist >= 3 ? 'far' : String(dist));
    });
    var realIndex = ((pos - CLONES) % N + N) % N;
    dots.forEach(function(dot, i){ dot.classList.toggle('is-active', i === realIndex); });
    label.textContent = items[realIndex + CLONES].dataset.name;
  }

  function jumpInstant(newPos){
    // reubica sin animación (usado para "teletransportar" al ítem real
    // equivalente cuando la posición cae en la zona clonada)
    track.style.transition = 'none';
    pos = newPos;
    render();
    void track.offsetWidth; // fuerza reflow antes de reactivar la transición
    track.style.transition = '';
  }

  function normalize(){
    if (pos >= N + CLONES){ jumpInstant(pos - N); }
    else if (pos < CLONES){ jumpInstant(pos + N); }
  }

  // corrige ANTES de aplicar un nuevo movimiento si "pos" ya había quedado
  // fuera de rango (típico de clicks encadenados más rápido que la animación)
  function settleIfNeeded(){
    if (pos >= N + CLONES || pos < CLONES){
      var real = ((pos - CLONES) % N + N) % N;
      pos = CLONES + real;
    }
  }

  function step_(delta){
    settleIfNeeded();
    pos += delta;
    render();
  }

  function goTo(newPos){
    settleIfNeeded();
    pos = newPos;
    render();
  }

  track.addEventListener('transitionend', function(e){
    if (e.target !== track || e.propertyName !== 'transform') return;
    normalize();
  });

  prevBtn.addEventListener('click', function(){ step_(-1); });
  nextBtn.addEventListener('click', function(){ step_(1); });
  items.forEach(function(item, i){ item.addEventListener('click', function(){ goTo(i); }); });
  window.addEventListener('resize', render);

  render();
})();
(function(){
  // Parallax: el fondo del destacado (spotlight) se mueve, el texto queda fijo/normal
  var section = document.querySelector('[data-js="spotlight"]');
  var bg = section ? section.querySelector('[data-js="spotlight-bg"]') : null;
  if (!section || !bg) return;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  var ticking = false;
  function update(){
    ticking = false;
    var rect = section.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    // progreso: -1 (sector debajo del viewport) .. 1 (sector arriba del viewport)
    var progress = (rect.top + rect.height / 2 - vh / 2) / ((vh + rect.height) / 2);
    progress = Math.max(-1, Math.min(1, progress));
    var shift = progress * 75; // px de recorrido del fondo, texto no se mueve
    bg.style.transform = 'translateY(' + shift.toFixed(1) + 'px)';
  }
  function onScroll(){
    if (!ticking){
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  update();
})();
