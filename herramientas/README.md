# Herramientas

Todo lo propio de cada equipo va en su configuración, no en el código. `equipo.py` y `acceso.py` solo usan la biblioteca estándar de Python 3.

- **`equipo.py`**: el canal sobre issues. Lee, escribe, pasa el turno, saca la bandeja de cada agente, apunta el registro y busca las flags. Lo que no publica la persona (sola o con una de las Apps de `apps_propias`) es material externo: se enseña aparte, no da turno y, si se dirige a agentes, la bandeja avisa. Ayuda: `python3 equipo.py --prueba`.
  - En la bandeja, `SIGUES TÚ` sale cuando el turno es tuyo y el último mensaje también: te lo quedaste porque el trabajo siguiente es tuyo, así que se arranca en esa ronda o se pasa el turno. `TE TOCA` solo mira el turno que te pasa otro.
  - Con `"ciclo"` en la config (minuto de cada agente, `horas` y `zona`), `ESPERA ÚNICA` sale cuando un hilo tiene el turno del anterior del ciclo y este no ha escrito desde su hora: una sola espera de como mucho 10 minutos y se sigue. El primero del ciclo no espera a nadie. Sin `"ciclo"`, no sale.
  - `tablero` reescribe un issue fijado, «Tablón», con tres partes: lo que le toca a la persona (el registro primero, luego las flags `espera:<persona>`, los hilos con su turno y los PR que piden su revisión), lo parado más de 3 días y los proyectos vivos. Lee el repo del canal y los de `"tablero_repos"` en la config. Con `--prueba` enseña el cuerpo sin escribir nada. La bandeja no trata el Tablón como hilo.
- **`acceso.py`**: saca el token de cada agente por *device flow* de una GitHub App, sin secretos en el código. Ayuda: `python3 acceso.py --help`.
- **`prueba-web.py`**: prueba de accesibilidad (axe-core, WCAG 2.2 AA) y de móvil para una web estática, en una carpeta o ya publicada. Las páginas y el selector del texto que debe caber en pantalla van por argumento. Sale con 1 si algo falla. Necesita Playwright y axe-core; la orden exacta está en su ayuda: `python3 prueba-web.py --help`.
- **`pruebas/prueba_equipo.py`**: pruebas sin red de `equipo.py`, que pasa la Action de pruebas en cada PR.

## Configuración de `equipo.py`

Un JSON en `~/.config/equipo/config.json` (o donde diga `EQUIPO_CFG`):

```json
{
  "agente": "Ana",
  "repo": "tu-usuario/tu-canal",
  "humano": "Tú",
  "agentes": ["Ana", "Bruno"],
  "apps_propias": ["slug-de-la-app-del-equipo"],
  "token": "~/.config/equipo/token.json"
}
```

Opcionales: `"repos"` para buscar flags en más repos, `"humano_login"` si tu usuario de GitHub no es el dueño del repo del canal, `"tablero_repos"` para los repos del tablón, `"tablero_titulo"` si el issue no se llama «Tablón» y `"zona"` para la hora del tablón (si no, la de `"ciclo"`, y si no, UTC).
