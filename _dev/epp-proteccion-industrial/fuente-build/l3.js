
/* ==========================================================================
   L3 · JS propio (el de arriba es el de la home, sin cambios)
   ========================================================================== */
(function(){
  // Marcas [VALIDAR]/[PENDIENTE]: mostrar/ocultar (preferencia por visitante)
  var btn = document.getElementById('phToggle');
  if (!btn) return;
  var root = document.documentElement;
  function apply(off){
    root.classList.toggle('ph-off', off);
    btn.textContent = off ? 'Mostrar marcas' : 'Ocultar marcas';
    btn.setAttribute('aria-pressed', off ? 'true' : 'false');
  }
  var saved = false;
  try { saved = localStorage.getItem('dif-ph-off') === '1'; } catch(e){}
  apply(saved);
  btn.addEventListener('click', function(){
    var off = !root.classList.contains('ph-off');
    apply(off);
    try { localStorage.setItem('dif-ph-off', off ? '1' : '0'); } catch(e){}
  });
})();

(function(){
  // Precarga de producto S5 -> formulario + WhatsApp (doc 17 §17)
  var WA_NUM = '5491159569713'; // [PENDIENTE] número definitivo de Diego (doc 05 §5B)
  var WA_BASE = 'Hola, necesito cotizar EPP para mi empresa.';
  var hidden = document.getElementById('productoInteres');
  var box = document.getElementById('quoting');
  var nameEl = document.getElementById('quotingName');
  var clear = document.getElementById('quotingClear');
  var waLinks = document.querySelectorAll('.js-wa');
  var target = document.getElementById('form-cotizacion-wrap');

  function setWa(text){
    var href = 'https://wa.me/' + WA_NUM + '?text=' + encodeURIComponent(text);
    waLinks.forEach(function(a){ a.href = href; });
  }
  function setProduct(label){
    if (!hidden) return;
    hidden.value = label || '';
    if (label){
      nameEl.textContent = label;
      box.hidden = false;
      setWa('Hola, quiero cotizar ' + label + ' para mi empresa.');
    } else {
      box.hidden = true;
      setWa(WA_BASE);
    }
  }
  document.querySelectorAll('[data-js="consultar"]').forEach(function(b){
    b.addEventListener('click', function(){
      var n = b.getAttribute('data-prod-nombre') || '';
      var c = b.getAttribute('data-prod-codigo') || '';
      setProduct(c ? n + ' (Cód. ' + c + ')' : n);
      // L3: tilda la categoría del producto en el campo multi-selección
      var cat = b.getAttribute('data-prod-cat');
      if (cat){
        var chk = document.querySelector('#form-cotizacion input[name="categorias_epp"][value="' + cat + '"]');
        if (chk){ chk.checked = true; chk.dispatchEvent(new Event('change', {bubbles:true})); }
      }
      if (target) target.scrollIntoView({behavior:'smooth', block:'start'});
    });
  });
  if (clear) clear.addEventListener('click', function(){ setProduct(''); });
  setWa(WA_BASE);
})();

(function(){
  // Catálogo: los CTAs "Descargar catálogo" expanden el form corto (no popup)
  var toggle = document.querySelector('.catalog-l3__toggle');
  var panel = document.getElementById('catalogPanel');
  var wrap = document.getElementById('catalogo');
  if (!toggle || !panel) return;
  function open(v){
    panel.hidden = !v;
    toggle.setAttribute('aria-expanded', v ? 'true' : 'false');
  }
  toggle.addEventListener('click', function(){ open(panel.hidden); });
  document.querySelectorAll('[data-js="catalogo"]').forEach(function(a){
    a.addEventListener('click', function(e){
      e.preventDefault();
      open(true);
      wrap.scrollIntoView({behavior:'smooth', block:'start'});
      setTimeout(function(){ var f = panel.querySelector('input:not([type=hidden]):not([tabindex="-1"])'); if (f) f.focus({preventScroll:true}); }, 600);
    });
  });
})();

(function(){
  // Validación al salir del campo (blur) + envío con estado loading.
  // [PENDIENTE] endpoint propio + webhook al CRM (doc 05 §7, doc 17 §19).
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function fieldOf(el){ return el.closest('.field'); }
  function valid(el){
    if (el.type === 'checkbox') return !el.required || el.checked;
    var v = (el.value || '').trim();
    if (el.required && !v) return false;
    if (el.type === 'email' && v && !EMAIL.test(v)) return false;
    if (el.type === 'tel' && v && v.replace(/\D/g,'').length < 8) return false;
    return true;
  }
  function check(el){
    var f = fieldOf(el); if (!f) return true;
    var ok = valid(el);
    f.classList.toggle('is-invalid', !ok);
    el.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }
  document.querySelectorAll('.js-lead-form').forEach(function(form){
    var inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    inputs.forEach(function(el){
      el.addEventListener('blur', function(){ check(el); });
      // Si el campo ya estaba marcado con error, se re-valida mientras se
      // escribe: asi el error desaparece antes del blur y el layout no se
      // mueve debajo del cursor cuando el usuario hace clic en otro campo.
      var recheck = function(){ if (fieldOf(el) && fieldOf(el).classList.contains('is-invalid')) check(el); };
      el.addEventListener('input', recheck);
      el.addEventListener('change', recheck);
    });
    // L3: grupos de checkboxes obligatorios (al menos uno tildado)
    var groups = form.querySelectorAll('[data-required-group]');
    function checkGroup(g){
      var ok = !!g.querySelector('input[type=checkbox]:checked');
      g.classList.toggle('is-invalid', !ok);
      return ok;
    }
    groups.forEach(function(g){
      g.addEventListener('change', function(){ if (g.classList.contains('is-invalid')) checkGroup(g); });
    });
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var first = null;
      inputs.forEach(function(el){ if (!check(el) && !first) first = el; });
      groups.forEach(function(g){ if (!checkGroup(g) && !first) first = g.querySelector('input'); });
      if (first){ first.focus(); return; }
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) return; // bot
      var btn = form.querySelector('button[type="submit"]');
      var status = form.querySelector('.form-l3__status');
      var label = btn.innerHTML;
      btn.disabled = true; btn.textContent = 'Enviando…';
      // Prototipo: simula el envío. Acá va el fetch al endpoint real; si
      // falla, se conserva lo cargado y se muestra error recuperable.
      setTimeout(function(){
        var isCat = form.id === 'form-catalogo';
        form.innerHTML =
          '<div class="form-l3__ok" role="status">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>' +
          (isCat
            ? '<h3>¡Listo!</h3><p>Te enviamos el catálogo de EPP por email.</p>'
            : '<h3>¡Gracias! Recibimos tu pedido.</h3><p>Un responsable de cuenta te va a contactar para armar la cotización.</p>') +
          '</div>';
      }, 900);
      if (status) status.textContent = '';
      void label;
    });
  });
})();
