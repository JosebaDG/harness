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
un recurso propio con error 400 o más, texto tapado por otro elemento (por ejemplo, un número de lista
encima de una palabra), o un bloque de --selector más alto que la pantalla.

Texto tapado: recorre la página pantalla a pantalla y, en tres puntos de cada línea de texto visible,
pregunta qué elemento queda encima. Si es otro (ni el del texto, ni uno de dentro, ni uno que lo
contiene), lo cuenta como solape. Salta el texto que no se ve (un details cerrado, visibility: hidden). No cuenta lo que tapa una cabecera fija o pegajosa al bajar.
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
TAPADO = r"""() => {
  const fijo = (e) => { for (; e && e !== document.body; e = e.parentElement) {
      const p = getComputedStyle(e).position; if (p === "fixed" || p === "sticky") return e; } return null; };
  const quien = (e) => e.tagName.toLowerCase() + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).join(".") : "");
  const vistos = new Set(), salida = [], H = innerHeight, W = innerWidth, alto = document.documentElement.scrollHeight;
  for (let y = 0; y < alto; y += Math.max(200, Math.floor(H * 0.8))) {
    scrollTo(0, y);
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const el = n.parentElement;
      if (!n.textContent.trim() || !el || el.closest("svg, script, style, noscript, [aria-hidden=true] svg")) continue;
      const cerrado = el.closest("details:not([open])");
      if (cerrado && !el.closest("summary")) continue;
      if (el.checkVisibility && !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === "hidden" || +cs.opacity === 0) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) {
        if (r.width < 4 || r.height < 4 || r.bottom <= 0 || r.top >= H) continue;
        const cy = r.top + r.height / 2;
        for (const cx of [r.left + 2, r.left + r.width / 2, r.right - 2]) {
          if (cx < 0 || cx >= W || cy < 0 || cy >= H) continue;
          const h = document.elementFromPoint(cx, cy);
          if (!h || h === el || el.contains(h) || h.contains(el)) continue;
          const f = fijo(h); if (f && !f.contains(el)) continue;
          const clave = quien(el) + "|" + quien(h) + "|" + n.textContent.trim().slice(0, 30);
          if (!vistos.has(clave)) { vistos.add(clave); salida.push("«" + n.textContent.trim().slice(0, 30) + "» (" + quien(el) + ") bajo " + quien(h)); }
        }
      }
    }
  }
  scrollTo(0, 0);
  return salida.slice(0, 10);
}"""
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
            tapado = pg.evaluate(TAPADO)
            nombre = u.strip("/").replace("/", "_") or "portada"
            pg.screenshot(path=str(CAPS / ("%s_%d_%s.png" % (motor, ancho, nombre))))
            r = dict(motor=motor, ancho=ancho, alto=alto, url=u, axe=v, desborda=desb, errores_js=errs,
                     recursos_con_error=malos, texto_tapado=tapado, texto_max_px=round(texto))
            r["falla"] = bool(v or desb or errs or malos or tapado or texto > alto)
            fallos += r["falla"]
            res.append(r)
            pg.close()
        b.close()
for r in res:
    print(json.dumps(r, ensure_ascii=False))
print("fallos: %d de %d" % (fallos, len(res)))
sys.exit(1 if fallos else 0)
