## 2 Background.

## 2.1 SQL Joins and Cost-Based Optimization

In a relational database management system, users specify what data they want
through SQL without indicating how to retrieve it. The system optimizer is
responsible for choosing both the access path for each table and the order in
which joins are performed. Query processing in System R proceeds through four
phases: parsing, optimization, code generation, and execution. During
optimization, the system uses catalog statistics, selectivity estimation, and
a cost model to select the most efficient plan among many possible
alternatives [CITE Selinger 1979].

The join order matters because different orders produce different intermediate
result sizes. A bad order creates a huge intermediate table that the next join
must process, while a good order keeps intermediates small. The catalog
provides selectivity values used to estimate the size of each intermediate.
For the same query, two different join orders can differ in cost by several
orders of magnitude. The cost model used in System R, 
COST = PAGE FETCHES + W × RSI CALLS, balances I/O and CPU work, where W is a
tunable weight [CITE Selinger 1979].

Selinger et al. (1979) introduced the first dynamic programming method for
join ordering in the System R query optimizer. The algorithm builds optimal
subplans from the bottom up. For every subset of tables, it computes and
stores the cheapest plan for each interesting order, along with the cheapest
unordered plan. It then extends these subplans by adding one table at a time,
considering only those tables that connect to the existing subset through a
join predicate. This connectivity heuristic prunes Cartesian products early,
while equivalence classes reduce redundant work across symmetric subproblems.
The final output is a complete execution plan tree that specifies the optimal
join order, the access method for each table, and the join algorithm used at
each step. For N input tables, the algorithm enumerates O(2^N) subsets and,
for each subset, examines O(N) possible last-joined tables, giving an overall
worst-case time complexity of O(3^N) [CITE Selinger 1979][CITE Ibaraki Kameda
1984]. This makes the algorithm practical for queries with fewer than about
15 tables but prohibitive beyond that range.

Ibaraki and Kameda (1984) formally proved that finding the optimal join order for a given query is NP-hard, establishing a fundamental complexity barrier for query optimization [CITE Ibaraki Kameda 1984]. This result implies that no exact polynomial-time algorithm for arbitrary join ordering can exist unless P = NP, directly motivating the use of approximation methods and heuristic pruning techniques — such as the connectivity-based pruning in Selinger's dynamic programming approach and, more recently, quantum optimization methods such as QAOA.
## 2.2 QUBO Formulations for Combinatorial Optimization

Quadratic Unconstrained Binary Optimization (QUBO) provides a uniform way to
encode NP-hard combinatorial problems as the ground state of a problem
Hamiltonian, suitable for both gate-based quantum algorithms such as QAOA and
adiabatic quantum optimization on annealing hardware [CITE Lucas 2014]. The
standard formulation expresses the Hamiltonian as H = H_A + H_B, where H_A
introduces penalty terms that assign large positive energy to infeasible
configurations and H_B encodes the objective function to be minimized. By
choosing coefficients such that 0 < B · max(cost) < A, constraint violations
are never energetically favourable, ensuring that the ground state of H
corresponds to an optimal feasible solution of the original problem. Many
problems require a number of binary variables that grows quadratically with
input size — for instance, position-based one-hot encodings for permutation
problems use O(N²) spins — and global constraints such as acyclicity or
connectivity often need additional auxiliary variables.

Classical combinatorial optimization problems such as the Traveling Salesman
Problem and Maximum Cut can be directly cast as QUBO instances, and the same
mapping extends to a wide range of NP-hard problems including number
partitioning and minimum vertex cover [CITE Lucas 2014]. Any binary variable
x_i ∈ {0,1} maps to an Ising spin variable s_i ∈ {-1,+1} through the
relation x_i = (1 - s_i)/2, transforming the QUBO objective function into an
equivalent Ising Hamiltonian. Since both quantum annealing hardware and
gate-model variational algorithms such as QAOA naturally operate by minimizing
Ising Hamiltonians, any QUBO-encoded problem can be executed directly on
existing quantum processors without further reformulation — making QUBO the
universal interface between classical combinatorial problems and near-term
quantum hardware.

## 2.3 Quantum Approximate Optimization Algorithm

QAOA is a hybrid quantum-classical algorithm, meaning that computation is divided between a quantum processor and a classical optimizer working in tandem. The quantum processor prepares a parameterized quantum state using alternating operators and measures it to produce a candidate solution bitstring along with its associated cost. The classical optimizer receives this cost, updates the variational parameters, and returns them to the quantum processor — this loop repeats iteratively until the cost converges to a minimum [CITE Farhi 2014].
The algorithm is parameterized by an integer p, representing the number of alternating layers in the QAOA circuit. Each layer applies one cost operator and one mixing operator in sequence. As p increases, the approximation ratio — the ratio of the algorithm's expected objective value to the true optimum — improves, because the layered circuit more closely mimics continuous adiabatic time evolution. In the limit p → ∞, QAOA approaches the exact optimal solution. The trade-off is that deeper circuits introduce more noise on current hardware and make classical optimization of the variational parameters more difficult [CITE Farhi 2014].
*The cost operator UC(γ)=e−iγHCU_C(\gamma) = e^{-i\gamma H_C}
UC​(γ)=e−iγHC​ encodes the objective function by applying phase shifts that mark high-quality solutions — for instance, in MaxCut it penalizes edges whose endpoints are assigned to the same partition. The mixing operator UB(β)=e−iβBU_B(\beta) = e^{-i\beta B}
UB​(β)=e−iβB, where B=∑jXjB = \sum_j X_j
B=∑j​Xj​ is the transverse-field mixer, explores the solution space by rotating qubit states, preventing the circuit from becoming trapped in any single candidate solution. Together, the alternating application of these two operators drives the quantum state toward configurations that minimize the objective function.


