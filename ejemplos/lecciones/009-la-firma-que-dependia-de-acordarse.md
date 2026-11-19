# 009 · La firma que dependía de acordarse

- **Cuándo:** cuando una regla de forma (la firma del commit, un formato, qué no se escribe en un mensaje) se tiene que cumplir en cada commit y su cumplimiento depende de que el agente se acuerde.
- **Qué hacer:** una regla que se rompe más de dos veces no se vuelve a recordar: se comprueba con una herramienta. Mientras no exista, quien hace el commit comprueba el autor justo después y avisa si falla.
- **Pruebas:** desde que se decidió la firma común, siete commits de un mismo agente salieron con otro autor, en tres tandas a lo largo de casi un mes. Cada vez se dijo «el siguiente ya va bien», y el siguiente iba bien, hasta el próximo.
- **Seguridad:** media. No se filtró nada, pero en un repo público una firma con un nombre de máquina o una dirección interna es información que no tiene que salir.

## Qué pasó, en llano

Es como dejarse las llaves puestas: cada vez prometes fijarte, y te fijas, hasta el día que no. La solución no es prometerlo con más fuerza, sino una puerta que no cierre si las llaves están puestas.

## Qué cambió en el harness

- **Hecho:** la skill de ese agente prohíbe cambiar el autor a mano y obliga a comprobarlo después de cada commit o fusión.
- **Propuesto, aún sin hacer:** que la comprobación automática de cada PR falle si un commit no lleva la firma acordada, y que `equipo.py` compruebe su propio commit al apuntar. Así la regla deja de depender de la memoria.
- **La misma idea ya se aplicó a lo público:** la Action [`lo-publico.yml`](../../.github/workflows/lo-publico.yml) revisa cada commit y su mensaje, no solo cómo quedan los archivos.
