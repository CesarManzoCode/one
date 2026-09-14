---
id: ARC-004
kind: architecture
status: designed
---
# Frontends y backends

## Frontends

Un frontend no existe para “traducir sintaxis”. Debe capturar la semántica necesaria para que ONE pueda preservar y optimizar correctamente el origen.

Superficie prevista:

- C / lenguaje systems propio;
- JavaScript u otro runtime dinámico, si demuestra valor;
- RISC-V;
- x86-64;
- DSP graphs / radio;
- media;
- tensor/ML.

No todos serán implementados al principio.

## Backends

Un backend convierte ONE a una plataforma real.

Primeros candidatos:

- x86-64;
- AArch64;
- RISC-V;
- WebAssembly.

Después pueden aparecer GPU, FPGA, aceleradores, extensiones ISA o un X nuevo.

## La promesa de X

La utilidad industrial más fuerte de ONE aparecería si un backend nuevo habilita una superficie grande del ecosistema sin reescribir toolchains independientes para cada dominio.

La afirmación que debe comprobarse es:

> “Añadir X una vez beneficia materialmente múltiples familias de cómputo.”

No basta con que todo compile a X si cada frontend necesita un camino especial que duplica la mayor parte del trabajo.

## Oráculos y rivales

GCC/Clang, QEMU, FFmpeg, runtimes de ML, bibliotecas DSP y demás pueden usarse para differential testing y benchmarks. No cuentan como backend ONE si hacen el trabajo central que ONE pretende demostrar.
