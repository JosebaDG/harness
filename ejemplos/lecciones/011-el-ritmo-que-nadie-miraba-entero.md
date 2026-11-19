# 011 · El ritmo que nadie miraba entero

- **Cuándo:** cuando cada agente tiene su propia rutina y se comprueba que cada una se ejecuta, pero nadie mira si juntas hacen avanzar los hilos.
- **Qué hacer:** medir el flujo y no solo las ejecuciones: cuántas vueltas completas da un hilo por ciclo y dónde se para. Los horarios se diseñan juntos, en el orden de los turnos, y van en la configuración del equipo, no en la memoria de cada rutina. Pieza: [protocolo, «Ritmo»](../../nucleo/protocolo.md#ritmo) y la clave `ciclo` de la configuración de [`equipo.py`](../../herramientas/equipo.py).
- **Pruebas:** un agente revisaba una vez al día y los demás varias veces, cada uno a su hora. Un turno que le llegaba después de su revisión esperaba un día entero, y un hilo estuvo parado un día por eso. Todas las rondas salían «bien» en el registro de ejecuciones. Lo detectó la persona, no el sistema.
- **Seguridad:** baja en riesgo, alta en coste: llamadas gastadas en rondas desacompasadas y días perdidos sin que nadie lo viera.

## Qué pasó, en llano

Es como una cadena de montaje donde cada puesto funciona, pero uno abre a las nueve y cierra a las nueve y cuarto. Cada puesto dice «hoy he trabajado bien», y las piezas se amontonan delante del que cierra pronto.

## Qué cambió en el harness

- **Revisiones escalonadas en el orden del ciclo**, con unos minutos entre una y otra, y el coordinador el último. Una sola espera de como mucho 10 minutos dentro de una orden, salida rápida si no hay nada y nunca bucles.
- **El coordinador mide en cada cierre** las vueltas completas, dónde se rompen y las esperas usadas, y la persona decide si se ajusta.

## Seguimiento: el relevo que se perdió

Con el ritmo nuevo, un relevo se rompió: un agente terminó su turno unos minutos después de que empezara la revisión del siguiente, y el siguiente no lo vio hasta el ciclo después. El trabajo se retrasó un ciclo, pero no se perdió.

- **Causa confirmada:** la ronda del primero no se alargó por el trabajo de código, sino porque sus escrituras esperaron la aprobación de la persona. Y la espera única solo existía en el texto de cada rutina: nada le dijo al segundo que esperase. Se repitió al día siguiente con otra espera de aprobación.
- **Cambio:** `bandeja` saca `ESPERA ÚNICA` cuando un hilo tiene el turno del anterior del ciclo y este no ha escrito desde su hora; la condición la calcula la herramienta, no cada rutina. En la misma revisión entró `SIGUES TÚ`, para el agente que se queda un turno con un mensaje suyo: son dos líneas distintas porque piden cosas contrarias, esperar o actuar ya.
- **Límite aceptado:** `ESPERA ÚNICA` solo recoge lo que llega en 10 minutos o menos. Una aprobación más larga sigue rompiendo el relevo.
