## 7. Conclusion and Future Work

### Conclusion

This paper presents an end-to-end study of QAOA applied to the
join order selection problem in relational databases. We
formulated a 3-table subset of TPC-H Query 5 as a 9-qubit QUBO
instance using one-hot positional encoding, and evaluated the
resulting QAOA circuit across four execution configurations of
increasing realism. Three findings emerge. First, noiseless QAOA
at p = 1 recovers the exact optimal join order identified by
classical diagonalization, validating the correctness of the
QUBO formulation. Second, a synthetic depolarizing noise model
reduces the peak solution probability by 45%, demonstrating
QAOA's sensitivity to gate errors even at modest error rates.
Third, execution on the real `ibm_kingston` 156-qubit processor
produces an output distribution statistically indistinguishable
from uniform random sampling, with a peak probability of 0.66%
at a transpiled circuit depth of 263 layers — empirically
establishing that current NISQ hardware cannot sustain coherent
computation at this circuit depth. Taken together, these results
confirm that the algorithmic formulation is sound, but that
hardware fidelity remains the binding constraint preventing
quantum query optimization from being practically competitive
today.

### Future Work

Several directions remain open for future investigation. On the
hardware side, the most pressing need is for error-mitigation
techniques — particularly zero-noise extrapolation and
probabilistic error cancellation — that could recover useful
solution signal from circuits whose transpiled depth currently
exceeds the device coherence budget. On the algorithmic side,
hardware-efficient ansätze that compile the cost Hamiltonian
into circuits with substantially lower native gate counts would
reduce transpiled depth and bring real-hardware execution closer
to the noiseless-simulation regime; increasing circuit depth
beyond p = 1 would also improve the approximation ratio,
provided that error-mitigation advances keep pace. On the
benchmark side, extending experiments to the full 5-table TPC-H
Q5 schema (25 qubits) and to TPC-H Q8 (8 tables, 64 qubits
under one-hot encoding) would require either hardware with
larger memory for classical simulation or a more qubit-efficient
encoding such as binary-tree positional encoding. Looking
further ahead, a hybrid classical-quantum optimizer — invoking
classical Selinger DP for small N where it dominates, and
switching to QAOA for large N where classical methods become
intractable — represents a practically motivated architecture
worth investigating. Finally, the current QUBO formulation
assumes inner joins exclusively; extending it to outer joins
(LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN) requires reconsidering
the commutativity and associativity assumptions that underpin
the permutation-matrix encoding, a non-trivial open problem
that we leave for future work.