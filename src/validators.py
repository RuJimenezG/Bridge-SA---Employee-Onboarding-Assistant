# Validación de entrada por caracteres (>0 & <2000)
MAX_CARACTERES = 2000

def validar_entrada(mensaje):
    if not mensaje or not mensaje.strip():
        return False, "Por favor, escribe una pregunta."
    if len(mensaje) > MAX_CARACTERES:
        return False, f"Tu mensaje es demasiado largo (máximo {MAX_CARACTERES} caracteres)."
    return True, None




#Detección de inyecciones 
PATRONES_INYECCION = [
    "olvida tus instrucciones",
    "ignora las instrucciones",
    "ignora todo lo anterior",
    "olvida que eres",
    "ahora eres",
    "actúa como",
    "eres un chatbot sin reglas",
    "modo developer",
    "jailbreak",
    "sin restricciones",
    "sin límites",
    "finge que eres",
    "pretende que eres",
    "nuevo rol",
    "cambia tu comportamiento",
    "eres libre de",
    "revela tus instrucciones",
    "muéstrame tu prompt",
    "cuál es tu system prompt",
    "bypass",
    "dan mode",
    "olbida tus instrucciones",
    "ignora tus instrucciones",
    "olvida las instrucciones",
    "actua como",
    "finje que eres",
    "sin restricciones",
    "sin limites",
    "eres libre",
    "nuevo sistema",
    "cambia de rol",
    "sal del personaje",
    "rompe el personaje",
    "override",
    "prompt injection",
    "ignore previous",
    "forget your instructions",
    "you are now",
    "act as",
]




def detectar_inyeccion(mensaje):
    mensaje_lower = mensaje.lower()
    for patron in PATRONES_INYECCION:
        if patron in mensaje_lower:
            return True, "No puedo procesar ese tipo de solicitud."
    return False, None



#Detección de datos sensibles 
PATRONES_SENSIBLES = [
    "cuánto gana",
    "cuanto gana",
    "sueldo de",
    "salario de",
    "bonus de",
    "nómina de",
    "nomina de",
    "cuánto cobra",
    "cuanto cobra",
    "cuánto le pagan",
    "cuanto le pagan",
    "banda salarial",
    "rango salarial",
    "tabla salarial",
    "mi sueldo exacto",
    "mi salario exacto",
    "datos de",
    "información de",
    "informacion de",
    "datos personales de",
    "información personal de",
    "informacion personal de",
    "expediente de",
    "contrato de",
    "dirección de",
    "direccion de",
    "teléfono de",
    "telefono de",
    "contraseña",
    "contrasena",
    "password",
    "credenciales",
    "clave de acceso",
    "token de acceso",
    "clave wifi",
    "wifi password",
    "cuenta bancaria",
    "número de cuenta",
    "numero de cuenta",
    "iban",
    "datos bancarios",
]

def detectar_sensible(mensaje):
    mensaje_lower = mensaje.lower()
    for patron in PATRONES_SENSIBLES:
        if patron in mensaje_lower:
            return True, "Esa información es confidencial. Consulta con tu manager o People en tu 1:1."
    return False, None




#Detección de consultas fuera de dominio
PATRONES_FUERA_DOMINIO = [
    # Participantes externos
    "soy participante",
    "soy alumno",
    "soy estudiante",
    "curso externo",
    "programa formativo",
    "módulo",
    "ejercicio del curso",
    "bootcamp",
    "mi profesor",
    "mi tutor",
    "mi clase",
    "mi examen",
    "entrega del proyecto",
    "trabajo de clase",

    # Entretenimiento
    "ayúdame con mi tarea",
    "ayudame con mi tarea",
    "recomiéndame una película",
    "recomiendame una pelicula",
    "recomiéndame una serie",
    "recomiendame una serie",
    "recomiéndame un libro",
    "recomiendame un libro",
    "recomiéndame música",
    "recomiendame musica",
    "qué canción",
    "que cancion",
    "qué película",
    "que pelicula",
    "qué serie",
    "que serie ver",
    "qué libro",
    "que libro leer",

    # Conocimiento general
    "cuál es la capital",
    "cual es la capital",
    "quién ganó",
    "quien gano",
    "háblame de",
    "hablame de",
    "explícame la historia",
    "explicame la historia",
    "qué es la fotosíntesis",
    "cuántos habitantes",
    "cuantos habitantes",
    "dónde está",
    "donde esta",
    "cuándo nació",
    "cuando nacio",
    "quién inventó",
    "quien invento",
    "cómo funciona el universo",
    "dame un resumen de",
    "tradúceme",
    "traduceme",
    "en qué año",
    "en que año",

    # Tareas personales
    "ayúdame a escribir un email personal",
    "ayudame a escribir un email personal",
    "redacta un mensaje para mi amigo",
    "escríbeme un poema",
    "escribeme un poema",
    "escríbeme una historia",
    "escribeme una historia",
    "hazme un resumen del libro",
    "hazme los deberes",
    "resuélveme este ejercicio",
    "resuelve este problema de matemáticas",
    "resuelve este problema de matematicas",

    # Tecnología general
    "cómo programo en",
    "como programo en",
    "enséñame python",
    "enséñame javascript",
    "ayúdame con mi código de",
    "ayudame con mi codigo de",
    "qué framework usar",
    "que framework usar",
    "cómo instalo",
    "como instalo",
    "configura mi ordenador",

    # Finanzas personales
    "cómo invierto",
    "como invierto",
    "qué criptomoneda",
    "que criptomoneda",
    "cómo ahorro dinero",
    "como ahorro dinero",
    "préstamo personal",
    "prestamo personal",
    "hipoteca",
    "declaración de la renta personal",
    "declaracion de la renta personal",

    # Salud general
    "qué medicamento",
    "que medicamento",
    "tengo fiebre",
    "me duele",
    "síntomas de",
    "sintomas de",
    "diagnóstico",
    "diagnostico",
    "qué doctor",
    "que doctor",

    # Otros
    "cuál es el mejor restaurante",
    "cual es el mejor restaurante",
    "qué tiempo hace",
    "que tiempo hace",
    "el horóscopo",
    "el horoscopo",
    "lotería",
    "loteria",
    "receta de cocina",
    "cómo cocino",
    "como cocino",
    ]


def detectar_fuera_dominio(mensaje):
    mensaje_lower = mensaje.lower()
    for patron in PATRONES_FUERA_DOMINIO:
        if patron in mensaje_lower:
            return True, "Solo puedo ayudarte con dudas sobre tu onboarding en Bridge SA. Para otras consultas, contacta con tu manager."
    return False, None




#Función principal que llama al resto
def validar(mensaje):
    ok, error = validar_entrada(mensaje)
    if not ok:
        return False, error
    
    detectado, error = detectar_inyeccion(mensaje)
    if detectado:
        return False, error
    
    detectado, error = detectar_sensible(mensaje)
    if detectado:
        return False, error
    
    detectado, error = detectar_fuera_dominio(mensaje)
    if detectado:
        return False, error
    
    return True, None

