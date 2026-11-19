
# US-06: Configuración de los logs de TaxiTech

# Importamos el módulo de registros de Python
import logging

# Permite crear archivos de log con tamaño limitado
from logging.handlers import RotatingFileHandler

# Permite construir la ruta del archivo
from pathlib import Path


# Guardaremos el log junto a los archivos Python
RUTA_LOG = Path(__file__).with_name("taxitech.log")


# Creamos un logger con el nombre de la aplicación
logger = logging.getLogger("taxitech")

# Registraremos eventos INFO, WARNING y ERROR
logger.setLevel(logging.INFO)


# Evitamos añadir varios manejadores al mismo logger
if not logger.handlers:

    # Creamos un archivo de log con rotación
    manejador = RotatingFileHandler(
        RUTA_LOG,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    # Definimos el formato de cada registro
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Aplicamos el formato al archivo
    manejador.setFormatter(formato)

    # Conectamos el manejador con el logger
    logger.addHandler(manejador)

# Evitamos duplicar mensajes en otros loggers
logger.propagate = False
