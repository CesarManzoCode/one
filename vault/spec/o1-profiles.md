---
id: SPEC-003
kind: spec
status: designed
version: 0.2
---
# Perfiles de O1: ONE-C-O1, RV64IM-O1, x86-64-O1

Superficie exacta de O1 decidida en [ADR-006](../decisions/ADR-006-o1-falsification-campaign.md). Las relaciones semánticas por arista están en [SPEC-001 §4](semantics.md); el core de destino es [SPEC-002](core-o1.md).

**Disciplina de salida de un frontend.** Cada construcción de entrada tiene exactamente uno de cuatro destinos:

1. **Aceptada**: se traduce según este documento.
2. **Rechazada**: diagnóstico estático obligatorio; nunca aproximación silenciosa.
3. **Trap**: comportamiento definido del origen, preservado como `trap` explícito.
4. **`unsupported`**: incompletitud dinámica declarada; nunca cuenta como éxito.

Confundir 2, 3 y 4 es un defecto de corrección.

## 1. ONE-C-O1 v0.1

### 1.1 Entorno fijado

| Aspecto | Valor |
|---|---|
| Base | ISO C23 freestanding (N3096 como texto de referencia). |
| Bytes y enteros | `CHAR_BIT = 8`; complemento a dos; `short` 16, `int` 32, `long` y `long long` 64 bits; `size_t` = `unsigned long`; `ptrdiff_t` = `long`. |
| Punteros | 64 bits, little-endian. |
| `char` sin calificar | **Rechazado.** x86-64 System V lo define con signo y RISC-V LP64 sin signo. |
| Conversión a entero con signo fuera de rango | módulo `2^N`. |
| `>>` sobre valor con signo negativo | aritmético. |
| Layout de `struct` | alineación natural psABI LP64; coincide en x86-64 System V y RISC-V LP64 para los tipos admitidos. |
| Orden de evaluación | izquierda a derecha; irrelevante por la regla de un efecto (§1.2). |

### 1.2 Aceptado

- **Tipos**: `_Bool`; enteros estándar con signo y sin signo y `intN_t`/`uintN_t` salvo `char` sin calificar; punteros a tipos objeto admitidos; arrays de tamaño constante; `struct` sin bitfields, sin miembro flexible y sin anonimato; calificador `const`.
- **Funciones**: definidas en la misma unidad de traducción; hasta 6 parámetros escalares (enteros o punteros); retorno escalar o `void`; llamadas directas; recursión directa o mutua; `static`.
- **Objetos**: globales con inicializador constante o implícitamente a cero; **locales con inicializador obligatorio** (agregados con inicializador completo o `{0}`).
- **Expresiones**: aritmética, operaciones bit a bit y desplazamientos; comparaciones enteras; `!`, `&&`, `||`; `?:`; asignación simple y compuesta; `++`/`--`; casts entre tipos enteros; `sizeof` y `_Alignof` de tipos admitidos; `&`, `*`, `[]`, `.`, `->`; puntero ± entero; resta de punteros; `==`/`!=` entre punteros del mismo tipo o con constante nula.
- **Sentencias**: bloques, `if`/`else`, `while`, `do`, `for`, `switch` con `case` constantes y `default`, `break`, `continue`, `return`.
- **Regla de un efecto**: cada full-expression contiene a lo sumo un efecto lateral (asignación, incremento/decremento o llamada), además de la asignación más externa si existe; el lvalue de esa asignación no contiene efectos laterales. Esta regla elimina estáticamente el orden no especificado y las modificaciones no secuenciadas.
- **Unidad**: una unidad de traducción; las entradas de contrato son funciones con enlace externo.

### 1.3 Rechazado

Coma flotante y `_Complex`; `char` sin calificar; `union`; bitfields; miembros flexibles; VLA; `enum`; punteros a función y llamadas indirectas; varargs; `setjmp`/`longjmp`; `goto` y etiquetas; `volatile`; `restrict`; `_Atomic`, `_Thread_local`, hilos; ensamblador inline y extensiones GNU; comparaciones relacionales entre punteros; casts puntero↔entero y entre tipos puntero distintos; `void*`; memoria dinámica y toda llamada a biblioteca; cabeceras distintas de `<stdint.h>`, `<stdbool.h>` y `<stddef.h>`; `struct` pasado o devuelto por valor; asignación de `struct`; locales sin inicializador; locales `static`; caminos de una función no-`void` que no terminan en `return`; `main` como unidad.

### 1.4 Descarga del `ub` de C

| Comportamiento indefinido en C | Forma en Core-O1 |
|---|---|
| Desbordamiento con signo en `+ − *` tras promociones enteras (incluido `uint16_t * uint16_t` promovido a `int`) | hecho `nsw` |
| `/` o `%` con divisor 0; `MIN / −1`; `MIN % −1` | precondición de `sdiv`/`srem`/`udiv`/`urem` |
| Desplazamiento negativo o `≥` ancho | precondición de shift |
| `<<` con signo que desborda | `shl nsw` |
| `<<` de valor con signo negativo | **olvidado**: `shl nsw` admite negativos; es un refinamiento |
| Acceso fuera de objeto, a nulo o a objeto muerto | precondición de acceso de `load`/`store` |
| Aritmética de puntero fuera de `[0, n]`; resta de punteros de objetos distintos | **olvidado**: resultado modular; el uso posterior se rige por la precondición de acceso |
| Lectura antes de escritura | imposible por las reglas de inicialización, salvo un puntero a slot muerto, que cae en la precondición de acceso |

### 1.5 Contrato de olvido C → Core-O1

| Información | Forma de destino | Condición | Qué queda imposible | ¿Recuperable? |
|---|---|---|---|---|
| Tipos C: signedness, campos | signedness en operaciones; offsets constantes | siempre | análisis basados en tipos (TBAA); no se emiten en v0.1 | no |
| Procedencia de punteros | direcciones planas + frescura de `slot` | sin casts ni `void*` | alias basado en objetos más allá de slots; bounds de objeto para optimización | no; ver [Q4](../roadmap/open-questions.md) |
| `ub` aritmético con signo | `nsw` | — | nada | — |
| `ub` de división, shift y acceso | precondiciones | — | nada | — |
| Obligaciones de §1.4 marcadas “olvidado” | ninguna | refinamiento | optimizaciones que las usarían | no |
| Estructura de bucles | CFG | — | forma `for`/`while` | parcialmente, por análisis de bucles |
| Ubicaciones | procedencia borrable | — | — | — |

## 2. RV64IM-O1 v0.2

**Cambios respecto de v0.1**, todos en esta sección:

- se fija el soporte de accesos no alineados, que v0.1 marcaba “A confirmar”;
- las cargas y escrituras que cruzan el límite de una región son atómicas, con `tval` igual a la dirección efectiva;
- las codificaciones `SLLIW`/`SRLIW`/`SRAIW` con `imm[5] ≠ 0` quedan reservadas por la ISA, y su trap es una decisión de este EEI.

Los oráculos y su configuración están en [ADR-008](../decisions/ADR-008-o1-oracle-baseline.md); la caracterización, en [research](../research/o1-oracle-probes.md). ONE-C-O1 y x86-64-O1 no cambian.

### 2.1 Máquina de referencia

| Aspecto | Valor |
|---|---|
| Hart | RV64IM: `XLEN = 64`, sin C, F, D, A, V ni Zicsr visible; `IALIGN = 32`. |
| Orden de bytes | little-endian. |
| Modo | U, con entorno de ejecución a nivel de función (§2.3). |
| Referencia normativa | RISC-V Unprivileged ISA, Version 20260120 (Official Release), citada en [fuentes](../research/sources.md). Oráculos y configuración: [ADR-008](../decisions/ADR-008-o1-oracle-baseline.md). |
| Accesos a datos en direcciones no alineadas | **Soportados por el EEI.** La ISA deja su comportamiento al EEI. Este EEI garantiza la semántica de Zicclsm en todas las regiones: una carga o escritura de ancho `w` en la dirección efectiva `a` opera sobre los bytes `[a, a + w)` en little-endian, incluido el cruce de página, y nunca produce trap de alineación. Si algún byte queda fuera de una región con el permiso requerido, se aplica §2.3. |

### 2.2 Entrada

Imagen cruda + manifiesto. **No se acepta ELF en v0.2.**

| Campo del manifiesto | Contenido |
|---|---|
| Regiones | `{vaddr, size, perms ⊆ {R,W,X}, bytes iniciales o relleno a cero}` |
| Funciones | `{símbolo, vaddr, size}` |
| Pila | región `RW` designada y su tope |
| Entradas | símbolo y firma de contrato (§4) |

### 2.3 Entorno de ejecución a nivel de función

**Estado inicial**:

- `pc` = entrada;
- `a0`–`a5` según el binding de §4;
- `sp` = tope de pila, alineado a 16;
- `ra` = continuación `R`: dirección centinela alineada fuera de toda región `X`;
- demás registros sin especificar (no determinismo del entorno, SPEC-001 §3).

**Terminación y traps.** Payload `(epc, tval)`. `tval` solo es observable donde este perfil lo fija.

| Evento | Resultado |
|---|---|
| Salto a la continuación de la activación | `return`: a nivel de entrada, `a0`/`a1` y el estado |
| Lectura en la que algún byte de `[dirección, dirección + ancho)` está fuera de una región `R` | `trap #load_access_fault(epc = pc, tval = dirección)`. `tval` es la dirección efectiva del acceso, no la del primer byte inaccesible. |
| Escritura en la que algún byte de `[dirección, dirección + ancho)` está fuera de una región `W` | `trap #store_access_fault(epc = pc, tval = dirección)`. El acceso es atómico: no se escribe ningún byte. |
| Rama tomada o salto a destino no múltiplo de 4 | `trap #instruction_address_misaligned(epc = pc, tval = destino)` |
| Ejecución en dirección fuera de región `X` | `trap #instruction_access_fault(epc = destino, tval = destino)` |
| Se alcanza una codificación no definida por RV64IM: reservada por la ISA (incluidas `SLLIW`/`SRLIW`/`SRAIW` con `imm[5] ≠ 0`) o de una extensión no implementada | `trap #illegal_instruction(epc = pc)`. Es una decisión de este EEI. La ISA 20260120 marca esas `*IW` como reservadas, con comportamiento UNSPECIFIED; versiones anteriores de la ISA exigían la excepción. |
| `ECALL` / `EBREAK` | `trap #env_call(epc)` / `trap #breakpoint(epc)` |
| Transferencia dinámica a una dirección `X` que no es la continuación | `unsupported(indirect_transfer)` |

Como ninguna región es `W` y `X` a la vez, el código automodificable es imposible por definición del entorno: no se necesita invalidación.

### 2.4 Instrucciones admitidas

`LUI AUIPC JAL JALR BEQ BNE BLT BGE BLTU BGEU LB LH LW LD LBU LHU LWU SB SH SW SD ADDI SLTI SLTIU XORI ORI ANDI SLLI SRLI SRAI ADD SUB SLL SLT SLTU XOR SRL SRA OR AND ADDIW SLLIW SRLIW SRAIW ADDW SUBW SLLW SRLW SRAW MUL MULH MULHSU MULHU DIV DIVU REM REMU MULW DIVW DIVUW REMW REMUW ECALL EBREAK`

### 2.5 Semántica que el lifter debe hacer explícita

| Aspecto | Semántica RV64IM | Forma en Core-O1 |
|---|---|---|
| `x0` | lectura 0; escritura descartada | constante; escrituras eliminadas |
| `JALR` | destino `(rs1 + sext(imm)) & ~1`, calculado antes de escribir `rd` | `and` explícito; orden preservado |
| Shifts por registro | cantidad `rs2 & 63`; variantes `W`: `& 31` y resultado extendido con signo desde 32 bits | `shl(x, and(amt, 63))`, que cumple la precondición por construcción |
| Variantes `W` | operan sobre los 32 bits bajos y extienden con signo | `sext<64>(op(trunc<32>(a), trunc<32>(b)))` sin hechos |
| `DIV`/`REM` | `b = 0` → cociente `−1`, resto `a`; `(MIN, −1)` → cociente `MIN`, resto `0` | guardas explícitas + `sdiv`/`srem` en el camino con precondición cierta |
| `DIVU`/`REMU` | `b = 0` → cociente `2^64 − 1`, resto `a` | guarda explícita + `udiv`/`urem` |
| `MULHSU` | alta mixta | `mulh_uu(a,b) − (a <s 0 ? b : 0)` |
| Cargas y escrituras | según permisos de región | comprobación explícita de rango y permiso + `load`/`store` en `guest` |

### 2.6 Control y llamadas

- Una **función lifted** tiene firma `(x1…x31, cont) → (x1…x31)`: estado entero completo. `cont` es la dirección de continuación.
- `JAL rd ≠ x0` a un símbolo de función → `call` con `rd := pc+4` y `cont := pc+4`; el llamador continúa en `pc+4` con el estado devuelto. A una dirección de la misma función → salto intra-función que escribe `rd`.
- `AUIPC rX` seguido de `JALR` sobre `rX` con destino constante → llamada o salto directo según el destino. Es un idioma de decodificación declarado como infraestructura del origen.
- `JALR x0` con destino `t`, en este orden: alineación → `#instruction_address_misaligned`; `t = cont` → `return`; `t` en región `X` → `unsupported(indirect_transfer)`; resto → `#instruction_access_fault`.
- Salto (`rd = x0`) a otro símbolo → llamada de cola: `call` seguido de `return`.
- **El lifter no asume el ABI.** No estrecha el estado en llamadas salvo por prueba. El estrechamiento lo hace un pase compartido o un análisis del frontend contabilizado como infraestructura del origen (VAL-003 §4, [Q11](../roadmap/open-questions.md)).
- Las guardas de retorno y las comprobaciones de acceso son eliminables solo por optimización probada. Contarlas mide precisión de optimización sobre código guest.

### 2.7 Rechazo estático de imagen

Regiones solapadas; región `W ∧ X`; símbolo de función fuera de `X` o desalineado; destino estático en `X` dentro de otra función que no es su entrada; `JALR rd ≠ x0` fuera del idioma `AUIPC`+`JALR`; límites de tamaño fijados en el preregistro.

### 2.8 Contrato de olvido RV64IM → Core-O1

| Información | Forma de destino | Condición | Qué queda imposible |
|---|---|---|---|
| Identidad de registros y `pc` | valores SSA; `pc` solo en payloads de trap y en `cont` | — | nada observable en el perfil |
| Fronteras de instrucción | perdidas | el perfil no tiene interrupciones ni single-step | interrupciones precisas y single-step (fuera de perfil) |
| Formato de instrucción y pseudo-instrucciones | perdidos | — | — |
| Mapa de memoria y permisos | declaración del espacio `guest` + comprobaciones explícitas | — | — |
| ABI LP64 | no asumido | — | estrechamiento sin prueba |
| Ubicación por instrucción | procedencia borrable | — | — |

### 2.9 Validez de workloads

Son propiedades del corpus comprobadas con los modelos de referencia, no suposiciones del lifter:

- **conformidad ABI**: con valores centinela en `s0`–`s11`, `sp`, `gp` y `tp`, la función los restaura al retornar;
- **independencia de registros basura**: el comportamiento de referencia no cambia con al menos dos rellenos aleatorios de registros no argumento;
- terminación dentro del combustible;
- ningún trap en la campaña primaria;
- construido o ensamblado restringido a `rv64im`/`lp64`.

## 3. x86-64-O1 v0.1

| Aspecto | Contrato |
|---|---|
| Salida | ELF64 `ET_REL`: `.text`, `.rodata`, `.data`, `.bss`, símbolos, relocations `R_X86_64_PC32`, `R_X86_64_PLT32`, `R_X86_64_64`. Sin PIC/GOT/PLT generados, sin DWARF, sin `.eh_frame`. |
| Enlace | Linker del sistema con el harness. **No central**: ningún claim cubre el linker. |
| Instrucciones | x86-64 base (nivel v1), solo enteras. |
| ABI exportado | System V AMD64: hasta 6 argumentos enteros en `rdi, rsi, rdx, rcx, r8, r9`; resultados en `rax` y `rdx`; pila alineada a 16 en cada `call`; `rbx, rbp, r12–r15` preservados. |
| ABI interno | Convención interna para funciones con más de 6 argumentos o 2 resultados. Es un mecanismo compartido por ambos orígenes. |
| Backend mínimo | Legalización de Core-O1; selección de instrucciones; registros virtuales con asignador real con spills (linear scan o superior); frames; llamadas; emisión y relocations. **Salida determinista bit a bit** para igual entrada y configuración. |
| CFG | Reducibles e irreducibles. |
| `ub` | Cualquier comportamiento es válido (por ejemplo, `#DE` de `idiv`). |
| Espacio `guest` | Traducción `host = H + (g − vaddr_min)` sobre una reserva contigua que cubre el rango de regiones. `H` lo provee el runtime; el mecanismo para fijarlo es interno del backend ([Q12](../roadmap/open-questions.md)). Sustituir comprobaciones explícitas por faults del host solo se permite si preserva resultado y payload exactos; no en v0.1. |
| Servicios de frontera (lista exhaustiva) | `one_rt_trap(etiqueta, payload)` noreturn; inicialización del espacio guest desde el manifiesto; detección de agotamiento de pila del host → `resource`. No son opacidad computacional. |
| Builds | `exact-state`: la entrada devuelve el estado guest completo para comparar bajo `π_orig`. `contract`: solo `π_K`. Ambos deben cumplir su relación. |
| Límite declarado | Sin tablas de unwind: debuggers y profilers no pueden desenrollar a través de código generado. |

**Wrapper de entrada RV.** Mapea argumentos System V a `a0`–`a5` según §4; fija `sp` al tope de pila guest, `ra = cont = R` y los demás registros a 0 (refinamiento del no determinismo); devuelve `a0` (y `a1`).

## 4. Binding de contratos

Las firmas de contrato ([VAL-004 §2](../validation/o1-protocol.md)) usan como máximo 6 parámetros.

| Tipo de contrato | C | RV64 LP64 | x86-64 System V (wrapper) |
|---|---|---|---|
| `i8`, `i16`, `i32` | `intN_t` | registro extendido con signo a 64 | extiende con signo desde el ancho declarado; no confía en bits altos |
| `u8`, `u16` | `uintN_t` | registro extendido con cero a 64 | extiende con cero desde el ancho declarado |
| `u32` | `uint32_t` | **extendido con signo desde el bit 31** (regla psABI) | extiende con cero; el wrapper RV reextiende según LP64 |
| `i64`, `u64` | `int64_t`, `uint64_t` | registro completo | registro completo |
| `region<L, n>` | `L*` hacia `n` elementos de layout `L` | dirección guest de la región colocada por el harness | puntero host (C) o dirección guest (RV) |

Los retornos se comparan en el ancho declarado.
