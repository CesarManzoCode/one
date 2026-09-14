---
id: ADR-003
kind: decision
status: accepted
---
# ADR-003 — Universalidad modular

## Decisión

ONE puede ser enorme como repositorio/toolchain, pero una aplicación desplegada debe poder enlazar o generar solo la closure de capabilities que necesita.

## Motivo

Ser universal y ser usable son requisitos simultáneos. Cargar codecs, emulación, ML y radio para ejecutar una función C simple sería un fracaso arquitectónico.

## Consecuencia

Footprint, startup y tamaño incremental por capability se consideran correctness/performance del producto, no polish posterior.
