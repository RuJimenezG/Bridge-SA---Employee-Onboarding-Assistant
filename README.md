# Employee Onboarding Assistant — Bridge SA
> **Team Challenge · Sprint 05–07 | AI Engineering Bootcamp**
> **Grupo 2:** Rubén Jiménez Gutiérrez, Miguel Gerardo Lopez Iraheta, Guzmán López Barceló, David Cruz Puri.

Copiloto conversacional e interactivo diseñado para acompañar a los nuevos empleados de **Bridge SA** durante sus primeros días de *onboarding*. El asistente resuelve dudas mediante documentación interna y FAQs, genera *checklists* personalizados según el día de incorporación, detecta situaciones que requieren escalado (People/IT/Manager) y aplica capas estrictas de seguridad frente a entradas maliciosas o fuera de dominio.

---

## 🛠️ Arquitectura del Sistema

El proyecto está diseñado bajo una arquitectura modular en Python para garantizar la separación de responsabilidades, la robustez del servicio y la trazabilidad de métricas:

```text
├── config.py           # Variables globales, límites de tokens, temperaturas y constantes
├── gemini_auth.py      # Autenticación y carga segura de la API Key (.env)
├── gemini_client.py    # Cliente LLM, wrapper seguro (safe_generate) y captura de métricas
├── context.py          # Contexto ligero: Carga en memoria, selección de docs/FAQ y política de escalado
├── prompts.py          # Plantillas de prompts dinámicos (resumen, consulta, checklist)
├── state.py            # Gestión del estado conversacional, historial y memoria comprimida
├── validators.py       # Guardrails: Filtro de inyecciones, contenido sensible y dominio
├── logic.py            # Orquestación del flujo, resúmenes automáticos y lógica de decisión
├── main.py             # Punto de entrada y demostraciones interactivas / casos trampa
└── data/               # Lore de Bridge SA (empresa.json, onboarding_docs.json, faq_onboarding.json)
```

## 🚀 Características Principales
- Contexto Ligero: Filtrado dinámico por palabras clave y etiquetas (tags) limitando el contexto a un máximo de 3 documentos y 2 entradas FAQ por consulta para no saturar la ventana de contexto.

- Gestión Híbrida de Memoria: Combinación de ventana deslizante de turnos recientes (WINDOW) con resúmenes automáticos periódicos (RESUMIR_CADA) gestionados por el modelo.

- Guardrails & Safety: Validación estricta en validators.py para interceptar prompt injections, solicitudes fuera de dominio (out-of-scope) y peticiones de datos confidenciales/sensibles antes de llamar a la API.

- Política de Escalado Transparente: Redirección automática hacia People (RRHH), IT, Manager o canal de onboarding en caso de dudas no resueltas por la documentación.

- Soporte Structured Output: Generación de checklists diarios parametrizados en formato JSON estructurado.

## ⚙️ Requisitos Previos e Instalación

### Prerrequisitos
- Python 3.10+
- Git
- Una clave API válida de Google Gemini

### 1. Clonar el repositorio

```bash
git clone https://github.com/RuJimenezG/Bridge-SA---Employee-Onboarding-Assistant.git
cd employee-onboarding-assistant
```

### 2. Crear y activar el entorno virtual

- En Linux/macOS:

```
python3 -m venv venv
source venv/bin/activate
```

- En Windows (CMD/PowerShell):
```
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias
```
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto (basado en .env.example si existe) e introduce tu API Key:

```
GEMINI_API_KEY=tu_api_key_aqui
```

## 💻 Ejecución del Proyecto
El archivo main.py contiene los scripts de prueba e iteración del asistente. Puedes ejecutar las demostraciones principales directamente desde la terminal:

```
python main.py
```

### Modos de Demostración Disponibles:

1. Consultas Multiturno (demo_cosultas_asistente): Simula una conversación real evaluando el mantenimiento del contexto, escalados automáticos a IT/Manager y la medición de tiempos y tokens por respuesta.

2. Generación de Checklist (demo_checklist): Evalúa la salida en formato JSON estructurado para el plan de tareas según el día de incorporación del empleado.

3. Pruebas de Robustez / Casos Trampa (demo_casos_trampa): Demuestra la interceptación de intentos de jailbreak, preguntas sensibles y solicitudes de cambio de rol gracias a la capa de validación previa.

## 📊 Evaluation & Benchmark

El proyecto incluye un entorno de evaluación comparativa situado en la carpeta output/ para analizar el rendimiento de distintos modelos bajo el mismo banco de pruebas (mínimo 10 casos):

- Modelos Evaluados: gemini-3.1-flash-lite vs gemma-4-31b-it (u otros proveedores como OpenAI/Cohere).

- Métricas Medidas:

    - Latencia (elapsed_ms): Tiempo de respuesta por turno.

    - Uso de Tokens: Tokens consumidos en el prompt de entrada y respuesta de salida.

    - Adherencia al Formato: Cumplimiento del esquema JSON en el checklist y alineación con las reglas de seguridad.

Para revisar los resultados detallados y los informes del benchmark, consulta:

- entregables/matriz_decision.md

- entregables/recomendacion.md