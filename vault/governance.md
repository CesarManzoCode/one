---
id: GOV-001
kind: governance
status: accepted
---
# Gobierno del conocimiento

## Objetivo

Que ONE no dependa de memoria de chats, que su significado no cambie según la conversación más reciente y que ninguna afirmación suba de estado epistemológico sin el mecanismo que lo autoriza.

## Estados epistemológicos

Este documento es la definición autoritativa de los estados. El resto del vault los usa sin redefinirlos.

| Estado | Significado | Se entra mediante | Se sale mediante |
|---|---|---|---|
| `accepted` | Vigente hasta que un documento posterior lo sustituya explícitamente. | ADR, o cambio versionado de constitución/gobierno/registros. | `superseded` por ADR nuevo. Nunca por reescritura silenciosa. |
| `designed` | Contrato o arquitectura que una implementación debe cumplir. Define qué sería correcto; no es evidencia de que funcione. | Documento suficientemente preciso para implementarse o falsarse. | Revisión versionada. Pasa a `accepted` solo si un ADR lo fija. |
| `hypothesis` | Afirmación empírica que debe sobrevivir experimentos. | Registro en [claims](claims.md) con falsador. | Estado de claim (`supported`, `refuted`, `inconclusive`) citado a entradas del [ledger](evidence/ledger.md). |
| `open` | Incertidumbre que no se rellena con una suposición cómoda. | [Preguntas abiertas](roadmap/open-questions.md) o riesgos. | Resolución enlazada: ADR, spec o evidencia. |
| `provisional` | Secuencia o intención revisable. | Roadmap. | Recomposición cuando la evidencia lo exija. |
| `research` | Hechos externos, inferencias y recomendaciones. No autoritativo. | `research/`. | Sus recomendaciones solo afectan a ONE mediante ADR o spec, con disposición registrada. |
| `observed` | Resultado de una ejecución identificable y reproducible. | Entrada del ledger. | Invalidación documentada por una entrada posterior; nunca borrado. |
| `superseded` | Histórico conservado. | ADR o versión que lo reemplaza. | — |

Los claims tienen su propio ciclo (`untested`, `supported`, `refuted`, `inconclusive`, `withdrawn`), definido en [claims](claims.md).

## Reglas

1. Las afirmaciones fundacionales viven en el vault. Los chats proponen; el vault vuelve durable. Una idea importante que no está en el vault es frágil.
2. Precedencia: propósito explícito → constitución → decisiones vigentes → contratos (`architecture/`, `spec/`, `validation/`) → planes → implementación. La evidencia puede obligar a cambiar una decisión; una decisión nunca justifica reinterpretar evidencia.
3. Una hipótesis no se promueve por repetición, por razonamiento ni por la calidad de un diseño. Solo por evidencia registrada bajo un protocolo citado.
4. Research no es arquitectura. Toda recomendación de un documento de research incorporada al vault tiene disposición registrada (aceptada, diseñada, limitada, modificada, rechazada o abierta) y enlace al artefacto que la incorpora. Ver [disposición de la consolidación](research/consolidation-disposition.md).
5. Una decisión reemplazada se conserva y se marca `superseded`. Un ADR vigente puede recibir una sección de relaciones (“refinado por”, “no ejercitado por”) sin alterar su decisión.
6. Evidencia negativa, inconclusa e inválida se registra con el mismo estándar que la positiva. `unknown`, timeout, `unsupported` y agotamiento de recursos nunca cuentan como éxito.
7. **Preregistro.** Antes de ejecutar una campaña comparativa se congelan, en un commit identificado: protocolo y versión, contratos semánticos citados, corpus con particiones (desarrollo, held-out, controles) y sus hashes, baselines con versiones y flags, métricas, umbrales, presupuestos y reglas de exclusión. Cada entrada del ledger cita ese commit.
8. Las varas fijadas para una campaña no se reducen cuando aparecen dificultades ni se inflan retrospectivamente. Enmendar un protocolo tras ver resultados crea una versión nueva; los resultados se reportan bajo el protocolo original y bajo el enmendado.
9. Una partición held-out usada en una ejecución queda “quemada” y pasa a desarrollo. Una nueva campaña confirmatoria necesita una partición nueva.
10. **Excepciones.** Toda excepción a un invariante (whitelist, caso especial, bypass, adapter que oculta un fallo) se registra con el invariante afectado, motivo y alcance. Un invariante con excepciones en una ruta de corrección está violado, no “casi cumplido”; la respuesta es la indicada en [riesgos](research/risks.md), normalmente rediseño.
11. Pares derivados, variantes de diagnóstico no fieles y ejecuciones fuera de protocolo nunca sostienen claims de titular. Se reportan en secciones separadas.
12. Un claim solo puede citarse fuera del vault con su estado del registro y su alcance.
13. Herramientas, incluida IA, se documentan cuando afectan reproducibilidad o independencia (por ejemplo, la autoría de pares independientes). No son una categoría moral distinta.
14. Material privado no se publica ni se resume en documentos públicos.

## Tipos de documento

| `kind` | Contiene | No contiene |
|---|---|---|
| `constitution` | Propósito y restricciones fundacionales. | Detalles de campaña o de implementación. |
| `decision` (ADR) | Una decisión con alternativas reales, base, consecuencias, qué no decide y condiciones de revisión. | Especificaciones extensas. |
| `spec` | Semántica precisa y versionada que una implementación debe cumplir. | Justificación extensa, resultados. |
| `architecture` | Estructura deseada y restricciones entre componentes. | Semántica de operaciones (va en spec). |
| `validation` | Protocolos, métricas, gates e invariantes. | Resultados. |
| `evidence` | Observaciones reproducibles y su esquema. | Conclusiones sin datos. |
| `registry` | Claims y su trazabilidad a decisiones, protocolos y evidencia. | Argumentación de diseño. |
| `research` | Investigación, prior art, riesgos. | Decisiones. |
| `roadmap` | Secuencia, estado y preguntas abiertas. | Criterios de éxito (viven en validation). |

Cada documento declara `id`, `kind` y `status` en frontmatter. Las specs y protocolos declaran además `version` del contrato.

## Versionado

- **Vault**: semver. Minor para cambios de decisiones, contratos o semántica; patch para correcciones editoriales. v0.1.0 fue la fundación; v0.2.0 es la consolidación técnica previa a O1; v0.3.0 incorpora la implementation foundation de O1 (ADR-007). Una 1.0 debe corresponder a una arquitectura implementada y defendible, no a documentación madura.
- **Contratos** (specs, protocolos): versión propia (`Core-O1 v0.1`). Un cambio semántico incrementa su versión. Toda evidencia cita la versión del vault y de cada contrato bajo el que se obtuvo.
