---
id: ARC-001
kind: architecture
status: designed
---
# Arquitectura general

## Visión

ONE es una plataforma donde diferentes orígenes de cómputo conservan inicialmente sus semánticas y después convergen gradualmente hacia infraestructura compartida.

```text
C / lenguaje propio ───────┐
JavaScript ────────────────┤
x86 / RISC-V binaries ────┤
DSP / radio ───────────────┤
media codecs ──────────────┤
tensor / ML ───────────────┤
                           ↓
                representaciones específicas
                           ↓
                 ONE multi-level IR
                           ↓
                    ONE optimizer
                           ↓
                    ONE Core / runtime
                           ↓
      x86-64 / AArch64 / RISC-V / WASM / X
```

La lista de dominios es una ambición de largo plazo, no el scope de la primera implementación.

## Demo de extremo a extremo imaginada

Una demostración final suficientemente fuerte podría tener dos máquinas ONE:

1. una recibe video/audio;
2. procesa y comprime mediante codecs propios;
3. usa el mismo stack de cómputo para DSP/ML cuando corresponda;
4. modula y transmite mediante SDR real;
5. la otra recibe, demodula, corrige errores, decodifica y reproduce;
6. parte del software puede provenir de C y parte de binarios de otra ISA traducidos dinámicamente;
7. el sistema utiliza el mismo family of IRs, optimizer, runtime y backends;
8. una variante puede ejecutarse en navegador mediante WASM;
9. una ruta de emulación puede arrancar Linux.

La demo no es el producto. Es una prueba visible de integración vertical.

## Superficies previstas

### Compilation/languages
Frontends de lenguaje, IR, optimización, codegen, linking y eventualmente self-hosting.

### DBT/emulation
Decodificación de ISAs, estado de CPU, MMU, excepciones, traducción dinámica, invalidación y ejecución de sistemas completos.

### Numerics
IEEE-754, enteros/floats de precisión arbitraria, FFT/NTT, SIMD y otras primitivas que múltiples dominios necesitan de verdad.

### Media
Imagen, audio, video, transforms, prediction, entropy coding, streaming y SIMD.

### Neural
Tensores, inferencia, cuantización y aplicaciones donde el ML sea parte del sistema y no un runtime externo opaco.

### Radio/SDR
DSP, sincronización, FFT/OFDM, FEC, modulación, channel estimation y protocolos necesarios para una vertical real.

### Tooling común
Profiler, debugger, tracing, fuzzing, verification y observabilidad sobre una representación común.

## Lo que no debe pasar

ONE no puede convertirse en:

- una colección de wrappers sobre sistemas existentes;
- cinco runtimes sin relación real;
- un IR tan bajo que toda semántica útil desaparezca;
- un IR tan alto que cada backend necesite reimplementar todo;
- un sistema universal que obliga a desplegar todo;
- un benchmark suite diseñado para ganar solo donde ONE ya es fuerte.
