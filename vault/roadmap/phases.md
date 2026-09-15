---
id: ROAD-002
kind: roadmap
status: provisional
---
# Fases provisionales

Estas fases conservan la dirección; no son un roadmap rígido y se recomponen cuando la evidencia lo exija. Los criterios de éxito de cada fase viven en `validation/`, no aquí.

## O0 — Foundation

**Completo.** v0.1.0: idea, hipótesis, invariantes. v0.2.0: consolidación técnica (semántica, Core-O1, perfiles, protocolo, métricas, claims, ledger). v0.3.0: cierre pre-código (ADR-007, ADR-008, SPEC-003 v0.2), sin implementación.

## O1 — Computational Core

**Objetivo**: intentar romper el join en el par de orígenes más cercano (ONE-C-O1 y RV64IM-O1 hacia x86-64) antes de ampliar superficie ([ADR-006](../decisions/ADR-006-o1-falsification-campaign.md)). No demuestra la tesis global.

Orden previsto. Cada componente tiene oráculo antes de existir su consumidor:

1. **Aparato** (siguiente; su primer sprint está descrito en el [estado actual](current-state.md)): verificador e intérprete de referencia de Core-O1; harness de contratos; integración de oráculos; contratos `K` iniciales y held-out sellada.
2. **Rutas de entrada**: frontend ONE-C-O1 y lifter RV64IM-O1 hasta legalidad en el join y corrección por origen.
3. **Mecanismos compartidos**: canonicalización y los cuatro pases fuertes con sus negativos.
4. **Backend** x86-64-O1 y runtime de frontera.
5. **Campaña**: preregistro, ejecución held-out, composición rival, entradas de ledger.

Cierre y consecuencias: [VAL-004 §13](../validation/o1-protocol.md).

## O2 — DSP stress

Primer dominio adversarial: vectores, streams, FFT, filtering y scheduling suficientes para intentar romper Core-O1 y ADR-004. Propósito y firmas de fallo en EXP-02. Sin diseñar hasta cerrar O1.

## O3 — Multi-backend

Segundo backend real; primera medición de H3 (EXP-03).

## O4 — Numerics

Bit-precise e IEEE-754, precisión arbitraria y kernels numéricos usados por más de un dominio.

## O5 — Media

Codec o pipeline propio con benchmarking serio y reutilización del stack ONE.

## O6 — Dynamic/runtime surface

Lenguaje o runtime dinámico solo si aporta una prueba técnica relevante.

## O7 — Neural/compression

Inferencia y compresión real como workload, con runtime propio suficiente.

## O8 — Radio/SDR

DSP + PHY/communications sobre hardware SDR real.

## O9 — Portability and browser

WASM/browser y/o hardware especializado X. Arranque de un sistema guest completo cuando la emulación esté madura y aporte información ([Q22](open-questions.md)).

## O10 — Integrated machine

Vertical de extremo a extremo con múltiples orígenes y dos máquinas ONE comunicándose.

## O11 — Comparative campaign

Campaña comparativa final frente a la composición de sistemas maduros, bajo criterios preregistrados. Evalúa; no redefine el criterio.
