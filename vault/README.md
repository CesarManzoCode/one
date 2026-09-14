---
id: NAV-001
kind: navigation
status: accepted
version: 0.1.0
cutoff: 2026-09-14
---
# ONE — Vault fundacional

Este vault conserva la idea completa de **ONE** en su estado fundacional. No pretende congelar una implementación prematuramente. Su función es impedir que la idea dependa de un chat, que se pierdan distinciones importantes o que futuras iteraciones reescriban retrospectivamente qué queríamos construir.

ONE parte de una apuesta simple y extrema:

> Muchos dominios de software que hoy viven en toolchains separados pueden conservar sus semánticas específicas en niveles altos y, aun así, converger hacia un núcleo computacional común capaz de compartir análisis, optimización, ejecución, tooling y backends sin pagar proporcionalmente por la generalidad.

La idea **no** es afirmar que video, radio, código fuente e instrucciones de CPU sean la misma cosa. Son objetos distintos con semánticas distintas. ONE intenta unificar **el cómputo que opera sobre ellos** en el nivel donde esa unificación sea real y útil.

## Lectura inicial

1. [Constitución](constitution.md): qué es ONE, qué no es y qué no se debe perder.
2. [Origen y criterio técnico](evidence/origin.md): por qué existe el proyecto y qué debe demostrar.
3. [Arquitectura general](architecture/overview.md): visión de extremo a extremo.
4. [Modelo computacional](architecture/computational-model.md): qué significa realmente “tratar cosas distintas con primitivas comunes”.
5. [ONE IR](architecture/ir.md): hipótesis central de representación multinivel.
6. [Frontends y backends](architecture/frontends-backends.md): cómo entran y salen los dominios.
7. [Modularidad y despliegue](architecture/modularity-deployment.md): cómo evitar que universal signifique pesado.
8. [Hipótesis](research/hypotheses.md): qué debe ser demostrado y qué puede fallar.
9. [Trabajo relacionado](research/related-work.md): QEMU/TCG, MLIR y prior art relevante.
10. [Invariantes](validation/invariants.md): propiedades que futuras implementaciones no pueden erosionar silenciosamente.
11. [Experimentos](validation/experiments.md): cómo se falsará la idea.
12. [Estado](roadmap/current-state.md), [fases](roadmap/phases.md) y [preguntas abiertas](roadmap/open-questions.md).

## Estados epistemológicos

- **Aceptado**: decisión fundacional vigente hasta que una decisión posterior la reemplace explícitamente.
- **Hipótesis**: afirmación que debe sobrevivir experimentos.
- **Diseñado**: contrato o arquitectura deseada, no evidencia de que ya funcione.
- **Observado**: hecho obtenido de una ejecución o medición identificable.
- **Abierto**: incertidumbre que no debe rellenarse con una suposición cómoda.

## Regla de precedencia

Propósito explícito → constitución → decisiones vigentes → contratos de arquitectura → planes → implementación.

La evidencia siempre puede obligar a cambiar una decisión. Una decisión nunca puede obligar a reinterpretar una medición para que “encaje”.

## Estado actual

**No existe implementación de ONE.** Existe una hipótesis, una arquitectura inicial y una ruta de falsificación. La siguiente acción técnica es O1: construir el primer vertical mínimo que pruebe o rompa el núcleo común.
