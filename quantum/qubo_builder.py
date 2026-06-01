import numpy as np

class QUBOBuilder:

    def __init__(self, graph):

        self.Q = None

        self.graph = graph

        self.tables = graph.get_tables()

        self.num_tables = len(self.tables)

        self.variables = {}

        self.reverse_variables = {}

        self.num_variables = 0

    def generate_variables(self):
        """
        Creates binary variables:

        x(table, position)

        Example:

        x(customer,0)
        x(customer,1)
        ...
        """

        index = 0

        for table in self.tables:

            for position in range(self.num_tables):

                self.variables[(table, position)] = index

                self.reverse_variables[index] = (
                    table,
                    position
                )

                index += 1

        self.num_variables = index

    def print_variables(self):

        print("\n===== QUBO VARIABLES =====\n")

        for key, value in self.variables.items():

            table, position = key

            print(
                f"x({table},{position}) -> {value}"
            )

        print(
            f"\nTotal Variables = {self.num_variables}"
        )

    def get_variable_index(
            self,
            table,
            position):

        return self.variables[
            (table, position)
        ]

    def get_variable_name(
            self,
            index):

        return self.reverse_variables[
            index
        ]
    
    def build_table_uniqueness_constraint(
            self,
            penalty = 10):
        n = self.num_variables

        self.Q = np.zeros((n, n))

        for table in self.tables:

            vars_for_table = []

            for position in range(
                    self.num_tables):

                idx = self.get_variable_index(
                    table,
                    position
                )

                vars_for_table.append(idx)

            # Diagonal terms

            for i in vars_for_table:

                self.Q[i, i] += -penalty

            # Pairwise terms

            for i in vars_for_table:

                for j in vars_for_table:

                    if i < j:

                        self.Q[i, j] += (
                            2 * penalty
                        )

        return self.Q
    
    def add_position_uniqueness_constraint(
            self,
            penalty = 10):
        """
        Every position must contain
        exactly one table.
        """

        for position in range(
                self.num_tables):

            vars_for_position = []

            for table in self.tables:

                idx = self.get_variable_index(
                    table,
                    position
                )

                vars_for_position.append(idx)

            # diagonal

            for i in vars_for_position:

                self.Q[i, i] += -penalty

            # pairwise

            for i in vars_for_position:

                for j in vars_for_position:

                    if i < j:

                        self.Q[i, j] += (
                            2 * penalty
                        )
    
    def print_qubo_matrix(
            self
    ):
        print("\n===== QUBO MATRIX =====\n")

        print(self.Q)


    def print_qubo_summary(self):

        print("\n===== QUBO SUMMARY =====")

        print(
            f"Variables: "
            f"{self.num_variables}"
        )

        print(
            f"Matrix Shape: "
            f"{self.Q.shape}"
        )

        print(
            f"Non-Zero Entries: "
            f"{np.count_nonzero(self.Q)}"
        )

        print(
            f"Min Value: "
            f"{self.Q.min()}"
        )

        print(
            f"Max Value: "
            f"{self.Q.max()}"
        )

        print(
            "\nSample Diagonal Entries:"
        )

        for i in range(
                min(10,
                    self.num_variables)
        ):

            print(
                f"Q[{i},{i}] = "
                f"{self.Q[i,i]:.4f}"
            )

    def add_cardinality_cost(
            self,
            scale = 0.00001):
        """
        Adds table cardinality cost.

        Smaller tables are preferred
        in earlier positions.
        """

        for table in self.tables:

            cardinality = (
                self.graph.cardinalities[
                    table
                ]
            )

            for position in range(
                    self.num_tables):

                idx = self.get_variable_index(
                    table,
                    position
                )

                weight = (
                    position + 1
                )

                cost = (
                    cardinality *
                    weight *
                    scale
                )

                self.Q[idx, idx] += cost

    def add_join_selectivity_cost(
        self,
        scale=0.00001):
        """
        Reward placing tables that share
        a join edge close together.

        Lower join cardinality
        -> lower energy

        Higher join cardinality
        -> higher energy
        """

        for edge, selectivity in self.graph.selectivities.items():

            table_a, table_b = tuple(edge)

            cardinality_a = (
                self.graph.cardinalities[
                    table_a
                ]
            )

            cardinality_b = (
                self.graph.cardinalities[
                    table_b
                ]
            )

            join_size = (
                cardinality_a *
                cardinality_b *
                selectivity
            )

            cost = join_size * scale

            # Encourage adjacent placement

            for pos in range(
                    self.num_tables - 1):

                idx_a = self.get_variable_index(
                    table_a,
                    pos
                )

                idx_b = self.get_variable_index(
                    table_b,
                    pos + 1
                )

                self.Q[idx_a, idx_b] += cost

                # symmetric term

                self.Q[idx_b, idx_a] += cost

    def add_intermediate_result_cost(
        self,
        scale=0.000001):
        """
        Approximate intermediate-result growth.

        Later positions become exponentially
        more expensive.
        """

        for table in self.tables:

            cardinality = (
                self.graph.cardinalities[
                    table
                ]
            )

            for position in range(
                    self.num_tables):

                idx = self.get_variable_index(
                    table,
                    position
                )

                growth_weight = (
                    2 ** position
                )

                cost = (
                    cardinality *
                    growth_weight *
                    scale
                )

                self.Q[idx, idx] += cost

        
    

    def print_cost_statistics(self):

        print("\n===== COST STATISTICS =====")

        print(
            f"Matrix Shape: {self.Q.shape}"
        )

        print(
            f"Non-Zero Entries: "
            f"{np.count_nonzero(self.Q)}"
        )

        print(
            f"Min Value: {self.Q.min():.6f}"
        )

        print(
            f"Max Value: {self.Q.max():.6f}"
        )

        print(
            f"Matrix Sum: {self.Q.sum():.6f}"
        )

    