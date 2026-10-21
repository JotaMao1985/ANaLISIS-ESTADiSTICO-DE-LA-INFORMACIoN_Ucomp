"""Sesión 6: estilo de las gráficas del curso y los verificadores de la práctica.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py. Cada
verificador recibe lo que el estudiante calculó, dice qué está bien y, en lo demás, da una
pista sin la respuesta. Nunca se cae: un «...» sin reemplazar o un tipo inesperado se avisa.

La sesión 6 cita la verdad de la sesión 5, pero no vuelve a usar la calificación oculta: este
archivo no la reconstruye (D24 y D25).

Los valores esperados se calculan aquí, en tiempo de ejecución, desde datos/pedidos.csv.
Tolerancias: en el ejercicio 1, la media de las 1000 medias a ±0,2 min de μ y su desviación entre
1,19 y 1,34 min (con las semillas de 100 a 999, n = 100 da de 1,21 a 1,29, con o sin
replace=True; n = 120 llega hasta 1,18 y n = 80 empieza en 1,38); en el ejercicio 2, ±0,05
puntos en cada extremo (una proporción entre 0 y 1 se acepta con una pista); en el ejercicio 3,
del tamaño exacto a su redondeo hacia arriba.
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


def _coma(x, decimales=2):
    """Un número con coma decimal, para los mensajes."""
    return f"{x:.{decimales}f}".replace(".", ",")


def _calificados(original):
    """Los pedidos calificados y si cada uno tiene 4 o 5 estrellas."""
    import pandas as pd

    cal = original[original["calificacion"].notna()]
    return cal, pd.to_numeric(cal["calificacion"]) >= 4


# ---------------------------------------------------------------------------------------------
# Ejercicio 1 · La distribución muestral con n = 100
# ---------------------------------------------------------------------------------------------

def _medias_como_lista(medias, n_pedidos):
    """(lista de floats, None) o (None, mensaje). Acepta lista, tupla, serie, arreglo o Index."""
    import math
    import numbers
    import numpy as np
    import pandas as pd

    x = medias
    if x is None:
        return None, "está vacía (None): ¿le asignaste el resultado de un print o de append?"
    if callable(x) and not isinstance(x, (pd.Series, pd.DataFrame)):
        return None, "es una función, no su resultado: ¿faltaron los paréntesis del final, ()?"
    if isinstance(x, str):
        return None, "es texto; hace falta la lista con las 1000 medias"
    if isinstance(x, (bool, np.bool_)):
        return None, "es True o False; hace falta la lista con las 1000 medias"
    if isinstance(x, (numbers.Number, np.number)) or (isinstance(x, np.ndarray) and x.ndim == 0):
        return None, ("es un solo número; hace falta la lista con las 1000 medias, una por "
                      "muestra")
    if isinstance(x, pd.DataFrame):
        if x.shape[1] == 1:
            x = x.iloc[:, 0]
        else:
            return None, (f"es una tabla de {x.shape[0]} × {x.shape[1]}; hace falta la lista con "
                          "las 1000 medias")
    if isinstance(x, dict):
        x = list(x.values())
    if isinstance(x, (set, frozenset)):
        return None, ("es un conjunto (set), que borra las medias repetidas: usa una lista, "
                      "medias = []")
    if not isinstance(x, (list, tuple, pd.Series, np.ndarray, pd.Index)):
        return None, f"tiene que ser una lista de números (es {type(x).__name__})"
    if isinstance(x, np.ndarray) and x.ndim > 1:
        if min(x.shape) > 1:   # una tabla de verdad, no una sola fila o columna
            return None, (f"es una tabla de {' × '.join(map(str, x.shape))}: cada fila es una "
                          "muestra entera; a medias.append le falta calcular la media, .mean()")
        x = x.ravel()
    elementos = list(x)
    if len(elementos) == 0:
        return None, ("está vacía: ¿medias.append(...) quedó fuera del for? Va con sangría, "
                      "dentro del bucle")
    if isinstance(x, pd.Series) and len(elementos) == n_pedidos:
        return None, ("esa es la columna entera, un valor por pedido: hacen falta las medias de "
                      "las 1000 muestras")
    valores = []
    for e in elementos:
        if isinstance(e, pd.DataFrame):
            return None, ("cada elemento es una muestra entera (una tabla de pedidos): elige la "
                          "columna del tiempo y calcula su media")
        if isinstance(e, (pd.Series, np.ndarray, list, tuple)):
            partes = list(np.ravel(np.asarray(e, dtype=object)))
            if len(partes) > 1 and isinstance(e, pd.Series) and set(map(str, e.index)) & _COLUMNAS:
                return None, ("cada elemento tiene un valor por columna: calculaste la media de "
                              "todas las columnas; quédate con la de tiempo_entrega_min")
            if len(partes) == 1:
                e = partes[0]
            elif len(partes) == 0:
                return None, ("cada elemento es una muestra vacía: ¿n=0? Saca muestras del "
                              "tamaño que pide el ejercicio")
            else:
                return None, (f"cada elemento es una muestra entera ({len(partes)} tiempos), no "
                              "su media: a medias.append le falta calcular la media, .mean()")
        if e is Ellipsis:
            return None, "todavía tiene ...: completa la línea de medias.append"
        if e is None:
            return None, ("tiene valores vacíos (None): ¿guardaste el resultado de un print? "
                          "Guarda la media")
        if isinstance(e, (bool, np.bool_)):
            return None, "tiene True o False; hacen falta las medias del tiempo"
        if isinstance(e, str):
            return None, "tiene texto; hacen falta números: las medias del tiempo"
        if callable(e):
            return None, ("tiene funciones, no resultados: ¿faltaron los paréntesis de "
                          ".mean()?")
        if not isinstance(e, (numbers.Real, np.number)) or isinstance(e, np.complexfloating):
            return None, f"tiene valores que no son números ({type(e).__name__})"
        try:
            v = float(e)
        except (TypeError, ValueError, OverflowError):
            return None, "tiene valores que no son números"
        if math.isnan(v):
            return None, ("tiene medias nan: ¿alguna muestra quedó vacía (n=0) o elegiste una "
                          "columna sin datos?")
        if math.isinf(v):
            return None, "tiene medias infinitas: revisa el cálculo"
        valores.append(v)
    return valores, None


_REFERENCIAS = {}


def _medias_de_referencia(original):
    """Las medias de n = 100 con mi_semilla = 123 y con las semillas de la clase (se guardan)."""
    import numpy as np

    t = original["tiempo_entrega_min"]
    clave = (len(t), float(t.sum()))
    if clave not in _REFERENCIAS:
        _REFERENCIAS[clave] = (
            np.array([t.sample(n=100, random_state=123 + i).mean() for i in range(1000)]),
            np.array([t.sample(n=100, random_state=i).mean() for i in range(1000)]))
    return _REFERENCIAS[clave]


@_seguro
def revisar_medias(medias=..., *sobran, **otros):
    """Ejercicio 1: las medias de 1000 muestras de 100 pedidos."""
    import numpy as np

    if _sobrantes(sobran, otros, ["medias"]):
        return
    if medias is Ellipsis:
        print("·  medias: todavía tiene ...")
        return
    original = _original()
    if original is None:
        return
    tiempo = original["tiempo_entrega_min"]
    mu = float(tiempo.mean())
    sigma = float(tiempo.std(ddof=0))
    valores, problema = _medias_como_lista(medias, len(original))
    if problema:
        print("✗  medias: " + problema)
        return
    k = len(valores)
    if k == 1:
        print("✗  medias: tiene una sola media: ¿medias.append quedó fuera del for, o medias = [] "
              "quedó dentro? El append va con sangría, dentro del bucle; medias = [], antes")
        return
    if k != 1000:
        if k % 1000 == 0:
            print(f"✗  medias: tiene {k} medias: ¿ejecutaste el bucle {k // 1000} veces sin volver a "
                  "crear la lista? Ejecuta la celda completa, con medias = [] arriba")
        else:
            print(f"✗  medias: tiene {k} medias; se piden 1000, una por muestra: for i in range(1000)")
        return
    v = np.asarray(valores, dtype=float)
    centro, desv = float(v.mean()), float(v.std(ddof=1))
    if desv < 1e-9:
        if abs(centro - mu) < 1e-6:
            print("✗  medias: todas valen μ: cada «muestra» es la tabla entera. Saca muestras de "
                  "100 pedidos")
        elif centro >= 1 and float(centro).is_integer():
            print(f"✗  medias: todas valen {centro:.0f}: eso es cuántos pedidos trae cada muestra "
                  "(.count(), len o .size), no su media. Usa .mean()")
        else:
            print("✗  medias: todas las medias son iguales: las 1000 muestras salieron idénticas. "
                  "¿Dejaste random_state fijo? Usa random_state=mi_semilla + i, que cambia en "
                  "cada vuelta")
        return
    lejos = abs(centro - mu)
    if lejos <= 0.2 and 1.19 <= desv <= 1.34:
        print("✓  medias: 1000 medias de muestras de 100 pedidos")
        print(f"Tus medias: centro {_coma(centro)} min (μ = {_coma(mu)} min) · EE = "
              f"{_coma(desv)} min")
        print(f"La fórmula: σ / √100 = {_coma(sigma)} / 10 = {_coma(sigma / 10)} min")
        de_123, de_clase = _medias_de_referencia(original)
        if np.allclose(v, de_123):
            print("·  Son las medias de mi_semilla = 123: cámbiala por un número de tres cifras "
                  "que elijas tú y vuelve a ejecutar")
        elif np.allclose(v, de_clase):
            print("·  Son las semillas de la clase (random_state=i): usa random_state=mi_semilla "
                  "+ i, con un número de tres cifras que elijas tú")
        print("✓  Cuadra. Responde abajo: con n = 400, ¿cuánto quedaría el EE, y por qué?")
        return
    if 33.4 <= centro <= 34.1 and 0.9 <= desv <= 1.6:
        print("✗  medias: esas son medianas, no medias: el centro queda en unos 33,8 min, el de la "
              "mediana del tiempo. Usa .mean()")
    elif 10.5 <= centro <= 13.5 and desv < 6:
        print("✗  medias: el centro de tus valores es de unos 12 min, la desviación estándar de los "
              "pedidos: ¿usaste .std() en vez de .mean()?")
    elif any(abs(centro / mu - k) <= 0.1 * k for k in (10, 25, 80, 100, 120, 400, 1000)):
        print("✗  medias: tus valores son muchas veces μ: ¿sumaste los tiempos (.sum()) en vez de "
              "promediarlos (.mean())?")
    elif lejos > 1.5:
        print(f"✗  medias: el centro de tus medias es {_coma(centro)}, lejos de los "
              f"{_coma(mu)} min del tiempo de entrega: ¿elegiste otra columna, filtraste los "
              "pedidos o usaste otra cosa en vez de .mean()? Va la media de tiempo_entrega_min, "
              "con muestras de todos los pedidos")
    elif 9 <= desv <= 14:
        print("✗  medias: tus medias varían tanto como los pedidos sueltos: cada muestra trae un "
              "solo pedido (¿n=1?). Saca muestras de 100 pedidos")
    elif lejos > 0.25:
        print(f"✗  medias: el centro de tus medias, {_coma(centro)} min, se corrió de μ "
              f"({_coma(mu)}) más de lo que da el azar: ¿filtraste los pedidos antes de sortear? "
              "Las muestras salen de todos los pedidos: pedidos.sample(...)")
    elif 0.59 <= desv <= 0.66:
        print("✗  medias: varían como las medias de 400 pedidos, el tamaño de la clase: cambia el "
              "400 por el tamaño que pide el ejercicio")
    elif 2.45 <= desv <= 2.72:
        print("✗  medias: varían como las medias de 25 pedidos: tus muestras son más chicas de lo "
              "que pide el ejercicio")
    elif 3.5 <= desv <= 4.25:
        print("✗  medias: varían como las medias de 10 pedidos: tus muestras son más chicas de lo "
              "que pide el ejercicio")
    elif 1.34 < desv <= 1.5:
        print("✗  medias: varían un poco más de lo esperado: tus muestras son algo más chicas que "
              "las que pide el ejercicio (¿n=80?)")
    elif 1.08 <= desv < 1.19:
        print("✗  medias: varían un poco menos de lo esperado: tus muestras son algo más grandes "
              "(¿n=120 o frac=0.01?). frac=0.01 es el 1 % de 12 000, o sea 120 pedidos; el "
              "ejercicio pide un número de pedidos, n=")
    elif desv < 1.19:
        print("✗  medias: varían menos de lo esperado: tus muestras son más grandes que las que "
              "pide el ejercicio. Revisa el n=")
    elif desv > 1.34:
        print("✗  medias: varían más de lo esperado: tus muestras son más chicas que las que pide "
              "el ejercicio. Revisa el n=")
    else:
        print("✗  medias: el centro se corrió de μ más de lo que da el azar: revisa que cada muestra "
              "salga de todos los pedidos (pedidos.sample) y que guardes la media del tiempo")


# ---------------------------------------------------------------------------------------------
# Ejercicio 2 · El intervalo de la semana 20
# ---------------------------------------------------------------------------------------------

def _intervalos_semana(original):
    """El intervalo correcto de la semana 20 y los de los errores probables, en %."""
    import math
    import pandas as pd

    fecha = pd.to_datetime(original["fecha"])
    semana = fecha.dt.isocalendar().week.astype(int)
    cal, buena = _calificados(original)
    p_sem = float(buena.mean())

    def ic(p, n, z=1.96, ee=None):
        e = math.sqrt(p * (1 - p) / n) if ee is None else ee
        return ((p - z * e) * 100, (p + z * e) * 100)

    w = original[semana == 20]
    c = w[w["calificacion"].notna()]
    estrellas = pd.to_numeric(c["calificacion"])
    p, n = float((estrellas >= 4).mean()), len(c)
    todos = float((pd.to_numeric(w["calificacion"]) >= 4).mean())   # el faltante cuenta como False
    w21 = original[semana == 21]
    c21 = pd.to_numeric(w21["calificacion"].dropna())
    e = math.sqrt(p * (1 - p) / n)
    correcto = ic(p, n)
    pistas = [
        (ic(todos, len(w)), "calculaste p̂ sobre todos los pedidos de la semana, y los que no "
                            "calificaron cuentan como «no 4 o 5»: p̂ y n son de los calificados"),
        (ic(p, len(w)), "usaste como n todos los pedidos de la semana; n son los calificados"),
        (ic(p, len(cal)), "usaste como n todos los calificados del semestre (la variable n de "
                          "[proporcion]); n son los calificados de la semana 20"),
        (ic(p, len(original)), "usaste como n los 12 000 pedidos; n son los calificados de la "
                               "semana 20"),
        (ic(p, n, 1.645), "ese es el intervalo de 90 % (z = 1,645); el de 95 % usa 1,96"),
        (ic(p, n, 2.576), "ese es el intervalo de 99 % (z = 2,576); el de 95 % usa 1,96"),
        (ic(p, n, 2), "usaste z = 2; el intervalo de 95 % usa 1,96"),
        (ic(p, n, ee=math.sqrt(p_sem * (1 - p_sem) / n)),
         "en el EE usaste la p̂ del semestre; va la de la semana 20"),
        (ic(float((estrellas >= 3).mean()), n), "contaste 3, 4 o 5 estrellas (>= 3); se pide 4 o 5"),
        (ic(float((estrellas == 5).mean()), n), "contaste solo las de 5 estrellas; se pide 4 o 5 "
                                                "(>= 4)"),
        (ic(1 - p, n), "ese es el intervalo de 1 − p̂, los que NO tienen 4 o 5 estrellas"),
        (ic(p, n, 1), "sumaste y restaste un solo EE; el margen es 1,96 · EE"),
        (ic(float((c21 >= 4).mean()), len(c21)),
         "esa es la semana ISO 21: ¿usaste %W o strftime? La semana va con "
         ".dt.isocalendar().week, como en [semanal]"),
    ]
    angostos = [((p - 1.96 * p * (1 - p) / n) * 100, (p + 1.96 * p * (1 - p) / n) * 100),
                (p * 100 - 1.96 * e, p * 100 + 1.96 * e)]
    return {"correcto": correcto, "pistas": pistas, "angostos": angostos, "p": p * 100, "n": n,
            "p_sem": p_sem * 100}


@_seguro
def revisar_intervalo(*sueltos, inferior=..., superior=..., **otros):
    """Ejercicio 2: el intervalo de 95 % del % de 4 o 5 estrellas de la semana 20, en %."""
    import pandas as pd

    nombres = ["inferior", "superior"]
    if sueltos:
        print("✗  Pasa los valores por nombre, como en la plantilla: "
              "revisar_intervalo(inferior=inferior, superior=superior)")
        return
    if _sobrantes((), otros, nombres):
        return
    original = _original()
    if original is None:
        return
    r = _intervalos_semana(original)
    lo, hi = r["correcto"]
    tol, tol_pista = 0.05, 0.06
    vals = {}
    for nombre, x in [("inferior", inferior), ("superior", superior)]:
        if x is Ellipsis:
            print(f"·  {nombre}: todavía tiene ...")
            continue
        val, problema = _un_numero(x, len(original))
        if problema:
            if isinstance(x, (pd.Series, pd.DataFrame)) and len(x) > 1:
                filas = f"{len(x):,}".replace(",", "\u202f")   # 12 000, con espacio fino
                problema = (f"es una columna o una tabla, con {filas} filas: hace falta un "
                            "solo número, el extremo del intervalo")
            elif problema.startswith("salió nan"):
                problema = ("salió nan: ¿la raíz de un número negativo (si p̂ va en %, el EE usa "
                            "100 − p̂, no 1 − p̂) o una semana sin calificados (revisa el filtro "
                            "semana == 20)?")
            print(f"✗  {nombre}: {problema}")
            continue
        vals[nombre] = val
    if len(vals) < 2:
        return
    a, b = vals["inferior"], vals["superior"]

    def es(par, t, escala=1.0):
        return _cerca(a, par[0] * escala, t * escala) and _cerca(b, par[1] * escala, t * escala)

    if es((lo, hi), tol):
        print("✓  inferior y superior: el intervalo de 95 % de la semana 20")
    elif es((lo, hi), tol, 0.01):
        print("✓  inferior y superior (como proporción)")
        print("·  Diste proporciones (entre 0 y 1); el ejercicio lo pide en %: multiplica por 100")
    elif es((hi, lo), tol) or es((hi, lo), tol, 0.01):
        print("✗  ¿Intercambiaste los dos? inferior es el extremo menor (p̂ − margen) y superior, "
              "el mayor")
        return
    else:
        for par, pista in r["pistas"]:
            if es(par, tol_pista) or es(par, tol_pista, 0.01) or \
                    es((par[1], par[0]), tol_pista) or es((par[1], par[0]), tol_pista, 0.01):
                print(f"✗  {pista}")
                return
        def redondeado(x, ref, dec):
            return round(x, dec) == x and abs(x - ref) <= 0.5 * 10 ** -dec + 1e-9

        if (redondeado(a, lo, 0) and redondeado(b, hi, 0)) or \
                (redondeado(a, lo / 100, 2) and redondeado(b, hi / 100, 2)):
            print("✗  casi: redondeaste demasiado. Entrega los extremos sin redondear, o en % con "
                  "al menos un decimal")
            return
        ancho = b - a
        escala = 0.01 if max(abs(a), abs(b)) <= 1.0 else 1.0
        centro = (a + b) / 2 / escala
        if a == b:
            print("✗  inferior y superior son iguales: falta sumar y restar el margen, 1,96 · EE")
        elif min(a, b) / escala < 0 or max(a, b) / escala > 100:
            print("✗  un porcentaje va de 0 a 100: revisa el cálculo (¿multiplicaste por 100 dos "
                  "veces, o sumaste el margen en otra escala?)")
        elif any(es(par, tol_pista) or es(par, tol_pista, 0.01) for par in r["angostos"]) or \
                (0 < abs(ancho) / escala < 1 and abs(centro - r["p"]) < 0.5):
            print("✗  tu intervalo mide menos de un punto de ancho: revisa la raíz de la fórmula "
                  "y que el margen esté en la misma escala que p̂ (las dos en %, o las dos en "
                  "proporción)")
        elif 1 <= min(a, b) and max(a, b) <= 5:
            print("✗  eso parece un intervalo para la media de las estrellas: la satisfacción no se "
                  "promedia; cuenta qué parte de los calificados tiene 4 o 5 estrellas, en %")
        elif a > b:
            print("✗  inferior es mayor que superior: inferior es p̂ − margen y superior, "
                  "p̂ + margen")
        elif abs(centro - r["p"]) <= 0.3:
            print("✗  el centro está bien (la p̂ de la semana 20), pero el margen no: es 1,96 · EE, "
                  "con EE = √(p̂ (1 − p̂) / n)")
        elif abs(centro - r["p_sem"]) <= 0.3:
            print("✗  ese intervalo está centrado en la cifra del semestre; se pide el de la semana "
                  "20: filtra semana == 20")
        else:
            print("✗  no cuadra: revisa que uses los calificados de la semana 20 y el % de 4 o 5 "
                  "estrellas")
        return
    print(f"Semana 20: p̂ = {_coma(r['p'])} % con n = {r['n']} calificados · intervalo "
          f"[{_coma(lo)}; {_coma(hi)}] % · semestre: {_coma(r['p_sem'])} %")
    print("✓  Cuadra. Responde abajo: ¿fue la semana 20 peor que el semestre?")


# ---------------------------------------------------------------------------------------------
# Ejercicio 3 (opcional) · ¿Cuántos calificados necesita Bucaramanga para ±5 puntos?
# ---------------------------------------------------------------------------------------------

@_seguro
def revisar_tamano(*sueltos, n=..., **otros):
    """Ejercicio 3: el tamaño de muestra de Bucaramanga para un margen de ±5 puntos."""
    import math
    import pandas as pd

    if sueltos:
        print("✗  Pasa el valor por nombre, como en la plantilla: revisar_tamano(n=n_necesario)")
        return
    if _sobrantes((), otros, ["n"]):
        return
    if n is Ellipsis:
        print("·  n: todavía tiene ...")
        return
    original = _original()
    if original is None:
        return
    val, problema = _un_numero(n, len(original))
    if problema:
        if isinstance(n, (pd.Series, pd.DataFrame)) and len(n) > 1:
            problema = "es una columna o una tabla; hace falta un solo número, el tamaño"
        print(f"✗  n: {problema}")
        return
    cal, buena = _calificados(original)
    en_buc = cal["ciudad"] == "Bucaramanga"
    p = float(buena[en_buc].mean())
    p_todos = float((pd.to_numeric(original["calificacion"]) >= 4)[
        original["ciudad"] == "Bucaramanga"].mean())
    p_nac = float(buena.mean())
    z2 = 1.96 ** 2

    def tam(q, e=0.05, z=1.96):
        return z ** 2 * q * (1 - q) / e ** 2

    exacto = tam(p)
    prudente = tam(0.5)

    def cerca_de(x):   # el valor exacto o redondeado (los muy pequeños, solo el exacto)
        if x < 1:
            return abs(val - x) <= 0.05 * abs(x)
        return x - 0.02 - 1e-9 <= val <= math.ceil(x) + 1e-9 or abs(val - x) <= 0.002 * abs(x)

    if val <= 0:
        print("✗  n: un tamaño de muestra es un número positivo: revisa el cálculo (si p̂ va "
              "en %, el complemento es 100 − p̂, no 1 − p̂)")
        return

    if exacto - 0.02 <= val <= math.ceil(exacto) + 1e-9:
        print("✓  n: el tamaño para ±5 puntos en Bucaramanga")
        if val < math.ceil(exacto):
            print("·  Un tamaño de muestra se redondea siempre hacia arriba: con uno menos, el "
                  "margen pasaría de ±5")
        mediana = cal[en_buc].groupby(
            pd.to_datetime(cal.loc[en_buc, "fecha"]).dt.isocalendar().week).size().median()
        print(f"Bucaramanga: p̂ = {_coma(p * 100, 1)} % de 4 o 5 estrellas · unos {mediana:.0f} "
              "calificados por semana")
        print("✓  Cuadra. Responde abajo: ¿cuántas semanas de Bucaramanga son? ¿Por semana o por "
              "mes?")
        return
    if prudente - 0.06 <= val <= math.ceil(prudente) + 1e-9:   # de 384,1 a 385
        print("✓  n: con p = 0,5, el tamaño más prudente: sirve para cualquier p̂")
        print("·  Es la opción prudente cuando no se conoce p̂. Con la p̂ de Bucaramanga, que ya "
              "conoces, hacen falta bastantes menos: pruébalo y compara")
        return
    if math.floor(exacto) <= val < exacto - 0.02:
        abajo = math.floor(val)
        margen = 1.96 * math.sqrt(p * (1 - p) / abajo) * 100
        print(f"✗  n: con {abajo} calificados el margen sería de ±{_coma(margen)} puntos, más de "
              "±5: un tamaño de muestra se redondea siempre hacia arriba")
        return
    if math.floor(prudente) <= val < prudente - 0.06:
        print("✗  n: ese es el tamaño con p = 0,5, pero redondeado hacia abajo: un tamaño de "
              "muestra se redondea siempre hacia arriba (con uno menos, el margen pasa de ±5)")
        return
    pistas = [
        (tam(p_todos), "calculaste p̂ sobre todos los pedidos de Bucaramanga, y los que no "
                       "calificaron cuentan como «no 4 o 5»: p̂ es entre los calificados"),
        (tam(p_nac), "esa es la p̂ nacional; se pide la de Bucaramanga"),
        (z2 * p * (1 - p) / 5 ** 2, "con p̂ en proporción, E también va en proporción: 0.05, no 5"),
        (z2 * (p * 100) * (100 - p * 100) / 0.05 ** 2, "con p̂ en %, E también va en %: 5, no 0.05"),
        (1.96 * p * (1 - p) / 0.05 ** 2, "el 1,96 va al cuadrado: 1.96 ** 2"),
        (z2 * p * (1 - p) / 0.05, "E va al cuadrado: 0.05 ** 2"),
        (tam(p, 0.025), "usaste la mitad de E: el margen es lo que se suma y se resta (±5), no el "
                        "ancho del intervalo"),
        (tam(p, 0.05, 2), "usaste z = 2; el 95 % usa 1,96"),
        (tam(p, 0.05, 1.645), "usaste z = 1,645, que es el de 90 %; el de 95 % usa 1,96"),
        (tam(p, 0.05, 2.576), "usaste z = 2,576, que es el de 99 %; el de 95 % usa 1,96"),
        (math.sqrt(exacto), "sacaste la raíz: la fórmula del tamaño no lleva raíz"),
    ]
    for x, pista in pistas:
        if cerca_de(x):
            print(f"✗  n: {pista}")
            return
    print("✗  n: no cuadra: revisa p̂ (4 o 5 estrellas entre los calificados de Bucaramanga) "
          "y E (0.05 si p̂ va en proporción)")
