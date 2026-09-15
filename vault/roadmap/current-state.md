---
id: ROAD-001
kind: roadmap
status: accepted
---
# Estado actual

Fecha: 2026-09-14. Vault **v0.2.0**.

## Existe

- Constitución y gobierno con estados epistemológicos, preregistro y reglas de excepción.
- Decisiones `accepted`: ADR-001 a ADR-006.
- Contratos `designed`:
  - SPEC-001: semántica, relaciones, join y contratos de olvido;
  - SPEC-002: Core-O1 v0.1;
  - SPEC-003: perfiles O1 v0.1;
  - VAL-003: métricas;
  - VAL-004: protocolo O1 v0.1.
- Registro de claims, con todos los claims `untested`.
- Ledger de evidencia, vacío.
- Prior art delimitado y composición rival de O1 identificada.
- Disposición del research de consolidación.

## No existe

- Implementación de cualquier componente: frontend C, lifter RV64IM, verificador, intérprete de referencia, canonicalización, pases, backend x86-64, runtime, harness.
- Lenguaje o infraestructura de implementación.
- Contratos `K`, corpus y controles.
- Preregistro y umbrales U1–U7.
- Ninguna medición. Ninguna evidencia de convergencia, reutilización, closure, utilidad, originalidad o superioridad frente a referencias maduras.

## Antes de escribir código de O1

1. ADR de lenguaje e infraestructura de implementación, incluida la alternativa de implementar Core-O1 sobre MLIR ([Q1](open-questions.md)).
2. Fijar versiones de oráculos (Sail, Spike, Clang, GCC) y confirmar los puntos marcados “a confirmar” en SPEC-003 §2.1 y §2.3: accesos a datos no alineados y `SLLIW`/`SRLIW`/`SRAIW` con `shamt[5] = 1`.

## Antes de ejecutar la campaña held-out

1. Contratos `K` y corpus por estrato; partición held-out sellada antes de comenzar canonicalización y pases compartidos.
2. Controles P1, N1 y N2; detector de derivación calibrado.
3. Umbrales U1–U7, instrumento de conteo determinista ([Q9](open-questions.md)), tamaños y presupuestos ([Q10](open-questions.md)).
4. Caracterización de las garantías de la composición Clang + Rellume + LLVM ([Q25](open-questions.md)).
5. Commit de preregistro.

## Regla

No describir diseño como implementación ni aspiración como resultado. La ambición es deliberadamente extrema; la evidencia empieza en cero.
