# Configuración del asistente

# Modelo de lenguaje utilizado
MODEL = "gemini-3.1-flash-lite"
# Segundo modelo propuesto para el benchmark "gemma-4-31b-it"
TEMPERATURE = 0.3
TEMPERATURE_RESUMEN = 0.2
TEMPERATURE_JSON = 0.0

# Número máximo de tokens permitidos en el prompt
MAX_PROMPT_TOKENS = 4000

# Ventana de mensajes recientes enviados al modelo. Indica el número de turnos que se envían. Cada turno tiene dos mensajes (user y model)
WINDOW = 4

# Frecuencia con la que se realiza resumen completo de la conversación para enviar al LLM. Indicar número de turnos.
RESUMIR_CADA = 8