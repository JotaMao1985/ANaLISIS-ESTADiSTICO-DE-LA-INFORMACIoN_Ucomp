"""Comprueba que las salidas (#>) proyectadas coinciden con la ejecución real.

    python precalculo/verifica_diapositivas.py 1

Para cada bloque ```python [id] de fuente/diapositivas/sesionN.md, compara sus
líneas #> con precalculo/salidas_sesionN.json (sin espacios al final). Una salida
partida en dos líneas en la diapositiva se acepta si, unida, coincide.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def normal(texto):
    return re.sub(r"\s+", " ", texto).strip()


def main(n):
    salidas = json.loads((RAIZ / f"precalculo/salidas_sesion{n}.json").read_text(encoding="utf-8"))
    fuente = (RAIZ / f"fuente/diapositivas/sesion{n}.md").read_text(encoding="utf-8")
    errores = 0
    for ident, cuerpo in re.findall(r"```python \[(\w+)\][^\n]*\n(.*?)```", fuente, re.S):
        proyectada = [l[2:] for l in cuerpo.split("\n") if l.startswith("#>")]
        if not proyectada:
            continue
        real = salidas.get(ident)
        if real is None:
            print(f"✗ [{ident}]: no está en salidas_sesion{n}.json")
            errores += 1
        elif normal(" ".join(proyectada)) != normal(real):
            print(f"✗ [{ident}]: la salida proyectada no coincide\n  diapositiva: {normal(' '.join(proyectada))}\n  real:        {normal(real)}")
            errores += 1
        else:
            print(f"✓ [{ident}]")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
