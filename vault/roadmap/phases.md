---
id: ROAD-002
kind: roadmap
status: provisional
---
# Fases provisionales

Estas fases sirven para conservar la dirección, no para prometer un roadmap rígido. Pueden recomponerse cuando la evidencia lo exija.

## O0 — Foundation

Vault, fuentes, hipótesis, invariantes y experimento inicial. **Estado: completo con v0.1.0.**

## O1 — Computational Core

C + RISC-V binary → ONE IR → optimizer → x86-64. Differential testing, fuzzing, cross-origin equivalence y primeras métricas de footprint/performance.

Objetivo: demostrar que existe un núcleo común real antes de ampliar la superficie.

## O2 — DSP stress

Introducir vectores, streams, FFT/filtering y scheduling suficiente para intentar romper la abstracción desde otro tipo de cómputo.

## O3 — Multi-backend

Añadir otro backend real y demostrar el efecto multiplicador frontend × backend.

## O4 — Numerics

Bit-precise/IEEE-754, arbitrary precision y kernels numéricos que sean usados por más de un dominio.

## O5 — Media

Codec/pipeline propio con benchmarking serio y reutilización del stack ONE.

## O6 — Dynamic/runtime surface

Lenguaje/runtime dinámico si aporta una prueba técnica relevante; no se añade por checklist.

## O7 — Neural/compression

Tensor/inference y compresión real como workload, con runtime propio suficiente.

## O8 — Radio/SDR

DSP + PHY/communications sobre hardware SDR real.

## O9 — Portability and browser

WASM/browser y/o hardware especializado X. Arranque de un sistema guest completo cuando la emulación esté madura.

## O10 — Integrated machine

Vertical de extremo a extremo con múltiples orígenes de cómputo y dos máquinas ONE comunicándose.

## O11 — Comparative campaign

Campaña comparativa final bajo criterios prefijados. Esta fase evalúa el criterio humano de victoria; no redefine el criterio.
