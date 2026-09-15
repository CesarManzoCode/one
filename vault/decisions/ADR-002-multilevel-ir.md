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

## Relaciones

O1 no produce evidencia para esta decisión: sus frontends descargan directamente al join ([ADR-006](ADR-006-o1-falsification-campaign.md)). La primera campaña que la ejercita es EXP-02. La noción de nivel como relación de legalidad está en [ARC-003](../architecture/ir.md).
