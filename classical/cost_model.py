operation_count = 0

def reset_operation_count():
    global operation_count
    operation_count = 0

def get_operation_count():
    return operation_count


def estimate_join_size(
        tables,
        cardinalities,
        selectivities):
    """
    Estimate cardinality of joining a set of tables.

    Formula:
    Product(cardinalities)
    *
    Product(selectivities)
    """
    global operation_count
    operation_count += 1
    
    size = 1.0

    for table in tables:
        size *= cardinalities[table]

    for edge, sel in selectivities.items():

        if edge.issubset(tables):
            size *= sel

    return max(size, 1.0)


def compute_plan_cost(
        ordering,
        cardinalities,
        selectivities):
    """
    Compute total cost of a join order.

    Cost =
    Sum of intermediate result sizes.
    """

    total_cost = 0.0

    current_tables = set()

    for table in ordering:

        current_tables.add(table)

        size = estimate_join_size(
            frozenset(current_tables),
            cardinalities,
            selectivities
        )

        total_cost += size

    return total_cost