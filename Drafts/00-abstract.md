## Abstract

Join order selection — determining the sequence in which a
relational query joins its input tables — is an NP-hard
combinatorial optimization problem whose exact solution requires
exponential cost under classical Selinger dynamic programming
(O(3^N)). While prior quantum approaches have addressed this
problem using quantum annealing on D-Wave hardware, no systematic
study has applied gate-based Quantum Approximate Optimization
Algorithm (QAOA) to join ordering using an industry-standard
benchmark. This paper presents an end-to-end QAOA-based framework
for join order optimization, formulating a 3-table subset of
TPC-H Query 5 as a 9-qubit Quadratic Unconstrained Binary
Optimization (QUBO) instance using one-hot positional encoding,
and evaluating the resulting circuit across four execution
configurations of increasing realism. On a noiseless statevector
simulator, QAOA at circuit depth p = 1 recovers the exact optimal
join order identified by classical diagonalization, validating
the correctness of the QUBO formulation. On real IBM quantum
hardware (ibm_kingston, 156 qubits), the transpiled circuit
reaches a depth of 263 layers and produces an output distribution
statistically indistinguishable from uniform random sampling
(peak probability 0.66%), empirically quantifying the coherence
gap of current NISQ devices. These results confirm that the QUBO
formulation is algorithmically sound, that hardware fidelity is
the binding practical constraint, and that the polynomial qubit
scaling of QAOA (O(N²)) motivates continued investigation as
quantum hardware matures toward fault tolerance.