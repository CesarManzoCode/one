---
id: ROAD-001
kind: roadmap
status: accepted
---
# Estado actual

Fecha: 2026-09-14. Vault **v0.3.0**.

## Existe

- Constitución y gobierno con estados epistemológicos, preregistro y reglas de excepción.
- Decisiones `accepted`: ADR-001 a ADR-007.
- Implementation foundation de O1 **decidida, no implementada** ([ADR-007](../decisions/ADR-007-o1-implementation-foundation.md)): C++17; Core-O1 como dialecto propio sobre MLIR fijado a `llvmorg-23.1.1`; CMake/Ninja; backend x86-64 propio con codificación y ELF delegables a un ensamblador externo.
- Contratos `designed`:
  - SPEC-001: semántica, relaciones, join y contratos de olvido;
  - SPEC-002: Core-O1 v0.1;
  - SPEC-003: perfiles O1 v0.1;
  - VAL-003: métricas;
  - VAL-004: protocolo O1 v0.1.
- Registro de claims, con todos los claims `untested`.
- Ledger de evidencia, vacío.
- Prior art delimitado y composición rival de O1 identificada.
- Disposición del research de consolidación y del research de Q1.

## No existe

- Implementación de cualquier componente: dialecto Core-O1, frontend C, lifter RV64IM, verificador, intérprete de referencia, canonicalización, pases, backend x86-64, runtime, harness.
- Build de ONE, dependencia MLIR/LLVM construida o configuración de build congelada.
- Contratos `K`, corpus y controles.
- Preregistro y umbrales U1–U7.
- Ninguna medición: ni coste de MLIR (build, RSS, latencia, closure) ni evidencia de convergencia, reutilización, closure, utilidad, originalidad o superioridad frente a referencias maduras.

## Antes de escribir código de O1

Q1 quedó resuelta por ADR-007. **Bloqueo inmediato pendiente, sin ejecutar:**

1. Fijar versiones y configuración de los oráculos de O1 (Sail, Spike, Clang, GCC).
2. Confirmar los puntos marcados “A confirmar” en SPEC-003 §2.1 y §2.3: accesos a datos no alineados, y `SLLIW`/`SRLIW`/`SRAIW` con `shamt[5] = 1`.

La revisión `llvmorg-23.1.1` es la dependencia de implementación; no fija ninguno de esos oráculos.

## Antes de ejecutar la campaña held-out

1. Contratos `K` y corpus por estrato; partición held-out sellada antes de comenzar canonicalización y pases compartidos.
2. Controles P1, N1 y N2; detector de derivación calibrado.
3. Umbrales U1–U7, instrumento de conteo determinista ([Q9](open-questions.md)), tamaños y presupuestos ([Q10](open-questions.md)).
4. Caracterización de las garantías de la composición Clang + Rellume + LLVM ([Q25](open-questions.md)).
5. Commit de preregistro.

## Regla

No describir diseño como implementación ni aspiración como resultado. Una decisión de infraestructura no es evidencia de rendimiento, y la infraestructura de MLIR no es contribución de ONE. La ambición es deliberadamente extrema; la evidencia empieza en cero.
