# 013 · Una sola fuente de datos y un día sin aviso

- **Cuándo:** cuando una rutina que llega a la persona (un aviso, un resumen, un dato diario) depende de una sola fuente externa que se pide desde una sola máquina.
- **Qué hacer:**
  - Antes de darla por buena, apuntar al menos una segunda vía que no comparta el punto de fallo: otra salida de red, una copia propia o una entrada manual. Tiene que dar el mismo formato, para que lo de después no se entere del cambio.
  - Ante un 403 o un 429, no insistir: pausar esa fuente un rato y tirar de la siguiente.
  - Si fallan todas, el aviso de error dice cómo salvar el día a mano.
  - La regla vale para cualquier skill que traiga datos de fuera.
- **Pruebas:** un aviso diario llevaba semanas saliendo y se daba por seguro. Un día, la API pública de la que tiraba contestó 403 desde nuestra máquina con la página de su cortafuegos, y el aviso no salió. Los datos estaban publicados: se veían desde un navegador con otra salida y desde las máquinas de GitHub. El archivo alternativo del mismo proveedor dio el mismo 403, porque está detrás del mismo cortafuegos: cambiar a «otra API del mismo sitio» no era una segunda vía.
- **Seguridad:** media. Pasó una vez, pero otros proyectos públicos cuentan los mismos bloqueos por IP de ese proveedor.

## Qué pasó, en llano

Todo dependía de que un tercero dejara pasar a una máquina que no controlamos. El día que la bloqueó, la persona se quedó sin aviso aunque los datos estaban ahí, y fue ella quien tuvo que ir a mirarlos.

## Qué cambió

El script del aviso prueba tres vías por orden, todas sin credenciales: la API, un archivo con la respuesta guardada a mano o desde un navegador, y la copia que una Action guarda en el repo desde los servidores de GitHub. Tras un 403 deja la API en paz media hora, porque el bloqueo se alarga a quien insiste. Queda pendiente que la copia de la Action llegue a tiempo para el aviso.
