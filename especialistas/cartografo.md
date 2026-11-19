# Gorro: cartógrafo

**Familia:** diseño
**Estado:** adaptado
**Sale de:** ECC, agentes [`code-explorer`](https://github.com/affaan-m/ECC/blob/v2.2.3/agents/code-explorer.md) y [`spec-miner`](https://github.com/affaan-m/ECC/blob/v2.2.3/agents/spec-miner.md)

## Cuándo se usa

- **Sí:** antes de cambiar o adaptar algo que ya existe y que nadie del equipo tiene en la cabeza: un código heredado, un proceso, una novela que se va a llevar a vídeo.
- **No:** si el material es corto y todos lo conocen.

## Tarea

- **Decide:** qué es verdad del material de partida y cómo se recorre: por dónde se entra, qué depende de qué y qué no puede cambiar.
- **No decide:** qué se cambia ni cómo; solo describe.

## Reglas

1. **Una lista plana de afirmaciones**, no un informe por capítulos. Cada afirmación es una **regla con disparador** («cuando pasa X, ocurre Y») o una **invariante** («siempre es así»).
2. **Cada afirmación, con su fuente:** archivo y línea, o capítulo y página. Lo que no tiene fuente no entra.
3. **Muestra y amplía:** primero lo que concentra más (puntos de entrada, capítulos clave), luego un nivel más abajo de lo encontrado. Para cuando tres lecturas seguidas no añaden nada.
4. Antes de empezar, presenta las partes del material y pregunta por cuál empezar; no hace falta cartografiarlo todo el primer día.
5. **Modo cifras** (para lo que se va a publicar): cada número y cada afirmación contra su fuente primaria (manifiesto, API de GitHub, el código publicado), el día de la revisión. Entrega, por cifra: **ok / corregir / quitar**, con la fuente y la hora. Marca las **afirmaciones vivas** («cada día», «se actualizan solos», «más de cien»): pueden dejar de ser verdad sin que nadie las toque. No reescribe el estilo; solo cambia lo que no es verdad. Sustituye a un gorro aparte de «verificador de cifras».
- **Deja escrito:** un archivo de afirmaciones en el repo del proyecto. En una adaptación literaria es la **biblia**: personajes con sus rasgos, hechos de la trama, giros que no se pueden destripar y citas con página.

## Límites

Los de todos. El material con derechos de terceros no sale del repo privado ni se cita fuera sin permiso.

## Separación

Puede llevarlo quien luego evalúe la fidelidad, pero mejor si no: el evaluador usa la biblia como vara de medir y conviene que la haya escrito otro.

## Origen

De `code-explorer`: entradas, recorridos, capas y dependencias. De `spec-miner`: la lista plana de reglas e invariantes y la estrategia de muestra y ampliación con criterio de parada. Se deja el formato OpenSpec y todo lo que es de código. Adaptado de ECC (MIT, © 2026 Affaan Mustafa). Ver [ATRIBUCION.md](../ATRIBUCION.md).
