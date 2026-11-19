# Flujo de ejemplo: de novela a vídeo

**Para qué:** un piloto de investigación. Un tráiler de 30 a 60 segundos de una novela, con permiso del autor por escrito y hecho con herramientas abiertas.
**Estado:** sin probar. Sirve para ver cómo el [orquestador](../especialistas/orquestador.md) reparte gorros en un equipo de una persona y cuatro agentes.

## Gorros que necesita

| Gorro | Para qué en este piloto |
|---|---|
| [orquestador](../especialistas/orquestador.md) | Repartir gorros por ciclo, fijar la rúbrica, los listones y las puertas, desempatar choques y cerrar con acta y métricas |
| [arquitecto jefe](../especialistas/arquitecto-jefe.md) | La cadena: de texto a escaleta, storyboard, planos y montaje. Qué herramienta va en cada paso y dónde corre |
| [investigador](../especialistas/investigador.md) | Comparar las herramientas candidatas y la licencia de cada modelo |
| [cumplimiento](../especialistas/cumplimiento.md) | El permiso del autor y las licencias de modelos y herramientas, antes de gastar |
| [cartógrafo](../especialistas/cartografo.md) | La biblia de la novela: personajes, hechos y giros que no se destripan, con su página |
| [guionista](../especialistas/guionista.md) | Escaleta y guion del tráiler, cada punto con su página |
| [director de arte](../especialistas/director-de-arte.md) | Paquete de estilo y storyboard en papel |
| [constructor](../especialistas/constructor.md) | Preparar la cadena en local, sin generar |
| [evaluador](../especialistas/evaluador.md) | La rúbrica de fidelidad, en papel y luego en vídeo |
| [contrapeso](../especialistas/contrapeso.md) | Objeciones antes de gastar en generación |
| [revisor](../especialistas/revisor.md) | Revisar la cadena antes de generar |
| [montador](../especialistas/montador.md) | Planos, montaje y registro de procedencia y coste |
| [guardián de lo público](../especialistas/guardian-de-lo-publico.md) | Solo si se decide enseñar el tráiler fuera |
| [estratega de lanzamiento](../especialistas/estratega-de-lanzamiento.md) | Solo si se decide publicar |

## Flujo por ciclos

Cuatro agentes, un gorro cada uno por ciclo. A, B, C y D son los agentes; el orquestador decide quién es quién.

| Ciclo | A | B | C | D | Puerta al final |
|---|---|---|---|---|---|
| 0. Diseño | orquestador | arquitecto jefe | investigador | cumplimiento | Flujo, cadena, rúbrica y líneas rojas escritos en el hilo |
| 1. Papel | guionista | director de arte | constructor | cartógrafo | Guion, estilo y storyboard entregados |
| 2. Evaluación en papel | guionista (arregla) | director de arte (arregla) | contrapeso | evaluador | Nota de fidelidad sobre el umbral. **La persona decide** si se gasta en planos |
| 3. Planos y montaje | orquestador (métricas) | revisor | montador | evaluador (sobre el vídeo) | Tráiler con procedencia y coste, y acta |
| 4. Opcional | estratega de lanzamiento | guardián de lo público | | | **La persona decide** si se publica |

## Reglas del flujo

- **El evaluador de los ciclos 2 y 3** no es quien escribió el guion ni quien hizo el storyboard. Mejor si tampoco escribió la biblia.
- **El arquitecto jefe** no es el orquestador ni quien propuso el proyecto, para que la forma de la cadena tenga una segunda opinión.
- **Listones del ciclo 0:** el umbral de la rúbrica y las líneas rojas (el permiso del autor por escrito y herramientas cuya licencia permita el uso). Si dos gorros chocan, la forma de la cadena la decide el arquitecto jefe y el orquestador desempata.
- **Hasta la puerta del ciclo 2 no se gasta nada:** todo es texto, imágenes de referencia y pruebas en local.
- **Métricas al cerrar:** horas por ciclo, coste, nota de fidelidad por criterio y qué se rehizo y por qué.

Cuando se pruebe, la prueba va a [ejemplos/](../ejemplos/) y este flujo cambia de estado.
