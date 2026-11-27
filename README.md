# harness

Método y herramientas para que una persona y un equipo de agentes de IA trabajen juntos sobre GitHub. Cada issue es un hilo con turno, lo decidido vive en un registro con su porqué y lo que se publica pasa antes por una revisión de lo público.

No depende de un proveedor de IA concreto.

## Estado: primera versión completa

Este repo se montó por PR, en este orden:

1. **Base:** estructura, licencia y atribución.
2. **Prueba de lo público:** una Action que revisa cada PR. Se estrena con cebos inventados, para verla fallar antes de que entre contenido de verdad.
3. **Herramientas:** el canal sobre issues, el acceso por device flow y la prueba de webs.
4. **Contenido:** núcleo, especialistas, flujos y ejemplos.

## Para quién

Para quien ya trabaja con uno o varios agentes de IA y quiere que el trabajo quede ordenado en GitHub: quién habla en cada momento, qué está decidido y por qué, y quién revisa qué.

## Requisitos

- **Una cuenta de GitHub y un repo privado propio** para el canal del equipo. El canal habla de cómo trabajáis; este repo solo trae el método.
- **Una GitHub App propia**, creada por ti e instalada en ese repo, con lectura y escritura en Issues y Contents y el device flow activado. Así cada agente entra sin que nadie pegue tokens en un chat.
- **Agentes que ejecuten Python 3** (solo la biblioteca estándar) y puedan llamar a la API de GitHub: un agente de terminal, un asistente con máquina propia o un script programado.
- **Una forma de programar la revisión** de cada agente: cron, rutina o tarea programada.
- **Una persona que decide** lo que se publica, se gasta, se borra, los servicios nuevos y los cambios de rumbo. Eso no lo hace ningún agente.

No damos un tiempo de arranque: todavía no está medido.

## Estructura

| Carpeta | Qué va ahí |
|---|---|
| [nucleo/](nucleo/) | El protocolo genérico: turnos, registro de decisiones, flags y reglas de lo público. Plantilla vacía del registro y glosario |
| [herramientas/](herramientas/) | El canal sobre issues, el acceso por device flow y la prueba de webs |
| [flujos/](flujos/) | Flujos de trabajo con sus especialistas, marcados como probados o sin probar |
| [especialistas/](especialistas/) | Los gorros: misión, qué decide y qué no, criterios, entregas y su plantilla |
| [ejemplos/](ejemplos/) | Pruebas reales y lecciones, reescritas en genérico |
| [web/](web/) | El escaparate del harness, publicado con GitHub Pages |

Las Actions irán en `.github/workflows/`: la prueba de lo público y las pruebas en cada PR, y la publicación de `web/` al fusionar.

## Licencia

[MIT](LICENSE). Parte del material adapta ideas de ECC y de mattpocock/skills, también con licencia MIT: los avisos completos están en [ATRIBUCION.md](ATRIBUCION.md).
