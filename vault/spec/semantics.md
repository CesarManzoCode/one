---
id: SPEC-001
kind: spec
status: designed
version: 0.1
---
# Fundamentos semánticos: observación, relaciones, descarga y olvido

Define qué significa “preservar semántica” en cada arista de un pipeline ONE, qué es el join de [ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md) en términos verificables y qué información puede perderse, y cuándo. Las instancias concretas para O1 están en [SPEC-002](core-o1.md) y [SPEC-003](o1-profiles.md).

## 1. Modelo de observación

Un **programa** `P` en un nivel `L` se ejecuta en una **configuración inicial** `E`: argumentos, contenido de memoria, estado del entorno. `Beh_L(P, E)` es el conjunto de **observaciones** posibles; tiene más de un elemento si la semántica es no determinista.

Una observación es un par `(resultado, estado final proyectable)`. Resultados:

| Resultado | Significado | Tratamiento |
|---|---|---|
| `return(v⃗)` | Terminación normal con valores. | Observable. |
| `trap(k, p⃗)` | Terminación por trap definido con etiqueta `k` y payload `p⃗`. | Observable. |
| `ub` | Se violó una precondición. | Si una ejecución de la fuente puede alcanzar `ub`, esa ejecución admite cualquier observación. |
| `unsupported(r)` | La implementación no cubre el comportamiento requerido. | No es comportamiento de la fuente. No viola refinamiento, pero nunca cuenta como éxito y permanece en denominadores. |
| `resource(r)` | Límite de implementación (pila del host, memoria). | Igual que `unsupported`. |
| `timeout` | Agotamiento del combustible del harness. | Inconcluso. |

## 2. Proyecciones

Una **proyección** `π` selecciona qué parte de una observación se compara.

- `π_orig` — **proyección de origen**, completa, para corrección por origen:
  - C: valor de retorno y bytes finales de todos los objetos visibles para el contrato y globales;
  - RV64IM: resultado, payload del trap (incluido el pc que falla), los 31 registros enteros y el contenido de todas las regiones escribibles del mapa de memoria.
- `π_K` — **proyección de contrato**, para comparaciones entre orígenes: valores de retorno según los tipos del contrato `K` y bytes de las regiones que `K` declara observables. Los traps solo son observables si `K` los admite; en la campaña primaria de O1 no los admite.

Tiempo, asignación de registros, ubicaciones de depuración y bytes fuera de la proyección no son observables salvo que la proyección los incluya.

## 3. Relaciones

**Refinamiento.** `T ⊑[R, π] S` sii para todo par de configuraciones `(E_S, E_T) ∈ R`:

- si alguna ejecución de `S` desde `E_S` alcanza `ub`, no se exige nada a esa ejecución;
- en caso contrario, `π(Beh(T, E_T) ∖ {unsupported, resource, timeout}) ⊆ π(Beh(S, E_S))`.

`R` relaciona configuraciones entre niveles (por ejemplo, un binding de ABI). Un refinamiento puede resolver no determinismo de la fuente eligiendo un comportamiento; no puede introducir comportamientos nuevos fuera de `ub`.

**Equivalencia exacta.** Refinamiento en ambas direcciones con la misma `π`. Para semánticas deterministas sin `ub`, es igualdad de la observación única.

**Equivalencia observacional bajo contrato.** Para un contrato `K` con precondición ejecutable `Pre(K)` y relación de entrada `R_in(K)`, dos implementaciones `A` y `B` de orígenes distintos son equivalentes bajo `K` sii para toda entrada `x ∈ Pre(K)`: ninguna de las dos alcanza `ub` y `π_K(Beh(A, R_in^A(x))) = π_K(Beh(B, R_in^B(x)))` es un único elemento. Para semánticas con no determinismo admitido, la relación se sustituye por refinamiento declarado en una dirección; nunca por similaridad.

**No determinismo del entorno.** Si la configuración de un origen deja valores sin especificar (por ejemplo, registros no argumento en RV64IM), la semántica los cuantifica universalmente. Una implementación puede fijarlos (refinamiento). Un workload solo es válido para `K` si su comportamiento de referencia no depende de esos valores; se comprueba ejecutando la referencia con valores distintos.

## 4. Relaciones por arista en O1

| Arista | Relación | Proyección | Notas |
|---|---|---|---|
| Fuente ONE-C-O1 → Core-O1 (join) | refinamiento | `π_orig` C | El perfil fija lo implementation-defined y el orden de evaluación. El `ub` de C se descarga como precondiciones o hechos (§5); el frontend no lo explota más allá. |
| Imagen RV64IM-O1 → Core-O1 (join) | equivalencia exacta | `π_orig` RV | La semántica RV64IM del EEI no tiene `ub`: el lifter no tiene libertad salvo el no determinismo del entorno. |
| Core-O1 → Core-O1 (pase o canonicalización) | refinamiento | `π_orig` del origen | Relación por pase; transitiva a lo largo del pipeline. |
| Core-O1 → objeto x86-64 + runtime | refinamiento bajo binding ABI | build `exact-state`: `π_orig`; build `contract`: `π_K` | SPEC-003 §3. |
| Implementación C ↔ implementación RV del mismo `K` | equivalencia observacional bajo `K` | `π_K` | Solo sobre `Pre(K)`. Nunca justifica que un frontend explote `Pre(K)`. |

**Totalidad de frontends.** Las relaciones frontend → join se exigen para *todas* las configuraciones del origen, no solo para `Pre(K)`. Un frontend que asume `Pre(K)` es debilitamiento semántico (ADR-004 §5).

## 5. Parcialidad y hechos

- **Precondición.** Una operación parcial declara un predicado sobre sus operandos y estado. Si es falso en ejecución, el resultado es `ub` en ese punto (`ub` inmediato). No existen valores indefinidos.
- **Trap.** Un comportamiento definido de terminación se expresa con un terminador `trap` explícito y alcanzado por control explícito. Una precondición nunca produce un trap implícito.
- **Hecho.** Anotación sobre una operación cuyo significado es una precondición adicional (`nsw`: el resultado con signo es representable).
  - **F1** — cada hecho tiene semántica formal como precondición;
  - **F2** — descartar un hecho es siempre refinamiento válido;
  - **F3** — introducir un hecho exige justificación: semántica del origen (el `ub` de desbordamiento con signo en C) o prueba de un análisis;
  - **F4** — mover o duplicar una operación a un punto donde podría ejecutarse sin haberse ejecutado en el programa original (especulación) exige que su precondición y sus hechos estén probados en el punto destino, o descartar los hechos. Si la precondición de la operación no puede probarse, no se especula.

## 6. Join y pruebas operacionales

El join de una campaña es una etapa de legalidad declarada que cumple J1–J4 de ADR-004. Se comprueba así:

| Prueba | Procedimiento | Resultado exigido |
|---|---|---|
| **Legalidad** | El verificador del contrato core se ejecuta sobre la salida de cada frontend. | Ninguna operación, tipo, hecho o atributo fuera del contrato. |
| **Borrado de procedencia** | Se eliminan ubicaciones, mapas de pc, nombres de origen, dialecto de origen y cualquier atributo del espacio borrable. Se ejecuta el pipeline post-join con y sin borrado. | Salida bit-idéntica (IR final, objeto y decisiones registradas). |
| **Borrado de identidad de workload** | Igual, eliminando nombres de función, símbolo y workload, sustituidos por nombres neutros. | Salida idéntica módulo renombrado. |
| **Configuración única** | Comparación de la configuración post-join usada para cada origen. | Idéntica. |
| **Auditoría estática** | Búsqueda en código post-join de identificadores de origen o dialecto de origen, más revisión. | Cero ramas keyed por origen. |
| **Exclusividad de operaciones** | Distribución de clases de operación por origen en el corpus. | Toda clase emitida por un solo origen tiene justificación semántica registrada. No es un gate: es diagnóstico de contaminación. |

**Procedencia.** Todo lo que un pase post-join o el backend necesitan para producir comportamiento observable es un valor u operación del IR. Por ejemplo, el pc que falla en un trap guest es un operando del `trap`, no metadato. Lo demás vive en un espacio de atributos borrable.

## 7. Contratos de olvido

Cada lowering declara, por clase de información, qué elimina, bajo qué condición y qué queda imposible después.

| Clase | Contenido | Regla |
|---|---|---|
| **I1 Obligaciones** | `ub`, precondiciones del origen. | Solo se eliminan convirtiéndolas en precondición explícita o hecho, o descartándolas, lo que es refinamiento y se registra como pérdida. |
| **I2 Hechos** | Suposiciones ya explícitas. | Descartables en cualquier punto; la pérdida se registra. |
| **I3 Estructura** | Bucles, regiones, tipos del origen, campos, forma del control. | Eliminable si ningún consumidor posterior declarado la requiere; si se recupera por análisis, se nombra el análisis. |
| **I4 Procedencia** | Ubicaciones, pc de instrucción no observable, nombres. | Siempre borrable; nunca influye en semántica ni en decisiones post-join. |
| **I5 Entorno** | ABI, EEI, mapa de memoria, etiquetas de trap. | Nunca implícita: se materializa como operaciones, valores o comprobaciones explícitas antes de eliminarse. |
| **I6 Tiempo y planificación** | Tasas, latencias, orden de producción/consumo (dominios futuros). | Reservada. No puede codificarse solo como orden de instrucciones sin un lowering que lo declare. |

Formato por arista: `información → forma de destino → condición → optimizaciones imposibilitadas → ¿recuperable y cómo?`. Las tablas de O1 están en SPEC-003.

## 8. Cuatro propiedades y cómo se establecen

| Propiedad | Se establece con | No se establece con |
|---|---|---|
| Equivalencia semántica | Semánticas ejecutables, ejecución diferencial, validación acotada. | Similaridad de IR. |
| Convergencia representacional | Métricas de VAL-003 §3 calibradas con controles. | Igualdad de nombres de pases. |
| Reutilización de mecanismos | T1/T2 con M1–M4, ablación. | Que ambas rutas llamen al mismo pass manager (T0). |
| Calidad de resultado | Costes medidos frente a baselines con garantías equivalentes. | Cualquiera de las tres anteriores. |

## 9. Clases residuales entre orígenes

La divergencia entre las formas post-join de dos implementaciones equivalentes bajo `K` se atribuye a clases declaradas. Cada clase tiene un **interruptor de ablación** que elimina su causa en una variante de diagnóstico. Las variantes no fieles nunca producen resultados de titular.

| Clase | Causa | Ablación | ¿Fiel? |
|---|---|---|---|
| **RC1** Asimetría de hechos | Un origen aporta hechos (`nsw`, frescura de slots) que el otro no tiene. | A1: descartar hechos del origen C. | Sí; descartar hechos es refinamiento. |
| **RC2** Preservación de traps | Comprobaciones explícitas del origen con traps definidos: acceso a memoria guest, guardas de división, alineación de destino, guardas de retorno. | A2: omitir comprobaciones bajo `Pre(K)`. | No; diagnóstico. |
| **RC3** Estado guest y ABI | Llamadas con estado completo, materialización de registros, extensión de signo LP64. | A3: estrechar llamadas asumiendo conformidad ABI. | No; diagnóstico. |
| **RC4** Modelo de memoria | Slots nativos frente a marcos de pila en memoria guest; traducción de base. | A4: suponer disjunción de pila guest. | No; diagnóstico. |

La divergencia que persiste con A1–A4 aplicadas es **no explicada**. Incluye las diferencias de elección representacional del autor dentro del mismo algoritmo (índice frente a puntero, forma del bucle, orden de cálculos independientes), que son precisamente lo que la canonicalización debe eliminar. No existe una clase residual para ellas.
