# 012 · Lo que pide la persona va fuera de ciclo, no rompe el ritmo

- **Cuándo:** cuando la persona le pide algo a un agente directamente («repasa este hilo», «ya tienes turno», «haz este PR») fuera de la franja de ese agente en el ciclo.
- **Qué hacer:** se hace en el momento, en rama propia y con PR, sin esperar a la franja. Lo que sale de ahí (el mensaje del hilo, el PR) va marcado «fuera de ciclo», y la medición del ritmo lo cuenta aparte, no como vuelta rota. Dentro del ciclo, lo que necesita el sí de la persona se prepara al principio de la franja para que salga dentro de ella. Pieza: [protocolo, «Ritmo»](../../nucleo/protocolo.md#ritmo).
- **Pruebas:** en el primer ciclo medido con el ritmo nuevo, ningún hilo dio la vuelta entera porque un agente escribió fuera de su hora. Sus dos mensajes no salieron de su rutina programada, sino de dos tareas que la persona le pidió directamente; en los dos el turno era suyo, y cada escritura salió cuando la persona la aprobó.
- **Seguridad:** media. Se vio un solo día, con dos mensajes, y la causa se entiende: no había regla para lo que pide la persona fuera de ciclo, y eso le puede pasar a cualquier agente.

## Qué pasó, en llano

Es como una cocina que saca los platos en un orden fijo. Si el dueño pide un café en mitad del servicio, se le sirve en el momento, sin esperar al siguiente plato. Y quien cuenta si los platos salieron en orden no cuenta el café como un fallo de la cadena.

## Qué cambió en el harness

- **Descartado:** trabajar lo pedido al momento pero dejar el mensaje del hilo y el paso de turno para la franja propia. La atención de la persona vale más que las llamadas: el ritmo es para pasarse el turno entre agentes, no para frenarla.
- **Entró en el protocolo:** «Lo que pide la persona va fuera de ciclo».
- **La marca:** sin ella, quien mide no puede separar un pedido de la persona de una vuelta rota. Propuesto: que `equipo.py escribir` ponga la marca sola, para que no dependa de acordarse ([lección 009](009-la-firma-que-dependia-de-acordarse.md)).
