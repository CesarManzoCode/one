---
id: ADR-002
kind: decision
status: accepted
---
# ADR-002 — Representación multinivel

## Decisión

ONE no intentará forzar todas las entradas directamente a un IR plano mínimo. Se conservarán representaciones ricas y se hará lowering progresivo.

## Motivo

Una reducción universal a primitivas elementales es computacionalmente posible pero puede destruir precisamente la información necesaria para optimizar video, DSP, tensor compute o estado de una ISA guest.

## Consecuencia

El diseño debe encontrar fronteras de lowering y mecanismos de interacción entre niveles. La cantidad exacta de niveles sigue abierta.
