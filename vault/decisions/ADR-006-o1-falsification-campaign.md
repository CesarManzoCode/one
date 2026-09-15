---
id: ADR-006
kind: decision
status: accepted
---
# ADR-006 — O1 como campaña de falsificación acotada

## Contexto

EXP-01 (v0.1) no definía una campaña válida. Si la entrada RISC-V es la salida de compilar el mismo C, la convergencia mide sobre todo la capacidad de un lifter y un canonicalizador para deshacer decisiones de lowering ya tomadas por un compilador: es un falso positivo de la hipótesis. Tampoco fijaba perfiles, unidad de traducción, relaciones semánticas, controles, baselines ni umbrales.

## Decisión

Alcance: O1.

1. **Propósito.** O1 intenta refutar H1 y H2 en su forma más débil (dos orígenes imperativos cercanos) y validar el aparato de medición. No puede apoyar la tesis global de ONE.
2. **Orígenes, perfiles y target** ([SPEC-003](../spec/o1-profiles.md)):
   - **ONE-C-O1**: subconjunto freestanding nombrado de C con entorno LP64 fijado;
   - **RV64IM-O1**: hart RV64IM little-endian, sin extensiones C/F/D/A/V, entorno de ejecución a nivel de función. El ABI LP64 es una propiedad de validez del workload, no una suposición del lifter;
   - **x86-64-O1**: System V AMD64, objeto ELF64 reubicable enlazado con el linker del sistema, declarado no central.
3. **Unidad**: funciones de una imagen con contrato de entrada. Sin loader ELF de entrada, libc, syscalls, hilos, señales ni código automodificable.
4. **Campaña primaria: pares independientes.** Implementaciones C y RV64IM de la misma especificación de contrato, escritas sin derivar una de otra, bajo un procedimiento de independencia con detector de derivación.
5. **Campaña secundaria: pares derivados** (C → compiladores RISC-V → lift). Sirve para corrección, robustez y sensibilidad a compilador, versión y flags. Excluida de claims de titular.
6. **Controles de métrica.** Controles positivos y negativos calibran las métricas de convergencia. Una métrica que no los separa invalida los claims de convergencia de la campaña.
7. **Composición de referencia.** Clang (C → LLVM IR) + Rellume (RV64 → LLVM IR) + optimizador y backend x86-64 de LLVM, medida con el mismo protocolo y con sus garantías caracterizadas (C-O1-8).
8. **Nombre de capacidad.** “Lifting y ejecución de funciones RV64IM”. O1 no se comunica como DBT ni emulación.
9. **Preregistro.** El protocolo [VAL-004](../validation/o1-protocol.md), con umbrales cuantitativos, se congela antes de cualquier ejecución sobre la partición held-out.

## Alternativas consideradas

- **Solo pares derivados**: falso positivo estructural.
- **RV32I**: ancho de dirección distinto del host; sin M, multiplicación y división serían bucles o helpers artificiales.
- **RV64GC**: la extensión C añade decodificación de longitud variable ortogonal a la tesis; F/D abre IEEE-754 antes de su fase; A abre concurrencia.
- **Ejecutables completos con syscalls** (user-mode emulation): introducen loader, libc y SO antes de probar la tesis.
- **DBT con caché de traducción**: añade dispatch e invalidación sin informar sobre convergencia.
- **Salida JIT en vez de objeto ELF**: menos inspeccionable y reproducible.
- **C completo hosted**: el espacio de UB e implementation-defined no es validable; los resultados no serían interpretables.
- **Remill como lifter de la composición**: su repositorio no lista soporte RISC-V (comprobado 2026-09-14). Rellume declara lifting de RV64 a LLVM IR.

## Base

Research de consolidación §1, §6, §7, §10, §13, §15, §20. Hechos externos: especificación Unprivileged de RISC-V y psABI, ABI System V AMD64, repositorios de Rellume y Remill (consultados 2026-09-14). Inferencia propia: la composición Clang + lifter + LLVM ya comparte optimizador y backend entre C y código máquina, así que “ambas rutas usan el mismo optimizador y backend” no distingue a ONE de lo existente. **No existe evidencia observada de ONE.**

## Consecuencias

- EXP-01 queda sustituido por VAL-004. Los claims de O1 son C-O1-1…C-O1-8 y S-O1-9 ([claims](../claims.md)).
- O1 no ejercita representaciones ricas previas al join: los frontends pueden descargar directamente desde AST o instrucción decodificada. ADR-002 no recibe evidencia de O1.
- Antes de escribir código de O1 falta decidir lenguaje e infraestructura de implementación ([Q1](../roadmap/open-questions.md)). Antes de ejecutar held-out faltan los umbrales `U*`, el instrumento de conteo y la caracterización de la composición.

## Qué no decide

O2 y el diseño DSP; segundo backend; DBT; ELF como formato de entrada.

## Condiciones de revisión

- Rellume deja de ser utilizable: se sustituye por otra composición documentada sin cambiar los claims.
- El detector de derivación no separa pares derivados conocidos de independientes: la campaña primaria es `inconclusive` por diseño y se rediseña el procedimiento.
- El perfil C resulta demasiado estrecho para producir bucles no triviales con memoria: se amplía mediante nueva versión de SPEC-003 antes del preregistro, nunca después.

## Relaciones

La dependencia `pre-código` sobre lenguaje e infraestructura (Q1) quedó resuelta por [ADR-007](ADR-007-o1-implementation-foundation.md) (v0.3.0). La consecuencia correspondiente describe el estado de v0.2.0. Los oráculos (Sail, Spike, Clang, GCC) quedan fijados por [ADR-008](ADR-008-o1-oracle-baseline.md). La caracterización de la composición rival sigue abierta como Q25 (`pre-held-out`).
