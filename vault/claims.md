---
id: CLM-001
kind: registry
status: accepted
---
# Registro de claims

Qué intenta demostrar ONE, qué no afirma y qué observación cambiaría cada estado. Sustituye a `research/hypotheses.md` de v0.1: H1–H7 conservan su significado y pasan a tener forma operacional, falsador y campaña capaz de evaluarlos.

**Estados de claim.** `untested` · `supported` (sobrevivió a su falsador bajo el protocolo citado; nunca “probado”) · `refuted` · `inconclusive` (el protocolo no pudo discriminar, por ejemplo por métrica inválida) · `withdrawn` (retirado con motivo). Todo cambio de estado cita entradas de [evidence/ledger.md](evidence/ledger.md).

> **Estado a 2026-09-14 (vault v0.2.0): todos los claims están `untested`. No existe evidencia observada.**

## 1. Hipótesis globales

| ID | Enunciado operacional | Falsador | Campaña más temprana con poder discriminante | Lo que O1 no puede aportar |
|---|---|---|---|---|
| **H1** — Convergencia útil | Para pares de orígenes con semánticas distintas existe un punto de convergencia ([ADR-004](decisions/ADR-004-semantic-discharge-convergence.md)) tras el cual análisis, optimización, backend y verificación son de un solo ejemplar y origin-blind, sin que antes de ese punto los orígenes pierdan las optimizaciones que los hacen competitivos. | Para algún par admitido, el join solo se alcanza con opacidad computacional, dependencia de origen post-join, pipelines post-join separados o lowering de la semántica rica antes de las optimizaciones que la necesitan. | O1 (forma débil); EXP-02/DSP (primera forma fuerte). | Que la convergencia sobreviva a semánticas no imperativas (tasas, tiempo, dataflow). |
| **H2** — Reutilización transversal | Un mecanismo de conocimiento T2 (ADR-004) implementado una vez produce beneficio medido por ablación en workloads de al menos dos orígenes. | Solo optimizaciones de clase baja (folding, DCE) tienen beneficio dual, o las de clase media/alta necesitan variantes por origen. | O1 (C-O1-3, forma débil); EXP-05. | Reutilización entre dominios estructuralmente distintos. |
| **H3** — Backend multiplicador | Añadir un backend beneficia a todos los orígenes soportados con trabajo origin-specific en el backend ≈ 0. | El segundo backend requiere trabajo proporcional al número de orígenes. | EXP-03. | Multiplicación (O1 tiene un backend); solo su precondición, C-O1-5. |
| **H4** — Generalidad compacta | Cada artefacto paga por su capability closure; el coste marginal de una capability no depende de capabilities no relacionadas. | Un artefacto mínimo contiene o paga por capabilities no usadas sin coste común medido y justificado. | O1 (C-O1-6, dos rutas); EXP-04. | Closure con muchos dominios. |
| **H5** — Densidad competitiva | Para una superficie dada, el vector de complejidad de ONE ([métricas §7](validation/metrics.md)) no está dominado por la composición práctica de sistemas especializados con garantías equivalentes. | La composición domina en el vector. | Requiere ≥3 dominios. | O1 solo produce línea base y una comparación pequeña (C-O1-8), no concluyente para H5. |
| **H6** — Ventaja arquitectónica nueva | Existe al menos una capacidad u optimización observable que la composición de infraestructuras existentes no logra o logra con coste materialmente mayor. | Toda capacidad de ONE es reproducible por composición (MLIR, LLVM, QEMU, lifters) con coste comparable. | **Sin candidato concreto registrado.** | Solo evidencia exploratoria (C-O1-8). |
| **H7** — Amplitud sin collage | Al añadir dominios, la fracción de mecanismos T1/T2 compartidos no decrece y el coste marginal de integración no crece superlinealmente. | Cada dominio añade optimizer, backend o runtime casi independientes. | Longitudinal desde EXP-02. | Tendencia (O1 es un punto). |

**H6 es el claim más débil del registro.** Mientras no exista un candidato concreto, ONE no tiene tesis diferencial frente a la composición de sistemas existentes; solo una apuesta. Registrar un candidato falsable es una pregunta abierta con horizonte anterior a EXP-03 ([Q13](roadmap/open-questions.md)).

## 2. Claims de O1

Alcance común: perfiles ONE-C-O1, RV64IM-O1 y x86-64-O1 ([SPEC-003](spec/o1-profiles.md)), Core-O1 ([SPEC-002](spec/core-o1.md)), relaciones de [SPEC-001](spec/semantics.md), bajo el protocolo [VAL-004](validation/o1-protocol.md). Gates `G*` y umbrales `U*` se definen allí. Todos `untested`.

| ID | Enunciado | Falsador | Gates / umbrales | Apoya |
|---|---|---|---|---|
| **C-O1-1** — Join sin opacidad ni origen | Todo programa aceptado por ambos frontends baja a Core-O1 legal en el join; ninguna construcción computacional admitida requiere operación opaca; el pipeline post-join es único y supera la prueba de borrado de procedencia. | Un op opaco computacional; salida post-join no idéntica tras borrado; configuración post-join distinta por origen; rama keyed por origen en código post-join. | G2, G3 | H1 |
| **C-O1-2** — Corrección por origen | Cada ruta refina la semántica de su origen sobre el corpus congelado y el presupuesto de fuzzing preregistrado, con cero miscompilaciones abiertas y todo `unknown` reportado. | Contraejemplo reproducible abierto al cierre; corrección obtenida debilitando semántica. | G1, G6 | precondición de todos |
| **C-O1-3** — Conocimiento de optimización compartido | Las cuatro optimizaciones fuertes requeridas (SCCP; GVN/CSE; una optimización de memoria sensible a efectos; una transformación de bucles) son T2 con M1–M4 y su ablación muestra beneficio en ambos orígenes en held-out. | Alguna necesita reglas por origen para disparar en ambos; beneficio nulo o negativo en un origen; beneficio solo en desarrollo. | G3, U4 | H2 |
| **C-O1-4** — Convergencia representacional atribuible | En pares independientes, la divergencia residual tras canonicalización se explica mecánicamente, por ablación, mediante las clases residuales RC1–RC4 de SPEC-001; la fracción no explicada queda bajo el umbral calibrado con controles. | Fracción no explicada sobre umbral. Si la métrica no separa controles positivos de negativos, el claim es `inconclusive`, no `supported`. | G8, U1 | H1 |
| **C-O1-5** — Backend único | Un backend x86-64 sin lowering, selección ni runtime condicionados por origen sirve ambas rutas y refina Core-O1 (diferencial contra el intérprete de referencia). | Regla seleccionada por origen; divergencia con el intérprete. | G1, G4 | precondición de H3 |
| **C-O1-6** — Capability closure | Herramientas y objetos generados de un origen no contienen símbolos ni dependencias del otro; objetos C no enlazan runtime guest; costes marginales medidos. | La auditoría de símbolos o dependencias falla. | G5 | H4 |
| **C-O1-7** — Origin gap acotado | `cost(ONE-RV,K) / cost(ONE-C,K)` en instrucciones ejecutadas deterministas queda bajo umbral, con ONE-C por encima del suelo de calidad frente a Clang/GCC. | Umbral excedido. Si ONE-C queda bajo el suelo, el gap no es interpretable y el claim es `inconclusive`. | U2, U3 | H1 |
| **C-O1-8** — Frente a la composición (exploratorio) | Frente a Clang + Rellume + LLVM sobre la misma superficie, ONE presenta ventaja en al menos una dimensión preregistrada (origin gap, contaminación de estado guest, closure, complejidad) sin pérdida de corrección ni de garantías. | La composición domina en todas las dimensiones preregistradas. Un resultado negativo no refuta H1, pero deja H6 sin apoyo en O1. | G6 | H6, H5 |
| **S-O1-9** — Robustez con pares derivados (secundario) | Corrección y convergencia de pares C → compilador RISC-V → ONE-RV se mantienen entre compiladores, versiones y niveles de optimización. | Fallos de corrección o sensibilidad no explicada. | G1 | Nunca titular |

## 3. Qué no afirma ONE

- Que C, una ISA, DSP, media, ML o radio sean semánticamente equivalentes.
- Novedad de: IR compartido, SSA, IR multinivel, dialectos, lowering progresivo, lifting binario, DBT sobre IR común, reutilización de frontends o backends, machine IR, runtimes especializados, stacks tensor/dataflow, translation validation o equality saturation. Ver [trabajo relacionado](research/related-work.md).
- Que implementar algo propio sea novedad o evidencia.
- **O1 no demuestra la tesis global.** C y RV64 son cómputo imperativo, escalar y basado en memoria. O1 solo puede mostrar que el join propuesto no es falso ya en el par más cercano y que el aparato de medición funciona.
- O1 no es DBT ni emulación. La capacidad se llama “lifting y ejecución de funciones RV64IM”.
- O1 no es un compilador de C. ONE-C-O1 es un subconjunto nombrado; ningún resultado se generaliza a “C”.
- Pruebas diferenciales, fuzzing y validación acotada no son verificación formal.
- Similaridad de IR no prueba equivalencia; equivalencia no implica convergencia; convergencia no implica reutilización; ninguna implica calidad ([ADR-004](decisions/ADR-004-semantic-discharge-convergence.md)).
- O1 no afirma superioridad de rendimiento frente a Clang, GCC, QEMU o LLVM.

## 4. Trazabilidad

| Claim | Decisiones | Contratos | Protocolo | Evidencia |
|---|---|---|---|---|
| C-O1-1 | ADR-001, ADR-004, ADR-005 | SPEC-001 §6, SPEC-002 | VAL-004 G2, G3 | — |
| C-O1-2 | ADR-004, ADR-006 | SPEC-001 §3–4, SPEC-003 | VAL-004 §7, G1, G6 | — |
| C-O1-3 | ADR-001, ADR-004 | SPEC-002 §10 | VAL-004 U4; VAL-003 §4 | — |
| C-O1-4 | ADR-004, ADR-006 | SPEC-001 §9 | VAL-004 §6, G8, U1; VAL-003 §3 | — |
| C-O1-5 | ADR-004 | SPEC-003 §3 | VAL-004 G4 | — |
| C-O1-6 | ADR-003 | ARC-005 | VAL-004 G5; VAL-003 §6 | — |
| C-O1-7 | ADR-006 | SPEC-003 | VAL-004 U2, U3; VAL-003 §8 | — |
| C-O1-8 | ADR-006 | — | VAL-004 §11 | — |
| S-O1-9 | ADR-006 | SPEC-003 | VAL-004 §5 | — |
