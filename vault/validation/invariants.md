---
id: VAL-001
kind: validation
status: accepted
---
# Invariantes fundacionales

| ID | Invariante | Cómo se protege inicialmente |
|---|---|---|
| INV-01 | ONE unifica cómputo, no declara equivalentes los dominios de origen. | Arquitectura y tests semánticos por frontend. |
| INV-02 | La semántica rica no se baja antes de que dejarla atrás sea defendible. | Pass contracts + differential testing. |
| INV-03 | Un frontend nuevo no debe requerir un backend nuevo por defecto. | Matriz frontend × backend. |
| INV-04 | Un backend nuevo debe ser reusable por múltiples frontends cuando sus requisitos estén soportados. | Cross-domain backend gates. |
| INV-05 | El runtime desplegado no paga por capabilities que no usa salvo coste común medido y justificado. | Footprint closure tests. |
| INV-06 | Las optimizaciones comunes no pueden cambiar semántica específica del origen. | Differential/fuzz/property tests. |
| INV-07 | Los benchmarks comparativos distinguen workloads equivalentes de comparaciones con garantías diferentes. | Benchmark schema previo a ejecución. |
| INV-08 | Ninguna mejora de benchmark justifica degradar silenciosamente una propiedad. | Claims + invariants + regression gates. |
| INV-09 | Una integración con un sistema externo no cuenta como implementación propia de la propiedad central. | Dependency/claim manifest. |
| INV-10 | ONE debe registrar explícitamente límites y casos donde el sistema especializado gana. | Evidence notes. |
| INV-11 | La cobertura de dominios debe aumentar integración real, no solo LOC. | Shared-pass/shared-backend metrics. |
| INV-12 | La herramienta usada para construir ONE no reduce por sí sola la atribución de capacidad técnica. | Evaluación por resultados efectivos; cualquier benchmark “sin asistencia” sería una prueba distinta. |
