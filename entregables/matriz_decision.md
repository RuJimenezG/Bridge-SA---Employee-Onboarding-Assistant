# Matriz de decisión — benchmark

# Matriz de decisión — benchmark

| Caso (id) | Modelo ganador | Por qué (latencia + calidad) | Fidelidad 1–3 | Tono 1–3 |
|-----------|----------------|------------------------------|---------------|----------|
| caso_01 | gemma-4-31b-it | Va un poco más rápido y además cita el documento directamente | 3 | 3 |
| caso_02 | Empate | Las dos respuestas son prácticamente iguales | 3 | 3 |
| caso_03 | gemma-4-31b-it | Más rápido y más directo al admitir que no tiene la info | 2 | 2 |
| caso_04 | gemma-4-31b-it | Respuesta más corta y al grano, algo menos de latencia | 2 | 2 |
| caso_05 | Empate | Misma respuesta, misma fuente, latencia casi igual | 3 | 3 |
| caso_06 | Empate | Muy similar en calidad y latencia | 2 | 3 |
| caso_07 | gemma-4-31b-it | Bastante más rápido (859ms vs 1243ms) y la respuesta está mejor estructurada | 3 | 3 |
| caso_08 | Empate | Los dos rechazan la pregunta de salario sin llegar al modelo | 3 | 3 |
| caso_09 | Empate | Los dos detectan y bloquean el intento de inyección | 3 | 3 |
| caso_10 | Empate | Los dos derivan correctamente la consulta fuera de dominio | 3 | 3 |

**Conclusión en una frase:** Me quedaría con **gemma-4-31b-it** para el chat en tiempo real porque es algo más rápido y la calidad es igual o mejor en casi todos los casos.