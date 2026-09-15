---
id: ADR-001
kind: decision
status: accepted
---
# ADR-001 — Un proyecto, un núcleo

## Decisión

ONE será un único sistema coherente. Compilación, DBT/emulación, DSP/media, ML y radio pueden tener módulos y representaciones específicas, pero deben compartir una arquitectura central suficiente para que la reutilización sea medible.

## Motivo

La tesis no se satisface acumulando subsistemas independientes. El reto técnico es demostrar que una abstracción propia puede atravesar varios dominios y producir reutilización material.

## Consecuencia

Un subsistema que no comparte infraestructura material debe justificar por qué pertenece a ONE y qué presión arquitectónica útil ejerce sobre el núcleo.

## Relaciones

Refinado por [ADR-004](ADR-004-semantic-discharge-convergence.md), que define join, origin-blindness y reutilización material (T0/T1/T2, M1–M4). Evaluado por C-O1-1, C-O1-3 y C-O1-5 ([claims](../claims.md)).
