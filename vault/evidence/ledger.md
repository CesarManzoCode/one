---
id: EVI-LEDGER-001
kind: evidence
status: accepted
---
# Ledger de evidencia

Único lugar donde vive evidencia observada de ONE. El esquema es `accepted`; las entradas son `observed`.

> **Entradas: ninguna.** A 2026-09-14 ONE no tiene implementación significativa ni resultados experimentales. Ningún documento del vault puede citar evidencia de ONE que no esté aquí.

## Reglas

1. Una entrada registra una observación bajo un protocolo, no una conclusión general. La interpretación se limita a los claims y al alcance citados.
2. Resultados positivos, negativos, inconclusos e inválidos tienen el mismo estándar de registro.
3. Una entrada no se borra ni se edita en sustancia. Si se descubre un error, una entrada posterior de tipo `invalidation` la invalida y explica por qué.
4. Fallos, `unknown`, timeouts, `unsupported`, `resource`, rechazos y exclusiones aparecen con sus conteos y permanecen en los denominadores.
5. Variantes de diagnóstico no fieles y pares derivados se marcan como tales en el campo `clase`.

## Esquema de entrada

| Campo | Contenido |
|---|---|
| `id` | `EV-AAAA-NNN` |
| `fecha` | Fecha de ejecución. |
| `tipo` | `correctness` · `convergence` · `reuse` · `opacity` · `closure` · `performance` · `complexity` · `derivation-check` · `invalidation` |
| `clase` | `headline` · `secondary` (pares derivados) · `diagnostic` (variantes no fieles) · `exploratory` |
| `claims` | IDs y dirección: `supports` · `refutes` · `inconclusive` · `invalid` |
| `protocolo` | ID, versión y commit de preregistro. |
| `contratos` | Versión del vault y de cada spec/perfil (p. ej. Core-O1 v0.1, RV64IM-O1 v0.1). |
| `código` | Commit de ONE, commit del harness, hash del corpus por partición. |
| `entorno` | Modelo y stepping de CPU, microcode, kernel, SO, estado de SMT/turbo/governor, versiones y hashes de toolchains y oráculos (Clang, GCC, LLVM, Sail, Spike, QEMU, Rellume, linker), flags exactos. |
| `ejecución` | Comandos exactos, semillas, presupuestos consumidos. |
| `entradas` | Contratos o workloads, partición (`dev`, `held-out`, `control`), estrato. |
| `resultados` | Ubicación y hash de datos crudos; agregados con su método. Resultados por workload conservados. |
| `fallos` | Conteos y enlaces a artefactos de fallo. |
| `desviaciones` | Toda desviación del protocolo. |
| `límites` | Qué no cubre la observación. |
| `reproducción` | Pasos mínimos. |

## Artefacto de fallo

Semilla; entrada minimizada; perfil y versión semántica; pipeline de pases con versiones; hashes de binarios; host; comandos; salida esperada y observada; capa responsable (`frontend`, `lowering`, `pass`, `canonicalization`, `backend`, `runtime`, `oracle`, `harness`). Todo contraejemplo minimizado queda como regresión permanente.

## Entradas

Ninguna.
