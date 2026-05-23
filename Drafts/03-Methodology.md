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

### 3.2 QUBO Encoding

Each binary variable x_{i,p} is 1 if table i is placed at position
p in the join order, and 0 otherwise. This is a one-hot positional
encoding, ensuring that every table is assigned to exactly one
slot in the sequence. For an N-table problem, this yields N²
binary variables in total. In our experiments with three tables,
this corresponds to nine qubits; a five-table TPC-H Q5 instance
would require 25 qubits. A valid solution is a permutation matrix:
exactly one 1 in each row (every table occupies exactly one
position) and exactly one 1 in each column (every position holds
exactly one table). Any assignment violating either constraint is
infeasible and is penalized in the Hamiltonian. One-hot encoding
is the standard choice in the QUBO literature because the
permutation constraints translate directly into simple quadratic
penalty terms, and decoding measurement outcomes back into join
orders is straightforward. The alternative — binary-tree
positional encoding — uses only N log₂ N qubits by encoding each
position as a binary index, but the resulting QUBO formulation is
far more complex: the constraints are harder to express as
quadratic penalties, and the cost interactions between table pairs
become higher-order rather than quadratic, making the resulting
Hamiltonian unsuitable for standard QAOA, which operates on
quadratic cost functions.

### 3.3 Cost Function Components

The full objective Hamiltonian decomposes into three additive
components: H = H_A + H_B + H_C, where H_A and H_B encode the row
and column permutation constraints, and H_C encodes the join cost
we wish to minimize.

H_A enforces the row constraint: every table must appear at
exactly one position in the join order. It penalizes any
assignment in which a table is placed at zero positions or at
multiple positions simultaneously. Formally,

  H_A = A · Σ_{i=1}^{N} ( Σ_{p=1}^{N} x_{i,p} − 1 )²,

where A is a penalty coefficient chosen large enough to ensure
that any infeasible configuration is energetically unfavourable
relative to all feasible ones.

H_B enforces the column constraint: every position in the join
order must hold exactly one table. It mirrors H_A across columns:

  H_B = B · Σ_{p=1}^{N} ( Σ_{i=1}^{N} x_{i,p} − 1 )².

Any column containing zero or multiple tables incurs the same
large penalty.

H_C encodes the actual join cost to be minimized. For each pair
of adjacent positions p and p+1, we sum the cost of joining
whichever tables occupy them:

  H_C = Σ_{p=1}^{N−1} Σ_{i=1}^{N} Σ_{j=1}^{N}
        cost(i, j) · x_{i,p} · x_{j,p+1}.

The product x_{i,p} · x_{j,p+1} evaluates to 1 only when table i
sits at position p and table j sits at position p+1, so exactly
one pairwise cost term contributes per adjacency in any feasible
solution.

The pairwise cost is derived from the database catalog:
cost(i, j) = log₁₀(card_i · card_j · sel_{i,j}) when tables i
and j are connected by a join predicate in the query graph, and
a fixed penalty of 15.0 when they are not directly joinable. The
latter case discourages Cartesian-product joins from appearing in
the optimal plan.

### 3.4 Penalty Weighting Strategy

To guarantee feasibility, the penalty coefficients A and B must
each be larger than the maximum possible join cost — otherwise
the optimizer could save more energy by violating a constraint
than by satisfying it. We set A = B = 500.0, which is
approximately 70× above the maximum pairwise join cost of 6.78
in our three-table instance, providing a comfortable feasibility
margin. When we initially tried a lower penalty of 200, the
optimizer returned a configuration decoding to `orders, orders,
lineitem` — an infeasible assignment with a duplicate table —
because the join-cost savings from violating the permutation
constraint outweighed the penalty paid. Conversely, setting the
penalties too high introduces a different problem: if the penalty
terms dominate by several orders of magnitude, the join-cost
differences become numerically negligible within the objective
function, and the variational optimizer effectively ignores plan
quality and focuses only on feasibility.