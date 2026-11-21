"""Genera la web estática de este repo a partir de sus archivos Markdown.

Uso:
  python3 web/generar.py            reescribe web/ con lo que hay en el repo
  python3 web/generar.py --comprobar  sale con 1 si web/ no está al día

Lee web/sitio.json (título, secciones y archivos) y escribe una página HTML por
cada archivo Markdown, más la portada y una página por sección. No inventa
texto: todo lo que se lee sale de los .md del repo. Los enlaces a otros .md se
convierten en enlaces a sus páginas; los que apuntan a archivos que no son
Markdown (código, Actions, licencia) van a GitHub.

Solo usa la biblioteca estándar de Python 3.
"""
import html, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web"
CFG = json.loads((WEB / "sitio.json").read_text(encoding="utf-8"))
REPO = CFG["repo"]
BLOB = "https://github.com/%s/blob/main/" % REPO
TREE = "https://github.com/%s/tree/main/" % REPO


# ---------- Markdown mínimo: lo que usan los documentos del repo ----------

def idd(texto, usados):
    base = re.sub(r"[^\w\s-]", "", texto.lower(), flags=re.U).strip()
    base = re.sub(r"[\s]+", "-", base) or "seccion"
    i, cand = 1, base
    while cand in usados:
        i += 1
        cand = "%s-%d" % (base, i)
    usados.add(cand)
    return cand


def enlace(dest, origen):
    """Traduce un enlace relativo de un .md (origen) a la web."""
    if re.match(r"^[a-z]+:", dest) or dest.startswith("#"):
        return dest
    dest, _, ancla = dest.partition("#")
    destino = (RAIZ / origen).parent.joinpath(dest).resolve()
    try:
        rel = destino.relative_to(RAIZ).as_posix()
    except ValueError:
        return dest
    if destino.is_dir() or dest.endswith("/"):
        if rel in SECCIONES_DIR:
            obj = SECCIONES_DIR[rel] + "/index.html"
        elif rel == ".":
            obj = "index.html"
        else:
            return TREE + rel
    elif rel in PAGINAS:
        obj = PAGINAS[rel]["html"]
    else:
        return BLOB + rel
    return relativo(PAGINA_ACTUAL[0], obj) + (("#" + ancla) if ancla else "")


def relativo(desde, hasta):
    """Ruta relativa entre dos páginas de la web (rutas tipo nucleo/x.html)."""
    subir = desde.count("/")
    return "../" * subir + hasta


def enlinea(t, origen):
    codigos = []

    def guarda(m):
        codigos.append("<code>%s</code>" % html.escape(m.group(1)))
        return "\x00%d\x00" % (len(codigos) - 1)

    s = re.sub(r"`([^`]+)`", guarda, t)
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: '<a href="%s">%s</a>' % (html.escape(enlace(html.unescape(m.group(2)), origen)), m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w\x00])_([^_\s][^_]*?)_(?![\w])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codigos[int(m.group(1))], s)


def md(texto, origen, sin_h1=True):
    """Devuelve (html, título, lista de h2 con id, primer párrafo)."""
    lineas = texto.replace("\r\n", "\n").split("\n")
    out, usados, h2s = [], set(), []
    titulo, primero = "", ""
    i = 0
    pila = []  # listas abiertas: (tipo, sangría)

    def cierra_listas(hasta=-1):
        while pila and pila[-1][1] > hasta:
            out.append("</li></%s>" % pila.pop()[0])

    parrafo = []

    def vacia_parrafo():
        nonlocal primero
        if parrafo:
            t = " ".join(x.strip() for x in parrafo)
            if not primero:
                primero = t
            out.append("<p>%s</p>" % enlinea(t, origen))
            parrafo.clear()

    while i < len(lineas):
        l = lineas[i]
        if l.startswith("```"):
            vacia_parrafo(); cierra_listas()
            bloque = []
            i += 1
            while i < len(lineas) and not lineas[i].startswith("```"):
                bloque.append(lineas[i]); i += 1
            out.append('<pre tabindex="0"><code>%s</code></pre>' % html.escape("\n".join(bloque)))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            vacia_parrafo(); cierra_listas()
            n, t = len(m.group(1)), m.group(2).strip()
            if n == 1 and not titulo:
                titulo = re.sub(r"[`*]", "", t)
                if not sin_h1:
                    out.append("<h1>%s</h1>" % enlinea(t, origen))
            else:
                limpio = re.sub(r"<[^>]+>", "", enlinea(t, origen))
                ident = idd(html.unescape(limpio), usados)
                nivel = min(n, 4) if n > 1 else 2
                if nivel == 2:
                    h2s.append((ident, html.unescape(limpio)))
                out.append('<h%d id="%s">%s</h%d>' % (nivel, ident, enlinea(t, origen), nivel))
            i += 1
            continue
        if l.startswith("|") and i + 1 < len(lineas) and re.match(r"^\|[\s:|-]+\|?\s*$", lineas[i + 1]):
            vacia_parrafo(); cierra_listas()
            celdas = lambda x: [c.strip() for c in x.strip().strip("|").split("|")]
            cab = celdas(l)
            i += 2
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                filas.append(celdas(lineas[i])); i += 1
            t = ['<div class="tabla" tabindex="0" role="region" aria-label="Tabla"><table><thead><tr>']
            t += ["<th scope=\"col\">%s</th>" % enlinea(c, origen) for c in cab]
            t.append("</tr></thead><tbody>")
            for f in filas:
                t.append("<tr>" + "".join("<td>%s</td>" % enlinea(c, origen) for c in f) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", l)
        if m:
            vacia_parrafo()
            sang = len(m.group(1).expandtabs(4))
            tipo = "ol" if m.group(2)[0].isdigit() else "ul"
            contenido = [m.group(3)]
            i += 1
            # continuación de la misma viñeta
            while i < len(lineas) and lineas[i].strip() and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lineas[i]) \
                    and lineas[i].startswith(" ") and not lineas[i].lstrip().startswith("```"):
                contenido.append(lineas[i].strip()); i += 1
            if pila and sang > pila[-1][1]:
                out.append("<%s>" % tipo); pila.append((tipo, sang))
            else:
                cierra_listas(sang)
                if pila and pila[-1][1] == sang:
                    out.append("</li>")
                else:
                    out.append("<%s>" % tipo); pila.append((tipo, sang))
            out.append("<li>%s" % enlinea(" ".join(contenido), origen))
            continue
        if l.startswith(">"):
            vacia_parrafo(); cierra_listas()
            bloque = []
            while i < len(lineas) and lineas[i].startswith(">"):
                bloque.append(lineas[i].lstrip(">").strip()); i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % enlinea(" ".join(bloque), origen))
            continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", l):
            vacia_parrafo(); cierra_listas(); out.append("<hr>"); i += 1; continue
        if not l.strip():
            vacia_parrafo()
            # una línea en blanco dentro de una lista no la cierra si sigue otra viñeta
            j = i + 1
            while j < len(lineas) and not lineas[j].strip():
                j += 1
            if pila and not (j < len(lineas) and re.match(r"^\s*([-*+]|\d+[.)])\s+", lineas[j])):
                cierra_listas()
            i += 1
            continue
        if pila and l.startswith(" "):
            out.append(" " + enlinea(l.strip(), origen)); i += 1; continue
        cierra_listas()
        parrafo.append(l)
        i += 1
    vacia_parrafo(); cierra_listas()
    return "\n".join(out), titulo, h2s, primero


def secciones_md(texto):
    """Parte un .md por sus h2: {título: texto}."""
    partes, actual = {"": []}, ""
    for l in texto.split("\n"):
        m = re.match(r"^##\s+(.*)$", l)
        if m:
            actual = m.group(1).strip(); partes[actual] = []
        else:
            partes[actual].append(l)
    return {k: "\n".join(v) for k, v in partes.items()}


# ---------- Plantilla ----------

def plantilla(ruta, titulo, cuerpo, descripcion, migas=(), seccion=None, toc=(), pie_extra=""):
    r = lambda x: relativo(ruta, x)
    nav = []
    for s in CFG["secciones"]:
        actual = ' aria-current="page"' if seccion == s["dir"] else ""
        nav.append('<li><a href="%s"%s>%s</a></li>' % (r(s["dir"] + "/index.html"), actual, html.escape(s["nombre"])))
    for e in CFG.get("extras_nav", []):
        actual = ' aria-current="page"' if ruta == PAGINAS[e]["html"] else ""
        nav.append('<li><a href="%s"%s>%s</a></li>' % (r(PAGINAS[e]["html"]), actual, html.escape(PAGINAS[e]["nombre"])))
    miga = ""
    if migas:
        pasos = ['<li><a href="%s">Inicio</a></li>' % r("index.html")]
        for texto, dest in migas:
            pasos.append('<li><a href="%s">%s</a></li>' % (r(dest), html.escape(texto)) if dest
                         else '<li aria-current="page">%s</li>' % html.escape(texto))
        miga = '<nav class="migas" aria-label="Estás en"><ol>%s</ol></nav>' % "".join(pasos)
    indice = ""
    if len(toc) >= 3:
        indice = ('<details class="indice"><summary>En esta página · %d apartados</summary><ol>%s</ol></details>'
                  % (len(toc), "".join('<li><a href="#%s">%s</a></li>' % (i, html.escape(t)) for i, t in toc)))
    titulo_doc = html.escape(titulo if ruta == "index.html" else "%s · %s" % (titulo, CFG["titulo"]))
    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo_doc)s</title>
<meta name="description" content="%(desc)s">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="%(css)s">
</head>
<body>
<a class="saltar" href="#contenido">Ir al contenido</a>
<header class="cabecera">
  <div class="marco cabecera-fila">
    <a class="marca" href="%(inicio)s"><span class="punto" aria-hidden="true"></span>%(marca)s</a>
    <nav aria-label="Secciones"><ul class="menu">%(nav)s</ul></nav>
  </div>
</header>
<main id="contenido" class="marco">
%(migas)s
%(indice)s
%(cuerpo)s
</main>
<footer class="pie">
  <div class="marco pie-fila">
    %(pie_extra)s
    <p>%(licencia)s · <a href="https://github.com/%(repo)s">Código y documentos en GitHub</a></p>
  </div>
</footer>
</body>
</html>
""" % dict(titulo_doc=titulo_doc, desc=html.escape(descripcion[:300]), css=r("estilo.css"), inicio=r("index.html"),
           marca=html.escape(CFG["titulo"]), nav="".join(nav), migas=miga, indice=indice, cuerpo=cuerpo,
           pie_extra=pie_extra, licencia=html.escape(CFG["licencia"]), repo=REPO)


def texto_plano(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return re.sub(r"[`*_]", "", t).strip()


# ---------- Recoger páginas ----------

PAGINAS = {}        # ruta del .md -> {html, nombre, seccion, desc}
SECCIONES_DIR = {}  # carpeta del repo -> carpeta de la web
PAGINA_ACTUAL = ["index.html"]


def recoger():
    for s in CFG["secciones"]:
        SECCIONES_DIR[s["origen"]] = s["dir"]
        carpeta = RAIZ / s["origen"]
        archivos = sorted(p for p in carpeta.rglob("*.md") if p.name != "README.md")
        orden = s.get("orden", [])
        archivos.sort(key=lambda p: (orden.index(p.name) if p.name in orden else len(orden), p.as_posix()))
        s["archivos"] = []
        for p in archivos:
            rel = p.relative_to(RAIZ).as_posix()
            dentro = p.relative_to(carpeta).with_suffix(".html").as_posix()
            texto = p.read_text(encoding="utf-8")
            _, titulo, _, primero = md(texto, rel)
            PAGINAS[rel] = dict(html=s["dir"] + "/" + dentro, nombre=titulo or p.stem, seccion=s["dir"],
                                desc=texto_plano(primero), grupo=p.parent.relative_to(carpeta).as_posix())
            s["archivos"].append(rel)
        readme = carpeta / "README.md"
        if readme.exists():
            PAGINAS[readme.relative_to(RAIZ).as_posix()] = dict(html=s["dir"] + "/index.html", nombre=s["nombre"],
                                                              seccion=s["dir"], desc="", grupo="")
    for e in CFG.get("paginas_sueltas", []):
        texto = (RAIZ / e["origen"]).read_text(encoding="utf-8")
        _, titulo, _, primero = md(texto, e["origen"])
        PAGINAS[e["origen"]] = dict(html=e["html"], nombre=e.get("nombre") or titulo, seccion=None,
                                    desc=texto_plano(primero), grupo="")
    PAGINAS[CFG["portada"]] = dict(html="index.html", nombre="Inicio", seccion=None, desc="", grupo="")


def tarjeta(ruta_actual, rel):
    p = PAGINAS[rel]
    return ('<li class="tarjeta"><a href="%s"><strong>%s</strong><span>%s</span></a></li>'
            % (relativo(ruta_actual, p["html"]), html.escape(p["nombre"]), html.escape(p["desc"][:180])))


def generar():
    recoger()
    salida = {}
    gh = lambda rel: '<a class="boton secundario" href="%s">Ver el archivo en GitHub</a>' % (BLOB + rel)

    # Portada
    PAGINA_ACTUAL[0] = "index.html"
    portada = (RAIZ / CFG["portada"]).read_text(encoding="utf-8")
    partes = secciones_md(portada)
    intro_html, titulo, _, primero = md(partes[""], CFG["portada"])
    bloques = []
    for s in CFG["secciones"]:
        readme = RAIZ / s["origen"] / "README.md"
        desc = s.get("desc", "")
        if readme.exists():
            desc = texto_plano(md(readme.read_text(encoding="utf-8"), s["origen"] + "/README.md")[3])
        n = len(s["archivos"])
        cuenta = ('<span class="cuenta">%s</span>' % html.escape("%d %s" % (n, s.get("unidad", "documentos") if n != 1 else s.get("unidad1", "documento")))) if n else ""
        bloques.append('<li class="tarjeta"><a href="%s/index.html"><strong>%s</strong>%s<span>%s</span></a></li>'
                       % (s["dir"], html.escape(s["nombre"]), cuenta, html.escape(desc[:220])))
    extra_portada = []
    for t in CFG.get("portada_apartados", []):
        if t in partes:
            h, _, _, _ = md("## %s\n%s" % (t, partes[t]), CFG["portada"])
            extra_portada.append('<section class="bloque">%s</section>' % h)
    clonar = ""
    if CFG.get("clonar"):
        clonar = ('<div class="clonar"><p class="etiqueta" id="clonar">Para empezar, clona el repo</p>'
                  '<pre tabindex="0" aria-labelledby="clonar"><code>git clone https://github.com/%s</code></pre></div>' % REPO)
    acciones = '<p class="acciones">'
    for a in CFG.get("acciones", []):
        dest = a["href"] if a["href"].startswith(("http", "#")) else a["href"]
        acciones += '<a class="boton%s" href="%s">%s</a> ' % ("" if a.get("principal") else " secundario", dest, html.escape(a["texto"]))
    acciones += '<a class="boton secundario" href="https://github.com/%s">Ver en GitHub</a></p>' % REPO
    cuerpo = ('<section class="portada"><h1>%s</h1>%s%s%s</section>'
              '<section class="bloque" aria-labelledby="que-hay"><h2 id="que-hay">%s</h2><ul class="tarjetas">%s</ul></section>%s'
              % (html.escape(titulo), intro_html, acciones, clonar, html.escape(CFG.get("titulo_secciones", "Qué hay dentro")),
                 "".join(bloques), "".join(extra_portada)))
    salida["index.html"] = plantilla("index.html", CFG["titulo"], cuerpo, texto_plano(primero))

    # Secciones
    for s in CFG["secciones"]:
        ruta = s["dir"] + "/index.html"
        PAGINA_ACTUAL[0] = ruta
        readme = RAIZ / s["origen"] / "README.md"
        intro, toc, desc = "", [], s.get("desc", "")
        if readme.exists():
            rel = s["origen"] + "/README.md"
            intro, _, toc, primero = md(readme.read_text(encoding="utf-8"), rel)
            desc = texto_plano(primero)
        else:
            intro = "<p>%s</p>" % html.escape(desc)
        grupos = {}
        for rel in s["archivos"]:
            grupos.setdefault(PAGINAS[rel]["grupo"], []).append(rel)
        listas = []
        for g, rels in grupos.items():
            cab = "" if g == "." else "<h3>%s</h3>" % html.escape(s.get("grupos", {}).get(g, g))
            listas.append(cab + '<ul class="tarjetas">%s</ul>' % "".join(tarjeta(ruta, r) for r in rels))
        lista = ('<section class="bloque" aria-labelledby="docs"><h2 id="docs">%s · %d</h2>%s</section>'
                 % (html.escape(s.get("titulo_lista", "Documentos")), len(s["archivos"]), "".join(listas))) if s["archivos"] else ""
        cuerpo = '<h1>%s</h1>%s%s<p class="acciones"><a class="boton secundario" href="%s">Ver la carpeta en GitHub</a></p>' % (
            html.escape(s["nombre"]), intro, lista, TREE + s["origen"])
        salida[ruta] = plantilla(ruta, s["nombre"], cuerpo, desc, migas=[(s["nombre"], None)], seccion=s["dir"],
                                 toc=(toc + ([("docs", s.get("titulo_lista", "Documentos"))] if s["archivos"] else [])) if len(toc) >= 2 else ())

        # Documentos de la sección
        for k, rel in enumerate(s["archivos"]):
            p = PAGINAS[rel]
            PAGINA_ACTUAL[0] = p["html"]
            h, titulo, toc, _ = md((RAIZ / rel).read_text(encoding="utf-8"), rel)
            ant = PAGINAS[s["archivos"][k - 1]] if k > 0 else None
            sig = PAGINAS[s["archivos"][k + 1]] if k + 1 < len(s["archivos"]) else None
            nav = '<nav class="pasos" aria-label="Más en %s">' % html.escape(s["nombre"])
            nav += ('<a class="ant" href="%s"><span>Anterior</span>%s</a>' % (relativo(p["html"], ant["html"]), html.escape(ant["nombre"]))) if ant else "<span></span>"
            nav += ('<a class="sig" href="%s"><span>Siguiente</span>%s</a>' % (relativo(p["html"], sig["html"]), html.escape(sig["nombre"]))) if sig else "<span></span>"
            nav += "</nav>"
            salida_doc = ('<article class="doc"><h1>%s</h1>%s</article>%s<p class="acciones"><a class="boton" href="%s">Volver a %s</a> %s</p>'
                          % (html.escape(titulo or p["nombre"]), h, nav, relativo(p["html"], ruta), html.escape(s["nombre"]), gh(rel)))
            salida[p["html"]] = plantilla(p["html"], titulo or p["nombre"], salida_doc, p["desc"],
                                          migas=[(s["nombre"], ruta), (titulo or p["nombre"], None)], seccion=s["dir"], toc=toc)

    # Páginas sueltas
    for e in CFG.get("paginas_sueltas", []):
        p = PAGINAS[e["origen"]]
        PAGINA_ACTUAL[0] = p["html"]
        h, titulo, toc, _ = md((RAIZ / e["origen"]).read_text(encoding="utf-8"), e["origen"])
        cuerpo = ('<article class="doc"><h1>%s</h1>%s</article><p class="acciones"><a class="boton" href="%s">Volver al inicio</a> %s</p>'
                  % (html.escape(p["nombre"]), h, relativo(p["html"], "index.html"), gh(e["origen"])))
        salida[p["html"]] = plantilla(p["html"], p["nombre"], cuerpo, p["desc"], migas=[(p["nombre"], None)], toc=toc)

    salida["404.html"] = plantilla("404.html", "Página no encontrada",
                                   '<h1>Esta página no existe</h1><p>Puede que se haya movido.</p><p class="acciones"><a class="boton" href="/%s/">Volver al inicio</a></p>' % REPO.split("/")[1],
                                   "Página no encontrada")
    return salida


def main():
    salida = generar()
    comprobar = "--comprobar" in sys.argv
    cambios = []
    for ruta, contenido in sorted(salida.items()):
        destino = WEB / ruta
        if not destino.exists() or destino.read_text(encoding="utf-8") != contenido:
            cambios.append(ruta)
            if not comprobar:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_text(contenido, encoding="utf-8")
    if comprobar:
        if cambios:
            print("web/ no está al día con los .md (%d páginas). Ejecuta: python3 web/generar.py" % len(cambios))
            for c in cambios[:20]:
                print("  " + c)
            sys.exit(1)
        print("web/ al día: %d páginas" % len(salida))
    else:
        print("%d páginas, %d cambiadas" % (len(salida), len(cambios)))


if __name__ == "__main__":
    main()
