---
id: NAV-001
kind: navigation
status: accepted
version: 0.3.0
cutoff: 2026-09-14
---
# ONE — Vault fundacional

Este vault conserva la idea de **ONE** y la convierte en contratos, decisiones y experimentos falsables antes de que exista implementación. Su función es impedir que la idea dependa de un chat, que se pierdan distinciones importantes o que futuras iteraciones reescriban retrospectivamente qué queríamos construir o qué se ha demostrado.

ONE parte de una apuesta:

> Formas de cómputo provenientes de dominios diferentes pueden conservar su semántica específica mientras importa y después converger hacia infraestructura materialmente compartida de representación, análisis, optimización, codegen, ejecución, verificación y tooling, sin que cada artefacto pague por la generalidad que no usa.

ONE **no** afirma que video, radio, código fuente e instrucciones de CPU sean lo mismo. Intenta unificar el cómputo que opera sobre ellos en el punto donde esa unificación sea real, medible y útil.

## Lectura

**Fundamento**

1. [Constitución](constitution.md): qué es ONE, qué no es y qué no se debe perder.
2. [Origen y criterio técnico](evidence/origin.md).
3. [Gobierno](governance.md): estados epistemológicos, preregistro, excepciones, versionado.
4. [Registro de claims](claims.md): qué se intenta demostrar, qué no se afirma, estado de cada claim.

**Decisiones y arquitectura**

5. [Decisiones](decisions/README.md): ADR-001 a ADR-008.
6. [Arquitectura general](architecture/overview.md) · [Modelo computacional](architecture/computational-model.md) · [ONE IR](architecture/ir.md) · [Frontends y backends](architecture/frontends-backends.md) · [Modularidad](architecture/modularity-deployment.md).

**Contratos**

7. [SPEC-001 Semántica](spec/semantics.md): observación, relaciones, join, contratos de olvido.
8. [SPEC-002 Core-O1](spec/core-o1.md): operaciones, verificador, canonicalización, pases.
9. [SPEC-003 Perfiles O1](spec/o1-profiles.md): ONE-C-O1, RV64IM-O1, x86-64-O1.

**Validación y evidencia**

10. [Invariantes](validation/invariants.md) · [Métricas](validation/metrics.md) · [Protocolo O1](validation/o1-protocol.md) · [Mapa experimental](validation/experiments.md).
11. [Ledger de evidencia](evidence/ledger.md): vacío.

**Investigación y estado**

12. [Trabajo relacionado](research/related-work.md) · [Riesgos](research/risks.md) · [Fuentes](research/sources.md) · [Research de consolidación](research/ONE-Technical-Foundation-Consolidation-Research.md) y su [disposición](research/consolidation-disposition.md) · [Research de Q1](research/ONE-Q1-Implementation-Foundation-Decision.md) y su [disposición](research/q1-disposition.md) · [Caracterización de oráculos O1](research/o1-oracle-probes.md).
13. [Estado actual](roadmap/current-state.md) · [Fases](roadmap/phases.md) · [Preguntas abiertas](roadmap/open-questions.md) · [Glosario](glossary.md).

## Estados y precedencia

Los estados (`accepted`, `designed`, `hypothesis`, `open`, `provisional`, `research`, `observed`, `superseded`) se definen en [gobierno](governance.md).

Precedencia: propósito explícito → constitución → decisiones vigentes → contratos (`architecture/`, `spec/`, `validation/`) → planes → implementación. La evidencia puede obligar a cambiar una decisión; una decisión nunca justifica reinterpretar una medición.

## Estado actual

**No existe implementación de ONE ni evidencia observada.** Existen decisiones, contratos diseñados, una campaña O1 definida para intentar romper el join en el par de orígenes más cercano una implementation foundation decidida pero no implementada (ADR-007) y oráculos fijados (ADR-008). El estado `pre-código` está cerrado: el siguiente paso es el primer sprint de implementación de O1. Lo que falta antes de escribir código está en el [estado actual](roadmap/current-state.md).
