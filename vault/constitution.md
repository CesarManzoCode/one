---
id: CON-001
kind: constitution
status: accepted
---
# Constitución técnica de ONE

## Qué debe existir

ONE debe ser una plataforma de cómputo capaz de recibir formas de cómputo provenientes de dominios distintos, preservar la información semántica que importa mientras todavía sea útil y hacerlas converger progresivamente hacia infraestructura compartida de análisis, optimización y ejecución.

La apuesta no es “todo es lo mismo”. La apuesta es que **muchas transformaciones computacionales comparten suficiente estructura como para justificar una arquitectura común**, siempre que el lowering ocurra en el nivel correcto y no destruya información prematuramente.

ONE debe poder crecer hacia compilación, traducción dinámica de binarios, emulación, cómputo numérico, DSP, multimedia, ML y comunicaciones definidas por software sin convertirse en una colección de subsistemas independientes unidos solo por estar en el mismo repositorio.

## La unidad común

ONE no unifica objetos del mundo. Un video sigue siendo video. Una señal de radio sigue siendo una señal muestreada. Un binario x86 sigue codificando una máquina abstracta concreta. Un programa C sigue teniendo semántica de lenguaje.

Lo común es el **cómputo**: lectura y escritura de estado, transformaciones escalares y vectoriales, memoria, control, efectos, streams, relaciones de dependencia y operaciones de dominio que pueden conservarse en niveles altos y bajar gradualmente.

ONE busca el nivel mínimo de abstracción donde compartir infraestructura sea materialmente útil **sin fingir equivalencias que no existen**.

## Arquitectura multinivel, no IR plano universal

Una única lista de `load/add/store/branch` podría representar casi cualquier cómputo, pero perdería demasiada información para optimizar bien dominios distintos. ONE por tanto debe asumir desde la fundación una arquitectura multinivel:

```text
entrada específica
    ↓
representación rica del dominio
    ↓
representaciones ONE de nivel intermedio
    ↓
ONE Core
    ↓
representación cercana a máquina
    ↓
backend/hardware
```

Las fronteras exactas no están decididas. Sí está decidido que **bajar demasiado pronto es un error** si destruye información que después habría que reconstruir.

## Universalidad sin coste universal obligatorio

El repositorio puede llegar a ser enorme en superficie. Una ejecución concreta no debe pagar por todas las capacidades del repositorio.

Un usuario que necesite RISC-V → x86 no debe cargar codecs, radio o ML. Un pipeline DSP no debe cargar el emulador completo. ONE debe soportar composición, eliminación agresiva de código no usado y perfiles especializados.

Idealmente, el toolchain general podrá producir runtimes especializados que contengan solo las capacidades necesarias para una aplicación concreta.

## Compactación de complejidad

ONE no gana por acumular millones de líneas o depender de decenas de frameworks. La densidad técnica forma parte del proyecto: máxima superficie útil con mínima complejidad accidental.

No se fija un límite arbitrario de LOC. Sí se medirán como propiedades de primera clase:

- tamaño de binarios;
- memoria residente;
- startup;
- tiempo de compilación;
- dependencias;
- cantidad de infraestructura duplicada entre dominios;
- reutilización material de mecanismos y de conocimiento de optimización entre dominios, medida como vector (el tamaño de código es solo diagnóstico);
- coste de añadir un frontend o backend nuevo.

## Herramientas

ONE puede construirse con IA, IDEs, compiladores, debuggers, theorem provers, fuzzers, documentación, GitHub o cualquier herramienta disponible. **No existe una penalización epistemológica especial por usar IA.**

La evaluación del proyecto es efectiva: qué problemas puede resolver el sistema que dirige César, con qué calidad y con qué evidencia. Si en algún contexto futuro se quisiera medir autoría manual o capacidad sin asistencia, sería otra pregunta y debería declararse explícitamente.

## Hardware y mundo físico

ONE opera sobre cómputo digital. No sustituye antenas, sensores, ADC, DAC, cámaras, altavoces ni otros transductores. Una vez que una señal o fenómeno está representado digitalmente, ONE puede intentar representar y ejecutar las transformaciones que operan sobre esa representación.

## Utilidad

El objetivo primario no es encontrar mercado. Sin embargo, ONE debe conservar la posibilidad de utilidad real.

La utilidad potencial más fuerte es reducir trabajo duplicado entre toolchains: si múltiples clases de cómputo convergen en una infraestructura común, un nuevo backend de hardware podría beneficiar simultáneamente compilación, DBT, DSP, media, ML y otras superficies. Una optimización nueva podría propagarse entre dominios en vez de ser reimplementada en cada ecosistema.

Esto es una hipótesis, no una promesa.

## Honestidad de la comparación

ONE puede usar LLVM, GCC, QEMU, FFmpeg, MLIR, GNU Radio, TVM, bibliotecas numéricas y otras implementaciones como oráculos, rivales y fuentes de investigación. No deben convertirse inadvertidamente en la implementación central de la propiedad que ONE pretende demostrar.

Si un sistema rival mejora y elimina una ventaja de ONE, se actualiza la comparación. La arquitectura debe sobrevivir al mejor rival disponible, no a una versión conveniente del rival.

ONE no reclama novedad por mecanismos ya establecidos (IR compartido, SSA, IR multinivel, dialectos, lowering progresivo, lifting binario, DBT sobre IR común, reutilización de frontends y backends, runtimes especializados) ni por haberlos implementado de nuevo. Su originalidad, si existe, solo puede demostrarse mediante propiedades observables que la composición de sistemas existentes no ofrezca con coste comparable.

## Qué significa éxito técnico

ONE habrá probado su tesis solo si compartir representación e infraestructura produce beneficios materiales: menos duplicación, mejor portabilidad, reutilización real de optimizaciones, mejor tooling común, mayor densidad o nuevas capacidades sin una penalización inaceptable de rendimiento.

Si cada dominio termina necesitando su propio compilador, optimizador y runtime prácticamente independiente y ONE solo aporta una capa común trivial, la hipótesis central habrá fallado aunque el repositorio sea impresionante.
