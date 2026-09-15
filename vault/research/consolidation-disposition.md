---
id: RES-006
kind: registry
status: accepted
---
# Disposición del research de consolidación

Trazabilidad entre las recomendaciones del [research de consolidación](ONE-Technical-Foundation-Consolidation-Research.md) (snapshot `main@a2f89d4`) y el vault v0.2.0. El research sigue siendo `research`: nada de lo que contiene es arquitectura salvo lo incorporado aquí mediante el artefacto indicado.

**Disposiciones**: `aceptada` (ADR) · `diseñada` (spec o protocolo `designed`) · `limitada a O1` · `modificada` · `rechazada` · `abierta`.

| # | Recomendación (§ del research) | Disposición | Dónde | Motivo o modificación |
|---|---|---|---|---|
| 1 | Campaña primaria de pares independientes y secundaria de round-trip (§1, §6.3) | aceptada, modificada | ADR-006; VAL-004 §4–§6 | Se añaden detector de derivación mecánico, controles P1/N1/N2, atribución de residuos por ablación y composición rival. |
| 2 | RV64IM + LP64, little-endian, U-mode, nivel función (§1, §7.1) | aceptada, limitada a O1 | ADR-006; SPEC-003 §2 | Se añaden: extensiones no implementadas como trap `illegal_instruction` del hart `rv64im`; ECALL/EBREAK como traps; regla de `JALR` con continuación explícita; mapa de memoria sin `W∧X` que hace imposible el SMC; ABI como validez de workload, no suposición del lifter. |
| 3 | Imagen cruda + manifiesto; subconjunto ELF `ET_REL` opcional (§7.1) | modificada | SPEC-003 §2.2 | Imagen + manifiesto aceptados; ELF de entrada **rechazado** en v0.1 ([Q24](../roadmap/open-questions.md)). |
| 4 | Perfil `ONE-C-O1` (§6.1) | diseñada, modificada | SPEC-003 §1 | Añadidos: `char` sin calificar rechazado (signedness distinta entre ABIs); inicialización obligatoria de locales; regla de un efecto; sin `void*`, casts de puntero ni comparaciones relacionales; `restrict` y TBAA no transportados; structs sin paso por valor. |
| 5 | `volatile` excluido (§6.1) | aceptada | SPEC-003 §1.3 | — |
| 6 | Entidades `c.ref` / `guest.addr` / `core.addr<space>` (§6.2) | modificada | ADR-005; SPEC-002 §4 | Core-O1 **sin tipo puntero**: direcciones `i64` con espacio estático en cada operación; procedencia descargada a frescura de slots y hechos. Tipos de dirección reabribles ([Q4](../roadmap/open-questions.md)). |
| 7 | Lenguaje de contrato independiente de frontends (§6.3, §10.1) | diseñada | VAL-004 §2; SPEC-001 §2–3 | Se separan `π_orig` y `π_K`, y se exige totalidad de frontends más allá de `Pre(K)`. |
| 8 | SSA + CFG con block arguments; contenedor de regiones (§1, §5.1, §8) | aceptada, limitada a O1 | ADR-005 | O1 implementa solo regiones CFG; el meta-modelo solo debe no impedir otras (E1). |
| 9 | Meta-modelo / interfaces / legalidad / canonicalidad como nociones separadas (§5.1) | diseñada | ARC-003; SPEC-002 §2, §7, §9 | — |
| 10 | Verificador tras cada pase; contratos de pase (§5.1) | diseñada | SPEC-002 §8, §10 | — |
| 11 | Metadatos que afectan legalidad son semántica (§5.1) | aceptada | ADR-004 §4 | Operacionalizado con la prueba de borrado de procedencia (SPEC-001 §6). |
| 12 | Canonicalización local determinista; e-graphs solo en islas puras (§5.2) | aceptada, modificada | ADR-005; SPEC-002 §9 | Equality saturation **fuera del pipeline** de O1; solo diagnóstico offline. Reglas sin prueba SMT sin crédito de convergencia. |
| 13 | Punto de descarga semántica (§1, §4) | aceptada | ADR-004; SPEC-001 §6 | Formalizado como join J1–J4 más pruebas operacionales. |
| 14 | Escalarizar estado guest; materializar en fronteras (§7.2) | diseñada, modificada | SPEC-003 §2.6 | Estado completo en llamadas internas; estrechamiento solo por prueba y contado ([Q11](../roadmap/open-questions.md)). |
| 15 | Helpers opacos con presupuesto medido (§7.2) | modificada | VAL-004 G2 | Presupuesto **cero** para semántica computacional en O1; servicios de frontera enumerados. |
| 16 | No llamar DBT a O1 (§7.3) | aceptada | ADR-006; claims §3 | — |
| 17 | Requisitos del core para O1 (§8.1) | diseñada, modificada | SPEC-002 | Sin poison/undef; parcialidad solo por precondición con `ub` inmediato; traps como terminadores; `MULHSU` expresada, no primitiva. |
| 18 | Diseñar ahora contra callejones sin salida (§8.2) | diseñada | SPEC-002 §12 | Convertido en restricciones E1–E7 con suposiciones prohibidas. |
| 19 | Mantener abiertas semánticas de streams, tensores, FP, etc. (§8.3, §22) | aceptada | SPEC-002 §13; open-questions | — |
| 20 | Ejes de memoria (§9) | diseñada, modificada | SPEC-002 §4, §7 | Accesibilidad como precondición uniforme; traps guest como comprobaciones explícitas; efectos por espacio. |
| 21 | `Obs` y fórmula de equivalencia (§10.1) | diseñada, modificada | SPEC-001 §1–§4 | Se añaden los resultados `unsupported`, `resource` y `timeout`, y la relación por arista. |
| 22 | Cuatro propiedades distintas (§10.2) | aceptada | ADR-004 §6 | — |
| 23 | Métricas de convergencia incluido el clasificador de origen (§10.3) | modificada | VAL-003 §3 | Clasificador **rechazado como gate** (corpus pequeño, resultado inestable); sustituido por la prueba de borrado, CV5 y CV4 calibrada. |
| 24 | Conjunto fuerte: SCCP + GVN/CSE + memoria + bucles (§11) | aceptada, limitada a O1 | claims C-O1-3; SPEC-002 §10.2 | Negativos obligatorios por pase; inlining y DCE sin crédito. |
| 25 | Matriz de verificación por capas (§12) | diseñada | VAL-004 §7 | Se añaden validación de `Pre(K)` en C, build `exact-state` y la regla de independencia intérprete/backend. |
| 26 | Backend AOT ELF relocatable + linker del sistema (§13) | aceptada, limitada a O1 | ADR-006; SPEC-003 §3 | JIT rechazado para O1. |
| 27 | Backend mínimo con asignación de registros real (§13) | diseñada | SPEC-003 §3 | — |
| 28 | Nodos de capability, closures derivadas, perfiles, delta test (§14) | diseñada, modificada | ARC-005; VAL-003 §6; G5 | Gate binario de procedencia de símbolos; separación herramienta / objeto generado / runtime. |
| 29 | Manifiesto de benchmark preregistrado; anti-gaming (§15) | aceptada, modificada | Gobierno reglas 7–9; VAL-003 §8–§9; VAL-004 | Conteo determinista de instrucciones como métrica primaria; held-out sellada y quemada tras su uso; composición rival. |
| 30 | Vector de reutilización con pesos preregistrados (§16) | modificada | VAL-003 §4 | Vector **sin pesos ni agregado**; niveles T0/T1/T2 con M1–M4. |
| 31 | Vector de complejidad y fronteras de Pareto (§17) | diseñada | VAL-003 §7 | — |
| 32 | Irreversibilidades a evitar por DSP, tensores, media y radio (§18) | diseñada | SPEC-002 §12; ARC-002; EXP-02 | Sin diseñar dominios. |
| 33 | Decisiones que deben seguir abiertas (§22) | aceptada | open-questions | — |
| 34 | Identificadores de versión semántica en contratos (§8.2) | aceptada | Gobierno, versionado | — |
| 35 | Umbrales de rechazo preregistrados (§21.10) | modificada | VAL-004 §8–§9 | Gates estructurales fijados ahora; umbrales numéricos U1–U7 al preregistro, con reglas de fijación. Números sin datos serían arbitrarios. |
| 36 | `validation/benchmark-schema.json`, `validation/reuse-schema.json` (§24) | rechazada por ahora | — | Campos especificados en Markdown (ledger, VAL-003, VAL-004). Un esquema de máquina sin harness derivaría antes de existir tooling. |
| 37 | `spec/o1-scope.md`, `semantic-relations.md`, `one-core-contract.md`, `pass-contracts.md` (§24) | modificada | SPEC-001, SPEC-002, SPEC-003 | Tres specs en lugar de cuatro: los contratos de pase viven en el contrato del core. |
| 38 | `claims/registry.md`, `evidence/ledger-schema.md` (§24) | aceptada, modificada | [claims](../claims.md); [ledger](../evidence/ledger.md) | El registro sustituye a `research/hypotheses.md`. |
| 39 | Lenguaje de implementación abierto hasta un ADR (§22, §26) | aceptada | [Q1](../roadmap/open-questions.md) | Bloqueante antes de escribir código de O1; incluye la alternativa MLIR. Cerrada en v0.3.0 por [ADR-007](../decisions/ADR-007-o1-implementation-foundation.md). |
| 40 | Comparación core propio frente a prototipo MLIR (§25) | abierta | Q1; related-work §4 | En v0.3.0, ADR-007 resuelve Q1 sin prototipo comparativo previo ([disposición de Q1](q1-disposition.md) #14). |

## Aportaciones de la consolidación ausentes en el research

- Totalidad de frontends más allá de `Pre(K)` (ADR-004 §5).
- Prueba de borrado de procedencia y de identidad de workload (SPEC-001 §6).
- Clases residuales RC1–RC4 con ablación mecánica (SPEC-001 §9).
- Composición rival instanciada para O1: Clang + Rellume + LLVM (ADR-006), tras verificar que Remill no soporta RISC-V.
- Origin gap acoplado a un suelo de calidad frente a Clang (C-O1-7, U3).
- Ausencia de poison y de tipo puntero en Core-O1 (ADR-005).
- Discrepancia de signedness de `char` entre ABIs y regla de extensión de `u32` en LP64 (SPEC-003).
