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
PLANTILLA_CONSULTA = """
Responde al mensaje del usuario teniendo en cuenta el historial de la conversación mantenida con él hasta ahora. Este historial está formado por los últimos mensajes y un resumen de la conversación completa.

{perfil_del_empleado}

{historial_reciente}

{resumen}

{mensaje_del_usuario}
"""

# Función para construir el prompt que solicita el resumen al LLM
def build_resumen_prompt(historial: str, max_puntos: int = 6) -> str:
    return PLANTILLA_RESUMEN.format(max_puntos=max_puntos, historial=historial.strip())


# Función para construir en modo texto el bloque del perfil que se le pasa al LLM
def build_profile_block(profile: dict) -> str:
    if not profile:
        return ""
    return(
        "--- PERFIL DEL EMPLEADO ---\n"
        f"id: {profile.get('id', 'desconocido')}\n"
        f"nombre: {profile.get('nombre', 'desconocido')}\n"
        f"departamento: {profile.get('departamento', 'desconocido')}\n"
        f"rol: {profile.get('rol', 'desconocido')}\n"
        f"fecha_inicio: {profile.get('fecha_inicio', 'desconocido')}\n"
        f"manager: {profile.get('manager', 'desconocido')}\n"
        f"modalidad: {profile.get('modalidad', 'remoto')}\n"
        f"ubicacion: {profile.get('ubicacion', 'desconocido')}\n"
        f"idioma_preferido: {profile.get('idioma_preferido', 'es')}\n"
        f"perfil: {profile.get('perfil', 'desconocido')}\n"
        "--- FIN DEL PERFIL DEL EMPLEADO ---"
    )

# Función para construir en modo texto el bloque de los últimos turnos que se le pasa al LLM
def build_history_block(historial_reciente: str) -> str:
    if not historial_reciente:
        return ""
    return (
        f"--- HISTORIAL DE CONVERSACIÓN DE LOS ÚLTIMOS TURNOS ---\n"
        "{historial_reciente}\n"
        f"--- FIN DEL HISTORIAL DE CONVERSACIÓN DE LOS ÚLTIMOS TURNOS ---"
    )
    
# Función para construir en modo texto el bloque de resumen que se le pasa al LLM
def build_summary_block(summary: str) -> str:
    if not summary:
        return ""
    return (
        f"--- RESUMEN DE TODA LA CONVERSACIÓN HASTA AHORA ---\n"
        f"{summary}\n"
        f"--- FIN DEL MENSAJE DEL USUARIO ---"
    )


# Función para construir en modo texto el bloque de mensaje del usuario que se le pasa al LLM
def build_question_block(question: str) -> str:
    if not question:
        return ""
    return (
        f"--- NUEVO MENSAJE DEL USUARIO ---\n"
        f"{question}"
        f"--- FIN DEL RESUMEN DE TODA LA CONVERSACIÓN HASTA AHORA ---\n"
    )


# Función para construir el prompt que se le pasa al LLM
def build_question_prompt(profile: dict, recent_messages: str, summary: str, consulta: str) -> str:
    return PLANTILLA_CONSULTA.format(
        perfil_del_empleado=build_profile_block(profile),
        historial_reciente=build_history_block(recent_messages),
        resumen=build_summary_block(summary),
        mensaje_del_usuario=build_question_block(consulta)
    )