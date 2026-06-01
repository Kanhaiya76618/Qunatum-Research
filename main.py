# main.py

from classical.join_graph import JoinGraph
from classical.selinger_dp import SelingerDP

from quantum.qubo_builder import QUBOBuilder


def run_classical_baseline():

    print("\n" + "=" * 50)
    print("CLASSICAL SELINGER DP")
    print("=" * 50)

    graph = JoinGraph()

    optimizer = SelingerDP(graph)

    best_cost, best_order = optimizer.optimize()

    print("\nOptimal Join Order:\n")
    print(" -> ".join(best_order))

    print("\nEstimated Cost:")
    print(f"{best_cost:,.2f}")


def run_qubo_variables():

    print("\n" + "=" * 50)
    print("QUBO VARIABLE GENERATION")
    print("=" * 50)

    graph = JoinGraph()

    qubo = QUBOBuilder(graph)

    qubo.generate_variables()

    qubo.print_variables()

def run_qubo_constraints():
    graph = JoinGraph()

    qubo = QUBOBuilder(graph)

    qubo.generate_variables()

    qubo.build_table_uniqueness_constraint()

    qubo.add_position_uniqueness_constraint()

    qubo.add_cardinality_cost()

    qubo.add_join_selectivity_cost()

    qubo.add_intermediate_result_cost()

    qubo.print_qubo_summary()

    qubo.print_cost_statistics()



def main():

    # Uncomment whichever phase you want to run

    # Phase 1
    #run_classical_baseline()

    # Phase 2
    #run_qubo_variables()

    # QUBO Matrix
    run_qubo_constraints()


if __name__ == "__main__":
    main()