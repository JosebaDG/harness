# 008 · La decisión que no llegó a la skill

- **Cuándo:** cuando una decisión cambia cómo trabaja una skill o qué herramienta usa («se hace con X», «se apunta en la skill Y»), y varios agentes tienen una skill con el mismo nombre.
- **Qué hacer:** la línea del registro separa el objetivo (lo que decidió la persona y vale para todos) del medio (la herramienta o el cambio de skill de un agente). Si nombra skills, dice de quién son. Si pide una herramienta, dice dónde vive. Así cada agente sabe por la línea si le toca, sin abrir un hilo para preguntarlo. Pieza: el campo «dónde» de `equipo.py apunta`.
- **Pruebas:** una línea decía «lecturas siempre con una herramienta concreta, nunca con curl» y «se apunta en las skills» con tres nombres que tenían todos los agentes. Pero esa herramienta solo vivía en la máquina de un agente, y los demás leían con curl. En el hilo se aclaró que el objetivo de la persona era que leer nunca le pidiera permiso; la herramienta era el medio de un agente. Para todos valía curl de solo lectura, nunca con datos. Se apuntó así en una línea nueva.
- **Seguridad:** baja. Se resolvió en una vuelta del hilo y no hizo daño. Habría sido peor si alguien hubiera cambiado su skill a una herramienta que no tiene.

## Qué pasó, en llano

Es como un aviso en la puerta de la cocina que dice «a partir de hoy, el café con la cafetera nueva», cuando la cafetera nueva solo está en una de las cocinas. Lo que se quería era que nadie se quedara sin café. Los demás seguían con la de siempre, que también lo cumplía, pero el aviso no lo decía.

## Qué cambió en el harness

Nada en las herramientas ni en el protocolo: la regla va en el «dónde» de la línea, que ya se escribe siempre. Si vuelve a pasar, se valora que `apunta` pida el dueño cuando el «dónde» nombre una skill. Familia: [lección 007](007-la-conversacion-que-se-apunto-como-decision.md); las dos tratan de que la línea diga más o menos de lo que se decidió.
