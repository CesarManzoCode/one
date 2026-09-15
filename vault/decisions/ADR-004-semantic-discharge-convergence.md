---
id: ADR-004
kind: decision
status: accepted
---
# ADR-004 — Convergencia por descarga semántica y mecanismos origin-blind

## Contexto

[ADR-001](ADR-001-one-core.md) exige reutilización material pero no define cuándo dos orígenes han convergido ni qué distingue reutilizar conocimiento de compartir utilidades. Sin esa definición:

- “mismo optimizer” puede ocultar reglas seleccionadas por origen detrás de un nombre compartido;
- el core puede adoptar la semántica de un origen como universal: punteros C como enteros (invalida optimizaciones C) o direcciones guest con identidad de objeto (inventa semántica que la máquina no tiene);
- similaridad textual de IR puede presentarse como equivalencia o como integración.

## Decisión

Alcance: global. La semántica precisa y las pruebas operacionales están en [SPEC-001](../spec/semantics.md).

1. **Punto de convergencia (join).** Toda afirmación de convergencia nombra un join: una etapa de legalidad declarada en una spec versionada que cumple:
   - **J1** — toda operación, tipo, hecho y atributo legal en el join tiene semántica definida por el contrato del core, independiente del origen;
   - **J2** — ninguna obligación del origen queda implícita: toda precondición cuya violación produce `ub` o un trap es explícita en una operación o en código;
   - **J3** — el significado de un programa legal en el join depende solo de su contenido, nunca de tablas o metadatos asociados al origen;
   - **J4** — el argumento de corrección de cada mecanismo posterior al join se formula solo contra el contrato del core.
2. **Descarga semántica.** Antes del join, cada obligación del origen se convierte en una de estas formas: operación explícita; precondición explícita con resultado declarado (`ub` o trap); hecho descartable; u olvido declarado en el contrato de olvido de esa arista. Nunca en una suposición implícita.
3. **Origin-blindness.** Los mecanismos posteriores al join (análisis, canonicalización, optimización, backend, verificación) no consultan origen, dialecto de origen ni procedencia. Consultan hechos e interfaces semánticas. Se exige operacionalmente:
   - **prueba de borrado**: eliminar toda procedencia deja la salida post-join bit-idéntica;
   - una única configuración de pipeline post-join para todos los orígenes;
   - cero ramas keyed por origen en código post-join.

   Resultados distintos entre orígenes son legítimos solo si provienen de contenido semántico distinto (por ejemplo, hechos que un origen aporta y otro no).
4. **Hechos descartables.** Un hecho es una precondición cuya falsedad produce `ub`. Descartarlo es siempre un refinamiento válido. Introducirlo exige justificación: semántica del origen o prueba de un análisis. Metadatos que afectan legalidad o comportamiento son semántica, no metadatos.
5. **Relación por arista.** Cada frontend, lowering, pase y backend declara su relación semántica. Un frontend refina la semántica completa de su origen para **todas** las entradas, no solo para las entradas de un contrato experimental; explotar precondiciones de un experimento es debilitamiento semántico.
6. **Cuatro propiedades distintas.** *Equivalencia semántica*, *convergencia representacional*, *reutilización de mecanismos* y *calidad de resultado* se afirman y miden por separado. Ninguna implica otra; toda afirmación nombra cuál.
7. **Reutilización material.** Se clasifica en tres niveles:
   - **T0 utilidad**: contenedores, arenas, pass manager, printers, algoritmos de grafos genéricos;
   - **T1 mecanismo semántico**: verificador, intérprete de referencia, canonicalización, lowering de backend, asignación de registros, emisión;
   - **T2 conocimiento**: análisis y reglas de optimización.

   Solo T1 y T2 reciben crédito de integración arquitectónica, y solo si cumplen: **M1** un único ejemplar sin despacho por origen; **M2** está en la ruta semántica de ambos orígenes; **M3** su argumento de corrección se enuncia una vez contra el contrato del core; **M4** es ejercitado dinámicamente por el corpus de ambos orígenes. T0 se reporta, nunca cuenta como integración.

## Alternativas consideradas

- **Core con la semántica de un origen** (direcciones planas sin descarga, u objetos con procedencia para todo): rechazada; invalida optimizaciones C o inventa identidad de objetos para código guest.
- **Puntero universal etiquetado** (dirección + procedencia opcional consultada por pases): rechazada por ahora; la procedencia opcional se convierte en rama por origen. Reabrible si se mide pérdida de optimización atribuible a la descarga ([Q4](../roadmap/open-questions.md)).
- **Pases conscientes de dialecto u origen con reglas especializadas**: rechazada; es la ilusión de nombre compartido.
- **Convergencia definida por similaridad de IR**: rechazada; no es semántica y es manipulable.
- **Metadatos descartables con efecto semántico**: rechazada; lo que cambia legalidad es semántica.

## Base

Razonamiento propio y del [research de consolidación](../research/ONE-Technical-Foundation-Consolidation-Research.md) §4, §8–§11, §16. Hechos externos: los flags `nsw`/`nuw` de LLVM funcionan como hechos descartables, y el manual de UB de LLVM junto con Lee et al. (PLDI 2017) documentan el coste de una semántica de indefinición mal delimitada; las interfaces y traits de MLIR permiten razonar sobre operaciones sin enumerar dialectos; QEMU TCG, Remill y Rellume modelan el estado guest como estructura, lo que muestra el riesgo de contaminar el core. **No existe evidencia observada de ONE.** Esta decisión fija un *criterio*; que un par real lo satisfaga con coste aceptable es H1 y C-O1-1.

## Consecuencias

- El contrato de cada core enumera operaciones con semántica, precondiciones y resultados ([SPEC-002](../spec/core-o1.md) para O1).
- Cada frontend publica su contrato de olvido.
- Las métricas de reutilización distinguen T0/T1/T2 ([VAL-003](../validation/metrics.md)).
- Un join que solo funciona con excepciones está mal declarado: se mueve o se cambia el contrato mediante ADR; no se añade whitelist.
- Datos observables (por ejemplo, el pc de un trap guest) son valores explícitos del IR. La procedencia (ubicaciones, mapas de pc) vive en un espacio borrable.

## Qué no decide

Número y nombres de niveles; forma del core más allá de O1; semántica de streams, tensores o tiempo; si alguna forma de procedencia debe sobrevivir al join en campañas futuras.

## Condiciones de revisión

- La prueba de borrado resulta insatisfacible sin perder corrección para un par de orígenes admitido.
- La descarga pierde optimizaciones que la ablación de hechos no explica y que un core con procedencia recuperaría, con medición.
- EXP-02 muestra que semántica de tasa o tiempo no admite descarga sin opacidad ni pases keyed por dominio.

## Relaciones

Refina ADR-001. Operacionalizado por SPEC-001 y VAL-003. Evaluado por C-O1-1, C-O1-3, C-O1-4 y C-O1-5.
