# Estado de la sesión del chat con el modelo

def inicializar_estado() -> dict:
    return {
        "messages": [] # Historial del mensajes: {"role": "user"|"model", "text": str}
    }

# Añadir al estado el mensaje del usuario
def append_user_msg(state: dict, texto: str) -> None:
    state["messages"].append({"role": "user", "text": texto.strip()})
    
# Añadir al estado la respuesta del modelo
def append_model_msg(state: dict, texto: str) -> None:
    state["messages"].append({"role": "model", "text": texto.strip()})