# qubo_builder.py
# SQL → QUBO mapping for TPC-H Q5 join order optimization

import numpy as np
from qiskit_optimization import QuadraticProgram

# Tables and their row counts (TPC-H scale factor 1)
TABLES = ['customer', 'orders', 'lineitem', 'supplier', 'nation']
CARDS = {
    'customer': 150_000,
    'orders':   1_500_000,
    'lineitem': 6_001_215,
    'supplier': 10_000,
    'nation':   25,
}

# Join edges with selectivity values
JOIN_EDGES = {
    frozenset(['customer', 'orders']):   1/150_000,
    frozenset(['orders',   'lineitem']): 1/1_500_000,
    frozenset(['lineitem', 'supplier']): 1/10_000,
    frozenset(['supplier', 'nation']):   1/25,
}

N = len(TABLES)  # 5 tables

# Cost function for joining two tables
def pair_cost(i: int, j: int) -> float:
    t1, t2 = TABLES[i], TABLES[j]
    edge = frozenset([t1, t2])
    if edge in JOIN_EDGES:
        sel = JOIN_EDGES[edge]
        cost = CARDS[t1] * CARDS[t2] * sel
        return np.log10(max(cost, 1.0))
    else:
        return 15.0  # penalty for non-adjacent tables

# # Test it
# if __name__ == '__main__':
#     print("Join cost table:")
#     for i in range(N):
#         for j in range(N):
#             if i != j:
#                 c = pair_cost(i, j)
#                 print(f"  {TABLES[i]:10} ↔ {TABLES[j]:10} = {c:.2f}")

def build_qubo(penalty: float = 200.0) -> QuadraticProgram:
    qp = QuadraticProgram('tpch_q5_join_order')

    # Add 25 binary variables: x_i_p
    # x_i_p = 1 means table i is at position p
    for i in range(N):
        for p in range(N):
            qp.binary_var(name=f'x_{i}_{p}')

    linear = {}
    quadratic = {}

    # Constraint A: each row sums to 1
    # (each table appears at exactly one position)
    for i in range(N):
        for p in range(N):
            key = f'x_{i}_{p}'
            linear[key] = linear.get(key, 0) - 2 * penalty
        for p1 in range(N):
            for p2 in range(p1 + 1, N):
                key = (f'x_{i}_{p1}', f'x_{i}_{p2}')
                quadratic[key] = quadratic.get(key, 0) + 2 * penalty

    # Constraint B: each column sums to 1
    # (each position has exactly one table)
    for p in range(N):
        for i in range(N):
            key = f'x_{i}_{p}'
            linear[key] = linear.get(key, 0) - 2 * penalty
        for i1 in range(N):
            for i2 in range(i1 + 1, N):
                key = (f'x_{i1}_{p}', f'x_{i2}_{p}')
                quadratic[key] = quadratic.get(key, 0) + 2 * penalty

    # Cost C: join cost between adjacent positions
    for p in range(N - 1):
        for i in range(N):
            for j in range(N):
                if i != j:
                    key = (f'x_{i}_{p}', f'x_{j}_{p+1}')
                    quadratic[key] = quadratic.get(key, 0) + pair_cost(i, j)

    # Constant term: N * 2 * penalty (from expanding (sum - 1)^2)
    constant = N * 2 * penalty

    qp.minimize(linear=linear, quadratic=quadratic, constant=constant)
    return qp


# Test the builder
if __name__ == '__main__':
    qp = build_qubo()
    print(f'Variables:       {qp.get_num_vars()}')
    print(f'Quadratic terms: {len(qp.objective.quadratic.to_dict())}')
    print(f'Linear terms:    {len(qp.objective.linear.to_dict())}')
    print('\nFirst 3 lines of problem:')
    lines = qp.prettyprint().split('\n')
    for line in lines[:8]:
        print(line)