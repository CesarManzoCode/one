---
id: RES-008
kind: registry
status: accepted
---
# Disposición del research de Q1

Trazabilidad entre las recomendaciones del [research de Q1](ONE-Q1-Implementation-Foundation-Decision.md) (snapshot `main@c82c868`) y el vault v0.3.0. El research sigue siendo `research`. Solo es vigente lo incorporado mediante [ADR-007](../decisions/ADR-007-o1-implementation-foundation.md) en los términos indicados aquí.

**Disposiciones**: `aceptada` (ADR) · `diseñada` · `limitada a O1` · `modificada` · `rechazada` · `abierta`.

| # | Recomendación (§ del research) | Disposición | Dónde | Motivo o modificación |
|---|---|---|---|---|
| 1 | C++17 como lenguaje principal; ODS/TableGen; sin segunda implementación del core (§1) | aceptada, limitada a O1 | ADR-007 §1 | — |
| 2 | Core-O1 como dialecto propio sobre MLIR, sin reutilizar operaciones upstream por nombre (§1, §2) | aceptada, limitada a O1 | ADR-007 §2 | — |
| 3 | MLIR como infraestructura estructural (§1, §2) | aceptada | ADR-007 §3 | Reutilización T0 o crédito upstream, nunca contribución de ONE. |
| 4 | Frontera de propiedad de ONE (§4) | aceptada, resumida | ADR-007 §4 | La tabla completa sigue en el research y no es normativa. |
| 5 | No adoptar LLVM IR, optimizador LLVM ni LLVM CodeGen en el pipeline (§1, §3) | aceptada | ADR-007 §5 | Se separa explícitamente del uso de LLVM en la composición rival. |
| 6 | Backend con selección y asignación propias; codificación y ELF delegables (§1, §4) | aceptada | ADR-007 §6 | Salida determinista bit a bit exigida a la cadena completa (SPEC-003 §3 sin cambios). |
| 7 | `llvm-mc` como emisor externo inicial (§4) | aceptada, modificada | ADR-007 §6 | Fijado a la misma revisión que MLIR. |
| 8 | CMake/Ninja; MLIR externo al árbol, fijado por revisión (§1, §2) | aceptada, modificada | ADR-007 §7–§9 | El research no fijaba revisión. ADR-007 fija `llvmorg-23.1.1` (commit `6dfe1677ab8d…`), prohíbe `main` e instalación del sistema, y exige reconfirmar dependencias sobre esa revisión. |
| 9 | Bibliotecas estáticas seleccionadas, registros explícitos, nodos externos, mapa de símbolos (§2) | aceptada | ADR-007 §9 | G5 y C-O1-6 siguen evaluándose sobre artefactos reales. |
| 10 | Driver de reescritura cerrado y ordenado; threading del contexto desactivado (§2) | aceptada | ADR-007 §4, Consecuencias | Desactivar threading no se presenta como prueba de determinismo. |
| 11 | Locations como procedencia borrable; hechos y espacios como semántica (§2) | aceptada | ADR-007 Consecuencias; SPEC-001 §6 | Sin cambio de SPEC-001. |
| 12 | Doble eje: reutilización entre orígenes y procedencia de implementación (§5) | aceptada | ADR-007 Consecuencias | Regla de atribución. No modifica VAL-003 v0.1. |
| 13 | Cinco fronteras controladas; sin API universal sobre MLIR (§6) | aceptada | ADR-007 Consecuencias | — |
| 14 | Sin prototipo comparativo previo (§7) | aceptada | ADR-007 Alternativas | Cierra la cláusula “idealmente un prototipo” de Q1 y la recomendación 40 de la [disposición de la consolidación](consolidation-disposition.md). |
| 15 | Condiciones de revisión (a)–(d) (§9) | aceptada, modificada | ADR-007 Condiciones de revisión | Se añade: un defecto de la revisión fijada, y el cambio de revisión solo por ADR antes del preregistro. |
| 16 | Integración con SMT, fuzzing, Sail/Spike y Clang/GCC (§4) | aceptada, modificada | [ADR-008](../decisions/ADR-008-o1-oracle-baseline.md); SPEC-003 v0.2 | Sail, Spike, Clang y GCC se fijan y caracterizan en el mismo sprint. Las versiones del solver SMT y de los fuzzers se fijan al introducir sus consumidores y no bloquean el inicio de la implementación. |
| 17 | Mediciones de RSS, startup y build; bytes idénticos bajo borrado y renombrado (§7) | abierta | ADR-007 Consecuencias | Requieren implementación. Sin cifras. |
