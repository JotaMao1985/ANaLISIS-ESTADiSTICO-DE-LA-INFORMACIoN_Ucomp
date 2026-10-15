# Fuente ÚNICA del código de la Sesión 3. De aquí salen:
#   - el notebook para Colab                    (notebook.py genera 3)
#   - las salidas y las gráficas que muestran las diapositivas
#                                               (notebook.py ejecuta 3 → salidas_sesion3.json y
#                                                fuente/diapositivas/recursos/s3/<id>.svg)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py, ayudas.py y
#               ayudas_sesion3.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar
#   precalculo  cifras que las diapositivas citan en el texto: se ejecuta, NO va al notebook

# %% [markdown]
# # Sesión 3 · Lo típico y lo variable
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este cuaderno (*notebook*) acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-3-lo-tipico-y-lo-variable.html).
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
# Crea datos/pedidos.csv: los mismos 12 000 pedidos de las sesiones 1 y 2
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Los datos, con sus escalas
#
# Cargamos los pedidos y declaramos las escalas, como en las sesiones 1 y 2: la escala de cada
# columna decide qué medida de centro tiene sentido.

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
# ## 2 · El centro: ¿cuánto tarda un pedido típico?
#
# ### La media y la mediana
#
# La **media** suma los valores y divide entre cuántos son: $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$.
# Es el punto de equilibrio de los datos: las distancias a la media de los que quedan por encima
# compensan las de los que quedan por debajo. La **mediana** es el valor del medio cuando se ordenan
# los datos: deja la mitad de los pedidos a cada lado.

# %% centro
tiempo = pedidos["tiempo_entrega_min"]
print(f"Media:   {tiempo.mean():.1f} min")
print(f"Mediana: {tiempo.median():.1f} min")

# %% [markdown]
# ### La moda de una continua es una clase, no un valor
#
# La **moda** es el valor más frecuente. En una variable continua casi ningún valor se repite, y el
# que más se repite lo decide el azar del redondeo. Lo que sí tiene sentido es la **clase modal**: el
# intervalo con más pedidos.

# %% moda
# La moda de los valores crudos: un tiempo que se repite por azar
moda = tiempo.mode()[0]
print("Moda de los valores:", moda, "min,",
      "en", (tiempo == moda).sum(), "pedidos")
# La clase modal: el intervalo de 5 min con más pedidos
clases = pd.cut(tiempo, bins=range(0, 210, 5), right=False)
conteo = clases.value_counts(sort=False)
print("Clase modal:", conteo.idxmax(), "con", conteo.max(), "pedidos")

# %% [markdown]
# ### El histograma, con la media y la mediana
#
# Es el histograma de la sesión 2 con dos líneas: la media y la mediana. La cola a la derecha
# separa una de la otra.

# %% histograma_centro
media, mediana = tiempo.mean(), tiempo.median()
ax = tiempo.plot.hist(bins=range(0, 210, 5), color="#8A2E9E", alpha=0.45,
                      edgecolor="white", label="Pedidos")
# Media en naranja, mediana en morado oscuro y punteada
ax.axvline(media, color="#F46201", linewidth=2.5,
           label=f"Media: {media:.1f} min")
ax.axvline(mediana, color="#3A0F47", linewidth=2.5, linestyle="--",
           label=f"Mediana: {mediana:.1f} min")
ax.set_xlim(0, 100)   # la cola sigue hasta 201 min
ax.legend()
ax.set_title("Tiempo de entrega, con su media y su mediana")
ax.set_xlabel("Minutos")
ax.set_ylabel("Pedidos")
plt.show()

# %% [markdown]
# ### Media frente a mediana
#
# Con los cinco tiempos del diagnóstico de la sesión 1 se ve por qué se separan: un solo pedido muy
# lento arrastra la media; la mediana solo mira el orden.

# %% cinco
cinco = pd.Series([20, 22, 25, 27, 150])   # los tiempos del diagnóstico
print("Media:", cinco.mean(), "· mediana:", cinco.median())
# ¿Y si el pedido de 150 min hubiera tardado 300?
cinco[4] = 300
print("Media:", cinco.mean(), "· mediana:", cinco.median())

# %% valor
# El valor del pedido: una cola a la derecha mucho más larga
valor = pedidos["valor_pedido"]
print(f"Media: {valor.mean():.0f} pesos · mediana: {valor.median():.0f} pesos")

# %% [markdown]
# ### ¿Qué centro admite cada tipo de variable?
#
# | Tipo de variable | Medida de centro |
# |---|---|
# | Nominal | La moda |
# | Ordinal | La mediana (y la moda) |
# | Cuantitativa | La media o la mediana, según la forma; en una continua, la clase modal |
#
# La mediana de una ordinal sí tiene sentido: solo necesita el orden. Pero pandas no la calcula para
# una categoría ordenada: da `TypeError`. Es lo contrario de la sesión 1, donde se negaba a promediar
# el estrato porque eso no tenía sentido. Aquí el error es una limitación de pandas, y la mediana se
# lee en la acumulada.

# %% mediana_ordinal
# La mediana de una ordinal tiene sentido, pero pandas no la calcula
try:
    pedidos["franja"].median()
except TypeError as error:
    print("TypeError:", error)

# %% acumulada_franja
# Se lee en la acumulada: la primera franja que llega al 50 %
franja = pedidos["franja"].value_counts(sort=False, normalize=True)
(franja.cumsum() * 100).round(1)

# %% [markdown]
# ### Para profundizar: la media de datos agrupados
#
# Si solo tienes la tabla de intervalos, y no los 12 000 tiempos, puedes aproximar la media con la
# **marca de clase** $m_i$, el punto medio de cada intervalo, que representa a los $n_i$ pedidos que
# caen en él:
#
# $$\bar{x} \approx \frac{1}{n}\sum_{i} n_i\, m_i$$
#
# Con intervalos de 5 minutos, la aproximación queda muy cerca de la media verdadera. La tabla de
# 10 minutos de la sesión 2 no sirve para esto: su última clase, [80, inf), es abierta y no tiene
# punto medio.

# %% agrupada
# Para profundizar: la media aproximada con las marcas de clase
clases = pd.cut(tiempo, bins=range(0, 210, 5), right=False)
conteo = clases.value_counts(sort=False)
marcas = [intervalo.mid for intervalo in conteo.index]   # puntos medios
agrupada = (conteo * marcas).sum() / conteo.sum()
print(f"Media con las marcas de clase: {agrupada:.2f} min")
print(f"Media con los 12 000 tiempos:  {tiempo.mean():.2f} min")

# %% [markdown]
# ## 3 · La dispersión: ¿qué tan variable es?
#
# ### El rango
#
# El **rango** es el máximo menos el mínimo. Es fácil de calcular, pero solo mira dos pedidos: los
# dos más extremos.

# %% rango
print("Mínimo:", tiempo.min(), "· máximo:", tiempo.max())
print(f"Rango: {tiempo.max() - tiempo.min():.1f} min")

# %% [markdown]
# ### Varianza y desviación estándar
#
# La **varianza** promedia los cuadrados de las distancias a la media; la **desviación estándar** es
# su raíz, y vuelve a quedar en minutos:
#
# $$\sigma^2 = \frac{1}{N}\sum_{i=1}^{N} (x_i - \mu)^2 \qquad s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2$$
#
# $\sigma$ (divide entre $N$) es la de una población: aquí, los 12 000 pedidos. $s$ (divide entre
# $n - 1$) es la de una muestra. En pandas, `std()` divide entre $n - 1$; con `ddof=0`, entre $N$.

# %% desviacion
print(f"Varianza:       {tiempo.var():.1f} min²")
print(f"s, entre n - 1: {tiempo.std():.3f} min")      # lo que hace std()
print(f"σ, entre N:     {tiempo.std(ddof=0):.3f} min")

# %% [markdown]
# ### La trampa: pandas y numpy no dividen igual
#
# Con muchos datos no se nota; con pocos, sí. `ddof` dice cuánto se le resta a $n$ al dividir.

# %% ddof
import numpy as np

cinco = [20, 22, 25, 27, 150]   # los tiempos del diagnóstico
print(f"pandas: {pd.Series(cinco).std():.2f}")   # divide entre n - 1
print(f"numpy:  {np.std(cinco):.2f}")            # divide entre n
print(f"pandas con ddof=0: {pd.Series(cinco).std(ddof=0):.2f}")

# %% [markdown]
# ### La desviación, en minutos
#
# ¿Qué parte de los pedidos queda a menos de una desviación de la media?

# %% dentro
media, s = tiempo.mean(), tiempo.std()
# between: True si el tiempo está entre los dos valores
cerca = tiempo.between(media - s, media + s)
# La media de una columna de True y False es la proporción de True
print(f"De {media - s:.1f} a {media + s:.1f} min:",
      f"{cerca.mean() * 100:.1f} % de los pedidos")

# %% [markdown]
# ### Cuartiles, rango intercuartílico y `describe()`
#
# Los **cuartiles** parten los datos ordenados en cuatro partes con la misma cantidad de pedidos:
# por debajo de $Q_1$ queda el 25 %; de $Q_2$ (la mediana), el 50 %, y de $Q_3$, el 75 %. El **rango
# intercuartílico** (RIC) es $Q_3 - Q_1$: el ancho del 50 % central. `describe()` da el resumen de
# cinco números (mínimo, $Q_1$, mediana, $Q_3$ y máximo), con la media y la desviación.

# %% cuartiles
q1 = tiempo.quantile(0.25)
q3 = tiempo.quantile(0.75)
print(f"Q1 = {q1:.1f} · Q3 = {q3:.1f} · RIC = {q3 - q1:.1f} min")
tiempo.describe().round(1)

# %% [markdown]
# ### El diagrama de caja, por ciudad
#
# La caja va de $Q_1$ a $Q_3$, con la mediana adentro; los bigotes llegan hasta el último pedido que
# no se aleja más de 1,5 RIC de la caja, y los puntos sueltos son los que se alejan más:
# **candidatos a atípicos**, el tema de la sesión 4.

# %% cajas
# groupby("ciudad") separa los pedidos de cada ciudad
por_ciudad = pedidos.groupby("ciudad")["tiempo_entrega_min"]
orden = por_ciudad.median().sort_values().index   # de menor a mayor mediana
tiempos = [por_ciudad.get_group(ciudad) for ciudad in orden]

fig, ax = plt.subplots()
ax.boxplot(tiempos, widths=0.5, patch_artist=True,
           boxprops={"facecolor": "#EFE3F2", "edgecolor": "#8A2E9E"},
           medianprops={"color": "#3A0F47", "linewidth": 2.5},
           whiskerprops={"color": "#8A2E9E"},
           capprops={"color": "#8A2E9E"},
           flierprops={"marker": ".", "markersize": 4,
                       "markerfacecolor": "#8A2E9E",
                       "markeredgecolor": "none"})
ax.set_xticks(range(1, len(orden) + 1), orden)
ax.set_title("Tiempo de entrega por ciudad")
ax.set_ylabel("Minutos")
plt.show()

# %% [markdown]
# ### ¿Qué medidas se mueven con la cola?
#
# Una medida es **robusta** si unos pocos datos extremos no la mueven. Quitemos el 0,5 % de pedidos
# más lentos y comparemos.

# %% robustez
# Sin el 0,5 % más lento: los pedidos por encima del percentil 99,5
corte = tiempo.quantile(0.995)
sin_cola = tiempo[tiempo <= corte]
print(f"Salen {len(tiempo) - len(sin_cola)} pedidos,",
      f"de más de {corte:.1f} min")
print(f"Media:      {tiempo.mean():.1f} → {sin_cola.mean():.1f}")
print(f"Desviación: {tiempo.std():.1f} → {sin_cola.std():.1f}")
print(f"Mediana:    {tiempo.median():.1f} → {sin_cola.median():.1f}")

# %% [markdown]
# ### Dos ciudades con casi la misma media
#
# `groupby` separa los pedidos de cada ciudad y calcula lo mismo en cada grupo.

# %% dos_ciudades
dos = pedidos[pedidos["ciudad"].isin(["Barranquilla", "Bucaramanga"])]
grupos = dos.groupby("ciudad")["tiempo_entrega_min"]
resumen = pd.DataFrame({
    "media": grupos.mean(),
    "desviación": grupos.std(),
    "RIC": grupos.quantile(0.75) - grupos.quantile(0.25),
})
resumen.round(1)

# %% [markdown]
# ### El coeficiente de variación
#
# El **coeficiente de variación** (CV) es la desviación dividida entre la media: compara la
# variabilidad de cantidades con unidades o tamaños distintos. Solo vale para variables de **razón**
# (con un cero verdadero) y media positiva; nunca para la temperatura, que es de intervalo.

# %% cv
# Coeficiente de variación: la desviación como fracción de la media
valor = pedidos["valor_pedido"]
print(f"Tiempo: CV = {tiempo.std() / tiempo.mean():.2f}")
print(f"Valor:  CV = {valor.std() / valor.mean():.2f}")

# %% [markdown]
# ---
# # Práctica guiada
#
# Cuatro ejercicios. Cada celda termina con un verificador que dice qué está bien y, en lo demás, te
# da una pista sin darte la respuesta. Reemplaza cada `...` y ejecuta; puedes repetir la celda las
# veces que quieras.
#
# ## Ejercicio 1 · El centro de `n_productos`
#
# Calcula la media, la mediana y la moda de `n_productos`. Es discreta y sus valores se repiten
# mucho: aquí `mode()` sí tiene sentido. Pista: las celdas [centro] y [moda].
#
# Después responde abajo, en «Tus respuestas»: ¿cuál de las tres representa mejor al pedido típico?
# ¿Por qué?

# %% ej1 plantilla
media = ...      # media de n_productos
mediana = ...    # mediana de n_productos
moda = ...       # moda de n_productos
revisar_centro(media=media, mediana=mediana, moda=moda)

# %% ej1_solucion solucion
productos = pedidos["n_productos"]
media = productos.mean()
mediana = productos.median()
moda = productos.mode()[0]
revisar_centro(media=media, mediana=mediana, moda=moda)

# %% [markdown]
# ## Ejercicio 2 · La mediana de dos ordinales
#
# El `estrato` y la `calificacion` son ordinales, y `median()` no funciona con ellas (celda
# [mediana_ordinal]). Calcula el % acumulado de cada una, como en la celda [acumulada_franja], y
# escribe su mediana: la **primera** categoría en la que el % acumulado llega al 50 %. La de la
# calificación es la de los pedidos **calificados**.
#
# Después responde abajo: ¿por qué no resumir estas dos columnas con la media?

# %% ej2 plantilla
# Calcula aquí el % acumulado del estrato y el de la calificación


# Escribe la mediana que leíste en cada acumulada
mediana_estrato = ...
mediana_calificacion = ...
revisar_medianas(estrato=mediana_estrato, calificacion=mediana_calificacion)

# %% ej2_solucion solucion
estrato = pedidos["estrato"].value_counts(sort=False, normalize=True)
print((estrato.cumsum() * 100).round(1))
estrellas = pedidos["calificacion"].value_counts(sort=False, normalize=True)
print((estrellas.cumsum() * 100).round(1))
mediana_estrato = (estrato.cumsum() >= 0.5).idxmax()       # la primera que llega
mediana_calificacion = (estrellas.cumsum() >= 0.5).idxmax()
revisar_medianas(estrato=mediana_estrato, calificacion=mediana_calificacion)

# %% [markdown]
# ## Ejercicio 3 · El tiempo de entrega, ciudad por ciudad
#
# Calcula, para cada una de las cinco ciudades, la media, la desviación estándar y el RIC del tiempo
# de entrega: tres series con un valor por ciudad. Pista: la celda [dos_ciudades], con todas las
# ciudades.
#
# Después responde abajo: ¿en qué ciudad se le puede prometer a la clientela una ventana de entrega
# más estrecha? ¿Por qué no basta con mirar la media?

# %% ej3 plantilla
media = ...        # media del tiempo de entrega, por ciudad
desviacion = ...   # desviación estándar, por ciudad
ric = ...          # Q3 - Q1, por ciudad
revisar_por_ciudad(media=media, desviacion=desviacion, ric=ric)

# %% ej3_solucion solucion
grupos = pedidos.groupby("ciudad")["tiempo_entrega_min"]
media = grupos.mean()
desviacion = grupos.std()
ric = grupos.quantile(0.75) - grupos.quantile(0.25)
revisar_por_ciudad(media=media, desviacion=desviacion, ric=ric)

# %% [markdown]
# ## Ejercicio 4 · Los cuartiles de la distancia
#
# Calcula $Q_1$, $Q_3$ y el RIC de `distancia_km`. Deja la última línea como está: entrega cada valor
# con su nombre (`q1=`, `q3=`, `ric=`) para que el verificador no los confunda. Pista: la celda
# [cuartiles].

# %% ej4 plantilla
q1 = ...    # primer cuartil de distancia_km
q3 = ...    # tercer cuartil de distancia_km
ric = ...   # rango intercuartílico
revisar_cuartiles(q1=q1, q3=q3, ric=ric)

# %% ej4_solucion solucion
distancia = pedidos["distancia_km"]
q1 = distancia.quantile(0.25)
q3 = distancia.quantile(0.75)
ric = q3 - q1
revisar_cuartiles(q1=q1, q3=q3, ric=ric)

# %% [markdown]
# Ahora dibuja el diagrama de caja de `distancia_km`, con una sola caja. Pista: la celda [cajas]; con
# una sola columna, `ax.boxplot` la recibe directamente, sin `groupby`.
# **El verificador no revisa el diagrama**: compáralo tú con tus cuartiles. ¿Qué ves por encima del
# bigote superior? Pista: el diccionario de datos.

# %% ej4_caja plantilla
# Dibuja aquí el diagrama de caja de distancia_km

# %% ej4_caja_solucion solucion
fig, ax = plt.subplots()
ax.boxplot(pedidos["distancia_km"], widths=0.4,
           flierprops={"marker": ".", "markersize": 4})
ax.set_xticks([1], ["Todos los pedidos"])
ax.set_title("Distancia del comercio a la dirección")
ax.set_ylabel("Kilómetros")
plt.show()

# %% [markdown]
# ### Tus respuestas
#
# *Doble clic para escribir aquí.*
#
# 1. Ejercicio 1: al pedido típico lo representa mejor la …, porque …
# 2. Ejercicio 2: no resumo el estrato ni la calificación con la media porque …
# 3. Ejercicio 3: la ventana más estrecha se puede prometer en …, porque …; la media no basta porque …
# 4. Ejercicio 4: por encima del bigote superior veo …, y creo que es porque …

# %% cifras precalculo
# Cifras que las diapositivas citan en el texto (esta celda no va al notebook)
datos = pd.read_csv("datos/pedidos.csv")
t = datos["tiempo_entrega_min"]
n = len(t)
moda_t = t.mode()[0]
print(f"tiempo: n {n}, media {t.mean():.1f}, mediana {t.median():.1f}, "
      f"diferencia {t.mean() - t.median():.1f}")
print(f"moda cruda {moda_t} en {(t == moda_t).sum()} pedidos "
      f"({(t == moda_t).mean() * 100:.1f} %)")
c5 = pd.cut(t, bins=range(0, 210, 5), right=False).value_counts()
print(f"clase modal {c5.idxmax()} con {c5.max()} pedidos ({c5.max() / n * 100:.1f} %)")
diag = pd.Series([20, 22, 25, 27, 150])
diag300 = pd.Series([20, 22, 25, 27, 300])
print(f"cinco tiempos: media {diag.mean():.1f}, mediana {diag.median():.0f}, "
      f"rango {diag.max() - diag.min()}; con 300: media {diag300.mean():.1f}, "
      f"mediana {diag300.median():.0f}")
print(f"cinco tiempos: s {diag.std():.2f}, sigma {diag.std(ddof=0):.2f}; "
      f"desviaciones {(diag - diag.mean()).round(1).tolist()}, suman {(diag - diag.mean()).sum():.1f}")
v = datos["valor_pedido"]
print(f"valor: media {v.mean():.0f}, mediana {v.median():.0f}, máximo {v.max()}, "
      f"CV {v.std() / v.mean():.2f}")
print(f"rango: mínimo {t.min()}, máximo {t.max()}, rango {t.max() - t.min():.1f}")
print(f"varianza {t.var():.1f}; s {t.std():.3f}; sigma {t.std(ddof=0):.3f}; "
      f"redondeadas {t.std():.1f}")
m_, s_ = t.mean(), t.std()
dentro1 = t.between(m_ - s_, m_ + s_).mean() * 100
dentro2 = t.between(m_ - 2 * s_, m_ + 2 * s_).mean() * 100
print(f"media ± s: de {m_ - s_:.1f} a {m_ + s_:.1f}, {dentro1:.1f} %; "
      f"media ± 2s: de {m_ - 2 * s_:.1f} a {m_ + 2 * s_:.1f}, {dentro2:.1f} %")
q1_, q3_ = t.quantile(0.25), t.quantile(0.75)
valla_t = q3_ + 1.5 * (q3_ - q1_)
print(f"cuartiles: Q1 {q1_:.1f}, Q3 {q3_:.1f}, RIC {q3_ - q1_:.1f}; "
      f"valla superior {valla_t:.2f}, el bigote llega a {t[t <= valla_t].max()}; "
      f"por encima {(t > valla_t).sum()} pedidos")
corte = t.quantile(0.995)
sin = t[t <= corte]
print(f"robustez: salen {n - len(sin)} pedidos ({(n - len(sin)) / n * 100:.1f} %), de más de "
      f"{corte:.1f}; media {t.mean():.1f} → {sin.mean():.1f}; s {t.std():.1f} → "
      f"{sin.std():.1f} (baja {(1 - sin.std() / t.std()) * 100:.0f} %); "
      f"mediana {t.median():.1f} → {sin.median():.1f}")
g = datos.groupby("ciudad")["tiempo_entrega_min"]
tabla = pd.DataFrame({"n": g.size(), "media": g.mean(), "s": g.std(),
                      "RIC": g.quantile(0.75) - g.quantile(0.25), "mediana": g.median(),
                      "p99": g.quantile(0.99), "máximo": g.max(),
                      "más de 80": g.apply(lambda x: (x > 80).sum()),
                      "% más de 80": g.apply(lambda x: (x > 80).mean() * 100)})
print("por ciudad (clave del ejercicio 3):")
print(tabla.round(2).to_string())
print(f"menor s: {tabla['s'].idxmin()}; menor RIC: {tabla['RIC'].idxmin()}")
fuera = {}
for ciudad, x in g:
    a, b = x.quantile(0.25), x.quantile(0.75)
    fuera[ciudad] = int((x > b + 1.5 * (b - a)).sum())
print("puntos por encima del bigote, por ciudad:", fuera)
print(f"CV: tiempo {t.std() / t.mean():.2f}, valor {v.std() / v.mean():.2f}, "
      f"el del valor es {(v.std() / v.mean()) / (t.std() / t.mean()):.1f} veces el del tiempo")
tc = datos["temperatura_c"]
tf = tc * 9 / 5 + 32
print(f"temperatura: media {tc.mean():.1f} °C = {tf.mean():.1f} °F; "
      f"CV en °C {tc.std() / tc.mean():.2f}, en °F {tf.std() / tf.mean():.2f}")
p = datos["n_productos"]
print(f"productos (clave del ejercicio 1): media {p.mean():.4f}, mediana {p.median():.0f}, "
      f"moda {p.mode()[0]}; 1 o 2 productos {(p <= 2).mean() * 100:.1f} %; máximo {p.max()}")
e = datos["estrato"].value_counts(normalize=True).sort_index().cumsum() * 100
print("estrato, % acumulado (clave del ejercicio 2):", e.round(1).to_dict(),
      f"; media de los números {datos['estrato'].mean():.1f}")
cal = datos["calificacion"].value_counts(normalize=True).sort_index().cumsum() * 100
print("calificación, % acumulado entre calificados:", cal.round(1).to_dict(),
      f"; media de las estrellas {datos['calificacion'].mean():.2f}")
cal_todos = (datos["calificacion"].value_counts(dropna=False, normalize=True)
             .sort_index(na_position="last").cumsum() * 100)
print("calificación, % acumulado sobre todos los pedidos:", cal_todos.round(1).to_dict())
fr = datos["franja"].value_counts(normalize=True).reindex(franjas).cumsum() * 100
print("franja, % acumulado:", fr.round(1).to_dict())
d = datos["distancia_km"]
valla_d = d.quantile(0.75) + 1.5 * (d.quantile(0.75) - d.quantile(0.25))
print(f"distancia (clave del ejercicio 4): Q1 {d.quantile(0.25):.2f}, mediana "
      f"{d.median():.2f}, Q3 {d.quantile(0.75):.2f}, RIC "
      f"{d.quantile(0.75) - d.quantile(0.25):.2f}, media {d.mean():.2f}, "
      f"valla superior {valla_d:.2f}, el bigote llega a {d[d <= valla_d].max()}, "
      f"por encima {(d > valla_d).sum()}, con 14 km {(d == 14).sum()}")
marcas_ = [i.left + 2.5 for i in c5.sort_index().index]
print(f"media agrupada (5 min): {(c5.sort_index() * marcas_).sum() / n:.2f}")
