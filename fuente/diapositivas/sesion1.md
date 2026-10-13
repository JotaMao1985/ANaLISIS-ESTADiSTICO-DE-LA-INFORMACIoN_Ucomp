---
tema: ucompensar
asignatura: Análisis Estadístico de la Información
unidad: Sesión
numero: 1
titulo: Del dato a la pregunta
subtitulo: Diagnóstico, conceptos básicos de estadística, tipos de variable y el primer DataFrame en Colab
lema: Antes de calcular, clasifica.
docente: Javier Mauricio Sierra
etiqueta: Sesión 1 · 2 horas
temas: Diagnóstico, Población y muestra, Variables y escalas, Fuentes de datos, pandas en Colab
objetivo: Distinguir población y muestra, clasificar los datos del caso Tingua por su tipo, su escala y su fuente, y comprobar en Python que esa clasificación decide qué cálculos tienen sentido.
salida: ../../Htmls/diapositivas/sesion-1-del-dato-a-la-pregunta.html
agenda: si
---

<!--
  Sesión 1 (2 h): bienvenida 8 min · diagnóstico 15 · conceptos 45 · Python 15 ·
  práctica 30 · cierre 7. Las diapositivas de código corresponden a las celdas
  del notebook (mismo identificador entre corchetes); las salidas son las de
  precalculo/salidas_sesion1.json, ejecutadas con Python 3.13 y pandas 2.2.3.
  Los hitos de reloj y el orden de recorte están en la nota de «Dos horas en
  seis momentos».
-->

# Bienvenida {icono=fa-door-open}

> Tener muchos datos no es lo mismo que saber qué dicen.

???
Arrancar con la frase. El syllabus abre igual: la era digital produce más información, que a veces se interpreta mal y termina distrayendo de los objetivos. Este curso trata de interpretarla bien. Pedir desde ya que abran el notebook de la sesión (botón «Abrir en Colab» de la portada del curso, o el enlace de la diapositiva de Colab) y ejecuten la primera celda: lo usaremos en la segunda hora.

## El curso recorre cuatro etapas, del diagnóstico al tablero

::: tarjetas {columnas=4}
### Reconocimiento
**Etapa 0** · diagnóstico sin nota: hoy
### Contextualización
**Etapa 1** · análisis exploratorio y muestreo
### Profundización
**Etapa 2** · regresión lineal simple y múltiple
### Transferencia
**Etapa 3** · visualización de datos e inteligencia de negocios
:::

**24 horas** con el docente y **72** de trabajo independiente: por cada hora de clase, tres por tu cuenta.

???
Son las cuatro etapas de la metodología y de los contenidos del syllabus. Dos créditos son 96 horas en total. El trabajo independiente no es opcional: lecturas, talleres y la práctica de cada sesión. Todo el curso se hace en Python, en Google Colab, sin instalar nada.

## Tres criterios valoran tu desempeño, y hoy empezamos por el primero

| Criterio | Qué pide |
|---|---|
| **CR1** | Clasificar los datos y su fuente para tomar decisiones |
| **CR2** | Comparar técnicas de minería de datos y elegir un modelo adecuado |
| **CR3** | Interpretar los resultados en distintos contextos |

Tres miradas en la evaluación: **autoevaluación**, **coevaluación** y **heteroevaluación**.

???
Los criterios de realización son la base de las rúbricas. Hoy trabajamos CR1 de principio a fin: clasificar variables, escalas y fuentes. CR2 y CR3 llegan con la regresión y la visualización. La autoevaluación empieza en un momento, con el diagnóstico.

## Dos horas en seis momentos

::: flujo
1. **Bienvenida** — 8 min
2. **Diagnóstico** — 15 min, sin nota
3. **Conceptos** — 45 min
4. **Python** — 15 min en Colab
5. **Práctica guiada** — 30 min
6. **Cierre** — 7 min
:::

Los conceptos de hoy: estadística, población y muestra, tipos de variable y fuentes de datos.

???
Hitos de reloj: la diapositiva 15 en el minuto 23; la 28, en el 45; la 37, en el 60; la 41, en el 68; la 49, en el 83, y la 51, en el 113. Si a los 45 min no se ha llegado a «Tipos de variable y escalas», recortar en este orden: (1) «El tipo de variable decide el resumen y el gráfico» (−1 min); (2) «La misma fórmula, sobre conjuntos distintos»: decir su frase en la diapositiva anterior (−1,5 min); (3) en «Clasifica estas cinco variables», comentar solo la 3 y la 5 (−2 min); (4) en Python, ejecutar en vivo solo [cargar] y [ordinal]: las demás salidas ya están proyectadas (−2 min). «Contar categorías» se salta solo como último recurso, diciendo que la respuesta a la 6 está en la celda [frecuencias]. Fuentes de datos y la práctica no se recortan: ahí se ve si CR1 quedó.

# Diagnóstico {icono=fa-stethoscope}

> Sin nota: sirve para saber desde dónde arrancamos, no para calificar.

???
Etapa 0 del syllabus: reconocimiento. Seis preguntas, un minuto cada una. Pedir que anoten sus respuestas (en papel, o en un mensaje sin enviar) y que no las busquen: el diagnóstico solo sirve si es honesto. Las respuestas se muestran todas juntas al final.

## ¿Qué tipo de variable es el estrato socioeconómico (1 a 6)? {.pregunta etiqueta="Diagnóstico · 1 de 6"}

- **A.** Cuantitativa continua
- **B.** Cuantitativa discreta
- **C.** Cualitativa ordinal
- **D.** Cualitativa nominal

???
Leer y dar un minuto. Respuesta: C. No dar pistas: esta y la 6 se resuelven hoy mismo.

## 20, 22, 25, 27 y 150 minutos: ¿qué describe mejor el tiempo típico? {.pregunta etiqueta="Diagnóstico · 2 de 6"}

Son los tiempos de entrega de cinco pedidos.

- **A.** La media: 48,8 min
- **B.** La mediana: 25 min
- **C.** El rango: 130 min
- **D.** La desviación estándar

???
Leer y dar un minuto. Respuesta: B. Si preguntan si el 150 es un error, no responder: es el tema de datos atípicos. Mide tendencia central.

## Misma media, distinta desviación estándar: ¿qué cambia? {.pregunta etiqueta="Diagnóstico · 3 de 6"}

En la ciudad A los pedidos tardan en promedio 35 min, con desviación estándar de 4 min. En la ciudad B, también 35 min, pero con desviación de 15 min.

- **A.** En B se entrega más rápido
- **B.** B tiene más pedidos
- **C.** Nada: con la misma media, el servicio es igual
- **D.** En B los tiempos son menos predecibles

???
Un minuto. Respuesta: D. Mide la idea de dispersión.

## Juzgar la satisfacción solo con las reseñas: ¿cuál es el problema? {.pregunta etiqueta="Diagnóstico · 4 de 6"}

Para saber qué tan satisfecha está **toda** su clientela, una empresa analiza solo las reseñas que algunas personas dejan en la app.

- **A.** Quienes escriben reseñas pueden no parecerse al resto
- **B.** La muestra es muy pequeña
- **C.** Ninguno, si las reseñas son muchas
- **D.** Habría que usar la mediana

???
Un minuto. Respuesta: A. Muestreo: sesgo de autoselección (respuesta voluntaria), un caso de sesgo de selección. Es lo mismo que pasa con las calificaciones de Tingua.

## Una regresión estima tiempo = 12 + 3 × distancia. ¿Qué dice el 3? {.pregunta etiqueta="Diagnóstico · 5 de 6"}

El tiempo está en minutos y la distancia en kilómetros.

- **A.** Que un pedido tarda 3 minutos
- **B.** Que la distancia explica el 3 % del tiempo
- **C.** Que cada kilómetro adicional suma, en promedio, 3 minutos
- **D.** Que la distancia promedio es de 3 km

???
Un minuto. Respuesta: C. Regresión lineal: interpretación de la pendiente.

## En pandas, ¿qué hace `pedidos["ciudad"].value_counts()`? {.pregunta etiqueta="Diagnóstico · 6 de 6"}

- **A.** Cuenta las columnas de la tabla
- **B.** Cuenta cuántos pedidos hay de cada ciudad
- **C.** Ordena la tabla por ciudad
- **D.** Borra las ciudades repetidas

???
Un minuto. Respuesta: B. Mide el nivel de Python. Si muchos fallan esta, dedicar más tiempo a la demostración en Colab.

## Respuestas del diagnóstico: cuenta tus aciertos

| Pregunta | Respuesta | Lo trabajamos en |
|---|---|---|
| 1 · Estrato | **C** · cualitativa ordinal | Hoy |
| 2 · Cinco tiempos | **B** · la mediana: el 150 arrastra la media | Tendencia central y atípicos |
| 3 · Misma media | **D** · menos predecibles | Medidas de dispersión |
| 4 · Solo reseñas | **A** · quien opina puede no parecerse al resto | Muestreo |
| 5 · El 3 | **C** · 3 min más por kilómetro | Regresión |
| 6 · `value_counts()` | **B** · pedidos por ciudad | Hoy, en Python |

???
Es su primera autoevaluación. Recoger dos cosas: el número de aciertos y la letra que marcaron en la 6 (p. ej., «4, B»); si la plataforma tiene encuesta, mejor, porque da los aciertos por pregunta; si no, en el chat. Si la mayoría tiene 2 o menos, la sesión 2 empieza con cinco minutos de media y mediana. Si muchos fallaron la 6, no saltar «Contar categorías» y mostrar pedidos.head() con calma. Guardar los números: el mismo diagnóstico se repite en la última sesión para comparar. Para la etapa 3, una encuesta rápida: ¿has construido un tablero en Power BI, Tableau o Looker Studio? Sí / No. No explicar ahora las preguntas 2 a 5: cada una tiene su sesión. La 2 sí merece una frase: la media (48,8) no se parece a ningún pedido; la mediana (25), a casi todos.

# Estadística para decidir {icono=fa-compass}

> Tingua Domicilios tiene 12 000 pedidos del semestre y una gerencia con preguntas.

???
Presentar el caso como una empresa de domicilios: el tipo de servicio que todos han usado alguna vez.

## Tingua Domicilios: el caso que nos acompaña todo el curso

::: tarjetas
### 12 000 pedidos
Todos los domicilios entregados entre enero y junio de 2026.
### 5 ciudades
Bogotá, Medellín, Cali, Barranquilla y Bucaramanga.
### 15 columnas
De la ciudad y el estrato a la distancia, la lluvia y la calificación.
:::

Tingua es una empresa **ficticia**: sus datos se generan con una semilla fija y no corresponden a personas ni a empresas reales.

???
Decir explícitamente que es ficticia. Los mismos datos sirven para todo el curso: hoy los clasificamos; en las próximas sesiones los resumimos, sacamos muestras, ajustamos regresiones y armamos un tablero.

## Cuatro preguntas de la gerencia ordenan el curso

1. ¿Cuánto tarda un pedido **típico**, y qué tan variable es? → *análisis exploratorio*
2. ¿Qué tan **satisfecha** está la clientela, si no todos los pedidos se califican? → *muestreo e inferencia*
3. ¿Cuántos minutos más tardan los pedidos por cada **kilómetro**, o con **lluvia**? → *regresión*
4. ¿Cómo se lo **mostramos** a la gerencia cada semana? → *visualización e inteligencia de negocios*

???
Volveremos a estas preguntas al final del curso. La segunda ya trae trampa: el 40,8 % de los pedidos no tiene calificación, y no faltan completamente al azar. Lo retomamos en fuentes de datos y, a fondo, en muestreo.

## Describir lo que hay; inferir lo que no vemos

::: definicion Análisis estadístico
La ciencia de recolectar, explorar y presentar datos para descubrir patrones y tendencias, y de medir cuánta incertidumbre tienen las conclusiones, para decidir con más fundamento.
:::

- **Descriptiva** — resume lo observado: «el 24,1 % de los pedidos del semestre se entregó con lluvia»
- **Inferencial** — generaliza más allá: «con 400 encuestas estimamos la satisfacción de toda la clientela»

???
La definición está adaptada del glosario del syllabus (*statistical analysis*): se le añadió la incertidumbre, que es lo que distingue la estadística de solo resumir datos. La distinción entre descriptiva e inferencial ordena las dos primeras etapas del curso: análisis exploratorio, y después muestreo.

## Un estudio estadístico empieza por la pregunta, aunque los datos lleguen primero

::: flujo
1. **Problema** — ¿qué queremos saber, y para decidir qué?
2. **Plan** — qué medir, a quién y cómo
3. **Datos** — recolectar, organizar y depurar
4. **Análisis** — resumir, graficar y modelar
5. **Conclusión** — responder, y decir con cuánta incertidumbre
:::

Es el ciclo **PPDAC**, que difundieron Wild y Pfannkuch (1999). En la empresa los datos suelen llegar primero: hoy vamos **del dato a la pregunta**, para saber qué preguntas pueden responder y cuáles no.

???
Hoy estamos al comienzo de «Datos»: antes de calcular hay que saber qué es cada columna. El título de la sesión recorre el ciclo al revés porque así pasa en las empresas: los datos llegan primero, recogidos para operar y no para nuestra pregunta (fuente secundaria). El trabajo es volver a la pregunta y decidir si estos datos la responden: eso es el criterio de pertinencia y el ejercicio 4. Buscar en los datos hasta que «algo» salga no es un estudio. El ciclo se debe a MacKay y Oldford; lo difundieron Wild, C. J. y Pfannkuch, M. (1999), *Statistical thinking in empirical enquiry*, International Statistical Review, 67(3).

## ¿Descriptiva o inferencial? {.pregunta}

1. «El tiempo medio de los 12 000 pedidos del semestre fue 35,1 min».
2. «Con una muestra de 400 clientes, estimamos que el 80 % recomendaría Tingua».
3. «En julio, los pedidos con lluvia tardarán unos 8 minutos más».

::: respuesta
**1, descriptiva**: resume todos los pedidos. **2 y 3, inferenciales**: la 2 va de una muestra a toda la clientela; la 3, del semestre observado a un mes que todavía no ha pasado.
:::

???
Dar 45 segundos y pedir en el chat tres letras en orden, D o I (p. ej., «D-I-I»). La 3 se apoya en un dato descriptivo real (con lluvia, los pedidos del semestre tardaron 7,8 min más en promedio), pero lo proyecta a julio: eso ya es inferir. En la 3 la población ya no son los 12 000 pedidos, sino todos los de Tingua, incluidos los de julio; el semestre hace de muestra, y no al azar: suponemos que julio se parece al semestre. La población la decide la pregunta: lo veremos enseguida.

# Población y muestra {icono=fa-users}

> ¿Cuánto tarda un pedido de Tingua? Depende de si miras los 12 000 o solo 100.

## La población es el todo; la muestra, la parte que observas

![Población, muestra, parámetro y estadístico (puntos ilustrativos, no a escala)](recursos/s1/poblacion-muestra.svg){alto=430}

???
Detenerse en las dos flechas: muestrear es ir de la población a la muestra; inferir es volver con una conclusión. Toda la estadística inferencial vive en la flecha punteada. Aquí la población cabe en una tabla y por eso podemos calcular μ. Si alguien objeta «en Big Data tenemos todos los datos»: tener todas las filas no es tener la población de la pregunta. Los pedidos de julio todavía no existen, quien no califica no opina, los pedidos cancelados no quedaron (la tabla solo trae los entregados) y quien nunca pidió no aparece.

## El parámetro describe la población; el estadístico, la muestra

| | Población · parámetro | Muestra · estadístico |
|---|---|---|
| Tamaño | \(N\) | \(n\) |
| Media | \(\mu\) | \(\bar{x}\) («x barra») |
| Desviación estándar | \(\sigma\) | \(s\) |
| Proporción | \(p\) | \(\hat{p}\) («p gorro») |

Letras **griegas** para los parámetros, salvo \(N\) y \(p\); **latinas** para los estadísticos.

???
Es la convención de casi todos los textos; el tamaño y la proporción son las excepciones (N, y p con su p gorro). Con los datos de Tingua: N = 12 000, μ = 35,1 min, p = 0,241 (pedidos con lluvia).

## La misma fórmula, sobre conjuntos distintos

$$ \begin{aligned} \mu &= \frac{1}{N}\sum_{i=1}^{N} x_i && \text{población: los } N \text{ pedidos} \\[6pt] \bar{x} &= \frac{1}{n}\sum_{i=1}^{n} x_i && \text{muestra: solo } n \text{ pedidos} \end{aligned} $$

\(x_i\) es el tiempo del pedido número \(i\), y \(\sum\) los suma todos, del primero (\(i = 1\)) al último. Misma cuenta: \(\mu\) recorre la población; \(\bar{x}\), solo la muestra.

???
Cómo se lee en voz alta: «mu es la suma de los x sub i, de i igual a 1 hasta N, dividida entre N». La cuenta es idéntica; lo que cambia es sobre qué conjunto se hace, y por eso cambia lo que significa. En media hora lo veremos en Python: tres muestras de 100 pedidos, tres x̄ distintos, un solo μ.

## Cada fila es una unidad de observación; cada columna, una variable

| id_pedido | ciudad | estrato | n_productos | distancia_km | tiempo_entrega_min |
|---|---|---|---|---|---|
| P00001 | Medellín | 4 | 2 | 4.4 | 30.6 |
| P00002 | Bogotá | 4 | 5 | 5.6 | 36.9 |
| P00003 | Bucaramanga | 5 | 2 | 1.9 | 16.0 |

En Tingua, la **unidad de observación** es el **pedido**, no el cliente.

???
Es la forma «ordenada» (*tidy*) de una tabla: una fila por unidad, una columna por variable (Wickham, 2014, *Tidy data*, Journal of Statistical Software). Preguntar: si la gerencia quiere saber cuántos clientes distintos tiene, ¿sirve esta tabla? No: no trae identificador de cliente. Las cifras van con punto decimal porque así las verán en pandas.

## ¿Parámetro o estadístico? {.pregunta}

1. El 24,1 % de los 12 000 pedidos del semestre se entregó con lluvia.
2. En 100 pedidos auditados al azar, el tiempo medio fue de 34,4 min.
3. El tiempo medio de **todos** los pedidos de Cali en el semestre fue de 32,5 min.

::: respuesta
**1, parámetro**: es \(p = 0{,}241\) (el 24,1 %), sobre toda la población. **2, estadístico**: es \(\bar{x}\), de una muestra. **3, parámetro**: es la media de una población completa, la de los pedidos de Cali.
:::

???
45 segundos; en el chat, P o E para cada una. La 3 es la que más se equivoca: «Cali» suena a una parte de algo más grande. Pero si la pregunta es sobre los pedidos de Cali, sus 1966 pedidos son la población. Qué es población lo decide la pregunta, no la tabla.

## Un parámetro es fijo y casi nunca se conoce; un estadístico se conoce, pero cambia {.idea}

La inferencia estadística consiste en medir cuánto se puede confiar en el segundo para hablar del primero.

???
Llevar esta frase hasta la etapa de muestreo. En la práctica la comprobarán: cada uno obtendrá un p̂ distinto.

# Tipos de variable y escalas {icono=fa-tags}

> Antes de calcular, clasifica: el tipo de variable decide qué operaciones tienen sentido.

???
Este es el núcleo de CR1. Los ejemplos son cotidianos; algunos anticipan columnas de Tingua (tiempo de espera, temperatura, satisfacción), y está bien: en la práctica quedan las demás por pensar.

## Toda variable es cualitativa o cuantitativa, y cada una tiene dos clases

![Clasificación de las variables](recursos/s1/tipos-variable.svg){alto=440}

???
Recorrer el árbol de arriba abajo, con una pregunta en cada nivel. ¿Tiene sentido sumar o promediar? Cualitativa o cuantitativa. ¿Hay un orden natural? Nominal u ordinal. ¿Se cuenta o se mide? Discreta o continua. Las de dos categorías, como «¿fuma?», se llaman dicotómicas y casi siempre se tratan como nominales.

## Cualitativas: las nominales solo nombran; las ordinales, además, ordenan {.arriba}

### Nominal
- Grupo sanguíneo: A, B, AB, O
- Medio de transporte: bus, carro, bicicleta
- ¿Fuma?: sí / no (*dicotómica*)

|||

### Ordinal
- Estrato: 1 < 2 < … < 6
- Nivel educativo: primaria < bachillerato < pregrado < posgrado
- Satisfacción: de «muy insatisfecho» a «muy satisfecho»

???
La pregunta que las separa: ¿tiene sentido decir que una categoría es «mayor» que otra? El grupo O no es mayor que el A. El estrato 4 sí es mayor que el 2, pero en una ordinal se sabe cuál es mayor, no por cuánto: la distancia entre los estratos 1 y 2 no tiene por qué ser la misma que entre el 5 y el 6.

## Cuantitativas: las discretas se cuentan; las continuas se miden

::: tarjetas
### Discreta
Número de hijos, quejas recibidas en un día: 0, 1, 2… Entre 2 y 3 hijos no hay nada.
### Continua
Estatura, peso corporal, tiempo de espera: entre dos valores siempre cabe otro.
:::

El dinero se cuenta en pesos, pero, como admite tantísimos valores, se suele tratar como **continuo**.

???
Una continua se registra redondeada (la estatura en centímetros), pero eso es una limitación del instrumento, no de la variable. Lo del dinero es una convención: decirlo, porque en el ejercicio 1 aparece el valor del pedido y el verificador acepta las dos respuestas.

## Cuatro escalas de medición: cada una permite una operación más

| Escala | Qué permite | Ejemplos |
|---|---|---|
| **Nominal** | igual o distinto | grupo sanguíneo, medio de transporte |
| **Ordinal** | + mayor o menor | estrato, nivel educativo |
| **Intervalo** | + restar: las diferencias tienen sentido; el cero es arbitrario | temperatura en °C, fecha y hora de un evento |
| **Razón** | + cocientes: «el doble», «la mitad»; el cero es «nada» | estatura, ingreso, tiempo de espera |

Es la clasificación de Stevens (1946).

???
Cada escala hereda las operaciones de la anterior. La de intervalo es la que más cuesta: de 10 a 20 °C hay lo mismo que de 20 a 30 °C, pero 0 °C no es ausencia de temperatura; y el origen del calendario es una convención. En razón, el cero sí es «nada»: 0 minutos de espera es no esperar. Referencia: Stevens, S. S. (1946), *On the theory of scales of measurement*, Science, 103(2684).

## ¿Hace el doble de calor en Barranquilla que en Bogotá? {.pregunta}

La temperatura media de los pedidos del semestre fue de **28,8 °C** en Barranquilla y de **13,9 °C** en Bogotá, y 28,8 / 13,9 ≈ 2,07.

::: respuesta
**No.** Los grados Celsius son una escala de **intervalo**: su cero es convencional (marca dónde se congela el agua), no la ausencia de temperatura. En kelvin (se suma 273,15), cuyo cero es el cero absoluto, la razón es 301,95 / 287,05 ≈ **1,05**: la temperatura absoluta es apenas un 5 % mayor.
:::

???
Antes de revelar, pedir un sí o un no en el chat. Lo que sí tiene sentido es la diferencia: en Barranquilla hacía 14,9 °C más. Las temperaturas salen de la columna temperatura_c de Tingua.

## Un número no siempre es una cantidad {.idea}

El estrato se escribe con números del 1 al 6, pero promediarlo (3,3 en Tingua) supone que del estrato 1 al 2 hay la misma distancia que del 5 al 6, y nada lo garantiza: los números son etiquetas con orden.

???
Era la pregunta 1 del diagnóstico: ¿quién la acertó? Si alguien objeta que el promedio de hijos tampoco es un número posible de hijos, tiene razón: por eso el argumento no es que 3,3 «no exista», sino que las distancias entre estratos no son iguales. Puente con Python: pandas leerá el estrato como un entero y lo promediará sin protestar; veremos cómo decirle que es una categoría con orden. En Colombia el estrato lo asigna el municipio a la vivienda, no a la persona (Ley 142 de 1994, art. 102, que nombra los seis estratos con orden). En Tingua es el estrato de la dirección de entrega.

## Clasifica estas cinco variables {.pregunta}

1. Clics en una visita a la app
2. Prioridad de un ticket de soporte: baja, media, alta, crítica
3. Código DIVIPOLA del municipio: 05001, 11001, 76001
4. Latencia de una consulta a la base de datos, en milisegundos
5. Año de nacimiento

::: respuesta
**1** cuantitativa discreta, de razón · **2** cualitativa ordinal · **3** cualitativa nominal: es un código, no una cantidad · **4** cuantitativa continua, de razón · **5** cuantitativa continua (aunque se registre en años enteros), de **intervalo**: el origen del calendario es una convención.
:::

???
Un minuto; en el chat, solo la 3 y la 5. Ninguna salió en las diapositivas anteriores. La 3 es la trampa de quien trabaja con datos: si pandas lee el código como número, 05001 (Medellín) se vuelve 5001 y deja de cruzar con otras tablas; se lee con dtype=str. La 5 es la difícil: restar años tiene sentido (una edad), dividirlos no. Lo que importa aquí es la escala.

## El tipo de variable decide el resumen y el gráfico

| Tipo | Resumen | Gráfico |
|---|---|---|
| Nominal | frecuencias, moda | barras |
| Ordinal | frecuencias acumuladas, mediana | barras en su orden |
| Discreta | media, mediana, frecuencias | barras o histograma |
| Continua | media, desviación estándar, cuartiles | histograma, caja |

Es el mapa de las próximas sesiones.

???
No desarrollar: es un adelanto. La próxima sesión empieza por la primera columna (tablas de frecuencias). Si el tiempo aprieta, esta es la diapositiva que se salta.

# Fuentes de datos {icono=fa-database}

> El mismo número vale distinto según de dónde viene y para qué se recogió.

???
La segunda mitad de CR1: clasificar la fuente. No se recorta: el ejercicio 4 de la práctica pide clasificar la fuente de pedidos.csv.

## Primaria o secundaria: ¿se recogió para tu pregunta?

::: tarjetas
### Primaria
La recoges tú, para tu pregunta: una encuesta de satisfacción que diseña Tingua, una prueba de una nueva app de rutas.
### Secundaria
Ya existía, recogida por otros o para otro fin: los registros de la app, los datos del clima del IDEAM, las encuestas del DANE.
:::

En otro eje: **interna**, si la produce la organización, o **externa**, si viene de fuera.

???
Preguntar antes de decirlo: ¿pedidos.csv es primaria o secundaria? ¿Interna o externa? 30 segundos, respuesta en el chat. pedidos.csv sorprende: es de Tingua (interna) pero secundaria, porque la app la registra para operar, no para responder nuestras preguntas. Por eso trae lo que la operación necesitó y no lo que el análisis querría: no tiene identificador de cliente. En la ficción, la lluvia y la temperatura vienen de un servicio de clima que se une a cada pedido: una fuente externa dentro de una tabla interna.

## Observar o experimentar: solo el experimento permite hablar de causa

::: tarjetas
### Estudio observacional
Se registra lo que pasa, sin intervenir. Con lluvia, los pedidos de Tingua tardaron **7,8 min más**; pero llueve más en Bogotá, donde los pedidos ya tardan más: parte de esa diferencia es de la ciudad, no de la lluvia.
### Experimento
Se asigna al azar quién recibe qué. Si Tingua prueba una nueva app de rutas en la mitad de los pedidos, elegidos al azar, la diferencia sí se puede atribuir a la app.
:::

???
Bogotá: 28,5 % de pedidos con lluvia y 39,5 min de media; Barranquilla: 10,6 % y 29,8 min. Comparando dentro de cada ciudad, la diferencia baja a unos 6,9 min. El tráfico que causa la lluvia no es un confusor: es parte de su efecto (un mediador). Los datos de Tingua son observacionales: lo que concluyamos con regresión será asociación, no causa. Saber esto es la mitad de interpretar en contexto, que es lo que pide CR3.

## Seis criterios para decidir si una fuente sirve

| Criterio | Pregunta | En Tingua |
|---|---|---|
| **Pertinencia** | ¿Responde mi pregunta? | Sin identificador de cliente, no se pueden contar clientes |
| **Exactitud** | ¿Los valores son correctos? | Un pedido de 201 minutos: ¿demora real o error? |
| **Completitud** | ¿Qué falta, y por qué? | El 40,8 % de los pedidos no tiene calificación |
| **Oportunidad** | ¿Está al día? | Llega hasta el 30 de junio de 2026 |
| **Consistencia** | ¿Coincide con otras fuentes? | Los totales deberían cuadrar con contabilidad |
| **Legitimidad** | ¿Puedo usarla para esto? | Dirección y estrato son datos personales (Ley 1581 de 2012) |

???
CR1 pide clasificar los datos y su fuente para decidir: esta es la lista de chequeo. La completitud trae una trampa (es la pregunta 4 del diagnóstico, con datos de Tingua) que veremos en muestreo: los clientes cuyo pedido tardó más de 55 minutos califican mucho más (81 %) que el resto (58 %). Los faltantes no son completamente al azar. El pedido de 201 minutos es el más lento del semestre: lo retomamos en datos atípicos. Legitimidad: que un dato exista no autoriza a usarlo; la ley pide autorización y respetar la finalidad. El estrato no está en la lista de datos sensibles, pero revela la condición socioeconómica del hogar.

# Primer contacto en Python {icono=fa-laptop-code}

> Lo que acabamos de clasificar a mano, ahora con pandas.

## Colab: un cuaderno de Python en el navegador, sin instalar nada

::: flujo
1. **Abre** — botón «Abrir en Colab» de la portada del curso
2. **Guarda una copia** — Archivo → Guardar una copia en Drive
3. **Crea los datos** — ejecuta la primera celda sin modificarla
4. **Avanza en orden** — Mayús + Enter, celda por celda
:::

[Abrir el cuaderno (*notebook*) de la sesión 1 en Colab](https://colab.research.google.com/github/JotaMao1985/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/blob/main/notebooks/sesion-1-del-dato-a-la-pregunta.ipynb). Cada celda lleva entre corchetes el mismo identificador que el código de estas diapositivas.

???
Si alguien todavía no lo ha abierto, que lo haga ahora: la portada del curso está en https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/ y el enlace de esta diapositiva abre el notebook directamente. Si Colab se reinicia o una celda falla al repetirla: Entorno de ejecución → Ejecutar anteriores. La primera celda está plegada: crea los datos y unas funciones para revisar la práctica. Si Colab avisa que el cuaderno no es de Google, elegir «Ejecutar de todos modos». Durante la demostración solo miran: ejecutan la primera celda y [cargar], y el resto en la práctica; así caben los 15 min.

## Tres líneas para cargar los 12 000 pedidos {columnas=3:2}

```python [cargar] {resaltar=3-4}
import pandas as pd

pedidos = pd.read_csv("datos/pedidos.csv")
pedidos.shape          # (filas, columnas)
#> (12000, 15)
```

|||

- `read_csv` lee el archivo y devuelve un **DataFrame**: una tabla con columnas con nombre
- `.shape`: 12 000 filas, una por **pedido**, y 15 columnas: un identificador y 14 **variables**
- Python escribe el decimal con punto y no separa los miles: `35.1` es 35,1 y `12000` es 12 000

???
Ejecutar en vivo y, en la celda siguiente del notebook, mostrar pedidos.head(): ahí se ven los NaN de la calificación, que usamos en dos diapositivas.

## pandas adivina el tipo de dato, no el tipo de variable {columnas=3:2}

```python [tipos] {resaltar=1,3,10,16}
pedidos.dtypes
#> id_pedido              object
#> fecha                  object
#> franja                 object
#> ciudad                 object
#> categoria              object
#> n_productos             int64
#> valor_pedido            int64
#> medio_pago             object
#> estrato                 int64
#> suscriptor             object
#> distancia_km          float64
#> lluvia                 object
#> temperatura_c         float64
#> tiempo_entrega_min    float64
#> calificacion          float64
#> dtype: object
```

|||

- `object` es texto; `int64`, entero; `float64`, decimal
- `estrato` es `int64`, pero es ordinal
- `calificacion` es `float64`, pero son estrellas de 1 a 5
- `fecha` es `object`: llegó como texto

???
El tipo de dato dice cómo se guarda el valor en memoria; el tipo de variable, qué significa. pandas solo puede adivinar lo primero. Las columnas iluminadas son ejemplos de lo que hay que corregir a mano; en la práctica también corregirán la franja, que es ordinal por el orden del día (Mañana < Almuerzo < Tarde < Noche): un criterio cronológico, no de tamaño.

## ¿Por qué la calificación es float64, si son estrellas de 1 a 5? {.pregunta}

Pista: mira la última columna de `pedidos.head()`.

::: respuesta
Porque **le faltan valores**: pandas marca un faltante con `NaN`, que es un número decimal, y, para que quepa, vuelve decimal toda la columna.

```python [faltantes]
faltan = pedidos["calificacion"].isna()
print("Pedidos sin calificación:", faltan.sum())
print("Proporción:", round(faltan.mean(), 3))
#> Pedidos sin calificación: 4901
#> Proporción: 0.408
```
:::

???
Dar 30 segundos para mirar la salida de pedidos.head(). Es la misma cifra del criterio de completitud: 4901 pedidos, el 40,8 %.

## Declarar la escala evita cálculos sin sentido {columnas=2:1}

```python [ordinal] {resaltar=2-5,7,10-12}
# El estrato es una categoría con orden, no una cantidad
pedidos["estrato"] = pd.Categorical(
    pedidos["estrato"], categories=[1, 2, 3, 4, 5, 6], ordered=True
)
print("Estrato máximo:", pedidos["estrato"].max())
try:
    pedidos["estrato"].mean()
except TypeError as error:
    print("TypeError:", error)
#> Estrato máximo: 6
#> TypeError: 'Categorical' with dtype category
#>   does not support reduction 'mean'
```

|||

- `ordered=True` le dice a pandas que hay un orden
- `max()` funciona; `mean()` se niega
- Un error a tiempo es mejor que un promedio sin sentido

???
El try/except solo está para que la celda no se detenga: lo que importa es el mensaje. En el notebook la celda trae dos comentarios más («comparar sí tiene sentido… promediar, no»). La salida del error está partida en dos líneas para que quepa. En la práctica harán lo mismo con la franja y la calificación.

## Tres muestras, tres x̄ distintos y un solo μ {columnas=2:1}

```python [parametro] {resaltar=2,7-8,10-13}
# Parámetro: se calcula con TODA la población
mu = pedidos["tiempo_entrega_min"].mean()
print(f"μ = {mu:.1f} min   (N = {len(pedidos)})")

# Estadísticos: cada muestra aleatoria da un valor distinto
for semilla in [1, 2, 3]:
    muestra = pedidos.sample(n=100, random_state=semilla)
    x_barra = muestra["tiempo_entrega_min"].mean()
    print(f"x̄ = {x_barra:.1f} min   (n = 100, semilla {semilla})")
#> μ = 35.1 min   (N = 12000)
#> x̄ = 34.4 min   (n = 100, semilla 1)
#> x̄ = 35.2 min   (n = 100, semilla 2)
#> x̄ = 35.9 min   (n = 100, semilla 3)
```

|||

- \(\mu\) no cambia: es uno solo
- \(\bar{x}\) cambia con cada muestra, pero queda **cerca** de \(\mu\)
- ¿Qué tan cerca? Esa es la pregunta del muestreo

???
La semilla (random_state) hace que la muestra sea reproducible: con la misma semilla sale la misma muestra en cualquier computador. Preguntar qué pasaría con muestras de 1000 pedidos en lugar de 100 y dejar la respuesta en el aire.

## Contar categorías: el primer paso de una tabla de frecuencias {columnas=3:2}

```python [frecuencias]
ciudad = pedidos["ciudad"]
conteo = ciudad.value_counts()
porcentaje = (ciudad.value_counts(normalize=True) * 100).round(1)
pd.DataFrame({"pedidos": conteo, "%": porcentaje})
#>               pedidos     %
#> ciudad
#> Bogotá           4707  39.2
#> Medellín         2663  22.2
#> Cali             1966  16.4
#> Barranquilla     1474  12.3
#> Bucaramanga      1190   9.9
```

|||

- `value_counts()`: frecuencia absoluta
- `normalize=True`: frecuencia relativa
- Es la respuesta a la pregunta 6 del diagnóstico

???
Es un adelanto de la próxima sesión, donde la tabla se completa con frecuencias acumuladas y sus gráficos. Si el tiempo aprieta, se salta: la celda está en el notebook.

# Práctica y cierre {icono=fa-keyboard}

> Treinta minutos con el notebook: clasificar, declarar escalas y sacar tu propia muestra.

## Práctica guiada: cuatro ejercicios en el notebook

::: flujo
1. **Clasifica** — tipo y escala de 13 variables de Tingua; `revisar_tipos` da pistas · 10 min
2. **Declara las escalas** — franja y calificación ordenadas; fecha como fecha · 8 min
3. **Tu propio estadístico** — \(\hat{p}\) con tu semilla, y al chat · 5 min
4. **De los datos a la pregunta** — dos preguntas para la gerencia, y la fuente de los datos · 7 min
:::

???
Los ejercicios 1 y 2 se revisan solos: revisar_tipos dice qué variable está mal y da una pista, sin la respuesta. Ir anotando en una pizarra compartida los p̂ que lleguen al chat en el ejercicio 3: todos rondan p = 0,241 y nadie lo obtiene exacto. Si dos personas eligieron el mismo número, obtienen el mismo p̂: eso es la reproducibilidad. En el ejercicio 4, pedir dos o tres voluntarios que lean sus preguntas.

## ¿Por qué cada uno obtuvo una proporción muestral distinta? {.pregunta}

Mira los \(\hat{p}\) del chat: todos con \(n = 200\), cada uno con su propia semilla. El parámetro es \(p = 0{,}241\).

::: respuesta
Porque cada semilla elige 200 pedidos distintos de los 12 000. El estadístico **varía de muestra en muestra** alrededor del parámetro; esa variación tiene forma y tamaño, y medirla es el trabajo de la inferencia.
:::

???
Es la imagen con la que abriremos la etapa de muestreo: un histograma con los p̂ del grupo tiende a la forma de campana, centrado cerca de p. Detalle para quien pregunte: con n = 200, p̂ siempre es múltiplo de 0,005, así que nadie puede obtener 0,241 exacto.

## Lo que te llevas hoy {.cierre}

- La estadística **describe** lo que hay e **infiere** lo que no vemos
- Un **parámetro** es fijo y casi nunca se conoce; un **estadístico** se conoce, pero cambia con la muestra
- Toda variable es **nominal, ordinal, discreta o continua**, y su **escala** decide qué cálculos valen
- La **fuente** importa: primaria o secundaria, observacional o experimental
- pandas adivina el **tipo de dato**; el **tipo de variable** se lo dices tú

???
Leer las cinco en voz alta y preguntar cuál les costó más: es la autoevaluación de cierre. Volver al título: hoy fuimos del dato a la pregunta, y sus dos preguntas del ejercicio 4 abren la sesión 2. Cerrar con el lema: antes de calcular, clasifica.

## La sesión 2 abre con tus dos preguntas

- **Termina** la práctica: los ejercicios 1 y 2 se revisan solos
- **Lee** *OpenIntro Statistics* (4.ª edición, de acceso abierto), capítulo 1, secciones 1.2 a 1.4
- **Trae** tus dos preguntas del ejercicio 4: otra persona del curso las revisará con los criterios de hoy (coevaluación)

**Próxima sesión:** tablas y distribuciones de frecuencias.

???
OpenIntro Statistics (Diez, Çetinkaya-Rundel y Barr) se descarga gratis en openintro.org; las secciones 1.2 a 1.4 cubren tipos de variable, principios de muestreo y experimentos, en inglés (el syllabus pide referencias en otros idiomas). Es una sugerencia del docente: no está en la bibliografía del syllabus. OpenIntro clasifica las variables, pero no desarrolla las escalas de intervalo y razón: esas quedan en las diapositivas. Con las preguntas que traigan se hace la coevaluación al abrir la sesión 2.
