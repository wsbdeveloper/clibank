class Operation:
    """ Model the operations the transaction"""

    def __init__(self, operation: str, unit_cost: float, quantity: int):
        self.operation = operation
        self.unit_cost = unit_cost
        self.quantity = quantity
    
