---
id: ROAD-003
kind: roadmap
status: open
---
# Preguntas abiertas

1. ¿Rust, C++, Zig u otra base para el core? No decidir por moda; medir necesidades de compiler/runtime/FFI/unsafe/control.
2. ¿SSA clásico, graph IR, region-based IR o combinación?
3. ¿Cuántos niveles/dialectos necesita ONE antes de que la extensibilidad se convierta en fragmentación?
4. ¿Cómo representar efectos, aliasing y memory spaces de forma común sin imponer semántica falsa?
5. ¿Cómo representar streams y dataflow junto a control flow convencional?
6. ¿Qué semántica guest debe permanecer explícita para DBT y qué puede lowering compartir con código normal?
7. ¿Cómo medir objetivamente “infraestructura compartida” y evitar contar utilidades triviales?
8. ¿Qué optimización cross-domain será la primera prueba material de la tesis?
9. ¿Qué backend después de x86 maximiza información: AArch64, RISC-V o WASM?
10. ¿Cuál es el primer workload DSP suficientemente real pero acotado?
11. ¿ONE necesita un lenguaje propio o C es suficiente durante mucho tiempo?
12. ¿Qué partes de numerics deben ser propias para que la comparación técnica sea significativa?
13. ¿Qué codec/pipeline permite demostrar originalidad sin convertir media en un proyecto aislado?
14. ¿Qué SDR/hardware es accesible para una prueba física seria?
15. ¿Cómo evitar que tooling/debug metadata vuelva pesado el runtime mínimo?
16. ¿Qué parte de MLIR/TCG es prior art que debemos adoptar conceptualmente y dónde está la oportunidad verdaderamente nueva?
17. ¿Cuál será la primera afirmación técnica que un especialista externo podría intentar falsar?
18. ¿Cuándo tiene sentido bootear Linux y cuándo solo añade espectáculo sin información nueva?
19. ¿Cómo fijar los benchmarks comparativos finales sin diseñarlos retrospectivamente para ganar?
20. ¿Qué resultado nos obligaría a abandonar o rediseñar la hipótesis unificadora en vez de seguir añadiendo excepciones?
