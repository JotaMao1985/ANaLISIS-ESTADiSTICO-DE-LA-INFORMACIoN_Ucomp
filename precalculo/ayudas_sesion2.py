"""Sesión 2: estilo de las gráficas del curso y verificadores de la práctica.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py. Cada
verificador recibe lo que el estudiante calculó, dice qué está bien y, en lo demás, da una
pista sin la respuesta. Nunca se cae: un «...» sin reemplazar o un tipo inesperado se avisa.
"""


def _estilo_graficas():
    """Colores del curso y letras que se leen en Colab y proyectadas."""
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "axes.prop_cycle": mpl.cycler(color=["#8A2E9E", "#F46201", "#566B7F"]),
        "figure.figsize": (6.4, 3.6),
        "figure.constrained_layout.use": True,
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#94A3B8",
        "axes.labelcolor": "#334155",
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "text.color": "#1E293B",
    })


_estilo_graficas()


def _mostrar(tabla):
    try:
        from IPython.display import display
        display(tabla)
    except ImportError:
        print(tabla.to_string())


def _serie(x):
    """La serie que entregó el estudiante, o None si no es una."""
    import pandas as pd

    if isinstance(x, pd.DataFrame) and x.shape[1] == 1:
        x = x.iloc[:, 0]
    if not isinstance(x, pd.Series):
        return None
    if isinstance(x.index, pd.MultiIndex) and x.index.nlevels == 1:  # pedidos[["col"]].value_counts()
        x = x.set_axis(x.index.get_level_values(0))
    return x


def _numerica(serie):
    import pandas as pd

    return pd.api.types.is_numeric_dtype(serie) and not pd.api.types.is_bool_dtype(serie)


def _valores(serie, indice):
    """Los valores de la serie en el orden de `indice` (claves comparadas como texto)."""
    texto = lambda c: str(c).removesuffix(".0")
    por_clave = {texto(k): v for k, v in serie.items()}
    try:
        return [float(por_clave[texto(k)]) for k in indice]
    except (KeyError, TypeError, ValueError):
        return None


def _cerca(a, b, tolerancia):
    return a is not None and len(a) == len(b) and all(abs(x - y) <= tolerancia for x, y in zip(a, b))


def revisar_nominal(conteo=..., porcentaje=...):
    """Ejercicio 1: frecuencia absoluta y relativa (en %) de medio_pago."""
    import pandas as pd

    original = pd.read_csv("datos/pedidos.csv")
    esperado = original["medio_pago"].value_counts()
    n = len(original)
    absolutas = [float(v) for v in esperado]
    relativas = [100 * v / n for v in absolutas]
    bien = 0

    c = _serie(conteo)
    if conteo is Ellipsis:
        print("·  conteo: todavía tiene ...")
    elif c is None:
        print("✗  conteo: tiene que ser una serie de pandas, como la que devuelve value_counts()")
    elif len(c) == n:
        print("✗  conteo: esa es la columna entera, un valor por pedido: falta contarla")
    elif _valores(c, esperado.index) is None or len(c) != len(esperado):
        print("✗  conteo: sus categorías no son las de medio_pago: ¿contaste la columna correcta?")
    elif not _numerica(c):
        print("✗  conteo: sus valores son texto; déjalos como números (sin astype(str))")
    elif _cerca(_valores(c, esperado.index), absolutas, 0):
        print("✓  conteo")
        bien += 1
    elif abs(c.sum() - 1) < 1e-6 or abs(c.sum() - 100) < 0.5:
        print("✗  conteo: eso ya es una frecuencia relativa; la absoluta cuenta pedidos")
    else:
        print("✗  conteo: los números no cuadran: ¿contaste todos los pedidos?")

    p = _serie(porcentaje)
    vp = None if p is None else _valores(p, esperado.index)
    if porcentaje is Ellipsis:
        print("·  porcentaje: todavía tiene ...")
    elif p is None:
        print("✗  porcentaje: tiene que ser una serie de pandas, como la que devuelve value_counts()")
    elif len(p) == n:
        print("✗  porcentaje: esa es la columna entera, un valor por pedido: falta contarla")
    elif vp is None or len(p) != len(esperado):
        print("✗  porcentaje: sus categorías no son las de medio_pago")
    elif not _numerica(p):
        print("✗  porcentaje: sus valores son texto; déjalos como números (sin astype(str) ni « %»)")
    elif _cerca(vp, relativas, 0.051):
        print("✓  porcentaje")
        bien += 1
    elif _cerca(vp, [r / 100 for r in relativas], 0.00051):
        print("✗  porcentaje: está como proporción (suma 1); el ejercicio la pide en %")
    elif _cerca(vp, absolutas, 0):
        print("✗  porcentaje: eso es la frecuencia absoluta; ¿qué hace normalize=True?")
    elif _cerca(vp, [a * 100 for a in absolutas], 0):
        print("✗  porcentaje: multiplicaste por 100 los conteos; antes hay que dividir entre el total")
    elif _cerca(vp, relativas, 0.51):
        print("✗  porcentaje: casi: perdiste precisión al redondear; deja al menos un decimal en el %")
    else:
        print("✗  porcentaje: no cuadra: ¿sobre qué total dividiste?")

    if bien == 2:
        tabla = pd.DataFrame({"pedidos": [int(v) for v in absolutas], "%": vp},
                             index=esperado.index)
        _mostrar(tabla.round({"%": 1}))
        print("✓  Tabla lista. ¿Cuál es la moda?")


def revisar_acumulada(conteo=..., acumulado=...):
    """Ejercicio 2: frecuencias del estrato en su orden, con el % acumulado."""
    import pandas as pd

    original = pd.read_csv("datos/pedidos.csv")
    orden = [1, 2, 3, 4, 5, 6]
    absolutas = [float((original["estrato"] == e).sum()) for e in orden]
    n = len(original)
    acumuladas = [100 * sum(absolutas[: i + 1]) / n for i in range(6)]
    bien = 0

    c = _serie(conteo)
    if conteo is Ellipsis:
        print("·  conteo: todavía tiene ...")
    elif c is None:
        print("✗  conteo: tiene que ser una serie de pandas, como la que devuelve value_counts()")
    elif len(c) == n:
        print("✗  conteo: esa es la columna entera, un valor por pedido: falta contarla")
    elif _valores(c, orden) is None or len(c) != 6:
        print("✗  conteo: sus categorías no son los estratos 1 a 6: ¿contaste la columna correcta?")
    elif not _numerica(c):
        print("✗  conteo: sus valores son texto; déjalos como números (sin astype(str))")
    elif not _cerca(_valores(c, orden), absolutas, 0):
        print("✗  conteo: los números no cuadran; la frecuencia absoluta cuenta pedidos")
    elif [str(k).removesuffix(".0") for k in c.index] != [str(e) for e in orden]:
        if list(c) == sorted(c, reverse=True):
            print("✗  conteo: los valores están bien, pero van por tamaño: una ordinal va en su "
                  "orden (1 a 6)")
        else:
            print("✗  conteo: los valores están bien, pero no van del 1 al 6. Si recargaste "
                  "pedidos, vuelve a ejecutar [cargar]: ahí estrato queda como categoría ordenada")
    else:
        print("✓  conteo, en su orden")
        bien += 1

    a = _serie(acumulado)
    valores = None
    if a is not None and _numerica(a):
        valores = [float(v) for v in a]
    if acumulado is Ellipsis:
        print("·  acumulado: todavía tiene ...")
    elif a is None:
        print("✗  acumulado: tiene que ser una serie de pandas (la que devuelve cumsum())")
    elif not _numerica(a):
        print("✗  acumulado: sus valores son texto; déjalos como números (sin astype(str) ni « %»)")
    elif len(a) != 6:
        print("✗  acumulado: debe tener un valor por estrato, seis en total")
    elif _cerca(valores, acumuladas, 0.151):
        print("✓  acumulado")
        bien += 1
    elif _cerca(valores, [x / 100 for x in acumuladas], 0.0016):
        print("✗  acumulado: está como proporción (termina en 1); el ejercicio lo pide en %")
    elif abs(valores[-1] - n) < 0.5:
        print("✗  acumulado: acumulaste pedidos; el ejercicio pide el % acumulado")
    elif valores[-1] > 0 and _cerca([100 * v / valores[-1] for v in valores], acumuladas, 0.151):
        print("✗  acumulado: los pasos cuadran, pero no termina en 100 %: ¿sobre qué total "
              "dividiste? (si usaste n, revisa cuánto vale)")
    elif _cerca(valores, acumuladas, 0.6):
        print("✗  acumulado: casi: perdiste precisión al redondear; redondea solo al final")
    elif abs(valores[-1] - 100) < 0.2:
        print("✗  acumulado: termina en 100, pero los pasos no cuadran: ¿acumulaste en el "
              "orden del estrato?")
    else:
        print("✗  acumulado: el último valor tiene que ser 100 %: acumula los %, no otra cosa")

    if bien == 2:
        tabla = pd.DataFrame({"pedidos": [int(v) for v in absolutas], "% acumulado": valores},
                             index=pd.Index(orden, name="estrato"))
        _mostrar(tabla.round({"% acumulado": 1}))
        print("✓  Tabla lista. Responde abajo: ¿qué % de los pedidos va a direcciones de estrato 3 "
              "o menos?")


def revisar_intervalos(cortes=...):
    """Ejercicio 3: intervalos de 2 km, cerrados a la izquierda, que cubran todos los pedidos."""
    import math
    import pandas as pd

    if cortes is Ellipsis:
        print("·  cortes: todavía tiene ...")
        return
    try:
        cortes = [float(x) for x in cortes]
    except (TypeError, ValueError):
        print("✗  cortes: escribe una lista de números, como [0, 2, 4] o list(range(0, 10, 2))")
        return
    if len(cortes) < 2:
        print("✗  cortes: hacen falta al menos dos cortes: el inicio y el fin de cada intervalo")
        return
    if any(math.isnan(x) for x in cortes):
        print("✗  cortes: hay un valor que no es un número (nan)")
        return
    if any(math.isinf(x) for x in cortes):
        print("✗  cortes: una clase abierta (inf) sirve cuando la cola no tiene techo; aquí todos los "
              "intervalos miden 2 km: ¿cuál es la distancia máxima?")
        return
    distancia = pd.read_csv("datos/pedidos.csv")["distancia_km"]
    if any(b <= a for a, b in zip(cortes, cortes[1:])):
        print("✗  cortes: tienen que ir de menor a mayor")
        return
    if cortes[0] != 0:
        print("✗  cortes: el primer intervalo empieza en 0 km")
        return
    if any(abs((b - a) - 2) > 1e-9 for a, b in zip(cortes, cortes[1:])):
        print("✗  cortes: cada intervalo mide 2 km: de 2 en 2")
        return
    fuera = int((distancia >= cortes[-1]).sum())
    if fuera:
        print(f"✗  cortes: se quedan por fuera {fuera} pedidos. Con intervalos [a, b), el último "
              "no incluye su borde derecho: ¿cuál es la distancia máxima?")
        return
    clases = pd.cut(distancia, bins=cortes, right=False)
    tabla = clases.value_counts(sort=False).to_frame("pedidos")
    tabla["%"] = (tabla["pedidos"] / len(distancia) * 100).round(1)
    vacias = int((tabla["pedidos"] == 0).sum())
    _mostrar(tabla)
    print(f"✓  Los {len(distancia):,} pedidos caben en {len(tabla)} intervalos de 2 km".replace(",", " "))
    if vacias:
        sobran = "Sobra 1 intervalo vacío" if vacias == 1 else f"Sobran {vacias} intervalos vacíos"
        print(f"·  {sobran} al final: puedes terminar antes")


def revisar_cruzada(mezcla=...):
    """Ejercicio 4: qué se pide en cada franja: franja × categoría, en % por fila."""
    import pandas as pd

    if mezcla is Ellipsis:
        print("·  mezcla: todavía tiene ...")
        return
    if not isinstance(mezcla, pd.DataFrame):
        print("✗  mezcla: tiene que ser una tabla (DataFrame), como la que devuelve pd.crosstab")
        return
    original = pd.read_csv("datos/pedidos.csv")
    cuenta = pd.crosstab(original["franja"], original["categoria"])
    texto = lambda x: {str(v) for v in x}
    if texto(mezcla.index) == texto(cuenta.columns) and texto(mezcla.columns) == texto(cuenta.index):
        print("✗  mezcla: las franjas deben ir en las filas y las categorías en las columnas: "
              "intercambia los dos primeros argumentos")
        return
    if (texto(mezcla.index) != texto(cuenta.index) or texto(mezcla.columns) != texto(cuenta.columns)
            or mezcla.index.duplicated().any() or mezcla.columns.duplicated().any()):
        print("✗  mezcla: las filas tienen que ser las franjas y las columnas, las categorías "
              "(sin totales)")
        return
    tuya = mezcla.copy()
    tuya.index, tuya.columns = tuya.index.astype(str), tuya.columns.astype(str)
    try:
        tuya = tuya.loc[cuenta.index, cuenta.columns].astype(float)
    except (TypeError, ValueError):
        print("✗  mezcla: tiene texto; deja los números (sin astype(str) ni « %»)")
        return
    por_fila = cuenta.div(cuenta.sum(axis=1), axis=0)
    por_columna = cuenta / cuenta.sum()
    del_total = cuenta / cuenta.to_numpy().sum()
    igual = lambda x, y, tol: bool(((x - y).abs() <= tol).all().all())
    if igual(tuya, por_fila, 0.0006) or igual(tuya / 100, por_fila, 0.0006):  # en proporción o en %
        orden = ["Mañana", "Almuerzo", "Tarde", "Noche"]
        _mostrar((por_fila.loc[orden] * 100).round(1))
        print("✓  Cada fila suma 100 %: es la mezcla de categorías de cada franja")
    elif igual(tuya, por_columna, 0.006) or igual(tuya / 100, por_columna, 0.006):
        print("✗  mezcla: cada columna suma 100 %. La pregunta es por la mezcla de cada franja: "
              "¿qué tiene que sumar 100 %?")
    elif igual(tuya, del_total, 0.006) or igual(tuya / 100, del_total, 0.006):
        print("✗  mezcla: toda la tabla suma 100 %. La pregunta es por la mezcla de cada franja: "
              "¿qué tiene que sumar 100 %?")
    elif igual(tuya, cuenta, 0.5):
        print("✗  mezcla: son conteos; falta normalize")
    elif igual(tuya, por_fila, 0.006) or igual(tuya / 100, por_fila, 0.006):
        print("✗  mezcla: casi: perdiste precisión al redondear; deja al menos un decimal en el %")
    else:
        print("✗  mezcla: los valores no cuadran: revisa las columnas que cruzaste")
