# Núcleo

El protocolo genérico del equipo: turnos, responsable de cada hilo, registro de decisiones, flags y reglas de lo público, con una plantilla vacía del registro y el glosario. En el núcleo van roles, no nombres.

El resto llega en el PR de contenido. Estas dos reglas de lo público ya están en vigor, porque la Action [`lo-publico.yml`](../.github/workflows/lo-publico.yml) las aplica desde ahora.

## Reglas de lo público

- **Un secreto que llega a un commit se avisa y se rota.** Vale aunque se corrija en el commit siguiente. Borrarlo no basta: el commit sigue a la vista en el PR, porque GitHub guarda la cabeza de cada PR aunque se borre la rama, y el *squash* solo limpia `main`. Quien lo vea avisa a la persona dueña del secreto, y esa persona lo revoca y crea uno nuevo antes de seguir. Por eso la Action revisa en cada PR las líneas añadidas de cada commit y sus mensajes, no solo cómo queda el árbol al final.
- **El mensaje del *squash* dice qué entra, no quién lo aprobó ni dónde.** Se escribe al fusionar y no pasa por la revisión del PR, así que lo que diga queda publicado en `main` tal cual. Quien fusiona escribe solo el cambio: ni nombres de quien dio el visto bueno, ni canales, chats o fechas de conversaciones. La Action revisa en cada push a `main` los commits que acaban de entrar, mensajes incluidos, pero eso solo lo descubre cuando ya está publicado.
- **Los issues de este repo se enlazan, no se numeran como hilos.** Se escribe el enlace al issue (`issues/N`) y nunca la palabra «hilo» seguida de `#N`. Esa forma es la de los hilos del canal privado de un equipo, y la Action la bloquea siempre, también cuando señala un issue de aquí.
