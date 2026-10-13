# Fuente ÚNICA del código de la Sesión 2. De aquí salen:
#   - el notebook para Colab                    (notebook.py genera 2)
#   - las salidas y las gráficas que muestran las diapositivas
#                                               (notebook.py ejecuta 2 → salidas_sesion2.json y
#                                                fuente/diapositivas/recursos/s2/<id>.svg)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py, ayudas.py y
#               ayudas_sesion2.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar
#   precalculo  cifras que las diapositivas citan en el texto: se ejecuta, NO va al notebook

# %% [markdown]
# # Sesión 2 · De 12 000 filas a una distribución
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este cuaderno (*notebook*) acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-2-de-las-filas-a-la-distribucion.html).
# Cada celda lleva entre corchetes el mismo identificador que el código proyectado, así que puedes seguir
# la clase celda a celda. La portada del curso está en https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/
#
# 1. **Archivo → Guardar una copia en Drive** para que tus cambios no se pierdan.
# 2. Ejecuta las celdas **en orden** con **Mayús + Enter**. Varias usan resultados de las anteriores.
#    Si Colab avisa que el cuaderno no es de Google, elige **Ejecutar de todos modos**.
# 3. Si Colab se reinicia o una celda falla al repetirla, usa **Entorno de ejecución → Ejecutar anteriores**.
# 4. La primera celda crea los datos del caso *Tingua Domicilios S.A.S.*, una empresa **ficticia**
#    (sus datos se inventan con una semilla fija y no corresponden a personas ni a empresas reales),
#    y les da a las gráficas los colores del curso.

# %% datos generador
# Crea datos/pedidos.csv: los mismos 12 000 pedidos de la sesión 1
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Los datos, con sus escalas
#
# Cargamos los pedidos y declaramos las escalas, como en la práctica de la sesión 1: el orden de
# `franja`, `estrato` y `calificacion` decide el orden de sus tablas.

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
# ## 2 · Variables cualitativas
#
# ### Nominal: cuántos pedidos hay de cada categoría
#
# La **frecuencia absoluta** $n_i$ cuenta los pedidos de cada categoría; la **relativa**,
# $f_i = n_i / n$, dice qué parte del total son. Sumadas, dan $n$ y 1 (el 100 %).

# %% nominal
conteo = pedidos["categoria"].value_counts()
porcentaje = pedidos["categoria"].value_counts(normalize=True) * 100
tabla = pd.DataFrame({"pedidos": conteo, "%": porcentaje.round(1)})
tabla

# %% barras_nominal
# Una nominal no tiene orden: las barras van de mayor a menor
ax = conteo.sort_values().plot.barh(width=0.6)
ax.bar_label(ax.containers[0], padding=3)
ax.set_title("Pedidos por categoría de comercio")
ax.set_xlabel("Pedidos")
ax.set_ylabel("")
plt.show()

# %% [markdown]
# ### Ordinal: el orden de la tabla lo pone la escala
#
# En una ordinal las categorías van en su orden, no por tamaño, y se pueden **acumular**: el
# **% acumulado** $F_i$ dice qué parte de los pedidos está en esa categoría **o en una anterior**.

# %% ordinal
# sort=False: en el orden de la escala (1 a 5), no por tamaño
estrellas = pedidos["calificacion"].value_counts(sort=False)
n = estrellas.sum()          # solo los pedidos calificados
tabla = pd.DataFrame({
    "pedidos": estrellas,
    "%": (estrellas / n * 100).round(1),
    "% acumulado": (estrellas.cumsum() / n * 100).round(1),
})
tabla

# %% [markdown]
# ### ¿Sobre qué total?
#
# `value_counts` deja fuera, sin avisar, los pedidos sin calificación: el 37,4 % de cinco estrellas es
# de los pedidos **calificados**. Con `dropna=False`, el total son todos los pedidos.

# %% total
# value_counts deja fuera los faltantes (NaN); dropna=False los cuenta
todas = pedidos["calificacion"].value_counts(
    normalize=True, sort=False, dropna=False)
(todas * 100).round(1)

# %% barras_ordinal
# Una ordinal sí tiene orden: las barras van en el orden del día
franja = pedidos["franja"].value_counts(sort=False)
ax = franja.plot.bar(width=0.6, rot=0)
ax.set_title("Pedidos por franja, en el orden del día")
ax.set_xlabel("")
ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ## 3 · Variables cuantitativas
#
# ### Discreta: una fila por valor, mientras sean pocos

# %% discreta
productos = pedidos["n_productos"].value_counts().sort_index()
print("Valores distintos:", len(productos),
      "· del", productos.index.min(), "al", productos.index.max())
productos.head(6)

# %% [markdown]
# ### Continua: se agrupa en intervalos
#
# El tiempo toma cientos de valores distintos: una tabla con una fila por valor no resume nada.
# Se agrupa en **intervalos** (clases) que no se traslapan y cubren todos los datos. La regla de
# Sturges sugiere cuántos: $k \approx 1 + \log_2 n$.

# %% distintos
tiempo = pedidos["tiempo_entrega_min"]
print("Valores distintos:", tiempo.nunique(), "de", len(tiempo))
print("Del", tiempo.min(), "al", tiempo.max(), "minutos")

# %% sturges
import math

k = 1 + math.log2(len(tiempo))
print(f"Sturges sugiere unas {k:.1f} clases")

# %% intervalos
cortes = [0, 10, 20, 30, 40, 50, 60, 70, 80, float("inf")]
clases = pd.cut(tiempo, bins=cortes, right=False)   # [a, b)
tabla = clases.value_counts(sort=False).to_frame("pedidos")
tabla["%"] = (tabla["pedidos"] / len(tiempo) * 100).round(1)
acumulado = tabla["pedidos"].cumsum() / len(tiempo) * 100
tabla["% acumulado"] = acumulado.round(1)
tabla

# %% [markdown]
# ### El histograma muestra la forma
#
# Es la tabla agrupada hecha gráfica: barras pegadas, porque el eje es continuo, y, con intervalos de
# igual ancho, la altura es la frecuencia. Mira si la distribución es simétrica, asimétrica o tiene
# dos jorobas.

# %% histograma
# Intervalos de 5 minutos, del 0 al 205: el máximo (200.9) queda dentro
ax = tiempo.plot.hist(bins=range(0, 210, 5), edgecolor="white")
ax.set_title("Tiempo de entrega, en intervalos de 5 minutos")
ax.set_xlabel("Minutos")
ax.set_ylabel("Pedidos")
plt.show()

# %% anchos
# Los mismos datos con tres anchos de intervalo (hasta 120 min, para ver la forma)
fig, ejes = plt.subplots(1, 3, figsize=(9, 3))
for ax, ancho in zip(ejes, [1, 5, 25]):
    tiempo.plot.hist(bins=range(0, 230, ancho), ax=ax,
                     edgecolor="white", linewidth=0.5)
    ax.set_xlim(0, 120)
    ax.set_title(f"Intervalos de {ancho} min")
    ax.set_xlabel("Minutos")
    ax.set_ylabel("Pedidos")
plt.show()

# %% formas
# Tres variables de Tingua, tres formas: temperatura en Medellín, temperatura en
# las cinco ciudades (intervalos de 1 °C) y valor del pedido
# .loc[filas, columna]: solo las filas de Medellín, solo la temperatura
medellin = pedidos.loc[pedidos["ciudad"] == "Medellín", "temperatura_c"]
miles = pedidos["valor_pedido"] / 1000
fig, ejes = plt.subplots(1, 3, figsize=(9, 3))
medellin.plot.hist(bins=range(4, 38), ax=ejes[0], edgecolor="white")
ejes[0].set_title("Medellín (°C)")
pedidos["temperatura_c"].plot.hist(bins=range(4, 38), ax=ejes[1],
                                   edgecolor="white")
ejes[1].set_title("Cinco ciudades (°C)")
miles.plot.hist(bins=range(0, 1780, 20), ax=ejes[2], edgecolor="white")
ejes[2].set_xlim(0, 400)   # 16 pedidos pasan de 400 mil: la cola sigue
ejes[2].set_title("Valor (miles de COP)")
for ax in ejes:
    ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ## 4 · Tablas cruzadas: dos variables a la vez
#
# Una **tabla cruzada** (o de contingencia) cuenta los pedidos de cada combinación de dos variables
# cualitativas. Sus porcentajes se pueden sacar sobre tres totales distintos: el de cada fila, el de
# cada columna o el de toda la tabla. Antes de leer un porcentaje, pregunta: **¿sobre qué total?**

# %% cruzada
pd.crosstab(pedidos["ciudad"], pedidos["lluvia"],
            margins=True, margins_name="Total")

# %% por_fila
# normalize="index": cada fila (cada ciudad) suma 100 %
por_ciudad = pd.crosstab(pedidos["ciudad"], pedidos["lluvia"],
                         normalize="index")
(por_ciudad * 100).round(1)

# %% por_columna
# normalize="columns": cada columna suma 100 %
por_lluvia = pd.crosstab(pedidos["ciudad"], pedidos["lluvia"],
                         normalize="columns")
(por_lluvia * 100).round(1)

# %% barras_lluvia
ax = (por_ciudad["Sí"] * 100).sort_values().plot.barh(width=0.6)
ax.bar_label(ax.containers[0], fmt="{:.1f} %", padding=3)
ax.set_title("Pedidos entregados con lluvia, por ciudad")
ax.set_xlabel("% de los pedidos de cada ciudad")
ax.set_ylabel("")
plt.show()

# %% [markdown]
# ---
# # Práctica guiada
#
# Cuatro ejercicios. Cada celda termina con un verificador que dice qué está bien y, en lo demás, te
# da una pista sin darte la respuesta. Reemplaza cada `...` y ejecuta; puedes repetir la celda las
# veces que quieras.
#
# ## Ejercicio 1 · La tabla de una nominal
#
# Calcula las frecuencias de `medio_pago`: `conteo`, la absoluta, y `porcentaje`, la relativa en %.
# Pista: la celda [nominal].

# %% ej1 plantilla
conteo = ...       # frecuencia absoluta de medio_pago
porcentaje = ...   # frecuencia relativa de medio_pago, en %
revisar_nominal(conteo, porcentaje)

# %% ej1_solucion solucion
conteo = pedidos["medio_pago"].value_counts()
porcentaje = pedidos["medio_pago"].value_counts(normalize=True) * 100
revisar_nominal(conteo, porcentaje)

# %% [markdown]
# ## Ejercicio 2 · Una ordinal, acumulada
#
# Calcula las frecuencias de `estrato`: `conteo`, en el orden de la escala (del 1 al 6), y
# `acumulado`, el % acumulado. Pista: la celda [ordinal].
#
# Después responde abajo, en «Tus respuestas»: ¿qué porcentaje de los pedidos va a direcciones de
# estrato 3 o menos? ¿Y de estrato 4 o más?

# %% ej2 plantilla
conteo = ...       # pedidos por estrato, en el orden de la escala
acumulado = ...    # % acumulado, del estrato 1 al 6
revisar_acumulada(conteo, acumulado)

# %% ej2_solucion solucion
conteo = pedidos["estrato"].value_counts(sort=False)
acumulado = conteo.cumsum() / conteo.sum() * 100
revisar_acumulada(conteo, acumulado)

# %% [markdown]
# ## Ejercicio 3 · Una continua, en intervalos
#
# Agrupa `distancia_km` en intervalos de 2 km, cerrados a la izquierda (`[0, 2)`, `[2, 4)`…), que
# cubran **todos** los pedidos. Escribe solo la lista de `cortes`: el verificador arma la tabla con
# `pd.cut(..., right=False)`, como en la celda [intervalos].

# %% ej3 plantilla
cortes = ...       # una lista: [0, 2, 4, ...]
revisar_intervalos(cortes)

# %% ej3_solucion solucion
cortes = list(range(0, 17, 2))
revisar_intervalos(cortes)

# %% [markdown]
# Ahora mira las distancias largas con intervalos de medio kilómetro. ¿Qué pasa en 14 km? Pista: el
# diccionario de datos.

# %% ej3_grafica
# .loc[filas, columna]: solo los pedidos de 8 km o más, solo la distancia
largas = pedidos.loc[pedidos["distancia_km"] >= 8, "distancia_km"]
cortes = [8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15]
ax = largas.plot.hist(bins=cortes, edgecolor="white")
ax.set_title("Pedidos de 8 km o más, en intervalos de 0,5 km")
ax.set_xlabel("Kilómetros")
ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ## Ejercicio 4 · Qué se pide en cada franja
#
# Cruza `franja` (filas) con `categoria` (columnas) para ver la mezcla de categorías de cada franja:
# cada **fila** debe sumar 100 %. Pista: la celda [por_fila].
#
# Después responde abajo: ¿en qué franja pesa más Mercado? ¿Y Restaurante? ¿Por qué crees que pasa?

# %% ej4 plantilla
mezcla = ...       # pd.crosstab(filas, columnas, normalize=...)
revisar_cruzada(mezcla)

# %% ej4_solucion solucion
mezcla = pd.crosstab(pedidos["franja"], pedidos["categoria"],
                     normalize="index")
revisar_cruzada(mezcla)

# %% [markdown]
# ### Tus respuestas
#
# *Doble clic para escribir aquí.*
#
# 1. Ejercicio 2: estrato 3 o menos, … %; estrato 4 o más, … %.
# 2. Ejercicio 3: en 14 km pasa que…
# 3. Ejercicio 4: Mercado pesa más en…; Restaurante, en…, porque…

# %% cifras precalculo
# Cifras que las diapositivas citan en el texto (esta celda no va al notebook)
datos = pd.read_csv("datos/pedidos.csv")
t = datos["tiempo_entrega_min"]
print(f"tiempo: media {t.mean():.1f}, mediana {t.median():.1f}, "
      f"de 30 a 40 min {((t >= 30) & (t < 40)).mean() * 100:.1f} %")
temp = datos.groupby("ciudad")["temperatura_c"].mean().round(1)
print("temperatura media por ciudad:", temp.to_dict())
bogota = (datos["ciudad"] == "Bogotá")
print(f"Bogotá: {bogota.mean() * 100:.1f} % de los pedidos y "
      f"{bogota[datos['lluvia'] == 'Sí'].mean() * 100:.1f} % de los pedidos con lluvia")
print(f"distancia: {(datos['distancia_km'] == 14).sum()} pedidos con 14.0 km exactos; "
      f"{((datos['distancia_km'] >= 13.5) & (datos['distancia_km'] < 14)).sum()} entre 13,5 y 14")
cal = datos["calificacion"].value_counts(normalize=True).sort_index().cumsum()
print("calificación, % acumulado:", (cal * 100).round(1).to_dict())
v = datos["valor_pedido"]
print(f"valor: mediana {v.median():.0f}, máximo {v.max()}, más de 400 mil: {(v > 400_000).sum()}")
est = datos["calificacion"].value_counts().sort_index()
print(f"calificación: {est.sum()} calificados; acumulada absoluta {est.cumsum().to_dict()}; "
      f"4 o 5 estrellas {(est[4.0] + est[5.0]) / est.sum() * 100:.1f} %")
prod = datos["n_productos"]
print(f"productos: de 1 a 4, {(prod <= 4).mean() * 100:.1f} %; 10 o más, {(prod >= 10).sum()} pedidos")
k = 1 + math.log2(len(t))
print(f"Sturges: k {k:.1f}, amplitud {(t.max() - t.min()) / k:.1f}")
cinco = pd.cut(t, bins=range(0, 210, 5), right=False).value_counts()
print(f"intervalo de 5 min más frecuente: {cinco.idxmax()} con {cinco.max()} pedidos")
llueve = datos["lluvia"] == "Sí"
medias = datos.groupby("ciudad")["tiempo_entrega_min"].mean().round(1)
por = datos.groupby(["ciudad", "lluvia"])["tiempo_entrega_min"].mean().unstack()
n_ciudad = datos["ciudad"].value_counts()
dentro = ((por["Sí"] - por["No"]) * n_ciudad).sum() / n_ciudad.sum()
print(f"lluvia: diferencia {t[llueve].mean() - t[~llueve].mean():.2f}; dentro de cada ciudad "
      f"{dentro:.2f}; media por ciudad {medias.to_dict()}")
print("media sin lluvia por ciudad:", por["No"].round(1).to_dict())
grandes = datos[prod >= 10]
print("10 o más productos, por categoría:", grandes["categoria"].value_counts().to_dict())
caro = datos.loc[datos["valor_pedido"].idxmax()]
est3 = (datos["estrato"] <= 3).mean() * 100
print(f"estrato 3 o menos (clave del ejercicio 2): {est3:.4f} %")
print(f"pedido más caro: {caro['categoria']}, {caro['n_productos']} productos, {caro['valor_pedido']}")
