# Recomendación — Employee Onboarding Assistant

## Caso de uso

El asistente ayuda a empleados nuevos de Bridge SA durante sus primeros días: responde dudas sobre herramientas, procesos y cultura de empresa usando documentación interna, y genera checklists personalizados según el día de onboarding. No responde sobre salarios, datos de otros empleados ni consultas externas a la empresa.

## Modelo recomendado para producción

Modelo gemini elegido para chat en tiempo real **gemma-4-31b-it**

## Modelo alternativo (opcional)

**gemini-3.1-flash-lite** para tareas como la generación de checklists, donde la latencia importa menos.

## Trade-off principal

Con gemma ganamos velocidad de respuesta y es gratuito con un límite "generoso" (1.500 llamadas/día), lo que lo hace más viable para un despliegue real. Lo que perdemos es algo de consistencia en preguntas donde la documentación interna no tiene respuesta directa — en esos casos los dos modelos se comportan igual de bien (o igual de mal).

## ¿Qué pasaría si duplicáramos el tráfico?

Si duplicamos trafico en tareas de onboarding, el numero de llamadas a la API también se duplica. Con gemma-4-31b-it tenemos margen con el límite de 1.500 llamadas/día pero habría que vigilar posibles picos como por ejemplo los del día 1 del onboarding.

## Riesgo o condición

No usaríamos gemma-4-31b-it si la documentación interna no está al día — el asistente deriva correctamente pero deja al empleado sin respuesta útil justo en sus primeros días, que es cuando más la necesita. Se debería validar que la documentación está actualizada para que se derive al dpto correcto y no deje al usuario sin respuesta.
