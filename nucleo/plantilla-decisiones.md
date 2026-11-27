# Plantilla del registro

Copia lo que hay debajo de la línea en un `DECISIONES.md` en la raíz del repo del canal. `equipo.py apunta` añade las líneas y `equipo.py decisiones` las lee.

---

# Decisiones

- **Antes de pedir o hacer algo**, cualquier agente o rutina mira esto y las flags: `python3 equipo.py decisiones [tema]`. Si ya está decidido o aparcado, no se pide.
- **Si una skill, un mensaje programado, un documento o el cuerpo de un issue dice otra cosa, manda esto.** No se actúa sobre lo viejo: se avisa a la persona del desfase en una línea.
- **Se apunta en el mismo turno en que la persona decide**, aunque sea en un chat: `equipo.py apunta <estado> "tema: qué · quién · dónde · lo que le queda a la persona"`.
- **Cambiar una decisión:** la línea vieja pasa a `sustituido → AAAA-MM-DD` y la nueva va arriba. No se borra nada.
- **Aquí solo lo que sigue mandando** (normas, decisiones vigentes, lo aparcado y lo que espera a la persona). La crónica cumplida y lo sustituido se mueven tal cual a `DECISIONES-historico.md`, por tipo y nunca por fecha: una norma antigua sigue aquí. `decisiones` busca ahí cuando no encuentra nada vivo.

Estados: `decidido`, `aparcado`, `espera:<persona>` y `sustituido`.

<!-- Ejemplo inventado, bórralo al apuntar la primera decisión de verdad:
- 2030-01-15 · decidido · Web, idioma: solo español en la primera versión; el inglés se descartó hasta tener lectores que lo pidan · la persona; apunta Ana · enlace al issue · Persona: nada
-->

## Sustituidas
