# 007 · La conversación que se apuntó como decisión

- **Cuándo:** cuando un agente apunta en el registro una línea que dice que la persona decide algo, o que cambia el estado de algo `aparcado` o `decidido` (reactivar, aparcar, cambiar de rumbo), a partir de una conversación con ella.
- **Qué hacer:** la línea lleva lo que dijo la persona o un enlace a donde lo dijo, **y el estado tiene que estar en lo que dijo**. Si no dijo «reactiva», la línea no dice «reactiva»: se apunta lo que dijo y el estado de lo aparcado no se toca. Antes de enviar la línea, quien apunta compara su verbo con las palabras de la persona. Pieza: `equipo.py apunta` y la regla «Mismo turno» del [protocolo](../../nucleo/protocolo.md#el-registro-si-no-está-en-el-repo-no-existe).
- **Pruebas:** la persona habló con un agente de documentar un fallo de un aviso diario y de buscar alternativas. En el registro quedó como «se reactiva» esa parte del proyecto, que estaba aparcada. La línea llevaba sus palabras, pero esas palabras no decían reactivar. Una revisión trabajó durante días sobre esa línea hasta que la persona lo aclaró: no había reactivado nada.
- **Seguridad:** media. Visto una vez, pero el mecanismo es claro: la línea interpretó la conversación, y las rutinas leen el estado de la línea, no lo que dijo la persona. «Solo con sus palabras o un enlace» no lo habría evitado, porque estaban; lo que falla es que el estado vaya más allá de ellas.

## Qué pasó, en llano

El registro manda sobre todo lo demás, así que una palabra de más cambió lo que hacía el equipo. El trabajo en sí seguía valiendo, porque mantener el aviso era mantenimiento. Lo que estaba mal era el estado.

## Qué cambió en el harness

Ninguna regla nueva en el protocolo: si entra una, se busca otra que quitar. Es criterio de quien apunta, para que la persona no tenga que vigilar el registro para que no hable por ella. Familia: [lección 010](010-la-reaccion-que-se-apunto-como-decision.md).
