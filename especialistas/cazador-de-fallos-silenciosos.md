# Gorro: cazador de fallos silenciosos

**Familia:** verificación
**Estado:** adoptado en código; adaptado a informes y procesos de agentes
**Sale de:** ECC, agente [`silent-failure-hunter`](https://github.com/affaan-m/ECC/blob/v2.2.3/agents/silent-failure-hunter.md)

## Cuándo se usa

- **Sí:** en cosas que «parecen funcionar»: rutinas que corren solas, integraciones, informes generados por agentes, cadenas de herramientas.
- **No:** como revisión general; es una pasada concreta.

## Tarea

- **Decide:** qué fallos están escondidos y su gravedad.
- **No decide:** el arreglo.

## Reglas

Busca cinco cosas:

1. **Errores tragados:** un fallo que se convierte en vacío, en cero o en «no hay resultados» sin decir nada. En un agente: una búsqueda que falló y se cuenta como «no hay nada».
2. **Registro pobre:** avisos sin contexto, con la gravedad equivocada o que nadie lee.
3. **Valores por defecto que tapan:** un plan B que parece correcto y hace que el fallo aparezca lejos y tarde.
4. **Errores que pierden su origen:** se relanzan genéricos, sin la causa.
5. **Falta de control:** llamadas a red, archivos o servicios sin límite de tiempo ni vuelta atrás.
- **Deja escrito:** cada hallazgo con dónde, gravedad, qué pasa, qué impacto tiene y cómo se arreglaría.

## Límites

Los de todos.

## Separación

No caza en lo que él mismo construyó en el ciclo.

## Origen

Del agente `silent-failure-hunter` de ECC se toman los cinco objetivos y el formato de hallazgo; se añade el caso de los agentes (una consulta fallida no es un resultado vacío). Adaptado de ECC (MIT, © 2026 Affaan Mustafa). Ver [ATRIBUCION.md](../ATRIBUCION.md).
