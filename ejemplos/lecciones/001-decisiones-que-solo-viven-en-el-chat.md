# 001 · Decisiones que solo viven en el chat

**En una línea:** una rutina arranca con la foto del contexto con el que se escribió. Si lo que la persona decide en el chat no llega al repo, la rutina lo pisa o lo vuelve a pedir.

- **Cuándo:** cuando la persona decide algo en un chat, y hay skills o mensajes programados que trabajan sobre ese tema.
- **Qué hacer:** quien lo recibe lo apunta en el registro en ese mismo turno (`equipo.py apunta`) y pone la flag en el issue o PR (`equipo.py flag`). Las rutinas miran el registro antes de pedir o de hacer, y si chocan con lo que dice su skill, gana el registro y se avisa del desfase. Pieza: [protocolo, «El registro»](../../nucleo/protocolo.md#el-registro-si-no-está-en-el-repo-no-existe).
- **Pruebas:** pasó dos veces en menos de un día. Una revisión programada pidió a la persona desplegar algo que ella acababa de aparcar en el chat. Al día siguiente, otra revisión le volvió a pedir una decisión que ya estaba tomada y escrita, pero en un comentario, mientras el cuerpo del issue seguía con las casillas sin marcar y con una marca vieja de «necesita a la persona». Ese mismo día, tras una compactación del chat, se volvieron a plantear opciones ya descartadas.
- **Seguridad:** alta. Se vio varias veces seguidas y la causa se entiende: las skills copian el contexto del día en que se escriben.

## Qué pasó, en llano

Las skills y los mensajes programados son fotos fijas. El chat sigue decidiendo y ellas no se enteran. Además, una marca que nadie quitó al decidir seguía diciendo «esto espera a la persona», y la rutina la creyó.

## Qué cambió en el harness

- **Un registro vivo**, una línea por decisión, y flags `decidido`, `aparcado`, `espera:<persona>` y `sustituido` donde se mira: en el issue o el PR. `flag` quita sola la marca vieja.
- **`bandeja` avisa con `REGISTRO CAMBIADO`**, así el desfase se ve al arrancar sin leer nada si no hay cambios.
- **Sin listas de decisiones dentro de skills**: el primer arreglo fue añadir a una skill la lista de lo que no había que pedir, y era otra foto fija. Las skills dicen el cómo y remiten al registro.
- **Descartado:** un documento largo de decisiones con plantilla, revisiones semanales obligatorias o pedir confirmación antes de cada rutina. Añaden fricción diaria y no evitan más errores que una línea y una flag.

## Qué aprendimos

Una marca que nadie quita es peor que ninguna: miente con autoridad. Y el arreglo de un fallo de contexto no puede ser más contexto congelado: tiene que ser un sitio vivo al que se mire.
