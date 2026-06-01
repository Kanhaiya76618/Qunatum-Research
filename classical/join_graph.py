class JoinGraph:
    """
    Stores TPC-H Q5 schema information:
    - Table cardinalities
    - Join graph
    - Join selectivities
    """

    def __init__(self):

        self.cardinalities = {
            "customer": 150000,
            "orders": 1500000,
            "lineitem": 6001215,
            "supplier": 10000,
            "nation": 25
        }

        self.edges = [
            ("customer", "orders"),
            ("orders", "lineitem"),
            ("lineitem", "supplier"),
            ("supplier", "nation")
        ]

        self.selectivities = {
            frozenset(["customer", "orders"]): 1 / 150000,
            frozenset(["orders", "lineitem"]): 1 / 1500000,
            frozenset(["lineitem", "supplier"]): 1 / 10000,
            frozenset(["supplier", "nation"]): 1 / 25
        }

    def get_tables(self):
        return list(self.cardinalities.keys())