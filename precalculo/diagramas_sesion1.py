"""Diagrama «población y muestra» de la Sesión 1, con las cifras reales del caso.

    python precalculo/diagramas_sesion1.py

Lee precalculo/salidas_sesion1.json (μ y el primer x̄) y escribe
fuente/diapositivas/recursos/s1/poblacion-muestra.svg. Los puntos son ilustrativos:
120 puntos representan los 12 000 pedidos, y 12 resaltados, la muestra.
"""

import json
import random
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
MORADO, NARANJA_TEXTO, NARANJA, PIZARRA = "#691E7A", "#B84A00", "#F46201", "#566B7F"


def coma(x):
    return f"{x}".replace(".", ",")


def main():
    salidas = json.loads((AQUI / "salidas_sesion1.json").read_text(encoding="utf-8"))
    mu = re.search(r"μ = ([\d.]+)", salidas["parametro"]).group(1)
    x_barra = re.search(r"x̄ = ([\d.]+)", salidas["parametro"]).group(1)

    az = random.Random(7)
    elegidos = set(az.sample(range(120), 12))
    puntos = []
    for i in range(120):
        fila, col = divmod(i, 15)
        x, y = 34 + col * 20.5, 62 + fila * 21
        color = NARANJA if i in elegidos else "#C9B3CF"
        puntos.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.2" fill="{color}" />')
    muestra = []
    for k, _ in enumerate(sorted(elegidos)):
        fila, col = divmod(k, 4)
        muestra.append(f'<circle cx="{560 + col * 22}" cy="{96 + fila * 22}" r="6.2" fill="{NARANJA}" />')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 300" width="100%" role="img" aria-labelledby="pm-titulo pm-desc">
  <title id="pm-titulo">Población, muestra, parámetro y estadístico</title>
  <desc id="pm-desc">A la izquierda, la población: los 12 000 pedidos del semestre, cuya media de tiempo de
    entrega es el parámetro mu, {coma(mu)} minutos. Una flecha de muestreo aleatorio lleva a la derecha, a una
    muestra de 100 pedidos, cuya media es el estadístico x barra, {coma(x_barra)} minutos. Una flecha punteada
    de regreso indica la inferencia: usar el estadístico para estimar el parámetro.</desc>
  <defs>
    <marker id="pm-flecha" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
      <path d="M0,0 L8,3.5 L0,7 z" fill="{PIZARRA}" />
    </marker>
  </defs>
  <rect x="12" y="14" width="350" height="272" rx="14" fill="#FAF6FB" stroke="{MORADO}" stroke-width="1.8" />
  <text x="187" y="40" text-anchor="middle" font-size="16" font-weight="700" fill="{MORADO}">Población · N = 12 000 pedidos</text>
  {"".join(puntos)}
  <text x="187" y="248" text-anchor="middle" font-size="14" fill="#334155">parámetro</text>
  <text x="187" y="272" text-anchor="middle" font-size="18" font-weight="700" fill="{MORADO}">μ = {coma(mu)} min</text>

  <rect x="520" y="54" width="128" height="134" rx="14" fill="#FDF0E6" stroke="{NARANJA_TEXTO}" stroke-width="1.8" />
  <text x="584" y="40" text-anchor="middle" font-size="16" font-weight="700" fill="{NARANJA_TEXTO}">Muestra · n = 100</text>
  {"".join(muestra)}
  <text x="584" y="218" text-anchor="middle" font-size="14" fill="#334155">estadístico</text>
  <text x="584" y="242" text-anchor="middle" font-size="18" font-weight="700" fill="{NARANJA_TEXTO}">x̄ = {coma(x_barra)} min</text>

  <path d="M372,98 C420,80 470,80 510,98" fill="none" stroke="{PIZARRA}" stroke-width="2" marker-end="url(#pm-flecha)" />
  <text x="441" y="74" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">muestreo aleatorio</text>
  <path d="M510,170 C470,192 420,192 372,170" fill="none" stroke="{PIZARRA}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#pm-flecha)" />
  <text x="441" y="208" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">inferencia</text>
  <text x="441" y="226" text-anchor="middle" font-size="12" fill="#475569">¿qué dice x̄ sobre μ?</text>
</svg>
"""
    destino = RAIZ / "fuente/diapositivas/recursos/s1/poblacion-muestra.svg"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(svg, encoding="utf-8")
    print("Diagrama:", destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
