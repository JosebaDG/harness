# Web

El escaparate del harness, publicado con GitHub Pages desde la Action [`pages.yml`](../.github/workflows/pages.yml) al fusionar en `main`.

Las páginas se generan a partir de los `.md` del repo: no se escriben a mano.

- `sitio.json`: título, secciones y orden.
- `generar.py`: escribe una página por cada `.md`, la portada y una página por sección. Solo biblioteca estándar de Python 3.
- `estilo.css`: el estilo, claro u oscuro según el sistema. Sin JavaScript ni fuentes descargadas.

Si cambias un `.md`, rehaz la web en el mismo PR:

```
python3 web/generar.py
```

`python3 web/generar.py --comprobar` sale con 1 si `web/` no está al día: si falta una página, si una no coincide con su `.md` o si sobra una huérfana. La Action [`web-al-dia.yml`](../.github/workflows/web-al-dia.yml) lo comprueba en cada PR, y `pages.yml` también la rehace antes de publicar.

Si renombras o quitas un `.md`, `generar.py` borra su página vieja. Solo borra `.html` dentro de `web/`, que los escribe todos él; no toca nada más.

`python3 web/prueba_generar.py` prueba el generador sobre una copia temporal del repo: una web desfasada, un renombrado y la web actual.
