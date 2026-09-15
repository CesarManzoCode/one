---
id: GLO-001
kind: glossary
status: accepted
---
# Glosario

Definiciones breves. La definición autoritativa está en el documento enlazado.

## Proyecto y arquitectura

**ONE** — Proyecto completo y repositorio único.

**ONE IR** — Familia de representaciones de ONE. El nombre no implica una sola representación plana ([ARC-003](architecture/ir.md)).

**ONE Core** — Núcleo compartido al que convergen orígenes distintos. Su forma a largo plazo es hipótesis; su instancia para O1 es **Core-O1** ([SPEC-002](spec/core-o1.md)).

**Origen** — Fuente concreta de cómputo con semántica propia: ONE-C-O1, RV64IM-O1. Dos orígenes pueden pertenecer a la misma familia de dominio; C y RV64 son ambos imperativos.

**Dominio** — Familia de cómputo con semánticas y optimizaciones propias: lenguajes, ISAs, DSP, media, tensores, radio.

**Frontend** — Traduce un origen a una forma legal en el join, con relación declarada y contrato de olvido ([ARC-004](architecture/frontends-backends.md)).

**Backend** — Refina el core hacia un target concreto bajo un binding de ABI ([ARC-004](architecture/frontends-backends.md)).

**Lowering** — Transformación hacia una representación más general o más cercana a máquina. Siempre declara su relación semántica y su contrato de olvido.

**X** — Hardware o backend nuevo que debería beneficiar a múltiples orígenes sin trabajo específico por origen (H3).

**EEI** — Execution environment interface: entorno que completa la semántica de una ISA (estado inicial, memoria, terminación). Para O1, SPEC-003 §2.3.

## Semántica ([SPEC-001](spec/semantics.md))

**Observación** — Resultado (`return`, `trap`, `ub`, `unsupported`, `resource`, `timeout`) y estado final proyectable.

**Proyección** — Parte comparada de una observación: `π_orig` (corrección por origen) o `π_K` (comparación entre orígenes bajo un contrato).

**Refinamiento** — La implementación no produce comportamientos que la fuente no admita, salvo donde la fuente alcanza `ub`. Es la relación de frontends C, pases y backend.

**Equivalencia observacional bajo contrato** — Igualdad de `π_K` para toda entrada de `Pre(K)`. Sustituye al término de v0.1 “cross-origin equivalence”, que confundía equivalencia con convergencia.

**`ub`** — Resultado de violar una precondición. Admite cualquier comportamiento. En Core-O1 es inmediato; no hay valores indefinidos.

**Trap** — Terminación definida y observable, expresada con un terminador explícito. Nunca la produce implícitamente una precondición.

**Obligación** — Condición del origen cuya violación carece de significado (UB de C) o tiene significado definido (trap RISC-V).

**Hecho** — Precondición adicional sobre una operación (`nsw`, `nuw`). Descartarlo siempre es válido; introducirlo exige justificación.

**Especulación** — Ejecutar una operación donde el programa original podría no ejecutarla. Exige precondición probada o descarte de hechos (F4).

**Contrato de olvido** — Declaración, por arista, de qué información se elimina, bajo qué condición y qué queda imposible (SPEC-001 §7).

**Procedencia** — Ubicaciones, mapas de pc, nombres y origen. Vive en un espacio borrable y nunca afecta a semántica ni a decisiones post-join.

## Convergencia y reutilización ([ADR-004](decisions/ADR-004-semantic-discharge-convergence.md))

**Join (punto de convergencia)** — Etapa de legalidad declarada que cumple J1–J4: semántica independiente del origen, obligaciones explícitas, significado dependiente solo del contenido y corrección post-join formulada contra el contrato del core.

**Descarga semántica** — Conversión de cada obligación del origen en operación, precondición, hecho u olvido declarado antes del join.

**Origin-blind** — Propiedad de los mecanismos post-join: no consultan origen ni procedencia. Se comprueba con la **prueba de borrado**: sin procedencia, la salida post-join es bit-idéntica.

**Convergencia representacional** — Similitud estructural de formas post-join de implementaciones equivalentes, medida con métricas calibradas por controles (VAL-003 §3). No prueba equivalencia.

**Clase residual** — Causa declarada de divergencia legítima entre orígenes (RC1–RC4), con ablación que la elimina en una variante de diagnóstico.

**Reutilización material** — Reutilización de mecanismos T1 (semánticos) o T2 (conocimiento de optimización) que cumplen M1–M4: un ejemplar, en la ruta de ambos orígenes, corrección enunciada una vez y ejercitada por ambos. Compartir utilidades (T0) no cuenta como integración.

**Operación opaca** — Operación cuya semántica en el join no está definida por el contrato del core. Distinta de un **servicio de frontera** enumerado (salida por trap, inicialización de memoria).

**Origin gap** — `cost(ONE-RV, K) / cost(ONE-C, K)` con conteo determinista de instrucciones (C-O1-7).

## Experimentación ([VAL-004](validation/o1-protocol.md), [gobierno](governance.md))

**Contrato de comportamiento `K`** — Especificación independiente de frontends: firma, memoria inicial, `Pre(K)`, algoritmo abstracto, libertad representacional y observables.

**Par independiente** — Implementaciones C y RV64IM de `K` escritas sin derivar una de otra. **Par derivado** — RV64IM obtenido compilando el C. Solo los independientes sostienen titulares de convergencia.

**Detector de derivación** — Comparación mecánica de un par independiente con salidas de compiladores para reclasificar pares derivados de facto.

**Control positivo / negativo** — Casos que una métrica debe declarar convergentes (P1) o no convergentes (N1). Una métrica que no los separa es inválida.

**Variante de diagnóstico** — Configuración no fiel (A2–A4) usada solo para atribuir residuos. Nunca produce resultados de titular.

**Preregistro** — Commit que congela protocolo, corpus, baselines, métricas y umbrales antes de una campaña.

**Held-out sellada / quemada** — Partición inaccesible hasta la ejecución preregistrada; tras usarse, pasa a desarrollo.

**Composición rival** — Combinación de sistemas existentes que ofrece la misma superficie. Para O1: Clang + Rellume + LLVM.

## Modularidad ([ARC-005](architecture/modularity-deployment.md), [VAL-003 §6](validation/metrics.md))

**Capability** — Nodo del grafo que provee operaciones, pases o servicios, con dependencias y raíces declaradas.

**Capability closure** — Cierre transitivo derivado de las capabilities de un artefacto. El artefacto no debe contener nada fuera de ella.

**Coste marginal** — `Δ(A, x) = cost(A ∪ {x}) − cost(A)`, medido sobre varias bases.

**Runtime especializado** — Artefacto que contiene solo la closure que una aplicación concreta necesita.

**Compression of complexity** — Relación entre capacidad acreditada y complejidad accidental, medida como vector y nunca como puntuación única (VAL-003 §7).
