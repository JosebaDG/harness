# Flujo: cambio en el escaparate web

**Para qué:** cualquier cambio de texto o contenido en una web pública que no toca el diseño ni las animaciones.
**Estado:** probado una vez, con los textos de una versión nueva de la web del propio equipo. La prueba está en [ejemplos/primera-prueba-escaparate-web.md](../ejemplos/primera-prueba-escaparate-web.md).

**Esqueleto y adaptador:** los pasos 0 a 5 y 7 a 9 son el esqueleto común (ver [README](README.md)). Esta página es el **adaptador web**: la vista previa es una copia de la rama publicada bajo `/preview/prN/` y el paso 6 es la prueba de accesibilidad y móvil de [herramientas/prueba-web.py](../herramientas/prueba-web.py).

**Puertas de la persona:** dos. Al principio, el encargo con sus palabras, y al final, sí, no o cambios. Nada en medio, **salvo** cuando el paso 3 encuentra en `main` algo ya publicado que no debe estar: se avisa a la persona en ese momento, porque despublicar es suyo y esperar a la puerta final lo deja días a la vista.

## Pasos

| # | Paso | Especialista | Entra | Sale | Automático |
|---|---|---|---|---|---|
| 0 | Encargo | [coordinador](../especialistas/coordinador.md) | Palabras de la persona | Línea en el registro, rama e hilo con turnos | No |
| 1 | Redacción | redactor de lo público (sin ficha todavía) | Encargo y material | PR con tabla antes → después y la fuente de cada cifra | No |
| 1b | Objeción de fondo | [contrapeso](../especialistas/contrapeso.md) | Borrador y encargo | La objeción más fuerte («esto no debería estar», «el encargo pide otra cosa») o nada | No |
| 2 | Cifras y hechos | [cartógrafo](../especialistas/cartografo.md), en modo cifras | PR | ok, corregir o quitar por cifra, con fuente y fecha. Marca las afirmaciones vivas | En parte: recuentos con una consulta fija |
| 3 | Lo público | [guardián de lo público](../especialistas/guardian-de-lo-publico.md) | PR | pasa, pasa con avisos o no pasa (vuelve al paso 1) | En parte: la Action de lo público |
| 4 | Lector en frío | [evaluador](../especialistas/evaluador.md) | Solo la vista previa | Frases a cambiar | No |
| 5 | Tono y marca | guardián de la voz (sin ficha todavía) | PR | Objeciones o «sin cambios» | No |
| 6 | Accesibilidad y móvil | [revisor](../especialistas/revisor.md) con la especialidad web | Rama y vista previa | Tabla motor × ancho × página. Sale con código 1 si algo falla | Sí: [prueba-web.py](../herramientas/prueba-web.py) |
| 7 | Última objeción | contrapeso | Paquete de decisión | Pasada rápida: objeción o nada | No |
| 8 | Empaquetado | [jefe de gabinete](../especialistas/jefe-de-gabinete.md) | Rastro de los pasos 0 a 7 | Vista previa, tarjeta en el tablón y mensaje a la persona | En parte: copiar la rama a `/preview/prN/` |
| — | **Puerta: la persona** | — | La vista previa, en su móvil | sí, no o cambios | — |
| 9 | Publicar y limpiar | coordinador | El sí de la persona | Fusión, quitar la vista previa y la tarjeta del tablón | En parte |

Los dos gorros sin ficha salieron de la primera prueba. Hasta que tengan ficha, el paso que llevan queda provisional.

## Reglas del flujo

- **La objeción de fondo va pronto (1b):** si aparece al final, se tira el trabajo de los pasos 2 a 6. En el 7 solo queda una pasada rápida.
- **Orden fijo de 2 a 4:** primero lo que no es verdad, luego lo que no debe salir y luego lo que no se entiende. Corregir el estilo de una frase que después se quita es trabajo tirado.
- **Afirmaciones vivas:** lo que se dice de algo automático («cada día», «se actualizan solos», «más de cien») puede dejar de ser verdad sin que nadie lo toque. El paso 2 las marca, y cada una se reescribe con fecha o entra en una comprobación sin agente. Pasó de verdad: una web decía que sus datos se actualizaban solos cada día cuando la fuente llevaba semanas parada.
- **Cada paso es un commit** con el gorro en el mensaje: `Gorro (quién): qué encontró -> qué cambió`. Si no cambia nada, la nota va en el hilo.
- **Separación:** quien redacta (1) no lleva el 2, el 4 ni el 5. Quien lleva el 3 no lleva el 4: si no hay nadie más, el 4 se hace antes de abrir el PR, mirando solo la vista previa.
- **Turnos:** los pasos que lleva otro agente van por el hilo del canal. Un turno en otro repo deja una línea en el canal, porque las revisiones de los agentes solo miran el canal.
- **Vista previa:** se regenera tras cada cambio de la rama. Solo cambian las rutas, y se añaden `noindex` y un enlace para volver.
- **Capturas:** se dice siempre si se han mirado o solo medido.

## Qué se automatiza y qué no

- **Ya, paso 6:** [prueba-web.py](../herramientas/prueba-web.py). Se pasa sobre la rama y sobre la vista previa (`prefijo` = `/preview/prN`). Dependencias y opciones, en su cabecera.
- **Ya, cifras con una consulta fija:** cada recuento que sale en la web (PR fusionados, registros de datos) se hace siempre con la misma consulta, escrita en el flujo de cada proyecto, y se anota con su fecha. Así dos personas que cuentan llegan a la misma cifra.
- **Ya, paso 3 en parte:** la Action de lo público, en cada PR.
- **Siguiente, sin agente ni gasto:** una Action en la web que en cada PR pase el paso 6, compruebe las afirmaciones vivas y deje el resultado como comentario. Dar de alta una Action nueva es un servicio nuevo, y eso lo decide la persona.
- **Nunca:** las dos puertas de la persona y mirar las capturas con ojos.

## Coste de referencia

En la primera prueba, una tarde de un agente y unas 95 llamadas a herramientas, más una ronda de revisiones del equipo. Más de la mitad se fue en leer y localizar fuentes, y los pasos 2 a 6 en una cuarta parte. Lo caro no es revisar: es encontrar dónde está cada cosa. Por eso un flujo nuevo empieza por un inventario de fuentes.
