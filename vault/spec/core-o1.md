---
id: SPEC-002
kind: spec
status: designed
version: 0.1
---
# Contrato Core-O1

Semántica del core ejecutable de O1 decidido en [ADR-005](../decisions/ADR-005-core-o1-representation.md). Es el join de O1 en el sentido de [ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md): todo lo legal aquí tiene semántica independiente del origen. Las relaciones y la noción de `ub` son las de [SPEC-001](semantics.md).

Estado `designed`: define qué sería una implementación correcta; no existe ninguna.

## 1. Alcance

- **Dentro**: legalidad en el join de O1 (`J_O1`), semántica de operaciones, verificador, canonicalización, contratos de pases post-join, intérprete de referencia, restricciones de extensión.
- **Fuera**: representaciones previas al join (internas a cada frontend), representación máquina interna del backend, sintaxis textual y serialización.

## 2. Meta-modelo

- **Módulo**: funciones, globales, declaraciones de espacios de memoria, conjunto declarado de etiquetas de trap con tipos de payload.
- **Función**: firma `(iN…) → (iN…)` (múltiples resultados permitidos), una región de cuerpo.
- **Región**: tipo declarado. En O1 el único tipo legal es `cfg`: lista de bloques con bloque de entrada.
- **Bloque**: parámetros tipados, operaciones, un terminador.
- **Operación**: opcode, operandos, resultados, atributos semánticos, hechos, regiones propias (ninguna en O1) y atributos de procedencia en un espacio borrable.

## 3. Tipos

`iN` con `N ∈ {1, 8, 16, 32, 64}` legal en `J_O1`. El meta-modelo admite cualquier `N ≥ 1`; otros anchos son ilegales en O1. La signedness no pertenece al tipo: la llevan las operaciones.

## 4. Espacios de memoria

Un espacio es un conjunto de bytes direccionados por `i64`, little-endian. **Espacios distintos nunca se solapan.** Cada operación de memoria nombra su espacio estáticamente.

| Espacio | Contenido | Accesibilidad |
|---|---|---|
| `native` | Slots, globales y regiones aportadas por el llamador (harness). | Bytes de objetos vivos: globales, slots de activaciones vivas, regiones de entrada. Escritura prohibida en globales `const`. |
| `guest` | Mapa de memoria de la imagen RV64IM-O1, declarado en el módulo como regiones `{vaddr, size, perms ⊆ {R,W,X}, bytes iniciales}`. | Lectura: región con `R`. Escritura: región con `W`. Todos los bytes mapeados tienen valor definido. |

La traducción de direcciones de un espacio a memoria del host es responsabilidad del backend ([SPEC-003 §3](o1-profiles.md)) y no forma parte de la semántica.

## 5. Operaciones

Semántica de bitvectors en complemento a dos, alineada con SMT-LIB `QF_BV`. `MIN = −2^(N−1)`. Una precondición falsa produce `ub` en ese punto.

| Operación | Resultado | Precondición | Hechos admitidos |
|---|---|---|---|
| `const<N>(c)` | `c` | — | — |
| `add`, `sub`, `mul` | `(a op b) mod 2^N` | — | `nsw`, `nuw` |
| `udiv`, `urem` | cociente y resto sin signo | `b ≠ 0` | — |
| `sdiv`, `srem` | truncamiento hacia cero; el resto toma el signo del dividendo | `b ≠ 0 ∧ ¬(a = MIN ∧ b = −1)` | — |
| `mulh_uu`, `mulh_ss` | bits `[2N−1 : N]` de `zext(a)·zext(b)` o de `sext(a)·sext(b)` | — | — |
| `and`, `or`, `xor` | bit a bit | — | — |
| `shl`, `lshr`, `ashr` | desplazamiento | `b <u N` | `nsw`, `nuw` solo en `shl` |
| `icmp<p>` → `i1` | `p ∈ {eq, ne, ult, ule, ugt, uge, slt, sle, sgt, sge}` | — | — |
| `zext<M>`, `sext<M>` (`M > N`), `trunc<M>` (`M < N`) | extensión o truncamiento | — | — |
| `select(c: i1, a, b)` | `c ? a : b` | — | — |
| `load<s, W>(p: i64)` → `i(8W)`, `W ∈ {1,2,4,8}` | bytes `[p, p+W)` de `s`, little-endian | bytes legibles en `s`; en `native`, escritos antes si pertenecen a un slot | — |
| `store<s, W>(p: i64, v: i(8W))` | escribe bytes `[p, p+W)` | bytes escribibles en `s` | — |
| `slot(size, align)` → `i64` | dirección en `native` alineada, de bytes frescos y disjuntos de toda memoria viva; vive hasta el retorno de la activación | — | — |
| `global_addr(@g)` → `i64` | dirección de `@g` en `native` | — | — |
| `call @f(args)` → `(results)` | ejecuta `@f` | las de las operaciones que ejecute `@f` | — |

Semántica de los hechos: `add nsw` exige que la suma con signo sea representable en `N` bits; `nuw`, la suma sin signo. Igual para `sub` y `mul`. `shl nsw` exige `ashr(shl(a,b),b) = a`; `shl nuw` exige `lshr(shl(a,b),b) = a`.

La multiplicación alta mixta (`MULHSU` de RISC-V) no es operación: se expresa con `mulh_uu`, `select` y `sub`. Una operación entra en el core solo si no es expresable, o si expresarla ocultaría un patrón que el target implementa con una instrucción.

## 6. Terminadores y llamadas

- `br ^b(args)`
- `cond_br %c: i1, ^t(args), ^f(args)`
- `return(values)`: tipos iguales a la firma.
- `trap #k(payload)`: etiqueta del conjunto declarado; payload con los tipos declarados para `#k`. **Ningún pase interpreta etiquetas**: dos traps con distinta etiqueta son observaciones distintas y no se fusionan.

Solo hay llamadas directas. La recursión está permitida. El agotamiento de recursos del host produce `resource` (SPEC-001).

## 7. Interfaces semánticas y efectos

Los pases consultan interfaces, no listas de opcodes, siempre que la interfaz baste.

| Interfaz | Operaciones O1 |
|---|---|
| `pure`: sin efectos ni precondición | `const`, `add`/`sub`/`mul` sin hechos, `mulh_*`, bit a bit, `icmp`, extensiones, `select`, `global_addr` |
| `partial`: precondición, sin efectos | `udiv`, `urem`, `sdiv`, `srem`, shifts, operaciones con hechos |
| `effects` | `load`: `read(s)`; `store`: `write(s)`; `slot`: `alloc(native)`; `call`: resumen de `@f` |
| `commutative` | `add`, `mul`, `and`, `or`, `xor`, `mulh_uu`, `mulh_ss`, `icmp eq/ne` |
| `terminator` | sucesores y argumentos |

**Resumen de efectos** de una función: espacios leídos y escritos, rangos de direcciones cuando se conocen, `alloc`, y si puede terminar en trap o `ub`. Se calcula sobre el módulo con punto fijo para recursión. Una llamada sin resumen se trata como lectura y escritura de todos los espacios con posible trap. Los recursos son nombrados (hoy, espacios) para admitir recursos futuros (§12).

## 8. Invariantes del verificador

| ID | Invariante |
|---|---|
| V1 | Cada bloque termina en exactamente un terminador y no contiene otro. |
| V2 | Cada valor se define una vez; toda uso está dominado por su definición. Los parámetros de bloque dominan su bloque. |
| V3 | Los argumentos de sucesor coinciden en número y tipo con los parámetros del bloque destino. |
| V4 | Operandos y resultados cumplen la tabla §5; anchos en el conjunto legal. |
| V5 | Las operaciones de memoria nombran un espacio declarado; `slot` y `global_addr` solo en `native`; `W ∈ {1,2,4,8}`. |
| V6 | Los hechos aparecen solo en operaciones que los admiten. |
| V7 | Los destinos de `call` existen y argumentos y resultados coinciden con su firma. |
| V8 | El bloque de entrada no tiene predecesores y sus parámetros son los de la función. |
| V9 | Ninguna operación fuera de §5–§6 en `J_O1`: no hay operaciones opacas. La procedencia solo aparece en el espacio borrable. |
| V10 | Las etiquetas de trap y los tipos de payload pertenecen al conjunto declarado. |
| V11 | Los inicializadores de globales y de regiones guest tienen tamaño exacto; ninguna región guest es `W` y `X` a la vez. |
| V12 | Solo existen regiones de tipo `cfg`. |

El verificador se ejecuta tras cada frontend y cada pase en modos debug y test. Un fallo del verificador es un fallo de corrección de la última transformación.

## 9. Canonicalización

**Política.** Reescrituras locales, deterministas y terminantes, separadas de las decisiones de coste del backend. No se afirma forma normal única: se reduce varianza representacional, no se prueba equivalencia.

**Requisitos por regla.**

1. Condiciones laterales explícitas sobre anchos, hechos y precondiciones. Una regla no introduce `ub` en caminos que no lo tenían, y la transferencia de hechos está probada.
2. Prueba acotada en `QF_BV` para cada ancho legal. Si el solver devuelve `unknown` o timeout en algún ancho, la regla se marca, se respalda con pruebas exhaustivas en anchos pequeños y diferenciales, y **no recibe crédito de convergencia** hasta tener prueba.
3. El conjunto de reglas está versionado y tiene una medida de terminación declarada. En debug, superar el combustible de reescritura es un bug.
4. Cada ejecución registra qué reglas dispararon. El origen de la ejecución lo conoce el harness, no el IR.

**Canonicalizaciones mínimas exigidas** (la lista concreta de reglas se versiona con la implementación):

- orden estable de operandos conmutativos por rango de valor; constantes a la derecha;
- `sub(x, c)` → `add(x, −c)`, descartando `nsw`/`nuw` salvo prueba;
- predicados de `icmp` reducidos a `{eq, ne, ult, ule, slt, sle}` intercambiando operandos;
- `xor(icmp p, 1)` → `icmp ¬p`; `cond_br` sobre condición negada → intercambio de sucesores; `cond_br` sobre constante → `br`;
- plegado de cadenas `zext`/`sext`/`trunc`;
- `mul(x, 2^k)` → `shl(x, k)` con transferencia de hechos probada;
- identidades (`add x 0`, `and x −1`, `or x 0`, `select c a a`) y fusión de argumentos de bloque idénticos.

## 10. Contratos de pase

### 10.1 Esquema

| Campo | Contenido |
|---|---|
| Identidad | Nombre y versión. |
| Etapas | Legalidad de entrada y de salida. |
| Análisis | Requeridos, preservados, invalidados. |
| Relación | Refinamiento bajo `π_orig` (SPEC-001 §4). |
| Hechos | Consumidos; introducidos, con justificación; descartados. |
| Especulación | Si mueve o duplica operaciones, cómo cumple F4. |
| Terminación | Argumento. |
| Validación | SMT local, diferencial con intérprete, casos negativos. |
| Negativos obligatorios | Transformaciones inseguras que debe rechazar, cada una con test. |
| Origin-blindness | Obligatoria post-join. |
| Clase de evidencia | `baja`, `media` o `alta`: determina el crédito T2 (VAL-003 §4). |

### 10.2 Conjunto requerido en O1

| Pase | Clase | Contenido mínimo | Negativos obligatorios |
|---|---|---|---|
| SCCP | media | Constantes y alcanzabilidad conjuntas sobre CFG con argumentos de bloque. | No pliega a un trap una operación con precondición violada. No elimina una guarda de trap cuya condición no es constante. |
| GVN/CSE | alta | Numeración global de valores sobre operaciones `pure` y `partial` con dominancia; cargas equivalentes sin escrituras intermedias según efectos. Al fusionar, el superviviente conserva la intersección de hechos. | Cargas separadas por un `store` posiblemente solapado; operaciones con hechos distintos fusionadas sin intersección. |
| Memoria | alta | Reenvío `store` → `load` y eliminación de `store` muerto, con resúmenes de efectos, disjunción entre espacios, frescura de slots y rangos probados. | `store` a dirección desconocida del mismo espacio; llamada sin resumen; carga de slot tras el retorno de su activación. |
| LICM | alta | Extracción de operaciones `pure`. Operaciones `partial`, hechos y cargas solo cumpliendo F4. | Carga en un bucle que puede ejecutar cero iteraciones; división guardada dentro del bucle; hecho `nsw` conservado al especular. |

**Infraestructura, sin crédito T2**: DCE, simplificación de CFG, plegado local, cálculo de resúmenes de efectos, inlining, eliminación interprocedural de argumentos y resultados muertos.

## 11. Intérprete de referencia

- Implementa §3–§7 literalmente, sin optimizaciones que alteren observaciones.
- Detecta toda violación de precondición y reporta `ub` con ubicación: es el oráculo de `ub` a nivel de core.
- Modela `native` con objetos, slots y tiempos de vida; `guest` con el mapa de regiones.
- Es determinista y tiene combustible configurable (`timeout`).
- Expone conteos de operaciones ejecutadas por clase para VAL-003 §3.
- **No comparte implementación semántica con el backend.** Puede compartir estructuras de datos del IR (T0). Si ambos derivan de las mismas tablas semánticas, el diferencial backend/intérprete deja de ser independiente y se declara.

## 12. Restricciones de extensión

O1 no diseña dominios futuros. Solo tiene prohibido cerrarles el paso de forma barata de evitar. Cada restricción tiene coste de implementación en O1 cercano a cero.

| ID | Restricción | Suposición prohibida en O1 |
|---|---|---|
| E1 | Las regiones tienen tipo declarado y los pases declaran qué tipos aceptan. | “Toda región es un CFG secuencial.” |
| E2 | Añadir tipos de valor (vector fijo o escalable, complejo, punto fijo, tensor) no exige modificar pases que no los consumen. Un pase ante un tipo desconocido es conservador o rechaza explícitamente. | “Todo valor es un escalar o un vector nativo del host.” |
| E3 | Los espacios de memoria son operando estático de primera clase (O1 ya usa dos). | “Existe una única memoria.” |
| E4 | Los efectos se describen por recursos nombrados; recursos futuros (canales, estado de retardo, dispositivos) son añadibles. | “Un bit de efectos laterales basta.” |
| E5 | El orden de ejecución es semántico solo donde los efectos lo imponen. | “El orden de instrucciones codifica tiempo o planificación.” |
| E6 | Cada familia aritmética (saturación, redondeo, punto fijo) es una operación propia, nunca un modo global. | “La aritmética es siempre modular o siempre IEEE.” |
| E7 | El meta-modelo no impide estado persistente entre invocaciones declarado como recurso. | “La unidad de ejecución es una función invocada una vez.” |

## 13. Semántica diferida

Fuera de Core-O1 y sin decidir: vectores; coma flotante y entorno FP; punto fijo y saturación; complejos; streams, tasas y tiempo; tensores y formas; concurrencia, atomicidad y memoria relajada; `volatile` y E/S de dispositivos; excepciones y unwinding; llamadas indirectas; `switch`/jump tables como operación; procedencia en el core; regiones no-CFG.

## 14. Versionado

Esta es **Core-O1 v0.1**. Cualquier cambio en §3–§8 incrementa la versión. Toda evidencia de O1 cita la versión bajo la que se obtuvo.
