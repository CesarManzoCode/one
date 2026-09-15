---
id: ADR-005
kind: decision
status: accepted
---
# ADR-005 — Representación ejecutable de Core-O1

## Contexto

O1 necesita un core concreto, ejecutable y verificable. [ADR-002](ADR-002-multilevel-ir.md) deja abiertos niveles y fronteras. El research compara SSA+CFG, sea of nodes, regiones estructuradas, dataflow, CPS y e-graphs. Decidir la forma de *todo* ONE Core ahora sería prematuro; no decidir la de O1 impediría implementar O1 sin inventar semántica sobre la marcha.

## Decisión

Alcance: **Core-O1**, el core de la campaña O1. La forma de ONE Core después de O1 sigue abierta. La semántica precisa está en [SPEC-002](../spec/core-o1.md).

1. **SSA tipado con CFG explícito y argumentos de bloque** (sin nodos φ). Se admiten CFG reducibles e irreducibles.
2. **Valores bitvector `iN`. Sin tipo puntero.** Las direcciones son `i64`; cada operación de memoria nombra estáticamente su espacio de memoria. La procedencia se descarga antes del join (ADR-004).
3. **Sin valores `undef` ni `poison`.** Todo valor es un bitvector concreto. La parcialidad existe solo como precondición de operación con resultado `ub` inmediato, o como trap explícito en el código.
4. **Hechos de Core-O1: `nsw` y `nuw`.** Descartables según ADR-004.
5. **Traps como terminadores explícitos** con etiqueta y payload. Las etiquetas son observables; ningún pase las interpreta.
6. **Meta-modelo con regiones.** Una operación puede poseer regiones con tipo de región declarado. O1 implementa solo regiones CFG (cuerpos de función). Los pases razonan sobre operaciones mediante interfaces semánticas, no enumerando opcodes de otros dominios.
7. **Canonicalización por reescrituras locales deterministas** con argumento de terminación y sin pretensión de forma normal única. Equality saturation queda fuera del pipeline de O1; se permite como diagnóstico offline.
8. **Verificador ejecutable** tras cada pase en modos debug/test e **intérprete de referencia** de Core-O1 como oráculo de pases y backend.

## Alternativas consideradas

- **Nodos φ clásicos**: semánticamente equivalentes. Se prefieren argumentos de bloque por edición y verificación más simples; precedentes en MLIR, Cranelift y Swift SIL. Diferencia de ingeniería, no de semántica.
- **Sea of nodes**: ninguna transformación requerida por O1 demuestra beneficio decisivo, y el coste está documentado. V8 sustituyó en 2025 el sea of nodes de TurboFan por Turboshaft, un IR basado en CFG, citando cadenas de efecto/control difíciles de mantener, peor depuración, mayor tiempo de compilación y peor comportamiento de caché.
- **Regiones estructuradas como forma base**: el código máquina produce CFG irreducibles que exigirían reestructuración antes del join.
- **Direcciones tipadas por espacio (`addr<space>`)**, propuestas por el research: tras la descarga no portan semántica adicional, y añaden conversiones int↔addr cuya distribución difiere por origen, lo que introduce ruido representacional. Reabrible si la procedencia debe sobrevivir al join ([Q4](../roadmap/open-questions.md)).
- **Poison/undef al estilo LLVM**: habilita especulación sin descartar hechos, pero su historia muestra inconsistencias sutiles (Lee et al., PLDI 2017). O1 no tiene lecturas no inicializadas porque los perfiles las excluyen. `ub` inmediato con descarte de hechos al especular es más simple de validar con SMT e intérprete. Coste aceptado: LICM y if-conversion deben descartar hechos o probarlos al especular ([Q5](../roadmap/open-questions.md)).
- **E-graphs como representación base**: crecimiento no acotado; efectos y bucles difíciles.
- **Construir sobre MLIR** no es una alternativa de *representación*: Core-O1 podría implementarse como dialecto. Es una decisión de infraestructura, abierta junto al lenguaje de implementación ([Q1](../roadmap/open-questions.md)).

## Base

Research de consolidación §5, §8, §9. Hechos externos: documentación de MLIR (regiones, interfaces, conversión), LLVM (LangRef, manual de UB), Cranelift, V8 (“Land ahoy: leaving the Sea of Nodes”, 2025-03-25), Lee et al. 2017, egg (POPL 2021). **No existe evidencia observada de ONE.**

## Consecuencias

- La semántica de acceso a memoria es uniforme entre espacios: el acceso es una precondición. Los traps de acceso guest se expresan como comprobaciones explícitas en Core (SPEC-003), que quedan sujetas a optimización compartida y son una clase residual declarada (SPEC-001 §9).
- El backend debe soportar CFG irreducibles.
- Las reglas de canonicalización y los pases declaran transferencia de hechos y validez de especulación (SPEC-002 §9–§10).
- O1 no aporta evidencia sobre regiones no-CFG. Solo exige no impedirlas (SPEC-002 §12).

## Qué no decide

Sintaxis textual y serialización; implementación propia o sobre MLIR; nivel Machine; forma de ONE Core después de O1; vectores, flotantes, streams, concurrencia.

## Condiciones de revisión

- Una optimización requerida por O1 no puede implementarse sin poison, o el descarte de hechos al especular tiene un coste medido significativo en el corpus.
- La ausencia de tipo puntero impide un análisis de alias requerido por C-O1-3.
- EXP-02 requiere regiones no-CFG antes del join y el meta-modelo no las admite sin cambiar pases existentes.

## Relaciones

Complementado por [ADR-007](ADR-007-o1-implementation-foundation.md) (v0.3.0), que resuelve la infraestructura que este ADR dejaba abierta: Core-O1 se implementa como dialecto propio sobre MLIR. La representación decidida aquí no cambia. Las menciones a MLIR como alternativa abierta en “Alternativas consideradas” y “Qué no decide” reflejan el estado de v0.2.0.
