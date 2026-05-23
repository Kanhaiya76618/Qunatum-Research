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
Fig. 3: Asymptotic scaling of three join-ordering methods plotted
on a logarithmic operation count (y-axis) versus number of tables
N (x-axis). Exhaustive search grows factorially (N!), classical
Selinger dynamic programming grows exponentially (3^N), while
QAOA's gate count grows polynomially as 2·N^4. The curves cross
near N≈18, beyond which QAOA's quantum resource requirements
become smaller than classical DP's classical operation count.
The gold star marks our experimental N=3 instance, where
classical methods remain decisively more efficient.