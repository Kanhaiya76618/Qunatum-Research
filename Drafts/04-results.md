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

### 4.5 QAOA on Real IBM Quantum Hardware

We submitted the QAOA circuit to `ibm_kingston`, a 156-qubit
superconducting quantum processor available through the IBM
Quantum Platform. Transpilation decomposes the abstract QAOA
gates into the device's native gate set {`rz`, `sx`, `x`, `cz`,
`id`} and maps them onto the physical qubit topology. The
resulting transpiled circuit had a depth of 263 layers with 595
total native gate operations. The most probable measurement
outcome was the bitstring `110011001`, occurring 27 out of 4096
shots (0.66%). When decoded, this corresponds to the join order
`orders` → `lineitem` → `lineitem`, which is an invalid
permutation as `lineitem` appears twice while `customer` is
absent from the sequence. Crucially, the measured distribution
is essentially uniform — 0.66% is barely above the 1/512 ≈ 0.20%
uniform-random baseline for a 9-qubit system, indicating that
the 263-layer transpiled depth exceeds the coherent execution
window of current NISQ hardware. This constitutes our central
empirical finding: even a minimal three-table QAOA instance loses
essentially all coherent signal when executed on real hardware,
because transpilation overhead pushes the effective gate count
beyond the coherence budget of today's NISQ processors.

### 4.6 Summary and Observations

Across all four configurations, the classical exact solver is the
clear winner at N = 3: it returns the exact optimum in 18
milliseconds. Clean QAOA matches that optimum but takes 103
seconds, approximately 5,600× slower. A realistic depolarizing
noise model degrades the correct-solution probability by 45%
relative to the noiseless run. On real IBM Quantum hardware,
coherent signal collapses entirely, and the output distribution
becomes indistinguishable from uniform random sampling. The
progression of peak probabilities tells the story: 100%
(classical exact) → 2.01% (noiseless QAOA) → 1.11% (noisy
simulator) → 0.66% (real hardware) — a continuous decay from
perfect certainty to essentially uniform noise, with each layer
of realism stripping away more of the apparent quantum advantage.
The take-home message is clear: at small problem sizes, classical
methods dominate on every axis — speed, accuracy, and reliability.
The value of QAOA lies in its asymptotic and theoretical scaling,
not in present-day practical performance. The substantial gap
between what simulators promise and what real hardware delivers
is the central challenge the field must address before quantum
query optimization can become viable in practice.