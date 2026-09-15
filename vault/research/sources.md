---
id: RES-003
kind: research
status: research
---
# Fuentes

Fecha de corte: 2026-09-14. Se listan las fuentes en que se apoyan decisiones, specs o protocolos del vault, agrupadas por lo que sostienen. El ledger completo del research está en su §27.

**Marcas**:

- **[c]**: consultada directamente durante la consolidación (2026-09-14);
- **[r]**: tomada del ledger del research;
- **[b]**: referencia bibliográfica conocida, no consultada en este sprint. Debe verificarse antes de citarse como soporte central.

## Semántica, UB y representación (ADR-004, ADR-005, SPEC-001, SPEC-002)

- [r] LLVM Language Reference Manual — https://llvm.org/docs/LangRef.html
- [r] LLVM Undefined Behavior Manual — https://llvm.org/docs/UndefinedBehavior.html
- [b] Lee, Kim, Song, Hur, Das, Majnemer, Regehr, Lopes. *Taming Undefined Behavior in LLVM*. PLDI 2017.
- [r] MLIR Language Reference — https://mlir.llvm.org/docs/LangRef/
- [r] MLIR Rationale — https://mlir.llvm.org/docs/Rationale/Rationale/
- [r] MLIR Dialect Conversion — https://mlir.llvm.org/docs/DialectConversion/
- [r] Lattner et al. *MLIR: Scaling Compiler Infrastructure for Domain Specific Computation*. CGO 2021.
- [r] LLVM MemorySSA — https://llvm.org/docs/MemorySSA.html
- [c] V8. *Land ahoy: leaving the Sea of Nodes* (2025-03-25) — https://v8.dev/blog/leaving-the-sea-of-nodes
- [r] Willsey et al. *egg: Fast and Extensible Equality Saturation*. POPL 2021 — https://arxiv.org/abs/2004.03082
- [b] WebAssembly Core Specification — https://webassembly.github.io/spec/core/

## C (SPEC-003 §1)

- [r] ISO WG14 N3096, ISO/IEC 9899:2023 working draft — https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf
- [r] ISO WG14 N2676, provenance-aware memory object model — https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2676.pdf
- [r] Cerberus — https://github.com/rems-project/cerberus
- [r] CompCert — https://compcert.org/doc/

## RISC-V (SPEC-003 §2)

- [r] RISC-V Unprivileged ISA, release 20260120 — https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html
- [r] RISC-V ABIs Specification (psABI) — https://riscv-non-isa.github.io/riscv-elf-psabi-doc/
- [r] Sail RISC-V model — https://github.com/riscv/sail-riscv
- [b] Spike RISC-V ISA simulator — https://github.com/riscv-software-src/riscv-isa-sim
- [r] riscv-arch-test — https://github.com/riscv/riscv-arch-test
- [r] riscv-dv — https://github.com/chipsalliance/riscv-dv

## x86-64 y backend (SPEC-003 §3)

- [b] System V AMD64 psABI — https://gitlab.com/x86-psABIs/x86-64-ABI
- [r] ELF gABI — https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html
- [r] LLVM Target-Independent Code Generator — https://llvm.org/docs/CodeGenerator.html
- [r] Fallin, Cranelift ISLE (2023) y corrección en asignación de registros (2021) — https://cfallin.org/blog/

## Lifting, DBT y composición rival (ADR-006, VAL-004 §11)

- [c] Rellume: “x86-64/AArch64/RISC-V64 machine code to LLVM IR” — https://github.com/aengelke/rellume
- [c] Remill; arquitecturas listadas sin RISC-V — https://github.com/lifting-bits/remill
- [b] Engelke, Schulz. *Instrew: Leveraging LLVM for High Performance Dynamic Binary Instrumentation*. VEE 2020.
- [r] QEMU Translator Internals — https://www.qemu.org/docs/master/devel/tcg.html
- [r] QEMU TCG IR — https://www.qemu.org/docs/master/devel/tcg-ops.html
- [r] Bellard. *QEMU, a Fast and Portable Dynamic Translator*. USENIX ATC 2005.
- [r] rev.ng, ICCST 2018 — https://rev.ng/downloads/iccst-18-paper.pdf
- [r] BAP, CAV 2011 — https://edmcman.github.io/pres/cav11.pdf
- [b] TinyCC — https://bellard.org/tcc/

## Verificación y generación de pruebas (VAL-004 §7)

- [r] Lopes et al. *Alive2: Bounded Translation Validation for LLVM*. PLDI 2021.
- [r] Yang et al. *Finding and Understanding Bugs in C Compilers* (Csmith). PLDI 2011.
- [r] YARPGen — https://github.com/intel/yarpgen

## Método experimental (VAL-003, VAL-004)

- [r] SPEC CPU 2017 Run and Reporting Rules — https://www.spec.org/cpu2017/Docs/runrules.html
- [r] LLVM Benchmarking Tips — https://llvm.org/docs/Benchmarking.html

## Presión de dominios futuros (SPEC-002 §12, EXP-02)

- [r] Lee, Messerschmitt. *Synchronous Data Flow*. Proc. IEEE 1987.
- [r] StreamIt — https://groups.csail.mit.edu/cag/streamit/
- [r] Apache TVM architecture — https://tvm.apache.org/docs/arch/index.html
- [r] Halide — https://halide-lang.org/
- [r] Triton — https://triton-lang.org/main/index.html
- [r] StableHLO specification — https://openxla.org/stablehlo/spec

## Regla de investigación

Preferir especificaciones, documentación primaria, papers originales y código fuente. Blogs y comparativas de terceros pueden orientar búsquedas, pero no sostienen una afirmación central cuando existe fuente primaria. Una fuente marcada **[b]** no sostiene sola una decisión.
