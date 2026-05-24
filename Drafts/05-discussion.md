## 5. Discussion

### 5.1 Interpretation of Experimental Findings

The fact that noiseless QAOA at p = 1 recovers exactly the same
optimal join order and objective value as the classical
`NumPyMinimumEigensolver` proves that the QUBO formulation is
correctly specified: the encoding faithfully captures the join
ordering problem, and the penalty terms are weighted appropriately
to enforce valid permutation matrices. The 45% relative degradation
in solution probability when we introduced depolarizing errors of
0.1% on single-qubit gates and 1% on two-qubit gates shows that
QAOA solution quality is acutely sensitive to gate errors. Even
these modest error rates significantly flatten the output
probability distribution, implying that real-hardware performance
will depend critically on both circuit depth reduction and
error-mitigation techniques. The real-hardware result on
`ibm_kingston` demonstrates that synthetic depolarizing noise
models substantially underestimate the actual error environment of
a production quantum processor. The transpiled circuit depth of
263 gates pushed the computation well beyond the device's
effective coherence budget at this circuit depth, producing an
output distribution that is statistically indistinguishable from
uniform random sampling. This constitutes the empirical NISQ gap —
the chasm between the algorithmic promise of QAOA on idealized
simulators and what current hardware can actually deliver.

### 5.2 Limitations

We restricted our experiments to a 3-table subset because the
full 5-table TPC-H Query 5 instance would require 25 qubits (N²),
and classical statevector simulation of a 25-qubit circuit
exceeds the memory available on a standard workstation or the
Google Colab free tier. This memory barrier is itself the central
bottleneck that motivates quantum optimization — the classical
simulation memory grows as 2^(N²) in the worst case, while the
quantum resource cost stays at N² qubits. We limited the
experiment to p = 1 because higher p (e.g., p = 2 or p = 3)
produces deeper circuits with more two-qubit gates, which
amplifies cumulative noise and degrades the probability of
measuring the correct solution on current NISQ hardware. In
theory, higher p improves the approximation ratio, but on NISQ
devices the optimal choice of p is a hardware-aware trade-off
that we leave for future work. Our depolarizing noise model
applies a uniform symmetric error channel to every gate of the
same type, which is a convenient simplification but misses
several important real-device characteristics: T1/T2 decoherence,
measurement readout errors, crosstalk between neighboring qubits,
and gate-specific calibration drift that varies both spatially
across the chip and temporally between calibration cycles. A
more faithful noise model would incorporate device-specific
calibration data exported directly from the IBM backend at the
time of execution.

### 5.3 Implications and Outlook

Even though classical methods dominate at small N, the polynomial
qubit scaling (N²) versus the exponential classical operation
count (3^N) means that QAOA's logical gate count drops below
classical DP's operation count near N ≈ 9, though the practical
wall-clock crossover on real hardware lies considerably later.
This range is routinely encountered in data-warehouse and
analytical workloads, where queries joining 20 or more tables are
common. Several engineering and algorithmic advances must occur
before this approach becomes practically competitive: improvement
in gate fidelities and qubit coherence times, error correction or
mitigation sufficient to sustain transpiled circuit depths, and
hardware-efficient ansätze that compile the cost Hamiltonian into
circuits with substantially lower transpiled depth. Integration
with classical query optimizers as a hybrid execution layer would
also be required, so that quantum execution is invoked only when
classically intractable. The broader message of this work is that
the QUBO formulation and simulator pipeline are validated — the
QUBO encoding correctly captures join ordering, and QAOA solves
it exactly in the noiseless idealized setting. Real-hardware
execution at current NISQ fidelities is not yet competitive with
classical methods at any problem size we tested, but studies of
this kind prepare the algorithmic and methodological foundation
for the transition from NISQ devices to fault-tolerant or
near-fault-tolerant quantum systems.