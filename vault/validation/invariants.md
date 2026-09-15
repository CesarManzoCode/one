---
id: VAL-001
kind: validation
status: accepted
---
# Invariantes fundacionales

Propiedades que ninguna implementación puede erosionar silenciosamente. Cada invariante nombra dónde se define con precisión, cómo se protege y qué implica violarlo. Una excepción a un invariante en una ruta de corrección es una violación ([gobierno](../governance.md), regla 10).

| ID | Invariante | Definido en | Protección | Violación implica |
|---|---|---|---|---|
| INV-01 | ONE unifica cómputo; no declara equivalentes los dominios de origen. | Constitución; ADR-004 | Perfiles por origen con semántica propia; relaciones por arista | Revisión del contrato afectado |
| INV-02 | La semántica rica no se baja antes de que dejarla atrás sea defendible. | SPEC-001 §7 | Contratos de olvido; ablación de hechos; EXP-02 | Mover el join o cambiar el lowering |
| INV-03 | Un frontend nuevo no requiere un backend nuevo por defecto. | ADR-001 | Matriz frontend × backend; G4 | Rediseño del backend o del join |
| INV-04 | Un backend nuevo es reutilizable por todos los frontends cuyos requisitos soporta. | H3 | EXP-03: coste marginal por origen | H3 refutado para ese backend |
| INV-05 | Un artefacto no paga por capabilities que no usa, salvo coste común medido y justificado. | ADR-003; VAL-003 §6 | Grafo de capabilities; gate de símbolos G5; `Δ(A, x)` | Refactor de dependencias antes de añadir capabilities |
| INV-06 | Las optimizaciones comunes no cambian la semántica del origen. | SPEC-001 §3–4 | Validación por pase; diferencial; fuzzing (VAL-004 §7) | Fallo de corrección (G1) |
| INV-07 | Las comparaciones distinguen workloads equivalentes de comparaciones con garantías distintas. | VAL-004 §11 | Preregistro; G6 | Comparación inválida, no una victoria |
| INV-08 | Ninguna mejora de benchmark justifica degradar silenciosamente otra propiedad. | VAL-003 §9 | Reporte vectorial; regresiones visibles | Resultado inválido |
| INV-09 | Una integración con un sistema externo no cuenta como implementación propia de la propiedad central. | Constitución; ARC-004 | Grafo de capabilities; registro de claims | Claim retirado |
| INV-10 | Se registran límites y casos donde el sistema especializado gana. | Gobierno regla 6 | Ledger; reporte de negativos | Evidencia incompleta |
| INV-11 | Añadir dominios aumenta integración real, no solo superficie. | H7; VAL-003 §4 | R2–R8; T1/T2 con M1–M4 | Riesgo R5 activado |
| INV-12 | La herramienta usada para construir ONE no reduce por sí sola la atribución de capacidad técnica. | Constitución | Evaluación por resultados. Una prueba “sin asistencia” sería otra pregunta; la IA sí se registra cuando afecta a la independencia de pares | — |
| INV-13 | Los mecanismos posteriores al join son origin-blind. | ADR-004 §3; SPEC-001 §6 | Prueba de borrado; configuración única; auditoría estática (G3) | Join mal declarado: rediseño |
| INV-14 | Toda arista declara relación semántica y contrato de olvido. | SPEC-001 §4, §7 | Revisión de specs; contrato de pase | Arista no admitida en el pipeline |
| INV-15 | Un frontend refina la semántica completa de su origen, no solo la de un contrato experimental. | ADR-004 §5 | Build `exact-state` frente a oráculos con entradas fuera de `Pre(K)` | Debilitamiento semántico (G6) |
| INV-16 | Los hechos son descartables e introducirlos requiere justificación; los metadatos que afectan legalidad son semántica. | SPEC-001 §5 | Contratos de pase; SMT de transferencia de hechos | Fallo de corrección |
| INV-17 | La opacidad computacional es explícita y contada; en O1 es cero. | VAL-003 §5 | Verificador V9; G2 | Rediseño del contrato del core |
| INV-18 | `unknown`, timeout, `unsupported` y `resource` nunca cuentan como éxito. | SPEC-001 §1 | Denominadores en reportes | Resultado inválido |
| INV-19 | El core no depende de módulos de dominio. | VAL-003 §7 | Grafo de dependencias | Refactor obligatorio |
| INV-20 | El crédito de integración arquitectónica solo corresponde a mecanismos T1/T2 que cumplen M1–M4. | ADR-004 §7 | R2–R4 | Claim de reutilización retirado |
| INV-21 | Pares derivados y variantes de diagnóstico no sostienen claims de titular. | ADR-006; gobierno regla 11 | Campo `clase` del ledger | Claim retirado |
