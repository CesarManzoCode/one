---
id: ARC-002
kind: architecture
status: designed
---
# Modelo computacional

## Qué es una forma de cómputo

Para ONE, una forma de cómputo proveniente de un dominio queda caracterizada por seis componentes:

1. **Estado** y configuración inicial.
2. **Transición**: cómo cambia el estado.
3. **Observables**: qué del comportamiento importa ([SPEC-001 §1–2](../spec/semantics.md)).
4. **Obligaciones**: qué ejecuciones carecen de significado o tienen un significado excepcional definido.
5. **Estructura**: organización que habilita optimización (bucles, dependencias de datos, tasas, formas tensor, planificación).
6. **Entorno**: ABI, EEI, dispositivos, reloj.

Dos formas de dominios distintos no son “la misma”. Lo compartible es la maquinaria que opera sobre transiciones una vez que las obligaciones (4) y el entorno (6) se han hecho explícitos, y la estructura (5) ya no hace falta o se ha traducido a interfaces semánticas. Ese punto es el join de [ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md). Cuanto más tarde está el join, más estructura sobrevive y menos maquinaria se comparte; cuanto antes, al revés. **La tesis de ONE es que existe un join útil entre esos extremos para dominios muy distintos.** Es hipótesis H1.

## El error de la equivalencia literal

ONE no intenta “transmitir video mediante instrucciones x86” ni convertir semánticamente radio en video. Una ISA describe operacionalmente una máquina; un video es información estructurada; una señal muestreada es una serie temporal. Sus significados permanecen distintos. La convergencia ocurre, si ocurre, en las transformaciones computables que operan sobre ellos.

## Universalidad computacional frente a utilidad

Cualquier cómputo puede reducirse a primitivas elementales. Eso prueba posibilidad, no utilidad. La pregunta de ONE es más fuerte: ¿puede una representación común conservar suficiente estructura para que compartir optimizaciones y backends sea útil y competitivo frente a toolchains especializados?

## Qué lleva cada dominio y dónde debe sobrevivir

Filas de C e ISA: diseñadas para O1 (SPEC-003). Resto de filas: inferencia de research (research de consolidación §18), sin diseño. Las clases I1–I6 son las de SPEC-001 §7.

| Dominio | Obligaciones (I1) | Estructura crítica (I3, I6) | Entorno (I5) | Lowering prematuro destruye | Estado |
|---|---|---|---|---|---|
| C (ONE-C-O1) | UB aritmético, de acceso y de lifetime; procedencia | Tipos, forma de bucles | ABI LP64 / System V | Alias basado en objetos si los punteros se vuelven enteros sin descarga | designed |
| ISA (RV64IM-O1) | Ninguna UB; traps definidos | CFG irreducible, estado arquitectónico | EEI, mapa de memoria, ABI no garantizado | Optimizabilidad, si el estado se copia como estructura de memoria | designed |
| DSP | Precisión, redondeo, saturación | Tasas, tokens, estado de retardo, planificación | Reloj de muestreo, latencia | Fusión, planificación estática y buffers acotados, si los streams se bajan a ring buffers con `load`/`store` | abierto |
| Media | Bit-exactness | Transforms regulares, entropy coding irregular, dependencias entre frames | Bitstream, latencia | Bit-exactness, o el core se llena de operaciones de codec | abierto |
| Tensor/ML | Tolerancia numérica, cuantización | Formas, layouts, planificación y tiling | Jerarquía de memoria de acelerador | Movimiento de datos y tiling, con bufferización temprana o rango fijo | abierto |
| Radio/SDR | Timing duro | Sincronización, FFT y bancos de filtros, FEC | Hardware de E/S | Información de tasa, si todo es CFG imperativo | abierto |

## Implicación arquitectónica

Operaciones como `fft`, `convolution`, `guest_load`, `vector_shuffle` o `entropy_decode` pueden existir como operaciones ricas antes del join. El join se declara por campaña y par de orígenes; no es un nivel global fijado de antemano. Core-O1 no contiene ninguna de esas operaciones, pero no puede impedirlas: restricciones E1–E7 de [SPEC-002 §12](../spec/core-o1.md).
