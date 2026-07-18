from gemini_client import safe_generate

from state import inicializar_estado, append_user_msg, append_model_msg, ultimos_n_mensajes
from logic import maybe_uptdate_summary, responder_consulta
from prompts import PLANTILLA_CONSULTA
from config import WINDOW
from context import cargar_empleados_demo

# Función para imprimir métricas de la llamada
def imprimir_metricas(respuesta:dict) -> None:
    if respuesta.get("status") == "ok":
        print("+++ Métricas del turno:")
        print(f"{'ms':<6} {'in':>6} {'out':>6} {'total':>6}")
        print("-" * 30)
        print(f"{respuesta.get("data", {}).get("metricas").get("elapsed_ms"):<6} {respuesta.get("data", {}).get("metricas").get("prompt_tokens"):>6} {respuesta.get("data", {}).get("metricas").get("output_tokens"):>6} {respuesta.get("data", {}).get("metricas").get("total_tokens"):>6}")

# DEMOSTRACIÓN con varios turnos
def demo_test_memoria_y_contexto() -> None:
    mensajes_usuario = [
    "Hola, me llamo Matías.",
    "Explica en 20 palabras quién fué el mejor físico del mundo.",
    "Dime en 10 palabras cuál es la mejor canción de los últimos 100 años.",
    "Reproduce con exactitud, sin añadir ni quitar nada, el turno 2 de nuestra conversación, indicando cual fue mi pregunta y cuál tu respuesta.",
    "Dime cómo me llamo. ",
    "Reproduce con exactitud, sin añadir ni quitar nada, el turno 10 de nuestra conversación, indicando cual fue mi pregunta y cuál tu respuesta."
]  
    empleados = cargar_empleados_demo()
    state = inicializar_estado(empleados[1])
 
    print("+++ Iniciando DEMOSTRACIÓN:")
    print("=" * 30 + "\n")
    for mensaje in mensajes_usuario:
        respuesta = responder_consulta(state, mensaje)
        print("+++ Pregunta: ")
        print(mensaje)
        print("+++ Respuesta: ")
        if respuesta.get("status") == "ok":
            print(respuesta.get("data", {}).get("respuesta"))
            imprimir_metricas(respuesta)
        else:
            print(f"Status: {respuesta.get("status")} - {respuesta.get("mensaje")}")
            print("ERRORES: ")
            print(f"{respuesta.get("errores")}")
        print("=" * 30 + "\n")
    print("=" * 50 + "\n")
    print("--- STATE ---")
    print("--- MESSAGES ---")
    print(state["messages"])
    print("--- SUMMARY ---")
    print(state["summary"])
    print("=" * 10 + "\n")
    print("Fin de la DEMOSTRACIÓN")
    
# DEMOSTRACIÓN con varios turnos
def demo() -> None:
    mensajes_usuario = [
    "¿A qué canales de Slack tengo que unirme?",
    "¿Cuántos días de vacaciones tengo?",
    "No puedo entrar a mi cuenta de correo, ¿qué contraseña uso?",
    "¿Cuál es la prioridad del sprint de esta semana?",
    "¿Debo usar vpn para conectar a los recursos de la compañía?",
    "Hola, quería saludar al equipo",  # sin coincidencia -> fallback MANAGER
    "¿Me das una receta de croquetas ricas, por favor?"
]  
    empleados = cargar_empleados_demo()
    state = inicializar_estado(empleados[1])
 
    print("+++ Iniciando DEMOSTRACIÓN:")
    print("=" * 30 + "\n")
    for mensaje in mensajes_usuario:
        respuesta = responder_consulta(state, mensaje)
        print("+++ Pregunta: ")
        print(mensaje)
        print("+++ Respuesta: ")
        if respuesta.get("status") == "ok":
            print(respuesta.get("data", {}).get("respuesta"))
            imprimir_metricas(respuesta)
        else:
            print(f"Status: {respuesta.get("status")} - {respuesta.get("mensaje")}")
            print("ERRORES: ")
            print(f"{respuesta.get("errores")}")
        print("=" * 30 + "\n")
    print("=" * 50 + "\n")
    print("Fin de la DEMOSTRACIÓN")
    
demo()
