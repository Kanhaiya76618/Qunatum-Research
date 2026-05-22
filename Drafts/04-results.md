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