---
id: RES-009
kind: research
status: research
date: 2026-09-14
decision: decisions/ADR-008-o1-oracle-baseline.md
---
# Caracterización de oráculos RV64IM-O1

Probes mínimos sobre Sail y Spike que sostienen la resolución de los dos puntos “A confirmar” de SPEC-003 v0.1 ([ADR-008](../decisions/ADR-008-o1-oracle-baseline.md)).

**Estado:** research sobre herramientas externas. No es evidencia de ONE, no sostiene claims y no se registra en el ledger. No es tooling de ONE. El generador se conserva solo para reproducir estas observaciones.

## Entorno

| Elemento | Valor |
|---|---|
| Host | Linux 7.2.4-arch1-2 x86_64, glibc 2.44, Python 3.14.7, g++ 16.2.1 20260810 |
| Sail | Release 0.14, binario precompilado (identificadores y sha256 en ADR-008) |
| Spike | Commit `1e05ddac`, build local; dtc v1.7.2 |
| Generador | [`o1-oracle-probes/mkprobe.py`](o1-oracle-probes/mkprobe.py), sha256 `d300959248c5acf0b96eab3ef81a6e00e216792f01d3e7a4e5f9ea56a5e1e732` |
| Configuración Sail | [`sail-rv64im-o1.json`](o1-oracle-probes/sail-rv64im-o1.json); probes de límite de región con [`sail-region-end-0x80003000.json`](o1-oracle-probes/sail-region-end-0x80003000.json) |
| Configuración Spike | `--priv=mu -m0x80000000:0x10000000`; probes de límite de región con `-m0x80000000:0x3000` |

## Método

Cada probe es un ELF RV64 bare-metal:

| Contenido | Detalle |
|---|---|
| `.text` | en `0x80000000` |
| `tohost` | en `0x80001000` |
| Datos | 4 KiB en `0x80002000`, con byte `i` = `(0x11 + i) & 0xff` |

El probe instala un manejador de traps en modo M, ejecuta una instrucción bajo prueba y compara el registro resultado con el valor esperado. Sale por HTIF con uno de estos códigos:

- `0`: el valor coincide;
- `2`: valor incorrecto;
- `16 + mcause`: trap. Se añaden `mtval` y el byte `0x80002ffd`, que revela escrituras parciales.

Codificaciones `*IW` probadas, con `rd = a1`, `rs1 = a0 = 0xf0000001`:

| Probe | Palabra | Controles legales con `shamt = 1` |
|---|---|---|
| `slliw_imm5_1` | `0x0215159b` | `slliw_ctrl` `0x0015159b` |
| `srliw_imm5_1` | `0x0215559b` | `srliw_ctrl` `0x0015559b` |
| `sraiw_imm5_1` | `0x4215559b` | `sraiw_ctrl` `0x4015559b` |

Reproducción:

```sh
python3 mkprobe.py elfs
sail_riscv_sim --config-override sail-rv64im-o1.json [--config-override sail-region-end-0x80003000.json] elfs/<probe>.elf
spike --isa=rv64im_zicsr_zicclsm --priv=mu -m0x80000000:0x10000000 elfs/<probe>.elf   # región: -m0x80000000:0x3000
```

## Resultados (2026-09-14)

Leyenda: `pass` es el valor esperado sin trap; `cause` es `mcause`; `tval_lo22` son los 22 bits bajos de `mtval`; `byte[0xffd]` es el byte en `0x80002ffd` tras el trap. Su valor inicial es `0x0e`, y `0xef` indica escritura parcial.

| Probe | Sail 0.14 (`sail-rv64im-o1`) | Spike `rv64im_zicsr_zicclsm` | Spike `rv64im_zicsr` (sin Zicclsm) |
|---|---|---|---|
| `al_ld_control` | pass | pass | pass |
| `mis_ld_intrapage` | pass | pass | trap cause=4 |
| `mis_lw_intrapage` | pass | pass | trap cause=4 |
| `mis_sd_intrapage` | pass | pass | trap cause=6 |
| `mis_ld_crosspage` | pass | pass | trap cause=4 |
| `mis_ld_region_end` | trap cause=5 byte[0xffd]=0x0e | trap cause=5 byte[0xffd]=0x0e | trap cause=4 |
| `mis_ld_region_end_tval` | trap cause=5 tval_lo22=0x002ffd | trap cause=5 tval_lo22=0x003000 | trap cause=4 tval_lo22=0x002ffd |
| `mis_sd_region_end` | trap cause=7 byte[0xffd]=0x0e | trap cause=7 **byte[0xffd]=0xef** | trap cause=6 |
| `mis_sd_region_end_tval` | trap cause=7 tval_lo22=0x002ffd | trap cause=7 tval_lo22=0x003000 | trap cause=6 tval_lo22=0x002ffd |
| `slliw_ctrl`, `srliw_ctrl`, `sraiw_ctrl` | pass | pass | pass |
| `slliw_imm5_1`, `srliw_imm5_1`, `sraiw_imm5_1` | trap cause=2 | trap cause=2 | trap cause=2 |

Sail dio resultados idénticos con Zicclsm deshabilitado y con la configuración por defecto de la release. En Sail, el tratamiento de los accesos no alineados depende de `memory.misaligned`, no de la bandera `Zicclsm`.

## Interpretación

- **ISA.** Los accesos no alineados dependen del EEI. `*IW` con `imm[5] ≠ 0` son reservadas y decodificarlas es UNSPECIFIED.
- **Oráculos.** Con la configuración fijada, ambos soportan los accesos no alineados dentro de regiones y ambos producen `illegal_instruction` en las `*IW` reservadas. Spike exige `zicclsm` en `--isa`. En accesos que cruzan el final de una región difieren: Sail es atómico con `tval` igual a la dirección efectiva; Spike reporta el primer byte inaccesible y deja aplicada la escritura parcial.
- **EEI de O1.** SPEC-003 v0.2 adopta el soporte Zicclsm, la atomicidad con `tval` igual a la dirección efectiva, y el trap `illegal_instruction` para las codificaciones reservadas. ADR-008 excluye a Spike como oráculo en la clase de cruce de región con fault.
