# Figure Captions for Paper

## Figure 1
Fig. 1: Join graph for the 3-table subset of TPC-H Query 5.
Nodes show base relation cardinalities at scale factor 1; edges
are foreign-key joins annotated with estimated selectivities and
their underlying predicates. The optimization problem is to find
the join order minimizing the total intermediate cardinality.

## Figure 2
Fig. 2: Peak measurement probability of the optimal bitstring
across four execution configurations (log scale). Classical exact
diagonalization yields 100% certainty; noiseless QAOA at p=1
recovers a 2.01% peak; depolarizing noise reduces this to 1.11%;
real-hardware execution on ibm_kingston yields 0.66% — barely
above the 0.20% uniform-random baseline for a 9-qubit system.
The progression quantifies the gap between simulator promise and
NISQ-hardware reality.

## Figure 3
Fig. 3: Asymptotic scaling of three join-ordering methods on
a logarithmic operation count (y-axis) versus number of tables N
(x-axis). Naive exhaustive search grows factorially (N!),
classical Selinger dynamic programming grows exponentially (3^N),
and QAOA's logical gate count at p = 2 grows polynomially (2·N⁴).
Two crossovers emerge: Selinger DP overtakes exhaustive search at
N ≈ 8, marking the 1979 algorithmic breakthrough; and QAOA's
logical gate count drops below DP's operation count at N ≈ 9,
marking the asymptotic threshold beyond which quantum optimization
becomes attractive in principle. Real-hardware wall-clock
crossover lies considerably later due to variational-loop
overhead, shot noise, and queue latency. Our N = 3 experiment
falls in the classical-favored regime, where direct
diagonalization is ~5,600× faster than noiseless QAOA simulation.