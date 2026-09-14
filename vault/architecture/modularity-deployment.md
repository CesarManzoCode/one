---
id: ARC-005
kind: architecture
status: designed
---
# Modularidad, peso y despliegue

## Problema

ONE engloba demasiadas superficies como para que “instalar ONE” signifique cargar todo en cada proceso. Universalidad ingenua produciría una plataforma lenta, pesada e inútil.

## Regla fundacional

**El coste de la superficie total del repositorio no debe convertirse automáticamente en coste de cada despliegue.**

Ejemplos:

```text
RISC-V → x86 runtime
= RISC-V frontend + ONE Core necesario + x86 backend + runtime mínimo

DSP runtime
= DSP frontend + ONE Core necesario + SIMD/backend + runtime mínimo
```

No se incluyen codecs, radio, ML o emulación si no se necesitan.

## Estrategias esperadas

- componentes enlazables independientemente;
- feature/capability closure explícita;
- dead-code elimination agresiva;
- generación de runtimes especializados;
- perfiles `minimal`, `dbt`, `media`, `radio`, `ml`, `full` solo si resultan útiles;
- lazy loading cuando tenga sentido;
- cero dependencias globales innecesarias;
- herramientas pesadas permitidas en build-time si producen runtime pequeño.

## Métricas de primera clase

Cada vertical debe medir:

- binary size;
- startup;
- RSS/peak memory;
- build/compile latency;
- dependencies;
- cold/warm performance;
- tamaño incremental por capability;
- porcentaje de infraestructura realmente compartida.

## Objetivo conceptual

La forma más fuerte de ONE sería una plataforma muy general capaz de **producir sistemas especializados**. La universalidad vive en el toolchain; el artefacto desplegado paga solo por lo que usa.
