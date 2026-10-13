"""Verificadores de la práctica de la sesión 1: dan pistas sin revelar la respuesta.

Van dentro de la celda oculta del notebook, junto con genera_datos.py y ayudas.py.
"""

import unicodedata


# Formas equivalentes que también se aceptan
_SINONIMOS = {
    "cualitativa nominal": "nominal", "cualitativa ordinal": "ordinal",
    "cuantitativa discreta": "discreta", "cuantitativa continua": "continua",
    "de razon": "razon", "proporcion": "razon", "de proporcion": "razon",
    "ratio": "razon", "de intervalo": "intervalo", "intervalar": "intervalo",
}


def _normal(texto):
    texto = unicodedata.normalize("NFD", " ".join(str(texto).lower().split()))
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return _SINONIMOS.get(texto, texto)


_TIPOS = {
    "franja": ("ordinal", "ordinal"),
    "ciudad": ("nominal", "nominal"),
    "categoria": ("nominal", "nominal"),
    "n_productos": ("discreta", "razon"),
    "valor_pedido": ("continua", "razon"),
    "medio_pago": ("nominal", "nominal"),
    "estrato": ("ordinal", "ordinal"),
    "suscriptor": ("nominal", "nominal"),
    "distancia_km": ("continua", "razon"),
    "lluvia": ("nominal", "nominal"),
    "temperatura_c": ("continua", "intervalo"),
    "tiempo_entrega_min": ("continua", "razon"),
    "calificacion": ("ordinal", "ordinal"),
}
_CUALI, _CUANTI = {"nominal", "ordinal"}, {"discreta", "continua"}
_ESCALAS = {"nominal", "ordinal", "intervalo", "razon"}


def _pista_tipo(dado, correcto):
    if dado not in _CUALI | _CUANTI:
        return "el tipo debe ser nominal, ordinal, discreta o continua"
    if (dado in _CUALI) != (correcto in _CUALI):
        return "¿tiene sentido sumar o promediar sus valores?"
    if correcto in _CUALI:
        return "¿sus categorías siguen un orden o una secuencia natural, o solo son nombres?"
    return "¿se cuenta (0, 1, 2…) o se mide (cualquier valor dentro de un rango)?"


def _pista_escala(dado, correcto):
    if dado not in _ESCALAS:
        return "la escala debe ser nominal, ordinal, intervalo o razón"
    if {dado, correcto} == {"intervalo", "razon"}:
        return "¿el cero significa «nada» de esa cantidad?"
    return "la escala tiene que ser coherente con el tipo"


def revisar_tipos(mis_tipos):
    """Compara tu clasificación con la esperada y da una pista en cada error."""
    if not isinstance(mis_tipos, dict):
        print('✗  mis_tipos debe ser un diccionario: {"franja": ("tipo", "escala"), ...}')
        return
    tuyas = {_normal(k): v for k, v in mis_tipos.items()}  # «categoría» = «categoria»
    aciertos = 0
    for variable, (tipo_ok, escala_ok) in _TIPOS.items():
        if variable not in tuyas:
            print(f"·  {variable}: falta en tu diccionario")
            continue
        par = tuyas[variable]
        if not isinstance(par, (tuple, list)) or len(par) != 2:
            print(f'✗  {variable}: escribe una pareja ("tipo", "escala"), '
                  "con una coma entre los dos textos")
            continue
        tipo, escala = (_normal(x) for x in par)
        if tipo == "?" or escala == "?":
            print(f"·  {variable}: todavía tiene «?»")
            continue
        if variable == "valor_pedido" and tipo == "discreta":
            tipo = "continua"  # en rigor se cuenta en pesos; se trata como continua
        pistas = []
        if variable == "calificacion" and tipo in _CUANTI:
            pistas.append("las apps promedian las estrellas, pero ¿hay la misma distancia entre 1 y 2 "
                          "estrellas que entre 4 y 5? ¿Qué otra variable de hoy usa números solo "
                          "para ordenar?")
        elif tipo != tipo_ok:
            pistas.append(_pista_tipo(tipo, tipo_ok))  # con el tipo mal, la escala se corrige sola
        elif escala != escala_ok:
            pistas.append(_pista_escala(escala, escala_ok))
        if pistas:
            print(f"✗  {variable}: " + " · ".join(pistas))
        else:
            aciertos += 1
            print(f"✓  {variable}")
    print(f"\n{aciertos} de {len(_TIPOS)} variables bien clasificadas")


def revisar_escalas(tabla):
    """Revisa que franja y calificacion sean categorías ordenadas y fecha, una fecha."""
    import pandas as pd

    if not isinstance(tabla, pd.DataFrame):
        print("✗  pásale la tabla: revisar_escalas(pedidos)")
        return
    faltan = [c for c in ("franja", "calificacion", "fecha") if c not in tabla.columns]
    if faltan:
        print(f"✗  a la tabla le falta: {', '.join(faltan)}; vuelve a ejecutar [cargar]")
        return
    original = pd.read_csv("datos/pedidos.csv")

    def ordenada(columna, categorias):
        serie = tabla[columna]
        if isinstance(serie, pd.DataFrame):
            return f"✗  {columna}: la tabla tiene dos columnas {columna}; vuelve a ejecutar [cargar]"
        if not isinstance(serie.dtype, pd.CategoricalDtype):
            return f"✗  {columna}: todavía es {serie.dtype}; conviértela con pd.Categorical"
        if not serie.cat.ordered:
            return f"✗  {columna}: es categoría, pero falta ordered=True"
        texto = lambda c: str(c).removesuffix(".0")  # 4 y 4.0 son la misma estrella
        tuyas = [texto(c) for c in serie.cat.categories]
        esperadas = [texto(c) for c in categorias]
        if sorted(tuyas) != sorted(esperadas):
            return (f"✗  {columna}: revisa las categorías: deben escribirse igual que "
                    "en los datos (mayúsculas, tildes, sin espacios de más)")
        if tuyas != esperadas:
            return f"✗  {columna}: las categorías están bien escritas; revisa su orden"
        if serie.notna().sum() != original[columna].notna().sum():
            return (f"✗  {columna}: se perdieron valores al convertir; "
                    "revisa que las categorías se escriban igual que en los datos")
        return f"✓  {columna}: categoría ordenada"

    print(ordenada("franja", ["Mañana", "Almuerzo", "Tarde", "Noche"]))
    print(ordenada("calificacion", [1, 2, 3, 4, 5]))
    if pd.api.types.is_datetime64_any_dtype(tabla["fecha"]) and (
            tabla["fecha"].notna().sum() < original["fecha"].notna().sum()):
        print("✗  fecha: es fecha, pero se perdieron valores; "
              "los datos vienen como 2026-01-31 (año-mes-día)")
    elif pd.api.types.is_datetime64_any_dtype(tabla["fecha"]):
        inicio, fin = tabla["fecha"].min().date(), tabla["fecha"].max().date()
        print(f"✓  fecha: es una fecha (del {inicio} al {fin})")
    else:
        print(f"✗  fecha: todavía es {tabla['fecha'].dtype}; conviértela con pd.to_datetime")
