# Fuente ÚNICA del código de la Sesión 6. De aquí salen:
#   - el notebook para Colab                    (notebook.py genera 6)
#   - las salidas y las gráficas que muestran las diapositivas
#                                               (notebook.py ejecuta 6 → salidas_sesion6.json y
#                                                fuente/diapositivas/recursos/s6/<id>.svg)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py, ayudas.py y
#               ayudas_sesion6.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar
#   precalculo  cifras que las diapositivas citan en el texto: se ejecuta, NO va al notebook

# %% [markdown]
# # Sesión 6 · La cifra y su margen
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este cuaderno (*notebook*) acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-6-la-cifra-y-su-margen.html).
# Cada celda lleva entre corchetes el mismo identificador que el código proyectado, así que puedes seguir
# la clase celda a celda. La portada del curso está en https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/
# y el enunciado del proyecto final, el tablero, en
# [su página](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/proyecto-tablero.html).
#
# 1. **Archivo → Guardar una copia en Drive** para que tus cambios no se pierdan.
# 2. Ejecuta las celdas **en orden** con **Mayús + Enter**. Varias usan resultados de las anteriores.
#    Si Colab avisa que el cuaderno no es de Google, elige **Ejecutar de todos modos**.
# 3. Si Colab se reinicia o una celda falla al repetirla, usa **Entorno de ejecución → Ejecutar anteriores**.
# 4. La primera celda crea los datos del caso *Tingua Domicilios S.A.S.*, una empresa **ficticia**
#    (sus datos se inventan con una semilla fija y no corresponden a personas ni a empresas reales),
#    y les da a las gráficas los colores del curso.

# %% datos generador
# Crea datos/pedidos.csv: los mismos 12 000 pedidos de las sesiones 1 a 5
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Los datos, con sus escalas
#
# Cargamos los pedidos y declaramos las escalas, como en las sesiones anteriores. También usamos
# `numpy`, que se importa como `np`.

# %% cargar
import numpy as np
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
# ## La pregunta de hoy: ¿cuánto confiar en una muestra?
#
# En la sesión 5, la cifra de satisfacción del tablero fue el 79,1 % de 4 o 5 estrellas, con su
# «¿de quiénes?»: los 7099 pedidos que se calificaron. Hoy la pregunta es otra. Una cifra que sale de
# una muestra es una **estimación puntual**: con otra muestra habría salido otra. ¿Cuánto puede
# alejarse de la verdad solo por azar? Eso lo dice su **margen**.
#
# En la sesión 3 el lema fue «Ningún centro sin su dispersión»: era la dispersión de los pedidos. Hoy
# es la de las cifras que salen de una muestra: **ninguna cifra sin su margen**.
#
# Primero veremos qué pasa con muchas muestras (la distribución muestral); después, cómo poner el
# margen cuando hay una sola (el intervalo de confianza).
#
# La pregunta de entrada de la clase: en la semana 13, el 86,2 % de los pedidos calificados tuvo 4 o 5
# estrellas, la mejor del semestre. ¿Premiamos al equipo? La respondemos en la sección 4.

# %% [markdown]
# ## 2 · ¿Cuánto puede alejarse una muestra?
#
# En la sesión 5, las cuatro muestras al azar de 400 pedidos cayeron cerca de $\mu$. ¿Fue suerte?
# Repetimos el sorteo 1000 veces, cada vez con otra semilla, y guardamos la media de cada muestra.
# Como conocemos los 12 000 pedidos, sabemos dónde está $\mu$: el blanco.

# %% mil_muestras
tiempo = pedidos["tiempo_entrega_min"]
mu = tiempo.mean()                         # el parámetro: lo conocemos
medias = []
for i in range(1000):                      # 1000 muestras de 400 pedidos
    muestra = pedidos.sample(n=400, random_state=i)
    medias.append(muestra["tiempo_entrega_min"].mean())
medias = pd.Series(medias)
print(f"μ = {mu:.2f} min")
print(f"Las 1000 medias: de {medias.min():.2f} a {medias.max():.2f} min,",
      f"con media {medias.mean():.2f}")

# %% [markdown]
# Las 1000 medias forman la **distribución muestral** de $\bar x$: cómo se reparte la media de una
# muestra de 400 pedidos entre muchas muestras. A la izquierda, los pedidos; a la derecha, las medias,
# con una curva normal encima (centrada en $\mu$ y con la misma desviación que las medias).

# %% mil_muestras_grafica
from statistics import NormalDist
fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 3.8))
izq.hist(tiempo, bins=range(0, 205, 5), color="#8A2E9E")
izq.set_title("Los 12 000 pedidos")
izq.set_xlabel("Tiempo de entrega (min)")
izq.set_ylabel("Pedidos")
der.hist(medias, bins=30, density=True, color="#8A2E9E", alpha=0.55)
normal = NormalDist(mu, medias.std())   # mismo centro, misma desviación
x = np.linspace(medias.min(), medias.max(), 200)
der.plot(x, [normal.pdf(v) for v in x], color="#F46201", linewidth=2.5)
der.set_yticks([])                         # importa la forma, no la altura
der.set_title("Las 1000 medias de 400 pedidos")
der.set_xlabel("Media del tiempo (min)")
titulo = "Los pedidos son asimétricos; las medias de 400, casi normales"
fig.suptitle(titulo, x=0.01, ha="left", fontsize=15, fontweight="bold")
plt.show()

# %% [markdown]
# Los pedidos tienen una cola larga a la derecha, hasta 200,9 min. Las medias de 400 no: forman una
# campana estrecha alrededor de $\mu$, y la curva normal las describe bien. Fíjate en los ejes: los
# pedidos van de 0 a 200 min; las medias, de 33 a 38.
#
# ### El error estándar
#
# - La **desviación estándar** de los pedidos (sesión 3) dice cuánto varía **un pedido**.
# - La desviación de las 1000 medias dice cuánto varía **la media de una muestra**: se llama **error
#   estándar** (EE). Describe una cifra, no los pedidos.
#
# No hace falta simular para conocerlo. Si $\sigma$ es la desviación de los pedidos y $n$ el tamaño de
# la muestra,
#
# $$\mathrm{EE} = \frac{\sigma}{\sqrt{n}}$$

# %% error_estandar
sigma = tiempo.std(ddof=0)                 # la de los 12 000 pedidos
ee = medias.std()                          # la de las 1000 medias
print(f"Desviación estándar de los pedidos:  σ  = {sigma:.2f} min")
print(f"Error estándar de las medias de 400: EE = {ee:.2f} min")
print(f"La fórmula: σ / √400 = {sigma / np.sqrt(400):.2f} min")

# %% [markdown]
# La simulación (0,62) y la fórmula (0,63) casi coinciden. **Antes de seguir, predice:** si la gerencia
# toma 1600 pedidos en vez de 400, ¿el EE baja a la mitad o a la cuarta parte? La celda siguiente
# repite la simulación con 25, 100 y 400 pedidos: cada tamaño es 4 veces el anterior.

# %% tres_n
bordes = np.arange(28, 48, 0.4)           # las mismas barras en los tres
fig, ejes = plt.subplots(1, 3, figsize=(9.6, 3.4), sharex=True)
for n, ax in zip([25, 100, 400], ejes):
    medias_n = pd.Series([tiempo.sample(n=n, random_state=i).mean()
                          for i in range(1000)])
    print(f"n = {n:3}: EE = {medias_n.std():.2f}",
          f"(fórmula {sigma / np.sqrt(n):.2f})",
          f"· asimetría {medias_n.skew():.2f}")
    ax.hist(medias_n, bins=bordes, color="#8A2E9E")
    ax.set_title(f"n = {n} · EE = {medias_n.std():.2f}")
    ax.set_yticks([])
ejes[1].set_xlabel("Media del tiempo de entrega (min)")
fig.suptitle("Con 4 veces más pedidos, el error estándar baja a la mitad",
             x=0.01, ha="left", fontsize=15, fontweight="bold")
plt.show()

# %% [markdown]
# Cuatro veces más pedidos dan la mitad de EE, porque $\sqrt 4 = 2$. Con $n = 25$ las medias todavía se
# inclinan un poco a la derecha (su asimetría es la más alta); con 400, casi nada.
#
# ### La distribución normal
#
# Es lo que prometieron las sesiones 3 y 4. El **teorema del límite central** dice que, con $n$ grande,
# las medias de las muestras se reparten casi como una **normal**, aunque los datos no lo sean. En una
# normal, el 68 % queda a menos de una desviación del centro y el 95 % a menos de 1,96 desviaciones.
#
# - En las medias de 400 se cumple casi exacto: es una normal con desviación EE.
# - En los pedidos, no: a una desviación de la media hay un 81,7 % (sesión 3), porque no son normales.
#
# El puntaje $z$ de la sesión 4 también vale para una cifra: $z = (\bar x - \mu)/\mathrm{EE}$ dice a
# cuántos errores estándar de $\mu$ cayó una media. En el 95 % de las muestras, $|z| \le 1{,}96$.
#
# ### ¿Qué método de muestreo es más preciso?
#
# La sesión 5 lo dejó pendiente: con una sola muestra por método no se podía saber. Ahora repetimos
# 1000 veces cada método al azar (el sistemático solo tiene 30 inicios posibles) y medimos el error
# estándar de cada uno. Las medias de la aleatoria simple ya las tenemos: son `medias`. Tarda unos
# segundos.

# %% metodos_precision
fechas = pedidos["fecha"].drop_duplicates()        # los 181 días
metodos = {"Aleatoria simple": list(medias), "Sistemática": [],
           "Estratificada": [], "Por conglomerados": []}
for i in range(1000):
    estratificada = pedidos.groupby("ciudad").sample(frac=1/30,
                                                     random_state=i)
    metodos["Estratificada"].append(
        estratificada["tiempo_entrega_min"].mean())
    dias = fechas.sample(n=6, random_state=i)
    de_los_dias = pedidos[pedidos["fecha"].isin(dias)]
    metodos["Por conglomerados"].append(
        de_los_dias["tiempo_entrega_min"].mean())
for inicio in range(30):                           # los 30 inicios posibles
    metodos["Sistemática"].append(tiempo.iloc[inicio::30].mean())
ee_metodo = pd.Series({m: np.std(v) for m, v in metodos.items()})
print("Error estándar de cada método (min):")
print(ee_metodo.round(2).to_string())

# %% metodos_precision_grafica
conveniencia = pedidos[pedidos["ciudad"] == "Bogotá"].head(400)
x_conv = conveniencia["tiempo_entrega_min"].mean()   # no depende del azar
desorden = np.random.default_rng(0)   # separa los puntos de cada franja
fig, ax = plt.subplots(figsize=(6.4, 3.8))
for fila, (m, v) in enumerate(metodos.items()):
    y = fila + desorden.uniform(-0.25, 0.25, len(v))
    ax.scatter(v, y, s=8, alpha=0.3, color="#8A2E9E")
    ax.text(max(v) + 0.2, fila, f"EE = {np.std(v):.2f}", va="center")
ax.scatter(x_conv, len(metodos), s=110, color="#F46201", zorder=3)
ax.text(x_conv - 0.3, len(metodos), f"siempre {x_conv:.2f}", va="center",
        ha="right")
ax.axvline(mu, color="#3A0F47", linewidth=2, linestyle="--")
ax.set_yticks(range(len(metodos) + 1), list(metodos) + ["Por conveniencia"])
ax.set_ylim(len(metodos) + 0.6, -0.6)              # en el orden de la lista
ax.set_title("El azar da el ancho; el sesgo mueve el centro")
ax.set_xlabel("Media del tiempo de entrega (min); la línea es μ")
plt.show()

# %% [markdown]
# En Tingua, los cuatro métodos al azar tienen casi la misma precisión: sus franjas son casi igual de
# anchas y están centradas en $\mu$. Las centésimas de diferencia son en parte ruido de la simulación.
# La muestra por conveniencia cae siempre en el mismo punto, lejos de $\mu$: el azar da el ancho; el
# sesgo mueve el centro.
#
# ## 3 · En la vida real hay una sola muestra
#
# No conocemos $\mu$ ni $\sigma$: tenemos una muestra. En la fórmula del EE, $\sigma$ se reemplaza por la
# desviación de la muestra, $s$ (la que divide entre $n - 1$, sesión 3):
#
# $$\mathrm{EE} \approx \frac{s}{\sqrt{n}}$$
#
# Usamos la muestra aleatoria simple de la sesión 5, la de la semilla 1.

# %% una_muestra
muestra = pedidos.sample(n=400, random_state=1)   # la de la sesión 5
x_barra = muestra["tiempo_entrega_min"].mean()
s = muestra["tiempo_entrega_min"].std()           # divide entre n − 1
ee_1 = s / np.sqrt(400)
print(f"x̄ = {x_barra:.2f} min · s = {s:.2f} min · EE = {ee_1:.3f} min")

# %% [markdown]
# ### El intervalo de confianza de 95 %
#
# En el 95 % de las muestras, $\bar x$ cae a menos de 1,96 EE de $\mu$. Dándole la vuelta: si a cada
# $\bar x$ le sumamos y restamos 1,96 EE, el 95 % de esos intervalos atrapa a $\mu$. El **margen** es
# $1{,}96 \cdot \mathrm{EE}$ (en las encuestas lo llaman «margen de error»):
#
# $$\bar x \pm 1{,}96\,\mathrm{EE}$$

# %% intervalo
margen = 1.96 * ee_1          # el 1,96 deja el 95 % central de la normal
inferior, superior = x_barra - margen, x_barra + margen
print(f"Margen: ±{margen:.2f} min")
print(f"Intervalo de 95 %: [{inferior:.2f}; {superior:.2f}] min")
print(f"¿Contiene a μ = {mu:.2f}? {inferior <= mu <= superior}")

# %% [markdown]
# En la vida real no sabríamos si este intervalo contiene a $\mu$. ¿Qué quiere decir entonces el 95 %?
# Repetimos el intervalo con 100 muestras, las de las semillas 1 a 100.

# %% cien_intervalos
filas = []
for semilla in range(1, 101):             # 100 muestras, 100 intervalos
    x = pedidos.sample(n=400, random_state=semilla)["tiempo_entrega_min"]
    m = 1.96 * x.std() / np.sqrt(400)
    filas.append({"inferior": x.mean() - m, "superior": x.mean() + m})
intervalos = pd.DataFrame(filas, index=range(1, 101))
atrapa = (intervalos["inferior"] <= mu) & (mu <= intervalos["superior"])
print(f"Atrapan a μ: {atrapa.sum()} de 100")
print(f"Fallan por debajo: {(intervalos['superior'] < mu).sum()}",
      f"· por encima: {(intervalos['inferior'] > mu).sum()}")

# %% cien_intervalos_grafica
color = np.where(atrapa, "#8A2E9E", "#F46201")   # naranja: los que fallan
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.hlines(intervalos.index, intervalos["inferior"], intervalos["superior"],
          colors=color, linewidth=2)
ax.axvline(mu, color="#3A0F47", linewidth=2, linestyle="--")
ax.text(mu + 0.1, 103, f"μ = {mu:.2f}", ha="left")
ax.set_ylim(0, 107)
ax.set_title(f"{atrapa.sum()} de los 100 intervalos atrapan μ;"
             f" {(~atrapa).sum()} no")
ax.set_xlabel("Tiempo de entrega (min)")
ax.set_ylabel("Muestra (semilla)")
plt.show()

# %% [markdown]
# El 95 % es del **método**: de cada 100 intervalos calculados así, unos 95 atrapan a $\mu$. Un intervalo
# ya calculado lo atrapa o no; no tiene «95 % de probabilidad». Que aquí sean 93 y no 95 es azar: con
# 100 intervalos, lo esperable va de unos 91 a 99.
#
# ### Para una proporción
#
# La satisfacción es una proporción: el % de 4 o 5 estrellas. Su error estándar es
#
# $$\mathrm{EE} = \sqrt{\frac{\hat p\,(1-\hat p)}{n}}$$
#
# donde $\hat p$ es la proporción de la muestra y $n$, el número de pedidos **calificados**, no el de
# pedidos. La fórmula pide al menos 10 éxitos (4 o 5 estrellas) y 10 fracasos.

# %% proporcion
calificados = pedidos[pedidos["calificacion"].notna()]
buena = calificados["calificacion"] >= 4   # True si tiene 4 o 5 estrellas
p_hat = buena.mean()                       # la media de True y False
n = len(calificados)
ee_p = np.sqrt(p_hat * (1 - p_hat) / n)
margen_p = 1.96 * ee_p
print(f"n = {n} · éxitos: {buena.sum()} · fracasos: {(~buena).sum()}")
print(f"4 o 5 estrellas: {p_hat * 100:.2f} % ± {margen_p * 100:.2f} puntos")
print(f"Intervalo de 95 %: [{(p_hat - margen_p) * 100:.2f};",
      f"{(p_hat + margen_p) * 100:.2f}] %")

# %% [markdown]
# El margen depende de $n$, no de cuántos pedidos hay en total. Estimamos la satisfacción de la
# operación, la de los pedidos que vendrán, y no solo la de estos 12 000.
#
# ### Un intervalo mide el azar, no el sesgo
#
# Hagamos lo mismo con la insatisfacción, el % de 1 o 2 estrellas.

# %% sesgo_no
mala = calificados["calificacion"] <= 2    # True si tiene 1 o 2 estrellas
p_mala = mala.mean()
margen_mala = 1.96 * np.sqrt(p_mala * (1 - p_mala) / n)
print(f"1 o 2 estrellas: {p_mala * 100:.2f} %",
      f"± {margen_mala * 100:.2f} puntos")
print(f"Intervalo de 95 %: [{(p_mala - margen_mala) * 100:.2f};",
      f"{(p_mala + margen_mala) * 100:.2f}] %")

# %% [markdown]
# En la sesión 5, la comprobación que solo es posible en un caso ficticio dio la verdad: 3,80 % de 1 o 2
# estrellas. Queda **fuera** del intervalo. No es mala suerte: es el sesgo de no respuesta (los pedidos
# de más de 55 min se califican más). El intervalo mide el azar de quién calificó, no el sesgo. Más
# respuestas lo angostan, pero alrededor de la cifra sesgada: el *Literary Digest* tenía más de dos
# millones. Ponderar quita el sesgo que depende de lo que vemos, pero no el azar: la cifra ponderada
# también lleva su margen. El intervalo no quita nada.
#
# ## 4 · La satisfacción, semana a semana
#
# El tablero muestra la satisfacción de cada semana. Con menos calificados, el margen crece. La semana
# es la ISO (de lunes a domingo); `isocalendar()` la da como entero sin signo, y la pasamos a `int`
# enseguida para poder restar sin sorpresas.

# %% semanal
fecha = pd.to_datetime(pedidos["fecha"])
semana = fecha.dt.isocalendar().week.astype(int).rename("semana")
grupos = buena.groupby(semana)             # buena: solo los calificados
por_semana = pd.DataFrame({"n": grupos.size(),
                           "% 4 o 5": grupos.mean() * 100})
por_semana["margen"] = 1.96 * np.sqrt(
    por_semana["% 4 o 5"] * (100 - por_semana["% 4 o 5"]) / por_semana["n"])
por_semana["dias"] = fecha.groupby(semana).nunique()   # 7 si está completa
print(f"Semestre: {p_hat * 100:.2f} %")
por_semana.round(1)

# %% semanal_grafica
fig, ax = plt.subplots(figsize=(9.6, 3.8))
for sem, fila in por_semana.iterrows():
    color = "#F46201" if sem == 13 else "#8A2E9E"
    relleno = color if fila["dias"] == 7 else "white"  # incompleta: hueca
    ax.errorbar(sem, fila["% 4 o 5"], yerr=fila["margen"], fmt="o",
                color=color, mfc=relleno, capsize=3)
    if fila["dias"] < 7 and sem < 14:         # la primera, debajo
        ax.text(sem - 0.4, fila["% 4 o 5"] - fila["margen"] - 1,
                "incompleta", va="top", fontsize=11)
    elif fila["dias"] < 7:                    # la última, a la izquierda
        ax.text(sem - 0.4, fila["% 4 o 5"], "incompleta", ha="right",
                va="center", fontsize=11)
ax.axhline(p_hat * 100, color="#3A0F47", linewidth=2, linestyle="--")
ax.annotate(f"semestre:\n{p_hat * 100:.1f} %", (1.01, p_hat * 100),
            xycoords=("axes fraction", "data"), va="center")
ax.set_title("Cada semana trae unos ±5 puntos de azar")
ax.set_xlabel("Semana ISO (en naranja, la 13)")
ax.set_ylabel("% de 4 o 5 estrellas")
plt.show()

# %% [markdown]
# Cada barra es el intervalo de 95 % de su semana. Las semanas completas tienen de 226 a 305
# calificados y márgenes de unos ±4 a ±6 puntos; la 27, con dos días, ±11. Solo la semana 13 (en
# naranja) tiene un intervalo que no contiene la cifra del semestre.
#
# ¿Y por mes? Con unas 1100 a 1300 calificaciones por mes, el margen baja a unos ±2 puntos.

# %% mensual
mes = fecha.dt.month.rename("mes")
grupos_mes = buena.groupby(mes)
por_mes = pd.DataFrame({"n": grupos_mes.size(),
                        "% 4 o 5": grupos_mes.mean() * 100})
por_mes["margen"] = 1.96 * np.sqrt(
    por_mes["% 4 o 5"] * (100 - por_mes["% 4 o 5"]) / por_mes["n"])
llueve = pedidos["lluvia"] == "Sí"
por_mes["% con lluvia"] = llueve.groupby(mes).mean() * 100
por_mes["tiempo medio"] = tiempo.groupby(mes).mean()
por_mes.round(1)

# %% [markdown]
# Abril, el mes con más lluvia, sale más bajo; pero febrero, con poca lluvia, también. El mes solo no
# prueba que la lluvia baje la satisfacción: en la sesión 7 mediremos cuántos minutos suma la lluvia.
#
# ### La pregunta de entrada: ¿premiamos al equipo de la semana 13?
#
# Su intervalo no contiene la cifra del semestre. Pero con 27 semanas, se esperan 1 o 2 así solo por
# azar (el 5 % de 27). Esa semana también fue rápida, y la siguiente bajó al 76,5 %, dentro de su
# margen.
# **Todavía no**: una semana fuera de su margen pasa; mira si se repite y si el tiempo también cambió.
#
# ## 5 · ¿Cuántos calificados hacen falta?
#
# Si se despeja $n$ del margen $E = 1{,}96\,\sqrt{p(1-p)/n}$, sale el tamaño de muestra para un margen
# dado:
#
# $$n = \frac{1{,}96^2\, p\,(1-p)}{E^2}$$
#
# El tamaño se redondea siempre **hacia arriba**: con uno menos, el margen pasa de $E$.

# %% tamano
def tamano(p, e):                          # n = 1,96² · p · (1 − p) / E²
    return np.ceil(1.96 ** 2 * p * (1 - p) / e ** 2)

print(f"Nacional, ±3 puntos: {tamano(p_hat, 0.03):.0f} calificados")
print(f"Nacional, ±5 puntos: {tamano(p_hat, 0.05):.0f} calificados")
tasa = len(calificados) / len(pedidos)     # la parte que califica
for llamadas in [400, 400 * tasa]:
    e = 1.96 * np.sqrt(p_hat * (1 - p_hat) / llamadas) * 100
    print(f"Con {llamadas:.0f} respuestas: ±{e:.1f} puntos")

# %% [markdown]
# Si la gerencia llama a 400 pedidos y todos responden, el margen es de unos ±4 puntos. Si responden
# como en la app (el 59,2 %), son unas 237 respuestas y unos ±5 puntos, y el sesgo de no respuesta
# sigue ahí: el margen no lo mide.
#
# ## 6 · Para tu tablero
#
# - El indicador **no cambia**: el % de 4 o 5 estrellas entre los calificados, con su $n$.
# - El margen de una proporción pide al menos 10 éxitos y 10 fracasos (OpenIntro 5.1). Con pocos
#   calificados, **avisa** o **agrupa** (por ejemplo, por mes), y vuelve a revisar la condición en lo
#   agrupado.
# - Frente a la cifra del semestre, no anuncies cambios menores que el margen. Y no compares dos
#   semanas mirando si sus intervalos se tocan: entre dos semanas, el margen de la diferencia es de
#   unos ±7 puntos.
# - Las bandas de margen son opcionales: la página del proyecto las pone en «Para ir más lejos
#   (opcional)», como «intervalos de confianza para los porcentajes semanales (sesión 6)».
#
# ¿Cuántas combinaciones de ciudad y semana cumplen la condición?

# %% ciudad_semana
por_cs = buena.groupby([calificados["ciudad"], semana])
cs = pd.DataFrame({"n": por_cs.size(), "exitos": por_cs.sum()})
cs["fracasos"] = cs["n"] - cs["exitos"]
cs["aplica"] = (cs["exitos"] >= 10) & (cs["fracasos"] >= 10)
print(f"Combinaciones de ciudad y semana: {len(cs)}",
      f"· con 10 éxitos y 10 fracasos: {cs['aplica'].sum()}")
por_ciudad = cs.groupby(level="ciudad")
pd.DataFrame({"calificados por semana (mediana)": por_ciudad["n"].median(),
              "semanas con 10 y 10": por_ciudad["aplica"].sum()})

# %% [markdown]
# En Bogotá todas las semanas cumplen; en Barranquilla y Bucaramanga, ninguna. Una semana de
# Bucaramanga con pocos calificados, todos de 4 o 5, da 100 % con margen 0: la fórmula no aplica ahí.
# Agrupar por mes casi siempre basta, pero no siempre: revisa la condición también en los meses.
#
# ---
# # Práctica guiada
#
# Tres ejercicios; el tercero es **opcional** (o para la casa). Cada celda termina con un verificador
# que dice qué está bien y, en lo demás, te da una pista sin darte la respuesta. Completa lo que se
# indica y ejecuta; puedes repetir la celda las veces que quieras. Las respuestas escritas van al
# final, en «Tus respuestas»: esas no las revisa ningún verificador.
#
# ## Ejercicio 1 · La distribución muestral con $n = 100$
#
# Repite la celda [mil_muestras] con muestras de **100** pedidos y tu propia semilla.
#
# - Cambia `mi_semilla` por un número de tres cifras que elijas tú.
# - La plantilla trae el tamaño de la clase: cámbialo por el que pide el ejercicio.
# - A la línea de `medias.append` le falta algo: el ejercicio pide la **media** de cada muestra.
# - Esta celda reemplaza la lista `medias` de la clase: si después vuelves a una celda de la clase, usa
#   **Entorno de ejecución → Ejecutar anteriores**.
#
# Después responde abajo: el verificador te dice tu EE. ¿Cuánto quedaría con $n = 400$, y por qué?

# %% ej1 plantilla
mi_semilla = 123   # cámbiala por un número de tres cifras que elijas tú
medias = []
for i in range(1000):
    # ← cambia el 400 por el tamaño que pide el ejercicio
    muestra = pedidos.sample(n=400, random_state=mi_semilla + i)
    medias.append(muestra["tiempo_entrega_min"])   # ← ¿qué le falta?
revisar_medias(medias)

# %% ej1_solucion solucion
mi_semilla = 314
medias = []
for i in range(1000):
    muestra = pedidos.sample(n=100, random_state=mi_semilla + i)
    medias.append(muestra["tiempo_entrega_min"].mean())
revisar_medias(medias)

# %% [markdown]
# ## Ejercicio 2 · El intervalo de la semana 20
#
# La semana 20 es la semana completa con el % de 4 o 5 estrellas más bajo. Calcula su intervalo de
# 95 %, **en %**: la proporción $\hat p$ entre sus calificados, su $n$, su EE y el intervalo. La variable
# `semana` ya existe: viene de [semanal]. Pista: las celdas [proporcion] y [semanal].
#
# Deja como está la llamada final: entrega cada extremo con su nombre.
#
# Después responde abajo: ¿fue la semana 20 peor que el semestre?

# %% ej2 plantilla
semana_20 = pedidos[semana == 20]   # los pedidos de la semana 20
p_20 = ...       # la proporción de 4 o 5 estrellas entre sus calificados
n_20 = ...       # cuántos calificados tiene
ee_20 = ...      # su error estándar
inferior = ...   # el intervalo de 95 %, en %
superior = ...
revisar_intervalo(inferior=inferior, superior=superior)

# %% ej2_solucion solucion
semana_20 = pedidos[semana == 20]
calificados_20 = semana_20[semana_20["calificacion"].notna()]
p_20 = (calificados_20["calificacion"] >= 4).mean()
n_20 = len(calificados_20)
ee_20 = np.sqrt(p_20 * (1 - p_20) / n_20)
inferior = (p_20 - 1.96 * ee_20) * 100
superior = (p_20 + 1.96 * ee_20) * 100
revisar_intervalo(inferior=inferior, superior=superior)

# %% [markdown]
# ## Ejercicio 3 (opcional) · ¿Cuántos calificados necesita Bucaramanga para ±5 puntos?
#
# Con la $\hat p$ de 4 o 5 estrellas de Bucaramanga (entre sus calificados), calcula cuántos calificados
# hacen falta para un margen de ±5 puntos. Pista: la celda [tamano]. Si escribes $\hat p$ en proporción,
# $E$ también va en proporción (`0.05`).
#
# Después responde abajo: ¿cuántas semanas de calificaciones de Bucaramanga son? (Tiene unos 27
# calificados por semana.) ¿Conviene mostrarla por semana o por mes?

# %% ej3 plantilla
bucaramanga = ...   # los calificados de Bucaramanga
p_buc = ...         # su proporción de 4 o 5 estrellas
n_necesario = ...   # el tamaño para un margen de ±5 puntos
revisar_tamano(n=n_necesario)

# %% ej3_solucion solucion
bucaramanga = calificados[calificados["ciudad"] == "Bucaramanga"]
p_buc = (bucaramanga["calificacion"] >= 4).mean()
n_necesario = 1.96 ** 2 * p_buc * (1 - p_buc) / 0.05 ** 2
revisar_tamano(n=n_necesario)

# %% [markdown]
# ### Tus respuestas
#
# *Doble clic para escribir aquí.*
#
# 1. Ejercicio 1: mi EE con $n = 100$ salió …; con $n = 400$ quedaría cerca de … porque …
# 2. Ejercicio 2: el intervalo de la semana 20 es [… ; …]. ¿Fue peor que el semestre (79,07 %)? …
#    porque …
# 3. Ejercicio 3: Bucaramanga necesita … calificados, que son unas … semanas; conviene mostrarla …
#    porque …
# 4. Autoevaluación. ¿Verdadero o falso, o qué harías? Explica cada una.
#    - Una semana de Bucaramanga trae 4 calificaciones, todas de 4 o 5: 100 % ± 0. ¿Lo publicas así? …
#    - «El 95 % de los pedidos tarda entre 33,2 y 35,5 min.» …
#    - «Una encuesta voluntaria con 100 000 respuestas tiene ±0,25 puntos de margen y aun así puede
#      estar lejos de la verdad.» …
#    - Del tiempo de entrega tienes dos cifras: 12,7 min y 0,62 min (de muestras de 400). ¿Cuál usas
#      para decir cuánto varía un pedido y cuál para decir cuánto confiar en la media? …
#    - «Con el doble de calificados, el margen se parte por la mitad.» …

# %% [markdown]
# ---
# ## La respuesta a la gerencia
#
# **¿Cuánto confiar en una muestra? Lo que diga su margen.** El 79,1 % de 4 o 5 estrellas del semestre,
# con 7099 calificados, tiene un margen de ±1 punto; una semana, con unos 270 calificados, de unos ±5;
# y en una semana de Bucaramanga la fórmula ni siquiera aplica: hay que agrupar por mes o avisar. Y el
# margen no cubre el sesgo: que los calificados representen a todos sigue siendo el supuesto de la
# sesión 5.

# %% verdad_s5 precalculo
# La verdad de la sesión 5 (solo se cita en las diapositivas; no va al notebook, D24 y D25).
# Es una copia de calificacion_completa() de precalculo/ayudas_sesion5.py, que en la sesión 6
# no está en ayudas_sesion6.py: usa _pedido, _Azar y las constantes de la celda oculta.
def calificacion_completa():
    """La calificación que habría dado cada pedido si todos calificaran. Solo en un caso ficticio."""
    import numpy as np
    import pandas as pd
    from datetime import timedelta

    base = _Azar
    generar = _pedido
    semilla, total, inicio, n_dias, orden_franjas = SEMILLA, N_PEDIDOS, INICIO, DIAS, list(FRANJAS)

    class _Graba(base):
        def __init__(self, s):
            super().__init__(s)
            self.cinta = []

        def u(self):
            x = super().u()
            self.cinta[-1].append(x)
            return x

    class _Repite(base):
        def __init__(self, cinta):
            self.cinta, self.i = cinta, 0

        def u(self):
            x = self.cinta[self.i]
            self.i += 1
            return x

    original = pd.read_csv("datos/pedidos.csv")
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
    for i in orden:
        a, b = vistos[i], completos[i]
        if any(a[c] != b[c] for c in a if c != "calificacion") or b["calificacion"] == "":
            raise ValueError("cambió otra columna")
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


import math
_datos_v = pd.read_csv("datos/pedidos.csv")
_comp = _datos_v["id_pedido"].map(calificacion_completa())
_cal_v = _datos_v["calificacion"].notna()
_vis = _datos_v.loc[_cal_v, "calificacion"].astype(int)
verdad_45 = (_comp >= 4).mean() * 100
verdad_12 = (_comp <= 2).mean() * 100
print(f"reconstrucción: {len(_comp)} pedidos; coincide con las {len(_vis)} visibles: "
      f"{bool((_comp[_cal_v] == _vis).all())}")
print(f"verdad de la S5 (12 000 pedidos): 4 o 5 {verdad_45:.2f} %, 1 o 2 {verdad_12:.2f} %")
if round(verdad_45, 2) != 79.23 or round(verdad_12, 2) != 3.80 or len(_vis) != 7099:
    raise SystemExit("PARADA DURA: [verdad_s5] no reproduce la verdad de la sesión 5")
# Sesgo esperado del % sin ponderar: con las tasas de respuesta del generador (genera_datos.py,
# _pedido: califica con probabilidad 0,80 si el tiempo pasa de 55 min y 0,58 si no)
_t55 = _datos_v["tiempo_entrega_min"] > 55
for _nombre, _ind, _verdad in [("4 o 5", lambda s: s >= 4, verdad_45), ("1 o 2", lambda s: s <= 2, verdad_12)]:
    _num = _den = 0.0
    for _g, _r in [(~_t55, 0.58), (_t55, 0.80)]:
        _num += _r * _g.sum() * _ind(_comp[_g]).mean()
        _den += _r * _g.sum()
    _esperado = _num / _den * 100
    _visto = _ind(_vis).mean() * 100
    print(f"{_nombre}: sin ponderar {_visto:.2f}; esperado {_esperado:.2f}; sesgo esperado "
          f"{_esperado - _verdad:+.2f} puntos; azar {_visto - _esperado:+.2f} puntos")
    _var = 0.0
    _pond_n = _pond_d = 0.0
    for _g in [~_t55, _t55]:
        _nh, _kh = _g.sum(), (_g & _cal_v).sum()
        _ph = _ind(_comp[_g]).mean()
        _var += (_nh / len(_datos_v)) ** 2 * _ph * (1 - _ph) / _kh * (1 - _kh / _nh)
        _pond_n += _nh * _ind(_vis[_g[_cal_v]]).mean()
        _pond_d += _nh
    _ee_p = math.sqrt(_var) * 100
    print(f"  ponderado {_pond_n / _pond_d * 100:.2f}; con la corrección por población finita (sesión 5), "
          f"EE {_ee_p:.3f} puntos; se aleja de la verdad {(_pond_n / _pond_d * 100 - _verdad) / _ee_p:+.2f} EE")

# %% cifras precalculo
# Cifras que las diapositivas y sus notas citan (no va al notebook)
import math
import time
datos = pd.read_csv("datos/pedidos.csv")
datos["calificacion"] = pd.Categorical(datos["calificacion"], categories=[1, 2, 3, 4, 5],
                                       ordered=True)
N = len(datos)
t = datos["tiempo_entrega_min"]
mu_ = t.mean()
sig = t.std(ddof=0)
print(f"tiempo: μ {mu_:.2f}, σ {sig:.2f} (ddof=0), s {t.std():.2f}, mediana {t.median():.1f}, "
      f"asimetría {t.skew():.2f}, máximo {t.max():.1f}; a una σ de μ {t.between(mu_ - sig, mu_ + sig).mean() * 100:.1f} %; "
      f"a una s (sesión 3) {t.between(mu_ - t.std(), mu_ + t.std()).mean() * 100:.1f} %")
_m400 = pd.Series([datos.sample(n=400, random_state=i)["tiempo_entrega_min"].mean() for i in range(1000)])
_ee400 = _m400.std()
print(f"1000 medias de 400: de {_m400.min():.2f} a {_m400.max():.2f}, media {_m400.mean():.2f}; EE simulado "
      f"{_ee400:.3f} (ddof=0 {_m400.std(ddof=0):.3f}); σ/√400 {sig / 20:.3f}; con la corrección por población "
      f"finita {sig / 20 * math.sqrt((N - 400) / (N - 1)):.3f}")
print(f"la más lejana de las 1000 medias de 400, a {(_m400 - mu_).abs().max():.2f} min de μ")
print(f"forma: a 1 EE de μ {((_m400 - mu_).abs() <= _ee400).mean() * 100:.1f} %; a 1,96 EE "
      f"{((_m400 - mu_).abs() <= 1.96 * _ee400).mean() * 100:.1f} %; asimetría de las medias {_m400.skew():.2f}")
for _n in [25, 100, 400]:
    _mn = pd.Series([t.sample(n=_n, random_state=i).mean() for i in range(1000)])
    print(f"n = {_n}: EE simulado {_mn.std():.2f}, fórmula {sig / math.sqrt(_n):.2f}, asimetría {_mn.skew():.2f}")
print(f"¿t.sample = pedidos.sample? {bool(np.allclose(_m400, [t.sample(n=400, random_state=i).mean() for i in range(1000)]))}")
print(f"1600 pedidos: σ/√1600 {sig / 40:.3f}; con la corrección por población finita "
      f"{sig / 40 * math.sqrt((N - 1600) / (N - 1)):.3f}; razón frente a 400 {sig / 40 * math.sqrt((N - 1600) / (N - 1)) / _ee400:.2f}; "
      f"1600 son el {1600 / N * 100:.0f} % de los pedidos")
# Métodos
_t0 = time.perf_counter()
_fe = datos["fecha"].drop_duplicates()
_met = {"simple": list(_m400), "estratificado": [], "conglomerados": [], "sistematico": []}
_tam = []
for i in range(1000):
    _met["estratificado"].append(datos.groupby("ciudad").sample(frac=1/30, random_state=i)["tiempo_entrega_min"].mean())
    _d = datos[datos["fecha"].isin(_fe.sample(n=6, random_state=i))]
    _met["conglomerados"].append(_d["tiempo_entrega_min"].mean())
    _tam.append(len(_d))
_met["sistematico"] = [t.iloc[k::30].mean() for k in range(30)]
_seg = time.perf_counter() - _t0
print("EE por método (np.std, ddof=0):", {k: round(float(np.std(v)), 3) for k, v in _met.items()},
      f"conglomerados de {min(_tam)} a {max(_tam)} pedidos; réplicas en menos de 10 s: {_seg < 10}")
_conv = datos[datos["ciudad"] == "Bogotá"].head(400)["tiempo_entrega_min"].mean()
print(f"conveniencia {_conv:.2f}; ruido de un EE simulado con 1000 réplicas ≈ ±{_ee400 / math.sqrt(2 * 999):.3f}")
# Una muestra e intervalos
_s1 = datos.sample(n=400, random_state=1)["tiempo_entrega_min"]
_e1 = _s1.std() / 20
print(f"semilla 1: x̄ {_s1.mean():.2f}, s {_s1.std():.2f}, EE {_e1:.3f}, margen {1.96 * _e1:.2f}, "
      f"IC [{_s1.mean() - 1.96 * _e1:.2f}; {_s1.mean() + 1.96 * _e1:.2f}]")


def _cobertura(semillas, con_sigma=False):
    debajo = encima = 0
    for i in semillas:
        x = datos.sample(n=400, random_state=i)["tiempo_entrega_min"]
        e = sig / 20 if con_sigma else x.std() / 20
        debajo += x.mean() + 1.96 * e < mu_
        encima += x.mean() - 1.96 * e > mu_
    total = len(semillas)
    return f"{(total - debajo - encima) / total * 100:.1f} % ({total - debajo - encima} de {total}; fallan {debajo} por debajo y {encima} por encima)"


print("cobertura, semillas 1 a 100:", _cobertura(range(1, 101)))
print("cobertura, semillas 0 a 999:", _cobertura(range(1000)))
_t0 = time.perf_counter()
print("cobertura, 20 000 intervalos:", _cobertura(range(20000)))
print("cobertura, 20 000 con σ conocida:", _cobertura(range(20000), con_sigma=True),
      f"(en menos de 60 s: {time.perf_counter() - _t0 < 60})")
_pr = [math.comb(100, k) * 0.95 ** k * 0.05 ** (100 - k) for k in range(101)]
print(f"de 100 intervalos al 95 %: P(91 a 99) = {sum(_pr[91:100]) * 100:.1f} %; P(≤ 90) = {sum(_pr[:91]) * 100:.1f} %; "
      f"P(100) = {_pr[100] * 100:.1f} %")
print("t de Student con 399 grados de libertad: 1,966 (OpenIntro 7.1; hecho externo)")
# Proporciones
_c = datos[datos["calificacion"].notna()]
_n = len(_c)
_ok = _c["calificacion"] >= 4
_p = _ok.mean()
_e = math.sqrt(_p * (1 - _p) / _n)
print(f"4 o 5: {_p * 100:.2f} % de {_n} calificados ({_n / N * 100:.1f} % de los pedidos); EE {_e * 100:.2f} "
      f"puntos; margen ±{1.96 * _e * 100:.2f}; IC [{(_p - 1.96 * _e) * 100:.2f}; {(_p + 1.96 * _e) * 100:.2f}]; "
      f"éxitos {_ok.sum()}, fracasos {(~_ok).sum()}")
_p12 = (_c["calificacion"] <= 2).mean()
_e12 = math.sqrt(_p12 * (1 - _p12) / _n)
print(f"1 o 2: {_p12 * 100:.2f} %; margen ±{1.96 * _e12 * 100:.2f}; IC [{(_p12 - 1.96 * _e12) * 100:.2f}; "
      f"{(_p12 + 1.96 * _e12) * 100:.2f}]")
print(f"margen con el doble de calificados ±{1.96 * math.sqrt(_p * (1 - _p) / (2 * _n)) * 100:.2f}; "
      f"con 100 000 respuestas ±{1.96 * math.sqrt(_p * (1 - _p) / 100000) * 100:.2f}; razón √2 = {math.sqrt(2):.3f}")
# Ponderado de la S5 y su margen (con el p̂ de cada grupo, sin corrección por población finita)
_m55 = t > 55
_k = datos["calificacion"].notna()
_var = 0.0
_pond_num = _pond_den = 0.0
for _g in [~_m55, _m55]:
    _nh, _kh = _g.sum(), (_g & _k).sum()
    _ph = (datos.loc[_g & _k, "calificacion"] >= 4).mean()
    _var += (_nh / N) ** 2 * _ph * (1 - _ph) / _kh
    _pond_num += _nh * _ph
    _pond_den += _nh
print(f"ponderado de la S5: 4 o 5 {_pond_num / _pond_den * 100:.2f} %, margen ±{1.96 * math.sqrt(_var) * 100:.2f} puntos")
# Semanas
_f = pd.to_datetime(datos["fecha"])
_sem = _f.dt.isocalendar().week.astype(int)
_gs = _ok.groupby(_sem[_c.index])
_ws = pd.DataFrame({"n": _gs.size(), "p": _gs.mean() * 100})
_ws["m"] = 1.96 * np.sqrt(_ws["p"] * (100 - _ws["p"]) / _ws["n"])
_ws["dias"] = _f.groupby(_sem).nunique()
_ws["lo"], _ws["hi"] = _ws["p"] - _ws["m"], _ws["p"] + _ws["m"]
_comp7 = _ws[_ws["dias"] == 7]
print(f"semanas: {len(_ws)}; completas {len(_comp7)}: de {_comp7['n'].min()} a {_comp7['n'].max()} calificados "
      f"(mediana {_comp7['n'].median():.0f}), márgenes de ±{_comp7['m'].min():.1f} a ±{_comp7['m'].max():.1f}")
for _s in _ws.index[_ws["dias"] < 7]:
    print(f"  semana {_s} incompleta: {_ws.loc[_s, 'dias']} días, {_ws.loc[_s, 'n']} calificados, "
          f"{_ws.loc[_s, 'p']:.1f} % ± {_ws.loc[_s, 'm']:.1f}")
_sin27 = _ws.drop(index=_ws.index[-1])
print(f"% por semana (sin la 27): de {_sin27['p'].min():.1f} (semana {_sin27['p'].idxmin()}) a "
      f"{_sin27['p'].max():.1f} (semana {_sin27['p'].idxmax()}); la 27: {_ws['p'].iloc[-1]:.1f}")
_fuera = list(_ws.index[(_ws["lo"] > _p * 100) | (_ws["hi"] < _p * 100)])
print(f"semanas cuyo IC no contiene {_p * 100:.2f}: {_fuera}; esperadas por azar en 27: {0.05 * 27:.2f}")
for _s in [13, 14, 20]:
    print(f"  semana {_s}: {_ws.loc[_s, 'p']:.2f} % (n = {_ws.loc[_s, 'n']}), IC [{_ws.loc[_s, 'lo']:.2f}; "
          f"{_ws.loc[_s, 'hi']:.2f}]; con un decimal {_ws.loc[_s, 'p']:.1f} [{_ws.loc[_s, 'lo']:.1f}; {_ws.loc[_s, 'hi']:.1f}]")
_tsem = t.groupby(_sem).mean()
_m45 = (t > 45).groupby(_sem).mean() * 100
print(f"semana 13: tiempo medio {_tsem[13]:.1f} min (puesto {int(_tsem.rank()[13])} de {len(_tsem)} de menor a mayor; "
      f"la más rápida, la {_tsem.idxmin()} con {_tsem.min():.1f}); más de 45 min {_m45[13]:.1f} % frente a "
      f"{(t > 45).mean() * 100:.1f} % del semestre")
print(f"margen de la diferencia entre dos semanas (√2 × margen mediano de las completas): ±{math.sqrt(2) * _comp7['m'].median():.1f}")
# Meses
_mes = _f.dt.month
_gm = _ok.groupby(_mes[_c.index])
_wm = pd.DataFrame({"n": _gm.size(), "p": _gm.mean() * 100})
_wm["m"] = 1.96 * np.sqrt(_wm["p"] * (100 - _wm["p"]) / _wm["n"])
_wm["lluvia"] = (datos["lluvia"] == "Sí").groupby(_mes).mean() * 100
_wm["tiempo"] = t.groupby(_mes).mean()
print("meses:", _wm.round(2).to_dict("index"))
print(f"meses: márgenes de ±{_wm['m'].min():.1f} a ±{_wm['m'].max():.1f}; calificados de {_wm['n'].min()} a {_wm['n'].max()}; "
      f"el más bajo {_wm['p'].idxmin()} ({_wm['p'].min():.1f} %, lluvia {_wm.loc[_wm['p'].idxmin(), 'lluvia']:.1f} %, "
      f"tiempo {_wm.loc[_wm['p'].idxmin(), 'tiempo']:.1f}); el más lluvioso {_wm['lluvia'].idxmax()}; el más alto "
      f"{_wm['p'].idxmax()} ({_wm['p'].max():.1f} %)")
# Ciudad y semana
_gcs = _ok.groupby([_c["ciudad"], _sem[_c.index]])
_cs = pd.DataFrame({"n": _gcs.size(), "e": _gcs.sum()})
_cs["f"] = _cs["n"] - _cs["e"]
_cs["ok"] = (_cs["e"] >= 10) & (_cs["f"] >= 10)
print(f"ciudad × semana: {len(_cs)} combinaciones; con 10 y 10: {_cs['ok'].sum()}; por ciudad "
      f"{_cs['ok'].groupby(level=0).sum().to_dict()}; mediana de calificados "
      f"{_cs['n'].groupby(level=0).median().to_dict()}")
_buc = _cs.loc["Bucaramanga"]
print(f"Bucaramanga: semanas con 100 % {int((_buc['f'] == 0).sum())}; calificados por semana de {_buc['n'].min()} a {_buc['n'].max()}")
_cb = _c[_c["ciudad"] == "Bucaramanga"]
_pb = (_cb["calificacion"] >= 4).mean()
print(f"Bucaramanga semestre: {_pb * 100:.1f} % de 4 o 5, n = {len(_cb)} ({len(_cb) / len(_ws):.1f} por semana en promedio, "
      f"mediana {_buc['n'].median():.0f}); para 10 fracasos hacen falta {math.ceil(10 / (1 - _pb))} calificados, "
      f"{10 / (1 - _pb) / _buc['n'].median():.1f} semanas")
_mes_c = _f.dt.month[_c.index]
_cm = _ok.groupby([_c["ciudad"], _mes_c]).agg(["size", "sum"])
_cm["f"] = _cm["size"] - _cm["sum"]
_cmok = (_cm["sum"] >= 10) & (_cm["f"] >= 10)
print(f"ciudad × mes: {int(_cmok.sum())} de {len(_cm)} con 10 y 10; sin cumplir: {_cm[~_cmok].to_dict('index')}")
print(f"Literary Digest: margen con 2 376 523 respuestas y p = 0,5: ±{1.96 * math.sqrt(0.25 / 2376523) * 100:.2f} puntos")
_v25 = [t.sample(n=25, random_state=i) for i in range(1000)]
print(f"n = 25, 1000 muestras: la varianza que divide entre n queda en promedio en el "
      f"{np.mean([v.var(ddof=0) for v in _v25]) / sig ** 2 * 100:.1f} % de σ²; la que divide entre n − 1, en el "
      f"{np.mean([v.var() for v in _v25]) / sig ** 2 * 100:.1f} %")
# Tamaño de muestra
_tam_n = lambda p, e: 1.96 ** 2 * p * (1 - p) / e ** 2
print(f"tamaño nacional: ±3 → {_tam_n(_p, 0.03):.2f} ({math.ceil(_tam_n(_p, 0.03))}, "
      f"{math.ceil(_tam_n(_p, 0.03)) / _comp7['n'].median():.1f} semanas); ±5 → {_tam_n(_p, 0.05):.2f} "
      f"({math.ceil(_tam_n(_p, 0.05))}, {math.ceil(_tam_n(_p, 0.05)) / _comp7['n'].median():.1f} semanas)")
_tasa = _n / N
print(f"400 llamadas: todos ±{1.96 * math.sqrt(_p * (1 - _p) / 400) * 100:.1f}; tasa {_tasa * 100:.1f} % → "
      f"{400 * _tasa:.1f} respuestas, ±{1.96 * math.sqrt(_p * (1 - _p) / (400 * _tasa)) * 100:.1f}")
_nb = _tam_n(_pb, 0.05)
print(f"Bucaramanga ±5: {_nb:.2f} → {math.ceil(_nb)} ({math.ceil(_nb) / _buc['n'].median():.1f} semanas con la mediana; "
      f"{_nb / (len(_cb) / len(_ws)):.1f} con el promedio); con p = 0,5: {_tam_n(0.5, 0.05):.2f} → {math.ceil(_tam_n(0.5, 0.05))}; "
      f"margen con 142: ±{1.96 * math.sqrt(_pb * (1 - _pb) / 142) * 100:.2f}; con 143: ±{1.96 * math.sqrt(_pb * (1 - _pb) / 143) * 100:.2f}")
# Pistas de revisar_tamano (ejercicio 3)
_pb_todos = (datos["calificacion"] >= 4)[datos["ciudad"] == "Bucaramanga"].mean()
print("pistas del ej. 3:", {
    "p̂ sobre todos los pedidos": round(_tam_n(_pb_todos, 0.05), 2), "p̂ nacional": round(_tam_n(_p, 0.05), 2),
    "E = 5 con p̂ en proporción": round(1.96 ** 2 * _pb * (1 - _pb) / 25, 4),
    "1,96 sin cuadrado": round(1.96 * _pb * (1 - _pb) / 0.0025, 2), "E sin cuadrado": round(1.96 ** 2 * _pb * (1 - _pb) / 0.05, 2),
    "el ancho": round(_tam_n(_pb, 0.025), 2), "z = 2": round(_tam_n(_pb, 0.05) / 1.96 ** 2 * 4, 2),
    "z = 1,645": round(_tam_n(_pb, 0.05) / 1.96 ** 2 * 1.645 ** 2, 2), "z = 2,576": round(_tam_n(_pb, 0.05) / 1.96 ** 2 * 2.576 ** 2, 2),
    "con raíz": round(math.sqrt(_tam_n(_pb, 0.05)), 2), "p̂ en % y E = 5": round(1.96 ** 2 * (_pb * 100) * (100 - _pb * 100) / 25, 2)})
# Pistas de revisar_intervalo (ejercicio 2)
_w20 = datos[_sem == 20]
_c20 = _w20[_w20["calificacion"].notna()]
_p20, _n20 = (_c20["calificacion"] >= 4).mean(), len(_c20)


def _ic(p, n, z=1.96):
    e = math.sqrt(p * (1 - p) / n)
    return [round((p - z * e) * 100, 2), round((p + z * e) * 100, 2)]


_pt = (_w20["calificacion"] >= 4).mean()
_w21 = datos[_sem == 21]
_c21 = _w21[_w21["calificacion"].notna()]
print("pistas del ej. 2:", {
    "correcto": _ic(_p20, _n20), "faltante como False": _ic(_pt, len(_w20)), "n = pedidos de la semana": _ic(_p20, len(_w20)),
    "pedidos de la semana": len(_w20), "n = 7099": _ic(_p20, _n), "n = 12 000": _ic(_p20, N),
    "sin raíz": [round((_p20 - 1.96 * _p20 * (1 - _p20) / _n20) * 100, 2), round((_p20 + 1.96 * _p20 * (1 - _p20) / _n20) * 100, 2)],
    "margen en proporción sumado al %": [round(_p20 * 100 - 1.96 * math.sqrt(_p20 * (1 - _p20) / _n20), 2),
                                         round(_p20 * 100 + 1.96 * math.sqrt(_p20 * (1 - _p20) / _n20), 2)],
    "z = 1,645": _ic(_p20, _n20, 1.645), "z = 2,576": _ic(_p20, _n20, 2.576), "z = 2": _ic(_p20, _n20, 2),
    "p̂ del semestre en el EE": [round((_p20 - 1.96 * math.sqrt(_p * (1 - _p) / _n20)) * 100, 2),
                                round((_p20 + 1.96 * math.sqrt(_p * (1 - _p) / _n20)) * 100, 2)],
    ">= 3": _ic((_c20["calificacion"] >= 3).mean(), _n20), "== 5": _ic((_c20["calificacion"] == 5).mean(), _n20),
    "> 4": _ic((_c20["calificacion"] > 4).mean(), _n20), "1 − p̂": _ic(1 - _p20, _n20), "±1 EE": _ic(_p20, _n20, 1),
    "semana 21 (%W = 20)": _ic((_c21["calificacion"] >= 4).mean(), len(_c21))})
print(f"semana 20: {_p20 * 100:.2f} % de {_n20} calificados ({len(_w20)} pedidos); %W = 20 es la ISO "
      f"{sorted(_sem[_f.dt.strftime('%W') == '20'].unique())}")
# Pistas de revisar_medias (ejercicio 1): con semillas mi_semilla + i, mi_semilla de 100 a 999


def _ventanas(f):
    v = np.array([f(s) for s in range(100, 1999)])
    ms = [v[a:a + 1000].mean() for a in range(900)]
    ss = [v[a:a + 1000].std(ddof=1) for a in range(900)]
    return f"media {min(ms):.3f}–{max(ms):.3f}, desviación {min(ss):.4f}–{max(ss):.4f}"


_t0 = time.perf_counter()
for _nombre, _f1 in [("n = 100", lambda s: t.sample(n=100, random_state=s).mean()),
                     ("n = 100 con replace=True", lambda s: t.sample(n=100, random_state=s, replace=True).mean()),
                     ("n = 400", lambda s: t.sample(n=400, random_state=s).mean()),
                     ("n = 25", lambda s: t.sample(n=25, random_state=s).mean()),
                     ("n = 10", lambda s: t.sample(n=10, random_state=s).mean()),
                     ("n = 80", lambda s: t.sample(n=80, random_state=s).mean()),
                     ("n = 120 o frac=0.01", lambda s: t.sample(n=120, random_state=s).mean()),
                     ("n = 1", lambda s: t.sample(n=1, random_state=s).mean()),
                     ("mediana (n = 100)", lambda s: t.sample(n=100, random_state=s).median()),
                     (".std() (n = 100)", lambda s: t.sample(n=100, random_state=s).std()),
                     (".sum() (n = 100)", lambda s: t.sample(n=100, random_state=s).sum())]:
    print(f"pista del ej. 1, {_nombre}: {_ventanas(_f1)}")
print(f"(ventanas del ej. 1 en menos de 30 s: {time.perf_counter() - _t0 < 30})")
_sol = [datos.sample(n=100, random_state=314 + i)["tiempo_entrega_min"].mean() for i in range(1000)]
print(f"solución del ej. 1 (semilla 314): media {np.mean(_sol):.2f}, EE {np.std(_sol, ddof=1):.2f}; fórmula "
      f"σ/√100 = {sig / 10:.2f}")
