## 4. Results

### 4.1 Experimental Setup

We encoded a three-table join ordering problem from TPC-H Query 5
(tables `customer`, `orders`, `lineitem`) as a QUBO instance, in
which each table is assigned to one position in the join order and
the objective cost is based on the estimated intermediate result
size. The QUBO formulation requires 9 qubits (N² for N = 3 tables
with a one-hot positional encoding) and a penalty weight of 500.0
to enforce that each table occupies exactly one position and each
position holds exactly one table. All experiments were conducted
using the Qiskit framework, with Qiskit Optimization for QUBO
construction, Qiskit Aer for both noiseless and noisy simulated
backends, and Qiskit IBM Runtime to submit the circuit to a real
quantum processor. We compare four configurations: (1) a classical
`NumPyMinimumEigensolver` as the exact baseline, (2) noiseless QAOA
(p=1, ideal statevector simulation), (3) noisy QAOA (p=1 with 0.1%
single-qubit and 1% two-qubit depolarizing error on AerSimulator),
and (4) the same QAOA circuit executed on real IBM quantum hardware.

### 4.2 Classical Exact Baseline

The `NumPyMinimumEigensolver` computes the exact ground state of
the QUBO Hamiltonian by direct diagonalization of the 2⁹ × 2⁹ =
512 × 512 Hamiltonian matrix, yielding the provably optimal join
order with no approximation error. The optimal join order was
`customer` → `orders` → `lineitem`, with an objective value of
−2987.0457. The computation took 18.31 ms on a standard Google
Colab CPU runtime. This result serves as the gold-standard
reference against which all subsequent QAOA experiments are
compared.

### 4.3 QAOA on Noiseless Simulator

For the noiseless QAOA configuration, we used the
`StatevectorSampler` with COBYLA as the classical optimizer
(50 iterations maximum) and a single QAOA layer (p = 1). The
optimal variational angles found by COBYLA were γ = 3.6333 and
β = −5.9390. QAOA recovered the same join order as the classical
baseline (`customer` → `orders` → `lineitem`) with an identical
objective value of −2987.0457, confirming successful recovery of
the global optimum. The QAOA simulation took 103.6 s, approximately
5,600× slower than the classical solver's 18 ms. This validates
that QAOA correctly solves the QUBO at p = 1 for this small
instance, while highlighting that the overhead of the variational
loop (which invokes the quantum circuit simulator once per
optimizer evaluation) is far higher than direct diagonalization
at this scale.

### 4.4 QAOA under Simulated Depolarizing Noise

We applied a depolarizing noise model with 0.1% error probability
on single-qubit gates (`rz`, `rx`, `h`, `x`) and 1% on two-qubit
`CX` gates, parameters chosen to approximate the gate fidelity
levels of current IBM superconducting quantum processors. We
reused the optimal angles from the clean QAOA run (γ = 3.6333,
β = −5.9390) rather than re-optimizing under noise, because the
`qiskit-aer` sampler primitive does not natively support the
high-level `QAOA` gate composite. We manually constructed the QAOA
circuit with the same variational parameters and executed it
under the noise model — a standard methodology for isolating the
effect of hardware noise from variational-optimizer convergence
behavior. In the noiseless run with 8192 measurement shots, the
peak measurement probability was 2.01%. Under the depolarizing
noise model, the same bitstring's probability dropped to 1.11% —
a 45% relative degradation. This indicates that even mild
depolarizing noise significantly flattens the QAOA probability
landscape: the correct solution remains the most probable outcome,
but its margin shrinks considerably. Increasing circuit depth
(higher p) would worsen the degradation, suggesting that
error-mitigation techniques will be necessary before QAOA can be
deployed for production-grade query optimization on real hardware.