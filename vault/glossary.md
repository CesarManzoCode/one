---
id: GLO-001
kind: glossary
status: accepted
---
# Glosario

**ONE** — Proyecto completo y repositorio único.

**ONE IR** — Familia de representaciones intermedias de ONE. El nombre no implica una sola representación plana.

**ONE Core** — Núcleo computacional compartido al que múltiples dominios convergen progresivamente.

**Frontend** — Componente que traduce una entrada con semántica propia a representaciones ONE: C, RISC-V, x86, DSP, media, etc.

**Backend** — Componente que lleva una representación ONE a una plataforma de ejecución concreta: x86-64, AArch64, RISC-V, WASM, GPU/acelerador u otra futura X.

**Dominio** — Familia de cómputo con semánticas y optimizaciones propias: lenguaje, ISA, DSP, video, radio, tensor, etc.

**Lowering** — Transformación desde una representación más rica/específica a otra más general o cercana a máquina.

**Semántica preservada** — Información que una transformación debe mantener para que el programa o pipeline conserve significado y para que optimizaciones válidas sigan siendo posibles.

**Cross-origin equivalence** — Capacidad de reconocer o canonicalizar cómputos equivalentes que llegaron desde orígenes distintos, por ejemplo C y un binario RISC-V.

**Compression of complexity** — Relación entre superficie/capacidad ofrecida y complejidad accidental necesaria para ofrecerla.

**X** — Hardware/backend nuevo o especializado que ONE debería poder incorporar sin reconstruir cada ecosistema por separado.

**Runtime especializado** — Artefacto generado o enlazado a partir de ONE que contiene solo las capacidades que una aplicación concreta necesita.

