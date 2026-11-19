# 006 · Dos revisiones, la misma acción esperando

- **Cuándo:** cuando una revisión va a preparar una acción que necesita el sí de la persona y una revisión anterior pudo dejar preparada la misma.
- **Qué hacer:** antes de prepararla, mirar si ya hay una igual esperando, o si el hilo dice que está «preparada» o «esperando el sí». Si la hay, no se prepara otra: se cuenta en el hilo que sigue esperando. Una acción, una petición. Pieza: [protocolo, «Turnos», punto 6](../../nucleo/protocolo.md#turnos).
- **Pruebas:** dos revisiones del mismo agente, el mismo día, prepararon el mismo cambio de base de un PR. La persona vio dos peticiones iguales y rechazó las dos, porque el coordinador ya había cambiado la base y fusionado horas antes.
- **Seguridad:** media. Visto una vez, pero el mecanismo es claro: cada revisión arranca sin saber qué dejó esperando la anterior. La segunda, además, llegó tarde ([lección 005](005-la-aprobacion-que-llego-tarde.md)).

## Qué pasó, en llano

Dos recados iguales en la bandeja de la persona: no sabe si son dos cosas distintas y tiene que pararse a averiguarlo. Y cuando llegaron, el trabajo ya estaba hecho.

## Qué cambió en el harness

La persona es quien aprueba, así que cada petición de más le cuesta atención. Una sola petición por acción, y si el hilo ya avanzó, ninguna.
