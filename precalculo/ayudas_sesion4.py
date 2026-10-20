"""Sesión 4: estilo de las gráficas del curso y verificadores de la práctica.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py. Cada
verificador recibe lo que el estudiante calculó, dice qué está bien y, en lo demás, da una
pista sin la respuesta. Nunca se cae: un «...» sin reemplazar o un tipo inesperado se avisa.

Tolerancias: relativa en pesos (ejercicio 1), ±0,05 en minutos (las tablas redondeadas a un
decimal valen) y ±0,005 en kilómetros en el ejercicio 3, porque ahí la media cambia apenas
centésimas. El puntaje z se acepta con las dos fórmulas de la desviación (entre n − 1 o entre n):
con 12 000 pedidos, el conteo no cambia.
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


def _seguro(verificador):
    """Red de seguridad: si algo imprevisto falla al revisar, se avisa sin traceback."""
    import functools

    @functools.wraps(verificador)
    def envoltura(*args, **kwargs):
        try:
            return verificador(*args, **kwargs)
        except Exception as error:   # noqa: BLE001 — el estudiante nunca ve un traceback
            print(f"✗  No pude revisar lo que entregaste ({type(error).__name__}). Revisa que cada "
                  "valor sea el resultado de un cálculo de pandas y vuelve a ejecutar la celda")
    return envoltura


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
                pista = ": ¿elegiste la columna?"   # p. ej., pedidos.quantile(0.25, numeric_only=True)
            elif isinstance(x, pd.Series) and {"count", "mean", "std"} <= set(map(str, x.index)):
                pista = ": describe() da varias medidas; quédate solo con la que se pide"
            return None, f"tiene {len(valores)} valores; hace falta uno solo{pista}"
        x = valores[0]   # quantile([0.25]) devuelve una serie de un solo valor
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


def _cerca(a, b, tolerancia):
    return a is not None and abs(a - b) <= tolerancia


def _relativo(a, b, tolerancia):
    """¿a está a menos de `tolerancia` (relativa) de b? Para pesos."""
    return a is not None and abs(a - b) <= tolerancia * max(abs(b), 1.0)


def _vallas(x):
    """(valla inferior, valla superior, Q1, Q3) de 1,5 RIC."""
    a, b = x.quantile(0.25), x.quantile(0.75)
    return a - 1.5 * (b - a), b + 1.5 * (b - a), a, b


@_seguro
def revisar_atipicos(*sueltos, valla_inferior=..., valla_superior=..., n_ric=..., n_z=..., **otros):
    """Ejercicio 1: vallas de 1,5 RIC de valor_pedido, pedidos fuera y pedidos con |z| > 3."""
    import pandas as pd

    nombres = ["valla_inferior", "valla_superior", "n_ric", "n_z"]
    if sueltos:
        print("✗  Pasa los valores por nombre, como en la plantilla: revisar_atipicos("
              "valla_inferior=valla_inferior, valla_superior=valla_superior, n_ric=n_ric, n_z=n_z)")
        return
    if _sobrantes((), otros, nombres):
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    v = original["valor_pedido"]
    vi, vs, q1, q3 = _vallas(v)
    ric = q3 - q1
    fuera = int(((v < vi) | (v > vs)).sum())
    con_iguales = int(((v <= vi) | (v >= vs)).sum())
    solo_arriba = int((v > vs).sum())
    z1 = ((v - v.mean()) / v.std()).abs()
    z0 = ((v - v.mean()) / v.std(ddof=0)).abs()
    n_z_bien = {int((z1 > 3).sum()), int((z0 > 3).sum())}
    media, s = v.mean(), v.std()
    # z mal armado: dividido entre el RIC, o centrado con la mediana (en valor_pedido dan lo mismo)
    z_mal = {int((((v - media) / ric).abs() > 3).sum()), int((((v - v.median()) / s).abs() > 3).sum()),
             int((((v - v.median()) / ric).abs() > 3).sum())}
    # los pedidos que pueden confundirse con una valla: el mínimo, el máximo y el final de un bigote
    de_los_datos = (v.min(), v.max(), v[v >= vi].min(), v[v <= vs].max())
    # lo mismo con el tiempo de entrega: la columna de las celdas [vallas] y [puntaje_z]
    t = original["tiempo_entrega_min"]
    ti, ts, tq1, tq3 = _vallas(t)
    del_tiempo_vallas = [ti, ts, tq1, tq3, tq3 + 3 * (tq3 - tq1)]
    zt = ((t - t.mean()) / t.std()).abs()
    del_tiempo_conteos = {int(((t < ti) | (t > ts)).sum()), int((t > ts).sum()),
                          int((zt > 3).sum())}
    tol = 0.001   # relativa: en pesos

    bien = 0
    for nombre, x in [("valla_inferior", valla_inferior), ("valla_superior", valla_superior)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        val, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        verdad = vi if nombre == "valla_inferior" else vs
        otra = vs if nombre == "valla_inferior" else vi
        if _relativo(val, verdad, tol):
            print(f"✓  {nombre}")
            bien += 1
        elif any(_cerca(val, c, 0.051) for c in del_tiempo_vallas):
            print(f"✗  {nombre}: esa cifra es del tiempo de entrega: ¿copiaste la columna del "
                  "ejemplo? Aquí va valor_pedido")
        elif nombre == "valla_inferior" and val == 0:
            print("✗  valla_inferior: la valla puede ser negativa; el valor no. No la cambies "
                  "por cero: déjala como sale de la fórmula")
        elif nombre == "valla_inferior" and _relativo(val, -vi, tol):
            print("✗  valla_inferior: revisa el signo: la valla inferior se aleja de Q1 hacia abajo")
        elif _relativo(val, otra, tol):
            print(f"✗  {nombre}: esa es la otra valla: ¿las intercambiaste?")
        elif _relativo(val, q3 + 1.5 * q3 - q1, tol) or _relativo(val, q1 - 1.5 * q3 - q1, tol):
            print(f"✗  {nombre}: ¿faltan paréntesis? El 1,5 multiplica al RIC entero: 1.5 * (Q3 - Q1)")
        elif any(_cerca(val, c, 0.01) for c in (q1 - 1.5 * (tq3 - tq1), q3 + 1.5 * (tq3 - tq1))):
            print(f"✗  {nombre}: ¿recalculaste el RIC? Ese 1,5 RIC es el del tiempo de entrega")
        elif _relativo(val, q1, tol) or _relativo(val, q3, tol):
            print(f"✗  {nombre}: eso es un cuartil; la valla se aleja 1,5 RIC de la caja")
        elif _relativo(val, q3 + 3 * ric, tol) or _relativo(val, q1 - 3 * ric, tol):
            print(f"✗  {nombre}: esa es la valla de 3 RIC; aquí se pide la de 1,5 RIC")
        elif _relativo(val, media + 3 * s, tol) or _relativo(val, media - 3 * s, tol):
            print(f"✗  {nombre}: ese es el límite de |z| > 3; la valla usa los cuartiles y el RIC")
        elif any(_relativo(val, c, tol) for c in de_los_datos):
            print(f"✗  {nombre}: ese es un pedido de los datos (el mínimo, el máximo o el final de un "
                  "bigote); la valla se calcula con la fórmula y puede no ser ningún pedido")
        elif _relativo(val, verdad, 0.02):
            print(f"✗  {nombre}: casi: revisa los cuartiles (sin redondear) y el 1,5 RIC")
        else:
            print(f"✗  {nombre}: no cuadra: ¿usaste los cuartiles de valor_pedido y 1,5 veces su RIC?")

    for nombre, x in [("n_ric", n_ric), ("n_z", n_z)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        if (isinstance(x, (pd.Series, pd.DataFrame)) and 1 < len(x) < n
                and x.index.dtype.kind in "iu"):
            # valor[condicion] o pedidos[condicion]: los pedidos mismos (no decir cuántos son)
            print(f"✗  {nombre}: son los pedidos mismos, no cuántos son: cuéntalos con .sum() "
                  "sobre la condición (cada True cuenta 1) o con len()")
            continue
        val, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        if not float(val).is_integer():
            if 0 < val < 1:
                print(f"✗  {nombre}: eso parece una proporción; hace falta cuántos pedidos son: "
                      "con True y False, sum() cuenta los True")
            else:
                print(f"✗  {nombre}: un conteo es un número entero de pedidos")
            continue
        val = int(val)
        if nombre == "n_ric":
            if val == fuera:
                print("✓  n_ric")
                bien += 1
            elif val == con_iguales:
                print("✗  n_ric: ¿usaste ≥ o ≤? «Fuera» es estrictamente más allá de la valla: "
                      "< con la inferior y > con la superior")
            elif val == n - fuera or val == n - con_iguales:
                print("✗  n_ric: esos son los pedidos de dentro; se piden los de fuera")
            elif val in n_z_bien:
                print("✗  n_ric: ese conteo es el de |z| > 3; aquí van los que quedan fuera de las vallas")
            elif val in del_tiempo_conteos:
                print("✗  n_ric: ese conteo es del tiempo de entrega: ¿copiaste la columna del ejemplo?")
            elif val == 0:
                print("✗  n_ric: salió cero. Un pedido queda fuera si está por debajo de la inferior o "
                      "por encima de la superior: cuenta los dos lados y únelos con | («o»), no con & («y»)")
            elif val == n:
                print("✗  n_ric: son todos los pedidos: ¿comparaste valor_pedido con sus propias vallas?")
            else:
                print("✗  n_ric: no cuadra: cuenta los pedidos por debajo de la valla inferior o por "
                      "encima de la superior")
        else:
            if val in n_z_bien:
                print("✓  n_z")
                bien += 1
            elif val in (fuera, con_iguales):
                print("✗  n_z: ese conteo es el de las vallas; aquí van los de |z| > 3")
            elif val in del_tiempo_conteos:
                print("✗  n_z: ese conteo es del tiempo de entrega: ¿copiaste la columna del ejemplo?")
            elif val == 0:
                print("✗  n_z: salió cero: z se calcula con la media y la desviación de valor_pedido")
            elif val == n:
                print("✗  n_z: marca todos los pedidos: ¿faltan los paréntesis? z = (valor − media) / desviación")
            elif val in {n - k for k in n_z_bien}:
                print("✗  n_z: esos son los de dentro (|z| ≤ 3); se piden los de |z| > 3")
            elif val in z_mal:
                print("✗  n_z: z se centra con la media y se divide entre la desviación estándar, "
                      "std(): ¿usaste el RIC o la mediana?")
            elif val > max(n_z_bien):
                print("✗  n_z: marca de más: revisa el límite (3), el centro (la media) y el divisor "
                      "(la desviación, std())")
            else:
                print("✗  n_z: no cuadra: z = (valor − media) / desviación, y se cuentan los de |z| > 3")

    if bien == 4:
        tabla = pd.DataFrame({"valor_pedido": [vi, vs, fuera, (v < vi).sum(), (v > vs).sum(),
                                               max(n_z_bien)]},
                             index=["valla inferior (pesos)", "valla superior (pesos)",
                                    "fuera de las vallas", "· por debajo de la inferior",
                                    "· por encima de la superior", "con |z| > 3"])
        _mostrar(tabla.round(0).astype(int))
        print("✓  Los cuatro cuadran. Responde abajo: ¿por qué z marca menos pedidos que las vallas?")


def _texto(etiquetas):
    """Etiquetas comparadas como texto (las categóricas y los números también)."""
    return [str(e) for e in etiquetas]


@_seguro
def revisar_dinamica(tabla=..., *sobran, **otros):
    """Ejercicio 2: tabla dinámica de la mediana del tiempo por ciudad (filas) y franja (columnas).

    Acepta la tabla transpuesta, márgenes «All» o «Total», etiquetas categóricas (se comparan como
    texto), una serie con dos niveles (con la pista de unstack) y valores redondeados a un decimal.
    """
    import numbers
    import numpy as np
    import pandas as pd

    if _sobrantes(sobran, otros, ["tabla"]):
        return
    if tabla is Ellipsis:
        print("·  tabla: todavía tiene ...")
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    franjas = ["Mañana", "Almuerzo", "Tarde", "Noche"]
    original["franja"] = pd.Categorical(original["franja"], categories=franjas, ordered=True)
    ciudades = sorted(original["ciudad"].unique())
    grupos = original.groupby(["ciudad", "franja"], observed=True)["tiempo_entrega_min"]

    def como_tabla(serie):
        return serie.unstack().reindex(index=ciudades, columns=franjas)

    verdad = como_tabla(grupos.median())
    otras = {"tiene la media del tiempo": como_tabla(grupos.mean()),
             "cuenta pedidos": como_tabla(grupos.size().astype(float)),
             "tiene la suma del tiempo": como_tabla(grupos.sum()),
             "tiene el máximo del tiempo": como_tabla(grupos.max()),
             "tiene el mínimo del tiempo": como_tabla(grupos.min())}
    margenes = {"All", "Total"}
    pista_serie = False

    x = tabla
    # --- sin resumir: una fila por pedido, o varias por grupo (unstack fallaría) ---
    if isinstance(x, (pd.Series, pd.DataFrame)):
        if len(x) == n:
            print("✗  tabla: tiene una fila por pedido: falta resumir cada grupo con la mediana "
                  "(pd.pivot_table con values=, index=, columns= y aggfunc=)")
            return
        if isinstance(x.index, pd.MultiIndex) and x.index.has_duplicates:
            print("✗  tabla: tiene varias filas por cada ciudad y franja: falta resumir cada grupo "
                  "con la mediana")
            return
    # --- lo que no es una tabla ---
    if isinstance(x, pd.Series):
        if isinstance(x.index, pd.MultiIndex) and x.index.nlevels == 2:
            x = x.unstack()
            pista_serie = True
        elif isinstance(x.index, pd.MultiIndex):
            print(f"✗  tabla: cruza {x.index.nlevels} niveles; la tabla dinámica cruza solo dos: "
                  "las ciudades y las franjas")
            return
        else:
            print("✗  tabla: tiene una sola dimensión; la tabla dinámica cruza dos: las ciudades "
                  "y las franjas")
            return
    if not isinstance(x, pd.DataFrame):
        if x is None:
            print("✗  tabla: está vacía (None): ¿le asignaste el resultado de un print?")
        elif isinstance(x, str):
            print("✗  tabla: es texto; hace falta la tabla que devuelve pd.pivot_table")
        elif callable(x):
            print("✗  tabla: es una función, no su resultado: ¿faltaron los paréntesis o los "
                  "argumentos de pd.pivot_table?")
        elif type(x).__name__.endswith("GroupBy"):
            print("✗  tabla: es el agrupamiento, todavía sin la medida: falta calcularla en cada grupo")
        elif isinstance(x, (numbers.Number, np.number)):
            print("✗  tabla: es un solo número; hace falta una tabla de ciudades por franjas")
        elif isinstance(x, (list, tuple, dict, np.ndarray)):
            print("✗  tabla: no es una tabla de pandas: usa pd.pivot_table, que trae las "
                  "ciudades y las franjas como etiquetas")
        else:
            print(f"✗  tabla: tiene que ser una tabla de pandas (es {type(x).__name__})")
        return
    # --- una tabla: la forma ---
    if isinstance(x.index, pd.MultiIndex) and x.index.nlevels == 2 and x.shape[1] == 1:
        x = x.iloc[:, 0].unstack()   # groupby([...])[["col"]].median(): una columna, dos niveles
        pista_serie = True
    funciones = {"median", "mean", "count", "size", "sum", "min", "max", "std", "var", "nunique"}
    while isinstance(x.columns, pd.MultiIndex):
        nivel0 = set(_texto(x.columns.get_level_values(0)))
        if len(nivel0) == 1 and nivel0 <= _COLUMNAS | funciones:
            x = x.droplevel(0, axis=1)   # values=[...] o aggfunc=[...], entre corchetes
        elif nivel0 & _COLUMNAS:
            print("✗  tabla: resume varias columnas a la vez: ¿falta values=? Indica la medida que "
                  "se resume")
            return
        elif nivel0 <= funciones:
            print("✗  tabla: resume con varias funciones a la vez; en aggfunc= deja solo la que se pide")
            return
        else:
            print("✗  tabla: sus columnas tienen varios niveles: ¿pusiste dos dimensiones en "
                  "columns=? Van una en index= y otra en columns=")
            return
    if isinstance(x.index, pd.MultiIndex):
        cols = set(_texto(x.columns))
        if {"count", "mean", "50%"} <= cols:
            print("✗  tabla: describe() da varias medidas; aquí va solo la mediana, con la franja "
                  "en las columnas (pd.pivot_table lo hace de una vez)")
        elif x.index.nlevels == 2 and cols <= _COLUMNAS | funciones:
            print("✗  tabla: tiene varias medidas por grupo; aquí va solo la mediana del tiempo, con "
                  "la franja en las columnas (pd.pivot_table lo hace de una vez)")
        else:
            print("✗  tabla: sus filas tienen varios niveles: ¿pusiste dos dimensiones en index=? Van "
                  "una en index= y otra en columns=")
        return
    if x.size == 0:
        print("✗  tabla: está vacía")
        return
    columnas_txt = set(_texto(x.columns))
    if "ciudad" in columnas_txt or "franja" in columnas_txt:
        print("✗  tabla: una dimensión quedó como columna (¿usaste reset_index?); déjala en el "
              "índice, como sale de pd.pivot_table")
        return
    filas = [e for e in _texto(x.index) if e not in margenes]
    cols = [e for e in _texto(x.columns) if e not in margenes]
    hay_margenes = len(filas) < len(x.index) or len(cols) < len(x.columns)
    if len(set(filas)) != len(filas) or len(set(cols)) != len(cols):
        print("✗  tabla: tiene etiquetas repetidas; cada ciudad y cada franja deben aparecer una vez")
        return
    if sorted(filas) == sorted(franjas) and sorted(cols) == sorted(ciudades):
        x = x.T   # transpuesta: también vale
        filas, cols = cols, filas
    if not (sorted(filas) == sorted(ciudades) and sorted(cols) == sorted(franjas)):
        dims = set(filas) | set(cols)
        faltan = ([c for c in ciudades if c not in dims] if set(ciudades) & dims else []) + \
                 ([f for f in franjas if f not in dims] if set(franjas) & dims else [])
        if dims & {"Sí", "No"}:
            print("✗  tabla: una de sus dimensiones es la lluvia, como en la celda [dinamica]; aquí "
                  "se cruzan la ciudad y la franja")
        elif faltan and (dims - set(ciudades) - set(franjas)) == set():
            print(f"✗  tabla: le falta{'n' if len(faltan) > 1 else ''} {', '.join(faltan)}: ¿filtraste "
                  "los pedidos o quitaste columnas? La tabla va con todos")
        elif set(filas) == set(ciudades) or set(cols) == set(ciudades):
            print("✗  tabla: las ciudades están; la otra dimensión tiene que ser la franja")
        elif set(filas) == set(franjas) or set(cols) == set(franjas):
            print("✗  tabla: las franjas están; la otra dimensión tiene que ser la ciudad")
        elif dims & _COLUMNAS:
            print("✗  tabla: sus etiquetas son nombres de columnas: ¿pasaste la medida en index= o "
                  "en columns=? La medida va en values=")
        else:
            print("✗  tabla: sus filas y columnas tienen que ser las cinco ciudades y las cuatro "
                  "franjas: revisa index= y columns=")
        return
    # --- los valores ---
    sin_margenes = x.loc[[e not in margenes for e in _texto(x.index)],
                         [e not in margenes for e in _texto(x.columns)]]
    if pd.api.types.is_bool_dtype(sin_margenes.stack()):
        print("✗  tabla: sus valores son True o False; hace falta la mediana del tiempo")
        return
    if any(isinstance(e, str) for e in sin_margenes.to_numpy().ravel()):
        print("✗  tabla: sus valores son texto (¿astype(str)?); déjalos como números")
        return
    try:
        valores = sin_margenes.apply(pd.to_numeric, errors="raise").astype(float)
    except (TypeError, ValueError):
        print("✗  tabla: sus valores no son números (¿astype(str)?); déjalos como números")
        return
    valores.index = _texto(valores.index)
    valores.columns = _texto(valores.columns)
    valores = valores.reindex(index=ciudades, columns=franjas)
    if valores.isna().any().any():
        print("✗  tabla: tiene celdas vacías (nan): ¿filtraste los pedidos antes de construirla?")
        return

    def igual(a, b, tolerancia=0.051):
        return bool((a - b).abs().max().max() <= tolerancia)

    if igual(valores, verdad):
        print("✓  tabla" + (" (con márgenes, que no se revisan)" if hay_margenes else ""))
        if pista_serie:
            print("·  Las dos dimensiones quedaron en las filas: con .unstack() las franjas pasan "
                  "a las columnas. pd.pivot_table la construye así de una vez")
        _mostrar(verdad.round(1))
        print("✓  Cuadra. Responde abajo: ¿la franja más lenta es la misma en todas las ciudades?")
        return
    for nombre, otra in otras.items():
        if igual(valores, otra):
            print(f"✗  tabla: esa tabla {nombre}; se pide la mediana del tiempo (aggfunc=)")
            return
    if igual(valores, verdad, 0.51) and bool((valores == valores.round()).all().all()):
        print("✗  tabla: casi: le quitaste los decimales; deja al menos uno")
        return
    numericas = original.select_dtypes("number").drop(columns="tiempo_entrega_min")
    for col in numericas.columns:
        mediana_otra = como_tabla(original.groupby(["ciudad", "franja"], observed=True)[col].median())
        if igual(valores, mediana_otra.astype(float), 1e-6):
            print("✗  tabla: esas medianas son de otra columna: ¿values= es tiempo_entrega_min?")
            return
    print("✗  tabla: no cuadra: revisa la medida (values=), la función (aggfunc=) y que estén "
          "todos los pedidos")


@_seguro
def revisar_tope(*sueltos, mediana_30=..., media_30=..., **otros):
    """Ejercicio 3 (opcional): mediana y media de la distancia si los 20 pedidos de 14 km fueran de 30."""
    import pandas as pd

    if sueltos:
        print("✗  Pasa los valores por nombre, como en la plantilla: "
              "revisar_tope(mediana_30=mediana_30, media_30=media_30)")
        return
    if _sobrantes((), otros, ["mediana_30", "media_30"]):
        return
    original = _original()
    if original is None:
        return
    d = original["distancia_km"]
    n = len(d)
    d30 = d.where(d != 14, 30)
    verdad = {"mediana_30": d30.median(), "media_30": d30.mean()}
    con_14 = {"mediana": d.median(), "media": d.mean()}
    sin_tope = d[d != 14]
    tol = 0.005
    bien = 0

    for nombre, x in [("mediana_30", mediana_30), ("media_30", media_30)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        val, problema = _un_numero(x, n)
        if problema:
            print(f"✗  {nombre}: {problema}")
            continue
        if nombre == "mediana_30":
            if _cerca(val, verdad["mediana_30"], tol):
                print("✓  mediana_30")
                bien += 1
            elif _cerca(val, verdad["media_30"], tol) or _cerca(val, con_14["media"], tol):
                print("✗  mediana_30: eso parece una media; la mediana es el valor del medio")
            elif _cerca(val, 30, tol) or _cerca(val, 14, tol):
                print("✗  mediana_30: esa es la distancia de los 20 pedidos; la mediana es la de "
                      "los 12 000")
            elif _cerca(val, sin_tope.median(), tol):
                print("✗  mediana_30: ¿quitaste los 20 pedidos? La idea es cambiarles la distancia, "
                      "no borrarlos")
            else:
                print("✗  mediana_30: no cuadra: es la mediana de la copia, con los 12 000 pedidos")
        else:
            if _cerca(val, verdad["media_30"], tol):
                print("✓  media_30")
                bien += 1
            elif _cerca(val, con_14["media"], tol):
                print("✗  media_30: esa es la media con los 14 km: ¿la copia tiene 30 donde había "
                      "14? replace devuelve una copia: guárdala en distancia_30")
            elif _cerca(val, sin_tope.mean(), tol):
                print("✗  media_30: ¿quitaste los 20 pedidos? La idea es cambiarles la distancia, "
                      "no borrarlos")
            elif _cerca(val, verdad["mediana_30"], tol):
                print("✗  media_30: eso parece la mediana; la media suma y divide")
            elif any(_cerca(val, round(verdad["media_30"], k), 1e-9) for k in (0, 1)):
                print("✗  media_30: casi: aquí la diferencia está en las centésimas; deja al "
                      "menos dos decimales")
            elif _cerca(val, 30, tol) or _cerca(val, 14, tol):
                print("✗  media_30: esa es la distancia de los 20 pedidos; la media es la de los "
                      "12 000, con esos 20 cambiados")
            elif val > verdad["media_30"]:
                print("✗  media_30: salió de más: ¿cambiaste solo los pedidos de exactamente 14 km, "
                      "y por 30?")
            else:
                print("✗  media_30: no cuadra: es la media de la copia, con los 12 000 pedidos")

    # el enunciado pide la copia «sin cambiar pedidos»: se mira la tabla del cuaderno
    try:
        from IPython import get_ipython
        cuaderno = get_ipython().user_ns.get("pedidos") if get_ipython() is not None else None
    except ImportError:
        cuaderno = None
    if (isinstance(cuaderno, pd.DataFrame) and "distancia_km" in cuaderno.columns
            and len(cuaderno) == n
            and not cuaderno["distancia_km"].reset_index(drop=True).equals(d)):
        print("✗  pedidos: su distancia_km ya no es la original: la copia se hace sin tocar pedidos. "
              "Vuelve a ejecutar la celda [cargar] y guarda el cambio solo en distancia_30")
        return
    if bien == 2:
        tabla = pd.DataFrame({"con 14 km": [con_14["mediana"], con_14["media"]],
                              "con 30 km": [verdad["mediana_30"], verdad["media_30"]]},
                             index=["mediana", "media"])
        _mostrar(tabla.round(3))
        print("✓  Las dos cuadran. Responde abajo: ¿qué cambia y qué no? ¿Qué te dice eso de un "
              "dato censurado?")
