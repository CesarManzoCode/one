---
id: ARC-003
kind: architecture
status: hypothesis
---
# ONE IR

## Hipótesis central

Debe existir una familia de representaciones intermedias que permita a dominios heterogéneos converger gradualmente sin sacrificar prematuramente semántica ni impedir una fase final común de optimización/codegen.

El nombre **ONE IR** se conserva por simplicidad, pero el diseño esperado es multinivel.

## Estratos tentativos

### Domain IRs
Representan intención rica del dominio: instrucciones guest, operaciones tensoriales, filtros, codecs, streams, etc.

### ONE High
Representa patrones computacionales compartibles de alto nivel: regiones, loops, dataflow, streams, vectores, tensors, memory spaces, effects y scheduling constraints.

### ONE Core
Representa cómputo general suficientemente explícito para análisis común: SSA o modelo equivalente, control flow, memory, arithmetic, vectors, state/effects y calls.

### ONE Machine
Representación cercana a backend: legalización, register classes, calling conventions, instruction selection y machine-specific constraints.

Los nombres y fronteras son provisionales.

## Propiedades deseadas

- semántica formalizable de las operaciones fundamentales;
- representación explícita de efectos;
- control de aliasing/memory effects cuando sea conocido;
- soporte de vectores y tipos bit-precise;
- posibilidad de representar estado arquitectónico de una ISA guest;
- posibilidad de conservar streams/dataflow sin convertirlos inmediatamente en memoria imperativa;
- lowering verificable;
- textual form para debugging;
- formato in-memory eficiente;
- serialización estable solo cuando exista una necesidad real;
- extensibilidad sin convertir cada optimización en una cascada de `if dialect == ...`.

## Cross-origin equivalence

Una prueba especial de ONE será tomar funciones semánticamente equivalentes provenientes de orígenes distintos y observar cuánto convergen después de canonicalización.

Ejemplo inicial:

```text
C function ───────────┐
                      ├──> ONE Core canonical form ──> x86-64
RISC-V binary ────────┘
```

No se exige que la representación textual sea byte-for-byte idéntica. Sí se busca que optimizaciones comunes puedan reconocer la misma estructura y producir resultados equivalentes o materialmente compartidos.

## Criterio de fracaso

Si cada dominio necesita bypasses masivos, operaciones opaque que el optimizer no entiende o pipelines completamente separados, hay que cuestionar el diseño del IR en vez de esconder el problema detrás de adapters.
