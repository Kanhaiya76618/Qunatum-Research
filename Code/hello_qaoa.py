# hello_qaoa.py — verify Qiskit works on a tiny MaxCut problem
import numpy as np
from qiskit_optimization.applications import Maxcut
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler

# A simple 4-node graph adjacency matrix
adjacency = np.array([
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 0],
])

# Build MaxCut problem from the graph
maxcut = Maxcut(adjacency)
qp = maxcut.to_quadratic_program()
print("Problem:")
print(qp.prettyprint())

# Solve with QAOA p=1
qaoa = QAOA(sampler=StatevectorSampler(), optimizer=COBYLA(), reps=1)
solver = MinimumEigenOptimizer(qaoa)
result = solver.solve(qp)

print("Optimal solution:", result.x)
print("Objective value:", result.fval)