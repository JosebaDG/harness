# 003 · El mensaje viejo que salió por el nuevo

- **Cuándo:** cuando un agente escribe su mensaje en un archivo y lo publica con `equipo.py escribir`, `nuevo` o `cerrar`, sobre todo si reutiliza el mismo nombre de archivo de una ronda a otra.
- **Qué hacer:** escribir el archivo y enviarlo en dos pasos separados, nunca a la vez; un nombre de archivo nuevo cada vez; mirar la línea `EMPIEZA:` que enseña `equipo.py` al enviar. Pieza: [`equipo.py`](../../herramientas/equipo.py), que para si el archivo tiene más de 15 minutos (`--viejo` lo salta).
- **Pruebas:** una respuesta salió con el texto del día anterior y se corrigió menos de un minuto después. El agente había lanzado a la vez la orden de escribir el archivo y la de enviarlo, y el envío leyó el archivo antes de que se sobrescribiera. Otro agente publicó dos veces el mismo mensaje, con horas de diferencia.
- **Seguridad:** media. El primer caso está confirmado y se entiende la causa. El segundo encaja (un archivo viejo que se vuelve a enviar), pero no está confirmado.

## Qué pasó, en llano

Si las dos órdenes salen a la vez, puede ganar la segunda: se publica lo que había antes en el archivo. Nadie se equivocó al escribir; falló el orden.

## Qué cambió en el harness

| Medida | Por qué |
|---|---|
| Escribir y enviar en dos pasos | El envío siempre lee el archivo ya escrito |
| Un nombre de archivo nuevo cada vez | Si algo falla, no queda un mensaje viejo esperando a salir |
| `equipo.py` para si el archivo tiene más de 15 minutos | Es la pieza más barata que no se olvida: una regla en la skill se puede saltar, el script no |
| `equipo.py` enseña la primera línea al enviar | Un vistazo basta para ver si es el mensaje de ahora |

## Cómo se comprueba

En las rondas siguientes no debe salir ningún mensaje viejo ni repetido. Si `equipo.py` para un envío legítimo, se usa `--viejo` y se apunta, por si hay que subir el límite.
