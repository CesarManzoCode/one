---
id: ROAD-003
kind: roadmap
status: open
---
# Preguntas abiertas

Una pregunta sigue abierta cuando no existe evidencia que la discrimine. Cada una declara qué evidencia la resolvería y cuándo debe resolverse.

**Horizontes**: `pre-código` (antes de escribir código de O1) · `pre-held-out` (antes de ejecutar la campaña O1) · `O1` (se resuelve con mediciones de O1) · `post-O1` · `O2+`.

| ID | Pregunta | Por qué sigue abierta | Evidencia que la resuelve | Horizonte |
|---|---|---|---|---|
| Q2 | Forma de ONE Core después de O1: híbridos de regiones y grafos. | O1 solo usa CFG. | Necesidades medidas de EXP-02. | O2+ |
| Q3 | Número y fronteras de niveles. | O1 no ejercita niveles previos al join. | EXP-02: dónde debe estar el join para DSP. | O2+ |
| Q4 | ¿Debe sobrevivir alguna procedencia al join (direcciones tipadas, hechos de procedencia)? | La descarga de O1 es suficiente por diseño, no por evidencia. | Ablación de hechos y pérdida de descarga en O1; necesidades de buffers en O2. | O1 / O2 |
| Q5 | ¿`ub` inmediato o poison? | ADR-005 elige `ub` inmediato por simplicidad. | Hechos descartados al especular en el corpus O1 y coste de ablación asociado. | O1 |
| Q6 | Semántica de streams y dataflow junto al control convencional. | Sin workload DSP. | EXP-02. | O2 |
| Q7 | Semántica guest para DBT real: caché de traducción, destinos indirectos, interrupciones precisas. | Fuera del perfil O1. | Campaña DBT posterior. | post-O1 |
| Q8 | ¿Qué optimización T2 será la primera prueba entre dominios distintos (no solo orígenes)? | O1 solo tiene orígenes imperativos. | EXP-05. | O2+ |
| Q9 | Instrumento de conteo determinista de instrucciones. | Elección de tooling sin harness. | Validar determinismo (varianza cero entre ejecuciones) y overhead. | pre-held-out |
| Q10 | Tamaño del corpus por estrato y presupuestos de fuzzing y SMT. | Requiere coste real del harness. | Pilotos en la partición de desarrollo. | pre-held-out |
| Q11 | Estrechamiento del estado guest en llamadas: pase interprocedural compartido o análisis del frontend. | Ambos son válidos; el coste es desconocido. | Medición de R2/R7 en O1. | O1 |
| Q12 | Estrategia de acceso guest: registro de base fijado, comprobaciones explícitas o faults del host. | La semántica está fijada; la implementación no. | Origin gap (RC2) y corrección con faults. | O1 |
| Q13 | **Candidato concreto para H6**: una capacidad u optimización que la composición no logra con coste comparable. | Ninguno propuesto con falsador. | Propuesta registrada con experimento. | antes de EXP-03, **crítica** |
| Q14 | Segundo backend: AArch64, RISC-V o WASM. | Depende de qué informa más sobre H3. | Análisis tras O1/O2. | post-O1 |
| Q15 | Primer workload DSP real pero acotado. | Sin diseño DSP. | Preparación de O2. | O2 |
| Q16 | ¿Necesita ONE un lenguaje propio o basta C por mucho tiempo? | Sin presión medida. | Limitaciones observadas de ONE-C-O1 y de DSP. | O2+ |
| Q17 | ¿Qué partes de numerics deben ser propias para que la comparación sea significativa? | Fase O4. | Diseño de EXP-07. | O4 |
| Q18 | ¿Qué codec o pipeline demuestra originalidad sin aislar media? | Fase O5. | Diseño de EXP-06. | O5 |
| Q19 | ¿Qué SDR es accesible para una prueba física seria? | Fase O8. | Diseño de EXP-09. | O8 |
| Q20 | ¿Cómo evitar que tooling y metadatos de depuración vuelvan pesado el runtime mínimo? | Acotada por A5; sin tooling aún. | Closure medida con tooling presente. | post-O1 |
| Q21 | Ubicación, formato y retención de datos crudos citados por el ledger. | Sin datos aún. | Decisión antes de la primera entrada. | pre-held-out |
| Q22 | ¿Cuándo aporta información arrancar Linux y cuándo es solo espectáculo? | Sin emulación de sistema. | Campaña de emulación. | O9 |
| Q23 | Serialización estable del IR. | Sin necesidad real. | Consumidor externo concreto. | sin horizonte |
| Q24 | ¿Aceptar ELF como entrada RV? | Ortogonal a la tesis en O1. | Necesidad de workloads posteriores. | post-O1 |
| Q25 | Garantías de la composición Clang + Rellume + LLVM: preservación de traps de acceso y fidelidad de estado. | No verificado. | Pruebas de caracterización con los oráculos de VAL-004. | pre-held-out |

## Resueltas en v0.3.0

| ID | Pregunta | Resolución |
|---|---|---|
| Q1 | Lenguaje e infraestructura de implementación, incluido Core-O1 como dialecto MLIR frente a infraestructura propia (`pre-código`, bloqueante). | Resuelta por [ADR-007](../decisions/ADR-007-o1-implementation-foundation.md): C++17 y Core-O1 como dialecto propio sobre MLIR `llvmorg-23.1.1`, sin prototipo comparativo previo. La deliberación está en el [research de Q1](../research/ONE-Q1-Implementation-Foundation-Decision.md). Las mediciones de coste quedan para la implementación. |

## Resueltas o acotadas en v0.2.0

Numeración de v0.1:

| v0.1 | Pregunta | Resolución |
|---|---|---|
| 1 | Rust, C++, Zig u otra base | Sigue abierta como Q1, ahora bloqueante y con la alternativa MLIR. Resuelta en v0.3.0 por ADR-007. |
| 2 | SSA, graph IR, regiones | Acotada para O1 por ADR-005; resto en Q2. |
| 3 | Cuántos niveles | Q3; O1 no la informa. |
| 4 | Efectos, aliasing, espacios de memoria | Acotada para O1 por SPEC-002 §4 y §7; resto en Q4. |
| 5 | Streams y dataflow | Q6. |
| 6 | Semántica guest explícita | Acotada para O1 por SPEC-003 §2; DBT en Q7. |
| 7 | Medir infraestructura compartida sin contar utilidades triviales | Resuelta: ADR-004 §7 y VAL-003 §4–§5. |
| 8 | Primera optimización cross-domain | Para O1, conjunto fuerte de C-O1-3; entre dominios, Q8. |
| 9 | Segundo backend | Q14. |
| 10 | Primer workload DSP | Q15. |
| 11 | Lenguaje propio | Q16. |
| 12 | Numerics propios | Q17. |
| 13 | Codec o pipeline | Q18. |
| 14 | SDR | Q19. |
| 15 | Metadatos de tooling | Q20. |
| 16 | Prior art de MLIR y TCG frente a oportunidad nueva | Prior art resuelto en related-work; la oportunidad, en Q13. |
| 17 | Primera afirmación falsable por un especialista | Resuelta: C-O1-1 a C-O1-8 en el registro de claims. |
| 18 | Arrancar Linux | Q22. |
| 19 | Benchmarks sin diseño retrospectivo | Resuelta: gobierno reglas 7–9, VAL-003 §9, VAL-004. |
| 20 | Resultado que obliga a rediseñar | Resuelta: gates G2–G5 y riesgos (“Cuándo rediseñar”). |
