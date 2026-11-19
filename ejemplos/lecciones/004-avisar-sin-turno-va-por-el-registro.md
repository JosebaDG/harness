# 004 · Avisar en un hilo sin turno va por el registro

- **Cuándo:** cuando hay que contar al equipo una decisión de la persona, el hilo del tema tiene el turno de otro agente y `equipo.py escribir` contesta `NO TE TOCA`.
- **Qué hacer:** no forzar el turno ni buscar otra vía (la API a mano, otro hilo). Se apunta en el registro con `equipo.py apunta`, y en la siguiente revisión de cada agente `bandeja` le avisa con `REGISTRO CAMBIADO`. Pieza: [protocolo, «El registro»](../../nucleo/protocolo.md#el-registro-si-no-está-en-el-repo-no-existe).
- **Pruebas:** pasó dos veces en dos días: un agente no pudo avisar en un hilo porque el turno era de otro, y lo apuntó en el registro. El agente que tenía el turno siguió lo apuntado: su siguiente entrega traía justo el primer paso que decía la línea.
- **Seguridad:** alta para que el aviso llega, porque `bandeja` avisa a todos cuando cambia el registro. Media para que se lea a tiempo: llega en la siguiente revisión de cada uno, no al momento.

## Qué pasó, en llano

El turno es como pasar la palabra en una reunión: solo habla quien la tiene. Que la herramienta no deje escribir no es un fallo, es la norma que evita que nos pisemos. Lo que faltaba era tener claro por dónde va el aviso.

## Qué cambió en el harness

Nada nuevo en las herramientas: el registro ya avisa solo. Cambia la lectura: `NO TE TOCA` deja de ser un error que hay que sortear y pasa a ser la señal de usar el registro. Así no se gasta tiempo ni llamadas buscando otra vía.
