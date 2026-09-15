---
id: ADR-008
kind: decision
status: accepted
date: 2026-09-14
characterization: research/o1-oracle-probes.md
---
# ADR-008 — Oráculos de O1 y cierre pre-código de RV64IM-O1

## Contexto

[VAL-004 §7](../validation/o1-protocol.md) usa Sail, Spike, Clang y GCC como oráculos. Los primeros consumidores de código de O1 (verificador, intérprete, decodificador) no pueden validarse de forma reproducible sin versiones y configuración fijadas. SPEC-003 v0.1 dejaba esas versiones para el preregistro y tenía dos puntos “A confirmar”:

1. los accesos RV64IM no alineados;
2. `SLLIW`/`SRLIW`/`SRAIW` con `imm[5] ≠ 0`.

Tras [ADR-007](ADR-007-o1-implementation-foundation.md), eran las únicas obligaciones `pre-código` restantes.

## Decisión

Alcance: O1.

### 1. Versiones fijadas

| Oráculo | Identificador | Versión observada o esperada | Configuración para O1 |
|---|---|---|---|
| **Sail RISC-V** | Release `0.14` (tag ligero) → commit `29e6158f0a88bdb26b9fbcd0718ab919449b5179`. Artefacto `sail-riscv-Linux-x86_64.tar.gz`, sha256 `363f851ba91c674cd818040e232c4baf0ec382406a0a9696b1dde687ea160b2a`; `bin/sail_riscv_sim`, sha256 `ba63996a0b1fb65149db83ae561dd96776b22432d4bddbd4c3d56f78cfce29dc`. | Observada: `--version` → `0.14`. `--build-info`: Sail 0.20.2 (`3b7af38d`), GNU C++ 8.5.0. | Configuración por defecto de esa release más el override [`sail-rv64im-o1.json`](../research/o1-oracle-probes/sail-rv64im-o1.json): solo `M`, `U`, `Zicsr` y `Zicclsm`; `V` deshabilitada; `mstatus.FS`/`VS` de solo lectura a cero; `memory.misaligned.exceptions.load_store = None`. |
| **Spike** | Commit `1e05ddac3a6c351bfc0aeed0cf3a68940e7200ab` de `master` (2026-09-11). Build desde fuente con `configure && make`, host g++ 16.2.1, dtc v1.7.2 (`2d10aa2afe35527728db30b35ec491ecb6959e5c`). | Observada: `Spike RISC-V ISA Simulator 1.1.1-dev`. | `--isa=rv64im_zicsr_zicclsm --priv=mu`. |
| **Clang** | `llvmorg-23.1.1` → commit `6dfe1677ab8dffbc6ec13d53a1e0215d75147689`, la revisión de ADR-007. Build de oráculo (nodo `test`) separado del prefijo MLIR de implementación. | Esperada: `clang version 23.1.1`. No construido en este sprint; se verifica en su primer build. | Nativo `x86_64-pc-linux-gnu`. Pares derivados RISC-V: `--target=riscv64-unknown-elf -march=rv64im -mabi=lp64`. |
| **GCC** | `releases/gcc-16.2.0` → commit `78d4ac73dd391005b895a6148cd9831e28e1208b` (objeto tag `1831ac03fd08e3400c16b29f21762e6b326a618d`). Release estable del 2026-08-07. | Esperada: `gcc (GCC) 16.2.0`. No construido en este sprint; se verifica en su primer build. | Nativo `x86_64-pc-linux-gnu`. Cross RISC-V para pares derivados: `--target=riscv64-unknown-elf --with-arch=rv64im --with-abi=lp64`. |

`Zicsr` y `--priv=mu` sirven solo al harness en modo M para observar traps. El código bajo prueba se ejecuta en U, sin CSRs, conforme a SPEC-003.

Sail informa además `zvl*` y `ssstateen`/`smstateen` en su ISA string. No añaden instrucciones a la superficie U de RV64IM-O1.

Ninguna instalación del sistema, rama móvil, `latest` ni pre-release semanal es baseline autoritativo.

### 2. Resolución de SPEC-003

SPEC-003 pasa a la versión 0.2. En ambos puntos se separa lo que dice la ISA, lo que decide el EEI de O1 y lo que hacen los oráculos.

| Punto | ISA 20260120 | EEI de RV64IM-O1 (SPEC-003 v0.2) | Sail 0.14 (configuración de §1) | Spike `1e05ddac` (configuración de §1) |
|---|---|---|---|---|
| Accesos no alineados | Dependen del EEI. | Soportados, con semántica Zicclsm en todas las regiones; little-endian, también si cruzan página. | Completan con el valor correcto. | Completan con el valor correcto. Sin `zicclsm` en `--isa` producen trap `*_address_misaligned` (causa 4 o 6). |
| Acceso con algún byte fuera de región | Sin cláusula específica en la ISA no privilegiada. | Trap de acceso con `tval` igual a la dirección efectiva; escritura atómica. | Coincide: `tval = a`, sin escritura parcial. | **Diverge**: `tval` = primer byte inaccesible, y la escritura parcial queda aplicada. |
| `*IW` con `imm[5] ≠ 0` | Reservadas; comportamiento UNSPECIFIED. Antes causaban illegal-instruction. | Trap `illegal_instruction(epc = pc)` al alcanzarse, por decisión del EEI. | `illegal_instruction` (causa 2). | `illegal_instruction` (causa 2). |

### 3. Regla de divergencia conocida

Sail es el oráculo derivado de especificación y la referencia en caso de discrepancia. Spike **no es oráculo** para la clase “carga o escritura que cruza el límite de una región y produce fault”: sus resultados en esa clase se registran aparte y nunca cuentan como divergencia de ONE ni como acuerdo.

Es una limitación del alcance de un oráculo, no una excepción a un invariante de ONE. Cualquier otra divergencia Sail/Spike que se encuentre se caracteriza y se resuelve por ADR antes de usar esa clase como evidencia.

### 4. Cambios posteriores

Cambiar una versión o una configuración fijada exige un ADR posterior, antes del preregistro y nunca durante una campaña.

## Alternativas consideradas

- **Spike `v1.1.0`** (única release, de 2021): no se caracterizó. Un commit probado es más reproducible que una release antigua sin caracterizar.
- **Sail `master` o una pre-release semanal:** rolling.
- **GCC 15.3 o 13.5:** ramas anteriores; 16.2 es la release estable de la rama más reciente.
- **Clang o GCC del sistema:** versiones rolling y dependientes del host.
- **Prohibir los accesos no alineados en el perfil:** reduce el perfil sin necesidad, porque ambos oráculos los soportan con configuración explícita. La trampa por defecto de Spike es configuración, no semántica.
- **Rechazar estáticamente las `*IW` reservadas:** los bytes de una región `X` pueden no alcanzarse nunca, y en eso SPEC-003 decide por alcance.
- **Dejar las `*IW` reservadas como comportamiento libre:** pierde comparabilidad con los oráculos.
- **Adoptar la semántica de Spike en los cruces de región:** una escritura parcial con `tval` desplazado complica las comprobaciones explícitas de acceso en Core-O1 (ADR-005) y diverge del oráculo derivado de especificación.

## Base

**Fuentes primarias** ([fuentes](../research/sources.md)):

- Unprivileged ISA 20260120:
  - cap. RV32I: accesos no alineados dependientes del EEI; decodificación de instrucciones reservadas UNSPECIFIED;
  - cap. RV64I: `*IW` con `imm[5] ≠ 0` reservadas;
- perfil RVA23: definición de Zicclsm.

**Código fuente:**

- en Spike, `mmu.h` habilita accesos no alineados solo si `EXT_ZICCLSM` está en la ISA, y `MASK_SLLIW`/`SRLIW`/`SRAIW` = `0xfe00707f` incluye `imm[5]`;
- en Sail, `encdec` de `SHIFTIWOP` exige `0b0000000`/`0b0100000` en `imm[11:5]`, y `memory.misaligned` controla los accesos.

**Probes:** la [caracterización](../research/o1-oracle-probes.md) es reproducible.

**No existe implementación de ONE ni evidencia observada de sus claims.** Los probes caracterizan herramientas externas y no entran en el ledger.

## Consecuencias

- SPEC-003 v0.2 no contiene puntos “A confirmar”. VAL-004 §7 remite a esta configuración.
- No queda ninguna obligación `pre-código`. El primer sprint de implementación puede construir e integrar los oráculos desde estos identificadores.
- El harness fija el mapa de memoria del oráculo a partir de las regiones del manifiesto. Los probes de límite de región muestran que la frontera de región afecta a `tval` y a las escrituras.

## Qué no decide

- Flags, niveles de optimización y presupuestos de la campaña (U5, `pre-held-out`).
- Binutils y newlib del cross RISC-V, necesarios solo para pares derivados, que se fijan con su preregistro.
- Versiones de Rellume y caracterización de la composición rival ([Q25](../roadmap/open-questions.md)).
- Solver SMT y fuzzers, que se fijan al introducir sus consumidores.
- Cerberus.
- Otras partes de SPEC-003.

## Condiciones de revisión

- Una versión fijada presenta un defecto que impide validar SPEC-003.
- Aparece otra divergencia Sail/Spike en una clase admitida por el perfil.
- El primer build de Clang o GCC no reproduce la versión esperada.

## Relaciones

Complementa [ADR-007](ADR-007-o1-implementation-foundation.md). Motiva SPEC-003 v0.2. Afecta a C-O1-2 y a la matriz de VAL-004 §7.
