from gemini_client import llamar_gemini

from state import inicializar_estado, append_user_msg, append_model_msg
from prompts import PLANTILLA

# Función para imprimir métricas de la llamada
def imprimir_metricas(respuesta) -> None:
    print("+++ Métricas del turno:")
    print(f"{'ms':<6} {'in':>6} {'out':>6} {'total':>6}")
    print("-" * 30)
    print(f"{respuesta[1].elapsed_ms:<6} {respuesta[1].prompt_tokens:>6} {respuesta[1].output_tokens:>6} {respuesta[1].total_tokens:>6}")

# DEMOSTRACIÓN con varios turnos
def demo() -> None:
    llamadas = [
    "Hola, me llamo Matías.",
    "Explica en 20 palabras quién fué el mejor físico del mundo.",
    "Dime en 10 palabras cuál es la mejor canción de los últimos 100 años.",
    "Dime cómo me llamo. ",
    "Reproduce con exactitud, sin añadir ni quitar nada, el segundo turno de nuestra conversación, indicando cual fue mi pregunta y cuál tu respuesta."
]
    state = inicializar_estado()
 
    print("+++ Iniciando DEMOSTRACIÓN:")
    print("=" * 30 + "\n")
    for llamada in llamadas:
        respuesta = llamar_gemini(PLANTILLA.format(
            historial=state,
            mensaje_del_usuario=llamada
        ))
        print("+++ Pregunta: ")
        print(llamada)
        print("+++ Respuesta: ")
        print(respuesta[0])
        imprimir_metricas(respuesta)
        print("=" * 30 + "\n")
        append_user_msg(state, llamada)
        append_model_msg(state, respuesta[0])
    print("=" * 50 + "\n")
    print("--- STATE ---")
    print(state)
    print("=" * 10 + "\n")
    print("Fin de la DEMOSTRACIÓN")
    
    
demo()
