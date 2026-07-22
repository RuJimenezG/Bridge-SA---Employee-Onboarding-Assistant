import json
import csv
import os
import getpass
from datetime import datetime
from dotenv import load_dotenv

import config
from state import inicializar_estado
from logic import decidir_checklist_o_consulta

if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = getpass.getpass("Pega aquí tu GEMINI_API_KEY: ")

load_dotenv()

# Modelos
MODELOS = ["gemini-3.1-flash-lite", "gemma-4-31b-it"]

# Cargar casos
with open("../benchmark_cases.json", "r", encoding="utf-8") as f:
    casos = json.load(f)["casos"]


def ejecutar_benchmark():
    resultados = []

    for modelo in MODELOS:
        print(f"\n{'='*50}")
        print(f"Modelo: {modelo}")
        print(f"{'='*50}")

        config.MODEL = modelo

        for caso in casos:
            print(f"\n  Caso {caso['id']} [{caso['tipo']}]: {caso['pregunta'][:60]}...")

            state = inicializar_estado(
                user_profile={
                    "departamento": caso["departamento"],
                    "perfil": caso["perfil"],
                    "manager": "manager@bridgesa.example"
                },
                onboarding_day=1
            )

            try:
                resultado = decidir_checklist_o_consulta(state, caso["pregunta"])
                status = resultado.get("status", "error")
                data = resultado.get("data", {})
                metricas = data.get("metricas", {})
                respuesta = data.get("respuesta", resultado.get("mensaje", ""))

                resultados.append({
                    "caso_id": caso["id"],
                    "tipo": caso["tipo"],
                    "departamento": caso["departamento"],
                    "perfil": caso["perfil"],
                    "pregunta": caso["pregunta"],
                    "modelo": modelo,
                    "status": status,
                    "respuesta": str(respuesta)[:300],
                    "latencia_ms": metricas.get("elapsed_ms", ""),
                    "prompt_tokens": metricas.get("prompt_tokens", ""),
                    "output_tokens": metricas.get("output_tokens", ""),
                    "total_tokens": metricas.get("total_tokens", ""),
                    "fidelidad": "",
                    "tono": "",
                })
                print(f"  Status: {status} | Tokens: {metricas.get('total_tokens', 'N/A')} | Latencia: {metricas.get('elapsed_ms', 'N/A')}ms")

            except Exception as e:
                print(f"  Error: {e}")
                resultados.append({
                    "caso_id": caso["id"],
                    "tipo": caso["tipo"],
                    "departamento": caso["departamento"],
                    "perfil": caso["perfil"],
                    "pregunta": caso["pregunta"],
                    "modelo": modelo,
                    "status": "exception",
                    "respuesta": str(e)[:300],
                    "latencia_ms": "",
                    "prompt_tokens": "",
                    "output_tokens": "",
                    "total_tokens": "",
                    "fidelidad": "",
                    "tono": "",
                })

    return resultados


def guardar_csv(resultados):
    os.makedirs("../output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"../output/benchmark_{timestamp}.csv"

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nResultados guardados en {ruta}")
    return ruta


if __name__ == "__main__":
    print("Iniciando benchmark...")
    print(f"Modelos: {MODELOS}")
    print(f"Casos: {len(casos)}")
    resultados = ejecutar_benchmark()
    guardar_csv(resultados)
    print("\nBenchmark completado.")