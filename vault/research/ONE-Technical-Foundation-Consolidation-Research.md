---
id: RES-005
kind: research
status: research
snapshot: main@a2f89d4
disposition: research/consolidation-disposition.md
---
# ONE — Technical Foundation Consolidation Research

> **Epistemic status.** This is a research artifact, not an accepted specification or ADR. Every statement is labeled by role: **[ONE fact]**, **[current decision]**, **[hypothesis]**, **[external fact]**, **[research inference]**, **[recommendation]**, or **[open question]**. Recommendations do not become ONE decisions merely by appearing here.

## 1. Executive technical summary

**[ONE fact]** At repository snapshot `main@a2f89d4cf28a3cafc89951861dc44f838d7c7639`, ONE has a coherent founding vault and no significant implementation or experimental evidence. The vault fixes three architectural commitments: one materially shared core, progressive multi-level lowering, and specialized deployments that pay only for their capability closure. It explicitly leaves the representation, exact levels, C/ISA semantics, verification boundary, first nontrivial shared optimization, and objective reuse metrics open.[^S01]

**[research inference]** The thesis is plausible but O1, as currently phrased, can produce a false positive. If the RISC-V input is simply the output of compiling the same C function, convergence may mostly show that a lifter and canonicalizer can erase a compiler's already-made lowering choices. That is useful engineering, but not evidence that two genuinely independent origins share semantics or optimization knowledge. O1 therefore needs two distinct campaigns:

1. **Primary cross-origin campaign:** independently authored C and RISC-V implementations of the same behavioral contracts, generated and reviewed without deriving one from the other.
2. **Secondary round-trip campaign:** C → independent RISC-V compiler → ONE lift, used to test recovery robustness and sensitivity to compiler/version/flags, but excluded from the headline convergence claim.

**[recommendation]** Define O1 as a bounded, user-mode, function-level experiment over little-endian **RV64IM + LP64**, not as a general emulator or full DBT. Admit integer arithmetic, branches, direct calls, stack frames, globals, and sandboxed byte-addressed memory; exclude compressed instructions, FP, atomics, privileged state, MMU, syscalls, signals, threads, and self-modifying code. RV64 aligns pointer width with the first x86-64 host; `M` prevents multiplication/division from becoming artificial helper calls; LP64 is ratified whereas RV64ILP32 remains draft.[^S22][^S23] This is large enough to test state, memory, calls, ABI, lifting, shared optimization, and backend reuse, yet small enough to specify precisely.

**[research inference]** ONE Core must not select one source's semantics as universal semantics. C pointers carry object/lifetime/provenance and undefined-behavior obligations; a machine address is an XLEN-bit value interpreted by an execution environment. Conflating them either makes C optimizations unsound or invents provenance for guest code. The safe convergence boundary is an explicit **semantic discharge point**: source-specific obligations remain in higher representations; only operations whose preconditions and effects have been made explicit enter a shared bitvector/control/memory core.

**[recommendation]** The minimum core should be a typed, SSA-based CFG with block arguments; arbitrary-width bitvectors; explicit loads/stores with width, alignment, endianness, address space, volatility/order, and trap behavior; explicit call/effect summaries; explicit trap/termination outcomes; fixed and scalable extension hooks for vectors; and a region container that does not require every future domain to be CFG-shaped. SSA is a value discipline, not the entire architecture. MLIR demonstrates that operations, regions, traits, interfaces, and dialect conversion can host CFG and graph regions, while LLVM and QEMU show the strength and limits of low-level common IRs.[^S03][^S04][^S08]

**[recommendation]** O1 correctness should be layered:

- executable reference semantics for the accepted C profile, RV64IM subset, ONE Core, and observable harness;
- decoder/lifter differential tests against the official Sail RISC-V model;
- transformation-local refinement checking with bounded SMT where applicable;
- differential execution against Clang/GCC and Spike/QEMU/Sail;
- structure-aware fuzzing, property tests, metamorphic pairs, fixed regression corpora, and reducers;
- backend differential tests against a ONE Core interpreter before performance claims.

Full compiler verification is not required. However, every lowering and optimization must have a declared semantic relation and a validation method. Alive2 shows the practical value—and bounded/interprocedural limits—of per-transformation refinement checking; CompCert shows the stronger reference model of chained semantic preservation.[^S30][^S31]

**[research inference]** “Same optimizer” and “same backend” are necessary but insufficient evidence of integration. A shared utility or pass name can hide origin-conditioned implementations. O1 needs preregistered measurements of: common semantic surface used by both origins; identical transformation contracts/rules; origin-blind code paths after the join; pass applicability and benefit by origin; generated-code delta under ablation; origin-conditioned branches/opaque helpers; shared verification artifacts; and marginal capability cost. LOC is diagnostic only.

**[adversarial conclusion]** MLIR already supplies most generic mechanisms suggested by the current vault: extensible operations/types, multiple coexisting dialects, regions, traits/interfaces, generic rewriting, legality-driven conversion, declarative definitions, and progressive lowering.[^S03][^S05][^S06] QEMU already demonstrates many guests through one TCG IR and multiple hosts, with explicit architectural state, helpers, translation blocks, chaining, exception recovery, and invalidation.[^S08][^S09] LLVM already supplies a reusable SSA optimizer and multi-target machine pipeline.[^S02][^S07] Consequently, ONE cannot claim novelty for a multi-level IR, dialects, guest→IR→host translation, or a shared backend. Its defensible claim must be empirical: materially more cross-family semantic/optimization/backend reuse per unit of complexity and deployment cost than composing existing infrastructures.

## 2. Methodology and source hierarchy

The repository's entire `vault/` tree was read at the snapshot above. Internal claims are reconstructed according to the vault's own precedence rule: explicit purpose → constitution → active decisions → architectural contracts → plans → implementation; evidence may overturn any decision.[^S01]

External evidence was selected in this order: normative specifications; original papers; first-party architecture documentation; source repositories where documentation is incomplete; author technical material. Current-version facts were checked against the live first-party material available at the cutoff. Historical systems are used to recover design rationale, not to infer current feature status.

The investigation uses three tests:

- **semantic test:** what behaviors does a representation preserve, forbid, or leave nondeterministic?
- **reuse test:** what knowledge/mechanism is genuinely shared, rather than merely invoked through a common API?
- **adversarial test:** what observation would show that ONE is a weaker reimplementation, a monorepo collage, or an abstraction with hidden universal tax?

No recommendation below changes the accepted vault state. Where evidence does not discriminate among options, the correct output is an explicit open question plus the experiment needed to resolve it.

## 3. Reconstruction of ONE's current epistemic state

### 3.1 What ONE is and is not

**[current decision]** ONE is one coherent computational system in which domain-specific semantics may remain local but materially shared infrastructure must exist. A subsystem that shares nothing material must justify its membership.[^S01]

**[current decision]** ONE unifies computation, not source objects or meanings. It rejects both a flat universal primitive list that destroys structure early and a collection of unrelated domain runtimes.[^S01]

**[current decision]** Lowering is multi-level and progressive. The number, names, and boundaries of levels are provisional.[^S01]

**[current decision]** Repository capability is not deployed-runtime cost. Footprint, RSS, startup, dependency closure, and marginal capability cost are architectural properties.[^S01]

**[ONE fact]** There is no implementation, chosen implementation language, stable IR syntax, frontend, decoder, optimizer, backend, runtime, benchmark result, or evidence of utility/originality. O0 is documentation-complete; O1 is the proposed first implementation campaign.[^S01]

### 3.2 Hypotheses and invariants

**[hypothesis]** H1–H7 assert useful convergence, transversal optimization reuse, backend multiplication, compact generality, competitive density, a new architectural advantage, and cross-domain breadth without collage. Each has a stated failure mode, but quantitative rejection thresholds do not yet exist.[^S01]

**[current decision]** INV-01–INV-12 protect semantic honesty, delayed lowering, frontend×backend reuse, capability closure, benchmark comparability, no silent tradeoff, dependency honesty, negative evidence, integration over LOC, and evaluation by effective results.[^S01]

### 3.3 Designed but unproved

**[ONE fact]** Domain IR → ONE High → ONE Core → ONE Machine is a tentative decomposition, not an established architecture. The imagined end-to-end media/radio machine is a long-term integration proof, not a product or current capability. The C + RISC-V → x86-64 path is a designed experiment, not evidence.

### 3.4 Explicit open questions

The vault correctly keeps implementation language, IR form, level count, effects/aliasing/memory spaces, streams with control flow, guest-state boundary, reuse metrics, first shared optimization, second backend, DSP workload, numerical ownership, and benchmark policy open. The consolidation should narrow only the questions that block an honest O1.

## 4. Fundamental questions exposed by the research

1. **What is the theorem or observational claim at each edge?** “Preserve semantics” is incomplete without source/target states, admissible inputs, observables, nondeterminism, traps, and refinement direction.
2. **What is the join point?** A file named `ONE Core` is not a convergence boundary. The boundary is where both origins satisfy the same operation semantics and downstream passes no longer consult provenance for correctness.
3. **What information may be forgotten?** Every lowering needs a forgetting contract: information removed, proof/condition that permits removal, and later optimizations thereby made impossible.
4. **What is shared knowledge?** A generic walker is infrastructure; an origin-independent GVN rule with one semantic proof and measured benefit for both origins is shared compiler knowledge. Both matter, but should not be counted alike.
5. **What is O1's unit?** A whole ELF process introduces loader, libc, syscalls, TLS, dynamic linking, signals, and OS semantics before the thesis is tested. A function ABI sandbox is the smallest honest unit.
6. **What does failure mean?** Failure thresholds must be preregistered: excessive opaque helpers, origin-conditioned downstream branches, inability to express memory relations, or unacceptable overhead must trigger redesign, not adapter accumulation.

## 5. Compiler and IR architecture findings

### 5.1 Representation families

| Model | Strength | Cost/risk | Consequence for ONE |
|---|---|---|---|
| SSA + explicit CFG | Mature dominance, sparse dataflow, simple textual form, broad algorithms | CFG restructuring and memory are separate problems; source structure can disappear | Best default for O1 Core, not a universal domain model |
| Sea of nodes / graph IR | Unifies value and control dependencies; flexible scheduling | Harder invariants, mutation, deterministic printing, and phase debugging | Do not choose before an O1 transformation demonstrates a decisive benefit |
| Regions + structured control | Retains loop/branch hierarchy and supports progressive lowering | Canonical forms and region semantics must be defined; arbitrary nesting can fragment passes | Use a region container and interfaces; keep O1 executable core CFG-capable |
| Dataflow graph | Makes dependencies, fusion, rates, and parallelism explicit | Poor fit for unrestricted side effects and irregular control | Preserve as a future region/dialect, never encode prematurely as loads/stores |
| CPS/continuations | Explicit control, calls, exceptions, and transformations | Representation volume and unfamiliar optimization pipeline | Useful conceptual tool for traps/continuations, not justified as O1's base |
| E-graphs | Delays rewrite ordering and compactly represents equal expressions | Saturation/extraction cost, effects and loops are difficult; unguided growth can explode | Restricted pure bitvector islands only; not an O1 architectural foundation[^S18] |

**[external fact]** MLIR operations can own regions; regions may have SSA-CFG or graph semantics; traits and interfaces allow generic transforms without enumerating every operation.[^S03] Its dialect conversion explicitly separates legality, rewrite patterns, and type conversion.[^S06] These are direct answers to ONE's extensibility problem, but MLIR does not supply domain semantics or evidence that the intended domains converge.

**[external fact]** LLVM IR is typed SSA with a precisely consequential UB/poison model; its target pipeline separates IR translation, legalization, register-bank selection, instruction selection, scheduling, register allocation, frame lowering, and emission.[^S02][^S07][^S46] GCC's GIMPLE/SSA and RTL similarly separate language-neutral optimization from machine-oriented representation.[^S10][^S11]

**[recommendation]** Specify four notions independently:

- **container meta-model:** operation, value, block, region, type, attribute, location;
- **semantic interfaces:** purity, memory effects, trapping, commutativity, call behavior, terminator/successor behavior;
- **legalization relation:** which operations/types are legal at each stage and how illegal ones are discharged;
- **canonicality:** terminating local normalizations with explicit phase boundaries, not a claim of a globally unique normal form.

**[recommendation]** Require a verifier after every pass in debug/test modes. Each operation owns a semantic contract; each pass declares accepted invariants, preserved analyses, introduced/removed capabilities, and failure behavior. Metadata that affects legality or behavior is semantics and must not be discardable.

### 5.2 Canonicalization and rewriting

Canonicalization should reduce representational variance, not prove equivalence. Greedy rewrite systems are sensitive to rule ordering; equality saturation explores alternatives but can consume prohibitive memory without guidance.[^S18][^S19] For O1:

- use deterministic, terminating local rewrites for algebraic identities, constant folding, compare normalization, branch normalization, and explicit state scalarization;
- separate semantic rewrites from target cost-based selection;
- give every rule side conditions over bit width, poison/undefinedness, traps, memory effects, and overflow;
- version rule sets and record which rules fired by origin;
- reserve bounded SMT/e-graphs for pure expression islands and equivalence diagnosis.

## 6. C semantics findings

**[external fact]** C's abstract-machine behavior includes implementation-defined choices, unspecified behavior, and undefined behavior; pointer validity depends on objects, lifetimes, bounds, alignment, effective types, and increasingly explicit provenance research.[^S20][^S21] LLVM's poison/undef model is not C semantics and cannot be copied casually.[^S47]

### 6.1 Defensible O1 C profile

**[recommendation]** Define a named profile, for example `ONE-C-O1`, as a strict freestanding subset:

- scalar `bool`, exact-width signed/unsigned integers up to 64 bits; structs only if layout is explicitly fixed;
- functions, locals, globals, conditionals, loops, direct calls, arrays, and pointers into declared live objects;
- two's-complement, 8-bit bytes, little-endian, fixed widths and alignments, LP64 data model;
- unsigned wrap; signed overflow, division by zero, invalid shift counts, out-of-bounds access, misalignment where forbidden, invalid pointer arithmetic, and uninitialized reads rejected or modeled explicitly before Core;
- no floating point, atomics, threads, varargs, VLAs, unions/type punning, `setjmp`, signals, inline assembly, function-pointer calls, dynamic allocation, or hosted library dependency;
- `volatile` excluded from equivalence workloads in O1; if parser support exists, lower it to explicit non-removable ordered I/O-like effects, never an ordinary load/store.

This is not “C” without qualification. Every result must name the profile and implementation environment.

### 6.2 Pointers, provenance, and memory

**[recommendation]** Use distinct high-level entities:

- `c.ref<object, offset, bounds/provenance>` for source reasoning;
- `guest.addr<i64, space>` for ISA addresses;
- `core.addr<space>` only after a lowering records the relation and obligations that permit convergence.

Do not represent a C pointer as an unqualified `i64` at parse time. Do not attach origin only as optional metadata. Provenance and lifetime affect valid transformations and therefore remain semantic until discharged. Conversely, guest addresses should not acquire fictitious C object identity.

### 6.3 Avoiding false C↔binary comparison

Use a contract language independent of both frontends: typed inputs, initial object graph, readable/writable regions, alias relation, allowed outcomes, final scalar results, final memory projection, and trap/termination policy. Authors implement this contract separately in `ONE-C-O1` and hand-written RV64IM assembly. Generation should be order-randomized and reviewed for accidental structural cloning.

The C side should be UB-free under the fixed profile. Then observational equivalence can be symmetric for deterministic terminating cases. If later C nondeterminism/UB is admitted, the correct relation is refinement: the machine behavior must belong to the allowed source behaviors, not text/graph equality.

## 7. RISC-V, DBT, and lifting findings

### 7.1 O1 surface

**[recommendation]** RV64IM, little-endian, U-mode computational semantics, LP64 function ABI, static sandbox memory. Include base loads/stores, word and XLEN arithmetic, compares, direct/conditional jumps, `JAL/JALR` under constrained targets, and M arithmetic. Treat x0 and PC semantics explicitly. Support integer register calling convention, 16-byte stack alignment, callee-saved registers, and a declared clobber set.[^S23]

Accept raw function images plus a small manifest initially; optionally admit a deliberately tiny ET_REL ELF subset only after the raw path is correct. Full ELF parsing/relocation is orthogonal. If ELF is admitted, enumerate supported section/symbol/relocation types and reject everything else—never silently approximate.[^S24][^S50]

Exclude A/F/D/C/V, CSRs, counters, privilege, MMU, syscalls, interrupts, concurrency, dynamic linking, TLS, self-modifying code, and asynchronous signals. Misaligned access behavior and instruction-address alignment must be fixed from the official ISA profile, not inherited from host behavior.[^S22]

### 7.2 Architectural state boundary

**[external fact]** QEMU TCG keeps a `cpu_env` plus globals tied to `CPUArchState`; helpers conservatively flush/read/write state unless annotated. Translation blocks cache assumed CPU state, chain direct branches, recover guest PC/state for exceptions, and invalidate translated code for self-modification.[^S08][^S09]

**[research inference]** Copying `CPUArchState*` into ONE Core would make downstream optimization operate through a guest-shaped memory blob and produce false “shared backend” reuse. Instead:

- decode each instruction to an explicit guest semantic op or executable semantic function;
- scalarize live registers/PC into SSA across the bounded function/region;
- represent guest memory through a typed address-space/effect interface;
- materialize architectural state only at entries, exits, helper boundaries, traps, or deoptimization points;
- keep precise source-PC mapping as semantic side data for faults, not as optimizer-visible origin branching.

Opaque helpers are permitted only with effect/trap summaries and a measured opacity budget. A helper for every complex instruction defeats convergence.

### 7.3 Static lifting versus DBT

O1's bounded function lifting is closer to static lifting/AOT translation than production DBT. Remill lifts machine instructions to LLVM bitcode using explicit state and memory interfaces; rev.ng uses QEMU-derived semantics and must recover control flow; BAP makes instruction side effects explicit; VEX and DynamoRIO show runtime instrumentation/translation tradeoffs.[^S12][^S13][^S14][^S15][^S16]

**[recommendation]** Do not claim DBT in O1 unless translation caching, indirect targets, runtime dispatch, precise faults, invalidation, and code mutation are actually exercised. Call the initial capability `RV64IM function lifting and execution`.

## 8. ONE Core design constraints

### 8.1 Required by O1

- bitvectors `i1…i64` with explicit truncation/extension and signedness on operations, not latent in storage type;
- typed function signatures and block arguments/SSA values;
- reducible and irreducible CFG representation;
- integer arithmetic with explicit overflow/trap/precondition semantics;
- comparisons, selects, direct calls, returns, and explicit exceptional/trap exits;
- address spaces and byte-addressed memory effects with width/alignment/endianness;
- globals, stack objects, and externally supplied memory regions;
- operation effects sufficient for DCE, CSE/GVN, load forwarding, and motion;
- source locations and origin trace for diagnostics, forbidden as correctness inputs after join.

### 8.2 Design now to avoid an obvious dead end

- region ownership and semantic interfaces so graph/dataflow regions can coexist later;
- vector type abstraction that does not assume only host-native fixed widths;
- memory-space identity and layout descriptors;
- explicit effect resources/tokens or equivalent dependence interface rather than one global “has side effects” bit;
- type/operation extensibility with dialect namespaces and verifier hooks;
- capability/dependency declarations separated from runtime implementation;
- semantic version identifiers on the IR contracts, without promising stable serialized bytecode.

### 8.3 Keep deliberately open

Do not choose stream token/rate semantics, tensor shape system, async execution model, relaxed concurrency, scalable-vector policy, floating-point environment, GPU hierarchy, codec primitives, or radio timing contracts during O1. Preserve extension points and record irreversible assumptions, but require DSP/O2 evidence before selecting these semantics.

## 9. Memory, effects, aliasing, and state

**[external fact]** LLVM MemorySSA versions memory through `MemoryDef`, `MemoryUse`, and `MemoryPhi`, but remains intraprocedural and relies on alias analysis for precision.[^S44] MLIR's extensibility depends on interfaces/traits that let passes reason about unknown operations; unknown effects must conservatively block transforms.[^S03]

**[recommendation]** Define memory along independent axes:

| Axis | O1 values |
|---|---|
| Space | `c.object`, `guest.ram`, `host/runtime`, later device spaces |
| Address | object+offset or numeric guest address; conversion is explicit |
| Access | read/write/read-modify-write; width and byte order explicit |
| Ordering | ordinary; volatile-like ordered; atomic reserved |
| Fault | impossible by precondition; trap outcome; host fault is never semantics |
| Alias | must/may/no-alias from frontend evidence, never guessed from origin |
| Lifetime | explicit for C objects; sandbox lifetime for guest regions |

Effect summaries should name resources and ranges where known. Calls without summaries conservatively touch all reachable memory and may trap. Guest register state is not memory unless materialized. The optimizer must consume semantic interfaces, not dialect names.

## 10. Cross-origin equivalence

### 10.1 Formal object of comparison

For contract `K`, define initial states `C₀` and `R₀` related by `R_in(K)` and observations:

`Obs = (termination kind, return bits, projected memory bytes, declared external events, trap code/location class)`.

The target claim for the UB-free deterministic O1 subset is:

`∀ input ∈ Pre(K): Obs_C(input) = Obs_RV(input) = Obs_ONE-C(input) = Obs_ONE-RV(input)`.

For nondeterministic semantics, replace equality with mutual refinement or a declared directional refinement. Time, register allocation, debug locations, and bytes outside the observable projection are not semantic observations unless the contract says so.

### 10.2 Four distinct properties

1. **Semantic equivalence:** established by executable references, differential execution, and bounded symbolic/refinement checks.
2. **Representational convergence:** normalized common IR shares operation/effect/control structure under a declared correspondence.
3. **Mechanism reuse:** identical analyses/rules/backends operate without origin-conditioned correctness paths.
4. **Outcome quality:** generated code and resource costs remain within preregistered bounds.

None implies the others. Graph similarity can diagnose variance but cannot prove equivalence.

### 10.3 Operational convergence metrics

- normalized basic-block/operation correspondence after alpha-renaming and commutative canonicalization;
- weighted overlap of semantic op classes emitted by both origins;
- percentage of dynamic common-Core operations processed by identical pass rules;
- divergence introduced by source-required semantics versus accidental frontend choices;
- final machine-code equivalence classes (identical, isomorphic, equal-cost, or only behaviorally equal);
- SMT-proved expression equivalence for bounded pure regions;
- origin-classifier test: attempt to predict origin from canonical Core features. High accuracy after controlling for source algorithm is evidence of residual provenance, not automatically failure but requiring explanation.

## 11. Shared optimization

### 11.1 Evidence strength

| Optimization | O1 evidence strength | Reason |
|---|---:|---|
| Constant folding, trivial DCE | Low | Any common IR obtains these almost mechanically |
| Branch folding, copy propagation | Low–medium | Exercises CFG but weak semantic knowledge |
| SCCP | Medium | Joint value/control reasoning; useful across both paths |
| GVN/CSE across reconstructed expressions | High | Tests canonicalization and effect precision |
| Load forwarding / redundant store elimination | High | Tests alias/effect/state boundary directly |
| Loop-invariant code motion | High if memory-bearing | Requires loop, dominance, aliasing, trapping correctness |
| Strength reduction | Medium–high | Meaningful if applied unchanged to independently shaped origins |
| Vectorization | Deferred | Too much O1 surface; strong later cross-domain evidence |

**[recommendation]** O1's minimum strong set is SCCP + GVN/CSE + one alias/effect-sensitive memory optimization + one loop transform. Each must have:

- one origin-independent implementation and contract;
- applicability and fire counts by origin;
- correctness validation;
- ablation showing runtime/code-size or instruction-count benefit on both origins;
- negative cases demonstrating blocked unsafe transforms;
- no frontend-side duplicate of the core rule.

“Both call the same pass manager” is infrastructure reuse, not optimization-knowledge reuse.

## 12. Verification strategy

### 12.1 Layered assurance matrix

| Layer | Oracle/method | Required evidence |
|---|---|---|
| C parser/type/lowering | fixed `ONE-C-O1` spec; Clang/GCC differential; Cerberus/CompCert concepts | accepted/rejected corpus, UB boundary tests |
| RV decode/semantics | official RISC-V spec + Sail model | exhaustive decode by admitted encoding; differential instruction and trace tests |
| Core interpreter | executable small-step semantics | golden traces, property tests, determinism where claimed |
| Lowerings | per-pass source/target relation | bounded SMT/refinement for pure/finite fragments; differential execution otherwise |
| Optimizer | translation validation + fuzzing | counterexample artifacts and minimized regressions |
| x86 backend | Core interpreter vs emitted execution | randomized functions, ABI sentinels, disassembly/relocation checks |
| Cross-origin | contract harness | concrete, symbolic bounded, and metamorphic equivalence |

**[external fact]** Sail can generate executable emulators and theorem-prover definitions from ISA semantics; the official RISC-V Sail model and architectural tests provide strong reusable oracles.[^S25][^S26][^S27] Csmith found mature-compiler bugs by generating defined C programs; YARPGen adds optimization-focused generation; `riscv-dv` generates instruction streams.[^S33][^S34][^S35]

**[recommendation]** Differential agreement between two systems is evidence, not proof: correlated bugs and undefined inputs remain possible. Use at least one specification-derived oracle plus independent implementations. Every failure artifact records seed, minimized input, semantic profile, hashes, pass pipeline, host, and exact commands.

**[recommendation]** Keep SMT bounded: straight-line bitvector regions, bounded memory, and bounded loops. Timeouts are `unknown`, never pass. Random testing covers breadth; translation validation covers local transformations; executable semantics anchors meaning.

## 13. x86-64 backend implications

**[recommendation]** Build a minimal AOT backend first. Emit a relocatable ELF object or a JIT memory image, but choose one claim. AOT ELF offers inspectable artifacts and normal linking; JIT avoids writing a linker but introduces executable-memory and symbol-resolution concerns. For O1 reproducibility, a small ELF64 relocatable emitter plus the system linker is defensible, provided external linking is declared non-central.

Minimum meaningful backend:

- System V AMD64 integer calling convention and stack alignment;
- instruction selection for admitted integer/control/memory ops;
- legalization with explicit helper policy;
- virtual registers, liveness, at least linear-scan or similarly real allocation with spills;
- stack frames, callee-saved preservation, direct calls/returns;
- labels, branches, relocations, `.text`, minimal symbols, and machine-code emission;
- deterministic output and differential execution.

Delay FP/SIMD, PIC/PLT/GOT, dynamic linking, DWARF, exceptions/unwinding, TLS, atomics, varargs, and multiple code models. Do not delay register allocation or calls: omitting them makes backend reuse too toy-like. LLVM and Cranelift both expose why legalization, selection, register allocation, frames, and emission are distinct correctness surfaces.[^S07][^S46][^S48][^S49]

## 14. Modularity and runtime specialization

**[external fact]** Compile-time feature selection alone does not guarantee small closures; monomorphization, registries, reflection, function-pointer tables, initialization, and retained sections can preserve unused code. Linker section GC and LTO can remove unreachable units, but roots and dynamic lookup must be audited.[^S51][^S52][^S53]

**[recommendation]** Model each capability as a manifest node with:

- semantic operations/types provided;
- compiler-only versus runtime components;
- hard dependencies and optional edges;
- initialization hooks and linker roots;
- supported targets;
- measurable closure hash.

Build profiles must be derived closures, not hand-maintained lists. Test `minimal-c`, `rv-lift`, and `full-o1` artifacts. For each, record stripped file size, loadable segment size, dynamic dependencies, exported symbols, RSS/peak RSS, startup, and build time. Add a **capability delta test**: `cost(A∪{x}) − cost(A)` across multiple bases; non-additivity is itself evidence.

## 15. Performance and experimental methodology

**[external fact]** SPEC's run rules treat a result as an observation under disclosed conditions, require repeated runs and output validation, distinguish common “base” settings from benchmark-specific “peak” tuning, and explicitly reject name-based benchmark specialization.[^S54] LLVM benchmarking guidance emphasizes stable machines, repeated measurements, noise control, and statistical interpretation.[^S55]

### 15.1 Preregistered benchmark manifest

Every workload records:

- semantic contract and equivalence class;
- provenance of both implementations and independence procedure;
- included/excluded guarantees;
- input distributions plus held-out adversarial inputs;
- frozen baseline versions, flags, host/toolchain hashes;
- warmup, cold/warm distinction, repetitions, aggregation, confidence interval, outlier rule;
- correctness oracle and acceptable output relation;
- compile time split by phase, runtime, code size, executed instructions, peak memory, startup;
- timeout/resource ceilings and all failures.

Use three tiers: micro semantics tests; kernel workloads with loops/memory/calls; small application kernels. Freeze a hidden/held-out subset before optimizer tuning. Report geomeans only over compatible ratios and always retain per-workload results.

### 15.2 Anti-gaming controls

- base pipeline fixed for the suite; peak results labeled separately;
- no workload names visible to optimization rules;
- leave-one-family-out tests for learned/tuned heuristics;
- negative and worst-case workloads retained;
- baselines receive comparable tuning and correctness guarantees;
- compile-time and footprint regressions cannot be hidden by runtime wins;
- any helper/library substitution reported as such;
- all unsupported cases remain in denominators or are explicitly counted as failures.

## 16. Measuring real shared infrastructure

No single percentage is trustworthy. Publish a vector:

1. **Semantic overlap:** weighted fraction of normalized Core op/effect classes exercised by at least two origins.
2. **Pass reuse:** for each pass, origins accepted, workloads transformed, rules fired, and ablation benefit.
3. **Contract reuse:** count semantic definitions/proofs/tests consumed unchanged by multiple origins.
4. **Backend reuse:** fraction of target backend mechanisms exercised by both origins, weighted by dynamic machine operations and feature coverage.
5. **Origin blindness:** after the declared join, static count and dynamic coverage of branches or dispatch keyed by origin/dialect; target is zero for correctness paths, exceptions justified.
6. **Opacity:** dynamic/static fraction of computation hidden behind helpers/opaque ops at the join.
7. **Marginal integration cost:** new origin-specific code, concepts, contracts, and tests needed to reuse an existing pass/backend.
8. **Reuse quality:** defect fixes or optimizations in a shared component that benefit/regress multiple origins without parallel patches.

Weighting must be preregistered. LOC may accompany these metrics as provenance, never as the headline. A shared 1,000-line generic framework unused by one path counts less than a 100-line semantic rule with validated benefit for both.

## 17. Complexity-compression metrics

**[research inference]** “Maximum useful capability with minimum accidental complexity” is multi-objective; collapsing it into one score permits arbitrary weights. Track slopes and Pareto fronts instead.

| Dimension | Practical proxy | Failure signal |
|---|---|---|
| Semantic concepts | operations, types, effects, invariants required per capability | each frontend adds parallel concepts |
| Interface surface | public APIs + IR grammar/interface members | superlinear growth with domains |
| Dependency structure | nodes/edges, cycles, closure size, unstable hubs | core depends upward on domains |
| Duplication | semantic clone/rule duplication, not token clones only | same proof/optimization rewritten per origin |
| Conditionality | origin-dependent branches after join | growing provenance cascades |
| Build/deploy cost | build time, artifact bytes, RSS, startup, dependencies | full-repo growth inflates minimal artifacts |
| Extension cost | change set to add frontend/backend/capability | multiplicative edits across existing modules |
| Maintenance evidence | defect propagation, test matrix, change coupling | one change requires unrelated domain repairs |

For each campaign record `Δcapability / Δcomplexity-vector`. Do not reward many shallow capabilities. Capability receives credit only when correctness, quality, and integration gates pass.

## 18. Future-domain pressure tests

### 18.1 DSP/dataflow

Synchronous dataflow makes token production/consumption rates explicit, enabling static schedules and bounded buffers; StreamIt exploits stream structure for fusion, fission, load balancing, and communication-aware mapping.[^S57][^S58] Lowering streams immediately into imperative ring-buffer loads/stores destroys rates, latency, fusion, and schedule freedom.

Irreversibilities to avoid in O1:

- assuming all regions execute as sequential CFGs;
- assuming values are only scalar/fixed host vectors;
- one undifferentiated memory space;
- effects that cannot express channels, stateful delay, or resource ordering;
- treating scheduling only as machine-instruction order;
- arithmetic lacking explicit saturation, rounding, fixed-point, complex, or accuracy contracts.

### 18.2 Tensor/ML

TVM separates graph-level Relax from scheduled TensorIR and notes that unscheduled CPU code may be slow while GPU schedules are required for valid mapping; MLIR Linalg preserves structured tensor semantics before bufferization; Triton exposes tiled program instances and memory hierarchy.[^S36][^S39][^S40] Dangerous O1 commitments are fixed layouts, eager bufferization, fixed rank assumptions in the core container, and inability to express target-dependent tiling/async copies.

### 18.3 Media

Codecs mix regular transforms with bit-exact integer arithmetic, entropy-driven irregular control, stateful prediction, frame/tile dependencies, and latency/throughput tradeoffs. Preserve room for explicit bitstream effects, stateful streaming, vectorizable transforms, and accuracy/bit-exact modes. Do not add codec ops to O1 Core.

### 18.4 Radio/SDR

Radio adds sample-rate clocks, bounded latency, complex/fixed-point arithmetic, synchronization loops, FFT/filter banks, FEC, and hardware I/O. A purely functional tensor graph is insufficient; an unrestricted imperative CFG loses schedule/rate information. The container must permit distinct time/dataflow semantics until a justified lowering point.

## 19. Prior-art comparative matrix

| System | Central model / solved problem | Preserves and shares | Principal cost/limit | Lesson and non-novelty for ONE |
|---|---|---|---|---|
| LLVM | low-level typed SSA + broad optimizer/backend | language-neutral analyses and targets | high-level intent often lost; complex UB/memory semantics | common compiler IR/backend is established[^S02] |
| MLIR | extensible ops/types/regions/dialects and conversions | infrastructure across abstraction levels | semantics/pipelines remain project-defined; dialect fragmentation risk | multi-level IR, dialects, progressive lowering are established[^S03][^S17] |
| GCC | GIMPLE/SSA → RTL machine pipeline | mature language and target reuse | large historical complexity; two worlds and target hooks | staged language-neutral/machine IR is established[^S10][^S11] |
| QEMU TCG | guest instruction semantics → compact typed IR → hosts | multi-guest/multi-host translation machinery | guest state, helpers, TB boundaries constrain optimization | ISA→common IR→host and portable DBT are established[^S08][^S09] |
| Valgrind/VEX | guest-neutral IR for DBI and shadow tools | analyses/instrumentation across ISAs | heavyweight overhead; IR tailored to instrumentation | shared binary-analysis IR is established[^S15][^S43] |
| Remill/McSema | instruction semantics lifted to LLVM | LLVM analysis/tool reuse on binaries | explicit state/memory can obscure high-level structure; CFG recovery separate | binary→LLVM reuse is established[^S12][^S59] |
| rev.ng | whole-binary analysis/translation via QEMU/LLVM | multi-ISA semantic translation | CFG/function/indirect-target recovery is fundamental | lifting is not only instruction decoding[^S13][^S60] |
| BAP | side-effect-explicit binary IL and analyses | multi-architecture analysis APIs | analysis focus, not competitive codegen | explicit instruction effects are established[^S16] |
| Cranelift | fast SSA compiler, VCode, ISLE lowering | compact reusable codegen | deliberately trades peak optimization scope for speed/simplicity | declarative lowering and small serious backends are precedents[^S48][^S49] |
| V8 TurboFan | sea-of-nodes optimizing JIT | control/data/effect dependency optimizations | speculative/deopt complexity and JS specialization | graph IR is an option, not inherently more general[^S61] |
| SPIR-V | binary IR for graphics/compute environments | portable structured modules and memory semantics | environment/capability constrained; not a general optimizer architecture | capabilities and explicit memory model are precedents[^S37] |
| TVM | Relax graphs + TensorIR schedules + modular runtime | cross-level tensor optimization and targets | domain-specific scheduling remains essential | one low IR cannot preserve ML optimization opportunity[^S36] |
| XLA/StableHLO | tensor operation graphs and portable semantics | graph optimizations/backend interfaces | tensor-centered; layouts/dynamics/side effects are difficult | tensor dialect/portable op semantics are established[^S38][^S62] |
| Halide | algorithm/schedule separation for image pipelines | reusable scheduling vocabulary | specialized domain and purity assumptions | schedule is semantic optimization information[^S41] |
| Triton | tiled GPU program abstraction | layout/memory-hierarchy-aware kernel compilation | accelerator-specific execution model | useful convergence may occur above scalar loops[^S40] |
| CIRCT | MLIR dialect stack for hardware design | shared compiler infrastructure with hardware semantics | many dialects and staged conversions | extensibility does not itself create semantic integration[^S42] |
| egg | e-graphs/equality saturation | declarative equivalences and extraction | blow-up, cost model, effects/loops | equality saturation is prior art and must be bounded[^S18][^S19] |

## 20. Failure modes and adversarial findings

| Failure | Observable signature | Required response |
|---|---|---|
| False convergence | high IR similarity only for compiler-derived pairs | exclude from primary claim; use independent pairs |
| Lowest-common-denominator Core | rich ops lower before shared useful transforms | move join later or introduce semantic interface |
| Guest contamination | common passes manipulate `CPUState` offsets/helpers | scalarize state; redefine join |
| Dialect explosion | passes enumerate dialects/origins | interface-based semantics or abandon claimed commonality |
| Universal tax | minimal artifact grows with unrelated capability | closure test failure; dependency inversion/refactor |
| Opaque-helper success | correctness passes but computation hides in helpers | opacity budget failure; no convergence credit |
| Shared-name illusion | same pass entrypoint dispatches separate rules | report split; no shared-knowledge credit |
| Benchmark overfit | gains vanish on held-out compiler/inputs | invalidate general claim |
| Semantic weakening | ONE compares faster by omitting traps/ABI/alias guarantees | comparison invalid, not a win |
| Premature future design | unused stream/tensor abstractions dominate O1 | remove or mark experimental; preserve only extension constraints |
| MLIR/QEMU/LLVM reimplementation | no measurable property beyond existing composition | revise thesis or produce differential evidence |

**[adversarial finding]** O1 alone cannot prove the broad thesis because C and RV64 machine code are both conventional imperative, scalar, memory-based computation. It can only establish that the proposed semantic join is not already false and that reuse metrics work. DSP remains the first genuinely adversarial domain.

## 21. Decisions O1 requires before implementation

1. Exact `ONE-C-O1` grammar, data model, UB policy, memory/provenance semantics, and exclusions.
2. Exact RV64IM instruction/ABI/environment profile and rejection rules.
3. Cross-origin contract schema, observables, state relation, equivalence/refinement direction.
4. Primary independent-pair methodology versus secondary compiler-roundtrip methodology.
5. Core operation/type/control/memory/effect/trap semantics and verifier invariants.
6. Semantic discharge/join criteria and forbidden origin dependencies after join.
7. Pass contracts and required strong shared optimization set.
8. Backend ABI, output format, register allocator, linker boundary, and oracle.
9. Correctness matrix, corpus classes, SMT bounds/timeouts, differential oracles.
10. Benchmark/reuse/complexity manifests and preregistered rejection thresholds.
11. Capability graph and minimal/rv/full artifact profiles.

## 22. Decisions that should remain open

- implementation language until a separate evidence-based engineering decision;
- exact long-term number/names of IR levels;
- sea-of-nodes versus region/CFG hybrids beyond the O1 core;
- stable serialized IR format and compatibility promise;
- stream/dataflow semantics and DSP scheduler;
- tensor types, shapes, bufferization, accelerator hierarchy;
- relaxed memory, atomics, concurrency, and synchronization;
- FP/IEEE-754, arbitrary precision, fixed-point, and numerical library ownership;
- JIT/DBT architecture, TB cache/invalidation, full-system emulation;
- second backend and long-term runtime/plugin model;
- own systems language, media codec, and radio stack.

## 23. Research-backed recommendations for the consolidation sprint

The consolidation should convert prose claims into a compact chain of falsifiable contracts without pretending the architecture is implemented:

1. Correct EXP-01 into primary independent-pair and secondary round-trip campaigns.
2. Specify O1 boundaries using accept/reject tables, not examples alone.
3. Add a semantic relation for every pipeline edge and a canonical observable model.
4. Define the join/discharge rule and an origin-blindness invariant.
5. Define minimum Core semantics and explicitly deferred semantics.
6. Replace “percentage shared” with the reuse vector in §16.
7. Add opacity, semantic weakening, and compiler-derived-pair failure gates.
8. Define the O1 correctness/verification matrix and evidence artifact schema.
9. Preregister benchmark manifests, baselines, held-out sets, and rejection thresholds.
10. Turn capability closure and complexity compression into executable future schemas.
11. Expand related work with the comparative matrix, including what ONE cannot claim.
12. Record negative evidence and unknown/timeout outcomes as first-class results.

## 24. Suggested vault artifacts and contracts

Keep the set small and authoritative:

| Artifact | Purpose | Status after consolidation |
|---|---|---|
| `spec/o1-scope.md` | exact C/RV/backend surface and exclusions | designed |
| `spec/semantic-relations.md` | states, observables, refinement, join/discharge | designed |
| `spec/one-core-contract.md` | operations, types, effects, traps, invariants | designed, versioned |
| `spec/pass-contracts.md` | required inputs, legality, preservation, validation | designed |
| `validation/o1-protocol.md` | independent pairs, oracles, fuzz/SMT/differential methods | designed |
| `validation/benchmark-schema.json` | frozen machine-readable experiment manifest | designed |
| `validation/reuse-schema.json` | reuse vector and origin-blindness/opacity data | designed |
| `claims/registry.md` | claim → status → evidence → falsifier → dependencies | accepted governance |
| `evidence/ledger-schema.md` | hashes, commands, environment, positive/negative results | accepted governance |
| expanded `research/related-work.md` | prior-art boundaries and active comparisons | accepted research |

Avoid one ADR per detail. ADRs should record only decisions with real alternatives and architectural consequences. Specifications state semantics; protocols state how claims are tested; evidence records observations; the claims registry connects them.

## 25. Remaining unknowns and research gaps

- Whether independent C/RV implementations converge enough for nontrivial memory loops without frontend-specific recovery.
- Whether a provenance-aware C layer can discharge to a guest-compatible address model without losing useful alias information.
- Whether origin-blind post-join optimization is feasible or whether justified semantic capabilities must remain visible.
- Which memory-sensitive shared pass yields the first robust benefit across both origins.
- What quantitative opacity/origin-branch threshold distinguishes acceptable boundary code from failed convergence.
- Whether a purpose-built core beats an MLIR-based prototype on density, compile latency, and semantic clarity; this cannot be settled by taste.
- How DSP's rates, buffering, timing, and state should interact with regions/effects; O2 evidence is required.
- What complexity vector predicts maintenance burden over several domains; early metrics must be revised against observed change history without moving prior campaign thresholds.

## 26. Decision matrix for the next agent

| Question | Current ONE state | Relevant evidence | Real options | Main risks | Resolve in consolidation? | Resolve before O1? |
|---|---|---|---|---|---:|---:|
| C profile | open | C23, Cerberus, CompCert, provenance work | full C; strict subset; implementation-defined profile | unsound UB or toy subset | Yes | Yes |
| RV surface | open | ISA + psABI + Sail | RV32I; RV64I; RV64IM; larger | artificial helpers or scope explosion | Yes | Yes |
| Comparison corpus | underspecified | compiler testing/lifting literature | compiler-derived; independent; both labeled | false convergence | Yes | Yes |
| Equivalence relation | open | translation validation/formal semantics | equality; refinement; testing only | meaningless “similarity” | Yes | Yes |
| Core form | hypothesis | LLVM/MLIR/GCC/graph IRs | CFG SSA; graph; regions+CFG | premature lock-in | minimum only | Yes, minimum |
| C/guest memory join | open | provenance, MemorySSA, TCG | integer addresses; distinct refs then discharge; tagged universal pointer | C unsoundness or guest fiction | Yes | Yes |
| Guest state | open | QEMU/Remill/BAP | monolithic state; scalar SSA; hybrid materialization | contaminated core or imprecise traps | Yes | Yes |
| Effects | open | MLIR interfaces, LLVM MemorySSA | global token; resource effects; implicit flags | blocked optimization or unsound motion | Yes | Yes |
| Canonicalization | hypothesis | MLIR rewriting, egg | greedy phases; e-graphs; mixed | nontermination/blow-up or weak convergence | policy | Yes |
| Shared optimization proof | open | SCCP/GVN/memory passes, Alive2 | utility reuse; rule/contract reuse; ablation | vanity metric | Yes | Yes |
| Backend output | open | ELF, SysV ABI, LLVM/Cranelift | JIT; ELF object; assembly | toy backend or linker scope | Yes | Yes |
| Runtime specialization | designed | linker GC/LTO/features | static closure; plugins; generated runtime | universal tax | schema/gates | minimum profiles |
| Stable serialization | merely desired if needed | MLIR/LLVM/SPIR-V | none; textual only; versioned binary | compatibility burden | No | No |
| Streams/tensors | future constraint | SDF/StreamIt/TVM/MLIR | encode now; extension hooks; wait | speculative architecture | constraints only | No |
| Implementation language | open | no discriminating experiment yet | Rust/C++/Zig/other | fashion-driven choice | No | before coding, separate ADR |
| Reuse metric | open | §16 synthesis | scalar percentage; metric vector | gaming | Yes | Yes |
| Complexity metric | principle only | §17 synthesis | LOC; composite score; Pareto vector | vanity/gaming | Yes | Yes |
| Abandon/redesign threshold | qualitative | risks/invariants | opaque/helper/origin/tax thresholds | adapters hide failure | Yes | Yes |

## 27. Source ledger

### ONE snapshot

[^S01]: ONE repository, [`vault/` at `main@a2f89d4`](https://github.com/CesarManzoCode/one/tree/a2f89d4cf28a3cafc89951861dc44f838d7c7639/vault), accessed 2026-09-14. All statements labeled **ONE fact**, **current decision**, or **hypothesis** derive from the complete vault at this snapshot.

### Compiler and IR architecture

[^S02]: LLVM Project, [LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html), current documentation.
[^S03]: MLIR Project, [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/), current documentation.
[^S04]: MLIR Project, [MLIR Rationale](https://mlir.llvm.org/docs/Rationale/Rationale/), current documentation.
[^S05]: MLIR Project, [Pattern Rewriting](https://mlir.llvm.org/docs/PatternRewriter/), current documentation.
[^S06]: MLIR Project, [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/), current documentation.
[^S07]: LLVM Project, [Target-Independent Code Generator](https://llvm.org/docs/CodeGenerator.html), current documentation.
[^S08]: QEMU Project, [Translator Internals](https://www.qemu.org/docs/master/devel/tcg.html), current documentation.
[^S09]: QEMU Project, [TCG Intermediate Representation](https://www.qemu.org/docs/master/devel/tcg-ops.html), current documentation.
[^S10]: GCC Project, [GIMPLE](https://gcc.gnu.org/onlinedocs/gccint/GIMPLE.html), GCC internals manual.
[^S11]: GCC Project, [RTL](https://gcc.gnu.org/onlinedocs/gccint/RTL.html), GCC internals manual.
[^S12]: Lifting Bits, [Remill](https://github.com/lifting-bits/remill), source repository and architecture overview.
[^S13]: rev.ng, [A Multi-Architecture Framework for Reverse Engineering](https://rev.ng/downloads/iccst-18-paper.pdf), 2018.
[^S14]: DynamoRIO Project, [DynamoRIO documentation](https://dynamorio.org/), current first-party documentation.
[^S15]: Valgrind Project, [The Design and Implementation of Valgrind](https://valgrind.org/docs/manual/mc-tech-docs.html), current manual.
[^S16]: Brumley et al., [BAP: A Binary Analysis Platform](https://edmcman.github.io/pres/cav11.pdf), CAV 2011.
[^S17]: Lattner et al., [MLIR: Scaling Compiler Infrastructure for Domain Specific Computation](https://research.google/pubs/mlir-scaling-compiler-infrastructure-for-domain-specific-computation/), CGO 2021.
[^S18]: Willsey et al., [egg: Fast and Extensible Equality Saturation](https://arxiv.org/abs/2004.03082), POPL 2021.
[^S19]: Köhler et al., [Sketch-Guided Equality Saturation](https://arxiv.org/abs/2111.13040), 2021.

### C and ISA semantics

[^S20]: ISO WG14, [N3096 — ISO/IEC 9899:2023 working draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf), 2023.
[^S21]: ISO WG14, [N2676 — Provenance-aware Memory Object Model for C](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2676.pdf), 2021 draft TS.
[^S22]: RISC-V International, [Unprivileged ISA, official 20260120 release](https://docs.riscv.org/reference/isa/v20260120/unpriv/unpriv-index.html), 2026.
[^S23]: RISC-V International, [RISC-V ABIs Specification](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), version displayed 2026-08-13.
[^S24]: RISC-V International, [RISC-V ELF psABI chapters](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), current draft.
[^S25]: RISC-V International, [Sail RISC-V model](https://github.com/riscv/sail-riscv), source repository.
[^S26]: Armstrong et al., [ISA Semantics for ARMv8-A, RISC-V, and CHERI-MIPS](https://www.cl.cam.ac.uk/~pes20/sail/sail-popl2019.pdf), POPL 2019.
[^S27]: RISC-V International, [RISC-V Architectural Certification Tests](https://github.com/riscv/riscv-arch-test), source repository.
[^S28]: REMS Project, [Cerberus C semantics](https://github.com/rems-project/cerberus), source repository.
[^S29]: CompCert Project, [The CompCert Verified Compiler](https://compcert.org/doc/), current project documentation.

### Verification and testing

[^S30]: Alive2 Project, [Alive2: Automatic Verification of LLVM Optimizations](https://github.com/AliveToolkit/alive2), source repository and limitations.
[^S31]: Lopes et al., [Alive2: Bounded Translation Validation for LLVM](https://web.ist.utl.pt/nuno.lopes/pres/alive2-pldi21.pdf), PLDI 2021.
[^S32]: CompCert Project, [Context and motivations](https://compcert.org/motivations.html), formal semantics and preservation overview.
[^S33]: Yang et al., [Finding and Understanding Bugs in C Compilers](https://www.flux.utah.edu/paper/yang-pldi11), PLDI 2011.
[^S34]: Intel, [YARPGen](https://github.com/intel/yarpgen), source repository.
[^S35]: Chips Alliance, [riscv-dv](https://github.com/chipsalliance/riscv-dv), source repository.

### Domain compilers and future pressure

[^S36]: Apache TVM, [Design and Architecture](https://tvm.apache.org/docs/arch/index.html), current documentation.
[^S37]: Khronos Group, [SPIR-V Specification](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html), unified specification.
[^S38]: OpenXLA Project, [XLA Architecture](https://openxla.org/xla/architecture), current documentation.
[^S39]: MLIR Project, [Linalg Dialect](https://mlir.llvm.org/docs/Dialects/Linalg/), current documentation.
[^S40]: Triton Project, [Triton language and compiler documentation](https://triton-lang.org/main/index.html), current documentation.
[^S41]: Halide Project, [Halide language overview and scheduling model](https://halide-lang.org/), first-party documentation.
[^S42]: CIRCT Project, [CIRCT documentation](https://circt.llvm.org/docs/), current documentation.
[^S43]: Nethercote and Seward, [Valgrind: A Framework for Heavyweight Dynamic Binary Instrumentation](https://nnethercote.github.io/pubs/valgrind2007.pdf), PLDI 2007.

### Memory, backend, and modularity

[^S44]: LLVM Project, [MemorySSA](https://llvm.org/docs/MemorySSA.html), current documentation.
[^S45]: LLVM Project, [Alias Analysis Infrastructure](https://llvm.org/docs/AliasAnalysis.html), current documentation.
[^S46]: LLVM Project, [Global Instruction Selection](https://llvm.org/docs/GlobalISel/index.html), current documentation.
[^S47]: LLVM Project, [LLVM IR Undefined Behavior Manual](https://llvm.org/docs/UndefinedBehavior.html), current documentation.
[^S48]: Fallin, [Cranelift's Instruction Selector DSL, ISLE](https://cfallin.org/blog/2023/01/20/cranelift-isle/), 2023, author technical account.
[^S49]: Fallin, [Cranelift: Correctness in Register Allocation](https://cfallin.org/blog/2021/03/15/cranelift-isel-3/), 2021, author technical account.
[^S50]: System V ABI, [ELF Generic ABI](https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html), object/loading specification.
[^S51]: LLVM lld, [ELF section garbage collection notes](https://lld.llvm.org/ELF/start-stop-gc.html), current documentation.
[^S52]: Rust Project, [Cargo Features](https://doc.rust-lang.org/cargo/reference/features.html), current reference.
[^S53]: LLVM Project, [Link Time Optimization design](https://llvm.org/docs/LinkTimeOptimization.html), current documentation.

### Experimental method, additional prior art, and streaming

[^S54]: SPEC, [CPU 2017 Run and Reporting Rules](https://www.spec.org/cpu2017/Docs/runrules.html), current published rules.
[^S55]: LLVM Project, [Benchmarking Tips](https://llvm.org/docs/Benchmarking.html), current documentation.
[^S56]: Google Benchmark, [User Guide](https://github.com/google/benchmark/blob/main/docs/user_guide.md), current documentation.
[^S57]: Lee and Messerschmitt, [Synchronous Data Flow](https://ptolemy.berkeley.edu/publications/papers/87/synchdataflow/), Proceedings of the IEEE 1987.
[^S58]: MIT CSAIL, [StreamIt research project and publications](https://groups.csail.mit.edu/cag/streamit/), first-party project archive; see the ASPLOS 2002 compiler work listed there.
[^S59]: Lifting Bits, [McSema](https://github.com/lifting-bits/mcsema), source repository.
[^S60]: Di Federico et al., [A Jump-Target Identification Method for Multi-Architecture Static Binary Translation](https://rev.ng/downloads/cases-2016-paper.pdf), CASES 2016.
[^S61]: V8 Project, [TurboFan JIT design material](https://v8.dev/docs/turbofan), first-party documentation.
[^S62]: OpenXLA Project, [StableHLO Specification](https://openxla.org/stablehlo/spec), current specification.

### Additional specifications and tools consulted

- LLVM Project, [Machine IR Reference](https://llvm.org/docs/MIRLangRef.html).
- LLVM Project, [Auto-Vectorization](https://llvm.org/docs/Vectorizers.html).
- LLVM Project, [Opaque Pointers](https://llvm.org/docs/OpaquePointers.html).
- LLVM Project, [Writing an LLVM Backend](https://llvm.org/docs/WritingAnLLVMBackend.html).
- LLVM Project, [ORC JIT Design](https://llvm.org/docs/ORCv2.html).
- QEMU Project, [Record/replay](https://www.qemu.org/docs/master/system/replay.html).
- QEMU Project, [TCG plugins](https://www.qemu.org/docs/master/devel/tcg-plugins.html).
- RISC-V International, [M extension semantics](https://docs.riscv.org/reference/isa/v20260120/unpriv/m-st-ext.html).
- RISC-V International, [Formal memory-model appendix](https://docs.riscv.org/reference/isa/v20260120/unpriv/mm-formal.html).
- MLIR Project, [Bufferization](https://mlir.llvm.org/docs/Bufferization/).
- Google, [Souper superoptimizer](https://github.com/google/souper).
- Lattner and Adve, [LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation](https://llvm.org/pubs/2004-01-30-CGO-LLVM.html), CGO 2004.
- Bellard, [QEMU, a Fast and Portable Dynamic Translator](https://www.usenix.org/conference/2005-usenix-annual-technical-conference/qemu-fast-and-portable-dynamic-translator), USENIX 2005.

---

**Research conclusion.** ONE's founding decisions are directionally defensible, but the present O1 description does not yet define a valid scientific test. The consolidation should not freeze a grand universal architecture. It should freeze the smallest semantic and experimental constitution capable of making O1 fail honestly: exact profiles, explicit relations, a defensible join point, strong shared-pass evidence, origin-blindness and opacity gates, capability-closure measurements, and preregistered benchmark rules. If those survive, O1 earns the right to be challenged by DSP. If they do not, the vault must force redesign before breadth is added.
