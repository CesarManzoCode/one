---
id: ROAD-001
kind: roadmap
status: accepted
---
# Estado actual

Fecha: 2026-09-14. Vault **v0.3.0**.

## Existe

- Constitución y gobierno con estados epistemológicos, preregistro y reglas de excepción.
- Decisiones `accepted`: ADR-001 a ADR-008.
- Implementation foundation de O1 **decidida, no implementada** ([ADR-007](../decisions/ADR-007-o1-implementation-foundation.md)): C++17; Core-O1 como dialecto propio sobre MLIR fijado a `llvmorg-23.1.1`; CMake/Ninja; backend x86-64 propio, con codificación y ELF delegables a un ensamblador externo.
- Oráculos de O1 **fijados** ([ADR-008](../decisions/ADR-008-o1-oracle-baseline.md)): Sail RISC-V 0.14, Spike `1e05ddac`, Clang `llvmorg-23.1.1`, GCC 16.2.0, con la configuración RV64IM-O1.
- Contratos `designed`:
  - SPEC-001: semántica, relaciones, join y contratos de olvido;
  - SPEC-002: Core-O1 v0.1;
  - SPEC-003: perfiles O1 v0.2, sin puntos “A confirmar”;
  - VAL-003: métricas;
  - VAL-004: protocolo O1 v0.1.
- Registro de claims, con todos los claims `untested`.
- Ledger de evidencia, vacío.
- Prior art delimitado y composición rival de O1 identificada.
- Disposición del research de consolidación y del research de Q1.
- [Caracterización de oráculos](../research/o1-oracle-probes.md): probes de Sail y Spike que sostienen SPEC-003 v0.2. Es research sobre herramientas externas, no evidencia de ONE.

## No existe

- Implementación de cualquier componente: dialecto Core-O1, frontend C, lifter RV64IM, verificador, intérprete de referencia, canonicalización, pases, backend x86-64, runtime, harness.
- Build de ONE, dependencia MLIR/LLVM construida o configuración de build congelada.
- Integración de oráculos en ONE. Sail y Spike solo se ejecutaron temporalmente para caracterizarlos; Clang y GCC no se han construido.
- Contratos `K`, corpus y controles.
- Preregistro y umbrales U1–U7.
- Ninguna medición: ni coste de MLIR (build, RSS, latencia, closure), ni evidencia de convergencia, reutilización, closure, utilidad, originalidad o superioridad frente a referencias maduras.

## Estado pre-código: cerrado

No queda ninguna obligación ni pregunta abierta con horizonte `pre-código`:

| Obligación | Resuelta por |
|---|---|
| Lenguaje e infraestructura de implementación ([Q1](open-questions.md)) | ADR-007 |
| Revisión de LLVM/MLIR | ADR-007 (`llvmorg-23.1.1`) |
| Oráculos Sail, Spike, Clang y GCC | ADR-008 |
| Accesos RV64IM no alineados | SPEC-003 v0.2 §2.1 y §2.3 |
| `SLLIW`/`SRLIW`/`SRAIW` con `imm[5] ≠ 0` | SPEC-003 v0.2 §2.3 |

## Siguiente paso: primer sprint de implementación de O1

Es el primer tramo del **Aparato** ([fases, O1 §1](phases.md)). Todavía no ha empezado.

1. Infraestructura mínima de Core-O1: build CMake/Ninja contra MLIR `llvmorg-23.1.1` y dialecto con las operaciones de SPEC-002.
2. Verificador (V1–V12).
3. Intérprete de referencia independiente.
4. Harness e integración de oráculos, solo en el alcance que exijan esos primeros consumidores, con la configuración de ADR-008.

## Antes de ejecutar la campaña held-out

1. Contratos `K` y corpus por estrato; partición held-out sellada antes de comenzar canonicalización y pases compartidos.
2. Controles P1, N1 y N2; detector de derivación calibrado.
3. Umbrales U1–U7, instrumento de conteo determinista ([Q9](open-questions.md)), tamaños y presupuestos ([Q10](open-questions.md)).
4. Caracterización de las garantías de la composición Clang + Rellume + LLVM ([Q25](open-questions.md)).
5. Commit de preregistro.

## Regla

No describir diseño como implementación ni aspiración como resultado. Una decisión de infraestructura no es evidencia de rendimiento, y la infraestructura de MLIR no es contribución de ONE. Caracterizar un oráculo no es evidencia de ONE. La ambición es deliberadamente extrema; la evidencia empieza en cero.
