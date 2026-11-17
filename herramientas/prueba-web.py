"""Prueba de accesibilidad y móvil para una web estática.

Uso:
  python3 prueba-web.py <raíz del sitio> [prefijo] [opciones]   sirve la carpeta en local y la prueba
  python3 prueba-web.py --url <dirección> [opciones]             prueba una web ya publicada

Opciones:
  --paginas / /otra/ ...   páginas a probar, relativas al prefijo o a --url (por defecto, solo /)
  --selector CSS           bloques de texto que deben caber en la pantalla (por defecto, ninguno)
  --axe RUTA               axe.min.js de axe-core (por defecto, ./node_modules/axe-core/axe.min.js)
  --capturas CARPETA       dónde se guardan las capturas (por defecto, capturas-prueba)
  --puerto N               puerto del servidor local (por defecto, 8771)

Dependencias: playwright para Python con webkit y chromium
(pip install playwright && playwright install --with-deps webkit chromium) y axe-core (npm i axe-core).
Mide WebKit 390x844 y 320x568 y Chromium 1280x800 en cada página.
Sale con código 1 si algo falla: un fallo de axe (WCAG 2.2 AA), desborde horizontal, error de JS,
un recurso propio con error 400 o más, o un bloque de --selector más alto que la pantalla.
Sale con código 2 si no puede hacer la prueba (falta axe, playwright o la raíz).
"""
import argparse, functools, http.server, json, sys, threading
from pathlib import Path

ap = argparse.ArgumentParser(description="Prueba de accesibilidad y móvil para una web estática.")
ap.add_argument("raiz", nargs="?", help="carpeta del sitio, que se sirve en local")
ap.add_argument("prefijo", nargs="?", default="", help="ruta bajo la que cuelga el sitio, por ejemplo /preview/pr7")
ap.add_argument("--url", help="dirección de una web ya publicada, en lugar de una carpeta")
ap.add_argument("--paginas", nargs="+", default=["/"])
ap.add_argument("--selector", default="")
ap.add_argument("--axe", default=str(Path.cwd() / "node_modules/axe-core/axe.min.js"))
ap.add_argument("--capturas", default="capturas-prueba")
ap.add_argument("--puerto", type=int, default=8771)
a = ap.parse_args()

if bool(a.url) == bool(a.raiz):
    ap.error("di una raíz del sitio o --url, una de las dos")
if a.raiz and not Path(a.raiz).is_dir():
    print("No encuentro la raíz del sitio: %s" % a.raiz)
    sys.exit(2)
try:
    AXE = Path(a.axe).read_text()
except OSError:
    print("No encuentro axe-core en %s. Instálalo (npm i axe-core) o pásalo con --axe." % a.axe)
    sys.exit(2)
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Falta playwright: pip install playwright && playwright install --with-deps webkit chromium")
    sys.exit(2)

CAPS = Path(a.capturas); CAPS.mkdir(parents=True, exist_ok=True)
if a.url:
    BASE = a.url.rstrip("/")
    PREFIJO = ""
else:
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x):
            pass
    s = http.server.ThreadingHTTPServer(("127.0.0.1", a.puerto), functools.partial(Silencioso, directory=a.raiz))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    BASE = "http://127.0.0.1:%d" % a.puerto
    PREFIJO = a.prefijo.rstrip("/")

MIDE_TEXTO = ("sel => Math.max(0, ...[...document.querySelectorAll(sel)]"
              ".map(e => e.getBoundingClientRect().height))")
res, fallos = [], 0
with sync_playwright() as p:
    for motor, ancho, alto in (("webkit", 390, 844), ("webkit", 320, 568), ("chromium", 1280, 800)):
        b = getattr(p, motor).launch()
        for pagina in a.paginas:
            u = PREFIJO + "/" + pagina.lstrip("/")
            pg = b.new_page(viewport={"width": ancho, "height": alto})
            errs, malos = [], []
            pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
            pg.on("response", lambda r: malos.append(r.url) if r.status >= 400 and r.url.startswith(BASE) else None)
            resp = pg.goto(BASE + u, wait_until="networkidle")
            if resp is not None and resp.status >= 400 and resp.url not in malos:
                malos.append(resp.url)
            pg.add_script_tag(content=AXE)
            v = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa']})"
                            ".then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))")
            desb = pg.evaluate("document.documentElement.scrollWidth>innerWidth+1")
            texto = pg.evaluate(MIDE_TEXTO, a.selector) if a.selector else 0
            nombre = u.strip("/").replace("/", "_") or "portada"
            pg.screenshot(path=str(CAPS / ("%s_%d_%s.png" % (motor, ancho, nombre))))
            r = dict(motor=motor, ancho=ancho, alto=alto, url=u, axe=v, desborda=desb, errores_js=errs,
                     recursos_con_error=malos, texto_max_px=round(texto))
            r["falla"] = bool(v or desb or errs or malos or texto > alto)
            fallos += r["falla"]
            res.append(r)
            pg.close()
        b.close()
for r in res:
    print(json.dumps(r, ensure_ascii=False))
print("fallos: %d de %d" % (fallos, len(res)))
sys.exit(1 if fallos else 0)
