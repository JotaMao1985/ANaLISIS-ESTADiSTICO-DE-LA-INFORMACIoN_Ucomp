"""Sesión 3: estilo de las gráficas del curso y verificadores de la práctica.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py. Cada
verificador recibe lo que el estudiante calculó, dice qué está bien y, en lo demás, da una
pista sin la respuesta. Nunca se cae: un «...» sin reemplazar o un tipo inesperado se avisa.

Tolerancias: ±0,05 en minutos y kilómetros; la desviación se acepta con las dos fórmulas
(entre n − 1 o entre n) porque cada grupo pasa de 1000 pedidos.
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


def _original():
    """Los pedidos tal como salen del generador, o None (con aviso) si no están."""
    import pandas as pd

    try:
        return pd.read_csv("datos/pedidos.csv")
    except FileNotFoundError:
        print("✗  No encuentro datos/pedidos.csv: ejecuta primero la celda que crea los datos "
              "(Entorno de ejecución → Ejecutar anteriores)")
        return None


def _sobrantes(sobran, otros, nombres):
    """Avisa de argumentos de más o con otro nombre. True si hubo alguno."""
    if otros:
        print(f"✗  No conozco {', '.join(repr(k) for k in otros)}: usa estos nombres, en "
              f"minúsculas y sin tildes: {', '.join(n + '=' for n in nombres)}")
        return True
    if sobran:
        print(f"✗  Sobran valores: el verificador recibe solo {len(nombres)} "
              f"({', '.join(n + '=' for n in nombres)})")
        return True
    return False


_COLUMNAS = {"id_pedido", "fecha", "franja", "ciudad", "categoria", "n_productos", "valor_pedido",
             "medio_pago", "estrato", "suscriptor", "distancia_km", "lluvia", "temperatura_c",
             "tiempo_entrega_min", "calificacion"}


def _un_numero(x, n_columna=None):
    """(valor, None) si x es un número, o una serie o lista con un solo número; si no, (None, motivo)."""
    import math
    import numbers
    import numpy as np
    import pandas as pd

    if isinstance(x, pd.DataFrame):
        if x.size != 1:
            return None, f"es una tabla de {x.shape[0]} × {x.shape[1]}; hace falta un solo número"
        x = x.iloc[0, 0]
    if isinstance(x, (pd.Series, pd.Index, np.ndarray, list, tuple)):
        valores = list(np.ravel(np.asarray(x, dtype=object)))
        if n_columna is not None and len(valores) == n_columna:
            return None, "esa es la columna entera, un valor por pedido: falta resumirla"
        if len(valores) == 0:
            return None, "está vacío"
        if len(valores) > 1:
            if all(isinstance(v, float) and math.isnan(v) for v in valores):
                return None, ("salió nan: si restaste dos series, pandas las alinea por su índice "
                              "y lo que no coincide queda nan; calcula cada valor como un número")
            pista = ""
            if isinstance(x, pd.Series) and set(map(str, x.index)) & _COLUMNAS:
                pista = ": ¿elegiste la columna?"   # p. ej., pedidos.mean(numeric_only=True)
            elif isinstance(x, pd.Series) and {"count", "mean", "std"} <= set(map(str, x.index)):
                pista = ": describe() da varias medidas; quédate solo con la que se pide"
            return None, f"tiene {len(valores)} valores; hace falta uno solo{pista}"
        x = valores[0]   # mode() o quantile([0.25]) devuelven una serie de un solo valor
    if x is None:
        return None, "está vacío (None): ¿le asignaste el resultado de un print?"
    if x is pd.NA:
        return None, "salió <NA>: revisa el cálculo (¿la columna tiene datos?)"
    if callable(x):
        return None, "es una función, no su resultado: ¿faltaron los paréntesis del final, ()?"
    if isinstance(x, (bool, np.bool_)):
        return None, "es True o False; hace falta un número"
    if isinstance(x, str):
        return None, "es texto; escríbelo como número, sin comillas y con punto decimal"
    if not isinstance(x, (numbers.Real, np.number)) or isinstance(x, np.complexfloating):
        return None, f"no es un número real (es {type(x).__name__})"
    try:
        valor = float(x)
    except (TypeError, ValueError, OverflowError):
        return None, "no es un número real"
    if math.isnan(valor):
        return None, "salió nan: revisa el cálculo (¿la columna tiene datos?)"
    if math.isinf(valor):
        return None, "salió infinito: ¿dividiste entre cero?"
    return valor, None


def _serie(x):
    """La serie que entregó el estudiante, o None si no es una."""
    import pandas as pd

    if isinstance(x, pd.DataFrame) and x.shape[1] == 1:
        x = x.iloc[:, 0]
    if not isinstance(x, pd.Series):
        return None
    if isinstance(x.index, pd.MultiIndex) and x.index.nlevels == 1:  # pedidos[["col"]].groupby…
        x = x.set_axis(x.index.get_level_values(0))
    return x


def _cerca(a, b, tolerancia):
    return a is not None and abs(a - b) <= tolerancia


def revisar_centro(media=..., mediana=..., moda=..., *sobran, **otros):
    """Ejercicio 1: media, mediana y moda de n_productos."""
    import pandas as pd

    if _sobrantes(sobran, otros, ["media", "mediana", "moda"]):
        return
    original = _original()
    if original is None:
        return
    columna = original["n_productos"]
    n = len(columna)
    verdad = {"media": columna.mean(), "mediana": columna.median(), "moda": columna.mode()[0]}
    veces_moda = int((columna == verdad["moda"]).sum())
    # medias y medianas de las otras columnas numéricas: para detectar la columna equivocada
    otras = original.select_dtypes("number").drop(columns="n_productos")
    de_otras = list(otras.mean()) + list(otras.median())
    bien = 0

    for nombre, x in [("media", media), ("mediana", mediana), ("moda", moda)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        v, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        if nombre == "media":
            if _cerca(v, verdad["media"], 0.0051):
                print("✓  media")
                bien += 1
            elif _cerca(v, verdad["media"], 0.051):
                print("✗  media: casi: perdiste precisión al redondear; deja al menos dos decimales")
            elif _cerca(v, verdad["mediana"], 1e-9) or _cerca(v, verdad["moda"], 1e-9):
                print("✗  media: ese es el valor del medio o el más frecuente, o la media sin sus "
                      "decimales (¿usaste int()?); la media suma todos los valores, divide entre "
                      "cuántos son y conserva los decimales")
            elif v != round(v) and any(_cerca(v, o, 1e-6) for o in de_otras):
                print("✗  media: ese valor es de otra columna: ¿elegiste n_productos?")
            else:
                print("✗  media: no cuadra: ¿la calculaste sobre n_productos, con todos los pedidos?")
        elif nombre == "mediana":
            if _cerca(v, verdad["mediana"], 1e-9):
                print("✓  mediana")
                bien += 1
            elif v != round(v) and _cerca(v, verdad["media"], 0.051):
                print("✗  mediana: eso parece la media; la mediana es el valor del medio de los "
                      "datos ordenados")
            elif v != round(v) and any(_cerca(v, o, 1e-6) for o in de_otras):
                print("✗  mediana: ese valor es de otra columna: ¿elegiste n_productos?")
            else:
                print("✗  mediana: no cuadra: es el valor que deja la mitad de los pedidos a cada lado")
        else:
            if _cerca(v, verdad["moda"], 1e-9):
                print("✓  moda")
                bien += 1
            elif _cerca(v, veces_moda, 1e-9):
                print("✗  moda: ese número dice cuántas veces aparece el valor más frecuente; la "
                      "moda es el valor, no su frecuencia")
            elif v != round(v) and _cerca(v, verdad["media"], 0.051):
                print("✗  moda: eso parece la media; la moda es el valor que más se repite")
            else:
                print("✗  moda: no cuadra: es el valor de n_productos que más se repite")

    if bien == 3:
        tabla = pd.DataFrame({"n_productos": [verdad["media"], verdad["mediana"], verdad["moda"]]},
                             index=["media", "mediana", "moda"])
        _mostrar(tabla.round(2))
        print("✓  Las tres cuadran. Responde abajo: ¿cuál representa mejor al pedido típico?")


def revisar_medianas(estrato=..., calificacion=..., *sobran, **otros):
    """Ejercicio 2: mediana del estrato y de la calificación (pedidos calificados), leídas en la
    acumulada."""
    import pandas as pd

    if _sobrantes(sobran, otros, ["estrato", "calificacion"]):
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    resultado = {}
    bien = 0

    for nombre, x, columna, categorias in [
        ("estrato", estrato, "estrato", [1, 2, 3, 4, 5, 6]),
        ("calificacion", calificacion, "calificacion", [1, 2, 3, 4, 5]),
    ]:
        datos = original[columna].dropna()
        acumulada = datos.value_counts(normalize=True).reindex(categorias, fill_value=0).cumsum()
        verdad = int((acumulada >= 0.5).idxmax())
        resultado[nombre] = (verdad, acumulada)
        # lecturas de dos errores típicos: acumular en orden de frecuencia (value_counts sin
        # sort=False) y, en la calificación, sumar al total los pedidos sin calificar
        por_frecuencia = int((datos.value_counts(normalize=True).cumsum() >= 0.5).idxmax())
        sobre_todos = int((original[columna].value_counts(normalize=True, dropna=False)
                           .reindex(categorias, fill_value=0).cumsum() >= 0.5).idxmax())
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        if isinstance(x, (pd.Series, pd.DataFrame)) and len(x) == len(categorias):
            print(f"✗  {nombre}: esa es la tabla completa, un valor por categoría; escribe solo la "
                  "categoría en la que el % acumulado llega al 50 %")
            continue
        v, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        if _cerca(v, verdad, 1e-9):
            print(f"✓  {nombre}")
            bien += 1
        elif _cerca(v, datos.mean(), 0.051):
            print(f"✗  {nombre}: eso es la media de los números; en una ordinal no sabemos si las "
                  "categorías están a la misma distancia: usa la acumulada")
        elif v not in categorias:
            print(f"✗  {nombre}: la mediana de una ordinal es una de sus categorías "
                  f"({categorias[0]} a {categorias[-1]})")
        elif nombre == "calificacion" and v == sobre_todos and v == por_frecuencia:
            print("✗  calificacion: revisa dos cosas: que la acumulada vaya en el orden de las "
                  "categorías, de 1 a 5 (value_counts las ordena por frecuencia si no le dices "
                  "sort=False), y que el total sean los pedidos calificados: los que no tienen "
                  "calificación no cuentan")
        elif nombre == "calificacion" and v == sobre_todos:
            print("✗  calificacion: ¿sobre qué total calculaste la acumulada? La mediana es la de "
                  "los pedidos calificados: los que no tienen calificación no cuentan")
        else:
            orden = (" (con las categorías en su orden, de la menor a la mayor: value_counts las "
                     "ordena por frecuencia si no le dices sort=False)" if v == por_frecuencia else "")
            if acumulada[int(v)] < 0.5:
                print(f"✗  {nombre}: en esa categoría el % acumulado todavía no llega al 50 %{orden}")
            else:
                print(f"✗  {nombre}: en esa categoría la acumulada ya pasó del 50 %, pero no es la "
                      f"primera que llega: mira las anteriores{orden}")

    if bien == 2:
        filas = {}
        for nombre, (verdad, acumulada) in resultado.items():
            posicion = acumulada.index.get_loc(verdad)
            anterior = acumulada.iloc[posicion - 1] if posicion > 0 else 0.0
            filas[nombre] = {"mediana": verdad,
                             "% acumulado en la anterior": anterior * 100,
                             "% acumulado en la mediana": acumulada[verdad] * 100}
        _mostrar(pd.DataFrame(filas).T.round(1).astype({"mediana": int}))
        if all(original[c].dropna().mode()[0] == v for c, (v, _) in resultado.items()):
            print("·  Aquí la mediana coincide con la moda; la mediana sale de la acumulada (la "
                  "primera categoría que llega al 50 %), no de la barra más alta")
        print("✓  Las dos cuadran. Responde abajo: ¿por qué no resumirlas con la media?")


def revisar_por_ciudad(media=..., desviacion=..., ric=..., *sobran, **otros):
    """Ejercicio 3: media, desviación estándar y RIC del tiempo de entrega, por ciudad."""
    import math
    import numbers
    import numpy as np
    import pandas as pd

    if _sobrantes(sobran, otros, ["media", "desviacion", "ric"]):
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    grupos = original.groupby("ciudad")["tiempo_entrega_min"]
    ciudades = list(grupos.size().index)
    q1, q3 = grupos.quantile(0.25), grupos.quantile(0.75)
    candidatos = {
        "media": grupos.mean(), "mediana": grupos.median(),
        "desviacion": grupos.std(), "desviacion0": grupos.std(ddof=0),
        "varianza": grupos.var(), "varianza0": grupos.var(ddof=0),
        "ric": q3 - q1, "ric_negativo": q1 - q3, "q1": q1, "q3": q3,
        "rango": grupos.max() - grupos.min(),
        "media_total": pd.Series(original["tiempo_entrega_min"].mean(), index=ciudades),
    }
    pocos = int(grupos.size().min())

    def igual(valores, clave, tolerancia=0.051):
        return bool((valores - candidatos[clave]).abs().max() <= tolerancia)

    def leer(nombre, x):
        """Los valores por ciudad, en el orden de `ciudades`, o None (con aviso)."""
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            return None
        if isinstance(x, pd.DataFrame) and "ciudad" in x.columns:
            print(f"✗  {nombre}: la ciudad quedó como columna (¿usaste reset_index?); déjala en "
                  "el índice, como sale de groupby")
            return None
        if isinstance(x, pd.DataFrame) and x.shape[1] > 1:
            columnas = set(map(str, x.columns))
            if columnas & _COLUMNAS:
                print(f"✗  {nombre}: es una tabla con {x.shape[1]} columnas; hace falta una serie con "
                      "un valor por ciudad: ¿elegiste la columna tiempo_entrega_min antes de calcular?")
            elif columnas & set(ciudades):
                print(f"✗  {nombre}: las ciudades quedaron como columnas; déjalas en el índice, como "
                      "sale de groupby")
            else:
                print(f"✗  {nombre}: es una tabla con {x.shape[1]} columnas, una por medida; hace "
                      "falta una serie: quédate solo con la columna de la medida que se pide")
            return None
        s = _serie(x)
        if s is None:
            if isinstance(x, (numbers.Real, np.number)) and not isinstance(x, bool):
                print(f"✗  {nombre}: es un solo número; hace falta un valor por ciudad: agrupa "
                      "por ciudad, como en la celda [dos_ciudades]")
            elif isinstance(x, (list, tuple, np.ndarray)):
                print(f"✗  {nombre}: es una lista sin los nombres de las ciudades; deja el "
                      "resultado de groupby, que trae la ciudad en el índice")
            elif isinstance(x, str):
                print(f"✗  {nombre}: es texto; hace falta una serie de pandas con un valor por ciudad")
            elif x is None:
                print(f"✗  {nombre}: está vacío (None): ¿le asignaste el resultado de un print?")
            elif callable(x):
                print(f"✗  {nombre}: es una función, no su resultado: ¿faltaron los paréntesis "
                      "del final, ()?")
            elif type(x).__name__.endswith("GroupBy"):
                print(f"✗  {nombre}: es el agrupamiento, todavía sin la medida: falta calcularla "
                      "en cada grupo")
            else:
                print(f"✗  {nombre}: tiene que ser una serie de pandas con un valor por ciudad "
                      f"(es {type(x).__name__})")
            return None
        if len(s) == n:
            print(f"✗  {nombre}: esa es la columna entera, un valor por pedido: falta agruparla "
                  "por ciudad y resumirla")
            return None
        if isinstance(s.index, pd.MultiIndex) and s.index.nlevels > 1:
            ultimo = s.index.get_level_values(-1)
            if pd.api.types.is_float_dtype(ultimo) and bool(((ultimo >= 0) & (ultimo <= 1)).all()):
                print(f"✗  {nombre}: su índice tiene {s.index.nlevels} niveles: con una lista entre "
                      "corchetes, como quantile([0.25]), pandas añade un nivel; usa quantile(0.25)")
            else:
                print(f"✗  {nombre}: su índice tiene {s.index.nlevels} niveles: ¿agrupaste por más "
                      "de una columna? Agrupa solo por ciudad")
            return None
        claves = [str(k) for k in s.index]
        if sorted(claves) != sorted(ciudades) or len(set(claves)) != len(claves):
            if isinstance(s.index, pd.RangeIndex):
                print(f"✗  {nombre}: sus filas van numeradas, sin el nombre de la ciudad; deja el "
                      "resultado de groupby, que trae la ciudad en el índice")
            elif set(claves) < set(ciudades):
                faltan = ", ".join(c for c in ciudades if c not in claves)
                print(f"✗  {nombre}: le faltan ciudades ({faltan}): ¿partiste de dos, la tabla de "
                      "la celda [dos_ciudades]? Agrupa pedidos, con todas las ciudades")
            else:
                print(f"✗  {nombre}: sus filas tienen que ser las cinco ciudades: ¿agrupaste por "
                      "ciudad?")
            return None
        if pd.api.types.is_bool_dtype(s):
            print(f"✗  {nombre}: sus valores son True o False; hace falta un número por ciudad")
            return None
        if s.dtype == object and all(isinstance(v, numbers.Real) and not isinstance(v, bool)
                                     for v in s):
            s = s.astype(float)   # números guardados como object
        if (not pd.api.types.is_numeric_dtype(s)) or pd.api.types.is_complex_dtype(s):
            print(f"✗  {nombre}: sus valores son texto; déjalos como números (sin astype(str))")
            return None
        valores = pd.Series(s.to_numpy(dtype=float), index=claves).reindex(ciudades)
        if valores.isna().any():
            print(f"✗  {nombre}: tiene valores nan: si restaste dos series, revisa que las dos "
                  "tengan las mismas ciudades en el índice")
            return None
        return valores

    bien = 0
    valores = leer("media", media)
    if valores is not None:
        if igual(valores, "media"):
            print("✓  media")
            bien += 1
        elif igual(valores, "mediana"):
            print("✗  media: esas son las medianas; la media suma y divide")
        elif igual(valores, "media_total"):
            print("✗  media: es la misma media para todas las ciudades: falta agrupar")
        elif igual(valores, "media", 0.51):
            print("✗  media: casi: perdiste precisión al redondear; deja al menos dos decimales")
        elif bool((valores == valores.round()).all()) and igual(valores, "media", 1.0):
            print("✗  media: le quitaste los decimales (¿astype(int)?); deja al menos dos decimales")
        else:
            print("✗  media: no cuadra: ¿la calculaste sobre tiempo_entrega_min?")

    valores = leer("desviacion", desviacion)
    if valores is not None:
        if igual(valores, "desviacion") or (pocos > 1000 and igual(valores, "desviacion0")):
            print("✓  desviacion")
            bien += 1
        elif (bool(((valores / candidatos["varianza"] - 1).abs() <= 0.01).all())
              or bool(((valores / candidatos["varianza0"] - 1).abs() <= 0.01).all())):
            print("✗  desviacion: eso es la varianza, en minutos al cuadrado; la desviación "
                  "vuelve a minutos")
        elif igual(valores, "ric"):
            print("✗  desviacion: eso parece el RIC; la desviación mide la distancia a la media")
        elif igual(valores, "rango"):
            print("✗  desviacion: eso es el rango (máximo menos mínimo)")
        elif igual(valores, "media"):
            print("✗  desviacion: esas son las medias")
        elif igual(valores, "desviacion", 0.51):
            print("✗  desviacion: casi: perdiste precisión al redondear; deja al menos dos decimales")
        else:
            print("✗  desviacion: no cuadra: revisa la columna y la función que usaste")

    valores = leer("ric", ric)
    if valores is not None:
        if igual(valores, "ric"):
            print("✓  ric")
            bien += 1
        elif igual(valores, "ric_negativo"):
            print("✗  ric: salió negativo: revisa el orden de la resta")
        elif igual(valores, "q3") or igual(valores, "q1"):
            print("✗  ric: eso es un cuartil; el RIC es la distancia entre dos cuartiles")
        elif igual(valores, "rango"):
            print("✗  ric: eso es el rango (máximo menos mínimo); el RIC usa los cuartiles")
        elif igual(valores, "mediana"):
            print("✗  ric: esas son las medianas")
        elif igual(valores, "desviacion") or igual(valores, "desviacion0"):
            print("✗  ric: esa es la desviación estándar")
        elif igual(valores, "ric", 0.51):
            print("✗  ric: casi: perdiste precisión al redondear; deja al menos dos decimales")
        else:
            print("✗  ric: no cuadra: ¿qué cuantiles restaste? (en quantile, 0.25 es el 25 %)")

    if bien == 3:
        tabla = pd.DataFrame({"media": candidatos["media"], "desviación": candidatos["desviacion"],
                              "RIC": candidatos["ric"]})
        _mostrar(tabla.round(1))
        print("✓  Las tres cuadran. Responde abajo: ¿en qué ciudad se puede prometer una ventana "
              "más estrecha?")


def revisar_cuartiles(*sueltos, q1=..., q3=..., ric=..., **otros):
    """Ejercicio 4: Q1, Q3 y RIC de distancia_km, recibidos por nombre."""
    import numpy as np
    import pandas as pd

    if sueltos:
        print("✗  Pasa los valores por nombre, como en la plantilla: "
              "revisar_cuartiles(q1=q1, q3=q3, ric=ric)")
        return
    if _sobrantes((), otros, ["q1", "q3", "ric"]):
        return
    original = _original()
    if original is None:
        return
    d = original["distancia_km"]
    n = len(d)
    verdad = {"q1": d.quantile(0.25), "q3": d.quantile(0.75)}
    verdad["ric"] = verdad["q3"] - verdad["q1"]
    otros_valores = {"mediana": d.median(), "media": d.mean(), "mínimo": d.min(),
                     "máximo": d.max(), "desviación": d.std()}
    # los mismos cálculos sobre otras columnas: la celda [cuartiles] usa tiempo_entrega_min
    otras = original.select_dtypes("number").drop(columns="distancia_km")
    de_otras = {"q1": list(otras.quantile(0.25)), "q3": list(otras.quantile(0.75)),
                "ric": list(otras.quantile(0.75) - otras.quantile(0.25))}
    tol = 0.051
    bien = 0

    for nombre, x in [("q1", q1), ("q3", q3), ("ric", ric)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        if nombre == "ric" and isinstance(x, np.generic) and x is q1:   # ric = q1
            print("✗  ric: es el mismo valor que pasaste en q1; el RIC es la distancia entre los "
                  "dos cuartiles")
            continue
        v, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        if _cerca(v, verdad[nombre], tol):
            print(f"✓  {nombre}")
            bien += 1
            continue
        if v != round(v) and any(_cerca(v, o, 1e-6) for o in de_otras[nombre]):
            print(f"✗  {nombre}: ese valor es de otra columna: ¿lo calculaste sobre distancia_km?")
            continue
        if nombre == "ric":
            if _cerca(v, -verdad["ric"], tol):
                print("✗  ric: salió negativo: revisa el orden de la resta")
            elif _cerca(v, otros_valores["máximo"] - otros_valores["mínimo"], tol):
                print("✗  ric: eso es el rango (máximo menos mínimo); el RIC usa los cuartiles")
            elif _cerca(v, otros_valores["desviación"], tol):
                print("✗  ric: esa es la desviación estándar")
            else:
                print("✗  ric: no cuadra: es la distancia entre el tercer y el primer cuartil")
            continue
        otro = "q3" if nombre == "q1" else "q1"
        if _cerca(v, verdad[otro], tol):
            print(f"✗  {nombre}: ese es el otro cuartil: ¿los intercambiaste?")
        elif any(_cerca(v, valor, tol) for clave, valor in otros_valores.items()):
            clave = next(c for c, valor in otros_valores.items() if _cerca(v, valor, tol))
            print(f"✗  {nombre}: eso es {'la' if clave in ('mediana', 'media', 'desviación') else 'el'} "
                  f"{clave}")
        else:
            parte = "25 %" if nombre == "q1" else "75 %"
            print(f"✗  {nombre}: no cuadra: es el valor que deja por debajo el {parte} de los pedidos")

    if bien == 3:
        tabla = pd.DataFrame({"km": [verdad["q1"], d.median(), verdad["q3"], verdad["ric"]]},
                             index=["Q1", "mediana", "Q3", "RIC"])
        _mostrar(tabla.round(2))
        print("✓  Los tres cuadran. Ahora dibuja el diagrama de caja (el verificador no lo revisa) "
              "y compáralo con estos cuartiles")
