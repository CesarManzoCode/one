---
id: RES-004
kind: risks
status: open
---
# Riesgos y respuestas obligatorias

Cada riesgo tiene una firma observable, un detector y una respuesta precomprometida. La respuesta a una firma confirmada **no es añadir una excepción** ([gobierno](../governance.md), regla 10): es la acción indicada, normalmente rediseño documentado por ADR.

| ID | Riesgo | Firma observable | Detector | Respuesta obligatoria |
|---|---|---|---|---|
| R1 | Abstracción artificial o core de mínimo común denominador | Operaciones ricas bajan antes de las transformaciones compartidas útiles; solo pases de clase baja tienen beneficio dual. | R2 (VAL-003 §4); C-O1-3; EXP-02 | Mover el join o introducir una interfaz semántica por ADR. |
| R2 | Pérdida semántica temprana | La ablación de hechos o el contrato de olvido muestran optimizaciones perdidas e irrecuperables en el nivel donde se necesitaban. | SPEC-001 §7; ablaciones | Revisar el lowering; reabrir [Q4](../roadmap/open-questions.md) si la causa es la procedencia. |
| R3 | Explosión de dialectos | Pases que enumeran opcodes o dialectos en vez de interfaces; exclusividad (CV5) creciente. | Auditoría; CV5 | Semántica basada en interfaces o abandonar la comunidad afirmada. |
| R4 | Universal tax | Un artefacto mínimo crece con capabilities no relacionadas; `Δ(A, x)` no aditivo sin causa. | G5; VAL-003 §6 | Refactor de dependencias antes de añadir capabilities. |
| R5 | Monorepo Frankenstein | Fracción T1/T2 decreciente; coste de extensión superlineal; dependencias del core hacia dominios. | R2–R8; VAL-003 §7 | Detener expansión de superficie; integrar o retirar el subsistema (ADR-001). |
| R6 | Benchmark gaming | Ganancias que desaparecen en held-out, con otros compiladores o con baselines de garantías equivalentes. | Preregistro; G6; G7 | Invalidar el claim general; reportar. |
| R7 | Reinventar prior art o perder frente a la composición | C-O1-8 negativo; ningún candidato H6. | Registro de claims | Revisar la tesis o producir evidencia diferencial; nunca reclamar novedad por implementación propia. |
| R8 | Complejidad incontrolable | Pendiente del vector de complejidad superior al crecimiento de capacidad acreditada. | VAL-003 §7 | Congelar superficie y reducir conceptos antes de añadir dominio. |
| R9 | Algorítmica como cuello de botella | Media, radio, numerics o compresión dependen de bibliotecas externas en la ruta central o tienen calidad no competitiva. | EXP-06…09; INV-09 | La capacidad no recibe crédito hasta tener resultado algorítmico propio medido. |
| R10 | Utilidad no emergente | Excelencia técnica sin ventaja práctica medible. | Campañas comparativas | Registrar honestamente; no es criterio primario, pero no se oculta. |
| R11 | Falsa convergencia por pares derivados | Alta similaridad solo en pares derivados de compilador. | Detector de derivación (VAL-004 §4) | Excluir del titular; rediseñar el procedimiento si el detector no discrimina. |
| R12 | Contaminación por estado guest | Pases comunes manipulan una estructura de estado u offsets guest; helpers en el join. | G2; CV5; auditoría | Escalarizar el estado; redefinir el join. |
| R13 | Ilusión de nombre compartido | Un pase “compartido” despacha reglas distintas por origen. | M1–M4; disparos por regla y origen | Contarlo como dos pases mono-origen; C-O1-3 refutado si afecta a los pases fuertes. |
| R14 | Éxito por helpers opacos | Corrección que pasa con cómputo escondido en helpers. | G2; opacidad dinámica | Sin crédito de convergencia; ampliar el contrato del core o reducir el perfil por versión previa al preregistro. |
| R15 | Debilitamiento semántico | ONE gana omitiendo traps, garantías de ABI o de alias, o explotando `Pre(K)`. | G6; build `exact-state` fuera de `Pre(K)` | Comparación inválida; defecto de corrección. |
| R16 | Diseño prematuro de dominios futuros | Abstracciones de stream o tensor sin uso dominan O1. | Revisión frente a SPEC-002 §12 | Eliminarlas; conservar solo restricciones E1–E7. |
| R17 | Métrica inválida o indulgente | La métrica no separa P1 de N1. | G8 | Claim `inconclusive`; corregir la métrica con una held-out nueva. |
| R18 | Independencia contaminada por herramientas | Mismo generador o contexto en ambos lados; similaridad estructural sistemática. | Registro de autoría; detector | Estratificar por fuente de autoría; reclasificar pares. |

## Cuándo rediseñar en lugar de parchear

Una abstracción se rediseña, en lugar de extenderse con casos especiales, cuando ocurre cualquiera de:

1. un gate estructural (G2–G5) falla por una construcción admitida por el perfil;
2. la corrección exige ramas por origen después del join;
3. un pase fuerte solo funciona con variantes por origen;
4. la fracción no explicada supera su umbral tras corregir defectos de canonicalización identificados;
5. un dominio nuevo obliga a cambiar la semántica de operaciones existentes en vez de añadir operaciones o interfaces.
