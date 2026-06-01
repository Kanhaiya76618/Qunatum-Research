import time
from classical.selinger_dp import SelingerDP

from classical.cost_model import (
    reset_operation_count,
    get_operation_count
)


class SyntheticGraph:

    def __init__(self, n):

        self.cardinalities = {
            f"T{i}": 1000 * (i + 1)
            for i in range(n)
        }

        self.selectivities = {}

        tables = list(
            self.cardinalities.keys()
        )

        for i in range(n - 1):

            self.selectivities[
                frozenset(
                    [tables[i],
                     tables[i + 1]]
                )
            ] = 0.001

    def get_tables(self):

        return list(
            self.cardinalities.keys()
        )


results = []

for n in range(3, 9):

    graph = SyntheticGraph(n)

    reset_operation_count()

    optimizer = SelingerDP(graph)

    start = time.perf_counter()

    cost, order = optimizer.optimize()

    elapsed = (
        time.perf_counter()
        - start
    )

    operations = (
        get_operation_count()
    )

    results.append(
        (
            n,
            operations,
            elapsed * 1000
        )
    )

print("\nSCALING RESULTS\n")

for r in results:

    print(
        f"N={r[0]} | "
        f"Ops={r[1]} | "
        f"Time={r[2]:.3f} ms"
    )

print("\nRaw Results:")
print(results)