---
id: RES-002
kind: research
status: accepted
---
# Trabajo relacionado y superficie de referencia

Este documento no pretende ser una revisión completa. Registra sistemas que ya prueban partes de la intuición de ONE y por tanto evitan reclamar novedad donde no existe.

## QEMU TCG

QEMU demuestra una forma importante de unificación: varias ISAs guest se traducen a una IR intermedia y después a hosts diferentes. TCG incluye IR, optimizaciones, helpers, soporte vectorial y backends.

ONE debe asumir que “guest ISA → common IR → host” no es una idea nueva. La apuesta de ONE es extender una arquitectura de convergencia más allá de emulación y explorar reutilización real con otras familias de cómputo.

## MLIR

MLIR demuestra que un IR multinivel con dialectos puede conservar información específica y bajar progresivamente hacia representaciones más cercanas a máquina. También documenta explícitamente el problema de bajar demasiado pronto y después intentar reconstruir semántica perdida.

ONE debe aprender de MLIR y evitar reclamar como propia la mera idea de dialectos o multi-level lowering.

La pregunta diferenciadora es si una arquitectura deliberadamente construida alrededor de **compilation + DBT + DSP/media + ML/radio** puede compartir más mecanismos y optimizaciones de los que hoy comparten esos ecosistemas separados, manteniendo una densidad extrema.

## El riesgo de reinventar MLIR peor

Si ONE termina siendo únicamente “MLIR, pero escrito por nosotros y con menos ecosistema”, habrá fallado arquitectónicamente incluso si funciona.

ONE necesita una tesis propia observable, no solo independencia de dependencias.
