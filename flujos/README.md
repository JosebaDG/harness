# Flujos

Flujos de trabajo de principio a fin: qué especialistas hacen falta, en qué orden y qué entrega cada uno. Cada flujo dice si ya se ha probado en un trabajo real o si está sin probar.

## Esqueleto y adaptador

Un flujo tiene dos partes:

- **El esqueleto:** los pasos que valen para cualquier proyecto. El encargo, la redacción o construcción, la objeción de fondo, las cifras, lo público, el lector en frío, la última objeción, el empaquetado para la persona y publicar.
- **El adaptador:** lo que cambia según el tipo de proyecto. Qué es la vista previa que ve la persona y qué prueba automática se hace. Una web tiene un adaptador; una app o un vídeo tendrán otro.

Así un flujo nuevo no empieza de cero: copia el esqueleto y escribe su adaptador.

## Catálogo

| Flujo | Para qué | Estado |
|---|---|---|
| [escaparate-web.md](escaparate-web.md) | Un cambio de texto o contenido en una web pública, sin tocar el diseño | Probado una vez. La prueba está en [ejemplos/](../ejemplos/primera-prueba-escaparate-web.md) |
| [novela-a-video.md](novela-a-video.md) | Un piloto de investigación: un tráiler corto de una novela con herramientas abiertas | Sin probar. Sirve para ver cómo se reparten gorros por ciclos |

## Reglas para todos los flujos

1. **Dos puertas de la persona:** al principio, el encargo con sus palabras, y al final, sí, no o cambios. En medio, nada, salvo que aparezca algo ya publicado que no debe estar: eso se le avisa en el momento, porque despublicar es suyo.
2. **Un commit por paso,** con el gorro en el mensaje: `Gorro (quién): qué encontró -> qué cambió`. Si no cambia nada, la nota va en el hilo. El rastro queda en `git log`.
3. **Quien hace una pieza no la evalúa.** Si un solo agente lleva varios gorros, lo dice en el commit y esos gorros quedan provisionales hasta que los repase otro.
4. **Un flujo pasa a «probado» solo con una prueba en [ejemplos/](../ejemplos/):** qué pasó, qué funcionó, qué rozó y cuánto costó.

Los procedimientos que citan algunos pasos (conflictos, consejo, traspaso) y las especialidades, como la web, llegan en otro PR.
