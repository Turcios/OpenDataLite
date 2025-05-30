import os, sys


def obtener_ruta_recurso(nombre_archivo):
    """Retorna la ruta al recurso empaquetado (compatible con PyInstaller)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)