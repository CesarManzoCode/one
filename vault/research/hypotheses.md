---
id: RES-001
kind: research
status: hypothesis
---
# Hipótesis fundacionales

## H1 — Convergencia útil

Dominios diferentes pueden converger hacia representaciones comunes sin perder las oportunidades de optimización que hacen competitivos a sus toolchains especializados.

**Falsación:** los dominios requieren bypasses o pipelines independientes hasta tan abajo que la capa común aporta valor trivial.

## H2 — Reutilización transversal

Una optimización escrita una vez puede beneficiar de forma material workloads provenientes de más de un dominio.

Ejemplo ideal: una mejora de vectorización nacida en media acelera también DSP y parte de DBT.

**Falsación:** las optimizaciones comunes son demasiado genéricas y las mejoras importantes siguen siendo casi totalmente específicas.

## H3 — Backend multiplicador

Añadir un backend/hardware nuevo una vez habilita materialmente múltiples familias de cómputo.

**Falsación:** cada dominio necesita tanto trabajo específico para X que no existe multiplicación real.

## H4 — Generalidad compacta

Es posible ofrecer una superficie enorme sin que los despliegues individuales paguen proporcionalmente en tamaño, startup o memoria.

**Falsación:** la arquitectura obliga a arrastrar infraestructura universal incluso en tareas simples.

## H5 — Densidad competitiva

Una arquitectura común puede reducir duplicación suficiente para competir en complejidad/footprint con sistemas mucho más especializados.

**Falsación:** ONE termina siendo inevitablemente mucho más complejo que la suma práctica de soluciones especializadas equivalentes.

## H6 — Nueva ventaja arquitectónica

La unificación permite al menos una capacidad o clase de optimización difícil de obtener cuando compiler, DBT, DSP, media y ML viven en ecosistemas separados.

**Falsación:** ONE solo reproduce capacidades existentes detrás de una interfaz común.

## H7 — Extreme cross-domain breadth in one coherent system

Un único proyecto puede demostrar profundidad extrema en varias familias técnicas distintas sin convertirse en un collage.

**Falsación:** la única forma de cubrir la superficie es implementar proyectos esencialmente independientes.
