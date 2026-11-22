import logging
import os

CARPETA_LOGS = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(CARPETA_LOGS, exist_ok=True)

def configurar_logger(nombre, archivo):
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    ruta = os.path.join(CARPETA_LOGS, archivo)
    # Evita agregar manejadores repetidos si el módulo se importa varias veces.
    if not logger.handlers:
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger

eventos = configurar_logger("software_fj_eventos", "eventos.log")
errores = configurar_logger("software_fj_errores", "errores.log")
