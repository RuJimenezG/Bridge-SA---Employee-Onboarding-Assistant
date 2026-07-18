import json
import time
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuración
MODELOS = ["gemini-1.5-flash", "gemini-1.5-pro"]
TEMPERATURA = 0.2

# Cargar casos del dataset
with open("benchmark_cases.json", "r", encoding="utf-8") as f:
    casos = json.load(f)["casos"]

def llamar_modelo(modelo_nombre, pregunta, perfil):
    modelo = genai.GenerativeModel(
        model_name=modelo_nombre,
        generation_config={"temperature": TEMPERATURA}
    )

    prompt = f"""
    Eres un asistente de onboarding para empleados nuevos de Bridge SA.
    Perfil del empleado: {perfil}

    Responde SOLO con información documentada.
    Si no tienes información, indícalo claramente.
    Si la pregunta es sobre salarios, datos de otros empleados o está fuera del dominio de onboarding, recházala.

    Pregunta: {pregunta}
    """

    inicio = time.time()
    respuesta = modelo.generate_content(prompt)
    latencia = round(time.time() - inicio, 2)
    tokens = respuesta.usage_metadata.total_token_count if hasattr(respuesta, "usage_metadata") else 0

    return respuesta.text, latencia, tokens

def ejecutar_benchmark():
    resultados = []

    for caso in casos:
        print(f"\nEjecutando {caso['id']} — {caso['tipo']}...")

        for modelo in MODELOS:
            print(f"  Modelo: {modelo}")
            try:
                respuesta, latencia, tokens = llamar_modelo(modelo, caso["pregunta"], caso["perfil"])
                resultados.append({
                    "caso_id": caso["id"],
                    "tipo": caso["tipo"],
                    "departamento": caso["departamento"],
                    "perfil": caso["perfil"],
                    "pregunta": caso["pregunta"],
                    "modelo": modelo,
                    "respuesta": respuesta[:300],
                    "latencia_seg": latencia,
                    "tokens": tokens,
                    "fidelidad": "",
                    "tono": "",
                })
            except Exception as e:
                print(f"  Error con {modelo}: {e}")

    return resultados

def guardar_csv(resultados):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"output/benchmark_{timestamp}.csv"

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nResultados guardados en {ruta}")
    return ruta

if __name__ == "__main__":
    print("Iniciando benchmark...")
    resultados = ejecutar_benchmark()
    guardar_csv(resultados)
    print("Benchmark completado.")