import itertools

from classical.cost_model import (
    estimate_join_size,
    compute_plan_cost
)


class SelingerDP:

    def __init__(self, graph, verbose = False):

        self.graph = graph
        self.verbose = verbose


        self.cardinalities = graph.cardinalities
        self.selectivities = graph.selectivities

    def optimize(self):

        tables = self.graph.get_tables()

        best = {}

        # --------------------
        # Base Case
        # --------------------

        for table in tables:

            best[frozenset([table])] = (
                0.0,
                [table]
            )

        # --------------------
        # DP Build-Up
        # --------------------

        n = len(tables)

        for size in range(2, n + 1):

            for subset in itertools.combinations(
                    tables,
                    size):

                subset = frozenset(subset)

                best_cost = float("inf")
                best_order = None

                for left_size in range(1, size):

                    for left in itertools.combinations(
                            subset,
                            left_size):

                        left = frozenset(left)

                        right = subset - left

                        if left not in best:
                            continue

                        if right not in best:
                            continue

                        left_order = best[left][1]
                        right_order = best[right][1]

                        candidate_order = (
                                left_order +
                                right_order
                        )

                        candidate_cost = compute_plan_cost(
                            candidate_order,
                            self.cardinalities,
                            self.selectivities
                        )

                        if candidate_cost < best_cost:

                            best_cost = candidate_cost
                            best_order = candidate_order

                best[subset] = (
                    best_cost,
                    best_order
                )

                if self.verbose:
                    print(
                        f"{set(subset)}"
                        f" -> Cost: {best_cost:,.2f}"
                        f" -> Order: {best_order}"
                    )

        return best[frozenset(tables)]