---
id: ARC-001
kind: architecture
status: designed
---
# Arquitectura general

## Visión de largo plazo

Esta es una intención, no un diseño. ONE es una plataforma donde orígenes de cómputo distintos conservan inicialmente su semántica y después convergen hacia infraestructura compartida.

```text
C / lenguaje propio ───────┐
JavaScript ────────────────┤
x86 / RISC-V binaries ─────┤
DSP / radio ───────────────┤
media codecs ──────────────┤
tensor / ML ───────────────┤
                           ↓
                representaciones de dominio
                           ↓
                 ONE multi-level IR
                           ↓
                    ONE optimizer
                           ↓
                  ONE Core / runtime
                           ↓
      x86-64 / AArch64 / RISC-V / WASM / X
```

La lista de dominios es ambición, no scope.

## Estructura de convergencia

Toda ruta de ONE tiene la misma forma. Cada flecha declara una relación semántica ([SPEC-001](../spec/semantics.md)).

```text
origen ──frontend──▶ descarga semántica ──▶ JOIN ──▶ mecanismos origin-blind ──▶ backend ──▶ target
        (perfil)     (contrato de olvido)   (contrato   (canonicalización,         (legalización,   + runtime
                                             del core)   análisis, optimización,    selección,       por closure
                                                         verificación)              emisión)
```

- **Antes del join**, cada origen es libre y específico: puede conservar semántica rica todo lo que la necesite ([ADR-002](../decisions/ADR-002-multilevel-ir.md)).
- **En el join**, toda obligación es explícita y la semántica no depende del origen ([ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md)).
- **Después del join**, cada mecanismo existe una vez, no consulta el origen y es la única fuente de crédito de integración (T1/T2).
- **Cada artefacto** contiene solo su capability closure ([ADR-003](../decisions/ADR-003-modular-universality.md), [ARC-005](modularity-deployment.md)).

## Estado de cada parte

| Parte | Estado | Documento |
|---|---|---|
| Visión multi-dominio y demo integrada | intención | este documento |
| Criterio de convergencia y reutilización | accepted | ADR-004 |
| Niveles Domain / High / Core / Machine | hypothesis | [ARC-003](ir.md) |
| Core-O1 | designed | [SPEC-002](../spec/core-o1.md) |
| Perfiles C, RV64IM, x86-64 de O1 | designed | [SPEC-003](../spec/o1-profiles.md) |
| Grafo de capabilities | designed | ARC-005 |
| Implementación | no existe | [estado](../roadmap/current-state.md) |

## Instancia O1

```text
fuente ONE-C-O1 ──▶ frontend C ─────┐
                                    ▼
                                  J_O1 (Core-O1) ──▶ canonicalización ──▶ SCCP · GVN/CSE · memoria · LICM ──▶ backend x86-64-O1 ──▶ ELF64 ET_REL + runtime
                                    ▲
imagen RV64IM-O1 ──▶ lifter RV ─────┘
```

O1 no ejercita representaciones previas al join ni progressive lowering: los frontends descargan directamente al join ([ADR-006](../decisions/ADR-006-o1-falsification-campaign.md)).

## Demo de extremo a extremo imaginada

Intención de largo plazo, sin diseño. Una demostración suficientemente fuerte podría tener dos máquinas ONE:

1. una recibe video y audio;
2. los procesa y comprime con codecs propios;
3. usa el mismo stack para DSP y ML cuando corresponde;
4. modula y transmite mediante SDR real;
5. la otra recibe, demodula, corrige errores, decodifica y reproduce;
6. parte del software proviene de C y parte de binarios de otra ISA;
7. todo comparte la misma familia de IRs, optimizador, runtime y backends;
8. una variante se ejecuta en navegador mediante WASM;
9. una ruta de emulación arranca Linux.

La demo no es el producto. Es una prueba visible de integración vertical, y solo cuenta si cada parte pasa los gates de integración (EXP-10).

## Superficies previstas

- **Compilation/languages**: frontends, IR, optimización, codegen, linking y eventualmente self-hosting.
- **DBT/emulation**: decodificación, estado de CPU, MMU, excepciones, traducción dinámica, invalidación, sistemas completos.
- **Numerics**: IEEE-754, precisión arbitraria, FFT/NTT, SIMD y primitivas que varios dominios necesitan.
- **Media**: imagen, audio, video, transforms, prediction, entropy coding, streaming.
- **Neural**: tensores, inferencia, cuantización, con ML como parte del sistema y no como runtime externo opaco.
- **Radio/SDR**: DSP, sincronización, FFT/OFDM, FEC, modulación, estimación de canal, protocolos.
- **Tooling común**: profiler, debugger, tracing, fuzzing, verificación y observabilidad sobre representaciones comunes.

## Lo que no debe pasar

La tabla de firmas y respuestas obligatorias está en [riesgos](../research/risks.md). ONE no puede convertirse en:

- una colección de wrappers sobre sistemas existentes (INV-09);
- varios runtimes sin relación real (R5);
- un IR tan bajo que la semántica útil desaparece (R1, R2);
- un IR tan alto que cada backend reimplementa todo (INV-03);
- un sistema universal que obliga a desplegarlo todo (R4);
- una suite diseñada para ganar solo donde ONE ya es fuerte (R6).
