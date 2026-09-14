---
id: VAL-002
kind: validation
status: designed
---
# Plan experimental inicial

## EXP-01 — C y RISC-V convergen

Construir dos entradas genuinamente distintas:

```text
C source ───────────→ C frontend ──────┐
                                       ↓
                                    ONE IR → optimizer → x86-64
                                       ↑
RISC-V binary ─────→ RV decoder ───────┘
```

Ambos deben soportar pequeños programas reales con memoria, control flow, functions/calls e integer arithmetic.

### Éxito

- los dos caminos usan el mismo optimizer y x86 backend;
- al menos varias optimizaciones son exactamente las mismas, no duplicadas;
- differential execution contra referencias pasa;
- pares semánticamente equivalentes convergen materialmente después de canonicalización;
- el coste de la abstracción queda medido.

### Fracaso útil

Si RISC-V exige una ruta especial que no puede expresar correctamente su estado o C pierde demasiada información, se revisa el modelo antes de añadir dominios.

## EXP-02 — Tercer dominio que estire el modelo: DSP

Después de EXP-01, introducir un pipeline DSP con vectores/streams/FFT/filtering.

Objetivo: descubrir qué abstractions faltan cuando el cómputo deja de parecerse a código escalar convencional.

Debe demostrar al menos una optimización compartida con C o DBT y una optimización rica que se preserve hasta el lowering adecuado.

## EXP-03 — Backend nuevo

Añadir AArch64, RISC-V o WASM como segundo backend real.

Medir cuánto código de frontends/optimizer permanece intacto y cuánto trabajo específico exige cada dominio.

## EXP-04 — Runtime specialization

Construir un artefacto `full` y al menos dos runtimes especializados. Medir tamaño, startup, RSS y dependencias. Verificar que agregar capacidades al repo no infla automáticamente los artefactos mínimos.

## EXP-05 — Cross-domain optimization

Seleccionar una optimización con impacto medible en al menos dos dominios distintos. La evidencia debe mostrar que una implementación compartida produjo ambas mejoras.

## EXP-06 — Media

Introducir un codec o pipeline multimedia propio suficiente para tensionar transforms, entropy, SIMD, streaming y memory layout.

No cuenta solo “decodifica”. Debe existir comparación cuantitativa en quality/bitrate/latency/complexity según el artefacto elegido.

## EXP-07 — Numerics

Añadir SoftFloat/precisión arbitraria o un núcleo numérico propio que pueda usarse por emulación y otros dominios. Differential testing contra referencias maduras.

## EXP-08 — Neural/compression

Introducir tensor/inference y una aplicación real, preferentemente compression, donde el runtime ONE ejecute el cómputo sin depender de PyTorch en producción.

## EXP-09 — Radio/SDR físico

Procesar una cadena real con SDR: samples → sync/filter/FFT/modulation/FEC → transmisión/recepción. Hardware físico en la frontera; cómputo digital dentro de ONE.

## EXP-10 — Vertical integrada

Dos máquinas ONE transmiten media por una cadena definida por software; parte del cómputo puede originarse en código compilado y otra en binarios traducidos, compartiendo optimizer/runtime/backend.

## EXP-11 — Cross-domain comparative campaign

Solo cuando la superficie exista. Comparar honestamente contra sistemas maduros equivalentes en compiler/runtime, emulation/DBT, numerics, media/compression y radio según equivalencia real.

La campaña debe fijar métricas y clases de equivalencia antes de ejecutar para evitar mover la vara después de ver resultados.
