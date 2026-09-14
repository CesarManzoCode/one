---
id: ARC-002
kind: architecture
status: designed
---
# Modelo computacional

## La intuición

Video, radio y código no son equivalentes.

Sin embargo, el **trabajo** que hacen sus implementaciones puede descomponerse en familias comunes de operaciones: aritmética, memoria, control, vectores, streams, estado, sincronización, transformaciones numéricas y efectos.

Ejemplo conceptual:

```text
video decoder
  prediction + transform + memory + entropy + vector math

radio receiver
  filter + FFT + complex math + FEC + streams

RISC-V program
  arithmetic + memory + branches + architectural state

C program
  arithmetic + memory + calls + control
```

ONE intenta representar esas estructuras de forma que las partes realmente comunes puedan compartir infraestructura.

## El error de la equivalencia literal

ONE no intenta “transmitir video mediante instrucciones x86” ni convertir semánticamente radio en video. Una ISA es una descripción operacional de una máquina; un video es información estructurada; una señal muestreada es una serie temporal. Sus significados permanecen distintos.

La convergencia ocurre cuando expresamos **las transformaciones computables que operan sobre ellos**.

## El alfabeto y las obras

Una analogía útil: novela, contrato y ecuación pueden usar el mismo alfabeto sin ser equivalentes. ONE intenta construir un alfabeto computacional compartido, pero debe conservar estructuras superiores cuando importen.

## Universalidad computacional vs utilidad

En principio, cualquier cómputo computable podría reducirse a primitivas extremadamente básicas. Eso prueba posibilidad, no utilidad.

La pregunta de ONE es más fuerte:

> ¿Puede una representación común conservar suficiente estructura para que compartir optimizaciones y backends sea útil y competitivo frente a toolchains especializados?

## Implicación arquitectónica

Por eso ONE debe aceptar representaciones de diferentes niveles. Una operación como `fft`, `convolution`, `guest_load`, `vector_shuffle` o `entropy_decode` puede existir temporalmente como una operación rica antes de lowering. Forzarla demasiado pronto a escalares podría destruir oportunidades de optimización.
