"""
Módulo encargado de recuperar el contexto necesario para responder
preguntas relacionadas con el proceso de onboarding.

Responsabilidades del módulo:
- Cargar la información almacenada en los archivos JSON.
- Recuperar empleados.
- Recuperar documentación.
- Recuperar preguntas frecuentes.
- Construir el contexto que posteriormente utilizará el modelo.

IMPORTANTE:
Este módulo NO realiza llamadas al modelo Gemini.
Su única responsabilidad es gestionar y recuperar información.
"""

import json

from functools import lru_cache
from pathlib import Path
from typing import Any

from context_rules import (
    BONIFICACION_DEPARTAMENTO,
    MAX_DOCUMENTOS,
    MAX_FAQ,
    PUNTOS_CUERPO,
    PUNTOS_TAG,
    PUNTOS_TITULO,
)

# =============================================================================
# RUTAS DEL PROYECTO
# =============================================================================

# Directorio raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio donde se encuentran todos los archivos JSON.
DATA_DIR = BASE_DIR / "data"


# =============================================================================
# FUNCIONES PRIVADAS
# =============================================================================

@lru_cache(maxsize=None)
def _cargar_json(nombre_archivo: str) -> Any:
    """
    Carga un archivo JSON desde el directorio de datos.

    La información se almacena en memoria mediante caché para evitar
    leer repetidamente el mismo archivo durante la ejecución.

    Args:
        nombre_archivo:
            Nombre del archivo JSON.

    Returns:
        Contenido del archivo JSON.

    Raises:
        FileNotFoundError:
            Si el archivo no existe.

        ValueError:
            Si el contenido del archivo no es un JSON válido.
    """

    ruta = DATA_DIR / nombre_archivo

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo '{ruta}'."
        )

    try:
        with ruta.open(
            mode="r",
            encoding="utf-8"
        ) as archivo:
            return json.load(archivo)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo '{nombre_archivo}' no contiene un JSON válido."
        ) from error


# =============================================================================
# CARGA DE DATOS
# =============================================================================

@lru_cache(maxsize=None)
def cargar_empresa() -> dict:
    """
    Devuelve la información general de la empresa.

    Returns:
        Diccionario con la información de la empresa.
    """
    return _cargar_json("empresa.json")


@lru_cache(maxsize=None)
def cargar_empleados() -> list:
    """
    Devuelve la lista de empleados de demostración.

    Returns:
        Lista con los empleados disponibles.
    """
    return _cargar_json("empleados_demo.json")


@lru_cache(maxsize=None)
def cargar_documentos() -> list:
    """
    Devuelve la documentación utilizada durante el onboarding.

    Returns:
        Lista con todos los documentos disponibles.
    """
    return _cargar_json("onboarding_docs.json")


@lru_cache(maxsize=None)
def cargar_faq() -> list:
    """
    Devuelve la lista de preguntas frecuentes.

    Returns:
        Lista con las FAQ disponibles.
    """
    return _cargar_json("faq_onboarding.json")