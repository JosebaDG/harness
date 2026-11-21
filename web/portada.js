// La escena viva de la portada. Sin dependencias y sin aleatoriedad: todo lo que se ve es una función
// pura del estado (tiempo de ambiente acumulado, progreso del desplazamiento y turnos pasados a mano).
//
// Harness: el punto (la persona) en el fondo del pozo de la malla; el equipo en órbita; el relevo es una
// luz que viaja de un agente al siguiente como un turno. Al llegar, el agente se enciende y escribe
// (una línea al punto). Cuando el relevo completa la vuelta, el punto late.
// Wiki: una estantería; el punto salta de libro en libro leyendo, enlaza conceptos con un arco y, al
// final de la fila, deja un libro nuevo en el hueco.
//
// El desplazamiento es el reloj: al bajar, la cámara sube sobre la órbita y el relevo avanza; al subir,
// retrocede. Tocar la escena pasa el turno. Con «reducir movimiento» no hay animación: se pinta un
// fotograma quieto y tocar sigue pasando el turno. El botón de pausa para todo (WCAG 2.2.2).
(() => {
  const caja = document.querySelector(".escena-caja");
  if (!caja) return;
  const svg = caja.querySelector("svg");
  const boton = caja.querySelector(".escena-pausa");
  const NS = "http://www.w3.org/2000/svg";
  const quieto = matchMedia("(prefers-reduced-motion: reduce)");
  const $ = (sel) => svg.querySelector(sel);
  const $$ = (sel) => [...svg.querySelectorAll(sel)];
  const pon = (el, attrs) => { for (const k in attrs) el.setAttribute(k, attrs[k]); };
  const f = (n) => Math.round(n * 10) / 10;
  const sat = (x) => Math.min(1, Math.max(0, x));
  const suave = (x) => { x = sat(x); return x * x * (3 - 2 * x); };
  const salida = (x) => 1 - Math.pow(1 - sat(x), 3);
  const TAU = Math.PI * 2;

  // ---------- Harness ----------
  function harness() {
    const C = { x: 180, y: 150 }, N_ANILLOS = 7, N_RADIOS = 12, T = 3.6, LLEGA = 0.55;
    const anillos = $$(".anillo"), radios = $$(".radio"), agentes = $$(".agente");
    const detras = $(".detras"), delante = $(".delante");
    const estela = $(".estela"), cabeza = $(".cabeza"), lazo = $(".lazo"), onda = $(".onda"), punto = $(".punto"), halo = $(".halo");
    const pozo = (u, s, golpe) => ({ rx: 26 + u * 150, ry: (26 + u * 150) * (0.3 + 0.1 * s), cy: C.y - (44 + 14 * s) * Math.pow(u, 0.8) * (1 - 0.12 * golpe) });
    const orbita = (s, dx) => ({ x: C.x + dx, y: 124 - 6 * s, rx: 122, ry: 34 + 30 * s });
    return function pinta(e) {
      const s = e.s, rot = e.rot + s * Math.PI * 0.75;
      const turnos = e.turnos, k = Math.floor(turnos), p = turnos - k;
      const viaje = suave(p / LLEGA), llegado = p >= LLEGA, tras = (p - LLEGA) / (1 - LLEGA);
      const activo = ((llegado ? k + 1 : k) % 4 + 4) % 4;
      const vuelta = ((k + 1) % 4 + 4) % 4 === 0;
      const golpe = llegado && vuelta ? Math.sin(Math.PI * sat(tras * 1.6)) : 0;
      // el pozo: anillos que fluyen hacia el punto y radios que giran despacio
      anillos.forEach((a, i) => {
        const u = ((i + e.flujo) / N_ANILLOS) % 1, w = pozo(u, s, golpe);
        pon(a, { rx: f(w.rx), ry: f(w.ry), cy: f(w.cy), "stroke-opacity": (0.55 * Math.sin(Math.PI * u)).toFixed(3) });
      });
      radios.forEach((r, i) => {
        const fi = (i / N_RADIOS) * TAU + rot * 0.25;
        let d = "";
        for (let j = 0; j <= 8; j++) {
          const u = 0.06 + (j / 8) * 0.94, w = pozo(u, s, golpe);
          d += (j ? "L" : "M") + f(C.x + w.rx * Math.cos(fi)) + " " + f(w.cy + w.ry * Math.sin(fi));
        }
        r.setAttribute("d", d);
      });
      // el equipo en órbita: delante o detrás del punto según su profundidad
      const o = orbita(s, e.dx), en = (th) => ({ x: o.x + o.rx * Math.cos(th), y: o.y + o.ry * Math.sin(th), z: Math.sin(th) });
      const pos = [];
      agentes.forEach((g, i) => {
        const q = en(rot + i * TAU / 4); pos.push(q);
        const esc = 0.72 + 0.4 * (q.z + 1) / 2, on = i === activo;
        const nucleo = g.querySelector(".nucleo"), aura = g.querySelector(".aura"), anillo = g.querySelector(".llamada");
        pon(nucleo, { cx: f(q.x), cy: f(q.y), r: f(9 * esc * (on ? 1.18 : 1)) });
        pon(aura, { cx: f(q.x), cy: f(q.y), r: f(9 * esc * (on ? 2.6 : 1.7)), "fill-opacity": on ? 0.3 : 0.12 });
        const rr = on && llegado ? salida(tras) : 1;
        pon(anillo, { cx: f(q.x), cy: f(q.y), r: f(9 * esc * (1 + 3 * rr)), "stroke-opacity": (on && llegado ? 0.9 * (1 - rr) : 0).toFixed(3) });
        g.setAttribute("opacity", (0.55 + 0.45 * (q.z + 1) / 2).toFixed(3));
        const capa = q.z > 0 ? delante : detras;
        if (g.parentNode !== capa) capa.appendChild(g);
      });
      // el relevo: una luz con estela que viaja al siguiente agente
      const th0 = rot + (k % 4) * TAU / 4, th = th0 + viaje * TAU / 4;
      let d = "";
      for (let j = 0; j <= 10; j++) {
        const a = Math.max(th0, th - 0.95) + (j / 10) * (th - Math.max(th0, th - 0.95));
        const q = en(a); d += (j ? "L" : "M") + f(q.x) + " " + f(q.y);
      }
      const brillo = llegado ? 1 - salida(tras * 2) : Math.min(1, p / 0.08);
      pon(estela, { d, "stroke-opacity": (0.85 * brillo).toFixed(3) });
      const h = en(th);
      pon(cabeza, { cx: f(h.x), cy: f(h.y), "fill-opacity": brillo.toFixed(3) });
      // quien tiene el turno escribe: una línea de su color hasta el punto
      const pa = pos[activo];
      pon(lazo, { x1: f(pa.x), y1: f(pa.y), x2: C.x, y2: C.y, stroke: agentes[activo].dataset.color,
                  "stroke-opacity": (0.25 + 0.5 * (llegado ? 1 - salida(tras) : 0.4)).toFixed(3) });
      // el punto respira y late al cerrar la vuelta
      const latido = 1 + 0.035 * Math.sin(e.amb * 1.6) + 0.32 * golpe;
      punto.setAttribute("r", f(11 * latido));
      halo.setAttribute("r", f(40 * (1 + 0.15 * golpe)));
      const oa = llegado && vuelta ? salida(tras) : 1;
      pon(onda, { r: f(11 * (1 + 3.2 * oa)), "stroke-opacity": (llegado && vuelta ? 0.75 * (1 - oa) : 0).toFixed(3) });
    };
  }

  // ---------- Wiki ----------
  function wiki() {
    const libros = $$(".libro"), estante = 246, H = 1.15;
    const datos = libros.map((b) => ({ x: +b.dataset.x, w: +b.dataset.w, h: +b.dataset.h }));
    const n = datos.length - 1; // el último es el hueco que se llena
    const punto = $(".punto"), onda = $(".onda"), arco = $(".arco"), luz = $(".luz"), hueco = $(".hueco");
    const centro = (i) => datos[i].x + datos[i].w / 2, cima = (i) => estante - datos[i].h;
    const CICLO = n + 2; // n saltos por la fila, dejar el libro nuevo, y volver al principio en un arco largo
    return function pinta(e) {
      const t = ((e.turnos % CICLO) + CICLO) % CICLO, j = Math.floor(t), q = t - j, qe = suave(q);
      let x, y, enLibro = -1, nuevo = 0, aterriza = 0;
      if (j < n - 1) { // de libro j a libro j+1
        const ya = cima(j) - 18, yb = cima(j + 1) - 18;
        x = centro(j) + (centro(j + 1) - centro(j)) * qe;
        y = ya + (yb - ya) * qe - 30 * Math.sin(Math.PI * q);
        enLibro = q > 0.85 ? j + 1 : (q < 0.15 ? j : -1);
        aterriza = q > 0.85 ? (q - 0.85) / 0.15 : 0;
      } else if (j === n - 1) { // del último libro al hueco: deja el libro nuevo
        const ya = cima(n - 1) - 18, yb = cima(n) - 18;
        x = centro(n - 1) + (centro(n) - centro(n - 1)) * qe;
        y = ya + (yb - ya) * qe - 30 * Math.sin(Math.PI * q);
        nuevo = salida((q - 0.45) / 0.55);
      } else { // vuelta al principio en un arco alto; el libro nuevo se queda y luego se archiva
        x = centro(n) + (centro(0) - centro(n)) * qe;
        const ya = cima(n) - 18, yb = cima(0) - 18;
        y = ya + (yb - ya) * qe - 70 * Math.sin(Math.PI * q);
        nuevo = 1 - suave((q - 0.7) / 0.3);
      }
      const s = e.s;
      libros.forEach((b, i) => {
        const dd = datos[i];
        let alza = 0, op = i % 2 ? 0.88 : 0.6;
        if (i === n) { op = 0.95 * nuevo; }
        const cerca = Math.abs(centro(i) - x) < dd.w / 2 + 3;
        if (i < n && cerca) { alza = 6 + 4 * s; op = 1; }
        const h = i === n ? dd.h * nuevo : dd.h;
        const rect = b.querySelector("rect"), raya = b.querySelector("line");
        pon(rect, { y: f(estante - h - alza), height: f(Math.max(0, h)), "fill-opacity": op.toFixed(3) });
        pon(raya, { y1: f(estante - h - alza + 16), y2: f(estante - h - alza + 16), "stroke-opacity": h > 20 ? 0.45 : 0 });
      });
      hueco.setAttribute("stroke-opacity", (0.5 * (1 - nuevo)).toFixed(3));
      punto.setAttribute("cx", f(x)); punto.setAttribute("cy", f(y));
      punto.setAttribute("r", f(6.5 * (1 + 0.04 * Math.sin(e.amb * 1.6))));
      onda.setAttribute("cx", f(x)); onda.setAttribute("cy", f(y));
      const oa = aterriza > 0 ? salida(aterriza) : (j === n - 1 ? salida((q - 0.5) / 0.5) : 0);
      pon(onda, { r: f(6.5 * (1 + 2.6 * oa)), "stroke-opacity": (oa > 0 && oa < 1 ? 0.7 * (1 - oa) : 0).toFixed(3) });
      pon(luz, { cx: f(x), rx: f(26 + 8 * Math.sin(Math.PI * q)) });
      // el enlace: al llegar a un libro, un arco lo une con otro anterior (un concepto que cita una fuente)
      const actual = j < n - 1 ? j + 1 : -1, otro = actual >= 0 ? actual - 2 - (actual % 3) : -1;
      if (otro >= 0) {
        const xa = centro(otro), xb = centro(actual), ya = cima(otro) - 4, yb = cima(actual) - 4;
        const alto = Math.min(ya, yb) - 26 - 4 * (actual - otro);
        arco.setAttribute("d", "M" + f(xa) + " " + f(ya) + "Q" + f((xa + xb) / 2) + " " + f(alto) + " " + f(xb) + " " + f(yb));
        arco.setAttribute("stroke", libros[actual].querySelector("rect").getAttribute("fill"));
        const vis = q < 0.85 ? Math.sin(Math.PI * sat(q / 0.85)) : 0;
        arco.setAttribute("stroke-opacity", (0.75 * vis).toFixed(3));
        arco.setAttribute("stroke-dashoffset", f(60 * (1 - suave(q / 0.4))));
      } else arco.setAttribute("stroke-opacity", "0");
    };
  }

  const pinta = svg.dataset.escena === "wiki" ? wiki() : harness();
  const inicio = { harness: { rot: +svg.dataset.rot || 0, turnos: +svg.dataset.turnos || 0 }, wiki: { rot: 0, turnos: +svg.dataset.turnos || 0 } }[svg.dataset.escena || "harness"];
  const est = { amb: 0, flujo: 0, rot: inicio.rot, turnos: inicio.turnos, s: 0, sObj: 0, dx: 0, dxObj: 0 };
  let pausa = false, visible = true, raf = 0, antes = 0;

  const progreso = () => {
    const r = caja.getBoundingClientRect(), alto = r.height + Math.max(0, r.top + scrollY);
    return sat(scrollY / Math.max(1, alto));
  };
  const anima = () => !quieto.matches && !pausa && visible && !document.hidden;
  function cuadro(ahora) {
    raf = 0;
    const dt = antes ? Math.min(0.05, (ahora - antes) / 1000) : 0;
    antes = ahora;
    est.amb += dt; est.flujo += dt * 0.11; est.rot += dt * TAU / 30;
    est.sObj = progreso();
    const ds = est.sObj - est.s;
    est.s += ds * Math.min(1, dt * 6);
    est.turnos += dt / (svg.dataset.escena === "wiki" ? 1.15 : 3.6) + ds * (svg.dataset.escena === "wiki" ? 6 : 2) * Math.min(1, dt * 6);
    est.dx += (est.dxObj - est.dx) * Math.min(1, dt * 4);
    pinta(est);
    if (anima()) raf = requestAnimationFrame(cuadro); else antes = 0;
  }
  const arranca = () => { if (!raf && anima()) raf = requestAnimationFrame(cuadro); };
  const repinta = () => { if (!anima()) { est.s = est.sObj = quieto.matches ? 0 : progreso(); pinta(est); } };

  // Tocar la escena pasa el turno: el relevo llega ya al siguiente
  caja.addEventListener("pointerdown", (ev) => {
    if (ev.target.closest(".escena-pausa")) return;
    const k = Math.floor(est.turnos), p = est.turnos - k;
    if (svg.dataset.escena === "wiki") est.turnos = p < 0.9 ? k + 0.9 : k + 1.9;
    else est.turnos = p < 0.55 ? k + 0.551 : k + 1.551;
    pinta(est); arranca();
  });
  if (matchMedia("(pointer: fine)").matches) {
    caja.addEventListener("pointermove", (ev) => { const r = caja.getBoundingClientRect(); est.dxObj = ((ev.clientX - r.left) / r.width - 0.5) * 20; arranca(); });
    caja.addEventListener("pointerleave", () => { est.dxObj = 0; arranca(); });
  }
  if (boton) {
    const marca = () => {
      boton.setAttribute("aria-pressed", String(pausa));
      boton.setAttribute("aria-label", pausa ? "Reanudar la animación" : "Pausar la animación");
      boton.hidden = quieto.matches;
    };
    boton.addEventListener("click", () => { pausa = !pausa; marca(); if (pausa) repinta(); else arranca(); });
    quieto.addEventListener("change", () => { marca(); repinta(); arranca(); });
    marca();
  }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([x]) => { visible = x.isIntersecting; arranca(); }).observe(caja);
  }
  document.addEventListener("visibilitychange", arranca);
  addEventListener("scroll", () => { if (anima()) arranca(); }, { passive: true });
  svg.classList.add("viva");
  pinta(est);
  arranca();
})();

// Copiar la orden de clonar: el botón solo aparece si el navegador deja copiar
(() => {
  const boton = document.querySelector(".copiar");
  const orden = document.querySelector(".clonar .orden");
  const aviso = document.querySelector(".copiado");
  if (!boton || !orden || !(navigator.clipboard && window.isSecureContext)) return;
  boton.hidden = false;
  boton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(orden.textContent.trim());
      boton.textContent = "Copiado"; if (aviso) aviso.textContent = "Orden copiada";
    } catch (e) {
      boton.textContent = "No se pudo"; if (aviso) aviso.textContent = "No se ha podido copiar";
    }
    setTimeout(() => { boton.textContent = "Copiar"; if (aviso) aviso.textContent = ""; }, 2200);
  });
})();
