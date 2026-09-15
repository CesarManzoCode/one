---
id: ADR-NAV-001
kind: decisions
status: accepted
---
# Registro de decisiones

Un ADR registra una decisión con alternativas reales y consecuencias arquitectónicas. No se escribe un ADR por detalle: la semántica precisa vive en `spec/`, los criterios de éxito en `validation/`.

Cambiar una decisión exige un ADR nuevo que la sustituya; el anterior se marca `superseded`. No se reescribe el pasado para aparentar que siempre supimos la respuesta. Un ADR vigente puede recibir una sección **Relaciones** sin alterar su decisión.

## Estructura

1. **Contexto**: qué problema obliga a decidir.
2. **Decisión**, con su alcance (global, O1, contrato concreto).
3. **Alternativas consideradas** y por qué se rechazan.
4. **Base**: razonamiento y hechos externos, separados. Si no hay evidencia observada de ONE, se dice.
5. **Consecuencias**.
6. **Qué no decide**.
7. **Condiciones de revisión**: qué observación obliga a reabrirla.

## Índice

| ADR | Decisión | Estado | Alcance |
|---|---|---|---|
| [ADR-001](ADR-001-one-core.md) | Un proyecto, un núcleo | accepted | global; refinado por ADR-004 |
| [ADR-002](ADR-002-multilevel-ir.md) | Representación multinivel | accepted | global; no ejercitado por O1 |
| [ADR-003](ADR-003-modular-universality.md) | Universalidad modular | accepted | global |
| [ADR-004](ADR-004-semantic-discharge-convergence.md) | Convergencia por descarga semántica y mecanismos origin-blind | accepted | global |
| [ADR-005](ADR-005-core-o1-representation.md) | Representación ejecutable de Core-O1 | accepted | Core-O1 (O1) |
| [ADR-006](ADR-006-o1-falsification-campaign.md) | O1 como campaña de falsificación acotada | accepted | O1 |
