# Recomendación — Employee Onboarding Assistant

## Caso de uso

El asistente ayuda a empleados nuevos de Bridge SA durante sus primeros días: responde dudas sobre herramientas, procesos y cultura de empresa usando documentación interna, y genera checklists personalizados según el día de onboarding. No responde sobre salarios, datos de otros empleados ni consultas externas a la empresa.

## Modelo recomendado para producción

Modelo elegido para chat en tiempo real: **gemini-3.1-flash-lite**

## Modelo alternativo (opcional)

**gemma-4-31b-it** podría usarse para tareas donde la latencia no sea crítica, pero los tiempos de 16-22 segundos lo hacen inviable para un chat en tiempo real.

## Trade-off principal

Con gemini-3.1-flash-lite ganamos velocidad — entre 15 y 20 veces más rápido que gemma (1-1.5 segundos vs 16-22 segundos) con una calidad de respuesta equivalente en todos los casos. Lo que perdemos es algo de margen en el límite de llamadas diarias comparado con gemma, aunque sigue siendo suficiente para el volumen esperado.

## ¿Qué pasaría si duplicáramos el tráfico?

Si duplicamos el tráfico en tareas de onboarding, el número de llamadas a la API también se duplica. Con gemini-3.1-flash-lite habría que vigilar posibles picos, especialmente los del día 1 del onboarding donde varios empleados pueden empezar a la vez.

## Riesgo o condición

No usaríamos gemini-3.1-flash-lite si la documentación interna no está al día — el asistente deriva correctamente pero deja al empleado sin respuesta útil justo en sus primeros días, que es cuando más la necesita. Se debería validar que la documentación está actualizada para que se derive al dpto correcto y no deje al usuario sin respuesta.