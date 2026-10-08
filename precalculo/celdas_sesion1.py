# Fuente ÚNICA del código de la Sesión 1. De aquí salen:
#   - el notebook para Colab               (genera_notebook.py)
#   - las salidas que muestran las diapositivas (ejecuta_notebook.py → salidas_sesion1.json)
#
# No es un script ejecutable: es el formato «percent» de Jupyter.
#   # %% [markdown]            celda de texto (líneas con «# »)
#   # %% <id> [banderas]       celda de código
# Banderas:
#   generador   en el notebook se antepone el código de genera_datos.py y ayudas.py (celda oculta)
#   solucion    solución de un ejercicio: se ejecuta para verificar, NO va al notebook
#   plantilla   ejercicio por completar: va al notebook, NO se ejecuta al verificar

# %% [markdown]
# # Sesión 1 · Del dato a la pregunta
# **Análisis Estadístico de la Información — Especialización en Big Data (UCompensar)**
#
# Este notebook acompaña las [diapositivas de la sesión](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-1-del-dato-a-la-pregunta.html).
# Cada celda lleva entre corchetes el mismo identificador que el código proyectado, así que puedes seguir
# la clase celda a celda. La portada del curso está en https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/
#
# 1. **Archivo → Guardar una copia en Drive** para que tus cambios no se pierdan.
# 2. Ejecuta las celdas **en orden** con **Mayús + Enter**. Varias usan resultados de las anteriores.
# 3. Si Colab se reinicia o una celda falla al repetirla, usa **Entorno de ejecución → Ejecutar anteriores**.
# 4. La primera celda crea los datos del caso *Tingua Domicilios S.A.S.*, una empresa **ficticia**:
#    sus datos se inventan con una semilla fija y no corresponden a personas ni a empresas reales.

# %% datos generador
# Crea datos/pedidos.csv: los 12 000 pedidos del primer semestre de 2026
ruta = crear_datos("datos")

# %% [markdown]
# ## 1 · Primer contacto con los datos

# %% cargar
import pandas as pd

pedidos = pd.read_csv("datos/pedidos.csv")
pedidos.shape          # (filas, columnas)

# %% vistazo
# Las primeras cinco filas: cada fila es un pedido, cada columna una variable
pedidos.head()

# %% tipos
# El tipo de dato que pandas adivinó para cada columna
pedidos.dtypes

# %% faltantes
# calificacion es float64 aunque sean estrellas de 1 a 5: ¿por qué?
faltan = pedidos["calificacion"].isna()
print("Pedidos sin calificación:", faltan.sum())
print("Proporción:", round(faltan.mean(), 3))

# %% [markdown]
# ## 2 · Declarar la escala de medición
#
# pandas guarda el estrato como un número entero (`int64`), y con un número se puede promediar.
# Pero el estrato es una **categoría con orden**: decírselo a pandas evita cálculos sin sentido.

# %% ordinal
# El estrato es una categoría con orden, no una cantidad
pedidos["estrato"] = pd.Categorical(
    pedidos["estrato"], categories=[1, 2, 3, 4, 5, 6], ordered=True
)
# Comparar sí tiene sentido...
print("Estrato máximo:", pedidos["estrato"].max())
# ...promediar, no
try:
    pedidos["estrato"].mean()
except TypeError as error:
    print("TypeError:", error)

# %% [markdown]
# ## 3 · Un parámetro y tres estadísticos
#
# La tabla tiene **todos** los pedidos del semestre: es la población. Su media es un **parámetro** (μ).
# Una muestra aleatoria de 100 pedidos da un **estadístico** (x̄), que cambia de muestra en muestra.

# %% parametro
# Parámetro: se calcula con TODA la población
mu = pedidos["tiempo_entrega_min"].mean()
print(f"μ = {mu:.1f} min   (N = {len(pedidos)})")

# Estadísticos: cada muestra aleatoria da un valor distinto
for semilla in [1, 2, 3]:
    muestra = pedidos.sample(n=100, random_state=semilla)
    x_barra = muestra["tiempo_entrega_min"].mean()
    print(f"x̄ = {x_barra:.1f} min   (n = 100, semilla {semilla})")

# %% [markdown]
# ## 4 · Un adelanto: contar categorías
#
# Contar cuántas veces aparece cada categoría es el primer paso de una tabla de frecuencias,
# el tema de la próxima sesión.

# %% frecuencias
ciudad = pedidos["ciudad"]
conteo = ciudad.value_counts()
porcentaje = (ciudad.value_counts(normalize=True) * 100).round(1)
pd.DataFrame({"pedidos": conteo, "%": porcentaje})

# %% [markdown]
# ---
# # Práctica guiada
#
# Cuatro ejercicios. Los dos primeros se revisan solos al ejecutar su celda de revisión;
# el tercero lo comparamos en el chat y el cuarto lo comentamos en clase.
#
# ## Ejercicio 1 · Clasifica las variables
#
# Para cada variable escribe su **tipo** (`nominal`, `ordinal`, `discreta` o `continua`) y su
# **escala de medición** (`nominal`, `ordinal`, `intervalo` o `razon`). `id_pedido` y `fecha` no
# están: el primero es un identificador y la segunda la trabajamos en el ejercicio 2.
#
# `revisar_tipos` te dice cuáles están bien y, en las demás, te da una pista sin darte la respuesta.

# %% ej1
mis_tipos = {
    # variable              (tipo,  escala)
    "franja":              ("?", "?"),
    "ciudad":              ("?", "?"),
    "categoria":           ("?", "?"),
    "n_productos":         ("?", "?"),
    "valor_pedido":        ("?", "?"),
    "medio_pago":          ("?", "?"),
    "estrato":             ("ordinal", "ordinal"),   # este ya lo hicimos juntos
    "suscriptor":          ("?", "?"),
    "distancia_km":        ("?", "?"),
    "lluvia":              ("?", "?"),
    "temperatura_c":       ("?", "?"),
    "tiempo_entrega_min":  ("?", "?"),
    "calificacion":        ("?", "?"),
}
revisar_tipos(mis_tipos)

# %% ej1_solucion solucion
mis_tipos = {
    "franja": ("ordinal", "ordinal"), "ciudad": ("nominal", "nominal"),
    "categoria": ("nominal", "nominal"), "n_productos": ("discreta", "razón"),
    "valor_pedido": ("continua", "razón"), "medio_pago": ("nominal", "nominal"),
    "estrato": ("ordinal", "ordinal"), "suscriptor": ("nominal", "nominal"),
    "distancia_km": ("continua", "razón"), "lluvia": ("nominal", "nominal"),
    "temperatura_c": ("continua", "intervalo"), "tiempo_entrega_min": ("continua", "razón"),
    "calificacion": ("ordinal", "ordinal"),
}
revisar_tipos(mis_tipos)

# %% [markdown]
# ## Ejercicio 2 · Declara las escalas
#
# Como hicimos con el estrato:
#
# - convierte `franja` en categoría ordenada (`Mañana` < `Almuerzo` < `Tarde` < `Noche`);
# - convierte `calificacion` en categoría ordenada de 1 a 5 estrellas;
# - convierte `fecha` en fecha con `pd.to_datetime`.
#
# Reemplaza cada `...` y ejecuta. Después corre la celda de revisión. Como cada conversión parte
# del archivo original, puedes repetir la celda las veces que quieras sin perder datos.

# %% ej2 plantilla
original = pd.read_csv("datos/pedidos.csv")

pedidos["franja"] = pd.Categorical(
    original["franja"], categories=..., ordered=True
)
pedidos["calificacion"] = pd.Categorical(
    original["calificacion"], categories=..., ordered=True
)
pedidos["fecha"] = pd.to_datetime(...)

# %% ej2_solucion solucion
original = pd.read_csv("datos/pedidos.csv")

pedidos["franja"] = pd.Categorical(
    original["franja"], categories=["Mañana", "Almuerzo", "Tarde", "Noche"], ordered=True
)
pedidos["calificacion"] = pd.Categorical(
    original["calificacion"], categories=[1, 2, 3, 4, 5], ordered=True
)
pedidos["fecha"] = pd.to_datetime(original["fecha"])

# %% ej2_revision
revisar_escalas(pedidos)

# %% [markdown]
# ## Ejercicio 3 · Tu propio estadístico
#
# La proporción de pedidos que se entregaron con lluvia, calculada con **toda** la población, es el
# parámetro *p*. Toma tu propia muestra de 200 pedidos y calcula su proporción, *p̂*.
#
# Usa como semilla los **tres últimos dígitos de tu documento** (si empiezan por 0, quita los ceros:
# 045 se escribe 45) y comparte tu *p̂* en el chat. ¿Por qué cada uno obtiene un valor distinto?

# %% ej3
p = (pedidos["lluvia"] == "Sí").mean()
print(f"p = {p:.3f}   (los {len(pedidos)} pedidos)")

mi_semilla = 123   # ← tus tres últimos dígitos, sin ceros a la izquierda
muestra = pedidos.sample(n=200, random_state=mi_semilla)
p_gorro = (muestra["lluvia"] == "Sí").mean()
print(f"p̂ = {p_gorro:.3f}   (n = 200, semilla {mi_semilla})")

# %% [markdown]
# ## Ejercicio 4 · De los datos a la pregunta
#
# Escribe **dos preguntas** que la gerencia de Tingua podría responder con estos datos. Para cada una:
#
# 1. ¿Qué variables necesitas y de qué tipo son?
# 2. ¿Basta con describir los 12 000 pedidos, o tendrías que inferir algo que no está en la tabla?
#
# Y una pregunta sobre la fuente: ¿`pedidos.csv` es una fuente primaria o secundaria, interna o externa?
# ¿Sus datos son observacionales o experimentales? ¿Qué limita eso en lo que puedes concluir?
#
# *Escribe tus respuestas aquí (doble clic para editar).*
