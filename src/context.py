"""
Módulo encargado de recuperar el contexto necesario para responder
preguntas relacionadas con el proceso de onboarding.

Responsabilidades
-----------------
- Cargar la información almacenada en los archivos JSON.
- Recuperar empleados.
- Recuperar documentación.
- Recuperar preguntas frecuentes.
- Construir el contexto que posteriormente utilizará el modelo.

Este módulo NO realiza llamadas al modelo Gemini.
Su única responsabilidad es gestionar y recuperar información.

IMPORTANTE PARA EL EQUIPO
-------------------------
Este módulo actuará como la puerta de acceso a todos los datos del
asistente.

Los demás módulos del proyecto NO deberían leer directamente los
archivos JSON. En su lugar deberán utilizar las funciones públicas
definidas aquí.

De esta forma toda la lógica de acceso a datos permanecerá centralizada
en un único lugar.
"""

import json

from functools import lru_cache
from pathlib import Path
from typing import Any


# =============================================================================
# RUTAS DEL PROYECTO
# =============================================================================

# Directorio raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio que contiene todos los archivos JSON.
DATA_DIR = BASE_DIR / "data"


# =============================================================================
# FUNCIONES PRIVADAS
# =============================================================================

def _obtener_ruta(nombre_archivo: str) -> Path:
    """
    Construye la ruta absoluta de un archivo ubicado dentro del
    directorio de datos del proyecto.

    Args:
        nombre_archivo:
            Nombre del archivo JSON.

    Returns:
        Ruta completa al archivo solicitado.
    """

    return DATA_DIR / nombre_archivo


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
        dict | list:
            Contenido del archivo JSON.

    Raises:
        FileNotFoundError:
            Si el archivo no existe.

        ValueError:
            Si el contenido del archivo no es un JSON válido.
    """

    ruta = _obtener_ruta(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta}"
        )

    try:
        with ruta.open(
            mode="r",
            encoding="utf-8"
        ) as archivo:

            contenido = json.load(archivo)

        return contenido

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo '{nombre_archivo}' no contiene un JSON válido."
        ) from error


# =============================================================================
# FUNCIONES PÚBLICAS DE CARGA
# =============================================================================

@lru_cache(maxsize=None)
def cargar_empresa() -> dict[str, Any]:
    """
    Recupera la información general de la empresa.

    Returns:
        Diccionario con la información de la empresa.
    """

    return _cargar_json("empresa.json")


@lru_cache(maxsize=None)
def cargar_empleados() -> list[dict[str, Any]]:
    """
    Recupera la lista de empleados disponibles para las demostraciones.

    Returns:
        Lista de empleados.
    """

    return _cargar_json("empleados_demo.json")


@lru_cache(maxsize=None)
def cargar_documentos() -> list[dict[str, Any]]:
    """
    Recupera toda la documentación del proceso de onboarding.

    Returns:
        Lista con todos los documentos disponibles.
    """

    return _cargar_json("onboarding_docs.json")


@lru_cache(maxsize=None)
def cargar_faq() -> list[dict[str, Any]]:
    """
    Recupera las preguntas frecuentes del proceso de onboarding.

    Returns:
        Lista de preguntas frecuentes.
    """

    return _cargar_json("faq_onboarding.json")