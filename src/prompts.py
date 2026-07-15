# Plantillas y construcción de prompts

# Plantilla para pedir al LLM el resumen que luego le pasaremos al mismo LLM como contexto o "memoria" de la conversación.
PLANTILLA_RESUMEN = """
Eres un asistente que resume conversaciones mantenidas con un LLM dedicado a dar asistencia en el onboarding de una compañía. Vas a recibir un texto que incluye todo el historial de la conversación, indicando el número de turno de la misma, el rol de quién escribe cada mensaje (user o model) y el texto del mensaje.


Tarea: resume el texto en {max_puntos} puntos clave.
Reglas:
- No inventes ningún dato.
- Conserva nombres, temas de sobre los que se ha preguntado y preferencias del usuario.
- Devuelve solo la lista en texto plano.

El resumen debe ser óptimo para dar contexto al asistente de onboarding y que recuerde apropiadamente la conversación mantenida hasta ahora.

--- HISTORIAL DE LA CONVERSACIÓN A RESUMIR ---:
{historial}
"""


# Plantilla con envío de historial y mensaje del usuario
PLANTILLA = """
Responde al mensaje del usuario teniendo en cuenta el historial de la conversación mantenida con él hasta ahora. Este historial está formado por los últimos {window} mensajes y un resumen de la conversación completa.

--- HISTORIAL DE CONVERSACIÓN DE LOS ÚLTIMOS {window} MENSAJES ---
{historial_reciente}
--- FIN DEL HISTORIAL DE CONVERSACIÓN DE LOS ÚLTIMOS {window} MENSAJES ---

--- RESUMEN DE TODA LA CONVERSACIÓN HASTA AHORA ---
{resumen}
--- FIN DEL RESUMEN DE TODA LA CONVERSACIÓN HASTA AHORA ---

--- NUEVO MENSAJE DEL USUARIO ---
{mensaje_del_usuario}
--- FIN DEL MENSAJE DEL USUARIO ---
"""

# Función para construir el prompt que solicita el resumen al LLM
def build_resumen_prompt(historial: str, max_puntos: int = 6) -> str:
    return PLANTILLA_RESUMEN.format(max_puntos=max_puntos, historial=historial.strip())

