# Fuente ÚNICA del código de la Sesión 4. De aquí salen:
#   - el notebook para Colab                    (notebook.py genera 4)
#   - las salidas y las gráficas que muestran las diapositivas
#                                               (notebook.py ejecuta 4 → salidas_sesion4.json y
#                                                fuente/diapositivas/recursos/s4/<id>.svg)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py, ayudas.py y
#               ayudas_sesion4.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar
#   precalculo  cifras que las diapositivas citan en el texto: se ejecuta, NO va al notebook

# %% [markdown]
# # Sesión 4 · Lo que se sale de lo normal
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este cuaderno (*notebook*) acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-4-lo-que-se-sale-de-lo-normal.html).
# Cada celda lleva entre corchetes el mismo identificador que el código proyectado, así que puedes seguir
# la clase celda a celda. La portada del curso está en https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/
# y el enunciado del proyecto final, el tablero, en
# [su página](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/proyecto-tablero.html).
#
# 1. **Archivo → Guardar una copia en Drive** para que tus cambios no se pierdan.
# 2. Ejecuta las celdas **en orden** con **Mayús + Enter**. Varias usan resultados de las anteriores.
#    Si Colab avisa que el cuaderno no es de Google, elige **Ejecutar de todos modos**.
# 3. Si Colab se reinicia o una celda falla al repetirla, haz clic en esa celda y usa
#    **Entorno de ejecución → Ejecutar anteriores**.
# 4. La primera celda crea los datos del caso *Tingua Domicilios S.A.S.*, una empresa **ficticia**
#    (sus datos se inventan con una semilla fija y no corresponden a personas ni a empresas reales),
#    y les da a las gráficas los colores del curso.

# %% datos generador
# Crea datos/pedidos.csv: los mismos 12 000 pedidos de las sesiones 1 a 3
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Los datos, con sus escalas
#
# Cargamos los pedidos y declaramos las escalas, como en las sesiones anteriores.

# %% cargar
import pandas as pd
import matplotlib.pyplot as plt

pedidos = pd.read_csv("datos/pedidos.csv")
# Las escalas que declaramos en la sesión 1
franjas = ["Mañana", "Almuerzo", "Tarde", "Noche"]
pedidos["franja"] = pd.Categorical(
    pedidos["franja"], categories=franjas, ordered=True)
pedidos["estrato"] = pd.Categorical(
    pedidos["estrato"], categories=[1, 2, 3, 4, 5, 6], ordered=True)
pedidos["calificacion"] = pd.Categorical(
    pedidos["calificacion"], categories=[1, 2, 3, 4, 5], ordered=True)
pedidos.shape

# %% [markdown]
# ### Diccionario de datos (el mismo de la sesión 1)
#
# | Columna | Qué registra | Valores o unidad |
# |---|---|---|
# | `id_pedido` | Código del pedido | P00001, P00002… |
# | `fecha` | Día del pedido | del 1 de enero al 30 de junio de 2026 |
# | `franja` | Momento del día en que se pidió | Mañana, Almuerzo, Tarde, Noche |
# | `ciudad` | Ciudad de entrega | Bogotá, Medellín, Cali, Barranquilla, Bucaramanga |
# | `categoria` | Tipo de comercio que despacha | Restaurante, Mercado, Farmacia, Mascotas, Floristería |
# | `n_productos` | Unidades pedidas | conteo |
# | `valor_pedido` | Valor de los productos, sin domicilio ni propina | pesos (COP) |
# | `medio_pago` | Cómo se pagó | Efectivo, Tarjeta, Billetera digital |
# | `estrato` | Estrato de la **dirección de entrega** (lo asigna el municipio a la vivienda) | 1 a 6 |
# | `suscriptor` | Si quien pide paga la suscripción de Tingua | Sí / No |
# | `distancia_km` | Distancia por vía del comercio a la dirección | kilómetros; la app registra hasta 14: una ruta más larga queda como 14 |
# | `lluvia` | Si llovía en la zona durante la entrega | Sí / No |
# | `temperatura_c` | Temperatura en la zona al momento de la entrega | grados Celsius |
# | `tiempo_entrega_min` | Minutos desde que se confirma el pedido hasta que llega | minutos |
# | `calificacion` | Estrellas que dio quien pidió; vacía si no calificó | 1 a 5 |

# %% [markdown]
# ## 2 · Los atípicos: ¿qué pedidos se salen de lo normal?
#
# Un **atípico** es un dato que queda lejos de los demás. Ante cada candidato hacemos dos preguntas:
#
# - **¿Por qué está lejos?** Puede ser un error, un valor real y raro, o un dato censurado.
# - **¿Lejos respecto a qué?** De todos los pedidos o de los de su grupo.
#
# ### La regla de 1,5 RIC (las vallas de Tukey)
#
# Las **vallas** se ponen a 1,5 RIC de la caja: $Q_1 - 1{,}5\,\text{RIC}$ por debajo y
# $Q_3 + 1{,}5\,\text{RIC}$ por encima. Un pedido queda **fuera** si está **estrictamente** más allá
# de una valla: menor que la inferior o mayor que la superior.

# %% vallas
tiempo = pedidos["tiempo_entrega_min"]
q1, q3 = tiempo.quantile(0.25), tiempo.quantile(0.75)
ric = q3 - q1
valla_inf = q1 - 1.5 * ric
valla_sup = q3 + 1.5 * ric
print(f"Vallas: {valla_inf:.2f} y {valla_sup:.2f} min")
# «Fuera» es estrictamente más allá: < y >, no <= ni >=
print("Por debajo:", (tiempo < valla_inf).sum(), "pedidos")
print("Por encima:", (tiempo > valla_sup).sum(), "pedidos")

# %% [markdown]
# Con 3 RIC en lugar de 1,5, la valla marca solo los **extremos**.

# %% extremos
valla_ext = q3 + 3 * ric
print(f"Valla de 3 RIC: {valla_ext:.1f} min ·",
      (tiempo > valla_ext).sum(), "pedidos por encima")

# %% [markdown]
# ### Las vallas en el diagrama de caja
#
# El diagrama de caja de la sesión 3 usa esta misma regla. La **caja** va de $Q_1$ a $Q_3$ y la línea
# es la mediana. Los **bigotes** no llegan hasta la valla, sino hasta el último pedido que **no** la
# pasa: solo coinciden con ella si un pedido vale justo la valla. Un bigote llega al mínimo o al
# máximo solo del lado en que no hay puntos sueltos. Los **puntos sueltos** son los que pasan la
# valla: los candidatos. Varios pedidos con el mismo valor se dibujan como un solo punto.

# %% caja_tiempo
estilo_caja = dict(          # los colores de la caja, para todas las cajas
    widths=0.5, patch_artist=True,
    boxprops={"facecolor": "#EFE3F2", "edgecolor": "#8A2E9E"},
    medianprops={"color": "#3A0F47", "linewidth": 2.5},
    whiskerprops={"color": "#8A2E9E"},
    capprops={"color": "#8A2E9E"},
    flierprops={"marker": ".", "markersize": 4,
                "markerfacecolor": "#8A2E9E", "markeredgecolor": "none"})
fig, ax = plt.subplots(figsize=(5.2, 4.2))
caja = ax.boxplot(tiempo, **estilo_caja)
for valla in [valla_inf, valla_sup]:       # las dos vallas, con su valor
    ax.axhline(valla, color="#F46201", linewidth=2, linestyle="--")
    ax.text(1.48, valla + 2, f"valla: {valla:.2f}", ha="right")
ax.set_xticks([1], ["Todos los pedidos"])
ax.set_ylabel("Minutos")
# Los bigotes llegan al último pedido que no pasa cada valla
bigotes = [linea.get_ydata()[1] for linea in caja["whiskers"]]
print(f"Bigotes: de {bigotes[0]:.1f} a {bigotes[1]:.1f} min")
sueltos = caja["fliers"][0].get_ydata()
print("Fuera de los bigotes:", len(sueltos), "pedidos en",
      pd.Series(sueltos).nunique(), "puntos distintos")
ax.set_title(f"{len(sueltos)} pedidos pasan las vallas")   # un título que afirma
plt.show()

# %% [markdown]
# ### El puntaje z
#
# El **puntaje z** dice a cuántas desviaciones estándar de la media está un pedido:
#
# $$z = \frac{x - \bar{x}}{s}$$
#
# Por convención, se marca un pedido si $|z| > 3$: si está a más de tres desviaciones de la media,
# por encima o por debajo. Aquí z solo mide distancias; su relación con la distribución normal llega
# en la sesión 6.

# %% puntaje_z
media, s = tiempo.mean(), tiempo.std()
z = (tiempo - media) / s           # a cuántas desviaciones de la media
print("|z| > 3:", (z.abs() > 3).sum(), "pedidos")
marcados = tiempo[z.abs() > 3]
print("¿Todos por encima de la valla?", bool((marcados > valla_sup).all()))
print(f"Media - 3s = {media - 3 * s:.1f} min")   # ningún tiempo es negativo

# %% [markdown]
# ### ¿Por qué z marca menos? El enmascaramiento
#
# z usa la media y la desviación, y los propios candidatos las inflan: así se esconden.

# %% enmascaramiento
fuera = (tiempo < valla_inf) | (tiempo > valla_sup)
print(f"s con todos los pedidos: {s:.2f} min")
print(f"s sin los {fuera.sum()} candidatos: {tiempo[~fuera].std():.2f} min")

# %% [markdown]
# ### Las dos reglas en el histograma
#
# La franja sombreada va de la valla superior a $z = 3$: son los pedidos que la valla marca y z no.

# %% histograma_vallas
z3 = media + 3 * s                 # el tiempo donde z vale 3
entre = ((tiempo > valla_sup) & (tiempo <= z3)).sum()   # la valla sí, z no
mas_alla = (tiempo > z3).sum()                          # las dos
ax = tiempo.plot.hist(bins=range(0, 210, 5), color="#8A2E9E", alpha=0.45,
                      edgecolor="white")
ax.axvspan(valla_sup, z3, color="#F46201", alpha=0.12)
ax.axvline(valla_sup, color="#F46201", linewidth=2.5, linestyle="--")
ax.axvline(z3, color="#3A0F47", linewidth=2.5, linestyle=":")
alto = ax.get_ylim()[1]
ax.text(valla_sup - 1.5, alto * 0.95, f"valla\n{valla_sup:.2f}",
        ha="right", va="top")
ax.text(z3 + 1.5, alto * 0.95, f"z = 3\n{z3:.1f}", ha="left", va="top")
ax.text((valla_sup + z3) / 2, alto * 0.5, str(entre), ha="center",
        fontweight="bold", color="#B84A00")
ax.text(z3 + 2, alto * 0.35,
        f"{mas_alla} más allá,\nhasta {tiempo.max():.1f} min", ha="left")
ax.set_xlim(0, 140)   # la cola sigue más allá de 200 min
ax.set_title(f"La valla superior marca {entre + mas_alla}; z = 3, solo {mas_alla}")
ax.set_xlabel("Minutos")
ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ### ¿Son raros todos los que marca la regla?
#
# En `n_productos` la regla marca muchos pedidos. Antes de creerle, miremos la gráfica: a la
# izquierda, la caja; en el centro, los pedidos de 1 a 17 productos, con los de fuera en un color
# más claro; a la derecha, ampliados los de más de 14 productos.

# %% productos_barras
productos = pedidos["n_productos"]
p1, p3 = productos.quantile(0.25), productos.quantile(0.75)
valla_p = p3 + 1.5 * (p3 - p1)
print("Valla superior:", valla_p, "· fuera:", (productos > valla_p).sum(),
      "· justo en la valla:", (productos == valla_p).sum())
conteo = productos.value_counts().sort_index()
fig, (caja_p, izq, der) = plt.subplots(1, 3, width_ratios=[1, 3, 2],
                                       figsize=(8.4, 3.6))
sueltos = caja_p.boxplot(productos, **estilo_caja)["fliers"][0].get_ydata()
print("En la caja:", len(sueltos), "pedidos en",
      pd.Series(sueltos).nunique(), "puntos distintos")
caja_p.set_xticks([1], ["Caja"])
caja_p.set_title("La caja", fontsize=12)
caja_p.set_ylabel("Productos")
fuera_p = conteo.index > valla_p       # «fuera» es estrictamente más de 6
izq.axvline(valla_p, color="#F46201", linewidth=2.5, linestyle="--",
            zorder=0, label=f"Valla superior: {valla_p:.0f}")   # detrás
izq.bar(conteo.index[~fuera_p], conteo.values[~fuera_p], color="#8A2E9E")
izq.bar(conteo.index[fuera_p], conteo.values[fuera_p], color="#8A2E9E",
        alpha=0.45, label=f"Fuera: más de {valla_p:.0f}")
izq.set_xlim(0, 18)                    # lo de más de 14, en la ampliación
izq.legend()
izq.set_title(f"La regla marca {(productos > valla_p).sum()} pedidos")
izq.set_xlabel("Productos")
izq.set_ylabel("Pedidos")
grandes = conteo[conteo.index > 14]
corp = grandes.index >= 20             # el grupo aparte
der.bar(grandes.index[~corp], grandes.values[~corp], color="#8A2E9E",
        alpha=0.45)                    # fuera, como en el centro
der.bar(grandes.index[corp], grandes.values[corp], color="#3A0F47")
der.text(32, 4.6, f"{(productos >= 20).sum()} pedidos\nde 20 a {productos.max()}",
         ha="center")
der.set_title("Ampliado: más de 14", fontsize=12)
der.set_xlabel("Productos")
plt.show()

# %% [markdown]
# ### Los pedidos lentos son dos grupos
#
# Los 240 pedidos por encima de la valla superior no son todos iguales. Partámoslos en
# **moderados** (hasta la valla de 3 RIC) y **extremos** (más allá).

# %% lentos
lentos = pedidos[tiempo > valla_sup].copy()
lentos["grupo"] = pd.cut(lentos["tiempo_entrega_min"],
                         bins=[valla_sup, valla_ext, 250],
                         labels=["moderado", "extremo"])
lentos["llueve"] = (lentos["lluvia"] == "Sí") * 100      # 100 o 0
lentos["bogota"] = (lentos["ciudad"] == "Bogotá") * 100
resumen = lentos.groupby("grupo", observed=True).agg(
    pedidos=("id_pedido", "count"),
    km_mediana=("distancia_km", "median"),
    pct_lluvia=("llueve", "mean"),
    pct_bogota=("bogota", "mean"))
resumen.round(2)

# %% [markdown]
# ¿Y la calificación de las demoras extremas? Contamos estrellas, sin promediarlas.

# %% extremos_calificacion
extremos = pedidos[tiempo > valla_ext]
calificados = extremos["calificacion"].dropna()
print("Extremos calificados:", len(calificados),
      "· con 1 estrella:", (calificados == 1).sum())
# El pedido más lento de todos (la pregunta de la sesión 1)
columnas = ["id_pedido", "ciudad", "distancia_km", "lluvia",
            "tiempo_entrega_min", "calificacion"]
pedidos.loc[tiempo.idxmax(), columnas]

# %% [markdown]
# ### ¿Atípico respecto a qué?
#
# La valla se puede calcular con todos los pedidos (la valla **global**) o con los de cada ciudad
# (la valla **propia**). Un mismo pedido puede ser atípico en su ciudad y normal en el total.

# %% valla_ciudad
ciudad = pedidos["ciudad"]
grupos = tiempo.groupby(ciudad)
q1c, q3c = grupos.quantile(0.25), grupos.quantile(0.75)
valla_c = q3c + 1.5 * (q3c - q1c)            # una valla por ciudad
lento_global = tiempo > valla_sup
lento_propia = tiempo > ciudad.map(valla_c)  # la valla de su ciudad
pd.DataFrame({
    "valla propia": valla_c,
    "lentos (global)": lento_global.groupby(ciudad).sum(),
    "lentos (propia)": lento_propia.groupby(ciudad).sum(),
}).round(2)

# %% [markdown]
# Un pedido de 55 min en Barranquilla pasa la valla de su ciudad, pero no la global. ¿Cuántos hay así?

# %% solo_ciudad
# Atípicos en Barranquilla con la valla propia, pero no con la global
solo_propia = (ciudad == "Barranquilla") & lento_propia & ~lento_global
print("Barranquilla, atípicos solo en su ciudad:", solo_propia.sum())

# %% [markdown]
# Barranquilla y Bucaramanga tenían casi el mismo cuerpo (sesión 3). ¿Cuántos pedidos pasan la valla
# de su ciudad, y cuánto se alejan de ella?

# %% alejan
for nombre in ["Barranquilla", "Bucaramanga"]:
    x = tiempo[ciudad == nombre]
    exceso = x[x > valla_c[nombre]] - valla_c[nombre]   # cuánto se pasa
    print(f"{nombre}: {len(exceso)} pasan su valla;",
          f"se alejan {exceso.median():.1f} min en mediana",
          f"y {exceso.max():.1f} el más lejano")

# %% [markdown]
# Las cajas por ciudad de la sesión 3 usan la valla **propia** de cada ciudad. Encima va la valla
# **global**: la misma línea para todas.

# %% cajas_ciudad
orden = valla_c.sort_values().index     # de menor a mayor valla
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.boxplot([tiempo[ciudad == c] for c in orden], **estilo_caja)
ax.axhline(valla_sup, color="#F46201", linewidth=2, linestyle="--")
ax.set_xticks(range(1, len(orden) + 1), orden)
# Sin leyenda: taparía los puntos más altos (el de 200.9 min)
ax.set_title(f"Por ciudad; en naranja, la valla global ({valla_sup:.2f} min)")
ax.set_ylabel("Minutos")
plt.show()

# %% [markdown]
# ### El tope de 14 km: un dato censurado
#
# El diccionario de datos lo dice: la app registra hasta 14 km, y una ruta más larga queda como 14.
# Un «14» significa «14 o más»: es un **dato censurado**.

# %% tope
distancia = pedidos["distancia_km"]
distancia.value_counts().sort_index().tail()

# %% distancia_tope
lejos = distancia[distancia > 8]
conteo = lejos.value_counts().sort_index()
fig, (caja_d, ax) = plt.subplots(1, 2, width_ratios=[1, 4])
sueltos = caja_d.boxplot(distancia, **estilo_caja)["fliers"][0].get_ydata()
print("En la caja:", len(sueltos), "pedidos en",
      pd.Series(sueltos).nunique(), "puntos distintos")
caja_d.set_xticks([1], ["Caja"])
caja_d.set_title("La caja", fontsize=12)
caja_d.set_ylabel("Kilómetros")
ax.bar(conteo.index, conteo.values, width=0.08, color="#8A2E9E",
       label="Pedidos a cada distancia")
ax.bar([14], [conteo[14.0]], width=0.08, color="#F46201",
       label="Exactamente 14.0 km")
ax.legend()
ax.set_title(f"{conteo[14.0]} pedidos en el tope de 14 km")
ax.set_xlabel("Kilómetros")
ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ### Qué hacer con cada candidato
#
# | Pregunta | Si la respuesta es sí | Qué se hace |
# |---|---|---|
# | ¿Es imposible o choca con otras columnas? | Es un **error** (seguro o probable) | Se corrige en la fuente o se marca como faltante |
# | ¿Está en el tope del registro? | Es un dato **censurado** | Se marca; no se borra ni se trata como exacto |
# | ¿Es posible, coherente y no está en un tope? | Es un atípico **real** | Se conserva, se investiga y se informa con medidas robustas |
#
# Un valor posible también puede ser un error (un 20,9 escrito 200,9): por eso se mira si es
# coherente con las demás columnas. Primero, ¿hay errores evidentes en Tingua?

# %% errores
print("Filas repetidas:", pedidos.duplicated().sum())
print("Códigos repetidos:", pedidos["id_pedido"].duplicated().sum())
cantidades = ["n_productos", "valor_pedido", "distancia_km",
              "tiempo_entrega_min"]
print("Valores ≤ 0:", (pedidos[cantidades] <= 0).sum().sum())

# %% [markdown]
# ¿Y si borramos los candidatos y recalculamos las vallas?

# %% cadena
resto = tiempo[~fuera]                 # sin los candidatos de la valla
a, b = resto.quantile(0.25), resto.quantile(0.75)
nuevos = (resto < a - 1.5 * (b - a)) | (resto > b + 1.5 * (b - a))
print("Borrados:", fuera.sum(), "· atípicos nuevos:", nuevos.sum())

# %% [markdown]
# ## 3 · Exploración multidimensional
#
# Un **cubo** de datos cruza **dimensiones** (por dónde se corta: ciudad, franja, lluvia) con
# **medidas** (lo que se resume: tiempo, valor). Sobre él se **filtra** (se deja una parte), se
# **desglosa** (se baja a más detalle) y se **pivota** (se cambia qué va en filas y en columnas). Es
# lo que hacen las tablas dinámicas de Excel, Power BI y Looker Studio.
#
# ### La tabla dinámica
#
# `pd.pivot_table` resume una medida (`values`) por dos dimensiones (`index` y `columns`) con la
# función que se le diga (`aggfunc`). `margins=True` añade los totales.

# %% dinamica
tabla = pd.pivot_table(pedidos, values="tiempo_entrega_min",
                       index="ciudad", columns="lluvia",
                       aggfunc="median", observed=True,
                       margins=True, margins_name="Total")
tabla.round(1)

# %% efecto_lluvia
# Cuántos minutos suma la lluvia, ciudad por ciudad (con la mediana)
(tabla["Sí"] - tabla["No"]).round(1)

# %% [markdown]
# En el total, Bogotá tarda 9,4 min más que Barranquilla; sin lluvia, 8,1. ¿Por qué se acorta la
# diferencia? Porque la columna «Total» mezcla pedidos con y sin lluvia, y en Bogotá llueve en más
# pedidos:

# %% composicion
con_lluvia = (pedidos["lluvia"] == "Sí").groupby(ciudad).mean()
(con_lluvia * 100).round(1)

# %% [markdown]
# ### Desglosar: los lentos, por distancia y lluvia
#
# Partimos la distancia en tramos con cortes explícitos. El 4,4 es $Q_3$ de la distancia. El 7,7 es
# su valla superior, y 26 pedidos la tienen exacta: con `right=True` quedan en el tramo del medio, no
# entre los lejanos. Un pedido es **lento** si pasa la valla de 59,15 min; la media de una columna de
# 100 y 0 es el porcentaje.

# %% desglose
tramo = pd.cut(distancia, bins=[0, 4.4, 7.7, 14], right=True,
               labels=["hasta 4,4 km", "4,4 a 7,7 km", "más de 7,7 km"])
lento = (tiempo > valla_sup) * 100     # 100 si es atípico lento, 0 si no
pd.pivot_table(pedidos.assign(tramo=tramo, lento=lento),
               values="lento", index="tramo", columns="lluvia",
               aggfunc="mean", observed=True).round(1)

# %% [markdown]
# ## 4 · Para tu tablero
#
# El proyecto final es un tablero semanal para la gerencia (el
# [enunciado](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/proyecto-tablero.html)
# tiene todos los detalles). El primer paso es agrupar por **semana ISO**, que va de lunes a domingo,
# y marcar las semanas que no están completas. Esta celda no tiene verificador: los indicadores y las
# gráficas son el trabajo de tu pareja.

# %% semanas
fecha = pd.to_datetime(pedidos["fecha"])
# Semana ISO: de lunes a domingo
semana = fecha.dt.isocalendar().week.rename("semana")
por_semana = pd.DataFrame({
    "pedidos": pedidos.groupby(semana).size(),
    "dias": fecha.groupby(semana).nunique(),   # días con pedidos
})
por_semana["completa"] = por_semana["dias"] == 7
print("Semanas:", len(por_semana))
por_semana[~por_semana["completa"]]          # las incompletas

# %% [markdown]
# ---
# # Práctica guiada
#
# Tres ejercicios; el tercero es **opcional**, para la casa. Cada ejercicio termina con un verificador
# (la caja del ejercicio 1 no lo tiene) que dice qué está bien y, en lo demás, te da una pista sin
# darte la respuesta. Reemplaza cada `...` y ejecuta; puedes repetir la celda las veces que quieras.
# Las respuestas escritas van al final, en «Tus respuestas»: esas no las revisa ningún verificador.
#
# ## Ejercicio 1 · Los atípicos del valor del pedido
#
# Calcula las vallas de 1,5 RIC de `valor_pedido` y cuenta los pedidos **estrictamente** fuera de
# ellas (`n_ric`). Después cuenta los que tienen $|z| > 3$ (`n_z`). Deja como está la llamada final a
# `revisar_atipicos`: entrega cada valor con su nombre. Pista: las celdas [vallas] y [puntaje_z].
#
# Después responde abajo: ¿por qué z marca menos pedidos que las vallas?

# %% ej1 plantilla
valor = pedidos["valor_pedido"]
valla_inferior = ...   # Q1 - 1.5 RIC
valla_superior = ...   # Q3 + 1.5 RIC
n_ric = ...            # pedidos estrictamente fuera de las vallas
n_z = ...              # pedidos con |z| > 3
revisar_atipicos(valla_inferior=valla_inferior,
                 valla_superior=valla_superior, n_ric=n_ric, n_z=n_z)

# %% ej1_solucion solucion
valor = pedidos["valor_pedido"]
v1, v3 = valor.quantile(0.25), valor.quantile(0.75)
valla_inferior = v1 - 1.5 * (v3 - v1)
valla_superior = v3 + 1.5 * (v3 - v1)
n_ric = ((valor < valla_inferior) | (valor > valla_superior)).sum()
z_valor = (valor - valor.mean()) / valor.std()
n_z = (z_valor.abs() > 3).sum()
revisar_atipicos(valla_inferior=valla_inferior,
                 valla_superior=valla_superior, n_ric=n_ric, n_z=n_z)

# %% [markdown]
# Ahora dibuja la caja de `valor` con una línea en `valla_superior`. Este paso **no** tiene verificador.
# Pista: la celda [caja_tiempo], incluidas las líneas que imprimen los bigotes. Responde abajo: ¿dónde termina el bigote superior? ¿Coincide con la
# valla? ¿Por qué el pedido que vale justo la valla no es un punto suelto?

# %% ej1_caja plantilla
# Dibuja aquí la caja de valor, con una línea en valla_superior

# %% ej1_caja_solucion solucion
fig, ax = plt.subplots()
caja = ax.boxplot(valor / 1000, **estilo_caja)      # en miles de pesos
ax.axhline(valla_superior / 1000, color="#F46201", linewidth=2, linestyle="--",
           label=f"Valla superior: {valla_superior / 1000:.1f}")
ax.set_xticks([1], ["Todos los pedidos"])
ax.legend()
ax.set_title("Valor del pedido")
ax.set_ylabel("Miles de pesos")
bigotes = [linea.get_ydata()[1] for linea in caja["whiskers"]]
print(f"Bigotes: de {bigotes[0]:.1f} a {bigotes[1]:.1f} miles de pesos")
plt.show()

# %% [markdown]
# ## Ejercicio 2 · Una tabla dinámica: ciudad por franja
#
# Construye la tabla dinámica de la **mediana** del tiempo de entrega, con las ciudades en las filas y
# las franjas en las columnas. Pista: la celda [dinamica]. Si pandas responde «agg function failed»,
# revisa `values=`: sin él, intenta resumir todas las columnas.
#
# Después responde abajo: ¿la franja más lenta es la misma en todas las ciudades?

# %% ej2 plantilla
tabla_franja = ...   # pd.pivot_table(pedidos, values=..., index=..., columns=...,
                     #                aggfunc=..., observed=True)
revisar_dinamica(tabla_franja)

# %% ej2_solucion solucion
tabla_franja = pd.pivot_table(pedidos, values="tiempo_entrega_min",
                              index="ciudad", columns="franja",
                              aggfunc="median", observed=True)
revisar_dinamica(tabla_franja)

# %% [markdown]
# ## Ejercicio 3 (opcional) · ¿Y si el tope escondiera rutas de 30 km?
#
# Los 20 pedidos con 14 km son «14 o más». Supón que en realidad eran de 30 km: haz una **copia** de
# `distancia_km` con 30 en lugar de 14, sin cambiar `pedidos`, y calcula su mediana y su media. Pista:
# `replace` cambia un valor por otro y devuelve una copia. Deja la última línea como está.
#
# Después responde abajo: ¿cambia la mediana? ¿Y la media? ¿Qué te dice eso de un dato censurado?

# %% ej3 plantilla
distancia_30 = ...   # una copia de distancia_km con 30 en lugar de 14
mediana_30 = ...     # su mediana
media_30 = ...       # su media
revisar_tope(mediana_30=mediana_30, media_30=media_30)

# %% ej3_solucion solucion
distancia_30 = pedidos["distancia_km"].replace(14, 30)
mediana_30 = distancia_30.median()
media_30 = distancia_30.mean()
revisar_tope(mediana_30=mediana_30, media_30=media_30)

# %% [markdown]
# ### Tus respuestas
#
# *Doble clic para escribir aquí.*
#
# 1. Ejercicio 1: z marca menos pedidos que las vallas porque …; el bigote superior termina en …, que
#    (no) coincide con la valla porque …; el pedido que vale justo la valla no es un punto suelto
#    porque …
# 2. Ejercicio 2: la franja más lenta es … en …; (no) es la misma en todas porque …
# 3. Ejercicio 3: la mediana …; la media …; de un dato censurado aprendo que …
# 4. Autoevaluación. Para cada pedido, di su causa (error, real o censurado) y si es atípico respecto
#    a todos, solo respecto a su grupo o a ninguno:
#    - un pedido de 62 min en Bogotá (la valla de Bogotá es de 63,40 min): …
#    - una ruta registrada con 14,0 km: …
#    - un pedido de farmacia de 120 000 pesos (la valla de las farmacias es de 103 000; la de todos
#      los pedidos, de 155 600): …
#    - un tiempo de entrega de −5 min: …
#    - un pedido de una empresa con 44 productos: …

# %% cifras precalculo
# Cifras que las diapositivas, sus notas y la página del proyecto citan (no va al notebook)
datos = pd.read_csv("datos/pedidos.csv")
n = len(datos)
t = datos["tiempo_entrega_min"]
tq1, tq3 = t.quantile(0.25), t.quantile(0.75)
tric = tq3 - tq1
vi, vs, ve = tq1 - 1.5 * tric, tq3 + 1.5 * tric, tq3 + 3 * tric
print(f"tiempo: n {n}; Q1 {tq1:.1f}, Q3 {tq3:.1f}, RIC {tric:.1f}; 1,5 RIC = {1.5 * tric:.2f}; "
      f"vallas {vi:.2f} y {vs:.2f}; 3 RIC = {3 * tric:.1f}, valla de extremos {ve:.1f}")
fuera_t = (t < vi) | (t > vs)
print(f"fuera: por debajo {(t < vi).sum()}, por encima {(t > vs).sum()}, total {fuera_t.sum()} "
      f"({fuera_t.mean() * 100:.1f} %); exactamente en una valla {((t == vi) | (t == vs)).sum()}; "
      f"con <= y >= {((t <= vi) | (t >= vs)).sum()}")
mod = (t > vs) & (t <= ve)
ext = t > ve
print(f"moderados {mod.sum()}, extremos {ext.sum()}; los de abajo van de {t[t < vi].min()} a "
      f"{t[t < vi].max()} min; mínimo general {t.min()} en {(t == t.min()).sum()} pedidos (piso)")
m_, s_ = t.mean(), t.std()
zt = (t - m_) / s_
print(f"z: media {m_:.2f}, s {s_:.2f}; |z| > 3 {(zt.abs() > 3).sum()} pedidos "
      f"({(zt.abs() > 3).mean() * 100:.1f} %), por encima {(zt > 3).sum()}, por debajo {(zt < -3).sum()}; "
      f"media - 3s = {m_ - 3 * s_:.1f}, media + 3s = {m_ + 3 * s_:.1f}; "
      f"todos dentro de los de la valla {bool((t[zt.abs() > 3] > vs).all())}")
print(f"|z| > 3 con s entre n − 1 y entre n: {(zt.abs() > 3).sum()} y "
      f"{(((t - m_) / t.std(ddof=0)).abs() > 3).sum()}; entre la valla y z = 3 (la valla sí, z no): "
      f"{((t > vs) & (t <= m_ + 3 * s_)).sum()}; más allá de z = 3: {(t > m_ + 3 * s_).sum()}")
print(f"enmascaramiento: s con todos {s_:.2f}, sin los {fuera_t.sum()} {t[~fuera_t].std():.2f}; "
      f"media sin ellos {t[~fuera_t].mean():.1f}; con s sin atípicos, z > 3 marcaría "
      f"{((t - t[~fuera_t].mean()) / t[~fuera_t].std() > 3).sum()}")
p = datos["n_productos"]
pq1, pq3 = p.quantile(0.25), p.quantile(0.75)
vp = pq3 + 1.5 * (pq3 - pq1)
print(f"productos: Q1 {pq1:.0f}, Q3 {pq3:.0f}, RIC {pq3 - pq1:.0f}, valla inferior "
      f"{pq1 - 1.5 * (pq3 - pq1):.0f}, valla superior {vp:.0f}; fuera {(p > vp).sum()} "
      f"({(p > vp).mean() * 100:.1f} %); con exactamente {vp:.0f}: {(p == vp).sum()}; de 7 a 17: "
      f"{((p > vp) & (p <= 17)).sum()}; 20 o más: {(p >= 20).sum()} (de {p[p >= 20].min()} a "
      f"{p.max()}); entre 18 y 19: {p.between(18, 19).sum()}; el mayor por debajo del hueco "
      f"{p[p < 20].max()}; 1 a 3 productos {(p <= 3).mean() * 100:.1f} %")
print("productos, pedidos con 15, 16 y 17:", p[p.between(15, 17)].value_counts().sort_index().to_dict())
lent = datos[t > vs]
for nombre, sub in [("moderados", datos[mod]), ("extremos", datos[ext]), ("todos", datos)]:
    print(f"{nombre}: n {len(sub)}, km mediana {sub['distancia_km'].median():.2f}, "
          f"lluvia {(sub['lluvia'] == 'Sí').mean() * 100:.1f} %, "
          f"Bogotá {(sub['ciudad'] == 'Bogotá').mean() * 100:.1f} %, "
          f"más de 7,7 km {(sub['distancia_km'] > 7.7).mean() * 100:.1f} %")
cal_ext = datos.loc[ext, "calificacion"].dropna()
print(f"extremos calificados {len(cal_ext)}, con 1 estrella {(cal_ext == 1).sum()} "
      f"({(cal_ext == 1).mean() * 100:.1f} %); sin calificar {ext.sum() - len(cal_ext)}")
cal_todos = datos["calificacion"].dropna()
print(f"todos los calificados {len(cal_todos)}: con 1 estrella {(cal_todos == 1).mean() * 100:.1f} %, "
      f"con 4 o 5 {(cal_todos >= 4).mean() * 100:.1f} %; de {n}, calificados "
      f"{len(cal_todos) / n * 100:.1f} %")
print(f"extremos: calificados {len(cal_ext)} de {ext.sum()}, el {len(cal_ext) / ext.sum() * 100:.1f} %, "
      f"frente al {len(cal_todos) / n * 100:.1f} % de todos los pedidos")
lento_max = datos.loc[t.idxmax()]
print(f"z del más lento: {(t.max() - m_) / s_:.1f}")
print("el más lento:", lento_max[["id_pedido", "fecha", "ciudad", "distancia_km", "lluvia",
                                  "tiempo_entrega_min", "calificacion"]].to_dict())
print("atípicos (global) por ciudad:", lent["ciudad"].value_counts().to_dict())
pct_propia = {}
for c, x in datos.groupby("ciudad")["tiempo_entrega_min"]:
    a_, b_ = x.quantile(0.25), x.quantile(0.75)
    pct_propia[c] = (x > b_ + 1.5 * (b_ - a_)).mean() * 100
print(f"Bogotá: {(datos['ciudad'] == 'Bogotá').mean() * 100:.1f} % de los pedidos y "
      f"{(lent['ciudad'] == 'Bogotá').mean() * 100:.1f} % de los {len(lent)} lentos (valla global); "
      f"con su valla, {pct_propia['Bogotá']:.1f} %; sobre su valla propia, las ciudades van de "
      f"{min(pct_propia.values()):.1f} a {max(pct_propia.values()):.1f} %")
for c, x in datos.groupby("ciudad")["tiempo_entrega_min"]:
    a_, b_ = x.quantile(0.25), x.quantile(0.75)
    vc = b_ + 1.5 * (b_ - a_)
    exc = x[x > vc] - vc
    print(f"  {c}: n {len(x)}, valla propia {vc:.2f}, fuera propia {(x > vc).sum()}, "
          f"fuera global {(x > vs).sum()}, solo en su ciudad {((x > vc) & (x <= vs)).sum()}, "
          f"exceso mediano {exc.median():.1f}, máximo {x.max()}, exceso máximo {exc.max():.1f}, "
          f"% fuera propia {(x > vc).mean() * 100:.2f}")
d = datos["distancia_km"]
dq1, dq3 = d.quantile(0.25), d.quantile(0.75)
print(f"distancia: Q1 {dq1:.1f}, mediana {d.median():.1f}, Q3 {dq3:.1f}, valla superior "
      f"{dq3 + 1.5 * (dq3 - dq1):.1f}; con 14 km {(d == 14).sum()}; más de 8 km {(d > 8).sum()}; "
      f"entre 13 y 14 sin el tope {((d > 13) & (d < 14)).sum()}; exactamente 7,7 km {(d == 7.7).sum()}; "
      f"máximo {d.max()}; media {d.mean():.4f}")
d30 = d.replace(14, 30)
print(f"tope a 30 km (clave del ejercicio 3): mediana {d.median():.2f} → {d30.median():.2f}; "
      f"media {d.mean():.4f} → {d30.mean():.4f} (sube {d30.mean() - d.mean():.4f}); "
      f"sin los 20: media {d[d < 14].mean():.4f}")
num = ["n_productos", "valor_pedido", "distancia_km", "tiempo_entrega_min"]
print(f"errores: filas repetidas {datos.duplicated().sum()}, códigos repetidos "
      f"{datos['id_pedido'].duplicated().sum()}, valores <= 0 {(datos[num] <= 0).sum().sum()}")
r_ = t[~fuera_t]
ra, rb = r_.quantile(0.25), r_.quantile(0.75)
print(f"cadena: borrados {fuera_t.sum()}, vallas nuevas {ra - 1.5 * (rb - ra):.2f} y "
      f"{rb + 1.5 * (rb - ra):.2f}, atípicos nuevos "
      f"{((r_ < ra - 1.5 * (rb - ra)) | (r_ > rb + 1.5 * (rb - ra))).sum()}")
resto_, rondas = t.copy(), []
while True:                          # la cadena repetida hasta que no aparezcan nuevos
    ra, rb = resto_.quantile(0.25), resto_.quantile(0.75)
    f_r = (resto_ < ra - 1.5 * (rb - ra)) | (resto_ > rb + 1.5 * (rb - ra))
    rondas.append(int(f_r.sum()))
    if f_r.sum() == 0:
        break
    resto_ = resto_[~f_r]
print(f"cadena repetida: {' → '.join(map(str, rondas))} por ronda; se detiene en la ronda "
      f"{len(rondas)}; borrados {sum(rondas)} ({sum(rondas) / n * 100:.1f} %)")
tab = pd.pivot_table(datos, values="tiempo_entrega_min", index="ciudad", columns="lluvia",
                     aggfunc="median", observed=True, margins=True, margins_name="Total")
dif = tab["Sí"] - tab["No"]
print(f"tabla dinámica: la lluvia suma de {dif.drop('Total').min():.1f} a "
      f"{dif.drop('Total').max():.1f} min por ciudad (entre {dif.drop('Total').min():.0f} y "
      f"{dif.drop('Total').max():.0f}) y {dif['Total']:.1f} en el total (medianas)")
print(f"composición (medianas de la tabla): Bogotá − Barranquilla en Total "
      f"{tab.loc['Bogotá', 'Total'] - tab.loc['Barranquilla', 'Total']:.1f}, sin lluvia "
      f"{tab.loc['Bogotá', 'No'] - tab.loc['Barranquilla', 'No']:.1f}, con lluvia "
      f"{tab.loc['Bogotá', 'Sí'] - tab.loc['Barranquilla', 'Sí']:.1f}")
ll = (datos["lluvia"] == "Sí").groupby(datos["ciudad"]).mean() * 100
print("% con lluvia por ciudad:", ll.round(1).to_dict(),
      f"; total {(datos['lluvia'] == 'Sí').mean() * 100:.1f}")
mll = datos.groupby("lluvia")["tiempo_entrega_min"].mean()
dentro = datos.groupby(["ciudad", "lluvia"])["tiempo_entrega_min"].mean().unstack()
peso = datos.groupby("ciudad").size()
print(f"con medias (sesión 1): la lluvia suma {mll['Sí'] - mll['No']:.1f} min en el total y "
      f"{((dentro['Sí'] - dentro['No']) * peso).sum() / peso.sum():.1f} dentro de cada ciudad "
      f"(promedio ponderado por pedidos)")
tr = pd.cut(d, bins=[0, 4.4, 7.7, 14], right=True)
des = pd.pivot_table(datos.assign(tramo=tr, lento=(t > vs) * 100), values="lento", index="tramo",
                     columns="lluvia", aggfunc="mean", observed=True)
print("desglose, % de lentos:", des.round(1).to_dict())
print("pedidos por tramo y lluvia:", datos.assign(tramo=tr).groupby(["tramo", "lluvia"],
      observed=True).size().to_dict())
v = datos["valor_pedido"]
vq1, vq3 = v.quantile(0.25), v.quantile(0.75)
vvi, vvs = vq1 - 1.5 * (vq3 - vq1), vq3 + 1.5 * (vq3 - vq1)
zv1 = (v - v.mean()) / v.std()
zv0 = (v - v.mean()) / v.std(ddof=0)
print(f"valor (clave del ejercicio 1): Q1 {vq1:.0f}, Q3 {vq3:.0f}, RIC {vq3 - vq1:.0f}; "
      f"vallas {vvi:.0f} y {vvs:.0f}; fuera {((v < vvi) | (v > vvs)).sum()}, con >= "
      f"{((v <= vvi) | (v >= vvs)).sum()}, exactamente en la valla {(v == vvs).sum()}; "
      f"|z| > 3: {(zv1.abs() > 3).sum()} (n − 1) y {(zv0.abs() > 3).sum()} (N); "
      f"media − 3s = {v.mean() - 3 * v.std():.0f}, media + 3s = {v.mean() + 3 * v.std():.0f}; "
      f"máximo {v.max()}")
bog = t[datos["ciudad"] == "Bogotá"]
vb = bog.quantile(0.75) + 1.5 * (bog.quantile(0.75) - bog.quantile(0.25))
entre_b = bog[(bog > vs) & (bog <= vb)]
farm = datos.loc[datos["categoria"] == "Farmacia", "valor_pedido"]
vf = farm.quantile(0.75) + 1.5 * (farm.quantile(0.75) - farm.quantile(0.25))
entre_f = farm[(farm > vf) & (farm <= vvs)]
print(f"autoevaluación: valla de Bogotá {vb:.2f}; pedidos de Bogotá entre {vs:.2f} y {vb:.2f}: "
      f"{len(entre_b)}, de 61.5 a 62.5 min: {entre_b.between(61.5, 62.5).sum()}; valla superior de "
      f"las farmacias {vf:.0f} (la de todos los pedidos, {vvs:.0f}); farmacias entre las dos: "
      f"{len(entre_f)}, la más cercana a 120 000: {entre_f.iloc[(entre_f - 120000).abs().argmin()]}; "
      f"valla de la distancia {dq3 + 1.5 * (dq3 - dq1):.1f}; valla de productos {vp:.0f}")
fr = pd.pivot_table(datos.assign(franja=pd.Categorical(datos["franja"], franjas, ordered=True)),
                    values="tiempo_entrega_min", index="ciudad", columns="franja",
                    aggfunc="median", observed=True)
print("ciudad × franja, medianas (clave del ejercicio 2):")
print(fr.round(1).to_string())
print("franja más lenta por ciudad:", fr.idxmax(axis=1).to_dict(),
      "; la más rápida:", fr.idxmin(axis=1).to_dict())
f_ = pd.to_datetime(datos["fecha"])
sem = f_.dt.isocalendar().week
ps = datos.groupby(sem).size()
dias_ = f_.groupby(sem).nunique()
print(f"semanas ISO: {len(ps)}, de la {ps.index.min()} a la {ps.index.max()}; incompletas "
      f"{list(dias_[dias_ < 7].index)} con {list(ps[dias_ < 7])} pedidos y {list(dias_[dias_ < 7])} días; "
      f"completas: de {ps[dias_ == 7].min()} a {ps[dias_ == 7].max()} pedidos, mediana "
      f"{ps[dias_ == 7].median():.0f}; 1 de enero {f_.min():%A} (semana "
      f"{f_.min().isocalendar().week}), 30 de junio {f_.max():%A} (semana {f_.max().isocalendar().week})")
cs = datos.assign(semana=sem).groupby(["ciudad", "semana"]).size()
print(f"pedidos por ciudad y semana completa: de {cs[cs.index.get_level_values(1).isin(dias_[dias_ == 7].index)].min()} "
      f"a {cs[cs.index.get_level_values(1).isin(dias_[dias_ == 7].index)].max()}")
cal_sem = datos.assign(semana=sem).groupby("semana")["calificacion"].count()
print(f"calificados por semana completa: de {cal_sem[dias_ == 7].min()} a {cal_sem[dias_ == 7].max()}")
cal_cs = datos.assign(semana=sem).groupby(["ciudad", "semana"])["calificacion"].count()
print(f"calificados por ciudad y semana completa: de "
      f"{cal_cs[cal_cs.index.get_level_values(1).isin(dias_[dias_ == 7].index)].min()} a "
      f"{cal_cs[cal_cs.index.get_level_values(1).isin(dias_[dias_ == 7].index)].max()}")
from matplotlib.cbook import boxplot_stats   # lo mismo que dibuja ax.boxplot
for nombre, col in [("tiempo", "tiempo_entrega_min"), ("productos", "n_productos"),
                    ("distancia", "distancia_km"), ("valor", "valor_pedido")]:
    bx = boxplot_stats(datos[col].to_numpy())[0]
    print(f"caja de {nombre}: bigotes {bx['whislo']} y {bx['whishi']}; puntos sueltos "
          f"{len(bx['fliers'])} en {len(set(bx['fliers']))} valores distintos; con 14 km "
          f"{(bx['fliers'] == 14).sum() if col == 'distancia_km' else '-'}")
for c, x in datos.groupby("ciudad")["tiempo_entrega_min"]:
    bx = boxplot_stats(x.to_numpy())[0]
    a_, b_ = x.quantile(0.25), x.quantile(0.75)
    vc = b_ + 1.5 * (b_ - a_)
    print(f"  caja de {c}: bigote superior {bx['whishi']}, puntos arriba "
          f"{(bx['fliers'] > bx['whishi']).sum()}, abajo {(bx['fliers'] < bx['whislo']).sum()}, "
          f"máximo {x.max()}; solo con la valla global {((x > vs) & (x <= vc)).sum()}")
print(f"umbral de ejemplo: más de 45 min {(t > 45).sum()} pedidos ({(t > 45).mean() * 100:.1f} %)")
print("pedidos por ciudad:", datos["ciudad"].value_counts().to_dict())
print(f"faltantes de calificación {datos['calificacion'].isna().mean() * 100:.1f} %")
