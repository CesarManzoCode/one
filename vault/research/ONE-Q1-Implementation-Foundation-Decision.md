---
id: RES-007
kind: research
status: research
snapshot: main@c82c868
disposition: research/q1-disposition.md
accepted_by: decisions/ADR-007-o1-implementation-foundation.md
---
# ONE — Q1: Implementation Foundation Decision

## 1. Decision

**Recomiendo C++ y Core-O1 como dialecto propio sobre MLIR, usando MLIR como infraestructura de representación y transformación, sin adoptar LLVM IR como Core-O1 ni incorporar automáticamente el optimizador y el backend de LLVM.**

| Dimensión | Recomendación |
|---|---|
| Lenguaje principal | C++, con C++17 como base y toolchain compatible con la revisión congelada de MLIR. ODS/TableGen para declaraciones; no añadir Rust como segunda implementación del core. |
| Infraestructura | MLIR: almacenamiento SSA/CFG, argumentos de bloque, regiones, tipos/atributos, builders, verificación estructural, interfaces, gestión de análisis/pases y primitivas de reescritura. |
| Propiedad de ONE | Contrato Core-O1, legalidad del join, descarga de ambos frontends, interfaces semánticas concretas, reglas y política de transformación, intérprete independiente, lowering al backend y aparato experimental. |
| Backend de O1 | Backend x86-64 de ONE conforme a SPEC-003, con selección, asignación real y spills, ABI y tratamiento de espacios explícitos. Delegar codificación mecánica y producción de ELF a un ensamblador existente; no usar LLVM CodeGen como sustitución implícita de ese backend. |
| Build | CMake/Ninja; MLIR externo al árbol de ONE, fijado por revisión y configuración; bibliotecas y registros seleccionados por la closure. |
| Alcance temporal | Implementación de O1 y restricciones E1–E7 existentes. No fija la representación de ONE posterior a O1. |
| Confianza | **Media-alta como decisión arquitectónica; sin evidencia de superioridad cuantitativa.** |

**La evidencia documental permite recomendar el cierre de Q1 mediante ADR, sin un experimento comparativo previo obligatorio.** No existe un empate que dependa de un número hoy desconocido: ninguna restricción vigente exige un layout físico propio o un techo de tamaño/latencia que MLIR incumpla documentalmente. Sí existe trabajo genérico concreto que MLIR evita. La elección acepta un coste común medible; no presupone que sea pequeño.

Esta es una **recomendación de research, no una decisión aceptada**. Fuente autoritativa: `CesarManzoCode/one`, `main` resuelto a [`c82c868c60359aec8791731bb44868f446ed8a40`](https://github.com/CesarManzoCode/one/commit/c82c868c60359aec8791731bb44868f446ed8a40), consultado el 15 de septiembre de 2026. Se leyeron los 18 documentos prioritarios del encargo y el registro de claims. ADR-001…006 están `accepted`; las specs y métricas están `designed`; los claims siguen `untested`. No se construyeron prototipos ni se modificó el repositorio.

## 2. Why this wins for ONE

### La decisión se deriva de las propiedades que O1 debe medir

El criterio no es quién ofrece más funcionalidades. Es qué trabajo puede delegarse conservando una observación interpretable de O1. De [ADR-004](https://github.com/CesarManzoCode/one/blob/c82c868c60359aec8791731bb44868f446ed8a40/vault/decisions/ADR-004-semantic-discharge-convergence.md), [Core-O1](https://github.com/CesarManzoCode/one/blob/c82c868c60359aec8791731bb44868f446ed8a40/vault/spec/core-o1.md) y [las métricas](https://github.com/CesarManzoCode/one/blob/c82c868c60359aec8791731bb44868f446ed8a40/vault/validation/metrics.md) se desprenden tres prioridades, sin puntuaciones ponderadas:

1. **Admisibilidad:** expresar exactamente el contrato, mantener origin-blindness, permitir las ablaciones y no contaminar las closures.
2. **Poder experimental:** poder atribuir cada regla, decisión y coste; no confundir compartir utilidades con compartir conocimiento.
3. **Carga de implementación y mantenimiento:** entre bases admisibles, evitar maquinaria genérica que no aporta evidencia adicional.

MLIR y un IR propio en Rust son admisibles en principio. MLIR gana en la tercera prioridad sin una pérdida necesaria en las dos primeras. **Es una inferencia de ingeniería, no una medición del vector de complejidad.**

La alternativa propia gana libertad física y reduce la superficie nativa sin garantías estáticas de memoria; esa ventaja es real. Pero O1 no estudia un nuevo allocator de nodos ni exige un almacenamiento compacto específico. Sus propiedades centrales viven en la semántica, las reglas compartidas, la fidelidad del backend y la composición de artefactos. MLIR permite que ONE siga controlándolas.

### Qué encaja y qué sigue faltando

MLIR proporciona operaciones extensibles, resultados múltiples, argumentos de bloque y regiones SSA con CFG. Una región de función admite control no estructurado; no requiere convertir el código RV en bucles estructurados antes del join. El significado de las operaciones pertenece al dialecto. Esto encaja con ADR-005, sin asumir que todos los dialectos existentes sean legales en Core-O1. [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/).

| Necesidad de Core-O1 | Reutilización concreta | Trabajo que permanece en ONE |
|---|---|---|
| SSA, CFG y argumentos de bloque | Nodos, listas de usos, builders, sustitución de valores, dominancia y estructura de regiones. | Declarar funciones/terminadores y restringir el metamodelo al perfil legal. |
| Verifier | Comprobaciones estructurales y generación de verificaciones de tipos/atributos mediante ODS. | Cobertura explícita V1–V12: espacios, hechos permitidos, etiquetas/payloads, llamadas, inicializadores y legalidad cerrada del join. |
| Semantic interfaces | Mecanismo de interfaces de operaciones, tipos y atributos. | Significado de `pure`, `partial`, efectos, hechos y condiciones de especulación. |
| Memoria y efectos | Interfaces y recursos extensibles. | Modelo `native`/`guest`, rangos, frescura, alias y resúmenes recursivos; no vienen resueltos por registrar dos recursos. |
| Canonicalización | API de reescritura y seguimiento de mutaciones. | Conjunto versionado de reglas, pruebas SMT, orden, terminación y registro de disparos. |
| Optimización | Gestión de análisis, invalidación y soporte de dataflow. | Contratos efectivos de SCCP, GVN/CSE, memoria y LICM, sus negativos y sus ablaciones. |
| Traps explícitos | Operación terminadora propia. | Etiqueta/payload observables y lowering fiel, sin interpretar la etiqueta en los pases. |
| Intérprete | Lectura de la misma estructura del IR. | Ejecución literal de la spec, memoria/lifetimes, `ub`, traps, combustible y conteos. MLIR no lo entrega. |

ODS permite combinar constraints generadas con verificadores propios y ordenar la verificación de regiones. Las interfaces pueden implementarse externamente sin introducir dependencias del dialecto hacia sus consumidores. Son ahorros concretos de infraestructura, no una prueba de corrección de las definiciones de ONE. [ODS](https://mlir.llvm.org/docs/DefiningDialects/Operations/), [interfaces](https://mlir.llvm.org/docs/Interfaces/).

### Las diferencias semánticas no se resuelven renombrando operaciones

**Core-O1 debe tener sus operaciones propias**, aunque sus nombres se parezcan a `arith`. Por ejemplo, `arith.addi` con `nsw` produce poison al desbordar; Core-O1 exige `ub` inmediato. Compartir nombres o copiar traits de `arith` modificaría el contrato. Los enteros de MLIR sí pueden servir como representación de `iN`, con la restricción de anchos del verificador de ONE. [Semántica de `arith`](https://mlir.llvm.org/docs/Dialects/ArithOps/).

La distinción relevante para optimizar tampoco es solamente «tiene efectos». Una división puede no escribir memoria y aun así no poder extraerse de un camino guardado. MLIR distingue efectos de memoria y especulabilidad; su jerarquía de recursos no sustituye el análisis fino de direcciones y tamaños. ONE debe expresar la parcialidad y probar las condiciones de F4. [Side Effects & Speculation](https://mlir.llvm.org/docs/Rationale/SideEffectsAndSpeculation/).

Consecuencias concretas para O1:

- Un `fold` con precondición falsa no inventa un trap ni un valor definido para obtener crédito de canonicalización.
- El GVN/CSE requerido debe manejar la intersección de hechos y las equivalencias de cargas previstas por SPEC-002; ejecutar un pase llamado `cse` no acredita ese contrato.
- LICM debe operar sobre los bucles del CFG de O1. Un pase que solo reconoce operaciones de bucle estructurado no cubre esa superficie por compartir nombre.
- Los resúmenes de llamadas incluyen posible trap, `ub`, allocation y efectos de memoria; la recursión exige el punto fijo del contrato.

Por tanto, **el ahorro principal de MLIR está debajo de las reglas semánticas**. No se presume que sus cuatro pases existentes resuelvan C-O1-3. Un algoritmo reutilizado solo se admite con contrato compatible, instrumentación y atribución explícita; el nombre de su API no basta.

### Determinismo y procedencia

El canonicalizador general de MLIR es best-effort y recoge patrones de dialectos cargados; alcanzar su límite no equivale a demostrar terminación. Para ONE se recomienda un conjunto cerrado y ordenado de patrones y una política de aplicación controlada por ONE sobre las primitivas de reescritura. El combustible sigue siendo detector de bugs, no argumento de terminación. MLIR permite drivers propios sin reemplazar el almacenamiento ni la maquinaria de mutación. [Canonicalization](https://mlir.llvm.org/docs/Canonicalization/), [Pattern Rewriter](https://mlir.llvm.org/docs/PatternRewriter/).

La ejecución experimental inicial debe fijar orden de recorrido, desempates, configuración y registros, y desactivar el paralelismo del contexto. Esta última medida elimina una fuente de variación; no demuestra por sí sola determinismo. Ninguna elección puede depender de direcciones de nodos, orden incidental de tablas hash o locations. El contexto de MLIR expone control del threading. [MLIRContext.h](https://github.com/llvm/llvm-project/blob/main/mlir/include/mlir/IR/MLIRContext.h).

No basta con ocultar ubicaciones al imprimir: la prueba de borrado debe ejecutar la misma ruta con procedencia presente y ausente. La equivalencia, hashing, ordenación y logs de decisiones de ONE deben excluir ese espacio. `nsw`, `nuw`, espacios, etiquetas y pc observable son semántica; **no** pertenecen a la procedencia borrable. Los dumps de diagnóstico pueden conservar ubicaciones fuera del resultado experimental comparable. Se mantiene la prueba adicional de renombrado de símbolos, sin cambiar la ABI exportada que declare el harness.

### Control de memoria: dos problemas diferentes

ONE conserva el modelo de memoria **del programa representado**: bytes, precondiciones, espacios, lifetimes y traducción de direcciones. MLIR controla gran parte del almacenamiento **del compilador**: layout de `Operation`, listas, usos y uniquing. `Operation` usa almacenamiento especializado con partes adyacentes a su cabecera y asignación en heap; sustituirlo por una arena indexada propia implicaría una adaptación profunda o un fork. [Operation.h](https://github.com/llvm/llvm-project/blob/main/mlir/include/mlir/IR/Operation.h).

Los tipos y atributos usan almacenamiento gestionado por el contexto. Esto facilita compartirlos, pero no da a ONE control arbitrario sobre reclamación individual y disposición física. La opción operativa para O1 es acotar la vida del contexto al trabajo de compilación y medir el pico de memoria. No se necesita un compilador residente indefinido para esta campaña. [Defining Attributes and Types](https://mlir.llvm.org/docs/DefiningDialects/AttributesAndTypes/).

Esta cesión es el principal lock-in técnico aceptado. No impide medir RSS, latencia o coste común; sí limita cuánto podrá corregir ONE esos costes sin cambiar de base.

### Peso real y capability closure

MLIR no es «solo un header», pero tampoco obliga a desplegar todos los dialectos o LLVM CodeGen. La inspección de CMake muestra `MLIRIR → MLIRSupport`; `add_mlir_library` incorpora normalmente `LLVMSupport`. El núcleo incluye también utilidades y representaciones generales que O1 no necesita directamente. No debe prometerse que el linker eliminará cada byte no ejercitado. [MLIRIR](https://github.com/llvm/llvm-project/blob/main/mlir/lib/IR/CMakeLists.txt), [MLIRSupport](https://github.com/llvm/llvm-project/blob/main/mlir/lib/Support/CMakeLists.txt), [AddMLIR](https://github.com/llvm/llvm-project/blob/main/mlir/cmake/modules/AddMLIR.cmake).

Además, `MLIRPass` depende de `MLIRAnalysis` y `MLIRIR`; `MLIRAnalysis` incorpora varias interfaces y Presburger. Por tanto, el coste de adoptar pass management es mayor que el de alojar operaciones. Esa dependencia debe aparecer en el grafo y en las mediciones, aunque parte de sus objetos no sobreviva al enlace estático. [MLIRPass](https://github.com/llvm/llvm-project/blob/main/mlir/lib/Pass/CMakeLists.txt), [MLIRAnalysis](https://github.com/llvm/llvm-project/blob/main/mlir/lib/Analysis/CMakeLists.txt).

La política concreta recomendada es:

1. Bibliotecas estáticas seleccionadas y herramientas propias; evitar agregados que registren todos los dialectos/pases o incorporen todo `libMLIR`/`libLLVM` como comodidad de distribución.
2. Grafo de capabilities que produzca dependencias de enlace **y** registros explícitos. Los registros internos del core deben ser iguales para ambas rutas; los de frontend pertenecen a sus respectivos nodos.
3. MLIR/LLVM support son nodos externos de compilador. Runtime, oráculos y generadores de build pertenecen a closures separadas. Una herramienta externa ejecutada como subproceso también cuenta como dependencia operacional.
4. Mapa de símbolos construido con objetos de origen y mapa del linker, además de namespaces. Los templates, símbolos fusionados y código generado requieren procedencia de build; un prefijo textual no basta. Conservar esa información antes de stripping.
5. G5 se evalúa en los artefactos reales. Incluir MLIR en un nodo «common» no permite esconder un lifter RV, un frontend C o un runtime guest indebidamente enlazado. Registrar por separado cualquier lastre común, aunque no sea contaminación cruzada de G5.

La traducción es AOT. Los objetos generados no necesitan MLIR para ejecutarse. `one-c` puede necesitar MLIR sin que el objeto C enlace un runtime de compilador. El runtime guest puede ser independiente de MLIR, porque recibe el código ya generado y el manifiesto. Esto es una posibilidad arquitectónica, **no una closure observada**. [Modularidad de ONE](https://github.com/CesarManzoCode/one/blob/c82c868c60359aec8791731bb44868f446ed8a40/vault/architecture/modularity-deployment.md).

### Coste de build y del lenguaje

MLIR añade CMake, Ninja, TableGen, bibliotecas nativas y compatibilidad de headers/configuración. La ruta de menor fricción es construir una dependencia fijada y desarrollar ONE fuera de ese árbol; no recompilar todo LLVM en cada iteración ni usar la instalación rolling del sistema como referencia experimental. Separar tiempo de bootstrap limpio, build limpio de ONE y rebuild incremental. Un SDK cacheado reduce espera cotidiana, pero no elimina su coste del reporte. La documentación soporta dialectos externos y generación con TableGen. [Creating a Dialect](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/).

La guía oficial contempla builds Release con assertions, sanitizers y cache de compilación. El tamaño y tiempo finales dependen de configuración, target, símbolos y paralelismo: **no se ha medido su viabilidad en la máquina de trabajo, y no se ofrecen minutos ni megabytes inventados**. Es preferible comenzar con targets/componentes necesarios y concurrencia de build limitada a la memoria disponible. [Getting Started](https://mlir.llvm.org/getting_started/).

C++ gana condicionado a esta infraestructura: acceso directo a ODS, interfaces, rewriters y ownership nativo, sin puente por operación. Su coste es que errores de lifetime, iteradores invalidados o aritmética host pueden corromper el compilador. Usar RAII, APIs de mutación de MLIR, assertions y ASan/UBSan; implementar bitvectors explícitamente y no dejar que overflow, shifts o división del lenguaje host definan Core-O1. La base C++17 sigue el estándar documentado de LLVM; congelar la configuración concreta al implementar. [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html).

No se reportará «cero unsafe» por ausencia de esa palabra en C++. La superficie relevante incluye todo código nativo sin seguridad de memoria comprobada, límites de ownership y dependencias transitivas. Sanitizers detectan defectos; no convierten esa superficie en Rust seguro.

## 3. Serious alternatives

### A. Rust + infraestructura propia acotada — segundo finalista

**Ventaja principal:** control de layout y composición, con seguridad de memoria en la mayor parte del código propio si se usan arenas indexadas y handles comprobados. No necesita un SDK MLIR, y puede ajustar almacenamiento y reclamación a los workloads reales.

No equivale a «escribir un enum de instrucciones». Para igualar el contrato haría falta:

| Paquete de trabajo adicional | Obligación concreta |
|---|---|
| Almacenamiento mutable | Identidad de valores, resultados múltiples, listas de usos, borrado/sustitución, ownership de regiones/bloques y handles inválidos. |
| Infraestructura SSA/CFG | Predecesores, dominancia, edición de argumentos de bloque y mantenimiento de referencias en cada transformación. |
| Extensión | Tipos/regiones declarados, descriptores de operaciones e interfaces; tratamiento conservador de tipos desconocidos sin switches exhaustivos repartidos por todos los pases. |
| Verificación estructural | Unicidad, dominancia, sucesores, firmas, referencias y diagnósticos robustos ante IR inválido. |
| Transformaciones | Disciplina de mutación, invalidación de análisis, worklists deterministas, eventos por regla y contratos de pase. |
| Tooling mínimo | Inspección textual reproducible y lectura de fixtures suficientes para regresiones y minimización; no un formato público estable ni un framework de plugins. |

El intérprete, las pruebas, la descarga y los cuatro mecanismos semánticos seguirían siendo necesarios con cualquiera de las dos opciones; no se contabilizan como sobrecoste exclusivo de Rust. Asimismo, dominancia, contenedores y algoritmos de grafos pueden reutilizar bibliotecas: no se exige reinventarlo todo.

El riesgo discriminante está en la **composición y mantenimiento** de esa infraestructura: un error en sustituir usos, invalidar dominancia o editar un CFG puede contaminar muchos experimentos. Resolverlo no produce crédito T1/T2 por sí mismo. Rust reduce errores de memoria, pero no demuestra invariantes SSA ni refinamiento.

Rust tampoco proporciona determinismo automático: `HashMap` tiene orden arbitrario, y la semántica aritmética debe usar operaciones explícitas, independientes del comportamiento de overflow del build. [HashMap](https://doc.rust-lang.org/std/collections/struct.HashMap.html), [Rust Reference: operadores y overflow](https://doc.rust-lang.org/reference/expressions/operator-expr.html).

La alternativa puede reutilizar componentes de backend, por ejemplo un asignador independiente como `regalloc2`, que publica checker y herramientas de fuzzing. Eso disminuye su carga real y debe reconocerse, pero no elimina la construcción del IR y su disciplina de transformación. No se propone incorporarlo a la opción C++ mediante un nuevo puente sin necesidad. [regalloc2](https://github.com/bytecodealliance/regalloc2).

**Por qué pierde hoy:** para obtener una ventaja cuantitativa de footprint/latencia aún no exigida ni demostrada, añade un subsistema genérico de corrección transversal. No hay una necesidad de O1 que obligue a pagar ese coste. **Ganaría** si el almacenamiento o coste común de MLIR resultara materialmente inadecuado y no corregible por composición, o si implementar los contratos exigiera un fork sustancial de su núcleo.

### B. C++ + Core-O1 propio sobre MLIR — opción recomendada

**Ventaja principal:** delega infraestructura estructural manteniendo visibles las decisiones semánticas y experimentales.

**Coste principal:** dependencia común más pesada, ownership nativo, APIs acopladas a MLIR y menos control del layout del compilador. ONE sigue teniendo que construir una parte importante del optimizador; MLIR no hace desaparecer O1.

**Por qué gana:** satisface el contrato sin una incompatibilidad documentada y evita construir el sustrato genérico. La ventaja no depende de obtener reutilización gratis de `arith`, LICM estructurado o LLVM CodeGen. Se acepta con las fronteras de §4 y condiciones de revisión de §9.

### Combinaciones descartadas antes de profundizar

| Combinación | Razón concreta |
|---|---|
| Rust + MLIR vía C API/Melior | Conserva el peso y almacenamiento C++ y añade el puente a las extensiones que ONE necesita escribir. Melior reconoce límites actuales de seguridad/ownership; la C API no ofrece garantía de estabilidad. No aporta aquí la combinación «Rust seguro + MLIR completo» sin costes adicionales. Puede servir a consumidores periféricos después. [C API](https://mlir.llvm.org/docs/CAPI/), [Melior](https://github.com/mlir-rs/melior). |
| C++ + IR propio | Renuncia al ahorro estructural de MLIR y a la protección de memoria que favorece a Rust en la opción propia. No hay un requisito de O1 que compense ambos costes. |
| Zig + IR propio | No se ha identificado una ventaja requerida por el contrato que justifique elevarlo a tercer finalista; su elección no elimina ninguno de los paquetes de infraestructura listados. No se afirma una inferioridad universal del lenguaje. |
| LLVM IR o Cranelift IR como Core-O1 | Obliga a adaptar el contrato a un IR con semántica y extensibilidad propias, en lugar de alojar el contrato diseñado. No responde a Q1 sin introducir otra decisión sobre la representación. Usarlos después del join sería otra frontera, no «Core-O1 ya implementado». [Cranelift IR](https://github.com/bytecodealliance/wasmtime/blob/main/cranelift/docs/ir.md). |
| Core-O1 sobre MLIR → LLVM IR → optimizador/backend LLVM | Es técnicamente plausible y no está prohibido por usar tecnología ajena. Pierde como opción inicial porque incorpora una segunda capa semántica y un gran conjunto de decisiones que hay que separar en las ablaciones y en R4; el beneficio de sus mecanismos sería de LLVM. La recomendación conserva la legalización/selección de O1 y delega la emisión mecánica. [LLVM IR Target](https://mlir.llvm.org/docs/TargetLLVMIR/). |

La última alternativa no es imposible por poison: un lowering puede satisfacer refinamiento sin que ambas representaciones tengan semántica idéntica. Su corrección tendría que justificarse. Tampoco usar LLVM invalidaría automáticamente C-O1-5; produciría evidencia de un backend compuesto, con autoría y costes separados. No es la base recomendada para la campaña actual.

## 4. Ownership boundary

«Propiedad» significa quién define el contrato, controla sus cambios y responde por la evidencia. No exige escribir cada línea a mano ni impide reutilización con atribución.

| Elemento | Control de ONE | Delegación admitida y límite |
|---|---|---|
| Contrato semántico | SPEC-001…003: valores, memoria, hechos, traps, observables y refinamiento. | Ningún comportamiento del framework sustituye la spec. |
| Definición del IR | Dialecto y etapa legal `J_O1`; correspondencia verificable entre operaciones implementadas y spec. | Metamodelo de MLIR, tipos básicos compatibles y almacenamiento. No admitir todo dialecto cargado en el join. |
| Verifier | Cobertura V1–V12 y restricciones globales. | Dominancia/estructura upstream y constraints generadas. Atribuir esas verificaciones a MLIR. |
| Interfaces y efectos | Condiciones semánticas, resúmenes y análisis fino de memoria. | Mecanismo de interfaces y consultas conservadoras compatibles. |
| Canonicalización y pases | Reglas, pruebas, orden, terminación, transferencia de hechos, invalidación declarada, negativos y eventos. | Rewriter, pass/analysis manager y algoritmos compatibles. Todo mecanismo semántico importado conserva procedencia externa. |
| Intérprete | Implementación separada y literal, memoria simulada, detección de `ub`, traps y combustible. | Estructuras IR y utilidades T0; no invocar el evaluador del optimizador o el backend como oráculo. |
| Parsing del IR | Legalidad de la entrada y normalización del resultado experimental. | Parser/printer genéricos de MLIR; formato local fijado con la revisión. No resolver Q23 mediante promesa de estabilidad. |
| Parsing C | Perfil de aceptación/rechazo y descarga al join. | Parser o AST existente si conserva la información necesaria y se contabiliza en `frontend-c`; no sustituir el frontend por C → LLVM optimizado → Core. Q1 no exige construir un parser nuevo. |
| Decoder/lifter RV | Semántica y descarga de la imagen admitida. | Utilidades de decodificación; independencia del oráculo declarada si se comparte material generado. |
| Backend | Legalización, selección, machine representation interna, ABI, asignación con spills, frames y traducción de espacios. | Componentes reemplazables compatibles; nunca presentar sus mecanismos como contribución de ONE. No se prescribe diseñar un framework general de backends. |
| Codificación/ELF | Secuencia seleccionada, símbolos, secciones y relocations legales. | Ensamblador existente después de seleccionar instrucciones y asignar registros. La emisión queda dentro de la cadena validada, con crédito externo. |
| Allocator del compilador | Límites de vida y medición de memoria. | Allocator estándar y almacenamiento MLIR. No es el modelo de memoria ejecutada. |
| Runtime | Servicios enumerados, ABI y dependencia estricta por capability. | Primitivas del SO; sin MLIR, frontends ni helpers computacionales ocultos. |
| Grafo y build | Nodos, raíces, closures, configuración y procedencia de símbolos. | CMake/Ninja/linker ejecutan la composición, no definen qué capabilities debe contener. |
| Harness/tooling | Casos, proyecciones, seeds, eventos, ablaciones y atribución. | Solvers, fuzzers, modelos ISA, compiladores de referencia y herramientas de inspección, en nodos de test. |

Como elección inicial para evitar rehacer un ensamblador y un escritor ELF, **`llvm-mc` puede ser el emisor externo** de la secuencia x86 ya decidida por ONE. Su interfaz permite salida objeto y target explícito. Se debe contabilizar su instalación, startup y tiempo; separar encoding/relaxation externos de selección propia. Confirmar secciones y relocations de SPEC-003, sin DWARF ni unwind. Esto no es delegar a `llc` la selección y asignación. [llvm-mc](https://llvm.org/docs/CommandGuide/llvm-mc.html).

No hay motivo para que el proceso que ejecuta el objeto cargue ese ensamblador. Tampoco se puede omitir su coste de compilación porque se ejecuta fuera de `one-c`.

### Integración con validación

- **SMT:** emitir obligaciones locales con precondición y hechos explícitos; QF_BV cubre las reglas bitvector de SPEC-002, no constituye por sí solo una prueba de alias, memoria ilimitada o terminación de bucles. Las transformaciones con memoria requieren su modelo acotado y el diferencial del protocolo. Alive2 valida LLVM; no se obtiene un validador Core-O1 por enlazar MLIR. [SMT-LIB](https://smt-lib.org/logics-all.shtml), [Alive2](https://github.com/AliveToolkit/alive2).
- **Fuzzing:** C++ dispone de libFuzzer; Rust de cargo-fuzz sobre esa infraestructura. Ninguno gana por disponibilidad básica. Los generadores deben respetar ONE-C-O1 y producir también Core válido y entradas negativas; fuzzear solo el parser de MLIR no valida el core. [libFuzzer](https://llvm.org/docs/LibFuzzer.html), [cargo-fuzz](https://rust-fuzz.github.io/book/cargo-fuzz.html).
- **Sail/Spike:** mantener adaptadores de test de estado, imagen, configuración y resultado. Sus ejecutables/modelos son accesibles desde ambos lenguajes. El EEI a nivel de función, pc/payload de trap y estados finales no se obtienen automáticamente de una ejecución CLI genérica. Usar una envoltura de test no introduce ELF como entrada de ONE. [Sail RISC-V](https://github.com/riscv/sail-riscv), [Spike](https://github.com/riscv-software-src/riscv-isa-sim).
- **Clang/GCC:** invocación por proceso con versiones/flags fijados; diagnóstico de UB y diferencias de garantías registrados. Son oráculos/baselines, no dependencias del runtime.
- **Instrumentación:** MLIR ofrece hooks por pase y análisis. ONE añade identidad estable de reglas, disparos y snapshots para las ablaciones; esas estadísticas no sustituyen el conteo dinámico de instrucciones x86. Q9 permanece abierta. [Pass Infrastructure](https://mlir.llvm.org/docs/PassManagement/).
- **Reproducibilidad:** fijar fuentes, toolchain, dependencias, configuración, pipeline, threads, seeds y emisor. Medir bootstrap, compilación por fase y ejecución por separado. Reconstruir y comparar bytes es una verificación necesaria posterior, no un resultado obtenido aquí.

## 5. Claim impact

| Claim o dimensión | Qué permite observar la elección | Qué no puede atribuirse a ONE |
|---|---|---|
| **H1** | Si la descarga converge a un contrato ejecutable común y la ruta posterior es origin-blind. MLIR no decide dónde está ese join. | Que SSA o dialectos sean una contribución; O1 tampoco apoya H1 en dominios no imperativos. |
| **H2** | Beneficio dual de reglas que operan sobre semántica Core-O1, probado por ablación. | Beneficio de un mecanismo upstream como conocimiento inventado por ONE. Un pass manager compartido sigue siendo T0. |
| **H4** | Closure y coste marginal reales, incluyendo dependencias externas. | Que MLIR sea «gratis» por ser build-time o por quedar en un nodo común. O1 solo mide dos rutas. |
| **C-O1-1** | V9, ausencia de opacidad, configuración única y prueba de borrado sobre el dialecto legal. | Que emitir MLIR o pasar su verifier general garantice J1–J4. |
| **C-O1-3** | Ablación de las cuatro optimizaciones fuertes; pruebas y eventos propios contra el contrato común. | Acreditar las cuatro por activar `canonicalize`, `cse` o un pipeline upstream; omitir el coste de adaptarlo. |
| **C-O1-5** | La misma legalización/selección/backend sobre Core de ambas rutas, diferencial frente al intérprete. | La codificación y el ELF producidos por el emisor externo. R4 se reporta en la frontera de reglas realmente controlada. |
| **C-O1-6** | Ausencia de contaminación entre rutas y objetos C sin runtime guest. | Declarar G5 satisfecho por diseño de CMake; hace falta inspección de artefactos y dependencias. |
| **Complejidad** | Vector con conceptos, APIs, dependencias, duplicación, condicionalidad, build, extensión y mantenimiento. | Reducirlo a LOC propias, tamaño del repo o contar infraestructura importada como trabajo inexistente. |

Usar `guest`/`native` como espacios semánticos estáticos no es consultar el origen. El backend puede actuar sobre esa diferencia definida por Core-O1; no puede escoger reglas porque «el frontend fue RV». El mismo tratamiento debe aplicar a cualquier programa legal con ese contenido.

Para cada mecanismo T1/T2 se registran dos ejes: **reutilización entre orígenes** y **procedencia de implementación**. Un mecanismo externo puede satisfacer M1–M4 como parte del sistema compuesto; eso acredita reutilización observada del sistema, no originalidad ni autoría de ONE. La atribución evita tanto inflar ONE como invalidar injustificadamente una integración real. [Registro de claims](https://github.com/CesarManzoCode/one/blob/c82c868c60359aec8791731bb44868f446ed8a40/vault/claims.md).

La contabilidad de complejidad debe mostrar el coste absoluto común y los deltas por capability sobre al menos dos bases, como exige VAL-003. Exponer dependencias declaradas y material retenido por separado: el grafo de bibliotecas de CMake y el binario final no son el mismo objeto. Los resultados de LLVM/MLIR precompilados también consumen disco y setup. No hace falta asignarles LOC «equivalentes» ficticias.

## 6. Lock-in and exit cost

**Abandonar MLIR después de O1 sería costoso, aunque no exigiría rediseñar la semántica.** C++ no se reemplaza automáticamente al cambiar de IR: migrar además a Rust sería otro coste.

| Superficie | Coste de salida esperado | Qué conservar |
|---|---|---|
| Contrato, corpus y pruebas de reglas | Bajo si no dependen de representación incidental. | Specs, precondiciones, casos y resultados esperados. |
| Definiciones ODS, builders y verificación estructural | Alto: deben trasladarse a otra infraestructura. | Correspondencia operación/invariante ↔ contrato, IDs semánticos. |
| Pases y análisis | Medio-alto: algoritmos reaprovechables, implementación acoplada a Value/Operation/rewriter. | Contratos de interfaces, reglas, eventos y argumentos de corrección. |
| Intérprete | Medio: cambia acceso al IR; no deberían cambiar memoria ni semántica ejecutable. | Evaluación separada del backend y fixtures semánticos. |
| Backend | Medio si la adaptación desde Core está localizada; alto si expone MLIR en toda su representación máquina. | Frontera Core → representación máquina, ABI y eventos de selección. |
| Runtime, oráculos y corpus de entrada | Bajo. | Interfaces por datos/ABI, independientes de MLIR. |
| Evidencia anterior | No se migra silenciosamente. | Versiones antiguas, toolchains y artefactos necesarios para reproducirla. |

Conviene controlar desde el inicio cinco fronteras: contrato del dialecto; interfaz semántica de consultas; entrada del backend; esquema de eventos/resultados del harness; manifiesto de capabilities y ABI del runtime. **No** construir una segunda API universal que replique todo MLIR para fingir portabilidad: trasladaría hoy parte del coste de una migración hipotética.

Los fixtures pueden usar sintaxis MLIR fijada a la campaña. Las observaciones y obligaciones SMT deben poder entenderse sin esa sintaxis. No se decide un formato público estable, Q23. Eliminar MLIR exigiría portar infraestructura y repetir mediciones; no basta exportar un archivo textual.

### Restricciones futuras preservadas

E1 puede representarse declarando el tipo semántico de región en la operación propietaria y consultándolo mediante una interfaz; MLIR no da a las regiones atributos propios. E2–E4 permiten extender tipos, operaciones y recursos sin que cada pase enumere dominios. E5–E7 siguen siendo obligaciones de los contratos de ONE, no funcionalidades que se activen por usar MLIR.

Hay límites reales: MLIR distingue regiones SSACFG/Graph y las Graph tienen restricciones estructurales; su documentación de efectos está centrada en CFG. Eso puede exigir trabajo posterior si otra campaña necesita una representación distinta. **No se presupone resuelto DSP ni se puntúa esa posibilidad como beneficio presente.** Nada de lo documentado obliga a cerrar E1–E7 en O1. [Regiones de MLIR](https://mlir.llvm.org/docs/LangRef/), [alcance del modelo de efectos](https://mlir.llvm.org/docs/Rationale/SideEffectsAndSpeculation/).

## 7. Remaining uncertainty

| Clase | Punto material | Tratamiento |
|---|---|---|
| Hecho conocido | MLIR puede representar el metamodelo de O1 con operaciones propias y verificación adicional. | Sustenta admisibilidad, no corrección implementada. |
| Hecho conocido | El almacenamiento nativo, las dependencias del pass manager y el build generado tienen costes y restricciones reales. | Se aceptan y se hacen visibles; no se anuncian cifras. |
| Inferencia | Reutilizar esa estructura será menos complejo que construir y mantener su equivalente acotado en Rust. | Razón principal de elección, revisable con experiencia. No es dominancia empírica en todas las dimensiones. |
| Inferencia | Registros explícitos, separación de bibliotecas y runtime independiente permiten satisfacer G5. | Requiere confirmar los artefactos de ONE. La modularidad upstream no es evidencia suficiente. |
| Requiere medición | RSS, startup, build limpio/incremental y compilación por fase en la máquina de trabajo. | Medir con la implementación, separando dependencia común y coste marginal. |
| Requiere medición | Reescrituras y objetos bit-idénticos bajo borrado/renombrado, y ausencia de símbolos ajenos. | Gates del sistema implementado; no sustituirlos por una inspección documental. |
| Requiere experiencia | Fricción de APIs/ODS, coste real de los cuatro pases e impacto de cambios upstream. | Registrar adaptaciones y mantenimiento; fijar versiones durante la campaña. |

Las fuentes externas se consultaron el 15 de septiembre de 2026. Las páginas oficiales y enlaces a `main` describen el estado consultado, no una release de implementación ya seleccionada. Al adoptar el ADR se deberá fijar revisión/versión y configuración; esta recomendación no depende de usar continuamente upstream `main`.

No se propone un experimento previo porque medir un verifier/intérprete diminuto no estimaría bien la carga completa de SSA mutable, cuatro pases, backend y mantenimiento. Podría medir bootstrap y RSS, pero no existe hoy un umbral decisivo que permita convertir esos números en ganador sin inventar una preferencia. La cláusula «idealmente un prototipo» de Q1 no es una obligación; el encargo exige no hacerlo salvo empate real.

Si aparece una limitación concreta de memoria, latencia o cierre que cambie esta conclusión, se reabre la dimensión afectada con un experimento diseñado para ese obstáculo. No se posponen Q1 ni O1 para resolver Q13/H6, y no se alteran los demás requisitos previos al código indicados por el vault.

## 9. ADR-ready recommendation

**Estado propuesto:** recomendación pendiente de aceptación. Sin número de ADR asignado.

**Decision.** Implementar O1 principalmente en C++, con Core-O1 como dialecto propio sobre una revisión fijada de MLIR. Reutilizar su representación y maquinaria estructural. ONE conserva el contrato, la descarga semántica, legalidad del join, interfaces, políticas/reglas de transformación, intérprete independiente, backend y aparato experimental.

**Scope.** Core-O1 v0.1 y perfiles O1 vigentes. Backend x86-64 con legalización/selección y asignación reales controladas por ONE; codificación/ELF delegables a un emisor externo contabilizado. Sin adopción automática de LLVM IR, optimizador LLVM o LLVM CodeGen. Sin fijar niveles o dominios posteriores.

**Rationale.** MLIR aloja el contrato sin imponer la semántica de LLVM y evita reconstruir infraestructura genérica con riesgos transversales. Permite instrumentar la ruta semántica y componer herramientas/runtime por separado. O1 no exige controlar el layout físico de sus nodos; sí exige medir su coste común. La recomendación es arquitectónica, no una afirmación de mejor rendimiento o menor footprint medidos.

**Alternatives rejected.** Rust con infraestructura propia queda como alternativa de salida ante restricciones físicas o acoplamiento demostrado; no se justifica su coste inicial con necesidades actuales. Rust sobre MLIR añade bindings y conserva el sustrato nativo. C++ propio pierde el ahorro estructural. Un pipeline LLVM completo introduce otra capa de semántica y atribución que no es necesaria para iniciar O1.

**Consequences.** Definir operaciones propias y verifier V1–V12; mantener reglas versionadas, terminación, pruebas y ablaciones. Separar procedencia borrable de semántica. Derivar enlace y registros del grafo, contabilizar dependencias externas y no enlazar MLIR al runtime. Conservar independencia semántica del intérprete. Aceptar el peso de build, la superficie nativa sin garantías de memoria y un coste de salida alto en la implementación de pases. Todos los claims permanecen `untested`.

**Review conditions.** Reabrir si: (a) implementar el contrato requiere cambiar el núcleo de MLIR o debilitar un gate; (b) la closure retiene capabilities ajenas por dependencias/raíces inevitables, tras agotar composición ordinaria; (c) una medición identifica almacenamiento, startup o build como impedimento material para ejecutar la campaña, sin solución local razonable; o (d) una necesidad efectiva posterior demuestra incompatibilidad con E1–E7. Un coste desconocido no es por sí solo un bloqueo, y una preferencia de lenguaje no es una condición de revisión.
