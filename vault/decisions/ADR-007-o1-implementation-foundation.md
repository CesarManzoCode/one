---
id: ADR-007
kind: decision
status: accepted
date: 2026-09-14
research: research/ONE-Q1-Implementation-Foundation-Decision.md
disposition: research/q1-disposition.md
---
# ADR-007 — Implementation foundation de O1

## Contexto

[ADR-005](ADR-005-core-o1-representation.md) fija la representación de Core-O1 y deja abierta su implementación, propia o sobre MLIR. [ADR-006](ADR-006-o1-falsification-campaign.md) exige decidir lenguaje e infraestructura antes de escribir código de O1 ([Q1](../roadmap/open-questions.md), bloqueante `pre-código`). Sin esa decisión no se puede implementar verificador, intérprete, frontends ni backend sin fijar por omisión una base cuyo coste y cuya atribución afectan a C-O1-3, C-O1-5 y C-O1-6.

La deliberación está en el [research de Q1](../research/ONE-Q1-Implementation-Foundation-Decision.md) (snapshot `main@c82c868`). Este ADR acepta su recomendación con las modificaciones registradas en su [disposición](../research/q1-disposition.md). No la redelibera.

## Decisión

Alcance: **implementación de O1**, bajo Core-O1 v0.1 (SPEC-002), los perfiles O1 v0.1 (SPEC-003) y las restricciones E1–E7. No fija la representación ni la implementación de ONE después de O1.

1. **Lenguaje.** C++17 es el lenguaje principal de implementación de O1. Las declaraciones de operaciones, tipos y atributos usan ODS/TableGen. No se añade una segunda implementación del core en otro lenguaje.
2. **Core-O1 como dialecto propio sobre MLIR.** Core-O1 se implementa como un dialecto de ONE con operaciones, funciones y terminadores propios. Solo es legal en `J_O1` lo que declara ese dialecto conforme a SPEC-002. Ninguna operación upstream (por ejemplo, `arith`) entra en el join por semejanza de nombre, porque su semántica difiere (poison frente a `ub` inmediato). Los tipos enteros de MLIR pueden representar `iN`, con los anchos que restringe el verificador de ONE.
3. **Qué se reutiliza de MLIR** (infraestructura estructural): almacenamiento de IR, SSA, CFG, argumentos de bloque y regiones; tipos y atributos; builders; verificación estructural y constraints generadas; mecanismo de interfaces; gestión de análisis y pases; primitivas de reescritura; parser y printer genéricos para fixtures.
4. **Qué conserva ONE:** el contrato semántico (SPEC-001…003); la legalidad del join y la cobertura V1–V12 del verificador; la descarga de ambos frontends; las interfaces semánticas concretas (parcialidad, efectos, hechos, especulación); las reglas de canonicalización y optimización, junto con su orden, su terminación, sus pruebas y su registro de disparos. Se aplican mediante un driver con conjunto cerrado y ordenado de patrones, no mediante el canonicalizador general de MLIR. También conserva el intérprete de referencia independiente, el backend x86-64-O1 y el aparato experimental (harness, eventos, ablaciones, atribución).
5. **Fuera del pipeline de O1.** LLVM IR no es Core-O1. No se usan el optimizador de LLVM, LLVM CodeGen, `llc` ni la traducción MLIR → LLVM IR como implementación de ninguna etapa de ONE. El uso de LLVM en la composición rival de ADR-006 es independiente de esta decisión.
6. **Backend.** ONE controla la legalización, la selección de instrucciones, la representación máquina interna, la asignación real de registros con spills, los frames, la ABI y la traducción de espacios de SPEC-003 §3. La codificación mecánica de la secuencia ya seleccionada y la producción del objeto ELF64 `ET_REL` pueden delegarse a un ensamblador externo. Si se delega, el emisor inicial es `llvm-mc` de la revisión fijada en el punto 8, invocado como proceso con target explícito. Queda dentro de la cadena validada, con su crédito atribuido como externo y su coste contabilizado. La obligación de salida determinista bit a bit de SPEC-003 §3 aplica a la cadena completa.
7. **Build.** CMake y Ninja.
8. **Revisión fijada de MLIR/LLVM.**

   | Campo | Valor |
   |---|---|
   | Repositorio | `https://github.com/llvm/llvm-project` |
   | Tag | `llvmorg-23.1.1` |
   | Commit | `6dfe1677ab8dffbc6ec13d53a1e0215d75147689` (objeto tag `e7ce3600b55034ddf819638f395e3c475fad5be2`) |
   | Verificado | 2026-09-14, `git ls-remote` del repositorio |

   Toda build de ONE y toda evidencia de O1 usan esa revisión. No se sustituye por LLVM `main`, por una revisión flotante ni por una instalación del sistema.
9. **Fronteras de dependencia.**
   - **Fuera del árbol.** MLIR/LLVM se construye e instala fuera del repositorio de ONE, que lo consume como paquete CMake externo desde un prefijo de esa revisión. No se vendoriza, no se copia en el repositorio y ONE no se desarrolla dentro del árbol de llvm-project.
   - **Configuración mínima.** Proyectos habilitados limitados a los que MLIR requiere. Targets de LLVM limitados a los que exija el emisor x86-64. La configuración concreta (tipo de build, assertions, sanitizers, toolchain host) se congela en el commit que introduzca el build y se registra en el campo `entorno` del ledger.
   - **Enlace selectivo.** Bibliotecas estáticas seleccionadas por nodo del grafo de capabilities ([ARC-005](../architecture/modularity-deployment.md)). Prohibidos los agregados `libMLIR`/`libLLVM` y los registros globales de todos los dialectos o pases. Los registros son explícitos y derivados del grafo (A3), e idénticos en el core para ambas rutas.
   - **Closures.** MLIR/LLVM Support son nodos externos de tipo `compiler`. El runtime y los objetos generados no enlazan MLIR ni LLVM. El ensamblador externo es una dependencia operacional del nodo backend. Los oráculos, solvers, fuzzers y baselines pertenecen a nodos `test`.
   - **Procedencia de símbolos.** El mapa símbolo → nodo (A7) se construye con objetos de origen y mapa del linker antes del stripping. Un prefijo textual no basta.

## Alternativas consideradas

Resumen. El análisis está en el research §3.

- **Rust con infraestructura propia acotada** (segundo finalista): da control de layout y seguridad de memoria en código propio. Se rechaza hoy porque obliga a construir y mantener almacenamiento mutable, SSA/CFG, extensión, verificación estructural y disciplina de transformación, y ninguna necesidad actual de O1 lo exige. Queda como salida si se cumple una condición de revisión.
- **Rust sobre MLIR** (C API o bindings): conserva el sustrato nativo y añade un puente a las extensiones que ONE debe escribir.
- **C++ con IR propio:** renuncia al ahorro estructural sin obtener la seguridad de memoria de la opción Rust.
- **Zig con IR propio:** no se identificó una ventaja requerida por el contrato.
- **LLVM IR o Cranelift IR como Core-O1:** adapta el contrato a otro IR en lugar de alojarlo, lo que implica otra decisión de representación.
- **Core-O1 → LLVM IR → optimizador y backend de LLVM:** es plausible, pero introduce una segunda capa semántica y mezcla en ablaciones y en R4 mecanismos cuyo beneficio sería de LLVM.
- **Prototipo comparativo previo:** no se exige. Un verificador o intérprete mínimo no estima la carga de SSA mutable, pases, backend y mantenimiento, y no existe un umbral que convierta sus números en ganador.

## Base

**Razonamiento.** Research de Q1 §1–§7 y §9. El criterio ordena admisibilidad (expresar el contrato, origin-blindness, ablaciones, closure), después poder experimental (atribución) y después carga de implementación. MLIR y un IR propio en Rust son admisibles. MLIR gana en carga sin pérdida necesaria en las dos primeras. **Es una inferencia de ingeniería, no una medición.**

**Hechos externos**, según documentación y código de MLIR/LLVM consultados por el research:

- MLIR admite operaciones, regiones SSACFG con control no estructurado, ODS, interfaces externas, drivers de reescritura propios y control del threading del contexto;
- la semántica de `arith` usa poison;
- `MLIRPass` depende de `MLIRAnalysis`;
- `llvm-mc` produce objeto con target explícito.

El research inspeccionó upstream `main`. Las dependencias concretas deben reconfirmarse sobre `llvmorg-23.1.1` al introducir el build.

**No existe implementación de ONE ni evidencia observada.** Esta decisión no afirma rendimiento, footprint, latencia de compilación ni menor complejidad medidos.

## Consecuencias

- **Atribución.** La infraestructura de MLIR/LLVM es T0 o crédito upstream, nunca contribución de ONE ([ADR-004 §7](ADR-004-semantic-discharge-convergence.md)). Todo mecanismo T1/T2 registra por separado la reutilización entre orígenes y la procedencia de su implementación. Un algoritmo upstream solo se admite en la ruta semántica con contrato compatible, instrumentación y atribución explícita. Activar un pase llamado `cse` o `canonicalize` no acredita C-O1-3.
- **Backend.** C-O1-5 y R4 se reportan en la frontera de selección y asignación que ONE controla. La codificación y el ELF producidos por el emisor externo no se acreditan a ONE.
- **Closure.** G5 y C-O1-6 se evalúan sobre los artefactos reales. Colocar MLIR en un nodo común no satisface G5 por diseño. El coste común de MLIR se reporta por separado del coste marginal por capability (VAL-003).
- **Determinismo y procedencia.** Orden de recorrido, desempates, configuración y registros fijados. Paralelismo del contexto desactivado en ejecuciones experimentales. Ninguna decisión depende de direcciones, orden de tablas hash ni locations. Las locations de MLIR son procedencia borrable (SPEC-001 §6); `nsw`, `nuw`, espacios, etiquetas y pc observable son semántica.
- **Intérprete.** Lee la misma estructura de IR pero no invoca folders, evaluadores del optimizador ni el backend.
- **Aritmética.** La aritmética de Core-O1 se implementa con bitvectors explícitos. El overflow, los shifts y la división de C++ no definen semántica.
- **Seguridad de memoria.** El compilador es código nativo sin seguridad de memoria comprobada: RAII, APIs de mutación de MLIR, assertions, ASan y UBSan. No se reporta “cero unsafe”.
- **Lock-in aceptado:** ONE cede el layout y la reclamación del almacenamiento del compilador. El coste de salida de las definiciones ODS y de los pases es alto. Se controlan cinco fronteras: contrato del dialecto, interfaz de consultas semánticas, entrada del backend, esquema de eventos del harness, y manifiesto de capabilities con ABI del runtime. No se construye una API universal que replique MLIR.
- **Mediciones.** Bootstrap de la dependencia, build limpio, rebuild incremental, RSS y compilación por fase se medirán por separado con la implementación. Hoy no hay cifras.
- **Claims.** Todos siguen `untested`. Q1 queda resuelta.

## Qué no decide

- Versiones de los oráculos y baselines de VAL-004: Sail, Spike, Clang, GCC, y LLVM/Rellume de la composición rival. `llvmorg-23.1.1` es la dependencia de implementación, no la versión de ningún oráculo o baseline.
- Los puntos “A confirmar” de SPEC-003.
- La configuración concreta del build y la versión del toolchain host.
- El parser C concreto, que debe preservar el perfil y la descarga, y se contabiliza en `frontend-c`.
- Serialización estable del IR ([Q23](../roadmap/open-questions.md)).
- El instrumento de conteo ([Q9](../roadmap/open-questions.md)).
- La representación o infraestructura de ONE después de O1.
- La forma de regiones no-CFG futuras.

## Condiciones de revisión

Se reabre si:

1. implementar el contrato exige modificar el núcleo de MLIR o debilitar un gate;
2. la closure retiene capabilities ajenas por dependencias o raíces inevitables, tras agotar la composición ordinaria;
3. una medición identifica almacenamiento, startup o build como impedimento material para ejecutar la campaña, sin solución local razonable;
4. una necesidad efectiva posterior demuestra incompatibilidad con E1–E7;
5. la revisión fijada presenta un defecto que bloquea el contrato.

Cambiar la revisión exige un ADR posterior, antes del preregistro y nunca durante una campaña.

Un coste desconocido no es por sí solo condición de revisión. Una preferencia de lenguaje tampoco.

## Relaciones

Complementa ADR-005 (implementación de la representación, sin cambiarla). Resuelve la dependencia `pre-código` de ADR-006 sobre Q1. Se apoya en ADR-003 y ADR-004 para closure y atribución. Afecta a la atribución de C-O1-3, C-O1-5 y C-O1-6.
