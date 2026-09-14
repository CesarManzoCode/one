---
id: RES-004
kind: risks
status: open
---
# Riesgos principales

## R1 — Abstracción artificial

Todo puede reducirse a cómputo general, pero esa reducción puede ser inútil para optimización. El proyecto podría “unificar” formalmente sin producir beneficio real.

## R2 — Pérdida semántica temprana

Bajar demasiado pronto a un IR genérico puede destruir patrones de dominio difíciles de reconstruir.

## R3 — Dialect explosion

Intentar conservar semántica puede producir tantos dialectos/especial cases que el núcleo común deje de ser realmente común.

## R4 — Universal tax

La arquitectura puede imponer costes de startup, memory, indirection o compile time a workloads que toolchains especializados resuelven de forma más directa.

## R5 — Frankenstein monorepo

El repositorio puede crecer en superficie sin crecer en integración real. Este es un fracaso aunque todos los subsistemas funcionen.

## R6 — Benchmark gaming

La amplitud del proyecto facilita elegir microbenchmarks favorables. Deben fijarse clases de comparación antes de medir, preservar workloads desfavorables y publicar límites.

## R7 — Reinventar prior art

MLIR, TCG, compiler infrastructures, DSP compilers y tensor compilers ya cubren porciones importantes. La novedad debe demostrarse, no asumirse porque la implementación sea propia.

## R8 — Complejidad incontrolable

El proyecto es cualitativamente más difícil que proyectos previos porque combina familias técnicas distintas. El vault debe proteger contra scope accidental sin reducir la ambición final.

## R9 — Matemática/algoritmos como cuello de botella

Media, radio, numerics y compression exigen más que architecture/software plumbing. ONE necesita resultados algorítmicos reales, no wrappers sobre bibliotecas externas.

## R10 — Utilidad no emergente

ONE puede ser técnicamente extraordinario y aun así no ofrecer una ventaja práctica. La utilidad es deseable pero no el criterio primario de decisión; aun así debe medirse honestamente.
