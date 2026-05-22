# run_qaoa.py
# QAOA simulation for TPC-H Q5 join order optimization

import time
import numpy as np
from qubo_builder import build_qubo, TABLES, N

from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer

def decode_solution(x, n=N):
    """Convert 25-element binary vector back to join order."""
    order = [None] * n
    for i in range(n):
        for p in range(n):
            if round(x[i * n + p]) == 1:
                order[p] = TABLES[i]
    return order


def is_valid_permutation(order):
    """Check if decoded order is a valid join sequence."""
    return None not in order and len(set(order)) == N


def run_qaoa(reps=1, seed=42):
    print(f"Building QUBO for TPC-H Q5 ({N} tables, {N*N} qubits)...")
    qp = build_qubo(penalty=200.0)
    print(f"Variables: {qp.get_num_vars()}")
    print(f"Starting QAOA p={reps}... (this takes 5-30 minutes)")

    np.random.seed(seed)
    sampler = StatevectorSampler()
    optimizer = COBYLA(maxiter=100)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    solver = MinimumEigenOptimizer(qaoa)

    start = time.perf_counter()
    result = solver.solve(qp)
    elapsed = time.perf_counter() - start

    print(f"\n=== RESULTS ===")
    print(f"Time taken:      {elapsed:.1f} seconds")
    print(f"Objective value: {result.fval:.4f}")
    print(f"Solution vector: {result.x}")

    order = decode_solution(result.x)
    valid = is_valid_permutation(order)

    print(f"Decoded order:   {order}")
    print(f"Valid solution:  {valid}")

    return result, order, elapsed


if __name__ == '__main__':
    result, order, elapsed = run_qaoa(reps=1)