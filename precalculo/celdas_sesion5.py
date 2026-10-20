# Fuente ÚNICA del código de la Sesión 5. De aquí salen:
#   - el notebook para Colab                    (notebook.py genera 5)
#   - las salidas y las gráficas que muestran las diapositivas
#                                               (notebook.py ejecuta 5 → salidas_sesion5.json y
#                                                fuente/diapositivas/recursos/s5/<id>.svg)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py, ayudas.py y
#               ayudas_sesion5.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar
#   precalculo  cifras que las diapositivas citan en el texto: se ejecuta, NO va al notebook

# %% [markdown]
# # Sesión 5 · La muestra que se eligió sola
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este cuaderno (*notebook*) acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-5-la-muestra-que-se-eligio-sola.html).
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
# Crea datos/pedidos.csv: los mismos 12 000 pedidos de las sesiones 1 a 4
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Los datos, con sus escalas
#
# Cargamos los pedidos y declaramos las escalas, como en las sesiones anteriores. Hoy también usamos
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
# ## La pregunta de hoy: ¿qué tan satisfecha está la clientela?
#
# La lista mínima del tablero pide el % de 4 o 5 estrellas: 79,1 %. Pero ¿79 % **de quiénes**? De los
# 7099 pedidos que se calificaron, el 59,2 % de los 12 000; el 40,8 % no calificó. Las calificaciones
# son una muestra que nadie diseñó: **se eligió sola**. Primero veremos cómo se diseña una muestra al
# azar; después, cómo corregir una que se eligió sola. Antes de la cifra, pregunta quién respondió.

# %% [markdown]
# ## 2 · Si la gerencia llamara a 400 pedidos, ¿a cuáles?
#
# La gerencia quiere llamar a 400 pedidos para preguntar por su satisfacción. Antes de elegir:
#
# - El **marco** es la lista de la que se sortea: aquí, `pedidos.csv`. Solo trae los pedidos
#   **entregados**: un pedido cancelado nunca podría salir en la muestra. Es un problema de **cobertura**.
# - La **unidad** es el pedido, no el cliente: la tabla no dice quién pidió.
# - Comparamos los métodos con el **tiempo de entrega** porque lo conocemos para todos los pedidos: su
#   media $\mu$ es el blanco al que debería apuntar cada muestra.
#
# En un muestreo **probabilístico**, cada pedido tiene una probabilidad conocida y mayor que cero de
# entrar. Eso es lo que permite inferir: la media de la muestra, $\bar x$, estima $\mu$. Cuánto puede
# alejarse de $\mu$ se mide en la sesión 6.
#
# ### Aleatorio simple
#
# Cualquier grupo de 400 pedidos tiene la misma probabilidad de salir. La **semilla** hace que la
# muestra se pueda repetir: con la misma semilla sale la misma muestra.

# %% mas
semilla = 1                     # la de la clase; cámbiala y compara
mu = pedidos["tiempo_entrega_min"].mean()   # el parámetro: lo conocemos
mas = pedidos.sample(n=400, random_state=semilla)
x_mas = mas["tiempo_entrega_min"].mean()
print(f"μ = {mu:.2f} min · x̄ = {x_mas:.2f} min")
print("De Bucaramanga:", (mas["ciudad"] == "Bucaramanga").sum(), "pedidos")

# %% [markdown]
# ### Sistemático
#
# Se elige un inicio al azar entre los primeros 30 pedidos y, desde ahí, uno de cada 30
# ($12\,000 / 400 = 30$). Funciona si el orden del archivo no tiene un ciclo que coincida con el paso.

# %% sistematico
paso = len(pedidos) // 400                # 12 000 / 400 = 30
inicio = np.random.default_rng(semilla).integers(paso)   # de 0 a 29
sistematica = pedidos.iloc[inicio::paso]  # uno de cada 30
x_sis = sistematica["tiempo_entrega_min"].mean()
print("Inicio:", inicio, "· pedidos:", len(sistematica))
print(f"x̄ = {x_sis:.2f} min")

# %% [markdown]
# ### Estratificado
#
# Se sortea **dentro de cada ciudad** la misma fracción, 1 de cada 30: cada ciudad entra con su parte.
#
# **Aviso:** en muestreo, un **estrato** es cualquier grupo que se sortea por separado; aquí, la ciudad.
# No es la columna `estrato`.

# %% estratificado
estratificada = pedidos.groupby("ciudad").sample(
    frac=1/30, random_state=semilla)      # 1 de cada 30 en cada ciudad
print("Pedidos:", len(estratificada))
pd.DataFrame({"estratificada": estratificada["ciudad"].value_counts(),
              "aleatoria simple": mas["ciudad"].value_counts()})

# %% [markdown]
# ### Por conglomerados
#
# Se sortean **grupos enteros**: 6 días al azar, con todos sus pedidos. Sirve cuando hay una lista de
# grupos (días, barrios, sucursales) y no una de unidades. El tamaño de la muestra depende de los días
# que salgan. Si se sortean grupos y después unidades dentro de cada grupo, el muestreo es **multietapa**.

# %% conglomerados
fechas = pedidos["fecha"].drop_duplicates()       # los 181 días
dias = fechas.sample(n=6, random_state=semilla)   # 6 días al azar
conglomerados = pedidos[pedidos["fecha"].isin(dias)]   # todos sus pedidos
print("Pedidos:", len(conglomerados))
conglomerados["fecha"].value_counts().sort_index()

# %% [markdown]
# ### ¿Qué tan cerca de $\mu$ cae cada una?
#
# Añadimos una muestra **por conveniencia**: los primeros 400 pedidos de Bogotá, los más a la mano.

# %% comparar
# Por conveniencia: los primeros 400 pedidos de Bogotá
conveniencia = pedidos[pedidos["ciudad"] == "Bogotá"].head(400)
muestras = {"Aleatoria simple": mas, "Sistemática": sistematica,
            "Estratificada": estratificada,
            "Por conglomerados": conglomerados,
            "Por conveniencia": conveniencia}
comparacion = pd.DataFrame({
    "pedidos": {m: len(d) for m, d in muestras.items()},
    "media": {m: d["tiempo_entrega_min"].mean()
              for m, d in muestras.items()}})
print(f"μ = {mu:.2f} min")
comparacion.round(2)

# %% metodos_grafica
colores = ["#F46201" if m == "Por conveniencia" else "#8A2E9E"
           for m in comparacion.index]
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.scatter(comparacion["media"], comparacion.index, s=110, color=colores,
           zorder=3)
for m, x in comparacion["media"].items():   # el valor, del lado de afuera
    lado = 1 if x > mu else -1
    ax.annotate(f"{x:.2f}", (x, m), xytext=(10 * lado, 0),
                textcoords="offset points", va="center",
                ha="left" if lado > 0 else "right")
filas = len(comparacion)
ax.vlines(mu, -0.5, filas - 0.5, color="#3A0F47", linewidth=2,
          linestyle="--")                   # la línea de μ
ax.text(mu, -0.9, f"μ = {mu:.2f} min (los 12 000 pedidos)", ha="left")
ax.set_ylim(filas - 0.5, -1.3)              # en el orden de la tabla
ax.set_xlim(comparacion["media"].min() - 1, comparacion["media"].max() + 1)
ax.set_title("La muestra por conveniencia cae lejos de μ")
ax.set_xlabel("Media del tiempo de entrega (min)")
plt.show()

# %% [markdown]
# Una sola muestra por método no dice cuál es más **precisa**: para eso hay que sacar muchas muestras
# de cada uno y ver cuánto varían. Es lo que haremos en la sesión 6.
#
# ### Los no probabilísticos
#
# - **Por conveniencia:** los que están a la mano, como los primeros 400 pedidos de Bogotá.
# - **Voluntario:** responde quien quiere. **La calificación de la app es una muestra voluntaria.**
# - **Por cuotas:** se llenan cupos por grupo (tantos de cada ciudad), pero dentro de cada cupo se
#   elige a mano, no al azar.
#
# Sin probabilidades conocidas no hay forma de medir cuánto puede alejarse $\bar x$ de $\mu$. Y más datos
# no lo arreglan: en 1936, la revista *Literary Digest* recibió más de dos millones de respuestas y se
# equivocó de ganador en la elección presidencial de los Estados Unidos (Squire, 1988, *Public Opinion
# Quarterly*).

# %% [markdown]
# ## 3 · ¿Quién calificó? Sesgo y no respuesta
#
# - El **error muestral** es azar: cambia de una muestra a otra y baja cuando crece $n$ (sesión 6).
# - El **sesgo** es sistemático: empuja siempre hacia el mismo lado y **no** baja cuando crece $n$.
#
# | Sesgo | Qué pasa |
# |---|---|
# | De **cobertura** | El marco deja fuera a una parte de la población |
# | De **selección** o **autoselección** | Quien entra a la muestra no se parece al resto |
# | De **no respuesta** | Quien no responde no se parece a quien sí |
# | De **medición** | La pregunta o el instrumento miden mal |
#
# La calificación mezcla dos: la app se la pide a **todos** los pedidos y solo algunos responden. Como
# de todos sabemos el tiempo, la tratamos como **no respuesta**: veremos de qué depende y cómo
# corregirla.
#
# ### ¿Quién califica?
#
# `calificacion` está vacía en los pedidos que no se calificaron. Partimos el tiempo de entrega en
# tramos con cortes explícitos y contamos qué parte de cada tramo se calificó.

# %% tasa_tiempo
tramo = pd.cut(pedidos["tiempo_entrega_min"],
               bins=[0, 15, 25, 35, 45, 55, 65, 210],
               labels=["hasta 15", "15–25", "25–35", "35–45", "45–55",
                       "55–65", "más de 65"])
califico = pedidos["calificacion"].notna()       # True si calificó
tasa = califico.groupby(tramo, observed=True).mean() * 100
print(pd.DataFrame({"pedidos": tramo.value_counts(sort=False),
                    "% calificado": tasa.round(1)}))
fig, ax = plt.subplots()
etiquetas = tasa.index.astype(str)
ax.bar(etiquetas[:5], tasa.values[:5], color="#8A2E9E",
       label="55 min o menos")
ax.bar(etiquetas[5:], tasa.values[5:], color="#F46201",
       label="Más de 55 min")
ax.axhline(califico.mean() * 100, color="#3A0F47", linewidth=2,
           linestyle="--",
           label=f"Todos los pedidos: {califico.mean() * 100:.1f} %")
ax.set_ylim(0, 100)                        # las barras empiezan en cero
ax.legend(loc="upper left")
ax.set_title("Los pedidos de más de 55 min se califican más")
ax.set_xlabel("Tiempo de entrega (min)")
ax.set_ylabel("% de pedidos calificados")
plt.show()

# %% [markdown]
# ¿Cambia la tasa de calificación con la ciudad, la suscripción o la lluvia?

# %% tasa_grupos
tasa_grupos = pd.concat({
    columna: califico.groupby(pedidos[columna]).mean() * 100
    for columna in ["ciudad", "suscriptor", "lluvia"]})
tasa_grupos.round(1)

# %% [markdown]
# Por ciudad, suscripción o lluvia, la tasa va de 57,6 a 59,9 %: casi no cambia. De estas columnas,
# ninguna la mueve como el tiempo.
#
# ### Tres tipos de faltantes
#
# | Si la calificación falta… | Qué pasa | Qué se hace |
# |---|---|---|
# | **completamente al azar** | Solo se pierde $n$ | Nada: los calificados se parecen a todos |
# | **según algo que vemos** (en Tingua, el tiempo) | Los calificados no se parecen a todos, pero sabemos en qué | Se **pondera** |
# | **según lo que no vemos** (por ejemplo, que con el mismo tiempo califiquen más los pedidos de clientes muy molestos) | Ninguna columna lo revela | Hay que salir a preguntar: sortear algunos pedidos sin calificación y llamar hasta obtener su respuesta |
#
# En inglés se llaman MCAR, MAR y MNAR. Ponderar por el tiempo funciona porque el tiempo se conoce
# **también** para los pedidos sin calificación. La tasa de calificación muestra de qué variable
# **observada** depende la no respuesta; que no dependa también de lo que no vemos es un **supuesto**
# que en la vida real no se puede comprobar.
#
# ### Pocos pedidos, mucho peso en la insatisfacción (1 o 2 estrellas)

# %% quien_pesa
mas_55 = pedidos["tiempo_entrega_min"] > 55
calificados = pedidos[califico]               # solo los que calificaron
baja = calificados["calificacion"] <= 2       # 1 o 2 estrellas
partes = pd.Series({
    "Pedidos": mas_55.mean() * 100,
    "Calificaciones": mas_55[califico].mean() * 100,
    "De 1 o 2 estrellas": mas_55[califico][baja].mean() * 100})
print(partes.round(1))
fig, ax = plt.subplots()
ax.bar(partes.index, partes.values, color="#F46201")
for i, v in enumerate(partes.values):         # el valor sobre cada barra
    ax.text(i, v + 2, f"{v:.1f} %", ha="center")
ax.set_ylim(0, 100)
ax.set_title("Más de 55 min: pocos pedidos, mucho peso en el 1 o 2")
ax.set_ylabel("% que son de más de 55 min")
plt.show()

# %% [markdown]
# Los de más de 55 min son el 3,5 % de los pedidos, el 4,8 % de las calificaciones y el 63,1 % de las de
# 1 o 2 estrellas. Dominan la insatisfacción sobre todo porque esperar más trae calificaciones bajas;
# como además se califican más, pesan de más: ese exceso es el sesgo que la ponderación quita.
#
# ### Ponderar
#
# Si la no respuesta depende **solo** del tiempo (y no de lo que no vemos), dentro de cada grupo de
# tiempo los pedidos sin calificación se parecen a los calificados: ese es el supuesto. El **peso** de
# cada grupo es pedidos entre calificados: a cuántos pedidos representa cada calificación. La
# proporción ponderada es
#
# $$\hat p_w = \frac{\sum w_i\, y_i}{\sum w_i}$$
#
# La suma va **solo sobre los calificados**; $w_i$ es el peso del grupo del pedido $i$, y $y_i = 1$ si el
# pedido tiene 1 o 2 estrellas (y 0 si no). Es la misma idea de un estratificado con distinta fracción
# en cada estrato. Con estos pesos, los de más de 55 min vuelven a pesar lo que pesan entre los
# pedidos: el 3,5 %, no el 4,8 % de las calificaciones.
#
# El grupo se arma con `np.where`, un texto por pedido. La línea `datos = pedidos` va sola a
# propósito: en el ejercicio 2 solo cambia esa.

# %% ponderar
datos = pedidos              # ejercicio 2: solo cambia esta línea
grupo = pd.Series(np.where(datos["tiempo_entrega_min"] > 55,
                           "más de 55 min", "55 min o menos"),
                  index=datos.index)
calificado = datos["calificacion"].notna()
peso = grupo.value_counts() / grupo[calificado].value_counts()
print("Pesos:", peso.round(2).to_dict())
w = grupo[calificado].map(peso)       # el peso de cada calificado
estrellas = datos.loc[calificado, "calificacion"]
y = (estrellas <= 2).astype(int)      # 1 si tiene 1 o 2 estrellas
sin_ponderar = y.mean() * 100
ponderado = (w * y).sum() / w.sum() * 100
print(f"1 o 2 estrellas: {sin_ponderar:.2f} % → {ponderado:.2f} %")
y45 = (estrellas >= 4).astype(int)    # 1 si tiene 4 o 5 estrellas
print(f"4 o 5 estrellas: {y45.mean() * 100:.2f} % → "
      f"{(w * y45).sum() / w.sum() * 100:.2f} %")

# %% [markdown]
# ### La comprobación, solo posible en un caso ficticio
#
# Tingua es inventado: el generador sabe qué calificación habría dado **cada** pedido. La función
# `calificacion_completa()`, que está en la celda oculta, la recupera: devuelve una serie indexada por
# `id_pedido`, que se cruza con `map` por código.
#
# **En la vida real esta celda no existe: no la uses en el tablero.**

# %% comprobacion
completa = pedidos["id_pedido"].map(calificacion_completa())  # por código
print(f"1 o 2: {sin_ponderar:.2f} % sin ponderar · "
      f"{ponderado:.2f} % ponderado · "
      f"{(completa <= 2).mean() * 100:.2f} % de verdad")

# %% [markdown]
# En el 1 o 2, ponderar acercó la cifra a la verdad: de 4,39 a 3,66 %, con la verdad en 3,80 %. ¿Y en el
# 4 o 5?

# %% comprobacion_45
print(f"4 o 5: {y45.mean() * 100:.2f} % sin ponderar · "
      f"{(w * y45).sum() / w.sum() * 100:.2f} % ponderado · "
      f"{(completa >= 4).mean() * 100:.2f} % de verdad")

# %% [markdown]
# Ponderar quita el sesgo que depende de lo que vemos, no el azar. En el 4 o 5, el azar de quién
# calificó dentro del grupo de 55 min o menos empujaba hacia el lado contrario del sesgo y, por
# suerte, casi lo compensaba en la cifra sin ponderar; al quitar el sesgo, quedó solo el azar.
# Medir ese azar es el tema de la sesión 6.
#
# ### La respuesta a la gerencia
#
# Estimamos que cerca de 8 de cada 10 pedidos tendrían 4 o 5 estrellas, si, dentro de cada grupo de
# tiempo, los pedidos sin calificación se parecen a los calificados. La insatisfacción es menor de lo
# que dicen las calificaciones: ponderada, baja de 4,4 % a 3,7 %.
#
# ## 4 · Para tu tablero
#
# El indicador de satisfacción **no cambia**: el % de 4 o 5 estrellas entre los pedidos calificados,
# mostrando cuántos se calificaron. Lo recomendable es mostrar la **tasa de calificación** de cada
# semana y advertir en la nota sobre los datos que el % es solo de los calificados. Ponderar es
# opcional. Esta celda calcula la tasa por semana ISO y marca las
# semanas incompletas; no tiene verificador. Mira el rango que imprime: una semana con unos puntos
# menos de tasa no es una tendencia. No conviertas ruido en noticia.

# %% semanas_calificacion
fecha = pd.to_datetime(pedidos["fecha"])
semana = fecha.dt.isocalendar().week.rename("semana")   # lunes a domingo
por_semana = pd.DataFrame({
    "pedidos": pedidos.groupby(semana).size(),
    "calificados": califico.groupby(semana).sum(),
    "dias": fecha.groupby(semana).nunique()})
por_semana["% calificado"] = (por_semana["calificados"]
                              / por_semana["pedidos"] * 100).round(1)
por_semana["completa"] = por_semana["dias"] == 7
print("De", por_semana["% calificado"].min(), "a",
      por_semana["% calificado"].max(), "% según la semana")
por_semana

# %% [markdown]
# ---
# # Práctica guiada
#
# Tres ejercicios; el tercero es **opcional** (o para la casa). Cada celda termina con un verificador
# que dice qué está bien y, en lo demás, te da una pista sin darte la respuesta. Reemplaza cada `...`
# y ejecuta; puedes repetir la celda las veces que quieras. Las respuestas escritas van al final, en
# «Tus respuestas»: esas no las revisa ningún verificador.
#
# ## Ejercicio 1 · Una muestra estratificada proporcional
#
# Saca una muestra estratificada por ciudad con el **2 %** de los pedidos de cada ciudad. Pista: la
# celda [estratificado].
#
# - `frac=` es una proporción: el 2 % se escribe `0.02`, no `2`.
# - `n=` es un número de pedidos por grupo. No uses `frac=` y `n=` a la vez.
# - Cambia `mi_semilla` por un número de tres cifras que elijas tú.
#
# Después responde abajo: con una aleatoria simple de 240 pedidos (sin agrupar), ¿cuántos de
# Bucaramanga esperarías? ¿Saldrían siempre 24? ¿Por qué tu estratificada sí trae siempre el mismo
# número, con cualquier semilla?

# %% ej1 plantilla
mi_semilla = 123   # cámbiala por un número de tres cifras que elijas tú
# 2 % = 0.02: frac=0.02 saca el 2 % de cada grupo
muestra = ...      # agrupa por ciudad y saca el 2 % de cada una
revisar_estratificada(muestra)

# %% ej1_solucion solucion
mi_semilla = 314
muestra = pedidos.groupby("ciudad").sample(frac=0.02,
                                           random_state=mi_semilla)
revisar_estratificada(muestra)

# %% [markdown]
# ## Ejercicio 2 · La insatisfacción de Bogotá, ponderada
#
# Repite la ponderación solo con los pedidos de **Bogotá**, con sus propios pesos. La celda es la de
# [ponderar]: cambia **solo** la línea `datos =`. Deja la última línea como está: entrega cada valor,
# en %, con su nombre.
#
# Después responde abajo: en **puntos**, la corrección de Bogotá casi duplica la del total; en
# proporción, las dos se parecen (18 % y 17 %). ¿Por qué en puntos es mayor? Pista: ¿qué parte de los
# pedidos de Bogotá pasa de 55 min, frente al 3,5 % del total? Y en una celda nueva escribe `w.sum()`:
# ¿por qué da justo el número de pedidos de Bogotá?

# %% ej2 plantilla
datos = pedidos       # ← cambia esta línea: solo los pedidos de Bogotá
grupo = pd.Series(np.where(datos["tiempo_entrega_min"] > 55,
                           "más de 55 min", "55 min o menos"),
                  index=datos.index)
calificado = datos["calificacion"].notna()
peso = grupo.value_counts() / grupo[calificado].value_counts()
print("Pesos:", peso.round(2).to_dict())
w = grupo[calificado].map(peso)       # el peso de cada calificado
estrellas = datos.loc[calificado, "calificacion"]
y = (estrellas <= 2).astype(int)      # 1 si tiene 1 o 2 estrellas
sin_ponderar = y.mean() * 100
ponderado = (w * y).sum() / w.sum() * 100
revisar_ponderada(sin_ponderar=sin_ponderar, ponderado=ponderado)

# %% ej2_solucion solucion
datos = pedidos[pedidos["ciudad"] == "Bogotá"]
grupo = pd.Series(np.where(datos["tiempo_entrega_min"] > 55,
                           "más de 55 min", "55 min o menos"),
                  index=datos.index)
calificado = datos["calificacion"].notna()
peso = grupo.value_counts() / grupo[calificado].value_counts()
print("Pesos:", peso.round(2).to_dict())
w = grupo[calificado].map(peso)
estrellas = datos.loc[calificado, "calificacion"]
y = (estrellas <= 2).astype(int)
sin_ponderar = y.mean() * 100
ponderado = (w * y).sum() / w.sum() * 100
revisar_ponderada(sin_ponderar=sin_ponderar, ponderado=ponderado)

# %% [markdown]
# ## Ejercicio 3 (opcional) · Una muestra por conglomerados
#
# Elige 6 días al azar con tu semilla y quédate con **todos** sus pedidos. Pista: la celda
# [conglomerados]. Deja la última línea como está.
#
# Después responde abajo: el verificador dice a cuántos minutos de $\mu$ quedó tu $\bar x$; la muestra
# por conveniencia quedó a 3,98. ¿Cuál de las dos diferencias es error muestral y cuál es sesgo? ¿Cuál
# se achicaría con una muestra más grande?

# %% ej3 plantilla
mi_semilla = 123        # la tuya, de tres cifras
dias = ...              # 6 días al azar
muestra_dias = ...      # todos los pedidos de esos días
revisar_conglomerados(muestra_dias)

# %% ej3_solucion solucion
mi_semilla = 314
dias = pedidos["fecha"].drop_duplicates().sample(n=6,
                                                 random_state=mi_semilla)
muestra_dias = pedidos[pedidos["fecha"].isin(dias)]
revisar_conglomerados(muestra_dias)

# %% [markdown]
# ### Tus respuestas
#
# *Doble clic para escribir aquí.*
#
# 1. Ejercicio 1: con una aleatoria simple de 240 esperaría unos … de Bucaramanga, pero …; mi
#    estratificada trae siempre el mismo número porque …
# 2. Ejercicio 2: en puntos, la corrección de Bogotá es mayor porque …; en proporción …; `w.sum()` da …
#    porque …
# 3. Ejercicio 3: mi $\bar x$ quedó a … min de $\mu$; es error muestral (o sesgo) porque …; la de
#    conveniencia, a 3,98, es … porque …; con una muestra más grande se achicaría …
# 4. En la comprobación, ponderar alejó el 4 o 5 de la verdad (79,07 → 80,09 %, con la verdad en
#    79,23 %). ¿Quiere decir que no había que ponderar? ¿Qué quita la ponderación y qué no? …
# 5. Autoevaluación. En otra app de domicilios, ¿qué tipo de faltante es cada uno, y qué harías?
#    - Los pedidos que llegan con algo dañado casi nunca se califican; la app no registra daños: …
#    - De noche se califica menos que de día: …
#    - Una falla borró las calificaciones de los pedidos cuyo código termina en 7: …
#    - Quien paga en efectivo califica menos que quien usa tarjeta: …

# %% cifras precalculo
# Cifras que las diapositivas y sus notas citan (no va al notebook)
import time
datos = pd.read_csv("datos/pedidos.csv")
datos["calificacion"] = pd.Categorical(datos["calificacion"], categories=[1, 2, 3, 4, 5],
                                       ordered=True)
n = len(datos)
t = datos["tiempo_entrega_min"]
cal = datos["calificacion"].notna()
m55 = t > 55
print(f"calificados {cal.sum()} de {n} ({cal.mean() * 100:.1f} %); sin calificar "
      f"{n - cal.sum()} ({(~cal).mean() * 100:.1f} %)")
c_ = datos[cal]
b12 = c_["calificacion"] <= 2
print(f"más de 55 min: {m55.sum()} pedidos ({m55.mean() * 100:.1f} %); calificados {(m55 & cal).sum()} "
      f"= {(m55 & cal).sum() / cal.sum() * 100:.1f} % de las calificaciones; de 1 o 2 estrellas: "
      f"{b12.sum()} en total, {(b12 & (c_['tiempo_entrega_min'] > 55)).sum()} de más de 55 min "
      f"({(b12 & (c_['tiempo_entrega_min'] > 55)).sum() / b12.sum() * 100:.1f} %); tasa de calificación "
      f"{(m55 & cal).sum() / m55.sum() * 100:.1f} % (más de 55) y "
      f"{(~m55 & cal).sum() / (~m55).sum() * 100:.1f} % (55 o menos)")
tr = pd.cut(t, bins=[0, 15, 25, 35, 45, 55, 65, 210])
tt = pd.DataFrame({"pedidos": tr.value_counts(sort=False),
                   "calificados": cal.groupby(tr, observed=True).sum(),
                   "%": (cal.groupby(tr, observed=True).mean() * 100).round(1)})
print("tasa por tramo:", tt.to_dict("index"))
rangos = [cal.groupby(datos[c]).mean() * 100 for c in ["ciudad", "suscriptor", "lluvia"]]
print(f"tasa por ciudad, suscriptor o lluvia: de {min(r.min() for r in rangos):.1f} a "
      f"{max(r.max() for r in rangos):.1f} %")
print(f"entre los calificados: 4 o 5 {(c_['calificacion'] >= 4).mean() * 100:.2f} % "
      f"({(c_['calificacion'] >= 4).mean() * 100:.1f}); 1 o 2 {b12.mean() * 100:.2f} % "
      f"({b12.mean() * 100:.1f}); 3 estrellas {(c_['calificacion'] == 3).mean() * 100:.2f} %")


def _pondera(d, mayor_igual=False, pesos=None):
    """Proporciones sin ponderar y ponderadas (en %) y las variantes erróneas del ejercicio 2."""
    marca = d["tiempo_entrega_min"] >= 55 if mayor_igual else d["tiempo_entrega_min"] > 55
    g = pd.Series(np.where(marca, "más de 55 min", "55 min o menos"), index=d.index)
    k = d["calificacion"].notna()
    p_ = g.value_counts() / g[k].value_counts() if pesos is None else pesos
    w_ = g[k].map(p_)
    e_ = d.loc[k, "calificacion"]
    y12, y45_ = (e_ <= 2).astype(int), (e_ >= 4).astype(int)
    return {"pesos": p_.to_dict(), "s12": y12.mean() * 100,
            "p12": (w_ * y12).sum() / w_.sum() * 100, "s45": y45_.mean() * 100,
            "p45": (w_ * y45_).sum() / w_.sum() * 100,
            "den_todos": (w_ * y12).sum() / g.map(p_).sum() * 100,
            "den_pedidos": y12.sum() / len(d) * 100,
            "invertidos": ((1 / w_) * y12).sum() / (1 / w_).sum() * 100,
            "entre_calificados": (w_ * y12).sum() / k.sum() * 100,
            "media_estrellas": e_.astype(int).mean(),
            "media_ponderada": (w_ * e_.astype(int)).sum() / w_.sum()}


def _redondo(r):
    return {k: (round(float(v), 2) if not isinstance(v, dict) else
                {a: round(b, 2) for a, b in v.items()}) for k, v in r.items()}


nac = _pondera(datos)
print("nacional:", _redondo(nac))
print(f"nacional con ≥ 55: 1 o 2 ponderado {_pondera(datos, True)['p12']:.2f}")
print(f"baja del 1 o 2 al ponderar: {nac['s12'] - nac['p12']:.2f} puntos, "
      f"{(nac['s12'] - nac['p12']) / nac['s12'] * 100:.0f} % en proporción; sube el 4 o 5 "
      f"{nac['p45'] - nac['s45']:.2f} puntos")
t0 = time.perf_counter()
comp1 = calificacion_completa()
segundos = time.perf_counter() - t0
comp2 = calificacion_completa()
ver = datos["id_pedido"].map(comp1)
vis = datos.loc[cal, "calificacion"].astype(int)
print(f"calificación completa: {len(comp1)} pedidos, {segundos:.2f} s, reproducible "
      f"{comp1.equals(comp2)}, coincide con las {len(vis)} visibles "
      f"{bool((ver[cal] == vis).all())}, tipo {comp1.dtype}")
print(f"verdad: 4 o 5 {(ver >= 4).mean() * 100:.2f} %, 1 o 2 {(ver <= 2).mean() * 100:.2f} %; "
      f"entre los que no calificaron: 4 o 5 {(ver[~cal] >= 4).mean() * 100:.2f} %, "
      f"1 o 2 {(ver[~cal] <= 2).mean() * 100:.2f} %")
for nombre, ind, est in [("4 o 5", lambda s: s >= 4, nac["p45"]), ("1 o 2", lambda s: s <= 2, nac["p12"])]:
    var = 0.0
    for marca in [~m55, m55]:
        nh, kh = marca.sum(), (marca & cal).sum()
        ph = ind(ver[marca]).mean()
        var += (nh / n) ** 2 * ph * (1 - ph) / kh * (1 - kh / nh)
    ee = np.sqrt(var) * 100
    print(f"{nombre}: error estándar del ponderado {ee:.3f} puntos; el ponderado se aleja "
          f"{est - ind(ver).mean() * 100:+.2f} puntos de la verdad = {(est - ind(ver).mean() * 100) / ee:+.2f} "
          f"errores estándar")
bog = datos[datos["ciudad"] == "Bogotá"]
rb = _pondera(bog)
vb = bog["id_pedido"].map(comp1)
print(f"Bogotá: {len(bog)} pedidos, {bog['calificacion'].notna().sum()} calificados, "
      f"{(bog['tiempo_entrega_min'] > 55).sum()} de más de 55 min (de {m55.sum()}); "
      f"verdad 1 o 2 {(vb <= 2).mean() * 100:.2f} %, 4 o 5 {(vb >= 4).mean() * 100:.2f} %")
print("Bogotá (clave del ejercicio 2):", _redondo(rb))
print(f"Bogotá con ≥ 55: ponderado {_pondera(bog, True)['p12']:.2f}; con los pesos nacionales: "
      f"{_pondera(bog, pesos=pd.Series(nac['pesos']))['p12']:.2f}")
acerca12, acerca45 = [], []
for c, d in datos.groupby("ciudad"):
    r = _pondera(d)
    v = d["id_pedido"].map(comp1)
    v12, v45 = (v <= 2).mean() * 100, (v >= 4).mean() * 100
    a12 = abs(r["p12"] - v12) < abs(r["s12"] - v12)
    a45 = abs(r["p45"] - v45) < abs(r["s45"] - v45)
    acerca12.append(a12)
    acerca45.append(a45)
    print(f"  {c}: 1 o 2 {r['s12']:.3f} → {r['p12']:.3f} (verdad {v12:.3f}, acerca {a12}); "
          f"4 o 5 {r['s45']:.2f} → {r['p45']:.2f} (verdad {v45:.2f}, acerca {a45})")
print(f"por ciudad, ponderar acerca el 1 o 2 en {sum(acerca12)} de 5 y el 4 o 5 en {sum(acerca45)} de 5")
print(f"μ = {t.mean():.2f}; conveniencia (primeros 400 de Bogotá) {bog.head(400)['tiempo_entrega_min'].mean():.2f}; "
      f"media de Bogotá {bog['tiempo_entrega_min'].mean():.2f}; paso {n // 400}")
cuenta = datos["ciudad"].value_counts()
print("pedidos por ciudad:", cuenta.to_dict())
print("estratificada 2 % por ciudad (clave del ejercicio 1):", (cuenta * 0.02).round().astype(int).to_dict(),
      f"total {int((cuenta * 0.02).round().sum())}; 1/30: {(cuenta / 30).round().astype(int).to_dict()} "
      f"total {int((cuenta / 30).round().sum())}")
buc = [int((datos.sample(n=400, random_state=s)["ciudad"] == "Bucaramanga").sum())
       for s in range(100, 1000)]
print(f"aleatoria simple de 400, pedidos de Bucaramanga con semillas de 100 a 999: de {min(buc)} a {max(buc)}")
fe = datos["fecha"].drop_duplicates()
tam = [int(datos["fecha"].isin(fe.sample(n=6, random_state=s)).sum()) for s in range(100, 1000)]
tam0 = [int(datos["fecha"].isin(fe.sample(n=6, random_state=s)).sum()) for s in range(0, 1000)]
print(f"conglomerados de 6 días: semillas 100–999 de {min(tam)} a {max(tam)} pedidos; 0–999 de "
      f"{min(tam0)} a {max(tam0)}; pedidos por día de {datos['fecha'].value_counts().min()} a "
      f"{datos['fecha'].value_counts().max()}; días {len(fe)}")
f_ = pd.to_datetime(datos["fecha"])
sem = f_.dt.isocalendar().week
dias_ = f_.groupby(sem).nunique()
ts = cal.groupby(sem).mean() * 100
print(f"semanas: {len(ts)}; tasa de calificación de {ts.min():.1f} % (semana {ts.idxmin()}) a "
      f"{ts.max():.1f} % (semana {ts.idxmax()}); incompletas {list(dias_[dias_ < 7].index)} con "
      f"{[round(v, 1) for v in ts[dias_ < 7]]} %; completas de {ts[dias_ == 7].min():.1f} a {ts[dias_ == 7].max():.1f}")
q_ = datos.assign(sem=sem, m=m55, mc=m55 & cal).groupby(["ciudad", "sem"]).agg(m=("m", "sum"),
                                                                               mc=("mc", "sum"))
print(f"ciudad × semana: {len(q_)} combinaciones; con pedidos de más de 55 min {(q_['m'] > 0).sum()}; "
      f"con alguno y ninguno calificado {((q_['m'] > 0) & (q_['mc'] == 0)).sum()}")
print(f"8 de cada 10: ponderado 4 o 5 = {nac['p45'] / 10:.1f} de cada 10")
tq1_, tq3_ = t.quantile(0.25), t.quantile(0.75)
print(f"valla superior del tiempo (sesión 4): {tq3_ + 1.5 * (tq3_ - tq1_):.2f} min")
print(f"tasa de calificación con dos decimales: más de 55 {(m55 & cal).sum()} de {m55.sum()} = "
      f"{(m55 & cal).sum() / m55.sum() * 100:.2f} %; 55 o menos {(~m55 & cal).sum()} de {(~m55).sum()} = "
      f"{(~m55 & cal).sum() / (~m55).sum() * 100:.2f} %")
print(f"Bucaramanga: {cuenta['Bucaramanga']} / 30 = {cuenta['Bucaramanga'] / 30:.1f}; "
      f"× 0.02 = {cuenta['Bucaramanga'] * 0.02:.1f}")
por_fecha = datos.groupby("fecha").size()
dia_sem = pd.to_datetime(por_fecha.index).dayofweek
print(f"pedidos por día: de viernes a domingo {por_fecha[dia_sem >= 4].mean():.1f} en promedio; "
      f"de lunes a jueves {por_fecha[dia_sem < 4].mean():.1f}")
# Revisión del 19 de octubre: cifras nuevas de las diapositivas, sus notas y el notebook
m55c = c_["tiempo_entrega_min"] > 55
w12 = np.where(m55c, nac["pesos"]["más de 55 min"], nac["pesos"]["55 min o menos"])
print(f"de las 1 o 2, % de más de 55 min: {(b12 & m55c).sum() / b12.sum() * 100:.1f} sin ponderar y "
      f"{(w12 * (b12 & m55c)).sum() / (w12 * b12).sum() * 100:.1f} ponderado; diferencia "
      f"{((b12 & m55c).sum() / b12.sum() - (w12 * (b12 & m55c)).sum() / (w12 * b12).sum()) * 100:.1f} puntos")
print(f"parte ponderada de los de más de 55 min entre los calificados: {(w12 * m55c).sum() / w12.sum() * 100:.2f} % "
      f"(sin ponderar {m55c.mean() * 100:.2f} %; entre los pedidos {m55.mean() * 100:.2f} %)")
print(f"Bogotá: más de 55 min {(bog['tiempo_entrega_min'] > 55).sum()} de {len(bog)} = "
      f"{(bog['tiempo_entrega_min'] > 55).mean() * 100:.1f} % (total {m55.mean() * 100:.1f} %); corrección del 1 o 2 "
      f"{rb['s12'] - rb['p12']:.2f} puntos = {(rb['s12'] - rb['p12']) / rb['s12'] * 100:.1f} % en proporción; "
      f"total {nac['s12'] - nac['p12']:.2f} puntos = {(nac['s12'] - nac['p12']) / nac['s12'] * 100:.1f} %; "
      f"razón de puntos {(rb['s12'] - rb['p12']) / (nac['s12'] - nac['p12']):.2f}")
_gb = pd.Series(np.where(bog["tiempo_entrega_min"] > 55, "más de 55 min", "55 min o menos"), index=bog.index)
_kb = bog["calificacion"].notna()
print(f"Bogotá: suma de los pesos w = {_gb[_kb].map(_gb.value_counts() / _gb[_kb].value_counts()).sum():.2f} "
      f"(pedidos de Bogotá {len(bog)})")
tr7 = pd.cut(t, bins=[0, 15, 25, 35, 45, 55, 65, 210])
p7 = tr7.value_counts() / tr7[cal].value_counts()
w7 = tr7[cal].map(p7).astype(float)
print(f"ponderando por los siete tramos: 1 o 2 {(w7 * b12).sum() / w7.sum() * 100:.2f} %, "
      f"4 o 5 {(w7 * (c_['calificacion'] >= 4)).sum() / w7.sum() * 100:.2f} %")
lejos = []
for s_ in range(100, 1000):
    i_ = np.random.default_rng(s_).integers(30)
    xs = [datos.sample(n=400, random_state=s_)["tiempo_entrega_min"].mean(),
          t.iloc[i_::30].mean(),
          datos.groupby("ciudad").sample(frac=1/30, random_state=s_)["tiempo_entrega_min"].mean(),
          t[datos["fecha"].isin(fe.sample(n=6, random_state=s_))].mean()]
    lejos.append(max(abs(x - t.mean()) for x in xs))
lejos = np.array(lejos)
print(f"semillas 100–999: la más lejana de las cuatro al azar, a {lejos.max():.2f} min de μ; alguna a más de "
      f"1 min en el {(lejos > 1).mean() * 100:.0f} % de las semillas; la de conveniencia, siempre a "
      f"{bog.head(400)['tiempo_entrega_min'].mean() - t.mean():.2f}")
buc240 = [int((datos.sample(n=240, random_state=s)["ciudad"] == "Bucaramanga").sum()) for s in range(100, 1000)]
print(f"aleatoria simple de 240: de Bucaramanga se esperan {240 * cuenta['Bucaramanga'] / n:.1f}; con las "
      f"semillas de 100 a 999, de {min(buc240)} a {max(buc240)}; exactamente 24 en el "
      f"{np.mean(np.array(buc240) == 24) * 100:.0f} %; estratificada al 2 %: {int((cuenta * 0.02).round().sum())} pedidos")
ext = t > tq3_ + 3 * (tq3_ - tq1_)
print(f"extremos de la sesión 4 (más de Q3 + 3 RIC): {ext.sum()}; calificados {(ext & cal).sum()} "
      f"({(ext & cal).sum() / ext.sum() * 100:.1f} %); con 1 estrella {(datos.loc[ext & cal, 'calificacion'] == 1).sum()}")
for c in ["franja", "medio_pago"]:
    r_ = cal.groupby(datos[c]).mean() * 100
    print(f"tasa de calificación por {c}: de {r_.min():.1f} a {r_.max():.1f} %", r_.round(1).to_dict())
print(f"Literary Digest: respondió {2376523 / 10_000_000 * 100:.1f} % de los 10 millones")
