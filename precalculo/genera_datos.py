"""Datos del caso «Tingua Domicilios S.A.S.» (empresa FICTICIA).

Genera datos/pedidos.csv: los 12 000 pedidos que la plataforma entregó entre el
1 de enero y el 30 de junio de 2026 en cinco ciudades. Todo se inventa con una
semilla fija: los datos no corresponden a personas ni a empresas reales.

Solo usa la biblioteca estándar y, del generador aleatorio, solo random(), que
es lo único que Python garantiza igual entre versiones. Por eso la tabla sale
idéntica en Colab y en cualquier computador.

El caso sirve para todo el curso: variables de todos los tipos (sesión 1),
asimetrías y algunos atípicos (medidas y datos atípicos), una población
completa de la que se pueden sacar muestras (muestreo) y un tiempo de entrega
que depende de la distancia, la lluvia y otras variables (regresión).
"""

import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 2026
N_PEDIDOS = 12_000
INICIO = date(2026, 1, 1)
DIAS = 181  # del 1 de enero al 30 de junio de 2026

COLUMNAS = ["id_pedido", "fecha", "franja", "ciudad", "categoria", "n_productos",
            "valor_pedido", "medio_pago", "estrato", "suscriptor", "distancia_km",
            "lluvia", "temperatura_c", "tiempo_entrega_min", "calificacion"]

# ciudad: (peso, temperatura media °C, desviación, prob. de lluvia, minutos extra, factor de distancia)
CIUDADES = {
    "Bogotá":       (0.40, 14.5, 2.2, 0.30, 5.0, 1.15),
    "Medellín":     (0.22, 22.5, 2.3, 0.28, 2.0, 1.00),
    "Cali":         (0.16, 25.0, 2.3, 0.22, 0.0, 1.00),
    "Barranquilla": (0.12, 29.0, 1.8, 0.12, -1.0, 0.95),
    "Bucaramanga":  (0.10, 23.5, 2.2, 0.20, -2.0, 0.90),
}
LLUVIA_MES = {1: 0.6, 2: 0.7, 3: 1.0, 4: 1.4, 5: 1.3, 6: 0.8}

# franja: (peso, ajuste de temperatura °C, minutos extra)
FRANJAS = {
    "Mañana":   (0.15, -1.5, 0.0),
    "Almuerzo": (0.35, 1.5, 4.0),
    "Tarde":    (0.20, 1.0, 0.0),
    "Noche":    (0.30, -2.0, 3.0),
}

# categoría: (productos extra en promedio, precio medio por producto en COP, minutos de preparación)
CATEGORIAS = {
    "Restaurante": (1.3, 27_000, 3.0),
    "Mercado":     (6.0, 8_500, 4.0),
    "Farmacia":    (0.9, 21_000, 0.0),
    "Mascotas":    (1.2, 36_000, 1.0),
    "Floristería": (0.2, 88_000, 2.0),
}
# Qué se pide en cada franja (mismo orden que CATEGORIAS)
CATEGORIA_POR_FRANJA = {
    "Mañana":   (0.30, 0.35, 0.20, 0.10, 0.05),
    "Almuerzo": (0.78, 0.08, 0.07, 0.04, 0.03),
    "Tarde":    (0.40, 0.25, 0.15, 0.12, 0.08),
    "Noche":    (0.70, 0.10, 0.12, 0.05, 0.03),
}
ESTRATOS = {1: 0.06, 2: 0.22, 3: 0.33, 4: 0.20, 5: 0.11, 6: 0.08}


class _Azar:
    """Lo que hace falta del azar, construido solo sobre random()."""

    def __init__(self, semilla):
        self.r = random.Random(semilla)

    def u(self):
        return self.r.random()

    def elegir(self, opciones, pesos):
        x, acum = self.u() * sum(pesos), 0.0
        for opcion, peso in zip(opciones, pesos):
            acum += peso
            if x < acum:
                return opcion
        return opciones[-1]

    def normal(self, media=0.0, desv=1.0):
        # Box-Muller
        u1, u2 = 1.0 - self.u(), self.u()
        return media + desv * math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    def exponencial(self, media):
        return -media * math.log(1.0 - self.u())

    def poisson(self, lam):
        # Knuth: suficiente para medias pequeñas
        limite, k, p = math.exp(-lam), 0, 1.0
        while True:
            p *= self.u()
            if p <= limite:
                return k
            k += 1


def _redondear(x, decimales=0):
    factor = 10 ** decimales
    return math.floor(x * factor + 0.5) / factor


def _pedido(az, dias, pesos_dias):
    fecha = az.elegir(dias, pesos_dias)
    ciudad = az.elegir(list(CIUDADES), [v[0] for v in CIUDADES.values()])
    _, t_media, t_desv, p_lluvia, min_ciudad, f_dist = CIUDADES[ciudad]
    franja = az.elegir(list(FRANJAS), [v[0] for v in FRANJAS.values()])
    _, t_franja, min_franja = FRANJAS[franja]
    categoria = az.elegir(list(CATEGORIAS), CATEGORIA_POR_FRANJA[franja])
    extra, precio, min_prep = CATEGORIAS[categoria]
    estrato = az.elegir(list(ESTRATOS), list(ESTRATOS.values()))

    suscriptor = az.u() < 0.10 + 0.06 * (estrato - 1)
    p_efectivo = 0.45 - 0.07 * (estrato - 1)
    medio_pago = az.elegir(["Efectivo", "Billetera digital", "Tarjeta"],
                           [p_efectivo, 0.25, 1 - p_efectivo - 0.25])

    n = 1 + az.poisson(extra)
    if categoria in ("Mercado", "Restaurante") and az.u() < 0.003:
        n = 20 + int(az.u() * 26)  # pedido corporativo: pocos, pero existen
    valor = n * precio * math.exp(az.normal(0, 0.22)) * (1 + 0.07 * (estrato - 3))
    valor = max(3_000, _redondear(valor / 100) * 100)

    distancia = math.exp(az.normal(math.log(3.0), 0.5)) * f_dist
    distancia = min(14.0, max(0.4, _redondear(distancia, 1)))

    lluvia = az.u() < p_lluvia * LLUVIA_MES[fecha.month]
    temperatura = _redondear(az.normal(t_media + t_franja - 1.8 * lluvia, t_desv), 1)

    tiempo = (11 + 3.1 * distancia + 0.45 * min(n, 15) + min_prep + min_franja + min_ciudad
              + 7.5 * lluvia - 2.5 * suscriptor + az.normal(0, 4) + az.exponencial(3))
    if az.u() < 0.005:
        tiempo += 55 + 95 * az.u()  # pedidos que se demoraron muchísimo
    tiempo = max(6.0, _redondear(tiempo, 1))

    latente = 6.4 - 0.065 * tiempo + 0.2 * suscriptor + az.normal(0, 0.6)
    estrellas = int(min(5, max(1, math.floor(latente + 0.5))))
    califico = az.u() < (0.80 if tiempo > 55 else 0.58)

    return {
        "fecha": fecha, "franja": franja, "ciudad": ciudad, "categoria": categoria,
        "n_productos": n, "valor_pedido": int(valor), "medio_pago": medio_pago,
        "estrato": estrato, "suscriptor": "Sí" if suscriptor else "No",
        "distancia_km": distancia, "lluvia": "Sí" if lluvia else "No",
        "temperatura_c": temperatura, "tiempo_entrega_min": tiempo,
        "calificacion": estrellas if califico else "",
    }


def crear_datos(carpeta="datos"):
    """Escribe <carpeta>/pedidos.csv y devuelve su ruta."""
    az = _Azar(SEMILLA)
    dias = [INICIO + timedelta(days=d) for d in range(DIAS)]
    pesos_dias = [1.35 if d.weekday() >= 4 else 1.0 for d in dias]  # viernes a domingo, más pedidos
    pedidos = [_pedido(az, dias, pesos_dias) for _ in range(N_PEDIDOS)]
    orden_franja = list(FRANJAS)
    pedidos.sort(key=lambda p: (p["fecha"], orden_franja.index(p["franja"])))

    ruta = Path(carpeta) / "pedidos.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUMNAS)
        escritor.writeheader()
        for i, p in enumerate(pedidos, start=1):
            escritor.writerow({"id_pedido": f"P{i:05d}", **p, "fecha": p["fecha"].isoformat()})
    print(f"Listo: {ruta} con {N_PEDIDOS:,} pedidos y {len(COLUMNAS)} columnas".replace(",", "."))
    return ruta


if __name__ == "__main__":
    import sys
    crear_datos(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "datos"))
