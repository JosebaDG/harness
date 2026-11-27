"""Pruebas sin red de web/generar.py, sobre una copia temporal del repo.

No toca el repo de verdad. Comprueba tres casos:
  1. La web actual sale «al día» y generar no cambia nada.
  2. Una página de web/ desfasada hace fallar --comprobar.
  3. Al renombrar un .md, la página vieja queda huérfana: --comprobar falla
     y generar la borra (sin tocar nada fuera de web/ ni lo que no es .html).

Uso: python3 web/prueba_generar.py
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
fallos = []


def copia():
    d = Path(tempfile.mkdtemp()) / "repo"
    shutil.copytree(REPO, d, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
    return d


def generar(d, *args):
    r = subprocess.run([sys.executable, str(d / "web" / "generar.py"), *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def foto(d):
    return {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def caso(nombre, ok, detalle=""):
    print(("OK    " if ok else "FALLA ") + nombre)
    if not ok:
        fallos.append(nombre)
        print("      " + detalle.strip().replace("\n", "\n      "))


# 1. La web actual: al día y sin cambios.
d = copia()
antes = foto(d)
cod, out = generar(d, "--comprobar")
caso("web actual: --comprobar sale al día", cod == 0 and "al día" in out, out)
cod, out = generar(d)
caso("web actual: generar no cambia ni borra nada", cod == 0 and foto(d) == antes, out)

# 2. Una página desfasada: --comprobar la rechaza.
d = copia()
indice = d / "web" / "index.html"
indice.write_text(indice.read_text(encoding="utf-8") + "<!-- desfasada -->", encoding="utf-8")
cod, out = generar(d, "--comprobar")
caso("web desfasada: --comprobar falla", cod == 1 and "index.html" in out, out)

# 3. Renombrar un .md deja una huérfana: --comprobar falla y generar la borra.
d = copia()
cfg = json.loads((d / "web" / "sitio.json").read_text(encoding="utf-8"))
# El primer .md de una sección (el generador los descubre solo en su carpeta).
sec, md_viejo = next((s, p) for s in cfg["secciones"]
                     for p in sorted((d / s["origen"]).rglob("*.md")) if p.name != "README.md")
md_viejo.rename(md_viejo.with_name(md_viejo.stem + "-renombrado.md"))
html_viejo = d / "web" / sec["dir"] / md_viejo.relative_to(d / sec["origen"]).with_suffix(".html")
caso("renombrado: la página vieja existe antes de generar", html_viejo.exists(), str(html_viejo))
fuera = {k: v for k, v in foto(d).items() if not (k.startswith("web/") and k.endswith(".html"))}
cod, out = generar(d, "--comprobar")
caso("renombrado: --comprobar detecta la huérfana", cod == 1 and "sobra" in out, out)
cod, out = generar(d)
caso("renombrado: generar borra la huérfana", cod == 0 and not html_viejo.exists(), out)
despues = {k: v for k, v in foto(d).items() if not (k.startswith("web/") and k.endswith(".html"))}
caso("renombrado: no toca nada fuera de los .html de web/",
     set(despues) - {"web/marca/favicon.svg"} == set(fuera) - {"web/marca/favicon.svg"}
     and all(despues[k] == fuera[k] for k in fuera if k in despues and k != "web/marca/favicon.svg"))
cod, out = generar(d, "--comprobar")
caso("renombrado: después de generar sale al día", cod == 0, out)

print("\n%s" % ("Todo bien" if not fallos else "%d fallos" % len(fallos)))
sys.exit(1 if fallos else 0)
