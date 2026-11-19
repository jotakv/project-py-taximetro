
# US-07: Configuración externa de tarifas

# Importamos json para leer archivos JSON
import json

# Importamos math para validar números
import math

# Importamos Path para localizar archivos
from pathlib import Path


# Archivo que contiene los precios configurables
RUTA_CONFIGURACION = Path(__file__).with_name(
    "tarifas.json"
)


# Función para cargar las tarifas del archivo
def cargar_tarifas():

    # Abrimos y leemos el archivo JSON
    with RUTA_CONFIGURACION.open(
        "r", encoding="utf-8"
    ) as archivo:

        datos = json.load(archivo)

    # Comprobamos que el JSON contiene un objeto
    if not isinstance(datos, dict):
        raise ValueError(
            "La configuración debe ser un objeto JSON."
        )

    # Obtenemos los precios de cada estado
    parado = datos.get("tarifa_parado")
    movimiento = datos.get("tarifa_movimiento")

    # Validamos los dos precios
    for nombre, valor in [
        ("tarifa_parado", parado),
        ("tarifa_movimiento", movimiento)
    ]:

        # Debe ser un número, no un texto ni un booleano
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
        ):
            raise ValueError(
                f"La tarifa {nombre} debe ser numérica."
            )

        # No aceptamos precios negativos o infinitos
        if not math.isfinite(valor) or valor < 0:
            raise ValueError(
                f"La tarifa {nombre} no es válida."
            )

    # Devolvemos los precios para utilizarlos
    return float(parado), float(movimiento)
