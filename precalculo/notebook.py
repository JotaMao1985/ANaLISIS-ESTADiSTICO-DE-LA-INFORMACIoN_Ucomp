"""Notebook de Colab de una sesión, a partir de celdas_sesionN.py.

    python precalculo/notebook.py genera N     # escribe notebooks/sesion-N-….ipynb (sin salidas)
    python precalculo/notebook.py ejecuta N    # lo ejecuta con las soluciones y guarda
                                               # precalculo/salidas_sesionN.json y las gráficas
                                               # en fuente/diapositivas/recursos/sN/<id>.svg

- La celda «generador» lleva dentro genera_datos.py, ayudas.py y ayudas_sesionN.py como
  formulario oculto de Colab (#@title): el estudiante la ejecuta sin leerla y los datos se
  crean en /content/datos.
- Las celdas «solucion» no van al notebook; al ejecutar, sustituyen a las «plantilla».
- Las celdas «precalculo» tampoco van al notebook: calculan las cifras que las diapositivas
  citan en el texto, para que ninguna se escriba a mano.
- Cada celda de código lleva «# [id]», el mismo identificador del código proyectado.

Ejecutar necesita nbformat, nbclient y el kernel «replica-colab» (ipykernel install --prefix
<venv> --name replica-colab); el entorno que replica Colab (Python 3.13,
pandas 2.2.3, numpy 2.1.3) está descrito en el PLAN.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SESIONES = {
    1: "sesion-1-del-dato-a-la-pregunta.ipynb",
    2: "sesion-2-de-las-filas-a-la-distribucion.ipynb",
    3: "sesion-3-lo-tipico-y-lo-variable.ipynb",
    4: "sesion-4-lo-que-se-sale-de-lo-normal.ipynb",
}

# Al ejecutar (no en el notebook del estudiante): las gráficas salen en SVG con texto real,
# para proyectarlas nítidas y con la tipografía de las diapositivas.
PRELUDIO = """%config InlineBackend.figure_formats = ["svg"]
import matplotlib as mpl
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["svg.hashsalt"] = "tingua"
"""


def leer_celdas(ruta):
    celdas, actual = [], None
    for linea in ruta.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"# %%(?: (\[markdown\]|\S+)(.*))?$", linea)
        if m:
            if actual:
                celdas.append(actual)
            if m.group(1) == "[markdown]":
                actual = {"tipo": "markdown", "id": None, "banderas": set(), "lineas": []}
            else:
                actual = {"tipo": "code", "id": m.group(1), "banderas": set(m.group(2).split()), "lineas": []}
            continue
        if actual is None:
            continue  # comentarios de cabecera del archivo
        if actual["tipo"] == "markdown":
            linea = linea[2:] if linea.startswith("# ") else linea.lstrip("#")
        actual["lineas"].append(linea)
    celdas.append(actual)
    for c in celdas:
        c["fuente"] = "\n".join(c.pop("lineas")).strip("\n")
    return celdas


def _codigo_oculto(numero):
    partes = []
    for nombre in ("genera_datos.py", "ayudas.py", f"ayudas_sesion{numero}.py"):
        codigo = (AQUI / nombre).read_text(encoding="utf-8")
        partes.append(codigo.split('\nif __name__ == "__main__":')[0].rstrip())
    titulo = '#@title ▶ Crea los datos del caso (ejecútala sin modificar) { display-mode: "form" }'
    return titulo + "\n" + "\n\n\n".join(partes) + "\n\n"


def _lineas(texto):
    lineas = texto.split("\n")
    return [l + "\n" for l in lineas[:-1]] + [lineas[-1]]


def armar(numero, para_ejecutar=False):
    celdas_nb = []
    for i, c in enumerate(leer_celdas(AQUI / f"celdas_sesion{numero}.py")):
        ident = f"c{i:03d}"
        if c["tipo"] == "markdown":
            celdas_nb.append({"cell_type": "markdown", "id": ident, "metadata": {},
                              "source": _lineas(c["fuente"])})
            continue
        if ("solucion" in c["banderas"]) != para_ejecutar and {"solucion", "plantilla"} & c["banderas"]:
            continue
        if "precalculo" in c["banderas"] and not para_ejecutar:
            continue
        metadata = {"etiqueta": c["id"]} if para_ejecutar else {}
        if "generador" in c["banderas"]:
            fuente = _codigo_oculto(numero) + c["fuente"]
            metadata["cellView"] = "form"
        else:
            fuente = f"# [{c['id']}]\n{c['fuente']}"
        celdas_nb.append({"cell_type": "code", "execution_count": None, "id": ident,
                          "metadata": metadata, "outputs": [], "source": _lineas(fuente)})
    if para_ejecutar:
        celdas_nb.insert(0, {"cell_type": "code", "execution_count": None, "id": "preludio",
                             "metadata": {"etiqueta": "_preludio"}, "outputs": [],
                             "source": _lineas(PRELUDIO)})
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "cells": celdas_nb,
    }


def genera(numero):
    destino = RAIZ / "notebooks" / SESIONES[numero]
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps(armar(numero), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Notebook:", destino.relative_to(RAIZ))


def ejecuta(numero):
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.reads(json.dumps(armar(numero, para_ejecutar=True)), as_version=4)
    with tempfile.TemporaryDirectory() as carpeta:  # carpeta limpia, como un Colab recién abierto
        NotebookClient(nb, timeout=120, kernel_name="replica-colab",
                       resources={"metadata": {"path": carpeta}}).execute()
    salidas, graficas = {}, []
    carpeta_graficas = RAIZ / "fuente" / "diapositivas" / "recursos" / f"s{numero}"
    for celda in nb.cells:
        if celda.cell_type != "code":
            continue
        texto = []
        for s in celda.outputs:
            if s.output_type == "stream":
                texto.append(s.text)
            elif s.output_type == "display_data" and "image/svg+xml" in s.data:
                carpeta_graficas.mkdir(parents=True, exist_ok=True)
                destino = carpeta_graficas / f"{celda.metadata['etiqueta']}.svg"
                destino.write_text(_svg_para_diapositiva(s.data["image/svg+xml"]), encoding="utf-8")
                graficas.append(destino)
            elif s.output_type in ("execute_result", "display_data"):
                texto.append(s.data.get("text/plain", "") + "\n")
            elif s.output_type == "error":
                raise SystemExit(f"La celda [{celda.metadata['etiqueta']}] falló: {s.ename}: {s.evalue}")
        salidas[celda.metadata["etiqueta"]] = "".join(texto).rstrip("\n")
    import pandas
    salidas.pop("_preludio", None)
    salidas["_entorno"] = f"Python {sys.version.split()[0]} · pandas {pandas.__version__}"
    destino = AQUI / f"salidas_sesion{numero}.json"
    destino.write_text(json.dumps(salidas, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for clave, texto in salidas.items():
        print(f"── [{clave}]\n{texto}\n")
    print("Salidas:", destino.relative_to(RAIZ))
    for g in graficas:
        print("Gráfica:", g.relative_to(RAIZ))


def _svg_para_diapositiva(svg):
    """SVG de matplotlib → SVG para incrustar: sin cabecera XML ni fecha, en Roboto."""
    svg = re.sub(r"^.*?(<svg)", r"\1", svg, flags=re.S)
    svg = re.sub(r"\s*<metadata>.*?</metadata>", "", svg, flags=re.S)
    # que llene su columna: sin ancho ni alto fijos, solo con viewBox
    svg = re.sub(r'<svg([^>]*?) width="[^"]*" height="[^"]*"', r'<svg\1 width="100%"', svg, count=1)
    svg = re.sub(r"font-family: [^;\"]*", "font-family: Roboto, 'Helvetica Neue', Arial, sans-serif", svg)
    return svg.strip() + "\n"


if __name__ == "__main__":
    accion, numero = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
    {"genera": genera, "ejecuta": ejecuta}[accion](numero)
