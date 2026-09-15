---
id: ARC-005
kind: architecture
status: designed
---
# Modularidad, peso y despliegue

## Problema

ONE engloba demasiadas superficies como para que “instalar ONE” signifique cargarlo todo en cada proceso. Una universalidad ingenua produciría una plataforma lenta, pesada e inútil.

## Regla fundacional

**El coste de la superficie total del repositorio no se convierte automáticamente en coste de cada despliegue** ([ADR-003](../decisions/ADR-003-modular-universality.md)).

## Grafo de capabilities

Cada componente es un nodo con operaciones y servicios provistos, tipo (`compiler`, `runtime`, `test`), dependencias, raíces y targets. El esquema del nodo y las mediciones están en [VAL-003 §6](../validation/metrics.md).

| Regla | Contenido |
|---|---|
| A1 | Las closures y los perfiles de artefacto se derivan del grafo; nunca son listas mantenidas a mano. |
| A2 | El core no depende de nodos de dominio ni de origen (INV-19). |
| A3 | No hay raíces ocultas: registros, inicializadores estáticos, reflexión y tablas de punteros a función declaran sus raíces en su nodo. Un registro que arrastra todos los pases a todo artefacto viola la closure. |
| A4 | Los componentes de compilador, runtime y test son nodos separados. |
| A5 | Tooling y metadatos de depuración son nodos opcionales, fuera del runtime mínimo. |
| A6 | Se permite infraestructura pesada en build-time si el artefacto resultante es pequeño. |
| A7 | La implementación usa una convención de espacios de nombres que permite mapear cada símbolo a su nodo. |

## Artefactos de O1

| Artefacto | Closure | Debe excluir |
|---|---|---|
| Herramienta `one-c` | frontend C + core + backend x86-64 | lifter RV, runtime guest |
| Herramienta `one-rv` | lifter RV + core + backend x86-64 | frontend C |
| Herramienta `one-o1` | ambas rutas | — |
| Objeto generado desde C | código generado | todo runtime: una ruta C sin traps no necesita servicios |
| Objeto generado desde RV64IM | código generado + `one_rt_trap` + runtime guest | frontends |

Estas exclusiones son el gate G5 y el claim C-O1-6.

## Perfiles

Perfiles como `minimal`, `dbt`, `media`, `radio`, `ml` o `full` existirán solo si son closures derivadas útiles, nunca como categorías previas. Lazy loading solo donde el coste medido lo justifique.

## Objetivo conceptual

La forma más fuerte de ONE sería una plataforma muy general capaz de producir sistemas especializados. La universalidad vive en el toolchain; el artefacto desplegado paga solo por lo que usa. Que esto se sostenga con muchos dominios es H4.
