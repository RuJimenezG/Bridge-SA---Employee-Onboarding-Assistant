# Matriz de decisión — benchmark

| Caso (id) | Modelo ganador | Por qué (latencia + calidad) | Fidelidad 1–3 | Tono 1–3 |
|-----------|----------------|------------------------------|---------------|----------|
| caso_01 | gemini-3.1-flash-lite | Misma calidad, latencia muy inferior (1549ms vs 17939ms) | 3 | 3 |
| caso_02 | gemini-3.1-flash-lite | Misma calidad, latencia muy inferior (1155ms vs 22887ms) | 3 | 3 |
| caso_03 | gemini-3.1-flash-lite | Misma calidad, mucho más rápido (878ms vs 17566ms) | 2 | 2 |
| caso_04 | gemini-3.1-flash-lite | Misma calidad, mucho más rápido (1290ms vs 19026ms) | 2 | 2 |
| caso_05 | gemini-3.1-flash-lite | Misma calidad, mucho más rápido (1179ms vs 22507ms) | 3 | 3 |
| caso_06 | gemini-3.1-flash-lite | Misma calidad, mucho más rápido (1016ms vs 16605ms) | 2 | 3 |
| caso_07 | gemini-3.1-flash-lite | Misma calidad, mucho más rápido (1112ms vs 20890ms) | 3 | 3 |
| caso_08 | Empate | Los dos rechazan la pregunta de salario sin llegar al modelo | 3 | 3 |
| caso_09 | Empate | Los dos detectan y bloquean el intento de inyección | 3 | 3 |
| caso_10 | Empate | Los dos derivan correctamente la consulta fuera de dominio | 3 | 3 |

**Conclusión** 

Me quedaría con **gemini-3.1-flash-lite** porque es entre 15 y 20 veces más rápido que gemma con la misma calidad de respuesta.