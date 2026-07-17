

from config import RESUMIR_CADA, WINDOW
from gemini_client import MetricasLlamada
from state import historial_como_texto, set_summary, ultimos_n_mensajes, append_user_msg, append_model_msg
from prompts import build_resumen_prompt, PLANTILLA_CONSULTA
from gemini_client import llamar_gemini_resumen,safe_generate

# Función para devolver una respuesta cuando hay un error
def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


# Función para devolver respuesta cuando todo va OK
def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


# Función para definir si es necesario resumir
def _debe_resumir(state:dict) -> bool:
    n = len(state.get("messages", []))
    return n >= (RESUMIR_CADA * 2) and n % (RESUMIR_CADA * 2) == 0


# Función para actualizar el resumen en caso necesario
def maybe_uptdate_summary(state:dict ) -> bool:
    if not _debe_resumir(state):
        return False
    historial = historial_como_texto(state)
    prompt = build_resumen_prompt(historial, max_puntos=6)
    summary = llamar_gemini_resumen(prompt)
    set_summary(state, summary)
    return True
    
# Función para convertir las métricas dentro de MetricasLlamada a un diccionario
def _metricas_a_dict(metricas: MetricasLlamada) -> dict:
    return{
        "elapsed_ms": metricas.elapsed_ms,
        "prompt_tokens": metricas.prompt_tokens,
        "output_tokens": metricas.output_tokens,
        "total_tokens": metricas.total_tokens,
    }


# Función de orquestación para responder consultas
# - Comprueba si hay mensaje del usuario
# - Genera el prompt
# - Hace la llamada con safe_generate
# - Guarda los mensajes con append_X_msg
# - Solicita el resumen de la conversación
# - Devuelve una respuesta con estado (ok o error), mensaje y datos.
def responder_consulta(state: dict, consulta: str) -> dict:
    # Se devuelve respuesta de error ad hoc para el caso de que la consulta esté vacía
    if not consulta.strip():
        return respuesta_error("Consulta vacía", ["La pregunta no puede estar vacía"])
    prompt = PLANTILLA_CONSULTA.format(
        window=WINDOW,
        historial_reciente=ultimos_n_mensajes(state, WINDOW),
        resumen=state.get("summary", ""),
        mensaje_del_usuario=consulta
    )
    try:
        texto, metricas = safe_generate(prompt)
    except ValueError as e:
        return respuesta_error("Contexto demasiado grande", [str(e)])
    
    append_user_msg(state, consulta)
    append_model_msg(state, texto)
    converascion_resumida = maybe_uptdate_summary(state)
    
    return respuesta_ok(
        "Respuesta generada",
        {
            "respuesta": texto,
            "resumen_actualizado": converascion_resumida,
            "summary": state.get("summary", ""),
            "metricas": _metricas_a_dict(metricas),
            "modo_contexto": "summary + ventana" if state.get("summary") else "ventana"
        }
    )
        
    
