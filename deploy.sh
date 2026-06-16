#!/usr/bin/env bash
# ---------------------------------------------------------------
# Publica el Garage Sale de DJ BYTE en Cloudflare Pages.
#
# La PRIMERA vez (una sola vez):
#   1) npx wrangler login        # abre el navegador e inicia sesion en tu Cloudflare
#   2) ./deploy.sh               # crea el proyecto y sube el sitio
#   3) En el panel de Cloudflare Pages -> proyecto "djbyte-garage-sale" ->
#      Custom domains -> agrega:  djbyte.cl  y  www.djbyte.cl
#      (Cloudflare crea los DNS solo; eso reemplaza el sitio viejo)
#
# Las VECES siguientes: solo corre  ./deploy.sh
# ---------------------------------------------------------------
set -e
cd "$(dirname "$0")"
npx wrangler@latest pages deploy . --project-name=djbyte-garage-sale --commit-dirty=true
echo ""
echo "Listo. Si es la 1a vez, conecta djbyte.cl y www.djbyte.cl en el panel de Cloudflare Pages."
