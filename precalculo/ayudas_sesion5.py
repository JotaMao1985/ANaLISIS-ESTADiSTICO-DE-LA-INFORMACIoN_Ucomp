"""Sesión 5: estilo de las gráficas del curso, la calificación completa y los verificadores.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py. Cada
verificador recibe lo que el estudiante calculó, dice qué está bien y, en lo demás, da una
pista sin la respuesta. Nunca se cae: un «...» sin reemplazar o un tipo inesperado se avisa.

calificacion_completa() repite el generador de la celda oculta para recuperar la calificación
que habría dado cada pedido. Solo existe porque el caso es ficticio: se usa una sola vez, en la
celda [comprobacion], y nunca en el tablero.

Tolerancias: ±1 pedido por ciudad en el ejercicio 1 (cada ciudad redondea), ±0,06 puntos
porcentuales en el ejercicio 2 (una proporción entre 0 y 1 se acepta con una pista) y conteos
exactos en el ejercicio 3, que no supone cuántos pedidos trae la muestra.
"""


def _estilo_graficas():
    """Colores del curso y letras que se leen en Colab y proyectadas."""
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "axes.prop_cycle": mpl.cycler(color=["#8A2E9E", "#F46201", "#566B7F"]),
        "figure.figsize": (6.4, 3.6),
        "figure.constrained_layout.use": True,
        "font.size": 13,
        "axes.titlesize": 15,
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
            print(f"✗  No pude revisar lo que entregaste ({type(error).__name__}). Revisa que lo que "
                  "entregas sea el resultado de un cálculo de pandas y vuelve a ejecutar la celda")
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


# ---------------------------------------------------------------------------------------------
# La calificación completa (solo para la comprobación de la sesión 5)
# ---------------------------------------------------------------------------------------------

def calificacion_completa():
    """La calificación que habría dado cada pedido si todos calificaran. Solo en un caso ficticio.

    Repite el generador de la celda oculta grabando los números al azar de cada pedido y vuelve a
    correr cada pedido con esa misma cinta, pero con el último número (el que decide si califica)
    puesto en 0: así todos califican y lo demás no cambia. Devuelve una serie de enteros indexada
    por id_pedido, que se cruza con map, por código. No escribe archivos. Si algo no cuadra con
    datos/pedidos.csv, avisa y devuelve None.
    """
    import numpy as np
    import pandas as pd
    from datetime import timedelta

    try:
        base = _Azar
        generar = _pedido
        semilla, total, inicio, n_dias, orden_franjas = SEMILLA, N_PEDIDOS, INICIO, DIAS, list(FRANJAS)
    except NameError:
        print("✗  No encuentro el generador de los datos: ejecuta primero la celda que crea los datos "
              "(Entorno de ejecución → Ejecutar anteriores)")
        return None

    class _Graba(base):
        """El azar de siempre, pero anota cada número que entrega, pedido por pedido."""

        def __init__(self, s):
            super().__init__(s)
            self.cinta = []

        def u(self):
            x = super().u()
            self.cinta[-1].append(x)
            return x

    class _Repite(base):
        """Entrega los números de una cinta grabada, en el mismo orden."""

        def __init__(self, cinta):
            self.cinta, self.i = cinta, 0

        def u(self):
            x = self.cinta[self.i]
            self.i += 1
            return x

    try:
        original = _original()
        if original is None:
            return None
        dias = [inicio + timedelta(days=d) for d in range(n_dias)]
        pesos_dias = [1.35 if d.weekday() >= 4 else 1.0 for d in dias]
        az = _Graba(semilla)
        vistos, completos = [], []
        for _ in range(total):
            az.cinta.append([])
            vistos.append(generar(az, dias, pesos_dias))
            cinta = az.cinta[-1][:-1] + [0.0]       # el último número decide si califica
            repite = _Repite(cinta)
            completos.append(generar(repite, dias, pesos_dias))
            if repite.i != len(cinta):
                raise ValueError("la cinta no se consumió entera")
        orden = sorted(range(total), key=lambda i: (vistos[i]["fecha"],
                                                    orden_franjas.index(vistos[i]["franja"])))
        ids = [f"P{k:05d}" for k in range(1, total + 1)]
        # 1) Las demás columnas no cambian al hacer que todos califiquen
        for i in orden:
            a, b = vistos[i], completos[i]
            if any(a[c] != b[c] for c in a if c != "calificacion") or b["calificacion"] == "":
                raise ValueError("cambió otra columna")
        # 2) Coincide con datos/pedidos.csv: los mismos pedidos y las calificaciones visibles
        tabla = pd.DataFrame([vistos[i] for i in orden])
        tabla["fecha"] = [vistos[i]["fecha"].isoformat() for i in orden]
        if (len(original) != total or list(original["id_pedido"].astype(str)) != ids
                or list(original["fecha"].astype(str)) != list(tabla["fecha"])):
            raise ValueError("los pedidos no son los del archivo")
        for c in ["franja", "ciudad", "categoria", "medio_pago", "suscriptor", "lluvia"]:
            if list(original[c].astype(str)) != list(tabla[c].astype(str)):
                raise ValueError(f"cambió {c}")
        for c in ["n_productos", "valor_pedido", "estrato", "distancia_km", "temperatura_c",
                  "tiempo_entrega_min"]:
            if not np.allclose(original[c].to_numpy(dtype=float), tabla[c].to_numpy(dtype=float),
                               rtol=0, atol=1e-9):
                raise ValueError(f"cambió {c}")
        if list(original["calificacion"].isna()) != [v == "" for v in tabla["calificacion"]]:
            raise ValueError("cambió qué pedidos calificaron")
        completa = pd.Series([int(completos[i]["calificacion"]) for i in orden],
                             index=pd.Index(ids, name="id_pedido"), name="calificacion_completa")
        visibles = original.set_index("id_pedido")["calificacion"].dropna()
        if not (completa.loc[visibles.index] == visibles.astype(int)).all():
            raise ValueError("no coincide con las calificaciones visibles")
        return completa
    except Exception as error:   # noqa: BLE001 — nunca un traceback
        print("✗  No pude reconstruir la calificación completa: no coincide con datos/pedidos.csv "
              f"({error}). Vuelve a ejecutar la celda que crea los datos y [cargar], sin cambiarlas")
        return None


# ---------------------------------------------------------------------------------------------
# Auxiliares de los verificadores
# ---------------------------------------------------------------------------------------------

def _no_es_tabla(nombre, x, agrupado="todavía sin la muestra: falta .sample(...) al final"):
    """Mensaje para lo que no es un DataFrame (o None si sí lo es)."""
    import numbers
    import numpy as np
    import pandas as pd

    if isinstance(x, pd.DataFrame):
        return None
    if type(x).__name__.endswith("GroupBy"):
        return f"{nombre}: es el agrupamiento, {agrupado}"
    if isinstance(x, pd.Series) and len(x) and pd.api.types.is_bool_dtype(x):
        return (f"{nombre}: es la condición, un True o False por pedido; úsala para quedarte con "
                "los pedidos: pedidos[condición]")
    if isinstance(x, pd.Series) and x.name in ("count", "proportion"):
        return (f"{nombre}: es un conteo (value_counts); hace falta la muestra misma, la tabla con "
                "sus pedidos")
    if isinstance(x, pd.Series):
        return (f"{nombre}: es una sola columna (una serie); hace falta la tabla de pedidos con "
                "todas sus columnas: ¿elegiste una columna con [\"...\"]?")
    if x is None:
        return f"{nombre}: está vacía (None): ¿le asignaste el resultado de un print?"
    if isinstance(x, str):
        return f"{nombre}: es texto; hace falta la tabla de pedidos que devuelve pandas"
    if callable(x):
        return f"{nombre}: es una función, no su resultado: ¿faltaron los paréntesis del final, ()?"
    if isinstance(x, (bool, np.bool_)):
        return f"{nombre}: es True o False; hace falta una tabla de pedidos"
    if isinstance(x, (numbers.Number, np.number)):
        return (f"{nombre}: es un solo número; hace falta la tabla de pedidos de la muestra "
                "(un DataFrame), no cuántos son")
    if isinstance(x, (list, tuple, dict, set, np.ndarray)):
        return f"{nombre}: no es una tabla de pandas: saca la muestra de pedidos con pandas"
    return f"{nombre}: tiene que ser una tabla de pandas (es {type(x).__name__})"


def _filas(nombre, x, original, repetidos="¿usaste replace=True?"):
    """Los id_pedido de las filas de x, comprobando que son pedidos reales y sin cambios.

    Usa la columna id_pedido, el índice si son los id_pedido (set_index) o, si no, el número de
    fila original (el índice). Devuelve (lista de id, None) o (None, mensaje)."""
    import numpy as np
    import pandas as pd

    indice = x.index.get_level_values(-1) if isinstance(x.index, pd.MultiIndex) else x.index
    if {"count", "mean", "std"} <= set(map(str, x.index)):
        return None, (f"{nombre}: describe() resume la tabla en unas medidas; hace falta la muestra "
                      "misma, con sus pedidos")
    if "id_pedido" in x.columns:
        ids = x["id_pedido"]
        if isinstance(ids, pd.DataFrame):
            return None, f"{nombre}: tiene la columna id_pedido repetida"
        ids = ids.astype(str).tolist()
        por_id = original.set_index("id_pedido")
        if not set(ids) <= set(por_id.index):
            return None, (f"{nombre}: trae filas que no son pedidos de la tabla: saca la muestra "
                          "de pedidos sin cambiarla")
        filas = por_id.loc[ids]
        posiciones = None
    elif len(indice) and pd.Index(indice).astype(str).isin(original["id_pedido"]).all():
        ids = pd.Index(indice).astype(str).tolist()          # set_index("id_pedido")
        filas = original.set_index("id_pedido").loc[ids]
        posiciones = None
    elif pd.api.types.is_integer_dtype(indice) and len(indice) and \
            indice.min() >= 0 and indice.max() < len(original):
        posiciones = np.asarray(indice)
        filas = original.iloc[posiciones]
        ids = filas["id_pedido"].astype(str).tolist()
    else:
        return None, (f"{nombre}: no encuentro el código de cada pedido (id_pedido) ni su número de "
                      "fila: ¿quitaste columnas o cambiaste el índice? Saca la muestra de pedidos "
                      "tal como está")
    if len(set(ids)) < len(ids):
        return None, (f"{nombre}: hay pedidos repetidos: {repetidos} En una muestra cada "
                      "pedido entra una sola vez")
    cambiados = (f"{nombre}: hay pedidos con valores cambiados (en {{}}): saca la muestra de "
                 "pedidos sin modificarla")
    if posiciones is not None:   # sin id_pedido, el índice tiene que ser el número de fila original
        cambiados = (f"{nombre}: no sé de qué pedido es cada fila: ¿reiniciaste el índice "
                     "(reset_index) o quitaste la columna id_pedido? Deja la muestra como sale de "
                     "pandas")
    for c in ["tiempo_entrega_min", "distancia_km", "valor_pedido"]:
        if c in x.columns and not isinstance(x[c], pd.DataFrame):
            try:
                propios = pd.to_numeric(x[c], errors="raise").to_numpy(dtype=float)
            except (TypeError, ValueError):
                return None, f"{nombre}: la columna {c} ya no tiene números: ¿la cambiaste?"
            if not np.allclose(propios, filas[c].to_numpy(dtype=float), equal_nan=True):
                return None, cambiados.format(c)
    if "ciudad" in x.columns and not isinstance(x["ciudad"], pd.DataFrame):
        if list(x["ciudad"].astype(str)) != list(filas["ciudad"].astype(str)):
            return None, cambiados.format("ciudad")
    return ids, None


def _sin_sorteo(original, ids, grupo="ciudad"):
    """¿Las filas de cada grupo siguen un patrón fijo, sin sorteo?

    "seguidas" si en cada grupo son filas consecutivas (head, tail o un tramo); "desde_primera" si
    van a paso fijo desde la primera fila de cada grupo (iloc[::k]); "paso_azar" si van a paso fijo
    con otro inicio (un sistemático con inicio al azar, que sí es probabilístico); None si no hay
    patrón (hubo sorteo). Con las semillas de 100 a 999, ninguna muestra al azar tiene patrón."""
    import numpy as np

    orden = original.groupby(grupo).cumcount().set_axis(original["id_pedido"].astype(str))
    g = original.set_index("id_pedido").loc[ids, grupo]
    pasos, inicios = set(), set()
    for _, q in orden.loc[ids].groupby(g.values):
        q = np.sort(q.to_numpy())
        if len(q) < 3 or len(set(np.diff(q))) > 1:
            return None
        pasos |= set(np.diff(q).tolist())
        inicios.add(int(q[0]))
    if pasos == {1}:
        return "seguidas"
    return "desde_primera" if inicios == {0} else "paso_azar"


def _dias_sin_sorteo(original, fechas):
    """Lo mismo para los días: "seguidas", "desde_primera", "paso_azar" o None."""
    import numpy as np

    todas = sorted(original["fecha"].astype(str).unique())
    pos = sorted(todas.index(f) for f in fechas)
    pasos = set(np.diff(pos).tolist())
    if len(pos) < 3 or len(pasos) > 1:
        return None
    if pasos == {1}:
        return "seguidas"
    return "desde_primera" if pos[0] == 0 else "paso_azar"


# ---------------------------------------------------------------------------------------------
# Ejercicio 1 · Una muestra estratificada proporcional
# ---------------------------------------------------------------------------------------------

@_seguro
def revisar_estratificada(muestra=..., *sobran, **otros):
    """Ejercicio 1: muestra estratificada por ciudad con el 2 % de cada ciudad."""
    import pandas as pd

    if _sobrantes(sobran, otros, ["muestra"]):
        return
    if muestra is Ellipsis:
        print("·  muestra: todavía tiene ...")
        return
    problema = _no_es_tabla("muestra", muestra)
    if problema:
        print("✗  " + problema)
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    x = muestra
    if len(x) == 0:
        print("✗  muestra: está vacía: ¿filtraste los pedidos antes de sacarla? La muestra sale de "
              "pedidos, agrupando por ciudad")
        return
    ids, problema = _filas("muestra", x, original)
    if problema:
        print("✗  " + problema)
        return
    if len(ids) == n:
        print("✗  muestra: es la tabla entera: falta sacar la muestra (el 2 % de cada ciudad)")
        return
    poblacion = original["ciudad"].value_counts()
    ciudad = original.set_index("id_pedido").loc[ids, "ciudad"]   # la ciudad de cada pedido
    obtenido = ciudad.value_counts().reindex(poblacion.index, fill_value=0)
    esperado = (poblacion * 0.02).round().astype(int)
    faltan = [c for c in poblacion.index if obtenido[c] == 0]

    def proporcional(fraccion):
        return bool(((obtenido - (poblacion * fraccion).round()).abs() <= 1).all())

    def agrupo_estrato():   # la confusión que avisa la diapositiva: la columna estrato
        por_estrato = original["estrato"].value_counts()
        en_muestra = original.set_index("id_pedido").loc[ids, "estrato"].value_counts()
        en_muestra = en_muestra.reindex(por_estrato.index, fill_value=0)
        return bool((en_muestra == (por_estrato * 0.02).round()).all())

    if proporcional(0.02):
        patron = _sin_sorteo(original, ids)
        if patron == "seguidas":
            print("✗  muestra: en cada ciudad tomaste pedidos seguidos (los primeros, los últimos o un "
                  "tramo): no hay sorteo, es una muestra por conveniencia. Agrupa por ciudad y usa "
                  ".sample(frac=0.02, random_state=mi_semilla)")
            return
        if patron == "desde_primera":
            print("✗  muestra: en cada ciudad tomaste uno de cada tantos desde el primero: no hay "
                  "sorteo, es una muestra por conveniencia. Agrupa por ciudad y usa "
                  ".sample(frac=0.02, random_state=mi_semilla)")
            return
        print("✓  muestra: el 2 % de cada ciudad")
        if patron == "paso_azar":
            print("·  Es un sistemático dentro de cada ciudad, con inicio al azar: también es "
                  "probabilístico. El ejercicio pide el estratificado de la celda [estratificado], "
                  "con .sample")
        sin_cambiar = original.groupby("ciudad").sample(frac=0.02, random_state=123)
        if sorted(ids) == sorted(sin_cambiar["id_pedido"].astype(str)):
            print("·  Es la muestra de mi_semilla = 123: cámbiala por un número de tres cifras "
                  "que elijas tú y vuelve a ejecutar")
        tabla = pd.DataFrame({"pedidos": poblacion, "en tu muestra": obtenido,
                              "% de la ciudad": (obtenido / poblacion * 100).round(2)})
        tabla.index.name = "ciudad"
        _mostrar(tabla)
        tiempo = original.set_index("id_pedido").loc[ids, "tiempo_entrega_min"]
        print(f"Tu x̄ = {tiempo.mean():.2f} min · μ = {original['tiempo_entrega_min'].mean():.2f} "
              "min (los 12 000 pedidos)")
        print("✓  Cuadra. Responde abajo: con una aleatoria simple de 240 pedidos, ¿saldrían siempre "
              "24 de Bucaramanga? ¿Por qué tu estratificada sí trae siempre el mismo número?")
        return
    if faltan and len(faltan) < len(poblacion):
        print(f"✗  muestra: le falta{'n' if len(faltan) > 1 else ''} {', '.join(faltan)}: ¿filtraste "
              "los pedidos? La muestra estratificada sortea en todas las ciudades")
    elif len(set(obtenido)) == 1 and len(poblacion) > 1:
        print("✗  muestra: todas las ciudades traen el mismo número de pedidos: eso es el mismo n "
              "por ciudad. Proporcional es la misma fracción en cada ciudad: usa frac=, no n=")
    elif proporcional(1 / 30):
        print("✗  muestra: esa es la fracción del ejemplo de la clase, 1 de cada 30; aquí va el 2 % "
              "(frac=0.02)")
    elif agrupo_estrato():
        print("✗  muestra: es proporcional por la columna estrato, no por ciudad: en muestreo, el "
              "estrato es el grupo que se sortea por separado, y aquí es la ciudad: groupby(\"ciudad\")")
    elif abs(len(ids) - esperado.sum()) <= 3:
        print("✗  muestra: el total está bien, pero las ciudades no traen su parte: ¿agrupaste por "
              "ciudad antes de .sample? Sin agrupar, cada ciudad sale con lo que toque al azar")
    elif original.set_index("id_pedido").loc[ids, "calificacion"].notna().all():
        print("✗  muestra: solo trae pedidos calificados: ¿filtraste (dropna) antes de sacarla? El 2 % "
              "es de todos los pedidos de cada ciudad")
    elif proporcional(len(ids) / n):
        parte = f"{len(ids) / n * 100:.1f}".replace(".", ",")
        print(f"✗  muestra: es proporcional, pero con el {parte} % de cada ciudad; se pide el 2 % "
              "(frac=0.02). Si ya usaste 0.02, ¿filtraste los pedidos antes de agrupar?")
    else:
        print("✗  muestra: no cuadra: agrupa por ciudad y saca el 2 % de cada una con "
              "frac=0.02 y tu semilla")


# ---------------------------------------------------------------------------------------------
# Ejercicio 2 · La insatisfacción de Bogotá, ponderada
# ---------------------------------------------------------------------------------------------

def _ponderar(d, mayor_igual=False, pesos=None):
    """Las cifras del 1 y 2 (y del 4 y 5) en %, sin ponderar y ponderadas, y sus errores típicos."""
    import numpy as np
    import pandas as pd

    marca = d["tiempo_entrega_min"] >= 55 if mayor_igual else d["tiempo_entrega_min"] > 55
    grupo = pd.Series(np.where(marca, "más de 55 min", "55 min o menos"), index=d.index)
    k = d["calificacion"].notna()
    peso = grupo.value_counts() / grupo[k].value_counts() if pesos is None else pesos
    w = grupo[k].map(peso).astype(float)
    estrellas = d.loc[k, "calificacion"].astype(int)
    y12, y45 = (estrellas <= 2).astype(int), (estrellas >= 4).astype(int)
    return {"sin": y12.mean() * 100, "pond": (w * y12).sum() / w.sum() * 100,
            "sin45": y45.mean() * 100, "pond45": (w * y45).sum() / w.sum() * 100,
            "den_todos": (w * y12).sum() / grupo.map(peso).astype(float).sum() * 100,
            "den_pedidos": y12.sum() / len(d) * 100,
            "invertidos": ((1 / w) * y12).sum() / (1 / w).sum() * 100,
            "entre_calificados": (w * y12).sum() / k.sum() * 100,
            "media": estrellas.mean(), "media_pond": (w * estrellas).sum() / w.sum(),
            "peso": peso}


@_seguro
def revisar_ponderada(*sueltos, sin_ponderar=..., ponderado=..., **otros):
    """Ejercicio 2: % de 1 o 2 estrellas en Bogotá, sin ponderar y ponderado por el tiempo."""
    import pandas as pd

    nombres = ["sin_ponderar", "ponderado"]
    if sueltos:
        print("✗  Pasa los valores por nombre, como en la plantilla: "
              "revisar_ponderada(sin_ponderar=sin_ponderar, ponderado=ponderado)")
        return
    if _sobrantes((), otros, nombres):
        return
    original = _original()
    if original is None:
        return
    bog = original[original["ciudad"] == "Bogotá"]
    b = _ponderar(bog)
    b_ge = _ponderar(bog, mayor_igual=True)
    t = _ponderar(original)
    t_ge = _ponderar(original, mayor_igual=True)
    b_nac = _ponderar(bog, pesos=t["peso"])
    verdad = {"sin_ponderar": [b["sin"]], "ponderado": [b["pond"], b_ge["pond"]]}
    tol, tol_pista = 0.06, 0.006
    # Las pistas, en el orden del diseño; cada una con las cifras que la delatan
    pistas = {
        "ponderado": [
            ([b["den_todos"]], "el denominador incluye a todos los pedidos: la suma va solo sobre "
                               "los calificados (filtra antes de sumar los pesos)"),
            ([t["pond"], t_ge["pond"], t["sin"]], "esa es la cifra de todos los pedidos, no la de "
                                                   "Bogotá: ¿cambiaste la línea datos =?"),
            ([b["den_pedidos"]], "el denominador son todos los pedidos de Bogotá; el % se calcula "
                                 "entre los calificados"),
            ([b["invertidos"]], "los pesos están al revés: el peso de cada grupo es pedidos ÷ "
                                "calificados"),
            ([b["entre_calificados"]], "dividiste entre el número de calificados; con pesos, se "
                                       "divide entre la suma de los pesos"),
            ([b["media"], b["media_pond"]], "esa es la media de las estrellas: la satisfacción no "
                                            "se promedia (¿usaste np.average?); cuenta los pedidos de 1 "
                                            "o 2 estrellas"),
            ([b["sin45"], b["pond45"]], "ese es el % de 4 o 5 estrellas; aquí va el de 1 o 2"),
            ([b_nac["pond"]], "usaste los pesos de todos los pedidos; Bogotá tiene los suyos: "
                              "calcúlalos dentro de datos"),
            ([b["sin"]], "ese es el % sin ponderar. Si los pesos salieron 1, datos solo trae los "
                         "calificados: tiene que traer todos los pedidos de Bogotá (el peso es "
                         "pedidos ÷ calificados). Si los pesos están bien, ¿multiplicaste cada "
                         "calificación por su peso?"),
        ],
        "sin_ponderar": [
            ([b["den_todos"]], "el denominador incluye a todos los pedidos; sin ponderar es el % "
                               "entre los calificados"),
            ([t["sin"], t["pond"]], "esa es la cifra de todos los pedidos, no la de Bogotá: "
                                    "¿cambiaste la línea datos =?"),
            ([b["den_pedidos"]], "el denominador son todos los pedidos de Bogotá; el % se calcula "
                                 "entre los calificados"),
            ([b["media"], b["media_pond"]], "esa es la media de las estrellas: la satisfacción no "
                                            "se promedia; cuenta los pedidos de 1 o 2 estrellas"),
            ([b["sin45"], b["pond45"]], "ese es el % de 4 o 5 estrellas; aquí va el de 1 o 2"),
            ([b["pond"]], "ese es el ponderado; sin ponderar es el % entre los calificados, sin "
                          "pesos"),
        ],
    }

    def _es(x, valores):
        if x is Ellipsis:
            return False
        val = _un_numero(x, len(original))[0]
        return any(_cerca(val, v, tol) or _cerca(val, v / 100, tol / 100) for v in valores)

    if _es(sin_ponderar, verdad["ponderado"]) and _es(ponderado, verdad["sin_ponderar"]):
        print("✗  ¿Intercambiaste los dos? sin_ponderar va sin pesos y ponderado, con pesos")
        return
    bien = 0
    proporcion = False
    for nombre, x in [("sin_ponderar", sin_ponderar), ("ponderado", ponderado)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        val, problema = _un_numero(x, len(original))
        if problema:
            if isinstance(x, (pd.Series, pd.DataFrame)) and len(x) in (
                    len(bog), int(bog["calificacion"].notna().sum()), len(original)):
                problema = "esa es la columna entera, un valor por pedido: falta resumirla"
            elif problema.startswith("salió nan"):
                problema = ("salió nan, que es lo que da 0 ÷ 0: ¿datos quedó sin pedidos? Escribe la "
                            "ciudad igual que en la tabla: \"Bogotá\", con tilde")
            print(f"✗  {nombre}: {problema}")
            continue
        if any(_cerca(val, v, tol) for v in verdad[nombre]):
            print(f"✓  {nombre}")
            bien += 1
            continue
        if any(_cerca(val, v / 100, tol / 100) for v in verdad[nombre]):
            print(f"✓  {nombre} (como proporción)")
            proporcion = True
            bien += 1
            continue
        for cifras, pista in pistas[nombre]:
            if any(_cerca(val, c, tol_pista) or _cerca(val, c / 100, tol_pista / 100)
                   for c in cifras):
                print(f"✗  {nombre}: {pista}")
                break
        else:
            if val < 0 or val > 100:
                print(f"✗  {nombre}: un porcentaje va de 0 a 100: revisa el cálculo")
            else:
                print(f"✗  {nombre}: no cuadra: revisa que datos sean los pedidos de Bogotá y que el "
                      "% sea de 1 o 2 estrellas entre los calificados")
    if proporcion:
        print("·  Diste una proporción (entre 0 y 1); el ejercicio lo pide en %: multiplica por 100")
    if bien == 2:
        tabla = pd.DataFrame({"sin ponderar": [b["sin"], t["sin"]],
                              "ponderado": [b["pond"], t["pond"]]},
                             index=["Bogotá", "Todos los pedidos"])
        tabla.index.name = "1 o 2 estrellas (%)"
        _mostrar(tabla.round(2))
        print("✓  Las dos cuadran. Responde abajo: en puntos, ¿por qué la corrección de Bogotá es "
              "mayor que la del total? En proporción, las dos se parecen")


# ---------------------------------------------------------------------------------------------
# Ejercicio 3 (opcional) · Una muestra por conglomerados
# ---------------------------------------------------------------------------------------------

@_seguro
def revisar_conglomerados(muestra=..., *sobran, **otros):
    """Ejercicio 3: todos los pedidos de exactamente 6 días (sin suponer cuántos pedidos son)."""
    import numpy as np
    import pandas as pd

    if _sobrantes(sobran, otros, ["muestra"]):
        return
    if muestra is Ellipsis:
        print("·  muestra: todavía tiene ...")
        return
    original = _original()
    if original is None:
        return
    n = len(original)
    por_dia = original["fecha"].value_counts()
    x = muestra
    if isinstance(x, pd.Series) and 0 < len(x) < n and \
            set(x.astype(str)) <= set(por_dia.index):
        print("✗  muestra: esos son los días (o sus fechas); falta quedarte con todos los pedidos "
              "de esos días")
        return
    if isinstance(x, (list, tuple, set, np.ndarray, pd.Index)) and getattr(x, "ndim", 1) == 1 \
            and 0 < len(x) < n and set(pd.Series(list(x)).astype(str)) <= set(por_dia.index):
        print("✗  muestra: esos son los días; falta quedarte con todos los pedidos de esos días")
        return
    problema = _no_es_tabla("muestra", x, agrupado="y en conglomerados no se agrupa: elige 6 días "
                                                 "al azar y quédate con sus pedidos con isin")
    if problema:
        print("✗  " + problema)
        return
    if len(x) == 0:
        print("✗  muestra: está vacía: ¿a isin le pasaste una tabla? isin necesita los días como una "
              "serie o una lista de fechas, no un DataFrame (y en el mismo formato que la columna "
              "fecha)")
        return
    if set(map(str, x.columns)) == {"fecha"}:
        print("✗  muestra: solo trae las fechas: esos son los días; falta quedarte con todos los "
              "pedidos de esos días")
        return
    ids, problema = _filas("muestra", x, original, repetidos="¿repetiste un día o usaste "
                                                           "replace=True?")
    if problema:
        print("✗  " + problema)
        return
    if len(ids) == n:
        print("✗  muestra: es la tabla entera: falta quedarte solo con los pedidos de 6 días")
        return
    fechas = original.set_index("id_pedido").loc[ids, "fecha"].astype(str)
    cuenta = fechas.value_counts()
    k = len(cuenta)
    completos = bool((cuenta == por_dia.reindex(cuenta.index)).all())
    if len(ids) == 6:
        print("✗  muestra: tiene 6 filas: son 6 pedidos, no 6 días. Un conglomerado entra entero: "
              "elige 6 días y quédate con todos sus pedidos")
    elif len(ids) == len(por_dia) and k == len(por_dia):
        print("✗  muestra: tiene una fila por día: eso es estratificar por día (un pedido de cada "
              "día). Aquí se sortean 6 días y entran todos sus pedidos")
    elif k == 6 and completos and _dias_sin_sorteo(original, cuenta.index) in ("seguidas",
                                                                               "desde_primera"):
        print("✗  muestra: esos 6 días van seguidos (o a paso fijo desde el primero): no los "
              "sorteaste, es una muestra por conveniencia. Sortéalos con .sample(n=6, "
              "random_state=mi_semilla)")
    elif k == 6 and completos:
        print(f"✓  muestra: todos los pedidos de 6 días ({len(ids)} pedidos)")
        if _dias_sin_sorteo(original, cuenta.index) == "paso_azar":
            print("·  Tus días van a paso fijo desde un inicio que no es el primero: si lo sorteaste, "
                  "es un sistemático de días, también probabilístico. El ejercicio pide sortear "
                  "los 6 con .sample")
        dias_123 = original["fecha"].drop_duplicates().sample(n=6, random_state=123)
        dias_clase = original["fecha"].drop_duplicates().sample(n=6, random_state=1)
        if set(cuenta.index) == set(dias_123.astype(str)):
            print("·  Son los días de mi_semilla = 123: cámbiala por un número de tres cifras que "
                  "elijas tú y vuelve a ejecutar")
        elif set(cuenta.index) == set(dias_clase.astype(str)):
            print("·  Son los días de la clase (semilla = 1): usa mi_semilla, con un número de tres "
                  "cifras que elijas tú, y vuelve a ejecutar")
        tabla = cuenta.sort_index().rename("pedidos").to_frame()
        tabla.index.name = "fecha"
        _mostrar(tabla)
        tiempo = original.set_index("id_pedido").loc[ids, "tiempo_entrega_min"]
        mu = original["tiempo_entrega_min"].mean()
        conveniencia = original[original["ciudad"] == "Bogotá"].head(400)["tiempo_entrega_min"].mean()
        lejos = f"{abs(tiempo.mean() - mu):.2f}".replace(".", ",")
        lejos_conv = f"{conveniencia - mu:.2f}".replace(".", ",")
        print(f"Tu x̄ = {tiempo.mean():.2f} min · μ = {mu:.2f} min (los 12 000 pedidos): quedó a "
              f"{lejos} min de μ")
        print(f"✓  Cuadra. Responde abajo: tu x̄ quedó a {lejos} min de μ, y la de conveniencia a "
              f"{lejos_conv}: ¿cuál diferencia es error muestral y cuál es sesgo? ¿Cuál se achicaría "
              "con una muestra más grande?")
    elif k == 6:
        print("✗  muestra: trae 6 días, pero no todos sus pedidos: un conglomerado entra entero. "
              "Quédate con todos los pedidos de esos días (pista: isin)")
    elif completos:
        print(f"✗  muestra: trae los pedidos completos de {k} día{'s' if k > 1 else ''}; se piden "
              "exactamente 6 días")
        if k < 6:
            print("·  Si sorteaste filas de pedidos, un día puede salir dos veces: sortea entre las "
                  "fechas sin repetir, pedidos[\"fecha\"].drop_duplicates()")
    else:
        print(f"✗  muestra: trae pedidos de {k} día{'s' if k > 1 else ''}, y no todos los de cada "
              "uno: elige 6 días al azar y quédate con todos sus pedidos")
