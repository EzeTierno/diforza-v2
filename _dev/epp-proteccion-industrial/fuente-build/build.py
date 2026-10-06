import re, os, sys
D = os.path.dirname(os.path.abspath(__file__))
home = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2]

style = re.search(r'<style>(.*?)</style>', home, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', home, re.S).group(1)
style = style.replace('url("img/', 'url("../img/')

css = open(os.path.join(D, 'l3.css'), encoding='utf-8').read()
body = open(os.path.join(D, 'body.html'), encoding='utf-8').read()
js = open(os.path.join(D, 'l3.js'), encoding='utf-8').read()

ARROW = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 10h13m0 0l-5-5m5 5l-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWNLOAD = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v9m0 0l-3.5-3.5M10 12l3.5-3.5M4 15.5h12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg viewBox="0 0 20 20" fill="#fbbc04" aria-hidden="true"><path d="M10 1.5l2.6 5.4 5.9.7-4.4 4.1 1.2 5.9L10 14.7l-5.3 2.9 1.2-5.9-4.4-4.1 5.9-.7L10 1.5z"/></svg>'
GPATHS = '<path fill="#FFC107" d="M43.6 20.5H42V20.4H24v7.2h11.3C33.7 32 29.3 35 24 35c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.1-5.1C33.9 6 29.2 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.2-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6 4.4C13.9 16.1 18.6 13 24 13c3.1 0 5.9 1.2 8 3.1l5.1-5.1C33.9 6.9 29.2 5 24 5c-7.9 0-14.7 4.4-18.2 10.9z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-1.7 13.5-4.8l-6.2-5.2C29.2 35.7 26.7 36.5 24 36.5c-5.3 0-9.7-3.4-11.3-8.1l-6.2 4.8C10 39.5 16.5 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20.4H24v7.2h11.3c-.8 2.2-2.2 4.1-4.1 5.4l6.2 5.2C40.5 35.7 44 30.5 44 24c0-1.2-.1-2.4-.4-3.5z"/>'
GICON = '<svg class="g-icon" viewBox="0 0 48 48" aria-hidden="true">' + GPATHS + '</svg>'
GCARD_G = '<svg class="gcard__g" viewBox="0 0 48 48" aria-hidden="true">' + GPATHS + '</svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
WA_URL = 'https://wa.me/5491159569713?text=Hola%2C%20necesito%20cotizar%20EPP%20para%20mi%20empresa.'

# Iconos de categorias de EPP (lineales, 24x24)
G = {
 'craneal':     '<path d="M3 17h18"/><path d="M5 17a7 7 0 0 1 14 0"/><path d="M10 10.6V5.6a1.6 1.6 0 0 1 1.6-1.6h.8A1.6 1.6 0 0 1 14 5.6v5"/>',
 'auditiva':    '<path d="M5 14v-3a7 7 0 0 1 14 0v3"/><rect x="3" y="13" width="4.5" height="7.5" rx="2.2"/><rect x="16.5" y="13" width="4.5" height="7.5" rx="2.2"/>',
 'ocular':      '<circle cx="6.5" cy="14" r="3.5"/><circle cx="17.5" cy="14" r="3.5"/><path d="M10 14h4M3.2 12.6 5 8M20.8 12.6 19 8"/>',
 'facial':      '<path d="M5 5h14v8.5a7 7 0 0 1-14 0z"/><path d="M3.5 5h17M9 9.5h6"/>',
 'respiratoria':'<path d="M6 9c2.5-2.2 9.5-2.2 12 0l-1 6.5c-1.2 3.3-8.8 3.3-10 0z"/><path d="M6 10 2.5 8M18 10l3.5-2"/><circle cx="12" cy="13" r="2"/>',
 'manos':       '<path d="M8 21v-3.5L4.6 13a1.6 1.6 0 0 1 2.5-2L8.5 12.5V5.5a1.5 1.5 0 0 1 3 0V11V4a1.5 1.5 0 0 1 3 0v7V5.5a1.5 1.5 0 0 1 3 0V16c0 2.8-2 5-4.8 5z"/>',
 'anticaida':   '<path d="M8.5 9V6.5a3.5 3.5 0 0 1 7 0V17a3.5 3.5 0 0 1-7 0v-4"/><path d="M6.5 9h4"/><path d="M12 3v0"/>',
 'vialidad':    '<path d="M9.8 4h4.4l4.3 15H5.5z"/><path d="M8.2 10h7.6M6.9 14.5h10.2M3 19h18"/>',
}
def ic(k, extra=''):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (extra, G[k])

# S4 · categoria + alcance (copy literal doc 04c)
CATS = [
 ('craneal','Craneal','Cascos, barbijos de casco, accesorios — línea Libus completa'),
 ('auditiva','Auditiva','Endoaurales, de copa, con arnés'),
 ('ocular','Ocular','Antiparras, lentes de seguridad, filtros'),
 ('facial','Facial','Máscaras, protectores faciales, soldadura'),
 ('respiratoria','Respiratoria','Semimáscaras, máscaras, filtros y descartables'),
 ('manos','Manos','Guantes según riesgo mecánico, químico, térmico y de corte'),
 ('anticaida','Anticaída','Arneses, cabos de vida, líneas y accesorios'),
 ('vialidad','Vialidad y señalización','Alta visibilidad, conos, señalización'),
]
cat_items = '\n      '.join(
  '<li><span class="line-l3__ic">%s</span><span class="line-l3__txt"><strong>%s</strong><small>%s</small></span></li>' % (ic(k), t, d) for k,t,d in CATS)

# Formulario · campo variable L3 (doc 05 §3): chips multi-seleccion
CHECKS = [('craneal','Craneal'),('auditiva','Auditiva'),('ocular','Ocular'),('facial','Facial'),
          ('respiratoria','Respiratoria'),('manos','Manos'),('anticaida','Anticaída'),('vialidad','Vialidad')]
cat_checks = '\n              '.join(
  '<label class="chip-l3"><input type="checkbox" name="categorias_epp" value="%s" data-cat="%s"><span>%s</span></label>' % (t, k, t) for k,t in CHECKS)

# 8 destacados por ventas reales ene-jun 2026 (doc 14 / doc 04c S5), en ese orden.
# (nombre, variante, marca, nota_marca, norma, icono/categoria, img, badge, nota_foto)
# img=None -> placeholder con icono. Fotos 800x800 normalizadas (30/09); falta respirador definitivo.
PRODS = [
 ('Anteojo Argon','Transparente HC','Libus','','ocular','img/prod-anteojo-argon.webp','top',''),
 ('Anteojo Eco-line','Transparente HC','Libus','','ocular','img/prod-anteojo-ecoline.webp',None,''),
 ('Protector auditivo Quantum','','Libus','','auditiva','img/prod-auditivo-quantum.webp',None,''),
 ('Protector auditivo Alternative','Vincha','—','Validar marca','auditiva','img/prod-protector-auditivo-alternative.webp',None,''),
 ('Casco Milenium','Amarillo y blanco','Libus','','craneal','img/prod-casco-milenium.webp',None,''),
 ('Arnés a cremallera plástico','Para casco','Libus','','craneal','img/prod-arnes-a-cremallera-plastico.webp',None,''),
 ('Arnés completo con toma frontal y faja lumbar','','Skiway','Validar marca','anticaida','img/prod-arnes-completo.webp',None,''),
 ('Respirador desechable 522','FFP2 NR D','—','Validar marca','respiratoria','img/prod-respirador.webp',None,'Foto provisoria'),
]
CAT_LABEL = dict(CHECKS)
BADGE_TOP = '<span class="products-v2__badge products-v2__badge--top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.4c1.6 2 2.6 3.4 2.6 4.9a2.6 2.6 0 0 1-5.2 0c0-.9.4-1.7 1-2.5.5 1.2 1.6.9 1.6-2.4z"/></svg> Más vendido</span>'
cards = []
for name, variant, brand, bnote, k, img, badge, pnote in PRODS:
    full = name + (' ' + variant if variant else '')
    if img:
        media = '<div class="pcard-l3__media"><img src="%s" alt="%s" draggable="false" loading="lazy">%s</div>' % (
            img, full, ('<span class="pcard-l3__phlabel">%s</span>' % pnote) if pnote else '')
    else:
        media = '<div class="pcard-l3__media is-ph">%s<span class="pcard-l3__phlabel">Foto a reemplazar</span></div>' % ic(k)
    cards.append('''<article class="pcard-l3">
        %s
        %s
        <div class="pcard-l3__body">
          <h3 class="pcard-l3__name">%s</h3>
          <p class="pcard-l3__code">%sCód. —<span class="ph">Pendiente</span></p>
          <dl class="pcard-l3__specs">
            <dt>Marca</dt><dd>%s%s</dd>
            <dt>Norma</dt><dd class="pcard-l3__norm">— <span class="ph">Pendiente norma</span></dd>
          </dl>
          <button type="button" class="pcard-l3__cta" data-js="consultar" data-prod-nombre="%s" data-prod-codigo="" data-prod-cat="%s">Consultar %s</button>
        </div>
      </article>''' % (BADGE_TOP if badge == 'top' else '', media, name,
                      (variant + ' · ') if variant else '', brand, ('<span class="ph">%s</span>' % bnote) if bnote else '',
                      full, CAT_LABEL[k], ARROW))
products = '\n      '.join(cards)

CHEV24 = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'

rep = {'{{ARROW}}':ARROW,'{{DOWNLOAD}}':DOWNLOAD,'{{CHEV}}':CHEV,'{{CHEV24}}':CHEV24,'{{STAR5}}':STAR*5,
       '{{GICON}}':GICON,'{{GCARD_G}}':GCARD_G,'{{WA_ICON}}':WA_ICON,'{{WA_URL}}':WA_URL,
       '{{CAT_ITEMS}}':cat_items,'{{CAT_CHECKS}}':cat_checks,'{{PRODUCTS}}':products}
for a,b in rep.items(): body = body.replace(a,b)
assert '{{' not in body, re.findall(r'\{\{\w+\}\}', body)

head = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EPP Certificado para Industria | Diforza</title>
<meta name="description" content="Protección craneal, auditiva, ocular, respiratoria y de manos con certificación IRAM. Stock permanente y asesoramiento por puesto de trabajo.">
<!-- [VALIDAR] title y description mencionan certificación: sujetos a confirmación de Diforza (doc 06 §4) -->
<!-- [PENDIENTE] canonical definitivo: https://<dominio>/epp-proteccion-industrial/ -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<style>'''
html = head + style.rstrip() + '\n' + css + '</style>\n</head>\n<body>\n' + body + '\n<script>' + script.rstrip() + '\n' + js + '</script>\n</body>\n</html>\n'
# Carpeta autocontenida para subir: todas las imagenes viven en ./img/
# (las compartidas con la home se copian ahi), sin rutas ../img/
html = html.replace('../img/', 'img/')
assert '../img/' not in html
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(html)
print('ok', len(html))
