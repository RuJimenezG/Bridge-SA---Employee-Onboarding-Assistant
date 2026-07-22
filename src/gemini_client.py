# Módulos estándar necesarios
import time
from dataclasses import dataclass

# Módulo de Gemini
from google import genai
from google.genai import types

# Dependencias de módulos dentro del proyecto
from config import MODEL, TEMPERATURE, TEMPERATURE_RESUMEN, MAX_PROMPT_TOKENS
from gemini_auth import configurar_gemini_api_key

configurar_gemini_api_key()


# Contenedor de datos optimizado automáticamente por el decorador dataclass para almacenar métricas de la API
@dataclass
class MetricasLlamada:
    elapsed_ms: int
    prompt_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None


# Variable global, el convenio dice que el guión bajo se utiliza para variables internas
_client_instance: genai.Client | None = None


# Función de inicialización del cliente
def _client() -> genai.Client:
    global _client_instance
    if _client_instance is None:
        _client_instance = genai.Client()
    return _client_instance


# Función para extraer las métricas de la respuesta y guardarlas en un objeto MetricasLlamada
def _metrics_from_response(response, started: float) -> MetricasLlamada:
    elapsed_ms = int((time.time() - started) * 1000)
    um = response.usage_metadata
    return MetricasLlamada(
        elapsed_ms = elapsed_ms,
        prompt_tokens = getattr(um, "prompt_token_count", None),
        output_tokens = getattr(um, "candidates_token_count", None),
        total_tokens = getattr(um, "total_token_count", None)
    )
    

# Función para llamar a Gemini, pasarle un prompt y que devuelva una tupla que contiene un string con la respuesta y un objeto MetricasLlamada
def llamar_gemini(prompt: str, system_prompt: str, temperature: float = TEMPERATURE, json_switch: bool = False) -> tuple[str, MetricasLlamada]:
    # Tiempo inicial
    started = time.time()
    # Respuesta
    response = _client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json" if json_switch == True else "",
            system_instruction=system_prompt
            )
    )
    return (response.text or "").strip(), _metrics_from_response(response, started)


# Función para solicitar al LLM el resumen de la conversación pasándole el historial
def llamar_gemini_resumen(prompt: str) -> str:
    texto, _ = llamar_gemini(prompt, temperature=TEMPERATURE_RESUMEN)
    return texto


# Función para contar tokens
def count_tokens(contents: str) -> int:
    tokens = _client().models.count_tokens(model=MODEL, contents=contents)
    return int(tokens.total_tokens or 0)


# Función para comprobar si se exceden los tokens del prompt antes de llamar a Gemini
def safe_generate(prompt:str, system_prompt: str, temperature = TEMPERATURE, json_switch: bool = False) -> tuple[str, MetricasLlamada]:
    tokens_prompt = count_tokens(prompt)
    if tokens_prompt > MAX_PROMPT_TOKENS:
        raise ValueError(
            f"Prompt demasiado grande: {tokens_prompt}. El máximo de tokens permitido es {MAX_PROMPT_TOKENS}"
        )
    return llamar_gemini(prompt, system_prompt, temperature, json_switch)