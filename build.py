#!/usr/bin/env python3
"""Genera index.html del Garage Sale de DJ BYTE desde products.json + carpeta img/.

Uso:
    python3 build.py

Cuando quieras actualizar el sitio (precios, estado, fotos, items nuevos):
  1) edita products.json (o agrega imagenes a img/ con el patron <key>-<n>.webp/jpg)
  2) corre: python3 build.py
  3) sube los cambios (ver README.md)
"""
import json, os, html, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.djbyte.cl"
WA_NUM = "56988072838"

with open(os.path.join(HERE, "products.json"), encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def group_of(cat):
    c = cat.lower()
    if c.startswith("dj") or "tornamesa" in c: return "dj"
    if "audio" in c or "monitor" in c: return "audio"
    if "camara" in c or "cámara" in c or "video" in c: return "video"
    return "otros"

def price_fmt(p):
    return "$" + format(int(p), ",").replace(",", ".")

WA_SVG = ("<svg viewBox='0 0 24 24' width='15' height='15' fill='currentColor' style='vertical-align:-2px'>"
"<path d='M19.05 4.91A9.82 9.82 0 0 0 12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.86-7.02zM12.04 20.13a8.23 8.23 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.82c0 4.54-3.7 8.23-8.24 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.79.97-.15.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.42h-.48c-.16 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.16 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.22-.17-.47-.29z'/></svg>")
FLOAT_SVG = WA_SVG.replace("width='15' height='15'", "width='28' height='28'")

CSS = r"""
:root{--carbon:#0A0A0A;--carbon2:#141414;--carbon3:#1F1F1F;--ice:#F4F4F1;--pista:#00E5A6;--meta:#A8A8A4;--press:#00B883}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--carbon);color:var(--ice);font-family:'Archivo',system-ui,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
header{position:sticky;top:0;z-index:50;background:rgba(10,10,10,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--carbon3)}
.bar{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:16px;padding:14px 24px}
.bar img{height:28px;width:auto;display:block}.sep{width:1px;height:24px;background:var(--carbon3)}
.gs{font-family:'Archivo Black',sans-serif;text-transform:uppercase;letter-spacing:.02em;font-size:17px}.gs b{color:var(--pista)}
.bar .meta{margin-left:auto;color:var(--meta);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-family:'JetBrains Mono',monospace}
.hero{max-width:1180px;margin:0 auto;padding:72px 24px 24px}
.kicker{color:var(--pista);font-size:12px;letter-spacing:.24em;text-transform:uppercase;margin-bottom:18px;font-family:'JetBrains Mono',monospace}
.hero h1{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:clamp(44px,9vw,104px);line-height:.84;letter-spacing:-.035em}
.hero h1 .p{color:var(--pista)}
.hero p{max-width:560px;margin-top:22px;color:var(--meta);font-size:17px}
.chips{max-width:1180px;margin:0 auto;padding:28px 24px 4px;display:flex;gap:8px;flex-wrap:wrap}
.chip{font-family:'JetBrains Mono',monospace;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--meta);border:1px solid var(--carbon3);padding:7px 14px;border-radius:999px;cursor:pointer;background:none}
.chip.on{color:var(--carbon);background:var(--pista);border-color:var(--pista);font-weight:700}
.grid{max-width:1180px;margin:0 auto;padding:22px 24px 90px;display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:20px}
.card{background:var(--carbon2);border:1px solid var(--carbon3);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;transition:border-color .2s,transform .2s}
.card:hover{border-color:var(--pista);transform:translateY(-3px)}
.media{position:relative;aspect-ratio:4/3;background:#0d0d0d;overflow:hidden}
.gal{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none}
.gal::-webkit-scrollbar{display:none}
.gal img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;scroll-snap-align:center}
.ph{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#171717,#0b0b0b)}
.ph .c{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--meta)}
.nav{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:none;border-radius:50%;background:rgba(10,10,10,.55);color:var(--ice);font-size:18px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s}
.media:hover .nav{opacity:1}.nav.prev{left:8px}.nav.next{right:8px}
.count{position:absolute;bottom:8px;right:8px;background:rgba(10,10,10,.7);color:var(--ice);font-family:'JetBrains Mono',monospace;font-size:10px;padding:2px 7px;border-radius:999px}
.body{padding:16px 16px 18px;display:flex;flex-direction:column;gap:9px;flex:1}
.tag{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--pista)}
.name{font-weight:700;font-size:16px;line-height:1.25}
.price{font-family:'JetBrains Mono',monospace;font-size:21px;font-weight:700;color:var(--ice)}
.desc{color:var(--meta);font-size:13px;flex:1}
.wa{margin-top:6px;display:flex;align-items:center;justify-content:center;gap:8px;background:var(--pista);color:var(--carbon);font-weight:700;text-transform:uppercase;font-size:13px;letter-spacing:.03em;text-decoration:none;padding:12px;border-radius:6px}
.wa:hover{background:var(--press)}
.float{position:fixed;right:22px;bottom:22px;width:56px;height:56px;border-radius:50%;background:var(--pista);color:var(--carbon);display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,.5);text-decoration:none;z-index:60}
footer{border-top:1px solid var(--carbon3);padding:34px 24px;text-align:center;color:var(--meta)}
footer img{height:20px;opacity:.85;margin-bottom:10px}
footer .sig{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.18em;text-transform:uppercase;margin-top:8px}
"""

JS = ("document.querySelectorAll('.chip').forEach(ch=>ch.addEventListener('click',()=>{"
"document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));ch.classList.add('on');"
"const g=ch.dataset.g;document.querySelectorAll('.card').forEach(c=>{c.style.display=(g==='all'||c.dataset.group===g)?'':'none';});}));"
"document.querySelectorAll('.media').forEach(m=>{const gal=m.querySelector('.gal'),cnt=m.querySelector('.count');if(!gal)return;"
"const n=gal.children.length;const pv=m.querySelector('.prev'),nx=m.querySelector('.next');"
"if(nx)nx.addEventListener('click',()=>gal.scrollBy({left:gal.clientWidth,behavior:'smooth'}));"
"if(pv)pv.addEventListener('click',()=>gal.scrollBy({left:-gal.clientWidth,behavior:'smooth'}));"
"if(cnt)gal.addEventListener('scroll',()=>requestAnimationFrame(()=>{const i=Math.round(gal.scrollLeft/gal.clientWidth)+1;cnt.textContent=i+'/'+n;}));});")

def media(images, name):
    if not images:
        return "<div class='ph'><span class='c'>Foto</span></div>"
    imgs = "".join("<img loading='lazy' src='%s' alt='%s'>" % (src, html.escape(name)) for src in images)
    n = len(images)
    extra = ""
    if n > 1:
        extra = ("<button class='nav prev' aria-label='anterior'>&#8249;</button>"
                 "<button class='nav next' aria-label='siguiente'>&#8250;</button>"
                 "<span class='count'>1/%d</span>" % n)
    return "<div class='media'><div class='gal'>%s</div>%s</div>" % (imgs, extra)

cards = []
for p in PRODUCTS:
    fmt = price_fmt(p["price"]); name = p["name"]
    msg = "Hola Byte, me interesa el %s (%s). ¿Sigue disponible?" % (name, fmt)
    wa = "https://wa.me/%s?text=%s" % (WA_NUM, urllib.parse.quote(msg))
    cards.append(
        "<article class='card' data-group='%s'>%s<div class='body'>"
        "<span class='tag'>%s</span><h3 class='name'>%s</h3>"
        "<div class='price'>%s</div><p class='desc'>%s</p>"
        "<a class='wa' href='%s' target='_blank' rel='noopener'>%s Consultar por WhatsApp</a></div></article>"
        % (group_of(p["cat"]), media(p.get("images", []), name),
           html.escape(p["cat"]), html.escape(name), fmt, html.escape(p["desc"]), html.escape(wa), WA_SVG))

wa_float = "https://wa.me/%s?text=%s" % (WA_NUM, urllib.parse.quote("Hola Byte, te escribo por la venta de garage."))
DESC = ("Venta de garage de DJ BYTE: equipo profesional de DJ, estudio y video, usado e impecable "
        "(Technics, Reloop, Focal, HEDD, camaras Sony y mas). Consulta y compra directa por WhatsApp.")
TITLE = "DJ BYTE · Garage Sale — Equipo de DJ, estudio y video"

head = (
"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
"<meta name='viewport' content='width=device-width,initial-scale=1'>"
"<title>%s</title>" % html.escape(TITLE) +
"<meta name='description' content='%s'>" % html.escape(DESC) +
"<link rel='canonical' href='%s/'>" % SITE +
"<meta name='theme-color' content='#0A0A0A'>"
"<link rel='icon' type='image/png' href='icon.png'>"
"<link rel='apple-touch-icon' href='icon.png'>"
"<meta property='og:type' content='website'>"
"<meta property='og:site_name' content='DJ BYTE'>"
"<meta property='og:title' content='%s'>" % html.escape(TITLE) +
"<meta property='og:description' content='%s'>" % html.escape(DESC) +
"<meta property='og:url' content='%s/'>" % SITE +
"<meta property='og:image' content='%s/og-image.jpg'>" % SITE +
"<meta name='twitter:card' content='summary_large_image'>"
"<meta name='twitter:title' content='%s'>" % html.escape(TITLE) +
"<meta name='twitter:description' content='%s'>" % html.escape(DESC) +
"<meta name='twitter:image' content='%s/og-image.jpg'>" % SITE +
"<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
"<link href='https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=Archivo+Black&family=JetBrains+Mono:wght@400;700&display=swap' rel='stylesheet'>"
"<style>" + CSS + "</style></head><body>")

body = (
"<header><div class='bar'><img src='logo.png' alt='DJ BYTE'><div class='sep'></div>"
"<span class='gs'>GARAGE <b>SALE</b></span><span class='meta'>Venta directa · WhatsApp</span></div></header>"
"<section class='hero'><div class='kicker'>DJ BYTE · Equipo de estudio</div>"
"<h1>GARAGE <span class='p'>SALE</span></h1>"
"<p>Equipo profesional de DJ, estudio y video. Mío, cuidado y probado. Lo que ves es lo que hay — consultas y compra directa por WhatsApp.</p></section>"
"<div class='chips'><button class='chip on' data-g='all'>Todo</button><button class='chip' data-g='dj'>DJ</button>"
"<button class='chip' data-g='audio'>Audio</button><button class='chip' data-g='video'>Cámaras / Video</button>"
"<button class='chip' data-g='otros'>Otros</button></div>"
"<main class='grid'>" + "".join(cards) + "</main>"
"<footer><img src='logo.png' alt='DJ BYTE'><div>© 2026 DJ BYTE — Santiago, Chile</div>"
"<div class='sig'>Contacto directo por WhatsApp</div></footer>"
"<a class='float' href='%s' target='_blank' rel='noopener' aria-label='WhatsApp'>%s</a>" % (html.escape(wa_float), FLOAT_SVG) +
"<script>" + JS + "</script></body></html>")

with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(head + body)

print("index.html generado con %d productos." % len(PRODUCTS))
