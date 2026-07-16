from gemini_client import llamar_gemini

from state import inicializar_estado, append_user_msg, append_model_msg, ultimos_n_mensajes
from logic import maybe_uptdate_summary
from prompts import PLANTILLA
from config import WINDOW

# Función para imprimir métricas de la llamada
def imprimir_metricas(respuesta) -> None:
    print("+++ Métricas del turno:")
    print(f"{'ms':<6} {'in':>6} {'out':>6} {'total':>6}")
    print("-" * 30)
    print(f"{respuesta[1].elapsed_ms:<6} {respuesta[1].prompt_tokens:>6} {respuesta[1].output_tokens:>6} {respuesta[1].total_tokens:>6}")

# DEMOSTRACIÓN con varios turnos
def demo() -> None:
    mensajes_usuario = [
    "Hola, me llamo Matías.",
    "Explica en 20 palabras quién fué el mejor físico del mundo.",
    "Dime en 10 palabras cuál es la mejor canción de los últimos 100 años.",
    "Reproduce con exactitud, sin añadir ni quitar nada, el turno 2 de nuestra conversación, indicando cual fue mi pregunta y cuál tu respuesta.",
    "Dime cómo me llamo. ",
    "Reproduce con exactitud, sin añadir ni quitar nada, el turno 10 de nuestra conversación, indicando cual fue mi pregunta y cuál tu respuesta."
]
    state = inicializar_estado()
 
    print("+++ Iniciando DEMOSTRACIÓN:")
    print("=" * 30 + "\n")
    for mensaje in mensajes_usuario:
        respuesta = llamar_gemini(PLANTILLA.format(
            window=WINDOW,
            historial_reciente=ultimos_n_mensajes(state, WINDOW),
            resumen=maybe_uptdate_summary(state),
            mensaje_del_usuario=mensaje
        ))
        print("+++ Pregunta: ")
        print(mensaje)
        print("+++ Respuesta: ")
        print(respuesta[0])
        imprimir_metricas(respuesta)
        print("=" * 30 + "\n")
        append_user_msg(state, mensaje)
        append_model_msg(state, respuesta[0])
    # print("=" * 50 + "\n")
    # print("--- STATE ---")
    # print("--- MESSAGES ---")
    # print(state["messages"])
    # print("--- SUMMARY ---")
    # print(state["summary"])
    print("=" * 10 + "\n")
    print("Fin de la DEMOSTRACIÓN")
    
    
demo()
