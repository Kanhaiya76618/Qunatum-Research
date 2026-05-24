## 1. Introduction

When a relational database executes a multi-table query, the
query optimizer must determine the order in which to perform
the joins. The chosen order directly determines the size of
intermediate results produced at each step, which in turn
governs memory consumption, I/O volume, and CPU time. A
suboptimal join order can cause intermediate result sets to
grow by several orders of magnitude relative to the optimal
sequence — both paths produce identical final answers, but the
difference in execution cost can mean the difference between a
query completing in seconds and one that exhausts available
memory or runs for hours. This is not an academic edge case:
modern data warehouses and analytical workloads routinely join
10 to 25 tables in a single query, and every query powering a
business dashboard, a recommendation engine, or a financial
report depends on the optimizer making this decision correctly.

Classical database optimizers — PostgreSQL, MySQL, Oracle, and
virtually every relational system in production use over the
past four decades — employ Selinger's dynamic programming
algorithm (1979) to find the optimal join order [CITE Selinger
1979]. Selinger's algorithm was a landmark contribution: it
reduces the search space from N! to O(3^N) by building optimal
subplans bottom-up over all table subsets and discarding
dominated alternatives. However, O(3^N) remains exponential —
the algorithm scales tractably to roughly 15 tables, beyond
which exhaustive enumeration becomes prohibitive for interactive
query response times. Beyond this threshold, production systems
fall back to heuristics such as greedy join ordering, randomized
search, or genetic algorithms [CITE Ioannidis 1987]. These
approaches can find reasonable plans but offer no optimality
guarantee, and the gap between a heuristic plan and the true
optimum is in general unknown and unbounded. The fundamental
barrier is complexity-theoretic: join ordering is NP-hard
[CITE Ibaraki 1984], implying that no polynomial-time exact
algorithm exists unless P = NP, and any solution guaranteeing
optimality must either accept exponential worst-case cost or
explore an entirely different computational model.

Quantum computing offers precisely such an alternative model.
The Quantum Approximate Optimization Algorithm (QAOA) encodes
combinatorial optimization problems as Quadratic Unconstrained
Binary Optimization (QUBO) instances and solves them using a
qubit count that grows polynomially as N² with problem size,
rather than the exponential number of subsets that classical
DP must enumerate. Prior work in this direction includes
Trummer and Koch (2016), who first applied quantum annealing
on a D-Wave processor to database optimization; Schönberger
et al. (2023), who formulated join ordering as a QUBO and
evaluated it on D-Wave hardware; and Uotila (2025), who
extended the encoding to higher-order unconstrained binary
optimization (HUBO) for left-deep join trees [CITE Schonberger
2023][CITE Uotila 2025][CITE Trummer 2016]. However, these
studies focus primarily on quantum annealing rather than
gate-based QAOA, and none provides a systematic comparison
across all three tiers of experimental realism — noiseless
ideal simulation, synthetic noise injection, and execution
on a real gate-based quantum processor — using an
industry-standard benchmark. This paper fills that gap.