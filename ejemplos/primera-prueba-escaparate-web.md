# Prueba: primer cambio en el escaparate web con el flujo

**Flujo:** [escaparate web](../flujos/escaparate-web.md).
**Encargo de la persona:** probar todo el material del harness con un trabajo real, de la forma más profesional posible, porque la web es el escaparate del equipo, y sacar de ahí los flujos de trabajo.
**Trabajo de partida:** los textos de la versión siguiente de la web del equipo, ya redactados en un PR con tabla antes → después.

## Rastro, paso a paso

| Paso | Gorro | Qué encontró | Qué cambió |
|---|---|---|---|
| 0 Encargo | coordinador | El PR ya tenía tabla antes → después y fuentes. `main` iba por delante de la rama | Se trajo `main` a la rama |
| 1 Redacción | redactor | — | Los textos del PR |
| 2 Cifras | cartógrafo, en modo cifras (**provisional**) | Recuentos y fechas, ok con su fuente. **Dos fallos:** «se pueden descargar» no tenía una ruta visible en la web enlazada, y «el código está abierto» exageraba, porque parte del trabajo vive en repos privados. El segundo se repetía en la descripción para buscadores | «en abierto en GitHub» y «el código de lo publicado», en el cuerpo y en los metadatos |
| 3 Lo público | guardián de lo público | **Pasa con avisos.** Dos comentarios del HTML nombraban a la persona: no se ven en la página, pero sí en el código fuente. Sin secretos ni enlaces a repos privados | Fuera el nombre de los comentarios |
| 4 Lector en frío | evaluador (**provisional**) | Un recuento de repos no se podía comprobar desde fuera, «desde octubre» iba a envejecer y una entradilla le hablaba al equipo y no al visitante | Fecha con año y entradilla para el visitante |
| 5 Tono y marca | guardián de la voz (**provisional**) | Tres objeciones posibles, ninguna de peso | Sin cambios, con el porqué en la prueba |
| 6 Accesibilidad y móvil | revisor con la especialidad web | WebKit a 390 y 320 de ancho y Chromium a 1280, en tres páginas de la rama y de la vista previa: axe sin fallos, sin desborde, sin errores de JavaScript ni recursos rotos. **Capturas medidas, no miradas** | Nada que corregir |
| 7 Objeción | contrapeso | Objeciones a varias propuestas de la ronda | Recogidas en las recomendaciones a la persona |
| 8 Empaquetado | jefe de gabinete | — | Vista previa regenerada y tarjeta en el tablón con qué revisiones lleva y cuáles faltan |

## Qué funcionó

- **El orden cifras → público → frío** encontró dos afirmaciones falsas que habían pasado la redacción, y una de ellas repetida en los metadatos, que ninguna revisión visual habría visto.
- **Un commit por gorro** dejó el rastro en `git log`: no hizo falta otro documento para saber quién cambió qué y por qué.
- **El paso 6 ya era un script:** se pasó dos veces, sobre la rama y sobre la vista previa, sin gastar atención.

## Qué rozó

- **El cuello de botella fue el turno, no el trabajo.** El hilo de los textos se quedó días sin respuesta mientras los mismos agentes contestaban en minutos otra ronda del canal. Una ronda en el canal arranca; un reparto en otro hilo, no.
- **Separación incumplida:** un solo agente llevó redacción, cifras, frío y tono, y por eso tres gorros quedaron provisionales. Cuatro agentes no dan para separar ocho gorros en una tarde sin esperar turnos.
- **El catálogo estaba hecho para vídeo y código:** para un texto público faltaban gorros (redactor y guardián de la voz; el verificador de cifras acabó siendo un modo del cartógrafo).
- **Nadie miró las capturas.** Se midió todo, pero la imagen solo la vio la persona.

## Qué cambió en el harness

- El flujo se partió en **esqueleto y adaptador**, para no reescribirlo en cada tipo de proyecto.
- La **objeción de fondo** pasó al principio (1b), y al final solo queda una pasada rápida.
- Las **afirmaciones vivas** entraron como regla del paso 2.
- El paso 3 avisa a la persona **en el momento** si encuentra algo ya publicado que no debe estar.
- Los gorros nuevos quedan pendientes de ficha, y hasta entonces su paso es provisional.

## Cuánto costó

Una tarde de un agente y unas 95 llamadas a herramientas. Más de la mitad fue leer (hilos, registro, catálogo) y localizar fuentes, y los pasos 2 a 6 una cuarta parte. Los turnos del resto del equipo no entran en esa cuenta.
