---
id: VAL-002
kind: validation
status: designed
---
# Mapa experimental

Secuencia de experimentos capaces de falsar ONE. Solo EXP-01 está diseñado con precisión suficiente para ejecutarse. Los demás fijan su propósito, el claim que atacan y lo que ya se sabe que invalidaría el resultado. No diseñan los dominios.

| EXP | Ataca | Estado |
|---|---|---|
| EXP-01 | H1, H2 (débiles), H4, H6 (exploratorio) | **Diseñado**: [VAL-004](o1-protocol.md) |
| EXP-02 | H1, H2 (fuertes); ADR-002; ADR-004 | Propósito fijado; sin diseñar |
| EXP-03 | H3 | Sin diseñar |
| EXP-04 | H4 | Sin diseñar; métricas en VAL-003 §6 |
| EXP-05 | H2 | Sin diseñar |
| EXP-06 … EXP-09 | H1, H7 en dominios concretos | Sin diseñar |
| EXP-10 | H7 | Sin diseñar |
| EXP-11 | H5, H6 | Sin diseñar |

## EXP-01 — C y RV64IM hacia Core-O1 y x86-64

Sustituido por la campaña O1 ([ADR-006](../decisions/ADR-006-o1-falsification-campaign.md), [VAL-004](o1-protocol.md)). La formulación de v0.1 —dos entradas convergen hacia un optimizador y un backend— no distinguía pares derivados de independientes ni reutilización de conocimiento de reutilización de utilidades.

## EXP-02 — DSP como primer dominio adversarial

**Rol.** Romper Core-O1 y el criterio de ADR-004 con cómputo que deja de parecer código escalar imperativo. No es una demostración.

**Preguntas que debe poder responder:**

1. ¿Puede la semántica de tasas, tokens y estado de retardo vivir antes del join y descargarse sin bajar streams a `load`/`store` sobre buffers antes de las optimizaciones que dependen de tasas (fusión, planificación estática, buffers acotados)?
2. ¿Qué mecanismos T1/T2 de O1 se reutilizan sin cambio y cuáles necesitan extensión?
3. ¿Aguantaron E1–E7 (SPEC-002 §12), o hubo que cambiar la semántica de operaciones de O1?
4. ¿Existe una optimización rica que se preserve hasta su lowering adecuado y, además, una optimización compartida con O1 con beneficio dual (H2 fuerte)?

**Firmas de fallo precomprometidas:**

| Observación | Consecuencia |
|---|---|
| DSP necesita optimizador o backend separados | H1 refutado para el par |
| Fusión o planificación solo son posibles como pase específico que duplica análisis del core | H2 sin apoyo; riesgo R3 |
| Kernels FFT o filtros como operaciones opacas en el join | Opacidad: G2 del nuevo protocolo |
| Hubo que cambiar la semántica de operaciones O1 existentes | Fallo de las restricciones de extensión; se registra como fallo de diseño de Core-O1 |

**No decidido:** modelo de streams (SDF u otro), vectores, punto fijo, workload ([Q6](../roadmap/open-questions.md), [Q15](../roadmap/open-questions.md)).

**Prerrequisito:** O1 cerrado según VAL-004 §13.

## EXP-03 — Segundo backend

Añadir AArch64, RISC-V o WASM. Medir el trabajo origin-specific en el backend nuevo (debería ser ≈ 0) y cuántos componentes de frontends y core permanecen intactos. Es la primera medición de H3; O1 solo aporta su precondición (C-O1-5).

## EXP-04 — Runtime specialization

Un artefacto `full` y al menos dos especializados. Medir según VAL-003 §6, con `Δ(A, x)` sobre varias bases. Verificar que añadir capabilities al repositorio no infla los artefactos mínimos.

## EXP-05 — Optimización entre dominios

Una optimización T2 con beneficio por ablación en al menos dos *dominios* (no solo dos orígenes imperativos). La evidencia debe mostrar un único ejemplar (M1–M4).

## EXP-06 — Media

Codec o pipeline propio que tensione transforms, entropy coding, SIMD, streaming y layout de memoria. “Decodifica” no cuenta: comparación cuantitativa de calidad, bitrate, latencia y complejidad frente a referencias con clase de equivalencia declarada.

## EXP-07 — Numerics

Coma flotante en software o precisión arbitraria usada por emulación y por otro dominio. Diferencial frente a referencias maduras.

## EXP-08 — Neural / compresión

Inferencia de tensores con una aplicación real, preferentemente compresión, ejecutada por el runtime ONE sin depender de frameworks externos en producción.

## EXP-09 — Radio / SDR físico

Cadena real con SDR: samples → sincronización, filtrado, FFT, modulación, FEC → transmisión y recepción. Hardware físico en la frontera; cómputo digital dentro de ONE.

## EXP-10 — Vertical integrada

Dos máquinas ONE transmiten media por una cadena definida por software, con cómputo originado en código compilado y en binarios traducidos, compartiendo optimizador, runtime y backend.

## EXP-11 — Campaña comparativa entre dominios

Solo cuando la superficie exista. Compara contra la composición de sistemas maduros con garantías equivalentes. Clases de equivalencia, métricas y umbrales se preregistran antes de ejecutar.
