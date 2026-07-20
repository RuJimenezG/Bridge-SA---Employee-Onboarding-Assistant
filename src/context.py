"""
context.py
==========
Capa de Datos y Contexto (RAG ligero) del Employee Onboarding Assistant.

Responsable: Miguel (feature/contexto-datos — Parte 1).

Qué hace este módulo:
    1. Carga los ficheros de data/ (empresa, documentos de onboarding y FAQ)
       una sola vez y los deja en caché en memoria.
    2. Selecciona qué documentos y qué preguntas frecuentes son relevantes
       para una pregunta libre del empleado, SIN volcar todo el JSON en
       cada llamada al LLM (requisito del enunciado: máx. 3 docs + 2 FAQ
       por turno).
    3. Selecciona qué documentos corresponden al día de onboarding (1-5)
       en el que está el empleado, para construir el checklist.
    4. Implementa la política de escalado acordada en la reunión de equipo
       (RRHH / IT / MANAGER / ONBOARDING), como último recurso cuando la
       pregunta no se puede resolver solo con documentación.

Contrato con el resto del equipo (acordado en la reunión de alineamiento):
    - Todas las funciones devuelven listas/diccionarios "planos" (dict, list,
      str) para que logic.py y prompts.py (Integrante 2) los puedan insertar
      directamente en las plantillas de prompt.
    - Ninguna función lanza excepciones hacia arriba si faltan datos o no
      hay coincidencias: en el peor caso devuelven listas vacías o valores
      por defecto ("mecanismo ciego" a prueba de fallos), para no romper la
      ejecución del asistente (requisito de robustez / fail-closed).

De dónde sale cada cosa de este archivo (para que quede trazado):
    - Del ENUNCIADO del reto (Parte 1 · Contexto y datos):
        * "Copiar data/ y plantillas a vuestro repositorio" -> los ficheros
          en data/, no este .py.
        * "Leer empresa.json, onboarding_docs.json, faq_onboarding.json" ->
          cargar_empresa(), cargar_docs(), cargar_faq().
        * "Selección de contexto sin volcar todo el JSON (máx. 3 docs + 2
          FAQ por turno; filtro por departamento o keywords)" ->
          seleccionar_documento() y seleccionar_faq().
        * "Acordar en el equipo cuándo escalar a RRHH, IT, manager u
          onboarding@bridgesa.example" -> determinar_escalado() +
          CATEGORIAS_ESCALADO + obtener_contacto_escalado().
    - De la REUNIÓN DE EQUIPO (tareas concretas para Integrante 1 / Miguel):
        * "obtener_docs_por_dia(day_number) que filtre los documentos
          obligatorios para el día de onboarding actual" -> implementada
          tal cual, con el nombre exacto que se acordó.
        * "Búsqueda basada en tags (en vez de keywords) para las FAQ" ->
          seleccionar_faq() puntúa por tags + texto de la pregunta.
        * "Si no hay coincidencias conceptuales, devolver lista vacía sin
          romper la ejecución" -> aplicado en las 3 funciones de selección.
        * Política de escalado de 3 pasos acordada en la reunión -> ver el
          bloque de comentarios justo encima de CATEGORIAS_ESCALADO.

Qué NO hace este archivo (a propósito, porque es responsabilidad de otro
módulo/compañero — para que no haya solapes ni huecos en el equipo):
    - No lee data/empleados_demo.json ni guarda el estado del empleado
      (departamento, día, historial). Eso es state.py (Rubén).
    - No llama al LLM ni construye el prompt final con delimitadores
      <empleado>/<docs>/<pregunta>. Eso es gemini_client.py / prompts.py
      (Rubén).
    - No ensambla el JSON final del checklist (empleado_id, tareas[].id,
      tareas[].completada, mensaje_resumen). Este módulo solo entrega los
      documentos que justifican las tareas (tareas[].fuente_doc); el
      ensamblado es de logic.py (Rubén).
    - No valida la entrada ni bloquea inyecciones/datos sensibles/fuera de
      dominio (longitud, blacklist, patrones de jailbreak). Eso es
      validators.py (Guzmán). determinar_escalado() solo decide A QUIÉN
      derivar una pregunta legítima, no decide SI hay que rechazarla.
    - No adapta el tono de la respuesta al perfil (dev_junior/comercial/
      remoto_eu). Eso es prompts.py con TONOS_VALIDOS (Rubén).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Rutas y utilidades de carga
# ---------------------------------------------------------------------------
# Enunciado, Parte 1, paso 2: "Leer data/empresa.json, onboarding_docs.json,
# faq_onboarding.json y empleados_demo.json". De estos tres primeros nos
# encargamos aquí; empleados_demo.json lo carga state.py (Rubén), porque
# ahí es donde vive el estado/perfil del empleado en sesión.

# src/context.py -> parent = src/ -> parent.parent = raíz del repo
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Caché en memoria para no leer el disco en cada llamada.
_CACHE: dict[str, object] = {}


def _cargar_json(nombre_archivo: str, valor_por_defecto):
    """
    Carga un fichero JSON de data/ de forma segura.

    Si el fichero no existe o está corrupto, NO lanza una excepción:
    devuelve `valor_por_defecto` (lista o dict vacíos) para que el resto
    del asistente pueda seguir funcionando en modo degradado.
    """
    ruta = DATA_DIR / nombre_archivo
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"[context.py] Aviso: no se pudo cargar {ruta} ({error}). "
              f"Se usará un valor por defecto vacío.")
        return valor_por_defecto


def cargar_empresa() -> dict:
    """Carga (con caché) data/empresa.json."""
    if "empresa" not in _CACHE:
        _CACHE["empresa"] = _cargar_json("empresa.json", {})
    return _CACHE["empresa"]


def cargar_docs() -> list[dict]:
    """Carga (con caché) data/onboarding_docs.json."""
    if "docs" not in _CACHE:
        _CACHE["docs"] = _cargar_json("onboarding_docs.json", [])
    return _CACHE["docs"]


def cargar_faq() -> list[dict]:
    """Carga (con caché) data/faq_onboarding.json."""
    if "faq" not in _CACHE:
        _CACHE["faq"] = _cargar_json("faq_onboarding.json", [])
    return _CACHE["faq"]


def cargar_empleados_demo() -> list[dict]:
    """Carga (con caché) data/empleados_demo.json."""
    if "empleados_demo" not in _CACHE:
        _CACHE["empleados_demo"] = _cargar_json("empleados_demo.json", [])
    return _CACHE["empleados_demo"]


def cargar_casos_trampa_demo() -> list[dict]:
    """Carga (con caché) data/casos_trampa.json."""
    if "casos_trampa" not in _CACHE:
        _CACHE["casos_trampa"] = _cargar_json("casos_trampa.json", [])
    return _CACHE["casos_trampa"]


def recargar_cache() -> None:
    """
    Limpia la caché en memoria. Útil para tests/demos si se modifican
    los ficheros de data/ durante la ejecución.
    """
    _CACHE.clear()


# ---------------------------------------------------------------------------
# Tokenización simple para el "matching" por palabras clave / tags
# ---------------------------------------------------------------------------

# Palabras muy frecuentes en español que no aportan señal para el matching.
_STOPWORDS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "o",
    "a", "en", "que", "qué", "por", "para", "con", "mi", "me", "es", "soy",
    "tengo", "tu", "su", "al", "del", "cómo", "como", "cuál", "cual",
    "cuánto", "cuanto", "cuántos", "cuantos", "hago", "puedo", "hay",
    "esta", "este", "esa", "ese", "sobre", "si", "no", "se", "lo",
}


def _tokenizar(texto: str) -> set[str]:
    """
    Convierte un texto libre en un conjunto de palabras clave en minúsculas,
    sin tildes problemáticas ni stopwords. Es una tokenización deliberadamente
    simple (sin librerías de NLP) porque el reto no lo requiere.
    """
    if not texto:
        return set()
    texto = texto.lower()
    palabras = re.findall(r"[a-zñáéíóúü0-9_]+", texto)
    return {p for p in palabras if p not in _STOPWORDS and len(p) > 2}


# ---------------------------------------------------------------------------
# Selección de documentos por PREGUNTA (chat libre)
# ---------------------------------------------------------------------------
# Enunciado, Parte 2: "Selección de contexto sin volcar todo el JSON (p. ej.
# máx. 3 docs + 2 FAQ por turno; filtro por departamento o keywords)".
# Esta función cubre el "máx. 3 docs" + "filtro por departamento" para el
# modo Conversación (funcionalidad 1 del enunciado). La usará logic.py en
# cada turno de chat, ANTES de llamar al LLM.

def seleccionar_documento(
    pregunta: str,
    departamento: Optional[str] = None,
    max_docs: int = 3,
) -> list[dict]:
    """
    Selecciona hasta `max_docs` documentos de onboarding_docs.json relevantes
    para `pregunta`, puntuando por coincidencia de palabras clave con las
    tags/título/cuerpo del documento, con un plus si el documento pertenece
    al departamento del empleado.

    Si no hay ninguna coincidencia conceptual, devuelve una lista vacía
    (no se inventa contexto ni se rompe la ejecución).
    """
    tokens_pregunta = _tokenizar(pregunta)
    if not tokens_pregunta:
        return []

    candidatos = []
    for doc in cargar_docs():
        tokens_doc = set(t.lower() for t in doc.get("tags", []))
        tokens_doc |= _tokenizar(doc.get("titulo", ""))
        tokens_doc |= _tokenizar(doc.get("cuerpo", ""))

        score = len(tokens_pregunta & tokens_doc)

        # Empleados del mismo departamento reciben un pequeño empujón para
        # desempatar, pero no fuerza a incluir un doc irrelevante.
        if departamento and doc.get("departamento") == departamento and score > 0:
            score += 1

        if score > 0:
            candidatos.append((score, doc))

    candidatos.sort(key=lambda par: par[0], reverse=True)
    return [doc for _, doc in candidatos[:max_docs]]


# ---------------------------------------------------------------------------
# Selección de FAQ por PREGUNTA (chat libre)
# ---------------------------------------------------------------------------
# Enunciado: cubre el "máx. 2 FAQ por turno" de la selección de contexto.
# Reunión de equipo: la nota de config.py decía "en vez de keywords tenemos
# tags", por eso aquí puntuamos primero por tags (más fiable, curadas a
# mano en el JSON) y sumamos también las palabras de la propia pregunta de
# la FAQ como señal extra, para no depender solo de que las tags estén
# perfectamente completas.

def seleccionar_faq(pregunta: str, max_faq: int = 2) -> list[dict]:
    """
    Selecciona hasta `max_faq` entradas de faq_onboarding.json relevantes
    para `pregunta`, puntuando por coincidencia de palabras clave con las
    tags y con el texto de la propia pregunta de la FAQ.

    Si no hay coincidencias, devuelve una lista vacía de forma segura.
    """
    tokens_pregunta = _tokenizar(pregunta)
    if not tokens_pregunta:
        return []

    candidatos = []
    for item in cargar_faq():
        tokens_faq = set(t.lower() for t in item.get("tags", []))
        tokens_faq |= _tokenizar(item.get("pregunta", ""))

        score = len(tokens_pregunta & tokens_faq)
        if score > 0:
            candidatos.append((score, item))

    candidatos.sort(key=lambda par: par[0], reverse=True)
    return [item for _, item in candidatos[:max_faq]]


# ---------------------------------------------------------------------------
# Selección de documentos por DÍA de onboarding (para el checklist)
# ---------------------------------------------------------------------------
# Reunión de equipo (tarea explícita de Integrante 1): "Implementar en
# context.py una función como obtener_docs_por_dia(day_number: int) que
# filtre los documentos obligatorios para el día de onboarding actual del
# empleado." Se ha respetado el nombre y la firma tal cual se acordó,
# añadiendo `departamento` como parámetro opcional (no rompe la firma
# original, solo la extiende) porque sin él la función no podría priorizar
# doc_eng_01/doc_sales_01 y perdería precisión.
#
# Enunciado: esto alimenta la funcionalidad 2 (Checklist JSON) y el
# requisito transversal del día de onboarding (chat + checklist deben
# reflejar en qué día 1-5 está el empleado). logic.py debe llamar a esta
# función y usar cada doc devuelto como `fuente_doc` de las tareas del
# checklist.

# Mapa día -> tags relevantes. Se ha diseñado a partir de las tags reales
# de data/onboarding_docs.json (no hay campo "dia" en los datos, así que
# el equipo de Parte 1 traduce "día de onboarding" a "temas relevantes
# ese día"). Documentado también en docs/parte1_contexto_y_escalado.md.
DIA_TAGS: dict[int, set[str]] = {
    1: {"primer_dia", "bienvenida", "hardware", "slack", "checklist"},
    2: {"hardware", "slack", "accesos", "github", "checklist", "crm"},
    3: {"checklist", "buddy", "primeras_semanas", "accesos"},
    4: {"checklist", "conducta", "compliance", "buddy"},
    5: {"checklist", "beneficios", "vacaciones", "primeras_semanas"},
}

DIA_POR_DEFECTO = 1


def obtener_docs_por_dia(
    dia: int,
    departamento: Optional[str] = None,
    max_docs: int = 3,
) -> list[dict]:
    """
    Devuelve hasta `max_docs` documentos obligatorios para el día de
    onboarding indicado (1-5), priorizando:
        1. Documentos cuyo departamento coincide con el del empleado
           y que además contienen un plan día a día (p. ej. doc_eng_01).
        2. Documentos generales de "people"/"it" cuyas tags coinciden
           con los temas típicos de ese día (DIA_TAGS).

    Si `dia` no es válido (no está en 1-5), se usa DIA_POR_DEFECTO y se
    avisa por consola, sin interrumpir la ejecución (fail-safe).
    """
    if dia not in DIA_TAGS:
        print(f"[context.py] Aviso: día de onboarding '{dia}' fuera de rango "
              f"(1-5). Se usará el día {DIA_POR_DEFECTO} por defecto.")
        dia = DIA_POR_DEFECTO

    tags_dia = DIA_TAGS[dia]

    candidatos = []
    for doc in cargar_docs():
        tags_doc = set(t.lower() for t in doc.get("tags", []))
        score = len(tags_doc & tags_dia)

        # El documento "primeros cinco días" del propio departamento del
        # empleado (doc_eng_01, doc_sales_01...) es siempre muy relevante,
        # porque contiene el plan día a día completo.
        if departamento and doc.get("departamento") == departamento:
            score += 2

        if score > 0:
            candidatos.append((score, doc))

    candidatos.sort(key=lambda par: par[0], reverse=True)
    return [doc for _, doc in candidatos[:max_docs]]


# ---------------------------------------------------------------------------
# Política de escalado (acordada en la reunión de equipo — Parte 1)
# ---------------------------------------------------------------------------
# Enunciado, Parte 1, paso 3: "Acordar en el equipo cuándo escalar a RRHH,
# IT, manager u onboarding@bridgesa.example." La política de 3 pasos y el
# propio diccionario CATEGORIAS_ESCALADO son los que definisteis en la
# reunión (los he dejado con las mismas claves/palabras que acordasteis,
# solo he añadido variantes con/sin tilde para que el matching no falle
# por acentos).
#
# Flujo acordado por el equipo:
#   Paso 1) Buscar la respuesta en el contexto (FAQ / docs / empresa.json).
#           -> Esto ya lo resuelven seleccionar_documento() y seleccionar_faq()
#              de este mismo módulo; si devuelven resultados, logic.py debe
#              usarlos como contexto para que responda el modelo.
#   Paso 2) Si no hay contexto documental, mirar el diccionario de palabras
#           clave de CATEGORIAS_ESCALADO y derivar al departamento que
#           corresponda (RRHH, IT, ONBOARDING).
#   Paso 3) Si tampoco hay coincidencia de palabras clave, derivar al
#           manager del empleado (fallback final, nunca se deja al
#           empleado sin una vía de contacto).

CATEGORIAS_ESCALADO: dict[str, list[str]] = {
    "RRHH": [
        "vacaciones", "baja", "contrato", "nomina", "nómina", "salario",
        "despido", "permiso", "maternidad", "paternidad", "medico",
        "médico", "laboral", "conflicto", "acoso", "denuncia", "people",
        "recursos humanos",
    ],
    "IT": [
        "acceso", "contraseña", "password", "vpn", "ordenador", "laptop",
        "correo", "email", "cuenta", "software", "instalacion",
        "instalación", "red", "wifi", "dispositivo", "ticket",
        "soporte tecnico", "soporte técnico",
    ],
    "MANAGER": [
        "objetivo", "kpi", "rendimiento", "evaluacion", "evaluación",
        "proyecto", "tarea asignada", "sprint", "reunion de equipo",
        "reunión de equipo", "one to one", "feedback", "prioridad",
    ],
    "ONBOARDING": [
        "onboarding@bridgesa.example",
    ],
}

# Categoría de último recurso cuando no hay coincidencia de palabras clave
# (Paso 3 del flujo acordado).
CATEGORIA_ESCALADO_POR_DEFECTO = "MANAGER"


def determinar_escalado(texto: str) -> str:
    """
    Implementa el Paso 2 y el Paso 3 de la política de escalado acordada
    por el equipo (ver comentario superior). Devuelve una de las claves de
    CATEGORIAS_ESCALADO ("RRHH", "IT", "MANAGER", "ONBOARDING").

    Esta función NO decide si hay contexto documental disponible (eso lo
    hacen seleccionar_documento/seleccionar_faq); se debe llamar solo
    cuando esas funciones no han devuelto nada útil, siguiendo el flujo:
        contexto -> (si vacío) -> determinar_escalado(texto)
    """
    if not texto:
        return CATEGORIA_ESCALADO_POR_DEFECTO

    texto_normalizado = texto.lower()

    for categoria, palabras_clave in CATEGORIAS_ESCALADO.items():
        for palabra in palabras_clave:
            if palabra in texto_normalizado:
                return categoria

    # Paso 3: ninguna palabra clave ha coincidido -> derivar al manager.
    return CATEGORIA_ESCALADO_POR_DEFECTO


def obtener_contacto_escalado(categoria: str, manager: str) -> Optional[str]:
    """
    Traduce una categoría de escalado ("RRHH", "IT", "ONBOARDING") al email
    de contacto real, según data/empresa.json -> contactos.

    Para "MANAGER" se devuelve None a propósito: no hay un email genérico
    de manager en los datos, así que logic.py debe usar el campo `manager`
    del propio empleado (ver data/empleados_demo.json) para redirigirlo.
    """
    contactos = cargar_empresa().get("contactos", {})
    mapa = {
        "RRHH": contactos.get("rrhh"),
        "IT": contactos.get("it"),
        "ONBOARDING": contactos.get("onboarding"),
        "MANAGER": manager,
    }
    return mapa.get(categoria)


# ---------------------------------------------------------------------------
# Demo / autotest manual (Hito 2: trabajar en paralelo simulando al resto
# de módulos). Ejecutar con: python src/context.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== DEMO context.py (Parte 1 · feature/contexto-datos) ===\n")

    empleado_demo = {
        "nombre": "Laura Méndez",
        "departamento": "engineering",
        "perfil": "dev_junior",
        "dia_onboarding": 1,
    }

    pregunta_demo = "¿A qué canales de Slack tengo que unirme?"
    print(f"Empleado: {empleado_demo['nombre']} ({empleado_demo['departamento']})")
    print(f"Pregunta: {pregunta_demo}\n")

    docs = seleccionar_documento(pregunta_demo, departamento=empleado_demo["departamento"])
    print(f"Documentos seleccionados ({len(docs)}):")
    for d in docs:
        print(f"  - [{d['id']}] {d['titulo']}")

    faqs = seleccionar_faq(pregunta_demo)
    print(f"\nFAQ seleccionadas ({len(faqs)}):")
    for f in faqs:
        print(f"  - [{f['id']}] {f['pregunta']}")

    print(f"\nDocumentos del día {empleado_demo['dia_onboarding']} "
          f"para {empleado_demo['departamento']}:")
    docs_dia = obtener_docs_por_dia(
        empleado_demo["dia_onboarding"], departamento=empleado_demo["departamento"]
    )
    for d in docs_dia:
        print(f"  - [{d['id']}] {d['titulo']}")

    print("\n--- Casos de escalado (Paso 2 / Paso 3) ---")
    casos = [
        "¿Cuántos días de vacaciones tengo?",
        "No puedo entrar a mi cuenta de correo, ¿qué contraseña uso?",
        "¿Cuál es la prioridad del sprint de esta semana?",
        "Hola, quería saludar al equipo",  # sin coincidencia -> fallback MANAGER
    ]
    for caso in casos:
        categoria = determinar_escalado(caso)
        contacto = obtener_contacto_escalado(categoria)
        print(f"  '{caso}' -> {categoria} ({contacto or 'usar el manager del empleado'})")

    print("\nDemo finalizada correctamente (sin errores ni excepciones).")