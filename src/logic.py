

from config import RESUMIR_CADA
from gemini_client import MetricasLlamada
from state import historial_como_texto, set_summary
from prompts import build_resumen_prompt
from gemini_client import llamar_gemini_resumen

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


    

    
