---
id: ARC-003
kind: architecture
status: hypothesis
---
# ONE IR

## Hipótesis central

Existe una familia de representaciones que permite a dominios heterogéneos converger gradualmente sin sacrificar semántica prematuramente y sin impedir una fase final común de optimización y codegen. El nombre **ONE IR** se conserva por simplicidad; el diseño esperado es multinivel ([ADR-002](../decisions/ADR-002-multilevel-ir.md)).

Nada de este documento está implementado. Solo Core-O1 está especificado ([ADR-005](../decisions/ADR-005-core-o1-representation.md), [SPEC-002](../spec/core-o1.md)), y su existencia no valida los demás estratos.

## Cuatro nociones separadas

Confundirlas produce IRs extensibles sin integración, o integración sin extensibilidad.

| Noción | Pregunta | Instancia O1 |
|---|---|---|
| **Meta-modelo contenedor** | Qué es una operación, valor, bloque, región, tipo, atributo, procedencia. | SPEC-002 §2 |
| **Interfaces semánticas** | Cómo razona un pase sobre operaciones que no conoce: pureza, efectos, parcialidad, conmutatividad, terminadores. | SPEC-002 §7 |
| **Relación de legalidad** | Qué es legal en cada etapa y cómo se descarga lo ilegal. Un nivel es un conjunto de legalidad más las obligaciones ya descargadas, no un nombre. | `J_O1` = legalidad de SPEC-002 |
| **Canonicalidad** | Qué normalizaciones terminantes reducen varianza en cada etapa. No existe forma normal única global. | SPEC-002 §9 |

## Estratos tentativos

Hipótesis; nombres y fronteras provisionales.

- **Domain IRs**: intención rica del dominio (instrucciones guest, operaciones tensor, filtros, codecs, streams). Obligaciones del origen aún implícitas o parcialmente descargadas.
- **ONE High**: patrones compartibles de alto nivel (regiones, loops, dataflow, streams, vectores, tensores, espacios de memoria, efectos, restricciones de planificación). Estructura preservada, obligaciones descargadas.
- **ONE Core**: cómputo general con análisis común. Todo explícito salvo la estructura que ya no se necesita. Core-O1 es su primera instancia y la más baja posible.
- **ONE Machine**: legalización, clases de registro, convenciones de llamada, selección de instrucciones, restricciones del target. En O1 es interno al backend y no forma parte de claims.

Si un join puede existir en ONE High para algunos pares de dominios, o solo en ONE Core, es algo que O1 no puede responder; EXP-02 empieza a hacerlo.

## Propiedades exigidas

| Propiedad | Estado en O1 |
|---|---|
| Semántica formal de las operaciones fundamentales | `QF_BV` por operación (SPEC-002 §5) |
| Efectos explícitos por recursos nombrados | SPEC-002 §7; E4 |
| Alias y efectos de memoria cuando se conocen | Espacios disjuntos, frescura de slots, resúmenes |
| Vectores y tipos bit-precise | Bit-precise sí; vectores diferidos con E2 |
| Estado arquitectónico guest | Escalarizado en SSA (SPEC-003 §2.6) |
| Streams y dataflow sin convertirse de inmediato en memoria imperativa | Diferido; E1, E5, E7 |
| Lowering verificable | Relación y contrato de olvido por arista (SPEC-001) |
| Forma textual para depuración y formato in-memory eficiente | Requeridos; sintaxis sin decidir |
| Serialización estable | Solo ante necesidad real ([Q23](../roadmap/open-questions.md)) |
| Extensibilidad sin cascadas `if dialect == …` | Interfaces más origin-blindness (INV-13) |

## Convergencia entre orígenes

La definición está en [ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md), la medición en [VAL-003 §3](../validation/metrics.md) y la campaña O1 en [VAL-004](../validation/o1-protocol.md). No se exige identidad textual. Convergencia no es equivalencia, y ninguna de las dos implica reutilización.

## Criterios de fracaso

El diseño del IR se cuestiona, en vez de esconder el problema detrás de adapters, cuando:

- un dominio necesita bypasses masivos;
- aparecen operaciones opacas que el optimizador no entiende;
- hacen falta pipelines separados;
- los pases enumeran dialectos en lugar de usar interfaces.

Firmas y respuestas obligatorias: [riesgos](../research/risks.md) R1, R3, R12–R14; gates G2–G4 de VAL-004.
