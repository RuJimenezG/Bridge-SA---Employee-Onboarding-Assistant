# Plantillas y construcción de prompts

# Plantilla con envío de historial y mensaje del usuario
PLANTILLA = """
Responde al mensaje del usuario teniendo en cuenta el historial de la conversación mantenida con él hasta ahora.

--- HISTORIAL DE CONVERSACIÓN HASTA AHORA ---
{historial}
--- FIN DEL HISTORIAL DE CONVERSACIÓN ---

--- NUEVO MENSAJE DEL USUARIO ---
{mensaje_del_usuario}
--- FIN DEL MENSAJE DEL USUARIO ---
"""
