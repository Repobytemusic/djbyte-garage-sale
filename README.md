# DJ BYTE · Garage Sale — sitio web

Sitio estático (HTML/CSS/JS, sin framework) para la venta de equipo de DJ BYTE.
Marca "Sistema D · Pista". Cada producto abre WhatsApp con mensaje pre-escrito.

## Estructura

- `index.html` — el sitio (generado, no editar a mano).
- `products.json` — **el catálogo** (esto sí se edita): nombre, precio, estado, descripción, fotos.
- `img/` — fotos optimizadas (`<key>-<n>.webp/jpg`) + `logo.png`.
- `build.py` — regenera `index.html` desde `products.json`.
- `deploy.sh` — publica en Cloudflare Pages.
- `_redirects`, `robots.txt`, `sitemap.xml` — config de hosting/SEO.

## Actualizar el catálogo (sin programar)

1. Edita `products.json` (precio, descripción, o borra/agrega un bloque de producto).
   - Para fotos nuevas: déjalas en `img/` con el patrón `nombre-1.webp`, `nombre-2.webp`… y
     agrégalas en la lista `"images"` de ese producto.
2. Corre: `python3 build.py`
3. Publica: `./deploy.sh`  (ver abajo)

> Para sacar un producto vendido: borra su bloque en `products.json` y corre `build.py`.

## Publicar en djbyte.cl (Cloudflare Pages)

**Primera vez (una sola vez, ~2 min):**
1. `npx wrangler login` — abre el navegador, inicia sesión en tu Cloudflare.
2. `./deploy.sh` — crea el proyecto `djbyte-garage-sale` y sube el sitio.
3. En el panel de **Cloudflare → Pages → djbyte-garage-sale → Custom domains**, agrega
   `djbyte.cl` y `www.djbyte.cl`. Cloudflare ajusta el DNS solo y reemplaza el sitio viejo.

**Arreglar el dominio sin www** (hoy `djbyte.cl` sin www da error): al agregar ambos dominios
en Pages queda resuelto; el archivo `_redirects` ya manda `djbyte.cl → www.djbyte.cl`.

**Siguientes veces:** solo `./deploy.sh`.

> Alternativa: conectar el repo público `djbyte-garage-sale` a Cloudflare Pages
> (Pages → Connect to Git) para que cada `git push` despliegue solo.

## Notas

- El número de WhatsApp está en `build.py` (`WA_NUM`).
- El sitio viejo estaba hecho en Lovable (cuenta cerrada); este lo reemplaza y es 100% tuyo.
