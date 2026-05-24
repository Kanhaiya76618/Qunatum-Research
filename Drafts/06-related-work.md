## Related Work

### Classical Join Order Optimization

Selinger et al. (1979) established cost-based dynamic programming
for join ordering, laying the foundation for virtually every major
relational optimizer built in the subsequent four decades
[CITE Selinger 1979]. Their insight — building optimal subplans
bottom-up and pruning dominated alternatives — reduced the search
space from N! to O(3^N), yet the worst-case complexity remains
exponential. For queries beyond the reach of exact DP, Ioannidis
and Kang (1990) introduced randomized search for join ordering,
including iterative improvement and simulated annealing applied
to query plan spaces [CITE Ioannidis 1990]. These were followed
by genetic algorithms, which trade optimality guarantees for the
ability to explore larger search spaces within polynomial planning
time. Modern production systems address very large join sets
through hybrid strategies: PostgreSQL activates its Genetic Query
Optimizer (GEQO) when the number of tables exceeds a configurable
threshold, accepting a potentially suboptimal plan in exchange for
bounded planning time; newer adaptive query execution frameworks
re-optimize plans at runtime using cardinality feedback from
partially executed fragments. None of these approaches changes the
fundamental reality that any exact classical algorithm must
confront exponential worst-case cost beyond some problem size.
This complexity barrier motivates the exploration of fundamentally
different computational models for query optimization.

### Quantum Approaches to Database Optimization

Trummer and Koch (2016) were the first to apply quantum computing
to database query optimization, using a D-Wave 2X adiabatic
quantum annealer to solve the multiple query optimization problem
— demonstrating that a quantum annealing device could find valid
optimization plans, though the approach was constrained by the
limited qubit connectivity and count of that generation of
hardware [CITE Trummer 2016]. Schönberger et al. (2023)
formulated the join ordering problem as a QUBO and evaluated it
on D-Wave quantum annealers, demonstrating valid optimal plans
for queries involving up to five relations on real D-Wave hardware
and integrating their approach into PostgreSQL [CITE Schonberger
2023]. The authors discussed the theoretical applicability of
gate-based variational methods such as QAOA but did not execute
or systematically evaluate them on real gate-based quantum
processors. Uotila (2025) extended the encoding to higher-order
unconstrained binary optimization (HUBO) for left-deep join
trees, establishing theoretical bounds showing that the HUBO
formulation is equivalent in expressive power to the classical
DP search space [CITE Uotila 2025]. Experiments used randomly
generated query graphs of multiple structural types, with real
D-Wave execution limited to approximately seven to eight
relations due to hardware constraints. The common thread across
all three works is their exclusive reliance on quantum annealing
hardware (D-Wave) as the execution substrate. None evaluates
gate-based QAOA on a real superconducting processor, none uses
an industry-standard benchmark such as TPC-H, and none provides
a systematic comparison across the full simulation-to-hardware
fidelity spectrum — from ideal noiseless simulation through
synthetic noise injection to real device execution. The present
work fills precisely this gap.

### Positioning of the Present Work

The present work sits at the intersection of both research
streams. From the classical literature, we adopt the Selinger
cost model directly — catalog statistics, selectivity
estimation, and log-scaled intermediate result cardinalities
— grounding our QUBO formulation in the same cost framework
that underpins every production relational optimizer. From the
quantum literature, we depart from the annealing paradigm and
adopt gate-based QAOA on IBM superconducting hardware, using
the TPC-H industry benchmark rather than randomly generated
query graphs. Our unique contribution is to bridge the gap
between algorithmic formulation and empirical hardware reality:
we demonstrate that a correctly specified QUBO encoding of
join ordering can be solved exactly by QAOA in the noiseless
idealized setting, and we quantify — for the first time for
this problem class — the degradation in solution quality
across three tiers of realism: ideal simulation, synthetic
depolarizing noise, and execution on a real 156-qubit quantum
processor. The result is a reproducible end-to-end pipeline
from SQL query to quantum circuit to hardware measurement,
together with an honest characterization of where current
NISQ technology stands relative to classical baselines.