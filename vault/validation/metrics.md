---
id: VAL-003
kind: validation
status: designed
version: 0.1
---
# Métricas: corrección, convergencia, reutilización, opacidad, closure, complejidad y rendimiento

Definiciones independientes de campaña. Los umbrales pertenecen a cada protocolo; para O1, [VAL-004](o1-protocol.md).

## 1. Principios

1. **Vectores, no puntuaciones compuestas.** Agregar dimensiones con pesos elegidos permite fabricar el resultado. No existe “porcentaje compartido” ni “score de complejidad”.
2. LOC y tokens son diagnóstico de procedencia, nunca titular.
3. Cada métrica declara unidad, fuente de datos, manipulación conocida y contramedida.
4. Toda métrica de convergencia se calibra con controles positivos y negativos antes de interpretarse.
5. El origen de una ejecución lo conoce el harness, nunca el IR. La medición por origen no introduce procedencia en el pipeline.

## 2. Corrección

Por capa (VAL-004 §7): pasadas, fallos, `unknown`, `unsupported`, `resource`, rechazos; presupuesto de fuzzing consumido; contraejemplos minimizados únicos; reglas de canonicalización con prueba, con `unknown` y sin prueba.

## 3. Convergencia representacional

| ID | Definición | Manipulación conocida | Contramedida |
|---|---|---|---|
| **CV1** Solapamiento dinámico de clases | `Σ_c min(p_A(c), p_B(c))`, donde `p_X` es la distribución normalizada de operaciones ejecutadas por el intérprete Core-O1 sobre `Pre(K)`, y la clase `c` = opcode × ancho, sin hechos. | Canonicalizar todo a pocas clases. | N2 debe distinguir contratos; exclusividad reportada. |
| **CV2** Distancia estructural | Distancia de edición de grafo normalizada entre CFG canonicalizados tras alfa-renombrado. Primero se comprueba isomorfismo exacto; la distancia es acotada y se declara su aproximación. | Ajustar la canonicalización a held-out. | Partición sellada. |
| **CV3** Clase de código máquina | `idéntico` · `isomorfo` (módulo renombrado de registros y orden de bloques) · `igual coste` (mismas instrucciones ejecutadas) · `solo conductual`. | — | — |
| **CV4** Fracción no explicada | Con `D0` = CV2 fiel y `D_A` = CV2 con ablaciones A1–A4: `U = (D_A − D_P1) / (D_N1 − D_P1)`, calibrada con las distancias medias de los controles. | Declarar residuos para ocultar fallos de canonicalización. | Solo cuentan como explicadas las clases con ablación mecánica (SPEC-001 §9). |
| **CV5** Exclusividad | Fracción del conteo dinámico de operaciones en clases emitidas por un solo origen en el corpus. | — | Justificación semántica por clase. |

## 4. Reutilización material

Niveles T0/T1/T2 y condiciones M1–M4 de [ADR-004](../decisions/ADR-004-semantic-discharge-convergence.md).

| ID | Métrica | Definición |
|---|---|---|
| R1 | Solapamiento semántico | CV1 agregado por estrato. |
| R2 | Reutilización de conocimiento | Por pase y regla T2: disparos por origen, workloads transformados por origen y beneficio de ablación por origen (instrucciones deterministas). Clasificación: `dual-beneficioso`, `mono-origen`, `inerte`. Solo los pases de clase `media` o `alta` (SPEC-002 §10) cuentan para H2. |
| R3 | Reutilización de contratos | Definiciones semánticas, invariantes del verificador y pruebas SMT de reglas consumidas sin cambio por ambos orígenes. |
| R4 | Reutilización de backend | Fracción de reglas de legalización y selección ejercitadas dinámicamente por ambos orígenes, ponderada por instrucciones emitidas. |
| R5 | Origin-blindness | Resultado de las pruebas de SPEC-001 §6 (binario) y conteo de ramas keyed por origen: post-join, debe ser 0; pre-join, se reporta. |
| R6 | Opacidad | §5. |
| R7 | Coste marginal de integración | Componentes exclusivos del origen en el grafo de capabilities: conceptos semánticos introducidos (operaciones, tipos, hechos, etiquetas) y análisis propios que duplican un mecanismo del core. Tamaño como diagnóstico. |
| R8 | Propagación | Longitudinal: correcciones u optimizaciones en componentes T1/T2 que afectan a varios orígenes sin parches paralelos, frente a las que requieren parches por origen. No es gate en O1. |

**Regla de crédito.** Un framework genérico de 1 000 líneas ejercitado por un solo origen cuenta menos que una regla semántica de 20 líneas con beneficio validado en ambos. Un pase con reglas internas seleccionadas por origen se cuenta como dos pases mono-origen.

## 5. Dependencia de origen y opacidad

- **Dependencia de origen**: un mecanismo post-join depende del origen si su salida sobre un programa legal cambia por algo distinto del contenido semántico del programa, el target y la configuración. Se mide con la prueba de borrado, la configuración única y la auditoría estática.
- **Operación opaca**: operación cuya semántica en el join no está definida por el contrato del core más allá de un resumen de efectos (helpers, intrínsecos, llamadas a código no core).
  - Opacidad estática = operaciones opacas / operaciones en el join.
  - Opacidad dinámica = instrucciones ejecutadas dentro de código opaco / instrucciones totales.
  - Los **servicios de frontera** (salida por trap, inicialización de memoria) se enumeran exhaustivamente en el perfil y se reportan aparte; no son opacidad computacional.

## 6. Capability closure

**Nodo del grafo de capabilities** ([ARC-005](../architecture/modularity-deployment.md)):

| Campo | Contenido |
|---|---|
| `id` | Nombre. |
| `provides` | Operaciones, tipos, pases o servicios. |
| `kind` | `compiler` · `runtime` · `test`. |
| `requires` | Dependencias duras. |
| `optional` | Dependencias opcionales. |
| `roots` | Registros, inicializadores estáticos y raíces del linker. |
| `targets` | Targets soportados. |

**Closure**: cierre transitivo derivado, nunca mantenido a mano. Los perfiles de artefacto son closures derivadas.

**Mediciones por artefacto**:

- tamaño stripped y de segmentos cargables;
- dependencias dinámicas;
- símbolos exportados;
- **mapa de procedencia de símbolos** (símbolo → nodo), que exige una convención de espacios de nombres en la implementación;
- RSS y RSS pico;
- startup de herramientas;
- tiempo de build.

**Coste marginal**: `Δ(A, x) = cost(A ∪ {x}) − cost(A)` medido sobre al menos dos bases `A`. La no aditividad se reporta como hallazgo.

**Gate**: ningún símbolo de un nodo fuera de la closure del artefacto.

## 7. Compresión de complejidad

Vector por capability y por campaña. Se reporta `Δcapacidad / Δvector`. Una capability solo recibe crédito cuando sus gates de corrección e integración pasan.

| Dimensión | Proxy | Señal de fallo |
|---|---|---|
| Conceptos semánticos | Operaciones, tipos, hechos, interfaces, invariantes requeridos | Cada frontend añade conceptos paralelos |
| Superficie de interfaz | APIs públicas y miembros de interfaces del IR | Crecimiento superlineal con dominios |
| Dependencias | Nodos, aristas, ciclos, hubs; **dependencias del core hacia dominios (deben ser 0)** | El core depende de un dominio |
| Duplicación semántica | Reglas, pruebas u optimizaciones reescritas por origen; no clones de tokens | La misma optimización por origen |
| Condicionalidad | Ramas keyed por origen: post-join 0, pre-join reportadas | Cascadas de procedencia |
| Coste de build y despliegue | §6 | Crecimiento del repo infla artefactos mínimos |
| Coste de extensión | Módulos tocados fuera del nodo nuevo al añadir una capability; conceptos añadidos al core | Ediciones multiplicativas |
| Mantenimiento | Acoplamiento de cambios, propagación de defectos (longitudinal) | Un cambio exige reparar dominios no relacionados |

## 8. Rendimiento

- **Primario**: conteo determinista de instrucciones ejecutadas mediante instrumentación. No depende de ruido.
- **Secundario**:
  - ciclos y tiempo de pared en un núcleo aislado, con governor fijo y estado SMT/turbo declarado;
  - calentamiento y distinción frío/caliente en herramientas;
  - número de repeticiones preregistrado;
  - mediana e intervalo bootstrap al 95 %;
  - no se eliminan outliers salvo regla preregistrada, y todas las ejecuciones se conservan.
- Medias geométricas solo sobre ratios de pares con garantías compatibles; resultados por workload siempre publicados.
- Tiempo de compilación por fase y footprint se reportan junto a toda mejora de runtime.

## 9. Anti-gaming

1. Pipeline base fijo para toda la suite; configuraciones específicas (“peak”) etiquetadas aparte.
2. Ninguna identidad de workload es visible para el pipeline (prueba de borrado de identidad, SPEC-001 §6).
3. Particiones held-out selladas; una partición usada queda quemada.
4. Heurísticas ajustables validadas con leave-one-stratum-out.
5. Baselines con garantías equivalentes y flags congelados; esfuerzo de ajuste comparable declarado.
6. Regresiones de compilación y footprint no se ocultan tras mejoras de runtime.
7. Toda sustitución por helper o biblioteca se reporta.
8. Casos no soportados y rechazos permanecen en los denominadores.
9. Workloads negativos y peores casos se conservan.
10. Variantes de diagnóstico no fieles nunca aparecen en tablas de titular.
11. Toda métrica de convergencia requiere controles que la validen en la campaña.
