# Análisis Estadístico de la Información

Material de clase de la electiva institucional *Análisis Estadístico de la Información*
(Especialización en Big Data, UCompensar). Son sesiones sincrónicas de 2 horas, con Python en Google
Colab, que siguen un mismo caso: **Tingua Domicilios S.A.S.**, una plataforma de domicilios
**ficticia**. Sus datos se generan con una semilla fija y no corresponden a personas ni a empresas
reales.

**Material en línea:** <https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/>

| Sesión | Tema | Diapositivas | Notebook |
|---|---|---|---|
| 1 | Del dato a la pregunta: diagnóstico, población y muestra, tipos de variable, escalas y fuentes de datos, primer DataFrame con pandas | [Ver](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-1-del-dato-a-la-pregunta.html) | [Abrir en Colab](https://colab.research.google.com/github/JotaMao1985/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/blob/main/notebooks/sesion-1-del-dato-a-la-pregunta.ipynb) |
| 2 | De 12 000 filas a una distribución: frecuencias absolutas, relativas y acumuladas, intervalos e histogramas, forma de una distribución y tablas cruzadas | [Ver](https://jotamao1985.github.io/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/diapositivas/sesion-2-de-las-filas-a-la-distribucion.html) | [Abrir en Colab](https://colab.research.google.com/github/JotaMao1985/ANaLISIS-ESTADiSTICO-DE-LA-INFORMACIoN_Ucomp/blob/main/notebooks/sesion-2-de-las-filas-a-la-distribucion.ipynb) |

Cada sesión tiene:

- **diapositivas de clase** en HTML: las flechas avanzan, `F` pone la pantalla completa, `M` abre el
  índice y `P`, la vista del presentador;
- **un cuaderno (*notebook*) de Google Colab** con las mismas celdas que se proyectan y una práctica
  guiada cuyos dos primeros ejercicios se revisan solos. Después de abrirlo hay que guardar una copia en Drive para conservar los cambios. La
  primera celda crea los datos del caso, así que no hay que subir nada.

## Estructura del repositorio

```
Htmls/        sitio publicado en GitHub Pages: portada y diapositivas (generado, no se edita a mano)
notebooks/    notebooks para Colab, uno por sesión
datos/        datos del caso (los mismos que crea la primera celda de cada notebook)
fuente/       fuente de la portada y de las diapositivas (Markdown) y sus diagramas
precalculo/   scripts que generan los datos, arman y ejecutan los notebooks y verifican las diapositivas;
              ayudas_sesionN.py tiene los verificadores de la práctica de cada sesión
```

## Cómo se construye una sesión

Las cifras y salidas que muestran las diapositivas salen de ejecutar el código, nunca se escriben a
mano. El notebook se ejecuta completo, con las soluciones, en un entorno que replica Colab
(Python 3.13, pandas 2.2.3):

```bash
python precalculo/genera_datos.py
python precalculo/notebook.py genera N
python precalculo/notebook.py ejecuta N      # salidas_sesionN.json y gráficas en recursos/sN/
python precalculo/verifica_diapositivas.py N # código y salidas proyectados = notebook y ejecución
python precalculo/portada.py                 # Htmls/index.html
```

Las diapositivas se construyen desde `fuente/diapositivas/sesionN.md` con la herramienta de
diapositivas del docente. Al hacer *push* a `main` con cambios en `Htmls/`, GitHub Actions publica el
sitio.
