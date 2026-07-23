

from config import RESUMIR_CADA, WINDOW, TEMPERATURE_JSON
from gemini_client import MetricasLlamada
from state import historial_como_texto, set_summary, ultimos_n_mensajes, append_user_msg, append_model_msg, inicializar_estado
from prompts import build_resumen_prompt, build_question_prompt, build_checklist_prompt, SYSTEM_PROMPT_CONSULTA, SYSTEM_PROMPT_CHECKLIST
from gemini_client import llamar_gemini_resumen, safe_generate
from context import seleccionar_faq, seleccionar_documento, determinar_escalado, obtener_contacto_escalado, recargar_cache, cargar_empleados_demo
from validators import validar

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
# - Genera el prompt
# - Hace la llamada con safe_generate
# - Guarda los mensajes con append_X_msg
# - Solicita el resumen de la conversación
# - Devuelve una respuesta con estado (ok o error), mensaje y datos.
def responder_consulta(state: dict, consulta: str) -> dict:
    # 1. Obtener los datos intermedios
    recargar_cache()
    departamento_usuario = state.get("user_profile", {}).get("departamento")   
    manager_usuario = state.get("user_profile", {}).get("manager")
    faq_entries = seleccionar_faq(consulta)
    documents = seleccionar_documento(consulta, departamento=departamento_usuario) 
    # 2. Calcular el escalado
    escalation = determinar_escalado(consulta)
    contacto_escalado = obtener_contacto_escalado(escalation, manager_usuario)
    # 3. Construir el prompt con todas las variables ya listas
    prompt = build_question_prompt(
        faq_entries=faq_entries,
        documents=documents,
        escalation=(escalation, contacto_escalado),
        profile=state.get("user_profile"),
        recent_messages=ultimos_n_mensajes(state, WINDOW),
        summary=state.get("summary", ""),
        consulta=consulta
    )
    # 4. Hacer la llamada al LLM
    try:
        texto, metricas = safe_generate(prompt, system_prompt=SYSTEM_PROMPT_CONSULTA)
    except ValueError as e:
        return respuesta_error("Contexto demasiado grande", [str(e)])
    # 5. Guardar los mensajes y correr turno
    append_user_msg(state, consulta)
    append_model_msg(state, texto)
    # 6. Actualizar el resumen de la conversación si es necesario
    converascion_resumida = maybe_uptdate_summary(state)
    # 7. Devolver respuesta
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


# Función de orquestación para devolver checklist
# - Genera el prompt
# - Hace la llamada con safe_generate
# - Guarda los mensajes con append_X_msg
# - Solicita el resumen de la conversación
# - Devuelve una respuesta con estado (ok o error), mensaje y datos.
def responder_checklist_diario(state: dict, consulta: str) -> dict:
    # 1. Obtener los datos intermedios
    recargar_cache()
    departamento_usuario = state.get("user_profile", {}).get("departamento")
    faq_entries = seleccionar_faq(consulta)
    documents = seleccionar_documento(consulta, departamento=departamento_usuario, max_docs=5) 
    # 2. Construir el prompt con todas las variables ya listas
    prompt = build_checklist_prompt(
        faq_entries=faq_entries,
        documents=documents,
        profile=state.get("user_profile"),
        consulta=consulta
    )
    # 3. Hacer la llamada al LLM
    try:
        texto, metricas = safe_generate(prompt, system_prompt=SYSTEM_PROMPT_CHECKLIST, temperature=TEMPERATURE_JSON, json_switch = True)
    except ValueError as e:
        return respuesta_error("Contexto demasiado grande", [str(e)])
    # 4. Guardar los mensajes y correr turno
    append_user_msg(state, consulta)
    append_model_msg(state, texto)
    # 5. Actualizar el resumen de la conversación si es necesario
    converascion_resumida = maybe_uptdate_summary(state)
    # 6. Devolver respuesta
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
    

# Función para decidir si se devuelve checklist o se responde consulta
def decidir_checklist_o_consulta(state: dict, consulta: str) -> dict:
    # 1. Validación inicial
    validacion_ok, error_en_validacion = validar(consulta)
    if not validacion_ok:
        return respuesta_error("Se produjo un error al validar el input.", [error_en_validacion])
    # 2. Obtener los datos intermedios y establecer condiciones
    empleados = cargar_empleados_demo()
    check_nombre = False
    check_contenido = False
    # 3. Comprobar primera condición, aparición del nombre de empleado en la consulta
    for empleado in empleados:
        for palabra in empleado.get("nombre").split():
            if palabra in consulta:
                check_nombre = True
                break
    # 4. Comprobar segunda condicioón aparición de emp y día en el mensaje
    if "emp" in consulta and ("dia" in consulta or "día" in consulta):
        check_contenido = True
    # 5. Hacer la llamada correspondiente según las condiciones cumplidas
    if check_nombre == True and check_contenido == True:
        return responder_checklist_diario(state, consulta)
    else:
        return responder_consulta(state, consulta)
    

def chat_interactivo():
    print("==================================================")
    print("   Iniciando Chat con Memoria en Bucle Activo")
    print("   Escribe 'salir', 'exit' o 'q' para terminar.")
    print("==================================================\n")
    
    # 1. Inicializar el estado una sola vez antes de entrar al bucle
    # Esto mantiene la memoria de la sesión activa en la RAM de Python
    empleados = cargar_empleados_demo()
    state = inicializar_estado(empleados[0])
    # 2. Iniciamor el bucle interactivo de turnos
    while True:
        try:
            # Capturar el prompt del usuario desde la terminal
            pregunta_usuario = input("\n[Tú] > ")
            # Condición de salida para romper el bucle y terminar la sesión de Python
            if pregunta_usuario.strip().lower() in ["salir", "exit", "q", "quit"]:
                print("\nTerminando sesión de chat. ¡Hasta luego!")
                break
            if not pregunta_usuario.strip():
                continue # Evita procesar strings vacíos
            # Llamar a Gemini con una de las dos funcionalidades
            resultado = decidir_checklist_o_consulta(state, pregunta_usuario)
            
            if resultado.get("status") == "ok":
                respuesta_llm = resultado["data"]["respuesta"]
                metricas = resultado["data"].get("metricas", {})
                              
                # Imprimir la respuesta en pantalla
                print(f"\n[Asistente] > {respuesta_llm}")
                
                # Imprimir métricas útiles de tokens para auditar el consumo
                print(f"--- [Métricas de llamada]: {metricas.get('total_tokens', 0)} tokens totales | Latencia: {metricas.get('elapsed_ms', 0)}ms ---")
            else:
                print(f"\n[Error]: {resultado.get('mensaje')}")
                
        except KeyboardInterrupt:
            # Permite salir limpiamente pulsando Ctrl+C en la terminal
            print("\n\nSesión interrumpida con Ctrl+C. ¡Hasta luego!")
            break
