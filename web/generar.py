"""Genera la web estática de este repo a partir de sus archivos Markdown.

Uso:
  python3 web/generar.py            reescribe web/ con lo que hay en el repo
  python3 web/generar.py --comprobar  sale con 1 si web/ no está al día
                                      (páginas que faltan, distintas o huérfanas)

Páginas huérfanas: los .html de web/ que ya no salen de ningún .md, por ejemplo
al renombrar o quitar un archivo. Al generar se borran; solo dentro de web/ y
solo .html, que aquí los escribe todos el generador. Nada fuera de web/.

Lee web/sitio.json (título, secciones y archivos) y escribe una página HTML por
cada archivo Markdown, más la portada y una página por sección. No inventa
texto: todo lo que se lee sale de los .md del repo. Los enlaces a otros .md se
convierten en enlaces a sus páginas; los que apuntan a archivos que no son
Markdown (código, Actions, licencia) van a GitHub.

Solo usa la biblioteca estándar de Python 3.
"""
import hashlib, html, json, math, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web"
CFG = json.loads((WEB / "sitio.json").read_text(encoding="utf-8"))
REPO = CFG["repo"]
BLOB = "https://github.com/%s/blob/main/" % REPO
TREE = "https://github.com/%s/tree/main/" % REPO
VARIANTE = CFG.get("variante", "harness")
# La versión de la hoja de estilos y del script va en su dirección: una página guardada en la caché del
# navegador sigue con su hoja de entonces y no mezcla una página vieja con un estilo nuevo.
VERSION = hashlib.sha1(b"".join((WEB / n).read_bytes() for n in ("estilo.css", "portada.js") if (WEB / n).exists())).hexdigest()[:8]
CASA = CFG.get("casa", {"nombre": "The Singularity", "url": "https://josebadg.github.io/"})


# ---------- Lo visual: colores, iconos e ilustraciones (sin texto de los .md) ----------

# Los colores salen de la web principal (portada/punto.css): oro, azul, turquesa, rosa y ámbar.
COLORES = ["#a2bcff", "#47d6cf", "#f89dc9", "#e6b55d", "#f3cf96"]

ICONOS = {
    "nucleo": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.6" class="lleno"/>',
    "herramientas": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><path d="M7 10l3 2.5L7 15M12.5 15.5H17"/>',
    "especialistas": '<path d="M4 15.5c0-4.5 3.6-8 8-8s8 3.5 8 8"/><path d="M2.5 15.5h19"/><path d="M12 7.5V4.5"/><circle cx="12" cy="3.6" r="1.1" class="lleno"/>',
    "flujos": '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="5" cy="18" r="2"/><path d="M7 6c6 0 6 6 10 6M7 18c6 0 6-6 10-6"/>',
    "ejemplos": '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="2.4" class="lleno"/>',
    "conceptos": '<circle cx="6" cy="7" r="2.2"/><circle cx="18" cy="7" r="2.2"/><circle cx="12" cy="17.5" r="2.2"/><path d="M8 8.2l2.8 7.2M16 8.2l-2.8 7.2M8.2 7h7.6"/>',
    "fuentes": '<path d="M6 3.5h9l3.5 3.5v13.5H6z"/><path d="M15 3.5V7h3.5M9 11h6.5M9 14h6.5M9 17h4"/>',
}
ICONO_OTRO = '<rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="12" cy="12" r="1.6" class="lleno"/>'


def icono(clave, clase="icono"):
    return ('<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
            % (clase, ICONOS.get(clave, ICONO_OTRO)))


def color_seccion(dir_):
    for i, s in enumerate(CFG["secciones"]):
        if s["dir"] == dir_:
            return s.get("color") or COLORES[i % len(COLORES)]
    return COLORES[-1]


def isotipo():
    """El punto de la familia: el de la web principal, con el color de este sitio alrededor."""
    if VARIANTE == "wiki":
        dentro = ('<rect x="9" y="16" width="5" height="18" rx="1.5" fill="#a2bcff"/>'
                  '<rect x="16" y="11" width="5" height="23" rx="1.5" fill="#47d6cf"/>'
                  '<rect x="23" y="14" width="5" height="20" rx="1.5" fill="#f89dc9" transform="rotate(-12 25.5 34)"/>'
                  '<circle cx="31" cy="9" r="3.2" fill="#fff" class="iso-punto"/>')
    else:
        dentro = ('<circle cx="20" cy="20" r="13" fill="none" stroke="#f3cf96" stroke-width="1.6" stroke-dasharray="2 3.4"/>'
                  '<circle cx="20" cy="7" r="3" fill="#a2bcff"/><circle cx="33" cy="20" r="3" fill="#47d6cf"/>'
                  '<circle cx="20" cy="33" r="3" fill="#f89dc9"/><circle cx="7" cy="20" r="3" fill="#e6b55d"/>'
                  '<circle cx="20" cy="20" r="3.6" fill="#fff" class="iso-punto"/>')
    return '<svg class="iso" viewBox="0 0 40 40" aria-hidden="true" focusable="false">%s</svg>' % dentro


# ---------- La escena viva de la portada ----------
# El fotograma quieto sale de aquí con la misma geometría que escena.js usa en t=0, para que la página
# se vea bien sin JavaScript y con «reducir movimiento». escena.js anima los mismos elementos.

TAU = 2 * math.pi
R0, T0 = 0.35, 0.42          # harness: giro inicial y relevo en vuelo del primer agente al segundo
TW0 = 5.95                   # wiki: el punto acaba de llegar al séptimo libro


def _f(n):
    v = round(n * 10) / 10
    return ("%d" % v) if v == int(v) else ("%.1f" % v)


def _suave(x):
    x = min(1, max(0, x))
    return x * x * (3 - 2 * x)


def escena_harness(colores):
    C = (180, 150)
    s, rot, flujo, golpe = 0.0, R0, 0.0, 0.0
    k, p = int(math.floor(T0)), T0 - math.floor(T0)
    viaje = _suave(p / 0.55)
    activo = k % 4

    def pozo(u):
        rx = 26 + u * 150
        return rx, rx * 0.3, C[1] - 44 * (u ** 0.8)

    anillos = []
    for i in range(7):
        u = ((i + flujo) / 7) % 1
        rx, ry, cy = pozo(u)
        anillos.append('<ellipse class="anillo" cx="180" cy="%s" rx="%s" ry="%s" stroke-opacity="%.3f"/>'
                       % (_f(cy), _f(rx), _f(ry), 0.55 * math.sin(math.pi * u)))
    radios = []
    for i in range(12):
        fi = i / 12 * TAU + rot * 0.25
        d = ""
        for j in range(9):
            u = 0.06 + j / 8 * 0.94
            rx, ry, cy = pozo(u)
            d += ("L" if j else "M") + _f(C[0] + rx * math.cos(fi)) + " " + _f(cy + ry * math.sin(fi))
        radios.append('<path class="radio" d="%s"/>' % d)

    ox, oy, orx, ory = 180, 124, 122, 34
    en = lambda th: (ox + orx * math.cos(th), oy + ory * math.sin(th), math.sin(th))
    detras, delante, pos = [], [], []
    for i in range(4):
        x, y, z = en(rot + i * TAU / 4)
        pos.append((x, y))
        esc = 0.72 + 0.4 * (z + 1) / 2
        on = i == activo
        g = ('<g class="agente" data-color="%s" opacity="%.3f">'
             '<circle class="aura" cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/>'
             '<circle class="llamada" cx="%s" cy="%s" r="%s" stroke="%s" stroke-opacity="0"/>'
             '<circle class="nucleo" cx="%s" cy="%s" r="%s" fill="%s"/></g>'
             % (colores[i], 0.55 + 0.45 * (z + 1) / 2,
                _f(x), _f(y), _f(9 * esc * (2.6 if on else 1.7)), colores[i], "0.3" if on else "0.12",
                _f(x), _f(y), _f(9 * esc), colores[i],
                _f(x), _f(y), _f(9 * esc * (1.18 if on else 1)), colores[i]))
        (delante if z > 0 else detras).append(g)

    th0 = rot + k * TAU / 4
    th = th0 + viaje * TAU / 4
    d = ""
    a0 = max(th0, th - 0.95)
    for j in range(11):
        x, y, _ = en(a0 + j / 10 * (th - a0))
        d += ("L" if j else "M") + _f(x) + " " + _f(y)
    hx, hy, _ = en(th)
    pa = pos[activo]
    defs = ('<defs><radialGradient id="e-halo"><stop offset="0" stop-color="#f3cf96" stop-opacity=".55"/>'
            '<stop offset="1" stop-color="#f3cf96" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="e-suelo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3cf96" stop-opacity=".08"/>'
            '<stop offset="1" stop-color="#f3cf96" stop-opacity="0"/></linearGradient></defs>')
    return (defs
            + '<ellipse class="suelo" cx="180" cy="132" rx="176" ry="80" fill="url(#e-suelo)"/>'
            + '<g class="pozo">' + "".join(radios) + "".join(anillos) + '</g>'
            + '<ellipse class="via" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (ox, oy, orx, ory)
            + '<g class="detras">' + "".join(detras) + '</g>'
            + '<line class="lazo" x1="%s" y1="%s" x2="180" y2="150" stroke="%s" stroke-opacity="0.45"/>' % (_f(pa[0]), _f(pa[1]), colores[activo])
            + '<circle class="halo" cx="180" cy="150" r="40" fill="url(#e-halo)"/>'
            + '<circle class="onda" cx="180" cy="150" r="11" stroke-opacity="0"/>'
            + '<circle class="punto" cx="180" cy="150" r="11"/>'
            + '<g class="delante">' + "".join(delante) + '</g>'
            + '<path class="estela" d="%s" stroke-opacity="0.85"/>' % d
            + '<circle class="cabeza" cx="%s" cy="%s" r="4.5"/>' % (_f(hx), _f(hy)))


def escena_wiki(colores):
    # Libros: x, ancho, alto, color. El último es el hueco que se llena.
    xs, libros, x = [], [], 34
    alturas = [92, 118, 80, 104, 126, 88, 112, 98, 120, 108]
    anchos = [24, 20, 28, 22, 18, 26, 22, 20, 24, 24]
    for i, (h, w) in enumerate(zip(alturas, anchos)):
        libros.append((x, w, h, colores[i % len(colores)]))
        x += w + 6
    n = len(libros) - 1
    estante = 246
    t = TW0
    j, q = int(t), t - int(t)
    qe = _suave(q)
    cen = lambda i: libros[i][0] + libros[i][1] / 2
    cima = lambda i: estante - libros[i][2]
    px = cen(j) + (cen(j + 1) - cen(j)) * qe
    py = (cima(j) - 18) + ((cima(j + 1) - 18) - (cima(j) - 18)) * qe - 30 * math.sin(math.pi * q)
    out = []
    for i, (bx, w, h, c) in enumerate(libros):
        alza, op = 0, (0.88 if i % 2 else 0.6)
        if i == n:
            h2, op = 0, 0
        else:
            h2 = h
            if abs(cen(i) - px) < w / 2 + 3:
                alza, op = 6, 1
        y = estante - h2 - alza
        out.append('<g class="libro" data-x="%s" data-w="%s" data-h="%s"><rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="%s" fill-opacity="%.3f"/>'
                   '<line x1="%s" x2="%s" y1="%s" y2="%s" stroke-opacity="%s"/></g>'
                   % (bx, w, h, bx, _f(y), w, _f(h2), c, op, bx + 5, bx + w - 5, _f(y + 16), _f(y + 16), "0.45" if h2 > 20 else "0"))
    hx, hw, hh, _ = libros[n]
    actual = j + 1
    otro = actual - 2 - (actual % 3)
    xa, xb, ya, yb = cen(otro), cen(actual), cima(otro) - 4, cima(actual) - 4
    alto = min(ya, yb) - 26 - 4 * (actual - otro)
    return ('<defs><radialGradient id="e-luz"><stop offset="0" stop-color="#f3cf96" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#f3cf96" stop-opacity="0"/></radialGradient></defs>'
            + '<ellipse class="luz" cx="%s" cy="250" rx="26" ry="9" fill="url(#e-luz)"/>' % _f(px)
            + "".join(out)
            + '<rect class="hueco" x="%s" y="%s" width="%s" height="%s" rx="3" stroke-opacity="0.5"/>' % (hx + 1, estante - hh + 1, hw - 2, hh - 2)
            + '<line class="tabla" x1="22" y1="%s" x2="338" y2="%s"/>' % (estante + 2, estante + 2)
            + '<path class="arco" d="M%s %sQ%s %s %s %s" stroke="%s" stroke-opacity="0" stroke-dasharray="60"/>'
            % (_f(xa), _f(ya), _f((xa + xb) / 2), _f(alto), _f(xb), _f(yb), libros[actual][3])
            + '<circle class="onda" cx="%s" cy="%s" r="6.5" stroke-opacity="0"/>' % (_f(px), _f(py))
            + '<circle class="punto" cx="%s" cy="%s" r="6.5"/>' % (_f(px), _f(py)))


def ilustracion():
    colores = list(COLORES[:4])
    wiki = VARIANTE == "wiki"
    if wiki:
        cuerpo, vb, attrs = escena_wiki(colores), "0 16 360 248", ' data-escena="wiki" data-turnos="%s"' % TW0
    else:
        while len(colores) < 4:
            colores.append(colores[-1])
        cuerpo, vb, attrs = escena_harness(colores[:4]), "0 22 360 220", ' data-escena="harness" data-rot="%s" data-turnos="%s"' % (R0, T0)
    return ('<figure class="escena-caja">'
            '<svg viewBox="%s" aria-hidden="true" focusable="false"%s>%s</svg>'
            '<button type="button" class="escena-pausa" aria-pressed="false" aria-label="Pausar la animación" hidden>'
            '<span aria-hidden="true"></span></button></figure>' % (vb, attrs, cuerpo))


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
        miga = '<nav class="migas" aria-label="Estás en"><ol class="migas-lista">%s</ol></nav>' % "".join(pasos)
    indice = ""
    if len(toc) >= 3:
        indice = ('<details class="indice"><summary>En esta página · %d apartados</summary><ol>%s</ol></details>'
                  % (len(toc), "".join('<li><a href="#%s">%s</a></li>' % (i, html.escape(t)) for i, t in toc)))
    nav = [n.replace("<li><a ", '<li style="--acento:%s"><a ' % color_seccion(s["dir"]), 1)
           for n, s in zip(nav, CFG["secciones"])] + nav[len(CFG["secciones"]):]
    titulo_doc = html.escape(titulo if ruta == "index.html" else "%s · %s" % (titulo, CFG["titulo"]))
    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo_doc)s</title>
<meta name="description" content="%(desc)s">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#000000">
<link rel="icon" href="%(favicon)s" type="image/svg+xml">
<link rel="preload" href="%(fuente)s" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(css)s">%(script)s
</head>
<body class="sitio-%(variante)s%(clase_pag)s"%(estilo_pag)s>
<a class="saltar" href="#contenido">Ir al contenido</a>
<div class="reloj" aria-hidden="true"></div>
<header class="cabecera">
  <div class="marco cabecera-fila">
    <a class="marca" href="%(inicio)s">%(iso)s<span>%(marca)s</span></a>
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
    <p class="pie-casa"><a href="%(casa_url)s">%(iso)s<span>Parte de %(casa)s</span></a></p>
    <p>%(licencia)s · <a href="https://github.com/%(repo)s">Código y documentos en GitHub</a></p>
  </div>
</footer>
</body>
</html>
""" % dict(titulo_doc=titulo_doc, desc=html.escape(descripcion[:300]), css=r("estilo.css") + "?v=" + VERSION, script=('\n<script src="%s?v=%s" defer></script>' % (r("portada.js"), VERSION)) if ruta == "index.html" else "", inicio=r("index.html"),
           marca=html.escape(CFG["titulo"]), nav="".join(nav), migas=miga, indice=indice, cuerpo=cuerpo,
           pie_extra=pie_extra, licencia=html.escape(CFG["licencia"]), repo=REPO,
           favicon=r("marca/favicon.svg"), fuente=r("fuentes/archivo.woff2"), variante=VARIANTE, iso=isotipo(),
           clase_pag=" portada-pag" if ruta == "index.html" else "",
           estilo_pag=(' style="--acento:%s"' % color_seccion(seccion)) if seccion else "",
           casa=html.escape(CASA["nombre"]), casa_url=CASA["url"])


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
    return ('<li class="tarjeta revela"><a href="%s"><strong>%s</strong><span>%s</span></a></li>'
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
    for num, s in enumerate(CFG["secciones"], 1):
        readme = RAIZ / s["origen"] / "README.md"
        desc = s.get("desc", "")
        if readme.exists():
            desc = texto_plano(md(readme.read_text(encoding="utf-8"), s["origen"] + "/README.md")[3])
        n = len(s["archivos"])
        cuenta = ('<span class="cuenta">%s</span>' % html.escape("%d %s" % (n, s.get("unidad", "documentos") if n != 1 else s.get("unidad1", "documento")))) if n else ""
        bloques.append('<li class="pieza revela" style="--acento:%s"><a href="%s/index.html">'
                       '<span class="pieza-cab"><span class="num" aria-hidden="true">%02d</span>%s</span>'
                       '<strong>%s</strong>%s<span class="pieza-desc">%s</span><span class="flecha" aria-hidden="true">→</span></a></li>'
                       % (color_seccion(s["dir"]), s["dir"], num, icono(s["dir"]), html.escape(s["nombre"]), cuenta, html.escape(desc[:220])))
    extra_portada = []
    for t in CFG.get("portada_apartados", []):
        if t in partes:
            h, _, _, _ = md("## %s\n%s" % (t, partes[t]), CFG["portada"])
            extra_portada.append('<section class="bloque revela">%s</section>' % h)
    clonar = ""
    if CFG.get("clonar"):
        clonar = ('<div class="clonar"><div class="clonar-cab"><p class="etiqueta" id="clonar">Para empezar, clona el repo</p>'
                  '<button type="button" class="copiar" hidden>Copiar</button></div>'
                  '<pre tabindex="0" aria-labelledby="clonar"><code><span class="prompt" aria-hidden="true">$ </span><span class="orden">git clone https://github.com/%s</span></code></pre>'
                  '<p class="copiado" role="status" aria-live="polite"></p></div>' % REPO)
    acciones = '<p class="acciones">'
    for a in CFG.get("acciones", []):
        dest = a["href"] if a["href"].startswith(("http", "#")) else a["href"]
        acciones += '<a class="boton%s" href="%s">%s</a> ' % ("" if a.get("principal") else " secundario", dest, html.escape(a["texto"]))
    acciones += '<a class="boton secundario" href="https://github.com/%s">Ver en GitHub</a></p>' % REPO
    antetitulo = '<p class="antetitulo"><a href="%s">%s</a></p>' % (CASA["url"], html.escape(CASA["nombre"]))
    cuerpo = ('<section class="portada"><div class="portada-texto">%s<h1>%s</h1>%s%s%s</div>%s</section>'
              '<section class="bloque bloque-piezas" aria-labelledby="que-hay"><h2 id="que-hay">%s</h2><ol class="piezas">%s</ol></section>%s'
              % (antetitulo, html.escape(titulo), intro_html, acciones, clonar, ilustracion(),
                 html.escape(CFG.get("titulo_secciones", "Qué hay dentro")), "".join(bloques), "".join(extra_portada)))
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
        num = CFG["secciones"].index(s) + 1
        cuerpo = ('<header class="seccion-cab"><span class="num" aria-hidden="true">%02d</span>%s<h1>%s</h1></header>'
                  '<div class="seccion-intro">%s</div>%s<p class="acciones"><a class="boton secundario" href="%s">Ver la carpeta en GitHub</a></p>') % (
            num, icono(s["dir"], "icono icono-grande"), html.escape(s["nombre"]), intro, lista, TREE + s["origen"])
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
            salida_doc = ('<article class="doc"><p class="doc-seccion"><span class="num" aria-hidden="true">%02d</span>%s<span>%s</span></p><h1>%s</h1>%s</article>%s<p class="acciones"><a class="boton" href="%s">Volver a %s</a> %s</p>'
                          % (CFG["secciones"].index(s) + 1, icono(s["dir"]), html.escape(s["nombre"]), html.escape(titulo or p["nombre"]), h, nav, relativo(p["html"], ruta), html.escape(s["nombre"]), gh(rel)))
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
    # Icono de pestaña: el isotipo sobre negro, como el de la web principal
    salida["marca/favicon.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#000"/>%s</svg>\n'
                                   % isotipo().split(">", 1)[1].rsplit("</svg>", 1)[0])
    return salida


def huerfanas(salida):
    """Los .html de web/ que el generador ya no produce."""
    return sorted(p.relative_to(WEB).as_posix() for p in WEB.rglob("*.html")
                  if p.is_file() and p.relative_to(WEB).as_posix() not in salida)


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
    sobran = huerfanas(salida)
    if comprobar:
        if cambios or sobran:
            print("web/ no está al día con los .md (%d páginas, %d huérfanas). Ejecuta: python3 web/generar.py"
                  % (len(cambios), len(sobran)))
            for c in cambios[:20]:
                print("  " + c)
            for c in sobran[:20]:
                print("  sobra " + c)
            sys.exit(1)
        print("web/ al día: %d páginas" % len(salida))
    else:
        for ruta in sobran:
            p = WEB / ruta
            p.unlink()
            # Quita las carpetas que se quedan vacías, sin salir de web/.
            d = p.parent
            while d != WEB and WEB in d.parents and not any(d.iterdir()):
                d.rmdir()
                d = d.parent
        print("%d páginas, %d cambiadas, %d huérfanas borradas" % (len(salida), len(cambios), len(sobran)))


if __name__ == "__main__":
    main()
