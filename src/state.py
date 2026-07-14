# Estado de la sesión del chat con el modelo

def inicializar_estado() -> dict:
    return {
        "messages": [], # Historial del mensajes: {"turno": turno del mensaje, "role": "user"|"model", "text": str}
        "summary": "",
        "turnos": 0
    }

# Añadir al estado el mensaje del usuario
def append_user_msg(state: dict, texto: str) -> None:
    turno_actual = state.get("turnos", 0) + 1
    state["messages"].append({"turno": turno_actual, "role": "user", "text": texto.strip()})
    
# Añadir al estado la respuesta del modelo
def append_model_msg(state: dict, texto: str) -> None:
    turno_actual = state.get("turnos", 0) + 1
    state["messages"].append({"turno": turno_actual, "role": "model", "text": texto.strip()})
    state["turnos"] = turno_actual
    
# Función para devolver los últimos n mensajes configurados en WINDOW
def ultimos_n_mensajes (state: dict, n: int) -> list[dict]:
    all_messages = state.get("messages", [])
    return all_messages[-n:] if n > 0 else []