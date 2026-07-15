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
    lines = []
    all_messages = state.get("messages", [])
    # -n * 2 ya que cada turno se compone de dos mensajes
    # de este modo se guardan n turnos
    for message in all_messages[-n*2:]:
        lines.append(f"Turno {message.get('turno')} - {message.get('role', 'user')}: {message.get('text', '')}")
    return "\n".join(lines)


# Función para convertir state["messages"] de una list[dict] a líneas de texto
# Turno 1 - user: Pregunta
# Turno 1 - model: Respuesta
def historial_como_texto(state:dict) -> str:
    lines = []
    for message in state.get("messages", []):
        lines.append(f"Turno {message.get('turno')} - {message.get('role', 'user')}: {message.get('text', '')}")
    return "\n".join(lines)


def set_summary(state: dict, summary:str) -> None:
    state["summary"] = (summary or "").strip()