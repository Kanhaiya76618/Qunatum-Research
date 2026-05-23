## 3. Methodology

### 3.1 Problem Formulation

The input to the optimization problem is a set of N database tables
with their cardinality estimates (row counts) and the join
selectivity values between table pairs, all obtained from the
database catalog. The output is a permutation of the N tables that
minimizes the total estimated join cost (in our formulation, the
sum of log-scaled intermediate result cardinalities). Join ordering
is NP-hard: there are N! possible permutations, and Selinger-style
dynamic programming reduces the search to O(3^N) subset evaluations,
which remains exponential and becomes intractable beyond roughly
15 tables. A QUBO encoding enables the application of quantum
optimization methods such as QAOA, where the qubit count grows
polynomially as N² (under one-hot positional encoding), independent
of the factorial size of the underlying search space — ensuring
that the quantum resource requirements remain polynomial even
though the underlying combinatorial search space is factorial.

