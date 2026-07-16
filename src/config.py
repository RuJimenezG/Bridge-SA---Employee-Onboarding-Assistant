# Configuración del asistente

# Modelo de lenguaje utilizado
MODEL = "gemini-3.1-flash-lite"
TEMPERATURE = 0.3
TEMPERATURE_RESUMEN = 0.2

# Ventana de mensajes recientes enviados al modelo. Indica el número de turnos que se envían. Cada turno tiene dos mensajes (user y model)
WINDOW = 2

# Frecuencia con la que se realiza resumen completo de la conversación para enviar al LLM. Indicar número de turnos.
RESUMIR_CADA = 4