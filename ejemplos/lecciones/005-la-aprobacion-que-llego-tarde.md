# 005 · La aprobación que llegó tarde

- **Cuándo:** cuando una acción preparada para GitHub (abrir un PR, empujar una rama, cambiar una base, comentar) lleva horas esperando el sí de la persona y por fin se va a ejecutar.
- **Qué hacer:** justo antes de ejecutarla, compararla con el estado actual: ¿lo que trae ya está en `main`? ¿el PR sigue abierto y con la misma base? Si algo cambió, no se lanza: se descarta y se cuenta en el hilo en una línea. Pieza: [protocolo, «Turnos», punto 6](../../nucleo/protocolo.md#turnos).
- **Pruebas:** la apertura de un PR con un paquete de código se preparó un viernes y se aprobó el lunes. Mientras tanto, el mismo paquete había entrado en `main` por otro PR. El PR nuevo se abrió y se cerró tres minutos después, sin fusionar y con conflictos: reabrirlo habría quitado código.
- **Seguridad:** media. Se vio una vez con este resultado y otra parecida ([lección 006](006-dos-revisiones-la-misma-accion.md)). El mecanismo se entiende: la acción es una foto del momento en que se preparó.

## Qué pasó, en llano

Una acción esperando aprobación es como una carta escrita el viernes y echada al buzón el lunes: dice lo que era verdad el viernes. Entre medias el equipo siguió trabajando y la carta llegó sobrando.

## Qué cambió en el harness

La aprobación de la persona dice «sí a esto», no «sí pase lo que pase». Por eso la comprobación va justo antes de ejecutar, no al preparar. Es barata, una consulta, y evita PR fantasma y ruido en los hilos.
