---
id: RES-002
kind: research
status: research
---
# Prior art que restringe a ONE

Este documento incluye solo sistemas que cambian decisiones, claims, experimentos o no-claims de ONE. No es una revisión. Las referencias están en [fuentes](sources.md); el análisis extenso, en el [research de consolidación](ONE-Technical-Foundation-Consolidation-Research.md) §19. Los no-claims que se derivan de aquí son autoritativos en el [registro de claims](../claims.md) §3.

## 1. Lo que ONE no puede reclamar

| Mecanismo | Establecido por | Consecuencia para ONE |
|---|---|---|
| IR SSA compartido entre lenguajes y targets; optimizador y backend comunes | LLVM; GCC (GIMPLE → RTL) | Que dos orígenes compartan optimizador y backend no es novedad ni, por sí solo, evidencia. |
| IR extensible multinivel: operaciones, regiones, dialectos, interfaces, conversión por legalidad, lowering progresivo | MLIR; CIRCT como stack de dialectos | ADR-002 adopta prior art; no es una contribución. |
| ISA guest → IR común → varios hosts | QEMU TCG (Bellard, USENIX 2005); Valgrind/VEX | “Varias ISAs, varios hosts” no es novedad. |
| Lifting de código máquina a IR de compilador | Remill/McSema; rev.ng; Rellume; BAP | La ruta RV64IM → Core-O1 es una instancia de una técnica conocida. |
| DBT o instrumentación sobre un optimizador de propósito general | Instrew (Rellume + LLVM) | Optimizar código guest con un optimizador de compilador no es novedad. |
| Backends compactos y serios; lowering declarativo | Cranelift (ISLE, verificación del asignador de registros); TinyCC (compilador, ensamblador y linker C compactos) | La densidad de una ruta aislada C → x86-64 no es novedad. |
| Traps definidos y memoria aislada con semántica portable | WebAssembly | Preservar traps en un sandbox es conocido, incluida su implementación con guard pages. |
| Hechos descartables y semántica de UB en IR | LLVM (`nsw`/`nuw`, poison); Lee et al. 2017 | ADR-005 elige una variante conocida y más restringida. |
| Translation validation acotada; compilación verificada; semántica C ejecutable | Alive2; CompCert; Cerberus | Métodos que O1 usa, no contribuciones. |
| Semántica ISA ejecutable como oráculo | Sail RISC-V | Idem. |
| Separación algoritmo/planificación; dataflow síncrono; grafos tensor → IR planificado | Halide; SDF; StreamIt; TVM; XLA/StableHLO; Triton | Que existan futuras capas de dominio en ONE no será novedad. |
| Equality saturation | egg | Idem. |
| Capabilities declaradas en un IR portable | SPIR-V | Idem. |

## 2. Restricciones concretas

| Sistema | Restricción que impone | Observable que diferenciaría a ONE |
|---|---|---|
| **LLVM** | Su modelo de UB y poison muestra el coste de una indefinición mal delimitada → ADR-005 prescinde de poison. Su IR de bajo nivel pierde intención → ADR-002. Es el optimizador y backend de la composición rival de O1. | Origin gap y contaminación de estado frente a Rellume → LLVM, con garantías equivalentes (C-O1-8). |
| **MLIR** | Ya ofrece el meta-modelo que ONE necesita. Reimplementarlo peor es el riesgo R7. ADR-007 implementa Core-O1 como dialecto propio sobre MLIR: esa infraestructura es crédito upstream, no de ONE. | No la infraestructura, sino contratos semánticos que produzcan T1/T2 entre dominios distintos por unidad de complejidad. MLIR no afirma convergencia semántica entre dominios. |
| **QEMU TCG** | Estado guest como globals sobre `CPUArchState`, helpers y bloques de traducción. Copiar ese modelo al core produce contaminación → estado completo en SSA (SPEC-003 §2.6) y G2. | Código guest optimizado por el mismo conocimiento que el código fuente, con cero helpers para semántica computacional. |
| **Rellume / Instrew** | Las funciones lifted operan sobre una estructura genérica de estado de CPU envuelta para una convención de llamada; declaran rendimiento cercano al original. Rellume es el lifter RV64 de la composición rival. | ONE-RV con traps de acceso preservados frente a Rellume → LLVM; closure. |
| **Remill** | Estado explícito e intrínsecos de memoria muestran el riesgo de opacidad. No lista soporte RISC-V (comprobado 2026-09-14): no sirve como baseline de O1. | — |
| **rev.ng** | La recuperación de CFG y de destinos indirectos es un problema fundamental del lifting → O1 declara `unsupported(indirect_transfer)` en vez de afirmar recuperación. | — |
| **Cranelift** | Argumentos de bloque; lowering declarativo; la corrección del asignador de registros es una superficie propia → el backend de O1 no puede omitir asignación real. | — |
| **V8 (Turboshaft)** | En 2025 abandonó sea of nodes por un CFG, citando mantenimiento, depuración, tiempo de compilación y caché → ADR-005. | — |
| **WebAssembly** | División por cero y desbordamiento con trap, desplazamientos módulo ancho, acceso fuera de memoria con trap; implementaciones con guard pages → SPEC-003: comprobaciones explícitas; faults del host solo si preservan resultado exacto. | — |
| **Alive2; Lee et al. 2017** | Validación acotada por regla; trampas de undef/poison → SPEC-002 §9. | — |
| **CompCert; Cerberus** | Preservación semántica encadenada; semántica C ejecutable → relaciones de SPEC-001; oráculo de `Pre(K)`. | — |
| **Sail, Spike, riscv-arch-test, riscv-dv; Csmith, YARPGen** | Oráculos y generadores → VAL-004 §7. Csmith y YARPGen generan fuera de ONE-C-O1: hace falta generación restringida al perfil. | — |
| **SDF, StreamIt, Halide, TVM, Triton, XLA** | Tasas, planificación, tiling y estructura tensor son información de optimización que un lowering temprano destruye → E1–E7 (SPEC-002 §12), EXP-02. | — |
| **SPEC CPU run rules; guía de benchmarking de LLVM** | Separación base/peak, validación de salidas, repeticiones y ruido → VAL-003 §8–§9. | — |

## 3. La composición es el rival

Para cada campaña la pregunta no es si ONE funciona, sino qué aporta que la composición de infraestructuras existentes no aporte con coste comparable.

- **O1**: Clang + Rellume + LLVM ya comparten optimizador y backend entre C y código máquina RV64.
- **Largo plazo**: MLIR con dialectos de dominio + LLVM + QEMU + compiladores tensor.

**Dimensiones candidatas de diferencia** (no afirmadas):

- origin gap con garantías equivalentes;
- ausencia de contaminación por estado guest;
- closure y footprint;
- vector de complejidad;
- mecanismos T2 compartidos entre dominios estructuralmente distintos.

Hoy no hay candidato registrado para H6.

## 4. El riesgo de reinventar MLIR peor

Si ONE termina siendo “MLIR escrito por nosotros y con menos ecosistema”, habrá fallado arquitectónicamente aunque funcione. Si una implementación de Core-O1 sobre MLIR alcanza los mismos gates con mejor vector de complejidad y closure, construir infraestructura propia requiere justificación medida, no preferencia.

[ADR-007](../decisions/ADR-007-o1-implementation-foundation.md) adopta MLIR como infraestructura estructural de O1. El riesgo pasa a ser de atribución: presentar mecanismos upstream como conocimiento de ONE, o contar un pase upstream con nombre compartido como uno de los pases fuertes de C-O1-3.
