"""Portada del curso: fuente/index.html → Htmls/index.html.

    python precalculo/portada.py

Marcadores:
    {{LOGO}}      logo institucional como data URI (fuente/comun/logo-ucompensar.png)
    {{COLAB:N}}   enlace que abre en Colab el notebook de la sesión N publicado en GitHub
Si queda un marcador sin resolver, se detiene con error.
"""

import base64
import html
import re
from pathlib import Path

from notebook import SESIONES

RAIZ = Path(__file__).resolve().parent.parent
REPO = "JotaMao1985/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp"
PAGINAS = "https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/"


def enlace_colab(numero):
    return f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{SESIONES[numero]}"


def main():
    logo = base64.b64encode((RAIZ / "fuente/comun/logo-ucompensar.png").read_bytes()).decode()
    texto = (RAIZ / "fuente/index.html").read_text(encoding="utf-8")
    texto = texto.replace("{{LOGO}}", f"data:image/png;base64,{logo}")
    texto = re.sub(r"\{\{COLAB:(\d+)\}\}", lambda m: html.escape(enlace_colab(int(m.group(1)))), texto)
    restos = re.findall(r"\{\{[^}]*\}\}", texto)
    if restos:
        raise SystemExit(f"Marcadores sin resolver en la portada: {restos}")
    destino = RAIZ / "Htmls/index.html"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    print("Portada:", destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
