import re, os, sys
D = os.path.dirname(os.path.abspath(__file__))
home = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2]

style = re.search(r'<style>(.*?)</style>', home, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', home, re.S).group(1)
style = style.replace('url("img/', 'url("../img/')

css = open(os.path.join(D, 'l2.css'), encoding='utf-8').read()
body = open(os.path.join(D, 'body.html'), encoding='utf-8').read()
js = open(os.path.join(D, 'l2.js'), encoding='utf-8').read()

ARROW = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 10h13m0 0l-5-5m5 5l-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWNLOAD = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v9m0 0l-3.5-3.5M10 12l3.5-3.5M4 15.5h12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg viewBox="0 0 20 20" fill="#fbbc04" aria-hidden="true"><path d="M10 1.5l2.6 5.4 5.9.7-4.4 4.1 1.2 5.9L10 14.7l-5.3 2.9 1.2-5.9-4.4-4.1 5.9-.7L10 1.5z"/></svg>'
GPATHS = '<path fill="#FFC107" d="M43.6 20.5H42V20.4H24v7.2h11.3C33.7 32 29.3 35 24 35c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.1-5.1C33.9 6 29.2 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.2-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6 4.4C13.9 16.1 18.6 13 24 13c3.1 0 5.9 1.2 8 3.1l5.1-5.1C33.9 6.9 29.2 5 24 5c-7.9 0-14.7 4.4-18.2 10.9z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-1.7 13.5-4.8l-6.2-5.2C29.2 35.7 26.7 36.5 24 36.5c-5.3 0-9.7-3.4-11.3-8.1l-6.2 4.8C10 39.5 16.5 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20.4H24v7.2h11.3c-.8 2.2-2.2 4.1-4.1 5.4l6.2 5.2C40.5 35.7 44 30.5 44 24c0-1.2-.1-2.4-.4-3.5z"/>'
GICON = '<svg class="g-icon" viewBox="0 0 48 48" aria-hidden="true">' + GPATHS + '</svg>'
GCARD_G = '<svg class="gcard__g" viewBox="0 0 48 48" aria-hidden="true">' + GPATHS + '</svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
WA_URL = 'https://wa.me/5491159569713?text=Hola%2C%20necesito%20cotizar%20indumentaria%20de%20trabajo%20para%20mi%20empresa.'

# Iconos de prendas (lineales, 24x24)
G = {
 'camisa':   '<path d="M9 3 4 5.5 5.5 10 8 9v12h8V9l2.5 1L20 5.5 15 3l-3 3z"/><path d="M12 6v15M9 3l3 3 3-3"/>',
 'pantalon': '<path d="M7 3h10l1.2 18h-4.4L12 10.5 10.2 21H5.8z"/><path d="M7 6h10"/>',
 'conjunto': '<path d="M8 3h8v5l2.5 1.5V21h-4.5v-7h-4v7H5.5V9.5L8 8z"/><path d="M10 3v4h4V3M8 8h8"/>',
 'campera':  '<path d="M9 3 5 5.2V21h5V11M15 3l4 2.2V21h-5V11"/><path d="M9 3l3 3 3-3M12 6v15M7 14h2.5M14.5 14H17"/>',
 'remera':   '<path d="M8.5 4 3 7l2 4 3-1v10h8V10l3 1 2-4-5.5-3c-.6 1.4-1.9 2.2-3.5 2.2S9.1 5.4 8.5 4z"/>',
 'chomba':   '<path d="M8.5 4 3 7l2 4 3-1v10h8V10l3 1 2-4-5.5-3"/><path d="M8.5 4 12 6.5 15.5 4M12 6.5V10"/>',
 'delantal': '<path d="M9 3h6v4l3.5 2.2V21h-13V9.2L9 7z"/><path d="M5.5 10.5H3M18.5 10.5H21M9 14h6v3.5H9z"/>',
 'altavis':  '<path d="M8 3 5 6v15h5v-8h4v8h5V6l-3-3-2 4h-4z"/><path d="M5 14h5M14 14h5M5 17h5M14 17h5"/>',
 'ignifuga': '<path d="M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2.5 1.5-4 2.5-5 .3 2 1.4 3 2.5 3-.5-3 0-5.5 0-8z"/>',
 'buzo':     '<path d="M8.5 4 3 7.5l2 5.5 3-1.2V21h8v-9.2l3 1.2 2-5.5L15.5 4z"/><path d="M8.5 4h7M12 4v6.5"/>',
 'faja':     '<path d="M3 8.5c3 1 15 1 18 0v7c-3 1-15 1-18 0z"/><path d="M9 9.3v6.4M15 9.3v6.4M11 11h2v2h-2z"/>',
}
def ic(k, extra=''):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (extra, G[k])

LINE = [
 ('camisa','Camisas de trabajo',''),
 ('pantalon','Pantalones y cargos',''),
 ('conjunto','Conjuntos y ambos',''),
 ('campera','Camperas y abrigo',''),
 ('remera','Remeras y chombas',''),
 ('delantal','Delantales y guardapolvos',''),
 ('altavis','Indumentaria de alta visibilidad',''),
 ('ignifuga','Indumentaria ignífuga / especial','<span class="ph">Validar disponibilidad</span>'),
]
line_items = '\n      '.join(
  '<li><span class="line-l2__ic">%s</span><span>%s%s</span></li>' % (ic(k), t, ph) for k,t,ph in LINE)

# 8 destacados (doc 14). img=None -> placeholder con silueta.
# Archivo esperado: prod-<nombre-kebab>.webp en ../img/
# Seleccion definida por el usuario (30/09) con fotos propias 800x800.
# Imagenes normalizadas (recorte + mismo margen) en ./img/ de esta landing.
PRODS = [
 ('Campera trucker Diforza','Azul marino','campera','img/prod-campera-trucker-diforza.webp','top',''),
 ('Buzo polar 1/2 cierre Diforza','','buzo','img/prod-buzo-polar-medio-cierre-diforza.webp',None,''),
 ('Camisa clásica Diforza','Beige','camisa','img/prod-camisa-clasica-diforza.webp',None,''),
 ('Camisa de trabajo Diforza','','camisa','img/prod-camisa-trabajo-diforza.webp',None,''),
 ('Chomba piqué Diforza','Azul marino','chomba','img/prod-chomba-pique-diforza.webp',None,''),
 ('Mameluco con reflectivos Diforza','Azul marino','conjunto','img/prod-pantalon-refl-diforza.webp',None,'Validar nombre'),
 ('Traje de lluvia Diforza','Amarillo','campera','img/prod-traje-lluvia-diforza.webp',None,''),
 ('Traje de bombero Diforza','','ignifuga','img/prod-traje-bombero-diforza.webp',None,'Validar norma'),
]
BADGE_TOP = '<span class="products-v2__badge products-v2__badge--top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.4c1.6 2 2.6 3.4 2.6 4.9a2.6 2.6 0 0 1-5.2 0c0-.9.4-1.7 1-2.5.5 1.2 1.6.9 1.6-2.4z"/></svg> Más vendido</span>'
cards = []
for name, color, k, img, badge, note in PRODS:
    full = name + (' ' + color.lower() if color else '')
    if img:
        media = '<div class="pcard-l2__media"><img src="%s" alt="%s" draggable="false" loading="lazy" width="800" height="800"></div>' % (img, full)
    else:
        media = '<div class="pcard-l2__media is-ph">%s<span class="pcard-l2__phlabel">Foto a reemplazar</span></div>' % ic(k)
    cards.append('''<article class="pcard-l2">
        %s
        %s
        <div class="pcard-l2__body">
          <h3 class="pcard-l2__name">%s%s</h3>
          <p class="pcard-l2__code">%sCód. —<span class="ph">Pendiente</span></p>
          <dl class="pcard-l2__specs">
            <dt>Tela</dt><dd>— <span class="ph">Gramaje / composición</span></dd>
            <dt>Talles</dt><dd>— <span class="ph">Validar</span></dd>
            <dt>Norma</dt><dd>Si aplica</dd>
          </dl>
          <button type="button" class="pcard-l2__cta" data-js="consultar" data-prod-nombre="%s" data-prod-codigo="">Consultar %s</button>
        </div>
      </article>''' % (BADGE_TOP if badge == 'top' else '', media, name, ('<span class="ph">%s</span>' % note) if note else '',
                      (color + ' · ') if color else '', full, ARROW))
products = '\n      '.join(cards)

rep = {'{{ARROW}}':ARROW,'{{DOWNLOAD}}':DOWNLOAD,'{{CHEV}}':CHEV,'{{STAR5}}':STAR*5,
       '{{GICON}}':GICON,'{{GCARD_G}}':GCARD_G,'{{WA_ICON}}':WA_ICON,'{{WA_URL}}':WA_URL,
       '{{LINE_ITEMS}}':line_items,'{{PRODUCTS}}':products}
for a,b in rep.items(): body = body.replace(a,b)
assert '{{' not in body, re.findall(r'\{\{\w+\}\}', body)

head = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indumentaria de Trabajo para Empresas | Diforza</title>
<meta name="description" content="Camisas, pantalones, camperas y conjuntos de trabajo. Talles completos, stock permanente y personalización con el logo de tu empresa.">
<!-- [PENDIENTE] canonical definitivo: https://<dominio>/indumentaria-de-trabajo/ -->
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
