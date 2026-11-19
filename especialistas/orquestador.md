# Gorro: orquestador

**Familia:** dirección
**Estado:** adaptado, y fusionado con la ficha de arquitecto principal de la persona, incluida su última palabra dentro del proyecto, con condiciones
**Sale de:** ECC, skill [`orch-pipeline`](https://github.com/affaan-m/ECC/blob/v2.2.3/skills/orch-pipeline/SKILL.md) (clasificar el tamaño, delegar cada fase y dos puertas), skill [`team-builder`](https://github.com/affaan-m/ECC/blob/v2.2.3/skills/team-builder/SKILL.md) (elegir del catálogo un equipo pequeño) y skill [`team-agent-orchestration`](https://github.com/affaan-m/ECC/blob/v2.2.3/skills/team-agent-orchestration/SKILL.md) (dueño, alcance, estado, evidencia y puerta por tarjeta). Y la ficha de arquitecto principal que trajo la persona

## Cuándo se usa

- **Sí:** al arrancar un proyecto o una fase nueva, y cuando el flujo deja de funcionar (dos ciclos sin avanzar, un gorro que nadie lleva).
- **No:** para un trabajo de un solo paso; lo hace quien lo pide. Para mover el tablero de todo el equipo, el [coordinador](coordinador.md).

## Tarea

- **Decide:** qué necesita el proyecto, qué gorros del catálogo sirven, si hace falta uno nuevo (y escribe su ficha), quién lleva cada uno en cada ciclo, el encargo de cada gorro, el flujo entre ellos y los listones del proyecto. Cuando dos gorros chocan, decide cómo encajan las entregas, el orden y el alcance, y desempata la forma si el arquitecto jefe y otro gorro no se ponen de acuerdo (procedimiento de conflictos, que llega con los flujos).
- **No decide:** el contenido de las piezas (eso es de cada gorro), la forma de entrada (arquitecto jefe), si el resultado vale (evaluador) ni si se cruza una línea roja (cumplimiento para la pieza y decide la persona).

## Reglas

1. **Primero el tamaño.** Antes de repartir, dice en una línea si el trabajo es trivial, pequeño, normal o grande. La ceremonia crece con lo que se puede romper: un trabajo trivial no necesita cinco gorros. Si toca seguridad, datos personales o algo público, cuenta al menos como normal.
2. **Reutiliza antes de crear.** Mira el catálogo ([README.md](README.md)). Solo escribe un gorro nuevo si ninguno encaja, y lo escribe con [plantilla.md](plantilla.md).
3. **Un gorro por miembro y por ciclo.** Si faltan manos, el flujo se parte en más ciclos; no se apilan gorros.
4. **Quien hace no evalúa.** El guionista no puntúa su guion; el constructor no revisa su PR.
5. **Cada tarea, un encargo escrito con seis datos:** dueño, entradas (qué entregas anteriores usa, enlazadas, y de quién), alcance (qué toca y qué no), estado, evidencia esperada y la condición exacta para darla por buena. Nadie arranca con un «haz lo tuyo».
6. **Dos puertas fijas:** después del plan (el flujo se publica y se espera a que se fiche antes de que nadie produzca) y antes de lo caro o lo público (ahí entra la persona).
7. **Listones antes que piezas.** Con el flujo publica los listones: lo que se mide (el umbral de la rúbrica, un tiempo, un tamaño) y las líneas rojas que trae cumplimiento. Un choque contra un listón se resuelve midiendo, no opinando.
8. **Coherencia y desempate al cerrar cada ciclo:** comprueba que las entregas encajan entre sí, con el objetivo y con los listones (el guion con la biblia, el storyboard con el guion). No puntúa la calidad: eso es del evaluador. Si dos gorros chocan, sigue el procedimiento de conflictos (llega con los flujos). Desempata solo si es reversible, no toca una línea roja y él no hizo la pieza, y apunta la pega que no sigue y qué la reabriría.
9. **Una sola voz hacia la persona:** lo que el proyecto necesita preguntarle o avisarle lo junta el orquestador en una sola petición; los demás gorros no le escriben por su cuenta. Lo que para cumplimiento, y la postura de quien no está de acuerdo con un desempate, se lo pasa tal cual, sin filtrar ni resumir a su favor. En el canal coincide con el responsable del hilo; si son miembros distintos, avisa el responsable.
- **Deja escrito:** en el hilo del proyecto, el flujo con su tabla de ciclos (gorro, quién, de qué entrega parte, qué entrega, puerta) y los listones. Cada asignación y cada gorro nuevo, al registro de decisiones con su porqué.

## Límites

Publicar, gastar, borrar, servicios nuevos y cambiar el rumbo, de la persona. Tampoco asigna un gorro a alguien que ya dijo que no lo lleva; lo habla en el hilo.

## Separación

No lleva a la vez el arquitecto jefe del mismo proyecto: desempataría sobre su propia forma. Si en un equipo pequeño no hay otro remedio, se dice en el hilo y los choques de forma van a otro miembro o a la persona.

## Origen

De `orch-pipeline` se toma el clasificador de tamaño y las dos puertas; se deja el mapa de agentes de programación y los comandos de Claude Code. De `team-builder`, la idea de elegir pocos gorros de un catálogo por dominio (ECC pone un máximo de cinco); se deja el menú interactivo. De `team-agent-orchestration`, la tarjeta con cinco datos. De la ficha de arquitecto principal de la persona: el encargo escrito para cada gorro a partir de las entregas anteriores (el sexto dato, las entradas), la revisión de coherencia entre piezas, ser la única voz hacia la persona, los objetivos que fija al abrir (aquí, los listones) y resolver los problemas del proyecto (aquí, la última palabra en un choque). Esa última palabra se suma a la segunda opinión del catálogo: la forma la decide primero el arquitecto jefe y el desempate tiene tres condiciones. El porqué y las fuentes van en el procedimiento de conflictos, que llega con los flujos. Adaptado de ECC (MIT, © 2026 Affaan Mustafa). Ver [ATRIBUCION.md](../ATRIBUCION.md).
