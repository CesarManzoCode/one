---
id: VAL-004
kind: validation
status: designed
version: 0.1
---
# Protocolo de la campaña O1

Operacionaliza [ADR-006](../decisions/ADR-006-o1-falsification-campaign.md) y los claims C-O1-1…C-O1-8 y S-O1-9 del [registro](../claims.md). Las métricas se definen en [VAL-003](metrics.md); la semántica, en [SPEC-001](../spec/semantics.md)–[SPEC-003](../spec/o1-profiles.md).

Estado `designed`. Pasa a congelado en el commit de preregistro ([gobierno](../governance.md), regla 7). Los gates de §8 están fijados desde esta versión. Los umbrales de §9 se fijan en el preregistro bajo las restricciones que aquí se establecen.

## 1. Qué puede y qué no puede mostrar O1

Puede refutar, o dejar vivas, las formas débiles de H1 y H2 para dos orígenes imperativos, medir closure (H4) y comparar contra una composición existente. No puede apoyar la tesis global: C y RV64 comparten modelo imperativo, escalar y basado en memoria. Si O1 sobrevive, gana el derecho a ser atacado por DSP; no gana la tesis.

## 2. Contratos de comportamiento `K`

Un contrato es independiente de ambos frontends.

| Campo | Contenido |
|---|---|
| Identidad | ID y versión. |
| Firma | Hasta 6 parámetros de tipos `i8…i64`, `u8…u64`, `region<L, n>`; retorno de tipo entero o nada. |
| Layout | Layout `L` de cada región: tipo entero o `struct` con offsets y anchos explícitos. |
| Memoria inicial | Tamaños, generador de contenidos. Regiones disjuntas por defecto; el aliasing se declara como clase de entrada propia. |
| `Pre(K)` | Predicado ejecutable sobre la entrada, con cota de pasos. |
| Algoritmo abstracto | Pseudocódigo o máquina de estados que fija el algoritmo, no su representación. |
| Libertad representacional | Qué puede variar el autor: índice o puntero, forma del bucle, orden de cálculos independientes, reducción de fuerza manual, ubicación en registro o memoria. |
| Observables | `π_K`: retornos y regiones proyectadas. En la campaña primaria solo se admite `return`. |
| Entradas | Generador y semillas para desarrollo, held-out y casos frontera. |
| Estrato | §3. |

## 3. Corpus

**Estratos**, preregistrados; ninguno puede quedar vacío en desarrollo ni en held-out:

| Estrato | Contenido |
|---|---|
| S1 | Aritmética y bits sin memoria. |
| S2 | Bucles de lectura sobre regiones del llamador. |
| S3 | Bucles de escritura, con clases de aliasing declaradas. |
| S4 | Llamadas y recursión. |
| S5 | Locales en memoria: arrays y structs locales frente a marcos de pila guest. |
| S6 | Control irregular: salidas tempranas, bucles anidados, `switch`. |

**Particiones**:

- **desarrollo**: visible;
- **held-out**: escrita con el mismo procedimiento y sellada antes de empezar canonicalización y pases compartidos. Se custodia como archivo cifrado con hash comprometido; la clave solo se usa en la ejecución preregistrada;
- **controles**: §6.

Tamaños por estrato: [Q10](../roadmap/open-questions.md), fijados en el preregistro.

## 4. Pares independientes (campaña primaria)

**Procedimiento de autoría**:

1. Cada implementación se escribe a partir de `K` solamente. El autor RV64IM no ve la implementación C ni salidas de compilador para `K`, y viceversa.
2. El orden de autoría por contrato se aleatoriza.
3. Está prohibido compilar o desensamblar la contraparte y copiar patrones de salida de compilador.
4. Si interviene IA: sesiones separadas cuyo único contenido compartido es `K`, con modelo, sesión y hash del prompt registrados. Usar el mismo modelo en ambos lados se permite, pero se registra como autoría correlacionada y el reporte se estratifica por fuente de autoría.

**Detector de derivación** (mecánico):

- para cada par se compila la implementación C con al menos GCC y Clang a `-O0`, `-O1`, `-O2`, `-O3` y `-Os` con `-march=rv64im -mabi=lp64`;
- se calcula la distancia de edición normalizada entre la secuencia de opcodes RV del autor y cada salida, tras alfa-renombrado de registros y abstracción de inmediatos, además de la distancia de forma del CFG;
- los pares por debajo del umbral U6 se reclasifican como derivados: se reportan en la campaña secundaria y no se descartan;
- U6 se calibra con pares derivados conocidos y con los controles N1.

## 5. Pares derivados (campaña secundaria)

C → {GCC, Clang} × {versiones congeladas} × {`-O0`, `-O1`, `-O2`, `-Os`} × `rv64im`/`lp64` → imagen → ONE-RV.

Uso: corrección (C-O1-2), robustez de lifting y sensibilidad a compilador y flags (S-O1-9). Nunca entran en titulares de convergencia. El fuzzing entre orígenes usa esta vía, porque los programas generados no pueden tener autoría independiente.

## 6. Controles de métrica

| Control | Construcción | Expectativa |
|---|---|---|
| **P1** positivo | Una implementación C y variantes con perturbaciones sintácticas que preservan semántica: renombrado, orden de declaraciones, paréntesis redundantes. | Core post-canonicalización idéntico. Si no, es un defecto de determinismo del frontend o de la canonicalización. |
| **N1** negativo | Dos implementaciones de `K` con algoritmos abstractos distintos declarados (por ejemplo, popcount por bucle frente a SWAR). | No deben aparecer como convergidas. |
| **N2** sensibilidad | Contratos distintos con forma similar (suma frente a xor-fold). | La métrica distingue clases de operación. |
| Referencia superior | Par derivado Clang `-O2`. | Se reporta; no es control. |

**Validez (G8)**: una métrica de convergencia solo es válida en la campaña si separa P1 de N1 con el margen fijado en U1. Si no los separa, C-O1-4 queda `inconclusive`.

## 7. Matriz de corrección

| Capa | Oráculos | Método | Evidencia exigida |
|---|---|---|---|
| Aceptación de ONE-C-O1 | SPEC-003 §1.2–1.3 | Corpus de conformidad: cada fila aceptada y rechazada con casos | 100 % de filas cubiertas |
| `Pre(K)` en C | Clang con UBSan + ASan; Cerberus donde lo soporte | Cada entrada se ejecuta bajo detectores; una detección invalida la entrada | Clases de `ub` no cubiertas por los detectores, declaradas |
| Ruta C extremo a extremo | Clang y GCC (`-O0`, `-O2`) | Diferencial sobre entradas válidas | Todas las divergencias resueltas |
| Decodificador RV | Decodificador derivado de Sail | Clasificación legal/ilegal y campos: exhaustiva sobre las 2³² palabras si su coste se confirma; si no, exhaustiva por opcode mayor más aleatoria | Cobertura declarada |
| Semántica por instrucción | Sail y Spike configurados `rv64im` | Operandos aleatorios más fronteras (`0`, `±1`, `MIN`, `MAX`, frontera de 2³¹), traps incluidos | Cero divergencias |
| Lifting de funciones | Sail y Spike; subconjunto aplicable de riscv-arch-test; riscv-dv restringido a `rv64im` | Estado final bajo `π_orig` con el build `exact-state` | Cero divergencias |
| Intérprete Core-O1 | Tabla de SPEC-002 §5 expresada en `QF_BV` | Tests dorados por operación, tests de propiedades, detección de `ub` | Cero divergencias |
| Canonicalización y pases | SMT acotado; intérprete | Validación local por regla (SPEC-002 §9); diferencial antes/después sobre corpus y sobre programas Core generados sin `ub` | `unknown` contado por separado |
| Backend | Intérprete Core-O1 | Diferencial sobre funciones Core generadas y corpus; centinelas ABI; alineación de pila verificada en llamadas al runtime; desensamblado y relocations con herramienta externa | Cero divergencias |
| Entre orígenes | Clang nativo, Spike, ONE-C, ONE-RV | `π_K` sobre `Pre(K)` en las cuatro ejecuciones | Cero divergencias |

**Reglas**:

- el acuerdo diferencial es evidencia, no prueba: los errores correlacionados existen;
- cada capa usa al menos un oráculo derivado de especificación donde exista;
- `unknown` o timeout de SMT significa “no validado”, se reporta y no pasa;
- todo contraejemplo se minimiza y queda como regresión permanente;
- el fuzzing tiene presupuesto de CPU-horas preregistrado (U5) y semillas registradas.

## 8. Gates estructurales (fijados en v0.1)

| Gate | Condición | Claims |
|---|---|---|
| **G1** Corrección | Cero miscompilaciones abiertas. Tras corregir cualquiera, todas las mediciones se repiten desde cero sobre el corpus congelado. | todos |
| **G2** Opacidad computacional | Cero operaciones opacas en `J_O1` para construcciones admitidas; servicios de frontera limitados a la lista de SPEC-003 §3. | C-O1-1 |
| **G3** Origin-blindness | Prueba de borrado bit-idéntica en el 100 % del corpus; configuración post-join única; cero ramas keyed por origen post-join (SPEC-001 §6). | C-O1-1, C-O1-3 |
| **G4** Backend único | Cero reglas de legalización, selección, emisión o runtime seleccionadas por origen. | C-O1-5 |
| **G5** Closure | Cero símbolos o dependencias de la otra ruta en artefactos por origen; objetos C sin runtime guest. | C-O1-6 |
| **G6** Semántica no debilitada | Toda comparación usa garantías equivalentes o las etiqueta; ONE-RV es siempre fiel salvo variantes de diagnóstico etiquetadas; los baselines usan flags congelados con suposiciones equivalentes. | C-O1-2, C-O1-8 |
| **G7** Integridad del preregistro | Held-out no inspeccionada; hashes coinciden. | todos |
| **G8** Validez de métricas | Controles separados (§6). | C-O1-4 |

Si falla G2, G3, G4 o G5, la respuesta es la de [riesgos](../research/risks.md): rediseño del join, del contrato o de la arquitectura de dependencias. Nunca una excepción.

## 9. Umbrales cuantitativos (se fijan en el preregistro)

Hoy no se fijan números: no hay datos que los calibren y un número inventado sería arbitrario. Lo que queda fijado es cómo se establecen.

| ID | Umbral | Restricción de fijación |
|---|---|---|
| U1 | Fracción no explicada máxima para C-O1-4 y margen P1/N1 para G8 | Calibrado solo con controles y partición de desarrollo. |
| U2 | Origin gap máximo por estrato y agregado (C-O1-7) | Fijado antes de medir ONE-RV en held-out. |
| U3 | Suelo de calidad de ONE-C frente a Clang y GCC a `-O1` y `-O2` | Fijado antes de medir ONE-C en held-out. Existe para impedir que el origin gap mejore empeorando la ruta C. |
| U4 | Mínimo de contratos independientes por origen en que cada pase fuerte dispara, y beneficio mínimo | Con conteo determinista, beneficio estrictamente positivo en la media geométrica sobre workloads aplicables, en ambos orígenes. |
| U5 | Presupuestos de fuzzing y límites de SMT | Declarados por capa. |
| U6 | Umbral del detector de derivación | Calibrado con derivados conocidos y N1. |
| U7 | Dimensiones de C-O1-8 | Elegidas antes de medir la composición. |

Cada umbral lleva su justificación en el preregistro. Cambiarlo después crea una versión nueva del protocolo con reporte dual.

## 10. Medición y ablaciones

- **Coste dinámico primario**: número determinista de instrucciones x86-64 ejecutadas por la función bajo prueba, obtenido por instrumentación. La herramienta se fija en el preregistro ([Q9](../roadmap/open-questions.md)).
- **Secundario**: ciclos y tiempo según VAL-003 §8.
- Tamaño de código traducido y del runtime, por separado; tiempo de compilación por fase; RSS pico de las herramientas.
- **Ablaciones obligatorias**, siempre en ambos orígenes:
  - cada pase fuerte desactivado de uno en uno, y los cuatro a la vez;
  - A1–A4 de SPEC-001 §9 para atribución de residuos.
- Vectores de VAL-003 §3–§7.

## 11. Baselines y clases de comparación

| Comparación | Mide | Garantías | Uso |
|---|---|---|---|
| ONE-C frente a Clang/GCC `-O1` y `-O2` (x86-64 base) | Calidad de la ruta C | Equivalentes | Suelo U3 |
| ONE-RV frente a ONE-C | Origin gap | ONE-RV preserva traps: más garantías | C-O1-7 |
| ONE-RV frente a Clang nativo del C | Coste total frente a nativo | Distintas | Contexto |
| Clang + Rellume + LLVM `-O2` | Composición existente | A caracterizar: si Rellume no preserva traps de acceso, la comparación se etiqueta y se añade la variante A2 de ONE como referencia de garantías equivalentes | C-O1-8 |
| QEMU user (TCG), Spike | Referencias de ejecución | DBT o intérprete: otra clase | Solo contexto, nunca titular |

## 12. Reporte

- Resultados por workload conservados; medias geométricas solo sobre ratios compatibles.
- Fallos, `unknown`, `unsupported`, `resource`, rechazos y exclusiones en los denominadores.
- Pares derivados y variantes de diagnóstico en secciones separadas.
- Resultados negativos con el mismo detalle que los positivos.
- Una entrada del ledger por ejecución preregistrada.

## 13. Cierre de O1 y consecuencias

O1 cierra cuando cada claim C-O1 tiene un estado distinto de `untested` con entradas de ledger.

| Resultado | Consecuencia |
|---|---|
| C-O1-1…7 `supported` | O2 autorizado. La tesis global sigue sin demostrar. |
| C-O1-1 o C-O1-3 `refuted` | Rediseño del join o de Core-O1 mediante ADR antes de añadir dominios. |
| `inconclusive` por métrica inválida o por detector | Se corrige el aparato y se repite con una partición held-out nueva; la anterior queda quemada. |
| C-O1-8 negativo | H6 sin apoyo; se registra. No bloquea O2, pero obliga a registrar un candidato H6 antes de EXP-03. |
