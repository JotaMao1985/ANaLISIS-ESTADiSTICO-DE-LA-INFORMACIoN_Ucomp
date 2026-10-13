"""Ayudas comunes a todos los notebooks del curso (van en la celda oculta, tras genera_datos.py).

Las de cada sesión están en ayudas_sesionN.py.
"""


def _aviso_version():
    """Las diapositivas se ejecutaron con pandas 2.2; con pandas 3 algunas salidas cambian."""
    import pandas as pd

    if int(pd.__version__.split(".")[0]) >= 3:
        print(f"Aviso: este Colab trae pandas {pd.__version__} y las diapositivas usan pandas 2.2. "
              "Algunas salidas se verán un poco distintas (por ejemplo, el texto sale como str "
              "y no como object).")


_aviso_version()
