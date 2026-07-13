"""
Constantes utilizadas por el módulo de contexto.

Este archivo centraliza toda la configuración relacionada con la
recuperación de información para evitar números mágicos repartidos
por el código y facilitar futuras modificaciones.

IMPORTANTE
----------
Este archivo únicamente contiene configuración.

No debe contener lógica de negocio ni funciones.
"""

# =============================================================================
# CONFIGURACIÓN DE RECUPERACIÓN DE CONTEXTO
# =============================================================================

# Número máximo de documentos que se enviarán al modelo.
MAX_DOCUMENTOS = 3

# Número máximo de preguntas frecuentes relacionadas.
MAX_FAQ = 2

# =============================================================================
# PUNTUACIÓN DEL ALGORITMO DE BÚSQUEDA
# =============================================================================

# Coincidencia con una etiqueta (tag).
PUNTOS_TAG = 5

# Coincidencia con el título del documento.
PUNTOS_TITULO = 3

# Coincidencia dentro del cuerpo del documento.
PUNTOS_CUERPO = 1

# Bonificación cuando el documento pertenece al mismo departamento
# que el empleado que realiza la consulta.
BONIFICACION_DEPARTAMENTO = 2