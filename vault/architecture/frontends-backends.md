---
id: ARC-004
kind: architecture
status: designed
---
# Frontends y backends

## Contrato de frontend

Un frontend no traduce sintaxis: captura la semántica necesaria para preservar y optimizar correctamente su origen.

1. **Relación total.** Refina, o reproduce exactamente si el origen es determinista, la semántica completa de su origen para todas las entradas, no solo las de un contrato experimental ([ADR-004 §5](../decisions/ADR-004-semantic-discharge-convergence.md)).
2. **Disciplina de salida.** Cada construcción se acepta, se rechaza con diagnóstico, se preserva como trap definido o se declara `unsupported`. Nunca se aproxima en silencio ([SPEC-003](../spec/o1-profiles.md)).
3. **Descarga y olvido.** Publica su contrato de olvido ([SPEC-001 §7](../spec/semantics.md)).
4. **Legalidad.** Su salida pasa el verificador del join.
5. **Sin origen en la semántica.** Toda información de origen que sobrevive vive en el espacio borrable de procedencia.
6. **Análisis propios declarados.** Si hace un análisis que duplica un mecanismo del core (constantes, estrechamiento de estado), lo declara y se cuenta como coste marginal del origen (VAL-003 R7), no como reutilización.

## Contrato de backend

1. **Refinamiento** del core bajo un binding de ABI declarado.
2. **Sin reglas condicionadas por origen** en legalización, selección, emisión ni runtime (G4).
3. **Salida determinista** para igual entrada y configuración.
4. **Servicios de frontera enumerados**; no hay helpers computacionales.
5. **Libertad ante `ub`**: donde el core alcanza `ub`, cualquier comportamiento es válido.
6. **Oráculo propio**: diferencial frente al intérprete de referencia del core, que no comparte implementación semántica con el backend.

## Superficie prevista

Intención, no scope.

- **Frontends**: C / lenguaje systems propio; JavaScript u otro runtime dinámico si demuestra valor; RISC-V; x86-64; grafos DSP y radio; media; tensor/ML.
- **Backends**: x86-64 (O1), AArch64, RISC-V, WebAssembly; después GPU, FPGA, aceleradores, extensiones de ISA o un X nuevo.

## La promesa de X

La utilidad industrial más fuerte de ONE aparecería si un backend nuevo habilitara una superficie grande sin reescribir toolchains por dominio.

> “Añadir X una vez beneficia materialmente a múltiples familias de cómputo.”

Es H3. Se mide en EXP-03 como trabajo origin-specific dentro del backend nuevo, que debería ser ≈ 0, y como componentes de frontends y core que permanecen intactos. No basta con que todo compile a X si cada frontend necesita un camino especial.

## Oráculos, rivales y composición

- **Oráculos** (GCC, Clang, Sail, Spike, QEMU y bibliotecas maduras) se usan para testing diferencial y validación. Nunca realizan la propiedad central que ONE pretende demostrar (INV-09).
- **Rivales** se comparan con garantías equivalentes o con la diferencia etiquetada (INV-07).
- **La composición** de sistemas existentes que ofrece la misma superficie es el rival principal de cada campaña ([trabajo relacionado §3](../research/related-work.md)).
